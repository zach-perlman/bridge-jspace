# Which route the lookup follows: x6_routes_x45i_nochat_27b

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.6-27b, layer 32. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C2 | whole | 300 | 0.67 [0.62, 0.72] | 0.32 [0.27, 0.38] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.53 [0.44, 0.61] |
| C2 | no_jpp | 300 | 0.43 [0.38, 0.48] | 0.40 [0.36, 0.44] | 0.00 [0.00, 0.00] | 0.17 [0.13, 0.22] | 0.00 [0.00, 0.00] | 0.15 [0.10, 0.21] |
| C2 | no_jpp_rand | 300 | 0.68 [0.63, 0.73] | 0.30 [0.25, 0.35] | 0.00 [0.00, 0.00] | 0.02 [0.01, 0.03] | 0.00 [0.00, 0.00] | 0.46 [0.37, 0.55] |
| C2 | no_alf | 300 | 0.72 [0.67, 0.76] | 0.05 [0.03, 0.08] | 0.00 [0.00, 0.00] | 0.23 [0.19, 0.27] | 0.00 [0.00, 0.01] | 0.37 [0.28, 0.47] |
| C2 | no_alf_rand | 300 | 0.69 [0.64, 0.75] | 0.28 [0.23, 0.33] | 0.00 [0.00, 0.00] | 0.03 [0.01, 0.05] | 0.00 [0.00, 0.00] | 0.45 [0.37, 0.54] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C2 52.08.

## 45i: without the chat template (nochat, read X0 digit)

C2, lookup, whole change: value 0.00 [0.00, 0.00] (0 of 300), identity 0.67 [0.62, 0.72], position 0.32 [0.27, 0.38]. "Never the value" (the value share stays at 0): **holds**; value share 0 in every arm: yes.
