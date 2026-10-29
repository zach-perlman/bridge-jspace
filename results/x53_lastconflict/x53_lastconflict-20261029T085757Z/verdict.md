# 53.3: the conflict test at the last token

Batch 53, test 53.3 (jobs/c3/batch53.yaml; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). The change at the last token (P3) at 51.10's read-peak layer and the answer layer minus 2, per reader; 51.10's locker-first items. UNVERIFIED.

Rule (Dan's brief): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between".

As computed: the loss beyond random = X0's excess (S_no_rand - S_no_jpp) / S_whole; the rest alone's share = S_rest / S_whole; S_arm = the share of the locker-first items switched (the top token is S's answer's first token); point estimates decide (EPS 1e-9 at the bars); cluster-bootstrap CIs over the original bridge entities (10000, seed 0, paired) beside; S_whole = 0: not tested.

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | the rest alone | loss beyond random | rest / whole | label | X0 valid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.6-27b | lookup | 60 (read peak) | 69 (34) | 0.45 [0.35, 0.55] | 0.09 [0.03, 0.15] | 0.14 [0.08, 0.21] | 0.00 [0.00, 0.00] | 0.09 [0.03, 0.15] | 0.13 [0.03, 0.25] | 0.19 [0.07, 0.33] | **in between** | yes |
| qwen3.6-27b | lookup | 59 (answer L61 - 2) | 69 (34) | 0.30 [0.22, 0.39] | 0.03 [0.00, 0.08] | 0.07 [0.02, 0.13] | 0.00 [0.00, 0.00] | 0.03 [0.00, 0.08] | 0.14 [0.00, 0.29] | 0.10 [0.00, 0.25] | **in between** | no |
| qwen3.6-27b | recall | 56 (read peak) | 69 (34) | 0.97 [0.93, 1.00] | 0.77 [0.62, 0.91] | 0.80 [0.67, 0.93] | 0.01 [0.00, 0.05] | 0.77 [0.62, 0.91] | 0.03 [-0.09, 0.14] | 0.79 [0.64, 0.93] | **computes outside the lens at the last token** | yes |
| qwen3.6-27b | recall | 59 (answer L61 - 2) | 69 (34) | 0.99 [0.95, 1.00] | 0.25 [0.15, 0.36] | 0.87 [0.81, 0.94] | 0.10 [0.03, 0.18] | 0.25 [0.15, 0.36] | 0.63 [0.54, 0.73] | 0.25 [0.15, 0.37] | **through the lens** | yes |

O unedited switched (floor): qwen3.6-27b lookup 0.00 [0.00, 0.00]; qwen3.6-27b lookup 0.00 [0.00, 0.00]; qwen3.6-27b recall 0.00 [0.00, 0.00]; qwen3.6-27b recall 0.00 [0.00, 0.00].

Layer sources: qwen3.6-27b: results/x51_jread/x51_10_27b/peak.json, results/x51_jread/read-x51_10_27b-20261028T185638Z/read.json.

Figure: x53_lastconflict.png
