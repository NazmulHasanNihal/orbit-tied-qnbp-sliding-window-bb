"""Galois Field GF(2) linear algebra utilities for quantum error correction.

Provides binary matrix operations, Gaussian elimination, rank calculation,
null space determination, and canonical symplectic logical basis construction.
"""

from typing import Tuple
import numpy as np
from numpy.typing import NDArray


def gf2_rank(matrix: NDArray[np.uint8]) -> int:
    """Computes the binary rank of a matrix over GF(2).

    Args:
        matrix: 2D binary matrix of shape (m, n).

    Returns:
        The integer rank over GF(2).
    """
    mat = matrix.copy() % 2
    rows, cols = mat.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if mat[r, col] == 1:
                pivot = r
                break
        if pivot is not None:
            mat[[rank, pivot]] = mat[[pivot, rank]]
            for r in range(rows):
                if r != rank and mat[r, col] == 1:
                    mat[r] ^= mat[rank]
            rank += 1
    return rank


def gf2_nullspace(matrix: NDArray[np.uint8]) -> NDArray[np.uint8]:
    """Finds a basis for the nullspace of a matrix over GF(2).

    Solves matrix @ v = 0 (mod 2).

    Args:
        matrix: 2D binary matrix of shape (m, n).

    Returns:
        Basis vectors for ker(matrix) as rows of a matrix with shape (k, n).
    """
    mat = matrix.copy() % 2
    rows, cols = mat.shape
    r = 0
    col_to_pivot = {}
    pivots = []

    for col in range(cols):
        pivot = None
        for i in range(r, rows):
            if mat[i, col] == 1:
                pivot = i
                break
        if pivot is not None:
            mat[[r, pivot]] = mat[[pivot, r]]
            for i in range(rows):
                if i != r and mat[i, col] == 1:
                    mat[i] ^= mat[r]
            pivots.append(col)
            col_to_pivot[col] = r
            r += 1

    free_cols = [c for c in range(cols) if c not in col_to_pivot]
    null_basis = []
    for fc in free_cols:
        vec = np.zeros(cols, dtype=np.uint8)
        vec[fc] = 1
        for col in pivots:
            if mat[col_to_pivot[col], fc] == 1:
                vec[col] = 1
        null_basis.append(vec)

    if not null_basis:
        return np.zeros((0, cols), dtype=np.uint8)
    return np.array(null_basis, dtype=np.uint8)


def verify_css_commutativity(hx: NDArray[np.uint8], hz: NDArray[np.uint8]) -> bool:
    """Verifies that HX and HZ satisfy the CSS orthogonality condition HX @ HZ.T = 0 mod 2.

    Args:
        hx: X-check parity check matrix of shape (mx, n).
        hz: Z-check parity check matrix of shape (mz, n).

    Returns:
        True if HX @ HZ.T == 0 (mod 2), False otherwise.
    """
    prod = (hx @ hz.T) % 2
    return bool(np.all(prod == 0))


def compute_canonical_logicals(
    hx: NDArray[np.uint8], hz: NDArray[np.uint8]
) -> Tuple[NDArray[np.uint8], NDArray[np.uint8]]:
    """Constructs canonical logical X and Z operators satisfying symplectic relations.

    For a [[n, k, d]] CSS code defined by HX and HZ:
    - LX @ HZ.T = 0 (mod 2) and LX linearly independent of HX rows.
    - LZ @ HX.T = 0 (mod 2) and LZ linearly independent of HZ rows.
    - LX @ LZ.T = I_k (mod 2).

    Args:
        hx: X-check matrix of shape (mx, n).
        hz: Z-check matrix of shape (mz, n).

    Returns:
        Tuple of (logical_x, logical_z), each of shape (k, n).
    """
    n = hx.shape[1]
    ker_hx = gf2_nullspace(hx)  # contains HZ rows and LZ operators
    ker_hz = gf2_nullspace(hz)  # contains HX rows and LX operators

    rank_hx = gf2_rank(hx)
    rank_hz = gf2_rank(hz)
    k = n - rank_hx - rank_hz
    if k <= 0:
        return np.zeros((0, n), dtype=np.uint8), np.zeros((0, n), dtype=np.uint8)

    # Filter ker_hz down to basis modulo rowspace(HX)
    cand_x = []
    current_space = list(hx.copy() % 2)
    cur_rank = gf2_rank(np.array(current_space)) if current_space else 0

    for vec in ker_hz:
        test_space = np.vstack([current_space, vec]) if len(current_space) > 0 else vec[np.newaxis, :]
        new_rank = gf2_rank(test_space)
        if new_rank > cur_rank:
            cand_x.append(vec)
            current_space.append(vec)
            cur_rank = new_rank
            if len(cand_x) == k:
                break

    cand_x = np.array(cand_x, dtype=np.uint8)

    # Filter ker_hx down to basis modulo rowspace(HZ)
    cand_z = []
    current_space_z = list(hz.copy() % 2)
    cur_rank_z = gf2_rank(np.array(current_space_z)) if current_space_z else 0

    for vec in ker_hx:
        test_space = np.vstack([current_space_z, vec]) if len(current_space_z) > 0 else vec[np.newaxis, :]
        new_rank = gf2_rank(test_space)
        if new_rank > cur_rank_z:
            cand_z.append(vec)
            current_space_z.append(vec)
            cur_rank_z = new_rank
            if len(cand_z) == k:
                break

    cand_z = np.array(cand_z, dtype=np.uint8)

    # Symplectic Gram-Schmidt to achieve LX @ LZ.T = I_k (mod 2)
    lx = cand_x.copy()
    lz = cand_z.copy()
    ip = (lx @ lz.T) % 2

    # Invert binary commutator matrix
    from scipy.linalg import inv
    # We can perform row operations on lz to make ip the identity matrix
    ip_inv = _gf2_invert(ip)
    lz = (ip_inv.T @ lz) % 2

    return lx, lz


def _gf2_invert(matrix: NDArray[np.uint8]) -> NDArray[np.uint8]:
    """Inverts an invertible binary matrix over GF(2)."""
    n = matrix.shape[0]
    aug = np.hstack([matrix.copy() % 2, np.eye(n, dtype=np.uint8)])
    for c in range(n):
        pivot = None
        for r in range(c, n):
            if aug[r, c] == 1:
                pivot = r
                break
        if pivot is None:
            raise ValueError("Matrix is not invertible over GF(2).")
        aug[[c, pivot]] = aug[[pivot, c]]
        for r in range(n):
            if r != c and aug[r, c] == 1:
                aug[r] ^= aug[c]
    return aug[:, n:].astype(np.uint8)

