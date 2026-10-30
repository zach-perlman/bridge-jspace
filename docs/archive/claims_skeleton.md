# Claims and evidence: skeleton (draft, 2026-10-26 evening; for Zach and Dan to edit and lock on day 9)

Bullets, not prose. Every number is in docs/depth/digest.md (generated from results/ by scripts/results_digest.py) unless a
line names an EXPERIMENTS.md entry. Figures: figures/archive/writeup/fig1-5 (scripts/fig_writeup.py, same readers as the digest).
Greedy accuracy unless "by probability". Intervals: 95% bootstrap over bridges (seed 0). No LLM-judge numbers anywhere.

## Setup (one paragraph in the write-up)

- Two-hop questions over a short passage. The model works out a bridge entity, then gives an attribute of it.
- **Memory final (M):** the passage never states the attribute, so it must be recalled. **Stated-fact final (K):** the
  passage states it. Same bridges, same questions.
- 8 relations; test set disjoint from dev; three data renderings for the three headline models.
- **Intervention:** at every token, project out the top-10 directions the J++ lens reads at that position, across one
  band of layers per model. The band is fixed on dev before the test run (fig 5).
- **M − K** = recall answers lost minus stated-fact answers lost, over items right unedited.
- **Controls:**
  - the same directions randomly rotated;
  - the logit lens's top 10;
  - a same-norm removal along the top principal directions (size-matched variance);
  - answer probability instead of greedy accuracy.

## Claim 1: recall needs J-space at mid depth; reading a stated fact does not (3 models, 2 families)

| | Qwen 27B (L32-40) | Qwen 9B (L12-16) | Nemotron Lightning (L27-33) |
|---|---|---|---|
| M − K | +51 [46, 55], n 892 | +43 [37, 49], n 563 | +53 [48, 59], n 563 |
| Stated facts lost | 2.6 | 5.0 | 3.7 |
| Rotated / logit lens | +3 / +2 | +2 / +1 | +4 / +9 |
| Size-matched variance | +12 | +7 | +8 |
| By probability | +50 | +35 | +44 |
| Two more renderings | +49, +50 | +42, +43 | +49, +50 |

- **Clean-checkout reruns:** the 27B and 9B headlines reproduce row for row (EXPERIMENTS: h200mon0-1026-0340,
  h200rerun0-1025-0445). Lightning has not had one (its 3 renderings are the replication).
- **Independent recompute:** a few lines over rows.jsonl give +50.9 (27B) and +53.1 (Lightning) (docs/breadth/verify_kit.md).
- **Natural passages** (natplus, 10/23): 27B and 9B gaps of roughly 40-50, J-specific. CHECK which EXPERIMENTS lines
  supersede which before quoting a number.
- **Attacks tried:**
  - direction-specific (rotated, logit lens);
  - not just "remove a lot of variance" (size-matched: 0.15-0.24 of the effect);
  - not a scoring artifact (probability, independent recompute);
  - not one data draw (renderings) or one checkout (clean reruns);
  - not countries only (all 8 relations; the dev profiles were redone on all relations after we found they were
    countries-only).
- **Open:**
  - The removal also costs plain-text loss. Lightning's gate: +1.67 nats over L17-35 vs +0.30 rotated. It is a big
    edit, yet stated facts survive it.
  - The band is chosen per model. Fig 5 shows the whole depth profile, so readers see the choice.

## Claim 2: what J-space carries at the mention is a context-free pointer to the entity; the fact is looked up later

| | Qwen 27B | Qwen 9B | Lightning |
|---|---|---|---|
| J-part swap (same passage) | +64 [58, 70] | +64 [58, 70] | +46 [40, 52] |
| From one neutral sentence about D | +70 (1.09) | +70 (1.10) | +46 (1.01) |
| Relations holding >= 2/3 | 8 of 8 | 8 of 8 | 7 of 7 read |
| Cross-relation / same-relation donor | 0.99 | 0.99 | 0.98 |
| Without own-word rows (share) | 0.84 | 0.83 | 0.62 (mixed) |
| Probe subspace swap vs J++ swap, same items | +8 vs +75 | +6 vs +80 | +2 vs +62 |
| Probe readout (J++ / probe, above chance) | 0.91 | 1.21 | 1.11 |
| X's answer first >= 50% at the answer position | L50 | L23 | L32 |

- **Plain reading:** the J-part at the mention says "this is France", not "France's continent is Europe" and not "this
  is the country being asked about":
  - a J-part from an unrelated one-sentence mention works as well as one from the passage;
  - a J-part from a passage about a different relation works too;
  - the attribute appears at the answer position after the band (fig 4): 7-10 layers past it in the Qwens, at the band's
    end in Lightning (L30-32).
- **Probes read but don't carry:**
  - a supervised probe decodes the attribute at the mention about as well as J++;
  - swapping the probe's subspace barely moves the answer.
  - Readability is not use.
- **Paste is not a ceiling:** in the band's swap run (PM), the J-part swap beats pasting the whole residual (27B +66 vs
  +59, 9B +69 vs +45, Lightning +46 vs +13). Paste also overwrites binding and position information; the J-part swap
  leaves the rest of the residual in place.
- **Rotated and logit-lens swaps:** within 1 point of 0 everywhere.
- **Open:**
  - Lightning's pointer is more name-like (0.62).
  - Lightning's swapped attribute plateaus below half at the answer position (fig 4).
  - No pointer tests yet for Bolt at K = 100 (optional, day 9).

## Claim 3: across models it is graded, and fixed-K comparisons mislead

| Model | K = 10 M − K | What more directions show | Reading |
|---|---|---|---|
| Nemotron Bolt (L42-53) | +6 | top 10 removes 6% of the residual (others 13-20%); K 30 / 100: +14 / +31 (rotated +1 / +7); swap +3 / +10 / +41 vs paste +20 | J-space, spread over ~100 directions; weaker than Lightning at matched size (+31 at 18% vs +53 at 18%) |
| DeepSeek V4 Flash (L18-23) | +18 | dose still rising at K 30 on dev; swap +12 vs paste +20 at mid depth | weak |
| Ministral 14B (L32-37) | +23 | top 10 already removes 20%; knock-out K 30 / 100: +24 / +19 (rotated +1, logit lens +3); mid-depth swap +3 / +4 / +5 vs paste +10, comp +8 | late, moderate, not under-dosed; at mid depth the identity is mostly outside even the J++ top 100 (swap partial by amendment 53 note 1) |
| OLMo-3 32B base | +5 | swap +41 vs paste +52 | readable and carried, not needed |
| Muse 30B (L36-42) | +60 | logit lens +35 | mostly shared with the logit lens |
| Qwen 122B (L39-45) | +48 | by probability +2 | not interpretable (probability collapse) |
| Gemma 4, gpt-oss | - | any removal breaks them | untestable |

- **Methods lessons:**
  - Report removal size, not just K.
  - Paste isn't a ceiling.
  - Check that dev profiles cover all relations.
  - Readable (lens or probe) ≠ carried (swap) ≠ needed (knock-out); the three come apart in OLMo, Ministral and Bolt.

## What we are not claiming

- That this is "the" workspace, or that J-space is necessary for all recall.
- Anything about Gemma 4, gpt-oss, or the 122B.
- That the pointer is J-space-only in Bolt / DeepSeek / Ministral.

## To decide (Zach, Dan)

1. Is claim 3 a claim, or a section on limits?
2. Dan's half: where does it join (mechanism of the lookup after the pointer)?
3. Which 4-5 figures go in; fig 1 / 2 / 4 are the spine.
