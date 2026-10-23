# D3 v6 on Olmo-Hybrid-7B Instruct: the Nth statement, a place in the text, or a distance back from the question?

Run `olmo_hybrid_7b_d3v6_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo_hybrid_7b_d3v6_swap @ unknown | model Olmo-Hybrid-Instruct-DPO-7B (chat format) | n per family = memory → prompt 188 items / 69 entities / 25 wordings (nothing moves); memory → prompt 188 items / 69 entities / 25 wordings (extra sentence before the list); memory → prompt 188 items / 69 entities / 25 wordings (extra sentence before the question); memory → prompt 188 items / 69 entities / 25 wordings (long statements); named → prompt 188 items / 69 entities / 25 wordings (nothing moves); named → prompt 188 items / 69 entities / 25 wordings (extra sentence before the list); named → prompt 188 items / 69 entities / 25 wordings (extra sentence before the question); named → prompt 188 items / 69 entities / 25 wordings (long statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = 0% [0, 2]   Baseline: none = 100% [98, 100], identity = 0% [0, 2], value = 0% [0, 2]   Control: 'same' changed = 0% [0, 2]; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/by_layer_e5-still.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/by_layer_e5-abs.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/by_layer_e5-rel.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/by_layer_e5-long.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/slots_final_e5-still.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/slots_last_e5-still.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/windows_e5-still.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/domains_final_e5-still.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/levels_final.png, results/pointer_swap/olmo_hybrid_7b_d3v6_swap/analysis-20261023-051808-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo_hybrid_7b_d3v6_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=188); position should be 0, identity 0, value 0, none 188
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 2]; among alt prompt reads won by a predicted digit, 311/26760 have the runner-up prediction within p 0.1; hook checks self no-op 1504/1504, layer-0 reproduction 752/752.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "none", "body": "none", "countries": "none"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-still: **no effect** (answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2]); e5-abs: **no effect** (answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2]); e5-rel: **no effect** (answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2]); e5-long: **no effect** (answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-still | - | - | - |
| memory → prompt | question words | e5-abs | - | - | - |
| memory → prompt | question words | e5-rel | - | - | - |
| memory → prompt | question words | e5-long | - | - | - |
| memory → prompt | everything after the question | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 93%, answer at the same statement slot 4%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 93%, answer at the same statement slot 4%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer at the same statement slot 3%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer at the same statement slot 6%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 5%, the alt prompt's own answer 74%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 6%, the alt prompt's own answer 72%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 78%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 77%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | question words + everything after | e5-still | - | - | - |
| memory → prompt | question words + everything after | e5-abs | - | - | - |
| memory → prompt | question words + everything after | e5-rel | - | - | - |
| memory → prompt | question words + everything after | e5-long | - | - | - |
| named → prompt | question words | e5-still | - | - | - |
| named → prompt | question words | e5-abs | - | - | - |
| named → prompt | question words | e5-rel | - | - | - |
| named → prompt | question words | e5-long | - | - | - |
| named → prompt | everything after the question | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer at the same statement slot 1%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 1%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 2%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 2%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 90%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 92%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 86%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 89%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5-still | 188 | 188 | no effect | yes | answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2] |
| domain:animals | e5-still | 44 | 44 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| domain:body | e5-still | 38 | 38 | no effect | yes | answer org kept 100% [91, 100], answer of bridge alt's statement 0% [0, 9], answer at the same statement slot 0% [0, 9], the alt prompt's own answer 0% [0, 9] |
| domain:countries | e5-still | 106 | 106 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [-0, 4], answer at the same statement slot 0% [-0, 4], the alt prompt's own answer 0% [-0, 4] |
| slot:first | e5-still | 44 | 44 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| slot:middle | e5-still | 108 | 108 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| slot:last | e5-still | 36 | 36 | no effect | yes | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |
| all | e5-abs | 188 | 188 | no effect | yes | answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2] |
| domain:animals | e5-abs | 44 | 44 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| domain:body | e5-abs | 38 | 38 | no effect | yes | answer org kept 100% [91, 100], answer of bridge alt's statement 0% [0, 9], answer at the same statement slot 0% [0, 9], the alt prompt's own answer 0% [0, 9] |
| domain:countries | e5-abs | 106 | 106 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [-0, 4], answer at the same statement slot 0% [-0, 4], the alt prompt's own answer 0% [-0, 4] |
| slot:first | e5-abs | 44 | 44 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| slot:middle | e5-abs | 108 | 108 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| slot:last | e5-abs | 36 | 36 | no effect | yes | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |
| all | e5-rel | 188 | 188 | no effect | yes | answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2] |
| domain:animals | e5-rel | 44 | 44 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| domain:body | e5-rel | 38 | 38 | no effect | yes | answer org kept 100% [91, 100], answer of bridge alt's statement 0% [0, 9], answer at the same statement slot 0% [0, 9], the alt prompt's own answer 0% [0, 9] |
| domain:countries | e5-rel | 106 | 106 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [-0, 4], answer at the same statement slot 0% [-0, 4], the alt prompt's own answer 0% [-0, 4] |
| slot:first | e5-rel | 44 | 44 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| slot:middle | e5-rel | 108 | 108 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| slot:last | e5-rel | 36 | 36 | no effect | yes | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |
| all | e5-long | 188 | 188 | no effect | yes | answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2] |
| domain:animals | e5-long | 44 | 44 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| domain:body | e5-long | 38 | 38 | no effect | yes | answer org kept 100% [91, 100], answer of bridge alt's statement 0% [0, 9], answer at the same statement slot 0% [0, 9], the alt prompt's own answer 0% [0, 9] |
| domain:countries | e5-long | 106 | 106 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [-0, 4], answer at the same statement slot 0% [-0, 4], the alt prompt's own answer 0% [-0, 4] |
| slot:first | e5-long | 44 | 44 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| slot:middle | e5-long | 108 | 108 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| slot:last | e5-long | 36 | 36 | no effect | yes | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |

## Checks

`{"self_noop": {"n": 1504, "same_top": 1504, "max_abs_dlogit_max": 0.5}, "layer0_all_reproduces_source": {"n": 752, "same_top": 752, "max_abs_dlogit_max": 0.6875}, "unedited_base_answer_read": {"n": 1504, "base_answer": 1504}}`; near ties: `{"n": 26760, "within_gap": 311, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | everything after the question | 17 | 9% [5, 14] | 91% [86, 95] | 3% [1, 7] | 4% [2, 8] | 0% [0, 2] |
| memory → prompt | e5-still | last two tokens before the answer | 21 | 96% [92, 99] | 4% [1, 8] | 3% [1, 6] | 15% [10, 21] | 75% [68, 81] |
| memory → prompt | e5-abs | everything after the question | 17 | 9% [4, 14] | 91% [86, 96] | 4% [1, 8] | 4% [2, 8] | 0% [0, 2] |
| memory → prompt | e5-abs | last two tokens before the answer | 20 | 94% [90, 97] | 6% [3, 10] | 5% [2, 9] | 14% [10, 19] | 72% [66, 79] |
| memory → prompt | e5-rel | everything after the question | 17 | 9% [5, 14] | 91% [86, 95] | 3% [1, 7] | 5% [2, 10] | 0% [0, 2] |
| memory → prompt | e5-rel | last two tokens before the answer | 21 | 96% [93, 99] | 4% [1, 7] | 1% [0, 4] | 15% [11, 21] | 78% [72, 84] |
| memory → prompt | e5-long | everything after the question | 17 | 7% [4, 12] | 93% [88, 96] | 2% [0, 5] | 5% [2, 9] | 0% [0, 2] |
| memory → prompt | e5-long | last two tokens before the answer | 20 | 96% [93, 99] | 4% [1, 7] | 2% [1, 5] | 15% [10, 21] | 77% [71, 83] |
| named → prompt | e5-still | everything after the question | 17 | 1% [0, 4] | 99% [96, 100] | 0% [0, 2] | 1% [0, 4] | 0% [0, 2] |
| named → prompt | e5-still | last two tokens before the answer | 20 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 10% [6, 15] | 90% [85, 94] |
| named → prompt | e5-abs | everything after the question | 17 | 2% [1, 5] | 98% [95, 99] | 1% [0, 4] | 1% [0, 4] | 0% [0, 2] |
| named → prompt | e5-abs | last two tokens before the answer | 20 | 100% [98, 100] | 0% [0, 2] | 1% [0, 3] | 7% [4, 11] | 92% [87, 96] |
| named → prompt | e5-rel | everything after the question | 17 | 3% [1, 7] | 97% [93, 99] | 2% [0, 5] | 2% [0, 5] | 0% [0, 2] |
| named → prompt | e5-rel | last two tokens before the answer | 20 | 100% [98, 100] | 0% [0, 2] | 1% [0, 3] | 13% [8, 18] | 86% [81, 91] |
| named → prompt | e5-long | everything after the question | 17 | 2% [1, 5] | 98% [95, 99] | 0% [0, 2] | 2% [1, 5] | 0% [0, 2] |
| named → prompt | e5-long | last two tokens before the answer | 20 | 99% [97, 100] | 1% [0, 3] | 1% [0, 3] | 10% [6, 15] | 89% [84, 93] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 17 and 18 and 19, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **holds**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 17 | 188 / 188 | 9% [5, 13] | 5% [2, 10] | -3% [-9, 2] | 26% [19, 32] / 31% [25, 38] | 27% [21, 34] / 28% [22, 35] | 1% [-8, 10] |
| 18 | 188 / 188 | 10% [5, 15] | 9% [4, 13] | -2% [-8, 4] | 32% [26, 39] / 39% [32, 46] | 37% [30, 44] / 39% [32, 46] | 2% [-8, 11] |
| 19 | 188 / 188 | 3% [1, 6] | 0% [0, 2] | -3% [-6, -0] | 13% [9, 19] / 14% [9, 19] | 14% [10, 20] / 14% [9, 20] | 0% [-7, 7] |

## Agent priors in the job spec (jobs/d3/olmo_hybrid_7b_d3v6_swap.yaml `hypotheses`) vs results

- H-rel (Dan): as d3v6_swap_27b at layers 17, 18 or 19. Agents' prior 0.35 (copied from olmo3_7b_instruct_d3v6_swap)
- H-abs: as d3v6_swap_27b. Prior 0.15 (copied from olmo3_7b_instruct_d3v6_swap)
- H-ordinal: as d3v6_swap_27b. Prior 0.45 (copied from olmo3_7b_instruct_d3v6_swap)
- H-long (Dan): as d3v6_swap_27b. Prior 0.4 (copied from olmo3_7b_instruct_d3v6_swap)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [0, 2], last two tokens 1% [0, 3] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 0% [0, 2] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [0, 2] / 0% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 0% [0, 2] / 99% [97, 100] (>= 50%: met); first single layer where it reaches 20%: after the question None, last two tokens 19
- H-none: memory → prompt, answer changed after the question 0% [0, 2] (< 20%: met)

## Worked example (from examples.json)

Item `body-RL-e5-abs-0035` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The bladder chart is in folder 7. The eye chart is in folder 9. The liver chart is in folder 0. The knee chart is in folder 5. The ear chart is in folder 8.
What folder keeps the chart on the body part that hears sounds? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Alt prompt:

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The stairs creaked loudly at night. The liver chart is in folder 4. The knee chart is in folder 0. The ear chart is in folder 8. The eye chart is in folder 6. The bladder chart is in folder 5.
What folder keeps the chart on the body part that makes bile? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Answers: answer org 8; after the patch 7. Predicted: answer org kept 8 (p 0.004); answer of bridge alt's statement 0 (p 0.106); answer at the same statement slot 7 (p 0.208); answer at the same token position 9 (p 0.055); the alt prompt's own answer 4 (p 0.175).

