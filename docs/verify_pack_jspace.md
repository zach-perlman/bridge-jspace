## J-space rank checks (inspector)

Dan 11:45 (jobs/c3/batch53.yaml inspector_1145 item 3), verbatim: "Automatic check over every item of the conflict test and the routes test (not only the sample), at L and the bridge word, results in docs/verify_pack.md: the rank of S's bridge token (and its variants) in the readout of the J++ part, of the rest and of a random part of the same share; the share of items with it in the top 50 for each. Flag if the rest puts it in the top 50 on >= 20% of items more often than the random part does. The same for the answer words. No rule change: this is a check."

Dan 13:15 (jobs/c3/batch53.yaml answers_1315), verbatim: "Rank check: no flag (the rest 0.00-0.02 vs random 0.52; the rule flags the rest exceeding random)." Card line, verbatim: "what the lens can read about the item sits in the J++ part; the rest reads nothing (0.00-0.02); the random part reads the bridge because it keeps part of Δ itself".

The per-item panel: "Look into J-space" on every card of `make review-serve` (the state, the change, its J++ part, the rest, the random part and U at any saved token and layer; J++ and logit-lens top 30; typed and listed tokens' ranks; a token x layer heatmap; the change's 25 atoms at L; self-checks against 51.12 and x52_atoms; a free-text note per item, saved in review/marks.jsonl as kind "jspace").

