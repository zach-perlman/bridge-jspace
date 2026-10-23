# relay_swap / d2_relay_swap_long_27b (Qwen3.6-27B, items of d2_late_read_long_27b_r3)

**Verdict: relay**

Items: 178 memory -> prompt; counted (original prompt right unedited): 178.

- R, the answer's sentence hidden from the last tokens in every attention layer: +23.6 [+18.3, +28.7] points (entity cluster; items: +23.6 [+17.4, +30.3] points); new digit 24% [18, 30] substituted vs 0% [0, 2] original
- positive control (substituted, nothing hidden, answers the new digit): 100% [98, 100]
- off-path control (the off-path sentence hidden instead, substituted): 100% [98, 100]; its R +100.0 [+100.0, +100.0] points
- floor (hidden from every token after it, every layer): R +0.0 [+0.0, +0.0] points
- hidden from the last tokens in every layer, DeltaNet included: R +23.0 [+17.7, +28.4] points

R per topic: animals +24.1 [+15.0, +33.9] points (n 58, k 33); body +20.0 [+11.7, +28.3] points (n 60, k 15); countries +26.7 [+17.5, +35.6] points (n 60, k 36)

Answers per row kind (counted items): new digit / old digit / another listed digit / other
- orig|lookup|after|all: 1% / 0% / 99% / 1%
- orig|lookup|final|all: 1% / 27% / 72% / 0%
- orig|lookup|final|attn: 0% / 26% / 74% / 0%
- orig|lookup_off|final|attn: 0% / 100% / 0% / 0%
- orig|none|-|-: 0% / 100% / 0% / 0%
- sub|lookup|after|all: 1% / 0% / 99% / 1%
- sub|lookup|final|all: 24% / 0% / 76% / 0%
- sub|lookup|final|attn: 24% / 0% / 76% / 0%
- sub|lookup_off|final|attn: 100% / 0% / 0% / 0%
- sub|none|-|-: 100% / 0% / 0% / 0%

Agreement with the late-read run's rows: {"blocked": {"n": 178, "same_top": 1.0}, "unedited": {"n": 178, "same_top": 1.0}}
