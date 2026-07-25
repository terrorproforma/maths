.PHONY: paper verify clean

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode kappa_chains.tex && latexmk -c

verify:
	python3 code/verify_chain_certificate.py
	python3 code/verify_kappa_certificate.py
	python3 code/verify_block_games.py
	python3 code/beat_76_instance.py

clean:
	cd paper && latexmk -C
