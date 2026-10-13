EXP exp02_swaps/main @ 15fc11d | model Qwen/Qwen3.6-27B@6a9e13bd | n=67 eligible items (of 90: {'eligible': 67, 'clean_wrong': 16, 'multi_token_answer': 7}) | band 32-48 | seeds: null 0, bootstrap 0
Gate gate_v3: full probe 27% at band 32-48 vs the 30% threshold: FAILED; main was run anyway on the human's call (see manifest deviations).
Claim tested: swapping the bridge for the swap target flips the answer through the J-space part of the bridge's representation (J-part swap flips, remainder swap with J-coordinates clamped does not).
Headline: flip rate J-part = 39% [28, 51]   remainder = 13% [7, 24]   remainder with J clamped = 3% [1, 10]
Paired differences (bootstrap B=2000): jpart - remainder = +25 pts [+13, +37]; remainder - remainder_clamped = +10 pts [+3, +19]
Baseline: full probe = 27% [18, 39]   raw J-lens = 51% [39, 62]
Control (matched-norm random direction): raw_jlens = 1% [0, 8]   full_probe = 0% [0, 5]   jpart = 0% [0, 5]   remainder = 0% [0, 5]   remainder_clamped = 1% [0, 8]
Labels (J-part flip x clamped-remainder flip): J-mediated 25, non-J 1, both 1, neither 40
Figures: figures/exp02_swaps/main/flip_rates.png
Three dumbest ways this could be wrong:
1) Any edit this large flips the answer. Checked: null flip rates above, with null edits larger than the real ones (median edit ratio null vs real: raw_jlens 0.056 vs 0.008, full_probe 0.160 vs 0.063, jpart 0.054 vs 0.014, remainder 0.169 vs 0.068, remainder_clamped 0.185 vs 0.079). Not matched in total dose: each layer's null edit is sized to what the clamp still needs on the null run's own state, and a random direction never achieves the swap, so it stays full-size at every band layer while the real swap carries forward and later edits shrink. So the null is stricter for flips and overstates collateral damage (null kept-clean raw_jlens 97% [90, 99], full_probe 67% [55, 77], jpart 99% [92, 100], remainder 72% [60, 81], remainder_clamped 64% [52, 75]).
2) The J-part vs remainder gap is a dose gap. Checked: median direct edit ratio |delta|/|h| at the final position raw_jlens 0.008, full_probe 0.063, jpart 0.014, remainder 0.068, remainder_clamped 0.079.
3) Flips come from breaking the computation, not from installing the target. Checked: share with neither answer at rank 1 raw_jlens 13%, full_probe 22%, jpart 9%, remainder 21%, remainder_clamped 15%; items with skipped (near-parallel) layers raw_jlens 0, full_probe 0, jpart 0, remainder 0, remainder_clamped 0.
Caveats: the band was picked by the gate on these same items. The remainder holds most of the probes' prompt noise (the J-part is 12-18% of probe variance; exp01_probes v2 -> v3, 6 -> 24 kept prompts per entity, cut probe norms by about a third), so a weak remainder swap partly reflects a noisier direction.
For the human to verify: results/exp02_swaps/main/labels.csv (one row per item; recompute each condition's flip rate as the mean of flip_<condition> over status == eligible) and outcomes.jsonl (ranks, top words).
Status: UNVERIFIED until a human adds it to VERIFIED.md
