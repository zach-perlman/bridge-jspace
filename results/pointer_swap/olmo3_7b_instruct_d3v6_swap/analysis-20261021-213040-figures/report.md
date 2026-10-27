# D3 v6 on OLMo-3-7B-Instruct: the Nth statement, a place in the text, or a distance back from the question?

Run `olmo3_7b_instruct_d3v6_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-still` = 5 statements + 1 extra sentence in the same place in both prompts; `e5-abs` = 5 statements, an extra sentence before the list in one prompt only (place in the text shifts); `e5-rel` = 5 statements, an extra sentence before the question in one prompt only (distance back shifts); `e5-long` = 5 long statements + 1 extra sentence in the same place.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo3_7b_instruct_d3v6_swap @ unknown | model Olmo-3-7B-Instruct (chat format) | n per family = memory → prompt 132 items / 58 entities / 24 wordings (nothing moves); memory → prompt 132 items / 58 entities / 24 wordings (extra sentence before the list); memory → prompt 132 items / 58 entities / 24 wordings (extra sentence before the question); memory → prompt 132 items / 58 entities / 24 wordings (long statements); named → prompt 132 items / 58 entities / 24 wordings (nothing moves); named → prompt 132 items / 58 entities / 24 wordings (extra sentence before the list); named → prompt 132 items / 58 entities / 24 wordings (extra sentence before the question); named → prompt 132 items / 58 entities / 24 wordings (long statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-still): position = 0% [0, 3]   Baseline: none = 99% [96, 100], identity = 1% [0, 4], value = 0% [0, 3]   Control: 'same' changed = 0% [0, 3]; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/by_layer_e5-still.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/by_layer_e5-abs.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/by_layer_e5-rel.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/by_layer_e5-long.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/slots_final_e5-still.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/slots_last_e5-still.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/windows_e5-still.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/domains_final_e5-still.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/levels_final.png, results/pointer_swap/olmo3_7b_instruct_d3v6_swap/analysis-20261021-213040-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo3_7b_instruct_d3v6_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-still'`: count `role` (n=132); position should be 0, identity 1, value 0, none 131
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 3]; among alt prompt reads won by a predicted digit, 152/18365 have the runner-up prediction within p 0.1; hook checks self no-op 1056/1056, layer-0 reproduction 527/528.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "none", "body": "damage", "countries": "none"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-still: **no effect** (answer org kept 99% [96, 100], answer of bridge alt's statement 1% [0, 4], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3]); e5-abs: **no effect** (answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3]); e5-rel: **no effect** (answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3]); e5-long: **no effect** (answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 432, in cuts ['domain:body', 'slot:first', 'slot:last'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-still | - | - | - |
| memory → prompt | question words | e5-abs | - | - | - |
| memory → prompt | question words | e5-rel | - | - | - |
| memory → prompt | question words | e5-long | - | - | - |
| memory → prompt | everything after the question | e5-still | no effect (answer org kept 99%, answer at the same statement slot 1%) | no effect (answer org kept 93%, answer of bridge alt's statement 3%) | no effect (answer org kept 99%, answer of bridge alt's statement 1%) |
| memory → prompt | everything after the question | e5-abs | no effect (answer org kept 99%, answer at the same statement slot 1%) | no effect (answer org kept 95%, answer of bridge alt's statement 2%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 97%, answer of bridge alt's statement 2%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 95%, answer at the same statement slot 2%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 92%, answer at the same statement slot 5%) | mixed (answer org kept 7%, the alt prompt's own answer 32%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| memory → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 92%, answer at the same statement slot 5%) | mixed (answer org kept 8%, the alt prompt's own answer 32%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 91%, answer at the same statement slot 8%) | damage (answer org kept 6%, answer at the same statement slot 34%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 91%, answer at the same statement slot 5%) | mixed (answer org kept 5%, the alt prompt's own answer 40%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 99%) |
| memory → prompt | question words + everything after | e5-still | - | - | - |
| memory → prompt | question words + everything after | e5-abs | - | - | - |
| memory → prompt | question words + everything after | e5-rel | - | - | - |
| memory → prompt | question words + everything after | e5-long | - | - | - |
| named → prompt | question words | e5-still | - | - | - |
| named → prompt | question words | e5-abs | - | - | - |
| named → prompt | question words | e5-rel | - | - | - |
| named → prompt | question words | e5-long | - | - | - |
| named → prompt | everything after the question | e5-still | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5-abs | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5-rel | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | everything after the question | e5-long | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5-still | no effect (answer org kept 99%, answer at the same statement slot 1%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 77%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-abs | no effect (answer org kept 98%, answer at the same statement slot 2%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 80%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-rel | no effect (answer org kept 98%, answer at the same statement slot 2%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 73%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-long | no effect (answer org kept 91%, answer at the same statement slot 6%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 87%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5-still | - | - | - |
| named → prompt | question words + everything after | e5-abs | - | - | - |
| named → prompt | question words + everything after | e5-rel | - | - | - |
| named → prompt | question words + everything after | e5-long | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5-still | 132 | 132 | no effect | yes | answer org kept 99% [96, 100], answer of bridge alt's statement 1% [0, 4], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| domain:animals | e5-still | 45 | 45 | no effect | yes | answer org kept 98% [88, 100], answer of bridge alt's statement 2% [0, 12], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| domain:body | e5-still | 14 | 14 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [78, 100], answer of bridge alt's statement 0% [0, 22], answer at the same statement slot 0% [0, 22], the alt prompt's own answer 0% [0, 22] |
| domain:countries | e5-still | 73 | 73 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [-0, 5], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| slot:first | e5-still | 26 | 26 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [87, 100], answer of bridge alt's statement 0% [0, 13], answer at the same statement slot 0% [0, 13], the alt prompt's own answer 0% [0, 13] |
| slot:middle | e5-still | 73 | 73 | no effect | yes | answer org kept 99% [93, 100], answer of bridge alt's statement 1% [0, 7], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| slot:last | e5-still | 33 | 33 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |
| all | e5-abs | 132 | 132 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| domain:animals | e5-abs | 45 | 45 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| domain:body | e5-abs | 14 | 14 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [78, 100], answer of bridge alt's statement 0% [0, 22], answer at the same statement slot 0% [0, 22], the alt prompt's own answer 0% [0, 22] |
| domain:countries | e5-abs | 73 | 73 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [-0, 5], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| slot:first | e5-abs | 26 | 26 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [87, 100], answer of bridge alt's statement 0% [0, 13], answer at the same statement slot 0% [0, 13], the alt prompt's own answer 0% [0, 13] |
| slot:middle | e5-abs | 73 | 73 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [-0, 5], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| slot:last | e5-abs | 33 | 33 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |
| all | e5-rel | 132 | 132 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| domain:animals | e5-rel | 45 | 45 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| domain:body | e5-rel | 14 | 14 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [78, 100], answer of bridge alt's statement 0% [0, 22], answer at the same statement slot 0% [0, 22], the alt prompt's own answer 0% [0, 22] |
| domain:countries | e5-rel | 73 | 73 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [-0, 5], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| slot:first | e5-rel | 26 | 26 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [87, 100], answer of bridge alt's statement 0% [0, 13], answer at the same statement slot 0% [0, 13], the alt prompt's own answer 0% [0, 13] |
| slot:middle | e5-rel | 73 | 73 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [-0, 5], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| slot:last | e5-rel | 33 | 33 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |
| all | e5-long | 132 | 132 | no effect | yes | answer org kept 100% [97, 100], answer of bridge alt's statement 0% [0, 3], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| domain:animals | e5-long | 45 | 45 | no effect | yes | answer org kept 100% [92, 100], answer of bridge alt's statement 0% [0, 8], answer at the same statement slot 0% [0, 8], the alt prompt's own answer 0% [0, 8] |
| domain:body | e5-long | 14 | 14 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [78, 100], answer of bridge alt's statement 0% [0, 22], answer at the same statement slot 0% [0, 22], the alt prompt's own answer 0% [0, 22] |
| domain:countries | e5-long | 73 | 73 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [-0, 5], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| slot:first | e5-long | 26 | 26 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [87, 100], answer of bridge alt's statement 0% [0, 13], answer at the same statement slot 0% [0, 13], the alt prompt's own answer 0% [0, 13] |
| slot:middle | e5-long | 73 | 73 | no effect | yes | answer org kept 100% [95, 100], answer of bridge alt's statement 0% [-0, 5], answer at the same statement slot 0% [-0, 5], the alt prompt's own answer 0% [-0, 5] |
| slot:last | e5-long | 33 | 33 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [90, 100], answer of bridge alt's statement 0% [0, 10], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 0% [0, 10] |

## Checks

`{"self_noop": {"n": 1056, "same_top": 1056, "max_abs_dlogit_max": 0.3516}, "layer0_all_reproduces_source": {"n": 528, "same_top": 527, "max_abs_dlogit_max": 0.6875}, "unedited_base_answer_read": {"n": 1056, "base_answer": 1056}}`; near ties: `{"n": 18365, "within_gap": 152, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-still | everything after the question | 17 | 6% [2, 12] | 94% [88, 98] | 3% [1, 8] | 2% [0, 5] | 0% [0, 3] |
| memory → prompt | e5-still | last two tokens before the answer | 21 | 95% [89, 98] | 5% [2, 11] | 11% [5, 17] | 25% [17, 33] | 43% [34, 52] |
| memory → prompt | e5-abs | everything after the question | 17 | 5% [1, 10] | 95% [90, 99] | 1% [0, 4] | 2% [0, 5] | 0% [0, 3] |
| memory → prompt | e5-abs | last two tokens before the answer | 21 | 94% [88, 97] | 6% [3, 12] | 14% [9, 21] | 25% [17, 33] | 38% [29, 46] |
| memory → prompt | e5-rel | everything after the question | 16 | 2% [0, 5] | 98% [95, 100] | 2% [0, 5] | 0% [0, 3] | 0% [0, 3] |
| memory → prompt | e5-rel | last two tokens before the answer | 21 | 96% [91, 99] | 4% [1, 9] | 11% [6, 18] | 24% [17, 32] | 45% [37, 54] |
| memory → prompt | e5-long | everything after the question | 17 | 3% [1, 8] | 97% [92, 99] | 2% [0, 5] | 1% [0, 4] | 0% [0, 3] |
| memory → prompt | e5-long | last two tokens before the answer | 21 | 98% [94, 100] | 2% [0, 6] | 11% [7, 18] | 26% [19, 34] | 48% [39, 56] |
| named → prompt | e5-still | everything after the question | 16 | 0% [0, 3] | 100% [97, 100] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] |
| named → prompt | e5-still | last two tokens before the answer | 21 | 100% [97, 100] | 0% [0, 3] | 3% [1, 8] | 8% [4, 14] | 86% [79, 92] |
| named → prompt | e5-abs | everything after the question | 16 | 0% [0, 3] | 100% [97, 100] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] |
| named → prompt | e5-abs | last two tokens before the answer | 21 | 99% [96, 100] | 1% [0, 4] | 4% [1, 9] | 7% [3, 12] | 86% [79, 92] |
| named → prompt | e5-rel | everything after the question | 16 | 0% [0, 3] | 100% [97, 100] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] |
| named → prompt | e5-rel | last two tokens before the answer | 21 | 99% [96, 100] | 1% [0, 4] | 3% [1, 8] | 10% [5, 16] | 85% [78, 91] |
| named → prompt | e5-long | everything after the question | 16 | 0% [0, 3] | 100% [97, 100] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] |
| named → prompt | e5-long | last two tokens before the answer | 21 | 100% [97, 100] | 0% [0, 3] | 2% [0, 5] | 5% [1, 10] | 94% [88, 98] |

## Pre-registered primary (pointer_v6): memory -> prompt, the last two tokens, layers 17 and 18 and 19, pooled

H-rel (Dan: a shift of the distance back from the question moves more answers than a shift of the place in the text): **does not hold**; H-abs (the opposite): **does not hold**; H-ordinal (the same slot beats the moved statement under both shifts): **holds**; H-long (Dan: long statements lower the same-slot share): **does not hold**.

| layer | n abs / rel | moved: abs (same place) | moved: rel (same distance back) | rel - abs [95%] | slot: abs / rel | slot: still / long | long - still [95%] |
|---|---|---|---|---|---|---|---|
| 17 | 132 / 132 | 9% [4, 15] | 12% [7, 19] | 3% [-5, 11] | 34% [26, 43] / 40% [32, 49] | 37% [29, 46] / 44% [36, 52] | 7% [-5, 18] |
| 18 | 132 / 132 | 13% [8, 20] | 12% [7, 19] | -1% [-9, 7] | 36% [28, 44] / 42% [34, 51] | 39% [30, 47] / 46% [38, 55] | 8% [-4, 19] |
| 19 | 132 / 132 | 10% [5, 16] | 10% [6, 16] | 0% [-7, 7] | 30% [22, 38] / 38% [29, 47] | 35% [26, 43] / 37% [28, 46] | 2% [-9, 14] |

## Agent priors in the job spec (jobs/d3/olmo3_7b_instruct_d3v6_swap.yaml `hypotheses`) vs results

- H-rel (Dan): as d3v6_swap_27b at layers 17, 18 or 19. Agents' prior 0.35
- H-abs: as d3v6_swap_27b. Prior 0.15
- H-ordinal: as d3v6_swap_27b. Prior 0.45
- H-long (Dan): as d3v6_swap_27b. Prior 0.4

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [0, 3], last two tokens 0% [0, 3] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 0% [0, 3] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 1% [0, 4] / 0% [0, 3] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 0% [0, 3] / 100% [97, 100] (>= 50%: met); first single layer where it reaches 20%: after the question None, last two tokens 19
- H-none: memory → prompt, answer changed after the question 1% [0, 4] (< 20%: met)

## Worked example (from examples.json)

Item `countries-RL-e5-rel-0140` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
Drawer 0 holds the China file. Drawer 5 holds the Hungary file. Drawer 7 holds the Lebanon file. Drawer 2 holds the Canada file. Drawer 9 holds the Sweden file. The lamp in the hall flickered.
What drawer keeps the file on the country whose capital is Stockholm? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Alt prompt:

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
Drawer 6 holds the Canada file. Drawer 2 holds the Hungary file. Drawer 7 holds the Sweden file. Drawer 0 holds the Lebanon file. Drawer 9 holds the China file.
What drawer keeps the file on the country whose capital is Ottawa? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Answers: answer org 9; after the patch 0. Predicted: answer org kept 9 (p 0.000); answer of bridge alt's statement 2 (p 0.000); answer at the same statement slot 0 (p 0.499); answer at the same distance back from the question 5 (p 0.000); the alt prompt's own answer 6 (p 0.499).

