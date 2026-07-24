.PHONY: paper arxiv verify clean

# Compile the manuscript (single source of truth: paper/)
paper:
	cd paper && latexmk -pdf -interaction=nonstopmode chairman_counterexample.tex

# Assemble the self-contained arXiv upload package (generated, not tracked)
arxiv: paper
	rm -rf arxiv-upload
	mkdir -p arxiv-upload
	sed 's|\\input{../figures/chairman_gadget.tex}|\\input{chairman_gadget.tex}|' paper/chairman_counterexample.tex > arxiv-upload/chairman_counterexample.tex
	cp figures/chairman_gadget.tex arxiv-upload/
	cp paper/chairman_counterexample.bbl arxiv-upload/
	cd arxiv-upload && latexmk -pdf -interaction=nonstopmode chairman_counterexample.tex && latexmk -c
	@echo "arXiv package ready in arxiv-upload/: upload the two .tex files and the .bbl"

verify:
	cd code && python3 verify_chairman.py
	cd code && python3 verify_chairman_certificate.py
	cd code && python3 verify_stronger_bound.py

clean:
	cd paper && latexmk -C
	rm -rf arxiv-upload
