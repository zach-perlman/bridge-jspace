# X0 probes: qwen35_9b_x0_probe (qwen3.5-9b, layer 12, the bridge's word, org run)

Descriptive, added after data (Dan, 24 Oct evening); not part of X0's rule. Source run qwen35_9b_x0_necessity (set d1_topics_v3). Probes cross-validated by bridge entity ((a), (b)) or by item ((c)); 10000 cluster-bootstrap resamples over entities, seed 0. 'structure' and 'layout' (b only) are the agent's additions: the training folds' most frequent locker index given the asked pick's sentence index (structure), or given which sentences before the pick are locker sentences (layout: what the word can see of the scene, with no binding). UNVERIFIED.

Pre-stated reading (Dan): (a) high in locker-before and at chance in locker-after -> the answer value is stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address. Locker-after: the locker sentence follows the word, so the stratum is a control by construction.

| subset | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X0 items | before | answer digit | 100 | 35 | 9 | 0.13 [0.06, 0.19] | 0.11 [0.06, 0.17] | 0.11 | - | - | 0.02 [-0.05, 0.08] (chance) |
| X0 items | before | locker sentence | 100 | 35 | 5 | 0.82 [0.74, 0.89] | 0.31 [0.21, 0.41] | 0.20 | 0.32 [0.21, 0.42] | 0.44 [0.34, 0.53] | 0.38 [0.28, 0.48] (layout) |
| X0 items | before | bridge identity | 100 | 35 | 35 | 0.83 [0.71, 0.91] | 0.08 [0.00, 0.21] | 0.03 | - | - | 0.75 [0.60, 0.87] (majority) |
| X0 items | after | answer digit | 100 | 28 | 9 | 0.07 [0.03, 0.12] | 0.09 [0.03, 0.14] | 0.11 | - | - | -0.04 [-0.09, 0.01] (chance) |
| X0 items | after | locker sentence | 100 | 28 | 5 | 0.40 [0.31, 0.48] | 0.40 [0.31, 0.48] | 0.20 | 0.26 [0.17, 0.35] | 0.26 [0.19, 0.32] | 0.00 [0.00, 0.00] (majority) |
| X0 items | after | bridge identity | 100 | 28 | 28 | 0.87 [0.75, 0.94] | 0.12 [0.00, 0.34] | 0.04 | - | - | 0.75 [0.52, 0.91] (majority) |
| X0 items | both | answer digit | 200 | 40 | 9 | 0.12 [0.08, 0.17] | 0.12 [0.08, 0.17] | 0.11 | - | - | 0.00 [-0.04, 0.04] (majority) |
| X0 items | both | locker sentence | 200 | 40 | 6 | 0.56 [0.50, 0.62] | 0.17 [0.12, 0.21] | 0.17 | 0.25 [0.18, 0.31] | 0.21 [0.14, 0.29] | 0.31 [0.24, 0.39] (structure) |
| X0 items | both | bridge identity | 200 | 40 | 40 | 0.92 [0.85, 0.96] | 0.10 [0.00, 0.30] | 0.03 | - | - | 0.81 [0.61, 0.94] (majority) |
| every scene | before | answer digit | 301 | 45 | 9 | 0.18 [0.15, 0.22] | 0.10 [0.06, 0.14] | 0.11 | - | - | 0.07 [0.03, 0.11] (chance) |
| every scene | before | locker sentence | 301 | 45 | 5 | 0.89 [0.85, 0.93] | 0.24 [0.19, 0.30] | 0.20 | 0.35 [0.30, 0.40] | 0.50 [0.45, 0.56] | 0.39 [0.34, 0.45] (layout) |
| every scene | before | bridge identity | 301 | 45 | 45 | 0.97 [0.94, 0.99] | 0.07 [0.00, 0.23] | 0.02 | - | - | 0.89 [0.74, 0.98] (majority) |
| every scene | after | answer digit | 299 | 42 | 9 | 0.12 [0.08, 0.15] | 0.10 [0.07, 0.14] | 0.11 | - | - | 0.01 [-0.03, 0.04] (chance) |
| every scene | after | locker sentence | 299 | 42 | 5 | 0.33 [0.28, 0.38] | 0.34 [0.29, 0.39] | 0.20 | 0.29 [0.25, 0.34] | 0.31 [0.26, 0.36] | -0.01 [-0.04, 0.03] (majority) |
| every scene | after | bridge identity | 299 | 42 | 42 | 0.99 [0.98, 1.00] | 0.08 [0.00, 0.25] | 0.02 | - | - | 0.91 [0.74, 1.00] (majority) |
| every scene | both | answer digit | 600 | 46 | 9 | 0.17 [0.14, 0.19] | 0.09 [0.06, 0.13] | 0.11 | - | - | 0.06 [0.03, 0.08] (chance) |
| every scene | both | locker sentence | 600 | 46 | 6 | 0.59 [0.55, 0.63] | 0.15 [0.13, 0.18] | 0.17 | 0.17 [0.14, 0.20] | 0.28 [0.26, 0.32] | 0.31 [0.27, 0.35] (layout) |
| every scene | both | bridge identity | 600 | 46 | 46 | 0.99 [0.99, 1.00] | 0.07 [0.00, 0.18] | 0.02 | - | - | 0.93 [0.81, 1.00] (majority) |
