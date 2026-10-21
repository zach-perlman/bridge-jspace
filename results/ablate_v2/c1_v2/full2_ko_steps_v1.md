# C1 on tasks_v2 / full2_ko_steps_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - | - | - |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - | - | - |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - | - | - |

## step1 alone (all formats)

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 92 | 100 | 92 | 99 | 99 |
| L32-40 | paper10 | 95 | 85 | 95 | 86 | 94 | 94 |
| L32-40 | paper10_rot | 99 | 94 | 99 | 94 | 99 | 99 |

## step2 alone (all formats)

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 99 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 | 100 | 57 | 55 | 99 | 63 |
| L32-40 | paper10_rot | 100 | 100 | 99 | 100 | 100 | 98 |

Rule at L32-40: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit ec642c2.
