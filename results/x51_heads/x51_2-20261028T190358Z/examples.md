# 51.2 view (verify pack): prompts as read, rows per arm. UNVERIFIED.

## qwen35_9b_x51_2 (qwen3.5-9b)

### 5 random items of 300 (seed 0)

#### C2-0035 (read): bridge goat, j = 2, lockers [['beetle', 2], ['tiger', 4], ['goat', 9]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

#### C2-0235 (read): bridge crow, j = 2, lockers [['fox', 5], ['ant', 3], ['crow', 4]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

#### C2-0367 (read): bridge pig, j = 2, lockers [['bee', 9], ['butterfly', 8], ['pig', 4]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

#### C2-0390 (read): bridge owl, j = 1, lockers [['bee', 9], ['owl', 4], ['mouse', 8]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

#### C2-0475 (read): bridge crow, j = 0, lockers [['crow', 1], ['lion', 2], ['fox', 5]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

### top1 at the last token(s): L27:h1

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top1 at the question token(s): L27:h1

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top3 at the last token(s): L27:h1, L27:h13, L23:h15

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top3 at the question token(s): L27:h1, L27:h13, L23:h15

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top5 at the last token(s): L27:h1, L27:h13, L23:h15, L23:h0, L23:h9

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top5 at the question token(s): L27:h1, L27:h13, L23:h15, L23:h0, L23:h9

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top10 at the last token(s): L27:h1, L27:h13, L23:h15, L23:h0, L23:h9, L23:h7, L23:h12, L23:h4, L23:h14, L19:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top10 at the question token(s): L27:h1, L27:h13, L23:h15, L23:h0, L23:h9, L23:h7, L23:h12, L23:h4, L23:h14, L19:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### best_layer at the last token(s): L27:h0, L27:h1, L27:h2, L27:h3, L27:h4, L27:h5, L27:h6, L27:h7, L27:h8, L27:h9, L27:h10, L27:h11, L27:h12, L27:h13, L27:h14, L27:h15

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### best_layer at the question token(s): L27:h0, L27:h1, L27:h2, L27:h3, L27:h4, L27:h5, L27:h6, L27:h7, L27:h8, L27:h9, L27:h10, L27:h11, L27:h12, L27:h13, L27:h14, L27:h15

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top1_r0 at the last token(s): L27:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top1_r0 at the question token(s): L27:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top3_r0 at the last token(s): L23:h14, L27:h6, L27:h7

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top3_r0 at the question token(s): L23:h14, L27:h6, L27:h7

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top5_r0 at the last token(s): L23:h7, L23:h8, L23:h10, L27:h2, L27:h9

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 21 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top5_r0 at the question token(s): L23:h7, L23:h8, L23:h10, L27:h2, L27:h9

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top10_r0 at the last token(s): L19:h11, L23:h1, L23:h2, L23:h5, L23:h6, L23:h10, L23:h11, L23:h13, L27:h4, L27:h14

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### top10_r0 at the question token(s): L19:h11, L23:h1, L23:h2, L23:h5, L23:h6, L23:h10, L23:h11, L23:h13, L27:h4, L27:h14

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### best_layer_r0 at the last token(s): L15:h2, L15:h6, L15:h14, L15:h15, L19:h2, L19:h7, L23:h0, L23:h11, L23:h13, L31:h1, L31:h2, L31:h8, L31:h9, L31:h11, L31:h12, L31:h15

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

### best_layer_r0 at the question token(s): L15:h2, L15:h6, L15:h14, L15:h15, L19:h2, L19:h7, L23:h0, L23:h11, L23:h13, L31:h1, L31:h2, L31:h8, L31:h9, L31:h11, L31:h12, L31:h15

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0043 | 0 | original (22) | original (22) | 23 | 23 |
| C2-0217 | 0 | target (23) | target (23) | 19 | 19 |
| C2-0246 | 1 | original (19) | original (19) | 17 | 17 |
| C2-0297 | 2 | third (23) | third (23) | 17 | 17 |
| C2-0324 | 2 | other (18) | other (18) | 17 | 17 |
| C2-0337 | 2 | third (16) | third (16) | 17 | 17 |
| C2-0362 | 2 | original (17) | original (17) | 19 | 19 |
| C2-0390 | 0 | target (24) | target (24) | 21 | 21 |
| C2-0392 | 0 | target (21) | target (21) | 17 | 17 |
| C2-0406 | 1 | original (21) | original (21) | 17 | 17 |

