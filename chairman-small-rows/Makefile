.PHONY: paper verify verify-quick clean

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode two_machines.tex && latexmk -c

# exact checks; Python standard library only
verify:
	python3 code/verify_rail_family.py 9
	python3 code/verify_two_row_theorem.py
	python3 code/verify_instances.py

# the same with 2,000 random instances in place of 20,000 (about 15 s)
verify-quick:
	python3 code/verify_rail_family.py 9
	python3 code/verify_two_row_theorem.py 2000
	python3 code/verify_instances.py

clean:
	cd paper && latexmk -C
