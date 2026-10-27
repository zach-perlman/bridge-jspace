# Reproduction: d3v4_swap_topics at layer 50 from the job's clean checkout, same seeds (numbers should match)

Run `d3v4_swap_topics_repro` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements, 3 wordings per topic.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP d3v4_swap_topics_repro @ unknown | model Qwen3.6-27B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/d3v4_swap_topics_repro/analysis-20261021-214834-figures/by_layer_e5f0.png, results/pointer_swap/d3v4_swap_topics_repro/analysis-20261021-214834-figures/slots_final_e5f0.png, results/pointer_swap/d3v4_swap_topics_repro/analysis-20261021-214834-figures/slots_last_e5f0.png, results/pointer_swap/d3v4_swap_topics_repro/analysis-20261021-214834-figures/windows_e5f0.png, results/pointer_swap/d3v4_swap_topics_repro/analysis-20261021-214834-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v4_swap_topics_repro/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 145/9021 have the runner-up prediction within p 0.1; hook checks self no-op 2286/2286, layer-0 reproduction 2286/2286.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | - | - | - |
| memory → prompt | everything after the question | e5f0 | - | - | - |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 25%, the alt prompt's own answer 42%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words | e5f0 | - | - | - |
| named → prompt | everything after the question | e5f0 | - | - | - |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 84%, answer at the same statement slot 10%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |
| memory → memory | question words | e5f0 | - | - | - |
| memory → memory | everything after the question | e5f0 | - | - | - |
| memory → memory | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 78%, answer of bridge alt's statement 21%) | bridge alt's statement (H-word) (answer org kept 7%, answer of bridge alt's statement 92%) |
| memory → memory | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 2286, "same_top": 2286, "max_abs_dlogit_max": 2.75}, "layer0_all_reproduces_source": {"n": 2286, "same_top": 2286, "max_abs_dlogit_max": 6.6875}, "unedited_base_answer_read": {"n": 2286, "base_answer": 2286}}`; near ties: `{"n": 9021, "within_gap": 145, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | last two tokens before the answer | 50 | 83% [80, 86] | 17% [14, 20] | 22% [19, 25] | 51% [47, 54] | 0% [0, 0] |
| named → prompt | e5f0 | last two tokens before the answer | 50 | 48% [44, 51] | 52% [49, 56] | 12% [10, 14] | 32% [28, 36] | 0% [0, 0] |
| memory → memory | e5f0 | last two tokens before the answer | 50 | 81% [78, 84] | 19% [16, 22] | 81% [78, 83] | 1% [0, 1] | 0% [0, 0] |

## Agent priors in the job spec (jobs/d3/d3v4_swap_topics_repro.yaml `hypotheses`) vs results

- H-same: the same sampled items; per item the same role at layer 50 for >= 98% of items (bf16 noise), and the pooled shares within 1 point. Prior 0.85

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 26% [23, 30] (>= 50%: not met); memory → memory nan% [nan, nan] / 0% [0, 0] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 5% [4, 7] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 42% [39, 46] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens None
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

