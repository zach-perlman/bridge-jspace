# D3 v5 on Qwen3.5-122B: does the same-slot answer survive colour-word answers and 8-statement lists?

Run `qwen35_122b_d3v5_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-digit` = 5 statements, digit answers; `e5-word` = 5 statements, colour-word answers; `e8-digit` = 8 statements, digit answers; `e8-word` = 8 statements, colour-word answers.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP qwen35_122b_d3v5_swap @ unknown | model Qwen3.5-122B-A10B-FP8 (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 33-39: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-digit): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/by_layer_e5-digit.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/by_layer_e5-word.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/by_layer_e8-digit.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/by_layer_e8-word.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/slots_final_e5-digit.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/slots_last_e5-digit.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/windows_e5-digit.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/domains_final_e5-digit.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/levels_final.png, results/pointer_swap/qwen35_122b_d3v5_swap/analysis-20261023-055743-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/qwen35_122b_d3v5_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-digit'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 208/34681 have the runner-up prediction within p 0.1; hook checks self no-op 3262/3328, layer-0 reproduction 3281/3328.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-digit: **no data** (-); e5-word: **no data** (-); e8-digit: **no data** (-); e8-word: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-digit | - | - | - |
| memory → prompt | question words | e5-word | - | - | - |
| memory → prompt | question words | e8-digit | - | - | - |
| memory → prompt | question words | e8-word | - | - | - |
| memory → prompt | everything after the question | e5-digit | - | - | - |
| memory → prompt | everything after the question | e5-word | - | - | - |
| memory → prompt | everything after the question | e8-digit | - | - | - |
| memory → prompt | everything after the question | e8-word | - | - | - |
| memory → prompt | last two tokens before the answer | e5-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer of bridge alt's statement 1%) |
| memory → prompt | last two tokens before the answer | e5-word | damage (answer org kept 88%, answer of bridge alt's statement 0%) | damage (answer org kept 87%, answer of bridge alt's statement 0%) | damage (answer org kept 87%, answer of bridge alt's statement 0%) |
| memory → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 1%) |
| memory → prompt | last two tokens before the answer | e8-word | damage (answer org kept 93%, answer of bridge alt's statement 0%) | damage (answer org kept 92%, answer of bridge alt's statement 0%) | damage (answer org kept 91%, answer of bridge alt's statement 0%) |
| memory → prompt | question words + everything after | e5-digit | - | - | - |
| memory → prompt | question words + everything after | e5-word | - | - | - |
| memory → prompt | question words + everything after | e8-digit | - | - | - |
| memory → prompt | question words + everything after | e8-word | - | - | - |
| named → prompt | question words | e5-digit | - | - | - |
| named → prompt | question words | e5-word | - | - | - |
| named → prompt | question words | e8-digit | - | - | - |
| named → prompt | question words | e8-word | - | - | - |
| named → prompt | everything after the question | e5-digit | - | - | - |
| named → prompt | everything after the question | e5-word | - | - | - |
| named → prompt | everything after the question | e8-digit | - | - | - |
| named → prompt | everything after the question | e8-word | - | - | - |
| named → prompt | last two tokens before the answer | e5-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5-word | no effect (answer org kept 93%, answer of bridge alt's statement 0%) | no effect (answer org kept 93%, answer of bridge alt's statement 0%) | no effect (answer org kept 93%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e8-word | no effect (answer org kept 97%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 0%) |
| named → prompt | question words + everything after | e5-digit | - | - | - |
| named → prompt | question words + everything after | e5-word | - | - | - |
| named → prompt | question words + everything after | e8-digit | - | - | - |
| named → prompt | question words + everything after | e8-word | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 3328, "same_top": 3262, "max_abs_dlogit_max": 3.5312}, "layer0_all_reproduces_source": {"n": 3328, "same_top": 3281, "max_abs_dlogit_max": 4.0}, "unedited_base_answer_read": {"n": 3328, "base_answer": 3209}}`; near ties: `{"n": 34681, "within_gap": 208, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-digit | last two tokens before the answer | 42 | 81% [77, 85] | 19% [15, 23] | 31% [27, 35] | 43% [38, 48] | 0% [0, 1] |
| memory → prompt | e5-word | last two tokens before the answer | 42 | 37% [32, 42] | 63% [58, 68] | 6% [4, 8] | 7% [4, 9] | 0% [0, 1] |
| memory → prompt | e8-digit | last two tokens before the answer | 42 | 87% [84, 91] | 13% [9, 16] | 44% [40, 50] | 28% [24, 33] | 0% [0, 1] |
| memory → prompt | e8-word | last two tokens before the answer | 42 | 36% [30, 41] | 64% [59, 70] | 9% [6, 13] | 5% [3, 8] | 0% [0, 1] |
| named → prompt | e5-digit | last two tokens before the answer | 42 | 80% [76, 84] | 20% [16, 24] | 24% [21, 29] | 47% [42, 52] | 0% [0, 1] |
| named → prompt | e5-word | last two tokens before the answer | 42 | 52% [47, 57] | 48% [43, 53] | 4% [3, 7] | 12% [9, 16] | 0% [0, 1] |
| named → prompt | e8-digit | last two tokens before the answer | 42 | 86% [82, 89] | 14% [11, 18] | 39% [34, 44] | 32% [28, 37] | 0% [0, 1] |
| named → prompt | e8-word | last two tokens before the answer | 42 | 38% [33, 43] | 62% [57, 67] | 6% [4, 9] | 10% [7, 13] | 0% [0, 1] |

## Pre-registered primary (pointer_v5): memory -> prompt, the last two tokens, layers 21 and 24 and 27 and 30 and 33 and 36 and 39 and 42: does each layout keep the statement slot?

| layout | keeps the slot | per layer: pooled verdict, topics with the slot |
|---|---|---|
| 5 statements, digits | **no** | 21: none, 0/3; 24: none, 0/3; 27: none, 0/3; 30: none, 0/3; 33: none, 0/3; 36: none, 0/3; 39: none, 0/3; 42: position, 1/3 |
| 5 statements, colour words | **no** | 21: damage, 0/3; 24: damage, 0/3; 27: damage, 0/3; 30: damage, 0/3; 33: damage, 0/3; 36: damage, 0/3; 39: damage, 0/3; 42: damage, 0/3 |
| 8 statements, digits | **no** | 21: none, 0/3; 24: none, 0/3; 27: none, 0/3; 30: none, 0/3; 33: none, 0/3; 36: none, 0/3; 39: none, 0/3; 42: identity, 0/3 |
| 8 statements, colour words | **no** | 21: damage, 0/3; 24: damage, 0/3; 27: damage, 0/3; 30: damage, 0/3; 33: damage, 0/3; 36: damage, 0/3; 39: damage, 0/3; 42: damage, 0/3 |

## Agent priors in the job spec (jobs/d3/qwen35_122b_d3v5_swap.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v5 tests (H-word, H-long) come out as on Qwen3.6-27B. Prior 0.4 (copied from qwen35_9b_d3v5_swap_r2)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 0% [0, 1] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 0% [0, 1] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens None
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `body-RL-e5-digit-0012` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 39 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The chart on the ear is kept in folder 6. The chart on the wrist is kept in folder 9. The chart on the ankle is kept in folder 3. The chart on the heart is kept in folder 7. The chart on the skull is kept in folder 5.
In which folder is the chart on the body part joining hand and arm? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The chart on the skull is kept in folder 4. The chart on the ankle is kept in folder 5. The chart on the wrist is kept in folder 9. The chart on the ear is kept in folder 3. The chart on the heart is kept in folder 8.
In which folder is the chart on the body part that protects the brain? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 9; after the patch 6. Predicted: answer org kept 9 (p 0.434); answer of bridge alt's statement 5 (p 0.003); answer at the same statement slot 6 (p 0.492); the alt prompt's own answer 4 (p 0.010).

