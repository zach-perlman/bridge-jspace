EXP exp02_swaps/main_v4_jpp_pos-last_two @ 1616fe0 | model Qwen/Qwen3.6-27B@6a9e13bd | n=77 eligible items (of 90: {'eligible': 77, 'clean_wrong': 13}) | band 24-40 | seeds: null 0, bootstrap 0
Gate gate_v4: full probe 27% at band 24-40 vs the 30% threshold: FAILED; main was run anyway on the human's call (see manifest deviations).
Claim tested: swapping the bridge for the swap target flips the answer through the J-space part of the bridge's representation (J-part swap flips, remainder swap with J-coordinates clamped does not).
Headline: flip rate J-part = 17% [10, 27]   remainder = 1% [0, 7]   remainder with J clamped = 1% [0, 7]
Paired differences (bootstrap B=2000): jpart - remainder = +16 pts [+8, +23]; remainder - remainder_clamped = +0 pts [+0, +0]
Baseline: full probe = 17% [10, 27]   raw J-lens = 16% [9, 25]
Control (matched-norm random direction): raw_jlens = 0% [0, 5]   full_probe = 1% [0, 7]   jpart = 0% [0, 5]   remainder = 1% [0, 7]   remainder_clamped = 1% [0, 7]
Labels (J-part flip x clamped-remainder flip): J-mediated 12, non-J 0, both 1, neither 64
Figures: figures/exp02_swaps/main_v4_jpp_pos-last_two/flip_rates.png
Three dumbest ways this could be wrong:
1) Any edit this large flips the answer. Checked: null flip rates above, with null edits larger than the real ones (median edit ratio null vs real: raw_jlens 0.035 vs 0.010, full_probe 0.154 vs 0.073, jpart 0.043 vs 0.017, remainder 0.151 vs 0.077, remainder_clamped 0.171 vs 0.090). Not matched in total dose: each layer's null edit is sized to what the clamp still needs on the null run's own state, and a random direction never achieves the swap, so it stays full-size at every band layer while the real swap carries forward and later edits shrink. So the null is stricter for flips and overstates collateral damage (null kept-clean raw_jlens 100% [95, 100], full_probe 94% [86, 97], jpart 100% [95, 100], remainder 91% [82, 96], remainder_clamped 88% [79, 94]).
2) The J-part vs remainder gap is a dose gap. Checked: median direct edit ratio |delta|/|h| at the final position raw_jlens 0.010, full_probe 0.073, jpart 0.017, remainder 0.077, remainder_clamped 0.090.
3) Flips come from breaking the computation, not from installing the target. Checked: share with neither answer in the continuation raw_jlens 3%, full_probe 6%, jpart 4%, remainder 8%, remainder_clamped 6%; items with skipped (near-parallel) layers raw_jlens 0, full_probe 0, jpart 0, remainder 0, remainder_clamped 0.
Caveats: the band was picked by the gate on these same items. The remainder holds most of the probes' prompt noise (the J-part is a minority of probe variance; see the exp01 run's per-layer fve), so a weak remainder swap partly reflects a noisier direction.
For the human to verify: results/exp02_swaps/main_v4_jpp_pos-last_two/labels.csv (one row per item; recompute each condition's flip rate as the mean of flip_<condition> over status == eligible) and outcomes.jsonl (ranks, top words).
Status: UNVERIFIED until a human adds it to VERIFIED.md
