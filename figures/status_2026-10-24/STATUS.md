# Status, 24 Oct 2026: X0 (does the lookup let go of the bridge's J++ form?)

The X0 test was pre-registered: the layers, the rule and Dan's predictions were fixed before any result was opened. Its verdicts are 9B **confirmed** and 27B **not confirmed**. Everything here is unverified. Every number comes from `data.csv` beside the figures (made by `scripts/x0_status_pack.py`). The detailed figures are in [figures/x0_necessity/](../x0_necessity/) and the design is in [jobs/c3/X0.md](../../jobs/c3/X0.md).

**Setup.** One edit changes the bridge (for example frog → tick) at the bridge's word, at one layer. A lookup ("Which locker belongs to Iris's pick?") and a recall ("How many legs does Iris's pick have?") read the same patched prompt. We count how many answer flips are lost when the edit's J++-readable part is removed, against a random part of the same size.

## F1. Recall needs the J++ form; lookup much less

![F1](f1_readers.png)

- At the pre-registered layers, removing the J++ part costs recalls 52.5 points (9B) and 57.5 points (27B) of all items. A random part of the same size costs them 3.5 and 2.0.
- Lookups lose 11.5 (9B) and 7.5 (27B); the random part takes 13.0 and 1.5. On the 9B the J++ part is no worse than a random part of its size.
- The graded contrast (recall minus lookup extra loss) is 0.53 [0.42, 0.61] on the 9B and 0.60 [0.50, 0.69] on the 27B. By the rule fixed in advance, the 9B is confirmed and the 27B is not confirmed, because its lookup extra loss is 0.14.

## F2. Where in depth

![F2](f2_depth.png)

- Recall keeps needing the J++ form at every valid depth on both models.
- The lookup's need falls with depth. It reaches the random band at 9B layer 12 and stays slightly above it on the 27B.
- Caveat: on the 27B, the lookup's profile across layers tracks the share of the change J++ takes (Spearman 0.79). Part of its depth profile may be size, not reader.

## F3. It is J++, not any dictionary; the 27B lookup needs more J++ atoms

![F3](f3_dictionaries.png)

- The logit lens's directions, the input embeddings and random atoms cost neither reader more than a random subspace of the same size, at any share tested.
- Recall depends on the leading J++ atoms (extra loss 0.77 on the 27B and 0.50 on the 9B at 25 atoms).
- The 27B lookup depends on further J++ atoms: its extra loss is 0.12 at 25 atoms and 0.60 at 100, close to the recall's 0.67. The 9B lookup does not depend on J++ at any k (−0.08 at 100).

## F4. What moves lookups: sentence order

![F4](f4_order.png)

- The edit at the bridge's word flips a lookup mostly when the locker sentence comes before the pick sentence: 86% vs 19% on the 9B, 76% vs 9% on the 27B.
- This was found after the data. The X0 lookup cells are therefore carried by the locker-before items.
- Open hypothesis (Dan): there, the lookup may read the answer digit, already bound at the bridge's word. The J++ dictionary has letter-bearing tokens only, so it cannot remove a digit.

## Next

- **Digit check** (running): J++ with digit tokens included, the digit directions alone, and the J++ readout of the answer digits, split by locker before / after. It decides whether X0's lookup result is a dictionary artefact.
- **Qwen3.5-122B** (today): weights downloaded, then a hardware gate, then X0 at layers 30 / 33 / 36 (predicted 33) with the k-curve, the digit arm and the strata. Caveats: a bf16 J++ on FP8 weights, MoE, 2x H100.
- **Single-change alt**: only the asked person's pick changes, to separate the upstream change that X0's alt carries.
- **X2' and X4 on the 9B (confirmatory)**: where the final fact sits, and whether "around" is a verbatim match. Both put the locker sentences before the picks. Specs and Dan's predictions come before the runs.
