# Replication of the 9B's double dissociation: qwen35_9b_x0_replicate

Fixed in advance (Dan, 25 Oct morning item 4; spec jobs/c3/x0_replicate.yaml; prediction: batch 31). Model qwen3.5-9b (decisive), layer 12, 200 items of d1_topics_v5 (single change, both locker sentences before the pick). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ (k = 25) | lookup | 0.180 | 0.99 | 0.99 | 0.98 | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | -0.01 [-0.02, 0.00] | around |
| J++ (k = 25) | recall | 0.180 | 0.96 | 0.82 | 0.94 | 0.14 [0.07, 0.22] | 0.02 [0.00, 0.04] | 0.12 [0.06, 0.19] | mixed |
| pointer directions (Alf, not refit) | lookup | 0.170 | 0.99 | 0.51 | 0.97 | 0.49 [0.42, 0.56] | 0.02 [0.00, 0.04] | 0.47 [0.41, 0.53] | through |
| pointer directions (Alf, not refit) | recall | 0.170 | 0.96 | 0.80 | 0.94 | 0.17 [0.10, 0.24] | 0.02 [0.00, 0.04] | 0.15 [0.10, 0.21] | mixed |
| PCA at J++'s share | lookup | 0.181 | 0.99 | 0.96 | 0.98 | 0.04 [0.01, 0.06] | 0.01 [0.00, 0.02] | 0.03 [0.00, 0.05] | around |
| PCA at J++'s share | recall | 0.181 | 0.96 | 0.89 | 0.95 | 0.07 [0.04, 0.11] | 0.01 [0.00, 0.03] | 0.06 [0.03, 0.10] | around |

## Rule (decisive): DOES NOT HOLD

Rule: holds iff J++: recall excess >= 0.20 with lower CI > 0 and lookup excess <= 0.10; and Alf: lookup excess >= 0.20 with lower CI > 0 and recall excess <= 0.10 or at most half the lookup's (point estimates where no CI is named).
J++ clause: not met; pointer clause: met.

## Pasted alone (descriptive): switches as a share of the whole change's, against the random part alone

| part | reader | n | kept / whole | random kept / whole | difference |
|---|---|---|---|---|---|
| J++ orthogonal to the word | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| J++ orthogonal to the word | recall | 200 | 0.05 [0.02, 0.09] | 0.01 [0.00, 0.03] | 0.04 [0.01, 0.07] |
| the word part | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| the word part | recall | 200 | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.03] |
