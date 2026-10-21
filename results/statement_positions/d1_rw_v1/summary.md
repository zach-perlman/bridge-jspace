# statement_positions / d1_rw_v1

Claims: {"BL": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "inconclusive"}, "verdict": "neither (mixed)"}, "BLR": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "inconclusive"}, "verdict": "neither (mixed)"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| BL/context/primary | [32, 36, 40] | 32 | 100% / 88% | 100% | 76% (90%) | 1% (0%) | 10% (0%) | 15% (0%) | 43% (12%) | inconclusive |
| BL/context/secondary | [32, 36, 40] | 32 | 100% / 88% | 100% | 76% (90%) | 1% (0%) | 10% (0%) | 15% (0%) | 43% (12%) | inconclusive |
| BR/bind_bridge/primary | [32] | 32 | 100% / 72% | 0% | 85% (100%) | 94% (100%) | 58% (62%) | 28% (6%) | 33% (19%) | written |
| BR/bind_bridge/secondary | [32] | 32 | 100% / 72% | 0% | 85% (100%) | 94% (100%) | 58% (62%) | 28% (6%) | 33% (19%) | written |
| BR/bridge_word/primary | [32] | 32 | 100% / 72% | 0% | 85% (100%) | 94% (100%) | 56% (56%) | 27% (9%) | 35% (22%) | written |
| BR/bridge_word/secondary | [32] | 32 | 100% / 72% | 0% | 85% (100%) | 94% (100%) | 56% (56%) | 27% (9%) | 35% (22%) | written |
| BR/context/primary | [32, 36] | 32 | 100% / 88% | 100% | 67% (77%) | 84% (95%) | 51% (44%) | 25% (11%) | 27% (14%) | written |
| BR/context/secondary | [32, 36] | 32 | 100% / 88% | 100% | 67% (77%) | 84% (95%) | 51% (44%) | 25% (11%) | 27% (14%) | written |
| RL/question/primary | [36, 40] | 32 | 81% / 25% | 0% | 50% (56%) | 6% (0%) | 16% (0%) | 8% (0%) | 21% (2%) | not written |
| RL/question/secondary | [36, 40] | 32 | 81% / 25% | 0% | 50% (56%) | 6% (0%) | 16% (0%) | 8% (0%) | 21% (2%) | not written |
| BLR/context/primary | [32] | 32 | 100% / 81% | 100% | 74% (78%) | 6% (9%) | 24% (6%) | 13% (0%) | 49% (22%) | inconclusive |
| BLR/context/secondary | [32] | 32 | 100% / 81% | 100% | 74% (78%) | 6% (9%) | 24% (6%) | 13% (0%) | 49% (22%) | inconclusive |
| BRL/context/primary | [32] | 32 | 100% / 72% | 100% | 70% (69%) | 32% (19%) | 35% (19%) | 33% (12%) | 39% (22%) | inconclusive |
| BRL/context/secondary | [32] | 32 | 100% / 72% | 100% | 70% (69%) | 32% (19%) | 35% (19%) | 33% (12%) | 39% (22%) | inconclusive |
| R/question/primary | [36, 40] | 32 | 100% / 69% | 19% | 60% (73%) | 79% (97%) | 113% (98%) | 13% (2%) | 92% (45%) | written |
| R/question/secondary | [36, 40] | 32 | 100% / 69% | 19% | 60% (73%) | 79% (97%) | 113% (98%) | 13% (2%) | 92% (45%) | written |
| B/bind_bridge/primary | [32, 36, 40] | 32 | 100% / 91% | 16% | 83% (85%) | 86% (83%) | 83% (75%) | 17% (2%) | 42% (23%) | written |
| B/bind_bridge/secondary | [32, 36, 40] | 32 | 100% / 91% | 16% | 83% (85%) | 86% (83%) | 83% (75%) | 17% (2%) | 42% (23%) | written |
| B/bridge_word/primary | [32, 36, 40] | 32 | 100% / 91% | 0% | 84% (85%) | 86% (83%) | 80% (72%) | 18% (5%) | 36% (21%) | written |
| B/bridge_word/secondary | [32, 36, 40] | 32 | 100% / 91% | 0% | 84% (85%) | 86% (83%) | 80% (72%) | 18% (5%) | 36% (21%) | written |
| B/context/primary | [32, 36] | 32 | 100% / 91% | 100% | 87% (97%) | 104% (100%) | 90% (80%) | 13% (0%) | 26% (5%) | written |
| B/context/secondary | [32, 36] | 32 | 100% / 91% | 100% | 87% (97%) | 104% (100%) | 90% (80%) | 13% (0%) | 26% (5%) | written |
| B/question/primary | [40] | 32 | 100% / 22% | 34% | 64% (88%) | 81% (100%) | 118% (94%) | 6% (0%) | 118% (75%) | written |
| B/question/secondary | [40] | 32 | 100% / 22% | 34% | 64% (88%) | 81% (100%) | 118% (94%) | 6% (0%) | 118% (75%) | written |

Write cells: mean frac of the way to C (flips).
