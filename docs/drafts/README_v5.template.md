<!-- grid: results/cross_model/20261023T210238Z -->
# The lookup goes around the lens: what a model reads from the bridge word

*When a model answers a two-step question, does it use the part of the in-between entity that a lens can read, and does that depend on what it does with that entity next?*

## In one minute

- **Recall uses the part of the bridge the lens can read; the lookup does not:** on all four models, removing the lens-readable part breaks the recall far more than the lookup, under rules fixed before the run.
- **The lookup uses which item it is and where its locker sentence sits:** the "where" is a pointer the lens cannot see. Removing it stops position-based lookups, and writing it sends the lookup to the place it points at.
- **The pointer we found is tied to the layout:** our directions mark the first locker only when no item is named before it. Refit per format, a pointer is found again in two of three formats on the 9B (prose, JSON) and Muse (prose, tables), not on the 27B. About half of the lookup's route around the lens is still open.
- **For monitoring:** a lens on the bridge word shows which item the model is using, but not where in the context the model will read its answer from.

**Status.** Qwen3.5-9B, Qwen3.6-27B, Qwen3.5-122B-A10B (FP8) and Muse Glimmer 30B (another family); 26 Oct 2026. All numbers unverified until hand-checked (Section 7). Built at {{head}} from the run files.

## Setup

![One prompt, two questions about the same bridge word](figures/story/fig00_setup.png)
*Fig. 0.*

- **Lookup**: "Which locker belongs to Iris's pick?" The answer is in a sentence of the prompt. **Recall**: "How many legs does Iris's pick have?" The answer comes from memory.
- **The change**: swap the bridge (frog → tick), take the hidden state's difference at the bridge word at one layer, and add it into the original prompt there, whole, without a part, or without a **random part** of the same size. A reader **switches** when it gives the swapped bridge's answer.
- **J++ part**: the 25 lens directions that best rebuild the change.
- **Extra loss**: the share of switches lost without a part minus the share lost without its random part. **Gap**: the recall's extra loss minus the lookup's.
- **Fixed in advance**: test, layer, sample and bar committed before any result; **after the data**: chosen after seeing results. Brackets: {{q|95%}} bootstrap intervals.

## 1. Recall needs the lens-readable part; the lookup does not

*Fixed in advance (the main test; Muse's whole grid; the other settings' bars).*

Does removing the part of the bridge the lens can read cost the recall more than the lookup?

- **The split holds on all four models:** removing the J++ part costs the recall a large share of its switches and the lookup almost none; the gap is {{pt|contrast_122b}} to {{pt|contrast_muse}}.

![Recall needs the J++ part of the bridge; the lookup mostly does not](figures/story/fig01_split.png)
*Fig. 1.*

- **It is not a margin effect:** scored on the logit difference instead of switches, the gap is about the same ({{pt|ld_gap_122b}} to {{pt|ld_gap_muse}}).
- **It holds in every setting, weaker outside simple scenes**; in natural passages Muse's lookup switches too rarely to measure.
- **On every model the recall needs J++ less when its locker sentence came first** (9B {{pt|sbo_fresh_before_rc_9b}}-{{pt|sbo_swap_before_rc_9b}} vs {{pt|sbo_one_after_rc_9b}}-{{pt|sbo_swap_after_rc_9b}}; 122B {{pt|sbo_swap_before_rc_122b}} vs {{pt|sbo_swap_after_rc_122b}}; 27B and Muse {{pt|sbo_swap_before_rc_27b}}-{{pt|sbo_swap_before_rc_muse}} vs {{pt|sbo_swap_after_rc_muse}}-{{pt|sbo_swap_after_rc_27b}}).

![In every setting, recall needs the J++ part more than the lookup does](figures/story/fig01b_settings.png)
*Fig. 1b.*

- **It is specific to the lens's part:** other parts of the same size cost the recall much less. The 122B is the exception: its main directions come close ({{num|pcaeq_pca_eq_rc_excess_122b}} vs {{num|pcaeq_jpp_rc_excess_122b}}).

