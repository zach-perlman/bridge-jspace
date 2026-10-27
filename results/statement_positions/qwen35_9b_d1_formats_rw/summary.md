# statement_positions / qwen35_9b_d1_formats_rw

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"context": "around"}, "positive_control": {"context": "inside"}, "jspace_half": "H-around"}, "lens_write": {"context": "not written"}, "verdict": "H-around supported"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/context/primary | [16, 18] | 180 | 100% / 96% | 100% | 59% (59%) | 2% (1%) | 15% (3%) | 19% (3%) | 33% (6%) | not written |
| PP/context/secondary | [16, 18] | 180 | 100% / 96% | 100% | 59% (59%) | 2% (1%) | 15% (3%) | 19% (3%) | 33% (6%) | not written |
| PM/bind_bridge/primary | [16, 18] | 180 | 100% / 93% | 21% | 73% (72%) | 64% (64%) | 52% (42%) | 34% (22%) | 39% (25%) | written |
| PM/bind_bridge/secondary | [16, 18] | 180 | 100% / 93% | 21% | 73% (72%) | 64% (64%) | 52% (42%) | 34% (22%) | 39% (25%) | written |
| PM/bridge_word/primary | [16, 18] | 180 | 100% / 93% | 18% | 73% (73%) | 63% (63%) | 49% (38%) | 33% (21%) | 38% (25%) | written |
| PM/bridge_word/secondary | [16, 18] | 180 | 100% / 93% | 18% | 73% (73%) | 63% (63%) | 49% (38%) | 33% (21%) | 38% (25%) | written |
| PM/context/primary | [16, 18] | 180 | 100% / 96% | 100% | 64% (65%) | 65% (62%) | 57% (39%) | 32% (16%) | 40% (19%) | written |
| PM/context/secondary | [16, 18] | 180 | 100% / 96% | 100% | 64% (65%) | 65% (62%) | 57% (39%) | 32% (16%) | 40% (19%) | written |

Write cells: mean frac of the way to C (flips).
