# X0 probes: x0_probe_27b (qwen3.6-27b, layer 32, the bridge's word, org run)

Descriptive, added after data (Dan, 24 Oct evening); not part of X0's rule. Source run x0_necessity_27b_chat (set d1_topics_v3). Probes cross-validated by bridge entity ((a), (b)) or by item ((c)); 10000 cluster-bootstrap resamples over entities, seed 0. 'structure' (b only) is the agent's addition: the most frequent locker index given the asked pick's sentence index. UNVERIFIED.

Pre-stated reading (Dan): (a) high in locker-before and at chance in locker-after -> the answer value is stored at the word, not in J++ form; (b) high in locker-before with (a) at chance -> the word stores an address. Locker-after: the locker sentence follows the word, so the stratum is a control by construction.

| subset | locker vs pick | target | n | entities | classes | probe | majority | chance | structure | probe - best baseline |
|---|---|---|---|---|---|---|---|---|---|---|
| X0 items | before | answer digit | 101 | 38 | 9 | 0.14 [0.07, 0.21] | 0.04 [0.01, 0.08] | 0.11 | - | 0.03 [-0.04, 0.10] (chance) |
| X0 items | before | locker sentence | 101 | 38 | 5 | 0.85 [0.79, 0.91] | 0.34 [0.24, 0.44] | 0.20 | 0.24 [0.15, 0.33] | 0.51 [0.42, 0.61] (majority) |
| X0 items | before | bridge identity | 101 | 38 | 38 | 0.67 [0.53, 0.78] | 0.08 [0.00, 0.23] | 0.03 | - | 0.59 [0.43, 0.73] (majority) |
| X0 items | after | answer digit | 99 | 33 | 9 | 0.04 [0.01, 0.09] | 0.07 [0.02, 0.13] | 0.11 | - | -0.07 [-0.10, -0.03] (chance) |
| X0 items | after | locker sentence | 99 | 33 | 5 | 0.29 [0.20, 0.38] | 0.36 [0.26, 0.45] | 0.20 | 0.33 [0.26, 0.42] | -0.07 [-0.15, 0.00] (majority) |
| X0 items | after | bridge identity | 99 | 33 | 33 | 0.81 [0.68, 0.89] | 0.11 [0.00, 0.31] | 0.03 | - | 0.70 [0.49, 0.85] (majority) |
| X0 items | both | answer digit | 200 | 44 | 9 | 0.10 [0.06, 0.13] | 0.07 [0.04, 0.11] | 0.11 | - | -0.02 [-0.05, 0.02] (chance) |
| X0 items | both | locker sentence | 200 | 44 | 6 | 0.55 [0.50, 0.60] | 0.10 [0.06, 0.15] | 0.17 | 0.16 [0.11, 0.21] | 0.38 [0.33, 0.43] (chance) |
| X0 items | both | bridge identity | 200 | 44 | 44 | 0.82 [0.72, 0.89] | 0.10 [0.00, 0.27] | 0.02 | - | 0.72 [0.55, 0.86] (majority) |
| every scene | before | answer digit | 301 | 45 | 9 | 0.20 [0.16, 0.24] | 0.10 [0.06, 0.14] | 0.11 | - | 0.08 [0.05, 0.13] (chance) |
| every scene | before | locker sentence | 301 | 45 | 5 | 0.95 [0.93, 0.98] | 0.24 [0.19, 0.30] | 0.20 | 0.35 [0.30, 0.40] | 0.61 [0.55, 0.66] (structure) |
| every scene | before | bridge identity | 301 | 45 | 45 | 0.96 [0.92, 0.98] | 0.07 [0.00, 0.23] | 0.02 | - | 0.88 [0.73, 0.97] (majority) |
| every scene | after | answer digit | 299 | 42 | 9 | 0.10 [0.06, 0.14] | 0.10 [0.07, 0.14] | 0.11 | - | -0.01 [-0.05, 0.03] (chance) |
| every scene | after | locker sentence | 299 | 42 | 5 | 0.34 [0.29, 0.39] | 0.34 [0.29, 0.39] | 0.20 | 0.29 [0.25, 0.34] | 0.00 [-0.05, 0.05] (majority) |
| every scene | after | bridge identity | 299 | 42 | 42 | 0.98 [0.96, 1.00] | 0.08 [0.00, 0.25] | 0.02 | - | 0.90 [0.74, 0.99] (majority) |
| every scene | both | answer digit | 600 | 46 | 9 | 0.15 [0.12, 0.18] | 0.09 [0.06, 0.13] | 0.11 | - | 0.04 [0.01, 0.07] (chance) |
| every scene | both | locker sentence | 600 | 46 | 6 | 0.63 [0.60, 0.67] | 0.15 [0.13, 0.18] | 0.17 | 0.17 [0.14, 0.20] | 0.46 [0.41, 0.51] (structure) |
| every scene | both | bridge identity | 600 | 46 | 46 | 0.99 [0.98, 1.00] | 0.07 [0.00, 0.18] | 0.02 | - | 0.92 [0.80, 0.99] (majority) |
