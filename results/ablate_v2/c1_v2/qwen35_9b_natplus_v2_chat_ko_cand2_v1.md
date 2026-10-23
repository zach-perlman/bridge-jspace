# C1 on tasks_v2 / qwen35_9b_natplus_v2_chat_ko_cand2_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 92 [88-94] (n=308) | 88 [84-91] (n=299) | 46 [38-53] (n=308) | 56 [48-64] (n=299) |
| L12-16 | paper10_rot | 90 [86-93] (n=308) | 95 [93-98] (n=299) | 97 [95-99] (n=308) | 97 [95-99] (n=299) |
| L12-16 | unembed10 | 94 [91-96] (n=308) | 95 [92-97] (n=299) | 99 [98-100] (n=308) | 99 [98-100] (n=299) |
| L12-16 | unembed10_rot | 95 [93-97] (n=308) | 95 [92-97] (n=299) | 98 [96-99] (n=308) | 98 [97-100] (n=299) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 92 [88-94] (n=308) | 88 [84-91] (n=299) | 46 [38-53] (n=308) | 56 [48-64] (n=299) |
| L12-16 | paper10_rot | 90 [86-93] (n=308) | 95 [93-98] (n=299) | 97 [95-99] (n=308) | 97 [95-99] (n=299) |
| L12-16 | unembed10 | 94 [91-96] (n=308) | 95 [92-97] (n=299) | 99 [98-100] (n=308) | 99 [98-100] (n=299) |
| L12-16 | unembed10_rot | 95 [93-97] (n=308) | 95 [92-97] (n=299) | 98 [96-99] (n=308) | 98 [97-100] (n=299) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |
| L12-16 | unembed10 | - | - | - | - |
| L12-16 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.62, M->P 2.75, P->M 3.25, M->M 4.88. Loss (points) by quartile of that margin (cuts 1.62, 3.38, 5.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 15 (n=121) | 7 (n=71) | 3 (n=67) | 0 (n=49) |
| M->P | 29 (n=94) | 8 (n=84) | 2 (n=65) | 2 (n=56) |
| P->M | 71 (n=65) | 49 (n=100) | 57 (n=84) | 41 (n=59) |
| M->M | 66 (n=35) | 64 (n=47) | 41 (n=82) | 33 (n=135) |
| prompt-final, pooled | 21 (n=215) | 8 (n=155) | 2 (n=132) | 1 (n=105) |
| memory-final, pooled | 69 (n=100) | 54 (n=147) | 49 (n=166) | 36 (n=194) |

Memory-final minus prompt-final, items pooled per group: raw 39; reweighted to the prompt-final margins 45, to the memory-final margins 43; matched within 0.25-logit margin bins 43 [39-48] (596 of 607 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.62, M->P 2.75, P->M 3.25, M->M 4.88. Loss (points) by quartile of that margin (cuts 1.62, 3.38, 5.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 15 (n=121) | 0 (n=71) | 0 (n=67) | 0 (n=49) |
| M->P | 16 (n=94) | 0 (n=84) | 0 (n=65) | 0 (n=56) |
| P->M | 5 (n=65) | 0 (n=100) | 0 (n=84) | 0 (n=59) |
| M->M | 6 (n=35) | 0 (n=47) | 0 (n=82) | 0 (n=135) |
| prompt-final, pooled | 15 (n=215) | 0 (n=155) | 0 (n=132) | 0 (n=105) |
| memory-final, pooled | 5 (n=100) | 0 (n=147) | 0 (n=166) | 0 (n=194) |

Memory-final minus prompt-final, items pooled per group: raw -5; reweighted to the prompt-final margins -4, to the memory-final margins -2; matched within 0.25-logit margin bins -2 [-3--1] (596 of 607 memory-final items have a same-bin partner) points.

Rule at L12-16: losses P->P 8, M->P 12, P->M 54, M->M 44; memory-final minus prompt-final 39 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 12bdc15.
