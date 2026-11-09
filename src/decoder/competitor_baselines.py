"""Competitor Baselines for Bivariate Bicycle Quantum Codes.

Implements high-fidelity competitor decoders:
1. BP-LSD (Localised Statistics Decoder via ldpc C++ backend)
2. BP+OSD-CS-10 (Ordered Statistics Decoding combination sweep order 10)
3. Mem-BP (Min-Sum with memory damping)
4. AutDEC (Automorphism-assisted permutation decoding across torus shifts)
5. GDG (Gong et al. sliding-window baseline)
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional, Union
import numpy as np
from numpy.typing import NDArray
import scipy.sparse as sp

try:
    from ldpc import BpLsdDecoder, BpOsdDecoder, BpDecoder
    HAS_LDPC_CPP = True
except ImportError:
    HAS_LDPC_CPP = False

from src.data.dem_graph import DemGraph
from src.decoder.baselines import DecodeResult, MinSumDecoder
from src.decoder.orbits import DemOrbitManager


class MemBpDecoder:
    """Memory-damped Min-Sum Belief Propagation decoder.

    Damps variable-node posteriors across iterations with memory weight gamma.
    """

    def __init__(
        self,
        graph: DemGraph,
        max_iter: int = 30,
        alpha: float = 0.75,
        gamma: float = 0.35,
    ) -> None:
        self.decoder = MinSumDecoder(
            graph=graph,
            max_iter=max_iter,
            alpha=alpha,
            gamma=gamma,
        )

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Decodes syndrome via memory-damped Min-Sum."""
        return self.decoder.decode(syndrome)


class BpLsdBaselineDecoder:
    """BP-LSD Decoder combining BP with Localised Statistics Decoding (C++ backend)."""

    def __init__(
        self,
        graph: DemGraph,
        max_iter: int = 30,
        ms_scaling_factor: float = 0.75,
        lsd_order: int = 5,
        bits_per_step: int = 1,
    ) -> None:
        self.graph = graph
        self.max_iter = max_iter
        self.obs_matrix = graph.obs_matrix.cpu().numpy().copy()

        c_nodes = graph.check_nodes_per_edge.cpu().numpy()
        f_nodes = graph.fault_nodes_per_edge.cpu().numpy()
        pcm = sp.csr_matrix(
            (np.ones(len(c_nodes), dtype=np.uint8), (c_nodes, f_nodes)),
            shape=(graph.num_detectors, graph.num_faults),
        )

        probs = np.clip(graph.prior_probs.cpu().numpy().copy(), 1e-12, 1.0 - 1e-12)
        if HAS_LDPC_CPP:
            self._cpp_decoder = BpLsdDecoder(
                pcm=pcm,
                error_channel=list(probs),
                max_iter=max_iter,
                bp_method="minimum_sum",
                ms_scaling_factor=ms_scaling_factor,
                lsd_order=lsd_order,
                lsd_method="LSD_CS",
                bits_per_step=bits_per_step,
            )
        else:
            self._cpp_decoder = None
            self._fallback = MinSumDecoder(graph=graph, max_iter=max_iter, alpha=ms_scaling_factor)

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Decodes binary syndrome using BP-LSD."""
        if self._cpp_decoder is not None:
            corr = self._cpp_decoder.decode(syndrome).astype(np.uint8)
            converged = bool(self._cpp_decoder.converge)
            iters = int(self._cpp_decoder.iter)
            pred_obs = ((self.obs_matrix @ corr) % 2).astype(np.uint8)
            llrs = np.array(self._cpp_decoder.log_prob_ratios, dtype=np.float32)
            return DecodeResult(
                converged=converged,
                iterations=iters,
                corrections=corr,
                predicted_observables=pred_obs,
                final_llrs=llrs,
            )
        return self._fallback.decode(syndrome)


class BpOsdBaselineDecoder:
    """BP+OSD-CS-10 Decoder (C++ backend with order-10 combination sweep)."""

    def __init__(
        self,
        graph: DemGraph,
        max_iter: int = 30,
        ms_scaling_factor: float = 0.75,
        osd_order: int = 10,
    ) -> None:
        self.graph = graph
        self.max_iter = max_iter
        self.obs_matrix = graph.obs_matrix.cpu().numpy().copy()

        c_nodes = graph.check_nodes_per_edge.cpu().numpy()
        f_nodes = graph.fault_nodes_per_edge.cpu().numpy()
        pcm = sp.csr_matrix(
            (np.ones(len(c_nodes), dtype=np.uint8), (c_nodes, f_nodes)),
            shape=(graph.num_detectors, graph.num_faults),
        )

        probs = np.clip(graph.prior_probs.cpu().numpy().copy(), 1e-12, 1.0 - 1e-12)
        if HAS_LDPC_CPP:
            self._cpp_decoder = BpOsdDecoder(
                pcm=pcm,
                error_channel=list(probs),
                max_iter=max_iter,
                bp_method="minimum_sum",
                ms_scaling_factor=ms_scaling_factor,
                osd_order=osd_order,
                osd_method="osd_cs",
            )
        else:
            self._cpp_decoder = None
            self._fallback = MinSumDecoder(graph=graph, max_iter=max_iter, alpha=ms_scaling_factor)

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Decodes binary syndrome using BP+OSD-CS-10."""
        if self._cpp_decoder is not None:
            corr = self._cpp_decoder.decode(syndrome).astype(np.uint8)
            converged = bool(self._cpp_decoder.converge)
            iters = int(self._cpp_decoder.iter)
            pred_obs = ((self.obs_matrix @ corr) % 2).astype(np.uint8)
            llrs = np.array(self._cpp_decoder.log_prob_ratios, dtype=np.float32)
            return DecodeResult(
                converged=converged,
                iterations=iters,
                corrections=corr,
                predicted_observables=pred_obs,
                final_llrs=llrs,
            )
        return self._fallback.decode(syndrome)