![No other part of the same size costs the recall as much as the J++ part](figures/story/fig02_specificity.png)
*Fig. 2.*

- **One model misses the strict rule:** on the 27B the lookup loses {{num|lk_excess_27b}} (bar 0.10) and needs J++ once 100 directions are removed ({{num|lk_excess_k100_27b}}).

## 2. The lookup follows the change only when the locker came first

*After the data.*

- **Lookups switch when the locker sentence comes before the pick:** {{num|lk_order_before_muse}}-{{num|lk_order_before_122b}} of such scenes switch, against {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} when it comes after, on all four models.

![Lookups follow the change mostly when the locker sentence comes first](figures/story/fig03_order.png)
*Fig. 3.*

- **Timing** (after the data, on the items identical after the bridge word: {{num|x45bsw_pass_9b}} / {{num|x45bsw_pass_27b}}): a bridge change made early still switches locker-after lookups ({{num|x45bsw_bw_L6_9b}} at L6 on the 9B, {{num|x45bsw_bw_L16_27b}} at L16 on the 27B) and fades by the layer fixed in advance ({{num|x45bsw_bw_L12_9b}} / {{num|x45bsw_bw_L32_27b}}).
- **Location is open:** copying the locker sentences at that layer carries about a third ({{num|x45bsw_ls_L12_9b}} / {{num|x45bsw_ls_L32_27b}}), mostly on the item's own token ({{num|x45bsw_li_L12_9b}} / {{num|x45bsw_li_L32_27b}}), never the number.

## 3. The lookup uses which item it is and where its locker sentence sits

*The routes test fixed in advance; the layer sweep after the data.*

Which route does the lookup take: the item's identity, its position, or the number itself?

- **We set three routes against each other:** the change comes from a prompt where another item's locker sentence moved to a new place with a new number (after Gur-Arieh et al. 2025).

![Each route predicts a different locker](figures/story/fig04_routes_design.png)
*Fig. 4.*

- **The lookup never takes the number itself, and splits between identity and position:** the 27B leans on identity, the 9B and Muse on position. **The lens's part alone gives no identity answers**, so even the identity route runs mostly outside J++.

![The lookup follows identity or position, never the value](figures/story/fig05_routes.png)
*Fig. 5.*

| Another item moved, whole change | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B° | Muse Glimmer 30B |
|---|---|---|---|---|
| Identity / position | {{num|rt_C2_whole_identity_9b}} / {{num|rt_C2_whole_position_9b}} | {{num|rt_C2_whole_identity_27b}} / {{num|rt_C2_whole_position_27b}} | {{num|rtg_C2_whole_identity_122b}} / {{num|rtg_C2_whole_position_122b}} | {{num|rt_C2_whole_identity_muse}} / {{num|rt_C2_whole_position_muse}} |

*° gate lowered to 0.75 after the data.*

- **Position appears with depth (candidate):** at an early layer the change moves the lookup by identity only, and on the Qwens that identity sits inside J++; position answers appear a few layers later. On the 27B the lookup stops needing J++ at layer 24, four layers before position appears.

![Position answers appear with depth, once the lookup stops needing the J++ part](figures/story/fig06_depth.png)
*Fig. 6.*

## 4. The pointer can be removed and written

*Removal after the data, replicated in advance on the 9B and Muse; the routes arms and the writes fixed in advance; the writes' recall split after the data.*

Is "where the item's locker is stated" a part of the bridge word that the model uses?

