# statement_positions / qwen3_32b_jpp_d1_formats_rw

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "positive_control": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "jspace_half": "H-around but positive control fails (not interpretable)"}, "lens_write": {"bind_bridge": "not written", "bridge_word": "inconclusive", "context": "not written"}, "verdict": "neither (mixed)"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [32, 36, 40] | 180 | 70% / 38% | 8% | 70% (71%) | 2% (0%) | 38% (28%) | 27% (14%) | 46% (32%) | not written |
| PP/bind_bridge/secondary | [32, 36, 40] | 180 | 70% / 38% | 8% | 70% (71%) | 2% (0%) | 38% (28%) | 27% (14%) | 46% (32%) | not written |
| PP/bridge_word/primary | [32, 36] | 180 | 70% / 36% | 5% | 77% (78%) | 2% (1%) | 36% (26%) | 23% (14%) | 40% (28%) | inconclusive |
| PP/bridge_word/secondary | [32, 36] | 180 | 70% / 36% | 5% | 77% (78%) | 2% (1%) | 36% (26%) | 23% (14%) | 40% (28%) | inconclusive |
| PP/context/primary | [32, 36, 40] | 180 | 98% / 76% | 98% | 100% (100%) | 3% (0%) | 40% (26%) | 36% (18%) | 50% (24%) | not written |
| PP/context/secondary | [32, 36, 40] | 180 | 98% / 76% | 98% | 100% (100%) | 3% (0%) | 40% (26%) | 36% (18%) | 50% (24%) | not written |
| PM/bind_bridge/primary | [32, 36, 40] | 180 | 70% / 38% | 8% | 92% (90%) | 20% (15%) | 58% (49%) | 23% (14%) | 52% (37%) | inconclusive |
| PM/bind_bridge/secondary | [32, 36, 40] | 180 | 70% / 38% | 8% | 92% (90%) | 20% (15%) | 58% (49%) | 23% (14%) | 52% (37%) | inconclusive |
| PM/bridge_word/primary | [32, 36, 40] | 180 | 70% / 38% | 8% | 91% (89%) | 20% (14%) | 50% (43%) | 21% (14%) | 39% (27%) | inconclusive |
| PM/bridge_word/secondary | [32, 36, 40] | 180 | 70% / 38% | 8% | 91% (89%) | 20% (14%) | 50% (43%) | 21% (14%) | 39% (27%) | inconclusive |
| PM/context/primary | [32, 36, 40] | 180 | 98% / 76% | 98% | 100% (100%) | 24% (19%) | 70% (56%) | 35% (22%) | 58% (30%) | written |
| PM/context/secondary | [32, 36, 40] | 180 | 98% / 76% | 98% | 100% (100%) | 24% (19%) | 70% (56%) | 35% (22%) | 58% (30%) | written |

Write cells: mean frac of the way to C (flips).
