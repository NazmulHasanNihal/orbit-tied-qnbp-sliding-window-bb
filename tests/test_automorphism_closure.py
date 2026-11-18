"""Unit tests for Proposition 1 & 2 (automorphism group action, orbit closure, and probability invariance)."""

import json
from pathlib import Path
import pytest

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.decoder.orbits import DemOrbitManager


def test_orbit_partition_count_and_sizes():
    """Verify that DEM faults on [[72,12,6]] partition into exactly 203 orbits of size 36."""
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=3, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    mgr = DemOrbitManager(code=code, num_rounds=3, dem=dem)

    assert len(mgr.parsed_errors) == 7308, f"Expected 7308 errors, got {len(mgr.parsed_errors)}"
    assert mgr.num_fault_orbits == 203, f"Expected 203 orbits, got {mgr.num_fault_orbits}"

    # Orbit size verification
    orbit_counts = {}
    for o in mgr.fault_orbits:
        orbit_counts[int(o)] = orbit_counts.get(int(o), 0) + 1

    assert len(orbit_counts) == 203
    for o_id, count in orbit_counts.items():
        assert count == 36, f"Orbit {o_id} has size {count}, expected 36"


def test_group_action_automorphisms():
    """Verify that all 36 torus translations are exact DEM graph automorphisms."""
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=3, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    mgr = DemOrbitManager(code=code, num_rounds=3, dem=dem)

    stats = mgr.verify_automorphisms()
    assert stats["shifts_tested"] == 36
    assert stats["valid_shifts"] == 36
    assert stats["compression_ratio"] == 36.0


def test_automorphism_closure_artifact():
    """Verify that results/automorphism_closure_verification.json exists and passes."""
    artifact_path = Path("results/automorphism_closure_verification.json")
    assert artifact_path.exists(), "results/automorphism_closure_verification.json must exist"

    with open(artifact_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["verification_status"] == "PASS"
    assert data["orbit_statistics"]["all_orbits_size_36"] is True
    assert data["group_action_verification"]["shifts_fully_verified"] == 36
    assert data["group_action_verification"]["closure_violations"] == 0
    assert data["group_action_verification"]["probability_invariance_violations"] == 0
