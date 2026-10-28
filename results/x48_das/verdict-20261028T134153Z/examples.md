# 48.1 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word where R R^T Delta is added at L. UNVERIFIED.

## qwen35_9b_x48_das_r2 at L12: 10 random test pairs of 19 (seed 0)

### P2-L0-0039 (animals): bridge spider → rabbit; the whole change switches: lookup 1, recall 1 (stored)

S's context: Victor picked the spider. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the bee is 9. Nina picked the rabbit.

**lookup** (PP-L0-0039): O's answer 2, S's answer 8; in this reader's pairs: 1

```
<|im_start|>user
Victor picked the rabbit. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the bee is 9. Nina picked the ⟦bridge:spider⟧.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '2' | 0 | 1 |
| whole | '8' | 1 | 0 |
| R_PP_k1 | '2' | 0 | 1 |
| R_PM_k1 | '2' | 0 | 1 |
| rand_k1 | '2' | 0 | 1 |
| shuf_PP_k1 | '2' | 0 | 1 |
| shuf_PM_k1 | '2' | 0 | 1 |
| R_PP_k4 | '2' | 0 | 1 |
| R_PM_k4 | '8' | 1 | 0 |
| rand_k4 | '2' | 0 | 1 |
| shuf_PP_k4 | '2' | 0 | 1 |
| shuf_PM_k4 | '2' | 0 | 1 |
| R_PP_k16 | '8' | 1 | 0 |
| R_PM_k16 | '2' | 0 | 1 |
| rand_k16 | '2' | 0 | 1 |
| shuf_PP_k16 | '2' | 0 | 1 |
| shuf_PM_k16 | '2' | 0 | 1 |
| R_PP_k64 | '2' | 0 | 1 |
| R_PM_k64 | '2' | 0 | 1 |
| rand_k64 | '2' | 0 | 1 |
| shuf_PP_k64 | '2' | 0 | 1 |
| shuf_PM_k64 | '2' | 0 | 1 |

**recall** (PM-L0-0039): O's answer 8, S's answer 4; in this reader's pairs: 1

```
<|im_start|>user
Victor picked the rabbit. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the bee is 9. Nina picked the ⟦bridge:spider⟧.
How many legs does Nina's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '4' | 1 | 0 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '4' | 1 | 0 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0059 (greek): bridge gamma → iota; the whole change switches: lookup 1, recall 1 (stored)

S's context: Paul picked gamma. The locker of beta is 9. The locker of gamma is 7. The locker of iota is 3. Fiona picked iota. Ivan picked beta.

**lookup** (PP-L0-0059): O's answer 7, S's answer 3; in this reader's pairs: 1

```
<|im_start|>user
Paul picked iota. The locker of beta is 9. The locker of gamma is 7. The locker of iota is 3. Fiona picked ⟦bridge:gamma⟧. Ivan picked beta.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '7' | 0 | 1 |
| whole | '3' | 1 | 0 |
| R_PP_k1 | '7' | 0 | 1 |
| R_PM_k1 | '7' | 0 | 1 |
| rand_k1 | '7' | 0 | 1 |
| shuf_PP_k1 | '7' | 0 | 1 |
| shuf_PM_k1 | '7' | 0 | 1 |
| R_PP_k4 | '7' | 0 | 1 |
| R_PM_k4 | '7' | 0 | 1 |
| rand_k4 | '7' | 0 | 1 |
| shuf_PP_k4 | '7' | 0 | 1 |
| shuf_PM_k4 | '7' | 0 | 1 |
| R_PP_k16 | '7' | 0 | 1 |
| R_PM_k16 | '7' | 0 | 1 |
| rand_k16 | '7' | 0 | 1 |
| shuf_PP_k16 | '7' | 0 | 1 |
| shuf_PM_k16 | '7' | 0 | 1 |
| R_PP_k64 | '7' | 0 | 1 |
| R_PM_k64 | '7' | 0 | 1 |
| rand_k64 | '7' | 0 | 1 |
| shuf_PP_k64 | '7' | 0 | 1 |
| shuf_PM_k64 | '7' | 0 | 1 |

**recall** (PM-L0-0059): O's answer 3, S's answer 9; in this reader's pairs: 1

```
<|im_start|>user
Paul picked iota. The locker of beta is 9. The locker of gamma is 7. The locker of iota is 3. Fiona picked ⟦bridge:gamma⟧. Ivan picked beta.
Which position in the Greek alphabet does Fiona's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '3' | 0 | 1 |
| whole | '9' | 1 | 0 |
| R_PP_k1 | '3' | 0 | 1 |
| R_PM_k1 | '3' | 0 | 1 |
| rand_k1 | '3' | 0 | 1 |
| shuf_PP_k1 | '3' | 0 | 1 |
| shuf_PM_k1 | '3' | 0 | 1 |
| R_PP_k4 | '3' | 0 | 1 |
| R_PM_k4 | '3' | 0 | 1 |
| rand_k4 | '3' | 0 | 1 |
| shuf_PP_k4 | '3' | 0 | 1 |
| shuf_PM_k4 | '3' | 0 | 1 |
| R_PP_k16 | '3' | 0 | 1 |
| R_PM_k16 | '3' | 0 | 1 |
| rand_k16 | '3' | 0 | 1 |
| shuf_PP_k16 | '3' | 0 | 1 |
| shuf_PM_k16 | '3' | 0 | 1 |
| R_PP_k64 | '3' | 0 | 1 |
| R_PM_k64 | '3' | 0 | 1 |
| rand_k64 | '3' | 0 | 1 |
| shuf_PP_k64 | '3' | 0 | 1 |
| shuf_PM_k64 | '3' | 0 | 1 |

### P2-L0-0060 (animals): bridge spider → duck; the whole change switches: lookup 1, recall 1 (stored)

S's context: The locker of the spider is nine. Ivan picked the spider. The locker of the goat is one. The locker of the duck is five. Kyle picked the duck. Anna picked the goat.

**lookup** (PP-L0-0060): O's answer 9, S's answer 5; in this reader's pairs: 1

