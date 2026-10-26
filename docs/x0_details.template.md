# X0 in detail

The README gives the summary; this page holds the tables behind it. Every number is recomputed from the run files by `scripts/x0_details.py`, and every number is unverified. Design and log: [jobs/c3/X0.md](../jobs/c3/X0.md). Run folders: [results/x0_necessity/](../results/x0_necessity/).

**Terms.** "Excess" here is the README's "extra loss": the J-dependence (the share of the whole edit's flips lost when a part is removed) minus that of a random subspace of the same share of ‖Δ‖².

**Labels**, per reader and layer:
- around: excess ≤ 0.10, upper CI ≤ 0.20;
- through: J-dependence ≥ 0.30 and excess ≥ 0.20, lower CI ≥ 0.10;
- mixed: the rest;
- can't tell: the whole edit flips < 30% or < 30 items.

CIs are 95%, from a cluster bootstrap over bridge entities (10,000 resamples).

![Overview: excess by layer, two models, three prompt formats](../figures/x0_necessity/overview.png)

## Every layer (chat, the bridge's word, J++ at 25 atoms)

Qwen3.5-9B (n = {{num|n_9b}} scenes, {{num|ents_9b}} bridge entities; pre-registered layer {{num|layer_9b}}):

{{tbl|layers_9b}}

Qwen3.6-27B (n = {{num|n_27b}} scenes, {{num|ents_27b}} bridge entities; pre-registered layer {{num|layer_27b}}):

{{tbl|layers_27b}}

Qwen3.5-122B-A10B (n = {{num|n_122b}} scenes, {{num|ents_122b}} bridge entities; pre-registered layer {{num|layer_122b}}; FP8 weights, mixture of experts, J++ fitted on the bf16 weights, 2x H100, hardware gate 0.998):

{{tbl|layers_122b}}

![27B detail](../figures/x0_necessity/detail_x0_necessity_27b_chat_chat.png)
![9B detail](../figures/x0_necessity/detail_qwen35_9b_x0_necessity_chat.png)

## Every dictionary and number of atoms (the pre-registered layer; added after the data)

Each dictionary's part is set against a random subspace of its own share. These come from the k-match runs, which recompute the X0 items.

Qwen3.5-9B, layer {{num|layer_9b}}:

{{tbl|dicts_9b}}

Qwen3.6-27B, layer {{num|layer_27b}}:

{{tbl|dicts_27b}}

Qwen3.5-122B, layer {{num|layer_122b}} (from its X0 run: J++ at 25 / 50 / 100 atoms; W_U, W_E and random atoms at 25 only; J++ over every token and the digit directions):

{{tbl|dicts_122b}}

![Equal removed share](../figures/x0_necessity/kmatch.png)
![Excess against the number of atoms](../figures/x0_necessity/kcurve.png)
![Share against J-dependence](../figures/x0_necessity/share.png)

On the 27B, the lookup's J-dependence tracks, across layers, the share of ‖Δ‖² that J++ takes (Spearman {{num|share_rho_27b}}). The recall's does not.

## Subsets (the pre-registered layer; added after the data)

- **Upstream change.** The alt swaps two people's picks. Where the other changed pick comes first, Δ at the asked word also carries that change. On the 27B:
  - with the upstream change (n = {{num|lk_n_up_27b}}), lookups flip {{num|lk_swhole_up_27b}}, excess {{num|lk_excess_up_27b}};
  - asked first (n = {{num|lk_n_af_27b}}), lookups flip {{num|lk_swhole_af_27b}}, excess {{num|lk_excess_af_27b}}, too few flips to measure.
- **Sentence order.** The whole edit flips lookups {{num|lk_order_before_9b}} vs {{num|lk_order_after_9b}} (9B) and {{num|lk_order_before_27b}} vs {{num|lk_order_after_27b}} (27B), with the locker sentence before vs after the pick sentence.

Qwen3.5-9B:

{{tbl|strata_9b}}

Qwen3.6-27B:

{{tbl|strata_27b}}

Qwen3.5-122B:

{{tbl|strata_122b}}

![Upstream change](../figures/x0_necessity/asked_first.png)

## The digit check (the pre-registered layer; added after the data)

The question: the J++ dictionary has letter-bearing tokens only. Does the lookup read the answer digit at the bridge's word, which no letter-only dictionary can remove?
- The pre-stated reading (Dan, before the run): if J++ over every token, or the 10 digit directions alone, makes the lookup "through" in locker-before items, X0's "around" was the excluded digit.
- The reference: letter-only J++ at the same number of atoms.
- Result: the digits change nothing. The J++ readout at the bridge's word ranks the lookup's answer digit first in {{num|dig_readout_first_before_9b}} (9B) and {{num|dig_readout_first_before_27b}} (27B) of locker-before items, against a chance of 10%.

Qwen3.5-9B, layer 12:

{{tbl|digit_9b}}

Qwen3.6-27B, layer 32:

{{tbl|digit_27b}}

