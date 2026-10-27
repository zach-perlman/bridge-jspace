# X4 probe: the bridge's locker statement (its first mention), x4_probe_27b

Descriptive (jobs/c3/X4.md). Org states at the bridge word; one-hot ridge; bootstrap over bridge entities (10000 resamples). UNVERIFIED.

## Within each form (cross-validated by bridge entity)

| form | n | entities | probe | majority | pick position only | chance | probe - best baseline |
|---|---|---|---|---|---|---|---|
| animals/same | 400 | 8 | 1.00 [1.00, 1.00] | 0.22 [0.16, 0.27] | 0.24 [0.20, 0.29] | 0.20 | 0.76 [0.71, 0.80] (structure) |
| animals/xlang | 400 | 8 | 0.99 [0.99, 1.00] | 0.22 [0.16, 0.27] | 0.24 [0.20, 0.29] | 0.20 | 0.75 [0.71, 0.79] (structure) |
| elements/same | 400 | 6 | 0.99 [0.98, 1.00] | 0.21 [0.18, 0.24] | 0.18 [0.15, 0.21] | 0.20 | 0.79 [0.74, 0.82] (majority) |
| elements/syn | 400 | 6 | 0.97 [0.90, 1.00] | 0.21 [0.18, 0.24] | 0.18 [0.15, 0.21] | 0.20 | 0.76 [0.68, 0.81] (majority) |

## Transfer: trained on the verbatim scenes, tested on the other form (same domain)

| domain | test form | n | accuracy | chance |
|---|---|---|---|---|
| animals | xlang | 400 | 0.94 [0.90, 0.97] | 0.20 |
| elements | syn | 400 | 0.97 [0.90, 1.00] | 0.20 |
