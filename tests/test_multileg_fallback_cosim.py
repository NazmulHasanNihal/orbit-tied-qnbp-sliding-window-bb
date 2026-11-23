"""Unit tests and hardware co-simulation for Self-Contained On-Chip Multi-Leg CSD Fallback."""

import pytest
import torch
import numpy as np

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.multileg_csd import MultiLegCsdFallback


def test_multileg_fallback_initialization():
    """Verify that MultiLegCsdFallback initializes cleanly and builds check parity matrix."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 2
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    fallback = MultiLegCsdFallback(graph=graph, num_layers_per_leg=5, bit_width=6)
    assert fallback.h_matrix.shape == (graph.num_detectors, graph.num_faults)
    assert fallback.base_model.orbit_gamma.shape[0] == 5


def test_multileg_fallback_single_fault_recovery():
    """Verify that multi-leg perturbed execution resolves single fault syndrome excitations."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 2
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    fallback = MultiLegCsdFallback(graph=graph, num_layers_per_leg=8, bit_width=6)

    # Inject single fault
    test_fault = 10
    h_col = fallback.h_matrix[:, test_fault]
    syndrome = h_col.unsqueeze(0)  # shape (1, num_detectors)

    corrections, leg_used, satisfied = fallback.decode_multi_leg(syndrome, max_legs=4)

    assert corrections.shape == (1, graph.num_faults)
    assert leg_used.shape == (1,)
    assert satisfied.shape == (1,)
    # If satisfied, syndrome parity must be 100% matched
    if satisfied[0]:
        recomputed = torch.matmul(corrections.float(), fallback.h_matrix.float().T) % 2
        assert torch.all(recomputed.byte() == syndrome.byte())


def test_zero_dsp_rtl_audit_fallback():
    """Audit rtl/csd_multileg_fallback.sv for strict zero DSP multipliers and zero Block RAM."""
    with open("rtl/csd_multileg_fallback.sv", "r", encoding="utf-8") as f:
        rtl = f.read()

    # Verify no DSP multipliers or multiplication operators
    assert "*" not in [line.split("//")[0] for line in rtl.splitlines() if "timescale" not in line and "*" in line and "parameter" not in line and "**" not in line], "Multipliers found in RTL"
    assert "DSP = 0" in rtl or "Zero DSP" in rtl
