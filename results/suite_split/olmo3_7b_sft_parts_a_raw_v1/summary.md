# suite_split / olmo3_7b_sft_parts_a_raw_v1

Claims (the manifest's rules, primary measure): {"claim_1": "supported (BL outside)", "by_family": {"BL": "outside", "BR": null, "RL": "outside", "RR": null}}

## BL: window [15, 18, 21, 24, 27]

frac (n=138): lens2 -0%, lens2 null -0%, not_lens2 21%, not_lens2 null 0%, jspace 2%, jspace null -0%, not_jspace 18%, not_jspace null 0%, lens2_matched 0%, jspace_matched 2%, full 21%, O full -0%
- jspace: concentration 1.28 [1.19, 1.37]; not_jspace - jspace +15 [+14, +16]; jspace - jspace_matched +1 [+1, +1]; jspace - its null +3 [+2, +3]; not_jspace - its null +17 [+16, +18]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration -0.30 [-0.81, 0.18]; not_lens2 - lens2 +21 [+20, +22]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null -0 [-0, +0]; not_lens2 - its null +21 [+20, +22]; verdict: outside (exp09's rule: outside)

flip (n=138): lens2 0%, lens2 null 0%, not_lens2 3%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 1%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 3%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +1 [+0, +3]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +1 [+0, +3]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +3 [+1, +5]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +3 [+1, +5]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.081, jspace_wo_own 0.080, rand_omp 0.091

## BR: window []

not interpreted (empty window)

## RL: window [12, 15, 18, 21, 24, 27]

frac (n=138): lens2 0%, lens2 null 0%, not_lens2 21%, not_lens2 null 1%, jspace 2%, jspace null 0%, not_jspace 18%, not_jspace null 1%, lens2_matched 0%, jspace_matched 1%, full 21%, O full -0%
- jspace: concentration 0.90 [0.82, 0.97]; not_jspace - jspace +16 [+16, +17]; jspace - jspace_matched +0 [+0, +1]; jspace - its null +2 [+1, +2]; not_jspace - its null +18 [+17, +18]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.18 [-0.45, 0.74]; not_lens2 - lens2 +21 [+20, +22]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +20 [+19, +21]; verdict: outside (exp09's rule: outside)

flip (n=138): lens2 0%, lens2 null 0%, not_lens2 2%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 2%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 3%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +2 [+0, +3]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +2 [+0, +3]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +2 [+1, +4]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +2 [+1, +4]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.078, jspace_wo_own 0.077, rand_omp 0.091

## RR: window []

not interpreted (empty window)

Chance share (a random direction's J-space part): 0.083
