# 🌀 Continuity Status (5-Gate OpenSpec & Q1 Research Workflow)

**Project:** Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes  
**Current Task:** Full Authorship Records, Specific Roles, Institutional Emails, and ORCID Synchronization  
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
**Status:** All author roles, emails, ORCID records, and URLs synchronized across README.md, docs/README.md, CITATION.cff, pyproject.toml, manuscript/main.tex, manuscript/main_ieeetran.tex, compile_manuscript_pdf.py, build_submission_bundle.py, submission/cover_letter.pdf, submission/cover_letter.tex, submission/COVER_LETTER.md, submission/SUBMISSION_METADATA.md, and tests/verify_main_pdf.py. 13/13 PDF forensic checks passed. 6/6 CLI verification checks passed. 35/35 pytest unit/integration tests passed.

---

## 📅 Action Log & Deliverables Status

1. **Full Authorship Record Synchronization:**
   - Synchronized all 3 authors with their individual roles, institutional emails, and direct ORCID URLs across all documentation and manuscript files.
   - Recompiled `manuscript/main.pdf` (1.75 MB, 12 pages) with PyMuPDF compression (`deflate=True, garbage=4, clean=True`), embedding author block and CRediT statement.
   - Rebuilt submission bundle (`submission/main.pdf`, `submission/cover_letter.pdf`, `submission/cover_letter.tex`, `submission/COVER_LETTER.md`, `submission/SUBMISSION_METADATA.md`, `submission/manuscript_sources.zip`).
   - Built distribution wheel and sdist with twine check passed (`dist/orbit_tied_qnbp-1.0.0-py3-none-any.whl`, `dist/orbit_tied_qnbp-1.0.0.tar.gz`).
   - Ran `verify_main_pdf.py` asserting all 3 author emails on Page 1 (PASSED 13/13).
   - Ran `qnbp verify` (PASSED 6/6 in 1.04s).
