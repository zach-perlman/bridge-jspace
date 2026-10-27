# early_push_where / d4_shared_code_27b (rule v2)

Items: [{'family': 'BL', 'n': 100, 'right_unedited': 100}, {'family': 'BR', 'n': 100, 'right_unedited': 100}, {'family': 'RL', 'n': 100, 'right_unedited': 100}, {'family': 'RR', 'n': 100, 'right_unedited': 100}]

**Verdict:** H-around: the lens writes a stated bridge for recall but not for a lookup where it sits

Primary cell: subset w, layer 28, 4x (valid: True)

- BL: 0% [0, 4]
- BR: 65% [55, 74]
- BL_random: 0% [0, 4]
- RL_changed: 1% [0, 5]
- RR_changed: 9% [5, 16]
- BR - BL (scene-paired, 100 scenes): +65 [+56, +74] points

Selected cells (BR rows only): 2

**Shared code (w, 8x):** H-none: the form is scene-specific, not a reusable linear code (patch_dir read from d4_layer_gap_dose_27b)

Median over scenes, by layer: cosine with the lens push's direction (with / without its J-space part), share of its squared norm in its J-space part: 20: +0.31 / +0.00, 27%; 24: +0.28 / +0.01, 24%; 28: +0.42 / +0.02, 36%

Lookups switched to X (prompt → prompt), at the word:

| layer | shared_perp 4x | shared_perp 8x | shared 4x | shared 8x | lens 4x | lens 8x | random 4x | random 8x | valid (shared_perp) |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 20% [13, 29] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | True |
| 24 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 11% [6, 19] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | True |
| 28 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | True |

Recalls switched to X (prompt → memory), at the word:

| layer | shared_perp 4x | shared_perp 8x | shared 4x | shared 8x | lens 4x | lens 8x | random 4x | random 8x | valid (shared_perp) |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 0% [0, 4] | 13% [8, 21] | 7% [3, 14] | 80% [71, 87] | 6% [3, 12] | 71% [61, 79] | 0% [0, 4] | 0% [0, 4] | True |
| 24 | 0% [0, 4] | 5% [2, 11] | 8% [4, 15] | 79% [70, 86] | 41% [32, 51] | 85% [77, 91] | 0% [0, 4] | 0% [0, 4] | True |
| 28 | 0% [0, 4] | 5% [2, 11] | 35% [26, 45] | 100% [96, 100] | 65% [55, 74] | 99% [95, 100] | 0% [0, 4] | 0% [0, 4] | True |

Same role as d4_layer_gap_v2_27b, item by item: lens 2393/2400, offscene 2396/2400, random 2400/2400

Slide 6 anchor (b, layer 20, 8x, lens): BL - (slide 6: 1%), BR - (slide 6: 2%), RL - (slide 6: 73%), RR - (slide 6: 84%)

| family | where | layer | scale | lens → X | random → X | off-scene: changed | off-scene → Y |
|---|---|---|---|---|---|---|---|
| BL | w | 20 | 4 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] |
| BL | w | 20 | 8 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] |
| BL | w | 24 | 4 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] |
| BL | w | 24 | 8 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] |
| BL | w | 28 | 4 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] |
| BL | w | 28 | 8 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] |
| BR | w | 20 | 4 | 6% [3, 12] | 0% [0, 4] | 5% [2, 11] | 4% [2, 10] |
| BR | w | 20 | 8 | 71% [61, 79] | 0% [0, 4] | 81% [72, 87] | 76% [67, 83] |
| BR | w | 24 | 4 | 41% [32, 51] | 0% [0, 4] | 32% [24, 42] | 26% [18, 35] |
| BR | w | 24 | 8 | 85% [77, 91] | 0% [0, 4] | 90% [83, 94] | 86% [78, 91] |
| BR | w | 28 | 4 | 65% [55, 74] | 0% [0, 4] | 67% [57, 75] | 64% [54, 73] |
| BR | w | 28 | 8 | 99% [95, 100] | 0% [0, 4] | 99% [95, 100] | 96% [90, 98] |
| RL | w | 20 | 4 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] |
| RL | w | 20 | 8 | 1% [0, 5] | 0% [0, 4] | 17% [11, 26] | 0% [0, 4] |
| RL | w | 24 | 4 | 0% [0, 4] | 0% [0, 4] | 2% [1, 7] | 0% [0, 4] |
| RL | w | 24 | 8 | 3% [1, 8] | 0% [0, 4] | 22% [15, 31] | 0% [0, 4] |
| RL | w | 28 | 4 | 0% [0, 4] | 0% [0, 4] | 1% [0, 5] | 0% [0, 4] |
| RL | w | 28 | 8 | 0% [0, 4] | 0% [0, 4] | 9% [5, 16] | 0% [0, 4] |
| RR | w | 20 | 4 | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] | 0% [0, 4] |
| RR | w | 20 | 8 | 5% [2, 11] | 0% [0, 4] | 7% [3, 14] | 4% [2, 10] |
| RR | w | 24 | 4 | 3% [1, 8] | 0% [0, 4] | 1% [0, 5] | 1% [0, 5] |
| RR | w | 24 | 8 | 4% [2, 10] | 0% [0, 4] | 6% [3, 12] | 2% [1, 7] |
| RR | w | 28 | 4 | 9% [5, 16] | 0% [0, 4] | 10% [6, 17] | 9% [5, 16] |
| RR | w | 28 | 8 | 35% [26, 45] | 0% [0, 4] | 31% [23, 41] | 25% [18, 34] |

| family | edit | n | → X | changed |
|---|---|---|---|---|
| BL | E-cue | 100 | 100% [96, 100] | 100% [96, 100] |
| BL | E-head | 100 | 81% [72, 87] | 81% [72, 87] |
| BL | E-insert | 100 | 1% [0, 5] | 1% [0, 5] |
| BL | E-name | 100 | 100% [96, 100] | 100% [96, 100] |
| BL | E-unrelated | 100 | 0% [0, 4] | 0% [0, 4] |
| BR | E-cue | 100 | 100% [96, 100] | 100% [96, 100] |
| BR | E-head | 100 | 40% [31, 50] | 100% [96, 100] |
| BR | E-insert | 100 | 98% [93, 99] | 98% [93, 99] |
| BR | E-name | 100 | 100% [96, 100] | 100% [96, 100] |
| BR | E-unrelated | 100 | 0% [0, 4] | 0% [0, 4] |
| RL | E-cue | 100 | 100% [96, 100] | 100% [96, 100] |
| RL | E-head | 100 | 72% [63, 80] | 72% [63, 80] |
| RL | E-insert | 100 | 100% [96, 100] | 100% [96, 100] |
| RL | E-name | 100 | 100% [96, 100] | 100% [96, 100] |
| RL | E-unrelated | 100 | 0% [0, 4] | 0% [0, 4] |
| RR | E-cue | 100 | 100% [96, 100] | 100% [96, 100] |
| RR | E-head | 100 | 44% [35, 54] | 97% [92, 99] |
| RR | E-insert | 100 | 92% [85, 96] | 93% [86, 97] |
| RR | E-name | 100 | 100% [96, 100] | 100% [96, 100] |
| RR | E-unrelated | 100 | 0% [0, 4] | 0% [0, 4] |
