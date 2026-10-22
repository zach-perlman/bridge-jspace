# C1 on tasks_v2 / muse30_full3_ko_steps_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - | - | - |

## text formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - | - | - |

## structured formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - | - | - |

## secondary stratum (planets, three-step words), all formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->M->P |
|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - | - |

## step1 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 98 |
| L36-42 | paper10 | 99 | 100 | 98 | 98 | 94 | 82 |
| L36-42 | paper10_rot | 100 | 100 | 99 | 100 | 100 | 98 |

## step2 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 100 | 100 | 99 | 100 | 100 | 100 |
| L36-42 | paper10_rot | 100 | 100 | 99 | 100 | 100 | 100 |

## step3 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 100 | 91 | 100 | 100 | 91 | 100 |
| L36-42 | paper10_rot | 100 | 100 | 100 | 100 | 100 | 100 |


Rule at L36-42: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit 50be071.
