# C1 on tasks_v2 / olmo3d7_full2_ko_v1 WITHOUT guessable items (robustness split) (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 95 | 100 | 100 | 100 | 100 |
| L6-10 | paper10 | 85 [76-94] (n=53) | 85 [74-95] (n=20) | 94 [86-100] (n=52) | 92 [70-100] (n=12) | 90 [81-98] (n=41) | 89 [81-97] (n=35) |
| L6-10 | paper10_rot | 94 [85-100] (n=53) | 95 [80-100] (n=20) | 96 [88-100] (n=52) | 100 [100-100] (n=12) | 100 [100-100] (n=41) | 97 [91-100] (n=35) |
| L10-14 | paper10 | 91 [78-100] (n=53) | 80 [67-100] (n=20) | 90 [83-98] (n=52) | 100 [100-100] (n=12) | 95 [85-100] (n=41) | 91 [83-100] (n=35) |
| L10-14 | paper10_rot | 89 [78-97] (n=53) | 95 [80-100] (n=20) | 100 [100-100] (n=52) | 100 [100-100] (n=12) | 95 [88-100] (n=41) | 89 [76-100] (n=35) |
| L0-30 | paper10 | 70 [53-81] (n=53) | 65 [48-88] (n=20) | 81 [67-91] (n=52) | 67 [20-93] (n=12) | 78 [66-90] (n=41) | 57 [38-75] (n=35) |
| L0-30 | paper10_rot | 74 [63-84] (n=53) | 90 [79-100] (n=20) | 92 [85-98] (n=52) | 83 [55-100] (n=12) | 93 [88-100] (n=41) | 80 [65-96] (n=35) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L6-10 | paper10 | 90 [82-100] (n=30) | 73 [50-100] (n=11) | 93 [81-100] (n=29) | 88 [40-100] (n=8) | 79 [52-100] (n=14) | 82 [67-100] (n=11) |
| L6-10 | paper10_rot | 100 [100-100] (n=30) | 91 [62-100] (n=11) | 97 [88-100] (n=29) | 100 [100-100] (n=8) | 100 [100-100] (n=14) | 100 [100-100] (n=11) |
| L10-14 | paper10 | 93 [80-100] (n=30) | 73 [50-100] (n=11) | 93 [84-100] (n=29) | 100 [100-100] (n=8) | 100 [100-100] (n=14) | 100 [100-100] (n=11) |
| L10-14 | paper10_rot | 93 [83-100] (n=30) | 91 [62-100] (n=11) | 100 [100-100] (n=29) | 100 [100-100] (n=8) | 93 [81-100] (n=14) | 73 [40-100] (n=11) |
| L0-30 | paper10 | 73 [59-87] (n=30) | 64 [25-88] (n=11) | 83 [64-97] (n=29) | 75 [20-100] (n=8) | 64 [38-89] (n=14) | 64 [38-89] (n=11) |
| L0-30 | paper10_rot | 80 [67-92] (n=30) | 91 [82-100] (n=11) | 97 [88-100] (n=29) | 75 [20-100] (n=8) | 79 [65-93] (n=14) | 55 [31-88] (n=11) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 89 | 100 | 100 | 100 | 100 |
| L6-10 | paper10 | 78 [56-95] (n=23) | 100 [100-100] (n=9) | 96 [82-100] (n=23) | 100 [100-100] (n=4) | 96 [87-100] (n=27) | 92 [81-100] (n=24) |
| L6-10 | paper10_rot | 87 [62-100] (n=23) | 100 [100-100] (n=9) | 96 [82-100] (n=23) | 100 [100-100] (n=4) | 100 [100-100] (n=27) | 96 [88-100] (n=24) |
| L10-14 | paper10 | 87 [62-100] (n=23) | 89 [73-100] (n=9) | 87 [71-100] (n=23) | 100 [100-100] (n=4) | 93 [78-100] (n=27) | 88 [76-100] (n=24) |
| L10-14 | paper10_rot | 83 [59-98] (n=23) | 100 [100-100] (n=9) | 100 [100-100] (n=23) | 100 [100-100] (n=4) | 96 [85-100] (n=27) | 96 [88-100] (n=24) |
| L0-30 | paper10 | 65 [33-86] (n=23) | 67 [33-100] (n=9) | 78 [56-92] (n=23) | 50 [0-100] (n=4) | 85 [64-100] (n=27) | 54 [33-75] (n=24) |
| L0-30 | paper10_rot | 65 [47-82] (n=23) | 89 [73-100] (n=9) | 87 [72-100] (n=23) | 100 [100-100] (n=4) | 100 [100-100] (n=27) | 92 [83-100] (n=24) |


## Margin-matched gap under paper10 at L10-14 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.38, M->P 5.75, P->M 9.72, M->M 7.84. Loss (points) by quartile of that margin (cuts 4.62, 7.56, 10.38), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 31 (n=16) | 0 (n=15) | 0 (n=12) | 0 (n=10) |
| M->P | 33 (n=9) | 0 (n=3) | 0 (n=4) | 0 (n=4) |
| P->M | 57 (n=7) | 8 (n=13) | 0 (n=12) | 0 (n=20) |
| M->M | 0 (n=3) | 0 (n=3) | 0 (n=6) | - (n=0) |
| prompt-final, pooled | 32 (n=25) | 0 (n=18) | 0 (n=16) | 0 (n=14) |
| memory-final, pooled | 40 (n=10) | 6 (n=16) | 0 (n=18) | 0 (n=20) |

Memory-final minus prompt-final, items pooled per group: raw -3; reweighted to the prompt-final margins 4, to the memory-final margins 3; matched within 0.25-logit margin bins 7 [-4-20] (38 of 64 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L10-14: losses P->P 9, M->P 15, P->M 10, M->M 0, C->P 5, C->M 9; memory-final minus prompt-final -7 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 2d65551.
