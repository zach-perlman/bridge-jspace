.PHONY: install fmt lint typecheck test test-model check run data-report examples-render examples-serve enqueue queue-status queue-pull queue-worker queue-cancel queue-stats

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

# Job queue on a GPU box (scripts/jobq.py): make enqueue JOB=jobs/d2/d2_ko_v1.yaml (committed tree only).
# Which box: QUEUE=a100 (default: sesterce-a100x4, 4 GPUs) or QUEUE=h100 (sesterce-h100x2, 2 GPUs; rented 23 Oct
# for the 122B; it replaces the deleted 2x H200, whose ledger stays in results/jobq/); queue-stats also takes QUEUE=all.
# Example: make queue-stats QUEUE=h100
QUEUE ?= a100
QUEUE_HOST_a100 := sesterce-a100x4
QUEUE_HOST_h100 := sesterce-h100x2
QUEUE_GPUS_a100 := 4
QUEUE_GPUS_h100 := 2
JOBQ = JOBQ_HOST=$(QUEUE_HOST_$(QUEUE)) uv run python -m scripts.jobq

enqueue:            ## queue a job spec (or several: JOB="a.yaml b.yaml") on the GPU box (QUEUE=a100|h100)
	$(JOBQ) enqueue $(JOB) $(ARGS)

queue-status:       ## running (with progress/ETA), pending, last done/failed jobs and their durations (QUEUE=a100|h100)
	$(JOBQ) status

queue-pull:         ## results (new dirs only), ledger, EXPERIMENTS.md drafts, logs from the box (QUEUE=a100|h100)
	$(JOBQ) pull

queue-worker:       ## start the worker for GPU $(GPU) (default 0) in tmux on the box, if not running (QUEUE=a100|h100)
	$(JOBQ) start-worker --gpu $(or $(GPU),0)

queue-cancel:       ## cancel a pending job: make queue-cancel ID=<job id> (QUEUE=a100|h100)
	$(JOBQ) cancel $(ID)

queue-archive:      ## move done / failed / cancelled records out of queue-status (the ledger keeps them) (QUEUE=a100|h100)
	$(JOBQ) archive

queue-stats:        ## counts, GPU-hours used (last 24 h) and left, when the queue drains (QUEUE=a100|h100|all)
ifeq ($(QUEUE),all)
	@echo "== a100 ($(QUEUE_HOST_a100))"; JOBQ_HOST=$(QUEUE_HOST_a100) uv run python -m scripts.jobq stats --gpus $(QUEUE_GPUS_a100)
	@echo "== h100 ($(QUEUE_HOST_h100))"; JOBQ_HOST=$(QUEUE_HOST_h100) uv run python -m scripts.jobq stats --gpus $(QUEUE_GPUS_h100) || echo "(h100 queue not set up yet or box gone)"
else
	$(JOBQ) stats --gpus $(QUEUE_GPUS_$(QUEUE))
endif

examples-render:    ## examples/<exp>/ from the latest examples run of each experiment (no GPU)
	uv run python -m bridge_jspace.examples export

examples-serve:     ## render, then serve examples/ on http://localhost:$(PORT) and open it (PORT=8000)
	uv run python -m bridge_jspace.examples serve $(or $(PORT),8000)
