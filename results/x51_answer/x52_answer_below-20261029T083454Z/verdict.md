# 51.12: is it the bridge or the answer that moves through the lens? (r2, amendment 20:20; UNVERIFIED)

Batch 51, test 51.12 (jobs/c3/batch51.yaml addendum_4 and addendum_4_amendment; batch 52 coverage, below gate (exploratory): Lightning's 47.3 gate fails (O's lookup read 0.72 < 0.80, results/x47_cue/nem35l_x52_cue/gate.json); eligible scenes only; hollow, never in the claims table or grades; rules verbatim, no prediction (Dan's morning queue, 29 Oct) (rules first scored in results/x51_answer/x51_12-20261028T201842Z)). Cluster bootstrap over the bridge entity (10000, seed 0), paired across arms.

Rule (fixed in advance): Per model, per reader: "the lens effect is the entity": arm 2 keeps >= 0.7 of arm 1's extra loss and arm 3 costs <= 0.10 beyond random. "The lens effect is the answer": arm 2 falls to <= 0.3 of arm 1 and arm 3 alone costs >= 0.5 of arm 1. Else: mixed, report both shares. Amendment (Dan 20:20): before the arms, the lens readout check at the bridge word; the verdict says which case held, either 'the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)' or the arm-based entity / answer / mixed (never 'void by construction'). Z2: arm 3 is read against its controls (a same-size random part and a frequency-matched part), not against zero.

As computed: Extra loss of arm k = X0's excess = (S_rand_k - S_k) / S_whole per reader over the source run's items (switch: the set's own read; 47.3's lookup: follows the change, identity / position / value). e1, e2, e3 = arms 1, 2, 3; arm 4 (no_A_rand) is arm 3's random twin. 'Keeps >= 0.7 of arm 1' = e2 / e1 >= 0.7; 'costs <= 0.10 beyond random' = e3 <= 0.10; 'falls to <= 0.3 of arm 1' = e2 / e1 <= 0.3; 'costs >= 0.5 of arm 1' = e3 / e1 >= 0.5. Z2: arm 3 against both its controls, e3 (vs no_A_rand) and e3f = (S_noF - S_noA) / S_whole (vs no_F); 'entity' needs max(e3, e3f) <= 0.10, 'answer' needs min(e3, e3f) >= 0.5 e1 (a label holds only against both controls). Point estimates decide (EPS 1e-9); e1 <= 0 or undefined (no switch under the whole change) -> can't tell; CIs from X0's cluster bootstrap over the bridge entity (10,000, seed 0), paired across arms (ratios on the same draws). Readout case first: per reader the rank (1 + tokens with a strictly higher lens logit, full vocabulary) of its own answer word (best of its A-style variant tokens) at the edited token at L, O's answer on O's state and S's on S's (z2: the reader's own state; e1 / cue: the lookup's, shared through the edited token); an item is 'not read' when it ranks > 50 on both; >= 90 % of items not read -> 'the answer word is not read at the bridge word', the arms reported beside; else the arm-based label. A: J++ unit atoms of letter tokens (the OMP dictionary); e1 / cue the answers' number words (suite_v1.WORDS: 6 -> 'six'), each of its variants (as is, leading space, capitalised, both) kept where it is one letter token; z2 the first token of each answer word and variant (where the tokenizer splits the full word, its first token only). Frequency-matched control F (z2): per atom a of A, the letter token f with |log((id_f + 1) / (id_a + 1))| <= log 2 (a BPE id is its merge rank, earlier = more frequent in the tokenizer's training corpus; the factor doubles until a candidate exists) and the closest log J++ readout norm ||(g * W_U[t]) J_L|| (ties: lower id); unrelated = its key (decode, stripped, lower-cased) equals no key of the set's answer words, A tokens, bridge entities' tokens / names or edited tokens, and (keys of >= 3 characters) neither contains nor is contained in one; never twice in one item. no_F = Δ - P_F Δ, P_F the projector on span(F). Decisive cells for Q51.12: Z2 both readers; E1 the recall (the lookup beside); 47.3 both readers. Projected out: (I - P_A) P_J Δ, P_A the orthogonal projector on the span of the item's answer atoms (the J++ part minus its component along span(A)).

Which case held, per cell: first the readout check (the reader's own answer word at the edited token at L; 'not read' = rank > 50 on both O and S), then the arms.

| set | model | reader | n | answer word top-50 O | top-50 S | not read | case | e1 (no J++) | e2 (no J++, A kept) | e3 (no A vs random) | e3f (no A vs freq.) | e2/e1 | e3/e1 | verdict | decisive |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cue | nemotron-3.5-lightning | lookup | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | not_read | 0.17 [0.10, 0.22] | 0.15 [0.09, 0.21] | 0.00 [-0.01, 0.02] | - | 0.90 [0.67, 1.28] | 0.02 [-0.09, 0.15] | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) (100% of 300 items; arms beside: the lens effect is the entity)** | yes |
| cue | nemotron-3.5-lightning | recall | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | not_read | 0.48 [0.37, 0.57] | 0.50 [0.38, 0.58] | 0.00 [-0.02, 0.02] | - | 1.04 [0.94, 1.17] | 0.00 [-0.05, 0.05] | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) (100% of 300 items; arms beside: the lens effect is the entity)** | yes |

## cue on nemotron-3.5-lightning (nem35l_x52_cue_answer_below, L14, source nem35l_x52_cue_below)

