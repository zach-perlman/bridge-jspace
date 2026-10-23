# D3 v6 on Qwen3.5-122B: under an extra sentence before the list or before the question, which statement does the patched answer come from?

Run `qwen35_122b_d3v6_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP qwen35_122b_d3v6_swap @ unknown | model Qwen3.5-122B-A10B-FP8 (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 33-39: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/by_layer_e5-still.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/by_layer_e5-abs.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/by_layer_e5-rel.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/by_layer_e5-long.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/slots_final_e5-still.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/slots_last_e5-still.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/windows_e5-still.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/domains_final_e5-still.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/levels_final.png, results/pointer_swap/qwen35_122b_d3v6_swap/analysis-20261023-071040-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/qwen35_122b_d3v6_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 119/36020 have the runner-up prediction within p 0.1; hook checks self no-op 3296/3296, layer-0 reproduction 1646/1648.
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
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 1%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer of bridge alt's statement 1%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 1%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer at the same statement slot 1%) |
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
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer at the same statement slot 0%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 3296, "same_top": 3296, "max_abs_dlogit_max": 3.375}, "layer0_all_reproduces_source": {"n": 1648, "same_top": 1646, "max_abs_dlogit_max": 3.3438}, "unedited_base_answer_read": {"n": 3296, "base_answer": 3294}}`; near ties: `{"n": 36020, "within_gap": 119, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | last two tokens before the answer | 42 | 82% [78, 86] | 18% [14, 22] | 31% [26, 36] | 40% [35, 45] | 0% [0, 1] |
| memory → prompt | e5-abs | last two tokens before the answer | 42 | 77% [73, 81] | 23% [19, 27] | 32% [28, 37] | 29% [25, 34] | 0% [0, 1] |
| memory → prompt | e5-rel | last two tokens before the answer | 42 | 79% [75, 83] | 21% [17, 25] | 25% [21, 29] | 43% [38, 48] | 0% [0, 1] |
| memory → prompt | e5-long | last two tokens before the answer | 42 | 77% [73, 81] | 23% [19, 27] | 21% [17, 26] | 45% [41, 50] | 0% [0, 1] |
| named → prompt | e5-still | last two tokens before the answer | 42 | 80% [76, 84] | 20% [16, 24] | 20% [16, 24] | 50% [46, 55] | 0% [0, 1] |
| named → prompt | e5-abs | last two tokens before the answer | 42 | 74% [69, 78] | 26% [22, 31] | 21% [16, 25] | 40% [35, 44] | 0% [0, 1] |
| named → prompt | e5-rel | last two tokens before the answer | 42 | 79% [74, 82] | 21% [18, 26] | 19% [15, 23] | 50% [45, 55] | 0% [0, 1] |
| named → prompt | e5-long | last two tokens before the answer | 42 | 76% [72, 80] | 24% [20, 28] | 14% [11, 18] | 53% [48, 58] | 0% [0, 1] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 21 and 24 and 27 and 30 and 33 and 36 and 39 and 42, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **holds**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 21 | 412 / 412 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 24 | 412 / 412 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 27 | 412 / 412 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 30 | 412 / 412 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 33 | 412 / 412 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 36 | 412 / 412 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 39 | 412 / 412 | 0% [0, 1] | 0% [0, 1] | -0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 1% [0, 2] / 1% [0, 2] | 0% [-1, 1] |
| 42 | 412 / 412 | 12% [9, 16] | 7% [5, 10] | -5% [-9, -1] | 29% [25, 34] / 43% [38, 48] | 40% [35, 45] / 45% [41, 50] | 5% [-1, 12] |

## Agent priors in the job spec (jobs/d3/qwen35_122b_d3v6_swap.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v6 tests (H-rel, H-abs, H-ordinal, H-long) come out as on Qwen3.6-27B. Prior 0.4 (copied from qwen35_9b_d3v6_swap_r2)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 1% [0, 2] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 0% [0, 1] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens None
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e5-rel-0132` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The Spain file is in drawer 2. The Indonesia file is in drawer 0. The Canada file is in drawer 5. The Belgium file is in drawer 8. The Poland file is in drawer 9. The clock on the wall was slow again.
Which drawer holds the file on the country whose capital is Ottawa? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The Belgium file is in drawer 7. The Indonesia file is in drawer 5. The Spain file is in drawer 9. The Poland file is in drawer 0. The Canada file is in drawer 2.
Which drawer holds the file on the country whose capital is Brussels? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 5; after the patch 2. Predicted: answer org kept 5 (p 0.430); answer of bridge alt's statement 8 (p 0.002); answer at the same statement slot 2 (p 0.552); answer at the same distance back from the question 0 (p 0.007); the alt prompt's own answer 7 (p 0.001).

