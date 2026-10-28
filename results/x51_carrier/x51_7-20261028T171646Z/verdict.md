# Batch 51, 51.7: Z1 on the full carrier (UNVERIFIED)

Q51.7 (Dan: (i) yes · 85%; no · 15% | (ii) (b) · 60%; (c) · 30%; (a) · 10%). Items: Z1's chosen passages (Zach's jsuite v2, P start, named bridge). Cluster bootstrap over the original bridge entity (10000, seed 0).

Rule (fixed in advance): (i) "The slice explanation": the whole before-L raises the lookup's switch on fact-after items by >= 0.3 over the one-layer whole, and on fact-first brings the lookup within 0.10 of the recall. (ii) On the full carrier, per model and reported per stratum with fact-first decisive: recall extra loss - lookup extra loss >= 0.3 and lookup <= 0.10 -> "the split holds on the full carrier"; lookup >= 0.20 -> "the lookup follows the lens on the full carrier"; else in between. (iii) If fact-after lookups stay under 0.5 even under whole before-L: "the link is made away from the bridge token" -- only then the window-patching read (the bridge token at layers <= L plus the bridge's fact sentence), 50 items, descriptive.

As computed: Items: Z1's chosen passages in Z1's order (its gate.json), rebuilt with x50_zach.z1_cases on the target's tokenizer and equal to Z1's stored cases; Z1's gate decides tested / not tested (numbers descriptive only on a failed gate). Switch = the top token is the first token of the other entity's answer (Z1's read). Before-L = block outputs 0..L (the input embedding is not edited in the three arms: the lens has no map there, and the arms must stay matched; whole_emb, 47.4's (b), beside). Delta_l = h_S,l - h_O,l at the name's last token from clean S and O forwards, per reader; J++ part = x0_necessity.fit(layer l's letter-token J++ atoms, Delta_l, 25, signed); random part = statement_positions.random_subspace_part(Delta_l, its share, X0's random basis seed 888 + l). Shares per stratum (fact-first, fact-after; 'all' beside) with 95% cluster-bootstrap intervals over the original bridge entity (10,000 resamples, seed 0; every arm and both readers on the same draws). (i): rise = S_K(whole_bL) - S_K(whole_1L) on fact-after, clause at >= 0.30; fact-first |S_K(whole_bL) - S_M(whole_bL)| <= 0.10 (the recall under the same arm); 'the slice explanation' iff both; Q51.7 (i) reads the rise clause. (ii): extra loss = X0's excess (S_rand_bL - S_no_jpp_bL) / S_whole_bL per reader, gap = M's - K's on paired draws; labels as written, fact-first decisive, fact-after and all reported; Z1's one-layer cells beside. An undefined extra loss (no switch under whole_bL) holds no clause ("can't tell"). (iii): S_K(whole_bL) on fact-after < 0.50 -> 'the link is made away from the bridge token' and the window read is reported (S_K(window) beside S_K(whole_bL) on the same 50 passages; window = the patch token and both bridges' fact sentences, O's and S's, in the K passage, set to S's states at blocks 0..L); else it stays in the files, unreported. Point estimates decide (EPS 1e-9 at the bars). Loss: mean plain-text loss per arm and reader with intervals, and its ratio to the one-layer whole's (descriptive). Checks: our none read against Z1's stored none read (top token, item by item); the whole before-L switch split by whether only the name's last token differs between O and S (descriptive).

| model | run | status | (i) fact-after rise | (i) fact-first K - M | (i) slice explanation | (ii) fact-first (decisive) | (ii) fact-after | (iii) away from the bridge token |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | qwen35_9b_x51_7 | tested | 0.54 [0.44, 0.64] (True) | -0.01 [-0.05, 0.03] (True) | True | in between | the lookup follows the lens on the full carrier | False |
| qwen3.6-27b | x51_7_27b | tested | 0.73 [0.64, 0.81] (True) | -0.02 [-0.07, 0.03] (True) | True | in between | the lookup follows the lens on the full carrier | False |

## qwen3.5-9b (qwen35_9b_x51_7, L12; items from qwen35_9b_x50_z1)

Z1's gate: O's read accuracy {'K': 0.9466911764705882, 'M': 0.8419117647058824}, pass True; chosen 200 (strata {'fact-after': 100, 'fact-first': 100}).

Switch shares (the other entity's answer), one-layer (Z1's stored rows) and before-L (this run):

| stratum | n (entities) | reader | none | whole 1L | without J++ 1L | random 1L | whole bL | without J++ bL | random bL | whole bL + emb |
|---|---|---|---|---|---|---|---|---|---|---|
| fact-first | 100 (79) | K | 0.00 [0.00, 0.00] | 0.78 [0.68, 0.86] | 0.60 [0.49, 0.70] | 0.75 [0.65, 0.84] | 0.86 [0.78, 0.93] | 0.69 [0.58, 0.78] | 0.78 [0.68, 0.86] | 0.85 [0.77, 0.92] |
| fact-first | 100 (79) | M | 0.00 [0.00, 0.00] | 0.81 [0.72, 0.89] | 0.34 [0.26, 0.42] | 0.77 [0.68, 0.85] | 0.87 [0.79, 0.94] | 0.44 [0.34, 0.53] | 0.80 [0.71, 0.88] | 0.87 [0.79, 0.94] |
| fact-after | 100 (80) | K | 0.00 [0.00, 0.00] | 0.36 [0.27, 0.46] | 0.11 [0.05, 0.18] | 0.26 [0.17, 0.36] | 0.90 [0.84, 0.95] | 0.36 [0.27, 0.45] | 0.82 [0.74, 0.89] | 0.90 [0.84, 0.95] |
| fact-after | 100 (80) | M | 0.00 [0.00, 0.00] | 0.78 [0.69, 0.86] | 0.14 [0.07, 0.22] | 0.72 [0.63, 0.81] | 0.87 [0.79, 0.94] | 0.22 [0.14, 0.31] | 0.79 [0.70, 0.87] | 0.88 [0.80, 0.94] |
| all | 200 (120) | K | 0.00 [0.00, 0.00] | 0.57 [0.49, 0.64] | 0.35 [0.28, 0.43] | 0.51 [0.43, 0.58] | 0.88 [0.82, 0.93] | 0.53 [0.45, 0.60] | 0.80 [0.73, 0.86] | 0.88 [0.82, 0.92] |
| all | 200 (120) | M | 0.00 [0.00, 0.00] | 0.80 [0.73, 0.85] | 0.24 [0.18, 0.30] | 0.74 [0.68, 0.81] | 0.87 [0.81, 0.92] | 0.33 [0.26, 0.40] | 0.80 [0.73, 0.85] | 0.88 [0.82, 0.92] |

Extra loss without J++ (X0's excess) and the gap (rule ii; before-L decides, one-layer beside):

| stratum | carrier | K extra loss | M extra loss | gap | label | K S_whole | M S_whole | K valid | M valid |
|---|---|---|---|---|---|---|---|---|---|
| fact-first | before | 0.10 [0.05, 0.17] | 0.41 [0.31, 0.52] | 0.31 [0.20, 0.42] | in between | 0.86 [0.78, 0.91] | 0.87 [0.79, 0.92] | True | True |
| fact-first | one | 0.19 [0.10, 0.30] | 0.53 [0.43, 0.64] | 0.34 [0.22, 0.45] | in between | 0.78 [0.69, 0.85] | 0.81 [0.72, 0.87] | True | True |
| fact-after | before | 0.51 [0.41, 0.61] | 0.66 [0.55, 0.75] | 0.14 [0.03, 0.26] | the lookup follows the lens on the full carrier | 0.90 [0.83, 0.94] | 0.87 [0.79, 0.92] | True | True |
| fact-after | one | 0.42 [0.25, 0.59] | 0.74 [0.63, 0.85] | 0.33 [0.14, 0.50] | the lookup follows the lens on the full carrier | 0.36 [0.27, 0.46] | 0.78 [0.69, 0.85] | True | True |
| all | before | 0.31 [0.25, 0.39] | 0.53 [0.46, 0.61] | 0.22 [0.14, 0.30] | the lookup follows the lens on the full carrier | 0.88 [0.83, 0.92] | 0.87 [0.82, 0.91] | True | True |
| all | one | 0.26 [0.18, 0.36] | 0.64 [0.56, 0.71] | 0.37 [0.27, 0.47] | the lookup follows the lens on the full carrier | 0.57 [0.50, 0.64] | 0.80 [0.73, 0.85] | True | True |

Rule (iii): fact-after lookups under the whole before-L 0.90 [0.84, 0.95]; under 0.5: False.
The window read (50 passages) is recorded in window.jsonl and not reported (rule iii's condition does not hold).

Plain-text loss at the patch token (O's own next token), mean [CI] and ratio to the one-layer whole's, all passages (descriptive):

| reader | none | whole_1L | no_jpp_1L | rand_1L | whole_bL | no_jpp_bL | rand_bL | whole_emb |
|---|---|---|---|---|---|---|---|---|
| K | 0.77 [0.56, 0.99] (x0.98) | 0.78 [0.54, 1.06] (x1.00) | 0.76 [0.53, 1.03] (x0.97) | 0.77 [0.53, 1.04] (x0.98) | 0.78 [0.54, 1.06] (x1.00) | 0.76 [0.53, 1.03] (x0.97) | 0.77 [0.53, 1.04] (x0.98) | 0.78 [0.54, 1.06] (x1.00) |
| M | 0.76 [0.56, 0.97] (x0.97) | 0.78 [0.56, 1.03] (x1.00) | 0.76 [0.54, 0.99] (x0.97) | 0.75 [0.54, 0.99] (x0.97) | 0.78 [0.56, 1.03] (x1.00) | 0.76 [0.54, 0.99] (x0.97) | 0.75 [0.54, 0.99] (x0.97) | 0.78 [0.56, 1.03] (x1.00) |

Checks: our none read's top token equals Z1's stored none read on 400 of 400 (passage, reader); none reads O's answer {'K': 1.0, 'M': 1.0}; the lookup's whole before-L by whether only the name's last token differs: {"fact-first, only the last token changed": {"n": 73, "lookup_whole_bL": 1.0}, "fact-first, more tokens changed": {"n": 27, "lookup_whole_bL": 0.48148148148148145}, "fact-after, only the last token changed": {"n": 65, "lookup_whole_bL": 1.0}, "fact-after, more tokens changed": {"n": 35, "lookup_whole_bL": 0.7142857142857143}}.

## qwen3.6-27b (x51_7_27b, L32; items from x50_z1_27b)

Z1's gate: O's read accuracy {'K': 1.0, 'M': 0.8962962962962963}, pass True; chosen 200 (strata {'fact-after': 103, 'fact-first': 97}).

Switch shares (the other entity's answer), one-layer (Z1's stored rows) and before-L (this run):

| stratum | n (entities) | reader | none | whole 1L | without J++ 1L | random 1L | whole bL | without J++ bL | random bL | whole bL + emb |
|---|---|---|---|---|---|---|---|---|---|---|
| fact-first | 97 (77) | K | 0.00 [0.00, 0.00] | 0.67 [0.57, 0.76] | 0.47 [0.36, 0.58] | 0.65 [0.55, 0.74] | 0.79 [0.70, 0.88] | 0.64 [0.53, 0.74] | 0.76 [0.66, 0.85] | 0.78 [0.69, 0.87] |
| fact-first | 97 (77) | M | 0.00 [0.00, 0.00] | 0.63 [0.51, 0.73] | 0.31 [0.22, 0.40] | 0.59 [0.47, 0.69] | 0.81 [0.72, 0.89] | 0.57 [0.46, 0.67] | 0.79 [0.70, 0.87] | 0.81 [0.72, 0.89] |
| fact-after | 103 (82) | K | 0.00 [0.00, 0.00] | 0.11 [0.05, 0.17] | 0.01 [0.00, 0.03] | 0.05 [0.01, 0.09] | 0.83 [0.76, 0.90] | 0.37 [0.28, 0.46] | 0.80 [0.70, 0.88] | 0.83 [0.76, 0.90] |
| fact-after | 103 (82) | M | 0.00 [0.00, 0.00] | 0.63 [0.53, 0.73] | 0.12 [0.06, 0.18] | 0.56 [0.46, 0.66] | 0.84 [0.77, 0.91] | 0.29 [0.20, 0.38] | 0.81 [0.72, 0.88] | 0.84 [0.77, 0.91] |
| all | 200 (116) | K | 0.00 [0.00, 0.00] | 0.38 [0.31, 0.45] | 0.23 [0.17, 0.30] | 0.34 [0.27, 0.41] | 0.81 [0.75, 0.87] | 0.50 [0.42, 0.57] | 0.78 [0.71, 0.84] | 0.81 [0.74, 0.87] |
| all | 200 (116) | M | 0.00 [0.00, 0.00] | 0.63 [0.55, 0.70] | 0.21 [0.16, 0.27] | 0.57 [0.50, 0.65] | 0.83 [0.77, 0.88] | 0.42 [0.35, 0.49] | 0.80 [0.73, 0.86] | 0.83 [0.77, 0.88] |

Extra loss without J++ (X0's excess) and the gap (rule ii; before-L decides, one-layer beside):

| stratum | carrier | K extra loss | M extra loss | gap | label | K S_whole | M S_whole | K valid | M valid |
|---|---|---|---|---|---|---|---|---|---|
| fact-first | before | 0.16 [0.07, 0.25] | 0.28 [0.18, 0.38] | 0.12 [0.01, 0.24] | in between | 0.79 [0.70, 0.86] | 0.81 [0.73, 0.88] | True | True |
| fact-first | one | 0.26 [0.16, 0.37] | 0.44 [0.30, 0.57] | 0.18 [0.02, 0.34] | the lookup follows the lens on the full carrier | 0.67 [0.57, 0.76] | 0.63 [0.53, 0.72] | True | True |
| fact-after | before | 0.51 [0.42, 0.61] | 0.61 [0.50, 0.71] | 0.10 [0.00, 0.19] | the lookup follows the lens on the full carrier | 0.83 [0.75, 0.89] | 0.84 [0.76, 0.90] | True | True |
| fact-after | one | 0.36 [0.08, 0.75] | 0.71 [0.58, 0.83] | 0.34 [-0.09, 0.68] | the lookup follows the lens on the full carrier | 0.11 [0.06, 0.18] | 0.63 [0.53, 0.72] | False | True |
| all | before | 0.34 [0.28, 0.41] | 0.45 [0.38, 0.52] | 0.11 [0.03, 0.18] | the lookup follows the lens on the full carrier | 0.81 [0.76, 0.86] | 0.83 [0.77, 0.88] | True | True |
| all | one | 0.28 [0.18, 0.38] | 0.58 [0.49, 0.66] | 0.30 [0.17, 0.43] | the lookup follows the lens on the full carrier | 0.38 [0.32, 0.45] | 0.63 [0.56, 0.69] | True | True |

Rule (iii): fact-after lookups under the whole before-L 0.83 [0.76, 0.90]; under 0.5: False.
The window read (50 passages) is recorded in window.jsonl and not reported (rule iii's condition does not hold).

Plain-text loss at the patch token (O's own next token), mean [CI] and ratio to the one-layer whole's, all passages (descriptive):

| reader | none | whole_1L | no_jpp_1L | rand_1L | whole_bL | no_jpp_bL | rand_bL | whole_emb |
|---|---|---|---|---|---|---|---|---|
| K | 3.44 [3.14, 3.77] (x1.14) | 3.02 [2.65, 3.44] (x1.00) | 3.21 [2.85, 3.61] (x1.06) | 3.04 [2.67, 3.46] (x1.01) | 3.01 [2.65, 3.44] (x1.00) | 3.21 [2.86, 3.62] (x1.06) | 3.04 [2.67, 3.46] (x1.01) | 3.02 [2.66, 3.45] (x1.00) |
| M | 3.93 [3.57, 4.35] (x1.23) | 3.19 [2.84, 3.57] (x1.00) | 3.38 [3.04, 3.76] (x1.06) | 3.23 [2.87, 3.62] (x1.01) | 3.18 [2.83, 3.57] (x1.00) | 3.38 [3.04, 3.76] (x1.06) | 3.23 [2.87, 3.63] (x1.01) | 3.18 [2.84, 3.57] (x1.00) |

Checks: our none read's top token equals Z1's stored none read on 400 of 400 (passage, reader); none reads O's answer {'K': 1.0, 'M': 1.0}; the lookup's whole before-L by whether only the name's last token differs: {"fact-first, only the last token changed": {"n": 73, "lookup_whole_bL": 1.0}, "fact-first, more tokens changed": {"n": 24, "lookup_whole_bL": 0.16666666666666666}, "fact-after, only the last token changed": {"n": 66, "lookup_whole_bL": 1.0}, "fact-after, more tokens changed": {"n": 37, "lookup_whole_bL": 0.5405405405405406}}.

Arms: none = O unedited; whole_1L = Z1's whole arm: h_S,L - h_O,L added at the patch token at L (stored rows); no_jpp_1L = Z1's without-J++ arm at L (stored rows); rand_1L = Z1's without-a-random-part arm at L (stored rows); whole_bL = whole before-L: the patch token set to h_S,l at block outputs 0..L; no_jpp_bL = without J++ before-L: set to h_S,l - P_J,l Delta_l (layer l's own 25 signed-OMP J++ atoms); rand_bL = random before-L: set to h_S,l - a random part of Delta_l of P_J,l Delta_l's share (seed 888 + l); whole_emb = descriptive: whole before-L with S's token at the patch token (47.4's (b)); window = descriptive (rule iii): the patch token and both bridges' fact sentences (O's and S's, K passage) set to S's states at block outputs 0..L; K reader, the first 50 fact-after passages.

Figure: x51_7_qwen3.5-9b.png

Figure: x51_7_qwen3.6-27b.png
