# D3 v4 without the chat template: is the statement-slot answer still there in plain text?

Run `d3v4_swap_raw_27b_v2` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements, 3 wordings per topic.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP d3v4_swap_raw_27b_v2 @ unknown | model Qwen3.6-27B (raw format) | n per family = memory → prompt 321 items / 80 entities / 25 wordings (5 statements); named → prompt 321 items / 80 entities / 25 wordings (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 16% [13, 21]   Baseline: none = 41% [35, 46], identity = 6% [3, 9], value = 18% [14, 22]   Control: 'same' changed = 1% [0, 3]; random push of the same size changed (max over transit layers) = 2% [0, 4]; another domain's prompt changed = 18% [15, 23]
Figures: results/pointer_swap/d3v4_swap_raw_27b_v2/analysis-20261021-191154-figures/by_layer_e5f0.png, results/pointer_swap/d3v4_swap_raw_27b_v2/analysis-20261021-191154-figures/slots_final_e5f0.png, results/pointer_swap/d3v4_swap_raw_27b_v2/analysis-20261021-191154-figures/slots_last_e5f0.png, results/pointer_swap/d3v4_swap_raw_27b_v2/analysis-20261021-191154-figures/windows_e5f0.png, results/pointer_swap/d3v4_swap_raw_27b_v2/analysis-20261021-191154-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v4_swap_raw_27b_v2/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=321); position should be 52, identity 18, value 57, none 131
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 2% [0, 4] (max over transit layers); digits of the base context that no hypothesis predicts win 1% [0, 3]; among alt prompt reads won by a predicted digit, 372/15791 have the runner-up prediction within p 0.1; hook checks self no-op 642/642, layer-0 reproduction 641/642.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "mixed", "body": "damage", "countries": "mixed"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **mixed** (answer org kept 41% [35, 46], answer of bridge alt's statement 6% [3, 9], answer at the same statement slot 16% [13, 21], the alt prompt's own answer 18% [14, 22])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 52, in cuts ['domain:body'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | - | - | - |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 98%, answer of bridge alt's statement 0%) | no effect (answer org kept 91%, answer of bridge alt's statement 1%) | mixed (answer org kept 41%, the alt prompt's own answer 18%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 97%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 44%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words | e5f0 | - | - | - |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 72%, answer at the same statement slot 11%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 61%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 321 | 321 | mixed | yes | answer org kept 41% [35, 46], answer of bridge alt's statement 6% [3, 9], answer at the same statement slot 16% [13, 21], the alt prompt's own answer 18% [14, 22] |
| domain:animals | e5f0 | 150 | 150 | mixed | yes | answer org kept 27% [21, 35], answer of bridge alt's statement 11% [7, 17], answer at the same statement slot 21% [15, 28], the alt prompt's own answer 26% [18, 34] |
| domain:body | e5f0 | 21 | 21 | damage (2 same-entity control changes) | NO (n < 35) | answer org kept 5% [0, 23], answer of bridge alt's statement 0% [0, 15], answer at the same statement slot 10% [0, 29], the alt prompt's own answer 10% [0, 29] |
| domain:countries | e5f0 | 150 | 150 | mixed | yes | answer org kept 59% [51, 67], answer of bridge alt's statement 1% [0, 4], answer at the same statement slot 13% [8, 19], the alt prompt's own answer 11% [7, 17] |
| slot:first | e5f0 | 57 | 57 | mixed | yes | answer org kept 35% [24, 48], answer of bridge alt's statement 11% [4, 21], answer at the same statement slot 7% [2, 17], the alt prompt's own answer 26% [15, 39] |
| slot:middle | e5f0 | 193 | 193 | mixed | yes | answer org kept 43% [36, 50], answer of bridge alt's statement 6% [3, 10], answer at the same statement slot 16% [11, 21], the alt prompt's own answer 17% [12, 23] |
| slot:last | e5f0 | 71 | 71 | mixed | yes | answer org kept 39% [29, 51], answer of bridge alt's statement 1% [0, 8], answer at the same statement slot 25% [17, 37], the alt prompt's own answer 13% [6, 22] |

## Checks

`{"self_noop": {"n": 642, "same_top": 642, "max_abs_dlogit_max": 0.3438}, "layer0_all_reproduces_source": {"n": 642, "same_top": 641, "max_abs_dlogit_max": 0.6875}, "unedited_base_answer_read": {"n": 642, "base_answer": 642}}`; near ties: `{"n": 15791, "within_gap": 372, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | everything after the question | 46 | 55% [49, 61] | 45% [39, 51] | 15% [11, 19] | 26% [22, 32] | 0% [0, 1] |
| memory → prompt | e5f0 | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 95% [92, 98] |
| named → prompt | e5f0 | everything after the question | 50 | 29% [24, 34] | 71% [66, 76] | 5% [3, 8] | 16% [12, 21] | 0% [0, 1] |
| named → prompt | e5f0 | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 99% [97, 100] |

## Agent priors in the job spec (jobs/d3/d3v4_swap_raw_27b_v2.yaml `hypotheses`) vs results

- H-format-free: raw, memory -> prompt, last two tokens, pooled: rule verdict "same statement slot" at layer 50 (or 48 or 52); slot 30-55%, word <= 25%; per topic slot > word by point estimate in all three
- H-template: raw, memory -> prompt, last two tokens, at every one of layers 48, 50 and 52: slot below 15% or within 10 points of the word (point estimates)
- prior: Agent prior: H-format-free 0.6, H-template 0.4 (coordinator's priors; the last two tokens, ":" and the space, exist in both formats, but in chat they follow the template, in raw the question directly).

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 16% [13, 21], last two tokens 23% [18, 28] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 11% [8, 15] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 6% [3, 9] / 8% [6, 12] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 18% [14, 22] / 44% [38, 49] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 52
- H-none: memory → prompt, answer changed after the question 59% [54, 65] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e5f0-0010` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 46 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
Drawer 8 holds the Germany file. Drawer 7 holds the China file. Drawer 5 holds the Belgium file. Drawer 1 holds the Syria file. Drawer 2 holds the Indonesia file.
Which drawer holds the file on the country whose capital is Damascus? Answer with a single word and nothing else.
Answer: 
```

Alt prompt:

```
Drawer 3 holds the Indonesia file. Drawer 2 holds the Syria file. Drawer 5 holds the Belgium file. Drawer 1 holds the Germany file. Drawer 7 holds the China file.
Which drawer holds the file on the country whose capital is Jakarta? Answer with a single word and nothing else.
Answer: 
```

Answers: answer org 1; after the patch 8. Predicted: answer org kept 1 (p 0.225); answer of bridge alt's statement 2 (p 0.001); answer at the same statement slot 8 (p 0.540); the alt prompt's own answer 3 (p 0.000).

