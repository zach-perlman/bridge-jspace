# 51.5: the anatomy by depth on Zach's passages (UNVERIFIED)

Batch 51, test 51.5 (jobs/c3/batch51.yaml; batch 52, design from the 9B / 27B spec (jobs/c3/x51_5_9b.yaml / x51_5_27b.yaml), 51.5's rule verbatim; Zach's Lightning band L27-33 (x50_zach.BESIDE_BAND) beside the script's fixed swap window; no prediction (Dan's morning queue, 29 Oct)). Z1's items (his v2 passages, the pointer's name changed), the whole change at the name's last token at one layer at a time; readers K (lookup) and M (recall). Cluster bootstrap over the bridge entity (10000, seed 0).

Rule (fixed in advance): "The same read window as ours" if the last layer where each reader's switch >= 0.3 lies within 4 layers of ours (9B: both readers to ~L16, the recall to L24; 27B: from 49.4). Report against Zach's swap window (L4-20, gone by L25).

As computed: Items: Z1's chosen passages on the model (its gate.json order joined to its cases.jsonl; Z1's gate, alignment, strata, readers K = lookup and M = recall), re-aligned on the tokenizer before the run. Sweep: 9B L2-L30 every 2nd (47.8's 9B grid), 27B L4-L60 every 2nd (47.8's 27B span at step 2). Delta_l = h_S - h_O at the pointer name's last token per reader, added at layer l alone on O. Arms: whole; no_jpp (minus the signed-OMP J++ part, k = 25, the layer's own letter-token atoms); no_jpp_ratoms (minus a random part of the same share from random lens atoms, seed 777 + l, 47.8's control); no_jpp_rand (minus a random part of the same share in X0's random subspace, seed 888 + l, Z1's control). Switch = Z1's read (top token = the first token of S's answer). Per layer and reader: the whole change's switch share; extra loss without J++ = X0's excess against no_jpp_ratoms (Z1's no_jpp_rand beside); cluster bootstrap over the original bridge entity (10,000, seed 0). Window end = the last sampled layer whose switch share (point estimate) >= 0.30 (EPS 1e-9); None if no layer reaches it. Ours = the same function on the stored 47.8 runs (9B qwen35_9b_x47_anatomy, 27B x49_4_anatomy_27b; C2 test half; lookup switch = identity + position + value, recall = the changed item): 9B lookup L16, recall L14; 27B lookup L40, recall L32 (27B grid every 8th with L30-34). Per model: the same read window iff, for both readers, his window end exists and |his - ours| <= 4; decided on all of Z1's items (both strata pooled), each stratum's window end beside (a run that stopped after fact-first: the rule on fact-first alone, labelled partial). Z1's gate failed -> not tested (numbers descriptive). Zach's swap window beside, descriptive: each reader's first and last layer >= 0.3 against L4-L20, and whether the switch is < 0.3 at every sampled layer >= L25. The identity / position split (--split) runs only when the job's command carries the flag (off in the spec).

| model | run | status | n | decided on | lookup end: his / ours (diff) | recall end: his / ours (diff) | label |
|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | nem35l_x52_depth51 | tested | 200 | all of Z1's items (both strata) | L18 / L22 (-4) | L22 / L22 (0) | the same read window as ours |

## nemotron-3.5-lightning (nem35l_x52_depth51)

Z1's items: 200 (strata {'fact-first': 103, 'fact-after': 97}; Z1's gate pass True, O read {'K': 0.9945652173913043, 'M': 0.9184782608695652}). Ours: nem35l_x52_anatomy (lookup L22, recall L22; matches the opened verdict None: None; the spec's reference True).

Window ends (last layer >= 0.30): pooled: lookup L18, recall L22; fact-first: lookup L18, recall L22; fact-after: lookup L14, recall L30.

Beside, Zach's swap window (L4-L20, gone by L25): his_passages lookup L2-L18 gone by L25 True; his_passages recall L2-L22 gone by L25 True; our_scenes lookup L2-L22 gone by L25 True; our_scenes recall L2-L22 gone by L25 True.

| layer | n | lookup switch | recall switch | fact-first lookup / recall | fact-after lookup / recall | lookup extra loss no J++ (subspace) | recall extra loss no J++ (subspace) |
|---|---|---|---|---|---|---|---|
| 2 | 200 | 0.88 [0.82, 0.92] | 0.90 [0.86, 0.94] | 0.88 [0.82, 0.94] / 0.90 [0.84, 0.95] | 0.87 [0.79, 0.93] / 0.90 [0.83, 0.95] | 0.01 [0.00, 0.03] (0.01 [−0.02, 0.05]) | 0.02 [−0.01, 0.04] (0.02 [−0.01, 0.05]) |
| 6 | 200 | 0.83 [0.78, 0.89] | 0.90 [0.85, 0.94] | 0.88 [0.82, 0.94] / 0.89 [0.82, 0.95] | 0.78 [0.69, 0.87] / 0.90 [0.83, 0.95] | 0.14 [0.08, 0.20] (0.44 [0.36, 0.51]) | 0.17 [0.11, 0.23] (0.45 [0.37, 0.52]) |
| 10 | 200 | 0.82 [0.77, 0.88] | 0.89 [0.84, 0.93] | 0.87 [0.81, 0.93] / 0.88 [0.81, 0.94] | 0.77 [0.68, 0.86] / 0.89 [0.82, 0.95] | 0.05 [−0.01, 0.10] (0.44 [0.36, 0.52]) | 0.12 [0.07, 0.18] (0.59 [0.51, 0.68]) |
| 14 | 200 | 0.54 [0.46, 0.62] | 0.83 [0.78, 0.89] | 0.70 [0.60, 0.79] / 0.83 [0.75, 0.91] | 0.37 [0.27, 0.48] / 0.84 [0.76, 0.90] | 0.02 [−0.03, 0.07] (0.14 [0.05, 0.23]) | 0.10 [0.04, 0.17] (0.47 [0.40, 0.54]) |
| 18 | 200 | 0.40 [0.32, 0.47] | 0.75 [0.68, 0.81] | 0.57 [0.46, 0.68] / 0.73 [0.63, 0.82] | 0.21 [0.11, 0.30] / 0.77 [0.68, 0.85] | 0.05 [−0.01, 0.12] (0.22 [0.12, 0.31]) | 0.14 [0.08, 0.20] (0.48 [0.40, 0.57]) |
| 22 | 200 | 0.14 [0.09, 0.18] | 0.53 [0.46, 0.60] | 0.23 [0.15, 0.32] / 0.43 [0.33, 0.52] | 0.03 [0.00, 0.07] / 0.64 [0.54, 0.73] | 0.33 [0.14, 0.57] (0.56 [0.32, 0.81]) | 0.11 [0.06, 0.18] (0.66 [0.54, 0.78]) |
| 26 | 200 | 0.01 [0.00, 0.02] | 0.25 [0.19, 0.31] | 0.00 [0.00, 0.00] / 0.09 [0.03, 0.15] | 0.01 [0.00, 0.03] / 0.42 [0.32, 0.53] | 0.00 [0.00, 0.00] (2.00 [1.00, 4.00]) | 0.04 [−0.04, 0.12] (0.56 [0.42, 0.71]) |
| 30 | 200 | 0.01 [0.00, 0.02] | 0.17 [0.12, 0.22] | 0.00 [0.00, 0.00] / 0.03 [0.00, 0.07] | 0.01 [0.00, 0.03] / 0.32 [0.23, 0.41] | 0.00 [0.00, 0.00] (1.00 [1.00, 1.00]) | 0.09 [0.00, 0.20] (0.56 [0.37, 0.80]) |
| 34 | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | - (-) | - (-) |
| 38 | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | - (-) | - (-) |
| 42 | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | - (-) | - (-) |
| 46 | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | - (-) | - (-) |
| 50 | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] / 0.00 [0.00, 0.00] | - (-) | - (-) |
