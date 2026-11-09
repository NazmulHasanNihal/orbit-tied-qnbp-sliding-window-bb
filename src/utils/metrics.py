"""Statistical metrics and confidence interval utilities for Q1 research.

Provides 95% Wilson score intervals, Clopper-Pearson bounds, and paired
hypothesis tests (McNemar test) for quantum error correction benchmarks.
"""

from typing import Tuple, Dict, Any, List
import numpy as np
from scipy import stats


def wilson_score_interval(
    errors: int, total: int, confidence: float = 0.95
) -> Tuple[float, float, float]:
    """Computes the Wilson score confidence interval for a binomial proportion.

    Args:
        errors: Number of observed error events (failures).
        total: Total number of trials (shots).
        confidence: Confidence level (default 0.95 for 95% CI).

    Returns:
        Tuple of (lower_bound, center_estimate, upper_bound).
    """
    if total <= 0:
        return 0.0, 0.0, 0.0

    p_hat = errors / total
    z = float(stats.norm.ppf(1.0 - (1.0 - confidence) / 2.0))

    denom = 1.0 + (z ** 2) / total
    center = (p_hat + (z ** 2) / (2.0 * total)) / denom
    half_width = (
        z * np.sqrt((p_hat * (1.0 - p_hat) + (z ** 2) / (4.0 * total)) / total)
    ) / denom

    lower = max(0.0, float(center - half_width))
    upper = min(1.0, float(center + half_width))

    return lower, float(p_hat), upper


def mcnemar_paired_test(
    outcomes_a: np.ndarray, outcomes_b: np.ndarray
) -> Tuple[float, float]:
    """Computes McNemar's paired test statistic and exact two-tailed p-value.

    Used to compare paired decoders tested on identical Stim shots.
    outcomes: 1 if logical error, 0 if success.

    Returns:
        Tuple of (test_statistic, p_value).
    """
    assert len(outcomes_a) == len(outcomes_b), "Outcomes must have equal length."

    # b: A correct (0), B incorrect (1)
    b = int(np.sum((outcomes_a == 0) & (outcomes_b == 1)))
    # c: A incorrect (1), B correct (0)
    c = int(np.sum((outcomes_a == 1) & (outcomes_b == 0)))

    if b + c == 0:
        return 0.0, 1.0

    # With continuity correction
    statistic = ((abs(b - c) - 1.0) ** 2) / (b + c)
    # Exact binomial p-value for small sample discordant pairs
    p_value = 2.0 * stats.binom.cdf(min(b, c), b + c, 0.5)
    p_value = min(1.0, float(p_value))

    return float(statistic), p_value


def format_ci_metric(errors: int, total: int) -> Dict[str, Any]:
    """Formats error rate with 95% Wilson confidence intervals."""
    lower, rate, upper = wilson_score_interval(errors, total, confidence=0.95)
    return {
        "errors": errors,
        "total": total,
        "rate": rate,
        "ci_95_lower": lower,
        "ci_95_upper": upper,
        "display": f"{rate:.4e} [{lower:.4e}, {upper:.4e}]",
    }
