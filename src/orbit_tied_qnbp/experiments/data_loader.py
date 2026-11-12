"""Deterministic dataset sampling and caching for paired decoder comparisons.

Generates paired Stim detector syndromes and true logical observable flips
under pinned seeds for reproducible train, validation, and test splits.
"""

from typing import Tuple, Dict, Any, Optional
import os
import numpy as np
import stim

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode


class QecDataLoader:
    """Manages deterministic dataset generation and caching for BB codes."""

    def __init__(
        self,
        code: BivariateBicycleCode,
        num_rounds: int = 3,
        cache_dir: str = "results/data_cache",
    ) -> None:
        self.code = code
        self.num_rounds = num_rounds
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_dataset(
        self,
        error_rate: float,
        num_shots: int,
        seed: int = 42,
        split: str = "test",
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Loads cached shots or samples new shots deterministically.

        Args:
            error_rate: Physical error rate p.
            num_shots: Number of shots to sample.
            seed: Pinned random seed.
            split: 'train', 'val', or 'test'.

        Returns:
            Tuple of (syndromes, true_observables).
        """
        code_name = f"bb_{self.code.l}_{self.code.m}"
        filename = (
            f"{code_name}_r{self.num_rounds}_p{error_rate:.4f}_"
            f"s{seed}_{split}_n{num_shots}.npz"
        )
        filepath = os.path.join(self.cache_dir, filename)

        if os.path.exists(filepath):
            data = np.load(filepath)
            return data["syndromes"], data["true_observables"]

        # Sample using Stim
        circuit = self.code.build_stim_circuit(
            rounds=self.num_rounds, error_rate=error_rate
        )
        sampler = circuit.compile_detector_sampler(seed=seed)
        syndromes, observables = sampler.sample(
            shots=num_shots, separate_observables=True
        )

        np.savez_compressed(
            filepath,
            syndromes=syndromes.astype(np.uint8),
            true_observables=observables.astype(np.uint8),
        )

        return syndromes.astype(np.uint8), observables.astype(np.uint8)
