"""Tune Normalized Min-Sum parameters (alpha, max_iter) on held-out dataset.

Evaluates alpha in {0.5, 0.625, 0.75, 0.875, 1.0} and max_iter in {15, 30, 50}
on 500 held-out shots of [[72,12,6]] bivariate-bicycle code at p=0.003.
Saves results to results/min_sum_tuning.json.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List

# Ensure src is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.competitor_baselines import FastBpBaselineDecoder
from orbit_tied_qnbp.utils.metrics import wilson_score_interval


def tune_min_sum(
    shots: int = 500,
    physical_p: float = 0.003,
    rounds: int = 2,
    seed: int = 9999,  # Distinct held-out seed
    out_path: str = "results/min_sum_tuning.json",
) -> Dict[str, Any]:
    print(f"--- Running Min-Sum Tuning on {shots} held-out shots (seed={seed}, p={physical_p}) ---")
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=physical_p)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    sampler = circuit.compile_detector_sampler(seed=seed)
    syn, obs = sampler.sample(shots=shots, separate_observables=True)

    alphas = [0.5, 0.625, 0.75, 0.875, 1.0]
    iters_list = [15, 30, 50]

    sweep_results: List[Dict[str, Any]] = []
    best_config: Dict[str, Any] | None = None
    best_ler = 1.0

    for alpha in alphas:
        for iters in iters_list:
            t0 = time.perf_counter()
            dec = FastBpBaselineDecoder(graph=graph, max_iter=iters, alpha=alpha)

            errors = 0
            conv_count = 0
            tot_iters = 0

            for s, true_o in zip(syn, obs):
                res = dec.decode(s)
                err = not np.array_equal(res.predicted_observables, true_o)
                if err:
                    errors += 1
                if res.converged:
                    conv_count += 1
                tot_iters += res.iterations

            elapsed = time.perf_counter() - t0
            ler = errors / shots
            ci_low, _, ci_high = wilson_score_interval(errors, shots)
            mean_iter = tot_iters / shots
            conv_rate = conv_count / shots

            entry = {
                "alpha": float(alpha),
                "max_iter": int(iters),
                "shots": int(shots),
                "errors": int(errors),
                "ler": float(ler),
                "ci_lower": float(ci_low),
                "ci_upper": float(ci_high),
                "mean_iterations": float(mean_iter),
                "convergence_rate": float(conv_rate),
                "elapsed_s": float(elapsed),
            }
            sweep_results.append(entry)

            print(
                f"alpha={alpha:5.3f}, iters={iters:2d} -> "
                f"errors={errors:3d}/{shots} (LER={ler:.4f} [{ci_low:.4f}, {ci_high:.4f}]), "
                f"conv={conv_rate*100:.1f}%, mean_iter={mean_iter:.1f}, time={elapsed:.2f}s"
            )

            if ler < best_ler or (ler == best_ler and mean_iter < (best_config["mean_iterations"] if best_config else 999)):
                best_ler = ler
                best_config = entry

    data = {
        "description": "Grid tuning of Normalized Min-Sum scaling factor alpha and max iterations on held-out set",
        "code": "[[72, 12, 6]]",
        "physical_p": physical_p,
        "rounds": rounds,
        "shots": shots,
        "seed": seed,
        "alphas_tested": alphas,
        "iters_tested": iters_list,
        "best_configuration": best_config,
        "grid_results": sweep_results,
    }

    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\nSaved tuning results to {out_path}")
    print(f"Optimal configuration: alpha={best_config['alpha']}, max_iter={best_config['max_iter']} with LER={best_config['ler']:.4f}")
    return data


if __name__ == "__main__":
    tune_min_sum()
