# 🌀 Continuity Status (5-Gate OpenSpec & Q1 Research Workflow)

**Project:** Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes  
**Current Task:** Comprehensive 10-Task Pre-Submission Repair Pass (Code, JSON, Tables, Figures, RTL & Theorems)  
**Current Gate:** GATE 5 — VERIFIED & SUBMISSION-READY (Strictly 1 Canonical Deliverable: `manuscript/main.pdf`)  
**Authors & Specific Roles:**  
1. **Md. Nazmul** (Lead & Corresponding Author, `nazmulhas36@gmail.com`, ORCID: `0009-0001-6115-7023`)  
2. **Musrat Jahan Gungun** (Co-Author, `gungunjahan84@gmail.com`, ORCID: `0009-0006-4249-9198`)  
3. **Maheli Ahmed** (Co-Author & Supervisor, `maheli.ahmed.cse.cot@gmail.com`, ORCID: `0000-0002-5183-7498`)  
**Affiliation:** Department of Computer Science and Engineering, College of Technology, National University, Gazipur-1704, Bangladesh  
**Status:** 10-task repair pass complete. Master benchmark JSON, tables, figures, LaTeX, and compiled PDF synchronized from single source of truth. Passed 13/13 PDF forensic audit checks, 38/38 pytest tests, 0 ruff errors.

---

## 📅 Action Log & Deliverables Status

1. **Task 1 (Single Source of Truth & Baselines):** Added IBM Relay-BP full 300-leg baseline ($P_L=0.0060$, 148.5 iters, $\chi^2=1.14, p=0.286$) alongside hardware-capped Relay-BP ($P_L=0.0090, \chi^2=12.06, p=0.000515$). Generated `scripts/sync_all_tables.py`, synchronizing `README.md`, LaTeX sources, and PDF table entries with zero duplicate placeholder rows.
2. **Task 2 (Two-Tier Fallback & Unmixing p=0.003/0.001):** Defined Tier 1 (on-chip FPGA fallback, 950 ns service time, $\rho_{\text{fb}}=0.23$) at $p=0.003$ ($P_{\text{pipe}}=1.90 \times 10^{-3}$) and Tier 2 (software OSD fallback, $320\,\mu\text{s}$, $\rho_{\text{fb}}<1.0$) at $p=0.001$ ($P_{\text{pipe}}=7.00 \times 10^{-6}$).
3. **Task 3 (Stim Priors & Formal Proposition Titles):** Retitled Proposition 1 (Torus Translation Invariance), Proposition 2 (Equivariance of Message Passing), Lemma 1 (6-Bit Dyadic Dynamic Range Bound), and Proposition 3 (Effective Dephasing Concentration). Documented dyadic pre-scaling $\kappa = 0.75 = 1 - 2^{-2}$ preventing prior clipping for depth-7 depolarizing circuits.
4. **Task 4 (Hardware RTL Scope & Device Unification):** Formally distinguished 216-VNU Bipartite Syndrome-Projection Decoder (28,204 LUTs) vs. 203-orbit full-DEM architecture (31,800 LUTs). Unified FPGA target to AMD Kintex UltraScale+ XCKU040 with DSP=0 and verified 10,000-shot bit-exact co-simulation parity.
5. **Task 5 ($P_L$ Metric & Phrasing):** Defined $P_L = P(\hat{y} \ne y)$ and $P_{L,\text{round}} = 1 - (1 - P_L)^{1/W}$. Reserved "gross code" strictly for $[[144,12,12]]$. Shortened Abstract to $\le 225$ words and moved citations [24], [25], [53] to respective methodologies.
6. **Task 6 (Visual Multi-Panels & Schematics):** Regenerated multi-panel Fig 1, Fig 2, Fig 5, Fig 6 (CSD datapath schematic + Pareto frontier), and Fig 7. Fixed Table V caption position.
7. **Task 7 (LaTeX Synchronization & Repo Hygiene):** Synced `main_ieeetran.tex` and `main.tex`. Fixed Mermaid diagram label typo. Deleted obsolete audit files in `docs/`.
8. **Task 8 (Verification & Packaging):** Recompiled `manuscript/main.pdf` (12 pages, 2.4 MB) and `submission/` package. Verified `tests/verify_main_pdf.py` (13/13 passed), `pytest` (38/38 passed), and `ruff check .` (0 errors).