- **A probe reads the pointer, the lens does not:** a linear probe on the bridge word tells which sentence holds the item's locker in {{num|v4_b_before_122b}}-{{num|v4_b_before_27b}} of scenes (layout alone: {{num|v4_b_layout_before_27b}}), almost none of it in J++. A probe shows the information is there, not its use, so we tested the four **pointer directions** that separate the positions causally.
- **Removing the pointer stops position answers:** they drop to near zero on the Qwens and by half on Muse; a random part of the same size barely changes them, and the recall loses much less than the lookup (Fig. 5).
- **Adding only the pointer creates position answers** on three of four models (not the 27B); a random part of the same size creates none.
- **One fixed vector written into the bridge moves the lookup:** the mean difference between two positions, the same for every scene, sends the lookup to the target locker in a quarter to a half of the writes once it is as large as a real change; a random vector moves nothing. The strength fixed in advance moved nothing (a design error, Section 6).
- **The recall follows a strong write to the item:** on the Qwens about four in five of the recalls a strong write changes name the item at the target position (Muse: {{num|x8_rc_target_muse}}).

![One fixed vector written at the bridge sends the lookup to its locker](figures/story/fig07_writes.png)
*Fig. 7.*

## 5. Where the pointer stops working

*After the data, except the transfer bars and the identity test, fixed in advance.*

How far does the pointer we found reach?

- **It marks the first locker, in the clean layout:** a sentence before the lockers (Q45.3, fixed in advance) gives mixed. After the data: its code shifts with every sentence naming an item first (code shift β: neutral {{num|x45a_beta_V4_9b}}-{{num|x45a_beta_V4_muse}}, pick {{num|x45a_beta_V2_27b}}-{{num|x45a_beta_V1_muse}}), and after a pick sentence the Qwens' lookup follows identity instead of position ({{num|x45a_id_V3_9b}}-{{num|x45a_id_V3_27b}} vs {{num|x45a_id_V0_9b}} / {{num|x45a_id_V0_27b}}).

![Naming an item before the lockers switches the lookup from position to identity](figures/story/fig08b_layout.png)
*Fig. 8b. On Muse part of the lost position answers go back to the original answer.*

- **Later positions are coded elsewhere:** the pointer moves the lookup to and from the first locker, not between the second and third on the Qwens (Muse: {{num|pm_keep_12w_muse}}), though the whole change does; directions found from those moves do not carry them either (Q45.6). Halfway writes land between lockers only from the first: the code is first-vs-rest, not a line.

![The pointer marks the first locker, in the clean layout](figures/story/fig08_first_mentioned.png)
*Fig. 8.*

- **It carries over poorly to other texts:** fit on simple scenes and not refit, the pointer costs the lookup {{num|tptr_varied_range}} in varied scenes and {{num|tptr_natural_range}} in natural passages, while the lookup still does not need J++ there.

![The split carries over to other texts; the pointer does not](figures/story/fig09_transfer.png)
*Fig. 9.*

- **About half of the route is unexplained:** with J++ and the pointer removed, about half of the lookups still switch; identity outside J++ removes most of the rest on the 9B and 27B. Against a wrong-pair direction of its size (Q45.7) it is partly specific on the Qwens: fewer lookups left ({{num|x45e_left_idout_9b}} vs {{num|x45e_left_wrong_9b}}; {{num|x45e_left_idout_27b}} vs {{num|x45e_left_wrong_27b}}), but identity answers cut only {{num|x45e_cut_9b}} / {{num|x45e_cut_27b}} more (bar 0.15); not on Muse.

