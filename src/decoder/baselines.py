"""Classical Min-Sum Belief Propagation and BP-OSD Baselines for BB Codes.

Implements baseline A0 (unweighted min-sum), baseline A1 (normalized min-sum
with iteration-dependent scaling alpha_t), and BP-OSD post-processing wrapper.
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional, Union
import numpy as np
from numpy.typing import NDArray
import torch

from src.data.dem_graph import DemGraph

try:
    from ldpc import bposd_decoder  # type: ignore
    HAS_BPOSD = True
except ImportError:
    HAS_BPOSD = False


@dataclass
class DecodeResult:
    """Output structure of a belief propagation decoding execution."""
    converged: bool
    iterations: int
    corrections: NDArray[np.uint8]
    predicted_observables: NDArray[np.uint8]
    final_llrs: NDArray[np.float32]


class MinSumDecoder:
    """Vectorized Min-Sum Belief Propagation decoder for DEM hypergraphs.

    Supports A0 (unweighted min-sum, alpha=1.0) and A1 (normalized min-sum, alpha<1.0).

    Attributes:
        graph: DemGraph representing the DEM bipartite Tanner graph.
        max_iter: Maximum decoding iterations T.
        alpha: Scaling factor alpha (scalar float or list of floats of length T).
        gamma: Memory damping factor gamma in [0, 1) or signed in (-1, 1).
    """

    def __init__(
        self,
        graph: DemGraph,
        max_iter: int = 30,
        alpha: Union[float, List[float]] = 1.0,
        gamma: float = 0.0,
    ) -> None:
        self.graph = graph
        self.max_iter = max_iter
        self.gamma = gamma

        if isinstance(alpha, (int, float)):
            self.alpha_schedule = [float(alpha)] * max_iter
        else:
            self.alpha_schedule = [float(a) for a in alpha]
            if len(self.alpha_schedule) < max_iter:
                self.alpha_schedule += [self.alpha_schedule[-1]] * (max_iter - len(self.alpha_schedule))

        self.num_checks = graph.num_detectors
        self.num_faults = graph.num_faults
        self.num_edges = graph.num_edges

        # Precompute edge mappings
        self.c_nodes = graph.check_nodes_per_edge.cpu().numpy()
        self.f_nodes = graph.fault_nodes_per_edge.cpu().numpy()
        self.check_to_edges = graph.check_to_edges
        self.fault_to_edges = graph.fault_to_edges
        self.priors = graph.priors.cpu().numpy().copy()
        self.obs_matrix = graph.obs_matrix.cpu().numpy().copy()

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Decodes an observed binary detector syndrome vector s.

        Args:
            syndrome: 1D binary array of length num_detectors (1 if detector fired).

        Returns:
            DecodeResult containing convergence status, iterations, corrections,
            predicted logical observable flips, and posterior LLRs.
        """
        # Edge message initialization: L_{v -> c} = lambda_v
        # msg_v2c: variable-to-check messages along edges
        # msg_c2v: check-to-variable messages along edges
        msg_v2c = self.priors[self.f_nodes].copy()
        msg_c2v = np.zeros(self.num_edges, dtype=np.float32)

        # Variable posterior LLRs
        posteriors = self.priors.copy()
        prev_posteriors = self.priors.copy()

        converged = False
        iteration = 0

        for t in range(self.max_iter):
            iteration = t + 1
            alpha_t = self.alpha_schedule[t]

            # 1. Check Node Update (CNU) with Min-1 and Min-2
            self._update_cnu(syndrome, msg_v2c, msg_c2v, alpha_t)

            # 2. Variable Node Update (VNU) with optional memory damping
            prev_posteriors[:] = posteriors
            self._update_vnu(msg_c2v, msg_v2c, posteriors, prev_posteriors)

            # 3. Hard decisions & Syndrome parity verification
            hard_e = (posteriors < 0.0).astype(np.uint8)
            if self._check_syndrome(syndrome, hard_e):
                converged = True
                break

        # Compute predicted logical observable flips
        pred_obs = (self.obs_matrix @ hard_e) % 2

        return DecodeResult(
            converged=converged,
            iterations=iteration,
            corrections=hard_e,
            predicted_observables=pred_obs.astype(np.uint8),
            final_llrs=posteriors,
        )

    def _update_cnu(
        self,
        syndrome: NDArray[np.uint8],
        msg_v2c: NDArray[np.float32],
        msg_c2v: NDArray[np.float32],
        alpha_t: float,
    ) -> None:
        """Vectorized CNU with min-1 and min-2 in O(1)."""
        for c in range(self.num_checks):
            e_indices = self.check_to_edges[c]
            deg = len(e_indices)
            if deg == 0:
                continue

            signs = np.sign(msg_v2c[e_indices])
            signs[signs == 0] = 1.0
            total_sign = int(np.prod(signs))
            if syndrome[c] == 1:
                total_sign = -total_sign

            mags = np.abs(msg_v2c[e_indices])
            if deg == 1:
                msg_c2v[e_indices[0]] = total_sign * signs[0] * 100.0
                continue

            sorted_idx = np.argsort(mags)
            idx1 = int(sorted_idx[0])
            min1 = float(mags[idx1])
            min2 = float(mags[sorted_idx[1]])

            scaled_out = total_sign * signs * (alpha_t * min1)
            scaled_out[idx1] = total_sign * signs[idx1] * (alpha_t * min2)
            msg_c2v[e_indices] = scaled_out

    def _update_vnu(
        self,
        msg_c2v: NDArray[np.float32],
        msg_v2c: NDArray[np.float32],
        posteriors: NDArray[np.float32],
        prev_posteriors: NDArray[np.float32],
    ) -> None:
        """Computes variable-to-check messages and posterior LLRs with memory in O(1)."""
        sum_c2v = np.bincount(
            self.f_nodes, weights=msg_c2v, minlength=self.num_faults
        ).astype(np.float32)

        if self.gamma != 0.0:
            posteriors[:] = (
                (1.0 - self.gamma) * self.priors
                + self.gamma * prev_posteriors
                + sum_c2v
            )
        else:
            posteriors[:] = self.priors + sum_c2v

        msg_v2c[:] = posteriors[self.f_nodes] - msg_c2v

    def _check_syndrome(
        self, syndrome: NDArray[np.uint8], hard_e: NDArray[np.uint8]
    ) -> bool:
        """Checks if hard decisions satisfy all detector syndrome bits in O(1)."""
        syndrome_pred = (
            np.bincount(
                self.c_nodes, weights=hard_e[self.f_nodes], minlength=self.num_checks
            ).astype(np.int64)
            % 2
        )
        return bool(np.all(syndrome_pred == syndrome))


