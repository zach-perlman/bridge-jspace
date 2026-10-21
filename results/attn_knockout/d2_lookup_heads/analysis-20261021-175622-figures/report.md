# attn_knockout / d2_lookup_heads: analysis

EXP d2_lookup_heads @ 3da911d | model Qwen3.6-27B | n={'memory → prompt': 200, 'named → prompt': 200, 'memory → memory': 200} org prompts per family, k={'memory → prompt': 22, 'named → prompt': 22, 'memory → memory': 22} queried entities, domains ['animals', 'elements'] | seeds=[0]

Claim tested: Batch 2 found three reads of the answer's statement in pointer_v1's locker scenes, all through attention (UNVERIFIED): (1) the last tokens read it late (layers 48-63) in memory → prompt; (2) in named → prompt the question words read it early (hiding it from the question words + last tokens in layers 0-31 leaves 1/175 right, attention layers only 6/175, DeltaNet layers only 175/175; the last tokens alone at 0-31 keep 175/175); (3) in memory → prompt the question words and the last tokens together in layers 32-47 (78/175 left, each alone 87-88%). Which attention heads do each read: one or a few query heads, one key/value group, one layer, or only all of them together? And does any single head's attention pattern point at the asked statement (a pointer readout better than D3b's slot probe, 39%)?

Terms: org prompt = the unedited prompt; answer org = its answer; 'hidden from' = those positions cannot read it directly (the attention scores of the named query heads masked; attention layers only, DeltaNet layers untouched); accuracy = % of org prompts still giving answer org (100% unedited, by selection). Headline and rule intervals: entity-cluster bootstrap (the queried entities resampled with replacement within each domain, all their items kept; 4000 draws, seed 0); reported second: the item-level Wilson interval (accuracy) and the paired item bootstrap (2000 draws). Every number also per domain, with n items / k entities.

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every attention layer of layers 51-63 (51, 55, 59, 63; all heads): answer org kept 18% [12, 24] (entity cluster; Wilson [13, 23]); n=200 items / k=22 entities; per domain animals 30% (100/16), elements 5% (100/6)   Baseline: unedited 100% (200/200)   Control: an off-path statement, the same blocking 100% [98, 100] (Wilson)
Single heads, memory → prompt, the last tokens before the answer, late attention layers: 0 of 96 are readers; the largest drop: layer 51, query head 20, +0 [+0, +2] points (entity cluster), per domain animals +0 pts (100/16), elements +1 pts (100/6)
Headline: named → prompt, the statement giving the answer hidden from the last tokens before the answer in every attention layer of layers 51-63 (51, 55, 59, 63; all heads): answer org kept 10% [7, 13] (entity cluster; Wilson [7, 15]); n=200 items / k=22 entities; per domain animals 20% (100/16), elements 0% (100/6)   Baseline: unedited 100% (200/200)   Control: an off-path statement, the same blocking 100% [98, 100] (Wilson)
Single heads, named → prompt, the last tokens before the answer, late attention layers: 0 of 96 are readers; the largest drop: layer 51, query head 0, +0 [+0, +0] points (entity cluster), per domain animals +0 pts (100/16), elements +0 pts (100/6)
Null: memory → memory, the lowest cell over every unit: the statement hidden from the last tokens before the answer in every attention layer of layers 51-63 (51, 55, 59, 63; all heads) 100% [100, 100] (n=200 / k=22)
Pointer readout (the last token): layer 51, head 22 (chosen on even-numbered scenes) looks most at the asked statement on the odd-numbered ones in 100% [100, 100] (entity cluster; Wilson [98, 100]); n=196 / k=20; per domain animals 100% (100/14), elements 100% (96/6); chance 20%, the slot probe 39%

