# d5a_head_pointer / d5a_head_pointer_27b: analysis

EXP d5a_head_pointer_27b | model Qwen3.6-27B | n={'RL': 450, 'DL': 450, 'RR': 450} org prompts per family (rows: 4 patch settings each) | seeds=[0]

Claim tested: On unedited scenes layer 51 head 22 looks most at the asked statement from the last token (100% of held-out pointer_v1 scenes), but also on recall questions (95%), where the statement is not needed (d2_lookup_heads, UNVERIFIED). D3's patch of the alt prompt's last tokens / tokens after the question at layers 48 or 50 moves the answer to another statement of the org prompt (to the statement at the alt prompt's slot, or the alt entity's). Item by item: after the patch, does the head look most at the statement the new answer comes from (it follows the pointer), or still at the org prompt's asked statement (it tracks something the patch does not change)? Is that better than the J-lens's word read on the same tokens?

Headline: memory → prompt, layer 51, head 22, rows whose answer moved to another statement: looks most at the new answer's statement 58% [54, 62] (Wilson [54, 61]; n=776 / k=84 / t=9); still at the asked statement 38% [34, 41] (Wilson [35, 41]; n=776 / k=84 / t=9)   Baseline: rows whose answer stayed, on the asked statement 79% [77, 82] (Wilson [77, 82]; n=1024 / k=85 / t=9)   Control: the J-lens's word read on the same moved rows 18% [15, 22] (Wilson [16, 21]; n=776 / k=84 / t=9); head - lens +40 points [+35, +45] (entity cluster)
Verdict (pre-registered): neither

Controls: memory → prompt, same: answer changed 0% [0, 0] (Wilson [0, 0]; n=1800 / k=85 / t=9), head on the asked statement 99% [99, 100] (Wilson [99, 100]; n=1800 / k=85 / t=9); memory → prompt, rand: answer changed 0% [0, 0] (Wilson [0, 0]; n=1800 / k=85 / t=9), head on the asked statement 100% [99, 100] (Wilson [99, 100]; n=1800 / k=85 / t=9); named → prompt, same: answer changed 0% [0, 0] (Wilson [0, 0]; n=1800 / k=85 / t=9), head on the asked statement 99% [99, 100] (Wilson [99, 99]; n=1800 / k=85 / t=9); named → prompt, rand: answer changed 0% [0, 0] (Wilson [0, 0]; n=1800 / k=85 / t=9), head on the asked statement 100% [99, 100] (Wilson [99, 100]; n=1800 / k=85 / t=9); memory → memory, same: answer changed 0% [0, 0] (Wilson [0, 0]; n=1800 / k=85 / t=9), head on the asked statement 85% [81, 88] (Wilson [83, 86]; n=1800 / k=85 / t=9); memory → memory, rand: answer changed 0% [0, 0] (Wilson [0, 0]; n=1800 / k=85 / t=9), head on the asked statement 86% [83, 89] (Wilson [84, 87]; n=1800 / k=85 / t=9)

Figures: readers.png, readers.svg

Three dumbest ways this could be wrong:
1) The head looks at the new statement because the patch copied the alt prompt's whole last-token state, including its attention query, so 'follows' only says the query moved with the patch. Checked: that is the question here (does the query carry the pointer); the same-entity patch copies a state too and must leave the head on the asked statement (99% [99, 100] (Wilson [99, 100]; n=1800 / k=85 / t=9)).
2) Statement spans or the role map are off. Checked: the answer roles agree with d3v4_swap_main on the same items and edits in 99.1% of 5400 (item, tokens, layer); every statement has tokens (asserted); a self-patch changes the logits by at most 1.013.
3) Few entities carry the result. Checked: every interval is the entity-cluster bootstrap (k entities next to every number); per topic in the tables.

For the human to verify: rows.jsonl, family=RL, source=dissoc, outcome in ['slot', 'word', 'other statement']: count heads['51:22']['top'] == new_statement (expect 448/776).

Status: UNVERIFIED

## Pre-registered rule

