"""Measure empirical software fallback latency distributions on CPU.

Benchmarks BP+OSD-CS-10 and IBM Relay-BP (5-leg and 30-leg) on >= 200 shots
at p=0.003, recording high-resolution CPU execution times.
Saves metrics (mean, std, min, p50, p90, p95, p99, max) to results/fallback_latency_distribution.json.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.competitor_baselines import BpOsdBaselineDecoder, FastRelayBpDecoder


def measure_fallback_latencies(
    shots: int = 250,
    physical_p: float = 0.003,
    rounds: int = 2,
    seed: int = 7777,
    out_path: str = "results/fallback_latency_distribution.json",
) -> Dict[str, Any]:
    print(f"=== Measuring Empirical Fallback Latency Distributions ({shots} shots, p={physical_p}) ===")
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=physical_p)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    sampler = circuit.compile_detector_sampler(seed=seed)
    syn, obs = sampler.sample(shots=shots, separate_observables=True)

    decoders = {
        "BP_OSD_CS_10": BpOsdBaselineDecoder(graph=graph, max_iter=30, ms_scaling_factor=0.75, osd_order=10),
        "IBM_Relay_BP_5leg": FastRelayBpDecoder(graph=graph, num_relays=5, iters_per_relay=10, alpha=0.75, relay_gamma=0.125),
        "IBM_Relay_BP_30leg": FastRelayBpDecoder(graph=graph, num_relays=30, iters_per_relay=10, alpha=0.75, relay_gamma=0.125),
    }

    results: Dict[str, Any] = {
        "metadata": {
            "shots": shots,
            "physical_p": physical_p,
            "rounds": rounds,
            "seed": seed,
            "platform": "x86_64 CPU (Python C++ wrapper via ldpc library)",
        },
        "decoders": {},
    }

    for name, dec in decoders.items():
        print(f"Profiling {name}...", flush=True)
        latencies_us: List[float] = []
        errors = 0

        # Warm-up 5 shots
        for s in syn[:5]:
            dec.decode(s)

        for s, true_o in zip(syn, obs):
            t0 = time.perf_counter_ns()
            res = dec.decode(s)
            t1 = time.perf_counter_ns()

            dt_us = (t1 - t0) / 1000.0
            latencies_us.append(dt_us)
            if not np.array_equal(res.predicted_observables, true_o):
                errors += 1

        arr = np.array(latencies_us)
        summary = {
            "shots": shots,
            "errors": errors,
            "error_rate": float(errors / shots),
            "mean_us": float(np.mean(arr)),
            "std_us": float(np.std(arr)),
            "min_us": float(np.min(arr)),
            "p50_us": float(np.percentile(arr, 50)),
            "p90_us": float(np.percentile(arr, 90)),
            "p95_us": float(np.percentile(arr, 95)),
            "p99_us": float(np.percentile(arr, 99)),
            "max_us": float(np.max(arr)),
        }
        results["decoders"][name] = summary
        print(
            f"  {name}: Mean={summary['mean_us']:.1f} us, p50={summary['p50_us']:.1f} us, "
            f"p95={summary['p95_us']:.1f} us, p99={summary['p99_us']:.1f} us, Max={summary['max_us']:.1f} us"
        )

    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved empirical fallback latency distributions to {out_path}")
    return results


if __name__ == "__main__":
    measure_fallback_latencies()
