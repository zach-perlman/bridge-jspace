# statement_positions / qwen35_122b_d1_topics2_rw

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inside"}, "positive_control": {"bind_bridge": "inside", "bridge_word": "inside", "context": "inside"}, "jspace_half": "H-loc"}, "lens_write": {"bind_bridge": "written", "bridge_word": "written", "context": "written"}, "verdict": "H-loc supported"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [24, 27, 30] | 180 | 100% / 98% | 14% | 80% (84%) | 56% (56%) | 58% (54%) | 20% (9%) | 52% (39%) | written |
| PP/bind_bridge/secondary | [24, 27, 30] | 180 | 100% / 98% | 14% | 80% (84%) | 56% (56%) | 58% (54%) | 20% (9%) | 52% (39%) | written |
| PP/bridge_word/primary | [24, 27, 30] | 180 | 100% / 98% | 12% | 75% (79%) | 52% (51%) | 53% (52%) | 18% (9%) | 45% (36%) | written |
| PP/bridge_word/secondary | [24, 27, 30] | 180 | 100% / 98% | 12% | 75% (79%) | 52% (51%) | 53% (52%) | 18% (9%) | 45% (36%) | written |
| PP/context/primary | [24, 27, 30] | 180 | 100% / 99% | 100% | 99% (99%) | 35% (32%) | 51% (39%) | 34% (17%) | 49% (21%) | written |
| PP/context/secondary | [24, 27, 30] | 180 | 100% / 99% | 100% | 99% (99%) | 35% (32%) | 51% (39%) | 34% (17%) | 49% (21%) | written |
| PM/bind_bridge/primary | [24, 27, 30] | 180 | 100% / 98% | 14% | 99% (95%) | 86% (78%) | 95% (81%) | 14% (5%) | 66% (51%) | written |
| PM/bind_bridge/secondary | [24, 27, 30] | 180 | 100% / 98% | 14% | 99% (95%) | 86% (78%) | 95% (81%) | 14% (5%) | 66% (51%) | written |
| PM/bridge_word/primary | [24, 27, 30] | 180 | 100% / 98% | 12% | 98% (94%) | 84% (77%) | 92% (77%) | 13% (4%) | 58% (44%) | written |
| PM/bridge_word/secondary | [24, 27, 30] | 180 | 100% / 98% | 12% | 98% (94%) | 84% (77%) | 92% (77%) | 13% (4%) | 58% (44%) | written |
| PM/context/primary | [24, 27, 30] | 180 | 100% / 99% | 100% | 99% (97%) | 89% (81%) | 95% (80%) | 20% (7%) | 75% (61%) | written |
| PM/context/secondary | [24, 27, 30] | 180 | 100% / 99% | 100% | 99% (97%) | 89% (81%) | 95% (80%) | 20% (7%) | 75% (61%) | written |

Write cells: mean frac of the way to C (flips).
