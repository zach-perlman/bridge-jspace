<!-- grid: results/cross_model/20261023T210238Z -->
# When a model answers a two-step question, does it use the part of the in-between entity that a lens can read, and does that depend on what it does with that entity next?

**Answer.** Recalling a fact about the in-between entity from memory needs the lens-readable (J++) part of its representation far more than looking its answer up in the prompt does, on three Qwen models (at the default 25 J++ directions), and on two of them in varied scenes. The lookup instead uses something at that word the lens does not read; on the 9B, a few directions that point at where the item was first mentioned carry the lookup (after the data; a replication fixed in advance is pending).

**Status.** Qwen3.5-9B, Qwen3.6-27B, Qwen3.5-122B-A10B. All numbers are unverified until hand-checked. 25 Oct 2026. Built at {{head}} from the run files.

## How to read this page

> "Iris picked the frog. The locker of the frog is 5. …" The in-between entity, the **bridge**, is *frog*.
> - **Lookup:** "Which locker belongs to Iris's pick?" (the answer is written in the prompt)
> - **Recall:** "How many legs does Iris's pick have?" (the answer comes from the model's memory)

**The one test used throughout.** We change the bridge (frog → tick) and, at one layer, take the change in the hidden state at the bridge word. We add the change back into the unedited prompt's forward pass at that word in three ways: whole, without its J++ part, or without a random part of the same size. Both questions (the two readers) read the same edited prompt, so any difference between them comes from the reader, not the edit. The main test's edit swaps two people's picks; later tests change only the asked person's pick. Brackets are {{q|95%}} intervals from resampling the bridge items (10,000 resamples, seed 0).

- **J++ part:** J++ is a lens that reads a hidden state as words; each word has a direction. The J++ part is the combination of 25 such directions (by default) that best rebuilds the change; its share is its fraction of the change's squared length.
- **Extra loss:** a reader's answer switches when it gives the new bridge's answer. Extra loss = the share of the switches the whole change causes that are lost without the J++ part, minus the share lost without the random part.
- **Recall-lookup gap:** the recall's extra loss minus the lookup's.
- **Tags:** [fixed in advance] = the test, the layer and the pass bar were written down before any result; [after the data] = added after seeing results.

## 1. Recall needs the J++ part far more than lookup does [fixed in advance]

- **Hypothesis.** At the layer fixed in advance, recall needs the J++ part of the bridge change and lookup does not. It would be wrong if the lookup's extra loss were above 0.10 or if recall lost less than 0.30 of its switches without the J++ part (raw, not extra loss).
- **Experiment.** At one layer per model fixed in advance (9B layer {{num|layer_9b}}, 27B layer {{num|layer_27b}}, 122B layer {{num|layer_122b}}), 200 scenes each, an edit that swaps two people's picks. The J++ part (25 directions) is removed, and as a control a random part of the same size.
- **Result.** The recall-lookup gap is {{num|contrast_9b}} on the 9B, {{num|contrast_27b}} on the 27B and {{num|contrast_122b}} on the 122B: without the J++ part, recall loses that much more of its answer switches than lookup does. The strict test passed on the 9B and the 122B and missed on the 27B, whose lookup lost {{num|lk_excess_27b}} (bar 0.10); with an edit that changes one pick (after the data), {{num|single_lk_excess_27b}}. In counts (27B, 200 scenes): recall switches {{num|rc_whole_27b}} → {{num|rc_noj_27b}} without the J++ part and {{num|rc_whole_27b}} → {{num|rc_norand_27b}} without the random part; lookup {{num|lk_whole_27b}} → {{num|lk_noj_27b}} and {{num|lk_whole_27b}} → {{num|lk_norand_27b}}.

![Removing the J++ part costs recall far more than lookup](figures/status_2026-10-25/f1_readers.png)
*Share of the change's flips each reader loses without the J++ part (colour) or a random part (grey). Compare each reader's J++ bar with its dashed bar fixed in advance.*

- **How to read it.** The lookup still uses the bridge (its answers switch with it); it just does not need the bridge's J++ part to do so. This does not say the lookup never needs J++: on the 27B it does at 100 J++ directions (finding 3's second figure). Main caveat: lookups were measured almost only in scenes where the locker sentence comes first (finding 4).

