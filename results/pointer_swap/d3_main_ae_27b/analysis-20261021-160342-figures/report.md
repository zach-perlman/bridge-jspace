# D3 main: word or pointer? (animals and elements, 100 scenes per family)

Run `d3_main_ae_27b` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements.

```
EXP d3_main_ae_27b @ 9a100de | model Qwen3.6-27B | n per family = memory → prompt 100 (5 statements); named → prompt 100 (5 statements); memory → memory 100 (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 29% [21, 39]   Baseline: none = 49% [39, 59], identity = 9% [5, 16], value = 12% [7, 20]   Control: 'same' changed = 0% [0, 4]; random push of the same size changed (max over transit layers) = 0% [0, 4]; another domain's prompt changed = 11% [6, 19]
Figures: results/pointer_swap/d3_main_ae_27b/analysis-20261021-160342-figures/by_layer_e5f0.png, results/pointer_swap/d3_main_ae_27b/analysis-20261021-160342-figures/slots_final_e5f0.png, results/pointer_swap/d3_main_ae_27b/analysis-20261021-160342-figures/slots_last_e5f0.png, results/pointer_swap/d3_main_ae_27b/analysis-20261021-160342-figures/windows_e5f0.png, results/pointer_swap/d3_main_ae_27b/analysis-20261021-160342-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_main_ae_27b/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=100); position should be 29, identity 9, value 12, none 49
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 4] (max over transit layers); digits of the base context that no hypothesis predicts win 1% [0, 5]; among alt prompt reads won by a predicted digit, 371/30926 have the runner-up prediction within p 0.1; hook checks self no-op 300/300, layer-0 reproduction 300/300.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "mixed", "elements": "mixed"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **same statement slot (H-pointer)** (answer org kept 49% [39, 59], answer of bridge alt's statement 9% [5, 16], answer at the same statement slot 29% [21, 39], the alt prompt's own answer 12% [7, 20])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 624, in cuts ['slot:first', 'slot:last'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 1%, answer of bridge alt's statement 90%) | bridge alt's statement (H-word) (answer org kept 7%, answer of bridge alt's statement 73%) | no effect (answer org kept 97%, answer of bridge alt's statement 1%) |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 84%, answer of bridge alt's statement 12%) | same statement slot (H-pointer) (answer org kept 49%, answer at the same statement slot 29%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer at the same statement slot 1%) | mixed (answer org kept 18%, the alt prompt's own answer 46%) |
| memory → prompt | question words + everything after | e5f0 | bridge alt's statement (H-word) (answer org kept 1%, answer of bridge alt's statement 89%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 75%) | same statement slot (H-pointer) (answer org kept 35%, answer at the same statement slot 37%) |
| named → prompt | question words | e5f0 | mixed (answer org kept 2%, answer of bridge alt's statement 55%) | mixed (answer org kept 2%, answer of bridge alt's statement 56%) | same statement slot (H-pointer) (answer org kept 30%, answer at the same statement slot 47%) |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 66%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 84%, answer at the same statement slot 12%) |
| named → prompt | question words + everything after | e5f0 | mixed (answer org kept 2%, answer of bridge alt's statement 56%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 58%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 60%) |
| memory → memory | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) | bridge alt's statement (H-word) (answer org kept 6%, answer of bridge alt's statement 91%) | no effect (answer org kept 94%, answer of bridge alt's statement 5%) |
| memory → memory | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 92%, answer of bridge alt's statement 8%) | bridge alt's statement (H-word) (answer org kept 71%, answer of bridge alt's statement 29%) |
| memory → memory | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 66%, answer of bridge alt's statement 33%) | bridge alt's statement (H-word) (answer org kept 1%, answer of bridge alt's statement 99%) |
| memory → memory | question words + everything after | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 98%) | bridge alt's statement (H-word) (answer org kept 39%, answer of bridge alt's statement 61%) |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 100 | 100 | same statement slot (H-pointer) | yes | answer org kept 49% [39, 59], answer of bridge alt's statement 9% [5, 16], answer at the same statement slot 29% [21, 39], the alt prompt's own answer 12% [7, 20] |
| domain:animals | e5f0 | 50 | 50 | mixed | yes | answer org kept 30% [19, 44], answer of bridge alt's statement 10% [4, 21], answer at the same statement slot 34% [22, 48], the alt prompt's own answer 24% [14, 37] |
| domain:elements | e5f0 | 50 | 50 | mixed | yes | answer org kept 68% [54, 79], answer of bridge alt's statement 8% [3, 19], answer at the same statement slot 24% [14, 37], the alt prompt's own answer 0% [0, 7] |
| slot:first | e5f0 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 53% [30, 75], answer of bridge alt's statement 20% [7, 45], answer at the same statement slot 13% [4, 38], the alt prompt's own answer 7% [1, 30] |
| slot:middle | e5f0 | 61 | 61 | mixed | yes | answer org kept 51% [39, 63], answer of bridge alt's statement 7% [3, 16], answer at the same statement slot 28% [18, 40], the alt prompt's own answer 15% [8, 26] |
| slot:last | e5f0 | 24 | 24 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 42% [24, 61], answer of bridge alt's statement 8% [2, 26], answer at the same statement slot 42% [24, 61], the alt prompt's own answer 8% [2, 26] |

## Checks

`{"self_noop": {"n": 300, "same_top": 300, "max_abs_dlogit_max": 0.625}, "layer0_all_reproduces_source": {"n": 300, "same_top": 300, "max_abs_dlogit_max": 1.0}, "unedited_base_answer_read": {"n": 300, "base_answer": 300}}`; near ties: `{"n": 30926, "within_gap": 371, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | question words | 18 | 100% [96, 100] | 0% [0, 4] | 95% [89, 98] | 1% [0, 5] | 0% [0, 4] |
| memory → prompt | e5f0 | everything after the question | 46 | 48% [38, 58] | 52% [42, 62] | 18% [12, 27] | 27% [19, 36] | 0% [0, 4] |
| memory → prompt | e5f0 | last two tokens before the answer | 60 | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 100% [96, 100] |
| memory → prompt | e5f0 | question words + everything after | 16 | 100% [96, 100] | 0% [0, 4] | 95% [89, 98] | 1% [0, 5] | 0% [0, 4] |
| named → prompt | e5f0 | question words | 16 | 100% [96, 100] | 0% [0, 4] | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] |
| named → prompt | e5f0 | everything after the question | 56 | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 100% [96, 100] |
| named → prompt | e5f0 | last two tokens before the answer | 60 | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 100% [96, 100] |
| named → prompt | e5f0 | question words + everything after | 16 | 100% [96, 100] | 0% [0, 4] | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] |
| memory → memory | e5f0 | question words | 16 | 100% [96, 100] | 0% [0, 4] | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] |
| memory → memory | e5f0 | everything after the question | 46 | 23% [16, 32] | 77% [68, 84] | 23% [16, 32] | 0% [0, 4] | 0% [0, 4] |
| memory → memory | e5f0 | last two tokens before the answer | 56 | 100% [96, 100] | 0% [0, 4] | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] |
| memory → memory | e5f0 | question words + everything after | 16 | 100% [96, 100] | 0% [0, 4] | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] |

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D3) vs results

