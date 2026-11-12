"""Novelty Benchmarks: Biased Noise and Relay-BP (IBM Müller et al.) Evaluation.

Generates empirical evidence for:
1. Biased Pauli Noise (eta in {1, 10, 50, 100}) demonstrating that Orbit-Tied QNBP
   exploits asymmetry to reduce logical errors without parameter explosion.
2. Relay-BP comparison demonstrating that 6-bit integer QNBP matches or beats
   Relay-BP while running multiplier-free in hardware (DSP=0).
"""

from typing import Dict, Any, List
import json
import os
import numpy as np
import stim

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.baselines import MinSumDecoder, RelayBPDecoder
from orbit_tied_qnbp.decoder.integer_reference import IntegerQNBP
from orbit_tied_qnbp.decoder.orbits import DemOrbitManager
from orbit_tied_qnbp.experiments.runner import (
    evaluate_minsum_decoder,
    evaluate_relay_bp_decoder,
    evaluate_integer_decoder,
)
from orbit_tied_qnbp.utils.metrics import format_ci_metric


def run_biased_noise_sweep(
    n_shots: int = 200,
    physical_p: float = 0.003,
    biases: List[float] = [1.0, 10.0, 50.0, 100.0],
    seed: int = 42,
) -> Dict[str, Any]:
    """Sweeps Pauli Z bias ratio eta and evaluates BP vs. Orbit-Tied QNBP."""
    print("=" * 70)
    print(f"🔬 RUNNING BIASED NOISE SWEEP (p={physical_p}, shots={n_shots})")
    print("=" * 70)

    code = BivariateBicycleCode.code_72_12_6()
    rounds = 3
    results: Dict[str, Any] = {}

    for eta in biases:
        print(f"\n--- Evaluating Bias eta = {eta:.1f} ---")
        circuit = code.build_stim_circuit(rounds=rounds, error_rate=physical_p, bias=eta)
        dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
        graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

        # Sample test shots
        sampler = circuit.compile_detector_sampler(seed=seed + int(eta))
        syn, obs = sampler.sample(shots=n_shots, separate_observables=True)

        # 1. Classical Min-Sum BP (alpha=0.75)
        bp_dec = MinSumDecoder(graph=graph, max_iter=15, alpha=0.75)
        bp_metrics = evaluate_minsum_decoder(bp_dec, syn, obs)
        print(f"  Classical BP:  LER = {bp_metrics['rate']:.4f} [{bp_metrics['ci_95_lower']:.4f}, {bp_metrics['ci_95_upper']:.4f}]")

        # 2. Integer 6-bit QNBP (CSD shifts, DSP=0)
        qnbp_int = IntegerQNBP(graph=graph, num_layers=15, bit_width=6, alpha_val=0.75)
        int_metrics = evaluate_integer_decoder(qnbp_int, syn, obs)
        print(f"  Integer QNBP:  LER = {int_metrics['rate']:.4f} [{int_metrics['ci_95_lower']:.4f}, {int_metrics['ci_95_upper']:.4f}]")

        results[f"eta_{int(eta)}"] = {
            "bias_eta": eta,
            "physical_p": physical_p,
            "num_faults": graph.num_faults,
            "bp": {
                "rate": bp_metrics["rate"],
                "ci_lower": bp_metrics["ci_95_lower"],
                "ci_upper": bp_metrics["ci_95_upper"],
                "display": bp_metrics["display"],
                "mean_iterations": bp_metrics["mean_iterations"],
            },
            "qnbp_int_6bit": {
                "rate": int_metrics["rate"],
                "ci_lower": int_metrics["ci_95_lower"],
                "ci_upper": int_metrics["ci_95_upper"],
                "display": int_metrics["display"],
                "mean_iterations": int_metrics["mean_iterations"],
            },
        }

    return results


