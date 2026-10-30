# README drafts from Tier 0 (batch-45 brief, Dan 26 Oct ~18:30). Not merged.

Numbers are the template markers; docs/depth/x0_details.md ("Tier 0 of the batch-45 brief") renders them.

## T0.2: Section 1 and Fig. 1's subtitle

Section 1, after the first bullet:

- **The lookup is measurable only where the locker comes first:** it barely switches when the locker sentence comes after the pick ({{num|sbo_swap_after_lksw_27b}}-{{num|sbo_swap_after_lksw_9b}}), so its extra loss there rests on few switches. In locker-first scenes the gap is {{pt|sbo_swap_before_gap_122b}} to {{pt|sbo_swap_before_gap_muse}}, beside the pre-registered {{pt|contrast_122b}} to {{pt|contrast_muse}} over all scenes.

Small table (Section 1), replacing nothing:

| Gap, main test | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| All scenes (fixed in advance) | {{num|contrast_9b}} | {{num|contrast_27b}} | {{num|contrast_122b}} | {{num|contrast_muse}} |
| Locker before the pick (after the data) | {{num|sbo_swap_before_gap_9b}} | {{num|sbo_swap_before_gap_27b}} | {{num|sbo_swap_before_gap_122b}} | {{num|sbo_swap_before_gap_muse}} |

Fig. 1's subtitle, second line: "Main test, fixed in advance; the lookup switches mostly where the locker comes first (Fig. 3), so its extra loss rests on those scenes."

## T0.3: How we checked

- **Sampling instead of the top token.** With "switch" replaced by p_alt, the expected switch rate when sampling at T = 1, the main test's gap is {{pt|prob_gap_122b}} to {{pt|prob_gap_muse}} (switches: {{pt|contrast_122b}} to {{pt|contrast_muse}}).

## T0.4: shares of the change

Section 5's table header: "The part's share of the change (median over items)". Appendix line: "Every '% of the change' is the median over items of ‖PΔ‖² / ‖Δ‖²; the mean and the pooled ratio are in docs/depth/x0_details.md (9B identity removal: median {{num|share_median_jppalfid_9b}}, mean {{num|share_mean_jppalfid_9b}}, pooled {{num|share_pooled_jppalfid_9b}})."
