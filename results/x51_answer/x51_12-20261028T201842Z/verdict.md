# 51.12: is it the bridge or the answer that moves through the lens? (r2, amendment 20:20; UNVERIFIED)

Batch 51, test 51.12 (jobs/c3/batch51.yaml addendum_4 and addendum_4_amendment; Q51.12, Dan: entity). Cluster bootstrap over the bridge entity (10000, seed 0), paired across arms.

Rule (fixed in advance): Per model, per reader: "the lens effect is the entity": arm 2 keeps >= 0.7 of arm 1's extra loss and arm 3 costs <= 0.10 beyond random. "The lens effect is the answer": arm 2 falls to <= 0.3 of arm 1 and arm 3 alone costs >= 0.5 of arm 1. Else: mixed, report both shares. Amendment (Dan 20:20): before the arms, the lens readout check at the bridge word; the verdict says which case held, either 'the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)' or the arm-based entity / answer / mixed (never 'void by construction'). Z2: arm 3 is read against its controls (a same-size random part and a frequency-matched part), not against zero.

As computed: Extra loss of arm k = X0's excess = (S_rand_k - S_k) / S_whole per reader over the source run's items (switch: the set's own read; 47.3's lookup: follows the change, identity / position / value). e1, e2, e3 = arms 1, 2, 3; arm 4 (no_A_rand) is arm 3's random twin. 'Keeps >= 0.7 of arm 1' = e2 / e1 >= 0.7; 'costs <= 0.10 beyond random' = e3 <= 0.10; 'falls to <= 0.3 of arm 1' = e2 / e1 <= 0.3; 'costs >= 0.5 of arm 1' = e3 / e1 >= 0.5. Z2: arm 3 against both its controls, e3 (vs no_A_rand) and e3f = (S_noF - S_noA) / S_whole (vs no_F); 'entity' needs max(e3, e3f) <= 0.10, 'answer' needs min(e3, e3f) >= 0.5 e1 (a label holds only against both controls). Point estimates decide (EPS 1e-9); e1 <= 0 or undefined (no switch under the whole change) -> can't tell; CIs from X0's cluster bootstrap over the bridge entity (10,000, seed 0), paired across arms (ratios on the same draws). Readout case first: per reader the rank (1 + tokens with a strictly higher lens logit, full vocabulary) of its own answer word (best of its A-style variant tokens) at the edited token at L, O's answer on O's state and S's on S's (z2: the reader's own state; e1 / cue: the lookup's, shared through the edited token); an item is 'not read' when it ranks > 50 on both; >= 90 % of items not read -> 'the answer word is not read at the bridge word', the arms reported beside; else the arm-based label. A: J++ unit atoms of letter tokens (the OMP dictionary); e1 / cue the answers' number words (suite_v1.WORDS: 6 -> 'six'), each of its variants (as is, leading space, capitalised, both) kept where it is one letter token; z2 the first token of each answer word and variant (where the tokenizer splits the full word, its first token only). Frequency-matched control F (z2): per atom a of A, the letter token f with |log((id_f + 1) / (id_a + 1))| <= log 2 (a BPE id is its merge rank, earlier = more frequent in the tokenizer's training corpus; the factor doubles until a candidate exists) and the closest log J++ readout norm ||(g * W_U[t]) J_L|| (ties: lower id); unrelated = its key (decode, stripped, lower-cased) equals no key of the set's answer words, A tokens, bridge entities' tokens / names or edited tokens, and (keys of >= 3 characters) neither contains nor is contained in one; never twice in one item. no_F = Δ - P_F Δ, P_F the projector on span(F). Decisive cells for Q51.12: Z2 both readers; E1 the recall (the lookup beside); 47.3 both readers. Projected out: (I - P_A) P_J Δ, P_A the orthogonal projector on the span of the item's answer atoms (the J++ part minus its component along span(A)).

Which case held, per cell: first the readout check (the reader's own answer word at the edited token at L; 'not read' = rank > 50 on both O and S), then the arms.

| set | model | reader | n | answer word top-50 O | top-50 S | not read | case | e1 (no J++) | e2 (no J++, A kept) | e3 (no A vs random) | e3f (no A vs freq.) | e2/e1 | e3/e1 | verdict | decisive |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| z2 | qwen3.5-9b | lookup | 158 | 0.53 [0.43, 0.62] | 0.49 [0.40, 0.58] | 0.22 [0.16, 0.29] | arms | 0.56 [0.45, 0.67] | 0.15 [0.06, 0.26] | 0.34 [0.22, 0.45] | 0.37 [0.24, 0.51] | 0.27 [0.11, 0.45] | 0.61 [0.37, 0.91] | **the lens effect is the answer** | yes |
| z2 | qwen3.5-9b | recall | 158 | 0.53 [0.43, 0.63] | 0.53 [0.44, 0.62] | 0.20 [0.13, 0.27] | arms | 0.70 [0.57, 0.82] | 0.23 [0.13, 0.33] | 0.55 [0.39, 0.70] | 0.53 [0.38, 0.67] | 0.32 [0.19, 0.47] | 0.78 [0.55, 1.07] | **mixed** | yes |
| z2 | qwen3.6-27b | lookup | 166 | 0.58 [0.48, 0.68] | 0.62 [0.53, 0.70] | 0.21 [0.14, 0.29] | arms | 0.67 [0.48, 0.84] | 0.33 [0.19, 0.50] | 0.50 [0.33, 0.66] | 0.42 [0.25, 0.58] | 0.50 [0.31, 0.70] | 0.75 [0.44, 1.22] | **mixed** | yes |
| z2 | qwen3.6-27b | recall | 166 | 0.57 [0.47, 0.66] | 0.62 [0.54, 0.70] | 0.19 [0.13, 0.27] | arms | 0.61 [0.44, 0.78] | 0.03 [-0.12, 0.18] | 0.42 [0.24, 0.60] | 0.45 [0.27, 0.63] | 0.05 [-0.21, 0.28] | 0.68 [0.35, 1.18] | **the lens effect is the answer** | yes |
| e1 | qwen3.5-9b | lookup | 200 | 0.14 [0.08, 0.20] | 0.10 [0.06, 0.13] | 0.77 [0.70, 0.83] | arms | -0.05 [-0.09, 0.00] | -0.02 [-0.07, 0.04] | -0.04 [-0.08, -0.01] | - | - | - | **can't tell (arm 1 has no extra loss beyond random)** | beside |
| e1 | qwen3.5-9b | recall | 200 | 0.28 [0.16, 0.40] | 0.27 [0.20, 0.33] | 0.56 [0.47, 0.66] | arms | 0.50 [0.41, 0.57] | 0.47 [0.39, 0.55] | 0.00 [0.00, 0.00] | - | 0.95 [0.90, 0.99] | 0.00 [0.00, 0.00] | **the lens effect is the entity** | yes |
| e1 | qwen3.6-27b | lookup | 200 | 0.07 [0.03, 0.11] | 0.04 [0.02, 0.06] | 0.90 [0.85, 0.93] | arms | 0.14 [0.08, 0.20] | 0.12 [0.06, 0.18] | -0.01 [-0.04, 0.00] | - | 0.83 [0.50, 1.18] | -0.08 [-0.36, 0.00] | **the lens effect is the entity** | beside |
| e1 | qwen3.6-27b | recall | 200 | 0.12 [0.04, 0.19] | 0.12 [0.08, 0.15] | 0.79 [0.72, 0.86] | arms | 0.74 [0.66, 0.80] | 0.69 [0.59, 0.77] | 0.03 [0.01, 0.05] | - | 0.93 [0.85, 0.99] | 0.04 [0.01, 0.07] | **the lens effect is the entity** | yes |
| e1 | muse-glimmer-30b | lookup | 200 | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.03] | 0.99 [0.97, 1.00] | not_read | -0.10 [-0.15, -0.04] | -0.07 [-0.12, -0.02] | -0.03 [-0.07, 0.00] | - | - | - | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) (99% of 200 items; arms beside: can't tell (arm 1 has no extra loss beyond random))** | beside |
| e1 | muse-glimmer-30b | recall | 200 | 0.01 [0.00, 0.02] | 0.01 [0.00, 0.02] | 0.99 [0.98, 1.00] | not_read | 0.76 [0.62, 0.88] | 0.71 [0.56, 0.84] | -0.01 [-0.05, 0.03] | - | 0.93 [0.85, 1.00] | -0.01 [-0.07, 0.04] | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) (100% of 200 items; arms beside: the lens effect is the entity)** | yes |
| cue | qwen3.5-9b | lookup | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | not_read | 0.07 [0.01, 0.16] | 0.04 [-0.01, 0.11] | 0.00 [-0.01, 0.01] | - | 0.50 [-0.71, 0.81] | 0.00 [-0.33, 0.20] | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) (100% of 300 items; arms beside: mixed)** | yes |
| cue | qwen3.5-9b | recall | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | not_read | 0.39 [0.31, 0.47] | 0.39 [0.31, 0.47] | 0.01 [0.00, 0.03] | - | 1.00 [0.95, 1.07] | 0.03 [0.00, 0.07] | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) (100% of 300 items; arms beside: the lens effect is the entity)** | yes |
| cue | qwen3.6-27b | lookup | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | not_read | 0.39 [0.32, 0.45] | 0.42 [0.36, 0.48] | 0.00 [-0.03, 0.04] | - | 1.08 [1.00, 1.21] | 0.01 [-0.07, 0.10] | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) (100% of 300 items; arms beside: the lens effect is the entity)** | yes |
| cue | qwen3.6-27b | recall | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | not_read | 0.48 [0.37, 0.60] | 0.46 [0.36, 0.57] | 0.05 [0.02, 0.09] | - | 0.97 [0.92, 1.03] | 0.11 [0.04, 0.19] | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) (100% of 300 items; arms beside: the lens effect is the entity)** | yes |

