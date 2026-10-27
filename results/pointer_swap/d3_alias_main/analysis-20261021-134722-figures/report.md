# d3_alias_main

Run `d3_alias_main` (results/pointer_swap/), analysis of the saved outputs only.

```
EXP d3_alias_main @ unknown | model Qwen3.6-27B | n={"RL|e5f0": 122, "RL|e5f0-xlang": 100, "RL|e5f0-syn": 22, "DL|e5f0": 122, "DL|e5f0-xlang": 100, "DL|e5f0-syn": 22} | seeds=[0, 0, 0] (sample, null, other)
Claim tested: in RL (recalled cue -> in-prompt lookup), what the tokens after the question carry at layers 44-52: the bridge's identity (H-word), a pointer to its statement's position (H-pointer), or the answer (H-value)
Headline: RL, tokens after the question, transit window (e5f0): position = 30% [23, 39]   Baseline: none = 30% [23, 39], identity = 9% [5, 15], value = 29% [21, 37]   Control: 'same' changed = 0% [0, 3]; random direction changed (max over transit layers) = 1% [0, 4]; other item changed = 7% [3, 12]
Figures: results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/by_layer_e5f0.png, results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/by_layer_e5f0-xlang.png, results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/by_layer_e5f0-syn.png, results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/slots_final_e5f0.png, results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/slots_last_e5f0.png, results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/windows_e5f0.png, results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/domains_final_e5f0.png, results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/levels_final.png, results/pointer_swap/d3_alias_main/analysis-20261021-134722-figures/levels_last.png
Three dumbest ways this could be wrong: see below
For the human to verify: results/pointer_swap/d3_alias_main/outcomes.jsonl, rows `family == 'memory → prompt'`, `group == 'final'`, `layer == 'transit'`, `source == 'alt prompt'`, `level == 'e5f0'`: count `role` (n=122); position should be 37, identity 11, value 35, none 37
Status: UNVERIFIED
```

## Three dumbest ways this could be wrong

1. Position here could be the absolute token offset rather than the statement's order: statements have equal length, so the two coincide (the filler level keeps the same layout in base and source and does not separate them). Not checked; needs an offset-shift variant.
2. Generic disruption or bf16 noise could pick an org-prompt digit that happens to be the same-slot answer. Checked: the random-push control at the same per-token norm changes memory → prompt's answer 1% [0, 4] (max over transit layers); digits of the base context that no hypothesis predicts win 2% [0, 6]; among alt prompt reads won by a predicted digit, 589/22663 have the runner-up prediction within p 0.1; hook checks self no-op 487/488, layer-0 reproduction 488/488.
3. The pooled verdict could rest on pooling: per domain the same cell's verdict is {"animals": "mixed", "elements": "damage"}; the spec reports a verdict holding in fewer than 3 of 4 domains as domain-dependent.

## Pre-registered decision rule and its verdict

Rule (scripts/pointer_swap.py docstring, written before any run):

