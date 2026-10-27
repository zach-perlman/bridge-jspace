# 45b, where the binding is made when the locker comes after the pick: qwen35_9b_x45b_binding

Model qwen3.5-9b, L = 12 (L/2 = 6, L/4 = 3); items: qwen35_9b_x0_necessity's items whose org locker sentence comes after the asked pick, n = 100 (28 bridge entities; 100 locker-after, dropped none; aligned {'token': 100}). Read on O at its answer position as X0 reads; switch = the top token is S's answer. Cluster bootstrap over bridge entities (10000 resamples, seed 0). UNVERIFIED.

## Rule (lookup, point estimates): HOLDS

Rule (batch 45, fixed in advance): the reading-order explanation holds if (c) or (d) switches at least half of the lookups that S itself switches, while (a) stays at or below 0.25.
(c) switches 66 of the 100 lookups S switches (0.66 [0.53, 0.76]); (d) 12 of 100 (0.12 [0.07, 0.18]); (a) switches 20 of 100 (0.20 [0.14, 0.28]).

| arm | what | layer | lookup switch rate | lookup switched | recall switch rate (descriptive) | median ‖h_S − h_O‖ |
|---|---|---|---|---|---|---|
| none | O unedited | - | 0.01 [0.00, 0.03] | 1 / 100 | 0.00 [0.00, 0.00] | - |
| a | the bridge-word change at L | 12 | 0.20 [0.14, 0.28] | 20 / 100 | 0.97 [0.94, 1.00] | 17.6 |
| b_half | the bridge-word change at L/2 | 6 | 0.68 [0.60, 0.77] | 68 / 100 | 0.98 [0.95, 1.00] | 12.3 |
| b_quarter | the bridge-word change at L/4 | 3 | 0.93 [0.90, 0.97] | 93 / 100 | 0.99 [0.97, 1.00] | 6.5 |
| c | S patched into O at every locker-sentence token, at L | 12 | 0.66 [0.53, 0.76] | 66 / 100 | 0.01 [0.00, 0.03] | 27.6 |
| d | S patched into O at every locker-sentence token, at L/2 | 6 | 0.12 [0.07, 0.18] | 12 / 100 | 0.00 [0.00, 0.00] | 10.5 |
| S | S read on S (unedited) | - | 1.00 [1.00, 1.00] | 100 / 100 | 1.00 [1.00, 1.00] | - |

Among the items S itself switches:

| arm | lookup: share of S's switches | recall (descriptive) |
|---|---|---|
| c | 0.66 [0.53, 0.76] (66 / 100) | 0.01 [0.00, 0.03] (1 / 100) |
| d | 0.12 [0.07, 0.18] (12 / 100) | 0.00 [0.00, 0.00] (0 / 100) |

Checks against the main run (descriptive): PP a vs stored whole at L12: 99 of 100 agree (rerun 20, stored 19); PP b_half vs stored whole at L6: 99 of 100 agree (rerun 68, stored 67); PP S vs stored S read: 100 of 100 agree (rerun 100, stored 100); PM a vs stored whole at L12: 100 of 100 agree (rerun 97, stored 97); PM b_half vs stored whole at L6: 100 of 100 agree (rerun 98, stored 98); PM S vs stored S read: 100 of 100 agree (rerun 100, stored 100)
