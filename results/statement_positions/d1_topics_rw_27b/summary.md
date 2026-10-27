# statement_positions / d1_topics_rw_27b

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "not written"}, "verdict": "H-around supported"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [32, 36, 40] | 120 | 99% / 92% | 100% | 64% (68%) | 2% (0%) | 22% (6%) | 27% (6%) | 46% (21%) | not written |
| PP/context/secondary | [32, 36, 40] | 120 | 99% / 92% | 100% | 64% (68%) | 2% (0%) | 22% (6%) | 27% (6%) | 46% (21%) | not written |
| PM/bind_bridge/primary | [32] | 120 | 85% / 62% | 5% | 69% (69%) | 57% (50%) | 46% (38%) | 22% (11%) | 28% (16%) | written |
| PM/bind_bridge/secondary | [32] | 120 | 85% / 62% | 5% | 69% (69%) | 57% (50%) | 46% (38%) | 22% (11%) | 28% (16%) | written |
| PM/bridge_word/primary | [32] | 120 | 85% / 62% | 5% | 67% (69%) | 56% (49%) | 44% (36%) | 20% (9%) | 26% (15%) | written |
| PM/bridge_word/secondary | [32] | 120 | 85% / 62% | 5% | 67% (69%) | 56% (49%) | 44% (36%) | 20% (9%) | 26% (15%) | written |
| PM/context/primary | [32, 36] | 120 | 99% / 92% | 99% | 66% (67%) | 62% (57%) | 57% (44%) | 28% (10%) | 38% (16%) | written |
| PM/context/secondary | [32, 36] | 120 | 99% / 92% | 99% | 66% (67%) | 62% (57%) | 57% (44%) | 28% (10%) | 38% (16%) | written |

Write cells: mean frac of the way to C (flips).
