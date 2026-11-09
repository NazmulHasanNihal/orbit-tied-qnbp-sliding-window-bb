"""Unit tests for Stim DEM to PyTorch/PyG bipartite graph bridge."""

import numpy as np
import pytest
import torch
from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph, HAS_PYG


def test_dem_graph_construction():
    """Verify that node and edge counts strictly match the DEM."""
    code = BivariateBicycleCode.code_72_12_6()
    rounds = 3
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)

    graph = DemGraph.from_dem(code=code, num_rounds=rounds, dem=dem)

    # Core assertion from Research Plan Section 8:
    assert graph.num_detectors == dem.num_detectors
    assert graph.num_observables == dem.num_observables
    assert graph.priors.shape[0] == graph.num_faults
    assert graph.obs_matrix.shape == (dem.num_observables, graph.num_faults)
    assert len(graph.check_nodes_per_edge) == graph.num_edges

    # Prior numerical accuracy check
    for i in range(min(100, graph.num_faults)):
        p = graph.prior_probs[i].item()
        expected_llr = np.log((1.0 - p) / p)
        assert graph.priors[i].item() == pytest.approx(expected_llr, rel=1e-5)


@pytest.mark.skipif(not HAS_PYG, reason="PyTorch Geometric not installed")
def test_to_hetero_data():
    """Verify conversion to PyG HeteroData structure."""
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=2, error_rate=0.003)
    dem = circuit.detector_error_model(decompose_errors=False)

    graph = DemGraph.from_dem(code=code, num_rounds=2, dem=dem)
    pyg_data = graph.to_hetero_data()

    assert pyg_data["detector"].num_nodes == graph.num_detectors
    assert pyg_data["fault"].num_nodes == graph.num_faults
    assert pyg_data["detector", "checks", "fault"].edge_index.shape[1] == graph.num_edges

