# C2 re-score (scripts: /workspace/scratch/c2_rescore.py; rule in its docstring)

Fixed-cell cross-validated flips to C's answer (%), one cell per pair, chosen on half the bridges and scored on the other half, cells gated on random-control keep >= 95% AND own breakage <= 10%. [95% bootstrap over bridges]. D = recall word - lookup word at the same cell.

| model | run | n MP/MM, PP/PM, CP/CM | eligible cells M/P/C | M->P vs M->M (D) | ceilings MP/MM; raw relative | P: PP vs PM (D) | C: CP vs CM (D) | C2-graded old -> new | C2-relative old -> new | C2' old -> new |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | wm2_suite_v1 | 60/60, 60/60, - | 121/116/- | 1 vs 52 (D 51 [30, 73]) | 65/59; 0.02/0.89 | 0 vs 57 (D 57 [38, 72]) | - | HOLDS (8/65) -> HOLDS | HOLDS -> HOLDS | not scored -> n/a (no C words) |
| Qwen3.6-27B | wm2_ctrl_v1 | 24/24, 34/34, - | 95/101/- | 37 vs 54 (D 17 [3, 30]) | 21/6; 1.78/8.59 **>1** | 0 vs 18 (D 18 [3, 34]) | - | FAILS (38/54) -> FAILS | None -> inconclusive (ceiling < 0.5) | not scored -> n/a |
| Qwen3.6-27B | wm2_full2_v1 | 40/40, 40/40, 40/40 | 113/107/114 | 22 vs 36 (D 14 [-0, 29]) | 30/26; 0.73/1.36 **>1** | 0 vs 5 (D 5 [0, 12]) | 0 vs 13 (D 13 [2, 24]) | FAILS (30/45) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | not scored -> PARTIAL |
| Qwen3.6-27B | wm2_full2_v2 | 72/72, 87/87, 82/82 | 110/108/113 | 22 vs 28 (D 7 [-0, 21]) | 57/17; 0.38/1.66 **>1** | 0 vs 10 (D 10 [2, 16]) | 0 vs 18 (D 18 [8, 30]) | FAILS (36/40) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | HOLDS -> PARTIAL |
| Qwen3.6-27B | wm2_full2_aligned_v1 | 72/72, 87/87, 82/82 | 102/118/115 | 0 vs 7 (D 7 [0, 12]) | 71/91; 0.00/0.07 | 0 vs 9 (D 9 [4, 17]) | 0 vs 18 (D 18 [8, 29]) | FAILS (0/19) -> FAILS | FAILS -> FAILS | HOLDS -> PARTIAL |
| Qwen3-32B | qwen3_32b_wm2_full2_v1 | 40/40, 55/55, 52/52 | 118/101/117 | 2 vs 2 (D -0 [-5, 9]) | 2/3; 0.79/0.61 | 0 vs 0 (D 0 [0, 0]) | 0 vs 0 (D 0 [0, 3]) | FAILS (12/10) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | FAILS -> FAILS |
| Qwen3-32B | qwen3_32b_wm2_full2_aligned_v1 | 40/40, 55/55, 52/52 | 111/92/103 | 2 vs 38 (D 36 [12, 51]) | 98/96; 0.03/0.39 | 0 vs 0 (D 0 [0, 0]) | 0 vs 0 (D 0 [0, 0]) | HOLDS (8/75) -> HOLDS | HOLDS -> FAILS | HOLDS -> FAILS |
| Muse Glimmer 30B | muse30_wm2_full2_v1 | 48/48, 60/60, 48/48 | 98/95/93 | 0 vs 38 (D 38 [10, 52]) | 96/85; 0.00/0.45 | 0 vs 4 (D 4 [0, 11]) | 0 vs 0 (D 0 [0, 0]) | HOLDS (6/56) -> HOLDS | HOLDS -> FAILS | FAILS -> FAILS |
| Muse Glimmer 30B | muse30_wm2_full2_aligned_v1 | 48/48, 60/60, 48/48 | 97/91/96 | 0 vs 12 (D 12 [3, 25]) | 97/80; 0.00/0.15 | 0 vs 7 (D 7 [1, 15]) | 0 vs 1 (D 1 [0, 3]) | HOLDS (10/50) -> FAILS | HOLDS -> FAILS | FAILS -> FAILS |
| Muse Glimmer 30B | muse30_wm2_fresh2_v1 | 43/43, 52/52, 52/52 | 92/85/95 | 1 vs 9 (D 8 [0, 19]) | 98/86; 0.01/0.10 | 0 vs 2 (D 2 [0, 7]) | 0 vs 13 (D 13 [2, 23]) | FAILS (9/42) -> FAILS | FAILS -> FAILS | HOLDS -> PARTIAL |
| Qwen3.5-9B | qwen35_9b_wm2_full2_v1 | 25/25, 58/58, 48/48 | 110/102/111 | 0 vs 46 (D 46 [18, 73]) | 73/68; 0.00/0.67 | 0 vs 13 (D 13 [5, 23]) | 0 vs 5 (D 5 [0, 12]) | HOLDS (8/72) -> HOLDS | HOLDS -> HOLDS | HOLDS -> PARTIAL |
| Qwen3.5-9B | qwen35_9b_wm2_full2_aligned_v1 | 25/25, 58/58, 48/48 | 109/99/111 | 0 vs 51 (D 51 [14, 68]) | 78/61; 0.00/0.83 | 0 vs 8 (D 8 [1, 16]) | 0 vs 4 (D 4 [0, 10]) | HOLDS (8/68) -> HOLDS | HOLDS -> HOLDS | PARTIAL -> FAILS |
| Qwen3.5-9B | qwen35_9b_wm2_fresh2_v1 | 18/18, 59/59, 48/48 | 107/102/111 | 0 vs 61 (D 61 [19, 87]) | 73/78; 0.00/0.79 | 0 vs 8 (D 8 [1, 15]) | 0 vs 20 (D 20 [2, 34]) | HOLDS (6/61) -> HOLDS | HOLDS -> HOLDS | PARTIAL -> PARTIAL |
| Qwen3.5-122B-A10B | qwen35_122b_wm2_full2_v1 | 75/75, 78/78, 80/80 | 166/149/167 | 15 vs 12 (D -2 [-12, 9]) | 9/3; 1.69/4.11 **>1** | 0 vs 5 (D 5 [0, 11]) | 0 vs 3 (D 3 [0, 6]) | FAILS (28/39) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | FAILS -> FAILS |
| Qwen3.5-122B-A10B | qwen35_122b_wm2_full2_aligned_v1 | 75/75, 78/78, 80/80 | 118/113/117 | 0 vs 29 (D 29 [13, 43]) | 97/100; 0.00/0.29 | 0 vs 17 (D 17 [8, 26]) | 0 vs 51 (D 51 [40, 64]) | HOLDS (0/39) -> FAILS | FAILS -> FAILS | not scored -> HOLDS |
| Olmo-3-7B | olmo3d7_wm2_full2_v1 | 11/11, 19/19, 15/15 | 101/98/97 | 0 vs 0 (D 0 [0, 0]) | 92/81; 0.00/0.00 | 0 vs 3 (D 3 [0, 10]) | 0 vs 0 (D 0 [0, 0]) | HOLDS (0/36) -> FAILS | FAILS -> FAILS | UNDERPOWERED -> UNDERPOWERED |
| Olmo-3-7B | olmo3d7_wm2_full2_aligned_v1 | 11/11, 19/19, 15/15 | 101/95/99 | 0 vs 0 (D 0 [0, 0]) | 92/81; 0.00/0.00 | 0 vs 3 (D 3 [0, 10]) | 0 vs 0 (D 0 [0, 0]) | FAILS (0/9) -> FAILS | FAILS -> FAILS | UNDERPOWERED -> UNDERPOWERED |
| Olmo-Hybrid-7B | olmoh7_wm2_full2_v1 | 17/17, 20/20, 17/17 | 68/89/90 | 0 vs 21 (D 21 [0, 33]) | 89/73; 0.00/0.29 | 0 vs 1 (D 1 [0, 7]) | 0 vs 18 (D 18 [0, 35]) | FAILS (6/41) -> FAILS | FAILS -> FAILS | UNDERPOWERED -> UNDERPOWERED |
| Olmo-Hybrid-7B | olmoh7_wm2_full2_aligned_v1 | 17/17, 20/20, 17/17 | 63/92/96 | 0 vs 20 (D 20 [0, 43]) | 89/59; 0.00/0.34 | 0 vs 1 (D 1 [0, 7]) | 0 vs 16 (D 16 [0, 33]) | HOLDS (6/59) -> FAILS | HOLDS -> FAILS | UNDERPOWERED -> UNDERPOWERED |
| gpt-oss-20b (our J++) | gptoss20_wm2_full2_v1 | 11/11, 25/25, 23/23 | 74/53/67 | 0 vs 0 (D 0 [0, 0]) | 0/12; -/0.00 | 0 vs 0 (D 0 [0, 0]) | 0 vs 2 (D 2 [0, 14]) | FAILS (0/27) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | UNDERPOWERED -> UNDERPOWERED |
| gpt-oss-20b (our J++) | gptoss20_wm2_full2_aligned_v1 | 11/11, 25/25, 23/23 | 49/30/45 | 0 vs 0 (D 0 [0, 0]) | 95/77; 0.00/0.00 | 0 vs 0 (D 0 [0, 0]) | 0 vs 4 (D 4 [0, 12]) | FAILS (9/27) -> FAILS | FAILS -> FAILS | not scored -> UNDERPOWERED |
| gpt-oss-20b (J-lens) | gptoss20j_wm2_full2_v1 | 11/11, 25/25, 23/23 | 72/48/66 | 0 vs 0 (D 0 [0, 0]) | 0/12; -/0.00 | 0 vs 0 (D 0 [0, 0]) | 0 vs 4 (D 4 [0, 15]) | FAILS (0/9) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | UNDERPOWERED -> UNDERPOWERED |
| gpt-oss-20b (J-lens) | gptoss20j_wm2_full2_aligned_v1 | 11/11, 25/25, 23/23 | 45/27/40 | 0 vs 1 (D 1 [0, 14]) | 95/77; 0.00/0.01 | 0 vs 0 (D 0 [0, 0]) | 0 vs 4 (D 4 [0, 15]) | FAILS (18/27) -> FAILS | FAILS -> FAILS | not scored -> UNDERPOWERED |

