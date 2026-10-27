# statement_positions / qwen35_9b_d1_topics2_rw

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "not written"}, "verdict": "H-around supported"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [16, 18] | 180 | 100% / 100% | 100% | 54% (55%) | 0% (0%) | 16% (5%) | 17% (4%) | 42% (16%) | not written |
| PP/context/secondary | [16, 18] | 180 | 100% / 100% | 100% | 54% (55%) | 0% (0%) | 16% (5%) | 17% (4%) | 42% (16%) | not written |
| PM/bind_bridge/primary | [16, 18] | 180 | 100% / 89% | 10% | 63% (61%) | 59% (50%) | 41% (30%) | 26% (14%) | 29% (18%) | written |
| PM/bind_bridge/secondary | [16, 18] | 180 | 100% / 89% | 10% | 63% (61%) | 59% (50%) | 41% (30%) | 26% (14%) | 29% (18%) | written |
| PM/bridge_word/primary | [16, 18] | 180 | 100% / 89% | 9% | 62% (60%) | 58% (49%) | 38% (26%) | 25% (14%) | 28% (16%) | written |
| PM/bridge_word/secondary | [16, 18] | 180 | 100% / 89% | 9% | 62% (60%) | 58% (49%) | 38% (26%) | 25% (14%) | 28% (16%) | written |
| PM/context/primary | [16, 18] | 180 | 100% / 100% | 100% | 62% (63%) | 68% (59%) | 58% (42%) | 34% (12%) | 41% (21%) | written |
| PM/context/secondary | [16, 18] | 180 | 100% / 100% | 100% | 62% (63%) | 68% (59%) | 58% (42%) | 34% (12%) | 41% (21%) | written |

Write cells: mean frac of the way to C (flips).