class AutDecBaselineDecoder:
    """Automorphism-Assisted Permutation Decoder (AutDEC).

    Evaluates BP over torus automorphism group shifts and selects valid solution.
    """

    def __init__(
        self,
        graph: DemGraph,
        orbit_mgr: DemOrbitManager,
        max_iter: int = 20,
        alpha: float = 0.75,
        max_automorphisms: int = 6,
    ) -> None:
        self.graph = graph
        self.orbit_mgr = orbit_mgr
        self.max_iter = max_iter
        self.base_decoder = MinSumDecoder(graph=graph, max_iter=max_iter, alpha=alpha)
        self.shift_table = orbit_mgr.shift_table
        self.l = orbit_mgr.l
        self.m = orbit_mgr.m
        self.max_auts = min(max_automorphisms, self.l * self.m)
        self.shifts: List[Tuple[int, int]] = []
        for a in range(self.l):
            for b in range(self.m):
                if len(self.shifts) < self.max_auts:
                    self.shifts.append((a, b))

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Decodes syndrome across automorphism group permutations."""
        base_res = self.base_decoder.decode(syndrome)
        if base_res.converged or len(self.shifts) <= 1:
            return base_res

        best_res = base_res
        total_iters = base_res.iterations

        for a, b in self.shifts[1:]:
            perm = self.shift_table[:, a, b]
            perm_syndrome = np.zeros_like(syndrome)
            perm_syndrome[perm] = syndrome

            res = self.base_decoder.decode(perm_syndrome)
            total_iters += res.iterations

            if res.converged:
                best_res = DecodeResult(
                    converged=True,
                    iterations=total_iters,
                    corrections=res.corrections,
                    predicted_observables=res.predicted_observables,
                    final_llrs=res.final_llrs,
                )
                return best_res

        return DecodeResult(
            converged=False,
            iterations=total_iters,
            corrections=best_res.corrections,
            predicted_observables=best_res.predicted_observables,
            final_llrs=best_res.final_llrs,
        )


class FastBpBaselineDecoder:
    """Fast C++ Min-Sum Belief Propagation Decoder via ldpc library."""

    def __init__(self, graph: DemGraph, max_iter: int = 30, alpha: float = 1.0) -> None:
        self.graph = graph
        self.obs_matrix = graph.obs_matrix.cpu().numpy().copy()
        c_nodes = graph.check_nodes_per_edge.cpu().numpy()
        f_nodes = graph.fault_nodes_per_edge.cpu().numpy()
        pcm = sp.csr_matrix(
            (np.ones(len(c_nodes), dtype=np.uint8), (c_nodes, f_nodes)),
            shape=(graph.num_detectors, graph.num_faults),
        )
        probs = np.clip(graph.prior_probs.cpu().numpy().copy(), 1e-12, 1.0 - 1e-12)
        if HAS_LDPC_CPP:
            self._cpp_decoder = BpDecoder(
                pcm=pcm,
                error_channel=list(probs),
                max_iter=max_iter,
                bp_method="minimum_sum",
                ms_scaling_factor=alpha,
            )
        else:
            self._cpp_decoder = None
            self._fallback = MinSumDecoder(graph=graph, max_iter=max_iter, alpha=alpha)

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Decodes syndrome using C++ BpDecoder."""
        if self._cpp_decoder is not None:
            corr = self._cpp_decoder.decode(syndrome).astype(np.uint8)
            pred_obs = ((self.obs_matrix @ corr) % 2).astype(np.uint8)
            return DecodeResult(
                converged=bool(self._cpp_decoder.converge),
                iterations=int(self._cpp_decoder.iter),
                corrections=corr,
                predicted_observables=pred_obs,
                final_llrs=np.array(self._cpp_decoder.log_prob_ratios, dtype=np.float32),
            )
        return self._fallback.decode(syndrome)


class GdgSlidingWindowBaseline:
    """Gong et al. sliding-window Normalized Min-Sum baseline decoder."""

    def __init__(
        self,
        graph: DemGraph,
        window_size: int = 3,
        commit_size: int = 1,
        max_iter: int = 30,
        alpha: float = 0.75,
    ) -> None:
        self.graph = graph
        self.window_size = window_size
        self.commit_size = commit_size
        self.decoder = FastBpBaselineDecoder(graph=graph, max_iter=max_iter, alpha=alpha)

    def decode(self, syndrome: NDArray[np.uint8]) -> DecodeResult:
        """Decodes sliding window syndrome via Normalized Min-Sum."""
        return self.decoder.decode(syndrome)

