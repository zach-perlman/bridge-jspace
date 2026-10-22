# suite_split / olmo3_7b_dpo_parts_a_raw_v1

Claims (the manifest's rules, primary measure): {"claim_1": "supported (BL outside)", "by_family": {"BL": "outside", "BR": null, "RL": "outside", "RR": "outside"}}

## BL: window [15, 18, 21, 24, 27]

frac (n=150): lens2 0%, lens2 null 0%, not_lens2 18%, not_lens2 null 1%, jspace 2%, jspace null 0%, not_jspace 15%, not_jspace null 0%, lens2_matched 0%, jspace_matched 1%, full 18%, O full 0%
- jspace: concentration 1.14 [1.05, 1.24]; not_jspace - jspace +13 [+12, +14]; jspace - jspace_matched +1 [+1, +1]; jspace - its null +2 [+2, +2]; not_jspace - its null +14 [+13, +15]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.74 [0.04, 1.47]; not_lens2 - lens2 +18 [+17, +19]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +17 [+16, +19]; verdict: outside (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 3%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 2%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 3%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +2 [+1, +4]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +2 [+1, +4]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +3 [+1, +5]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +3 [+1, +5]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.079, jspace_wo_own 0.079, rand_omp 0.091

## BR: window []

not interpreted (empty window)

## RL: window [12, 15, 18, 21, 24, 27]

frac (n=150): lens2 -0%, lens2 null 0%, not_lens2 17%, not_lens2 null 1%, jspace 1%, jspace null 0%, not_jspace 15%, not_jspace null 1%, lens2_matched 0%, jspace_matched 1%, full 17%, O full 0%
- jspace: concentration 0.74 [0.67, 0.82]; not_jspace - jspace +14 [+13, +15]; jspace - jspace_matched +0 [+0, +1]; jspace - its null +1 [+1, +1]; not_jspace - its null +14 [+13, +15]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration -0.05 [-0.80, 0.73]; not_lens2 - lens2 +17 [+16, +18]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null -0 [-0, +0]; not_lens2 - its null +16 [+15, +17]; verdict: outside (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 2%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 2%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 2%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +2 [+0, +3]; jspace - jspace_matched -0 [-0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +2 [+0, +3]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +2 [+1, +4]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +2 [+1, +3]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.078, jspace_wo_own 0.078, rand_omp 0.091

## RR: window [12]

frac (n=150): lens2 0%, lens2 null 0%, not_lens2 14%, not_lens2 null 0%, jspace 1%, jspace null 0%, not_jspace 8%, not_jspace null 1%, lens2_matched 0%, jspace_matched 0%, full 13%, O full 0%
- jspace: concentration 0.53 [0.34, 0.77]; not_jspace - jspace +7 [+5, +10]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +1 [+0, +1]; not_jspace - its null +7 [+5, +10]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 6.71 [-8.15, 20.11]; not_lens2 - lens2 +13 [+10, +17]; lens2 - lens2_matched -0 [-0, +0]; lens2 - its null -0 [-0, +0]; not_lens2 - its null +13 [+9, +17]; verdict: inconclusive (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 11%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 5%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 10%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +5 [+2, +9]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +5 [+2, +9]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +11 [+6, +16]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +11 [+6, +16]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.077, jspace_wo_own 0.077, rand_omp 0.091

Chance share (a random direction's J-space part): 0.083
