# 🌀 Continuity Status (5-Gate OpenSpec & Q1 Research Workflow)

**Project:** Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes  
**Current Task:** CI/CD Workflow Audit, Linter Configuration, and Pipeline Hardening  
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
**Status:** CI/CD GitHub Actions workflow audited and hardened. Configured tool.ruff in pyproject.toml to enforce essential syntax/runtime checks while ignoring cosmetic style preferences. Fixed missing NDArray typing import in quantization.py. Added concurrency control to ci.yml. Verified ruff check passes with 0 errors, 13/13 PDF forensic checks pass, and 6/6 CLI self-verification checks pass.

---

## 📅 Action Log & Deliverables Status

1. **CI/CD Pipeline Hardening:**
   - Configured `[tool.ruff]` in `pyproject.toml` with `select = ["E", "F", "W"]` and appropriate style ignores (`E501`, `UP`, `RUF`, `PLR`, `I`) to prevent false-positive linter build failures.
   - Added missing `NDArray` typing import in `src/orbit_tied_qnbp/decoder/quantization.py`.
   - Cleaned redundant `f` string prefixes across scaling and benchmark scripts.
   - Added concurrency management with `cancel-in-progress: true` in `.github/workflows/ci.yml`.
   - Verified that all steps in the CI pipeline (`ruff check`, `qnbp verify`, `pytest`, `verify_main_pdf.py`, `twine check`) pass locally with exit code 0.
