# exp04_brew_patch / parts_window

Items: not_eligible 17, no_target 1, eligible 82
Full copy reproduces patch_map (item x layer cells): 656/656

Step score (mean over items of the share of window layers giving f(X)):
- full: 31%
- jpp lens2: 0%
- jpp lens2 null: 0%
- jpp not_lens2: 31%
- jpp not_lens2 null: 0%
- jpp jspace: 0%
- jpp jspace null: 0%
- jpp not_jspace: 26%
- jpp not_jspace null: 0%
- jlens lens2: 0%
- jlens lens2 null: 0%
- jlens not_lens2: 30%
- jlens not_lens2 null: 0%
- jlens jspace: 0%
- jlens jspace null: 0%
- jlens not_jspace: 24%
- jlens not_jspace null: 0%

Decisions (paired bootstrap over items, pts):
- jpp lens2: not_lens2 - lens2 +31 [+24, +38]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +30 [+24, +37]; verdict: outside
- jpp jspace: not_jspace - jspace +26 [+20, +32]; jspace - its null +0 [+0, +0]; not_jspace - its null +26 [+20, +32]; verdict: outside
- jlens lens2: not_lens2 - lens2 +30 [+24, +37]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +30 [+24, +37]; verdict: outside
- jlens jspace: not_jspace - jspace +24 [+18, +30]; jspace - its null +0 [+0, +0]; not_jspace - its null +24 [+18, +30]; verdict: outside

Median share of δ's variance in each part (and of a random direction's, 'chance'):
- jpp chance: 0.074
- jpp lens2: 0.002
- jpp jspace: 0.076
- jlens chance: 0.070
- jlens lens2: 0.002
- jlens jspace: 0.083

