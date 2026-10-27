# d5a_head_pointer / d5a_head_pointer_smoke_27b: analysis

EXP d5a_head_pointer_smoke_27b | model Qwen3.6-27B | n={'RL': 6, 'DL': 6, 'RR': 6} org prompts per family (rows: 4 patch settings each) | seeds=[0]

Claim tested: Does the D5a read-out run end to end on the 27B (the CUDA loader, the frozen J-lens, the patched forward with attention capture), with the self-patch a no-op?

Headline: memory → prompt, layer 51, head 22, rows whose answer moved to another statement: looks most at the new answer's statement 64% [50, 88] (Wilson [35, 85]; n=11 / k=6 / t=6); still at the asked statement 36% [12, 50] (Wilson [15, 65]; n=11 / k=6 / t=6)   Baseline: rows whose answer stayed, on the asked statement 69% [50, 85] (Wilson [42, 87]; n=13 / k=6 / t=6)   Control: the J-lens's word read on the same moved rows 18% [0, 43] (Wilson [5, 48]; n=11 / k=6 / t=6); head - lens +45 points [+30, +62] (entity cluster)
Verdict (pre-registered): not judged (moved n=11, kept n=13 < 35)

Controls: memory → prompt, same: answer changed 0% [0, 0] (Wilson [0, 14]; n=24 / k=6 / t=6), head on the asked statement 96% [92, 100] (Wilson [80, 99]; n=24 / k=6 / t=6); memory → prompt, rand: answer changed 0% [0, 0] (Wilson [0, 14]; n=24 / k=6 / t=6), head on the asked statement 100% [100, 100] (Wilson [86, 100]; n=24 / k=6 / t=6); named → prompt, same: answer changed 0% [0, 0] (Wilson [0, 14]; n=24 / k=6 / t=6), head on the asked statement 96% [92, 100] (Wilson [80, 99]; n=24 / k=6 / t=6); named → prompt, rand: answer changed 0% [0, 0] (Wilson [0, 14]; n=24 / k=6 / t=6), head on the asked statement 100% [100, 100] (Wilson [86, 100]; n=24 / k=6 / t=6); memory → memory, same: answer changed 0% [0, 0] (Wilson [0, 14]; n=24 / k=6 / t=6), head on the asked statement 62% [29, 96] (Wilson [43, 79]; n=24 / k=6 / t=6); memory → memory, rand: answer changed 0% [0, 0] (Wilson [0, 14]; n=24 / k=6 / t=6), head on the asked statement 67% [33, 100] (Wilson [47, 82]; n=24 / k=6 / t=6)

Figures: readers.png, readers.svg

Three dumbest ways this could be wrong:
1) The head looks at the new statement because the patch copied the alt prompt's whole last-token state, including its attention query, so 'follows' only says the query moved with the patch. Checked: that is the question here (does the query carry the pointer); the same-entity patch copies a state too and must leave the head on the asked statement (96% [92, 100] (Wilson [80, 99]; n=24 / k=6 / t=6)).
2) Statement spans or the role map are off. Checked: the answer roles agree with d3v4_swap_main on the same items and edits in 100.0% of 72 (item, tokens, layer); every statement has tokens (asserted); a self-patch changes the logits by at most 0.500.
3) Few entities carry the result. Checked: every interval is the entity-cluster bootstrap (k entities next to every number); per topic in the tables.

For the human to verify: rows.jsonl, family=RL, source=dissoc, outcome in ['slot', 'word', 'other statement']: count heads['51:22']['top'] == new_statement (expect 7/11).

Status: UNVERIFIED

## Pre-registered rule

