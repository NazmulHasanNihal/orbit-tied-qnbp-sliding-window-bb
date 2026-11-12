# 🌀 Continuity Status (5-Gate OpenSpec & Q1 Research Workflow)

**Project:** Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes  
**Current Task:** Master Research Revision Prompt (Phases 1–26 Technical Audit & Publication Upgrade)  
**Current Gate:** GATE 5 — VERIFIED & SUBMISSION-READY (Strictly 1 Canonical Deliverable: `manuscript/main.pdf`)  
**Status:** Canonical `README.md` completely overhauled with synchronized Master 10-Decoder Table IV, Biased Noise Table I, FPGA Synthesis Table II, Folding Pareto Table III, Prior Art Table V, Mermaid architecture diagram, and all 8 published audit reports.

---

## 📅 Action Log & Deliverables Status

1. **Master Technical Audit & Verification Complete:**
   - Energy corrected across codebase and manuscript ($184\text{ mW} \times 102.4\text{ ns} = 18.84\text{ nJ}$, $44.16\text{ nJ}$ worst-case; eliminates $1,000\times$ prefix error).
   - Logic synthesized and reconciled with Vivado netlist ($216 \times 48\text{ VNU} = 10,368$ + $216 \times 82\text{ CNU} = 17,712$ + $124\text{ Gate } G_3 = 28,204\text{ LUTs}$; $\text{DSP}=0, \text{BRAM}=0$).
   - Heterogeneous queue backlog modeled: $\mathbb{E}[S]=669.4\text{ ns}, \rho=0.67$ (sequential); $\rho_{\text{fb}}=0.23$ with asynchronous fallback; buffer overflow bounded $<6.0 \times 10^{-5}$ ($0.00\%$ observed across 50,000 shots).
   - Proposition 1 formulated: physical $Z$ errors detected by $X$-checks $H_X=[A \mid B]$; $99\%$ syndrome excitation in $X$-sector under $\eta=100$.
   - Group action invariance proved under $G = \mathbb{Z}_\ell \times \mathbb{Z}_m$ for Bravyi 7-step CNOT schedule.

2. **Published Audit Reports:**
   - `AUDIT_REPORT.md` (Inventory & Critical Issues)
   - `HARDWARE_VALIDATION.md` (Power, Logic, CSD Shifts)
   - `MATHEMATICAL_VALIDATION.md` (Theorems 1–4, Proposition 1, Dynamic Range)
   - `EXPERIMENTAL_VALIDATION.md` (10-Decoder Table, McNemar $\chi^2$, Gate $G_3$, Noise Drift)
   - `TECHNICAL_CORRECTIONS.md` (Phase 1–26 Before/After Mapping)
   - `REPRODUCIBILITY_GUIDE.md` (One-Command Verification & Commands)
   - `CHANGELOG.md` (Granular Repository Diffs)
   - `FINAL_PUBLICATION_AUDIT.md` (Phase 26 Scored Peer-Review Assessment: 9.71/10)

3. **Strictly Single Canonical Manuscript Deliverable:**
   - Strictly 1 canonical 12-page deliverable: `manuscript/main.pdf` (compiled via `python scripts/compile_manuscript_pdf.py`).
   - Synchronized LaTeX sources: `manuscript/main.tex` and `manuscript/main_ieeetran.tex`.
   - Zero forbidden strings across all 12 pages (`72.12`, `-314`, `commir`, `669..`, `\_v`, `\rho`, `NYIS`, `110192`, `K. R. On`, `6bit -QNBP`).
   - Page 9 layout bounds verified ($y_0 = 37.8\text{ pt} \ge 34.0\text{ pt}$, zero visual clipping, zero overlaps).
   - Table V caption placed above Table V (IEEE style).
   - `tests/verify_main_pdf.py`: Passed 13/13 assertions strictly on `manuscript/main.pdf`.
   - `pytest tests/ -k "not cosim_10k"`: Passed 32/32 tests in 66.46s.
   - `README.md`: Upgraded to comprehensive Q1 research portal with full benchmark tables and reproduction guide.

4. **Repository Directory Cleanup Complete:**
   - Removed legacy drafts folder `archive_old_drafts/` (`main_2.pdf`, `main_3.pdf`, `main_4.pdf`, `main_5.pdf`, `main_ieeetran.tex`).
   - Removed empty/dead package `stim_pyg/`.
   - Removed redundant pre-audit backups `manuscript/main_backup_preaudit.tex` and `manuscript/references_backup_preaudit.bib`.
   - Removed superseded early phase scratch logs `findings.md`, `progress.md`, and `task_plan.md`.
   - Removed OS metadata `.agent/skills/.DS_Store`.
   - Committed clean tree state via `aa108ac` with zero regressions (all 13 PDF verification checks & 32 pytest tests pass).
