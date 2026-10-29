# D1 + D2 (batch 47, amendment 3): the token x layer causal map, and window patching

Batch 52 coverage (no prediction: coverage run on an already-scored rule; designs ['main', 'clean']). Cells = S's state placed into O at one token group and one layer; the switch rate over the order group's items (X0's chat read; switch = the top token is S's answer); cluster bootstrap over bridge items (10000, seed 0; intervals in depth.json). Rules scored per design, point estimates; the Q-depth answer reads the clean design, the main test beside it. UNVERIFIED.

## Rules

| model | design | D1 (a) locker-after: bridge <= 0.25, a locker cell >= 0.5 | D1 (b) locker-first: lookup's bridge mass ends first | D1 (c) recall's lk_cf item hot in locker-first only | D2: l_R(recall) <= late band |
|---|---|---|---|---|---|
| nemotron-3.5-lightning | main | no (bridge max 0.9873417721518988, best locker {'arm': 'glk_cf_item@12', 'rate': 0.25316455696202533}) | no (lookup last 24, recall last 24, lead 0 of 4) | no (peaks first 0.01694915254237288, after 0.05063291139240506) | - (l_R recall 36, band None) |
| nemotron-3.5-lightning | clean | - (bridge max None, best locker None) | - (lookup last None, recall last None, lead None of None) | no (peaks first None, after None) | - (l_R recall None, band None) |

## l_R per reader (D2: the first sampled layer where the w curve is <= 0.1)

| model | design | order | lookup l_R | recall l_R | n |
|---|---|---|---|---|---|
| nemotron-3.5-lightning | main | locker-first | 28 | 28 | 59 |
| nemotron-3.5-lightning | main | locker-after | 12 | 36 | 79 |
| nemotron-3.5-lightning | main | all | 28 | 36 | 200 |

## Maps: nemotron-3.5-lightning (L14, 52 layers; sampled [0, 4, 8, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 50])

### main, locker-first, lookup (n = 59, 30 bridge items; none 0.00, a 0.98 [0.94, 1.00], S 1.00; l_R 28)

| group | emb | 0 | 4 | 8 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 0.98 | 0.98 | 0.81 | 0.64 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| pick_rest |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| person |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| question |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.39 | 0.24 | 0.12 | 0.05 | 0.03 | 0.02 | 0.00 | 0.00 | 0.00 |
| last |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.03 | 0.85 | 0.90 | 0.97 | 0.98 | 1.00 | 1.00 | 1.00 |
| margin b: bridge at every layer <= l | | 1.00 | 1.00 | 1.00 | 0.98 | 0.98 | 0.98 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 |
| D2 w: bridge at every layer >= l | | 0.97 | 0.97 | 0.97 | 0.95 | 0.97 | 0.97 | 0.83 | 0.63 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| margin d: pick sentence at every layer | 0.95 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### main, locker-first, recall (n = 59, 30 bridge items; none 0.02, a 1.00 [1.00, 1.00], S 1.00; l_R 28)

| group | emb | 0 | 4 | 8 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge | 0.98 | 0.98 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.75 | 0.53 | 0.07 | 0.05 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| pick_rest |  | 0.02 | 0.02 | 0.00 | 0.00 | 0.02 | 0.00 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| person |  | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| lk_org_item |  | 0.02 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| lk_org_num |  | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.00 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| lk_cf_item |  | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| lk_cf_num |  | 0.02 | 0.00 | 0.02 | 0.02 | 0.00 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| lk_other1_item |  | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| lk_other1_num |  | 0.02 | 0.02 | 0.02 | 0.02 | 0.00 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| question |  | 0.02 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.37 | 0.24 | 0.05 | 0.00 | 0.02 | 0.02 | 0.00 | 0.00 | 0.02 |
| last |  | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.69 | 0.86 | 0.97 | 1.00 | 1.00 | 1.00 | 1.00 |
| margin b: bridge at every layer <= l | | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 | 0.98 | 0.98 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 |
| D2 w: bridge at every layer >= l | | 0.98 | 0.98 | 0.98 | 0.97 | 0.97 | 0.98 | 0.71 | 0.47 | 0.07 | 0.05 | 0.00 | 0.02 | 0.00 | 0.02 | 0.02 |
| margin d: pick sentence at every layer | 0.98 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### main, locker-after, lookup (n = 79, 23 bridge items; none 0.00, a 0.05 [0.01, 0.10], S 0.99; l_R 12)

