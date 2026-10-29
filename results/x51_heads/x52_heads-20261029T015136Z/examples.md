# 51.2 view (verify pack): prompts as read, rows per arm. UNVERIFIED.

## nem35l_x52_heads (nemotron-3.5-lightning)

### 5 random items of 300 (seed 0)

#### C2-0046 (read): bridge crow, j = 0, lockers [['crow', 9], ['wolf', 5], ['horse', 3]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (j):The locker of the crow is 9.⟧⟦slot1 (k): The locker of the wolf is 5.⟧⟦slot2 (k): The locker of the horse is 3.⟧ Eve picked the horse. Owen picked the wolf. Peter picked the⟦bridge: crow⟧.
Which locker belongs to Peter's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [77], "question": [50, 51, 52, 53, 54, 55, 56, 57]}, "PM": {"last": [78], "question": [50, 51, 52, 53, 54, 55, 56, 57, 58]}}

#### C2-0304 (fit): bridge ant, j = 1, lockers [['fox', 4], ['ant', 6], ['rabbit', 7]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (k):The locker of the fox is 4.⟧⟦slot1 (j): The locker of the ant is 6.⟧⟦slot2 (k): The locker of the rabbit is 7.⟧ Ruby picked the rabbit. Eric picked the⟦bridge: ant⟧. James picked the fox.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [77], "question": [50, 51, 52, 53, 54, 55, 56, 57]}, "PM": {"last": [78], "question": [50, 51, 52, 53, 54, 55, 56, 57, 58]}}

#### C2-0475 (fit): bridge fly, j = 0, lockers [['fly', 7], ['turkey', 2], ['dog', 9]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (j):The locker of the fly is 7.⟧⟦slot1 (k): The locker of the turkey is 2.⟧⟦slot2 (k): The locker of the dog is 9.⟧ Ivan picked the dog. Sara picked the turkey. Victor picked the⟦bridge: fly⟧.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [77], "question": [50, 51, 52, 53, 54, 55, 56, 57]}, "PM": {"last": [78], "question": [50, 51, 52, 53, 54, 55, 56, 57, 58]}}

#### C2-0511 (fit): bridge owl, j = 0, lockers [['owl', 2], ['butterfly', 1], ['lion', 4]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (j):The locker of the owl is 2.⟧⟦slot1 (k): The locker of the butterfly is 1.⟧⟦slot2 (k): The locker of the lion is 4.⟧ Eve picked the lion. Carl picked the butterfly. Zoe picked the⟦bridge: owl⟧.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [77], "question": [50, 51, 52, 53, 54, 55, 56, 57]}, "PM": {"last": [78], "question": [50, 51, 52, 53, 54, 55, 56, 57, 58]}}

#### C2-0602 (fit): bridge ant, j = 2, lockers [['cat', 9], ['eagle', 1], ['ant', 4]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (k):The locker of the cat is 9.⟧⟦slot1 (k): The locker of the eagle is 1.⟧⟦slot2 (j): The locker of the ant is 4.⟧ Sam picked the⟦bridge: ant⟧. Adam picked the eagle. Grace picked the cat.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

Sites: {"PP": {"last": [77], "question": [50, 51, 52, 53, 54, 55, 56, 57]}, "PM": {"last": [78], "question": [50, 51, 52, 53, 54, 55, 56, 57, 58]}}

