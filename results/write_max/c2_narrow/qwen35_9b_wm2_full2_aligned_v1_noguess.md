# C2' (narrow) / qwen35_9b_wm2_full2_aligned_v1_noguess: PARTIAL (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 2 [0-10] | 19 [10-36] | True | True | True | 54 | True |
| C | 0 [0-0] | 6 [4-22] | False | True | True | 39 | False |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 0, MM 60
