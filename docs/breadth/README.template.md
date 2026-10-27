# Recall goes through the lens: what a model needs from the bridge's mention, across models

*When a model answers a two-step question about an entity, does it need the directions the J++ lens reads at that
entity, does that depend on whether the final fact is recalled or stated, and in which models?*

## In one minute

- **Recall needs a handful of lens-readable directions; reading the same fact does not.**
  - In Qwen3.6-27B, Qwen3.5-9B and Nemotron 3.5 Lightning (two families), we remove the top 10 J++ directions at one
    band.
  - Recall then loses {{a|ko.q27.mk}}, {{a|ko.q9.mk}} and {{a|ko.nl.mk}} points more than the same question with the
    fact stated.
  - This holds under controls fixed before the run.
- **At the entity's mention, those directions carry which entity it is, not its fact.** Taken from one neutral sentence
  about another entity, they move the answer as much as when taken from that entity's own passage. A probe that reads
  the fact there does not carry it.
- **Across models it is graded.**
  - Of nine models we could test, three show it strongly.
  - The rest are weak, need far more directions, carry it without needing it, share it with the logit lens, or lose it
    by probability.
  - Three more models cannot be tested: any lens removal breaks them.
- **For monitoring:** at the entity's mention the lens shows which entity the model will recall from, in every model.
  Whether the model depends on those directions is a separate, model-specific question.

**Status.** This is Zach's half (breadth): nine models on our dataset jsuite v2, plus the Qwens on every earlier dataset,
as of 27 Oct 2026. All numbers are unverified until hand-checked (Section 8). Built at {{head}} from the run files.

## Setup

- **The question.** "The composer who wrote The Magic Flute was of which nationality?" The bridge (Mozart) is:
  - read from the passage (**P**);
  - tracked through it (**T**);
  - or described, and so recalled (**M**).
- **The two finals.** The final fact is either **stated** in the passage (**K**: "Mozart was Austrian by birth") or
  left to **memory** (**M**). Same question, same answer, same passage otherwise.
  - Controls: **P** (a new made-up fact is stated), **A** (the answer word appears once, on another entity), **N**
    (nothing stated, no lures).
- **Dataset.** jsuite v2: 8 relations; 179 bridge facts on test and a disjoint 171 on dev (dev is used only to choose
  bands); 15 start × final words; 5,370 test items. An item counts only if the model gets every part of it right
  unedited.
- **The knock-out.** At every token, at each layer of one mid-depth band, project out the 10 directions the J++ lens
  reads most there.
  - **M − K**: recall answers lost minus stated-fact answers lost, in points.
- **Controls of the same size.**
  - The removal **rotated** to a random direction.
  - The **logit lens**'s own top 10.
  - The same norm along the residual's **top principal directions**.
- **The swap.** Replace the J-part (the span of the top-10 J++ directions) of the bridge's last token with another
  entity's (D).
  - **Transfer**: the share answering D's fact minus the share answering a third entity's.
- **Fixed in advance** = pre-registered in docs/prereg_replication_1022.md (amendments 1-55) before the run.
  **After the data** = chosen after seeing results. Brackets: 95% bootstrap over bridges.

## 1. Recall needs the J++ directions; reading the stated fact does not

*Fixed in advance (amendments 33, 39, 42, 48).*

Does removing what the lens reads cost recall more than reading?

- **Three models, two families.**
  - M − K is {{vci|ko.q27.mk}} (27B), {{vci|ko.q9.mk}} (9B) and {{vci|ko.nl.mk}} (Lightning).
  - Stated facts lose {{v|ko.q27.klost}}, {{v|ko.q9.klost}} and {{v|ko.nl.klost}} points.
- **It is specific to the lens's directions.**
  - Rotated: {{v|ko.q27.rot}} / {{v|ko.q9.rot}} / {{v|ko.nl.rot}}.
  - Logit lens: {{v|ko.q27.u}} / {{v|ko.q9.u}} / {{v|ko.nl.u}}.
  - The same norm along the residual's top principal directions costs {{v|ko.q27.pcr}}, {{v|ko.q9.pcr}} and
    {{v|ko.nl.pcr}} of the effect.
