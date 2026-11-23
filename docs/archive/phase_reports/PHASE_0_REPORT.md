# PHASE_0_REPORT.md — Full Forensic Audit Report

> **Phase:** PHASE 0 — Comprehensive Forensic Audit  
> **Date:** November 18, 2026  
> **Auditor Roles:** Senior QEC Decoder Researcher + FPGA Engineer + Paper Editor  
> **Status:** COMPLETE — Ready to proceed to Phase 1.

---

## 1. What Changed in Phase 0

In strict compliance with the Phase 0 instruction (*"Do not change anything yet except creating the ledger"*):
1. **Zero modifications** were made to existing source code, LaTeX text, RTL, test suites, or raw benchmark data.
2. Created [`CLAIMS_LEDGER.md`](CLAIMS_LEDGER.md): A comprehensive 76-claim audit matrix tracking every numeric statement across the Abstract, Sections I–IX, Tables I–V, Figures 1–7, README, and technical whitepapers.
3. Created [`TODO_HUMAN.md`](TODO_HUMAN.md): Explicitly cataloged all external dependencies requiring specialized compute (Vivado place-and-route, physical FPGA boards, multi-core cluster scaling) with exact Tcl and Bash scripts.

---

## 2. Forensic Evidence of Identified Deficiencies

### A. Real-Time Pipeline Error Mismatch (10× Discrepancy)
- **Claimed in Abstract, Table V, Fig. 1, and README:** $P_{\text{pipe}} = 1.90 \times 10^{-4}$ at $p = 0.003$ ($102.4\text{ ns}$ mean latency).
- **Mathematical Reality:**
  At $p = 0.003$, Gate $G_3$ ($\tau = 1.5$) achieves acceptance rate $P_{\text{accept}} = 0.756 \implies p_{\text{fb}} = 0.244$.
  Even if $P(\text{err} \mid \text{accepted}) = 0.0$ and fallback error rate is $P(\text{err} \mid \text{fallback}) = 0.0078$:
  $$P_{\text{pipe}} = (1 - p_{\text{fb}}) \cdot 0 + p_{\text{fb}} \cdot P(\text{err} \mid \text{fallback}) = 0.244 \times 0.0078 = 1.9032 \times 10^{-3}$$
- **Root Cause:** $1.90 \times 10^{-4}$ was carried over from preliminary low-noise ($p = 0.001$) screening runs without recalculating for $p = 0.003$.

### B. Mixed Operating Points & Unverified Zero-Error Bound
- In `results/gating_results.json`, the gating calibration was performed at `physical_p: 0.001` over $N = 50,000$ shots, where fast path errors were 0 and slow path errors were 1.
- In the manuscript text, this $75.6\%$ acceptance rate was attributed to $p = 0.003$.
- The 95% Wilson upper bound on zero error was quoted as $7.68 \times 10^{-5}$, which was calculated using total shots $N = 50,000$ rather than accepted shots $N_{\text{acc}} = 37,800$.

### C. Table IV Duplicate Baseline ("GDG Sliding Window")
- In Table IV, `A1 Normalized Min-Sum` and `GDG Sliding Window` have identical error counts ($4,160 / 10,000$), identical LER ($0.4160$), identical Wilson CIs ($[0.4063, 0.4257]$), identical mean iterations ($19.3$), and identical $\chi^2 = 2,642.1$.
- Forensic inspection of `scripts/run_competitor_benchmarks.py` revealed:
  ```python
  "A1_Normalized_MinSum": (FastBpBaselineDecoder(graph=graph, max_iter=30, alpha=0.75), 0),
  # ...
  "GDG_Sliding_Window": (FastBpBaselineDecoder(graph=graph, max_iter=30, alpha=0.75), 0),
  ```
  Both rows literally instantiated the identical object. Gong et al.'s guided decimation sliding window algorithm was never implemented.

### D. Normalized Min-Sum Sub-Optimality ($0.4160$ vs. $0.2940$)
- Classical unweighted Min-Sum ($\alpha=1.0$) achieved $P_L = 0.2940$.
- Normalized Min-Sum ($\alpha=0.75$) performed substantially worse ($P_L = 0.4160$), indicating an untuned damping factor and lack of iteration convergence optimization on this dense Tanner graph.

