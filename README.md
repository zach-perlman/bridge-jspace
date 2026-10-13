# bridge-jspace

**Question.** In a two-hop question ("the language spoken in the country where the Amazon River ends is ..."), the
model has to compute a bridge entity (Brazil) before it can answer (Portuguese). On Qwen3.6-27B and Gemma 4 31B the
J-lens often cannot read that bridge. Does the bridge still act on the answer through the J-space, or through a part
of the representation the J-lens cannot read?

**Reference result (Claude, Gurnee et al. 2026,
[Verbalizable Representations Form a Global Workspace](https://transformer-circuits.pub/2026/workspace/index.html)).**
Swapping the bridge's probe for another entity's flips the answer in 61% of items when only the J-space part of the
probe is swapped, 28% for the remainder, and 6% for the remainder when the J-space coordinates are clamped.

**Reading.** If on open models the remainder flips about as often as the J-space part and survives the clamp, the
bridge works outside the workspace. If the numbers look like Claude's, the J-lens misses on open models are a read-site
or tokenization artifact.

## Method, part A: can any reader see the bridge? (exp10+)
1. `exp10_lens_sanity`: the lens works on this model. Sanity gate (known fact, HF parity, our readout == jlens's
   `apply`), then `lens-eval-multihop` pass@k for the J-lens and J++ against the logit lens, plus a bridge vs
   same-category distractor control. Debugged on Qwen3.5-0.8B/4B (same `qwen3_5` hybrid architecture), then
   Qwen3.6-27B.
2. Where the bridge is readable: rank of the bridge vs a distractor at every layer x position (planned).
3. Oracle lens and NLA on the same items, split by part B's J-mediated / non-J labels (planned).

## Method, part B: is the bridge used outside the J-space? (exp01-09)
1. `data/entity_prompts.json`: about 8 prompts per entity that imply the entity without naming it, for the 97
   entities in `data/probe_swap.json` (bridges and swap targets). Qwen keeps the ones it answers correctly.
2. Probe per entity and layer: mean final-token residual over its kept prompts minus the mean over all entities.
3. Decomposition per layer: non-negative OMP (k=25) over J-lens token directions gives the J-space part; the remainder
   is the rest.
4. Swaps on the 90 two-hop items, at every band layer and prompt position, under five conditions: raw J-lens vectors,
   full probe, J-space part, remainder, remainder with the J-space coordinates clamped. Each has a random-direction
   control of the same edit norm. Metric: rate at which the swap answer becomes the top word, with Wilson 95% CIs.

## Layout
```
src/bridge_jspace/
  config.py       typed YAML configs + dotted CLI overrides (model=<yaml> swaps the whole model)
  models.py       pinned HF model -> jlens LensModel; lens / J++ files (same format) moved to GPU once
  readout.py      rank-only readouts (J-lens, J++, logit lens), word -> token ids
  sanity.py       checks every new model/pod must pass before any readout is trusted
  stats.py        Wilson and bootstrap CIs
  experiment.py   Experiment base: results/<exp id>/<timestamp>/, manifest.json before run()
  pins.py         pinned upstream data, sha256-checked on load
configs/models/   one YAML per model: HF revision + lens files (qwen3.5-0.8b / 2b / 4b, qwen3.6-27b)
experiments/      expNN_name/config.yaml + experiment.py
scripts/run.sh    experiment in a detached tmux session, log in log/
infra/            pod bootstrap
```
`AGENTS.md`: rules for running experiments. `VERIFIED.md`: results a human has checked.

## Running
```bash
make install                 # uv sync + pre-commit hooks
make check                   # ruff + pyright + unit tests (no download)
make test-model              # integration on Qwen3.5-0.8B + its lenses (CPU ok)

# GPU box: bash infra/setup_pod.sh, then any experiment = one config, run in tmux:
make run CONFIG=experiments/exp10_lens_sanity/config.yaml                      # Qwen3.5-4B
make run CONFIG=experiments/exp10_lens_sanity/config.yaml ARGS="model=configs/models/qwen3.6-27b.yaml"
tmux attach -t <session>     # or: tail -f log/<session>.log
```
GPU memory: Qwen3.5-4B fits a 24 GB card; Qwen3.6-27B needs 1x 80 GB (bf16 weights ~54 GB + two fp32 lens maps
~13 GB).

## Status
See the STATE block in `AGENTS.md`. Nothing is verified yet.
