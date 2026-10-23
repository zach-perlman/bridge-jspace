# statement_positions / qwen35_122b_d1_formats_rw

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inside"}, "positive_control": {"bind_bridge": "inside", "bridge_word": "inside", "context": "inside"}, "jspace_half": "H-loc"}, "lens_write": {"bind_bridge": "written", "bridge_word": "written", "context": "written"}, "verdict": "H-loc supported"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [24, 27, 30] | 180 | 100% / 98% | 43% | 86% (88%) | 67% (69%) | 67% (64%) | 18% (7%) | 56% (44%) | written |
| PP/bind_bridge/secondary | [24, 27, 30] | 180 | 100% / 98% | 43% | 86% (88%) | 67% (69%) | 67% (64%) | 18% (7%) | 56% (44%) | written |
| PP/bridge_word/primary | [24, 27, 30] | 180 | 100% / 98% | 13% | 74% (74%) | 55% (54%) | 59% (57%) | 12% (4%) | 53% (47%) | written |
| PP/bridge_word/secondary | [24, 27, 30] | 180 | 100% / 98% | 13% | 74% (74%) | 55% (54%) | 59% (57%) | 12% (4%) | 53% (47%) | written |
| PP/context/primary | [24, 27, 30] | 180 | 100% / 100% | 100% | 100% (100%) | 47% (48%) | 62% (54%) | 25% (10%) | 54% (26%) | written |
| PP/context/secondary | [24, 27, 30] | 180 | 100% / 100% | 100% | 100% (100%) | 47% (48%) | 62% (54%) | 25% (10%) | 54% (26%) | written |
| PM/bind_bridge/primary | [24, 27, 30] | 180 | 100% / 98% | 43% | 95% (96%) | 81% (81%) | 92% (84%) | 11% (3%) | 68% (58%) | written |
| PM/bind_bridge/secondary | [24, 27, 30] | 180 | 100% / 98% | 43% | 95% (96%) | 81% (81%) | 92% (84%) | 11% (3%) | 68% (58%) | written |
| PM/bridge_word/primary | [24, 27, 30] | 180 | 100% / 98% | 13% | 91% (94%) | 78% (79%) | 90% (84%) | 10% (3%) | 69% (61%) | written |
| PM/bridge_word/secondary | [24, 27, 30] | 180 | 100% / 98% | 13% | 91% (94%) | 78% (79%) | 90% (84%) | 10% (3%) | 69% (61%) | written |
| PM/context/primary | [24, 27, 30] | 180 | 100% / 100% | 100% | 99% (99%) | 83% (81%) | 94% (87%) | 16% (6%) | 77% (63%) | written |
| PM/context/secondary | [24, 27, 30] | 180 | 100% / 100% | 100% | 99% (99%) | 83% (81%) | 94% (87%) | 16% (6%) | 77% (63%) | written |

Write cells: mean frac of the way to C (flips).