```
<|im_start|>user
The locker of the spider is nine. Ivan picked the duck. The locker of the goat is one. The locker of the duck is five. Kyle picked the ⟦bridge:spider⟧. Anna picked the goat.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '9' | 0 | 1 |
| whole | '5' | 1 | 0 |
| R_PP_k1 | '5' | 1 | 0 |
| R_PM_k1 | '5' | 1 | 0 |
| rand_k1 | '9' | 0 | 1 |
| shuf_PP_k1 | '5' | 1 | 0 |
| shuf_PM_k1 | '9' | 0 | 1 |
| R_PP_k4 | '5' | 1 | 0 |
| R_PM_k4 | '5' | 1 | 0 |
| rand_k4 | '9' | 0 | 1 |
| shuf_PP_k4 | '5' | 1 | 0 |
| shuf_PM_k4 | '9' | 0 | 1 |
| R_PP_k16 | '5' | 1 | 0 |
| R_PM_k16 | '9' | 0 | 1 |
| rand_k16 | '9' | 0 | 1 |
| shuf_PP_k16 | '9' | 0 | 1 |
| shuf_PM_k16 | '5' | 1 | 0 |
| R_PP_k64 | '5' | 1 | 0 |
| R_PM_k64 | '9' | 0 | 1 |
| rand_k64 | '9' | 0 | 1 |
| shuf_PP_k64 | '9' | 0 | 1 |
| shuf_PM_k64 | '9' | 0 | 1 |

**recall** (PM-L0-0060): O's answer 8, S's answer 2; in this reader's pairs: 1

```
<|im_start|>user
The locker of the spider is nine. Ivan picked the duck. The locker of the goat is one. The locker of the duck is five. Kyle picked the ⟦bridge:spider⟧. Anna picked the goat.
How many legs does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '2' | 1 | 0 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '8' | 0 | 1 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0063 (animals): bridge spider → owl; the whole change switches: lookup 1, recall 1 (stored)

S's context: Leo picked the sheep. The locker of the spider is three. The locker of the owl is four. Alice picked the spider. Grace picked the owl. The locker of the sheep is one.

**lookup** (PP-L0-0063): O's answer 3, S's answer 4; in this reader's pairs: 1

```
<|im_start|>user
Leo picked the sheep. The locker of the spider is three. The locker of the owl is four. Alice picked the owl. Grace picked the ⟦bridge:spider⟧. The locker of the sheep is one.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '3' | 0 | 1 |
| whole | '4' | 1 | 0 |
| R_PP_k1 | '3' | 0 | 1 |
| R_PM_k1 | '3' | 0 | 1 |
| rand_k1 | '3' | 0 | 1 |
| shuf_PP_k1 | '3' | 0 | 1 |
| shuf_PM_k1 | '3' | 0 | 1 |
| R_PP_k4 | '3' | 0 | 1 |
| R_PM_k4 | '3' | 0 | 1 |
| rand_k4 | '3' | 0 | 1 |
| shuf_PP_k4 | '3' | 0 | 1 |
| shuf_PM_k4 | '3' | 0 | 1 |
| R_PP_k16 | '4' | 1 | 0 |
| R_PM_k16 | '3' | 0 | 1 |
| rand_k16 | '3' | 0 | 1 |
| shuf_PP_k16 | '3' | 0 | 1 |
| shuf_PM_k16 | '3' | 0 | 1 |
| R_PP_k64 | '4' | 1 | 0 |
| R_PM_k64 | '3' | 0 | 1 |
| rand_k64 | '3' | 0 | 1 |
| shuf_PP_k64 | '3' | 0 | 1 |
| shuf_PM_k64 | '3' | 0 | 1 |

**recall** (PM-L0-0063): O's answer 8, S's answer 2; in this reader's pairs: 1

```
<|im_start|>user
Leo picked the sheep. The locker of the spider is three. The locker of the owl is four. Alice picked the owl. Grace picked the ⟦bridge:spider⟧. The locker of the sheep is one.
How many legs does Grace's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '2' | 1 | 0 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '8' | 0 | 1 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0078 (animals): bridge wolf → chicken; the whole change switches: lookup 1, recall 1 (stored)

S's context: Hugo picked the wolf. The locker of the wolf is six. The locker of the chicken is four. Beth picked the mouse. The locker of the mouse is three. Jack picked the chicken.

**lookup** (PP-L0-0078): O's answer 6, S's answer 4; in this reader's pairs: 1

```
<|im_start|>user
Hugo picked the chicken. The locker of the wolf is six. The locker of the chicken is four. Beth picked the mouse. The locker of the mouse is three. Jack picked the ⟦bridge:wolf⟧.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '6' | 0 | 1 |
| whole | '4' | 1 | 0 |
| R_PP_k1 | '6' | 0 | 1 |
| R_PM_k1 | '6' | 0 | 1 |
| rand_k1 | '6' | 0 | 1 |
| shuf_PP_k1 | '6' | 0 | 1 |
| shuf_PM_k1 | '6' | 0 | 1 |
| R_PP_k4 | '2' | 0 | 0 |
| R_PM_k4 | '6' | 0 | 1 |
| rand_k4 | '6' | 0 | 1 |
| shuf_PP_k4 | '6' | 0 | 1 |
| shuf_PM_k4 | '6' | 0 | 1 |
| R_PP_k16 | '2' | 0 | 0 |
| R_PM_k16 | '6' | 0 | 1 |
| rand_k16 | '6' | 0 | 1 |
| shuf_PP_k16 | '6' | 0 | 1 |
| shuf_PM_k16 | '6' | 0 | 1 |
| R_PP_k64 | '2' | 0 | 0 |
| R_PM_k64 | '6' | 0 | 1 |
| rand_k64 | '6' | 0 | 1 |
| shuf_PP_k64 | '6' | 0 | 1 |
| shuf_PM_k64 | '6' | 0 | 1 |

**recall** (PM-L0-0078): O's answer 4, S's answer 2; in this reader's pairs: 1

```
<|im_start|>user
Hugo picked the chicken. The locker of the wolf is six. The locker of the chicken is four. Beth picked the mouse. The locker of the mouse is three. Jack picked the ⟦bridge:wolf⟧.
How many legs does Jack's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '4' | 0 | 1 |
| whole | '2' | 1 | 0 |
| R_PP_k1 | '4' | 0 | 1 |
| R_PM_k1 | '4' | 0 | 1 |
| rand_k1 | '4' | 0 | 1 |
| shuf_PP_k1 | '4' | 0 | 1 |
| shuf_PM_k1 | '4' | 0 | 1 |
| R_PP_k4 | '4' | 0 | 1 |
| R_PM_k4 | '4' | 0 | 1 |
| rand_k4 | '4' | 0 | 1 |
| shuf_PP_k4 | '4' | 0 | 1 |
| shuf_PM_k4 | '4' | 0 | 1 |
| R_PP_k16 | '4' | 0 | 1 |
| R_PM_k16 | '4' | 0 | 1 |
| rand_k16 | '4' | 0 | 1 |
| shuf_PP_k16 | '4' | 0 | 1 |
| shuf_PM_k16 | '4' | 0 | 1 |
| R_PP_k64 | '4' | 0 | 1 |
| R_PM_k64 | '4' | 0 | 1 |
| rand_k64 | '4' | 0 | 1 |
| shuf_PP_k64 | '4' | 0 | 1 |
| shuf_PM_k64 | '4' | 0 | 1 |

