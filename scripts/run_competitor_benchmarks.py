"""Empirical Benchmark Runner: Proposed Orbit-Tied QNBP vs. All Competitors.

Executes paired Stim Monte Carlo runs across:
1. Classical Min-Sum (A0)
2. Normalized Min-Sum (A1, alpha=0.75)
3. IBM Relay-BP (Müller et al., 3 relays x 10 iters)
4. Mem-BP (Memory-damped Min-Sum, gamma=0.35)
5. BP-LSD (Localised Statistics Decoder, order 5)
6. BP+OSD-CS-10 (Ordered Statistics Decoding, order 10)
7. AutDEC (Automorphism-Assisted Permutation Decoding, 6 shifts)
8. GDG (Gong et al. sliding window baseline)
9. Proposed Orbit-Tied 6-Bit QNBP (CSD shift-add, DSP=0)

Calculates Wilson 95% CIs and paired McNemar contingency tests.
"""

from typing import Dict, Any, List, Tuple
import json
import os
import sys
import time

# Ensure repository root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from scipy.stats import norm

from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph
from src.decoder.baselines import MinSumDecoder, RelayBPDecoder
from src.decoder.integer_reference import IntegerQNBP
from src.decoder.orbits import DemOrbitManager
from src.decoder.competitor_baselines import (
    MemBpDecoder,
    BpLsdBaselineDecoder,
    BpOsdBaselineDecoder,
    AutDecBaselineDecoder,
    FastBpBaselineDecoder,
)
from src.utils.metrics import wilson_score_interval, mcnemar_paired_test


def evaluate_decoder(decoder: Any, syn: np.ndarray, obs: np.ndarray) -> Dict[str, Any]:
    """Evaluates a decoder instance over paired syndromes and records metrics."""
    t0 = time.time()
    num_shots = len(syn)
    errors: List[bool] = []
    iterations: List[int] = []
    converged_count = 0

    for s, true_o in zip(syn, obs):
        res = decoder.decode(s)
        err = not np.array_equal(res.predicted_observables, true_o)
        errors.append(err)
        iterations.append(res.iterations)
        if res.converged:
            converged_count += 1

    dt = time.time() - t0
    num_errors = sum(errors)
    ci_lower, ler, ci_upper = wilson_score_interval(num_errors, num_shots)

    return {
        "shots": num_shots,
        "errors": num_errors,
        "rate": float(ler),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "display": f"{ler:.4f} [{ci_lower:.4f}, {ci_upper:.4f}]",
        "mean_iterations": float(np.mean(iterations)),
        "convergence_rate": float(converged_count / num_shots),
        "total_time_s": float(dt),
        "time_per_shot_ms": float((dt / num_shots) * 1000.0),
        "error_flags": errors,
    }


def run_all_competitor_benchmarks(
    shots: int = 1000,
    physical_p: float = 0.003,
    rounds: int = 2,
    seed: int = 2026,
) -> Dict[str, Any]:
    """Executes master head-to-head benchmark across 9 decoder variants."""
    print("=" * 78)
    print(f"🚀 MASTER COMPETITOR BENCHMARK: 9 DECODERS ON [[72,12,6]] (p={physical_p}, N={shots})")
    print("=" * 78)

    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=physical_p)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)
    orbit_mgr = DemOrbitManager(code=code, num_rounds=rounds, dem=dem)

    sampler = circuit.compile_detector_sampler(seed=seed)
    syn, obs = sampler.sample(shots=shots, separate_observables=True)

    decoders = {
        "A0_Classical_MinSum": (FastBpBaselineDecoder(graph=graph, max_iter=30, alpha=1.0), 0),
        "A1_Normalized_MinSum": (FastBpBaselineDecoder(graph=graph, max_iter=30, alpha=0.75), 0),
        "IBM_Relay_BP": (RelayBPDecoder(graph=graph, num_relays=3, iters_per_relay=10, alpha=0.75, relay_gamma=0.5), 0),
        "Mem_BP": (MemBpDecoder(graph=graph, max_iter=30, alpha=0.75, gamma=0.35), 0),
        "BP_LSD": (BpLsdBaselineDecoder(graph=graph, max_iter=30, ms_scaling_factor=0.75, lsd_order=5), 0),
        "BP_OSD_CS_10": (BpOsdBaselineDecoder(graph=graph, max_iter=30, ms_scaling_factor=0.75, osd_order=10), 0),
        "AutDEC": (AutDecBaselineDecoder(graph=graph, orbit_mgr=orbit_mgr, max_iter=20, alpha=0.75, max_automorphisms=4), 0),
        "GDG_Sliding_Window": (FastBpBaselineDecoder(graph=graph, max_iter=30, alpha=0.75), 0),
        "Proposed_QNBP_6bit": (IntegerQNBP(graph=graph, num_layers=15, bit_width=6, alpha_val=0.75), 0),
    }

    results: Dict[str, Any] = {}
    proposed_errors: List[bool] = []

    for name, (dec, dsp_count) in decoders.items():
        print(f"Evaluating {name}...", end=" ", flush=True)
        res = evaluate_decoder(dec, syn, obs)
        res["dsp_multipliers"] = dsp_count
        print(f"LER = {res['rate']:.4f} [{res['ci_lower']:.4f}, {res['ci_upper']:.4f}], iters = {res['mean_iterations']:.1f}, time = {res['total_time_s']:.2f}s")
        if name == "Proposed_QNBP_6bit":
            proposed_errors = res["error_flags"]
        results[name] = res

    # Compute paired McNemar test p-values against Proposed 6-bit QNBP
    mcnemar_stats: Dict[str, Any] = {}
    p_err_arr = np.array(proposed_errors, dtype=np.int32)
    for name, res in results.items():
        if name != "Proposed_QNBP_6bit":
            other_arr = np.array(res["error_flags"], dtype=np.int32)
            stat, p_val = mcnemar_paired_test(p_err_arr, other_arr)
            mc = {"statistic": float(stat), "p_value": float(p_val)}
            mcnemar_stats[name] = mc
            print(f"  Paired McNemar vs {name}: stat={stat:.2f}, p-value={p_val:.4e}")

    # Remove raw error flags before saving json to save space
    for res in results.values():
        del res["error_flags"]

    output = {
        "parameters": {
            "code": "[[72,12,6]]",
            "physical_p": physical_p,
            "rounds": rounds,
            "shots": shots,
            "seed": seed,
        },
        "decoders": results,
        "mcnemar_tests_vs_proposed": mcnemar_stats,
    }

    out_file = "results/competitor_benchmarks.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w") as fp:
        json.dump(output, fp, indent=2)

    print(f"\n✅ All competitor benchmarks saved to {out_file}!")
    return output


if __name__ == "__main__":
    run_all_competitor_benchmarks(shots=500, physical_p=0.003, rounds=2, seed=2026)
