# Developer guide

How the repo is laid out and how to run, re-analyse and publish things. The research itself (question, setup,
results) is in [README.md](README.md); the rules for agents running experiments are in [AGENTS.md](AGENTS.md).

## Layout
```
src/bridge_jspace/        shared library
  config.py               typed YAML configs + dotted CLI overrides (model=<yaml> swaps the whole model)
  models.py               pinned HF model -> jlens LensModel; J-lens / J++ files (same format) moved to GPU once
  readout.py              rank-only readouts (logit lens, J-lens, J++), word -> token ids, pool ranks
  items.py                probe-swap items joined with part B's labels; entity / answer candidate pools
  sanity.py               the gate every run passes first (known fact, HF parity, readout == jlens.apply)
  experiment.py           Experiment base: results/<exp>/<timestamp>/, manifest.json written before run()
  stats.py                Wilson and bootstrap CIs
  plotting.py             shared figure frame (title, data note, percent axes, legend) and colours
  examples.py             worked-example runs and their HTML / Markdown pages
  pins.py                 pinned upstream data, sha256-checked on load
  run.py                  `bj-run`: config -> experiment
  model.py, lens.py, clamp.py, omp.py, tokens.py, data.py   part B (probes, decomposition, swaps)
scripts/
  exp10_lens_sanity/ ... exp13_greedy_answers/   part A: config.yaml + experiment.py (+ plot.py, examples.yaml)
  exp01_probes.py, exp02_*.py, exp03_*.py, exp04_*.py   part B
  verify_headlines.py     recomputes every README headline from the raw run files, independently of the code
  data_report.py          the counts data/README.md quotes (`make data-report`)
  prefetch.py             download a model YAML's snapshot + lenses, retrying on HF rate limits
  run.sh                  an experiment in a detached tmux session, log in log/
configs/models/           one YAML per model: HF revision + lens files (qwen3.5-0.8b / 2b / 4b, qwen3.6-27b)
data/                     pinned inputs; catalogue in data/README.md, provenance in data/SOURCES.md
results/<exp>/<stamp>/    raw run outputs (never edited); analysis-*/ = re-aggregations; map in results/README.md
figures/<exp>/            the final figures the README shows (copies from analysis-*/)
examples/                 rendered worked-example pages (slices/ not committed)
tests/                    unit tests (`make check`) and model tests on Qwen3.5-0.8B (`make test-model`)
infra/setup_pod.sh        GPU box bootstrap
cache/, log/              not committed: smoke runs and intermediates, run logs
```

## Checks
```bash
make install       # uv sync + pre-commit hooks
make check         # ruff format + lint, pyright, unit tests (no download)
make test-model    # integration on Qwen3.5-0.8B + its lenses (CPU ok, a few minutes); after readout/sanity changes
uv run python scripts/verify_headlines.py   # every README headline, recomputed from the raw files
```

## Running an experiment
Every run goes through one config and a detached tmux session; the manifest is written before the run and the run
never overwrites an earlier one.
```bash
make run CONFIG=scripts/exp11_bridge_vs_answer_by_layer/config.yaml          # Qwen3.6-27B, the README's setup
make run CONFIG=scripts/exp10_lens_sanity/config.yaml ARGS="model=configs/models/qwen3.6-27b.yaml"
tmux attach -t <session>     # or: tail -f log/<session>.log
uv run bj-run scripts/exp11_bridge_vs_answer_by_layer/config.yaml \
    model=configs/models/qwen3.5-0.8b.yaml params.limit=6 results_dir=cache/smoke   # CPU smoke
```
Each config's header lists its variants (e.g. exp11 split by the J++ swaps). Defaults follow the shared setup in the
README: trailing space stripped, part B's v4 labels, bands 32-48 (primary) and 24-40.

