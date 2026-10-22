# C2' (narrow) / wm2_full2_v2: HOLDS (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 1 [0-6] | 18 [14-30] | True | True | True | 87 | True |
| C | 0 [0-0] | 17 [11-33] | True | True | True | 82 | True |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 31, MM 31
