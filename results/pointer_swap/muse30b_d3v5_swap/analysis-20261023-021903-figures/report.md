# Muse Glimmer 30B: pointer_v5 (the label's counting / 8 sentences and colour words / shifts)

Run `muse30b_d3v5_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-digit` = 5 statements, digit answers; `e5-word` = 5 statements, colour-word answers; `e8-digit` = 8 statements, digit answers; `e8-word` = 8 statements, colour-word answers.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP muse30b_d3v5_swap @ unknown | model Muse-Glimmer-30B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 36-42: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-digit): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/by_layer_e5-digit.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/by_layer_e5-word.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/by_layer_e8-digit.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/by_layer_e8-word.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/slots_final_e5-digit.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/slots_last_e5-digit.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/windows_e5-digit.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/domains_final_e5-digit.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/levels_final.png, results/pointer_swap/muse30b_d3v5_swap/analysis-20261023-021903-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/muse30b_d3v5_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-digit'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 540/18168 have the runner-up prediction within p 0.1; hook checks self no-op 1384/1388, layer-0 reproduction 1382/1388.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-digit: **no data** (-); e5-word: **no data** (-); e8-digit: **no data** (-); e8-word: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 180, in cuts ['slot:first', 'slot:last'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-digit | - | - | - |
| memory → prompt | question words | e5-word | - | - | - |
| memory → prompt | question words | e8-digit | - | - | - |
| memory → prompt | question words | e8-word | - | - | - |
| memory → prompt | everything after the question | e5-digit | - | - | - |
| memory → prompt | everything after the question | e5-word | - | - | - |
| memory → prompt | everything after the question | e8-digit | - | - | - |
| memory → prompt | everything after the question | e8-word | - | - | - |
| memory → prompt | last two tokens before the answer | e5-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 7%, answer at the same statement slot 48%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 99%) |
| memory → prompt | last two tokens before the answer | e5-word | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 18%, answer at the same statement slot 40%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 20%) |
| memory → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 6%, answer of bridge alt's statement 39%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| memory → prompt | last two tokens before the answer | e8-word | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 9%, answer at the same statement slot 27%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 31%) |
| memory → prompt | question words + everything after | e5-digit | - | - | - |
| memory → prompt | question words + everything after | e5-word | - | - | - |
| memory → prompt | question words + everything after | e8-digit | - | - | - |
| memory → prompt | question words + everything after | e8-word | - | - | - |
| named → prompt | question words | e5-digit | - | - | - |
| named → prompt | question words | e5-word | - | - | - |
| named → prompt | question words | e8-digit | - | - | - |
| named → prompt | question words | e8-word | - | - | - |
| named → prompt | everything after the question | e5-digit | - | - | - |
| named → prompt | everything after the question | e5-word | - | - | - |
| named → prompt | everything after the question | e8-digit | - | - | - |
| named → prompt | everything after the question | e8-word | - | - | - |
| named → prompt | last two tokens before the answer | e5-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 13%, answer at the same statement slot 51%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5-word | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 41%, answer at the same statement slot 42%) | alt prompt's own answer (H-value) (answer org kept 13%, the alt prompt's own answer 68%) |
| named → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 16%, answer of bridge alt's statement 31%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e8-word | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 39%, answer at the same statement slot 28%) | alt prompt's own answer (H-value) (answer org kept 6%, the alt prompt's own answer 77%) |
| named → prompt | question words + everything after | e5-digit | - | - | - |
| named → prompt | question words + everything after | e5-word | - | - | - |
| named → prompt | question words + everything after | e8-digit | - | - | - |
| named → prompt | question words + everything after | e8-word | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 1388, "same_top": 1384, "max_abs_dlogit_max": 2.0}, "layer0_all_reproduces_source": {"n": 1388, "same_top": 1382, "max_abs_dlogit_max": 3.9375}, "unedited_base_answer_read": {"n": 1388, "base_answer": 1386}}`; near ties: `{"n": 18168, "within_gap": 540, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-digit | last two tokens before the answer | 36 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 1% [0, 3] | 98% [95, 100] |
| memory → prompt | e5-word | last two tokens before the answer | 44 | 100% [98, 100] | 0% [0, 2] | 1% [0, 4] | 0% [0, 2] | 78% [71, 84] |
| memory → prompt | e8-digit | last two tokens before the answer | 36 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 2% [0, 5] | 98% [95, 100] |
| memory → prompt | e8-word | last two tokens before the answer | 48 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 1% [0, 3] | 97% [93, 99] |
| named → prompt | e5-digit | last two tokens before the answer | 36 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 1% [0, 3] | 99% [97, 100] |
| named → prompt | e5-word | last two tokens before the answer | 48 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 100% [98, 100] |
| named → prompt | e8-digit | last two tokens before the answer | 36 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 1% [0, 3] | 99% [97, 100] |
| named → prompt | e8-word | last two tokens before the answer | 44 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 100% [98, 100] |

## Pre-registered primary (pointer_v5): memory -> prompt, the last two tokens, layers 26 and 28 and 30 and 32 and 34 and 36 and 38 and 40 and 42 and 44 and 46 and 48: does each layout keep the statement slot?

| layout | keeps the slot | per layer: pooled verdict, topics with the slot |
|---|---|---|
| 5 statements, digits | **no** | 26: none, 0/3; 28: none, 0/3; 30: identity, 0/3; 32: position, 1/3; 34: position, 1/3; 36: value, 0/3; 38: value, 0/3; 40: value, 0/3; 42: value, 0/3; 44: value, 0/3; 46: value, 0/3; 48: value, 0/3 |
| 5 statements, colour words | **no** | 26: none, 0/3; 28: none, 0/3; 30: mixed, 0/3; 32: position, 1/3; 34: position, 1/3; 36: position, 0/3; 38: mixed, 0/3; 40: mixed, 0/3; 42: value, 0/3; 44: value, 0/3; 46: value, 0/3; 48: value, 0/3 |
| 8 statements, digits | **no** | 26: none, 0/3; 28: none, 0/3; 30: identity, 0/3; 32: mixed, 0/3; 34: mixed, 0/3; 36: value, 0/3; 38: value, 0/3; 40: value, 0/3; 42: value, 0/3; 44: value, 0/3; 46: value, 0/3; 48: value, 0/3 |
| 8 statements, colour words | **no** | 26: none, 0/3; 28: none, 0/3; 30: mixed, 0/3; 32: mixed, 0/3; 34: damage, 0/3; 36: mixed, 0/3; 38: mixed, 0/3; 40: value, 0/3; 42: value, 0/3; 44: value, 0/3; 46: value, 0/3; 48: value, 0/3 |

## Agent priors in the job spec (jobs/d3/muse30b_d3v5_swap.yaml `hypotheses`) vs results

- H-as-others: the same verdicts as Qwen3.5-9B / OLMo / Gemma. Prior 0.5

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 1% [0, 3] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 0% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 99% [96, 100] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 36
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

