"""Unit tests for Lemma 1 (6-bit dyadic dynamic range and clipping verification)."""

import json
from pathlib import Path
import numpy as np
import pytest

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph


def test_lemma1_prior_dynamic_range():
    """Verify that dyadic scaled priors achieve 100% containment in [-7.75, +7.75]."""
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=3, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    graph = DemGraph.from_dem(code=code, num_rounds=3, dem=dem)

    bit_width = 6
    delta = 0.25
    q_max_int = (1 << (bit_width - 1)) - 1  # 31
    v_max = float(q_max_int * delta)        # 7.75
    v_min = float(-v_max)                   # -7.75

    raw_priors = graph.priors.cpu().numpy()
    assert np.max(raw_priors) > v_max, "Raw priors under depth-7 depolarizing noise should exceed 7.75"

    # Under dyadic scaling kappa = 0.75 = 1 - 2^-2
    kappa = 0.75
    scaled_priors = raw_priors * kappa
    clipped_count = int(np.sum((scaled_priors < v_min) | (scaled_priors > v_max)))
    assert clipped_count == 0, f"Expected 0 clipped priors under kappa=0.75, got {clipped_count}"

    headroom = v_max - float(np.max(scaled_priors))
    assert headroom >= 0.5, f"Expected headroom >= 0.5, got {headroom:.4f}"


def test_lemma1_bit_width_sensitivity():
    """Verify that B <= 5 causes severe clipping of prior LLRs."""
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=3, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    graph = DemGraph.from_dem(code=code, num_rounds=3, dem=dem)

    scaled_priors = graph.priors.cpu().numpy() * 0.75
    delta = 0.25

    # B = 5 bits: qmax = 15 -> v_max = 3.75
    v_max_5bit = 15 * delta
    clipped_5bit = np.mean(scaled_priors > v_max_5bit)
    assert clipped_5bit > 0.50, f"Expected >50% clipping for 5 bits, got {clipped_5bit*100:.2f}%"

    # B = 4 bits: qmax = 7 -> v_max = 1.75
    v_max_4bit = 7 * delta
    clipped_4bit = np.mean(scaled_priors > v_max_4bit)
    assert clipped_4bit > 0.99, f"Expected >99% clipping for 4 bits, got {clipped_4bit*100:.2f}%"


def test_quant_clipping_empirical_artifact():
    """Verify that the empirical verification artifact exists and passes."""
    artifact_path = Path("results/quant_clipping_empirical.json")
    assert artifact_path.exists(), "results/quant_clipping_empirical.json must exist"

    with open(artifact_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["verification_status"] == "PASS"
    assert data["dyadic_scaled_priors_lemma1"]["clipped_faults_count"] == 0
    assert data["dyadic_scaled_priors_lemma1"]["coverage_pct"] == 100.0
    assert data["monte_carlo_10k_evaluation"]["empirical_clipping_frequency_pct"] < 0.5
