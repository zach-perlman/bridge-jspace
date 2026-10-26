# T: the pointer directions beyond simple scenes (batch 42)

Extra loss without the pointer directions minus without a random part of their share; cluster bootstrap over bridge entities (10000 resamples). Natural: passages whose original fact sentence comes before the bridge's mention. UNVERIFIED.

| model | scenes | n | lookup switches (whole) | lookup extra loss | recall extra loss |
|---|---|---|---|---|---|
| qwen3.5-9b | natural | – | – | not tested (stopped at its gate) | – |
| qwen3.5-9b | pooled | 1010 | 796 | 0.11 [0.08, 0.13] | 0.02 [0.01, 0.03] |
| qwen3.5-9b | json + table | 545 | 448 | 0.06 [0.03, 0.09] | 0.01 [-0.00, 0.02] |
| qwen3.5-9b | prose | 465 | 348 | 0.16 [0.13, 0.20] | 0.03 [0.02, 0.06] |
| qwen3.5-9b | json | 113 | 85 | 0.02 [-0.04, 0.08] | 0.01 [-0.03, 0.06] |
| qwen3.5-9b | table | 432 | 363 | 0.07 [0.04, 0.10] | 0.01 [-0.00, 0.02] |
| qwen3.6-27b | pooled | 1635 | 1082 | 0.05 [0.04, 0.06] | 0.02 [0.00, 0.04] |
| qwen3.6-27b | json + table | 894 | 639 | 0.02 [0.01, 0.03] | 0.02 [-0.00, 0.04] |
| qwen3.6-27b | prose | 741 | 443 | 0.09 [0.07, 0.12] | 0.03 [0.00, 0.06] |
| qwen3.6-27b | json | 233 | 167 | 0.01 [-0.02, 0.02] | 0.02 [-0.01, 0.05] |
| qwen3.6-27b | table | 661 | 472 | 0.03 [0.02, 0.04] | 0.02 [-0.00, 0.04] |
| qwen3.6-27b | natural | 75 | 54 | 0.07 [0.00, 0.18] | 0.03 [0.00, 0.07] |
| qwen3.5-122b-a10b | pooled | 1552 | 1181 | 0.06 [0.04, 0.07] | 0.01 [0.00, 0.03] |
| qwen3.5-122b-a10b | json + table | 861 | 669 | 0.04 [0.02, 0.07] | 0.02 [0.00, 0.03] |
| qwen3.5-122b-a10b | prose | 691 | 512 | 0.07 [0.05, 0.10] | 0.01 [-0.00, 0.03] |
| qwen3.5-122b-a10b | json | 221 | 173 | 0.06 [0.01, 0.11] | 0.05 [0.01, 0.09] |
| qwen3.5-122b-a10b | table | 640 | 496 | 0.04 [0.02, 0.06] | 0.01 [-0.01, 0.02] |
| qwen3.5-122b-a10b | natural | 57 | 46 | 0.07 [-0.02, 0.16] | 0.02 [0.00, 0.06] |
| muse-glimmer-30b | varied | – | – | not landed | – |
| muse-glimmer-30b | natural | – | – | not landed | – |

Q42.1: bar 0.2; passed none of 3 tested -> (d) none (not all models landed).
Q42.2: bar 0.15; passed none of 3 tested -> (d) none (not all models landed).
Q42.3: bar 0.15; passed none of 2 tested -> (d) none (not all models landed).
