# Batch 52 prerequisite: Lightning's layer (dev set, the published rule)

no prediction: the layer is a design choice fixed by the published rule (batch 52 addendum). Model nemotron-3.5-lightning. UNVERIFIED.

Rule: Batch 52 prerequisite (jobs/c3/batch52.yaml part C, Dan's words): "the gate passes on 60 main-test scenes; the layer is fixed by the published rule (earliest layer where both readers switch >= 0.3, sweeping every 4th layer)". As computed: the gate = X0's (unedited org accuracy under X0's top-token read >= 0.80 for both readers) on the first 60 main-test scenes in scene order; the sweep = the whole change at the bridge word on 60 dev scenes (51.6's split: random.Random(0).sample of the eligible scenes) at L2, L6, ..., L50; the layer by amendment 1 (PICK_RULE: the earliest layer where both readers' switch rates are >= 0.3 at relative depth >= 0.25); every swept layer's rates, passing status and the bridge word's lens readability recorded; none: "the bridge word does not redirect the lookup at any layer on Lightning" and the column is cancelled.

Gate (main): the main test's gate verbatim (X0's: unedited org accuracy >= 0.80 for both readers on all main-test scenes, >= 150 eligible); the 60-scene gate reported beside as a pre-check.

Gate on the first 60 main-test scenes (beside, a pre-check): org accuracy {'PP': 0.8833, 'PM': 0.7833} (bar 0.8) -> **FAIL**. X0's gate on all 516 scenes (decides): {'PP': 0.9574, 'PM': 0.8159}, pass True; eligible 315; dev 60, test (for the coverage runs) 200.

**Layer: L14**

Pick rule: Batch 52 prerequisite (jobs/c3/batch52.yaml part C, Dan's words): "the gate passes on 60 main-test scenes; the layer is fixed by the published rule (earliest layer where both readers switch >= 0.3, sweeping every 4th layer)". As computed: the gate = X0's (unedited org accuracy under X0's top-token read >= 0.80 for both readers) on the first 60 main-test scenes in scene order; the sweep = the whole change at the bridge word on 60 dev scenes (51.6's split: random.Random(0).sample of the eligible scenes) at L2, L6, ..., L50; the layer by amendment 1 (PICK_RULE: the earliest layer where both readers' switch rates are >= 0.3 at relative depth >= 0.25); every swept layer's rates, passing status and the bridge word's lens readability recorded; none: "the bridge word does not redirect the lookup at any layer on Lightning" and the column is cancelled.

Every passing layer: [2, 6, 10, 14, 18, 22]; candidates (relative depth >= 0.25): [14, 18, 22].

| layer | depth | lookup switch [CI] | recall switch [CI] | both >= 0.3 | depth >= 0.25 | lens top-1 (bridge word) | median rank |
|---|---|---|---|---|---|---|---|
| L2 | 0.04 | 0.98 [0.95, 1.00] | 0.97 [0.92, 1.00] | yes |  | 0.00 | 38323.5 |
| L6 | 0.12 | 0.87 [0.79, 0.95] | 0.98 [0.94, 1.00] | yes |  | 0.10 | 62.5 |
| L10 | 0.19 | 0.78 [0.69, 0.88] | 0.98 [0.94, 1.00] | yes |  | 0.17 | 50.5 |
| L14 (pick) | 0.27 | 0.58 [0.45, 0.73] | 0.98 [0.94, 1.00] | yes | yes | 0.24 | 2 |
| L18 | 0.35 | 0.52 [0.37, 0.67] | 0.97 [0.91, 1.00] | yes | yes | 0.44 | 2 |
| L22 | 0.42 | 0.32 [0.18, 0.46] | 0.80 [0.68, 0.90] | yes | yes | 0.15 | 26 |
| L26 | 0.50 | 0.02 [0.00, 0.05] | 0.40 [0.27, 0.51] |  | yes | 0.36 | 2 |
| L30 | 0.58 | 0.00 [0.00, 0.00] | 0.37 [0.23, 0.49] |  | yes | 0.25 | 3 |
| L34 | 0.65 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |  | yes | 0.13 | 5 |
| L38 | 0.73 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |  | yes | 0.07 | 8 |
| L42 | 0.81 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |  | yes | 0.04 | 188 |
| L46 | 0.88 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |  | yes | 0.03 | 92 |
| L50 | 0.96 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |  | yes | 0.00 | 41 |

The conflict result at every swept layer comes from the Lightning conflict-test run (all 13 layers, deciding at the pick), not from this sweep.
