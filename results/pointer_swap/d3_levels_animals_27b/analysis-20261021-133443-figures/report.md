# D3: 3 vs 5 statements, and filler sentences between them (animals)

Run `d3_levels_animals_27b` (results/pointer_swap/), analysis of the saved outputs only.

```
EXP d3_levels_animals_27b @ 9a100de | model Qwen3.6-27B | n={"RL|e3f0": 60, "RL|e5f0": 56, "RL|e5f4": 60, "DL|e3f0": 60, "DL|e5f0": 56, "DL|e5f4": 60, "RR|e3f0": 60, "RR|e5f0": 56, "RR|e5f4": 60} | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in RL (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: RL, tokens after the question, transit window (e5f0): position = 21% [13, 34]   Baseline: none = 27% [17, 40], identity = 20% [11, 32], value = 32% [21, 45]   Control: 'same' changed = 0% [0, 6]; random direction changed (max over transit layers) = 0% [0, 6]; other item changed = 0% [0, 6]
Figures: results/pointer_swap/d3_levels_animals_27b/analysis-20261021-133443-figures/by_layer_e3f0.png, results/pointer_swap/d3_levels_animals_27b/analysis-20261021-133443-figures/by_layer_e5f0.png, results/pointer_swap/d3_levels_animals_27b/analysis-20261021-133443-figures/by_layer_e5f4.png, results/pointer_swap/d3_levels_animals_27b/analysis-20261021-133443-figures/slots_final_e5f0.png, results/pointer_swap/d3_levels_animals_27b/analysis-20261021-133443-figures/slots_last_e5f0.png, results/pointer_swap/d3_levels_animals_27b/analysis-20261021-133443-figures/windows_e5f0.png, results/pointer_swap/d3_levels_animals_27b/analysis-20261021-133443-figures/levels_final.png, results/pointer_swap/d3_levels_animals_27b/analysis-20261021-133443-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_levels_animals_27b/outcomes.jsonl, rows `family == 'memory → prompt'`, `group == 'final'`, `layer == 'transit'`, `source == 'alt prompt'`, `level == 'e5f0'`: count `role` (n=56); position should be 12, identity 11, value 18, none 15
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 0% [0, 6] (max over transit layers); digits of the base context that no hypothesis predicts win 0% [0, 6]; among alt prompt reads won by a predicted digit, 324/39990 have the runner-up prediction within p 0.1; hook checks self no-op 528/528, layer-0 reproduction 528/528.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "mixed"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e3f0: **mixed** (answer org kept 25% [16, 37], answer of bridge alt's statement 2% [0, 9], answer at the same statement slot 37% [26, 49], the alt prompt's own answer 37% [26, 49]); e5f0: **mixed** (answer org kept 27% [17, 40], answer of bridge alt's statement 20% [11, 32], answer at the same statement slot 21% [13, 34], the alt prompt's own answer 32% [21, 45]); e5f4: **mixed** (answer org kept 28% [19, 41], answer of bridge alt's statement 15% [8, 26], answer at the same statement slot 20% [12, 32], the alt prompt's own answer 37% [26, 49])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 1824, in cuts ['slot:first', 'slot:last', 'slot:middle'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e3f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 97%) | mixed (answer org kept 5%, answer of bridge alt's statement 57%) | no effect (answer org kept 98%, answer at the same statement slot 2%) |
| memory → prompt | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 96%) | bridge alt's statement (H-word) (answer org kept 4%, answer of bridge alt's statement 75%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | question words | e5f4 | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 92%) | bridge alt's statement (H-word) (answer org kept 5%, answer of bridge alt's statement 77%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → prompt | everything after the question | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 70%, answer of bridge alt's statement 20%) | mixed (answer org kept 25%, answer at the same statement slot 37%) |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 89%, answer of bridge alt's statement 9%) | mixed (answer org kept 27%, the alt prompt's own answer 32%) |
| memory → prompt | everything after the question | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 88%, answer of bridge alt's statement 7%) | mixed (answer org kept 28%, the alt prompt's own answer 37%) |
| memory → prompt | last two tokens before the answer | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 37%, answer at the same statement slot 45%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 29%, the alt prompt's own answer 32%) |
| memory → prompt | last two tokens before the answer | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 32%, the alt prompt's own answer 43%) |
| memory → prompt | question words + everything after | e3f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 90%) | mixed (answer org kept 2%, answer of bridge alt's statement 53%) | same statement slot (H-pointer) (answer org kept 12%, answer at the same statement slot 55%) |
| memory → prompt | question words + everything after | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 96%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 80%) | mixed (answer org kept 11%, answer at the same statement slot 32%) |
| memory → prompt | question words + everything after | e5f4 | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 90%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 82%) | mixed (answer org kept 10%, answer of bridge alt's statement 37%) |
| named → prompt | question words | e3f0 | same statement slot (H-pointer) (answer org kept 0%, answer at the same statement slot 80%) | same statement slot (H-pointer) (answer org kept 0%, answer at the same statement slot 65%) | same statement slot (H-pointer) (answer org kept 27%, answer at the same statement slot 68%) |
| named → prompt | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 66%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 66%) | mixed (answer org kept 16%, answer at the same statement slot 46%) |
| named → prompt | question words | e5f4 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 75%) | bridge alt's statement (H-word) (answer org kept 3%, answer of bridge alt's statement 72%) | mixed (answer org kept 27%, answer of bridge alt's statement 42%) |
| named → prompt | everything after the question | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 12%, answer at the same statement slot 53%) |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 73%) |
| named → prompt | everything after the question | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 7%, the alt prompt's own answer 60%) |
| named → prompt | last two tokens before the answer | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | same statement slot (H-pointer) (answer org kept 47%, answer at the same statement slot 45%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 79%, answer of bridge alt's statement 7%) |
| named → prompt | last two tokens before the answer | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | mixed (answer org kept 60%, the alt prompt's own answer 23%) |
| named → prompt | question words + everything after | e3f0 | same statement slot (H-pointer) (answer org kept 0%, answer at the same statement slot 80%) | same statement slot (H-pointer) (answer org kept 0%, answer at the same statement slot 65%) | same statement slot (H-pointer) (answer org kept 10%, answer at the same statement slot 58%) |
| named → prompt | question words + everything after | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 68%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 66%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 70%) |
| named → prompt | question words + everything after | e5f4 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 75%) | bridge alt's statement (H-word) (answer org kept 3%, answer of bridge alt's statement 70%) | alt prompt's own answer (H-value) (answer org kept 0%, the alt prompt's own answer 60%) |
| memory → memory | question words | e3f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 83%) | no effect (answer org kept 98%, answer at the same statement slot 2%) |
| memory → memory | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 89%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) |
| memory → memory | question words | e5f4 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 93%) | no effect (answer org kept 98%, answer of bridge alt's statement 2%) |
| memory → memory | everything after the question | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 95%, answer of bridge alt's statement 5%) |
| memory → memory | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 86%, answer of bridge alt's statement 14%) |
| memory → memory | everything after the question | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer of bridge alt's statement 2%) | no effect (answer org kept 93%, answer of bridge alt's statement 7%) |
| memory → memory | last two tokens before the answer | e3f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 43%, answer of bridge alt's statement 57%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) |
| memory → memory | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 34%, answer of bridge alt's statement 66%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 98%) |
| memory → memory | last two tokens before the answer | e5f4 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | bridge alt's statement (H-word) (answer org kept 33%, answer of bridge alt's statement 63%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) |
| memory → memory | question words + everything after | e3f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 90%) | no effect (answer org kept 80%, answer of bridge alt's statement 18%) |
| memory → memory | question words + everything after | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) | bridge alt's statement (H-word) (answer org kept 2%, answer of bridge alt's statement 91%) | bridge alt's statement (H-word) (answer org kept 68%, answer of bridge alt's statement 32%) |
| memory → memory | question words + everything after | e5f4 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 100%) | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 97%) | bridge alt's statement (H-word) (answer org kept 68%, answer of bridge alt's statement 30%) |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e3f0 | 60 | 60 | mixed | yes | answer org kept 25% [16, 37], answer of bridge alt's statement 2% [0, 9], answer at the same statement slot 37% [26, 49], the alt prompt's own answer 37% [26, 49] |
| domain:animals | e3f0 | 60 | 60 | mixed | yes | answer org kept 25% [16, 37], answer of bridge alt's statement 2% [0, 9], answer at the same statement slot 37% [26, 49], the alt prompt's own answer 37% [26, 49] |
| slot:first | e3f0 | 20 | 20 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 30% [15, 52], answer of bridge alt's statement 5% [1, 24], answer at the same statement slot 35% [18, 57], the alt prompt's own answer 30% [15, 52] |
| slot:middle | e3f0 | 20 | 20 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 25% [11, 47], answer of bridge alt's statement 0% [-0, 16], answer at the same statement slot 30% [15, 52], the alt prompt's own answer 45% [26, 66] |
| slot:last | e3f0 | 20 | 20 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 20% [8, 42], answer of bridge alt's statement 0% [-0, 16], answer at the same statement slot 45% [26, 66], the alt prompt's own answer 35% [18, 57] |
| all | e5f0 | 56 | 56 | mixed | yes | answer org kept 27% [17, 40], answer of bridge alt's statement 20% [11, 32], answer at the same statement slot 21% [13, 34], the alt prompt's own answer 32% [21, 45] |
| domain:animals | e5f0 | 56 | 56 | mixed | yes | answer org kept 27% [17, 40], answer of bridge alt's statement 20% [11, 32], answer at the same statement slot 21% [13, 34], the alt prompt's own answer 32% [21, 45] |
| slot:first | e5f0 | 12 | 12 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 42% [19, 68], answer of bridge alt's statement 33% [14, 61], answer at the same statement slot 0% [0, 24], the alt prompt's own answer 25% [9, 53] |
| slot:middle | e5f0 | 33 | 33 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 21% [11, 38], answer of bridge alt's statement 21% [11, 38], answer at the same statement slot 27% [15, 44], the alt prompt's own answer 30% [17, 47] |
| slot:last | e5f0 | 11 | 11 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 27% [10, 57], answer of bridge alt's statement 0% [0, 26], answer at the same statement slot 27% [10, 57], the alt prompt's own answer 45% [21, 72] |
| all | e5f4 | 60 | 60 | mixed | yes | answer org kept 28% [19, 41], answer of bridge alt's statement 15% [8, 26], answer at the same statement slot 20% [12, 32], the alt prompt's own answer 37% [26, 49] |
| domain:animals | e5f4 | 60 | 60 | mixed | yes | answer org kept 28% [19, 41], answer of bridge alt's statement 15% [8, 26], answer at the same statement slot 20% [12, 32], the alt prompt's own answer 37% [26, 49] |
| slot:first | e5f4 | 12 | 12 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 67% [39, 86], answer of bridge alt's statement 25% [9, 53], answer at the same statement slot 0% [0, 24], the alt prompt's own answer 8% [1, 35] |
| slot:middle | e5f4 | 36 | 36 | mixed | yes | answer org kept 19% [10, 35], answer of bridge alt's statement 14% [6, 29], answer at the same statement slot 22% [12, 38], the alt prompt's own answer 44% [30, 60] |
| slot:last | e5f4 | 12 | 12 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 17% [5, 45], answer of bridge alt's statement 8% [1, 35], answer at the same statement slot 33% [14, 61], the alt prompt's own answer 42% [19, 68] |

## Checks

`{"self_noop": {"n": 528, "same_top": 528, "max_abs_dlogit_max": 1.125}, "layer0_all_reproduces_source": {"n": 528, "same_top": 528, "max_abs_dlogit_max": 1.5}, "unedited_base_answer_read": {"n": 528, "base_answer": 528}}`; near ties: `{"n": 39990, "within_gap": 324, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e3f0 | question words | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → prompt | e3f0 | everything after the question | 56 | 82% [70, 89] | 18% [11, 30] | 0% [-0, 6] | 0% [-0, 6] | 82% [70, 89] |
| memory → prompt | e3f0 | last two tokens before the answer | 56 | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] | 2% [0, 9] | 98% [91, 100] |
| memory → prompt | e3f0 | question words + everything after | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → prompt | e5f0 | question words | 0 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| memory → prompt | e5f0 | everything after the question | 48 | 77% [64, 86] | 23% [14, 36] | 30% [20, 43] | 39% [28, 52] | 0% [0, 6] |
| memory → prompt | e5f0 | last two tokens before the answer | 56 | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] | 0% [0, 6] | 100% [94, 100] |
| memory → prompt | e5f0 | question words + everything after | 0 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| memory → prompt | e5f4 | question words | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → prompt | e5f4 | everything after the question | 56 | 68% [56, 79] | 32% [21, 44] | 0% [-0, 6] | 0% [-0, 6] | 68% [56, 79] |
| memory → prompt | e5f4 | last two tokens before the answer | 56 | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] | 0% [-0, 6] | 100% [94, 100] |
| memory → prompt | e5f4 | question words + everything after | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| named → prompt | e3f0 | question words | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| named → prompt | e3f0 | everything after the question | 56 | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] | 0% [-0, 6] | 100% [94, 100] |
| named → prompt | e3f0 | last two tokens before the answer | 60 | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] | 0% [-0, 6] | 100% [94, 100] |
| named → prompt | e3f0 | question words + everything after | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| named → prompt | e5f0 | question words | 0 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| named → prompt | e5f0 | everything after the question | 56 | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] | 0% [0, 6] | 100% [94, 100] |
| named → prompt | e5f0 | last two tokens before the answer | 60 | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] | 0% [0, 6] | 100% [94, 100] |
| named → prompt | e5f0 | question words + everything after | 0 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| named → prompt | e5f4 | question words | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| named → prompt | e5f4 | everything after the question | 56 | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] | 0% [-0, 6] | 100% [94, 100] |
| named → prompt | e5f4 | last two tokens before the answer | 56 | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] | 0% [-0, 6] | 100% [94, 100] |
| named → prompt | e5f4 | question words + everything after | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e3f0 | question words | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e3f0 | everything after the question | 52 | 3% [1, 11] | 97% [89, 99] | 3% [1, 11] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e3f0 | last two tokens before the answer | 52 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e3f0 | question words + everything after | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e5f0 | question words | 0 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| memory → memory | e5f0 | everything after the question | 48 | 11% [5, 21] | 89% [79, 95] | 11% [5, 21] | 0% [0, 6] | 0% [0, 6] |
| memory → memory | e5f0 | last two tokens before the answer | 60 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| memory → memory | e5f0 | question words + everything after | 0 | 100% [94, 100] | 0% [0, 6] | 100% [94, 100] | 0% [0, 6] | 0% [0, 6] |
| memory → memory | e5f4 | question words | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e5f4 | everything after the question | 52 | 7% [3, 16] | 93% [84, 97] | 7% [3, 16] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e5f4 | last two tokens before the answer | 52 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |
| memory → memory | e5f4 | question words + everything after | 0 | 100% [94, 100] | 0% [-0, 6] | 100% [94, 100] | 0% [-0, 6] | 0% [-0, 6] |

