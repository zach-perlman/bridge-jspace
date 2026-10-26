# C1 on tasks_v2 / natplus_v1_chat_ko_cand2_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 98 [96-99] (n=423) | 90 [87-93] (n=413) | 42 [36-47] (n=423) | 42 [35-49] (n=413) |
| L32-40 | paper10_rot | 97 [95-98] (n=423) | 98 [96-100] (n=413) | 98 [96-99] (n=423) | 99 [98-100] (n=413) |
| L32-40 | unembed10 | 99 [98-100] (n=423) | 99 [98-100] (n=413) | 99 [97-100] (n=423) | 99 [98-100] (n=413) |
| L32-40 | unembed10_rot | 99 [98-100] (n=423) | 99 [98-100] (n=413) | 99 [98-100] (n=423) | 98 [97-100] (n=413) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 98 [96-99] (n=423) | 90 [87-93] (n=413) | 42 [36-47] (n=423) | 42 [35-49] (n=413) |
| L32-40 | paper10_rot | 97 [95-98] (n=423) | 98 [96-100] (n=413) | 98 [96-99] (n=423) | 99 [98-100] (n=413) |
| L32-40 | unembed10 | 99 [98-100] (n=423) | 99 [98-100] (n=413) | 99 [97-100] (n=423) | 99 [98-100] (n=413) |
| L32-40 | unembed10_rot | 99 [98-100] (n=423) | 99 [98-100] (n=413) | 99 [98-100] (n=423) | 98 [97-100] (n=413) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - |
| L32-40 | unembed10 | - | - | - | - |
| L32-40 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.25, M->P 5.62, P->M 5.25, M->M 5.38. Loss (points) by quartile of that margin (cuts 3.38, 5.62, 7.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 8 (n=99) | 0 (n=76) | 0 (n=100) | 1 (n=148) |
| M->P | 30 (n=101) | 2 (n=107) | 4 (n=96) | 4 (n=109) |
| P->M | 75 (n=122) | 57 (n=115) | 47 (n=118) | 50 (n=68) |
| M->M | 74 (n=99) | 62 (n=136) | 47 (n=107) | 42 (n=71) |
| prompt-final, pooled | 19 (n=200) | 1 (n=183) | 2 (n=196) | 2 (n=257) |
| memory-final, pooled | 75 (n=221) | 60 (n=251) | 47 (n=225) | 46 (n=139) |

Memory-final minus prompt-final, items pooled per group: raw 52; reweighted to the prompt-final margins 50, to the memory-final margins 52; matched within 0.25-logit margin bins 49 [45-53] (821 of 836 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.25, M->P 5.62, P->M 5.25, M->M 5.38. Loss (points) by quartile of that margin (cuts 3.38, 5.62, 7.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 3 (n=99) | 0 (n=76) | 0 (n=100) | 0 (n=148) |
| M->P | 3 (n=101) | 0 (n=107) | 0 (n=96) | 0 (n=109) |
| P->M | 5 (n=122) | 0 (n=115) | 0 (n=118) | 0 (n=68) |
| M->M | 3 (n=99) | 0 (n=136) | 0 (n=107) | 0 (n=71) |
| prompt-final, pooled | 3 (n=200) | 0 (n=183) | 0 (n=196) | 0 (n=257) |
| memory-final, pooled | 4 (n=221) | 0 (n=251) | 0 (n=225) | 0 (n=139) |

Memory-final minus prompt-final, items pooled per group: raw 0; reweighted to the prompt-final margins 0, to the memory-final margins 0; matched within 0.25-logit margin bins -1 [-3-1] (821 of 836 memory-final items have a same-bin partner) points.

Rule at L32-40: losses P->P 2, M->P 10, P->M 58, M->M 57; memory-final minus prompt-final 52 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit 55e0f9a.
