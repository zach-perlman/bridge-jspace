# D3 v2 test run: the new scenes and the --data option work on the 27B

Run `d3v2_smoke_27b` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5-off` = 5 statements + 1 filler, the filler sentence in another place in the alt prompt (order and token position split); `e5-pln` = 5 statements + 1 filler, the filler sentence in the same place in both prompts; `e5-ref` = 5 statements + 1 filler, the alt prompt's answer also in the org prompt.

```
EXP d3v2_smoke_27b @ ca14894 | model Qwen3.6-27B | n per family = memory → prompt 2 (filler moved); memory → prompt 2 (filler in place); memory → prompt 2 (alt answer in org); named → prompt 2 (filler moved); named → prompt 2 (filler in place); named → prompt 2 (alt answer in org) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5-off): position = 50% [9, 91]   Baseline: none = 0% [0, 66], identity = 0% [0, 66], value = 50% [9, 91]   Control: 'same' changed = 0% [0, 66]; random push of the same size changed (max over transit layers) = -; another domain's prompt changed = -
Figures: results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/by_layer_e5-off.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/by_layer_e5-pln.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/by_layer_e5-ref.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/slots_final_e5-off.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/slots_last_e5-off.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/windows_e5-off.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/domains_final_e5-off.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/levels_final.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/levels_last.png, results/pointer_swap/d3v2_smoke_27b/analysis-20261021-160408-figures/reflexive.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v2_smoke_27b/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5-off'`: count `role` (n=2); position should be 1, identity 0, value 1, none 0
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer - (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 66]; among alt prompt reads won by a predicted digit, 3/251 have the runner-up prediction within p 0.1; hook checks self no-op 12/12, layer-0 reproduction 12/12.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "damage", "elements": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5-off: **damage** (answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91]); e5-pln: **damage** (answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91]); e5-ref: **damage** (answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 504, in cuts ['all', 'domain:animals', 'domain:elements', 'slot:last'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5-off | damage (answer org kept 0%, answer of bridge alt's statement 100%) | - | - |
| memory → prompt | question words | e5-pln | damage (answer org kept 0%, answer of bridge alt's statement 100%) | - | - |
| memory → prompt | question words | e5-ref | damage (answer org kept 0%, answer of bridge alt's statement 100%) | - | - |
| memory → prompt | everything after the question | e5-off | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| memory → prompt | everything after the question | e5-pln | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| memory → prompt | everything after the question | e5-ref | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| memory → prompt | last two tokens before the answer | e5-off | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| memory → prompt | last two tokens before the answer | e5-pln | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| memory → prompt | last two tokens before the answer | e5-ref | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| memory → prompt | question words + everything after | e5-off | - | - | - |
| memory → prompt | question words + everything after | e5-pln | - | - | - |
| memory → prompt | question words + everything after | e5-ref | - | - | - |
| named → prompt | question words | e5-off | damage (answer org kept 0%, answer at the same statement slot 50%) | - | - |
| named → prompt | question words | e5-pln | damage (answer org kept 0%, answer of bridge alt's statement 50%) | - | - |
| named → prompt | question words | e5-ref | damage (answer org kept 0%, answer of bridge alt's statement 50%) | - | - |
| named → prompt | everything after the question | e5-off | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| named → prompt | everything after the question | e5-pln | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| named → prompt | everything after the question | e5-ref | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| named → prompt | last two tokens before the answer | e5-off | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| named → prompt | last two tokens before the answer | e5-pln | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| named → prompt | last two tokens before the answer | e5-ref | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, answer at the same statement slot 50%) |
| named → prompt | question words + everything after | e5-off | - | - | - |
| named → prompt | question words + everything after | e5-pln | - | - | - |
| named → prompt | question words + everything after | e5-ref | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5-off | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91] |
| domain:animals | e5-off | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 100% [21, 100] |
| domain:elements | e5-off | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 100% [21, 100], the alt prompt's own answer 0% [0, 79] |
| slot:last | e5-off | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91] |
| all | e5-pln | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91] |
| domain:animals | e5-pln | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 100% [21, 100] |
| domain:elements | e5-pln | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 100% [21, 100], the alt prompt's own answer 0% [0, 79] |
| slot:last | e5-pln | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91] |
| all | e5-ref | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91] |
| domain:animals | e5-ref | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 100% [21, 100] |
| domain:elements | e5-ref | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 100% [21, 100], the alt prompt's own answer 0% [0, 79] |
| slot:last | e5-ref | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 66], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 50% [9, 91], the alt prompt's own answer 50% [9, 91] |

## Checks

