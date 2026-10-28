# 49.7 view (verify pack): the lookup's prompt exactly as the model reads it. UNVERIFIED.

## qwen35_9b_x49_7 (qwen3.5-9b): 10 random items of 300 (seed 0); best head L27:h1

### C2-0035 (read): bridge goat, j = 2, lockers [['beetle', 2], ['tiger', 4], ['goat', 9]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('24') | '19' | 0.001 / 0.005 / 0.888 |
| swap | 0 | original ('24') | '21' | 0.008 / 0.005 / 0.876 |
| random | 0 | original ('24') | '19' | 0.001 / 0.004 / 0.901 |
| swap | 1 | original ('24') | '19' | 0.001 / 0.005 / 0.932 |
| random | 1 | original ('24') | '19' | 0.001 / 0.005 / 0.907 |

### C2-0235 (read): bridge crow, j = 2, lockers [['fox', 5], ['ant', 3], ['crow', 4]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('19') | '17' | 0.015 / 0.006 / 0.632 |
| swap | 0 | target ('20') | '19' | 0.852 / 0.004 / 0.028 |
| random | 0 | original ('19') | '17' | 0.017 / 0.005 / 0.630 |
| swap | 1 | original ('19') | '17' | 0.021 / 0.014 / 0.590 |
| random | 1 | original ('19') | '17' | 0.014 / 0.006 / 0.643 |

### C2-0280 (read): bridge cow, j = 1, lockers [['chicken', 3], ['cow', 8], ['spider', 6]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('23') | '19' | 0.019 / 0.750 / 0.030 |
| swap | 0 | target ('18') | '19' | 0.617 / 0.083 / 0.026 |
| random | 0 | original ('23') | '19' | 0.018 / 0.747 / 0.033 |
| swap | 2 | original ('23') | '19' | 0.021 / 0.512 / 0.092 |
| random | 2 | original ('23') | '19' | 0.021 / 0.717 / 0.032 |

### C2-0337 (read): bridge turkey, j = 0, lockers [['turkey', 7], ['tick', 1], ['rabbit', 8]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('22') | '17' | 0.835 / 0.011 / 0.003 |
| swap | 1 | target ('16') | '17' | 0.055 / 0.718 / 0.007 |
| random | 1 | original ('22') | '17' | 0.826 / 0.011 / 0.003 |
| swap | 2 | third ('16') | '17' | 0.057 / 0.293 / 0.024 |
| random | 2 | original ('22') | '17' | 0.823 / 0.010 / 0.003 |

### C2-0367 (read): bridge pig, j = 2, lockers [['bee', 9], ['butterfly', 8], ['pig', 4]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('19') | '19' | 0.012 / 0.013 / 0.685 |
| swap | 0 | original ('19') | '19' | 0.111 / 0.005 / 0.579 |
| random | 0 | original ('19') | '19' | 0.013 / 0.014 / 0.689 |
| swap | 1 | original ('19') | '19' | 0.017 / 0.015 / 0.671 |
| random | 1 | original ('19') | '19' | 0.013 / 0.013 / 0.685 |

### C2-0378 (read): bridge duck, j = 2, lockers [['fox', 9], ['deer', 1], ['duck', 4]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('19') | '17' | 0.007 / 0.003 / 0.847 |
| swap | 0 | target ('24') | '17' | 0.543 / 0.006 / 0.142 |
| random | 0 | original ('19') | '17' | 0.006 / 0.003 / 0.856 |
| swap | 1 | original ('19') | '17' | 0.007 / 0.008 / 0.876 |
| random | 1 | original ('19') | '17' | 0.008 / 0.003 / 0.841 |

### C2-0390 (read): bridge owl, j = 1, lockers [['bee', 9], ['owl', 4], ['mouse', 8]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('19') | '17' | 0.019 / 0.788 / 0.004 |
| swap | 0 | target ('24') | '21' | 0.786 / 0.038 / 0.003 |
| random | 0 | original ('19') | '17' | 0.019 / 0.797 / 0.004 |
| swap | 2 | original ('19') | '17' | 0.022 / 0.787 / 0.004 |
| random | 2 | original ('19') | '17' | 0.019 / 0.787 / 0.004 |

