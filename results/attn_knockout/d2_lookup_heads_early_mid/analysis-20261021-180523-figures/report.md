# attn_knockout / d2_lookup_heads_early_mid: analysis

EXP d2_lookup_heads_early_mid @ 3da911d | model Qwen3.6-27B | n={'memory → prompt': 200, 'named → prompt': 200, 'memory → memory': 200} org prompts per family, k={'memory → prompt': 22, 'named → prompt': 22, 'memory → memory': 22} queried entities, domains ['animals', 'elements'] | seeds=[0]

Claim tested: The early and middle halves of d2_lookup_heads (its spec has the full question). Batch 2 (UNVERIFIED): in named → prompt the question words read the answer's statement early (hiding it from the question words + last tokens in layers 0-31 leaves 1/175 right, attention layers only 6/175); in memory → prompt the question words and the last tokens together read it in layers 32-47 (78/175 left, each alone 87-88%). Which heads do these two reads?

Terms: org prompt = the unedited prompt; answer org = its answer; 'hidden from' = those positions cannot read it directly (the attention scores of the named query heads masked; attention layers only, DeltaNet layers untouched); accuracy = % of org prompts still giving answer org (100% unedited, by selection). Headline and rule intervals: entity-cluster bootstrap (the queried entities resampled with replacement within each domain, all their items kept; 4000 draws, seed 0); reported second: the item-level Wilson interval (accuracy) and the paired item bootstrap (2000 draws). Every number also per domain, with n items / k entities.

Headline: named → prompt, the statement giving the answer hidden from the question words in every attention layer of layers 3-31 (3, 7, 11, 15, 19, 23, 27, 31; all heads): answer org kept 3% [0, 8] (entity cluster; Wilson [1, 6]); n=200 items / k=22 entities; per domain animals 0% (100/16), elements 6% (100/6)   Baseline: unedited 100% (200/200)   Control: an off-path statement, the same blocking 100% [98, 100] (Wilson)
Headline: named → prompt, the statement giving the answer hidden from the name tokens in the question in every attention layer of layers 3-31 (3, 7, 11, 15, 19, 23, 27, 31; all heads): answer org kept 3% [0, 8] (entity cluster; Wilson [1, 6]); n=200 items / k=22 entities; per domain animals 0% (100/16), elements 6% (100/6)   Baseline: unedited 100% (200/200)   Control: an off-path statement, the same blocking 100% [98, 100] (Wilson)
Single heads, named → prompt, the question words, early attention layers: 0 of 192 are readers; the largest drop: layer 3, query head 0, +0 [+0, +0] points (entity cluster), per domain animals +0 pts (100/16), elements +0 pts (100/6)
Headline: memory → prompt, the statement giving the answer hidden from the question words and the last tokens in every attention layer of layers 35-47 (35, 39, 43, 47; all heads): answer org kept 43% [35, 52] (entity cluster; Wilson [36, 50]); n=200 items / k=22 entities; per domain animals 47% (100/16), elements 39% (100/6)   Baseline: unedited 100% (200/200)   Control: an off-path statement, the same blocking 100% [98, 100] (Wilson)
Single heads, memory → prompt, the question words and the last tokens together, middle attention layers: 0 of 96 are readers; the largest drop: layer 43, query head 22, +3 [+0, +8] points (entity cluster), per domain animals +1 pts (100/16), elements +5 pts (100/6)
Null: memory → memory, the lowest cell over every unit: the statement hidden from the question words in every attention layer of layers 3-31 (3, 7, 11, 15, 19, 23, 27, 31; all heads) 100% [98, 100] (n=200 / k=22)
Pointer readout (the name tokens): layer 3, head 19 (chosen on even-numbered scenes) looks most at the asked statement on the odd-numbered ones in 100% [100, 100] (entity cluster; Wilson [96, 100]); n=98 / k=20; per domain animals 100% (50/14), elements 100% (48/6); chance 20%, the slot probe 39%

Figures: heads.png, heads.svg, head_units.png, head_units.svg, readout.png, readout.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.55, median 0.996; an unedited row moves by up to 0.25 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any statement there breaks the model. Checked: the off-path statement, blocked the same way, loses answer org in 5 of 74600 rows; the worst control cell: memory → prompt, hidden from the question words and the last tokens in layer 39, query head 22 keeps 100%.
3) With 288 single heads tested, some readers are noise. Checked: the mirror image of the rule (the off-path block costing >= 10 points more than the statement) fires for 0 of 288 single heads; single heads are read with their group and layer. Items of one entity are correlated (few entities per domain): the entity-cluster intervals are 1.5x the item-level ones (median over the 8 cells between 2% and 98%).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=DL, source=lookup, dest=question, layers=early, mode=value (expect 6/200; the cluster interval: entity = cases.jsonl 'bridge', resampled within 'domain').

Status: UNVERIFIED

## Pre-registered rules (manifest.json 'batch3_rules', 'intervals'; job spec decision_rule)

