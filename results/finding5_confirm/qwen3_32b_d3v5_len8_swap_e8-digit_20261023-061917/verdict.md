# finding5_confirm / qwen3_32b_d3v5_len8_swap, layer 50 (e8-digit, 8 statements)

**DL (reported): confirms** (A True, B True; n 256)
- 1st and 2nd: position - identity +92 [+84, +98] points (n 64)
- 3rd-8th: identity - position +8 [-0, +17] points (n 192)
- by k: {"1": {"none": 1, "position": 34}, "2": {"position": 26, "none": 2, "identity": 1}, "3": {"none": 6, "identity": 10, "position": 11, "context": 5}, "4": {"context": 12, "none": 3, "identity": 11, "position": 7}, "5": {"context": 8, "position": 7, "identity": 7, "none": 7}, "6": {"identity": 13, "context": 11, "none": 6, "position": 2}, "7": {"identity": 9, "position": 4, "none": 3, "context": 8}, "8": {"identity": 12, "position": 15, "none": 5, "context": 10}}

**RL (decisive): confirms** (A True, B True; n 256)
- 1st and 2nd: position - identity +83 [+69, +94] points (n 64)
- 3rd-8th: identity - position +20 [+11, +30] points (n 192)
- by k: {"1": {"position": 34, "context": 1}, "2": {"context": 2, "none": 2, "position": 22, "identity": 3}, "3": {"identity": 13, "position": 8, "context": 10, "none": 1}, "4": {"none": 6, "identity": 12, "context": 11, "position": 4}, "5": {"none": 7, "position": 6, "identity": 8, "context": 7, "recall": 1}, "6": {"identity": 13, "context": 10, "none": 7, "position": 2}, "7": {"identity": 9, "value": 1, "recall": 1, "context": 8, "position": 3, "none": 2}, "8": {"identity": 16, "none": 6, "value": 2, "position": 9, "context": 8, "recall": 1}}

