# qwen3_32b_full_v8_competence_v1 on full_v8: whole-question accuracy %

| word | n | L0 | L1 | L2 | L3 | text | structured | each step alone (all right) | C | O | guess right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 192 | 100 | 98 | 98 | 100 | 100 | 98 | 99 | 96 | 98 | 14 |
| PM | 192 | 77 | 79 | 88 | 83 | 84 | 80 | 94 | 71 | 73 | 8 |
| MP | 152 | 90 | 62 | 79 | 79 | 75 | 79 | 99 | 74 | 77 | 11 |
| MM | 152 | 92 | 94 | 86 | 71 | 87 | 88 | 89 | 81 | 86 | 14 |
| CP | 192 | 96 | 98 | 88 | 90 | 91 | 94 | 94 | 93 | 96 | 7 |
| CM | 192 | 79 | 79 | 81 | 79 | 77 | 83 | 90 | 72 | 79 | 12 |
| PPP | 192 | 75 | 40 | 40 | 33 | 66 | 28 | 96 | 48 | 46 | 20 |
| PPM | 192 | 52 | 21 | 29 | 33 | 40 | 28 | 92 | 30 | 30 | 20 |
| PMP | 192 | 62 | 58 | 50 | 58 | 65 | 50 | 91 | 47 | 41 | 10 |
| MPP | 152 | 48 | 29 | 32 | 25 | 41 | 29 | 97 | 35 | 32 | 16 |
| MPM | 152 | 46 | 17 | 4 | 18 | 29 | 18 | 86 | 40 | 21 | 24 |
| MMP | 152 | 54 | 48 | 43 | 32 | 58 | 33 | 93 | 44 | 37 | 7 |

## By domain (whole %)

| word | animals | planets | elements | greek | instruments | vehicles | shapes |
|---|---|---|---|---|---|---|---|
| PP | 100 | 97 | 100 | 100 | 100 | 100 | 96 |
| PM | 100 | 40 | 62 | 81 | 100 | 100 | 96 |
| MP | 83 | 89 | 67 | - | 79 | 85 | 54 |
| MM | 89 | 80 | 88 | - | 100 | 85 | 92 |
| CP | 96 | 100 | 86 | 97 | 96 | 96 | 79 |
| CM | 96 | 52 | 86 | 77 | 100 | 65 | 82 |
| PPP | 48 | 45 | 41 | - | - | 55 | 45 |
| PPM | 42 | 8 | 29 | - | - | 29 | 61 |
| PMP | 35 | 29 | 62 | - | - | 74 | 87 |
| MPP | 48 | 29 | 21 | - | - | 37 | 43 |
| MPM | 35 | 11 | 18 | - | - | 16 | 43 |
| MMP | 52 | 34 | 38 | - | - | 63 | 52 |

## Items the experiments will use (three-step words: scene rule / per word, the 2026-10-21 fix)

| word | knock-out (all domains) | of which text / structured (scene rule) | steering pool (counterfactual, core) |
|---|---|---|---|
| PP | 123 | 67 / 56 | 55 (40 used) |
| PM | 123 | 67 / 56 | 55 (40 used) |
| MP | 61 | 33 / 28 | 40 (40 used) |
| MM | 61 | 33 / 28 | 40 (40 used) |
| CP | 108 | 49 / 59 | 57 (40 used) |
| CM | 108 | 49 / 59 | 57 (40 used) |
| PPP | 21 / 69 | 15 / 6 | 2 / 23 (40 used) |
| PPM | 21 / 48 | 15 / 6 | 2 / 14 (40 used) |
| PMP | 21 / 83 | 15 / 6 | 2 / 19 (40 used) |
| MPP | 7 / 22 | 5 / 2 | 3 / 6 (40 used) |
| MPM | 7 / 24 | 5 / 2 | 3 / 11 (40 used) |
| MMP | 7 / 43 | 5 / 2 | 3 / 18 (40 used) |

Total: knock-out 668 items, steering pool 319 items.