> (fixed before the run; job spec jobs/d5/d5a_head_pointer_27b.yaml). Primary cut: memory → prompt, source dissoc, the four patch settings pooled; unit a row; intervals by entity cluster (queried entity resampled within topic, 4000 draws, seed 0; stats.cluster_bootstrap), item-level Wilson second; n rows / k entities / t wordings per cell; a cut is judged only with >= 35 rows.   H-head-follows (layer 51 head 22): on moved rows the head's top statement is the new statement with lower bound     >= 60%, AND on unmoved rows (kept) it is the org statement with lower bound >= 80%.   H-head-static: on moved rows the head's top statement is the org statement with lower bound >= 60%.   Otherwise neither (reported with the shares). The J-lens comparison: on the same moved rows, the share where the   lens's top entity's statement is the new statement; paired difference head - lens (entity cluster); the head reads   the pointer better than the lens iff its lower bound > 0.   Controls: the same-entity patch and the random push should move <= 10% of answers and leave the head on the org   statement (>= 80%); memory → memory: reported (does the head move to the bridge's new statement without a lookup?).   The other heads get the same numbers, not a verdict.

## Every reader and family (dissoc, settings pooled)

| family | reader | moved: new statement | moved: asked statement | kept: asked statement |
|---|---|---|---|---|
| memory → prompt | layer 51, head 22 | 64% [50, 88] (Wilson [35, 85]; n=11 / k=6 / t=6) | 36% [12, 50] (Wilson [15, 65]; n=11 / k=6 / t=6) | 69% [50, 85] (Wilson [42, 87]; n=13 / k=6 / t=6) |
| memory → prompt | layer 59, head 3 | 64% [50, 88] (Wilson [35, 85]; n=11 / k=6 / t=6) | 36% [12, 50] (Wilson [15, 65]; n=11 / k=6 / t=6) | 69% [58, 80] (Wilson [42, 87]; n=13 / k=6 / t=6) |
| memory → prompt | layer 59, head 1 | 64% [50, 88] (Wilson [35, 85]; n=11 / k=6 / t=6) | 36% [12, 50] (Wilson [15, 65]; n=11 / k=6 / t=6) | 69% [58, 80] (Wilson [42, 87]; n=13 / k=6 / t=6) |
| memory → prompt | layer 55, head 23 | 64% [36, 91] (Wilson [35, 85]; n=11 / k=6 / t=6) | 27% [0, 45] (Wilson [10, 57]; n=11 / k=6 / t=6) | 69% [56, 76] (Wilson [42, 87]; n=13 / k=6 / t=6) |
| memory → prompt | layer 59, head 21 | 64% [50, 88] (Wilson [35, 85]; n=11 / k=6 / t=6) | 36% [12, 50] (Wilson [15, 65]; n=11 / k=6 / t=6) | 69% [50, 85] (Wilson [42, 87]; n=13 / k=6 / t=6) |
| memory → prompt | the J-lens | 18% [0, 43] (Wilson [5, 48]; n=11 / k=6 / t=6) | 18% [0, 36] (Wilson [5, 48]; n=11 / k=6 / t=6) | 8% [0, 15] (Wilson [1, 33]; n=13 / k=6 / t=6) |
| named → prompt | layer 51, head 22 | 30% [25, 33] (Wilson [11, 60]; n=10 / k=6 / t=6) | 70% [67, 75] (Wilson [40, 89]; n=10 / k=6 / t=6) | 64% [50, 79] (Wilson [39, 84]; n=14 / k=6 / t=6) |
| named → prompt | layer 59, head 3 | 30% [25, 33] (Wilson [11, 60]; n=10 / k=6 / t=6) | 70% [67, 75] (Wilson [40, 89]; n=10 / k=6 / t=6) | 64% [62, 67] (Wilson [39, 84]; n=14 / k=6 / t=6) |
| named → prompt | layer 59, head 1 | 30% [25, 33] (Wilson [11, 60]; n=10 / k=6 / t=6) | 70% [67, 75] (Wilson [40, 89]; n=10 / k=6 / t=6) | 57% [50, 67] (Wilson [33, 79]; n=14 / k=6 / t=6) |
| named → prompt | layer 55, head 23 | 30% [25, 33] (Wilson [11, 60]; n=10 / k=6 / t=6) | 70% [67, 75] (Wilson [40, 89]; n=10 / k=6 / t=6) | 64% [50, 79] (Wilson [39, 84]; n=14 / k=6 / t=6) |
| named → prompt | layer 59, head 21 | 30% [25, 33] (Wilson [11, 60]; n=10 / k=6 / t=6) | 70% [67, 75] (Wilson [40, 89]; n=10 / k=6 / t=6) | 57% [50, 67] (Wilson [33, 79]; n=14 / k=6 / t=6) |
| named → prompt | the J-lens | 10% [0, 25] (Wilson [2, 40]; n=10 / k=6 / t=6) | 20% [17, 25] (Wilson [6, 51]; n=10 / k=6 / t=6) | 14% [12, 17] (Wilson [4, 40]; n=14 / k=6 / t=6) |
| memory → memory | layer 51, head 22 | 20% [0, 67] (Wilson [6, 51]; n=10 / k=4 / t=4) | 20% [0, 40] (Wilson [6, 51]; n=10 / k=4 / t=4) | 50% [17, 75] (Wilson [27, 73]; n=14 / k=5 / t=5) |
| memory → memory | layer 59, head 3 | 40% [33, 43] (Wilson [17, 69]; n=10 / k=4 / t=4) | 30% [0, 67] (Wilson [11, 60]; n=10 / k=4 / t=4) | 79% [67, 88] (Wilson [52, 92]; n=14 / k=5 / t=5) |
| memory → memory | layer 59, head 1 | 50% [33, 60] (Wilson [24, 76]; n=10 / k=4 / t=4) | 20% [0, 67] (Wilson [6, 51]; n=10 / k=4 / t=4) | 71% [50, 88] (Wilson [45, 88]; n=14 / k=5 / t=5) |
| memory → memory | layer 55, head 23 | 20% [14, 33] (Wilson [6, 51]; n=10 / k=4 / t=4) | 20% [0, 67] (Wilson [6, 51]; n=10 / k=4 / t=4) | 64% [50, 75] (Wilson [39, 84]; n=14 / k=5 / t=5) |
| memory → memory | layer 59, head 21 | 20% [0, 40] (Wilson [6, 51]; n=10 / k=4 / t=4) | 30% [0, 67] (Wilson [11, 60]; n=10 / k=4 / t=4) | 50% [17, 75] (Wilson [27, 73]; n=14 / k=5 / t=5) |
| memory → memory | the J-lens | 60% [43, 100] (Wilson [31, 83]; n=10 / k=4 / t=4) | 40% [0, 57] (Wilson [17, 69]; n=10 / k=4 / t=4) | 57% [50, 62] (Wilson [33, 79]; n=14 / k=5 / t=5) |

## By patch setting (layer 51 head 22)

| family | patched tokens | layer | answer moved | moved: new statement | kept: asked statement |
|---|---|---|---|---|---|
| memory → prompt | the last two tokens | 48 | 17% [0, 33] (Wilson [3, 56]; n=6 / k=6 / t=6) | 100% [100, 100] (Wilson [21, 100]; n=1 / k=1 / t=1) | 20% [0, 40] (Wilson [4, 62]; n=5 / k=5 / t=5) |
| memory → prompt | the last two tokens | 50 | 100% [100, 100] (Wilson [61, 100]; n=6 / k=6 / t=6) | 100% [100, 100] (Wilson [61, 100]; n=6 / k=6 / t=6) | - |
| memory → prompt | every token after the question | 48 | 33% [0, 67] (Wilson [10, 70]; n=6 / k=6 / t=6) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 100% [100, 100] (Wilson [51, 100]; n=4 / k=4 / t=4) |
| memory → prompt | every token after the question | 50 | 33% [0, 67] (Wilson [10, 70]; n=6 / k=6 / t=6) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 100% [100, 100] (Wilson [51, 100]; n=4 / k=4 / t=4) |
| named → prompt | the last two tokens | 48 | 0% [0, 0] (Wilson [0, 39]; n=6 / k=6 / t=6) | - | 67% [33, 100] (Wilson [30, 90]; n=6 / k=6 / t=6) |
| named → prompt | the last two tokens | 50 | 50% [33, 67] (Wilson [19, 81]; n=6 / k=6 / t=6) | 100% [100, 100] (Wilson [44, 100]; n=3 / k=3 / t=3) | 0% [0, 0] (Wilson [0, 56]; n=3 / k=3 / t=3) |
| named → prompt | every token after the question | 48 | 17% [0, 33] (Wilson [3, 56]; n=6 / k=6 / t=6) | 0% [0, 0] (Wilson [0, 79]; n=1 / k=1 / t=1) | 100% [100, 100] (Wilson [57, 100]; n=5 / k=5 / t=5) |
| named → prompt | every token after the question | 50 | 100% [100, 100] (Wilson [61, 100]; n=6 / k=6 / t=6) | 0% [0, 0] (Wilson [0, 39]; n=6 / k=6 / t=6) | - |
| memory → memory | the last two tokens | 48 | 33% [33, 33] (Wilson [10, 70]; n=6 / k=6 / t=6) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 25% [0, 50] (Wilson [5, 70]; n=4 / k=4 / t=4) |
| memory → memory | the last two tokens | 50 | 67% [67, 67] (Wilson [30, 90]; n=6 / k=6 / t=6) | 50% [0, 100] (Wilson [15, 85]; n=4 / k=4 / t=4) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) |
| memory → memory | every token after the question | 48 | 33% [0, 67] (Wilson [10, 70]; n=6 / k=6 / t=6) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 75% [50, 100] (Wilson [30, 95]; n=4 / k=4 / t=4) |
| memory → memory | every token after the question | 50 | 33% [0, 67] (Wilson [10, 70]; n=6 / k=6 / t=6) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 75% [50, 100] (Wilson [30, 95]; n=4 / k=4 / t=4) |

