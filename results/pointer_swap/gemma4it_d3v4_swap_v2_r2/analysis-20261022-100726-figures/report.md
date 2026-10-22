# D3 on Gemma 4 31B-it: is there a statement-slot phase at the last tokens before the digit arrives?

Run `gemma4it_d3v4_swap_v2_r2` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements, 3 wordings per topic.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP gemma4it_d3v4_swap_v2_r2 @ unknown | model gemma-4-31B-it (chat format) | n per family =  | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 41-49: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = -   Baseline: none = -, identity = -, value = -   Control: 'same' changed = -; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/gemma4it_d3v4_swap_v2_r2/analysis-20261022-100726-figures/by_layer_e5f0.png, results/pointer_swap/gemma4it_d3v4_swap_v2_r2/analysis-20261022-100726-figures/slots_final_e5f0.png, results/pointer_swap/gemma4it_d3v4_swap_v2_r2/analysis-20261022-100726-figures/slots_last_e5f0.png, results/pointer_swap/gemma4it_d3v4_swap_v2_r2/analysis-20261022-100726-figures/windows_e5f0.png, results/pointer_swap/gemma4it_d3v4_swap_v2_r2/analysis-20261022-100726-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/gemma4it_d3v4_swap_v2_r2/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=-); position should be -, identity -, value -, none -
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win -; among alt prompt reads won by a predicted digit, 130/15281 have the runner-up prediction within p 0.1; hook checks self no-op 850/850, layer-0 reproduction 850/850.
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
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 17%, the alt prompt's own answer 83%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words | e5f0 | - | - | - |
| named → prompt | everything after the question | e5f0 | - | - | - |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 20%, the alt prompt's own answer 80%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|

## Checks

`{"self_noop": {"n": 850, "same_top": 850, "max_abs_dlogit_max": 0.7812}, "layer0_all_reproduces_source": {"n": 850, "same_top": 850, "max_abs_dlogit_max": 2.4375}, "unedited_base_answer_read": {"n": 850, "base_answer": 850}}`; near ties: `{"n": 15281, "within_gap": 130, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | last two tokens before the answer | 56 | 100% [98, 100] | 0% [0, 2] | 0% [0, 1] | 0% [0, 1] | 100% [98, 100] |
| named → prompt | e5f0 | last two tokens before the answer | 56 | 100% [99, 100] | 0% [0, 1] | 0% [0, 1] | 0% [0, 1] | 100% [99, 100] |

## Agent priors in the job spec (jobs/d3/gemma4it_d3v4_swap_v2_r2.yaml `hypotheses`) vs results

- H-slot-gemma: at some patched layer whose pooled alt-digit share (memory -> prompt, last two tokens) has upper bound < 10%, the rule's verdict is "same statement slot" pooled and in >= 2 of 3 topics. Prior 0.45

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question nan% [nan, nan], last two tokens 0% [0, 1] (>= 50%: not met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question nan% [nan, nan] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: nan% [nan, nan] / 0% [0, 1] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: nan% [nan, nan] / 83% [79, 86] (>= 50%: not met); first single layer where it reaches 20%: after the question None, last two tokens 42
- H-none: memory → prompt, answer changed after the question nan% [nan, nan] (< 20%: not met)

## Worked example (from examples.json)

Item `body-RL-e5f0-0011` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the last tokens replaced by the alt prompt's at layer 44 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<bos><|turn>user
Folder 4 holds the tongue chart. Folder 8 holds the skull chart. Folder 6 holds the ear chart. Folder 3 holds the bladder chart. Folder 7 holds the stomach chart.
In which folder is the chart on the body part that tastes food? Answer with a single word and nothing else.<turn|>
<|turn>model
<|channel>thought
<channel|>Answer: 
```

Alt prompt:

```
<bos><|turn>user
Folder 3 holds the bladder chart. Folder 9 holds the ear chart. Folder 7 holds the stomach chart. Folder 5 holds the tongue chart. Folder 4 holds the skull chart.
In which folder is the chart on the body part that hears sounds? Answer with a single word and nothing else.<turn|>
<|turn>model
<|channel>thought
<channel|>Answer: 
```

Answers: answer org 4; after the patch 8. Predicted: answer org kept 4 (p 0.060); answer of bridge alt's statement 6 (p 0.000); answer at the same statement slot 8 (p 0.933); the alt prompt's own answer 9 (p 0.007).

