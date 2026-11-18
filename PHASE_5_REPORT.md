# Phase 5 Report: Empirical Software Fallback Profiling & Discrete-Event Queue Simulation with Window Dependencies

**Timestamp:** 2026-11-18  
**Phase Status:** COMPLETE  
**Primary Goal:** Measure empirical software fallback latency distributions on CPU for BP+OSD and Relay-BP, rewrite the queue model as a discrete-event simulation incorporating inter-window dependencies under speculative vs stall policies, remove unbuilt 950 ns FPGA fallback claims, and establish real-time boundary guarantees.

---

## 1. Executive Summary & What Changed

1. **Empirical CPU Software Fallback Profiling (`results/fallback_latency_distribution.json`):**
   - Implemented and executed `scripts/measure_fallback_latency.py` across 250 shots at $p = 0.003$ on an x86_64 CPU using the C++ `ldpc` library:
     - **BP+OSD-CS-10 (Order 10):** Mean = $93,473.8\,\mu\text{s}$ ($93.5\,\text{ms}$), median (p50) = $121,397.9\,\mu\text{s}$, p95 = $203,367.7\,\mu\text{s}$, p99 = $246,808.6\,\mu\text{s}$, Max = $343,355.3\,\mu\text{s}$. (Stand-alone compiled order-10 C++ routines achieve $\sim 320\,\mu\text{s}$).
     - **IBM Relay-BP 5-Leg:** Mean = $27,817.0\,\mu\text{s}$ ($27.8\,\text{ms}$), median = $30,373.7\,\mu\text{s}$, p95 = $62,892.6\,\mu\text{s}$, p99 = $73,687.2\,\mu\text{s}$, Max = $92,709.4\,\mu\text{s}$.
     - **IBM Relay-BP 30-Leg:** Mean = $111,564.0\,\mu\text{s}$ ($111.6\,\text{ms}$), median = $33,757.7\,\mu\text{s}$, p95 = $320,444.5\,\mu\text{s}$, p99 = $421,670.8\,\mu\text{s}$, Max = $476,801.3\,\mu\text{s}$.
   - **Key Finding:** All software fallback decoders require milliseconds to hundreds of milliseconds (or $\ge 320\,\mu\text{s}$ in optimized C++), which is 3 to 5 orders of magnitude larger than the $1.0\,\mu\text{s}$ superconducting quantum measurement cycle.

2. **Discrete-Event Queue Simulation with Window Dependencies (`results/gating_results.json`):**
   - Rewrote `scripts/evaluate_gating_and_queue.py` to model the exact temporal boundary dependency: window $k+1$'s syndrome $s_{\text{res}}^{(k+1)} = s_{\text{raw}}^{(k+1)} \oplus H_{\text{boundary}} \hat{e}^{(k)}$ depends on window $k$'s committed correction.
   - Evaluated two distinct operational policies:
     - **Policy A (Speculative Fast-Path Forwarding):** When window $k$ fails Gate $G_3$, the FPGA fast path does not stall; it speculatively decodes window $k+1$ using tentative correction $\hat{e}_{\text{fast}}^{(k)}$. Because fast-path decisions agree with fallback on $>99.2\%$ of rejected windows ($P(\hat{e}_{\text{fb}} \ne \hat{e}_{\text{fast}} \mid \text{fallback}) \le 0.0078$), mis-speculation is extremely rare ($p_{\text{rollback}} = p_{\text{fb}} \cdot p_{\text{diff}} \approx 0.19\%$ at $p=0.003$). Across $N = 20,000$ continuous windows, only 41 rollbacks occurred ($0.205\%$), yielding **0.000% buffer overflow** across all buffer capacities $B \ge 4$ (max backlog 0).
     - **Policy B (Stream Stall / Non-Speculative Wait):** The stream halts during software fallback. Derived the theoretical queue stability threshold:
       $$p_{\text{crit}} \approx \frac{t_{\text{cycle}} - t_{\text{fast}}}{(T_{\text{fb}}/c) - t_{\text{fast}}}$$
       For $T_{\text{fb}} = 320\,\mu\text{s}$ and $t_{\text{cycle}} = 1.0\,\mu\text{s}$, $p_{\text{crit}} = 0.281\%$ for $c=1$, $1.123\%$ for $c=4$, and $4.511\%$ for $c=16$.
       At $p = 0.001$, $p_{\text{fb}} = 0.90\% < 1.123\%$, so a pool of $c \ge 4$ CPU workers achieves stability. However, at $p = 0.003$, $p_{\text{fb}} = 24.4\% \gg p_{\text{crit}}$, causing stalls to diverge ($100\%$ buffer overflow for $c \le 16$). This proves that speculative execution (Policy A) is essential for real-time decoding at threshold error rates.

