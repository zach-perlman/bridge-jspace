# 45b layer sweep (descriptive, after the data): qwen35_9b_x45b_sweep_v2

Model qwen3.5-9b, L = 12; the 45b items (locker after the pick) that pass the sanity check (O and S the same length and the same ids after the bridge word): 36 of 100, 64 dropped. Switch = the top token is S's answer. Cluster bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## lookup (n = 36, S switches 36): switch rate over the items

| layer | the bridge-word change | S patched into O at every locker-sentence token | only the item's tokens inside the locker sentences | only the value token(s) | only the sentence-final token |
|---|---|---|---|---|---|
| 6 | 0.92 [0.80, 1.00] | 0.03 [0.00, 0.09] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 8 | 0.53 [0.33, 0.72] | 0.06 [0.00, 0.13] | 0.06 [0.00, 0.13] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 10 | 0.36 [0.20, 0.54] | 0.06 [0.00, 0.13] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 12 | 0.28 [0.16, 0.40] | 0.39 [0.26, 0.53] | 0.28 [0.16, 0.41] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

## recall (n = 36, S switches 36): switch rate over the items

| layer | the bridge-word change | S patched into O at every locker-sentence token | only the item's tokens inside the locker sentences | only the value token(s) | only the sentence-final token |
|---|---|---|---|---|---|
| 6 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 8 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 10 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 12 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