### P2-L0-0084 (animals): bridge spider → turkey; the whole change switches: lookup 1, recall 1 (stored)

S's context: The locker of the turkey is 1. The locker of the horse is 2. The locker of the spider is 9. Maria picked the turkey. Anna picked the spider. Will picked the horse.

**lookup** (PP-L0-0084): O's answer 9, S's answer 1; in this reader's pairs: 1

```
<|im_start|>user
The locker of the turkey is 1. The locker of the horse is 2. The locker of the spider is 9. Maria picked the ⟦bridge:spider⟧. Anna picked the turkey. Will picked the horse.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '9' | 0 | 1 |
| whole | '1' | 1 | 0 |
| R_PP_k1 | '1' | 1 | 0 |
| R_PM_k1 | '9' | 0 | 1 |
| rand_k1 | '9' | 0 | 1 |
| shuf_PP_k1 | '9' | 0 | 1 |
| shuf_PM_k1 | '1' | 1 | 0 |
| R_PP_k4 | '1' | 1 | 0 |
| R_PM_k4 | '1' | 1 | 0 |
| rand_k4 | '9' | 0 | 1 |
| shuf_PP_k4 | '9' | 0 | 1 |
| shuf_PM_k4 | '9' | 0 | 1 |
| R_PP_k16 | '1' | 1 | 0 |
| R_PM_k16 | '1' | 1 | 0 |
| rand_k16 | '9' | 0 | 1 |
| shuf_PP_k16 | '9' | 0 | 1 |
| shuf_PM_k16 | '9' | 0 | 1 |
| R_PP_k64 | '1' | 1 | 0 |
| R_PM_k64 | '1' | 1 | 0 |
| rand_k64 | '9' | 0 | 1 |
| shuf_PP_k64 | '1' | 1 | 0 |
| shuf_PM_k64 | '9' | 0 | 1 |

**recall** (PM-L0-0084): O's answer 8, S's answer 2; in this reader's pairs: 1

```
<|im_start|>user
The locker of the turkey is 1. The locker of the horse is 2. The locker of the spider is 9. Maria picked the ⟦bridge:spider⟧. Anna picked the turkey. Will picked the horse.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '2' | 1 | 0 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '2' | 1 | 0 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '4' | 0 | 0 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '4' | 0 | 0 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0115 (elements): bridge oxygen → hydrogen; the whole change switches: lookup 1, recall 1 (stored)

S's context: The locker of hydrogen is 7. Victor picked carbon. The locker of oxygen is 5. Zoe picked hydrogen. The locker of carbon is 1. Olivia picked oxygen.

**lookup** (PP-L0-0115): O's answer 5, S's answer 7; in this reader's pairs: 1

```
<|im_start|>user
The locker of hydrogen is 7. Victor picked carbon. The locker of oxygen is 5. Zoe picked ⟦bridge:oxygen⟧. The locker of carbon is 1. Olivia picked hydrogen.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '5' | 0 | 1 |
| whole | '7' | 1 | 0 |
| R_PP_k1 | '7' | 1 | 0 |
| R_PM_k1 | '7' | 1 | 0 |
| rand_k1 | '5' | 0 | 1 |
| shuf_PP_k1 | '5' | 0 | 1 |
| shuf_PM_k1 | '5' | 0 | 1 |
| R_PP_k4 | '7' | 1 | 0 |
| R_PM_k4 | '5' | 0 | 1 |
| rand_k4 | '5' | 0 | 1 |
| shuf_PP_k4 | '5' | 0 | 1 |
| shuf_PM_k4 | '5' | 0 | 1 |
| R_PP_k16 | '7' | 1 | 0 |
| R_PM_k16 | '7' | 1 | 0 |
| rand_k16 | '5' | 0 | 1 |
| shuf_PP_k16 | '5' | 0 | 1 |
| shuf_PM_k16 | '5' | 0 | 1 |
| R_PP_k64 | '7' | 1 | 0 |
| R_PM_k64 | '7' | 1 | 0 |
| rand_k64 | '5' | 0 | 1 |
| shuf_PP_k64 | '5' | 0 | 1 |
| shuf_PM_k64 | '5' | 0 | 1 |

**recall** (PM-L0-0115): O's answer 8, S's answer 1; in this reader's pairs: 1

```
<|im_start|>user
The locker of hydrogen is 7. Victor picked carbon. The locker of oxygen is 5. Zoe picked ⟦bridge:oxygen⟧. The locker of carbon is 1. Olivia picked hydrogen.
What is the atomic number of Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '1' | 1 | 0 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '8' | 0 | 1 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0139 (elements): bridge oxygen → nitrogen; the whole change switches: lookup 1, recall 1 (stored)

S's context: Hugo picked oxygen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked nitrogen.

**lookup** (PP-L0-0139): O's answer 6, S's answer 9; in this reader's pairs: 1

