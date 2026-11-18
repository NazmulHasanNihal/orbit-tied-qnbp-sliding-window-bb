"""Standardized Experimental Result Schema.

Ensures strict schema compliance for all experimental data in results/:
- code: Quantum code identifier (e.g., '[[72,12,6]]' or '[[144,12,12]]')
- rounds: Syndrome extraction rounds in window (e.g., 3)
- p: Physical error rate (e.g., 0.003)
- bias: Channel bias ratio eta = p_Z / p_X (float or None)
- decoder: Canonical decoder name
- config: Dictionary of architectural/hyperparameter settings
- seed: Random seed for deterministic replication
- n_shots: Total test shots evaluated
- n_errors: Total observed logical frame error events
- n_accepted: Total windows accepted by fast-path gating (or None)
- n_fallback: Total windows routed to fallback (or None)
- iterations_histogram: List of iteration counts or dictionary histogram
- wall_time: Execution duration in seconds
- git_commit: Current repository git commit SHA
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional, List, Union
import subprocess
import os


def get_git_commit() -> str:
    """Retrieves current git commit hash, or 'unknown'."""
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode("ascii").strip()
        return commit
    except Exception:
        return "unknown"


@dataclass
class StandardResultRecord:
    code: str
    rounds: int
    p: float
    bias: Optional[float]
    decoder: str
    config: Dict[str, Any]
    seed: int
    n_shots: int
    n_errors: int
    n_accepted: Optional[int] = None
    n_fallback: Optional[int] = None
    iterations_histogram: Dict[str, int] = field(default_factory=dict)
    wall_time: float = 0.0
    git_commit: str = field(default_factory=get_git_commit)

    def validate(self) -> None:
        """Validates that numerical counts and bounds are consistent."""
        if self.n_shots <= 0:
            raise ValueError(f"n_shots must be positive, got {self.n_shots}")
        if self.n_errors < 0 or self.n_errors > self.n_shots:
            raise ValueError(f"n_errors must be in [0, {self.n_shots}], got {self.n_errors}")
        if self.n_accepted is not None and self.n_fallback is not None:
            if self.n_accepted + self.n_fallback != self.n_shots:
                raise ValueError(
                    f"n_accepted ({self.n_accepted}) + n_fallback ({self.n_fallback}) "
                    f"!= n_shots ({self.n_shots})"
                )

    def to_dict(self) -> Dict[str, Any]:
        self.validate()
        return asdict(self)
