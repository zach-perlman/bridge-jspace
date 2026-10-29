# 51.12: is it the bridge or the answer that moves through the lens? (r2, amendment 20:20; UNVERIFIED)

Batch 51, test 51.12 (jobs/c3/batch51.yaml addendum_4 and addendum_4_amendment; batch 52 coverage, no prediction: coverage run on an already-scored rule (rules first scored in results/x51_answer/x51_12-20261028T201842Z)). Cluster bootstrap over the bridge entity (10000, seed 0), paired across arms.

Rule (fixed in advance): Per model, per reader: "the lens effect is the entity": arm 2 keeps >= 0.7 of arm 1's extra loss and arm 3 costs <= 0.10 beyond random. "The lens effect is the answer": arm 2 falls to <= 0.3 of arm 1 and arm 3 alone costs >= 0.5 of arm 1. Else: mixed, report both shares. Amendment (Dan 20:20): before the arms, the lens readout check at the bridge word; the verdict says which case held, either 'the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)' or the arm-based entity / answer / mixed (never 'void by construction'). Z2: arm 3 is read against its controls (a same-size random part and a frequency-matched part), not against zero.

As computed: Extra loss of arm k = X0's excess = (S_rand_k - S_k) / S_whole per reader over the source run's items (switch: the set's own read; 47.3's lookup: follows the change, identity / position / value). e1, e2, e3 = arms 1, 2, 3; arm 4 (no_A_rand) is arm 3's random twin. 'Keeps >= 0.7 of arm 1' = e2 / e1 >= 0.7; 'costs <= 0.10 beyond random' = e3 <= 0.10; 'falls to <= 0.3 of arm 1' = e2 / e1 <= 0.3; 'costs >= 0.5 of arm 1' = e3 / e1 >= 0.5. Z2: arm 3 against both its controls, e3 (vs no_A_rand) and e3f = (S_noF - S_noA) / S_whole (vs no_F); 'entity' needs max(e3, e3f) <= 0.10, 'answer' needs min(e3, e3f) >= 0.5 e1 (a label holds only against both controls). Point estimates decide (EPS 1e-9); e1 <= 0 or undefined (no switch under the whole change) -> can't tell; CIs from X0's cluster bootstrap over the bridge entity (10,000, seed 0), paired across arms (ratios on the same draws). Readout case first: per reader the rank (1 + tokens with a strictly higher lens logit, full vocabulary) of its own answer word (best of its A-style variant tokens) at the edited token at L, O's answer on O's state and S's on S's (z2: the reader's own state; e1 / cue: the lookup's, shared through the edited token); an item is 'not read' when it ranks > 50 on both; >= 90 % of items not read -> 'the answer word is not read at the bridge word', the arms reported beside; else the arm-based label. A: J++ unit atoms of letter tokens (the OMP dictionary); e1 / cue the answers' number words (suite_v1.WORDS: 6 -> 'six'), each of its variants (as is, leading space, capitalised, both) kept where it is one letter token; z2 the first token of each answer word and variant (where the tokenizer splits the full word, its first token only). Frequency-matched control F (z2): per atom a of A, the letter token f with |log((id_f + 1) / (id_a + 1))| <= log 2 (a BPE id is its merge rank, earlier = more frequent in the tokenizer's training corpus; the factor doubles until a candidate exists) and the closest log J++ readout norm ||(g * W_U[t]) J_L|| (ties: lower id); unrelated = its key (decode, stripped, lower-cased) equals no key of the set's answer words, A tokens, bridge entities' tokens / names or edited tokens, and (keys of >= 3 characters) neither contains nor is contained in one; never twice in one item. no_F = Δ - P_F Δ, P_F the projector on span(F). Decisive cells for Q51.12: Z2 both readers; E1 the recall (the lookup beside); 47.3 both readers. Projected out: (I - P_A) P_J Δ, P_A the orthogonal projector on the span of the item's answer atoms (the J++ part minus its component along span(A)).

Which case held, per cell: first the readout check (the reader's own answer word at the edited token at L; 'not read' = rank > 50 on both O and S), then the arms.

| set | model | reader | n | answer word top-50 O | top-50 S | not read | case | e1 (no J++) | e2 (no J++, A kept) | e3 (no A vs random) | e3f (no A vs freq.) | e2/e1 | e3/e1 | verdict | decisive |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| z1k | qwen3.5-9b | | pending (no manifest here) | | | | | | | | | | | | |
| z1k | qwen3.6-27b | lookup | 200 | 0.85 [0.80, 0.91] | 0.71 [0.65, 0.78] | 0.07 [0.03, 0.11] | arms | 0.30 [0.20, 0.40] | 0.14 [0.07, 0.23] | 0.10 [0.04, 0.18] | 0.10 [0.04, 0.18] | 0.48 [0.26, 0.73] | 0.35 [0.15, 0.61] | **mixed** | yes |
| z1k | qwen3.6-27b | recall | 200 | 0.80 [0.74, 0.86] | 0.74 [0.67, 0.80] | 0.09 [0.05, 0.13] | arms | 0.58 [0.50, 0.67] | 0.17 [0.09, 0.25] | 0.32 [0.24, 0.41] | 0.29 [0.21, 0.37] | 0.29 [0.15, 0.42] | 0.55 [0.41, 0.72] | **mixed** | yes |
| z1k | nemotron-3.5-lightning | | pending (no manifest here) | | | | | | | | | | | | |

## z1k on qwen3.6-27b (x52_answer_z1k_27b, L32, source x50_z1_27b)

Source gate: {'pass': True, 'chosen': 200, 'org_read_accuracy': {'K': 1.0, 'M': 0.8962962962962963}, 'gate': 0.8}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 200, no letter token for the word 0): top-10 O 0.62 [0.54, 0.71], S 0.48 [0.40, 0.56], either 0.74 [0.67, 0.81]; top-50 O 0.85 [0.80, 0.91], S 0.71 [0.65, 0.78], either 0.93 [0.89, 0.97]; median rank O 4.0, S 12.0 vs the bridge entity's O 1.0, S 1.0; above the bridge O 0.30 [0.23, 0.38], S 0.23 [0.16, 0.30]; not read 0.07 [0.03, 0.11] -> case arms
- recall (state: recall's prompts; n 200, no letter token for the word 0): top-10 O 0.58 [0.50, 0.67], S 0.51 [0.43, 0.59], either 0.70 [0.63, 0.78]; top-50 O 0.80 [0.74, 0.86], S 0.74 [0.67, 0.80], either 0.92 [0.87, 0.95]; median rank O 5.0, S 8.5 vs the bridge entity's O 1.0, S 1.0; above the bridge O 0.28 [0.21, 0.36], S 0.26 [0.18, 0.34]; not read 0.09 [0.05, 0.13] -> case arms

| arm | lookup | recall |
|---|---|---|
| none | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| whole | 0.39 [0.31, 0.46] | 0.62 [0.55, 0.70] |
| no_jpp | 0.23 [0.17, 0.29] | 0.21 [0.15, 0.27] |
| no_jpp_rand | 0.34 [0.28, 0.41] | 0.57 [0.50, 0.65] |
| no_jpp_A | 0.30 [0.23, 0.38] | 0.52 [0.43, 0.60] |
| no_jpp_A_rand | 0.36 [0.29, 0.43] | 0.62 [0.54, 0.69] |
| no_A | 0.34 [0.27, 0.42] | 0.45 [0.37, 0.52] |
| no_A_rand | 0.39 [0.31, 0.46] | 0.65 [0.57, 0.71] |
| no_F | 0.39 [0.31, 0.46] | 0.62 [0.55, 0.70] |
- lookup: X0's validity bar True; whole 77 of 200; arm rule: mixed; e3f/e1 0.35 [0.14, 0.64]
- recall: X0's validity bar True; whole 125 of 200; arm rule: mixed; e3f/e1 0.49 [0.36, 0.65]

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 200, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 200}}; rank {'n': 200, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 200}}; answer atoms among the 25: {'n': 200, 'min': 0, 'median': 0.0, 'max': 2, 'mean': 0.055, 'hist': {0: 190, 1: 9, 2: 1}} (10 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.16772, 'share_jpp_A': 0.14744, 'share_A': 0.02328, 'share_A_in_jpp': 0.02034, 'share_F': 0.003}; frequency match {'pairs': 800, 'median_id_ratio': 1.303, 'median_norm_ratio': 1.0, 'widened': 0}
- Δ from the recall's prompts: |A| tokens {'n': 200, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 200}}; rank {'n': 200, 'min': 4, 'median': 4.0, 'max': 4, 'mean': 4.0, 'hist': {4: 200}}; answer atoms among the 25: {'n': 200, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.05, 'hist': {0: 190, 1: 10}} (10 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.1724, 'share_jpp_A': 0.14639, 'share_A': 0.02396, 'share_A_in_jpp': 0.02193, 'share_F': 0.00297}; frequency match {'pairs': 800, 'median_id_ratio': 1.303, 'median_norm_ratio': 1.0, 'widened': 0}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 200 | 0.12 [0.07, 0.17] | 0.62 [0.54, 0.70] | 0.27 [0.20, 0.34] | lookup_answer: 0.12 [0.07, 0.17]; recall_answer: 0.12 [0.07, 0.17] | 0.00 [0.00, 0.00] | - |
| lookup's prompt, S | 200 | 0.07 [0.03, 0.10] | 0.51 [0.42, 0.59] | 0.43 [0.35, 0.52] | lookup_answer: 0.07 [0.03, 0.10]; recall_answer: 0.07 [0.03, 0.10] | 0.00 [0.00, 0.00] | - |
| recall's prompt, O | 200 | 0.09 [0.05, 0.14] | 0.63 [0.54, 0.71] | 0.28 [0.21, 0.36] | lookup_answer: 0.09 [0.05, 0.14]; recall_answer: 0.09 [0.05, 0.14] | 0.00 [0.00, 0.00] | - |
| recall's prompt, S | 200 | 0.08 [0.04, 0.12] | 0.54 [0.45, 0.62] | 0.39 [0.31, 0.47] | lookup_answer: 0.08 [0.04, 0.12]; recall_answer: 0.08 [0.04, 0.12] | 0.00 [0.00, 0.00] | - |

