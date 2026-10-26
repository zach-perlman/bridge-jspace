<!-- grid: results/cross_model/20261023T210238Z -->
# The lookup goes around the lens: what a model reads from the bridge word

*When a model answers a two-step question, does it use the part of the in-between entity that a lens can read, and does that depend on what it does with that entity next?*

## In one minute

- Recall needs the lens-readable (J++) part of the bridge; the lookup mostly doesn't, on three Qwen models and a second family, Muse Glimmer 30B (rule fixed in advance; strict on all but the 27B), clearest in simple scenes.
- The lookup's route around the lens runs through the pointer on 3 of 4 models (9B, 122B, Muse): directions that say where the item was first mentioned. The 27B leans on identity, partly inside J++.
- New here: the readers' split; the pointer directions' causal role (necessary on 4 of 4 models, sufficient for position answers on 3 of 4); and depth: early the bridge carries only the item's identity, inside J++; later it adds the pointer, which only the lookup uses (candidate; Section 3).

![Recall needs the J++ part; the lookup mostly doesn't](figures/story/fig1_readers.png)
*Fig. 1. Lookup against recall in each row; grey band: not needed. Muse's natural passages: no gap (few lookup switches).*

**Status.** Qwen3.5-9B, Qwen3.6-27B, Qwen3.5-122B-A10B and Muse Glimmer 30B (another family); 26 Oct 2026. All numbers unverified until hand-checked (Section 5). Built at {{head}} from the run files.

## Setup

![One prompt, two questions about the same in-between word](figures/story/fig0_setup.png)

The **bridge** is the item Iris picked (*frog*). The **lookup** asks for its locker, written in the prompt; the **recall** asks for a fact from memory. We swap the bridge (frog → tick), take **the change** in the hidden state at the bridge word at one layer, and add it into the original prompt there: whole, without its **J++ part** (the 25 lens directions that best rebuild it), or without a random part of the same size. A reader switches when it gives the swapped bridge's answer. **Extra loss** = the share of switches lost without the J++ part minus the share lost without the random part. **Gap** = the recall's extra loss minus the lookup's. **Matched scenes**: the asked pick is not the bridge's first mention. Brackets: {{q|95%}} bootstrap intervals.

## 1. Recall needs the lens-readable part of the bridge; the lookup mostly doesn't

*Fixed in advance (main test; Muse's whole grid); other settings: pass bars set before each run.*

- **Question.** Does removing the J++ part of the change cost the recall more than the lookup?
- **What we did.** One layer per model fixed in advance; 200 scenes (two people swap picks), then other scene sets and parts of the same size.
- **What we found.**
  - The gap is positive wherever measured (table). The strict rule held on the 9B, the 122B and Muse; on the 27B the lookup lost {{num|lk_excess_27b}}, over its 0.10 bar. In matched scenes the gap is smaller, clearest on the 27B and Muse.
  - It shrinks outside simple scenes; Muse's stays the largest.
  - On the 27B the lookup needs J++ once more directions are removed (25 / 50 / 100: {{num|lk_excess_k25_27b}} / {{num|lk_excess_k50_27b}} / {{num|lk_excess_k100_27b}}; gap {{num|contrast_k100_27b}} at 100); the 9B, 122B and Muse keep the gap ({{num|contrast_k100_9b}}, {{num|contrast_k100_122b}}, {{num|contrast_k100_muse}}).
  - Other parts of a similar size cost the recall less than J++ (Fig. 2); J++ fitted to another scene holds only {{num|jppother_jpp_other_share_27b}}-{{num|jppother_jpp_other_share_9b}} of the change, so it does not test this.

| Gap | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| Two people swap picks (fixed in advance) | {{num|contrast_9b}} | {{num|contrast_27b}} | {{num|contrast_122b}} | {{num|contrast_muse}} |
| Matched: fresh scenes, both locker sentences first, only the asked pick changes | {{num|comp_rep_both_gap_9b}} | {{num|comp_rep_both_gap_27b}} | {{num|comp_rep_both_gap_122b}}° | {{num|comp_rep_both_gap_muse}} |
| Varied scenes | {{num|x0b_c_9b}} | {{num|x0b_c_27b}} | {{num|x0b_c_122b}} | {{num|x0b_c_muse}} |
| Natural passages | {{num|natg75_gap_9b}}° | {{num|nat_gap_27b}} | {{num|nat_gap_122b}} | recall {{num|nat_rc_excess_muse}}, lookup {{num|nat_lk_excess_muse}} ({{num|nat_n_muse}} passages) |

*°: after the data, the gate lowered to 0.75.*

![No other part costs the recall as much as the scene's own J++](figures/story/fig2_parts.png)
*Fig. 2. †: two people swap picks; others: only the asked pick changes.*

- **Caveat.** On the 122B the main directions at J++'s share cost the recall almost as much as J++ ({{num|pcaeq_pca_eq_rc_excess_122b}} vs {{num|pcaeq_jpp_rc_excess_122b}}).

## 2. What the lookup reads instead: which item, and where it was first mentioned

*After the data; the routes test (2c) and Muse's grid fixed in advance.*

- **Question.** What does the lookup take from the bridge word instead?
- **What we did.** (a) Split lookups by sentence order. (b) Probed the bridge word for which sentence holds the item's locker, and removed the 4 **pointer** directions that separate those answers. (c) Swapped prompts where identity, position and value predict different lockers (Fig. 3); parts removed or added alone.
- **What we found.**
  - (a) Lookups switch in {{num|lk_order_before_27b}}-{{num|lk_order_before_122b}} of locker-first scenes and {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} otherwise; lookup claims here are about locker-first scenes. On the 27B's natural passages the lookup switches mostly when the fact comes first ({{num|natsplit_before_lk_sw_27b}} of {{num|natsplit_before_n_27b}} vs {{num|natsplit_after_lk_sw_27b}} of {{num|natsplit_after_n_27b}}) and needs J++ where it does ({{num|natsplit_before_lk_27b}}): the route around the lens is weaker in natural text.
  - (b) The probe is right in {{num|v4_b_before_122b}}-{{num|v4_b_before_27b}} of scenes (layout alone: {{num|v4_b_layout_before_27b}}), almost none of it in J++. A probe shows the pointer is decodable, not that it is used; the causal claims rest on removing the pointer directions and on adding them alone. The probe points at the item's first mention, even another person's earlier pick, where the lookup still switches. Removing the pointer directions costs the lookup on every model, the recall less (table).
  - (c) When another item moved, the lookup follows its identity or its locker sentence's position, never the new value (Fig. 4). Removing the pointer directions cuts position; adding only them gives position answers on all but the 27B; the J++ part alone moves none.

| | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B° | Muse Glimmer 30B |
|---|---|---|---|---|
| Lookup's extra loss without the pointer directions | {{num|rep_alf_lk_excess_9b}} (replicated) | {{num|mmlf_Alf_lk_excess_27b}} | {{num|mmlf_Alf_lk_excess_122b}} | {{num|rep_alf_lk_excess_muse}} (replicated) |
| Same, varied scenes (directions fit on the simple scenes) | {{num|tptr_pooled_9b}} | {{num|tptr_pooled_27b}} | {{num|tptr_pooled_122b}} | {{num|tptr_pooled_muse}} |
| Same, varied scenes: prose / json / table | {{num|tptr_split_9b}} | {{num|tptr_split_27b}} | {{num|tptr_split_122b}} | {{num|tptr_split_muse}} |
| Same, natural passages (the fact before the bridge) | {{num|tptr_natural_9b}} | {{num|tptr_natural_27b}} | {{num|tptr_natural_122b}} | {{num|tptr_natural_muse}} |
| Another item moved: identity / position | {{num|rt_C2_whole_identity_9b}} / {{num|rt_C2_whole_position_9b}} | {{num|rt_C2_whole_identity_27b}} / {{num|rt_C2_whole_position_27b}} | {{num|rtg_C2_whole_identity_122b}} / {{num|rtg_C2_whole_position_122b}} | {{num|rt_C2_whole_identity_muse}} / {{num|rt_C2_whole_position_muse}} |
| Position without the pointer directions / without a random part of their size | {{num|rt_C2_no_alf_position_9b}} / {{num|rt_C2_no_alf_rand_position_9b}} | {{num|rt_C2_no_alf_position_27b}} / {{num|rt_C2_no_alf_rand_position_27b}} | {{num|rtg_C2_no_alf_position_122b}} / {{num|rtg_C2_no_alf_rand_position_122b}} | {{num|rt_C2_no_alf_position_muse}} / {{num|rt_C2_no_alf_rand_position_muse}} |
| Position with only the pointer part / only a random part of its size | {{num|rtk_C2_keep_alf_position_9b}} / {{num|rtk_C2_keep_alf_rand_position_9b}} | {{num|rtk_C2_keep_alf_position_27b}} / {{num|rtk_C2_keep_alf_rand_position_27b}} | {{num|rtk_C2_keep_alf_position_122b}} / {{num|rtk_C2_keep_alf_rand_position_122b}} | {{num|rtk_C2_keep_alf_position_muse}} / {{num|rtk_C2_keep_alf_rand_position_muse}} |

*°: after the data, the gate lowered to 0.75 (varied and natural rows: 0.80).*

![The routes test: each route predicts a different locker](figures/story/fig3_routes_design.png)
![The lookup follows identity or position, never the value](figures/story/fig4_routes.png)
*Fig. 3, Fig. 4. Blue: identity; orange: position; no green (value). Hatched: 122B, after the data, gate 0.75.*

- **Caveat.** Same item moved: a random part of the pointer's size also removed position (F20).
- **Scope.** The pointer directions explain the route around the lens in simple scenes; fitted there and not refit, they cost the lookup {{num|tptr_varied_range}} in varied scenes and {{num|tptr_natural_range}} in natural passages, while the lookup still does not need J++ there. Whether a pointer fit on those texts does better: P_cf (pending).

## 3. Why the readers split: with depth the bridge adds a pointer the lens can't see

*Candidate, after the data; 3a's layers and 3b's bar fixed in advance (Muse's two layers too).*

- **Question.** Does the split come with depth?
- **What we did.** (a) The routes test at more layers (9B 6-12, 27B 16-32, 122B 24-36, Muse 13 and 26). (b) J++ and the pointer directions removed together in the sanity swap. (c) Matched scenes against the rest. (d) The item's identity as one direction (the difference of the two items' mean states, outside J++), removed with both (9B, 27B, Muse; fixed in advance).
- **What we found.**
  - (a) Early, the lookup follows identity only; without J++ the Qwens give the original answer (table). Position appears by layer 12 (9B), 28 (27B), 33 (122B) and 26 (Muse); the rule fixed in advance (9B and 27B; the 122B's layers after the data) holds on the 9B only.
  - (b) Removing both costs the lookup more than the pointer alone, and more than the pointer with a random part of J++'s size, only on the 27B (bars fixed in advance, 0.15; table). J++ and the pointer directions removed together still leave about half of the lookups switching ({{num|rtc_left_C0_alf_jpp_lk_9b}} on the 9B, {{num|rtc_left_C0_alf_jpp_lk_27b}} on the 27B): these two parts explain about half of the route around the lens. On the 9B a random part of J++'s size costs the lookup more than J++, so its second route is not in J++; in these scenes (the item already mentioned) the 9B's recall does not need J++ either ({{num|rtc_ex_C0_jpp_rc_9b}}), as table 3c predicts. The 27B is the case where the same scenes show the split and its mechanism.
  - (c) The recall needs J++ most where the pick is the bridge's first mention (table 3c).
  - (d) With identity added, {{num|rtd_left_C0_jpp+alf+idout_lk_9b}} (9B), {{num|rtd_left_C0_jpp+alf+idout_lk_27b}} (27B) and {{num|rtd_left_C0_jpp+alf+idout_lk_muse}} (Muse) of the sanity swap's lookups still switch, against {{num|rtd_randleft_C0_jpp+alf+idout_lk_9b}}, {{num|rtd_randleft_C0_jpp+alf+idout_lk_27b}} and {{num|rtd_randleft_C0_jpp+alf+idout_lk_muse}} without a random part of the same share: below the 0.80 bar fixed in advance, which the random part alone put out of reach on the Qwens. The recall needs identity on the 27B and Muse ({{num|rtd_ex_C0_id_rc_27b}}, {{num|rtd_ex_C0_id_rc_muse}}), not the 9B ({{num|rtd_ex_C0_id_rc_9b}}).

| Early layer, another item moved, and the sanity swap | Qwen3.5-9B (L6) | Qwen3.6-27B (L16) | Qwen3.5-122B (L27)° | Muse Glimmer 30B (L13) |
|---|---|---|---|---|
| Identity share | {{num|rte_C2_whole_identity_9b}} | {{num|rte_C2_whole_identity_27b}} | {{num|rte_C2_whole_identity_122b}} | {{num|rte_C2_whole_identity_muse}} |
| Without J++: the original answer | {{num|rte_C2_no_jpp_original_9b}} | {{num|rte_C2_no_jpp_original_27b}} | {{num|rte_C2_no_jpp_original_122b}} | {{num|rte_C2_no_jpp_original_muse}} |
| **Sanity swap, at the layer fixed in advance** | **Qwen3.5-9B** | **Qwen3.6-27B** | **Qwen3.5-122B°** | **Muse Glimmer 30B** |
| Both removed minus the pointer alone (lookup extra loss) | {{num|rtb_ex_C0_both_minus_alf_lk_9b}} | {{num|rtb_ex_C0_both_minus_alf_lk_27b}} | {{num|rtb_ex_C0_both_minus_alf_lk_122b}} | {{num|rtb_ex_C0_both_minus_alf_lk_muse}} |
| Switches lost: pointer + J++ minus pointer + random | {{num|rtc_lost_C0_jpp_minus_rand_lk_9b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_27b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_122b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_muse}} |
| Lookups still switching with both removed | {{num|rtc_left_C0_alf_jpp_lk_9b}} | {{num|rtc_left_C0_alf_jpp_lk_27b}} | {{num|rtc_left_C0_alf_jpp_lk_122b}} | {{num|rtc_left_C0_alf_jpp_lk_muse}} |

*°: after the data, the gate lowered to 0.75.*

![Position answers appear with depth; on the 9B and 122B where the lookup stops needing J++](figures/story/fig5_depth.png)
![Removing J++ and the pointer directions together](figures/story/fig6_both_removed.png)
*Fig. 5: shaded where the lookup still needs J++ (at least 0.30); Muse: the main test at layers 8-32 (after the data), its routes L34 not tested. Fig. 6: dots against dotted bars; grey: recall.*

| Swap | Pick is the first mention? (no = matched) | Qwen3.5-9B lookup | Qwen3.5-9B recall | Qwen3.6-27B lookup | Qwen3.6-27B recall | Qwen3.5-122B lookup | Qwen3.5-122B recall | Muse Glimmer 30B lookup | Muse Glimmer 30B recall |
|---|---|---|---|---|---|---|---|---|---|
| Two people swap picks | yes | {{num|comp_two_fmyes_lk_cell_9b}} | {{num|comp_two_fmyes_rc_9b}} | {{num|comp_two_fmyes_lk_cell_27b}} | {{num|comp_two_fmyes_rc_27b}} | {{num|comp_two_fmyes_lk_cell_122b}} | {{num|comp_two_fmyes_rc_122b}} | {{num|comp_two_fmyes_lk_cell_muse}} | {{num|comp_two_fmyes_rc_muse}} |
| Two people swap picks | no | {{num|comp_two_fmno_lk_cell_9b}} | {{num|comp_two_fmno_rc_9b}} | {{num|comp_two_fmno_lk_cell_27b}} | {{num|comp_two_fmno_rc_27b}} | {{num|comp_two_fmno_lk_cell_122b}} | {{num|comp_two_fmno_rc_122b}} | {{num|comp_two_fmno_lk_cell_muse}} | {{num|comp_two_fmno_rc_muse}} |
| Only the asked person's pick changes | yes | {{num|comp_one_fmyes_lk_cell_9b}} | {{num|comp_one_fmyes_rc_9b}} | {{num|comp_one_fmyes_lk_cell_27b}} | {{num|comp_one_fmyes_rc_27b}} | {{num|comp_one_fmyes_lk_cell_122b}} | {{num|comp_one_fmyes_rc_122b}} | {{num|comp_one_fmyes_lk_cell_muse}} | {{num|comp_one_fmyes_rc_muse}} |
| Only the asked person's pick changes | no | {{num|comp_one_fmno_lk_cell_9b}} | {{num|comp_one_fmno_rc_9b}} | {{num|comp_one_fmno_lk_cell_27b}} | {{num|comp_one_fmno_rc_27b}} | {{num|comp_one_fmno_lk_cell_122b}} | {{num|comp_one_fmno_rc_122b}} | {{num|comp_one_fmno_lk_cell_muse}} | {{num|comp_one_fmno_rc_muse}} |
| Same, fresh scenes | no | {{num|comp_rep_fmno_lk_cell_9b}} | {{num|comp_rep_fmno_rc_9b}} | {{num|comp_rep_fmno_lk_cell_27b}} | {{num|comp_rep_fmno_rc_27b}} | {{num|comp_rep_fmno_lk_cell_122b}}° | {{num|comp_rep_fmno_rc_122b}}° | {{num|comp_rep_fmno_lk_cell_muse}} | {{num|comp_rep_fmno_rc_muse}} |

*J++ extra loss, after the data; °: gate 0.75; italics: under 30 lookup switches (count shown); n in Appendix A.*

- **Caveat.** On the 27B the lookup stops needing J++ at layer 24, four layers before position answers appear (28): there the pointer is not the whole reason. Removing both costs the recall too ({{num|rtb_ex_C0_both_rc_9b}}, {{num|rtb_ex_C0_both_rc_27b}}).
- **Muse.** At L26 the whole change moves only {{num|lk_swhole_pct_muse}}-{{num|single_lk_swhole_pct_muse}} of lookups and about {{num|rc_swhole_pct_muse}} of recalls; without the pointer directions position falls to {{num|rt_C2_no_alf_position_muse}} (random part {{num|rt_C2_no_alf_rand_position_muse}}), not near zero (the early layer: table above); L34 not tested (no lookup switched).

## 4. What did not hold, and limits

![What held where: ten claims on four models](figures/story/fig7_scorecard.png)
*Fig. 7. Filled: fixed in advance; open: after the data or a lowered gate. Only the asked pick changing: confirmed on all four (Appendix A).*

- The 27B's strict rule: lookup lost {{num|lk_excess_27b}} (bar 0.10).
- The 9B's fixed-in-advance replication: its J++ clause failed (recall {{num|rep_jpp_rc_excess_9b}}).
- The gap everywhere: the 122B's varied scenes ({{num|x0b_c_122b}}, every format alike) and the 27B's natural passages ({{num|nat_gap_27b}}) are in between.
- Writing the pointer: s = 1, fixed in advance, was below a real change's size on every pair (s needed: {{num|x8_sreal_9b}}; {{num|x8_sreal_27b}}; {{num|x8_sreal_122b}}; {{num|x8_sreal_muse}}): a design error, not a finding.
- The pointer directions are fit on 5 slot labels and carry mostly first-vs-rest; the code for later slots is not captured (per-move table).
- The locker number at the bridge word: never the answer; digit directions cost {{num|dig_lk_jppdig_k10_before_27b}}. The positive control (chemical symbols) stayed below its 0.20 bar: 27B {{num|x4_D_elements_27b}}.
- Gates missed (bar 0.80), not tested: the 9B's natural passages (lookup {{num|nat_gate_lk_9b}}), the 122B's routes (recall {{num|rt_c0gate_rc_122b}}) and replication (recall {{num|rep_gate_rc_122b}}); reruns at 0.75 are descriptive. The 122B in FP8.
- One-token answers and bridges. The reader is confounded with the answer's source (prompt vs memory).
- Zach's knock-out finds the split weak outside Qwen; our change-removal finds it on Muse (different measures).

## 5. How we checked

- **Hand-checked numbers.** None yet ([docs/review_summary.md](docs/review_summary.md)); [docs/verify_pack.md](docs/verify_pack.md) recounts each claim's numbers from the per-item files.
- **Raw examples.** `make review-serve`: random items per claim (fixed seed), as the model saw them.
- **Predictions.** Committed before results are opened, then scored ([predictions/](predictions/README.md)): mean Brier {{num|pred_brier}} over {{num|pred_n}} answers, worse than always answering {{q|50%}}; the mechanistic questions were mostly wrong.
- **"Fixed in advance"**: test, layer, sample and bar committed before any result; "after the data": chosen after seeing results.
- **Inventory.** [docs/inventory.md](docs/inventory.md): pre-pivot experiments are kept and labelled legacy.

## 6. Next

- **Running now.** The pointer directions in Muse's varied scenes and natural passages; a pointer found without slot labels (P_cf); writing the pointer on Muse.

![Writing the pointer: one fixed vector per slot pair, against a random direction](figures/story/fig8_writes.png)
*Fig. 8. The dose fixed in advance (s = 1) moves nothing on any model; s\* marks a real pointer change's size. The real change's pointer part does not move the lookup between slots 1 and 2 either, while the whole change does: our 4 directions miss how the model tells later slots apart.*

- **Follow-up: answers by sampling**, not the top token.
- **Follow-up: the routes and pointer tests without the chat template.**
- **Follow-up: OLMo checkpoints**, to see when in training the pointer appears.
- **Later.** New datasets; intermediates in reasoning traces; DeepSeek-V4-Flash (about four H200s or native FP4; its lens's residual stream unnamed).

## Appendix A. Key numbers

Every number on this page comes from [figures/story/data.csv](figures/story/data.csv) (also every plotted number) and [docs/x0_numbers.json](docs/x0_numbers.json), each with its source file; [docs/x0_details.md](docs/x0_details.md) has the full tables.

| Quantity | Qwen3.5-9B | Qwen3.6-27B | Qwen3.5-122B | Muse Glimmer 30B |
|---|---|---|---|---|
| Gap, two people swap picks | {{num|contrast_9b}} | {{num|contrast_27b}} | {{num|contrast_122b}} | {{num|contrast_muse}} |
| Gap, only the asked person's pick changes | {{num|single_contrast_9b}} | {{num|single_contrast_27b}} | {{num|single_contrast_122b}} | {{num|single_contrast_muse}} |
| Gap, varied scenes | {{num|x0b_c_9b}} | {{num|x0b_c_27b}} | {{num|x0b_c_122b}} | {{num|x0b_c_muse}} |
| Gap, natural passages (Muse: recall / lookup extra loss) | {{num|natg75_gap_9b}}° | {{num|nat_gap_27b}} | {{num|nat_gap_122b}} | {{num|nat_rc_excess_muse}} / {{num|nat_lk_excess_muse}} |
| Lookup, translated locker key minus verbatim | {{num|x4_D_animals_9b}} | {{num|x4_D_animals_27b}} | {{num|x4_D_animals_122b}} | {{num|x4_D_animals_muse}} |
| Recall, J++ / main directions at J++'s share | {{num|pcaeq_jpp_rc_excess_9b}} / {{num|pcaeq_pca_eq_rc_excess_9b}} | {{num|pcaeq_jpp_rc_excess_27b}} / {{num|pcaeq_pca_eq_rc_excess_27b}} | {{num|pcaeq_jpp_rc_excess_122b}} / {{num|pcaeq_pca_eq_rc_excess_122b}} | {{num|pcaeq_jpp_rc_excess_muse}} / {{num|pcaeq_pca_eq_rc_excess_muse}} |
| Lookup, pointer directions | {{num|mmlf_Alf_lk_excess_9b}} | {{num|mmlf_Alf_lk_excess_27b}} | {{num|mmlf_Alf_lk_excess_122b}} | {{num|mmlf_Alf_lk_excess_muse}} |
| n, table 3c rows (first mention yes / no): two people swap picks | {{num|comp_two_fmyes_n_9b}} / {{num|comp_two_fmno_n_9b}} | {{num|comp_two_fmyes_n_27b}} / {{num|comp_two_fmno_n_27b}} | {{num|comp_two_fmyes_n_122b}} / {{num|comp_two_fmno_n_122b}} | {{num|comp_two_fmyes_n_muse}} / {{num|comp_two_fmno_n_muse}} |
| n, table 3c rows: only the asked person's pick changes; fresh scenes (no) | {{num|comp_one_fmyes_n_9b}} / {{num|comp_one_fmno_n_9b}}; {{num|comp_rep_fmno_n_9b}} | {{num|comp_one_fmyes_n_27b}} / {{num|comp_one_fmno_n_27b}}; {{num|comp_rep_fmno_n_27b}} | {{num|comp_one_fmyes_n_122b}} / {{num|comp_one_fmno_n_122b}}; {{num|comp_rep_fmno_n_122b}}° | {{num|comp_one_fmyes_n_muse}} / {{num|comp_one_fmno_n_muse}}; {{num|comp_rep_fmno_n_muse}} |
| Pointer probe right; another person's earlier pick read as first mention | {{num|v4_b_before_9b}}; {{num|dup_otherfirst_reads_other_9b}} | {{num|v4_b_before_27b}}; {{num|dup_otherfirst_reads_other_27b}} | {{num|v4_b_before_122b}}; {{num|dup_otherfirst_reads_other_122b}} | {{num|v4_b_before_muse}}; {{num|dup_otherfirst_reads_other_muse}} |
| Routes, another item moved, position without the pointer / without a random part of its size | {{num|rt_C2_no_alf_position_9b}} / {{num|rt_C2_no_alf_rand_position_9b}} | {{num|rt_C2_no_alf_position_27b}} / {{num|rt_C2_no_alf_rand_position_27b}} | {{num|rtg_C2_no_alf_position_122b}} / {{num|rtg_C2_no_alf_rand_position_122b}}° | {{num|rt_C2_no_alf_position_muse}} / {{num|rt_C2_no_alf_rand_position_muse}} |
| Early layer, recall still switching without J++ | {{num|rte_C2_no_jpp_recall_follows_s_9b}} | {{num|rte_C2_no_jpp_recall_follows_s_27b}} | {{num|rte_C2_no_jpp_recall_follows_s_122b}}° | {{num|rte_C2_no_jpp_recall_follows_s_muse}} |
| Routes, position share at each tested layer (another item moved) | L6 {{num|rte_C2_whole_position_9b}}; L8 {{num|rts8_C2_whole_position_9b}}; L10 {{num|rts10_C2_whole_position_9b}}; L12 {{num|rt_C2_whole_position_9b}} | L16 {{num|rte_C2_whole_position_27b}}; L20 {{num|rts20_C2_whole_position_27b}}; L24 {{num|rts24_C2_whole_position_27b}}; L28 {{num|rts28_C2_whole_position_27b}}; L32 {{num|rt_C2_whole_position_27b}} | L24 {{num|rts24_C2_whole_position_122b}}; L27 {{num|rte_C2_whole_position_122b}}; L30 {{num|rts30_C2_whole_position_122b}}; L33 {{num|rtg_C2_whole_position_122b}}; L36 {{num|rts36_C2_whole_position_122b}}° | L13 {{num|rte_C2_whole_position_muse}}; L26 {{num|rt_C2_whole_position_muse}}; L34 not tested |
| Routes, added alone: position with the pointer part / with its random part; identity with the J++ part | {{num|rtk_C2_keep_alf_position_9b}} / {{num|rtk_C2_keep_alf_rand_position_9b}}; {{num|rtk_C2_keep_jpp_identity_9b}} | {{num|rtk_C2_keep_alf_position_27b}} / {{num|rtk_C2_keep_alf_rand_position_27b}}; {{num|rtk_C2_keep_jpp_identity_27b}} | {{num|rtk_C2_keep_alf_position_122b}} / {{num|rtk_C2_keep_alf_rand_position_122b}}; {{num|rtk_C2_keep_jpp_identity_122b}}° | {{num|rtk_C2_keep_alf_position_muse}} / {{num|rtk_C2_keep_alf_rand_position_muse}}; {{num|rtk_C2_keep_jpp_identity_muse}} |
| Sanity swap, switches lost: pointer + J++ minus pointer + random | {{num|rtc_lost_C0_jpp_minus_rand_lk_9b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_27b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_122b}}° | {{num|rtc_lost_C0_jpp_minus_rand_lk_muse}} |
| Sanity swap, lookup without both / pointer alone | {{num|rtb_ex_C0_both_lk_9b}} / {{num|rtb_ex_C0_alf_lk_9b}} | {{num|rtb_ex_C0_both_lk_27b}} / {{num|rtb_ex_C0_alf_lk_27b}} | {{num|rtb_ex_C0_both_lk_122b}} / {{num|rtb_ex_C0_alf_lk_122b}}° | {{num|rtb_ex_C0_both_lk_muse}} / {{num|rtb_ex_C0_alf_lk_muse}} |

*°: after the data, the gate lowered to 0.75.*

## Appendix B. Supplementary figures

Earlier figures, unchanged in [figures/status_2026-10-25/](figures/status_2026-10-25/) (shared links; the 24 Oct folder too):
[F1](figures/status_2026-10-25/f1_readers.png) the main test as bars ·
[F2](figures/status_2026-10-25/f2_depth.png) extra loss by depth ·
[F3](figures/status_2026-10-25/f3_dictionaries.png) logit lens, input embeddings, random directions ·
[F4](figures/status_2026-10-25/f4_order.png) lookups by sentence order ·
[F5](figures/status_2026-10-25/f5_atoms.png) more J++ directions ·
[F6](figures/status_2026-10-25/f6_digits.png) digit directions ·
[F7](figures/status_2026-10-25/f7_probe.png) probes ·
[F8](figures/status_2026-10-25/f8_address.png) the pointer outside J++ ·
[F9](figures/status_2026-10-25/f9_first_mention.png) first mention ·
[F10](figures/status_2026-10-25/f10_contrast.png) both swaps ·
[F11](figures/status_2026-10-25/f11_parts.png), [F12](figures/status_2026-10-25/f12_massmean.png) superseded ·
[F13](figures/status_2026-10-25/f13_x0b.png) varied scenes ·
[F14](figures/status_2026-10-25/f14_pcaeq.png) parts at equal share ·
[F15](figures/status_2026-10-25/f15_pointer.png) pointer directions ·
[F16](figures/status_2026-10-25/f16_x4.png) translated keys ·
[F17](figures/status_2026-10-25/f17_x0b_parts.png) varied-scene parts ·
[F18](figures/status_2026-10-25/f18_natural.png) natural passages ·
[F19](figures/status_2026-10-25/f19_replication.png) replication ·
[F20](figures/status_2026-10-25/f20_routes.png) routes, both swaps and all arms ·
[F21](figures/status_2026-10-25/f21_routes_early.png) routes, early layer ·
[F22](figures/status_2026-10-25/f22_jpp_other.png) J++ from another scene ·
[F23](figures/status_2026-10-25/f23_bothoff.png) both removed (superseded by Fig. 6).

## Appendix C. Prior work

The workspace paper (Gurnee et al. 2026); two-hop recall resolves its bridge early (Biran et al. 2024); mass-mean probing (Marks & Tegmark 2023); counterfactual routes (Gur-Arieh et al. 2025).
