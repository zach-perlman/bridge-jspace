# 45b, where the binding is made when the locker comes after the pick: muse30b_x45b_binding

Model muse-glimmer-30b, L = 26 (L/2 = 13, L/4 = 6); items: muse30b_x0_necessity's items whose org locker sentence comes after the asked pick, n = 108 (31 bridge entities; 108 locker-after, dropped none; aligned {'token': 108}). Read on O at its answer position as X0 reads; switch = the top token is S's answer. Cluster bootstrap over bridge entities (10000 resamples, seed 0). UNVERIFIED.

## Rule (lookup, point estimates): HOLDS

Rule (batch 45, fixed in advance): the reading-order explanation holds if (c) or (d) switches at least half of the lookups that S itself switches, while (a) stays at or below 0.25.
(c) switches 68 of the 108 lookups S switches (0.63 [0.51, 0.73]); (d) 22 of 108 (0.20 [0.13, 0.28]); (a) switches 9 of 108 (0.08 [0.03, 0.15]).

| arm | what | layer | lookup switch rate | lookup switched | recall switch rate (descriptive) | median ‖h_S − h_O‖ |
|---|---|---|---|---|---|---|
| none | O unedited | - | 0.00 [0.00, 0.00] | 0 / 108 | 0.00 [0.00, 0.00] | - |
| a | the bridge-word change at L | 26 | 0.08 [0.03, 0.15] | 9 / 108 | 0.66 [0.54, 0.76] | 171.6 |
| b_half | the bridge-word change at L/2 | 13 | 0.48 [0.37, 0.60] | 52 / 108 | 0.76 [0.66, 0.86] | 153.2 |
| b_quarter | the bridge-word change at L/4 | 6 | 0.80 [0.72, 0.88] | 86 / 108 | 0.84 [0.75, 0.91] | 105.7 |
| c | S patched into O at every locker-sentence token, at L | 26 | 0.63 [0.51, 0.73] | 68 / 108 | 0.06 [0.01, 0.11] | 411.7 |
| d | S patched into O at every locker-sentence token, at L/2 | 13 | 0.20 [0.13, 0.28] | 22 / 108 | 0.04 [0.01, 0.07] | 179.4 |
| S | S read on S (unedited) | - | 1.00 [1.00, 1.00] | 108 / 108 | 1.00 [1.00, 1.00] | - |

Among the items S itself switches:

| arm | lookup: share of S's switches | recall (descriptive) |
|---|---|---|
| c | 0.63 [0.51, 0.73] (68 / 108) | 0.06 [0.01, 0.11] (6 / 108) |
| d | 0.20 [0.13, 0.28] (22 / 108) | 0.04 [0.01, 0.07] (4 / 108) |

Checks against the main run (descriptive): PP a vs stored whole at L26: 107 of 108 agree (rerun 9, stored 10); PP b_half vs stored whole at L13: 107 of 108 agree (rerun 52, stored 51); PP S vs stored S read: 108 of 108 agree (rerun 108, stored 108); PM a vs stored whole at L26: 107 of 108 agree (rerun 71, stored 70); PM b_half vs stored whole at L13: 108 of 108 agree (rerun 82, stored 82); PM S vs stored S read: 108 of 108 agree (rerun 108, stored 108)

Sanity check (Dan ~22:35: O and S the same length, the same token ids after the bridge word, both readers): 34 of 108 items pass, 74 dropped.
The rule on the passing items: does not hold; (c) 14 of 34 S switches (0.41 [0.26, 0.58]), (d) 0 (0.00 [0.00, 0.00]), (a) 6 of 34 (0.18 [0.06, 0.31]).
