# Phase 4 Report: Baselines Tuning & Authentic Competitor Reconciliation

**Timestamp:** 2026-11-18  
**Phase Status:** COMPLETE  
**Primary Goal:** Grid-tune Normalized Min-Sum parameters on held-out data, reconcile GDG Sliding Window single-window degeneracy, structure Table IV into latency-matched panels, and document short-cycle Tanner graph trapping mechanisms.

---

## 1. Executive Summary & What Changed

1. **Normalized Min-Sum Grid Tuning (`results/min_sum_tuning.json`):**
   - Executed a grid sweep over scaling factor $\alpha \in \{0.5, 0.625, 0.75, 0.875, 1.0\}$ and maximum iterations $I \in \{15, 30, 50\}$ across $N = 500$ held-out shots at $p = 0.003$ using `scripts/tune_min_sum.py`.
   - **Key Finding:** Standard unweighted Min-Sum ($\alpha^* = 1.0, I^* = 50$) achieves the lowest logical frame error rate ($P_L = 0.2220$ [0.1878, 0.2605], convergence rate 67.6%), whereas heuristic scaling $\alpha = 0.75$ degrades performance ($P_L = 0.4180$ [0.3756, 0.4617] at 50 iters; $P_L = 0.4320$ at 30 iters).
   - **Theoretical Explanation:** In classical LDPC codes with sparse, long-cycle Tanner graphs (girth $\ge 6$ or $8$), heuristic normalization $\alpha \approx 0.75$ counteracts check-to-variable over-estimation. However, bivariate-bicycle codes possess dense check degrees and many short girth-6 cycles. Uniform scalar attenuation $\alpha = 0.75$ attenuates valid syndrome messages prematurely across iterations, preventing the decoder from escaping symmetric trapping sets. In contrast, Proposed Orbit-Tied QNBP learns structured per-orbit scaling $\alpha_{o,t}$ and signed memory factors $\gamma_{o,t}$, achieving $P_L = 0.0068$.

2. **GDG Sliding Window Degeneracy Clarification:**
   - In Section VIII-A and the Table IV caption, explicitly stated:
     > *"GDG sliding window ($W=3, F=1$, without inter-window residual propagation) degenerates to standard Min-Sum on single-window benchmarks."*
   - Documented the role of inter-window residual propagation: it transmits boundary syndrome discrepancies across overlapping window frames $W$ with stride $F$ to resolve temporal boundary faults; when evaluated on an isolated window without inter-window residual propagation, the decoder reduces identically to single-window Normalized Min-Sum ($4,160 / 10,000$ errors, $P_L = 0.4160$ [0.4063, 0.4257]).

3. **Latency-Matched Table IV Restructuring (LaTeX & Markdown):**
   - Partitioned Table IV into two distinct panels in `manuscript/tables/tab4_competitor_benchmarks.tex`, `scripts/make_tables.py`, and `README.md`:
     - **Panel A: Real-Time Compatible Decoders ($t_{\text{dec}} \le 1.0\,\mu\text{s}$ Deadline):**
       - Proposed Orbit-Tied QNBP: 102.4 ns, $P_L = 0.0068$, DSP = 0
       - IBM Relay-BP (5-Leg Hardware-Capped): 454.4 ns, $P_L = 0.0090$, DSP = 0
       - Mem-BP: 120.0 ns, $P_L = 0.0102$, DSP = 0
       - IBM DMem-BP (Single-Leg): 147.2 ns, $P_L = 0.0160$, DSP = 0
       - A0 Classical Min-Sum ($\alpha=1.0$): 276.8 ns, $P_L = 0.2940$, DSP = 0
       - QNBP (Un-damped, $\gamma=0.0$): 163.2 ns, $P_L = 0.3100$, DSP = 0
       - A1 Normalized Min-Sum ($\alpha=0.75$): 308.8 ns, $P_L = 0.4160$, DSP = 0
       - GDG Sliding Window ($W=3, F=1$ isolated): 308.8 ns, $P_L = 0.4160$, DSP = 0
     - **Panel B: Budget-Exceeding Decoders ($t_{\text{dec}} > 1.0\,\mu\text{s}$, High Latency):**
       - IBM Relay-BP-5 (Full 300-Leg, S=5): $2,376\,\text{ns} = 2.38\,\mu\text{s}$ ($2.4\times$ budget), $P_L = 0.0060$
       - BP+OSD-CS-10: $320,000\,\text{ns} = 320\,\mu\text{s}$ ($320\times$ budget), $P_L = 0.0120$
       - BP-LSD (Localised Statistics, Order 5): $25,000\,\text{ns} = 25\,\mu\text{s}$ ($25\times$ budget), $P_L = 0.0340$
       - AutDEC (4 Torus Shifts): $4,800\,\text{ns} = 4.8\,\mu\text{s}$ ($4.8\times$ budget), $P_L = 0.4320$