## 2. It holds beyond the simple scenes [after the data; its pass bars were fixed before its own run]

- **Hypothesis.** The gap is not a quirk of one scene template or of the locker key matching the pick word. It would be wrong if, in varied scenes, the lookup's extra loss rose above 0.10 or the gap fell below 0.20 (bars fixed before that run), or if a translated locker key raised the lookup's extra loss by 0.20 or more.
- **Experiment.** Varied scenes: 7 topics, prose / JSON / tables, 3 difficulty levels; {{num|x0b_n_27b}} scenes on the 27B and {{num|x0b_n_9b}} on the 9B; an edit that changes one pick. Locker key in another language: the locker statements name 8 animals in French, Spanish or German while the picks stay in English (about 400 scenes per form); the same with 6 chemical elements named by symbol, as a positive control (a symbol such as O can be matched to "oxygen" only through knowledge, so there the lookup should need J++).
- **Result.** In varied scenes the recall-lookup gap is {{num|x0b_c_27b}} (27B) and {{num|x0b_c_9b}} (9B), with the lookup's extra loss at {{num|x0b_lk_excess_27b}} and {{num|x0b_lk_excess_9b}}. With the locker key in another language, the lookup's extra loss changes by {{num|x4_D_animals_27b}} (27B) and {{num|x4_D_animals_9b}} (9B) against the English key.

![The recall-lookup gap holds in varied scenes](figures/status_2026-10-25/f13_x0b.png) ![With the locker key in another language, the lookup still does not need the J++ part](figures/status_2026-10-25/f16_x4.png)
*Left: compare the purple (lookup) and dark (recall) bar in each group. Right, bottom: compare each diamond with the dashed line at 0.20.*

- **How to read it.** In locker-first scenes, the lookup does not need the J++ part at the pick word even without a word-for-word match. The model may have linked the translated name to its English concept at the locker statement, so this does not mean that no concept is needed anywhere. Caveats: the positive control stayed below its bar (Limits); the 9B's gap in varied scenes is below the sprint plan's stricter bar of 0.30.

## 3. The J++ part is more than the layer's main directions, and recall can use either the word or the rest [after the data]

- **Hypothesis.** If J++ only picked out the layer's most common directions, those directions at the same share would cost recall as much as J++; if recall read only the bridge word itself, the word's directions alone would cost as much as J++.
- **Experiment.** An edit that changes one pick, 200 scenes per model (9B, 27B). Removed in turn, each against a random part of its own share: the layer's main directions (top 2,000 principal directions, as many per scene as match that scene's J++ share); the bridge word's own J++ directions (the word and its spelling variants); J++ without the word's directions (fit after the word part is taken out). Also logit-lens directions, input embeddings and random directions at 25-200 directions, on all three models.
- **Result.** Recall's extra loss: J++ {{num|pcaeq_jpp_rc_excess_27b}} (27B) and {{num|pcaeq_jpp_rc_excess_9b}} (9B); the main directions at the same share {{num|pcaeq_pca_eq_rc_excess_27b}} and {{num|pcaeq_pca_eq_rc_excess_9b}}; the word alone {{num|parts_w_rc_excess_27b}} and {{num|parts_w_rc_excess_9b}}; J++ without the word's directions {{num|pcaeq_jwo_rc_excess_27b}} and {{num|pcaeq_jwo_rc_excess_9b}}. Logit-lens, input-embedding and random directions cost neither reader anything comparable.

![At the same share, the layer's main directions and J++ without the word's directions cost the recall far less than J++](figures/status_2026-10-25/f14_pcaeq.png) ![Logit-lens, input-embedding and random directions do nothing; only J++ separates the readers](figures/status_2026-10-25/f3_dictionaries.png)
*Left: compare the dark (recall) bar of J++ with the other two parts, which take about the same share of the change. Right: compare the J++ lines with the grey bands.*

