<!-- grid: results/cross_model/20261023T210238Z -->
# One word, two readers: what a model keeps at the bridge and what the lens sees

*A two-step question passes through one word, the bridge. The recall asks what the model knows about the item, the lookup where the prompt put it. What does each read from that word, and what can a lens see?*

## In one minute

- **In a conflict the recall follows the part of the bridge word the lens reads; the lookup does not** [A]. The recall does not need that part at one layer [B].
- **The lookup follows the item's identity or its locker's position, never the number** [A]; its identity route runs outside the lens on all three models [B].
- **The position is an address:** readable early, used late, removable, swappable, one code per slot, not verbalizable [A/B].
- **What did not hold:** four mechanism tests, a person mark at the locker sentence, blocking the pick sentence [✗].

**Status.** Qwen3.5-9B, Qwen3.6-27B, Muse Glimmer 30B (another family), and Qwen3.5-122B-A10B (FP8) on the first tests; 28 Oct 2026. Unverified until hand-checked. Built at {{head}} from the run files. Sealed and running: the gain map, one question two sources, the learned subspaces on the 27B and Muse; results land here when opened.

## Setup

![One prompt, two questions about the same bridge word](figures/story/fig00_setup.png)
*Fig. 0.*

![How to read the figures: colour is who, the mark is what was done](figures/story/fig00b_marks.png)

- **Lookup**: "Which locker belongs to Iris's pick?" (answer in the prompt). **Recall**: "How many legs does Iris's pick have?" (answer from memory).
- **Bridge**: the word at the pick ("frog"). **The change**: the bridge word's state from a changed prompt minus the original's, added at one layer; a reader **switches** to the changed prompt's answer.
- **The J++ part**: the 25 lens directions that best rebuild the change. **A random part**: random directions of the same share of the change.
- **Extra loss**: switches lost without a part minus those lost without its random part. **Gap**: the recall's extra loss minus the lookup's.
- **The address**: four directions at the bridge word that code where the item's locker sentence sits.

## Claims

| # | Claim | Models | Grade | Key numbers | Hand-checked |
|---|---|---|---|---|---|
| 1 | In a conflict between the J++ part and the rest of the change, the recall follows the J++ part and the lookup follows the rest | 9B, 27B, Muse (and the 122B) | **A** (27B partial) | recall {{pt|rc_excess_9b}} / {{pt|rc_excess_27b}} / {{pt|rc_excess_muse}}; lookup {{pt|lk_excess_9b}} / {{pt|lk_excess_27b}} / {{pt|lk_excess_muse}} | no |
| 2 | The lookup follows identity or position, never the number | 9B, 27B, Muse | **A** | 9B identity / position {{pt|rt_C2_whole_identity_9b}} / {{pt|rt_C2_whole_position_9b}}; value none anywhere | no |
| 3 | The bridge word redirects the lookup only when the locker sentence came first; otherwise the link is made at the locker sentences | 9B, 27B, Muse | **A** | locker first {{num|lk_order_before_muse}}-{{num|lk_order_before_122b}}, after {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}}; copy {{pt|x45q_c_9b}} / {{pt|x45q_c_27b}} / {{pt|x45q_c_muse}} | no |
| 4a | The address can be removed and swapped | 9B, 27B, Muse | **A** | without it {{pt|rt_C2_no_alf_position_9b}} / {{pt|rt_C2_no_alf_position_27b}} / {{pt|rt_C2_no_alf_position_muse}} vs random {{pt|rt_C2_no_alf_rand_position_9b}} / {{pt|rt_C2_no_alf_rand_position_27b}} / {{pt|rt_C2_no_alf_rand_position_muse}} | no |
| 4b | Adding only the address creates position answers | 9B, Muse (27B fails) | **B** | {{pt|rtk_C2_keep_alf_position_9b}} / {{pt|rtk_C2_keep_alf_position_27b}} / {{pt|rtk_C2_keep_alf_position_muse}} | no |
| 5 | The recall does not need the J++ part at one layer; it follows it | 9B, 27B, Muse | **B** | kept {{dp|fig01c|9b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|fig01c|27b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|fig01c|muse|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} | no |
| 6 | The lookup's identity route runs outside the lens on all three models; on the 27B the lens holds redundant copies of it (1–25: {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 1-25}}, 26–100: {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 26-100}}, both: {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 1-100}}). The position route never loses to any lens slice | 9B, 27B, Muse | **B** | identity route without 26–100: {{dp|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 26-100}}; position route at most {{dp|fig05d||47.1: position route: the most answers lost beyond random, over the models and slices}} | no |
| 7 | With depth: identity early, position in the last window that reads the word; the address readable 8-16 layers before it is used | 9B, Muse | **B** | address overlap across depth {{dp|fig06c|9b|D4: the address's mean overlap over every pair of window layers}} / {{dp|fig06c|muse|D4: the address's mean overlap over every pair of window layers}} | no |
| 8 | The recall also reads the item's earlier mention when there is one | 9B, 27B, Muse | **B** | {{pt|x45p_d23_9b}}-{{pt|x45p_d23_muse}} | no |
| 9a | The address is not verbalizable through the lens | 9B, 27B, Muse | **B** | share rebuilt {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: pointer}} | no |
| 10 | With six lockers each slot has its own code; the slot means lie in order; no single shift moves the lookup | 9B, Muse | **B** | | no |
| 11 | Lookups that do not switch at L read the bridge word before L (locker after the pick) or elsewhere | 9B, Muse | **B** | carried before L {{dp|e11_before_l|9b|47.4: main, locker after the pick: lookups carried by the bridge word before L}} / {{dp|e11_before_l|muse|47.4: main, locker after the pick: lookups carried by the bridge word before L}} | no |

