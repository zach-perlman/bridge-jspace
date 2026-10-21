# D3: is the statement-slot pointer counted from the start or from the end of the list (or is it a token position)?

Run `d3_start_or_end_main` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5more` = 5 statements, the alt prompt has 6; `e5fewer` = 5 statements, the alt prompt has 4.

```
EXP d3_start_or_end_main @ 596c89e | model Qwen3.6-27B | n per family = memory → prompt 201 (alt has one statement more); memory → prompt 202 (alt has one statement fewer); named → prompt 201 (alt has one statement more); named → prompt 202 (alt has one statement fewer) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5more): position = 7% [5, 12]   Baseline: none = 49% [42, 56], identity = 13% [9, 18], value = 24% [19, 31]   Control: 'same' changed = 0% [0, 3]; random push of the same size changed (max over transit layers) = 1% [0, 4]; another domain's prompt changed = 13% [9, 19]
Figures: results/pointer_swap/d3_start_or_end_main/analysis-20261021-172625-figures/by_layer_e5more.png, results/pointer_swap/d3_start_or_end_main/analysis-20261021-172625-figures/by_layer_e5fewer.png, results/pointer_swap/d3_start_or_end_main/analysis-20261021-172625-figures/slots_final_e5more.png, results/pointer_swap/d3_start_or_end_main/analysis-20261021-172625-figures/slots_last_e5more.png, results/pointer_swap/d3_start_or_end_main/analysis-20261021-172625-figures/windows_e5more.png, results/pointer_swap/d3_start_or_end_main/analysis-20261021-172625-figures/domains_final_e5more.png, results/pointer_swap/d3_start_or_end_main/analysis-20261021-172625-figures/levels_final.png, results/pointer_swap/d3_start_or_end_main/analysis-20261021-172625-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_start_or_end_main/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5more'`: count `role` (n=201); position should be 15, identity 26, value 49, none 99
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 1% [0, 4] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 2]; among alt prompt reads won by a predicted digit, 682/19336 have the runner-up prediction within p 0.1; hook checks self no-op 806/806, layer-0 reproduction 804/806.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "value", "elements": "mixed"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5more: **alt prompt's own answer (H-value)** (answer org kept 49% [42, 56], answer of bridge alt's statement 13% [9, 18], answer at the same statement slot 7% [5, 12], the alt prompt's own answer 24% [19, 31]); e5fewer: **mixed** (answer org kept 55% [48, 62], answer of bridge alt's statement 10% [7, 15], answer at the same statement slot 12% [8, 17], the alt prompt's own answer 16% [12, 22])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5more | - | - | - |
| memory → prompt | question words | e5fewer | - | - | - |
| memory → prompt | everything after the question | e5more | no effect (answer org kept 98%, answer of bridge alt's statement 1%) | no effect (answer org kept 87%, answer of bridge alt's statement 9%) | alt prompt's own answer (H-value) (answer org kept 49%, the alt prompt's own answer 24%) |
| memory → prompt | everything after the question | e5fewer | no effect (answer org kept 98%, answer at the same statement slot 0%) | no effect (answer org kept 85%, answer of bridge alt's statement 12%) | mixed (answer org kept 55%, the alt prompt's own answer 16%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 2%) | alt prompt's own answer (H-value) (answer org kept 18%, the alt prompt's own answer 61%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 2%) | alt prompt's own answer (H-value) (answer org kept 30%, the alt prompt's own answer 48%) |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 86%) |
| named → prompt | everything after the question | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 20%, the alt prompt's own answer 56%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 71%, the alt prompt's own answer 24%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 71%, the alt prompt's own answer 21%) |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5more | 201 | 201 | alt prompt's own answer (H-value) | yes | answer org kept 49% [42, 56], answer of bridge alt's statement 13% [9, 18], answer at the same statement slot 7% [5, 12], the alt prompt's own answer 24% [19, 31] |
| domain:animals | e5more | 117 | 117 | alt prompt's own answer (H-value) | yes | answer org kept 39% [31, 48], answer of bridge alt's statement 12% [7, 19], answer at the same statement slot 7% [4, 13], the alt prompt's own answer 37% [29, 46] |
| domain:elements | e5more | 84 | 84 | mixed | yes | answer org kept 63% [52, 73], answer of bridge alt's statement 14% [8, 23], answer at the same statement slot 8% [4, 16], the alt prompt's own answer 7% [3, 15] |
| slot:first | e5more | 67 | 67 | mixed | yes | answer org kept 57% [45, 68], answer of bridge alt's statement 18% [11, 29], answer at the same statement slot 1% [0, 8], the alt prompt's own answer 18% [11, 29] |
| slot:middle | e5more | 66 | 66 | alt prompt's own answer (H-value) | yes | answer org kept 38% [27, 50], answer of bridge alt's statement 9% [4, 18], answer at the same statement slot 9% [4, 18], the alt prompt's own answer 36% [26, 48] |
| slot:last | e5more | 68 | 68 | mixed | yes | answer org kept 53% [41, 64], answer of bridge alt's statement 12% [6, 22], answer at the same statement slot 12% [6, 22], the alt prompt's own answer 19% [12, 30] |
| all | e5fewer | 202 | 202 | mixed | yes | answer org kept 55% [48, 62], answer of bridge alt's statement 10% [7, 15], answer at the same statement slot 12% [8, 17], the alt prompt's own answer 16% [12, 22] |
| domain:animals | e5fewer | 119 | 119 | alt prompt's own answer (H-value) | yes | answer org kept 50% [42, 59], answer of bridge alt's statement 5% [2, 11], answer at the same statement slot 11% [6, 18], the alt prompt's own answer 27% [20, 35] |
| domain:elements | e5fewer | 83 | 83 | mixed | yes | answer org kept 61% [51, 71], answer of bridge alt's statement 18% [11, 28], answer at the same statement slot 13% [8, 22], the alt prompt's own answer 1% [0, 7] |
| slot:first | e5fewer | 69 | 69 | mixed | yes | answer org kept 57% [45, 68], answer of bridge alt's statement 14% [8, 25], answer at the same statement slot 10% [5, 19], the alt prompt's own answer 12% [6, 21] |
| slot:middle | e5fewer | 66 | 66 | mixed | yes | answer org kept 50% [38, 62], answer of bridge alt's statement 11% [5, 20], answer at the same statement slot 12% [6, 22], the alt prompt's own answer 21% [13, 33] |
| slot:last | e5fewer | 67 | 67 | mixed | yes | answer org kept 58% [46, 69], answer of bridge alt's statement 6% [2, 14], answer at the same statement slot 13% [7, 24], the alt prompt's own answer 16% [9, 27] |

