# D4 (1): is the address one code across depth? (Q-depth, Dan: - Part D1: (a) · 60%; (b) · 55%; (c) · 45%
- Part D2: 60%
- Part D3: 40%;
- Part D4: one code · 60%; re-encoded · 30%; in between · 10%). UNVERIFIED.

Rule (D4, verbatim): persistent if the mean cos^2 of the principal angles >= 0.5 across the window where the slot probe is >= 0.8; re-encoded if it drops below 0.2 between adjacent sampled layers. The same for I_l, read as the fit half's entity mass-mean basis Id_l over the identity probe's window.

| model | basis | rank | window | mean cos^2 | adjacent drops | label |
|---|---|---|---|---|---|---|
| qwen3.6-27b | U | [2] | [8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60] | 0.256 | none | mixed |
| qwen3.6-27b | Id | [31] | [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60] | 0.386 | none | mixed |
