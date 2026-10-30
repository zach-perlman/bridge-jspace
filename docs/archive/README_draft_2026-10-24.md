# bridge-jspace

**Question.** When a model answers a two-step question, it first finds an entity in between (the **bridge**) and then uses it. A lens called **J++** reads hidden states as words. Does the model use the bridge in that word-like form, or does it get it some other way? And does the answer depend on what the model does with the bridge next?

> **Example.** "Iris picked the frog. The locker of the frog is 5. …" The bridge is *frog*.
> - **Lookup:** "Which locker belongs to Iris's pick?" The answer is written in the prompt.
> - **Recall:** "How many legs does Iris's pick have?" The answer comes from the model's memory.

**Status (24 Oct 2026).**
- Models: Qwen3.5-9B and Qwen3.6-27B. Qwen3.5-122B is running.
- All numbers are unverified (not yet hand-checked).
- Full log: [jobs/c3/X0.md](jobs/c3/X0.md).

## Main findings

1. **Recall needs the bridge's J++ form.**
   - Removing the J++ part of a bridge change costs recalls about half to three quarters of their answer flips, on both models.
   - A random part of the same size costs almost nothing.
2. **It is specific to J++.** At the same size, the logit-lens directions, the input embeddings and random directions do nothing comparable.
3. **Lookups need the J++ form much less, and the two models differ.**
   - **9B:** the lookup does not need it at all, at any number of J++ atoms. The pre-registered test passed.
   - **27B:** the lookup needs it a little at 25 atoms, so the pre-registered test did not pass. With 100 atoms it needs it about as much as recall does.
4. **Open lead.** Lookups flip mostly when the locker sentence comes *before* the pick sentence. The lookup may read a locker number that is already attached to the bridge word. Our J++ dictionary has no digit tokens, so this is being checked now.

![Recall needs the J++ form; lookup much less](figures/archive/status_2026-10-24/f1_readers.png)

## How we test it

- **Change the bridge.** Make a copy of the prompt where Iris picks a different animal (frog → tick). At one layer, take the difference between the two hidden states at the bridge word.
- **Paste the change back in three ways:**
  - whole;
  - without its J++ part (the 25 J++ directions that best describe it);
  - without a random part of the same size.
- **Ask both questions on the same patched prompt.** The question comes after the patch, so both readers get the exact same edit. Any difference comes from the reader, not the edit.
- **Measure** how many answers flip to the new animal's answer. The key number is the **extra loss**: flips lost without the J++ part, minus flips lost without the random part.
- **Fixed in advance:** the layer (9B layer 12, 27B layer 32), the rule, and Dan's predictions, all committed before any result was opened.

## Results at the pre-registered layer

| Model, layer | Lookup: extra loss | Recall: extra loss | Rule | Recall minus lookup |
|---|---|---|---|---|
| 9B, 12 | −0.03 [−0.08, 0.03] | 0.50 [0.41, 0.57] | **confirmed** | 0.53 [0.42, 0.61] |
| 27B, 32 | 0.14 [0.08, 0.20] | 0.74 [0.66, 0.80] | **not confirmed** | 0.60 [0.50, 0.69] |

How to read this:
- The rule asked for a lookup extra loss of at most 0.10 and a recall loss of at least 0.30.
- In answer counts (27B, 200 scenes): lookups go 86 → 71 without J++ and 86 → 83 without the random part; recalls go 150 → 35 and 150 → 146.
- 95% intervals come from resampling the 44 bridge entities.

![Where in depth](figures/archive/status_2026-10-24/f2_depth.png)

![It is J++, not any dictionary](figures/archive/status_2026-10-24/f3_dictionaries.png)

## What did not hold

- **"Past mid-depth, lookups don't use the J++ form at all."**
  - Holds on the 9B.
  - On the 27B, holds only when the change is pasted across the whole context (lookups 84% → 87% without J++, recalls 77% → 36%), not at the bridge word alone.
- **Prompts without the chat template.** Can't test: the models open a thinking block or answer in markdown. This says nothing about the question.

## Weak spots we know about

| Weak spot | Status |
|---|---|
| The J++ dictionary has no digit tokens; lookups may read a digit at the bridge word | checking now |
| Lookup flips depend on sentence order: locker before pick 76–86%, after 9–19% | figure F4; next experiments fix the order |
| The counterfactual changes two picks, not one (adds ~0.08 to the 27B lookup) | a single-change version is next |
| On the 27B, the lookup's drop with depth follows how much of the change J++ captures | stated beside the depth figure |
| Two models from one family, generated scenes only | 122B running; diverse and natural-text sets planned |

![What moves lookups: sentence order](figures/archive/status_2026-10-24/f4_order.png)

## Next

| Step | What it tells us |
|---|---|
| Digit check: add digit tokens to the J++ dictionary | whether the lookup's "other route" is just a digit we didn't look at |
| Qwen3.5-122B on the same test | whether the contrast changes with model size |
| Counterfactual with one change | whether the 27B result comes from how we built the edit |
| X2' (9B): the final fact made up in the text, true in the text, or from memory | whether the route depends on where the fact sits or on what the model knows |
| X4 (9B): the locker key written word for word, translated, or described | whether the lookup's route works only for exact word matches |
| X0b: 7 topics, 3 formats, numbers as digits and as words | whether the 27B result holds beyond one simple scene type |

## More

- [Detailed results](docs/depth/x0_details.md): every layer, every dictionary and number of atoms, subsets, controls, simple explanations we ruled out.
- [Pre-registration and every change made after the data](jobs/c3/X0.md).
- [Predictions and scores](predictions/2026-10-24_dan.md), scored question by question.
- [Earlier claims and history](CHANGELOG.md) · [Zach's breadth results](https://github.com/zach-perlman/bridge-jspace/tree/zach/v8-breadth-1021).

Prior work: the workspace paper (Gurnee et al. 2026); two-hop recall resolves its bridge early (Biran et al. 2024).
