# Results map

Where the final numbers, figures and examples of each experiment are. Everything is UNVERIFIED until it is in
`VERIFIED.md`. Each run directory holds its raw outputs (`manifest.json`, ranks / grids, `items.jsonl`); its
`analysis-*` folder is the current aggregation of those outputs (rerun with the experiment's `analyze`).

## Part A on Qwen3.6-27B (current)

| Experiment | Question | Final numbers | Final figures | Worked examples |
|---|---|---|---|---|
exp11 and exp12 use the trailing-space-stripped prompts and part B's v4 labels (77 eligible: the greedy continuation
contains the answer). Each of those runs' own `summary.json` is current; its `analysis-*` folder holds the figures as
re-rendered with the current plotting code.

| Experiment | Question | Final numbers | Final figures | Worked examples |
|---|---|---|---|---|
| exp10_lens_sanity | Does a lens read two-hop intermediates at all? (lens-eval multihop, last token) | `exp10_lens_sanity/20261013-205936/summary.json` (space stripped; `-205736` as published) | `../figures/exp10_lens_sanity/20261015-123717/pass_at_10_by_model.png`, `27b_by_layer.png` | `../examples/exp10_lens_sanity/index.html` (data: `exp10_lens_sanity/20261014-134942/examples.json`) |
| exp11_bridge_vs_answer_by_layer | At the last token, at which layers are the bridge and the answer readable? | `exp11_bridge_vs_answer_by_layer/20261015-100110/summary.json` (J-lens swap labels; `20261015-100426`: J++ swap labels, same ranks) | `../figures/exp11_bridge_vs_answer_by_layer/`: `pool_top1_by_layer.png`, `advantage_by_layer.png` (from `20261015-100110/analysis-20261015-122817/`) | `../examples/exp11_bridge_vs_answer_by_layer/index.html` (data: `exp11_bridge_vs_answer_by_layer/20261015-103149/examples.json`) |
| exp12_position_map | Where in the prompt, and how deep, are they readable? | `exp12_position_map/20261015-100735/summary.json` (J-lens swap labels; `20261015-100947`: J++ swap labels, same grids) | `../figures/exp12_position_map/`: **`two_step.png`** (headline), `layers_at_positions_jlens.png`, `by_offset.png`, `position_layer.png` (from `20261015-100735/analysis-20261015-122822/`) | `../examples/exp12_position_map/index.html` (data: `exp12_position_map/20261015-103055/examples.json`) (published: https://claude.ai/artifact/TXLZH6WxuxSQDhoK5YHTj9, anyone with the link) |

Variants and earlier runs:
- Prompts as published with part B's earlier (v3) labels, 67 eligible: exp11 `20261014-092835/analysis-20261014-113947/`,
  exp12 `20261014-095358/analysis-20261014-121341/` (their own `summary.json` predates later metrics; use the
  `analysis-*` one). Examples from those: exp11 `20261014-134854`, exp12 `20261014-134702`.
- exp11 stripped with the v3 labels: `exp11_bridge_vs_answer_by_layer/20261014-093050/analysis-20261014-113952/`.
- exp10 on Qwen3.5-4B: runs `20261013-205029` (as published) and `20261013-205057` (stripped).
- Per-run exp10 figures: `exp10_lens_sanity/<run>/figures-*/multihop_pass_at_k.png`.

Notes:
- `figures/exp11_*` and `figures/exp12_*` are copies of the PNGs in the analysis folders above (the source of record).
- Examples runs keep the data (`examples.json`) and the interactive jlens pages (`slices/`, gitignored); the pages
  to read are rendered into `../examples/` by `make examples-render` (`make examples-serve` opens them).

## Part B (Zach)
- **v4 (current):** J-lens and J++ on shared probes (`exp01_probes/v3_jlens`, `v3_jpp`), stripped prompts, answers
  judged on the greedy continuation, 77 eligible. Gate `exp02_swaps/gate_v4`; main runs `exp02_swaps/main_v4_{jlens,jpp}`
  (24-40), `*_32-48`, and position runs `*_pos-{prev,last,last_two,earlier}`; reports in `exp02_swaps/analysis/<run>/`.
  Figures: `../figures/exp02_swaps/v4/` (`jpart_vs_remainder.png` and `swap_position.png` are the headline ones;
  rebuilt with `uv run python scripts/exp02_figures.py <new folder>`).
- **exp03_brew_swaps:** in-context two-step lookups (WorkspaceBench's brew bank). Runs `sweep`, `main`, `followup`,
  `start_steer`, `start_steer_low` under `exp03_brew_swaps/`; figures `../figures/exp03_brew_swaps/v1/`
  (`uv run python scripts/exp03_figures.py <new folder> followup start_steer start_steer_low`). Then `swap_amp`
  (amplified swaps; `swap_early` is its void predecessor, see the main README) and `fresh_steer` (held-out items,
  `data/brew_fresh.json`); figures `v2_swaps/` and `v2_fresh/` (one run each: the runs use different item sets).
- **exp04_brew_patch:** lens-free activation patching of brew's two-step lookup (counterfactual rule tables, one
  layer and position group at a time). Run `patch_map` under `exp04_brew_patch/`; figures
  `../figures/exp04_brew_patch/v1/` (`uv run python scripts/exp04_figures.py <new folder> patch_map`).
- exp02 controls for "the J-space part flips more because it carries more of the probe": `exp02_swaps/
  matched_v4_{jpp,jlens}` (matched-alignment random directions) and `exp02_swaps/analysis/edit_size_v1/`
  (`scripts/exp02_edit_size.py`, no model).
- exp02 figures with the cue regimes: `../figures/exp02_swaps/v4b/` (same as `v4/` plus the cue split).
- v3 (superseded by v4): exp02_swaps main report `exp02_swaps/analysis/main/REPORT_auto.md`; labels used by
  exp11/exp12: `exp02_swaps/main/labels.csv`; figure: `../figures/exp02_swaps/main/flip_rates.png`.
