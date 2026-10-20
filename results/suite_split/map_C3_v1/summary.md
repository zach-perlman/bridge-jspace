# suite_split / map_C3_v1

Cases: {"ARITH": {"families": ["ARITH"], "eligible_scenes": 200, "sampled": 150}, "TYPO": {"families": ["TYPO"], "eligible_scenes": 133, "sampled": 133}, "TRANS": {"families": ["TRANS"], "eligible_scenes": 200, "sampled": 150}, "eligible_items": {"ARITH": 200, "TYPO": 133, "TRANS": 200}}

Read vs greedy: {"n": 3840, "agree": 0.9982, "read/greedy": {"A/A": 3749, "b/b": 80, "A/b": 5, "other/other": 4, "b/A": 2}}

Windows: {"ARITH": {"question": [52, 56, 60]}, "TYPO": {"question": [24, 28, 32, 36, 40, 44, 48, 52, 56, 60], "last": [56, 60]}, "TRANS": {"question": [28, 32, 36, 40, 44, 48, 52, 56, 60], "last": [56, 60]}}
Windows by exp09's flip rule: {"TYPO": {"question": [28, 32, 36, 40, 44, 48, 52, 56]}, "TRANS": {"question": [36, 40, 44, 48, 52, 56, 60]}}
Answer formed: {}

