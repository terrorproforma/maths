PYTHON ?= python3
PAPER = paper/tp01_dirac_brst_global_audit_v1_1.tex
PDF = paper/tp01_dirac_brst_global_audit_v1_1.pdf
ROOTPDF = TP-01_Dirac_BRST_Global_Audit_v1.1.pdf

.PHONY: all verify figures test source paper validate manifest clean

all: verify figures test paper validate manifest

verify:
	$(PYTHON) code/verify_dirac_brst_global_v1_1.py --root .

figures:
	$(PYTHON) code/generate_summary_figures.py --root .

test:
	$(PYTHON) -m unittest discover -s code/tests -v

source:
	$(PYTHON) paper/rebuild_source.py

paper: source
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error tp01_dirac_brst_global_audit_v1_1.tex
	cp $(PDF) $(ROOTPDF)

validate:
	$(PYTHON) code/final_validate.py --root .

manifest:
	$(PYTHON) code/build_manifest.py --root .

clean:
	cd paper && latexmk -C tp01_dirac_brst_global_audit_v1_1.tex
	rm -f $(PAPER) $(ROOTPDF) manifest_sha256.csv
