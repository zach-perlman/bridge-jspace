# 53.7 add-on: code_pointer_v1's CH2 chains (Dan 11:25, critic_1125; descriptive): the address probe (descriptive, numbers only)

Batch 53, 53.7 (Dan 11:10); no prediction; UNVERIFIED. Spec: jobs/c3/batch53.yaml (next_1110 item 2, standing_rules_0950 item 6, next_1110_reading_537).

Rule: none: descriptive, numbers only (Dan 11:25, critic_1125: 'code_pointer_v1 (CH2 chains) only if time remains: descriptive, the address probe and the monitor'); no label is computed or stated

Gate: X0's main gate on CH2's one reader: the unedited base prompt's chat read right on >= 0.80 of the scenes (both domains pooled; per domain beside), before any state is kept; a failure is 'not tested (gate x < 0.80)'. code_pointer_v1's own competence gate (Wilson lower bound >= 0.85 per domain x family; the 27B: CH2 100% on both domains, results/code_pointer_v1/code_competence_27b) is not re-applied.

- cp_ch2: code_pointer_v1's CH2 programs (data/code_pointer_v1/main/{animals,months}_CH2_e5f0.json, 400 scenes each): a dict line `lockers = {...}` of 5 keys, then a 2-variable target chain (x = "mouse"; h = x) and a distractor chain, then print(lockers[h]); suite_v1's chat prompt ('What does this Python code print?'). The bridge word = the target chain's head key; S = the item's dissoc source (another key heads the chain, its own dict). One reader (the lookup): the monitor's (d) is the key's recalled number (legs / month), read at the bridge word and at the lookup's last token (CH2 has no recall prompt; the recall slot repeats the lookup's prompt); the dict always precedes the chain, so the probe has no locker-after stratum.

| model | format | layer | aligned scenes | gate (lookup) | status |
|---|---|---|---|---|---|
| Qwen3.5-9B | cp_ch2 | L12 | 800 | 0.901 | tested |

## Probe accuracy (every scene of the run; folds by bridge entity for (a), (b), by item for (c))

| model | format | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | layout | probe - best baseline | prose v4 probe (beside) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | cp_ch2 | before | answer digit | 800 | 19 | 10 | 0.43 [0.36, 0.51] | 0.16 [0.13, 0.18] | 0.10 | - | - | 0.27 [0.20, 0.36] (majority) | - |
| Qwen3.5-9B | cp_ch2 | before | locker sentence | 800 | 19 | 5 | 1.00 [0.99, 1.00] | 0.16 [0.14, 0.19] | 0.20 | 0.15 [0.13, 0.17] | 0.16 [0.14, 0.19] | 0.80 [0.79, 0.80] (chance) | - |
| Qwen3.5-9B | cp_ch2 | before | bridge identity | 800 | 19 | 19 | 1.00 [1.00, 1.00] | 0.10 [0.00, 0.30] | 0.05 | - | - | 0.90 [0.70, 1.00] (majority) | - |

## Report

EXP x0_probe (code_pointer_v1 CH2, descriptive) @ 430d2f7c | models Qwen3.5-9B | n: per run in the tables above | seeds: bootstrap 0 (10,000 resamples unless stated); scenes as each test's own generator / set

Claim tested: the test's own rule holds the same way when the scene is rendered as code or as tool output (53.7: no prediction). Headline: numbers only (no rule, no label): probe (b), the key's dict slot, against the best baseline; there is no locker-after stratum (the dict always comes first), so no control by construction.

Status per run: Qwen3.5-9B cp_ch2: tested.

Three dumbest ways this could be wrong:
1) The format changes which scenes survive the alignment check (code keeps names that are one token after a quote: few elements), so a difference from prose can be the scene mix, not the format. Checked: drops and domains per format are in each run's gate.json / manifest; not controlled.
2) The tool format adds the template's tools block and two turns before the scene, so the bridge sits ~250 tokens later than in prose; position effects are not separated from the tool role. Not checked.
3) The gate passes on the read of O alone (X0's gate); a format the model reads right but by another route would pass it. Not checked beyond each test's own controls.

For the human to verify: verdict.json: runs[].rows; rerun x0_probe.score on results/x0_probe/<run>/{states.npz, items.jsonl}.

Status: UNVERIFIED (batch 53, exploration; nothing into the README).
