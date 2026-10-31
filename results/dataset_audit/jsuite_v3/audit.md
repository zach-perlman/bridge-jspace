# jsuite_v3: dataset audit

36504 fact items (18252 per rendering), 141 probes.

| check | violations | of | expected | pass |
|---|---|---|---|---|
| recalled finals (M, N): answer absent from the passage | 0 | 10296 | 0 violations | yes |
| answer-elsewhere finals (A): answer present once on another entity | 0 | 3744 | 0 violations | yes |
| nothing-stated finals (N): no answer-vocabulary word anywhere | 0 | 3744 | 0 violations | yes |
| never-named start (R): bridge never in the passage | 0 | 2808 | 0 violations | yes |
| every other start names the bridge | 0 | 33696 | 0 violations | yes |
| two-mention start (W): the distractor is named and not bound to anyone | 0 | 3744 | 0 violations | yes |
| described starts: the question never names the bridge | 0 | 16848 | 0 violations | yes |
| described starts: the question never contains the answer or an alias | 0 | 16848 | 0 violations | yes |
| stated finals (K, G, H): the true answer is in the passage | 0 | 11232 | 0 violations | yes |
| conflict finals: the counterfactual is in the passage | 0 | 9360 | 0 violations | yes |
| conflict finals: the counterfactual differs from the truth | 0 | 9360 | 0 violations | yes |
| counterfactual pairs (Y): passage identical to its P partner except the bridge | 0 | 936 | 0 violations | yes |
| computed start (X): the arithmetic picks the bridge | 0 | 936 | 0 violations | yes |
| duplicate item ids | 0 | 36645 | 0 violations | yes |
| hard-read anchors are made up (not a bridge or answer) | 0 | 15400 | 0 violations | yes |
| scenes where another entity shares the bridge's answer (reported, not excluded) | 0 | 11232 | a few | yes |
| answers (as written) share no first token: qwen3.6-27b | 0 | 5 | 0 violations | yes |
| answers (as written) share no first token: qwen3.5-9b | 0 | 5 | 0 violations | yes |
| answers (as written) share no first token: nemotron-3.5-lightning | 0 | 5 | 0 violations | yes |
| answers (as written) share no first token: muse-glimmer-30b | 0 | 5 | 0 violations | yes |
| answers (as written) share no first token: ministral-3-14b | 0 | 5 | 0 violations | yes |
