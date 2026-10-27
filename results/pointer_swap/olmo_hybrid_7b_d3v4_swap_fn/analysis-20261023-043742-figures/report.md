# G3 on Olmo-Hybrid-7B Instruct, cells placed by function: is there a statement-slot phase before the digit arrives?

Run `olmo_hybrid_7b_d3v4_swap_fn` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements, 3 wordings per topic.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo_hybrid_7b_d3v4_swap_fn @ unknown | model Olmo-Hybrid-Instruct-DPO-7B (chat format) | n per family = memory → prompt 516 items / 81 entities / 27 wordings (5 statements); named → prompt 516 items / 81 entities / 27 wordings (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 0% [0, 1]   Baseline: none = 100% [99, 100], identity = 0% [0, 1], value = 0% [0, 1]   Control: 'same' changed = 0% [0, 1]; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo_hybrid_7b_d3v4_swap_fn/analysis-20261023-043742-figures/by_layer_e5f0.png, results/pointer_swap/olmo_hybrid_7b_d3v4_swap_fn/analysis-20261023-043742-figures/slots_final_e5f0.png, results/pointer_swap/olmo_hybrid_7b_d3v4_swap_fn/analysis-20261023-043742-figures/slots_last_e5f0.png, results/pointer_swap/olmo_hybrid_7b_d3v4_swap_fn/analysis-20261023-043742-figures/windows_e5f0.png, results/pointer_swap/olmo_hybrid_7b_d3v4_swap_fn/analysis-20261023-043742-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo_hybrid_7b_d3v4_swap_fn/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=516); position should be 0, identity 0, value 0, none 514
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 1]; among alt prompt reads won by a predicted digit, 216/18204 have the runner-up prediction within p 0.1; hook checks self no-op 1032/1032, layer-0 reproduction 1032/1032.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "none", "body": "none", "countries": "none"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **no effect** (answer org kept 100% [99, 100], answer of bridge alt's statement 0% [0, 1], answer at the same statement slot 0% [0, 1], the alt prompt's own answer 0% [0, 1])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 0, in cuts [].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | - | - | - |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | no effect (answer org kept 86%, answer at the same statement slot 8%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 99%, answer at the same statement slot 0%) | alt prompt's own answer (H-value) (answer org kept 3%, the alt prompt's own answer 79%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 98%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words | e5f0 | - | - | - |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 2%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 89%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 516 | 516 | no effect | yes | answer org kept 100% [99, 100], answer of bridge alt's statement 0% [0, 1], answer at the same statement slot 0% [0, 1], the alt prompt's own answer 0% [0, 1] |
| domain:animals | e5f0 | 167 | 167 | no effect | yes | answer org kept 99% [97, 100], answer of bridge alt's statement 0% [0, 2], answer at the same statement slot 0% [0, 2], the alt prompt's own answer 0% [0, 2] |
| domain:body | e5f0 | 94 | 94 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| domain:countries | e5f0 | 255 | 255 | no effect | yes | answer org kept 100% [98, 100], answer of bridge alt's statement 0% [0, 1], answer at the same statement slot 0% [0, 1], the alt prompt's own answer 0% [0, 1] |
| slot:first | e5f0 | 103 | 103 | no effect | yes | answer org kept 98% [93, 100], answer of bridge alt's statement 0% [0, 4], answer at the same statement slot 0% [0, 4], the alt prompt's own answer 0% [0, 4] |
| slot:middle | e5f0 | 307 | 307 | no effect | yes | answer org kept 100% [99, 100], answer of bridge alt's statement 0% [0, 1], answer at the same statement slot 0% [0, 1], the alt prompt's own answer 0% [0, 1] |
| slot:last | e5f0 | 106 | 106 | no effect | yes | answer org kept 100% [96, 100], answer of bridge alt's statement 0% [-0, 4], answer at the same statement slot 0% [-0, 4], the alt prompt's own answer 0% [-0, 4] |

## Checks

`{"self_noop": {"n": 1032, "same_top": 1032, "max_abs_dlogit_max": 0.625}, "layer0_all_reproduces_source": {"n": 1032, "same_top": 1032, "max_abs_dlogit_max": 0.75}, "unedited_base_answer_read": {"n": 1032, "base_answer": 1032}}`; near ties: `{"n": 18204, "within_gap": 216, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | everything after the question | 17 | 17% [13, 21] | 83% [79, 87] | 6% [4, 9] | 9% [6, 11] | 0% [0, 1] |
| memory → prompt | e5f0 | last two tokens before the answer | 20 | 97% [95, 98] | 3% [2, 5] | 3% [2, 5] | 12% [9, 15] | 79% [75, 82] |
| named → prompt | e5f0 | everything after the question | 17 | 4% [2, 6] | 96% [94, 98] | 2% [1, 3] | 2% [1, 4] | 0% [0, 1] |
| named → prompt | e5f0 | last two tokens before the answer | 20 | 99% [98, 100] | 1% [0, 2] | 1% [0, 2] | 10% [7, 13] | 89% [86, 91] |

## Agent priors in the job spec (jobs/d3/olmo_hybrid_7b_d3v4_swap_fn.yaml `hypotheses`) vs results

- H-slot-phase: memory → prompt, last two tokens, at least one of layers 17, 18, 19: verdict "same statement slot" pooled (the slot share's lower bound above the word's, the alt digit's and the random push's upper bounds; the same-entity control <= 10%), and the same at that layer in >= 2 of the topics with n >= 35. Prior 0.5 (copied from olmo3_7b_instruct_d3v4_swap_fn)
- H-word: the word (bridge alt's statement) wins at 17-19 (a content code, as the J-lens would suggest). Prior 0.15 (copied from olmo3_7b_instruct_d3v4_swap_fn)
- H-no-phase: mixed or none at every layer 17-19 (slot and digit arrive together; no separable pointer phase). Prior 0.35 (copied from olmo3_7b_instruct_d3v4_swap_fn)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [0, 1], last two tokens 0% [0, 1] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 0% [0, 1] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [0, 1] / 0% [0, 1] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 0% [0, 1] / 98% [97, 99] (>= 50%: met); first single layer where it reaches 20%: after the question None, last two tokens 19
- H-none: memory → prompt, answer changed after the question 0% [0, 1] (< 20%: met)

## Worked example (from examples.json)

Item `countries-RL-e5f0-0209` (memory → prompt; the patched answer was the answer org kept). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The file on Turkey is kept in drawer 1. The file on Philippines is kept in drawer 6. The file on China is kept in drawer 5. The file on Kenya is kept in drawer 9. The file on Denmark is kept in drawer 7.
Which drawer holds the file on the country whose capital is Copenhagen? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Alt prompt:

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The file on Denmark is kept in drawer 9. The file on China is kept in drawer 7. The file on Kenya is kept in drawer 3. The file on Philippines is kept in drawer 5. The file on Turkey is kept in drawer 1.
Which drawer holds the file on the country whose capital is Nairobi? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Answers: answer org 7; after the patch 7. Predicted: answer org kept 7 (p 0.993); answer of bridge alt's statement 9 (p 0.000); answer at the same statement slot 5 (p 0.000); the alt prompt's own answer 3 (p 0.004).

