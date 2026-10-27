# D3 v4: with many more entities and wordings, does the patch still carry bridge alt's statement slot rather than its word or answer?

Run `d3v4_swap_main` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements, 3 wordings per topic.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP d3v4_swap_main @ unknown | model Qwen3.6-27B | n per family = memory → prompt 450 items / 85 entities / 27 wordings (5 statements); named → prompt 450 items / 85 entities / 27 wordings (5 statements); memory → memory 450 items / 85 entities / 27 wordings (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 16% [12, 19]   Baseline: none = 72% [67, 77], identity = 4% [2, 6], value = 7% [5, 9]   Control: 'same' changed = 0% [0, 1]; random push of the same size changed (max over transit layers) = 0% [0, 1]; another domain's prompt changed = 7% [4, 10]
Figures: results/pointer_swap/d3v4_swap_main/analysis-20261021-163654-figures/by_layer_e5f0.png, results/pointer_swap/d3v4_swap_main/analysis-20261021-163654-figures/slots_final_e5f0.png, results/pointer_swap/d3v4_swap_main/analysis-20261021-163654-figures/slots_last_e5f0.png, results/pointer_swap/d3v4_swap_main/analysis-20261021-163654-figures/windows_e5f0.png, results/pointer_swap/d3v4_swap_main/analysis-20261021-163654-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v4_swap_main/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=450); position should be 70, identity 18, value 30, none 324
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 1] (max over transit layers); digits of the base context that no hypothesis predicts win 2% [1, 3]; among alt prompt reads won by a predicted digit, 648/34851 have the runner-up prediction within p 0.1; hook checks self no-op 1350/1350, layer-0 reproduction 1350/1350.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "none", "body": "mixed", "countries": "mixed"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **same statement slot (H-pointer)** (answer org kept 72% [67, 77], answer of bridge alt's statement 4% [2, 6], answer at the same statement slot 16% [12, 19], the alt prompt's own answer 7% [5, 9])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | - | - | - |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 92%, answer of bridge alt's statement 7%) | same statement slot (H-pointer) (answer org kept 72%, answer at the same statement slot 16%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 26%, the alt prompt's own answer 41%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words | e5f0 | - | - | - |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 18%, the alt prompt's own answer 45%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 86%, answer at the same statement slot 9%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |
| memory → memory | question words | e5f0 | - | - | - |
| memory → memory | everything after the question | e5f0 | no effect (answer org kept 99%, answer of bridge alt's statement 1%) | no effect (answer org kept 94%, answer of bridge alt's statement 6%) | bridge alt's statement (H-word) (answer org kept 64%, answer of bridge alt's statement 35%) |
| memory → memory | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 81%, answer of bridge alt's statement 19%) | bridge alt's statement (H-word) (answer org kept 7%, answer of bridge alt's statement 93%) |
| memory → memory | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 450 | 450 | same statement slot (H-pointer) | yes | answer org kept 72% [67, 77], answer of bridge alt's statement 4% [2, 6], answer at the same statement slot 16% [12, 19], the alt prompt's own answer 7% [5, 9] |
| domain:animals | e5f0 | 150 | 150 | no effect | yes | answer org kept 74% [65, 82], answer of bridge alt's statement 3% [1, 8], answer at the same statement slot 13% [8, 19], the alt prompt's own answer 7% [4, 13] |
| domain:body | e5f0 | 150 | 150 | mixed | yes | answer org kept 72% [63, 80], answer of bridge alt's statement 7% [3, 12], answer at the same statement slot 17% [12, 24], the alt prompt's own answer 1% [0, 5] |
| domain:countries | e5f0 | 150 | 150 | mixed | yes | answer org kept 70% [62, 77], answer of bridge alt's statement 2% [0, 6], answer at the same statement slot 17% [11, 23], the alt prompt's own answer 11% [6, 17] |
| slot:first | e5f0 | 85 | 85 | no effect | yes | answer org kept 84% [74, 92], answer of bridge alt's statement 4% [0, 10], answer at the same statement slot 5% [1, 11], the alt prompt's own answer 6% [1, 13] |
| slot:middle | e5f0 | 280 | 280 | same statement slot (H-pointer) | yes | answer org kept 70% [64, 75], answer of bridge alt's statement 4% [2, 7], answer at the same statement slot 16% [12, 21], the alt prompt's own answer 7% [4, 11] |
| slot:last | e5f0 | 85 | 85 | same statement slot (H-pointer) | yes | answer org kept 67% [57, 76], answer of bridge alt's statement 4% [0, 10], answer at the same statement slot 24% [15, 34], the alt prompt's own answer 6% [1, 13] |

## Checks

`{"self_noop": {"n": 1350, "same_top": 1350, "max_abs_dlogit_max": 3.125}, "layer0_all_reproduces_source": {"n": 1350, "same_top": 1350, "max_abs_dlogit_max": 1.75}, "unedited_base_answer_read": {"n": 1350, "base_answer": 1350}}`; near ties: `{"n": 34851, "within_gap": 648, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | everything after the question | 48 | 35% [31, 40] | 65% [60, 69] | 8% [6, 11] | 26% [22, 30] | 0% [0, 1] |
| memory → prompt | e5f0 | last two tokens before the answer | 56 | 99% [98, 100] | 1% [0, 2] | 0% [0, 1] | 0% [0, 1] | 99% [97, 100] |
| named → prompt | e5f0 | everything after the question | 56 | 88% [85, 91] | 12% [9, 15] | 0% [0, 1] | 0% [0, 1] | 88% [85, 91] |
| named → prompt | e5f0 | last two tokens before the answer | 56 | 87% [83, 90] | 13% [10, 17] | 0% [0, 1] | 0% [0, 1] | 87% [83, 90] |
| memory → memory | e5f0 | everything after the question | 48 | 34% [27, 40] | 66% [60, 73] | 33% [27, 39] | 0% [0, 1] | 0% [0, 1] |
| memory → memory | e5f0 | last two tokens before the answer | 56 | 99% [98, 100] | 1% [0, 2] | 99% [98, 100] | 0% [0, 1] | 0% [0, 1] |

## Agent priors in the job spec (jobs/d3/d3v4_swap_main.yaml `hypotheses`) vs results

- H-pointer: memory -> prompt, after the question, window 44-52, pooled: verdict "same statement slot" (its cluster lower bound above the word's and the answer's upper bounds and the random push); same slot 20-35%; in >= 2 of 3 topics; named -> prompt shows it too; memory -> memory same slot <= 5%
- H-word: verdict "bridge alt's statement" pooled (the word beats the slot once entities and wordings vary)
- H-mixed: no outcome separates under entity-cluster intervals (pooled verdict "mixed"), or the verdict holds in fewer than 2 of 3 topics (topic-dependent)
- H-value: the alt prompt's own answer already wins inside 44-52 (> 30% at layer 50 after the question)
- prior: Agent prior: H-pointer 0.35, H-mixed 0.35, H-word 0.2, H-the alt prompt's own answer 0.1 (pointer_v2's offset run, scored by the coordinator: last two tokens, layer 50, same slot 28% vs bridge alt's statement ~32%, after the question layer 48 17% vs 26%, so the slot-over-word margin may not survive).

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 16% [12, 19], last two tokens 27% [23, 31] (>= 50%: not met); memory → memory 0% [0, 1] / 0% [0, 1] (<= 10%: met); named → prompt after the question 28% [24, 32] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 4% [2, 6] / 5% [3, 7] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 7% [5, 9] / 41% [37, 46] (>= 50%: not met); first single layer where it reaches 20%: after the question 56, last two tokens 52
- H-none: memory → prompt, answer changed after the question 28% [23, 33] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RL-e5f0-0204` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 48 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The moth's locker is 5. The crow's locker is 1. The dog's locker is 9. The wolf's locker is 2. The spider's locker is 7.
Which locker belongs to the animal known for spinning webs? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The dog's locker is 3. The spider's locker is 9. The wolf's locker is 5. The crow's locker is 2. The moth's locker is 7.
Which locker belongs to the animal known for barking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 7; after the patch 5. Predicted: answer org kept 7 (p 0.003); answer of bridge alt's statement 9 (p 0.001); answer at the same statement slot 5 (p 0.992); the alt prompt's own answer 3 (p 0.000).

