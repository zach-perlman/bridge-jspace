# natural_read / olmo3_7b_instruct_d2_natural_read

Verdict (primary, <= 10% right with the upper bound <= 20%): **holds**

Verdict (secondary, finding 4's bar <= 20% / <= 30%): holds

Items: 718 built -> 428 eligible (competence run olmo3_7b_instruct_natural_competence) -> 428 in the knockout run, 426 right unedited there.

| dropped because | dropped at this step | left | failing this criterion on its own |
|---|---|---|---|
| the answer's first token is under 3 characters and not its whole first word | 90 | 628 | 90 |
| with the paragraph, the answer's first token is not on top | 113 | 515 | 121 |
| with the paragraph, the greedy answer is wrong | 6 | 509 | 55 |
| the answer's sentence alone is not enough (first token not on top) | 57 | 452 | 142 |
| without the answer's sentence the first token is still on top (answered without it) | 24 | 428 | 33 |

Not covered: items whose answer needs a neighbouring sentence (a pronoun's antecedent, a subject named earlier) fail 'the answer's sentence alone' and are dropped, so the verdict is about answers that one sentence gives on its own.

| cell | right [95% Wilson] | n |
|---|---|---|
| answer's sentence hidden from the last tokens | 5% [3, 7] | 426 |
| another sentence hidden from the last tokens (control) | 100% [98, 100] | 426 |
| answer's sentence hidden from the last tokens, DeltaNet layers only (control) | - | 0 |
| answer's sentence hidden from everything after it (floor) | 1% [1, 3] | 426 |
| another sentence hidden from everything after it | 99% [97, 99] | 426 |
| answer's sentence hidden from the question words | 64% [59, 68] | 426 |
| baseline: the question after another article's paragraph | 1% [1, 3] | - |
| baseline: blocked answers scored against another item's answer | 0% [0, 1] | - |
