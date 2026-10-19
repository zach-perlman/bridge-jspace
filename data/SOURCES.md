# Data sources

Provenance, revisions, checksums and licences. What each dataset is and how much of it there is: [README.md](README.md).

| File | Source | Revision | sha256 | License |
|---|---|---|---|---|
| `probe_swap.json` | [anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens) `data/experiments/probe-swap.json` | `581d398613e5602a5af361e1c34d3a92ea82ba8e` | `a0edd27ca23f7b4d0fbe90448c2ddcc7457a3d812121bf024ed12a032ff86796` | Apache-2.0 |
| `brew_intermediates.json` | [camilablank/workspace-bench](https://github.com/camilablank/workspace-bench) `evals/brew_intermediates/items.json` | `92d763e722377f5bfae045e829a308ab5919a820` | `183be95d4182c373674786b7610820520e56434fb0c15a75a62dad854bed9d83` | MIT |
| `brew_fresh.json` | Generated for this repo: `scripts/exp03_make_items.py --n 200 --seed 1`, in the format of `brew_intermediates.json` (ungated; exp03 keeps the greedy-correct ones) | - | `1e20ed25b3727842acba0806b346d91d991db1fa31f42f514e537fb3ab000d3c` | - |
| `brew_fit.json` | Generated for this repo: `scripts/exp03_make_items.py --name brew_fit --prefix brewfit --n 1000 --seed 2`, in the format of `brew_intermediates.json`, no prompt of the bank or of `brew_fresh.json` (ungated; exp07 fits its code on the greedy-correct ones) | - | `b9ab169a50bf576d71c074b31516f283e3163366d8ce2aea0907addbdf0e2659` | - |
| `brew_test.json` | Generated for this repo: `scripts/exp03_make_items.py --name brew_test --prefix brewtest --n 600 --seed 3`, in the format of `brew_intermediates.json`, no prompt of the bank, `brew_fresh.json` or `brew_fit.json` (ungated; exp18 v3's held-out items) | - | `40f07001d080af30bbd6396c554f90e2b350108f7a0bfb7e7bae1a5fc1e250d0` | - |
| `bind_recall.json` | Generated for this repo: `scripts/exp09_make_items.py --per-city 6 --n-bound 400 --seed 0` (facts written in the script; three people and countries before a recalled (R) or bound (B) bridge question; ungated) | - | `bbb1cfa8e95b6a83ec1c6003fc3a05c5c1fba195cff6a5cb7e3ea968dce59029` | - |
| `bind_lookup.json` | Generated for this repo: `scripts/exp09_make_items.py --lookup 400 --seed 1` (exp09's family L: B's bindings, then a colour per country in the prompt, the second hop an in-context lookup; ungated) | - | `dec730702c8805ac96699f9b2553cc06a7fa5d0090132b62a96ab6d84936fed3` | - |
| `bind_lookup_v2.json` | Generated for this repo: `scripts/exp09_make_items.py --lookup 400 --seed 1 --lookup-version 2` (the same L items ending "The country where {person} lives has the colour": the first file's ending is continued as a sentence, 1 of 400 answered) | - | `0883e3e5aa3dcecb41295a1324d6e366ba1bb766d6bd97b5b378a97cf4beae45` | - |
| `recall_lookup.json` | Generated for this repo: `scripts/exp09_make_items.py --recall-lookup 12 --seed 2` (exp09's family RL: R's recalled bridge, then a colour per country in the prompt, "The country where {city} is located has the colour"; ungated) | - | `d6905b4445032dab8ca3a2e8fff74588750175e004af1c31b3a235f44d15703f` | - |
| `lens_eval_multihop.json` | [anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens) `data/evaluations/lens-eval-multihop.json` | `581d398613e5602a5af361e1c34d3a92ea82ba8e` | `50b7e4c9255291c0ca2a8e94615be9f44531fa57bb1a844e4f9616056d987416` | Apache-2.0 |
| `wikitext103_test.json` | [Salesforce/wikitext](https://huggingface.co/datasets/Salesforce/wikitext) `wikitext-103-raw-v1/test-00000-of-00001.parquet` (sha256 `5f1bea067869d04849c0f975a2b29c4ff47d867f484f5010ea5e861eab246d91`), its `text` column in order, converted to JSON (see the file's `meta`) | `b08601e04326c79dfdd32d625aee71d232d685c3` | `a6b5b17a576932fbb570a96b0f5b6a65ced408690a2dce749a8c56f980bbcc0f` | CC BY-SA 3.0 |
| `entity_prompts.json` | Written for this repo by the coding agent (Claude, in a Cursor session); see the file's `meta` block | - | - | - |
| `suite_v1/*.json` (BL, BR, RL, RR, NAMES, CODE) | Generated for this repo: `scripts/suite_v1.py make` (seed 101; facts and cues written in the script, checked by the model's competence on each step alone) | - | see `results/suite_v1/competence_v1/manifest.json` | - |
| `suite_v1/BLR.json`, `suite_v1/BRL.json` | Generated for this repo: `scripts/suite_v1.py make --set tiebreak` (seed 102) | - | see `results/suite_v1/competence_tiebreak_v1/manifest.json` | - |
| `suite_v1_dev/*.json` | Generated for this repo: `scripts/suite_v1.py make --set dev` (seeds 90010-90013); difficulty pilot, dev only | - | see `results/suite_v1/competence_dev_v1/manifest.json` | - |
| `suite_v1/B1_annotations.json` | Derived: `scripts/suite_v1_b1_annotations.py` over `probe_swap.json` | - | - | - |
| `entity_prompts_topup.json`, `entity_prompts_more/part*.json` | Written for this repo (rounds 2 and 3, coding agents in Cursor sessions); see each file's `meta` block | - | - | - |

`probe_swap.json` is the 90 two-hop prompts of the probe-swap experiment in Gurnee et al. (2026),
[Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace/index.html).
It is copied unchanged.

`lens_eval_multihop.json` is the paper's lens-quality eval for two-hop prompts (93 items: `prompt`, `target`,
`intermediates`; readout at the token before `target`, pass@k over min-over-layers rank). Copied unchanged.

Models and lenses (J-lens, J++) are not stored here; they are downloaded at pinned revisions (see
`configs/models/*.yaml`). Data files are sha256-checked on load (`src/bridge_jspace/pins.py`).