```
<|im_start|>user
Hugo picked nitrogen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked ⟦bridge:oxygen⟧.
Which locker belongs to Ruby's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '6' | 0 | 1 |
| whole | '9' | 1 | 0 |
| R_PP_k1 | '9' | 1 | 0 |
| R_PM_k1 | '6' | 0 | 1 |
| rand_k1 | '6' | 0 | 1 |
| shuf_PP_k1 | '6' | 0 | 1 |
| shuf_PM_k1 | '6' | 0 | 1 |
| R_PP_k4 | '9' | 1 | 0 |
| R_PM_k4 | '6' | 0 | 1 |
| rand_k4 | '6' | 0 | 1 |
| shuf_PP_k4 | '6' | 0 | 1 |
| shuf_PM_k4 | '6' | 0 | 1 |
| R_PP_k16 | '9' | 1 | 0 |
| R_PM_k16 | '6' | 0 | 1 |
| rand_k16 | '6' | 0 | 1 |
| shuf_PP_k16 | '6' | 0 | 1 |
| shuf_PM_k16 | '6' | 0 | 1 |
| R_PP_k64 | '9' | 1 | 0 |
| R_PM_k64 | '6' | 0 | 1 |
| rand_k64 | '6' | 0 | 1 |
| shuf_PP_k64 | '6' | 0 | 1 |
| shuf_PM_k64 | '6' | 0 | 1 |

**recall** (PM-L0-0139): O's answer 8, S's answer 7; in this reader's pairs: 1

```
<|im_start|>user
Hugo picked nitrogen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked ⟦bridge:oxygen⟧.
What is the atomic number of Ruby's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '7' | 1 | 0 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '7' | 1 | 0 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '7' | 1 | 0 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '7' | 1 | 0 |

### P2-L0-0218 (greek): bridge gamma → epsilon; the whole change switches: lookup 1, recall 1 (stored)

S's context: The locker of gamma is 8. The locker of epsilon is 6. Mark picked gamma. Clara picked epsilon. The locker of theta is 3. Finn picked theta.

**lookup** (PP-L0-0218): O's answer 8, S's answer 6; in this reader's pairs: 1

```
<|im_start|>user
The locker of gamma is 8. The locker of epsilon is 6. Mark picked epsilon. Clara picked ⟦bridge:gamma⟧. The locker of theta is 3. Finn picked theta.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '6' | 1 | 0 |
| R_PP_k1 | '6' | 1 | 0 |
| R_PM_k1 | '6' | 1 | 0 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '7' | 0 | 0 |
| shuf_PM_k1 | '7' | 0 | 0 |
| R_PP_k4 | '6' | 1 | 0 |
| R_PM_k4 | '6' | 1 | 0 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '6' | 1 | 0 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '6' | 1 | 0 |
| R_PM_k16 | '6' | 1 | 0 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '6' | 1 | 0 |
| R_PP_k64 | '6' | 1 | 0 |
| R_PM_k64 | '6' | 1 | 0 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

**recall** (PM-L0-0218): O's answer 3, S's answer 5; in this reader's pairs: 1

```
<|im_start|>user
The locker of gamma is 8. The locker of epsilon is 6. Mark picked epsilon. Clara picked ⟦bridge:gamma⟧. The locker of theta is 3. Finn picked theta.
Which position in the Greek alphabet does Clara's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '3' | 0 | 1 |
| whole | '5' | 1 | 0 |
| R_PP_k1 | '3' | 0 | 1 |
| R_PM_k1 | '5' | 1 | 0 |
| rand_k1 | '3' | 0 | 1 |
| shuf_PP_k1 | '3' | 0 | 1 |
| shuf_PM_k1 | '3' | 0 | 1 |
| R_PP_k4 | '5' | 1 | 0 |
| R_PM_k4 | '5' | 1 | 0 |
| rand_k4 | '3' | 0 | 1 |
| shuf_PP_k4 | '5' | 1 | 0 |
| shuf_PM_k4 | '3' | 0 | 1 |
| R_PP_k16 | '5' | 1 | 0 |
| R_PM_k16 | '5' | 1 | 0 |
| rand_k16 | '3' | 0 | 1 |
| shuf_PP_k16 | '5' | 1 | 0 |
| shuf_PM_k16 | '5' | 1 | 0 |
| R_PP_k64 | '5' | 1 | 0 |
| R_PM_k64 | '5' | 1 | 0 |
| rand_k64 | '3' | 0 | 1 |
| shuf_PP_k64 | '5' | 1 | 0 |
| shuf_PM_k64 | '3' | 0 | 1 |

### P2-L0-0253 (elements): bridge oxygen → lithium; the whole change switches: lookup 1, recall 1 (stored)

S's context: The locker of lithium is 6. Oscar picked oxygen. The locker of oxygen is 9. The locker of hydrogen is 5. Ivan picked lithium. Mia picked hydrogen.

**lookup** (PP-L0-0253): O's answer 9, S's answer 6; in this reader's pairs: 1

```
<|im_start|>user
The locker of lithium is 6. Oscar picked lithium. The locker of oxygen is 9. The locker of hydrogen is 5. Ivan picked ⟦bridge:oxygen⟧. Mia picked hydrogen.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '9' | 0 | 1 |
| whole | '6' | 1 | 0 |
| R_PP_k1 | '6' | 1 | 0 |
| R_PM_k1 | '6' | 1 | 0 |
| rand_k1 | '9' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 0 |
| shuf_PM_k1 | '6' | 1 | 0 |
| R_PP_k4 | '6' | 1 | 0 |
| R_PM_k4 | '6' | 1 | 0 |
| rand_k4 | '9' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 0 |
| shuf_PM_k4 | '9' | 0 | 1 |
| R_PP_k16 | '6' | 1 | 0 |
| R_PM_k16 | '6' | 1 | 0 |
| rand_k16 | '9' | 0 | 1 |
| shuf_PP_k16 | '9' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 0 |
| R_PP_k64 | '6' | 1 | 0 |
| R_PM_k64 | '6' | 1 | 0 |
| rand_k64 | '9' | 0 | 1 |
| shuf_PP_k64 | '6' | 1 | 0 |
| shuf_PM_k64 | '6' | 1 | 0 |

**recall** (PM-L0-0253): O's answer 8, S's answer 3; in this reader's pairs: 1

```
<|im_start|>user
The locker of lithium is 6. Oscar picked lithium. The locker of oxygen is 9. The locker of hydrogen is 5. Ivan picked ⟦bridge:oxygen⟧. Mia picked hydrogen.
What is the atomic number of Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '3' | 1 | 0 |
| R_PP_k1 | '6' | 0 | 0 |
| R_PM_k1 | '3' | 1 | 0 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '6' | 0 | 0 |
| R_PM_k4 | '3' | 1 | 0 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '6' | 0 | 0 |
| R_PM_k16 | '3' | 1 | 0 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '6' | 0 | 0 |
| R_PM_k64 | '3' | 1 | 0 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '6' | 0 | 0 |

