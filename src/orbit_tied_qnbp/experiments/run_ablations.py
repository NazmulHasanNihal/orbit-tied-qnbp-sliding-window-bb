"""Master execution script for the Phase 2 Ablation Ladder (A0 - A10).

Runs all ablation experiments under paired Stim shots on [[72, 12, 6]],
computes 95% Wilson confidence intervals, and exports results/ablations_results.json.
"""

from typing import Dict, Any, List
import json
import os
import time
import numpy as np
import torch

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.baselines import MinSumDecoder
from orbit_tied_qnbp.decoder.integer_reference import IntegerQNBP
from orbit_tied_qnbp.decoder.sliding_window import ConfidenceGate, TraceDrivenQueueSimulator
from orbit_tied_qnbp.experiments.data_loader import QecDataLoader
from orbit_tied_qnbp.experiments.runner import (
    evaluate_minsum_decoder,
    evaluate_integer_decoder,
    evaluate_cpp_bp_decoder,
    evaluate_cpp_bposd_decoder,
    train_and_eval_qnbp,
)
from orbit_tied_qnbp.utils.metrics import format_ci_metric, mcnemar_paired_test


def run_full_ablation_ladder(
    num_train: int = 150,
    num_val: int = 100,
    num_test: int = 250,
    p_phys: float = 0.003,
    output_path: str = "results/ablations_results.json",
) -> Dict[str, Any]:
    """Runs the complete experiment ladder A0 to A10."""
    start_time = time.time()
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 3
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=p_phys)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    # 1. Deterministic paired datasets
    loader = QecDataLoader(code=code, num_rounds=rounds)
    train_syn, train_obs = loader.get_dataset(p_phys, num_train, seed=10, split="train")
    val_syn, val_obs = loader.get_dataset(p_phys, num_val, seed=20, split="val")
    test_syn, test_obs = loader.get_dataset(p_phys, num_test, seed=30, split="test")

    results: Dict[str, Any] = {
        "metadata": {
            "code": "[[72,12,6]]",
            "rounds": rounds,
            "physical_p": p_phys,
            "num_test": num_test,
        },
        "ablations": {},
    }

    print("\n--- Running Baseline A0: Floating-point Unweighted Min-Sum ---", flush=True)
    dec_a0 = MinSumDecoder(graph=graph, max_iter=15, alpha=1.0)
    res_a0 = evaluate_minsum_decoder(dec_a0, test_syn, test_obs)
    results["ablations"]["A0_unweighted_minsum"] = res_a0
    print(f"A0 LER: {res_a0['display']}", flush=True)

    print("\n--- Running Baseline A1: Normalized Min-Sum (Tuned alpha) ---", flush=True)
    best_alpha = 0.75
    dec_a1 = MinSumDecoder(graph=graph, max_iter=15, alpha=best_alpha)
    res_a1 = evaluate_minsum_decoder(dec_a1, test_syn, test_obs)
    results["ablations"]["A1_normalized_minsum"] = res_a1
    print(f"A1 (alpha={best_alpha}) LER: {res_a1['display']}", flush=True)

    print("\n--- Running Baseline A1 (C++ ldpc.BpDecoder) ---", flush=True)
    res_a1_cpp = evaluate_cpp_bp_decoder(graph, test_syn, test_obs, max_iter=15, ms_scaling_factor=best_alpha)
    results["ablations"]["A1_cpp_bp"] = res_a1_cpp
    print(f"A1 C++ BP LER: {res_a1_cpp['display']}", flush=True)

    print("\n--- Running A2: Untied Unfolded NBP ---", flush=True)
    untied_orbits = torch.arange(graph.num_faults, dtype=torch.int64)
    _, res_a2 = train_and_eval_qnbp(
        graph, train_syn, train_obs, test_syn, test_obs,
        custom_orbits=untied_orbits, num_layers=15, epochs=2
    )
    results["ablations"]["A2_untied_nbp"] = res_a2
    print(f"A2 (untied) LER: {res_a2['display']}", flush=True)

    print("\n--- Running A3: Orbit-Tied NBP (No Boundary Classes) ---", flush=True)
    _, res_a3 = train_and_eval_qnbp(
        graph, train_syn, train_obs, test_syn, test_obs,
        use_boundary_classes=False, num_layers=15, epochs=2
    )
    results["ablations"]["A3_orbit_tied_no_boundary"] = res_a3
    print(f"A3 (orbit-tied, no boundary) LER: {res_a3['display']}", flush=True)

    print("\n--- Running A4: Headline Orbit-Tied QNBP (With Boundary Classes) ---", flush=True)
    model_a4, res_a4 = train_and_eval_qnbp(
        graph, train_syn, train_obs, test_syn, test_obs,
        use_boundary_classes=True, bit_width=6, quantize=True, num_layers=15, epochs=2
    )
    results["ablations"]["A4_orbit_tied_with_boundary"] = res_a4
    print(f"A4 (proposed 6-bit) LER: {res_a4['display']}", flush=True)

    print("\n--- Running A5: Random-Tying Control (5 Seeds) ---", flush=True)
    a5_runs = []
    a5_first_outcomes = None
    num_orbits = int(torch.max(graph.fault_orbits).item()) + 1
    for seed_idx, seed in enumerate([101, 102, 103, 104, 105]):
        np.random.seed(seed)
        rand_orbits = torch.tensor(
            np.random.randint(0, num_orbits, size=graph.num_faults), dtype=torch.int64
        )
        _, res_a5_s = train_and_eval_qnbp(
            graph, train_syn, train_obs, test_syn, test_obs,
            custom_orbits=rand_orbits, num_layers=15, epochs=2
        )
        a5_runs.append(res_a5_s["rate"])
        if a5_first_outcomes is None:
            a5_first_outcomes = res_a5_s["raw_outcomes"]
        print(f"  Seed {seed}: LER = {res_a5_s['rate']:.4e}", flush=True)
    results["ablations"]["A5_random_tying_control"] = {
        "mean_rate": float(np.mean(a5_runs)),
        "std_rate": float(np.std(a5_runs)),
        "runs": a5_runs,
    }
    print(f"A5 Random Control: {np.mean(a5_runs):.4e} +/- {np.std(a5_runs):.4e}", flush=True)

    print("\n--- Running A6: Loss Function Comparison ---", flush=True)
    _, res_a6_soft = train_and_eval_qnbp(
        graph, train_syn, train_obs, test_syn, test_obs,
        loss_type="softplus_parity", num_layers=15, epochs=2
    )
    results["ablations"]["A6_loss_comparison"] = {
        "soft_syndrome": res_a4["rate"],
        "softplus_parity": res_a6_soft["rate"],
    }
    print(
        f"A6: Soft Syndrome (proposed): {res_a4['rate']:.4e} | Softplus parity: {res_a6_soft['rate']:.4e}",
        flush=True,
    )

    print("\n--- Running A7: Quantization Bit-Width Sweep ---", flush=True)
    a7_results = {}
    for b_bits in [32, 6, 5, 4, 3]:
        quant_active = b_bits != 32
        eff_bits = 4 if b_bits == 32 else b_bits
        _, res_a7 = train_and_eval_qnbp(
            graph, train_syn, train_obs, test_syn, test_obs,
            bit_width=eff_bits, quantize=quant_active, num_layers=15, epochs=2
        )
        a7_results[f"{b_bits}bit"] = res_a7["rate"]
        print(f"  {b_bits}-bit LER: {res_a7['display']}", flush=True)

    # Integer Reference Model verification
    dec_int = IntegerQNBP(graph=graph, num_layers=15, bit_width=6, alpha_val=0.75)
    res_int = evaluate_integer_decoder(dec_int, test_syn, test_obs)
    a7_results["integer_hardware_reference_6bit"] = res_int["rate"]
    results["ablations"]["A7_quantization_sweep"] = a7_results
    print(f"  Integer Hardware Ref 6-bit LER: {res_int['display']}", flush=True)

    print("\n--- Running A8: Gold-Standard C++ BP+OSD-0 (`ldpc.BpOsdDecoder`) ---", flush=True)
    res_a8_bposd = evaluate_cpp_bposd_decoder(
        graph, test_syn, test_obs, max_iter=20, ms_scaling_factor=best_alpha, osd_method="osd0"
    )
    results["ablations"]["A8_cpp_bposd_gold_standard"] = res_a8_bposd
    print(f"A8 Gold-Standard C++ BP+OSD LER: {res_a8_bposd['display']}", flush=True)

    print("\n--- Running A9: Fast-Path Confidence Margin Gates ---", flush=True)
    gate_sweep = {}
    obs_mat_np = graph.obs_matrix.cpu().numpy()
    dec_test = MinSumDecoder(graph=graph, max_iter=15, alpha=0.75)
    print(f"Pre-decoding {num_test} test shots for margin gate evaluation...", flush=True)
    decode_results = [dec_test.decode(test_syn[i]) for i in range(num_test)]
    error_flags = [int(np.any(res.predicted_observables != test_obs[i])) for i, res in enumerate(decode_results)]

    for tau in [0.5, 1.0, 1.5, 2.0, 3.0]:
        acc_g1, acc_g2, acc_g3 = 0, 0, 0
        err_g1, err_g2, err_g3 = 0, 0, 0
        for i, res_i in enumerate(decode_results):
            is_err = error_flags[i]
            if ConfidenceGate.evaluate("G1", res_i, obs_mat_np, tau):
                acc_g1 += 1
                err_g1 += is_err
            if ConfidenceGate.evaluate("G2", res_i, obs_mat_np, tau):
                acc_g2 += 1
                err_g2 += is_err
            if ConfidenceGate.evaluate("G3", res_i, obs_mat_np, tau):
                acc_g3 += 1
                err_g3 += is_err
        gate_sweep[f"tau_{tau}"] = {
            "G1": {"p_accept": acc_g1 / num_test, "error_in_accept": err_g1 / max(1, acc_g1)},
            "G2": {"p_accept": acc_g2 / num_test, "error_in_accept": err_g2 / max(1, acc_g2)},
            "G3": {"p_accept": acc_g3 / num_test, "error_in_accept": err_g3 / max(1, acc_g3)},
        }
    results["ablations"]["A9_gate_sweep"] = gate_sweep
    print(
        f"A9 Gate G3 at tau=1.5: Accept={gate_sweep['tau_1.5']['G3']['p_accept']:.1%}, LER={gate_sweep['tau_1.5']['G3']['error_in_accept']:.4e}",
        flush=True,
    )

    print("\n--- Running A10: Trace-Driven Queue Backlog Simulation ---", flush=True)
    sim = TraceDrivenQueueSimulator(
        t_cycle_ns=1000.0,
        commit_stride=1,
        ns_per_iteration_fast=24.0,
        ns_per_iteration_slow=100.0,
    )
    tau_chosen = 1.5
    is_acc = [ConfidenceGate.evaluate("G3", res_i, obs_mat_np, tau_chosen) for res_i in decode_results]
    fast_iters = [res_i.iterations for res_i in decode_results]
    slow_iters = [20] * num_test

    queue_results = {}
    for cap in [0, 1, 2, 5, 10, 15, 20]:
        q_metrics = sim.simulate(
            is_accepted=is_acc, fast_iters=fast_iters, slow_iters=slow_iters, buffer_capacity=cap
        )
        queue_results[f"cap_{cap}"] = q_metrics
    results["ablations"]["A10_queue_simulation"] = queue_results
    print(
        f"A10 Queue at Cap 5: Overflow={queue_results['cap_5']['overflow_fraction']:.2%}, Avg Backlog={queue_results['cap_5']['avg_backlog']:.2f}",
        flush=True,
    )

    # Paired hypothesis test between A4 and A1
    stat, p_val = mcnemar_paired_test(res_a4["raw_outcomes"], res_a1["raw_outcomes"])
    results["ablations"]["A4_vs_A1_significance"] = {
        "mcnemar_statistic": stat,
        "p_value": p_val,
        "relative_gain": (res_a1["rate"] - res_a4["rate"]) / max(1e-6, res_a1["rate"]),
    }
    print(
        f"\nA4 vs A1 Relative Gain: {results['ablations']['A4_vs_A1_significance']['relative_gain']:.1%}, McNemar p-value = {p_val:.4e}",
        flush=True,
    )

    # Paired hypothesis test between A4 and A5 (Claim C1: Torus symmetry vs Random control)
    if a5_first_outcomes is not None:
        stat_c1, p_val_c1 = mcnemar_paired_test(res_a4["raw_outcomes"], a5_first_outcomes)
        results["ablations"]["A4_vs_A5_significance"] = {
            "mcnemar_statistic": stat_c1,
            "p_value": p_val_c1,
            "relative_gain": (np.mean(a5_runs) - res_a4["rate"]) / max(1e-6, np.mean(a5_runs)),
        }
        print(
            f"A4 vs A5 (Claim C1) Relative Gain: {results['ablations']['A4_vs_A5_significance']['relative_gain']:.1%}, McNemar p-value = {p_val_c1:.4e}",
            flush=True,
        )

    # Remove non-serializable raw outcome arrays
    for k, v in results["ablations"].items():
        if isinstance(v, dict) and "raw_outcomes" in v:
            del v["raw_outcomes"]

    elapsed = time.time() - start_time
    results["metadata"]["elapsed_seconds"] = elapsed
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Complete Ablation Ladder Finished in {elapsed:.1f}s. Saved to {output_path}", flush=True)
    return results


if __name__ == "__main__":
    run_full_ablation_ladder()
