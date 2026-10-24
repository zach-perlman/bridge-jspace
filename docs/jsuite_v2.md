# jsuite_v2: the combined suite, version 2

One dataset for every module (Zach, 2026-10-24; prereg amendment 33). Built by `scripts/jsuite_v2.py` from the fact
tables in `scripts/jsuite_v2_tables.py`; audited by `scripts/audit_jsuite_v2.py`; scored by `scripts/jsuite2_score.py`.

## Sets

| set | split | framing | items |
|---|---|---|---|
| `data/tasks_v2/jsuite_v2_test_chat` | test | chat (instruct models) | 7,080 |
| `data/tasks_v2/jsuite_v2_dev_chat` | dev (band choice only) | chat | 6,460 |
| `data/tasks_v2/jsuite_v2_test_qa`, `..._dev_qa` | same items | raw text "Question/Answer" (base models) | same |

Dev and test share no fact bridge. Use dev only to choose a band; report test.

## Modules (field `module`)

- **facts** (two-hop fact chains; test 5,370 items, 171 bridges; dev 5,130, 163 bridges). 8 relations (field
  `relation`): countries -> continent, languages (country -> language), people -> nationality, cities -> country,
  companies -> country, landmarks -> country, dishes -> country, animals -> class. Words `start + final`:
  - start: `P` the bridge is read from the passage (a fictional person's binding), `M` recalled from a description in
    the question, `T` tracked (where one of two objects moving through a story went last)
  - final: `P` a new fictional fact stated in the passage (the answer is read), `K` the true fact stated, `M` recall
    (the answer is absent; other entities carry fictional values from the answer vocabulary, possible lures), `A` as M
    with the true answer present once on another entity, `N` recall with no answer-vocabulary word anywhere
  - the five finals of a scene share the passage except their final-hop sentences, and name the bridge equally often
  - test bridges are split into halves `half` = A / B (disjoint facts: an independent replication inside one run)
  - `eponymous` marks language items whose answer is readable off the country's name (France -> French)
- **threehop** (natural3's three-step chains, words `PPP` ... `MMM`; per-item eligibility)
- **numbers** (numbers as intermediates, jsuite_numbers' design; words prefixed `n`: `nPR`, `nPL`, `nPM`, ... ; run
  with `--dict-digits`; per-item eligibility)

## Running it

```bash
# competence (one run per model, split and framing)
uv run python scripts/natural_v1.py competence --set jsuite_v2_test_chat --name PREFIXjsuite_v2_test_chat_competence_cand2_v1 \
  --read cand2 --hop1 gen --why "..."
# the facts knock-out (scene eligibility over the 15 facts words)
uv run python scripts/ablate_v2.py --name PREFIXjsuite_v2_test_chat_ko_cand2_v1 --why "..." --plan bands --bands LO-HI \
  --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks jsuite_v2_test_chat \
  --tasks-competence PREFIXjsuite_v2_test_chat_competence_cand2_v1 \
  --tasks-words PP PK PM PA PN MP MK MM MA MN TP TK TM TA TN --tasks-level all --n 1000 --kinds clean --batch 32 --read cand2
# scoring: M - K (primary), M - P, M - N (lure capture), A - M, per start, half and relation
uv run python scripts/jsuite2_score.py PREFIXjsuite_v2_test_chat_ko_cand2_v1 --set jsuite_v2_test_chat --by-relation
```

Knock-out rows record `top_id` (the top token) and `pick2` (the candidate read's pick) for lure analysis.

## Known caveats

- Facts were written from knowledge (an agent's, checked by script for leaks and first-token collisions), not verified
  by a model: competence screens out what a model does not know.
- Some descriptors hint (Table Mountain names Cape Town); countries -> continent has 5 answers; countries needing "the"
  (US, UK) are absent; English, templated sentences with real WikiText filler.
- The three-hop module's dev and test share 44 chain entities (band choice uses facts only).

## First result (9B, L12-16, test): M - K +43 [37, 49], logit-lens +1, halves A / B +42 / +44, positive in 8 of 8
relations (7 with intervals above 0); M - N +6 (lures matter only for dishes).
