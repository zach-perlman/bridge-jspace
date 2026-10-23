# C2' (narrow) / qwen35_122b_wm2_full2_v1_noguess: FAILS (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 39 [31-55] | 58 [47-74] | True | False | False | 74 | False |
| C | 0 [0-7] | 4 [2-14] | False | True | False | 73 | False |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 23, MM 32
