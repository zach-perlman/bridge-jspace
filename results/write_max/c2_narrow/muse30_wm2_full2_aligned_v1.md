# C2' (narrow) / muse30_wm2_full2_aligned_v1: FAILS (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 13 [5-23] | 8 [4-22] | False | False | False | 60 | False |
| C | 5 [2-16] | 17 [11-34] | True | True | False | 48 | False |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 7, MM 43
