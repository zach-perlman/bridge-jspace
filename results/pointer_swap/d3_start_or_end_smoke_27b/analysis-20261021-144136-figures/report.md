# D3 start-or-end test run: the scenes with one statement more or fewer work in the patching code on the 27B

Run `d3_start_or_end_smoke_27b` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5more` = 5 statements, the alt prompt has 6; `e5fewer` = 5 statements, the alt prompt has 4.

```
EXP d3_start_or_end_smoke_27b @ unknown | model Qwen3.6-27B | n per family = memory → prompt 2 (alt has one statement more); memory → prompt 2 (alt has one statement fewer); named → prompt 2 (alt has one statement more); named → prompt 2 (alt has one statement fewer) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5more): position = 0% [0, 66]   Baseline: none = 100% [34, 100], identity = 0% [0, 66], value = 0% [0, 66]   Control: 'same' changed = 0% [0, 66]; random push of the same size changed (max over transit layers) = 0% [0, 66]; another domain's prompt changed = 100% [34, 100]
Figures: results/pointer_swap/d3_start_or_end_smoke_27b/analysis-20261021-144136-figures/by_layer_e5more.png, results/pointer_swap/d3_start_or_end_smoke_27b/analysis-20261021-144136-figures/by_layer_e5fewer.png, results/pointer_swap/d3_start_or_end_smoke_27b/analysis-20261021-144136-figures/slots_final_e5more.png, results/pointer_swap/d3_start_or_end_smoke_27b/analysis-20261021-144136-figures/slots_last_e5more.png, results/pointer_swap/d3_start_or_end_smoke_27b/analysis-20261021-144136-figures/windows_e5more.png, results/pointer_swap/d3_start_or_end_smoke_27b/analysis-20261021-144136-figures/domains_final_e5more.png, results/pointer_swap/d3_start_or_end_smoke_27b/analysis-20261021-144136-figures/levels_final.png, results/pointer_swap/d3_start_or_end_smoke_27b/analysis-20261021-144136-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_start_or_end_smoke_27b/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5more'`: count `role` (n=2); position should be 0, identity 0, value 0, none 2
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 66] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 66]; among alt prompt reads won by a predicted digit, 3/112 have the runner-up prediction within p 0.1; hook checks self no-op 8/8, layer-0 reproduction 8/8.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "damage", "elements": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5more: **damage** (answer org kept 100% [34, 100], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 0% [0, 66]); e5fewer: **damage** (answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 50% [9, 91])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 252, in cuts ['all', 'domain:animals', 'domain:elements', 'slot:last', 'slot:middle'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5more | - | - | - |
| memory → prompt | question words | e5fewer | - | - | - |
| memory → prompt | everything after the question | e5more | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5fewer | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 50%, answer of bridge alt's statement 50%) | damage (answer org kept 0%, the alt prompt's own answer 50%) |
| memory → prompt | last two tokens before the answer | e5more | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 50%, answer of bridge alt's statement 0%) |
| memory → prompt | last two tokens before the answer | e5fewer | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, the alt prompt's own answer 100%) |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5more | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| named → prompt | everything after the question | e5fewer | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 50%, the alt prompt's own answer 50%) |
| named → prompt | last two tokens before the answer | e5more | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5fewer | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 50%, the alt prompt's own answer 50%) |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5more | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [34, 100], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 0% [0, 66] |
| domain:animals | e5more | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| domain:elements | e5more | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| slot:middle | e5more | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| slot:last | e5more | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| all | e5fewer | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 50% [9, 91] |
| domain:animals | e5fewer | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 100% [21, 100] |
| domain:elements | e5fewer | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| slot:middle | e5fewer | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 50% [9, 91] |

## Checks

`{"self_noop": {"n": 8, "same_top": 8, "max_abs_dlogit_max": 0.2734}, "layer0_all_reproduces_source": {"n": 8, "same_top": 8, "max_abs_dlogit_max": 0.3125}, "unedited_base_answer_read": {"n": 8, "base_answer": 8}}`; near ties: `{"n": 112, "within_gap": 3, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5more | everything after the question | 48 | 50% [9, 91] | 50% [9, 91] | 0% [0, 66] | 50% [9, 91] | 0% [0, 66] |
| memory → prompt | e5more | last two tokens before the answer | 56 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 0% [0, 66] | 100% [34, 100] |
| memory → prompt | e5fewer | everything after the question | 44 | 50% [9, 91] | 50% [9, 91] | 0% [0, 66] | 0% [0, 66] | 0% [0, 66] |
| memory → prompt | e5fewer | last two tokens before the answer | 52 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 0% [0, 66] | 100% [34, 100] |
| named → prompt | e5more | everything after the question | 52 | 50% [9, 91] | 50% [9, 91] | 0% [0, 66] | 0% [0, 66] | 50% [9, 91] |
| named → prompt | e5more | last two tokens before the answer | 56 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 0% [0, 66] | 100% [34, 100] |
| named → prompt | e5fewer | everything after the question | 56 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 0% [0, 66] | 100% [34, 100] |
| named → prompt | e5fewer | last two tokens before the answer | 56 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 0% [0, 66] | 100% [34, 100] |

## Agent priors in the job spec (jobs/d3/d3_start_or_end_smoke_27b.yaml `hypotheses`) vs results

- H-ok: self no-op and layer-0 reproduction 8/8
- H-broken: any check below 8/8: stop the main run

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [0, 66], last two tokens 0% [0, 66] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 50% [9, 91] (>= 50%: met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [0, 66] / 0% [0, 66] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 0% [0, 66] / 0% [0, 66] (>= 50%: not met); first single layer where it reaches 20%: after the question 56, last two tokens 56
- H-none: memory → prompt, answer changed after the question 0% [0, 66] (< 20%: met)

## Worked example (from examples.json)

Item `animals-RL-e5more-0049` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 48 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The kitchen window looked onto the yard. The sheep's locker is 0. The turkey's locker is 3. The paper was left on the step. The goose's locker is 7. The frog's locker is 8. The dog's locker is 1.
Which locker belongs to the animal known for gobbling? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The frog's locker is 3. The turkey's locker is 8. The goose's locker is 0. The dog's locker is 9. The sheep's locker is 6. The duck's locker is 1. The kitchen window looked onto the yard.
Which locker belongs to the animal known for its wool? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 3; after the patch 1. Predicted: answer org kept 3 (p 0.105); answer of bridge alt's statement 0 (p 0.000); answer at the same statement slot 1 (p 0.876); answer at the same slot counted from the end 8 (p 0.005); answer at the same token position 7 (p 0.001); the alt prompt's own answer 6 (p 0.000).

