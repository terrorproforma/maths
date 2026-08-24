# Reproducibility entry points for Null-Relational Chronometry.
# Author: Angus Muffatti

PYTHON ?= python3

.PHONY: verify inventory

verify:
	$(PYTHON) scripts/run_repository_verification.py

inventory:
	@find . -type f ! -path './.git/*' -print | sort