- **It is not a threshold effect.** Scored by the answer's probability, M − K is {{v|ko.q27.soft}} /
  {{v|ko.q9.soft}} / {{v|ko.nl.soft}}.
- **What is lost tracks where the answer is.** Points lost on the 27B, by final:

  | Final | Lost |
  |---|---|
  | Fact stated (K) | {{v|ko.q27.lostK}} |
  | New made-up fact stated (P) | {{v|ko.q27.lostP}} |
  | Answer word once, on another entity (A) | {{v|ko.q27.lostA}} |
  | Nothing stated, no lures (N) | {{v|ko.q27.lostN}} |
  | Recall (M) | {{v|ko.q27.lostM}} |

  Under the knock-out, the Qwens rarely name the bridge: {{v|gen.q27.PM.bridge}} and {{v|gen.q9.PM.bridge}} of replies.
  They still know which entity it is, but not its fact.
- **The other six models are in the grid (Section 6).** All six fail to show it cleanly:
  - DeepSeek and Ministral are weak ({{v|ko.ds.mk}}, {{v|ko.mi.mk}});
  - Bolt needs many more directions ({{v|ko.nb.mk}} at 10);
  - OLMo does not need it ({{v|ko.ol.mk}});
  - Muse shares more than half of it with the logit lens ({{v|ko.mu.u}} of {{v|ko.mu.mk}});
  - the 122B loses it by probability ({{v|ko.q122.soft}} vs {{v|ko.q122.mk}}).

## 2. It is not one dataset, relation, rendering or checkout

*Fixed in advance (amendments 6, 11, 14, 20, 23, 29, 33, 35, 38, 50, 55).*

Does the split survive everything we could vary?

- **Every dataset we built since day 1 (the two Qwens).** Each dataset has its own contrast: memory-final minus
  prompt-final words on the earlier sets, M − P on v1.

  | Dataset | 27B | 9B |
  |---|---|---|
  | Toy puzzles, data seeds 1 / 2 / 3 | {{v|toy.q27.s1}} / {{v|toy.q27.s2}} / {{v|toy.q27.s3}} | {{v|toy.q9.s1}} / {{v|toy.q9.s2}} / {{v|toy.q9.s3}} |
  | Natural fact chains, seeds 1 / 2 / 3 | {{v|nat.q27.s1}} / {{v|nat.q27.s2}} / {{v|nat.q27.s3}} | {{v|nat.q9.s1}} / {{v|nat.q9.s2}} / {{v|nat.q9.s3}} |
  | natplus | {{vci|natplus.q27}} | {{vci|natplus.q9}} |
  | jsuite v1 | {{vci|v1.q27}} | {{vci|v1.q9}} |

  The logit lens stays near zero wherever it was run:

  | Logit lens on | 27B | 9B |
  |---|---|---|
  | Toy puzzles | {{v|toy.q27.u}} | {{v|toy.q9.u}} |
  | Natural fact chains | {{v|nat.q27.u}} | {{v|nat.q9.u}} |
  | natplus | {{v|natplus.q27.u}} | {{v|natplus.q9.u}} |
  | jsuite v1 | {{v|v1.q27.u}} | {{v|v1.q9.u}} |
- **Every relation.**
  - On the 27B, M − K runs from {{v|ko.q27.rel.languages}} (languages) to {{v|ko.q27.rel.dishes}} (dishes).
  - Animals is the weakest everywhere (6 answers): 9B {{vci|ko.q9.rel.animals}}, Lightning {{vci|ko.nl.rel.animals}}.
- **Every start, both test halves, three renderings.**
  - Renderings: 27B {{v|ko.q27.r2}} and {{v|ko.q27.r3}}; 9B {{v|ko.q9.r2}} and {{v|ko.q9.r3}}; Lightning
    {{v|ko.nl.r2}} and {{v|ko.nl.r3}}.
  - A rendering redraws passages, distractors and wording over the same facts.
