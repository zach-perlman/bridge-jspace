# 45b layer sweep (descriptive, after the data): qwen35_9b_x45b_sweep_v2

Model qwen3.5-9b, L = 12; the 45b items (locker after the pick). Switch = the top token is S's answer. Cluster bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## lookup (n = 100, S switches 100): switch rate over the items

| layer | the bridge-word change | S patched into O at every locker-sentence token | only the item's tokens inside the locker sentences | only the value token(s) | only the sentence-final token |
|---|---|---|---|---|---|
| 6 | 0.68 [0.60, 0.77] | 0.12 [0.07, 0.18] | 0.08 [0.04, 0.12] | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.03] |
| 8 | 0.39 [0.32, 0.48] | 0.33 [0.22, 0.45] | 0.26 [0.17, 0.36] | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.03] |
| 10 | 0.29 [0.22, 0.37] | 0.33 [0.22, 0.45] | 0.16 [0.10, 0.23] | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.03] |
| 12 | 0.20 [0.14, 0.28] | 0.66 [0.53, 0.76] | 0.39 [0.29, 0.49] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.03] |

## recall (n = 100, S switches 100): switch rate over the items

| layer | the bridge-word change | S patched into O at every locker-sentence token | only the item's tokens inside the locker sentences | only the value token(s) | only the sentence-final token |
|---|---|---|---|---|---|
| 6 | 0.98 [0.95, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 8 | 0.98 [0.95, 1.00] | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 10 | 0.98 [0.95, 1.00] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 12 | 0.97 [0.94, 1.00] | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

