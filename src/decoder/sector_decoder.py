"""Separate X and Z Sector Decoder for Bivariate-Bicycle QLDPC Codes.

Implements decoupled X-sector and Z-sector belief propagation decoding
across T in {10, 20, 30, 50} iterations to benchmark baseline convergence
without split-belief inter-sector cross-talk.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import scipy.sparse as sp
from numpy.typing import NDArray

from src.circuits.bivariate_bicycle import BivariateBicycleCode
from src.data.dem_graph import DemGraph
from src.decoder.baselines import DecodeResult, MinSumDecoder
from src.utils.metrics import format_ci_metric


class SeparateXZSectorDecoder:
    """Decodes X and Z check sectors independently using CSS Tanner graph decoupling.

    Attributes:
        code: BivariateBicycleCode instance.
        hx: Parity-check matrix for X-checks [A, B].
        hz: Parity-check matrix for Z-checks [B^T, A^T].
        lx: Canonical logical X operators.
        lz: Canonical logical Z operators.
    """

    def __init__(
        self,
        code: BivariateBicycleCode,
        max_iter: int = 30,
        alpha: float = 0.75,
    ) -> None:
        self.code = code
        self.max_iter = max_iter
        self.alpha = alpha

        self.hx = code.hx
        self.hz = code.hz
        self.lx = code.lx
        self.lz = code.lz

        self.n = code.num_data_qubits
        self.k = code.num_logicals

    def decode_phenom_sectors(
        self,
        syn_x: NDArray[np.uint8],
        syn_z: NDArray[np.uint8],
        prior_p: float = 0.003,
        num_iters: int = 30,
    ) -> Tuple[bool, bool, NDArray[np.uint8], NDArray[np.uint8]]:
        """Decodes phenomenological X and Z syndromes independently.

        Args:
            syn_x: Binary syndrome for X-checks (length |G|).
            syn_z: Binary syndrome for Z-checks (length |G|).
            prior_p: Physical error probability p.
            num_iters: Belief propagation iterations.

        Returns:
            Tuple of (conv_x, conv_z, pred_obs_z, pred_obs_x).
        """
        prior_llr = float(np.log((1.0 - prior_p) / prior_p))

        # Decode X-checks -> predicts Z errors (e_z)
        conv_x, e_z = self._decode_single_sector(
            pcm=self.hx,
            syndrome=syn_x,
            prior_llr=prior_llr,
            num_iters=num_iters,
        )
        pred_obs_z = (self.lz @ e_z) % 2

        # Decode Z-checks -> predicts X errors (e_x)
        conv_z, e_x = self._decode_single_sector(
            pcm=self.hz,
            syndrome=syn_z,
            prior_llr=prior_llr,
            num_iters=num_iters,
        )
        pred_obs_x = (self.lx @ e_x) % 2

        return conv_x, conv_z, pred_obs_z, pred_obs_x

    def _decode_single_sector(
        self,
        pcm: NDArray[np.uint8],
        syndrome: NDArray[np.uint8],
        prior_llr: float,
        num_iters: int,
    ) -> Tuple[bool, NDArray[np.uint8]]:
        """Vectorized Min-Sum decoding on a single CSS check matrix."""
        num_checks, num_bits = pcm.shape
        check_to_bits = [np.where(pcm[c] == 1)[0] for c in range(num_checks)]
        bit_to_checks = [np.where(pcm[:, v] == 1)[0] for v in range(num_bits)]

        # Messages: check-to-bit and bit-to-check
        msg_b2c = { (c, v): prior_llr for c in range(num_checks) for v in check_to_bits[c] }
        msg_c2b = { (c, v): 0.0 for c in range(num_checks) for v in check_to_bits[c] }
        posteriors = np.full(num_bits, prior_llr, dtype=np.float32)

        converged = False
        for _ in range(num_iters):
            # Check Node Update
            for c in range(num_checks):
                bits = check_to_bits[c]
                signs = [np.sign(msg_b2c[(c, v)]) if msg_b2c[(c, v)] != 0 else 1.0 for v in bits]
                prod_sign = int(np.prod(signs))
                if syndrome[c] == 1:
                    prod_sign = -prod_sign
                mags = [abs(msg_b2c[(c, v)]) for v in bits]

                for idx, v in enumerate(bits):
                    other_mags = [mags[j] for j in range(len(bits)) if j != idx]
                    min_mag = min(other_mags) if other_mags else 0.0
                    sgn_out = prod_sign * signs[idx]
                    msg_c2b[(c, v)] = sgn_out * (self.alpha * min_mag)

            # Variable Node Update
            for v in range(num_bits):
                checks = bit_to_checks[v]
                sum_in = sum(msg_c2b[(c, v)] for c in checks)
                posteriors[v] = prior_llr + sum_in
                for c in checks:
                    msg_b2c[(c, v)] = posteriors[v] - msg_c2b[(c, v)]

            # Hard decision & syndrome check
            hard_e = (posteriors < 0.0).astype(np.uint8)
            syn_check = (pcm @ hard_e) % 2
            if np.all(syn_check == syndrome):
                converged = True
                break

        return converged, hard_e


def benchmark_separate_sectors(
    code_cls: Any = BivariateBicycleCode.code_72_12_6,
    num_shots: int = 500,
    p_phys: float = 0.003,
    iter_list: List[int] = [10, 20, 30, 50],
    seed: int = 42,
) -> Dict[str, Any]:
    """Benchmarks separate X/Z decoding across T in {10, 20, 30, 50}."""
    code = code_cls()
    decoder = SeparateXZSectorDecoder(code=code, alpha=0.75)
    rng = np.random.default_rng(seed)

    results: Dict[str, Any] = {}

    for t_iter in iter_list:
        errors_z = 0  # Logical Z errors from X-checks
        errors_x = 0  # Logical X errors from Z-checks
        total_conv_x = 0
        total_conv_z = 0

        for _ in range(num_shots):
            # Sample independent Z errors on data qubits
            true_e_z = (rng.random(code.num_data_qubits) < p_phys).astype(np.uint8)
            syn_x = (code.hx @ true_e_z) % 2
            true_obs_z = (code.lz @ true_e_z) % 2

            # Sample independent X errors on data qubits
            true_e_x = (rng.random(code.num_data_qubits) < p_phys).astype(np.uint8)
            syn_z = (code.hz @ true_e_x) % 2
            true_obs_x = (code.lx @ true_e_x) % 2

            conv_x, conv_z, pred_obs_z, pred_obs_x = decoder.decode_phenom_sectors(
                syn_x=syn_x,
                syn_z=syn_z,
                prior_p=p_phys,
                num_iters=t_iter,
            )

            if conv_x:
                total_conv_x += 1
            if conv_z:
                total_conv_z += 1

            if np.any(pred_obs_z != true_obs_z):
                errors_z += 1
            if np.any(pred_obs_x != true_obs_x):
                errors_x += 1

        ci_z = format_ci_metric(errors_z, num_shots)
        ci_x = format_ci_metric(errors_x, num_shots)

        results[f"T_{t_iter}"] = {
            "iterations": t_iter,
            "sector_x": {
                "ler_z": ci_z["rate"],
                "ci": ci_z["display"],
                "convergence": total_conv_x / num_shots,
            },
            "sector_z": {
                "ler_x": ci_x["rate"],
                "ci": ci_x["display"],
                "convergence": total_conv_z / num_shots,
            },
        }

    return results


if __name__ == "__main__":
    res = benchmark_separate_sectors(num_shots=200)
    print("✅ Separate Sector Benchmark Results:")
    for k, v in res.items():
        print(f"  {k}: Sector X (LER_Z) = {v['sector_x']['ci']} (conv: {v['sector_x']['convergence']:.2f}) | Sector Z (LER_X) = {v['sector_z']['ci']} (conv: {v['sector_z']['convergence']:.2f})")
