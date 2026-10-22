# C2' (narrow) / qwen3_32b_wm2_full2_v1_noguess: FAILS (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 3 [2-19] | 15 [5-30] | True | True | False | 46 | False |
| C | 0 [0-8] | 2 [0-12] | False | True | False | 43 | False |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 3, MM 2
