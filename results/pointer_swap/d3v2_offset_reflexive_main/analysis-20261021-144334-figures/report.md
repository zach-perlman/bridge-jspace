# d3v2_offset_reflexive_main

Run `d3v2_offset_reflexive_main` (results/pointer_swap/), analysis of the saved outputs only.

```
EXP d3v2_offset_reflexive_main @ unknown | model Qwen3.6-27B | n={"RL|e5-off": 287, "RL|e5-pln": 287, "RL|e5-ref": 287, "DL|e5-off": 287, "DL|e5-pln": 287, "DL|e5-ref": 287} | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in RL (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: RL, tokens after the question, transit window (e5-off): position = 7% [5, 11]   Baseline: none = 48% [43, 54], identity = 11% [8, 15], value = 29% [24, 35]   Control: 'same' changed = 0% [0, 1]; random direction changed (max over transit layers) = -; other item changed = -
Figures: results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/by_layer_e5-off.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/by_layer_e5-pln.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/by_layer_e5-ref.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/slots_final_e5-off.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/slots_last_e5-off.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/windows_e5-off.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/domains_final_e5-off.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/levels_final.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/levels_last.png, results/pointer_swap/d3v2_offset_reflexive_main/analysis-20261021-144334-figures/reflexive.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v2_offset_reflexive_main/outcomes.jsonl, rows `family == 'memory → prompt'`, `group == 'final'`, `layer == 'transit'`, `source == 'alt prompt'`, `level == 'e5-off'`: count `role` (n=287); position should be 20, identity 31, value 84, none 139
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 2]; among alt prompt reads won by a predicted digit, 1390/80337 have the runner-up prediction within p 0.1; hook checks self no-op 1722/1722, layer-0 reproduction 1721/1722.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "value", "elements": "mixed"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-off: **alt prompt's own answer (H-value)** (answer org kept 48% [43, 54], answer of bridge alt's statement 11% [8, 15], answer at the same statement slot 7% [5, 11], the alt prompt's own answer 29% [24, 35]); e5-pln: **alt prompt's own answer (H-value)** (answer org kept 44% [38, 49], answer of bridge alt's statement 9% [6, 13], answer at the same statement slot 14% [10, 18], the alt prompt's own answer 32% [27, 37]); e5-ref: **alt prompt's own answer (H-value)** (answer org kept 39% [33, 44], answer of bridge alt's statement 12% [8, 16], answer at the same statement slot 13% [10, 17], the alt prompt's own answer 36% [31, 42])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-off | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 94%) | - | - |
| memory → prompt | question words | e5-pln | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 94%) | - | - |
| memory → prompt | question words | e5-ref | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 94%) | - | - |
| memory → prompt | everything after the question | e5-off | no effect (answer org kept 98%, answer of bridge alt's statement 1%) | no effect (answer org kept 88%, answer of bridge alt's statement 9%) | alt prompt's own answer (H-value) (answer org kept 48%, the alt prompt's own answer 29%) |
| memory → prompt | everything after the question | e5-pln | no effect (answer org kept 98%, answer of bridge alt's statement 1%) | no effect (answer org kept 86%, answer of bridge alt's statement 11%) | alt prompt's own answer (H-value) (answer org kept 44%, the alt prompt's own answer 32%) |
| memory → prompt | everything after the question | e5-ref | no effect (answer org kept 98%, answer of bridge alt's statement 1%) | no effect (answer org kept 87%, answer of bridge alt's statement 10%) | alt prompt's own answer (H-value) (answer org kept 39%, the alt prompt's own answer 36%) |
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 97%, answer of bridge alt's statement 2%) | alt prompt's own answer (H-value) (answer org kept 24%, the alt prompt's own answer 55%) |
| memory → prompt | last two tokens before the answer | e5-pln | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 97%, answer of bridge alt's statement 3%) | alt prompt's own answer (H-value) (answer org kept 21%, the alt prompt's own answer 56%) |
| memory → prompt | last two tokens before the answer | e5-ref | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 97%, answer of bridge alt's statement 2%) | alt prompt's own answer (H-value) (answer org kept 9%, the alt prompt's own answer 77%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5-pln | - | - | - |
| memory → prompt | question words + everything after | e5-ref | - | - | - |
| named → prompt | question words | e5-off | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 91%) | - | - |
| named → prompt | question words | e5-pln | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 69%) | - | - |
| named → prompt | question words | e5-ref | bridge alt's statement (H-word) (answer org kept 1%, answer of bridge alt's statement 70%) | - | - |
| named → prompt | everything after the question | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 10%, the alt prompt's own answer 74%) |
| named → prompt | everything after the question | e5-pln | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 11%, the alt prompt's own answer 72%) |
| named → prompt | everything after the question | e5-ref | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 90%) |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 60%, the alt prompt's own answer 33%) |
| named → prompt | last two tokens before the answer | e5-pln | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 58%, the alt prompt's own answer 30%) |
| named → prompt | last two tokens before the answer | e5-ref | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 27%, the alt prompt's own answer 66%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5-pln | - | - | - |
| named → prompt | question words + everything after | e5-ref | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5-off | 287 | 287 | alt prompt's own answer (H-value) | yes | answer org kept 48% [43, 54], answer of bridge alt's statement 11% [8, 15], answer at the same statement slot 7% [5, 11], the alt prompt's own answer 29% [24, 35] |
| domain:animals | e5-off | 179 | 179 | alt prompt's own answer (H-value) | yes | answer org kept 40% [33, 48], answer of bridge alt's statement 8% [5, 13], answer at the same statement slot 6% [3, 10], the alt prompt's own answer 44% [37, 51] |
| domain:elements | e5-off | 108 | 108 | mixed | yes | answer org kept 62% [53, 71], answer of bridge alt's statement 16% [10, 24], answer at the same statement slot 9% [5, 16], the alt prompt's own answer 5% [2, 10] |
| slot:first | e5-off | 98 | 98 | mixed | yes | answer org kept 52% [42, 62], answer of bridge alt's statement 16% [10, 25], answer at the same statement slot 4% [2, 10], the alt prompt's own answer 26% [18, 35] |
| slot:middle | e5-off | 93 | 93 | alt prompt's own answer (H-value) | yes | answer org kept 48% [38, 58], answer of bridge alt's statement 10% [5, 17], answer at the same statement slot 6% [3, 13], the alt prompt's own answer 32% [24, 42] |
| slot:last | e5-off | 96 | 96 | alt prompt's own answer (H-value) | yes | answer org kept 45% [35, 55], answer of bridge alt's statement 6% [3, 13], answer at the same statement slot 10% [6, 18], the alt prompt's own answer 30% [22, 40] |
| all | e5-pln | 287 | 287 | alt prompt's own answer (H-value) | yes | answer org kept 44% [38, 49], answer of bridge alt's statement 9% [6, 13], answer at the same statement slot 14% [10, 18], the alt prompt's own answer 32% [27, 37] |
| domain:animals | e5-pln | 179 | 179 | alt prompt's own answer (H-value) | yes | answer org kept 32% [25, 39], answer of bridge alt's statement 5% [3, 9], answer at the same statement slot 12% [8, 18], the alt prompt's own answer 49% [42, 56] |
| domain:elements | e5-pln | 108 | 108 | mixed | yes | answer org kept 63% [54, 71], answer of bridge alt's statement 16% [10, 24], answer at the same statement slot 17% [11, 25], the alt prompt's own answer 3% [1, 8] |
| slot:first | e5-pln | 98 | 98 | mixed | yes | answer org kept 50% [40, 60], answer of bridge alt's statement 12% [7, 20], answer at the same statement slot 10% [6, 18], the alt prompt's own answer 26% [18, 35] |
| slot:middle | e5-pln | 93 | 93 | alt prompt's own answer (H-value) | yes | answer org kept 40% [30, 50], answer of bridge alt's statement 9% [4, 16], answer at the same statement slot 15% [9, 24], the alt prompt's own answer 34% [26, 45] |
| slot:last | e5-pln | 96 | 96 | alt prompt's own answer (H-value) | yes | answer org kept 41% [31, 51], answer of bridge alt's statement 6% [3, 13], answer at the same statement slot 17% [11, 25], the alt prompt's own answer 35% [27, 45] |
| all | e5-ref | 287 | 287 | alt prompt's own answer (H-value) | yes | answer org kept 39% [33, 44], answer of bridge alt's statement 12% [8, 16], answer at the same statement slot 13% [10, 17], the alt prompt's own answer 36% [31, 42] |
| domain:animals | e5-ref | 179 | 179 | alt prompt's own answer (H-value) | yes | answer org kept 27% [21, 34], answer of bridge alt's statement 8% [5, 13], answer at the same statement slot 12% [8, 18], the alt prompt's own answer 52% [45, 59] |
| domain:elements | e5-ref | 108 | 108 | mixed | yes | answer org kept 57% [48, 66], answer of bridge alt's statement 18% [12, 26], answer at the same statement slot 14% [9, 22], the alt prompt's own answer 10% [6, 17] |
| slot:first | e5-ref | 98 | 98 | alt prompt's own answer (H-value) | yes | answer org kept 41% [32, 51], answer of bridge alt's statement 14% [9, 23], answer at the same statement slot 4% [2, 10], the alt prompt's own answer 40% [31, 50] |
| slot:middle | e5-ref | 93 | 93 | alt prompt's own answer (H-value) | yes | answer org kept 39% [29, 49], answer of bridge alt's statement 11% [6, 19], answer at the same statement slot 15% [9, 24], the alt prompt's own answer 34% [26, 45] |
| slot:last | e5-ref | 96 | 96 | mixed | yes | answer org kept 36% [28, 46], answer of bridge alt's statement 9% [5, 17], answer at the same statement slot 20% [13, 29], the alt prompt's own answer 34% [26, 44] |

## Checks

`{"self_noop": {"n": 1722, "same_top": 1722, "max_abs_dlogit_max": 1.0625}, "layer0_all_reproduces_source": {"n": 1722, "same_top": 1721, "max_abs_dlogit_max": 1.0}, "unedited_base_answer_read": {"n": 1722, "base_answer": 1722}}`; near ties: `{"n": 80337, "within_gap": 1390, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | question words | 16 | 99% [96, 99] | 1% [1, 4] | 96% [93, 98] | 1% [1, 4] | 0% [0, 1] |
| memory → prompt | e5-off | everything after the question | 48 | 54% [49, 60] | 46% [40, 51] | 26% [21, 31] | 17% [13, 21] | 0% [0, 1] |
| memory → prompt | e5-off | last two tokens before the answer | 60 | 100% [99, 100] | 0% [0, 1] | 0% [0, 2] | 0% [0, 2] | 98% [96, 99] |
| memory → prompt | e5-pln | question words | 16 | 99% [97, 100] | 1% [0, 3] | 96% [93, 98] | 1% [1, 4] | 0% [0, 1] |
| memory → prompt | e5-pln | everything after the question | 48 | 56% [51, 62] | 44% [38, 49] | 25% [21, 31] | 24% [19, 29] | 0% [0, 1] |
| memory → prompt | e5-pln | last two tokens before the answer | 56 | 100% [98, 100] | 0% [0, 2] | 0% [0, 1] | 0% [0, 2] | 99% [97, 100] |
| memory → prompt | e5-ref | question words | 16 | 99% [97, 100] | 1% [0, 3] | 96% [93, 98] | 1% [1, 4] | 1% [0, 2] |
| memory → prompt | e5-ref | everything after the question | 48 | 56% [51, 62] | 44% [38, 49] | 24% [19, 29] | 23% [19, 29] | 7% [4, 10] |
| memory → prompt | e5-ref | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 2] | 99% [98, 100] |
| named → prompt | e5-off | question words | 16 | 100% [99, 100] | 0% [0, 1] | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] |
| named → prompt | e5-off | everything after the question | 56 | 97% [95, 99] | 3% [1, 5] | 0% [0, 1] | 0% [0, 1] | 97% [95, 99] |
| named → prompt | e5-off | last two tokens before the answer | 60 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-pln | question words | 16 | 100% [99, 100] | 0% [0, 1] | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] |
| named → prompt | e5-pln | everything after the question | 56 | 98% [96, 99] | 2% [1, 4] | 0% [0, 1] | 0% [0, 1] | 98% [96, 99] |
| named → prompt | e5-pln | last two tokens before the answer | 60 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-ref | question words | 16 | 100% [99, 100] | 0% [0, 1] | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] |
| named → prompt | e5-ref | everything after the question | 56 | 99% [97, 100] | 1% [0, 3] | 0% [0, 1] | 0% [0, 1] | 99% [97, 100] |
| named → prompt | e5-ref | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |

