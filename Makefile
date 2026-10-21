.PHONY: install fmt lint typecheck test test-model check run data-report examples-render examples-serve enqueue queue-status queue-pull queue-worker queue-cancel

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

# Job queue on the GPU box (scripts/jobq.py): make enqueue JOB=jobs/d2/d2_ko_v1.yaml (committed tree only)
enqueue:            ## queue a job spec (or several: JOB="a.yaml b.yaml") on the GPU box
	uv run python -m scripts.jobq enqueue $(JOB) $(ARGS)

queue-status:       ## running (with progress/ETA), pending, last done/failed jobs and their durations
	uv run python -m scripts.jobq status

queue-pull:         ## results (new dirs only), ledger, EXPERIMENTS.md drafts, logs from the box
	uv run python -m scripts.jobq pull

queue-worker:       ## start the worker for GPU $(GPU) (default 0) in tmux on the box, if not running
	uv run python -m scripts.jobq start-worker --gpu $(or $(GPU),0)

queue-cancel:       ## cancel a pending job: make queue-cancel ID=<job id>
	uv run python -m scripts.jobq cancel $(ID)

examples-render:    ## examples/<exp>/ from the latest examples run of each experiment (no GPU)
	uv run python -m bridge_jspace.examples export

examples-serve:     ## render, then serve examples/ on http://localhost:$(PORT) and open it (PORT=8000)
	uv run python -m bridge_jspace.examples serve $(or $(PORT),8000)
