# code_positions / d1code_smoke_rw_27b

Claims: {"KL": {"jspace": {"statement_verdicts": {"bind_bridge": "around", "context": "around"}, "positive_control": {"bind_bridge": "around", "context": "inconclusive"}, "jspace_half": "H-around but positive control fails (not interpretable)"}, "lens_write": {"bind_bridge": "inconclusive", "context": null}, "verdict": "neither (mixed)"}}

| family/set/window | layers | n | read top-10 / top-1 | X top-10 | copy | lens x1 | lens x4 | random x4 | lens x16 | write verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| KL/bind_bridge/primary | [32] | 2 | 100% / 50% | 0% | 99% (100%) | 0% (0%) | 28% (0%) | 8% (0%) | 55% (0%) | inconclusive |
| KL/bind_bridge/secondary | [32] | 2 | 100% / 50% | 0% | 99% (100%) | 0% (0%) | 28% (0%) | 8% (0%) | 55% (0%) | inconclusive |
| KR/bind_bridge/primary | [32] | 2 | 100% / 50% | 0% | 100% (100%) | 93% (50%) | 102% (100%) | 14% (0%) | 35% (0%) | written |
| KR/bind_bridge/secondary | [32] | 2 | 100% / 50% | 0% | 100% (100%) | 93% (50%) | 102% (100%) | 14% (0%) | 35% (0%) | written |

Write cells: mean frac of the way to C (flips).
