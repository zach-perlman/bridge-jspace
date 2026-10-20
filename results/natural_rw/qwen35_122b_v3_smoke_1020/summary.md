# natural_rw / qwen35_122b_v3_smoke_1020: 4 items, layers [36, 39]

| version | lens reads the city (top-10 / top-1) | a=0.05 | a=0.1 | a=0.2 | a=0.4 | a=0.8 |
|---|---|---|---|---|---|---|
| NM | 50% / 25% | 0% (21%) / 0% (2%) | 0% (41%) / 0% (3%) | 25% (80%) / 0% (0%) | 75% (141%) / 0% (7%) | 88% (257%) / 0% (19%) |
| NL | 25% / 0% | 12% (25%) / 0% (-0%) | 0% (16%) / 0% (18%) | 12% (33%) / 12% (64%) | 25% (86%) / 0% (64%) | 0% (207%) / 12% (63%) |

Write cells: lens | random direction: flips (share of the clean margin closed), single layers averaged.
MX flips go to X's country as the prompt gives it; the lens's flips to X's real country, per alpha: {"0.05": 0, "0.1": 0, "0.2": 0, "0.4": 0, "0.8": 0}
