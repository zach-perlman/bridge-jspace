# D3 v5 on Qwen3.5-9B: does the same-slot answer survive colour-word answers and 8-statement ...

Run `qwen35_9b_d3v5_swap_r2` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-digit` = 5 statements, digit answers; `e5-word` = 5 statements, colour-word answers; `e8-digit` = 8 statements, digit answers; `e8-word` = 8 statements, colour-word answers.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP qwen35_9b_d3v5_swap_r2 @ unknown | model Qwen3.5-9B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-digit): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/by_layer_e5-digit.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/by_layer_e5-word.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/by_layer_e8-digit.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/by_layer_e8-word.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/slots_final_e5-digit.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/slots_last_e5-digit.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/windows_e5-digit.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/domains_final_e5-digit.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/levels_final.png, results/pointer_swap/qwen35_9b_d3v5_swap_r2/analysis-20261022-102428-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/qwen35_9b_d3v5_swap_r2/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-digit'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 2078/30182 have the runner-up prediction within p 0.1; hook checks self no-op 2853/2860, layer-0 reproduction 2856/2860.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-digit: **no data** (-); e5-word: **no data** (-); e8-digit: **no data** (-); e8-word: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 44, in cuts ['slot:first'].

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
| memory → prompt | last two tokens before the answer | e5-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 15%, answer at the same statement slot 38%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 92%) |
| memory → prompt | last two tokens before the answer | e5-word | damage (answer org kept 94%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 55%, answer at the same statement slot 23%) | alt prompt's own answer (H-value) (answer org kept 35%, the alt prompt's own answer 53%) |
| memory → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 13%, answer of bridge alt's statement 41%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 95%) |
| memory → prompt | last two tokens before the answer | e8-word | no effect (answer org kept 96%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 56%, answer of bridge alt's statement 22%) | alt prompt's own answer (H-value) (answer org kept 23%, the alt prompt's own answer 70%) |
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
| named → prompt | last two tokens before the answer | e5-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 35%, answer at the same statement slot 38%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 96%) |
| named → prompt | last two tokens before the answer | e5-word | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 65%, answer at the same statement slot 25%) | alt prompt's own answer (H-value) (answer org kept 40%, the alt prompt's own answer 54%) |
| named → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 27%, answer of bridge alt's statement 25%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 99%) |
| named → prompt | last two tokens before the answer | e8-word | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 62%, answer of bridge alt's statement 17%) | alt prompt's own answer (H-value) (answer org kept 23%, the alt prompt's own answer 73%) |
| named → prompt | question words + everything after | e5-digit | - | - | - |
| named → prompt | question words + everything after | e5-word | - | - | - |
| named → prompt | question words + everything after | e8-digit | - | - | - |
| named → prompt | question words + everything after | e8-word | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 2860, "same_top": 2853, "max_abs_dlogit_max": 1.2345}, "layer0_all_reproduces_source": {"n": 2860, "same_top": 2856, "max_abs_dlogit_max": 1.4688}, "unedited_base_answer_read": {"n": 2860, "base_answer": 2817}}`; near ties: `{"n": 30182, "within_gap": 2078, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-digit | last two tokens before the answer | 28 | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 0% [-0, 1] | 100% [98, 100] |
| memory → prompt | e5-word | last two tokens before the answer | 28 | 98% [95, 99] | 2% [1, 5] | 0% [0, 2] | 0% [-0, 1] | 93% [90, 95] |
| memory → prompt | e8-digit | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [98, 100] |
| memory → prompt | e8-word | last two tokens before the answer | 28 | 95% [92, 98] | 5% [2, 8] | 0% [0, 1] | 0% [0, 1] | 93% [90, 96] |
| named → prompt | e5-digit | last two tokens before the answer | 28 | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 0% [-0, 1] | 100% [99, 100] |
| named → prompt | e5-word | last two tokens before the answer | 28 | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 0% [-0, 1] | 100% [98, 100] |
| named → prompt | e8-digit | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e8-word | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |

## Pre-registered primary (pointer_v5): memory -> prompt, the last two tokens, layers 14 and 16 and 18 and 20 and 22 and 24 and 26 and 28: does each layout keep the statement slot?

| layout | keeps the slot | per layer: pooled verdict, topics with the slot |
|---|---|---|
| 5 statements, digits | **no** | 14: none, 0/3; 16: none, 0/3; 18: identity, 0/3; 20: mixed, 0/3; 22: mixed, 0/3; 24: value, 0/3; 26: value, 0/3; 28: value, 0/3 |
| 5 statements, colour words | **no** | 14: damage, 0/3; 16: damage, 0/3; 18: mixed, 0/3; 20: position, 0/3; 22: position, 0/3; 24: value, 0/3; 26: value, 0/3; 28: damage, 0/3 |
| 8 statements, digits | **no** | 14: none, 0/3; 16: none, 0/3; 18: identity, 0/3; 20: identity, 0/3; 22: identity, 0/3; 24: value, 0/3; 26: value, 0/3; 28: value, 0/3 |
| 8 statements, colour words | **no** | 14: none, 0/3; 16: none, 0/3; 18: identity, 0/3; 20: identity, 0/3; 22: identity, 0/3; 24: value, 0/3; 26: value, 0/3; 28: value, 0/3 |

## Agent priors in the job spec (jobs/d3/qwen35_9b_d3v5_swap_r2.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v5 tests (H-word, H-long) come out as on Qwen3.6-27B. Prior 0.4

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 3% [1, 5] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 3] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 92% [88, 94] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 24
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e8-digit-0130` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 22 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
Drawer 5 holds the Australia file. Drawer 2 holds the Japan file. Drawer 8 holds the Canada file. Drawer 9 holds the Finland file. Drawer 1 holds the Thailand file. Drawer 4 holds the Ireland file. Drawer 3 holds the Iran file. Drawer 0 holds the Chile file.
Which drawer holds the file on the country whose capital is Bangkok? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
Drawer 4 holds the Canada file. Drawer 7 holds the Finland file. Drawer 2 holds the Japan file. Drawer 8 holds the Thailand file. Drawer 0 holds the Chile file. Drawer 9 holds the Ireland file. Drawer 5 holds the Iran file. Drawer 3 holds the Australia file.
Which drawer holds the file on the country whose capital is Helsinki? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 1; after the patch 2. Predicted: answer org kept 1 (p 0.021); answer of bridge alt's statement 9 (p 0.035); answer at the same statement slot 2 (p 0.906); the alt prompt's own answer 7 (p 0.004).