*Grades: **A**, a rule fixed in advance held on at least three models with a specificity control and a variant design; **B**, on two models, or three with one operation, or descriptive on three with a random null.* Weaker and failed results are in Part IV; pending tests under Status.

## Part I. What each reader follows at the bridge word

*The recall follows the part the lens reads; the lookup follows the rest.*

![Both operations, both datasets, one direction](figures/story/fig12_two_by_two.png)

![The split carries over to other texts](figures/story/fig09a_transfer.png)

### E1. The conflict test: who follows which part <a id="e1-conflict"></a>

- **Hypothesis.** Without the J++ part the recall loses switches beyond random, the lookup does not (gap at least 0.3, lookup at most 0.10; fixed in advance).
- **Mechanics.** The bridge word's change at layer L: whole, without the J++ part, or without a random part of its share.
- **Data.** The main test (two people swap picks), 200 items per model.
- **Result.** Recall {{num|rc_excess_9b}} / {{num|rc_excess_27b}} / {{num|rc_excess_muse}}; lookup {{num|lk_excess_9b}} / {{num|lk_excess_27b}} / {{num|lk_excess_muse}} (9B / 27B / Muse). Held on all three by the gap; the 27B misses the strict lookup bar.
- **Figure.**

![Recall follows the J++ part of the bridge; the lookup mostly does not](figures/story/fig01_split.png)

- **Conclusion.** The readers weight [different parts](figures/story/fig05b_identity_outside.png) of one word. Not shown: that the recall needs the part (E2).

### E2. Followed, not needed at one layer <a id="e2-followed"></a>

- **Hypothesis.** Only the recall needs the J++ part, and only once its other copies go. Fixed in advance.
- **Mechanics.** The J++ part's directions taken out at the bridge word at L, then also over four layers, the earlier mention, the question and every token; against a random part.
- **Data.** Main test; clean scenes for the rungs.
- **Result.** At L the recall keeps {{dp|fig01c|9b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|fig01c|27b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|fig01c|muse|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}}. Also without the earlier mention it loses {{d|fig01d|9b|rung 3: recall, locker before the pick: answers lost beyond random}} (9B), {{d|fig01d|muse|rung 3: recall, locker before the pick: answers lost beyond random}} (Muse); the lookup nothing at any rung.
- **Figure.**

![Recall needs the J++ part once its other copies go; the lookup never](figures/story/fig01d_ladder.png)

- **Conclusion.** Followed at one layer, needed once other copies go. Not shown: Zach's band on Muse (rerun running).

### E3. The lookup's identity route runs outside the lens <a id="e3-identity"></a>

- **Hypothesis.** The lookup's answers by the identity route fall at least 0.30 beyond random without lens directions 26-100, or under 0.10 (outside the lens). Fixed in advance.
- **Mechanics.** Lens directions 1-25, 26-100 or both taken out of the change, against a random part.
- **Data.** Routes scenes, 300 items per model.
- **Result.** Identity route without 1-25 / 26-100 / both: {{dp|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 1-25}} / {{dp|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 1-100}} (9B), {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 1-25}} / {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 1-100}} (27B), {{dp|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 1-25}} / {{dp|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 1-100}} (Muse); position route at most {{dp|fig05d||47.1: position route: the most answers lost beyond random, over the models and slices}}.
- **Figure.**

