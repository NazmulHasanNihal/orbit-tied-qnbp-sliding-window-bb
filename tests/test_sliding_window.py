"""Unit tests for sliding-window scheduling, confidence margin gates, and queue model."""

import numpy as np
import pytest
from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.decoder.baselines import DecodeResult
from orbit_tied_qnbp.decoder.sliding_window import (
    ConfidenceGate,
    SlidingWindowManager,
    TraceDrivenQueueSimulator,
)


def test_confidence_gates():
    """Verify gating logic for G1, G2, G3, and control_all."""
    # Dummy decode result: converged, fault 0 flipped with LLR = -1.5, fault 1 flipped with LLR = -5.0
    corrections = np.array([1, 1, 0, 0], dtype=np.uint8)
    final_llrs = np.array([-1.5, -5.0, 10.0, 8.0], dtype=np.float32)
    obs_matrix = np.array([
        [1, 0, 0, 0],  # obs 0 touches fault 0
        [0, 1, 0, 0],  # obs 1 touches fault 1
    ], dtype=np.float32)

    res = DecodeResult(
        converged=True,
        iterations=5,
        corrections=corrections,
        predicted_observables=np.array([1, 1], dtype=np.uint8),
        final_llrs=final_llrs,
    )

    # G1 accepts any converged result
    assert ConfidenceGate.evaluate("G1", res, obs_matrix, tau=2.0) is True

    # G2 requires min |LLR| among flipped faults >= tau. Here min(|-1.5|, |-5.0|) = 1.5 < 2.0 -> Rejected!
    assert ConfidenceGate.evaluate("G2", res, obs_matrix, tau=2.0) is False
    assert ConfidenceGate.evaluate("G2", res, obs_matrix, tau=1.0) is True

    # G3: checks min |LLR| among committed faults touching each observable
    # For obs 0, fault 0 has |LLR|=1.5 < 2.0 -> Rejected at tau=2.0
    assert ConfidenceGate.evaluate("G3", res, obs_matrix, tau=2.0) is False
    assert ConfidenceGate.evaluate("G3", res, obs_matrix, tau=1.0) is True


def test_sliding_window_schedule():
    """Verify sliding-window round slicing with W=3, F=1 on 6 rounds."""
    code = BivariateBicycleCode.code_72_12_6()
    mgr = SlidingWindowManager(code=code, window_width=3, commit_stride=1)
    schedule = mgr.get_window_schedule(total_rounds=6)

    assert len(schedule) == 4
    assert schedule[0] == (0, 2, 0)
    assert schedule[1] == (1, 3, 1)
    assert schedule[2] == (2, 4, 2)
    assert schedule[3] == (3, 5, 3)


def test_queue_simulator():
    """Verify trace-driven sequential queue simulation."""
    sim = TraceDrivenQueueSimulator(
        t_cycle_ns=1000.0,
        commit_stride=1,
        ns_per_iteration_fast=24.0,  # 24 ns / iter
        ns_per_iteration_slow=100.0,
    )

    # 100 windows: 90 accepted on fast path (5 iterations), 10 consecutive fallbacks
    fast_iters = [5] * 100
    is_accepted = [True] * 90 + [False] * 10
    slow_iters = [20] * 100

    # With capacity 5, 10 consecutive fallbacks cause exactly 5 buffer overflow events (0.05)
    report_cap5 = sim.simulate(fast_iters, is_accepted, slow_iters, buffer_capacity=5)
    assert report_cap5["p_fast"] == pytest.approx(0.9)
    assert report_cap5["mean_service_ns"] == pytest.approx(332.0, rel=1e-1)
    assert report_cap5["utilization"] < 1.0  # Stable on average
    assert report_cap5["is_stable"] == 1.0
    assert report_cap5["overflow_rate"] == pytest.approx(0.05)

    # With buffer capacity 15, the queue absorbs the 10-burst without overflow
    report_cap15 = sim.simulate(fast_iters, is_accepted, slow_iters, buffer_capacity=15)
    assert report_cap15["overflow_rate"] == 0.0
    assert report_cap15["max_backlog"] == 10.0
