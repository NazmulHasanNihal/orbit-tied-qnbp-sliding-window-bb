# Forensic Change Log: Master Technical Revision

**Project:** Orbit-Tied Quantized Neural Belief Propagation (QNBP) for Bivariate-Bicycle Codes  
**Tracking Period:** Pre-Audit Baseline to Post-Audit Final Verified State  
**Verification Method:** Bit-exact simulation, Stim Monte Carlo validation, Vivado synthesis audit, and PyMuPDF PDF forensics

---

## [v2.0.0] - 2026-11-11: Master Technical Audit & Validation Upgrade

### 🔴 Critical Corrections Applied

#### 1. Hardware Dynamic Energy Units (Phase 2)
- **Before:** Reported as $18.8\text{ pJ}$ (mean early exit) and $44.2\text{ pJ}$ (worst case).
- **After:** Recalculated using $E = P \times t$:
  $$184\text{ mW} \times 102.4\text{ ns} = \mathbf{18.84\text{ nJ}} \quad (0.262\text{ nJ per data qubit})$$
  $$184\text{ mW} \times 240.0\text{ ns} = \mathbf{44.16\text{ nJ}} \quad (0.613\text{ nJ per data qubit})$$
- **Files Modified:** `manuscript/main.tex` (Abstract, Table II, Section VII-A), `tests/verify_main_pdf.py`, `HARDWARE_VALIDATION.md`.

#### 2. Macro-VNU Logic Count Reconciliation (Phase 10)
- **Before:** Section VII-A erroneously stated $498\text{ macro-VNUs} \times 48\text{ LUTs} = 23,904\text{ LUTs} + 17,712\text{ CNU LUTs} = 41,616\text{ LUTs}$, contradicting the synthesized total of 28,204 LUTs.
- **After:** Corrected to match `rtl/synth_results.json`:
  - 216 VNUs: $216 \times 48\text{ LUTs} = 10,368\text{ LUTs}$
  - 216 CNUs: $216 \times 82\text{ LUTs} = 17,712\text{ LUTs}$
  - Gate $G_3$ & interconnect: $124\text{ LUTs}$
  - Post-synthesis total: **28,204 LUTs** ($11.64\%$ of AMD XCKU040).
- **Files Modified:** `manuscript/main.tex` (Section VII-A), `HARDWARE_VALIDATION.md`, `AUDIT_REPORT.md`.

#### 3. Real-Time Queuing & Fallback Service Time Reconciliation (Phase 3)
- **Before:** Conflated sequential service times ($1760\text{ ns}$, $2000\text{ ns}$) with asynchronous fallback pool utilization ($950\text{ ns}$, $\rho = 0.23$). Claimed zero overflow as a mathematical certainty without finite-buffer distributional modeling.
- **After:**
  - Formulated both sequential pipeline ($\mathbb{E}[S] = 669.4\text{ ns}, \rho = 0.67$) and decoupled asynchronous pool ($\rho_{\text{fb}} = 0.23$ for $c=1$, $0.12$ for $c=2$).
  - Reframed buffer overflow as an empirical finite-buffer result: zero buffer overflows observed over 50,000 trace-driven windows for $B \ge 4$, establishing a 95% Wilson upper bound of $6.0 \times 10^{-5}$.
- **Files Modified:** `manuscript/main.tex` (Abstract, Section VI-D), `AUDIT_REPORT.md`, `EXPERIMENTAL_VALIDATION.md`.

#### 4. CSS Sector Separation & Dephasing Channel Concentration (Phase 4)
- **Before:** Theorem 4 asserted that "effective error rate on the Z-sector approaches 0" under dephasing bias, conflating $Z$-errors with $Z$-checks.
- **After:** Reformulated as Proposition 1: Physical $Z$-errors are detected exclusively by $X$-checks ($H_X = [A \mid B]$). Under high bias $\eta \to \infty$, syndrome excitation concentrates on $X$-checks while $Z$-checks receive near-zero excitation. Explicitly analyzed circuit-level CNOT hook errors and physical $Y$ faults.
- **Files Modified:** `manuscript/main.tex` (Section V-B), `MATHEMATICAL_VALIDATION.md`.

#### 5. Round Depth Indexing for DEM Fault Mechanisms (Phase 6)
- **Before:** Stated 10,260 faults / 285 orbits on BB72 and 14,616 faults / 203 orbits on BB144 without specifying round depth $R$.
- **After:** Specified round depths:
  - BB72: $R=3 \implies 7,308$ faults / 203 orbits; $R=4 \implies 10,260$ faults / 285 orbits ($36.0\times$ collapse).
  - BB144: $R=3 \implies 14,616$ faults / 203 orbits ($72.0\times$ collapse).
  - Proved the exact growth rate of 84 interior orbits ($84 \times |G|$ faults) per additional syndrome round.
- **Files Modified:** `manuscript/main.tex` (Abstract, Corollary 1), `MATHEMATICAL_VALIDATION.md`.

---

## 2. Documentation & Artifact Deliverables Generated

1. [`docs/AUDIT_REPORT.md`](docs/AUDIT_REPORT.md): Comprehensive 8-category forensic audit of all source files, raw data, and claims.
2. [`docs/TECHNICAL_CORRECTIONS.md`](docs/TECHNICAL_CORRECTIONS.md): Detailed mapping of pre-audit issues to corrected states.
3. [`docs/MATHEMATICAL_VALIDATION.md`](docs/MATHEMATICAL_VALIDATION.md): Complete theoretical derivations and proofs for Theorems 1–4, Proposition 1, and Corollary 1.
4. [`docs/EXPERIMENTAL_VALIDATION.md`](docs/EXPERIMENTAL_VALIDATION.md): Benchmark audit across 10 decoders, McNemar statistics, G3 calibration, and 60-round streaming tests.
5. [`docs/HARDWARE_VALIDATION.md`](docs/HARDWARE_VALIDATION.md): Energy re-calculation, logic synthesis breakdown, CSD arithmetic, and folding Pareto frontier.
6. [`docs/REPRODUCIBILITY_GUIDE.md`](docs/REPRODUCIBILITY_GUIDE.md): Step-by-step reproduction instructions for all tables, figures, and tests.
7. [`docs/FINAL_PUBLICATION_AUDIT.md`](docs/FINAL_PUBLICATION_AUDIT.md): 10-point scored publication-readiness audit.
8. [`docs/RESEARCH_PLAN.md`](docs/RESEARCH_PLAN.md): Monolithic research execution roadmap.

