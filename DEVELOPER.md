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
  verify_headlines.py     the 30 Oct sprint's headlines (exp02-exp23) from the raw run files; not the current READMEs
  data_report.py          the counts data/README.md quotes (`make data-report`)
  prefetch.py             download a model YAML's snapshot + lenses, retrying on HF rate limits
  run.sh                  an experiment in a detached tmux session, log in log/
configs/models/           part A's model YAMLs, HF revision + lens files: six (muse-glimmer-30b,
                          olmo-hybrid-7b-instruct-dpo, qwen3.5-0.8b / 2b / 4b, qwen3.6-27b); the other models
                          are TARGETS entries in src/bridge_jspace/pins.py, chosen with BJ_TARGET (default qwen3.6-27b)
data/                     pinned inputs; catalogue in data/README.md, provenance in data/SOURCES.md
results/<exp>/<stamp>/    raw run outputs (never edited); analysis-*/ = re-aggregations; map in results/README.md
figures/<track>/<set>/    the published figures by track (breadth, depth, common), one numbered set per document
                          (figkit/layout.py; `make readme`, `make figures-writeup`)
examples/                 rendered worked-example pages (slices/ not committed)
tests/                    unit tests (`make check`) and model tests on Qwen3.5-0.8B (`make test-model`)
infra/setup_pod.sh        GPU box bootstrap
cache/, log/              not committed: smoke runs and intermediates, run logs
```

## Reproduce
The README's tiers in detail. Each tier is measured in its own fresh blob-less sparse clone by `uv run python scripts/measure_reproduce.py --cold-uv-cache` (uv sync into an empty package cache); the measured values are not typed here: they are the `repro.*` keys of [data/figures/reproduce.csv](data/figures/reproduce.csv), named below, and each row's source says how it was measured. `repro.commit` is the commit measured (its source names the URL: `--url file://$PWD --branch <branch>` measures a local commit not yet pushed), `repro.hw.*` the machine. The sparse sets are `TIERS` in that script (`python3 scripts/measure_reproduce.py paths <tier>` prints one). The whole tracked `results/` is `repro.results_all_gb` GB in `repro.results_all_files` files; no tier needs all of it.

**Read only (no Python).** The READMEs, docs, figures and the figures' data files. Time `repro.read.time_s`; disk `repro.read.files_mb` of files and `repro.read.git_mb` of `.git`. Of the README's `repro.read.links` local links, `repro.read.links_dead` fall outside this set (the row names them; add their folders to the sparse set).
```bash
git clone --filter=blob:none --sparse https://github.com/zach-perlman/bridge-jspace
cd bridge-jspace && git sparse-checkout set docs figures data/figures
```

**Tier one: the figures and READMEs from tracked numbers (CPU).** `make readme` rebuilds the three READMEs and their figures from the tracked data files and the run folders behind them (`repro.t1.results_folders` folders, `repro.t1.results_mb` MB), found by tracing every file its scripts open; the set includes tier two's, since `make readme` ends with the same tests. Its first step, `scripts/provenance_counts.py`, counts only run folders whose `manifest.json` git tracks; in a checkout that lacks their files (a sparse clone such as the read-only set) it prints that it skipped and keeps the committed data/figures/provenance.csv, and in a blob-less clone it keeps the committed `g1.*` rows (counts of two fixed commits) instead of running `git archive` on those commits, which fetched nearly every blob of a commit. Clone `repro.t1.clone_s` s, `uv sync` `repro.t1.sync_s` s, `make readme` `repro.t1.readme_s` s (exit `repro.t1.exit`); disk `repro.t1.files_mb` MB of files, `repro.t1.venv_mb` MB of uv env, `repro.t1.git_mb` MB of `.git`. `repro.t1.changed` names the tracked files the rebuild changed, and `repro.t1.changed_other` counts the changed words other than the build stamp ("Built at <commit>").
```bash
git clone --filter=blob:none --sparse https://github.com/zach-perlman/bridge-jspace && cd bridge-jspace
git sparse-checkout set scripts && git sparse-checkout set $(python3 scripts/measure_reproduce.py paths tier1)
uv sync && make readme
```

