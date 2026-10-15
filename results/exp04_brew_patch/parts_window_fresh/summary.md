# exp04_brew_patch / parts_window_fresh

Items: no_target 1, eligible 154, not_eligible 45
Full copy reproduces patch_map (item x layer cells): 1232/1232

Step score (mean over items of the share of window layers giving f(X)):
- full: 31%
- jpp lens2: 0%
- jpp lens2 null: 0%
- jpp not_lens2: 31%
- jpp not_lens2 null: 0%
- jpp jspace: 0%
- jpp jspace null: 0%
- jpp not_jspace: 28%
- jpp not_jspace null: 0%
- jlens lens2: 0%
- jlens lens2 null: 0%
- jlens not_lens2: 31%
- jlens not_lens2 null: 0%
- jlens jspace: 0%
- jlens jspace null: 0%
- jlens not_jspace: 26%
- jlens not_jspace null: 0%

Decisions (paired bootstrap over items, pts):
- jpp lens2: not_lens2 - lens2 +31 [+26, +36]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +31 [+26, +36]; verdict: outside
- jpp jspace: not_jspace - jspace +28 [+24, +33]; jspace - its null +0 [+0, +0]; not_jspace - its null +28 [+24, +33]; verdict: outside
- jlens lens2: not_lens2 - lens2 +31 [+26, +36]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +31 [+26, +36]; verdict: outside
- jlens jspace: not_jspace - jspace +26 [+22, +31]; jspace - its null +0 [+0, +0]; not_jspace - its null +26 [+22, +31]; verdict: outside

Median share of δ's variance in each part (and of a random direction's, 'chance'):
- jpp chance: 0.074
- jpp lens2: 0.002
- jpp jspace: 0.076
- jlens chance: 0.070
- jlens lens2: 0.002
- jlens jspace: 0.084

