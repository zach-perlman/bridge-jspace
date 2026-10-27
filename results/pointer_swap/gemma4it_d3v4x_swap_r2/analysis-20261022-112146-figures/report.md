# D3 v4x on Gemma 4 31B-it: does the address count statements by order and from the start (filler ...

Run `gemma4it_d3v4x_swap_r2` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP gemma4it_d3v4x_swap_r2 @ unknown | model gemma-4-31B-it (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 41-49: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/by_layer_e5-off.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/by_layer_e5more.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/by_layer_e5fewer.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/slots_final_e5-off.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/slots_last_e5-off.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/windows_e5-off.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/domains_final_e5-off.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/domains_last_e5-off.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/domains_last_e5more.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/domains_last_e5fewer.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/levels_final.png, results/pointer_swap/gemma4it_d3v4x_swap_r2/analysis-20261022-112146-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/gemma4it_d3v4x_swap_r2/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 145/19353 have the runner-up prediction within p 0.1; hook checks self no-op 1760/1760, layer-0 reproduction 1760/1760.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-off: **no data** (-); e5more: **no data** (-); e5fewer: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 22, in cuts ['domain:animals'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-off | - | - | - |
| memory → prompt | question words | e5more | - | - | - |
| memory → prompt | question words | e5fewer | - | - | - |
| memory → prompt | everything after the question | e5-off | - | - | - |
| memory → prompt | everything after the question | e5more | - | - | - |
| memory → prompt | everything after the question | e5fewer | - | - | - |
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 10%, the alt prompt's own answer 90%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 6%, the alt prompt's own answer 94%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 12%, the alt prompt's own answer 88%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | - | - | - |
| named → prompt | everything after the question | e5more | - | - | - |
| named → prompt | everything after the question | e5fewer | - | - | - |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 10%, the alt prompt's own answer 90%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 7%, the alt prompt's own answer 93%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 12%, the alt prompt's own answer 88%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 1760, "same_top": 1760, "max_abs_dlogit_max": 1.0859}, "layer0_all_reproduces_source": {"n": 1760, "same_top": 1760, "max_abs_dlogit_max": 1.75}, "unedited_base_answer_read": {"n": 1760, "base_answer": 1760}}`; near ties: `{"n": 19353, "within_gap": 145, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | last two tokens before the answer | 48 | 93% [89, 96] | 7% [4, 11] | 0% [0, 1] | 0% [0, 1] | 93% [89, 96] |
| memory → prompt | e5more | last two tokens before the answer | 48 | 95% [91, 97] | 5% [3, 9] | 0% [-0, 1] | 0% [-0, 1] | 95% [91, 97] |
| memory → prompt | e5fewer | last two tokens before the answer | 52 | 89% [85, 93] | 11% [7, 15] | 0% [0, 1] | 0% [0, 1] | 89% [85, 93] |
| named → prompt | e5-off | last two tokens before the answer | 48 | 92% [88, 95] | 8% [5, 12] | 0% [0, 1] | 0% [0, 1] | 92% [88, 95] |
| named → prompt | e5more | last two tokens before the answer | 48 | 94% [91, 97] | 6% [3, 9] | 0% [-0, 1] | 0% [-0, 1] | 94% [91, 97] |
| named → prompt | e5fewer | last two tokens before the answer | 52 | 90% [86, 93] | 10% [7, 14] | 0% [0, 1] | 0% [0, 1] | 90% [86, 93] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 24 and 28 and 32 and 36 and 40 and 44 and 48 and 52

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **does not hold**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 24 | all | 338 | 77 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 24 | domain:countries | 150 | 36 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 24 | domain:animals | 75 | 27 | 0% [0, 5] | token 0% [0, 5] | no |
| filler moved | 24 | domain:body | 113 | 14 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 28 | all | 338 | 77 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 28 | domain:countries | 150 | 36 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 28 | domain:animals | 75 | 27 | 0% [0, 5] | token 0% [0, 5] | no |
| filler moved | 28 | domain:body | 113 | 14 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 32 | all | 338 | 77 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 32 | domain:countries | 150 | 36 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 32 | domain:animals | 75 | 27 | 0% [0, 5] | token 0% [0, 5] | no |
| filler moved | 32 | domain:body | 113 | 14 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 36 | all | 338 | 77 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 36 | domain:countries | 150 | 36 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 36 | domain:animals | 75 | 27 | 0% [0, 5] | token 0% [0, 5] | no |
| filler moved | 36 | domain:body | 113 | 14 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 40 | all | 338 | 77 | 12% [9, 16] | token 2% [1, 4] | yes |
| filler moved | 40 | domain:countries | 150 | 36 | 13% [8, 19] | token 3% [1, 7] | yes |
| filler moved | 40 | domain:animals | 75 | 27 | 9% [3, 18] | token 3% [0, 9] | no |
| filler moved | 40 | domain:body | 113 | 14 | 14% [8, 22] | token 1% [0, 5] | yes |
| filler moved | 44 | all | 338 | 77 | 1% [0, 2] | token 0% [0, 1] | no |
| filler moved | 44 | domain:countries | 150 | 36 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 44 | domain:animals | 75 | 27 | 1% [0, 7] | token 0% [0, 5] | no |
| filler moved | 44 | domain:body | 113 | 14 | 1% [0, 5] | token 0% [0, 3] | no |
| filler moved | 48 | all | 338 | 77 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 48 | domain:countries | 150 | 36 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 48 | domain:animals | 75 | 27 | 0% [0, 5] | token 0% [0, 5] | no |
| filler moved | 48 | domain:body | 113 | 14 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 52 | all | 338 | 77 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 52 | domain:countries | 150 | 36 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 52 | domain:animals | 75 | 27 | 0% [0, 5] | token 0% [0, 5] | no |
| filler moved | 52 | domain:body | 113 | 14 | 0% [0, 3] | token 0% [0, 3] | no |
| alt has one statement more | 24 | all | 266 | 70 | 0% [-0, 1] | end 0% [-0, 1]; token 0% [-0, 1] | no |
| alt has one statement more | 24 | domain:countries | 127 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 24 | domain:animals | 35 | 20 | 0% [0, 10] | end 0% [0, 10]; token 0% [0, 10] | no |
| alt has one statement more | 24 | domain:body | 104 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement more | 28 | all | 266 | 70 | 0% [-0, 1] | end 0% [-0, 1]; token 0% [-0, 1] | no |
| alt has one statement more | 28 | domain:countries | 127 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 28 | domain:animals | 35 | 20 | 0% [0, 10] | end 0% [0, 10]; token 0% [0, 10] | no |
| alt has one statement more | 28 | domain:body | 104 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement more | 32 | all | 266 | 70 | 0% [-0, 1] | end 0% [-0, 1]; token 0% [-0, 1] | no |
| alt has one statement more | 32 | domain:countries | 127 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 32 | domain:animals | 35 | 20 | 0% [0, 10] | end 0% [0, 10]; token 0% [0, 10] | no |
| alt has one statement more | 32 | domain:body | 104 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement more | 36 | all | 266 | 70 | 0% [-0, 1] | end 0% [-0, 1]; token 0% [-0, 1] | no |
| alt has one statement more | 36 | domain:countries | 127 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 36 | domain:animals | 35 | 20 | 0% [0, 10] | end 0% [0, 10]; token 0% [0, 10] | no |
| alt has one statement more | 36 | domain:body | 104 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement more | 40 | all | 266 | 70 | 9% [6, 13] | end 1% [0, 3]; token 2% [1, 5] | yes |
| alt has one statement more | 40 | domain:countries | 127 | 36 | 9% [5, 16] | end 1% [0, 4]; token 1% [0, 4] | yes |
| alt has one statement more | 40 | domain:animals | 35 | 20 | 0% [0, 10] | end 3% [0, 15]; token 9% [0, 22] | no |
| alt has one statement more | 40 | domain:body | 104 | 14 | 11% [6, 18] | end 0% [0, 4]; token 2% [0, 7] | no |
| alt has one statement more | 44 | all | 266 | 70 | 0% [0, 2] | end 0% [-0, 1]; token 0% [-0, 1] | no |
| alt has one statement more | 44 | domain:countries | 127 | 36 | 1% [0, 4] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 44 | domain:animals | 35 | 20 | 0% [0, 10] | end 0% [0, 10]; token 0% [0, 10] | no |
| alt has one statement more | 44 | domain:body | 104 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement more | 48 | all | 266 | 70 | 0% [-0, 1] | end 0% [-0, 1]; token 0% [-0, 1] | no |
| alt has one statement more | 48 | domain:countries | 127 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 48 | domain:animals | 35 | 20 | 0% [0, 10] | end 0% [0, 10]; token 0% [0, 10] | no |
| alt has one statement more | 48 | domain:body | 104 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement more | 52 | all | 266 | 70 | 0% [-0, 1] | end 0% [-0, 1]; token 0% [-0, 1] | no |
| alt has one statement more | 52 | domain:countries | 127 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 52 | domain:animals | 35 | 20 | 0% [0, 10] | end 0% [0, 10]; token 0% [0, 10] | no |
| alt has one statement more | 52 | domain:body | 104 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement fewer | 24 | all | 276 | 70 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 24 | domain:countries | 136 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 24 | domain:animals | 32 | 20 | 0% [0, 11] | end 0% [0, 11]; token 0% [0, 11] | no (n < 35) |
| alt has one statement fewer | 24 | domain:body | 108 | 14 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 28 | all | 276 | 70 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 28 | domain:countries | 136 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 28 | domain:animals | 32 | 20 | 0% [0, 11] | end 0% [0, 11]; token 0% [0, 11] | no (n < 35) |
| alt has one statement fewer | 28 | domain:body | 108 | 14 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 32 | all | 276 | 70 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 32 | domain:countries | 136 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 32 | domain:animals | 32 | 20 | 0% [0, 11] | end 0% [0, 11]; token 0% [0, 11] | no (n < 35) |
| alt has one statement fewer | 32 | domain:body | 108 | 14 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 36 | all | 276 | 70 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 36 | domain:countries | 136 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 36 | domain:animals | 32 | 20 | 0% [0, 11] | end 0% [0, 11]; token 0% [0, 11] | no (n < 35) |
| alt has one statement fewer | 36 | domain:body | 108 | 14 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 40 | all | 276 | 70 | 11% [7, 15] | end 2% [1, 5]; token 3% [1, 5] | yes |
| alt has one statement fewer | 40 | domain:countries | 136 | 36 | 10% [5, 17] | end 2% [0, 6]; token 4% [1, 9] | no |
| alt has one statement fewer | 40 | domain:animals | 32 | 20 | 3% [0, 16] | end 3% [0, 16]; token 0% [0, 11] | no (n < 35) |
| alt has one statement fewer | 40 | domain:body | 108 | 14 | 14% [7, 23] | end 2% [0, 6]; token 1% [0, 5] | yes |
| alt has one statement fewer | 44 | all | 276 | 70 | 0% [0, 2] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 44 | domain:countries | 136 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 44 | domain:animals | 32 | 20 | 3% [0, 16] | end 0% [0, 11]; token 0% [0, 11] | no (n < 35) |
| alt has one statement fewer | 44 | domain:body | 108 | 14 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 48 | all | 276 | 70 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 48 | domain:countries | 136 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 48 | domain:animals | 32 | 20 | 0% [0, 11] | end 0% [0, 11]; token 0% [0, 11] | no (n < 35) |
| alt has one statement fewer | 48 | domain:body | 108 | 14 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 52 | all | 276 | 70 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 52 | domain:countries | 136 | 36 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 52 | domain:animals | 32 | 20 | 0% [0, 11] | end 0% [0, 11]; token 0% [0, 11] | no (n < 35) |
| alt has one statement fewer | 52 | domain:body | 108 | 14 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |

## Agent priors in the job spec (jobs/d3/gemma4it_d3v4x_swap_r2.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v4x tests (H-order-v4, H-start-v4) come out as on Qwen3.6-27B. Prior 0.4

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 0% [0, 1] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 0% [0, 1] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 90% [87, 94] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 44
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `body-RL-e5-off-0044` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 44 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<bos><|turn>user
The garden hose was left out in the sun all day. The chart on the knee is kept in folder 0. The chart on the ear is kept in folder 5. The chart on the brain is kept in folder 4. The chart on the eye is kept in folder 3. The chart on the tongue is kept in folder 9.
In which folder is the chart on the body part that tastes food? Answer with a single word and nothing else.<turn|>
<|turn>model
<|channel>thought
<channel|>Answer: 
```

Alt prompt:

```
<bos><|turn>user
The chart on the tongue is kept in folder 5. The chart on the eye is kept in folder 7. The chart on the knee is kept in folder 0. The garden hose was left out in the sun all day. The chart on the ear is kept in folder 9. The chart on the brain is kept in folder 6.
In which folder is the chart on the body part that sees colours? Answer with a single word and nothing else.<turn|>
<|turn>model
<|channel>thought
<channel|>Answer: 
```

Answers: answer org 9; after the patch 5. Predicted: answer org kept 9 (p 0.175); answer of bridge alt's statement 3 (p 0.000); answer at the same statement slot 5 (p 0.785); answer at the same token position 0 (p 0.000); the alt prompt's own answer 7 (p 0.039).

