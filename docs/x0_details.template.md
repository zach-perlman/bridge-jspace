# X0 in detail

The README gives the summary; this page holds the tables behind it. Every number is recomputed from the run files by `scripts/x0_details.py`, and every number is unverified. Design and log: [jobs/c3/X0.md](../jobs/c3/X0.md). Run folders: [results/x0_necessity/](../results/x0_necessity/).

**Terms.** "Excess" here is the README's "extra loss": the J-dependence (the share of the whole edit's flips lost when a part is removed) minus that of a random subspace of the same share of ‖Δ‖².

**Labels**, per reader and layer:
- around: excess ≤ 0.10, upper CI ≤ 0.20;
- through: J-dependence ≥ 0.30 and excess ≥ 0.20, lower CI ≥ 0.10;
- mixed: the rest;
- can't tell: the whole edit flips < 30% or < 30 items.

CIs are 95%, from a cluster bootstrap over bridge entities (10,000 resamples).

![Overview: excess by layer, two models, three prompt formats](../figures/x0_necessity/overview.png)

## Every layer (chat, the bridge's word, J++ at 25 atoms)

Qwen3.5-9B (n = {{num|n_9b}} scenes, {{num|ents_9b}} bridge entities; pre-registered layer {{num|layer_9b}}):

{{tbl|layers_9b}}

Qwen3.6-27B (n = {{num|n_27b}} scenes, {{num|ents_27b}} bridge entities; pre-registered layer {{num|layer_27b}}):

{{tbl|layers_27b}}

![27B detail](../figures/x0_necessity/detail_x0_necessity_27b_chat_chat.png)
![9B detail](../figures/x0_necessity/detail_qwen35_9b_x0_necessity_chat.png)

## Every dictionary and number of atoms (the pre-registered layer; added after the data)

Each dictionary's part is set against a random subspace of its own share. These come from the k-match runs, which recompute the X0 items.

Qwen3.5-9B, layer {{num|layer_9b}}:

{{tbl|dicts_9b}}

Qwen3.6-27B, layer {{num|layer_27b}}:

{{tbl|dicts_27b}}

![Equal removed share](../figures/x0_necessity/kmatch.png)
![Excess against the number of atoms](../figures/x0_necessity/kcurve.png)
![Share against J-dependence](../figures/x0_necessity/share.png)

On the 27B, the lookup's J-dependence tracks, across layers, the share of ‖Δ‖² that J++ takes (Spearman {{num|share_rho_27b}}). The recall's does not.

## Subsets (the pre-registered layer; added after the data)

- **Upstream change.** The alt swaps two people's picks. Where the other changed pick comes first, Δ at the asked word also carries that change. On the 27B:
  - with the upstream change (n = {{num|lk_n_up_27b}}), lookups flip {{num|lk_swhole_up_27b}}, excess {{num|lk_excess_up_27b}};
  - asked first (n = {{num|lk_n_af_27b}}), lookups flip {{num|lk_swhole_af_27b}}, excess {{num|lk_excess_af_27b}}, too few flips to measure.
- **Sentence order.** The whole edit flips lookups {{num|lk_order_before_9b}} vs {{num|lk_order_after_9b}} (9B) and {{num|lk_order_before_27b}} vs {{num|lk_order_after_27b}} (27B), with the locker sentence before vs after the pick sentence.

Qwen3.5-9B:

{{tbl|strata_9b}}

Qwen3.6-27B:

{{tbl|strata_27b}}

![Upstream change](../figures/x0_necessity/asked_first.png)

## The digit check (the pre-registered layer; added after the data)

The question: the J++ dictionary has letter-bearing tokens only. Does the lookup read the answer digit at the bridge's word, which no letter-only dictionary can remove?
- The pre-stated reading (Dan, before the run): if J++ over every token, or the 10 digit directions alone, makes the lookup "through" in locker-before items, X0's "around" was the excluded digit.
- The reference: letter-only J++ at the same number of atoms.
- Result: the digits change nothing. The J++ readout at the bridge's word ranks the lookup's answer digit first in {{num|dig_readout_first_before_9b}} (9B) and {{num|dig_readout_first_before_27b}} (27B) of locker-before items, against a chance of 10%.

Qwen3.5-9B, layer 12:

{{tbl|digit_9b}}

Qwen3.6-27B, layer 32:

{{tbl|digit_27b}}

![The digit check](../figures/status_2026-10-24/f6_digits.png)

## The J++ atoms of the bridge edit (27B, layer 32, 20 random items; added after the data)

- The first atom is the bridge's own token (before or after the edit) in {{num|atoms_first_bridge_letters}} items.
- The rest of the top 25 are mostly tokens that are neither context words nor names. Some of them are the bridge in other scripts (フライ for *fly*, 小熊 for *bear*).
- Digits never enter the top 25, even when every token is allowed ({{num|atoms_digit_top25_all}}). Number words enter {{num|atoms_number_word_top25_all}}.

Tables: [letter atoms](../results/x0_atoms/x0_atoms_27b_letters/tables.md), [every token](../results/x0_atoms/x0_atoms_27b_all/tables.md).

