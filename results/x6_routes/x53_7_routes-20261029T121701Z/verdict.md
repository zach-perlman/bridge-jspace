# 53.7 (the pointer in code and tool output): the routes test in code and tool output

Batch 53, 53.7 (Dan 11:10); no prediction; UNVERIFIED. Spec: jobs/c3/batch53.yaml (next_1110 item 2, standing_rules_0950 item 6, next_1110_reading_537).

**adapted design: lookup-only gate; the recall is not part of this test.**

Rule (the routes test's, verbatim): "A route counts as used if its share is >= 0.2 with lower CI >= 0.1." The C0 sanity swap must reproduce the one-pick lookup switch rate within 0.1, or the run stops (lookup-based, unchanged). Gate: adapted design: lookup-only gate; the recall is not part of this test (Dan 12:10, decisions_1210): per condition the lookup says and reads O and S right (X0's greedy answer and chat read, both prompts) on >= 0.80 of the scenes; an item is eligible when the lookup does; the recall's rates reported descriptively; a failed condition is not tested. Cluster bootstrap over the bridge item (10,000 resamples, seed 0). C1: identity = original (both a). The recall's columns are descriptive (not part of this test).

- code: the scene as Python in the user turn (tasks_v2's code framing): picks = {} and lockers = {}, then one assignment per statement in the scene's order (picks["Eva"] = "oxygen"; lockers["oxygen"] = 5), then the question and the digit instruction.
- tool: the scene's text verbatim as the response of a declared tool (get_notes) in the model's chat template, after the user's 'Look up my notes.' and the assistant's call; the question and the instruction in a new user turn.

| model | format | condition | status | gate | beside (descriptive) |
|---|---|---|---|---|---|
| Qwen3.5-9B | tool | C0 | tested | lookup says and reads O and S right: 1.000 (700 eligible) | recall the same: 0.851; O read lookup / recall 1.000 / 0.916 |
| Qwen3.5-9B | tool | C1 | tested | lookup says and reads O and S right: 1.000 (700 eligible) | recall the same: 0.879; O read lookup / recall 1.000 / 0.916 |
| Qwen3.5-9B | tool | C2 | tested | lookup says and reads O and S right: 0.999 (699 eligible) | recall the same: 0.849; O read lookup / recall 1.000 / 0.916 |
| | | C0 check | ok | lookup switch 0.997 vs reference 0.9863013698630136 |

## Route shares of the lookup per arm (the rule's 'used' routes at the right)

| model | format | condition | arm | n | identity | position | value | original | other | recall follows S (descriptive) | used |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | tool | C0 | the whole change | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.91 [0.87, 0.94] | none |
| Qwen3.5-9B | tool | C0 | without the address | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.25 [0.20, 0.30] | 0.75 [0.70, 0.80] | 0.87 [0.83, 0.90] | original |
| Qwen3.5-9B | tool | C0 | without a random part (the address's share) | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.90 [0.87, 0.94] | none |
| Qwen3.5-9B | tool | C0 | the address alone | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.92 [0.88, 0.95] | 0.08 [0.05, 0.12] | 0.10 [0.06, 0.15] | original |
| Qwen3.5-9B | tool | C0 | a random part alone (the address's share) | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.05 [0.02, 0.09] | original |
| Qwen3.5-9B | tool | C0 | without J++ | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.99 [0.98, 1.00] | 0.82 [0.77, 0.87] | none |
| Qwen3.5-9B | tool | C0 | without a random part (J++'s share) | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.99 [0.98, 1.00] | 0.89 [0.85, 0.92] | none |
| Qwen3.5-9B | tool | C0 | J++ alone | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.13 [0.07, 0.20] | original |
| Qwen3.5-9B | tool | C0 | a random part alone (J++'s share) | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.07 [0.03, 0.11] | original |
| Qwen3.5-9B | tool | C1 | the whole change | 300 | 0.48 [0.41, 0.55] | 0.50 [0.43, 0.58] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.81 [0.72, 0.89] | identity, position |
| Qwen3.5-9B | tool | C1 | without the address | 300 | 0.99 [0.98, 1.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.92 [0.83, 0.98] | identity |
| Qwen3.5-9B | tool | C1 | without a random part (the address's share) | 300 | 0.94 [0.91, 0.96] | 0.06 [0.03, 0.08] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.90 [0.81, 0.96] | identity |
| Qwen3.5-9B | tool | C1 | the address alone | 300 | 0.83 [0.78, 0.87] | 0.16 [0.12, 0.21] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.87 [0.79, 0.94] | identity |
| Qwen3.5-9B | tool | C1 | a random part alone (the address's share) | 300 | 0.99 [0.98, 1.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.92 [0.83, 0.98] | identity |
| Qwen3.5-9B | tool | C1 | without J++ | 300 | 0.54 [0.47, 0.61] | 0.44 [0.37, 0.51] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.02 [0.00, 0.03] | 0.82 [0.73, 0.90] | identity, position |
| Qwen3.5-9B | tool | C1 | without a random part (J++'s share) | 300 | 0.54 [0.47, 0.62] | 0.44 [0.37, 0.52] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.82 [0.73, 0.90] | identity, position |
| Qwen3.5-9B | tool | C1 | J++ alone | 300 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.92 [0.84, 0.97] | identity |
| Qwen3.5-9B | tool | C1 | a random part alone (J++'s share) | 300 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.92 [0.84, 0.98] | identity |
| Qwen3.5-9B | tool | C2 | the whole change | 300 | 0.50 [0.45, 0.54] | 0.46 [0.41, 0.51] | 0.00 [0.00, 0.00] | 0.04 [0.02, 0.06] | 0.00 [0.00, 0.00] | 0.81 [0.76, 0.86] | identity, position |
| Qwen3.5-9B | tool | C2 | without the address | 300 | 0.37 [0.32, 0.43] | 0.09 [0.05, 0.12] | 0.00 [0.00, 0.00] | 0.54 [0.48, 0.60] | 0.00 [0.00, 0.00] | 0.80 [0.74, 0.85] | identity, original |
| Qwen3.5-9B | tool | C2 | without a random part (the address's share) | 300 | 0.44 [0.40, 0.49] | 0.48 [0.42, 0.53] | 0.00 [0.00, 0.00] | 0.08 [0.05, 0.11] | 0.00 [0.00, 0.00] | 0.79 [0.74, 0.84] | identity, position |
| Qwen3.5-9B | tool | C2 | the address alone | 300 | 0.00 [0.00, 0.01] | 0.08 [0.05, 0.12] | 0.00 [0.00, 0.00] | 0.91 [0.87, 0.95] | 0.00 [0.00, 0.01] | 0.08 [0.04, 0.13] | original |
| Qwen3.5-9B | tool | C2 | a random part alone (the address's share) | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.06 [0.02, 0.11] | original |
| Qwen3.5-9B | tool | C2 | without J++ | 300 | 0.39 [0.35, 0.44] | 0.52 [0.47, 0.57] | 0.00 [0.00, 0.00] | 0.09 [0.06, 0.13] | 0.00 [0.00, 0.00] | 0.55 [0.49, 0.62] | identity, position |
| Qwen3.5-9B | tool | C2 | without a random part (J++'s share) | 300 | 0.41 [0.37, 0.47] | 0.44 [0.38, 0.49] | 0.00 [0.00, 0.00] | 0.15 [0.11, 0.19] | 0.00 [0.00, 0.00] | 0.75 [0.69, 0.81] | identity, position |
| Qwen3.5-9B | tool | C2 | J++ alone | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.12 [0.07, 0.19] | original |
| Qwen3.5-9B | tool | C2 | a random part alone (J++'s share) | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.08 [0.04, 0.13] | original |

## Report

EXP x6_routes (53.7 routes) @ 4e209c5b | models Qwen3.5-9B | n: per run in the tables above | seeds: bootstrap 0 (10,000 resamples unless stated); scenes as each test's own generator / set

Claim tested: the test's own rule holds the same way when the scene is rendered as code or as tool output (53.7: no prediction). Headline: the lookup's position share without the address against without a random part of its share, and with the address alone against a random part alone, per format; the value share under the whole change.

Status per run: Qwen3.5-9B tool: C0 tested, C1 tested, C2 tested.

Three dumbest ways this could be wrong:
1) The format changes which scenes survive the alignment check (code keeps names that are one token after a quote: few elements), so a difference from prose can be the scene mix, not the format. Checked: drops and domains per format are in each run's gate.json / manifest; not controlled.
2) The tool format adds the template's tools block and two turns before the scene, so the bridge sits ~250 tokens later than in prose; position effects are not separated from the tool role. Not checked.
3) The gate passes on the read of O alone (X0's gate); a format the model reads right but by another route would pass it. Not checked beyond each test's own controls.

For the human to verify: verdict.json: runs[].cells['C2|whole'].share (recompute from results/x6_routes/<run>/outcomes.jsonl, lookup rows of C2 under 'whole': the share of route == 'position').

Status: UNVERIFIED (batch 53, exploration; nothing into the README).