## Level contrasts (spec rule: Newcombe 95% interval of the share difference vs e5f0; 'same' if within +-0.15, 'differs' if it excludes 0 and |diff| > 0.15)

| contrast | interpretable | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|
| e3f0_vs_e5f0|final | True | -2 [-18, +14] unclear | -18 [-30, -7] differs | +15 [-1, +31] unclear | +5 [-13, +21] unclear |
| e3f0_vs_e5f0|last | True | +8 [-9, +24] unclear | -16 [-28, -7] differs | +22 [+4, +37] differs | -14 [-29, +2] unclear |
| e5f4_vs_e5f0|final | True | +2 [-15, +17] unclear | -5 [-19, +9] unclear | -1 [-16, +13] unclear | +5 [-13, +21] unclear |
| e5f4_vs_e5f0|last | True | +3 [-13, +19] unclear | -6 [-19, +6] unclear | -8 [-23, +6] unclear | +11 [-6, +28] unclear |

## Agent priors in the job spec (jobs/d3/d3_levels_animals_27b.yaml `hypotheses`) vs results

- H-robust: memory → prompt final/last at the transit window: the pilot's winning outcome keeps its share at e5f4 within 0.15
- H-contiguity: the winning outcome's share drops by more than 0.15 with filler (e5f4 vs e5f0)
- H-fewer-entities: answer at the same statement slot share at e3f0 above e5f0 by more than 0.15 (positional route dominates at N=3)
- prior: Coordinator prior: H-robust 0.65; H-fewer-entities 0.4.