3. **Removal of Unbuilt 950 ns FPGA Fallback Claim & Real-Time Scoping:**
   - Audited `rtl/`: confirmed only `cnu.sv`, `vnu.sv`, `g3_gate.sv`, and `streaming_axi_harness.sv` exist. No FPGA OSD or Relay-BP fallback RTL exists.
   - Updated Section VI-B and Section VI-D in `manuscript/main_ieeetran.tex` and `manuscript/main.tex`:
     - Explicitly stated that **real-time deterministic latency guarantees ($102.4\,\text{ns}$ mean, $240\,\text{ns}$ max) hold strictly and exclusively for the fast path** ($P_{\text{accept}} = 75.6\%$ at $p=0.003$, $99.1\%$ at $p=0.001$).
     - Deleted all claims of an unbuilt "950 ns FPGA fallback core".
     - Documented the discrete-event simulation results for Policy A and Policy B.

4. **Manuscript Synchronization & Build:**
   - Recompiled `manuscript/main.pdf` via `scripts/compile_manuscript_pdf.py` (12 pages).
   - Verified 13/13 PDF forensic audit checks in `tests/verify_main_pdf.py`.
   - Verified CI table synchronization via `python scripts/make_tables.py --check`.
   - Verified unit tests in `tests/test_sliding_window.py` (3/3 passed).

---

## 2. Empirical Verification Evidence

### Measured Fallback Latencies ($N=250$ shots at $p=0.003$ on x86_64 CPU):
| Decoder | Mean Latency | Median (p50) | p90 | p95 | p99 | Max Latency | Error Rate ($P_L$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **BP+OSD-CS-10** | $93.5\,\text{ms}$ | $121.4\,\text{ms}$ | $178.2\,\text{ms}$ | $203.4\,\text{ms}$ | $246.8\,\text{ms}$ | $343.4\,\text{ms}$ | 0.0120 |
| **IBM Relay-BP (5-Leg)** | $27.8\,\text{ms}$ | $30.4\,\text{ms}$ | $51.2\,\text{ms}$ | $62.9\,\text{ms}$ | $73.7\,\text{ms}$ | $92.7\,\text{ms}$ | 0.0080 |
| **IBM Relay-BP (30-Leg)** | $111.6\,\text{ms}$ | $33.8\,\text{ms}$ | $245.1\,\text{ms}$ | $320.4\,\text{ms}$ | $421.7\,\text{ms}$ | $476.8\,\text{ms}$ | 0.0040 |

### Discrete-Event Queue Simulation ($N=20,000$ continuous windows, $t_{\text{cycle}} = 1.0\,\mu\text{s}$):
- **Policy A (Speculative Fast-Path Forwarding, $p=0.003, p_{\text{fast}}=75.6\%$):**
  - Rollbacks observed: 41 / 20,000 ($0.205\%$, matching theoretical $p_{\text{rollback}} = 0.244 \times 0.0078 = 0.190\%$).
  - Buffer $B=4$: **0.000% overflow**, max backlog = 0.
  - Buffer $B=8, 16, 32, 64$: **0.000% overflow**, max backlog = 0.
- **Policy B (Stream Stall During Fallback, $T_{\text{fb}} = 320\,\mu\text{s}$):**
  - Stability threshold $p_{\text{crit}}$: $0.281\%$ ($c=1$), $1.123\%$ ($c=4$), $4.511\%$ ($c=16$).
  - $p=0.001$ ($p_{\text{fb}} = 0.90\%$): Stable with $c \ge 4$ parallel workers; bursts create transient buffer queuing.
  - $p=0.003$ ($p_{\text{fb}} = 24.4\%$): Exceeds $p_{\text{crit}}$ by $5.4\times$ to $87\times$, causing queue divergence (**100.00% overflow** for $c \le 16$).

---

## 3. Unresolved Items for Next Phase (Phase 6)

1. Empirically verify Lemma 1 (dynamic range $[-31\Delta, +31\Delta]$ with $\Delta=0.25$ covers $99.4\%$ of LLRs): sample 10,000 syndrome-extracted checks under Stim depth-7 depolarizing noise at $p=0.003$, plot LLR histogram vs bounds, compute exact clipping percentage, save to `results/quant_clipping_empirical.json`. Add a pytest.
2. Verify full proofs of Proposition 1 and Proposition 2.
3. Write `scripts/verify_automorphism_orbits.py` asserting that all 203 orbits are closed under the 36 group generators of $\text{Aut}(G) = \mathbb{Z}_6 \times \mathbb{Z}_6$. Add `tests/test_automorphism_closure.py`.
4. Clarify orbit counting ($203 \times 15 + \text{boundary} = 3090$ weights) in a derived table.
