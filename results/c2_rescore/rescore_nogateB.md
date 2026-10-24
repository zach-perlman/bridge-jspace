# C2 re-score (scripts: /workspace/scratch/c2_rescore.py; rule in its docstring)

Fixed-cell cross-validated flips to C's answer (%), one cell per pair, chosen on half the bridges and scored on the other half, cells gated on random-control keep >= 95% AND own breakage <= 10%. [95% bootstrap over bridges]. D = recall word - lookup word at the same cell.

| model | run | n MP/MM, PP/PM, CP/CM | eligible cells M/P/C | M->P vs M->M (D) | ceilings MP/MM; raw relative | P: PP vs PM (D) | C: CP vs CM (D) | C2-graded old -> new | C2-relative old -> new | C2' old -> new |
|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | wm2_suite_v1 | 60/60, 60/60, - | 126/125/- | 1 vs 52 (D 51 [30, 73]) | 65/59; 0.02/0.89 | 1 vs 53 (D 52 [38, 65]) | - | HOLDS (8/65) -> HOLDS | HOLDS -> HOLDS | not scored -> n/a (no C words) |
| Qwen3.6-27B | wm2_ctrl_v1 | 24/24, 34/34, - | 120/116/- | 35 vs 49 (D 14 [0, 29]) | 21/6; 1.69/7.78 **>1** | 0 vs 17 (D 17 [7, 35]) | - | FAILS (38/54) -> FAILS | None -> inconclusive (ceiling < 0.5) | not scored -> n/a |
| Qwen3.6-27B | wm2_full2_v1 | 40/40, 40/40, 40/40 | 123/121/120 | 26 vs 37 (D 10 [-1, 28]) | 30/26; 0.87/1.39 **>1** | 0 vs 12 (D 12 [3, 23]) | 0 vs 12 (D 12 [2, 22]) | FAILS (30/45) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | not scored -> HOLDS |
| Qwen3.6-27B | wm2_full2_v2 | 72/72, 87/87, 82/82 | 121/120/123 | 32 vs 35 (D 3 [-10, 20]) | 57/17; 0.57/2.08 **>1** | 1 vs 19 (D 18 [8, 25]) | 0 vs 18 (D 18 [7, 29]) | FAILS (36/40) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | HOLDS -> HOLDS |
| Qwen3.6-27B | wm2_full2_aligned_v1 | 72/72, 87/87, 82/82 | 117/122/120 | 0 vs 14 (D 14 [2, 29]) | 71/91; 0.00/0.15 | 0 vs 10 (D 10 [4, 18]) | 0 vs 18 (D 18 [10, 29]) | FAILS (0/19) -> FAILS | FAILS -> FAILS | HOLDS -> HOLDS |
| Qwen3-32B | qwen3_32b_wm2_full2_v1 | 40/40, 55/55, 52/52 | 121/104/119 | 3 vs 1 (D -2 [-8, 8]) | 2/3; 1.35/0.58 **>1** | 4 vs 16 (D 13 [1, 21]) | 1 vs 2 (D 1 [-1, 6]) | FAILS (12/10) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | FAILS -> PARTIAL |
| Qwen3-32B | qwen3_32b_wm2_full2_aligned_v1 | 40/40, 55/55, 52/52 | 117/96/108 | 2 vs 75 (D 72 [45, 87]) | 98/96; 0.03/0.77 | 0 vs 24 (D 24 [13, 33]) | 0 vs 29 (D 29 [16, 39]) | HOLDS (8/75) -> HOLDS | HOLDS -> HOLDS | HOLDS -> HOLDS |
| Muse Glimmer 30B | muse30_wm2_full2_v1 | 48/48, 60/60, 48/48 | 105/97/98 | 4 vs 52 (D 48 [15, 65]) | 96/85; 0.04/0.61 | 0 vs 17 (D 17 [5, 27]) | 0 vs 15 (D 15 [2, 30]) | HOLDS (6/56) -> HOLDS | HOLDS -> HOLDS | FAILS -> HOLDS |
| Muse Glimmer 30B | muse30_wm2_full2_aligned_v1 | 48/48, 60/60, 48/48 | 102/97/99 | 4 vs 48 (D 44 [11, 61]) | 97/80; 0.04/0.60 | 0 vs 8 (D 8 [1, 17]) | 2 vs 15 (D 13 [0, 28]) | HOLDS (10/50) -> HOLDS | HOLDS -> HOLDS | FAILS -> PARTIAL |
| Muse Glimmer 30B | muse30_wm2_fresh2_v1 | 43/43, 52/52, 52/52 | 97/91/99 | 1 vs 9 (D 8 [-0, 18]) | 98/86; 0.01/0.10 | 0 vs 17 (D 17 [4, 31]) | 2 vs 18 (D 16 [6, 25]) | FAILS (9/42) -> FAILS | FAILS -> FAILS | HOLDS -> HOLDS |
| Qwen3.5-9B | qwen35_9b_wm2_full2_v1 | 25/25, 58/58, 48/48 | 115/103/115 | 0 vs 59 (D 59 [28, 76]) | 73/68; 0.00/0.87 | 1 vs 13 (D 13 [6, 23]) | 0 vs 16 (D 16 [3, 27]) | HOLDS (8/72) -> HOLDS | HOLDS -> HOLDS | HOLDS -> HOLDS |
| Qwen3.5-9B | qwen35_9b_wm2_full2_aligned_v1 | 25/25, 58/58, 48/48 | 114/101/113 | 0 vs 61 (D 61 [21, 75]) | 78/61; 0.00/1.00 **>1** | 2 vs 20 (D 19 [5, 30]) | 0 vs 6 (D 6 [1, 13]) | HOLDS (8/68) -> HOLDS | HOLDS -> HOLDS | PARTIAL -> PARTIAL |
| Qwen3.5-9B | qwen35_9b_wm2_fresh2_v1 | 18/18, 59/59, 48/48 | 116/108/114 | 0 vs 60 (D 60 [17, 84]) | 73/78; 0.00/0.77 | 0 vs 15 (D 15 [5, 30]) | 0 vs 16 (D 16 [4, 30]) | HOLDS (6/61) -> HOLDS | HOLDS -> HOLDS | PARTIAL -> HOLDS |
| Qwen3.5-122B-A10B | qwen35_122b_wm2_full2_v1 | 75/75, 78/78, 80/80 | 172/159/173 | 25 vs 24 (D -2 [-16, 18]) | 9/3; 2.93/7.85 **>1** | 31 vs 62 (D 31 [19, 43]) | 0 vs 3 (D 3 [0, 8]) | FAILS (28/39) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | FAILS -> FAILS |
| Qwen3.5-122B-A10B | qwen35_122b_wm2_full2_aligned_v1 | 75/75, 78/78, 80/80 | 124/117/121 | 0 vs 33 (D 33 [14, 48]) | 97/100; 0.00/0.33 | 0 vs 29 (D 29 [17, 40]) | 0 vs 51 (D 51 [38, 64]) | HOLDS (0/39) -> HOLDS | FAILS -> FAILS | not scored -> HOLDS |
| Olmo-3-7B | olmo3d7_wm2_full2_v1 | 11/11, 19/19, 15/15 | 104/104/98 | 0 vs 6 (D 6 [0, 13]) | 92/81; 0.00/0.07 | 0 vs 1 (D 1 [0, 7]) | 0 vs 0 (D 0 [0, 0]) | HOLDS (0/36) -> FAILS | FAILS -> FAILS | UNDERPOWERED -> UNDERPOWERED |
| Olmo-3-7B | olmo3d7_wm2_full2_aligned_v1 | 11/11, 19/19, 15/15 | 103/99/100 | 0 vs 0 (D 0 [0, 0]) | 92/81; 0.00/0.00 | 0 vs 1 (D 1 [0, 7]) | 0 vs 0 (D 0 [0, 0]) | FAILS (0/9) -> FAILS | FAILS -> FAILS | UNDERPOWERED -> UNDERPOWERED |
| Olmo-Hybrid-7B | olmoh7_wm2_full2_v1 | 17/17, 20/20, 17/17 | 72/93/91 | 0 vs 35 (D 35 [4, 62]) | 89/73; 0.00/0.49 | 0 vs 14 (D 14 [0, 34]) | 0 vs 17 (D 17 [0, 35]) | FAILS (6/41) -> HOLDS | FAILS -> FAILS | UNDERPOWERED -> UNDERPOWERED |
| Olmo-Hybrid-7B | olmoh7_wm2_full2_aligned_v1 | 17/17, 20/20, 17/17 | 65/96/98 | 0 vs 58 (D 58 [12, 78]) | 89/55; 0.00/1.05 **>1** | 0 vs 1 (D 1 [0, 7]) | 0 vs 39 (D 39 [4, 68]) | HOLDS (6/59) -> HOLDS | HOLDS -> HOLDS | UNDERPOWERED -> UNDERPOWERED |
| gpt-oss-20b (our J++) | gptoss20_wm2_full2_v1 | 11/11, 25/25, 23/23 | 90/78/88 | 0 vs 8 (D 8 [0, 41]) | 0/12; -/0.65 | 0 vs 0 (D 0 [0, 0]) | 1 vs 2 (D 2 [0, 11]) | FAILS (0/27) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | UNDERPOWERED -> UNDERPOWERED |
| gpt-oss-20b (our J++) | gptoss20_wm2_full2_aligned_v1 | 11/11, 25/25, 23/23 | 70/67/71 | 0 vs 7 (D 7 [0, 36]) | 95/77; 0.00/0.09 | 6 vs 2 (D -3 [-10, 1]) | 3 vs 9 (D 5 [-5, 21]) | FAILS (9/27) -> FAILS | FAILS -> FAILS | not scored -> UNDERPOWERED |
| gpt-oss-20b (J-lens) | gptoss20j_wm2_full2_v1 | 11/11, 25/25, 23/23 | 90/77/88 | 0 vs 0 (D 0 [0, 0]) | 0/12; -/0.00 | 2 vs 3 (D 1 [-4, 6]) | 2 vs 3 (D 1 [-4, 12]) | FAILS (0/9) -> FAILS | inconclusive: sites carry the bridge only partly -> inconclusive (ceiling < 0.5) | UNDERPOWERED -> UNDERPOWERED |
| gpt-oss-20b (J-lens) | gptoss20j_wm2_full2_aligned_v1 | 11/11, 25/25, 23/23 | 69/63/69 | 1 vs 10 (D 9 [-9, 28]) | 95/77; 0.01/0.13 | 2 vs 1 (D -2 [-6, 6]) | 3 vs 6 (D 2 [-5, 13]) | FAILS (18/27) -> FAILS | FAILS -> FAILS | not scored -> UNDERPOWERED |