> (fixed before any run; the job specs in jobs/d3/ repeat it). Per cell (family x group x layer or window x source alt prompt), pooled over domains, Wilson 95% intervals over items:   - interpretable iff the alt prompt patch changes the answer (1 - share 'answer org kept': lower bound >= 0.20) and the same-entity control (statements reshuffled)     changes it rarely (upper bound <= 0.10); otherwise "none" (nothing moves) or "damage"   - verdict W in {answer of bridge alt's statement, answer at the same statement slot, the alt prompt's own answer} (memory → memory: answer of bridge alt's statement, answer at the same statement slot) iff W's lower bound exceeds the upper bounds of     the other two and the chance bar: the random-push control's upper bound for W at that layer (windows: the max over the     window's layers) and the per-digit context rate (upper bound of share context / (N - 3), N = 5 only)   - otherwise "mixed". Primary: memory → prompt, group final, window transit (the suite's 98-100% copy flips at 44-52). H-pointer:     answer at the same statement slot; H-word (or a lexical key): answer of bridge alt's statement; H-the alt prompt's own answer: the alt prompt's own answer. named → prompt is the reference (classic binding retrieval),     memory → memory the contrast (a pointer is useless there).   - Other datasets name their primary / reference / contrast families in the manifest (code_pointer_v1: memory ->     prompt memory → prompt / named -> prompt named → prompt / memory → memory).

Applied to the saved outcomes (analysis summary.json `verdicts`). Primary cell(s): e5f0: **mixed** (answer org kept 30% [23, 39], answer of bridge alt's statement 9% [5, 15], answer at the same statement slot 30% [23, 39], the alt prompt's own answer 29% [21, 37]); e5f0-xlang: **no effect** (answer org kept 73% [64, 81], answer of bridge alt's statement 2% [1, 7], answer at the same statement slot 12% [7, 20], the alt prompt's own answer 12% [7, 20]); e5f0-syn: **damage** (answer org kept 32% [16, 53], answer of bridge alt's statement 14% [5, 33], answer at the same statement slot 45% [27, 65], the alt prompt's own answer 0% [0, 15])

A cell needs n >= 35 items for the same-entity control (statements reshuffled)'s Wilson upper bound to reach <= 0.1 even with zero changes (3.84 / (n + 3.84)); with n between 35 and ~53 a single same-entity-control change gives 'damage'. Cells where the rule cannot pass: 940, in cuts ['all', 'domain:elements', 'slot:first', 'slot:last', 'slot:middle'].

| family | patched tokens | level | early 16-28 | mid 32-40 | transit 44-52 |
|---|---|---|---|---|---|
| memory → prompt | question words | e5f0 | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 87%) | - | - |
| memory → prompt | question words | e5f0-xlang | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 84%) | - | - |
| memory → prompt | question words | e5f0-syn | damage (answer org kept 0%, answer of bridge alt's statement 45%) | - | - |
| memory → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 77%, answer of bridge alt's statement 13%) | mixed (answer org kept 30%, answer at the same statement slot 30%) |
| memory → prompt | everything after the question | e5f0-xlang | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 73%, answer at the same statement slot 12%) |
| memory → prompt | everything after the question | e5f0-syn | damage (answer org kept 86%, answer of bridge alt's statement 9%) | damage (answer org kept 50%, answer of bridge alt's statement 18%) | damage (answer org kept 32%, answer at the same statement slot 45%) |
| memory → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 98%, answer at the same statement slot 2%) | mixed (answer org kept 30%, the alt prompt's own answer 37%) |
| memory → prompt | last two tokens before the answer | e5f0-xlang | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer of bridge alt's statement 1%) | alt prompt's own answer (H-value) (answer org kept 36%, the alt prompt's own answer 41%) |
| memory → prompt | last two tokens before the answer | e5f0-syn | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 77%, answer of bridge alt's statement 9%) | damage (answer org kept 9%, answer of bridge alt's statement 32%) |
| memory → prompt | question words + everything after | e5f0 | - | - | - |
| memory → prompt | question words + everything after | e5f0-xlang | - | - | - |
| memory → prompt | question words + everything after | e5f0-syn | - | - | - |
| named → prompt | question words | e5f0 | mixed (answer org kept 1%, answer of bridge alt's statement 54%) | - | - |
| named → prompt | question words | e5f0-xlang | bridge alt's statement (H-word) (answer org kept 0%, answer of bridge alt's statement 84%) | - | - |
| named → prompt | question words | e5f0-syn | damage (answer org kept 0%, answer of bridge alt's statement 91%) | - | - |
| named → prompt | everything after the question | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 2%, the alt prompt's own answer 70%) |
| named → prompt | everything after the question | e5f0-xlang | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 80%, the alt prompt's own answer 11%) |
| named → prompt | everything after the question | e5f0-syn | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 64%, the alt prompt's own answer 23%) |
| named → prompt | last two tokens before the answer | e5f0 | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 85%, answer at the same statement slot 11%) |
| named → prompt | last two tokens before the answer | e5f0-xlang | no effect (answer org kept 100%, answer of bridge alt's statement 0%) | no effect (answer org kept 99%, answer of bridge alt's statement 0%) | alt prompt's own answer (H-value) (answer org kept 29%, the alt prompt's own answer 46%) |
| named → prompt | last two tokens before the answer | e5f0-syn | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 100%, answer of bridge alt's statement 0%) | damage (answer org kept 32%, the alt prompt's own answer 50%) |
| named → prompt | question words + everything after | e5f0 | - | - | - |
| named → prompt | question words + everything after | e5f0-xlang | - | - | - |
| named → prompt | question words + everything after | e5f0-syn | - | - | - |

