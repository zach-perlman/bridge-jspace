EXP exp02_swaps/main_v4_jlens_32-48 @ 26fd2f7 | model Qwen/Qwen3.6-27B@6a9e13bd | n=77 eligible items (of 90: {'eligible': 77, 'clean_wrong': 13}) | band 32-48 | seeds: null 0, bootstrap 0
Gate gate_v4: full probe 27% at band 24-40 vs the 30% threshold: FAILED; main was run anyway on the human's call (see manifest deviations).
Claim tested: swapping the bridge for the swap target flips the answer through the J-space part of the bridge's representation (J-part swap flips, remainder swap with J-coordinates clamped does not).
Headline: flip rate J-part = 34% [24, 45]   remainder = 12% [6, 21]   remainder with J clamped = 1% [0, 7]
Paired differences (bootstrap B=2000): jpart - remainder = +22 pts [+12, +32]; remainder - remainder_clamped = +10 pts [+4, +18]
Baseline: full probe = 25% [16, 35]   raw J-lens = 48% [37, 59]
Control (matched-norm random direction): raw_jlens = 1% [0, 7]   full_probe = 0% [0, 5]   jpart = 0% [0, 5]   remainder = 3% [1, 9]   remainder_clamped = 3% [1, 9]
Labels (J-part flip x clamped-remainder flip): J-mediated 25, non-J 0, both 1, neither 51
Figures: figures/exp02_swaps/main_v4_jlens_32-48/flip_rates.png
Three dumbest ways this could be wrong:
1) Any edit this large flips the answer. Checked: null flip rates above, with null edits larger than the real ones (median edit ratio null vs real: raw_jlens 0.056 vs 0.008, full_probe 0.167 vs 0.064, jpart 0.058 vs 0.014, remainder 0.175 vs 0.070, remainder_clamped 0.173 vs 0.081). Not matched in total dose: each layer's null edit is sized to what the clamp still needs on the null run's own state, and a random direction never achieves the swap, so it stays full-size at every band layer while the real swap carries forward and later edits shrink. So the null is stricter for flips and overstates collateral damage (null kept-clean raw_jlens 99% [93, 100], full_probe 74% [63, 83], jpart 99% [93, 100], remainder 75% [65, 84], remainder_clamped 68% [56, 77]).
2) The J-part vs remainder gap is a dose gap. Checked: median direct edit ratio |delta|/|h| at the final position raw_jlens 0.008, full_probe 0.064, jpart 0.014, remainder 0.070, remainder_clamped 0.081.
3) Flips come from breaking the computation, not from installing the target. Checked: share with neither answer in the continuation raw_jlens 10%, full_probe 18%, jpart 9%, remainder 14%, remainder_clamped 8%; items with skipped (near-parallel) layers raw_jlens 0, full_probe 0, jpart 0, remainder 0, remainder_clamped 0.
Caveats: the band was set by the human, not the gate's pick (24-40). The remainder holds most of the probes' prompt noise (the J-part is a minority of probe variance; see the exp01 run's per-layer fve), so a weak remainder swap partly reflects a noisier direction.
For the human to verify: results/exp02_swaps/main_v4_jlens_32-48/labels.csv (one row per item; recompute each condition's flip rate as the mean of flip_<condition> over status == eligible) and outcomes.jsonl (ranks, top words).
Status: UNVERIFIED until a human adds it to VERIFIED.md
