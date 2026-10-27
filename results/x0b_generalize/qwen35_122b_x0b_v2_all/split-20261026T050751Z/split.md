# X0b's pooled rule on the 122B, b6's cells vs the new ones: qwen35_122b_x0b_v2_all, layer 33

Fixed in x0_122b_b12's spec before the run; after the data, descriptive, not scored (b6's cells were seen). Same functions as the verdict (x0b_generalize.contrast / rule), J++ k = 25 signed; bootstrap over bridge entities (10000 resamples). UNVERIFIED.

| subset | scenes | lookup excess | recall excess | C (recall - lookup) | rule |
|---|---|---|---|---|---|
| all cells (pooled) | 1552 | -0.02 [-0.03, -0.01] | 0.14 [0.11, 0.16] | 0.15 [0.13, 0.18] | mixed |
| b6's cells (prose and tables, levels 0-1) | 852 | -0.02 [-0.04, -0.01] | 0.15 [0.12, 0.18] | 0.16 [0.14, 0.20] | mixed |
| the new cells (json; level 2) | 700 | -0.01 [-0.03, 0.00] | 0.13 [0.10, 0.16] | 0.14 [0.10, 0.18] | mixed |