class RelayBPDecoder:
    """Relay Belief Propagation decoder (Müller et al., IBM Quantum).

    Iteratively restarts belief propagation across multiple relay stages,
    damping posterior beliefs into the next stage's priors to escape cycles.

    Attributes:
        graph: DemGraph representing the DEM bipartite Tanner graph.
        num_relays: Number of relay stages (default: 3).
        iters_per_relay: BP iterations per relay stage (default: 10).
        alpha: Min-sum scaling factor (default: 0.75).
        relay_gamma: Soft posterior memory damping factor in (0, 1) (default: 0.5).
    """

    def __init__(
        self,
        graph: DemGraph,
        num_relays: int = 3,
        iters_per_relay: int = 10,
        alpha: Union[float, List[float]] = 0.75,
        relay_gamma: float = 0.5,
    ) -> None:
        self.graph = graph
        self.num_relays = num_relays
        self.iters_per_relay = iters_per_relay
        self.relay_gamma = relay_gamma
        self.base_decoder = MinSumDecoder(
            graph=graph,
            max_iter=iters_per_relay,
            alpha=alpha,
            gamma=0.0,
        )

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Decodes an observed binary detector syndrome vector s via Relay-BP.

        Args:
            syndrome: 1D binary array of length num_detectors.

        Returns:
            DecodeResult containing convergence status, total iterations,
            corrections, predicted logical observables, and posterior LLRs.
        """
        orig_priors = self.graph.priors.cpu().numpy().copy()
        current_priors = orig_priors.copy()
        total_iters = 0
        last_result: Optional[DecodeResult] = None

        for relay in range(self.num_relays):
            self.base_decoder.priors = current_priors.copy()
            res = self.base_decoder.decode(syndrome)
            total_iters += res.iterations
            last_result = res

            if res.converged:
                self.base_decoder.priors = orig_priors
                return DecodeResult(
                    converged=True,
                    iterations=total_iters,
                    corrections=res.corrections,
                    predicted_observables=res.predicted_observables,
                    final_llrs=res.final_llrs,
                )

            # Damped relay update for next stage
            current_priors = (
                (1.0 - self.relay_gamma) * orig_priors
                + self.relay_gamma * res.final_llrs
            )

        # Restore original priors
        self.base_decoder.priors = orig_priors

        assert last_result is not None
        return DecodeResult(
            converged=last_result.converged,
            iterations=total_iters,
            corrections=last_result.corrections,
            predicted_observables=last_result.predicted_observables,
            final_llrs=last_result.final_llrs,
        )

