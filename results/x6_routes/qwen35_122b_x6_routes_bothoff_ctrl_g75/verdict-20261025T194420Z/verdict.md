# Which route the lookup follows: qwen35_122b_x6_routes_bothoff_ctrl_g75

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.5-122b-a10b, layer 33. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.91 [0.86, 0.96] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.82 [0.74, 0.89] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.85 [0.79, 0.92] |
| C0 | no_alf | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.25 [0.21, 0.30] | 0.75 [0.70, 0.79] | 0.74 [0.66, 0.83] |
| C0 | no_alf_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.86 [0.79, 0.93] |
| C0 | no_both | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.49 [0.44, 0.55] | 0.51 [0.45, 0.56] | 0.45 [0.37, 0.55] |
| C0 | no_both_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.15 [0.11, 0.19] | 0.85 [0.81, 0.89] | 0.67 [0.58, 0.77] |
| C0 | no_alf_jrand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.50 [0.45, 0.55] | 0.50 [0.45, 0.55] | 0.52 [0.44, 0.62] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 3.66.

Extra loss of the switch (Jdep - Rdep, each part against a random part of its own share); 'both - alf': the union's extra loss minus the pointer directions' (paired resamples).

| condition | reader | part | n | S_whole | Jdep | Rdep | extra loss | median share |
|---|---|---|---|---|---|---|---|---|
| C0 | PP | jpp | 300 | 1.00 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | -0.00 [-0.01, 0.00] | 0.218 |
| C0 | PP | alf | 300 | 1.00 | 0.26 [0.22, 0.31] | 0.00 [0.00, 0.00] | 0.26 [0.22, 0.31] | 0.142 |
| C0 | PP | both | 300 | 1.00 | 0.50 [0.45, 0.55] | 0.15 [0.11, 0.19] | 0.35 [0.30, 0.42] | 0.369 |
| C0 | PP | both - alf | 300 | | | | 0.09 [0.03, 0.16] | |
| C0 | PM | jpp | 300 | 0.91 | 0.10 [0.06, 0.14] | 0.06 [0.03, 0.09] | 0.04 [0.01, 0.07] | 0.218 |
| C0 | PM | alf | 300 | 0.91 | 0.19 [0.13, 0.24] | 0.06 [0.03, 0.09] | 0.13 [0.07, 0.18] | 0.142 |
| C0 | PM | both | 300 | 0.91 | 0.50 [0.41, 0.58] | 0.26 [0.18, 0.34] | 0.24 [0.19, 0.29] | 0.369 |
| C0 | PM | both - alf | 300 | | | | 0.11 [0.03, 0.18] | |

Switches lost (share of the whole change's switches; no random control subtracted) without the pointer directions, without them and J++, and without them and a random part of J++'s share; the last row: J++'s union minus the random union (paired resamples).

| condition | reader | removed | n | switches lost |
|---|---|---|---|---|
| C0 | PP | alf | 300 | 0.26 [0.22, 0.31] |
| C0 | PP | alf + J++ | 300 | 0.50 [0.45, 0.55] |
| C0 | PP | alf + random (J++ share) | 300 | 0.50 [0.45, 0.55] |
| C0 | PP | alf + J++ - alf + random | 300 | 0.00 [-0.02, 0.03] |
| C0 | PM | alf | 300 | 0.19 [0.13, 0.24] |
| C0 | PM | alf + J++ | 300 | 0.50 [0.41, 0.58] |
| C0 | PM | alf + random (J++ share) | 300 | 0.43 [0.34, 0.51] |
| C0 | PM | alf + J++ - alf + random | 300 | 0.07 [0.04, 0.11] |