## muse30_x51_2_r2 (muse-glimmer-30b)

### 5 random items of 296 (seed 0)

#### C2-0039 (fit): bridge dog, j = 1, lockers [['bee', 9], ['dog', 7], ['cow', 8]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [109], "question": [84, 85, 86, 87, 88, 89, 90, 91]}, "PM": {"last": [110], "question": [84, 85, 86, 87, 88, 89, 90, 91, 92]}}

#### C2-0281 (fit): bridge bee, j = 2, lockers [['duck', 9], ['butterfly', 3], ['bee', 5]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [109], "question": [84, 85, 86, 87, 88, 89, 90, 91]}, "PM": {"last": [110], "question": [84, 85, 86, 87, 88, 89, 90, 91, 92]}}

#### C2-0420 (fit): bridge cow, j = 2, lockers [['fly', 8], ['fox', 1], ['cow', 5]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [109], "question": [84, 85, 86, 87, 88, 89, 90, 91]}, "PM": {"last": [110], "question": [84, 85, 86, 87, 88, 89, 90, 91, 92]}}

#### C2-0468 (read): bridge crow, j = 2, lockers [['goat', 1], ['rabbit', 5], ['crow', 4]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [109], "question": [84, 85, 86, 87, 88, 89, 90, 91]}, "PM": {"last": [110], "question": [84, 85, 86, 87, 88, 89, 90, 91, 92]}}

#### C2-0564 (fit): bridge mouse, j = 1, lockers [['frog', 1], ['mouse', 3], ['turkey', 8]]

```
(tokenizer of another target)
```

Sites: {"PP": {"last": [109], "question": [84, 85, 86, 87, 88, 89, 90, 91]}, "PM": {"last": [110], "question": [84, 85, 86, 87, 88, 89, 90, 91, 92]}}

### top1 at the last token(s): L39:h1

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | original (34) | 30 | 30 |
| C2-0448 | 2 | third (32) | target (34) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top1 at the question token(s): L39:h1

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top3 at the last token(s): L39:h1, L35:h25, L35:h21

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | original (33) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | original (34) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top3 at the question token(s): L39:h1, L35:h25, L35:h21

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top5 at the last token(s): L39:h1, L35:h25, L35:h21, L34:h20, L35:h17

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | original (33) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | original (34) | 30 | 30 |
| C2-0448 | 2 | third (32) | target (34) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top5 at the question token(s): L39:h1, L35:h25, L35:h21, L34:h20, L35:h17

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top10 at the last token(s): L39:h1, L35:h25, L35:h21, L34:h20, L35:h17, L43:h4, L34:h21, L33:h25, L35:h31, L47:h25

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | original (33) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | original (34) | 30 | 30 |
| C2-0448 | 2 | third (32) | target (34) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top10 at the question token(s): L39:h1, L35:h25, L35:h21, L34:h20, L35:h17, L43:h4, L34:h21, L33:h25, L35:h31, L47:h25

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### best_layer at the last token(s): L39:h0, L39:h1, L39:h2, L39:h3, L39:h4, L39:h5, L39:h6, L39:h7, L39:h8, L39:h9, L39:h10, L39:h11, L39:h12, L39:h13, L39:h14, L39:h15, L39:h16, L39:h17, L39:h18, L39:h19, L39:h20, L39:h21, L39:h22, L39:h23, L39:h24, L39:h25, L39:h26, L39:h27, L39:h28, L39:h29, L39:h30, L39:h31

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | original (34) | 30 | 30 |
| C2-0448 | 2 | third (32) | target (34) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### best_layer at the question token(s): L39:h0, L39:h1, L39:h2, L39:h3, L39:h4, L39:h5, L39:h6, L39:h7, L39:h8, L39:h9, L39:h10, L39:h11, L39:h12, L39:h13, L39:h14, L39:h15, L39:h16, L39:h17, L39:h18, L39:h19, L39:h20, L39:h21, L39:h22, L39:h23, L39:h24, L39:h25, L39:h26, L39:h27, L39:h28, L39:h29, L39:h30, L39:h31

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top1_r0 at the last token(s): L39:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top1_r0 at the question token(s): L39:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top3_r0 at the last token(s): L35:h13, L35:h30, L39:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top3_r0 at the question token(s): L35:h13, L35:h30, L39:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top5_r0 at the last token(s): L34:h17, L35:h3, L35:h13, L35:h16, L39:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | target (34) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top5_r0 at the question token(s): L34:h17, L35:h3, L35:h13, L35:h16, L39:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top10_r0 at the last token(s): L33:h5, L34:h14, L34:h24, L35:h15, L35:h18, L35:h20, L35:h24, L39:h0, L43:h6, L47:h27

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### top10_r0 at the question token(s): L33:h5, L34:h14, L34:h24, L35:h15, L35:h18, L35:h20, L35:h24, L39:h0, L43:h6, L47:h27

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | third (32) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### best_layer_r0 at the last token(s): L27:h6, L27:h21, L27:h30, L28:h0, L28:h9, L28:h27, L29:h4, L29:h17, L30:h2, L30:h15, L32:h21, L33:h7, L34:h9, L34:h16, L34:h20, L36:h0, L36:h9, L37:h10, L38:h14, L38:h18, L38:h28, L42:h12, L44:h5, L44:h11, L45:h26, L45:h31, L47:h10, L48:h28, L49:h28, L50:h18, L50:h23, L51:h7

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | original (33) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | target (34) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

