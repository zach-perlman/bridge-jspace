# 49.7 view (verify pack): the lookup's prompt exactly as the model reads it. UNVERIFIED.

## nem35l_x52_attn (nemotron-3.5-lightning): 10 random items of 300 (seed 0); best head L33:h7

### C2-0046 (read): bridge crow, j = 0, lockers [['crow', 9], ['wolf', 5], ['horse', 3]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (j):The locker of the crow is 9.⟧⟦slot1 (k): The locker of the wolf is 5.⟧⟦slot2 (k): The locker of the horse is 3.⟧ Eve picked the horse. Owen picked the wolf. Peter picked the⟦bridge: crow⟧.
Which locker belongs to Peter's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('9') | '2' | 0.983 / 0.003 / 0.002 |
| swap | 1 | third ('3') | '2' | 0.006 / 0.361 / 0.582 |
| random | 1 | original ('9') | '2' | 0.987 / 0.003 / 0.001 |
| swap | 2 | target ('3') | '2' | 0.005 / 0.079 / 0.800 |
| random | 2 | original ('9') | '2' | 0.985 / 0.003 / 0.002 |

### C2-0304 (fit): bridge ant, j = 1, lockers [['fox', 4], ['ant', 6], ['rabbit', 7]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (k):The locker of the fox is 4.⟧⟦slot1 (j): The locker of the ant is 6.⟧⟦slot2 (k): The locker of the rabbit is 7.⟧ Ruby picked the rabbit. Eric picked the⟦bridge: ant⟧. James picked the fox.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('6') | '6' | 0.003 / 0.977 / 0.019 |
| swap | 0 | target ('4') | '4' | 0.993 / 0.005 / 0.001 |
| random | 0 | original ('6') | '6' | 0.002 / 0.981 / 0.016 |
| swap | 2 | original ('6') | '6' | 0.004 / 0.938 / 0.056 |
| random | 2 | original ('6') | '6' | 0.004 / 0.975 / 0.020 |

### C2-0357 (fit): bridge dog, j = 1, lockers [['duck', 2], ['dog', 6], ['deer', 9]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (k):The locker of the duck is 2.⟧⟦slot1 (j): The locker of the dog is 6.⟧⟦slot2 (k): The locker of the deer is 9.⟧ Clara picked the deer. Alice picked the duck. Frank picked the⟦bridge: dog⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('6') | '4' | 0.007 / 0.902 / 0.084 |
| swap | 0 | original ('6') | '4' | 0.231 / 0.708 / 0.043 |
| random | 0 | original ('6') | '4' | 0.007 / 0.874 / 0.110 |
| swap | 2 | original ('6') | '4' | 0.010 / 0.716 / 0.258 |
| random | 2 | original ('6') | '4' | 0.006 / 0.920 / 0.068 |

### C2-0430 (fit): bridge spider, j = 1, lockers [['dog', 2], ['spider', 5], ['fox', 6]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (k):The locker of the dog is 2.⟧⟦slot1 (j): The locker of the spider is 5.⟧⟦slot2 (k): The locker of the fox is 6.⟧ Sam picked the⟦bridge: spider⟧. Victor picked the fox. Sara picked the dog.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('5') | '8' | 0.000 / 0.999 / 0.000 |
| swap | 0 | target ('2') | '8' | 0.966 / 0.027 / 0.003 |
| random | 0 | original ('5') | '8' | 0.000 / 0.999 / 0.000 |
| swap | 2 | original ('5') | '8' | 0.000 / 0.998 / 0.001 |
| random | 2 | original ('5') | '8' | 0.000 / 0.999 / 0.000 |

### C2-0475 (fit): bridge fly, j = 0, lockers [['fly', 7], ['turkey', 2], ['dog', 9]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (j):The locker of the fly is 7.⟧⟦slot1 (k): The locker of the turkey is 2.⟧⟦slot2 (k): The locker of the dog is 9.⟧ Ivan picked the dog. Sara picked the turkey. Victor picked the⟦bridge: fly⟧.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('7') | '6' | 0.971 / 0.005 / 0.010 |
| swap | 1 | third ('9') | '6' | 0.059 / 0.356 / 0.465 |
| random | 1 | original ('7') | '6' | 0.944 / 0.007 / 0.025 |
| swap | 2 | target ('9') | '6' | 0.022 / 0.123 / 0.637 |
| random | 2 | original ('7') | '6' | 0.973 / 0.006 / 0.006 |

