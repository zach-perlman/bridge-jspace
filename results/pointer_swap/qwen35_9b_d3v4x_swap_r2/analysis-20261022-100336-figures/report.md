# D3 v4x on Qwen3.5-9B: does the address count statements by order and from the start (filler ...

Run `qwen35_9b_d3v4x_swap_r2` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP qwen35_9b_d3v4x_swap_r2 @ unknown | model Qwen3.5-9B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/by_layer_e5-off.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/by_layer_e5more.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/by_layer_e5fewer.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/slots_final_e5-off.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/slots_last_e5-off.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/windows_e5-off.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/domains_final_e5-off.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/domains_last_e5-off.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/domains_last_e5more.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/domains_last_e5fewer.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/levels_final.png, results/pointer_swap/qwen35_9b_d3v4x_swap_r2/analysis-20261022-100336-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/qwen35_9b_d3v4x_swap_r2/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 1308/26315 have the runner-up prediction within p 0.1; hook checks self no-op 2404/2404, layer-0 reproduction 2401/2404.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-off: **no data** (-); e5more: **no data** (-); e5fewer: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-off | - | - | - |
| memory → prompt | question words | e5more | - | - | - |
| memory → prompt | question words | e5fewer | - | - | - |
| memory → prompt | everything after the question | e5-off | - | - | - |
| memory → prompt | everything after the question | e5more | - | - | - |
| memory → prompt | everything after the question | e5fewer | - | - | - |
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 20%, answer of bridge alt's statement 32%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 93%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 19%, answer of bridge alt's statement 37%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 95%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 21%, answer of bridge alt's statement 29%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 94%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | - | - | - |
| named → prompt | everything after the question | e5more | - | - | - |
| named → prompt | everything after the question | e5fewer | - | - | - |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 40%, answer at the same statement slot 25%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 99%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 35%, answer of bridge alt's statement 25%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 99%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 45%, answer at the same statement slot 27%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 98%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 2404, "same_top": 2404, "max_abs_dlogit_max": 0.9688}, "layer0_all_reproduces_source": {"n": 2404, "same_top": 2401, "max_abs_dlogit_max": 0.8016}, "unedited_base_answer_read": {"n": 2404, "base_answer": 2404}}`; near ties: `{"n": 26315, "within_gap": 1308, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 99% [98, 100] |
| memory → prompt | e5more | last two tokens before the answer | 28 | 99% [98, 100] | 1% [0, 2] | 0% [0, 1] | 0% [0, 1] | 99% [97, 100] |
| memory → prompt | e5fewer | last two tokens before the answer | 28 | 100% [98, 100] | 0% [0, 2] | 0% [0, 1] | 0% [0, 1] | 99% [97, 100] |
| named → prompt | e5-off | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5more | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5fewer | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 14 and 16 and 18 and 20 and 22 and 24 and 26 and 28

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **does not hold**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 14 | all | 406 | 85 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 14 | domain:countries | 148 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 14 | domain:animals | 131 | 34 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 14 | domain:body | 127 | 15 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 16 | all | 406 | 85 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 16 | domain:countries | 148 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 16 | domain:animals | 131 | 34 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 16 | domain:body | 127 | 15 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 18 | all | 406 | 85 | 22% [18, 26] | token 5% [3, 8] | yes |
| filler moved | 18 | domain:countries | 148 | 36 | 34% [26, 42] | token 5% [2, 10] | yes |
| filler moved | 18 | domain:animals | 131 | 34 | 21% [14, 29] | token 4% [1, 9] | yes |
| filler moved | 18 | domain:body | 127 | 15 | 9% [5, 16] | token 7% [4, 13] | no |
| filler moved | 20 | all | 406 | 85 | 28% [23, 32] | token 6% [4, 8] | yes |
| filler moved | 20 | domain:countries | 148 | 36 | 26% [20, 34] | token 6% [3, 11] | yes |
| filler moved | 20 | domain:animals | 131 | 34 | 29% [21, 37] | token 6% [2, 12] | yes |
| filler moved | 20 | domain:body | 127 | 15 | 28% [20, 37] | token 5% [2, 10] | yes |
| filler moved | 22 | all | 406 | 85 | 29% [24, 34] | token 8% [5, 11] | yes |
| filler moved | 22 | domain:countries | 148 | 36 | 28% [21, 36] | token 7% [4, 13] | yes |
| filler moved | 22 | domain:animals | 131 | 34 | 32% [23, 41] | token 8% [3, 16] | yes |
| filler moved | 22 | domain:body | 127 | 15 | 27% [18, 36] | token 8% [4, 14] | yes |
| filler moved | 24 | all | 406 | 85 | 1% [0, 3] | token 0% [0, 2] | no |
| filler moved | 24 | domain:countries | 148 | 36 | 1% [0, 4] | token 0% [0, 3] | no |
| filler moved | 24 | domain:animals | 131 | 34 | 1% [0, 4] | token 0% [0, 3] | no |
| filler moved | 24 | domain:body | 127 | 15 | 2% [0, 6] | token 2% [0, 6] | no |
| filler moved | 26 | all | 406 | 85 | 1% [0, 3] | token 0% [0, 2] | no |
| filler moved | 26 | domain:countries | 148 | 36 | 1% [0, 4] | token 0% [0, 3] | no |
| filler moved | 26 | domain:animals | 131 | 34 | 1% [0, 4] | token 0% [0, 3] | no |
| filler moved | 26 | domain:body | 127 | 15 | 2% [0, 6] | token 2% [0, 6] | no |
| filler moved | 28 | all | 406 | 85 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 28 | domain:countries | 148 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 28 | domain:animals | 131 | 34 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 28 | domain:body | 127 | 15 | 1% [0, 4] | token 0% [0, 3] | no |
| alt has one statement more | 14 | all | 391 | 83 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 14 | domain:countries | 144 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 14 | domain:animals | 126 | 32 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 14 | domain:body | 121 | 15 | 0% [0, 3] | end 1% [0, 5]; token 0% [0, 3] | no |
| alt has one statement more | 16 | all | 391 | 83 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 16 | domain:countries | 144 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 16 | domain:animals | 126 | 32 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 16 | domain:body | 121 | 15 | 0% [0, 3] | end 1% [0, 5]; token 0% [0, 3] | no |
| alt has one statement more | 18 | all | 391 | 83 | 14% [11, 18] | end 7% [4, 10]; token 7% [4, 10] | yes |
| alt has one statement more | 18 | domain:countries | 144 | 36 | 24% [17, 31] | end 9% [4, 15]; token 6% [2, 11] | yes |
| alt has one statement more | 18 | domain:animals | 126 | 32 | 9% [5, 15] | end 6% [2, 11]; token 8% [3, 14] | no |
| alt has one statement more | 18 | domain:body | 121 | 15 | 8% [5, 15] | end 5% [2, 10]; token 7% [3, 13] | no |
| alt has one statement more | 20 | all | 391 | 83 | 14% [11, 18] | end 8% [5, 11]; token 5% [3, 7] | yes |
| alt has one statement more | 20 | domain:countries | 144 | 36 | 16% [11, 23] | end 7% [3, 12]; token 1% [0, 4] | no |
| alt has one statement more | 20 | domain:animals | 126 | 32 | 13% [7, 20] | end 8% [3, 14]; token 9% [5, 15] | no |
| alt has one statement more | 20 | domain:body | 121 | 15 | 13% [8, 20] | end 8% [3, 15]; token 6% [2, 12] | no |
| alt has one statement more | 22 | all | 391 | 83 | 15% [12, 19] | end 8% [6, 12]; token 6% [3, 8] | yes |
| alt has one statement more | 22 | domain:countries | 144 | 36 | 15% [10, 22] | end 8% [4, 13]; token 1% [0, 4] | no |
| alt has one statement more | 22 | domain:animals | 126 | 32 | 16% [9, 23] | end 10% [5, 17]; token 10% [5, 17] | no |
| alt has one statement more | 22 | domain:body | 121 | 15 | 15% [9, 22] | end 7% [3, 14]; token 7% [2, 13] | no |
| alt has one statement more | 24 | all | 391 | 83 | 1% [0, 2] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 24 | domain:countries | 144 | 36 | 1% [0, 4] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 24 | domain:animals | 126 | 32 | 0% [-0, 3] | end 0% [-0, 3]; token 1% [0, 4] | no |
| alt has one statement more | 24 | domain:body | 121 | 15 | 1% [0, 5] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 26 | all | 391 | 83 | 1% [0, 2] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 26 | domain:countries | 144 | 36 | 1% [0, 4] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 26 | domain:animals | 126 | 32 | 0% [-0, 3] | end 0% [-0, 3]; token 1% [0, 4] | no |
| alt has one statement more | 26 | domain:body | 121 | 15 | 1% [0, 5] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 28 | all | 391 | 83 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 28 | domain:countries | 144 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 28 | domain:animals | 126 | 32 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 28 | domain:body | 121 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 14 | all | 405 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 14 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 14 | domain:animals | 130 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 14 | domain:body | 125 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 16 | all | 405 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 16 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 16 | domain:animals | 130 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 16 | domain:body | 125 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 18 | all | 405 | 85 | 23% [19, 28] | end 10% [7, 14]; token 8% [5, 11] | yes |
| alt has one statement fewer | 18 | domain:countries | 150 | 36 | 39% [30, 48] | end 12% [7, 18]; token 7% [3, 13] | yes |
| alt has one statement fewer | 18 | domain:animals | 130 | 34 | 16% [10, 23] | end 9% [5, 15]; token 12% [7, 18] | no |
| alt has one statement fewer | 18 | domain:body | 125 | 15 | 12% [7, 19] | end 9% [3, 17]; token 4% [1, 9] | no |
| alt has one statement fewer | 20 | all | 405 | 85 | 28% [24, 32] | end 9% [6, 12]; token 8% [6, 11] | yes |
| alt has one statement fewer | 20 | domain:countries | 150 | 36 | 38% [30, 46] | end 6% [3, 11]; token 7% [3, 12] | yes |
| alt has one statement fewer | 20 | domain:animals | 130 | 34 | 20% [13, 28] | end 10% [6, 16]; token 13% [7, 20] | no |
| alt has one statement fewer | 20 | domain:body | 125 | 15 | 24% [17, 32] | end 11% [6, 18]; token 5% [2, 10] | no |
| alt has one statement fewer | 22 | all | 405 | 85 | 29% [25, 34] | end 10% [7, 13]; token 9% [7, 13] | yes |
| alt has one statement fewer | 22 | domain:countries | 150 | 36 | 39% [31, 47] | end 7% [4, 13]; token 7% [3, 13] | yes |
| alt has one statement fewer | 22 | domain:animals | 130 | 34 | 25% [17, 34] | end 10% [5, 16]; token 15% [9, 22] | no |
| alt has one statement fewer | 22 | domain:body | 125 | 15 | 22% [15, 30] | end 13% [8, 20]; token 6% [3, 12] | no |
| alt has one statement fewer | 24 | all | 405 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 24 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 24 | domain:animals | 130 | 34 | 1% [0, 4] | end 1% [0, 4]; token 1% [0, 4] | no |
| alt has one statement fewer | 24 | domain:body | 125 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 26 | all | 405 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 26 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 26 | domain:animals | 130 | 34 | 1% [0, 4] | end 1% [0, 4]; token 1% [0, 4] | no |
| alt has one statement fewer | 26 | domain:body | 125 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 28 | all | 405 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 28 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 28 | domain:animals | 130 | 34 | 1% [0, 4] | end 1% [0, 4]; token 0% [0, 3] | no |
| alt has one statement fewer | 28 | domain:body | 125 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |

## Agent priors in the job spec (jobs/d3/qwen35_9b_d3v4x_swap_r2.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v4x tests (H-order-v4, H-start-v4) come out as on Qwen3.6-27B. Prior 0.4

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 1% [0, 3] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 93% [90, 95] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 24
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e5fewer-0067` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 22 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The town hall bell rang twice today. Drawer 3 holds the Philippines file. Drawer 0 holds the Turkey file. Drawer 1 holds the Pakistan file. Drawer 8 holds the Iraq file. Drawer 2 holds the Norway file.
In which drawer is the file on the country whose capital is Ankara? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
Drawer 3 holds the Pakistan file. Drawer 1 holds the Iraq file. Drawer 2 holds the Norway file. Drawer 7 holds the Philippines file. The town hall bell rang twice today. The film at the cinema started late.
In which drawer is the file on the country whose capital is Manila? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 0; after the patch 8. Predicted: answer org kept 0 (p 0.051); answer of bridge alt's statement 3 (p 0.017); answer at the same statement slot 8 (p 0.804); answer at the same slot counted from the end 2 (p 0.007); answer at the same token position 1 (p 0.017); the alt prompt's own answer 7 (p 0.031).