## muse30_x48_das at L26: 9 random test pairs of 9 (seed 0)

### P2-L0-0039 (animals): bridge spider → rabbit; the whole change switches: lookup 0, recall 1 (stored)

S's context: Victor picked the spider. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the bee is 9. Nina picked the rabbit.

**lookup** (PP-L0-0039): O's answer 2, S's answer 8; in this reader's pairs: 0

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Victor picked the rabbit. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the bee is 9. Nina picked the ⟦bridge:spider⟧.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '2' | 0 | 1 |
| whole | '2' | 0 | 1 |
| R_PP_k1 | '2' | 0 | 1 |
| R_PM_k1 | '2' | 0 | 1 |
| rand_k1 | '2' | 0 | 1 |
| shuf_PP_k1 | '2' | 0 | 1 |
| shuf_PM_k1 | '2' | 0 | 1 |
| R_PP_k4 | '2' | 0 | 1 |
| R_PM_k4 | '2' | 0 | 1 |
| rand_k4 | '2' | 0 | 1 |
| shuf_PP_k4 | '2' | 0 | 1 |
| shuf_PM_k4 | '2' | 0 | 1 |
| R_PP_k16 | '2' | 0 | 1 |
| R_PM_k16 | '2' | 0 | 1 |
| rand_k16 | '2' | 0 | 1 |
| shuf_PP_k16 | '2' | 0 | 1 |
| shuf_PM_k16 | '2' | 0 | 1 |
| R_PP_k64 | '2' | 0 | 1 |
| R_PM_k64 | '2' | 0 | 1 |
| rand_k64 | '2' | 0 | 1 |
| shuf_PP_k64 | '2' | 0 | 1 |
| shuf_PM_k64 | '2' | 0 | 1 |

**recall** (PM-L0-0039): O's answer 8, S's answer 4; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Victor picked the rabbit. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the bee is 9. Nina picked the ⟦bridge:spider⟧.
How many legs does Nina's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '4' | 1 | 0 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '8' | 0 | 1 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0060 (animals): bridge spider → duck; the whole change switches: lookup 1, recall 0 (stored)

S's context: The locker of the spider is nine. Ivan picked the spider. The locker of the goat is one. The locker of the duck is five. Kyle picked the duck. Anna picked the goat.

**lookup** (PP-L0-0060): O's answer 9, S's answer 5; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is nine. Ivan picked the duck. The locker of the goat is one. The locker of the duck is five. Kyle picked the ⟦bridge:spider⟧. Anna picked the goat.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '9' | 0 | 1 |
| whole | '5' | 1 | 0 |
| R_PP_k1 | '9' | 0 | 1 |
| R_PM_k1 | '9' | 0 | 1 |
| rand_k1 | '9' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 0 |
| shuf_PM_k1 | '9' | 0 | 1 |
| R_PP_k4 | '5' | 1 | 0 |
| R_PM_k4 | '9' | 0 | 1 |
| rand_k4 | '9' | 0 | 1 |
| shuf_PP_k4 | '9' | 0 | 1 |
| shuf_PM_k4 | '9' | 0 | 1 |
| R_PP_k16 | '5' | 1 | 0 |
| R_PM_k16 | '9' | 0 | 1 |
| rand_k16 | '9' | 0 | 1 |
| shuf_PP_k16 | '9' | 0 | 1 |
| shuf_PM_k16 | '9' | 0 | 1 |
| R_PP_k64 | '5' | 1 | 0 |
| R_PM_k64 | '9' | 0 | 1 |
| rand_k64 | '9' | 0 | 1 |
| shuf_PP_k64 | '9' | 0 | 1 |
| shuf_PM_k64 | '9' | 0 | 1 |

**recall** (PM-L0-0060): O's answer 8, S's answer 2; in this reader's pairs: 0

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is nine. Ivan picked the duck. The locker of the goat is one. The locker of the duck is five. Kyle picked the ⟦bridge:spider⟧. Anna picked the goat.
How many legs does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '8' | 0 | 1 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '8' | 0 | 1 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0063 (animals): bridge spider → owl; the whole change switches: lookup 1, recall 0 (stored)

S's context: Leo picked the sheep. The locker of the spider is three. The locker of the owl is four. Alice picked the spider. Grace picked the owl. The locker of the sheep is one.

**lookup** (PP-L0-0063): O's answer 3, S's answer 4; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Leo picked the sheep. The locker of the spider is three. The locker of the owl is four. Alice picked the owl. Grace picked the ⟦bridge:spider⟧. The locker of the sheep is one.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '3' | 0 | 1 |
| whole | '4' | 1 | 0 |
| R_PP_k1 | '3' | 0 | 1 |
| R_PM_k1 | '3' | 0 | 1 |
| rand_k1 | '3' | 0 | 1 |
| shuf_PP_k1 | '3' | 0 | 1 |
| shuf_PM_k1 | '3' | 0 | 1 |
| R_PP_k4 | '4' | 1 | 0 |
| R_PM_k4 | '3' | 0 | 1 |
| rand_k4 | '3' | 0 | 1 |
| shuf_PP_k4 | '3' | 0 | 1 |
| shuf_PM_k4 | '3' | 0 | 1 |
| R_PP_k16 | '4' | 1 | 0 |
| R_PM_k16 | '3' | 0 | 1 |
| rand_k16 | '3' | 0 | 1 |
| shuf_PP_k16 | '3' | 0 | 1 |
| shuf_PM_k16 | '3' | 0 | 1 |
| R_PP_k64 | '4' | 1 | 0 |
| R_PM_k64 | '3' | 0 | 1 |
| rand_k64 | '3' | 0 | 1 |
| shuf_PP_k64 | '3' | 0 | 1 |
| shuf_PM_k64 | '3' | 0 | 1 |

