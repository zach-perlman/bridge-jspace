# attn_knockout / d2_code_readers: analysis

EXP d2_code_readers @ 3da911d | model Qwen3.6-27B | n={'code: named → prompt': 200, 'code: list position → prompt': 200, 'code: 2-variable chain → prompt': 200, 'code: 3-variable chain → prompt': 200, 'code: memory → prompt': 100} org prompts per family, k={'code: named → prompt': 19, 'code: list position → prompt': 19, 'code: 2-variable chain → prompt': 19, 'code: 3-variable chain → prompt': 19, 'code: memory → prompt': 12} queried entities, domains ['animals', 'months'] | seeds=[0]

Claim tested: In code_pointer_v1 (lockers = {"bee": 7, ..., "mouse": 5}; names = ["mouse", ...]; print(lockers[names[0]]) -> 5), batch 2 found (UNVERIFIED) that hiding the answer's dict entry from the last tokens in all layers leaves 36% of list-position programs right (43/120), from the question words (print line onward) 100%, from everything after the entry 3%. Which later lines read the entry themselves: the names list line, a chain line (x = "mouse"), the print line, the rest of the question? Does a line pass it on, i.e. does hiding it from that line and the last tokens together cost more than the last tokens alone, and do these lines account for the gap between 36% and 3%?

Terms: org prompt = the unedited prompt; answer org = its answer; 'hidden from' = those positions cannot read it directly (attention scores masked and DeltaNet values removed, every layer); accuracy = % of org prompts still giving answer org (100% unedited, by selection). Headline and rule intervals: entity-cluster bootstrap (the queried entities resampled with replacement within each domain, all their items kept; 4000 draws, seed 0); reported second: the item-level Wilson interval (accuracy) and the paired item bootstrap (2000 draws). Every number also per domain, with n items / k entities.

