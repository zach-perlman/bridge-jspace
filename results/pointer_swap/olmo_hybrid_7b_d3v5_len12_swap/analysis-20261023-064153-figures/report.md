# Finding 5 by the fixed rule on fresh 12-sentence lists, colour-word answers (Olmo-Hybrid-7B Instruct, layers 16-21)

Run `olmo_hybrid_7b_d3v5_len12_swap` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e12-word` = 12 statements, colour-word answers.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP olmo_hybrid_7b_d3v5_len12_swap @ unknown | model Olmo-Hybrid-Instruct-DPO-7B (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 22-26: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e12-word): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/olmo_hybrid_7b_d3v5_len12_swap/analysis-20261023-064153-figures/by_layer_e12-word.png, results/pointer_swap/olmo_hybrid_7b_d3v5_len12_swap/analysis-20261023-064153-figures/slots_final_e12-word.png, results/pointer_swap/olmo_hybrid_7b_d3v5_len12_swap/analysis-20261023-064153-figures/slots_last_e12-word.png, results/pointer_swap/olmo_hybrid_7b_d3v5_len12_swap/analysis-20261023-064153-figures/windows_e12-word.png, results/pointer_swap/olmo_hybrid_7b_d3v5_len12_swap/analysis-20261023-064153-figures/domains_final_e12-word.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/olmo_hybrid_7b_d3v5_len12_swap/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e12-word'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 101/2632 have the runner-up prediction within p 0.1; hook checks self no-op 382/382, layer-0 reproduction 382/382.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": null, "body": null, "countries": null}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e12-word: **no data** (-)

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 36, in cuts ['slot:first', 'slot:last'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e12-word | - | - | - |
| memory → prompt | everything after the question | e12-word | - | - | - |
| memory → prompt | last two tokens before the answer | e12-word | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | mixed (answer org kept 6%, answer of bridge alt's statement 23%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 75%) |
| memory → prompt | question words + everything after | e12-word | - | - | - |
| named → prompt | question words | e12-word | - | - | - |
| named → prompt | everything after the question | e12-word | - | - | - |
| named → prompt | last two tokens before the answer | e12-word | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 3%, the alt prompt's own answer 27%) | alt prompt's own answer (H-value) (answer org kept 1%, the alt prompt's own answer 99%) |
| named → prompt | question words + everything after | e12-word | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 382, "same_top": 382, "max_abs_dlogit_max": 0.625}, "layer0_all_reproduces_source": {"n": 382, "same_top": 382, "max_abs_dlogit_max": 0.8125}, "unedited_base_answer_read": {"n": 382, "base_answer": 381}}`; near ties: `{"n": 2632, "within_gap": 101, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e12-word | last two tokens before the answer | 21 | 95% [91, 98] | 5% [2, 9] | 22% [16, 28] | 17% [11, 23] | 9% [5, 14] |
| named → prompt | e12-word | last two tokens before the answer | 20 | 97% [93, 99] | 3% [1, 7] | 18% [12, 24] | 17% [12, 23] | 27% [21, 34] |

## Pre-registered primary (pointer_v5): memory -> prompt, the last two tokens, layers 17 and 18 and 19: does each layout keep the statement slot?

| layout | keeps the slot | per layer: pooled verdict, topics with the slot |
|---|---|---|
| 12 statements, colour words | **no** | 17: identity, 0/3; 18: damage, 0/3; 19: mixed, 0/3 |

## Agent priors in the job spec (jobs/d3/olmo_hybrid_7b_d3v5_len12_swap.yaml `hypotheses`) vs results

- H-A: e12-word: answer at the same statement slot - answer of bridge alt's statement (1st and 2nd) has its entity-cluster 95% lower bound > 0. Prior 0.6 (agent's) (copied from qwen35_9b_d3v5_len12_swap)
- H-B: e12-word: answer of bridge alt's statement - answer at the same statement slot (3rd-12th) >= 0 with lower bound >= -0.05. Prior 0.55 (agent's) (copied from qwen35_9b_d3v5_len12_swap)

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 4% [2, 8] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 4% [1, 7] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 75% [69, 81] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens None
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `body-RL-e12-word-0087` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer transit (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The chart on the liver is kept in the violet folder. The chart on the knee is kept in the cyan folder. The chart on the eye is kept in the green folder. The chart on the forehead is kept in the yellow folder. The chart on the bladder is kept in the blue folder. The chart on the ankle is kept in the gold folder. The chart on the tongue is kept in the black folder. The chart on the ear is kept in the orange folder. The chart on the wrist is kept in the red folder. The chart on the brain is kept in the grey folder. The chart on the eyebrow is kept in the brown folder. The chart on the heart is kept in the purple folder.
Which colour is the folder that holds the chart on the body part that does the thinking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Alt prompt:

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The chart on the bladder is kept in the cyan folder. The chart on the knee is kept in the brown folder. The chart on the forehead is kept in the purple folder. The chart on the brain is kept in the gold folder. The chart on the liver is kept in the red folder. The chart on the ear is kept in the blue folder. The chart on the heart is kept in the green folder. The chart on the eye is kept in the black folder. The chart on the eyebrow is kept in the orange folder. The chart on the tongue is kept in the white folder. The chart on the wrist is kept in the violet folder. The chart on the ankle is kept in the pink folder.
Which colour is the folder that holds the chart on the body part joining foot and leg? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

Answers: answer org grey; after the patch purple. Predicted: answer org kept grey (p 0.019); answer of bridge alt's statement gold (p 0.008); answer at the same statement slot purple (p 0.292); the alt prompt's own answer pink (p 0.041).

