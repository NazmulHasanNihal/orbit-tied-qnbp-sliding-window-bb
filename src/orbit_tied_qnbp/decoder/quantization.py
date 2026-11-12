"""Power-of-Two Quantization and Canonical Signed-Digit (CSD) Module.

Implements Straight-Through Estimator (STE) power-of-two quantization and
multiplier-free canonical signed-digit shift-and-add arithmetic for QNBP.
"""

from typing import Tuple, List, Optional
import numpy as np
from numpy.typing import NDArray
import torch
import torch.nn as nn
from torch.autograd import Function


class SteRound(Function):
    """Straight-Through Estimator (STE) for round() operator."""

    @staticmethod
    def forward(ctx, x: torch.Tensor) -> torch.Tensor:
        return torch.round(x)

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> torch.Tensor:
        # Straight-through gradient: derivative treated as identity
        return grad_output


class SteClamp(Function):
    """Straight-Through Estimator (STE) for clamp() operator."""

    @staticmethod
    def forward(ctx, x: torch.Tensor, min_val: float, max_val: float) -> torch.Tensor:
        ctx.save_for_backward(x)
        ctx.min_val = min_val
        ctx.max_val = max_val
        return torch.clamp(x, min_val, max_val)

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> Tuple[torch.Tensor, None, None]:
        # Straight-through gradient: identity pass-through across bounds to enable weight recovery
        return grad_output, None, None


class PowerOfTwoQuantizer(nn.Module):
    """Learned step-size power-of-two quantizer Delta = 2^(-round(b_tilde)).

    Multiplication by Delta is equivalent to an arithmetic right shift by b bits,
    enabling multiplier-free integer inference.

    Attributes:
        bit_width: Integer bit-width k (e.g. 4, 5, 6 bits).
        b_tilde: Learnable continuous exponent parameter.
    """

    def __init__(self, bit_width: int = 4, initial_shift: float = 2.0) -> None:
        super().__init__()
        self.bit_width = bit_width
        self.qmin = -(2 ** (bit_width - 1) - 1)
        self.qmax = 2 ** (bit_width - 1) - 1
        self.b_tilde = nn.Parameter(torch.tensor(float(initial_shift)))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Applies fake quantization with learned power-of-two step size."""
        # Discrete shift exponent: b = round(b_tilde)
        b = SteRound.apply(self.b_tilde)
        scale = torch.pow(2.0, -b)

        # Scale, round, clip, and rescale
        x_scaled = x / scale
        x_rounded = SteRound.apply(x_scaled)
        x_clipped = SteClamp.apply(x_rounded, float(self.qmin), float(self.qmax))

        return x_clipped * scale

    def to_integer(self, x: torch.Tensor) -> torch.Tensor:
        """Converts float tensor directly to clipped integer representation."""
        with torch.no_grad():
            b = int(torch.round(self.b_tilde).item())
            scale = 2.0 ** (-b)
            x_scaled = torch.round(x / scale)
            x_int = torch.clamp(x_scaled, float(self.qmin), float(self.qmax))
            return x_int.to(torch.int32)


class CanonicalSignedDigit:
    """Canonical Signed Digit (CSD) table projection for multiplier-free scaling.

    Maps continuous weights into sum of power-of-two terms:
    1-term CSD: s1 * 2^(-a)
    2-term CSD: s1 * 2^(-a) + s2 * 2^(-b)
    where s1, s2 in {-1, 0, 1} and a, b in {0, 1, 2, 3, 4, 5}.
    """

    def __init__(self, max_shift: int = 5, num_terms: int = 2) -> None:
        self.max_shift = max_shift
        self.num_terms = num_terms
        self.candidates = self._build_csd_table()

    def _build_csd_table(self) -> NDArray[np.float32]:
        """Constructs discrete table of admissible CSD values."""
        values = set([0.0])
        shifts = list(range(0, self.max_shift + 1))

        # 1-term: +/- 2^(-a)
        for a in shifts:
            val = 2.0 ** (-a)
            values.add(val)
            values.add(-val)

        # 2-term: +/- 2^(-a) +/- 2^(-b)
        if self.num_terms >= 2:
            for a in shifts:
                for b in shifts:
                    for s1 in [-1.0, 1.0]:
                        for s2 in [-1.0, 1.0]:
                            values.add(s1 * (2.0 ** (-a)) + s2 * (2.0 ** (-b)))

        return np.array(sorted(values), dtype=np.float32)

    def project(self, value: float) -> Tuple[float, List[Tuple[int, int]]]:
        """Projects a continuous value to the nearest CSD value and shift instructions.

        Returns:
            Tuple of (projected_float_value, list of (sign, shift) terms).
        """
        best_val = self.candidates[int(np.argmin(np.abs(self.candidates - value)))]

        # Decompose into shift terms
        terms: List[Tuple[int, int]] = []
        rem = float(best_val)
        for _ in range(self.num_terms):
            if abs(rem) < 1e-6:
                break
            best_sign = 1 if rem > 0 else -1
            target_mag = abs(rem)
            shifts = [abs(2.0 ** (-s) - target_mag) for s in range(self.max_shift + 1)]
            best_shift = int(np.argmin(shifts))
            term_val = best_sign * (2.0 ** (-best_shift))
            terms.append((best_sign, best_shift))
            rem -= term_val

        return float(best_val), terms

