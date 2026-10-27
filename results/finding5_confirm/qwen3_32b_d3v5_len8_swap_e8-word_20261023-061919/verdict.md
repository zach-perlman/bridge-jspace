# finding5_confirm / qwen3_32b_d3v5_len8_swap, layer 52 (e8-word, 8 statements)

**DL (reported): partly** (A True, B False; n 256)
- 1st and 2nd: position - identity +70 [+55, +84] points (n 64)
- 3rd-8th: identity - position +1 [-10, +11] points (n 192)
- by k: {"1": {"position": 33, "context": 1, "none": 1}, "2": {"context": 6, "position": 16, "none": 3, "identity": 4}, "3": {"position": 11, "none": 10, "identity": 4, "context": 6, "other": 1}, "4": {"position": 7, "none": 4, "context": 12, "identity": 9, "value": 1}, "5": {"identity": 9, "context": 10, "position": 7, "none": 3}, "6": {"identity": 10, "none": 8, "position": 2, "context": 10, "value": 2}, "7": {"identity": 4, "position": 3, "context": 7, "none": 7, "value": 2, "other": 1}, "8": {"position": 12, "none": 11, "identity": 7, "value": 2, "other": 3, "context": 7}}

**RL (decisive): confirms** (A True, B True; n 256)
- 1st and 2nd: position - identity +61 [+46, +76] points (n 64)
- 3rd-8th: identity - position +14 [+4, +23] points (n 192)
- by k: {"1": {"position": 31, "context": 1, "none": 1, "identity": 2}, "2": {"position": 15, "context": 6, "none": 2, "identity": 5, "value": 1}, "3": {"position": 6, "none": 10, "identity": 11, "context": 5}, "4": {"position": 4, "identity": 12, "context": 14, "none": 2, "value": 1}, "5": {"none": 2, "context": 9, "position": 8, "identity": 9, "value": 1}, "6": {"identity": 10, "context": 12, "position": 4, "none": 5, "value": 1}, "7": {"identity": 6, "position": 6, "none": 7, "context": 5}, "8": {"position": 3, "none": 10, "identity": 9, "context": 14, "value": 5, "other": 1}}

