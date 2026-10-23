# qwen35_9b_full_v8_competence_v1 on full_v8: whole-question accuracy %

| word | n | L0 | L1 | L2 | L3 | text | structured | each step alone (all right) | C | O | guess right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 192 | 98 | 92 | 94 | 92 | 94 | 94 | 99 | 93 | 96 | 11 |
| PM | 192 | 81 | 88 | 85 | 92 | 91 | 82 | 89 | 79 | 87 | 14 |
| MP | 152 | 77 | 73 | 64 | 57 | 75 | 65 | 99 | 58 | 66 | 14 |
| MM | 152 | 73 | 79 | 71 | 61 | 69 | 75 | 88 | 70 | 71 | 16 |
| CP | 192 | 96 | 96 | 92 | 94 | 91 | 97 | 94 | 95 | 93 | 11 |
| CM | 192 | 79 | 81 | 77 | 73 | 82 | 73 | 87 | 68 | 72 | 18 |
| PPP | 192 | 58 | 17 | 21 | 23 | 30 | 29 | 98 | 38 | 25 | 27 |
| PPM | 192 | 54 | 25 | 17 | 23 | 33 | 26 | 89 | 27 | 23 | 21 |
| PMP | 192 | 40 | 42 | 42 | 48 | 56 | 29 | 89 | 33 | 25 | 14 |
| MPP | 152 | 54 | 15 | 7 | 11 | 29 | 21 | 97 | 22 | 24 | 20 |
| MPM | 152 | 31 | 17 | 7 | 11 | 18 | 19 | 86 | 22 | 16 | 20 |
| MMP | 152 | 44 | 40 | 25 | 21 | 46 | 23 | 86 | 24 | 33 | 11 |

## By domain (whole %)

| word | animals | planets | elements | greek | instruments | vehicles | shapes |
|---|---|---|---|---|---|---|---|
| PP | 100 | 97 | 90 | 89 | 92 | 96 | 92 |
| PM | 96 | 70 | 93 | 78 | 92 | 82 | 96 |
| MP | 74 | 83 | 48 | - | 100 | 85 | 46 |
| MM | 89 | 49 | 74 | - | 71 | 77 | 85 |
| CP | 93 | 96 | 93 | 97 | 92 | 96 | 93 |
| CM | 89 | 56 | 79 | 67 | 81 | 81 | 93 |
| PPP | 28 | 24 | 35 | - | - | 31 | 32 |
| PPM | 28 | 13 | 35 | - | - | 36 | 37 |
| PMP | 40 | 18 | 26 | - | - | 55 | 71 |
| MPP | 15 | 24 | 24 | - | - | 42 | 33 |
| MPM | 12 | 16 | 21 | - | - | 37 | 14 |
| MMP | 38 | 37 | 15 | - | - | 53 | 43 |

## Items the experiments will use (three-step words: scene rule / per word, the 2026-10-21 fix)

| word | knock-out (all domains) | of which text / structured (scene rule) | steering pool (counterfactual, core) |
|---|---|---|---|
| PP | 119 | 65 / 54 | 58 (40 used) |
| PM | 119 | 65 / 54 | 58 (40 used) |
| MP | 43 | 22 / 21 | 25 (40 used) |
| MM | 43 | 22 / 21 | 25 (40 used) |
| CP | 105 | 51 / 54 | 48 (40 used) |
| CM | 105 | 51 / 54 | 48 (40 used) |
| PPP | 10 / 39 | 8 / 2 | 1 / 10 (40 used) |
| PPM | 10 / 34 | 8 / 2 | 1 / 5 (40 used) |
| PMP | 10 / 61 | 8 / 2 | 1 / 8 (40 used) |
| MPP | 2 / 16 | 1 / 1 | 0 / 1 (40 used) |
| MPM | 2 / 11 | 1 / 1 | 0 / 0 (40 used) |
| MMP | 2 / 26 | 1 / 1 | 0 / 5 (40 used) |

Total: knock-out 570 items, steering pool 265 items.