Arm 1 against the stored run, item by item (agreement.json):

- lookup: none 200/200 agree (rerun 0, stored 0); whole 199/200 agree (rerun 77, stored 76); no_jpp 199/200 agree (rerun 46, stored 47); no_jpp_rand 199/200 agree (rerun 69, stored 68); arm 1's extra loss rerun 0.2987012987012986 vs stored 0.2763157894736843
- recall: none 200/200 agree (rerun 0, stored 0); whole 199/200 agree (rerun 125, stored 126); no_jpp 198/200 agree (rerun 42, stored 42); no_jpp_rand 200/200 agree (rerun 115, stored 115); arm 1's extra loss rerun 0.584 vs stored 0.5793650793650793

Arms: whole = Δ = h_S - h_O at the edited token at L; no_jpp = arm 1: Δ - P_J Δ (P_J Δ: X0's 25-atom signed OMP part over the J++ letter-token atoms at L); no_jpp_A = arm 2: Δ - (I - P_A) P_J Δ (the J++ part with the answer directions A projected out); no_A = arm 3: Δ - P_A Δ (the answer directions alone); *_rand = each arm's random twin: Δ minus X0's random subspace part of the removed part's share of ||Δ||^2 (seed 888 + L); no_A_rand is arm 4, 'without a random part of A's share'; no_F = Z2 only: arm 3's frequency-matched control, Δ - P_F Δ (F: per atom of A one unrelated letter atom with its BPE id within a factor 2 and the closest J++ readout norm).
