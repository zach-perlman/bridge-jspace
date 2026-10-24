# X0 probes: x0_probe_v4_27b (qwen3.6-27b, layer 32, the bridge's word, org run)

Descriptive, added after data (Dan, 24 Oct evening); not part of X0's rule. Source run None (set d1_topics_v4). Probes cross-validated by bridge entity ((a), (b)) or by item ((c)); 10000 cluster-bootstrap resamples over entities, seed 0. 'structure' and 'layout' (b only) are the agent's additions: the training folds' most frequent locker index given the asked pick's sentence index (structure), or given which sentences before the pick are locker sentences (layout: what the word can see of the scene, with no binding). UNVERIFIED.

Pre-stated reading (Dan): (a) high in locker-before and at chance in locker-after -> the answer value is stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address. Locker-after: the locker sentence follows the word, so the stratum is a control by construction.

| subset | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| every scene | before | answer digit | 758 | 46 | 9 | 0.40 [0.36, 0.44] | 0.10 [0.07, 0.13] | 0.11 | - | - | 0.29 [0.25, 0.33] (chance) |
| every scene | before | locker sentence | 758 | 46 | 5 | 0.99 [0.98, 1.00] | 0.33 [0.30, 0.36] | 0.20 | 0.35 [0.32, 0.39] | 0.53 [0.50, 0.56] | 0.46 [0.43, 0.49] (layout) |
| every scene | before | bridge identity | 758 | 46 | 46 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.21] | 0.02 | - | - | 0.93 [0.79, 1.00] (majority) |
| every scene | after | answer digit | 742 | 46 | 9 | 0.11 [0.08, 0.14] | 0.13 [0.11, 0.16] | 0.11 | - | - | -0.02 [-0.05, 0.01] (majority) |
| every scene | after | locker sentence | 742 | 46 | 5 | 0.34 [0.31, 0.37] | 0.33 [0.30, 0.36] | 0.20 | 0.37 [0.34, 0.40] | 0.36 [0.33, 0.39] | -0.03 [-0.07, 0.01] (structure) |
| every scene | after | bridge identity | 742 | 46 | 46 | 1.00 [1.00, 1.00] | 0.06 [0.00, 0.20] | 0.02 | - | - | 0.94 [0.80, 1.00] (majority) |
| every scene | both | answer digit | 1500 | 46 | 9 | 0.23 [0.20, 0.26] | 0.12 [0.10, 0.13] | 0.11 | - | - | 0.11 [0.08, 0.14] (majority) |
| every scene | both | locker sentence | 1500 | 46 | 6 | 0.66 [0.64, 0.68] | 0.17 [0.15, 0.18] | 0.17 | 0.22 [0.20, 0.24] | 0.33 [0.31, 0.35] | 0.33 [0.30, 0.36] (layout) |
| every scene | both | bridge identity | 1500 | 46 | 46 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.21] | 0.02 | - | - | 0.93 [0.79, 1.00] (majority) |