### C2-0438 (read): bridge dog, j = 2, lockers [['beetle', 9], ['sheep', 6], ['dog', 7]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('22') | '19' | 0.019 / 0.010 / 0.661 |
| swap | 0 | target ('24') | '21' | 0.657 / 0.014 / 0.063 |
| random | 0 | original ('22') | '19' | 0.017 / 0.009 / 0.661 |
| swap | 1 | original ('22') | '19' | 0.027 / 0.018 / 0.639 |
| random | 1 | original ('22') | '19' | 0.020 / 0.010 / 0.657 |

### C2-0447 (fit): bridge bee, j = 1, lockers [['goat', 7], ['bee', 5], ['rabbit', 2]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('20') | '21' | 0.018 / 0.864 / 0.003 |
| swap | 0 | target ('22') | '21' | 0.653 / 0.086 / 0.009 |
| random | 0 | original ('20') | '21' | 0.019 / 0.880 / 0.003 |
| swap | 2 | original ('20') | '21' | 0.026 / 0.594 / 0.017 |
| random | 2 | original ('20') | '21' | 0.017 / 0.857 / 0.004 |

### C2-0475 (read): bridge crow, j = 0, lockers [['crow', 1], ['lion', 2], ['fox', 5]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('16') | '17' | 0.676 / 0.040 / 0.007 |
| swap | 1 | target ('17') | '17' | 0.104 / 0.716 / 0.009 |
| random | 1 | original ('16') | '17' | 0.673 / 0.040 / 0.006 |
| swap | 2 | target ('20') | '17' | 0.018 / 0.009 / 0.885 |
| random | 2 | original ('16') | '17' | 0.685 / 0.039 / 0.007 |

## muse30_x49_7 (muse-glimmer-30b): 10 random items of 300 (seed 0); best head L39:h1

### C2-0039 (fit): bridge dog, j = 1, lockers [['bee', 9], ['dog', 7], ['cow', 8]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('35') | '32' | 0.038 / 0.937 / 0.003 |
| swap | 0 | target ('37') | '32' | 0.943 / 0.036 / 0.002 |
| random | 0 | original ('35') | '32' | 0.033 / 0.947 / 0.002 |
| swap | 2 | original ('35') | '32' | 0.054 / 0.901 / 0.006 |
| random | 2 | original ('35') | '32' | 0.037 / 0.940 / 0.003 |

### C2-0278 (fit): bridge owl, j = 2, lockers [['cow', 1], ['camel', 6], ['owl', 8]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('36') | '30' | 0.001 / 0.476 / 0.497 |
| swap | 0 | third ('34') | '30' | 0.030 / 0.797 / 0.090 |
| random | 0 | original ('36') | '30' | 0.001 / 0.453 / 0.522 |
| swap | 1 | target ('34') | '30' | 0.001 / 0.636 / 0.342 |
| random | 1 | original ('36') | '30' | 0.001 / 0.343 / 0.635 |

### C2-0324 (fit): bridge butterfly, j = 2, lockers [['spider', 1], ['zebra', 2], ['butterfly', 5]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('33') | '34' | 0.003 / 0.171 / 0.796 |
| swap | 0 | third ('30') | '34' | 0.156 / 0.365 / 0.381 |
| random | 0 | original ('33') | '34' | 0.003 / 0.074 / 0.899 |
| swap | 1 | target ('30') | '34' | 0.005 / 0.579 / 0.389 |
| random | 1 | original ('33') | '34' | 0.003 / 0.202 / 0.764 |

### C2-0385 (fit): bridge horse, j = 0, lockers [['horse', 7], ['turkey', 2], ['lion', 9]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('35') | '32' | 0.993 / 0.004 / 0.000 |
| swap | 1 | target ('30') | '32' | 0.013 / 0.969 / 0.005 |
| random | 1 | original ('35') | '32' | 0.993 / 0.004 / 0.000 |
| swap | 2 | third ('30') | '32' | 0.075 / 0.821 / 0.052 |
| random | 2 | original ('35') | '32' | 0.993 / 0.004 / 0.000 |