### best_layer_r0 at the question token(s): L27:h6, L27:h21, L27:h30, L28:h0, L28:h9, L28:h27, L29:h4, L29:h17, L30:h2, L30:h15, L32:h21, L33:h7, L34:h9, L34:h16, L34:h20, L36:h0, L36:h9, L37:h10, L38:h14, L38:h18, L38:h28, L42:h12, L44:h5, L44:h11, L45:h26, L45:h31, L47:h10, L48:h28, L49:h28, L50:h18, L50:h23, L51:h7

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0037 | 1 | target (29) | target (29) | 32 | 32 |
| C2-0291 | 0 | target (29) | target (29) | 32 | 32 |
| C2-0331 | 2 | original (35) | original (35) | 32 | 32 |
| C2-0401 | 2 | target (36) | target (36) | 30 | 30 |
| C2-0448 | 2 | third (32) | target (34) | 32 | 32 |
| C2-0472 | 2 | target (34) | target (34) | 30 | 30 |
| C2-0490 | 1 | original (36) | original (36) | 32 | 32 |
| C2-0559 | 0 | third (30) | third (30) | 30 | 30 |
| C2-0563 | 1 | target (33) | target (33) | 30 | 30 |
| C2-0582 | 1 | original (35) | original (35) | 32 | 32 |

## x51_2_27b (qwen3.6-27b)

### 5 random items of 300 (seed 0)

#### C2-0028 (read): bridge fly, j = 0, lockers [['fly', 3], ['duck', 6], ['bee', 4]]

```
<|im_start|>user
⟦slot0 (j):The locker of the fly is 3.⟧⟦slot1 (k): The locker of the duck is 6.⟧⟦slot2 (k): The locker of the bee is 4.⟧ Lucy picked the duck. Sam picked the⟦bridge: fly⟧. Liam picked the bee.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

#### C2-0199 (read): bridge tick, j = 0, lockers [['tick', 7], ['fly', 9], ['bee', 6]]

```
<|im_start|>user
⟦slot0 (j):The locker of the tick is 7.⟧⟦slot1 (k): The locker of the fly is 9.⟧⟦slot2 (k): The locker of the bee is 6.⟧ Vera picked the bee. James picked the fly. Owen picked the⟦bridge: tick⟧.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

#### C2-0293 (fit): bridge mouse, j = 2, lockers [['butterfly', 4], ['fly', 1], ['mouse', 6]]

```
<|im_start|>user
⟦slot0 (k):The locker of the butterfly is 4.⟧⟦slot1 (k): The locker of the fly is 1.⟧⟦slot2 (j): The locker of the mouse is 6.⟧ Mark picked the butterfly. Anna picked the fly. Noah picked the⟦bridge: mouse⟧.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

#### C2-0324 (read): bridge crow, j = 0, lockers [['crow', 8], ['camel', 1], ['wolf', 2]]

```
<|im_start|>user
⟦slot0 (j):The locker of the crow is 8.⟧⟦slot1 (k): The locker of the camel is 1.⟧⟦slot2 (k): The locker of the wolf is 2.⟧ Laura picked the camel. Vera picked the⟦bridge: crow⟧. Eve picked the wolf.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

#### C2-0390 (fit): bridge owl, j = 1, lockers [['bee', 9], ['owl', 4], ['mouse', 8]]

