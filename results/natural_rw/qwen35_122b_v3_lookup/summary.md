# natural_rw / qwen35_122b_v3_lookup: 67 items, layers [36, 39]

| version | lens reads the city (top-10 / top-1) | a=0.05 | a=0.1 | a=0.2 | a=0.4 | a=0.8 |
|---|---|---|---|---|---|---|
| NM | 55% / 25% | 0% (11%) / 0% (-1%) | 1% (26%) / 0% (-1%) | 7% (56%) / 0% (-1%) | 49% (127%) / 0% (2%) | 71% (248%) / 0% (6%) |
| NL | 33% / 9% | 2% (1%) / 1% (93278%) | 3% (3%) / 4% (-93283%) | 2% (-373125%) / 1% (-279853%) | 6% (-1679082%) / 4% (-93280%) | 6% (-4477574%) / 5% (-1585821%) |

Write cells: lens | random direction: flips (share of the clean margin closed), single layers averaged.
MX flips go to X's country as the prompt gives it; the lens's flips to X's real country, per alpha: {"0.05": 0, "0.1": 0, "0.2": 0, "0.4": 0, "0.8": 0}
