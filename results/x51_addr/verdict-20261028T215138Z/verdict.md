# 51.11: what is the address, independent of how we built it?

Batch 51 addendum 3 (jobs/c3/batch51.yaml; Q51.11, Dan: - Part 1: one per slot
- Part 2: one code
- Part 3: first vs the rest). Every number on held-out entities (test split; part 3: select and test); cluster bootstrap over bridge entities (10000, seed 0). UNVERIFIED.

As computed: scripts/x51_addr.py's docstring (repeated in the job specs).

## qwen3.5-9b

Runs: {1: 'qwen35_9b_x51_11_p1', 2: 'qwen35_9b_x51_11_p2', 3: 'qwen35_9b_x51_11_p3'}; present here: {1: 'qwen35_9b_x51_11_p1', 2: 'qwen35_9b_x51_11_p2', 3: 'qwen35_9b_x51_11_p3'}.

### Part 1: dimension vs the number of slots (qwen35_9b_x51_11_p1, L12)

**in between** (holding: none; d* not found at S = [6])

| S | status | pairs (train / select / test) | ordered pairs covered | test n (entities) | whole | U (rank S-1) | d*(S) | d* without the random bar | k blocked by random > 0.15 | d* through P |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | tested | 358 ({'train': 213, 'select': 95, 'test': 50}) | 6 / 6 | 50 (6) | 1.00 [1.00, 1.00] | 0.74 [0.63, 0.84] | 2 | 2 | - | 3 |
| 4 | tested | 306 ({'select': 59, 'train': 191, 'test': 56}) | 10 / 12 | 56 (5) | 0.98 [0.94, 1.00] | 0.75 [0.69, 0.84] | 2 | 2 | - | > 7 |
| 6 | tested | 303 ({'select': 61, 'train': 200, 'test': 42}) | 23 / 30 | 42 (6) | 1.00 [1.00, 1.00] | 0.48 [0.38, 0.63] | > 7 | - | - | > 7 |
| 8 | tested | 304 ({'train': 174, 'select': 73, 'test': 57}) | 32 / 56 | 57 (6) | 1.00 [1.00, 1.00] | 0.51 [0.38, 0.61] | 2 | 2 | - | > 7 |

