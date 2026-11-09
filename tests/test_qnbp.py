"""Unit tests for Orbit-Tied Quantized Neural BP (QNBP) module."""

import numpy as np
import pytest
import torch
from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph
from src.decoder.qnbp import OrbitTiedQNBP
from src.decoder.quantization import PowerOfTwoQuantizer, CanonicalSignedDigit


def test_quantizer_powers_of_two():
    """Verify PowerOfTwoQuantizer bounds and straight-through gradient."""
    quant = PowerOfTwoQuantizer(bit_width=4, initial_shift=2.0)
    # 4-bit signed symmetric bounds: -(2^3 - 1) = -7, +(2^3 - 1) = +7
    assert quant.qmin == -7
    assert quant.qmax == 7

    x = torch.tensor([-10.0, -1.0, 0.0, 1.5, 8.0], requires_grad=True)
    out = quant(x)
    assert out.shape == x.shape

    loss = out.sum()
    loss.backward()
    assert x.grad is not None
    assert quant.b_tilde.grad is not None


def test_csd_projection():
    """Verify CanonicalSignedDigit table projection to shift-and-add."""
    csd = CanonicalSignedDigit(max_shift=5, num_terms=2)
    # 0.75 = 1.0 - 0.25 = 2^0 - 2^(-2) in canonical form (or 2^(-1) + 2^(-2))
    val, terms = csd.project(0.75)
    assert val == pytest.approx(0.75)
    assert len(terms) == 2
    # Verify shift-and-add sum reconstructs 0.75 exactly
    reconstructed = sum(s * (2.0 ** (-shift)) for s, shift in terms)
    assert reconstructed == pytest.approx(0.75)
    assert terms == [(1, 0), (-1, 2)]


def test_qnbp_forward_and_backward():
    """Verify QNBP forward pass, parameter tying count, and end-to-end backprop."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 2
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    num_layers = 3
    model = OrbitTiedQNBP(graph=graph, num_layers=num_layers, bit_width=4, quantize=True)

    # Parameter count verification: orbit tying should compress parameter count ~36x
    num_orbits = model.orbit_alpha.shape[1]
    assert num_orbits <= graph.num_faults // 30
    assert model.orbit_alpha.shape == (num_layers, num_orbits)

    # Forward pass with batch of 2 syndromes
    syndromes = torch.zeros((2, graph.num_detectors), dtype=torch.uint8)
    syndromes[0, 5] = 1
    syndromes[1, 10] = 1

    outputs = model(syndromes)
    assert len(outputs) == num_layers
    posteriors, hard_corr = outputs[-1]
    assert posteriors.shape == (2, graph.num_faults)
    assert hard_corr.shape == (2, graph.num_faults)

    # Compute loss and check gradients
    true_obs = torch.zeros((2, graph.num_observables), dtype=torch.float32)
    loss = model.compute_loss(outputs, true_obs, syndromes)
    assert torch.isfinite(loss)
    assert loss.item() > 0.0

    loss.backward()
    assert model.orbit_alpha.grad is not None
    assert model.orbit_gamma.grad is not None
    assert model.class_offsets.grad is not None
    assert torch.all(torch.isfinite(model.orbit_alpha.grad))
