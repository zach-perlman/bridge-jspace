# Muse Glimmer 30B: pointer_v6 (the label's counting / 8 sentences and colour words / shifts)

Run `muse30b_d3v6_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP muse30b_d3v6_swap @ unknown | model Muse-Glimmer-30B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 36-42: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/by_layer_e5-still.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/by_layer_e5-abs.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/by_layer_e5-rel.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/by_layer_e5-long.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/slots_final_e5-still.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/slots_last_e5-still.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/windows_e5-still.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/domains_final_e5-still.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/levels_final.png, results/pointer_swap/muse30b_d3v6_swap/analysis-20261023-031835-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/muse30b_d3v6_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 482/38568 have the runner-up prediction within p 0.1; hook checks self no-op 2632/2632, layer-0 reproduction 1316/1316.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-still: **no data** (-); e5-abs: **no data** (-); e5-rel: **no data** (-); e5-long: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

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
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 8%, answer at the same statement slot 46%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 6%, answer at the same statement slot 44%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 97%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 6%, answer at the same statement slot 48%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 9%, answer at the same statement slot 47%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
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
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 14%, answer at the same statement slot 46%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 14%, answer at the same statement slot 45%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 13%, answer at the same statement slot 48%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 22%, answer at the same statement slot 43%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 2632, "same_top": 2632, "max_abs_dlogit_max": 1.4297}, "layer0_all_reproduces_source": {"n": 1316, "same_top": 1316, "max_abs_dlogit_max": 1.5391}, "unedited_base_answer_read": {"n": 2632, "base_answer": 2632}}`; near ties: `{"n": 38568, "within_gap": 482, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | last two tokens before the answer | 36 | 100% [99, 100] | 0% [-0, 1] | 2% [0, 4] | 2% [1, 4] | 95% [93, 98] |
| memory → prompt | e5-abs | last two tokens before the answer | 44 | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 0% [-0, 1] | 100% [98, 100] |
| memory → prompt | e5-rel | last two tokens before the answer | 44 | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 0% [0, 2] | 99% [97, 100] |
| memory → prompt | e5-long | last two tokens before the answer | 36 | 100% [99, 100] | 0% [-0, 1] | 2% [0, 4] | 3% [1, 6] | 94% [91, 97] |
| named → prompt | e5-still | last two tokens before the answer | 36 | 100% [99, 100] | 0% [-0, 1] | 0% [0, 2] | 1% [0, 3] | 99% [97, 100] |
| named → prompt | e5-abs | last two tokens before the answer | 36 | 100% [99, 100] | 0% [-0, 1] | 1% [0, 2] | 0% [0, 2] | 99% [97, 100] |
| named → prompt | e5-rel | last two tokens before the answer | 36 | 100% [99, 100] | 0% [-0, 1] | 0% [0, 2] | 0% [-0, 1] | 100% [98, 100] |
| named → prompt | e5-long | last two tokens before the answer | 36 | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 2% [1, 4] | 98% [95, 99] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 26 and 28 and 30 and 32 and 34 and 36 and 38 and 40 and 42 and 44 and 46 and 48, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **does not hold**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 26 | 329 / 329 | 0% [-0, 1] | 0% [0, 2] | 0% [-1, 2] | 0% [-0, 1] / 0% [-0, 1] | 0% [-0, 1] / 0% [-0, 1] | 0% [-1, 1] |
| 28 | 329 / 329 | 0% [0, 2] | 0% [0, 2] | 0% [-1, 1] | 0% [0, 2] / 1% [0, 2] | 0% [0, 2] / 0% [-0, 1] | -0% [-2, 1] |
| 30 | 329 / 329 | 7% [4, 10] | 5% [2, 7] | -2% [-6, 1] | 19% [15, 23] / 26% [21, 31] | 25% [20, 30] / 28% [23, 33] | 3% [-3, 10] |
| 32 | 329 / 329 | 11% [8, 15] | 9% [6, 13] | -2% [-7, 3] | 44% [39, 49] / 48% [42, 53] | 46% [41, 52] / 47% [42, 53] | 1% [-7, 8] |
| 34 | 329 / 329 | 9% [6, 12] | 5% [3, 8] | -3% [-7, 1] | 39% [34, 45] / 44% [39, 50] | 43% [38, 49] / 44% [39, 49] | 0% [-7, 8] |
| 36 | 329 / 329 | 1% [0, 3] | 1% [0, 3] | -0% [-2, 2] | 2% [1, 4] / 2% [1, 4] | 2% [1, 4] / 3% [1, 6] | 1% [-1, 4] |
| 38 | 329 / 329 | 1% [0, 3] | 1% [0, 3] | -0% [-2, 2] | 2% [1, 4] / 2% [1, 4] | 2% [1, 4] / 3% [1, 5] | 1% [-2, 3] |
| 40 | 329 / 329 | 0% [0, 2] | 0% [-0, 1] | -0% [-2, 1] | 1% [0, 2] / 1% [0, 3] | 1% [0, 2] / 1% [0, 2] | 0% [-2, 2] |
| 42 | 329 / 329 | 0% [0, 2] | 0% [-0, 1] | -0% [-2, 1] | 1% [0, 2] / 1% [0, 3] | 1% [0, 2] / 1% [0, 2] | 0% [-2, 2] |
| 44 | 329 / 329 | 0% [-0, 1] | 0% [-0, 1] | 0% [-1, 1] | 0% [-0, 1] / 0% [0, 2] | 0% [-0, 1] / 0% [0, 2] | 0% [-1, 2] |
| 46 | 329 / 329 | 0% [-0, 1] | 0% [-0, 1] | 0% [-1, 1] | 0% [-0, 1] / 0% [0, 2] | 0% [-0, 1] / 0% [0, 2] | 0% [-1, 2] |
| 48 | 329 / 329 | 0% [-0, 1] | 0% [-0, 1] | 0% [-1, 1] | 0% [-0, 1] / 0% [-0, 1] | 0% [-0, 1] / 0% [0, 2] | 0% [-1, 2] |

## Agent priors in the job spec (jobs/d3/muse30b_d3v6_swap.yaml `hypotheses`) vs results

- H-as-others: the same verdicts as Qwen3.5-9B / OLMo / Gemma. Prior 0.5

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 1% [0, 2] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 3] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 98% [96, 99] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 36
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