Shares are answer of bridge alt's statement / answer at the same statement slot / the alt prompt's own answer / answer org kept, in % of prompts.

| question | Dan | result (this run unless said) | reading |
|---|---|---|---|
| Q3.1 memory → prompt with 5 statements >= 80%? | yes, >= 95% | org prompt answered (main, first 100 per topic): animals 98% [93, 99]; planets 91% [84, 95]; elements 94% [88, 97]; months 46% [37, 56] | partly: >= 80% for 3 of 4 topics; >= 95% only for animals; months fail |
| Q3.2 memory → prompt, patch the question words: shares at the strongest layer | 60 / 10 / 10 / 20 | layer 18: 95 / 1 / 0 / 0 | direction right (answer of bridge alt's statement), more extreme; from layer 40 on the question words carry nothing (layers 44-52: answer org kept 97%) |
| Q3.3 memory → prompt, patch only the last tokens | 80 / 10 / 5 / 5 | strongest layer 60: 0 / 0 / 100 / 0; at layer 50: 25 / 53 / 0 / 14 | wrong: the last tokens give the answer at the same statement slot (layer 50), then the alt prompt's own answer (52+); answer of bridge alt's statement never above ~25% |
| Q3.4 does it depend on where bridge org's statement sits? | no | memory → prompt, everything after the question, layers 44-52: first n=15 answer at the same statement slot 13% [4, 38]; middle n=61 answer at the same statement slot 28% [18, 40]; last n=24 answer at the same statement slot 42% [24, 61] | undetermined: first/last panels have n < 35 (the rule cannot pass); first is lowest, not highest as Mixing Mechanisms predicts |
| Q3.5 memory → memory (a pointer is useless) | 85 / 5 / 5 / 5 | question words, layer 16: 100 / 0 / 0 / 0; last two tokens, layers 44-52: answer of bridge alt's statement 99% [95, 100], answer at the same statement slot 0% [0, 4] | right: answer of bridge alt's statement (here the same digit as the alt prompt's own answer); answer at the same statement slot ~0 everywhere |
| Q3.5 named → prompt (direct question) | 80 / 5 / 5 / 10 | question words, layer 16: 100 / 0 / 0 / 0; question words, layer 44: answer at the same statement slot 47%; everything after the question, layer 50: 20 / 53 / 0 / 20 | partly wrong: from layer 28 the question words give the answer at the same statement slot for ~40% of prompts, and the tokens after the question give it before the alt prompt's own answer |
| Q3.6 what the lens reads but cannot steer | the word dominates; the statement's slot has little effect | memory → prompt, everything after the question, layers 44-52: 9 / 29 / 12 / 49 | contradicted at 44-52: the bridge is no longer on the question words; the tokens after the question carry a pointer to the statement's slot (answer at the same statement slot, more than answer of bridge alt's statement), then the answer itself; pooled verdict 'same statement slot', but 'mixed' for each topic alone |

## Agent priors in the job spec (jobs/d3/d3_main_ae_27b.yaml `hypotheses`) vs results

- H-pointer: memory → prompt final/last transit (44-52): answer at the same statement slot >= 50% [Wilson lower bound > answer of bridge alt's statement and the alt prompt's own answer upper bounds], memory → memory answer at the same statement slot <= 10%, named → prompt answer at the same statement slot >= 50%; by slot: answer at the same statement slot strongest for first/last, weaker in the middle
- H-word: memory → prompt final/last transit: answer of bridge alt's statement >= 50%, answer at the same statement slot <= 20%, the alt prompt's own answer <= 20%
- H-value: memory → prompt final/last transit: the alt prompt's own answer >= 50%; last group the alt prompt's own answer earlier (lower layer) than final
- H-none: memory → prompt final transit changes < 20%
- prior: Agent prior: the alt prompt's own answer 0.4, answer at the same statement slot 0.3, answer of bridge alt's statement 0.3 (to be updated by the pilot before enqueuing).

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 29% [21, 39], last two tokens 28% [20, 37] (>= 50%: not met); memory → memory 0% [0, 4] / 0% [0, 4] (<= 10%: met); named → prompt after the question 29% [21, 39] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 9% [5, 16] / 6% [3, 12] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 12% [7, 20] / 46% [37, 56] (>= 50%: not met); first single layer where it reaches 20%: after the question 56, last two tokens 52
- H-none: memory → prompt, answer changed after the question 51% [41, 61] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e5f0-0088` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 48 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The turkey's locker is 9. The chicken's locker is 1. The bee's locker is 3. The lion's locker is 8. The frog's locker is 7.
Which locker belongs to the animal known for its roar? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The lion's locker is 8. The frog's locker is 9. The turkey's locker is 5. The bee's locker is 7. The chicken's locker is 3.
Which locker belongs to the animal known for gobbling? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 8; after the patch 3. Predicted: answer org kept 8 (p 0.034); answer of bridge alt's statement 9 (p 0.000); answer at the same statement slot 3 (p 0.867); the alt prompt's own answer 5 (p 0.000).

