# Data sources

| File | Source | Revision | sha256 | License |
|---|---|---|---|---|
| `probe_swap.json` | [anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens) `data/experiments/probe-swap.json` | `581d398613e5602a5af361e1c34d3a92ea82ba8e` | `a0edd27ca23f7b4d0fbe90448c2ddcc7457a3d812121bf024ed12a032ff86796` | Apache-2.0 |
| `entity_prompts.json` | Written for this repo by the coding agent (Claude, in a Cursor session); see the file's `meta` block | - | - | - |

`probe_swap.json` is the 90 two-hop prompts of the probe-swap experiment in Gurnee et al. (2026),
[Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace/index.html).
It is copied unchanged.

The J-lens is not stored here; it is downloaded at a pinned revision (see `src/bridge_jspace/pins.py`).
