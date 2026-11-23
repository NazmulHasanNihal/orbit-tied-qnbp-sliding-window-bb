# Phase 3 Report: Statistical Power & Exact McNemar Testing

**Date:** 2026-11-18  
**Phase:** 3 — Statistical Power & Exact McNemar  
**Status:** Completed  
**Objective:** Provide rigorous statistical hypothesis testing between paired decoders, implementing exact binomial tests for small sample sizes ($b+c < 25$), reporting discordant counts ($b, c$), and formalizing high-statistics compute plans in `TODO_HUMAN.md`.

---

## 1. What Changed

1. **Exact Binomial & Asymptotic McNemar Testing (`src/orbit_tied_qnbp/utils/metrics.py`)**:
   - Implemented `mcnemar_test_detailed(outcomes_a, outcomes_b)`:
     - Calculates discordant pairs:
       - $b$: Decoder A succeeded ($0$) while Decoder B failed ($1$)
       - $c$: Decoder A failed ($1$) while Decoder B succeeded ($0$)
     - When $b+c < 25$: Computes exact two-tailed binomial p-value under $H_0: p = 0.5$:
       $$p = 2 \times \sum_{k=0}^{\min(b,c)} \binom{b+c}{k} 0.5^{b+c}$$
     - When $b+c \ge 25$: Evaluates the Edwards continuity-corrected $\chi^2$ statistic with 1 degree of freedom:
       $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c}, \quad p = 1 - F_{\chi^2_1}(\chi^2)$$
     - Returns a structured dictionary reporting `statistic`, `p_value`, `b`, `c`, and `method`.
   - Maintained full backwards compatibility for `mcnemar_paired_test` returning `(statistic, p_value)`.

2. **Automated Unit Testing (`tests/test_metrics.py`)**:
   - Added unit tests verifying:
     - Wilson score interval behavior at zero errors ($N = 37,800 \implies [0.0, 1.016 \times 10^{-4}]$) and typical error rates ($100 / 10,000$).
     - Exact binomial McNemar p-value calculations for small discordant counts ($b=10, c=0 \implies p = 0.001953$).
     - Asymptotic $\chi^2$ calculations for large discordant counts ($b=50, c=10 \implies \chi^2 = 25.35, p < 10^{-6}$).
     - Identity handling for concordant pairs ($b=c=0 \implies \chi^2 = 0.0, p = 1.0$).
     - Confidence interval formatting utility (`format_ci_metric`).

3. **High-Statistics Sampling Specifications in `TODO_HUMAN.md`**:
   - Documented external compute requirements for high-statistics Monte Carlo sampling:
     - $N \ge 10^5$ shots for $p = 0.003$ competitor benchmarks to narrow the Wilson interval to $\pm 0.0005$.
     - $N \ge 10^5$ shots for the empirical IBM Heron r2 calibration profile to observe $\ge 100$ failure events per decoder (resolving the current $N = 250$ shot exploratory sample).
     - Gross code $[[144, 12, 12]]$ scaling with $\ge 100$ failure events per noise point ($p \in \{0.001, 0.002, 0.003, 0.005\}$).
   - Specified exact Python CLI execution script:
     `python scripts/run_high_statistics_benchmarks.py --shots 1000000 --workers 16`
   - Established strict reporting rule: Any cell with zero observed events must report the exact Clopper-Pearson 95% upper bound $1 - (0.05)^{1/N}$.

---

## 2. Verification Evidence

- Executed `tests/test_metrics.py` verifying exact mathematical parity between theoretical binomial distributions and implementation.
- All checks pass.
