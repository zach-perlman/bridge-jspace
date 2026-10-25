# Which route the lookup follows: x6_routes_bothoff_ctrl_27b

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.6-27b, layer 32. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.54 [0.43, 0.65] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.36 [0.25, 0.47] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.50 [0.39, 0.62] |
| C0 | no_alf | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.15 [0.11, 0.18] | 0.85 [0.82, 0.89] | 0.37 [0.28, 0.47] |
| C0 | no_alf_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.99 [0.98, 1.00] | 0.46 [0.35, 0.57] |
| C0 | no_both | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.47 [0.42, 0.52] | 0.53 [0.48, 0.58] | 0.10 [0.06, 0.14] |
| C0 | no_both_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.08 [0.05, 0.11] | 0.92 [0.89, 0.95] | 0.33 [0.24, 0.43] |
| C0 | no_alf_jrand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.24 [0.20, 0.29] | 0.76 [0.71, 0.80] | 0.28 [0.19, 0.37] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 54.24.

Extra loss of the switch (Jdep - Rdep, each part against a random part of its own share); 'both - alf': the union's extra loss minus the pointer directions' (paired resamples).

| condition | reader | part | n | S_whole | Jdep | Rdep | extra loss | median share |
|---|---|---|---|---|---|---|---|---|
| C0 | PP | jpp | 300 | 0.98 | -0.01 [-0.02, 0.01] | -0.00 [-0.01, 0.00] | -0.00 [-0.01, 0.01] | 0.114 |
| C0 | PP | alf | 300 | 0.98 | 0.15 [0.11, 0.18] | -0.01 [-0.02, 0.01] | 0.15 [0.12, 0.19] | 0.140 |
| C0 | PP | both | 300 | 0.98 | 0.47 [0.43, 0.52] | 0.06 [0.03, 0.10] | 0.41 [0.35, 0.47] | 0.261 |
| C0 | PP | both - alf | 300 | | | | 0.26 [0.19, 0.32] | |
| C0 | PM | jpp | 300 | 0.54 | 0.34 [0.26, 0.43] | 0.08 [0.03, 0.14] | 0.26 [0.19, 0.34] | 0.114 |
| C0 | PM | alf | 300 | 0.54 | 0.32 [0.25, 0.40] | 0.15 [0.11, 0.21] | 0.17 [0.10, 0.23] | 0.140 |
| C0 | PM | both | 300 | 0.54 | 0.82 [0.76, 0.88] | 0.39 [0.31, 0.47] | 0.43 [0.36, 0.51] | 0.261 |
| C0 | PM | both - alf | 300 | | | | 0.27 [0.16, 0.37] | |

Switches lost (share of the whole change's switches; no random control subtracted) without the pointer directions, without them and J++, and without them and a random part of J++'s share; the last row: J++'s union minus the random union (paired resamples).

| condition | reader | removed | n | switches lost |
|---|---|---|---|---|
| C0 | PP | alf | 300 | 0.15 [0.11, 0.18] |
| C0 | PP | alf + J++ | 300 | 0.47 [0.43, 0.52] |
| C0 | PP | alf + random (J++ share) | 300 | 0.24 [0.20, 0.29] |
| C0 | PP | alf + J++ - alf + random | 300 | 0.23 [0.18, 0.27] |
| C0 | PM | alf | 300 | 0.32 [0.25, 0.40] |
| C0 | PM | alf + J++ | 300 | 0.82 [0.76, 0.88] |
| C0 | PM | alf + random (J++ share) | 300 | 0.49 [0.40, 0.58] |
| C0 | PM | alf + J++ - alf + random | 300 | 0.33 [0.25, 0.41] |
