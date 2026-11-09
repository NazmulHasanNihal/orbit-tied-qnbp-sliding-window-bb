"""Stim Detector Error Model to PyTorch and PyTorch Geometric Graph Bridge.

Converts a Stim DEM into a typed bipartite graph tensor structure (check nodes
and variable fault nodes) with priors, observable incidence, and orbit maps.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import torch
from numpy.typing import NDArray
import stim

try:
    from torch_geometric.data import HeteroData  # type: ignore
    HAS_PYG = True
except ImportError:
    HAS_PYG = False

from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.decoder.orbits import DemOrbitManager


class DemGraph:
    """Represents a DEM as a bipartite graph for neural belief propagation.

    Attributes:
        num_detectors: Total check nodes (C).
        num_faults: Total variable nodes (V).
        num_observables: Total logical observables (K).
        num_edges: Total bipartite edges (E).
        priors: Tensor of shape (V,) containing float32 initial LLRs.
        prior_probs: Tensor of shape (V,) containing float32 fault probabilities.
        fault_orbits: Tensor of shape (V,) containing int64 symmetry orbit IDs.
        fault_classes: Tensor of shape (V,) containing int64 window boundary classes.
        obs_matrix: Tensor of shape (K, V) containing binary observable incidence.
        check_nodes_per_edge: Tensor of shape (E,) check node index for each edge.
        fault_nodes_per_edge: Tensor of shape (E,) fault node index for each edge.
        check_to_edges: List of edge index lists for each check node.
        fault_to_edges: List of edge index lists for each fault node.
    """

    def __init__(
        self,
        num_detectors: int,
        num_faults: int,
        num_observables: int,
        priors: torch.Tensor,
        prior_probs: torch.Tensor,
        fault_orbits: torch.Tensor,
        fault_classes: torch.Tensor,
        obs_matrix: torch.Tensor,
        check_nodes_per_edge: torch.Tensor,
        fault_nodes_per_edge: torch.Tensor,
        check_to_edges: List[List[int]],
        fault_to_edges: List[List[int]],
    ) -> None:
        self.num_detectors = num_detectors
        self.num_faults = num_faults
        self.num_observables = num_observables
        self.num_edges = len(check_nodes_per_edge)
        self.priors = priors
        self.prior_probs = prior_probs
        self.fault_orbits = fault_orbits
        self.fault_classes = fault_classes
        self.obs_matrix = obs_matrix
        self.check_nodes_per_edge = check_nodes_per_edge
        self.fault_nodes_per_edge = fault_nodes_per_edge
        self.check_to_edges = check_to_edges
        self.fault_to_edges = fault_to_edges

    @classmethod
    def from_dem(
        cls,
        code: BivariateBicycleCode,
        num_rounds: int,
        dem: stim.DetectorErrorModel,
        window_start_round: int = 0,
        window_end_round: Optional[int] = None,
    ) -> "DemGraph":
        """Builds a DemGraph from a Stim DetectorErrorModel and Code instance."""
        if window_end_round is None:
            window_end_round = num_rounds - 1

        orbit_mgr = DemOrbitManager(code=code, num_rounds=num_rounds, dem=dem)
        num_detectors = dem.num_detectors
        num_faults = len(orbit_mgr.parsed_errors)
        num_observables = dem.num_observables

        priors = np.zeros(num_faults, dtype=np.float32)
        prior_probs = np.zeros(num_faults, dtype=np.float32)
        obs_matrix = np.zeros((num_observables, num_faults), dtype=np.float32)

        check_edges_list: List[int] = []
        fault_edges_list: List[int] = []
        check_to_edges: List[List[int]] = [[] for _ in range(num_detectors)]
        fault_to_edges: List[List[int]] = [[] for _ in range(num_faults)]

        edge_counter = 0
        for f_idx, (p, dets, obs) in enumerate(orbit_mgr.parsed_errors):
            p_clamped = min(max(p, 1e-15), 1.0 - 1e-15)
            prior_probs[f_idx] = p
            priors[f_idx] = np.log((1.0 - p_clamped) / p_clamped)

            for o_idx in obs:
                obs_matrix[o_idx, f_idx] = 1.0

            for d_idx in dets:
                check_edges_list.append(d_idx)
                fault_edges_list.append(f_idx)
                check_to_edges[d_idx].append(edge_counter)
                fault_to_edges[f_idx].append(edge_counter)
                edge_counter += 1

        boundary_classes = orbit_mgr.classify_window_boundary(
            window_start_round=window_start_round,
            window_end_round=window_end_round,
        )

        return cls(
            num_detectors=num_detectors,
            num_faults=num_faults,
            num_observables=num_observables,
            priors=torch.from_numpy(priors),
            prior_probs=torch.from_numpy(prior_probs),
            fault_orbits=torch.from_numpy(orbit_mgr.fault_orbits),
            fault_classes=torch.from_numpy(boundary_classes.astype(np.int64)),
            obs_matrix=torch.from_numpy(obs_matrix),
            check_nodes_per_edge=torch.tensor(check_edges_list, dtype=torch.int64),
            fault_nodes_per_edge=torch.tensor(fault_edges_list, dtype=torch.int64),
            check_to_edges=check_to_edges,
            fault_to_edges=fault_to_edges,
        )

    def to_hetero_data(self) -> Any:
        """Converts graph to a PyTorch Geometric HeteroData instance if PyG is installed."""
        if not HAS_PYG:
            raise ImportError("PyTorch Geometric is not installed.")

        data = HeteroData()
        data["detector"].num_nodes = self.num_detectors
        data["fault"].num_nodes = self.num_faults
        data["fault"].priors = self.priors
        data["fault"].orbit_id = self.fault_orbits
        data["fault"].class_id = self.fault_classes

        # Directed bipartite edges
        edge_index_cf = torch.stack([self.check_nodes_per_edge, self.fault_nodes_per_edge], dim=0)
        edge_index_fc = torch.stack([self.fault_nodes_per_edge, self.check_nodes_per_edge], dim=0)

        data["detector", "checks", "fault"].edge_index = edge_index_cf
        data["fault", "symptom_of", "detector"].edge_index = edge_index_fc

        return data

