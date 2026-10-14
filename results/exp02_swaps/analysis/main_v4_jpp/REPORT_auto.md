EXP exp02_swaps/main_v4_jpp @ 26fd2f7 | model Qwen/Qwen3.6-27B@6a9e13bd | n=77 eligible items (of 90: {'eligible': 77, 'clean_wrong': 13}) | band 24-40 | seeds: null 0, bootstrap 0
Gate gate_v4: full probe 27% at band 24-40 vs the 30% threshold: FAILED; main was run anyway on the human's call (see manifest deviations).
Claim tested: swapping the bridge for the swap target flips the answer through the J-space part of the bridge's representation (J-part swap flips, remainder swap with J-coordinates clamped does not).
Headline: flip rate J-part = 52% [41, 63]   remainder = 8% [4, 16]   remainder with J clamped = 1% [0, 7]
Paired differences (bootstrap B=2000): jpart - remainder = +44 pts [+32, +56]; remainder - remainder_clamped = +6 pts [+1, +13]
Baseline: full probe = 27% [19, 38]   raw J-lens = 49% [38, 60]
Control (matched-norm random direction): raw_jlens = 0% [0, 5]   full_probe = 1% [0, 7]   jpart = 0% [0, 5]   remainder = 1% [0, 7]   remainder_clamped = 0% [0, 5]
Labels (J-part flip x clamped-remainder flip): J-mediated 39, non-J 0, both 1, neither 37
Figures: figures/exp02_swaps/main_v4_jpp/flip_rates.png
Three dumbest ways this could be wrong:
1) Any edit this large flips the answer. Checked: null flip rates above, with null edits larger than the real ones (median edit ratio null vs real: raw_jlens 0.034 vs 0.009, full_probe 0.161 vs 0.074, jpart 0.044 vs 0.016, remainder 0.154 vs 0.078, remainder_clamped 0.179 vs 0.090). Not matched in total dose: each layer's null edit is sized to what the clamp still needs on the null run's own state, and a random direction never achieves the swap, so it stays full-size at every band layer while the real swap carries forward and later edits shrink. So the null is stricter for flips and overstates collateral damage (null kept-clean raw_jlens 97% [91, 99], full_probe 88% [79, 94], jpart 100% [95, 100], remainder 87% [78, 93], remainder_clamped 84% [75, 91]).
2) The J-part vs remainder gap is a dose gap. Checked: median direct edit ratio |delta|/|h| at the final position raw_jlens 0.009, full_probe 0.074, jpart 0.016, remainder 0.078, remainder_clamped 0.090.
3) Flips come from breaking the computation, not from installing the target. Checked: share with neither answer in the continuation raw_jlens 10%, full_probe 18%, jpart 9%, remainder 14%, remainder_clamped 12%; items with skipped (near-parallel) layers raw_jlens 0, full_probe 0, jpart 0, remainder 0, remainder_clamped 0.
Caveats: the band was picked by the gate on these same items. The remainder holds most of the probes' prompt noise (the J-part is a minority of probe variance; see the exp01 run's per-layer fve), so a weak remainder swap partly reflects a noisier direction.
For the human to verify: results/exp02_swaps/main_v4_jpp/labels.csv (one row per item; recompute each condition's flip rate as the mean of flip_<condition> over status == eligible) and outcomes.jsonl (ranks, top words).
Status: UNVERIFIED until a human adds it to VERIFIED.md