## The 23 Oct context cell on the fresh scenes (a replication; not part of X0's rule)

27B at layer 32, with the change at every context position, using the 23 Oct code, filter and read (n = {{num|ctx_n}} per reader):
- lookups flip {{num|ctx_lookup_full}} with the whole change and {{num|ctx_lookup_noj}} without the J++ part;
- recalls flip {{num|ctx_recall_full}} → {{num|ctx_recall_noj}}, a loss of {{num|ctx_recall_drop}} points, against {{num|ctx_recall_droprand}} for a random part. The difference is {{num|ctx_recall_diff}} (shares).

[Verdict](../results/d1_verdict/x0_ctx_parts_27b_20261024-144050/verdict.md).

## Controls

- A random part at each dictionary's own share of ‖Δ‖², per item.
- The random dictionary's own 25-atom fit.
- Both readers on the identical patch.
- The valid-cell bar: the whole edit flips at least 30% and 30 items.
- The competence gate: at least 80% unedited accuracy for both readers.
- A hardware gate reran a 23 Oct cell on the new box (0.99 per-row agreement).

## Simple explanations we checked

| Explanation | Test | Result | Status |
|---|---|---|---|
| The J++ part is just small | A random part of the same share removed | Recalls lose {{num|rc_rdep_27b}} to it at the 27B's layer 32, and {{num|rc_jdep_27b}} to J++ | checked |
| The edit differs between lookups and recalls | The identical patch at the bridge's word | By design | checked |
| Any token-aligned part would do | W_U, W_E and random atoms at 25-200 atoms | Only J++ costs the recall more than a random subspace of the same share | checked (27B, 9B) |
| The chat template | No chat template, with thinking not disabled or off | Can't test: the models open a think block or answer in markdown (first-token read right on {{num|nochat_gate_9b}} of 9B lookups / recalls, {{num|nochat_gate_27b}} on the 27B) | not a test of the hypothesis |
| The alt's second changed pick | Asked-first vs upstream-change items | Recalls the same; 27B lookups flip less without the upstream change | partly; a single-change alt is next |
| The lookup's layer profile is the J++ share | J-dependence against share across layers | 27B lookups track it; recalls do not | open |

## Choices made after the data (24 Oct; log in [jobs/c3/X0.md](../jobs/c3/X0.md))

| Choice | Why | What we did |
|---|---|---|
| X1-X4 run on the 27B although X0 did not confirm it (D3 amendment) | The graded contrast is large and specific to J++ | Reader comparisons at layer 32 under graded rules; the X0 verdict stays "not confirmed" |
| X1-X4 confirmatory on the 9B, exploratory on the 27B | The 9B passed X0's gate | Committed to each spec before its run |
| "No chat template, thinking off" arm (amendment 2) | Raw prompts open a think block | Descriptive; it failed its gate too |
| A first-digit read without the gate (amendment 3) | Answers start with " **" or a word | Descriptive, labeled |
| Descriptive tables and figures (the critic's requests) | Share, absolute drops, upstream change, equal shares, strata | Labeled "added after data" |

## Pre-registered tests and Dan's predictions

| Test | Rule fixed before the run | Verdict | Dan's prediction |
|---|---|---|---|
| X0, 27B at layer 32 | lookup excess ≤ 0.10 and recall J-dependence ≥ 0.30; killed if excess ≥ 0.20 or recall < 0.20 | {{num|verdict_27b}} | confirmed, 80%: wrong |
| X0, 9B at layer 12 | the same | {{num|verdict_9b}} | confirmed, 80%: right |
| The 27B's layer-32 cell is valid for both readers | the whole edit flips ≥ 30% and ≥ 30 items | both valid | only recalls, 80%: wrong |
| W_E removal (H-token) | W_E lookup excess ≥ 0.20 with J++'s around | 9B: neither; 27B: not applicable | neither, 90%: right / wrong |
| W_U removal | both readers around | both models | inert, 90%: right |
| No chat template, thinking not disabled: gate | ≥ 80% for both readers | can't test | both pass, 80%: wrong |
| No chat template, thinking off: gate (amendment 2) | the same | can't test | both pass, 80%: wrong |

Scored question by question in [predictions/2026-10-24_dan.md](../predictions/2026-10-24_dan.md).

## Prompt formats and words

| Word | Meaning |
|---|---|
| chat | the chat template, thinking off (run key `chat`) |
| no chat template, thinking off | the template's empty think block added by hand; no roles, no instruction (run key `nochat`; two earlier runs say `nothink`) |
| no chat template, thinking not disabled | raw text (run key `raw`) |
| J++ | the refit J-lens, pinned per model (sha256 checked on load) |
| part | the 25-atom signed OMP fit of Δ over a dictionary's letter-token atoms |
| J-dependence | 1 − (flips without the part) / (flips with the whole edit) |
| excess | J-dependence minus that of a random subspace of the same share |
| graded contrast C | recall excess minus lookup excess on the same items (paired bootstrap over entities) |
| read | the top token after "Answer:" and a space is the alt answer's first token (chat) |
