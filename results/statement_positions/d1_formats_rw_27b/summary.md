# statement_positions / d1_formats_rw_27b

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "not written"}, "verdict": "H-around supported"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [32, 36, 40] | 180 | 99% / 95% | 100% | 72% (76%) | 2% (0%) | 17% (4%) | 19% (4%) | 35% (10%) | not written |
| PP/context/secondary | [32, 36, 40] | 180 | 99% / 95% | 100% | 72% (76%) | 2% (0%) | 17% (4%) | 19% (4%) | 35% (10%) | not written |
| PM/bind_bridge/primary | [32, 36] | 180 | 98% / 76% | 16% | 73% (76%) | 47% (45%) | 44% (36%) | 15% (5%) | 25% (14%) | written |
| PM/bind_bridge/secondary | [32, 36] | 180 | 98% / 76% | 16% | 73% (76%) | 47% (45%) | 44% (36%) | 15% (5%) | 25% (14%) | written |
| PM/bridge_word/primary | [32, 36] | 180 | 98% / 76% | 14% | 72% (75%) | 46% (44%) | 44% (38%) | 13% (4%) | 22% (12%) | written |
| PM/bridge_word/secondary | [32, 36] | 180 | 98% / 76% | 14% | 72% (75%) | 46% (44%) | 44% (38%) | 13% (4%) | 22% (12%) | written |
| PM/context/primary | [32, 36, 40] | 180 | 99% / 95% | 100% | 68% (68%) | 38% (34%) | 52% (44%) | 18% (4%) | 32% (11%) | inconclusive |
| PM/context/secondary | [32, 36, 40] | 180 | 99% / 95% | 100% | 68% (68%) | 38% (34%) | 52% (44%) | 18% (4%) | 32% (11%) | inconclusive |

Write cells: mean frac of the way to C (flips).
