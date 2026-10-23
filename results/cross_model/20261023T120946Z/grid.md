# Every finding on every model

Built by scripts/cross_model_grid.py at 31a4372 (uncommitted changes) (20261023T120946Z) from the saved results; each cell is judged by the rule committed with its run (rule ids in the mapping table below). Nothing here is human-verified. Long format with every number: grid.csv; the files behind each cell: sources.txt.

Cell: verdict, key number [95% CI], n. ✓ holds · ✗ fails · ≈ inconclusive (the rule itself says so; no control failed) · ⚠ not interpretable (a control failed; footnote) · ⊘ not testable (no lens, the gate or competence failed) · · missing (did not run, failed, or no saved verdict) · ○ open (values shown, no committed rule: descriptive). A second line lists a run with another lens (plain J-lens, base-model J++) or another run beside the main one. Numbered footnotes: failed controls and the cell-level notes.

Finding 1: "no random-dictionary control" marks the removal runs that dropped it (Qwen3-32B, Gemma 4, Muse: too large next to the model on an 80 GB GPU); their gate G2 reads the rotated control alone.

J-space removal (finding 1, animal suite) has no committed rule, so its cell is descriptive: the gap is the share of lookups right minus the share of recalls right with the J-space removed (the clean question; items pooled within each group). Its 95% interval: the bridge animals are drawn with replacement, separately for the lookup items and for the recall items (unpaired), 4000 times with seed 0; each draw gives the lookups' mean minus the recalls' mean, and the interval is the 2.5th to 97.5th percentile of those differences. stats.cluster_bootstrap does this resampling for one mean only, so the grid applies it to each group and takes the difference (scripts/cross_model_grid.py gap_ci). Chosen after seeing the data; accepted by Dan (23 Oct).

## Key cells

- Qwen3.6-27B, A lookup ends in a late attention read of the answer's sentence (long context): ✗ 26% [20,33] n=178 [1]
- Qwen3-32B, The order label counts order in the list, not place in the text (filler moved): ✗ 13% vs 3% n=365 [2]
- Olmo-Hybrid-7B, The last tokens read the answer's digit, not the entity's name (draw 2): ✓ 10% [6,17] n=100
- Olmo-Hybrid-7B, A lookup ends in a late attention read of the answer's sentence (draw 2): ✓ 7% [3,14] n=100
- Olmo-Hybrid-7B, Order label for the 1st and 2nd sentence, the bridge's identity after (draw 1): ✓ +58/+31 n=516
- Olmo-Hybrid-7B, Order label for the 1st and 2nd sentence, the bridge's identity after (draw 2): ✓ +52/+35 n=526
- Olmo-Hybrid-7B, The order label counts order in the list, not place in the text (filler moved): ✓ 29% vs 9% n=296
- OLMo-3-7B-I, A lens push writes a stated bridge for recall; the lookup does not follow (main rule): ✓ 0% vs recall 51% n=100
- Qwen3-32B, The lens names a stated bridge where it is stated (lens gate) (v1 (at the word)): ✓ 72% [59,81] n=60<br>plain J-lens: ✗ 8% [4,18] n=60
- Qwen3-32B, The lens names a stated bridge where it is stated (lens gate) (v2 (after the word)): ✗ 7% [3,16] n=60<br>plain J-lens: ✗ 0% [0,6] n=60
- OLMo-3-7B-I, The lens names a stated bridge where it is stated (lens gate) (v1 (at the word)): ✓ 100% [94,100] n=60<br>plain J-lens: ✓ 85% [74,92] n=60
- OLMo-3-7B-I, The lens names a stated bridge where it is stated (lens gate) (v2 (after the word)): ✗ 3% [1,11] n=60<br>plain J-lens: ✗ 0% [0,6] n=60
- Gemma 4 31B-it, The lens names a stated bridge where it is stated (lens gate) (v1 (at the word)): ✓ 95% [86,98] n=59<br>base-model J++: ✓ 81% [70,89] n=59
- Gemma 4 31B-it, The lens names a stated bridge where it is stated (lens gate) (v2 (after the word)): ✗ 3% [1,12] n=59<br>base-model J++: ✗ 2% [0,9] n=59
- Muse 30B, The lens names a stated bridge where it is stated (lens gate) (v1 (at the word)): ✓ 95% [86,98] n=57
- Muse 30B, The lens names a stated bridge where it is stated (lens gate) (v2 (after the word)): ✗ 7% [3,17] n=57
- Qwen3-32B, A lookup ignores the lens-readable part of a stated bridge (draw 1): ⚠ 5% [2,10] n=120 [3]<br>plain J-lens: ⚠ 3% [1,8] n=120 [4]
- OLMo-3-7B-I, A lookup ignores the lens-readable part of a stated bridge (draw 2): ⊘ not testable: no layer from 16 on<br>plain J-lens: ⊘ not testable: no layer from 16 on
- Gemma 4 31B-it, A lookup ignores the lens-readable part of a stated bridge (draw 2): · missing: blocked [5]<br>base-model J++: · missing: not run
- Muse 30B, A lookup ignores the lens-readable part of a stated bridge (draw 2): ⊘ not testable: too few scenes

## Lens

