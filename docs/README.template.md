<!-- grid: results/cross_model/20261023T210238Z -->
# One word, two readers: what a model keeps at the bridge and what the lens sees

*A two-step question passes through one word, the bridge. The recall asks what the model knows about the item, the lookup where the prompt put it. What does each read from that word, and what can a lens see?*

## In one minute

- **In a conflict the recall follows the part of the bridge word the lens reads; the lookup does not** [A]. The recall does not need that part at one layer [B].
- **The lookup follows the item's identity or its locker's position, never the number** [A]; its identity code lies outside the lens on all three models [B].
- **The position is an address:** readable early, used late, removable, swappable, one code per slot, not verbalizable [A/B].
- **What did not hold:** four mechanism tests, a person mark at the locker sentence, blocking the pick sentence [✗].

**Status.** Qwen3.5-9B, Qwen3.6-27B, Muse Glimmer 30B (another family), Qwen3.5-122B-A10B (FP8) on the first tests; 28 Oct 2026. Unverified until hand-checked. Built at {{head}} from the run files.

## Setup

![One prompt, two questions about the same bridge word](figures/story/fig00_setup.png)
*Fig. 0.*

- **Lookup**: "Which locker belongs to Iris's pick?" (answer in the prompt). **Recall**: "How many legs does Iris's pick have?" (answer from memory).
- **Bridge**: the word at the pick ("frog"). **The change**: the bridge word's state from a changed prompt minus the original's, added at one layer; a reader **switches** to the changed prompt's answer.
- **The J++ part**: the 25 lens directions that best rebuild the change. **A random part**: random directions of the same share of the change.
- **Extra loss**: switches lost without a part minus those lost without its random part. **Gap**: the recall's extra loss minus the lookup's.
- **The address**: four directions at the bridge word that code where the item's locker sentence sits.

## Claims

