# suite_split / qwen35_122b_parts_A4_cap42_v1

Claims (the manifest's rules, primary measure): {"claim_1": "supported (BL outside)", "by_family": {"BL": "outside", "BR": "outside", "RL": "outside", "RR": "outside"}}

## BL: window [36, 39]

frac (n=100): lens2 -0%, lens2 null -0%, not_lens2 27%, not_lens2 null 1%, jspace 1%, jspace null 0%, not_jspace 23%, not_jspace null 1%, lens2_matched 0%, jspace_matched 1%, full 27%, O full -0%
- jspace: concentration 0.48 [0.32, 0.65]; not_jspace - jspace +21 [+18, +25]; jspace - jspace_matched +0 [+0, +1]; jspace - its null +1 [+1, +1]; not_jspace - its null +22 [+18, +26]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration -0.53 [-21.19, 18.10]; not_lens2 - lens2 +27 [+22, +32]; lens2 - lens2_matched -0 [-0, +0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +26 [+22, +31]; verdict: inconclusive (exp09's rule: outside)

flip (n=100): lens2 0%, lens2 null 0%, not_lens2 18%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 14%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 18%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +14 [+8, +21]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +14 [+8, +21]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +18 [+11, +25]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +18 [+11, +25]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.091

## BR: window [36, 39]

frac (n=100): lens2 1%, lens2 null 1%, not_lens2 24%, not_lens2 null 1%, jspace 2%, jspace null 1%, not_jspace 18%, not_jspace null 1%, lens2_matched 1%, jspace_matched 1%, full 25%, O full 1%
- jspace: concentration 0.78 [0.56, 1.02]; not_jspace - jspace +16 [+13, +20]; jspace - jspace_matched +1 [+1, +1]; jspace - its null +1 [+1, +2]; not_jspace - its null +17 [+14, +21]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 11.30 [4.60, 18.36]; not_lens2 - lens2 +23 [+19, +28]; lens2 - lens2_matched +0 [-0, +1]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +23 [+19, +28]; verdict: inside (exp09's rule: outside)

flip (n=100): lens2 0%, lens2 null 0%, not_lens2 18%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 10%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 18%, O full 0%
- jspace: concentration 0.28 [0.00, 0.90]; not_jspace - jspace +9 [+5, +14]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +2]; not_jspace - its null +10 [+5, +14]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +18 [+12, +25]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +18 [+12, +25]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.003, jspace 0.098

## RL: window [33, 36, 39]

frac (n=100): lens2 0%, lens2 null 0%, not_lens2 40%, not_lens2 null 2%, jspace 1%, jspace null 0%, not_jspace 36%, not_jspace null 1%, lens2_matched 0%, jspace_matched 1%, full 41%, O full 0%
- jspace: concentration 0.24 [0.14, 0.33]; not_jspace - jspace +34 [+32, +37]; jspace - jspace_matched -0 [-0, +0]; jspace - its null +1 [+0, +1]; not_jspace - its null +34 [+32, +37]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.57 [-0.01, 1.13]; not_lens2 - lens2 +40 [+38, +42]; lens2 - lens2_matched +0 [-0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +39 [+37, +41]; verdict: outside (exp09's rule: both or neither)

flip (n=100): lens2 0%, lens2 null 0%, not_lens2 41%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 34%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 44%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +34 [+29, +39]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +34 [+29, +39]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +41 [+36, +46]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +41 [+36, +46]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.013, jspace 0.110

## RR: window [36, 39]

frac (n=100): lens2 1%, lens2 null 0%, not_lens2 33%, not_lens2 null 2%, jspace 4%, jspace null 0%, not_jspace 25%, not_jspace null 1%, lens2_matched 1%, jspace_matched 1%, full 36%, O full 0%
- jspace: concentration 1.02 [0.88, 1.15]; not_jspace - jspace +20 [+18, +23]; jspace - jspace_matched +3 [+2, +3]; jspace - its null +4 [+4, +5]; not_jspace - its null +24 [+21, +27]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 1.73 [0.93, 2.57]; not_lens2 - lens2 +32 [+29, +35]; lens2 - lens2_matched +0 [+0, +1]; lens2 - its null +1 [+0, +1]; not_lens2 - its null +31 [+28, +35]; verdict: inconclusive (exp09's rule: both or neither)

flip (n=100): lens2 0%, lens2 null 0%, not_lens2 20%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 9%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 22%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +9 [+4, +14]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +9 [+4, +14]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +20 [+14, +26]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +20 [+14, +26]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.015, jspace 0.116

Chance share (a random direction's J-space part): 0.105
