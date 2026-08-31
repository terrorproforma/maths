PYTHON ?= python3

.PHONY: verify manifest all

verify:
	$(PYTHON) code/count_scalar_invariants.py --root .
	$(PYTHON) code/generate_invariant_coupling_basis.py --root .
	$(PYTHON) code/verify_phase2b_vacuum.py --root .
	$(PYTHON) -m unittest discover -s code/tests -v

manifest:
	$(PYTHON) code/build_manifest.py --root .

all: verify manifest
