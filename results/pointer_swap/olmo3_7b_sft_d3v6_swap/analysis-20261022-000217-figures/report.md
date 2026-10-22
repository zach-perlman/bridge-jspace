# olmo3_7b_sft_d3v6_swap

Run `olmo3_7b_sft_d3v6_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo3_7b_sft_d3v6_swap @ unknown | model Olmo-3-7B-Instruct-SFT (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/by_layer_e5-still.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/by_layer_e5-abs.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/by_layer_e5-rel.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/by_layer_e5-long.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/slots_final_e5-still.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/slots_last_e5-still.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/windows_e5-still.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/domains_final_e5-still.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/levels_final.png, results/pointer_swap/olmo3_7b_sft_d3v6_swap/analysis-20261022-000217-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo3_7b_sft_d3v6_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 448/10576 have the runner-up prediction within p 0.1; hook checks self no-op 1248/1248, layer-0 reproduction 624/624.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-still: **no data** (-); e5-abs: **no data** (-); e5-rel: **no data** (-); e5-long: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 144, in cuts ['domain:body', 'slot:first'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-still | - | - | - |
| memory → prompt | question words | e5-abs | - | - | - |
| memory → prompt | question words | e5-rel | - | - | - |
| memory → prompt | question words | e5-long | - | - | - |
| memory → prompt | everything after the question | e5-still | - | - | - |
| memory → prompt | everything after the question | e5-abs | - | - | - |
| memory → prompt | everything after the question | e5-rel | - | - | - |
| memory → prompt | everything after the question | e5-long | - | - | - |
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 93%, answer at the same statement slot 4%) | mixed (answer org kept 5%, the alt prompt's own answer 38%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 92%, answer at the same statement slot 4%) | mixed (answer org kept 6%, the alt prompt's own answer 36%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 92%, answer at the same statement slot 5%) | mixed (answer org kept 4%, the alt prompt's own answer 35%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 98%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 90%, answer at the same statement slot 6%) | mixed (answer org kept 4%, the alt prompt's own answer 38%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | question words + everything after | e5-still | - | - | - |
| memory → prompt | question words + everything after | e5-abs | - | - | - |
| memory → prompt | question words + everything after | e5-rel | - | - | - |
| memory → prompt | question words + everything after | e5-long | - | - | - |
| named → prompt | question words | e5-still | - | - | - |
| named → prompt | question words | e5-abs | - | - | - |
| named → prompt | question words | e5-rel | - | - | - |
| named → prompt | question words | e5-long | - | - | - |
| named → prompt | everything after the question | e5-still | - | - | - |
| named → prompt | everything after the question | e5-abs | - | - | - |
| named → prompt | everything after the question | e5-rel | - | - | - |
| named → prompt | everything after the question | e5-long | - | - | - |
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 98%, answer at the same statement slot 1%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 73%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 98%, answer at the same statement slot 2%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 76%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 99%, answer at the same statement slot 1%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 72%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 89%, answer at the same statement slot 7%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 85%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 1248, "same_top": 1248, "max_abs_dlogit_max": 0.2188}, "layer0_all_reproduces_source": {"n": 624, "same_top": 624, "max_abs_dlogit_max": 0.375}, "unedited_base_answer_read": {"n": 1248, "base_answer": 1248}}`; near ties: `{"n": 10576, "within_gap": 448, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | last two tokens before the answer | 21 | 96% [92, 99] | 4% [1, 8] | 15% [9, 21] | 21% [15, 28] | 46% [38, 53] |
| memory → prompt | e5-abs | last two tokens before the answer | 21 | 94% [89, 97] | 6% [3, 11] | 15% [10, 22] | 22% [16, 29] | 42% [35, 50] |
| memory → prompt | e5-rel | last two tokens before the answer | 20 | 96% [91, 98] | 4% [2, 9] | 16% [10, 23] | 29% [21, 37] | 35% [28, 42] |
| memory → prompt | e5-long | last two tokens before the answer | 21 | 96% [92, 99] | 4% [1, 8] | 10% [5, 16] | 26% [20, 34] | 49% [41, 56] |
| named → prompt | e5-still | last two tokens before the answer | 21 | 100% [98, 100] | 0% [0, 2] | 1% [0, 5] | 9% [5, 14] | 87% [80, 92] |
| named → prompt | e5-abs | last two tokens before the answer | 21 | 98% [94, 100] | 2% [0, 6] | 3% [1, 6] | 8% [4, 13] | 84% [77, 89] |
| named → prompt | e5-rel | last two tokens before the answer | 21 | 99% [96, 100] | 1% [0, 4] | 3% [1, 7] | 12% [7, 18] | 81% [74, 86] |
| named → prompt | e5-long | last two tokens before the answer | 20 | 100% [98, 100] | 0% [0, 2] | 1% [0, 5] | 13% [8, 19] | 85% [78, 90] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 17 and 18 and 19, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **does not hold**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 17 | 156 / 156 | 6% [3, 11] | 12% [7, 18] | 6% [-1, 12] | 38% [31, 46] / 44% [36, 51] | 41% [34, 49] / 52% [44, 60] | 11% [-0, 22] |
| 18 | 156 / 156 | 10% [6, 15] | 10% [6, 16] | 1% [-6, 7] | 40% [32, 48] / 43% [35, 51] | 41% [34, 49] / 53% [45, 61] | 12% [1, 23] |
| 19 | 156 / 156 | 10% [6, 16] | 10% [6, 15] | -1% [-7, 6] | 31% [24, 39] / 35% [26, 43] | 31% [23, 39] / 40% [32, 48] | 9% [-2, 19] |

## Agent priors in the job spec (jobs/d3/olmo3_7b_sft_d3v6_swap.yaml `hypotheses`) vs results


Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 0% [0, 2] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 5] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 99% [95, 100] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 19
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

