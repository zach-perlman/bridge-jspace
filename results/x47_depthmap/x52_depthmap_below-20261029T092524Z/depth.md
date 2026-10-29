# D1 + D2 (batch 47, amendment 3): the token x layer causal map, and window patching

Batch 52 coverage (below gate (exploratory): Lightning's clean one-pick gate fails (recall 0.751 < 0.80, results/x0_necessity/nem35l_x45s_smoke_clean/gate.json); eligible items only; hollow, never in the claims table or grades; rules verbatim, no prediction (Dan's morning queue, 29 Oct); designs ['clean']). Cells = S's state placed into O at one token group and one layer; the switch rate over the order group's items (X0's chat read; switch = the top token is S's answer); cluster bootstrap over bridge items (10000, seed 0; intervals in depth.json). Rules scored per design, point estimates; the Q-depth answer reads the clean design, the main test beside it. UNVERIFIED.

## Rules

| model | design | D1 (a) locker-after: bridge <= 0.25, a locker cell >= 0.5 | D1 (b) locker-first: lookup's bridge mass ends first | D1 (c) recall's lk_cf item hot in locker-first only | D2: l_R(recall) <= late band |
|---|---|---|---|---|---|
| nemotron-3.5-lightning | clean | no (bridge max 0.9924812030075187, best locker {'arm': 'glk_cf_item@12', 'rate': 0.22556390977443608}) | no (lookup last 24, recall last 24, lead 0 of 4) | no (peaks first 0.011235955056179775, after 0.015037593984962405) | - (l_R recall 36, band None) |

## l_R per reader (D2: the first sampled layer where the w curve is <= 0.1)

| model | design | order | lookup l_R | recall l_R | n |
|---|---|---|---|---|---|
| nemotron-3.5-lightning | clean | locker-first | 28 | 28 | 89 |
| nemotron-3.5-lightning | clean | locker-after | 12 | 36 | 133 |
| nemotron-3.5-lightning | clean | all | 28 | 36 | 222 |

## Maps: nemotron-3.5-lightning (L14, 52 layers; sampled [0, 4, 8, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 50])

### clean, locker-first, lookup (n = 89, 37 bridge items; none 0.00, a 0.99 [0.96, 1.00], S 1.00; l_R 28)

| group | emb | 0 | 4 | 8 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 0.99 | 0.85 | 0.56 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| pick_rest |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| person |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other2_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other2_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| question |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.08 | 0.04 | 0.07 | 0.03 | 0.02 | 0.01 | 0.00 | 0.00 | 0.00 |
| last |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.92 | 0.98 | 0.98 | 0.99 | 1.00 | 1.00 | 1.00 |
| margin b: bridge at every layer <= l | | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| D2 w: bridge at every layer >= l | | 1.00 | 1.00 | 1.00 | 1.00 | 0.99 | 0.99 | 0.85 | 0.57 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| margin d: pick sentence at every layer | 1.00 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### clean, locker-first, recall (n = 89, 37 bridge items; none 0.01, a 0.99 [0.96, 1.00], S 1.00; l_R 28)

| group | emb | 0 | 4 | 8 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge | 1.00 | 0.98 | 0.98 | 0.97 | 0.97 | 0.99 | 0.98 | 0.74 | 0.52 | 0.03 | 0.02 | 0.01 | 0.02 | 0.02 | 0.01 | 0.01 |
| pick_rest |  | 0.01 | 0.01 | 0.02 | 0.01 | 0.01 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.02 | 0.01 | 0.01 | 0.01 |
| person |  | 0.01 | 0.01 | 0.01 | 0.01 | 0.02 | 0.00 | 0.00 | 0.01 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| lk_org_item |  | 0.01 | 0.01 | 0.00 | 0.01 | 0.02 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| lk_org_num |  | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.02 | 0.02 | 0.01 | 0.00 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| lk_cf_item |  | 0.01 | 0.01 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| lk_cf_num |  | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| lk_other1_item |  | 0.01 | 0.01 | 0.01 | 0.01 | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.01 | 0.01 | 0.00 | 0.01 | 0.01 | 0.01 |
| lk_other1_num |  | 0.01 | 0.01 | 0.01 | 0.02 | 0.01 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| lk_other2_item |  | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.02 | 0.02 | 0.01 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 |
| lk_other2_num |  | 0.01 | 0.01 | 0.01 | 0.00 | 0.02 | 0.02 | 0.01 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| question |  | 0.01 | 0.01 | 0.02 | 0.02 | 0.02 | 0.02 | 0.18 | 0.09 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 |
| last |  | 0.00 | 0.01 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.81 | 0.87 | 0.99 | 1.00 | 1.00 | 1.00 | 1.00 |
| margin b: bridge at every layer <= l | | 1.00 | 0.98 | 1.00 | 0.98 | 0.99 | 0.98 | 0.98 | 0.98 | 1.00 | 0.99 | 0.99 | 0.99 | 1.00 | 1.00 | 1.00 |
| D2 w: bridge at every layer >= l | | 1.00 | 0.99 | 0.97 | 0.97 | 0.98 | 0.98 | 0.73 | 0.52 | 0.04 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.00 |
| margin d: pick sentence at every layer | 0.99 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### clean, locker-after, lookup (n = 133, 31 bridge items; none 0.00, a 0.06 [0.02, 0.11], S 0.99; l_R 12)

