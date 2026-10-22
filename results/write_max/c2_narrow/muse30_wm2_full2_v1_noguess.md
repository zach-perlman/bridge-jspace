# C2' (narrow) / muse30_wm2_full2_v1_noguess: FAILS (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 13 [4-26] | 15 [9-33] | False | False | False | 48 | False |
| C | 2 [0-13] | 16 [6-37] | True | True | False | 38 | False |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 2, MM 50