## Cells surviving the gates (own lens direction cells at question/final, per word: total / gate A / A and B)

- wm2_suite_v1: RL 128/126/122, RR 128/126/121, BL 128/125/122, BR 128/126/116
- wm2_ctrl_v1: MP 128/122/110, MM 128/124/103, PP 128/124/121, PM 128/116/101
- wm2_full2_v1: MP 128/124/119, MM 128/124/114, PP 128/125/122, PM 128/121/107, CP 128/126/121, CM 128/120/114
- wm2_full2_v2: MP 128/125/117, MM 128/121/112, PP 128/125/121, PM 128/120/108, CP 128/126/122, CM 128/123/113
- wm2_full2_aligned_v1: MP 128/126/123, MM 128/117/102, PP 128/126/122, PM 128/122/118, CP 128/126/123, CM 128/120/115
- qwen3_32b_wm2_full2_v1: MP 128/121/119, MM 128/126/122, PP 128/124/119, PM 128/104/101, CP 128/126/122, CM 128/119/117
- qwen3_32b_wm2_full2_aligned_v1: MP 128/122/122, MM 128/118/112, PP 128/125/124, PM 128/96/92, CP 128/126/124, CM 128/108/103
- muse30_wm2_full2_v1: MP 112/107/101, MM 112/105/99, PP 112/108/103, PM 112/97/95, CP 112/110/105, CM 112/98/93
- muse30_wm2_full2_aligned_v1: MP 112/104/100, MM 112/105/98, PP 112/107/103, PM 112/97/91, CP 112/110/104, CM 112/99/96
- muse30_wm2_fresh2_v1: MP 112/100/97, MM 112/103/95, PP 112/103/100, PM 112/91/85, CP 112/108/106, CM 112/99/95
- qwen35_9b_wm2_full2_v1: MP 128/115/114, MM 128/125/118, PP 128/121/120, PM 128/103/102, CP 128/126/124, CM 128/115/111
- qwen35_9b_wm2_full2_aligned_v1: MP 128/115/113, MM 128/123/118, PP 128/120/119, PM 128/102/99, CP 128/126/124, CM 128/113/111
- qwen35_9b_wm2_fresh2_v1: MP 128/120/118, MM 128/121/112, PP 128/121/120, PM 128/108/102, CP 128/126/124, CM 128/114/111
- qwen35_122b_wm2_full2_v1: MP 176/172/169, MM 176/173/166, PP 176/173/156, PM 176/159/149, CP 176/174/170, CM 176/173/167
- qwen35_122b_wm2_full2_aligned_v1: MP 128/128/124, MM 128/124/119, PP 128/128/125, PM 128/117/113, CP 128/128/125, CM 128/121/117
- olmo3d7_wm2_full2_v1: MP 128/110/110, MM 128/113/109, PP 128/121/115, PM 128/104/99, CP 128/124/123, CM 128/98/97
- olmo3d7_wm2_full2_aligned_v1: MP 128/107/107, MM 128/117/113, PP 128/117/108, PM 128/104/98, CP 128/122/121, CM 128/104/103
- olmoh7_wm2_full2_v1: MP 128/84/83, MM 128/103/100, PP 128/114/113, PM 128/94/89, CP 128/119/119, CM 128/93/92
- olmoh7_wm2_full2_aligned_v1: MP 128/75/73, MM 128/108/104, PP 128/113/113, PM 128/98/93, CP 128/120/120, CM 128/101/98
- gptoss20_wm2_full2_v1: MP 112/94/75, MM 112/97/84, PP 112/101/71, PM 112/78/53, CP 112/102/80, CM 112/90/68
- gptoss20_wm2_full2_aligned_v1: MP 96/77/55, MM 96/73/50, PP 96/81/47, PM 96/67/30, CP 96/83/56, CM 96/72/45
- gptoss20j_wm2_full2_v1: MP 112/94/77, MM 112/97/81, PP 112/101/70, PM 112/77/48, CP 112/102/76, CM 112/90/66
- gptoss20j_wm2_full2_aligned_v1: MP 96/77/56, MM 96/72/47, PP 96/81/44, PM 96/63/27, CP 96/83/47, CM 96/70/41

