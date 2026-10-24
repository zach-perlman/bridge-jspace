<!-- grid: results/cross_model/20261023T210238Z -->
# bridge-jspace

**Question.** To answer a two-step question, a model first finds an entity in between (the **bridge**) and then uses it. A lens called **J++** reads hidden states as words. Does the model use the part of the bridge's representation that J++ can read, or does it reach the bridge another way? And does that depend on what the model does with the bridge next?

> **Example.** "Iris picked the frog. The locker of the frog is 5. …" The bridge is *frog*.
> - **Lookup:** "Which locker belongs to Iris's pick?" The answer is written in the prompt.
> - **Recall:** "How many legs does Iris's pick have?" The answer comes from the model's memory.

**Status (24 Oct 2026).**
- Models: Qwen3.5-9B, Qwen3.6-27B and Qwen3.5-122B-A10B (FP8 weights, mixture of experts, split over two H100s; its J++ was fitted on the bf16 weights; a hardware gate reproduced a 23 Oct cell first, 0.998 per-row agreement).
- All numbers are unverified (not yet hand-checked); the layers, the rule and Dan's predictions were fixed before any result was opened. Built at {{head}} from the X0 run files. Full log: [jobs/c3/X0.md](jobs/c3/X0.md).

## Main findings

1. **Recall needs the J++ part of the change.** Removing the J++ part of a bridge change costs recalls {{num|rc_jdep_9b}} (9B), {{num|rc_jdep_27b}} (27B) and {{num|rc_jdep_122b}} (122B) of their answer flips. A random part of the same size costs {{num|rc_rdep_9b}}, {{num|rc_rdep_27b}} and {{num|rc_rdep_122b}}.
2. **It is specific to J++.** At the same size, the logit-lens directions, the input embeddings and random directions do nothing comparable, on all three models.
3. **Lookups need it much less.**
   - **9B:** not at any number of J++ atoms (extra loss {{num|lk_excess_k25_9b}} at 25 atoms to {{num|lk_excess_k200_9b}} at 200). The pre-registered test: **confirmed**.
   - **27B:** a little at 25 atoms, so the pre-registered test was **not confirmed**; at 100 atoms about as much as recall ({{num|lk_excess_k100_27b}} vs {{num|rc_excess_k100_27b}}). Added after the data: with an edit that changes only the asked pick, the 27B lookup's extra loss is {{num|single_lk_excess_27b}} (9B: {{num|single_lk_excess_pt_9b}}). At 100 atoms it is still {{num|single_lk_excess_k100_27b}}.
   - **122B:** the pre-registered test at layer 33: **confirmed** (lookup {{num|lk_excess_122b}}; recalls lose {{num|rc_jdep_122b}} of their flips). At 100 atoms the lookup stays at {{num|lk_excess_k100_122b}}. Up to layer 30 both readers need the J++ part. Its J++ part takes no smaller a share of the change ({{num|jshare_122b}}) than the 27B's ({{num|jshare_27b}}) or the 9B's ({{num|jshare_9b}}), so its weaker recall dependence is not a smaller J++ share; its cause is open.