Lens quality: pass@10 (macro) on the J++ recipe's held-out readout evals, minus the logit lens on the same items and layers (results/lens_table/20261023T091623Z/table.json). Gates: the bridge in the lens's top 10 at its own sentence (v1) or after its word (v2), share of items.

| Model | Lens | Source, sha256 | Recipe (prompts) | pass@10 | Gate v1 | Gate v2 | Listed beside |
|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | J++ | published (neuronpedia), bbef480b | jpp_lens recipe (koayon/jpp-lenses), 64 WikiText prompts | 0.71 (+0.28 vs the logit lens) | ✓ 95% [86,98] n=60 | ✗ 7% [3,16] n=60 | plain J-lens (plain J-lens, published (neuronpedia, n1000), 1718c8c5): v1 ✓ 92% [82,96] n=60, v2 ✗ 0% [0,6] n=60, pass@10 0.43 (-0.00 vs the logit lens) |
| Qwen3.5-9B | J++ | published (neuronpedia), 8cda12f7 | jpp_lens recipe (koayon/jpp-lenses), 64 WikiText prompts | pending | ✓ 100% [94,100] n=60 | ✗ 5% [2,14] n=60 | - |
| Olmo-Hybrid-7B | none | - | - | - | ⊘ no lens | ⊘ no lens | - |
| Qwen3-32B | J++ | ours, 7d6856b6 | J++ (jpp_lens@93f02cd), 64 WikiText prompts (2 shards x 32), layers 16-51 | 0.55 (+0.43 vs the logit lens, on the 298 items both runs kept) | ✓ 72% [59,81] n=60 | ✗ 7% [3,16] n=60 | plain J-lens (plain J-lens, published (neuronpedia), 0af5ccf2): v1 ✗ 8% [4,18] n=60, v2 ✗ 0% [0,6] n=60, pass@10 0.24 (+0.11 vs the logit lens) |
| OLMo-3-7B-I | J++ | ours, 6847cfb3 | J++ (jpp_lens@93f02cd), 64 WikiText prompts, layers 0-30 | 0.47 (+0.15 vs the logit lens) | ✓ 100% [94,100] n=60 | ✗ 3% [1,11] n=60 | plain J-lens (plain J-lens, published (mhough), b847dbba): v1 ✓ 85% [74,92] n=60, v2 ✗ 0% [0,6] n=60, pass@10 0.36 (+0.04 vs the logit lens) |
| Muse 30B | J++ | Zach, 90fc5e52 | J++ (jpp_lens@93f02cd + jpp_lens_muse_1022.patch), 32 WikiText prompts, layers 0-50 | 0.96 (+0.29 vs the logit lens) | ✓ 95% [86,98] n=57 | ✗ 7% [3,17] n=57 | - |
| Gemma 4 31B-it | J++ | Zach (every layer), d16d81d8 | J++ (jpp_lens@93f02cd), 64 WikiText prompts, layers 0-58 | 0.63 (+0.07 vs the logit lens) | ✓ 95% [86,98] n=59 | ✗ 3% [1,12] n=59 | base-model J++ (J++, published (neuronpedia, base model), ef50bc54): v1 ✓ 81% [70,89] n=59, v2 ✗ 2% [0,9] n=59, pass@10 0.52 (-0.04 vs the logit lens) |
| Qwen3.5-122B | J++ | published (neuronpedia), b771e502 | jpp_lens recipe (koayon/jpp-lenses), fit on the bf16 weights | pending | ✓ 100% [94,100] n=60 | ✗ 13% [7,24] n=60 | - |

## The grid