- **How to read it.** Word alone {{num|parts_w_rc_excess_27b}} / {{num|parts_w_rc_excess_9b}}, J++ without the word's directions {{num|pcaeq_jwo_rc_excess_27b}} / {{num|pcaeq_jwo_rc_excess_9b}}, both together (J++) {{num|pcaeq_jpp_rc_excess_27b}} / {{num|pcaeq_jpp_rc_excess_9b}}: super-additive, i.e. the recall reads the bridge from either part (descriptive). This does not make J++ the only route: at twice J++'s share, the main directions cost both readers ({{num|parts_pca_lk_excess_27b}} lookup, {{num|parts_pca_rc_excess_27b}} recall on the 27B). Caveat: two models, after the data.

## 4. Lookups move only when the locker sentence comes first [after the data]

- **Hypothesis.** An edit at the bridge word should switch the lookup's answer whatever the sentence order. It would be wrong if switching depended on whether the locker sentence comes before or after the pick.
- **Experiment.** The whole edit, no part removed, in the main test's scenes, split by sentence order; about 100 scenes per group, all three models.
- **Result.** {{num|lk_order_before_27b}}-{{num|lk_order_before_122b}} of lookups switch when the locker sentence comes before the pick, {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} when it comes after.

![Lookups move only when the locker sentence comes first](figures/status_2026-10-25/f4_order.png)
*Compare the dark purple bar (locker first) with the light one (locker after) for each model.*

- **How to read it.** In locker-after scenes the lookup rarely depends on the bridge word at all, so there is little to measure there; every lookup claim on this page describes locker-first scenes. It does not say how the lookup works in locker-after scenes.

## 5. The bridge word holds a pointer to the item's first mention, outside the J++ part [after the data]

- **Hypothesis.** If the lookup goes through the bridge word, that word's state should say where the locker is. It would be wrong if a linear probe could not beat what the scene's layout alone predicts.
- **Experiment.** A linear probe at the bridge word, trained on 1,500 fresh locker-first scenes (tested on items it did not see), answers "which sentence holds this item's locker?". It is then read on edited states, on parts of the change, in scenes with the locker key in another language, and in pairs where the new pick was already picked by another person earlier in the scene.
- **Result.** The probe is right in {{num|v4_b_before_27b}} (27B) and {{num|v4_b_before_9b}} (9B) of scenes, against {{num|v4_b_layout_before_27b}} for a guess from which sentences before the pick are locker sentences. It forms for translated statements too (27B: {{num|x4_probe_animals_xlang_27b}}; 9B: {{num|x4_probe_animals_xlang_9b}}; trained on English keys, tested on translated ones: {{num|x4_transfer_animals_27b}} and {{num|x4_transfer_animals_9b}}) and for symbols ({{num|x4_probe_elements_syn_27b}} and {{num|x4_probe_elements_syn_9b}}; transfer {{num|x4_transfer_elements_27b}} and {{num|x4_transfer_elements_9b}}). Of the part of the change the probe's directions can see, the J++ part holds {{num|patched_j25_probe_energy_27b}} (27B). When another person's pick of the item comes first, the probe points at that pick sentence in {{num|dup_otherfirst_reads_other_9b}} of 9B pairs ({{num|dup_otherfirst_reads_other_27b}} on the 27B), and the lookup still switches to the right locker in {{num|fm_lk_whole_other_9b}}.

