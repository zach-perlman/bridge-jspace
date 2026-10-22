# D3 v6: is the last tokens' address the Nth statement, a place in the text, or a distance back from the question?

Run `d3v6_swap_27b` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP d3v6_swap_27b @ unknown | model Qwen3.6-27B (chat format) | n per family = memory → prompt 435 items / 85 entities / 27 wordings (nothing moves); memory → prompt 435 items / 85 entities / 27 wordings (extra sentence before the list); memory → prompt 435 items / 85 entities / 27 wordings (extra sentence before the question); memory → prompt 435 items / 85 entities / 27 wordings (long statements); named → prompt 435 items / 85 entities / 27 wordings (nothing moves); named → prompt 435 items / 85 entities / 27 wordings (extra sentence before the list); named → prompt 435 items / 85 entities / 27 wordings (extra sentence before the question); named → prompt 435 items / 85 entities / 27 wordings (long statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = 11% [8, 15]   Baseline: none = 70% [65, 74], identity = 5% [3, 7], value = 14% [10, 17]   Control: 'same' changed = 0% [0, 1]; random push of the same size changed (max over transit layers) = 0% [0, 1]; another domain's prompt changed = 9% [6, 12]
Figures: results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/by_layer_e5-still.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/by_layer_e5-abs.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/by_layer_e5-rel.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/by_layer_e5-long.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/slots_final_e5-still.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/slots_last_e5-still.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/windows_e5-still.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/domains_final_e5-still.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/levels_final.png, results/pointer_swap/d3v6_swap_27b/analysis-20261021-234143-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v6_swap_27b/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=435); position should be 50, identity 20, value 59, none 304
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 1] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 2]; among alt prompt reads won by a predicted digit, 1237/55040 have the runner-up prediction within p 0.1; hook checks self no-op 3479/3480, layer-0 reproduction 1740/1740.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "mixed", "body": "none", "countries": "mixed"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-still: **mixed** (answer org kept 70% [65, 74], answer of bridge alt's statement 5% [3, 7], answer at the same statement slot 11% [8, 15], the alt prompt's own answer 14% [10, 17]); e5-abs: **mixed** (answer org kept 75% [71, 79], answer of bridge alt's statement 4% [2, 6], answer at the same statement slot 7% [5, 9], the alt prompt's own answer 12% [9, 16]); e5-rel: **mixed** (answer org kept 66% [61, 72], answer of bridge alt's statement 3% [2, 5], answer at the same statement slot 13% [10, 17], the alt prompt's own answer 17% [13, 21]); e5-long: **mixed** (answer org kept 67% [62, 71], answer of bridge alt's statement 4% [2, 6], answer at the same statement slot 15% [12, 18], the alt prompt's own answer 13% [9, 17])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-still | - | - | - |
| memory → prompt | question words | e5-abs | - | - | - |
| memory → prompt | question words | e5-rel | - | - | - |
| memory → prompt | question words | e5-long | - | - | - |
| memory → prompt | everything after the question | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 93%, answer of bridge alt's statement 6%) | mixed (answer org kept 70%, the alt prompt's own answer 14%) |
| memory → prompt | everything after the question | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 93%, answer of bridge alt's statement 6%) | mixed (answer org kept 75%, the alt prompt's own answer 12%) |
| memory → prompt | everything after the question | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer of bridge alt's statement 4%) | mixed (answer org kept 66%, the alt prompt's own answer 17%) |
| memory → prompt | everything after the question | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 92%, answer of bridge alt's statement 6%) | mixed (answer org kept 67%, answer at the same statement slot 15%) |
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 20%, the alt prompt's own answer 55%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 23%, the alt prompt's own answer 57%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 22%, the alt prompt's own answer 52%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 26%, the alt prompt's own answer 51%) |
| memory → prompt | question words + everything after | e5-still | - | - | - |
| memory → prompt | question words + everything after | e5-abs | - | - | - |
| memory → prompt | question words + everything after | e5-rel | - | - | - |
| memory → prompt | question words + everything after | e5-long | - | - | - |
| named → prompt | question words | e5-still | - | - | - |
| named → prompt | question words | e5-abs | - | - | - |
| named → prompt | question words | e5-rel | - | - | - |
| named → prompt | question words | e5-long | - | - | - |
| named → prompt | everything after the question | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 22%, the alt prompt's own answer 49%) |
| named → prompt | everything after the question | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 21%, the alt prompt's own answer 62%) |
| named → prompt | everything after the question | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 17%, the alt prompt's own answer 54%) |
| named → prompt | everything after the question | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 39%, the alt prompt's own answer 37%) |
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 72%, the alt prompt's own answer 14%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 84%, the alt prompt's own answer 10%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 73%, the alt prompt's own answer 14%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 61%, the alt prompt's own answer 26%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5-still | 435 | 435 | mixed | yes | answer org kept 70% [65, 74], answer of bridge alt's statement 5% [3, 7], answer at the same statement slot 11% [8, 15], the alt prompt's own answer 14% [10, 17] |
| domain:animals | e5-still | 145 | 145 | mixed | yes | answer org kept 70% [61, 79], answer of bridge alt's statement 7% [3, 12], answer at the same statement slot 9% [5, 15], the alt prompt's own answer 13% [6, 21] |
| domain:body | e5-still | 140 | 140 | no effect | yes | answer org kept 82% [73, 91], answer of bridge alt's statement 5% [2, 10], answer at the same statement slot 8% [3, 14], the alt prompt's own answer 4% [0, 10] |
| domain:countries | e5-still | 150 | 150 | mixed | yes | answer org kept 58% [50, 66], answer of bridge alt's statement 2% [0, 6], answer at the same statement slot 17% [12, 24], the alt prompt's own answer 23% [16, 30] |
| slot:first | e5-still | 90 | 90 | no effect | yes | answer org kept 73% [63, 82], answer of bridge alt's statement 11% [5, 19], answer at the same statement slot 1% [0, 6], the alt prompt's own answer 14% [8, 23] |
| slot:middle | e5-still | 258 | 258 | mixed | yes | answer org kept 71% [66, 77], answer of bridge alt's statement 3% [1, 5], answer at the same statement slot 13% [9, 17], the alt prompt's own answer 12% [8, 17] |
| slot:last | e5-still | 87 | 87 | mixed | yes | answer org kept 62% [52, 72], answer of bridge alt's statement 3% [0, 10], answer at the same statement slot 18% [11, 28], the alt prompt's own answer 16% [8, 25] |
| all | e5-abs | 435 | 435 | mixed | yes | answer org kept 75% [71, 79], answer of bridge alt's statement 4% [2, 6], answer at the same statement slot 7% [5, 9], the alt prompt's own answer 12% [9, 16] |
| domain:animals | e5-abs | 145 | 145 | no effect | yes | answer org kept 77% [68, 84], answer of bridge alt's statement 7% [3, 12], answer at the same statement slot 3% [1, 8], the alt prompt's own answer 11% [5, 18] |
| domain:body | e5-abs | 140 | 140 | no effect | yes | answer org kept 83% [76, 88], answer of bridge alt's statement 5% [2, 10], answer at the same statement slot 6% [2, 11], the alt prompt's own answer 5% [2, 10] |
| domain:countries | e5-abs | 150 | 150 | mixed | yes | answer org kept 66% [58, 73], answer of bridge alt's statement 1% [0, 4], answer at the same statement slot 11% [6, 17], the alt prompt's own answer 21% [14, 28] |
| slot:first | e5-abs | 90 | 90 | no effect | yes | answer org kept 78% [68, 86], answer of bridge alt's statement 10% [5, 18], answer at the same statement slot 1% [0, 6], the alt prompt's own answer 10% [4, 18] |
| slot:middle | e5-abs | 258 | 258 | no effect | yes | answer org kept 77% [72, 82], answer of bridge alt's statement 3% [1, 5], answer at the same statement slot 6% [4, 10], the alt prompt's own answer 12% [7, 16] |
| slot:last | e5-abs | 87 | 87 | mixed | yes | answer org kept 66% [55, 76], answer of bridge alt's statement 2% [0, 8], answer at the same statement slot 14% [7, 23], the alt prompt's own answer 17% [9, 27] |
| all | e5-rel | 435 | 435 | mixed | yes | answer org kept 66% [61, 72], answer of bridge alt's statement 3% [2, 5], answer at the same statement slot 13% [10, 17], the alt prompt's own answer 17% [13, 21] |
| domain:animals | e5-rel | 145 | 145 | mixed | yes | answer org kept 69% [59, 78], answer of bridge alt's statement 3% [1, 8], answer at the same statement slot 12% [7, 19], the alt prompt's own answer 13% [6, 21] |
| domain:body | e5-rel | 140 | 140 | no effect | yes | answer org kept 79% [70, 88], answer of bridge alt's statement 4% [1, 8], answer at the same statement slot 12% [6, 19], the alt prompt's own answer 5% [1, 10] |
| domain:countries | e5-rel | 150 | 150 | alt prompt's own answer (H-value) | yes | answer org kept 52% [43, 61], answer of bridge alt's statement 2% [0, 6], answer at the same statement slot 15% [8, 22], the alt prompt's own answer 31% [23, 40] |
| slot:first | e5-rel | 90 | 90 | no effect | yes | answer org kept 76% [66, 85], answer of bridge alt's statement 7% [1, 14], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 18% [10, 27] |
| slot:middle | e5-rel | 258 | 258 | mixed | yes | answer org kept 67% [61, 73], answer of bridge alt's statement 2% [1, 5], answer at the same statement slot 15% [11, 20], the alt prompt's own answer 15% [10, 20] |
| slot:last | e5-rel | 87 | 87 | mixed | yes | answer org kept 55% [44, 67], answer of bridge alt's statement 1% [0, 6], answer at the same statement slot 22% [12, 32], the alt prompt's own answer 22% [13, 32] |
| all | e5-long | 435 | 435 | mixed | yes | answer org kept 67% [62, 71], answer of bridge alt's statement 4% [2, 6], answer at the same statement slot 15% [12, 18], the alt prompt's own answer 13% [9, 17] |
| domain:animals | e5-long | 145 | 145 | mixed | yes | answer org kept 63% [55, 72], answer of bridge alt's statement 6% [3, 11], answer at the same statement slot 12% [8, 19], the alt prompt's own answer 16% [9, 23] |
| domain:body | e5-long | 140 | 140 | no effect | yes | answer org kept 76% [69, 83], answer of bridge alt's statement 5% [2, 10], answer at the same statement slot 14% [9, 21], the alt prompt's own answer 1% [0, 5] |
| domain:countries | e5-long | 150 | 150 | mixed | yes | answer org kept 61% [52, 69], answer of bridge alt's statement 1% [0, 5], answer at the same statement slot 17% [11, 24], the alt prompt's own answer 21% [14, 28] |
| slot:first | e5-long | 90 | 90 | no effect | yes | answer org kept 73% [63, 82], answer of bridge alt's statement 10% [4, 18], answer at the same statement slot 3% [0, 9], the alt prompt's own answer 12% [5, 21] |
| slot:middle | e5-long | 258 | 258 | mixed | yes | answer org kept 66% [60, 71], answer of bridge alt's statement 3% [1, 6], answer at the same statement slot 17% [13, 22], the alt prompt's own answer 12% [8, 17] |
| slot:last | e5-long | 87 | 87 | mixed | yes | answer org kept 63% [53, 74], answer of bridge alt's statement 1% [0, 6], answer at the same statement slot 20% [12, 29], the alt prompt's own answer 15% [7, 24] |

