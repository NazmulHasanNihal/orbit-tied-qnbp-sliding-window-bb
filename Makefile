.PHONY: help test test-all tables check-tables reproduce-smoke pdf audit-pdf lint verify all

help:
	@echo "Available targets:"
	@echo "  make test             Run standard test suite (46 tests, excluding slow cosim)"
	@echo "  make test-all         Run complete test suite including 10k cosim"
	@echo "  make tables           Regenerate all manuscript and README tables from results/"
	@echo "  make check-tables     Verify tables match results/ with zero diff"
	@echo "  make reproduce-smoke  Run smoke benchmarks across decoders"
	@echo "  make pdf              Compile 12-page IEEE manuscript PDF (manuscript/main.pdf)"
	@echo "  make audit-pdf        Run full 13-point forensic audit on manuscript/main.pdf"
	@echo "  make lint             Run ruff linter check"
	@echo "  make verify           Run lint, check-tables, test, and audit-pdf"
	@echo "  make all              Run tables, pdf, test, and audit-pdf"

test:
	python -m pytest tests/ -k "not cosim_10k"

test-all:
	python -m pytest tests/

tables:
	python scripts/make_tables.py

check-tables:
	python scripts/make_tables.py --check

reproduce-smoke:
	python scripts/run_competitor_benchmarks.py --smoke

pdf:
	python scripts/compile_manuscript_pdf.py

audit-pdf:
	python tests/verify_main_pdf.py

lint:
	python -m ruff check .

verify: lint check-tables test audit-pdf

all: tables pdf test audit-pdf
