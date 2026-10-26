# X0 probes: muse30b_x0_probe_v4 (muse-glimmer-30b, layer 26, the bridge's word, org run)

Descriptive, added after data (Dan, 24 Oct evening); not part of X0's rule. Source run None (set d1_topics_v4). Probes cross-validated by bridge entity ((a), (b)) or by item ((c)); 10000 cluster-bootstrap resamples over entities, seed 0. 'structure' and 'layout' (b only) are the agent's additions: the training folds' most frequent locker index given the asked pick's sentence index (structure), or given which sentences before the pick are locker sentences (layout: what the word can see of the scene, with no binding). UNVERIFIED.

Pre-stated reading (Dan): (a) high in locker-before and at chance in locker-after -> the answer value is stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address. Locker-after: the locker sentence follows the word, so the stratum is a control by construction.

| subset | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | layout | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| every scene | before | answer digit | 657 | 44 | 9 | 0.33 [0.28, 0.37] | 0.12 [0.09, 0.15] | 0.11 | - | - | 0.21 [0.16, 0.25] (majority) |
| every scene | before | locker sentence | 657 | 44 | 5 | 0.97 [0.95, 0.98] | 0.34 [0.31, 0.37] | 0.20 | 0.35 [0.30, 0.38] | 0.53 [0.49, 0.56] | 0.44 [0.41, 0.47] (layout) |
| every scene | before | bridge identity | 657 | 44 | 44 | 1.00 [0.99, 1.00] | 0.08 [0.00, 0.23] | 0.02 | - | - | 0.92 [0.76, 1.00] (majority) |
| every scene | after | answer digit | 669 | 44 | 9 | 0.10 [0.08, 0.11] | 0.14 [0.11, 0.16] | 0.11 | - | - | -0.04 [-0.06, -0.01] (majority) |
| every scene | after | locker sentence | 669 | 44 | 5 | 0.34 [0.31, 0.37] | 0.33 [0.30, 0.37] | 0.20 | 0.35 [0.31, 0.39] | 0.32 [0.28, 0.35] | -0.01 [-0.05, 0.04] (structure) |
| every scene | after | bridge identity | 669 | 44 | 44 | 1.00 [0.99, 1.00] | 0.07 [0.00, 0.22] | 0.02 | - | - | 0.93 [0.78, 1.00] (majority) |
| every scene | both | answer digit | 1326 | 44 | 9 | 0.20 [0.18, 0.22] | 0.11 [0.09, 0.13] | 0.11 | - | - | 0.09 [0.06, 0.11] (majority) |
| every scene | both | locker sentence | 1326 | 44 | 6 | 0.63 [0.61, 0.65] | 0.17 [0.15, 0.18] | 0.17 | 0.23 [0.21, 0.24] | 0.32 [0.30, 0.34] | 0.31 [0.28, 0.33] (layout) |
| every scene | both | bridge identity | 1326 | 44 | 44 | 1.00 [1.00, 1.00] | 0.07 [0.00, 0.22] | 0.02 | - | - | 0.93 [0.78, 1.00] (majority) |