## Checks

`{"self_noop": {"n": 3480, "same_top": 3479, "max_abs_dlogit_max": 1.4062}, "layer0_all_reproduces_source": {"n": 1740, "same_top": 1740, "max_abs_dlogit_max": 1.3031}, "unedited_base_answer_read": {"n": 3480, "base_answer": 3479}}`; near ties: `{"n": 55040, "within_gap": 1237, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | everything after the question | 50 | 40% [35, 45] | 60% [55, 65] | 9% [6, 12] | 28% [24, 33] | 0% [0, 1] |
| memory → prompt | e5-still | last two tokens before the answer | 50 | 84% [81, 87] | 16% [13, 19] | 22% [18, 26] | 48% [44, 53] | 0% [0, 1] |
| memory → prompt | e5-abs | everything after the question | 48 | 32% [28, 36] | 68% [64, 72] | 8% [5, 10] | 19% [15, 23] | 0% [0, 1] |
| memory → prompt | e5-abs | last two tokens before the answer | 50 | 79% [75, 83] | 21% [17, 25] | 20% [16, 24] | 38% [34, 43] | 0% [0, 1] |
| memory → prompt | e5-rel | everything after the question | 50 | 42% [37, 47] | 58% [53, 63] | 10% [7, 13] | 29% [24, 33] | 0% [0, 1] |
| memory → prompt | e5-rel | last two tokens before the answer | 50 | 82% [78, 85] | 18% [15, 22] | 18% [15, 22] | 50% [46, 55] | 0% [0, 1] |
| memory → prompt | e5-long | everything after the question | 50 | 41% [36, 46] | 59% [54, 64] | 8% [5, 11] | 29% [25, 34] | 0% [0, 1] |
| memory → prompt | e5-long | last two tokens before the answer | 50 | 81% [77, 84] | 19% [16, 23] | 16% [13, 20] | 51% [47, 56] | 0% [0, 1] |
| named → prompt | e5-still | everything after the question | 50 | 75% [71, 79] | 25% [21, 29] | 19% [15, 23] | 46% [41, 51] | 0% [0, 1] |
| named → prompt | e5-still | last two tokens before the answer | 50 | 52% [47, 56] | 48% [44, 53] | 11% [9, 15] | 35% [31, 40] | 0% [0, 1] |
| named → prompt | e5-abs | everything after the question | 50 | 73% [69, 77] | 27% [23, 31] | 18% [14, 22] | 40% [36, 45] | 0% [0, 1] |
| named → prompt | e5-abs | last two tokens before the answer | 50 | 36% [31, 40] | 64% [60, 69] | 9% [7, 13] | 19% [15, 23] | 0% [0, 1] |
| named → prompt | e5-rel | everything after the question | 50 | 77% [73, 81] | 23% [19, 27] | 16% [12, 20] | 50% [45, 55] | 0% [0, 1] |
| named → prompt | e5-rel | last two tokens before the answer | 50 | 51% [47, 56] | 49% [44, 53] | 11% [8, 14] | 36% [31, 40] | 0% [0, 1] |
| named → prompt | e5-long | everything after the question | 50 | 67% [63, 72] | 33% [28, 37] | 14% [10, 17] | 46% [41, 50] | 0% [0, 1] |
| named → prompt | e5-long | last two tokens before the answer | 50 | 71% [67, 76] | 29% [24, 33] | 13% [10, 17] | 48% [43, 53] | 0% [0, 1] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 48 and 50, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **holds**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 48 | 435 / 435 | 4% [3, 7] | 1% [0, 3] | -3% [-6, -1] | 15% [12, 18] / 16% [13, 20] | 19% [16, 23] / 18% [14, 22] | -1% [-7, 4] |
| 50 | 435 / 435 | 17% [14, 21] | 9% [6, 12] | -9% [-13, -4] | 38% [34, 43] / 50% [46, 55] | 48% [44, 53] / 51% [47, 56] | 3% [-3, 10] |

## Agent priors in the job spec (jobs/d3/d3v6_swap_27b.yaml `hypotheses`) vs results

- H-rel (Dan): share of answers at the same distance back (e5-rel) minus share at the same place in the text (e5-abs) has lower bound > 0 at layer 48 or 50 (memory -> prompt, last two tokens, pooled). Agents' prior 0.35
- H-abs: the same difference has upper bound < 0. Prior 0.15
- H-ordinal: in both shifted layouts the same slot's lower bound exceeds the moved statement's upper bound, at layer 48 or 50. Prior 0.6
- H-long (Dan): same-slot share, long minus still, upper bound < 0 at layer 48 or 50. Prior 0.4

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 11% [8, 15], last two tokens 20% [16, 24] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 23% [20, 28] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 5% [3, 7] / 4% [2, 6] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 14% [10, 17] / 55% [50, 60] (>= 50%: met); first single layer where it reaches 20%: after the question None, last two tokens 52
- H-none: memory → prompt, answer changed after the question 30% [26, 35] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e5-still-0105` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 50 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
Drawer 0 holds the Greece file. Drawer 8 holds the Spain file. Drawer 1 holds the Finland file. Drawer 5 holds the Egypt file. Drawer 4 holds the Pakistan file. The town hall bell rang twice today.
What drawer keeps the file on the country whose capital is Cairo? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
Drawer 0 holds the Finland file. Drawer 6 holds the Pakistan file. Drawer 4 holds the Greece file. Drawer 5 holds the Spain file. Drawer 7 holds the Egypt file. The town hall bell rang twice today.
What drawer keeps the file on the country whose capital is Islamabad? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 5; after the patch 8. Predicted: answer org kept 5 (p 0.016); answer of bridge alt's statement 4 (p 0.000); answer at the same statement slot 8 (p 0.982); the alt prompt's own answer 6 (p 0.000).