Cuts of the primary cell (memory → prompt, tokens after the question, transit window):

| cut | level | n | control n | verdict | rule reachable | shares |
|---|---|---|---|---|---|---|
| all | e5f0 | 122 | 122 | mixed | yes | answer org kept 30% [23, 39], answer of bridge alt's statement 9% [5, 15], answer at the same statement slot 30% [23, 39], the alt prompt's own answer 29% [21, 37] |
| domain:animals | e5f0 | 100 | 100 | mixed | yes | answer org kept 25% [18, 34], answer of bridge alt's statement 10% [6, 17], answer at the same statement slot 28% [20, 37], the alt prompt's own answer 35% [26, 45] |
| domain:elements | e5f0 | 22 | 22 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 55% [35, 73], answer of bridge alt's statement 5% [1, 22], answer at the same statement slot 41% [23, 61], the alt prompt's own answer 0% [0, 15] |
| slot:first | e5f0 | 22 | 22 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 50% [31, 69], answer of bridge alt's statement 9% [3, 28], answer at the same statement slot 14% [5, 33], the alt prompt's own answer 27% [13, 48] |
| slot:middle | e5f0 | 73 | 73 | mixed | yes | answer org kept 27% [18, 39], answer of bridge alt's statement 5% [2, 13], answer at the same statement slot 36% [26, 47], the alt prompt's own answer 30% [21, 41] |
| slot:last | e5f0 | 27 | 27 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 22% [11, 41], answer of bridge alt's statement 19% [8, 37], answer at the same statement slot 30% [16, 48], the alt prompt's own answer 26% [13, 45] |
| all | e5f0-xlang | 100 | 100 | no effect | yes | answer org kept 73% [64, 81], answer of bridge alt's statement 2% [1, 7], answer at the same statement slot 12% [7, 20], the alt prompt's own answer 12% [7, 20] |
| domain:animals | e5f0-xlang | 100 | 100 | no effect | yes | answer org kept 73% [64, 81], answer of bridge alt's statement 2% [1, 7], answer at the same statement slot 12% [7, 20], the alt prompt's own answer 12% [7, 20] |
| slot:first | e5f0-xlang | 18 | 18 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 100% [82, 100], answer of bridge alt's statement 0% [0, 18], answer at the same statement slot 0% [0, 18], the alt prompt's own answer 0% [0, 18] |
| slot:middle | e5f0-xlang | 64 | 64 | mixed | yes | answer org kept 66% [53, 76], answer of bridge alt's statement 3% [1, 11], answer at the same statement slot 14% [8, 25], the alt prompt's own answer 16% [9, 26] |
| slot:last | e5f0-xlang | 18 | 18 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 72% [49, 88], answer of bridge alt's statement 0% [0, 18], answer at the same statement slot 17% [6, 39], the alt prompt's own answer 11% [3, 33] |
| all | e5f0-syn | 22 | 22 | damage (1 same-entity control changes) | NO (n < 35) | answer org kept 32% [16, 53], answer of bridge alt's statement 14% [5, 33], answer at the same statement slot 45% [27, 65], the alt prompt's own answer 0% [0, 15] |
| domain:elements | e5f0-syn | 22 | 22 | damage (1 same-entity control changes) | NO (n < 35) | answer org kept 32% [16, 53], answer of bridge alt's statement 14% [5, 33], answer at the same statement slot 45% [27, 65], the alt prompt's own answer 0% [0, 15] |
| slot:first | e5f0-syn | 4 | 4 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 50% [15, 85], answer of bridge alt's statement 50% [15, 85], answer at the same statement slot 0% [0, 49], the alt prompt's own answer 0% [0, 49] |
| slot:middle | e5f0-syn | 9 | 9 | damage (1 same-entity control changes) | NO (n < 35) | answer org kept 33% [12, 65], answer of bridge alt's statement 11% [2, 44], answer at the same statement slot 56% [27, 81], the alt prompt's own answer 0% [0, 30] |
| slot:last | e5f0-syn | 9 | 9 | damage (0 same-entity control changes) | NO (n < 35) | answer org kept 22% [6, 55], answer of bridge alt's statement 0% [0, 30], answer at the same statement slot 56% [27, 81], the alt prompt's own answer 0% [0, 30] |