Headline: code: named → prompt, the dict entry giving the answer hidden from the last tokens in all 64 layers: answer org kept 48% [40, 56] (entity cluster; Wilson [41, 54]); n=200 items / k=19 entities; per domain animals 49% (100/12), months 46% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Headline: code: named → prompt, the dict entry giving the answer hidden from all of the question + list/chain in all 64 layers: answer org kept 0% [0, 0] (entity cluster; Wilson [0, 2]); n=200 items / k=19 entities; per domain animals 0% (100/12), months 0% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Headline: code: named → prompt, the dict entry giving the answer hidden from every line after the dict in all 64 layers: answer org kept 0% [0, 0] (entity cluster; Wilson [0, 2]); n=200 items / k=19 entities; per domain animals 0% (100/12), months 0% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Readers, code: named → prompt: the print line; relays (with the last tokens): last tokens + print line, all of the question + list/chain; the lines explain the survivors: yes (+0 [+0, +0] points)
Headline: code: list position → prompt, the dict entry giving the answer hidden from the last tokens in all 64 layers: answer org kept 35% [28, 43] (entity cluster; Wilson [29, 42]); n=200 items / k=19 entities; per domain animals 30% (100/12), months 40% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Headline: code: list position → prompt, the dict entry giving the answer hidden from all of the question + list/chain in all 64 layers: answer org kept 6% [4, 9] (entity cluster; Wilson [4, 11]); n=200 items / k=19 entities; per domain animals 6% (100/12), months 7% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Headline: code: list position → prompt, the dict entry giving the answer hidden from every line after the dict in all 64 layers: answer org kept 6% [4, 9] (entity cluster; Wilson [4, 11]); n=200 items / k=19 entities; per domain animals 6% (100/12), months 7% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Readers, code: list position → prompt: the names list line; relays (with the last tokens): last tokens + list/chain lines, last tokens + print + list/chain, all of the question + list/chain; the lines explain the survivors: yes (+0 [+0, +0] points)
Headline: code: 2-variable chain → prompt, the dict entry giving the answer hidden from the last tokens in all 64 layers: answer org kept 41% [33, 50] (entity cluster; Wilson [35, 48]); n=199 items / k=19 entities; per domain animals 41% (100/12), months 41% (99/7)   Baseline: unedited 100% (199/199)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Headline: code: 2-variable chain → prompt, the dict entry giving the answer hidden from all of the question + list/chain in all 64 layers: answer org kept 6% [2, 9] (entity cluster; Wilson [3, 10]); n=199 items / k=19 entities; per domain animals 3% (100/12), months 8% (99/7)   Baseline: unedited 100% (199/199)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Headline: code: 2-variable chain → prompt, the dict entry giving the answer hidden from every line after the dict in all 64 layers: answer org kept 6% [2, 9] (entity cluster; Wilson [3, 10]); n=199 items / k=19 entities; per domain animals 3% (100/12), months 8% (99/7)   Baseline: unedited 100% (199/199)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Readers, code: 2-variable chain → prompt: chain line 1 (holds the key); relays (with the last tokens): last tokens + list/chain lines, last tokens + print + list/chain, all of the question + list/chain; the lines explain the survivors: yes (+0 [+0, +0] points)
Headline: code: 3-variable chain → prompt, the dict entry giving the answer hidden from the last tokens in all 64 layers: answer org kept 32% [24, 42] (entity cluster; Wilson [26, 39]); n=200 items / k=19 entities; per domain animals 27% (100/12), months 38% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Headline: code: 3-variable chain → prompt, the dict entry giving the answer hidden from all of the question + list/chain in all 64 layers: answer org kept 6% [3, 8] (entity cluster; Wilson [3, 10]); n=200 items / k=19 entities; per domain animals 6% (100/12), months 5% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Headline: code: 3-variable chain → prompt, the dict entry giving the answer hidden from every line after the dict in all 64 layers: answer org kept 6% [3, 8] (entity cluster; Wilson [3, 10]); n=200 items / k=19 entities; per domain animals 5% (100/12), months 6% (100/7)   Baseline: unedited 100% (200/200)   Control: another dict entry, the same blocking 100% [98, 100] (Wilson)
Readers, code: 3-variable chain → prompt: chain line 1 (holds the key); relays (with the last tokens): last tokens + list/chain lines, last tokens + print + list/chain, all of the question + list/chain; the lines explain the survivors: yes (+0 [-1, +1] points)
Headline: code: memory → prompt, the dict entry giving the answer hidden from the last tokens in all 64 layers: answer org kept 20% [12, 28] (entity cluster; Wilson [13, 29]); n=100 items / k=12 entities; per domain animals 20% (100/12)   Baseline: unedited 100% (100/100)   Control: another dict entry, the same blocking 100% [96, 100] (Wilson)
Headline: code: memory → prompt, the dict entry giving the answer hidden from all of the question + list/chain in all 64 layers: answer org kept 2% [0, 6] (entity cluster; Wilson [1, 7]); n=100 items / k=12 entities; per domain animals 2% (100/12)   Baseline: unedited 100% (100/100)   Control: another dict entry, the same blocking 100% [96, 100] (Wilson)
Headline: code: memory → prompt, the dict entry giving the answer hidden from every line after the dict in all 64 layers: answer org kept 2% [0, 6] (entity cluster; Wilson [1, 7]); n=100 items / k=12 entities; per domain animals 2% (100/12)   Baseline: unedited 100% (100/100)   Control: another dict entry, the same blocking 100% [96, 100] (Wilson)
Readers, code: memory → prompt: no single line; relays (with the last tokens): all of the question + list/chain; the lines explain the survivors: yes (+0 [+0, +0] points)

Figures: code_readers.png, code_readers.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.47, median 0.996; an unedited row moves by up to 0.33 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any statement there breaks the model. Checked: another dict entry, blocked the same way, loses answer org in 6 of 9487 rows; the worst control cell: code: 3-variable chain → prompt, hidden from chain line 1 (holds the key) in all 64 layers keeps 99%.
3) Items of one entity are correlated (few queried keys per domain): every interval is the entity-cluster bootstrap; the item-level intervals are next to them (cluster intervals are 1.0x the item-level ones (median over the 28 cells between 2% and 98%)). The lines are not independent: unions are read against 'every line after the dict', not summed.

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=DK, source=lookup, dest=final, layers=all, mode=value (expect 95/200; the cluster interval: entity = cases.jsonl 'bridge', resampled within 'domain').

Status: UNVERIFIED

## Pre-registered rules (manifest.json 'batch3_rules', 'intervals'; job spec decision_rule)

