# statement_positions / qwen36_27b_jlens_d1_topics2_rw

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "not written"}, "verdict": "H-around supported"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [32, 36, 40] | 180 | 96% / 88% | 97% | 60% (64%) | 3% (0%) | 25% (5%) | 27% (7%) | 42% (15%) | not written |
| PP/context/secondary | [32, 36, 40] | 180 | 96% / 88% | 97% | 60% (64%) | 3% (0%) | 25% (5%) | 27% (7%) | 42% (15%) | not written |
| PM/bind_bridge/primary | [32] | 180 | 63% / 41% | 3% | 77% (78%) | 44% (35%) | 36% (28%) | 19% (9%) | 26% (16%) | written |
| PM/bind_bridge/secondary | [32] | 180 | 63% / 41% | 3% | 77% (78%) | 44% (35%) | 36% (28%) | 19% (9%) | 26% (16%) | written |
| PM/bridge_word/primary | [32] | 180 | 63% / 41% | 2% | 74% (74%) | 43% (36%) | 34% (27%) | 17% (7%) | 26% (14%) | written |
| PM/bridge_word/secondary | [32] | 180 | 63% / 41% | 2% | 74% (74%) | 43% (36%) | 34% (27%) | 17% (7%) | 26% (14%) | written |
| PM/context/primary | [32, 36] | 180 | 94% / 85% | 95% | 66% (66%) | 50% (41%) | 56% (41%) | 29% (8%) | 39% (18%) | written |
| PM/context/secondary | [32, 36] | 180 | 94% / 85% | 95% | 66% (66%) | 50% (41%) | 56% (41%) | 29% (8%) | 39% (18%) | written |

Write cells: mean frac of the way to C (flips).