## Checks

`{"self_noop": {"n": 488, "same_top": 487, "max_abs_dlogit_max": 1.25}, "layer0_all_reproduces_source": {"n": 488, "same_top": 488, "max_abs_dlogit_max": 2.3125}, "unedited_base_answer_read": {"n": 488, "base_answer": 488}}`; near ties: `{"n": 22663, "within_gap": 589, "gap": 0.1}`

## Strongest single layer per family and patch site (largest share changed; earliest on ties)

| family | level | patched tokens | layer | changed | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | e5f0 | question words | 16 | 100% [97, 100] | 0% [0, 3] | 97% [92, 99] | 2% [0, 6] | 0% [0, 3] |
| memory → prompt | e5f0 | everything after the question | 48 | 64% [55, 72] | 36% [28, 45] | 18% [12, 26] | 42% [33, 51] | 0% [0, 3] |
| memory → prompt | e5f0 | last two tokens before the answer | 56 | 100% [97, 100] | 0% [0, 3] | 0% [0, 3] | 2% [0, 6] | 98% [94, 100] |
| memory → prompt | e5f0-xlang | question words | 16 | 100% [96, 100] | 0% [0, 4] | 98% [93, 99] | 1% [0, 5] | 0% [0, 4] |
| memory → prompt | e5f0-xlang | everything after the question | 50 | 31% [23, 41] | 69% [59, 77] | 9% [5, 16] | 20% [13, 29] | 0% [0, 4] |
| memory → prompt | e5f0-xlang | last two tokens before the answer | 60 | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 100% [96, 100] |
| memory → prompt | e5f0-syn | question words | 16 | 100% [85, 100] | 0% [0, 15] | 45% [27, 65] | 27% [13, 48] | 0% [0, 15] |
| memory → prompt | e5f0-syn | everything after the question | 44 | 73% [52, 87] | 27% [13, 48] | 23% [10, 43] | 36% [20, 57] | 0% [0, 15] |
| memory → prompt | e5f0-syn | last two tokens before the answer | 56 | 100% [85, 100] | 0% [0, 15] | 9% [3, 28] | 9% [3, 28] | 77% [57, 90] |
| named → prompt | e5f0 | question words | 16 | 100% [97, 100] | 0% [0, 3] | 100% [97, 100] | 0% [0, 3] | 0% [0, 3] |
| named → prompt | e5f0 | everything after the question | 56 | 100% [97, 100] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 100% [97, 100] |
| named → prompt | e5f0 | last two tokens before the answer | 60 | 100% [97, 100] | 0% [0, 3] | 0% [0, 3] | 0% [0, 3] | 100% [97, 100] |
| named → prompt | e5f0-xlang | question words | 16 | 100% [96, 100] | 0% [0, 4] | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] |
| named → prompt | e5f0-xlang | everything after the question | 50 | 20% [13, 29] | 80% [71, 87] | 4% [2, 10] | 16% [10, 24] | 0% [0, 4] |
| named → prompt | e5f0-xlang | last two tokens before the answer | 56 | 100% [96, 100] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 100% [96, 100] |
| named → prompt | e5f0-syn | question words | 16 | 100% [85, 100] | 0% [0, 15] | 100% [85, 100] | 0% [0, 15] | 0% [0, 15] |
| named → prompt | e5f0-syn | everything after the question | 56 | 59% [39, 77] | 41% [23, 61] | 0% [0, 15] | 0% [0, 15] | 59% [39, 77] |
| named → prompt | e5f0-syn | last two tokens before the answer | 56 | 100% [85, 100] | 0% [0, 15] | 0% [0, 15] | 0% [0, 15] | 100% [85, 100] |

## Level contrasts (spec rule: Newcombe 95% interval of the share difference vs e5f0; 'same' if within +-0.15, 'differs' if it excludes 0 and |diff| > 0.15)