![J++ part, pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's](figures/story/fig10_what_is_left.png)
*Fig. 10.*


## 6. What did not hold

![What held where](figures/story/fig11_scorecard.png)
*Fig. 11.*

- **Failed when fixed in advance.**
  - The 27B's strict rule (Section 1).
  - The 9B's replication: its J++ clause failed (recall {{num|rep_jpp_rc_excess_9b}}).
  - The positive control (chemical symbols) stayed below its 0.20 bar: 27B {{num|x4_D_elements_27b}}.
  - Removing the identity direction alone cut the identity route on the 27B only.
  - Gates missed (bar 0.80), not tested: the 9B's natural passages (lookup {{num|nat_gate_lk_9b}}), the 122B's routes (recall {{num|rt_c0gate_rc_122b}}) and replication (recall {{num|rep_gate_rc_122b}}); reruns at 0.75 are descriptive.
- **Design errors.**
  - The write's dose fixed in advance, s = 1, was below a real change's size on every pair (s needed: {{num|x8_sreal_9b}}; {{num|x8_sreal_27b}}; {{num|x8_sreal_122b}}; {{num|x8_sreal_muse}}).
  - The bar for J++, the pointer and identity removed together was out of reach at their share: the random part removes most switches on the Qwens.
  - The one-pick scenes' new bridge is already another person's pick; with a new, unpicked item (Q45.10) the locker-first gap is {{pt|x45m_before_gap_27b}} / {{pt|x45m_before_gap_muse}} / {{pt|x45m_before_gap_9b}} (27B / Muse / 9B).
- **Limits.**
  - The pointer comes from five position labels in simple scenes and mostly carries the first locker versus the rest, in the clean layout.
  - The locker number at the bridge word: never the answer; digit directions cost {{num|dig_lk_jppdig_k10_before_27b}}.
  - One-token answers and bridges; the reader is confounded with the answer's source (prompt vs memory). The 122B in FP8.
  - Zach's knock-out finds the split weak outside Qwen; our change-removal finds it on Muse.

## 7. How we checked

- **Hand-checked numbers.** None yet ([docs/review_summary.md](docs/review_summary.md)); [docs/verify_pack.md](docs/verify_pack.md) recounts each claim's numbers from the per-item files.
- **Raw examples.** `make review-serve`: random items per claim (fixed seed), as the model saw them.
- **Predictions.** Committed before results are opened, then scored ([predictions/](predictions/README.md)): mean Brier {{num|pred_brier}} over {{num|pred_n}} answers, worse than always answering {{q|50%}}; the mechanistic questions were mostly wrong.
- **Inventory.** [docs/inventory.md](docs/inventory.md): pre-pivot experiments are kept and labelled legacy.

## 8. Related work and what is new

Language models bind an entity to its attributes in context (Feng & Steinhardt 2023) and track entities through lookback pointers (Prakash et al. 2025); the order of bound entities lives in a low-dimensional subspace (Dai et al. 2024). Two-hop recall resolves its bridge early (Biran et al. 2024). Our routes test sets identity, position and value against each other as in Gur-Arieh et al. (2025); the pointer directions are mass-mean directions (Marks & Tegmark 2023); a part that moves an answer when added alone can mislead (Makelov et al. 2023), so every part has a random part of its size beside it. The lens is the workspace paper's J++ (Gurnee et al. 2026). New here: two readers of the same word need different parts of it, and only the recall needs the lens's part; the pointer is the part the lens misses; and it can be written into the model to redirect the lookup.

## 9. Next

- **Follow-ups:** what tells the second and third locker apart; answers by sampling; the 122B's identity test.
- **Training:** OLMo checkpoints, when the pointer appears.
- **Later:** new datasets; intermediates in reasoning traces; DeepSeek-V4-Flash.

## Appendix A. Links

Every number on this page comes from [figures/story/data.csv](figures/story/data.csv) (also every plotted number) and [docs/x0_numbers.json](docs/x0_numbers.json), each with its source file; [docs/x0_details.md](docs/x0_details.md) has the full tables; [docs/verify_pack.md](docs/verify_pack.md) recounts them. All figures on one page: [docs/figures_contact_sheet.png](docs/figures_contact_sheet.png); the figure plan: [docs/figure_plan.md](docs/figure_plan.md). Supplementary figures: [every scene set](figures/supp/s01_split_all_scene_sets.png), [every part](figures/supp/s02_parts_all.png), [every routes arm](figures/supp/s05_routes_all_arms.png), [the parts removed together, with the bars fixed in advance](figures/supp/s10_removed_together_bars.png). Earlier figures: [figures/status_2026-10-25/](figures/status_2026-10-25/).
