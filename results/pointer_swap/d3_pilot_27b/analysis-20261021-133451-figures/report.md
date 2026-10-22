# D3 pilot (superseded: too few items for the rule)

Run `d3_pilot_27b` (results/pointer_swap/), analysis of the saved outputs only.

**NOT A HEADLINE RUN (superseded or smoke)**: pilot with 34 prompts per family: below 35 the rule's control bound cannot pass, so every cell reads 'damage'; includes topics that failed the competence check. Shown for completeness.

```
EXP d3_pilot_27b @ 2d90ce4 | model Qwen3.6-27B | n={"RL|e5f0": 34, "DL|e5f0": 34, "RR|e5f0": 34} | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in RL (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: RL, tokens after the question, transit window (e5f0): position = 9% [3, 23]   Baseline: none = 53% [37, 69], identity = 15% [6, 30], value = 24% [12, 40]   Control: 'same' changed = 0% [0, 10]; random direction changed (max over transit layers) = 3% [1, 15]; other item changed = 12% [5, 27]
Figures: results/pointer_swap/d3_pilot_27b/analysis-20261021-133451-figures/by_layer_e5f0.png, results/pointer_swap/d3_pilot_27b/analysis-20261021-133451-figures/slots_final_e5f0.png, results/pointer_swap/d3_pilot_27b/analysis-20261021-133451-figures/slots_last_e5f0.png, results/pointer_swap/d3_pilot_27b/analysis-20261021-133451-figures/windows_e5f0.png, results/pointer_swap/d3_pilot_27b/analysis-20261021-133451-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_pilot_27b/outcomes.jsonl, rows `family == 'memory → prompt'`, `group == 'final'`, `layer == 'transit'`, `source == 'alt prompt'`, `level == 'e5f0'`: count `role` (n=34); position should be 3, identity 5, value 8, none 18
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 3% [1, 15] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 10]; among alt prompt reads won by a predicted digit, 105/7654 have the runner-up prediction within p 0.1; hook checks self no-op 102/102, layer-0 reproduction 102/102.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "damage", "elements": "damage", "months": "damage", "planets": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **damage** (answer org kept 53% [37, 69], answer of bridge alt's statement 15% [6, 30], answer at the same statement slot 9% [3, 23], the alt prompt's own answer 24% [12, 40])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 1824, in cuts ['all', 'domain:animals', 'domain:elements', 'domain:months', 'domain:planets', 'slot:first', 'slot:last', 'slot:middle'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 85%) | damage (answer org kept 6%, answer of bridge alt's statement 76%) | damage (answer org kept 94%, answer of bridge alt's statement 3%) |
| memory → prompt | everything after the question | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 79%, answer of bridge alt's statement 12%) | damage (answer org kept 53%, the alt prompt's own answer 24%) |
| memory → prompt | last two tokens before the answer | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 97%, answer of bridge alt's statement 3%) | damage (answer org kept 29%, the alt prompt's own answer 41%) |
| memory → prompt | question words + everything after | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 85%) | damage (answer org kept 0%, answer of bridge alt's statement 82%) | damage (answer org kept 35%, answer of bridge alt's statement 26%) |
| named → prompt | question words | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 76%) | damage (answer org kept 0%, answer of bridge alt's statement 74%) | damage (answer org kept 38%, answer at the same statement slot 41%) |
| named → prompt | everything after the question | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, the alt prompt's own answer 74%) |
| named → prompt | last two tokens before the answer | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 82%, the alt prompt's own answer 12%) |
| named → prompt | question words + everything after | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 76%) | damage (answer org kept 0%, answer of bridge alt's statement 68%) | damage (answer org kept 0%, the alt prompt's own answer 68%) |
| memory → memory | question words | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 97%) | damage (answer org kept 6%, answer of bridge alt's statement 88%) | damage (answer org kept 91%, answer of bridge alt's statement 9%) |
| memory → memory | everything after the question | e5f0 | damage (answer org kept 97%, answer of bridge alt's statement 3%) | damage (answer org kept 94%, answer of bridge alt's statement 6%) | damage (answer org kept 65%, answer of bridge alt's statement 35%) |
| memory → memory | last two tokens before the answer | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 71%, answer of bridge alt's statement 29%) | damage (answer org kept 12%, answer of bridge alt's statement 88%) |
| memory → memory | question words + everything after | e5f0 | damage (answer org kept 0%, answer of bridge alt's statement 97%) | damage (answer org kept 0%, answer of bridge alt's statement 97%) | damage (answer org kept 35%, answer of bridge alt's statement 65%) |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 34 | 34 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 53% [37, 69], answer of bridge alt's statement 15% [6, 30], answer at the same statement slot 9% [3, 23], the alt prompt's own answer 24% [12, 40] |
| domain:animals | e5f0 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 27% [11, 52], answer of bridge alt's statement 7% [1, 30], answer at the same statement slot 13% [4, 38], the alt prompt's own answer 53% [30, 75] |
| domain:elements | e5f0 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 73% [48, 89], answer of bridge alt's statement 20% [7, 45], answer at the same statement slot 7% [1, 30], the alt prompt's own answer 0% [-0, 20] |
| domain:months | e5f0 | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 50% [9, 91], answer of bridge alt's statement 50% [9, 91], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 0% [0, 66] |
| domain:planets | e5f0 | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [34, 100], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 0% [0, 66] |
| slot:first | e5f0 | 11 | 11 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 73% [43, 90], answer of bridge alt's statement 18% [5, 48], answer at the same statement slot 0% [0, 26], the alt prompt's own answer 9% [2, 38] |
| slot:middle | e5f0 | 15 | 15 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 40% [20, 64], answer of bridge alt's statement 20% [7, 45], answer at the same statement slot 7% [1, 30], the alt prompt's own answer 33% [15, 58] |
| slot:last | e5f0 | 8 | 8 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 50% [22, 78], answer of bridge alt's statement 0% [0, 32], answer at the same statement slot 25% [7, 59], the alt prompt's own answer 25% [7, 59] |

## Checks

`{"self_noop": {"n": 102, "same_top": 102, "max_abs_dlogit_max": 1.125}, "layer0_all_reproduces_source": {"n": 102, "same_top": 102, "max_abs_dlogit_max": 1.0625}, "unedited_base_answer_read": {"n": 102, "base_answer": 102}}`; near ties: `{"n": 7654, "within_gap": 105, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | question words | 0 | 100% [90, 100] | 0% [0, 10] | 91% [77, 97] | 3% [1, 15] | 0% [0, 10] |
| memory → prompt | e5f0 | everything after the question | 48 | 38% [24, 55] | 62% [45, 76] | 18% [8, 34] | 21% [10, 37] | 0% [0, 10] |
| memory → prompt | e5f0 | last two tokens before the answer | 60 | 100% [90, 100] | 0% [0, 10] | 0% [0, 10] | 0% [0, 10] | 100% [90, 100] |
| memory → prompt | e5f0 | question words + everything after | 4 | 100% [90, 100] | 0% [0, 10] | 91% [77, 97] | 3% [1, 15] | 0% [0, 10] |
| named → prompt | e5f0 | question words | 0 | 100% [90, 100] | 0% [0, 10] | 100% [90, 100] | 0% [0, 10] | 0% [0, 10] |
| named → prompt | e5f0 | everything after the question | 56 | 100% [90, 100] | 0% [0, 10] | 0% [0, 10] | 0% [0, 10] | 100% [90, 100] |
| named → prompt | e5f0 | last two tokens before the answer | 60 | 100% [90, 100] | 0% [0, 10] | 0% [0, 10] | 0% [0, 10] | 100% [90, 100] |
| named → prompt | e5f0 | question words + everything after | 0 | 100% [90, 100] | 0% [0, 10] | 100% [90, 100] | 0% [0, 10] | 0% [0, 10] |
| memory → memory | e5f0 | question words | 0 | 100% [90, 100] | 0% [0, 10] | 97% [85, 99] | 0% [0, 10] | 0% [0, 10] |
| memory → memory | e5f0 | everything after the question | 48 | 21% [10, 37] | 79% [63, 90] | 21% [10, 37] | 0% [0, 10] | 0% [0, 10] |
| memory → memory | e5f0 | last two tokens before the answer | 60 | 100% [90, 100] | 0% [0, 10] | 100% [90, 100] | 0% [0, 10] | 0% [0, 10] |
| memory → memory | e5f0 | question words + everything after | 0 | 100% [90, 100] | 0% [0, 10] | 97% [85, 99] | 0% [0, 10] | 0% [0, 10] |

## Agent priors in the job spec (jobs/d3/d3_pilot_27b.yaml `hypotheses`) vs results

- H-pointer: memory → prompt, final (and last) at the transit window 44-52: answer at the same statement slot >= 50%, answer of bridge alt's statement <= 20%, the alt prompt's own answer <= 20%; memory → memory answer at the same statement slot <= 10% (answer of bridge alt's statement >= 50%); named → prompt answer at the same statement slot >= 50%
- H-word: memory → prompt final/last transit: answer of bridge alt's statement >= 50%, answer at the same statement slot <= 20%
- H-value: memory → prompt final/last transit: the alt prompt's own answer >= 50% (the source's digit, absent from the base)
- H-none: memory → prompt final transit changes the answer < 20% (would contradict the suite's copy flips; design mismatch)
- prior: Agent prior (before any run): question group answer of bridge alt's statement at layers <= 28 under every hypothesis (the cue words are patched); at 44-52 on final/last: the alt prompt's own answer 0.4, answer at the same statement slot 0.3, answer of bridge alt's statement 0.3. Mixing Mechanisms predicts answer at the same statement slot mainly for first/last slots and answer of bridge alt's statement (lexical) / reflexive in the middle: reported by slot.

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 9% [3, 23], last two tokens 18% [8, 34] (>= 50%: not met); memory → memory 0% [0, 10] / 0% [0, 10] (<= 10%: met); named → prompt after the question 24% [12, 40] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 15% [6, 30] / 12% [5, 27] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 24% [12, 40] / 41% [26, 58] (>= 50%: not met); first single layer where it reaches 20%: after the question 52, last two tokens 52
- H-none: memory → prompt, answer changed after the question 47% [31, 63] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e5f0-0014` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The lion's locker is 3. The spider's locker is 7. The turkey's locker is 6. The cow's locker is 9. The dog's locker is 1.
Which locker belongs to the animal known for barking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The spider's locker is 7. The turkey's locker is 5. The cow's locker is 1. The dog's locker is 9. The lion's locker is 3.
Which locker belongs to the animal known for gobbling? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 1; after the patch 7. Predicted: answer org kept 1 (p 0.020); answer of bridge alt's statement 6 (p 0.001); answer at the same statement slot 7 (p 0.964); the alt prompt's own answer 5 (p 0.004).

