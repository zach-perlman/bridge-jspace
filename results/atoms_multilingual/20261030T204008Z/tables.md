# Multilingual answer classes for the 25 atoms (30 Oct)

## Muse first: Dan's case, `muse-glimmer-30b|muse30_x51_12_e1_r2|P2-L0-0095|PP` (muse30_x51_12_e1_r2)

The recall's answers: original 3, changed 7. Share of the J++ part's energy in an answer atom, any language: 0.0704.

| OMP | token | coefficient | energy share | old class | new class | reads as |
|---|---|---|---|---|---|---|
| 1 | ` Carm` | -14.15 | 0.0191 | other | other |  |
| 2 | `Eta` | +24.71 | 0.0159 | new bridge | new_bridge |  |
| 3 | ` Gamma` | -19.64 | 0.0252 | bridge | bridge |  |
| 4 | `，三` | -18.53 | 0.0130 | other | answer_any | 3 Chinese / Japanese number word |
| 5 | `VG` | -19.93 | 0.0081 | other | other |  |
| 6 | ` Ani` | +14.38 | 0.0089 | other | other |  |
| 7 | ` DPP` | -13.75 | 0.0067 | other | other |  |
| 8 | `(Id` | +18.22 | 0.0063 | other | other |  |
| 9 | ` ids` | -17.31 | 0.0065 | other | other |  |
| 10 | ` oito` | +16.11 | 0.0072 | other | number_other | 8 Portuguese number word |
| 11 | `.side` | -11.56 | 0.0061 | other | other |  |
| 12 | ` V` | +12.27 | 0.0060 | other | other |  |

## 51.12's 'the answer word is not read': English rank against the best over the translations

The answer_control items whose states are on this machine (the review's fixed sample; the run's other items need the box). Rank 1 = top, the recall's answer in O and its changed answer in S, the J++ lens at L and the bridge word; not read = best rank over both prompts > 50.

| model | items | label changes if translations count | per item: English best rank -> best over translations (token) |
|---|---|---|---|
| muse-glimmer-30b | 2 | 0 | P2-L0-0095: 61 -> 61 (' three'); P2-L0-0208: 7452 -> 2379 (' Sept') |
| qwen3.5-9b | 2 | 0 | P2-L0-0191: 38 -> 38 (' one'); P2-L0-0031: 107 -> 107 (' eight') |
| qwen3.6-27b | 3 | 0 | P2-L0-0043: 76 -> 76 (' three'); P2-L0-0130: 4264 -> 4264 (' six'); P2-L0-0039: 267 -> 267 (' four') |
| nemotron-3.5-lightning | 3 | 0 | P2-L0-0078: 3667 -> 3667 (' Two'); P2-L0-0092: 70379 -> 1645 (' Otto'); P2-L0-0041: 872 -> 872 (' three') |
| qwen3.5-122b-a10b | 0 | 0 | no states on this machine |

