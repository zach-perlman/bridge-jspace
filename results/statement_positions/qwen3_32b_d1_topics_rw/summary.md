# statement_positions / qwen3_32b_d1_topics_rw

Claims: {"BL": "no statement set in transit at the primary layers: H-loc's location premise fails there", "BLR": "no statement set in transit at the primary layers: H-loc's location premise fails there", "PP": {"jspace": {"statement_verdicts": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "positive_control": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "jspace_half": "H-around but positive control fails (not interpretable)"}, "lens_write": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "not written"}, "verdict": "neither (mixed)"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| PP/bind_bridge/primary | [32, 36] | 120 | 6% / 1% | 1% | 72% (71%) | 3% (1%) | 37% (28%) | 31% (20%) | 46% (32%) | inconclusive |
| PP/bind_bridge/secondary | [32, 36] | 120 | 6% / 1% | 1% | 72% (71%) | 3% (1%) | 37% (28%) | 31% (20%) | 46% (32%) | inconclusive |
| PP/bridge_word/primary | [32] | 120 | 2% / 1% | 1% | 87% (89%) | 4% (2%) | 35% (22%) | 31% (18%) | 38% (22%) | inconclusive |
| PP/bridge_word/secondary | [32] | 120 | 2% / 1% | 1% | 87% (89%) | 4% (2%) | 35% (22%) | 31% (18%) | 38% (22%) | inconclusive |
| PP/context/primary | [32, 36, 40] | 120 | 24% / 8% | 22% | 99% (100%) | 2% (1%) | 39% (25%) | 43% (28%) | 51% (21%) | not written |
| PP/context/secondary | [32, 36, 40] | 120 | 24% / 8% | 22% | 99% (100%) | 2% (1%) | 39% (25%) | 43% (28%) | 51% (21%) | not written |
| PM/bind_bridge/primary | [32, 36, 40] | 120 | 10% / 2% | 2% | 86% (83%) | 23% (18%) | 50% (35%) | 30% (15%) | 48% (29%) | inconclusive |
| PM/bind_bridge/secondary | [32, 36, 40] | 120 | 10% / 2% | 2% | 86% (83%) | 23% (18%) | 50% (35%) | 30% (15%) | 48% (29%) | inconclusive |
| PM/bridge_word/primary | [32, 36, 40] | 120 | 10% / 2% | 2% | 84% (81%) | 22% (18%) | 39% (26%) | 23% (10%) | 33% (15%) | inconclusive |
| PM/bridge_word/secondary | [32, 36, 40] | 120 | 10% / 2% | 2% | 84% (81%) | 22% (18%) | 39% (26%) | 23% (10%) | 33% (15%) | inconclusive |
| PM/context/primary | [32, 36, 40] | 120 | 24% / 8% | 22% | 100% (98%) | 31% (23%) | 64% (38%) | 42% (14%) | 56% (30%) | written |
| PM/context/secondary | [32, 36, 40] | 120 | 24% / 8% | 22% | 100% (98%) | 31% (23%) | 64% (38%) | 42% (14%) | 56% (30%) | written |

Write cells: mean frac of the way to C (flips).
