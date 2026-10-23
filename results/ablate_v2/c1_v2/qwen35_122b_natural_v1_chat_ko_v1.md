# C1 on tasks_v2 / qwen35_122b_natural_v1_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 99 | 100 | 100 |
| L39-45 | paper10 | 2 [0-4] (n=231) | 3 [1-6] (n=232) | 1 [0-2] (n=231) | 11 [7-15] (n=232) |
| L39-45 | paper10_rot | 97 [94-99] (n=231) | 97 [94-99] (n=232) | 97 [94-99] (n=231) | 99 [97-100] (n=232) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 99 | 100 | 100 |
| L39-45 | paper10 | 2 [0-4] (n=231) | 3 [1-6] (n=232) | 1 [0-2] (n=231) | 11 [7-15] (n=232) |
| L39-45 | paper10_rot | 97 [94-99] (n=231) | 97 [94-99] (n=232) | 97 [94-99] (n=231) | 99 [97-100] (n=232) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L39-45 | paper10 | - | - | - | - |
| L39-45 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L39-45 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.12, M->P 5.12, P->M 6.38, M->M 7.38. Loss (points) by quartile of that margin (cuts 4.00, 6.38, 7.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 100 (n=86) | 99 (n=73) | 97 (n=38) | 94 (n=34) |
| M->P | 96 (n=89) | 97 (n=60) | 96 (n=47) | 94 (n=36) |
| P->M | 100 (n=41) | 99 (n=77) | 100 (n=66) | 98 (n=47) |
| M->M | 100 (n=18) | 88 (n=33) | 90 (n=80) | 87 (n=101) |
| prompt-final, pooled | 98 (n=175) | 98 (n=133) | 96 (n=85) | 94 (n=70) |
| memory-final, pooled | 100 (n=59) | 95 (n=110) | 95 (n=146) | 91 (n=148) |

Memory-final minus prompt-final, items pooled per group: raw -3; reweighted to the prompt-final margins -1, to the memory-final margins -2; matched within 0.25-logit margin bins -2 [-5-1] (462 of 463 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L39-45: losses P->P 98, M->P 96, P->M 99, M->M 89; memory-final minus prompt-final -3 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 42e0e34.
