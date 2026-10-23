# C1 on tasks_v2 / qwen35_9b_full2_ko_pos_question_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 99 | 100 | 100 | 100 |
| L6-10 | paper10 | 96 [92-99] (n=119) | 65 [48-79] (n=43) | 79 [68-88] (n=119) | 49 [30-68] (n=43) | 90 [85-95] (n=105) | 79 [70-87] (n=105) |
| L6-10 | paper10_rot | 99 [97-100] (n=119) | 79 [64-92] (n=43) | 95 [90-98] (n=119) | 93 [85-100] (n=43) | 99 [97-100] (n=105) | 90 [85-97] (n=105) |
| L12-16 | paper10 | 99 [97-100] (n=119) | 93 [85-98] (n=43) | 92 [85-96] (n=119) | 86 [77-95] (n=43) | 100 [100-100] (n=105) | 94 [90-98] (n=105) |
| L12-16 | paper10_rot | 99 [97-100] (n=119) | 95 [89-100] (n=43) | 97 [94-99] (n=119) | 98 [93-100] (n=43) | 99 [97-100] (n=105) | 98 [95-100] (n=105) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L6-10 | paper10 | 100 [100-100] (n=65) | 73 [47-92] (n=22) | 83 [71-92] (n=65) | 55 [35-76] (n=22) | 90 [80-98] (n=51) | 76 [62-88] (n=51) |
| L6-10 | paper10_rot | 100 [100-100] (n=65) | 86 [71-100] (n=22) | 95 [87-100] (n=65) | 91 [78-100] (n=22) | 98 [94-100] (n=51) | 90 [82-98] (n=51) |
| L12-16 | paper10 | 98 [95-100] (n=65) | 95 [85-100] (n=22) | 88 [78-96] (n=65) | 82 [67-100] (n=22) | 100 [100-100] (n=51) | 94 [87-100] (n=51) |
| L12-16 | paper10_rot | 100 [100-100] (n=65) | 100 [100-100] (n=22) | 97 [92-100] (n=65) | 95 [85-100] (n=22) | 100 [100-100] (n=51) | 100 [100-100] (n=51) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 98 | 100 | 100 | 100 |
| L6-10 | paper10 | 91 [82-98] (n=54) | 57 [36-75] (n=21) | 74 [60-88] (n=54) | 43 [13-72] (n=21) | 91 [83-98] (n=54) | 81 [71-91] (n=54) |
| L6-10 | paper10_rot | 98 [93-100] (n=54) | 71 [50-91] (n=21) | 94 [88-100] (n=54) | 95 [82-100] (n=21) | 100 [100-100] (n=54) | 91 [83-97] (n=54) |
| L12-16 | paper10 | 100 [100-100] (n=54) | 90 [78-100] (n=21) | 96 [90-100] (n=54) | 90 [76-100] (n=21) | 100 [100-100] (n=54) | 94 [88-100] (n=54) |
| L12-16 | paper10_rot | 98 [93-100] (n=54) | 90 [79-100] (n=21) | 96 [92-100] (n=54) | 100 [100-100] (n=21) | 98 [94-100] (n=54) | 96 [90-100] (n=54) |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.75, M->P 2.12, P->M 2.62, M->M 2.88. Loss (points) by quartile of that margin (cuts 1.62, 2.62, 3.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 4 (n=24) | 0 (n=33) | 0 (n=37) | 0 (n=25) |
| M->P | 17 (n=18) | 0 (n=9) | 0 (n=7) | 0 (n=9) |
| P->M | 20 (n=35) | 8 (n=25) | 0 (n=31) | 0 (n=28) |
| M->M | 36 (n=11) | 12 (n=8) | 6 (n=17) | 0 (n=7) |
| prompt-final, pooled | 10 (n=42) | 0 (n=42) | 0 (n=44) | 0 (n=34) |
| memory-final, pooled | 24 (n=46) | 9 (n=33) | 2 (n=48) | 0 (n=35) |

Memory-final minus prompt-final, items pooled per group: raw 7; reweighted to the prompt-final margins 7, to the memory-final margins 7; matched within 0.25-logit margin bins 7 [0-13] (161 of 162 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 1, M->P 7, P->M 8, M->M 14, C->P 0, C->M 6; memory-final minus prompt-final 7 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 6c0760e.