Own-IIA on the test pairs by k (R; P's top k; the random R; the shuffled-target R):

| S | arm | k = 1 | k = 2 | k = 3 | k = 4 | k = 5 | k = 7 |
|---|---|---|---|---|---|---|---|
| 3 | R | 0.60 [0.46, 0.71] | 0.98 [0.94, 1.00] | 0.96 [0.89, 1.00] | 0.98 [0.94, 1.00] | 0.98 [0.92, 1.00] | 0.98 [0.94, 1.00] |
| 3 | P | 0.24 [0.11, 0.35] | 0.74 [0.64, 0.84] | 0.84 [0.79, 0.88] | 0.86 [0.79, 0.94] | 0.86 [0.79, 0.94] | 0.86 [0.79, 0.94] |
| 3 | rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 3 | shuf | 0.02 [0.00, 0.06] | 0.22 [0.16, 0.29] | 0.04 [0.00, 0.09] | 0.04 [0.00, 0.09] | 0.04 [0.00, 0.09] | 0.20 [0.10, 0.31] |
| 4 | R | 0.62 [0.51, 0.80] | 0.91 [0.79, 0.99] | 0.89 [0.77, 0.97] | 0.95 [0.87, 1.00] | 0.95 [0.87, 1.00] | 0.98 [0.94, 1.00] |
| 4 | P | 0.09 [0.02, 0.16] | 0.70 [0.63, 0.80] | 0.71 [0.63, 0.82] | 0.73 [0.66, 0.82] | 0.73 [0.66, 0.82] | 0.75 [0.69, 0.84] |
| 4 | rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 4 | shuf | 0.07 [0.04, 0.10] | 0.18 [0.09, 0.25] | 0.14 [0.06, 0.20] | 0.16 [0.08, 0.22] | 0.36 [0.28, 0.44] | 0.41 [0.26, 0.55] |
| 6 | R | 0.33 [0.23, 0.46] | 0.71 [0.59, 0.87] | 0.79 [0.69, 0.90] | 0.74 [0.62, 0.87] | 0.71 [0.61, 0.81] | 0.79 [0.63, 0.93] |
| 6 | P | 0.14 [0.08, 0.17] | 0.33 [0.21, 0.45] | 0.45 [0.33, 0.62] | 0.50 [0.38, 0.66] | 0.52 [0.42, 0.67] | 0.55 [0.43, 0.68] |
| 6 | rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 6 | shuf | 0.10 [0.04, 0.16] | 0.10 [0.02, 0.20] | 0.26 [0.17, 0.38] | 0.33 [0.22, 0.43] | 0.29 [0.16, 0.43] | 0.33 [0.22, 0.45] |
| 8 | R | 0.56 [0.37, 0.70] | 0.82 [0.70, 0.91] | 0.86 [0.70, 0.97] | 0.89 [0.76, 0.98] | 0.88 [0.72, 0.97] | 0.89 [0.76, 0.98] |
| 8 | P | 0.09 [0.02, 0.16] | 0.33 [0.15, 0.48] | 0.44 [0.31, 0.53] | 0.49 [0.33, 0.60] | 0.49 [0.36, 0.60] | 0.53 [0.43, 0.61] |
| 8 | rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 8 | shuf | 0.04 [0.00, 0.07] | 0.07 [0.02, 0.13] | 0.11 [0.05, 0.15] | 0.05 [0.00, 0.12] | 0.21 [0.14, 0.29] | 0.12 [0.09, 0.15] |

Dumbest ways (verify pack): per S the locker-sentence layout (tokens per sentence, slot starts), the ordered pairs with no position pair, the whole change's routes among eligible scenes; every pair's answer digit is asserted equal in O and S at build; d* is read on the test entities only; the random bar is per k (the rand rows above).
- S = 3: layout {'sentence_tokens': 9, 'slot_starts': [3, 12, 21], 'layouts_seen': 1}; missing ordered pairs none; routes {'position': 358, 'other': 14, 'identity': 397} (position share 0.4655); gate {'lookup': 0.9988372093023256, 'recall': 0.9232558139534883}
- S = 4: layout {'sentence_tokens': 9, 'slot_starts': [3, 12, 21, 30], 'layouts_seen': 1}; missing ordered pairs ['3-4', '4-3']; routes {'position': 306, 'identity': 473, 'other': 57} (position share 0.366); gate {'lookup': 1.0, 'recall': 0.9331140350877193}
- S = 6: layout {'sentence_tokens': 9, 'slot_starts': [3, 12, 21, 30, 39, 48], 'layouts_seen': 1}; missing ordered pairs ['3-4', '3-5', '3-6', '4-5', '4-6', '5-4', '5-6']; routes {'position': 303, 'other': 178, 'identity': 1046} (position share 0.1984); gate {'lookup': 1.0, 'recall': 0.9270334928229665}
- S = 8: layout {'sentence_tokens': 9, 'slot_starts': [3, 12, 21, 30, 39, 48, 57, 66], 'layouts_seen': 1}; missing ordered pairs ['3-4', '3-5', '3-6', '3-7', '4-3', '4-5', '4-6', '4-7', '4-8', '5-3', '5-4', '5-6', '5-7', '5-8', '6-4', '6-5', '6-7', '6-8', '7-5', '7-6', '7-8', '8-4', '8-5', '8-7']; routes {'other': 283, 'position': 304, 'identity': 1565} (position share 0.1413); gate {'lookup': 1.0, 'recall': 0.9330204778156996}

### Part 2: do three methods find the same code? (qwen35_9b_x51_11_p2, L12)

**S = 6: in between (none of the three)**

S = 6 (decisive): 600 (item, target) reads on 120 items (6 entities); bases U rank 5, P and R at k = 7 (d*(6) > 7: the working dimension is k = 7); label in between (none of the three)

| removed \ swap through | whole | U | P | R |
|---|---|---|---|---|
| none | 0.36 [0.32, 0.40] | 0.36 [0.32, 0.40] | 0.35 [0.32, 0.39] | 0.44 [0.43, 0.46] |
| U | 0.03 [0.01, 0.05] | 0.03 [0.01, 0.05] | 0.04 [0.02, 0.06] | 0.39 [0.37, 0.40] |
| P | 0.03 [0.01, 0.04] | 0.03 [0.01, 0.04] | 0.03 [0.01, 0.05] | 0.38 [0.37, 0.41] |
| R | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.01] | 0.04 [0.03, 0.06] |
| random direction (same norm) | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

