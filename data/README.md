# Data catalog

What every experiment reads, where it comes from, and how much of it there is. Counts below are recomputed by
`make data-report` (`scripts/data_report.py`, checked by `tests/test_data_report.py`); provenance, licences and
sha256 pins are in [SOURCES.md](SOURCES.md) and `src/bridge_jspace/pins.py`.

## Part B's prompt suite v1 (from 2026-10-19; the headline data)

`data/suite_v1/` (generator and checks: `scripts/suite_v1.py`; page with examples: `figures/suite_v1/index.html`).
Chat format (one user turn, thinking off, "Answer:" prefilled). Every item has a clean prompt, a counterfactual C that
changes only the bridge, an off-path control O, and each step alone; C and O line up with the clean prompt token for
token (2,400 of 2,400). No place relations and no answer tied one-to-one to its bridge (the France -> Paris problem).

| Family | Bridge from → used by → answer from | Answer | Items | Clean right | Eligible* | Bridges |
|---|---|---|---|---|---|---|
| BL | bound in the prompt → a lookup in the prompt → prompt | locker (odd digit) | 400 | 400 | 400 | 16 animals |
| BR | bound in the prompt → a recalled fact → memory | legs (2/4/6/8) | 400 | 400 | 400 | 16 animals |
| RL | recalled from a cue → a lookup in the prompt → prompt | locker (odd digit) | 400 | 398 | 398 | 16 animals |
| RR | recalled from a cue → a recalled fact → memory | legs (2/4/6/8) | 400 | 400 | 398 | 16 animals |
| NAMES | bound → a lookup → prompt ("Who is the sister of Alice's partner?") | a name | 400 | 400 | 400 | 30 names |
| CODE | bound in code → a lookup in code → code | digit 1-9 | 400 | 400 | 399 | 23 words |
| BLR | bound → a lookup (the pet's friend) → a recalled fact → memory | legs (2/4/6/8) | 400 | 395 | 390 | 16 animals |
| BRL | bound → a recalled fact (legs) → a lookup by legs → prompt | locker (odd digit) | 400 | 359 | 324 | 16 animals |
| BREW | prompt → a lookup → a lookup → prompt (kept: `brew_test.json`, `brew_fresh.json`) | 12 colours | 800 | 87-88% | exp04's rule | 12 colours |

\* clean, C, O and both steps alone answered (results/suite_v1/competence_v1). BL/BR/RL/RR share one context per scene
(people's pets and the pets' lockers) and differ only in the question, so they are paired item by item. Lockers are odd
digits and legs even (the answers never collide); legs is many-to-one, so an answer cannot stand in for its bridge. The
recall cues each name one animal ("known for mooing"; bleating, stripes, mane and buzzing were dropped as ambiguous);
"squeaking" is answered "pig" on 2 items with a pig present, which the eligibility rule removes.

**Tie-breakers BLR and BRL** (`make --set tiebreak`, seed 102; results/suite_v1/competence_tiebreak_v1). In the 2x2,
what uses the bridge also decides where the answer comes from; BLR (used by a lookup, answer from memory) and BRL (used
by a recall, answer from the prompt) separate the two at equal depth. Built in pairs on one scene (same people, pets
and C). BRL is the one family the 27B gets wrong without any step being wrong alone (90% clean, every step 100%; the
misses are 4- and 6-legged pets answered with the 2-legs locker or with a leg count), so its eligible items are a
selected 81% and any BLR vs BRL comparison has to allow for that.

**Wording B** (`data/suite_v1_b/`, `make --set wording_b`, seeds 201 and 202): all eight families again in other
words, same vocabulary, structure and token alignment, so no result rests on one template: "Jack owns a cow. ... The
cow uses locker 5. ... Which locker does the animal that Jack owns use?"; "the animal famous for mooing"; "Alice is
married to Ben. ... Ben's sister is called Grace."; CODE with `key`/`lookup`/`values` and a `result` line; BLR's
"neighbour" for "friend"; BRL's "Locker 7 is for animals with 4 legs." (results/suite_v1/competence_b_v1).

**Difficulty pilot** (`data/suite_v1_dev/`, `make --set dev`, seeds 90010-90013; never a headline run's items): every
family at 3 or 5 entities per scene and 0 or 8 unrelated filler sentences, 100 items per cell
(results/suite_v1/competence_dev_v1 and qwen35_9b_competence_dev_v1).

**How many items:** every item for competence; patching runs sample at least 150 eligible items per family (a 95%
interval of at most ±8 points on a rate; ±4 on a paired part-vs-rest difference; ±11 between two families).

**B1 (the paper's 90) is kept unchanged as a reference**, annotated in `data/suite_v1/B1_annotations.json`
(`scripts/suite_v1_b1_annotations.py`): 28 places, 8 people and 25 other items have an answer tied one-to-one to the
bridge; 29 are clean (non-place, answer shared by many bridges; 25 eligible in the verified run).

**Retired from headline runs** (files kept, results stand as earlier evidence): `bind_recall.json` R and B
(country -> capital), `bind_lookup*.json` and `recall_lookup.json` (countries; cities recalled to countries),
`use_source.json` (capitals and landmark cities; RM not reliable), `arith.json` (the copy carries too little).

## Datasets

| Dataset | File | Origin | Size | Used by |
|---|---|---|---|---|
| Probe-swap two-hop items | `probe_swap.json` | paper, copied unchanged | 90 items, 36 categories | exp02 (B), exp11, exp12, exp14 |
| Part B labels for those items | `../results/exp02_swaps/main_v4_jlens/labels.csv` (and `main_v4_jpp`) | derived: part B's exp02 v4 runs | 90 rows | exp11, exp12, exp14 (pinned by sha256 in their configs) |
| Lens-eval multihop | `lens_eval_multihop.json` | paper, copied unchanged | 93 items | exp10 |
| Entity prompts | `entity_prompts.json`, `entity_prompts_topup.json`, `entity_prompts_more/part*.json` | generated for this repo (coding agents, 3 rounds) | 97 entities, 2673 prompts | exp01 (B): bridge probes |

### Probe-swap two-hop items
One two-hop question per item: `prompt` (e.g. "Fact: The language spoken in the country where the Amazon River ends
is "), the bridge `intermediate` (Brazil) and `answer` (Portuguese), and a same-category `swap_to` (Mexico) with its
`swap_answer` (Spanish), plus a `category`.
- **Why this set:** it is the paper's probe-swap set, so part B's swap rates can be set against Claude's (61% / 28% /
  6%); the uneven mix of questions below comes with it.
- **Composition:** 29 items in category `multihop`; the other 61 spread over 35 categories, 23 of them with a single
  item. 70 unique bridges (Canada appears 4 times; oxygen, iron, China 3 times). 29 prompts end in a space. By bridge
  type (part B's split of the 77 eligible items): 26 countries or places, 7 people, 44 other (elements, organs,
  animals, dates); swap effects concentrate in the places (exp02, exp14).
- **Part B labels** (v4, `exp02_swaps/main_v4_jlens/labels.csv`; prompts with the trailing space stripped):
  `status` = eligible (Qwen3.6-27B's greedy continuation contains the answer) 77 / clean_wrong 13; for eligible items
  `label` = J-mediated 25 / neither 49 / both 2 / non-J 1 (from which swaps flip the answer; `main_v4_jpp` labels the
  same items by the J++ swaps). 22 of the 77 eligible items are `multihop`. The earlier labels
  (`exp02_swaps/main/labels.csv`, prompts as published, first-word correctness) had 67 eligible.
- **What it supports:** headline rates over the 77 eligible items (95% CIs about +-0.1); comparisons between large
  groups. **Not:** per-category claims (most categories have one item), or non-J vs J-mediated (1 non-J item).
  Items are not fully independent (shared categories and bridges): on the earlier 67 items, exp11's headline barely
  changed under a bootstrap over categories or bridges instead of items (J-lens 0.59: [0.49, 0.68] vs [0.49, 0.71]).

### Lens-eval multihop
The paper's lens-quality set: `prompt`, `target` (the answer, which only fixes the readout position) and
`intermediates` (1 per item for 84 items, 2 for 8, 3 for 1; several intermediates are forms of one bridge, '6' and
'six'). 83 prompts end in a space. One prompt names its bridge ("the time of day ..." -> "day"); a substring search
also flags four single-letter bridges (H, O, C, N) that only occur inside other words. By kind, the bridges are 63
words, 26 numbers ('6', 'four', 'third') and 4 letters (chemical symbols); among the 84 single-token items, 63 / 17 /
4 (exp10 reports pass@k per kind). **30 prompts are identical to probe-swap prompts**, so exp10 and exp11 are not
independent samples.

### Entity prompts
Prompts that imply one entity without naming it, ending before a one-word answer (e.g. "Fact: The dance at the heart
of the carnival in Rio de Janeiro is the" -> samba, for Brazil). Part B averages Qwen's residuals over the prompts it
answers correctly to build each entity's probe. Rules (each file's `meta` block): the entity, its swap partners and
the test answers never appear; no 4-gram overlap with the 90 test prompts.
- Round 1 `entity_prompts.json` (97 entities, 672 prompts), round 2 `entity_prompts_topup.json` (3 entities, 12),
  round 3 `entity_prompts_more/` (97 entities, 1989). 24-32 prompts per entity.
- exp01 v3 kept 2260 of 2673 (Qwen answered as expected): 12-30 per entity, median 24.

### Depth-track scenes (Dan, 21 Oct; generated, seeded, each with a `check` and a `verify` stage)
Five statements give entities a digit ("The pig's locker is 9."); a question asks one of them by a recalled cue
(memory → prompt), by name (named → prompt), or a recalled fact (memory → memory); each item carries alt prompts
(statements reordered, another entity asked) for patching. Used by D2 / D3 / D3b (see the root README).

| Set | Generator | What differs | Size |
|---|---|---|---|
| `pointer_v1/` | `scripts/pointer_v1.py` | 5 statements; animals (16), elements (6), planets, months | 400 scenes per domain × family (main), plus fit / dev |
| `pointer_v2/` | `scripts/pointer_v2.py` | one filler sentence placed differently in org and alt (order vs token position) | 180 per topic (5 statements), 120 (3) |
| `pointer_v3/` | `scripts/pointer_v3.py` | alt with one statement more or fewer (from the start vs from the end) | 120 per topic × alt type |
| `code_pointer_v1/` | `scripts/code_pointer_v1.py` | Python dict lookups: named key, list position, 2-3 variable chains, recalled key | 400 per domain × family |
| `alias_pointer_v1/` | `scripts/alias_pointer_v1.py` | statements in French/Spanish/German or by chemical symbol | 400 per domain × form × family |
| `pointer_v4/` | `scripts/pointer_v4.py` | many entities and 3 wordings: countries (36), animals (34), body parts (16) kept by the 27B entity check `d3v4_entity_probe_27b` (sports failed: 14 < 16); a held-out third of each topic's entities and wording 2 never in the fit set (`split.json`); at most 12 scenes per asked entity | main 300 / 300 / 180 scenes per family, fit 200 / 200 / 120 |

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
