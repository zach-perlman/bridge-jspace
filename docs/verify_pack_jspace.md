## J-space rank checks (inspector)

Dan 11:45 (jobs/c3/batch53.yaml inspector_1145 item 3), verbatim: "Automatic check over every item of the conflict test and the routes test (not only the sample), at L and the bridge word, results in docs/verify_pack.md: the rank of S's bridge token (and its variants) in the readout of the J++ part, of the rest and of a random part of the same share; the share of items with it in the top 50 for each. Flag if the rest puts it in the top 50 on >= 20% of items more often than the random part does. The same for the answer words. No rule change: this is a check."

The per-item panel: "Look into J-space" on every card of `make review-serve` (the state, the change, its J++ part, the rest, the random part and U at any saved token and layer; J++ and logit-lens top 30; typed and listed tokens' ranks; a token x layer heatmap; the change's 25 atoms at L; self-checks against 51.12 and x52_atoms; a free-text note per item, saved in review/marks.jsonl as kind "jspace").

As computed (scripts/review_jspace.py rank-check): the readout is the J++ lens (JLens.readout) at L; the J++ part is X0's 25-atom signed OMP over the J++ letter-token atoms, the rest = Δ minus it, the random part X0's (seed 888 + L) at the J++ part's share; rank = 1 + tokens with a strictly larger logit, a word's best token (S's bridge: its one-token spellings and symbol, then also the first pieces of split spellings; an answer: its digit and its number word). Flag read as: (share in the top 50 under the rest) minus (under the random part) >= 0.20 (the agent's reading of the sentence; to confirm). Beside it, column 'alt': the other reading, the rest's share >= 0.20 and above the random part's. Routes: per condition and over all. By construction the random part keeps share x Δ along Δ itself (statement_positions.random_subspace_part's docstring), so it carries whatever Δ's own direction reads as. Sources: Qwen3.5-9B: `51.10's cached states (results/x51_jread, CPU; conflict test only)`; Qwen3.6-27B: `51.10's cached states (results/x51_jread, CPU; conflict test only)`. Models read from 51.10's states: the conflict test only, until their states job lands. 

**Flags: 0**. Under the other reading: 0.

The parts reproduce the runs': the J++ share of Δ against the run's stored share, per model and test: Qwen3.5-9B main_swap: max |gap| 0.0000 over 200; Qwen3.6-27B main_swap: max |gap| 0.0042 over 200.

| model | test | condition | token | n | top 50: J++ part | rest | random part | rest - random | flag | alt | median rank: J++ / rest / random |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | main_swap | all | S's bridge (word or symbol) | 200 | 0.81 | 0.00 | 0.52 | -0.52 |  |  | 2 / 15326 / 44 |
| Qwen3.5-9B | main_swap | all | S's bridge (with first pieces) | 200 | 0.82 | 0.01 | 0.55 | -0.55 |  |  | 2 / 13198 / 37 |
| Qwen3.5-9B | main_swap | all | the lookup's S answer (digit or word) | 200 | 0.00 | 0.00 | 0.00 | +0.00 |  |  | 27712 / 50404 / 38897 |
| Qwen3.5-9B | main_swap | all | the recall's S answer (digit or word) | 200 | 0.01 | 0.00 | 0.01 | -0.01 |  |  | 21213 / 25839 / 19328 |
| Qwen3.6-27B | main_swap | all | S's bridge (word or symbol) | 200 | 0.81 | 0.02 | 0.53 | -0.51 |  |  | 2 / 20384 / 42 |
| Qwen3.6-27B | main_swap | all | S's bridge (with first pieces) | 200 | 0.82 | 0.03 | 0.54 | -0.51 |  |  | 2 / 16758 / 41 |
| Qwen3.6-27B | main_swap | all | the lookup's S answer (digit or word) | 200 | 0.01 | 0.00 | 0.00 | +0.00 |  |  | 46339 / 52854 / 35004 |
| Qwen3.6-27B | main_swap | all | the recall's S answer (digit or word) | 200 | 0.01 | 0.01 | 0.01 | +0.00 |  |  | 18502 / 28734 / 18362 |