> (fixed before the run; job spec jobs/d5/d5a_head_pointer_27b.yaml). Primary cut: memory → prompt, source dissoc, the four patch settings pooled; unit a row; intervals by entity cluster (queried entity resampled within topic, 4000 draws, seed 0; stats.cluster_bootstrap), item-level Wilson second; n rows / k entities / t wordings per cell; a cut is judged only with >= 35 rows.   H-head-follows (layer 51 head 22): on moved rows the head's top statement is the new statement with lower bound     >= 60%, AND on unmoved rows (kept) it is the org statement with lower bound >= 80%.   H-head-static: on moved rows the head's top statement is the org statement with lower bound >= 60%.   Otherwise neither (reported with the shares). The J-lens comparison: on the same moved rows, the share where the   lens's top entity's statement is the new statement; paired difference head - lens (entity cluster); the head reads   the pointer better than the lens iff its lower bound > 0.   Controls: the same-entity patch and the random push should move <= 10% of answers and leave the head on the org   statement (>= 80%); memory → memory: reported (does the head move to the bridge's new statement without a lookup?).   The other heads get the same numbers, not a verdict.

## Every reader and family (dissoc, settings pooled)

| family | reader | moved: new statement | moved: asked statement | kept: asked statement |
|---|---|---|---|---|
| memory → prompt | layer 51, head 22 | 58% [54, 62] (Wilson [54, 61]; n=776 / k=84 / t=9) | 38% [34, 41] (Wilson [35, 41]; n=776 / k=84 / t=9) | 79% [77, 82] (Wilson [77, 82]; n=1024 / k=85 / t=9) |
| memory → prompt | layer 59, head 3 | 60% [56, 63] (Wilson [56, 63]; n=776 / k=84 / t=9) | 38% [35, 42] (Wilson [35, 42]; n=776 / k=84 / t=9) | 75% [72, 77] (Wilson [72, 77]; n=1024 / k=85 / t=9) |
| memory → prompt | layer 59, head 1 | 57% [54, 61] (Wilson [54, 61]; n=776 / k=84 / t=9) | 40% [37, 43] (Wilson [37, 44]; n=776 / k=84 / t=9) | 73% [70, 76] (Wilson [70, 76]; n=1024 / k=85 / t=9) |
| memory → prompt | layer 55, head 23 | 53% [50, 57] (Wilson [50, 57]; n=776 / k=84 / t=9) | 39% [35, 42] (Wilson [35, 42]; n=776 / k=84 / t=9) | 73% [70, 76] (Wilson [71, 76]; n=1024 / k=85 / t=9) |
| memory → prompt | layer 59, head 21 | 65% [61, 68] (Wilson [61, 68]; n=776 / k=84 / t=9) | 32% [29, 35] (Wilson [29, 35]; n=776 / k=84 / t=9) | 77% [74, 80] (Wilson [75, 80]; n=1024 / k=85 / t=9) |
| memory → prompt | the J-lens | 18% [15, 22] (Wilson [16, 21]; n=776 / k=84 / t=9) | 25% [19, 33] (Wilson [22, 29]; n=776 / k=84 / t=9) | 34% [27, 41] (Wilson [31, 37]; n=1024 / k=85 / t=9) |
| named → prompt | layer 51, head 22 | 31% [29, 33] (Wilson [28, 35]; n=702 / k=85 / t=9) | 68% [67, 70] (Wilson [65, 72]; n=702 / k=85 / t=9) | 66% [63, 68] (Wilson [63, 69]; n=1098 / k=85 / t=9) |
| named → prompt | layer 59, head 3 | 33% [31, 35] (Wilson [30, 36]; n=702 / k=85 / t=9) | 67% [65, 69] (Wilson [63, 70]; n=702 / k=85 / t=9) | 66% [63, 68] (Wilson [63, 69]; n=1098 / k=85 / t=9) |
| named → prompt | layer 59, head 1 | 33% [31, 36] (Wilson [30, 37]; n=702 / k=85 / t=9) | 65% [62, 68] (Wilson [62, 69]; n=702 / k=85 / t=9) | 69% [66, 71] (Wilson [66, 71]; n=1098 / k=85 / t=9) |
| named → prompt | layer 55, head 23 | 37% [34, 39] (Wilson [33, 40]; n=702 / k=85 / t=9) | 60% [57, 63] (Wilson [56, 64]; n=702 / k=85 / t=9) | 67% [64, 69] (Wilson [64, 70]; n=1098 / k=85 / t=9) |
| named → prompt | layer 59, head 21 | 50% [46, 53] (Wilson [46, 53]; n=702 / k=85 / t=9) | 49% [45, 53] (Wilson [45, 53]; n=702 / k=85 / t=9) | 63% [59, 66] (Wilson [60, 65]; n=1098 / k=85 / t=9) |
| named → prompt | the J-lens | 17% [13, 21] (Wilson [15, 20]; n=702 / k=85 / t=9) | 30% [22, 38] (Wilson [27, 33]; n=702 / k=85 / t=9) | 24% [18, 32] (Wilson [22, 27]; n=1098 / k=85 / t=9) |
| memory → memory | layer 51, head 22 | 25% [22, 29] (Wilson [22, 28]; n=834 / k=82 / t=9) | 36% [32, 39] (Wilson [32, 39]; n=834 / k=82 / t=9) | 63% [59, 67] (Wilson [60, 66]; n=960 / k=85 / t=9) |
| memory → memory | layer 59, head 3 | 25% [21, 30] (Wilson [22, 28]; n=834 / k=82 / t=9) | 36% [31, 41] (Wilson [33, 39]; n=834 / k=82 / t=9) | 69% [66, 73] (Wilson [66, 72]; n=960 / k=85 / t=9) |
| memory → memory | layer 59, head 1 | 28% [23, 33] (Wilson [25, 31]; n=834 / k=82 / t=9) | 33% [26, 39] (Wilson [30, 36]; n=834 / k=82 / t=9) | 56% [51, 60] (Wilson [52, 59]; n=960 / k=85 / t=9) |
| memory → memory | layer 55, head 23 | 26% [22, 31] (Wilson [23, 29]; n=834 / k=82 / t=9) | 39% [34, 45] (Wilson [36, 43]; n=834 / k=82 / t=9) | 70% [66, 73] (Wilson [67, 73]; n=960 / k=85 / t=9) |
| memory → memory | layer 59, head 21 | 21% [18, 25] (Wilson [19, 24]; n=834 / k=82 / t=9) | 26% [21, 30] (Wilson [23, 29]; n=834 / k=82 / t=9) | 43% [38, 48] (Wilson [40, 46]; n=960 / k=85 / t=9) |
| memory → memory | the J-lens | 66% [63, 70] (Wilson [63, 70]; n=834 / k=82 / t=9) | 30% [26, 34] (Wilson [27, 33]; n=834 / k=82 / t=9) | 65% [62, 68] (Wilson [62, 68]; n=960 / k=85 / t=9) |

## By patch setting (layer 51 head 22)

| family | patched tokens | layer | answer moved | moved: new statement | kept: asked statement |
|---|---|---|---|---|---|
| memory → prompt | the last two tokens | 48 | 24% [20, 28] (Wilson [20, 28]; n=450 / k=85 / t=9) | 93% [89, 97] (Wilson [87, 97]; n=106 / k=55 / t=9) | 54% [48, 59] (Wilson [48, 59]; n=344 / k=85 / t=9) |
| memory → prompt | the last two tokens | 50 | 81% [78, 85] (Wilson [77, 84]; n=450 / k=85 / t=9) | 92% [88, 95] (Wilson [89, 94]; n=365 / k=83 / t=9) | 42% [32, 52] (Wilson [32, 53]; n=85 / k=55 / t=9) |
| memory → prompt | every token after the question | 48 | 36% [31, 41] (Wilson [31, 40]; n=450 / k=85 / t=9) | 9% [5, 13] (Wilson [5, 14]; n=161 / k=74 / t=9) | 99% [98, 100] (Wilson [97, 100]; n=289 / k=80 / t=9) |
| memory → prompt | every token after the question | 50 | 32% [28, 36] (Wilson [28, 36]; n=450 / k=85 / t=9) | 0% [0, 0] (Wilson [0, 3]; n=144 / k=69 / t=9) | 100% [99, 100] (Wilson [98, 100]; n=306 / k=81 / t=9) |
| named → prompt | the last two tokens | 48 | 0% [0, 1] (Wilson [0, 1]; n=450 / k=85 / t=9) | 100% [100, 100] (Wilson [21, 100]; n=1 / k=1 / t=1) | 60% [55, 65] (Wilson [55, 64]; n=449 / k=85 / t=9) |
| named → prompt | the last two tokens | 50 | 48% [43, 53] (Wilson [43, 53]; n=450 / k=85 / t=9) | 99% [98, 100] (Wilson [97, 100]; n=216 / k=77 / t=9) | 17% [12, 22] (Wilson [13, 22]; n=234 / k=81 / t=9) |
| named → prompt | every token after the question | 48 | 29% [25, 33] (Wilson [25, 33]; n=450 / k=85 / t=9) | 2% [0, 4] (Wilson [0, 5]; n=129 / k=66 / t=9) | 100% [100, 100] (Wilson [99, 100]; n=321 / k=84 / t=9) |
| named → prompt | every token after the question | 50 | 79% [76, 82] (Wilson [75, 83]; n=450 / k=85 / t=9) | 0% [0, 1] (Wilson [0, 2]; n=356 / k=85 / t=9) | 100% [100, 100] (Wilson [96, 100]; n=94 / k=61 / t=9) |
| memory → memory | the last two tokens | 48 | 48% [41, 54] (Wilson [43, 52]; n=450 / k=85 / t=9) | 19% [14, 24] (Wilson [14, 25]; n=214 / k=56 / t=9) | 42% [36, 48] (Wilson [36, 49]; n=235 / k=64 / t=9) |
| memory → memory | the last two tokens | 50 | 82% [78, 85] (Wilson [78, 85]; n=450 / k=85 / t=9) | 40% [35, 46] (Wilson [35, 45]; n=367 / k=82 / t=9) | 17% [9, 25] (Wilson [10, 27]; n=82 / k=42 / t=9) |
| memory → memory | every token after the question | 48 | 33% [27, 39] (Wilson [29, 38]; n=450 / k=85 / t=9) | 12% [7, 18] (Wilson [8, 18]; n=149 / k=36 / t=9) | 64% [57, 70] (Wilson [58, 69]; n=299 / k=79 / t=9) |
| memory → memory | every token after the question | 50 | 23% [18, 29] (Wilson [19, 27]; n=450 / k=85 / t=9) | 4% [0, 8] (Wilson [2, 9]; n=104 / k=33 / t=9) | 88% [84, 91] (Wilson [84, 91]; n=344 / k=83 / t=9) |

## By outcome (dissoc): share naming the new answer's statement

| family | outcome | layer 51, head 22 | layer 59, head 3 | layer 59, head 1 | layer 55, head 23 | layer 59, head 21 | the J-lens |
|---|---|---|---|---|---|---|---|
| memory → prompt | slot | 57% [54, 61] (Wilson [53, 62]; n=515 / k=79 / t=9) | 58% [55, 62] (Wilson [54, 63]; n=515 / k=79 / t=9) | 56% [52, 60] (Wilson [52, 60]; n=515 / k=79 / t=9) | 54% [50, 59] (Wilson [50, 58]; n=515 / k=79 / t=9) | 69% [65, 73] (Wilson [65, 73]; n=515 / k=79 / t=9) | 13% [9, 18] (Wilson [11, 17]; n=515 / k=79 / t=9) |
| memory → prompt | word | 55% [49, 62] (Wilson [48, 62]; n=193 / k=54 / t=9) | 55% [50, 62] (Wilson [48, 62]; n=193 / k=54 / t=9) | 56% [51, 62] (Wilson [49, 63]; n=193 / k=54 / t=9) | 52% [47, 58] (Wilson [45, 59]; n=193 / k=54 / t=9) | 54% [49, 61] (Wilson [47, 61]; n=193 / k=54 / t=9) | 33% [24, 43] (Wilson [27, 40]; n=193 / k=54 / t=9) |
| memory → prompt | other statement | 68% [54, 80] (Wilson [56, 78]; n=68 / k=40 / t=9) | 81% [71, 91] (Wilson [70, 88]; n=68 / k=40 / t=9) | 71% [59, 82] (Wilson [59, 80]; n=68 / k=40 / t=9) | 47% [35, 60] (Wilson [36, 59]; n=68 / k=40 / t=9) | 62% [50, 74] (Wilson [50, 72]; n=68 / k=40 / t=9) | 12% [3, 21] (Wilson [6, 22]; n=68 / k=40 / t=9) |
| named → prompt | slot | 32% [30, 34] (Wilson [28, 37]; n=460 / k=79 / t=9) | 35% [32, 37] (Wilson [30, 39]; n=460 / k=79 / t=9) | 37% [33, 40] (Wilson [32, 41]; n=460 / k=79 / t=9) | 40% [36, 43] (Wilson [36, 45]; n=460 / k=79 / t=9) | 61% [57, 66] (Wilson [57, 66]; n=460 / k=79 / t=9) | 15% [10, 20] (Wilson [12, 18]; n=460 / k=79 / t=9) |
| named → prompt | word | 31% [27, 35] (Wilson [25, 39]; n=159 / k=55 / t=9) | 32% [28, 36] (Wilson [25, 40]; n=159 / k=55 / t=9) | 31% [27, 35] (Wilson [24, 38]; n=159 / k=55 / t=9) | 35% [30, 39] (Wilson [28, 42]; n=159 / k=55 / t=9) | 30% [26, 34] (Wilson [24, 38]; n=159 / k=55 / t=9) | 22% [15, 30] (Wilson [16, 29]; n=159 / k=55 / t=9) |
| named → prompt | other statement | 24% [18, 30] (Wilson [16, 34]; n=83 / k=43 / t=9) | 25% [19, 31] (Wilson [17, 36]; n=83 / k=43 / t=9) | 22% [15, 28] (Wilson [14, 32]; n=83 / k=43 / t=9) | 22% [15, 28] (Wilson [14, 32]; n=83 / k=43 / t=9) | 23% [17, 29] (Wilson [15, 33]; n=83 / k=43 / t=9) | 22% [13, 32] (Wilson [14, 32]; n=83 / k=43 / t=9) |
| memory → memory | slot | - | - | - | - | - | - |
| memory → memory | word | 25% [22, 29] (Wilson [22, 28]; n=834 / k=82 / t=9) | 25% [21, 30] (Wilson [22, 28]; n=834 / k=82 / t=9) | 28% [23, 33] (Wilson [25, 31]; n=834 / k=82 / t=9) | 26% [22, 31] (Wilson [23, 29]; n=834 / k=82 / t=9) | 21% [18, 25] (Wilson [19, 24]; n=834 / k=82 / t=9) | 66% [63, 70] (Wilson [63, 70]; n=834 / k=82 / t=9) |
| memory → memory | other statement | - | - | - | - | - | - |

## Per topic (layer 51 head 22, memory → prompt, moved rows: new statement)

- animals: 59% (n=268)
- body: 69% (n=241)
- countries: 46% (n=267)

## The agent's priors (job spec hypotheses), checked

| hypothesis | prediction | result | verdict |
|---|---|---|---|
| H_head_follows | memory → prompt, layer 51 head 22: on rows whose answer moved to another statement it looks most at the new answer's statement (entity-cluster lower bound >= 60%), and on rows whose answer stayed a... | moved -> new 58% [54, 62] (Wilson [54, 61]; n=776 / k=84 / t=9); kept -> asked 79% [77, 82] (Wilson [77, 82]; n=1024 / k=85 / t=9) | fails |
| H_head_static | it stays on the asked statement when the answer moves (lower bound >= 60%). Prior 0.35 | moved -> asked 38% [34, 41] (Wilson [35, 41]; n=776 / k=84 / t=9) | fails |
| H_head_beats_lens | on the same moved rows the head names the new statement more often than the J-lens's top entity at the last token (layer 50, what the head reads): paired entity-cluster lower bound > 0. Prior 0.6 | head - lens +40 [+35, +45] | holds |
| H_controls | the same-entity patch and the random push change <= 10% of answers in each lookup family (d3v4_swap_main: 0% [0, 1] for both). Prior 0.9 | RL|same: ok, RL|rand: ok, DL|same: ok, DL|rand: ok, RR|same: ok, RR|rand: ok | holds |