![The lookup's identity route runs outside the lens; the position route never touches it](figures/story/fig05d_routes_lens.png)

- **Conclusion.** The identity route survives the loss of lens directions 26-100 on all three models and of 1-25 on the 9B and Muse; on the 27B the two slices are redundant copies. Not shown: the identity code itself.

## Part II. What the lookup reads

*The lookup reads which item it is and an address for where its locker sits, never the number.*

### E5. Identity, position, never the value <a id="e5-routes"></a>

- **Hypothesis.** The lookup follows the item's identity, its locker's position, or the number itself. Rule fixed in advance.
- **Mechanics.** The change comes from a prompt where another item's locker sentence moved and took a new number; each route predicts a different locker. Whole change, and without the address against a random part.
- **Data.** Routes scenes, 300 items per model.
- **Result.** Identity / position {{pt|rt_C2_whole_identity_9b}} / {{pt|rt_C2_whole_position_9b}} (9B), {{pt|rt_C2_whole_identity_27b}} / {{pt|rt_C2_whole_position_27b}} (27B), {{pt|rt_C2_whole_identity_muse}} / {{pt|rt_C2_whole_position_muse}} (Muse); the value never, in any format.
- **Figure.**

![The lookup takes the identity route or the position route, never the value](figures/story/fig05_routes.png)

- **Conclusion.** The lookup reads what the item is and where it sits. Not shown: who reads the position (the dereference test is running).

### E6. The address: probe, remove, add, swap <a id="e6-address"></a>

- **Hypothesis.** Removing the address stops position answers; adding it alone creates them; swapping it moves the lookup. Fixed in advance; probe post hoc.
- **Mechanics.** Removed or kept alone, against a random part; swapped (two slot means' difference) against a random vector of its size.
- **Data.** Routes scenes, 300 items per model.
- **Result.** A probe reads it in {{num|v4_b_before_122b}}-{{num|v4_b_before_27b}} of scenes. Without it position answers drop to {{pt|rt_C2_no_alf_position_9b}} / {{pt|rt_C2_no_alf_position_27b}} / {{pt|rt_C2_no_alf_position_muse}} (random {{pt|rt_C2_no_alf_rand_position_9b}} / {{pt|rt_C2_no_alf_rand_position_27b}} / {{pt|rt_C2_no_alf_rand_position_muse}}); alone it gives {{pt|rtk_C2_keep_alf_position_9b}} / {{pt|rtk_C2_keep_alf_position_27b}} / {{pt|rtk_C2_keep_alf_position_muse}}; a swap at a real change's size moves {{dp|fig07|9b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|27b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|muse|lookup target share, mean over locker pairs, s = 2}} of lookups, {{dp|e6_distance|9b|47.16: the swap (fit with none) sends lookups to the target, 50 sentences}} after 50 neutral sentences (9B).
- **Figure.**

![The address carries the position route; swapping it moves the lookup](figures/story/fig07_writes.png)

- **Conclusion.** The address is causal and survives distance. Not shown: who reads it.

### E7. Six lockers: one code per slot <a id="e7-code"></a>

- **Hypothesis.** The address is a line over slots (one shift steps the lookup one slot), first-vs-rest, or one code per slot. Fixed in advance.
- **Mechanics.** Six-locker scenes: one shift per start slot and swaps between given slots, against a random direction.
- **Data.** 300 items each, 9B and Muse.
- **Result.** One code per slot on both: slot means lie in order, no single shift reaches the bar, given-slot swaps reach it on {{dp|fig09b|9b|47.2: pairwise writes reaching 25% (dose 2)}} and {{dp|fig09b|muse|47.2: pairwise writes reaching 25% (dose 2)}} of 30 pairs.
- **Figure.**

![Six lockers: each locker has its own code, no single shift](figures/story/fig09b_six_lockers.png)

- **Conclusion.** Order is readable; each slot is its own target. Not shown: whether the code is shared across item kinds (Part IV).

### E8. The lens is blind to the address <a id="e8-blind"></a>

- **Hypothesis.** Through the J++ lens an address swap looks like a random draw. Descriptive.
- **Mechanics.** The swap against 200 random draws: the right ordinal's rank and the share the lens rebuilds; an identity change as control.
- **Data.** 200 cases per model.
- **Result.** The lens rebuilds {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: pointer}} of the swap, as for random draws. Asked for the position, the 27B's lens top five hold the right ordinal in {{dp|e8_report|27b|47.10: lens top-5 holds the right ordinal (report prompt)}} of reports, yet it loses {{dp|e8_report|27b|47.10: the report's extra loss without the address}} without the address.
- **Figure.**

![The lens is blind to the address](figures/story/fig07b_verbal.png)