reach (projected / whole): U 1.00 [0.99, 1.00]; P 0.98 [0.96, 1.00]; R 1.22 [1.08, 1.37]. Cuts (1 - removed / not): U->P 0.89 [0.84, 0.94]; U->R 0.12 [0.09, 0.16]; P->U 0.93 [0.89, 0.97]; P->R 0.14 [0.10, 0.17]; R->U 0.98 [0.96, 1.00]; R->P 0.98 [0.96, 1.00]. Self-removal left: U 0.09 [0.04, 0.15]; P 0.08 [0.04, 0.14]; R 0.10 [0.07, 0.13]. Removal alone moves the lookup off its slot: {'U': 0.1583, 'P': 0.15, 'R': 0.225}. Median swap norms {'whole': 12.8914, 'U': 12.8913, 'P': 12.8146, 'R': 10.709}. The recall moved per cell: {'none|whole': 0.1517, 'none|U': 0.1483, 'none|P': 0.14, 'none|R': 0.2383, 'U|whole': 0.0167, 'U|U': 0.0167, 'U|P': 0.0233, 'U|R': 0.1867, 'P|whole': 0.02, 'P|U': 0.02, 'P|P': 0.0167, 'P|R': 0.2017, 'R|whole': 0.0467, 'R|U': 0.0483, 'R|P': 0.0467, 'R|R': 0.0233}.

Geometry (mean cos² of the principal angles; random: max rank / d and the mean of 20 seeded pairs): U-P 0.757 (random 0.0017 / 0.0018); U-R 0.397 (random 0.0017 / 0.0018); P-R 0.308 (random 0.0017 / 0.0017)

S = 3 (beside): 240 (item, target) reads on 120 items (7 entities); bases U rank 2, P and R at k = 2 (d* = 2); label in between (none of the three)

| removed \ swap through | whole | U | P | R |
|---|---|---|---|---|
| none | 0.82 [0.76, 0.87] | 0.82 [0.76, 0.87] | 0.82 [0.76, 0.88] | 0.92 [0.90, 0.95] |
| U | 0.03 [0.02, 0.05] | 0.03 [0.02, 0.05] | 0.03 [0.02, 0.05] | 0.83 [0.79, 0.86] |
| P | 0.05 [0.03, 0.07] | 0.05 [0.03, 0.07] | 0.03 [0.02, 0.05] | 0.83 [0.79, 0.86] |
| R | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.12 [0.06, 0.17] |
| random direction (same norm) | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

reach (projected / whole): U 1.00 [1.00, 1.00]; P 1.01 [0.99, 1.02]; R 1.12 [1.06, 1.21]. Cuts (1 - removed / not): U->P 0.96 [0.94, 0.97]; U->R 0.10 [0.07, 0.14]; P->U 0.94 [0.91, 0.97]; P->R 0.10 [0.06, 0.13]; R->U 1.00 [1.00, 1.00]; R->P 1.00 [1.00, 1.00]. Self-removal left: U 0.04 [0.03, 0.06]; P 0.04 [0.03, 0.06]; R 0.14 [0.07, 0.19]. Removal alone moves the lookup off its slot: {'U': 0.0667, 'P': 0.0667, 'R': 0.25}. Median swap norms {'whole': 15.9205, 'U': 15.9206, 'P': 15.848, 'R': 12.583}. The recall moved per cell: {'none|whole': 0.3542, 'none|U': 0.35, 'none|P': 0.3542, 'none|R': 0.3833, 'U|whole': 0.0167, 'U|U': 0.0208, 'U|P': 0.0417, 'U|R': 0.3375, 'P|whole': 0.025, 'P|U': 0.025, 'P|P': 0.0333, 'P|R': 0.3292, 'R|whole': 0.0542, 'R|U': 0.0542, 'R|P': 0.0542, 'R|R': 0.05}.

Geometry (mean cos² of the principal angles; random: max rank / d and the mean of 20 seeded pairs): U-P 0.985 (random 0.0005 / 0.0004); U-R 0.670 (random 0.0005 / 0.0004); P-R 0.665 (random 0.0005 / 0.0004)

### Part 3: categories, an order or a line? (qwen35_9b_x51_11_p3, L12, S = 6)

**none of the three** at dose 2 (midpoint share from slot 1 0.06, from slot 6 0.00; full swaps at their target 0.40); at dose 4: none of the three (from 1 0.05, from 6 0.01)

Unedited O answers its own slot: {1: 1.0, 6: 1.0}. Real change size (median ||U U^T Δ||, test pairs) 7.998; median ||h_O|| 31.4. Items {'1': {'pool': 238, 'read': 128, 'eligible': 104, 'kept': 100}, '6': {'pool': 269, 'read': 120, 'eligible': 103, 'kept': 100}}.

