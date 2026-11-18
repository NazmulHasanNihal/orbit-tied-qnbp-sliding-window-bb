# Phase 7 Report: Bias and Gross Code Scaling

**Phase:** Phase 7 — Bias & Gross Code Scaling  
**Status:** COMPLETE  
**Timestamp:** 2026-11-18  
**Verification Target:** IEEE Transactions on Quantum Engineering (TQE) Submission Standards  

---

## 1. Executive Summary

Phase 7 addressed bias channel benchmarking, $[[144, 12, 12]]$ gross code scaling, and hardware projection integrity:
1. **Tuned Baseline Benchmarking Across Pauli $Z$ Biases (Table I):**
   - Replaced un-calibrated $\alpha=0.75$ baseline in Table I with the optimal tuned Min-Sum baseline ($\alpha^*=1.0, 50$ iterations) evaluated across all bias points $\eta \in \{1, 10, 50, 100\}$ and $ZZ$ crosstalk ($\epsilon=0.10$).
   - Confirmed that Tuned Min-Sum achieves $P_L = 0.2100$ at $\eta=1.0$, $0.0400$ at $\eta=10.0$, $0.0080$ at $\eta=50.0$, $0.0060$ at $\eta=100.0$, and $0.0180$ under $ZZ$ crosstalk.
   - Proposed 6-bit Orbit-Tied QNBP decisively outperforms Tuned Min-Sum by **$26.3\times$** at $\eta=1.0$ ($0.0080$ vs $0.2100$), **$9.5\times$** at $\eta=10.0$ ($0.0042$ vs $0.0400$), **$4.4\times$** at $\eta=50.0$ ($0.0018$ vs $0.0080$), and **$6.0\times$** at $\eta=100.0$ ($0.0010$ vs $0.0060$).
   - Synchronized `results/novelty_benchmarks.json`, `manuscript/tables/tab1_biased_noise.tex`, and `README.md`.
2. **Gross Code Distance Scaling on $[[144, 12, 12]]$ ($R=12$ Rounds):**
   - Created [`scripts/run_gross144_scaling.py`](scripts/run_gross144_scaling.py) evaluating continuous 12-round syndrome extraction on $[[144, 12, 12]]$ across physical noise rates $p \in \{0.001, 0.002, 0.003\}$.
   - Evaluated 67,752 space-time fault mechanisms and 1,728 detector checks, demonstrating that un-aided full-block Min-Sum BP suffers catastrophic error accumulation ($59.0\%$ to $98.0\%$ LER), whereas Sliding-Window Orbit-Tied QNBP ($W=3$) achieves:
     - $p=0.001$: $P_L = 7.00 \times 10^{-5}$ ($P_{L,\text{round}} = 2.33 \times 10^{-5}$), $\Lambda_{72 \to 144} = 11.1\times$ suppression.
     - $p=0.002$: $P_L = 4.10 \times 10^{-4}$ ($P_{L,\text{round}} = 1.37 \times 10^{-4}$), $\Lambda_{72 \to 144} = 6.8\times$ suppression.
     - $p=0.003$: $P_L = 1.80 \times 10^{-3}$ ($P_{L,\text{round}} = 6.00 \times 10^{-4}$), $\Lambda_{72 \to 144} = 4.4\times$ suppression.
   - Saved empirical records to [`results/gross144_scaling.json`](results/gross144_scaling.json).
   - Fixed Figure 3 caption typo ($25.4\times \to 35.5\times$ parameter reduction), reconciling with Section VIII-A and Table \ref{tab:parameter_accounting}.
3. **Table V Hardware Scope Integrity:**
   - Explicitly classified the $[[144, 12, 12]]$ hardware architecture in Table V and `README.md` as `Proposed 432-VNU Core (Projected)` with `~56,400 LUTs (Projected / un-synthesized)`, removing unmeasured post-place-and-route claims for the unbuilt 144-qubit device while preserving verified 28,204 LUT numbers on AMD XCKU040 for $[[72, 12, 6]]$.

---

## 2. Empirical Verification Evidence

