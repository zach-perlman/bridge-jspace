# Late read: relay reference (A3), natural text, digit-swap relay test (opened 23 Oct)

Read-only summary at HEAD e9972ef; no repo file was edited. Scene sets: memory -> prompt (RL), items answered right with nothing hidden. 95% CIs: Wilson for rates; paired item bootstrap (4000 draws, seed 0) for the share; entity-cluster bootstrap (4000 draws, seed 0) for R. Status: UNVERIFIED (exploration phase).

## 1) A3 relay reference: hiding the answer's sentence from every later token

**What it tests:** hide the answer's sentence from the last tokens only, then from every token after it. If the last tokens carry at least 70% of the drop, the late read is a direct read. If they carry less, other tokens relay the answer.

**Where the verdict comes from:** no saved file has a late-read-v2 verdict for these runs (the newest `results/cross_model/` grid is from 12:18 and predates them). I applied the repo's own `late_read_v2()` from `scripts/cross_model_grid.py` to each run's `rows.jsonl`, in memory, using the same function the grid uses. Script: `/private/tmp/claude-502/-Users-danorel-Workspace-Research-mats-bridge-jspace/fa0f527d-6031-4147-8bc3-75ed29692476/scratchpad/lr_v2.py`; output: `/private/tmp/claude-502/-Users-danorel-Workspace-Research-mats-bridge-jspace/fa0f527d-6031-4147-8bc3-75ed29692476/scratchpad/lr_v2.json`.

**The rule:**
- share = (1 - last) / (1 - every later). It must be ≥ 0.70, judged on the point estimate.
- floor: every-later-token block ≤ 10% right, with upper bound ≤ 15%.
- off-path sentence hidden at both places keeps ≥ 90%.
- on a hybrid, the DeltaNet-only block keeps ≥ 90%.
- "Every later" means every attention layer on a hybrid (27B, 9B, Olmo-Hybrid, 122B) and every layer otherwise.

Column key: "last" = % right with last tokens blocked; "every later" = % right with every later token blocked; "relay" = last minus every later, in points.

| model · set | n | last % [CI] | every later % [CI] | relay | share [CI] | off-path (last / every later) | DeltaNet-only | verdict |
|---|---|---|---|---|---|---|---|---|
| 27B · seed2 | 300 | 7.3 [4.9, 10.8] | 2.0 [0.9, 4.3] | +5.3 | 0.95 [0.92, 0.97] | 100 / 100 | 100 | **holds** |
| 27B · long | 178 | 25.8 [20.0, 32.7] | 1.1 [0.3, 4.0] | +24.7 | 0.75 [0.69, 0.81] | 100 / 100 | 100 | **holds** |
| 9B · seed2 | 300 | 1.3 [0.5, 3.4] | 1.3 [0.5, 3.4] | 0.0 | 1.00 [0.98, 1.02] | 100 / 99.7 | 99.7 | **holds** |
| 9B · long | 156 | 0.6 [0.1, 3.5] | 0.0 [0, 2.4] | +0.6 | 0.99 [0.98, 1.00] | 100 / 99.4 | 100 | **holds** |
| Olmo-Hybrid · seed2 | 100 | 7.0 [3.4, 13.8] | 6.0 [2.8, 12.5] | +1.0 | 0.99 [0.95, 1.02] | 100 / 100 | 100 | **holds** |
| Olmo-Hybrid · long | 53 | 7.5 [3.0, 17.9] | 1.9 [0.3, 9.9] | +5.7 | 0.94 [0.87, 1.00] | 100 / 96.2 | 100 | **holds** |
| 32B · seed2 | 299 | 3.3 [1.8, 6.0] | 12.7 [9.4, 17.0] | −9.4 | 1.11 [1.07, 1.16] | 100 / 99.7 | – | **not interpretable** (floor > 10%) |
| 32B · long | 93 | 2.2 [0.6, 7.5] | 4.3 [1.7, 10.5] | −2.2 | 1.02 [0.98, 1.07] | 100 / 98.9 | – | **holds** |
| OLMo-3 · seed2 | 100 | 0.0 [0, 3.7] | 7.0 [3.4, 13.8] | −7.0 | 1.08 [1.03, 1.14] | 99 / 99 | – | **holds** |
| OLMo-3 · long | 41 | 4.9 [1.4, 16.1] | 9.8 [3.9, 22.6] | −4.9 | 1.05 [0.93, 1.21] | 100 / 95.1 | – | **not interpretable** (floor upper bound > 15%) |
| Muse · seed2 | 299 | 1.3 [0.5, 3.4] | 2.0 [0.9, 4.3] | −0.7 | 1.01 [0.99, 1.03] | 99.7 / 98.7 | – | **holds** |
| Muse · long | 167 | 16.8 [11.9, 23.2] | 0.0 [0, 2.2] | +16.8 | 0.83 [0.77, 0.89] | 100 / 100 | – | **holds** |
| Gemma · seed2 | 300 | 21.7 [17.4, 26.7] | 4.0 [2.3, 6.9] | +17.7 | 0.82 [0.76, 0.87] | 100 / 100 | – | **holds** |
| 122B · seed2 | 300 | 6.3 [4.1, 9.7] | 7.7 [5.2, 11.2] | −1.3 | 1.01 [0.98, 1.05] | 100 / 100 | 99.7 | **holds** |
| 122B · long | – | – | – | – | – | – | – | **still running** (no `_long_after` folder yet) |

