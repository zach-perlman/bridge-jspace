# D3 v4 per topic: does the slot beat the word in each topic alone, with every eligible scene?

Run `d3v4_swap_topics` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements, 3 wordings per topic.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP d3v4_swap_topics @ unknown | model Qwen3.6-27B | n per family = memory → prompt 762 items / 85 entities / 27 wordings (5 statements); named → prompt 762 items / 85 entities / 27 wordings (5 statements); memory → memory 762 items / 85 entities / 27 wordings (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 15% [12, 18]   Baseline: none = 72% [67, 76], identity = 4% [3, 6], value = 8% [6, 10]   Control: 'same' changed = 0% [0, 0]; random push of the same size changed (max over transit layers) = 0% [0, 1]; another domain's prompt changed = 6% [5, 8]
Figures: results/pointer_swap/d3v4_swap_topics/analysis-20261021-192842-figures/by_layer_e5f0.png, results/pointer_swap/d3v4_swap_topics/analysis-20261021-192842-figures/slots_final_e5f0.png, results/pointer_swap/d3v4_swap_topics/analysis-20261021-192842-figures/slots_last_e5f0.png, results/pointer_swap/d3v4_swap_topics/analysis-20261021-192842-figures/windows_e5f0.png, results/pointer_swap/d3v4_swap_topics/analysis-20261021-192842-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v4_swap_topics/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=762); position should be 117, identity 31, value 60, none 545
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 1] (max over transit layers); digits of the base context that no hypothesis predicts win 1% [0, 2]; among alt prompt reads won by a predicted digit, 975/59070 have the runner-up prediction within p 0.1; hook checks self no-op 2286/2286, layer-0 reproduction 2286/2286.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "none", "body": "mixed", "countries": "mixed"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **same statement slot (H-pointer)** (answer org kept 72% [67, 76], answer of bridge alt's statement 4% [3, 6], answer at the same statement slot 15% [12, 18], the alt prompt's own answer 8% [6, 10])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | - | - | - |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer of bridge alt's statement 6%) | same statement slot (H-pointer) (answer org kept 72%, answer at the same statement slot 15%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 24%, the alt prompt's own answer 43%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words | e5f0 | - | - | - |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 16%, the alt prompt's own answer 49%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 84%, answer at the same statement slot 10%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |
| memory → memory | question words | e5f0 | - | - | - |
| memory → memory | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer of bridge alt's statement 6%) | bridge alt's statement (H-word) (answer org kept 70%, answer of bridge alt's statement 29%) |
| memory → memory | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 78%, answer of bridge alt's statement 22%) | bridge alt's statement (H-word) (answer org kept 7%, answer of bridge alt's statement 92%) |
| memory → memory | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 762 | 762 | same statement slot (H-pointer) | yes | answer org kept 72% [67, 76], answer of bridge alt's statement 4% [3, 6], answer at the same statement slot 15% [12, 18], the alt prompt's own answer 8% [6, 10] |
| domain:animals | e5f0 | 297 | 297 | no effect | yes | answer org kept 73% [65, 81], answer of bridge alt's statement 5% [3, 8], answer at the same statement slot 12% [7, 17], the alt prompt's own answer 9% [5, 13] |
| domain:body | e5f0 | 169 | 169 | mixed | yes | answer org kept 72% [64, 80], answer of bridge alt's statement 7% [3, 12], answer at the same statement slot 17% [12, 24], the alt prompt's own answer 1% [0, 4] |
| domain:countries | e5f0 | 296 | 296 | mixed | yes | answer org kept 70% [64, 75], answer of bridge alt's statement 2% [0, 4], answer at the same statement slot 18% [13, 23], the alt prompt's own answer 11% [8, 15] |
| slot:first | e5f0 | 151 | 151 | no effect | yes | answer org kept 82% [75, 88], answer of bridge alt's statement 5% [2, 10], answer at the same statement slot 5% [2, 10], the alt prompt's own answer 6% [2, 11] |
| slot:middle | e5f0 | 458 | 458 | mixed | yes | answer org kept 71% [66, 76], answer of bridge alt's statement 4% [3, 7], answer at the same statement slot 15% [11, 19], the alt prompt's own answer 9% [6, 11] |
| slot:last | e5f0 | 153 | 153 | same statement slot (H-pointer) | yes | answer org kept 63% [55, 70], answer of bridge alt's statement 2% [0, 6], answer at the same statement slot 27% [21, 35], the alt prompt's own answer 8% [4, 13] |

## Checks

`{"self_noop": {"n": 2286, "same_top": 2286, "max_abs_dlogit_max": 3.125}, "layer0_all_reproduces_source": {"n": 2286, "same_top": 2286, "max_abs_dlogit_max": 3.3438}, "unedited_base_answer_read": {"n": 2286, "base_answer": 2286}}`; near ties: `{"n": 59070, "within_gap": 975, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | everything after the question | 48 | 38% [33, 42] | 62% [58, 67] | 9% [7, 11] | 27% [23, 31] | 0% [0, 0] |
| memory → prompt | e5f0 | last two tokens before the answer | 56 | 99% [98, 100] | 1% [0, 2] | 0% [0, 0] | 0% [0, 1] | 99% [98, 100] |
| named → prompt | e5f0 | everything after the question | 56 | 90% [88, 92] | 10% [8, 12] | 0% [0, 0] | 0% [0, 0] | 90% [88, 92] |
| named → prompt | e5f0 | last two tokens before the answer | 56 | 88% [85, 90] | 12% [10, 15] | 0% [0, 0] | 0% [0, 0] | 88% [85, 90] |
| memory → memory | e5f0 | everything after the question | 48 | 28% [23, 33] | 72% [67, 77] | 27% [23, 32] | 0% [0, 1] | 0% [0, 0] |
| memory → memory | e5f0 | last two tokens before the answer | 56 | 99% [98, 99] | 1% [1, 2] | 99% [98, 99] | 0% [0, 0] | 0% [0, 0] |

## Agent priors in the job spec (jobs/d3/d3v4_swap_topics.yaml `hypotheses`) vs results

- H-each-topic: primary cell (memory → prompt, after the question, layers 44-52 together): verdict "same statement slot" in at least 2 of 3 topics. Prior 0.45
- H-pooled-only: pooled "same statement slot", but at most 1 topic alone (the effect, ~16%, is too small for the rule per topic even at ~300 scenes). Prior 0.45
- H-word: the word wins in some topic. Prior 0.1

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 15% [12, 18], last two tokens 26% [23, 30] (>= 50%: not met); memory → memory 0% [0, 0] / 0% [0, 0] (<= 10%: met); named → prompt after the question 27% [24, 31] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 4% [3, 6] / 6% [4, 7] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 8% [6, 10] / 43% [39, 46] (>= 50%: not met); first single layer where it reaches 20%: after the question 56, last two tokens 52
- H-none: memory → prompt, answer changed after the question 28% [24, 33] (< 20%: not met)

## Worked example (from examples.json)

Item `countries-RL-e5f0-0237` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 46 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
Drawer 8 holds the Poland file. Drawer 1 holds the Finland file. Drawer 2 holds the Lebanon file. Drawer 6 holds the Spain file. Drawer 5 holds the Philippines file.
In which drawer is the file on the country whose capital is Beirut? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
Drawer 7 holds the Spain file. Drawer 8 holds the Finland file. Drawer 5 holds the Lebanon file. Drawer 2 holds the Poland file. Drawer 1 holds the Philippines file.
In which drawer is the file on the country whose capital is Madrid? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 2; after the patch 8. Predicted: answer org kept 2 (p 0.085); answer of bridge alt's statement 6 (p 0.000); answer at the same statement slot 8 (p 0.910); the alt prompt's own answer 7 (p 0.000).