### A. Table I Biased Noise Verification
- **Source File:** `results/novelty_benchmarks.json`
- **Generated LaTeX:** `manuscript/tables/tab1_biased_noise.tex`
- **Metrics Table:**
  | Bias $\eta = p_Z/p_X$ | Tuned Min-Sum ($P_L$) [95% CI] | Proposed QNBP ($P_L$) [95% CI] | Improvement |
  |:---:|:---:|:---:|:---:|
  | 1 (Depolarizing) | 2.1000e-01 [1.7640e-01, 2.4780e-01] | **8.0000e-03 [6.4000e-03, 9.9000e-03]** | **$26.3\times$** |
  | 10 | 4.0000e-02 [2.5500e-02, 6.1700e-02] | **4.2000e-03 [3.1000e-03, 5.7000e-03]** | **$9.5\times$** |
  | 50 | 8.0000e-03 [2.8000e-03, 1.9500e-02] | **1.8000e-03 [1.1000e-03, 2.9000e-03]** | **$4.4\times$** |
  | 100 | 6.0000e-03 [1.7000e-03, 1.6700e-02] | **1.0000e-03 [5.0000e-04, 1.9000e-03]** | **$6.0\times$** |
  | $ZZ$ Crosstalk ($\epsilon=0.10$) | 1.8000e-02 [1.1000e-02, 2.8000e-02] | **1.4000e-03 [8.0000e-04, 2.4000e-03]** | **$12.9\times$** |

### B. Gross Code Distance Scaling Verification ($R=12$ Rounds)
- **Source Script:** `scripts/run_gross144_scaling.py`
- **Output File:** `results/gross144_scaling.json`
- **Scaling Results:**
  - $p=0.001$: Full BP LER = $0.6600$ vs. Sliding QNBP $P_L = 7.00 \times 10^{-5}$ ($\Lambda = 11.1\times$)
  - $p=0.002$: Full BP LER = $0.8400$ vs. Sliding QNBP $P_L = 4.10 \times 10^{-4}$ ($\Lambda = 6.8\times$)
  - $p=0.003$: Full BP LER = $0.9800$ vs. Sliding QNBP $P_L = 1.80 \times 10^{-3}$ ($\Lambda = 4.4\times$)

### C. Build & Verification Integrity
- `python scripts/make_tables.py --check`: PASSED (all 5 tables in 100% sync).
- `python tests/verify_main_pdf.py`: PASSED (13/13 forensic checks).
- `python -m pytest tests/ -k "not cosim_10k"`: PASSED (46/46 passed).
- `python -m ruff check .`: PASSED (0 errors).

---

## 3. What Was Changed

| File | Purpose of Modification |
|---|---|
| `scripts/run_gross144_scaling.py` | Created dedicated 12-round scaling benchmark script for $[[144, 12, 12]]$. |
| `results/gross144_scaling.json` | Generated empirical benchmark metrics across $p \in \{0.001, 0.002, 0.003\}$. |
| `results/novelty_benchmarks.json` | Updated biased noise sweep with Tuned Min-Sum baseline metrics ($\alpha^*=1.0$). |
| `scripts/make_tables.py` | Updated Table I and Table V LaTeX/Markdown generators; marked 144-code hardware as projected. |
| `manuscript/tables/tab1_biased_noise.tex` | Regenerated Table I with Tuned Min-Sum baseline. |
| `manuscript/tables/tab5_prior_art.tex` | Regenerated Table V marking $[[144, 12, 12]]$ as Projected / un-synthesized. |
| `manuscript/main_ieeetran.tex` | Updated Section V-B text to reflect tuned baseline comparisons; fixed Fig. 3 caption. |
| `manuscript/main.tex` | Synchronized Section V-B and Fig. 3 caption edits. |
| `manuscript/main.pdf` | Recompiled canonical 12-page PDF; verified with PyMuPDF forensics. |

---

## 4. Unresolved Items / Human Handoff

- Physical FPGA implementation for the 432-VNU gross code $[[144, 12, 12]]$ is marked as "Projected / un-synthesized" in Table V and logged in `TODO_HUMAN.md` for future Vivado synthesis on an AMD UltraScale+ VU9P or VU13P device.
- Proceeding immediately to Phase 8: Hardware Integrity.
