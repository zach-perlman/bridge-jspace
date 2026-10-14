# Results map

Where the final numbers, figures and examples of each experiment are. Everything is UNVERIFIED until it is in
`VERIFIED.md`. Each run directory holds its raw outputs (`manifest.json`, ranks / grids, `items.jsonl`); its
`analysis-*` folder is the current aggregation of those outputs (rerun with the experiment's `analyze`).

## Part A on Qwen3.6-27B (current)

| Experiment | Question | Final numbers | Final figures | Worked examples |
|---|---|---|---|---|
| exp10_lens_sanity | Does a lens read two-hop intermediates at all? (lens-eval multihop, last token) | `exp10_lens_sanity/20261013-205936/summary.json` (space stripped; `-205736` as published) | `../figures/exp10_lens_sanity/20261013-230247/pass_at_10_by_model.png`, `27b_by_layer.png` | `exp10_lens_sanity/20261014-134942/examples.html` |
| exp11_bridge_vs_answer_by_layer | At the last token, at which layers are the bridge and the answer readable? | `exp11_bridge_vs_answer_by_layer/20261014-092835/analysis-20261014-113947/summary.json` | `../figures/exp11_bridge_vs_answer_by_layer/`: `pool_top1_by_layer.png`, `advantage_by_layer.png` | `exp11_bridge_vs_answer_by_layer/20261014-134854/examples.html` |
| exp12_position_map | Where in the prompt, and how deep, are they readable? | `exp12_position_map/20261014-095358/analysis-20261014-121341/summary.json` | `../figures/exp12_position_map/`: **`two_step.png`** (headline), `position_layer_jlens.png`, `by_offset.png`, `position_layer.png` | `exp12_position_map/20261014-134702/examples.html` (published: https://claude.ai/artifact/TXLZH6WxuxSQDhoK5YHTj9, private) |

Variants and side runs:
- exp11 with the trailing space stripped: `exp11_bridge_vs_answer_by_layer/20261014-093050/analysis-20261014-113952/`.
- exp10 on Qwen3.5-4B: runs `20261013-205029` (as published) and `20261013-205057` (stripped).
- Per-run exp10 figures: `exp10_lens_sanity/<run>/figures-20261013-23014*/multihop_pass_at_k.png`.

Notes:
- `figures/exp11_*` and `figures/exp12_*` are copies of the PNGs in the analysis folders above (the source of record).
- The exp11 and exp12 runs' own `summary.json` predate later metrics (named bands, emergence order, crossings, the
  two-step lag); use the `analysis-*` one.
- Example runs keep the interactive jlens pages in `slices/`, which is gitignored (regenerate with
  `make run CONFIG=scripts/<exp>/examples.yaml`).

## Part B (Zach)
- exp02_swaps main report: `exp02_swaps/analysis/main/REPORT_auto.md`; labels used by exp11/exp12:
  `exp02_swaps/main/labels.csv`; figure: `../figures/exp02_swaps/main/flip_rates.png`.