## Checks

`{"self_noop": {"n": 806, "same_top": 806, "max_abs_dlogit_max": 0.7656}, "layer0_all_reproduces_source": {"n": 806, "same_top": 804, "max_abs_dlogit_max": 0.8125}, "unedited_base_answer_read": {"n": 806, "base_answer": 805}}`; near ties: `{"n": 19336, "within_gap": 682, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5more | everything after the question | 48 | 43% [37, 50] | 57% [50, 63] | 16% [12, 22] | 17% [12, 23] | 0% [0, 2] |
| memory → prompt | e5more | last two tokens before the answer | 56 | 100% [98, 100] | 0% [0, 2] | 1% [0, 4] | 1% [0, 4] | 97% [93, 98] |
| memory → prompt | e5fewer | everything after the question | 56 | 44% [37, 50] | 56% [50, 63] | 0% [0, 3] | 0% [-0, 2] | 43% [36, 50] |
| memory → prompt | e5fewer | last two tokens before the answer | 56 | 99% [96, 100] | 1% [0, 4] | 0% [-0, 2] | 0% [-0, 2] | 99% [96, 99] |
| named → prompt | e5more | everything after the question | 56 | 96% [92, 98] | 4% [2, 8] | 0% [0, 2] | 0% [0, 2] | 96% [92, 98] |
| named → prompt | e5more | last two tokens before the answer | 56 | 100% [97, 100] | 0% [0, 3] | 0% [0, 2] | 0% [0, 2] | 100% [97, 100] |
| named → prompt | e5fewer | everything after the question | 56 | 98% [95, 99] | 2% [1, 5] | 0% [-0, 2] | 0% [-0, 2] | 98% [95, 99] |
| named → prompt | e5fewer | last two tokens before the answer | 56 | 99% [96, 99] | 1% [1, 4] | 0% [-0, 2] | 0% [-0, 2] | 99% [96, 99] |

## Agent priors in the job spec (jobs/d3/d3_start_or_end_main.yaml `hypotheses`) vs results

- H-start: memory -> prompt, last two tokens, layer 50 (and after the question, layer 48): answer at the same slot counted from the start >= 25% and counted from the end <= 10%, in both alt types
- H-end: counted from the end >= 25% and from the start <= 10%, in both alt types
- H-token: the same token answer at the same statement slot >= 25%, both slot answers <= 10% (would agree with a token-answer at the same statement slot result of d3v2_offset_reflexive_main)
- H-mixed: two of them >= 10% (verdict "mixed"), or the winner differs between one more and one fewer
- prior: Agent prior: H-start 0.4, H-token 0.25, H-end 0.15, H-mixed 0.2.

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 7% [5, 12], last two tokens 5% [3, 10] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 5% [3, 10] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 13% [9, 18] / 10% [7, 15] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 24% [19, 31] / 61% [54, 67] (>= 50%: met); first single layer where it reaches 20%: after the question 52, last two tokens 52
- H-none: memory → prompt, answer changed after the question 51% [44, 58] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e5more-0008` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 48 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The stairs creaked at night. The paper was left on the step. The sheep's locker is 1. The dog's locker is 5. The duck's locker is 3. The spider's locker is 0. The mouse's locker is 7.
Which locker belongs to the animal known for squeaking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The duck's locker is 3. The turkey's locker is 1. The spider's locker is 9. The mouse's locker is 5. The sheep's locker is 7. The stairs creaked at night. The dog's locker is 0.
Which locker belongs to the animal known for spinning webs? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 7; after the patch 3. Predicted: answer org kept 7 (p 0.373); answer of bridge alt's statement 0 (p 0.065); answer at the same statement slot 3 (p 0.423); answer at the same slot counted from the end 5 (p 0.024); answer at the same token position 1 (p 0.107); the alt prompt's own answer 9 (p 0.001).

