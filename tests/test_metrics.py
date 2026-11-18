"""Unit tests for statistical metrics, Wilson score intervals, and McNemar tests."""

import numpy as np
import pytest
from orbit_tied_qnbp.utils.metrics import (
    wilson_score_interval,
    mcnemar_paired_test,
    mcnemar_test_detailed,
    format_ci_metric,
)


def test_wilson_score_interval_bounds():
    # Zero errors out of 37,800
    low, rate, high = wilson_score_interval(0, 37800, confidence=0.95)
    assert low == 0.0
    assert rate == 0.0
    assert 1.01e-4 <= high <= 1.02e-4

    # 100 errors out of 10,000 (1%)
    low, rate, high = wilson_score_interval(100, 10000, confidence=0.95)
    assert rate == 0.01
    assert 0.008 <= low < 0.01
    assert 0.01 < high <= 0.013

    # Edge cases
    assert wilson_score_interval(0, 0) == (0.0, 0.0, 0.0)


def test_mcnemar_exact_binomial_small_sample():
    # Small discordant count b=10, c=0 -> b+c = 10 < 25
    outcomes_a = np.array([0] * 10 + [0] * 90)
    outcomes_b = np.array([1] * 10 + [0] * 90)

    res = mcnemar_test_detailed(outcomes_a, outcomes_b)
    assert res["b"] == 10
    assert res["c"] == 0
    assert res["method"] == "exact_binomial"
    # Exact binomial p-value for (0, 10, 0.5) is 2 * (0.5)^10 = 2 / 1024 = 0.001953125
    assert pytest.approx(res["p_value"], rel=1e-3) == 0.001953125
    assert res["statistic"] == ((9.0) ** 2) / 10.0


def test_mcnemar_asymptotic_large_sample():
    # Large discordant count b=50, c=10 -> b+c = 60 >= 25
    outcomes_a = np.array([0] * 50 + [1] * 10 + [0] * 40)
    outcomes_b = np.array([1] * 50 + [0] * 10 + [0] * 40)

    res = mcnemar_test_detailed(outcomes_a, outcomes_b)
    assert res["b"] == 50
    assert res["c"] == 10
    assert res["method"] == "asymptotic_chi2"
    assert res["p_value"] < 1e-6
    # Stat = (abs(50 - 10) - 1)^2 / 60 = 39^2 / 60 = 1521 / 60 = 25.35
    assert pytest.approx(res["statistic"], rel=1e-3) == 25.35


def test_mcnemar_identical_outcomes():
    outcomes_a = np.array([1, 0, 1, 0])
    outcomes_b = np.array([1, 0, 1, 0])
    stat, p = mcnemar_paired_test(outcomes_a, outcomes_b)
    assert stat == 0.0
    assert p == 1.0


def test_format_ci_metric():
    res = format_ci_metric(68, 10000)
    assert res["errors"] == 68
    assert res["total"] == 10000
    assert res["rate"] == 0.0068
    assert "6.8000e-03" in res["display"]
