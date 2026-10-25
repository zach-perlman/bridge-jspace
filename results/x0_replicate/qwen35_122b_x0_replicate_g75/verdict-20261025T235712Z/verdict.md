# Replication of the 9B's double dissociation: qwen35_122b_x0_replicate_g75

Fixed in advance (Dan, 25 Oct morning item 4; spec jobs/c3/x0_replicate.yaml; prediction: batch 31). Model qwen3.5-122b-a10b (descriptive), layer 33, 200 items of d1_topics_v5 (single change, both locker sentences before the pick). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ (k = 25) | lookup | 0.180 | 1.00 | 1.00 | 1.00 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| J++ (k = 25) | recall | 0.180 | 0.94 | 0.86 | 0.92 | 0.08 [0.04, 0.13] | 0.03 [-0.01, 0.06] | 0.06 [0.03, 0.09] | around |
| pointer directions (Alf, not refit) | lookup | 0.167 | 1.00 | 0.72 | 0.99 | 0.28 [0.22, 0.34] | 0.01 [0.00, 0.02] | 0.27 [0.21, 0.33] | mixed |
| pointer directions (Alf, not refit) | recall | 0.167 | 0.94 | 0.81 | 0.91 | 0.15 [0.10, 0.21] | 0.04 [0.01, 0.07] | 0.11 [0.07, 0.16] | mixed |
| PCA at J++'s share | lookup | 0.178 | 1.00 | 0.98 | 1.00 | 0.02 [0.00, 0.04] | 0.00 [0.00, 0.00] | 0.02 [0.00, 0.04] | around |
| PCA at J++'s share | recall | 0.178 | 0.94 | 0.85 | 0.93 | 0.10 [0.05, 0.15] | 0.02 [0.00, 0.05] | 0.07 [0.03, 0.13] | around |

## Rule (descriptive): DOES NOT HOLD

Rule: holds iff J++: recall excess >= 0.20 with lower CI > 0 and lookup excess <= 0.10; and Alf: lookup excess >= 0.20 with lower CI > 0 and recall excess <= 0.10 or at most half the lookup's (point estimates where no CI is named).
J++ clause: not met; pointer clause: met.

## Pasted alone (descriptive): switches as a share of the whole change's, against the random part alone

| part | reader | n | kept / whole | random kept / whole | difference |
|---|---|---|---|---|---|
| J++ orthogonal to the word | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| J++ orthogonal to the word | recall | 200 | 0.04 [0.01, 0.07] | 0.02 [0.00, 0.05] | 0.02 [0.00, 0.04] |
| the word part | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| the word part | recall | 200 | 0.03 [0.01, 0.06] | 0.01 [0.00, 0.02] | 0.03 [0.01, 0.06] |