### E. Severe Statistical Sample Size Deficits
- **IBM Heron Calibration:** `results/realworld_benchmarks.json` lists `shots: 250`. In 250 shots, exactly 1 error occurred per decoder ($P_L = 0.0040$), resulting in a massive 95% Wilson confidence interval $[0.0007, 0.0223]$ that spans 30-fold.
- **100-Round Continuous Streaming Survival:** Evaluated over only 10 shots (`shots_evaluated: 10`). Survival percentages ($98.12\%$) are analytical powers $(1 - P_{\text{round}})^{100}$ from unverified per-window rates.
- **Gross Code $[[144,12,12]]$:** Tested at only $p=0.003$ with $N=1,000$ shots (yielding 2 errors). The other 3 noise points ($p \in \{0.001, 0.002, 0.005\}$) and the $\Lambda = 11.2\times$ suppression factor cited in Section VIII-C are completely absent from committed raw JSON files.

### F. Hardware RTL Synthesis vs. Analytical Spreadsheet
- In `rtl/synth_results.json`, the 28,204 LUT figure is derived by simple scalar summation:
  $$216 \times 48\text{ (VNU)} + 216 \times 82\text{ (CNU)} + 124\text{ (G3)} = 28,204\text{ LUTs}$$
- It does not account for top-level interconnect multiplexing or routing fabric.
- Timing ($\text{WNS} = +0.18\text{ ns}$ at $250\text{ MHz}$) and dynamic power ($184\text{ mW}$) are unverified estimates without Vivado implementation reports.
- No RTL exists for the "203-orbit full-DEM" core ($31,800$ LUTs) or the gross code ($58,400$ LUTs).

### G. Co-Simulation Parity Reality
- `tests/test_hardware_cosim_10k.py` is pure Python executing integer arithmetic; neither Verilator, Icarus Verilog, nor Vivado XSim was invoked.

### H. Citation Integrity Bugs
- Reference [53] (`li2024high` / Sahay et al. 2024) is a paper on neutral-atom qubits with biased erasures, erroneously cited for superconducting transmon dephasing noise.
- References [24] and [25] are classical LDPC/OSD papers.

---

## 3. What is Still Unresolved (Roadmap for Phases 1–12)

| Phase | Core Objective | Key Deliverables |
|---|---|---|
| **Phase 1** | Single Source of Truth | Create `scripts/make_tables.py` generating LaTeX & README tables from raw JSON; standardize schema; add CI diff check. |
| **Phase 2** | Fix Pipeline Contradiction | Recompute $P_{\text{pipe}}$ at $p=0.003$ ($1.90 \times 10^{-3}$) and $p=0.001$ ($7.00 \times 10^{-6}$); re-derive zero-event bounds on accepted shots ($N_{\text{acc}}$); eliminate operating point mixing. |
| **Phase 3** | Statistical Power | Run high-statistics simulations via Stim/sinter; compute exact Clopper-Pearson bounds and exact McNemar binomial tests. |
| **Phase 4** | Baselines Tuning & Truth | Tune $\alpha \in [0.5, 1.0]$ for Normalized Min-Sum; run official IBM Relay-BP settings; remove GDG duplicate row or implement authentic guided decimation; build matched-budget comparison. |
| **Phase 5** | Fallback & Queue Simulation | Measure real empirical fallback latency distributions on CPU; rewrite queue simulator with inter-window residual dependency and rollback; remove imaginary 950 ns FPGA fallback core if not built. |
| **Phase 6** | Quantization & Theory Proofs | Empirically verify prior LLR histograms and saturation stats; formalize proofs of Proposition 1 and Proposition 2 with automated symmetry pytest. |
| **Phase 7** | Bias & Gross Code Scaling | Separate channel difficulty from decoder adaptation across $\eta \in [1, 100]$; obtain real multi-point data for $[[144,12,12]]$ with $\ge 100$ errors or upper bounds. |
| **Phase 8** | Hardware Integrity | Label hardware numbers as estimated; write Vivado Tcl scripts to `TODO_HUMAN.md`; report software reference model matching RTL. |
| **Phase 9** | Literature & Citation Fixes | Verify all 59 references via web search/DOI; replace neutral-atom ref [53]; add Positioning table and Limitations section. |
| **Phase 10**| Manuscript Polish | Real IEEEtran two-column format; abstract $\le 200$ words with only verified numbers; remove hype wording. |
| **Phase 11**| Repo Hygiene | Clean README badges (remove unverified DOI/PyPI/test count badges); add Makefile with smoke and full reproduction targets. |
| **Phase 12**| Independent Verification | Re-derive every number in final paper from `results/`; output `FINAL_VERIFICATION.md` and `REVIEWER_RISKS.md`. |

---

## 4. Conclusion & Next Step

Phase 0 is complete. We now proceed immediately to **PHASE 1 — SINGLE SOURCE OF TRUTH**.
