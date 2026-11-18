"""Verification of Automorphism Group Action and Orbit Closure for Bivariate-Bicycle DEM.

Verifies that all 36 elements of the 2D torus translation group G = Z_6 x Z_6:
  1) Induce exact automorphisms of the Detector Error Model (DEM) graph.
  2) Preserve fault prior probabilities: p(g(v)) == p(v).
  3) Strictly preserve orbit membership (Orbit Closure): orbit(g(v)) == orbit(v).
  4) Partition all 7,308 fault mechanisms on [[72,12,6]] into exactly 203 orbits of size 36.
Saves verification results to results/automorphism_closure_verification.json.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Set, Tuple

# Ensure src is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.decoder.orbits import DemOrbitManager


def verify_automorphism_orbits(
    rounds: int = 3,
    error_rate: float = 0.003,
    out_path: str = "results/automorphism_closure_verification.json",
) -> Dict[str, Any]:
    print(f"=== Verifying Automorphism Orbits and Group Closure (rounds={rounds}, p={error_rate}) ===")
    t0 = time.time()
    code = BivariateBicycleCode.code_72_12_6()
    circuit = code.build_stim_circuit(rounds=rounds, error_rate=error_rate)
    dem = circuit.detector_error_model(decompose_errors=False, approximate_disjoint_errors=True)
    mgr = DemOrbitManager(code=code, num_rounds=rounds, dem=dem)

    l, m = code.l, code.m
    group_order = code.group_order  # 36
    num_errors = len(mgr.parsed_errors)  # 7308
    num_orbits = mgr.num_fault_orbits  # 203

    print(f"Code: [[72, 12, 6]], Torus Dimensions: l={l}, m={m}, |G|={group_order}")
    print(f"Total DEM Fault Mechanisms: {num_errors}")
    print(f"Total Disjoint Orbits: {num_orbits}")

    # Build symptom lookup map: (sorted_detectors, rounded_p) -> fault_index
    symptom_map: Dict[Tuple[Tuple[int, ...], float], int] = {}
    for idx, (p, dets, _) in enumerate(mgr.parsed_errors):
        key = (dets, round(p, 12))
        symptom_map[key] = idx

    # 1. Verify orbit partition sizes
    orbit_members: Dict[int, List[int]] = {o: [] for o in range(num_orbits)}
    for f_idx, o_id in enumerate(mgr.fault_orbits):
        orbit_members[int(o_id)].append(f_idx)

    orbit_sizes = [len(orbit_members[o]) for o in range(num_orbits)]
    min_orbit_size = int(min(orbit_sizes))
    max_orbit_size = int(max(orbit_sizes))
    all_orbits_size_36 = (min_orbit_size == group_order) and (max_orbit_size == group_order)
    print(f"Orbit Sizes: min={min_orbit_size}, max={max_orbit_size} (All exactly {group_order}: {all_orbits_size_36})")

    # 2. Verify group closure and automorphism invariance across all 36 shifts
    closure_violations = 0
    probability_violations = 0
    missing_targets = 0
    shifts_verified = 0

    shift_stats = []

    for a in range(l):
        for b in range(m):
            matched_faults = 0
            shift_closure_ok = True
            shift_prob_ok = True

            for v_idx in range(num_errors):
                p_v, dets_v, _ = mgr.parsed_errors[v_idx]
                o_v = mgr.fault_orbits[v_idx]

                # Apply torus shift to detectors
                shifted_dets = tuple(sorted([mgr.shift_detector(d, a, b) for d in dets_v]))
                p_rounded = round(p_v, 12)
                target_key = (shifted_dets, p_rounded)

                if target_key in symptom_map:
                    v_target = symptom_map[target_key]
                    o_target = mgr.fault_orbits[v_target]

                    # Orbit closure check
                    if o_target != o_v:
                        closure_violations += 1
                        shift_closure_ok = False

                    # Probability equality check
                    p_target = mgr.parsed_errors[v_target][0]
                    if abs(p_target - p_v) > 1e-12:
                        probability_violations += 1
                        shift_prob_ok = False

                    matched_faults += 1
                else:
                    missing_targets += 1

            if matched_faults == num_errors and shift_closure_ok and shift_prob_ok:
                shifts_verified += 1

            shift_stats.append({
                "shift": [a, b],
                "matched_faults": matched_faults,
                "closure_preserved": shift_closure_ok,
                "probability_preserved": shift_prob_ok,
            })

    total_checks = group_order * num_errors
    passed = (
        (shifts_verified == group_order)
        and (closure_violations == 0)
        and (probability_violations == 0)
        and (missing_targets == 0)
        and (num_orbits == 203)
        and all_orbits_size_36
    )

    elapsed = time.time() - t0

    results = {
        "verification": "Proposition 1 & 2: Automorphism Orbits and Group Closure",
        "parameters": {
            "code": "[[72, 12, 6]]",
            "group": "Z_6 x Z_6",
            "group_order": group_order,
            "rounds": rounds,
            "physical_p": error_rate,
            "total_fault_mechanisms": num_errors,
            "total_orbits": num_orbits,
            "compression_ratio": float(num_errors / num_orbits),
        },
        "orbit_statistics": {
            "all_orbits_size_36": all_orbits_size_36,
            "min_orbit_size": min_orbit_size,
            "max_orbit_size": max_orbit_size,
        },
        "group_action_verification": {
            "total_shifts_tested": group_order,
            "shifts_fully_verified": shifts_verified,
            "total_group_action_checks": total_checks,
            "closure_violations": closure_violations,
            "probability_invariance_violations": probability_violations,
            "missing_target_faults": missing_targets,
            "closure_rate_pct": float(100.0 * (1.0 - closure_violations / max(1, total_checks))),
        },
        "verification_status": "PASS" if passed else "FAIL",
        "elapsed_seconds": elapsed,
    }

    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Shifts verified: {shifts_verified}/{group_order}")
    print(f"Closure violations: {closure_violations}/{total_checks}")
    print(f"Probability violations: {probability_violations}/{total_checks}")
    print(f"Verification status: {results['verification_status']} (in {elapsed:.2f}s)")
    print(f"Saved results to {out_path}")
    return results


if __name__ == "__main__":
    verify_automorphism_orbits()