| # | Claim | Cards | Models | Fixed in advance | Variants | Controls | Hand-checked | Grade | Key numbers |
|---|---|---|---|---|---|---|---|---|---|
| 1 | In a conflict between the J++ part and the rest of the change, the recall follows the J++ part and the lookup follows the rest | [E1](#e1-conflict), [E3](#e3-identity) | 9B, 27B, 122B, Muse | yes | clean design (2 of 3), logit difference, probability, six scene sets | random part, PCA, logit-lens | no | **A** (27B partial; 122B not specific vs PCA) | recall {{pt|rc_excess_9b}} / {{pt|rc_excess_27b}} / {{pt|rc_excess_muse}}; lookup {{pt|lk_excess_9b}} / {{pt|lk_excess_27b}} / {{pt|lk_excess_muse}} |
| 2 | The lookup follows identity or position, never the number | [E5](#e5-routes), [E12](#e12-anatomy) | 4 | yes | formats; described bridge; every depth; question first (27B) | random part | no | **A** | 9B identity / position {{pt|rt_C2_whole_identity_9b}} / {{pt|rt_C2_whole_position_9b}}; value none anywhere |
| 3 | The bridge word redirects the lookup only when the locker sentence came first; otherwise the link is made at the locker sentences | [E10](#e10-order) | 4 | order split after the data (4 models); the link test fixed in advance (3 of 3) | token x layer map | random part | no | **A** | locker first {{num|lk_order_before_muse}}-{{num|lk_order_before_122b}}, after {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}}; copy {{pt|x45q_c_9b}} / {{pt|x45q_c_27b}} / {{pt|x45q_c_muse}} |
| 4a | The address can be removed and swapped | [E6](#e6-address) | 9B, 27B, Muse | yes | six lockers; distance (9B); chains (negative) | random part, random vector | no | **A** | without the address {{pt|rt_C2_no_alf_position_9b}} / {{pt|rt_C2_no_alf_position_27b}} / {{pt|rt_C2_no_alf_position_muse}} vs random {{pt|rt_C2_no_alf_rand_position_9b}} / {{pt|rt_C2_no_alf_rand_position_27b}} / {{pt|rt_C2_no_alf_rand_position_muse}}; swap {{dp|fig07|9b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|27b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|muse|lookup target share, mean over locker pairs, s = 2}} |
| 4b | Adding only the address creates position answers | [E6](#e6-address) | 9B, Muse (27B fails) | yes | none | random part | no | **B** | {{pt|rtk_C2_keep_alf_position_9b}} / {{pt|rtk_C2_keep_alf_position_27b}} / {{pt|rtk_C2_keep_alf_position_muse}} |
| 5 | The recall does not need the J++ part at one layer; it follows it | [E2](#e2-followed) | 3 | yes | none (one operation) | random part | no | **B** | kept {{dp|fig01c|9b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|fig01c|27b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|fig01c|muse|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} |
| 6 | The lookup's identity code lies outside the lens; on the 27B the lens copies are redundant | [E3](#e3-identity) | 3 | yes | none | random part, random lens directions | no | **B** | directions 26-100: {{dp|e3_identity|9b|47.1: identity answers lost beyond random without lens directions 26-100}} / {{dp|e3_identity|27b|47.1: identity answers lost beyond random without lens directions 26-100}} / {{dp|e3_identity|muse|47.1: identity answers lost beyond random without lens directions 26-100}} |
| 7 | With depth: identity early, position in the last window that reads the word; the address is readable 8-16 layers before it is used; re-encoded early, one code from the layer the probe reaches 0.8 | [E12](#e12-anatomy) | 9B, Muse | yes | none | random part | no | **B** | mean overlap {{dp|fig06c|9b|D4: the address's mean overlap over every pair of window layers}} / {{dp|fig06c|muse|D4: the address's mean overlap over every pair of window layers}} |
| 8 | The recall also reads the item's earlier mention when there is one | [E10](#e10-order) | 3 | yes | none | random part, another item | no | **B** | {{pt|x45p_d23_9b}}-{{pt|x45p_d23_muse}} |
| 9a | The address is not verbalizable through the lens | [E8](#e8-blind) | 3 | descriptive | none | random null | no | **B** | share rebuilt {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: pointer}} |
| 9b | The address does not surface in the lens when the model must report the position | [E8](#e8-blind) | 27B (9B, Muse cannot report positions: gate) | yes | none | random part | no | **C** | report without the address {{d|e8_report|27b|47.10: the report's extra loss without the address}}; lens top-5 {{dp|e8_report|27b|47.10: lens top-5 holds the right ordinal (report prompt)}} |
| 10 | With six lockers each slot has its own code; the slot means lie in order; no single shift moves the lookup | [E7](#e7-code) | 9B, Muse | yes | none | random direction | no | **B** | |
| 11 | Lookups that do not switch at L read the bridge word before L (locker after the pick) or elsewhere | [E11](#e11-map) | 9B, Muse | descriptive | token x layer map | none | no | **B** | |
| 12 | A described bridge: the split holds on the 9B and Muse; on the 27B the lookup follows the lens | [E13](#e13-described) | 3 | yes | none | random part | no | **C** | gap {{dp|fig05c|9b|47.3: gap (recall's extra loss minus the lookup's)}} / {{dp|fig05c|muse|47.3: gap (recall's extra loss minus the lookup's)}}; 27B lookup {{dp|fig05c|27b|47.3: lookup's extra loss without the J++ part}} |
| 13 | The address must be refit per text format; the split carries, the address barely | [E14](#e14-texts) | 9B, 27B, Muse | refit fixed in advance | formats | random part | no | **C** | fit on simple scenes {{num|tptr_varied_range}} (varied), {{num|tptr_natural_range}} (natural); refit {{pt|x45d_table_9b}}-{{pt|x45d_prose_9b}} (9B), {{pt|x45d_prose_muse}}-{{pt|x45d_table_muse}} (Muse), at most {{pt|x45d_table_27b}} (27B) |
| 14 | The lookup's errors are not address errors | [E8](#e8-blind) | 9B | yes | none | chance, most common locker | no | **C** | {{dp|fig07c|9b|47.13: wrong answers whose locker the address probe predicts}} vs chance {{dp|fig07c|9b|47.13: chance (1 / lockers)}} |
| 15 | Identity outside J++ is only partly specific against a wrong pair | [E3](#e3-identity) | 9B, 27B, Muse | yes | none | wrong pair | no | **C** | {{pt|x45em_cut_9b}} / {{pt|x45em_cut_27b}} / {{pt|x45em_cut_muse}} |
| ✗ | J++ keys the attribute at the bridge word; late MLPs there carry the recall | [E15](#e15-failed) | 9B, Muse | yes | | random part, two controls | no | ✗ | |
| ✗ | A person mark is written at the locker sentence (item or number token) | [E15](#e15-failed) | 9B, Muse | yes | pooled probe pending | random direction | no | ✗ | |
| ✗ | The copying heads pass the rest at twice the J++ part | [E15](#e15-failed) | 9B, Muse | yes | | random part | no | ✗ | |
| ✗ | The address is the recall's second route | [E15](#e15-failed) | 3 | yes | | random vector | no | ✗ | |
| ✗ | Blocking the pick sentence from the lockers removes position answers only | [E15](#e15-failed) | 9B, Muse | yes | | neutral edges | no | ✗ (removes the address, with collateral) | |
| ✗ | The second hop's key token (the locker digit) carries an address the hall question needs | [E15](#e15-failed) | 9B, Muse | yes | | random part | no | ✗ | hall probe there {{dp|fig09d|9b|47.14: hall probe at the locker digit}} / {{dp|fig09d|muse|47.14: hall probe at the locker digit}} |
| ✗ | Token x layer rules: (a) one locker-sentence cell carries the locker-after lookup; (b) the lookup stops reading the bridge word before the recall | [E11](#e11-map) | 9B, Muse | yes | | | no | ✗ (and the evidence for row 11) | |
| ✗ | Positive control (recalled key into a lookup); second-vs-third address; the 9B in the clean design and its replication; the 27B's strict bar | [E1](#e1-conflict), [E6](#e6-address) | | yes | | | no | ✗ | 27B control {{pt|x4_D_elements_27b}}, bar 0.20 |
| … | Weights, not routes (49.1); who dereferences the address (49.7); one question, two sources (47.15); the identity code by learned subspaces (48.1); the removal ladder (49.2); the pooled probe (49.3); the 27B's anatomy (49.4); clean reruns (49.5); the address by learned subspaces (49.8) | [E4](#e4-gain), [E9](#e9-dereference), [E16](#e16-sources) | | yes | | | | … | |

*Grades: **A**, a rule fixed in advance held on at least three gated models with a specificity control and at least one variant design or scoring; **B**, held on two models, or on three with one operation, or descriptive on three with a random null; **C**, one model, after the data, or held in part; **✗**, fixed in advance and failed; **…**, sealed or queued.*

## Part I. What each reader follows at the bridge word

*The recall follows the part the lens reads; the lookup follows the rest.*

### E1. The conflict test: who follows which part <a id="e1-conflict"></a>

**Hypothesis.** Without the J++ part the recall loses switches beyond random and the lookup does not (bar: gap at least 0.3, lookup at most 0.10).
**Mechanics.** The change at the bridge word at L: whole, without the J++ part, without a random part.
**Data.** The main test (two people swap picks), 200 items per model.
**Result.** Recall {{num|rc_excess_9b}} / {{num|rc_excess_27b}} / {{num|rc_excess_muse}}; lookup {{num|lk_excess_9b}} / {{num|lk_excess_27b}} / {{num|lk_excess_muse}} (9B / 27B / Muse); the 27B misses the strict lookup bar.
**Figure.**

![Recall follows the J++ part of the bridge; the lookup mostly does not](figures/story/fig01_split.png)

**Conclusion.** The readers weight different parts of one word. Not shown: need (E2).

<sub>Fixed in advance · hand-checked: no · results/x0_necessity/</sub>

### E2. Followed, not needed at one layer <a id="e2-followed"></a>

**Hypothesis.** The recall needs the J++ part at L (removing it costs at least 0.30 beyond random) or only follows it (keeps at least 0.80).
**Mechanics.** On the changed prompt, the J++ part's 25 directions taken out of the bridge word's state at L; a random part beside.
**Data.** The main test, 200 items per model.
**Result.** The recall keeps {{d|fig01c|9b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{d|fig01c|27b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{d|fig01c|muse|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}}: followed on all three.
**Figure.**

![The J++ part zeroed at one layer: the recall keeps its answers](figures/story/fig01c_zeroing.png)

**Conclusion.** The recall follows the part but has other copies. Not shown: where (the removal ladder, pending).

<sub>Fixed in advance · hand-checked: no · results/x47_zero/</sub>

### E3. Where the lookup's identity lives <a id="e3-identity"></a>

**Hypothesis.** The lookup's identity sits in lens directions 26-100 (identity falls at least 0.30 beyond random without them) or outside the lens (under 0.10).
**Mechanics.** Routes scenes; lens directions 26-100 taken out, 1-25 kept; random parts beside.
**Data.** 300 items per model.
**Result.** Identity falls {{d|e3_identity|9b|47.1: identity answers lost beyond random without lens directions 26-100}} / {{d|e3_identity|27b|47.1: identity answers lost beyond random without lens directions 26-100}} / {{d|e3_identity|muse|47.1: identity answers lost beyond random without lens directions 26-100}}: outside the lens on all three. On the 27B, directions 1-25 cost {{dp|e3_identity|27b|47.1: identity answers lost beyond random without lens directions 1-25}}, both slices together {{dp|e3_identity|27b|47.1: identity answers lost beyond random without lens directions 1-100}}: redundant copies.
**Figure.**

![The lookup's identity route lies outside the lens, not in directions 26-100](figures/story/fig05b_identity_outside.png)

**Conclusion.** Adding only the J++ part gives no identity answers, so even the identity route runs mostly outside J++. Not shown: the identity code itself (pending).

<sub>Fixed in advance · hand-checked: no · results/x47_atoms/</sub>

### E4. Weights, not routes (pending) <a id="e4-gain"></a>

**Hypothesis.** Each reader's switch depends on the gain of its own part: the change written as α (its J++ part) + β (the rest), α, β from 0 to 2.
**Mechanics.** 25 gain cells at L, both readers; random corners; the address removed from the rest at (0, 2).
**Data.** The main test's locker-first items; three models.
**Result.** Sealed; Dan's prediction committed.
**Figure.** None yet.
**Conclusion.** Pending.

<sub>Fixed in advance · jobs/c3/batch49.yaml</sub>

## Part II. What the lookup reads

*The lookup reads which item it is and an address for where its locker sits, never the number.*

### E5. Routes: identity, position, never the value <a id="e5-routes"></a>

**Hypothesis.** The lookup follows the change's identity, its position, or its value (the number itself).
**Mechanics.** The change comes from a prompt where another item's locker sentence moved and took a new number; each route predicts a different locker. Arms: whole, without the address, random beside.
**Data.** 300 items per model; four models (the 122B's gate lowered to 0.75 after the data).
**Result.** Identity / position {{pt|rt_C2_whole_identity_9b}} / {{pt|rt_C2_whole_position_9b}} (9B), {{pt|rt_C2_whole_identity_27b}} / {{pt|rt_C2_whole_position_27b}} (27B), {{pt|rt_C2_whole_identity_muse}} / {{pt|rt_C2_whole_position_muse}} (Muse); the value never.
**Figure.**

![The lookup follows identity or position, never the value](figures/story/fig05_routes.png)

**Conclusion.** The lookup reads what the item is and where it sits. Not shown: who reads the position (E9).

<sub>Fixed in advance · hand-checked: no · results/x6_routes/</sub>

### E6. The address: probe, remove, add, swap <a id="e6-address"></a>

**Hypothesis.** Removing the address stops position answers, adding it alone creates them, swapping it sends the lookup to the target locker.
**Mechanics.** Removed or kept against a random part; swapped as the difference of two slot means, against a random vector.
**Data.** Routes scenes, 300 items per model.
**Result.** A probe reads the address in {{num|v4_b_before_122b}}-{{num|v4_b_before_27b}} of scenes (layout alone {{num|v4_b_layout_before_27b}}). Without it position answers drop to {{pt|rt_C2_no_alf_position_9b}} / {{pt|rt_C2_no_alf_position_27b}} / {{pt|rt_C2_no_alf_position_muse}} (random {{pt|rt_C2_no_alf_rand_position_9b}} / {{pt|rt_C2_no_alf_rand_position_27b}} / {{pt|rt_C2_no_alf_rand_position_muse}}); alone it gives {{pt|rtk_C2_keep_alf_position_9b}} / {{pt|rtk_C2_keep_alf_position_27b}} / {{pt|rtk_C2_keep_alf_position_muse}}; the swap, at about a real change's size, sends {{dp|fig07|9b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|27b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|muse|lookup target share, mean over locker pairs, s = 2}} of lookups to the target. After 50 neutral sentences (9B) position answers stay {{dp|e6_distance|9b|47.16: position share with 50 neutral sentences}} and the swap still sends {{dp|e6_distance|9b|47.16: the swap (fit with none) sends lookups to the target, 50 sentences}}, though the code shifts {{dp|e6_distance|9b|47.16: the code's shift beta with 50 sentences}} positions.
**Figure.**

![One fixed vector written at the bridge sends the lookup to its locker](figures/story/fig07_writes.png)

**Conclusion.** The address is causal and survives distance. Not shown: who reads it (E9).

<sub>Removal after the data, replicated in advance; swaps fixed in advance · hand-checked: no · results/x6_routes/, results/x8_write/, results/x47_distance/</sub>

### E7. What kind of code: six lockers <a id="e7-code"></a>

**Hypothesis.** The address is a line over slots (one shift moves the lookup one slot on), first-vs-rest, or one code per slot.
**Mechanics.** Six lockers; one shift vector from each start slot; pairwise swaps; a random direction beside.
**Data.** 300 items per model; 9B and Muse.
**Result.** One code per slot on both: the slot means lie in order, no single shift reaches the bar, pairwise swaps do.
**Figure.**

![Six lockers: each locker has its own code, no single shift](figures/story/fig09b_six_lockers.png)

**Conclusion.** Order is readable; each slot is its own target. Not shown: other item kinds (pending).

<sub>Fixed in advance · hand-checked: no · results/x47_six/</sub>

### E8. The lens is blind to the address <a id="e8-blind"></a>

**Hypothesis.** Through the lens an address swap looks random; when the model must report the position, the lens still does not show it.
**Mechanics.** The swap against 200 random draws: ordinal ranks, the share the lens rebuilds, the readout's change; the report question "first, second or third?".
**Data.** 200 cases per model; the report on the 27B (gate).
**Result.** The lens rebuilds {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: pointer}} of the swap, as of random draws. The 27B's report loses {{d|e8_report|27b|47.10: the report's extra loss without the address}} without the address, and the lens never ranks the ordinal in its top five. The lookup's errors are not address errors (9B: {{dp|fig07c|9b|47.13: wrong answers whose locker the address probe predicts}}).
**Figure.**

![Read through the J++ lens, the pointer looks like a random direction](figures/story/fig07b_verbal.png)

**Conclusion.** A lens monitor sees which item is at the bridge, not where the model will look.

<sub>Descriptive and fixed in advance · hand-checked: no · results/x47_verbal/, results/x47_report/, results/x47_errors/</sub>

### E9. Who dereferences the address (pending) <a id="e9-dereference"></a>

**Hypothesis.** A swap of the address moves the question's attention onto the written slot's locker sentence.
**Mechanics.** Attention from the last and question tokens at every full-attention layer after L; five candidate heads chosen on a fit half; the best head zeroed under the swap.
**Data.** Routes scenes, locker first; 9B and Muse.
**Result.** Sealed; Dan's prediction committed.
**Figure.** None yet.
**Conclusion.** Pending.

<sub>Fixed in advance · jobs/c3/batch49.yaml</sub>

## Part III. Where and when

*The link to the locker is made where the order puts it, and the bridge word is read up to a depth where position takes over.*

### E10. Sentence order: where the link is made <a id="e10-order"></a>

**Hypothesis.** With the locker after the pick, the locker sentences make the link by L (a copy into them carries at least half the switches).
**Mechanics.** The main test split by order; clean scenes; copies into the locker sentences by layer.
**Data.** 200 items per model.
**Result.** Lookups switch in {{num|lk_order_before_muse}}-{{num|lk_order_before_122b}} of locker-first scenes, {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} otherwise. With the locker after, the copy carries {{pt|x45q_c_9b}} / {{pt|x45q_c_27b}} / {{pt|x45q_c_muse}} of its lookup switches, the bridge-word change {{pt|x45q_a_9b}} / {{pt|x45q_a_27b}} / {{pt|x45q_a_muse}}.
**Figure.**

![Lookups follow the change mostly when the locker sentence comes first](figures/story/fig03_order.png)

**Conclusion.** The bridge word carries the link only when the locker came first. Not shown: what the locker sentence holds (pending).

<sub>Order split after the data; the link test fixed in advance · hand-checked: no · results/x0_necessity/</sub>

#### E10c. The earlier mention <a id="e10c-mention"></a>

**Hypothesis.** With its locker first, the recall also reads the item's earlier mention. **Mechanics.** The J++ part removed there too. **Data.** Clean scenes, three models. **Result.** It costs the recall {{pt|x45p_d23_9b}}-{{pt|x45p_d23_muse}} more switches than a random part; the lookup does not move. **Figure.**

![The recall reads the item's earlier mention when its locker came first](figures/story/fig03c_earlier_mention.png)

**Conclusion.** The recall has a second copy of the item. <sub>Fixed in advance · hand-checked: no</sub>

### E11. Token by token, layer by layer <a id="e11-map"></a>

**Hypothesis.** (a) With the locker after the pick, one locker-sentence cell carries the lookup; (b) the lookup stops reading the bridge word before the recall.
**Mechanics.** The changed prompt's state placed into one token group at one layer.
**Data.** Clean scenes, 9B and Muse.
**Result.** Both rules fail: no single locker-sentence cell carries the locker-after lookup; both readers read the bridge word to about the same depth, then the question and the last token carry the answer.
**Figure.**

![The lookup reads the bridge word to layer 16, the recall to layer 14](figures/story/fig03d_depth_map.png)

**Conclusion.** The link is spread, not in one place.

<sub>Fixed in advance · hand-checked: no · results/x47_depthmap/</sub>

### E12. The anatomy by depth <a id="e12-anatomy"></a>

**Hypothesis.** The lookup drops the J++ part no later than it takes up the address; the address is readable before use; never the value.
**Mechanics.** The change and its parts at each sampled layer, against random parts; the slot probe per layer.
**Data.** Routes scenes, fit and test halves; 9B and Muse.
**Result.** Identity early, position in the last window that reads the word; the probe reads the address 8 (9B) and 16 (Muse) layers before position starts; re-encoded early, one code later (mean overlap {{dp|fig06c|9b|D4: the address's mean overlap over every pair of window layers}} / {{dp|fig06c|muse|D4: the address's mean overlap over every pair of window layers}}).
**Figure.**

![With depth the change moves the lookup by identity, then by position](figures/story/fig06b_anatomy.png)

**Conclusion.** The address is written early and read late. Not shown: the 27B (pending).

<sub>Fixed in advance · hand-checked: no · results/x47_anatomy/, results/x47_depth_cpu/</sub>

## Part IV. Harder settings and what did not hold

*The split survives harder prompts in part, and every mechanism we proposed for why failed.*

### E13. A described bridge <a id="e13-described"></a>

**Hypothesis.** With the bridge described ("the one known for honey") the split holds (gap at least 0.3, lookup at most 0.10), or the bridge goes through the lens (lookup at least 0.20).
**Mechanics.** The change at the description's word.
**Data.** 300 items, few bridge items (15 / 15 / 9).
**Result.** Gap {{d|fig05c|9b|47.3: gap (recall's extra loss minus the lookup's)}} (9B), {{d|fig05c|muse|47.3: gap (recall's extra loss minus the lookup's)}} (Muse); the 27B's lookup loses {{d|fig05c|27b|47.3: lookup's extra loss without the J++ part}}. Never the value.
**Figure.**

![A described bridge: the split holds on the 9B and Muse, not on the 27B](figures/story/fig05c_described_bridge.png)

**Conclusion.** On two models the split does not need a named word. Not shown: why the 27B differs.

<sub>Fixed in advance · hand-checked: no · results/x47_cue/</sub>

### E14. Other texts: formats, natural passages, question first <a id="e14-texts"></a>

**Hypothesis.** The split and the address carry over to other formats; with the question first the number is fetched onto the bridge word.
**Mechanics.** The same arms in varied and natural scenes; the address refit per format; the question placed first.
**Data.** Varied scenes, natural passages; question first on the 27B (gate).
**Result.** The split carries; the simple-scene address costs the lookup {{num|tptr_varied_range}} in varied scenes; refit it reaches {{pt|x45d_table_9b}}-{{pt|x45d_prose_9b}} (9B), {{pt|x45d_prose_muse}}-{{pt|x45d_table_muse}} (Muse). Never the number in any format; with the question first the 27B's value probe rises from {{dp|e14_question_first|27b|47.7(a): value probe at the bridge word, question last}} to {{dp|e14_question_first|27b|47.7(a): value probe at the bridge word, question first}}, and its lookup still never answers it.
**Figure.**

![The split carries over to other texts; the pointer must be refit for each format](figures/story/fig09_transfer.png)

**Conclusion.** The split travels; the address must be refit.

<sub>Fixed in advance and after the data · hand-checked: no · results/x47_value/</sub>

### E15. What did not hold: the mechanism tests <a id="e15-failed"></a>

**Hypothesis.** Five accounts of why the readers differ.
**Mechanics.** Probes, mean ablations, head read-outs, blocks, each against a control.
**Data.** 9B and Muse (the second route on three models).
**Result.** All five failed (table).
**Figure.** The table below.

| Account | What was done | Result |
|---|---|---|
| J++ keys the attribute; late MLPs carry the recall | a probe for legs by layer; the bridge word's late MLPs mean-ablated | without J++ the attribute still moves part way; the recall loses {{dp|fig10b|9b|48.2 B, bridge_late: recall accuracy lost}} / {{dp|fig10b|muse|48.2 B, bridge_late: recall accuracy lost}} |
| A person mark at the locker sentence | a probe for who picked the item; a person direction swapped in there | the probe at chance; the swap moves nothing |
| The copying heads pass the rest | each head's output gain on the rest vs the J++ part | about equal; few heads pass the bar |
| The address is the recall's second route | the address swapped on top of the change without J++ | few recalls name the swapped slot's item |
| The pick sentence alone forms the address | the pick sentence blocked from the locker sentences up to L | position answers fall, and identity and recall with them |

**Conclusion.** We know what each reader follows, not how. Not shown: the gain map and the dereference (pending).

<sub>Fixed in advance · hand-checked: no · results/x48_enrich/, results/x48_bind/, results/x48_heads/, results/x48_route2/, results/x47_edges/</sub>

### E16. One question, two sources (pending) <a id="e16-sources"></a>

**Hypothesis.** An instruction that picks the source ("from the passage" / "from what you know") decides the split, not the question.
**Mechanics.** A passage with a false attribute; the same question under two instructions; the J++ part and the address removed.
**Data.** Routes scenes; three models.
**Result.** Sealed; Dan's prediction committed.
**Figure.** None yet.
**Conclusion.** Pending.

<sub>Fixed in advance · jobs/c3/batch47.yaml</sub>

## How we checked

- **Hand-checked numbers:** none yet; [docs/verify_pack.md](docs/verify_pack.md) recounts each claim from the per-item files.
- **Independent reimplementation:** code written from scratch reproduces the 9B's main test on {{num|indep_agree_9b}} random items, every arm.
- **Clean reruns:** the headline cells rerun from a clean checkout (queued).
- **Predictions:** committed before results are opened, then scored ([predictions/](predictions/README.md)): mean Brier {{num|pred_brier}} over {{num|pred_n}} answers, worse than always answering {{q|50%}}.
- **Limits:** one-token answers and bridges; reader and answer source confounded; the 122B in FP8.

## Related work and what is new

Models bind entities to attributes in context (Feng & Steinhardt 2023) and track them through lookback pointers (Prakash et al. 2025) in a low-dimensional order subspace (Dai et al. 2024). The routes test follows Gur-Arieh et al. (2025); the address uses mass-mean directions (Marks & Tegmark 2023); random parts answer Makelov et al. (2023). The lens is the workspace paper's J++ (Gurnee et al. 2026). New here: two readers of one word follow different parts of it; the address is the part the lens misses, and swapping it redirects the lookup.

## Open questions

- **Why does the 27B's lookup need J++ only when all 100 directions go together?**
- **Why does the recall follow J++ without needing it at one layer?** Removing it over four layers costs the 9B's recall about a quarter.
- **Does the address exist in natural text?** Refit per format, it is found on the 9B and Muse, not the 27B.

## Appendix A. Links

Every number on this page comes from [figures/story/data.csv](figures/story/data.csv) and [docs/x0_numbers.json](docs/x0_numbers.json), each with its source comment; [docs/x0_details.md](docs/x0_details.md) has the full tables. All figures on one page: [docs/figures_contact_sheet.png](docs/figures_contact_sheet.png); the figure plan: [docs/figure_plan.md](docs/figure_plan.md). Supplementary figures: [every scene set](figures/supp/s01_split_all_scene_sets.png), [the settings](figures/story/fig01b_settings.png), [every part](figures/supp/s02_parts_all.png), [parts of the same size](figures/story/fig02_specificity.png), [the 27B with more directions](figures/story/fig02b_k_curve.png), [the layer sweep](figures/story/fig03b_layers.png), [the link copy variants](figures/supp/s03d_link_copy_variants.png), [the lookups the change misses](figures/supp/s03e_cumulative.png), [the depth candidate on the main test](figures/story/fig06_depth.png), [the address across depth](figures/story/fig06c_address_depth.png), [the lookup's errors](figures/story/fig07c_probe_errors.png), [the first locker](figures/story/fig08_first_locker.png), [the first sentence and the moves](figures/supp/s08b_pointer_moves_and_neutral_sentence.png), [every routes arm](figures/supp/s05_routes_all_arms.png), [the blocked pick sentence](figures/story/fig09c_formation.png), [chained addresses](figures/story/fig09d_chain.png), [what is left of the route](figures/story/fig10_what_is_left.png), [attribute probe and MLPs](figures/story/fig10b_enrichment.png), [binding](figures/story/fig10c_binding.png), [heads](figures/story/fig10d_heads.png), [second route](figures/story/fig10e_second_route.png), [learned subspaces on Muse](figures/supp/s12_das_muse.png), [the scorecard](figures/story/fig11_scorecard.png). Earlier figures: [figures/status_2026-10-25/](figures/status_2026-10-25/).