## Stacked joint writes (modal CV cell per pair; bounds on the added norm / |h| at the band's last layer)

- wm2_suite_v1 (n_L=13; natural top-1 J share L32 0.083): lens_add final joint a=0.05: <= 0.65 (orthogonal 0.18); lens_add question L36 a=0.8: single layer: alpha x |h| added once
- wm2_ctrl_v1 (n_L=13; natural top-1 J share L32 0.083): lens_add question L34 a=0.8: single layer: alpha x |h| added once; lens_add final L40 a=0.8: single layer: alpha x |h| added once
- wm2_full2_v1 (n_L=13; natural top-1 J share L32 0.083): lens_add question L30 a=0.8: single layer: alpha x |h| added once; lens_add final L34 a=0.8: single layer: alpha x |h| added once; lens_add final L36 a=0.8: single layer: alpha x |h| added once
- wm2_full2_v2 (n_L=13; natural top-1 J share L32 0.083): lens_add question L34 a=0.8: single layer: alpha x |h| added once; lens_add final L34 a=0.8: single layer: alpha x |h| added once; lens_add final L38 a=0.8: single layer: alpha x |h| added once
- wm2_full2_aligned_v1 (n_L=13; natural top-1 J share L40 0.111): lens_add question L50 a=0.8: single layer: alpha x |h| added once; lens_add final L52 a=0.8: single layer: alpha x |h| added once; lens_add final L54 a=0.8: single layer: alpha x |h| added once
- qwen3_32b_wm2_full2_v1 (n_L=13; natural top-1 J share L32 0.067): lens_add question L34 a=0.8: single layer: alpha x |h| added once; lens_add question joint a=0.05: <= 0.65 (orthogonal 0.18); lens_add question L30 a=0.8: single layer: alpha x |h| added once
- qwen3_32b_wm2_full2_aligned_v1 (n_L=13; natural top-1 J share L40 0.075): lens_add final L46 a=0.8: single layer: alpha x |h| added once; lens_add final L40 a=0.05: single layer: alpha x |h| added once; lens_add final L52 a=0.2: single layer: alpha x |h| added once
- muse30_wm2_full2_v1 (n_L=11; natural top-1 J share L29 0.083): lens_add final L33 a=0.4: single layer: alpha x |h| added once; lens_add question L25 a=0.4: single layer: alpha x |h| added once; lens_add final L27 a=0.4: single layer: alpha x |h| added once
- muse30_wm2_full2_aligned_v1 (n_L=11; natural top-1 J share L26 0.076): lens_add final L32 a=0.4: single layer: alpha x |h| added once; lens_add question L22 a=0.4: single layer: alpha x |h| added once; lens_add final L32 a=0.4: single layer: alpha x |h| added once
- muse30_wm2_fresh2_v1 (n_L=11; natural top-1 J share L29 0.083): lens_add final L33 a=0.4: single layer: alpha x |h| added once; lens_add question L25 a=0.4: single layer: alpha x |h| added once; lens_add final L33 a=0.4: single layer: alpha x |h| added once
- qwen35_9b_wm2_full2_v1 (n_L=7; natural top-1 J share L16 0.096): lens_add final L18 a=0.8: single layer: alpha x |h| added once; lens_add final joint a=0.1: <= 0.70 (orthogonal 0.26); lens_add final L19 a=0.4: single layer: alpha x |h| added once
- qwen35_9b_wm2_full2_aligned_v1 (n_L=7; natural top-1 J share L16 0.096): lens_add final L18 a=0.8: single layer: alpha x |h| added once; lens_add final joint a=0.1: <= 0.70 (orthogonal 0.26); lens_add final L18 a=0.4: single layer: alpha x |h| added once
- qwen35_9b_wm2_fresh2_v1 (n_L=7; natural top-1 J share L16 0.096): lens_add final L18 a=0.8: single layer: alpha x |h| added once; lens_add final L20 a=0.4: single layer: alpha x |h| added once; lens_add final joint a=0.1: <= 0.70 (orthogonal 0.26)
- qwen35_122b_wm2_full2_v1 (n_L=10): lens_add question L30 a=0.4: single layer: alpha x |h| added once; lens_add question L23 a=0.4: single layer: alpha x |h| added once; lens_add final L25 a=0.8: single layer: alpha x |h| added once
- qwen35_122b_wm2_full2_aligned_v1 (n_L=7): lens_add final L40 a=0.8: single layer: alpha x |h| added once; lens_add final L42 a=0.4: single layer: alpha x |h| added once; lens_add final L41 a=0.8: single layer: alpha x |h| added once
- olmo3d7_wm2_full2_v1 (n_L=7): lens_swap final L20 a=4: lens_swap: size not logged (n/a); lens_swap final Ljoint a=2: lens_swap: size not logged (n/a); lens_add final L18 a=0.4: single layer: alpha x |h| added once
- olmo3d7_wm2_full2_aligned_v1 (n_L=7): lens_add final L12 a=0.05: single layer: alpha x |h| added once; lens_swap final Ljoint a=4: lens_swap: size not logged (n/a); lens_add final L13 a=0.8: single layer: alpha x |h| added once
- olmoh7_wm2_full2_v1 (n_L=7; natural top-1 J share L17 0.044): lens_swap final L19 a=4: lens_swap: size not logged (n/a); lens_swap final L19 a=4: lens_swap: size not logged (n/a); lens_add final L20 a=0.4: single layer: alpha x |h| added once
- olmoh7_wm2_full2_aligned_v1 (n_L=7; natural top-1 J share L16 0.054): lens_add final joint a=0.1: <= 0.70 (orthogonal 0.26); lens_swap final L19 a=4: lens_swap: size not logged (n/a); lens_add final L19 a=0.4: single layer: alpha x |h| added once
- gptoss20_wm2_full2_v1 (n_L=6; natural top-1 J share L13 0.069): lens_add final L12 a=0.1: single layer: alpha x |h| added once; lens_add final L10 a=0.05: single layer: alpha x |h| added once; lens_add final L10 a=0.05: single layer: alpha x |h| added once
- gptoss20_wm2_full2_aligned_v1 (n_L=5; natural top-1 J share L13 0.069): lens_add question L17 a=0.4: single layer: alpha x |h| added once; lens_add final L15 a=0.05: single layer: alpha x |h| added once; lens_add question L16 a=0.2: single layer: alpha x |h| added once
- gptoss20j_wm2_full2_v1 (n_L=6; natural top-1 J share L13 0.069): lens_add final L10 a=0.2: single layer: alpha x |h| added once; lens_add final L10 a=0.05: single layer: alpha x |h| added once; lens_add final L10 a=0.05: single layer: alpha x |h| added once
- gptoss20j_wm2_full2_aligned_v1 (n_L=5; natural top-1 J share L13 0.069): lens_add final L15 a=0.1: single layer: alpha x |h| added once; lens_add final L15 a=0.05: single layer: alpha x |h| added once; lens_add final L17 a=0.05: single layer: alpha x |h| added once