## Cells surviving the gates (own lens direction cells at question/final, per word: total / gate A / A and B)

- wm2_suite_v1: RL 128/126/126, RR 128/126/126, BL 128/125/125, BR 128/126/126
- wm2_ctrl_v1: MP 128/122/122, MM 128/124/124, PP 128/124/124, PM 128/116/116
- wm2_full2_v1: MP 128/124/124, MM 128/124/124, PP 128/125/125, PM 128/121/121, CP 128/126/126, CM 128/120/120
- wm2_full2_v2: MP 128/125/125, MM 128/121/121, PP 128/125/125, PM 128/120/120, CP 128/126/126, CM 128/123/123
- wm2_full2_aligned_v1: MP 128/126/126, MM 128/117/117, PP 128/126/126, PM 128/122/122, CP 128/126/126, CM 128/120/120
- qwen3_32b_wm2_full2_v1: MP 128/121/121, MM 128/126/126, PP 128/124/124, PM 128/104/104, CP 128/126/126, CM 128/119/119
- qwen3_32b_wm2_full2_aligned_v1: MP 128/122/122, MM 128/118/118, PP 128/125/125, PM 128/96/96, CP 128/126/126, CM 128/108/108
- muse30_wm2_full2_v1: MP 112/107/107, MM 112/105/105, PP 112/108/108, PM 112/97/97, CP 112/110/110, CM 112/98/98
- muse30_wm2_full2_aligned_v1: MP 112/104/104, MM 112/105/105, PP 112/107/107, PM 112/97/97, CP 112/110/110, CM 112/99/99
- muse30_wm2_fresh2_v1: MP 112/100/100, MM 112/103/103, PP 112/103/103, PM 112/91/91, CP 112/108/108, CM 112/99/99
- qwen35_9b_wm2_full2_v1: MP 128/115/115, MM 128/125/125, PP 128/121/121, PM 128/103/103, CP 128/126/126, CM 128/115/115
- qwen35_9b_wm2_full2_aligned_v1: MP 128/115/115, MM 128/123/123, PP 128/120/120, PM 128/102/102, CP 128/126/126, CM 128/113/113
- qwen35_9b_wm2_fresh2_v1: MP 128/120/120, MM 128/121/121, PP 128/121/121, PM 128/108/108, CP 128/126/126, CM 128/114/114
- qwen35_122b_wm2_full2_v1: MP 176/172/172, MM 176/173/173, PP 176/173/173, PM 176/159/159, CP 176/174/174, CM 176/173/173
- qwen35_122b_wm2_full2_aligned_v1: MP 128/128/128, MM 128/124/124, PP 128/128/128, PM 128/117/117, CP 128/128/128, CM 128/121/121
- olmo3d7_wm2_full2_v1: MP 128/110/110, MM 128/113/113, PP 128/121/121, PM 128/104/104, CP 128/124/124, CM 128/98/98
- olmo3d7_wm2_full2_aligned_v1: MP 128/107/107, MM 128/117/117, PP 128/117/117, PM 128/104/104, CP 128/122/122, CM 128/104/104
- olmoh7_wm2_full2_v1: MP 128/84/84, MM 128/103/103, PP 128/114/114, PM 128/94/94, CP 128/119/119, CM 128/93/93
- olmoh7_wm2_full2_aligned_v1: MP 128/75/75, MM 128/108/108, PP 128/113/113, PM 128/98/98, CP 128/120/120, CM 128/101/101
- gptoss20_wm2_full2_v1: MP 112/94/94, MM 112/97/97, PP 112/101/101, PM 112/78/78, CP 112/102/102, CM 112/90/90
- gptoss20_wm2_full2_aligned_v1: MP 96/77/77, MM 96/73/73, PP 96/81/81, PM 96/67/67, CP 96/83/83, CM 96/72/72
- gptoss20j_wm2_full2_v1: MP 112/94/94, MM 112/97/97, PP 112/101/101, PM 112/77/77, CP 112/102/102, CM 112/90/90
- gptoss20j_wm2_full2_aligned_v1: MP 96/77/77, MM 96/72/72, PP 96/81/81, PM 96/63/63, CP 96/83/83, CM 96/70/70

