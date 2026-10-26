# Replication of the 9B's double dissociation: muse30b_x0_replicate

Fixed in advance (Dan, 25 Oct morning item 4; spec jobs/c3/x0_replicate.yaml; prediction: batch 31). Model muse-glimmer-30b (descriptive), layer 26, 200 items of d1_topics_v5 (single change, both locker sentences before the pick). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ (k = 25) | lookup | 0.098 | 0.94 | 0.95 | 0.94 | -0.02 [-0.05, 0.02] | -0.01 [-0.04, 0.02] | -0.01 [-0.03, 0.02] | around |
| J++ (k = 25) | recall | 0.098 | 0.59 | 0.42 | 0.60 | 0.29 [0.15, 0.43] | -0.02 [-0.05, 0.02] | 0.31 [0.16, 0.45] | mixed |
| pointer directions (Alf, not refit) | lookup | 0.135 | 0.94 | 0.56 | 0.94 | 0.40 [0.34, 0.47] | -0.01 [-0.04, 0.02] | 0.41 [0.34, 0.49] | through |
| pointer directions (Alf, not refit) | recall | 0.135 | 0.59 | 0.55 | 0.59 | 0.08 [-0.01, 0.18] | 0.00 [-0.05, 0.05] | 0.08 [0.00, 0.17] | around |
| PCA at J++'s share | lookup | 0.100 | 0.94 | 0.88 | 0.94 | 0.06 [0.00, 0.13] | -0.01 [-0.03, 0.02] | 0.07 [0.02, 0.13] | around |
| PCA at J++'s share | recall | 0.100 | 0.59 | 0.58 | 0.61 | 0.02 [-0.06, 0.09] | -0.03 [-0.07, 0.00] | 0.05 [-0.04, 0.13] | around |

## Rule (descriptive): HOLDS

Rule: holds iff J++: recall excess >= 0.20 with lower CI > 0 and lookup excess <= 0.10; and Alf: lookup excess >= 0.20 with lower CI > 0 and recall excess <= 0.10 or at most half the lookup's (point estimates where no CI is named).
J++ clause: met; pointer clause: met.

## Pasted alone (descriptive): switches as a share of the whole change's, against the random part alone

| part | reader | n | kept / whole | random kept / whole | difference |
|---|---|---|---|---|---|
| J++ orthogonal to the word | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| J++ orthogonal to the word | recall | 200 | 0.03 [0.00, 0.06] | 0.02 [0.00, 0.04] | 0.01 [-0.02, 0.04] |
| the word part | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| the word part | recall | 200 | 0.03 [0.00, 0.07] | 0.01 [0.00, 0.03] | 0.02 [0.00, 0.04] |
