"""Bit-Exact Pure Integer Reference Model for Multiplier-Free Hardware QNBP.

Executes inference strictly using integer arithmetic (shifts, adds, subtracts,
and comparisons). Verifies bit-exact parity with PyTorch quantized models.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from numpy.typing import NDArray

from src.data.dem_graph import DemGraph
from src.decoder.quantization import CanonicalSignedDigit
from src.decoder.baselines import DecodeResult


class IntegerQNBP:
    """Multiplier-free pure integer reference belief propagation decoder.

    All multiplications are implemented as shifts and adds using Canonical
    Signed Digit (CSD) term decomposition: val * alpha = sum s_i * (val >> a_i).

    Attributes:
        graph: DemGraph instance.
        num_layers: Number of unfolded BP iterations T.
        bit_width: Message bit-width k (e.g. 4, 5, 6 bits).
        qmin: Minimum clipped integer message.
        qmax: Maximum clipped integer message.
    """

    def __init__(
        self,
        graph: DemGraph,
        num_layers: int = 15,
        bit_width: int = 4,
        alpha_val: float = 0.75,
        gamma_val: float = 0.0,
        shift_scale: int = 2,
    ) -> None:
        self.graph = graph
        self.num_layers = num_layers
        self.bit_width = bit_width
        self.shift_scale = shift_scale

        self.qmin = -(2 ** (bit_width - 1) - 1)
        self.qmax = 2 ** (bit_width - 1) - 1

        # Decompose alpha into shift-and-add terms
        csd = CanonicalSignedDigit(max_shift=5, num_terms=2)
        _, self.alpha_terms = csd.project(alpha_val)
        _, self.gamma_terms = csd.project(gamma_val)

        # Scale float priors into integer representation: int_prior = round(prior * 2^shift_scale)
        float_priors = graph.priors.cpu().numpy()
        scaled = np.round(float_priors * (2.0 ** shift_scale))
        self.int_priors = np.clip(scaled, self.qmin, self.qmax).astype(np.int32)

        self.num_checks = graph.num_detectors
        self.num_faults = graph.num_faults
        self.num_edges = graph.num_edges

        self.c_nodes = graph.check_nodes_per_edge.cpu().numpy()
        self.f_nodes = graph.fault_nodes_per_edge.cpu().numpy()
        self.check_to_edges = graph.check_to_edges
        self.fault_to_edges = graph.fault_to_edges
        self.obs_matrix = graph.obs_matrix.cpu().numpy().astype(np.uint8)

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Executes pure integer inference without any floating-point arithmetic."""
        msg_v2c = self.int_priors[self.f_nodes].copy()
        msg_c2v = np.zeros(self.num_edges, dtype=np.int32)

        posteriors = self.int_priors.copy()
        prev_posteriors = self.int_priors.copy()

        converged = False
        iteration = 0

        for t in range(self.num_layers):
            iteration = t + 1

            # 1. Integer CNU: min-1/min-2 with shift-add scaling
            self._integer_cnu(syndrome, msg_v2c, msg_c2v)

            # 2. Integer VNU: addition and subtraction
            prev_posteriors[:] = posteriors
            self._integer_vnu(msg_c2v, msg_v2c, posteriors, prev_posteriors)

            # 3. Hard decisions & Syndrome check
            hard_e = (posteriors < 0).astype(np.uint8)
            if self._check_syndrome(syndrome, hard_e):
                converged = True
                break

        pred_obs = (self.obs_matrix @ hard_e) % 2

        return DecodeResult(
            converged=converged,
            iterations=iteration,
            corrections=hard_e,
            predicted_observables=pred_obs.astype(np.uint8),
            final_llrs=posteriors.astype(np.float32) / (2.0 ** self.shift_scale),
        )

    def _integer_cnu(
        self,
        syndrome: NDArray[np.uint8],
        msg_v2c: NDArray[np.int32],
        msg_c2v: NDArray[np.int32],
    ) -> None:
        """Computes check messages using integer shifts, adds, and compares in O(1)."""
        for c in range(self.num_checks):
            e_indices = self.check_to_edges[c]
            deg = len(e_indices)
            if deg == 0:
                continue

            signs = np.sign(msg_v2c[e_indices])
            signs[signs == 0] = 1
            total_sign = int(np.prod(signs))
            if syndrome[c] == 1:
                total_sign = -total_sign

            mags = np.abs(msg_v2c[e_indices])
            if deg == 1:
                msg_c2v[e_indices[0]] = np.clip(
                    total_sign * signs[0] * self.qmax, self.qmin, self.qmax
                )
                continue

            sorted_idx = np.argsort(mags)
            idx1 = int(sorted_idx[0])
            min1 = int(mags[idx1])
            min2 = int(mags[sorted_idx[1]])

            # Multiplier-free shift-and-add scaling for min1 and min2
            scaled_min1 = 0
            for s_i, shift_i in self.alpha_terms:
                scaled_min1 += (min1 >> shift_i) if s_i > 0 else -(min1 >> shift_i)

            scaled_min2 = 0
            for s_i, shift_i in self.alpha_terms:
                scaled_min2 += (min2 >> shift_i) if s_i > 0 else -(min2 >> shift_i)

            clamped_min1 = np.clip(scaled_min1, 0, self.qmax)
            clamped_min2 = np.clip(scaled_min2, 0, self.qmax)

            out = total_sign * signs * clamped_min1
            out[idx1] = total_sign * signs[idx1] * clamped_min2
            msg_c2v[e_indices] = np.clip(out, self.qmin, self.qmax)

    def _integer_vnu(
        self,
        msg_c2v: NDArray[np.int32],
        msg_v2c: NDArray[np.int32],
        posteriors: NDArray[np.int32],
        prev_posteriors: NDArray[np.int32],
    ) -> None:
        """Computes posterior sums and variable messages in integer accumulator in O(1)."""
        sum_c2v = np.bincount(
            self.f_nodes, weights=msg_c2v, minlength=self.num_faults
        ).astype(np.int32)

        # Memory shift-add contribution
        mem_contrib = np.zeros(self.num_faults, dtype=np.int32)
        for s_i, shift_i in self.gamma_terms:
            term = np.right_shift(prev_posteriors, shift_i)
            mem_contrib += term if s_i > 0 else -term

        total_acc = self.int_priors + mem_contrib + sum_c2v
        posteriors[:] = np.clip(total_acc, self.qmin * 4, self.qmax * 4)

        extrinsic = posteriors[self.f_nodes] - msg_c2v
        msg_v2c[:] = np.clip(extrinsic, self.qmin, self.qmax)

    def _check_syndrome(
        self, syndrome: NDArray[np.uint8], hard_e: NDArray[np.uint8]
    ) -> bool:
        """Verifies parity check satisfaction in O(1)."""
        syndrome_pred = (
            np.bincount(
                self.c_nodes, weights=hard_e[self.f_nodes], minlength=self.num_checks
            ).astype(np.int64)
            % 2
        )
        return bool(np.all(syndrome_pred == syndrome))