**recall** (PM-L0-0063): O's answer 8, S's answer 2; in this reader's pairs: 0

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Leo picked the sheep. The locker of the spider is three. The locker of the owl is four. Alice picked the owl. Grace picked the ⟦bridge:spider⟧. The locker of the sheep is one.
How many legs does Grace's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '8' | 0 | 1 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '8' | 0 | 1 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0078 (animals): bridge wolf → chicken; the whole change switches: lookup 1, recall 1 (stored)

S's context: Hugo picked the wolf. The locker of the wolf is six. The locker of the chicken is four. Beth picked the mouse. The locker of the mouse is three. Jack picked the chicken.

**lookup** (PP-L0-0078): O's answer 6, S's answer 4; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Hugo picked the chicken. The locker of the wolf is six. The locker of the chicken is four. Beth picked the mouse. The locker of the mouse is three. Jack picked the ⟦bridge:wolf⟧.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '6' | 0 | 1 |
| whole | '4' | 1 | 0 |
| R_PP_k1 | '6' | 0 | 1 |
| R_PM_k1 | '6' | 0 | 1 |
| rand_k1 | '6' | 0 | 1 |
| shuf_PP_k1 | '6' | 0 | 1 |
| shuf_PM_k1 | '6' | 0 | 1 |
| R_PP_k4 | '6' | 0 | 1 |
| R_PM_k4 | '6' | 0 | 1 |
| rand_k4 | '6' | 0 | 1 |
| shuf_PP_k4 | '6' | 0 | 1 |
| shuf_PM_k4 | '6' | 0 | 1 |
| R_PP_k16 | '6' | 0 | 1 |
| R_PM_k16 | '6' | 0 | 1 |
| rand_k16 | '6' | 0 | 1 |
| shuf_PP_k16 | '6' | 0 | 1 |
| shuf_PM_k16 | '6' | 0 | 1 |
| R_PP_k64 | '6' | 0 | 1 |
| R_PM_k64 | '6' | 0 | 1 |
| rand_k64 | '6' | 0 | 1 |
| shuf_PP_k64 | '6' | 0 | 1 |
| shuf_PM_k64 | '6' | 0 | 1 |

**recall** (PM-L0-0078): O's answer 4, S's answer 2; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Hugo picked the chicken. The locker of the wolf is six. The locker of the chicken is four. Beth picked the mouse. The locker of the mouse is three. Jack picked the ⟦bridge:wolf⟧.
How many legs does Jack's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '4' | 0 | 1 |
| whole | '2' | 1 | 0 |
| R_PP_k1 | '4' | 0 | 1 |
| R_PM_k1 | '4' | 0 | 1 |
| rand_k1 | '4' | 0 | 1 |
| shuf_PP_k1 | '4' | 0 | 1 |
| shuf_PM_k1 | '4' | 0 | 1 |
| R_PP_k4 | '4' | 0 | 1 |
| R_PM_k4 | '4' | 0 | 1 |
| rand_k4 | '4' | 0 | 1 |
| shuf_PP_k4 | '4' | 0 | 1 |
| shuf_PM_k4 | '4' | 0 | 1 |
| R_PP_k16 | '4' | 0 | 1 |
| R_PM_k16 | '4' | 0 | 1 |
| rand_k16 | '4' | 0 | 1 |
| shuf_PP_k16 | '4' | 0 | 1 |
| shuf_PM_k16 | '4' | 0 | 1 |
| R_PP_k64 | '4' | 0 | 1 |
| R_PM_k64 | '4' | 0 | 1 |
| rand_k64 | '4' | 0 | 1 |
| shuf_PP_k64 | '4' | 0 | 1 |
| shuf_PM_k64 | '4' | 0 | 1 |

### P2-L0-0084 (animals): bridge spider → turkey; the whole change switches: lookup 1, recall 1 (stored)

S's context: The locker of the turkey is 1. The locker of the horse is 2. The locker of the spider is 9. Maria picked the turkey. Anna picked the spider. Will picked the horse.

**lookup** (PP-L0-0084): O's answer 9, S's answer 1; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 1. The locker of the horse is 2. The locker of the spider is 9. Maria picked the ⟦bridge:spider⟧. Anna picked the turkey. Will picked the horse.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '9' | 0 | 1 |
| whole | '1' | 1 | 0 |
| R_PP_k1 | '9' | 0 | 1 |
| R_PM_k1 | '9' | 0 | 1 |
| rand_k1 | '9' | 0 | 1 |
| shuf_PP_k1 | '1' | 1 | 0 |
| shuf_PM_k1 | '9' | 0 | 1 |
| R_PP_k4 | '9' | 0 | 1 |
| R_PM_k4 | '9' | 0 | 1 |
| rand_k4 | '9' | 0 | 1 |
| shuf_PP_k4 | '9' | 0 | 1 |
| shuf_PM_k4 | '9' | 0 | 1 |
| R_PP_k16 | '9' | 0 | 1 |
| R_PM_k16 | '9' | 0 | 1 |
| rand_k16 | '9' | 0 | 1 |
| shuf_PP_k16 | '9' | 0 | 1 |
| shuf_PM_k16 | '9' | 0 | 1 |
| R_PP_k64 | '1' | 1 | 0 |
| R_PM_k64 | '9' | 0 | 1 |
| rand_k64 | '9' | 0 | 1 |
| shuf_PP_k64 | '9' | 0 | 1 |
| shuf_PM_k64 | '9' | 0 | 1 |

**recall** (PM-L0-0084): O's answer 8, S's answer 2; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 1. The locker of the horse is 2. The locker of the spider is 9. Maria picked the ⟦bridge:spider⟧. Anna picked the turkey. Will picked the horse.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '2' | 1 | 0 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '8' | 0 | 1 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0213 (animals): bridge goose → bee; the whole change switches: lookup 1, recall 0 (stored)

S's context: The locker of the bee is three. The locker of the beetle is one. The locker of the goose is four. Hugo picked the beetle. Noah picked the goose. Rose picked the bee.

