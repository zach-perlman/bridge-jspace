.PHONY: readme figures-kit install fmt lint typecheck test test-model check run data-report review-serve review-export review-summary review-verified verify-checks verify-independent verify-pack examples-render examples-serve enqueue queue-status queue-pull queue-worker queue-cancel queue-stats autonomy autonomy-status autonomy-off

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
	uv run pytest -n auto  # parallel (pytest-xdist): ~2.5 min instead of ~7

test-model:         ## integration tests on Qwen3.5-0.8B + its lenses (CPU ok, a few minutes)
	uv run pytest -m model

check: lint typecheck test

data-report:        ## what data we work with: counts, categories, labels, overlaps (add ARGS=--json)
	uv run python -m scripts.data_report $(ARGS)

# Job queue on a GPU box (scripts/jobq.py): make enqueue JOB=jobs/d2/d2_ko_v1.yaml (committed tree only).
# Which box: QUEUE=a100 (default: sesterce-a100x4, 4 GPUs), QUEUE=mats (sesterce-h100x2, 2x H100; rented 23 Oct for the
# 122B; QUEUE=h100 is the same box) or QUEUE=helper (sesterce-helper2, 1x H100 80GB HBM3, rented 28 Oct ~16:10; the 26 Oct helper is gone, its ledger kept) or QUEUE=speedup (sesterce-speedup, 1x H100 PCIe, rented 28 Oct ~16:20) or QUEUE=another (sesterce-another, 185.216.22.248, 1x H100 PCIe, rented 29 Oct ~00:20, replaces the helper, whose ledger is kept); each box
# has its own queue and ledger (results/jobq/ledger_<host>.jsonl); queue-stats also takes QUEUE=all.
# Example: make queue-stats QUEUE=h100
QUEUE ?= a100
QUEUE_HOST_a100 := sesterce-a100x4
QUEUE_HOST_h100 := sesterce-h100x2
QUEUE_HOST_mats := sesterce-h100x2
QUEUE_HOST_helper := sesterce-helper2
QUEUE_HOST_speedup := sesterce-speedup
QUEUE_HOST_another := sesterce-another
QUEUE_GPUS_a100 := 4
QUEUE_GPUS_h100 := 2
QUEUE_GPUS_mats := 2
QUEUE_GPUS_helper := 1
QUEUE_GPUS_speedup := 1
QUEUE_GPUS_another := 1
JOBQ = JOBQ_HOST=$(QUEUE_HOST_$(QUEUE)) uv run python -m scripts.jobq

enqueue:            ## queue a job spec (or several: JOB="a.yaml b.yaml") on the GPU box (QUEUE=a100|mats|helper|speedup|another)
	$(JOBQ) enqueue $(JOB) $(ARGS)

queue-status:       ## running (with progress/ETA), pending, last done/failed jobs and their durations (QUEUE=a100|mats|helper|speedup|another)
	$(JOBQ) status

queue-pull:         ## results (new dirs only), ledger, EXPERIMENTS.md drafts, logs from the box (QUEUE=a100|mats|helper|speedup|another)
	$(JOBQ) pull

queue-worker:       ## start the worker for GPU $(GPU) (default 0) in tmux on the box, if not running (QUEUE=a100|mats|helper|speedup|another)
	$(JOBQ) start-worker --gpu $(or $(GPU),0)

queue-cancel:       ## cancel a pending job: make queue-cancel ID=<job id> (QUEUE=a100|mats|helper|speedup|another)
	$(JOBQ) cancel $(ID)

queue-archive:      ## move done / failed / cancelled records out of queue-status (the ledger keeps them) (QUEUE=a100|mats|helper|speedup|another)
	$(JOBQ) archive

