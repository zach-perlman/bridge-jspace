# C1 on tasks_v2 / muse30_full2_ko_steps_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - | - | - |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - | - | - |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - | - | - |

## step1 alone (all formats)

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 100 | 94 | 100 | 94 | 99 | 99 |
| L36-42 | paper10_rot | 99 | 100 | 99 | 100 | 99 | 99 |

## step2 alone (all formats)

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 100 | 100 | 94 | 91 | 100 | 87 |
| L36-42 | paper10_rot | 100 | 100 | 98 | 99 | 100 | 100 |


Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L36-42: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit 50be071.
