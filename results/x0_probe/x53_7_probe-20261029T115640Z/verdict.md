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
| ○ Qwen3.5-9B | code | L12 | 682 | lookup says and reads O and S right: 0.669 | PP 0.669, O read 0.828; PM 0.513, O read 0.727 | not tested (gate 0.669 < 0.80) |
| Qwen3.5-9B | tool | L12 | 1500 | lookup says and reads O and S right: 0.955 | PP 0.955, O read 0.981; PM 0.682, O read 0.815 | tested |

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

## Report

EXP x0_probe (53.7 address probe) @ 2e311dff | models Qwen3.5-9B | n: per run in the tables above | seeds: bootstrap 0 (10,000 resamples unless stated); scenes as each test's own generator / set

Claim tested: the test's own rule holds the same way when the scene is rendered as code or as tool output (53.7: no prediction). Headline: probe (b), which locker sentence, locker before the pick, against the best baseline (layout / pick index / majority); the locker-after stratum is the control.

Status per run: Qwen3.5-9B code: not tested (gate 0.669 < 0.80); Qwen3.5-9B tool: tested.

Three dumbest ways this could be wrong:
1) The format changes which scenes survive the alignment check (code keeps names that are one token after a quote: few elements), so a difference from prose can be the scene mix, not the format. Checked: drops and domains per format are in each run's gate.json / manifest; not controlled.
2) The tool format adds the template's tools block and two turns before the scene, so the bridge sits ~250 tokens later than in prose; position effects are not separated from the tool role. Not checked.
3) The gate passes on the read of O alone (X0's gate); a format the model reads right but by another route would pass it. Not checked beyond each test's own controls.

For the human to verify: verdict.json: runs[].rows (stratum 'before', target 'locker sentence'); rerun x0_probe.score on results/x0_probe/<run>/{states.npz, items.jsonl}.

Status: UNVERIFIED (batch 53, exploration; nothing into the README).
