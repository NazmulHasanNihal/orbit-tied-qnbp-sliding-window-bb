# Phase 1 Report: Single Source of Truth & Table Pipeline

**Date:** 2026-11-18  
**Phase:** 1 — Single Source of Truth  
**Status:** Completed  
**Objective:** Eliminate hand-typed numbers and create an automated single-source-of-truth pipeline generating all manuscript and README tables from committed raw results in `results/` and `rtl/`.

---

## 1. What Changed

1. **Standardized JSON Schema (`src/orbit_tied_qnbp/utils/result_schema.py`)**:
   - Created `BenchmarkResultRecord` and `BenchmarkSuiteOutput` dataclasses enforcing standardized keys:
     - `code`: Quantum code identifier (e.g. `[[72,12,6]]`)
     - `rounds`: Syndrome measurement rounds
     - `p`: Physical noise rate
     - `bias`: Noise bias $\eta = p_Z / p_X$
     - `decoder`: Canonical decoder name
     - `config`: Dictionary of hyperparameters
     - `seed`: PRNG seed
     - `n_shots`: Total Monte Carlo shots evaluated
     - `n_errors`: Total observed logical errors
     - `n_accepted`: Windows admitted to fast path
     - `n_fallback`: Windows routed to fallback path
     - `iterations_histogram`: Distribution of iteration counts
     - `wall_time`: Total evaluation wall time
     - `git_commit`: Repository commit hash at execution

2. **Automated Table Generation Script (`scripts/make_tables.py`)**:
   - Implemented an automated parser and formatter that reads:
     - `results/novelty_benchmarks.json`
     - `rtl/synth_results.json`
     - `results/hardware_folding_results.json`
     - `results/competitor_benchmarks.json`
   - Generates 5 canonical LaTeX table fragments in `manuscript/tables/`:
     - `tab1_biased_noise.tex`: Table I (Biased Noise & Crosstalk)
     - `tab2_hardware_synth.tex`: Table II (FPGA Logic & Synthesis)
     - `tab3_hardware_folding.tex`: Table III (Hardware Folding Pareto Frontier)
     - `tab4_competitor_benchmarks.tex`: Table IV (Master Competitor Benchmarks)
     - `tab5_prior_art.tex`: Table V (Prior Art Hardware Comparison)
   - Injects synchronized Markdown tables directly into `README.md` between sentinel markers (`<!-- BEGIN_TABLE_X -->` ... `<!-- END_TABLE_X -->`).
   - Implements a strict `--check` mode for CI pipelines, failing with exit code 1 if any generated table or README section differs from disk.

3. **LaTeX Source Synchronization (`manuscript/main_ieeetran.tex` and `manuscript/main.tex`)**:
   - Replaced all hand-typed inline `\begin{table}` / `\begin{table*}` blocks with modular `\input{tables/...}` directives:
     - Table I: `\input{tables/tab1_biased_noise.tex}`
     - Table II: `\input{tables/tab2_hardware_synth.tex}`
     - Table III: `\input{tables/tab3_hardware_folding.tex}`
     - Table IV: `\input{tables/tab4_competitor_benchmarks.tex}`
     - Table V: `\input{tables/tab5_prior_art.tex}`
   - Synchronized `manuscript/main.tex` to maintain byte-level parity with `main_ieeetran.tex`.

4. **CI Pipeline Integration (`.github/workflows/ci.yml`)**:
   - Added a mandatory validation step to the GitHub Actions workflow:
     ```yaml
     - name: Verify Single-Source-of-Truth Tables
       run: |
         python scripts/make_tables.py --check
     ```
   - Guarantees that any PR or commit with out-of-sync or hand-edited numbers will fail CI immediately.

5. **Smoke Test Mode (`scripts/run_competitor_benchmarks.py`)**:
   - Added `--smoke` command-line flag running 20 shots per decoder, allowing rapid local testing and CI execution within seconds.

---

## 2. Verification Evidence

1. **Table Generation Execution**:
   ```
   > python scripts/make_tables.py
   ✅ Generated: manuscript/tables/tab1_biased_noise.tex
   ✅ Generated: manuscript/tables/tab2_hardware_synth.tex
   ✅ Generated: manuscript/tables/tab3_hardware_folding.tex
   ✅ Generated: manuscript/tables/tab4_competitor_benchmarks.tex
   ✅ Generated: manuscript/tables/tab5_prior_art.tex
   ✅ Updated: README.md tables
   🎉 Single-source-of-truth table generation complete!
   ```

2. **CI Check Mode Verification**:
   ```
   > python scripts/make_tables.py --check
   🔍 CI Check Mode: Verifying all generated tables match disk...
   ✅ Verified: manuscript/tables/tab1_biased_noise.tex
   ✅ Verified: manuscript/tables/tab2_hardware_synth.tex
   ✅ Verified: manuscript/tables/tab3_hardware_folding.tex
   ✅ Verified: manuscript/tables/tab4_competitor_benchmarks.tex
   ✅ Verified: manuscript/tables/tab5_prior_art.tex
   ✅ Verified: README.md tables
   ✅ All tables are in 100% sync with results/!
   ```

3. **Forensic PDF Audit**:
   - Re-verified `python tests/verify_main_pdf.py`: All 13 checks pass cleanly (100% zero-defect).

---

## 3. Unresolved Items / Next Phase

- **Pipeline Error Contradiction (Phase 2)**:
  - While single-source generation is now enforced, the raw values in `results/gating_results.json` and claims in text still contain the mixed-operating-point contradiction:
    - At $p=0.003$, $P_{\text{pipe}} = 1.90 \times 10^{-3}$ ($p_{\text{fb}} = 0.244$).
    - At $p=0.001$, $P_{\text{pipe}} = 7.00 \times 10^{-6}$ ($p_{\text{fb}} = 0.009$).
  - Moving immediately to Phase 2 to resolve the math, raw data, text, and tables.
