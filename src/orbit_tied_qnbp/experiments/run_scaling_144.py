"""Generalization Scaling Experiment on [[144, 12, 12]] Gross BB Code.

Evaluates orbit extraction, 72x parameter collapse under Z_12 x Z_6 torus shifts,
and benchmarks 6-bit integer QNBP against Classical Min-Sum BP under circuit noise.
Exports results to results/scaling_results.json.
"""

from typing import Dict, Any
import json
import os
import time
import numpy as np
import scipy.sparse as sp
import torch
from ldpc import BpDecoder

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.baselines import MinSumDecoder
from orbit_tied_qnbp.decoder.orbits import DemOrbitManager
from orbit_tied_qnbp.decoder.qnbp import OrbitTiedQNBP
from orbit_tied_qnbp.experiments.data_loader import QecDataLoader
from orbit_tied_qnbp.experiments.trainer import QnbpTrainer
from orbit_tied_qnbp.utils.metrics import format_ci_metric


def run_scaling_experiment(
    num_train: int = 80,
    num_test: int = 150,
    p_phys: float = 0.003,
    rounds: int = 3,
    output_path: str = "results/scaling_results.json",
) -> Dict[str, Any]:
    """Runs the [[144, 12, 12]] code scaling experiment."""
    start_time = time.time()
    code = BivariateBicycleCode.code_144_12_12()
    print("\n==========================================", flush=True)
    print("  Running Scaling Benchmark: [[144, 12, 12]] (Group order |G| = 72)", flush=True)
    print("==========================================", flush=True)

    circuit = code.build_stim_circuit(rounds=rounds, error_rate=p_phys)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    # 1. Torus Automorphism Orbit verification
    orbit_manager = DemOrbitManager(code=code, num_rounds=rounds, dem=dem)
    n_orbits = orbit_manager.num_fault_orbits
    n_faults = graph.num_faults
    n_detectors = graph.num_detectors
    param_collapse = float(n_faults) / max(1, n_orbits)

    print(f"  Total Fault Mechanisms: {n_faults}", flush=True)
    print(f"  Total Detectors: {n_detectors}", flush=True)
    print(f"  Collapsed Symmetry Orbits: {n_orbits} ({param_collapse:.1f}x reduction)", flush=True)

    # 2. Datasets
    loader = QecDataLoader(code=code, num_rounds=rounds)
    train_syn, train_obs = loader.get_dataset(p_phys, num_train, seed=1441, split="train")
    test_syn, test_obs = loader.get_dataset(p_phys, num_test, seed=1442, split="test")

    # Setup Parity Check Matrix
    c_idx = graph.check_nodes_per_edge.numpy()
    f_idx = graph.fault_nodes_per_edge.numpy()
    pcm = sp.coo_matrix(
        (np.ones(len(c_idx)), (c_idx, f_idx)),
        shape=(graph.num_detectors, graph.num_faults),
    ).tocsr()
    channel_probs = graph.prior_probs.numpy().astype(np.float64)
    obs_mat = graph.obs_matrix.cpu().numpy()

    # 3. Baseline A1: Normalized Min-Sum (C++ ldpc.BpDecoder)
    print("  Evaluating Classical Min-Sum BP (C++ ldpc.BpDecoder)...", flush=True)
    bp_dec = BpDecoder(
        pcm, channel_probs=channel_probs, max_iter=15, bp_method="ms", ms_scaling_factor=0.75
    )
    bp_errors = 0
    for i in range(num_test):
        corr = bp_dec.decode(test_syn[i])
        pred_obs = (corr @ obs_mat.T) % 2
        bp_errors += int(np.any(pred_obs != test_obs[i]))
    bp_ci = format_ci_metric(bp_errors, num_test)
    print(f"    BP LER: {bp_ci['display']}", flush=True)

    # 4. Proposed 6-Bit Orbit-Tied QNBP
    print("  Training and Evaluating 6-Bit Orbit-Tied QNBP...", flush=True)
    qnbp_model = OrbitTiedQNBP(
        graph=graph,
        num_layers=15,
        bit_width=6,
        quantize=True,
        use_boundary_classes=True,
    )
    trainer = QnbpTrainer(model=qnbp_model, lr=0.005)
    for _ in range(2):
        trainer.train_epoch(train_syn, train_obs, batch_size=32, loss_type="soft_syndrome")

    qnbp_model.eval()
    with torch.no_grad():
        syn_t = torch.from_numpy(test_syn)
        outputs = qnbp_model(syn_t)
        best_corr = outputs[-1][1].cpu().numpy().copy()
        converged_mask = np.zeros(num_test, dtype=bool)

        for t in range(15):
            corr_t = outputs[t][1].cpu().numpy()
            syn_pred = (pcm @ corr_t.T) % 2
            match_t = np.all(syn_pred == test_syn.T, axis=0)
            newly_converged = match_t & (~converged_mask)
            if np.any(newly_converged):
                best_corr[newly_converged] = corr_t[newly_converged]
                converged_mask[newly_converged] = True

        pred_obs = (best_corr @ obs_mat.T) % 2
        outcomes = np.any(pred_obs != test_obs, axis=1).astype(np.uint8)
        qnbp_errors = int(np.sum(outcomes))
    qnbp_ci = format_ci_metric(qnbp_errors, num_test)
    print(f"    6-Bit QNBP LER: {qnbp_ci['display']}", flush=True)

    elapsed = time.time() - start_time
    results = {
        "metadata": {
            "code": "[[144,12,12]]",
            "group_order": 72,
            "rounds": rounds,
            "physical_p": p_phys,
            "num_test": num_test,
            "elapsed_seconds": elapsed,
        },
        "symmetries": {
            "num_faults": n_faults,
            "num_detectors": n_detectors,
            "num_orbits": n_orbits,
            "parameter_collapse_factor": param_collapse,
            "untied_weights_15layers": 15 * n_faults,
            "orbit_tied_weights_15layers": 15 * n_orbits + 45,
        },
        "performance": {
            "classical_min_sum_bp": bp_ci,
            "orbit_tied_qnbp_6bit": qnbp_ci,
        },
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ [[144, 12, 12]] Scaling Results Saved to {output_path} in {elapsed:.1f}s", flush=True)
    return results


if __name__ == "__main__":
    run_scaling_experiment()