- reader: a unit (query head, key/value group, layer, whole range; a code line or union of lines) is a reader if acc(control) - acc(unit) >= 10 points and its entity-cluster bootstrap 95% lower bound >= 5 points (control: the same unit blocked from a statement of the same kind off the answer's path, the same items)
- relay: code: a line relays if blocking it together with the last tokens costs >= 10 points more than the last tokens alone (entity-cluster lower bound >= 5 points)
- explained: code: the lines explain the survivors if the union (last tokens + print + list/chain lines + the rest of the question) keeps answer org within 10 points of 'every line after the dict' (point estimate)
- readout: the best head is chosen on even-numbered scenes (pooled over the families that look the answer up) and scored on odd-numbered ones; it reads the pointer better than the slot probe if its entity-cluster lower bound > 39%
- reproduction: heads grid: memory → prompt with all late attention heads blocked at the last tokens reproduces batch 2 if its cluster interval overlaps 11%-20%
- multiplicity: single heads are many tests (24 heads x 4-8 layers per range): a single-head reader is read together with its key/value group and layer cells, never alone

## Code line readers

| family | hidden from | n / k | answer org kept [95%, entity cluster] | per domain (n/k) | control (off-path) | drop, control - cell [95%, entity cluster] | drop [95%, items] | reader |
|---|---|---|---|---|---|---|---|---|
| code: named → prompt | the print line | 200 / 19 | 6% [1, 12] | animals 3% (100/12), months 9% (100/7) | 100% | +94 [+88, +99] | +94 [+90, +97] | yes |
| code: named → prompt | the rest of the question | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: named → prompt | the last tokens | 200 / 19 | 48% [40, 56] | animals 49% (100/12), months 46% (100/7) | 100% | +52 [+44, +60] | +52 [+46, +59] | yes |
| code: named → prompt | last tokens + print line | 200 / 19 | 0% [0, 0] | animals 0% (100/12), months 0% (100/7) | 100% | +100 [+100, +100] | +100 [+100, +100] | yes |
| code: named → prompt | all of the question + list/chain | 200 / 19 | 0% [0, 0] | animals 0% (100/12), months 0% (100/7) | 100% | +100 [+100, +100] | +100 [+100, +100] | yes |
| code: named → prompt | every line after the dict | 200 / 19 | 0% [0, 0] | animals 0% (100/12), months 0% (100/7) | 100% | +100 [+100, +100] | +100 [+100, +100] | yes |
| code: named → prompt | everything after the entry | 200 / 19 | 2% [1, 4] | animals 5% (100/12), months 0% (100/7) | 100% | +98 [+96, +99] | +98 [+95, +100] | yes |
| code: list position → prompt | the names list line | 200 / 19 | 44% [34, 53] | animals 44% (100/12), months 43% (100/7) | 100% | +56 [+47, +65] | +56 [+49, +63] | yes |
| code: list position → prompt | the print line | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: list position → prompt | the rest of the question | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: list position → prompt | the last tokens | 200 / 19 | 35% [28, 43] | animals 30% (100/12), months 40% (100/7) | 100% | +65 [+57, +72] | +65 [+58, +72] | yes |
| code: list position → prompt | last tokens + print line | 200 / 19 | 34% [27, 42] | animals 29% (100/12), months 40% (100/7) | 100% | +66 [+58, +73] | +66 [+59, +72] | yes |
| code: list position → prompt | last tokens + list/chain lines | 200 / 19 | 6% [5, 8] | animals 5% (100/12), months 8% (100/7) | 100% | +94 [+92, +95] | +94 [+90, +96] | yes |
| code: list position → prompt | last tokens + print + list/chain | 200 / 19 | 7% [4, 10] | animals 6% (100/12), months 8% (100/7) | 100% | +93 [+90, +96] | +93 [+90, +96] | yes |
| code: list position → prompt | all of the question + list/chain | 200 / 19 | 6% [4, 9] | animals 6% (100/12), months 7% (100/7) | 100% | +94 [+91, +96] | +94 [+90, +97] | yes |
| code: list position → prompt | every line after the dict | 200 / 19 | 6% [4, 9] | animals 6% (100/12), months 7% (100/7) | 100% | +94 [+91, +96] | +94 [+90, +97] | yes |
| code: list position → prompt | everything after the entry | 200 / 19 | 3% [1, 4] | animals 6% (100/12), months 0% (100/7) | 100% | +97 [+96, +99] | +97 [+94, +99] | yes |
| code: 2-variable chain → prompt | chain line 1 (holds the key) | 199 / 19 | 44% [38, 48] | animals 43% (100/12), months 44% (99/7) | 99% | +56 [+51, +62] | +56 [+49, +63] | yes |
| code: 2-variable chain → prompt | chain line 2 | 199 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (99/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 2-variable chain → prompt | other chain, line 1 | 199 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (99/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 2-variable chain → prompt | other chain, line 2 | 199 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (99/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 2-variable chain → prompt | the print line | 199 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (99/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 2-variable chain → prompt | the rest of the question | 199 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (99/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 2-variable chain → prompt | the last tokens | 199 / 19 | 41% [33, 50] | animals 41% (100/12), months 41% (99/7) | 100% | +59 [+50, +67] | +59 [+52, +65] | yes |
| code: 2-variable chain → prompt | last tokens + print line | 199 / 19 | 37% [29, 45] | animals 36% (100/12), months 37% (99/7) | 100% | +63 [+55, +71] | +63 [+56, +70] | yes |
| code: 2-variable chain → prompt | last tokens + list/chain lines | 199 / 19 | 7% [3, 11] | animals 4% (100/12), months 9% (99/7) | 100% | +93 [+89, +97] | +93 [+90, +96] | yes |
| code: 2-variable chain → prompt | last tokens + print + list/chain | 199 / 19 | 6% [2, 10] | animals 3% (100/12), months 9% (99/7) | 100% | +94 [+90, +98] | +94 [+90, +97] | yes |
| code: 2-variable chain → prompt | all of the question + list/chain | 199 / 19 | 6% [2, 9] | animals 3% (100/12), months 8% (99/7) | 100% | +94 [+91, +98] | +94 [+91, +97] | yes |
| code: 2-variable chain → prompt | every line after the dict | 199 / 19 | 6% [2, 9] | animals 3% (100/12), months 8% (99/7) | 100% | +94 [+91, +98] | +94 [+91, +97] | yes |
| code: 2-variable chain → prompt | everything after the entry | 199 / 19 | 1% [0, 2] | animals 2% (100/12), months 0% (99/7) | 100% | +99 [+98, +100] | +99 [+97, +100] | yes |
| code: 3-variable chain → prompt | chain line 1 (holds the key) | 200 / 19 | 40% [35, 46] | animals 38% (100/12), months 43% (100/7) | 99% | +58 [+53, +65] | +58 [+52, +66] | yes |
| code: 3-variable chain → prompt | chain line 2 | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | -0 [-2, +0] | -1 [-2, +0] | no |
| code: 3-variable chain → prompt | chain line 3 | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 3-variable chain → prompt | other chain, line 1 | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 3-variable chain → prompt | other chain, line 2 | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 3-variable chain → prompt | other chain, line 3 | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 3-variable chain → prompt | the print line | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 3-variable chain → prompt | the rest of the question | 200 / 19 | 100% [100, 100] | animals 100% (100/12), months 100% (100/7) | 100% | +0 [+0, +0] | +0 [+0, +0] | no |
| code: 3-variable chain → prompt | the last tokens | 200 / 19 | 32% [24, 42] | animals 27% (100/12), months 38% (100/7) | 100% | +68 [+58, +76] | +68 [+61, +74] | yes |
| code: 3-variable chain → prompt | last tokens + print line | 200 / 19 | 33% [25, 42] | animals 28% (100/12), months 38% (100/7) | 100% | +67 [+58, +75] | +67 [+60, +74] | yes |
| code: 3-variable chain → prompt | last tokens + list/chain lines | 200 / 19 | 6% [4, 9] | animals 6% (100/12), months 7% (100/7) | 100% | +94 [+91, +96] | +94 [+90, +97] | yes |
| code: 3-variable chain → prompt | last tokens + print + list/chain | 200 / 19 | 6% [4, 9] | animals 6% (100/12), months 7% (100/7) | 100% | +94 [+91, +96] | +94 [+90, +97] | yes |
| code: 3-variable chain → prompt | all of the question + list/chain | 200 / 19 | 6% [3, 8] | animals 6% (100/12), months 5% (100/7) | 100% | +94 [+92, +97] | +94 [+91, +98] | yes |
| code: 3-variable chain → prompt | every line after the dict | 200 / 19 | 6% [3, 8] | animals 5% (100/12), months 6% (100/7) | 100% | +94 [+92, +97] | +94 [+91, +98] | yes |
| code: 3-variable chain → prompt | everything after the entry | 200 / 19 | 1% [0, 3] | animals 2% (100/12), months 0% (100/7) | 100% | +99 [+97, +100] | +99 [+98, +100] | yes |
| code: memory → prompt | the rest of the question | 100 / 12 | 91% [80, 98] | animals 91% (100/12) | 100% | +9 [+2, +20] | +9 [+4, +15] | no |
| code: memory → prompt | the last tokens | 100 / 12 | 20% [12, 28] | animals 20% (100/12) | 100% | +80 [+72, +88] | +80 [+72, +87] | yes |
| code: memory → prompt | all of the question + list/chain | 100 / 12 | 2% [0, 6] | animals 2% (100/12) | 100% | +98 [+94, +100] | +98 [+95, +100] | yes |
| code: memory → prompt | every line after the dict | 100 / 12 | 2% [0, 6] | animals 2% (100/12) | 100% | +98 [+94, +100] | +98 [+95, +100] | yes |
| code: memory → prompt | everything after the entry | 100 / 12 | 3% [0, 7] | animals 3% (100/12) | 99% | +96 [+92, +99] | +96 [+92, +99] | yes |

| family | union | extra loss vs the last tokens alone [95%, entity cluster] | per domain | relays | union - every line after the dict [95%] | explained |
|---|---|---|---|---|---|---|
| code: named → prompt | last tokens + print line | +48 [+40, +56] | animals +49 pts (100/12), months +46 pts (100/7) | yes |  | |
| code: named → prompt | all of the question + list/chain | +48 [+40, +56] | animals +49 pts (100/12), months +46 pts (100/7) | yes | +0 [+0, +0] | yes |
| code: list position → prompt | last tokens + print line | +0 [+0, +2] | animals +1 pts (100/12), months +0 pts (100/7) | no |  | |
| code: list position → prompt | last tokens + list/chain lines | +28 [+22, +36] | animals +25 pts (100/12), months +32 pts (100/7) | yes |  | |
| code: list position → prompt | last tokens + print + list/chain | +28 [+21, +35] | animals +24 pts (100/12), months +32 pts (100/7) | yes |  | |
| code: list position → prompt | all of the question + list/chain | +28 [+22, +36] | animals +24 pts (100/12), months +33 pts (100/7) | yes | +0 [+0, +0] | yes |
| code: 2-variable chain → prompt | last tokens + print line | +5 [+2, +7] | animals +5 pts (100/12), months +4 pts (99/7) | no |  | |
| code: 2-variable chain → prompt | last tokens + list/chain lines | +35 [+28, +42] | animals +37 pts (100/12), months +32 pts (99/7) | yes |  | |
| code: 2-variable chain → prompt | last tokens + print + list/chain | +35 [+28, +42] | animals +38 pts (100/12), months +32 pts (99/7) | yes |  | |
| code: 2-variable chain → prompt | all of the question + list/chain | +36 [+28, +43] | animals +38 pts (100/12), months +33 pts (99/7) | yes | +0 [+0, +0] | yes |
| code: 3-variable chain → prompt | last tokens + print line | -0 [-1, +0] | animals -1 pts (100/12), months +0 pts (100/7) | no |  | |
| code: 3-variable chain → prompt | last tokens + list/chain lines | +26 [+19, +34] | animals +21 pts (100/12), months +31 pts (100/7) | yes |  | |
| code: 3-variable chain → prompt | last tokens + print + list/chain | +26 [+19, +34] | animals +21 pts (100/12), months +31 pts (100/7) | yes |  | |
| code: 3-variable chain → prompt | all of the question + list/chain | +27 [+20, +35] | animals +21 pts (100/12), months +33 pts (100/7) | yes | +0 [-1, +1] | yes |
| code: memory → prompt | all of the question + list/chain | +18 [+11, +26] | animals +18 pts (100/12) | yes | +0 [+0, +0] | yes |

## The agent's priors (job spec hypotheses), checked

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_print_reader | named key: the print line (print(lockers["mouse"])) is a reader of the entry (batch 2: the question words, which start at the print line, are needed: 6% kept). Prior 0.8 | code: named → prompt: +94 [+88, +99] points (reader) | holds |
| H_list_not_reader | list position: the names list line alone is not a reader (the last tokens still read the entry directly). Prior 0.6 | code: list position → prompt: +56 [+47, +65] points (reader) | fails |
| H_relay | list position: the names list line (or the print line) relays the entry: blocking it together with the last tokens costs >= 10 points more than the last tokens alone. Prior 0.65 | last tokens + print line: +0 [+0, +2], last tokens + list/chain lines: +28 [+22, +36] | holds |
| H_explained | in every family, the union (last tokens + print line + list/chain lines + the rest of the question) keeps answer org within 10 points of hiding the entry from every line after the dict, i.e. no other line (the other c... | code: named → prompt: +0 [+0, +0], code: list position → prompt: +0 [+0, +0], code: 2-variable chain → prompt: +0 [+0, +0], code: 3-variable chain → prompt: +0 [-1, +1], code: memory → prompt: +0 [+0, +0] | holds |

## Worked example (examples.json, group one_line_breaks)

```
<|im_start|>user
```python
lockers = {"mouse": 8, "owl": 7, "wolf": 1, "bee": 9, "frog": 5}
print(lockers["owl"])
```
What does this Python code print? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

code: named → prompt, org prompt animals-DK-e5f0-0084. What was done: the print line cannot read the lookup span ('"owl": 7') directly at all 64 layers. Unedited the model answers '7' (answer org '7'); blocked it answers '<|im_end|>' (the prompt's other answers: ['1', '5', '8', '9']). log p(answer org): -0.003 -> -2.649.

