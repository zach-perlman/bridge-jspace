# natural_rw / v3_smoke_1020: 4 items, layers [32, 36, 40]

| version | lens reads the city (top-10 / top-1) | a=0.05 | a=0.1 | a=0.2 | a=0.4 | a=0.8 |
|---|---|---|---|---|---|---|
| NM | 100% / 25% | 0% (26%) / 0% (0%) | 0% (52%) / 0% (1%) | 33% (101%) / 0% (1%) | 50% (197%) / 0% (-4%) | 100% (272%) / 0% (22%) |
| NL | 100% / 25% | 0% (3%) / 0% (-2%) | 0% (9%) / 0% (-4%) | 0% (27%) / 0% (-4%) | 8% (44%) / 0% (0%) | 0% (40%) / 0% (-4%) |

Write cells: lens | random direction: flips (share of the clean margin closed), single layers averaged.
MX flips go to X's country as the prompt gives it; the lens's flips to X's real country, per alpha: {"0.05": 0, "0.1": 0, "0.2": 0, "0.4": 0, "0.8": 0}
