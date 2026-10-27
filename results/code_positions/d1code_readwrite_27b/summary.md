# code_positions / d1code_readwrite_27b

Claims: {"KL": {"jspace": {"statement_verdicts": {"bind_bridge": "around", "bridge_word": "around", "context": "around"}, "positive_control": {"bind_bridge": "inconclusive", "bridge_word": "inconclusive", "context": "inconclusive"}, "jspace_half": "H-around but positive control fails (not interpretable)"}, "lens_write": {"bind_bridge": "not written", "bridge_word": "not written", "context": "not written"}, "verdict": "neither (mixed)"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| KL/bind_bridge/primary | [32, 36, 40] | 80 | 100% / 88% | 0% | 87% (99%) | 1% (0%) | 12% (2%) | 8% (0%) | 26% (8%) | not written |
| KL/bind_bridge/secondary | [28, 32, 36, 40] | 80 | 100% / 89% | 0% | 90% (99%) | 1% (0%) | 18% (9%) | 9% (0%) | 33% (12%) | not written |
| KL/bridge_word/primary | [32, 36, 40] | 80 | 100% / 88% | 0% | 87% (99%) | 1% (0%) | 11% (2%) | 8% (0%) | 24% (6%) | not written |
| KL/bridge_word/secondary | [28, 32, 36, 40] | 80 | 100% / 89% | 0% | 90% (99%) | 1% (0%) | 17% (8%) | 8% (0%) | 30% (10%) | not written |
| KL/context/primary | [32, 36, 40] | 80 | 100% / 100% | 100% | 87% (99%) | 1% (0%) | 12% (2%) | 8% (0%) | 26% (9%) | not written |
| KL/context/secondary | [28, 32, 36, 40] | 80 | 100% / 100% | 100% | 91% (99%) | 1% (0%) | 18% (9%) | 9% (0%) | 32% (13%) | not written |
| KR/bind_bridge/primary | [32, 36, 40] | 80 | 100% / 88% | 0% | 76% (83%) | 67% (61%) | 61% (50%) | 15% (9%) | 24% (12%) | written |
| KR/bind_bridge/secondary | [28, 32, 36, 40] | 80 | 100% / 89% | 0% | 82% (88%) | 70% (67%) | 71% (62%) | 15% (8%) | 31% (15%) | written |
| KR/bridge_word/primary | [32, 36, 40] | 80 | 100% / 88% | 0% | 76% (82%) | 66% (60%) | 56% (45%) | 16% (8%) | 21% (12%) | written |
| KR/bridge_word/secondary | [28, 32, 36, 40] | 80 | 100% / 89% | 0% | 81% (87%) | 69% (65%) | 66% (57%) | 15% (7%) | 26% (15%) | written |
| KR/context/primary | [32, 36, 40] | 80 | 100% / 100% | 100% | 76% (84%) | 68% (62%) | 59% (47%) | 15% (9%) | 19% (8%) | written |
| KR/context/secondary | [28, 32, 36, 40] | 80 | 100% / 100% | 100% | 82% (88%) | 72% (68%) | 70% (59%) | 15% (8%) | 27% (12%) | written |

Write cells: mean frac of the way to C (flips).