### C2-0414 (read): bridge tiger, j = 0, lockers [['tiger', 5], ['fox', 2], ['duck', 8]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('33') | '32' | 0.967 / 0.018 / 0.005 |
| swap | 1 | target ('30') | '30' | 0.007 / 0.923 / 0.036 |
| random | 1 | original ('33') | '32' | 0.970 / 0.017 / 0.004 |
| swap | 2 | target ('36') | '30' | 0.013 / 0.396 / 0.533 |
| random | 2 | original ('33') | '32' | 0.965 / 0.018 / 0.006 |

### C2-0441 (read): bridge deer, j = 0, lockers [['deer', 6], ['pig', 2], ['goose', 4]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('34') | '32' | 0.979 / 0.009 / 0.002 |
| swap | 1 | third ('32') | '32' | 0.009 / 0.017 / 0.950 |
| random | 1 | original ('34') | '32' | 0.976 / 0.009 / 0.002 |
| swap | 2 | target ('32') | '32' | 0.006 / 0.006 / 0.968 |
| random | 2 | original ('34') | '32' | 0.967 / 0.013 / 0.003 |

### C2-0459 (fit): bridge pig, j = 1, lockers [['eagle', 9], ['pig', 5], ['fox', 7]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('33') | '32' | 0.013 / 0.946 / 0.016 |
| swap | 0 | original ('33') | '32' | 0.363 / 0.508 / 0.077 |
| random | 0 | original ('33') | '32' | 0.012 / 0.935 / 0.025 |
| swap | 2 | original ('33') | '32' | 0.010 / 0.715 / 0.230 |
| random | 2 | original ('33') | '32' | 0.012 / 0.935 / 0.023 |

### C2-0523 (read): bridge rabbit, j = 2, lockers [['turkey', 1], ['spider', 3], ['rabbit', 7]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('35') | '32' | 0.003 / 0.007 / 0.974 |
| swap | 0 | target ('29') | '32' | 0.902 / 0.041 / 0.025 |
| random | 0 | original ('35') | '32' | 0.003 / 0.007 / 0.974 |
| swap | 1 | original ('35') | '32' | 0.005 / 0.019 / 0.948 |
| random | 1 | original ('35') | '32' | 0.003 / 0.007 / 0.973 |

### C2-0530 (fit): bridge mouse, j = 0, lockers [['mouse', 9], ['butterfly', 1], ['owl', 2]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('37') | '32' | 0.974 / 0.017 / 0.001 |
| swap | 1 | target ('29') | '32' | 0.037 / 0.944 / 0.005 |
| random | 1 | original ('37') | '32' | 0.974 / 0.017 / 0.001 |
| swap | 2 | third ('29') | '32' | 0.026 / 0.949 / 0.008 |
| random | 2 | original ('37') | '32' | 0.971 / 0.020 / 0.001 |

### C2-0560 (fit): bridge owl, j = 1, lockers [['bear', 2], ['owl', 6], ['mouse', 8]]

```
(tokenizer of another target)
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('34') | '30' | 0.011 / 0.904 / 0.033 |
| swap | 0 | target ('30') | '30' | 0.925 / 0.049 / 0.006 |
| random | 0 | original ('34') | '30' | 0.011 / 0.876 / 0.046 |
| swap | 2 | original ('34') | '30' | 0.008 / 0.821 / 0.095 |
| random | 2 | original ('34') | '30' | 0.009 / 0.918 / 0.028 |

## x49_7_27b (qwen3.6-27b): 10 random items of 300 (seed 0); best head L51:h20

### C2-0028 (read): bridge fly, j = 0, lockers [['fly', 3], ['duck', 6], ['bee', 4]]

```
<|im_start|>user
⟦slot0 (j):The locker of the fly is 3.⟧⟦slot1 (k): The locker of the duck is 6.⟧⟦slot2 (k): The locker of the bee is 4.⟧ Lucy picked the duck. Sam picked the⟦bridge: fly⟧. Liam picked the bee.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('3') | '6' | 0.979 / 0.004 / 0.000 |
| swap | 1 | target ('6') | '6' | 0.006 / 0.984 / 0.001 |
| random | 1 | original ('3') | '6' | 0.977 / 0.003 / 0.001 |
| swap | 2 | third ('6') | '6' | 0.001 / 0.995 / 0.000 |
| random | 2 | original ('3') | '6' | 0.973 / 0.008 / 0.001 |

