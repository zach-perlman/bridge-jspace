# Data catalog

What every experiment reads, where it comes from, and how much of it there is. Counts below are recomputed by
`make data-report` (`scripts/data_report.py`, checked by `tests/test_data_report.py`); provenance, licences and
sha256 pins are in [SOURCES.md](SOURCES.md) and `src/bridge_jspace/pins.py`.

## Datasets

| Dataset | File | Origin | Size | Used by |
|---|---|---|---|---|
| Probe-swap two-hop items | `probe_swap.json` | paper, copied unchanged | 90 items, 36 categories | exp02 (B), exp11, exp12 |
| Part B labels for those items | `../results/exp02_swaps/main/labels.csv` | derived: part B's exp02 main run | 90 rows | exp11, exp12 (pinned by sha256 in their configs) |
| Lens-eval multihop | `lens_eval_multihop.json` | paper, copied unchanged | 93 items | exp10 |
| Entity prompts | `entity_prompts.json`, `entity_prompts_topup.json`, `entity_prompts_more/part*.json` | generated for this repo (coding agents, 3 rounds) | 97 entities, 2673 prompts | exp01 (B): bridge probes |

### Probe-swap two-hop items
One two-hop question per item: `prompt` (e.g. "Fact: The language spoken in the country where the Amazon River ends
is "), the bridge `intermediate` (Brazil) and `answer` (Portuguese), and a same-category `swap_to` (Mexico) with its
`swap_answer` (Spanish), plus a `category`.
- **Composition:** 29 items in category `multihop`; the other 61 spread over 35 categories, 23 of them with a single
  item. 70 unique bridges (Canada appears 4 times; oxygen, iron, China 3 times). 29 prompts end in a space.
- **Part B labels** (`labels.csv`): `status` = eligible (Qwen3.6-27B's top word is the answer, formatting tokens
  removed) 67 / clean_wrong 16 / multi_token_answer 7; for eligible items `label` = J-mediated 25 / neither 40 /
  non-J 1 / both 1 (from which swaps flip the answer). 21 of the 67 eligible items are `multihop`.
- **What it supports:** headline rates over the 67 eligible items (95% CIs about +-0.1); comparisons between large
  groups. **Not:** per-category claims (most categories have one item), or non-J vs J-mediated (1 non-J item).
  Items are not fully independent (shared categories and bridges): exp11's headline barely changes under a bootstrap
  over categories or bridges instead of items (J-lens 0.59: [0.49, 0.68] vs [0.49, 0.71]).

### Lens-eval multihop
The paper's lens-quality set: `prompt`, `target` (the answer, which only fixes the readout position) and
`intermediates` (1 per item for 84 items, 2 for 8, 3 for 1). 83 prompts end in a space; 5 contain their intermediate
word. **30 prompts are identical to probe-swap prompts**, so exp10 and exp11 are not independent samples.

### Entity prompts
Prompts that imply one entity without naming it, ending before a one-word answer (e.g. "Fact: The dance at the heart
of the carnival in Rio de Janeiro is the" -> samba, for Brazil). Part B averages Qwen's residuals over the prompts it
answers correctly to build each entity's probe. Rules (each file's `meta` block): the entity, its swap partners and
the test answers never appear; no 4-gram overlap with the 90 test prompts.
- Round 1 `entity_prompts.json` (97 entities, 672 prompts), round 2 `entity_prompts_topup.json` (3 entities, 12),
  round 3 `entity_prompts_more/` (97 entities, 1989). 24-32 prompts per entity.
- exp01 v3 kept 2260 of 2673 (Qwen answered as expected): 12-30 per entity, median 24.

## What the lenses were fitted on

Not on our data: a lens is the average Jacobian of the final residual with respect to a layer's residual over
generic text, downloaded pre-fitted from `neuronpedia/jacobian-lens` (revision pinned in `configs/models/*.yaml`).
Our prompts were never seen by the fit, so a lens reading the bridge is not fitted to the task.

| Model | Lens | Fitting text | Size | Fitted by | Source of these facts |
|---|---|---|---|---|---|
| Qwen3.6-27B | J-lens | WikiText (folder `Salesforce-wikitext`) | 1000 prompts | mntss (Anthropic) | `n_prompts` in the file; CREDIT.md |
| Qwen3.6-27B | J++ | WikiText | 64 prompts x 128 tokens, first 16 positions skipped | Ayonrinde & Lindsey | `provenance` in the file; config.yaml |
| Qwen3.5-4B | J-lens (`_n1000`) | WikiText (folder name) | not read (file name says n1000) | mntss | file name; CREDIT.md |
| Qwen3.5-0.8B | J-lens / J++ | WikiText | 233 / 96 prompts | Neuronpedia | `n_prompts` at load |

Caveats: the fitting text is encyclopedic, close to our factual prompts; lenses may read worse on other kinds of
text. J++ for 27B was fitted on far fewer texts than the J-lens and still reads the bridge better (exp10, exp11).

## Not in the repo
Model weights and lens files (HF cache, pinned revisions), run caches (`cache/`), logs (`log/`).