Share of the J++ part's energy (mean over items). old: x52_atoms' answer_own (English number words, digits, ordinals of the reader's two answers); new: the reader's original or changed answer in any of eleven languages, Roman numerals and digits, leading punctuation and spaces stripped.

## f5

| model | view | n | old answer share | new answer (any language) [95%] | number, not the answer | items with an answer atom | of those in another language | answer energy toward original / changed |
|---|---|---|---|---|---|---|---|---|
| muse-glimmer-30b | PM | 50 | 0.0007 | 0.0007 [0.0000, 0.0027] | 0.0030 | 1 of 50 | 0 | 0.0000 / 0.0007 |
| muse-glimmer-30b | PP | 50 | 0.0000 | 0.0000 [0.0000, 0.0000] | 0.0037 | 0 of 50 | 0 | 0.0000 / 0.0000 |
| qwen3.5-9b | PM | 50 | 0.0005 | 0.0012 [0.0000, 0.0027] | 0.0019 | 2 of 50 | 1 | 0.0007 / 0.0005 |
| qwen3.5-9b | PP | 50 | 0.0000 | 0.0000 [0.0000, 0.0000] | 0.0031 | 0 of 50 | 0 | 0.0000 / 0.0000 |
| qwen3.6-27b | PM | 50 | 0.0007 | 0.0014 [0.0000, 0.0034] | 0.0017 | 2 of 50 | 1 | 0.0000 / 0.0014 |
| qwen3.6-27b | PP | 50 | 0.0000 | 0.0000 [0.0000, 0.0000] | 0.0031 | 0 of 50 | 0 | 0.0000 / 0.0000 |
| nemotron-3.5-lightning | PM | 50 | 0.0000 | 0.0016 [0.0000, 0.0036] | 0.0020 | 2 of 50 | 2 | 0.0000 / 0.0016 |
| nemotron-3.5-lightning | PP | 50 | 0.0000 | 0.0013 [0.0000, 0.0027] | 0.0023 | 3 of 50 | 3 | 0.0004 / 0.0009 |
| qwen3.5-122b-a10b | PM | 50 | 0.0000 | 0.0005 [0.0000, 0.0016] | 0.0003 | 1 of 50 | 1 | 0.0000 / 0.0005 |
| qwen3.5-122b-a10b | PP | 50 | 0.0000 | 0.0000 [0.0000, 0.0000] | 0.0008 | 0 of 50 | 0 | 0.0000 / 0.0000 |

## answer_control

| model | view | n | old answer share | new answer (any language) [95%] | number, not the answer | items with an answer atom | of those in another language | answer energy toward original / changed |
|---|---|---|---|---|---|---|---|---|
| muse-glimmer-30b | PM | 50 | 0.0007 | 0.0007 [0.0000, 0.0027] | 0.0030 | 1 of 50 | 0 | 0.0000 / 0.0007 |
| muse-glimmer-30b | PP | 50 | 0.0000 | 0.0000 [0.0000, 0.0000] | 0.0037 | 0 of 50 | 0 | 0.0000 / 0.0000 |
| qwen3.5-9b | PM | 50 | 0.0005 | 0.0012 [0.0000, 0.0027] | 0.0019 | 2 of 50 | 1 | 0.0007 / 0.0005 |
| qwen3.5-9b | PP | 50 | 0.0000 | 0.0000 [0.0000, 0.0000] | 0.0031 | 0 of 50 | 0 | 0.0000 / 0.0000 |
| qwen3.6-27b | PM | 50 | 0.0007 | 0.0014 [0.0000, 0.0034] | 0.0017 | 2 of 50 | 1 | 0.0000 / 0.0014 |
| qwen3.6-27b | PP | 50 | 0.0000 | 0.0000 [0.0000, 0.0000] | 0.0031 | 0 of 50 | 0 | 0.0000 / 0.0000 |
| nemotron-3.5-lightning | PM | 50 | 0.0000 | 0.0016 [0.0000, 0.0036] | 0.0020 | 2 of 50 | 2 | 0.0000 / 0.0016 |
| nemotron-3.5-lightning | PP | 50 | 0.0000 | 0.0013 [0.0000, 0.0027] | 0.0023 | 3 of 50 | 3 | 0.0004 / 0.0009 |
| qwen3.5-122b-a10b | PM | 50 | 0.0000 | 0.0005 [0.0000, 0.0016] | 0.0003 | 1 of 50 | 1 | 0.0000 / 0.0005 |
| qwen3.5-122b-a10b | PP | 50 | 0.0000 | 0.0000 [0.0000, 0.0000] | 0.0008 | 0 of 50 | 0 | 0.0000 / 0.0000 |

## The largest answer atoms (any model, both views, the f5 items)

| model | scene | token | language | kind | value | sign | energy share | old class | weak |
|---|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | P2-L0-0347 | `prima` | Italian | ordinal | 1 | toward changed | 0.0115 | other |  |
| qwen3.5-9b | P2-L0-0063 | ` Segundo` | Spanish | ordinal | 2 | toward original | 0.0085 | other |  |
| nemotron-3.5-lightning | P2-L0-0407 | ` quattro` | Italian | number word | 4 | toward changed | 0.0077 | other |  |
| nemotron-3.5-lightning | P2-L0-0428 | `-IV` | Roman numeral | roman | 4 | toward original | 0.0052 | other |  |
| qwen3.6-27b | P2-L0-0206 | `Fourth` | English | ordinal | 4 | toward changed | 0.0052 | answer_own |  |