| # | Finding | Setting | Qwen3.6-27B | Qwen3.5-9B | Olmo-Hybrid-7B | Qwen3-32B | OLMo-3-7B-I | Muse 30B | Gemma 4 31B-it | Qwen3.5-122B |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Removing the J-space breaks recall, not the lookup | tasks, Zach's rule | ✓ +36 pts n=506 | · missing: no spec | ⊘ not testable: no lens | · missing: no spec | · missing: no spec | · missing: no spec | · missing: not on Zach's branch | · missing: no spec |
| 1 | Removing the J-space breaks recall, not the lookup | animal suite | ○ gap +78 [+62,+90] n=400 | ○ gap +14 [+1,+30] n=400 | ⊘ not testable: no lens | ○ gap +9 [+0,+19] n=400, no random-dictionary control | ⚠ gap +28 [+16,+41] n=400 [6]<br>plain J-lens: ⚠ gap +14 [+4,+26] n=400 [7] | ○ gap +10 [+3,+18] n=400, no random-dictionary control | · missing: blocked<br>refit J++: ○ gap +1 [+0,+3] n=200 | ○ gap +10 [+0,+22] n=400<br>Zach's pilot: ○ gap +17 [+8,+26] n=400 |
| 2 | A lookup ignores the lens-readable part of a stated bridge | draw 1 | ✓ 0% [0,3] n=120 | · missing: no spec | ⊘ not testable: no lens | ⚠ 5% [2,10] n=120 [3]<br>plain J-lens: ⚠ 3% [1,8] n=120 [4] | · missing: no spec | · missing: no spec | · missing: no spec | · missing: no spec |
| 2 | A lookup ignores the lens-readable part of a stated bridge | draw 2 | ✓ 1% [0,3] n=180<br>plain J-lens: ⚠ 0% [0,2] n=180 [8] | ✓ 1% [0,3] n=180 | ⊘ not testable: no lens | · missing: no spec | ⊘ not testable: no layer from 16 on<br>plain J-lens: ⊘ not testable: no layer from 16 on | ⊘ not testable: too few scenes | · missing: blocked [5]<br>base-model J++: · missing: not run | ✗ 29% [23,36] n=180 |
| 2 | A lookup ignores the lens-readable part of a stated bridge | table | ✓ 2% [1,8] n=83 | ✓ 0% [0,4] n=93 | ⊘ not testable: no lens | · missing: pending | ⊘ not testable: too few scenes | ⊘ not testable: too few scenes | · missing: blocked [9] | ✗ 49% [39,59] n=88 |
| 2 | A lookup ignores the lens-readable part of a stated bridge | JSON | ✓ 3% [1,9] n=97 | ✓ 0% [0,4] n=87 | ⊘ not testable: no lens | · missing: pending | ⊘ not testable: too few scenes | ⊘ not testable: too few scenes | · missing: blocked [10] | ✗ 34% [25,44] n=92 |
| 3 | The last tokens read the answer's digit, not the entity's name | draw 1 | ✓ 11% [8,15] n=300 | ✓ 2% [1,4] n=300 | ✓ 11% [6,19] n=100 | ✓ 4% [2,7] n=300 | ✓ 5% [2,11] n=100 | ✓ 3% [2,6] n=300 | ✓ 28% [23,33] n=300 | ✓ 9% [7,13] n=300 |
| 3 | The last tokens read the answer's digit, not the entity's name | draw 2 | ✓ 10% [7,14] n=300 | ✓ 1% [0,3] n=300 | ✓ 10% [6,17] n=100 | ✓ 4% [2,7] n=199 | ✓ 0% [0,4] n=100 | ✓ 1% [1,3] n=299 | ✓ 29% [24,34] n=300 | ✓ 7% [5,10] n=300 |
| 3 | The last tokens read the answer's digit, not the entity's name | draw 3 | · missing: no spec | ✓ 2% [1,4] n=300 | · missing: not run | ✓ 2% [1,4] n=199 | ✓ 5% [2,11] n=99 | ✓ 1% [1,3] n=300 | ✓ 27% [23,33] n=300 | · missing: no spec |
| 3 | The last tokens read the answer's digit, not the entity's name | prose | ✓ 9% [4,20] n=53 | ✓ 8% [2,26] n=24 | ⚠ 14% [4,40] n=14 [11] | ✓ 6% [2,20] n=32 | ⚠ 0% [0,18] n=18 [12] | ✗ 40% [12,77] n=5 | ✓ 34% [21,51] n=35 | ✓ 21% [12,33] n=53 |
| 3 | The last tokens read the answer's digit, not the entity's name | table | ✓ 4% [1,13] n=52 | ✓ 0% [0,11] n=32 | ✓ 0% [0,14] n=24 | ✓ 0% [0,9] n=38 | ✓ 0% [0,14] n=23 | ⊘ not testable: no item right | ✓ 11% [5,22] n=55 | ✓ 4% [1,13] n=52 |
| 3 | The last tokens read the answer's digit, not the entity's name | JSON | ✓ 4% [1,13] n=54 | ✓ 4% [1,18] n=27 | ⚠ 0% [0,22] n=14 [13] | ✓ 0% [0,9] n=41 | ✓ 0% [0,19] n=16 | ⊘ not testable: no item right | ✓ 23% [14,36] n=56 | ✓ 2% [0,10] n=52 |
| 4 | A lookup ends in a late attention read of the answer's sentence | draw 1 | ✓ 9% [6,12] n=300 [14] | ✓ 3% [1,5] n=300 [15] | ✓ 8% [4,15] n=100 [16] | ✓ 3% [2,6] n=300 [17] | ✓ 0% [0,4] n=100 [18] | ✓ 3% [1,5] n=300 [19] | ✗ 23% [18,28] n=300 [20] [21] | ✓ 5% [3,8] n=300 [22] |
| 4 | A lookup ends in a late attention read of the answer's sentence | draw 2 | ✓ 7% [5,11] n=300 | ✓ 1% [1,3] n=300 | ✓ 7% [3,14] n=100 | ✓ 3% [2,6] n=299 | ✓ 0% [0,4] n=100 | ✓ 1% [1,3] n=300 | ✗ 22% [17,27] n=300 [23] | ✓ 5% [3,8] n=300 |
| 4 | A lookup ends in a late attention read of the answer's sentence | draw 3 | · missing: no spec | ✓ 2% [1,4] n=300 | · missing: not run | ✓ 1% [0,4] n=199 | ✓ 1% [0,6] n=99 | ✓ 2% [1,4] n=300 | ✓ 19% [15,24] n=300 | · missing: no spec |
| 4 | A lookup ends in a late attention read of the answer's sentence | prose | ✓ 9% [4,20] n=53 | ✓ 8% [2,26] n=24 | ⚠ 14% [4,40] n=14 [24] | ✓ 6% [2,20] n=32 | ⚠ 0% [0,18] n=18 [25] | ⚠ 40% [12,77] n=5 [26] | ✗ 34% [21,51] n=35 [27] | ✓ 11% [5,23] n=53 |
| 4 | A lookup ends in a late attention read of the answer's sentence | table | ✓ 4% [1,13] n=52 | ✓ 0% [0,11] n=32 | ✗ 0% [0,14] n=24 | ✓ 0% [0,9] n=38 | ✓ 0% [0,14] n=23 | ⊘ not testable: no item right | ✓ 15% [8,26] n=55 | ✓ 2% [0,10] n=52 |
| 4 | A lookup ends in a late attention read of the answer's sentence | JSON | ✓ 2% [0,10] n=54 | ✓ 0% [0,12] n=27 | ⚠ 0% [0,22] n=14 [28] | ✓ 0% [0,9] n=41 | ⚠ 6% [1,28] n=16 [29] | ⊘ not testable: no item right | ✗ 21% [13,34] n=56 [30] | ✓ 0% [0,7] n=52 |
| 4 | A lookup ends in a late attention read of the answer's sentence | long context | ✗ 26% [20,33] n=178 [1] | ✓ 1% [0,4] n=156 | · missing: running | ✓ 2% [1,8] n=93 | ✓ 5% [1,16] n=41 | ✓ 17% [12,23] n=167 | · missing: failed | ✓ 7% [4,12] n=171 |
| 4 | A lookup ends in a late attention read of the answer's sentence | draw 1, last tokens' share | · missing: no floor block in this run | · missing: no floor block in this run | · missing: no floor block in this run | · missing: no floor block in this run | · missing: no floor block in this run | · missing: no floor block in this run | · missing: no floor block in this run | · missing: no floor block in this run |
| 4 | A lookup ends in a late attention read of the answer's sentence | draw 2, last tokens' share | · missing: not run | · missing: not run | · missing: not run | · missing: not run | · missing: not run | · missing: not run | · missing: not run | · missing: not run |
| 4 | A lookup ends in a late attention read of the answer's sentence | long context, last tokens' share | · missing: not run | · missing: not run | · missing: not run | · missing: not run | · missing: not run | · missing: not run | · missing: out of memory | · missing: not run |
| 5 | Order label for the 1st and 2nd sentence, the bridge's identity after | draw 1 | ✓ +98/+17 n=762 | ✓ +52/+35 n=450 | ✓ +58/+31 n=516 | ✗ +92/+3 n=450 | ✓ +43/+26 n=412 | ✓ +75/+38 n=434 | ✓ +33/+30 n=425 | ✓ +72/+43 n=450 |
| 5 | Order label for the 1st and 2nd sentence, the bridge's identity after | draw 2 | ✓ +94/+18 n=767 | ✓ +51/+43 n=450 | ✓ +52/+35 n=526 | ✓ +82/+12 n=447 | ✓ +51/+26 n=393 | ✓ +79/+30 n=440 | ✓ +24/+28 n=426 | ✓ +64/+41 n=450 |
| 5 | Order label for the 1st and 2nd sentence, the bridge's identity after | draw 3 | ✓ +95/+14 n=766 | ✓ +53/+40 n=450 | · missing: not run | ✓ +84/+12 n=445 | ✓ +40/+22 n=408 | ✓ +76/+24 n=436 | ✓ +31/+27 n=432 | ✓ +65/+34 n=450 |
| 5 | Order label for the 1st and 2nd sentence, the bridge's identity after | 8 sentences | ✓ +98/+32 n=419 | ✓ +56/+50 n=341 | ✓ +79/+31 n=186 | ✓ +83/+20 n=256 | ✓ +50/+33 n=105 | ✓ +78/+22 n=151 | · missing: no spec | ✓ +80/+46 n=392 |
| 5 | Order label for the 1st and 2nd sentence, the bridge's identity after | 12 sentences | ✓ +69/+18 n=413 | ✓ +57/+35 n=318 | ✓ +70/+13 n=191 | ✓ +73/+14 n=269 | ✓ +44/+18 n=92 | ✓ +56/+5 n=124 | · missing: no spec | ✓ +30/+24 n=376 |
| 6 | The order label counts order in the list, not place in the text | filler moved | ✓ 39% vs 9% n=435 | ✓ 22% vs 5% n=406 [31] | ✓ 29% vs 9% n=296 | ✗ 13% vs 3% n=365 [2] | ✓ 31% vs 11% n=202 | ✓ 38% vs 9% n=372 [32] | ✓ 12% vs 2% n=338 [33] | ✓ 29% vs 8% n=425 [34] |
| 6 | The order label counts order in the list, not place in the text | one statement more | ✓ 31% vs 9% n=434 | ✗ 14% vs 7% n=391 [35] | ✗ 20% vs 8% n=270 | ✗ 4% vs 4% n=337 [36] | ✗ 23% vs 12% n=190 | ✓ 30% vs 7% n=319 [37] | ✗ 9% vs 2% n=266 [38] | ✓ 22% vs 5% n=426 [39] |
| 6 | The order label counts order in the list, not place in the text | one statement fewer | ✓ 39% vs 16% n=442 | ✗ 23% vs 8% n=405 [40] | ✗ 31% vs 10% n=296 | ✗ 14% vs 5% n=361 [41] | ✗ 27% vs 10% n=216 | ✓ 43% vs 14% n=310 [42] | ✗ 11% vs 3% n=276 [43] | ✓ 31% vs 11% n=429 [44] |
| 7 | A lens push writes a stated bridge for recall; the lookup does not follow | main rule | ≈ 29% vs recall 84% n=100 | ⚠  [45] | ⊘ not testable: no lens | · missing: running | ✓ 0% vs recall 51% n=100 | ⚠  [46] | · missing: blocked | ✓ 0% vs recall 89% n=94 |
| 7 | A lens push writes a stated bridge for recall; the lookup does not follow | amended rule | ✓ 0% vs recall 70% n=100 | ⚠  [47] | ⊘ not testable: no lens | · missing: running | ✓ 0% vs recall 51% n=100 | ⚠  [48] | · missing: blocked | ✓ 0% vs recall 89% n=94 |
| 7 | A lens push writes a stated bridge for recall; the lookup does not follow | main rule, draw 2 | ✓ 0% vs recall 84% n=100 | ✓ 0% vs recall 40% n=100 | ⊘ not testable: no lens | · missing: no spec | · missing: no spec | · missing: no spec | · missing: no spec | · missing: no spec |
| 7 | A lens push writes a stated bridge for recall; the lookup does not follow | amended rule, draw 2 | ✓ 0% vs recall 84% n=100 | ✓ 0% vs recall 40% n=100 | ⊘ not testable: no lens | · missing: no spec | · missing: no spec | · missing: no spec | · missing: no spec | · missing: no spec |
| 8 | Where the lens writes the bridge, the lookup still does not follow it | stated bridge, draw 1 | ✓ 0% vs recall 51% n=120 | · missing: no spec | ⊘ not testable: no lens | ⚠ 0% vs recall 22% n=120 [49]<br>plain J-lens: ✓ 0% vs recall 23% n=120 | · missing: no spec | · missing: no spec | · missing: no spec | · missing: no spec |
| 8 | Where the lens writes the bridge, the lookup still does not follow it | stated bridge, draw 2 | ✓ 0% vs recall 43% n=180<br>plain J-lens: ✓ 0% vs recall 32% n=180 | ✓ 0% vs recall 55% n=180 | ⊘ not testable: no lens | · missing: no spec | ⊘ not testable: no layer from 16 on<br>plain J-lens: ⊘ not testable: no layer from 16 on | ⊘ not testable: too few scenes | · missing: pending [50]<br>base-model J++: · missing: not run | ✗ 29% vs recall 78% n=180 |
| 8 | Where the lens writes the bridge, the lookup still does not follow it | last tokens | ○ 0% [0,1] n=420 | ○ 0% [0,1] n=410 | ⊘ not testable: no lens | ○ 0% [0,1] n=377 | ○ 0% [0,1] n=257<br>plain J-lens: ○ 0% [0,1] n=257 | · missing: no spec | · missing: blocked | ○ 0% [0,1] n=418 |

