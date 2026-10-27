# D3 v4 test run: the new scenes work in the patching and pointer-direction code on the 27B

Run `d3v4_smoke_27b` (results/pointer_swap/), analysis of the saved outputs only.

Level names: `e5f0` = 5 statements, 3 wordings per topic.

Intervals: 95% entity-cluster bootstrap (asked entity resampled within each topic, 2000 resamples, seed 0), widened to the item-level Wilson interval where that is wider; the rule reads these. Item-level Wilson: summary.json `rates[...]['wilson']`.

```
EXP d3v4_smoke_27b @ unknown | model Qwen3.6-27B | n per family = memory → prompt 3 items / 3 entities / 3 wordings (5 statements); named → prompt 3 items / 3 entities / 3 wordings (5 statements); memory → memory 3 items / 3 entities / 3 wordings (5 statements) | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in memory → prompt (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: memory → prompt, tokens after the question, transit window (e5f0): position = 0% [0, 56]   Baseline: none = 67% [21, 94], identity = 0% [0, 56], value = 33% [6, 79]   Control: 'same' changed = 0% [0, 56]; random push of the same size changed (max over transit layers) = 0% [0, 56]; another domain's prompt changed = 0% [0, 56]
Figures: results/pointer_swap/d3v4_smoke_27b/analysis-20261021-153301-figures/by_layer_e5f0.png, results/pointer_swap/d3v4_smoke_27b/analysis-20261021-153301-figures/slots_final_e5f0.png, results/pointer_swap/d3v4_smoke_27b/analysis-20261021-153301-figures/slots_last_e5f0.png, results/pointer_swap/d3v4_smoke_27b/analysis-20261021-153301-figures/windows_e5f0.png, results/pointer_swap/d3v4_smoke_27b/analysis-20261021-153301-figures/domains_final_e5f0.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3v4_smoke_27b/outcomes.jsonl, rows `family == 'RL'`, `group == 'final'`, `layer == 'transit'`, `source == 'dissoc'`, `level == 'e5f0'`: count `role` (n=3); position should be 0, identity 0, value 1, none 2
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 56] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 56]; among alt prompt reads won by a predicted digit, 2/108 have the runner-up prediction within p 0.1; hook checks self no-op 9/9, layer-0 reproduction 9/9.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "damage", "body": "damage", "countries": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **damage** (answer org kept 67% [21, 94], answer of bridge alt's statement 0% [0, 56], answer at the same statement slot 0% [0, 56], the alt prompt's own answer 33% [6, 79])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 216, in cuts ['all', 'domain:animals', 'domain:body', 'domain:countries', 'slot:first', 'slot:middle'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | - | - | - |
| memory → prompt | everything after the question | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 33%, answer of bridge alt's statement 67%) | damage (answer org kept 67%, the alt prompt's own answer 33%) |
| memory → prompt | last two tokens before the answer | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 33%, the alt prompt's own answer 67%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words | e5f0 | - | - | - |
| named → prompt | everything after the question | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 0%, the alt prompt's own answer 100%) |
| named → prompt | last two tokens before the answer | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |
| memory → memory | question words | e5f0 | - | - | - |
| memory → memory | everything after the question | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 67%, answer of bridge alt's statement 33%) |
| memory → memory | last two tokens before the answer | e5f0 | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 67%, answer of bridge alt's statement 33%) | damage (answer org kept 33%, answer of bridge alt's statement 67%) |
| memory → memory | question words + everything after | e5f0 | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 3 | 3 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 67% [21, 94], answer of bridge alt's statement 0% [0, 56], answer at the same statement slot 0% [0, 56], the alt prompt's own answer 33% [6, 79] |
| domain:animals | e5f0 | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 0% [0, 79], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 100% [21, 100] |
| domain:body | e5f0 | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| domain:countries | e5f0 | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |
| slot:first | e5f0 | 2 | 2 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 50% [9, 91], answer of bridge alt's statement 0% [0, 66], answer at the same statement slot 0% [0, 66], the alt prompt's own answer 50% [9, 91] |
| slot:middle | e5f0 | 1 | 1 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [21, 100], answer of bridge alt's statement 0% [0, 79], answer at the same statement slot 0% [0, 79], the alt prompt's own answer 0% [0, 79] |

## Checks

`{"self_noop": {"n": 9, "same_top": 9, "max_abs_dlogit_max": 0.3125}, "layer0_all_reproduces_source": {"n": 9, "same_top": 9, "max_abs_dlogit_max": 0.3281}, "unedited_base_answer_read": {"n": 9, "base_answer": 9}}`; near ties: `{"n": 108, "within_gap": 2, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | everything after the question | 44 | 33% [6, 79] | 67% [21, 94] | 33% [6, 79] | 0% [0, 56] | 0% [0, 56] |
| memory → prompt | e5f0 | last two tokens before the answer | 52 | 67% [21, 94] | 33% [6, 79] | 0% [0, 56] | 0% [0, 56] | 67% [21, 94] |
| named → prompt | e5f0 | everything after the question | 52 | 100% [44, 100] | 0% [0, 56] | 0% [0, 56] | 0% [0, 56] | 100% [44, 100] |
| named → prompt | e5f0 | last two tokens before the answer | 44 | 0% [0, 56] | 100% [44, 100] | 0% [0, 56] | 0% [0, 56] | 0% [0, 56] |
| memory → memory | e5f0 | everything after the question | 44 | 33% [6, 79] | 67% [21, 94] | 33% [6, 79] | 0% [0, 56] | 0% [0, 56] |
| memory → memory | e5f0 | last two tokens before the answer | 52 | 67% [21, 94] | 33% [6, 79] | 67% [21, 94] | 0% [0, 56] | 0% [0, 56] |

## Agent priors in the job spec (jobs/d3/d3v4_smoke_27b.yaml `hypotheses`) vs results

- H-ok: pointer_swap: self no-op and layer-0 reproduction 9/9 (3 topics x 3 families); summary has nkt_per_family and ci entity_cluster. pointer_fit: fit.json and outcomes.jsonl written; outcomes carry entity, template and cut; every steered item's cut is not "neither"; summary has pointer_v4 per_domain and per_cut
- H-broken: any check fails or a stage crashes: stop both mains

Against the saved numbers:

- H-pointer: memory → prompt, answer at the same statement slot: after the question 0% [0, 56], last two tokens 0% [0, 56] (>= 50%: not met); memory → memory 0% [0, 56] / 0% [0, 56] (<= 10%: met); named → prompt after the question 0% [0, 56] (>= 50%: not met)
- H-word: memory → prompt, answer of bridge alt's statement: 0% [0, 56] / 0% [0, 56] (>= 50%: not met)
- H-value: memory → prompt, the alt prompt's own answer: 33% [6, 79] / 67% [21, 94] (>= 50%: met); first single layer where it reaches 20%: after the question 52, last two tokens 52
- H-none: memory → prompt, answer changed after the question 33% [6, 79] (< 20%: not met)

## Worked example (from examples.json)

Item `body-RR-e5f0-0107` (memory → memory; the patched answer was the answer of bridge alt's statement). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 44 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The chart on the eye is kept in folder 7. The chart on the spine is kept in folder 3. The chart on the tongue is kept in folder 9. The chart on the knee is kept in folder 8. The chart on the skull is kept in folder 4.
How many of the body part that tastes food does a human have? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The chart on the skull is kept in folder 9. The chart on the spine is kept in folder 8. The chart on the tongue is kept in folder 7. The chart on the eye is kept in folder 6. The chart on the knee is kept in folder 3.
How many of the body part that sees colours does a human have? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 1; after the patch 2. Predicted: answer org kept 1 (p 0.405); answer of bridge alt's statement 2 (p 0.590); answer at the same statement slot 2 (p 0.590); the alt prompt's own answer 2 (p 0.590).