| contrast | interpretable | answer org kept | answer of bridge alt's statement | answer at the same statement slot | the alt prompt's own answer |
|---|---|---|---|---|---|
| e5f0-xlang_vs_e5f0|domain:animals|final | False | +48 [+35, +59] differs | -8 [-16, -1] unclear | -16 [-27, -5] differs | -23 [-34, -11] differs |
| e5f0-xlang_vs_e5f0|domain:animals|last | True | +0 [-13, +13] same | -6 [-13, +0] same | -4 [-15, +8] unclear | +9 [-4, +22] unclear |
| e5f0-syn_vs_e5f0|domain:elements|final | False | -23 [-47, +6] unclear | +9 [-10, +29] unclear | +5 [-23, +31] unclear | +0 [-15, +15] same |
| e5f0-syn_vs_e5f0|domain:elements|last | False | +5 [-14, +24] unclear | +27 [+4, +48] differs | -5 [-30, +21] unclear | -36 [-58, -7] differs |

## Agent priors in the job spec (jobs/d3/d3_alias_main.yaml `hypotheses`) vs results

- H-pointer-survives: memory -> prompt, after the question, window 44-52: answer at the same statement slot in the other language within 15 points of English (Newcombe CI, same topic), answer of bridge alt's statement lower by > 15
- H-lexical: the slot answer drops by > 15 points with the other language or symbol
- prior: Agent prior: H-pointer-survives 0.5, H-lexical 0.3, unclear 0.2.

Against the saved numbers:

- e5f0-xlang_vs_e5f0|domain:animals|final (interpretable: False): answer org kept +48 [+35, +59] differs, answer of bridge alt's statement -8 [-16, -1] unclear, answer at the same statement slot -16 [-27, -5] differs, the alt prompt's own answer -23 [-34, -11] differs
- e5f0-xlang_vs_e5f0|domain:animals|last (interpretable: True): answer org kept +0 [-13, +13] same, answer of bridge alt's statement -6 [-13, +0] same, answer at the same statement slot -4 [-15, +8] unclear, the alt prompt's own answer +9 [-4, +22] unclear
- e5f0-syn_vs_e5f0|domain:elements|final (interpretable: False): answer org kept -23 [-47, +6] unclear, answer of bridge alt's statement +9 [-10, +29] unclear, answer at the same statement slot +5 [-23, +31] unclear, the alt prompt's own answer +0 [-15, +15] same
- e5f0-syn_vs_e5f0|domain:elements|last (interpretable: False): answer org kept +5 [-14, +24] unclear, answer of bridge alt's statement +27 [+4, +48] differs, answer at the same statement slot -5 [-30, +21] unclear, the alt prompt's own answer -36 [-58, -7] differs
- H-robust / H-contiguity: this run's leading outcome at 5 statements (memory → prompt, everything after the question, layers 44-52) is 'answer at the same statement slot'; e5f4 vs e5f0 for it: see the rows above ('same' = within 0.15 supports H-robust, 'differs' with a drop H-contiguity, 'unclear' neither).
- H-fewer-entities: the e3f0_vs_e5f0 'answer at the same statement slot' entries above ('differs' with a positive difference supports it).

## Worked example (from examples.json)

Item `animals-RL-e5f0-m0125` (memory → prompt; the patched answer was the answer at the same statement slot). org prompt's hidden states at the final tokens replaced by the alt prompt's at layer 44 (one forward, answer read after 'Answer:' and a space).

Org prompt (as fed):

```
<|im_start|>user
The pig's locker is 8. The dog's locker is 7. The cow's locker is 1. The horse's locker is 5. The chicken's locker is 9.
Which locker belongs to the animal known for barking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Alt prompt:

```
<|im_start|>user
The chicken's locker is 3. The pig's locker is 6. The cow's locker is 9. The horse's locker is 8. The dog's locker is 1.
Which locker belongs to the animal known for clucking? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Answers: answer org 7; after the patch 8. Predicted: answer org kept 7 (p 0.094); answer of bridge alt's statement 9 (p 0.001); answer at the same statement slot 8 (p 0.892); the alt prompt's own answer 3 (p 0.000).

