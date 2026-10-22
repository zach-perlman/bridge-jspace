# C1 on tasks_v2 / gemma4itf_full2_ko_v1 WITHOUT guessable items (robustness split) (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L11-19 | paper10 | 4 [1-8] (n=141) | 3 [0-7] (n=87) | 4 [0-10] (n=141) | 8 [1-15] (n=85) | 6 [2-12] (n=124) | 6 [1-12] (n=118) |
| L11-19 | paper10_rot | 3 [1-6] (n=141) | 10 [4-17] (n=87) | 6 [1-13] (n=141) | 4 [0-8] (n=85) | 7 [3-12] (n=124) | 6 [2-11] (n=118) |
| L19-27 | paper10 | 6 [3-10] (n=141) | 8 [3-14] (n=87) | 10 [4-16] (n=141) | 8 [3-14] (n=85) | 5 [1-9] (n=124) | 8 [3-14] (n=118) |
| L19-27 | paper10_rot | 30 [23-38] (n=141) | 22 [13-30] (n=87) | 26 [16-35] (n=141) | 48 [34-62] (n=85) | 31 [24-39] (n=124) | 42 [32-54] (n=118) |
| L48-56 | paper10 | 7 [2-13] (n=141) | 7 [2-13] (n=87) | 10 [4-17] (n=141) | 7 [2-12] (n=85) | 9 [4-14] (n=124) | 12 [5-20] (n=118) |
| L48-56 | paper10_rot | 100 [100-100] (n=141) | 100 [100-100] (n=87) | 100 [100-100] (n=141) | 100 [100-100] (n=85) | 99 [97-100] (n=124) | 100 [100-100] (n=118) |
| L0-58 | paper10 | 1 [0-2] (n=141) | 0 [0-0] (n=87) | 0 [0-0] (n=141) | 0 [0-0] (n=85) | 0 [0-0] (n=124) | 0 [0-0] (n=118) |
| L0-58 | paper10_rot | 4 [1-7] (n=141) | 2 [0-6] (n=87) | 4 [0-8] (n=141) | 4 [0-8] (n=85) | 1 [0-3] (n=124) | 3 [1-7] (n=118) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L11-19 | paper10 | 4 [0-10] (n=68) | 2 [0-7] (n=45) | 1 [0-5] (n=68) | 5 [0-12] (n=42) | 8 [2-16] (n=49) | 4 [0-10] (n=49) |
| L11-19 | paper10_rot | 4 [0-11] (n=68) | 13 [5-23] (n=45) | 6 [1-12] (n=68) | 5 [0-11] (n=42) | 12 [4-20] (n=49) | 6 [0-14] (n=49) |
| L19-27 | paper10 | 9 [3-16] (n=68) | 4 [0-10] (n=45) | 15 [6-24] (n=68) | 12 [3-23] (n=42) | 4 [0-11] (n=49) | 12 [4-21] (n=49) |
| L19-27 | paper10_rot | 35 [27-45] (n=68) | 11 [2-23] (n=45) | 24 [14-34] (n=68) | 52 [35-74] (n=42) | 33 [21-45] (n=49) | 39 [24-53] (n=49) |
| L48-56 | paper10 | 1 [0-5] (n=68) | 2 [0-8] (n=45) | 9 [0-21] (n=68) | 10 [2-19] (n=42) | 6 [0-14] (n=49) | 18 [8-30] (n=49) |
| L48-56 | paper10_rot | 100 [100-100] (n=68) | 100 [100-100] (n=45) | 100 [100-100] (n=68) | 100 [100-100] (n=42) | 100 [100-100] (n=49) | 100 [100-100] (n=49) |
| L0-58 | paper10 | 0 [0-0] (n=68) | 0 [0-0] (n=45) | 0 [0-0] (n=68) | 0 [0-0] (n=42) | 0 [0-0] (n=49) | 0 [0-0] (n=49) |
| L0-58 | paper10_rot | 3 [0-8] (n=68) | 2 [0-7] (n=45) | 3 [0-7] (n=68) | 2 [0-8] (n=42) | 2 [0-6] (n=49) | 2 [0-7] (n=49) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L11-19 | paper10 | 4 [0-9] (n=73) | 5 [0-11] (n=42) | 7 [0-16] (n=73) | 12 [0-28] (n=43) | 5 [0-13] (n=75) | 7 [0-17] (n=69) |
| L11-19 | paper10_rot | 1 [0-4] (n=73) | 7 [0-16] (n=42) | 7 [0-15] (n=73) | 2 [0-7] (n=43) | 4 [0-8] (n=75) | 6 [1-12] (n=69) |
| L19-27 | paper10 | 4 [0-8] (n=73) | 12 [3-22] (n=42) | 5 [0-13] (n=73) | 5 [0-13] (n=43) | 5 [0-11] (n=75) | 4 [0-10] (n=69) |
| L19-27 | paper10_rot | 26 [13-38] (n=73) | 33 [22-44] (n=42) | 27 [16-41] (n=73) | 44 [28-59] (n=43) | 31 [19-41] (n=75) | 45 [33-57] (n=69) |
| L48-56 | paper10 | 12 [3-22] (n=73) | 12 [3-22] (n=42) | 11 [5-18] (n=73) | 5 [0-12] (n=43) | 11 [4-18] (n=75) | 7 [1-15] (n=69) |
| L48-56 | paper10_rot | 100 [100-100] (n=73) | 100 [100-100] (n=42) | 100 [100-100] (n=73) | 100 [100-100] (n=43) | 99 [96-100] (n=75) | 100 [100-100] (n=69) |
| L0-58 | paper10 | 1 [0-5] (n=73) | 0 [0-0] (n=42) | 0 [0-0] (n=73) | 0 [0-0] (n=43) | 0 [0-0] (n=75) | 0 [0-0] (n=69) |
| L0-58 | paper10_rot | 4 [0-9] (n=73) | 2 [0-8] (n=42) | 4 [0-9] (n=73) | 5 [0-12] (n=43) | 0 [0-0] (n=75) | 4 [0-9] (n=69) |


## Margin-matched gap under paper10 at L48-56 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 16.50, M->P 15.38, P->M 14.44, M->M 14.69. Loss (points) by quartile of that margin (cuts 13.75, 15.50, 16.50), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 100 (n=4) | 96 (n=26) | 93 (n=45) | 91 (n=66) |
| M->P | 91 (n=23) | 92 (n=24) | 92 (n=26) | 100 (n=14) |
| P->M | 93 (n=55) | 76 (n=41) | 100 (n=30) | 100 (n=15) |
| M->M | 85 (n=33) | 96 (n=23) | 100 (n=16) | 100 (n=13) |
| prompt-final, pooled | 93 (n=27) | 94 (n=50) | 93 (n=71) | 92 (n=80) |
| memory-final, pooled | 90 (n=88) | 83 (n=64) | 100 (n=46) | 100 (n=28) |

Memory-final minus prompt-final, items pooled per group: raw -2; reweighted to the prompt-final margins 2, to the memory-final margins -2; matched within 0.25-logit margin bins -3 [-9-2] (186 of 226 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L48-56: losses P->P 93, M->P 93, P->M 90, M->M 93, C->P 91, C->M 88; memory-final minus prompt-final -1 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 1249d90.
