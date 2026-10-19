# suite_split / qwen35_9b_parts_B8_v1

Claims (the manifest's rules, primary measure): {"claim_1": "refuted (BL inside)", "by_family": {"BL": "inside", "BR": "outside", "RL": "outside", "RR": "outside", "BLR": "inconclusive", "BRL": "outside", "NAMES": "outside", "CODE": "outside"}, "tie_break": "mixed: BLR inconclusive, BRL outside"}

## BL: window [12, 16, 18, 20, 22, 24, 26, 28]

frac (n=150): lens2 0%, lens2 null 0%, not_lens2 35%, not_lens2 null 0%, jspace 10%, jspace null 0%, not_jspace 28%, not_jspace null 0%, lens2_matched 0%, jspace_matched 7%, full 35%, O full 0%
- jspace: concentration 2.21 [2.13, 2.30]; not_jspace - jspace +18 [+16, +19]; jspace - jspace_matched +4 [+3, +4]; jspace - its null +10 [+10, +11]; not_jspace - its null +28 [+26, +29]; verdict: inside (exp09's rule: both or neither)
- lens2: concentration 0.81 [0.23, 1.38]; not_lens2 - lens2 +35 [+34, +36]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null -0 [-0, +0]; not_lens2 - its null +35 [+34, +36]; verdict: outside (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 19%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 4%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 19%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +4 [+2, +6]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +4 [+2, +6]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +19 [+15, +23]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +19 [+15, +23]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.002, jspace 0.101

## BR: window [20, 22, 24, 26, 28]

frac (n=150): lens2 0%, lens2 null -0%, not_lens2 22%, not_lens2 null 1%, jspace 6%, jspace null 0%, not_jspace 16%, not_jspace null 0%, lens2_matched 0%, jspace_matched 2%, full 24%, O full -0%
- jspace: concentration 1.51 [1.42, 1.60]; not_jspace - jspace +11 [+10, +11]; jspace - jspace_matched +3 [+3, +4]; jspace - its null +6 [+5, +6]; not_jspace - its null +16 [+15, +17]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.39 [0.25, 0.52]; not_lens2 - lens2 +22 [+20, +23]; lens2 - lens2_matched -0 [-0, +0]; lens2 - its null +0 [+0, +1]; not_lens2 - its null +21 [+20, +23]; verdict: outside (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 0%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 0%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 0%, O full 0%
- jspace: concentration nan [nan, nan]; not_jspace - jspace +0 [+0, +0]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +0 [+0, +0]; verdict: inconclusive (exp09's rule: both or neither)
- lens2: concentration nan [nan, nan]; not_lens2 - lens2 +0 [+0, +0]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +0 [+0, +0]; verdict: inconclusive (exp09's rule: both or neither)

Median share of delta's variance: lens2 0.041, jspace 0.153

## RL: window [14, 16, 18, 20, 22, 24, 26, 28]

frac (n=150): lens2 0%, lens2 null 0%, not_lens2 42%, not_lens2 null 0%, jspace 9%, jspace null -0%, not_jspace 37%, not_jspace null 0%, lens2_matched 0%, jspace_matched 6%, full 42%, O full 0%
- jspace: concentration 1.65 [1.59, 1.71]; not_jspace - jspace +28 [+27, +29]; jspace - jspace_matched +3 [+3, +3]; jspace - its null +9 [+9, +10]; not_jspace - its null +37 [+36, +39]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.06 [-0.08, 0.18]; not_lens2 - lens2 +42 [+41, +43]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +42 [+41, +43]; verdict: outside (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 25%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 15%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 25%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +15 [+12, +18]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +15 [+12, +18]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +25 [+20, +29]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +25 [+20, +29]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.019, jspace 0.121

## RR: window [16, 18, 20, 22, 24, 26, 28]

frac (n=150): lens2 1%, lens2 null 0%, not_lens2 27%, not_lens2 null 1%, jspace 5%, jspace null 0%, not_jspace 22%, not_jspace null 0%, lens2_matched 0%, jspace_matched 2%, full 27%, O full 0%
- jspace: concentration 1.23 [1.16, 1.31]; not_jspace - jspace +18 [+16, +19]; jspace - jspace_matched +3 [+2, +3]; jspace - its null +5 [+4, +5]; not_jspace - its null +22 [+21, +23]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.52 [0.38, 0.67]; not_lens2 - lens2 +26 [+25, +28]; lens2 - lens2_matched +0 [-0, +0]; lens2 - its null +0 [+0, +1]; not_lens2 - its null +26 [+25, +28]; verdict: outside (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 3%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 1%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 3%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +1 [+0, +2]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +1 [+0, +2]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +3 [+1, +4]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +3 [+1, +4]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.035, jspace 0.146

## BLR: window [12, 14, 16, 18, 20, 22, 24, 26, 28]

frac (n=23): lens2 1%, lens2 null 1%, not_lens2 29%, not_lens2 null 2%, jspace 7%, jspace null 1%, not_jspace 23%, not_jspace null 2%, lens2_matched 1%, jspace_matched 4%, full 29%, O full 2%
- jspace: concentration 1.88 [1.63, 2.15]; not_jspace - jspace +16 [+13, +20]; jspace - jspace_matched +3 [+2, +3]; jspace - its null +5 [+4, +6]; not_jspace - its null +21 [+16, +26]; verdict: inconclusive (exp09's rule: both or neither)
- lens2: concentration 4.62 [0.85, 8.18]; not_lens2 - lens2 +28 [+23, +33]; lens2 - lens2_matched +0 [-0, +1]; lens2 - its null +0 [+0, +1]; not_lens2 - its null +27 [+22, +32]; verdict: inconclusive (exp09's rule: both or neither)

flip (n=23): lens2 0%, lens2 null 0%, not_lens2 22%, not_lens2 null 2%, jspace 6%, jspace null 0%, not_jspace 16%, not_jspace null 2%, lens2_matched 0%, jspace_matched 4%, full 22%, O full 2%
- jspace: concentration 2.36 [0.00, 4.49]; not_jspace - jspace +10 [+4, +17]; jspace - jspace_matched +2 [+0, +4]; jspace - its null +6 [+0, +14]; not_jspace - its null +14 [+5, +25]; verdict: inconclusive (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +22 [+9, +35]; lens2 - lens2_matched -0 [-1, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +19 [+9, +32]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.003, jspace 0.110

## BRL: window [12, 14, 16, 18, 20, 22, 24, 26, 28]

frac (n=23): lens2 1%, lens2 null 1%, not_lens2 39%, not_lens2 null 1%, jspace 7%, jspace null 1%, not_jspace 34%, not_jspace null 2%, lens2_matched 1%, jspace_matched 5%, full 39%, O full 1%
- jspace: concentration 1.34 [1.10, 1.59]; not_jspace - jspace +27 [+24, +29]; jspace - jspace_matched +3 [+2, +3]; jspace - its null +6 [+6, +7]; not_jspace - its null +32 [+30, +35]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 0.84 [0.05, 1.81]; not_lens2 - lens2 +38 [+35, +42]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null +0 [-0, +0]; not_lens2 - its null +38 [+35, +41]; verdict: outside (exp09's rule: outside)

flip (n=23): lens2 0%, lens2 null 0%, not_lens2 30%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 21%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 32%, O full 0%
- jspace: concentration 0.00 [0.00, 0.00]; not_jspace - jspace +21 [+10, +32]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +21 [+10, +32]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +30 [+16, +45]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +30 [+16, +45]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.017, jspace 0.131

## NAMES: window [16, 18, 20, 22]

frac (n=150): lens2 0%, lens2 null 0%, not_lens2 40%, not_lens2 null 0%, jspace 4%, jspace null 0%, not_jspace 35%, not_jspace null -0%, lens2_matched 0%, jspace_matched 3%, full 40%, O full 0%
- jspace: concentration 1.06 [0.98, 1.15]; not_jspace - jspace +32 [+28, +35]; jspace - jspace_matched +0 [+0, +1]; jspace - its null +4 [+3, +4]; not_jspace - its null +36 [+32, +39]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration 2.62 [-1.11, 6.34]; not_lens2 - lens2 +40 [+36, +43]; lens2 - lens2_matched +0 [-0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +40 [+36, +43]; verdict: inconclusive (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 37%, not_lens2 null 1%, jspace 0%, jspace null 0%, not_jspace 31%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 37%, O full 1%
- jspace: concentration 0.16 [0.00, 0.54]; not_jspace - jspace +30 [+24, +37]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [-0, +2]; not_jspace - its null +30 [+24, +37]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +37 [+30, +44]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +36 [+29, +43]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.001, jspace 0.084

## CODE: window [20, 22, 24, 26, 28]

frac (n=150): lens2 -0%, lens2 null -0%, not_lens2 21%, not_lens2 null -0%, jspace 6%, jspace null -0%, not_jspace 16%, not_jspace null -0%, lens2_matched -0%, jspace_matched 3%, full 21%, O full 0%
- jspace: concentration 1.73 [1.63, 1.82]; not_jspace - jspace +10 [+9, +11]; jspace - jspace_matched +2 [+2, +3]; jspace - its null +6 [+5, +7]; not_jspace - its null +16 [+15, +18]; verdict: outside (exp09's rule: both or neither)
- lens2: concentration -1.26 [-2.48, -0.07]; not_lens2 - lens2 +22 [+20, +23]; lens2 - lens2_matched -0 [-0, -0]; lens2 - its null -0 [-0, -0]; not_lens2 - its null +22 [+20, +23]; verdict: outside (exp09's rule: outside)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 6%, not_lens2 null 0%, jspace 2%, jspace null 0%, not_jspace 4%, not_jspace null 0%, lens2_matched 0%, jspace_matched 1%, full 7%, O full 1%
- jspace: concentration 1.51 [0.48, 2.46]; not_jspace - jspace +2 [+1, +4]; jspace - jspace_matched +1 [+0, +2]; jspace - its null +2 [+0, +3]; not_jspace - its null +4 [+1, +7]; verdict: inconclusive (exp09's rule: both or neither)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +6 [+3, +9]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +6 [+3, +9]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.005, jspace 0.157

Chance share (a random direction's J-space part): 0.093
