"""Unit tests for Real-World Benchmarks module."""

import os
import pytest
from orbit_tied_qnbp.experiments.run_realworld_benchmarks import (
    run_heron_calibration_benchmark,
    run_streaming_100round_survival,
    run_axi_stream_ingress_benchmark,
)


def test_heron_calibration_benchmark_smoke():
    """Verifies that IBM Heron calibration benchmark executes and returns valid metrics."""
    res = run_heron_calibration_benchmark(n_shots=10, seed=1234)
    assert res["profile"] == "IBM Quantum Heron r2"
    assert "decoders" in res
    assert "proposed_qnbp_6bit" in res["decoders"]
    assert "standalone_bposd_10" in res["decoders"]
    assert res["decoders"]["proposed_qnbp_6bit"]["dsp_multipliers"] == 0
    assert 0.0 <= res["decoders"]["proposed_qnbp_6bit"]["rate"] <= 1.0


def test_streaming_100round_survival_smoke():
    """Verifies that 100-round streaming survival benchmark executes and computes retention."""
    res = run_streaming_100round_survival(n_shots=5, rounds=100, seed=1234)
    assert res["rounds"] == 100
    assert "survival_at_checkpoints" in res
    assert "pipeline_gate_g3" in res["survival_at_checkpoints"]
    assert "round_100" in res["survival_at_checkpoints"]["pipeline_gate_g3"]
    assert res["survival_at_checkpoints"]["pipeline_gate_g3"]["round_100"] > 0.0


def test_axi_stream_ingress_benchmark():
    """Verifies that AXI4-Stream ingress parameters meet sub-microsecond requirements."""
    res = run_axi_stream_ingress_benchmark()
    assert res["clock_mhz"] == 250.0
    assert res["line_rate_gbps"] >= 1.0
    assert res["max_latency_ns"] <= 250.0
    assert res["cycle_slack_ns"] >= 750.0
    assert res["observed_buffer_overflow"] == 0.0
