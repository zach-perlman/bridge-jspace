# Batch 52 prerequisite: Lightning's layer (dev set, the published rule)

no prediction: the layer is a design choice fixed by the published rule (batch 52 addendum). Model nemotron-3.5-lightning. UNVERIFIED.

Rule: Batch 52 prerequisite (jobs/c3/batch52.yaml part C, Dan's words): "the gate passes on 60 main-test scenes; the layer is fixed by the published rule (earliest layer where both readers switch >= 0.3, sweeping every 4th layer)". As computed: the gate = X0's (unedited org accuracy under X0's top-token read >= 0.80 for both readers) on the first 60 main-test scenes in scene order; the sweep = the whole change at the bridge word on 60 dev scenes (51.6's split: random.Random(0).sample of the eligible scenes) at L2, L6, ..., L50; the layer = the earliest where both readers' switch rates are >= 0.3 (point estimates, EPS 1e-9); none: "the bridge word does not redirect the lookup at any layer on Lightning" and the column is cancelled.

Gate on the first 60 main-test scenes: org accuracy {'PP': 0.8833, 'PM': 0.7833} (bar 0.8) -> **FAIL**. X0's gate on all 516 scenes (beside): {'PP': 0.9574, 'PM': 0.8159}, pass True; eligible 315; dev 0, test (for the coverage runs) 0.

**Layer: prerequisite failed: the gate on the first 60 main-test scenes failed**