Qwen3.5-122B, layer {{num|layer_122b}} (its X0 run; the readout ranks the answer digit first in {{num|dig_readout_first_before_122b}} of locker-before items):

{{tbl|digit_122b}}

![The digit check](../figures/status_2026-10-24/f6_digits.png)

## The J++ atoms of the bridge edit (27B, layer 32, 20 random items; added after the data)

- The first atom is the bridge's own token (before or after the edit) in {{num|atoms_first_bridge_letters}} items.
- Over all 40 items (random and asked-first), the bridge's own tokens are among the top 25 atoms in {{num|atoms_bridge_top25_letters}} and carry a median {{num|atoms_bridge_coef2_letters}} of the part's Σcoef²: the J++ part is mostly not the bridge word (Dan's audit, 24 Oct ~19:30). Ranks 26-100 hold no bridge, name, digit or context token.
- The rest of the top 25 are mostly tokens that are neither context words nor names. Some of them are the bridge in other scripts (フライ for *fly*, 小熊 for *bear*).
- Digits never enter the top 25, even when every token is allowed ({{num|atoms_digit_top25_all}}). Number words enter {{num|atoms_number_word_top25_all}}.

Tables: [letter atoms](../results/x0_atoms/x0_atoms_27b_letters/tables.md), [every token](../results/x0_atoms/x0_atoms_27b_all/tables.md).

## The 23 Oct context cell on the fresh scenes (a replication; not part of X0's rule)

27B at layer 32, with the change at every context position, using the 23 Oct code, filter and read (n = {{num|ctx_n}} per reader):
- lookups flip {{num|ctx_lookup_full}} with the whole change and {{num|ctx_lookup_noj}} without the J++ part;
- recalls flip {{num|ctx_recall_full}} → {{num|ctx_recall_noj}}, a loss of {{num|ctx_recall_drop}} points, against {{num|ctx_recall_droprand}} for a random part. The difference is {{num|ctx_recall_diff}} (shares).

[Verdict](../results/d1_verdict/x0_ctx_parts_27b_20261024-144050/verdict.md).

## The first-mention table (README Section 5 keeps four rows)

J++ extra loss by whether the asked pick is the bridge's first mention (no = matched), after the data; italics: under 30 lookup switches (count shown); n: items per row; the 122B's fresh scenes at gate 0.75.

| Swap | First mention? | 9b lookup | 9b recall | 9b n | 27b lookup | 27b recall | 27b n | 122b lookup | 122b recall | 122b n | muse lookup | muse recall | muse n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Two people swap picks | yes | {{num|comp_two_fmyes_lk_cell_9b}} | {{num|comp_two_fmyes_rc_9b}} | {{num|comp_two_fmyes_n_9b}} | {{num|comp_two_fmyes_lk_cell_27b}} | {{num|comp_two_fmyes_rc_27b}} | {{num|comp_two_fmyes_n_27b}} | {{num|comp_two_fmyes_lk_cell_122b}} | {{num|comp_two_fmyes_rc_122b}} | {{num|comp_two_fmyes_n_122b}} | {{num|comp_two_fmyes_lk_cell_muse}} | {{num|comp_two_fmyes_rc_muse}} | {{num|comp_two_fmyes_n_muse}} |
| Two people swap picks | no | {{num|comp_two_fmno_lk_cell_9b}} | {{num|comp_two_fmno_rc_9b}} | {{num|comp_two_fmno_n_9b}} | {{num|comp_two_fmno_lk_cell_27b}} | {{num|comp_two_fmno_rc_27b}} | {{num|comp_two_fmno_n_27b}} | {{num|comp_two_fmno_lk_cell_122b}} | {{num|comp_two_fmno_rc_122b}} | {{num|comp_two_fmno_n_122b}} | {{num|comp_two_fmno_lk_cell_muse}} | {{num|comp_two_fmno_rc_muse}} | {{num|comp_two_fmno_n_muse}} |
| Only the asked person's pick changes | yes | {{num|comp_one_fmyes_lk_cell_9b}} | {{num|comp_one_fmyes_rc_9b}} | {{num|comp_one_fmyes_n_9b}} | {{num|comp_one_fmyes_lk_cell_27b}} | {{num|comp_one_fmyes_rc_27b}} | {{num|comp_one_fmyes_n_27b}} | {{num|comp_one_fmyes_lk_cell_122b}} | {{num|comp_one_fmyes_rc_122b}} | {{num|comp_one_fmyes_n_122b}} | {{num|comp_one_fmyes_lk_cell_muse}} | {{num|comp_one_fmyes_rc_muse}} | {{num|comp_one_fmyes_n_muse}} |
| Only the asked person's pick changes | no | {{num|comp_one_fmno_lk_cell_9b}} | {{num|comp_one_fmno_rc_9b}} | {{num|comp_one_fmno_n_9b}} | {{num|comp_one_fmno_lk_cell_27b}} | {{num|comp_one_fmno_rc_27b}} | {{num|comp_one_fmno_n_27b}} | {{num|comp_one_fmno_lk_cell_122b}} | {{num|comp_one_fmno_rc_122b}} | {{num|comp_one_fmno_n_122b}} | {{num|comp_one_fmno_lk_cell_muse}} | {{num|comp_one_fmno_rc_muse}} | {{num|comp_one_fmno_n_muse}} |
| Same, fresh scenes | no | {{num|comp_rep_fmno_lk_cell_9b}} | {{num|comp_rep_fmno_rc_9b}} | {{num|comp_rep_fmno_n_9b}} | {{num|comp_rep_fmno_lk_cell_27b}} | {{num|comp_rep_fmno_rc_27b}} | {{num|comp_rep_fmno_n_27b}} | {{num|comp_rep_fmno_lk_cell_122b}} | {{num|comp_rep_fmno_rc_122b}} | {{num|comp_rep_fmno_n_122b}} | {{num|comp_rep_fmno_lk_cell_muse}} | {{num|comp_rep_fmno_rc_muse}} | {{num|comp_rep_fmno_n_muse}} |

## Tables moved from the README (README v4, Dan 26 Oct ~16:45)

°: after the data, the gate lowered to 0.75. ‡: the lookup switches in only {{num|nat_lk_whole_sw_muse}} of {{num|nat_n_muse}} passages; recall {{num|nat_rc_excess_muse}}, lookup {{num|nat_lk_excess_muse}}.

**The split in every setting.**

| Gap | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| Two people swap picks (fixed in advance) | {{num|contrast_9b}} | {{num|contrast_27b}} | {{num|contrast_122b}} | {{num|contrast_muse}} |
| Only the asked person's pick changes | {{num|single_contrast_9b}} | {{num|single_contrast_27b}} | {{num|single_contrast_122b}} | {{num|single_contrast_muse}} |
| Matched: fresh scenes, both locker sentences first, only the asked pick changes | {{num|comp_rep_both_gap_9b}} | {{num|comp_rep_both_gap_27b}} | {{num|comp_rep_both_gap_122b}}° | {{num|comp_rep_both_gap_muse}} |
| Varied scenes | {{num|x0b_c_9b}} | {{num|x0b_c_27b}} | {{num|x0b_c_122b}} | {{num|x0b_c_muse}} |
| Natural passages | {{num|natg75_gap_9b}}° | {{num|nat_gap_27b}} | {{num|nat_gap_122b}} | not measurable‡ |
| More J++ directions removed, 100: gap (27B: lookup's extra loss at 25 / 50 / 100) | {{num|contrast_k100_9b}} | {{num|lk_excess_k25_27b}} / {{num|lk_excess_k50_27b}} / {{num|lk_excess_k100_27b}} | {{num|contrast_k100_122b}} | {{num|contrast_k100_muse}} |
| Logit difference: gap | {{num|ld_gap_9b}} | {{num|ld_gap_27b}} | {{num|ld_gap_122b}} | {{num|ld_gap_muse}} |
| Logit difference (lookup / recall extra loss) | {{num|ld_lk_9b}} / {{num|ld_rc_9b}} | {{num|ld_lk_27b}} / {{num|ld_rc_27b}} | {{num|ld_lk_122b}} / {{num|ld_rc_122b}} | {{num|ld_lk_muse}} / {{num|ld_rc_muse}} |

**The pointer: removed, added alone, written.**

| Pointer directions | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B° | Muse Glimmer 30B |
|---|---|---|---|---|
| Lookup's extra loss without them | {{num|rep_alf_lk_excess_9b}} (replicated) | {{num|mmlf_Alf_lk_excess_27b}} | {{num|mmlf_Alf_lk_excess_122b}} | {{num|rep_alf_lk_excess_muse}} (replicated) |
| Position without them / without a random part of their size | {{num|rt_C2_no_alf_position_9b}} / {{num|rt_C2_no_alf_rand_position_9b}} | {{num|rt_C2_no_alf_position_27b}} / {{num|rt_C2_no_alf_rand_position_27b}} | {{num|rtg_C2_no_alf_position_122b}} / {{num|rtg_C2_no_alf_rand_position_122b}} | {{num|rt_C2_no_alf_position_muse}} / {{num|rt_C2_no_alf_rand_position_muse}} |
| Position with only their part / only a random part of its size | {{num|rtk_C2_keep_alf_position_9b}} / {{num|rtk_C2_keep_alf_rand_position_9b}} | {{num|rtk_C2_keep_alf_position_27b}} / {{num|rtk_C2_keep_alf_rand_position_27b}} | {{num|rtk_C2_keep_alf_position_122b}} / {{num|rtk_C2_keep_alf_rand_position_122b}} | {{num|rtk_C2_keep_alf_position_muse}} / {{num|rtk_C2_keep_alf_rand_position_muse}} |
| Write, lookup's target share: s = 1 / 2 / 4; random direction, 4 | {{num|x8_t1_9b}} / {{num|x8_t2_9b}} / {{num|x8_t4_9b}}; {{num|x8_rand4_9b}} | {{num|x8_t1_27b}} / {{num|x8_t2_27b}} / {{num|x8_t4_27b}}; {{num|x8_rand4_27b}} | {{num|x8_t1_122b}} / {{num|x8_t2_122b}} / {{num|x8_t4_122b}}; {{num|x8_rand4_122b}} | {{num|x8_t1_muse}} / {{num|x8_t2_muse}} / {{num|x8_t4_muse}}; {{num|x8_rand4_muse}} |
| Write at s = 4: changed recalls giving the target slot's item | {{num|x8_rc_target_9b}} | {{num|x8_rc_target_27b}} | {{num|x8_rc_target_122b}} | {{num|x8_rc_target_muse}} |

**How far the pointer reaches.**

| Pointer directions | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| Lookup's extra loss without them, by what the first sentence names: the bridge in its locker sentence / the bridge in a pick sentence / another item | {{num|fs_named_9b}} | {{num|fs_named_27b}} | {{num|fs_named_122b}} | {{num|fs_named_muse}} |
| Same, by locker sentence: first sentence / first locker, not first / neither | {{num|fs_groups_9b}} | {{num|fs_groups_27b}} | {{num|fs_groups_122b}} | {{num|fs_groups_muse}} |
| Same, first sentence minus the rest | {{num|fs_diff_9b}} | {{num|fs_diff_27b}} | {{num|fs_diff_122b}} | {{num|fs_diff_muse}} |
| Neutral sentence before the first locker / before the first pick: the code's shift (B1 / B2) | {{num|x8_order_b1_9b}} / {{num|x8_order_b2_9b}} | {{num|x8_order_b1_27b}} / {{num|x8_order_b2_27b}} | {{num|x8_order_b1_122b}}° / {{num|x8_order_b2_122b}}° | {{num|x8_order_b1_muse}} / {{num|x8_order_b2_muse}} |
| Routes, only their part: moves from or to slot 0 / 1 → 2 and 2 → 1 | {{num|pm_keep_slot0_9b}} / {{num|pm_keep_12_9b}} | {{num|pm_keep_slot0_27b}} / {{num|pm_keep_12_27b}} | {{num|pm_keep_slot0_122b}} / {{num|pm_keep_12_122b}} | {{num|pm_keep_slot0_muse}} / {{num|pm_keep_12_muse}} |
| Routes, the whole change: 1 → 2 / 2 → 1 | {{num|pm_whole_12_9b}} | {{num|pm_whole_12_27b}} | {{num|pm_whole_12_122b}} | {{num|pm_whole_12_muse}} |
| Varied scenes, lookup's extra loss without them | {{num|tptr_pooled_9b}} | {{num|tptr_pooled_27b}} | {{num|tptr_pooled_122b}} | {{num|tptr_pooled_muse}} |
| Same: prose / json / table | {{num|tptr_split_9b}} | {{num|tptr_split_27b}} | {{num|tptr_split_122b}} | {{num|tptr_split_muse}} |
| Natural passages (the fact before the bridge) | {{num|tptr_natural_9b}} | {{num|tptr_natural_27b}} | {{num|tptr_natural_122b}} | {{num|tptr_natural_muse}} |
| Sanity swap, both removed minus the pointer alone | {{num|rtb_ex_C0_both_minus_alf_lk_9b}} | {{num|rtb_ex_C0_both_minus_alf_lk_27b}} | {{num|rtb_ex_C0_both_minus_alf_lk_122b}}° | {{num|rtb_ex_C0_both_minus_alf_lk_muse}} |
| Lookups still switching: J++ and the pointer removed | {{num|rtc_left_C0_alf_jpp_lk_9b}} | {{num|rtc_left_C0_alf_jpp_lk_27b}} | {{num|rtc_left_C0_alf_jpp_lk_122b}}° | {{num|rtc_left_C0_alf_jpp_lk_muse}} |
| Same, with identity outside J++ / its random part | {{num|rtd_left_C0_jpp+alf+idout_lk_9b}} / {{num|rtd_randleft_C0_jpp+alf+idout_lk_9b}} | {{num|rtd_left_C0_jpp+alf+idout_lk_27b}} / {{num|rtd_randleft_C0_jpp+alf+idout_lk_27b}} | not in this test | {{num|rtd_left_C0_jpp+alf+idout_lk_muse}} / {{num|rtd_randleft_C0_jpp+alf+idout_lk_muse}} |
| Recall's extra loss without identity | {{num|rtd_ex_C0_id_rc_9b}} | {{num|rtd_ex_C0_id_rc_27b}} | not in this test | {{num|rtd_ex_C0_id_rc_muse}} |
| Switches lost: pointer + J++ minus pointer + random | {{num|rtc_lost_C0_jpp_minus_rand_lk_9b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_27b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_122b}}° | {{num|rtc_lost_C0_jpp_minus_rand_lk_muse}} |

**Depth: the early layer.**

| Early layer, another item moved | Qwen3.5-9B (L6) | Qwen3.6-27B (L16) | Qwen3.5-122B (L27)° | Muse Glimmer 30B (L13) |
|---|---|---|---|---|
| Identity share | {{num|rte_C2_whole_identity_9b}} | {{num|rte_C2_whole_identity_27b}} | {{num|rte_C2_whole_identity_122b}} | {{num|rte_C2_whole_identity_muse}} |
| Without J++: the original answer | {{num|rte_C2_no_jpp_original_9b}} | {{num|rte_C2_no_jpp_original_27b}} | {{num|rte_C2_no_jpp_original_122b}} | {{num|rte_C2_no_jpp_original_muse}} |

## Tier 0 of the batch-45 brief (Dan, 26 Oct ~18:30; after the data, descriptive)

**Shares of the change.** Every "% of the change" in the README is the median over items of ‖PΔ‖² / ‖Δ‖². For the 9B's J++ + pointer + identity outside J++ (sanity swap) that is {{num|share_median_jppalfid_9b}}; the mean of the per-item ratios is {{num|share_mean_jppalfid_9b}} and the pooled ratio (Σ‖PΔ‖² / Σ‖Δ‖²) {{num|share_pooled_jppalfid_9b}} (27B {{num|share_median_jppalfid_27b}} / {{num|share_mean_jppalfid_27b}} / {{num|share_pooled_jppalfid_27b}}; Muse {{num|share_median_jppalfid_muse}} / {{num|share_mean_jppalfid_muse}} / {{num|share_pooled_jppalfid_muse}}).

**The split by sentence order** (main test; [split_by_order.md](split_by_order.md) has every design). The lookup's extra loss is a share of the lookups the whole change switches, so it is measurable only where the locker sentence comes before the pick.

| Main test | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| Gap, all scenes (fixed in advance) | {{num|sbo_swap_all_gap_9b}} | {{num|sbo_swap_all_gap_27b}} | {{num|sbo_swap_all_gap_122b}} | {{num|sbo_swap_all_gap_muse}} |
| Gap, locker before the pick | {{num|sbo_swap_before_gap_9b}} | {{num|sbo_swap_before_gap_27b}} | {{num|sbo_swap_before_gap_122b}} | {{num|sbo_swap_before_gap_muse}} |
| Gap, locker after the pick | {{num|sbo_swap_after_gap_9b}} | {{num|sbo_swap_after_gap_27b}} | {{num|sbo_swap_after_gap_122b}} | {{num|sbo_swap_after_gap_muse}} |
| Lookups switched: before / after | {{num|sbo_swap_before_lksw_9b}} / {{num|sbo_swap_after_lksw_9b}} | {{num|sbo_swap_before_lksw_27b}} / {{num|sbo_swap_after_lksw_27b}} | {{num|sbo_swap_before_lksw_122b}} / {{num|sbo_swap_after_lksw_122b}} | {{num|sbo_swap_before_lksw_muse}} / {{num|sbo_swap_after_lksw_muse}} |

**The switch as a probability** (the TA's sampling question): with "switch" replaced by p_alt, the expected switch rate when sampling at T = 1, the main test's gap is {{num|prob_gap_9b}} (9B), {{num|prob_gap_27b}} (27B), {{num|prob_gap_122b}} (122B), {{num|prob_gap_muse}} (Muse); lookup {{num|prob_lk_9b}} / {{num|prob_lk_27b}} / {{num|prob_lk_122b}} / {{num|prob_lk_muse}}, recall {{num|prob_rc_9b}} / {{num|prob_rc_27b}} / {{num|prob_rc_122b}} / {{num|prob_rc_muse}}.

## Writing between the second and third locker (batch 45c; after the data, descriptive)

A strong write can switch on a route the model does not use at its natural size; the removal and keep-only arms say the real change carries little of it (Q45.6: the pair of directions found from second-vs-third moves halves position on none of the three models, and only it gives position in under 0.15 of scenes). The write adds a fixed vector, μ of the target locker minus μ of the bridge's, at the bridge word; the dose is in units of a real pointer change. Share of writes whose lookup answers the written locker (n: writes per pair).

| Write, second ↔ third locker | Qwen3.5-9B: 1 → 2 / 2 → 1 | Qwen3.6-27B: 1 → 2 / 2 → 1 | Muse Glimmer 30B: 1 → 2 / 2 → 1 |
|---|---|---|---|
| dose 1 | {{num|x45c_write_12_1_9b}} / {{num|x45c_write_21_1_9b}} | {{num|x45c_write_12_1_27b}} / {{num|x45c_write_21_1_27b}} | {{num|x45c_write_12_1_muse}} / {{num|x45c_write_21_1_muse}} |
| dose 2 | {{num|x45c_write_12_2_9b}} / {{num|x45c_write_21_2_9b}} | {{num|x45c_write_12_2_27b}} / {{num|x45c_write_21_2_27b}} | {{num|x45c_write_12_2_muse}} / {{num|x45c_write_21_2_muse}} |
| dose 3 | {{num|x45c_write_12_3_9b}} / {{num|x45c_write_21_3_9b}} | {{num|x45c_write_12_3_27b}} / {{num|x45c_write_21_3_27b}} | {{num|x45c_write_12_3_muse}} / {{num|x45c_write_21_3_muse}} |
| dose 4 | {{num|x45c_write_12_4_9b}} / {{num|x45c_write_21_4_9b}} | {{num|x45c_write_12_4_27b}} / {{num|x45c_write_21_4_27b}} | {{num|x45c_write_12_4_muse}} / {{num|x45c_write_21_4_muse}} |
| random direction (same size), dose 1 | {{num|x45c_random_12_1_9b}} / {{num|x45c_random_21_1_9b}} | {{num|x45c_random_12_1_27b}} / {{num|x45c_random_21_1_27b}} | {{num|x45c_random_12_1_muse}} / {{num|x45c_random_21_1_muse}} |
| random direction (same size), dose 4 | {{num|x45c_random_12_4_9b}} / {{num|x45c_random_21_4_9b}} | {{num|x45c_random_12_4_27b}} / {{num|x45c_random_21_4_27b}} | {{num|x45c_random_12_4_muse}} / {{num|x45c_random_21_4_muse}} |
| n | {{num|x45c_n_12_9b}} / {{num|x45c_n_21_9b}} | {{num|x45c_n_12_27b}} / {{num|x45c_n_21_27b}} | {{num|x45c_n_12_muse}} / {{num|x45c_n_21_muse}} |

## Batch 45 behind README v5 (27 Oct; UNVERIFIED)

Rules and readings: [predictions/2026-10-26_dan.md](../predictions/2026-10-26_dan.md), batch 45; specs in [jobs/c3/batch45.yaml](../jobs/c3/batch45.yaml).

**The clean design (45m, fixed in advance).** An added locker item nobody picks becomes the asked person's pick, so only the bridge token differs. Extra loss without the J++ part (25 directions) against a random part of the same size, at the layer fixed in advance; the lookup's extra loss is not measurable where the locker comes after the pick (too few switches).

| Clean design | Qwen3.5-9B | Qwen3.6-27B | Muse Glimmer 30B |
|---|---|---|---|
| Gap, locker before the pick (the rule) | {{num|x45m_before_gap_9b}} | {{num|x45m_before_gap_27b}} | {{num|x45m_before_gap_muse}} |
| Lookup extra loss, locker before the pick | {{num|x45m_before_lk_9b}} | {{num|x45m_before_lk_27b}} | {{num|x45m_before_lk_muse}} |
| Recall extra loss: locker before / after the pick | {{num|x45m_before_rc_9b}} / {{num|x45m_after_rc_9b}} | {{num|x45m_before_rc_27b}} / {{num|x45m_after_rc_27b}} | {{num|x45m_before_rc_muse}} / {{num|x45m_after_rc_muse}} |
| Gap, all scenes | {{num|x45m_all_gap_9b}} | {{num|x45m_all_gap_27b}} | {{num|x45m_all_gap_muse}} |
| Lookups switched by the whole change: before / after | {{num|x45m_before_lksw_9b}} / {{num|x45m_after_lksw_9b}} | {{num|x45m_before_lksw_27b}} / {{num|x45m_after_lksw_27b}} | {{num|x45m_before_lksw_muse}} / {{num|x45m_after_lksw_muse}} |
| n: before / after / all | {{num|x45m_before_n_9b}} / {{num|x45m_after_n_9b}} / {{num|x45m_all_n_9b}} | {{num|x45m_before_n_27b}} / {{num|x45m_after_n_27b}} / {{num|x45m_all_n_27b}} | {{num|x45m_before_n_muse}} / {{num|x45m_after_n_muse}} / {{num|x45m_all_n_muse}} |

**Locker after the pick, by layer (45b's sweep; after the data).** Main-test items whose two prompts are identical after the bridge word (9B {{num|x45bsw_pass_9b}}, 27B {{num|x45bsw_pass_27b}}). Share of lookups switched by: the bridge-word change; the changed prompt's states copied into every locker-sentence token; only into the item names in those sentences; only into the numbers. 45b's rule on these items (copy at the layer fixed in advance, share of the lookups the changed prompt switches / the bridge-word change over all items): 9B {{num|x45b_sane_c_9b}} / {{num|x45b_sane_a_9b}}, 27B {{num|x45b_sane_c_27b}} / {{num|x45b_sane_a_27b}}, Muse ({{num|x45b_sane_pass_muse}}) {{num|x45b_sane_c_muse}} / {{num|x45b_sane_a_muse}}.

| Qwen3.5-9B, layer | bridge word | locker sentences | item names | numbers |
|---|---|---|---|---|
| 6 | {{num|x45bsw_bw_L6_9b}} | {{num|x45bsw_ls_L6_9b}} | {{num|x45bsw_li_L6_9b}} | {{num|x45bsw_lv_L6_9b}} |
| 8 | {{num|x45bsw_bw_L8_9b}} | {{num|x45bsw_ls_L8_9b}} | {{num|x45bsw_li_L8_9b}} | {{num|x45bsw_lv_L8_9b}} |
| 10 | {{num|x45bsw_bw_L10_9b}} | {{num|x45bsw_ls_L10_9b}} | {{num|x45bsw_li_L10_9b}} | {{num|x45bsw_lv_L10_9b}} |
| 12 (fixed in advance) | {{num|x45bsw_bw_L12_9b}} | {{num|x45bsw_ls_L12_9b}} | {{num|x45bsw_li_L12_9b}} | {{num|x45bsw_lv_L12_9b}} |

| Qwen3.6-27B, layer | bridge word | locker sentences | item names | numbers |
|---|---|---|---|---|
| 16 | {{num|x45bsw_bw_L16_27b}} | {{num|x45bsw_ls_L16_27b}} | {{num|x45bsw_li_L16_27b}} | {{num|x45bsw_lv_L16_27b}} |
| 20 | {{num|x45bsw_bw_L20_27b}} | {{num|x45bsw_ls_L20_27b}} | {{num|x45bsw_li_L20_27b}} | {{num|x45bsw_lv_L20_27b}} |
| 24 | {{num|x45bsw_bw_L24_27b}} | {{num|x45bsw_ls_L24_27b}} | {{num|x45bsw_li_L24_27b}} | {{num|x45bsw_lv_L24_27b}} |
| 28 | {{num|x45bsw_bw_L28_27b}} | {{num|x45bsw_ls_L28_27b}} | {{num|x45bsw_li_L28_27b}} | {{num|x45bsw_lv_L28_27b}} |
| 32 (fixed in advance) | {{num|x45bsw_bw_L32_27b}} | {{num|x45bsw_ls_L32_27b}} | {{num|x45bsw_li_L32_27b}} | {{num|x45bsw_lv_L32_27b}} |

**A refit pointer per format (45d, fixed in advance).** Fit without labels on half of each format's varied scenes, removed from the change on the other half; the lookup's extra loss (a format with fewer than 30 lookup switches does not count).

| Refit pointer | Qwen3.5-9B | Qwen3.6-27B | Muse Glimmer 30B |
|---|---|---|---|
| Prose | {{num|x45d_prose_9b}} | {{num|x45d_prose_27b}} | {{num|x45d_prose_muse}} |
| JSON | {{num|x45d_json_9b}} | {{num|x45d_json_27b}} | {{num|x45d_json_muse}} |
| Table | {{num|x45d_table_9b}} | {{num|x45d_table_27b}} | {{num|x45d_table_muse}} |
| The rule's label | {{num|x45d_outcome_9b}} | {{num|x45d_outcome_27b}} | {{num|x45d_outcome_muse}} |

**What the prompt names first (45a; the rule fixed in advance, these numbers after the data).** One sentence put at the start of both prompts. Identity share of the lookup's answers under the whole change on moves to or from the first locker, and the code shift β (positions) at the bridge word against no sentence.

| First sentence | Qwen3.5-9B: identity / β | Qwen3.6-27B: identity / β | Muse Glimmer 30B: identity / β |
|---|---|---|---|
| none | {{num|x45a_id_V0_9b}} / – | {{num|x45a_id_V0_27b}} / – | {{num|x45a_id_V0_muse}} / – |
| a pick naming the first locker's item | {{num|x45a_id_V1_9b}} / {{num|x45a_beta_V1_9b}} | {{num|x45a_id_V1_27b}} / {{num|x45a_beta_V1_27b}} | {{num|x45a_id_V1_muse}} / {{num|x45a_beta_V1_muse}} |
| a pick naming another item with a locker | {{num|x45a_id_V2_9b}} / {{num|x45a_beta_V2_9b}} | {{num|x45a_id_V2_27b}} / {{num|x45a_beta_V2_27b}} | {{num|x45a_id_V2_muse}} / {{num|x45a_beta_V2_muse}} |
| a pick naming an item with no locker | {{num|x45a_id_V3_9b}} / {{num|x45a_beta_V3_9b}} | {{num|x45a_id_V3_27b}} / {{num|x45a_beta_V3_27b}} | {{num|x45a_id_V3_muse}} / {{num|x45a_beta_V3_muse}} |
| a neutral sentence | {{num|x45a_id_V4_9b}} / {{num|x45a_beta_V4_9b}} | {{num|x45a_id_V4_27b}} / {{num|x45a_beta_V4_27b}} | {{num|x45a_id_V4_muse}} / {{num|x45a_beta_V4_muse}} |

**Other batch-45 numbers the README quotes.** Identity outside J++ against a wrong-pair direction (45e): identity answers cut beyond it {{num|x45e_cut_9b}} (9B), {{num|x45e_cut_27b}} (27B), {{num|x45e_cut_muse}} (Muse; bar 0.15). Without the chat template, the routes test's value answers (another item moved, whole change): {{num|x45i_value_9b}} (9B), {{num|x45i_value_27b}} (27B). The independent re-implementation of the 9B's main test: {{num|indep_agree_9b}} items agree on every arm.

## Controls

- A random part at each dictionary's own share of ‖Δ‖², per item.
- The random dictionary's own 25-atom fit.
- Both readers on the identical patch.
- The valid-cell bar: the whole edit flips at least 30% and 30 items.
- The competence gate: at least 80% unedited accuracy for both readers.
- A hardware gate reran a 23 Oct cell on the new box (0.99 per-row agreement).

## Simple explanations we checked

| Explanation | Test | Result | Status |
|---|---|---|---|
| The J++ part is just small | A random part of the same share removed | Recalls lose {{num|rc_rdep_27b}} to it at the 27B's layer 32, and {{num|rc_jdep_27b}} to J++ | checked |
| The edit differs between lookups and recalls | The identical patch at the bridge's word | By design | checked |
| Any token-aligned part would do | W_U, W_E and random atoms at 25-200 atoms | Only J++ costs the recall more than a random subspace of the same share | checked (27B, 9B) |
| The chat template | No chat template, with thinking not disabled or off | Can't test: the models open a think block or answer in markdown (first-token read right on {{num|nochat_gate_9b}} of 9B lookups / recalls, {{num|nochat_gate_27b}} on the 27B) | not a test of the hypothesis |
| The alt's second changed pick | Asked-first vs upstream-change items | Recalls the same; 27B lookups flip less without the upstream change | partly; a single-change alt is next |
| The lookup's layer profile is the J++ share | J-dependence against share across layers | 27B lookups track it; recalls do not | open |

## Choices made after the data (24 Oct; log in [jobs/c3/X0.md](../jobs/c3/X0.md))

| Choice | Why | What we did |
|---|---|---|
| X1-X4 run on the 27B although X0 did not confirm it (D3 amendment) | The graded contrast is large and specific to J++ | Reader comparisons at layer 32 under graded rules; the X0 verdict stays "not confirmed" |
| X1-X4 confirmatory on the 9B, exploratory on the 27B | The 9B passed X0's gate | Committed to each spec before its run |
| "No chat template, thinking off" arm (amendment 2) | Raw prompts open a think block | Descriptive; it failed its gate too |
| A first-digit read without the gate (amendment 3) | Answers start with " **" or a word | Descriptive, labeled |
| Descriptive tables and figures (the critic's requests) | Share, absolute drops, upstream change, equal shares, strata | Labeled "added after data" |

## Pre-registered tests and Dan's predictions

| Test | Rule fixed before the run | Verdict | Dan's prediction |
|---|---|---|---|
| X0, 27B at layer 32 | lookup excess ≤ 0.10 and recall J-dependence ≥ 0.30; killed if excess ≥ 0.20 or recall < 0.20 | {{num|verdict_27b}} | confirmed, 80%: wrong |
| X0, 9B at layer 12 | the same | {{num|verdict_9b}} | confirmed, 80%: right |
| X0, 122B at layer 33 | the same | {{num|verdict_122b}} | not confirmed, 70%: wrong |
| The 27B's layer-32 cell is valid for both readers | the whole edit flips ≥ 30% and ≥ 30 items | both valid | only recalls, 80%: wrong |
| W_E removal (H-token) | W_E lookup excess ≥ 0.20 with J++'s around | 9B: neither; 27B: not applicable | neither, 90%: right / wrong |
| W_U removal | both readers around | both models | inert, 90%: right |
| No chat template, thinking not disabled: gate | ≥ 80% for both readers | can't test | both pass, 80%: wrong |
| No chat template, thinking off: gate (amendment 2) | the same | can't test | both pass, 80%: wrong |

Scored question by question in [predictions/2026-10-24_dan.md](../predictions/2026-10-24_dan.md).

## Prompt formats and words

| Word | Meaning |
|---|---|
| chat | the chat template, thinking off (run key `chat`) |
| no chat template, thinking off | the template's empty think block added by hand; no roles, no instruction (run key `nochat`; two earlier runs say `nothink`) |
| no chat template, thinking not disabled | raw text (run key `raw`) |
| J++ | the refit J-lens, pinned per model (sha256 checked on load) |
| part | the 25-atom signed OMP fit of Δ over a dictionary's letter-token atoms |
| J-dependence | 1 − (flips without the part) / (flips with the whole edit) |
| excess | J-dependence minus that of a random subspace of the same share |
| graded contrast C | recall excess minus lookup excess on the same items (paired bootstrap over entities) |
| read | the top token after "Answer:" and a space is the alt answer's first token (chat) |
