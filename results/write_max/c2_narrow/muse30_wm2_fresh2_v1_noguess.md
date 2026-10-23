# C2' (narrow) / muse30_wm2_fresh2_v1_noguess: FAILS (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 0 [0-8] | 6 [4-28] | False | True | False | 44 | False |
| C | 1 [0-10] | 18 [10-33] | True | True | False | 43 | False |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 4, MM 38
