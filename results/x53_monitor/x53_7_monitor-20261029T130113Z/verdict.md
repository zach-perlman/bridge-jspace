# 53.7 (the pointer in code and tool output): the monitor test (53.2) in code and tool output

Batch 53, 53.7 (Dan 11:10); no prediction; UNVERIFIED. Spec: jobs/c3/batch53.yaml (next_1110 item 2, standing_rules_0950 item 6, next_1110_reading_537).

**adapted design: lookup-only gate; the recall is not part of this test.** Target (d), the recall's answer, is a positive control (critic_1125); the gate's recall rates are descriptive.

Rule (53.2's, verbatim): "J-space blind to X" if the J++ probe is within 0.10 of the random subspace at every layer while the full residual reaches >= 0.8 at some layer; "J-space carries X" if J++ >= 0.8 and >= 0.3 above random; else in between.

Gate (53.7): adapted design: lookup-only gate; the recall is not part of this test: Dan 12:10 (decisions_1210): the share of the test's own scenes in the format where the lookup says and reads O and S right (X0's competence: the greedy answer and the chat read) >= 0.80, before any state is kept; a failed format is 'not tested (gate x < 0.80)'; an item is eligible when the lookup is right on all four; the recall's rates are reported descriptively.

- code: the scene as Python in the user turn (tasks_v2's code framing): picks = {} and lockers = {}, then one assignment per statement in the scene's order (picks["Eva"] = "oxygen"; lockers["oxygen"] = 5), then the question and the digit instruction.
- tool: the scene's text verbatim as the response of a declared tool (get_notes) in the model's chat template, after the user's 'Look up my notes.' and the assistant's call; the question and the instruction in a new user turn.

| model | format | gate set | gate | beside (descriptive) | status |
|---|---|---|---|---|---|
| Qwen3.5-9B | code | d1_topics_v3 (272 scenes) | lookup says and reads O and S right: 0.702 (191 eligible) | PP 0.702, O read 0.827; PM 0.511, O read 0.750 | not tested (gate 0.702 < 0.80) |
| Qwen3.5-9B | tool | d1_topics_v3 (600 scenes) | lookup says and reads O and S right: 0.948 (569 eligible) | PP 0.948, O read 0.978; PM 0.683, O read 0.825 | tested |

## Labels (53.2's rule per position, target and k; the arms beside where their passes ran)

The decisive label is the per-state J++ part against a random subspace of the same k. Beside it (53.2, critic_1125): the same rule with the fixed J++ subspace (fixed) and with the energy-matched random subspace (erand); '-' where that pass has not run.

| model | format | position | target | k = 25 | k = 100 | full max | J++25 max (gap max) | J++100 max (gap max) | beside: fixed k25 / k100 | beside: erand k25 / k100 |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | tool_l (n 400 rows, 46 entities) | B | (a) which item is the bridge | in between | random reads it too | 0.98 | 0.98 (+0.27) | 0.98 (+0.01) | in between / random reads it too | no different from random directions of the same energy / no different from random directions of the same energy |
| Qwen3.5-9B | tool_l (n 400 rows, 46 entities) | B | (b) the bridge item's locker slot (the address) | in between | in between | 0.72 | 0.61 (+0.06) | 0.68 (+0.07) | in between / in between | in between / in between |
| Qwen3.5-9B | tool_l (n 400 rows, 46 entities) | B | (c) the lookup's answer digit | in between | in between | 0.12 | 0.14 (+0.04) | 0.14 (+0.03) | in between / in between | no different from random directions of the same energy / no different from random directions of the same energy |
| Qwen3.5-9B | tool_l (n 400 rows, 46 entities) | B | (d) the recall's answer | J-space carries X | random reads it too | 1.00 | 1.00 (+0.42) | 1.00 (+0.07) | J-space carries X / random reads it too | no different from random directions of the same energy / no different from random directions of the same energy |
| Qwen3.5-9B | tool_l (n 400 rows, 46 entities) | T | (a) which item is the bridge | in between | in between | 0.76 | 0.63 (+0.30) | 0.64 (+0.03) | in between / in between | in between / in between |
| Qwen3.5-9B | tool_l (n 400 rows, 46 entities) | T | (b) the bridge item's locker slot (the address) | in between | in between | 0.93 | 0.62 (+0.03) | 0.75 (+0.11) | in between / J-space blind to X | under-represented in the lens directions / under-represented in the lens directions |
| Qwen3.5-9B | tool_l (n 400 rows, 46 entities) | T | (c) the lookup's answer digit | in between | random reads it too | 0.99 | 0.99 (+0.11) | 0.99 (+0.04) | random reads it too / random reads it too | under-represented in the lens directions / under-represented in the lens directions |
| Qwen3.5-9B | tool_l (n 400 rows, 46 entities) | T | (d) the recall's answer | in between | in between | 0.99 | 0.99 (+0.12) | 0.99 (+0.00) | random reads it too / random reads it too | under-represented in the lens directions / in between |

## Report

EXP x53_monitor (53.7 monitor) @ 92ec2f1c | models Qwen3.5-9B | n: per run in the tables above | seeds: bootstrap 0 (10,000 resamples unless stated); scenes as each test's own generator / set

Claim tested: the test's own rule holds the same way when the scene is rendered as code or as tool output (53.7: no prediction). Headline: per target and position the J++ probe against the random subspace of the same k, and the full residual's best layer (53.2's rule).

Status per run: Qwen3.5-9B code: not tested (gate 0.702 < 0.80); Qwen3.5-9B tool: tested.

Three dumbest ways this could be wrong:
1) The format changes which scenes survive the alignment check (code keeps names that are one token after a quote: few elements), so a difference from prose can be the scene mix, not the format. Checked: drops and domains per format are in each run's gate.json / manifest; not controlled.
2) The tool format adds the template's tools block and two turns before the scene, so the bridge sits ~250 tokens later than in prose; position effects are not separated from the tool role. Not checked.
3) The gate passes on the read of O alone (X0's gate); a format the model reads right but by another route would pass it. Not checked beyond each test's own controls.

For the human to verify: x53_7_monitor.json: results[<model>][<format>]['acc'] and ['rules']; the probes in cache/x53_monitor/<run>/<format>.npz (x53_monitor.py probe, deterministic).

Status: UNVERIFIED (batch 53, exploration; nothing into the README).
