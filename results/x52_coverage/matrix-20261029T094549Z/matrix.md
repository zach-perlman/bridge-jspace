# Batch 52 C: model coverage matrix, full grid (20261029T094549Z)

Built at cedd7546 from this checkout (amendments 2-3: every test with a card or claim on the depth page; the 10 key rows first, in Dan's order). Status: done / partial / running / queued / missing / not tested (reason) / not designed. Coverage cells read what has landed here (verdict folders, run folders, the job ledgers); 'queued' means queued or running with no ledger entry pulled yet. Coverage verdicts carry no prediction (rules first scored on the 9B / 27B / Muse). Every result UNVERIFIED until hand-checked. Each cell's sources are in matrix.json.

Nemotron 3.5 Bolt: out of scope: only a J-lens exists, no J++ lens (amendment 2; every depth test uses J++ atoms). Checked 28 Oct ~23:15 UTC: no J++ file under cache/nemotron-3.5-bolt/lenses/jpp/ on mats, speedup or another; the H200 box it was fit on is unreachable.

Lightning's gate: the main test's gate on all 516 scenes (lookup 0.957, recall 0.816), chosen after the 60-scene pre-check was seen (lookup 0.883, recall 0.783: failed) — hollow mark (Dan 01:10); layer L14 by amendment 1 (results/x51_lightning/nem35l_x52_layer_r2); every Lightning cell carries it.

| test | 27B | Lightning | 9B | Muse |
|---|---|---|---|---|
| 1. Conflict test (main test, at L) | **done** (not confirmed (lookup 0.14 > 0.10; recall 0.74)) | **done** (decided at L14; 3 arms at all 13 swept layers) | **done** (confirmed) | **done** (confirmed) |
| 2. Answer control (51.12 E1) | **done** (recall: the entity) | **done** | **done** (recall: the entity) | **done** (answer word not read) |
| 3. Routes test (identity / position / value; no address; address alone) | **done** (0.66 / 0.34 / 0.00; alone fails) | **done** | **done** | **done** |
| 4. Address swap by dose (x8_write, s = 1 / 2 / 4) | **done** (target share at s = 1 / 2 / 4: 0.01 / 0.24 / 0.50) | **done** (target share at s = 1 / 2 / 4: 0.03 / 0.50 / 0.69) | **done** (target share at s = 1 / 2 / 4: 0.02 / 0.46 / 0.73) | **done** (target share at s = 1 / 2 / 4: 0.05 / 0.52 / 0.52) |
| 5a. Order split (descriptive) | **done** | **done** (CPU from the conflict test's outcomes) | **done** | **done** |
| 5b. Copy test (45q) | **done** (holds) | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** (holds) | **done** (holds) |
| 6. Anatomy by layer (47.8) | **done** (full grid) | **done** (every 4th layer L2-L50) | **done** | **done** |
| 7. Ladder (49.2, rungs 1-6) | **done** (rungs 1-6, rung 6 at Zach's L32-40) | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** | **done** (rung 6 in Zach's L36-42 (49.2 ran it at L23-29)) |
| 8. Lens readout with the item-change control (47.0) | **done** | **done** | **done** | **done** |
| 9. Last-token read / write (51.10) | **done** | **done** | **done** | **done** |
| 10. Attention under the swap (49.7) | **done** | **done** (attention blocks 19 / 26 / 33 / 42 after L14 (6 of 52 blocks)) | **done** | **done** |
| Split in other texts: varied scenes (x0b) | **done** | **done** | **done** | **done** |
| Split in other texts: natural passages (x5) | **done** | **not tested**: its gate failed ({'PP': 0.7701149425287356, 'PM': 0.896551724137931}, eligible 36); no lowered rerun (the spec's rule) | **done** (gate lowered after the data) | **done** |
| Dose curves, a part alone (51.1) | **done** | **done** | **done** | **done** |
| Zeroing at one layer (47.5) | **done** | **done** (L14 and L14..17; the 60 dev scenes kept out) | **done** | **done** |
| Earlier mention (45p) | **done** | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) | **done** | **done** |
| E3: identity route outside the lens (47.1 atom slices) | **done** | **done** | **done** | **done** |
| E6: the address probe (x0_probe v4) | **done** | **done** | **done** | **done** |
| E6: the swap after neutral sentences (47.16 distance) | **done** | **done** | **done** | **done** (x47_16_muse was cancelled by Dan mid-run (batch 49 amendment 1; no outcomes); r2 re-opens it under amendment 2 (flagged)) |
| E7: six lockers, one code per slot (47.2) | **done** | **done** | **done** | **done** |
| E8: the report prompt (47.10) | **done** | **not tested**: the cited verdict lists Lightning as not tested (results/x47_report/x52_report-20261029T023828Z) | **not tested**: the cited verdict lists 9B as not tested (results/x47_report/x47_10-20261028T113109Z) | **not tested**: the cited verdict lists Muse as not tested (results/x47_report/x47_10-20261028T113109Z) |
| E11: token by layer map (47.D1) | **done** | **partial**: the main design only; the clean design (the decisive cell) not tested: gate fails | **done** | **done** |
| E11: lookups carried before L (47.4 cumulative) | **done** | **partial**: the main design only; the clean design not tested: gate fails | **done** | **done** |
| E12: address persistence across depth (D4, CPU) | **done** (CPU from x47_anatomy_27b's cache) | **done** (CPU from Lightning's anatomy cache (on its box)) | **done** | **done** |
| Part V: Zach's passages Z1 / Z2 (x50) | **done** | **done** (Z1 done; Z2 done) | **done** | **done** |
| Part V: Zach's passages Z3 (routes on his passages) | **done** (at L32 (X0's layer = the start of his band L32-40)) | **done** (at L14 and L27) | **done** | **done** |
| Described bridge (47.3, and 51.12's cue r2) | **done** | **not tested**: the cited verdict lists Lightning as not tested (gate: O's read accuracy {'PP': 0.7228571428571429, 'PM': 0.87} (bar 0.8), eligible 301; results/x47_cue/x52_cue-20261029T023827Z); was: 47.3 done; 51.12 cue r2 queued (x52_lightning_cue_answer (queued or running; no ledger entry here yet)) | **done** | **partial**: 47.3 done; 51.12's cue r2 not run on Muse (9B / 27B only by design) |
| Report of slot 1, reworded (49.6) | **done** | **done** (the 9B / 27B design; read per model, the action is the 9B's) | **done** (the deciding model) | **not designed**: designed for the 9B and 27B (conservative, Dan 01:10) |
| Address refit per text format (x45d) | **done** | **done** | **done** | **done** |
| The lookup's errors are not address errors (47.13) | **done** | **done** (count (CPU) then the verdict) | **done** | **done** |
| Failed: the J++ part keys the attribute; late MLPs (48.2 enrichment) | **done** (A and B) | **partial**: A only; B not tested: it ablates each block's MLP and NemotronH has none (MoE blocks are separate) | **done** | **done** |
| Failed: a person mark at the locker sentence (48.3 bind) | **done** | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) (48.3 reads the 45m scenes too) | **done** | **done** |
| Failed: copying heads pass the rest (48 heads) | **done** | **done** (attention blocks after L14 (NemotronH port)) | **done** | **done** |
| Failed: the address as the recall's second route (48 route2) | **done** | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) (route2 reads the 45m scenes) | **done** | **done** |
| Failed: blocking the pick sentence (47.6 edges) | **done** | **not tested**: the edge knock-out (knockout.py) is not ported to NemotronH's Mamba-2 blocks | **done** | **done** |
| Failed: the second hop's key token (47.15 source) | **done** | **not tested**: its gate failed (no placement / condition passed; see gate.json); no lowered rerun (the spec's rule) | **missing**: the cited verdict lists 9B as pending (no run given; results/x47_source/x47_15-20261028T142722Z) | **not tested**: the cited verdict lists Muse as not tested (the gate failed; results/x47_source/x47_15-20261028T142722Z) |
| Failed: the address is the same for any kind of item (47.11 agnostic) | **done** | **done** | **done** | **done** |
| Chained addresses (47.14) | **done** | **not tested**: the cited verdict lists Lightning as not tested (the gate missed (see gate.json); results/x47_chain/x52_chain-20261029T023424Z) | **done** | **done** |
| What is left of the route; the value (47.7) | **done** | **partial**: (a) not tested (its gate failed (no placement / condition passed; see gate.json); no lowered rerun (the spec's rule)); (c) done | **missing**: the cited verdict lists 9B as pending (the run has no manifest or outcomes here; results/x47_value/x47_7a-20261028T131819Z) | **missing**: the cited verdict lists Muse as pending (the run has no manifest or outcomes here; results/x47_value/x47_7a-20261028T131819Z) |
| Gain map (49.1) | **done** | **done** | **done** | **done** |
| Pooled person probe (49.3) | **done** | **not tested**: the clean one-pick design's gate fails on Lightning (recall 0.751 < 0.80; amendment 1: no gate change) (49.3 reads the 45m scenes) | **done** | **done** |
| DAS by position (49.x das_pos) | **not designed**: 9B only by design | **not designed**: 9B only by design | **done** | **not designed**: 9B only by design |
| Learned subspaces (48 DAS; 51.3 DAS at scale) | **done** (51.3 done; 48.1 done) | **not tested**: DAS trains through the model's backward, unverified through NemotronH's Mamba-2 kernels; its recall half needs the clean design (gate fails) | **done** | **done** |
| Joint head ablation under the swap (51.2) | **done** | **done** | **done** | **done** |
| The address at the last token (51.4) | **done** | **done** | **done** | **done** |
| Anatomy on Zach's passages (51.5) | **done** | **not designed**: the test was designed for the 9B and 27B; amendment 2's grid adds no new design | **done** | **not designed**: designed for the 9B and 27B (conservative, Dan 01:10) |
| Z1 on the full carrier (51.7) | **done** | **done** | **done** | **not designed**: designed for the 9B and 27B (conservative, Dan 01:10) |
| What is the address: dimension, methods, geometry (51.11) | **partial**: part 2 only by design (parts 1, 3 not designed for the 27B) | **not tested**: DAS trains through the model's backward, unverified through NemotronH's Mamba-2 kernels; its recall half needs the clean design (gate fails) | **done** | **done** |
| Answer-direction control on Zach's Z2 (51.12 Z2) | **done** | **not designed**: the test was designed for the 9B and 27B; amendment 2's grid adds no new design | **done** | **not designed**: designed for the 9B and 27B (conservative, Dan 01:10) |

Counts per model: 27B {'done': 47, 'not designed': 1, 'partial': 1}; Lightning {'done': 28, 'not tested': 14, 'partial': 4, 'not designed': 3}; 9B {'done': 46, 'not tested': 1, 'missing': 2}; Muse {'done': 40, 'not tested': 2, 'partial': 1, 'not designed': 5, 'missing': 1}

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
- Report of slot 1, reworded (49.6): jobs/c3/batch49.yaml 49.6
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
