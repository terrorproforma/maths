PYTHON ?= python3

.PHONY: verify

verify:
	$(PYTHON) code/verify_representation_dimensions.py --root .
	$(PYTHON) code/verify_inhomogeneous_group_signs.py --root .
	$(PYTHON) code/verify_first_order_action_covariance.py --root .
	$(PYTHON) code/verify_shiab_einstein_pattern.py --root .
	$(PYTHON) -m unittest discover -s code/tests -v