queue-stats:        ## counts, GPU-hours used (last 24 h) and left, when the queue drains (QUEUE=a100|mats|speedup|another|all; helper retired 29 Oct)
ifeq ($(QUEUE),all)
	@echo "== mats ($(QUEUE_HOST_mats))"; JOBQ_HOST=$(QUEUE_HOST_mats) uv run python -m scripts.jobq stats --gpus $(QUEUE_GPUS_mats) || echo "(mats queue not set up yet or box gone)"
	@echo ""; echo "== speedup ($(QUEUE_HOST_speedup))"; JOBQ_HOST=$(QUEUE_HOST_speedup) uv run python -m scripts.jobq stats --gpus $(QUEUE_GPUS_speedup) || echo "(speedup queue not set up yet or box gone)"
	@echo ""; echo "== another ($(QUEUE_HOST_another))"; JOBQ_HOST=$(QUEUE_HOST_another) uv run python -m scripts.jobq stats --gpus $(QUEUE_GPUS_another) || echo "(another queue not set up yet or box gone)"
else
	$(JOBQ) stats --gpus $(QUEUE_GPUS_$(QUEUE))
endif

# Claude Code autonomy window (.claude/autonomy/, not part of the experiments; stdlib only): no permission prompts for a
# while (e.g. overnight); the old limits come back by themselves at the deadline. git push / reset --hard / clean /
# rm -rf stay denied.
autonomy:           ## no permission prompts until the deadline: make autonomy HOURS=10 (or UNTIL=11:00)
	python3 .claude/autonomy/autonomy.py grant $(if $(HOURS),--hours $(HOURS)) $(if $(UNTIL),--until "$(UNTIL)")

autonomy-status:    ## is a window open, until when, watcher and caffeinate alive
	python3 .claude/autonomy/autonomy.py status

autonomy-off:       ## close the window now (the old limits back)
	python3 .claude/autonomy/autonomy.py revoke

review-serve:       ## the review dashboard (docs/review_views.yaml) on http://localhost:$(PORT) (SEED=7 PORT=8001; no GPU)
	uv run python scripts/review.py serve --seed $(or $(SEED),7) --port $(or $(PORT),8001)

review-export:      ## a static sample of every review view under review/seed-<SEED>/ (SEED=0 N=10; no GPU)
	uv run python scripts/review.py export --seed $(or $(SEED),0) --n $(or $(N),10)

review-summary:     ## docs/review_summary.md: items read by hand per view, flagged, seeds, automatic-check failures
	uv run python scripts/review.py summary

review-verified:    ## VERIFIED.md's generated section from review/marks.jsonl + the automatic checks + the independent recount
	uv run python scripts/verified.py

verify-checks:      ## automatic checks over every item of the tier-1 review views -> review/verify_checks.json (no GPU)
	uv run python scripts/verify_checks.py

verify-independent: ## the README's conflict-test and routes numbers recounted from scratch -> review/verify_independent.json
	uv run python scripts/verify_independent.py

verify-pack:        ## docs/verify_pack.md: how to review in 2 hours, the automatic checks, one section per tier-1 view
	uv run python scripts/verify_checks.py
	-uv run python scripts/verify_independent.py
	uv run python scripts/verify_pack_tier1.py

examples-render:    ## examples/<exp>/ from the latest examples runs; SEED=29 adds examples/review-seed-29/ (the items Dan read; no GPU)
	uv run python -m bridge_jspace.examples export $(if $(SEED),--seed $(SEED))

examples-serve:     ## render, then serve examples/ on http://localhost:$(PORT) and open it (PORT=8000)
	uv run python -m bridge_jspace.examples serve $(or $(PORT),8000)

figures-kit:        ## every figure-kit figure for both targets (figures/presentation/, figures/readme/): FIG="p1 p5" for some
	uv run python -m bridge_jspace.figkit.build $(FIG) --target slide
	uv run python -m bridge_jspace.figkit.build $(FIG) --target readme

readme: figures-kit ## the root README from docs/README.root.template.md (numbers and figures fill in)
	uv run python scripts/readme_root.py build
	uv run pytest -q tests/test_readme_sources.py