Figures: heads.png, heads.svg, head_units.png, head_units.svg, readout.png, readout.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.55, median 0.996; an unedited row moves by up to 0.25 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any statement there breaks the model. Checked: the off-path statement, blocked the same way, loses answer org in 0 of 47800 rows; the worst control cell: memory → prompt, hidden from the last tokens before the answer in every attention layer of layers 51-63 (51, 55, 59, 63; all heads) keeps 100%.
3) With 192 single heads tested, some readers are noise. Checked: the mirror image of the rule (the off-path block costing >= 10 points more than the statement) fires for 0 of 192 single heads; single heads are read with their group and layer. Items of one entity are correlated (few entities per domain): the entity-cluster intervals are 1.2x the item-level ones (median over the 4 cells between 2% and 98%).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=late, mode=value (expect 35/200; the cluster interval: entity = cases.jsonl 'bridge', resampled within 'domain').

Status: UNVERIFIED

## Pre-registered rules (manifest.json 'batch3_rules', 'intervals'; job spec decision_rule)

- reader: a unit (query head, key/value group, layer, whole range; a code line or union of lines) is a reader if acc(control) - acc(unit) >= 10 points and its entity-cluster bootstrap 95% lower bound >= 5 points (control: the same unit blocked from a statement of the same kind off the answer's path, the same items)
- relay: code: a line relays if blocking it together with the last tokens costs >= 10 points more than the last tokens alone (entity-cluster lower bound >= 5 points)
- explained: code: the lines explain the survivors if the union (last tokens + print + list/chain lines + the rest of the question) keeps answer org within 10 points of 'every line after the dict' (point estimate)
- readout: the best head is chosen on even-numbered scenes (pooled over the families that look the answer up) and scored on odd-numbered ones; it reads the pointer better than the slot probe if its entity-cluster lower bound > 39%
- reproduction: heads grid: memory → prompt with all late attention heads blocked at the last tokens reproduces batch 2 if its cluster interval overlaps 11%-20%
- multiplicity: single heads are many tests (24 heads x 4-8 layers per range): a single-head reader is read together with its key/value group and layer cells, never alone

## memory → prompt: blocked at the last tokens before the answer, late attention layers (layers 51-63: layers 51, 55, 59, 63)

| family | unit | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the last tokens before the answer in layer 51, query head 20 | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the last tokens before the answer in layer 51, query head 23 | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the last tokens before the answer in layer 59, query head 3 | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the last tokens before the answer in layer 51, query head 0 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 51, query head 1 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 51, query head 2 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 51, query head 3 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 51, query head 4 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 51 (all heads) | 200 / 22 | 96% [91, 99] | animals 99% (100/16), elements 93% (100/6) | 100% | +4 [+1, +9] | +4 [+2, +7] | no |
| memory → prompt | the last tokens before the answer in layer 51, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 51, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 51, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 51, key/value group 3 (its query heads) | 200 / 22 | 96% [91, 99] | animals 99% (100/16), elements 93% (100/6) | 100% | +4 [+1, +9] | +4 [+2, +7] | no |
| memory → prompt | the last tokens before the answer in layer 55 (all heads) | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the last tokens before the answer in layer 55, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 55, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 55, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 55, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 59 (all heads) | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the last tokens before the answer in layer 59, key/value group 0 (its query heads) | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the last tokens before the answer in layer 59, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 59, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 59, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 63 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 63, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 63, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 63, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in layer 63, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the last tokens before the answer in every attention layer of layers 51-63 (51, 55, 59, 63; all heads) | 200 / 22 | 18% [12, 24] | animals 30% (100/16), elements 5% (100/6) | 100% | +82 [+76, +88] | +82 [+77, +88] | yes |

Single heads that are readers: 0 of 96 (the 8 largest drops are listed); mirror image (the off-path block costs >= 10 points more, the noise floor): 0 of 96.

## named → prompt: blocked at the last tokens before the answer, late attention layers (layers 51-63: layers 51, 55, 59, 63)

| family | unit | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |
|---|---|---|---|---|---|---|---|---|
| named → prompt | the last tokens before the answer in layer 51, query head 0 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, query head 1 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, query head 2 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, query head 3 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, query head 4 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, query head 5 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, query head 6 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, query head 7 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 51, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 55 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 55, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 55, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 55, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 55, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 59 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 59, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 59, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 59, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 59, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 63 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 63, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 63, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 63, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in layer 63, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the last tokens before the answer in every attention layer of layers 51-63 (51, 55, 59, 63; all heads) | 200 / 22 | 10% [7, 13] | animals 20% (100/16), elements 0% (100/6) | 100% | +90 [+87, +93] | +90 [+86, +94] | yes |

Single heads that are readers: 0 of 96 (the 8 largest drops are listed); mirror image (the off-path block costs >= 10 points more, the noise floor): 0 of 96.

## memory → memory: blocked at the last tokens before the answer, late attention layers (layers 51-63: layers 51, 55, 59, 63)

| family | unit | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |
|---|---|---|---|---|---|---|---|---|
| memory → memory | the last tokens before the answer in layer 51 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the last tokens before the answer in layer 55 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the last tokens before the answer in layer 59 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the last tokens before the answer in layer 63 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the last tokens before the answer in every attention layer of layers 51-63 (51, 55, 59, 63; all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |

## Pointer readout: attention from the last token

Best head chosen on even-numbered scenes (pooled over the families that look the answer up): layer 51, query head 22 (even half 100%). On the odd-numbered scenes it puts the most attention on the asked statement in 100% [100, 100] (entity cluster; Wilson [98, 100]), n=196 / k=20; per domain animals 100% (100/14), elements 100% (96/6); chance 20%, the slot probe 39%. Above the probe (entity-cluster lower bound > 39%): yes.

## The agent's priors (job spec hypotheses), checked

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_reproduce | memory → prompt, every head of the 4 late attention layers (51, 55, 59, 63) blocked at the last tokens: answer org kept in 11-20% (the entity-cluster interval overlaps 11-20%), reproducing batch 2. Prior 0.7 | memory → prompt, whole late range: 18% [12, 24] | holds |
| H_late_few_heads | memory → prompt: no single late query head is a reader (24 heads x 4 layers; the read is redundant across heads), but at least one whole late layer is. Prior 0.45 | memory → prompt: 0 of 96 single late heads are readers; late layers that are: none | partly |
| H_named_early | named → prompt, every head of the 8 early attention layers (3, 7, ..., 31) blocked at the question words: <= 10% kept; and at least one single early head is a reader (a name-matching head). Prior 0.5 (<= 10% alone: 0.7) | not measured in this run | - |
| H_name_tokens | named → prompt, early layers: blocking the read from the name tokens only (" pig") keeps answer org within 10 points of blocking it from all the question words, so the per-head results at the question words are about ... | not measured in this run | - |
| H_mid_joint | memory → prompt, every head of the 4 middle attention layers (35, 39, 43, 47) blocked at the question words and the last tokens together: 30-60% kept (batch 2: 45% with the DeltaNet layers blocked too, which alone cos... | not measured in this run | - |
| H_readout | the late head chosen on even-numbered scenes looks most at the asked statement (attention from the last token, argmax over the 5 statements) on > 39% of odd-numbered scenes (entity-cluster lower bound > 39%, the D3b p... | layer 51 head 22: 100% [100, 100] on held-out scenes | holds |
| H_null | memory → memory: every whole-layer and whole-range cell >= 95%. Prior 0.9 | memory → memory, lowest cell 100% | holds |

## Worked example (examples.json, group one_head_breaks)

```
<|im_start|>user
The oxygen card is in locker 4. The nitrogen card is in locker 3. The helium card is in locker 6. The hydrogen card is in locker 9. The carbon card is in locker 8.
Which locker holds the card for the lightest element? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

memory → prompt, org prompt elements-RL-e5f0-0024. What was done: the final template positions cannot read the lookup span ('The hydrogen card is in locker 9.') directly at layer 51, query head 23. Unedited the model answers '9' (answer org '9'); blocked it answers '6' (the prompt's other answers: ['3', '4', '6', '8']). log p(answer org): -0.425 -> -0.744.

