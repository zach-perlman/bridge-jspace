# suite_split / qwen35_9b_parts_A8_v1

Claims (the manifest's rules, primary measure): {"claim_1": "supported (BL outside)", "by_family": {"BL": "outside", "BR": "outside", "RL": "outside", "RR": "outside", "BLR": "outside", "BRL": "outside", "NAMES": "outside", "CODE": "outside"}, "tie_break": "mixed: BLR outside, BRL outside"}

## BL: window [12, 16, 18, 20, 22, 24, 26, 28]

frac (n=150): lens2 0%, lens2 null 0%, not_lens2 37%, not_lens2 null 0%, jspace 10%, jspace null 0%, not_jspace 30%, not_jspace null 0%, lens2_matched 0%, jspace_matched 6%, full 37%, O full 1%
- jspace: concentration 1.88 [1.80, 1.96]; not_jspace - jspace +20 [+19, +21]; jspace - jspace_matched +4 [+3, +4]; jspace - its null +9 [+9, +10]; not_jspace - its null +29 [+28, +31]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.30 [0.05, 0.57]; not_lens2 - lens2 +37 [+35, +38]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +37 [+35, +38]; verdict: outside (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 21%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 4%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 21%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +4 [+3, +6]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +4 [+3, +6]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +21 [+17, +25]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +21 [+17, +25]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.003, jspace 0.103

## BR: window [16, 20, 22, 24, 26, 28]

frac (n=150): lens2 1%, lens2 null 0%, not_lens2 22%, not_lens2 null 1%, jspace 6%, jspace null 0%, not_jspace 17%, not_jspace null 1%, lens2_matched 1%, jspace_matched 3%, full 23%, O full 0%
- jspace: concentration 1.64 [1.53, 1.75]; not_jspace - jspace +11 [+10, +12]; jspace - jspace_matched +3 [+3, +4]; jspace - its null +6 [+5, +6]; not_jspace - its null +16 [+14, +18]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.73 [0.57, 0.88]; not_lens2 - lens2 +21 [+19, +23]; lens2 - lens2_matched +0 [-0, +0]; lens2 - its null +1 [+0, +1]; not_lens2 - its null +21 [+19, +23]; verdict: outside (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 4%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 3%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 4%, O full 0%
- jspace: concentration 0.52 [0.00, 1.40]; not_jspace - jspace +2 [+1, +4]; jspace - jspace_matched +0 [+0, +1]; jspace - its null +0 [+0, +1]; not_jspace - its null +3 [+1, +5]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +4 [+2, +6]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +4 [+2, +6]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.039, jspace 0.155

## RL: window [14, 16, 18, 20, 22, 24, 26, 28]

frac (n=150): lens2 0%, lens2 null 0%, not_lens2 46%, not_lens2 null 0%, jspace 10%, jspace null 0%, not_jspace 41%, not_jspace null 0%, lens2_matched 0%, jspace_matched 7%, full 46%, O full 1%
- jspace: concentration 1.49 [1.42, 1.55]; not_jspace - jspace +31 [+30, +32]; jspace - jspace_matched +3 [+3, +4]; jspace - its null +10 [+9, +10]; not_jspace - its null +41 [+39, +42]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.14 [0.07, 0.22]; not_lens2 - lens2 +46 [+45, +47]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +46 [+45, +47]; verdict: outside (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 34%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 19%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 35%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +19 [+16, +22]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +19 [+16, +22]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +34 [+29, +39]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +34 [+29, +39]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.025, jspace 0.134

## RR: window [14, 16, 18, 20, 22, 24, 26, 28]

frac (n=150): lens2 0%, lens2 null -0%, not_lens2 26%, not_lens2 null 1%, jspace 4%, jspace null 0%, not_jspace 22%, not_jspace null 0%, lens2_matched 0%, jspace_matched 2%, full 26%, O full 0%
- jspace: concentration 1.26 [1.17, 1.34]; not_jspace - jspace +17 [+16, +19]; jspace - jspace_matched +3 [+2, +3]; jspace - its null +4 [+4, +5]; not_jspace - its null +21 [+19, +23]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.53 [0.36, 0.70]; not_lens2 - lens2 +25 [+23, +27]; lens2 - lens2_matched +0 [-0, +0]; lens2 - its null +0 [+0, +1]; not_lens2 - its null +25 [+23, +27]; verdict: outside (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 4%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 2%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 4%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +2 [+1, +4]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +2 [+1, +4]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +4 [+2, +5]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +4 [+2, +5]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.025, jspace 0.134

## BLR: window [12, 16, 18, 20, 22, 24, 26, 28]

frac (n=136): lens2 0%, lens2 null 0%, not_lens2 27%, not_lens2 null 1%, jspace 5%, jspace null 0%, not_jspace 22%, not_jspace null 1%, lens2_matched 0%, jspace_matched 2%, full 27%, O full 0%
- jspace: concentration 1.42 [1.31, 1.54]; not_jspace - jspace +17 [+15, +18]; jspace - jspace_matched +2 [+2, +3]; jspace - its null +5 [+4, +5]; not_jspace - its null +21 [+19, +22]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.58 [-0.28, 1.45]; not_lens2 - lens2 +27 [+25, +28]; lens2 - lens2_matched +0 [-0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +26 [+24, +28]; verdict: outside (exp09's rule: both or neither)

flip (n=136): lens2 0%, lens2 null 0%, not_lens2 9%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 7%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 9%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +7 [+5, +9]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +7 [+5, +9]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +9 [+7, +12]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +9 [+7, +12]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.005, jspace 0.117

## BRL: window [12, 14, 16, 18, 20, 22, 24, 26, 28]

frac (n=136): lens2 0%, lens2 null 0%, not_lens2 34%, not_lens2 null 0%, jspace 6%, jspace null -0%, not_jspace 29%, not_jspace null 0%, lens2_matched 0%, jspace_matched 4%, full 34%, O full -1%
- jspace: concentration 1.25 [1.14, 1.35]; not_jspace - jspace +23 [+22, +24]; jspace - jspace_matched +2 [+1, +2]; jspace - its null +6 [+5, +6]; not_jspace - its null +29 [+27, +30]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.08 [-0.41, 0.56]; not_lens2 - lens2 +34 [+32, +35]; lens2 - lens2_matched -0 [-0, +0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +34 [+32, +35]; verdict: outside (exp09's rule: outside)

flip (n=136): lens2 0%, lens2 null 0%, not_lens2 29%, not_lens2 null 0%, jspace 2%, jspace null 0%, not_jspace 24%, not_jspace null 1%, lens2_matched 0%, jspace_matched 2%, full 29%, O full 0%
- jspace: concentration 0.46 [0.09, 0.94]; not_jspace - jspace +23 [+18, +28]; jspace - jspace_matched +0 [-0, +1]; jspace - its null +1 [+0, +3]; not_jspace - its null +24 [+19, +29]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.30 [0.00, 1.01]; not_lens2 - lens2 +29 [+23, +35]; lens2 - lens2_matched -0 [-1, +0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +29 [+23, +35]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.011, jspace 0.117

## NAMES: window [16, 18, 20, 22, 24, 26]

frac (n=150): lens2 0%, lens2 null -0%, not_lens2 55%, not_lens2 null -0%, jspace 8%, jspace null -0%, not_jspace 45%, not_jspace null -0%, lens2_matched 0%, jspace_matched 6%, full 55%, O full -0%
- jspace: concentration 1.22 [1.16, 1.28]; not_jspace - jspace +37 [+35, +39]; jspace - jspace_matched +2 [+2, +2]; jspace - its null +8 [+8, +9]; not_jspace - its null +45 [+43, +48]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.25 [-0.01, 0.50]; not_lens2 - lens2 +55 [+52, +57]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +55 [+53, +57]; verdict: outside (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 58%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 41%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 59%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +41 [+35, +47]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +41 [+35, +47]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +58 [+54, +63]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +58 [+54, +63]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.005, jspace 0.107

## CODE: window [20, 22, 24, 26, 28]

frac (n=36): lens2 -1%, lens2 null -0%, not_lens2 18%, not_lens2 null -1%, jspace 5%, jspace null -0%, not_jspace 14%, not_jspace null -1%, lens2_matched -0%, jspace_matched 3%, full 19%, O full -1%
- jspace: concentration 1.70 [1.36, 1.99]; not_jspace - jspace +9 [+7, +10]; jspace - jspace_matched +2 [+1, +2]; jspace - its null +5 [+4, +7]; not_jspace - its null +14 [+12, +17]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration -2.26 [-6.89, 1.77]; not_lens2 - lens2 +19 [+16, +22]; lens2 - lens2_matched -0 [-0, +0]; lens2 - its null -0 [-0, +0]; not_lens2 - its null +19 [+16, +22]; verdict: outside (exp09's rule: outside)

flip (n=36): lens2 0%, lens2 null 0%, not_lens2 4%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 3%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 4%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +3 [+0, +8]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +3 [+0, +8]; verdict: inconclusive (exp09's rule: both or neither)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +4 [+0, +12]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +4 [+0, +12]; verdict: inconclusive (exp09's rule: both or neither)

Median share of delta's variance: lens2 0.003, jspace 0.148

Chance share (a random direction's J-space part): 0.093