- reader: a unit (query head, key/value group, layer, whole range; a code line or union of lines) is a reader if acc(control) - acc(unit) >= 10 points and its entity-cluster bootstrap 95% lower bound >= 5 points (control: the same unit blocked from a statement of the same kind off the answer's path, the same items)
- relay: code: a line relays if blocking it together with the last tokens costs >= 10 points more than the last tokens alone (entity-cluster lower bound >= 5 points)
- explained: code: the lines explain the survivors if the union (last tokens + print + list/chain lines + the rest of the question) keeps answer org within 10 points of 'every line after the dict' (point estimate)
- readout: the best head is chosen on even-numbered scenes (pooled over the families that look the answer up) and scored on odd-numbered ones; it reads the pointer better than the slot probe if its entity-cluster lower bound > 39%
- reproduction: heads grid: memory → prompt with all late attention heads blocked at the last tokens reproduces batch 2 if its cluster interval overlaps 11%-20%
- multiplicity: single heads are many tests (24 heads x 4-8 layers per range): a single-head reader is read together with its key/value group and layer cells, never alone

## named → prompt: blocked at the question words, early attention layers (layers 3-31: layers 3, 7, 11, 15, 19, 23, 27, 31)

| family | unit | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |
|---|---|---|---|---|---|---|---|---|
| named → prompt | the question words in layer 3, query head 0 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, query head 1 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, query head 2 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, query head 3 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, query head 4 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, query head 5 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, query head 6 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, query head 7 | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 3, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the name tokens in the question in layer 3 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 7 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 7, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 7, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 7, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 7, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the name tokens in the question in layer 7 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 11 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 11, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 11, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 11, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 11, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the name tokens in the question in layer 11 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 15 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 15, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 15, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 15, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 15, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the name tokens in the question in layer 15 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 19 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 19, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 19, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 19, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 19, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the name tokens in the question in layer 19 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 23 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 23, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 23, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 23, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 23, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the name tokens in the question in layer 23 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 27 (all heads) | 200 / 22 | 95% [90, 99] | animals 90% (100/16), elements 100% (100/6) | 100% | +5 [+1, +10] | +5 [+2, +8] | no |
| named → prompt | the question words in layer 27, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 27, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 27, key/value group 2 (its query heads) | 200 / 22 | 100% [98, 100] | animals 99% (100/16), elements 100% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| named → prompt | the question words in layer 27, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the name tokens in the question in layer 27 (all heads) | 200 / 22 | 95% [90, 99] | animals 90% (100/16), elements 100% (100/6) | 100% | +5 [+1, +10] | +5 [+2, +8] | no |
| named → prompt | the question words in layer 31 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 31, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 31, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 31, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in layer 31, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the name tokens in the question in layer 31 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| named → prompt | the question words in every attention layer of layers 3-31 (3, 7, 11, 15, 19, 23, 27, 31; all heads) | 200 / 22 | 3% [0, 8] | animals 0% (100/16), elements 6% (100/6) | 100% | +97 [+92, +100] | +97 [+94, +99] | yes |
| named → prompt | the name tokens in the question in every attention layer of layers 3-31 (3, 7, 11, 15, 19, 23, 27, 31; all heads) | 200 / 22 | 3% [0, 8] | animals 0% (100/16), elements 6% (100/6) | 100% | +97 [+92, +100] | +97 [+94, +99] | yes |

Single heads that are readers: 0 of 192 (the 8 largest drops are listed); mirror image (the off-path block costs >= 10 points more, the noise floor): 0 of 192.

## memory → memory: blocked at the question words, early attention layers (layers 3-31: layers 3, 7, 11, 15, 19, 23, 27, 31)

| family | unit | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |
|---|---|---|---|---|---|---|---|---|
| memory → memory | the question words in layer 3 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words in layer 7 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words in layer 11 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words in layer 15 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words in layer 19 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words in layer 23 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words in layer 27 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words in layer 31 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words in every attention layer of layers 3-31 (3, 7, 11, 15, 19, 23, 27, 31; all heads) | 200 / 22 | 100% [98, 100] | animals 99% (100/16), elements 100% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |

## memory → prompt: blocked at the question words and the last tokens together, middle attention layers (layers 35-47: layers 35, 39, 43, 47)

| family | unit | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the question words and the last tokens in layer 43, query head 22 | 200 / 22 | 97% [92, 100] | animals 99% (100/16), elements 95% (100/6) | 100% | +3 [+0, +8] | +3 [+1, +6] | no |
| memory → prompt | the question words and the last tokens in layer 47, query head 3 | 200 / 22 | 98% [96, 100] | animals 100% (100/16), elements 97% (100/6) | 100% | +2 [+0, +4] | +2 [+0, +4] | no |
| memory → prompt | the question words and the last tokens in layer 47, query head 1 | 200 / 22 | 99% [98, 100] | animals 100% (100/16), elements 98% (100/6) | 100% | +1 [+0, +2] | +1 [+0, +3] | no |
| memory → prompt | the question words and the last tokens in layer 35, query head 17 | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the question words and the last tokens in layer 35, query head 18 | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the question words and the last tokens in layer 39, query head 15 | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the question words and the last tokens in layer 39, query head 23 | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the question words and the last tokens in layer 43, query head 7 | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the question words and the last tokens in layer 35 (all heads) | 200 / 22 | 99% [98, 100] | animals 99% (100/16), elements 99% (100/6) | 100% | +1 [+0, +2] | +1 [+0, +3] | no |
| memory → prompt | the question words and the last tokens in layer 35, key/value group 0 (its query heads) | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the question words and the last tokens in layer 35, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 35, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 35, key/value group 3 (its query heads) | 200 / 22 | 99% [98, 100] | animals 99% (100/16), elements 99% (100/6) | 100% | +1 [+0, +2] | +1 [+0, +3] | no |
| memory → prompt | the question words and the last tokens in layer 39 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 39, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 39, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 39, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 39, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 43 (all heads) | 200 / 22 | 96% [91, 99] | animals 97% (100/16), elements 94% (100/6) | 100% | +4 [+1, +9] | +5 [+2, +7] | no |
| memory → prompt | the question words and the last tokens in layer 43, key/value group 0 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 43, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 43, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 43, key/value group 3 (its query heads) | 200 / 22 | 98% [93, 100] | animals 100% (100/16), elements 95% (100/6) | 100% | +2 [+0, +7] | +3 [+1, +5] | no |
| memory → prompt | the question words and the last tokens in layer 47 (all heads) | 200 / 22 | 100% [98, 100] | animals 100% (100/16), elements 99% (100/6) | 100% | +0 [+0, +2] | +1 [+0, +2] | no |
| memory → prompt | the question words and the last tokens in layer 47, key/value group 0 (its query heads) | 200 / 22 | 99% [98, 100] | animals 100% (100/16), elements 98% (100/6) | 100% | +1 [+0, +2] | +1 [+0, +3] | no |
| memory → prompt | the question words and the last tokens in layer 47, key/value group 1 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 47, key/value group 2 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in layer 47, key/value group 3 (its query heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → prompt | the question words and the last tokens in every attention layer of layers 35-47 (35, 39, 43, 47; all heads) | 200 / 22 | 43% [35, 52] | animals 47% (100/16), elements 39% (100/6) | 100% | +57 [+48, +65] | +57 [+50, +64] | yes |

Single heads that are readers: 0 of 96 (the 8 largest drops are listed); mirror image (the off-path block costs >= 10 points more, the noise floor): 0 of 96.

## memory → memory: blocked at the question words and the last tokens together, middle attention layers (layers 35-47: layers 35, 39, 43, 47)

| family | unit | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |
|---|---|---|---|---|---|---|---|---|
| memory → memory | the question words and the last tokens in layer 35 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words and the last tokens in layer 39 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words and the last tokens in layer 43 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words and the last tokens in layer 47 (all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| memory → memory | the question words and the last tokens in every attention layer of layers 35-47 (35, 39, 43, 47; all heads) | 200 / 22 | 100% [100, 100] | animals 100% (100/16), elements 100% (100/6) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |

## Pointer readout: attention from the name tokens

Best head chosen on even-numbered scenes (pooled over the families that look the answer up): layer 3, query head 19 (even half 100%). On the odd-numbered scenes it puts the most attention on the asked statement in 100% [100, 100] (entity cluster; Wilson [96, 100]), n=98 / k=20; per domain animals 100% (50/14), elements 100% (48/6); chance 20%, the slot probe 39%. Above the probe (entity-cluster lower bound > 39%): yes.

## The agent's priors (job spec hypotheses), checked

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_named_early | named → prompt, every head of the 8 early attention layers (3, 7, ..., 31) blocked at the question words: <= 10% kept; and at least one single early head is a reader (a name-matching head). Prior 0.5 (<= 10% alone: 0.7) | named → prompt, question words, whole early range: 3% [0, 8]; 0 single early heads are readers | partly |
| H_name_tokens | named → prompt, early layers: blocking the read from the name tokens only (" pig") keeps answer org within 10 points of blocking it from all the question words, so the per-head results at the question words are about ... | whole early range, question words 3% [0, 8], name tokens only 3% [0, 8] | holds |
| H_mid_joint | memory → prompt, every head of the 4 middle attention layers (35, 39, 43, 47) blocked at the question words and the last tokens together: 30-60% kept (batch 2: 45% with the DeltaNet layers blocked too, which alone cos... | memory → prompt, both destinations, whole middle range: 43% [35, 52]; 0 single middle heads are readers | holds |
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

memory → prompt, org prompt elements-RL-e5f0-0024. What was done: the question and final positions cannot read the lookup span ('The hydrogen card is in locker 9.') directly at layer 47, query head 1. Unedited the model answers '9' (answer org '9'); blocked it answers '6' (the prompt's other answers: ['3', '4', '6', '8']). log p(answer org): -0.425 -> -0.949.

