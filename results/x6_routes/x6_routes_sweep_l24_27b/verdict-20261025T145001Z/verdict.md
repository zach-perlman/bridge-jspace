# Which route the lookup follows: x6_routes_sweep_l24_27b

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.6-27b, layer 24. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.99 [0.97, 1.00] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] |
| C2 | whole | 300 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [0.99, 1.00] |
| C2 | no_jpp | 300 | 0.94 [0.92, 0.97] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.04 [0.02, 0.07] | 0.00 [0.00, 0.00] | 0.95 [0.92, 0.97] |
| C2 | no_jpp_rand | 300 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.99 [0.98, 1.00] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 30.88, C2 31.13.
