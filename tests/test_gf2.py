"""Unit tests for GF(2) linear algebra utilities."""

import numpy as np
import pytest
from orbit_tied_qnbp.utils.gf2 import (
    gf2_rank,
    gf2_nullspace,
    verify_css_commutativity,
    compute_canonical_logicals,
)


def test_gf2_rank_simple():
    """Verify rank calculation on known binary matrices."""
    # Identity
    assert gf2_rank(np.eye(4, dtype=np.uint8)) == 4
    # Linearly dependent rows
    mat = np.array([
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 0]  # row 0 ^ row 1
    ], dtype=np.uint8)
    assert gf2_rank(mat) == 2


def test_gf2_nullspace():
    """Verify nullspace basis satisfies mat @ v = 0 mod 2."""
    mat = np.array([
        [1, 0, 1, 1],
        [0, 1, 1, 0]
    ], dtype=np.uint8)
    ns = gf2_nullspace(mat)
    assert len(ns) == 2
    for vec in ns:
        assert np.all((mat @ vec) % 2 == 0)


def test_css_steane_code():
    """Verify canonical logicals on the [[7, 1, 3]] Steane code."""
    # Classical [7, 4, 3] Hamming code parity check
    H = np.array([
        [1, 0, 0, 1, 0, 1, 1],
        [0, 1, 0, 1, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 1]
    ], dtype=np.uint8)
    hx = H
    hz = H
    assert verify_css_commutativity(hx, hz)

    lx, lz = compute_canonical_logicals(hx, hz)
    assert lx.shape == (1, 7)
    assert lz.shape == (1, 7)
    # Check orthogonality with checks
    assert np.all((hx @ lz.T) % 2 == 0)
    assert np.all((hz @ lx.T) % 2 == 0)
    # Check symplectic product
    assert (lx @ lz.T)[0, 0] % 2 == 1

