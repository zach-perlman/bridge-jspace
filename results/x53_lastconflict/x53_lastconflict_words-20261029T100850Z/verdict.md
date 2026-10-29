# 53.3b: the last-token conflict test on word answers

Batch 53, test 53.3b (jobs/c3/batch53.yaml test_53_3b; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). Zach's named-bridge passages (Z1-P's items: PP = the lookup copies a made-up word the passage states; PM = the recall, the same answer vocabulary); the change at the last token at each reader's own answer layer minus 1, 2, 3 and 51.10's read peak. UNVERIFIED.

Rule per reader and layer (53.3's): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between"; 53.3's validity bar (S_whole >= 0.3, >= 30 switches) applied.

Rule across readers: "copy bypasses the lens" if at answer - 1 and - 2 the recall is "through the lens" and the lookup "outside" on >= 3 of 4 models; "digits only" if on words the lookup goes through the lens like the recall; else in between.

As computed: 53.3's (the loss beyond random = (S_no_rand - S_no_jpp) / S_whole; the rest alone = S_no_jpp / S_whole, the same vector); a cell under 53.3's validity bar is "invalid" and counts for neither clause; per model a clause holds when it holds at both answer - 1 and - 2 with all four cells valid; "digits only" read as the lookup and the recall both "through the lens" at both layers, on >= 3 of 4 models, as the first clause; the answer layer = the plain logit lens at O's last token (51.10's settle rule: the layer from which O's answer token stays top through the last layer, the lower median over the passages); a layer without a J++ map is dropped and named; a model below its source's gate (○, hollow) is shown and never counted toward a clause.

**Across readers: in between (only 2 of 4 models above their gate: neither clause can reach 3 of 4)** (copy bypasses on 0 and digits only on 2 of the 2 models counted; 4 models run).

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | lookup | 30 (answer L31 - 1) | 112 (86) | 0.79 [0.71, 0.86] | 0.08 [0.04, 0.13] | 0.51 [0.42, 0.60] | 0.59 [0.50, 0.68] | 0.55 [0.44, 0.64] | 0.10 [0.05, 0.17] | **through the lens** | yes |
| qwen3.5-9b | lookup | 29 (answer L31 - 2) | 112 (86) | 0.53 [0.43, 0.62] | 0.18 [0.11, 0.25] | 0.38 [0.29, 0.46] | 0.14 [0.08, 0.21] | 0.37 [0.23, 0.53] | 0.34 [0.22, 0.46] | **through the lens** | yes |
| qwen3.5-9b | lookup | 28 (answer L31 - 3) | 112 (86) | 0.44 [0.35, 0.53] | 0.16 [0.09, 0.23] | 0.23 [0.15, 0.31] | 0.12 [0.06, 0.19] | 0.16 [0.05, 0.29] | 0.37 [0.23, 0.51] | **in between** | yes |
| qwen3.5-9b | lookup | 24 (read peak) | 112 (86) | 0.34 [0.25, 0.43] | 0.21 [0.13, 0.28] | 0.21 [0.14, 0.29] | 0.04 [0.01, 0.08] | 0.03 [-0.06, 0.12] | 0.61 [0.44, 0.77] | **in between** | yes |
| qwen3.5-9b | recall | 30 (answer L31 - 1) | 112 (86) | 0.96 [0.93, 0.99] | 0.03 [0.00, 0.06] | 0.65 [0.56, 0.75] | 0.83 [0.75, 0.90] | 0.65 [0.55, 0.75] | 0.03 [0.00, 0.06] | **through the lens** | yes |
| qwen3.5-9b | recall | 29 (answer L31 - 2) | 112 (86) | 0.72 [0.63, 0.81] | 0.07 [0.03, 0.13] | 0.43 [0.32, 0.53] | 0.09 [0.04, 0.14] | 0.49 [0.37, 0.62] | 0.10 [0.04, 0.17] | **through the lens** | yes |
| qwen3.5-9b | recall | 28 (answer L31 - 3) | 112 (86) | 0.32 [0.23, 0.42] | 0.01 [0.00, 0.03] | 0.16 [0.09, 0.24] | 0.04 [0.01, 0.07] | 0.47 [0.29, 0.65] | 0.03 [0.00, 0.09] | **through the lens** | yes |
| qwen3.5-9b | recall | 24 (read peak) | 112 (86) | 0.18 [0.10, 0.26] | 0.02 [0.00, 0.05] | 0.12 [0.06, 0.20] | 0.01 [0.00, 0.03] | 0.60 [0.35, 0.83] | 0.10 [0.00, 0.24] | **invalid (through the lens)** | no |
| qwen3.6-27b | lookup | 62 (answer L63 - 1) | 200 (118) | 0.99 [0.98, 1.00] | 0.04 [0.01, 0.06] | 0.92 [0.88, 0.95] | 0.78 [0.72, 0.83] | 0.88 [0.84, 0.92] | 0.04 [0.01, 0.06] | **through the lens** | yes |
| qwen3.6-27b | lookup | 61 (answer L63 - 2) | 200 (118) | 0.98 [0.97, 1.00] | 0.21 [0.16, 0.27] | 0.94 [0.91, 0.97] | 0.25 [0.20, 0.31] | 0.74 [0.68, 0.80] | 0.22 [0.16, 0.27] | **through the lens** | yes |
| qwen3.6-27b | lookup | 60 (read peak) | 200 (118) | 0.97 [0.95, 0.99] | 0.26 [0.20, 0.32] | 0.83 [0.78, 0.88] | 0.04 [0.01, 0.07] | 0.58 [0.51, 0.65] | 0.27 [0.21, 0.33] | **through the lens** | yes |
| qwen3.6-27b | recall | 62 (answer L63 - 1) | 200 (118) | 0.99 [0.98, 1.00] | 0.00 [0.00, 0.00] | 0.96 [0.93, 0.98] | 0.89 [0.83, 0.93] | 0.96 [0.94, 0.99] | 0.00 [0.00, 0.00] | **through the lens** | yes |
| qwen3.6-27b | recall | 61 (answer L63 - 2) | 200 (118) | 0.98 [0.97, 1.00] | 0.02 [0.00, 0.04] | 0.89 [0.85, 0.93] | 0.48 [0.41, 0.56] | 0.88 [0.84, 0.93] | 0.02 [0.00, 0.04] | **through the lens** | yes |
| qwen3.6-27b | recall | 60 (answer L63 - 3) | 200 (118) | 0.94 [0.90, 0.97] | 0.01 [0.00, 0.02] | 0.60 [0.53, 0.67] | 0.34 [0.27, 0.41] | 0.64 [0.56, 0.71] | 0.01 [0.00, 0.02] | **through the lens** | yes |
| qwen3.6-27b | recall | 56 (read peak) | 200 (118) | 0.90 [0.86, 0.94] | 0.04 [0.01, 0.07] | 0.60 [0.53, 0.67] | 0.14 [0.09, 0.18] | 0.62 [0.54, 0.70] | 0.04 [0.02, 0.08] | **through the lens** | yes |
| muse-glimmer-30b ○ | lookup | 48 (answer L49 - 1) | 120 (85) | 0.96 [0.92, 0.99] | 0.07 [0.03, 0.13] | 0.83 [0.76, 0.90] | 0.69 [0.60, 0.78] | 0.79 [0.71, 0.87] | 0.08 [0.03, 0.13] | **through the lens** | yes |
| muse-glimmer-30b ○ | lookup | 47 (answer L49 - 2) | 120 (85) | 0.97 [0.93, 0.99] | 0.17 [0.10, 0.24] | 0.80 [0.72, 0.87] | 0.48 [0.40, 0.57] | 0.66 [0.56, 0.74] | 0.17 [0.11, 0.25] | **through the lens** | yes |
| muse-glimmer-30b ○ | lookup | 46 (answer L49 - 3) | 120 (85) | 0.97 [0.93, 0.99] | 0.22 [0.15, 0.29] | 0.86 [0.79, 0.92] | 0.33 [0.25, 0.42] | 0.66 [0.58, 0.75] | 0.22 [0.15, 0.30] | **through the lens** | yes |
| muse-glimmer-30b ○ | lookup | 32 (read peak) | 120 (85) | 0.27 [0.19, 0.34] | 0.24 [0.17, 0.32] | 0.23 [0.15, 0.30] | 0.01 [0.00, 0.03] | -0.06 [-0.16, 0.00] | 0.91 [0.79, 1.00] | **invalid (computes outside the lens at the last token)** | no |
| muse-glimmer-30b ○ | recall | 48 (answer L49 - 1) | 120 (85) | 0.95 [0.91, 0.98] | 0.00 [0.00, 0.00] | 0.71 [0.62, 0.79] | 0.76 [0.68, 0.83] | 0.75 [0.66, 0.83] | 0.00 [0.00, 0.00] | **through the lens** | yes |
| muse-glimmer-30b ○ | recall | 47 (answer L49 - 2) | 120 (85) | 0.95 [0.91, 0.98] | 0.02 [0.00, 0.04] | 0.65 [0.56, 0.74] | 0.59 [0.51, 0.68] | 0.67 [0.57, 0.76] | 0.02 [0.00, 0.05] | **through the lens** | yes |
| muse-glimmer-30b ○ | recall | 46 (answer L49 - 3) | 120 (85) | 0.95 [0.91, 0.98] | 0.02 [0.00, 0.04] | 0.68 [0.59, 0.76] | 0.57 [0.48, 0.66] | 0.69 [0.60, 0.78] | 0.02 [0.00, 0.04] | **through the lens** | yes |
| muse-glimmer-30b ○ | recall | 40 (read peak) | 120 (85) | 0.90 [0.84, 0.95] | 0.01 [0.00, 0.03] | 0.71 [0.63, 0.79] | 0.40 [0.31, 0.50] | 0.78 [0.70, 0.86] | 0.01 [0.00, 0.03] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | lookup | 49 (answer L50 - 1) | 129 (100) | 1.00 [1.00, 1.00] | 0.06 [0.02, 0.11] | 0.88 [0.83, 0.93] | 0.87 [0.81, 0.92] | 0.82 [0.75, 0.89] | 0.06 [0.02, 0.11] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | lookup | 48 (answer L50 - 2) | 129 (100) | 1.00 [1.00, 1.00] | 0.03 [0.01, 0.06] | 0.88 [0.83, 0.93] | 0.84 [0.77, 0.90] | 0.85 [0.79, 0.91] | 0.03 [0.01, 0.06] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | lookup | 47 (answer L50 - 3) | 129 (100) | 0.99 [0.98, 1.00] | 0.05 [0.02, 0.09] | 0.80 [0.73, 0.86] | 0.74 [0.66, 0.81] | 0.76 [0.68, 0.83] | 0.05 [0.02, 0.09] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | lookup | 32 (read peak) | 129 (100) | 0.47 [0.39, 0.56] | 0.40 [0.31, 0.49] | 0.37 [0.29, 0.46] | 0.00 [0.00, 0.00] | -0.05 [-0.12, 0.02] | 0.84 [0.73, 0.93] | **computes outside the lens at the last token** | yes |
| nemotron-3.5-lightning ○ | recall | 49 (answer L50 - 1) | 129 (100) | 0.99 [0.98, 1.00] | 0.03 [0.01, 0.06] | 0.90 [0.84, 0.95] | 0.95 [0.90, 0.98] | 0.88 [0.81, 0.93] | 0.03 [0.01, 0.06] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | recall | 48 (answer L50 - 2) | 129 (100) | 0.99 [0.98, 1.00] | 0.04 [0.01, 0.08] | 0.90 [0.85, 0.95] | 0.95 [0.90, 0.98] | 0.87 [0.80, 0.93] | 0.04 [0.01, 0.08] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | recall | 47 (answer L50 - 3) | 129 (100) | 1.00 [1.00, 1.00] | 0.05 [0.02, 0.10] | 0.80 [0.72, 0.87] | 0.94 [0.89, 0.98] | 0.74 [0.66, 0.82] | 0.05 [0.02, 0.10] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | recall | 36 (read peak) | 129 (100) | 0.26 [0.18, 0.35] | 0.03 [0.01, 0.06] | 0.07 [0.03, 0.12] | 0.06 [0.02, 0.10] | 0.15 [0.04, 0.27] | 0.12 [0.03, 0.23] | **invalid (in between)** | no |

Per model (answer - 1 and - 2): qwen3.5-9b: copy bypasses no, digits only yes {"lookup answer-1": "through", "lookup answer-2": "through", "recall answer-1": "through", "recall answer-2": "through"}; qwen3.6-27b: copy bypasses no, digits only yes {"lookup answer-1": "through", "lookup answer-2": "through", "recall answer-1": "through", "recall answer-2": "through"}; muse-glimmer-30b: copy bypasses no, digits only yes {"lookup answer-1": "through", "lookup answer-2": "through", "recall answer-1": "through", "recall answer-2": "through"}; nemotron-3.5-lightning: copy bypasses no, digits only yes {"lookup answer-1": "through", "lookup answer-2": "through", "recall answer-1": "through", "recall answer-2": "through"}.

- qwen3.5-9b (qwen35_9b_x53_3b): answer layer (never settled, layers without a lens map) {'lookup': (31, 0, []), 'recall': (31, 0, [])}
- qwen3.6-27b (x53_3b_27b): answer layer (never settled, layers without a lens map) {'lookup': (63, 0, []), 'recall': (63, 0, [])}
○ muse-glimmer-30b: below gate (exploratory): Z1-P's gate on muse-glimmer-30b fails ({'K': 0.78125, 'M': 0.8584558823529411} < 0.80); its eligible passages only; hollow, rules verbatim, no prediction
- muse-glimmer-30b (muse30_x53_3b): answer layer (never settled, layers without a lens map) {'lookup': (49, 2, []), 'recall': (49, 0, [])}
○ nemotron-3.5-lightning: below gate (exploratory): Z1-P's gate on nemotron-3.5-lightning fails ({'K': 0.7939508506616257, 'M': 0.9224952741020794} < 0.80); its eligible passages only; hollow, rules verbatim, no prediction
- nemotron-3.5-lightning (nem35l_x53_3b): answer layer (never settled, layers without a lens map) {'lookup': (50, 0, []), 'recall': (50, 0, [])}

## The check: 53.3's lookup on the locker scenes at its own answer layer minus 1 and minus 3

| model | reader | layer (why) | n | whole | without the lens part | without a random part | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | lookup | 28 (answer L29 - 1) | 75 | 0.84 [0.77, 0.91] | 0.15 [0.07, 0.23] | 0.31 [0.19, 0.42] | 0.19 [0.11, 0.26] | 0.17 [0.08, 0.26] | **in between** | yes |
| qwen3.5-9b | lookup | 26 (answer L29 - 3) | 75 | 0.73 [0.63, 0.84] | 0.27 [0.16, 0.38] | 0.31 [0.18, 0.45] | 0.05 [-0.02, 0.13] | 0.36 [0.23, 0.50] | **in between** | yes |
| qwen3.6-27b | lookup | 60 (read peak) | 69 | 0.45 [0.35, 0.55] | 0.09 [0.03, 0.15] | 0.14 [0.08, 0.21] | 0.13 [0.03, 0.25] | 0.19 [0.07, 0.33] | **in between** | yes |
| qwen3.6-27b | lookup | 58 (answer L61 - 3) | 69 | 0.29 [0.21, 0.37] | 0.26 [0.17, 0.35] | 0.20 [0.12, 0.29] | -0.20 [-0.36, -0.05] | 0.90 [0.74, 1.00] | **computes outside the lens at the last token** | no |
| muse-glimmer-30b | lookup | 34 (answer L35 - 1) | 68 | 0.96 [0.90, 1.00] | 0.94 [0.88, 0.99] | 0.93 [0.87, 0.98] | -0.02 [-0.05, 0.00] | 0.98 [0.95, 1.00] | **computes outside the lens at the last token** | yes |
| muse-glimmer-30b | lookup | 32 (read peak) | 68 | 0.88 [0.82, 0.95] | 0.88 [0.82, 0.95] | 0.88 [0.82, 0.95] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | **computes outside the lens at the last token** | yes |
| nemotron-3.5-lightning | lookup | 44 (answer L45 - 1) | 59 | 1.00 [1.00, 1.00] | 0.73 [0.60, 0.85] | 0.92 [0.85, 0.98] | 0.19 [0.09, 0.29] | 0.73 [0.60, 0.85] | **in between** | yes |
| nemotron-3.5-lightning | lookup | 42 (answer L45 - 3) | 59 | 1.00 [1.00, 1.00] | 0.78 [0.66, 0.90] | 0.92 [0.85, 0.98] | 0.14 [0.05, 0.22] | 0.78 [0.66, 0.90] | **in between** | yes |

Figure: x53_lastconflict_words.png