## By outcome (dissoc): share naming the new answer's statement

| family | outcome | layer 51, head 22 | layer 59, head 3 | layer 59, head 1 | layer 55, head 23 | layer 59, head 21 | the J-lens |
|---|---|---|---|---|---|---|---|
| memory → prompt | slot | 75% [75, 75] (Wilson [30, 95]; n=4 / k=2 / t=2) | 75% [75, 75] (Wilson [30, 95]; n=4 / k=2 / t=2) | 75% [75, 75] (Wilson [30, 95]; n=4 / k=2 / t=2) | 100% [100, 100] (Wilson [51, 100]; n=4 / k=2 / t=2) | 75% [75, 75] (Wilson [30, 95]; n=4 / k=2 / t=2) | 0% [0, 0] (Wilson [0, 49]; n=4 / k=2 / t=2) |
| memory → prompt | word | 50% [38, 75] (Wilson [19, 81]; n=6 / k=3 / t=3) | 50% [38, 75] (Wilson [19, 81]; n=6 / k=3 / t=3) | 50% [38, 75] (Wilson [19, 81]; n=6 / k=3 / t=3) | 50% [38, 75] (Wilson [19, 81]; n=6 / k=3 / t=3) | 50% [38, 75] (Wilson [19, 81]; n=6 / k=3 / t=3) | 33% [12, 75] (Wilson [10, 70]; n=6 / k=3 / t=3) |
| memory → prompt | other statement | 100% [100, 100] (Wilson [21, 100]; n=1 / k=1 / t=1) | 100% [100, 100] (Wilson [21, 100]; n=1 / k=1 / t=1) | 100% [100, 100] (Wilson [21, 100]; n=1 / k=1 / t=1) | 0% [0, 0] (Wilson [0, 79]; n=1 / k=1 / t=1) | 100% [100, 100] (Wilson [21, 100]; n=1 / k=1 / t=1) | 0% [0, 0] (Wilson [0, 79]; n=1 / k=1 / t=1) |
| named → prompt | slot | 40% [40, 40] (Wilson [12, 77]; n=5 / k=2 / t=2) | 40% [40, 40] (Wilson [12, 77]; n=5 / k=2 / t=2) | 40% [40, 40] (Wilson [12, 77]; n=5 / k=2 / t=2) | 40% [40, 40] (Wilson [12, 77]; n=5 / k=2 / t=2) | 40% [40, 40] (Wilson [12, 77]; n=5 / k=2 / t=2) | 0% [0, 0] (Wilson [-0, 43]; n=5 / k=2 / t=2) |
| named → prompt | word | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 0% [0, 0] (Wilson [0, 66]; n=2 / k=2 / t=2) | 50% [50, 50] (Wilson [9, 91]; n=2 / k=2 / t=2) |
| named → prompt | other statement | 33% [33, 33] (Wilson [6, 79]; n=3 / k=2 / t=2) | 33% [33, 33] (Wilson [6, 79]; n=3 / k=2 / t=2) | 33% [33, 33] (Wilson [6, 79]; n=3 / k=2 / t=2) | 33% [33, 33] (Wilson [6, 79]; n=3 / k=2 / t=2) | 33% [33, 33] (Wilson [6, 79]; n=3 / k=2 / t=2) | 0% [0, 0] (Wilson [0, 56]; n=3 / k=2 / t=2) |
| memory → memory | slot | - | - | - | - | - | - |
| memory → memory | word | 20% [0, 67] (Wilson [6, 51]; n=10 / k=4 / t=4) | 40% [33, 43] (Wilson [17, 69]; n=10 / k=4 / t=4) | 50% [33, 60] (Wilson [24, 76]; n=10 / k=4 / t=4) | 20% [14, 33] (Wilson [6, 51]; n=10 / k=4 / t=4) | 20% [0, 40] (Wilson [6, 51]; n=10 / k=4 / t=4) | 60% [43, 100] (Wilson [31, 83]; n=10 / k=4 / t=4) |
| memory → memory | other statement | - | - | - | - | - | - |

## Per topic (layer 51 head 22, memory → prompt, moved rows: new statement)

- animals: 75% (n=4)
- body: 50% (n=4)
- countries: 67% (n=3)

## The agent's priors (job spec hypotheses), checked

| hypothesis | prediction | result | verdict |
|---|---|---|---|
| H_smoke | every stage writes its files; check.json self_patch_noop true (max |dlogit| < 0.5 in bf16); no item without single-token entities. Prior 0.85 | see summary.json | - |