## Reading check: old per-word best gated own-direction flips (c2_graded) vs recomputed here

- wm2_suite_v1: all match
- wm2_ctrl_v1: all match
- wm2_full2_v1: all match
- wm2_full2_v2: all match
- wm2_full2_aligned_v1: all match
- qwen3_32b_wm2_full2_v1: all match
- qwen3_32b_wm2_full2_aligned_v1: all match
- muse30_wm2_full2_v1: all match
- muse30_wm2_full2_aligned_v1: all match
- muse30_wm2_fresh2_v1: all match
- qwen35_9b_wm2_full2_v1: all match
- qwen35_9b_wm2_full2_aligned_v1: all match
- qwen35_9b_wm2_fresh2_v1: all match
- qwen35_122b_wm2_full2_v1: all match
- qwen35_122b_wm2_full2_aligned_v1: all match
- olmo3d7_wm2_full2_v1: all match
- olmo3d7_wm2_full2_aligned_v1: all match
- olmoh7_wm2_full2_v1: all match
- olmoh7_wm2_full2_aligned_v1: all match
- gptoss20_wm2_full2_v1: all match
- gptoss20_wm2_full2_aligned_v1: all match
- gptoss20j_wm2_full2_v1: all match
- gptoss20j_wm2_full2_aligned_v1: all match
