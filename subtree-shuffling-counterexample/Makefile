PYTHON ?= python3
PAPER_DIR := paper
PAPER := subtree_shuffling_counterexample

.PHONY: install verify test paper clean

install:
	$(PYTHON) -m pip install -e '.[test]'

verify:
	$(PYTHON) -m shuffle_counterexample.verify --strict

test:
	pytest -q

paper:
	cd $(PAPER_DIR) && latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode $(PAPER).tex

clean:
	cd $(PAPER_DIR) && latexmk -C $(PAPER).tex
	rm -rf .pytest_cache build dist src/*.egg-info src/shuffle_counterexample/__pycache__ tests/__pycache__
