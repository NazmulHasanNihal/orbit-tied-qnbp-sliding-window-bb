# Contributing to Orbit-Tied QNBP

Thank you for your interest in contributing to the **Orbit-Tied Quantized Neural Belief Propagation (QNBP)** project! This repository houses the official implementation, automated evaluation pipelines, and synthesizeable RTL for sliding-window decoding of bivariate-bicycle LDPC quantum error-correcting codes.

---

## 📜 Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. All participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 🛠️ Development Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb.git
cd orbit-tied-qnbp-sliding-window-bb
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv

# On Linux / macOS:
source .venv/bin/activate

# On Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 3. Install in Editable Mode with Development Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

---

## 🧪 Testing and Verification

Before submitting any Pull Request, ensure that all automated checks pass:

### 1. Run Complete Test Suite
```bash
python -m pytest tests/ -k "not cosim_10k"
```

### 2. Run CLI Self-Verification
```bash
python -m orbit_tied_qnbp.cli verify
```

### 3. Run Forensic Manuscript Verification
```bash
python tests/verify_main_pdf.py
```

### 4. Code Quality & Linting
```bash
ruff check .
ruff format --check .
mypy src/ tests/
```

---

## 📐 Coding Standards & Guidelines

- **Python Standards:** Python 3.9+ compatible. Strictly type-annotated (`from typing import ...`).
- **No Magic Numbers:** All physical constants, error rates, window sizes, and quantization parameters must be explicitly defined in configuration dataclasses or settings.
- **Docstrings:** All public functions, classes, and methods must include Google- or Sphinx-style docstrings with arguments, returns, and mathematical formulations where appropriate.
- **Hardware Co-Simulation:** Any modification to neural BP quantization schemes, saturating arithmetic, or CSD representations must maintain bit-exact numerical agreement with the SystemVerilog RTL modules in `rtl/`.

---

## 🔄 Pull Request Guidelines

1. **Branch Naming:**
   - Feature: `feat/short-description`
   - Bugfix: `fix/short-description`
   - Documentation: `docs/short-description`
   - Performance: `perf/short-description`
2. **Commit Messages:** Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat(decoder): add support for gross code [[360,12,d<=24]]`
   - `fix(rtl): resolve carry bit overflow in 6-bit saturating VNU adder`
   - `docs(readme): add interactive benchmark widget`
3. **Draft Pull Requests:** Open a Draft PR if you want early feedback before all tests are passing.
4. **Clean Git History:** Rebase onto `main` before requesting review; avoid merge commits where possible.

---

## 📬 Contact & Inquiries

For questions regarding theoretical derivations, hardware co-design, or academic collaboration:
- **Lead Author:** Md. Nazmul (`nazmulhas36@gmail.com`)
- **Institution:** Department of Computer Science and Engineering, College of Technology, National University, Gazipur, Bangladesh

