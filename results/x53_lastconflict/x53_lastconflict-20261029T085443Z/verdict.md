# 53.3: the conflict test at the last token

Batch 53, test 53.3 (jobs/c3/batch53.yaml; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). The change at the last token (P3) at 51.10's read-peak layer and the answer layer minus 2, per reader; 51.10's locker-first items. UNVERIFIED.

Rule (Dan's brief): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between".

As computed: the loss beyond random = X0's excess (S_no_rand - S_no_jpp) / S_whole; the rest alone's share = S_rest / S_whole; S_arm = the share of the locker-first items switched (the top token is S's answer's first token); point estimates decide (EPS 1e-9 at the bars); cluster-bootstrap CIs over the original bridge entities (10000, seed 0, paired) beside; S_whole = 0: not tested.

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | the rest alone | loss beyond random | rest / whole | label | X0 valid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | lookup | 24 (read peak) | 75 (32) | 0.68 [0.58, 0.78] | 0.24 [0.12, 0.37] | 0.32 [0.19, 0.46] | 0.00 [0.00, 0.00] | 0.24 [0.12, 0.37] | 0.12 [0.00, 0.23] | 0.35 [0.19, 0.52] | **in between** | yes |
| qwen3.5-9b | lookup | 27 (answer L29 - 2) | 75 (32) | 0.73 [0.62, 0.84] | 0.12 [0.03, 0.22] | 0.24 [0.13, 0.36] | 0.00 [0.00, 0.00] | 0.12 [0.03, 0.22] | 0.16 [0.08, 0.26] | 0.16 [0.04, 0.29] | **in between** | yes |
| qwen3.5-9b | recall | 24 (read peak) | 75 (32) | 0.95 [0.88, 1.00] | 0.75 [0.63, 0.86] | 0.81 [0.72, 0.91] | 0.03 [0.00, 0.06] | 0.75 [0.63, 0.86] | 0.07 [-0.03, 0.18] | 0.79 [0.67, 0.90] | **computes outside the lens at the last token** | yes |
| qwen3.5-9b | recall | 27 (answer L29 - 2) | 75 (32) | 0.95 [0.88, 1.00] | 0.56 [0.42, 0.70] | 0.75 [0.61, 0.87] | 0.07 [0.00, 0.14] | 0.56 [0.42, 0.70] | 0.20 [0.06, 0.33] | 0.59 [0.45, 0.73] | **in between** | yes |

O unedited switched (floor): qwen3.5-9b lookup 0.00 [0.00, 0.00]; qwen3.5-9b lookup 0.00 [0.00, 0.00]; qwen3.5-9b recall 0.00 [0.00, 0.00]; qwen3.5-9b recall 0.00 [0.00, 0.00].

Layer sources: qwen3.5-9b: results/x51_jread/qwen35_9b_x51_10/peak.json, results/x51_jread/read-qwen35_9b_x51_10-20261028T185634Z/read.json.

Figure: x53_lastconflict.png
