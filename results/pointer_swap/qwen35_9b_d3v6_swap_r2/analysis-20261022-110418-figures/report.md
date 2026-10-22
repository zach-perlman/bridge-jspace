# D3 v6 on Qwen3.5-9B: under an extra sentence before the list (place in the text shifts) or ...

Run `qwen35_9b_d3v6_swap_r2` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP qwen35_9b_d3v6_swap_r2 @ unknown | model Qwen3.5-9B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/by_layer_e5-still.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/by_layer_e5-abs.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/by_layer_e5-rel.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/by_layer_e5-long.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/slots_final_e5-still.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/slots_last_e5-still.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/windows_e5-still.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/domains_final_e5-still.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/levels_final.png, results/pointer_swap/qwen35_9b_d3v6_swap_r2/analysis-20261022-110418-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/qwen35_9b_d3v6_swap_r2/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 1336/32093 have the runner-up prediction within p 0.1; hook checks self no-op 2999/3000, layer-0 reproduction 1500/1500.
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
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 20%, answer at the same statement slot 31%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 93%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 19%, answer of bridge alt's statement 33%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 93%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 17%, answer at the same statement slot 35%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 95%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 24%, answer at the same statement slot 38%) | alt prompt's own answer (H-value) (answer org kept 5%, the alt prompt's own answer 91%) |
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
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 38%, answer at the same statement slot 32%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 96%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 45%, answer at the same statement slot 22%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 96%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 41%, answer at the same statement slot 31%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 96%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 38%, answer at the same statement slot 35%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 97%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 3000, "same_top": 2999, "max_abs_dlogit_max": 0.875}, "layer0_all_reproduces_source": {"n": 1500, "same_top": 1500, "max_abs_dlogit_max": 1.2656}, "unedited_base_answer_read": {"n": 3000, "base_answer": 3000}}`; near ties: `{"n": 32093, "within_gap": 1336, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| memory → prompt | e5-abs | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| memory → prompt | e5-rel | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| memory → prompt | e5-long | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-still | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-abs | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-rel | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-long | last two tokens before the answer | 28 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 14 and 16 and 18 and 20 and 22 and 24 and 26 and 28, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **does not hold**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 14 | 375 / 375 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 16 | 375 / 375 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 18 | 375 / 375 | 6% [4, 9] | 7% [4, 10] | 0% [-3, 4] | 21% [17, 25] / 31% [27, 36] | 30% [26, 35] / 37% [32, 42] | 6% [-1, 13] |
| 20 | 375 / 375 | 9% [6, 12] | 6% [3, 8] | -3% [-7, 1] | 24% [20, 29] / 35% [31, 40] | 31% [26, 36] / 38% [32, 43] | 7% [-0, 13] |
| 22 | 375 / 375 | 10% [7, 13] | 6% [4, 9] | -4% [-8, 0] | 26% [22, 31] / 37% [32, 42] | 34% [29, 39] / 40% [35, 45] | 6% [-1, 13] |
| 24 | 375 / 375 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 1% [0, 3] / 1% [0, 3] | 2% [1, 3] / 2% [1, 4] | 1% [-2, 3] |
| 26 | 375 / 375 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 2% [1, 3] / 1% [0, 3] | 2% [1, 3] / 2% [1, 4] | 1% [-2, 3] |
| 28 | 375 / 375 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |

## Agent priors in the job spec (jobs/d3/qwen35_9b_d3v6_swap_r2.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v6 tests (H-rel, H-abs, H-ordinal, H-long) come out as on Qwen3.6-27B. Prior 0.4

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 2% [1, 3] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 1% [0, 3] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 93% [90, 96] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 24
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e5-still-0024` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 22 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
Drawer 2 holds the Thailand file. Drawer 8 holds the Norway file. Drawer 9 holds the Sweden file. Drawer 7 holds the Peru file. Drawer 0 holds the Canada file. The lamp in the hall flickered.
What drawer keeps the file on the country whose capital is Bangkok? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
Drawer 7 holds the Peru file. Drawer 0 holds the Canada file. Drawer 2 holds the Thailand file. Drawer 3 holds the Norway file. Drawer 8 holds the Sweden file. The lamp in the hall flickered.
What drawer keeps the file on the country whose capital is Oslo? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 2; after the patch 7. Predicted: answer org kept 2 (p 0.119); answer of bridge alt's statement 8 (p 0.024); answer at the same statement slot 7 (p 0.535); the alt prompt's own answer 3 (p 0.286).

