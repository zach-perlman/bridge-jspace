# mistral24_full_v8_competence_v1 on full_v8: whole-question accuracy %

| word | n | L0 | L1 | L2 | L3 | text | structured | each step alone (all right) | C | O | guess right |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PP | 192 | 96 | 94 | 100 | 92 | 96 | 95 | 93 | 99 | 96 | 14 |
| PM | 192 | 94 | 90 | 98 | 94 | 97 | 90 | 92 | 95 | 92 | 17 |
| MP | 152 | 88 | 81 | 71 | 79 | 79 | 83 | 99 | 79 | 81 | 2 |
| MM | 152 | 96 | 88 | 79 | 86 | 91 | 86 | 98 | 89 | 89 | 5 |
| CP | 192 | 88 | 90 | 88 | 92 | 87 | 91 | 96 | 91 | 93 | 2 |
| CM | 192 | 81 | 75 | 75 | 73 | 81 | 71 | 93 | 74 | 73 | 9 |
| PPP | 192 | 71 | 44 | 52 | 38 | 69 | 33 | 97 | 49 | 51 | 20 |
| PPM | 192 | 54 | 33 | 40 | 44 | 52 | 33 | 96 | 35 | 32 | 26 |
| PMP | 192 | 46 | 54 | 54 | 50 | 68 | 34 | 93 | 34 | 36 | 15 |
| MPP | 152 | 54 | 17 | 11 | 7 | 28 | 23 | 99 | 29 | 25 | 18 |
| MPM | 152 | 40 | 15 | 18 | 14 | 23 | 23 | 97 | 26 | 28 | 26 |
| MMP | 152 | 25 | 23 | 36 | 18 | 35 | 14 | 91 | 29 | 26 | 5 |

## By domain (whole %)

| word | animals | planets | elements | greek | instruments | vehicles | shapes |
|---|---|---|---|---|---|---|---|
| PP | 96 | 97 | 100 | 89 | 92 | 100 | 92 |
| PM | 96 | 87 | 100 | 93 | 88 | 100 | 92 |
| MP | 74 | 91 | 81 | - | 100 | 92 | 38 |
| MM | 86 | 94 | 88 | - | 93 | 100 | 62 |
| CP | 93 | 93 | 89 | 90 | 96 | 85 | 79 |
| CM | 59 | 67 | 82 | 80 | 85 | 81 | 79 |
| PPP | 52 | 39 | 56 | - | - | 50 | 58 |
| PPM | 28 | 18 | 47 | - | - | 45 | 76 |
| PMP | 28 | 29 | 32 | - | - | 83 | 79 |
| MPP | 32 | 26 | 12 | - | - | 37 | 24 |
| MPM | 45 | 11 | 18 | - | - | 32 | 5 |
| MMP | 30 | 21 | 21 | - | - | 53 | 5 |

## Items the experiments will use (three-step words: scene rule / per word, the 2026-10-21 fix)

| word | knock-out (all domains) | of which text / structured (scene rule) | steering pool (counterfactual, core) |
|---|---|---|---|
| PP | 151 | 83 / 68 | 86 (40 used) |
| PM | 151 | 83 / 68 | 86 (40 used) |
| MP | 88 | 47 / 41 | 65 (40 used) |
| MM | 88 | 47 / 41 | 65 (40 used) |
| CP | 103 | 51 / 52 | 54 (40 used) |
| CM | 103 | 51 / 52 | 54 (40 used) |
| PPP | 28 / 80 | 23 / 5 | 1 / 27 (40 used) |
| PPM | 28 / 60 | 23 / 5 | 1 / 10 (40 used) |
| PMP | 28 / 77 | 23 / 5 | 1 / 9 (40 used) |
| MPP | 1 / 21 | 0 / 1 | 0 / 7 (40 used) |
| MPM | 1 / 12 | 0 / 1 | 0 / 4 (40 used) |
| MMP | 1 / 23 | 0 / 1 | 0 / 9 (40 used) |

Total: knock-out 771 items, steering pool 413 items.
