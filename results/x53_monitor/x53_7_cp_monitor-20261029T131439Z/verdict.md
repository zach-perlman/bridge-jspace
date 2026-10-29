# 53.7 add-on: code_pointer_v1's CH2 chains (Dan 11:25, critic_1125; descriptive): the monitor (53.2's probes; numbers only)

Batch 53, 53.7 (Dan 11:10); no prediction; UNVERIFIED. Spec: jobs/c3/batch53.yaml (next_1110 item 2, standing_rules_0950 item 6, next_1110_reading_537).

Rule: none: descriptive, numbers only (Dan 11:25, critic_1125: 'code_pointer_v1 (CH2 chains) only if time remains: descriptive, the address probe and the monitor'); no label is computed or stated.

Gate: X0's main gate on CH2's one reader: the unedited base prompt's chat read right on >= 0.80 of the scenes (both domains pooled; per domain beside), before any state is kept; a failure is 'not tested (gate x < 0.80)'. code_pointer_v1's own competence gate (Wilson lower bound >= 0.85 per domain x family; the 27B: CH2 100% on both domains, results/code_pointer_v1/code_competence_27b) is not re-applied.

- cp_ch2: code_pointer_v1's CH2 programs (data/code_pointer_v1/main/{animals,months}_CH2_e5f0.json, 400 scenes each): a dict line `lockers = {...}` of 5 keys, then a 2-variable target chain (x = "mouse"; h = x) and a distractor chain, then print(lockers[h]); suite_v1's chat prompt ('What does this Python code print?'). The bridge word = the target chain's head key; S = the item's dissoc source (another key heads the chain, its own dict). One reader (the lookup): the monitor's (d) is the key's recalled number (legs / month), read at the bridge word and at the lookup's last token (CH2 has no recall prompt; the recall slot repeats the lookup's prompt); the dict always precedes the chain, so the probe has no locker-after stratum.

| model | gate (lookup; per domain) | status |
|---|---|---|
| Qwen3.6-27B | {'PP': 0.9988} {'animals': {'PP': 1.0}, 'months': {'PP': 0.9975}} | tested |
| Qwen3.5-9B | {'PP': 0.9012} {'animals': {'PP': 0.8925}, 'months': {'PP': 0.91}} | tested |

## Best layer per cell (accuracy [95% CI]; no label)

