# 53.3b: the last-token conflict test on word answers

Batch 53, test 53.3b (jobs/c3/batch53.yaml test_53_3b; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). Zach's named-bridge passages (Z1-P's items: PP = the lookup copies a made-up word the passage states; PM = the recall, the same answer vocabulary); the change at the last token at each reader's own answer layer minus 1, 2, 3 and 51.10's read peak. UNVERIFIED.

Rule per reader and layer (53.3's): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between"; 53.3's validity bar (S_whole >= 0.3, >= 30 switches) applied.

Rule across readers: "copy bypasses the lens" if at answer - 1 and - 2 the recall is "through the lens" and the lookup "outside" on >= 3 of 4 models; "digits only" if on words the lookup goes through the lens like the recall; else in between.

As computed: 53.3's (the loss beyond random = (S_no_rand - S_no_jpp) / S_whole; the rest alone = S_no_jpp / S_whole, the same vector); a cell under 53.3's validity bar is "invalid" and counts for neither clause; per model a clause holds when it holds at both answer - 1 and - 2 with all four cells valid; "digits only" read as the lookup and the recall both "through the lens" at both layers, on >= 3 of 4 models, as the first clause; the answer layer = the plain logit lens at O's last token (51.10's settle rule: the layer from which O's answer token stays top through the last layer, the lower median over the passages); a layer without a J++ map is dropped and named.

**Across readers: pending (1 of 4 models)** (copy bypasses on 0 of 1 models run, digits only on 0).

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning ○ | lookup | 49 (answer L50 - 1) | 129 (100) | 1.00 [1.00, 1.00] | 0.06 [0.02, 0.11] | 0.88 [0.83, 0.93] | 0.87 [0.81, 0.92] | 0.82 [0.75, 0.89] | 0.06 [0.02, 0.11] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | lookup | 48 (answer L50 - 2) | 129 (100) | 1.00 [1.00, 1.00] | 0.03 [0.01, 0.06] | 0.88 [0.83, 0.93] | 0.84 [0.77, 0.90] | 0.85 [0.79, 0.91] | 0.03 [0.01, 0.06] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | lookup | 47 (answer L50 - 3) | 129 (100) | 0.99 [0.98, 1.00] | 0.05 [0.02, 0.09] | 0.80 [0.73, 0.86] | 0.74 [0.66, 0.81] | 0.76 [0.68, 0.83] | 0.05 [0.02, 0.09] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | lookup | 32 (read peak) | 129 (100) | 0.47 [0.39, 0.56] | 0.40 [0.31, 0.49] | 0.37 [0.29, 0.46] | 0.00 [0.00, 0.00] | -0.05 [-0.12, 0.02] | 0.84 [0.73, 0.93] | **computes outside the lens at the last token** | yes |
| nemotron-3.5-lightning ○ | recall | 49 (answer L50 - 1) | 129 (100) | 0.99 [0.98, 1.00] | 0.03 [0.01, 0.06] | 0.90 [0.84, 0.95] | 0.95 [0.90, 0.98] | 0.88 [0.81, 0.93] | 0.03 [0.01, 0.06] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | recall | 48 (answer L50 - 2) | 129 (100) | 0.99 [0.98, 1.00] | 0.04 [0.01, 0.08] | 0.90 [0.85, 0.95] | 0.95 [0.90, 0.98] | 0.87 [0.80, 0.93] | 0.04 [0.01, 0.08] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | recall | 47 (answer L50 - 3) | 129 (100) | 1.00 [1.00, 1.00] | 0.05 [0.02, 0.10] | 0.80 [0.72, 0.87] | 0.94 [0.89, 0.98] | 0.74 [0.66, 0.82] | 0.05 [0.02, 0.10] | **through the lens** | yes |
| nemotron-3.5-lightning ○ | recall | 36 (read peak) | 129 (100) | 0.26 [0.18, 0.35] | 0.03 [0.01, 0.06] | 0.07 [0.03, 0.12] | 0.06 [0.02, 0.10] | 0.15 [0.04, 0.27] | 0.12 [0.03, 0.23] | **invalid (in between)** | no |

Per model (answer - 1 and - 2): nemotron-3.5-lightning: copy bypasses no, digits only yes {"lookup answer-1": "through", "lookup answer-2": "through", "recall answer-1": "through", "recall answer-2": "through"}.

○ nemotron-3.5-lightning: below gate (exploratory): Z1-P's gate on nemotron-3.5-lightning fails ({'K': 0.7939508506616257, 'M': 0.9224952741020794} < 0.80); its eligible passages only; hollow, rules verbatim, no prediction
- nemotron-3.5-lightning (nem35l_x53_3b): answer layer (never settled, layers without a lens map) {'lookup': (50, 0, []), 'recall': (50, 0, [])}

## The check: 53.3's lookup on the locker scenes at its own answer layer minus 1 and minus 3

| model | reader | layer (why) | n | whole | without the lens part | without a random part | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | lookup | 44 (answer L45 - 1) | 59 | 1.00 [1.00, 1.00] | 0.73 [0.60, 0.85] | 0.92 [0.85, 0.98] | 0.19 [0.09, 0.29] | 0.73 [0.60, 0.85] | **in between** | yes |
| nemotron-3.5-lightning | lookup | 42 (answer L45 - 3) | 59 | 1.00 [1.00, 1.00] | 0.78 [0.66, 0.90] | 0.92 [0.85, 0.98] | 0.14 [0.05, 0.22] | 0.78 [0.66, 0.90] | **in between** | yes |

Figure: x53_lastconflict_words.png
