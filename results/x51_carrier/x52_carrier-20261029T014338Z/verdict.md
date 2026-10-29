# Batch 51, 51.7: Z1 on the full carrier (UNVERIFIED)

Q51.7 (Dan: no prediction: coverage run on an already-scored rule; rules first scored in results/x51_carrier/x51_7-20261028T171646Z). Items: Z1's chosen passages (Zach's jsuite v2, P start, named bridge). Cluster bootstrap over the original bridge entity (10000, seed 0).

Rule (fixed in advance): (i) "The slice explanation": the whole before-L raises the lookup's switch on fact-after items by >= 0.3 over the one-layer whole, and on fact-first brings the lookup within 0.10 of the recall. (ii) On the full carrier, per model and reported per stratum with fact-first decisive: recall extra loss - lookup extra loss >= 0.3 and lookup <= 0.10 -> "the split holds on the full carrier"; lookup >= 0.20 -> "the lookup follows the lens on the full carrier"; else in between. (iii) If fact-after lookups stay under 0.5 even under whole before-L: "the link is made away from the bridge token" -- only then the window-patching read (the bridge token at layers <= L plus the bridge's fact sentence), 50 items, descriptive.

As computed: Items: Z1's chosen passages in Z1's order (its gate.json), rebuilt with x50_zach.z1_cases on the target's tokenizer and equal to Z1's stored cases; Z1's gate decides tested / not tested (numbers descriptive only on a failed gate). Switch = the top token is the first token of the other entity's answer (Z1's read). Before-L = block outputs 0..L (the input embedding is not edited in the three arms: the lens has no map there, and the arms must stay matched; whole_emb, 47.4's (b), beside). Delta_l = h_S,l - h_O,l at the name's last token from clean S and O forwards, per reader; J++ part = x0_necessity.fit(layer l's letter-token J++ atoms, Delta_l, 25, signed); random part = statement_positions.random_subspace_part(Delta_l, its share, X0's random basis seed 888 + l). Shares per stratum (fact-first, fact-after; 'all' beside) with 95% cluster-bootstrap intervals over the original bridge entity (10,000 resamples, seed 0; every arm and both readers on the same draws). (i): rise = S_K(whole_bL) - S_K(whole_1L) on fact-after, clause at >= 0.30; fact-first |S_K(whole_bL) - S_M(whole_bL)| <= 0.10 (the recall under the same arm); 'the slice explanation' iff both; Q51.7 (i) reads the rise clause. (ii): extra loss = X0's excess (S_rand_bL - S_no_jpp_bL) / S_whole_bL per reader, gap = M's - K's on paired draws; labels as written, fact-first decisive, fact-after and all reported; Z1's one-layer cells beside. An undefined extra loss (no switch under whole_bL) holds no clause ("can't tell"). (iii): S_K(whole_bL) on fact-after < 0.50 -> 'the link is made away from the bridge token' and the window read is reported (S_K(window) beside S_K(whole_bL) on the same 50 passages; window = the patch token and both bridges' fact sentences, O's and S's, in the K passage, set to S's states at blocks 0..L); else it stays in the files, unreported. Point estimates decide (EPS 1e-9 at the bars). Loss: mean plain-text loss per arm and reader with intervals, and its ratio to the one-layer whole's (descriptive). Checks: our none read against Z1's stored none read (top token, item by item); the whole before-L switch split by whether only the name's last token differs between O and S (descriptive).

| model | run | status | (i) fact-after rise | (i) fact-first K - M | (i) slice explanation | (ii) fact-first (decisive) | (ii) fact-after | (iii) away from the bridge token |
|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | nem35l_x52_carrier | tested | 0.49 [0.39, 0.60] (True) | -0.08 [-0.14, -0.02] (True) | True | in between | the lookup follows the lens on the full carrier | False |

## nemotron-3.5-lightning (nem35l_x52_carrier, L14; items from nem35l_x52_z1)

Z1's gate: O's read accuracy {'K': 0.9945652173913043, 'M': 0.9184782608695652}, pass True; chosen 200 (strata {'fact-after': 97, 'fact-first': 103}).

Switch shares (the other entity's answer), one-layer (Z1's stored rows) and before-L (this run):

| stratum | n (entities) | reader | none | whole 1L | without J++ 1L | random 1L | whole bL | without J++ bL | random bL | whole bL + emb |
|---|---|---|---|---|---|---|---|---|---|---|
| fact-first | 103 (87) | K | 0.00 [0.00, 0.00] | 0.71 [0.61, 0.80] | 0.52 [0.41, 0.63] | 0.61 [0.50, 0.71] | 0.79 [0.70, 0.87] | 0.58 [0.47, 0.69] | 0.69 [0.58, 0.79] | 0.80 [0.71, 0.88] |
| fact-first | 103 (87) | M | 0.00 [0.00, 0.00] | 0.83 [0.75, 0.91] | 0.49 [0.39, 0.58] | 0.82 [0.73, 0.89] | 0.86 [0.78, 0.93] | 0.51 [0.41, 0.62] | 0.83 [0.75, 0.91] | 0.85 [0.77, 0.93] |
| fact-after | 97 (80) | K | 0.00 [0.00, 0.00] | 0.38 [0.27, 0.49] | 0.19 [0.11, 0.27] | 0.27 [0.18, 0.36] | 0.88 [0.80, 0.94] | 0.45 [0.35, 0.56] | 0.81 [0.73, 0.89] | 0.90 [0.83, 0.95] |
| fact-after | 97 (80) | M | 0.00 [0.00, 0.00] | 0.82 [0.74, 0.90] | 0.25 [0.16, 0.34] | 0.71 [0.61, 0.80] | 0.89 [0.82, 0.94] | 0.34 [0.24, 0.44] | 0.85 [0.77, 0.91] | 0.89 [0.82, 0.94] |
| all | 200 (133) | K | 0.00 [0.00, 0.00] | 0.55 [0.47, 0.63] | 0.36 [0.29, 0.43] | 0.45 [0.37, 0.52] | 0.83 [0.77, 0.88] | 0.52 [0.44, 0.59] | 0.75 [0.68, 0.82] | 0.84 [0.79, 0.90] |
| all | 200 (133) | M | 0.00 [0.00, 0.00] | 0.83 [0.77, 0.88] | 0.37 [0.30, 0.44] | 0.77 [0.70, 0.83] | 0.88 [0.82, 0.92] | 0.43 [0.35, 0.51] | 0.84 [0.78, 0.89] | 0.87 [0.82, 0.92] |

Extra loss without J++ (X0's excess) and the gap (rule ii; before-L decides, one-layer beside):

| stratum | carrier | K extra loss | M extra loss | gap | label | K S_whole | M S_whole | K valid | M valid |
|---|---|---|---|---|---|---|---|---|---|
| fact-first | before | 0.14 [0.05, 0.23] | 0.37 [0.27, 0.48] | 0.23 [0.12, 0.36] | in between | 0.79 [0.70, 0.85] | 0.86 [0.78, 0.92] | True | True |
| fact-first | one | 0.12 [0.04, 0.21] | 0.40 [0.30, 0.50] | 0.27 [0.14, 0.40] | in between | 0.71 [0.61, 0.79] | 0.83 [0.75, 0.89] | True | True |
| fact-after | before | 0.41 [0.31, 0.52] | 0.57 [0.46, 0.68] | 0.16 [0.03, 0.28] | the lookup follows the lens on the full carrier | 0.88 [0.80, 0.93] | 0.89 [0.81, 0.94] | True | True |
| fact-after | one | 0.22 [0.03, 0.41] | 0.56 [0.45, 0.67] | 0.35 [0.12, 0.57] | the lookup follows the lens on the full carrier | 0.38 [0.29, 0.48] | 0.82 [0.74, 0.89] | True | True |
| all | before | 0.28 [0.20, 0.35] | 0.47 [0.39, 0.55] | 0.19 [0.11, 0.28] | the lookup follows the lens on the full carrier | 0.83 [0.77, 0.88] | 0.88 [0.82, 0.91] | True | True |
| all | one | 0.15 [0.07, 0.25] | 0.48 [0.40, 0.55] | 0.32 [0.21, 0.44] | in between | 0.55 [0.48, 0.62] | 0.83 [0.77, 0.88] | True | True |

Rule (iii): fact-after lookups under the whole before-L 0.88 [0.80, 0.94]; under 0.5: False.
The window read (50 passages) is recorded in window.jsonl and not reported (rule iii's condition does not hold).

Plain-text loss at the patch token (O's own next token), mean [CI] and ratio to the one-layer whole's, all passages (descriptive):

| reader | none | whole_1L | no_jpp_1L | rand_1L | whole_bL | no_jpp_bL | rand_bL | whole_emb |
|---|---|---|---|---|---|---|---|---|
| K | 0.80 [0.64, 0.97] (x0.96) | 0.83 [0.67, 1.00] (x1.00) | 0.82 [0.66, 0.99] (x0.99) | 0.82 [0.66, 1.00] (x0.99) | 0.83 [0.67, 1.01] (x1.00) | 0.82 [0.66, 0.99] (x0.99) | 0.82 [0.66, 0.99] (x0.99) | 0.83 [0.67, 1.00] (x1.00) |
| M | 0.86 [0.69, 1.04] (x0.99) | 0.87 [0.70, 1.05] (x1.00) | 0.87 [0.70, 1.05] (x1.00) | 0.87 [0.70, 1.04] (x1.00) | 0.87 [0.70, 1.04] (x1.00) | 0.87 [0.70, 1.05] (x1.00) | 0.86 [0.70, 1.04] (x1.00) | 0.87 [0.70, 1.05] (x1.00) |

Checks: our none read's top token equals Z1's stored none read on 400 of 400 (passage, reader); none reads O's answer {'K': 1.0, 'M': 1.0}; the lookup's whole before-L by whether only the name's last token differs: {"fact-first, only the last token changed": {"n": 64, "lookup_whole_bL": 1.0}, "fact-first, more tokens changed": {"n": 39, "lookup_whole_bL": 0.4358974358974359}, "fact-after, only the last token changed": {"n": 62, "lookup_whole_bL": 1.0}, "fact-after, more tokens changed": {"n": 35, "lookup_whole_bL": 0.6571428571428571}}.

Arms: none = O unedited; whole_1L = Z1's whole arm: h_S,L - h_O,L added at the patch token at L (stored rows); no_jpp_1L = Z1's without-J++ arm at L (stored rows); rand_1L = Z1's without-a-random-part arm at L (stored rows); whole_bL = whole before-L: the patch token set to h_S,l at block outputs 0..L; no_jpp_bL = without J++ before-L: set to h_S,l - P_J,l Delta_l (layer l's own 25 signed-OMP J++ atoms); rand_bL = random before-L: set to h_S,l - a random part of Delta_l of P_J,l Delta_l's share (seed 888 + l); whole_emb = descriptive: whole before-L with S's token at the patch token (47.4's (b)); window = descriptive (rule iii): the patch token and both bridges' fact sentences (O's and S's, K passage) set to S's states at block outputs 0..L; K reader, the first 50 fact-after passages.

Figure: x51_7_nemotron-3.5-lightning.png
