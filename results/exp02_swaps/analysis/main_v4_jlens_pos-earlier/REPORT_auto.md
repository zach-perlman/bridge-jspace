EXP exp02_swaps/main_v4_jlens_pos-earlier @ 1616fe0 | model Qwen/Qwen3.6-27B@6a9e13bd | n=77 eligible items (of 90: {'eligible': 77, 'clean_wrong': 13}) | band 24-40 | seeds: null 0, bootstrap 0
Gate gate_v4: full probe 27% at band 24-40 vs the 30% threshold: FAILED; main was run anyway on the human's call (see manifest deviations).
Claim tested: swapping the bridge for the swap target flips the answer through the J-space part of the bridge's representation (J-part swap flips, remainder swap with J-coordinates clamped does not).
Headline: flip rate J-part = 23% [15, 34]   remainder = 4% [1, 11]   remainder with J clamped = 3% [1, 9]
Paired differences (bootstrap B=2000): jpart - remainder = +19 pts [+9, +30]; remainder - remainder_clamped = +1 pts [+0, +4]
Baseline: full probe = 16% [9, 25]   raw J-lens = 26% [17, 37]
Control (matched-norm random direction): raw_jlens = 0% [0, 5]   full_probe = 1% [0, 7]   jpart = 0% [0, 5]   remainder = 1% [0, 7]   remainder_clamped = 3% [1, 9]
Labels (J-part flip x clamped-remainder flip): J-mediated 18, non-J 2, both 0, neither 57
Figures: figures/exp02_swaps/main_v4_jlens_pos-earlier/flip_rates.png
Three dumbest ways this could be wrong:
1) Any edit this large flips the answer. Checked: null flip rates above, with null edits larger than the real ones (median edit ratio null vs real: raw_jlens 0.042 vs 0.008, full_probe 0.144 vs 0.064, jpart 0.038 vs 0.015, remainder 0.145 vs 0.067, remainder_clamped 0.159 vs 0.074). Not matched in total dose: each layer's null edit is sized to what the clamp still needs on the null run's own state, and a random direction never achieves the swap, so it stays full-size at every band layer while the real swap carries forward and later edits shrink. So the null is stricter for flips and overstates collateral damage (null kept-clean raw_jlens 97% [91, 99], full_probe 94% [86, 97], jpart 97% [91, 99], remainder 92% [84, 96], remainder_clamped 91% [82, 96]).
2) The J-part vs remainder gap is a dose gap. Checked: median direct edit ratio |delta|/|h| at the final position raw_jlens 0.008, full_probe 0.064, jpart 0.015, remainder 0.067, remainder_clamped 0.074.
3) Flips come from breaking the computation, not from installing the target. Checked: share with neither answer in the continuation raw_jlens 4%, full_probe 9%, jpart 3%, remainder 9%, remainder_clamped 5%; items with skipped (near-parallel) layers raw_jlens 0, full_probe 0, jpart 0, remainder 0, remainder_clamped 0.
Caveats: the band was picked by the gate on these same items. The remainder holds most of the probes' prompt noise (the J-part is a minority of probe variance; see the exp01 run's per-layer fve), so a weak remainder swap partly reflects a noisier direction.
For the human to verify: results/exp02_swaps/main_v4_jlens_pos-earlier/labels.csv (one row per item; recompute each condition's flip rate as the mean of flip_<condition> over status == eligible) and outcomes.jsonl (ranks, top words).
Status: UNVERIFIED until a human adds it to VERIFIED.md
