# X0 probes: nem35l_x52_probe (nemotron-3.5-lightning, layer 14, the bridge's word, org run)

Descriptive, added after data (Dan, 24 Oct evening); not part of X0's rule. Source run None (set d1_topics_v4). Probes cross-validated by bridge entity ((a), (b)) or by item ((c)); 10000 cluster-bootstrap resamples over entities, seed 0. 'structure' and 'layout' (b only) are the agent's additions: the training folds' most frequent locker index given the asked pick's sentence index (structure), or given which sentences before the pick are locker sentences (layout: what the word can see of the scene, with no binding). UNVERIFIED.

Pre-stated reading (Dan): (a) high in locker-before and at chance in locker-after -> the answer value is stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address. Locker-after: the locker sentence follows the word, so the stratum is a control by construction.

| subset | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| every scene | before | answer digit | 636 | 43 | 9 | 0.25 [0.21, 0.28] | 0.11 [0.08, 0.15] | 0.11 | - | - | 0.14 [0.09, 0.18] (majority) |
| every scene | before | locker sentence | 636 | 43 | 5 | 0.85 [0.81, 0.88] | 0.34 [0.31, 0.37] | 0.20 | 0.33 [0.30, 0.36] | 0.52 [0.49, 0.54] | 0.33 [0.28, 0.38] (layout) |
| every scene | before | bridge identity | 636 | 43 | 43 | 1.00 [1.00, 1.00] | 0.08 [0.00, 0.24] | 0.02 | - | - | 0.92 [0.76, 1.00] (majority) |
| every scene | after | answer digit | 658 | 43 | 9 | 0.10 [0.08, 0.13] | 0.14 [0.11, 0.16] | 0.11 | - | - | -0.03 [-0.07, 0.00] (majority) |
| every scene | after | locker sentence | 658 | 43 | 5 | 0.36 [0.33, 0.39] | 0.33 [0.31, 0.37] | 0.20 | 0.36 [0.33, 0.40] | 0.31 [0.28, 0.35] | -0.01 [-0.04, 0.03] (structure) |
| every scene | after | bridge identity | 658 | 43 | 43 | 1.00 [0.99, 1.00] | 0.07 [0.00, 0.22] | 0.02 | - | - | 0.93 [0.78, 1.00] (majority) |
| every scene | both | answer digit | 1294 | 43 | 9 | 0.16 [0.13, 0.19] | 0.11 [0.09, 0.13] | 0.11 | - | - | 0.05 [0.02, 0.08] (majority) |
| every scene | both | locker sentence | 1294 | 43 | 6 | 0.58 [0.56, 0.60] | 0.16 [0.14, 0.18] | 0.17 | 0.22 [0.20, 0.24] | 0.30 [0.27, 0.33] | 0.28 [0.25, 0.31] (layout) |
| every scene | both | bridge identity | 1294 | 43 | 43 | 1.00 [1.00, 1.00] | 0.08 [0.00, 0.23] | 0.02 | - | - | 0.92 [0.77, 1.00] (majority) |
