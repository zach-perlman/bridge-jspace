# C2' (narrow) / gptoss20_wm2_full2_v1: UNDERPOWERED (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 11 [0-29] | 0 [0-13] | False | False | False | 25 | False |
| C | 0 [0-12] | 4 [0-25] | False | True | False | 23 | False |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 0, MM 10
