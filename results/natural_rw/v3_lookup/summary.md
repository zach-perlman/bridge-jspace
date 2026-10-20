# natural_rw / v3_lookup: 91 items, layers [32, 36, 40]

| version | lens reads the city (top-10 / top-1) | a=0.05 | a=0.1 | a=0.2 | a=0.4 | a=0.8 |
|---|---|---|---|---|---|---|
| NM | 73% / 8% | 0% (17%) / 0% (0%) | 0% (35%) / 0% (0%) | 14% (70%) / 0% (0%) | 59% (132%) / 0% (1%) | 75% (228%) / 0% (6%) |
| NL | 85% / 9% | 0% (6%) / 0% (-2%) | 1% (16%) / 0% (-2%) | 8% (35%) / 0% (-1%) | 20% (68%) / 1% (-1%) | 15% (75%) / 6% (9%) |

Write cells: lens | random direction: flips (share of the clean margin closed), single layers averaged.
MX flips go to X's country as the prompt gives it; the lens's flips to X's real country, per alpha: {"0.05": 0, "0.1": 0, "0.2": 0, "0.4": 0, "0.8": 0}
