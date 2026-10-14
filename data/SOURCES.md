# Data sources

Provenance, revisions, checksums and licences. What each dataset is and how much of it there is: [README.md](README.md).

| File | Source | Revision | sha256 | License |
|---|---|---|---|---|
| `probe_swap.json` | [anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens) `data/experiments/probe-swap.json` | `581d398613e5602a5af361e1c34d3a92ea82ba8e` | `a0edd27ca23f7b4d0fbe90448c2ddcc7457a3d812121bf024ed12a032ff86796` | Apache-2.0 |
| `lens_eval_multihop.json` | [anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens) `data/evaluations/lens-eval-multihop.json` | `581d398613e5602a5af361e1c34d3a92ea82ba8e` | `50b7e4c9255291c0ca2a8e94615be9f44531fa57bb1a844e4f9616056d987416` | Apache-2.0 |
| `entity_prompts.json` | Written for this repo by the coding agent (Claude, in a Cursor session); see the file's `meta` block | - | - | - |
| `entity_prompts_topup.json`, `entity_prompts_more/part*.json` | Written for this repo (rounds 2 and 3, coding agents in Cursor sessions); see each file's `meta` block | - | - | - |

`probe_swap.json` is the 90 two-hop prompts of the probe-swap experiment in Gurnee et al. (2026),
[Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace/index.html).
It is copied unchanged.

`lens_eval_multihop.json` is the paper's lens-quality eval for two-hop prompts (93 items: `prompt`, `target`,
`intermediates`; readout at the token before `target`, pass@k over min-over-layers rank). Copied unchanged.

Models and lenses (J-lens, J++) are not stored here; they are downloaded at pinned revisions (see
`configs/models/*.yaml`). Data files are sha256-checked on load (`src/bridge_jspace/pins.py`).
