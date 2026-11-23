"""Unit tests for exact differentiable soft-XOR observable parity loss."""

import pytest
import torch
import torch.nn.functional as F

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.qnbp import OrbitTiedQNBP


def test_soft_xor_two_flips_cancel():
    """Verify that two high-confidence error flips cancel in F_2 soft-XOR, yielding near-zero flip probability."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 2
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    model = OrbitTiedQNBP(graph=graph, num_layers=2, bit_width=6, quantize=False)

    # Find an observable with at least two participating fault nodes
    obs_idx = 0
    fault_indices = torch.where(model.obs_matrix[obs_idx] > 0)[0]
    assert len(fault_indices) >= 2, f"Observable {obs_idx} has fewer than 2 fault nodes"

    v1, v2 = fault_indices[0].item(), fault_indices[1].item()

    # Case A: No errors (all posteriors large positive, e.g. +20.0 for high-confidence no-fault)
    posteriors_no_err = torch.full((1, graph.num_faults), 20.0)
    
    # Case B: Exactly ONE error (v1 negative, e.g. -20.0)
    posteriors_one_err = torch.full((1, graph.num_faults), 20.0)
    posteriors_one_err[0, v1] = -20.0

    # Case C: TWO errors (both v1 and v2 negative, e.g. -20.0) -> MUST cancel in F_2!
    posteriors_two_err = torch.full((1, graph.num_faults), 20.0)
    posteriors_two_err[0, v1] = -20.0
    posteriors_two_err[0, v2] = -20.0

    # Test soft-XOR computation directly
    eps = 1e-7
    for name, post, expected_flip in [
        ("no_err", posteriors_no_err, False),
        ("one_err", posteriors_one_err, True),
        ("two_err", posteriors_two_err, False),
    ]:
        x = post / 2.0
        t = torch.tanh(x)
        log_abs_t = torch.log(torch.clamp(torch.abs(t), min=eps, max=1.0 - eps))
        signs = torch.sign(torch.where(t == 0, torch.ones_like(t), t))
        log_mag_sum = torch.matmul(log_abs_t, model.obs_matrix.T)
        mag_prod = torch.exp(log_mag_sum)
        neg_count = torch.matmul((signs < 0).float(), model.obs_matrix.T)
        sign_prod = torch.where(
            torch.fmod(neg_count, 2.0) == 1.0,
            -torch.ones_like(neg_count),
            torch.ones_like(neg_count),
        )
        prod_val = sign_prod.detach() * mag_prod
        hat_p = 0.5 * (1.0 - torch.clamp(prod_val, -1.0 + eps, 1.0 - eps))

        p_flip = hat_p[0, obs_idx].item()
        if expected_flip:
            assert p_flip > 0.90, f"Expected high flip probability for {name}, got {p_flip}"
        else:
            assert p_flip < 0.10, f"Expected cancellation / low flip probability for {name}, got {p_flip}"


def test_soft_xor_gradient_backprop():
    """Verify that gradients flow backward cleanly through soft-XOR observable loss without NaN or inf."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 2
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    model = OrbitTiedQNBP(graph=graph, num_layers=2, bit_width=6, quantize=True)
    syndromes = torch.zeros((2, graph.num_detectors), dtype=torch.uint8)
    syndromes[0, 1] = 1
    true_obs = torch.zeros((2, graph.num_observables), dtype=torch.float32)
    true_obs[0, 0] = 1.0  # target flip on observable 0

    outputs = model(syndromes)
    loss = model.compute_loss(outputs, true_obs, syndromes, beta_obs=0.5)

    assert torch.isfinite(loss)
    assert loss.item() > 0.0

    loss.backward()
    assert model.orbit_alpha.grad is not None
    assert torch.all(torch.isfinite(model.orbit_alpha.grad))
    assert model.orbit_gamma.grad is not None
    assert torch.all(torch.isfinite(model.orbit_gamma.grad))
