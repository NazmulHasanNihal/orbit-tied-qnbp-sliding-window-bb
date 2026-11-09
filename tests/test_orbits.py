"""Unit tests for DEM automorphism extraction, invariance verification, and window boundary classes."""

import numpy as np
import pytest
from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.decoder.orbits import DemOrbitManager


def test_orbits_72_12_6():
    """Verify orbit partitioning and 100% automorphism validity on [[72, 12, 6]]."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 3
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)

    orbit_mgr = DemOrbitManager(code=code, num_rounds=rounds, dem=dem)

    # Run formal verifier
    report = orbit_mgr.verify_automorphisms()
    assert report["shifts_tested"] == 36
    assert report["valid_shifts"] == 36
    assert report["compression_ratio"] == pytest.approx(36.0, rel=1e-2)

    # Verify no unassigned orbit (-1)
    assert np.all(orbit_mgr.fault_orbits >= 0)
    assert orbit_mgr.num_fault_orbits == len(set(orbit_mgr.fault_orbits))


def test_window_boundary_classification():
    """Verify window boundary classes (open_left=0, interior=1, open_right=2)."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 4
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)

    orbit_mgr = DemOrbitManager(code=code, num_rounds=rounds, dem=dem)
    classes = orbit_mgr.classify_window_boundary(window_start_round=0, window_end_round=3)

    assert set(classes).issubset({0, 1, 2})
    # Must have errors in all 3 classes
    assert np.any(classes == 0), "No open_left faults detected!"
    assert np.any(classes == 1), "No interior faults detected!"
    assert np.any(classes == 2), "No open_right faults detected!"