- **A clean checkout reproduces it.** Rerun from a fresh worktree:
  - the 27B's and 9B's knock-outs match row for row ({{v|clean.q27.diff}} of {{v|clean.q27.rows}} and
    {{v|clean.q9.diff}} of {{v|clean.q9.rows}} rows differ);
  - Lightning's headline reproduces ({{vci|clean.nl.mk_rerun}} vs {{vci|ko.nl.mk}}) but not row for row:
    {{v|clean.nl.diff}} of {{v|clean.nl.rows}} rows differ.
  - The likely cause, unverified, is numerics that depend on which prompts share a batch. Lightning's competence
    rerun covered more prompts, which shifted a few items' eligibility and batching.
- **It is not the bridge's own word (the plan's kill test).** Keeping the bridge's own-word directions restores only:

  | | Share restored |
  |---|---|
  | 27B (v2) | {{v|keepown.q27}} |
  | 9B (v2) | {{v|keepown.q9}} |
  | Lightning (v2) | {{v|keepown.nl}} |
  | Ministral (v2) | {{v|keepown.mi}} |
  | 27B (toy suite) | {{v|keepown.toy.q27}} |
  | 9B (toy suite) | {{v|keepown.toy.q9}} |

  The kill bar is 0.75.
- **Rare bridges lose as much as popular ones**, so Neel's narrow-concept prediction is not supported. natplus,
  popular vs rare: 27B {{v|natplus.q27.pop}} vs {{v|natplus.q27.rare}}; 9B {{v|natplus.q9.pop}} vs
  {{v|natplus.q9.rare}}.
- **It is mostly from pretraining.** The 9B base model gives {{v|v1.q9base.qa}} against the instruct model's
  {{v|v1.q9inst.qa}} (same Q&A format, same lens).
- **The lens matters.** On the 27B (v1), the plain J-lens finds {{v|v1.q27.jlens}} against J++'s {{v|v1.q27}}.
- **A bridge never named.** Deleting the bridge's one passing mention adds recall loss: {{vci|r.q27}} (27B),
  {{vci|r.q9}} (9B) and {{vci|r.nl}} (Lightning).

## 3. Where: at the bridge's mention at mid depth, in the question late

*Fixed in advance (amendments 30, 36, 37); Lightning's and Bolt's split in amendment 54.*

Where in the prompt must the removal act?

- **In the Qwens, a read bridge needs the directions at its own mention.**
  - Mention alone: {{v|pos.q27.P.bridge}} of {{v|pos.q27.P.all}} (27B) and {{v|pos.q9.P.bridge}} of
    {{v|pos.q9.P.all}} (9B).
  - Question alone: {{v|pos.q27.P.question}} and {{v|pos.q9.P.question}}.
- **Lightning needs them at both the mention and the question.** Mention {{v|pos.nl.P.bridge}} and question
  {{v|pos.nl.P.question}}, of {{v|pos.nl.P.all}}. Its lookup happens inside its band (Section 4); the Qwens' happens
  after theirs.
- **A recalled bridge needs them at several places at once.** No single region carries it: on the 27B, mention
  {{v|pos.q27.M.bridge}} and question {{v|pos.q27.M.question}}, of {{v|pos.q27.M.all}}.
- **Late in depth, the dependence moves to the question:**

  | Model (late band) | Question only | Mention only |
  |---|---|---|
  | 27B (L52-60) | {{v|pos.q27late.question}} | {{v|pos.q27late.bridge}} |
  | Ministral | {{v|pos.mi.question}} | {{v|pos.mi.bridge}} |
  | 122B | {{v|pos.q122.question}} | {{v|pos.q122.bridge}} |

## 4. What the directions carry at the mention: which entity it is

*Fixed in advance (amendments 32, 34, 38A, 47, 48, 51).*

If the mention's J-part is swapped for another entity's, does the answer follow, and what is being moved?

- **The answer follows a swapped J-part.**
  - Transfer: {{vci|swap.q27.swap}} (27B), {{vci|swap.q9.swap}} (9B), {{vci|swap.nl.swap}} (Lightning).
  - Rotated or logit-lens parts move nothing (27B: {{v|swap.q27.swap_rot}} and {{v|swap.q27.swap_u}}).
  - Pasting the whole residual moves less in Lightning ({{v|swap.nl.paste}}), because it also overwrites position and
    binding.
