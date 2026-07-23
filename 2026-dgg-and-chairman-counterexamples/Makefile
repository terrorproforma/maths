PYTHON ?= python3
LATEXMK ?= latexmk

.PHONY: all verify verify-exact verify-milp paper clean

all: verify paper

verify: verify-exact verify-milp

verify-exact:
	$(PYTHON) code/verify_dgg.py
	$(PYTHON) code/verify_chairman_certificate.py

verify-milp:
	$(PYTHON) code/verify_chairman_milp.py

paper:
	cd paper && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex
	mkdir -p artifacts
	cp paper/main.pdf artifacts/counterexamples.pdf

clean:
	cd paper && $(LATEXMK) -C main.tex
	rm -f artifacts/counterexamples.pdf