| start | arm | dose | n | median norm | original | midpoint | far | near | another slot | not a slot |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | mid | 2 | 200 | 9.0243 | 0.03 [0.00, 0.06] | 0.06 [0.03, 0.09] | 0.42 [0.37, 0.47] | 0.00 [0.00, 0.00] | 0.43 [0.36, 0.50] | 0.06 [0.03, 0.10] |
| 1 | mid | 4 | 200 | 18.0486 | 0.00 [0.00, 0.00] | 0.05 [0.02, 0.07] | 0.38 [0.32, 0.43] | 0.01 [0.00, 0.02] | 0.54 [0.49, 0.59] | 0.03 [0.01, 0.05] |
| 1 | mid_random | 2 | 200 | 9.0243 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 1 | mid_random | 4 | 200 | 18.0486 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 1 | full | 2 | 200 | 18.0486 | 0.00 [0.00, 0.00] | 0.05 [0.02, 0.07] | 0.38 [0.32, 0.43] | 0.01 [0.00, 0.02] | 0.54 [0.49, 0.59] | 0.03 [0.01, 0.05] |
| 1 | full_random | 2 | 200 | 18.0486 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 6 | mid | 2 | 200 | 5.6728 | 0.83 [0.76, 0.90] | 0.00 [0.00, 0.00] | 0.16 [0.10, 0.23] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 6 | mid | 4 | 200 | 11.3455 | 0.57 [0.54, 0.61] | 0.01 [0.00, 0.02] | 0.41 [0.38, 0.45] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 6 | mid_random | 2 | 200 | 5.6728 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 6 | mid_random | 4 | 200 | 11.3455 | 0.99 [0.98, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 6 | full | 2 | 200 | 11.3455 | 0.57 [0.54, 0.61] | 0.01 [0.00, 0.02] | 0.41 [0.38, 0.45] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 6 | full_random | 2 | 200 | 11.3455 | 0.99 [0.98, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |

Slot means at S = 6: mean distance by |i - j| 1: 4.08, 2: 5.66, 3: 7.20, 4: 8.71, 5: 9.82 (over lag 1: 1: 1.00, 2: 1.39, 3: 1.77, 4: 2.14, 5: 2.41); spread (std / mean; a simplex 0) 0.436; corr(distance, |i - j|) 0.698; PC shares [0.619, 0.274, 0.087], PC1 per slot [-6.52, -2.18, 0.86, 2.01, 2.71, 3.11], Spearman 1.00

Slot means at S = 8: mean distance by |i - j| 1: 3.24, 2: 4.42, 3: 5.54, 4: 6.74, 5: 7.99, 6: 9.28, 7: 10.08 (over lag 1: 1: 1.00, 2: 1.36, 3: 1.71, 4: 2.08, 5: 2.46, 6: 2.86, 7: 3.11); spread (std / mean; a simplex 0) 0.515; corr(distance, |i - j|) 0.708; PC shares [0.6, 0.265, 0.099], PC1 per slot [-6.52, -3.72, -0.56, 0.9, 1.77, 2.27, 2.75, 3.11], Spearman 1.00

### Part 4: the finding's wording

Labels: part 1 in_between, part 2 in_between, part 3 none. Row -: no row of the wording table matches these labels; the wording is not fixed by the addendum

In every case the sentence no longer says "four directions"; "four" becomes a note on the first construction.

Figure: qwen3.5-9b_part1.png

Figure: qwen3.5-9b_part3.png

## muse-glimmer-30b

Runs: {1: 'muse30_x51_11_p1', 2: 'muse30_x51_11_p2', 3: 'muse30_x51_11_p3'}; present here: {1: 'muse30_x51_11_p1', 2: 'muse30_x51_11_p2', 3: 'muse30_x51_11_p3'}.

### Part 1: dimension vs the number of slots (muse30_x51_11_p1, L26)

**one dimension per slot** (holding: one_per_slot; d* not found at S = [8])

| S | status | pairs (train / select / test) | ordered pairs covered | test n (entities) | whole | U (rank S-1) | d*(S) | d* without the random bar | k blocked by random > 0.15 | d* through P |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | tested | 373 ({'train': 200, 'test': 91, 'select': 82}) | 6 / 6 | 91 (7) | 0.99 [0.97, 1.00] | 0.77 [0.63, 0.88] | 2 | 2 | - | 3 |
| 4 | tested | 347 ({'select': 72, 'train': 191, 'test': 84}) | 11 / 12 | 84 (7) | 0.99 [0.96, 1.00] | 0.74 [0.68, 0.79] | 2 | 2 | - | 5 |
| 6 | tested | 328 ({'select': 60, 'train': 192, 'test': 76}) | 28 / 30 | 76 (7) | 1.00 [1.00, 1.00] | 0.62 [0.56, 0.69] | 7 | 7 | - | > 7 |
| 8 | tested | 315 ({'train': 169, 'select': 64, 'test': 82}) | 45 / 56 | 82 (7) | 1.00 [1.00, 1.00] | 0.50 [0.39, 0.59] | > 7 | - | - | > 7 |

Own-IIA on the test pairs by k (R; P's top k; the random R; the shuffled-target R):

| S | arm | k = 1 | k = 2 | k = 3 | k = 4 | k = 5 | k = 7 |
|---|---|---|---|---|---|---|---|
| 3 | R | 0.44 [0.35, 0.54] | 0.98 [0.93, 1.00] | 0.98 [0.93, 1.00] | 0.99 [0.96, 1.00] | 0.99 [0.96, 1.00] | 0.99 [0.96, 1.00] |
| 3 | P | 0.32 [0.21, 0.43] | 0.71 [0.55, 0.86] | 0.84 [0.70, 0.94] | 0.84 [0.70, 0.94] | 0.86 [0.75, 0.94] | 0.88 [0.80, 0.95] |
| 3 | rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 3 | shuf | 0.03 [0.01, 0.06] | 0.10 [0.06, 0.16] | 0.29 [0.22, 0.36] | 0.09 [0.03, 0.16] | 0.24 [0.19, 0.32] | 0.33 [0.28, 0.41] |
| 4 | R | 0.52 [0.45, 0.61] | 0.81 [0.76, 0.88] | 0.94 [0.92, 0.97] | 0.94 [0.92, 0.97] | 0.93 [0.88, 0.96] | 0.92 [0.86, 0.96] |
| 4 | P | 0.15 [0.06, 0.25] | 0.44 [0.33, 0.55] | 0.54 [0.44, 0.64] | 0.63 [0.55, 0.72] | 0.82 [0.79, 0.85] | 0.82 [0.77, 0.87] |
| 4 | rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 4 | shuf | 0.18 [0.07, 0.30] | 0.14 [0.04, 0.25] | 0.21 [0.15, 0.27] | 0.18 [0.11, 0.25] | 0.33 [0.20, 0.49] | 0.30 [0.24, 0.39] |
| 6 | R | 0.36 [0.25, 0.46] | 0.50 [0.38, 0.65] | 0.70 [0.59, 0.82] | 0.70 [0.59, 0.81] | 0.74 [0.65, 0.83] | 0.84 [0.75, 0.93] |
| 6 | P | 0.22 [0.11, 0.34] | 0.34 [0.23, 0.45] | 0.34 [0.23, 0.45] | 0.54 [0.47, 0.61] | 0.57 [0.51, 0.63] | 0.62 [0.53, 0.72] |
| 6 | rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 6 | shuf | 0.05 [0.02, 0.08] | 0.07 [0.03, 0.11] | 0.12 [0.05, 0.19] | 0.14 [0.07, 0.23] | 0.05 [0.02, 0.07] | 0.11 [0.03, 0.20] |
| 8 | R | 0.27 [0.16, 0.34] | 0.43 [0.35, 0.47] | 0.54 [0.45, 0.60] | 0.60 [0.49, 0.70] | 0.67 [0.56, 0.73] | 0.71 [0.62, 0.78] |
| 8 | P | 0.12 [0.03, 0.21] | 0.21 [0.10, 0.29] | 0.21 [0.12, 0.28] | 0.35 [0.22, 0.46] | 0.46 [0.33, 0.55] | 0.54 [0.45, 0.60] |
| 8 | rand | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 8 | shuf | 0.09 [0.03, 0.14] | 0.09 [0.03, 0.12] | 0.13 [0.07, 0.18] | 0.12 [0.06, 0.21] | 0.18 [0.10, 0.26] | 0.16 [0.07, 0.24] |

Dumbest ways (verify pack): per S the locker-sentence layout (tokens per sentence, slot starts), the ordered pairs with no position pair, the whole change's routes among eligible scenes; every pair's answer digit is asserted equal in O and S at build; d* is read on the test entities only; the random bar is per k (the rand rows above).
- S = 3: layout {'sentence_tokens': 9, 'slot_starts': [42, 51, 60], 'layouts_seen': 1}; missing ordered pairs none; routes {'position': 373, 'other': 74, 'identity': 148} (position share 0.6269); gate {'lookup': 0.9912790697674418, 'recall': 0.9418604651162791}
- S = 4: layout {'sentence_tokens': 9, 'slot_starts': [42, 51, 60, 69], 'layouts_seen': 1}; missing ordered pairs ['3-4']; routes {'position': 347, 'other': 151, 'identity': 372} (position share 0.3989); gate {'lookup': 0.9419291338582677, 'recall': 0.9704724409448819}
- S = 6: layout {'sentence_tokens': 9, 'slot_starts': [42, 51, 60, 69, 78, 87], 'layouts_seen': 1}; missing ordered pairs ['5-6', '6-5']; routes {'position': 328, 'other': 342, 'identity': 940} (position share 0.2037); gate {'lookup': 0.9631696428571429, 'recall': 0.9754464285714286}
- S = 8: layout {'sentence_tokens': 9, 'slot_starts': [42, 51, 60, 69, 78, 87, 96, 105], 'layouts_seen': 1}; missing ordered pairs ['3-4', '3-5', '4-5', '4-6', '4-8', '5-6', '5-7', '6-5', '7-5', '7-6', '8-7']; routes {'identity': 1387, 'position': 315, 'other': 451} (position share 0.1463); gate {'lookup': 0.9642857142857143, 'recall': 0.9671926910299004}

### Part 2: do three methods find the same code? (muse30_x51_11_p2, L26)

**S = 6: in between (none of the three)**

S = 6 (decisive): 600 (item, target) reads on 120 items (7 entities); bases U rank 5, P and R at k = 7 (d* = 7); label in between (none of the three)

| removed \ swap through | whole | U | P | R |
|---|---|---|---|---|
| none | 0.33 [0.30, 0.36] | 0.33 [0.30, 0.36] | 0.32 [0.30, 0.35] | 0.43 [0.42, 0.46] |
| U | 0.05 [0.03, 0.06] | 0.05 [0.03, 0.06] | 0.06 [0.04, 0.08] | 0.39 [0.37, 0.42] |
| P | 0.04 [0.03, 0.06] | 0.04 [0.03, 0.06] | 0.05 [0.03, 0.06] | 0.40 [0.38, 0.41] |
| R | 0.06 [0.04, 0.08] | 0.06 [0.04, 0.08] | 0.06 [0.04, 0.08] | 0.07 [0.05, 0.10] |
| random direction (same norm) | 0.00 [0.00, 0.01] | 0.01 [0.00, 0.01] | 0.00 [0.00, 0.01] | 0.01 [0.00, 0.01] |

reach (projected / whole): U 1.00 [1.00, 1.00]; P 0.97 [0.95, 1.01]; R 1.31 [1.19, 1.45]. Cuts (1 - removed / not): U->P 0.82 [0.76, 0.89]; U->R 0.10 [0.08, 0.13]; P->U 0.86 [0.82, 0.91]; P->R 0.09 [0.06, 0.11]; R->U 0.82 [0.76, 0.88]; R->P 0.81 [0.74, 0.88]. Self-removal left: U 0.14 [0.10, 0.19]; P 0.15 [0.10, 0.20]; R 0.17 [0.11, 0.24]. Removal alone moves the lookup off its slot: {'U': 0.2333, 'P': 0.2417, 'R': 0.375}. Median swap norms {'whole': 135.862, 'U': 135.862, 'P': 135.0525, 'R': 107.5416}. The recall moved per cell: {'none|whole': 0.0433, 'none|U': 0.0433, 'none|P': 0.0433, 'none|R': 0.085, 'U|whole': 0.0083, 'U|U': 0.0083, 'U|P': 0.01, 'U|R': 0.06, 'P|whole': 0.0067, 'P|U': 0.0067, 'P|P': 0.0117, 'P|R': 0.0667, 'R|whole': 0.0217, 'R|U': 0.0217, 'R|P': 0.0233, 'R|R': 0.0167}.

Geometry (mean cos² of the principal angles; random: max rank / d and the mean of 20 seeded pairs): U-P 0.785 (random 0.0011 / 0.0010); U-R 0.441 (random 0.0011 / 0.0010); P-R 0.338 (random 0.0011 / 0.0010)

S = 3 (beside): 240 (item, target) reads on 120 items (7 entities); bases U rank 2, P and R at k = 2 (d* = 2); label in between (none of the three)

| removed \ swap through | whole | U | P | R |
|---|---|---|---|---|
| none | 0.74 [0.68, 0.81] | 0.74 [0.68, 0.81] | 0.75 [0.70, 0.80] | 0.92 [0.89, 0.94] |
| U | 0.14 [0.10, 0.18] | 0.14 [0.10, 0.18] | 0.13 [0.08, 0.18] | 0.86 [0.82, 0.91] |
| P | 0.18 [0.13, 0.23] | 0.18 [0.13, 0.23] | 0.11 [0.07, 0.14] | 0.87 [0.83, 0.91] |
| R | 0.05 [0.02, 0.09] | 0.05 [0.02, 0.09] | 0.07 [0.03, 0.11] | 0.24 [0.20, 0.27] |
| random direction (same norm) | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.02] | 0.02 [0.00, 0.05] | 0.02 [0.01, 0.03] |

reach (projected / whole): U 1.00 [1.00, 1.00]; P 1.02 [0.99, 1.06]; R 1.24 [1.15, 1.35]. Cuts (1 - removed / not): U->P 0.82 [0.74, 0.90]; U->R 0.06 [0.03, 0.08]; P->U 0.75 [0.67, 0.83]; P->R 0.05 [0.02, 0.08]; R->U 0.93 [0.88, 0.97]; R->P 0.91 [0.86, 0.96]. Self-removal left: U 0.19 [0.12, 0.27]; P 0.14 [0.09, 0.19]; R 0.26 [0.21, 0.29]. Removal alone moves the lookup off its slot: {'U': 0.2833, 'P': 0.2167, 'R': 0.475}. Median swap norms {'whole': 165.1255, 'U': 165.1255, 'P': 160.8526, 'R': 129.8725}. The recall moved per cell: {'none|whole': 0.1458, 'none|U': 0.1542, 'none|P': 0.1375, 'none|R': 0.175, 'U|whole': 0.0083, 'U|U': 0.0083, 'U|P': 0.0042, 'U|R': 0.15, 'P|whole': 0.0083, 'P|U': 0.0083, 'P|P': 0.0083, 'P|R': 0.1458, 'R|whole': 0.0125, 'R|U': 0.0125, 'R|P': 0.0083, 'R|R': 0.025}.

Geometry (mean cos² of the principal angles; random: max rank / d and the mean of 20 seeded pairs): U-P 0.954 (random 0.0003 / 0.0003); U-R 0.623 (random 0.0003 / 0.0003); P-R 0.600 (random 0.0003 / 0.0003)

### Part 3: categories, an order or a line? (muse30_x51_11_p3, L26, S = 6)

**none of the three** at dose 2 (midpoint share from slot 1 0.13, from slot 6 0.01; full swaps at their target 0.36); at dose 4: none of the three (from 1 0.19, from 6 0.02)

Unedited O answers its own slot: {1: 1.0, 6: 1.0}. Real change size (median ||U U^T Δ||, test pairs) 82.128; median ||h_O|| 359.8. Items {'1': {'pool': 238, 'read': 112, 'eligible': 102, 'kept': 100}, '6': {'pool': 269, 'read': 120, 'eligible': 107, 'kept': 100}}.

| start | arm | dose | n | median norm | original | midpoint | far | near | another slot | not a slot |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | mid | 2 | 200 | 102.8024 | 0.01 [0.00, 0.02] | 0.13 [0.08, 0.18] | 0.49 [0.39, 0.60] | 0.04 [0.02, 0.08] | 0.33 [0.26, 0.39] | 0.00 [0.00, 0.00] |
| 1 | mid | 4 | 200 | 205.6047 | 0.01 [0.00, 0.01] | 0.19 [0.15, 0.22] | 0.34 [0.28, 0.41] | 0.08 [0.04, 0.12] | 0.39 [0.32, 0.45] | 0.00 [0.00, 0.00] |
| 1 | mid_random | 2 | 200 | 102.8024 | 0.99 [0.98, 1.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 1 | mid_random | 4 | 200 | 205.6048 | 0.96 [0.93, 0.99] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] |
| 1 | full | 2 | 200 | 205.6047 | 0.01 [0.00, 0.01] | 0.19 [0.15, 0.22] | 0.34 [0.28, 0.41] | 0.08 [0.04, 0.12] | 0.39 [0.32, 0.45] | 0.00 [0.00, 0.00] |
| 1 | full_random | 2 | 200 | 205.6048 | 0.96 [0.92, 1.00] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.04] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] |
| 6 | mid | 2 | 200 | 69.0032 | 0.74 [0.69, 0.80] | 0.01 [0.00, 0.02] | 0.22 [0.17, 0.27] | 0.00 [0.00, 0.00] | 0.03 [0.01, 0.05] | 0.00 [0.00, 0.00] |
| 6 | mid | 4 | 200 | 138.0063 | 0.39 [0.33, 0.44] | 0.02 [0.01, 0.04] | 0.39 [0.36, 0.41] | 0.03 [0.01, 0.05] | 0.18 [0.12, 0.24] | 0.00 [0.00, 0.00] |
| 6 | mid_random | 2 | 200 | 69.0032 | 0.99 [0.98, 1.00] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.01] | 0.00 [0.00, 0.00] |
| 6 | mid_random | 4 | 200 | 138.0063 | 0.96 [0.93, 0.98] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.02 [0.00, 0.04] | 0.00 [0.00, 0.00] |
| 6 | full | 2 | 200 | 138.0063 | 0.39 [0.33, 0.44] | 0.02 [0.01, 0.04] | 0.39 [0.36, 0.41] | 0.03 [0.01, 0.05] | 0.18 [0.12, 0.24] | 0.00 [0.00, 0.00] |
| 6 | full_random | 2 | 200 | 138.0063 | 0.95 [0.93, 0.98] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.03] | 0.01 [0.00, 0.02] | 0.03 [0.00, 0.05] | 0.00 [0.00, 0.00] |

