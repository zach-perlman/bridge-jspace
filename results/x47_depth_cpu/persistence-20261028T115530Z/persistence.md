# D4 (1): is the address one code across depth? (Q-depth, Dan: - Part D1: (a) · 60%; (b) · 55%; (c) · 45%
- Part D2: 60%
- Part D3: 40%;
- Part D4: one code · 60%; re-encoded · 30%; in between · 10%). UNVERIFIED.

Rule (D4, verbatim): persistent if the mean cos^2 of the principal angles >= 0.5 across the window where the slot probe is >= 0.8; re-encoded if it drops below 0.2 between adjacent sampled layers. The same for I_l, read as the fit half's entity mass-mean basis Id_l over the identity probe's window.

| model | basis | rank | window | mean cos^2 | adjacent drops | label |
|---|---|---|---|---|---|---|
| qwen3.5-9b | U | [2] | [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30] | 0.279 | ['6-8'] | re-encoded |
| qwen3.5-9b | Id | [30] | [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30] | 0.432 | none | mixed |
| muse-glimmer-30b | U | [2] | [6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50] | 0.213 | ['6-10'] | re-encoded |
| muse-glimmer-30b | Id | [31] | [2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50] | 0.365 | none | mixed |