Against the saved numbers:

- e3f0_vs_e5f0|final (interpretable: True): answer org kept -2 [-18, +14] unclear, answer of bridge alt's statement -18 [-30, -7] differs, answer at the same statement slot +15 [-1, +31] unclear, the alt prompt's own answer +5 [-13, +21] unclear
- e3f0_vs_e5f0|last (interpretable: True): answer org kept +8 [-9, +24] unclear, answer of bridge alt's statement -16 [-28, -7] differs, answer at the same statement slot +22 [+4, +37] differs, the alt prompt's own answer -14 [-29, +2] unclear
- e5f4_vs_e5f0|final (interpretable: True): answer org kept +2 [-15, +17] unclear, answer of bridge alt's statement -5 [-19, +9] unclear, answer at the same statement slot -1 [-16, +13] unclear, the alt prompt's own answer +5 [-13, +21] unclear
- e5f4_vs_e5f0|last (interpretable: True): answer org kept +3 [-13, +19] unclear, answer of bridge alt's statement -6 [-19, +6] unclear, answer at the same statement slot -8 [-23, +6] unclear, the alt prompt's own answer +11 [-6, +28] unclear
- H-robust / H-contiguity: this run's leading outcome at 5 statements (memory → prompt, everything after the question, layers 44-52) is 'the alt prompt's own answer'; e5f4 vs e5f0 for it: see the rows above ('same' = within 0.15 supports H-robust, 'differs' with a drop H-contiguity, 'unclear' neither).
- H-fewer-entities: the e3f0_vs_e5f0 'answer at the same statement slot' entries above ('differs' with a positive difference supports it).

## Worked example (from examples.json)

Item `animals-RL-e5f0-0057` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 48 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The bee's locker is 7. The goose's locker is 9. The duck's locker is 8. The mouse's locker is 3. The horse's locker is 5.
Which locker belongs to the animal known for neighing? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The goose's locker is 1. The duck's locker is 3. The bee's locker is 7. The mouse's locker is 5. The horse's locker is 8.
Which locker belongs to the animal known for honking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 5; after the patch 7. Predicted: answer org kept 5 (p 0.004); answer of bridge alt's statement 9 (p 0.000); answer at the same statement slot 7 (p 0.989); the alt prompt's own answer 1 (p 0.001).

