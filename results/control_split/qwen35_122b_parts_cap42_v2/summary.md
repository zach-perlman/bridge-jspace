# control_split / qwen35_122b_parts_cap42_v2

Control (the manifest's rule): passes: R inside in ['R/question/band']

| family | group | mode | n | full | rest | J-space | matched | concentration | verdict |
|---|---|---|---|---|---|---|---|---|---|
| R | question | single | 100 | 31% | 19% | 6.3% | 1.7% | 1.56 [1.40, 1.73] | outside |
| R | question | band | 100 | 86% | 71% | 36.1% | 9.1% | 3.30 [3.04, 3.56] | inside |
| B | question | single | 100 | 32% | 12% | 6.9% | 1.6% | 1.59 [1.42, 1.76] | outside |
| B | question | band | 100 | 81% | 39% | 22.0% | 3.5% | 1.99 [1.79, 2.20] | inconclusive |
- R/question/single: answer2 2.9%, answer2 null 0.1%, words4 5.1%, words4 null 0.1%, jspace_minus_words 6.4%, jspace_minus_words null 0.2%, jspace_wo_own 1.2%, jspace_wo_own null 0.2%, jspace_wo_words4 1.2%, jspace_wo_words4 null 0.2% | variance shares: answer2 0.012, words4 0.027, jspace_minus_words 0.122, jspace_wo_own 0.100, jspace_wo_words4 0.099
- R/question/band: answer2 16.5%, answer2 null 0.4%, words4 32.1%, words4 null 0.5%, jspace_minus_words 36.7%, jspace_minus_words null 0.8%, jspace_wo_own 6.2%, jspace_wo_own null 0.0%, jspace_wo_words4 5.4%, jspace_wo_words4 null -0.0% | variance shares: answer2 0.012, words4 0.027, jspace_minus_words 0.122, jspace_wo_own 0.100, jspace_wo_words4 0.099
- B/question/single: answer2 3.8%, answer2 null -0.1%, words4 5.6%, words4 null -0.0%, jspace_minus_words 6.9%, jspace_minus_words null 0.0%, jspace_wo_own 1.4%, jspace_wo_own null -0.0%, jspace_wo_words4 1.2%, jspace_wo_words4 null -0.1% | variance shares: answer2 0.018, words4 0.034, jspace_minus_words 0.135, jspace_wo_own 0.107, jspace_wo_words4 0.106
- B/question/band: answer2 9.3%, answer2 null 0.0%, words4 16.4%, words4 null -0.0%, jspace_minus_words 22.1%, jspace_minus_words null -0.0%, jspace_wo_own 3.3%, jspace_wo_own null -0.1%, jspace_wo_words4 2.5%, jspace_wo_words4 null 0.1% | variance shares: answer2 0.018, words4 0.034, jspace_minus_words 0.135, jspace_wo_own 0.107, jspace_wo_words4 0.106
