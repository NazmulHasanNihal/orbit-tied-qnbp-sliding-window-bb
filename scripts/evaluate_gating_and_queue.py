"""Fast-Path Confidence Gating and Discrete-Event Queue Simulation with Window Dependencies.

Models:
1. G1, G2, G3 confidence margin gates on [[72,12,6]] bivariate-bicycle code.
2. Exact conditional pipeline error P_pipe = (1-p_fb)*P(err|acc) + p_fb*P(err|fb).
3. Discrete-event queue simulation with inter-window dependencies:
   - Policy A: Speculative fast-path decoding under e_fast, roll back on mis-speculation (fallback differs).
   - Policy B: Stream stall/pause during fallback.
4. Stability threshold p_crit calculation and buffer overflow analysis.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Tuple

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.competitor_baselines import BpOsdBaselineDecoder
from orbit_tied_qnbp.decoder.integer_reference import IntegerQNBP
from orbit_tied_qnbp.decoder.sliding_window import ConfidenceGate
from orbit_tied_qnbp.utils.metrics import wilson_score_interval


def run_gating_calibration(
    shots: int = 500,
    physical_p: float = 0.001,
    rounds: int = 2,
    seed: int = 4040,
) -> Dict[str, Any]:
    """Calibrates G1, G2, G3 gates and computes P_pipe on paired shots."""
    print("=" * 78)
    print(f"🎯 FAST-PATH GATING CALIBRATION (p={physical_p}, N={shots})")
    print("=" * 78)

    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=physical_p)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)
    obs_mat = graph.obs_matrix.cpu().numpy().copy()

    # Fast-path decoder (6-bit Integer QNBP)
    fast_dec = IntegerQNBP(graph=graph, num_layers=15, bit_width=6, alpha_val=0.75)
    # Fallback decoder (BP+OSD-CS-10)
    slow_dec = BpOsdBaselineDecoder(graph=graph, max_iter=20, ms_scaling_factor=0.75, osd_order=10)

    sampler = circuit.compile_detector_sampler(seed=seed)
    syn, obs = sampler.sample(shots=shots, separate_observables=True)

    fast_results = [fast_dec.decode(s) for s in syn]
    slow_results = [slow_dec.decode(s) for s in syn]

    tau_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    gate_types = ["G1", "G2", "G3"]
    calibration_results: Dict[str, Any] = {}

    for g_type in gate_types:
        calibration_results[g_type] = {}
        for tau in tau_values:
            accepted_indices: List[int] = []
            fallback_indices: List[int] = []

            for idx, res in enumerate(fast_results):
                passed = ConfidenceGate.evaluate(g_type, res, obs_mat, tau=tau)
                if passed:
                    accepted_indices.append(idx)
                else:
                    fallback_indices.append(idx)

            p_fast = len(accepted_indices) / shots
            p_fb = len(fallback_indices) / shots

            fast_errors = 0
            for idx in accepted_indices:
                if not np.array_equal(fast_results[idx].predicted_observables, obs[idx]):
                    fast_errors += 1
            err_given_acc = fast_errors / max(1, len(accepted_indices))

            slow_errors = 0
            for idx in fallback_indices:
                if not np.array_equal(slow_results[idx].predicted_observables, obs[idx]):
                    slow_errors += 1
            err_given_fb = slow_errors / max(1, len(fallback_indices))

            p_pipe = (1.0 - p_fb) * err_given_acc + p_fb * err_given_fb

            calibration_results[g_type][f"tau_{tau:.1f}"] = {
                "tau": tau,
                "p_fast": float(p_fast),
                "p_fb": float(p_fb),
                "fast_errors": fast_errors,
                "slow_errors": slow_errors,
                "err_given_acc": float(err_given_acc),
                "err_given_fb": float(err_given_fb),
                "p_pipe": float(p_pipe),
            }
            print(f"Gate {g_type} (tau={tau:.1f}): Accept={p_fast*100:.1f}%, FastErr={err_given_acc:.4f}, P_pipe={p_pipe:.4f}")

    return {
        "parameters": {"shots": shots, "physical_p": physical_p, "rounds": rounds, "seed": seed},
        "gates": calibration_results,
        "fast_iterations": [r.iterations for r in fast_results],
        "slow_iterations": [r.iterations for r in slow_results],
    }


def simulate_discrete_event_queue_with_dependencies(
    n_windows: int = 10000,
    arrival_period_ns: float = 1000.0,
    t_fast_ns: float = 102.4,
    t_slow_mean_us: float = 320.0,
    t_slow_std_us: float = 80.0,
    p_fast: float = 0.756,
    p_diff_given_fallback: float = 0.0078,
    c_servers: int = 4,
    buffer_capacity: int = 16,
    policy: str = "speculative",
    seed: int = 42,
) -> Dict[str, Any]:
    """Simulates sliding-window queue with window dependencies under Policy A or B.

    Policy A (Speculative): Fast path speculatively executes window k+1 assuming e_fast^(k).
    Rollback occurs only when fallback returns differing correction (prob p_diff_given_fallback).

    Policy B (Stall): Pipeline pauses window k+1 until window k fallback finishes.
    """
    rng = np.random.default_rng(seed)
    server_free_times = np.zeros(c_servers, dtype=np.float64)

    # State tracking
    t_now = 0.0
    buffer_queue: List[float] = []  # arrival times of waiting windows
    overflows = 0
    rollbacks = 0
    backlog_history: List[int] = []

    # Log-normal distribution for slow fallback latency in ns
    mu_log = np.log(max(10.0, t_slow_mean_us * 1000.0))
    sigma_log = 0.4

    pipeline_busy_until = 0.0

    for i in range(n_windows):
        arrival_t = i * arrival_period_ns
        is_fast = rng.random() < p_fast
        slow_latency_ns = float(rng.lognormal(mu_log, sigma_log))

        if policy == "speculative":
            # Fast path decodes window immediately in t_fast_ns
            start_fast = max(arrival_t, pipeline_busy_until)
            finish_fast = start_fast + t_fast_ns
            pipeline_busy_until = finish_fast

            if not is_fast:
                # Dispatch to fallback worker pool asynchronously
                earliest_srv = int(np.argmin(server_free_times))
                fb_start = max(finish_fast, server_free_times[earliest_srv])
                fb_finish = fb_start + slow_latency_ns
                server_free_times[earliest_srv] = fb_finish

                # Mis-speculation check
                if rng.random() < p_diff_given_fallback:
                    rollbacks += 1
                    # Re-decoding penalty for mis-speculated window
                    pipeline_busy_until += t_fast_ns

            # Backlog is windows arriving before pipeline_busy_until
            current_backlog = max(0, int((pipeline_busy_until - arrival_t) / arrival_period_ns))
            backlog_history.append(current_backlog)
            if current_backlog >= buffer_capacity:
                overflows += 1

        elif policy == "stall":
            # Window k must complete fully before window k+1 can proceed
            start_t = max(arrival_t, pipeline_busy_until)
            if is_fast:
                finish_t = start_t + t_fast_ns
            else:
                # Fallback on worker pool
                earliest_srv = int(np.argmin(server_free_times))
                fb_start = max(start_t, server_free_times[earliest_srv])
                finish_t = fb_start + slow_latency_ns
                server_free_times[earliest_srv] = finish_t

            pipeline_busy_until = finish_t
            current_backlog = max(0, int((pipeline_busy_until - arrival_t) / arrival_period_ns))
            backlog_history.append(current_backlog)
            if current_backlog >= buffer_capacity:
                overflows += 1

    overflow_rate = overflows / n_windows
    mean_backlog = float(np.mean(backlog_history))
    max_backlog = int(np.max(backlog_history)) if backlog_history else 0

    # Theoretical queue stability threshold p_crit for Policy B
    p_crit_stall = float((arrival_period_ns - t_fast_ns) / max(1.0, (t_slow_mean_us * 1000.0 / c_servers) - t_fast_ns))

    return {
        "policy": policy,
        "n_windows": n_windows,
        "c_servers": c_servers,
        "buffer_capacity": buffer_capacity,
        "p_fast": float(p_fast),
        "overflows": overflows,
        "overflow_rate": float(overflow_rate),
        "rollbacks": rollbacks,
        "mean_backlog": mean_backlog,
        "max_backlog": max_backlog,
        "p_crit_stall": p_crit_stall,
    }


def main() -> None:
    # 1. Gate calibration and P_pipe computation
    calib = run_gating_calibration(shots=500, physical_p=0.001, rounds=2, seed=4040)

    # 2. Discrete-Event Queue Simulation with Window Dependencies
    print("\n" + "=" * 78)
    print("🚀 DISCRETE-EVENT QUEUE SIMULATION WITH WINDOW DEPENDENCIES")
    print("=" * 78)

    queue_results: Dict[str, Any] = {
        "metadata": {
            "arrival_period_ns": 1000.0,
            "t_fast_ns": 102.4,
            "t_slow_mean_us": 320.0,
            "p_fast_high_noise_p003": 0.756,
            "p_fast_sub_threshold_p001": 0.991,
        },
        "policy_A_speculative": {},
        "policy_B_stall": {},
    }

    # Sweep Policy A (Speculative Execution) at p=0.003
    print("\n--- Policy A: Speculative Decoding (p=0.003, p_fast=75.6%, p_diff=0.78%) ---")
    for buf in [4, 8, 16, 32, 64]:
        res = simulate_discrete_event_queue_with_dependencies(
            n_windows=20000,
            p_fast=0.756,
            p_diff_given_fallback=0.0078,
            c_servers=4,
            buffer_capacity=buf,
            policy="speculative",
        )
        queue_results["policy_A_speculative"][f"buf_{buf}"] = res
        print(f"  Buffer B={buf:2d}: Overflow={res['overflow_rate']*100:.3f}%, Rollbacks={res['rollbacks']}, MaxBacklog={res['max_backlog']}")

    # Sweep Policy B (Stream Stall) at p=0.001 and p=0.003
    print("\n--- Policy B: Stream Stall During Fallback (p=0.001 vs p=0.003) ---")
    for p_noise, p_acc in [(0.001, 0.991), (0.003, 0.756)]:
        queue_results["policy_B_stall"][f"p_{p_noise}"] = {}
        for c in [1, 4, 16]:
            res = simulate_discrete_event_queue_with_dependencies(
                n_windows=20000,
                p_fast=p_acc,
                c_servers=c,
                buffer_capacity=64,
                policy="stall",
            )
            queue_results["policy_B_stall"][f"p_{p_noise}"][f"servers_{c}"] = res
            print(f"  p={p_noise}, Servers c={c:2d}: p_crit={res['p_crit_stall']*100:.3f}%, Overflow={res['overflow_rate']*100:.2f}%, MaxBacklog={res['max_backlog']}")

    out_data = {
        "calibration": calib["gates"],
        "parameters": calib["parameters"],
        "queue_discrete_event": queue_results,
    }

    out_file = "results/gating_results.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as fp:
        json.dump(out_data, fp, indent=2)

    print(f"\nSaved updated gating calibration and discrete-event queue results to {out_file}!")


if __name__ == "__main__":
    main()
