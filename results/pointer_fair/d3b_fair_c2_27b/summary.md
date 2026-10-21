# pointer_fair

## memory → prompt, after the cue, layers 32-40 at once, 1x: **not shown (controls failed or n too small: not interpretable)**

pointer 34% [27, 41] (n=300, k=22); lens 13% [6, 23] (n=300, k=22); random 1% [0, 2] (n=300, k=22); shuffled 4% [1, 7] (n=300, k=22); patch 34% [25, 43] (n=300, k=22)
memory → memory answers changed by the pointer: 16% [9, 24] (n=200, k=22)
pointer - lens [0.2067, 0.1082, 0.292]; pointer - random [0.3333, 0.2602, 0.4051]
overshoot: {"n_off_target": 44, "beyond": 24, "expected_uniform": 14.0, "beyond_minus_uniform": [0.2273, 0.1143, 0.3411]}; shuffled: {"n_off_target": 66, "beyond": 21, "expected_uniform": 25.67, "beyond_minus_uniform": [-0.0707, -0.1576, 0.0205]}

## memory → prompt, question words, layers 32-40 at once, 1x: **not shown (controls failed or n too small: not interpretable)**

pointer 47% [40, 55] (n=300, k=22); lens 36% [24, 48] (n=300, k=22); random 1% [1, 2] (n=300, k=22); shuffled 9% [4, 14] (n=300, k=22); patch 79% [73, 84] (n=300, k=22)
memory → memory answers changed by the pointer: 16% [9, 24] (n=200, k=22)
pointer - lens [0.11, -0.042, 0.2803]; pointer - random [0.46, 0.3923, 0.5324]
overshoot: {"n_off_target": 108, "beyond": 52, "expected_uniform": 37.0, "beyond_minus_uniform": [0.1389, 0.0685, 0.2171]}; shuffled: {"n_off_target": 91, "beyond": 31, "expected_uniform": 30.0, "beyond_minus_uniform": [0.011, -0.0346, 0.05]}

