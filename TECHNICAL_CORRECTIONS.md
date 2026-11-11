# Technical Corrections & Revision Plan

**Project:** Orbit-Tied Quantized Neural Belief Propagation (QNBP) for Bivariate-Bicycle Codes  
**Status:** Systematic Forensic Modifications  
**Target:** Publication-Grade Technical Rigor for IEEE TQE / Nature QI / PRX Quantum

---

## 1. Summary of Forensic Technical Corrections

| Phase | Technical Issue Identified | Pre-Audit Draft State | Post-Audit Corrected State | Verification Evidence |
| :---: | :--- | :--- | :--- | :--- |
| **Phase 2** | **Energy Unit Conversion** | Reported as $18.8\text{ pJ}$ (mean) / $44.2\text{ pJ}$ (worst-case). | Corrected to **$18.84\text{ nJ}$ (mean) / $44.16\text{ nJ}$ (worst-case)**. Normalized: $0.262\text{ nJ/qubit}$. | $P \times t = 0.184\text{ W} \times 102.4\text{ ns} = 18.8416\text{ nJ}$. |
| **Phase 3** | **Queue Latency Reconciliation** | Spliced $1760\text{ ns}$, $2000\text{ ns}$, and $950\text{ ns}$ arbitrarily to claim $\rho=0.23$. Claimed zero overflow guaranteed mathematically. | Reconciled: Sequential queue service time is $\mathbb{E}[S] = 669.4\text{ ns}$ ($\rho_{\text{seq}} = 0.67$); asynchronous fallback pool utilization is $\rho_{\text{fb}} = 0.23$ ($c=1$) / $0.12$ ($c=2$). Overflows bounded statistically by $6.0 \times 10^{-5}$ over 50,000 trace-driven shots ($B \ge 4$). | Trace-driven $D/G/c/B$ simulation in `results/gating_results.json`. |
| **Phase 4** | **CSS Sector Separation** | Stated that "effective error rate on the Z-sector approaches 0" under dephasing noise, conflating $Z$-errors with $Z$-checks. | Formulated Proposition 1: Physical $Z$-errors are detected by $X$-checks ($H_X = [A \mid B]$). Under high bias $\eta \to \infty$, syndrome excitation concentrates on $X$-checks, while $Z$-checks receive near-zero excitation. Stated that circuit-level two-qubit CNOT gates and $Y$-errors introduce cross-basis correlations. | CSS stabilizer commutation relations and DEM hyperedge analysis. |
| **Phase 5** | **DEM Automorphism Conditions** | Stated general automorphism theorem without specifying noise homogeneity conditions. | Explicitly conditioned Theorem 1 on spatially homogeneous gate noise. Stated that heterogeneous hardware noise preserves graph incidence while breaking exact prior invariance, motivating approximately equivariant weighting. | `tests/test_orbits.py` and `src/decoder/orbits.py` verification. |
| **Phase 6** | **Orbit Count Round Specification** | Stated 10,260 faults / 285 orbits on BB72 and 14,616 faults / 203 orbits on BB144 without round indices. | Specified: BB72 has 7,308 faults / 203 orbits for $R=3$ ($W=3$ window) and 10,260 faults / 285 orbits for $R=4$. BB144 has 14,616 faults / 203 orbits for $R=3$. Documented exact growth: $\Delta |\mathcal{O}| = 84$ orbits per round. | Computational sweep in `src/decoder/orbits.py` across $R=1\dots 5$. |
| **Phase 8** | **Quantization Dynamic Range Bound** | Outlined dynamic range $[-7.75, +7.75]$ without formal comparison to $B=4$ and $B=5$ bit-widths. | Added explicit headroom proof: $\delta_6 = 7.75 - \ln(999) = +0.8433 > 0$. Proved that $B=5$ truncates channel priors by $45.7\%$, and $B=4$ truncates by $74.7\%$, explaining the sharp threshold failure in Fig. 4. | Mathematical derivation and LSQ PyTorch quantization validation. |
| **Phase 9** | **Multiplier-Free RTL Framing** | Described RTL modules as implementing per-orbit neural weights without clarifying register structure. | Clarified: RTL modules `vnu.sv` and `cnu.sv` synthesize the canonical CSD kernel ($\alpha=0.75, \gamma=0.75$) with zero DSP multipliers, while the neural software model demonstrates that per-orbit learned variations within this CSD envelope yield the reported convergence speedups. | `rtl/vnu.sv`, `rtl/cnu.sv`, and `rtl/synth_results.json`. |
| **Phase 10** | **Macro-VNU Arithmetic Contradiction** | Stated $498 \times 48 = 23,904 + 216 \times 82 = 17,712 = 41,616\text{ LUTs}$, contradicting 28,204 total. | Reconciled: 216 VNUs ($10,368\text{ LUTs}$) + 216 CNUs ($17,712\text{ LUTs}$) + Gate $G_3$ ($124\text{ LUTs}$) = **$28,204\text{ LUTs}$** ($11.64\%$ of AMD XCKU040). | `rtl/synth_results.json` post-synthesis reports. |
| **Phase 11** | **Table I vs Table IV Clarification** | Table I reported $P_L = 0.0080$ at $\eta=1.0$, while Table IV reported $P_L = 0.0068$. | Clarified: Table I evaluated an earlier baseline checkpoint with fixed scalar damping $\gamma=0.35$ (6.8 mean iters), while Table IV evaluates the final model with fully trained signed per-orbit damping $\gamma \in [-0.5, 1.0]$ (6.4 mean iters). | `results/novelty_benchmarks.json` vs `results/competitor_benchmarks.json`. |
| **Phase 13** | **Confidence Gating Terminology** | Used "zero logical degradation" without empirical sample size qualification. | Replaced absolute claims with empirical bounds: $N=50,000$ test shots, zero false acceptances observed, establishing 95% Wilson fast-path upper bound of $7.68 \times 10^{-5}$ and end-to-end pipeline LER of $P_{\text{pipe}} = 1.90 \times 10^{-4}$. | 50,000-shot gating calibration in `results/gating_results.json`. |

