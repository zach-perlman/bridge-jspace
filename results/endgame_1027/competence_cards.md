# Competence cards (unedited, cand2 read, stored competence runs; no new runs)

Code: /workspace/scratch/endgame/code/competence_cards.py; raw numbers competence_cards.json. Accuracy in %. 'correct' is each run's own field: cand2 read (top among the item's candidate answers, either case); hop 1 also needs the greedy generation to name the bridge (hop1='gen').

Columns: n = items in the set; whole; h1 / h2 / h3 = each hop alone; guess = the guess prompt (start replaced by an unknown one; candidates = answer_vocab); chance = mean over items of 1/k, k = len(answer_vocab); maj = majority baseline: per relation (domain for three-hop), share of items whose answer is that relation's most common answer, pooled; real = (whole - guess) / (1 - guess), * if >= 0.7; elig = items passing tasks_v2.eligible's rule with the knock-out runs' settings (facts: scene rule over the 15 facts words; three-hop and numbers: per-item rule; level 'all', core stratum; replicated without its assert and checked equal to tasks_v2.eligible and to the knock-out rows' item sets where those exist); h1x = items with hop 1 alone wrong, and the share of them right on the whole question (shortcut diagnostic).

Notes:
- Lightning facts competence vs its clean-checkout rerun: 21387 of 21480 prompt reads agree
- q27 facts: replicated 4465, tasks_v2.eligible 4465, equal True; knock-out rows' items 4465, equal True
- q9 facts: replicated 2820, tasks_v2.eligible 2820, equal True; knock-out rows' items 2820, equal True
- nl facts: replicated 2840, tasks_v2.eligible 2840, equal True; knock-out rows' items 2840, equal True
- q27 threehop: replicated 709, tasks_v2.eligible 709, equal True; knock-out rows' items 709, equal True
- nl numbers: replicated 340, tasks_v2.eligible 340, equal True; knock-out rows' items 340, equal True
- Lightning: facts from nem35l_jsuite_v2_test_chat_competence_cand2_v1 (the headline knock-out's); three-hop and numbers from nem35l_clean_jsuite_v2_test_chat_competence_cand2_v1 (the run the Lightning three-hop / numbers knock-outs used; the facts-only run has no three-hop / numbers rows).
- Ministral, Bolt, DeepSeek: their jsuite v2 test competence runs cover the 15 facts words only (manifest 'words'); three-hop and number words: NOT COMPUTABLE from stored runs.
- OLMo: only a QA-rendering run exists (olmo32_jsuite_v2_test_qa_competence_cand2_v1 on jsuite_v2_test_qa; the same items, ids j2:qa:* map 1:1 to j2:chat:*, same questions and answers). Not directly comparable to the chat-rendered runs.
- Never-named R start: v2.1 R competence runs exist for 27B, 9B, Lightning, Ministral, Muse, 122B. None for Bolt, DeepSeek, OLMo (OLMo has none; 9B-base has a QA one, not included).
- The guess prompt keeps the scene's context (only the start is replaced), so 'guess' measures priors plus context cues, not priors alone: for K / A / P finals the answer is in the passage (guess 20-60%); for the R start the in-context entities are other countries etc. and RM / RN guess rates are 0-2%.
- ANOMALY, not investigated: OLMo (QA rendering) answers the guess prompt right on 100% of nPR, nKR, nAR, nMR items (e.g. 53 of 53 nPR; 'How many fruits did Wanda pack?' with Wanda absent). The Qwen / Lightning runs do not (0-31%). Treat OLMo's number-word guess / real columns as suspect.
- Common subset: three strong models = 27B, 9B, Lightning (the three headline models).

## Summary across models (recalled-final words, the two-hop words a model fails most, three-hop and number flags)

| model | PM whole/guess/real | MM | TM | TP | MP | elig scenes P/M/T (of 358 per word) | three-hop words real >= 0.7 | number words real >= 0.7 |
|---|---|---|---|---|---|---|---|---|
| Qwen3.6 27B | 96/22/95 | 97/17/97 | 85/27/80 | 81/33/71 | 94/38/91 | 338/327/228 | 4 of 8 (PPM, MPM, PMM, MMM) | 5 of 12 (nPR, nPM, nKR, nAR, nMR) |
| Qwen3.5 9B | 92/8/91 | 94/2/94 | 48/9/42 | 42/27/20 | 77/31/66 | 259/247/58 | 2 of 8 (PMM, MMM) | 4 of 12 (nPR, nKR, nAR, nMR) |
| Nemotron 3.5 Lightning | 97/17/96 | 96/3/96 | 50/20/38 | 45/30/21 | 65/32/49 | 275/224/69 | 2 of 8 (PMM, MMM) | 4 of 12 (nPR, nKR, nAR, nMR) |
| Ministral 3 14B | 99/26/99 | 93/17/92 | 80/33/71 | 52/30/32 | 72/39/55 | 284/241/120 | no run | no run |
| Nemotron 3.5 Bolt | 94/13/93 | 98/4/98 | 63/12/58 | 50/32/27 | 86/37/78 | 292/298/85 | no run | no run |
| DeepSeek V4 Flash | 88/11/86 | 96/2/96 | 20/4/17 | 34/24/13 | 71/29/59 | 251/241/14 | no run | no run |
| Muse Glimmer 30B | 96/13/95 | 94/6/94 | 48/9/43 | 38/25/16 | 76/32/64 | 256/247/38 | 2 of 8 (PMM, MMM) | 4 of 12 (nPR, nKR, nAR, nMR) |
| OLMo 3 32B (QA rendering) | 96/20/95 | 94/4/94 | 35/13/25 | 34/27/10 | 68/37/49 | 227/216/24 | 2 of 8 (PMM, MMM) | 0 of 12 () |
| Qwen3.5 122B-A10B | 99/23/99 | 98/22/97 | 89/28/84 | 56/32/36 | 86/45/74 | 327/301/156 | 2 of 8 (PMM, MMM) | 4 of 12 (nPR, nKR, nAR, nMR) |

## Three-hop shortcut diagnostic (items whose hop 1 alone is wrong: n, and % of them right on the whole chain)

| model | PPP | MPP | PMP | PPM | MPM | MMP | PMM | MMM |
|---|---|---|---|---|---|---|---|---|
| Qwen3.6 27B | 0: - | 7: 29 | 0: - | 0: - | 6: 50 | 24: 33 | 0: - | 25: 76 |
| Qwen3.5 9B | 0: - | 8: 25 | 0: - | 2: 50 | 9: 56 | 33: 33 | 0: - | 26: 62 |
| Nemotron 3.5 Lightning | 1: 0 | 7: 29 | 0: - | 1: 100 | 8: 50 | 19: 26 | 1: 100 | 14: 43 |
| Ministral 3 14B | no three-hop run | | | | | | | |
| Nemotron 3.5 Bolt | no three-hop run | | | | | | | |
| DeepSeek V4 Flash | no three-hop run | | | | | | | |
| Muse Glimmer 30B | 6: 17 | 7: 29 | 2: 50 | 3: 33 | 6: 17 | 20: 0 | 2: 50 | 23: 70 |
| OLMo 3 32B (QA rendering) | 4: 0 | 6: 33 | 1: 0 | 1: 0 | 6: 50 | 11: 27 | 11: 91 | 9: 11 |
| Qwen3.5 122B-A10B | 0: - | 5: 20 | 0: - | 0: - | 3: 0 | 17: 41 | 0: - | 18: 67 |

## Never-named R start (v2.1 R competence runs)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Qwen3.6 27B** (jsuite_v2_1_test_chat_R_competence_cand2_v1) | | | | | | | | | | | |
| RM | 358 | 79 | 72 | 99 | - | 0 | 8 | 21 | 79* | 204 | 102: 51 |
| RA | 358 | 89 | 71 | 100 | - | 30 | 8 | 21 | 84* | 204 | 104: 75 |
| RN | 358 | 85 | 71 | 100 | - | 2 | 8 | 21 | 84* | 204 | 105: 69 |
| **Qwen3.5 9B** (qwen35_9b_jsuite_v2_1_test_chat_R_competence_cand2_v1) | | | | | | | | | | | |
| RM | 358 | 76 | 69 | 99 | - | 0 | 8 | 21 | 76* | 202 | 110: 44 |
| RA | 358 | 82 | 70 | 99 | - | 32 | 8 | 21 | 74* | 202 | 108: 58 |
| RN | 358 | 78 | 68 | 99 | - | 2 | 8 | 21 | 78* | 202 | 113: 50 |
| **Nemotron 3.5 Lightning** (nem35l_jsuite_v2_1_test_chat_R_competence_cand2_v1) | | | | | | | | | | | |
| RM | 358 | 87 | 84 | 100 | - | 1 | 8 | 21 | 87* | 261 | 57: 53 |
| RA | 358 | 90 | 84 | 100 | - | 28 | 8 | 21 | 86* | 261 | 59: 64 |
| RN | 358 | 88 | 85 | 99 | - | 2 | 8 | 21 | 88* | 261 | 55: 65 |
| **Ministral 3 14B** (min14_jsuite_v2_1_test_chat_R_competence_cand2_v1) | | | | | | | | | | | |
| RM | 358 | 77 | 81 | 99 | - | 2 | 8 | 21 | 76* | 231 | 68: 47 |
| RA | 358 | 81 | 83 | 99 | - | 26 | 8 | 21 | 75* | 231 | 60: 52 |
| RN | 358 | 80 | 82 | 100 | - | 2 | 8 | 21 | 79* | 231 | 66: 47 |
| **Muse Glimmer 30B** (muse30_jsuite_v2_1_test_chat_R_competence_cand2_v1) | | | | | | | | | | | |
| RM | 358 | 73 | 63 | 92 | - | 0 | 8 | 21 | 73* | 170 | 132: 50 |
| RA | 358 | 86 | 67 | 98 | - | 25 | 8 | 21 | 82* | 170 | 117: 74 |
| RN | 358 | 80 | 64 | 99 | - | 1 | 8 | 21 | 80* | 170 | 129: 62 |
| **Qwen3.5 122B-A10B** (qwen35_122b_jsuite_v2_1_test_chat_R_competence_cand2_v1) | | | | | | | | | | | |
| RM | 358 | 91 | 87 | 100 | - | 0 | 8 | 21 | 91* | 279 | 46: 65 |
| RA | 358 | 92 | 87 | 100 | - | 27 | 8 | 21 | 90* | 279 | 46: 74 |
| RN | 358 | 91 | 86 | 100 | - | 1 | 8 | 21 | 91* | 279 | 50: 66 |

RM per relation:

| model | animals | cities | companies | countries | dishes | landmarks | languages | people |
|---|---|---|---|---|---|---|---|---|
| Qwen3.6 27B | 41/0/41 e6 | 85/0/85 e26 | 69/0/69 e18 | 94/0/94 e42 | 63/0/63 e9 | 81/0/81 e20 | 88/0/88 e31 | 92/0/92 e52 |
| Qwen3.5 9B | 50/0/50 e6 | 88/0/88 e30 | 52/0/52 e14 | 85/0/85 e39 | 71/0/71 e10 | 76/0/76 e26 | 82/0/82 e33 | 87/0/87 e44 |
| Nemotron 3.5 Lightning | 76/0/76 e14 | 92/0/92 e33 | 81/5/80 e29 | 90/0/90 e41 | 87/0/87 e23 | 88/5/88 e33 | 90/0/90 e35 | 90/0/90 e53 |
| Ministral 3 14B | 47/3/45 e10 | 87/0/87 e35 | 62/2/61 e20 | 83/8/82 e37 | 68/0/68 e16 | 76/5/75 e27 | 82/0/82 e33 | 92/0/92 e53 |
| Muse Glimmer 30B | 44/3/42 e0 | 87/0/87 e30 | 55/0/55 e13 | 71/0/71 e33 | 63/0/63 e8 | 79/0/79 e23 | 82/0/82 e32 | 90/0/90 e31 |
| Qwen3.5 122B-A10B | 68/3/67 e13 | 94/0/94 e42 | 86/0/86 e29 | 94/0/94 e43 | 92/0/92 e29 | 95/0/95 e34 | 90/0/90 e35 | 98/0/98 e54 |
(cells: whole / guess / real, e = eligible n)

## Common subset (items eligible in all three strong models: 27B, 9B, Lightning; by the knock-out's rule)

Whole / guess / real on that subset. The three strong models are 100% on 'whole' there by construction (eligible = every non-guess prompt right); their guess rates are not.

### facts: 2035 items

| model | PP | PK | PM | PA | PN | MP | MK | MM | MA | MN | TP | TK | TM | TA | TN |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6 27B | 100/39/100 (n211) | 100/26/100 (n211) | 100/23/100 (n211) | 100/39/100 (n211) | 100/20/100 (n211) | 100/46/100 (n179) | 100/60/100 (n179) | 100/21/100 (n179) | 100/58/100 (n179) | 100/39/100 (n179) | 100/71/100 (n17) | 100/53/100 (n17) | 100/47/100 (n17) | 100/47/100 (n17) | 100/47/100 (n17) |
| Qwen3.5 9B | 100/36/100 (n211) | 100/25/100 (n211) | 100/10/100 (n211) | 100/32/100 (n211) | 100/15/100 (n211) | 100/37/100 (n179) | 100/41/100 (n179) | 100/3/100 (n179) | 100/47/100 (n179) | 100/22/100 (n179) | 100/53/100 (n17) | 100/47/100 (n17) | 100/24/100 (n17) | 100/76/100 (n17) | 100/53/100 (n17) |
| Nemotron 3.5 Lightning | 100/32/100 (n211) | 100/24/100 (n211) | 100/18/100 (n211) | 100/38/100 (n211) | 100/24/100 (n211) | 100/33/100 (n179) | 100/30/100 (n179) | 100/2/100 (n179) | 100/41/100 (n179) | 100/13/100 (n179) | 100/71/100 (n17) | 100/76/100 (n17) | 100/47/100 (n17) | 100/59/100 (n17) | 100/71/100 (n17) |
| Ministral 3 14B | 89/20/86 (n211) | 100/19/99 (n211) | 99/27/99 (n211) | 99/30/99 (n211) | 100/26/99 (n211) | 90/37/84 (n179) | 99/49/99 (n179) | 99/19/99 (n179) | 99/43/99 (n179) | 99/33/99 (n179) | 65/35/45 (n17) | 100/76/100 (n17) | 100/24/100 (n17) | 100/59/100 (n17) | 100/41/100 (n17) |
| Nemotron 3.5 Bolt | 98/36/97 (n211) | 100/31/100 (n211) | 97/14/96 (n211) | 98/49/96 (n211) | 98/19/98 (n211) | 98/42/96 (n179) | 99/45/99 (n179) | 99/5/99 (n179) | 99/50/98 (n179) | 99/13/99 (n179) | 71/47/44 (n17) | 100/53/100 (n17) | 94/29/92 (n17) | 94/47/89 (n17) | 88/41/80 (n17) |
| DeepSeek V4 Flash | 91/33/87 (n211) | 99/27/98 (n211) | 92/14/91 (n211) | 95/53/90 (n211) | 95/25/93 (n211) | 87/32/80 (n179) | 100/37/100 (n179) | 99/3/99 (n179) | 99/48/99 (n179) | 100/14/100 (n179) | 65/29/50 (n17) | 65/35/45 (n17) | 29/6/25 (n17) | 76/59/43 (n17) | 47/24/31 (n17) |
| Muse Glimmer 30B | 90/31/85 (n211) | 100/25/99 (n211) | 97/14/97 (n211) | 99/47/98 (n211) | 97/20/96 (n211) | 90/28/86 (n179) | 100/49/100 (n179) | 98/7/98 (n179) | 99/40/99 (n179) | 99/25/99 (n179) | 65/41/40 (n17) | 94/24/92 (n17) | 65/12/60 (n17) | 94/35/91 (n17) | 71/12/67 (n17) |
| OLMo 3 32B (QA rendering) | 86/32/79 (n211) | 98/24/97 (n211) | 98/20/98 (n211) | 99/47/98 (n211) | 95/22/94 (n211) | 87/39/79 (n179) | 98/29/98 (n179) | 97/3/97 (n179) | 97/52/94 (n179) | 95/24/93 (n179) | 65/41/40 (n17) | 88/71/60 (n17) | 47/18/36 (n17) | 76/53/50 (n17) | 65/53/25 (n17) |
| Qwen3.5 122B-A10B | 99/34/98 (n211) | 100/23/100 (n211) | 100/25/99 (n211) | 100/31/100 (n211) | 99/20/99 (n211) | 98/47/97 (n179) | 100/46/100 (n179) | 99/23/99 (n179) | 100/56/100 (n179) | 100/34/100 (n179) | 76/41/60 (n17) | 100/65/100 (n17) | 88/29/83 (n17) | 94/71/80 (n17) | 94/47/89 (n17) |

### threehop: 324 items

| model | PPP | MPP | PMP | PPM | MPM | MMP | PMM | MMM |
|---|---|---|---|---|---|---|---|---|
| Qwen3.6 27B | 100/46/100 (n13) | 100/28/100 (n25) | 100/33/100 (n30) | 100/34/100 (n44) | 100/46/100 (n13) | 100/35/100 (n17) | 100/18/100 (n108) | 100/12/100 (n74) |
| Qwen3.5 9B | 100/62/100 (n13) | 100/52/100 (n25) | 100/37/100 (n30) | 100/18/100 (n44) | 100/31/100 (n13) | 100/41/100 (n17) | 100/19/100 (n108) | 100/20/100 (n74) |
| Nemotron 3.5 Lightning | 100/54/100 (n13) | 100/36/100 (n25) | 100/23/100 (n30) | 100/39/100 (n44) | 100/23/100 (n13) | 100/59/100 (n17) | 100/25/100 (n108) | 100/16/100 (n74) |
| Muse Glimmer 30B | 62/54/17 (n13) | 60/48/23 (n25) | 63/23/52 (n30) | 59/23/47 (n44) | 23/23/0 (n13) | 35/18/21 (n17) | 97/19/97 (n108) | 97/14/97 (n74) |
| OLMo 3 32B (QA rendering) | 46/54/-17 (n13) | 52/44/14 (n25) | 73/23/65 (n30) | 48/23/32 (n44) | 46/31/22 (n13) | 71/47/44 (n17) | 98/11/98 (n108) | 100/7/100 (n74) |
| Qwen3.5 122B-A10B | 54/38/25 (n13) | 64/20/55 (n25) | 67/53/29 (n30) | 95/23/94 (n44) | 92/31/89 (n13) | 65/41/40 (n17) | 98/31/97 (n108) | 100/18/100 (n74) |

### numbers: 270 items

| model | nPR | nPL | nPM | nKR | nKL | nKM | nAR | nAL | nAM | nMR | nML | nMM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6 27B | 100/17/100 (n53) | 100/40/100 (n5) | 100/9/100 (n32) | 100/5/100 (n42) | - | 100/33/100 (n3) | 100/11/100 (n57) | - | 100/0/100 (n1) | 100/2/100 (n59) | 100/25/100 (n8) | 100/0/100 (n10) |
| Qwen3.5 9B | 100/2/100 (n53) | 100/60/100 (n5) | 100/3/100 (n32) | 100/0/100 (n42) | - | 100/0/100 (n3) | 100/5/100 (n57) | - | 100/0/100 (n1) | 100/10/100 (n59) | 100/12/100 (n8) | 100/10/100 (n10) |
| Nemotron 3.5 Lightning | 100/0/100 (n53) | 100/20/100 (n5) | 100/12/100 (n32) | 100/31/100 (n42) | - | 100/0/100 (n3) | 100/7/100 (n57) | - | 100/0/100 (n1) | 100/8/100 (n59) | 100/25/100 (n8) | 100/10/100 (n10) |
| Muse Glimmer 30B | 100/28/100 (n53) | 40/0/40 (n5) | 69/22/60 (n32) | 95/26/94 (n42) | - | 33/0/33 (n3) | 98/30/97 (n57) | - | 100/100/- (n1) | 86/2/86 (n59) | 25/0/25 (n8) | 90/20/87 (n10) |
| OLMo 3 32B (QA rendering) | 100/100/- (n53) | 100/20/100 (n5) | 91/25/88 (n32) | 100/100/- (n42) | - | 33/33/0 (n3) | 100/100/- (n57) | - | 0/0/0 (n1) | 100/100/- (n59) | 75/12/71 (n8) | 100/0/100 (n10) |
| Qwen3.5 122B-A10B | 100/25/100 (n53) | 80/20/75 (n5) | 94/16/93 (n32) | 100/2/100 (n42) | - | 100/33/100 (n3) | 100/4/100 (n57) | - | 100/0/100 (n1) | 100/5/100 (n59) | 38/25/17 (n8) | 100/0/100 (n10) |

## Full cards per model

### Qwen3.6 27B (jsuite_v2_test_chat; runs: jsuite_v2_test_chat_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 99 | 100 | 100 | - | 32 | 8 | 16 | 98* | 338 | 0: - |
| PK | 358 | 100 | 100 | 100 | - | 26 | 8 | 21 | 100* | 338 | 0: - |
| PM | 358 | 96 | 100 | 98 | - | 22 | 8 | 21 | 95* | 338 | 0: - |
| PA | 358 | 98 | 100 | 100 | - | 40 | 8 | 21 | 97* | 338 | 0: - |
| PN | 358 | 100 | 100 | 100 | - | 20 | 8 | 21 | 100* | 338 | 0: - |
| MP | 358 | 94 | 99 | 100 | - | 38 | 8 | 16 | 91* | 327 | 5: 20 |
| MK | 358 | 98 | 99 | 100 | - | 55 | 8 | 21 | 96* | 327 | 4: 0 |
| MM | 358 | 97 | 99 | 100 | - | 17 | 8 | 21 | 97* | 327 | 2: 0 |
| MA | 358 | 99 | 99 | 100 | - | 57 | 8 | 21 | 98* | 327 | 2: 100 |
| MN | 358 | 97 | 99 | 100 | - | 36 | 8 | 21 | 96* | 327 | 2: 0 |
| TP | 358 | 81 | 98 | 100 | - | 33 | 8 | 16 | 71* | 228 | 6: 50 |
| TK | 358 | 97 | 97 | 100 | - | 41 | 8 | 21 | 95* | 228 | 9: 22 |
| TM | 358 | 85 | 99 | 98 | - | 27 | 8 | 21 | 80* | 228 | 5: 60 |
| TA | 358 | 95 | 99 | 100 | - | 39 | 8 | 21 | 92* | 228 | 5: 40 |
| TN | 358 | 92 | 98 | 100 | - | 34 | 8 | 21 | 88* | 228 | 6: 17 |
| PPP | 118 | 56 | 100 | 100 | 100 | 27 | 20 | 27 | 40 | 66 | 0: - |
| MPP | 131 | 62 | 95 | 100 | 100 | 21 | 20 | 30 | 51 | 79 | 7: 29 |
| PMP | 126 | 55 | 100 | 99 | 100 | 27 | 20 | 26 | 38 | 69 | 0: - |
| PPM | 131 | 79 | 100 | 100 | 100 | 27 | 20 | 31 | 72* | 104 | 0: - |
| MPM | 121 | 79 | 95 | 100 | 100 | 26 | 20 | 29 | 72* | 93 | 6: 50 |
| MMP | 132 | 67 | 82 | 100 | 100 | 25 | 20 | 29 | 56 | 80 | 24: 33 |
| PMM | 131 | 100 | 100 | 98 | 100 | 19 | 20 | 37 | 100* | 129 | 0: - |
| MMM | 117 | 92 | 79 | 100 | 100 | 10 | 20 | 41 | 91* | 89 | 25: 76 |
| nPR | 53 | 100 | 100 | - | - | 17 | 11 | 21 | 100* | 53 | 0: - |
| nPL | 61 | 49 | 98 | 100 | - | 13 | 12 | 10 | 42 | 29 | 1: 100 |
| nPM | 61 | 75 | 98 | 90 | - | 13 | 12 | 21 | 72* | 43 | 1: 0 |
| nKR | 52 | 100 | 100 | - | - | 4 | 11 | 21 | 100* | 52 | 0: - |
| nKL | 62 | 21 | 100 | 100 | - | 15 | 12 | 8 | 8 | 13 | 0: - |
| nKM | 62 | 61 | 100 | 77 | - | 5 | 12 | 19 | 59 | 33 | 0: - |
| nAR | 58 | 100 | 100 | - | - | 10 | 11 | 19 | 100* | 58 | 0: - |
| nAL | 60 | 10 | 100 | 100 | - | 7 | 12 | 7 | 4 | 6 | 0: - |
| nAM | 60 | 58 | 100 | 87 | - | 8 | 12 | 20 | 55 | 35 | 0: - |
| nMR | 62 | 97 | 97 | - | - | 2 | 11 | 19 | 97* | 60 | 2: 0 |
| nML | 56 | 46 | 98 | 100 | - | 16 | 12 | 9 | 36 | 26 | 1: 0 |
| nMM | 56 | 46 | 98 | 84 | - | 11 | 12 | 21 | 40 | 25 | 1: 100 |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 100 / 35 / 100*, e33 (maj 35% 'insect') | 97 / 18 / 96*, e30 (maj 35% 'insect') | 88 / 44 / 79*, e19 (maj 35% 'insect') |
| cities (30) | 100 / 27 / 100*, e52 (maj 12% 'Germany') | 94 / 0 / 94*, e44 (maj 12% 'Germany') | 96 / 23 / 95*, e37 (maj 12% 'Germany') |
| companies (14) | 95 / 24 / 94*, e40 (maj 14% 'Germany') | 100 / 36 / 100*, e41 (maj 14% 'Germany') | 95 / 31 / 93*, e31 (maj 14% 'Germany') |
| countries (5) | 100 / 21 / 100*, e48 (maj 42% 'Europe') | 100 / 21 / 100*, e43 (maj 42% 'Europe') | 96 / 25 / 94*, e33 (maj 42% 'Europe') |
| dishes (20) | 71 / 13 / 67, e26 (maj 16% 'Italy') | 95 / 3 / 95*, e36 (maj 16% 'Italy') | 42 / 13 / 33, e13 (maj 16% 'Italy') |
| landmarks (27) | 100 / 33 / 100*, e41 (maj 10% 'Peru') | 100 / 52 / 100*, e42 (maj 10% 'Peru') | 98 / 48 / 95*, e27 (maj 10% 'Peru') |
| languages (16) | 100 / 12 / 100*, e40 (maj 30% 'Spanish') | 98 / 5 / 97*, e36 (maj 30% 'Spanish') | 100 / 28 / 100*, e35 (maj 30% 'Spanish') |
| people (23) | 97 / 16 / 96*, e58 (maj 13% 'German') | 95 / 6 / 95*, e55 (maj 13% 'German') | 68 / 15 / 62, e33 (maj 13% 'German') |

### Qwen3.5 9B (jsuite_v2_test_chat; runs: qwen35_9b_jsuite_v2_test_chat_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 80 | 100 | 99 | - | 31 | 8 | 16 | 71* | 259 | 1: 0 |
| PK | 358 | 99 | 100 | 100 | - | 25 | 8 | 21 | 99* | 259 | 1: 0 |
| PM | 358 | 92 | 100 | 99 | - | 8 | 8 | 21 | 91* | 259 | 0: - |
| PA | 358 | 98 | 100 | 100 | - | 31 | 8 | 21 | 97* | 259 | 0: - |
| PN | 358 | 99 | 100 | 100 | - | 15 | 8 | 21 | 98* | 259 | 1: 100 |
| MP | 358 | 77 | 97 | 98 | - | 31 | 8 | 16 | 66 | 247 | 11: 45 |
| MK | 358 | 97 | 98 | 100 | - | 38 | 8 | 21 | 96* | 247 | 7: 71 |
| MM | 358 | 94 | 97 | 99 | - | 2 | 8 | 21 | 94* | 247 | 10: 10 |
| MA | 358 | 96 | 97 | 100 | - | 44 | 8 | 21 | 92* | 247 | 9: 33 |
| MN | 358 | 94 | 98 | 100 | - | 22 | 8 | 21 | 92* | 247 | 8: 38 |
| TP | 358 | 42 | 90 | 99 | - | 27 | 8 | 16 | 20 | 58 | 36: 28 |
| TK | 358 | 77 | 92 | 100 | - | 26 | 8 | 21 | 69 | 58 | 27: 19 |
| TM | 358 | 48 | 93 | 100 | - | 9 | 8 | 21 | 42 | 58 | 24: 12 |
| TA | 358 | 79 | 94 | 100 | - | 39 | 8 | 21 | 66 | 58 | 20: 45 |
| TN | 358 | 72 | 89 | 100 | - | 25 | 8 | 21 | 63 | 58 | 40: 28 |
| PPP | 118 | 21 | 100 | 97 | 98 | 25 | 20 | 27 | -6 | 25 | 0: - |
| MPP | 131 | 34 | 94 | 99 | 99 | 27 | 20 | 30 | 9 | 42 | 8: 25 |
| PMP | 126 | 40 | 100 | 98 | 100 | 29 | 20 | 26 | 16 | 50 | 0: - |
| PPM | 131 | 45 | 98 | 98 | 100 | 20 | 20 | 31 | 31 | 58 | 2: 50 |
| MPM | 121 | 32 | 93 | 100 | 100 | 23 | 20 | 29 | 12 | 34 | 9: 56 |
| MMP | 132 | 38 | 75 | 99 | 100 | 27 | 20 | 29 | 15 | 39 | 33: 33 |
| PMM | 131 | 94 | 100 | 100 | 100 | 19 | 20 | 37 | 92* | 123 | 0: - |
| MMM | 117 | 87 | 78 | 99 | 100 | 17 | 20 | 41 | 85* | 86 | 26: 62 |
| nPR | 53 | 100 | 100 | - | - | 2 | 11 | 21 | 100* | 53 | 0: - |
| nPL | 61 | 16 | 100 | 100 | - | 20 | 12 | 10 | -4 | 10 | 0: - |
| nPM | 61 | 67 | 100 | 89 | - | 8 | 12 | 21 | 64 | 40 | 0: - |
| nKR | 52 | 98 | 98 | - | - | 0 | 11 | 21 | 98* | 51 | 1: 0 |
| nKL | 62 | 10 | 100 | 100 | - | 11 | 12 | 8 | -2 | 6 | 0: - |
| nKM | 62 | 18 | 100 | 89 | - | 5 | 12 | 19 | 14 | 9 | 0: - |
| nAR | 58 | 98 | 98 | - | - | 5 | 11 | 19 | 98* | 57 | 1: 0 |
| nAL | 60 | 8 | 100 | 100 | - | 15 | 12 | 7 | -8 | 5 | 0: - |
| nAM | 60 | 23 | 100 | 93 | - | 0 | 12 | 20 | 23 | 13 | 0: - |
| nMR | 62 | 98 | 98 | - | - | 10 | 11 | 19 | 98* | 61 | 1: 0 |
| nML | 56 | 25 | 100 | 100 | - | 16 | 12 | 9 | 11 | 14 | 0: - |
| nMM | 56 | 46 | 100 | 89 | - | 5 | 12 | 21 | 43 | 25 | 0: - |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 100 / 15 / 100*, e27 (maj 35% 'insect') | 79 / 6 / 78*, e12 (maj 35% 'insect') | 53 / 32 / 30, e3 (maj 35% 'insect') |
| cities (30) | 100 / 6 / 100*, e48 (maj 12% 'Germany') | 92 / 0 / 92*, e33 (maj 12% 'Germany') | 73 / 10 / 70*, e14 (maj 12% 'Germany') |
| companies (14) | 98 / 12 / 97*, e36 (maj 14% 'Germany') | 98 / 5 / 98*, e36 (maj 14% 'Germany') | 45 / 7 / 41, e10 (maj 14% 'Germany') |
| countries (5) | 98 / 21 / 97*, e36 (maj 42% 'Europe') | 100 / 0 / 100*, e28 (maj 42% 'Europe') | 79 / 2 / 79*, e13 (maj 42% 'Europe') |
| dishes (20) | 79 / 0 / 79*, e23 (maj 16% 'Italy') | 92 / 0 / 92*, e27 (maj 16% 'Italy') | 13 / 8 / 6, e0 (maj 16% 'Italy') |
| landmarks (27) | 93 / 10 / 92*, e26 (maj 10% 'Peru') | 98 / 5 / 98*, e38 (maj 10% 'Peru') | 40 / 12 / 32, e2 (maj 10% 'Peru') |
| languages (16) | 100 / 5 / 100*, e33 (maj 30% 'Spanish') | 90 / 0 / 90*, e24 (maj 30% 'Spanish') | 60 / 10 / 56, e8 (maj 30% 'Spanish') |
| people (23) | 73 / 2 / 72*, e30 (maj 13% 'German') | 98 / 0 / 98*, e49 (maj 13% 'German') | 19 / 2 / 18, e8 (maj 13% 'German') |

### Nemotron 3.5 Lightning (jsuite_v2_test_chat; runs: nem35l_clean_jsuite_v2_test_chat_competence_cand2_v1, nem35l_jsuite_v2_test_chat_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 82 | 100 | 98 | - | 29 | 8 | 16 | 75* | 275 | 1: 100 |
| PK | 358 | 99 | 99 | 100 | - | 23 | 8 | 21 | 99* | 275 | 2: 50 |
| PM | 358 | 97 | 100 | 99 | - | 17 | 8 | 21 | 96* | 275 | 0: - |
| PA | 358 | 98 | 100 | 100 | - | 37 | 8 | 21 | 96* | 275 | 1: 100 |
| PN | 358 | 96 | 99 | 100 | - | 23 | 8 | 21 | 95* | 275 | 2: 50 |
| MP | 358 | 65 | 97 | 100 | - | 32 | 8 | 16 | 49 | 224 | 12: 25 |
| MK | 358 | 96 | 98 | 100 | - | 28 | 8 | 21 | 95* | 224 | 6: 67 |
| MM | 358 | 96 | 97 | 100 | - | 3 | 8 | 21 | 96* | 224 | 12: 42 |
| MA | 358 | 96 | 97 | 100 | - | 42 | 8 | 21 | 93* | 224 | 11: 45 |
| MN | 358 | 97 | 97 | 99 | - | 10 | 8 | 21 | 96* | 224 | 10: 60 |
| TP | 358 | 45 | 78 | 99 | - | 30 | 8 | 16 | 21 | 69 | 79: 20 |
| TK | 358 | 67 | 81 | 100 | - | 38 | 8 | 21 | 47 | 69 | 69: 16 |
| TM | 358 | 50 | 84 | 99 | - | 20 | 8 | 21 | 38 | 69 | 59: 7 |
| TA | 358 | 68 | 82 | 99 | - | 40 | 8 | 21 | 46 | 69 | 63: 24 |
| TN | 358 | 66 | 78 | 99 | - | 36 | 8 | 21 | 48 | 69 | 77: 18 |
| PPP | 118 | 31 | 99 | 99 | 99 | 20 | 20 | 27 | 13 | 36 | 1: 0 |
| MPP | 131 | 41 | 95 | 98 | 98 | 25 | 20 | 30 | 21 | 51 | 7: 29 |
| PMP | 126 | 38 | 100 | 98 | 99 | 20 | 20 | 26 | 23 | 47 | 0: - |
| PPM | 131 | 53 | 99 | 95 | 100 | 31 | 20 | 31 | 32 | 67 | 1: 100 |
| MPM | 121 | 25 | 93 | 100 | 100 | 21 | 20 | 29 | 4 | 26 | 8: 50 |
| MMP | 132 | 27 | 86 | 98 | 94 | 22 | 20 | 29 | 7 | 31 | 19: 26 |
| PMM | 131 | 86 | 99 | 98 | 100 | 24 | 20 | 37 | 82* | 112 | 1: 100 |
| MMM | 117 | 87 | 88 | 97 | 100 | 14 | 20 | 41 | 85* | 94 | 14: 43 |
| nPR | 53 | 100 | 100 | - | - | 0 | 11 | 21 | 100* | 53 | 0: - |
| nPL | 61 | 34 | 100 | 100 | - | 5 | 12 | 10 | 31 | 21 | 0: - |
| nPM | 61 | 62 | 100 | 93 | - | 11 | 12 | 21 | 57 | 37 | 0: - |
| nKR | 52 | 83 | 83 | - | - | 29 | 11 | 21 | 76* | 43 | 9: 0 |
| nKL | 62 | 16 | 94 | 100 | - | 16 | 12 | 8 | 0 | 9 | 4: 25 |
| nKM | 62 | 26 | 94 | 92 | - | 6 | 12 | 19 | 21 | 15 | 4: 25 |
| nAR | 58 | 100 | 100 | - | - | 7 | 11 | 19 | 100* | 58 | 0: - |
| nAL | 60 | 7 | 100 | 100 | - | 15 | 12 | 7 | -10 | 4 | 0: - |
| nAM | 60 | 13 | 100 | 97 | - | 7 | 12 | 20 | 7 | 8 | 0: - |
| nMR | 62 | 100 | 100 | - | - | 8 | 11 | 19 | 100* | 62 | 0: - |
| nML | 56 | 23 | 98 | 100 | - | 16 | 12 | 9 | 9 | 13 | 1: 0 |
| nMM | 56 | 30 | 98 | 96 | - | 7 | 12 | 21 | 25 | 17 | 1: 0 |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 100 / 12 / 100*, e30 (maj 35% 'insect') | 94 / 0 / 94*, e25 (maj 35% 'insect') | 56 / 38 / 29, e5 (maj 35% 'insect') |
| cities (30) | 96 / 13 / 96*, e44 (maj 12% 'Germany') | 92 / 0 / 92*, e26 (maj 12% 'Germany') | 48 / 21 / 34, e11 (maj 12% 'Germany') |
| companies (14) | 95 / 31 / 93*, e36 (maj 14% 'Germany') | 98 / 5 / 98*, e34 (maj 14% 'Germany') | 40 / 12 / 32, e10 (maj 14% 'Germany') |
| countries (5) | 98 / 25 / 97*, e35 (maj 42% 'Europe') | 96 / 4 / 96*, e18 (maj 42% 'Europe') | 65 / 21 / 55, e10 (maj 42% 'Europe') |
| dishes (20) | 100 / 13 / 100*, e29 (maj 16% 'Italy') | 97 / 3 / 97*, e26 (maj 16% 'Italy') | 74 / 39 / 57, e15 (maj 16% 'Italy') |
| landmarks (27) | 98 / 12 / 97*, e30 (maj 10% 'Peru') | 98 / 5 / 98*, e29 (maj 10% 'Peru') | 48 / 7 / 44, e4 (maj 10% 'Peru') |
| languages (16) | 98 / 15 / 97*, e30 (maj 30% 'Spanish') | 95 / 2 / 95*, e19 (maj 30% 'Spanish') | 60 / 35 / 38, e10 (maj 30% 'Spanish') |
| people (23) | 94 / 16 / 92*, e41 (maj 13% 'German') | 98 / 2 / 98*, e47 (maj 13% 'German') | 26 / 2 / 25, e4 (maj 13% 'German') |

### Ministral 3 14B (jsuite_v2_test_chat; runs: min14_jsuite_v2_test_chat_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 81 | 99 | 97 | - | 21 | 8 | 16 | 76* | 284 | 2: 50 |
| PK | 358 | 100 | 100 | 100 | - | 18 | 8 | 21 | 100* | 284 | 1: 0 |
| PM | 358 | 99 | 100 | 100 | - | 26 | 8 | 21 | 99* | 284 | 1: 0 |
| PA | 358 | 99 | 100 | 100 | - | 30 | 8 | 21 | 99* | 284 | 1: 0 |
| PN | 358 | 99 | 99 | 100 | - | 22 | 8 | 21 | 99* | 284 | 2: 50 |
| MP | 358 | 72 | 97 | 97 | - | 39 | 8 | 16 | 55 | 241 | 9: 22 |
| MK | 358 | 96 | 99 | 100 | - | 49 | 8 | 21 | 91* | 241 | 5: 20 |
| MM | 358 | 93 | 97 | 100 | - | 17 | 8 | 21 | 92* | 241 | 10: 60 |
| MA | 358 | 94 | 97 | 100 | - | 42 | 8 | 21 | 89* | 241 | 11: 73 |
| MN | 358 | 93 | 97 | 100 | - | 28 | 8 | 21 | 91* | 241 | 10: 40 |
| TP | 358 | 52 | 88 | 95 | - | 30 | 8 | 16 | 32 | 120 | 42: 29 |
| TK | 358 | 90 | 91 | 100 | - | 46 | 8 | 21 | 82* | 120 | 34: 59 |
| TM | 358 | 80 | 92 | 100 | - | 33 | 8 | 21 | 71* | 120 | 27: 22 |
| TA | 358 | 85 | 92 | 100 | - | 43 | 8 | 21 | 74* | 120 | 30: 40 |
| TN | 358 | 81 | 89 | 100 | - | 35 | 8 | 21 | 71* | 120 | 38: 34 |
| PPP | no threehop competence run for this model | | | | | | | | | | |
| MPP | no threehop competence run for this model | | | | | | | | | | |
| PMP | no threehop competence run for this model | | | | | | | | | | |
| PPM | no threehop competence run for this model | | | | | | | | | | |
| MPM | no threehop competence run for this model | | | | | | | | | | |
| MMP | no threehop competence run for this model | | | | | | | | | | |
| PMM | no threehop competence run for this model | | | | | | | | | | |
| MMM | no threehop competence run for this model | | | | | | | | | | |
| nPR | no numbers competence run for this model | | | | | | | | | | |
| nPL | no numbers competence run for this model | | | | | | | | | | |
| nPM | no numbers competence run for this model | | | | | | | | | | |
| nKR | no numbers competence run for this model | | | | | | | | | | |
| nKL | no numbers competence run for this model | | | | | | | | | | |
| nKM | no numbers competence run for this model | | | | | | | | | | |
| nAR | no numbers competence run for this model | | | | | | | | | | |
| nAL | no numbers competence run for this model | | | | | | | | | | |
| nAM | no numbers competence run for this model | | | | | | | | | | |
| nMR | no numbers competence run for this model | | | | | | | | | | |
| nML | no numbers competence run for this model | | | | | | | | | | |
| nMM | no numbers competence run for this model | | | | | | | | | | |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 100 / 26 / 100*, e28 (maj 35% 'insect') | 79 / 21 / 74*, e13 (maj 35% 'insect') | 71 / 47 / 44, e9 (maj 35% 'insect') |
| cities (30) | 100 / 23 / 100*, e45 (maj 12% 'Germany') | 94 / 10 / 94*, e36 (maj 12% 'Germany') | 88 / 25 / 85*, e14 (maj 12% 'Germany') |
| companies (14) | 100 / 43 / 100*, e35 (maj 14% 'Germany') | 95 / 40 / 92*, e39 (maj 14% 'Germany') | 81 / 43 / 67, e21 (maj 14% 'Germany') |
| countries (5) | 100 / 19 / 100*, e32 (maj 42% 'Europe') | 92 / 21 / 89*, e26 (maj 42% 'Europe') | 94 / 35 / 90*, e9 (maj 42% 'Europe') |
| dishes (20) | 100 / 32 / 100*, e33 (maj 16% 'Italy') | 97 / 18 / 97*, e26 (maj 16% 'Italy') | 97 / 47 / 95*, e26 (maj 16% 'Italy') |
| landmarks (27) | 100 / 24 / 100*, e33 (maj 10% 'Peru') | 93 / 26 / 90*, e29 (maj 10% 'Peru') | 71 / 40 / 52, e7 (maj 10% 'Peru') |
| languages (16) | 98 / 22 / 97*, e35 (maj 30% 'Spanish') | 88 / 2 / 87*, e22 (maj 30% 'Spanish') | 80 / 15 / 76*, e21 (maj 30% 'Spanish') |
| people (23) | 98 / 23 / 98*, e43 (maj 13% 'German') | 100 / 3 / 100*, e50 (maj 13% 'German') | 65 / 23 / 54, e13 (maj 13% 'German') |

### Nemotron 3.5 Bolt (jsuite_v2_test_chat; runs: nem35b_jsuite_v2_test_chat_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 90 | 100 | 100 | - | 32 | 8 | 16 | 85* | 292 | 0: - |
| PK | 358 | 100 | 100 | 100 | - | 27 | 8 | 21 | 100* | 292 | 0: - |
| PM | 358 | 94 | 100 | 99 | - | 13 | 8 | 21 | 93* | 292 | 0: - |
| PA | 358 | 95 | 100 | 100 | - | 46 | 8 | 21 | 91* | 292 | 1: 100 |
| PN | 358 | 96 | 100 | 99 | - | 19 | 8 | 21 | 96* | 292 | 1: 0 |
| MP | 358 | 86 | 99 | 100 | - | 37 | 8 | 16 | 78* | 298 | 4: 0 |
| MK | 358 | 98 | 99 | 100 | - | 36 | 8 | 21 | 97* | 298 | 4: 50 |
| MM | 358 | 98 | 99 | 99 | - | 4 | 8 | 21 | 98* | 298 | 4: 50 |
| MA | 358 | 99 | 99 | 99 | - | 49 | 8 | 21 | 97* | 298 | 5: 80 |
| MN | 358 | 99 | 99 | 99 | - | 11 | 8 | 21 | 98* | 298 | 4: 100 |
| TP | 358 | 50 | 93 | 99 | - | 32 | 8 | 16 | 27 | 85 | 24: 42 |
| TK | 358 | 84 | 93 | 100 | - | 34 | 8 | 21 | 75* | 85 | 25: 24 |
| TM | 358 | 63 | 94 | 98 | - | 12 | 8 | 21 | 58 | 85 | 23: 39 |
| TA | 358 | 79 | 93 | 99 | - | 43 | 8 | 21 | 63 | 85 | 26: 65 |
| TN | 358 | 66 | 93 | 100 | - | 22 | 8 | 21 | 56 | 85 | 24: 12 |
| PPP | no threehop competence run for this model | | | | | | | | | | |
| MPP | no threehop competence run for this model | | | | | | | | | | |
| PMP | no threehop competence run for this model | | | | | | | | | | |
| PPM | no threehop competence run for this model | | | | | | | | | | |
| MPM | no threehop competence run for this model | | | | | | | | | | |
| MMP | no threehop competence run for this model | | | | | | | | | | |
| PMM | no threehop competence run for this model | | | | | | | | | | |
| MMM | no threehop competence run for this model | | | | | | | | | | |
| nPR | no numbers competence run for this model | | | | | | | | | | |
| nPL | no numbers competence run for this model | | | | | | | | | | |
| nPM | no numbers competence run for this model | | | | | | | | | | |
| nKR | no numbers competence run for this model | | | | | | | | | | |
| nKL | no numbers competence run for this model | | | | | | | | | | |
| nKM | no numbers competence run for this model | | | | | | | | | | |
| nAR | no numbers competence run for this model | | | | | | | | | | |
| nAL | no numbers competence run for this model | | | | | | | | | | |
| nAM | no numbers competence run for this model | | | | | | | | | | |
| nMR | no numbers competence run for this model | | | | | | | | | | |
| nML | no numbers competence run for this model | | | | | | | | | | |
| nMM | no numbers competence run for this model | | | | | | | | | | |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 100 / 9 / 100*, e29 (maj 35% 'insect') | 97 / 0 / 97*, e30 (maj 35% 'insect') | 47 / 26 / 28, e2 (maj 35% 'insect') |
| cities (30) | 100 / 13 / 100*, e48 (maj 12% 'Germany') | 98 / 0 / 98*, e39 (maj 12% 'Germany') | 81 / 6 / 80*, e17 (maj 12% 'Germany') |
| companies (14) | 90 / 19 / 88*, e33 (maj 14% 'Germany') | 90 / 19 / 88*, e35 (maj 14% 'Germany') | 50 / 14 / 42, e11 (maj 14% 'Germany') |
| countries (5) | 100 / 6 / 100*, e40 (maj 42% 'Europe') | 98 / 4 / 98*, e35 (maj 42% 'Europe') | 71 / 2 / 70*, e12 (maj 42% 'Europe') |
| dishes (20) | 82 / 5 / 81*, e28 (maj 16% 'Italy') | 100 / 0 / 100*, e36 (maj 16% 'Italy') | 32 / 5 / 28, e8 (maj 16% 'Italy') |
| landmarks (27) | 98 / 26 / 97*, e38 (maj 10% 'Peru') | 100 / 7 / 100*, e38 (maj 10% 'Peru') | 79 / 24 / 72*, e9 (maj 10% 'Peru') |
| languages (16) | 98 / 12 / 97*, e35 (maj 30% 'Spanish') | 98 / 0 / 98*, e34 (maj 30% 'Spanish') | 78 / 20 / 72*, e14 (maj 30% 'Spanish') |
| people (23) | 84 / 13 / 81*, e41 (maj 13% 'German') | 100 / 0 / 100*, e51 (maj 13% 'German') | 58 / 5 / 56, e12 (maj 13% 'German') |

### DeepSeek V4 Flash (jsuite_v2_test_chat; runs: dsv4f_jsuite_v2_test_chat_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 82 | 100 | 99 | - | 30 | 8 | 16 | 74* | 251 | 1: 0 |
| PK | 358 | 97 | 100 | 100 | - | 26 | 8 | 21 | 97* | 251 | 0: - |
| PM | 358 | 88 | 100 | 99 | - | 11 | 8 | 21 | 86* | 251 | 0: - |
| PA | 358 | 94 | 100 | 100 | - | 51 | 8 | 21 | 89* | 251 | 1: 0 |
| PN | 358 | 94 | 100 | 99 | - | 23 | 8 | 21 | 92* | 251 | 0: - |
| MP | 358 | 71 | 99 | 97 | - | 29 | 8 | 16 | 59 | 241 | 4: 50 |
| MK | 358 | 99 | 99 | 100 | - | 28 | 8 | 21 | 98* | 241 | 3: 33 |
| MM | 358 | 96 | 99 | 99 | - | 2 | 8 | 21 | 96* | 241 | 3: 67 |
| MA | 358 | 98 | 99 | 99 | - | 45 | 8 | 21 | 97* | 241 | 2: 100 |
| MN | 358 | 98 | 100 | 100 | - | 13 | 8 | 21 | 98* | 241 | 1: 100 |
| TP | 358 | 34 | 74 | 98 | - | 24 | 8 | 16 | 13 | 14 | 92: 23 |
| TK | 358 | 47 | 81 | 100 | - | 19 | 8 | 21 | 34 | 14 | 69: 30 |
| TM | 358 | 20 | 87 | 99 | - | 4 | 8 | 21 | 17 | 14 | 47: 15 |
| TA | 358 | 61 | 87 | 100 | - | 38 | 8 | 21 | 36 | 14 | 45: 38 |
| TN | 358 | 46 | 79 | 99 | - | 19 | 8 | 21 | 33 | 14 | 76: 30 |
| PPP | no threehop competence run for this model | | | | | | | | | | |
| MPP | no threehop competence run for this model | | | | | | | | | | |
| PMP | no threehop competence run for this model | | | | | | | | | | |
| PPM | no threehop competence run for this model | | | | | | | | | | |
| MPM | no threehop competence run for this model | | | | | | | | | | |
| MMP | no threehop competence run for this model | | | | | | | | | | |
| PMM | no threehop competence run for this model | | | | | | | | | | |
| MMM | no threehop competence run for this model | | | | | | | | | | |
| nPR | no numbers competence run for this model | | | | | | | | | | |
| nPL | no numbers competence run for this model | | | | | | | | | | |
| nPM | no numbers competence run for this model | | | | | | | | | | |
| nKR | no numbers competence run for this model | | | | | | | | | | |
| nKL | no numbers competence run for this model | | | | | | | | | | |
| nKM | no numbers competence run for this model | | | | | | | | | | |
| nAR | no numbers competence run for this model | | | | | | | | | | |
| nAL | no numbers competence run for this model | | | | | | | | | | |
| nAM | no numbers competence run for this model | | | | | | | | | | |
| nMR | no numbers competence run for this model | | | | | | | | | | |
| nML | no numbers competence run for this model | | | | | | | | | | |
| nMM | no numbers competence run for this model | | | | | | | | | | |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 91 / 9 / 90*, e26 (maj 35% 'insect') | 85 / 6 / 84*, e15 (maj 35% 'insect') | 12 / 6 / 6, e0 (maj 35% 'insect') |
| cities (30) | 98 / 8 / 98*, e46 (maj 12% 'Germany') | 94 / 0 / 94*, e25 (maj 12% 'Germany') | 19 / 0 / 19, e3 (maj 12% 'Germany') |
| companies (14) | 90 / 29 / 87*, e30 (maj 14% 'Germany') | 95 / 0 / 95*, e38 (maj 14% 'Germany') | 14 / 10 / 5, e1 (maj 14% 'Germany') |
| countries (5) | 71 / 15 / 66, e24 (maj 42% 'Europe') | 98 / 0 / 98*, e20 (maj 42% 'Europe') | 31 / 6 / 27, e3 (maj 42% 'Europe') |
| dishes (20) | 71 / 5 / 69, e25 (maj 16% 'Italy') | 100 / 0 / 100*, e30 (maj 16% 'Italy') | 8 / 0 / 8, e0 (maj 16% 'Italy') |
| landmarks (27) | 100 / 7 / 100*, e32 (maj 10% 'Peru') | 100 / 12 / 100*, e35 (maj 10% 'Peru') | 29 / 5 / 25, e3 (maj 10% 'Peru') |
| languages (16) | 100 / 12 / 100*, e35 (maj 30% 'Spanish') | 98 / 2 / 97*, e27 (maj 30% 'Spanish') | 48 / 10 / 42, e4 (maj 30% 'Spanish') |
| people (23) | 82 / 6 / 81*, e33 (maj 13% 'German') | 97 / 0 / 97*, e51 (maj 13% 'German') | 6 / 2 / 5, e0 (maj 13% 'German') |

### Muse Glimmer 30B (jsuite_v2_test_chat; runs: muse30_jsuite_v2_test_chat_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 82 | 99 | 99 | - | 29 | 8 | 16 | 74* | 256 | 5: 60 |
| PK | 358 | 99 | 99 | 100 | - | 24 | 8 | 21 | 99* | 256 | 4: 100 |
| PM | 358 | 96 | 99 | 96 | - | 13 | 8 | 21 | 95* | 256 | 2: 100 |
| PA | 358 | 99 | 99 | 100 | - | 45 | 8 | 21 | 97* | 256 | 5: 100 |
| PN | 358 | 96 | 98 | 100 | - | 19 | 8 | 21 | 95* | 256 | 8: 88 |
| MP | 358 | 76 | 96 | 99 | - | 32 | 8 | 16 | 64 | 247 | 13: 46 |
| MK | 358 | 98 | 98 | 100 | - | 43 | 8 | 21 | 96* | 247 | 7: 43 |
| MM | 358 | 94 | 98 | 99 | - | 6 | 8 | 21 | 94* | 247 | 7: 57 |
| MA | 358 | 97 | 98 | 100 | - | 41 | 8 | 21 | 94* | 247 | 7: 71 |
| MN | 358 | 95 | 98 | 99 | - | 23 | 8 | 21 | 93* | 247 | 8: 50 |
| TP | 358 | 38 | 82 | 99 | - | 25 | 8 | 16 | 16 | 38 | 66: 24 |
| TK | 358 | 63 | 80 | 100 | - | 20 | 8 | 21 | 54 | 38 | 71: 32 |
| TM | 358 | 48 | 88 | 98 | - | 9 | 8 | 21 | 43 | 38 | 44: 23 |
| TA | 358 | 68 | 88 | 99 | - | 37 | 8 | 21 | 49 | 38 | 43: 42 |
| TN | 358 | 46 | 84 | 99 | - | 14 | 8 | 21 | 37 | 38 | 57: 33 |
| PPP | 118 | 19 | 95 | 94 | 99 | 26 | 20 | 27 | -9 | 21 | 6: 17 |
| MPP | 131 | 27 | 95 | 96 | 99 | 31 | 20 | 30 | -4 | 31 | 7: 29 |
| PMP | 126 | 25 | 98 | 98 | 100 | 25 | 20 | 26 | 1 | 31 | 2: 50 |
| PPM | 131 | 37 | 98 | 100 | 100 | 21 | 20 | 31 | 19 | 47 | 3: 33 |
| MPM | 121 | 21 | 95 | 98 | 100 | 21 | 20 | 29 | -1 | 24 | 6: 17 |
| MMP | 132 | 19 | 85 | 99 | 100 | 14 | 20 | 29 | 5 | 25 | 20: 0 |
| PMM | 131 | 94 | 98 | 99 | 100 | 18 | 20 | 37 | 93* | 121 | 2: 50 |
| MMM | 117 | 87 | 80 | 100 | 100 | 12 | 20 | 41 | 85* | 86 | 23: 70 |
| nPR | 53 | 100 | 100 | - | - | 28 | 11 | 21 | 100* | 53 | 0: - |
| nPL | 61 | 25 | 100 | 100 | - | 7 | 12 | 10 | 19 | 15 | 0: - |
| nPM | 61 | 44 | 100 | 95 | - | 15 | 12 | 21 | 35 | 25 | 0: - |
| nKR | 52 | 96 | 96 | - | - | 23 | 11 | 21 | 95* | 50 | 2: 0 |
| nKL | 62 | 6 | 98 | 100 | - | 3 | 12 | 8 | 3 | 4 | 1: 0 |
| nKM | 62 | 13 | 98 | 87 | - | 15 | 12 | 19 | -2 | 8 | 1: 0 |
| nAR | 58 | 98 | 97 | - | - | 31 | 11 | 19 | 97* | 56 | 2: 50 |
| nAL | 60 | 5 | 97 | 100 | - | 3 | 12 | 7 | 2 | 3 | 2: 0 |
| nAM | 60 | 13 | 97 | 88 | - | 15 | 12 | 20 | -2 | 6 | 2: 0 |
| nMR | 62 | 85 | 77 | - | - | 2 | 11 | 19 | 85* | 48 | 14: 36 |
| nML | 56 | 9 | 86 | 100 | - | 0 | 12 | 9 | 9 | 5 | 8: 0 |
| nMM | 56 | 27 | 86 | 89 | - | 16 | 12 | 21 | 13 | 13 | 8: 12 |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 94 / 12 / 93*, e28 (maj 35% 'insect') | 88 / 6 / 88*, e14 (maj 35% 'insect') | 26 / 15 / 14, e0 (maj 35% 'insect') |
| cities (30) | 100 / 13 / 100*, e46 (maj 12% 'Germany') | 94 / 2 / 94*, e32 (maj 12% 'Germany') | 73 / 2 / 73*, e15 (maj 12% 'Germany') |
| companies (14) | 98 / 10 / 97*, e36 (maj 14% 'Germany') | 100 / 5 / 100*, e40 (maj 14% 'Germany') | 36 / 5 / 32, e2 (maj 14% 'Germany') |
| countries (5) | 98 / 15 / 98*, e31 (maj 42% 'Europe') | 83 / 0 / 83*, e20 (maj 42% 'Europe') | 46 / 4 / 43, e3 (maj 42% 'Europe') |
| dishes (20) | 97 / 13 / 97*, e25 (maj 16% 'Italy') | 97 / 0 / 97*, e33 (maj 16% 'Italy') | 61 / 18 / 52, e8 (maj 16% 'Italy') |
| landmarks (27) | 98 / 17 / 97*, e31 (maj 10% 'Peru') | 98 / 33 / 96*, e32 (maj 10% 'Peru') | 60 / 17 / 51, e5 (maj 10% 'Peru') |
| languages (16) | 98 / 20 / 97*, e31 (maj 30% 'Spanish') | 95 / 8 / 95*, e28 (maj 30% 'Spanish') | 62 / 10 / 58, e3 (maj 30% 'Spanish') |
| people (23) | 89 / 10 / 88*, e28 (maj 13% 'German') | 98 / 0 / 98*, e48 (maj 13% 'German') | 24 / 6 / 19, e2 (maj 13% 'German') |

### OLMo 3 32B (QA rendering) (jsuite_v2_test_qa; runs: olmo32_jsuite_v2_test_qa_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 73 | 100 | 96 | - | 30 | 8 | 16 | 61 | 227 | 1: 0 |
| PK | 358 | 98 | 99 | 100 | - | 23 | 8 | 21 | 97* | 227 | 5: 60 |
| PM | 358 | 96 | 99 | 97 | - | 20 | 8 | 21 | 95* | 227 | 2: 50 |
| PA | 358 | 99 | 99 | 100 | - | 47 | 8 | 21 | 97* | 227 | 2: 100 |
| PN | 358 | 94 | 98 | 100 | - | 21 | 8 | 21 | 92* | 227 | 6: 83 |
| MP | 358 | 68 | 99 | 99 | - | 37 | 8 | 16 | 49 | 216 | 4: 25 |
| MK | 358 | 96 | 99 | 100 | - | 28 | 8 | 21 | 94* | 216 | 4: 25 |
| MM | 358 | 94 | 99 | 97 | - | 4 | 8 | 21 | 94* | 216 | 5: 40 |
| MA | 358 | 96 | 99 | 99 | - | 49 | 8 | 21 | 92* | 216 | 5: 40 |
| MN | 358 | 94 | 99 | 99 | - | 20 | 8 | 21 | 93* | 216 | 4: 25 |
| TP | 358 | 34 | 77 | 95 | - | 27 | 8 | 16 | 10 | 24 | 82: 23 |
| TK | 358 | 63 | 79 | 100 | - | 33 | 8 | 21 | 44 | 24 | 75: 20 |
| TM | 358 | 35 | 79 | 97 | - | 13 | 8 | 21 | 25 | 24 | 76: 13 |
| TA | 358 | 69 | 78 | 100 | - | 45 | 8 | 21 | 43 | 24 | 77: 45 |
| TN | 358 | 49 | 78 | 100 | - | 23 | 8 | 21 | 35 | 24 | 78: 23 |
| PPP | 118 | 24 | 97 | 95 | 94 | 26 | 20 | 27 | -3 | 27 | 4: 0 |
| MPP | 131 | 29 | 95 | 99 | 98 | 28 | 20 | 30 | 1 | 36 | 6: 33 |
| PMP | 126 | 40 | 99 | 98 | 99 | 17 | 20 | 26 | 27 | 49 | 1: 0 |
| PPM | 131 | 30 | 99 | 94 | 100 | 20 | 20 | 31 | 12 | 39 | 1: 0 |
| MPM | 121 | 31 | 95 | 99 | 100 | 28 | 20 | 29 | 5 | 35 | 6: 50 |
| MMP | 132 | 36 | 92 | 98 | 98 | 27 | 20 | 29 | 13 | 44 | 11: 27 |
| PMM | 131 | 92 | 92 | 99 | 100 | 10 | 20 | 37 | 91* | 110 | 11: 91 |
| MMM | 117 | 91 | 92 | 97 | 100 | 8 | 20 | 41 | 91* | 103 | 9: 11 |
| nPR | 53 | 100 | 75 | - | - | 100 | 11 | 21 | - | 40 | 13: 100 |
| nPL | 61 | 34 | 84 | 100 | - | 18 | 12 | 10 | 20 | 17 | 10: 40 |
| nPM | 61 | 66 | 84 | 100 | - | 18 | 12 | 21 | 58 | 33 | 10: 70 |
| nKR | 52 | 100 | 6 | - | - | 100 | 11 | 21 | - | 3 | 49: 100 |
| nKL | 62 | 11 | 13 | 100 | - | 11 | 12 | 8 | 0 | 0 | 54: 13 |
| nKM | 62 | 34 | 13 | 100 | - | 15 | 12 | 19 | 23 | 1 | 54: 37 |
| nAR | 58 | 100 | 88 | - | - | 100 | 11 | 19 | - | 51 | 7: 100 |
| nAL | 60 | 17 | 92 | 100 | - | 22 | 12 | 7 | -6 | 9 | 5: 20 |
| nAM | 60 | 12 | 92 | 100 | - | 13 | 12 | 20 | -2 | 6 | 5: 20 |
| nMR | 62 | 100 | 2 | - | - | 100 | 11 | 19 | - | 1 | 61: 100 |
| nML | 56 | 43 | 0 | 100 | - | 9 | 12 | 9 | 37 | 0 | 56: 43 |
| nMM | 56 | 39 | 0 | 96 | - | 2 | 12 | 21 | 38 | 0 | 56: 39 |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 97 / 15 / 97*, e22 (maj 35% 'insect') | 79 / 6 / 78*, e12 (maj 35% 'insect') | 29 / 21 / 11, e1 (maj 35% 'insect') |
| cities (30) | 100 / 21 / 100*, e43 (maj 12% 'Germany') | 94 / 0 / 94*, e36 (maj 12% 'Germany') | 42 / 12 / 35, e6 (maj 12% 'Germany') |
| companies (14) | 95 / 24 / 94*, e30 (maj 14% 'Germany') | 98 / 5 / 98*, e29 (maj 14% 'Germany') | 31 / 5 / 28, e2 (maj 14% 'Germany') |
| countries (5) | 100 / 17 / 100*, e30 (maj 42% 'Europe') | 92 / 8 / 91*, e28 (maj 42% 'Europe') | 54 / 15 / 46, e5 (maj 42% 'Europe') |
| dishes (20) | 87 / 16 / 84*, e21 (maj 16% 'Italy') | 97 / 0 / 97*, e19 (maj 16% 'Italy') | 3 / 8 / -6, e0 (maj 16% 'Italy') |
| landmarks (27) | 98 / 26 / 97*, e22 (maj 10% 'Peru') | 95 / 5 / 95*, e30 (maj 10% 'Peru') | 50 / 26 / 32, e4 (maj 10% 'Peru') |
| languages (16) | 98 / 25 / 97*, e21 (maj 30% 'Spanish') | 100 / 2 / 100*, e24 (maj 30% 'Spanish') | 60 / 10 / 56, e6 (maj 30% 'Spanish') |
| people (23) | 94 / 16 / 92*, e38 (maj 13% 'German') | 95 / 3 / 95*, e38 (maj 13% 'German') | 13 / 11 / 2, e0 (maj 13% 'German') |

### Qwen3.5 122B-A10B (jsuite_v2_test_chat; runs: qwen35_122b_jsuite_v2_test_chat_competence_cand2_v1)

| word | n | whole | h1 | h2 | h3 | guess | chance | maj | real | elig | h1x: whole right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 358 | 93 | 100 | 100 | - | 32 | 8 | 16 | 89* | 327 | 0: - |
| PK | 358 | 100 | 100 | 100 | - | 22 | 8 | 21 | 100* | 327 | 0: - |
| PM | 358 | 99 | 100 | 100 | - | 23 | 8 | 21 | 99* | 327 | 0: - |
| PA | 358 | 100 | 100 | 100 | - | 32 | 8 | 21 | 100* | 327 | 0: - |
| PN | 358 | 99 | 100 | 100 | - | 19 | 8 | 21 | 99* | 327 | 0: - |
| MP | 358 | 86 | 99 | 100 | - | 45 | 8 | 16 | 74* | 301 | 2: 0 |
| MK | 358 | 99 | 100 | 100 | - | 46 | 8 | 21 | 98* | 301 | 1: 0 |
| MM | 358 | 98 | 100 | 100 | - | 22 | 8 | 21 | 97* | 301 | 1: 0 |
| MA | 358 | 99 | 100 | 100 | - | 54 | 8 | 21 | 99* | 301 | 1: 0 |
| MN | 358 | 99 | 99 | 100 | - | 31 | 8 | 21 | 98* | 301 | 3: 33 |
| TP | 358 | 56 | 96 | 99 | - | 32 | 8 | 16 | 36 | 156 | 13: 23 |
| TK | 358 | 91 | 97 | 100 | - | 37 | 8 | 21 | 86* | 156 | 11: 18 |
| TM | 358 | 89 | 97 | 100 | - | 28 | 8 | 21 | 84* | 156 | 12: 33 |
| TA | 358 | 92 | 97 | 100 | - | 45 | 8 | 21 | 85* | 156 | 10: 50 |
| TN | 358 | 85 | 96 | 100 | - | 30 | 8 | 21 | 79* | 156 | 16: 50 |
| PPP | 118 | 28 | 100 | 100 | 100 | 33 | 20 | 27 | -8 | 33 | 0: - |
| MPP | 131 | 39 | 96 | 100 | 100 | 32 | 20 | 30 | 10 | 50 | 5: 20 |
| PMP | 126 | 39 | 100 | 99 | 100 | 39 | 20 | 26 | 0 | 49 | 0: - |
| PPM | 131 | 57 | 100 | 100 | 100 | 22 | 20 | 31 | 45 | 75 | 0: - |
| MPM | 121 | 56 | 98 | 100 | 100 | 25 | 20 | 29 | 42 | 68 | 3: 0 |
| MMP | 132 | 39 | 87 | 98 | 100 | 39 | 20 | 29 | 0 | 44 | 17: 41 |
| PMM | 131 | 96 | 100 | 99 | 100 | 27 | 20 | 37 | 95* | 126 | 0: - |
| MMM | 117 | 94 | 85 | 100 | 100 | 15 | 20 | 41 | 93* | 98 | 18: 67 |
| nPR | 53 | 100 | 100 | - | - | 25 | 11 | 21 | 100* | 53 | 0: - |
| nPL | 61 | 33 | 100 | 100 | - | 8 | 12 | 10 | 27 | 20 | 0: - |
| nPM | 61 | 61 | 100 | 95 | - | 15 | 12 | 21 | 54 | 36 | 0: - |
| nKR | 52 | 100 | 100 | - | - | 2 | 11 | 21 | 100* | 52 | 0: - |
| nKL | 62 | 16 | 100 | 100 | - | 10 | 12 | 8 | 7 | 10 | 0: - |
| nKM | 62 | 39 | 100 | 97 | - | 5 | 12 | 19 | 36 | 24 | 0: - |
| nAR | 58 | 100 | 100 | - | - | 3 | 11 | 19 | 100* | 58 | 0: - |
| nAL | 60 | 23 | 100 | 100 | - | 13 | 12 | 7 | 12 | 14 | 0: - |
| nAM | 60 | 40 | 100 | 90 | - | 3 | 12 | 20 | 38 | 23 | 0: - |
| nMR | 62 | 100 | 100 | - | - | 5 | 11 | 19 | 100* | 62 | 0: - |
| nML | 56 | 20 | 100 | 100 | - | 12 | 12 | 9 | 8 | 11 | 0: - |
| nMM | 56 | 36 | 100 | 89 | - | 14 | 12 | 21 | 25 | 20 | 0: - |

Per relation, recalled-final words (whole / guess / real, eligible n; k = candidates):

| relation (k) | PM | MM | TM |
|---|---|---|---|
| animals (6) | 100 / 12 / 100*, e31 (maj 35% 'insect') | 100 / 15 / 100*, e31 (maj 35% 'insect') | 91 / 47 / 83*, e12 (maj 35% 'insect') |
| cities (30) | 100 / 19 / 100*, e51 (maj 12% 'Germany') | 98 / 8 / 98*, e35 (maj 12% 'Germany') | 94 / 17 / 93*, e23 (maj 12% 'Germany') |
| companies (14) | 100 / 36 / 100*, e40 (maj 14% 'Germany') | 100 / 21 / 100*, e42 (maj 14% 'Germany') | 86 / 36 / 78*, e21 (maj 14% 'Germany') |
| countries (5) | 100 / 23 / 100*, e42 (maj 42% 'Europe') | 98 / 54 / 95*, e34 (maj 42% 'Europe') | 100 / 8 / 100*, e23 (maj 42% 'Europe') |
| dishes (20) | 97 / 16 / 97*, e36 (maj 16% 'Italy') | 89 / 26 / 86*, e29 (maj 16% 'Italy') | 87 / 26 / 82*, e22 (maj 16% 'Italy') |
| landmarks (27) | 100 / 31 / 100*, e38 (maj 10% 'Peru') | 100 / 52 / 100*, e41 (maj 10% 'Peru') | 90 / 40 / 84*, e17 (maj 10% 'Peru') |
| languages (16) | 98 / 28 / 97*, e35 (maj 30% 'Spanish') | 98 / 2 / 97*, e33 (maj 30% 'Spanish') | 92 / 30 / 89*, e16 (maj 30% 'Spanish') |
| people (23) | 98 / 18 / 98*, e54 (maj 13% 'German') | 100 / 3 / 100*, e56 (maj 13% 'German') | 74 / 29 / 64, e22 (maj 13% 'German') |