## z2 on qwen3.5-9b (qwen35_9b_x51_12_z2_r2, L12, source qwen35_9b_x50_z2)

Source gate: {'pass': True, 'chosen': 158, 'org_read_accuracy': {'K': 0.9606741573033708, 'M': 0.949438202247191}, 'gate': 0.8}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 158, no letter token for the word 0): top-10 O 0.23 [0.15, 0.31], S 0.23 [0.16, 0.29], either 0.40 [0.32, 0.48]; top-50 O 0.53 [0.43, 0.62], S 0.49 [0.40, 0.58], either 0.78 [0.71, 0.84]; median rank O 46.5, S 51.5 vs the bridge entity's O 177.0, S 221.0; above the bridge O 0.49 [0.39, 0.60], S 0.56 [0.47, 0.64]; not read 0.22 [0.16, 0.29] -> case arms
- recall (state: recall's prompts; n 158, no letter token for the word 0): top-10 O 0.25 [0.16, 0.34], S 0.27 [0.20, 0.34], either 0.44 [0.35, 0.52]; top-50 O 0.53 [0.43, 0.63], S 0.53 [0.44, 0.62], either 0.80 [0.73, 0.87]; median rank O 43.5, S 41.0 vs the bridge entity's O 181.0, S 251.0; above the bridge O 0.51 [0.40, 0.62], S 0.57 [0.48, 0.66]; not read 0.20 [0.13, 0.27] -> case arms

| arm | lookup | recall |
|---|---|---|
| none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| whole | 0.37 [0.28, 0.46] | 0.34 [0.25, 0.42] |
| no_jpp | 0.06 [0.03, 0.10] | 0.04 [0.01, 0.08] |
| no_jpp_rand | 0.27 [0.20, 0.35] | 0.28 [0.20, 0.37] |
| no_jpp_A | 0.22 [0.15, 0.29] | 0.20 [0.13, 0.28] |
| no_jpp_A_rand | 0.28 [0.20, 0.36] | 0.28 [0.20, 0.37] |
| no_A | 0.24 [0.17, 0.31] | 0.16 [0.10, 0.22] |
| no_A_rand | 0.37 [0.28, 0.46] | 0.34 [0.25, 0.43] |
| no_F | 0.38 [0.29, 0.47] | 0.34 [0.25, 0.42] |
- lookup: X0's validity bar True; whole 59 of 158; arm rule: the lens effect is the answer; e3f/e1 0.67 [0.40, 1.03]
- recall: X0's validity bar True; whole 53 of 158; arm rule: mixed; e3f/e1 0.76 [0.53, 1.03]

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 158, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 158}}; rank {'n': 158, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 158}}; answer atoms among the 25: {'n': 158, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.032, 'hist': {0: 153, 1: 5}} (5 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.19457, 'share_jpp_A': 0.18647, 'share_A': 0.00798, 'share_A_in_jpp': 0.00531, 'share_F': 0.00183}; frequency match {'pairs': 632, 'median_id_ratio': 1.1078, 'median_norm_ratio': 1.0, 'widened': 0}
- Δ from the recall's prompts: |A| tokens {'n': 158, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 158}}; rank {'n': 158, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 158}}; answer atoms among the 25: {'n': 158, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.038, 'hist': {0: 152, 1: 6}} (6 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.19236, 'share_jpp_A': 0.18503, 'share_A': 0.00808, 'share_A_in_jpp': 0.00605, 'share_F': 0.0018}; frequency match {'pairs': 632, 'median_id_ratio': 1.1078, 'median_norm_ratio': 1.0, 'widened': 0}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 158 | 0.03 [0.01, 0.07] | 0.13 [0.06, 0.21] | 0.84 [0.75, 0.92] | lookup_answer: 0.03 [0.01, 0.07]; recall_answer: 0.03 [0.01, 0.07] | 0.00 [0.00, 0.00] | - |
| lookup's prompt, S | 158 | 0.04 [0.01, 0.08] | 0.13 [0.08, 0.18] | 0.84 [0.78, 0.89] | lookup_answer: 0.04 [0.01, 0.08]; recall_answer: 0.04 [0.01, 0.08] | 0.00 [0.00, 0.00] | - |
| recall's prompt, O | 158 | 0.04 [0.01, 0.09] | 0.13 [0.06, 0.22] | 0.82 [0.74, 0.90] | lookup_answer: 0.04 [0.01, 0.09]; recall_answer: 0.04 [0.01, 0.09] | 0.00 [0.00, 0.00] | - |
| recall's prompt, S | 158 | 0.03 [0.00, 0.06] | 0.13 [0.08, 0.18] | 0.85 [0.79, 0.90] | lookup_answer: 0.03 [0.00, 0.06]; recall_answer: 0.03 [0.00, 0.06] | 0.00 [0.00, 0.00] | - |

