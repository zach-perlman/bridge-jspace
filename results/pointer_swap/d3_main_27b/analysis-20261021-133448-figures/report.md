# D3 main, first version (superseded: included domains that failed the gate)

Run `d3_main_27b` (results/pointer_swap/), analysis of the saved outputs only.

**NOT A HEADLINE RUN (superseded or smoke)**: includes months and planets, whose memory → prompt / memory → memory prompts fail the pre-registered competence check (months memory → prompt 46%, planets memory → memory 55%, planets memory → prompt lower bound 0.84). Shown for completeness.

```
EXP d3_main_27b @ 3b8db6e | model Qwen3.6-27B | n={"RL|e5f0": 62, "DL|e5f0": 62, "RR|e5f0": 62} | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in RL (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: RL, tokens after the question, transit window (e5f0): position = 32% [22, 45]   Baseline: none = 42% [30, 54], identity = 13% [7, 23], value = 10% [5, 20]   Control: 'same' changed = 0% [-0, 6]; random direction changed (max over transit layers) = 3% [1, 11]; other item changed = 13% [7, 23]
Figures: results/pointer_swap/d3_main_27b/analysis-20261021-133448-figures/by_layer_e5f0.png, results/pointer_swap/d3_main_27b/analysis-20261021-133448-figures/slots_final_e5f0.png, results/pointer_swap/d3_main_27b/analysis-20261021-133448-figures/slots_last_e5f0.png, results/pointer_swap/d3_main_27b/analysis-20261021-133448-figures/windows_e5f0.png, results/pointer_swap/d3_main_27b/analysis-20261021-133448-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_main_27b/outcomes.jsonl, rows `family == 'memory → prompt'`, `group == 'final'`, `layer == 'transit'`, `source == 'alt prompt'`, `level == 'e5f0'`: count `role` (n=62); position should be 20, identity 8, value 6, none 26
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 3% [1, 11] (max over transit layers); digits of the base context that no hypothesis predicts win 2% [0, 9]; among alt prompt reads won by a predicted digit, 281/18991 have the runner-up prediction within p 0.1; hook checks self no-op 185/186, layer-0 reproduction 186/186.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "damage", "elements": "damage", "months": "damage", "planets": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **mixed** (answer org kept 42% [30, 54], answer of bridge alt's statement 13% [7, 23], answer at the same statement slot 32% [22, 45], the alt prompt's own answer 10% [5, 20])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 1872, in cuts ['domain:animals', 'domain:elements', 'domain:months', 'domain:planets', 'slot:first', 'slot:last'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 77%) | bridge alt's statement (H-word) (answer org kept 6%, answer of bridge alt's statement 66%) | no effect (answer org kept 95%, answer of bridge alt's statement 3%) |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 94%, answer of bridge alt's statement 2%) | no effect (answer org kept 82%, answer of bridge alt's statement 10%) | mixed (answer org kept 42%, answer at the same statement slot 32%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 97%, answer of bridge alt's statement 2%) | damage (answer org kept 97%, answer of bridge alt's statement 2%) | mixed (answer org kept 13%, the alt prompt's own answer 42%) |
| memory → prompt | question words + everything after | e5f0 | bridge alt's statement (H-word) (answer org kept 3%, answer of bridge alt's statement 79%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 71%) | same statement slot (H-pointer) (answer org kept 31%, answer at the same statement slot 40%) |
| named → prompt | question words | e5f0 | mixed (answer org kept 2%, answer of bridge alt's statement 50%) | mixed (answer org kept 0%, answer of bridge alt's statement 55%) | same statement slot (H-pointer) (answer org kept 42%, answer at the same statement slot 42%) |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 5%, the alt prompt's own answer 56%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 81%, answer at the same statement slot 16%) |
| named → prompt | question words + everything after | e5f0 | mixed (answer org kept 2%, answer of bridge alt's statement 50%) | mixed (answer org kept 0%, answer of bridge alt's statement 56%) | mixed (answer org kept 2%, the alt prompt's own answer 52%) |
| memory → memory | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 98%) | bridge alt's statement (H-word) (answer org kept 6%, answer of bridge alt's statement 90%) | no effect (answer org kept 95%, answer of bridge alt's statement 3%) |
| memory → memory | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 90%, answer of bridge alt's statement 10%) | no effect (answer org kept 74%, answer of bridge alt's statement 26%) |
| memory → memory | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 68%, answer of bridge alt's statement 31%) | bridge alt's statement (H-word) (answer org kept 5%, answer of bridge alt's statement 95%) |
| memory → memory | question words + everything after | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 98%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 95%) | bridge alt's statement (H-word) (answer org kept 37%, answer of bridge alt's statement 63%) |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 62 | 62 | mixed | yes | answer org kept 42% [30, 54], answer of bridge alt's statement 13% [7, 23], answer at the same statement slot 32% [22, 45], the alt prompt's own answer 10% [5, 20] |
| domain:animals | e5f0 | 25 | 25 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 36% [20, 55], answer of bridge alt's statement 8% [2, 25], answer at the same statement slot 32% [17, 52], the alt prompt's own answer 20% [9, 39] |
| domain:elements | e5f0 | 25 | 25 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 52% [34, 70], answer of bridge alt's statement 12% [4, 30], answer at the same statement slot 36% [20, 55], the alt prompt's own answer 0% [0, 13] |
| domain:months | e5f0 | 4 | 4 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 49], answer of bridge alt's statement 0% [0, 49], answer at the same statement slot 50% [15, 85], the alt prompt's own answer 25% [5, 70] |
| domain:planets | e5f0 | 8 | 8 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 50% [22, 78], answer of bridge alt's statement 38% [14, 69], answer at the same statement slot 12% [2, 47], the alt prompt's own answer 0% [0, 32] |
| slot:first | e5f0 | 14 | 14 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 36% [16, 61], answer of bridge alt's statement 29% [12, 55], answer at the same statement slot 14% [4, 40], the alt prompt's own answer 14% [4, 40] |
| slot:middle | e5f0 | 37 | 37 | mixed | yes | answer org kept 49% [33, 64], answer of bridge alt's statement 5% [2, 18], answer at the same statement slot 35% [22, 51], the alt prompt's own answer 11% [4, 25] |
| slot:last | e5f0 | 11 | 11 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 27% [10, 57], answer of bridge alt's statement 18% [5, 48], answer at the same statement slot 45% [21, 72], the alt prompt's own answer 0% [0, 26] |

## Checks

`{"self_noop": {"n": 186, "same_top": 185, "max_abs_dlogit_max": 0.7578}, "layer0_all_reproduces_source": {"n": 186, "same_top": 186, "max_abs_dlogit_max": 1.0}, "unedited_base_answer_read": {"n": 186, "base_answer": 185}}`; near ties: `{"n": 18991, "within_gap": 281, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | question words | 28 | 98% [91, 100] | 2% [0, 9] | 77% [66, 86] | 6% [3, 15] | 0% [-0, 6] |
| memory → prompt | e5f0 | everything after the question | 46 | 52% [39, 64] | 48% [36, 61] | 18% [10, 29] | 27% [18, 40] | 0% [-0, 6] |
| memory → prompt | e5f0 | last two tokens before the answer | 56 | 100% [94, 100] | 0% [-0, 6] | 3% [1, 11] | 3% [1, 11] | 92% [82, 97] |
| memory → prompt | e5f0 | question words + everything after | 24 | 98% [91, 100] | 2% [0, 9] | 89% [78, 94] | 3% [1, 11] | 0% [-0, 6] |
| named → prompt | e5f0 | question words | 16 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| named → prompt | e5f0 | everything after the question | 56 | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] | 0% [-0, 6] | 100% [94, 100] |
| named → prompt | e5f0 | last two tokens before the answer | 60 | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] | 0% [-0, 6] | 100% [94, 100] |
| named → prompt | e5f0 | question words + everything after | 16 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e5f0 | question words | 16 | 100% [94, 100] | 0% [-0, 6] | 98% [91, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e5f0 | everything after the question | 46 | 18% [10, 29] | 82% [71, 90] | 18% [10, 29] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e5f0 | last two tokens before the answer | 60 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e5f0 | question words + everything after | 16 | 100% [94, 100] | 0% [-0, 6] | 98% [91, 100] | 0% [-0, 6] | 0% [-0, 6] |

## Agent priors in the job spec (jobs/d3/d3_main_27b.yaml `hypotheses`) vs results

- H-pointer: memory → prompt final/last transit (44-52): answer at the same statement slot >= 50% [Wilson lower bound > answer of bridge alt's statement and the alt prompt's own answer upper bounds], memory → memory answer at the same statement slot <= 10%, named → prompt answer at the same statement slot >= 50%; by slot: answer at the same statement slot strongest for first/last, weaker in the middle
- H-word: memory → prompt final/last transit: answer of bridge alt's statement >= 50%, answer at the same statement slot <= 20%, the alt prompt's own answer <= 20%
- H-value: memory → prompt final/last transit: the alt prompt's own answer >= 50%; last group the alt prompt's own answer earlier (lower layer) than final
- H-none: memory → prompt final transit changes < 20%
- prior: Agent prior: the alt prompt's own answer 0.4, answer at the same statement slot 0.3, answer of bridge alt's statement 0.3 (to be updated by the pilot before enqueuing).

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 32% [22, 45], last two tokens 34% [23, 46] (>= 50%: not met); memory → memory 0% [-0, 6] / 0% [-0, 6] (<= 10%: met); named → prompt after the question 35% [25, 48] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 13% [7, 23] / 6% [3, 15] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 10% [5, 20] / 42% [30, 54] (>= 50%: not met); first single layer where it reaches 20%: after the question 56, last two tokens 52
- H-none: memory → prompt, answer changed after the question 58% [46, 70] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e5f0-0064` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 50 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The duck's locker is 6. The pig's locker is 3. The mouse's locker is 1. The frog's locker is 9. The spider's locker is 7.
Which locker belongs to the animal known for oinking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The spider's locker is 5. The frog's locker is 1. The mouse's locker is 6. The pig's locker is 9. The duck's locker is 3.
Which locker belongs to the animal known for spinning webs? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 3; after the patch 6. Predicted: answer org kept 3 (p 0.001); answer of bridge alt's statement 7 (p 0.000); answer at the same statement slot 6 (p 0.995); the alt prompt's own answer 5 (p 0.000).

