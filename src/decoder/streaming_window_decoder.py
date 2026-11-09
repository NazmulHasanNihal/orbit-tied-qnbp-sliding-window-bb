"""Streaming Sliding-Window Decoder with Residual Syndrome Propagation.

Implements sliding-window commit accounting:
1. Evaluates local belief propagation over window of width W rounds.
2. Commits hard decisions strictly on faults in the first F rounds.
3. Propagates syndrome residuals along temporal boundaries to window k+1.
4. Accumulates logical observable flips strictly from committed faults.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from numpy.typing import NDArray

from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph
from src.decoder.baselines import DecodeResult, MinSumDecoder
from src.decoder.integer_reference import IntegerQNBP


class StreamingSlidingWindowDecoder:
    """Decodes continuous syndrome streams using sliding-window commit accounting.

    Attributes:
        code: BivariateBicycleCode instance.
        num_rounds: Total syndrome extraction rounds R.
        window_width: Window width W in syndrome rounds.
        commit_stride: Commit stride F in syndrome rounds.
        graph: Full DemGraph for the complete R-round circuit.
    """

    def __init__(
        self,
        code: BivariateBicycleCode,
        num_rounds: int,
        dem_graph: DemGraph,
        window_width: int = 3,
        commit_stride: int = 1,
        max_bp_iter: int = 15,
        alpha: float = 0.75,
    ) -> None:
        self.code = code
        self.num_rounds = num_rounds
        self.graph = dem_graph
        self.window_width = window_width
        self.commit_stride = commit_stride
        self.max_bp_iter = max_bp_iter
        self.alpha = alpha

        # Build round-to-detector and round-to-fault mapping
        self._build_temporal_partition()

    def _build_temporal_partition(self) -> None:
        """Partitions checks and faults by syndrome extraction round."""
        g = self.code.group_order
        num_dets = self.graph.num_detectors
        self.det_rounds = np.zeros(num_dets, dtype=np.int32)

        # In depth-7 circuit: each round has 2*g detectors (X and Z ancillas)
        # Terminal detectors are in the final round
        for d in range(num_dets):
            if d < (self.num_rounds - 1) * 2 * g + g:
                r = d // (2 * g)
                self.det_rounds[d] = r
            else:
                self.det_rounds[d] = self.num_rounds - 1

        # Check-to-fault incidence
        self.c_nodes = self.graph.check_nodes_per_edge.cpu().numpy()
        self.f_nodes = self.graph.fault_nodes_per_edge.cpu().numpy()
        self.obs_matrix = self.graph.obs_matrix.cpu().numpy()

        # Map each fault to its earliest and latest detector rounds
        self.fault_commit_round = np.zeros(self.graph.num_faults, dtype=np.int32)
        for f in range(self.graph.num_faults):
            e_list = self.graph.fault_to_edges[f]
            if e_list:
                rounds = [self.det_rounds[self.c_nodes[e]] for e in e_list]
                self.fault_commit_round[f] = min(rounds)
            else:
                self.fault_commit_round[f] = 0

    def decode_stream(
        self,
        syndrome: NDArray[np.uint8],
        use_integer_model: bool = True,
    ) -> Tuple[bool, NDArray[np.uint8], int]:
        """Decodes a multi-round syndrome stream with residual propagation.

        Args:
            syndrome: 1D binary syndrome array of length num_detectors.
            use_integer_model: If True, uses 6-bit integer CSD reference model.

        Returns:
            Tuple of (converged, predicted_observables, total_iterations).
        """
        num_dets = self.graph.num_detectors
        num_faults = self.graph.num_faults
        residual_syndrome = syndrome.copy().astype(np.uint8)

        total_committed_faults = np.zeros(num_faults, dtype=np.uint8)
        accumulated_obs = np.zeros(self.graph.num_observables, dtype=np.uint8)
        total_iterations = 0
        all_converged = True

        cur_start = 0
        while cur_start < self.num_rounds:
            cur_end = min(cur_start + self.window_width - 1, self.num_rounds - 1)
            is_final = (cur_end == self.num_rounds - 1)
            commit_end = cur_end if is_final else (cur_start + self.commit_stride - 1)

            # Check nodes active in this window
            win_checks = np.where(
                (self.det_rounds >= cur_start) & (self.det_rounds <= cur_end)
            )[0]
            if len(win_checks) == 0:
                cur_start += self.commit_stride
                continue

            # Run local decoder on full graph with residual syndrome
            if use_integer_model:
                dec = IntegerQNBP(
                    graph=self.graph,
                    num_layers=self.max_bp_iter,
                    bit_width=6,
                    alpha_val=self.alpha,
                )
                res = dec.decode(residual_syndrome)
            else:
                dec_ms = MinSumDecoder(
                    graph=self.graph,
                    max_iter=self.max_bp_iter,
                    alpha=self.alpha,
                )
                res = dec_ms.decode(residual_syndrome)

            total_iterations += res.iterations
            if not res.converged:
                all_converged = False

            # Strictly commit faults belonging to [cur_start, commit_end]
            commit_mask = (
                (self.fault_commit_round >= cur_start)
                & (self.fault_commit_round <= commit_end)
            )
            committed_faults = np.where(commit_mask & (res.corrections == 1))[0]

            if len(committed_faults) > 0:
                total_committed_faults[committed_faults] ^= 1

                # Update syndrome residual for all checks touched by committed faults
                for f in committed_faults:
                    for e in self.graph.fault_to_edges[f]:
                        c = self.c_nodes[e]
                        residual_syndrome[c] ^= 1

                # Accumulate committed observable flips
                delta_obs = (self.obs_matrix[:, committed_faults].sum(axis=1) % 2).astype(np.uint8)
                accumulated_obs = (accumulated_obs + delta_obs) % 2

            if is_final:
                break
            cur_start += self.commit_stride

        return all_converged, accumulated_obs, total_iterations