Arm 1 against the stored run, item by item (agreement.json):

- lookup: none 158/158 agree (rerun 0, stored 0); whole 158/158 agree (rerun 59, stored 59); no_jpp 156/158 agree (rerun 10, stored 12); no_jpp_rand 157/158 agree (rerun 43, stored 44); arm 1's extra loss rerun 0.5593220338983051 vs stored 0.5423728813559321
- recall: none 158/158 agree (rerun 0, stored 0); whole 158/158 agree (rerun 53, stored 53); no_jpp 158/158 agree (rerun 7, stored 7); no_jpp_rand 158/158 agree (rerun 44, stored 44); arm 1's extra loss rerun 0.6981132075471697 vs stored 0.6981132075471697

## z2 on qwen3.6-27b (x51_12_z2_27b_r2, L32, source x50_z2_27b)

Source gate: {'pass': True, 'chosen': 166, 'org_read_accuracy': {'K': 0.9900497512437811, 'M': 0.9303482587064676}, 'gate': 0.8}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 166, no letter token for the word 0): top-10 O 0.32 [0.23, 0.41], S 0.39 [0.31, 0.47], either 0.58 [0.49, 0.66]; top-50 O 0.58 [0.48, 0.68], S 0.62 [0.53, 0.70], either 0.79 [0.71, 0.86]; median rank O 32.0, S 22.5 vs the bridge entity's O 24.5, S 36.5; above the bridge O 0.47 [0.37, 0.57], S 0.50 [0.42, 0.58]; not read 0.21 [0.14, 0.29] -> case arms
- recall (state: recall's prompts; n 166, no letter token for the word 0): top-10 O 0.36 [0.27, 0.45], S 0.43 [0.35, 0.52], either 0.62 [0.53, 0.71]; top-50 O 0.57 [0.47, 0.66], S 0.62 [0.54, 0.70], either 0.81 [0.73, 0.87]; median rank O 28.5, S 17.5 vs the bridge entity's O 24.5, S 33.0; above the bridge O 0.46 [0.36, 0.56], S 0.50 [0.42, 0.58]; not read 0.19 [0.13, 0.27] -> case arms

| arm | lookup | recall |
|---|---|---|
| none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| whole | 0.22 [0.15, 0.29] | 0.19 [0.12, 0.25] |
| no_jpp | 0.02 [0.00, 0.04] | 0.00 [0.00, 0.00] |
| no_jpp_rand | 0.16 [0.10, 0.23] | 0.11 [0.07, 0.17] |
| no_jpp_A | 0.09 [0.05, 0.14] | 0.11 [0.06, 0.16] |
| no_jpp_A_rand | 0.16 [0.10, 0.23] | 0.11 [0.07, 0.17] |
| no_A | 0.10 [0.06, 0.15] | 0.10 [0.06, 0.15] |
| no_A_rand | 0.21 [0.14, 0.28] | 0.18 [0.12, 0.25] |
| no_F | 0.19 [0.12, 0.26] | 0.19 [0.12, 0.26] |
- lookup: X0's validity bar False; whole 36 of 166; arm rule: mixed; e3f/e1 0.63 [0.35, 1.05]
- recall: X0's validity bar False; whole 31 of 166; arm rule: the lens effect is the answer; e3f/e1 0.74 [0.41, 1.19]

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 166, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 166}}; rank {'n': 166, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 166}}; answer atoms among the 25: {'n': 166, 'min': 0, 'median': 0.0, 'max': 0, 'mean': 0.0, 'hist': {0: 166}} (0 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.16022, 'share_jpp_A': 0.15303, 'share_A': 0.00856, 'share_A_in_jpp': 0.00701, 'share_F': 0.00231}; frequency match {'pairs': 664, 'median_id_ratio': 1.3378, 'median_norm_ratio': 1.0, 'widened': 0}
- Δ from the recall's prompts: |A| tokens {'n': 166, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 166}}; rank {'n': 166, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 166}}; answer atoms among the 25: {'n': 166, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.012, 'hist': {0: 164, 1: 2}} (2 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.1563, 'share_jpp_A': 0.14929, 'share_A': 0.00854, 'share_A_in_jpp': 0.00733, 'share_F': 0.00241}; frequency match {'pairs': 664, 'median_id_ratio': 1.3378, 'median_norm_ratio': 1.0, 'widened': 0}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 166 | 0.09 [0.04, 0.14] | 0.14 [0.08, 0.22] | 0.77 [0.68, 0.84] | lookup_answer: 0.09 [0.04, 0.14]; recall_answer: 0.09 [0.04, 0.14] | 0.00 [0.00, 0.00] | - |
| lookup's prompt, S | 166 | 0.10 [0.05, 0.15] | 0.14 [0.09, 0.20] | 0.76 [0.69, 0.83] | lookup_answer: 0.10 [0.05, 0.15]; recall_answer: 0.10 [0.05, 0.15] | 0.00 [0.00, 0.00] | - |
| recall's prompt, O | 166 | 0.08 [0.04, 0.14] | 0.14 [0.07, 0.21] | 0.78 [0.69, 0.85] | lookup_answer: 0.08 [0.04, 0.14]; recall_answer: 0.08 [0.04, 0.14] | 0.00 [0.00, 0.00] | - |
| recall's prompt, S | 166 | 0.11 [0.06, 0.17] | 0.16 [0.10, 0.22] | 0.73 [0.66, 0.80] | lookup_answer: 0.11 [0.06, 0.17]; recall_answer: 0.11 [0.06, 0.17] | 0.00 [0.00, 0.00] | - |