## Stacked joint writes (modal CV cell per pair; bounds on the added norm / |h| at the band's last layer)

- wm2_suite_v1 (n_L=13; natural top-1 J share L32 0.083): lens_add final joint a=0.05: <= 0.65 (orthogonal 0.18); lens_add question L36 a=0.8: single layer: alpha x |h| added once
- wm2_ctrl_v1 (n_L=13; natural top-1 J share L32 0.083): lens_add question L34 a=0.8: single layer: alpha x |h| added once; lens_add question joint a=0.1: <= 1.30 (orthogonal 0.36)
- wm2_full2_v1 (n_L=13; natural top-1 J share L32 0.083): lens_add question joint a=0.1: <= 1.30 (orthogonal 0.36); lens_add question L28 a=0.8: single layer: alpha x |h| added once; lens_add final L36 a=0.8: single layer: alpha x |h| added once
- wm2_full2_v2 (n_L=13; natural top-1 J share L32 0.083): lens_add question joint a=0.1: <= 1.30 (orthogonal 0.36); lens_add question joint a=0.1: <= 1.30 (orthogonal 0.36); lens_add final L38 a=0.8: single layer: alpha x |h| added once
- wm2_full2_aligned_v1 (n_L=13; natural top-1 J share L40 0.111): lens_add final joint a=0.1: <= 1.30 (orthogonal 0.36); lens_add final L48 a=0.8: single layer: alpha x |h| added once; lens_add final L48 a=0.8: single layer: alpha x |h| added once
- qwen3_32b_wm2_full2_v1 (n_L=13; natural top-1 J share L32 0.067): lens_add question L34 a=0.8: single layer: alpha x |h| added once; lens_add question joint a=0.1: <= 1.30 (orthogonal 0.36); lens_add question joint a=0.2: <= 2.60 (orthogonal 0.72)
- qwen3_32b_wm2_full2_aligned_v1 (n_L=13; natural top-1 J share L40 0.075): lens_add final joint a=0.1: <= 1.30 (orthogonal 0.36); lens_add final joint a=0.1: <= 1.30 (orthogonal 0.36); lens_add final joint a=0.1: <= 1.30 (orthogonal 0.36)
- muse30_wm2_full2_v1 (n_L=11; natural top-1 J share L29 0.083): lens_add final joint a=0.1: <= 1.10 (orthogonal 0.33); lens_add final joint a=0.1: <= 1.10 (orthogonal 0.33); lens_add final joint a=0.1: <= 1.10 (orthogonal 0.33)
- muse30_wm2_full2_aligned_v1 (n_L=11; natural top-1 J share L26 0.076): lens_add final joint a=0.1: <= 1.10 (orthogonal 0.33); lens_add final joint a=0.1: <= 1.10 (orthogonal 0.33); lens_add final joint a=0.1: <= 1.10 (orthogonal 0.33)
- muse30_wm2_fresh2_v1 (n_L=11; natural top-1 J share L29 0.083): lens_add final L33 a=0.4: single layer: alpha x |h| added once; lens_add final joint a=0.1: <= 1.10 (orthogonal 0.33); lens_add final joint a=0.1: <= 1.10 (orthogonal 0.33)
- qwen35_9b_wm2_full2_v1 (n_L=7; natural top-1 J share L16 0.096): lens_add final L19 a=0.8: single layer: alpha x |h| added once; lens_add final joint a=0.1: <= 0.70 (orthogonal 0.26); lens_add final joint a=0.1: <= 0.70 (orthogonal 0.26)
- qwen35_9b_wm2_full2_aligned_v1 (n_L=7; natural top-1 J share L16 0.096): lens_add final L19 a=0.8: single layer: alpha x |h| added once; lens_add question joint a=0.1: <= 0.70 (orthogonal 0.26); lens_add final joint a=0.1: <= 0.70 (orthogonal 0.26)
- qwen35_9b_wm2_fresh2_v1 (n_L=7; natural top-1 J share L16 0.096): lens_add final L18 a=0.8: single layer: alpha x |h| added once; lens_add final joint a=0.2: <= 1.40 (orthogonal 0.53); lens_add final joint a=0.1: <= 0.70 (orthogonal 0.26)
- qwen35_122b_wm2_full2_v1 (n_L=10): lens_add question L29 a=0.8: single layer: alpha x |h| added once; lens_add question joint a=0.1: <= 1.00 (orthogonal 0.32); lens_add question L30 a=0.8: single layer: alpha x |h| added once
- qwen35_122b_wm2_full2_aligned_v1 (n_L=7): lens_add final joint a=0.2: <= 1.40 (orthogonal 0.53); lens_add final joint a=0.2: <= 1.40 (orthogonal 0.53); lens_add final L41 a=0.8: single layer: alpha x |h| added once
- olmo3d7_wm2_full2_v1 (n_L=7): lens_swap final Ljoint a=4: lens_swap: size not logged (n/a); lens_add question joint a=0.4: <= 2.80 (orthogonal 1.06); lens_add final L18 a=0.4: single layer: alpha x |h| added once
- olmo3d7_wm2_full2_aligned_v1 (n_L=7): lens_add final L12 a=0.05: single layer: alpha x |h| added once; lens_add question joint a=0.2: <= 1.40 (orthogonal 0.53); lens_add final L13 a=0.8: single layer: alpha x |h| added once
- olmoh7_wm2_full2_v1 (n_L=7; natural top-1 J share L17 0.044): lens_add final L20 a=0.8: single layer: alpha x |h| added once; lens_swap final Ljoint a=4: lens_swap: size not logged (n/a); lens_add final L20 a=0.4: single layer: alpha x |h| added once
- olmoh7_wm2_full2_aligned_v1 (n_L=7; natural top-1 J share L16 0.054): lens_add final L19 a=0.8: single layer: alpha x |h| added once; lens_swap final L19 a=4: lens_swap: size not logged (n/a); lens_add final joint a=0.2: <= 1.40 (orthogonal 0.53)
- gptoss20_wm2_full2_v1 (n_L=6; natural top-1 J share L13 0.069): lens_add final L15 a=0.2: single layer: alpha x |h| added once; lens_add final L11 a=0.2: single layer: alpha x |h| added once; lens_add final L11 a=0.4: single layer: alpha x |h| added once
- gptoss20_wm2_full2_aligned_v1 (n_L=5; natural top-1 J share L13 0.069): lens_add question L17 a=0.4: single layer: alpha x |h| added once; lens_add final L18 a=0.2: single layer: alpha x |h| added once; lens_add question joint a=0.1: <= 0.50 (orthogonal 0.22)
- gptoss20j_wm2_full2_v1 (n_L=6; natural top-1 J share L13 0.069): lens_add final L10 a=0.2: single layer: alpha x |h| added once; lens_add final L15 a=0.2: single layer: alpha x |h| added once; lens_add final L12 a=0.2: single layer: alpha x |h| added once
- gptoss20j_wm2_full2_aligned_v1 (n_L=5; natural top-1 J share L13 0.069): lens_add final L18 a=0.1: single layer: alpha x |h| added once; lens_add final L15 a=0.2: single layer: alpha x |h| added once; lens_add question L17 a=0.4: single layer: alpha x |h| added once

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
