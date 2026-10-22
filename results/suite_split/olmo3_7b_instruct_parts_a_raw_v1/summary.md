# suite_split / olmo3_7b_instruct_parts_a_raw_v1

Claims (the manifest's rules, primary measure): {"claim_1": "supported (BL outside)", "by_family": {"BL": "outside", "BR": null, "RL": "outside", "RR": "outside"}}

## BL: window [15, 18, 21, 24, 27]

frac (n=150): lens2 -0%, lens2 null -0%, not_lens2 20%, not_lens2 null 0%, jspace 2%, jspace null -0%, not_jspace 16%, not_jspace null 0%, lens2_matched 0%, jspace_matched 1%, full 20%, O full 0%
- jspace: concentration 1.15 [1.05, 1.25]; not_jspace - jspace +14 [+13, +15]; jspace - jspace_matched +1 [+1, +1]; jspace - its null +2 [+2, +2]; not_jspace - its null +16 [+14, +17]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration -0.50 [-1.30, 0.36]; not_lens2 - lens2 +20 [+18, +21]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +19 [+18, +21]; verdict: outside (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 4%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 3%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 5%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +3 [+1, +5]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +3 [+1, +5]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +4 [+2, +7]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +4 [+2, +7]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.079, jspace_wo_own 0.079, rand_omp 0.091

## BR: window []

not interpreted (empty window)

## RL: window [12, 15, 18, 21, 24, 27]

frac (n=150): lens2 0%, lens2 null -0%, not_lens2 18%, not_lens2 null 1%, jspace 1%, jspace null 0%, not_jspace 16%, not_jspace null 1%, lens2_matched 0%, jspace_matched 1%, full 18%, O full 0%
- jspace: concentration 0.76 [0.69, 0.83]; not_jspace - jspace +15 [+14, +16]; jspace - jspace_matched +0 [+0, +1]; jspace - its null +1 [+1, +1]; not_jspace - its null +15 [+15, +16]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.02 [-0.73, 0.81]; not_lens2 - lens2 +18 [+17, +19]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +18 [+17, +19]; verdict: outside (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 3%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 2%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 3%, O full 0%
- jspace: concentration 0.42 [0.00, 1.03]; not_jspace - jspace +2 [+1, +4]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +2 [+1, +4]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +3 [+2, +5]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +3 [+2, +5]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.079, jspace_wo_own 0.078, rand_omp 0.091

## RR: window [12]

frac (n=150): lens2 0%, lens2 null 0%, not_lens2 13%, not_lens2 null 0%, jspace 1%, jspace null 0%, not_jspace 8%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 13%, O full 0%
- jspace: concentration 0.55 [0.35, 0.80]; not_jspace - jspace +7 [+5, +10]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +1 [+0, +1]; not_jspace - its null +7 [+5, +10]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 7.71 [-4.85, 20.95]; not_lens2 - lens2 +13 [+9, +17]; lens2 - lens2_matched -0 [-0, +0]; lens2 - its null -0 [-0, +0]; not_lens2 - its null +13 [+9, +17]; verdict: inconclusive (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 7%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 4%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 9%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +4 [+1, +7]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +4 [+1, +7]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +7 [+4, +12]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +7 [+4, +12]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.077, jspace_wo_own 0.077, rand_omp 0.091

Chance share (a random direction's J-space part): 0.083
