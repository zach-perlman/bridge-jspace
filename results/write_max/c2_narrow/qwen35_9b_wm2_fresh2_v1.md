# C2' (narrow) / qwen35_9b_wm2_fresh2_v1: PARTIAL (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 5 [2-13] | 16 [9-38] | True | True | False | 59 | False |
| C | 0 [0-0] | 16 [8-36] | True | True | True | 48 | True |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 0, MM 62