**lookup** (PP-L0-0213): O's answer 4, S's answer 3; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is three. The locker of the beetle is one. The locker of the goose is four. Hugo picked the beetle. Noah picked the bee. Rose picked the ⟦bridge:goose⟧.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '4' | 0 | 1 |
| whole | '3' | 1 | 0 |
| R_PP_k1 | '4' | 0 | 1 |
| R_PM_k1 | '3' | 1 | 0 |
| rand_k1 | '4' | 0 | 1 |
| shuf_PP_k1 | '3' | 1 | 0 |
| shuf_PM_k1 | '4' | 0 | 1 |
| R_PP_k4 | '3' | 1 | 0 |
| R_PM_k4 | '3' | 1 | 0 |
| rand_k4 | '4' | 0 | 1 |
| shuf_PP_k4 | '4' | 0 | 1 |
| shuf_PM_k4 | '4' | 0 | 1 |
| R_PP_k16 | '3' | 1 | 0 |
| R_PM_k16 | '3' | 1 | 0 |
| rand_k16 | '4' | 0 | 1 |
| shuf_PP_k16 | '4' | 0 | 1 |
| shuf_PM_k16 | '4' | 0 | 1 |
| R_PP_k64 | '3' | 1 | 0 |
| R_PM_k64 | '3' | 1 | 0 |
| rand_k64 | '4' | 0 | 1 |
| shuf_PP_k64 | '4' | 0 | 1 |
| shuf_PM_k64 | '4' | 0 | 1 |

**recall** (PM-L0-0213): O's answer 2, S's answer 6; in this reader's pairs: 0

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is three. The locker of the beetle is one. The locker of the goose is four. Hugo picked the beetle. Noah picked the bee. Rose picked the ⟦bridge:goose⟧.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '2' | 0 | 1 |
| whole | '2' | 0 | 1 |
| R_PP_k1 | '2' | 0 | 1 |
| R_PM_k1 | '2' | 0 | 1 |
| rand_k1 | '2' | 0 | 1 |
| shuf_PP_k1 | '2' | 0 | 1 |
| shuf_PM_k1 | '2' | 0 | 1 |
| R_PP_k4 | '2' | 0 | 1 |
| R_PM_k4 | '2' | 0 | 1 |
| rand_k4 | '2' | 0 | 1 |
| shuf_PP_k4 | '2' | 0 | 1 |
| shuf_PM_k4 | '2' | 0 | 1 |
| R_PP_k16 | '2' | 0 | 1 |
| R_PM_k16 | '2' | 0 | 1 |
| rand_k16 | '2' | 0 | 1 |
| shuf_PP_k16 | '2' | 0 | 1 |
| shuf_PM_k16 | '2' | 0 | 1 |
| R_PP_k64 | '2' | 0 | 1 |
| R_PM_k64 | '2' | 0 | 1 |
| rand_k64 | '2' | 0 | 1 |
| shuf_PP_k64 | '2' | 0 | 1 |
| shuf_PM_k64 | '2' | 0 | 1 |

### P2-L0-0221 (greek): bridge beta → delta; the whole change switches: lookup 1, recall 1 (stored)

S's context: The locker of delta is nine. The locker of beta is one. Owen picked iota. Iris picked delta. The locker of iota is five. Mark picked beta.

**lookup** (PP-L0-0221): O's answer 1, S's answer 9; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of delta is nine. The locker of beta is one. Owen picked iota. Iris picked ⟦bridge:beta⟧. The locker of iota is five. Mark picked delta.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '1' | 0 | 1 |
| whole | '9' | 1 | 0 |
| R_PP_k1 | '1' | 0 | 1 |
| R_PM_k1 | '1' | 0 | 1 |
| rand_k1 | '1' | 0 | 1 |
| shuf_PP_k1 | '1' | 0 | 1 |
| shuf_PM_k1 | '1' | 0 | 1 |
| R_PP_k4 | '9' | 1 | 0 |
| R_PM_k4 | '1' | 0 | 1 |
| rand_k4 | '1' | 0 | 1 |
| shuf_PP_k4 | '1' | 0 | 1 |
| shuf_PM_k4 | '1' | 0 | 1 |
| R_PP_k16 | '9' | 1 | 0 |
| R_PM_k16 | '1' | 0 | 1 |
| rand_k16 | '1' | 0 | 1 |
| shuf_PP_k16 | '1' | 0 | 1 |
| shuf_PM_k16 | '1' | 0 | 1 |
| R_PP_k64 | '9' | 1 | 0 |
| R_PM_k64 | '1' | 0 | 1 |
| rand_k64 | '1' | 0 | 1 |
| shuf_PP_k64 | '1' | 0 | 1 |
| shuf_PM_k64 | '1' | 0 | 1 |

**recall** (PM-L0-0221): O's answer 2, S's answer 4; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of delta is nine. The locker of beta is one. Owen picked iota. Iris picked ⟦bridge:beta⟧. The locker of iota is five. Mark picked delta.
Which position in the Greek alphabet does Iris's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '2' | 0 | 1 |
| whole | '4' | 1 | 0 |
| R_PP_k1 | '2' | 0 | 1 |
| R_PM_k1 | '2' | 0 | 1 |
| rand_k1 | '2' | 0 | 1 |
| shuf_PP_k1 | '2' | 0 | 1 |
| shuf_PM_k1 | '2' | 0 | 1 |
| R_PP_k4 | '4' | 1 | 0 |
| R_PM_k4 | '2' | 0 | 1 |
| rand_k4 | '2' | 0 | 1 |
| shuf_PP_k4 | '2' | 0 | 1 |
| shuf_PM_k4 | '2' | 0 | 1 |
| R_PP_k16 | '4' | 1 | 0 |
| R_PM_k16 | '2' | 0 | 1 |
| rand_k16 | '2' | 0 | 1 |
| shuf_PP_k16 | '2' | 0 | 1 |
| shuf_PM_k16 | '2' | 0 | 1 |
| R_PP_k64 | '4' | 1 | 0 |
| R_PM_k64 | '2' | 0 | 1 |
| rand_k64 | '2' | 0 | 1 |
| shuf_PP_k64 | '2' | 0 | 1 |
| shuf_PM_k64 | '2' | 0 | 1 |

### P2-L0-0243 (animals): bridge spider → tiger; the whole change switches: lookup 1, recall 0 (stored)

