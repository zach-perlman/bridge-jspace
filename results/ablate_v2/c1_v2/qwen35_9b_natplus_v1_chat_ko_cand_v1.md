# C1 on tasks_v2 / qwen35_9b_natplus_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 91 [88-94] (n=301) | 89 [85-93] (n=257) | 51 [44-58] (n=301) | 53 [44-61] (n=257) |
| L12-16 | paper10_rot | 91 [88-94] (n=301) | 91 [88-94] (n=257) | 96 [93-98] (n=301) | 98 [97-100] (n=257) |
| L12-16 | unembed10 | 94 [91-96] (n=301) | 95 [92-97] (n=257) | 99 [98-100] (n=301) | 100 [100-100] (n=257) |
| L12-16 | unembed10_rot | 95 [92-97] (n=301) | 97 [95-99] (n=257) | 96 [94-98] (n=301) | 100 [99-100] (n=257) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 91 [88-94] (n=301) | 89 [85-93] (n=257) | 51 [44-58] (n=301) | 53 [44-61] (n=257) |
| L12-16 | paper10_rot | 91 [88-94] (n=301) | 91 [88-94] (n=257) | 96 [93-98] (n=301) | 98 [97-100] (n=257) |
| L12-16 | unembed10 | 94 [91-96] (n=301) | 95 [92-97] (n=257) | 99 [98-100] (n=301) | 100 [100-100] (n=257) |
| L12-16 | unembed10_rot | 95 [92-97] (n=301) | 97 [95-99] (n=257) | 96 [94-98] (n=301) | 100 [99-100] (n=257) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |
| L12-16 | unembed10 | - | - | - | - |
| L12-16 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.00, M->P 2.75, P->M 3.25, M->M 5.12. Loss (points) by quartile of that margin (cuts 1.50, 3.25, 5.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 18 (n=127) | 1 (n=75) | 0 (n=57) | 5 (n=42) |
| M->P | 26 (n=81) | 3 (n=71) | 3 (n=68) | 3 (n=37) |
| P->M | 64 (n=66) | 46 (n=90) | 40 (n=88) | 47 (n=57) |
| M->M | 67 (n=18) | 65 (n=40) | 45 (n=76) | 40 (n=123) |
| prompt-final, pooled | 21 (n=208) | 2 (n=146) | 2 (n=125) | 4 (n=79) |
| memory-final, pooled | 64 (n=84) | 52 (n=130) | 42 (n=164) | 42 (n=180) |

Memory-final minus prompt-final, items pooled per group: raw 38; reweighted to the prompt-final margins 44, to the memory-final margins 42; matched within 0.25-logit margin bins 42 [37-47] (551 of 558 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.00, M->P 2.75, P->M 3.25, M->M 5.12. Loss (points) by quartile of that margin (cuts 1.50, 3.25, 5.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 14 (n=127) | 0 (n=75) | 0 (n=57) | 0 (n=42) |
| M->P | 16 (n=81) | 0 (n=71) | 0 (n=68) | 0 (n=37) |
| P->M | 2 (n=66) | 0 (n=90) | 0 (n=88) | 0 (n=57) |
| M->M | 0 (n=18) | 0 (n=40) | 0 (n=76) | 0 (n=123) |
| prompt-final, pooled | 15 (n=208) | 0 (n=146) | 0 (n=125) | 0 (n=79) |
| memory-final, pooled | 1 (n=84) | 0 (n=130) | 0 (n=164) | 0 (n=180) |

Memory-final minus prompt-final, items pooled per group: raw -5; reweighted to the prompt-final margins -5, to the memory-final margins -2; matched within 0.25-logit margin bins -2 [-4--1] (551 of 558 memory-final items have a same-bin partner) points.

Rule at L12-16: losses P->P 9, M->P 10, P->M 48, M->M 47; memory-final minus prompt-final 38 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 466b6e0.
