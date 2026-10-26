# Which route the lookup follows: muse30b_x6_routes_l13

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model muse-glimmer-30b, layer 13. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.99 [0.97, 1.00] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.11 [0.07, 0.15] | 0.89 [0.85, 0.93] | 0.83 [0.78, 0.89] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.99 [0.98, 1.00] |
| C2 | whole | 300 | 0.96 [0.93, 0.98] | 0.04 [0.02, 0.07] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.95 [0.92, 0.97] |
| C2 | no_jpp | 300 | 0.63 [0.57, 0.69] | 0.11 [0.08, 0.15] | 0.00 [0.00, 0.00] | 0.26 [0.20, 0.31] | 0.00 [0.00, 0.00] | 0.59 [0.52, 0.68] |
| C2 | no_jpp_rand | 300 | 0.93 [0.90, 0.96] | 0.03 [0.01, 0.05] | 0.00 [0.00, 0.00] | 0.04 [0.02, 0.06] | 0.00 [0.00, 0.00] | 0.90 [0.87, 0.93] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 134.10, C2 135.49.
