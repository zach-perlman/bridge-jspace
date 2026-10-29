# 53.7 (the pointer in code and tool output): the address probe in code and tool output

Batch 53, 53.7 (Dan 11:10); no prediction; UNVERIFIED. Spec: jobs/c3/batch53.yaml (next_1110 item 2, standing_rules_0950 item 6, next_1110_reading_537).

Rule: none of its own (x0_probe v4 is descriptive, added after the data). Pre-stated reading (Dan, x0_probe): (a) high in locker-before and at chance in locker-after -> the answer value is stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address (a lookback-style pointer). In locker-after scenes the locker sentence follows the word, so (a) and (b) cannot be read there from the locker sentence itself: that stratum is the control by construction.

Gate (53.7): X0's main gate in the format, over the test's own scenes: the unedited O prompt's chat read right on >= 0.80 of the scenes for both readers; a failed format is not tested (no states, no probe).

- code: the scene as Python in the user turn (tasks_v2's code framing): picks = {} and lockers = {}, then one assignment per statement in the scene's order (picks["Eva"] = "oxygen"; lockers["oxygen"] = 5), then the question and the digit instruction.
- tool: the scene's text verbatim as the response of a declared tool (get_notes) in the model's chat template, after the user's 'Look up my notes.' and the assistant's call; the question and the instruction in a new user turn.

| model | format | layer | aligned scenes | gate (lookup / recall) | status |
|---|---|---|---|---|---|
| Qwen3.5-9B | code | L12 | 682 | 0.828 / 0.727 | not tested (gate 0.727 < 0.80) |
| Qwen3.5-9B | tool | L12 | 1500 | 0.981 / 0.815 | tested |
| Qwen3.6-27B | code | L32 | 682 | 0.996 / 0.880 | tested |
| Qwen3.6-27B | tool | L32 | 1500 | 0.997 / 0.967 | tested |

## Probe accuracy (every scene of the run; folds by bridge entity for (a), (b), by item for (c))

| model | format | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | layout | probe - best baseline | prose v4 probe (beside) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | tool | before | answer digit | 758 | 46 | 9 | 0.26 [0.23, 0.30] | 0.10 [0.07, 0.13] | 0.11 | - | - | 0.15 [0.11, 0.19] (chance) | 0.27 [0.24, 0.31] |
| Qwen3.5-9B | tool | before | locker sentence | 758 | 46 | 5 | 0.97 [0.95, 0.98] | 0.33 [0.30, 0.36] | 0.20 | 0.35 [0.32, 0.39] | 0.53 [0.50, 0.56] | 0.44 [0.41, 0.47] (layout) | 0.97 [0.96, 0.98] |
| Qwen3.5-9B | tool | before | bridge identity | 758 | 46 | 46 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.21] | 0.02 | - | - | 0.93 [0.79, 1.00] (majority) | 1.00 [1.00, 1.00] |
| Qwen3.5-9B | tool | after | answer digit | 742 | 46 | 9 | 0.11 [0.09, 0.14] | 0.13 [0.11, 0.16] | 0.11 | - | - | -0.02 [-0.05, 0.01] (majority) | 0.10 [0.08, 0.13] |
| Qwen3.5-9B | tool | after | locker sentence | 742 | 46 | 5 | 0.31 [0.28, 0.34] | 0.33 [0.30, 0.36] | 0.20 | 0.37 [0.34, 0.40] | 0.36 [0.33, 0.39] | -0.06 [-0.10, -0.02] (structure) | 0.34 [0.30, 0.37] |
| Qwen3.5-9B | tool | after | bridge identity | 742 | 46 | 46 | 1.00 [1.00, 1.00] | 0.06 [0.00, 0.20] | 0.02 | - | - | 0.94 [0.80, 1.00] (majority) | 1.00 [1.00, 1.00] |
| Qwen3.5-9B | tool | both | answer digit | 1500 | 46 | 9 | 0.17 [0.15, 0.18] | 0.12 [0.10, 0.13] | 0.11 | - | - | 0.05 [0.02, 0.08] (majority) | 0.17 [0.15, 0.19] |
| Qwen3.5-9B | tool | both | locker sentence | 1500 | 46 | 6 | 0.63 [0.61, 0.65] | 0.17 [0.15, 0.18] | 0.17 | 0.22 [0.20, 0.24] | 0.33 [0.31, 0.35] | 0.30 [0.28, 0.32] (layout) | 0.65 [0.63, 0.67] |
| Qwen3.5-9B | tool | both | bridge identity | 1500 | 46 | 46 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.21] | 0.02 | - | - | 0.93 [0.79, 1.00] (majority) | 1.00 [1.00, 1.00] |
| Qwen3.6-27B | code | before | answer digit | 349 | 28 | 9 | 0.30 [0.23, 0.35] | 0.12 [0.08, 0.15] | 0.11 | - | - | 0.18 [0.12, 0.22] (majority) | 0.40 [0.36, 0.44] |
| Qwen3.6-27B | code | before | locker sentence | 349 | 28 | 5 | 0.95 [0.93, 0.98] | 0.29 [0.25, 0.33] | 0.20 | 0.26 [0.22, 0.30] | 0.48 [0.42, 0.53] | 0.48 [0.42, 0.54] (layout) | 0.99 [0.98, 1.00] |
| Qwen3.6-27B | code | before | bridge identity | 349 | 28 | 28 | 0.99 [0.96, 1.00] | 0.11 [0.00, 0.34] | 0.04 | - | - | 0.87 [0.64, 0.99] (majority) | 1.00 [1.00, 1.00] |
| Qwen3.6-27B | code | after | answer digit | 333 | 29 | 9 | 0.12 [0.09, 0.14] | 0.15 [0.11, 0.19] | 0.11 | - | - | -0.03 [-0.06, 0.00] (majority) | 0.11 [0.08, 0.14] |
| Qwen3.6-27B | code | after | locker sentence | 333 | 29 | 5 | 0.38 [0.34, 0.43] | 0.36 [0.32, 0.39] | 0.20 | 0.29 [0.25, 0.32] | 0.32 [0.27, 0.37] | 0.03 [-0.01, 0.07] (majority) | 0.34 [0.31, 0.37] |
| Qwen3.6-27B | code | after | bridge identity | 333 | 29 | 29 | 0.98 [0.96, 0.99] | 0.11 [0.00, 0.23] | 0.03 | - | - | 0.88 [0.75, 0.99] (majority) | 1.00 [1.00, 1.00] |
| Qwen3.6-27B | code | both | answer digit | 682 | 29 | 9 | 0.20 [0.17, 0.22] | 0.09 [0.06, 0.12] | 0.11 | - | - | 0.09 [0.06, 0.11] (chance) | 0.23 [0.20, 0.26] |
| Qwen3.6-27B | code | both | locker sentence | 682 | 29 | 6 | 0.64 [0.61, 0.66] | 0.14 [0.11, 0.16] | 0.17 | 0.17 [0.14, 0.20] | 0.28 [0.24, 0.32] | 0.36 [0.32, 0.39] (layout) | 0.66 [0.64, 0.68] |
| Qwen3.6-27B | code | both | bridge identity | 682 | 29 | 29 | 1.00 [0.99, 1.00] | 0.10 [0.00, 0.31] | 0.03 | - | - | 0.90 [0.69, 1.00] (majority) | 1.00 [1.00, 1.00] |
| Qwen3.6-27B | tool | before | answer digit | 758 | 46 | 9 | 0.40 [0.37, 0.43] | 0.10 [0.07, 0.13] | 0.11 | - | - | 0.28 [0.25, 0.32] (chance) | 0.40 [0.36, 0.44] |
| Qwen3.6-27B | tool | before | locker sentence | 758 | 46 | 5 | 0.99 [0.98, 0.99] | 0.33 [0.30, 0.36] | 0.20 | 0.35 [0.32, 0.39] | 0.53 [0.50, 0.56] | 0.46 [0.43, 0.49] (layout) | 0.99 [0.98, 1.00] |
| Qwen3.6-27B | tool | before | bridge identity | 758 | 46 | 46 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.21] | 0.02 | - | - | 0.93 [0.79, 1.00] (majority) | 1.00 [1.00, 1.00] |
| Qwen3.6-27B | tool | after | answer digit | 742 | 46 | 9 | 0.11 [0.08, 0.14] | 0.13 [0.11, 0.16] | 0.11 | - | - | -0.02 [-0.05, 0.00] (majority) | 0.11 [0.08, 0.14] |
| Qwen3.6-27B | tool | after | locker sentence | 742 | 46 | 5 | 0.34 [0.31, 0.37] | 0.33 [0.30, 0.36] | 0.20 | 0.37 [0.34, 0.40] | 0.36 [0.33, 0.39] | -0.03 [-0.07, 0.01] (structure) | 0.34 [0.31, 0.37] |
| Qwen3.6-27B | tool | after | bridge identity | 742 | 46 | 46 | 1.00 [1.00, 1.00] | 0.06 [0.00, 0.20] | 0.02 | - | - | 0.94 [0.80, 1.00] (majority) | 1.00 [1.00, 1.00] |
| Qwen3.6-27B | tool | both | answer digit | 1500 | 46 | 9 | 0.20 [0.18, 0.23] | 0.12 [0.10, 0.13] | 0.11 | - | - | 0.09 [0.06, 0.12] (majority) | 0.23 [0.20, 0.26] |
| Qwen3.6-27B | tool | both | locker sentence | 1500 | 46 | 6 | 0.65 [0.63, 0.67] | 0.17 [0.15, 0.18] | 0.17 | 0.22 [0.20, 0.24] | 0.33 [0.31, 0.35] | 0.32 [0.29, 0.34] (layout) | 0.66 [0.64, 0.68] |
| Qwen3.6-27B | tool | both | bridge identity | 1500 | 46 | 46 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.21] | 0.02 | - | - | 0.93 [0.79, 1.00] (majority) | 1.00 [1.00, 1.00] |

