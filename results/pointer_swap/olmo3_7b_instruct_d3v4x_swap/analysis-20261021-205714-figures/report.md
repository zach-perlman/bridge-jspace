# D3 v4x on OLMo-3-7B-Instruct: does its last-token pointer also count statements by order, from the start?

Run `olmo3_7b_instruct_d3v4x_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo3_7b_instruct_d3v4x_swap @ unknown | model Olmo-3-7B-Instruct (chat format) | n per family = memory → prompt 202 items / 71 entities / 27 wordings (filler moved); memory → prompt 190 items / 67 entities / 27 wordings (alt has one statement more); memory → prompt 216 items / 74 entities / 26 wordings (alt has one statement fewer); named → prompt 202 items / 71 entities / 27 wordings (filler moved); named → prompt 190 items / 67 entities / 27 wordings (alt has one statement more); named → prompt 216 items / 74 entities / 26 wordings (alt has one statement fewer) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = 0% [-0, 2]   Baseline: none = 100% [97, 100], identity = 0% [-0, 2], value = 0% [0, 3]   Control: 'same' changed = 0% [-0, 2]; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/by_layer_e5-off.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/by_layer_e5more.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/by_layer_e5fewer.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/slots_final_e5-off.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/slots_last_e5-off.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/windows_e5-off.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/domains_final_e5-off.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/domains_last_e5-off.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/domains_last_e5more.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/domains_last_e5fewer.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/levels_final.png, results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/analysis-20261021-205714-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo3_7b_instruct_d3v4x_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=202); position should be 0, identity 0, value 1, none 201
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win 0% [-0, 2]; among alt prompt reads won by a predicted digit, 278/21663 have the runner-up prediction within p 0.1; hook checks self no-op 1216/1216, layer-0 reproduction 1214/1216.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "none", "body": "damage", "countries": "none"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-off: **no effect** (answer org kept 100% [97, 100], answer of bridge alt's statement 0% [-0, 2], answer at the same statement slot 0% [-0, 2], the alt prompt's own answer 0% [0, 3]); e5more: **no effect** (answer org kept 99% [96, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 1% [0, 3]); e5fewer: **no effect** (answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 3])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 72, in cuts ['domain:body'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-off | - | - | - |
| memory → prompt | question words | e5more | - | - | - |
| memory → prompt | question words | e5fewer | - | - | - |
| memory → prompt | everything after the question | e5-off | no effect (answer org kept 99%, answer of bridge alt's statement 1%) | no effect (answer org kept 94%, answer of bridge alt's statement 2%) | no effect (answer org kept 100%, the alt prompt's own answer 0%) |
| memory → prompt | everything after the question | e5more | no effect (answer org kept 99%, answer at the same statement slot 1%) | no effect (answer org kept 95%, answer of bridge alt's statement 3%) | no effect (answer org kept 99%, the alt prompt's own answer 1%) |
| memory → prompt | everything after the question | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer of bridge alt's statement 3%) | no effect (answer org kept 100%, the alt prompt's own answer 0%) |
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 94%, answer of bridge alt's statement 3%) | mixed (answer org kept 10%, the alt prompt's own answer 29%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 94%, answer of bridge alt's statement 3%) | mixed (answer org kept 11%, the alt prompt's own answer 32%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 92%, answer of bridge alt's statement 5%) | mixed (answer org kept 5%, the alt prompt's own answer 29%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 99%, answer of bridge alt's statement 1%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 84%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 88%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 76%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5-off | 202 | 202 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [-0, 2], answer at the same statement slot 0% [-0, 2], the alt prompt's own answer 0% [0, 3] |
| domain:animals | e5-off | 79 | 79 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [-0, 5], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| domain:body | e5-off | 33 | 33 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 97% [85, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 3% [0, 15] |
| domain:countries | e5-off | 90 | 90 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:first | e5-off | 53 | 53 | no effect | yes | answer org kept 98% [90, 100], answer of bridge alt's statement 0% [-0, 7], answer at the same statement slot 0% [-0, 7], the alt prompt's own answer 2% [0, 10] |
| slot:middle | e5-off | 71 | 71 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [0, 5], answer at the same statement slot 0% [0, 5], the alt prompt's own answer 0% [0, 5] |
| slot:last | e5-off | 78 | 78 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [0, 5], answer at the same statement slot 0% [0, 5], the alt prompt's own answer 0% [0, 5] |
| all | e5more | 190 | 190 | no effect | yes | answer org kept 99% [96, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 1% [0, 3] |
| domain:animals | e5more | 59 | 59 | no effect | yes | answer org kept 100% [94, 100], answer of bridge alt's statement 0% [0, 6], answer at the same statement slot 0% [0, 6], the alt prompt's own answer 0% [0, 6] |
| domain:body | e5more | 41 | 41 | no effect | yes | answer org kept 95% [84, 100], answer of bridge alt's statement 0% [0, 9], answer at the same statement slot 0% [0, 9], the alt prompt's own answer 2% [0, 13] |
| domain:countries | e5more | 90 | 90 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:first | e5more | 60 | 60 | no effect | yes | answer org kept 98% [91, 100], answer of bridge alt's statement 0% [-0, 6], answer at the same statement slot 0% [-0, 6], the alt prompt's own answer 0% [-0, 6] |
| slot:middle | e5more | 54 | 54 | no effect | yes | answer org kept 98% [90, 100], answer of bridge alt's statement 0% [0, 7], answer at the same statement slot 0% [0, 7], the alt prompt's own answer 2% [0, 10] |
| slot:last | e5more | 76 | 76 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [0, 5], answer at the same statement slot 0% [0, 5], the alt prompt's own answer 0% [0, 5] |
| all | e5fewer | 216 | 216 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 3] |
| domain:animals | e5fewer | 84 | 84 | no effect | yes | answer org kept 99% [94, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 1% [0, 6] |
| domain:body | e5fewer | 34 | 34 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |
| domain:countries | e5fewer | 98 | 98 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:first | e5fewer | 68 | 68 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [0, 5], answer at the same statement slot 0% [0, 5], the alt prompt's own answer 0% [0, 5] |
| slot:middle | e5fewer | 57 | 57 | no effect | yes | answer org kept 98% [91, 100], answer of bridge alt's statement 0% [0, 6], answer at the same statement slot 0% [0, 6], the alt prompt's own answer 2% [0, 9] |
| slot:last | e5fewer | 91 | 91 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |

## Checks

`{"self_noop": {"n": 1216, "same_top": 1216, "max_abs_dlogit_max": 0.3125}, "layer0_all_reproduces_source": {"n": 1216, "same_top": 1214, "max_abs_dlogit_max": 0.9062}, "unedited_base_answer_read": {"n": 1216, "base_answer": 1216}}`; near ties: `{"n": 21663, "within_gap": 278, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | everything after the question | 17 | 4% [2, 8] | 96% [92, 98] | 1% [0, 4] | 1% [0, 4] | 0% [-0, 2] |
| memory → prompt | e5-off | last two tokens before the answer | 21 | 92% [88, 95] | 8% [5, 12] | 18% [13, 24] | 25% [19, 31] | 36% [28, 43] |
| memory → prompt | e5more | everything after the question | 17 | 5% [2, 9] | 95% [91, 98] | 2% [1, 5] | 2% [0, 5] | 0% [0, 2] |
| memory → prompt | e5more | last two tokens before the answer | 21 | 91% [86, 95] | 9% [5, 14] | 18% [13, 25] | 13% [8, 18] | 39% [32, 47] |
| memory → prompt | e5fewer | everything after the question | 17 | 6% [3, 9] | 94% [91, 97] | 3% [1, 6] | 0% [0, 2] | 0% [0, 2] |
| memory → prompt | e5fewer | last two tokens before the answer | 20 | 95% [91, 98] | 5% [2, 9] | 18% [14, 24] | 24% [18, 30] | 29% [24, 36] |
| named → prompt | e5-off | everything after the question | 17 | 0% [0, 3] | 100% [97, 100] | 0% [0, 3] | 0% [-0, 2] | 0% [-0, 2] |
| named → prompt | e5-off | last two tokens before the answer | 21 | 98% [95, 100] | 2% [0, 5] | 2% [0, 5] | 3% [1, 7] | 90% [85, 94] |
| named → prompt | e5more | everything after the question | 16 | 0% [0, 2] | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] |
| named → prompt | e5more | last two tokens before the answer | 21 | 99% [97, 100] | 1% [0, 3] | 2% [0, 5] | 3% [1, 6] | 92% [87, 96] |
| named → prompt | e5fewer | everything after the question | 17 | 0% [0, 3] | 100% [97, 100] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] |
| named → prompt | e5fewer | last two tokens before the answer | 21 | 99% [96, 100] | 1% [0, 4] | 1% [0, 4] | 8% [5, 12] | 83% [78, 88] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 17 and 18 and 19

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **does not hold**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 17 | all | 202 | 71 | 27% [21, 34] | token 10% [6, 15] | yes |
| filler moved | 17 | domain:countries | 90 | 33 | 28% [19, 38] | token 10% [5, 18] | yes |
| filler moved | 17 | domain:animals | 79 | 29 | 33% [23, 44] | token 9% [4, 17] | yes |
| filler moved | 17 | domain:body | 33 | 9 | 12% [0, 29] | token 12% [0, 29] | no (n < 35) |
| filler moved | 18 | all | 202 | 71 | 31% [24, 37] | token 11% [7, 16] | yes |
| filler moved | 18 | domain:countries | 90 | 33 | 28% [20, 38] | token 12% [6, 21] | no |
| filler moved | 18 | domain:animals | 79 | 29 | 38% [27, 49] | token 9% [4, 17] | yes |
| filler moved | 18 | domain:body | 33 | 9 | 21% [10, 38] | token 12% [0, 31] | no (n < 35) |
| filler moved | 19 | all | 202 | 71 | 29% [23, 36] | token 8% [5, 13] | yes |
| filler moved | 19 | domain:countries | 90 | 33 | 26% [16, 36] | token 10% [5, 18] | no |
| filler moved | 19 | domain:animals | 79 | 29 | 33% [24, 44] | token 5% [1, 12] | yes |
| filler moved | 19 | domain:body | 33 | 9 | 30% [17, 47] | token 12% [0, 31] | no (n < 35) |
| alt has one statement more | 17 | all | 190 | 67 | 19% [14, 26] | end 16% [12, 22]; token 9% [5, 14] | no |
| alt has one statement more | 17 | domain:countries | 90 | 31 | 23% [16, 33] | end 13% [7, 22]; token 7% [2, 14] | no |
| alt has one statement more | 17 | domain:animals | 59 | 26 | 15% [6, 27] | end 24% [14, 36]; token 10% [3, 20] | no |
| alt has one statement more | 17 | domain:body | 41 | 10 | 17% [9, 31] | end 12% [3, 26]; token 12% [4, 29] | no |
| alt has one statement more | 18 | all | 190 | 67 | 23% [17, 29] | end 14% [9, 19]; token 12% [7, 17] | no |
| alt has one statement more | 18 | domain:countries | 90 | 31 | 26% [18, 35] | end 9% [4, 17]; token 11% [5, 19] | no |
| alt has one statement more | 18 | domain:animals | 59 | 26 | 22% [12, 34] | end 22% [13, 34]; token 12% [5, 23] | no |
| alt has one statement more | 18 | domain:body | 41 | 10 | 17% [9, 31] | end 12% [3, 26]; token 12% [4, 29] | no |
| alt has one statement more | 19 | all | 190 | 67 | 16% [11, 22] | end 11% [7, 16]; token 7% [4, 12] | no |
| alt has one statement more | 19 | domain:countries | 90 | 31 | 13% [7, 22] | end 8% [3, 15]; token 6% [1, 12] | no |
| alt has one statement more | 19 | domain:animals | 59 | 26 | 14% [5, 25] | end 15% [7, 27]; token 10% [3, 20] | no |
| alt has one statement more | 19 | domain:body | 41 | 10 | 24% [14, 39] | end 12% [5, 26]; token 7% [0, 19] | no |
| alt has one statement fewer | 17 | all | 216 | 74 | 22% [16, 28] | end 15% [10, 20]; token 9% [6, 14] | no |
| alt has one statement fewer | 17 | domain:countries | 98 | 33 | 30% [20, 39] | end 10% [5, 18]; token 9% [4, 17] | yes |
| alt has one statement fewer | 17 | domain:animals | 84 | 31 | 20% [10, 31] | end 20% [12, 30]; token 12% [6, 21] | no |
| alt has one statement fewer | 17 | domain:body | 34 | 10 | 3% [0, 15] | end 15% [4, 30]; token 3% [0, 15] | no (n < 35) |
| alt has one statement fewer | 18 | all | 216 | 74 | 27% [21, 33] | end 17% [12, 22]; token 10% [6, 15] | no |
| alt has one statement fewer | 18 | domain:countries | 98 | 33 | 36% [26, 46] | end 11% [4, 19]; token 9% [4, 17] | yes |
| alt has one statement fewer | 18 | domain:animals | 84 | 31 | 27% [19, 38] | end 21% [13, 31]; token 12% [5, 21] | no |
| alt has one statement fewer | 18 | domain:body | 34 | 10 | 0% [0, 10] | end 21% [10, 37]; token 9% [0, 23] | no (n < 35) |
| alt has one statement fewer | 19 | all | 216 | 74 | 26% [21, 33] | end 13% [9, 19]; token 11% [7, 15] | yes |
| alt has one statement fewer | 19 | domain:countries | 98 | 33 | 30% [21, 39] | end 6% [2, 13]; token 10% [5, 18] | yes |
| alt has one statement fewer | 19 | domain:animals | 84 | 31 | 30% [21, 40] | end 18% [10, 27]; token 11% [5, 19] | no |
| alt has one statement fewer | 19 | domain:body | 34 | 10 | 9% [0, 23] | end 24% [11, 40]; token 12% [4, 27] | no (n < 35) |

