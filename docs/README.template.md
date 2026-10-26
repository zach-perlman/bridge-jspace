<!-- grid: results/cross_model/20261023T210238Z -->
# The lookup goes around the lens: what a model reads from the bridge word

*When a model answers a two-step question, does it use the part of the in-between entity that a lens can read, and does that depend on what it does with that entity next?*

## In one minute

- **Recall uses the part the lens can read; the lookup does not:** on all four models by rules fixed in advance; in a clean design, on two of three.
- **The lookup uses which item it is and where its locker sits in the order of mentions:** the "where" is a pointer the lens cannot see; we can remove and write it.
- **The pointer is narrow:** it marks the first locker in a clean layout; naming an item first moves the lookup to identity. About half of the route around the lens is unexplained.
- **For monitoring:** a lens on the bridge word shows which item is there, not where the model will read its answer.

**Status.** Qwen3.5-9B, Qwen3.6-27B, Qwen3.5-122B-A10B (FP8) and Muse Glimmer 30B (another family); 27 Oct 2026. Unverified until hand-checked (Section 7). Built at {{head}} from the run files.

## Setup

![One prompt, two questions about the same bridge word](figures/story/fig00_setup.png)
*Fig. 0.*

- **Lookup**: "Which locker belongs to Iris's pick?" (answer in the prompt). **Recall**: "How many legs does Iris's pick have?" (answer from memory).
- **The change**: swap the bridge (frog → tick; the **main test** swaps two people's picks) and add the bridge word's hidden-state difference, at one layer, into the original prompt: whole, without a part, or without a **random part** of the same size. A reader **switches** to the changed prompt's answer.
- **Clean design**: an added locker item nobody picks becomes the asked person's pick; only the bridge token differs.
- **J++ part**: the 25 lens directions that best rebuild the change.
- **Extra loss**: the share of switches lost without a part minus that without its random part. **Gap**: the recall's extra loss minus the lookup's.
- **Fixed in advance**: committed before any result; otherwise **after the data**. Brackets: {{q|95%}} bootstrap intervals.

## 1. Recall needs the J++ part; the lookup does not

*Fixed in advance, except the split by sentence order and the two other scores.*

- **The split holds on all four models:** without the J++ part the recall loses a large share of its switches and the lookup almost none; the gap is {{pt|contrast_122b}} to {{pt|contrast_muse}} over all scenes and {{pt|sbo_swap_before_gap_122b}} to {{pt|sbo_swap_before_gap_muse}} where the locker sentence comes before the pick (Section 2).

![Recall needs the J++ part of the bridge; the lookup mostly does not](figures/story/fig01_split.png)
*Fig. 1.*

- **It holds in the clean design on two of three models** (bar: gap at least 0.3, lookup at most 0.10, locker before the pick): 27B {{num|x45m_before_gap_27b}}, Muse {{num|x45m_before_gap_muse}}. The 9B misses ({{num|x45m_before_gap_9b}}): when the locker came first, its recall needs the J++ part least of the three ({{pt|x45m_before_rc_9b}}, against {{pt|x45m_after_rc_9b}} after).
- **It is not a margin effect:** scored on the logit difference or the answer's probability, the gap is {{pt|ld_gap_122b}} to {{pt|ld_gap_muse}} and {{pt|prob_gap_122b}} to {{pt|prob_gap_muse}}.
- **It holds in every setting, weaker outside simple scenes**; in natural passages Muse's lookup switches too rarely to measure.

![In every setting, recall needs the J++ part more than the lookup does](figures/story/fig01b_settings.png)
*Fig. 1b.*

- **It is specific to the J++ part:** other parts of the same size cost the recall much less, except on the 122B, where PCA directions of the same size come close ({{num|pcaeq_pca_eq_rc_excess_122b}} vs {{num|pcaeq_jpp_rc_excess_122b}}).

![No other part of the same size costs the recall as much as the J++ part](figures/story/fig02_specificity.png)
*Fig. 2.*

- **The 27B misses the strict rule:** its lookup loses {{num|lk_excess_27b}} (bar 0.10), {{num|lk_excess_k100_27b}} at 100 directions.

## 2. At the layer we fixed, only locker-first lookups can be redirected

*After the data; the main test unless named.*

- **Lookups switch when the locker sentence comes before the pick** (locker-first scenes): {{num|lk_order_before_muse}}-{{num|lk_order_before_122b}} of them, against {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} after it, on all four models; in the clean design {{num|x45m_before_lksw_muse}}-{{num|x45m_before_lksw_9b}} against {{num|x45m_after_lksw_27b}}-{{num|x45m_after_lksw_9b}}.
- **The recall needs the J++ part less when its locker came first, on every model:** 9B {{pt|sbo_swap_before_rc_9b}} vs {{pt|sbo_swap_after_rc_9b}} after, 27B {{pt|sbo_swap_before_rc_27b}} vs {{pt|sbo_swap_after_rc_27b}}, 122B {{pt|sbo_swap_before_rc_122b}} vs {{pt|sbo_swap_after_rc_122b}}, Muse {{pt|sbo_swap_before_rc_muse}} vs {{pt|sbo_swap_after_rc_muse}}.

![Lookups follow the change mostly when the locker sentence comes first](figures/story/fig03_order.png)
*Fig. 3.*

- **Timing** (9B / 27B, on the items identical after the bridge word: {{num|x45bsw_pass_9b}} / {{num|x45bsw_pass_27b}}): a bridge change at an earlier layer still switches locker-after lookups ({{pt|x45bsw_bw_L6_9b}} / {{pt|x45bsw_bw_L16_27b}}), fading by the layer we fixed ({{pt|x45bsw_bw_L12_9b}} / {{pt|x45bsw_bw_L32_27b}}).
- **Where the link is made is open:** copying the changed prompt's states into the locker sentences at that layer switches {{pt|x45b_sane_c_9b}} / {{pt|x45b_sane_c_27b}} / {{pt|x45b_sane_c_muse}} of the lookups (9B / 27B / Muse), not the half the rule fixed in advance asked for; on the Qwens mostly through the item names there, never the numbers. We withdraw the account that the locker sentence makes the link.

![Locker after the pick: an early bridge change still switches the lookup](figures/story/fig03b_layers.png)
*Fig. 3b.*

## 3. The lookup uses which item it is and where its locker sits

*The routes test fixed in advance; the rest after the data.*

- **We set three routes against each other:** the change comes from a prompt where another item's locker sentence moved to a new place with a new number.

![Each route predicts a different locker](figures/story/fig04_routes_design.png)
*Fig. 4.*

- **The lookup never takes the number itself, and splits between identity and position:** the 27B leans on identity, the 9B and Muse on position. **Adding only the J++ part gives no identity answers**, so even the identity route runs mostly outside J++. Without the chat template, too, the lookup never answers the value ({{num|x45i_value_9b}} on the 9B, {{num|x45i_value_27b}} on the 27B).

![The lookup follows identity or position, never the value](figures/story/fig05_routes.png)
*Fig. 5.*

| Another item moved, whole change | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B° | Muse Glimmer 30B |
|---|---|---|---|---|
| Identity / position | {{num|rt_C2_whole_identity_9b}} / {{num|rt_C2_whole_position_9b}} | {{num|rt_C2_whole_identity_27b}} / {{num|rt_C2_whole_position_27b}} | {{num|rtg_C2_whole_identity_122b}} / {{num|rtg_C2_whole_position_122b}} | {{num|rt_C2_whole_identity_muse}} / {{num|rt_C2_whole_position_muse}} |

*° gate lowered to 0.75 after the data.*

- **Position appears with depth (candidate):** at an early layer the change moves the lookup by identity only, inside J++ on the Qwens; position answers appear a few layers later, on the 27B four layers after the lookup stops needing J++.

![Position answers appear with depth, once the lookup stops needing the J++ part](figures/story/fig06_depth.png)
*Fig. 6.*

## 4. The pointer can be removed and written

*Removal after the data, replicated in advance on the 9B and Muse; routes arms and writes fixed in advance, their recall split after the data.*

- **A probe reads the pointer, the lens does not:** a linear probe on the bridge word tells which sentence holds the item's locker in {{num|v4_b_before_122b}}-{{num|v4_b_before_27b}} of scenes (layout alone: {{num|v4_b_layout_before_27b}}), almost none of it in J++. A probe shows information, not use, so we tested the **pointer**, four directions separating the positions, causally.
- **Removing the pointer stops position answers:** to near zero on the Qwens, by half on Muse; a random part of the same size barely changes them, and the recall loses much less (Fig. 5).
- **Adding only the pointer creates position answers** on three of four models (not the 27B); a random part of the same size creates none.
- **One fixed vector written into the bridge moves the lookup:** the mean difference between two positions, the same for every scene, sends it to the target locker in a quarter to a half of the writes at a real change's size (the dose fixed in advance was smaller, Section 6); a random vector moves nothing.
- **The recall follows a strong write to the item:** on the Qwens about four in five recalls a strong write changes name the item at the target position (Muse: {{num|x8_rc_target_muse}}).

![One fixed vector written at the bridge sends the lookup to its locker](figures/story/fig07_writes.png)
*Fig. 7.*

## 5. Where the pointer stops working

*After the data unless marked fixed in advance.*

- **It marks the first locker in a clean layout, with no item named before them.** It follows the order of mentions: a neutral first sentence barely moves its code (code shift β {{pt|x45a_beta_V4_9b}}-{{pt|x45a_beta_V4_muse}} positions); one naming an item shifts it {{pt|x45a_beta_V2_27b}}-{{pt|x45a_beta_V3_muse}}, and the Qwens' lookup then follows identity ({{pt|x45a_id_V3_9b}}-{{pt|x45a_id_V3_27b}} of answers, against {{pt|x45a_id_V0_9b}} / {{pt|x45a_id_V0_27b}}). By the rule fixed in advance it is mixed: the neutral sentence also cuts the Qwens' position answers from only the pointer.

![The pointer marks the first locker in a clean layout](figures/story/fig08_first_locker.png)
*Fig. 8.*

- **It carries over poorly; a refit pointer works on two of three models:** fit on simple scenes, it costs the lookup {{num|tptr_varied_range}} in varied scenes and {{num|tptr_natural_range}} in natural passages; refit per format on half of the scenes (fixed in advance), it costs the held-out half's lookup {{pt|x45d_table_9b}}-{{pt|x45d_prose_9b}} on the 9B, {{pt|x45d_prose_muse}}-{{pt|x45d_table_muse}} on Muse and at most {{pt|x45d_table_27b}} on the 27B.

![The split carries over to other texts; the pointer does not](figures/story/fig09_transfer.png)
*Fig. 9.*

- **Later positions are coded elsewhere:** between the second and third locker the pointer barely moves the Qwens' lookup (Muse: {{num|pm_keep_12w_muse}}), and neither do directions found from those moves (fixed in advance). Writing their mean difference moves it at twice a real change (9B and Muse: {{pt|x45c_write_12_2_muse}}-{{pt|x45c_write_21_2_9b}} of writes; the 27B at four times), not at its size ({{pt|x45c_write_12_1_27b}}-{{pt|x45c_write_21_1_muse}}): a route the model does not use at its natural size.
- **About half of the route is unexplained:** that many lookups still switch without the J++ part and the pointer. Removing identity outside J++ too leaves few on the 9B and 27B, fewer than a wrong-pair direction of the same size (table), but it cuts identity answers only {{pt|x45e_cut_9b}} / {{pt|x45e_cut_27b}} more (bar 0.15, fixed in advance): partly specific on the Qwens, not on Muse.

![J++ part, pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's](figures/story/fig10_what_is_left.png)
*Fig. 10.*

| Sanity swap, without the J++ part + pointer + identity outside J++ | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| Lookups still switching: without the part / without a random part (same size) | {{pt|rtd_left_C0_jpp+alf+idout_lk_9b}} / {{pt|rtd_randleft_C0_jpp+alf+idout_lk_9b}} | {{pt|rtd_left_C0_jpp+alf+idout_lk_27b}} / {{pt|rtd_randleft_C0_jpp+alf+idout_lk_27b}} | not run | {{pt|rtd_left_C0_jpp+alf+idout_lk_muse}} / {{pt|rtd_randleft_C0_jpp+alf+idout_lk_muse}} |
| Lookups still switching: a wrong-pair direction (same size) in place of identity | {{num|x45e_left_wrong_9b}} | {{num|x45e_left_wrong_27b}} | not run | {{num|x45e_left_wrong_muse}} |
| The part's share of the change | {{num|rtd_share_C0_jpp+alf+idout_9b}} | {{num|rtd_share_C0_jpp+alf+idout_27b}} | – | {{num|rtd_share_C0_jpp+alf+idout_muse}} |
| Recall's extra loss without identity (nothing else removed) | {{num|rtd_ex_C0_id_rc_9b}} | {{num|rtd_ex_C0_id_rc_27b}} | – | {{num|rtd_ex_C0_id_rc_muse}} |

## 6. What did not hold

![What held where](figures/story/fig11_scorecard.png)
*Fig. 11.*

- **Failed when fixed in advance:** the 27B's strict rule and the 9B in the clean design; the 9B's replication (recall {{pt|rep_jpp_rc_excess_9b}}); the positive control (chemical symbols, 27B {{pt|x4_D_elements_27b}}, bar 0.20); a second route for the recall through the pointer; identity outside J++ by itself (27B only) and against a wrong pair; a second-versus-third pointer; the reading-order rule (withdrawn); the copied link outside the lens (27B, by one item).
- **Gates missed (bar 0.80), not tested:** the 9B's natural passages, the 122B's routes and replication, the Qwens' main test without the chat template; reruns at 0.75 are descriptive.
- **Design errors:** the write's dose fixed in advance, below a real change's size; the bar for the J++ part, pointer and identity removed together, out of reach at their share; the first scenes where only the asked pick changed reused another person's pick as the bridge (replaced by the clean design); the reading-order test's prompts differing after the bridge word.
- **Limits:** one-token answers and bridges; reader and answer source (prompt vs memory) confounded; the 122B in FP8; Zach's knock-out finds the split weak outside Qwen, our change-removal finds it on Muse.

## 7. How we checked

- **Hand-checked numbers:** none yet; one item read, consistent ([docs/review_summary.md](docs/review_summary.md)); [docs/verify_pack.md](docs/verify_pack.md) recounts each claim from the per-item files.
- **Independent reimplementation:** code written from scratch reproduces the 9B's main test on {{num|indep_agree_9b}} random items, every arm.
- **Same tokens after the bridge word:** this check caught the reading-order test, whose two prompts mostly differed there (Section 2).
- **Raw examples:** `make review-serve`, random items per claim (fixed seed).
- **Predictions:** committed before results are opened, then scored ([predictions/](predictions/README.md)): mean Brier {{num|pred_brier}} over {{num|pred_n}} answers, batch 45 included, worse than always answering {{q|50%}}.

## 8. Related work and what is new

Language models bind an entity to its attributes in context (Feng & Steinhardt 2023) and track entities through lookback pointers (Prakash et al. 2025); the order of bound entities lives in a low-dimensional subspace (Dai et al. 2024). Two-hop recall resolves its bridge early (Biran et al. 2024). Our routes test follows Gur-Arieh et al. (2025); the pointer is built from mass-mean directions (Marks & Tegmark 2023); a part that moves an answer when added by itself can mislead (Makelov et al. 2023), hence the random parts. The lens is the workspace paper's J++ (Gurnee et al. 2026). New here: two readers of the same word need different parts of it, and only the recall needs the J++ part; the pointer is the part the lens misses; and it can be written into the model to redirect the lookup.

## 9. Next

- **Follow-ups:** where locker-after lookups tie the item to its locker (pre-registered); what tells the second and third locker apart; answers by sampling; the 122B's identity test.
- **Training:** OLMo checkpoints, when the pointer appears.
- **Later:** new datasets; intermediates in reasoning traces; DeepSeek-V4-Flash.

## Appendix A. Links

Every number on this page comes from [figures/story/data.csv](figures/story/data.csv) (also every plotted number) and [docs/x0_numbers.json](docs/x0_numbers.json), each with its source file; [docs/x0_details.md](docs/x0_details.md) has the full tables; [docs/verify_pack.md](docs/verify_pack.md) recounts them. All figures on one page: [docs/figures_contact_sheet.png](docs/figures_contact_sheet.png); the figure plan: [docs/figure_plan.md](docs/figure_plan.md). Supplementary figures: [every scene set](figures/supp/s01_split_all_scene_sets.png), [our first scenes where only the asked pick changed, with the reused pick](figures/supp/s01b_one_pick_duplicate.png), [every part](figures/supp/s02_parts_all.png), [every routes arm](figures/supp/s05_routes_all_arms.png), [what the prompt names first, and the label-free pointer](figures/supp/s08_first_sentence_and_label_free.png), [the parts removed together, with the bars fixed in advance](figures/supp/s10_removed_together_bars.png). Earlier figures: [figures/status_2026-10-25/](figures/status_2026-10-25/).
