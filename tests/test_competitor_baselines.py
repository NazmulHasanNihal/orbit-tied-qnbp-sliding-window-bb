"""Unit tests for Competitor Baselines.

Tests:
1. MemBpDecoder execution and convergence.
2. BpLsdBaselineDecoder execution.
3. BpOsdBaselineDecoder execution.
4. AutDecBaselineDecoder execution across torus shifts.
5. GdgSlidingWindowBaseline execution.
"""

import numpy as np
import pytest
from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.orbits import DemOrbitManager
from orbit_tied_qnbp.decoder.competitor_baselines import (
    MemBpDecoder,
    BpLsdBaselineDecoder,
    BpOsdBaselineDecoder,
    AutDecBaselineDecoder,
    GdgSlidingWindowBaseline,
)


@pytest.fixture(scope="module")
def bb72_setup():
    """Sets up DemGraph and DemOrbitManager for [[72, 12, 6]] code."""
    code = BivariateBicycleCode.code_72_12_6()
    num_rounds = 2
    circuit = code.build_stim_circuit(rounds=num_rounds, error_rate=0.003)
    dem = circuit.detector_error_model(approximate_disjoint_errors=True)
    graph = DemGraph.from_dem(code=code, num_rounds=num_rounds, dem=dem)
    orbit_mgr = DemOrbitManager(code=code, num_rounds=num_rounds, dem=dem)
    return code, graph, orbit_mgr


def test_mem_bp_decoder(bb72_setup):
    """Verifies MemBpDecoder runs and returns DecodeResult with valid shapes."""
    # Arrange
    _, graph, _ = bb72_setup
    decoder = MemBpDecoder(graph=graph, max_iter=10, alpha=0.75, gamma=0.3)
    syndrome = np.zeros(graph.num_detectors, dtype=np.uint8)

    # Act
    res = decoder.decode(syndrome)

    # Assert
    assert res.converged is True
    assert res.iterations == 1
    assert len(res.corrections) == graph.num_faults
    assert len(res.predicted_observables) == graph.num_observables


def test_bp_lsd_decoder(bb72_setup):
    """Verifies BpLsdBaselineDecoder executes and handles noiseless syndrome."""
    # Arrange
    _, graph, _ = bb72_setup
    decoder = BpLsdBaselineDecoder(graph=graph, max_iter=10, ms_scaling_factor=0.75, lsd_order=0)
    syndrome = np.zeros(graph.num_detectors, dtype=np.uint8)

    # Act
    res = decoder.decode(syndrome)

    # Assert
    assert res.converged is True
    assert len(res.corrections) == graph.num_faults
    assert len(res.predicted_observables) == graph.num_observables


def test_bp_osd_decoder(bb72_setup):
    """Verifies BpOsdBaselineDecoder executes and decodes."""
    # Arrange
    _, graph, _ = bb72_setup
    decoder = BpOsdBaselineDecoder(graph=graph, max_iter=10, ms_scaling_factor=0.75, osd_order=0)
    syndrome = np.zeros(graph.num_detectors, dtype=np.uint8)

    # Act
    res = decoder.decode(syndrome)

    # Assert
    assert res.converged is True
    assert len(res.corrections) == graph.num_faults
    assert len(res.predicted_observables) == graph.num_observables


def test_aut_dec_decoder(bb72_setup):
    """Verifies AutDecBaselineDecoder executes across torus permutations."""
    # Arrange
    _, graph, orbit_mgr = bb72_setup
    decoder = AutDecBaselineDecoder(
        graph=graph,
        orbit_mgr=orbit_mgr,
        max_iter=10,
        alpha=0.75,
        max_automorphisms=4,
    )
    syndrome = np.zeros(graph.num_detectors, dtype=np.uint8)

    # Act
    res = decoder.decode(syndrome)

    # Assert
    assert res.converged is True
    assert len(res.corrections) == graph.num_faults
    assert len(res.predicted_observables) == graph.num_observables


def test_gdg_sliding_window_baseline(bb72_setup):
    """Verifies GdgSlidingWindowBaseline decodes cleanly."""
    # Arrange
    _, graph, _ = bb72_setup
    decoder = GdgSlidingWindowBaseline(graph=graph, window_size=3, commit_size=1, max_iter=10)
    syndrome = np.zeros(graph.num_detectors, dtype=np.uint8)

    # Act
    res = decoder.decode(syndrome)

    # Assert
    assert res.converged is True
    assert len(res.corrections) == graph.num_faults