| model | position | target | full (layer) | J++25 | random25 | J++100 | random100 | PCA25 | chance | fixed J++25 / 100 (beside) | energy-matched random25 / 100 (beside) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | B | (a) which item | 1.00 [1.00, 1.00] (L0) | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.09 [0.00, 0.25] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] |
| Qwen3.6-27B | B | (b) its locker slot | 1.00 [1.00, 1.00] (L32) | 0.75 [0.70, 0.79] | 0.77 [0.72, 0.82] | 0.93 [0.89, 0.96] | 0.93 [0.91, 0.95] | 0.98 [0.97, 0.99] | 0.15 [0.13, 0.16] | 0.61 [0.56, 0.67] / 0.86 [0.81, 0.90] | 0.98 [0.97, 0.99] / 0.99 [0.98, 1.00] |
| Qwen3.6-27B | B | (c) lookup's digit | 0.72 [0.65, 0.78] (L60) | 0.34 [0.29, 0.38] | 0.29 [0.26, 0.33] | 0.45 [0.39, 0.50] | 0.41 [0.36, 0.46] | 0.44 [0.39, 0.50] | 0.14 [0.11, 0.17] | 0.31 [0.26, 0.35] / 0.41 [0.33, 0.48] | 0.50 [0.44, 0.57] / 0.58 [0.53, 0.64] |
| Qwen3.6-27B | B | (d) recall's answer | 1.00 [1.00, 1.00] (L0) | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.29 [0.13, 0.54] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] |
| Qwen3.6-27B | T | (a) which item | 0.96 [0.92, 0.98] (L62) | 0.63 [0.51, 0.75] | 0.58 [0.48, 0.67] | 0.65 [0.53, 0.76] | 0.85 [0.78, 0.89] | 0.82 [0.72, 0.89] | 0.09 [0.00, 0.25] | 0.66 [0.56, 0.73] / 0.88 [0.82, 0.92] | 0.91 [0.86, 0.95] / 0.93 [0.88, 0.96] |
| Qwen3.6-27B | T | (b) its locker slot | 0.96 [0.95, 0.98] (L48) | 0.66 [0.61, 0.71] | 0.78 [0.74, 0.82] | 0.81 [0.77, 0.84] | 0.91 [0.88, 0.93] | 0.90 [0.86, 0.93] | 0.15 [0.13, 0.16] | 0.76 [0.70, 0.80] / 0.92 [0.89, 0.96] | 0.93 [0.91, 0.95] / 0.94 [0.92, 0.96] |
| Qwen3.6-27B | T | (c) lookup's digit | 1.00 [0.99, 1.00] (L52) | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.14 [0.11, 0.17] | 1.00 [0.99, 1.00] / 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] |
| Qwen3.6-27B | T | (d) recall's answer | 0.97 [0.95, 0.98] (L62) | 0.65 [0.55, 0.77] | 0.62 [0.54, 0.70] | 0.70 [0.62, 0.79] | 0.87 [0.84, 0.89] | 0.85 [0.80, 0.90] | 0.29 [0.13, 0.54] | 0.67 [0.59, 0.74] / 0.88 [0.84, 0.91] | 0.94 [0.92, 0.96] / 0.96 [0.94, 0.97] |
| Qwen3.5-9B | B | (a) which item | 1.00 [1.00, 1.00] (L0) | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.09 [0.00, 0.25] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] |
| Qwen3.5-9B | B | (b) its locker slot | 1.00 [1.00, 1.00] (L16) | 0.57 [0.53, 0.61] | 0.67 [0.63, 0.71] | 0.87 [0.83, 0.90] | 0.89 [0.86, 0.91] | 0.95 [0.93, 0.97] | 0.15 [0.13, 0.16] | 0.52 [0.44, 0.59] / 0.74 [0.69, 0.79] | 0.96 [0.95, 0.97] / 0.99 [0.98, 0.99] |
| Qwen3.5-9B | B | (c) lookup's digit | 0.63 [0.58, 0.69] (L28) | 0.23 [0.20, 0.28] | 0.22 [0.19, 0.25] | 0.33 [0.28, 0.39] | 0.32 [0.28, 0.37] | 0.33 [0.29, 0.39] | 0.14 [0.11, 0.17] | 0.21 [0.17, 0.26] / 0.26 [0.22, 0.30] | 0.37 [0.34, 0.41] / 0.46 [0.41, 0.52] |
| Qwen3.5-9B | B | (d) recall's answer | 1.00 [1.00, 1.00] (L0) | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.29 [0.13, 0.54] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] / 1.00 [1.00, 1.00] |
| Qwen3.5-9B | T | (a) which item | 0.85 [0.79, 0.88] (L28) | 0.62 [0.53, 0.71] | 0.58 [0.49, 0.65] | 0.70 [0.59, 0.78] | 0.78 [0.70, 0.84] | 0.72 [0.63, 0.79] | 0.09 [0.00, 0.25] | 0.60 [0.50, 0.67] / 0.79 [0.71, 0.84] | 0.83 [0.76, 0.87] / 0.84 [0.78, 0.88] |
| Qwen3.5-9B | T | (b) its locker slot | 0.78 [0.71, 0.84] (L20) | 0.45 [0.41, 0.50] | 0.55 [0.50, 0.59] | 0.62 [0.57, 0.66] | 0.68 [0.61, 0.74] | 0.68 [0.61, 0.74] | 0.15 [0.13, 0.16] | 0.51 [0.46, 0.57] / 0.67 [0.60, 0.73] | 0.74 [0.67, 0.79] / 0.76 [0.69, 0.82] |
| Qwen3.5-9B | T | (c) lookup's digit | 0.88 [0.84, 0.92] (L28) | 0.88 [0.85, 0.91] | 0.85 [0.81, 0.88] | 0.89 [0.86, 0.92] | 0.87 [0.84, 0.91] | 0.88 [0.85, 0.91] | 0.14 [0.11, 0.17] | 0.85 [0.81, 0.89] / 0.88 [0.84, 0.92] | 0.88 [0.84, 0.91] / 0.88 [0.84, 0.92] |
| Qwen3.5-9B | T | (d) recall's answer | 0.90 [0.88, 0.93] (L30) | 0.69 [0.61, 0.78] | 0.62 [0.56, 0.69] | 0.77 [0.71, 0.82] | 0.80 [0.77, 0.84] | 0.77 [0.71, 0.84] | 0.29 [0.13, 0.54] | 0.62 [0.53, 0.72] / 0.81 [0.78, 0.85] | 0.88 [0.86, 0.91] / 0.90 [0.88, 0.93] |

Each column's best layer (full: the layer named). (d) at the last token is read on the lookup's prompt (CH2 has no recall prompt).


## Report

EXP x53_monitor (code_pointer_v1 CH2, descriptive) @ 45cdd131 | models Qwen3.5-9B, Qwen3.6-27B | n: per run in the tables above | seeds: bootstrap 0 (10,000 resamples unless stated); scenes as each test's own generator / set

Claim tested: the test's own rule holds the same way when the scene is rendered as code or as tool output (53.7: no prediction). Headline: numbers only: per target and position the J++ probe beside the random subspace and the full residual, no label.

Status per run: Qwen3.6-27B cp_ch2: tested; Qwen3.5-9B cp_ch2: tested.

Three dumbest ways this could be wrong:
1) The format changes which scenes survive the alignment check (code keeps names that are one token after a quote: few elements), so a difference from prose can be the scene mix, not the format. Checked: drops and domains per format are in each run's gate.json / manifest; not controlled.
2) The tool format adds the template's tools block and two turns before the scene, so the bridge sits ~250 tokens later than in prose; position effects are not separated from the tool role. Not checked.
3) The gate passes on the read of O alone (X0's gate); a format the model reads right but by another route would pass it. Not checked beyond each test's own controls.

For the human to verify: x53_7_cp_monitor.json: results[<model>]['cp_ch2']['acc']; the probes in cache/x53_monitor/<run>/cp_ch2.npz (x53_monitor.py probe).

Status: UNVERIFIED (batch 53, exploration; nothing into the README).
