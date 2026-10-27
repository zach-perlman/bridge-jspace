# D3 levels, first version (superseded: too few items for the rule)

Run `d3_pilot_levels_27b` (results/pointer_swap/), analysis of the saved outputs only.

**NOT A HEADLINE RUN (superseded or smoke)**: includes topics that failed the competence check and only 15 prompts per topic. Shown for completeness.

```
EXP d3_pilot_levels_27b @ 3b8db6e | model Qwen3.6-27B | n={"RL|e3f0": 51, "RL|e5f4": 57, "DL|e3f0": 51, "DL|e5f4": 57, "RR|e3f0": 51, "RR|e5f4": 57} | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in RL (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: RL, tokens after the question, transit window (e3f0): position = 43% [30, 57]   Baseline: none = 39% [27, 53], identity = 8% [3, 18], value = 10% [4, 21]   Control: 'same' changed = 0% [0, 7]; random direction changed (max over transit layers) = 0% [0, 7]; other item changed = 16% [8, 28]
Figures: results/pointer_swap/d3_pilot_levels_27b/analysis-20261021-133454-figures/by_layer_e3f0.png, results/pointer_swap/d3_pilot_levels_27b/analysis-20261021-133454-figures/by_layer_e5f4.png, results/pointer_swap/d3_pilot_levels_27b/analysis-20261021-133454-figures/slots_final_e3f0.png, results/pointer_swap/d3_pilot_levels_27b/analysis-20261021-133454-figures/slots_last_e3f0.png, results/pointer_swap/d3_pilot_levels_27b/analysis-20261021-133454-figures/windows_e3f0.png, results/pointer_swap/d3_pilot_levels_27b/analysis-20261021-133454-figures/domains_final_e3f0.png, results/pointer_swap/d3_pilot_levels_27b/analysis-20261021-133454-figures/levels_final.png, results/pointer_swap/d3_pilot_levels_27b/analysis-20261021-133454-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_pilot_levels_27b/outcomes.jsonl, rows `family == 'memory → prompt'`, `group == 'final'`, `layer == 'transit'`, `source == 'alt prompt'`, `level == 'e3f0'`: count `role` (n=51); position should be 22, identity 4, value 5, none 20
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 7] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 7]; among alt prompt reads won by a predicted digit, 479/24267 have the runner-up prediction within p 0.1; hook checks self no-op 324/324, layer-0 reproduction 323/324.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "damage", "elements": "damage", "months": "damage", "planets": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e3f0: **same statement slot (H-pointer)** (answer org kept 39% [27, 53], answer of bridge alt's statement 8% [3, 18], answer at the same statement slot 43% [30, 57], the alt prompt's own answer 10% [4, 21]); e5f4: **mixed** (answer org kept 51% [38, 63], answer of bridge alt's statement 18% [10, 29], answer at the same statement slot 14% [7, 25], the alt prompt's own answer 12% [6, 23])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 2964, in cuts ['domain:animals', 'domain:elements', 'domain:months', 'domain:planets', 'slot:first', 'slot:last', 'slot:middle'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e3f0 | bridge alt's statement (H-word) (answer org kept 8%, answer of bridge alt's statement 86%) | bridge alt's statement (H-word) (answer org kept 10%, answer of bridge alt's statement 67%) | no effect (answer org kept 94%, answer of bridge alt's statement 4%) |
| memory → prompt | question words | e5f4 | bridge alt's statement (H-word) (answer org kept 4%, answer of bridge alt's statement 81%) | bridge alt's statement (H-word) (answer org kept 9%, answer of bridge alt's statement 65%) | no effect (answer org kept 98%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e3f0 | damage (answer org kept 98%, answer of bridge alt's statement 2%) | mixed (answer org kept 69%, answer of bridge alt's statement 18%) | same statement slot (H-pointer) (answer org kept 39%, answer at the same statement slot 43%) |
| memory → prompt | everything after the question | e5f4 | no effect (answer org kept 93%, answer of bridge alt's statement 2%) | no effect (answer org kept 77%, answer of bridge alt's statement 16%) | mixed (answer org kept 51%, answer of bridge alt's statement 18%) |
| memory → prompt | last two tokens before the answer | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 96%, answer of bridge alt's statement 2%) | same statement slot (H-pointer) (answer org kept 29%, answer at the same statement slot 43%) |
| memory → prompt | last two tokens before the answer | e5f4 | no effect (answer org kept 98%, answer of bridge alt's statement 0%) | no effect (answer org kept 95%, answer of bridge alt's statement 4%) | alt prompt's own answer (H-value) (answer org kept 12%, the alt prompt's own answer 49%) |
| memory → prompt | question words + everything after | e3f0 | bridge alt's statement (H-word) (answer org kept 4%, answer of bridge alt's statement 82%) | mixed (answer org kept 4%, answer of bridge alt's statement 61%) | same statement slot (H-pointer) (answer org kept 37%, answer at the same statement slot 47%) |
| memory → prompt | question words + everything after | e5f4 | bridge alt's statement (H-word) (answer org kept 4%, answer of bridge alt's statement 81%) | bridge alt's statement (H-word) (answer org kept 4%, answer of bridge alt's statement 74%) | mixed (answer org kept 40%, answer of bridge alt's statement 23%) |
| named → prompt | question words | e3f0 | same statement slot (H-pointer) (answer org kept 0%, answer at the same statement slot 86%) | same statement slot (H-pointer) (answer org kept 0%, answer at the same statement slot 69%) | same statement slot (H-pointer) (answer org kept 59%, answer at the same statement slot 41%) |
| named → prompt | question words | e5f4 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 79%) | bridge alt's statement (H-word) (answer org kept 5%, answer of bridge alt's statement 74%) | mixed (answer org kept 58%, answer at the same statement slot 23%) |
| named → prompt | everything after the question | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 25%, answer at the same statement slot 57%) |
| named → prompt | everything after the question | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 33%, the alt prompt's own answer 40%) |
| named → prompt | last two tokens before the answer | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 59%, answer at the same statement slot 39%) |
| named → prompt | last two tokens before the answer | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 74%, the alt prompt's own answer 16%) |
| named → prompt | question words + everything after | e3f0 | same statement slot (H-pointer) (answer org kept 0%, answer at the same statement slot 86%) | same statement slot (H-pointer) (answer org kept 0%, answer at the same statement slot 71%) | same statement slot (H-pointer) (answer org kept 10%, answer at the same statement slot 67%) |
| named → prompt | question words + everything after | e5f4 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 79%) | bridge alt's statement (H-word) (answer org kept 5%, answer of bridge alt's statement 70%) | mixed (answer org kept 12%, the alt prompt's own answer 42%) |
| memory → memory | question words | e3f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 94%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 84%) | no effect (answer org kept 80%, answer of bridge alt's statement 16%) |
| memory → memory | question words | e5f4 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 98%) | bridge alt's statement (H-word) (answer org kept 4%, answer of bridge alt's statement 91%) | no effect (answer org kept 74%, answer of bridge alt's statement 26%) |
| memory → memory | everything after the question | e3f0 | no effect (answer org kept 98%, answer of bridge alt's statement 0%) | no effect (answer org kept 80%, answer of bridge alt's statement 16%) | damage (answer org kept 65%, answer of bridge alt's statement 29%) |
| memory → memory | everything after the question | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 91%, answer of bridge alt's statement 9%) | no effect (answer org kept 70%, answer of bridge alt's statement 30%) |
| memory → memory | last two tokens before the answer | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 67%, answer of bridge alt's statement 29%) | damage (answer org kept 18%, answer of bridge alt's statement 76%) |
| memory → memory | last two tokens before the answer | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 77%, answer of bridge alt's statement 23%) | bridge alt's statement (H-word) (answer org kept 26%, answer of bridge alt's statement 74%) |
| memory → memory | question words + everything after | e3f0 | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 96%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 88%) | bridge alt's statement (H-word) (answer org kept 37%, answer of bridge alt's statement 59%) |
| memory → memory | question words + everything after | e5f4 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 96%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 96%) | bridge alt's statement (H-word) (answer org kept 28%, answer of bridge alt's statement 70%) |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e3f0 | 51 | 51 | same statement slot (H-pointer) | yes | answer org kept 39% [27, 53], answer of bridge alt's statement 8% [3, 18], answer at the same statement slot 43% [30, 57], the alt prompt's own answer 10% [4, 21] |
| domain:animals | e3f0 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 20% [7, 45], answer of bridge alt's statement 7% [1, 30], answer at the same statement slot 40% [20, 64], the alt prompt's own answer 33% [15, 58] |
| domain:elements | e3f0 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 33% [15, 58], answer of bridge alt's statement 13% [4, 38], answer at the same statement slot 53% [30, 75], the alt prompt's own answer 0% [-0, 20] |
| domain:months | e3f0 | 6 | 6 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 67% [30, 90], answer of bridge alt's statement 0% [0, 39], answer at the same statement slot 33% [10, 70], the alt prompt's own answer 0% [0, 39] |
| domain:planets | e3f0 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 53% [30, 75], answer of bridge alt's statement 7% [1, 30], answer at the same statement slot 40% [20, 64], the alt prompt's own answer 0% [-0, 20] |
| slot:first | e3f0 | 23 | 23 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 70% [49, 84], answer of bridge alt's statement 13% [5, 32], answer at the same statement slot 17% [7, 37], the alt prompt's own answer 0% [-0, 14] |
| slot:middle | e3f0 | 14 | 14 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 14% [4, 40], answer of bridge alt's statement 7% [1, 31], answer at the same statement slot 64% [39, 84], the alt prompt's own answer 14% [4, 40] |
| slot:last | e3f0 | 14 | 14 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 14% [4, 40], answer of bridge alt's statement 0% [0, 22], answer at the same statement slot 64% [39, 84], the alt prompt's own answer 21% [8, 48] |
| all | e5f4 | 57 | 57 | mixed | yes | answer org kept 51% [38, 63], answer of bridge alt's statement 18% [10, 29], answer at the same statement slot 14% [7, 25], the alt prompt's own answer 12% [6, 23] |
| domain:animals | e5f4 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 13% [4, 38], answer of bridge alt's statement 7% [1, 30], answer at the same statement slot 40% [20, 64], the alt prompt's own answer 40% [20, 64] |
| domain:elements | e5f4 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 60% [36, 80], answer of bridge alt's statement 27% [11, 52], answer at the same statement slot 7% [1, 30], the alt prompt's own answer 0% [-0, 20] |
| domain:months | e5f4 | 12 | 12 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 33% [14, 61], answer of bridge alt's statement 33% [14, 61], answer at the same statement slot 8% [1, 35], the alt prompt's own answer 8% [1, 35] |
| domain:planets | e5f4 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 93% [70, 99], answer of bridge alt's statement 7% [1, 30], answer at the same statement slot 0% [-0, 20], the alt prompt's own answer 0% [-0, 20] |
| slot:first | e5f4 | 11 | 11 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 55% [28, 79], answer of bridge alt's statement 27% [10, 57], answer at the same statement slot 0% [0, 26], the alt prompt's own answer 9% [2, 38] |
| slot:middle | e5f4 | 36 | 36 | mixed | yes | answer org kept 47% [32, 63], answer of bridge alt's statement 17% [8, 32], answer at the same statement slot 19% [10, 35], the alt prompt's own answer 14% [6, 29] |
| slot:last | e5f4 | 10 | 10 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 60% [31, 83], answer of bridge alt's statement 10% [2, 40], answer at the same statement slot 10% [2, 40], the alt prompt's own answer 10% [2, 40] |

## Checks

`{"self_noop": {"n": 324, "same_top": 324, "max_abs_dlogit_max": 1.125}, "layer0_all_reproduces_source": {"n": 324, "same_top": 323, "max_abs_dlogit_max": 1.6875}, "unedited_base_answer_read": {"n": 324, "base_answer": 324}}`; near ties: `{"n": 24267, "within_gap": 479, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e3f0 | question words | 8 | 96% [87, 99] | 4% [1, 13] | 92% [82, 97] | 4% [1, 13] | 0% [0, 7] |
| memory → prompt | e3f0 | everything after the question | 48 | 53% [40, 66] | 47% [34, 60] | 4% [1, 13] | 49% [36, 62] | 0% [0, 7] |
| memory → prompt | e3f0 | last two tokens before the answer | 60 | 96% [87, 99] | 4% [1, 13] | 0% [0, 7] | 0% [0, 7] | 96% [87, 99] |
| memory → prompt | e3f0 | question words + everything after | 0 | 94% [84, 98] | 6% [2, 16] | 90% [79, 96] | 4% [1, 13] | 0% [0, 7] |
| memory → prompt | e5f4 | question words | 4 | 96% [88, 99] | 4% [1, 12] | 89% [79, 95] | 4% [1, 12] | 0% [0, 6] |
| memory → prompt | e5f4 | everything after the question | 48 | 30% [20, 43] | 70% [57, 80] | 11% [5, 21] | 16% [9, 27] | 0% [0, 6] |
| memory → prompt | e5f4 | last two tokens before the answer | 60 | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] | 0% [0, 6] | 98% [91, 100] |
| memory → prompt | e5f4 | question words + everything after | 20 | 98% [91, 100] | 2% [0, 9] | 89% [79, 95] | 5% [2, 14] | 0% [0, 6] |
| named → prompt | e3f0 | question words | 0 | 100% [93, 100] | 0% [0, 7] | 100% [93, 100] | 0% [0, 7] | 0% [0, 7] |
| named → prompt | e3f0 | everything after the question | 56 | 98% [90, 100] | 2% [0, 10] | 0% [0, 7] | 0% [0, 7] | 98% [90, 100] |
| named → prompt | e3f0 | last two tokens before the answer | 60 | 100% [93, 100] | 0% [0, 7] | 0% [0, 7] | 0% [0, 7] | 100% [93, 100] |
| named → prompt | e3f0 | question words + everything after | 0 | 100% [93, 100] | 0% [0, 7] | 100% [93, 100] | 0% [0, 7] | 0% [0, 7] |
| named → prompt | e5f4 | question words | 0 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| named → prompt | e5f4 | everything after the question | 56 | 84% [73, 91] | 16% [9, 27] | 0% [0, 6] | 0% [0, 6] | 84% [73, 91] |
| named → prompt | e5f4 | last two tokens before the answer | 56 | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] | 0% [0, 6] | 100% [94, 100] |
| named → prompt | e5f4 | question words + everything after | 0 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| memory → memory | e3f0 | question words | 0 | 100% [93, 100] | 0% [0, 7] | 96% [87, 99] | 0% [0, 7] | 0% [0, 7] |
| memory → memory | e3f0 | everything after the question | 44 | 22% [12, 35] | 78% [65, 88] | 18% [10, 30] | 0% [0, 7] | 0% [0, 7] |
| memory → memory | e3f0 | last two tokens before the answer | 60 | 100% [93, 100] | 0% [0, 7] | 100% [93, 100] | 0% [0, 7] | 0% [0, 7] |
| memory → memory | e3f0 | question words + everything after | 0 | 100% [93, 100] | 0% [0, 7] | 94% [84, 98] | 0% [0, 7] | 0% [0, 7] |
| memory → memory | e5f4 | question words | 0 | 100% [94, 100] | 0% [0, 6] | 96% [88, 99] | 0% [0, 6] | 0% [0, 6] |
| memory → memory | e5f4 | everything after the question | 52 | 21% [12, 33] | 79% [67, 88] | 21% [12, 33] | 0% [0, 6] | 0% [0, 6] |
| memory → memory | e5f4 | last two tokens before the answer | 60 | 96% [88, 99] | 4% [1, 12] | 96% [88, 99] | 0% [0, 6] | 0% [0, 6] |
| memory → memory | e5f4 | question words + everything after | 0 | 100% [94, 100] | 0% [0, 6] | 96% [88, 99] | 0% [0, 6] | 0% [0, 6] |

