.PHONY: install test lint validate prepare clean

install:
	python -m pip install -e '.[test]'

test:
	pytest

lint:
	ruff check src tests
	mypy src

validate:
	bnsjet validate-manifest configs/campaign.yaml
	bnsjet validate-targets reference_targets/target_metrics.yaml

prepare:
	bnsjet prepare-run configs/campaign.yaml --run-root runs

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache src/*.egg-info src/**/__pycache__ tests/__pycache__
