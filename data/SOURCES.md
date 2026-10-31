# Data sources

Provenance, revisions, checksums and licences. What each dataset is and how much of it there is: [README.md](README.md).

| File | Source | Revision | sha256 | License |
|---|---|---|---|---|
| `probe_swap.json` | [anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens) `data/experiments/probe-swap.json` | `581d398613e5602a5af361e1c34d3a92ea82ba8e` | `a0edd27ca23f7b4d0fbe90448c2ddcc7457a3d812121bf024ed12a032ff86796` | Apache-2.0 |
| `brew_intermediates.json` | [camilablank/workspace-bench](https://github.com/camilablank/workspace-bench) `evals/brew_intermediates/items.json` | `92d763e722377f5bfae045e829a308ab5919a820` | `183be95d4182c373674786b7610820520e56434fb0c15a75a62dad854bed9d83` | MIT |
| `brew_fresh.json` | Generated for this repo: `scripts/exp03_make_items.py --n 200 --seed 1`, in the format of `brew_intermediates.json` (ungated; exp03 keeps the greedy-correct ones) | - | `1e20ed25b3727842acba0806b346d91d991db1fa31f42f514e537fb3ab000d3c` | - |
| `brew_fit.json` | Generated for this repo: `scripts/exp03_make_items.py --name brew_fit --prefix brewfit --n 1000 --seed 2`, in the format of `brew_intermediates.json`, no prompt of the bank or of `brew_fresh.json` (ungated; exp07 fits its code on the greedy-correct ones) | - | `b9ab169a50bf576d71c074b31516f283e3163366d8ce2aea0907addbdf0e2659` | - |
| `brew_test.json` | Generated for this repo: `scripts/exp03_make_items.py --name brew_test --prefix brewtest --n 600 --seed 3`, in the format of `brew_intermediates.json`, no prompt of the bank, `brew_fresh.json` or `brew_fit.json` (ungated; exp18 v3's held-out items) | - | `40f07001d080af30bbd6396c554f90e2b350108f7a0bfb7e7bae1a5fc1e250d0` | - |
| `wsb_wrong_bridge.json` | [camilablank/workspace-bench](https://github.com/camilablank/workspace-bench) `evals/wrong_bridge/items.json` | `ba33098131318bdc19ddfdcf60078caae5027409` | `1563f12995190f55a174de5b1099645dae9123fdcb33a7633505bc84ca419d0b` | MIT |
| `bind_recall.json` | Generated for this repo: `scripts/exp09_make_items.py --per-city 6 --n-bound 400 --seed 0` (facts written in the script; three people and countries before a recalled (R) or bound (B) bridge question; ungated) | - | `bbb1cfa8e95b6a83ec1c6003fc3a05c5c1fba195cff6a5cb7e3ea968dce59029` | - |
| `bind_lookup.json` | Generated for this repo: `scripts/exp09_make_items.py --lookup 400 --seed 1` (exp09's family L: B's bindings, then a colour per country in the prompt, the second hop an in-context lookup; ungated) | - | `dec730702c8805ac96699f9b2553cc06a7fa5d0090132b62a96ab6d84936fed3` | - |
| `bind_lookup_v2.json` | Generated for this repo: `scripts/exp09_make_items.py --lookup 400 --seed 1 --lookup-version 2` (the same L items ending "The country where {person} lives has the colour": the first file's ending is continued as a sentence, 1 of 400 answered) | - | `0883e3e5aa3dcecb41295a1324d6e366ba1bb766d6bd97b5b378a97cf4beae45` | - |
| `recall_lookup.json` | Generated for this repo: `scripts/exp09_make_items.py --recall-lookup 12 --seed 2` (exp09's family RL: R's recalled bridge, then a colour per country in the prompt, "The country where {city} is located has the colour"; ungated) | - | `d6905b4445032dab8ca3a2e8fff74588750175e004af1c31b3a235f44d15703f` | - |
| `lens_eval_multihop.json` | [anthropics/jacobian-lens](https://github.com/anthropics/jacobian-lens) `data/evaluations/lens-eval-multihop.json` | `581d398613e5602a5af361e1c34d3a92ea82ba8e` | `50b7e4c9255291c0ca2a8e94615be9f44531fa57bb1a844e4f9616056d987416` | Apache-2.0 |
| `lens_eval_multilingual.json` | [safety-research/jpp_lens](https://github.com/safety-research/jpp_lens) `data/jlens/evaluations/` (Apache-2.0) | `93f02cd` | `fa70b9bd89416a6d8d985a80dc628b109ae6fd3b25b9275c0fc5065d7ff4a0ef` |
| `lens_eval_order_ops.json` | [safety-research/jpp_lens](https://github.com/safety-research/jpp_lens) `data/jlens/evaluations/` (Apache-2.0) | `93f02cd` | `b203206d16ff628152cc86f3838604e06cb54776f3e14fa1c34f150db8bc7560` |
| `lens_eval_poetry.json` | [safety-research/jpp_lens](https://github.com/safety-research/jpp_lens) `data/jlens/evaluations/lens-eval-poetry.json`, copied unchanged (98 rhyming couplets; prereg amendment 72 note 55) | `93f02cd` | `6aeb3415c5a5c3f3827c9efe63f006de02f5ef39a816bbac68e15e733aba60cc` | Apache-2.0 |
| `wikitext103_test.json` | [Salesforce/wikitext](https://huggingface.co/datasets/Salesforce/wikitext) `wikitext-103-raw-v1/test-00000-of-00001.parquet` (sha256 `5f1bea067869d04849c0f975a2b29c4ff47d867f484f5010ea5e861eab246d91`), its `text` column in order, converted to JSON (see the file's `meta`) | `b08601e04326c79dfdd32d625aee71d232d685c3` | `a6b5b17a576932fbb570a96b0f5b6a65ced408690a2dce749a8c56f980bbcc0f` | CC BY-SA 3.0 |
| `entity_prompts.json` | Written for this repo by the coding agent (Claude, in a Cursor session); see the file's `meta` block | - | - | - |
| `suite_v1/*.json` (BL, BR, RL, RR, NAMES, CODE) | Generated for this repo: `scripts/suite_v1.py make` (seed 101; facts and cues written in the script, checked by the model's competence on each step alone) | - | see `results/suite_v1/competence_v1/manifest.json` | - |
| `suite_v1/BLR.json`, `suite_v1/BRL.json` | Generated for this repo: `scripts/suite_v1.py make --set tiebreak` (seed 102) | - | see `results/suite_v1/competence_tiebreak_v1/manifest.json` | - |
| `suite_v1_b/*.json` | Generated for this repo: `scripts/suite_v1.py make --set wording_b` (seeds 201, 202); wording B of every family | - | see `results/suite_v1/competence_b_v1/manifest.json` | - |
| `suite_v1_dev/*.json` | Generated for this repo: `scripts/suite_v1.py make --set dev` (seeds 90010-90013); difficulty pilot, dev only | - | see `results/suite_v1/competence_dev_v1/manifest.json` | - |
| `suite_v1/B1_annotations.json` | Derived: `scripts/suite_v1_b1_annotations.py` over `probe_swap.json` | - | - | - |
| `entity_prompts_topup.json`, `entity_prompts_more/part*.json` | Written for this repo (rounds 2 and 3, coding agents in Cursor sessions); see each file's `meta` block | - | - | - |
| `natural_read_v1/items.json` | Derived: `scripts/natural_read.py make` (seed 0) from SQuAD v1.1 dev, [rajpurkar/SQuAD-explorer](https://github.com/rajpurkar/SQuAD-explorer) `dataset/dev-v1.1.json` (raw sha256 `95aa6a52d5d6a735563366753ca50492a658031da74f301ac5238b03966972c9`; not committed: `cache/natural_read/squad/dev-v1.1.json`, URL in `pins.SQUAD_DEV_URL`); one question per paragraph, 718 items (see the file's `meta`) | `240e165ab706d95bd4323653bb92421f446208cf` | `60b8527dc63c2fff3217d40ece1a7f8405a46aa3946f8d7f36f2d475eab21cc9` | CC BY-SA 4.0 |

`probe_swap.json` is the 90 two-hop prompts of the probe-swap experiment in Gurnee et al. (2026),
[Verbalizable Representations Form a Global Workspace in Language Models](https://transformer-circuits.pub/2026/workspace/index.html).
It is copied unchanged.

`lens_eval_multihop.json` is the paper's lens-quality eval for two-hop prompts (93 items: `prompt`, `target`,
`intermediates`; readout at the token before `target`, pass@k over min-over-layers rank). Copied unchanged.

`natural_read_v1/items.json` holds Wikipedia paragraphs, questions and answers from SQuAD v1.1 (Rajpurkar et al. 2016, [SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250)), dev set, distributed under CC BY-SA 4.0 (the site's download note; the site repository's code is MIT). The derived file is under the same licence. The raw file is the one at the pinned commit above; the site's own copy (https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json) had the same sha256 on 2026-10-23. `tests/test_pins.py` rebuilds the items from the raw file when it is cached.

Models and lenses (J-lens, J++) are not stored here; they are downloaded at pinned revisions (see
`configs/models/*.yaml`). Data files are sha256-checked on load (`src/bridge_jspace/pins.py`).
