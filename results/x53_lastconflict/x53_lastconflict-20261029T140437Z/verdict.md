# 53.3: the conflict test at the last token

Batch 53, test 53.3 (jobs/c3/batch53.yaml; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). The change at the last token (P3) at 51.10's read-peak layer and the answer layer minus 2, per reader; 51.10's locker-first items. UNVERIFIED.

Rule (Dan's brief): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between".

As computed: the loss beyond random = X0's excess (S_no_rand - S_no_jpp) / S_whole; the rest alone's share = S_rest / S_whole; S_arm = the share of the locker-first items switched (the top token is S's answer's first token); point estimates decide (EPS 1e-9 at the bars); cluster-bootstrap CIs over the original bridge entities (10000, seed 0, paired) beside; S_whole = 0: not tested.

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | the rest alone | loss beyond random | rest / whole | label | X0 valid |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-122b-a10b | lookup | 12 (read peak) | 53 (27) | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | - | - | **not tested (the whole change switches no item)** | no |
| qwen3.5-122b-a10b | lookup | 44 (answer L46 - 2) | 53 (27) | 0.06 [0.00, 0.14] | 0.02 [0.00, 0.06] | 0.02 [0.00, 0.06] | 0.02 [0.00, 0.06] | 0.02 [0.00, 0.06] | 0.00 [0.00, 0.00] | 0.33 [0.00, 0.50] | **in between** | no |
| qwen3.5-122b-a10b | recall | 44 (read peak) | 53 (27) | 0.75 [0.66, 0.85] | 0.23 [0.11, 0.37] | 0.36 [0.24, 0.49] | 0.06 [0.00, 0.13] | 0.23 [0.11, 0.37] | 0.17 [0.05, 0.30] | 0.30 [0.15, 0.48] | **in between** | yes |

O unedited switched (floor): qwen3.5-122b-a10b lookup 0.00 [0.00, 0.00]; qwen3.5-122b-a10b lookup 0.00 [0.00, 0.00]; qwen3.5-122b-a10b recall 0.00 [0.00, 0.00].

Layer sources: qwen3.5-122b-a10b: results/x51_jread/qwen35_122b_x51_10/peak.json, results/x51_jread/read-qwen35_122b_x51_10-20261029T140039Z/read.json.

Figure: x53_lastconflict.png