Slot means at S = 6: mean distance by |i - j| 1: 46.74, 2: 65.88, 3: 83.36, 4: 99.72, 5: 115.86 (over lag 1: 1: 1.00, 2: 1.41, 3: 1.78, 4: 2.13, 5: 2.48); spread (std / mean; a simplex 0) 0.398; corr(distance, |i - j|) 0.776; PC shares [0.645, 0.228, 0.088], PC1 per slot [-75.16, -24.45, 5.18, 23.3, 32.6, 38.54], Spearman 1.00

Slot means at S = 8: mean distance by |i - j| 1: 38.96, 2: 53.80, 3: 67.62, 4: 80.12, 5: 93.69, 6: 106.47, 7: 118.40 (over lag 1: 1: 1.00, 2: 1.38, 3: 1.74, 4: 2.06, 5: 2.40, 6: 2.73, 7: 3.04); spread (std / mean; a simplex 0) 0.459; corr(distance, |i - j|) 0.759; PC shares [0.622, 0.221, 0.084], PC1 per slot [-80.16, -39.09, -9.63, 11.17, 22.05, 28.81, 33.0, 33.85], Spearman 1.00

### Part 4: the finding's wording

Labels: part 1 one_per_slot, part 2 in_between, part 3 none. Row -: no row of the wording table matches these labels; the wording is not fixed by the addendum

