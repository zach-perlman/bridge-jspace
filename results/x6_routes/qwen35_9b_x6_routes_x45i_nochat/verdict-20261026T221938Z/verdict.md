# Which route the lookup follows: qwen35_9b_x6_routes_x45i_nochat

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.5-9b, layer 12. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C2 | whole | 300 | 0.44 [0.39, 0.50] | 0.53 [0.48, 0.59] | 0.00 [0.00, 0.00] | 0.02 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.80 [0.76, 0.85] |
| C2 | no_jpp | 300 | 0.35 [0.30, 0.41] | 0.59 [0.53, 0.65] | 0.00 [0.00, 0.00] | 0.05 [0.02, 0.09] | 0.00 [0.00, 0.00] | 0.58 [0.51, 0.64] |
| C2 | no_jpp_rand | 300 | 0.41 [0.36, 0.46] | 0.47 [0.41, 0.52] | 0.00 [0.00, 0.00] | 0.13 [0.09, 0.16] | 0.00 [0.00, 0.00] | 0.72 [0.66, 0.78] |
| C2 | no_alf | 300 | 0.35 [0.29, 0.41] | 0.10 [0.06, 0.13] | 0.00 [0.00, 0.00] | 0.56 [0.49, 0.62] | 0.00 [0.00, 0.00] | 0.72 [0.64, 0.80] |
| C2 | no_alf_rand | 300 | 0.40 [0.35, 0.45] | 0.51 [0.45, 0.57] | 0.00 [0.00, 0.00] | 0.09 [0.05, 0.12] | 0.00 [0.00, 0.00] | 0.73 [0.66, 0.79] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C2 16.24.

## 45i: without the chat template (nochat, read X0 digit)

C2, lookup, whole change: value 0.00 [0.00, 0.00] (0 of 300), identity 0.44 [0.39, 0.50], position 0.53 [0.48, 0.59]. "Never the value" (the value share stays at 0): **holds**; value share 0 in every arm: yes.
