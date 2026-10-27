# Which route the lookup follows: qwen35_9b_x6_routes_bothoff_ctrl

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.5-9b, layer 12. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.97 [0.94, 0.99] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.94 [0.91, 0.98] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.96 [0.93, 0.98] |
| C0 | no_alf | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.30 [0.25, 0.36] | 0.70 [0.64, 0.75] | 0.84 [0.79, 0.89] |
| C0 | no_alf_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.99 [0.98, 1.00] | 0.96 [0.93, 0.99] |
| C0 | no_both | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.54 [0.50, 0.59] | 0.46 [0.41, 0.50] | 0.46 [0.38, 0.55] |
| C0 | no_both_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.12 [0.08, 0.16] | 0.88 [0.84, 0.92] | 0.79 [0.74, 0.85] |
| C0 | no_alf_jrand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.62 [0.57, 0.67] | 0.38 [0.33, 0.43] | 0.59 [0.51, 0.68] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 16.49.

Extra loss of the switch (Jdep - Rdep, each part against a random part of its own share); 'both - alf': the union's extra loss minus the pointer directions' (paired resamples).

| condition | reader | part | n | S_whole | Jdep | Rdep | extra loss | median share |
|---|---|---|---|---|---|---|---|---|
| C0 | PP | jpp | 300 | 0.99 | -0.00 [-0.01, 0.00] | 0.00 [0.00, 0.00] | -0.00 [-0.01, 0.00] | 0.195 |
| C0 | PP | alf | 300 | 0.99 | 0.32 [0.26, 0.38] | 0.00 [0.00, 0.01] | 0.32 [0.26, 0.38] | 0.145 |
| C0 | PP | both | 300 | 0.99 | 0.54 [0.50, 0.59] | 0.11 [0.08, 0.16] | 0.43 [0.38, 0.48] | 0.331 |
| C0 | PP | both - alf | 300 | | | | 0.11 [0.04, 0.18] | |
| C0 | PM | jpp | 300 | 0.97 | 0.02 [-0.01, 0.05] | 0.01 [-0.01, 0.03] | 0.01 [-0.01, 0.04] | 0.195 |
| C0 | PM | alf | 300 | 0.97 | 0.13 [0.09, 0.18] | 0.01 [-0.01, 0.02] | 0.12 [0.08, 0.17] | 0.145 |
| C0 | PM | both | 300 | 0.97 | 0.52 [0.44, 0.60] | 0.18 [0.13, 0.23] | 0.34 [0.28, 0.40] | 0.331 |
| C0 | PM | both - alf | 300 | | | | 0.21 [0.15, 0.28] | |

Switches lost (share of the whole change's switches; no random control subtracted) without the pointer directions, without them and J++, and without them and a random part of J++'s share; the last row: J++'s union minus the random union (paired resamples).

| condition | reader | removed | n | switches lost |
|---|---|---|---|---|
| C0 | PP | alf | 300 | 0.32 [0.26, 0.38] |
| C0 | PP | alf + J++ | 300 | 0.54 [0.50, 0.59] |
| C0 | PP | alf + random (J++ share) | 300 | 0.62 [0.57, 0.67] |
| C0 | PP | alf + J++ - alf + random | 300 | -0.08 [-0.11, -0.04] |
| C0 | PM | alf | 300 | 0.13 [0.09, 0.18] |
| C0 | PM | alf + J++ | 300 | 0.52 [0.44, 0.60] |
| C0 | PM | alf + random (J++ share) | 300 | 0.39 [0.31, 0.46] |
| C0 | PM | alf + J++ - alf + random | 300 | 0.13 [0.09, 0.18] |
