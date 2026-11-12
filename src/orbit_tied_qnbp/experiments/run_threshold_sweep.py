"""Physical error rate threshold sweep comparing QNBP, BP, and BP+OSD.

Samples genuine Stim circuit depolarizing errors across p in {0.001, 0.002, 0.003, 0.004, 0.005}
and benchmarks:
1. Classical Min-Sum BP (A1, normalized ms_scaling_factor=0.75 via C++ ldpc.BpDecoder)
2. Orbit-Tied QNBP (A4, proposed 4-bit integer quantized neural BP)
3. Gold-Standard BP+OSD-0 (via C++ ldpc.BpOsdDecoder)

Exports raw data and Wilson confidence intervals to results/threshold_sweep.json.
"""

from typing import Dict, Any, List
import json
import os
import time
import numpy as np
import scipy.sparse as sp
import torch
from ldpc import BpDecoder, BpOsdDecoder

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.qnbp import OrbitTiedQNBP
from orbit_tied_qnbp.experiments.data_loader import QecDataLoader
from orbit_tied_qnbp.experiments.trainer import QnbpTrainer
from orbit_tied_qnbp.utils.metrics import format_ci_metric


def run_threshold_sweep(
    p_values: List[float] = [0.001, 0.002, 0.003, 0.004, 0.005],
    num_train: int = 100,
    num_test: int = 200,
    rounds: int = 3,
    output_path: str = "results/threshold_sweep.json",
) -> Dict[str, Any]:
    """Executes the multi-point physical error rate sweep."""
    start_time = time.time()
    code = BivariateBicycleCode.code_72_12_6()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    results: Dict[str, Any] = {
        "metadata": {
            "code": "[[72,12,6]]",
            "rounds": rounds,
            "p_values": p_values,
            "num_test": num_test,
        },
        "points": {},
    }

    loader = QecDataLoader(code=code, num_rounds=rounds)

    for p in p_values:
        p_str = f"{p:.4f}"
        print("\n==========================================", flush=True)
        print(f"  Physical Error Rate p = {p_str}", flush=True)
        print("==========================================", flush=True)

        circuit = code.build_stim_circuit(rounds=rounds, error_rate=p)
        dem = circuit.detector_error_model(decompose_errors=False)
        graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

        # 1. Deterministic paired datasets for this p
        train_syn, train_obs = loader.get_dataset(p, num_train, seed=100 + int(p * 10000), split="train")
        test_syn, test_obs = loader.get_dataset(p, num_test, seed=200 + int(p * 10000), split="test")

        # 2. Setup Parity Check Matrix and prior probabilities for C++ decoders
        c_idx = graph.check_nodes_per_edge.numpy()
        f_idx = graph.fault_nodes_per_edge.numpy()
        pcm = sp.coo_matrix(
            (np.ones(len(c_idx)), (c_idx, f_idx)),
            shape=(graph.num_detectors, graph.num_faults),
        ).tocsr()
        channel_probs = graph.prior_probs.numpy().astype(np.float64)
        obs_mat = graph.obs_matrix.cpu().numpy()

        # A. Evaluate C++ BpDecoder (Min-Sum with scaling 0.75)
        print("  Evaluating C++ ldpc.BpDecoder (A1)...", flush=True)
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

        # B. Train and Evaluate Orbit-Tied QNBP (A4)
        print("  Training and Evaluating Orbit-Tied QNBP (A4)...", flush=True)
        qnbp_model = OrbitTiedQNBP(
            graph=graph,
            num_layers=15,
            bit_width=6,
            quantize=True,
            use_boundary_classes=True,
        )
        trainer = QnbpTrainer(model=qnbp_model, lr=0.005)
        for _ in range(2):
            trainer.train_epoch(train_syn, train_obs, batch_size=64, loss_type="soft_syndrome")

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
        print(f"    QNBP LER: {qnbp_ci['display']}", flush=True)

        # C. Evaluate C++ BpOsdDecoder (Gold-standard BP+OSD-0)
        print("  Evaluating C++ ldpc.BpOsdDecoder (A8 Gold-Standard)...", flush=True)
        bposd_dec = BpOsdDecoder(
            pcm,
            channel_probs=channel_probs,
            max_iter=20,
            bp_method="ms",
            ms_scaling_factor=0.75,
            osd_method="osd0",
            osd_order=0,
        )
        bposd_errors = 0
        for i in range(num_test):
            corr = bposd_dec.decode(test_syn[i])
            pred_obs = (corr @ obs_mat.T) % 2
            bposd_errors += int(np.any(pred_obs != test_obs[i]))
        bposd_ci = format_ci_metric(bposd_errors, num_test)
        print(f"    BP+OSD LER: {bposd_ci['display']}", flush=True)

        results["points"][p_str] = {
            "physical_p": p,
            "bp": bp_ci,
            "qnbp": qnbp_ci,
            "bposd": bposd_ci,
        }

    elapsed = time.time() - start_time
    results["metadata"]["elapsed_seconds"] = elapsed
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Threshold Sweep Finished in {elapsed:.1f}s. Saved to {output_path}", flush=True)
    return results


if __name__ == "__main__":
    run_threshold_sweep()
