# Batch 52 C: model coverage matrix, full grid (20261029T000836Z)

Built at 2ca7e5e8 (amendment 2: every test with a card or claim on the depth page; the 10 key rows first, in Dan's order). Status: done / partial / running / queued / missing / not tested (reason) / not designed. Every result UNVERIFIED until hand-checked. Each cell's source is in matrix.json.

Nemotron 3.5 Bolt: out of scope: only a J-lens exists, no J++ lens (amendment 2; every depth test uses J++ atoms). Checked 28 Oct ~23:15 UTC: no J++ file under cache/nemotron-3.5-bolt/lenses/jpp/ on mats, speedup or another; the H200 box it was fit on is unreachable.

Lightning's gate: the main test's gate on all 516 scenes (lookup 0.957, recall 0.816), chosen after the 60-scene pre-check was seen (lookup 0.883, recall 0.783: failed) — hollow mark (Dan 01:10); layer L14 by amendment 1 (results/x51_lightning/nem35l_x52_layer_r2).

| test | 27B | Lightning | 9B | Muse |
|---|---|---|---|---|
| 1. Conflict test (main test, at L) | **done** (not confirmed (lookup 0.14 > 0.10; recall 0.74)) | **queued**: x52_lightning_conflict, speedup first: 3 arms at all 13 swept layers, decided at L14; Lightning's gate: the main test's gate on all 516 scenes (lookup 0.957, recall 0.816), chosen after the 60-scene pre-check was seen (lookup 0.883, recall 0.783: failed) — hollow mark (Dan 01:10); layer L14 by amendment 1 (results/x51_lightning/nem35l_x52_layer_r2) | **done** (confirmed) | **done** (confirmed) |
| 2. Answer control (51.12 E1) | **done** (recall: the entity) | **missing**: missing: Lightning chain, spec in Dan's order (reads the committed L14) | **done** (recall: the entity) | **done** (answer word not read) |
| 3. Routes test (identity / position / value; no address; address alone) | **done** (0.66 / 0.34 / 0.00; alone fails) | **missing**: missing: Lightning chain, spec in Dan's order (reads the committed L14) | **done** | **done** |
| 4. Address swap by dose (x8_write, s = 1 / 2 / 4) | **done** (0.01 / 0.24 / 0.50) | **missing**: missing: Lightning chain, spec in Dan's order (reads the committed L14); needs the routes test's items | **done** (0.05 / 0.52 / 0.52) | **done** (0.02 / 0.46 / 0.73) |
| 5a. Order split (descriptive) | **done** | **missing**: CPU from the conflict test's outcomes once it lands | **done** | **done** |
| 5b. Copy test (45q) | **done** (holds) | **not tested**: not tested: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** (holds) | **done** (holds) |
| 6. Anatomy by layer (47.8) | **queued**: on record a reduced grid (9 of 15 layers); full grid x47_8_27b on mats (run x47_anatomy_27b) | **missing**: missing: Lightning chain, spec in Dan's order (reads the committed L14) | **done** | **done** |
| 7. Ladder (49.2, rungs 1-6) | **queued**: on record rungs 1-2 only; rungs 1-6 (rung 6 at Zach's L32-40) x52_ladder_27b on another (the speedup copy was stopped after 2 min) | **not tested**: not tested: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** | **queued**: on record, rung 6 at L23-29; rung 6 in Zach's L36-42: x52_ladder_muse on mats (behind part B) |
| 8. Lens readout with the item-change control (47.0) | **done** | **missing**: missing: Lightning chain, spec in Dan's order (reads the committed L14); needs x8_write's items | **done** | **done** |
| 9. Last-token read / write (51.10) | **done** | **missing**: missing: Lightning chain, spec in Dan's order (reads the committed L14) | **done** | **done** |
| 10. Attention under the swap (49.7) | **done** | **missing**: missing: Lightning chain, spec in Dan's order (reads the committed L14); full attention at 6 of 52 blocks only | **done** | **done** |
| Split in other texts: varied scenes (x0b) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Split in other texts: natural passages (x5) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** (gate lowered after the data) | **done** |
| Dose curves, a part alone (51.1) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Zeroing at one layer (47.5) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Earlier mention (45p) | **done** | **not tested**: not tested: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** | **done** |
| E3: identity route outside the lens (47.1 atom slices) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| E6: the address probe (x0_probe v4) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| E6: the swap after neutral sentences (47.16 distance) | **missing**: 27B gap: spec to write (mats) | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| E7: six lockers, one code per slot (47.2) | **queued**: x47_2_27b on another (behind part B and the 27B ladder) | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| E8: the report prompt (47.10) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| E11: token by layer map (47.D1) | **queued**: x47_d1_27b on mats (run x47_depthmap_27b) | **not tested**: not tested: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** | **done** |
| E11: lookups carried before L (47.4 cumulative) | **missing**: 27B gap: spec to write (mats) | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| E12: address persistence across depth (D4, CPU) | **missing**: CPU from x47_anatomy_27b's cache once it lands | **missing**: CPU after Lightning's anatomy | **done** | **done** |
| Part V: Zach's passages Z1 / Z2 (x50) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Part V: Zach's passages Z3 (routes on his passages) | **missing**: 27B gap: spec to write | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Described bridge (47.3, and 51.12's cue r2) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **partial**: 47.3 done; 51.12's cue r2 not run on Muse (9B / 27B only by design) |
| One question, two instructions (49.6) | **done** | **missing**: missing: Lightning, after the 10 key rows | **not tested**: ran; the gate failed (README: the others miss the gate) | **missing**: 9B / Muse gap: not run on Muse |
| Address refit per text format (x45d) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| The lookup's errors are not address errors (47.13) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Failed: the J++ part keys the attribute; late MLPs (48.2 enrichment) | **missing**: 27B gap: spec to write | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Failed: a person mark at the locker sentence (48.3 bind) | **missing**: 27B gap: spec to write | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Failed: copying heads pass the rest (48 heads) | **missing**: 27B gap: spec to write | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Failed: the address as the recall's second route (48 route2) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Failed: blocking the pick sentence (47.6 edges) | **missing**: 27B gap: spec to write | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Failed: the second hop's key token (47.15 source) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Failed: the address is the same for any kind of item (47.11 agnostic) | **missing**: 27B gap: spec to write | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Chained addresses (47.14) | **missing**: 27B gap: spec to write | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| What is left of the route; the value (47.7) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Gain map (49.1) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Pooled person probe (49.3) | **missing**: 27B gap: spec to write | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| DAS by position (49.x das_pos) | **not designed**: 9B only by design | **not designed**: 9B only by design | **done** | **not designed**: 9B only by design |
| Learned subspaces (48 DAS; 51.3 DAS at scale) | **partial**: 51.3 done; 48's DAS not run on the 27B (51.3 supersedes it) | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Joint head ablation under the swap (51.2) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| The address at the last token (51.4) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Anatomy on Zach's passages (51.5) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **missing**: 9B / Muse gap (51.5 designed for the 9B and 27B) |
| Z1 on the full carrier (51.7) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **missing**: 9B / Muse gap (51.7 designed for the 9B and 27B) |
| What is the address: dimension, methods, geometry (51.11) | **partial**: part 2 only by design (parts 1, 3 not designed for the 27B) | **missing**: missing: Lightning, after the 10 key rows | **done** | **done** |
| Answer-direction control on Zach's Z2 (51.12 Z2) | **done** | **missing**: missing: Lightning, after the 10 key rows | **done** | **missing**: 9B / Muse gap (Z2 designed for the 9B and 27B) |

Counts per model: 27B {'done': 31, 'queued': 4, 'missing': 11, 'not designed': 1, 'partial': 2}; Lightning {'queued': 1, 'missing': 43, 'not tested': 4, 'not designed': 1}; 9B {'done': 48, 'not tested': 1}; Muse {'done': 42, 'queued': 1, 'partial': 1, 'missing': 4, 'not designed': 1}

## Rules / designs per row

- 1. Conflict test (main test, at L): X0 (jobs/c3/x0_necessity_27b_chat.yaml)
- 2. Answer control (51.12 E1): jobs/c3/batch51.yaml 51.12 r2
- 3. Routes test (identity / position / value; no address; address alone): x6_routes (E5/E6)
- 4. Address swap by dose (x8_write, s = 1 / 2 / 4): x8_write (Q44.1-3)
- 5a. Order split (descriptive): x0_composition split-by-order
- 5b. Copy test (45q): jobs/c3/batch45.yaml 45b/45q
- 6. Anatomy by layer (47.8): jobs/c3/batch47.yaml 47.8
- 7. Ladder (49.2, rungs 1-6): jobs/c3/batch49.yaml 49.2
- 8. Lens readout with the item-change control (47.0): 47.0 (descriptive)
- 9. Last-token read / write (51.10): jobs/c3/batch51.yaml addendum_2
- 10. Attention under the swap (49.7): jobs/c3/batch49.yaml 49.7
- Split in other texts: varied scenes (x0b): x0b_generalize
- Split in other texts: natural passages (x5): x5_natural
- Dose curves, a part alone (51.1): jobs/c3/batch51.yaml 51.1
- Zeroing at one layer (47.5): jobs/c3/batch47.yaml 47.5
- Earlier mention (45p): jobs/c3/batch45.yaml 45p
- E3: identity route outside the lens (47.1 atom slices): jobs/c3/batch47.yaml 47.1
- E6: the address probe (x0_probe v4): x0_probe
- E6: the swap after neutral sentences (47.16 distance): jobs/c3/batch47.yaml 47.16
- E7: six lockers, one code per slot (47.2): jobs/c3/batch47.yaml 47.2
- E8: the report prompt (47.10): jobs/c3/batch47.yaml 47.10
- E11: token by layer map (47.D1): jobs/c3/batch47.yaml D1
- E11: lookups carried before L (47.4 cumulative): jobs/c3/batch47.yaml 47.4
- E12: address persistence across depth (D4, CPU): jobs/c3/batch47.yaml D4
- Part V: Zach's passages Z1 / Z2 (x50): jobs/c3/batch50 (x50_zach)
- Part V: Zach's passages Z3 (routes on his passages): x50_zach z3
- Described bridge (47.3, and 51.12's cue r2): jobs/c3/batch47.yaml 47.3
- One question, two instructions (49.6): jobs/c3/batch49.yaml 49.6
- Address refit per text format (x45d): x45d
- The lookup's errors are not address errors (47.13): jobs/c3/batch47.yaml 47.13
- Failed: the J++ part keys the attribute; late MLPs (48.2 enrichment): jobs/c3/batch48.yaml 48.2
- Failed: a person mark at the locker sentence (48.3 bind): jobs/c3/batch48.yaml
- Failed: copying heads pass the rest (48 heads): jobs/c3/batch48.yaml
- Failed: the address as the recall's second route (48 route2): jobs/c3/batch48.yaml
- Failed: blocking the pick sentence (47.6 edges): jobs/c3/batch47.yaml 47.6
- Failed: the second hop's key token (47.15 source): jobs/c3/batch47.yaml 47.15
- Failed: the address is the same for any kind of item (47.11 agnostic): jobs/c3/batch47.yaml 47.11
- Chained addresses (47.14): jobs/c3/batch47.yaml 47.14
- What is left of the route; the value (47.7): jobs/c3/batch47.yaml 47.7
- Gain map (49.1): jobs/c3/batch49.yaml 49.1
- Pooled person probe (49.3): jobs/c3/batch49.yaml 49.3
- DAS by position (49.x das_pos): jobs/c3/batch49.yaml
- Learned subspaces (48 DAS; 51.3 DAS at scale): jobs/c3/batch51.yaml 51.3
- Joint head ablation under the swap (51.2): jobs/c3/batch51.yaml 51.2
- The address at the last token (51.4): jobs/c3/batch51.yaml 51.4
- Anatomy on Zach's passages (51.5): jobs/c3/batch51.yaml 51.5
- Z1 on the full carrier (51.7): jobs/c3/batch51.yaml 51.7
- What is the address: dimension, methods, geometry (51.11): jobs/c3/batch51.yaml 51.11
- Answer-direction control on Zach's Z2 (51.12 Z2): jobs/c3/batch51.yaml 51.12
