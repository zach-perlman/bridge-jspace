# D3 v4x: does the last-token pointer name the statement by its order and from the start, on 85 entities and 9 wordings?

Run `d3v4x_swap_main` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP d3v4x_swap_main @ unknown | model Qwen3.6-27B (chat format) | n per family = memory → prompt 435 items / 85 entities / 27 wordings (filler moved); memory → prompt 434 items / 85 entities / 27 wordings (alt has one statement more); memory → prompt 442 items / 85 entities / 27 wordings (alt has one statement fewer); named → prompt 435 items / 85 entities / 27 wordings (filler moved); named → prompt 434 items / 85 entities / 27 wordings (alt has one statement more); named → prompt 442 items / 85 entities / 27 wordings (alt has one statement fewer) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = 5% [3, 7]   Baseline: none = 72% [67, 76], identity = 5% [3, 8], value = 17% [13, 21]   Control: 'same' changed = 0% [0, 1]; random push of the same size changed (max over transit layers) = 0% [0, 1]; another domain's prompt changed = 11% [8, 14]
Figures: results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/by_layer_e5-off.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/by_layer_e5more.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/by_layer_e5fewer.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/slots_final_e5-off.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/slots_last_e5-off.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/windows_e5-off.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/domains_final_e5-off.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/domains_last_e5-off.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/domains_last_e5more.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/domains_last_e5fewer.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/levels_final.png, results/pointer_swap/d3v4x_swap_main/analysis-20261021-202317-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v4x_swap_main/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=435); position should be 21, identity 23, value 74, none 312
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 1] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 1]; among alt prompt reads won by a predicted digit, 869/41865 have the runner-up prediction within p 0.1; hook checks self no-op 2622/2622, layer-0 reproduction 2622/2622.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "mixed", "body": "none", "countries": "value"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-off: **alt prompt's own answer (H-value)** (answer org kept 72% [67, 76], answer of bridge alt's statement 5% [3, 8], answer at the same statement slot 5% [3, 7], the alt prompt's own answer 17% [13, 21]); e5more: **alt prompt's own answer (H-value)** (answer org kept 70% [65, 74], answer of bridge alt's statement 6% [4, 9], answer at the same statement slot 5% [3, 7], the alt prompt's own answer 18% [15, 22]); e5fewer: **alt prompt's own answer (H-value)** (answer org kept 73% [68, 77], answer of bridge alt's statement 3% [1, 5], answer at the same statement slot 7% [5, 10], the alt prompt's own answer 15% [12, 19])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-off | - | - | - |
| memory → prompt | question words | e5more | - | - | - |
| memory → prompt | question words | e5fewer | - | - | - |
| memory → prompt | everything after the question | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 90%, answer of bridge alt's statement 9%) | alt prompt's own answer (H-value) (answer org kept 72%, the alt prompt's own answer 17%) |
| memory → prompt | everything after the question | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 91%, answer of bridge alt's statement 8%) | alt prompt's own answer (H-value) (answer org kept 70%, the alt prompt's own answer 18%) |
| memory → prompt | everything after the question | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 93%, answer of bridge alt's statement 6%) | alt prompt's own answer (H-value) (answer org kept 73%, the alt prompt's own answer 15%) |
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 23%, the alt prompt's own answer 62%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 17%, the alt prompt's own answer 68%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 22%, the alt prompt's own answer 56%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 23%, the alt prompt's own answer 55%) |
| named → prompt | everything after the question | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 19%, the alt prompt's own answer 65%) |
| named → prompt | everything after the question | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 24%, the alt prompt's own answer 53%) |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 75%, the alt prompt's own answer 17%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 72%, the alt prompt's own answer 21%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 76%, the alt prompt's own answer 17%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5-off | 435 | 435 | alt prompt's own answer (H-value) | yes | answer org kept 72% [67, 76], answer of bridge alt's statement 5% [3, 8], answer at the same statement slot 5% [3, 7], the alt prompt's own answer 17% [13, 21] |
| domain:animals | e5-off | 146 | 146 | mixed | yes | answer org kept 71% [62, 79], answer of bridge alt's statement 8% [4, 14], answer at the same statement slot 4% [1, 9], the alt prompt's own answer 16% [10, 23] |
| domain:body | e5-off | 139 | 139 | no effect | yes | answer org kept 81% [74, 88], answer of bridge alt's statement 6% [2, 11], answer at the same statement slot 6% [2, 11], the alt prompt's own answer 5% [2, 10] |
| domain:countries | e5-off | 150 | 150 | alt prompt's own answer (H-value) | yes | answer org kept 64% [55, 73], answer of bridge alt's statement 2% [0, 6], answer at the same statement slot 5% [2, 9], the alt prompt's own answer 29% [21, 38] |
| slot:first | e5-off | 146 | 146 | mixed | yes | answer org kept 73% [65, 80], answer of bridge alt's statement 12% [6, 18], answer at the same statement slot 1% [0, 5], the alt prompt's own answer 13% [8, 19] |
| slot:middle | e5-off | 144 | 144 | no effect | yes | answer org kept 78% [71, 86], answer of bridge alt's statement 1% [0, 5], answer at the same statement slot 3% [1, 8], the alt prompt's own answer 15% [9, 21] |
| slot:last | e5-off | 145 | 145 | alt prompt's own answer (H-value) | yes | answer org kept 64% [56, 72], answer of bridge alt's statement 3% [1, 7], answer at the same statement slot 10% [5, 16], the alt prompt's own answer 23% [17, 31] |
| all | e5more | 434 | 434 | alt prompt's own answer (H-value) | yes | answer org kept 70% [65, 74], answer of bridge alt's statement 6% [4, 9], answer at the same statement slot 5% [3, 7], the alt prompt's own answer 18% [15, 22] |
| domain:animals | e5more | 148 | 148 | mixed | yes | answer org kept 69% [60, 78], answer of bridge alt's statement 8% [3, 14], answer at the same statement slot 4% [1, 9], the alt prompt's own answer 18% [11, 24] |
| domain:body | e5more | 138 | 138 | no effect | yes | answer org kept 83% [76, 89], answer of bridge alt's statement 9% [3, 15], answer at the same statement slot 4% [2, 9], the alt prompt's own answer 3% [1, 7] |
| domain:countries | e5more | 148 | 148 | alt prompt's own answer (H-value) | yes | answer org kept 58% [50, 66], answer of bridge alt's statement 3% [1, 7], answer at the same statement slot 6% [3, 11], the alt prompt's own answer 32% [25, 40] |
| slot:first | e5more | 144 | 144 | no effect | yes | answer org kept 74% [66, 80], answer of bridge alt's statement 9% [5, 15], answer at the same statement slot 1% [0, 4], the alt prompt's own answer 16% [10, 23] |
| slot:middle | e5more | 144 | 144 | alt prompt's own answer (H-value) | yes | answer org kept 67% [59, 75], answer of bridge alt's statement 5% [1, 10], answer at the same statement slot 7% [3, 12], the alt prompt's own answer 19% [13, 26] |
| slot:last | e5more | 146 | 146 | alt prompt's own answer (H-value) | yes | answer org kept 68% [61, 76], answer of bridge alt's statement 5% [2, 10], answer at the same statement slot 7% [3, 12], the alt prompt's own answer 19% [13, 26] |
| all | e5fewer | 442 | 442 | alt prompt's own answer (H-value) | yes | answer org kept 73% [68, 77], answer of bridge alt's statement 3% [1, 5], answer at the same statement slot 7% [5, 10], the alt prompt's own answer 15% [12, 19] |
| domain:animals | e5fewer | 147 | 147 | mixed | yes | answer org kept 72% [64, 79], answer of bridge alt's statement 2% [0, 6], answer at the same statement slot 6% [3, 11], the alt prompt's own answer 16% [10, 22] |
| domain:body | e5fewer | 145 | 145 | no effect | yes | answer org kept 83% [76, 90], answer of bridge alt's statement 6% [2, 11], answer at the same statement slot 4% [2, 9], the alt prompt's own answer 5% [2, 10] |
| domain:countries | e5fewer | 150 | 150 | alt prompt's own answer (H-value) | yes | answer org kept 63% [54, 71], answer of bridge alt's statement 1% [0, 4], answer at the same statement slot 10% [5, 16], the alt prompt's own answer 25% [19, 33] |
| slot:first | e5fewer | 147 | 147 | no effect | yes | answer org kept 74% [67, 81], answer of bridge alt's statement 5% [2, 10], answer at the same statement slot 2% [0, 6], the alt prompt's own answer 16% [11, 22] |
| slot:middle | e5fewer | 148 | 148 | no effect | yes | answer org kept 76% [68, 82], answer of bridge alt's statement 1% [0, 4], answer at the same statement slot 8% [4, 14], the alt prompt's own answer 14% [9, 21] |
| slot:last | e5fewer | 147 | 147 | mixed | yes | answer org kept 68% [60, 76], answer of bridge alt's statement 3% [1, 7], answer at the same statement slot 10% [5, 16], the alt prompt's own answer 16% [11, 23] |

## Checks

`{"self_noop": {"n": 2622, "same_top": 2622, "max_abs_dlogit_max": 0.9531}, "layer0_all_reproduces_source": {"n": 2622, "same_top": 2622, "max_abs_dlogit_max": 2.2188}, "unedited_base_answer_read": {"n": 2622, "base_answer": 2622}}`; near ties: `{"n": 41865, "within_gap": 869, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | everything after the question | 50 | 34% [29, 39] | 66% [61, 71] | 11% [9, 15] | 16% [13, 20] | 0% [0, 1] |
| memory → prompt | e5-off | last two tokens before the answer | 50 | 79% [75, 83] | 21% [17, 25] | 26% [22, 30] | 39% [34, 43] | 0% [0, 1] |
| memory → prompt | e5more | everything after the question | 50 | 31% [26, 35] | 69% [65, 74] | 13% [10, 16] | 12% [9, 16] | 0% [0, 1] |
| memory → prompt | e5more | last two tokens before the answer | 52 | 83% [79, 86] | 17% [14, 21] | 5% [3, 8] | 8% [5, 10] | 68% [64, 73] |
| memory → prompt | e5fewer | everything after the question | 48 | 30% [25, 35] | 70% [65, 75] | 6% [4, 9] | 16% [12, 20] | 0% [0, 1] |
| memory → prompt | e5fewer | last two tokens before the answer | 50 | 82% [78, 85] | 18% [15, 22] | 15% [12, 19] | 39% [34, 43] | 0% [0, 1] |
| named → prompt | e5-off | everything after the question | 50 | 74% [70, 78] | 26% [22, 30] | 24% [20, 28] | 37% [33, 42] | 0% [0, 1] |
| named → prompt | e5-off | last two tokens before the answer | 50 | 46% [42, 51] | 54% [49, 58] | 16% [13, 20] | 23% [20, 28] | 0% [0, 1] |
| named → prompt | e5more | everything after the question | 50 | 73% [68, 77] | 27% [23, 32] | 25% [21, 30] | 30% [25, 34] | 0% [0, 1] |
| named → prompt | e5more | last two tokens before the answer | 50 | 47% [42, 52] | 53% [48, 58] | 17% [14, 21] | 20% [16, 24] | 0% [0, 1] |
| named → prompt | e5fewer | everything after the question | 50 | 77% [73, 81] | 23% [19, 27] | 10% [7, 13] | 40% [36, 45] | 0% [0, 1] |
| named → prompt | e5fewer | last two tokens before the answer | 50 | 43% [39, 48] | 57% [52, 61] | 7% [5, 10] | 24% [20, 28] | 0% [0, 1] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 48 and 50

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **holds**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 48 | all | 435 | 85 | 13% [10, 17] | token 2% [1, 4] | yes |
| filler moved | 48 | domain:countries | 150 | 36 | 6% [3, 11] | token 1% [0, 5] | no |
| filler moved | 48 | domain:animals | 146 | 34 | 14% [9, 21] | token 1% [0, 5] | yes |
| filler moved | 48 | domain:body | 139 | 15 | 20% [12, 29] | token 3% [1, 7] | yes |
| filler moved | 50 | all | 435 | 85 | 39% [34, 43] | token 9% [7, 13] | yes |
| filler moved | 50 | domain:countries | 150 | 36 | 37% [29, 45] | token 11% [7, 17] | yes |
| filler moved | 50 | domain:animals | 146 | 34 | 39% [30, 48] | token 8% [3, 13] | yes |
| filler moved | 50 | domain:body | 139 | 15 | 40% [32, 49] | token 9% [5, 15] | yes |
| alt has one statement more | 48 | all | 434 | 85 | 10% [7, 13] | end 2% [1, 4]; token 1% [0, 3] | yes |
| alt has one statement more | 48 | domain:countries | 148 | 36 | 4% [1, 9] | end 2% [0, 6]; token 1% [0, 4] | no |
| alt has one statement more | 48 | domain:animals | 148 | 34 | 9% [5, 15] | end 3% [1, 7]; token 2% [0, 6] | no |
| alt has one statement more | 48 | domain:body | 138 | 15 | 17% [10, 26] | end 1% [0, 5]; token 1% [0, 5] | yes |
| alt has one statement more | 50 | all | 434 | 85 | 31% [27, 36] | end 10% [7, 13]; token 9% [6, 12] | yes |
| alt has one statement more | 50 | domain:countries | 148 | 36 | 33% [25, 41] | end 8% [5, 14]; token 9% [5, 15] | yes |
| alt has one statement more | 50 | domain:animals | 148 | 34 | 28% [21, 36] | end 13% [7, 19]; token 9% [4, 16] | yes |
| alt has one statement more | 50 | domain:body | 138 | 15 | 33% [23, 42] | end 8% [4, 14]; token 7% [4, 13] | yes |
| alt has one statement fewer | 48 | all | 442 | 85 | 9% [6, 12] | end 2% [1, 4]; token 3% [1, 5] | yes |
| alt has one statement fewer | 48 | domain:countries | 150 | 36 | 6% [3, 11] | end 0% [0, 2]; token 2% [0, 6] | no |
| alt has one statement fewer | 48 | domain:animals | 147 | 34 | 13% [7, 19] | end 2% [0, 6]; token 3% [1, 8] | no |
| alt has one statement fewer | 48 | domain:body | 145 | 15 | 8% [5, 14] | end 4% [1, 9]; token 3% [1, 8] | no |
| alt has one statement fewer | 50 | all | 442 | 85 | 39% [34, 43] | end 12% [9, 15]; token 16% [13, 20] | yes |
| alt has one statement fewer | 50 | domain:countries | 150 | 36 | 47% [40, 55] | end 11% [7, 17]; token 13% [8, 19] | yes |
| alt has one statement fewer | 50 | domain:animals | 147 | 34 | 33% [25, 41] | end 11% [5, 17]; token 21% [14, 29] | no |
| alt has one statement fewer | 50 | domain:body | 145 | 15 | 36% [29, 44] | end 14% [9, 20]; token 15% [9, 22] | yes |

## Agent priors in the job spec (jobs/d3/d3v4x_swap_main.yaml `hypotheses`) vs results

- H-order-v4: filler moved: the order slot's lower bound exceeds the same-token-answer at the same statement slot's upper bound at layer 48 or 50, pooled and in >= 2 of 3 topics (pointer_v2 on 22 entities, last two tokens, layer 50: order 28% [23, 33] vs token answer at the same statement slot 16% [12, 20], d3v2_offset_reflexive_main, UNVERIFIED)
- H-start-v4: one more and one fewer: the slot from the start's lower bound exceeds the upper bounds of the slot from the end and of the same token answer at the same statement slot at layer 48 or 50, pooled and in >= 2 of 3 topics, in both alt types
- H-text-position: the same token answer at the same statement slot beats order (filler moved) or both rivals beat the start: the pointer is an address in the token sequence
- prior: Coordinator's priors: H-order-v4 0.6, H-start-v4 0.55.

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 5% [3, 7], last two tokens 9% [6, 12] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 13% [10, 16] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 5% [3, 8] / 5% [3, 7] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 17% [13, 21] / 62% [57, 67] (>= 50%: met); first single layer where it reaches 20%: after the question None, last two tokens 52
- H-none: memory → prompt, answer changed after the question 28% [24, 33] (< 20%: not met)

## Worked example (from examples.json)

Item `body-RL-e5-off-0081` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The eyebrow chart is in folder 3. The forehead chart is in folder 4. The ankle chart is in folder 0. The skull chart is in folder 9. The wind picked up late in the evening. The tongue chart is in folder 5.
What folder keeps the chart on the body part joining foot and leg? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The wind picked up late in the evening. The skull chart is in folder 6. The forehead chart is in folder 8. The eyebrow chart is in folder 3. The tongue chart is in folder 7. The ankle chart is in folder 5.
What folder keeps the chart on the body part that protects the brain? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 0; after the patch 3. Predicted: answer org kept 0 (p 0.070); answer of bridge alt's statement 9 (p 0.007); answer at the same statement slot 3 (p 0.514); answer at the same token position 4 (p 0.189); the alt prompt's own answer 6 (p 0.189).