- **Conclusion.** A lens monitor sees which item is at the bridge, not where the model will look. Not shown: a probe-based monitor.

## Part III. Where and when

*The link to the locker is made where the order puts it, and the bridge word is read up to a depth where position takes over.*

### E10. Sentence order: where the link is made <a id="e10-order"></a>

- **Hypothesis.** Locker after the pick: copying the changed prompt's locker-sentence states at L carries at least half the switches. Link rule fixed in advance, order split post hoc.
- **Mechanics.** Main test split by order; clean scenes; copies into the locker sentences per layer.
- **Data.** 200 items per model.
- **Result.** Lookups switch in {{num|lk_order_before_muse}}-{{num|lk_order_before_122b}} of locker-first scenes, {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} otherwise; the copy carries {{pt|x45q_c_9b}} / {{pt|x45q_c_27b}} / {{pt|x45q_c_muse}}.
- **Result.** Locker first, the recall also reads the earlier mention: the J++ part removed there costs {{pt|x45p_d23_9b}}-{{pt|x45p_d23_muse}} more switches than random.
- **Figure.**

![Locker after the pick: the link is made in the locker sentences](figures/story/fig03_order.png)

- **Conclusion.** The bridge word links only when the locker came first. Not shown: what the locker sentence holds.

### E11. Token by token, layer by layer <a id="e11-map"></a>

- **Hypothesis.** Locker after the pick: one locker-sentence cell carries the lookup, which stops reading the bridge word before the recall. Fixed in advance.
- **Mechanics.** The changed prompt's state placed into one token group at one layer, every other layer.
- **Data.** Clean scenes, 9B and Muse.
- **Result.** Both fail: no single cell carries the locker-after lookup, which reads the bridge word early; both readers read it to about the same depth, then the question and last token carry the answer.
- **Figure.**

![Locker after the pick: the lookup leaves the bridge word early](figures/story/fig03d_depth_map.png)

- **Conclusion.** The link is spread over tokens and layers. Not shown: the 27B.

### E12. The anatomy by depth <a id="e12-anatomy"></a>

- **Hypothesis.** The lookup drops the J++ part by the time it takes up the address, which is readable earlier; never the value. Fixed in advance.
- **Mechanics.** The change's parts per sampled layer against random parts, and a slot probe.
- **Data.** Routes scenes split in halves; 9B, Muse.
- **Result.** Identity early, position in the last window, never the value; the probe reads the address 8 (9B) / 16 (Muse) layers before position starts; it settles late (mean overlap {{dp|fig06c|9b|D4: the address's mean overlap over every pair of window layers}} / {{dp|fig06c|muse|D4: the address's mean overlap over every pair of window layers}}).
- **Figure.**

![The address forms early; identity route first, position route later](figures/story/fig06b_anatomy.png)

- **Conclusion.** The address: written early, read late; position grows with depth on the main test too (candidate). Not shown: the 27B.

## Part IV. Weaker results and what did not hold

*Harder prompts keep the split in part, and every mechanism we proposed for why failed.*

**Weaker results.**

