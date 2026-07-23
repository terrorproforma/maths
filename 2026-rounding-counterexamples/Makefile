PYTHON ?= python3
LATEXMK ?= latexmk
BUILD := build
PAPER_DIR := papers
FIGURE_DIR := figures
PAPERS := dgg-counterexample chairman-counterexample overview

.PHONY: all verify derive papers clean

all: verify papers

verify:
	$(PYTHON) code/verify_all.py

derive:
	$(PYTHON) code/derive_dgg_family.py
	$(PYTHON) code/derive_chairman_family.py

papers: $(PAPERS:%=$(BUILD)/%.pdf)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/dgg-counterexample.pdf: $(PAPER_DIR)/dgg-counterexample.tex $(PAPER_DIR)/references.bib $(FIGURE_DIR)/dgg_network.tex $(FIGURE_DIR)/dgg_obstruction.tex | $(BUILD)
	cd $(PAPER_DIR) && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error dgg-counterexample.tex
	cp $(PAPER_DIR)/dgg-counterexample.pdf $@

$(BUILD)/chairman-counterexample.pdf: $(PAPER_DIR)/chairman-counterexample.tex $(PAPER_DIR)/references.bib $(FIGURE_DIR)/chairman_gadget.tex | $(BUILD)
	cd $(PAPER_DIR) && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error chairman-counterexample.tex
	cp $(PAPER_DIR)/chairman-counterexample.pdf $@

$(BUILD)/overview.pdf: $(PAPER_DIR)/overview.tex $(PAPER_DIR)/references.bib $(FIGURE_DIR)/graphical_abstract.tex $(FIGURE_DIR)/dgg_network.tex $(FIGURE_DIR)/chairman_gadget.tex | $(BUILD)
	cd $(PAPER_DIR) && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error overview.tex
	cp $(PAPER_DIR)/overview.pdf $@

clean:
	cd $(PAPER_DIR) && $(LATEXMK) -C dgg-counterexample.tex chairman-counterexample.tex overview.tex || true
	rm -rf $(BUILD)
