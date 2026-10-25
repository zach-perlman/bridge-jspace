<!-- grid: results/cross_model/20261023T210238Z -->
# The lookup goes around the lens: what a model reads from the bridge word

*When a model answers a two-step question, does it use the part of the in-between entity that a lens can read, and does that depend on what it does with that entity next?*

## In one minute

- Recall needs the lens-readable (J++) part of the bridge; the lookup mostly doesn't (three Qwen models; rule fixed in advance), clearest in simple scenes.
- The lookup reads which item the bridge is and where it was first mentioned (a pointer the lens does not see), never the locker value. Adding only the pointer part moves the lookup to the other sentence on the 9B and the 122B; adding only the J++ part moves it on none.
- Early, the bridge carries only the item's identity, inside J++, which both readers need; later it adds a pointer outside J++ only the lookup uses (candidate; Section 3); on the 27B, removing both breaks the lookup beyond the pointer alone.

![Recall needs the J++ part; the lookup mostly doesn't](figures/story/fig1_readers.png)
*Fig. 1. Lookup against recall in each row; grey band: not needed.*

**Status.** Qwen3.5-9B, Qwen3.6-27B, Qwen3.5-122B-A10B; 25 Oct 2026. All numbers unverified until hand-checked (Section 5). Built at {{head}} from the run files.

## Setup

![One prompt, two questions about the same in-between word](figures/story/fig0_setup.png)

The **bridge** is the item Iris picked (*frog*). The **lookup** asks for its locker, written in the prompt; the **recall** asks for a fact from memory. We swap the bridge (frog → tick), take **the change** in the hidden state at the bridge word at one layer, and add it into the original prompt there: whole, without its **J++ part** (the 25 lens directions that best rebuild it), or without a random part of the same size. A reader switches when it gives the swapped bridge's answer. **Extra loss** = the share of switches lost without the J++ part minus the share lost without the random part. **Gap** = the recall's extra loss minus the lookup's. **Matched scenes**: the asked pick is not the bridge's first mention. Brackets: {{q|95%}} bootstrap intervals.

## 1. Recall needs the lens-readable part of the bridge; the lookup mostly doesn't

*Fixed in advance (main test); other settings: pass bars set before each run.*

- **Question.** Does removing the J++ part of the change cost the recall more than the lookup?
- **What we did.** One layer per model fixed in advance; 200 scenes (two people swap picks), then other scene sets and parts of the same size.
- **What we found.**
  - The gap is {{num|contrast_9b}} (9B), {{num|contrast_27b}} (27B) and {{num|contrast_122b}} (122B). The strict rule held on the 9B and the 122B; on the 27B the lookup lost {{num|lk_excess_27b}}, over its 0.10 bar.
  - It shrinks outside simple scenes: varied scenes {{num|x0b_c_9b}} (9B), {{num|x0b_c_27b}} (27B), {{num|x0b_c_122b}} (122B); natural passages {{num|nat_gap_27b}} (27B, whose lookup needs J++ there: {{num|nat_lk_excess_27b}}) and {{num|nat_gap_122b}} (122B).
  - Other parts of a similar size cost the recall less than J++ (Fig. 2). J++ fitted to another scene holds only {{num|jppother_jpp_other_share_27b}}-{{num|jppother_jpp_other_share_9b}} of the change and costs nothing, so it does not test this.

![No other part costs the recall as much as the scene's own J++](figures/story/fig2_parts.png)
*Fig. 2. †: two people swap picks; others: only the asked pick changes.*

- **Caveat.** On the 122B the main directions at J++'s share cost the recall almost as much as J++ ({{num|pcaeq_pca_eq_rc_excess_122b}} vs {{num|pcaeq_jpp_rc_excess_122b}}).

## 2. What the lookup reads instead: which item, and where it was first mentioned

*After the data; the routes test (2c) fixed in advance.*

- **Question.** What does the lookup take from the bridge word instead?
- **What we did.** (a) Split lookups by sentence order. (b) Probed the bridge word for which sentence holds the item's locker, and removed the 4 **pointer** directions that separate those answers. (c) Swapped prompts where identity, position and value predict different lockers (Fig. 3); parts removed or added alone.
- **What we found.**
  - (a) Lookups switch in {{num|lk_order_before_27b}}-{{num|lk_order_before_122b}} of locker-first scenes and {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} otherwise; lookup claims here are about locker-first scenes. On the 27B's natural passages the lookup switches mostly when the fact comes first ({{num|natsplit_before_lk_sw_27b}} of {{num|natsplit_before_n_27b}} vs {{num|natsplit_after_lk_sw_27b}} of {{num|natsplit_after_n_27b}}) and needs J++ where it does ({{num|natsplit_before_lk_27b}}): the route around the lens is weaker in natural text.
  - (b) The probe is right in {{num|v4_b_before_122b}}-{{num|v4_b_before_27b}} of scenes (layout alone: {{num|v4_b_layout_before_27b}}), almost none of it in J++. It points at the item's first mention, even another person's earlier pick, where the lookup still switches. Removing the pointer directions costs the lookup {{num|rep_alf_lk_excess_9b}} (9B, replicated) and {{num|mmlf_Alf_lk_excess_122b}} (122B), the recall less; the 27B {{num|mmlf_Alf_lk_excess_27b}}.
  - (c) When another item moved, the lookup follows its identity or its locker sentence's position, never the new value: 9B position {{num|rt_C2_whole_position_9b}}, identity {{num|rt_C2_whole_identity_9b}}; 27B identity {{num|rt_C2_whole_identity_27b}}, position {{num|rt_C2_whole_position_27b}}; 122B identity {{num|rtg_C2_whole_identity_122b}}, position {{num|rtg_C2_whole_position_122b}} (after the data); value {{num|rt_C2_whole_value_9b}}. Without the pointer directions position drops to {{num|rt_C2_no_alf_position_9b}}, {{num|rt_C2_no_alf_position_27b}} and {{num|rtg_C2_no_alf_position_122b}}. Added alone, the pointer part gives position answers on the 9B ({{num|rtk_C2_keep_alf_position_9b}}) and 122B ({{num|rtk_C2_keep_alf_position_122b}}; 27B {{num|rtk_C2_keep_alf_position_27b}}); the J++ part alone moves none.

![The routes test: each route predicts a different locker](figures/story/fig3_routes_design.png)
![The lookup follows identity or position, never the value](figures/story/fig4_routes.png)
*Fig. 3, Fig. 4. Compare blue (identity) and orange (position) across rows; no green (value) appears. Hatched: 122B, after the data, gate 0.75.*

- **Caveat.** Same item moved: a random part of the pointer's size also removed position (F20).

## 3. Why the readers split: with depth the bridge adds a pointer the lens can't see

*Candidate, after the data; 3a's layers and 3b's bar fixed in advance.*

- **Question.** Does the split come with depth?
- **What we did.** (a) The routes test at more layers (9B 6-12, 27B 16-32, 122B 24-36). (b) J++ and the pointer directions removed together in the sanity swap (only the pick changes). (c) Matched scenes against the rest.
- **What we found.**
  - (a) Early, the lookup follows identity only ({{num|rte_C2_whole_identity_9b}}, {{num|rte_C2_whole_identity_27b}}, {{num|rte_C2_whole_identity_122b}}); without J++ it gives the original answer ({{num|rte_C2_no_jpp_original_9b}}, {{num|rte_C2_no_jpp_original_27b}}, {{num|rte_C2_no_jpp_original_122b}}). Position appears by layer 12 (9B), 28 (27B) and 33 (122B); the rule fixed in advance (9B and 27B; the 122B's layers after the data) holds on the 9B only.
  - (b) Removing both costs the lookup {{num|rtb_ex_C0_both_minus_alf_lk_9b}} (9B) and {{num|rtb_ex_C0_both_minus_alf_lk_27b}} (27B) more than the pointer alone; the bar fixed in advance (0.15) is met on the 27B only. Against a random part of J++'s size: {{num|rtc_lost_C0_jpp_minus_rand_lk_27b}} (27B), {{num|rtc_lost_C0_jpp_minus_rand_lk_9b}} (9B); the bar is met on the 27B only. On the 9B a random part of J++'s size costs the lookup more than J++, so its second route is not in J++; in these scenes (the item already mentioned) the 9B's recall does not need J++ either ({{num|rtc_ex_C0_jpp_rc_9b}}), as table 3c predicts. The 27B is the case where the same scenes show the split and its mechanism.
  - (c) The recall needs J++ most where the pick is the bridge's first mention (table).

![Position answers appear with depth; on the 9B and 122B where the lookup stops needing J++](figures/story/fig5_depth.png)
![Removing J++ and the pointer directions together](figures/story/fig6_both_removed.png)
*Fig. 5: shaded where the lookup still needs J++ (at least 0.30). Fig. 6: dots against dotted bars; grey: recall.*

| Swap | Pick is the first mention? (no = matched) | 9B lookup | 9B recall | 27B lookup | 27B recall | 122B lookup | 122B recall |
|---|---|---|---|---|---|---|---|
| Two people swap picks | yes | {{num|comp_two_fmyes_lk_cell_9b}} | {{num|comp_two_fmyes_rc_9b}} | {{num|comp_two_fmyes_lk_cell_27b}} | {{num|comp_two_fmyes_rc_27b}} | {{num|comp_two_fmyes_lk_cell_122b}} | {{num|comp_two_fmyes_rc_122b}} |
| Two people swap picks | no | {{num|comp_two_fmno_lk_cell_9b}} | {{num|comp_two_fmno_rc_9b}} | {{num|comp_two_fmno_lk_cell_27b}} | {{num|comp_two_fmno_rc_27b}} | {{num|comp_two_fmno_lk_cell_122b}} | {{num|comp_two_fmno_rc_122b}} |
| Only the asked person's pick changes | yes | {{num|comp_one_fmyes_lk_cell_9b}} | {{num|comp_one_fmyes_rc_9b}} | {{num|comp_one_fmyes_lk_cell_27b}} | {{num|comp_one_fmyes_rc_27b}} | {{num|comp_one_fmyes_lk_cell_122b}} | {{num|comp_one_fmyes_rc_122b}} |
| Only the asked person's pick changes | no | {{num|comp_one_fmno_lk_cell_9b}} | {{num|comp_one_fmno_rc_9b}} | {{num|comp_one_fmno_lk_cell_27b}} | {{num|comp_one_fmno_rc_27b}} | {{num|comp_one_fmno_lk_cell_122b}} | {{num|comp_one_fmno_rc_122b}} |
| Same, fresh scenes | no | {{num|comp_rep_fmno_lk_cell_9b}} | {{num|comp_rep_fmno_rc_9b}} | {{num|comp_rep_fmno_lk_cell_27b}} | {{num|comp_rep_fmno_rc_27b}} | not tested (gate) | not tested (gate) |

*J++ extra loss, after the data; italics: under 30 lookup switches (count shown); n in Appendix A.*

- **Caveat.** On the 27B the lookup stops needing J++ at layer 24, four layers before position answers appear (28): there the pointer is not the whole reason. Removing both costs the recall too ({{num|rtb_ex_C0_both_rc_9b}}, {{num|rtb_ex_C0_both_rc_27b}}); the 122B's runs are after the data (both minus the pointer: {{num|rtb_ex_C0_both_minus_alf_lk_122b}}; J++ against random: {{num|rtc_lost_C0_jpp_minus_rand_lk_122b}}).

## 4. What did not hold, and limits

- The 27B's strict rule: lookup lost {{num|lk_excess_27b}} (bar 0.10).
- The 9B's fixed-in-advance replication: its J++ clause failed (recall {{num|rep_jpp_rc_excess_9b}}).
- The gap everywhere: the 122B's varied scenes ({{num|x0b_c_122b}}) and the 27B's natural passages ({{num|nat_gap_27b}}) are in between.
- On the 122B the layer's main directions at J++'s share cost the recall {{num|pcaeq_pca_eq_rc_excess_122b}}, near J++'s {{num|pcaeq_jpp_rc_excess_122b}}.
- The locker number at the bridge word: never the answer; digit directions cost {{num|dig_lk_jppdig_k10_before_27b}}. The positive control (chemical symbols) stayed below its 0.20 bar: 27B {{num|x4_D_elements_27b}}.
- Gates missed (bar 0.80), not tested: the 9B's natural passages (lookup {{num|nat_gate_lk_9b}}), the 122B's routes (recall {{num|rt_c0gate_rc_122b}}) and replication (recall {{num|rep_gate_rc_122b}}); their reruns at 0.75 are after the data, descriptive, none a confirmation. One model family; the 122B in FP8; natural passages: one-token bridges.

## 5. How we checked

- **Hand-checked numbers.** None yet; [docs/verify_pack.md](docs/verify_pack.md) recounts each section's numbers from per-item files, with commands.
- **Raw examples.** Ten natural passages ([docs/natural_examples.md](docs/natural_examples.md)) and routes cases (the pack).
- **Predictions.** Committed before results are opened, then scored: [predictions/](predictions/README.md).
- **"Fixed in advance"**: test, layer, sample and bar committed before any result; "after the data": chosen after seeing results.

## Appendix A. Key numbers

Every number on this page comes from [figures/story/data.csv](figures/story/data.csv) (also every plotted number) and [docs/x0_numbers.json](docs/x0_numbers.json), each with its source file; [docs/x0_details.md](docs/x0_details.md) has the full tables.

| Quantity | 9B | 27B | 122B |
|---|---|---|---|
| Gap, two people swap picks | {{num|contrast_9b}} | {{num|contrast_27b}} | {{num|contrast_122b}} |
| Gap, only the asked person's pick changes | {{num|single_contrast_9b}} | {{num|single_contrast_27b}} | {{num|single_contrast_122b}} |
| Gap, varied scenes | {{num|x0b_c_9b}} | {{num|x0b_c_27b}} | {{num|x0b_c_122b}} |
| Gap, natural passages | {{num|natg75_gap_9b}} (after the data, gate 0.75) | {{num|nat_gap_27b}} | {{num|nat_gap_122b}} |
| Lookup, translated locker key minus verbatim | {{num|x4_D_animals_9b}} | {{num|x4_D_animals_27b}} | {{num|x4_D_animals_122b}} |
| Recall, J++ / main directions at J++'s share | {{num|pcaeq_jpp_rc_excess_9b}} / {{num|pcaeq_pca_eq_rc_excess_9b}} | {{num|pcaeq_jpp_rc_excess_27b}} / {{num|pcaeq_pca_eq_rc_excess_27b}} | {{num|pcaeq_jpp_rc_excess_122b}} / {{num|pcaeq_pca_eq_rc_excess_122b}} |
| Lookup, pointer directions | {{num|mmlf_Alf_lk_excess_9b}} | {{num|mmlf_Alf_lk_excess_27b}} | {{num|mmlf_Alf_lk_excess_122b}} |
| n, table 3c rows (first mention yes / no): two people swap picks | {{num|comp_two_fmyes_n_9b}} / {{num|comp_two_fmno_n_9b}} | {{num|comp_two_fmyes_n_27b}} / {{num|comp_two_fmno_n_27b}} | {{num|comp_two_fmyes_n_122b}} / {{num|comp_two_fmno_n_122b}} |
| n, table 3c rows: only the asked person's pick changes; fresh scenes (no) | {{num|comp_one_fmyes_n_9b}} / {{num|comp_one_fmno_n_9b}}; {{num|comp_rep_fmno_n_9b}} | {{num|comp_one_fmyes_n_27b}} / {{num|comp_one_fmno_n_27b}}; {{num|comp_rep_fmno_n_27b}} | {{num|comp_one_fmyes_n_122b}} / {{num|comp_one_fmno_n_122b}}; not tested (gate) |
| Pointer probe right; another person's earlier pick read as first mention | {{num|v4_b_before_9b}}; {{num|dup_otherfirst_reads_other_9b}} | {{num|v4_b_before_27b}}; {{num|dup_otherfirst_reads_other_27b}} | {{num|v4_b_before_122b}}; {{num|dup_otherfirst_reads_other_122b}} |
| Routes, another item moved, position without the pointer / without a random part of its size | {{num|rt_C2_no_alf_position_9b}} / {{num|rt_C2_no_alf_rand_position_9b}} | {{num|rt_C2_no_alf_position_27b}} / {{num|rt_C2_no_alf_rand_position_27b}} | {{num|rtg_C2_no_alf_position_122b}} / {{num|rtg_C2_no_alf_rand_position_122b}} (after the data) |
| Early layer, recall still switching without J++ | {{num|rte_C2_no_jpp_recall_follows_s_9b}} | {{num|rte_C2_no_jpp_recall_follows_s_27b}} | {{num|rte_C2_no_jpp_recall_follows_s_122b}} (after the data) |
| Routes, position share at each tested layer (another item moved) | L6 {{num|rte_C2_whole_position_9b}}; L8 {{num|rts8_C2_whole_position_9b}}; L10 {{num|rts10_C2_whole_position_9b}}; L12 {{num|rt_C2_whole_position_9b}} | L16 {{num|rte_C2_whole_position_27b}}; L20 {{num|rts20_C2_whole_position_27b}}; L24 {{num|rts24_C2_whole_position_27b}}; L28 {{num|rts28_C2_whole_position_27b}}; L32 {{num|rt_C2_whole_position_27b}} | L24 {{num|rts24_C2_whole_position_122b}}; L27 {{num|rte_C2_whole_position_122b}}; L30 {{num|rts30_C2_whole_position_122b}}; L33 {{num|rtg_C2_whole_position_122b}}; L36 {{num|rts36_C2_whole_position_122b}} (after the data) |
| Routes, added alone: position with the pointer part / with its random part; identity with the J++ part | {{num|rtk_C2_keep_alf_position_9b}} / {{num|rtk_C2_keep_alf_rand_position_9b}}; {{num|rtk_C2_keep_jpp_identity_9b}} | {{num|rtk_C2_keep_alf_position_27b}} / {{num|rtk_C2_keep_alf_rand_position_27b}}; {{num|rtk_C2_keep_jpp_identity_27b}} | {{num|rtk_C2_keep_alf_position_122b}} / {{num|rtk_C2_keep_alf_rand_position_122b}}; {{num|rtk_C2_keep_jpp_identity_122b}} (after the data) |
| Sanity swap, switches lost: pointer + J++ minus pointer + random | {{num|rtc_lost_C0_jpp_minus_rand_lk_9b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_27b}} | {{num|rtc_lost_C0_jpp_minus_rand_lk_122b}} (after the data) |
| Sanity swap, lookup without both / pointer alone | {{num|rtb_ex_C0_both_lk_9b}} / {{num|rtb_ex_C0_alf_lk_9b}} | {{num|rtb_ex_C0_both_lk_27b}} / {{num|rtb_ex_C0_alf_lk_27b}} | {{num|rtb_ex_C0_both_lk_122b}} / {{num|rtb_ex_C0_alf_lk_122b}} (after the data) |

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

## Appendix C. Runs, specs, internal names

| Section | Run folders (results/) | Spec | Predictions |
|---|---|---|---|
| 1 | x0_necessity/{qwen35_9b_x0_necessity, x0_necessity_27b_chat, qwen35_122b_x0_necessity_r2, *_single_r2, qwen35_122b_x0_single}; x0b_generalize/*x0b_v2*; x5_natural/*; x0_parts/{*pcaeq*, *x0_parts*, *jppother*} | [X0.md](jobs/c3/X0.md), [X0b.md](jobs/c3/X0b.md), [x5_natural.yaml](jobs/c3/x5_natural.yaml), [x0_jppother.yaml](jobs/c3/x0_jppother.yaml) | batches 25-31, 33 |
| 2 | x0_probe/*v4*; x0_amnesic/*; x0_massmean/*; x0_replicate/*; x6_routes/{qwen35_9b_x6_routes, x6_routes_27b, qwen35_122b_x6_routes_g75} | [x0_massmean.yaml](jobs/c3/x0_massmean.yaml), [x0_replicate.yaml](jobs/c3/x0_replicate.yaml), [x6_routes_r2.yaml](jobs/c3/x6_routes_r2.yaml), [x6_routes_122b_g75.yaml](jobs/c3/x6_routes_122b_g75.yaml) | batches 27, 28, 31, 32 |
| 2, 3 | x6_routes/{*_l6, *_l16_*, *_l27_*, *sweep*, *bothoff*, *keeponly*}; x0_composition/* | [x6_routes_early_r2.yaml](jobs/c3/x6_routes_early_r2.yaml), [x6_routes_sweep.yaml](jobs/c3/x6_routes_sweep.yaml), [x6_routes_bothoff.yaml](jobs/c3/x6_routes_bothoff.yaml), [x6_routes_bothoff_ctrl.yaml](jobs/c3/x6_routes_bothoff_ctrl.yaml), [x6_routes_keeponly.yaml](jobs/c3/x6_routes_keeponly.yaml), [x0_122b_b8.yaml](jobs/c3/x0_122b_b8.yaml), [x0_122b_b9.yaml](jobs/c3/x0_122b_b9.yaml) | batches 32, 34-37 |

Internal names: X0 = the main test, X0b = varied scenes, X4 = the locker key in another language or as a symbol, X5 = natural passages, X6 = the routes test (C0 = the sanity swap, C1 = same item moved, C2 = another item moved), Alf = the pointer directions, PP / PM = lookup / recall, jwo = J++ without the word's directions. [README v1](docs/README_v1_2026-10-25.md) · [predictions 24 Oct](predictions/2026-10-24_dan.md), [25 Oct](predictions/2026-10-25_dan.md) · [earlier claims](CHANGELOG.md) · [Zach's breadth results](https://github.com/zach-perlman/bridge-jspace/tree/zach/v8-breadth-1021).

## Appendix D. Prior work

The workspace paper (Gurnee et al. 2026); two-hop recall resolves its bridge early (Biran et al. 2024); mass-mean probing (Marks & Tegmark 2023); counterfactual routes (Gur-Arieh et al. 2025).