Arm 1 against the stored run, item by item (agreement.json):

- lookup: none 166/166 agree (rerun 0, stored 0); whole 166/166 agree (rerun 36, stored 36); no_jpp 166/166 agree (rerun 3, stored 3); no_jpp_rand 165/166 agree (rerun 27, stored 28); arm 1's extra loss rerun 0.6666666666666666 vs stored 0.6944444444444443
- recall: none 166/166 agree (rerun 0, stored 0); whole 160/166 agree (rerun 31, stored 33); no_jpp 166/166 agree (rerun 0, stored 0); no_jpp_rand 166/166 agree (rerun 19, stored 19); arm 1's extra loss rerun 0.6129032258064516 vs stored 0.5757575757575757

## e1 on qwen3.5-9b (qwen35_9b_x51_12_e1_r2, L12, source qwen35_9b_x0_necessity)

Source gate: {'pass': True, 'chosen': 200, 'org_read_accuracy': {'PP': 0.95, 'PM': 0.8683}, 'gate': 0.8, 'eligible': 408}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 200, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.14 [0.08, 0.20], S 0.10 [0.06, 0.13], either 0.23 [0.17, 0.30]; median rank O 238.0, S 207.5 vs the bridge entity's O 2.5, S 4.0; above the bridge O 0.07 [0.03, 0.12], S 0.05 [0.02, 0.09]; not read 0.77 [0.70, 0.83] -> case arms
- recall (state: lookup's prompts; n 200, no letter token for the word 0): top-10 O 0.01 [0.00, 0.03], S 0.00 [0.00, 0.00], either 0.01 [0.00, 0.03]; top-50 O 0.28 [0.16, 0.40], S 0.27 [0.20, 0.33], either 0.43 [0.34, 0.53]; median rank O 143.5, S 132.0 vs the bridge entity's O 2.5, S 4.0; above the bridge O 0.12 [0.05, 0.19], S 0.07 [0.03, 0.11]; not read 0.56 [0.47, 0.66] -> case arms

| arm | lookup | recall |
|---|---|---|
| none | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.00] |
| whole | 0.53 [0.45, 0.62] | 0.98 [0.97, 1.00] |
| no_jpp | 0.41 [0.34, 0.52] | 0.46 [0.38, 0.55] |
| no_jpp_rand | 0.39 [0.31, 0.49] | 0.95 [0.92, 0.98] |
| no_jpp_A | 0.41 [0.33, 0.51] | 0.49 [0.41, 0.58] |
| no_jpp_A_rand | 0.40 [0.32, 0.50] | 0.95 [0.93, 0.98] |
| no_A | 0.53 [0.45, 0.62] | 0.98 [0.97, 1.00] |
| no_A_rand | 0.51 [0.43, 0.61] | 0.98 [0.97, 1.00] |
- lookup: X0's validity bar True; whole 106 of 200; arm rule: can't tell (arm 1 has no extra loss beyond random); e3f/e1 -
- recall: X0's validity bar True; whole 197 of 200; arm rule: the lens effect is the entity; e3f/e1 -

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.9, 'hist': {8: 2, 12: 51, 16: 147}}; rank {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.9, 'hist': {8: 2, 12: 51, 16: 147}}; answer atoms among the 25: {'n': 200, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.005, 'hist': {0: 199, 1: 1}} (1 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.23344, 'share_jpp_A': 0.22637, 'share_A': 0.01163, 'share_A_in_jpp': 0.00556}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 200 | 0.00 [0.00, 0.00] | 0.41 [0.32, 0.50] | 0.58 [0.50, 0.68] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.34 [0.19, 0.48]; lookup: 0.08 [0.05, 0.11] |
| lookup's prompt, S | 200 | 0.00 [0.00, 0.00] | 0.36 [0.27, 0.45] | 0.64 [0.55, 0.73] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.28 [0.19, 0.39]; lookup: 0.10 [0.05, 0.14] |