### top1 at the last token(s): L33:h7

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top1 at the question token(s): L33:h7

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top3 at the last token(s): L33:h7, L33:h0, L33:h5

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '4' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top3 at the question token(s): L33:h7, L33:h0, L33:h5

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top5 at the last token(s): L33:h7, L33:h0, L33:h5, L33:h19, L42:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '4' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top5 at the question token(s): L33:h7, L33:h0, L33:h5, L33:h19, L42:h12

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top10 at the last token(s): L33:h7, L33:h0, L33:h5, L33:h19, L42:h12, L33:h13, L33:h22, L33:h15, L33:h18, L33:h1

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '6' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '4' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top10 at the question token(s): L33:h7, L33:h0, L33:h5, L33:h19, L42:h12, L33:h13, L33:h22, L33:h15, L33:h18, L33:h1

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### best_layer at the last token(s): L33:h0, L33:h1, L33:h2, L33:h3, L33:h4, L33:h5, L33:h6, L33:h7, L33:h8, L33:h9, L33:h10, L33:h11, L33:h12, L33:h13, L33:h14, L33:h15, L33:h16, L33:h17, L33:h18, L33:h19, L33:h20, L33:h21, L33:h22, L33:h23, L33:h24, L33:h25, L33:h26, L33:h27, L33:h28, L33:h29, L33:h30, L33:h31

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '8' |
| C2-0180 | 0 | original ('8') | target ('4') | '2' | '4' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '4' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### best_layer at the question token(s): L33:h0, L33:h1, L33:h2, L33:h3, L33:h4, L33:h5, L33:h6, L33:h7, L33:h8, L33:h9, L33:h10, L33:h11, L33:h12, L33:h13, L33:h14, L33:h15, L33:h16, L33:h17, L33:h18, L33:h19, L33:h20, L33:h21, L33:h22, L33:h23, L33:h24, L33:h25, L33:h26, L33:h27, L33:h28, L33:h29, L33:h30, L33:h31

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top1_r0 at the last token(s): L33:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top1_r0 at the question token(s): L33:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top3_r0 at the last token(s): L33:h14, L33:h16, L33:h31

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '8' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '8' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top3_r0 at the question token(s): L33:h14, L33:h16, L33:h31

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top5_r0 at the last token(s): L33:h4, L33:h14, L33:h20, L33:h26, L42:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '8' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '8' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top5_r0 at the question token(s): L33:h4, L33:h14, L33:h20, L33:h26, L42:h0

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top10_r0 at the last token(s): L33:h2, L33:h8, L33:h9, L33:h14, L33:h20, L33:h23, L33:h26, L33:h28, L33:h29, L42:h6

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '8' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '8' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### top10_r0 at the question token(s): L33:h2, L33:h8, L33:h9, L33:h14, L33:h20, L33:h23, L33:h26, L33:h28, L33:h29, L42:h6

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### best_layer_r0 at the last token(s): L19:h3, L19:h4, L19:h6, L19:h8, L19:h10, L19:h13, L19:h15, L19:h24, L19:h29, L19:h30, L26:h0, L26:h2, L26:h4, L26:h10, L26:h13, L26:h14, L26:h15, L26:h19, L26:h22, L26:h25, L26:h28, L26:h31, L42:h0, L42:h1, L42:h7, L42:h11, L42:h19, L42:h20, L42:h21, L42:h23, L42:h28, L42:h29

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | original ('2') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

### best_layer_r0 at the question token(s): L19:h3, L19:h4, L19:h6, L19:h8, L19:h10, L19:h13, L19:h15, L19:h24, L19:h29, L19:h30, L26:h0, L26:h2, L26:h4, L26:h10, L26:h13, L26:h14, L26:h15, L26:h19, L26:h22, L26:h25, L26:h28, L26:h31, L42:h0, L42:h1, L42:h7, L42:h11, L42:h19, L42:h20, L42:h21, L42:h23, L42:h28, L42:h29

| scene | k | lookup swap | lookup swap + ablation | recall swap | recall swap + ablation |
|---|---|---|---|---|---|
| C2-0024 | 0 | original ('8') | original ('8') | '4' | '4' |
| C2-0180 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0271 | 1 | target ('2') | target ('2') | '2' | '2' |
| C2-0290 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0341 | 0 | original ('8') | original ('8') | '2' | '2' |
| C2-0345 | 0 | target ('2') | target ('2') | '2' | '2' |
| C2-0556 | 0 | target ('3') | target ('3') | '4' | '4' |
| C2-0605 | 0 | target ('1') | target ('1') | '4' | '4' |
| C2-0629 | 1 | original ('5') | original ('5') | '2' | '2' |
| C2-0664 | 1 | original ('5') | original ('5') | '2' | '2' |