### C2-0199 (read): bridge tick, j = 0, lockers [['tick', 7], ['fly', 9], ['bee', 6]]

```
<|im_start|>user
⟦slot0 (j):The locker of the tick is 7.⟧⟦slot1 (k): The locker of the fly is 9.⟧⟦slot2 (k): The locker of the bee is 6.⟧ Vera picked the bee. James picked the fly. Owen picked the⟦bridge: tick⟧.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('7') | '8' | 0.714 / 0.008 / 0.008 |
| swap | 1 | original ('7') | '8' | 0.809 / 0.077 / 0.012 |
| random | 1 | original ('7') | '8' | 0.790 / 0.008 / 0.007 |
| swap | 2 | original ('7') | '8' | 0.625 / 0.056 / 0.019 |
| random | 2 | original ('7') | '8' | 0.697 / 0.007 / 0.007 |

### C2-0231 (read): bridge pig, j = 1, lockers [['butterfly', 7], ['pig', 1], ['beetle', 3]]

```
<|im_start|>user
⟦slot0 (k):The locker of the butterfly is 7.⟧⟦slot1 (j): The locker of the pig is 1.⟧⟦slot2 (k): The locker of the beetle is 3.⟧ Paul picked the butterfly. Vera picked the⟦bridge: pig⟧. Mark picked the beetle.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('1') | '4' | 0.017 / 0.813 / 0.005 |
| swap | 0 | original ('1') | '4' | 0.055 / 0.795 / 0.007 |
| random | 0 | original ('1') | '4' | 0.016 / 0.829 / 0.005 |
| swap | 2 | original ('1') | '4' | 0.009 / 0.869 / 0.003 |
| random | 2 | original ('1') | '4' | 0.015 / 0.826 / 0.004 |

### C2-0271 (read): bridge pig, j = 0, lockers [['pig', 4], ['bear', 6], ['chicken', 1]]

```
<|im_start|>user
⟦slot0 (j):The locker of the pig is 4.⟧⟦slot1 (k): The locker of the bear is 6.⟧⟦slot2 (k): The locker of the chicken is 1.⟧ Beth picked the⟦bridge: pig⟧. David picked the bear. Oscar picked the chicken.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('4') | '4' | 0.483 / 0.013 / 0.016 |
| swap | 1 | target ('6') | '4' | 0.067 / 0.908 / 0.000 |
| random | 1 | original ('4') | '4' | 0.523 / 0.013 / 0.016 |
| swap | 2 | target ('1') | '4' | 0.577 / 0.003 / 0.377 |
| random | 2 | original ('4') | '4' | 0.583 / 0.011 / 0.013 |

### C2-0293 (fit): bridge mouse, j = 2, lockers [['butterfly', 4], ['fly', 1], ['mouse', 6]]

```
<|im_start|>user
⟦slot0 (k):The locker of the butterfly is 4.⟧⟦slot1 (k): The locker of the fly is 1.⟧⟦slot2 (j): The locker of the mouse is 6.⟧ Mark picked the butterfly. Anna picked the fly. Noah picked the⟦bridge: mouse⟧.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('6') | '4' | 0.013 / 0.007 / 0.863 |
| swap | 0 | original ('6') | '4' | 0.017 / 0.004 / 0.916 |
| random | 0 | original ('6') | '4' | 0.012 / 0.006 / 0.882 |
| swap | 1 | original ('6') | '4' | 0.012 / 0.007 / 0.888 |
| random | 1 | original ('6') | '4' | 0.012 / 0.006 / 0.864 |

### C2-0311 (fit): bridge chicken, j = 0, lockers [['chicken', 3], ['camel', 5], ['butterfly', 6]]

