# Endgame rescore of the jsuite v2 facts knock-out (CPU only, stored rows; no new GPU runs)

Repo /workspace/bridge-jspace at a20e7454 (branch recovery-2026-10-19), read only. Code: /workspace/scratch/endgame/code/rescore.py (imports scripts/jsuite2_score.boot and scripts/c1_v2.margin_matched). Data: data/tasks_v2/jsuite_v2_test_chat (179 bridges x 2 levels; facts module). Raw numbers: rescore.json.

Runs (one knock-out run per model; single data seed; deterministic conditions; the rotated controls use one fixed rotation seed):

- Qwen 27B: jsuite_v2_test_chat_ko_cand2_v1 (band L32-40; paper10, paper10_rot, unembed10, unembed10_rot) and jsuite_v2_test_chat_ko_cand2_L32-40_pca_v1 (paper10_pcasize); competence run jsuite_v2_test_chat_competence_cand2_v1
- Qwen 9B: qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1 (band L12-16; paper10, paper10_rot, unembed10, unembed10_rot) and qwen35_9b_jsuite_v2_test_chat_ko_cand2_L12-16_pca_v1 (paper10_pcasize); competence run qwen35_9b_jsuite_v2_test_chat_competence_cand2_v1
- Lightning: nem35l_jsuite_v2_test_chat_ko_cand2_v1 (band L27-33; paper10, paper10_rot, unembed10, unembed10_rot) and nem35l_jsuite_v2_test_chat_ko_cand2_L27-33_pca_v1 (paper10_pcasize); competence run nem35l_jsuite_v2_test_chat_competence_cand2_v1

