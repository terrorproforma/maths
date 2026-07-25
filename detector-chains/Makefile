.PHONY: paper verify verify-milp verify-all clean

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode kappa_chains.tex && latexmk -c

# exact certificates; standard library only, no solver
verify:
	python3 code/verify_chain_certificate.py
	python3 code/verify_kappa_certificate.py
	python3 code/verify_split_optimality.py
	python3 code/verify_block_games.py
	python3 code/verify_composition_failure.py

# independent confirmation of one instance; needs numpy + scipy (HiGHS)
verify-milp:
	python3 code/beat_76_instance.py

verify-all: verify verify-milp

clean:
	cd paper && latexmk -C