![The bridge word points at the item's first mention; the lookup still switches when that pointer is wrong](figures/status_2026-10-25/f9_first_mention.png) ![The pointer is in the rest of the change, not in its J++ part](figures/status_2026-10-25/f8_address.png)
*Left, top: compare the grey bars (pointing at the other person's pick) with the blue ones (pointing at the new pick's locker). Right: compare the J++ part with the rest.*

- **How to read it.** The pointer is not lexical: it is a first-mention pointer at the entity level, which the lens does not read. It does not show that the lookup reads this pointer: the lookup switches correctly even when the pointer points the wrong way, and it switches in nearly every such pair whatever is removed, so that comparison cannot show a dependence.

## 6. On the 9B, pointer directions outside the lens carry the lookup [after the data; replication pending]

- **Hypothesis.** If the lookup reads the pointer, removing the directions that encode it should cost the lookup and not the recall. It would be wrong if it cost both readers or neither.
- **Experiment.** The **pointer directions** are the 4 directions that separate the average state for each "which sentence holds the locker" answer on fresh scenes, after each layout's average is taken out (so they do not just encode which sentences are locker sentences). They are removed from an edit that changes one pick, against a random part of the same share, and compared with the J++ part and the layer's main directions at about the same share. Pointer directions: the {{num|mmlf_n_lk_9b}} (9B) and {{num|mmlf_n_lk_27b}} (27B) of those scenes whose old and new pick both have their locker sentence before the pick; J++ and main directions: all 200 scenes.
- **Result.** On the 9B the pointer directions cost the lookup {{num|mmlf_Alf_lk_excess_9b}} and the recall {{num|mmlf_Alf_rc_excess_9b}}. On the same scenes J++ costs the recall only {{num|ss_jpp_rc_excess_9b}} and the lookup {{num|ss_jpp_lk_excess_9b}} (on all 200 scenes: recall {{num|pcaeq_jpp_rc_excess_9b}}); the main directions {{num|ss_pca_lk_excess_9b}} and {{num|ss_pca_rc_excess_9b}}. On the 27B's same scenes J++ costs the recall {{num|ss_jpp_rc_excess_27b}}. On the 27B the pointer directions cost both readers ({{num|mmlf_Alf_lk_excess_27b}} lookup, {{num|mmlf_Alf_rc_excess_27b}} recall). In the pairs where another person's pick of the new item comes first, the edited state's nearest class average points at that pick sentence, not at the new item's locker sentence: {{num|dupnn_A_otherfirst_other_9b}} with the layout averages kept and {{num|dupnn_Alf_otherfirst_other_9b}} in the pointer directions on the 9B ({{num|dupnn_A_otherfirst_other_27b}} and {{num|dupnn_Alf_otherfirst_other_27b}} on the 27B), and the lookup still switches to the right locker ({{num|fm_lk_whole_other_9b}} on the 9B).

![On the same scenes, the pointer directions cost the 9B's lookup; J++ costs the 27B's recall but barely the 9B's](figures/status_2026-10-25/f15_pointer.png)
*All three parts on the same scenes. Compare the purple (lookup) and dark (recall) bar across the three parts in each panel.*

- **How to read it.** On these scenes the 9B's recall barely depends on J++, so the two readers' dependence on different parts holds across scene sets (J++ on all scenes, the pointer directions on locker-first scenes), not within the same scenes. The 9B lookup needs the pointer directions, but the 'where' they encode can point to the wrong sentence without hurting the lookup, so the lookup reads something else from them. Caveats: one model, after the data, 73 scenes; a replication fixed in advance is pending (closed until batch 31 is committed).

## What did not hold

- **The lookup reads the locker number at the bridge word.** Adding all digit tokens to J++ leaves the 27B lookup's extra loss unchanged ({{num|dig_lk_jppall_k25_before_27b}} with them, {{num|dig_lk_jpp_k25_before_27b}} with letters only); the 10 digit directions alone give {{num|dig_lk_jppdig_k10_before_27b}}.
- **The probe's own directions carry the lookup.** Removing them changes no lookup ({{num|amn_lk_excess_27b}} on the 27B, {{num|amn_lk_excess_9b}} on the 9B). These 4 directions come from a probe fit on standardized states, which favours rare directions; finding 6's pointer directions are class averages, a different set.
- **The strict test on the 27B.** Its lookup lost {{num|lk_excess_27b}} (bar 0.10), and at 100 J++ directions about as much as recall ({{num|lk_excess_k100_27b}} vs {{num|rc_excess_k100_27b}}).

## Limits

- **Positive control.** Chemical symbols should make the lookup need J++ (bar 0.20): on the 27B {{num|x4_D_elements_27b}}, below the bar but positive for {{num|x4_Dpos_elements_27b}} elements; null on the 9B ({{num|x4_D_elements_9b}}).
- **The 122B** was tested at one layer for most checks, in FP8 weights, with J++ fitted on the bf16 weights.
- **One model family** (Qwen) and generated scenes only.
- **Prompts without the chat template** could not be tested: the models open a thinking block or answer in markdown.
- **The edit that changes one pick** makes two people pick the same item; that is how the pairs in finding 5 arise.

## Next

| Step | What it tells us |
|---|---|
| A replication of finding 6, fixed in advance (fresh scenes; spec and Dan's predictions first) | whether the 9B's lookup and recall really depend on different parts of the change |
| Slides (Thu-Fri) | the six findings for the sprint review |
| After the sprint: distributed alignment search at the bridge word | how the lookup reads what it needs |

## Figures

Figures in [figures/status_2026-10-25/](figures/status_2026-10-25/) (the 24 Oct folder stays as shared). Panels from tonight's runs say "closed" until the batch-31 answers are committed.

| Figure | Claim | Models | | Role |
|---|---|---|---|---|
| F1 | Removing the J++ part costs recall far more than lookup | 9B, 27B, 122B | fixed in advance | main |
| F13 (+F18) | The recall-lookup gap holds in varied scenes (natural passages: closed) | 9B, 27B (122B queued) | rule fixed in advance | main |
| F14 | At the same share, the main directions and J++ without the word's directions cost the recall far less than J++ | 9B, 27B (122B closed) | after the data | main |
| F4 | Lookups move mostly when the locker sentence comes first | 9B, 27B, 122B | after the data | main |
| F9 | The bridge word points at the first mention; the lookup still switches when it is wrong | 9B, 27B (122B closed) | after the data | main |
| F15 (+F19) | On the same scenes, the pointer directions cost the 9B's lookup (replication: closed) | 9B, 27B (122B closed) | after the data (F19 fixed in advance) | main |
| F2, F3, F5, F6, F7, F8, F10, F16, F17 | depth; dictionaries; number of J++ directions; digits; probes; pointer outside J++; both swaps; translated keys; varied-scene parts | per figure | per figure | supplementary |
| F11, F12 | superseded by F14 (unequal shares) and F15 | 9B, 27B | after the data | superseded |

## Where the runs are

| Finding | Run folders (results/) | Spec | Predictions |
|---|---|---|---|
| 1 | x0_necessity/{qwen35_9b_x0_necessity, x0_necessity_27b_chat, qwen35_122b_x0_necessity_r2, *_single_r2} | [X0.md](jobs/c3/X0.md) | batches 25, 26 |
| 2 | x0b_generalize/*x0b_v2*; x4_alias/* | [X0b.md](jobs/c3/X0b.md), [X4.md](jobs/c3/X4.md) | batches 27, 29 |
| 3 | x0_parts/{*x0_parts*, *pcaeq*, *x0b_parts*}; x0_necessity/*kmatch* | [x0_parts.yaml](jobs/c3/x0_parts.yaml), [x0_pcaeq_mmlf.yaml](jobs/c3/x0_pcaeq_mmlf.yaml) | batches 25, 28, 30 |
| 4 | x0_necessity/* (cases and outcomes) | [X0.md](jobs/c3/X0.md) | — |
| 5 | x0_probe/*v4*; x0_amnesic/*/probe-patched-*; x4_alias/*probe*; x0_massmean/*_lf/dup-nearest-* | [x0_probe_power.yaml](jobs/c3/x0_probe_power.yaml) | batches 27, 29 |
| 6 | x0_massmean/{*massmean*, *_lf}; x0_parts/*pcaeq* | [x0_massmean.yaml](jobs/c3/x0_massmean.yaml), [x0_pcaeq_mmlf.yaml](jobs/c3/x0_pcaeq_mmlf.yaml) | batch 28 |

Internal names: X0 = the main test, X0b = varied scenes, X4 = the locker key in another language or as a symbol, Alf = the pointer directions. [Detailed results](docs/x0_details.md) · [Dan's predictions and scores](predictions/2026-10-24_dan.md) · [calibration](predictions/README.md) · [earlier claims](CHANGELOG.md) · [Zach's breadth results](https://github.com/zach-perlman/bridge-jspace/tree/zach/v8-breadth-1021).

Prior work: the workspace paper (Gurnee et al. 2026); two-hop recall resolves its bridge early (Biran et al. 2024); mass-mean probing (Marks & Tegmark 2023).
