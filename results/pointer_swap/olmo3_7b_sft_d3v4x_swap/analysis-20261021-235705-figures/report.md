# olmo3_7b_sft_d3v4x_swap

Run `olmo3_7b_sft_d3v4x_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo3_7b_sft_d3v4x_swap @ unknown | model Olmo-3-7B-Instruct-SFT (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/by_layer_e5-off.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/by_layer_e5more.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/by_layer_e5fewer.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/slots_final_e5-off.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/slots_last_e5-off.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/windows_e5-off.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/domains_final_e5-off.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/domains_last_e5-off.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/domains_last_e5more.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/domains_last_e5fewer.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/levels_final.png, results/pointer_swap/olmo3_7b_sft_d3v4x_swap/analysis-20261021-235705-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo3_7b_sft_d3v4x_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 788/11824 have the runner-up prediction within p 0.1; hook checks self no-op 1332/1332, layer-0 reproduction 1331/1332.
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
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 90%, answer of bridge alt's statement 4%) | mixed (answer org kept 9%, the alt prompt's own answer 28%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 89%, answer of bridge alt's statement 6%) | mixed (answer org kept 10%, the alt prompt's own answer 31%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 94%, answer of bridge alt's statement 5%) | mixed (answer org kept 8%, the alt prompt's own answer 28%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | - | - | - |
| named → prompt | everything after the question | e5more | - | - | - |
| named → prompt | everything after the question | e5fewer | - | - | - |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 79%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 99%, answer of bridge alt's statement 1%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 83%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 73%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 1332, "same_top": 1332, "max_abs_dlogit_max": 0.2461}, "layer0_all_reproduces_source": {"n": 1332, "same_top": 1331, "max_abs_dlogit_max": 0.375}, "unedited_base_answer_read": {"n": 1332, "base_answer": 1332}}`; near ties: `{"n": 11824, "within_gap": 788, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | last two tokens before the answer | 21 | 94% [90, 97] | 6% [3, 10] | 20% [15, 26] | 23% [18, 29] | 38% [31, 44] |
| memory → prompt | e5more | last two tokens before the answer | 21 | 91% [86, 94] | 9% [6, 14] | 22% [17, 29] | 13% [8, 18] | 39% [32, 46] |
| memory → prompt | e5fewer | last two tokens before the answer | 21 | 94% [90, 97] | 6% [3, 10] | 16% [12, 21] | 18% [13, 23] | 38% [32, 45] |
| named → prompt | e5-off | last two tokens before the answer | 21 | 98% [96, 100] | 2% [0, 4] | 4% [1, 7] | 4% [2, 7] | 87% [82, 91] |
| named → prompt | e5more | last two tokens before the answer | 21 | 98% [95, 100] | 2% [0, 5] | 3% [1, 7] | 2% [0, 5] | 88% [83, 93] |
| named → prompt | e5fewer | last two tokens before the answer | 21 | 98% [96, 100] | 2% [0, 4] | 2% [0, 4] | 8% [5, 13] | 79% [74, 84] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 17 and 18 and 19

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **does not hold**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 17 | all | 224 | 75 | 27% [20, 33] | token 12% [8, 16] | yes |
| filler moved | 17 | domain:countries | 108 | 34 | 30% [20, 40] | token 13% [7, 21] | no |
| filler moved | 17 | domain:animals | 79 | 30 | 28% [17, 39] | token 11% [6, 20] | no |
| filler moved | 17 | domain:body | 37 | 11 | 16% [3, 33] | token 8% [0, 21] | no |
| filler moved | 18 | all | 224 | 75 | 29% [23, 36] | token 14% [10, 19] | yes |
| filler moved | 18 | domain:countries | 108 | 34 | 28% [18, 38] | token 13% [7, 21] | no |
| filler moved | 18 | domain:animals | 79 | 30 | 38% [26, 49] | token 13% [7, 22] | yes |
| filler moved | 18 | domain:body | 37 | 11 | 16% [5, 31] | token 19% [6, 34] | no |
| filler moved | 19 | all | 224 | 75 | 29% [23, 36] | token 8% [5, 13] | yes |
| filler moved | 19 | domain:countries | 108 | 34 | 28% [19, 37] | token 8% [4, 15] | yes |
| filler moved | 19 | domain:animals | 79 | 30 | 34% [24, 45] | token 6% [2, 14] | yes |
| filler moved | 19 | domain:body | 37 | 11 | 24% [13, 40] | token 14% [3, 28] | no |
| alt has one statement more | 17 | all | 205 | 66 | 18% [13, 23] | end 17% [12, 22]; token 9% [6, 13] | no |
| alt has one statement more | 17 | domain:countries | 99 | 32 | 22% [14, 31] | end 13% [7, 21]; token 9% [4, 16] | no |
| alt has one statement more | 17 | domain:animals | 63 | 24 | 14% [5, 25] | end 22% [13, 34]; token 11% [5, 21] | no |
| alt has one statement more | 17 | domain:body | 43 | 10 | 12% [4, 24] | end 16% [7, 30]; token 5% [0, 15] | no |
| alt has one statement more | 18 | all | 205 | 66 | 23% [18, 30] | end 15% [10, 20]; token 12% [8, 17] | no |
| alt has one statement more | 18 | domain:countries | 99 | 32 | 27% [19, 37] | end 11% [6, 19]; token 13% [7, 21] | no |
| alt has one statement more | 18 | domain:animals | 63 | 24 | 19% [10, 30] | end 19% [10, 30]; token 14% [6, 25] | no |
| alt has one statement more | 18 | domain:body | 43 | 10 | 21% [11, 35] | end 16% [7, 30]; token 5% [0, 15] | no |
| alt has one statement more | 19 | all | 205 | 66 | 16% [12, 22] | end 10% [6, 15]; token 6% [3, 10] | no |
| alt has one statement more | 19 | domain:countries | 99 | 32 | 12% [7, 20] | end 8% [4, 15]; token 6% [2, 13] | no |
| alt has one statement more | 19 | domain:animals | 63 | 24 | 19% [8, 32] | end 11% [4, 21]; token 6% [2, 15] | no |
| alt has one statement more | 19 | domain:body | 43 | 10 | 21% [11, 35] | end 14% [5, 27]; token 5% [0, 15] | no |
| alt has one statement fewer | 17 | all | 237 | 74 | 24% [19, 31] | end 14% [9, 18]; token 11% [8, 16] | yes |
| alt has one statement fewer | 17 | domain:countries | 110 | 33 | 30% [22, 39] | end 11% [5, 18]; token 13% [7, 20] | yes |
| alt has one statement fewer | 17 | domain:animals | 87 | 31 | 25% [15, 37] | end 17% [9, 27]; token 13% [5, 21] | no |
| alt has one statement fewer | 17 | domain:body | 40 | 10 | 8% [0, 20] | end 12% [3, 26]; token 5% [0, 16] | no |
| alt has one statement fewer | 18 | all | 237 | 74 | 26% [21, 32] | end 19% [14, 24]; token 13% [9, 18] | no |
| alt has one statement fewer | 18 | domain:countries | 110 | 33 | 32% [23, 41] | end 12% [6, 19]; token 14% [8, 21] | yes |
| alt has one statement fewer | 18 | domain:animals | 87 | 31 | 26% [18, 37] | end 23% [14, 33]; token 15% [9, 24] | no |
| alt has one statement fewer | 18 | domain:body | 40 | 10 | 10% [3, 23] | end 28% [15, 43]; token 8% [0, 20] | no |
| alt has one statement fewer | 19 | all | 237 | 74 | 23% [18, 29] | end 14% [10, 19]; token 12% [9, 17] | no |
| alt has one statement fewer | 19 | domain:countries | 110 | 33 | 23% [14, 32] | end 5% [2, 11]; token 12% [7, 19] | no |
| alt has one statement fewer | 19 | domain:animals | 87 | 31 | 25% [17, 35] | end 21% [12, 30]; token 14% [7, 23] | no |
| alt has one statement fewer | 19 | domain:body | 40 | 10 | 18% [9, 32] | end 22% [12, 38]; token 10% [3, 23] | no |

## Agent priors in the job spec (jobs/d3/olmo3_7b_sft_d3v4x_swap.yaml `hypotheses`) vs results


Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 0% [0, 2] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 0% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 98% [95, 100] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 19
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

