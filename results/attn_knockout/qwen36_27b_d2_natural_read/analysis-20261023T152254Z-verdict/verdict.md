# natural_read / qwen36_27b_d2_natural_read

Verdict (primary, <= 10% right with the upper bound <= 20%): **fails (more than 10% right, or the upper bound above 20%)**

Verdict (secondary, finding 4's bar <= 20% / <= 30%): fails (more than 20% right, or the upper bound above 30%)

Items: 718 built -> 469 eligible (competence run qwen36_27b_natural_competence) -> 469 in the knockout run, 469 right unedited there.

| dropped because | dropped at this step | left | failing this criterion on its own |
|---|---|---|---|
| the answer's first token is under 3 characters and not its whole first word | 86 | 632 | 86 |
| with the paragraph, the answer's first token is not on top | 145 | 487 | 162 |
| with the paragraph, the greedy answer is wrong | 2 | 485 | 12 |
| the answer's sentence alone is not enough (first token not on top) | 6 | 479 | 153 |
| without the answer's sentence the first token is still on top (answered without it) | 10 | 469 | 10 |

Not covered: items whose answer needs a neighbouring sentence (a pronoun's antecedent, a subject named earlier) fail 'the answer's sentence alone' and are dropped, so the verdict is about answers that one sentence gives on its own.

| cell | right [95% Wilson] | n |
|---|---|---|
| answer's sentence hidden from the last tokens | 30% [26, 34] | 469 |
| another sentence hidden from the last tokens (control) | 100% [99, 100] | 469 |
| answer's sentence hidden from the last tokens, DeltaNet layers only (control) | 100% [98, 100] | 469 |
| answer's sentence hidden from everything after it (floor) | 0% [0, 1] | 469 |
| another sentence hidden from everything after it | 100% [99, 100] | 469 |
| answer's sentence hidden from the question words | 71% [67, 75] | 469 |
| baseline: the question after another article's paragraph | 0% [0, 1] | - |
| baseline: blocked answers scored against another item's answer | 0% [0, 1] | - |