| family | group | layer | n | C gives X's answer | O changes the answer | C frac (mean) | O frac (mean) |
|---|---|---|---|---|---|---|---|
| ARITH | question | 0 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | question | 4 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | question | 8 | 150 | 0% | 0% | +0.00 | -0.00 |
| ARITH | question | 12 | 150 | 0% | 0% | +0.00 | -0.00 |
| ARITH | question | 16 | 150 | 0% | 0% | +0.00 | -0.00 |
| ARITH | question | 20 | 150 | 0% | 0% | +0.01 | -0.00 |
| ARITH | question | 24 | 150 | 0% | 0% | +0.01 | -0.00 |
| ARITH | question | 28 | 150 | 0% | 0% | +0.02 | -0.00 |
| ARITH | question | 32 | 150 | 0% | 0% | +0.02 | -0.00 |
| ARITH | question | 36 | 150 | 0% | 0% | +0.02 | -0.00 |
| ARITH | question | 40 | 150 | 0% | 0% | +0.02 | -0.00 |
| ARITH | question | 44 | 150 | 0% | 0% | +0.02 | -0.00 |
| ARITH | question | 48 | 150 | 0% | 0% | +0.05 | -0.00 |
| ARITH | question | 52 | 150 | 4% | 0% | +0.31 | -0.00 |
| ARITH | question | 56 | 150 | 5% | 0% | +0.32 | -0.00 |
| ARITH | question | 60 | 150 | 2% | 0% | +0.31 | -0.00 |
| ARITH | last | 0 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 4 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 8 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 12 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 16 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 20 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 24 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 28 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 32 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 36 | 150 | 0% | 0% | -0.00 | -0.00 |
| ARITH | last | 40 | 150 | 0% | 0% | +0.00 | -0.00 |
| ARITH | last | 44 | 150 | 0% | 0% | +0.00 | -0.00 |
| ARITH | last | 48 | 150 | 0% | 0% | +0.00 | -0.00 |
| ARITH | last | 52 | 150 | 0% | 0% | +0.01 | -0.00 |
| ARITH | last | 56 | 150 | 0% | 0% | +0.01 | -0.00 |
| ARITH | last | 60 | 150 | 0% | 0% | +0.04 | -0.00 |
| TYPO | question | 0 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | question | 4 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | question | 8 | 133 | 0% | 0% | +0.01 | +0.00 |
| TYPO | question | 12 | 133 | 0% | 0% | +0.01 | +0.00 |
| TYPO | question | 16 | 133 | 0% | 0% | +0.01 | +0.00 |
| TYPO | question | 20 | 133 | 2% | 0% | +0.09 | +0.00 |
| TYPO | question | 24 | 133 | 5% | 0% | +0.22 | +0.00 |
| TYPO | question | 28 | 133 | 15% | 0% | +0.29 | +0.00 |
| TYPO | question | 32 | 133 | 10% | 0% | +0.29 | +0.00 |
| TYPO | question | 36 | 133 | 23% | 0% | +0.38 | +0.00 |
| TYPO | question | 40 | 133 | 34% | 0% | +0.45 | +0.00 |
| TYPO | question | 44 | 133 | 43% | 0% | +0.50 | +0.00 |
| TYPO | question | 48 | 133 | 35% | 0% | +0.46 | +0.00 |
| TYPO | question | 52 | 133 | 15% | 0% | +0.40 | +0.00 |
| TYPO | question | 56 | 133 | 13% | 0% | +0.40 | +0.00 |
| TYPO | question | 60 | 133 | 5% | 0% | +0.34 | +0.00 |
| TYPO | last | 0 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 4 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 8 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 12 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 16 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 20 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 24 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 28 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 32 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 36 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 40 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 44 | 133 | 0% | 0% | +0.00 | +0.00 |
| TYPO | last | 48 | 133 | 0% | 0% | +0.01 | +0.00 |
| TYPO | last | 52 | 133 | 0% | 0% | +0.09 | +0.00 |
| TYPO | last | 56 | 133 | 0% | 0% | +0.12 | +0.00 |
| TYPO | last | 60 | 133 | 0% | 0% | +0.16 | +0.00 |
| TRANS | question | 0 | 150 | 0% | 0% | -0.00 | -0.00 |
| TRANS | question | 4 | 150 | 2% | 0% | +0.02 | -0.00 |
| TRANS | question | 8 | 150 | 2% | 0% | +0.01 | -0.00 |
| TRANS | question | 12 | 150 | 2% | 0% | +0.01 | +0.00 |
| TRANS | question | 16 | 150 | 2% | 0% | +0.01 | +0.00 |
| TRANS | question | 20 | 150 | 2% | 0% | +0.03 | +0.00 |
| TRANS | question | 24 | 150 | 2% | 0% | +0.09 | +0.00 |
| TRANS | question | 28 | 150 | 2% | 0% | +0.13 | +0.00 |
| TRANS | question | 32 | 150 | 3% | 0% | +0.13 | +0.00 |
| TRANS | question | 36 | 150 | 12% | 0% | +0.28 | +0.00 |
| TRANS | question | 40 | 150 | 25% | 0% | +0.37 | -0.00 |
| TRANS | question | 44 | 150 | 40% | 0% | +0.42 | -0.00 |
| TRANS | question | 48 | 150 | 45% | 0% | +0.43 | -0.00 |
| TRANS | question | 52 | 150 | 33% | 0% | +0.40 | -0.00 |
| TRANS | question | 56 | 150 | 34% | 0% | +0.40 | -0.00 |
| TRANS | question | 60 | 150 | 8% | 0% | +0.33 | -0.00 |
| TRANS | last | 0 | 150 | 0% | 0% | +0.00 | -0.00 |
| TRANS | last | 4 | 150 | 0% | 0% | +0.00 | -0.00 |
| TRANS | last | 8 | 150 | 0% | 0% | -0.00 | -0.00 |
| TRANS | last | 12 | 150 | 0% | 0% | -0.00 | -0.00 |
| TRANS | last | 16 | 150 | 0% | 0% | +0.00 | -0.00 |
| TRANS | last | 20 | 150 | 0% | 0% | -0.00 | -0.00 |
| TRANS | last | 24 | 150 | 0% | 0% | -0.00 | -0.00 |
| TRANS | last | 28 | 150 | 0% | 0% | -0.00 | -0.00 |
| TRANS | last | 32 | 150 | 0% | 0% | +0.00 | -0.00 |
| TRANS | last | 36 | 150 | 0% | 0% | +0.00 | -0.00 |
| TRANS | last | 40 | 150 | 0% | 0% | +0.00 | -0.00 |
| TRANS | last | 44 | 150 | 0% | 0% | +0.01 | -0.00 |
| TRANS | last | 48 | 150 | 0% | 0% | +0.01 | -0.00 |
| TRANS | last | 52 | 150 | 0% | 0% | +0.09 | -0.00 |
| TRANS | last | 56 | 150 | 0% | 0% | +0.12 | -0.00 |
| TRANS | last | 60 | 150 | 0% | 0% | +0.17 | -0.00 |
