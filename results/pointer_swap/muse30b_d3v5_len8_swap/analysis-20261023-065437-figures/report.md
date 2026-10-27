# Finding 5 by the fixed rule on fresh 8-sentence lists (Muse Glimmer 30B, layers 26-48)

Run `muse30b_d3v5_len8_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e8-digit` = 8 statements, digit answers; `e8-word` = 8 statements, colour-word answers.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP muse30b_d3v5_len8_swap @ unknown | model Muse-Glimmer-30B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 36-42: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e8-digit): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/muse30b_d3v5_len8_swap/analysis-20261023-065437-figures/by_layer_e8-digit.png, results/pointer_swap/muse30b_d3v5_len8_swap/analysis-20261023-065437-figures/by_layer_e8-word.png, results/pointer_swap/muse30b_d3v5_len8_swap/analysis-20261023-065437-figures/slots_final_e8-digit.png, results/pointer_swap/muse30b_d3v5_len8_swap/analysis-20261023-065437-figures/slots_last_e8-digit.png, results/pointer_swap/muse30b_d3v5_len8_swap/analysis-20261023-065437-figures/windows_e8-digit.png, results/pointer_swap/muse30b_d3v5_len8_swap/analysis-20261023-065437-figures/domains_final_e8-digit.png, results/pointer_swap/muse30b_d3v5_len8_swap/analysis-20261023-065437-figures/levels_final.png, results/pointer_swap/muse30b_d3v5_len8_swap/analysis-20261023-065437-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/muse30b_d3v5_len8_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e8-digit'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 203/7818 have the runner-up prediction within p 0.1; hook checks self no-op 604/604, layer-0 reproduction 601/604.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e8-digit: **no data** (-); e8-word: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 120, in cuts ['slot:first', 'slot:last'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e8-digit | - | - | - |
| memory → prompt | question words | e8-word | - | - | - |
| memory → prompt | everything after the question | e8-digit | - | - | - |
| memory → prompt | everything after the question | e8-word | - | - | - |
| memory → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 6%, answer of bridge alt's statement 35%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | last two tokens before the answer | e8-word | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | mixed (answer org kept 11%, answer of bridge alt's statement 23%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 36%) |
| memory → prompt | question words + everything after | e8-digit | - | - | - |
| memory → prompt | question words + everything after | e8-word | - | - | - |
| named → prompt | question words | e8-digit | - | - | - |
| named → prompt | question words | e8-word | - | - | - |
| named → prompt | everything after the question | e8-digit | - | - | - |
| named → prompt | everything after the question | e8-word | - | - | - |
| named → prompt | last two tokens before the answer | e8-digit | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 15%, answer at the same statement slot 35%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e8-word | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 48%, answer at the same statement slot 24%) | alt prompt's own answer (H-value) (answer org kept 11%, the alt prompt's own answer 72%) |
| named → prompt | question words + everything after | e8-digit | - | - | - |
| named → prompt | question words + everything after | e8-word | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 604, "same_top": 604, "max_abs_dlogit_max": 2.666}, "layer0_all_reproduces_source": {"n": 604, "same_top": 601, "max_abs_dlogit_max": 4.3047}, "unedited_base_answer_read": {"n": 604, "base_answer": 604}}`; near ties: `{"n": 7818, "within_gap": 203, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e8-digit | last two tokens before the answer | 40 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 2% [0, 6] | 98% [94, 100] |
| memory → prompt | e8-word | last two tokens before the answer | 44 | 100% [98, 100] | 0% [0, 2] | 1% [0, 4] | 0% [0, 2] | 84% [77, 90] |
| named → prompt | e8-digit | last two tokens before the answer | 36 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 100% [98, 100] |
| named → prompt | e8-word | last two tokens before the answer | 44 | 100% [98, 100] | 0% [0, 2] | 0% [0, 2] | 0% [0, 2] | 99% [96, 100] |

## Pre-registered primary (pointer_v5): memory -> prompt, the last two tokens, layers 26 and 28 and 30 and 32 and 34 and 36 and 38 and 40 and 42 and 44 and 46 and 48: does each layout keep the statement slot?

| layout | keeps the slot | per layer: pooled verdict, topics with the slot |
|---|---|---|
| 8 statements, digits | **no** | 26: none, 0/3; 28: none, 0/3; 30: identity, 0/3; 32: mixed, 0/3; 34: mixed, 0/3; 36: value, 0/3; 38: value, 0/3; 40: value, 0/3; 42: value, 0/3; 44: value, 0/3; 46: value, 0/3; 48: value, 0/3 |
| 8 statements, colour words | **no** | 26: none, 0/3; 28: none, 0/3; 30: mixed, 0/3; 32: mixed, 0/3; 34: mixed, 0/3; 36: mixed, 0/3; 38: mixed, 0/3; 40: value, 0/3; 42: value, 0/3; 44: value, 0/3; 46: value, 0/3; 48: value, 0/3 |

## Agent priors in the job spec (jobs/d3/muse30b_d3v5_len8_swap.yaml `hypotheses`) vs results

- H-A: e8-digit: answer at the same statement slot - answer of bridge alt's statement (1st and 2nd) has its entity-cluster 95% lower bound > 0. Prior 0.75 (agent's) (copied from qwen35_9b_d3v5_len8_swap)
- H-B: e8-digit: answer of bridge alt's statement - answer at the same statement slot (3rd-8th) >= 0 with lower bound >= -0.05. Prior 0.6 (agent's) (copied from qwen35_9b_d3v5_len8_swap)
- H-word: e8-word gets the same verdict as e8-digit (reported, not decisive). Prior 0.5 (agent's) (copied from qwen35_9b_d3v5_len8_swap)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 2% [0, 6] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 0% [0, 2] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 98% [94, 100] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 36
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e8-word-0093` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 40 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-23.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The blue locker belongs to the bear. The red locker belongs to the chicken. The grey locker belongs to the spider. The yellow locker belongs to the horse. The orange locker belongs to the eagle. The white locker belongs to the deer. The green locker belongs to the snake. The black locker belongs to the worm.
Which colour is the locker that belongs to the animal known for clucking? Answer with a single word and nothing else.<|eot|><|start|>assistantAnswer: 
```

Alt prompt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-23.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The purple locker belongs to the spider. The red locker belongs to the horse. The orange locker belongs to the deer. The yellow locker belongs to the chicken. The grey locker belongs to the eagle. The blue locker belongs to the snake. The black locker belongs to the bear. The pink locker belongs to the worm.
Which colour is the locker that belongs to the animal known for spinning webs? Answer with a single word and nothing else.<|eot|><|start|>assistantAnswer: 
```

Answers: answer org red; after the patch blue. Predicted: answer org kept red (p 0.002); answer of bridge alt's statement grey (p 0.000); answer at the same statement slot blue (p 0.474); the alt prompt's own answer purple (p 0.088).

