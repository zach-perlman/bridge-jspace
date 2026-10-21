# statement_positions / d1_smoke_27b_rw

Claims: {"BL": {"jspace": {"statement_verdicts": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive"}, "positive_control": {"bind_bridge": "inside", "bridge_word": "inside"}, "jspace_half": "mixed / inconclusive"}, "lens_write": {"bind_bridge": "not written", "bridge_word": "not written"}, "verdict": "neither (mixed)"}, "BLR": {"jspace": {"statement_verdicts": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive"}, "positive_control": {"bind_bridge": "inside", "bridge_word": "inside"}, "jspace_half": "mixed / inconclusive"}, "lens_write": {"bind_bridge": "not written", "bridge_word": "not written"}, "verdict": "neither (mixed)"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| BL/bind_bridge/primary | [36] | 4 | 100% / 50% | 0% | -0% (0%) | 0% (0%) | 0% (0%) | 0% (0%) | 0% (0%) | not written |
| BL/bind_bridge/secondary | [36] | 4 | 100% / 50% | 0% | -0% (0%) | 0% (0%) | 0% (0%) | 0% (0%) | 0% (0%) | not written |
| BL/bridge_word/primary | [36] | 4 | 100% / 50% | 0% | 0% (0%) | 0% (0%) | -0% (0%) | 1% (0%) | 0% (0%) | not written |
| BL/bridge_word/secondary | [36] | 4 | 100% / 50% | 0% | 0% (0%) | 0% (0%) | -0% (0%) | 1% (0%) | 0% (0%) | not written |
| BL/question/primary | [36] | 4 | 0% / 0% | 0% | 15% (0%) | 0% (0%) | 10% (0%) | 3% (0%) | 36% (0%) | not written |
| BL/question/secondary | [36] | 4 | 0% / 0% | 0% | 15% (0%) | 0% (0%) | 10% (0%) | 3% (0%) | 36% (0%) | not written |
| BR/bind_bridge/primary | [36] | 4 | 100% / 50% | 0% | 38% (25%) | 72% (100%) | 27% (25%) | 10% (0%) | 11% (0%) | written |
| BR/bind_bridge/secondary | [36] | 4 | 100% / 50% | 0% | 38% (25%) | 72% (100%) | 27% (25%) | 10% (0%) | 11% (0%) | written |
| BR/bridge_word/primary | [36] | 4 | 100% / 50% | 0% | 39% (50%) | 72% (100%) | 26% (25%) | 12% (0%) | 12% (0%) | written |
| BR/bridge_word/secondary | [36] | 4 | 100% / 50% | 0% | 39% (50%) | 72% (100%) | 26% (25%) | 12% (0%) | 12% (0%) | written |
| BR/question/primary | [36] | 4 | 25% / 0% | 0% | 29% (25%) | 20% (0%) | 44% (50%) | 1% (0%) | 31% (25%) | inconclusive |
| BR/question/secondary | [36] | 4 | 25% / 0% | 0% | 29% (25%) | 20% (0%) | 44% (50%) | 1% (0%) | 31% (25%) | inconclusive |
| RL/bind_bridge/primary | [36] | 4 | 100% / 50% | 0% | - | - | - | - | - | no data |
| RL/bind_bridge/secondary | [36] | 4 | 100% / 50% | 0% | - | - | - | - | - | no data |
| RL/bridge_word/primary | [36] | 4 | 100% / 50% | 0% | - | - | - | - | - | no data |
| RL/bridge_word/secondary | [36] | 4 | 100% / 50% | 0% | - | - | - | - | - | no data |
| RL/question/primary | [36] | 4 | 50% / 25% | 0% | 52% (75%) | 3% (0%) | 23% (0%) | 6% (0%) | 25% (0%) | not written |
| RL/question/secondary | [36] | 4 | 50% / 25% | 0% | 52% (75%) | 3% (0%) | 23% (0%) | 6% (0%) | 25% (0%) | not written |
| RR/bind_bridge/primary | [36] | 4 | 100% / 50% | 0% | - | - | - | - | - | no data |
| RR/bind_bridge/secondary | [36] | 4 | 100% / 50% | 0% | - | - | - | - | - | no data |
| RR/bridge_word/primary | [36] | 4 | 100% / 50% | 0% | - | - | - | - | - | no data |
| RR/bridge_word/secondary | [36] | 4 | 100% / 50% | 0% | - | - | - | - | - | no data |
| RR/question/primary | [36] | 4 | 50% / 25% | 0% | 27% (0%) | 22% (0%) | 40% (50%) | 2% (0%) | 7% (0%) | inconclusive |
| RR/question/secondary | [36] | 4 | 50% / 25% | 0% | 27% (0%) | 22% (0%) | 40% (50%) | 2% (0%) | 7% (0%) | inconclusive |
| BLR/bind_bridge/primary | [36] | 4 | 100% / 100% | 0% | 1% (0%) | 1% (0%) | 1% (0%) | 1% (0%) | 2% (0%) | not written |
| BLR/bind_bridge/secondary | [36] | 4 | 100% / 100% | 0% | 1% (0%) | 1% (0%) | 1% (0%) | 1% (0%) | 2% (0%) | not written |
| BLR/bridge_word/primary | [36] | 4 | 100% / 100% | 0% | 1% (0%) | 1% (0%) | 1% (0%) | 1% (0%) | 1% (0%) | not written |
| BLR/bridge_word/secondary | [36] | 4 | 100% / 100% | 0% | 1% (0%) | 1% (0%) | 1% (0%) | 1% (0%) | 1% (0%) | not written |
| BLR/question/primary | [36] | 4 | 25% / 0% | 0% | 35% (25%) | -0% (0%) | 8% (25%) | 10% (0%) | 13% (0%) | inconclusive |
| BLR/question/secondary | [36] | 4 | 25% / 0% | 0% | 35% (25%) | -0% (0%) | 8% (25%) | 10% (0%) | 13% (0%) | inconclusive |
| BRL/bind_bridge/primary | [36] | 4 | 100% / 100% | 0% | 35% (50%) | 37% (25%) | 30% (25%) | 19% (0%) | 25% (0%) | inconclusive |
| BRL/bind_bridge/secondary | [36] | 4 | 100% / 100% | 0% | 35% (50%) | 37% (25%) | 30% (25%) | 19% (0%) | 25% (0%) | inconclusive |
| BRL/bridge_word/primary | [36] | 4 | 100% / 100% | 0% | 35% (50%) | 36% (25%) | 24% (0%) | 18% (0%) | 20% (0%) | inconclusive |
| BRL/bridge_word/secondary | [36] | 4 | 100% / 100% | 0% | 35% (50%) | 36% (25%) | 24% (0%) | 18% (0%) | 20% (0%) | inconclusive |
| BRL/question/primary | [36] | 4 | 25% / 0% | 0% | 29% (0%) | 14% (0%) | 39% (0%) | 8% (0%) | 33% (0%) | not written |
| BRL/question/secondary | [36] | 4 | 25% / 0% | 0% | 29% (0%) | 14% (0%) | 39% (0%) | 8% (0%) | 33% (0%) | not written |
| R/bind_bridge/primary | [36] | 4 | 100% / 100% | 25% | - | - | - | - | - | no data |
| R/bind_bridge/secondary | [36] | 4 | 100% / 100% | 25% | - | - | - | - | - | no data |
| R/bridge_word/primary | [36] | 4 | 100% / 100% | 0% | - | - | - | - | - | no data |
| R/bridge_word/secondary | [36] | 4 | 100% / 100% | 0% | - | - | - | - | - | no data |
| R/question/primary | [36] | 4 | 100% / 75% | 0% | 57% (75%) | 68% (75%) | 106% (100%) | 14% (0%) | 72% (50%) | written |
| R/question/secondary | [36] | 4 | 100% / 75% | 0% | 57% (75%) | 68% (75%) | 106% (100%) | 14% (0%) | 72% (50%) | written |
| B/bind_bridge/primary | [36] | 4 | 100% / 50% | 25% | 98% (100%) | 104% (100%) | 100% (100%) | 23% (0%) | 44% (25%) | written |
| B/bind_bridge/secondary | [36] | 4 | 100% / 50% | 25% | 98% (100%) | 104% (100%) | 100% (100%) | 23% (0%) | 44% (25%) | written |
| B/bridge_word/primary | [36] | 4 | 100% / 50% | 0% | 98% (100%) | 104% (100%) | 98% (100%) | 13% (0%) | 39% (25%) | written |
| B/bridge_word/secondary | [36] | 4 | 100% / 50% | 0% | 98% (100%) | 104% (100%) | 98% (100%) | 13% (0%) | 39% (25%) | written |
| B/question/primary | [36] | 4 | 100% / 25% | 50% | 20% (0%) | 30% (0%) | 106% (100%) | 2% (0%) | 104% (75%) | written |
| B/question/secondary | [36] | 4 | 100% / 25% | 50% | 20% (0%) | 30% (0%) | 106% (100%) | 2% (0%) | 104% (75%) | written |

Write cells: mean frac of the way to C (flips).
