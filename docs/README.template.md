<!-- grid: results/cross_model/20261023T210238Z -->
# The lookup goes around the lens: what a model reads from the bridge word

*When a model answers a two-step question, does it use the part of the in-between entity that a lens can read, and does that depend on what it does with that entity next?*

## In one minute

- Recall needs the part of the bridge word a lens can read (J++); the lookup, which reads its answer from the prompt, mostly does not. This holds on four models from two families, and on the logit difference too. The gap is smaller outside simple scenes.
- In simple scenes, the lookup instead takes which item it is (identity, mostly outside J++) and where that item was first mentioned (a pointer). One fixed vector written into the bridge word moves the lookup to the locker of the mention it points at. Under a strong write, the recall follows it to that mention's item.
- Our pointer directions mostly mark "first sentence of the prompt". The model also tells later positions apart, but mostly outside them. Fit on simple scenes, they explain little in varied scenes and natural text. About half of the route around the lens is still unexplained.
- Why it matters: a lens shows what the bridge is. What steers a lookup from context is where it was mentioned, and the lens does not show that.

![Recall needs the J++ part; the lookup mostly doesn't](figures/story/fig1_readers.png)
*Fig. 1. Lookup against recall in each row; grey band: not needed. Muse's natural passages: no gap (few lookup switches).*

**Status.** Qwen3.5-9B, Qwen3.6-27B, Qwen3.5-122B-A10B and Muse Glimmer 30B (another family); 26 Oct 2026. All numbers unverified until hand-checked (Section 7). Built at {{head}} from the run files.

## Setup

![One prompt, two questions about the same in-between word](figures/story/fig0_setup.png)

- **Bridge**: the in-between entity, here the item Iris picked (*frog*).
- **Lookup** and **recall**: the lookup asks for the bridge's locker, written in the prompt; the recall asks for a fact about it from memory.
- **The change**: swap the bridge (frog → tick), take the hidden state's difference at the bridge word at one layer, and add it into the original prompt there. A reader **switches** when it gives the swapped bridge's answer.
- **J++ part**: the 25 lens directions that best rebuild the change. We remove it, or as the control a **random part** of the same size.
- **Extra loss**: the share of switches lost without a part minus the share lost without its random part.
- **Gap**: the recall's extra loss minus the lookup's.
- **Fixed in advance**: test, layer, sample and bar committed before any result; **after the data**: chosen after seeing results. Brackets: {{q|95%}} bootstrap intervals.

## 1. The split: recall needs the lens-readable part; the lookup mostly doesn't

*Fixed in advance (main test; Muse's whole grid); other settings: pass bars set before each run.*

- **What we did.** One layer per model; 200 scenes, then other scene sets and parts.
- **What we found.**
  - The gap is positive wherever measured (table). The strict rule held on the 9B, the 122B and Muse; on the 27B the lookup lost {{num|lk_excess_27b}} (bar 0.10). In matched scenes (the asked pick is not the bridge's first mention) the gap is smaller.
  - It shrinks outside simple scenes; Muse's stays the largest.
  - On the logit difference instead of switches the gap holds on all four (bar fixed in advance; table).
  - On the 27B the lookup needs J++ once more directions are removed; the others keep the gap at 100 (table).
  - Other parts of a similar size cost the recall less than J++ (Fig. 2).

| Gap | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| Two people swap picks (fixed in advance) | {{num|contrast_9b}} | {{num|contrast_27b}} | {{num|contrast_122b}} | {{num|contrast_muse}} |
| Only the asked person's pick changes | {{num|single_contrast_9b}} | {{num|single_contrast_27b}} | {{num|single_contrast_122b}} | {{num|single_contrast_muse}} |
| Matched: fresh scenes, both locker sentences first, only the asked pick changes | {{num|comp_rep_both_gap_9b}} | {{num|comp_rep_both_gap_27b}} | {{num|comp_rep_both_gap_122b}}° | {{num|comp_rep_both_gap_muse}} |
| Varied scenes | {{num|x0b_c_9b}} | {{num|x0b_c_27b}} | {{num|x0b_c_122b}} | {{num|x0b_c_muse}} |
| Natural passages | {{num|natg75_gap_9b}}° | {{num|nat_gap_27b}} | {{num|nat_gap_122b}} | recall {{num|nat_rc_excess_muse}}, lookup {{num|nat_lk_excess_muse}} ({{num|nat_n_muse}} passages) |
| More J++ directions removed, 100: gap (27B: lookup's extra loss at 25 / 50 / 100) | {{num|contrast_k100_9b}} | {{num|lk_excess_k25_27b}} / {{num|lk_excess_k50_27b}} / {{num|lk_excess_k100_27b}} | {{num|contrast_k100_122b}} | {{num|contrast_k100_muse}} |
| Logit difference: gap | {{num|ld_gap_9b}} | {{num|ld_gap_27b}} | {{num|ld_gap_122b}} | {{num|ld_gap_muse}} |
| Logit difference (lookup / recall extra loss) | {{num|ld_lk_9b}} / {{num|ld_rc_9b}} | {{num|ld_lk_27b}} / {{num|ld_rc_27b}} | {{num|ld_lk_122b}} / {{num|ld_rc_122b}} | {{num|ld_lk_muse}} / {{num|ld_rc_muse}} |

*°: after the data, the gate lowered to 0.75.*

![No other part costs the recall as much as the scene's own J++](figures/story/fig2_parts.png)
*Fig. 2. †: two people swap picks; others: only the asked pick changes.*

- **Caveat.** On the 122B the main directions at J++'s share cost the recall almost as much as J++ ({{num|pcaeq_pca_eq_rc_excess_122b}} vs {{num|pcaeq_jpp_rc_excess_122b}}).

## 2. What the lookup takes instead: identity or position

*After the data; the routes test fixed in advance.*

- **What we did.** (a) Split lookups by sentence order. (b) Swapped prompts where the item's identity, its locker sentence's position and the locker value predict different lockers (Fig. 3).
- **What we found.**
  - (a) Lookups switch in {{num|lk_order_before_27b}}-{{num|lk_order_before_122b}} of locker-first scenes and {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} otherwise; lookup claims here are about locker-first scenes. On the 27B's natural passages the lookup switches mostly when the fact comes first ({{num|natsplit_before_lk_sw_27b}} of {{num|natsplit_before_n_27b}} vs {{num|natsplit_after_lk_sw_27b}} of {{num|natsplit_after_n_27b}}).
  - (b) When another item moved, the lookup follows its identity or its locker sentence's position, never the new value (Fig. 4); the J++ part alone moves none.

| Another item moved | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B° | Muse Glimmer 30B |
|---|---|---|---|---|
| Identity / position | {{num|rt_C2_whole_identity_9b}} / {{num|rt_C2_whole_position_9b}} | {{num|rt_C2_whole_identity_27b}} / {{num|rt_C2_whole_position_27b}} | {{num|rtg_C2_whole_identity_122b}} / {{num|rtg_C2_whole_position_122b}} | {{num|rt_C2_whole_identity_muse}} / {{num|rt_C2_whole_position_muse}} |
| Identity with only the J++ part | {{num|rtk_C2_keep_jpp_identity_9b}} | {{num|rtk_C2_keep_jpp_identity_27b}} | {{num|rtk_C2_keep_jpp_identity_122b}} | {{num|rtk_C2_keep_jpp_identity_muse}} |

*°: after the data, the gate lowered to 0.75.*

![The routes test: each route predicts a different locker](figures/story/fig3_routes_design.png)
![The lookup follows identity or position, never the value](figures/story/fig4_routes.png)
*Fig. 3, Fig. 4. Blue: identity; orange: position; no green (value). Hatched: 122B, after the data, gate 0.75.*

## 3. The pointer: remove it, write it

*Removal after the data (replicated in advance on the 9B and Muse); routes arms and writes fixed in advance; the writes' recall split after the data.*

- **What we did.** (a) Probed the bridge word for which sentence holds the item's locker; removed the 4 **pointer directions** that separate those answers, or added only them. (b) Wrote one fixed vector per slot pair (two slots' mean states' difference) at three doses, against a random direction of the same size.
- **What we found.**
  - (a) The probe is right in {{num|v4_b_before_122b}}-{{num|v4_b_before_27b}} of scenes (layout alone: {{num|v4_b_layout_before_27b}}), almost none of it in J++, and points at the item's first mention, even another person's earlier pick. Removing the pointer directions costs the lookup on every model, the recall less, and cuts position answers; adding only them gives position answers on all but the 27B.
  - (b) At the dose fixed in advance (s = 1) the write moves nothing. Stronger writes send the lookup to the target locker and a random direction does not; when the recall changes under the strongest write, it mostly gives the target slot's item (table, Fig. 8). Muse pending.

| Pointer directions | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B° | Muse Glimmer 30B |
|---|---|---|---|---|
| Lookup's extra loss without them | {{num|rep_alf_lk_excess_9b}} (replicated) | {{num|mmlf_Alf_lk_excess_27b}} | {{num|mmlf_Alf_lk_excess_122b}} | {{num|rep_alf_lk_excess_muse}} (replicated) |
| Position without them / without a random part of their size | {{num|rt_C2_no_alf_position_9b}} / {{num|rt_C2_no_alf_rand_position_9b}} | {{num|rt_C2_no_alf_position_27b}} / {{num|rt_C2_no_alf_rand_position_27b}} | {{num|rtg_C2_no_alf_position_122b}} / {{num|rtg_C2_no_alf_rand_position_122b}} | {{num|rt_C2_no_alf_position_muse}} / {{num|rt_C2_no_alf_rand_position_muse}} |
| Write, lookup's target share: s = 1 / 2 / 4; random direction, 4 | {{num|x8_t1_9b}} / {{num|x8_t2_9b}} / {{num|x8_t4_9b}}; {{num|x8_rand4_9b}} | {{num|x8_t1_27b}} / {{num|x8_t2_27b}} / {{num|x8_t4_27b}}; {{num|x8_rand4_27b}} | {{num|x8_t1_122b}} / {{num|x8_t2_122b}} / {{num|x8_t4_122b}}; {{num|x8_rand4_122b}} | not landed |
| Write at s = 4: changed recalls giving the target slot's item | {{num|x8_rc_target_9b}} | {{num|x8_rc_target_27b}} | {{num|x8_rc_target_122b}} | not landed |
| Position with only their part / only a random part of its size | {{num|rtk_C2_keep_alf_position_9b}} / {{num|rtk_C2_keep_alf_rand_position_9b}} | {{num|rtk_C2_keep_alf_position_27b}} / {{num|rtk_C2_keep_alf_rand_position_27b}} | {{num|rtk_C2_keep_alf_position_122b}} / {{num|rtk_C2_keep_alf_rand_position_122b}} | {{num|rtk_C2_keep_alf_position_muse}} / {{num|rtk_C2_keep_alf_rand_position_muse}} |

*°: after the data, the gate lowered to 0.75.*

![Writing the pointer: one fixed vector per slot pair, against a random direction](figures/story/fig8_writes.png)
*Fig. 8. The dose fixed in advance (s = 1) moves nothing on any model; s\* marks a real pointer change's size. The real change's pointer part does not move the lookup between slots 1 and 2 either, while the whole change does: our 4 directions miss how the model tells later slots apart.*

## 4. How far the pointer reaches

*After the data, except the transfer bars and the identity direction, fixed in advance.*

- **First sentence.** The pointer directions we found mostly mark whether the item's mention was the prompt's first sentence (Fig. 9a). In the routes test only their part moves the lookup to or from slot 0, not between slots 1 and 2, while the whole change does (Fig. 9b): the position route exists for other places too, mostly outside these directions.
- **Transfer.** Fit on simple scenes and not refit, they cost the lookup {{num|tptr_varied_range}} in varied scenes and {{num|tptr_natural_range}} in natural passages, while the lookup still does not need J++ there (Fig. 10).
- **What is left.** J++ and the pointer directions removed together leave about half of the sanity swap's lookups switching, and cost more than the pointer alone only on the 27B. Adding the item's identity outside J++ leaves fewer, but a random part of the same share removes most switches too (Fig. 6, table). About half of the route around the lens is still unexplained. The recall needs identity on the 27B and Muse, not the 9B.
- **A pointer found without slot labels** is pending on three models.

| Pointer directions, by where the item sits | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| Lookup's extra loss without them: first sentence / first locker, not first / neither | {{num|fs_groups_9b}} | {{num|fs_groups_27b}} | {{num|fs_groups_122b}} | {{num|fs_groups_muse}} |
| Same, first sentence minus the rest | {{num|fs_diff_9b}} | {{num|fs_diff_27b}} | {{num|fs_diff_122b}} | {{num|fs_diff_muse}} |
| Only their part's switch rate, first sentence minus the rest | {{num|fs_keepdiff_9b}} | {{num|fs_keepdiff_27b}} | {{num|fs_keepdiff_122b}} | {{num|fs_keepdiff_muse}} |
| Routes, only their part: moves from or to slot 0 / 1 → 2 and 2 → 1 | {{num|pm_keep_slot0_9b}} / {{num|pm_keep_12_9b}} | {{num|pm_keep_slot0_27b}} / {{num|pm_keep_12_27b}} | {{num|pm_keep_slot0_122b}} / {{num|pm_keep_12_122b}} | {{num|pm_keep_slot0_muse}} / {{num|pm_keep_12_muse}} |
| Routes, the whole change: 1 → 2 / 2 → 1 | {{num|pm_whole_12_9b}} | {{num|pm_whole_12_27b}} | {{num|pm_whole_12_122b}} | {{num|pm_whole_12_muse}} |
| Varied scenes, lookup's extra loss without them | {{num|tptr_pooled_9b}} | {{num|tptr_pooled_27b}} | {{num|tptr_pooled_122b}} | {{num|tptr_pooled_muse}} |
| Same: prose / json / table | {{num|tptr_split_9b}} | {{num|tptr_split_27b}} | {{num|tptr_split_122b}} | {{num|tptr_split_muse}} |
| Natural passages (the fact before the bridge) | {{num|tptr_natural_9b}} | {{num|tptr_natural_27b}} | {{num|tptr_natural_122b}} | {{num|tptr_natural_muse}} |
| Sanity swap, both removed minus the pointer alone | {{num|rtb_ex_C0_both_minus_alf_lk_9b}} | {{num|rtb_ex_C0_both_minus_alf_lk_27b}} | {{num|rtb_ex_C0_both_minus_alf_lk_122b}}° | {{num|rtb_ex_C0_both_minus_alf_lk_muse}} |
| Lookups still switching: J++ and the pointer removed | {{num|rtc_left_C0_alf_jpp_lk_9b}} | {{num|rtc_left_C0_alf_jpp_lk_27b}} | {{num|rtc_left_C0_alf_jpp_lk_122b}}° | {{num|rtc_left_C0_alf_jpp_lk_muse}} |
| Same, with identity outside J++ / its random part | {{num|rtd_left_C0_jpp+alf+idout_lk_9b}} / {{num|rtd_randleft_C0_jpp+alf+idout_lk_9b}} | {{num|rtd_left_C0_jpp+alf+idout_lk_27b}} / {{num|rtd_randleft_C0_jpp+alf+idout_lk_27b}} | not run | {{num|rtd_left_C0_jpp+alf+idout_lk_muse}} / {{num|rtd_randleft_C0_jpp+alf+idout_lk_muse}} |
| Recall's extra loss without identity | {{num|rtd_ex_C0_id_rc_9b}} | {{num|rtd_ex_C0_id_rc_27b}} | not run | {{num|rtd_ex_C0_id_rc_muse}} |
| Switches lost: pointer + J++ minus pointer + random | {{num|rtc_lost_C0_jpp_minus_rand_lk_9b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_27b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_122b}}° | {{num|rtc_lost_C0_jpp_minus_rand_lk_muse}} |

*°: after the data, the gate lowered to 0.75 (the routes and sanity-swap rows of the 122B).*

![Our pointer directions mostly mark the first sentence; the model tells later places apart without them](figures/story/fig9_first_sentence.png)
![The split travels; our pointer does not](figures/story/fig10_transfer.png)
![Removing J++, the pointer directions and identity together](figures/story/fig6_both_removed.png)
*Fig. 9, Fig. 10, Fig. 6. Fig. 6: dots against dotted bars; grey: recall; each part's share of the change on its bar.*

## 5. Depth (candidate)

*Candidate, after the data; the routes test's layers fixed in advance (Muse's two layers too).*

- **What we found.**
  - Early, the lookup follows identity only; without J++ the Qwens give the original answer (table). Position appears by layer 12 (9B), 28 (27B), 33 (122B), 26 (Muse); the rule fixed in advance holds on the 9B only.
  - The recall needs J++ most where the pick is the bridge's first mention (table below; the full table in [docs/x0_details.md](docs/x0_details.md)).
- **Caveat.** On the 27B the lookup stops needing J++ at layer 24, four layers before position answers appear (28).
- **Muse.** At L26 the whole change moves only {{num|lk_swhole_pct_muse}}-{{num|single_lk_swhole_pct_muse}} of lookups; L34 not tested (no lookup switched).

| Early layer, another item moved | Qwen3.5-9B (L6) | Qwen3.6-27B (L16) | Qwen3.5-122B (L27)° | Muse Glimmer 30B (L13) |
|---|---|---|---|---|
| Identity share | {{num|rte_C2_whole_identity_9b}} | {{num|rte_C2_whole_identity_27b}} | {{num|rte_C2_whole_identity_122b}} | {{num|rte_C2_whole_identity_muse}} |
| Without J++: the original answer | {{num|rte_C2_no_jpp_original_9b}} | {{num|rte_C2_no_jpp_original_27b}} | {{num|rte_C2_no_jpp_original_122b}} | {{num|rte_C2_no_jpp_original_muse}} |

| Swap | Pick is the first mention? | Qwen3.5-9B lookup | Qwen3.5-9B recall | Qwen3.6-27B lookup | Qwen3.6-27B recall | Qwen3.5-122B lookup | Qwen3.5-122B recall | Muse Glimmer 30B lookup | Muse Glimmer 30B recall |
|---|---|---|---|---|---|---|---|---|---|
| Two people swap picks | yes | {{num|comp_two_fmyes_lk_cell_9b}} | {{num|comp_two_fmyes_rc_9b}} | {{num|comp_two_fmyes_lk_cell_27b}} | {{num|comp_two_fmyes_rc_27b}} | {{num|comp_two_fmyes_lk_cell_122b}} | {{num|comp_two_fmyes_rc_122b}} | {{num|comp_two_fmyes_lk_cell_muse}} | {{num|comp_two_fmyes_rc_muse}} |
| Two people swap picks | no | {{num|comp_two_fmno_lk_cell_9b}} | {{num|comp_two_fmno_rc_9b}} | {{num|comp_two_fmno_lk_cell_27b}} | {{num|comp_two_fmno_rc_27b}} | {{num|comp_two_fmno_lk_cell_122b}} | {{num|comp_two_fmno_rc_122b}} | {{num|comp_two_fmno_lk_cell_muse}} | {{num|comp_two_fmno_rc_muse}} |
| Only the asked person's pick changes | yes | {{num|comp_one_fmyes_lk_cell_9b}} | {{num|comp_one_fmyes_rc_9b}} | {{num|comp_one_fmyes_lk_cell_27b}} | {{num|comp_one_fmyes_rc_27b}} | {{num|comp_one_fmyes_lk_cell_122b}} | {{num|comp_one_fmyes_rc_122b}} | {{num|comp_one_fmyes_lk_cell_muse}} | {{num|comp_one_fmyes_rc_muse}} |
| Only the asked person's pick changes | no | {{num|comp_one_fmno_lk_cell_9b}} | {{num|comp_one_fmno_rc_9b}} | {{num|comp_one_fmno_lk_cell_27b}} | {{num|comp_one_fmno_rc_27b}} | {{num|comp_one_fmno_lk_cell_122b}} | {{num|comp_one_fmno_rc_122b}} | {{num|comp_one_fmno_lk_cell_muse}} | {{num|comp_one_fmno_rc_muse}} |

*°: gate 0.75; J++ extra loss, after the data; italics: under 30 lookup switches (count shown).*

![Position answers appear with depth; on the 9B and 122B where the lookup stops needing J++](figures/story/fig5_depth.png)
*Fig. 5. Shaded where the lookup still needs J++ (at least 0.30); Muse: the main test at layers 8-32 (after the data).*

## 6. What did not hold

![What held where: the claims on four models](figures/story/fig7_scorecard.png)
*Fig. 7. Filled: fixed in advance; open: after the data or a lowered gate.*

- **Failed when fixed in advance.**
  - The 27B's strict rule: lookup lost {{num|lk_excess_27b}} (bar 0.10).
  - The 9B's replication: its J++ clause failed (recall {{num|rep_jpp_rc_excess_9b}}).
  - The positive control (chemical symbols) stayed below its 0.20 bar: 27B {{num|x4_D_elements_27b}}.
  - Removing the identity direction alone cut the identity route on the 27B only.
  - Gates missed (bar 0.80), not tested: the 9B's natural passages (lookup {{num|nat_gate_lk_9b}}), the 122B's routes (recall {{num|rt_c0gate_rc_122b}}) and replication (recall {{num|rep_gate_rc_122b}}); reruns at 0.75 are descriptive.
- **Design errors.**
  - The write's dose fixed in advance, s = 1, was below a real change's size on every pair (s needed: {{num|x8_sreal_9b}}; {{num|x8_sreal_27b}}; {{num|x8_sreal_122b}}; {{num|x8_sreal_muse}}).
  - The bar for J++, the pointer and identity removed together was out of reach at their share: the random part alone removes most switches on the Qwens.
- **Limits.**
  - The pointer directions are fit on 5 slot labels and carry mostly first-vs-rest; the code for later slots is not captured (per-move table).
  - The locker number at the bridge word: never the answer; digit directions cost {{num|dig_lk_jppdig_k10_before_27b}}.
  - One-token answers and bridges; the reader is confounded with the answer's source (prompt vs memory). The 122B in FP8.
  - Zach's knock-out finds the split weak outside Qwen; our change-removal finds it on Muse.

## 7. How we checked

- **Hand-checked numbers.** None yet ([docs/review_summary.md](docs/review_summary.md)); [docs/verify_pack.md](docs/verify_pack.md) recounts each claim's numbers from the per-item files.
- **Raw examples.** `make review-serve`: random items per claim (fixed seed), as the model saw them.
- **Predictions.** Committed before results are opened, then scored ([predictions/](predictions/README.md)): mean Brier {{num|pred_brier}} over {{num|pred_n}} answers, worse than always answering {{q|50%}}; the mechanistic questions were mostly wrong.
- **Inventory.** [docs/inventory.md](docs/inventory.md): pre-pivot experiments are kept and labelled legacy.

## 8. Related work and what is new

Language models bind an entity to its attributes in context (Feng & Steinhardt 2023) and track entities through pointer-like mechanisms (Prakash et al.); the order of bound entities lives in a low-dimensional subspace (Dai et al. 2024). Two-hop recall resolves its bridge early (Biran et al. 2024). Our routes test sets identity, position and value against each other as in Gur-Arieh et al. (2025); the pointer directions are mass-mean directions (Marks & Tegmark 2023); a part that moves an answer when added alone can mislead (Makelov et al. 2023), so every part has a random part of its size beside it. The lens is the workspace paper's J++ (Gurnee et al. 2026). New here: two readers of one word need different parts of it, the lens-readable part only for recall; our pointer directions mostly mark the first sentence; one fixed vector steers the lookup.

## 9. Next

- **Running now.** Muse's transfer and writes; a pointer found without slot labels.
- **Follow-up: answers by sampling**, not the top token.
- **Follow-up: the routes and pointer tests without the chat template.**
- **Follow-up: OLMo checkpoints**, to see when in training the pointer appears.
- **Later.** New datasets; intermediates in reasoning traces; DeepSeek-V4-Flash (about four H200s or native FP4; its lens's residual stream unnamed).

## Appendix A. Links

Every number on this page comes from [figures/story/data.csv](figures/story/data.csv) (also every plotted number) and [docs/x0_numbers.json](docs/x0_numbers.json), each with its source file; [docs/x0_details.md](docs/x0_details.md) has the full tables; [docs/verify_pack.md](docs/verify_pack.md) recounts them. Earlier figures: [figures/status_2026-10-25/](figures/status_2026-10-25/).
