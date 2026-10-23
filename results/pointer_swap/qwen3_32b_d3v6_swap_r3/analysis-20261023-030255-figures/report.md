# D3 v6 on Qwen3-32B: under an extra sentence before the list (place in the text shifts) or ...

Run `qwen3_32b_d3v6_swap_r3` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP qwen3_32b_d3v6_swap_r3 @ unknown | model Qwen3-32B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/by_layer_e5-still.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/by_layer_e5-abs.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/by_layer_e5-rel.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/by_layer_e5-long.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/slots_final_e5-still.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/slots_last_e5-still.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/windows_e5-still.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/domains_final_e5-still.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/levels_final.png, results/pointer_swap/qwen3_32b_d3v6_swap_r3/analysis-20261023-030255-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/qwen3_32b_d3v6_swap_r3/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 33/21785 have the runner-up prediction within p 0.1; hook checks self no-op 2200/2200, layer-0 reproduction 1100/1100.
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
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 64%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, the alt prompt's own answer 0%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 65%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 59%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 61%) |
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
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 56%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 62%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 52%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 4%, the alt prompt's own answer 53%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 2200, "same_top": 2200, "max_abs_dlogit_max": 1.125}, "layer0_all_reproduces_source": {"n": 1100, "same_top": 1100, "max_abs_dlogit_max": 1.0}, "unedited_base_answer_read": {"n": 2200, "base_answer": 2200}}`; near ties: `{"n": 21785, "within_gap": 33, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | last two tokens before the answer | 56 | 99% [97, 100] | 1% [0, 3] | 1% [0, 3] | 0% [0, 2] | 97% [95, 99] |
| memory → prompt | e5-abs | last two tokens before the answer | 56 | 99% [96, 100] | 1% [0, 4] | 0% [0, 2] | 0% [0, 2] | 97% [94, 98] |
| memory → prompt | e5-rel | last two tokens before the answer | 56 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 99% [97, 100] |
| memory → prompt | e5-long | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 2% [1, 5] | 1% [0, 4] | 95% [92, 97] |
| named → prompt | e5-still | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-abs | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-rel | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |
| named → prompt | e5-long | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 32 and 36 and 40 and 44 and 48 and 52 and 56, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **does not hold**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 32 | 275 / 275 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 36 | 275 / 275 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 40 | 275 / 275 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 1] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 44 | 275 / 275 | 0% [0, 1] | 0% [0, 1] | 0% [-1, 1] | 0% [0, 1] / 0% [0, 2] | 0% [0, 1] / 0% [0, 1] | 0% [-1, 1] |
| 48 | 275 / 275 | 4% [1, 7] | 2% [0, 4] | -2% [-5, 1] | 16% [12, 21] / 23% [18, 28] | 23% [19, 29] / 31% [26, 37] | 8% [1, 15] |
| 52 | 275 / 275 | 3% [1, 5] | 1% [0, 4] | -1% [-4, 1] | 20% [16, 25] / 31% [26, 37] | 25% [20, 31] / 27% [22, 32] | 2% [-6, 9] |
| 56 | 275 / 275 | 1% [0, 3] | 0% [0, 1] | -1% [-3, 1] | 0% [0, 2] / 0% [0, 2] | 0% [0, 2] / 1% [0, 4] | 1% [-1, 3] |

## Agent priors in the job spec (jobs/d3/qwen3_32b_d3v6_swap_r3.yaml `hypotheses`) vs results

- H-same-as-27b: the pointer_swap pointer_v6 tests (H-rel, H-abs, H-ordinal, H-long) come out as on Qwen3.6-27B. Prior 0.4 (copied from qwen3_32b_d3v6_swap_r2)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 25% [20, 31] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 6% [4, 10] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 64% [58, 69] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 52
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e5-abs-0009` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 52 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The cafe was full by noon that day. The China file is in drawer 9. The Lebanon file is in drawer 2. The Chile file is in drawer 3. The Poland file is in drawer 1. The Indonesia file is in drawer 7.
In which drawer is the file on the country whose capital is Jakarta? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The Indonesia file is in drawer 1. The Poland file is in drawer 7. The Chile file is in drawer 3. The China file is in drawer 0. The Lebanon file is in drawer 2.
In which drawer is the file on the country whose capital is Beijing? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 7; after the patch 1. Predicted: answer org kept 7 (p 0.002); answer of bridge alt's statement 9 (p 0.000); answer at the same statement slot 1 (p 0.998); answer at the same token position 3 (p 0.000); the alt prompt's own answer 0 (p 0.000).