Arm 1 against the stored run, item by item (agreement.json):

- recall: none 200/200 agree (rerun 0, stored 0); whole 200/200 agree (rerun 197, stored 197); no_jpp 200/200 agree (rerun 92, stored 92); no_jpp_rand 200/200 agree (rerun 190, stored 190); arm 1's extra loss rerun 0.4974619289340101 vs stored 0.4974619289340101
- lookup: none 200/200 agree (rerun 1, stored 1); whole 199/200 agree (rerun 106, stored 105); no_jpp 199/200 agree (rerun 83, stored 82); no_jpp_rand 199/200 agree (rerun 78, stored 79); arm 1's extra loss rerun -0.04716981132075465 vs stored -0.02857142857142849

## e1 on qwen3.6-27b (x51_12_e1_27b_r2, L32, source x0_necessity_27b_chat)

Source gate: {'pass': True, 'chosen': 200, 'org_read_accuracy': {'PP': 0.9967, 'PM': 0.9767}, 'gate': 0.8, 'eligible': 569}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 200, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.07 [0.03, 0.11], S 0.04 [0.02, 0.06], either 0.10 [0.07, 0.15]; median rank O 864.5, S 762.0 vs the bridge entity's O 2.0, S 3.0; above the bridge O 0.04 [0.01, 0.08], S 0.01 [0.00, 0.03]; not read 0.90 [0.85, 0.93] -> case arms
- recall (state: lookup's prompts; n 200, no letter token for the word 0): top-10 O 0.01 [0.00, 0.02], S 0.00 [0.00, 0.00], either 0.01 [0.00, 0.02]; top-50 O 0.12 [0.04, 0.19], S 0.12 [0.08, 0.15], either 0.21 [0.14, 0.28]; median rank O 613.5, S 505.0 vs the bridge entity's O 2.0, S 3.0; above the bridge O 0.01 [0.00, 0.03], S 0.01 [0.00, 0.02]; not read 0.79 [0.72, 0.86] -> case arms

| arm | lookup | recall |
|---|---|---|
| none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| whole | 0.43 [0.37, 0.50] | 0.75 [0.68, 0.81] |
| no_jpp | 0.35 [0.29, 0.42] | 0.17 [0.12, 0.25] |
| no_jpp_rand | 0.41 [0.35, 0.48] | 0.73 [0.67, 0.79] |
| no_jpp_A | 0.36 [0.30, 0.43] | 0.22 [0.15, 0.30] |
| no_jpp_A_rand | 0.41 [0.35, 0.48] | 0.73 [0.68, 0.79] |
| no_A | 0.43 [0.37, 0.50] | 0.73 [0.66, 0.79] |
| no_A_rand | 0.42 [0.36, 0.49] | 0.75 [0.68, 0.81] |
- lookup: X0's validity bar True; whole 86 of 200; arm rule: the lens effect is the entity; e3f/e1 -
- recall: X0's validity bar True; whole 150 of 200; arm rule: the lens effect is the entity; e3f/e1 -

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.86, 'hist': {8: 5, 12: 47, 16: 148}}; rank {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.86, 'hist': {8: 5, 12: 47, 16: 148}}; answer atoms among the 25: {'n': 200, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.015, 'hist': {0: 197, 1: 3}} (3 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.15525, 'share_jpp_A': 0.14848, 'share_A': 0.00909, 'share_A_in_jpp': 0.0051}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 200 | 0.00 [0.00, 0.00] | 0.47 [0.39, 0.54] | 0.53 [0.46, 0.61] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.28 [0.13, 0.45]; lookup: 0.11 [0.07, 0.16] |
| lookup's prompt, S | 200 | 0.00 [0.00, 0.00] | 0.45 [0.38, 0.51] | 0.55 [0.49, 0.62] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.23 [0.16, 0.31]; lookup: 0.08 [0.04, 0.13] |

