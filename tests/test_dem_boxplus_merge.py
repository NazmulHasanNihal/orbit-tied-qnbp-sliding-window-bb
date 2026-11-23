"""Unit tests for exact Bernoulli XOR / boxplus collinear DEM fault merging."""

import math
import numpy as np
import pytest

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.orbits import DemOrbitManager, boxplus_probabilities


def test_boxplus_formula_properties():
    """Verify Bernoulli XOR / boxplus algebraic properties and comparison against naive linear LLR sum."""
    p1 = 0.003
    p2 = 0.003

    # Exact Bernoulli XOR: p_v = 0.5 * (1 - (1 - 2p1)(1 - 2p2))
    p_exact = boxplus_probabilities([p1, p2])
    expected_p = 0.5 * (1.0 - (1.0 - 2.0 * p1) * (1.0 - 2.0 * p2))
    assert math.isclose(p_exact, expected_p, rel_tol=1e-7)

    # In F_2, two flips cancel: p_v < p1 + p2
    assert p_exact < (p1 + p2)

    # Boxplus in LLR domain: L_1 \boxplus L_2 = 2 * artanh(tanh(L1/2) * tanh(L2/2))
    L1 = math.log((1.0 - p1) / p1)
    L2 = math.log((1.0 - p2) / p2)
    L_boxplus = 2.0 * math.atanh(math.tanh(L1 / 2.0) * math.tanh(L2 / 2.0))
    p_from_L = 1.0 / (1.0 + math.exp(L_boxplus))
    assert math.isclose(p_from_L, p_exact, rel_tol=1e-6)

    # Naive linear sum of LLRs: L_linear = L1 + L2
    # This assumes independent non-canceling events, which erroneously pushes LLR too high (p too low!)
    L_linear = L1 + L2
    p_linear = 1.0 / (1.0 + math.exp(L_linear))
    assert p_linear < p_exact * 0.01, "Linear LLR sum severely underestimates error probability"


def test_dem_boxplus_merging_graph_construction():
    """Verify that DemGraph constructed with merge_collinear=True produces valid priors without NaN or inf."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 2
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)

    graph_unmerged = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem, merge_collinear=False)
    graph_merged = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem, merge_collinear=True)

    # Merging collinear faults should preserve or reduce total fault nodes
    assert graph_merged.num_faults <= graph_unmerged.num_faults
    assert graph_merged.num_detectors == graph_unmerged.num_detectors
    assert graph_merged.num_observables == graph_unmerged.num_observables

    # All merged priors should be finite and positive (for p < 0.5)
    priors_np = graph_merged.priors.numpy()
    assert np.all(np.isfinite(priors_np))
    assert np.all(priors_np > 0.0)