4. **Not a missing digit.** Lookups flip mostly when the locker sentence comes *before* the pick sentence, so the lookup might read a locker number already attached to the bridge word, which our letter-only J++ dictionary cannot remove. The digit tokens are not the route: with every token allowed, digits included, the 27B lookup's extra loss is {{num|dig_lk_jppall_k25_before_27b}} (letters only: {{num|dig_lk_jpp_k25_before_27b}}), and the 10 digit directions alone give {{num|dig_lk_jppdig_k10_before_27b}} on all three models.
5. **The address and the value at the bridge word, outside the J++ part (descriptive, probes).** On 1,500 fresh scenes, where the locker sentence comes before the pick, both are linearly readable at the bridge word: which sentence holds the bridge's locker ({{num|v4_b_before_27b}} on the 27B, {{num|v4_b_before_9b}} on the 9B; the layout alone gives {{num|v4_b_layout_before_27b}}) and the locker number ({{num|v4_a_before_27b}} and {{num|v4_a_before_9b}}, chance 0.11; {{num|v4_a_resid_27b}} and {{num|v4_a_resid_9b}} with the sentence factored out). On the one-change pairs the address readout follows the edit (both members of a pair right in {{num|pair_right_27b}} on the 27B, {{num|pair_right_9b}} on the 9B; the layout alone gets none). The readout tracks the item's first mention in the context, which in these scenes is the locker sentence. Where another person's pick of the item comes first, it points there: on the 9B in {{num|dup_otherfirst_reads_other_9b}} of such pairs, and the lookup still switches to the alt's locker in {{num|fm_lk_whole_other_9b}} (27B: {{num|dup_otherfirst_reads_other_27b}} and {{num|fm_lk_whole_other_27b}}; the same without the J++ part). So the bridge word carries a first-mention pointer that a linear probe reads and the lens does not, and the lookup does not need it (the model may hold another pointer in other directions). The change of address sits in the rest of the edit, not in its J++ part: at 25 atoms the J++ part holds {{num|patched_j25_share_27b}} of the change but {{num|patched_j25_probe_energy_27b}} of its component along the probe's directions (27B). Removing the ridge probe's 4 address directions ({{num|amn_share_27b}} of the change), or keeping only them, changes no lookup ({{num|amn_lk_excess_27b}}): the probe's directions are not what the lookup reads.
6. **Beyond one scene type (X0b, exploratory; one-change edit).** On 7 topics × prose / JSON / tables × 3 difficulty levels, the pooled rule holds on both models: 27B lookup {{num|x0b_lk_excess_27b}}, C {{num|x0b_c_27b}} ({{num|x0b_n_27b}} scenes, {{num|x0b_cells_27b}} cells pass the gate); 9B lookup {{num|x0b_lk_excess_9b}}, C {{num|x0b_c_9b}} ({{num|x0b_n_9b}} scenes; under the brief's stricter C threshold, 0.30, only the 27B passes). On the 27B, locker-before lookups are around in JSON ({{num|x0b_lk_before_json_27b}}) and tables ({{num|x0b_lk_before_table_27b}}) and mixed in prose ({{num|x0b_lk_before_prose_27b}}); at 100 atoms the 27B lookup reaches {{num|x0b_lk_k100_27b}}, as on X0's scenes. The address probe (which locker row is the bridge's) reads above every baseline in every format (locker-before, 27B: prose {{num|x0b_probe_prose_27b}}, JSON {{num|x0b_probe_json_27b}}, tables {{num|x0b_probe_table_27b}}).

![Removing the J++ part costs recall far more than lookup](figures/status_2026-10-24/f1_readers.png)

## How we test it

- **Change the bridge.** Make a copy of the prompt where Iris picks a different animal (frog → tick). At one layer, take the difference between the two hidden states at the bridge word.
- **Paste the change back in three ways:** whole; without its J++ part (the 25 J++ directions that best describe it); without a random part of the same size.
- **Ask both questions on the same patched prompt.** The question comes after the patch, so both readers get the exact same edit. Any difference comes from the reader, not the edit.
- **Measure** how many answers flip to the new animal's answer. The key number is the **extra loss**: the flips lost without the J++ part, minus the flips lost without the random part, both as shares of the whole change's flips.

## Results at the pre-registered layer

| Model, layer | Lookup: extra loss | Recall: extra loss | Rule (pre-registered, two-change edit) | Recall minus lookup, C: two-change edit | C: one-change edit | J++ part's median share of the change's ‖Δ‖² |
|---|---|---|---|---|---|---|
| 9B, {{num|layer_9b}} | {{num|lk_excess_9b}} | {{num|rc_excess_9b}} | **{{num|verdict_9b}}** | {{num|contrast_9b}} | {{num|single_contrast_9b}} | {{num|jshare_9b}} |
| 27B, {{num|layer_27b}} | {{num|lk_excess_27b}} | {{num|rc_excess_27b}} | **{{num|verdict_27b}}** | {{num|contrast_27b}} | {{num|single_contrast_27b}} | {{num|jshare_27b}} |
| 122B, {{num|layer_122b}} | {{num|lk_excess_122b}} | {{num|rc_excess_122b}} | **{{num|verdict_122b}}** | {{num|contrast_122b}} | not run | {{num|jshare_122b}} |

How to read this:
- The rule asked for a lookup extra loss of at most 0.10, and for recalls to lose at least 0.30 of their flips without the J++ part. The headline is C, the recall's extra loss minus the lookup's, under both edits; the categorical verdicts are the pre-registered ones (two-change edit).
- In answer counts (27B, {{num|n_27b}} scenes): lookups go {{num|lk_whole_27b}} → {{num|lk_noj_27b}} without J++ and {{num|lk_whole_27b}} → {{num|lk_norand_27b}} without the random part; recalls go {{num|rc_whole_27b}} → {{num|rc_noj_27b}} and {{num|rc_whole_27b}} → {{num|rc_norand_27b}}.
- Scope: almost all of the lookup's flips at the bridge word come from scenes where the locker sentence comes before the pick; the lookup results describe those scenes.
- {{q|95%}} intervals come from resampling the bridge entities ({{num|ents_9b}} on the 9B, {{num|ents_27b}} on the 27B, {{num|ents_122b}} on the 122B).

![The graded contrast holds under both edits](figures/status_2026-10-24/f10_contrast.png) ![27B: both readers depend on the J++ part up to L26; from L28 only recall does](figures/status_2026-10-24/f2_depth.png)

![On the 27B, with more J++ atoms the lookup needs J++ too](figures/status_2026-10-24/f5_atoms.png)

![It is J++, not any dictionary](figures/status_2026-10-24/f3_dictionaries.png) ![Adding the digit tokens to J++ changes nothing](figures/status_2026-10-24/f6_digits.png)

![The bridge word holds where its locker is](figures/status_2026-10-24/f7_probe.png) ![The address is in the rest of the change, not in its J++ part](figures/status_2026-10-24/f8_address.png) ![A first-mention pointer the lens does not read, and the lookup does not need](figures/status_2026-10-24/f9_first_mention.png)

## What did not hold

- **"Past mid-depth, lookups don't use the J++ part of the change at all."** It holds on the 9B, and on the 122B from layer 33. On the 27B it holds only when the change is pasted across the whole context (lookups {{num|ctx_lookup_full}} → {{num|ctx_lookup_noj}} without J++, recalls {{num|ctx_recall_full}} → {{num|ctx_recall_noj}}). That repeats a 23 Oct result on fresh scenes, but at the bridge word alone it does not hold.
- **"The lookup reads the answer digit at the bridge word"** (stated before the check). Digit tokens change nothing (above), and the J++ readout at the bridge word ranks the lookup's answer digit first in {{num|dig_readout_first_before_27b}} of items (27B; chance is {{q|10%}}).
- **Prompts without the chat template.** Can't test: the models open a thinking block or answer in markdown. This says nothing about the question.

## Weak spots we know about

| Weak spot | Status |
|---|---|
| The J++ part is mostly not the bridge word: the bridge's own tokens are among its top 25 atoms in {{num|atoms_bridge_top25_letters}} items and carry {{num|atoms_bridge_coef2_letters}} of it (27B; 9B: {{num|atoms_bridge_top25_letters_9b}}, {{num|atoms_bridge_coef2_letters_9b}}). Removing the word alone costs the recall {{num|parts_w_rc_excess_27b}} (27B) and {{num|parts_w_rc_excess_9b}} (9B); J++ without the word costs it {{num|parts_jw_rc_excess_27b}} and {{num|parts_jw_rc_excess_9b}}, as much as J++ ({{num|parts_jpp_rc_excess_27b}}, {{num|parts_jpp_rc_excess_9b}}): the recall's loss is J++ beyond the word. A PCA dictionary of the layer (top 2,000 directions, 25 atoms, {{num|parts_pca_share_27b}} of the change on the 27B) costs both readers (lookup {{num|parts_pca_lk_excess_27b}}, recall {{num|parts_pca_rc_excess_27b}}): it is not reader-specific, J++ is (not at equal share) | descriptive, done (x0_parts) |
| The lookup's route: an address at the bridge word (descriptive, probe; it tracks the item's first mention), outside the J++ part; not J++ on the 9B and the 122B, not a digit on any model. The ridge probe's 4 directions are not what the lookup reads: removing them, or keeping only them, changes no lookup ({{num|amn_lk_excess_27b}} on the 27B, {{num|amn_lk_excess_9b}} on the 9B) | mass-mean address and value subspaces (next); X4 |
| Lookup flips depend on sentence order: locker before pick {{num|lk_order_before_27b}}–{{num|lk_order_before_122b}}, after {{num|lk_order_after_27b}}–{{num|lk_order_after_9b}} | figure F4; X0b fixes the order by design |
| The two-change edit inflated the extra loss: on the same items, one change instead of two moves the recall's by {{num|paired_rc_excess_27b}} (27B) and {{num|paired_rc_excess_9b}} (9B), the 27B lookup's by {{num|paired_lk_excess_27b}} | the one-change edit from X0b on (it makes two people pick the same item) |
| On the 27B, the lookup's drop with depth follows how much of the change J++ captures (Spearman {{num|share_rho_27b}}) | stated beside the depth figure |
| Three models from one family, generated scenes only | X0b: 7 topics, 3 formats, 3 levels (holds on both models); natural text parked (X3) |

![What moves lookups: sentence order](figures/status_2026-10-24/f4_order.png)

## Next

| Step | What it tells us |
|---|---|
| X4 (queued): the locker key written word for word, translated (animals) or by chemical symbol (elements, the positive control); the probe first | whether the contrast holds on natural text, or whether the address forms only when the key matches word for word |

## More

- [Detailed results](docs/x0_details.md): every layer, every dictionary and number of atoms, subsets, controls, simple explanations we ruled out.
- [Pre-registration and every change made after the data](jobs/c3/X0.md) · [Dan's predictions and scores](predictions/2026-10-24_dan.md).
- [Earlier claims and history](CHANGELOG.md) · [Zach's breadth results](https://github.com/zach-perlman/bridge-jspace/tree/zach/v8-breadth-1021).

Prior work: the workspace paper (Gurnee et al. 2026); two-hop recall resolves its bridge early (Biran et al. 2024).
