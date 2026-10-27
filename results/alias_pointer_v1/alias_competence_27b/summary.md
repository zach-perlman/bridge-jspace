| file | statements | question | n | org prompt | alt prompt | control: same entity, reshuffled | control: answer digit changed | step: cue → entity | step: lookup or fact alone | step: other form → English name | eligible | median p | read = greedy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| main/animals_RL_e5f0 | statements in English | memory → prompt | 200 | 98% [96,99] | 100% [97,100] | 99% [96,100] | 98% [96,99] | 100% [97,100] | 100% [98,100] | - | 195 | 0.997 | 100.0% |
| main/animals_DL_e5f0 | statements in English | named → prompt | 200 | 100% [98,100] | 100% [98,100] | 100% [98,100] | 100% [98,100] | - | - | - | 200 | 0.999 | 100.0% |
| main/animals_RR_e5f0 | statements in English | memory → memory | 200 | 100% [98,100] | 100% [98,100] | 100% [98,100] | 100% [98,100] | 100% [97,100] | 100% [98,100] | - | 199 | 0.994 | 100.0% |
| main/animals_RL_e5f0-xlang | statements in French/Spanish/German | memory → prompt | 200 | 96% [92,98] | 98% [94,99] | 94% [90,97] | 96% [92,98] | 86% [80,90] | 98% [96,99] | 90% [85,93] | 139 | 0.990 | 86.4% |
| main/animals_DL_e5f0-xlang | statements in French/Spanish/German | named → prompt | 200 | 98% [96,99] | 99% [96,100] | 99% [96,100] | 100% [98,100] | - | - | 90% [85,93] | 175 | 0.984 | 98.0% |
| main/animals_RR_e5f0-xlang | statements in French/Spanish/German | memory → memory | 200 | 100% [98,100] | 100% [98,100] | 100% [98,100] | 100% [98,100] | 86% [80,90] | 100% [98,100] | - | 171 | 0.983 | 85.8% |
| main/elements_RL_e5f0 | statements in English | memory → prompt | 200 | 96% [92,98] | 92% [87,95] | 94% [89,96] | 96% [93,98] | 100% [98,100] | 100% [98,100] | - | 163 | 0.941 | 100.0% |
| main/elements_DL_e5f0 | statements in English | named → prompt | 200 | 100% [98,100] | 100% [98,100] | 100% [98,100] | 100% [98,100] | - | - | - | 200 | 0.998 | 100.0% |
| main/elements_RR_e5f0 | statements in English | memory → memory | 200 | 100% [98,100] | 100% [98,100] | 100% [98,100] | 100% [98,100] | 100% [98,100] | 100% [98,100] | - | 200 | 0.980 | 100.0% |
| main/elements_RL_e5f0-syn | statements with the chemical symbol | memory → prompt | 200 | 52% [45,58] | 46% [40,53] | 48% [42,55] | 52% [46,59] | 86% [81,91] | 100% [97,100] | 100% [98,100] | 23 | 0.307 | 98.9% |
| main/elements_DL_e5f0-syn | statements with the chemical symbol | named → prompt | 200 | 100% [97,100] | 96% [93,98] | 98% [94,99] | 100% [97,100] | - | - | 100% [98,100] | 187 | 0.995 | 99.9% |
| main/elements_RR_e5f0-syn | statements with the chemical symbol | memory → memory | 200 | 100% [98,100] | 100% [98,100] | 100% [97,100] | 100% [98,100] | 86% [81,91] | 100% [98,100] | - | 173 | 0.930 | 100.0% |
| dev/animals_RL_e3f0 | statements in English | memory → prompt | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | - | 60 | 0.995 | 100.0% |
| dev/animals_DL_e3f0 | statements in English | named → prompt | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | - | - | - | 60 | 0.998 | 100.0% |
| dev/animals_RR_e3f0 | statements in English | memory → memory | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | - | 60 | 0.993 | 100.0% |
| dev/animals_RL_e3f0-xlang | statements in French/Spanish/German | memory → prompt | 60 | 100% [94,100] | 100% [94,100] | 98% [91,100] | 100% [94,100] | 83% [72,91] | 98% [91,100] | 68% [56,79] | 32 | 0.988 | 84.3% |
| dev/animals_DL_e3f0-xlang | statements in French/Spanish/German | named → prompt | 60 | 98% [91,100] | 100% [94,100] | 100% [94,100] | 98% [91,100] | - | - | 68% [56,79] | 40 | 0.981 | 93.7% |
| dev/animals_RR_e3f0-xlang | statements in French/Spanish/German | memory → memory | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 83% [72,91] | 100% [94,100] | - | 50 | 0.973 | 86.9% |
| dev/elements_RL_e3f0 | statements in English | memory → prompt | 60 | 92% [82,96] | 90% [80,95] | 98% [91,100] | 93% [84,97] | 100% [94,100] | 100% [94,100] | - | 49 | 0.971 | 100.0% |
| dev/elements_DL_e3f0 | statements in English | named → prompt | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | - | - | - | 60 | 0.997 | 100.0% |
| dev/elements_RR_e3f0 | statements in English | memory → memory | 60 | 100% [94,100] | 98% [91,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | - | 59 | 0.984 | 100.0% |
| dev/elements_RL_e3f0-syn | statements with the chemical symbol | memory → prompt | 60 | 47% [35,59] | 35% [24,48] | 52% [39,64] | 43% [32,56] | 95% [86,98] | 98% [91,100] | 100% [94,100] | 5 | 0.373 | 99.0% |
| dev/elements_DL_e3f0-syn | statements with the chemical symbol | named → prompt | 60 | 98% [91,100] | 98% [91,100] | 98% [91,100] | 98% [91,100] | - | - | 100% [94,100] | 57 | 0.983 | 100.0% |
| dev/elements_RR_e3f0-syn | statements with the chemical symbol | memory → memory | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 95% [86,98] | 100% [94,100] | - | 57 | 0.927 | 100.0% |
| dev/animals_RL_e5f0 | statements in English | memory → prompt | 60 | 95% [86,98] | 98% [91,100] | 95% [86,98] | 95% [86,98] | 98% [91,100] | 100% [94,100] | - | 56 | 0.997 | 100.0% |
| dev/animals_DL_e5f0 | statements in English | named → prompt | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | - | - | - | 60 | 0.999 | 100.0% |
| dev/animals_RR_e5f0 | statements in English | memory → memory | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 98% [91,100] | 100% [94,100] | - | 59 | 0.994 | 100.0% |
| dev/animals_RL_e5f0-xlang | statements in French/Spanish/German | memory → prompt | 60 | 97% [89,99] | 98% [91,100] | 95% [86,98] | 95% [86,98] | 85% [74,92] | 100% [94,100] | 92% [82,96] | 44 | 0.991 | 86.4% |
| dev/animals_DL_e5f0-xlang | statements in French/Spanish/German | named → prompt | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 97% [89,99] | - | - | 92% [82,96] | 54 | 0.987 | 98.3% |
| dev/animals_RR_e5f0-xlang | statements in French/Spanish/German | memory → memory | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 85% [74,92] | 100% [94,100] | - | 51 | 0.982 | 85.8% |
| dev/elements_RL_e5f0 | statements in English | memory → prompt | 60 | 100% [94,100] | 93% [84,97] | 90% [80,95] | 98% [91,100] | 100% [94,100] | 100% [94,100] | - | 49 | 0.917 | 100.0% |
| dev/elements_DL_e5f0 | statements in English | named → prompt | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | - | - | - | 60 | 0.998 | 100.0% |
| dev/elements_RR_e5f0 | statements in English | memory → memory | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | - | 60 | 0.974 | 100.0% |
| dev/elements_RL_e5f0-syn | statements with the chemical symbol | memory → prompt | 60 | 45% [33,58] | 57% [44,68] | 58% [46,70] | 55% [42,67] | 88% [78,94] | 98% [91,100] | 100% [94,100] | 10 | 0.297 | 99.3% |
| dev/elements_DL_e5f0-syn | statements with the chemical symbol | named → prompt | 60 | 98% [91,100] | 98% [91,100] | 100% [94,100] | 98% [91,100] | - | - | 100% [94,100] | 58 | 0.995 | 100.0% |
| dev/elements_RR_e5f0-syn | statements with the chemical symbol | memory → memory | 60 | 100% [94,100] | 100% [94,100] | 100% [94,100] | 100% [94,100] | 88% [78,94] | 100% [94,100] | - | 53 | 0.929 | 100.0% |

Paired by scene (base prompt right): both / English only / other form only / neither

- dev/animals/e3f0-xlang: 60 scenes, 32 eligible in both conditions; memory → prompt: 60 / 0 / 0 / 0; named → prompt: 59 / 1 / 0 / 0; memory → memory: 60 / 0 / 0 / 0
- dev/animals/e5f0-xlang: 60 scenes, 39 eligible in both conditions; memory → prompt: 55 / 2 / 3 / 0; named → prompt: 60 / 0 / 0 / 0; memory → memory: 60 / 0 / 0 / 0
- dev/elements/e3f0-syn: 60 scenes, 5 eligible in both conditions; memory → prompt: 26 / 29 / 2 / 3; named → prompt: 59 / 1 / 0 / 0; memory → memory: 60 / 0 / 0 / 0
- dev/elements/e5f0-syn: 60 scenes, 10 eligible in both conditions; memory → prompt: 27 / 33 / 0 / 0; named → prompt: 59 / 1 / 0 / 0; memory → memory: 60 / 0 / 0 / 0
- main/animals/e5f0-xlang: 200 scenes, 136 eligible in both conditions; memory → prompt: 190 / 7 / 2 / 1; named → prompt: 197 / 3 / 0 / 0; memory → memory: 200 / 0 / 0 / 0
- main/elements/e5f0-syn: 200 scenes, 22 eligible in both conditions; memory → prompt: 102 / 90 / 1 / 7; named → prompt: 199 / 1 / 0 / 0; memory → memory: 200 / 0 / 0 / 0

Gate (docstring rule): main/animals/e5f0-xlang: PASS {'lookups_lo>=0.80': True, 'english_lo>=0.85': True, 'eligible_scenes_both': 136, 'passes': True}; main/elements/e5f0-syn: FAIL {'lookups_lo>=0.80': False, 'english_lo>=0.85': True, 'eligible_scenes_both': 22, 'passes': False}; dev/animals/e3f0-xlang: FAIL {'lookups_lo>=0.80': True, 'english_lo>=0.85': True, 'eligible_scenes_both': 32, 'passes': False}; dev/elements/e3f0-syn: FAIL {'lookups_lo>=0.80': False, 'english_lo>=0.85': False, 'eligible_scenes_both': 5, 'passes': False}; dev/animals/e5f0-xlang: PASS {'lookups_lo>=0.80': True, 'english_lo>=0.85': True, 'eligible_scenes_both': 39, 'passes': True}; dev/elements/e5f0-syn: FAIL {'lookups_lo>=0.80': False, 'english_lo>=0.85': True, 'eligible_scenes_both': 10, 'passes': False}
