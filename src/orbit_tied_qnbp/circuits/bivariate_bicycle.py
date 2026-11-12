"""Bivariate Bicycle (BB) Quantum LDPC Code and Stim Circuit Generator.

Implements code construction, check matrix derivation over GF(2), and the
Bravyi et al. (Nature 2024) depth-7 syndrome measurement circuit in Stim.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
from numpy.typing import NDArray
import stim

from orbit_tied_qnbp.utils.gf2 import (
    gf2_rank,
    verify_css_commutativity,
    compute_canonical_logicals,
)


class BivariateBicycleCode:
    """Represents a Bivariate Bicycle (BB) CSS quantum LDPC code QC(A, B).

    The code is defined by polynomials A(x, y) and B(x, y) over the group algebra
    F_2[x, y] / (x^l - 1, y^m - 1).

    Attributes:
        l: Cyclic shift length along x-dimension.
        m: Cyclic shift length along y-dimension.
        group_order: Order of the group G = Z_l x Z_m, |G| = l * m.
        num_data_qubits: Total data qubits n = 2 * |G|.
        hx: Parity check matrix for X-checks [A, B] of shape (|G|, 2|G|).
        hz: Parity check matrix for Z-checks [B^T, A^T] of shape (|G|, 2|G|).
        lx: Canonical logical X operators of shape (k, 2|G|).
        lz: Canonical logical Z operators of shape (k, 2|G|).
        num_logicals: Number of logical qubits k.
    """

    def __init__(
        self,
        l: int,
        m: int,
        a_terms: List[Tuple[int, int]],
        b_terms: List[Tuple[int, int]],
    ) -> None:
        """Initializes the Bivariate Bicycle code.

        Args:
            l: Dimension l.
            m: Dimension m.
            a_terms: Monomial powers (x_pow, y_pow) for polynomial A(x, y).
            b_terms: Monomial powers (x_pow, y_pow) for polynomial B(x, y).
        """
        self.l = l
        self.m = m
        self.group_order = l * m
        self.num_data_qubits = 2 * self.group_order
        self.a_terms = a_terms
        self.b_terms = b_terms

        # Compute cyclic matrices
        self.a_matrix = self._get_cyclic_matrix(a_terms)
        self.b_matrix = self._get_cyclic_matrix(b_terms)

        # Check matrices
        self.hx = np.hstack([self.a_matrix, self.b_matrix])
        self.hz = np.hstack([self.b_matrix.T, self.a_matrix.T])

        if not verify_css_commutativity(self.hx, self.hz):
            raise ValueError("CSS commutativity failed: HX @ HZ.T != 0 (mod 2).")

        # Logical operators
        self.lx, self.lz = compute_canonical_logicals(self.hx, self.hz)
        self.num_logicals = len(self.lx)

        # Precompute permutation mappings for monomials A1, A2, A3, B1, B2, B3
        self.perms = self._build_permutation_tables()

    @classmethod
    def gross_72(cls) -> "BivariateBicycleCode":
        """Instantiates the canonical [[72, 12, 6]] Gross Bivariate-Bicycle code."""
        return cls(
            l=6,
            m=6,
            a_terms=[(3, 0), (0, 1), (0, 2)],
            b_terms=[(0, 3), (1, 0), (2, 0)],
        )

    @classmethod
    def gross_144(cls) -> "BivariateBicycleCode":
        """Instantiates the canonical [[144, 12, 12]] Gross Bivariate-Bicycle code."""
        return cls(
            l=12,
            m=6,
            a_terms=[(3, 0), (0, 1), (0, 2)],
            b_terms=[(0, 3), (1, 0), (2, 0)],
        )

    @classmethod
    def code_72_12_6(cls) -> "BivariateBicycleCode":
        """Instantiates the [[72, 12, 6]] BB code (Bravyi et al. Nature 2024)."""
        return cls(
            l=6,
            m=6,
            a_terms=[(3, 0), (0, 1), (0, 2)],  # x^3 + y + y^2
            b_terms=[(0, 3), (1, 0), (2, 0)],  # y^3 + x + x^2
        )

    @classmethod
    def code_144_12_12(cls) -> "BivariateBicycleCode":
        """Instantiates the [[144, 12, 12]] Gross code (Bravyi et al. Nature 2024)."""
        return cls(
            l=12,
            m=6,
            a_terms=[(3, 0), (0, 1), (0, 2)],  # x^3 + y + y^2
            b_terms=[(0, 3), (1, 0), (2, 0)],  # y^3 + x + x^2
        )

    def _get_cyclic_matrix(self, poly_terms: List[Tuple[int, int]]) -> NDArray[np.uint8]:
        """Constructs a |G| x |G| binary permutation representation matrix."""
        mat = np.zeros((self.group_order, self.group_order), dtype=np.uint8)
        for x in range(self.l):
            for y in range(self.m):
                row = x * self.m + y
                for a, b in poly_terms:
                    col = ((x + a) % self.l) * self.m + ((y + b) % self.m)
                    mat[row, col] ^= 1
        return mat

    def _get_perm(self, a: int, b: int) -> NDArray[np.int64]:
        """Returns permutation index array for shift x^a y^b."""
        perm = np.zeros(self.group_order, dtype=np.int64)
        for x in range(self.l):
            for y in range(self.m):
                i = x * self.m + y
                perm[i] = ((x + a) % self.l) * self.m + ((y + b) % self.m)
        return perm

    def _build_permutation_tables(self) -> Dict[str, NDArray[np.int64]]:
        """Precomputes monomial shift permutations and their transposes."""
        # A1 = x^3, A2 = y, A3 = y^2; B1 = y^3, B2 = x, B3 = x^2
        a1_pow, a2_pow, a3_pow = self.a_terms[0], self.a_terms[1], self.a_terms[2]
        b1_pow, b2_pow, b3_pow = self.b_terms[0], self.b_terms[1], self.b_terms[2]

        return {
            "A1": self._get_perm(a1_pow[0], a1_pow[1]),
            "A2": self._get_perm(a2_pow[0], a2_pow[1]),
            "A3": self._get_perm(a3_pow[0], a3_pow[1]),
            "B1": self._get_perm(b1_pow[0], b1_pow[1]),
            "B2": self._get_perm(b2_pow[0], b2_pow[1]),
            "B3": self._get_perm(b3_pow[0], b3_pow[1]),
            "A1_T": self._get_perm(-a1_pow[0], -a1_pow[1]),
            "A2_T": self._get_perm(-a2_pow[0], -a2_pow[1]),
            "A3_T": self._get_perm(-a3_pow[0], -a3_pow[1]),
            "B1_T": self._get_perm(-b1_pow[0], -b1_pow[1]),
            "B2_T": self._get_perm(-b2_pow[0], -b2_pow[1]),
            "B3_T": self._get_perm(-b3_pow[0], -b3_pow[1]),
        }

    def build_stim_circuit(
        self,
        rounds: int,
        error_rate: float = 0.0,
        bias: Optional[float] = None,
    ) -> stim.Circuit:
        """Constructs the depth-7 syndrome measurement Stim circuit.

        Qubit register allocations:
            q(X): indices 0 .. |G|-1 (ancillas for Z error syndrome)
            q(L): indices |G| .. 2|G|-1 (left data qubits)
            q(R): indices 2|G| .. 3|G|-1 (right data qubits)
            q(Z): indices 3|G| .. 4|G|-1 (ancillas for X error syndrome)

        Args:
            rounds: Number of syndrome extraction rounds Nc.
            error_rate: Physical noise rate p.
            bias: Pauli Z noise bias eta = p_z / (p_x + p_y). If None or <= 0.5,
                standard symmetric depolarizing noise is applied. If > 0.5,
                asymmetric Pauli channel noise is applied.

        Returns:
            A complete, annotated stim.Circuit ready for DEM extraction.
        """
        c = stim.Circuit()
        g = self.group_order

        # Initialize data qubits to |0> and Z ancillas to |0>
        c.append("R", list(range(g, 3 * g)))
        if error_rate > 0:
            self._apply_single_qubit_noise(c, list(range(g, 3 * g)), error_rate, bias, "X_ERROR")
        c.append("R", list(range(3 * g, 4 * g)))
        if error_rate > 0:
            self._apply_single_qubit_noise(c, list(range(3 * g, 4 * g)), error_rate, bias, "X_ERROR")
        c.append("TICK")

        for r in range(rounds):
            self._append_syndrome_round(c, r, error_rate, bias)

        # Terminal measurement on data qubits in Z-basis
        if error_rate > 0:
            self._apply_single_qubit_noise(c, list(range(g, 3 * g)), error_rate, bias, "X_ERROR")
        c.append("M", list(range(g, 3 * g)))

        # Append terminal detectors comparing final data parities to last Z-ancilla
        self._append_terminal_detectors(c)

        # Append logical Z observables
        self._append_logical_observables(c)

        return c

    def _append_syndrome_round(
        self, c: stim.Circuit, r: int, p: float, bias: Optional[float] = None
    ) -> None:
        """Appends one round of the depth-7 CNOT syndrome extraction schedule."""
        g = self.group_order
        p_tab = self.perms

        # Round 1: InitX q(X), CNOT q(R, A1_T) -> q(Z)
        c.append("RX", list(range(0, g)))
        if p > 0:
            self._apply_single_qubit_noise(c, list(range(0, g)), p, bias, "Z_ERROR")
        t_r1 = [item for i in range(g) for item in (2 * g + int(p_tab["A1_T"][i]), 3 * g + i)]
        self._apply_cnot_layer(c, t_r1, p, bias)

        # Round 2: CNOT q(X) -> q(L, A2), CNOT q(R, A3_T) -> q(Z)
        t_r2 = []
        for i in range(g):
            t_r2.extend([i, g + int(p_tab["A2"][i]), 2 * g + int(p_tab["A3_T"][i]), 3 * g + i])
        self._apply_cnot_layer(c, t_r2, p, bias)

        # Round 3: CNOT q(X) -> q(R, B2), CNOT q(L, B1_T) -> q(Z)
        t_r3 = []
        for i in range(g):
            t_r3.extend([i, 2 * g + int(p_tab["B2"][i]), g + int(p_tab["B1_T"][i]), 3 * g + i])
        self._apply_cnot_layer(c, t_r3, p, bias)

        # Round 4: CNOT q(X) -> q(R, B1), CNOT q(L, B2_T) -> q(Z)
        t_r4 = []
        for i in range(g):
            t_r4.extend([i, 2 * g + int(p_tab["B1"][i]), g + int(p_tab["B2_T"][i]), 3 * g + i])
        self._apply_cnot_layer(c, t_r4, p, bias)

        # Round 5: CNOT q(X) -> q(R, B3), CNOT q(L, B3_T) -> q(Z)
        t_r5 = []
        for i in range(g):
            t_r5.extend([i, 2 * g + int(p_tab["B3"][i]), g + int(p_tab["B3_T"][i]), 3 * g + i])
        self._apply_cnot_layer(c, t_r5, p, bias)

        # Round 6: CNOT q(X) -> q(L, A1), CNOT q(R, A2_T) -> q(Z)
        t_r6 = []
        for i in range(g):
            t_r6.extend([i, g + int(p_tab["A1"][i]), 2 * g + int(p_tab["A2_T"][i]), 3 * g + i])
        self._apply_cnot_layer(c, t_r6, p, bias)

        # Round 7: CNOT q(X) -> q(L, A3)
        t_r7 = [item for i in range(g) for item in (i, g + int(p_tab["A3"][i]))]
        self._apply_cnot_layer(c, t_r7, p, bias)

        # Measure Z ancillas & Record detectors
        if p > 0:
            self._apply_single_qubit_noise(c, list(range(3 * g, 4 * g)), p, bias, "X_ERROR")
        c.append("M", list(range(3 * g, 4 * g)))
        for i in range(g):
            rec = -(g - i)
            targets = [stim.target_rec(rec)] if r == 0 else [stim.target_rec(rec), stim.target_rec(rec - 2 * g)]
            c.append("DETECTOR", targets)
        c.append("TICK")

        # Round 8: Measure X ancillas & Reset Z ancillas
        if p > 0:
            self._apply_single_qubit_noise(c, list(range(0, g)), p, bias, "Z_ERROR")
        c.append("MX", list(range(0, g)))
        c.append("R", list(range(3 * g, 4 * g)))
        if p > 0:
            self._apply_single_qubit_noise(c, list(range(3 * g, 4 * g)), p, bias, "X_ERROR")
        for i in range(g):
            rec = -(g - i)
            if r > 0:
                c.append("DETECTOR", [stim.target_rec(rec), stim.target_rec(rec - 2 * g)])
        c.append("TICK")

    def _apply_single_qubit_noise(
        self,
        c: stim.Circuit,
        targets: List[int],
        p: float,
        bias: Optional[float] = None,
        default_error: str = "DEPOLARIZE1",
    ) -> None:
        """Appends single-qubit noise, optionally biased towards Pauli Z."""
        if p <= 0:
            return
        if bias is not None and bias > 0.5:
            pz = (p * bias) / (bias + 1.0)
            px = (p / (bias + 1.0)) / 2.0
            py = px
            c.append("PAULI_CHANNEL_1", targets, [px, py, pz])
        else:
            if default_error == "DEPOLARIZE1":
                c.append("DEPOLARIZE1", targets, p)
            else:
                c.append(default_error, targets, p)

    def _apply_cnot_layer(
        self,
        c: stim.Circuit,
        targets: List[int],
        p: float,
        bias: Optional[float] = None,
    ) -> None:
        """Appends a CNOT layer followed by depolarizing or biased noise and a TICK."""
        c.append("CX", targets)
        if p > 0:
            if bias is not None and bias > 0.5:
                pz_pair = (p * bias) / (bias + 1.0) / 3.0
                p_other = (p / (bias + 1.0)) / 12.0
                # PAULI_CHANNEL_2 15 probabilities:
                # IX, IY, IZ, XI, XX, XY, XZ, YI, YX, YY, YZ, ZI, ZX, ZY, ZZ
                probs = [
                    p_other, p_other, pz_pair,
                    p_other, p_other, p_other, p_other,
                    p_other, p_other, p_other, p_other,
                    pz_pair, p_other, p_other, pz_pair,
                ]
                c.append("PAULI_CHANNEL_2", targets, probs)
            else:
                c.append("DEPOLARIZE2", targets, p)
        c.append("TICK")

    def _append_terminal_detectors(self, c: stim.Circuit) -> None:
        """Connects the final data measurements to the last round's Z ancilla checks."""
        g = self.group_order
        p_tab = self.perms
        for i in range(g):
            targets = [
                stim.target_rec(-(2 * g - int(p_tab["B1_T"][i]))),
                stim.target_rec(-(2 * g - int(p_tab["B2_T"][i]))),
                stim.target_rec(-(2 * g - int(p_tab["B3_T"][i]))),
                stim.target_rec(-(2 * g - (g + int(p_tab["A1_T"][i])))),
                stim.target_rec(-(2 * g - (g + int(p_tab["A2_T"][i])))),
                stim.target_rec(-(2 * g - (g + int(p_tab["A3_T"][i])))),
                stim.target_rec(-(4 * g - i)),
            ]
            c.append("DETECTOR", targets)

    def _append_logical_observables(self, c: stim.Circuit) -> None:
        """Adds OBSERVABLE_INCLUDE instructions for the canonical logical Z basis."""
        g = self.group_order
        for k in range(self.num_logicals):
            obs_targets = [
                stim.target_rec(-(2 * g - j))
                for j in range(2 * g)
                if self.lz[k, j] == 1
            ]
            c.append("OBSERVABLE_INCLUDE", obs_targets, k)

