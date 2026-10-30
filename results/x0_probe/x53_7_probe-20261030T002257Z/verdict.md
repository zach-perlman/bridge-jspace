# 53.7 (the pointer in code and tool output): the address probe in code and tool output

Batch 53, 53.7 (Dan 11:10); no prediction; UNVERIFIED. Spec: jobs/c3/batch53.yaml (next_1110 item 2, standing_rules_0950 item 6, next_1110_reading_537).

**adapted design: lookup-only gate; the recall is not part of this test.**

Rule: none of its own (x0_probe v4 is descriptive, added after the data). Pre-stated reading (Dan, x0_probe): (a) high in locker-before and at chance in locker-after -> the answer value is stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address (a lookback-style pointer). In locker-after scenes the locker sentence follows the word, so (a) and (b) cannot be read there from the locker sentence itself: that stratum is the control by construction.

Gate (53.7): adapted design: lookup-only gate; the recall is not part of this test: Dan 12:10 (decisions_1210): the share of the test's own scenes in the format where the lookup says and reads O and S right (X0's competence: the greedy answer and the chat read) >= 0.80, before any state is kept; a failed format is 'not tested (gate x < 0.80)'; an item is eligible when the lookup is right on all four; the recall's rates are reported descriptively.

Caveats (Dan 12:10b): tool output as prose (JSON is covered by x0b_v2), and the bridge ~250 tokens later in the tool format, not separated from the format (47.16's distance robustness beside). The probe only shows the address is readable; the routes test decides whether the lookup uses it.

- code: the scene as Python in the user turn (tasks_v2's code framing): picks = {} and lockers = {}, then one assignment per statement in the scene's order (picks["Eva"] = "oxygen"; lockers["oxygen"] = 5), then the question and the digit instruction.
- tool: the scene's text verbatim as the response of a declared tool (get_notes) in the model's chat template, after the user's 'Look up my notes.' and the assistant's call; the question and the instruction in a new user turn.

○ = gate changed after the data (hollow) (Dan 12:25, decisions_1225).

| model | format | layer | aligned scenes | gate | beside (descriptive) | status |
|---|---|---|---|---|---|---|
| qwen3.5-122b-a10b | code | L33 | 682 | lookup says and reads O and S right: 0.867 | PP 0.867, O read 0.934; PM 0.648, O read 0.824 | tested |
| qwen3.5-122b-a10b | tool | L33 | 1500 | lookup says and reads O and S right: 0.991 | PP 0.991, O read 0.997; PM 0.781, O read 0.891 | tested |

## Probe accuracy (every scene of the run; folds by bridge entity for (a), (b), by item for (c))

| model | format | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | layout | probe - best baseline | prose v4 probe (beside) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-122b-a10b | code | before | answer digit | 349 | 28 | 9 | 0.19 [0.15, 0.23] | 0.12 [0.08, 0.15] | 0.11 | - | - | 0.07 [0.02, 0.12] (majority) | 0.25 [0.21, 0.28] |
| qwen3.5-122b-a10b | code | before | locker sentence | 349 | 28 | 5 | 0.92 [0.88, 0.95] | 0.29 [0.25, 0.33] | 0.20 | 0.26 [0.22, 0.30] | 0.48 [0.42, 0.53] | 0.44 [0.38, 0.50] (layout) | 0.92 [0.90, 0.94] |
| qwen3.5-122b-a10b | code | before | bridge identity | 349 | 28 | 28 | 0.99 [0.97, 1.00] | 0.11 [0.00, 0.34] | 0.04 | - | - | 0.87 [0.65, 1.00] (majority) | 1.00 [1.00, 1.00] |
| qwen3.5-122b-a10b | code | after | answer digit | 333 | 29 | 9 | 0.12 [0.09, 0.17] | 0.15 [0.11, 0.19] | 0.11 | - | - | -0.02 [-0.07, 0.01] (majority) | 0.11 [0.09, 0.14] |
| qwen3.5-122b-a10b | code | after | locker sentence | 333 | 29 | 5 | 0.40 [0.36, 0.44] | 0.36 [0.32, 0.39] | 0.20 | 0.29 [0.25, 0.32] | 0.32 [0.27, 0.37] | 0.04 [0.00, 0.08] (majority) | 0.33 [0.31, 0.35] |
| qwen3.5-122b-a10b | code | after | bridge identity | 333 | 29 | 29 | 0.98 [0.96, 1.00] | 0.11 [0.00, 0.23] | 0.03 | - | - | 0.88 [0.75, 0.99] (majority) | 1.00 [1.00, 1.00] |
| qwen3.5-122b-a10b | code | both | answer digit | 682 | 29 | 9 | 0.16 [0.12, 0.19] | 0.09 [0.06, 0.12] | 0.11 | - | - | 0.05 [0.01, 0.08] (chance) | 0.16 [0.14, 0.18] |
| qwen3.5-122b-a10b | code | both | locker sentence | 682 | 29 | 6 | 0.61 [0.58, 0.63] | 0.14 [0.11, 0.16] | 0.17 | 0.17 [0.14, 0.20] | 0.28 [0.24, 0.32] | 0.33 [0.28, 0.37] (layout) | 0.60 [0.58, 0.62] |
| qwen3.5-122b-a10b | code | both | bridge identity | 682 | 29 | 29 | 1.00 [1.00, 1.00] | 0.10 [0.00, 0.31] | 0.03 | - | - | 0.90 [0.69, 1.00] (majority) | 1.00 [1.00, 1.00] |
| qwen3.5-122b-a10b | tool | before | answer digit | 758 | 46 | 9 | 0.25 [0.21, 0.28] | 0.10 [0.07, 0.13] | 0.11 | - | - | 0.13 [0.10, 0.17] (chance) | 0.25 [0.21, 0.28] |
| qwen3.5-122b-a10b | tool | before | locker sentence | 758 | 46 | 5 | 0.93 [0.91, 0.95] | 0.33 [0.30, 0.36] | 0.20 | 0.35 [0.32, 0.39] | 0.53 [0.50, 0.56] | 0.40 [0.37, 0.44] (layout) | 0.92 [0.90, 0.94] |
| qwen3.5-122b-a10b | tool | before | bridge identity | 758 | 46 | 46 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.21] | 0.02 | - | - | 0.93 [0.79, 1.00] (majority) | 1.00 [1.00, 1.00] |
| qwen3.5-122b-a10b | tool | after | answer digit | 742 | 46 | 9 | 0.11 [0.09, 0.13] | 0.13 [0.11, 0.16] | 0.11 | - | - | -0.03 [-0.06, 0.00] (majority) | 0.11 [0.09, 0.14] |
| qwen3.5-122b-a10b | tool | after | locker sentence | 742 | 46 | 5 | 0.34 [0.32, 0.37] | 0.33 [0.30, 0.36] | 0.20 | 0.37 [0.34, 0.40] | 0.36 [0.33, 0.39] | -0.03 [-0.06, 0.01] (structure) | 0.33 [0.31, 0.35] |
| qwen3.5-122b-a10b | tool | after | bridge identity | 742 | 46 | 46 | 1.00 [1.00, 1.00] | 0.06 [0.00, 0.20] | 0.02 | - | - | 0.94 [0.80, 1.00] (majority) | 1.00 [1.00, 1.00] |
| qwen3.5-122b-a10b | tool | both | answer digit | 1500 | 46 | 9 | 0.16 [0.14, 0.17] | 0.12 [0.10, 0.13] | 0.11 | - | - | 0.04 [0.02, 0.07] (majority) | 0.16 [0.14, 0.18] |
| qwen3.5-122b-a10b | tool | both | locker sentence | 1500 | 46 | 6 | 0.63 [0.60, 0.65] | 0.17 [0.15, 0.18] | 0.17 | 0.22 [0.20, 0.24] | 0.33 [0.31, 0.35] | 0.30 [0.27, 0.32] (layout) | 0.60 [0.58, 0.62] |
| qwen3.5-122b-a10b | tool | both | bridge identity | 1500 | 46 | 46 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.21] | 0.02 | - | - | 0.93 [0.79, 1.00] (majority) | 1.00 [1.00, 1.00] |

