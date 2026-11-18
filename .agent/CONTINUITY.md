# 🌀 Continuity Status (5-Gate OpenSpec & Q1 Research Workflow)

**Project:** Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes  
**Current Task:** 13-Phase Systematic Audit, Reproducibility Engine & Reviewer-Proofing (Phases 0–12 Complete)  
**Current Gate:** GATE 5 — VERIFIED & SUBMISSION-READY (Strictly 1 Canonical Deliverable: `manuscript/main.pdf`)  
**Authors & Specific Roles:**  
1. **Md. Nazmul** (Lead & Corresponding Author, `nazmulhas36@gmail.com`, ORCID: `0009-0001-6115-7023`)  
2. **Musrat Jahan Gungun** (Co-Author, `gungunjahan84@gmail.com`, ORCID: `0009-0006-4249-9198`)  
3. **Maheli Ahmed** (Co-Author & Supervisor, `maheli.ahmed.cse.cot@gmail.com`, ORCID: `0000-0002-5183-7498`)  
**Affiliation:** Department of Computer Science and Engineering, College of Technology, National University, Gazipur-1704, Bangladesh  
**Status:** All 13 Phases (Phase 0 through Phase 12) fully completed and verified. 39/39 automated claims verified against committed results JSON (100.0%), 46/46 pytest unit/integration tests passed, 13/13 PDF forensic audit checks passed (exactly 12 pages, IEEE Transactions format), 0 ruff errors.

---

## 📅 Action Log & Deliverables Status

1. **Phase 0 (Claims Ledger Audit):** Created `CLAIMS_LEDGER.md` auditing all 76 numeric claims across paper, README, and results. Created `TODO_HUMAN.md` for external hardware/cluster instructions. Produced `PHASE_0_REPORT.md`.
2. **Phase 1 (Single Source of Truth):** Created `src/orbit_tied_qnbp/utils/result_schema.py` and `scripts/make_tables.py` auto-generating LaTeX tables `tab1` through `tab5` and README tables with `--check` diff enforcement. Produced `PHASE_1_REPORT.md`.
3. **Phase 2 (Pipeline Error Unmixing):** Recomputed raw syndrome counts: $P_{\text{pipe}} = 1.90\times 10^{-3}$ at $p=0.003$ vs $7.00\times 10^{-6}$ at $p=0.001$. Bounded zero accepted errors ($N_{\text{acc}}=37,800$) to exact Clopper-Pearson $7.92\times 10^{-5}$ and Wilson $1.02\times 10^{-4}$. Produced `PHASE_2_REPORT.md`.
4. **Phase 3 (Statistical Rigor & McNemar):** Implemented exact binomial and continuity-corrected asymptotic McNemar test in `src/orbit_tied_qnbp/utils/metrics.py`. Verified in `tests/test_metrics.py`. Produced `PHASE_3_REPORT.md`.
5. **Phase 4 (Min-Sum Tuning & Table IV Panels):** Grid-tuned Min-Sum ($\alpha^*=1.0, 50$ iters, $P_L=0.2220$ vs. degraded $\alpha=0.75, P_L=0.4180$). Formatted Table IV into Panel A (Real-Time, $\le 1.0\,\mu\text{s}$) and Panel B (Budget-Exceeding, $>1.0\,\mu\text{s}$). Produced `PHASE_4_REPORT.md`.
6. **Phase 5 (Fallback Empirical Latency & Queue Stability):** Benchmarked CPU fallback latency distributions (BP+OSD mean 93.5 ms, Relay-BP 5-leg mean 27.8 ms). Modeled discrete-event queue with window boundary dependency and speculative fast path ($0.205\%$ mis-speculation rollback, $0.00\%$ buffer overflow for $B \ge 4$). Produced `PHASE_5_REPORT.md`.
7. **Phase 6 (Quantization Dynamic Range & Theory Proofs):** Verified Lemma 1 dyadic pre-scaling $\kappa = 0.75 = 1 - 2^{-2}$ across 10k shots ($73,080,000$ evals) with 100.0000% coverage, 0.0000% clipping, $\delta=1.3633$ headroom. Formally proved Proposition 2 (equivariance and fixed-point preservation) and Proposition 3 (effective dephasing concentration). Documented torus automorphism closure across 263,088 checks (0 violations) and parameter accounting (3,090 vs 109,620 weights, $35.5\times$ collapse). Produced `PHASE_6_REPORT.md`.
8. **Phase 7 (Bias & Gross Code Scaling):** Evaluated Tuned Min-Sum baseline in Table I across $\eta \in \{1, 10, 50, 100\}$. Evaluated $[[144, 12, 12]]$ 12-round scaling across $p \in \{0.001, 0.002, 0.003\}$ ($\Lambda = 11.1\times, 6.8\times, 4.4\times$). Updated Table V marking $[[144, 12, 12]]$ as Projected / un-synthesized ($\sim$56,400 LUTs). Produced `PHASE_7_REPORT.md`.
9. **Phase 8 (Hardware Integrity & Synthesis Scoping):** Re-framed 28,204 LUTs as module-sizing synthesis estimates ($216 \times 48\text{ VNU} + 216 \times 82\text{ CNU} + 124\text{ gate} = 28,204\text{ LUTs}$, 0 DSP, 0 BRAM). Replaced unverified WNS slack and power measurements with analytical models ($250\text{ MHz}$, $\sim 184\text{ mW}$). Produced `PHASE_8_REPORT.md`.
10. **Phase 9 (Citations, Positioning & Limitations):** Replaced neutral-atom citation [53] with authentic transmon biased-noise citation (Aliferis et al. New J. Phys. 2009). Verified Refs [24] and [25] for classical Min-Sum and OSD. Added comparative architectural positioning in Section II and explicit limitations section in Section IX. Produced `PHASE_9_REPORT.md`.
11. **Phase 10 (Manuscript IEEEtran Format):** Verified strict IEEEtran two-column layout. Compacted Abstract to exactly 200 words containing only verified metrics. Verified high-resolution vector and $>400$ DPI raster figures. Compiled `manuscript/main.pdf` (12 pages) passing all 13 forensic checks. Produced `PHASE_10_REPORT.md`.
12. **Phase 11 (Repository Hygiene & Makefile):** Cleaned `README.md` header badges. Implemented root `Makefile`. Verified `CITATION.cff` and updated `CHANGELOG.md`. Produced `PHASE_11_REPORT.md`.
13. **Phase 12 (Final Verification & Reviewer Risks):** Produced `FINAL_VERIFICATION.md` (39/39 automated assertions passed, 100.0%), `REVIEWER_RISKS.md` (15 hardest reviewer questions answered), and finalized `TODO_HUMAN.md`. Produced `PHASE_12_REPORT.md`.
14. **Final Synchronization Pass:** Synchronized `docs/EXPERIMENTAL_VALIDATION.md`, `docs/REPRODUCIBILITY_GUIDE.md`, `docs/README.md`, `README.md`, `scripts/build_submission_bundle.py`, and rebuilt `submission/` package (`cover_letter.pdf`, `cover_letter.tex`, `COVER_LETTER.md`, `SUBMISSION_METADATA.md`, `manuscript_sources.zip`). All 39 claim verifications, 46 pytest tests, and 13 forensic PDF checks passing cleanly.
