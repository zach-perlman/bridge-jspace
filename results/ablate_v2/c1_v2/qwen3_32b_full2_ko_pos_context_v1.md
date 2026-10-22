# C1 on tasks_v2 / qwen3_32b_full2_ko_pos_context_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 98 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 98 [96-100] (n=123) | 89 [81-95] (n=61) | 93 [88-98] (n=123) | 98 [95-100] (n=61) | 98 [95-100] (n=108) | 92 [85-96] (n=108) |
| L12-20 | paper10_rot | 99 [97-100] (n=123) | 93 [86-100] (n=61) | 94 [89-98] (n=123) | 97 [91-100] (n=61) | 100 [100-100] (n=108) | 93 [87-97] (n=108) |
| L44-52 | paper10 | 99 [97-100] (n=123) | 98 [95-100] (n=61) | 93 [87-98] (n=123) | 95 [88-100] (n=61) | 99 [97-100] (n=108) | 94 [86-98] (n=108) |
| L44-52 | paper10_rot | 99 [97-100] (n=123) | 97 [92-100] (n=61) | 96 [91-99] (n=123) | 95 [89-100] (n=61) | 99 [97-100] (n=108) | 97 [93-100] (n=108) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 99 [95-100] (n=67) | 82 [70-94] (n=33) | 91 [84-97] (n=67) | 97 [90-100] (n=33) | 96 [89-100] (n=49) | 90 [79-98] (n=49) |
| L12-20 | paper10_rot | 100 [100-100] (n=67) | 97 [89-100] (n=33) | 90 [80-96] (n=67) | 94 [85-100] (n=33) | 100 [100-100] (n=49) | 92 [84-98] (n=49) |
| L44-52 | paper10 | 100 [100-100] (n=67) | 97 [92-100] (n=33) | 90 [80-97] (n=67) | 97 [89-100] (n=33) | 98 [93-100] (n=49) | 94 [86-100] (n=49) |
| L44-52 | paper10_rot | 100 [100-100] (n=67) | 97 [89-100] (n=33) | 94 [87-99] (n=67) | 91 [79-100] (n=33) | 100 [100-100] (n=49) | 98 [93-100] (n=49) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 96 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 98 [94-100] (n=56) | 96 [90-100] (n=28) | 96 [88-100] (n=56) | 100 [100-100] (n=28) | 100 [100-100] (n=59) | 93 [85-98] (n=59) |
| L12-20 | paper10_rot | 98 [94-100] (n=56) | 89 [73-100] (n=28) | 100 [100-100] (n=56) | 100 [100-100] (n=28) | 100 [100-100] (n=59) | 93 [86-98] (n=59) |
| L44-52 | paper10 | 98 [94-100] (n=56) | 100 [100-100] (n=28) | 98 [94-100] (n=56) | 93 [81-100] (n=28) | 100 [100-100] (n=59) | 93 [84-100] (n=59) |
| L44-52 | paper10_rot | 98 [94-100] (n=56) | 96 [90-100] (n=28) | 98 [94-100] (n=56) | 100 [100-100] (n=28) | 98 [94-100] (n=59) | 97 [91-100] (n=59) |


## Margin-matched gap under paper10 at L44-52 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 10.75, M->P 7.00, P->M 7.38, M->M 7.62. Loss (points) by quartile of that margin (cuts 6.38, 8.50, 10.38), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 33 (n=3) | 0 (n=17) | 0 (n=30) | 0 (n=73) |
| M->P | 0 (n=30) | 0 (n=11) | 0 (n=10) | 0 (n=10) |
| P->M | 18 (n=39) | 2 (n=50) | 0 (n=29) | 0 (n=5) |
| M->M | 12 (n=24) | 0 (n=18) | 0 (n=18) | 0 (n=1) |
| prompt-final, pooled | 3 (n=33) | 0 (n=28) | 0 (n=40) | 0 (n=83) |
| memory-final, pooled | 16 (n=63) | 1 (n=68) | 0 (n=47) | 0 (n=6) |

Memory-final minus prompt-final, items pooled per group: raw 5; reweighted to the prompt-final margins 3, to the memory-final margins 5; matched within 0.25-logit margin bins 3 [0-6] (162 of 184 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L44-52: losses P->P 1, M->P 0, P->M 7, M->M 5, C->P 1, C->M 6; memory-final minus prompt-final 5 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): holds. Output from commit 50be071.