| group | emb | 0 | 4 | 8 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge | 0.99 | 0.98 | 0.77 | 0.64 | 0.06 | 0.06 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| pick_rest |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| person |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_item |  | 0.00 | 0.02 | 0.02 | 0.11 | 0.09 | 0.07 | 0.05 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.05 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_item |  | 0.00 | 0.00 | 0.02 | 0.23 | 0.17 | 0.12 | 0.05 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other2_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other2_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| question |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.11 | 0.05 | 0.02 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 |
| last |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.16 | 0.24 | 0.83 | 0.93 | 1.00 | 1.00 | 1.00 |
| margin b: bridge at every layer <= l | | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 1.00 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 |
| D2 w: bridge at every layer >= l | | 0.98 | 0.74 | 0.63 | 0.06 | 0.06 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| margin d: pick sentence at every layer | 0.99 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### clean, locker-after, recall (n = 133, 31 bridge items; none 0.00, a 0.94 [0.89, 0.98], S 1.00; l_R 36)

| group | emb | 0 | 4 | 8 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge | 1.00 | 1.00 | 1.00 | 0.98 | 0.94 | 0.94 | 0.94 | 0.90 | 0.89 | 0.86 | 0.61 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| pick_rest |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| person |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_item |  | 0.01 | 0.00 | 0.01 | 0.02 | 0.00 | 0.01 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other2_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other2_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| question |  | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.01 | 0.02 | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 |
| last |  | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.01 | 0.00 | 0.03 | 0.22 | 0.98 | 1.00 | 1.00 | 1.00 | 1.00 |
| margin b: bridge at every layer <= l | | 1.00 | 1.00 | 1.00 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 |
| D2 w: bridge at every layer >= l | | 1.00 | 0.99 | 0.98 | 0.94 | 0.93 | 0.95 | 0.90 | 0.89 | 0.86 | 0.61 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| margin d: pick sentence at every layer | 0.99 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## Checks

- nemotron-3.5-lightning, states: the bridge after L under b14 on O's tokens vs S's, max relative distance 0.0 over 222 prefix-identical items, flagged 0
- nemotron-3.5-lightning, clean lookup: O unedited reads O's answer on 222 of 222; S reads S's on 221; (a) switches 96; b14 vs S disagree on 0 (S's own run)
- nemotron-3.5-lightning, clean recall: O unedited reads O's answer on 219 of 222; S reads S's on 222; (a) switches 213; b14 vs S disagree on 2 (S's own run)
- nemotron-3.5-lightning, clean items: 222 of 295 at L from nem35l_x52_fresh (dropped none; mixed left out 73; groups {'locker-after': 133, 'locker-first': 89}; 38 bridge items)

Token groups: bridge = the bridge word; pick_rest = the rest of the asked pick sentence; person = the asked person's token; question = the question tokens (to the end of the prompt); last = the last token (the read position); lk_org_item = the item token(s) of O's bridge's locker sentence; lk_org_num = the number token(s) of O's bridge's locker sentence; lk_cf_item = the item token(s) of S's bridge's locker sentence; lk_cf_num = the number token(s) of S's bridge's locker sentence; lk_other1_item = the item token(s) of the first other item's locker sentence; lk_other1_num = the number token(s) of the first other item's locker sentence; lk_other2_item = the item token(s) of the second other item's locker sentence; lk_other2_num = the number token(s) of the second other item's locker sentence.
Arms: none = O unedited; a = (a) h_S - h_O added at the bridge word at L (47.4's (a), X0's whole arm); d = the whole asked pick sentence swapped at every layer (47.4's (d); margin); S = S read on S (unedited); b<l> = the bridge swapped at every layer <= l (47.4's (b); margin); w<l> = D2: S's state at the bridge at every block output >= l (the complement of b); g<group>@<l> = D1 cell: S's state placed at the group's tokens at block output l; gbridge@emb = D1 cell: O's prompt with S's bridge token, no state placed.
