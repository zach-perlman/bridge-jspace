# Finding 5 by the fixed rule on fresh 8-sentence lists (Qwen3.5-122B, layers 33-42)

Run `qwen35_122b_d3v5_len8_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e8-digit` = 8 statements, digit answers; `e8-word` = 8 statements, colour-word answers.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP qwen35_122b_d3v5_len8_swap @ unknown | model Qwen3.5-122B-A10B-FP8 (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 33-39: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e8-digit): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/qwen35_122b_d3v5_len8_swap/analysis-20261023-051446-figures/by_layer_e8-digit.png, results/pointer_swap/qwen35_122b_d3v5_len8_swap/analysis-20261023-051446-figures/by_layer_e8-word.png, results/pointer_swap/qwen35_122b_d3v5_len8_swap/analysis-20261023-051446-figures/slots_final_e8-digit.png, results/pointer_swap/qwen35_122b_d3v5_len8_swap/analysis-20261023-051446-figures/slots_last_e8-digit.png, results/pointer_swap/qwen35_122b_d3v5_len8_swap/analysis-20261023-051446-figures/windows_e8-digit.png, results/pointer_swap/qwen35_122b_d3v5_len8_swap/analysis-20261023-051446-figures/domains_final_e8-digit.png, results/pointer_swap/qwen35_122b_d3v5_len8_swap/analysis-20261023-051446-figures/levels_final.png, results/pointer_swap/qwen35_122b_d3v5_len8_swap/analysis-20261023-051446-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/qwen35_122b_d3v5_len8_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e8-digit'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 100/14876 have the runner-up prediction within p 0.1; hook checks self no-op 1541/1568, layer-0 reproduction 1544/1568.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e8-digit: **no data** (-); e8-word: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e8-digit | - | - | - |
| memory → prompt | question words | e8-word | - | - | - |
| memory → prompt | everything after the question | e8-digit | - | - | - |
| memory → prompt | everything after the question | e8-word | - | - | - |
| memory → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 1%) |
| memory → prompt | last two tokens before the answer | e8-word | damage (answer org kept 88%, answer of bridge alt's statement 0%) | damage (answer org kept 89%, answer of bridge alt's statement 0%) | damage (answer org kept 89%, answer of bridge alt's statement 0%) |
| memory → prompt | question words + everything after | e8-digit | - | - | - |
| memory → prompt | question words + everything after | e8-word | - | - | - |
| named → prompt | question words | e8-digit | - | - | - |
| named → prompt | question words | e8-word | - | - | - |
| named → prompt | everything after the question | e8-digit | - | - | - |
| named → prompt | everything after the question | e8-word | - | - | - |
| named → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e8-word | no effect (answer org kept 97%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 0%) | no effect (answer org kept 97%, answer of bridge alt's statement 0%) |
| named → prompt | question words + everything after | e8-digit | - | - | - |
| named → prompt | question words + everything after | e8-word | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 1568, "same_top": 1541, "max_abs_dlogit_max": 3.1152}, "layer0_all_reproduces_source": {"n": 1568, "same_top": 1544, "max_abs_dlogit_max": 3.125}, "unedited_base_answer_read": {"n": 1568, "base_answer": 1508}}`; near ties: `{"n": 14876, "within_gap": 100, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e8-digit | last two tokens before the answer | 42 | 86% [83, 90] | 14% [10, 17] | 42% [37, 47] | 30% [25, 34] | 0% [0, 1] |
| memory → prompt | e8-word | last two tokens before the answer | 42 | 35% [30, 40] | 65% [60, 70] | 10% [8, 14] | 5% [3, 7] | 0% [0, 1] |
| named → prompt | e8-digit | last two tokens before the answer | 42 | 86% [83, 90] | 14% [10, 17] | 38% [32, 42] | 32% [28, 37] | 0% [0, 1] |
| named → prompt | e8-word | last two tokens before the answer | 42 | 41% [36, 45] | 59% [55, 64] | 6% [4, 9] | 7% [5, 10] | 0% [0, 1] |

## Pre-registered primary (pointer_v5): memory -> prompt, the last two tokens, layers 36 and 38: does each layout keep the statement slot?

| layout | keeps the slot | per layer: pooled verdict, topics with the slot |
|---|---|---|
| 8 statements, digits | **no** | 36: none, 0/3; 38: none, 0/3 |
| 8 statements, colour words | **no** | 36: damage, 0/3; 38: damage, 0/3 |

## Agent priors in the job spec (jobs/d3/qwen35_122b_d3v5_len8_swap.yaml `hypotheses`) vs results

- H-A: e8-digit: answer at the same statement slot - answer of bridge alt's statement (1st and 2nd) has its entity-cluster 95% lower bound > 0. Prior 0.9 (agent's) (copied from d3v5_len8_swap_27b)
- H-B: e8-digit: answer of bridge alt's statement - answer at the same statement slot (3rd-8th) >= 0 with lower bound >= -0.05. Prior 0.75 (agent's) (copied from d3v5_len8_swap_27b)
- H-word: e8-word gets the same verdict as e8-digit (reported, not decisive). Prior 0.6 (agent's) (copied from d3v5_len8_swap_27b)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 1% [0, 3] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 0% [0, 1] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens None
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e8-digit-0067` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The horse keeps its things in locker 8. The moth keeps its things in locker 5. The mouse keeps its things in locker 7. The goat keeps its things in locker 1. The cat keeps its things in locker 2. The fish keeps its things in locker 3. The snake keeps its things in locker 0. The camel keeps its things in locker 6.
In which locker does the animal known for climbing cliffs keep its things? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The snake keeps its things in locker 9. The mouse keeps its things in locker 0. The cat keeps its things in locker 8. The horse keeps its things in locker 5. The goat keeps its things in locker 7. The moth keeps its things in locker 3. The camel keeps its things in locker 6. The fish keeps its things in locker 1.
In which locker does the animal known for hissing keep its things? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 1; after the patch 8. Predicted: answer org kept 1 (p 0.286); answer of bridge alt's statement 0 (p 0.064); answer at the same statement slot 8 (p 0.534); the alt prompt's own answer 9 (p 0.002).