- **A described bridge** ("the one known for honey"; rule fixed in advance): the split holds on the 9B and Muse (gap {{dp|fig05c|9b|47.3: gap (recall's extra loss minus the lookup's)}} / {{dp|fig05c|muse|47.3: gap (recall's extra loss minus the lookup's)}}); on the 27B the lookup follows the lens too ({{dp|fig05c|27b|47.3: lookup's extra loss without the J++ part}}). Few bridge items ([figure](figures/story/fig05c_described_bridge.png)).

- **One question under two instructions** ("from the passage" / "from what you know"; 27B only, the others miss the gate): both instructions lose most switches without the J++ part and many without the address and the outside identity. With no instruction the 27B answers from the passage.
- **The address must be refit per text format:** fit on simple scenes it costs the lookup {{num|tptr_varied_range}} in varied scenes; refit it reaches {{pt|x45d_table_9b}}-{{pt|x45d_prose_9b}} (9B) and {{pt|x45d_prose_muse}}-{{pt|x45d_table_muse}} (Muse), at most {{pt|x45d_table_27b}} on the 27B ([figure](figures/story/fig09b_refit.png)).

- **The lookup's errors are not address errors** (9B): the probe matches the wrong answer's slot in {{dp|fig07c|9b|47.13: wrong answers whose locker the address probe predicts}} of them.

**What did not hold** (each rule fixed in advance; [the five mechanism tests on one page](figures/story/fig15_mechanisms.png)):

- The J++ part keys the item's attribute at the bridge word; late MLPs there carry the recall → without the J++ part the attribute still moves part way; the MLPs are not needed.
- A person mark at the locker sentence → a probe reads chance there; a person direction moves nothing (the pooled probe is running).
- The copying heads pass the rest at twice the J++ part → about equal.
- The address is the recall's second route → few recalls name the swapped slot's item.
- Blocking the pick sentence from the lockers removes position answers only → identity answers and recall switches fall too.
- The second hop's key token (the locker number) carries the hall question's address → removing it costs no more than a random part of its large share.
- The address is the same for any kind of item (within 0.10 of the animal result) → on the 9B it moves fruits and names more than animals; on Muse names fall short.
- Token by layer: one locker-sentence cell carries the locker-after lookup; the lookup leaves the bridge word before the recall → neither.
- Also failed: the positive control, a second-vs-third address, the 9B in the clean design and its replication, the 27B's strict bar.

## How we checked

- **Hand-checked numbers:** none yet; [the verify pack](docs/verify_pack.md) recounts each claim from the per-item files.
- **Independent reimplementation:** code written from scratch reproduces the 9B's main test on {{num|indep_agree_9b}} random items, every arm.
- **Predictions:** committed before results are opened, then scored ([predictions](predictions/README.md)): mean Brier {{num|pred_brier}} over {{num|pred_n}} answers, worse than always answering {{q|50%}}.
- **Limits:** one-token answers and bridges; reader and answer source confounded; the 122B in FP8.

## Related work and what is new

Models bind entities to attributes in context (Feng & Steinhardt 2023) and track them through lookback pointers (Prakash et al. 2025) in a low-dimensional order subspace (Dai et al. 2024). The routes test follows Gur-Arieh et al. (2025); the address uses mass-mean directions (Marks & Tegmark 2023); random parts answer Makelov et al. (2023). The lens is the workspace paper's J++ (Gurnee et al. 2026). New here: two readers of one word follow different parts of it; the address is the part the lens misses, and swapping it redirects the lookup.

## Open questions

- **Why does the 27B's lookup need J++ only when all 100 directions go together?**
- **Why does the recall follow J++ without needing it at one layer?** Removing it over four layers costs the 9B's recall about a quarter.
- **Does the address exist in natural text?** Refit per format, it is found on the 9B and Muse, not the 27B.

## Appendix A. Links

Every number on this page carries a source comment into figures/story/data.csv or docs/x0_numbers.json; where things live: run files under results/, job specs under jobs/c3/, scripts under scripts/. All figures on one page: [the contact sheet](docs/figures_contact_sheet.png). Supplementary figures: [every scene set](figures/supp/s01_split_all_scene_sets.png), [the settings](figures/story/fig01b_settings.png), [every part](figures/supp/s02_parts_all.png), [parts of the same size](figures/story/fig02_specificity.png), [the 27B with more directions](figures/story/fig02b_k_curve.png), [the J++ part taken out at one layer](figures/story/fig01c_zeroing.png), [a described bridge](figures/story/fig05c_described_bridge.png), [the order split with every model](figures/supp/s03_order_split.png), [the layer sweep](figures/story/fig03b_layers.png), [the link copy variants](figures/supp/s03d_link_copy_variants.png), [the lookups the change misses](figures/supp/s03e_cumulative.png), [the depth candidate on the main test](figures/story/fig06_depth.png), [the address across depth](figures/story/fig06c_address_depth.png), [the recall follows the swap](figures/supp/s07_recall_follows_swap.png), [the lens readout of the swap](figures/supp/s07b_lens_readout.png), [the lookup's errors](figures/story/fig07c_probe_errors.png), [the first locker](figures/story/fig08_first_locker.png), [the first sentence and the moves](figures/supp/s08b_pointer_moves_and_neutral_sentence.png), [every routes arm](figures/supp/s05_routes_all_arms.png), [the blocked pick sentence](figures/story/fig09c_formation.png), [chained addresses](figures/story/fig09d_chain.png), [what is left of the route](figures/story/fig10_what_is_left.png), [attribute probe and MLPs](figures/story/fig10b_enrichment.png), [binding](figures/story/fig10c_binding.png), [heads](figures/story/fig10d_heads.png), [second route](figures/story/fig10e_second_route.png), [the mechanism tests](figures/story/fig15_mechanisms.png), [attention follows the swapped address](figures/story/fig13_attention.png), [learned subspaces](figures/story/fig14_learned.png), [Muse's learned subspaces](figures/supp/s12_das_muse.png), [the transfer on every model](figures/story/fig09_transfer.png). Earlier figures: [figures/status_2026-10-25/](figures/status_2026-10-25/).
