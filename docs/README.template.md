<!-- grid: results/cross_model/20261023T210238Z -->
# bridge-jspace

**Question.** To answer a two-step question, a model first finds an entity in between (the **bridge**) and then uses it. A lens called **J++** reads hidden states as words. Does the model use the bridge in that word-like form, or does it reach it another way? And does that depend on what the model does with the bridge next?

> **Example.** "Iris picked the frog. The locker of the frog is 5. …" The bridge is *frog*.
> - **Lookup:** "Which locker belongs to Iris's pick?" The answer is written in the prompt.
> - **Recall:** "How many legs does Iris's pick have?" The answer comes from the model's memory.

**Status (24 Oct 2026).**
- Models: Qwen3.5-9B and Qwen3.6-27B. Qwen3.5-122B is in progress.
- All numbers are unverified (not yet hand-checked). Built at {{head}} from the X0 run files.
- The layers, the rule and Dan's predictions were fixed before any result was opened. Full log: [jobs/c3/X0.md](jobs/c3/X0.md).

## Main findings

1. **Recall needs the bridge's J++ form.** Removing the J++ part of a bridge change costs recalls {{num|rc_jdep_9b}} (9B) and {{num|rc_jdep_27b}} (27B) of their answer flips. A random part of the same size costs {{num|rc_rdep_9b}} and {{num|rc_rdep_27b}}.
2. **It is specific to J++.** At the same size, the logit-lens directions, the input embeddings and random directions do nothing comparable.
3. **Lookups need the J++ form much less, and the two models differ.**
   - **9B:** the lookup does not need it, at any number of J++ atoms (extra loss {{num|lk_excess_k25_9b}} at 25 atoms to {{num|lk_excess_k200_9b}} at 200, on a rerun of the same scenes). The pre-registered test: **confirmed**.
   - **27B:** the lookup needs it a little at 25 atoms, so the pre-registered test was **not confirmed**. At 100 atoms (same rerun) it needs it about as much as recall does ({{num|lk_excess_k100_27b}} vs {{num|rc_excess_k100_27b}}).
4. **Open lead.** Lookups flip mostly when the locker sentence comes *before* the pick sentence. The lookup may read a locker number already attached to the bridge word, and our J++ dictionary has no digit tokens. This is being checked now.

![Removing the J++ part costs recall far more than lookup](figures/status_2026-10-24/f1_readers.png)

## How we test it

- **Change the bridge.** Make a copy of the prompt where Iris picks a different animal (frog → tick). At one layer, take the difference between the two hidden states at the bridge word.
- **Paste the change back in three ways:**
  - whole;
  - without its J++ part (the 25 J++ directions that best describe it);
  - without a random part of the same size.
- **Ask both questions on the same patched prompt.** The question comes after the patch, so both readers get the exact same edit. Any difference comes from the reader, not the edit.
- **Measure** how many answers flip to the new animal's answer. The key number is the **extra loss**: the flips lost without the J++ part, minus the flips lost without the random part, both as shares of the whole change's flips.

## Results at the pre-registered layer

| Model, layer | Lookup: extra loss | Recall: extra loss | Rule | Recall minus lookup |
|---|---|---|---|---|
| 9B, {{num|layer_9b}} | {{num|lk_excess_9b}} | {{num|rc_excess_9b}} | **{{num|verdict_9b}}** | {{num|contrast_9b}} |
| 27B, {{num|layer_27b}} | {{num|lk_excess_27b}} | {{num|rc_excess_27b}} | **{{num|verdict_27b}}** | {{num|contrast_27b}} |

How to read this:
- The rule asked for a lookup extra loss of at most 0.10, and for recalls to lose at least 0.30 of their flips without the J++ part.
- In answer counts (27B, {{num|n_27b}} scenes): lookups go {{num|lk_whole_27b}} → {{num|lk_noj_27b}} without J++ and {{num|lk_whole_27b}} → {{num|lk_norand_27b}} without the random part; recalls go {{num|rc_whole_27b}} → {{num|rc_noj_27b}} and {{num|rc_whole_27b}} → {{num|rc_norand_27b}}.
- {{q|95%}} intervals come from resampling the bridge entities ({{num|ents_9b}} on the 9B, {{num|ents_27b}} on the 27B).

![Recall depends on the J++ form at every depth; lookup only early](figures/status_2026-10-24/f2_depth.png)

![On the 27B, with more J++ atoms the lookup needs J++ too](figures/status_2026-10-24/f5_atoms.png)

![It is J++, not any dictionary](figures/status_2026-10-24/f3_dictionaries.png)

## What did not hold

- **"Past mid-depth, lookups don't use the J++ form at all."** It holds on the 9B.
  - On the 27B it holds only when the change is pasted across the whole context (lookups {{num|ctx_lookup_full}} → {{num|ctx_lookup_noj}} without J++, recalls {{num|ctx_recall_full}} → {{num|ctx_recall_noj}}). That repeats a 23 Oct result on fresh scenes, but at the bridge word alone it does not hold.
- **Prompts without the chat template.** Can't test: the models open a thinking block or answer in markdown. This says nothing about the question.

## Weak spots we know about

| Weak spot | Status |
|---|---|
| The J++ dictionary has no digit tokens; lookups may read a digit at the bridge word | checking now |
| Lookup flips depend on sentence order: locker before pick {{num|lk_order_before_27b}}–{{num|lk_order_before_9b}}, after {{num|lk_order_after_27b}}–{{num|lk_order_after_9b}} | figure F4; the next experiments fix the order |
| The edit changes two picks, not one: the 27B lookup's extra loss is {{num|lk_excess_up_27b}} where the second change comes first, {{num|lk_excess_af_27b}} where it does not (too few flips to measure) | a single-change version is next |
| On the 27B, the lookup's drop with depth follows how much of the change J++ captures (Spearman {{num|share_rho_27b}}) | stated beside the depth figure |
| Two models from one family, generated scenes only | 122B in progress; diverse and natural-text sets planned |

![What moves lookups: sentence order](figures/status_2026-10-24/f4_order.png)

## Next

| Step | What it tells us |
|---|---|
| Digit check: add digit tokens to the J++ dictionary | whether the lookup's "other route" is just a digit we didn't look at |
| Qwen3.5-122B on the same test | whether the contrast changes with model size |
| An edit with one change | whether the 27B result comes from how we built the edit |
| X2' (9B): the final fact made up in the text, true in the text, or from memory | whether the route depends on where the fact sits or on what the model knows |
| X4 (9B): the locker key written word for word, translated, or described | whether the lookup's route works only for exact word matches |
| X0b: 7 topics, 3 formats, numbers as digits and as words | whether the 27B result holds beyond one simple scene type |

## More

- [Detailed results](docs/x0_details.md): every layer, every dictionary and number of atoms, subsets, controls, simple explanations we ruled out.
- [Pre-registration and every change made after the data](jobs/c3/X0.md) · [Dan's predictions and scores](predictions/2026-10-24_dan.md).
- [Earlier claims and history](CHANGELOG.md) · [Zach's breadth results](https://github.com/zach-perlman/bridge-jspace/tree/zach/v8-breadth-1021).

Prior work: the workspace paper (Gurnee et al. 2026); two-hop recall resolves its bridge early (Biran et al. 2024).