## Reflexive test (pre-registered v2 rule): the alt prompt's own answer, when it is also in the org prompt vs when it is not (same scenes, paired)

| family | patched tokens | layer | pairs | alt answer, also in org | alt answer, not in org | difference [95% CI] | label | plain cell interpretable |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | everything after the question | 16 | 287 | 0% | 0% | +0 [+0, +1] | value | False |
| memory → prompt | last two tokens before the answer | 16 | 287 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 20 | 287 | 1% | 0% | +1 [+0, +2] | value | False |
| memory → prompt | last two tokens before the answer | 20 | 287 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 24 | 287 | 1% | 0% | +1 [+0, +2] | value | False |
| memory → prompt | last two tokens before the answer | 24 | 287 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 28 | 287 | 0% | 0% | +0 [+0, +1] | value | False |
| memory → prompt | last two tokens before the answer | 28 | 287 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 32 | 287 | 0% | 0% | +0 [+0, +1] | value | False |
| memory → prompt | last two tokens before the answer | 32 | 287 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 36 | 287 | 1% | 0% | +1 [+0, +3] | value | False |
| memory → prompt | last two tokens before the answer | 36 | 287 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 40 | 287 | 1% | 0% | +1 [+0, +2] | value | False |
| memory → prompt | last two tokens before the answer | 40 | 287 | 0% | 0% | +0 [+0, +1] | value | False |
| memory → prompt | everything after the question | 42 | 287 | 1% | 0% | +1 [+0, +3] | value | False |
| memory → prompt | last two tokens before the answer | 42 | 287 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 44 | 287 | 4% | 0% | +4 [+2, +7] | value | True |
| memory → prompt | last two tokens before the answer | 44 | 287 | 0% | 0% | +0 [+0, +1] | value | False |
| memory → prompt | everything after the question | 46 | 287 | 5% | 0% | +5 [+2, +7] | value | True |
| memory → prompt | last two tokens before the answer | 46 | 287 | 1% | 0% | +1 [+0, +2] | value | False |
| memory → prompt | everything after the question | 48 | 287 | 7% | 0% | +7 [+4, +10] | value | True |
| memory → prompt | last two tokens before the answer | 48 | 287 | 1% | 0% | +1 [+0, +3] | value | True |
| memory → prompt | everything after the question | 50 | 287 | 7% | 0% | +7 [+5, +10] | unclear | True |
| memory → prompt | last two tokens before the answer | 50 | 287 | 10% | 0% | +10 [+7, +14] | unclear | True |
| memory → prompt | everything after the question | 52 | 287 | 41% | 33% | +8 [+2, +14] | unclear | True |
| memory → prompt | last two tokens before the answer | 52 | 287 | 77% | 55% | +22 [+15, +29] | reflexive | True |
| memory → prompt | everything after the question | 54 | 287 | 32% | 28% | +4 [-2, +10] | unclear | True |
| memory → prompt | last two tokens before the answer | 54 | 287 | 78% | 55% | +23 [+17, +30] | reflexive | True |
| memory → prompt | everything after the question | 56 | 287 | 52% | 52% | +0 [-3, +5] | value | True |
| memory → prompt | last two tokens before the answer | 56 | 287 | 99% | 99% | +0 [-1, +2] | value | True |
| memory → prompt | everything after the question | 58 | 287 | 51% | 51% | -1 [-5, +3] | value | True |
| memory → prompt | last two tokens before the answer | 58 | 287 | 99% | 99% | +0 [-1, +1] | value | True |
| memory → prompt | everything after the question | 60 | 287 | 44% | 36% | +7 [+2, +13] | unclear | True |
| memory → prompt | last two tokens before the answer | 60 | 287 | 100% | 99% | +1 [+0, +2] | value | True |
| memory → prompt | everything after the question | early | 287 | 0% | 0% | +0 [+0, +1] | value | False |
| memory → prompt | last two tokens before the answer | early | 287 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | mid | 287 | 1% | 0% | +1 [+0, +2] | value | False |
| memory → prompt | last two tokens before the answer | mid | 287 | 0% | 0% | +0 [+0, +1] | value | False |
| memory → prompt | everything after the question | transit | 287 | 36% | 32% | +5 [-1, +10] | unclear | True |
| memory → prompt | last two tokens before the answer | transit | 287 | 77% | 56% | +21 [+14, +28] | reflexive | True |

