# pointer_fair

## memory → prompt, after the cue, layers 32-40 at once, 1x: **not shown (controls failed or n too small: not interpretable)**

pointer 25% [0, 44] (n=8, k=5); lens 0% [0, 0] (n=8, k=5); random 0% [0, 0] (n=8, k=5); shuffled 12% [0, 29] (n=8, k=5); patch 50% [12, 88] (n=8, k=5)
memory → memory answers changed by the pointer: 0% [0, 0] (n=8, k=5)
pointer - lens [0.25, 0.0, 0.4444]; pointer - random [0.25, 0.0, 0.4444]
overshoot: {"n_off_target": 0, "beyond": 0, "expected_uniform": 0.0, "beyond_minus_uniform": [NaN, NaN, NaN]}; shuffled: {"n_off_target": 0, "beyond": 0, "expected_uniform": 0.0, "beyond_minus_uniform": [NaN, NaN, NaN]}

## memory → prompt, question words, layers 32-40 at once, 1x: **not shown (controls failed or n too small: not interpretable)**

pointer 50% [12, 88] (n=8, k=5); lens 38% [22, 57] (n=8, k=5); random 0% [0, 0] (n=8, k=5); shuffled 0% [0, 0] (n=8, k=5); patch 62% [40, 100] (n=8, k=5)
memory → memory answers changed by the pointer: 0% [0, 0] (n=8, k=5)
pointer - lens [0.125, -0.4286, 0.625]; pointer - random [0.5, 0.125, 0.875]
overshoot: {"n_off_target": 2, "beyond": 2, "expected_uniform": 1.67, "beyond_minus_uniform": [0.1667, 0.1667, 0.1667]}; shuffled: {"n_off_target": 2, "beyond": 1, "expected_uniform": 0.67, "beyond_minus_uniform": [0.1667, 0.1667, 0.1667]}

