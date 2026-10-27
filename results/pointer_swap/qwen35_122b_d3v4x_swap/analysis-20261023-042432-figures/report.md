# D3 v4x on Qwen3.5-122B: does the address count statements by order and from the start?

Run `qwen35_122b_d3v4x_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP qwen35_122b_d3v4x_swap @ unknown | model Qwen3.5-122B-A10B-FP8 (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 33-39: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/by_layer_e5-off.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/by_layer_e5more.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/by_layer_e5fewer.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/slots_final_e5-off.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/slots_last_e5-off.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/windows_e5-off.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/domains_final_e5-off.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/domains_last_e5-off.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/domains_last_e5more.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/domains_last_e5fewer.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/levels_final.png, results/pointer_swap/qwen35_122b_d3v4x_swap/analysis-20261023-042432-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/qwen35_122b_d3v4x_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 130/28130 have the runner-up prediction within p 0.1; hook checks self no-op 2559/2560, layer-0 reproduction 2557/2560.
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
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 1%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 1%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 0%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | - | - | - |
| named → prompt | everything after the question | e5more | - | - | - |
| named → prompt | everything after the question | e5fewer | - | - | - |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer at the same statement slot 0%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer at the same statement slot 0%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 2560, "same_top": 2559, "max_abs_dlogit_max": 3.3438}, "layer0_all_reproduces_source": {"n": 2560, "same_top": 2557, "max_abs_dlogit_max": 4.9375}, "unedited_base_answer_read": {"n": 2560, "base_answer": 2560}}`; near ties: `{"n": 28130, "within_gap": 130, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | last two tokens before the answer | 42 | 80% [76, 84] | 20% [16, 24] | 40% [35, 45] | 29% [25, 34] | 0% [0, 1] |
| memory → prompt | e5more | last two tokens before the answer | 42 | 77% [72, 81] | 23% [19, 28] | 42% [38, 47] | 22% [19, 26] | 0% [0, 1] |
| memory → prompt | e5fewer | last two tokens before the answer | 42 | 81% [77, 85] | 19% [15, 23] | 30% [26, 35] | 31% [27, 35] | 0% [0, 1] |
| named → prompt | e5-off | last two tokens before the answer | 42 | 82% [78, 85] | 18% [15, 22] | 30% [26, 35] | 38% [34, 43] | 0% [0, 1] |
| named → prompt | e5more | last two tokens before the answer | 42 | 81% [76, 84] | 19% [16, 24] | 34% [30, 39] | 29% [25, 34] | 0% [0, 1] |
| named → prompt | e5fewer | last two tokens before the answer | 42 | 82% [78, 85] | 18% [15, 22] | 16% [12, 19] | 40% [36, 45] | 0% [0, 1] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 21 and 24 and 27 and 30 and 33 and 36 and 39 and 42

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **holds**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 21 | all | 425 | 84 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 21 | domain:countries | 147 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 21 | domain:animals | 140 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 21 | domain:body | 138 | 15 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 24 | all | 425 | 84 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 24 | domain:countries | 147 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 24 | domain:animals | 140 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 24 | domain:body | 138 | 15 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 27 | all | 425 | 84 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 27 | domain:countries | 147 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 27 | domain:animals | 140 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 27 | domain:body | 138 | 15 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 30 | all | 425 | 84 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 30 | domain:countries | 147 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 30 | domain:animals | 140 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 30 | domain:body | 138 | 15 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 33 | all | 425 | 84 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 33 | domain:countries | 147 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 33 | domain:animals | 140 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 33 | domain:body | 138 | 15 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 36 | all | 425 | 84 | 0% [0, 1] | token 0% [0, 1] | no |
| filler moved | 36 | domain:countries | 147 | 36 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 36 | domain:animals | 140 | 33 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 36 | domain:body | 138 | 15 | 0% [0, 3] | token 0% [0, 3] | no |
| filler moved | 39 | all | 425 | 84 | 1% [0, 2] | token 1% [0, 2] | no |
| filler moved | 39 | domain:countries | 147 | 36 | 1% [0, 4] | token 0% [0, 3] | no |
| filler moved | 39 | domain:animals | 140 | 33 | 0% [0, 3] | token 1% [0, 4] | no |
| filler moved | 39 | domain:body | 138 | 15 | 1% [0, 5] | token 1% [0, 5] | no |
| filler moved | 42 | all | 425 | 84 | 29% [25, 34] | token 8% [6, 12] | yes |
| filler moved | 42 | domain:countries | 147 | 36 | 32% [25, 40] | token 10% [5, 15] | yes |
| filler moved | 42 | domain:animals | 140 | 33 | 26% [18, 35] | token 6% [2, 11] | yes |
| filler moved | 42 | domain:body | 138 | 15 | 29% [22, 37] | token 10% [6, 16] | yes |
| alt has one statement more | 21 | all | 426 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 21 | domain:countries | 146 | 36 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 21 | domain:animals | 144 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 21 | domain:body | 136 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 24 | all | 426 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 24 | domain:countries | 146 | 36 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 24 | domain:animals | 144 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 24 | domain:body | 136 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 27 | all | 426 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 27 | domain:countries | 146 | 36 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 27 | domain:animals | 144 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 27 | domain:body | 136 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 30 | all | 426 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 30 | domain:countries | 146 | 36 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 30 | domain:animals | 144 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 30 | domain:body | 136 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 33 | all | 426 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 33 | domain:countries | 146 | 36 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 33 | domain:animals | 144 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 33 | domain:body | 136 | 15 | 1% [0, 4] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 36 | all | 426 | 85 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement more | 36 | domain:countries | 146 | 36 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 36 | domain:animals | 144 | 34 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 36 | domain:body | 136 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement more | 39 | all | 426 | 85 | 0% [0, 2] | end 0% [0, 1]; token 1% [0, 2] | no |
| alt has one statement more | 39 | domain:countries | 146 | 36 | 0% [-0, 3] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 39 | domain:animals | 144 | 34 | 0% [0, 3] | end 0% [0, 3]; token 1% [0, 5] | no |
| alt has one statement more | 39 | domain:body | 136 | 15 | 1% [0, 5] | end 0% [0, 3]; token 1% [0, 4] | no |
| alt has one statement more | 42 | all | 426 | 85 | 22% [19, 26] | end 7% [5, 10]; token 5% [3, 7] | yes |
| alt has one statement more | 42 | domain:countries | 146 | 36 | 21% [15, 28] | end 7% [3, 12]; token 6% [3, 11] | yes |
| alt has one statement more | 42 | domain:animals | 144 | 34 | 24% [17, 31] | end 8% [3, 14]; token 7% [3, 12] | yes |
| alt has one statement more | 42 | domain:body | 136 | 15 | 23% [15, 31] | end 7% [4, 13]; token 1% [0, 5] | yes |
| alt has one statement fewer | 21 | all | 429 | 84 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 21 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 21 | domain:animals | 142 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 21 | domain:body | 137 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 24 | all | 429 | 84 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 24 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 24 | domain:animals | 142 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 24 | domain:body | 137 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 27 | all | 429 | 84 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 27 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 27 | domain:animals | 142 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 27 | domain:body | 137 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 30 | all | 429 | 84 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 30 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 30 | domain:animals | 142 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 30 | domain:body | 137 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 33 | all | 429 | 84 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 33 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 33 | domain:animals | 142 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 33 | domain:body | 137 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 36 | all | 429 | 84 | 0% [0, 1] | end 0% [0, 1]; token 0% [0, 1] | no |
| alt has one statement fewer | 36 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 36 | domain:animals | 142 | 33 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 36 | domain:body | 137 | 15 | 0% [0, 3] | end 0% [0, 3]; token 0% [0, 3] | no |
| alt has one statement fewer | 39 | all | 429 | 84 | 0% [0, 1] | end 0% [0, 2]; token 0% [0, 2] | no |
| alt has one statement fewer | 39 | domain:countries | 150 | 36 | 0% [0, 2] | end 0% [0, 2]; token 1% [0, 5] | no |
| alt has one statement fewer | 39 | domain:animals | 142 | 33 | 1% [0, 4] | end 1% [0, 4]; token 0% [0, 3] | no |
| alt has one statement fewer | 39 | domain:body | 137 | 15 | 0% [0, 3] | end 1% [0, 4]; token 0% [0, 3] | no |
| alt has one statement fewer | 42 | all | 429 | 84 | 31% [27, 35] | end 9% [7, 12]; token 11% [8, 14] | yes |
| alt has one statement fewer | 42 | domain:countries | 150 | 36 | 36% [29, 44] | end 8% [4, 13]; token 14% [8, 20] | yes |
| alt has one statement fewer | 42 | domain:animals | 142 | 33 | 28% [21, 36] | end 9% [5, 15]; token 12% [6, 18] | yes |
| alt has one statement fewer | 42 | domain:body | 137 | 15 | 28% [20, 36] | end 10% [6, 16]; token 6% [3, 11] | yes |

## Agent priors in the job spec (jobs/d3/qwen35_122b_d3v4x_swap.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v4x tests (H-order-v4, H-start-v4) come out as on Qwen3.6-27B. Prior 0.4 (copied from qwen35_9b_d3v4x_swap_r2)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 1% [0, 2] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 0% [0, 1] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 0% [0, 1] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens None
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `body-RL-e5more-0008` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 39 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
Folder 0 holds the eye chart. Folder 3 holds the tongue chart. Folder 4 holds the knee chart. Folder 7 holds the liver chart. Folder 9 holds the eyebrow chart. The room still smelled of fresh paint. The weather was mild all week long.
In which folder is the chart on the body part that makes bile? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The room still smelled of fresh paint. Folder 4 holds the liver chart. Folder 5 holds the eyebrow chart. Folder 7 holds the tongue chart. Folder 0 holds the eye chart. Folder 6 holds the ankle chart. Folder 9 holds the knee chart.
In which folder is the chart on the body part above each eye? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 7; after the patch 3. Predicted: answer org kept 7 (p 0.189); answer of bridge alt's statement 9 (p 0.015); answer at the same statement slot 3 (p 0.747); answer at the same slot counted from the end 0 (p 0.012); answer at the same token position 4 (p 0.029); the alt prompt's own answer 5 (p 0.000).

