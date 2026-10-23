# Muse Glimmer 30B: pointer_v4x (the label's counting / 8 sentences and colour words / shifts)

Run `muse30b_d3v4x_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP muse30b_d3v4x_swap @ unknown | model Muse-Glimmer-30B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 36-42: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/by_layer_e5-off.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/by_layer_e5more.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/by_layer_e5fewer.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/slots_final_e5-off.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/slots_last_e5-off.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/windows_e5-off.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/domains_final_e5-off.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/domains_last_e5-off.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/domains_last_e5more.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/domains_last_e5fewer.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/levels_final.png, results/pointer_swap/muse30b_d3v4x_swap/analysis-20261023-011445-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/muse30b_d3v4x_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 526/29852 have the runner-up prediction within p 0.1; hook checks self no-op 2001/2002, layer-0 reproduction 2001/2002.
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
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 10%, answer at the same statement slot 38%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 98%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 7%, answer of bridge alt's statement 44%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 8%, answer at the same statement slot 43%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 97%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | - | - | - |
| named → prompt | everything after the question | e5more | - | - | - |
| named → prompt | everything after the question | e5fewer | - | - | - |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 18%, answer at the same statement slot 38%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 17%, answer of bridge alt's statement 35%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 13%, answer at the same statement slot 49%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 2002, "same_top": 2001, "max_abs_dlogit_max": 1.4551}, "layer0_all_reproduces_source": {"n": 2002, "same_top": 2001, "max_abs_dlogit_max": 1.5312}, "unedited_base_answer_read": {"n": 2002, "base_answer": 2001}}`; near ties: `{"n": 29852, "within_gap": 526, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | last two tokens before the answer | 44 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [98, 100] |
| memory → prompt | e5more | last two tokens before the answer | 40 | 100% [99, 100] | 0% [0, 1] | 0% [0, 2] | 0% [0, 1] | 98% [96, 100] |
| memory → prompt | e5fewer | last two tokens before the answer | 44 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [98, 100] |
| named → prompt | e5-off | last two tokens before the answer | 36 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 2] | 100% [98, 100] |
| named → prompt | e5more | last two tokens before the answer | 36 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 2] | 99% [98, 100] |
| named → prompt | e5fewer | last two tokens before the answer | 40 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 2] | 100% [98, 100] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 26 and 28 and 30 and 32 and 34 and 36 and 38 and 40 and 42 and 44 and 46 and 48

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **holds**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 26 | all | 372 | 81 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 26 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 26 | domain:animals | 129 | 33 | 1% [0, 4] | token 1% [0, 4] | no |
| filler moved | 26 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| filler moved | 28 | all | 372 | 81 | 0% [0, 2] | token 0% [0, 2] | no |
| filler moved | 28 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 28 | domain:animals | 129 | 33 | 1% [0, 4] | token 1% [0, 4] | no |
| filler moved | 28 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| filler moved | 30 | all | 372 | 81 | 14% [10, 18] | token 3% [2, 6] | yes |
| filler moved | 30 | domain:countries | 139 | 34 | 21% [15, 28] | token 5% [2, 10] | yes |
| filler moved | 30 | domain:animals | 129 | 33 | 16% [9, 23] | token 3% [1, 8] | yes |
| filler moved | 30 | domain:body | 104 | 14 | 2% [0, 7] | token 2% [0, 7] | no |
| filler moved | 32 | all | 372 | 81 | 38% [33, 44] | token 9% [6, 13] | yes |
| filler moved | 32 | domain:countries | 139 | 34 | 42% [33, 50] | token 12% [6, 18] | yes |
| filler moved | 32 | domain:animals | 129 | 33 | 36% [27, 45] | token 8% [4, 14] | yes |
| filler moved | 32 | domain:body | 104 | 14 | 38% [28, 48] | token 9% [3, 16] | yes |
| filler moved | 34 | all | 372 | 81 | 32% [26, 37] | token 8% [5, 12] | yes |
| filler moved | 34 | domain:countries | 139 | 34 | 36% [28, 45] | token 9% [4, 14] | yes |
| filler moved | 34 | domain:animals | 129 | 33 | 27% [18, 37] | token 9% [4, 15] | yes |
| filler moved | 34 | domain:body | 104 | 14 | 32% [21, 41] | token 8% [3, 14] | yes |
| filler moved | 36 | all | 372 | 81 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 36 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 36 | domain:animals | 129 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 36 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| filler moved | 38 | all | 372 | 81 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 38 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 38 | domain:animals | 129 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 38 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| filler moved | 40 | all | 372 | 81 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 40 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 40 | domain:animals | 129 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 40 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| filler moved | 42 | all | 372 | 81 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 42 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 42 | domain:animals | 129 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 42 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| filler moved | 44 | all | 372 | 81 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 44 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 44 | domain:animals | 129 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 44 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| filler moved | 46 | all | 372 | 81 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 46 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 46 | domain:animals | 129 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 46 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| filler moved | 48 | all | 372 | 81 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 48 | domain:countries | 139 | 34 | 0% [-0, 3] | token 0% [-0, 3] | no |
| filler moved | 48 | domain:animals | 129 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 48 | domain:body | 104 | 14 | 0% [0, 4] | token 0% [0, 4] | no |
| alt has one statement more | 26 | all | 319 | 81 | 0% [0, 2] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 26 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 26 | domain:animals | 118 | 33 | 1% [0, 5] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 26 | domain:body | 75 | 14 | 0% [0, 5] | end 0% [0, 5]; token 0% [0, 5] | no |
| alt has one statement more | 28 | all | 319 | 81 | 0% [0, 2] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 28 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 28 | domain:animals | 118 | 33 | 1% [0, 5] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 28 | domain:body | 75 | 14 | 0% [0, 5] | end 0% [0, 5]; token 0% [0, 5] | no |
| alt has one statement more | 30 | all | 319 | 81 | 12% [8, 16] | end 6% [3, 9]; token 3% [1, 5] | no |
| alt has one statement more | 30 | domain:countries | 126 | 34 | 11% [6, 18] | end 5% [2, 10]; token 1% [0, 4] | no |
| alt has one statement more | 30 | domain:animals | 118 | 33 | 14% [8, 22] | end 7% [2, 13]; token 4% [1, 10] | no |
| alt has one statement more | 30 | domain:body | 75 | 14 | 8% [3, 16] | end 7% [2, 15]; token 3% [0, 9] | no |
| alt has one statement more | 32 | all | 319 | 81 | 30% [25, 35] | end 11% [8, 15]; token 7% [4, 10] | yes |
| alt has one statement more | 32 | domain:countries | 126 | 34 | 32% [24, 40] | end 11% [7, 18]; token 6% [2, 11] | yes |
| alt has one statement more | 32 | domain:animals | 118 | 33 | 29% [21, 38] | end 12% [6, 19]; token 8% [4, 15] | yes |
| alt has one statement more | 32 | domain:body | 75 | 14 | 28% [17, 39] | end 11% [5, 20]; token 7% [2, 15] | no |
| alt has one statement more | 34 | all | 319 | 81 | 23% [19, 28] | end 6% [4, 9]; token 6% [3, 9] | yes |
| alt has one statement more | 34 | domain:countries | 126 | 34 | 25% [18, 33] | end 3% [1, 8]; token 5% [2, 10] | yes |
| alt has one statement more | 34 | domain:animals | 118 | 33 | 23% [16, 31] | end 8% [3, 15]; token 7% [2, 13] | yes |
| alt has one statement more | 34 | domain:body | 75 | 14 | 21% [14, 32] | end 8% [3, 16]; token 7% [2, 15] | no |
| alt has one statement more | 36 | all | 319 | 81 | 1% [0, 2] | end 1% [0, 2]; token 1% [0, 2] | no |
| alt has one statement more | 36 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 2% [0, 6] | no |
| alt has one statement more | 36 | domain:animals | 118 | 33 | 1% [0, 5] | end 1% [0, 5]; token 0% [0, 3] | no |
| alt has one statement more | 36 | domain:body | 75 | 14 | 1% [0, 7] | end 1% [0, 7]; token 0% [0, 5] | no |
| alt has one statement more | 38 | all | 319 | 81 | 1% [0, 2] | end 0% [0, 2]; token 1% [0, 3] | no |
| alt has one statement more | 38 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 2% [0, 6] | no |
| alt has one statement more | 38 | domain:animals | 118 | 33 | 1% [0, 5] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 38 | domain:body | 75 | 14 | 1% [0, 7] | end 1% [0, 7]; token 1% [0, 7] | no |
| alt has one statement more | 40 | all | 319 | 81 | 0% [0, 1] | end 0% [0, 2]; token 1% [0, 2] | no |
| alt has one statement more | 40 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 1% [0, 4] | no |
| alt has one statement more | 40 | domain:animals | 118 | 33 | 0% [0, 3] | end 1% [0, 5]; token 0% [0, 3] | no |
| alt has one statement more | 40 | domain:body | 75 | 14 | 0% [0, 5] | end 0% [0, 5]; token 1% [0, 7] | no |
| alt has one statement more | 42 | all | 319 | 81 | 0% [0, 1] | end 0% [0, 2]; token 1% [0, 2] | no |
| alt has one statement more | 42 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 1% [0, 4] | no |
| alt has one statement more | 42 | domain:animals | 118 | 33 | 0% [0, 3] | end 1% [0, 5]; token 0% [0, 3] | no |
| alt has one statement more | 42 | domain:body | 75 | 14 | 0% [0, 5] | end 0% [0, 5]; token 1% [0, 7] | no |
| alt has one statement more | 44 | all | 319 | 81 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 44 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 44 | domain:animals | 118 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 44 | domain:body | 75 | 14 | 0% [0, 5] | end 0% [0, 5]; token 0% [0, 5] | no |
| alt has one statement more | 46 | all | 319 | 81 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 46 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 46 | domain:animals | 118 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 46 | domain:body | 75 | 14 | 0% [0, 5] | end 0% [0, 5]; token 0% [0, 5] | no |
| alt has one statement more | 48 | all | 319 | 81 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 48 | domain:countries | 126 | 34 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 48 | domain:animals | 118 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 48 | domain:body | 75 | 14 | 0% [0, 5] | end 0% [0, 5]; token 0% [0, 5] | no |
| alt has one statement fewer | 26 | all | 310 | 79 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 26 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 26 | domain:animals | 109 | 31 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 26 | domain:body | 85 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement fewer | 28 | all | 310 | 79 | 0% [0, 1] | end 0% [0, 1]; token 1% [0, 2] | no |
| alt has one statement fewer | 28 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 28 | domain:animals | 109 | 31 | 0% [0, 3] | end 0% [0, 3]; token 1% [0, 5] | no |
| alt has one statement fewer | 28 | domain:body | 85 | 14 | 0% [0, 4] | end 0% [0, 4]; token 1% [0, 6] | no |
| alt has one statement fewer | 30 | all | 310 | 79 | 17% [13, 22] | end 8% [5, 12]; token 6% [4, 9] | yes |
| alt has one statement fewer | 30 | domain:countries | 116 | 34 | 22% [16, 31] | end 4% [1, 10]; token 8% [4, 14] | yes |
| alt has one statement fewer | 30 | domain:animals | 109 | 31 | 18% [12, 27] | end 11% [6, 18]; token 6% [3, 13] | no |
| alt has one statement fewer | 30 | domain:body | 85 | 14 | 9% [3, 18] | end 9% [4, 17]; token 4% [0, 10] | no |
| alt has one statement fewer | 32 | all | 310 | 79 | 43% [38, 49] | end 10% [7, 14]; token 14% [10, 19] | yes |
| alt has one statement fewer | 32 | domain:countries | 116 | 34 | 41% [32, 50] | end 11% [6, 18]; token 19% [12, 27] | yes |
| alt has one statement fewer | 32 | domain:animals | 109 | 31 | 50% [40, 61] | end 9% [4, 16]; token 10% [5, 17] | yes |
| alt has one statement fewer | 32 | domain:body | 85 | 14 | 36% [27, 47] | end 9% [4, 17]; token 13% [6, 22] | yes |
| alt has one statement fewer | 34 | all | 310 | 79 | 36% [31, 42] | end 12% [9, 16]; token 9% [6, 12] | yes |
| alt has one statement fewer | 34 | domain:countries | 116 | 34 | 32% [22, 42] | end 12% [6, 19]; token 10% [6, 17] | yes |
| alt has one statement fewer | 34 | domain:animals | 109 | 31 | 41% [32, 51] | end 10% [4, 17]; token 6% [2, 13] | yes |
| alt has one statement fewer | 34 | domain:body | 85 | 14 | 35% [26, 46] | end 14% [8, 23]; token 9% [4, 17] | yes |
| alt has one statement fewer | 36 | all | 310 | 79 | 1% [0, 2] | end 1% [0, 3]; token 0% [0, 2] | no |
| alt has one statement fewer | 36 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 1% [0, 5] | no |
| alt has one statement fewer | 36 | domain:animals | 109 | 31 | 0% [0, 3] | end 2% [0, 6]; token 0% [0, 3] | no |
| alt has one statement fewer | 36 | domain:body | 85 | 14 | 2% [0, 8] | end 1% [0, 6]; token 0% [0, 4] | no |
| alt has one statement fewer | 38 | all | 310 | 79 | 1% [0, 2] | end 1% [0, 3]; token 0% [0, 2] | no |
| alt has one statement fewer | 38 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 1% [0, 5] | no |
| alt has one statement fewer | 38 | domain:animals | 109 | 31 | 0% [0, 3] | end 2% [0, 6]; token 0% [0, 3] | no |
| alt has one statement fewer | 38 | domain:body | 85 | 14 | 2% [0, 8] | end 1% [0, 6]; token 0% [0, 4] | no |
| alt has one statement fewer | 40 | all | 310 | 79 | 0% [0, 1] | end 1% [0, 2]; token 0% [0, 1] | no |
| alt has one statement fewer | 40 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 40 | domain:animals | 109 | 31 | 0% [0, 3] | end 2% [0, 6]; token 0% [0, 3] | no |
| alt has one statement fewer | 40 | domain:body | 85 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement fewer | 42 | all | 310 | 79 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 1] | no |
| alt has one statement fewer | 42 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 42 | domain:animals | 109 | 31 | 1% [0, 5] | end 1% [0, 5]; token 0% [0, 3] | no |
| alt has one statement fewer | 42 | domain:body | 85 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement fewer | 44 | all | 310 | 79 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 44 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 44 | domain:animals | 109 | 31 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 44 | domain:body | 85 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement fewer | 46 | all | 310 | 79 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 46 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 46 | domain:animals | 109 | 31 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 46 | domain:body | 85 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |
| alt has one statement fewer | 48 | all | 310 | 79 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 48 | domain:countries | 116 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 48 | domain:animals | 109 | 31 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 48 | domain:body | 85 | 14 | 0% [0, 4] | end 0% [0, 4]; token 0% [0, 4] | no |

## Agent priors in the job spec (jobs/d3/muse30b_d3v4x_swap.yaml `hypotheses`) vs results

- H-as-others: the same verdicts as Qwen3.5-9B / OLMo / Gemma. Prior 0.5

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 0% [0, 1] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 3] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 98% [95, 99] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 36
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

