# D3 v6 on Gemma 4 31B-it: under an extra sentence before the list (place in the text shifts) or ...

Run `gemma4it_d3v6_swap_r2` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP gemma4it_d3v6_swap_r2 @ unknown | model gemma-4-31B-it (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 41-49: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/by_layer_e5-still.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/by_layer_e5-abs.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/by_layer_e5-rel.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/by_layer_e5-long.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/slots_final_e5-still.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/slots_last_e5-still.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/windows_e5-still.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/domains_final_e5-still.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/levels_final.png, results/pointer_swap/gemma4it_d3v6_swap_r2/analysis-20261022-122347-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/gemma4it_d3v6_swap_r2/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 259/29699 have the runner-up prediction within p 0.1; hook checks self no-op 2704/2704, layer-0 reproduction 1352/1352.
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
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 14%, the alt prompt's own answer 86%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 12%, the alt prompt's own answer 88%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 17%, the alt prompt's own answer 83%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 13%, the alt prompt's own answer 87%) |
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
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 20%, the alt prompt's own answer 80%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 17%, the alt prompt's own answer 83%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 21%, the alt prompt's own answer 79%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 18%, the alt prompt's own answer 82%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 2704, "same_top": 2704, "max_abs_dlogit_max": 1.75}, "layer0_all_reproduces_source": {"n": 1352, "same_top": 1352, "max_abs_dlogit_max": 1.5}, "unedited_base_answer_read": {"n": 2704, "base_answer": 2704}}`; near ties: `{"n": 29699, "within_gap": 259, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | last two tokens before the answer | 52 | 86% [82, 90] | 14% [10, 18] | 0% [0, 1] | 0% [0, 1] | 86% [82, 90] |
| memory → prompt | e5-abs | last two tokens before the answer | 52 | 89% [85, 92] | 11% [8, 15] | 0% [0, 1] | 0% [0, 2] | 89% [85, 92] |
| memory → prompt | e5-rel | last two tokens before the answer | 48 | 85% [80, 88] | 15% [12, 20] | 0% [0, 1] | 0% [0, 1] | 85% [80, 88] |
| memory → prompt | e5-long | last two tokens before the answer | 52 | 88% [84, 91] | 12% [9, 16] | 0% [0, 1] | 0% [0, 1] | 88% [84, 91] |
| named → prompt | e5-still | last two tokens before the answer | 52 | 83% [79, 87] | 17% [13, 21] | 0% [0, 1] | 0% [0, 1] | 83% [79, 87] |
| named → prompt | e5-abs | last two tokens before the answer | 52 | 86% [82, 90] | 14% [10, 18] | 0% [0, 1] | 0% [0, 1] | 86% [82, 90] |
| named → prompt | e5-rel | last two tokens before the answer | 52 | 80% [76, 85] | 20% [15, 24] | 0% [0, 1] | 0% [0, 1] | 80% [76, 85] |
| named → prompt | e5-long | last two tokens before the answer | 52 | 84% [79, 87] | 16% [13, 21] | 0% [0, 1] | 0% [0, 1] | 84% [79, 87] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 24 and 28 and 32 and 36 and 40 and 44 and 48 and 52, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **does not hold**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 24 | 338 / 338 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 28 | 338 / 338 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 32 | 338 / 338 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 36 | 338 / 338 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 40 | 338 / 338 | 1% [0, 3] | 1% [0, 3] | 0% [-2, 2] | 16% [12, 20] / 18% [14, 22] | 18% [14, 22] / 21% [17, 26] | 3% [-3, 9] |
| 44 | 338 / 338 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 2] | 0% [0, 2] / 1% [0, 3] | 1% [-1, 2] |
| 48 | 338 / 338 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 2] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 52 | 338 / 338 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 2] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |

## Agent priors in the job spec (jobs/d3/gemma4it_d3v6_swap_r2.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v6 tests (H-rel, H-abs, H-ordinal, H-long) come out as on Qwen3.6-27B. Prior 0.4

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 0% [0, 1] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 0% [0, 1] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 86% [82, 90] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 44
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e5-long-0091` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 44 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<bos><|turn>user
The morning was grey and very still. Drawer 8 holds the Norway file, as shown on the printed sheet pinned to the noticeboard. Drawer 7 holds the France file, as noted in the old inventory that was updated last spring. Drawer 0 holds the Greece file, following the change that was agreed at the last staff meeting. Drawer 2 holds the Venezuela file, as everyone on the team was told during the morning briefing. Drawer 6 holds the Austria file, as written on the faded label stuck to the side.
In which drawer is the file on the country whose capital is Athens? Answer with a single word and nothing else.<turn|>
<|turn>model
<|channel>thought
<channel|>Answer: 
```

Alt prompt:

```
<bos><|turn>user
The morning was grey and very still. Drawer 9 holds the Austria file, as shown on the printed sheet pinned to the noticeboard. Drawer 7 holds the France file, as noted in the old inventory that was updated last spring. Drawer 2 holds the Greece file, following the change that was agreed at the last staff meeting. Drawer 0 holds the Norway file, as everyone on the team was told during the morning briefing. Drawer 6 holds the Venezuela file, as written on the faded label stuck to the side.
In which drawer is the file on the country whose capital is Vienna? Answer with a single word and nothing else.<turn|>
<|turn>model
<|channel>thought
<channel|>Answer: 
```

Answers: answer org 0; after the patch 8. Predicted: answer org kept 0 (p 0.437); answer of bridge alt's statement 6 (p 0.000); answer at the same statement slot 8 (p 0.562); the alt prompt's own answer 9 (p 0.001).