Source gate: {'pass': True, 'chosen': 300, 'org_read_accuracy': {'PP': 0.7228571428571429, 'PM': 0.87}, 'gate': 0.8, 'below_gate': True, 'source_gate_pass': False}.

Readout check (the answer word at the edited token):

- lookup (state: lookup's prompts; n 300, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; median rank O 15180.0, S 23568.5 vs the bridge entity's O 5.0, S 5.0; above the bridge O 0.01 [0.00, 0.04], S 0.01 [0.00, 0.02]; not read 1.00 [1.00, 1.00] -> case not_read
- recall (state: lookup's prompts; n 300, no letter token for the word 0): top-10 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], either 0.00 [0.00, 0.00]; median rank O 13418.0, S 15731.0 vs the bridge entity's O 5.0, S 5.0; above the bridge O 0.01 [0.00, 0.04], S 0.01 [0.00, 0.02]; not read 1.00 [1.00, 1.00] -> case not_read

| arm | lookup | recall |
|---|---|---|
| none | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.01] |
| whole | 0.81 [0.75, 0.86] | 0.88 [0.85, 0.90] |
| no_jpp | 0.51 [0.46, 0.59] | 0.29 [0.20, 0.41] |
| no_jpp_rand | 0.64 [0.59, 0.71] | 0.71 [0.63, 0.78] |
| no_jpp_A | 0.53 [0.47, 0.61] | 0.32 [0.23, 0.43] |
| no_jpp_A_rand | 0.65 [0.60, 0.72] | 0.75 [0.70, 0.81] |
| no_A | 0.80 [0.74, 0.86] | 0.87 [0.82, 0.89] |
| no_A_rand | 0.80 [0.74, 0.86] | 0.87 [0.82, 0.89] |
- lookup: X0's validity bar True; whole 242 of 300; arm rule: the lens effect is the entity; e3f/e1 -
- recall: X0's validity bar True; whole 264 of 300; arm rule: the lens effect is the entity; e3f/e1 -

Answer directions and OMP atoms (per item):

- Δ from the lookup's prompts: |A| tokens {'n': 300, 'min': 13, 'median': 19.0, 'max': 24, 'mean': 18.843, 'hist': {13: 2, 14: 16, 15: 26, 16: 18, 17: 11, 18: 65, 19: 64, 20: 12, 21: 11, 22: 46, 23: 27, 24: 2}}; rank {'n': 300, 'min': 13, 'median': 19.0, 'max': 24, 'mean': 18.843, 'hist': {13: 2, 14: 16, 15: 26, 16: 18, 17: 11, 18: 65, 19: 64, 20: 12, 21: 11, 22: 46, 23: 27, 24: 2}}; answer atoms among the 25: {'n': 300, 'min': 0, 'median': 0.0, 'max': 0, 'mean': 0.0, 'hist': {0: 300}} (0 items with at least one); median shares of ||Δ||^2 {'share_jpp': 0.25604, 'share_jpp_A': 0.24652, 'share_A': 0.01443, 'share_A_in_jpp': 0.00958}

Lens readout at the edited token (top-1 over the vocabulary; O = org, S = alt):

| state | n | own answer | own bridge | neither | per reader's answer | other prompt's answer | top digit = reader's answer |
|---|---|---|---|---|---|---|---|
| lookup's prompt, O | 300 | 0.00 [0.00, 0.00] | 0.15 [0.00, 0.42] | 0.85 [0.58, 1.00] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.11 [0.01, 0.29]; lookup: 0.08 [0.05, 0.11] |
| lookup's prompt, S | 300 | 0.00 [0.00, 0.00] | 0.15 [0.10, 0.20] | 0.85 [0.80, 0.90] | recall_answer: 0.00 [0.00, 0.00]; lookup_answer: 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | recall: 0.11 [0.07, 0.14]; lookup: 0.11 [0.06, 0.16] |

Arm 1 against the stored run, item by item (agreement.json):

- recall: none 300/300 agree (rerun 1, stored 1); whole 300/300 agree (rerun 264, stored 264); no_jpp 300/300 agree (rerun 87, stored 87); no_jpp_rand 300/300 agree (rerun 213, stored 213); arm 1's extra loss rerun 0.47727272727272724 vs stored 0.47727272727272724
- lookup: none 300/300 agree (rerun 2, stored 2); whole 300/300 agree (rerun 242, stored 242); no_jpp 300/300 agree (rerun 153, stored 153); no_jpp_rand 300/300 agree (rerun 193, stored 193); arm 1's extra loss rerun 0.16528925619834708 vs stored 0.16528925619834708

Arms: whole = Δ = h_S - h_O at the edited token at L; no_jpp = arm 1: Δ - P_J Δ (P_J Δ: X0's 25-atom signed OMP part over the J++ letter-token atoms at L); no_jpp_A = arm 2: Δ - (I - P_A) P_J Δ (the J++ part with the answer directions A projected out); no_A = arm 3: Δ - P_A Δ (the answer directions alone); *_rand = each arm's random twin: Δ minus X0's random subspace part of the removed part's share of ||Δ||^2 (seed 888 + L); no_A_rand is arm 4, 'without a random part of A's share'; no_F = Z2 only: arm 3's frequency-matched control, Δ - P_F Δ (F: per atom of A one unrelated letter atom with its BPE id within a factor 2 and the closest J++ readout norm).
