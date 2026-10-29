# 53.3: the conflict test at the last token

Batch 53, test 53.3 (jobs/c3/batch53.yaml; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). The change at the last token (P3) at 51.10's read-peak layer and the answer layer minus 2, per reader; 51.10's locker-first items. UNVERIFIED.

Rule (Dan's brief): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between".

As computed: the loss beyond random = X0's excess (S_no_rand - S_no_jpp) / S_whole; the rest alone's share = S_rest / S_whole; S_arm = the share of the locker-first items switched (the top token is S's answer's first token); point estimates decide (EPS 1e-9 at the bars); cluster-bootstrap CIs over the original bridge entities (10000, seed 0, paired) beside; S_whole = 0: not tested.

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | the rest alone | loss beyond random | rest / whole | label | X0 valid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | lookup | 32 (read peak) | 59 (30) | 0.90 [0.81, 0.97] | 0.88 [0.80, 0.95] | 0.88 [0.80, 0.95] | 0.00 [0.00, 0.00] | 0.88 [0.80, 0.95] | 0.00 [0.00, 0.00] | 0.98 [0.95, 1.00] | **computes outside the lens at the last token** | yes |
| nemotron-3.5-lightning | lookup | 43 (answer L45 - 2) | 59 (30) | 1.00 [1.00, 1.00] | 0.63 [0.50, 0.76] | 0.92 [0.85, 0.98] | 0.10 [0.04, 0.17] | 0.63 [0.50, 0.76] | 0.29 [0.18, 0.39] | 0.63 [0.50, 0.76] | **in between** | yes |
| nemotron-3.5-lightning | recall | 36 (read peak) | 59 (30) | 0.95 [0.89, 1.00] | 0.44 [0.26, 0.61] | 0.80 [0.64, 0.92] | 0.19 [0.09, 0.29] | 0.44 [0.26, 0.61] | 0.38 [0.22, 0.53] | 0.46 [0.29, 0.63] | **through the lens** | yes |
| nemotron-3.5-lightning | recall | 47 (answer L49 - 2) | 59 (30) | 1.00 [1.00, 1.00] | 0.22 [0.12, 0.31] | 0.88 [0.78, 0.96] | 0.53 [0.38, 0.67] | 0.22 [0.12, 0.31] | 0.66 [0.57, 0.75] | 0.22 [0.12, 0.31] | **through the lens** | yes |

O unedited switched (floor): nemotron-3.5-lightning lookup 0.00 [0.00, 0.00]; nemotron-3.5-lightning lookup 0.00 [0.00, 0.00]; nemotron-3.5-lightning recall 0.02 [0.00, 0.05]; nemotron-3.5-lightning recall 0.02 [0.00, 0.05].

Layer sources: nemotron-3.5-lightning: results/x51_jread/nem35l_x52_jread/peak.json, results/x51_jread/read-nem35l_x52_jread-20261029T005704Z/read.json.

Figure: x53_lastconflict.png
