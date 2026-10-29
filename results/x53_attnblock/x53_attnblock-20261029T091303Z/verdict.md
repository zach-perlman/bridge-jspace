x53_attnblock (Lightning, L14; run nem35l_x53_attnblock); no prediction (Dan, 29 Oct ~10:05: the rule fixed then, before any run); UNVERIFIED

Rule (verbatim): "read through two blocks" if (iii) cuts the lookup's switches by >= 0.6 of the whole change's and (v) by <= 0.15; "one block" if (i) or (ii) alone cuts >= 0.6; "not through attention at the bridge" if (iv) cuts < 0.3 (the Mamba state carries it); else in between.
As computed: cut(x) = 1 - S_x / S_whole on the lookup, S_x = the share of items whose lookup switches under the whole change with arm x's block, S_whole = the same with no block (arm none), all in this run's forwards; point estimates decide, EPS 1e-09 at the bars ('< 0.3' strict). The clauses are checked in the rule's order and the first that holds is the label; any other clause that also holds is listed beside it (flagged for Dan: the rule does not say which wins). S_whole = 0: not tested. X0's validity (S_whole >= 0.30 and >= 30 items switched) is reported, not a gate (the rule has none).

Label (lookup): in between
Clauses: {"read through two blocks": false, "one block": false, "not through attention at the bridge": false}

Blocks: {"b19": [19], "b26": [26], "both": [19, 26], "after": [19, 26, 33, 42], "control": [19, 26]}; items 200 (37 bridge entities), the control's source before the bridge in 146

lookup: n 200, S_whole 0.440 (88 switched; X0-valid True), clean answer kept with no block 1.000
  (i) block 19 only: S 0.390, cut 0.114 [0.039, 0.189], clean kept 0.955, edges (median) 47
  (ii) block 26 only: S 0.380, cut 0.136 [0.060, 0.216], clean kept 0.910, edges (median) 47
  (iii) blocks 19 and 26: S 0.290, cut 0.341 [0.253, 0.420], clean kept 0.770, edges (median) 94
  (iv) every attention block after L: S 0.285, cut 0.352 [0.272, 0.423], clean kept 0.760, edges (median) 188
  (v) blocks 19 and 26, a random non-bridge token of the bridge's sentence as the source: S 0.440, cut 0.000 [-0.056, 0.054], clean kept 0.995, edges (median) 94
recall (beside): n 200, S_whole 0.955 (191 switched; X0-valid True), clean answer kept with no block 0.995
  (i) block 19 only: S 0.905, cut 0.052 [0.021, 0.083], clean kept 0.950, edges (median) 49
  (ii) block 26 only: S 0.905, cut 0.052 [0.014, 0.096], clean kept 0.970, edges (median) 49
  (iii) blocks 19 and 26: S 0.820, cut 0.141 [0.089, 0.199], clean kept 0.860, edges (median) 98
  (iv) every attention block after L: S 0.425, cut 0.555 [0.441, 0.647], clean kept 0.550, edges (median) 196
  (v) blocks 19 and 26, a random non-bridge token of the bridge's sentence as the source: S 0.950, cut 0.005 [-0.012, 0.022], clean kept 0.995, edges (median) 100

Whole change vs the conflict run's stored switch (descriptive): {"PP": {"agree": 0.98, "this_run": 88, "stored": 90, "n": 200}, "PM": {"agree": 0.98, "this_run": 191, "stored": 189, "n": 200}}

Examples (10 random items, seed 0; the lookup's top token under the whole change, '*' = switched):
- P2-L0-0037: sentence 'Carl picked hydrogen.', bridge ' hydrogen', control ' picked'; none '7', b19 '7', b26 '7', both '7', after '7', control '7'
- P2-L0-0165: sentence 'Paul picked the sheep.', bridge ' sheep', control '.'; none '3', b19 '3', b26 '3', both '3', after '3', control '3'
- P2-L0-0185: sentence ' James picked epsilon.', bridge ' epsilon', control ' James'; none '5'*, b19 '5'*, b26 '5'*, both '5'*, after '5'*, control '5'*
- P2-L0-0225: sentence ' Carl picked the rabbit.\n', bridge ' rabbit', control ' Carl'; none '3'*, b19 '3'*, b26 '3'*, both '3'*, after '3'*, control '3'*
- P2-L0-0235: sentence ' Sam picked lithium.', bridge ' lithium', control ' picked'; none '2', b19 '2', b26 '2', both '2', after '2', control '2'
- P2-L0-0247: sentence ' Clara picked hydrogen.', bridge ' hydrogen', control '.'; none '3', b19 '3', b26 '3', both '3', after '3', control '3'
- P2-L0-0274: sentence ' Julia picked oxygen.', bridge ' oxygen', control ' picked'; none '1', b19 '1', b26 '1', both '1', after '1', control '1'
- P2-L0-0284: sentence 'Kyle picked delta.', bridge ' delta', control 'K'; none '7', b19 '7', b26 '7', both '7', after '7', control '7'
- P2-L0-0295: sentence ' Tara picked helium.', bridge ' helium', control '.'; none '5', b19 '5', b26 '5', both '5', after '5', control '5'
- P2-L0-0443: sentence ' Leo picked delta.', bridge ' delta', control '.'; none '2'*, b19 '2'*, b26 '2'*, both '2'*, after '2'*, control '2'*