| lens | part | source | null | layer | n | A | b = f(X) | c | X | edit ratio |
|---|---|---|---|---|---|---|---|---|---|---|
|  | full | cf |  | 36 | 82 | 63% | 11% | 0% | 1% | 0.073 |
|  | full | cf |  | 38 | 82 | 57% | 13% | 0% | 1% | 0.067 |
|  | full | cf |  | 40 | 82 | 48% | 18% | 1% | 1% | 0.073 |
|  | full | cf |  | 42 | 82 | 45% | 23% | 2% | 1% | 0.073 |
|  | full | cf |  | 44 | 82 | 35% | 38% | 4% | 0% | 0.088 |
|  | full | cf |  | 46 | 82 | 28% | 48% | 1% | 1% | 0.094 |
|  | full | cf |  | 48 | 82 | 11% | 48% | 9% | 7% | 0.116 |
|  | full | cf |  | 50 | 82 | 12% | 48% | 9% | 7% | 0.138 |
|  | full | off |  | 36 | 82 | 100% | 0% | 0% | 0% | 0.045 |
|  | full | off |  | 38 | 82 | 100% | 0% | 0% | 0% | 0.042 |
|  | full | off |  | 40 | 82 | 100% | 0% | 0% | 0% | 0.045 |
|  | full | off |  | 42 | 82 | 100% | 0% | 0% | 0% | 0.046 |
|  | full | off |  | 44 | 82 | 99% | 0% | 0% | 1% | 0.054 |
|  | full | off |  | 46 | 82 | 98% | 0% | 0% | 1% | 0.057 |
|  | full | off |  | 48 | 82 | 98% | 0% | 0% | 1% | 0.066 |
|  | full | off |  | 50 | 82 | 98% | 0% | 0% | 1% | 0.082 |
| jlens | jspace | cf |  | 36 | 82 | 100% | 0% | 0% | 0% | 0.022 |
| jlens | jspace | cf |  | 38 | 82 | 100% | 0% | 0% | 0% | 0.019 |
| jlens | jspace | cf |  | 40 | 82 | 100% | 0% | 0% | 0% | 0.022 |
| jlens | jspace | cf |  | 42 | 82 | 100% | 0% | 0% | 0% | 0.021 |
| jlens | jspace | cf |  | 44 | 82 | 100% | 0% | 0% | 0% | 0.025 |
| jlens | jspace | cf |  | 46 | 82 | 100% | 0% | 0% | 0% | 0.025 |
| jlens | jspace | cf |  | 48 | 82 | 100% | 0% | 0% | 0% | 0.033 |
| jlens | jspace | cf |  | 50 | 82 | 100% | 0% | 0% | 0% | 0.039 |
| jlens | jspace | cf | yes | 36 | 82 | 100% | 0% | 0% | 0% | 0.022 |
| jlens | jspace | cf | yes | 38 | 82 | 100% | 0% | 0% | 0% | 0.019 |
| jlens | jspace | cf | yes | 40 | 82 | 100% | 0% | 0% | 0% | 0.022 |
| jlens | jspace | cf | yes | 42 | 82 | 100% | 0% | 0% | 0% | 0.021 |
| jlens | jspace | cf | yes | 44 | 82 | 100% | 0% | 0% | 0% | 0.025 |
| jlens | jspace | cf | yes | 46 | 82 | 100% | 0% | 0% | 0% | 0.025 |
| jlens | jspace | cf | yes | 48 | 82 | 100% | 0% | 0% | 0% | 0.033 |
| jlens | jspace | cf | yes | 50 | 82 | 100% | 0% | 0% | 0% | 0.039 |
| jlens | lens2 | cf |  | 36 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 38 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 40 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf |  | 42 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 44 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf |  | 46 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 48 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf |  | 50 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf | yes | 36 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 38 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 40 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf | yes | 42 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 44 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf | yes | 46 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 48 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf | yes | 50 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | not_jspace | cf |  | 36 | 82 | 78% | 4% | 0% | 1% | 0.070 |
| jlens | not_jspace | cf |  | 38 | 82 | 71% | 7% | 0% | 1% | 0.065 |
| jlens | not_jspace | cf |  | 40 | 82 | 65% | 9% | 0% | 1% | 0.070 |
| jlens | not_jspace | cf |  | 42 | 82 | 55% | 17% | 1% | 1% | 0.070 |
| jlens | not_jspace | cf |  | 44 | 82 | 48% | 27% | 1% | 0% | 0.085 |
| jlens | not_jspace | cf |  | 46 | 82 | 34% | 40% | 1% | 1% | 0.090 |
| jlens | not_jspace | cf |  | 48 | 82 | 20% | 43% | 7% | 7% | 0.111 |
| jlens | not_jspace | cf |  | 50 | 82 | 17% | 45% | 7% | 7% | 0.132 |
| jlens | not_jspace | cf | yes | 36 | 82 | 100% | 0% | 0% | 0% | 0.070 |
| jlens | not_jspace | cf | yes | 38 | 82 | 100% | 0% | 0% | 0% | 0.065 |
| jlens | not_jspace | cf | yes | 40 | 82 | 100% | 0% | 0% | 0% | 0.070 |
| jlens | not_jspace | cf | yes | 42 | 82 | 100% | 0% | 0% | 0% | 0.070 |
| jlens | not_jspace | cf | yes | 44 | 82 | 100% | 0% | 0% | 0% | 0.085 |
| jlens | not_jspace | cf | yes | 46 | 82 | 100% | 0% | 0% | 0% | 0.090 |
| jlens | not_jspace | cf | yes | 48 | 82 | 100% | 0% | 0% | 0% | 0.111 |
| jlens | not_jspace | cf | yes | 50 | 82 | 100% | 0% | 0% | 0% | 0.132 |
| jlens | not_lens2 | cf |  | 36 | 82 | 65% | 10% | 0% | 1% | 0.073 |
| jlens | not_lens2 | cf |  | 38 | 82 | 57% | 13% | 0% | 1% | 0.067 |
| jlens | not_lens2 | cf |  | 40 | 82 | 51% | 17% | 2% | 1% | 0.073 |
| jlens | not_lens2 | cf |  | 42 | 82 | 44% | 21% | 2% | 1% | 0.073 |
| jlens | not_lens2 | cf |  | 44 | 82 | 34% | 38% | 4% | 0% | 0.088 |
| jlens | not_lens2 | cf |  | 46 | 82 | 28% | 46% | 1% | 1% | 0.094 |
| jlens | not_lens2 | cf |  | 48 | 82 | 12% | 49% | 7% | 7% | 0.116 |
| jlens | not_lens2 | cf |  | 50 | 82 | 11% | 49% | 9% | 7% | 0.138 |
| jlens | not_lens2 | cf | yes | 36 | 82 | 100% | 0% | 0% | 0% | 0.073 |
| jlens | not_lens2 | cf | yes | 38 | 82 | 100% | 0% | 0% | 0% | 0.067 |
| jlens | not_lens2 | cf | yes | 40 | 82 | 100% | 0% | 0% | 0% | 0.073 |
| jlens | not_lens2 | cf | yes | 42 | 82 | 100% | 0% | 0% | 0% | 0.073 |
| jlens | not_lens2 | cf | yes | 44 | 82 | 100% | 0% | 0% | 0% | 0.088 |
| jlens | not_lens2 | cf | yes | 46 | 82 | 98% | 0% | 0% | 0% | 0.094 |
| jlens | not_lens2 | cf | yes | 48 | 82 | 100% | 0% | 0% | 0% | 0.116 |
| jlens | not_lens2 | cf | yes | 50 | 82 | 100% | 0% | 0% | 0% | 0.138 |
| jpp | jspace | cf |  | 36 | 82 | 100% | 0% | 0% | 0% | 0.020 |
| jpp | jspace | cf |  | 38 | 82 | 100% | 0% | 0% | 0% | 0.018 |
| jpp | jspace | cf |  | 40 | 82 | 100% | 0% | 0% | 0% | 0.021 |
| jpp | jspace | cf |  | 42 | 82 | 100% | 0% | 0% | 0% | 0.020 |
| jpp | jspace | cf |  | 44 | 82 | 100% | 0% | 0% | 0% | 0.024 |
| jpp | jspace | cf |  | 46 | 82 | 100% | 0% | 0% | 0% | 0.026 |
| jpp | jspace | cf |  | 48 | 82 | 100% | 0% | 0% | 0% | 0.032 |
| jpp | jspace | cf |  | 50 | 82 | 100% | 0% | 0% | 0% | 0.037 |
| jpp | jspace | cf | yes | 36 | 82 | 100% | 0% | 0% | 0% | 0.020 |
| jpp | jspace | cf | yes | 38 | 82 | 100% | 0% | 0% | 0% | 0.018 |
| jpp | jspace | cf | yes | 40 | 82 | 100% | 0% | 0% | 0% | 0.021 |
| jpp | jspace | cf | yes | 42 | 82 | 100% | 0% | 0% | 0% | 0.020 |
| jpp | jspace | cf | yes | 44 | 82 | 100% | 0% | 0% | 0% | 0.024 |
| jpp | jspace | cf | yes | 46 | 82 | 100% | 0% | 0% | 0% | 0.026 |
| jpp | jspace | cf | yes | 48 | 82 | 100% | 0% | 0% | 0% | 0.032 |
| jpp | jspace | cf | yes | 50 | 82 | 100% | 0% | 0% | 0% | 0.037 |
| jpp | lens2 | cf |  | 36 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 38 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 40 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf |  | 42 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 44 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf |  | 46 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 48 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf |  | 50 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf | yes | 36 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 38 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 40 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf | yes | 42 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 44 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf | yes | 46 | 82 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 48 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf | yes | 50 | 82 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | not_jspace | cf |  | 36 | 82 | 70% | 9% | 0% | 1% | 0.070 |
| jpp | not_jspace | cf |  | 38 | 82 | 70% | 10% | 0% | 1% | 0.065 |
| jpp | not_jspace | cf |  | 40 | 82 | 59% | 12% | 1% | 1% | 0.070 |
| jpp | not_jspace | cf |  | 42 | 82 | 54% | 16% | 2% | 1% | 0.070 |
| jpp | not_jspace | cf |  | 44 | 82 | 39% | 33% | 4% | 1% | 0.085 |
| jpp | not_jspace | cf |  | 46 | 82 | 37% | 39% | 1% | 2% | 0.090 |
| jpp | not_jspace | cf |  | 48 | 82 | 17% | 44% | 7% | 7% | 0.111 |
| jpp | not_jspace | cf |  | 50 | 82 | 15% | 43% | 10% | 9% | 0.133 |
| jpp | not_jspace | cf | yes | 36 | 82 | 100% | 0% | 0% | 0% | 0.070 |
| jpp | not_jspace | cf | yes | 38 | 82 | 100% | 0% | 0% | 0% | 0.065 |
| jpp | not_jspace | cf | yes | 40 | 82 | 100% | 0% | 0% | 0% | 0.070 |
| jpp | not_jspace | cf | yes | 42 | 82 | 100% | 0% | 0% | 0% | 0.070 |
| jpp | not_jspace | cf | yes | 44 | 82 | 100% | 0% | 0% | 0% | 0.085 |
| jpp | not_jspace | cf | yes | 46 | 82 | 100% | 0% | 0% | 0% | 0.090 |
| jpp | not_jspace | cf | yes | 48 | 82 | 100% | 0% | 0% | 0% | 0.111 |
| jpp | not_jspace | cf | yes | 50 | 82 | 100% | 0% | 0% | 0% | 0.133 |
| jpp | not_lens2 | cf |  | 36 | 82 | 65% | 10% | 0% | 1% | 0.073 |
| jpp | not_lens2 | cf |  | 38 | 82 | 57% | 13% | 0% | 1% | 0.067 |
| jpp | not_lens2 | cf |  | 40 | 82 | 51% | 18% | 1% | 1% | 0.073 |
| jpp | not_lens2 | cf |  | 42 | 82 | 45% | 21% | 2% | 1% | 0.073 |
| jpp | not_lens2 | cf |  | 44 | 82 | 35% | 39% | 4% | 0% | 0.088 |
| jpp | not_lens2 | cf |  | 46 | 82 | 28% | 46% | 1% | 1% | 0.094 |
| jpp | not_lens2 | cf |  | 48 | 82 | 12% | 49% | 7% | 7% | 0.116 |
| jpp | not_lens2 | cf |  | 50 | 82 | 12% | 49% | 7% | 7% | 0.138 |
| jpp | not_lens2 | cf | yes | 36 | 82 | 100% | 0% | 0% | 0% | 0.073 |
| jpp | not_lens2 | cf | yes | 38 | 82 | 100% | 0% | 0% | 0% | 0.067 |
| jpp | not_lens2 | cf | yes | 40 | 82 | 99% | 1% | 0% | 0% | 0.073 |
| jpp | not_lens2 | cf | yes | 42 | 82 | 99% | 0% | 0% | 0% | 0.073 |
| jpp | not_lens2 | cf | yes | 44 | 82 | 100% | 0% | 0% | 0% | 0.088 |
| jpp | not_lens2 | cf | yes | 46 | 82 | 100% | 0% | 0% | 0% | 0.094 |
| jpp | not_lens2 | cf | yes | 48 | 82 | 99% | 0% | 0% | 0% | 0.116 |
| jpp | not_lens2 | cf | yes | 50 | 82 | 100% | 0% | 0% | 0% | 0.138 |
