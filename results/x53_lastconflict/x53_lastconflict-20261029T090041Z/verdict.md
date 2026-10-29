# 53.3: the conflict test at the last token

Batch 53, test 53.3 (jobs/c3/batch53.yaml; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). The change at the last token (P3) at 51.10's read-peak layer and the answer layer minus 2, per reader; 51.10's locker-first items. UNVERIFIED.

Rule (Dan's brief): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between".

As computed: the loss beyond random = X0's excess (S_no_rand - S_no_jpp) / S_whole; the rest alone's share = S_rest / S_whole; S_arm = the share of the locker-first items switched (the top token is S's answer's first token); point estimates decide (EPS 1e-9 at the bars); cluster-bootstrap CIs over the original bridge entities (10000, seed 0, paired) beside; S_whole = 0: not tested.

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | the rest alone | loss beyond random | rest / whole | label | X0 valid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| muse-glimmer-30b | lookup | 32 (read peak) | 68 (29) | 0.88 [0.82, 0.95] | 0.88 [0.82, 0.95] | 0.88 [0.82, 0.95] | 0.00 [0.00, 0.00] | 0.88 [0.82, 0.95] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | **computes outside the lens at the last token** | yes |
| muse-glimmer-30b | lookup | 33 (answer L35 - 2) | 68 (29) | 0.93 [0.87, 0.98] | 0.93 [0.87, 0.98] | 0.93 [0.87, 0.98] | 0.00 [0.00, 0.00] | 0.93 [0.87, 0.98] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | **computes outside the lens at the last token** | yes |
| muse-glimmer-30b | recall | 40 (read peak) | 68 (29) | 1.00 [1.00, 1.00] | 0.85 [0.72, 0.96] | 0.96 [0.88, 1.00] | 0.03 [0.00, 0.08] | 0.85 [0.72, 0.96] | 0.10 [0.02, 0.22] | 0.85 [0.72, 0.96] | **in between** | yes |
| muse-glimmer-30b | recall | 44 (answer L46 - 2) | 68 (29) | 1.00 [1.00, 1.00] | 0.62 [0.46, 0.76] | 0.96 [0.87, 1.00] | 0.15 [0.07, 0.24] | 0.62 [0.46, 0.76] | 0.34 [0.20, 0.49] | 0.62 [0.46, 0.76] | **through the lens** | yes |

O unedited switched (floor): muse-glimmer-30b lookup 0.00 [0.00, 0.00]; muse-glimmer-30b lookup 0.00 [0.00, 0.00]; muse-glimmer-30b recall 0.00 [0.00, 0.00]; muse-glimmer-30b recall 0.00 [0.00, 0.00].

Layer sources: muse-glimmer-30b: results/x51_jread/muse30_x51_10/peak.json, results/x51_jread/read-muse30_x51_10-20261028T185636Z/read.json.

Figure: x53_lastconflict.png