def run_relay_bp_comparison(
    n_shots: int = 250,
    physical_p: float = 0.003,
    seed: int = 1234,
) -> Dict[str, Any]:
    """Compares Min-Sum BP vs. Relay-BP vs. QNBP on identical paired shots."""
    print("\n" + "=" * 70)
    print(f"🔬 RUNNING RELAY-BP (IBM MÜLLER ET AL.) COMPARISON (p={physical_p}, shots={n_shots})")
    print("=" * 70)

    code = BivariateBicycleCode.code_72_12_6()
    rounds = 3
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=physical_p)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    sampler = circuit.compile_detector_sampler(seed=seed)
    syn, obs = sampler.sample(shots=n_shots, separate_observables=True)

    # 1. Classical Min-Sum BP
    bp = MinSumDecoder(graph=graph, max_iter=30, alpha=0.75)
    bp_metrics = evaluate_minsum_decoder(bp, syn, obs)
    print(f"  1. Classical BP (T=30):       LER = {bp_metrics['rate']:.4f} [{bp_metrics['ci_95_lower']:.4f}, {bp_metrics['ci_95_upper']:.4f}], iters = {bp_metrics['mean_iterations']:.1f}")

    # 2. Relay-BP (IBM Müller et al.: 3 relays x 10 iters, gamma=0.5)
    relay_bp = RelayBPDecoder(graph=graph, num_relays=3, iters_per_relay=10, alpha=0.75, relay_gamma=0.5)
    relay_metrics = evaluate_relay_bp_decoder(relay_bp, syn, obs)
    print(f"  2. Relay-BP (IBM Müller):     LER = {relay_metrics['rate']:.4f} [{relay_metrics['ci_95_lower']:.4f}, {relay_metrics['ci_95_upper']:.4f}], iters = {relay_metrics['mean_iterations']:.1f}")

    # 3. Proposed Orbit-Tied QNBP (6-bit Integer Reference, T=15, DSP=0)
    int_dec = IntegerQNBP(graph=graph, num_layers=15, bit_width=6, alpha_val=0.75)
    int_metrics = evaluate_integer_decoder(int_dec, syn, obs)
    print(f"  3. Proposed 6-bit QNBP (T=15): LER = {int_metrics['rate']:.4f} [{int_metrics['ci_95_lower']:.4f}, {int_metrics['ci_95_upper']:.4f}], iters = {int_metrics['mean_iterations']:.1f}")

    return {
        "classical_bp": {
            "rate": bp_metrics["rate"],
            "ci_lower": bp_metrics["ci_95_lower"],
            "ci_upper": bp_metrics["ci_95_upper"],
            "display": bp_metrics["display"],
            "mean_iterations": bp_metrics["mean_iterations"],
            "convergence_rate": bp_metrics["convergence_rate"],
        },
        "relay_bp_ibm": {
            "rate": relay_metrics["rate"],
            "ci_lower": relay_metrics["ci_95_lower"],
            "ci_upper": relay_metrics["ci_95_upper"],
            "display": relay_metrics["display"],
            "mean_iterations": relay_metrics["mean_iterations"],
            "convergence_rate": relay_metrics["convergence_rate"],
        },
        "proposed_qnbp_6bit": {
            "rate": int_metrics["rate"],
            "ci_lower": int_metrics["ci_95_lower"],
            "ci_upper": int_metrics["ci_95_upper"],
            "display": int_metrics["display"],
            "mean_iterations": int_metrics["mean_iterations"],
            "convergence_rate": int_metrics["convergence_rate"],
        },
    }


def main() -> None:
    biased_results = run_biased_noise_sweep(n_shots=200, physical_p=0.003)
    relay_results = run_relay_bp_comparison(n_shots=250, physical_p=0.003)

    combined = {
        "biased_noise_sweep": biased_results,
        "relay_bp_comparison": relay_results,
    }

    out_path = "results/novelty_benchmarks.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as fp:
        json.dump(combined, fp, indent=2)

    print(f"\n✅ Novelty benchmark results successfully saved to {out_path}!")


if __name__ == "__main__":
    main()
