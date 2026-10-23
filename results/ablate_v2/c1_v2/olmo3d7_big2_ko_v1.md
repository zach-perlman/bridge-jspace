# C1 on tasks_v2 / olmo3d7_big2_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 99 | 100 | 100 |
| L10-14 | paper10 | 90 [85-93] (n=222) | 91 [85-96] (n=81) | 89 [83-93] (n=222) | 86 [75-95] (n=81) |
| L10-14 | paper10_rot | 95 [91-97] (n=222) | 89 [80-95] (n=81) | 95 [90-98] (n=222) | 93 [85-98] (n=81) |
| L12-16 | paper10 | 93 [89-96] (n=222) | 91 [84-97] (n=81) | 90 [85-93] (n=222) | 86 [74-95] (n=81) |
| L12-16 | paper10_rot | 93 [89-96] (n=222) | 96 [91-100] (n=81) | 94 [89-97] (n=222) | 91 [82-97] (n=81) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L10-14 | paper10 | 91 [83-96] (n=116) | 94 [86-100] (n=35) | 91 [84-97] (n=116) | 94 [84-100] (n=35) |
| L10-14 | paper10_rot | 95 [90-99] (n=116) | 89 [75-97] (n=35) | 97 [94-100] (n=116) | 97 [90-100] (n=35) |
| L12-16 | paper10 | 93 [89-96] (n=116) | 97 [90-100] (n=35) | 91 [84-97] (n=116) | 94 [84-100] (n=35) |
| L12-16 | paper10_rot | 92 [86-97] (n=116) | 97 [90-100] (n=35) | 97 [94-100] (n=116) | 94 [86-100] (n=35) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 98 | 98 | 100 | 100 |
| L10-14 | paper10 | 89 [83-93] (n=106) | 89 [80-97] (n=46) | 87 [80-93] (n=106) | 80 [63-93] (n=46) |
| L10-14 | paper10_rot | 94 [90-98] (n=106) | 89 [80-97] (n=46) | 92 [84-97] (n=106) | 89 [76-98] (n=46) |
| L12-16 | paper10 | 92 [87-97] (n=106) | 87 [79-95] (n=46) | 89 [83-94] (n=106) | 80 [62-93] (n=46) |
| L12-16 | paper10_rot | 93 [89-97] (n=106) | 96 [90-100] (n=46) | 90 [83-95] (n=106) | 89 [76-98] (n=46) |


## Margin-matched gap under paper10 at L10-14 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.38, M->P 5.00, P->M 7.97, M->M 7.81. Loss (points) by quartile of that margin (cuts 3.38, 6.88, 10.06), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 26 (n=61) | 8 (n=60) | 0 (n=55) | 0 (n=46) |
| M->P | 19 (n=31) | 0 (n=22) | 0 (n=16) | 0 (n=12) |
| P->M | 41 (n=44) | 12 (n=49) | 0 (n=59) | 0 (n=70) |
| M->M | 43 (n=23) | 7 (n=14) | 0 (n=23) | 0 (n=21) |
| prompt-final, pooled | 24 (n=92) | 6 (n=82) | 0 (n=71) | 0 (n=58) |
| memory-final, pooled | 42 (n=67) | 11 (n=63) | 0 (n=82) | 0 (n=91) |

Memory-final minus prompt-final, items pooled per group: raw 3; reweighted to the prompt-final margins 7, to the memory-final margins 5; matched within 0.25-logit margin bins 5 [-0-9] (302 of 303 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L10-14: losses P->P 9, M->P 7, P->M 11, M->M 14; memory-final minus prompt-final 4 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit e62ce40.
