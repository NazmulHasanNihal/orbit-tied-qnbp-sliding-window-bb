"""Unit tests and empirical size verification for Bivariate Bicycle codes."""

import numpy as np
import pytest
import stim
from src.circuits.bivariate_bicycle import BivariateBicycleCode


def test_code_72_12_6_properties():
    """Verify parameters and CSS commutativity of [[72, 12, 6]]."""
    code = BivariateBicycleCode.code_72_12_6()
    assert code.l == 6
    assert code.m == 6
    assert code.group_order == 36
    assert code.num_data_qubits == 72
    assert code.num_logicals == 12
    assert code.hx.shape == (36, 72)
    assert code.hz.shape == (36, 72)
    assert np.all((code.hx @ code.hz.T) % 2 == 0)


def test_code_144_12_12_properties():
    """Verify parameters and CSS commutativity of [[144, 12, 12]]."""
    code = BivariateBicycleCode.code_144_12_12()
    assert code.l == 12
    assert code.m == 6
    assert code.group_order == 72
    assert code.num_data_qubits == 144
    assert code.num_logicals == 12
    assert code.hx.shape == (72, 144)
    assert code.hz.shape == (72, 144)
    assert np.all((code.hx @ code.hz.T) % 2 == 0)


def test_code_72_noiseless_circuit():
    """Verify that noiseless simulation produces deterministic zero syndrome and observables."""
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=4, error_rate=0.0)
    sampler = circuit.compile_detector_sampler()
    dets, obs = sampler.sample(shots=50, separate_observables=True)

    assert not np.any(dets), "Noiseless circuit triggered unexpected detector failures!"
    assert not np.any(obs), "Noiseless circuit flipped logical observables!"


def test_code_144_gross_code_size_check():
    """Verify exact DEM detector and fault mechanism counts matching the literature."""
    code = BivariateBicycleCode.code_144_12_12()
    circuit = code.build_stim_circuit(rounds=12, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)

    # Literature ground truth: 1728 detectors, 67,752 error mechanisms
    assert dem.num_detectors == 1728
    assert dem.num_observables == 12
    assert dem.num_errors == 67752


def test_code_72_biased_noise_generation():
    """Verify that asymmetric Pauli noise with bias eta correctly compiles to DEM."""
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=3, error_rate=0.003, bias=10.0)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)

    assert dem.num_detectors == 216
    assert dem.num_observables == 12
    assert dem.num_errors > 0


