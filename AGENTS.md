# AGENTS.md

Instance/ops guide (Vast): /workspace/AGENTS.md; this file adds project rules on top.

## STATE (human-maintained; update at every close)
Question: on open models (Qwen3.6-27B first), does the bridge entity of a two-hop question act on the answer through
the J-space, or through a part of its representation the J-lens cannot read?
Established so far (exp ids): none verified.
In flight: exp01_probes (bridge probes and their J-space decomposition), exp02_swaps (swap conditions).

## Roles
- Agent: implement, run, report in the format below.
- Humans: design experiments, choose baselines and controls, read raw data, recompute headlines, interpret.
  If you think a design is wrong, say so, propose an alternative, and wait.

## Environment
- Python: the uv project env only (`uv run ...`; `uv add ... --dry-run` first, then without). Never pip install.
  New pod: `bash infra/setup_pod.sh`. Before finishing a change: `make check`; if models/readout/sanity changed,
  also `make test-model` (Qwen3.5-0.8B, CPU ok).
- One large model on the GPU at a time. Every experiment run goes through `make run CONFIG=... ARGS="..."`
  (`scripts/run.sh`): a detached tmux session, output tee'd to `log/`, progress bars with ETA.
- Pinned inputs: model snapshot and lens files in `configs/models/*.yaml`; upstream data in
  `src/bridge_jspace/pins.py` (sha256-checked on load) and `data/SOURCES.md`. Change a pin only with a new manifest.
- What data we work with: `data/README.md` (catalog, lens fitting data); `make data-report` recomputes its counts.
- Repo layout, commands, re-analysis and publishing: `DEVELOPER.md`.

## Experiments
- Every experiment: id expNN_name, directory results/expNN_name/<timestamp>/, manifest.json written BEFORE the run
  (`Experiment.setup`). exp01-09: part B (probes, swaps); exp10+: part A (who can read the bridge).
- All experiment code lives in `scripts/`, all outputs in `results/expNN_name/`. Part A: `scripts/expNN_name/`
  (config.yaml + experiment.py, run with `make run`). Part B: `scripts/expNN_*.py` (`uv run python scripts/...`),
  pins in `pins.py`; `tests/test_pins.py` keeps the pins shared with `configs/models/` in sync.
- Never overwrite or hand-edit results. Each analysis or figure run goes in a new folder.
- Always run the control the humans specified. If none was specified, stop and ask.
- Report n, seeds, CI, and the baseline next to every headline number.
- Cache expensive intermediates in cache/ (not committed).

## Report format (end of every experiment)
EXP <id> @ <commit> | model <id> | n=<n> | seeds=<list>
Claim tested:
Headline: <metric> = <value> [CI]   Baseline: <value> [CI]   Control: <value> [CI]
Figures:
Three dumbest ways this could be wrong: 1) ... checked? 2) ... checked? 3) ... checked?
For the human to verify: <file, rows, number to recompute>
Status: UNVERIFIED until a human adds it to VERIFIED.md

## Evidence norms
- Recomputed rates > plotted curves > judge scores. Label any judge score "judge".
- Random examples by fixed seed, stated as such.
- Interventions at matched norm/dose; report collateral damage (the clean answer lost) alongside the effect.
- A null with a working control is a result.

## Git and writing
- Commit when a figure exists (exp id in the message) and again when verified. No force-push; no amending pushed
  commits. Push only after a human OK.
- Drafts only. Never state a result as established unless it is in VERIFIED.md. No filler.
