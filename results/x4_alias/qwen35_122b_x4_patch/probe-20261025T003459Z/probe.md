# X4 probe: the bridge's locker statement (its first mention), qwen35_122b_x4_patch

Descriptive (jobs/c3/X4.md). Org states at the bridge word; one-hot ridge; bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Within each form (cross-validated by bridge entity)

| form | n | entities | probe | majority | pick position only | chance | probe - best baseline |
|---|---|---|---|---|---|---|---|
| animals/same | 400 | 8 | 0.98 [0.97, 1.00] | 0.22 [0.16, 0.27] | 0.24 [0.20, 0.29] | 0.20 | 0.74 [0.69, 0.78] (structure) |
| animals/xlang | 400 | 8 | 0.90 [0.83, 0.94] | 0.22 [0.16, 0.27] | 0.24 [0.20, 0.29] | 0.20 | 0.65 [0.60, 0.70] (structure) |
| elements/same | 400 | 6 | 0.98 [0.95, 1.00] | 0.21 [0.18, 0.24] | 0.18 [0.15, 0.21] | 0.20 | 0.77 [0.71, 0.82] (majority) |
| elements/syn | 400 | 6 | 0.89 [0.81, 0.95] | 0.21 [0.18, 0.24] | 0.18 [0.15, 0.21] | 0.20 | 0.68 [0.60, 0.76] (majority) |

## Transfer: trained on the verbatim scenes, tested on the other form (same domain)

| domain | test form | n | accuracy | chance |
|---|---|---|---|---|
| animals | xlang | 400 | 0.85 [0.80, 0.91] | 0.20 |
| elements | syn | 400 | 0.90 [0.83, 0.96] | 0.20 |