4. **Manuscript Synchronization & Build:**
   - Synchronized `manuscript/main_ieeetran.tex` and `manuscript/main.tex`.
   - Regenerated `manuscript/main.pdf` via `scripts/compile_manuscript_pdf.py`.
   - Verified 13/13 PDF forensic audit checks in `tests/verify_main_pdf.py`.
   - Verified CI table synchronization via `python scripts/make_tables.py --check`.
   - Verified all unit and regression tests (40 passed, 3 deselected in 46.51s).

---

## 2. Empirical Verification Evidence

### Min-Sum Parameter Tuning Grid ($N=500$ held-out shots at $p=0.003$):
| $\alpha$ | Max Iters ($I$) | Errors / 500 | LER ($P_L$) [95% Wilson CI] | Convergence Rate | Mean Iterations | Time (s) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.500 | 15 | 176 / 500 | 0.3520 [0.3114, 0.3948] | 34.6% | 11.3 | 2.65s |
| 0.500 | 30 | 212 / 500 | 0.4240 [0.3814, 0.4677] | 35.8% | 21.4 | 4.80s |
| 0.500 | 50 | 209 / 500 | 0.4180 [0.3756, 0.4617] | 36.2% | 34.6 | 7.60s |
| 0.625 | 15 | 178 / 500 | 0.3560 [0.3153, 0.3989] | 37.0% | 11.0 | 3.37s |
| 0.625 | 30 | 228 / 500 | 0.4560 [0.4128, 0.4998] | 38.2% | 20.6 | 4.79s |
| 0.625 | 50 | 222 / 500 | 0.4440 [0.4010, 0.4878] | 39.0% | 33.2 | 7.02s |
| 0.750 | 15 | 177 / 500 | 0.3540 [0.3133, 0.3969] | 39.8% | 10.7 | 2.98s |
| 0.750 | 30 | 216 / 500 | 0.4320 [0.3893, 0.4758] | 42.6% | 19.7 | 4.17s |
| 0.750 | 50 | 209 / 500 | 0.4180 [0.3756, 0.4617] | 43.8% | 31.2 | 5.75s |
| 0.875 | 15 | 178 / 500 | 0.3560 [0.3153, 0.3989] | 41.0% | 10.9 | 2.59s |
| 0.875 | 30 | 183 / 500 | 0.3660 [0.3249, 0.4091] | 47.8% | 19.3 | 5.47s |
| 0.875 | 50 | 168 / 500 | 0.3360 [0.2960, 0.3785] | 53.8% | 29.3 | 8.61s |
| **1.000** | 15 | 179 / 500 | 0.3580 [0.3172, 0.4010] | 47.8% | 10.7 | 3.89s |
| **1.000** | 30 | 137 / 500 | 0.2740 [0.2367, 0.3147] | 61.0% | 17.6 | 5.89s |
| **1.000** | **50** | **111 / 500** | **0.2220 [0.1878, 0.2605]** | **67.6%** | **24.9** | **8.53s** |

---

## 3. Unresolved Items for Next Phase (Phase 5)

1. Measure empirical CPU software fallback latency distributions (mean, p50, p95, p99) over $\ge 200$ shots for BP+OSD and Relay-BP; save to `results/fallback_latency_distribution.json`.
2. Rewrite queue model in `scripts/evaluate_gating_and_queue.py` as a discrete-event simulation including window dependency ($s_{\text{res}}^{(k+1)}$ depends on committed correction $\hat{e}^{(k)}$) and rollback/reconciliation.
3. Model both policies: (A) speculative decode under fast-path correction, roll back if fallback differs; (B) pause stream during fallback.
4. Report queue stability threshold $p_{\text{crit}}$ where queue length diverges.
5. In Section VI-B, state clearly that real-time guarantees hold ONLY for the fast path; remove any claims of an unbuilt 950 ns FPGA fallback core.
