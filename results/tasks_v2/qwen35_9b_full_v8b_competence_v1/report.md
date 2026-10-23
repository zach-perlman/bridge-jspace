# qwen35_9b_full_v8b_competence_v1 on full_v8: whole-question accuracy %

| word | n | L0 | L1 | L2 | L3 | text | structured | each step alone (all right) | C | O | guess right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 192 | 98 | 92 | 94 | 92 | 94 | 94 | 99 | 92 | 96 | 11 |
| PM | 192 | 81 | 88 | 85 | 92 | 91 | 82 | 89 | 78 | 87 | 15 |
| MP | 152 | 75 | 73 | 64 | 54 | 73 | 64 | 99 | 58 | 66 | 14 |
| MM | 152 | 73 | 79 | 71 | 61 | 69 | 75 | 88 | 70 | 71 | 16 |
| CP | 192 | 96 | 96 | 92 | 92 | 91 | 96 | 94 | 96 | 93 | 11 |
| CM | 192 | 79 | 81 | 79 | 71 | 81 | 74 | 87 | 68 | 73 | 16 |
| PPP | 192 | 56 | 17 | 25 | 23 | 32 | 28 | 98 | 39 | 26 | 27 |
| PPM | 192 | 54 | 25 | 17 | 27 | 33 | 28 | 89 | 27 | 23 | 20 |
| PMP | 192 | 40 | 40 | 42 | 48 | 56 | 28 | 88 | 34 | 25 | 14 |
| MPP | 152 | 52 | 15 | 7 | 14 | 28 | 22 | 97 | 21 | 22 | 20 |
| MPM | 152 | 29 | 17 | 7 | 11 | 18 | 18 | 86 | 23 | 16 | 20 |
| MMP | 152 | 44 | 38 | 21 | 21 | 43 | 23 | 86 | 24 | 33 | 11 |

## By domain (whole %)

| word | animals | planets | elements | greek | instruments | vehicles | shapes |
|---|---|---|---|---|---|---|---|
| PP | 100 | 97 | 90 | 89 | 92 | 96 | 92 |
| PM | 96 | 70 | 93 | 78 | 92 | 82 | 96 |
| MP | 71 | 80 | 48 | - | 100 | 85 | 46 |
| MM | 89 | 49 | 74 | - | 71 | 77 | 85 |
| CP | 93 | 96 | 93 | 93 | 92 | 96 | 93 |
| CM | 89 | 56 | 79 | 67 | 81 | 81 | 93 |
| PPP | 32 | 21 | 35 | - | - | 31 | 32 |
| PPM | 28 | 13 | 38 | - | - | 36 | 39 |
| PMP | 38 | 18 | 26 | - | - | 55 | 71 |
| MPP | 18 | 21 | 24 | - | - | 42 | 33 |
| MPM | 12 | 13 | 21 | - | - | 37 | 14 |
| MMP | 35 | 34 | 15 | - | - | 53 | 43 |

## Items the experiments will use (three-step words: scene rule / per word, the 2026-10-21 fix)

| word | knock-out (all domains) | of which text / structured (scene rule) | steering pool (counterfactual, core) |
|---|---|---|---|
| PP | 118 | 65 / 53 | 57 (40 used) |
| PM | 118 | 65 / 53 | 57 (40 used) |
| MP | 42 | 21 / 21 | 24 (40 used) |
| MM | 42 | 21 / 21 | 24 (40 used) |
| CP | 106 | 51 / 55 | 49 (40 used) |
| CM | 106 | 51 / 55 | 49 (40 used) |
| PPP | 10 / 40 | 8 / 2 | 1 / 11 (40 used) |
| PPM | 10 / 35 | 8 / 2 | 1 / 5 (40 used) |
| PMP | 10 / 61 | 8 / 2 | 1 / 8 (40 used) |
| MPP | 2 / 16 | 1 / 1 | 0 / 1 (40 used) |
| MPM | 2 / 10 | 1 / 1 | 0 / 0 (40 used) |
| MMP | 2 / 26 | 1 / 1 | 0 / 5 (40 used) |

Total: knock-out 568 items, steering pool 263 items.