M - K = points lost on recalled (final M) minus points lost on stated (final K); points lost = 100 x (1 - knock-out accuracy) among items right unedited in the same run (the scorer's definition). 95% CI: percentile bootstrap over relation:bridge clusters, 1000 reps, the scorer's boot(); CIs are rounded to integers by the scorer.

## A. Reproduction

| model | paper10 M-K | paper10_rot | unembed10 | pcasize | data.csv (mk / rot / u / pc) | within 0.1 |
|---|---|---|---|---|---|---|
| Qwen 27B | 50.9 [46, 55] (n M = 892) | 2.7 [1, 4] | 1.9 [1, 3] | 12.4 [10, 15] | 50.9 / 2.7 / 1.9 / 12.4 | yes |
| Qwen 9B | 42.6 [37, 49] (n M = 563) | 1.8 [1, 3] | 1.4 [0, 3] | 7.3 [5, 10] | 42.6 / 1.8 / 1.4 / 7.3 | yes |
| Lightning | 53.1 [48, 59] (n M = 563) | 3.6 [2, 6] | 8.7 [6, 11] | 8.2 [6, 11] | 53.1 / 3.6 / 8.7 / 8.2 | yes |

Every facts cell of the six stored score JSONs (204 cells: every condition x start / half / relation; every contrast, its CI and every n) was recomputed with the scorer's logic and rng order: 0 mismatches, max |diff| 0.0.

## B. Subsets

Subset CIs: a fresh random.Random(0) per cell (the scorer shares one rng across cells, so the 'all' row's CI can differ by 1 point from the stored one: 27B [46, 56] here vs [46, 55] stored; point values identical).

Definitions. Starts: P (bridge read, a made-up person bound to it), T (tracked), M (described). 5 'not guessable': drop every item of a scene (start x level x bridge; the 5 finals share it) if the model's own competence run (the knock-out's tasks[1] run; cand2 read) answers the guess prompt of that scene's recalled-final item (word PM / TM / MM: the start replaced by an unknown one) correctly. 6: answer_vocab >= 14 (drops countries k=5 and animals k=6). 7: eponymous == False. 8 STRICT = start P and 5 and 6 and 7. 5b / 8b (robustness, stricter): drop a whole relation:bridge (both levels, every start) if any of its recalled-final guess prompts is right.

| model | guessable scenes in set (of 1074) | scored scenes dropped by 5 (of scored) | guessable bridges (of 179) | scored scenes dropped by 5b |
|---|---|---|---|---|
| Qwen 27B | 237 | 211 of 893 | 117 | 605 of 893 |
| Qwen 9B | 69 | 41 of 564 | 54 | 172 of 564 |
| Lightning | 143 | 77 of 568 | 93 | 296 of 568 |

### Qwen 27B

| subset | n K / n M (bridges) | lost K / lost M (paper10) | paper10 M-K | paper10_rot | unembed10 | unembed10_rot | pcasize |
|---|---|---|---|---|---|---|---|
| 1 all | 892 / 892 (179) | 2.6 / 53.5 | **50.9 [46, 56]** | 2.7 [1, 4] | 1.9 [1, 3] | 1.3 [1, 2] | 12.4 [10, 15] |
| 2 start P | 338 / 338 (177) | 0.3 / 50.9 | **50.6 [45, 56]** | 2.1 [1, 4] | 0.6 [0, 1] | 0.6 [0, 1] | 9.5 [6, 13] |
| 3 start T | 227 / 227 (150) | 1.3 / 60.8 | **59.5 [52, 66]** | 5.3 [2, 8] | 3.5 [1, 6] | 3.5 [1, 6] | 29.5 [22, 37] |
| 4 start M | 327 / 327 (173) | 5.8 / 51.1 | **45.3 [39, 52]** | 1.5 [0, 3] | 2.1 [1, 4] | 0.6 [-1, 2] | 3.7 [2, 6] |
| 5 not guessable | 681 / 681 (179) | 2.9 / 55.2 | **52.3 [47, 57]** | 3.2 [2, 5] | 2.3 [1, 4] | 1.5 [1, 3] | 13.8 [11, 17] |
| 6 >=14 candidates | 686 / 686 (138) | 3.1 / 56.9 | **53.8 [48, 59]** | 2.6 [1, 4] | 1.7 [1, 3] | 1.3 [0, 2] | 14.3 [11, 17] |
| 7 non-eponymous | 854 / 853 (172) | 2.3 / 54.2 | **51.8 [47, 57]** | 2.8 [2, 4] | 2.0 [1, 3] | 1.4 [1, 2] | 12.9 [10, 16] |
| 8 STRICT | 190 / 190 (121) | 0.5 / 58.9 | **58.4 [51, 65]** | 3.2 [1, 6] | 1.1 [0, 3] | 1.1 [0, 3] | 12.1 [7, 18] |
| 5b not guessable (bridge-level) | 288 / 288 (62) | 3.5 / 60.8 | **57.3 [49, 64]** | 5.2 [3, 9] | 3.1 [1, 5] | 1.7 [0, 3] | 16.7 [12, 23] |
| 8b STRICT (bridge-level guess) | 89 / 89 (48) | 1.1 / 61.8 | **60.7 [51, 71]** | 5.6 [1, 12] | 1.1 [0, 3] | 2.2 [0, 6] | 15.7 [8, 24] |

### Qwen 9B

| subset | n K / n M (bridges) | lost K / lost M (paper10) | paper10 M-K | paper10_rot | unembed10 | unembed10_rot | pcasize |
|---|---|---|---|---|---|---|---|
| 1 all | 564 / 563 (178) | 5.0 / 47.6 | **42.6 [37, 48]** | 1.8 [1, 3] | 1.4 [1, 2] | 1.4 [0, 3] | 7.3 [5, 10] |
| 2 start P | 259 / 258 (164) | 2.3 / 52.7 | **50.4 [43, 57]** | 1.6 [0, 4] | 1.9 [0, 4] | 2.7 [0, 5] | 8.9 [5, 13] |
| 3 start T | 58 / 58 (53) | 12.1 / 72.4 | **60.3 [45, 74]** | 10.3 [3, 19] | 5.2 [0, 12] | 3.4 [0, 9] | 20.7 [10, 33] |
| 4 start M | 247 / 247 (150) | 6.1 / 36.4 | **30.4 [24, 37]** | 0.0 [-1, 1] | 0.0 [-1, 1] | -0.4 [-1, 0] | 2.4 [1, 5] |
| 5 not guessable | 523 / 522 (176) | 5.0 / 47.7 | **42.7 [37, 48]** | 1.7 [1, 3] | 1.5 [1, 3] | 1.5 [0, 3] | 7.1 [5, 10] |
| 6 >=14 candidates | 445 / 444 (137) | 5.4 / 50.7 | **45.3 [39, 51]** | 1.6 [0, 3] | 1.6 [0, 3] | 2.0 [1, 4] | 7.0 [4, 10] |
| 7 non-eponymous | 541 / 540 (171) | 4.6 / 48.0 | **43.3 [38, 49]** | 1.9 [1, 3] | 1.5 [0, 3] | 1.5 [0, 3] | 7.4 [5, 10] |
| 8 STRICT | 175 / 174 (113) | 2.9 / 58.6 | **55.8 [46, 64]** | 2.3 [0, 5] | 2.9 [1, 6] | 4.6 [2, 8] | 9.8 [4, 16] |
| 5b not guessable (bridge-level) | 392 / 391 (124) | 5.1 / 47.3 | **42.2 [36, 48]** | 1.8 [0, 4] | 2.0 [1, 4] | 2.3 [1, 4] | 7.9 [5, 11] |
| 8b STRICT (bridge-level guess) | 143 / 142 (91) | 2.8 / 55.6 | **52.8 [44, 62]** | 2.8 [0, 6] | 3.5 [1, 7] | 5.6 [2, 10] | 9.9 [3, 17] |

### Lightning

| subset | n K / n M (bridges) | lost K / lost M (paper10) | paper10 M-K | paper10_rot | unembed10 | unembed10_rot | pcasize |
|---|---|---|---|---|---|---|---|
| 1 all | 567 / 563 (178) | 3.7 / 56.8 | **53.1 [47, 59]** | 3.6 [2, 6] | 8.7 [6, 11] | 2.1 [1, 3] | 8.2 [6, 11] |
| 2 start P | 275 / 275 (168) | 2.2 / 62.5 | **60.4 [54, 67]** | 4.4 [2, 7] | 6.9 [4, 10] | 1.8 [0, 4] | 10.2 [6, 14] |
| 3 start T | 68 / 66 (58) | 4.4 / 80.3 | **75.9 [65, 86]** | 9.1 [3, 17] | 30.3 [20, 41] | 7.6 [0, 16] | 16.9 [8, 28] |
| 4 start M | 224 / 222 (143) | 5.4 / 42.8 | **37.4 [30, 45]** | 0.9 [0, 2] | 4.5 [2, 8] | 0.9 [0, 2] | 3.2 [1, 6] |
| 5 not guessable | 490 / 486 (175) | 3.5 / 56.2 | **52.7 [47, 59]** | 4.1 [2, 6] | 9.7 [7, 12] | 2.7 [1, 4] | 8.6 [6, 11] |
| 6 >=14 candidates | 444 / 440 (138) | 3.8 / 59.8 | **55.9 [49, 62]** | 3.9 [2, 6] | 7.3 [5, 10] | 1.8 [1, 3] | 8.2 [5, 11] |
| 7 non-eponymous | 547 / 543 (171) | 3.8 / 57.6 | **53.8 [48, 60]** | 3.7 [2, 6] | 9.0 [7, 12] | 2.2 [1, 4] | 8.5 [6, 11] |
| 8 STRICT | 169 / 169 (112) | 1.8 / 68.6 | **66.9 [58, 76]** | 6.5 [3, 11] | 8.3 [4, 13] | 2.4 [1, 5] | 12.4 [7, 18] |
| 5b not guessable (bridge-level) | 272 / 272 (85) | 4.0 / 59.2 | **55.1 [47, 63]** | 5.5 [2, 9] | 11.4 [7, 16] | 1.8 [0, 4] | 9.6 [6, 14] |
| 8b STRICT (bridge-level guess) | 110 / 110 (69) | 2.7 / 71.8 | **69.1 [59, 79]** | 8.2 [4, 14] | 10.0 [5, 16] | 2.7 [0, 6] | 15.5 [9, 23] |

Pass bar (fixed in advance): STRICT M - K >= 10 with paper10_rot M - K <= 10, in >= 2 of 3 models.

| model | STRICT paper10 M-K | STRICT rot M-K | pass |
|---|---|---|---|
| Qwen 27B | 58.4 [51, 65] | 3.2 [1, 6] | PASS |
| Qwen 9B | 55.8 [46, 64] | 2.3 [0, 5] | PASS |
| Lightning | 66.9 [58, 76] | 6.5 [3, 11] | PASS |

Result: PASS (3 of 3 models).

## C. Confidence-matched gap (c1_v2.margin_matched, applied to v2)

Method = scripts/c1_v2.margin_matched unchanged (0.25-logit bins of the unedited answer margin from the competence run's 'whole' row; recalled-final items against stated-final items in the same bin, bins weighted by recalled-final items; 95% bootstrap over items, 1000 reps, seed 0), with its groups set to recalled = PM, MM, TM and stated = PK, MK, TK (same question and answer). Items: right unedited in the knock-out run (so 'raw' equals the headline M - K). The c1_v2-style variant over every row (loss = unedited correct - knock-out correct) is in rescore.json and differs by at most 1.1 points (Lightning paper10: matched 49.6 [44.1, 55.7], 509 of 568 matched).

| model | condition | raw | matched [95% CI] | matched / recalled-final items | reweighted to K margins | to M margins | median margin PK / MK / TK vs PM / MM / TM |
|---|---|---|---|---|---|---|---|
| Qwen 27B | paper10 | 50.9 | **51.5** [47.5, 55.1] | 823 / 892 | 42.9 | 50.1 | 7.62 / 6.88 / 5.88 vs 6.25 / 6.00 / 3.75 |
| Qwen 27B | paper10_rot | 2.7 | **2.5** [1.3, 3.8] | 823 / 892 | 1.1 | 2.4 | 7.62 / 6.88 / 5.88 vs 6.25 / 6.00 / 3.75 |
| Qwen 27B | unembed10 | 1.9 | **1.6** [0.7, 2.6] | 823 / 892 | 0.7 | 1.6 | 7.62 / 6.88 / 5.88 vs 6.25 / 6.00 / 3.75 |
| Qwen 9B | paper10 | 42.6 | **40.3** [34.6, 45.8] | 530 / 563 | 36.1 | 38.9 | 6.75 / 7.00 / 3.38 vs 3.56 / 5.50 / 1.31 |
| Qwen 9B | paper10_rot | 1.8 | **0.9** [-1.6, 2.9] | 530 / 563 | 0.3 | 0.7 | 6.75 / 7.00 / 3.38 vs 3.56 / 5.50 / 1.31 |
| Qwen 9B | unembed10 | 1.4 | **1.4** [-0.0, 2.7] | 530 / 563 | 0.4 | 1.0 | 6.75 / 7.00 / 3.38 vs 3.56 / 5.50 / 1.31 |
| Lightning | paper10 | 53.1 | **50.6** [45.0, 57.0] | 504 / 563 | 49.9 | 49.2 | 4.88 / 4.62 / 4.75 vs 3.25 / 3.62 / 1.88 |
| Lightning | paper10_rot | 3.6 | **2.2** [0.7, 3.3] | 504 / 563 | 1.1 | 3.6 | 4.88 / 4.62 / 4.75 vs 3.25 / 3.62 / 1.88 |
| Lightning | unembed10 | 8.7 | **4.9** [2.1, 7.8] | 504 / 563 | 3.8 | 8.2 | 4.88 / 4.62 / 4.75 vs 3.25 / 3.62 / 1.88 |

Loss (points) by quartile of the unedited margin under paper10 (Q1 least confident; cuts over both groups), n per cell:

| model | group | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|---|
| Qwen 27B | recalled (M) | 68 (n=316) | 51 (n=268) | 44 (n=205) | 33 (n=103) |
| Qwen 27B | stated (K) | 4 (n=143) | 4 (n=166) | 2 (n=273) | 1 (n=310) |
| Qwen 9B | recalled (M) | 60 (n=207) | 47 (n=175) | 31 (n=125) | 38 (n=56) |
| Qwen 9B | stated (K) | 16 (n=92) | 8 (n=99) | 0 (n=167) | 2 (n=206) |
| Lightning | recalled (M) | 60 (n=237) | 58 (n=168) | 51 (n=109) | 51 (n=49) |
| Lightning | stated (K) | 12 (n=67) | 7 (n=117) | 3 (n=156) | 0 (n=227) |