```
<|im_start|>user
⟦slot0 (k):The locker of the bee is 9.⟧⟦slot1 (j): The locker of the owl is 4.⟧⟦slot2 (k): The locker of the mouse is 8.⟧ Mark picked the bee. Zoe picked the⟦bridge: owl⟧. Peter picked the mouse.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [74], "question": [46, 47, 48, 49, 50, 51, 52, 53]}, "PM": {"last": [75], "question": [46, 47, 48, 49, 50, 51, 52, 53, 54]}}

### top1 at the last token(s): L51:h20

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top1 at the question token(s): L51:h20

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top3 at the last token(s): L51:h20, L51:h22, L43:h17

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top3 at the question token(s): L51:h20, L51:h22, L43:h17

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top5 at the last token(s): L51:h20, L51:h22, L43:h17, L43:h14, L59:h21

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | original ('5') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top5 at the question token(s): L51:h20, L51:h22, L43:h17, L43:h14, L59:h21

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top10 at the last token(s): L51:h20, L51:h22, L43:h17, L43:h14, L59:h21, L59:h3, L51:h23, L39:h2, L39:h23, L47:h1

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | original ('5') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top10 at the question token(s): L51:h20, L51:h22, L43:h17, L43:h14, L59:h21, L59:h3, L51:h23, L39:h2, L39:h23, L47:h1

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### best_layer at the last token(s): L51:h0, L51:h1, L51:h2, L51:h3, L51:h4, L51:h5, L51:h6, L51:h7, L51:h8, L51:h9, L51:h10, L51:h11, L51:h12, L51:h13, L51:h14, L51:h15, L51:h16, L51:h17, L51:h18, L51:h19, L51:h20, L51:h21, L51:h22, L51:h23

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### best_layer at the question token(s): L51:h0, L51:h1, L51:h2, L51:h3, L51:h4, L51:h5, L51:h6, L51:h7, L51:h8, L51:h9, L51:h10, L51:h11, L51:h12, L51:h13, L51:h14, L51:h15, L51:h16, L51:h17, L51:h18, L51:h19, L51:h20, L51:h21, L51:h22, L51:h23

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top1_r0 at the last token(s): L51:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top1_r0 at the question token(s): L51:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top3_r0 at the last token(s): L43:h11, L51:h12, L51:h19

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top3_r0 at the question token(s): L43:h11, L51:h12, L51:h19

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top5_r0 at the last token(s): L43:h3, L43:h21, L51:h19, L51:h23, L59:h8

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top5_r0 at the question token(s): L43:h3, L43:h21, L51:h19, L51:h23, L59:h8

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top10_r0 at the last token(s): L39:h17, L39:h18, L43:h4, L43:h13, L47:h23, L51:h5, L51:h7, L51:h19, L59:h2, L59:h16

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### top10_r0 at the question token(s): L39:h17, L39:h18, L43:h4, L43:h13, L47:h23, L51:h5, L51:h7, L51:h19, L59:h2, L59:h16

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### best_layer_r0 at the last token(s): L35:h7, L35:h12, L35:h16, L35:h17, L35:h20, L39:h2, L39:h3, L39:h7, L43:h0, L43:h13, L43:h16, L43:h20, L47:h12, L47:h18, L47:h19, L47:h23, L55:h7, L55:h13, L59:h0, L59:h6, L59:h23, L63:h3, L63:h6, L63:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

### best_layer_r0 at the question token(s): L35:h7, L35:h12, L35:h16, L35:h17, L35:h20, L39:h2, L39:h3, L39:h7, L43:h0, L43:h13, L43:h16, L43:h20, L47:h12, L47:h18, L47:h19, L47:h23, L55:h7, L55:h13, L59:h0, L59:h6, L59:h23, L63:h3, L63:h6, L63:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0032 | 0 | target ('9') | target ('9') | '4' | '4' |
| C2-0199 | 1 | original ('7') | original ('7') | '8' | '8' |
| C2-0224 | 2 | original ('2') | original ('2') | '6' | '6' |
| C2-0263 | 1 | original ('3') | original ('3') | '2' | '2' |
| C2-0281 | 2 | original ('9') | original ('9') | '4' | '4' |
| C2-0291 | 2 | original ('1') | original ('1') | '8' | '8' |
| C2-0304 | 2 | target ('2') | target ('2') | '4' | '4' |
| C2-0358 | 0 | original ('5') | original ('5') | '6' | '6' |
| C2-0364 | 1 | target ('6') | target ('6') | '6' | '6' |
| C2-0373 | 2 | original ('1') | original ('1') | '6' | '6' |

