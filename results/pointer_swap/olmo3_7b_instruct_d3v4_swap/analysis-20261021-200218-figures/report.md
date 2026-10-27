# G3: does a second model (OLMo-3-7B-Instruct) also answer the statement slot when the last tokens are patched?

Run `olmo3_7b_instruct_d3v4_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements, 3 wordings per topic.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo3_7b_instruct_d3v4_swap @ unknown | model Olmo-3-7B-Instruct (chat format) | n per family = memory → prompt 346 items / 72 entities / 27 wordings (5 statements); named → prompt 346 items / 72 entities / 27 wordings (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 0% [-0, 1]   Baseline: none = 100% [98, 100], identity = 0% [0, 2], value = 0% [-0, 1]   Control: 'same' changed = 0% [-0, 1]; random push of the same size changed (max over transit layers) = 1% [0, 2]; another domain's prompt changed = 1% [0, 3]
Figures: results/pointer_swap/olmo3_7b_instruct_d3v4_swap/analysis-20261021-200218-figures/by_layer_e5f0.png, results/pointer_swap/olmo3_7b_instruct_d3v4_swap/analysis-20261021-200218-figures/slots_final_e5f0.png, results/pointer_swap/olmo3_7b_instruct_d3v4_swap/analysis-20261021-200218-figures/slots_last_e5f0.png, results/pointer_swap/olmo3_7b_instruct_d3v4_swap/analysis-20261021-200218-figures/windows_e5f0.png, results/pointer_swap/olmo3_7b_instruct_d3v4_swap/analysis-20261021-200218-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo3_7b_instruct_d3v4_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=346); position should be 0, identity 1, value 0, none 345
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 1% [0, 2] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [-0, 1]; among alt prompt reads won by a predicted digit, 78/17773 have the runner-up prediction within p 0.1; hook checks self no-op 692/692, layer-0 reproduction 691/692.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "none", "body": "none", "countries": "none"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **no effect** (answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [-0, 1], the alt prompt's own answer 0% [-0, 1])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | - | - | - |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 96%, answer of bridge alt's statement 1%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 92%, answer of bridge alt's statement 3%) | mixed (answer org kept 8%, answer at the same statement slot 32%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words | e5f0 | - | - | - |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 79%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 346 | 346 | no effect | yes | answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [-0, 1], the alt prompt's own answer 0% [-0, 1] |
| domain:animals | e5f0 | 141 | 141 | no effect | yes | answer org kept 99% [96, 100], answer of bridge alt's statement 1% [0, 4], answer at the same statement slot 0% [0, 3], the alt prompt's own answer 0% [0, 3] |
| domain:body | e5f0 | 55 | 55 | no effect | yes | answer org kept 100% [93, 100], answer of bridge alt's statement 0% [0, 7], answer at the same statement slot 0% [0, 7], the alt prompt's own answer 0% [0, 7] |
| domain:countries | e5f0 | 150 | 150 | no effect | yes | answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2] |
| slot:first | e5f0 | 56 | 56 | no effect | yes | answer org kept 100% [94, 100], answer of bridge alt's statement 0% [0, 6], answer at the same statement slot 0% [0, 6], the alt prompt's own answer 0% [0, 6] |
| slot:middle | e5f0 | 195 | 195 | no effect | yes | answer org kept 99% [97, 100], answer of bridge alt's statement 1% [0, 3], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2] |
| slot:last | e5f0 | 95 | 95 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |

## Checks

`{"self_noop": {"n": 692, "same_top": 692, "max_abs_dlogit_max": 0.4375}, "layer0_all_reproduces_source": {"n": 692, "same_top": 691, "max_abs_dlogit_max": 0.5938}, "unedited_base_answer_read": {"n": 692, "base_answer": 692}}`; near ties: `{"n": 17773, "within_gap": 78, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | everything after the question | 20 | 2% [1, 4] | 98% [96, 99] | 1% [0, 2] | 1% [0, 3] | 0% [-0, 1] |
| memory → prompt | e5f0 | last two tokens before the answer | 26 | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 0% [-0, 1] | 100% [98, 100] |
| named → prompt | e5f0 | everything after the question | 8 | 0% [-0, 1] | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 0% [-0, 1] |
| named → prompt | e5f0 | last two tokens before the answer | 22 | 100% [99, 100] | 0% [-0, 1] | 0% [-0, 1] | 1% [0, 3] | 99% [97, 100] |

## Agent priors in the job spec (jobs/d3/olmo3_7b_instruct_d3v4_swap.yaml `hypotheses`) vs results

- H-slot-olmo: memory -> prompt, last two tokens, layer 24 or 25, pooled over topics: the same-statement-slot share's entity-cluster lower bound exceeds the upper bound of the bridge-alt's-statement share
- H-word-olmo: the bridge alt's statement beats the slot there (OLMo looks the entity up by name)
- prior: Coordinator's prior: H-slot-olmo 0.5.

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [-0, 1], last two tokens 0% [-0, 1] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 0% [-0, 1] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [0, 2] / 0% [-0, 1] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 0% [-0, 1] / 100% [98, 100] (>= 50%: met); first single layer where it reaches 20%: after the question None, last two tokens 20
- H-none: memory → prompt, answer changed after the question 0% [0, 2] (< 20%: met)

## Worked example (from examples.json)

Item `countries-RL-e5f0-0157` (memory → prompt; the patched answer was the answer org kept). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The Pakistan file is in drawer 7. The Japan file is in drawer 2. The Canada file is in drawer 6. The Finland file is in drawer 4. The Indonesia file is in drawer 5.
Which drawer holds the file on the country whose capital is Helsinki? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Alt prompt:

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The Japan file is in drawer 1. The Indonesia file is in drawer 6. The Finland file is in drawer 7. The Canada file is in drawer 2. The Pakistan file is in drawer 5.
Which drawer holds the file on the country whose capital is Tokyo? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Answers: answer org 4; after the patch 4. Predicted: answer org kept 4 (p 0.996); answer of bridge alt's statement 2 (p 0.000); answer at the same statement slot 7 (p 0.000); the alt prompt's own answer 1 (p 0.000).