As computed (scripts/review_jspace.py rank-check): the readout is the J++ lens (JLens.readout) at L; the J++ part is X0's 25-atom signed OMP over the J++ letter-token atoms, the rest = Δ minus it, the random part X0's (seed 888 + L) at the J++ part's share; rank = 1 + tokens with a strictly larger logit, a word's best token (S's bridge: its one-token spellings and symbol, then also the first pieces of split spellings; an answer: its digit and its number word). Flag (Dan 13:15: the rest exceeding random): (share in the top 50 under the rest) minus (under the random part) >= 0.20. Routes: per condition and over all. By construction the random part keeps share x Δ along Δ itself (statement_positions.random_subspace_part's docstring), so it carries whatever Δ's own direction reads as. Sources: Muse Glimmer 30B: `results/review_states/muse30_review_states`; Nemotron 3.5 Lightning: `results/review_states/nem35l_review_states`; Qwen3.5-9B: `results/review_states/qwen35_9b_review_states`; Qwen3.6-27B: `51.10's cached states (results/x51_jread, CPU; conflict test only)`. Models read from 51.10's states: the conflict test only, until their states job lands. 

**Flags: 0**.

The parts reproduce the runs': the J++ share of Δ against the run's stored share, per model and test: Muse Glimmer 30B main_swap: max |gap| 0.0000 over 200; Muse Glimmer 30B routes: max |gap| 0.0000 over 900; Nemotron 3.5 Lightning main_swap: max |gap| 0.0000 over 200; Nemotron 3.5 Lightning routes: max |gap| 0.0000 over 900; Qwen3.5-9B main_swap: max |gap| 0.0000 over 200; Qwen3.5-9B routes: max |gap| 0.0000 over 900; Qwen3.6-27B main_swap: max |gap| 0.0042 over 200.

| model | test | condition | token | n | top 50: J++ part | rest | random part | rest - random | flag | median rank: J++ / rest / random |
|---|---|---|---|---|---|---|---|---|---|---|
| Muse Glimmer 30B | main_swap | all | S's bridge (word or symbol) | 200 | 0.89 | 0.01 | 0.66 | -0.65 |  | 1 / 41590 / 6 |
| Muse Glimmer 30B | main_swap | all | S's bridge (with first pieces) | 200 | 0.93 | 0.01 | 0.66 | -0.65 |  | 1 / 24364 / 6 |
| Muse Glimmer 30B | main_swap | all | the lookup's S answer (digit or word) | 200 | 0.00 | 0.01 | 0.00 | +0.01 |  | 44122 / 42103 / 48930 |
| Muse Glimmer 30B | main_swap | all | the recall's S answer (digit or word) | 200 | 0.01 | 0.00 | 0.00 | +0.00 |  | 41441 / 40204 / 35986 |
| Muse Glimmer 30B | routes | C0 | S's bridge (word or symbol) | 300 | 0.92 | 0.01 | 0.49 | -0.48 |  | 1 / 91278 / 66 |
| Muse Glimmer 30B | routes | C0 | S's bridge (with first pieces) | 300 | 0.93 | 0.01 | 0.49 | -0.48 |  | 1 / 83240 / 66 |
| Muse Glimmer 30B | routes | C0 | the lookup's S answer (digit or word) | 300 | 0.00 | 0.00 | 0.00 | +0.00 |  | 45436 / 40880 / 44956 |
| Muse Glimmer 30B | routes | C0 | the recall's S answer (digit or word) | 300 | 0.00 | 0.00 | 0.00 | +0.00 |  | 42262 / 31760 / 46554 |
| Muse Glimmer 30B | routes | C1 | S's bridge (word or symbol) | 300 | 0.13 | 0.01 | 0.00 | +0.01 |  | 45308 / 52707 / 63628 |
| Muse Glimmer 30B | routes | C1 | S's bridge (with first pieces) | 300 | 0.13 | 0.01 | 0.00 | +0.01 |  | 35564 / 44220 / 50094 |
| Muse Glimmer 30B | routes | C1 | the lookup's S answer (digit or word) | 300 | 0.01 | 0.00 | 0.01 | -0.01 |  | 36800 / 38081 / 44317 |
| Muse Glimmer 30B | routes | C1 | the recall's S answer (digit or word) | 300 | 0.01 | 0.00 | 0.00 | -0.00 |  | 30648 / 45556 / 41365 |
| Muse Glimmer 30B | routes | C2 | S's bridge (word or symbol) | 300 | 0.92 | 0.01 | 0.46 | -0.45 |  | 1 / 94052 / 140 |
| Muse Glimmer 30B | routes | C2 | S's bridge (with first pieces) | 300 | 0.93 | 0.01 | 0.46 | -0.45 |  | 1 / 82740 / 134 |
| Muse Glimmer 30B | routes | C2 | the lookup's S answer (digit or word) | 300 | 0.00 | 0.01 | 0.00 | +0.01 |  | 42458 / 35832 / 47240 |
| Muse Glimmer 30B | routes | C2 | the recall's S answer (digit or word) | 300 | 0.00 | 0.01 | 0.00 | +0.01 |  | 41303 / 36558 / 50198 |
| Muse Glimmer 30B | routes | all | S's bridge (word or symbol) | 900 | 0.66 | 0.01 | 0.32 | -0.31 |  | 2 / 87924 / 2324 |
| Muse Glimmer 30B | routes | all | S's bridge (with first pieces) | 900 | 0.66 | 0.01 | 0.32 | -0.31 |  | 2 / 71984 / 2183 |
| Muse Glimmer 30B | routes | all | the lookup's S answer (digit or word) | 900 | 0.00 | 0.00 | 0.00 | +0.00 |  | 41608 / 38178 / 46086 |
| Muse Glimmer 30B | routes | all | the recall's S answer (digit or word) | 900 | 0.00 | 0.00 | 0.00 | +0.00 |  | 39752 / 37590 / 47102 |
| Nemotron 3.5 Lightning | main_swap | all | S's bridge (word or symbol) | 200 | 0.93 | 0.06 | 0.65 | -0.59 |  | 1 / 7858 / 10 |
| Nemotron 3.5 Lightning | main_swap | all | S's bridge (with first pieces) | 200 | 0.94 | 0.07 | 0.67 | -0.60 |  | 1 / 4656 / 8 |
| Nemotron 3.5 Lightning | main_swap | all | the lookup's S answer (digit or word) | 200 | 0.00 | 0.00 | 0.01 | -0.01 |  | 31639 / 24055 / 12385 |
| Nemotron 3.5 Lightning | main_swap | all | the recall's S answer (digit or word) | 200 | 0.01 | 0.01 | 0.04 | -0.02 |  | 19497 / 17187 / 10481 |
| Nemotron 3.5 Lightning | routes | C0 | S's bridge (word or symbol) | 300 | 0.87 | 0.14 | 0.45 | -0.31 |  | 2 / 9322 / 82 |
| Nemotron 3.5 Lightning | routes | C0 | S's bridge (with first pieces) | 300 | 0.87 | 0.14 | 0.47 | -0.33 |  | 2 / 7044 / 66 |
| Nemotron 3.5 Lightning | routes | C0 | the lookup's S answer (digit or word) | 300 | 0.01 | 0.00 | 0.01 | -0.00 |  | 9578 / 25860 / 29095 |
| Nemotron 3.5 Lightning | routes | C0 | the recall's S answer (digit or word) | 300 | 0.00 | 0.00 | 0.01 | -0.01 |  | 8223 / 25470 / 18063 |
| Nemotron 3.5 Lightning | routes | C1 | S's bridge (word or symbol) | 300 | 0.01 | 0.01 | 0.00 | +0.01 |  | 54071 / 45854 / 45660 |
| Nemotron 3.5 Lightning | routes | C1 | S's bridge (with first pieces) | 300 | 0.01 | 0.01 | 0.00 | +0.01 |  | 34044 / 23644 / 28595 |
| Nemotron 3.5 Lightning | routes | C1 | the lookup's S answer (digit or word) | 300 | 0.05 | 0.01 | 0.04 | -0.03 |  | 36340 / 29812 / 23722 |
| Nemotron 3.5 Lightning | routes | C1 | the recall's S answer (digit or word) | 300 | 0.04 | 0.00 | 0.03 | -0.03 |  | 38558 / 27734 / 37058 |
| Nemotron 3.5 Lightning | routes | C2 | S's bridge (word or symbol) | 300 | 0.86 | 0.13 | 0.46 | -0.33 |  | 1 / 9362 / 78 |
| Nemotron 3.5 Lightning | routes | C2 | S's bridge (with first pieces) | 300 | 0.87 | 0.13 | 0.48 | -0.35 |  | 1 / 5506 / 65 |
| Nemotron 3.5 Lightning | routes | C2 | the lookup's S answer (digit or word) | 300 | 0.00 | 0.00 | 0.01 | -0.01 |  | 7572 / 29536 / 21068 |
| Nemotron 3.5 Lightning | routes | C2 | the recall's S answer (digit or word) | 300 | 0.00 | 0.00 | 0.03 | -0.03 |  | 6197 / 23824 / 24084 |
| Nemotron 3.5 Lightning | routes | all | S's bridge (word or symbol) | 900 | 0.58 | 0.09 | 0.31 | -0.21 |  | 6 / 17558 / 1006 |
| Nemotron 3.5 Lightning | routes | all | S's bridge (with first pieces) | 900 | 0.58 | 0.09 | 0.31 | -0.22 |  | 6 / 10840 / 742 |
| Nemotron 3.5 Lightning | routes | all | the lookup's S answer (digit or word) | 900 | 0.02 | 0.00 | 0.02 | -0.02 |  | 12294 / 28917 / 23992 |
| Nemotron 3.5 Lightning | routes | all | the recall's S answer (digit or word) | 900 | 0.02 | 0.00 | 0.02 | -0.02 |  | 10423 / 25530 / 25548 |
| Qwen3.5-9B | main_swap | all | S's bridge (word or symbol) | 200 | 0.81 | 0.00 | 0.52 | -0.52 |  | 2 / 15326 / 44 |
| Qwen3.5-9B | main_swap | all | S's bridge (with first pieces) | 200 | 0.82 | 0.01 | 0.55 | -0.55 |  | 2 / 13198 / 37 |
| Qwen3.5-9B | main_swap | all | the lookup's S answer (digit or word) | 200 | 0.00 | 0.00 | 0.00 | +0.00 |  | 27711 / 50404 / 38898 |
| Qwen3.5-9B | main_swap | all | the recall's S answer (digit or word) | 200 | 0.01 | 0.00 | 0.01 | -0.01 |  | 21213 / 25839 / 19327 |
| Qwen3.5-9B | routes | C0 | S's bridge (word or symbol) | 300 | 0.67 | 0.01 | 0.39 | -0.37 |  | 7 / 26405 / 156 |
| Qwen3.5-9B | routes | C0 | S's bridge (with first pieces) | 300 | 0.69 | 0.01 | 0.39 | -0.38 |  | 6 / 18989 / 156 |
| Qwen3.5-9B | routes | C0 | the lookup's S answer (digit or word) | 300 | 0.02 | 0.00 | 0.01 | -0.00 |  | 17077 / 28882 / 25652 |
| Qwen3.5-9B | routes | C0 | the recall's S answer (digit or word) | 300 | 0.02 | 0.00 | 0.00 | +0.00 |  | 20181 / 36710 / 33691 |
| Qwen3.5-9B | routes | C1 | S's bridge (word or symbol) | 300 | 0.05 | 0.00 | 0.00 | -0.00 |  | 43426 / 80644 / 64058 |
| Qwen3.5-9B | routes | C1 | S's bridge (with first pieces) | 300 | 0.05 | 0.00 | 0.00 | -0.00 |  | 14286 / 53150 / 35604 |
| Qwen3.5-9B | routes | C1 | the lookup's S answer (digit or word) | 300 | 0.03 | 0.01 | 0.04 | -0.02 |  | 6904 / 28189 / 36048 |
| Qwen3.5-9B | routes | C1 | the recall's S answer (digit or word) | 300 | 0.01 | 0.01 | 0.04 | -0.03 |  | 8072 / 32846 / 33281 |
| Qwen3.5-9B | routes | C2 | S's bridge (word or symbol) | 300 | 0.70 | 0.01 | 0.38 | -0.37 |  | 7 / 26434 / 192 |
| Qwen3.5-9B | routes | C2 | S's bridge (with first pieces) | 300 | 0.70 | 0.01 | 0.38 | -0.37 |  | 7 / 20586 / 192 |
| Qwen3.5-9B | routes | C2 | the lookup's S answer (digit or word) | 300 | 0.00 | 0.00 | 0.00 | +0.00 |  | 20314 / 28502 / 26870 |
| Qwen3.5-9B | routes | C2 | the recall's S answer (digit or word) | 300 | 0.02 | 0.00 | 0.01 | -0.01 |  | 19379 / 32550 / 40476 |
| Qwen3.5-9B | routes | all | S's bridge (word or symbol) | 900 | 0.47 | 0.01 | 0.26 | -0.25 |  | 66 / 38218 / 2680 |
| Qwen3.5-9B | routes | all | S's bridge (with first pieces) | 900 | 0.48 | 0.01 | 0.26 | -0.25 |  | 58 / 26460 / 1953 |
| Qwen3.5-9B | routes | all | the lookup's S answer (digit or word) | 900 | 0.02 | 0.01 | 0.02 | -0.01 |  | 14788 / 28458 / 29210 |
| Qwen3.5-9B | routes | all | the recall's S answer (digit or word) | 900 | 0.02 | 0.00 | 0.02 | -0.01 |  | 15521 / 33771 / 35538 |
| Qwen3.6-27B | main_swap | all | S's bridge (word or symbol) | 200 | 0.81 | 0.02 | 0.53 | -0.51 |  | 2 / 20384 / 42 |
| Qwen3.6-27B | main_swap | all | S's bridge (with first pieces) | 200 | 0.82 | 0.03 | 0.54 | -0.51 |  | 2 / 16758 / 41 |
| Qwen3.6-27B | main_swap | all | the lookup's S answer (digit or word) | 200 | 0.01 | 0.00 | 0.00 | +0.00 |  | 46339 / 52854 / 35004 |
| Qwen3.6-27B | main_swap | all | the recall's S answer (digit or word) | 200 | 0.01 | 0.01 | 0.01 | +0.00 |  | 18502 / 28734 / 18362 |
