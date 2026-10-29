x53_attnspan: the 53.4 follow-up on Lightning (L14; run nem35l_x53_attnspan); Batch 53, 53.4 follow-up (Dan 11:10); no prediction (Dan, 29 Oct ~10:05: the rule fixed then, before any run); UNVERIFIED

Rule (verbatim): "the pointer is read by attention after the Mamba state spreads it" if the span cuts the lookup's switches by >= 0.6 and the control by <= 0.15; else as 53.4.
53.4's rule (for "else as 53.4"): "read through two blocks" if (iii) cuts the lookup's switches by >= 0.6 of the whole change's and (v) by <= 0.15; "one block" if (i) or (ii) alone cuts >= 0.6; "not through attention at the bridge" if (iv) cuts < 0.3 (the Mamba state carries it); else in between.
As computed: cut(x) = 1 - S_x / S_whole on the lookup (53.4's), S_x = the share of the scenes kept whose lookup switches under the whole change with arm x's block, S_whole = the same with no block, all in this run's forwards; point estimates decide, EPS 1e-09 at the bars. "else as 53.4": 53.4's labels applied to the span arm: its (iv) clause "not through attention at the bridge" if the span cuts < 0.3 (the Mamba state carries it), else "in between" (the per-block clauses (i) / (ii) have no span arm). The span's destinations are every position after the scene's last token (knock_out needs disjoint sources and destinations, so attention inside the span is as is), the same for the control. the control span: as many tokens as the bridge-to-scene-end span, inside the scene before the bridge word (from the scene's first token to the token before the bridge word; never the bridge-to-end span, never the question, never position 0), its start drawn per scene among the starts that fit (random.Random('x53_attnspan|5348|<scene>')); a scene where no such span fits is dropped from the rule and counted (its span arm read beside); the destinations are the span arm's (every position after the scene's last token: the question and the read), so the two arms differ only in the keys blocked. S_whole = 0: not tested; X0's validity reported, not a gate. 53.4's (iii) and (v) from its committed verdict beside, and (iii) rerun here

Label (lookup): in between — decided on the 95 scenes where a control span fits (median span 10.0 tokens); 105 scenes without one (median span 31.0 tokens; the bridge word early) dropped from the rule. The span arm's cut: 0.527 [0.412, 0.627] on the 95, 0.413 [0.273, 0.542] on all 200 (median span 20.0 tokens), -0.056 [-0.875, 0.379] on the 105.

Scenes: 200 (53.4's); in the rule (a control span fits) 95 (35 bridge entities); dropped from the rule, no control fits: 105; span length (tokens, min / median / max) in the rule [2, 10, 21], all [2, 20, 39]

lookup (the rule's scenes): n 95, S_whole 0.779 (74 switched; X0-valid True), clean kept with no block 1.000
  (iii) of 53.4, rerun here: blocks 19 and 26, source = the bridge word: S 0.516, cut 0.338 [0.243, 0.427], clean kept 0.600 (collateral), edges (median) 74
  blocks 19 and 26: every position after the scene's last token cannot attend to any position from the bridge word through the scene's last token: S 0.368, cut 0.527 [0.412, 0.627], clean kept 0.474 (collateral), edges (median) 560
  the control: blocks 19 and 26, the same destinations, a source span of the same length inside the scene before the bridge word (seeded start): S 0.779, cut 0.000 [-0.039, 0.041], clean kept 1.000 (collateral), edges (median) 560
recall (beside) (the rule's scenes): n 95, S_whole 0.990 (94 switched; X0-valid True), clean kept with no block 1.000
  (iii) of 53.4, rerun here: blocks 19 and 26, source = the bridge word: S 0.832, cut 0.160 [0.089, 0.227], clean kept 0.779 (collateral), edges (median) 78
  blocks 19 and 26: every position after the scene's last token cannot attend to any position from the bridge word through the scene's last token: S 0.705, cut 0.287 [0.209, 0.363], clean kept 0.621 (collateral), edges (median) 580
  the control: blocks 19 and 26, the same destinations, a source span of the same length inside the scene before the bridge word (seeded start): S 1.000, cut -0.011 [-0.037, 0.000], clean kept 0.979 (collateral), edges (median) 580

Beside, the span and (iii) on every scene, and on the scenes without a control:
  all, lookup: n 200, S_whole 0.460; span cut 0.413 [0.273, 0.542], clean kept 0.585; (iii) cut 0.359 [0.274, 0.432]
  all, recall: n 200, S_whole 0.945; span cut 0.222 [0.162, 0.275], clean kept 0.685; (iii) cut 0.127 [0.077, 0.179]
  no control fits, lookup: n 105, S_whole 0.171; span cut -0.056 [-0.875, 0.379], clean kept 0.686; (iii) cut 0.444 [0.200, 0.733]
  no control fits, recall: n 105, S_whole 0.905; span cut 0.158 [0.081, 0.227], clean kept 0.743; (iii) cut 0.095 [0.038, 0.155]

Beside, 53.4's committed verdict (results/x53_attnblock/x53_attnblock-20261029T091303Z; label in between; n 200, S_whole 0.440): (iii) cut 0.341 [0.253, 0.420], clean kept 0.770; (v) cut 0.000 [-0.056, 0.054], clean kept 0.995

Examples (10 random scenes of the rule, seed 0; the lookup's top token under the whole change, '*' = switched):
- P2-L0-0030: span ' eagle. The locker of the bear is 6.\n'; control ' cat. The locker of the eagle is 7.'; none '2'*, both '6', span '6', span_ctrl '2'*
- P2-L0-0185: span ' epsilon. The locker of alpha is 6. Emma picked alpha. Fiona picked gamma.\n'; control 'The locker of gamma is 5. The locker of epsilon is 8. James picked'; none '5'*, both '5'*, span '8', span_ctrl '5'*
- P2-L0-0199: span ' nitrogen. Nina picked helium. The locker of nitrogen is 3.\n'; control '9. The locker of carbon is 5. Max picked carbon.'; none '3', both '3', span '3', span_ctrl '3'
- P2-L0-0226: span ' lithium.\n'; control ' is '; none '4'*, both '4'*, span '4'*, span_ctrl '4'*
- P2-L0-0252: span ' sheep. The locker of the butterfly is 3.\n'; control ' locker of the spider is 7. Rose picked the'; none '7'*, both '3', span '3', span_ctrl '7'*
- P2-L0-0257: span ' epsilon. The locker of delta is seven. The locker of epsilon is six.\n'; control 'The locker of theta is three. Sara picked delta. Finn picked theta. Carl'; none '6', both '6', span '6', span_ctrl '6'
- P2-L0-0263: span ' alpha. The locker of alpha is 2.\n'; control ' The locker of beta is 6. Eva picked'; none '6'*, both '2', span '6'*, span_ctrl '6'*
- P2-L0-0296: span ' epsilon. Tara picked alpha.\n'; control ' The locker of epsilon is seven'; none '9'*, both '9'*, span '7', span_ctrl '9'*
- P2-L0-0298: span ' hydrogen. The locker of helium is seven. Anna picked nitrogen.\n'; control ' locker of hydrogen is eight. Owen picked helium. The locker of'; none '5'*, both '5'*, span '5'*, span_ctrl '5'*
- P2-L0-0326: span ' beta. The locker of epsilon is one.\n'; control ' picked delta. The locker of delta is nine'; none '1'*, both '1'*, span '5', span_ctrl '1'*