| group | emb | 0 | 4 | 8 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge | 0.99 | 0.97 | 0.65 | 0.43 | 0.05 | 0.05 | 0.05 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| pick_rest |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| person |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_item |  | 0.00 | 0.00 | 0.03 | 0.11 | 0.10 | 0.09 | 0.05 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.05 | 0.15 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_item |  | 0.00 | 0.00 | 0.01 | 0.25 | 0.15 | 0.14 | 0.06 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.08 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| question |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.11 | 0.08 | 0.01 | 0.00 | 0.01 | 0.01 | 0.01 | 0.00 | 0.00 |
| last |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.16 | 0.23 | 0.81 | 0.87 | 0.99 | 1.00 | 1.00 |
| margin b: bridge at every layer <= l | | 0.99 | 0.99 | 0.99 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 | 0.97 |
| D2 w: bridge at every layer >= l | | 0.97 | 0.63 | 0.39 | 0.06 | 0.05 | 0.08 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| margin d: pick sentence at every layer | 0.97 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

### main, locker-after, recall (n = 79, 23 bridge items; none 0.00, a 0.91 [0.84, 0.97], S 1.00; l_R 36)

| group | emb | 0 | 4 | 8 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bridge | 0.95 | 0.95 | 0.99 | 0.96 | 0.94 | 0.91 | 0.92 | 0.86 | 0.86 | 0.84 | 0.67 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| pick_rest |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| person |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_item |  | 0.00 | 0.00 | 0.00 | 0.01 | 0.01 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_org_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_item |  | 0.00 | 0.00 | 0.01 | 0.04 | 0.05 | 0.04 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_cf_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_item |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| lk_other1_num |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| question |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| last |  | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.03 | 0.20 | 0.95 | 0.99 | 1.00 | 1.00 | 1.00 |
| margin b: bridge at every layer <= l | | 0.95 | 0.96 | 0.96 | 0.96 | 0.96 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 | 0.95 |
| D2 w: bridge at every layer >= l | | 0.96 | 0.99 | 0.97 | 0.94 | 0.91 | 0.91 | 0.86 | 0.86 | 0.85 | 0.70 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| margin d: pick sentence at every layer | 0.95 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## Checks

- nemotron-3.5-lightning, states: the bridge after L under b14 on O's tokens vs S's, max relative distance 0.0 over 111 prefix-identical items, flagged 0
- nemotron-3.5-lightning, main lookup: O unedited reads O's answer on 200 of 200; S reads S's on 199; (a) switches 92
- nemotron-3.5-lightning, main recall: O unedited reads O's answer on 199 of 200; S reads S's on 200; (a) switches 191
- nemotron-3.5-lightning, clean lookup: O unedited reads O's answer on 0 of 0; S reads S's on 0; (a) switches 0; b14 vs S disagree on 0 (S's own run)
- nemotron-3.5-lightning, clean recall: O unedited reads O's answer on 0 of 0; S reads S's on 0; (a) switches 0; b14 vs S disagree on 0 (S's own run)
- nemotron-3.5-lightning, main items: 200 of 200 at L from nem35l_x52_conflict (dropped none; mixed left out 0; groups {'locker-after': 79, 'mixed': 62, 'locker-first': 59}; 37 bridge items)

Token groups: bridge = the bridge word; pick_rest = the rest of the asked pick sentence; person = the asked person's token; question = the question tokens (to the end of the prompt); last = the last token (the read position); lk_org_item = the item token(s) of O's bridge's locker sentence; lk_org_num = the number token(s) of O's bridge's locker sentence; lk_cf_item = the item token(s) of S's bridge's locker sentence; lk_cf_num = the number token(s) of S's bridge's locker sentence; lk_other1_item = the item token(s) of the first other item's locker sentence; lk_other1_num = the number token(s) of the first other item's locker sentence; lk_other2_item = the item token(s) of the second other item's locker sentence; lk_other2_num = the number token(s) of the second other item's locker sentence.
Arms: none = O unedited; a = (a) h_S - h_O added at the bridge word at L (47.4's (a), X0's whole arm); d = the whole asked pick sentence swapped at every layer (47.4's (d); margin); S = S read on S (unedited); b<l> = the bridge swapped at every layer <= l (47.4's (b); margin); w<l> = D2: S's state at the bridge at every block output >= l (the complement of b); g<group>@<l> = D1 cell: S's state placed at the group's tokens at block output l; gbridge@emb = D1 cell: O's prompt with S's bridge token, no state placed.