## Agent priors in the job spec (jobs/d3/olmo3_7b_instruct_d3v4x_swap.yaml `hypotheses`) vs results

- H-order-olmo: filler moved: the order slot's lower bound exceeds the same-token-answer at the same statement slot's upper bound at layer 17, 18 or 19, pooled and in >= 2 of 3 topics (same layer). Prior 0.45 (Dan: yes, like Qwen)
- H-start-olmo: one more and one fewer: the slot from the start's lower bound exceeds the upper bounds of the slot from the end and of the same token answer at the same statement slot at layer 17, 18 or 19, pooled and in >= 2 of 3 topics, both alt types. Prior 0.4 (Dan: yes, like Qwen)
- H-text-position-olmo: the same token answer at the same statement slot beats order, or the end / token rival beats the start: OLMo's address is a place in the token sequence

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [-0, 2], last two tokens 0% [-0, 2] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 0% [-0, 2] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [-0, 2] / 0% [-0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 0% [0, 3] / 99% [96, 100] (>= 50%: met); first single layer where it reaches 20%: after the question None, last two tokens 19
- H-none: memory → prompt, answer changed after the question 0% [0, 3] (< 20%: met)

## Worked example (from examples.json)

Item `body-RL-e5more-0001` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
Folder 9 holds the stomach chart. Folder 7 holds the elbow chart. Folder 5 holds the bladder chart. The town hall bell rang twice today. Folder 0 holds the tongue chart. Folder 4 holds the ear chart. The clock on the wall was slow.
Which folder holds the chart on the body part that hears sounds? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Alt prompt:

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
Folder 7 holds the stomach chart. The town hall bell rang twice today. Folder 6 holds the tongue chart. Folder 9 holds the ear chart. Folder 5 holds the spine chart. Folder 3 holds the bladder chart. Folder 4 holds the elbow chart.
Which folder holds the chart on the body part that tastes food? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Answers: answer org 4; after the patch 7. Predicted: answer org kept 4 (p 0.001); answer of bridge alt's statement 0 (p 0.022); answer at the same statement slot 7 (p 0.238); answer at the same slot counted from the end 9 (p 0.077); answer at the same token position 5 (p 0.164); the alt prompt's own answer 6 (p 0.186).