`{"self_noop": {"n": 12, "same_top": 12, "max_abs_dlogit_max": 0.2812}, "layer0_all_reproduces_source": {"n": 12, "same_top": 12, "max_abs_dlogit_max": 0.3125}, "unedited_base_answer_read": {"n": 12, "base_answer": 12}}`; near ties: `{"n": 251, "within_gap": 3, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5-off | question words | 16 | 100% [34, 100] | 0% [0, 66] | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] |
| memory → prompt | e5-off | everything after the question | 48 | 50% [9, 91] | 50% [9, 91] | 0% [0, 66] | 0% [0, 66] | 0% [0, 66] |
| memory → prompt | e5-off | last two tokens before the answer | 52 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 50% [9, 91] | 50% [9, 91] |
| memory → prompt | e5-pln | question words | 16 | 100% [34, 100] | 0% [0, 66] | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] |
| memory → prompt | e5-pln | everything after the question | 48 | 50% [9, 91] | 50% [9, 91] | 50% [9, 91] | 0% [0, 66] | 0% [0, 66] |
| memory → prompt | e5-pln | last two tokens before the answer | 48 | 100% [34, 100] | 0% [0, 66] | 50% [9, 91] | 50% [9, 91] | 0% [0, 66] |
| memory → prompt | e5-ref | question words | 16 | 100% [34, 100] | 0% [0, 66] | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] |
| memory → prompt | e5-ref | everything after the question | 48 | 50% [9, 91] | 50% [9, 91] | 50% [9, 91] | 0% [0, 66] | 0% [0, 66] |
| memory → prompt | e5-ref | last two tokens before the answer | 52 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 50% [9, 91] | 50% [9, 91] |
| named → prompt | e5-off | question words | 16 | 100% [34, 100] | 0% [0, 66] | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] |
| named → prompt | e5-off | everything after the question | 48 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 50% [9, 91] | 0% [0, 66] |
| named → prompt | e5-off | last two tokens before the answer | 52 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 50% [9, 91] | 50% [9, 91] |
| named → prompt | e5-pln | question words | 16 | 100% [34, 100] | 0% [0, 66] | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] |
| named → prompt | e5-pln | everything after the question | 48 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 100% [34, 100] | 0% [0, 66] |
| named → prompt | e5-pln | last two tokens before the answer | 52 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 50% [9, 91] | 50% [9, 91] |
| named → prompt | e5-ref | question words | 16 | 100% [34, 100] | 0% [0, 66] | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] |
| named → prompt | e5-ref | everything after the question | 48 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 50% [9, 91] | 0% [0, 66] |
| named → prompt | e5-ref | last two tokens before the answer | 52 | 100% [34, 100] | 0% [0, 66] | 0% [0, 66] | 50% [9, 91] | 50% [9, 91] |

## Reflexive test (pre-registered v2 rule): the alt prompt's own answer, when it is also in the org prompt vs when it is not (same scenes, paired)

| family | patched tokens | layer | pairs | alt answer, also in org | alt answer, not in org | difference [95% CI] | label | plain cell interpretable |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | everything after the question | 16 | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | 16 | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 28 | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | 28 | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 40 | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | 40 | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 48 | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | 48 | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 52 | 2 | 50% | 50% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | 52 | 2 | 50% | 50% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | 56 | 2 | 50% | 50% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | 56 | 2 | 100% | 100% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | early | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | early | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | mid | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | mid | 2 | 0% | 0% | +0 [+0, +0] | value | False |
| memory → prompt | everything after the question | transit | 2 | 50% | 50% | +0 [+0, +0] | value | False |
| memory → prompt | last two tokens before the answer | transit | 2 | 50% | 50% | +0 [+0, +0] | value | False |

## Agent priors in the job spec (jobs/d3/d3v2_smoke_27b.yaml `hypotheses`) vs results

- H-ok: self no-op and layer-0 reproduction 12/12; >= 30 edited reads/s
- H-broken: any check below 12/12: the hooks or the token alignment are wrong; stop the queue

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 50% [9, 91], last two tokens 50% [9, 91] (>= 50%: met); memory → memory nan% [nan, nan] / nan% [nan, nan] (<= 10%: not met); named → prompt after the question 50% [9, 91] (>= 50%: met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [0, 66] / 0% [0, 66] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 50% [9, 91] / 50% [9, 91] (>= 50%: met); first single layer where it reaches 20%: after the question 52, last two tokens 52
- H-none: memory → prompt, answer changed after the question 100% [34, 100] (< 20%: not met)

## Worked example (from examples.json)

Item `animals-DL-e5-off-0098` (named → prompt; the patched answer was the answer at the same token position). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 48 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The lamp in the hall flickered. The bee's locker is 5. The dog's locker is 0. The goose's locker is 9. The turkey's locker is 7. The spider's locker is 3.
Which locker belongs to the spider? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The bee's locker is 0. The turkey's locker is 1. The goose's locker is 5. The dog's locker is 3. The spider's locker is 7. The lamp in the hall flickered.
Which locker belongs to the turkey? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 3; after the patch 5. Predicted: answer org kept 3 (p 0.003); answer of bridge alt's statement 7 (p 0.001); answer at the same statement slot 0 (p 0.005); answer at the same token position 5 (p 0.986); the alt prompt's own answer 1 (p 0.000).