| lens | part | source | null | layer | n | A | b = f(X) | c | X | edit ratio |
|---|---|---|---|---|---|---|---|---|---|---|
|  | full | cf |  | 36 | 154 | 45% | 10% | 0% | 3% | 0.072 |
|  | full | cf |  | 38 | 154 | 42% | 11% | 0% | 3% | 0.067 |
|  | full | cf |  | 40 | 154 | 32% | 19% | 3% | 3% | 0.074 |
|  | full | cf |  | 42 | 154 | 29% | 23% | 3% | 3% | 0.073 |
|  | full | cf |  | 44 | 154 | 19% | 40% | 5% | 3% | 0.088 |
|  | full | cf |  | 46 | 154 | 18% | 45% | 4% | 3% | 0.095 |
|  | full | cf |  | 48 | 154 | 8% | 52% | 12% | 6% | 0.114 |
|  | full | cf |  | 50 | 154 | 7% | 51% | 12% | 7% | 0.139 |
|  | full | off |  | 36 | 154 | 99% | 0% | 0% | 0% | 0.047 |
|  | full | off |  | 38 | 154 | 99% | 0% | 0% | 0% | 0.044 |
|  | full | off |  | 40 | 154 | 98% | 0% | 0% | 0% | 0.048 |
|  | full | off |  | 42 | 154 | 98% | 0% | 0% | 0% | 0.049 |
|  | full | off |  | 44 | 154 | 97% | 0% | 0% | 0% | 0.057 |
|  | full | off |  | 46 | 154 | 97% | 0% | 0% | 0% | 0.060 |
|  | full | off |  | 48 | 154 | 95% | 0% | 0% | 0% | 0.071 |
|  | full | off |  | 50 | 154 | 94% | 0% | 0% | 0% | 0.082 |
| jlens | jspace | cf |  | 36 | 154 | 97% | 0% | 0% | 1% | 0.022 |
| jlens | jspace | cf |  | 38 | 154 | 99% | 0% | 0% | 0% | 0.019 |
| jlens | jspace | cf |  | 40 | 154 | 98% | 0% | 0% | 0% | 0.021 |
| jlens | jspace | cf |  | 42 | 154 | 97% | 0% | 0% | 0% | 0.021 |
| jlens | jspace | cf |  | 44 | 154 | 97% | 0% | 0% | 0% | 0.025 |
| jlens | jspace | cf |  | 46 | 154 | 98% | 0% | 0% | 0% | 0.025 |
| jlens | jspace | cf |  | 48 | 154 | 97% | 0% | 0% | 0% | 0.033 |
| jlens | jspace | cf |  | 50 | 154 | 98% | 0% | 0% | 0% | 0.039 |
| jlens | jspace | cf | yes | 36 | 154 | 99% | 0% | 0% | 0% | 0.022 |
| jlens | jspace | cf | yes | 38 | 154 | 100% | 0% | 0% | 0% | 0.019 |
| jlens | jspace | cf | yes | 40 | 154 | 100% | 0% | 0% | 0% | 0.021 |
| jlens | jspace | cf | yes | 42 | 154 | 99% | 0% | 0% | 0% | 0.021 |
| jlens | jspace | cf | yes | 44 | 154 | 99% | 0% | 0% | 0% | 0.025 |
| jlens | jspace | cf | yes | 46 | 154 | 99% | 0% | 0% | 0% | 0.025 |
| jlens | jspace | cf | yes | 48 | 154 | 99% | 0% | 0% | 0% | 0.033 |
| jlens | jspace | cf | yes | 50 | 154 | 100% | 0% | 0% | 0% | 0.039 |
| jlens | lens2 | cf |  | 36 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 38 | 154 | 99% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 40 | 154 | 99% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf |  | 42 | 154 | 99% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 44 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 46 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf |  | 48 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf |  | 50 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf | yes | 36 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 38 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 40 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf | yes | 42 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 44 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 46 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jlens | lens2 | cf | yes | 48 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | lens2 | cf | yes | 50 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jlens | not_jspace | cf |  | 36 | 154 | 60% | 5% | 1% | 1% | 0.069 |
| jlens | not_jspace | cf |  | 38 | 154 | 51% | 7% | 0% | 2% | 0.064 |
| jlens | not_jspace | cf |  | 40 | 154 | 47% | 10% | 2% | 1% | 0.070 |
| jlens | not_jspace | cf |  | 42 | 154 | 37% | 17% | 3% | 3% | 0.070 |
| jlens | not_jspace | cf |  | 44 | 154 | 29% | 30% | 4% | 2% | 0.084 |
| jlens | not_jspace | cf |  | 46 | 154 | 19% | 42% | 4% | 3% | 0.092 |
| jlens | not_jspace | cf |  | 48 | 154 | 14% | 49% | 10% | 6% | 0.109 |
| jlens | not_jspace | cf |  | 50 | 154 | 8% | 52% | 11% | 7% | 0.133 |
| jlens | not_jspace | cf | yes | 36 | 154 | 99% | 0% | 0% | 0% | 0.069 |
| jlens | not_jspace | cf | yes | 38 | 154 | 98% | 1% | 0% | 0% | 0.064 |
| jlens | not_jspace | cf | yes | 40 | 154 | 97% | 1% | 0% | 0% | 0.070 |
| jlens | not_jspace | cf | yes | 42 | 154 | 98% | 0% | 0% | 0% | 0.070 |
| jlens | not_jspace | cf | yes | 44 | 154 | 95% | 0% | 0% | 0% | 0.084 |
| jlens | not_jspace | cf | yes | 46 | 154 | 95% | 0% | 0% | 0% | 0.092 |
| jlens | not_jspace | cf | yes | 48 | 154 | 98% | 0% | 0% | 0% | 0.109 |
| jlens | not_jspace | cf | yes | 50 | 154 | 98% | 0% | 0% | 0% | 0.133 |
| jlens | not_lens2 | cf |  | 36 | 154 | 44% | 9% | 0% | 3% | 0.072 |
| jlens | not_lens2 | cf |  | 38 | 154 | 41% | 11% | 0% | 3% | 0.067 |
| jlens | not_lens2 | cf |  | 40 | 154 | 32% | 18% | 3% | 3% | 0.074 |
| jlens | not_lens2 | cf |  | 42 | 154 | 29% | 21% | 3% | 3% | 0.073 |
| jlens | not_lens2 | cf |  | 44 | 154 | 19% | 40% | 4% | 3% | 0.088 |
| jlens | not_lens2 | cf |  | 46 | 154 | 19% | 44% | 4% | 3% | 0.095 |
| jlens | not_lens2 | cf |  | 48 | 154 | 8% | 54% | 12% | 6% | 0.114 |
| jlens | not_lens2 | cf |  | 50 | 154 | 7% | 52% | 12% | 6% | 0.139 |
| jlens | not_lens2 | cf | yes | 36 | 154 | 97% | 0% | 0% | 0% | 0.072 |
| jlens | not_lens2 | cf | yes | 38 | 154 | 96% | 0% | 0% | 0% | 0.067 |
| jlens | not_lens2 | cf | yes | 40 | 154 | 97% | 0% | 0% | 0% | 0.074 |
| jlens | not_lens2 | cf | yes | 42 | 154 | 97% | 0% | 0% | 0% | 0.073 |
| jlens | not_lens2 | cf | yes | 44 | 154 | 94% | 1% | 0% | 0% | 0.088 |
| jlens | not_lens2 | cf | yes | 46 | 154 | 97% | 0% | 0% | 0% | 0.095 |
| jlens | not_lens2 | cf | yes | 48 | 154 | 98% | 0% | 0% | 0% | 0.114 |
| jlens | not_lens2 | cf | yes | 50 | 154 | 97% | 1% | 0% | 0% | 0.139 |
| jpp | jspace | cf |  | 36 | 154 | 99% | 0% | 0% | 0% | 0.020 |
| jpp | jspace | cf |  | 38 | 154 | 98% | 0% | 0% | 0% | 0.018 |
| jpp | jspace | cf |  | 40 | 154 | 98% | 0% | 0% | 0% | 0.021 |
| jpp | jspace | cf |  | 42 | 154 | 98% | 0% | 0% | 0% | 0.020 |
| jpp | jspace | cf |  | 44 | 154 | 98% | 0% | 0% | 0% | 0.024 |
| jpp | jspace | cf |  | 46 | 154 | 97% | 0% | 0% | 0% | 0.026 |
| jpp | jspace | cf |  | 48 | 154 | 99% | 0% | 0% | 0% | 0.031 |
| jpp | jspace | cf |  | 50 | 154 | 99% | 0% | 0% | 0% | 0.037 |
| jpp | jspace | cf | yes | 36 | 154 | 100% | 0% | 0% | 0% | 0.020 |
| jpp | jspace | cf | yes | 38 | 154 | 100% | 0% | 0% | 0% | 0.018 |
| jpp | jspace | cf | yes | 40 | 154 | 100% | 0% | 0% | 0% | 0.021 |
| jpp | jspace | cf | yes | 42 | 154 | 100% | 0% | 0% | 0% | 0.020 |
| jpp | jspace | cf | yes | 44 | 154 | 99% | 0% | 0% | 0% | 0.024 |
| jpp | jspace | cf | yes | 46 | 154 | 100% | 0% | 0% | 0% | 0.026 |
| jpp | jspace | cf | yes | 48 | 154 | 99% | 0% | 0% | 0% | 0.031 |
| jpp | jspace | cf | yes | 50 | 154 | 100% | 0% | 0% | 0% | 0.037 |
| jpp | lens2 | cf |  | 36 | 154 | 99% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 38 | 154 | 99% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 40 | 154 | 99% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf |  | 42 | 154 | 99% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 44 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 46 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf |  | 48 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf |  | 50 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf | yes | 36 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 38 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 40 | 154 | 99% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf | yes | 42 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 44 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 46 | 154 | 100% | 0% | 0% | 0% | 0.003 |
| jpp | lens2 | cf | yes | 48 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | lens2 | cf | yes | 50 | 154 | 100% | 0% | 0% | 0% | 0.004 |
| jpp | not_jspace | cf |  | 36 | 154 | 53% | 6% | 0% | 3% | 0.070 |
| jpp | not_jspace | cf |  | 38 | 154 | 48% | 8% | 0% | 3% | 0.065 |
| jpp | not_jspace | cf |  | 40 | 154 | 44% | 12% | 3% | 2% | 0.071 |
| jpp | not_jspace | cf |  | 42 | 154 | 36% | 18% | 3% | 3% | 0.070 |
| jpp | not_jspace | cf |  | 44 | 154 | 25% | 37% | 4% | 2% | 0.085 |
| jpp | not_jspace | cf |  | 46 | 154 | 22% | 42% | 4% | 3% | 0.091 |
| jpp | not_jspace | cf |  | 48 | 154 | 10% | 52% | 11% | 6% | 0.109 |
| jpp | not_jspace | cf |  | 50 | 154 | 8% | 53% | 11% | 8% | 0.134 |
| jpp | not_jspace | cf | yes | 36 | 154 | 97% | 0% | 0% | 0% | 0.070 |
| jpp | not_jspace | cf | yes | 38 | 154 | 99% | 0% | 0% | 0% | 0.065 |
| jpp | not_jspace | cf | yes | 40 | 154 | 98% | 0% | 0% | 0% | 0.071 |
| jpp | not_jspace | cf | yes | 42 | 154 | 97% | 0% | 0% | 0% | 0.070 |
| jpp | not_jspace | cf | yes | 44 | 154 | 96% | 1% | 0% | 0% | 0.085 |
| jpp | not_jspace | cf | yes | 46 | 154 | 96% | 0% | 0% | 1% | 0.091 |
| jpp | not_jspace | cf | yes | 48 | 154 | 97% | 0% | 0% | 0% | 0.109 |
| jpp | not_jspace | cf | yes | 50 | 154 | 98% | 0% | 0% | 0% | 0.134 |
| jpp | not_lens2 | cf |  | 36 | 154 | 44% | 9% | 0% | 3% | 0.072 |
| jpp | not_lens2 | cf |  | 38 | 154 | 41% | 10% | 0% | 3% | 0.067 |
| jpp | not_lens2 | cf |  | 40 | 154 | 34% | 18% | 3% | 3% | 0.074 |
| jpp | not_lens2 | cf |  | 42 | 154 | 30% | 22% | 3% | 3% | 0.073 |
| jpp | not_lens2 | cf |  | 44 | 154 | 19% | 40% | 5% | 3% | 0.088 |
| jpp | not_lens2 | cf |  | 46 | 154 | 19% | 44% | 4% | 3% | 0.095 |
| jpp | not_lens2 | cf |  | 48 | 154 | 7% | 54% | 12% | 6% | 0.114 |
| jpp | not_lens2 | cf |  | 50 | 154 | 8% | 52% | 12% | 6% | 0.139 |
| jpp | not_lens2 | cf | yes | 36 | 154 | 98% | 0% | 0% | 0% | 0.072 |
| jpp | not_lens2 | cf | yes | 38 | 154 | 98% | 0% | 0% | 0% | 0.067 |
| jpp | not_lens2 | cf | yes | 40 | 154 | 98% | 1% | 0% | 0% | 0.074 |
| jpp | not_lens2 | cf | yes | 42 | 154 | 98% | 1% | 0% | 0% | 0.073 |
| jpp | not_lens2 | cf | yes | 44 | 154 | 98% | 0% | 0% | 0% | 0.088 |
| jpp | not_lens2 | cf | yes | 46 | 154 | 98% | 0% | 0% | 0% | 0.095 |
| jpp | not_lens2 | cf | yes | 48 | 154 | 99% | 0% | 0% | 1% | 0.114 |
| jpp | not_lens2 | cf | yes | 50 | 154 | 97% | 0% | 0% | 0% | 0.139 |
