# 45b, where the binding is made when the locker comes after the pick: x45b_binding_27b

Model qwen3.6-27b, L = 32 (L/2 = 16, L/4 = 8); items: x0_necessity_27b_chat's items whose org locker sentence comes after the asked pick, n = 99 (33 bridge entities; 99 locker-after, dropped none; aligned {'token': 99}). Read on O at its answer position as X0 reads; switch = the top token is S's answer. Cluster bootstrap over bridge entities (10000 resamples, seed 0). UNVERIFIED.

## Rule (lookup, point estimates): HOLDS

Rule (batch 45, fixed in advance): the reading-order explanation holds if (c) or (d) switches at least half of the lookups that S itself switches, while (a) stays at or below 0.25.
(c) switches 59 of the 99 lookups S switches (0.60 [0.49, 0.69]); (d) 3 of 99 (0.03 [0.00, 0.07]); (a) switches 8 of 99 (0.08 [0.03, 0.13]).

| arm | what | layer | lookup switch rate | lookup switched | recall switch rate (descriptive) | median ‖h_S − h_O‖ |
|---|---|---|---|---|---|---|
| none | O unedited | - | 0.00 [0.00, 0.00] | 0 / 99 | 0.00 [0.00, 0.00] | - |
| a | the bridge-word change at L | 32 | 0.08 [0.03, 0.13] | 8 / 99 | 0.76 [0.66, 0.85] | 50.1 |
| b_half | the bridge-word change at L/2 | 16 | 0.79 [0.72, 0.86] | 78 / 99 | 0.97 [0.93, 1.00] | 26.9 |
| b_quarter | the bridge-word change at L/4 | 8 | 0.97 [0.94, 1.00] | 96 / 99 | 0.99 [0.97, 1.00] | 17.3 |
| c | S patched into O at every locker-sentence token, at L | 32 | 0.60 [0.49, 0.69] | 59 / 99 | 0.03 [0.00, 0.06] | 97.0 |
| d | S patched into O at every locker-sentence token, at L/2 | 16 | 0.03 [0.00, 0.07] | 3 / 99 | 0.00 [0.00, 0.00] | 30.7 |
| S | S read on S (unedited) | - | 1.00 [1.00, 1.00] | 99 / 99 | 1.00 [1.00, 1.00] | - |

Among the items S itself switches:

| arm | lookup: share of S's switches | recall (descriptive) |
|---|---|---|
| c | 0.60 [0.49, 0.69] (59 / 99) | 0.03 [0.00, 0.06] (3 / 99) |
| d | 0.03 [0.00, 0.07] (3 / 99) | 0.00 [0.00, 0.00] (0 / 99) |

Checks against the main run (descriptive): PP a vs stored whole at L32: 98 of 99 agree (rerun 8, stored 9); PP b_half vs stored whole at L16: 99 of 99 agree (rerun 78, stored 78); PP S vs stored S read: 99 of 99 agree (rerun 99, stored 99); PM a vs stored whole at L32: 99 of 99 agree (rerun 75, stored 75); PM b_half vs stored whole at L16: 99 of 99 agree (rerun 96, stored 96); PM S vs stored S read: 99 of 99 agree (rerun 99, stored 99)

Sanity check (Dan ~22:35: O and S the same length, the same token ids after the bridge word, both readers): 34 of 99 items pass, 65 dropped.
The rule on the passing items: does not hold; (c) 12 of 34 S switches (0.35 [0.21, 0.47]), (d) 0 (0.00 [0.00, 0.00]), (a) 3 of 34 (0.09 [0.00, 0.19]).
