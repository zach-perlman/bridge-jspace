# statement_positions / d1_rw_n80_v1

Claims: {"BL": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "not written"}, "verdict": "H-around supported"}, "BLR": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "inconclusive"}, "verdict": "neither (mixed)"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| BL/context/primary | [32, 36, 40] | 80 | 100% / 90% | 100% | 78% (87%) | 0% (0%) | 9% (0%) | 14% (0%) | 43% (10%) | not written |
| BL/context/secondary | [32, 36, 40] | 80 | 100% / 90% | 100% | 78% (87%) | 0% (0%) | 9% (0%) | 14% (0%) | 43% (10%) | not written |
| BR/bind_bridge/primary | [32, 36] | 80 | 100% / 79% | 4% | 68% (74%) | 80% (88%) | 38% (31%) | 18% (6%) | 20% (7%) | written |
| BR/bind_bridge/secondary | [32, 36] | 80 | 100% / 79% | 4% | 68% (74%) | 80% (88%) | 38% (31%) | 18% (6%) | 20% (7%) | written |
| BR/bridge_word/primary | [32, 36] | 80 | 100% / 79% | 0% | 67% (74%) | 80% (87%) | 37% (31%) | 18% (5%) | 21% (11%) | written |
| BR/bridge_word/secondary | [32, 36] | 80 | 100% / 79% | 0% | 67% (74%) | 80% (87%) | 37% (31%) | 18% (5%) | 21% (11%) | written |
| BR/context/primary | [32, 36] | 80 | 100% / 90% | 100% | 69% (77%) | 86% (96%) | 50% (46%) | 24% (10%) | 25% (12%) | written |
| BR/context/secondary | [32, 36] | 80 | 100% / 90% | 100% | 69% (77%) | 86% (96%) | 50% (46%) | 24% (10%) | 25% (12%) | written |
| RL/question/primary | [36, 40] | 80 | 82% / 26% | 1% | 52% (62%) | 7% (0%) | 16% (1%) | 7% (0%) | 20% (1%) | not written |
| RL/question/secondary | [36, 40] | 80 | 82% / 26% | 1% | 52% (62%) | 7% (0%) | 16% (1%) | 7% (0%) | 20% (1%) | not written |
| BLR/context/primary | [32] | 80 | 100% / 82% | 100% | 72% (78%) | 7% (6%) | 28% (12%) | 16% (1%) | 50% (31%) | inconclusive |
| BLR/context/secondary | [32] | 80 | 100% / 82% | 100% | 72% (78%) | 7% (6%) | 28% (12%) | 16% (1%) | 50% (31%) | inconclusive |
| BRL/context/primary | [32] | 80 | 100% / 70% | 100% | 67% (65%) | 36% (26%) | 36% (26%) | 32% (15%) | 42% (21%) | inconclusive |
| BRL/context/secondary | [32] | 80 | 100% / 70% | 100% | 67% (65%) | 36% (26%) | 36% (26%) | 32% (15%) | 42% (21%) | inconclusive |
| R/question/primary | [36, 40] | 80 | 100% / 78% | 26% | 61% (77%) | 76% (92%) | 115% (97%) | 13% (1%) | 93% (45%) | written |
| R/question/secondary | [36, 40] | 80 | 100% / 78% | 26% | 61% (77%) | 76% (92%) | 115% (97%) | 13% (1%) | 93% (45%) | written |
| B/bind_bridge/primary | [32, 36] | 80 | 100% / 89% | 20% | 99% (100%) | 103% (100%) | 99% (92%) | 21% (6%) | 49% (30%) | written |
| B/bind_bridge/secondary | [32, 36] | 80 | 100% / 89% | 20% | 99% (100%) | 103% (100%) | 99% (92%) | 21% (6%) | 49% (30%) | written |
| B/bridge_word/primary | [32, 36] | 80 | 100% / 89% | 0% | 99% (100%) | 103% (100%) | 96% (90%) | 22% (4%) | 41% (22%) | written |
| B/bridge_word/secondary | [32, 36] | 80 | 100% / 89% | 0% | 99% (100%) | 103% (100%) | 96% (90%) | 22% (4%) | 41% (22%) | written |
| B/context/primary | [32, 36] | 80 | 100% / 91% | 100% | 85% (93%) | 103% (100%) | 86% (78%) | 14% (0%) | 24% (4%) | written |
| B/context/secondary | [32, 36] | 80 | 100% / 91% | 100% | 85% (93%) | 103% (100%) | 86% (78%) | 14% (0%) | 24% (4%) | written |
| B/question/primary | [40] | 80 | 98% / 26% | 34% | 65% (82%) | 81% (100%) | 115% (95%) | 5% (0%) | 113% (65%) | written |
| B/question/secondary | [40] | 80 | 98% / 26% | 34% | 65% (82%) | 81% (100%) | 115% (95%) | 5% (0%) | 113% (65%) | written |

Write cells: mean frac of the way to C (flips).