**Tier two: the READMEs' numbers checked against the repo (CPU).** `make check-numbers` runs the tests that check where each number on README.md, docs/depth/README.md and docs/breadth/README.md comes from (tests/test_readme_sources.py, tests/test_numbers_match_data.py): every `<!-- src: file | key -->` comment names a file git tracks and its key resolves there (a csv key is a cell, a json key a key at any depth, `l.N` a line count, `a :: b` parts on one line of the file, anything else the text); every run file named in the source column of a cited data row (or docs/depth/x0_numbers.json entry) is tracked by git; the lens table's pass@10 values are the cells their sources name; every number of the depth README is a value of data/figures/depth/data.csv. It does not recompute the numbers from the raw run files: tier one rebuilds them from the tracked data files and tier three reruns the experiments. It reads `repro.t2.run_folders` run folders (`repro.t2.run_mb` MB). Clone `repro.t2.clone_s` s, `uv sync` `repro.t2.sync_s` s, the tests `repro.t2.test_s` s (`repro.t2.passed` passed, `repro.t2.failed` failed, exit `repro.t2.exit`); disk `repro.t2.files_mb` MB of files, `repro.t2.venv_mb` MB of uv env, `repro.t2.git_mb` MB of `.git`.
```bash
git sparse-checkout set scripts && git sparse-checkout set $(python3 scripts/measure_reproduce.py paths tier2)
uv sync && make check-numbers
```

**The sprint's headline check (30 Oct, not this page's numbers).** `scripts/verify_headlines.py` recomputes the 30 Oct sprint's part A and part B headlines (exp02-exp23) from the raw run files, against values typed into the script; it does not check the current READMEs. Some of the run files it reads are in no commit, so it stops at the first one (exit `repro.sprint.exit`). Check by check (`uv run python scripts/measure_reproduce.py each .`): `repro.sprint.ok` of `repro.sprint.checks` checks match, `repro.sprint.diff` differ and `repro.sprint.missing` need one of `repro.sprint.missing_files` run files in no commit. No number on the three READMEs depends on those files (tier two checks that every run file behind them is tracked).
```bash
git sparse-checkout set scripts && git sparse-checkout set $(python3 scripts/measure_reproduce.py paths sprint)
uv sync && uv run python scripts/verify_headlines.py
```

**Tier three: the runs (GPU).** `make run CONFIG=…` on a GPU box (see "Running an experiment", "Job queue on the GPU box" and "GPU box" below). Qwen3.5-4B fits a 24 GB card; Qwen3.6-27B needs one 80 GB card. Not re-run for this page.

## Checks
```bash
make install       # uv sync + pre-commit hooks
make check         # ruff format + lint, pyright, unit tests (no download)
make test-model    # integration on Qwen3.5-0.8B + its lenses (CPU ok, a few minutes); after readout/sanity changes
make check-numbers # every number on the three READMEs traced to a tracked file and key (Reproduce, tier two)
uv run python scripts/verify_headlines.py   # the 30 Oct sprint's headlines from the raw files, not the current READMEs
```

## Hand check (review dashboard, docs/review/review_views.yaml; CPU only)
```bash
make verify-pack              # verify-checks + verify-independent, then docs/review/verify_pack.md (how to review, findings, views)
make verify-checks            # automatic checks over every item of the tier-1/2 views -> review/verify_checks.json
make verify-independent       # README conflict-test / routes numbers recounted from scratch -> review/verify_independent.json
make review-serve SEED=29     # the dashboard at :8001; the fixed sample (seed 29, views file fixed_sample); marks -> review/marks.jsonl
make review-export SEED=29 N=10   # the same pages as static HTML under review/seed-29/
make review-summary           # docs/review/review_summary.md from the marks (verdicts only; J-space notes skipped)
make review-verified          # VERIFIED.md's generated block from the marks (Dan runs it after his marks)
make examples-render SEED=29  # also examples/review-seed-29/: the items read, for the write-up
```

## Writing results
The shared documentation standard is [docs/STANDARD.md](docs/STANDARD.md). This repo's rules on top of it:

- The three READMEs are generated. Edit their templates, [docs/readme/README.template.md](docs/readme/README.template.md) (the root README), [docs/depth/README.template.md](docs/depth/README.template.md) and [docs/breadth/README.template.md](docs/breadth/README.template.md), then run `make readme`. Never edit README.md, docs/depth/README.md or docs/breadth/README.md by hand: the next build overwrites them.
- Never type a number. Every number comes from a data file by key, through a template marker that prints the value with its source comment. Each builder's docstring lists its markers: `scripts/readme_root.py` (root), `scripts/readme_build.py` (depth), `scripts/report_breadth.py` (breadth). A new number goes into its data file first, with its source, and the template cites its key.
- Keep every `<!-- src: ... -->` comment: it names the file and key a number came from, and `tests/test_readme_sources.py` resolves each one in the three READMEs (`make check-numbers`).

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
memory, new results dirs, W&B links. Each finished job gets a draft row for docs/archive/EXPERIMENTS.md (the run log) (`results/jobq/drafts/`) whose
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
uv run python -m scripts.exp10_lens_sanity.plot --summary    # exp10's README figures -> figures/pre-sprint/exp10_lens_sanity/<stamp>/
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
