PYTHON ?= python3

.PHONY: verify

verify:
	$(PYTHON) code/verify_pati_salam_phase1.py --root .
	$(PYTHON) -m unittest discover -s code/tests -v