## Job queue on the GPU box
GPU runs can be queued instead of started by hand (`scripts/jobq.py`). A job is a spec, `jobs/<thread>/<id>.yaml`, committed before the run: `command`, `gpus` (1; a job with `gpus: 2` runs on a worker that owns two GPUs, `start-worker --gpus 0,1`, and its command splits the model over them with `BJ_DEVICE_MAP=auto`), `mem_gb` (free GPU memory to wait for, in total over the job's GPUs; default 70 for the 27B), `est_gpu_hours`, `depends_on`, `examples_command`, `figures_command` (required in practice: every experiment ends with figures), and the pre-registration: `question`, `why_it_matters`, `hypotheses` (name -> predicted numbers), `decision_rule`, `controls`, `n`, `seeds`. `make enqueue` refuses a dirty tree, an id already used or a run name (`--name` in the command) already in the box's results/ (`ARGS=--reuse-names` for a command that only reads that run), pushes the commit to a bare repo on the box (not GitHub) and queues the spec.
```bash
make queue-worker                      # once per box/GPU: tmux session jobq-gpu0 on the box (GPU=N for others)
make enqueue JOB=jobs/d2/d2_ko_v1.yaml # or JOB="a.yaml b.yaml"
make queue-status                      # running (last progress line), pending (why waiting), recent done/failed
make queue-pull                        # results (new dirs only), results/jobq/{ledger.jsonl,drafts/}, log/jobq/
make queue-cancel ID=d2_ko_v1          # pending jobs only
make examples-render                   # job pages: examples/job_<id>/ beside the lens-example pages
```
The worker takes jobs first in, first out once their dependencies are done and the GPU has `mem_gb` free (it waits,
never kills), runs each in a fresh checkout of its commit (earlier jobs' results copied in; `cache/` and `.env` shared
with `~/bridge-jspace`), and appends to the ledger: queued/started/ended, setup/run/examples time, exit codes, peak GPU
memory, new results dirs, W&B links. Each finished job gets a draft EXPERIMENTS.md row (`results/jobq/drafts/`) whose
result and verdict a human writes. A script's `figures` stage writes PNGs into a new `analysis-*/` folder of the run
(the job page shows the newest such folder's figures). A script's `examples` stage writes `examples.json` (schema in
`src/bridge_jspace/job_pages.py`), which the job page shows with the pre-registered predictions.

## Re-analysing a finished run (no GPU)
Each part A experiment has an `analyze` command that re-aggregates a run's saved ranks with the current code into a
new `<run>/analysis-<timestamp>[-<kind>]/` (summary.json and, for exp11/exp12, figures; exp12's kinds: `-position-map`,
and `-cue-phrase` from `scripts.exp12_position_map.cue`):
```bash
uv run python -m scripts.exp10_lens_sanity.experiment analyze results/exp10_lens_sanity/<run>
uv run python -m scripts.exp11_bridge_vs_answer_by_layer.experiment analyze results/exp11_bridge_vs_answer_by_layer/<run>
uv run python -m scripts.exp12_position_map.experiment analyze results/exp12_position_map/<run>
uv run python -m scripts.exp10_lens_sanity.plot --summary    # exp10's README figures -> figures/exp10_lens_sanity/<stamp>/
```
Then copy the PNGs the README uses into `figures/<exp>/` and point `results/README.md` at the new analysis folder.

## Worked examples
```bash
make run CONFIG=scripts/exp12_position_map/examples.yaml   # GPU: results/<exp>/<stamp>/examples.json + slices/
make examples-render                                       # examples/<exp>/ from the latest examples run (no GPU)
make examples-serve                                        # render, serve examples/ on localhost:8000, open it
```
The verbalizer pages (exp15 oracle lens, exp16 NLA) are rendered from their runs' readings (no examples run, no GPU):
`uv run python -m scripts.exp15_oracle_lens.examples results/<exp>/<run> [<run> ...]`; `make examples-render` puts
their texts under the exp10-12 cards (`bridge_jspace.examples.VERBALIZERS`).
On a pod, `make examples-serve` plus `ssh -L 8000:localhost:8000 sesterce-a100` shows the pages locally. The exp12
page is published at https://claude.ai/artifact/TXLZH6WxuxSQDhoK5YHTj9: to update it, publish
`examples/exp12_position_map/artifact.html` to that URL with the examples run's `slices/*` as files.

## GPU box
```bash
git clone <repo> && cd bridge-jspace && bash infra/setup_pod.sh   # uv, caches, CUDA check, prefetch (MODEL_CONFIG=...)
uv run python scripts/prefetch.py configs/models/qwen3.6-27b.yaml # model + lenses ahead of a run; HF_TOKEN in .env
```
Memory: Qwen3.5-4B fits a 24 GB card; Qwen3.6-27B needs one 80 GB card (bf16 weights ~54 GB + two fp32 lens maps
~13 GB). The Linux torch build is cu126, so Blackwell cards (RTX Pro 6000, RTX 5090) need a different torch index
first. One large model on the GPU at a time.
