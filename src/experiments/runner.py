"""Execution harness for individual ablation models on paired datasets.

Evaluates decoders on identical Stim test shots and records logical error rates,
iteration counts, and 95% Wilson confidence intervals.
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import scipy.sparse as sp
import torch
from ldpc import BpDecoder, BpOsdDecoder

from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph
from src.decoder.baselines import MinSumDecoder, DecodeResult
from src.decoder.qnbp import OrbitTiedQNBP
from src.decoder.integer_reference import IntegerQNBP
from src.experiments.trainer import QnbpTrainer
from src.utils.metrics import format_ci_metric, wilson_score_interval


def evaluate_minsum_decoder(
    decoder: MinSumDecoder,
    syndromes: np.ndarray,
    true_observables: np.ndarray,
) -> Dict[str, Any]:
    """Evaluates a MinSumDecoder on paired test shots."""
    n_shots = len(syndromes)
    logical_errors = 0
    iterations_list = []
    converged_count = 0
    outcomes = np.zeros(n_shots, dtype=np.uint8)

    for i in range(n_shots):
        res = decoder.decode(syndromes[i])
        iterations_list.append(res.iterations)
        if res.converged:
            converged_count += 1

        is_error = int(np.any(res.predicted_observables != true_observables[i]))
        outcomes[i] = is_error
        logical_errors += is_error

    ci = format_ci_metric(logical_errors, n_shots)
    return {
        **ci,
        "mean_iterations": float(np.mean(iterations_list)),
        "convergence_rate": converged_count / max(1, n_shots),
        "raw_outcomes": outcomes,
    }


def evaluate_integer_decoder(
    decoder: IntegerQNBP,
    syndromes: np.ndarray,
    true_observables: np.ndarray,
) -> Dict[str, Any]:
    """Evaluates the integer reference decoder on paired test shots."""
    n_shots = len(syndromes)
    logical_errors = 0
    iterations_list = []
    converged_count = 0
    outcomes = np.zeros(n_shots, dtype=np.uint8)

    for i in range(n_shots):
        res = decoder.decode(syndromes[i])
        iterations_list.append(res.iterations)
        if res.converged:
            converged_count += 1

        is_error = int(np.any(res.predicted_observables != true_observables[i]))
        outcomes[i] = is_error
        logical_errors += is_error

    ci = format_ci_metric(logical_errors, n_shots)
    return {
        **ci,
        "mean_iterations": float(np.mean(iterations_list)),
        "convergence_rate": converged_count / max(1, n_shots),
        "raw_outcomes": outcomes,
    }


def evaluate_cpp_bp_decoder(
    graph: DemGraph,
    syndromes: np.ndarray,
    true_observables: np.ndarray,
    max_iter: int = 15,
    bp_method: str = "ms",
    ms_scaling_factor: float = 0.75,
) -> Dict[str, Any]:
    """Evaluates the official C++ ldpc.BpDecoder on paired test shots."""
    c_idx = graph.check_nodes_per_edge.numpy()
    f_idx = graph.fault_nodes_per_edge.numpy()
    pcm = sp.coo_matrix(
        (np.ones(len(c_idx)), (c_idx, f_idx)),
        shape=(graph.num_detectors, graph.num_faults),
    ).tocsr()
    channel_probs = graph.prior_probs.numpy().astype(np.float64)
    decoder = BpDecoder(
        pcm,
        channel_probs=channel_probs,
        max_iter=max_iter,
        bp_method=bp_method,
        ms_scaling_factor=ms_scaling_factor,
    )
    obs_mat = graph.obs_matrix.cpu().numpy()
    n_shots = len(syndromes)
    logical_errors = 0
    iterations_list = []
    converged_count = 0
    outcomes = np.zeros(n_shots, dtype=np.uint8)

    for i in range(n_shots):
        corr = decoder.decode(syndromes[i])
        iterations_list.append(int(decoder.iter))
        if decoder.converge:
            converged_count += 1
        pred_obs = (corr @ obs_mat.T) % 2
        is_error = int(np.any(pred_obs != true_observables[i]))
        outcomes[i] = is_error
        logical_errors += is_error

    ci = format_ci_metric(logical_errors, n_shots)
    return {
        **ci,
        "mean_iterations": float(np.mean(iterations_list)),
        "convergence_rate": converged_count / max(1, n_shots),
        "raw_outcomes": outcomes,
    }


def evaluate_cpp_bposd_decoder(
    graph: DemGraph,
    syndromes: np.ndarray,
    true_observables: np.ndarray,
    max_iter: int = 20,
    bp_method: str = "ms",
    osd_method: str = "osd0",
    osd_order: int = 0,
    ms_scaling_factor: float = 0.75,
) -> Dict[str, Any]:
    """Evaluates the official C++ ldpc.BpOsdDecoder on paired test shots."""
    c_idx = graph.check_nodes_per_edge.numpy()
    f_idx = graph.fault_nodes_per_edge.numpy()
    pcm = sp.coo_matrix(
        (np.ones(len(c_idx)), (c_idx, f_idx)),
        shape=(graph.num_detectors, graph.num_faults),
    ).tocsr()
    channel_probs = graph.prior_probs.numpy().astype(np.float64)
    decoder = BpOsdDecoder(
        pcm,
        channel_probs=channel_probs,
        max_iter=max_iter,
        bp_method=bp_method,
        ms_scaling_factor=ms_scaling_factor,
        osd_method=osd_method,
        osd_order=osd_order,
    )
    obs_mat = graph.obs_matrix.cpu().numpy()
    n_shots = len(syndromes)
    logical_errors = 0
    iterations_list = []
    converged_count = 0
    outcomes = np.zeros(n_shots, dtype=np.uint8)

    for i in range(n_shots):
        corr = decoder.decode(syndromes[i])
        iterations_list.append(int(decoder.iter))
        if decoder.converge:
            converged_count += 1
        pred_obs = (corr @ obs_mat.T) % 2
        is_error = int(np.any(pred_obs != true_observables[i]))
        outcomes[i] = is_error
        logical_errors += is_error

    ci = format_ci_metric(logical_errors, n_shots)
    return {
        **ci,
        "mean_iterations": float(np.mean(iterations_list)),
        "convergence_rate": converged_count / max(1, n_shots),
        "raw_outcomes": outcomes,
    }


def train_and_eval_qnbp(
    graph: DemGraph,
    train_syn: np.ndarray,
    train_obs: np.ndarray,
    test_syn: np.ndarray,
    test_obs: np.ndarray,
    num_layers: int = 15,
    bit_width: int = 6,
    quantize: bool = True,
    custom_orbits: Optional[torch.Tensor] = None,
    use_boundary_classes: bool = True,
    loss_type: str = "soft_syndrome",
    epochs: int = 2,
    lr: float = 0.005,
) -> Tuple[OrbitTiedQNBP, Dict[str, Any]]:
    """Instantiates, trains, and evaluates a QNBP model variant with syndrome early-stopping."""
    model = OrbitTiedQNBP(
        graph=graph,
        num_layers=num_layers,
        bit_width=bit_width,
        quantize=quantize,
        custom_orbits=custom_orbits,
        use_boundary_classes=use_boundary_classes,
    )
    trainer = QnbpTrainer(model=model, lr=lr)

    for _ in range(epochs):
        trainer.train_epoch(train_syn, train_obs, batch_size=64, loss_type=loss_type)

    # Evaluate on test set
    model.eval()
    obs_mat = graph.obs_matrix.cpu().numpy()
    n_shots = len(test_syn)
    outcomes = np.zeros(n_shots, dtype=np.uint8)

    # Construct Parity Check Matrix to verify syndrome satisfaction
    c_idx = graph.check_nodes_per_edge.numpy()
    f_idx = graph.fault_nodes_per_edge.numpy()
    pcm = sp.coo_matrix(
        (np.ones(len(c_idx)), (c_idx, f_idx)),
        shape=(graph.num_detectors, graph.num_faults),
    ).tocsr()

    converged_shots = 0
    iterations_taken: List[int] = []

    with torch.no_grad():
        syn_t = torch.from_numpy(test_syn)
        outputs = model(syn_t)

        best_corr = outputs[-1][1].cpu().numpy().copy()
        converged_mask = np.zeros(n_shots, dtype=bool)
        iter_used = np.full(n_shots, num_layers, dtype=np.int32)

        for t in range(num_layers):
            corr_t = outputs[t][1].cpu().numpy()
            syn_pred = (pcm @ corr_t.T) % 2
            match_t = np.all(syn_pred == test_syn.T, axis=0)

            newly_converged = match_t & (~converged_mask)
            if np.any(newly_converged):
                best_corr[newly_converged] = corr_t[newly_converged]
                iter_used[newly_converged] = t + 1
                converged_mask[newly_converged] = True

        converged_shots = int(np.sum(converged_mask))
        iterations_taken = iter_used.tolist()
        pred_obs = (best_corr @ obs_mat.T) % 2
        outcomes = np.any(pred_obs != test_obs, axis=1).astype(np.uint8)

    logical_errors = int(np.sum(outcomes))
    ci = format_ci_metric(logical_errors, n_shots)
    return model, {
        **ci,
        "mean_iterations": float(np.mean(iterations_taken)),
        "convergence_rate": converged_shots / max(1, n_shots),
        "raw_outcomes": outcomes,
    }
