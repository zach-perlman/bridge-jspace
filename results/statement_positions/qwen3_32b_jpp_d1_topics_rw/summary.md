# statement_positions / qwen3_32b_jpp_d1_topics_rw

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "positive_control": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inconclusive"}, "jspace_half": "H-around but positive control fails (not interpretable)"}, "lens_write": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inconclusive"}, "verdict": "neither (mixed)"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [32, 36] | 120 | 80% / 53% | 4% | 72% (71%) | 4% (2%) | 39% (28%) | 31% (20%) | 46% (32%) | inconclusive |
| PP/bind_bridge/secondary | [32, 36] | 120 | 80% / 53% | 4% | 72% (71%) | 4% (2%) | 39% (28%) | 31% (20%) | 46% (32%) | inconclusive |
| PP/bridge_word/primary | [32] | 120 | 72% / 42% | 3% | 87% (89%) | 6% (2%) | 39% (23%) | 31% (18%) | 39% (22%) | inconclusive |
| PP/bridge_word/secondary | [32] | 120 | 72% / 42% | 3% | 87% (89%) | 6% (2%) | 39% (23%) | 31% (18%) | 39% (22%) | inconclusive |
| PP/context/primary | [32, 36, 40] | 120 | 99% / 73% | 98% | 99% (100%) | 3% (1%) | 41% (29%) | 43% (28%) | 49% (21%) | inconclusive |
| PP/context/secondary | [32, 36, 40] | 120 | 99% / 73% | 98% | 99% (100%) | 3% (1%) | 41% (29%) | 43% (28%) | 49% (21%) | inconclusive |
| PM/bind_bridge/primary | [32, 36, 40] | 120 | 80% / 53% | 5% | 86% (83%) | 28% (20%) | 53% (41%) | 30% (15%) | 48% (29%) | inconclusive |
| PM/bind_bridge/secondary | [32, 36, 40] | 120 | 80% / 53% | 5% | 86% (83%) | 28% (20%) | 53% (41%) | 30% (15%) | 48% (29%) | inconclusive |
| PM/bridge_word/primary | [32, 36, 40] | 120 | 80% / 53% | 5% | 84% (81%) | 28% (20%) | 42% (31%) | 23% (10%) | 33% (15%) | inconclusive |
| PM/bridge_word/secondary | [32, 36, 40] | 120 | 80% / 53% | 5% | 84% (81%) | 28% (20%) | 42% (31%) | 23% (10%) | 33% (15%) | inconclusive |
| PM/context/primary | [32, 36, 40] | 120 | 99% / 73% | 98% | 100% (98%) | 38% (28%) | 68% (47%) | 42% (14%) | 57% (31%) | written |
| PM/context/secondary | [32, 36, 40] | 120 | 99% / 73% | 98% | 100% (98%) | 38% (28%) | 68% (47%) | 42% (14%) | 57% (31%) | written |

Write cells: mean frac of the way to C (flips).