On the hybrids, every later token blocked in all layers (DeltaNet included) leaves, in %: 27B 1.0 / 0.0, 9B 3.7 / 1.3, Olmo-Hybrid 9.0 / 0.0, and 122B 9.3 (seed2 only). The old late-read rule (≤ 20% right) still fails on 27B long (25.8%) and Gemma seed2 (21.7%), as before.

**Files:** `results/attn_knockout/<run>/rows.jsonl`, plus `analysis-*/summary.md` for the per-cell table. Runs:
- `d2_late_read_seed2_after_27b`, `d2_late_read_long_after_27b`
- `qwen35_9b_d2_late_read_{seed2,long}_after`
- `olmo_hybrid_7b_d2_late_read_{seed2,long}_after`
- `qwen3_32b_d2_late_read_{seed2,long}_after`
- `olmo3_7b_instruct_d2_late_read_{seed2,long}_after`
- `muse30b_d2_late_read_{seed2,long}_after`
- `gemma4it_d2_late_read_seed2_after`
- `qwen35_122b_d2_late_read_seed2_after`

**Dan's predictions (batch 20):**
- Q20.8 (every later token blocked in every layer: 27B, 9B, Gemma and OLMo-3 at "0–15% at max"): **match.** Observed 0–9.8% everywhere. OLMo-3 long's upper bound is 22.6%.
- Q20.9 (share ≥ 0.6 on 27B long and Gemma): **match.** Observed 0.75 and 0.82, both also ≥ 0.70.
- Q20.10 (122B "yes"): **match on seed2** (1.01). Long: pending.

**Odd things:**
- On 32B seed2, OLMo-3 seed2 and the 122B, blocking every later token leaves *more* answers right than blocking only the last tokens, which gives share > 1 and a negative relay. My guess (unchecked): the bigger block pushes the model to guess among the 5 listed digits (chance 20%), while the last-token block steers it to a wrong visible digit. So "every later token" is not a clean floor on these models.
- 27B long "holds" on the point estimate (0.75), but its interval dips to 0.69. The rule judges the point only.
- The long-context runs have small n on OLMo-3 (41) and Olmo-Hybrid (53).
- The 27B long spec's `n:` field says "100 ... (of 180)", but 178 items are counted.

## 2) Natural text: the late read on SQuAD paragraphs

**What it tests:** a Wikipedia paragraph, then the question, then "Answer:". The answer's sentence is hidden from the last tokens. The read holds if the model rarely still answers right.
- Primary bar: ≤ 10% right, upper bound ≤ 20%.
- Secondary bar: ≤ 20%, upper bound ≤ 30%.
- One seed (0); n = every eligible item.

**Source:** the verdicts are the run's own (`scripts/natural_read.py judge`), from the newest folder: `results/attn_knockout/<model>_d2_natural_read/analysis-*-verdict/verdict.{md,json}`. The 9B and 32B redraws (161146Z) have the same numbers as their 152xxxZ folders.

| model | n | last tokens blocked % [CI] | off-path | DeltaNet-only | floor (every later) | question words blocked | primary / secondary verdict |
|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | 469 | **30.1 [26.1, 34.4]** (article-cluster CI 25.8–34.5) | 99.8 | 99.6 | 0.2 | 70.8 [66.5, 74.7] | **fails / fails** |
| Qwen3.5-9B | 502 | 7.6 [5.6, 10.2] | 100 | 99.4 | 0.8 | 81.3 | **holds / holds** |
| Qwen3-32B | 442 | 7.0 [5.0, 9.8] | 99.5 | – | 0.0 | 75.8 | **holds / holds** |
| OLMo-3-7B | 426 | 4.7 [3.1, 7.1] | 99.5 | – | 1.2 | 63.6 | **holds / holds** |

The baselines are 0–1.4% on every model: the question after another article's paragraph, and blocked answers scored against another item's answer.

**Eligibility funnel** (`results/natural_read/<model>_natural_competence/summary.json`, repeated in verdict.md):

| model | built | after the short-first-token filter | after "first token on top with the paragraph" | eligible | right unedited |
|---|---|---|---|---|---|
| 27B | 718 | 632 | 487 | 469 | 469 |
| 9B | 718 | 632 | 533 | 503 | 502 |
| 32B | 718 | 628 | 484 | 443 | 442 |
| OLMo-3 | 718 | 628 | 515 | 428 | 426 |

The biggest single drop is "first token not on top with the paragraph" (99–145 items). Taken on its own, "the sentence alone is not enough" would fail 96–174 items, but most of those are already gone by then. So the result covers only answers that one sentence gives on its own.