S's context: The locker of the spider is four. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the tiger. Alice picked the spider. Henry picked the sheep.

**lookup** (PP-L0-0243): O's answer 4, S's answer 6; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is four. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the ⟦bridge:spider⟧. Alice picked the tiger. Henry picked the sheep.
Which locker belongs to Olivia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '4' | 0 | 1 |
| whole | '6' | 1 | 0 |
| R_PP_k1 | '4' | 0 | 1 |
| R_PM_k1 | '4' | 0 | 1 |
| rand_k1 | '4' | 0 | 1 |
| shuf_PP_k1 | '4' | 0 | 1 |
| shuf_PM_k1 | '4' | 0 | 1 |
| R_PP_k4 | '4' | 0 | 1 |
| R_PM_k4 | '4' | 0 | 1 |
| rand_k4 | '4' | 0 | 1 |
| shuf_PP_k4 | '4' | 0 | 1 |
| shuf_PM_k4 | '4' | 0 | 1 |
| R_PP_k16 | '4' | 0 | 1 |
| R_PM_k16 | '4' | 0 | 1 |
| rand_k16 | '4' | 0 | 1 |
| shuf_PP_k16 | '4' | 0 | 1 |
| shuf_PM_k16 | '4' | 0 | 1 |
| R_PP_k64 | '4' | 0 | 1 |
| R_PM_k64 | '4' | 0 | 1 |
| rand_k64 | '4' | 0 | 1 |
| shuf_PP_k64 | '4' | 0 | 1 |
| shuf_PM_k64 | '4' | 0 | 1 |

**recall** (PM-L0-0243): O's answer 8, S's answer 4; in this reader's pairs: 0

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is four. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the ⟦bridge:spider⟧. Alice picked the tiger. Henry picked the sheep.
How many legs does Olivia's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '8' | 0 | 1 |
| whole | '8' | 0 | 1 |
| R_PP_k1 | '8' | 0 | 1 |
| R_PM_k1 | '8' | 0 | 1 |
| rand_k1 | '8' | 0 | 1 |
| shuf_PP_k1 | '8' | 0 | 1 |
| shuf_PM_k1 | '8' | 0 | 1 |
| R_PP_k4 | '8' | 0 | 1 |
| R_PM_k4 | '8' | 0 | 1 |
| rand_k4 | '8' | 0 | 1 |
| shuf_PP_k4 | '8' | 0 | 1 |
| shuf_PM_k4 | '8' | 0 | 1 |
| R_PP_k16 | '8' | 0 | 1 |
| R_PM_k16 | '8' | 0 | 1 |
| rand_k16 | '8' | 0 | 1 |
| shuf_PP_k16 | '8' | 0 | 1 |
| shuf_PM_k16 | '8' | 0 | 1 |
| R_PP_k64 | '8' | 0 | 1 |
| R_PM_k64 | '8' | 0 | 1 |
| rand_k64 | '8' | 0 | 1 |
| shuf_PP_k64 | '8' | 0 | 1 |
| shuf_PM_k64 | '8' | 0 | 1 |

### P2-L0-0287 (greek): bridge gamma → theta; the whole change switches: lookup 1, recall 1 (stored)

S's context: Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked theta. Ryan picked gamma. The locker of epsilon is eight.

**lookup** (PP-L0-0287): O's answer 4, S's answer 5; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked ⟦bridge:gamma⟧. Ryan picked theta. The locker of epsilon is eight.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '4' | 0 | 1 |
| whole | '5' | 1 | 0 |
| R_PP_k1 | '4' | 0 | 1 |
| R_PM_k1 | '4' | 0 | 1 |
| rand_k1 | '4' | 0 | 1 |
| shuf_PP_k1 | '4' | 0 | 1 |
| shuf_PM_k1 | '4' | 0 | 1 |
| R_PP_k4 | '5' | 1 | 0 |
| R_PM_k4 | '4' | 0 | 1 |
| rand_k4 | '4' | 0 | 1 |
| shuf_PP_k4 | '4' | 0 | 1 |
| shuf_PM_k4 | '4' | 0 | 1 |
| R_PP_k16 | '5' | 1 | 0 |
| R_PM_k16 | '4' | 0 | 1 |
| rand_k16 | '4' | 0 | 1 |
| shuf_PP_k16 | '4' | 0 | 1 |
| shuf_PM_k16 | '4' | 0 | 1 |
| R_PP_k64 | '5' | 1 | 0 |
| R_PM_k64 | '4' | 0 | 1 |
| rand_k64 | '4' | 0 | 1 |
| shuf_PP_k64 | '4' | 0 | 1 |
| shuf_PM_k64 | '4' | 0 | 1 |

**recall** (PM-L0-0287): O's answer 3, S's answer 8; in this reader's pairs: 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked ⟦bridge:gamma⟧. Ryan picked theta. The locker of epsilon is eight.
Which position in the Greek alphabet does Ella's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | switched | right |
|---|---|---|---|
| none | '3' | 0 | 1 |
| whole | '8' | 1 | 0 |
| R_PP_k1 | '3' | 0 | 1 |
| R_PM_k1 | '3' | 0 | 1 |
| rand_k1 | '3' | 0 | 1 |
| shuf_PP_k1 | '3' | 0 | 1 |
| shuf_PM_k1 | '3' | 0 | 1 |
| R_PP_k4 | '3' | 0 | 1 |
| R_PM_k4 | '3' | 0 | 1 |
| rand_k4 | '3' | 0 | 1 |
| shuf_PP_k4 | '3' | 0 | 1 |
| shuf_PM_k4 | '3' | 0 | 1 |
| R_PP_k16 | '3' | 0 | 1 |
| R_PM_k16 | '3' | 0 | 1 |
| rand_k16 | '3' | 0 | 1 |
| shuf_PP_k16 | '3' | 0 | 1 |
| shuf_PM_k16 | '3' | 0 | 1 |
| R_PP_k64 | '3' | 0 | 1 |
| R_PM_k64 | '3' | 0 | 1 |
| rand_k64 | '3' | 0 | 1 |
| shuf_PP_k64 | '3' | 0 | 1 |
| shuf_PM_k64 | '3' | 0 | 1 |

