# D3 v4x on Olmo-Hybrid-7B Instruct: does its last-token pointer also count statements by order, from the start?

Run `olmo_hybrid_7b_d3v4x_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler in another place in the alt prompt (order and token split); `e5more` = 5 statements, the alt prompt has 6 (start, end and token split); `e5fewer` = 5 statements, the alt prompt has 4 (start, end and token split).

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo_hybrid_7b_d3v4x_swap @ unknown | model Olmo-Hybrid-Instruct-DPO-7B (chat format) | n per family = memory → prompt 296 items / 78 entities / 27 wordings (filler moved); memory → prompt 270 items / 80 entities / 27 wordings (alt has one statement more); memory → prompt 296 items / 79 entities / 27 wordings (alt has one statement fewer); named → prompt 296 items / 78 entities / 27 wordings (filler moved); named → prompt 270 items / 80 entities / 27 wordings (alt has one statement more); named → prompt 296 items / 79 entities / 27 wordings (alt has one statement fewer) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = 0% [0, 2]   Baseline: none = 99% [97, 100], identity = 0% [0, 2], value = 0% [0, 1]   Control: 'same' changed = 0% [0, 1]; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/by_layer_e5-off.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/by_layer_e5more.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/by_layer_e5fewer.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/slots_final_e5-off.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/slots_last_e5-off.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/windows_e5-off.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/domains_final_e5-off.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/domains_last_e5-off.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/domains_last_e5more.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/domains_last_e5fewer.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/levels_final.png, results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/analysis-20261023-050948-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo_hybrid_7b_d3v4x_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=296); position should be 1, identity 1, value 0, none 293
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 2]; among alt prompt reads won by a predicted digit, 522/30890 have the runner-up prediction within p 0.1; hook checks self no-op 1724/1724, layer-0 reproduction 1720/1724.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "none", "body": "none", "countries": "none"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-off: **no effect** (answer org kept 99% [97, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 1]); e5more: **no effect** (answer org kept 100% [99, 100], answer of bridge alt's statement 0% [0, 1], answer at the same statement slot 0% [0, 1], the alt prompt's own answer 0% [0, 1]); e5fewer: **no effect** (answer org kept 99% [97, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 1], the alt prompt's own answer 1% [0, 2])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-off | - | - | - |
| memory → prompt | question words | e5more | - | - | - |
| memory → prompt | question words | e5fewer | - | - | - |
| memory → prompt | everything after the question | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer of bridge alt's statement 2%) | no effect (answer org kept 99%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer of bridge alt's statement 3%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 91%, answer at the same statement slot 3%) | no effect (answer org kept 99%, the alt prompt's own answer 1%) |
| memory → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 5%, the alt prompt's own answer 76%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 96%) |
| memory → prompt | last two tokens before the answer | e5more | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 81%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 96%) |
| memory → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 78%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5more | - | - | - |
| memory → prompt | question words + everything after | e5fewer | - | - | - |
| named → prompt | question words | e5-off | - | - | - |
| named → prompt | question words | e5more | - | - | - |
| named → prompt | question words | e5fewer | - | - | - |
| named → prompt | everything after the question | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 1%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer at the same statement slot 1%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5-off | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 92%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5more | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5fewer | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 94%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5more | - | - | - |
| named → prompt | question words + everything after | e5fewer | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5-off | 296 | 296 | no effect | yes | answer org kept 99% [97, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 1] |
| domain:animals | e5-off | 102 | 102 | no effect | yes | answer org kept 98% [93, 100], answer of bridge alt's statement 1% [0, 5], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| domain:body | e5-off | 61 | 61 | no effect | yes | answer org kept 98% [91, 100], answer of bridge alt's statement 0% [0, 6], answer at the same statement slot 2% [0, 9], the alt prompt's own answer 0% [0, 6] |
| domain:countries | e5-off | 133 | 133 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [-0, 3], answer at the same statement slot 0% [-0, 3], the alt prompt's own answer 0% [-0, 3] |
| slot:first | e5-off | 88 | 88 | no effect | yes | answer org kept 99% [94, 100], answer of bridge alt's statement 1% [0, 6], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:middle | e5-off | 97 | 97 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:last | e5-off | 111 | 111 | no effect | yes | answer org kept 98% [94, 100], answer of bridge alt's statement 0% [-0, 3], answer at the same statement slot 1% [0, 5], the alt prompt's own answer 0% [-0, 3] |
| all | e5more | 270 | 270 | no effect | yes | answer org kept 100% [99, 100], answer of bridge alt's statement 0% [0, 1], answer at the same statement slot 0% [0, 1], the alt prompt's own answer 0% [0, 1] |
| domain:animals | e5more | 87 | 87 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| domain:body | e5more | 57 | 57 | no effect | yes | answer org kept 100% [94, 100], answer of bridge alt's statement 0% [0, 6], answer at the same statement slot 0% [0, 6], the alt prompt's own answer 0% [0, 6] |
| domain:countries | e5more | 126 | 126 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [-0, 3], answer at the same statement slot 0% [-0, 3], the alt prompt's own answer 0% [-0, 3] |
| slot:first | e5more | 88 | 88 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:middle | e5more | 85 | 85 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:last | e5more | 97 | 97 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| all | e5fewer | 296 | 296 | no effect | yes | answer org kept 99% [97, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 1], the alt prompt's own answer 1% [0, 2] |
| domain:animals | e5fewer | 100 | 100 | no effect | yes | answer org kept 98% [93, 100], answer of bridge alt's statement 1% [0, 5], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| domain:body | e5fewer | 61 | 61 | no effect | yes | answer org kept 100% [94, 100], answer of bridge alt's statement 0% [0, 6], answer at the same statement slot 0% [0, 6], the alt prompt's own answer 0% [0, 6] |
| domain:countries | e5fewer | 135 | 135 | no effect | yes | answer org kept 99% [95, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 1% [0, 5] |
| slot:first | e5fewer | 97 | 97 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:middle | e5fewer | 97 | 97 | no effect | yes | answer org kept 96% [90, 99], answer of bridge alt's statement 1% [0, 6], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 2% [0, 7] |
| slot:last | e5fewer | 102 | 102 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |

## Checks

`{"self_noop": {"n": 1724, "same_top": 1724, "max_abs_dlogit_max": 0.5}, "layer0_all_reproduces_source": {"n": 1724, "same_top": 1720, "max_abs_dlogit_max": 0.875}, "unedited_base_answer_read": {"n": 1724, "base_answer": 1724}}`; near ties: `{"n": 30890, "within_gap": 522, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | everything after the question | 17 | 10% [5, 14] | 90% [86, 95] | 5% [2, 8] | 4% [2, 7] | 0% [0, 1] |
| memory → prompt | e5-off | last two tokens before the answer | 20 | 95% [91, 97] | 5% [3, 9] | 5% [3, 9] | 9% [7, 13] | 76% [71, 81] |
| memory → prompt | e5more | everything after the question | 17 | 10% [7, 14] | 90% [86, 93] | 6% [3, 9] | 1% [0, 4] | 0% [0, 1] |
| memory → prompt | e5more | last two tokens before the answer | 21 | 96% [93, 98] | 4% [2, 7] | 7% [4, 11] | 5% [3, 9] | 81% [76, 86] |
| memory → prompt | e5fewer | everything after the question | 17 | 14% [10, 18] | 86% [82, 90] | 3% [2, 6] | 5% [2, 8] | 0% [0, 1] |
| memory → prompt | e5fewer | last two tokens before the answer | 20 | 98% [95, 99] | 2% [1, 5] | 5% [3, 8] | 7% [4, 11] | 78% [73, 83] |
| named → prompt | e5-off | everything after the question | 17 | 1% [0, 2] | 99% [98, 100] | 1% [0, 2] | 0% [0, 1] | 0% [0, 1] |
| named → prompt | e5-off | last two tokens before the answer | 20 | 99% [98, 100] | 1% [0, 2] | 0% [0, 1] | 6% [4, 9] | 92% [89, 95] |
| named → prompt | e5more | everything after the question | 17 | 3% [1, 6] | 97% [94, 99] | 1% [0, 4] | 1% [0, 3] | 0% [0, 1] |
| named → prompt | e5more | last two tokens before the answer | 20 | 100% [99, 100] | 0% [0, 1] | 1% [0, 3] | 1% [0, 3] | 98% [95, 99] |
| named → prompt | e5fewer | everything after the question | 17 | 2% [0, 4] | 98% [96, 100] | 0% [0, 1] | 1% [0, 3] | 0% [0, 1] |
| named → prompt | e5fewer | last two tokens before the answer | 20 | 99% [97, 100] | 1% [0, 3] | 0% [0, 2] | 3% [1, 6] | 94% [90, 96] |

## Pre-registered primary (pointer_v4x): memory -> prompt, the last two tokens, layers 17 and 18 and 19

H-order-v4 (filler moved: answer at the same statement slot beats answer at the same token position, pooled and in >= 2 of 3 topics at one layer): **holds**; H-start-v4 (one more / one fewer: the slot from the start beats answer at the same slot counted from the end and answer at the same token position, pooled and in >= 2 topics, both alt types, one layer): **does not hold**.

| layout | layer | cut | n | entities | winner (from the start / order) | rivals | lower bound > rivals' upper bounds |
|---|---|---|---|---|---|---|---|
| filler moved | 17 | all | 296 | 78 | 20% [15, 24] | token 4% [2, 7] | yes |
| filler moved | 17 | domain:countries | 133 | 35 | 26% [18, 34] | token 2% [0, 6] | yes |
| filler moved | 17 | domain:animals | 102 | 30 | 19% [11, 27] | token 7% [2, 13] | no |
| filler moved | 17 | domain:body | 61 | 13 | 8% [3, 18] | token 3% [0, 11] | no |
| filler moved | 18 | all | 296 | 78 | 29% [24, 35] | token 9% [6, 13] | yes |
| filler moved | 18 | domain:countries | 133 | 35 | 35% [26, 43] | token 8% [4, 14] | yes |
| filler moved | 18 | domain:animals | 102 | 30 | 30% [21, 40] | token 10% [5, 17] | yes |
| filler moved | 18 | domain:body | 61 | 13 | 15% [8, 26] | token 10% [4, 20] | no |
| filler moved | 19 | all | 296 | 78 | 8% [5, 12] | token 2% [1, 5] | yes |
| filler moved | 19 | domain:countries | 133 | 35 | 8% [4, 14] | token 2% [0, 6] | no |
| filler moved | 19 | domain:animals | 102 | 30 | 10% [5, 17] | token 1% [0, 5] | no |
| filler moved | 19 | domain:body | 61 | 13 | 5% [0, 13] | token 5% [0, 13] | no |
| alt has one statement more | 17 | all | 270 | 80 | 12% [8, 16] | end 6% [3, 10]; token 6% [3, 9] | no |
| alt has one statement more | 17 | domain:countries | 126 | 35 | 15% [8, 22] | end 4% [1, 9]; token 5% [2, 10] | no |
| alt has one statement more | 17 | domain:animals | 87 | 32 | 10% [5, 19] | end 10% [3, 19]; token 8% [3, 16] | no |
| alt has one statement more | 17 | domain:body | 57 | 13 | 7% [2, 17] | end 5% [0, 15]; token 5% [0, 14] | no |
| alt has one statement more | 18 | all | 270 | 80 | 20% [16, 26] | end 8% [5, 12]; token 8% [5, 12] | yes |
| alt has one statement more | 18 | domain:countries | 126 | 35 | 26% [19, 34] | end 7% [3, 13]; token 8% [4, 14] | yes |
| alt has one statement more | 18 | domain:animals | 87 | 32 | 14% [7, 23] | end 10% [3, 19]; token 8% [3, 16] | no |
| alt has one statement more | 18 | domain:body | 57 | 13 | 18% [10, 29] | end 7% [1, 17]; token 9% [2, 19] | no |
| alt has one statement more | 19 | all | 270 | 80 | 4% [2, 7] | end 1% [0, 3]; token 0% [0, 2] | no |
| alt has one statement more | 19 | domain:countries | 126 | 35 | 3% [1, 8] | end 0% [-0, 3]; token 0% [-0, 3] | no |
| alt has one statement more | 19 | domain:animals | 87 | 32 | 1% [0, 6] | end 2% [0, 8]; token 0% [0, 4] | no |
| alt has one statement more | 19 | domain:body | 57 | 13 | 11% [3, 21] | end 2% [0, 9]; token 2% [0, 9] | no |
| alt has one statement fewer | 17 | all | 296 | 79 | 21% [16, 26] | end 9% [6, 13]; token 8% [5, 12] | yes |
| alt has one statement fewer | 17 | domain:countries | 135 | 35 | 26% [18, 34] | end 4% [1, 9]; token 3% [1, 7] | yes |
| alt has one statement fewer | 17 | domain:animals | 100 | 32 | 21% [12, 30] | end 13% [6, 21]; token 13% [7, 21] | no |
| alt has one statement fewer | 17 | domain:body | 61 | 12 | 8% [3, 18] | end 15% [6, 26]; token 11% [5, 22] | no |
| alt has one statement fewer | 18 | all | 296 | 79 | 31% [26, 37] | end 15% [11, 19]; token 10% [7, 14] | yes |
| alt has one statement fewer | 18 | domain:countries | 135 | 35 | 39% [31, 48] | end 9% [4, 15]; token 8% [4, 14] | yes |
| alt has one statement fewer | 18 | domain:animals | 100 | 32 | 31% [21, 42] | end 18% [10, 28]; token 11% [6, 19] | no |
| alt has one statement fewer | 18 | domain:body | 61 | 12 | 13% [7, 24] | end 23% [12, 35]; token 15% [7, 26] | no |
| alt has one statement fewer | 19 | all | 296 | 79 | 7% [4, 11] | end 4% [2, 7]; token 2% [1, 5] | no |
| alt has one statement fewer | 19 | domain:countries | 135 | 35 | 7% [4, 13] | end 4% [1, 9]; token 0% [0, 3] | no |
| alt has one statement fewer | 19 | domain:animals | 100 | 32 | 7% [2, 14] | end 4% [0, 10]; token 6% [2, 12] | no |
| alt has one statement fewer | 19 | domain:body | 61 | 12 | 7% [0, 16] | end 3% [0, 11]; token 2% [0, 9] | no |

## Agent priors in the job spec (jobs/d3/olmo_hybrid_7b_d3v4x_swap.yaml `hypotheses`) vs results

- H-order-olmo: filler moved: the order slot's lower bound exceeds the same-token-answer at the same statement slot's upper bound at layer 17, 18 or 19, pooled and in >= 2 of 3 topics (same layer). Prior 0.45 (Dan: yes, like Qwen) (copied from olmo3_7b_instruct_d3v4x_swap)
- H-start-olmo: one more and one fewer: the slot from the start's lower bound exceeds the upper bounds of the slot from the end and of the same token answer at the same statement slot at layer 17, 18 or 19, pooled and in >= 2 of 3 topics, both alt types. Prior 0.4 (Dan: yes, like Qwen) (copied from olmo3_7b_instruct_d3v4x_swap)
- H-text-position-olmo: the same token answer at the same statement slot beats order, or the end / token rival beats the start: the address is a place in the token sequence (copied from olmo3_7b_instruct_d3v4x_swap)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [0, 2], last two tokens 0% [0, 1] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 0% [0, 1] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [0, 2] / 1% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 0% [0, 1] / 96% [93, 98] (>= 50%: met); first single layer where it reaches 20%: after the question None, last two tokens 19
- H-none: memory → prompt, answer changed after the question 1% [0, 3] (< 20%: met)

## Worked example (from examples.json)

Item `animals-RL-e5fewer-0013` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The new curtains made the room feel much warmer. The wolf keeps its things in locker 1. The lion keeps its things in locker 7. The mouse keeps its things in locker 9. The tiger keeps its things in locker 8. The goose keeps its things in locker 5.
Which locker belongs to the animal known for howling? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Alt prompt:

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The lion keeps its things in locker 5. The tiger keeps its things in locker 1. The goose keeps its things in locker 6. The new curtains made the room feel much warmer. The mouse keeps its things in locker 8. The school choir practised every evening that month.
Which locker belongs to the animal known for honking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Answers: answer org 1; after the patch 9. Predicted: answer org kept 1 (p 0.015); answer of bridge alt's statement 5 (p 0.014); answer at the same statement slot 9 (p 0.342); answer at the same slot counted from the end 8 (p 0.013); answer at the same token position 7 (p 0.117); the alt prompt's own answer 6 (p 0.326).