Arm 1 against the stored run, item by item (agreement.json):

- recall: none 200/200 agree (rerun 0, stored 0); whole 200/200 agree (rerun 150, stored 150); no_jpp 200/200 agree (rerun 35, stored 35); no_jpp_rand 200/200 agree (rerun 146, stored 146); arm 1's extra loss rerun 0.7399999999999999 vs stored 0.7399999999999999
- lookup: none 200/200 agree (rerun 0, stored 0); whole 200/200 agree (rerun 86, stored 86); no_jpp 200/200 agree (rerun 71, stored 71); no_jpp_rand 200/200 agree (rerun 83, stored 83); arm 1's extra loss rerun 0.13953488372093023 vs stored 0.13953488372093023

## e1 on muse-glimmer-30b (muse30_x51_12_e1_r2, L26, source muse30b_x0_necessity)

Source gate: {'pass': True, 'chosen': 200, 'org_read_accuracy': {'PP': 0.966, 'PM': 0.8906}, 'gate': 0.8, 'eligible': 395}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 200, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.00 [0.00, 0.00], S 0.01 [0.00, 0.03], either 0.01 [0.00, 0.03]; median rank O 7380.0, S 5769.5 vs the bridge entity's O 1.0, S 1.0; above the bridge O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00]; not read 0.99 [0.97, 1.00] -> case not_read
- recall (state: lookup's prompts; n 200, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.01 [0.00, 0.02], S 0.01 [0.00, 0.02], either 0.01 [0.00, 0.02]; median rank O 6204.5, S 4954.5 vs the bridge entity's O 1.0, S 1.0; above the bridge O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00]; not read 0.99 [0.98, 1.00] -> case not_read