## Report

EXP x0_probe (53.7 address probe) @ e1903224 | models qwen3.5-122b-a10b | n: per run in the tables above | seeds: bootstrap 0 (10,000 resamples unless stated); scenes as each test's own generator / set

Claim tested: the test's own rule holds the same way when the scene is rendered as code or as tool output (53.7: no prediction). Headline: probe (b), which locker sentence, locker before the pick, against the best baseline (layout / pick index / majority); the locker-after stratum is the control.

Status per run: qwen3.5-122b-a10b code: tested; qwen3.5-122b-a10b tool: tested.

Three dumbest ways this could be wrong:
1) The format changes which scenes survive the alignment check (code keeps names that are one token after a quote: few elements), so a difference from prose can be the scene mix, not the format. Checked: drops and domains per format are in each run's gate.json / manifest; not controlled.
2) The tool format adds the template's tools block and two turns before the scene, so the bridge sits ~250 tokens later than in prose; position effects are not separated from the tool role. Not checked.
3) The gate passes on the read of O alone (X0's gate); a format the model reads right but by another route would pass it. Not checked beyond each test's own controls.

For the human to verify: verdict.json: runs[].rows (stratum 'before', target 'locker sentence'); rerun x0_probe.score on results/x0_probe/<run>/{states.npz, items.jsonl}.

Status: UNVERIFIED (batch 53, exploration; nothing into the README).
