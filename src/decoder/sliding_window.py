"""Sliding-Window Decoding Manager, Confidence Margin Gates, and Queue Model.

Implements window slicing (width W, stride F), fast-path confidence gates
(G1, G2, G3), and trace-driven queue stability simulation for BB codes.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from numpy.typing import NDArray

from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph
from src.decoder.baselines import DecodeResult, MinSumDecoder


class ConfidenceGate:
    """Evaluates on-chip fast-path confidence margin gating rules.

    Rules:
        G1: Syndrome is matched by hard decisions.
        G2: G1 and min |Lambda_v| among flipped faults (e_v = 1) >= tau.
        G3: G1 and for all observables k, min |Lambda_v| among flipped faults
            touching observable k >= tau.
    """

    @staticmethod
    def evaluate(
        gate_type: str,
        result: DecodeResult,
        obs_matrix: NDArray[np.float32],
        tau: float = 2.0,
    ) -> bool:
        """Evaluates whether a decoded window is accepted on the fast path.

        Args:
            gate_type: One of 'G1', 'G2', 'G3', or 'control_all'.
            result: DecodeResult from belief propagation.
            obs_matrix: Observable incidence matrix of shape (num_obs, num_faults).
            tau: Minimum LLR confidence margin threshold.

        Returns:
            True if window passes confidence gate, False if rejected to fallback.
        """
        if not result.converged:
            return False

        if gate_type == "G1":
            return True

        flipped_indices = np.where(result.corrections == 1)[0]
        if len(flipped_indices) == 0:
            # No faults predicted -> trivial pass if syndrome is all-zero
            return True

        flipped_llrs = np.abs(result.final_llrs[flipped_indices])

        if gate_type == "G2":
            min_flipped_llr = float(np.min(flipped_llrs))
            return min_flipped_llr >= tau

        if gate_type == "G3":
            # For every observable touched by committed faults, check min LLR
            num_obs = obs_matrix.shape[0]
            for k in range(num_obs):
                obs_faults = np.where(obs_matrix[k] == 1.0)[0]
                common = np.intersect1d(flipped_indices, obs_faults)
                if len(common) > 0:
                    min_k_llr = float(np.min(np.abs(result.final_llrs[common])))
                    if min_k_llr < tau:
                        return False
            return True

        if gate_type == "control_all":
            # Minimum over ALL faults (overly conservative control)
            return float(np.min(np.abs(result.final_llrs))) >= tau

        raise ValueError(f"Unknown gate type: {gate_type}")


class SlidingWindowManager:
    """Manages 3D sliding-window decoding across temporal syndrome extractions.

    Attributes:
        code: BivariateBicycleCode instance.
        window_width: Window width W in syndrome rounds (e.g. 3, 5, 6).
        commit_stride: Commit stride F in syndrome rounds (e.g. 1, 2).
    """

    def __init__(
        self,
        code: BivariateBicycleCode,
        window_width: int = 3,
        commit_stride: int = 1,
    ) -> None:
        self.code = code
        self.window_width = window_width
        self.commit_stride = commit_stride

    def get_window_schedule(self, total_rounds: int) -> List[Tuple[int, int, int]]:
        """Computes list of (window_start, window_end, commit_end) rounds.

        Args:
            total_rounds: Total syndrome extraction rounds R.

        Returns:
            List of tuples (start_round, end_round, commit_end_round).
        """
        windows = []
        cur_start = 0
        while cur_start + self.window_width <= total_rounds:
            end_round = cur_start + self.window_width - 1
            commit_end = cur_start + self.commit_stride - 1
            windows.append((cur_start, end_round, commit_end))
            cur_start += self.commit_stride
        return windows


class TraceDrivenQueueSimulator:
    """Simulates real-time sequential decoding backlog and buffer stability.

    Models sequential chain:
        E[S] = p_fast * S_fast + (1 - p_fast) * (S_attempt + E[S_slow]) < F * T_cycle
    """

    def __init__(
        self,
        t_cycle_ns: float = 1000.0,
        commit_stride: int = 1,
        ns_per_iteration_fast: float = 24.0,
        ns_per_iteration_slow: float = 200.0,
    ) -> None:
        self.arrival_period_ns = commit_stride * t_cycle_ns
        self.ns_per_iter_fast = ns_per_iteration_fast
        self.ns_per_iter_slow = ns_per_iteration_slow

    def simulate(
        self,
        fast_iter_trace: Optional[List[int]] = None,
        is_accepted_trace: Optional[List[bool]] = None,
        slow_iter_trace: Optional[List[int]] = None,
        buffer_capacity: int = 10,
        **kwargs: Any,
    ) -> Dict[str, float]:
        """Simulates backlog queue over a trace of decoded windows.

        Returns:
            Dictionary with mean service time, utilization, overflow rate, and backlog stats.
        """
        fast_trace = fast_iter_trace if fast_iter_trace is not None else kwargs.get("fast_iters", [])
        acc_trace = is_accepted_trace if is_accepted_trace is not None else kwargs.get("is_accepted", [])
        slow_trace = slow_iter_trace if slow_iter_trace is not None else kwargs.get("slow_iters", [])

        n_windows = len(acc_trace)
        service_times = np.zeros(n_windows, dtype=np.float64)

        for i in range(n_windows):
            if acc_trace[i]:
                service_times[i] = fast_trace[i] * self.ns_per_iter_fast
            else:
                # Paid fast attempt + slow fallback execution
                s_attempt = fast_trace[i] * self.ns_per_iter_fast
                s_slow = slow_trace[i] * self.ns_per_iter_slow
                service_times[i] = s_attempt + s_slow

        mean_service_time = float(np.mean(service_times)) if n_windows > 0 else 0.0
        utilization = mean_service_time / self.arrival_period_ns

        # Simulate sequential queue buffer backlog
        overflow_events = 0
        max_backlog = 0
        backlog_list: List[int] = []
        current_time = 0.0

        for i in range(n_windows):
            arrival_time = i * self.arrival_period_ns
            start_time = max(current_time, arrival_time)
            finish_time = start_time + service_times[i]
            current_time = finish_time

            # Number of queued windows waiting at arrival
            queue_depth = max(0, int((start_time - arrival_time) / self.arrival_period_ns))
            backlog_list.append(queue_depth)
            max_backlog = max(max_backlog, queue_depth)
            if queue_depth >= buffer_capacity:
                overflow_events += 1

        overflow_rate = overflow_events / max(1, n_windows)
        p_fast = float(np.mean(acc_trace)) if n_windows > 0 else 0.0
        avg_backlog = float(np.mean(backlog_list)) if backlog_list else 0.0

        return {
            "p_fast": p_fast,
            "mean_service_ns": mean_service_time,
            "utilization": utilization,
            "is_stable": float(utilization < 1.0),
            "max_backlog": float(max_backlog),
            "avg_backlog": avg_backlog,
            "overflow_rate": overflow_rate,
            "overflow_fraction": overflow_rate,
        }