| arm | lookup | recall |
|---|---|---|
| none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| whole | 0.35 [0.27, 0.44] | 0.59 [0.48, 0.68] |
| no_jpp | 0.34 [0.27, 0.43] | 0.16 [0.10, 0.24] |
| no_jpp_rand | 0.31 [0.24, 0.40] | 0.61 [0.51, 0.70] |
| no_jpp_A | 0.34 [0.27, 0.43] | 0.19 [0.12, 0.28] |
| no_jpp_A_rand | 0.32 [0.25, 0.41] | 0.61 [0.51, 0.70] |
| no_A | 0.35 [0.27, 0.44] | 0.59 [0.49, 0.69] |
| no_A_rand | 0.34 [0.27, 0.43] | 0.59 [0.49, 0.68] |
- lookup: X0's validity bar True; whole 70 of 200; arm rule: can't tell (arm 1 has no extra loss beyond random); e3f/e1 -
- recall: X0's validity bar True; whole 118 of 200; arm rule: the lens effect is the entity; e3f/e1 -

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.94, 'hist': {8: 2, 12: 49, 16: 149}}; rank {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.94, 'hist': {8: 2, 12: 49, 16: 149}}; answer atoms among the 25: {'n': 200, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.005, 'hist': {0: 199, 1: 1}} (1 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.14157, 'share_jpp_A': 0.13667, 'share_A': 0.00866, 'share_A_in_jpp': 0.00432}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 200 | 0.00 [0.00, 0.00] | 0.97 [0.94, 0.99] | 0.03 [0.01, 0.06] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.14 [0.06, 0.23]; lookup: 0.07 [0.04, 0.11] |
| lookup's prompt, S | 200 | 0.00 [0.00, 0.00] | 0.92 [0.86, 0.96] | 0.09 [0.04, 0.14] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.10 [0.05, 0.17]; lookup: 0.09 [0.04, 0.14] |

Arm 1 against the stored run, item by item (agreement.json):

- recall: none 200/200 agree (rerun 0, stored 0); whole 199/200 agree (rerun 118, stored 117); no_jpp 199/200 agree (rerun 32, stored 33); no_jpp_rand 199/200 agree (rerun 122, stored 121); arm 1's extra loss rerun 0.7627118644067796 vs stored 0.7521367521367521
- lookup: none 200/200 agree (rerun 0, stored 0); whole 200/200 agree (rerun 70, stored 70); no_jpp 200/200 agree (rerun 69, stored 69); no_jpp_rand 200/200 agree (rerun 62, stored 62); arm 1's extra loss rerun -0.09999999999999994 vs stored -0.09999999999999994

## cue on qwen3.5-9b (qwen35_9b_x51_12_cue_r2, L12, source qwen35_9b_x47_cue)

Source gate: {'pass': True, 'chosen': 300, 'org_read_accuracy': {'PP': 0.9471428571428572, 'PM': 0.8742857142857143}, 'gate': 0.8}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 300, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; median rank O 1190.0, S 1122.5 vs the bridge entity's O 18.0, S 19.0; above the bridge O 0.03 [0.00, 0.10], S 0.01 [0.00, 0.03]; not read 1.00 [1.00, 1.00] -> case not_read
- recall (state: lookup's prompts; n 300, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; median rank O 1075.5, S 941.5 vs the bridge entity's O 18.0, S 19.0; above the bridge O 0.01 [0.00, 0.02], S 0.00 [0.00, 0.00]; not read 1.00 [1.00, 1.00] -> case not_read

| arm | lookup | recall |
|---|---|---|
| none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] |
| whole | 0.84 [0.81, 0.87] | 0.79 [0.75, 0.82] |
| no_jpp | 0.44 [0.40, 0.49] | 0.34 [0.26, 0.43] |
| no_jpp_rand | 0.50 [0.46, 0.56] | 0.65 [0.60, 0.70] |
| no_jpp_A | 0.50 [0.45, 0.54] | 0.35 [0.28, 0.43] |
| no_jpp_A_rand | 0.53 [0.49, 0.59] | 0.66 [0.62, 0.71] |
| no_A | 0.85 [0.82, 0.88] | 0.78 [0.73, 0.82] |
| no_A_rand | 0.85 [0.82, 0.88] | 0.79 [0.75, 0.82] |
- lookup: X0's validity bar True; whole 252 of 300; arm rule: mixed; e3f/e1 -
- recall: X0's validity bar True; whole 236 of 300; arm rule: the lens effect is the entity; e3f/e1 -

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 300, 'min': 16, 'median': 20.0, 'max': 24, 'mean': 20.667, 'hist': {16: 37, 20: 176, 24: 87}}; rank {'n': 300, 'min': 16, 'median': 20.0, 'max': 24, 'mean': 20.667, 'hist': {16: 37, 20: 176, 24: 87}}; answer atoms among the 25: {'n': 300, 'min': 0, 'median': 0.0, 'max': 0, 'mean': 0.0, 'hist': {0: 300}} (0 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.27891, 'share_jpp_A': 0.27019, 'share_A': 0.01418, 'share_A_in_jpp': 0.00806}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.00 [0.00, 0.00]; lookup: 0.09 [0.06, 0.12] |
| lookup's prompt, S | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.00 [0.00, 0.00]; lookup: 0.11 [0.09, 0.13] |

