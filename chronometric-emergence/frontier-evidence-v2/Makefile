PYTHON ?= python3
REPO_ROOT ?= ../..

.PHONY: reproduce test full clean

reproduce:
	$(PYTHON) -m frontier_evidence.run_all --repo-root $(REPO_ROOT)

test:
	pytest -q

full: test reproduce

clean:
	rm -f results/*.json results/*.csv results/*.npz docs/FRONTIER_EVIDENCE_REPORT.md
