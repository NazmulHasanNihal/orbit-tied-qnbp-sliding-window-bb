"""Unit tests for StreamingSlidingWindowDecoder with residual propagation."""

import numpy as np
import pytest
from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph
from src.decoder.streaming_window_decoder import StreamingSlidingWindowDecoder


def test_noiseless_streaming_window():
    """Verify that a noiseless stream decodes with 0 iterations and 0 observable flips."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 4
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.0)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    sw_dec = StreamingSlidingWindowDecoder(
        code=code,
        num_rounds=rounds,
        dem_graph=graph,
        window_width=3,
        commit_stride=1,
    )

    zero_syn = np.zeros(graph.num_detectors, dtype=np.uint8)
    converged, pred_obs, iters = sw_dec.decode_stream(zero_syn, use_integer_model=True)

    assert converged, "Noiseless stream failed to converge!"
    assert np.all(pred_obs == 0), "Noiseless stream generated false logical flips!"


def test_streaming_window_single_fault_correction():
    """Verify that a single fault injected in round 0 is committed and residual cleared."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 4
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)
    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    sw_dec = StreamingSlidingWindowDecoder(
        code=code,
        num_rounds=rounds,
        dem_graph=graph,
        window_width=3,
        commit_stride=1,
    )

    # Pick a fault committed in round 0
    f_target = None
    for f in range(graph.num_faults):
        if sw_dec.fault_commit_round[f] == 0 and len(graph.fault_to_edges[f]) >= 2:
            f_target = f
            break
    assert f_target is not None

    # Construct syndrome for this single fault
    syn = np.zeros(graph.num_detectors, dtype=np.uint8)
    for e in graph.fault_to_edges[f_target]:
        c = graph.check_nodes_per_edge[e].item()
        syn[c] ^= 1

    converged, pred_obs, iters = sw_dec.decode_stream(syn, use_integer_model=True)
    expected_obs = (graph.obs_matrix[:, f_target].cpu().numpy().astype(np.uint8)) % 2

    assert np.all(pred_obs == expected_obs), "Streaming decoder failed to match expected observable!"
