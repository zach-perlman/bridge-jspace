# suite_split / parts_C3_cal_v1

Claims (the manifest's rules, primary measure): {}

## ARITH: window []

not interpreted (empty window)

## TYPO: window [24, 28, 32, 36, 40]

frac (n=133): lens2 3%, lens2 null 0%, not_lens2 24%, not_lens2 null 1%, jspace 12%, jspace null 0%, not_jspace 14%, not_jspace null 1%, lens2_matched 1%, jspace_matched 2%, full 32%, O full 0%
- jspace: concentration 2.62 [2.38, 2.88]; not_jspace - jspace +3 [+1, +4]; jspace - jspace_matched +9 [+8, +10]; jspace - its null +11 [+10, +12]; not_jspace - its null +13 [+12, +14]; verdict: inside (exp09's rule: both or neither)
- lens2: concentration 3.09 [2.64, 3.57]; not_lens2 - lens2 +21 [+19, +23]; lens2 - lens2_matched +3 [+2, +3]; lens2 - its null +3 [+3, +4]; not_lens2 - its null +23 [+21, +25]; verdict: inside (exp09's rule: both or neither)

flip (n=133): lens2 0%, lens2 null 0%, not_lens2 10%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 3%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 17%, O full 0%
- jspace: concentration 0.13 [0.00, 0.31]; not_jspace - jspace +2 [+1, +5]; jspace - jspace_matched +0 [+0, +1]; jspace - its null +0 [+0, +1]; not_jspace - its null +3 [+1, +5]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +10 [+6, +13]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +10 [+6, +13]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.033, jspace 0.132, jspace_wo_own 0.100, rand_omp 0.082

## TRANS: window [28, 32, 36, 40]

frac (n=150): lens2 1%, lens2 null 0%, not_lens2 18%, not_lens2 null 0%, jspace 7%, jspace null 0%, not_jspace 10%, not_jspace null 0%, lens2_matched 0%, jspace_matched 2%, full 23%, O full 0%
- jspace: concentration 2.26 [2.05, 2.49]; not_jspace - jspace +3 [+2, +4]; jspace - jspace_matched +5 [+5, +6]; jspace - its null +7 [+6, +7]; not_jspace - its null +10 [+9, +11]; verdict: inside (exp09's rule: both or neither)
- lens2: concentration 2.13 [1.88, 2.42]; not_lens2 - lens2 +17 [+15, +18]; lens2 - lens2_matched +1 [+1, +1]; lens2 - its null +1 [+1, +2]; not_lens2 - its null +18 [+16, +19]; verdict: inconclusive (exp09's rule: both or neither)

flip (n=150): lens2 0%, lens2 null 0%, not_lens2 5%, not_lens2 null 0%, jspace 0%, jspace null 0%, not_jspace 1%, not_jspace null 0%, lens2_matched 0%, jspace_matched 0%, full 10%, O full 0%
- jspace: concentration 0.12 [0.00, 0.39]; not_jspace - jspace +1 [+0, +1]; jspace - jspace_matched +0 [+0, +0]; jspace - its null +0 [+0, +0]; not_jspace - its null +1 [+0, +2]; verdict: outside (exp09's rule: outside)
- lens2: concentration 0.00 [0.00, 0.00]; not_lens2 - lens2 +5 [+3, +7]; lens2 - lens2_matched +0 [+0, +0]; lens2 - its null +0 [+0, +0]; not_lens2 - its null +5 [+3, +7]; verdict: outside (exp09's rule: outside)

Median share of delta's variance: lens2 0.027, jspace 0.134, jspace_wo_own 0.106, rand_omp 0.082

Chance share (a random direction's J-space part): 0.067