- **It is not just the answer token (Neel's linear answer swap).**
  - Without D's answer direction, the swap is unchanged: {{v|ans.q27.swap_noans}} vs {{v|ans.q27.swap}} (27B) and
    {{v|ans.q9.swap_noans}} vs {{v|ans.q9.swap}} (9B), on the PM final.
  - The answer direction alone moves {{v|ans.q27.swap_ans}}.
- **It is a pointer, whatever context it came from.**
  - From one neutral sentence about D ("A reader asked a question about D in the letters page"), the J-part moves the
    answer {{v|ptr.q27.neutral}}, {{v|ptr.q9.neutral}} and {{v|ptr.nl.neutral}} times as much as from D's own passage.
    It holds on {{v|ptr.q27.rel_held}} of {{v|ptr.q27.rel_read}} relations on the 27B.
  - From a passage on another relation it moves {{v|xrel.q27}} / {{v|xrel.q9}} / {{v|xrel.nl}} as much.
- **It is more than the name.** Without the entity's own-word directions, the swap keeps {{v|ptr.q27.noown}} /
  {{v|ptr.q9.noown}} / {{v|ptr.nl.noown}}. Lightning's pointer is the most name-like.
- **Decodable is not carried.** A supervised probe reads the fact at the mention about as well as J++. Swapping the
  probe's subspace moves {{v|probe.q27.probe}} / {{v|probe.q9.probe}} / {{v|probe.nl.probe}}, against J++'s
  {{v|probe.q27.swap}} / {{v|probe.q9.swap}} / {{v|probe.nl.swap}}.
- **The fact is looked up later.** At the answer position, the lens first reads X's fact on half the items at:
  - layer {{v|ptr.q27.lookup}} on the 27B (band ends at L40);
  - layer {{v|ptr.q9.lookup}} on the 9B (L16);
  - layer {{v|ptr.nl.lookup}} on Lightning (L33).
  For a swapped entity it reads D's fact at the same layers.
- **Readable, carried and needed come apart.**
  - OLMo carries the entity (swap {{v|swap.ol.swap}}), but the knock-out costs only {{v|ko.ol.mk}}.
  - Ministral's lens reads the fact at mid depth, but its J-part carries only {{v|swap.mi.mid.swap}}, and
    {{v|swap.mi.mid.k100.swap}} with 100 directions.

## 5. How much J-space

*Fixed in advance (amendments 52-55); the excess and probability readings after Lightning's grid, before the others
(amendment 54 note 1).*

How many directions does the dependence need, and when does the removal stop being specific?

- **In three of four models, most of the J-specific part is there in the first few directions; the 27B needs about
  30.** M − K at 1, 10 and 100 directions:

  | Model | 1 | 10 | 100 |
  |---|---|---|---|
  | 27B | {{v|dose.q27.k1}} | {{v|dose.q27.k10}} | {{v|dose.q27.k100}} |
  | 9B | {{v|dose.q9.k1}} | {{v|dose.q9.k10}} | {{v|dose.q9.k100}} |
  | Lightning | {{v|dose.nl.k1}} | {{v|dose.nl.k10}} | {{v|dose.nl.k100}} |
  | Ministral | {{v|dose.mi.k1}} | {{v|dose.mi.k10}} | {{v|dose.mi.k100}} |

  The 27B keeps rising to 30 directions ({{v|dose.q27.k30}}).
- **More directions add damage that is not specific.** Greedy answers hide it: the stated answer usually stays on top
  while losing much of its probability.
  - Lightning: stated facts lose {{a|dose.nl.k100.K}} points by greedy answer at 100 directions, but
    {{a|dose.nl.k100.sK}} by probability.
  - The plateau rule as pre-registered calls Lightning distributed (K\* {{v|dose.nl.kstar}}). On the J-specific excess
    it is concentrated (K\* {{v|dose.nl.ekstar}}).
- **Bolt is the exception:** its effect is spread over about 100 directions.
  - M − K is {{v|dose.nb.k10}} at 10 and {{v|dose.nb.k100}} at 100.
  - Bolt's 100 directions remove {{v|dose.nb.k100.share}} of the residual. Lightning's top 10 remove about the same
    ({{v|dose.nl.k10.share}}) and give {{v|dose.nl.k10}}.
- **Swapping more directions.**
  - The 9B's swap grows: {{v|swapk.q9.k10}} → {{v|swapk.q9.k100}}.
  - Lightning's is saturated: {{v|swapk.nl.k10}} → {{v|swapk.nl.k100}}.
  - Bolt's carries only at 100: {{v|swapk.nb.k10}} → {{v|swapk.nb.k100}}.
  - Ministral's never carries (at mid depth, L20-25): {{v|swapk.mi.k10}} → {{v|swapk.mi.k100}}.

## 6. Every model, every test

{{grid}}

Untestable: removing the top 10 lens directions adds more plain text loss than the 2-nat bar:

| Model | Plain-text loss added |
|---|---|
| Gemma 4 31B-it | {{v|text.gemma}} |
| gpt-oss-20b | {{v|text.gptoss}} |
| Kolibri-1 | {{v|text.kol}} |

Three more models stopped on the earlier datasets, below the 30-point bar:

| Model | Earlier datasets |
|---|---|
| Qwen3-32B | {{v|old.q32.qwen3_32b_full2_ko_v1}} and {{v|old.q32.qwen3_32b_fresh2_ko_v1}} |
| Olmo-Hybrid 7B | {{v|old.oh7.olmoh7_big2_ko_v1}} |
| Olmo-3 7B | {{v|old.o7.olmo3d7_big2_ko_v1}} |

## 7. What did not hold

- **Failed when fixed in advance.**
  - The 9B's second toy data seed: {{v|toy.q9.s2}}, below the 30-point bar; pooled over seeds it passed.
  - The steering test (the plan's second claim, C2): most cells broke more than 10% of answers, and it was withdrawn on
    the 24 Oct re-score. The swap replaced it as the sufficiency test.
  - The 27B with the plain J-lens: {{v|v1.q27.jlens}}, below 30.
  - The never-named bridge, predicted to cost nothing extra: it costs the 27B {{v|r.q27}} and the 9B {{v|r.q9}}.
  - The 122B by probability ({{v|ko.q122.soft}}). Muse's share with the logit lens. Bolt at 10 directions. OLMo.
- **Design errors.**
  - **A fixed number of directions is not a fixed dose.** The top 10 remove 6% of the residual in Bolt and 13-20%
    elsewhere.
  - **The dose plateau rule (amendment 54) judged specificity by greedy answers**, which hide the stated facts' lost
    probability; note 1 adds the excess and probability readings.
  - **The dev depth profiles first covered countries only.** Redone on all relations, the bands held.
- **Limits.**
  - Templated passages over one fact set per dataset; English only.
  - One band per model.
  - Greedy answers with thinking off.
  - The Qwens use published J++ lenses; the Nemotrons, Ministral and Muse use our own fits.
  - The removal also costs plain text: {{v|text.q27}} (27B) to {{v|text.nl}} (Lightning).
  - One bootstrap seed.
  - The 122B in FP8.
  - The dose and swap-dose runs use 150 random items per word.

## 8. How we checked

- **Hand-checked numbers.** None yet; docs/verify_kit.md recomputes the headline M − K from the per-item rows and lists
  20 random items per model.
- **Clean-checkout reruns**: row-identical for the 27B and 9B; Lightning reproduces its headline, not row for row
  (Section 2).
- **Pre-registration**: docs/prereg_replication_1022.md, amendments 1-55. EXPERIMENTS.md has one line per run, with
  its W&B link.

## 9. Next

- DeepSeek and OLMo at matched removal size (their caches must come back).
- H0 head-on on v2: computed bridges, and the three-hop and numbers modules on v2 and on Lightning.
- Late-band positions for the 9B and Lightning.
- Lightning on the natural datasets (running).
- Bolt's pointer at 100 directions (running).
- Hand-checking.

## Appendix. Links

Every number on this page comes from [docs/breadth/data.csv](data.csv), each row with its source file;
scripts/report_breadth.py builds it and this page.
