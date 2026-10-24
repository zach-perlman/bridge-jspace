<!-- grid: results/cross_model/20261023T210238Z -->
# bridge-jspace

**The question.** A two-step question makes a model find an entity in between, the **bridge**, and then use it. A **J-lens** reads hidden states as words; the **J-space** is the part of a hidden state it reads (Gurnee et al. 2026; we use its refit, **J++**). Does the model use the bridge in the form the lens reads, or by another route?

> "Iris picked the frog. The locker of the frog is 5. ..." The bridge is *frog*. A **lookup** ("Which locker belongs to Iris's pick?") takes the answer from a sentence in the prompt; a **recall** ("How many legs does Iris's pick have?") takes it from memory.

> **Status, 24 Oct 2026, evening.** Built at {{head}} from the X0 run files. This page is the first experiment of the direction, X0 (pre-registered 24 Oct; [jobs/c3/X0.md](jobs/c3/X0.md)), and the plan it led to. Numbers are quoted from the run files (linked). Exploration phase: nothing here is hand-verified (UNVERIFIED). Models: Qwen3.6-27B and Qwen3.5-9B, hybrids with DeltaNet layers. The earlier claims (the late read, order then identity) are in [CHANGELOG.md](CHANGELOG.md).

## TL;DR

- **Recalls need the J-space form more than lookups do.** Remove the J++-readable part of an edit of the bridge, at a depth fixed in advance. Recalls lose most of their switches; lookups lose little more than to a random part of the same size. The graded contrast is {{q|0.60 [0.50, 0.69]}} on the 27B and {{q|0.53 [0.42, 0.61]}} on the 9B.
- **It is about J++.** The logit lens's directions (W_U), the input embeddings (W_E) and random atoms do nothing comparable, also at a similar removed share.
- **The categorical version is model-dependent.** "Lookups do not use the J-form" is confirmed on the 9B (layer {{q|12}}) and not confirmed on the 27B (layer {{q|32}}): there the lookup depends on further J++ atoms (weak spots).
- **Next**: what the lookup uses instead, and what decides the route (X2', X4, X1, X3), as graded reader comparisons.

![X0: lookup and recall excess by layer, two models, three renderings](figures/x0_necessity/overview.png)

## The experiment: X0

**What we did.**
- **Scenes.** Fresh scenes ({{q|600}}, seed {{q|24}}, never read by a model before), one question per reader.
- **The edit.** The asked person's pick is changed (frog → tick), and the change Δ = h_alt − h_org is pasted at the bridge's word at one layer. It goes in three ways: whole; without its J++ part (25 atoms, signed OMP); or without a random part of the same share of ‖Δ‖².
- **Readers.** The lookup and the recall read the identical patched prompt, because the question comes after the patch. A difference is therefore in what the reader uses, not in the edit.
- **Measures.**
  - J-dependence = the share of switches lost without the part.
  - Excess = J-dependence − the random part's dependence.
  - Graded contrast C = recall excess − lookup excess (paired).
- **Pre-registration.** The rule and the layers (27B {{q|32}}, 9B {{q|12}}) were fixed before the run. Dan's predictions were committed before any result was opened.

**Key numbers** (n = {{q|200}} scenes per cell, CIs over {{q|44}} bridge entities). Sources: [27B verdict](results/x0_necessity/x0_necessity_27b_chat/verdict-20261024T135446Z/verdict.md), [9B verdict](results/x0_necessity/qwen35_9b_x0_necessity/verdict-20261024T135419Z/verdict.md), [27B tables](results/x0_necessity/x0_necessity_27b_chat/descriptive-20261024T135952Z/tables.md), [9B tables](results/x0_necessity/qwen35_9b_x0_necessity/descriptive-20261024T135953Z/tables.md).

| Model, layer | Lookup excess (label) | Recall J-dependence (label) | Rule | Contrast C |
|---|---|---|---|---|
| 27B, {{q|32}} | {{q|0.14 [0.08, 0.20]}} (mixed) | {{q|0.77 [0.67, 0.84]}} (through) | **not confirmed** | {{q|0.60 [0.50, 0.69]}} |
| 9B, {{q|12}} | {{q|−0.03 [−0.08, 0.03]}} (around) | {{q|0.53 [0.45, 0.61]}} (through) | **confirmed** | {{q|0.53 [0.42, 0.61]}} |

- **In switches** (27B, layer 32):
  - removing J++ takes lookups from {{q|86 to 71}} of 200 and recalls from {{q|150 to 35}};
  - removing the random part takes them to {{q|83}} and {{q|146}}.
- **Specific to J++.**
  - At 25 atoms, W_U, W_E and random atoms leave both readers "around" at every layer (27B excess within {{q|±0.03}}).
  - At equal removed shares (27B layer 32, 25 to 200 atoms of each dictionary; [tables](results/x0_necessity/x0_kmatch_27b/descriptive-20261024T142650Z/tables.md)), at about a quarter of ‖Δ‖² the costs to lookups / recalls are:
    - J++ (100 atoms, share {{q|0.305}}): {{q|0.72}} / {{q|0.95}};
    - W_E (share {{q|0.264}}): {{q|0.05}} / {{q|0.07}};
    - random atoms (share {{q|0.264}}): {{q|0.06}} / {{q|0.01}}.
  - At about {{q|0.4}} every dictionary costs both readers (W_E {{q|0.67}} / {{q|0.52}}), but only J++ costs more than a random subspace of the same share (excess {{q|0.58}} / {{q|0.50}}; the others ≤ {{q|0.12}}).
  - A rerun on recomputed items reproduces layer 32 (lookup excess {{q|0.12}}, recall {{q|0.77}}).
  - On the 9B (layer 12, about a third of ‖Δ‖²; [tables](results/x0_necessity/qwen35_9b_x0_kmatch/descriptive-20261024T143539Z/tables.md)), the costs to lookups / recalls are:
    - J++ (50 atoms, share {{q|0.329}}): {{q|0.31}} / {{q|0.74}};
    - W_E (share {{q|0.329}}): {{q|0.34}} / {{q|0.09}};
    - random atoms (share {{q|0.323}}): {{q|0.38}} / {{q|0.07}}.
  - So on the 9B, the lookup's cost does not depend on the dictionary and the recall's is J++-specific. On the 27B both are J++-specific, the lookup's less.
- **The split** (lookup "around" and recall "through" at the same layer): 27B layer {{q|30}}; 9B layers {{q|12-14}}. On the 27B the lookup's decline with depth tracks the share of ‖Δ‖² that J++ takes (Spearman {{q|0.79}}; weak spots).
- **Replication of the 23 Oct cell; not part of X0's rule.** 27B layer 32: with the change at every context position, lookups lose nothing without the J++ part ({{q|84% → 87%}}) and recalls lose {{q|41}} points (random {{q|−1}}); this replicates 23 Oct on fresh scenes (n = {{q|180}}; [verdict](results/d1_verdict/x0_ctx_parts_27b_20261024-144050/verdict.md)). At the bridge's word alone (the pre-registered X0 test) the lookup depends on J++ moderately (excess {{q|0.14}}) and the rule is not met.

![Equal removed share](figures/x0_necessity/kmatch.png)

![Excess against the number of atoms](figures/x0_necessity/kcurve.png)

**Controls**
- A random part at each dictionary's own share.
- The random dictionary's own fit.
- Both readers on the identical patch.
- A valid cell needs the whole edit to switch at least {{q|30%}} and {{q|30}} items.
- A hardware gate reran a 23 Oct cell on the new box: {{q|0.99}} per-row agreement.

**Weak spots**
- **The atoms the readers depend on.** Recall depends on the leading J++ atoms. On the 27B the lookup depends on further J++ atoms, and at k = 100 the two readers depend on J++ about equally (excess {{q|0.60}} vs {{q|0.67}}). On the 9B the lookup does not depend on J++ at any k ({{q|−0.03}} at 50, {{q|−0.08}} at 100). A digit check is running: the J++ dictionary has letter-bearing tokens only, so digits are excluded.
- **Share tracks lookup dependence.** Across layers, the lookup's J-dependence tracks the share of ‖Δ‖² that J++ takes: 27B Pearson {{q|0.54}}, Spearman {{q|0.79}} over {{q|10}} valid layers. The recall's does not ({{q|0.03}}). On the 9B, share and depth fall together. Added after data ([figure](figures/x0_necessity/share.png)).
- **The whole edit fades for lookups** with depth (27B: {{q|0.89}} at layer 16, {{q|0.43}} at 32), not for recalls ({{q|0.98}}, {{q|0.75}}).
- **The alt changes a second pick.** At the 27B's layer 32 (added after data; [figure](figures/x0_necessity/asked_first.png)):
  - where the asked pick comes first (n = {{q|103}}), lookups switch {{q|24%}} ("can't tell"; excess {{q|0.08 [0.00, 0.20]}});
  - where the other changed pick comes first (n = {{q|97}}), they switch {{q|63% [53, 72]}} with excess {{q|0.16 [0.08, 0.27]}} (mixed);
  - recalls are the same in both (excess {{q|0.74}}). A single-change alt is next.
- **On the 9B, "around" means no J-specific cost, not no cost.** J++ and a random part of the same share each cost its lookups {{q|0.12-0.13}} of switches.
- **Without the chat template: can't test.** Post-trained models don't answer the bare QA format; this says nothing about the hypothesis.
  - **No chat template, thinking not disabled** (raw text): both models open a think block (gate {{q|0%}}).
  - **No chat template, thinking off** (the template's empty think block added by hand): they answer in markdown or in words (" **6**", " **Seven**"), so the first-token read is right on {{q|0% / 0%}} (9B) and {{q|63% / 90.5%}} (27B) of lookups / recalls.
  - A descriptive arm that reads the first digit is running (amendment 3).

<details><summary>Per-model detail figures and the 23 Oct reading that X0 tested</summary>

![27B detail](figures/x0_necessity/detail_x0_necessity_27b_chat_chat.png)
![9B detail](figures/x0_necessity/detail_qwen35_9b_x0_necessity_chat.png)

- **The 23 Oct reading was post hoc.** The split depth was read per layer after a pre-registered rule failed ([27B](results/d1_verdict/d1_necessity_parts_27b_r2_20261023-164424/verdict.md), [9B](results/d1_verdict/qwen35_9b_d1_necessity_parts_r2_20261023-162800/verdict.md)). Its 27B headline (lookups {{q|83% → 81%}}, recalls {{q|78% → 27%}} at layer 32) was every context position, not the bridge's word. On the fresh scenes that cell repeats ({{q|84% → 87%}}, {{q|77% → 36%}}; replication above).
- **Convergent evidence (Zach, quoted).** Knocking out the lens's top directions costs recall more points than lookups, on held-out bands chosen with lookups excluded.

</details>

## What X0 led to: what does the lookup use instead?

Each candidate for the lookup's route has one test. The rules are graded reader comparisons (D3 amendment, 24 Oct, after X0), committed to each spec before its run. The decisive read is X0's top-token switch (cand logged); X3 keeps cand2.
- **9B: confirmatory** (it passed X0). Order: X1, X2', X4, X3.
- **27B: exploratory** (D3 amendment). Order: X2', X4, X1, X3. X2' and X4 add a descriptive arm at the context positions (in X2' the shared prefix before the K / M block).

| Candidate | Test | Rule (fixed before the run) | Status |
|---|---|---|---|
| The bridge's input-token identity | X0's W_E dictionary | W_E lookup excess ≥ {{q|0.20}} | not supported: W_E is inert for both readers |
| Where the final fact sits, or whether the model knows it | X2': X0's generator and digit answers; the final fact made up in the passage (the lookup), true in the passage (K), or recalled (M) | r = (excess_K − excess_lookup) / (excess_M − excess_lookup): ≤ {{q|0.33}} where it sits, ≥ {{q|0.67}} what it knows; can't tell if the denominator < {{q|0.30}} | spec next |
| A verbatim-match shortcut | X4: the key stated verbatim, translated, or described | lookup excess, translated − verbatim: ≥ {{q|0.20}} verbatim, ≤ {{q|0.10}} not lexical; control: described − verbatim ≥ {{q|0.20}} | spec next |
| The J-form rebuilt downstream | X1: among lookups that still switch without J++ at layer 32, remove the rebuilt J++ part over layers 33-44 | share lost minus the random part's: ≥ {{q|0.20}} rebuilding matters, ≤ {{q|0.10}} it does not | 9B first |
| Generated lists only | X3: paired readers on natural passages (natplus) | C ≥ {{q|0.30}} with lower bound ≥ {{q|0.15}} holds; ≤ {{q|0.10}} fails | last (Zach has natural-text evidence); cand2 read |
| A scene-relative address (order label) | the slot subspace removed (23 Oct) | – | open: not necessary ({{q|98%}} of lookups kept) |

**Running or next** (descriptive, added after data): the first-digit read without the chat template, thinking off (27B, 9B); J++ atoms of 20 + 20 items at the 27B's layer 32; a single-change alt (27B layers 28-34, 9B 10-14).

## Boring explanations

| Explanation | Test | Result | Status |
|---|---|---|---|
| The J++ part is just small | A random part of the same share removed | Recalls lose {{q|0.03}} to it at the 27B's layer 32, {{q|0.77}} to J++ | checked |
| The edit differs between lookups and recalls | The identical patch at the bridge's word | By design | checked |
| Any token-aligned part would do | W_U, W_E and random atoms at 25 atoms; W_E at an equal share | All "around" at every layer; at equal shares only J++ costs the recall more than a random subspace (27B, 9B) | checked on the 27B and the 9B |
| The chat template | No chat template, with thinking not disabled / off | Can't test: post-trained models don't answer the bare QA format (a think block; markdown) | not a test of the hypothesis; first-digit read running |
| The alt's second changed pick | Asked-first vs upstream-change items | Recalls the same; 27B lookups switch {{q|24%}} vs {{q|63%}}, excess {{q|0.08}} vs {{q|0.16}} | partly checked; a single-change alt next |
| The lookup's layer profile is the J++ share | J-dependence against share across layers | 27B lookups track it (Spearman {{q|0.79}}); recalls do not | open |

## Choices made after seeing the data (24 Oct; log in [jobs/c3/X0.md](jobs/c3/X0.md))

| Choice | Why | What we did |
|---|---|---|
| X1-X4 run on the 27B although X0 did not confirm it (D3 amendment) | The categorical premise failed there, but the graded contrast is large and J++-specific | X1-X4 become reader comparisons at layer 32 under graded rules; the X0 verdict stays "not confirmed" |
| A "no chat template, thinking off" arm (amendment 2) | Without the template thinking is not disabled: raw prompts open a think block | Descriptive; it failed its gate too (markdown answers) |
| A first-digit read without the gate (amendment 3) | Answers start with " **" or a word | Descriptive, labeled; chat stays the verdict |
| X1-X4: confirmatory on the 9B, exploratory on the 27B; X2' on X0's generator, top-token read; a context-position arm on the 27B (Dan, ~17:00) | The 9B passed X0's gate; the 27B did not | Committed to each spec before its run |
| Descriptive tables and figures (the critic's requests) | To check share, absolute drops, the upstream change, equal shares | Labeled "added after data", outside the rule |

## Pre-registered tests and Dan's predictions

| Test | Rule fixed before the run | Verdict | Dan's prediction |
|---|---|---|---|
| X0, 27B at layer 32 | lookup excess ≤ {{q|0.10}} and recall J-dependence ≥ {{q|0.30}}; killed if excess ≥ {{q|0.20}} or recall < {{q|0.20}} | not confirmed | confirmed, {{q|80%}}: wrong |
| X0, 9B at layer 12 | the same | confirmed | confirmed, {{q|80%}}: right |
| The 27B's layer-32 cell is valid for both readers | the whole edit switches ≥ {{q|30%}} and ≥ {{q|30}} items | both valid (lookups {{q|43%}}) | only recalls, {{q|80%}}: wrong |
| W_E removal (H-token) | W_E lookup excess ≥ {{q|0.20}} with J++'s around | 9B: neither; 27B: not applicable (J++'s lookup mixed) | neither, {{q|90%}}: right / wrong |
| W_U removal | both readers around | both models | inert, {{q|90%}}: right |
| No chat template, thinking not disabled: gate | ≥ {{q|80%}} for both readers | can't test (bare QA format) | both pass, {{q|80%}}: wrong |
| No chat template, thinking off: gate (amendment 2) | the same | can't test (bare QA format) | both pass, {{q|80%}}: wrong |

Batch 25 is scored question by question in [predictions/2026-10-24_dan.md](predictions/2026-10-24_dan.md) (Brier and calibration from batch 25 on: [predictions/README.md](predictions/README.md)).

## Next steps

| Step | Decides | Cost |
|---|---|---|
| 9B, confirmatory: X1 (rebuilt J++ form over layers 13-24), X2', X4 | whether the lookup re-reads a rebuilt J-form; where the route is set; whether "around" is lexical | ~2 h data + ~2 GPU-h |
| 27B, exploratory: X2', X4 (with the context arm), then X1 (layers 33-44) | the same, on the model X0 did not confirm | ~3 GPU-h |
| X3: paired readers on natural passages | whether the contrast holds beyond generated lists | ~1.5 GPU-h |
| Hand check of the X0 cells at the predicted layers | the "verified" mark | 1 h, Dan |

<details><summary>Methods and words</summary>

| Word | Meaning |
|---|---|
| J++ | The refit J-lens used everywhere here (pinned per model, sha256 checked on load) |
| part | The 25-atom signed OMP fit of a change Δ over a dictionary's letter-token atoms |
| random part | Δ projected on a random subspace keeping the part's share of ‖Δ‖², per item |
| J-dependence | 1 − (switched without the part) / (switched by the whole edit) |
| excess | J-dependence − the random part's dependence |
| around / through / mixed | excess ≤ 0.10 (upper CI ≤ 0.20) / J-dependence ≥ 0.30 and excess ≥ 0.20 (lower CI ≥ 0.10) / the rest |
| can't tell | The whole edit switches < {{q|30%}} or < {{q|30}} items of a reader |
| graded contrast C | recall excess − lookup excess on the same items, paired bootstrap over entities |
| split | lookup around and recall through at the same layer |
| renderings | chat = chat template, thinking off (the run key `chat`); no chat template, thinking off = the template's empty think block added by hand, no roles, no instruction (key `nochat`); no chat template, thinking not disabled = raw text (key `raw`) |
| read | Chat: the top token after "Answer:" and a space is the alt answer's first token |

</details>

Prior work: the workspace paper (Gurnee et al. 2026); two-hop recall resolves its bridge early (Biran et al. 2024): [docs/prior_art.md](docs/prior_art.md).

## Links

[jobs/c3/X0.md](jobs/c3/X0.md) · [X0 runs](results/x0_necessity/) · [figures](figures/x0_necessity/) · [predictions](predictions/) · [CHANGELOG.md](CHANGELOG.md) · [STATUS.md](STATUS.md) · [prior work](docs/prior_art.md) · [VERIFIED.md](VERIFIED.md) · [DEVELOPER.md](DEVELOPER.md) · [HISTORY.md](HISTORY.md)
