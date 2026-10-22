# C1 on tasks_v2 / qwen3_32b_full2_ko_pos_question_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 98 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 99 [97-100] (n=123) | 89 [81-96] (n=61) | 97 [93-99] (n=123) | 95 [88-100] (n=61) | 97 [93-100] (n=108) | 94 [90-98] (n=108) |
| L12-20 | paper10_rot | 99 [97-100] (n=123) | 89 [81-96] (n=61) | 97 [93-99] (n=123) | 98 [95-100] (n=61) | 99 [97-100] (n=108) | 98 [95-100] (n=108) |
| L44-52 | paper10 | 98 [96-100] (n=123) | 97 [92-100] (n=61) | 90 [84-95] (n=123) | 85 [73-94] (n=61) | 97 [94-100] (n=108) | 83 [74-91] (n=108) |
| L44-52 | paper10_rot | 99 [97-100] (n=123) | 100 [100-100] (n=61) | 98 [95-100] (n=123) | 100 [100-100] (n=61) | 98 [95-100] (n=108) | 93 [84-98] (n=108) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 100 [100-100] (n=67) | 94 [86-100] (n=33) | 94 [87-99] (n=67) | 100 [100-100] (n=33) | 100 [100-100] (n=49) | 98 [93-100] (n=49) |
| L12-20 | paper10_rot | 100 [100-100] (n=67) | 91 [83-100] (n=33) | 97 [92-100] (n=67) | 97 [89-100] (n=33) | 100 [100-100] (n=49) | 96 [89-100] (n=49) |
| L44-52 | paper10 | 99 [94-100] (n=67) | 94 [86-100] (n=33) | 88 [78-95] (n=67) | 79 [61-93] (n=33) | 96 [92-100] (n=49) | 86 [73-94] (n=49) |
| L44-52 | paper10_rot | 100 [100-100] (n=67) | 100 [100-100] (n=33) | 97 [92-100] (n=67) | 100 [100-100] (n=33) | 98 [93-100] (n=49) | 90 [77-98] (n=49) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 96 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 98 [93-100] (n=56) | 82 [69-96] (n=28) | 100 [100-100] (n=56) | 89 [76-100] (n=28) | 95 [86-100] (n=59) | 92 [84-98] (n=59) |
| L12-20 | paper10_rot | 98 [94-100] (n=56) | 86 [68-100] (n=28) | 96 [91-100] (n=56) | 100 [100-100] (n=28) | 98 [94-100] (n=59) | 100 [100-100] (n=59) |
| L44-52 | paper10 | 98 [94-100] (n=56) | 100 [100-100] (n=28) | 93 [85-98] (n=56) | 93 [81-100] (n=28) | 98 [94-100] (n=59) | 81 [70-91] (n=59) |
| L44-52 | paper10_rot | 98 [94-100] (n=56) | 100 [100-100] (n=28) | 98 [94-100] (n=56) | 100 [100-100] (n=28) | 98 [94-100] (n=59) | 95 [88-100] (n=59) |


## Margin-matched gap under paper10 at L44-52 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 10.75, M->P 7.00, P->M 7.38, M->M 7.62. Loss (points) by quartile of that margin (cuts 6.38, 8.50, 10.38), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 67 (n=3) | 0 (n=17) | 0 (n=30) | 0 (n=73) |
| M->P | 3 (n=30) | 0 (n=11) | 0 (n=10) | 0 (n=10) |
| P->M | 26 (n=39) | 4 (n=50) | 0 (n=29) | 0 (n=5) |
| M->M | 33 (n=24) | 6 (n=18) | 0 (n=18) | 0 (n=1) |
| prompt-final, pooled | 9 (n=33) | 0 (n=28) | 0 (n=40) | 0 (n=83) |
| memory-final, pooled | 29 (n=63) | 4 (n=68) | 0 (n=47) | 0 (n=6) |

Memory-final minus prompt-final, items pooled per group: raw 10; reweighted to the prompt-final margins 4, to the memory-final margins 8; matched within 0.25-logit margin bins 6 [0-10] (162 of 184 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L44-52: losses P->P 2, M->P 2, P->M 10, M->M 15, C->P 3, C->M 17; memory-final minus prompt-final 11 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 50be071.
