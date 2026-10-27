# natural_read / qwen35_9b_d2_natural_read

Verdict (primary, <= 10% right with the upper bound <= 20%): **holds**

Verdict (secondary, finding 4's bar <= 20% / <= 30%): holds

Items: 718 built -> 503 eligible (competence run qwen35_9b_natural_competence) -> 503 in the knockout run, 502 right unedited there.

| dropped because | dropped at this step | left | failing this criterion on its own |
|---|---|---|---|
| the answer's first token is under 3 characters and not its whole first word | 86 | 632 | 86 |
| with the paragraph, the answer's first token is not on top | 99 | 533 | 109 |
| with the paragraph, the greedy answer is wrong | 1 | 532 | 10 |
| the answer's sentence alone is not enough (first token not on top) | 11 | 521 | 96 |
| without the answer's sentence the first token is still on top (answered without it) | 18 | 503 | 18 |

Not covered: items whose answer needs a neighbouring sentence (a pronoun's antecedent, a subject named earlier) fail 'the answer's sentence alone' and are dropped, so the verdict is about answers that one sentence gives on its own.

| cell | right [95% Wilson] | n |
|---|---|---|
| answer's sentence hidden from the last tokens | 8% [6, 10] | 502 |
| another sentence hidden from the last tokens (control) | 100% [99, 100] | 502 |
| answer's sentence hidden from the last tokens, DeltaNet layers only (control) | 99% [98, 100] | 502 |
| answer's sentence hidden from everything after it (floor) | 1% [0, 2] | 502 |
| another sentence hidden from everything after it | 99% [98, 100] | 502 |
| answer's sentence hidden from the question words | 81% [78, 84] | 502 |
| baseline: the question after another article's paragraph | 0% [0, 1] | - |
| baseline: blocked answers scored against another item's answer | 1% [0, 2] | - |
