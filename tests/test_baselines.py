"""Unit tests for classical Min-Sum BP baselines A0 and A1."""

import numpy as np
import pytest
from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph
from src.decoder.baselines import MinSumDecoder


def test_noiseless_decoding():
    """Verify that decoding a zero syndrome converges immediately in 1 iteration."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 2
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    decoder = MinSumDecoder(graph=graph, max_iter=10, alpha=1.0)
    zero_syndrome = np.zeros(graph.num_detectors, dtype=np.uint8)

    res = decoder.decode(zero_syndrome)
    assert res.converged, "Zero syndrome failed to converge!"
    assert res.iterations == 1
    assert np.all(res.corrections == 0)
    assert np.all(res.predicted_observables == 0)


def test_single_fault_correction():
    """Verify that Min-Sum can correct an injected single-fault error symptom."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 2
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    # Pick a fault node that has at least 1 symptom
    fault_idx = None
    for f in range(graph.num_faults):
        if len(graph.fault_to_edges[f]) >= 2:
            fault_idx = f
            break
    assert fault_idx is not None

    # Construct syndrome corresponding to this fault
    syndrome = np.zeros(graph.num_detectors, dtype=np.uint8)
    for e_k in graph.fault_to_edges[fault_idx]:
        c = graph.check_nodes_per_edge[e_k].item()
        syndrome[c] ^= 1

    # Decode with normalized min-sum (A1)
    decoder_a1 = MinSumDecoder(graph=graph, max_iter=20, alpha=0.75)
    res = decoder_a1.decode(syndrome)

    assert res.converged, "Normalized Min-Sum failed to converge on single fault!"
    assert res.corrections[fault_idx] == 1, "Failed to identify the injected fault!"