---

## 2. Line-by-Line LaTeX Manuscript Modification Mapping

The following exact text and tabular modifications will be applied to `manuscript/main.tex`:

1. **Abstract (Page 1):**
   - Update energy from `18.8 pJ (mean) / 44.2 pJ` to `18.84 nJ (mean) / 44.16 nJ (0.26 nJ/qubit)`.
   - Clarify round depths for orbit collapse: `10,260 circuit fault mechanisms into 285 symmetry orbits (R=4) on [[72,12,6]] and 14,616 mechanisms into 203 orbits (R=3) on [[144,12,12]]`.
   - Update queue overflow framing to empirical Wilson bound: `driving queue overflow below 6.0 x 10^-5 (0 overflows observed in 50,000 test windows) under a 1 \mu s quantum cycle budget`.

2. **Section V-B (Page 6) — CSS Sector Proposition:**
   - Update Theorem 4 to Proposition 1, clarifying that physical $Z$ errors are detected by $X$-checks, and framing circuit-level cross-basis effects accurately.

3. **Section VI-D (Pages 7–8) — Queueing Analysis:**
   - Reconcile service time equations: explain sequential pipeline ($\mathbb{E}[S] = 669.4\text{ ns}, \rho = 0.67$) versus decoupled asynchronous fallback pool ($\rho_{\text{fb}} = 0.23$ for $c=1$, $0.12$ for $c=2$).
   - Report the finite-buffer 50,000-shot simulation results with confidence intervals.

4. **Section VII-A (Page 9) — Logic Reconciliation & Energy Units:**
   - Replace the `498 macro-VNUs` text with the true synthesis breakdown: `216 VNUs (10,368 LUTs) and 216 CNUs (17,712 LUTs), combined with Gate G3 (124 LUTs) yielding 28,204 LUTs`.
   - Update Table II: change energy column from `pJ` to `nJ`: `18.84 nJ (mean) / 44.16 nJ (worst-case)` and unit energies to `pJ/cycle`.

5. **Section VIII-A (Page 10) & Table IV:**
   - Ensure complete alignment between Table IV, Section VIII-A prose, and `results/competitor_benchmarks.json`.
   - Reiterate the distinction between the scalar damping baseline evaluated in Table I ($0.0080$) and the fully trained signed per-orbit damping model in Table IV ($0.0068$).

