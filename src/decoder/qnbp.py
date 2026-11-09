"""Orbit-Tied Quantized Neural Belief Propagation (QNBP) Module for BB Codes.

Implements unfolded Min-Sum BP with automorphism orbit weight tying, signed memory,
power-of-two quantization, and numerically stable log-domain observable loss.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from src.data.dem_graph import DemGraph
from src.decoder.quantization import PowerOfTwoQuantizer, SteClamp


class OrbitTiedQNBP(nn.Module):
    """Unfolded Neural Belief Propagation decoder with orbit weight tying.

    Weights alpha and gamma are tied across DEM symmetry orbits under G = Z_l x Z_m.

    Attributes:
        graph: DemGraph representing the DEM bipartite graph.
        num_layers: Number of unfolded BP iterations T.
        bit_width: Integer quantization bit-width k (4, 5, or 6 bits).
        quantize: Whether to apply power-of-two quantization.
        orbit_alpha: Learnable scaling parameters of shape (T, num_fault_orbits).
        orbit_gamma: Learnable memory parameters of shape (T, num_fault_orbits).
        class_offsets: Learnable boundary class offsets of shape (T, 3).
    """

    def __init__(
        self,
        graph: DemGraph,
        num_layers: int = 15,
        bit_width: int = 4,
        quantize: bool = True,
        initial_alpha: float = 0.75,
        initial_gamma: float = 0.0,
        custom_orbits: Optional[torch.Tensor] = None,
        use_boundary_classes: bool = True,
    ) -> None:
        super().__init__()
        self.graph = graph
        self.num_layers = num_layers
        self.bit_width = bit_width
        self.quantize = quantize
        self.use_boundary_classes = use_boundary_classes

        # Orbit assignments: either geometric orbits, random groups, or untied
        if custom_orbits is not None:
            active_orbits = custom_orbits
        else:
            active_orbits = graph.fault_orbits

        num_orbits = int(torch.max(active_orbits).item()) + 1
        num_classes = int(torch.max(graph.fault_classes).item()) + 1

        # Learnable orbit-tied parameters
        self.orbit_alpha = nn.Parameter(
            torch.full((num_layers, num_orbits), float(initial_alpha), dtype=torch.float32)
        )
        self.orbit_gamma = nn.Parameter(
            torch.full((num_layers, num_orbits), float(initial_gamma), dtype=torch.float32)
        )
        self.class_offsets = nn.Parameter(
            torch.zeros((num_layers, num_classes), dtype=torch.float32),
            requires_grad=use_boundary_classes,
        )

        # Power-of-two quantizer
        self.quantizer = PowerOfTwoQuantizer(bit_width=bit_width, initial_shift=2.0)

        # Graph buffers (non-trainable)
        self.register_buffer("priors", graph.priors)
        self.register_buffer("fault_orbits", active_orbits)
        self.register_buffer("fault_classes", graph.fault_classes)
        self.register_buffer("check_nodes", graph.check_nodes_per_edge)
        self.register_buffer("fault_nodes", graph.fault_nodes_per_edge)
        self.register_buffer("obs_matrix", graph.obs_matrix)

        self.check_to_edges = graph.check_to_edges
        self.fault_to_edges = graph.fault_to_edges

        # Precompute check-to-edge padded tensors for vectorized CNU
        num_checks = graph.num_detectors
        max_deg = max((len(e) for e in graph.check_to_edges), default=0)
        num_edges = graph.num_edges

        c_edge_idx = torch.full((num_checks, max_deg), num_edges, dtype=torch.long)
        c_mask = torch.zeros((num_checks, max_deg), dtype=torch.bool)

        for c, e_idx in enumerate(graph.check_to_edges):
            if e_idx:
                c_edge_idx[c, :len(e_idx)] = torch.tensor(e_idx, dtype=torch.long)
                c_mask[c, :len(e_idx)] = True

        valid_edges = c_edge_idx[c_mask]
        inv_perm = torch.empty_like(valid_edges)
        if len(valid_edges) > 0:
            inv_perm[valid_edges] = torch.arange(num_edges)

        self.register_buffer("c_edge_idx", c_edge_idx)
        self.register_buffer("c_mask", c_mask)
        self.register_buffer("inv_perm", inv_perm)

    def forward(
        self, syndromes: torch.Tensor
    ) -> List[Tuple[torch.Tensor, torch.Tensor]]:
        """Executes T unfolded iterations of orbit-tied belief propagation.

        Args:
            syndromes: Tensor of shape (B, num_detectors) containing binary syndromes.

        Returns:
            List of T tuples: (posteriors, hard_corrections) for each iteration t.
        """
        b_size = syndromes.shape[0]
        num_faults = self.graph.num_faults
        num_edges = self.graph.num_edges

        # Variable-to-check messages: shape (B, num_edges)
        init_llr = self.priors[self.fault_nodes].unsqueeze(0).expand(b_size, -1)
        msg_v2c = self.quantizer(init_llr) if self.quantize else init_llr.clone()

        posteriors = self.priors.unsqueeze(0).expand(b_size, -1).clone()
        prev_posteriors = posteriors.clone()

        outputs: List[Tuple[torch.Tensor, torch.Tensor]] = []

        for t in range(self.num_layers):
            # Compute effective weights for this iteration
            alpha_f = self.orbit_alpha[t, self.fault_orbits] + self.class_offsets[t, self.fault_classes]
            alpha_edge = alpha_f[self.fault_nodes]
            gamma_f = self.orbit_gamma[t, self.fault_orbits]

            # 1. Check Node Update (CNU)
            msg_c2v = self._cnu_forward(syndromes, msg_v2c, alpha_edge)
            if self.quantize:
                msg_c2v = self.quantizer(msg_c2v)

            # 2. Variable Node Update (VNU)
            prev_posteriors = posteriors.clone()
            posteriors, msg_v2c = self._vnu_forward(
                msg_c2v, posteriors, prev_posteriors, gamma_f
            )
            if self.quantize:
                posteriors = self.quantizer(posteriors)
                msg_v2c = self.quantizer(msg_v2c)

            # Hard decisions
            hard_corrections = (posteriors < 0.0).float()
            outputs.append((posteriors, hard_corrections))

        return outputs

    def _cnu_forward(
        self, syndromes: torch.Tensor, msg_v2c: torch.Tensor, alpha_edge: torch.Tensor
    ) -> torch.Tensor:
        """Fully vectorized CNU with min-1/min-2 across bipartite edges."""
        padded_v2c = F.pad(msg_v2c, (0, 1), value=1e9)
        v2c_grid = padded_v2c[:, self.c_edge_idx]

        signs = torch.sign(v2c_grid)
        signs = torch.where(signs == 0, torch.ones_like(signs), signs)
        signs = torch.where(self.c_mask.unsqueeze(0), signs, torch.ones_like(signs))
        total_sign = torch.prod(signs, dim=2, keepdim=True)
        syn_factor = (1.0 - 2.0 * syndromes.float()).unsqueeze(2)
        total_sign = total_sign * syn_factor
        out_signs = total_sign * signs

        mags = torch.abs(v2c_grid)
        mags = torch.where(self.c_mask.unsqueeze(0), mags, torch.full_like(mags, 1e9))
        min1, idx1 = torch.min(mags, dim=2, keepdim=True)
        masked_mags = mags.clone()
        masked_mags.scatter_(2, idx1, 1e9)
        min2, _ = torch.min(masked_mags, dim=2, keepdim=True)

        max_deg = self.c_edge_idx.shape[1]
        deg_idx = torch.arange(max_deg, device=mags.device).view(1, 1, max_deg)
        out_mags = torch.where(deg_idx == idx1, min2, min1)

        alpha_padded = F.pad(alpha_edge, (0, 1), value=0.0)
        alpha_grid = alpha_padded[self.c_edge_idx].unsqueeze(0)
        out_grid = out_signs * alpha_grid * out_mags

        valid_out = out_grid[:, self.c_mask]
        msg_c2v = valid_out[:, self.inv_perm]
        return msg_c2v

    def _vnu_forward(
        self,
        msg_c2v: torch.Tensor,
        posteriors: torch.Tensor,
        prev_posteriors: torch.Tensor,
        gamma_f: torch.Tensor,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Vectorized VNU with O(1) scatter_add across all bipartite edges."""
        b_size = msg_c2v.shape[0]
        num_faults = self.graph.num_faults

        # Vectorized accumulation across bipartite edges into fault variable nodes
        f_nodes_batch = self.fault_nodes.unsqueeze(0).expand(b_size, -1)
        sum_c2v = torch.zeros(b_size, num_faults, device=msg_c2v.device)
        sum_c2v.scatter_add_(1, f_nodes_batch, msg_c2v)

        g_v = gamma_f.unsqueeze(0)
        new_posteriors = (
            (1.0 - g_v) * self.priors.unsqueeze(0)
            + g_v * prev_posteriors
            + sum_c2v
        )

        # Vectorized extrinsic subtraction along edges
        msg_v2c = new_posteriors[:, self.fault_nodes] - msg_c2v

        return new_posteriors, msg_v2c

    def compute_loss(
        self,
        outputs: List[Tuple[torch.Tensor, torch.Tensor]],
        true_observables: torch.Tensor,
        syndromes: torch.Tensor,
        lambda_syn: float = 0.1,
        loss_type: str = "soft_syndrome",
    ) -> torch.Tensor:
        """Computes multi-iteration supervised loss (syndrome parity, softplus, or BCE)."""
        total_loss = torch.tensor(0.0, device=true_observables.device)
        t_max = len(outputs)

        for t, (posteriors, _) in enumerate(outputs):
            omega_t = (t + 1.0) / t_max

            if loss_type == "softplus_parity":
                # Liu & Poulin style softplus check parity loss
                soft_parity = torch.sigmoid(-posteriors)
                syn_target = syndromes.float()
                loss_step = F.binary_cross_entropy(
                    torch.clamp(soft_parity[:, :syn_target.shape[1]], 1e-6, 1.0 - 1e-6),
                    syn_target,
                )
                total_loss = total_loss + omega_t * loss_step
                continue

            # Default: Soft syndrome parity violation loss
            padded_v2c = F.pad(posteriors[:, self.fault_nodes], (0, 1), value=1e9)
            v2c_grid = padded_v2c[:, self.c_edge_idx]
            tanh_grid = torch.tanh(v2c_grid / 2.0)
            tanh_grid = torch.where(self.c_mask.unsqueeze(0), tanh_grid, torch.ones_like(tanh_grid))
            prod_tanh = torch.prod(tanh_grid, dim=2)
            pi_c = (1.0 - 2.0 * syndromes.float()) * prod_tanh
            loss_syn = 0.5 * (1.0 - pi_c).mean()

            total_loss = total_loss + omega_t * loss_syn

        return total_loss

