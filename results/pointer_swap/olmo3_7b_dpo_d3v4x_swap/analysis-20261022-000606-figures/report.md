# olmo3_7b_dpo_d3v4x_swap

Run `olmo3_7b_dpo_d3v4x_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo3_7b_dpo_d3v4x_swap @ unknown | model Olmo-3-7B-Instruct-DPO (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/by_layer_e5-off.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/by_layer_e5more.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/by_layer_e5fewer.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/slots_final_e5-off.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/slots_last_e5-off.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/windows_e5-off.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/domains_final_e5-off.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/domains_last_e5-off.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/domains_last_e5more.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/domains_last_e5fewer.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/levels_final.png, results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/analysis-20261022-000606-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo3_7b_dpo_d3v4x_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 215/10842 have the runner-up prediction within p 0.1; hook checks self no-op 1234/1234, layer-0 reproduction 1232/1234.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-off: **no data** (-); e5more: **no data** (-); e5fewer: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 36, in cuts ['domain:body'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-off | - | - | - |
| memory → prompt | question words | e5more | - | - | - |
| memory → prompt | question words | e5fewer | - | - | - |
| memory → prompt | everything after the question | e5-off | - | - | - |
| memory → prompt | everything after the question | e5more | - | - | - |
| memory → prompt | everything after the question | e5fewer | - | - | - |
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 92%, answer of bridge alt's statement 3%) | mixed (answer org kept 8%, the alt prompt's own answer 32%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 92%, answer of bridge alt's statement 4%) | alt prompt's own answer (H-value) (answer org kept 8%, the alt prompt's own answer 35%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 93%, answer of bridge alt's statement 4%) | mixed (answer org kept 4%, the alt prompt's own answer 33%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | - | - | - |
| named → prompt | everything after the question | e5more | - | - | - |
| named → prompt | everything after the question | e5fewer | - | - | - |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 98%, answer of bridge alt's statement 1%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 83%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 99%, answer of bridge alt's statement 1%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 90%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 77%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 1234, "same_top": 1234, "max_abs_dlogit_max": 0.3906}, "layer0_all_reproduces_source": {"n": 1234, "same_top": 1232, "max_abs_dlogit_max": 1.3125}, "unedited_base_answer_read": {"n": 1234, "base_answer": 1234}}`; near ties: `{"n": 10842, "within_gap": 215, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | last two tokens before the answer | 21 | 94% [90, 97] | 6% [3, 10] | 18% [13, 23] | 22% [16, 28] | 43% [36, 50] |
| memory → prompt | e5more | last two tokens before the answer | 21 | 93% [88, 97] | 7% [3, 12] | 19% [14, 25] | 13% [8, 19] | 43% [36, 50] |
| memory → prompt | e5fewer | last two tokens before the answer | 20 | 96% [92, 98] | 4% [2, 8] | 16% [12, 21] | 23% [18, 29] | 33% [27, 39] |
| named → prompt | e5-off | last two tokens before the answer | 21 | 99% [97, 100] | 1% [0, 3] | 2% [0, 5] | 3% [1, 7] | 90% [85, 95] |
| named → prompt | e5more | last two tokens before the answer | 21 | 99% [96, 100] | 1% [0, 4] | 2% [0, 4] | 3% [1, 7] | 92% [88, 95] |
| named → prompt | e5fewer | last two tokens before the answer | 21 | 99% [97, 100] | 1% [0, 3] | 1% [0, 4] | 7% [4, 11] | 85% [79, 90] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 17 and 18 and 19

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **does not hold**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 17 | all | 210 | 71 | 28% [22, 35] | token 10% [6, 15] | yes |
| filler moved | 17 | domain:countries | 103 | 34 | 31% [22, 41] | token 12% [6, 19] | yes |
| filler moved | 17 | domain:animals | 77 | 29 | 32% [22, 44] | token 8% [3, 16] | yes |
| filler moved | 17 | domain:body | 30 | 8 | 7% [0, 21] | token 10% [0, 26] | no (n < 35) |
| filler moved | 18 | all | 210 | 71 | 30% [23, 37] | token 11% [7, 16] | yes |
| filler moved | 18 | domain:countries | 103 | 34 | 28% [18, 38] | token 14% [7, 22] | no |
| filler moved | 18 | domain:animals | 77 | 29 | 36% [25, 48] | token 8% [3, 16] | yes |
| filler moved | 18 | domain:body | 30 | 8 | 20% [10, 37] | token 10% [0, 26] | no (n < 35) |
| filler moved | 19 | all | 210 | 71 | 26% [20, 32] | token 6% [3, 10] | yes |
| filler moved | 19 | domain:countries | 103 | 34 | 24% [16, 33] | token 6% [2, 12] | yes |
| filler moved | 19 | domain:animals | 77 | 29 | 26% [17, 37] | token 4% [0, 11] | yes |
| filler moved | 19 | domain:body | 30 | 8 | 30% [17, 48] | token 13% [3, 30] | no (n < 35) |
| alt has one statement more | 17 | all | 192 | 64 | 19% [14, 25] | end 14% [10, 20]; token 9% [5, 14] | no |
| alt has one statement more | 17 | domain:countries | 93 | 32 | 25% [16, 35] | end 11% [5, 19]; token 8% [3, 15] | no |
| alt has one statement more | 17 | domain:animals | 60 | 25 | 15% [6, 26] | end 20% [11, 32]; token 10% [3, 20] | no |
| alt has one statement more | 17 | domain:body | 39 | 7 | 13% [6, 27] | end 13% [4, 27]; token 10% [4, 24] | no |
| alt has one statement more | 18 | all | 192 | 64 | 23% [18, 30] | end 13% [9, 19]; token 12% [8, 17] | no |
| alt has one statement more | 18 | domain:countries | 93 | 32 | 29% [21, 39] | end 9% [4, 16]; token 12% [6, 20] | yes |
| alt has one statement more | 18 | domain:animals | 60 | 25 | 20% [11, 32] | end 20% [11, 32]; token 13% [5, 24] | no |
| alt has one statement more | 18 | domain:body | 39 | 7 | 15% [7, 30] | end 13% [4, 27]; token 10% [4, 24] | no |
| alt has one statement more | 19 | all | 192 | 64 | 16% [12, 22] | end 9% [6, 14]; token 8% [5, 13] | no |
| alt has one statement more | 19 | domain:countries | 93 | 32 | 14% [7, 22] | end 6% [2, 13]; token 6% [2, 13] | no |
| alt has one statement more | 19 | domain:animals | 60 | 25 | 17% [8, 28] | end 12% [4, 22]; token 8% [3, 18] | no |
| alt has one statement more | 19 | domain:body | 39 | 7 | 21% [11, 36] | end 13% [6, 27]; token 13% [5, 27] | no |
| alt has one statement fewer | 17 | all | 215 | 73 | 22% [16, 29] | end 17% [12, 22]; token 9% [6, 14] | no |
| alt has one statement fewer | 17 | domain:countries | 103 | 33 | 30% [21, 40] | end 12% [6, 19]; token 10% [4, 17] | yes |
| alt has one statement fewer | 17 | domain:animals | 81 | 31 | 20% [10, 30] | end 23% [14, 34]; token 11% [5, 20] | no |
| alt has one statement fewer | 17 | domain:body | 31 | 9 | 3% [0, 16] | end 16% [6, 33]; token 3% [0, 16] | no (n < 35) |
| alt has one statement fewer | 18 | all | 215 | 73 | 27% [22, 34] | end 17% [12, 22]; token 10% [6, 14] | no |
| alt has one statement fewer | 18 | domain:countries | 103 | 33 | 36% [26, 46] | end 12% [5, 19]; token 10% [4, 17] | yes |
| alt has one statement fewer | 18 | domain:animals | 81 | 31 | 27% [19, 38] | end 22% [14, 32]; token 11% [5, 20] | no |
| alt has one statement fewer | 18 | domain:body | 31 | 9 | 0% [-0, 11] | end 19% [9, 36]; token 6% [0, 21] | no (n < 35) |
| alt has one statement fewer | 19 | all | 215 | 73 | 25% [19, 31] | end 13% [9, 18]; token 10% [7, 15] | yes |
| alt has one statement fewer | 19 | domain:countries | 103 | 33 | 27% [18, 36] | end 5% [1, 11]; token 10% [5, 17] | yes |
| alt has one statement fewer | 19 | domain:animals | 81 | 31 | 28% [20, 39] | end 17% [9, 27]; token 10% [4, 18] | no |
| alt has one statement fewer | 19 | domain:body | 31 | 9 | 10% [0, 25] | end 26% [12, 43]; token 13% [4, 29] | no (n < 35) |

## Agent priors in the job spec (jobs/d3/olmo3_7b_dpo_d3v4x_swap.yaml `hypotheses`) vs results


Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 0% [0, 2] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 0% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 99% [97, 100] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 19
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