What the key numbers are, by finding:

- 1: tasks, Zach's rule: points, memory-final minus prompt-final loss under the lens knock-out (his verdict); animal suite: points, lookups minus recalls right with the J-space removed [unpaired bootstrap over bridge entities], descriptive.
- 2: % of lookups the lens-readable part of a stated bridge's change switches.
- 3: % right with the sentence without its name hidden from the last tokens (the digit hidden too).
- 4: % right with the answer's sentence hidden from the last tokens (chance: 20% in the draws, five listed answers; 33% in prose / table / JSON, three). Last tokens' share: the share of the drop the last tokens carry, (unedited - last tokens blocked) / (unedited - every token after the sentence blocked).
- 5: points, position - identity for the 1st-2nd asked sentence / identity - position from the 3rd on.
- 6: % of patched answers at the same order in the list vs at the same place in the text (or from the end).
- 7: % of lookups vs recalls the lens push switches at the rule's cell.
- 8: % of lookups vs recalls the lens push writes (1x) at the stated bridge's cell; last tokens: % of lookups the lens push moves in the fitted-code test.

## Footnotes

1. Qwen3.6-27B, A lookup ends in a late attention read of the answer's sentence, long context: at chance (26% [20, 33], chance 20%)
2. Qwen3-32B, The order label counts order in the list, not place in the text, filler moved: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
3. Qwen3-32B, A lookup ignores the lens-readable part of a stated bridge, draw 1: not interpretable (the positive control fails)
4. Qwen3-32B, A lookup ignores the lens-readable part of a stated bridge, draw 1 (plain J-lens): not interpretable (the positive control fails)
5. Gemma 4 31B-it, A lookup ignores the lens-readable part of a stated bridge, draw 2: n = 167 (topics) / 169 (formats) instead of the pre-registered 180: 73c4a69 skips scenes whose positions fail the alignment check; accepted by Dan, 23 Oct
6. OLMo-3-7B-I, Removing the J-space breaks recall, not the lookup, animal suite: not interpretable (G2: a control removal keeps < 90% on country-R/clean (rotated 80%), country-R/clean (random 80%))
7. OLMo-3-7B-I, Removing the J-space breaks recall, not the lookup, animal suite (plain J-lens): not interpretable (G2: a control removal keeps < 90% on country-R/clean (rotated 80%), country-R/clean (random 80%))
8. Qwen3.6-27B, A lookup ignores the lens-readable part of a stated bridge, draw 2 (plain J-lens): not interpretable (the positive control fails)
9. Gemma 4 31B-it, A lookup ignores the lens-readable part of a stated bridge, table: n = 167 (topics) / 169 (formats) instead of the pre-registered 180: 73c4a69 skips scenes whose positions fail the alignment check; accepted by Dan, 23 Oct
10. Gemma 4 31B-it, A lookup ignores the lens-readable part of a stated bridge, JSON: n = 167 (topics) / 169 (formats) instead of the pre-registered 180: 73c4a69 skips scenes whose positions fail the alignment check; accepted by Dan, 23 Oct
11. Olmo-Hybrid-7B, The last tokens read the answer's digit, not the entity's name, prose: not interpretable (the off-path control: an off-path sentence's part hidden keeps < 90%)
12. OLMo-3-7B-I, The last tokens read the answer's digit, not the entity's name, prose: not interpretable (the off-path control: an off-path sentence's part hidden keeps < 90%)
13. Olmo-Hybrid-7B, The last tokens read the answer's digit, not the entity's name, JSON: not interpretable (the off-path control: an off-path sentence's part hidden keeps < 90%)
14. Qwen3.6-27B, A lookup ends in a late attention read of the answer's sentence, draw 1: draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older rule); accepted by Dan, 23 Oct
15. Qwen3.5-9B, A lookup ends in a late attention read of the answer's sentence, draw 1: draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older rule); accepted by Dan, 23 Oct
16. Olmo-Hybrid-7B, A lookup ends in a late attention read of the answer's sentence, draw 1: draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older rule); accepted by Dan, 23 Oct
17. Qwen3-32B, A lookup ends in a late attention read of the answer's sentence, draw 1: draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older rule); accepted by Dan, 23 Oct
18. OLMo-3-7B-I, A lookup ends in a late attention read of the answer's sentence, draw 1: draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older rule); accepted by Dan, 23 Oct
19. Muse 30B, A lookup ends in a late attention read of the answer's sentence, draw 1: draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older rule); accepted by Dan, 23 Oct
20. Gemma 4 31B-it, A lookup ends in a late attention read of the answer's sentence, draw 1: at chance (23% [18, 28], chance 20%)
21. Gemma 4 31B-it, A lookup ends in a late attention read of the answer's sentence, draw 1: draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older rule); accepted by Dan, 23 Oct
22. Qwen3.5-122B, A lookup ends in a late attention read of the answer's sentence, draw 1: draw 1 judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older rule); accepted by Dan, 23 Oct
23. Gemma 4 31B-it, A lookup ends in a late attention read of the answer's sentence, draw 2: at chance (22% [17, 27], chance 20%)
24. Olmo-Hybrid-7B, A lookup ends in a late attention read of the answer's sentence, prose: not interpretable (the off-path control: the off-path sentence hidden keeps < 90% or its lower bound < 85%)
25. OLMo-3-7B-I, A lookup ends in a late attention read of the answer's sentence, prose: not interpretable (the off-path control: the off-path sentence hidden keeps < 90% or its lower bound < 85%)
26. Muse 30B, A lookup ends in a late attention read of the answer's sentence, prose: not interpretable (the off-path control: the off-path sentence hidden keeps < 90% or its lower bound < 85%)
27. Gemma 4 31B-it, A lookup ends in a late attention read of the answer's sentence, prose: at chance (34% [21, 51], chance 33%)
28. Olmo-Hybrid-7B, A lookup ends in a late attention read of the answer's sentence, JSON: not interpretable (the off-path control: the off-path sentence hidden keeps < 90% or its lower bound < 85%)
29. OLMo-3-7B-I, A lookup ends in a late attention read of the answer's sentence, JSON: not interpretable (the off-path control: the off-path sentence hidden keeps < 90% or its lower bound < 85%)
30. Gemma 4 31B-it, A lookup ends in a late attention read of the answer's sentence, JSON: at chance (21% [13, 34], chance 33%)
31. Qwen3.5-9B, The order label counts order in the list, not place in the text, filler moved: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
32. Muse 30B, The order label counts order in the list, not place in the text, filler moved: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
33. Gemma 4 31B-it, The order label counts order in the list, not place in the text, filler moved: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
34. Qwen3.5-122B, The order label counts order in the list, not place in the text, filler moved: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
35. Qwen3.5-9B, The order label counts order in the list, not place in the text, one statement more: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
36. Qwen3-32B, The order label counts order in the list, not place in the text, one statement more: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
37. Muse 30B, The order label counts order in the list, not place in the text, one statement more: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
38. Gemma 4 31B-it, The order label counts order in the list, not place in the text, one statement more: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
39. Qwen3.5-122B, The order label counts order in the list, not place in the text, one statement more: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
40. Qwen3.5-9B, The order label counts order in the list, not place in the text, one statement fewer: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
41. Qwen3-32B, The order label counts order in the list, not place in the text, one statement fewer: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
42. Muse 30B, The order label counts order in the list, not place in the text, one statement fewer: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
43. Gemma 4 31B-it, The order label counts order in the list, not place in the text, one statement fewer: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
44. Qwen3.5-122B, The order label counts order in the list, not place in the text, one statement fewer: decisive layers by the donor-digit rule (the spec's rule, applied by the grid: pointer_swap's code tests every swept layer); accepted by Dan, 23 Oct
45. Qwen3.5-9B, A lens push writes a stated bridge for recall; the lookup does not follow, main rule: not interpretable (no cell where the lens push writes recall: the positive control fails)
46. Muse 30B, A lens push writes a stated bridge for recall; the lookup does not follow, main rule: not interpretable (no cell where the lens push writes recall: the positive control fails)
47. Qwen3.5-9B, A lens push writes a stated bridge for recall; the lookup does not follow, amended rule: not interpretable (no cell where the lens push writes recall: the positive control fails)
48. Muse 30B, A lens push writes a stated bridge for recall; the lookup does not follow, amended rule: not interpretable (no cell where the lens push writes recall: the positive control fails)
49. Qwen3-32B, Where the lens writes the bridge, the lookup still does not follow it, stated bridge, draw 1: not interpretable (the lookup write is inconclusive by the rule)
50. Gemma 4 31B-it, Where the lens writes the bridge, the lookup still does not follow it, stated bridge, draw 2: n = 167 (topics) / 169 (formats) instead of the pre-registered 180: 73c4a69 skips scenes whose positions fail the alignment check; accepted by Dan, 23 Oct

## Choices made after seeing the data

- Where the lens writes the bridge (finding 8, stated bridge): the cell holds iff the readwrite verdicts say recall written and lookup not written; recall not written means no positive control (not interpretable). The combination of the two committed per-family verdicts was written by the grid agent and accepted by Dan (23 Oct).
- Counting (finding 6) on Qwen3.5-9B, Qwen3-32B, Muse, Gemma and Qwen3.5-122B: the decisive layers are the swept layers where the donor's digit has its Wilson upper bound < 10% (the specs' rule, applied by the grid: pointer_swap's code tests every swept layer). Accepted by Dan (23 Oct).
- Late read (finding 4), draw 1: judged by the late-read rule fixed on 22 Oct for the second draws (the first draws ran under the older 'needed' rule). Accepted by Dan (23 Oct).
- The lens push's main rule says 'inconclusive' where the lookup moves 10-30%: shown as its own word, 'inconclusive', not as a failed control (Dan, 23 Oct).
- J-space removal (finding 1, animal suite) has no committed rule, so its cell is descriptive: the gap is the share of lookups right minus the share of recalls right with the J-space removed (the clean question; items pooled within each group). Its 95% interval: the bridge animals are drawn with replacement, separately for the lookup items and for the recall items (unpaired), 4000 times with seed 0; each draw gives the lookups' mean minus the recalls' mean, and the interval is the 2.5th to 97.5th percentile of those differences. stats.cluster_bootstrap does this resampling for one mean only, so the grid applies it to each group and takes the difference (scripts/cross_model_grid.py gap_ci). Chosen after seeing the data; accepted by Dan (23 Oct).
- A late read that fails with its interval around chance (guessing among the scene's listed answers: 20% in the draws' five, 33% in the prose / table / JSON scenes' three; from each run's cases) is footnoted 'at chance' (Gemma's reading in the README; Dan, 23 Oct; chance per run since 23 Oct, it was 20% everywhere before).
- Seven verdict words: 'open' is its own word for a cell that shows values under no committed rule (finding 1's animal-suite removal, finding 8's last-token lens arm), never 'missing' for that reason (Dan, 23 Oct).

## Mapping: names, internal codes, scripts, rules

| # | Finding | Internal codes | Scripts | Rule ids |
|---|---|---|---|---|
| 1 | Removing the J-space breaks recall, not the lookup | C1 (Zach's J-space knock-out; the J-space removal) | Zach's scripts/c1_v2.py (his branch); scripts/ablate_pilot.py | removal, zach-c1 |
| 2 | A lookup ignores the lens-readable part of a stated bridge | D1 (topics, formats; parts) | scripts/statement_positions.py parts, scripts/d1_verdict.py | stated-bridge |
| 3 | The last tokens read the answer's digit, not the entity's name | D2 parts (name vs digit) | scripts/attn_knockout.py, scripts/d2_parts.py, scripts/d2_formats.py | formats, name-digit |
| 4 | A lookup ends in a late attention read of the answer's sentence | D2 late read (C1b); relay floor (A3) | scripts/attn_knockout.py, scripts/d2_formats.py | formats, late-read, late-read-v2 |
| 5 | Order label for the 1st and 2nd sentence, the bridge's identity after | D3 v4 / v5 (pointer_swap) | scripts/pointer_swap.py, scripts/finding5_confirm.py | order-identity |
| 6 | The order label counts order in the list, not place in the text | D3 v4x (pointer_v4x) | scripts/pointer_swap.py (v4x tests) | counting |
|  | The lens names a stated bridge where it is stated (lens gate) | lens gate v1 / v2 | scripts/lens_gate.py | lens-gate-v1, lens-gate-v2 |
| 7 | A lens push writes a stated bridge for recall; the lookup does not follow | D4 v2 / v2.1 (early_push_where) | scripts/early_push_where.py | push-amended, push-main |
| 8 | Where the lens writes the bridge, the lookup still does not follow it | D1 readwrite; D3b lens arm | scripts/statement_positions.py readwrite, scripts/pointer_fit.py | fitted-code, lens-write |

| Rule id | Rule |
|---|---|
| late-read | the answer's sentence hidden from the last tokens in every attention layer (every layer on attention-only models) leaves <= 20% right with the Wilson upper bound <= 30%; the off-path sentence hidden there keeps >= 90% (lower bound >= 85%); on a hybrid, hidden in every DeltaNet layer instead keeps >= 90%. Memory -> prompt, items right unedited (fixed 22 Oct; scripts/d2_formats.py late_read) |
| late-read-v2 | reported beside late-read, whose verdicts do not change (Dan, 23 Oct). Memory -> prompt, items right unedited. The last tokens' share of the drop = (unedited - the answer's sentence hidden from the last tokens) / (unedited - hidden from every token after it); the relay = the first block's share right minus the second's. Holds iff the share >= 0.70, hidden from every token after it leaves <= 10% right with the Wilson upper bound <= 15% (the floor), the off-path sentence hidden at the same places keeps >= 90% at both, and on a hybrid the answer's sentence hidden in every DeltaNet layer instead keeps >= 90%. The last tokens are blocked as in late-read (every attention layer on a hybrid, every layer otherwise); every token after the sentence in every attention layer where the run has that block, else in all layers: the first scene set's runs blocked it in all layers, DeltaNet included, which on a hybrid hides more than the definition, so their share is a conservative lower bound (Dan, 23 Oct). A failed off-path control or a floor above its bar is not interpretable; a share below 0.70 fails, as does a DeltaNet block that keeps < 90% (as in late-read). The share's 95% interval: items resampled with replacement (paired), 4000 draws, seed 0 (scripts/cross_model_grid.py late_read_v2) |
| name-digit | the off-path sentence's parts hidden keep >= 90% at both places (valid-split); then the sentence without its name hidden from the last tokens leaves <= 35% right and without its digit >= 70% (H-digit-final-split). Memory -> prompt (amended 22 Oct 16:40; scripts/d2_parts.py verdicts) |
| formats | the late-read and name-vs-digit rules per format (prose, table, JSON), memory -> prompt (scripts/d2_formats.py, fixed 22 Oct evening) |
| order-identity | A: 1st-2nd asked, position - identity, entity-cluster lower bound > 0; B: 3rd on, identity - position >= 0 with lower bound >= -0.05; holds iff A and B. Layer: the last swept layer where the donor's digit has its Wilson upper bound < 10%, or fixed (Qwen3.6-27B: 50) (scripts/finding5_confirm.py) |
| counting | filler moved: the order slot's lower bound above the same place's upper bound, pooled and in >= 2 of 3 topics at one decisive layer; one more / one fewer: from the start above from the end and the same place, both layouts, same layer (scripts/pointer_swap.py v4x_tests). Decisive layers: the 27B's 48 and 50 and OLMo's 17-19 fixed; elsewhere the swept layers where the donor's digit has its Wilson upper bound < 10% (the specs) |
| lens-gate-v1 | the bridge in the lens's top 10 at its own sentence on >= 50% of items, the other bridge on <= 20% (scripts/lens_gate.py gate, 22 Oct) |
| lens-gate-v2 | the same bars read after the bridge's word (scripts/lens_gate.py gate_v2, 22 Oct 23:00) |
| stated-bridge | at the cell chosen without the lens: the lens-readable part alone switches <= 10% of lookups and the rest >= 50%, while the lens-readable part switches >= 30% of recalls (the control); where set, lookups keep their answer under the lens-part patch on >= 80% (scripts/d1_verdict.py) |
| push-main | rule v2: the valid cell with the most recall; holds (H-around) iff the lookup switches <= 10% and the scene-paired recall - lookup gap's lower bound >= 20 points; inconclusive where the rule says so (no control failed there); not interpretable when the off-path check fails or no cell writes recall (scripts/early_push_where.py decide) |
| push-amended | rule v2.1: v2 among cells from layer 20 on (Qwen3.5-9B: 10); written knowing the old data, reported beside the main rule |
| lens-write | statement_positions' write verdicts (written / not written / inconclusive) at the stated-bridge cell's set, primary window; holds iff recall is written and the lookup not written (recall not written: no positive control) |
| fitted-code | scripts/pointer_fit.py's rule judges the fitted position code; its lens push arm has no rule of its own: values only, verdict open (Dan, 23 Oct) |
| zach-c1 | Zach's C1-graded rule (scripts/c1_v2.py on his branch, fixed 21 Oct): at the middle band, the memory-final words lose >= 30 points more accuracy than the prompt-final words under the top-10 lens knock-out, and every word's rotated control stays within 10 points of unedited; his verdict file is read as it is (results/ablate_v2/c1_v2/<run>.json on origin/zach/v8-breadth-1021) |
| removal | descriptive, no committed rule (Dan, 23 Oct): the gap = lookups (BL, RL) - recalls (BR, RR) right under J-space removal, clean question, with a 95% interval from an unpaired bootstrap over bridge entities (stats.cluster_bootstrap's resampling, entities drawn with replacement within each group, 4000 draws, seed 0). Where the run's spec has gate G2 (the control removals keep >= 90% on every family and step), a failed G2 makes the cell not interpretable. The 32B, Gemma and Muse runs (and the 27B's d2_abl_read_*_v2 copies) ran without the random-dictionary control (too large next to the model on an 80 GB GPU): G2 reads the rotated control alone. Zach's pilots (the 27B's abl_rot_v1, Gemma's refit, the 122B's abl_v1) have no G2 |
