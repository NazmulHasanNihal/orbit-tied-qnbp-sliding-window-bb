# 🌀 Continuity Status (5-Gate OpenSpec & Q1 Research Workflow)

**Project:** Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes  
**Current Task:** Pre-Submission Repair Pass Across Visual Figures, Equations, Tables, and Bibliography  
**Current Gate:** GATE 5 — VERIFIED & SUBMISSION-READY (Strictly 1 Canonical Deliverable: `manuscript/main.pdf`)  
**Authors & Specific Roles:**  
1. **Md. Nazmul** (Lead & Corresponding Author)  
   - Role: Lead Researcher, Conceptualization, Methodology & Software Architecture  
   - Email: `nazmulhas36@gmail.com`  
   - ORCID: `0009-0001-6115-7023` (https://orcid.org/0009-0001-6115-7023)  
2. **Musrat Jahan Gungun** (Co-Author)  
   - Role: Data Curation, Baseline Benchmarking, Validation & Statistical Testing  
   - Email: `gungunjahan84@gmail.com`  
   - ORCID: `0009-0006-4249-9198` (https://orcid.org/0009-0006-4249-9198)  
3. **Maheli Ahmed** (Co-Author & Faculty Supervisor)  
   - Role: Faculty Supervision, Resources, Formal Analysis & Model Governance  
   - Email: `maheli.ahmed.cse.cot@gmail.com`  
   - ORCID: `0000-0002-5183-7498` (https://orcid.org/0000-0002-5183-7498)  
**Affiliation:** Department of Computer Science and Engineering, College of Technology, National University, Gazipur-1704, Bangladesh  
**Status:** Completed exhaustive 5-step pre-submission repair pass across visual figure generators, table captions, equations, inline typography, and bibliography. Single canonical deliverable `manuscript/main.pdf` (1.65 MB, exactly 12 pages) passes 13/13 forensic audit checks, 41/41 targeted regex assertions, 0 forbidden strings, 38/38 pytest tests, and twine packaging checks with 100% success.

---

## 📅 Action Log & Deliverables Status

1. **Step 1 (Visual Figures & Layouts):**
   - **Fig 1 (`fig1_architecture.png`):** Widened horizontal gaps between boxes 1, 2, 3, 4 with coordinate expansion (`xlim` 0 to 142) and generous 11-unit spacing for arrow labels (`Extract DEM`, `Orbit Tying`, `Posterior L_v`). Relocated `Pass (>= \tau)` and `Fail (< \tau)` onto arrow shafts to the right of Box 4 with zero border collisions.
   - **Fig 5(a) Legend:** Repositioned legend to `upper right` in `plot_figures.py`, eliminating overlap with curves at $\tau = 1.5$.
   - **Fig 6 Pareto Plot:** Regenerated pure dual-axis hardware folding Pareto frontier plot at 300 DPI (`fig6_folding_tradeoffs.png`) with zero rasterized table screenshots.
   - **Table V Caption:** Positioned above Table V in compliance with IEEE Transactions style.

2. **Step 2 (Equations & Glyphs):**
   - **Page 9 (Sec VII Line 6):** Formatted math $L_v^{(0)} = \sum_{f \in F_v} \ln((1 - p_f)/p_f)$ using valid HTML sub/sup tags, removing unparsed literal markup.
   - **Page 6 (Sec V-A):** Verified biased noise formula $p_Z = p \cdot \eta / (\eta + 1), p_X = p_Y = p / [2(\eta + 1)]$.
   - **Page 5 (Sec IV-B & IV-E):** Enforced $[-31\Delta, +31\Delta] = [-7.75, +7.75]$, $(1 - 2s_c)$, and proper subscript $y_j)$.
   - **Page 3 (Sec III-A Thm 1):** Verified all 3 numbered properties render visibly without blank spaces.
   - **Page 7 (Sec VI-B & VI-D):** Rendered Gate G1 $H\hat{e} \equiv s \pmod 2$, restored `\tau:` before colons in G2 and G3, replaced standalone `&and;` with `<b>and</b>` in displayed G3 equation, and verified $669.4\text{ ns} < 1000\text{ ns}$.

3. **Step 3 (Page-by-Page Typography & Tables):**
   - Verified zero occurrences of 14 specific error strings: `National University,.`, `72.12`, `144.12`, `-314`, `ranw`, `commir`, `thresholdt`, `\_v`, `6bit -QNBP`, `Nazmul HasanNihal`, `NYIS`, `110192`, `K. R. On`, `01045`.
   - Verified Table I caption closing parenthesis `at \eta=1))`, Table IV row 2 closing bracket `[0.4063, 0.4257]`, and Table V references.

4. **Step 4 (Bibliography & Sequential Ordering):**
   - Verified Ref [11] (2025), Ref [12] (2025), Ref [33] (arXiv:2603.10192), Ref [36] ((HPCA), pp. 259-273), Ref [40] (K. R. Ott, arXiv:2502.16408), Ref [48] (arXiv:2605.01035).
   - Enforced strictly sequential two-column bibliography ordering: references `[1]`–`[30]` down left column and `[31]`–`[59]` down right column.

5. **Step 5 (Rebuild, Audit & Packaging):**
   - Recompiled `manuscript/main.pdf` (1.65 MB, 12 pages).
   - Rebuilt `submission/` package: `main.pdf`, `cover_letter.pdf`, `COVER_LETTER.md`, `SUBMISSION_METADATA.md`, `manuscript_sources.zip`.
   - Verified: `python tests/verify_main_pdf.py` (13/13 passed), `python -m ruff check .` (0 errors), `qnbp verify` (6/6 passed), `pytest` (38/38 passed), `python -m twine check dist/*` (PASSED).
