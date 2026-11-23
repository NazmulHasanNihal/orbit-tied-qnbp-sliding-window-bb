"""Unit tests for Proposition 4: Cross-Distance Orbit Isomorphism between BB72 and BB144."""

import pytest
import numpy as np
from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.decoder.orbits import DemOrbitManager


def test_cross_distance_orbit_count_isomorphism():
    """Verify Proposition 4: quotient space-time DEM G_DEM / (Z_l x Z_m) yields exactly 203 orbits for both codes."""
    code72 = BivariateBicycleCode.code_72_12_6()
    circ72 = code72.build_stim_circuit(rounds=3, error_rate=0.003)
    dem72 = circ72.detector_error_model(decompose_errors=False)
    mgr72 = DemOrbitManager(code=code72, num_rounds=3, dem=dem72)

    code144 = BivariateBicycleCode.code_144_12_12()
    circ144 = code144.build_stim_circuit(rounds=3, error_rate=0.003)
    dem144 = circ144.detector_error_model(decompose_errors=False)
    mgr144 = DemOrbitManager(code=code144, num_rounds=3, dem=dem144)

    # In both codes, the depth-7 syndrome circuit over W=3 sliding window yields exactly 203 orbits
    assert mgr72.num_fault_orbits == 203, f"Expected 203 orbits for [[72,12,6]], got {mgr72.num_fault_orbits}"
    assert mgr144.num_fault_orbits == 203, f"Expected 203 orbits for [[144,12,12]], got {mgr144.num_fault_orbits}"

    # Group orders
    assert mgr72.group_order == 36
    assert mgr144.group_order == 72

    # Mechanism count matches group order * 203 orbits
    assert len(mgr72.parsed_errors) == 7308
    assert len(mgr144.parsed_errors) == 14616
    assert 7308 // 36 == 203
    assert 14616 // 72 == 203