## Report

EXP x0_probe (53.7 address probe) @ 63490932 | models Qwen3.5-9B, Qwen3.6-27B | n: per run in the tables above | seeds: bootstrap 0 (10,000 resamples unless stated); scenes as each test's own generator / set

Claim tested: the test's own rule holds the same way when the scene is rendered as code or as tool output (53.7: no prediction). Headline: probe (b), which locker sentence, locker before the pick, against the best baseline (layout / pick index / majority); the locker-after stratum is the control.

Status per run: Qwen3.5-9B code: not tested (gate 0.727 < 0.80); Qwen3.5-9B tool: tested; Qwen3.6-27B code: tested; Qwen3.6-27B tool: tested.

Three dumbest ways this could be wrong:
1) The format changes which scenes survive the alignment check (code keeps names that are one token after a quote: few elements), so a difference from prose can be the scene mix, not the format. Checked: drops and domains per format are in each run's gate.json / manifest; not controlled.
2) The tool format adds the template's tools block and two turns before the scene, so the bridge sits ~250 tokens later than in prose; position effects are not separated from the tool role. Not checked.
3) The gate passes on the read of O alone (X0's gate); a format the model reads right but by another route would pass it. Not checked beyond each test's own controls.

For the human to verify: verdict.json: runs[].rows (stratum 'before', target 'locker sentence'); rerun x0_probe.score on results/x0_probe/<run>/{states.npz, items.jsonl}.

Status: UNVERIFIED (batch 53, exploration; nothing into the README).