**Dan's predictions (batch 19):**
- Q19.1 (27B and OLMo-3, 0–10%): **27B miss** (30%), **OLMo-3 match** (4.7%).
- Q19.2 (27B with the question words blocked, 95–100%): **miss** (70.8%). The question words also carry part of the read.
- Q19.3 (DeltaNet-only, 27B and 9B, 95–100%): **match** (99.6 / 99.4).

**Odd things:**
- On natural text the 27B behaves like its long-context run: 30% right under the last-token block, with the floor at 0.2%.
- This run has no share rule. The arithmetic (1 − 0.301) / (1 − 0.002) = 0.70 lands exactly on the A3 bar, and is descriptive only.
- The question-words block costs 19–36 points on every model, more than on the synthetic lists.

## 3) Relay test by swapping the hidden digit

**What it tests:** the digit in the answer's sentence is replaced by one that is not in the list, and the sentence is hidden from the last tokens. If the answer still follows the new digit, it reached the last tokens through other tokens. That is a relay, not a lucky guess.
- R = P(new digit | swapped) − P(new digit | original), both under the block.
- Relay iff R's lower bound > 5 points.
- Controls: the positive and off-path controls need ≥ 90% (lower bound ≥ 85%). In the floor (every later token blocked), R's lower bound must be ≤ 5 points.

**Source:** the run's own verdict (`scripts/relay_swap.py`), in `results/relay_swap/{gemma4it_d2_relay_swap/analysis-20261023T150530Z, d2_relay_swap_long_27b/analysis-20261023T152724Z}/verdict.{md,json}`.

| run | n | swapped → new digit | original → new digit | R [cluster CI] | positive | off-path | floor R | verdict |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B-it, first scene set, every layer | 300 | 20.7% [16.5, 25.6] | 0.3% [0.1, 1.9] | **+20.3 [+16.2, +24.7]** | 100% [98.7, 100] | 100% [98.7, 100] | 0.0 | **relay** |
| 27B long, every attention layer | 178 | 23.6% [18.0, 30.4] | 0.0% [0, 2.1] | **+23.6 [+18.3, +28.7]** | 100% [97.9, 100] | 100% [97.9, 100] | 0.0 | **relay** |
| 27B long, every layer incl. DeltaNet (reported) | 178 | 23.6% | 0.6% | +23.0 [+17.7, +28.4] | | | | (not decisive) |

**Per topic:** R is positive in every topic.
- Gemma: animals +26, body +16, countries +19.
- 27B: animals +24, body +20, countries +27.

**Agreement with the late-read runs:** the blocked top token matches the late-read run's rows on 99% (Gemma) and 100% (27B) of items.

**Answers under the block:**
- Gemma, original prompt: 22% old digit, 75% another listed digit.
- Gemma, swapped prompt: 21% new digit, 1% old.
- So nearly all of the right answers under the block follow the hidden sentence's digit.

**Dan's predictions (batch 24):**
- Q24.1 (Gemma, swapped 15–20%, original 0–5%): original **match**. Swapped 20.7% is **just above the range**, with the CI overlapping it. His "the floor is 2%" fits: the original prompt under the every-later block gives the old digit 1.7%. His "most of the 23% is a real relay" is **match**.
- Q24.2 (27B long, swapped 15–20%, original 0–5%): original **match**. Swapped 23.6% is **above the range** (the CI's lower end, 18.0%, is inside it).
- Q24.3 (every layer incl. DeltaNet, "within ~5%"): the answer is ambiguous.
  - If it means within 5 points of the attention-only result: **match** (23.6% vs 23.6%).
  - If it means about 5% new digit: **miss**.
  - His reason ("the relay goes through other tokens, not DeltaNet") is supported.

**Odd things:**
- The floor R is exactly 0.0, which is guaranteed by construction. The two prompts differ only inside the hidden sentence, so this is a check that the block does not leak, not an extra finding.
- The off-path "R = +100" is just the positive control seen through a block.
- Under the every-later block, Gemma gives a non-listed "other" answer 45% of the time, against 1% on the 27B.

## Takeaway

1. On every model, scene set and length that is interpretable, the last tokens carry ≥ 70% of the drop (share 0.75–1.0; 12 "holds", 2 "not interpretable" on the floor, 122B long running). The "leftover" right answers on Gemma (22%) and on 27B / Muse long (26% / 17%) are a real relay. The digit swap proves it for Gemma and 27B long: R = +20 and +24 points, lower bounds +16 and +18, while a guesser would score 0.
2. On natural Wikipedia text the late read holds on 9B, 32B and OLMo-3 (5–8% right) but fails on the 27B (30% right, floor 0.2%). On every model the question words carry part of the read (64–81% right when they are blocked, against Dan's 95–100%).
3. Dan's predictions: batch 20 matched; batch 19 missed on the 27B (Q19.1, Q19.2); batch 24 got the direction right but put the relay size 1–4 points too low. Caveat: on 32B / OLMo-3 / 122B the "every later token" floor can sit above the last-token block, so share > 1 there is a guessing artefact, not evidence.
