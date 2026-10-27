# relay_swap / gemma4it_d2_relay_swap (gemma-4-31B-it, items of gemma4it_d2_v4_late_read_v3_r2)

**Verdict: relay**

Items: 300 memory -> prompt; counted (original prompt right unedited): 300.

- R, the answer's sentence hidden from the last tokens in every layer: +20.3 [+16.2, +24.7] points (entity cluster; items: +20.3 [+16.0, +25.0] points); new digit 21% [16, 26] substituted vs 0% [0, 2] original
- positive control (substituted, nothing hidden, answers the new digit): 100% [99, 100]
- off-path control (the off-path sentence hidden instead, substituted): 100% [99, 100]; its R +100.0 [+100.0, +100.0] points
- floor (hidden from every token after it, every layer): R +0.0 [+0.0, +0.0] points

R per topic: animals +26.0 [+18.8, +33.0] points (n 100, k 34); body +16.0 [+7.8, +25.2] points (n 100, k 14); countries +19.0 [+12.5, +26.0] points (n 100, k 36)

Answers per row kind (counted items): new digit / old digit / another listed digit / other
- orig|lookup|after|all: 2% / 2% / 51% / 45%
- orig|lookup|final|all: 0% / 22% / 75% / 2%
- orig|lookup_off|final|all: 0% / 100% / 0% / 0%
- orig|none|-|-: 0% / 100% / 0% / 0%
- sub|lookup|after|all: 2% / 2% / 51% / 45%
- sub|lookup|final|all: 21% / 1% / 77% / 2%
- sub|lookup_off|final|all: 100% / 0% / 0% / 0%
- sub|none|-|-: 100% / 0% / 0% / 0%

Agreement with the late-read run's rows: {"blocked": {"n": 300, "same_top": 0.99}, "unedited": {"n": 300, "same_top": 1.0}}
