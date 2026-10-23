# C2' (narrow) / qwen35_9b_wm2_full2_v1_noguess: HOLDS (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 0 [0-7] | 15 [8-31] | True | True | True | 54 | True |
| C | 0 [0-0] | 14 [9-35] | True | True | True | 39 | True |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 0, MM 61