In every case the sentence no longer says "four directions"; "four" becomes a note on the first construction.

Figure: muse-glimmer-30b_part1.png

Figure: muse-glimmer-30b_part3.png

## qwen3.6-27b

Runs: {2: 'x51_11_p2_27b'}; present here: {2: 'x51_11_p2_27b'}. The design gives this model no part 1, 3: those labels read 'lacks the part'.

### Part 2: do three methods find the same code? (x51_11_p2_27b, L32)

**S = 6: in between (none of the three)**

S = 6 (decisive): 600 (item, target) reads on 120 items (7 entities); bases U rank 5, P and R at k = 2 (d* = 2); label in between (none of the three)

| removed \ swap through | whole | U | P | R |
|---|---|---|---|---|
| none | 0.31 [0.27, 0.36] | 0.31 [0.27, 0.36] | 0.23 [0.20, 0.25] | 0.32 [0.29, 0.34] |
| U | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.30 [0.29, 0.32] |
| P | 0.03 [0.02, 0.04] | 0.03 [0.02, 0.04] | 0.00 [0.00, 0.00] | 0.32 [0.31, 0.33] |
| R | 0.01 [0.00, 0.01] | 0.01 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.01 [0.01, 0.02] |
| random direction (same norm) | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.01] |

reach (projected / whole): U 1.00 [1.00, 1.00]; P 0.72 [0.67, 0.78]; R 1.01 [0.92, 1.10]. Cuts (1 - removed / not): U->P 0.99 [0.98, 1.00]; U->R 0.03 [−0.02, 0.07]; P->U 0.91 [0.87, 0.94]; P->R −0.01 [−0.08, 0.04]; R->U 0.98 [0.97, 0.99]; R->P 1.00 [1.00, 1.00]. Self-removal left: U 0.00 [0.00, 0.00]; P 0.00 [0.00, 0.00]; R 0.04 [0.02, 0.07]. Removal alone moves the lookup off its slot: {'U': 0.0, 'P': 0.0, 'R': 0.075}. Median swap norms {'whole': 42.8611, 'U': 42.861, 'P': 35.0979, 'R': 30.1268}. The recall moved per cell: {'none|whole': 0.055, 'none|U': 0.055, 'none|P': 0.0467, 'none|R': 0.0733, 'U|whole': 0.0083, 'U|U': 0.0083, 'U|P': 0.0083, 'U|R': 0.0683, 'P|whole': 0.015, 'P|U': 0.015, 'P|P': 0.0, 'P|R': 0.0617, 'R|whole': 0.01, 'R|U': 0.01, 'R|P': 0.0067, 'R|R': 0.0083}.

Geometry (mean cos² of the principal angles; random: max rank / d and the mean of 20 seeded pairs): U-P 0.992 (random 0.0010 / 0.0010); U-R 0.638 (random 0.0010 / 0.0010); P-R 0.553 (random 0.0004 / 0.0003)

S = 3: missing

### Part 4: the finding's wording

Labels: part 1 lacks the part / not decided, part 2 in_between, part 3 lacks the part / not decided. Row -: no row of the wording table matches these labels; the wording is not fixed by the addendum

In every case the sentence no longer says "four directions"; "four" becomes a note on the first construction.

