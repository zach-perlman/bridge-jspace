# D3 in Python code: does the patched query carry the key, the dict entry's position, or the value?

Run `d3_code_main` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 dict entries.

```
EXP d3_code_main @ ca14894 | model Qwen3.6-27B | n per family = named → prompt 120 (5 statements); list position → prompt 120 (5 statements); 2-variable chain → prompt 120 (5 statements); 3-variable chain → prompt 120 (5 statements); memory → prompt 120 (5 statements); memory → memory 120 (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 20% [14, 28]   Baseline: none = 52% [43, 60], identity = 3% [1, 8], value = 24% [17, 33]   Control: 'same' changed = 1% [0, 5]; random push of the same size changed (max over transit layers) = 1% [0, 5]; another domain's prompt changed = 5% [2, 10]
Figures: results/pointer_swap/d3_code_main/analysis-20261021-162834-figures/by_layer_e5f0.png, results/pointer_swap/d3_code_main/analysis-20261021-162834-figures/slots_final_e5f0.png, results/pointer_swap/d3_code_main/analysis-20261021-162834-figures/slots_last_e5f0.png, results/pointer_swap/d3_code_main/analysis-20261021-162834-figures/windows_e5f0.png, results/pointer_swap/d3_code_main/analysis-20261021-162834-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_code_main/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=120); position should be 24, identity 4, value 29, none 62
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 1% [0, 5] (max over transit layers); digits of the base context that no hypothesis predicts win 1% [0, 5]; among alt prompt reads won by a predicted digit, 549/33156 have the runner-up prediction within p 0.1; hook checks self no-op 720/720, layer-0 reproduction 718/720.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "mixed", "months": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **mixed** (answer org kept 52% [43, 60], answer of bridge alt's statement 3% [1, 8], answer at the same statement slot 20% [14, 28], the alt prompt's own answer 24% [17, 33])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 846, in cuts ['domain:months', 'slot:first', 'slot:last'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| named → prompt | question words | e5f0 | mixed (answer org kept 1%, answer of bridge alt's statement 52%) | - | - |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 26%, the alt prompt's own answer 73%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 83%, the alt prompt's own answer 17%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |
| list position → prompt | question words | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | - | - |
| list position → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 87%, the alt prompt's own answer 10%) |
| list position → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 95%, answer at the same statement slot 3%) | alt prompt's own answer (H-value) (answer org kept 40%, the alt prompt's own answer 37%) |
| list position → prompt | question words + everything after | e5f0 | - | - | - |
| 2-variable chain → prompt | question words | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | - | - |
| 2-variable chain → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 74%, the alt prompt's own answer 26%) |
| 2-variable chain → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 1%) | alt prompt's own answer (H-value) (answer org kept 34%, the alt prompt's own answer 58%) |
| 2-variable chain → prompt | question words + everything after | e5f0 | - | - | - |
| 3-variable chain → prompt | question words | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | - | - |
| 3-variable chain → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 90%, the alt prompt's own answer 10%) |
| 3-variable chain → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 18%, the alt prompt's own answer 69%) |
| 3-variable chain → prompt | question words + everything after | e5f0 | - | - | - |
| memory → prompt | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 3%, answer of bridge alt's statement 88%) | - | - |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 94%, answer of bridge alt's statement 3%) | mixed (answer org kept 52%, the alt prompt's own answer 24%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 40%, the alt prompt's own answer 39%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| memory → memory | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 90%) | - | - |
| memory → memory | everything after the question | e5f0 | no effect (answer org kept 96%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 0%) | no effect (answer org kept 89%, answer of bridge alt's statement 8%) |
| memory → memory | last two tokens before the answer | e5f0 | no effect (answer org kept 95%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 26%, answer of bridge alt's statement 56%) | bridge alt's statement (H-word) (answer org kept 10%, answer of bridge alt's statement 88%) |
| memory → memory | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 120 | 120 | mixed | yes | answer org kept 52% [43, 60], answer of bridge alt's statement 3% [1, 8], answer at the same statement slot 20% [14, 28], the alt prompt's own answer 24% [17, 33] |
| domain:animals | e5f0 | 100 | 100 | mixed | yes | answer org kept 49% [39, 59], answer of bridge alt's statement 2% [1, 7], answer at the same statement slot 19% [13, 28], the alt prompt's own answer 29% [21, 39] |
| domain:months | e5f0 | 20 | 20 | damage (1 same-entity control changes) | NO (n < 35) | answer org kept 65% [43, 82], answer of bridge alt's statement 10% [3, 30], answer at the same statement slot 25% [11, 47], the alt prompt's own answer 0% [-0, 16] |
| slot:first | e5f0 | 33 | 33 | damage (1 same-entity control changes) | NO (n < 35) | answer org kept 58% [41, 73], answer of bridge alt's statement 9% [3, 24], answer at the same statement slot 0% [0, 10], the alt prompt's own answer 30% [17, 47] |
| slot:middle | e5f0 | 57 | 57 | mixed | yes | answer org kept 47% [35, 60], answer of bridge alt's statement 2% [0, 9], answer at the same statement slot 25% [15, 37], the alt prompt's own answer 26% [17, 39] |
| slot:last | e5f0 | 30 | 30 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 53% [36, 70], answer of bridge alt's statement 0% [-0, 11], answer at the same statement slot 33% [19, 51], the alt prompt's own answer 13% [5, 30] |

## Checks

`{"self_noop": {"n": 720, "same_top": 720, "max_abs_dlogit_max": 0.75}, "layer0_all_reproduces_source": {"n": 720, "same_top": 718, "max_abs_dlogit_max": 0.7656}, "unedited_base_answer_read": {"n": 720, "base_answer": 720}}`; near ties: `{"n": 33156, "within_gap": 549, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| named → prompt | e5f0 | question words | 16 | 100% [97, 100] | 0% [-0, 3] | 100% [97, 100] | 0% [-0, 3] | 0% [-0, 3] |
| named → prompt | e5f0 | everything after the question | 52 | 82% [75, 88] | 18% [12, 25] | 0% [-0, 3] | 2% [0, 6] | 81% [73, 87] |
| named → prompt | e5f0 | last two tokens before the answer | 60 | 100% [97, 100] | 0% [-0, 3] | 0% [-0, 3] | 0% [-0, 3] | 100% [97, 100] |
| list position → prompt | e5f0 | question words | 36 | 51% [42, 60] | 49% [40, 58] | 22% [16, 31] | 17% [11, 24] | 0% [-0, 3] |
| list position → prompt | e5f0 | everything after the question | 50 | 25% [18, 33] | 75% [67, 82] | 8% [4, 14] | 14% [9, 22] | 0% [-0, 3] |
| list position → prompt | e5f0 | last two tokens before the answer | 60 | 100% [97, 100] | 0% [-0, 3] | 0% [-0, 3] | 0% [-0, 3] | 100% [97, 100] |
| 2-variable chain → prompt | e5f0 | question words | 16 | 0% [-0, 3] | 100% [97, 100] | 0% [-0, 3] | 0% [-0, 3] | 0% [-0, 3] |
| 2-variable chain → prompt | e5f0 | everything after the question | 48 | 33% [26, 42] | 67% [58, 74] | 12% [8, 20] | 16% [10, 23] | 0% [-0, 3] |
| 2-variable chain → prompt | e5f0 | last two tokens before the answer | 56 | 100% [97, 100] | 0% [-0, 3] | 0% [-0, 3] | 0% [-0, 3] | 100% [97, 100] |
| 3-variable chain → prompt | e5f0 | question words | 32 | 1% [0, 5] | 99% [95, 100] | 0% [-0, 3] | 0% [-0, 3] | 0% [-0, 3] |
| 3-variable chain → prompt | e5f0 | everything after the question | 48 | 17% [11, 24] | 83% [76, 89] | 7% [3, 13] | 9% [5, 16] | 0% [-0, 3] |
| 3-variable chain → prompt | e5f0 | last two tokens before the answer | 56 | 100% [97, 100] | 0% [-0, 3] | 0% [-0, 3] | 0% [-0, 3] | 100% [97, 100] |
| memory → prompt | e5f0 | question words | 16 | 99% [95, 100] | 1% [0, 5] | 97% [92, 99] | 2% [0, 6] | 0% [-0, 3] |
| memory → prompt | e5f0 | everything after the question | 50 | 56% [47, 64] | 44% [36, 53] | 16% [10, 23] | 34% [26, 43] | 0% [-0, 3] |
| memory → prompt | e5f0 | last two tokens before the answer | 60 | 100% [97, 100] | 0% [-0, 3] | 0% [-0, 3] | 0% [-0, 3] | 100% [97, 100] |
| memory → memory | e5f0 | question words | 16 | 100% [97, 100] | 0% [-0, 3] | 85% [78, 90] | 0% [-0, 3] | 0% [-0, 3] |
| memory → memory | e5f0 | everything after the question | 48 | 22% [15, 30] | 78% [70, 85] | 12% [8, 20] | 0% [-0, 3] | 0% [-0, 3] |
| memory → memory | e5f0 | last two tokens before the answer | 58 | 100% [97, 100] | 0% [-0, 3] | 99% [95, 100] | 0% [-0, 3] | 0% [-0, 3] |

## Agent priors in the job spec (jobs/d3/d3_code_main.yaml `hypotheses`) vs results

- H-pointer: memory -> prompt (cue -> key), after the query, layers 44-52: answer at the same statement slot (entry answer at the same statement slot) >= 25%, above the alt key's entry; named -> prompt the same
- H-word: answer of bridge alt's statement (the alt key's entry) >= 25%, entry answer at the same statement slot <= 10%
- H-value: the alt program's own answer dominates from layer ~52 (as in prose)
- prior: Agent prior: H-pointer 0.45, H-word 0.35, mixed 0.2.

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 20% [14, 28], last two tokens 15% [10, 22] (>= 50%: not met); memory → memory 0% [-0, 3] / 0% [-0, 3] (<= 10%: met); named → prompt after the question 1% [0, 5] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 3% [1, 8] / 3% [1, 8] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 24% [17, 33] / 39% [31, 48] (>= 50%: not met); first single layer where it reaches 20%: after the question 52, last two tokens 52
- H-none: memory → prompt, answer changed after the question 48% [40, 57] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-RK-e5f0-0290` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 48 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
```python
lockers = {"duck": 9, "bee": 3, "cow": 1, "cat": 5, "horse": 0}
```
What number does lockers store for the animal known for neighing? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
```python
lockers = {"bee": 7, "cat": 1, "cow": 9, "duck": 0, "horse": 8}
```
What number does lockers store for the animal known for making honey? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 0; after the patch 9. Predicted: answer org kept 0 (p 0.059); answer of bridge alt's statement 3 (p 0.000); answer at the same statement slot 9 (p 0.929); the alt prompt's own answer 7 (p 0.000).