## Agent priors in the job spec (jobs/d3/d3_pilot_levels_27b.yaml `hypotheses`) vs results

- H-robust: memory → prompt final/last at the transit window: the pilot's winning outcome keeps its share at e5f4 within 0.15
- H-contiguity: the winning outcome's share drops by more than 0.15 with filler (e5f4 vs e5f0)
- H-fewer-entities: answer at the same statement slot share at e3f0 above e5f0 by more than 0.15 (positional route dominates at N=3)
- prior: Coordinator prior: H-robust 0.65; H-fewer-entities 0.4.

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 43% [30, 57], last two tokens 43% [30, 57] (>= 50%: not met); memory → memory 0% [0, 7] / 0% [0, 7] (<= 10%: met); named → prompt after the question 57% [43, 70] (>= 50%: met)
- H-word: memory → prompt, answer of bridge alt's statement: 8% [3, 18] / 12% [6, 23] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 10% [4, 21] / 16% [8, 28] (>= 50%: not met); first single layer where it reaches 20%: after the question 56, last two tokens 56
- H-none: memory → prompt, answer changed after the question 61% [47, 73] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e5f4-0039` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 44 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The bee's locker is 1. The street was lined with trees. The sheep's locker is 3. The market was busy on Saturday. The turkey's locker is 5. The museum had a new exhibit. The mouse's locker is 7. The cow's locker is 8. The sky turned grey by noon.
Which locker belongs to the animal known for its wool? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The turkey's locker is 9. The street was lined with trees. The cow's locker is 5. The market was busy on Saturday. The mouse's locker is 1. The museum had a new exhibit. The bee's locker is 8. The sheep's locker is 3. The sky turned grey by noon.
Which locker belongs to the animal known for gobbling? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 3; after the patch 1. Predicted: answer org kept 3 (p 0.067); answer of bridge alt's statement 5 (p 0.000); answer at the same statement slot 1 (p 0.927); the alt prompt's own answer 9 (p 0.000).

