# indep_check qwen35_9b_x45_indep_pregate: PASS

Stored run `/home/sesterce/jobq/runs/merge_pregate_indep_9b/code/results/x0_necessity/qwen35_9b_x0_necessity`, layer 12, chat, J++ k=25 signed OMP; n = 20 items (random.Random(0).sample); rule: PASS iff every arm has >= 19 items whose two readers both match the stored read's role (b / A / other).

| arm | items agree | rows agree | switched PP mine / stored | switched PM mine / stored | max abs ld diff | mean abs ld diff |
|---|---|---|---|---|---|---|
| none (descriptive) | 20/20 | 40/40 | 0 / 0 | 0 / 0 | 0.0005 | 0.0 |
| whole | 20/20 | 40/40 | 13 / 13 | 19 / 19 | 0.0 | 0.0 |
| no_part | 20/20 | 40/40 | 11 / 11 | 11 / 11 | 0.0 | 0.0 |
| no_rand | 20/20 | 40/40 | 8 / 8 | 19 / 19 | 0.125 | 0.0187 |

Prompts vs cases.jsonl: ids 20/20, bridge position 20/20, answer tokens 20/20.
J++ share of ||Δ||²: median 0.2126; largest |mine - stored| 0.0; random part's share off the J++ share by at most 8.60e-04.
Hook (block 12 output) vs hidden_states[13]: max |diff| 0. Final-norm gain: one_plus_weight. Atoms: 242132 letter tokens.

Disagreements:

- none
