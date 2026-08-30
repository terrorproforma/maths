PYTHON ?= python
LATEXMK ?= latexmk

.PHONY: tables figures paper verify test manifest all clean

tables:
	$(PYTHON) code/generate_latex_tables.py --root .

figures:
	$(PYTHON) code/generate_figures.py --root .

paper: tables figures
	cd paper && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error minimum_viable_successor_checklist.tex
	cd paper && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error frontier_model_constraint_ledger.tex
	cp paper/minimum_viable_successor_checklist.pdf minimum_viable_successor_checklist.pdf
	cp paper/frontier_model_constraint_ledger.pdf frontier_model_constraint_ledger.pdf

verify: paper
	$(PYTHON) code/verify_frontier_model.py --root .

test: verify
	$(PYTHON) -m unittest discover -s tests -v

manifest: test
	$(PYTHON) code/build_manifest.py --root .

all: tables figures paper verify test manifest

clean:
	cd paper && $(LATEXMK) -c minimum_viable_successor_checklist.tex || true
	cd paper && $(LATEXMK) -c frontier_model_constraint_ledger.tex || true
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
