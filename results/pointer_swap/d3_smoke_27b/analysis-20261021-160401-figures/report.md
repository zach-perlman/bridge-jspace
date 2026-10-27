# D3 test run: the patching code works on the 27B

Run `d3_smoke_27b` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements.

**NOT A HEADLINE RUN (superseded or smoke)**: smoke run: 1 prompt per topic, competence check skipped; a code-path and timing check, not a result. Shown for completeness.

```
EXP d3_smoke_27b @ 2d90ce4 | model Qwen3.6-27B | n per family = memory → prompt 4 (5 statements); named → prompt 4 (5 statements); memory → memory 4 (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 0% [0, 49]   Baseline: none = 100% [51, 100], identity = 0% [0, 49], value = 0% [0, 49]   Control: 'same' changed = 0% [0, 49]; random push of the same size changed (max over transit layers) = 0% [0, 49]; another domain's prompt changed = 25% [5, 70]
Figures: results/pointer_swap/d3_smoke_27b/analysis-20261021-160401-figures/by_layer_e5f0.png, results/pointer_swap/d3_smoke_27b/analysis-20261021-160401-figures/slots_final_e5f0.png, results/pointer_swap/d3_smoke_27b/analysis-20261021-160401-figures/slots_last_e5f0.png, results/pointer_swap/d3_smoke_27b/analysis-20261021-160401-figures/windows_e5f0.png, results/pointer_swap/d3_smoke_27b/analysis-20261021-160401-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_smoke_27b/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=4); position should be 0, identity 0, value 0, none 4
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 49] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 49]; among alt prompt reads won by a predicted digit, 9/485 have the runner-up prediction within p 0.1; hook checks self no-op 12/12, layer-0 reproduction 12/12.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "damage", "elements": "damage", "months": "damage", "planets": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **damage** (answer org kept 100% [51, 100], answer of bridge alt's statement 0% [0, 49], answer at the same statement slot 0% [0, 49], the alt prompt's own answer 0% [0, 49])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 924, in cuts ['all', 'domain:animals', 'domain:elements', 'domain:months', 'domain:planets', 'slot:first', 'slot:middle'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | last two tokens before the answer | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 25%, answer of bridge alt's statement 25%) |
| memory → prompt | question words + everything after | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 25%, answer at the same statement slot 50%) |
| named → prompt | question words | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 50%) | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 75%, answer at the same statement slot 25%) |
| named → prompt | everything after the question | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | question words + everything after | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 50%) | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 0%, the alt prompt's own answer 75%) |
| memory → memory | question words | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 75%, answer of bridge alt's statement 0%) |
| memory → memory | everything after the question | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 75%, answer of bridge alt's statement 0%) | damage (answer org kept 50%, answer of bridge alt's statement 25%) |
| memory → memory | last two tokens before the answer | e5f0 | damage (answer org kept 75%, answer of bridge alt's statement 0%) | damage (answer org kept 50%, answer of bridge alt's statement 25%) | damage (answer org kept 25%, answer of bridge alt's statement 50%) |
| memory → memory | question words + everything after | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 0%, answer of bridge alt's statement 75%) | damage (answer org kept 0%, answer of bridge alt's statement 75%) |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 4 | 4 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [51, 100], answer of bridge alt's statement 0% [0, 49], answer at the same statement slot 0% [0, 49], the alt prompt's own answer 0% [0, 49] |
| domain:animals | e5f0 | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| domain:elements | e5f0 | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| domain:months | e5f0 | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| domain:planets | e5f0 | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| slot:first | e5f0 | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [34, 100], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 0% [0, 66] |
| slot:middle | e5f0 | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [34, 100], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 0% [0, 66] |

## Checks

`{"self_noop": {"n": 12, "same_top": 12, "max_abs_dlogit_max": 0.4688}, "layer0_all_reproduces_source": {"n": 12, "same_top": 12, "max_abs_dlogit_max": 0.332}, "unedited_base_answer_read": {"n": 12, "base_answer": 11}}`; near ties: `{"n": 485, "within_gap": 9, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | question words | 0 | 100% [51, 100] | 0% [0, 49] | 100% [51, 100] | 0% [0, 49] | 0% [0, 49] |
| memory → prompt | e5f0 | everything after the question | 0 | 0% [0, 49] | 100% [51, 100] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] |
| memory → prompt | e5f0 | last two tokens before the answer | 56 | 100% [51, 100] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 100% [51, 100] |
| memory → prompt | e5f0 | question words + everything after | 0 | 100% [51, 100] | 0% [0, 49] | 100% [51, 100] | 0% [0, 49] | 0% [0, 49] |
| named → prompt | e5f0 | question words | 0 | 100% [51, 100] | 0% [0, 49] | 100% [51, 100] | 0% [0, 49] | 0% [0, 49] |
| named → prompt | e5f0 | everything after the question | 56 | 100% [51, 100] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 100% [51, 100] |
| named → prompt | e5f0 | last two tokens before the answer | 56 | 100% [51, 100] | 0% [0, 49] | 0% [0, 49] | 0% [0, 49] | 100% [51, 100] |
| named → prompt | e5f0 | question words + everything after | 0 | 100% [51, 100] | 0% [0, 49] | 100% [51, 100] | 0% [0, 49] | 0% [0, 49] |
| memory → memory | e5f0 | question words | 0 | 100% [51, 100] | 0% [0, 49] | 75% [30, 95] | 0% [0, 49] | 0% [0, 49] |
| memory → memory | e5f0 | everything after the question | 48 | 50% [15, 85] | 50% [15, 85] | 25% [5, 70] | 0% [0, 49] | 0% [0, 49] |
| memory → memory | e5f0 | last two tokens before the answer | 56 | 100% [51, 100] | 0% [0, 49] | 75% [30, 95] | 0% [0, 49] | 0% [0, 49] |
| memory → memory | e5f0 | question words + everything after | 0 | 100% [51, 100] | 0% [0, 49] | 75% [30, 95] | 0% [0, 49] | 0% [0, 49] |

## Agent priors in the job spec (jobs/d3/d3_smoke_27b.yaml `hypotheses`) vs results

- H-ok: self_noop same top 12/12 (max |dlogit| <= 0.5, bf16 batching); layer0_all_reproduces_source 12/12; >= 15 edited reads/s
- H-broken: any self_noop or layer-0 mismatch: hook placement wrong; stop the queue

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [0, 49], last two tokens 25% [5, 70] (>= 50%: not met); memory → memory 0% [0, 49] / 0% [0, 49] (<= 10%: met); named → prompt after the question 0% [0, 49] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [0, 49] / 25% [5, 70] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 0% [0, 49] / 25% [5, 70] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 56
- H-none: memory → prompt, answer changed after the question 0% [0, 49] (< 20%: met)

## Worked example (from examples.json)

Item `planets-RL-e5f0-0056` (memory → prompt; the patched answer was the answer org kept). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The Earth card is in locker 8. The Jupiter card is in locker 9. The Venus card is in locker 6. The Saturn card is in locker 7. The Mars card is in locker 3.
Which locker holds the card for the largest planet? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The Saturn card is in locker 3. The Jupiter card is in locker 6. The Mars card is in locker 7. The Earth card is in locker 8. The Venus card is in locker 1.
Which locker holds the card for the hottest planet? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 9; after the patch 9. Predicted: answer org kept 9 (p 0.521); answer of bridge alt's statement 6 (p 0.246); answer at the same statement slot 3 (p 0.026); the alt prompt's own answer 1 (p 0.012).

