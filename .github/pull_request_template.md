## Description of Changes

Please provide a brief summary of the changes introduced in this pull request and the motivation behind them.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement / Refactoring

## Verification Checklist

- [ ] My code follows the code style and typing guidelines of this project (`ruff check .`, `mypy`).
- [ ] I have added tests that prove my fix is effective or that my feature works.
- [ ] New and existing unit tests pass locally with my changes (`python -m pytest tests/ -k "not cosim_10k"`).
- [ ] CLI self-verification passes (`python -m orbit_tied_qnbp.cli verify`).
- [ ] Manuscript forensic verification remains intact (`python tests/verify_main_pdf.py`).
- [ ] Any modifications to quantized arithmetic maintain bit-exact RTL co-simulation parity.