## Agent priors in the job spec (jobs/d3/d3v2_offset_reflexive_main.yaml `hypotheses`) vs results

- H-order: memory -> prompt, after the question or last two tokens, at the layer of the slot peak (48-50): answer at the same statement slot >= 25% and answer at the same token answer at the same statement slot <= 10% (offset-shift scenes); verdict "answer at the same statement slot"
- H-token: the same cells: same token answer at the same statement slot >= 25% and same statement slot <= 10%; verdict "token"
- H-both: both >= 10% (verdict "mixed"): the pointer is partly positional in tokens, partly in order
- H-reflexive: last two tokens, layers 52-56: the alt answer share with the digit in the org prompt minus without it >= +10 points (paired lower bound)
- H-content: the same difference within ±10 points (CI): the digit is carried as content (v1: 98% alt answer at layer 56 though the digit was never in the org prompt)
- prior: Agent prior: H-order 0.55, H-token 0.25, H-both 0.2; H-content 0.75, H-reflexive 0.25.

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 7% [5, 11], last two tokens 9% [7, 13] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 10% [7, 14] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 11% [8, 15] / 8% [5, 11] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 29% [24, 35] / 55% [49, 60] (>= 50%: met); first single layer where it reaches 20%: after the question 52, last two tokens 52
- H-none: memory → prompt, answer changed after the question 52% [46, 57] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e5-pln-0102` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 48 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The turkey's locker is 5. The spider's locker is 3. The bee's locker is 0. The river was calm early that morning. The frog's locker is 7. The dog's locker is 1.
Which locker belongs to the animal known for gobbling? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The spider's locker is 1. The frog's locker is 9. The turkey's locker is 3. The river was calm early that morning. The dog's locker is 5. The bee's locker is 7.
Which locker belongs to the animal known for croaking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 5; after the patch 3. Predicted: answer org kept 5 (p 0.010); answer of bridge alt's statement 7 (p 0.001); answer at the same statement slot 3 (p 0.984); the alt prompt's own answer 9 (p 0.000).

