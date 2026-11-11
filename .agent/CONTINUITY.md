# 🌀 Continuity Status (5-Gate OpenSpec & Q1 Research Workflow)

**Project:** Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes  
**Current Task:** Single Canonical Manuscript Deliverable (`manuscript/main.pdf`)  
**Current Gate:** GATE 5 — VERIFIED & SUBMISSION-READY (Strictly 1 Canonical Deliverable: `manuscript/main.pdf`)  
**Status:** 100% publication-ready for IEEE Transactions on Quantum Engineering (IEEE TQE). There is strictly ONE canonical 12-page PDF in `manuscript/`: `manuscript/main.pdf`. All legacy/duplicate drafts (`main_2.pdf`, `main_3.pdf`, `main_4.pdf`, `main_5.pdf`, `main_ieeetran.tex`) have been moved into `archive_old_drafts/`.

---

## 📅 Action Log & Single Deliverable Consolidation

1. **Single Canonical Manuscript Consolidation:**
   - Modified `scripts/compile_manuscript_pdf.py` so it outputs strictly ONE single PDF: `manuscript/main.pdf`.
   - Moved duplicate drafts `main_4.pdf`, `main_5.pdf`, and `main_ieeetran.tex` into `archive_old_drafts/`.
   - Verified `manuscript/` directory contains strictly one PDF deliverable: `['main.pdf']`, one canonical LaTeX source: `main.tex`, one bibliography: `references.bib`, and the `figures/` directory.
   - Updated `tests/verify_main_pdf.py` to assert that `manuscript/` contains strictly `['main.pdf']` before executing all 13 forensic checks.
   - Verified that `archive_old_drafts/` cleanly stores all previous drafts: `['main_2.pdf', 'main_3.pdf', 'main_4.pdf', 'main_5.pdf', 'main_ieeetran.tex']`.

2. **Automated Verification:**
   - `manuscript/main.pdf` passes all 13 checks in `tests/verify_main_pdf.py`.
   - Exactly 12 pages with zero overflow.
   - All 59 references cited.
   - Zero occurrences of forbidden strings or outdated chi-square metrics:
     `["4,040.8", "4,200.4", "24.38", "18.05", "G<sub>2</sub>", "5.0 ns/iter", "314", "rayv", "commir", "falback", "0.1.25", "Gate G2", "669..", "toy d=3", "2006", "I. Q. A. Team", "and et al."]`.
