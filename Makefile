.PHONY: install fmt lint typecheck test test-model check run data-report

# make run CONFIG=scripts/exp10_lens_sanity/config.yaml ARGS="model=configs/models/qwen3.6-27b.yaml"
run:                ## experiment in a detached tmux session, log in log/
	bash scripts/run.sh $(CONFIG) $(ARGS)

install:            ## env + git hooks
	uv sync
	uv run pre-commit install

fmt:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff format --check .
	uv run ruff check .

typecheck:
	uv run pyright

test:               ## fast unit tests (no model download)
	uv run pytest

test-model:         ## integration tests on Qwen3.5-0.8B + its lenses (CPU ok, a few minutes)
	uv run pytest -m model

check: lint typecheck test

data-report:        ## what data we work with: counts, categories, labels, overlaps (add ARGS=--json)
	uv run python -m scripts.data_report $(ARGS)
