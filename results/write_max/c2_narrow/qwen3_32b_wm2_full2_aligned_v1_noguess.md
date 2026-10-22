# C2' (narrow) / qwen3_32b_wm2_full2_aligned_v1_noguess: HOLDS (rule in scripts/c2_narrow.py, docs/prereg_replication_1022.md)

| source | X->P write (CV) | X->M write (CV) | X->M >= X->P + 10 | X->M >= 3x | intervals apart | min n | pass |
|---|---|---|---|---|---|---|---|
| P | 0 [0-8] | 24 [16-38] | True | True | True | 46 | True |
| C | 0 [0-7] | 31 [19-41] | True | True | True | 43 | True |

Brackets: the best single cell's 95% interval over bridge entities (the interval guard uses these).
Recalled bridges, reported only (CV write): MP 3, MM 75
