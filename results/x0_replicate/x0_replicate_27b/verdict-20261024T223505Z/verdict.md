# Replication of the 9B's double dissociation: x0_replicate_27b

Fixed in advance (Dan, 25 Oct morning item 4; spec jobs/c3/x0_replicate.yaml; prediction: batch 31). Model qwen3.6-27b (descriptive), layer 32, 200 items of d1_topics_v5 (single change, both locker sentences before the pick). Bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |
|---|---|---|---|---|---|---|---|---|---|
| J++ (k = 25) | lookup | 0.106 | 0.99 | 0.98 | 0.99 | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | around |
| J++ (k = 25) | recall | 0.106 | 0.69 | 0.42 | 0.69 | 0.39 [0.29, 0.49] | 0.01 [-0.02, 0.06] | 0.37 [0.28, 0.46] | through |
| pointer directions (Alf, not refit) | lookup | 0.161 | 0.99 | 0.80 | 0.96 | 0.20 [0.14, 0.25] | 0.03 [0.00, 0.05] | 0.17 [0.12, 0.22] | mixed |
| pointer directions (Alf, not refit) | recall | 0.161 | 0.69 | 0.65 | 0.69 | 0.07 [-0.01, 0.16] | 0.01 [-0.05, 0.06] | 0.06 [-0.01, 0.15] | around |
| PCA at J++'s share | lookup | 0.107 | 0.99 | 0.99 | 0.99 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | around |
| PCA at J++'s share | recall | 0.107 | 0.69 | 0.66 | 0.69 | 0.05 [0.01, 0.10] | 0.01 [-0.04, 0.06] | 0.04 [0.00, 0.09] | around |

## Rule (descriptive): DOES NOT HOLD

Rule: holds iff J++: recall excess >= 0.20 with lower CI > 0 and lookup excess <= 0.10; and Alf: lookup excess >= 0.20 with lower CI > 0 and recall excess <= 0.10 or at most half the lookup's (point estimates where no CI is named).
J++ clause: met; pointer clause: not met.

## Pasted alone (descriptive): switches as a share of the whole change's, against the random part alone

| part | reader | n | kept / whole | random kept / whole | difference |
|---|---|---|---|---|---|
| J++ orthogonal to the word | lookup | 200 | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] |
| J++ orthogonal to the word | recall | 200 | 0.03 [0.00, 0.06] | 0.01 [0.00, 0.03] | 0.02 [-0.01, 0.06] |
| the word part | lookup | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| the word part | recall | 200 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
