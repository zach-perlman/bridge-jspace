# C1 on tasks_v2 / qwen35_122b_natural_v1_chat_ko_l2430_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 99 | 100 | 100 |
| L24-30 | paper10 | 11 [7-15] (n=231) | 10 [6-15] (n=232) | 1 [0-3] (n=231) | 3 [2-6] (n=232) |
| L24-30 | paper10_rot | 95 [92-98] (n=231) | 95 [92-98] (n=232) | 98 [96-100] (n=231) | 99 [97-100] (n=232) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 99 | 100 | 100 |
| L24-30 | paper10 | 11 [7-15] (n=231) | 10 [6-15] (n=232) | 1 [0-3] (n=231) | 3 [2-6] (n=232) |
| L24-30 | paper10_rot | 95 [92-98] (n=231) | 95 [92-98] (n=232) | 98 [96-100] (n=231) | 99 [97-100] (n=232) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L24-30 | paper10 | - | - | - | - |
| L24-30 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L24-30 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.12, M->P 5.12, P->M 6.38, M->M 7.38. Loss (points) by quartile of that margin (cuts 4.00, 6.38, 7.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 91 (n=86) | 93 (n=73) | 89 (n=38) | 74 (n=34) |
| M->P | 93 (n=89) | 92 (n=60) | 81 (n=47) | 86 (n=36) |
| P->M | 98 (n=41) | 99 (n=77) | 98 (n=66) | 100 (n=47) |
| M->M | 94 (n=18) | 100 (n=33) | 98 (n=80) | 95 (n=101) |
| prompt-final, pooled | 92 (n=175) | 92 (n=133) | 85 (n=85) | 80 (n=70) |
| memory-final, pooled | 97 (n=59) | 99 (n=110) | 98 (n=146) | 97 (n=148) |

Memory-final minus prompt-final, items pooled per group: raw 9; reweighted to the prompt-final margins 9, to the memory-final margins 12; matched within 0.25-logit margin bins 11 [7-16] (462 of 463 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L24-30: losses P->P 89, M->P 89, P->M 99, M->M 97; memory-final minus prompt-final 9 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 07f486e.