Arm 1 against the stored run, item by item (agreement.json):

- recall: none 300/300 agree (rerun 1, stored 1); whole 300/300 agree (rerun 236, stored 236); no_jpp 300/300 agree (rerun 102, stored 102); no_jpp_rand 300/300 agree (rerun 194, stored 194); arm 1's extra loss rerun 0.3898305084745762 vs stored 0.3898305084745762
- lookup: none 300/300 agree (rerun 0, stored 0); whole 300/300 agree (rerun 252, stored 252); no_jpp 300/300 agree (rerun 133, stored 133); no_jpp_rand 300/300 agree (rerun 151, stored 151); arm 1's extra loss rerun 0.07142857142857137 vs stored 0.07142857142857137

## cue on qwen3.6-27b (x51_12_cue_27b_r2, L32, source x47_cue_27b)

Source gate: {'pass': True, 'chosen': 300, 'org_read_accuracy': {'PP': 1.0, 'PM': 0.9985714285714286}, 'gate': 0.8}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 300, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; median rank O 8584.5, S 9065.0 vs the bridge entity's O 10.0, S 6.0; above the bridge O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00]; not read 1.00 [1.00, 1.00] -> case not_read
- recall (state: lookup's prompts; n 300, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; median rank O 7178.5, S 7903.0 vs the bridge entity's O 10.0, S 6.0; above the bridge O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00]; not read 1.00 [1.00, 1.00] -> case not_read

| arm | lookup | recall |
|---|---|---|
| none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| whole | 0.82 [0.77, 0.87] | 0.46 [0.33, 0.61] |
| no_jpp | 0.14 [0.08, 0.24] | 0.05 [0.01, 0.12] |
| no_jpp_rand | 0.46 [0.37, 0.58] | 0.27 [0.18, 0.40] |
| no_jpp_A | 0.14 [0.08, 0.24] | 0.06 [0.02, 0.13] |
| no_jpp_A_rand | 0.49 [0.39, 0.61] | 0.28 [0.18, 0.41] |
| no_A | 0.81 [0.74, 0.86] | 0.43 [0.30, 0.58] |
| no_A_rand | 0.81 [0.76, 0.86] | 0.45 [0.32, 0.60] |
- lookup: X0's validity bar True; whole 247 of 300; arm rule: the lens effect is the entity; e3f/e1 -
- recall: X0's validity bar True; whole 138 of 300; arm rule: the lens effect is the entity; e3f/e1 -

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 300, 'min': 16, 'median': 20.0, 'max': 24, 'mean': 20.653, 'hist': {16: 49, 20: 153, 24: 98}}; rank {'n': 300, 'min': 16, 'median': 20.0, 'max': 24, 'mean': 20.653, 'hist': {16: 49, 20: 153, 24: 98}}; answer atoms among the 25: {'n': 300, 'min': 0, 'median': 0.0, 'max': 0, 'mean': 0.0, 'hist': {0: 300}} (0 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.25034, 'share_jpp_A': 0.24195, 'share_A': 0.01192, 'share_A_in_jpp': 0.0078}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.40 [0.18, 0.67]; lookup: 0.09 [0.07, 0.12] |
| lookup's prompt, S | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.39 [0.27, 0.49]; lookup: 0.16 [0.11, 0.20] |

Arm 1 against the stored run, item by item (agreement.json):

- recall: none 300/300 agree (rerun 0, stored 0); whole 300/300 agree (rerun 138, stored 138); no_jpp 300/300 agree (rerun 16, stored 16); no_jpp_rand 300/300 agree (rerun 82, stored 82); arm 1's extra loss rerun 0.4782608695652173 vs stored 0.4782608695652173
- lookup: none 300/300 agree (rerun 0, stored 0); whole 300/300 agree (rerun 247, stored 247); no_jpp 300/300 agree (rerun 43, stored 43); no_jpp_rand 300/300 agree (rerun 139, stored 139); arm 1's extra loss rerun 0.388663967611336 vs stored 0.388663967611336

Arms: whole = Δ = h_S - h_O at the edited token at L; no_jpp = arm 1: Δ - P_J Δ (P_J Δ: X0's 25-atom signed OMP part over the J++ letter-token atoms at L); no_jpp_A = arm 2: Δ - (I - P_A) P_J Δ (the J++ part with the answer directions A projected out); no_A = arm 3: Δ - P_A Δ (the answer directions alone); *_rand = each arm's random twin: Δ minus X0's random subspace part of the removed part's share of ||Δ||^2 (seed 888 + L); no_A_rand is arm 4, 'without a random part of A's share'; no_F = Z2 only: arm 3's frequency-matched control, Δ - P_F Δ (F: per atom of A one unrelated letter atom with its BPE id within a factor 2 and the closest J++ readout norm).