```
<|im_start|>user
⟦slot0 (j):The locker of the chicken is 3.⟧⟦slot1 (k): The locker of the camel is 5.⟧⟦slot2 (k): The locker of the butterfly is 6.⟧ Will picked the⟦bridge: chicken⟧. Zoe picked the camel. Noah picked the butterfly.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('3') | '2' | 0.446 / 0.014 / 0.010 |
| swap | 1 | target ('5') | '2' | 0.000 / 0.991 / 0.000 |
| random | 1 | original ('3') | '2' | 0.470 / 0.013 / 0.009 |
| swap | 2 | original ('3') | '2' | 0.476 / 0.188 / 0.075 |
| random | 2 | original ('3') | '2' | 0.508 / 0.014 / 0.009 |

### C2-0324 (read): bridge crow, j = 0, lockers [['crow', 8], ['camel', 1], ['wolf', 2]]

```
<|im_start|>user
⟦slot0 (j):The locker of the crow is 8.⟧⟦slot1 (k): The locker of the camel is 1.⟧⟦slot2 (k): The locker of the wolf is 2.⟧ Laura picked the camel. Vera picked the⟦bridge: crow⟧. Eve picked the wolf.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('8') | '2' | 0.940 / 0.004 / 0.002 |
| swap | 1 | target ('1') | '2' | 0.036 / 0.883 / 0.008 |
| random | 1 | original ('8') | '2' | 0.955 / 0.003 / 0.001 |
| swap | 2 | third ('1') | '2' | 0.019 / 0.877 / 0.007 |
| random | 2 | original ('8') | '2' | 0.959 / 0.003 / 0.001 |

### C2-0369 (read): bridge goat, j = 0, lockers [['goat', 4], ['ant', 5], ['sheep', 7]]

```
<|im_start|>user
⟦slot0 (j):The locker of the goat is 4.⟧⟦slot1 (k): The locker of the ant is 5.⟧⟦slot2 (k): The locker of the sheep is 7.⟧ Emma picked the⟦bridge: goat⟧. Fiona picked the ant. Victor picked the sheep.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('4') | '4' | 0.679 / 0.009 / 0.010 |
| swap | 1 | target ('5') | '4' | 0.002 / 0.987 / 0.000 |
| random | 1 | original ('4') | '4' | 0.703 / 0.009 / 0.009 |
| swap | 2 | target ('7') | '4' | 0.283 / 0.003 / 0.704 |
| random | 2 | original ('4') | '4' | 0.747 / 0.008 / 0.008 |

### C2-0373 (read): bridge fly, j = 1, lockers [['tick', 6], ['fly', 1], ['goose', 9]]

```
<|im_start|>user
⟦slot0 (k):The locker of the tick is 6.⟧⟦slot1 (j): The locker of the fly is 1.⟧⟦slot2 (k): The locker of the goose is 9.⟧ Kyle picked the⟦bridge: fly⟧. Mark picked the goose. Clara picked the tick.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('1') | '6' | 0.007 / 0.946 / 0.004 |
| swap | 0 | target ('6') | '6' | 0.959 / 0.015 / 0.002 |
| random | 0 | original ('1') | '6' | 0.008 / 0.947 / 0.004 |
| swap | 2 | original ('1') | '6' | 0.003 / 0.965 / 0.003 |
| random | 2 | original ('1') | '6' | 0.006 / 0.953 / 0.003 |

### C2-0390 (fit): bridge owl, j = 1, lockers [['bee', 9], ['owl', 4], ['mouse', 8]]

```
<|im_start|>user
⟦slot0 (k):The locker of the bee is 9.⟧⟦slot1 (j): The locker of the owl is 4.⟧⟦slot2 (k): The locker of the mouse is 8.⟧ Mark picked the bee. Zoe picked the⟦bridge: owl⟧. Peter picked the mouse.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| arm | k | lookup | recall | best head mass slot 0 / 1 / 2 (last token) |
|---|---|---|---|---|
| none | - | original ('4') | '2' | 0.020 / 0.798 / 0.006 |
| swap | 0 | original ('4') | '2' | 0.033 / 0.897 / 0.003 |
| random | 0 | original ('4') | '2' | 0.023 / 0.789 / 0.007 |
| swap | 2 | original ('4') | '2' | 0.014 / 0.828 / 0.004 |
| random | 2 | original ('4') | '2' | 0.019 / 0.805 / 0.006 |

