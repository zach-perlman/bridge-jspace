# exp07_step_code / code_v1

Items (fresh): no_target 1, eligible 154, not_eligible 45
Items (bank): no_target 1, eligible 82, not_eligible 17
Caches: {"code": {"sha256": "c8f1492411295b0b5544e6ed2dfaba143679b6a533707d70c6a6204f9a9a5f9e", "fit_items_used": 883, "fit_items_wrong": 117}, "sigma": {"sha256": "b42285005bf1b09c623c4f4321d1a0689834b18af955d6f72f1f4a41be8d53f8", "n_positions": 100156}}

## fresh items (n=154)

Copy reproduces exp04's full rows: 1232/1232
Read accuracy of the code (intermediate decoded on the items' own activations, chance 8%): L36 91%, L38 87%, L40 92%, L42 90%, L44 89%, L46 84%, L48 81%, L50 76%

| edit | step score | A kept | X | I |
|---|---|---|---|---|
| copy | 31% | 25% | 4% | 29% |
| code | 34% | 26% | 3% | 25% |
| random | 0% | 97% | 0% | 2% |
| code (own size) | 4% | 72% | 1% | 19% |
| random (own size) | 0% | 99% | 0% | 1% |
| jpp lens | 1% | 93% | 2% | 2% |
| jpp sigma_0.5 | 1% | 90% | 1% | 6% |
| jpp sigma_0.0 | 1% | 90% | 1% | 6% |
| jpp code_jspace | 0% | 97% | 0% | 1% |
| jpp code_rest | 29% | 32% | 2% | 27% |
| jlens lens | 1% | 91% | 3% | 3% |
| jlens sigma_0.5 | 1% | 91% | 1% | 5% |
| jlens sigma_0.0 | 1% | 91% | 1% | 5% |
| jlens code_jspace | 0% | 95% | 0% | 3% |
| jlens code_rest | 27% | 35% | 2% | 27% |

Paired differences in step score (pts, 95% CI):
- copy - random: +31 [+26, +36]
- code - random: +34 [+29, +39]
- code - jpp lens: +33 [+27, +38]
- jpp sigma_0.5 - jpp lens: +0 [-1, +1]
- jpp sigma_0.0 - jpp lens: -0 [-2, +1]
- jpp code rest - jspace: +29 [+24, +33]
- jpp code jspace - random: -0 [-0, +0]
- jpp code rest - random: +29 [+24, +33]
- code - jlens lens: +33 [+28, +38]
- jlens sigma_0.5 - jlens lens: -0 [-1, +0]
- jlens sigma_0.0 - jlens lens: -0 [-1, +1]
- jlens code rest - jspace: +27 [+22, +31]
- jlens code jspace - random: +0 [-0, +0]
- jlens code rest - random: +27 [+22, +31]
- code - random (own size): +4 [+2, +6]

Verdicts (rules in the manifest):
- interpreted: True
- jpp code parts: outside
- jpp sigma helps: False
- jlens code parts: outside
- jlens sigma helps: False
- code writes the step: True
- code writes where the J++ lens does not: True
- code at its own size writes the step: True

## bank items (n=82)

Copy reproduces exp04's full rows: 656/656
Read accuracy of the code (intermediate decoded on the items' own activations, chance 8%): L36 88%, L38 85%, L40 93%, L42 87%, L44 88%, L46 82%, L48 84%, L50 76%

| edit | step score | A kept | X | I |
|---|---|---|---|---|
| copy | 31% | 38% | 3% | 22% |
| code | 25% | 40% | 5% | 22% |
| random | 0% | 100% | 0% | 0% |
| code (own size) | 4% | 88% | 0% | 5% |
| random (own size) | 0% | 100% | 0% | 0% |
| jpp lens | 1% | 99% | 0% | 0% |
| jpp sigma_0.5 | 0% | 99% | 0% | 0% |
| jpp sigma_0.0 | 0% | 99% | 0% | 0% |
| jpp code_jspace | 0% | 100% | 0% | 0% |
| jpp code_rest | 20% | 48% | 4% | 21% |
| jlens lens | 1% | 99% | 0% | 0% |
| jlens sigma_0.5 | 1% | 99% | 0% | 0% |
| jlens sigma_0.0 | 0% | 99% | 0% | 0% |
| jlens code_jspace | 0% | 100% | 0% | 0% |
| jlens code_rest | 18% | 50% | 4% | 21% |

Paired differences in step score (pts, 95% CI):
- copy - random: +31 [+24, +38]
- code - random: +25 [+19, +31]
- code - jpp lens: +24 [+18, +30]
- jpp sigma_0.5 - jpp lens: -0 [-1, +0]
- jpp sigma_0.0 - jpp lens: -0 [-1, +0]
- jpp code rest - jspace: +20 [+15, +25]
- jpp code jspace - random: +0 [+0, +0]
- jpp code rest - random: +20 [+15, +25]
- code - jlens lens: +24 [+18, +30]
- jlens sigma_0.5 - jlens lens: +0 [-0, +0]
- jlens sigma_0.0 - jlens lens: -0 [-0, +0]
- jlens code rest - jspace: +18 [+13, +24]
- jlens code jspace - random: +0 [+0, +0]
- jlens code rest - random: +18 [+13, +24]
- code - random (own size): +4 [+1, +8]

Verdicts (rules in the manifest):
- interpreted: True
- jpp code parts: outside
- jpp sigma helps: False
- jlens code parts: outside
- jlens sigma helps: False
- code writes the step: True
- code writes where the J++ lens does not: True
- code at its own size writes the step: True

Diagnostics (medians over items, layers and positions):
- code norm over copy norm: 0.453
- jpp chance: 0.074
- jpp cos code~lens: 0.021
- jpp cos code~sigma_0.5: 0.027
- jpp cos code~sigma_0.0: 0.025
- jpp code jspace share: 0.090
- jlens chance: 0.070
- jlens cos code~lens: 0.024
- jlens cos code~sigma_0.5: 0.026
- jlens cos code~sigma_0.0: 0.024
- jlens code jspace share: 0.108