### C2-0492 (fit): bridge cat, j = 0, lockers [['cat', 4], ['duck', 8], ['bear', 5]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (j):The locker of the cat is 4.⟧⟦slot1 (k): The locker of the duck is 8.⟧⟦slot2 (k): The locker of the bear is 5.⟧ Lily picked the bear. Frank picked the duck. Anna picked the⟦bridge: cat⟧.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('4') | '4' | 0.988 / 0.007 / 0.001 |
| swap | 1 | target ('8') | '4' | 0.004 / 0.974 / 0.019 |
| random | 1 | original ('4') | '4' | 0.978 / 0.013 / 0.002 |
| swap | 2 | third ('8') | '4' | 0.009 / 0.878 / 0.097 |
| random | 2 | original ('4') | '4' | 0.988 / 0.006 / 0.002 |

### C2-0511 (fit): bridge owl, j = 0, lockers [['owl', 2], ['butterfly', 1], ['lion', 4]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (j):The locker of the owl is 2.⟧⟦slot1 (k): The locker of the butterfly is 1.⟧⟦slot2 (k): The locker of the lion is 4.⟧ Eve picked the lion. Carl picked the butterfly. Zoe picked the⟦bridge: owl⟧.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('2') | '2' | 0.887 / 0.069 / 0.017 |
| swap | 1 | target ('1') | '2' | 0.014 / 0.741 / 0.228 |
| random | 1 | original ('2') | '2' | 0.896 / 0.069 / 0.012 |
| swap | 2 | target ('4') | '4' | 0.010 / 0.224 / 0.708 |
| random | 2 | original ('2') | '2' | 0.894 / 0.065 / 0.015 |

### C2-0567 (fit): bridge tick, j = 1, lockers [['elephant', 4], ['tick', 2], ['deer', 3]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (k):The locker of the elephant is 4.⟧⟦slot1 (j): The locker of the tick is 2.⟧⟦slot2 (k): The locker of the deer is 3.⟧ Fiona picked the⟦bridge: tick⟧. Zoe picked the elephant. Tom picked the deer.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('2') | '8' | 0.001 / 0.999 / 0.000 |
| swap | 0 | target ('4') | '4' | 0.962 / 0.028 / 0.005 |
| random | 0 | original ('2') | '8' | 0.001 / 0.998 / 0.001 |
| swap | 2 | original ('2') | '8' | 0.000 / 0.996 / 0.004 |
| random | 2 | original ('2') | '8' | 0.001 / 0.999 / 0.001 |

### C2-0575 (fit): bridge ant, j = 0, lockers [['ant', 2], ['tiger', 4], ['bear', 6]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (j):The locker of the ant is 2.⟧⟦slot1 (k): The locker of the tiger is 4.⟧⟦slot2 (k): The locker of the bear is 6.⟧ Lily picked the bear. Carl picked the⟦bridge: ant⟧. Eve picked the tiger.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('2') | '6' | 0.775 / 0.159 / 0.034 |
| swap | 1 | target ('4') | '4' | 0.000 / 0.911 / 0.083 |
| random | 1 | original ('2') | '6' | 0.855 / 0.104 / 0.013 |
| swap | 2 | target ('6') | '4' | 0.001 / 0.198 / 0.782 |
| random | 2 | original ('2') | '6' | 0.866 / 0.094 / 0.023 |

### C2-0602 (fit): bridge ant, j = 2, lockers [['cat', 9], ['eagle', 1], ['ant', 4]]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
⟦slot0 (k):The locker of the cat is 9.⟧⟦slot1 (k): The locker of the eagle is 1.⟧⟦slot2 (j): The locker of the ant is 4.⟧ Sam picked the⟦bridge: ant⟧. Adam picked the eagle. Grace picked the cat.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('4') | '6' | 0.000 / 0.002 / 0.998 |
| swap | 0 | target ('9') | '4' | 0.959 / 0.004 / 0.035 |
| random | 0 | original ('4') | '6' | 0.000 / 0.002 / 0.997 |
| swap | 1 | original ('4') | '6' | 0.000 / 0.002 / 0.997 |
| random | 1 | original ('4') | '6' | 0.000 / 0.002 / 0.998 |

