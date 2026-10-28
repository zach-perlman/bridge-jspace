# 47.3 view (verify pack): prompts exactly as the model reads them; ⟦…⟧ the cue token where the change is added. UNVERIFIED.

## x47_cue_27b (qwen3.6-27b, L32): 10 random scenes of 300 (random.Random(0) over the sorted scenes)

### C2-0037 (fit half): O's pick spider ('webs') -> S's eagle ('soaring'); routes {'identity': 9, 'position': 6, 'value': 7, 'original': 4}

**lookup**: O's answer 4, S's 7

O, as read:

```
<|im_start|>user
The locker of the spider is 4. The locker of the eagle is 9. The locker of the fox is 6. Grace picked the one known for⟦ webs⟧. Kate picked the fox. Max picked the eagle.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the spider is 4. The locker of the fox is 6. The locker of the eagle is 7. Grace picked the one known for⟦ soaring⟧. Kate picked the fox. Max picked the eagle.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '4' | original | 0 |
| no_jpp | '4' | original | 0 |
| no_jpp_rand | '4' | original | 0 |
| no_alf | '4' | original | 0 |
| no_alf_rand | '4' | original | 0 |
| no_pcf | '4' | original | 0 |
| no_pcf_rand | '4' | original | 0 |

**recall**: O's answer 8, S's 2

O, as read:

```
<|im_start|>user
The locker of the spider is 4. The locker of the eagle is 9. The locker of the fox is 6. Grace picked the one known for⟦ webs⟧. Kate picked the fox. Max picked the eagle.
How many legs does Grace's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the spider is 4. The locker of the fox is 6. The locker of the eagle is 7. Grace picked the one known for⟦ soaring⟧. Kate picked the fox. Max picked the eagle.
How many legs does Grace's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '8' |  | 0 |
| whole | '8' |  | 0 |
| no_jpp | '8' |  | 0 |
| no_jpp_rand | '8' |  | 0 |
| no_alf | '8' |  | 0 |
| no_alf_rand | '8' |  | 0 |
| no_pcf | '8' |  | 0 |
| no_pcf_rand | '8' |  | 0 |

Elimination read (A's cue -> 'racing', the horse, not in the scene): lookup top '4' (A's locker (found by elimination)).

### C2-0254 (fit half): O's pick cat ('curiosity') -> S's turkey ('Thanksgiving'); routes {'identity': 8, 'position': 6, 'value': 3, 'original': 2}

**lookup**: O's answer 2, S's 3

O, as read:

```
<|im_start|>user
The locker of the turkey is 8. The locker of the cow is 6. The locker of the cat is 2. Ivan picked the one known for⟦ curiosity⟧. Kyle picked the cow. Oscar picked the turkey.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the cow is 6. The locker of the turkey is 3. The locker of the cat is 2. Ivan picked the one known for⟦ Thanksgiving⟧. Kyle picked the cow. Oscar picked the turkey.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' | original | 0 |
| whole | '2' | original | 0 |
| no_jpp | '2' | original | 0 |
| no_jpp_rand | '2' | original | 0 |
| no_alf | '2' | original | 0 |
| no_alf_rand | '2' | original | 0 |
| no_pcf | '2' | original | 0 |
| no_pcf_rand | '2' | original | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|im_start|>user
The locker of the turkey is 8. The locker of the cow is 6. The locker of the cat is 2. Ivan picked the one known for⟦ curiosity⟧. Kyle picked the cow. Oscar picked the turkey.
How many legs does Ivan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the cow is 6. The locker of the turkey is 3. The locker of the cat is 2. Ivan picked the one known for⟦ Thanksgiving⟧. Kyle picked the cow. Oscar picked the turkey.
How many legs does Ivan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'packs', the wolf, not in the scene): lookup top '2' (A's locker (found by elimination)).

### C2-0299 (fit half): O's pick turkey ('Thanksgiving') -> S's sheep ('wool'); routes {'identity': 7, 'position': 5, 'value': 4, 'original': 3}

**lookup**: O's answer 3, S's 4

O, as read:

```
<|im_start|>user
The locker of the sheep is 7. The locker of the fox is 5. The locker of the turkey is 3. Vera picked the one known for⟦ Thanksgiving⟧. Adam picked the sheep. Emma picked the fox.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the fox is 5. The locker of the sheep is 4. The locker of the turkey is 3. Vera picked the one known for⟦ wool⟧. Adam picked the sheep. Emma picked the fox.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '3' | original | 0 |
| whole | '7' | identity | 0 |
| no_jpp | '3' | original | 0 |
| no_jpp_rand | '3' | original | 0 |
| no_alf | '3' | original | 0 |
| no_alf_rand | '7' | identity | 0 |
| no_pcf | '3' | original | 0 |
| no_pcf_rand | '7' | identity | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|im_start|>user
The locker of the sheep is 7. The locker of the fox is 5. The locker of the turkey is 3. Vera picked the one known for⟦ Thanksgiving⟧. Adam picked the sheep. Emma picked the fox.
How many legs does Vera's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the fox is 5. The locker of the sheep is 4. The locker of the turkey is 3. Vera picked the one known for⟦ wool⟧. Adam picked the sheep. Emma picked the fox.
How many legs does Vera's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '2' |  | 0 |
| no_jpp | '2' |  | 0 |
| no_jpp_rand | '2' |  | 0 |
| no_alf | '2' |  | 0 |
| no_alf_rand | '2' |  | 0 |
| no_pcf | '2' |  | 0 |
| no_pcf_rand | '2' |  | 0 |

Elimination read (A's cue -> 'eggs', the chicken, not in the scene): lookup top '3' (A's locker (found by elimination)).

### C2-0372 (test half): O's pick fox ('cunning') -> S's owl ('wisdom'); routes {'identity': 3, 'position': 4, 'value': 2, 'original': 7}

**lookup**: O's answer 7, S's 2

O, as read:

```
<|im_start|>user
The locker of the wolf is 4. The locker of the owl is 3. The locker of the fox is 7. Eve picked the one known for⟦ cunning⟧. Henry picked the wolf. Nina picked the owl.
Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the owl is 2. The locker of the wolf is 4. The locker of the fox is 7. Eve picked the one known for⟦ wisdom⟧. Henry picked the wolf. Nina picked the owl.
Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '3' | identity | 0 |
| no_jpp | '4' | position | 0 |
| no_jpp_rand | '3' | identity | 0 |
| no_alf | '3' | identity | 0 |
| no_alf_rand | '3' | identity | 0 |
| no_pcf | '3' | identity | 0 |
| no_pcf_rand | '3' | identity | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|im_start|>user
The locker of the wolf is 4. The locker of the owl is 3. The locker of the fox is 7. Eve picked the one known for⟦ cunning⟧. Henry picked the wolf. Nina picked the owl.
How many legs does Eve's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the owl is 2. The locker of the wolf is 4. The locker of the fox is 7. Eve picked the one known for⟦ wisdom⟧. Henry picked the wolf. Nina picked the owl.
How many legs does Eve's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'webs', the spider, not in the scene): lookup top '8' (other).

### C2-0399 (fit half): O's pick spider ('webs') -> S's cat ('curiosity'); routes {'identity': 7, 'position': 5, 'value': 1, 'original': 4}

**lookup**: O's answer 4, S's 1

O, as read:

```
<|im_start|>user
The locker of the spider is 4. The locker of the cat is 7. The locker of the horse is 5. Hugo picked the one known for⟦ webs⟧. Eve picked the horse. Clara picked the cat.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the spider is 4. The locker of the horse is 5. The locker of the cat is 1. Hugo picked the one known for⟦ curiosity⟧. Eve picked the horse. Clara picked the cat.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '7' | identity | 0 |
| no_jpp | '4' | original | 0 |
| no_jpp_rand | '4' | original | 0 |
| no_alf | '4' | original | 0 |
| no_alf_rand | '4' | original | 0 |
| no_pcf | '4' | original | 0 |
| no_pcf_rand | '4' | original | 0 |

**recall**: O's answer 8, S's 4

O, as read:

```
<|im_start|>user
The locker of the spider is 4. The locker of the cat is 7. The locker of the horse is 5. Hugo picked the one known for⟦ webs⟧. Eve picked the horse. Clara picked the cat.
How many legs does Hugo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the spider is 4. The locker of the horse is 5. The locker of the cat is 1. Hugo picked the one known for⟦ curiosity⟧. Eve picked the horse. Clara picked the cat.
How many legs does Hugo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '8' |  | 0 |
| whole | '8' |  | 0 |
| no_jpp | '8' |  | 0 |
| no_jpp_rand | '8' |  | 0 |
| no_alf | '8' |  | 0 |
| no_alf_rand | '8' |  | 0 |
| no_pcf | '8' |  | 0 |
| no_pcf_rand | '8' |  | 0 |

Elimination read (A's cue -> 'roaring', the lion, not in the scene): lookup top '4' (A's locker (found by elimination)).

### C2-0423 (test half): O's pick lion ('roaring') -> S's chicken ('eggs'); routes {'identity': 7, 'position': 8, 'value': 1, 'original': 6}

**lookup**: O's answer 6, S's 1

O, as read:

```
<|im_start|>user
The locker of the lion is 6. The locker of the spider is 8. The locker of the chicken is 7. Leo picked the chicken. Mark picked the one known for⟦ roaring⟧. Maria picked the spider.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the lion is 6. The locker of the chicken is 1. The locker of the spider is 8. Leo picked the chicken. Mark picked the one known for⟦ eggs⟧. Maria picked the spider.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '6' | original | 0 |
| whole | '7' | identity | 0 |
| no_jpp | '6' | original | 0 |
| no_jpp_rand | '6' | original | 0 |
| no_alf | '7' | identity | 0 |
| no_alf_rand | '7' | identity | 0 |
| no_pcf | '7' | identity | 0 |
| no_pcf_rand | '7' | identity | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|im_start|>user
The locker of the lion is 6. The locker of the spider is 8. The locker of the chicken is 7. Leo picked the chicken. Mark picked the one known for⟦ roaring⟧. Maria picked the spider.
How many legs does Mark's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the lion is 6. The locker of the chicken is 1. The locker of the spider is 8. Leo picked the chicken. Mark picked the one known for⟦ eggs⟧. Maria picked the spider.
How many legs does Mark's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '2' |  | 1 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '2' |  | 1 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '2' |  | 1 |

Elimination read (A's cue -> 'milk', the cow, not in the scene): lookup top '6' (A's locker (found by elimination)).

### C2-0442 (fit half): O's pick horse ('racing') -> S's eagle ('soaring'); routes {'identity': 6, 'position': 8, 'value': 3, 'original': 7}

**lookup**: O's answer 7, S's 3

O, as read:

```
<|im_start|>user
The locker of the horse is 7. The locker of the eagle is 6. The locker of the lion is 8. Hugo picked the lion. Ruby picked the eagle. Eric picked the one known for⟦ racing⟧.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the horse is 7. The locker of the lion is 8. The locker of the eagle is 3. Hugo picked the lion. Ruby picked the eagle. Eric picked the one known for⟦ soaring⟧.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '6' | identity | 0 |
| no_jpp | '7' | original | 0 |
| no_jpp_rand | '6' | identity | 0 |
| no_alf | '6' | identity | 0 |
| no_alf_rand | '6' | identity | 0 |
| no_pcf | '7' | original | 0 |
| no_pcf_rand | '6' | identity | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|im_start|>user
The locker of the horse is 7. The locker of the eagle is 6. The locker of the lion is 8. Hugo picked the lion. Ruby picked the eagle. Eric picked the one known for⟦ racing⟧.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the horse is 7. The locker of the lion is 8. The locker of the eagle is 3. Hugo picked the lion. Ruby picked the eagle. Eric picked the one known for⟦ soaring⟧.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '2' |  | 1 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '2' |  | 1 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '2' |  | 1 |
| no_pcf | '2' |  | 1 |
| no_pcf_rand | '2' |  | 1 |

Elimination read (A's cue -> 'eggs', the chicken, not in the scene): lookup top '6' (B's locker).

### C2-0496 (test half): O's pick spider ('webs') -> S's cat ('curiosity'); routes {'identity': 9, 'position': 4, 'value': 1, 'original': 7}

**lookup**: O's answer 7, S's 1

O, as read:

```
<|im_start|>user
The locker of the cow is 4. The locker of the cat is 9. The locker of the spider is 7. Grace picked the cow. Laura picked the cat. Ella picked the one known for⟦ webs⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the cat is 1. The locker of the cow is 4. The locker of the spider is 7. Grace picked the cow. Laura picked the cat. Ella picked the one known for⟦ curiosity⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '9' | identity | 0 |
| no_jpp | '7' | original | 0 |
| no_jpp_rand | '7' | original | 0 |
| no_alf | '9' | identity | 0 |
| no_alf_rand | '9' | identity | 0 |
| no_pcf | '7' | original | 0 |
| no_pcf_rand | '9' | identity | 0 |

**recall**: O's answer 8, S's 4

O, as read:

```
<|im_start|>user
The locker of the cow is 4. The locker of the cat is 9. The locker of the spider is 7. Grace picked the cow. Laura picked the cat. Ella picked the one known for⟦ webs⟧.
How many legs does Ella's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the cat is 1. The locker of the cow is 4. The locker of the spider is 7. Grace picked the cow. Laura picked the cat. Ella picked the one known for⟦ curiosity⟧.
How many legs does Ella's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '8' |  | 0 |
| whole | '8' |  | 0 |
| no_jpp | '8' |  | 0 |
| no_jpp_rand | '8' |  | 0 |
| no_alf | '8' |  | 0 |
| no_alf_rand | '8' |  | 0 |
| no_pcf | '8' |  | 0 |
| no_pcf_rand | '8' |  | 0 |

Elimination read (A's cue -> 'cunning', the fox, not in the scene): lookup top '9' (B's locker).

### C2-0502 (test half): O's pick pig ('bacon') -> S's spider ('webs'); routes {'identity': 3, 'position': 7, 'value': 9, 'original': 4}

**lookup**: O's answer 4, S's 9

O, as read:

```
<|im_start|>user
The locker of the pig is 4. The locker of the wolf is 7. The locker of the spider is 3. Will picked the one known for⟦ bacon⟧. Clara picked the wolf. Eric picked the spider.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the pig is 4. The locker of the spider is 9. The locker of the wolf is 7. Will picked the one known for⟦ webs⟧. Clara picked the wolf. Eric picked the spider.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '3' | identity | 0 |
| no_jpp | '4' | original | 0 |
| no_jpp_rand | '4' | original | 0 |
| no_alf | '3' | identity | 0 |
| no_alf_rand | '3' | identity | 0 |
| no_pcf | '4' | original | 0 |
| no_pcf_rand | '3' | identity | 0 |

**recall**: O's answer 4, S's 8

O, as read:

```
<|im_start|>user
The locker of the pig is 4. The locker of the wolf is 7. The locker of the spider is 3. Will picked the one known for⟦ bacon⟧. Clara picked the wolf. Eric picked the spider.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the pig is 4. The locker of the spider is 9. The locker of the wolf is 7. Will picked the one known for⟦ webs⟧. Clara picked the wolf. Eric picked the spider.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'eggs', the chicken, not in the scene): lookup top '4' (A's locker (found by elimination)).

### C2-0538 (test half): O's pick owl ('wisdom') -> S's wolf ('packs'); routes {'identity': 5, 'position': 1, 'value': 4, 'original': 7}

**lookup**: O's answer 7, S's 4

O, as read:

```
<|im_start|>user
The locker of the horse is 1. The locker of the wolf is 5. The locker of the owl is 7. Max picked the one known for⟦ wisdom⟧. Eve picked the wolf. Zoe picked the horse.
Which locker belongs to Max's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the wolf is 4. The locker of the horse is 1. The locker of the owl is 7. Max picked the one known for⟦ packs⟧. Eve picked the wolf. Zoe picked the horse.
Which locker belongs to Max's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '5' | identity | 0 |
| no_jpp | '7' | original | 0 |
| no_jpp_rand | '7' | original | 0 |
| no_alf | '5' | identity | 0 |
| no_alf_rand | '5' | identity | 0 |
| no_pcf | '5' | identity | 0 |
| no_pcf_rand | '5' | identity | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|im_start|>user
The locker of the horse is 1. The locker of the wolf is 5. The locker of the owl is 7. Max picked the one known for⟦ wisdom⟧. Eve picked the wolf. Zoe picked the horse.
How many legs does Max's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the wolf is 4. The locker of the horse is 1. The locker of the owl is 7. Max picked the one known for⟦ packs⟧. Eve picked the wolf. Zoe picked the horse.
How many legs does Max's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '4' |  | 1 |
| no_jpp | '2' |  | 0 |
| no_jpp_rand | '2' |  | 0 |
| no_alf | '2' |  | 0 |
| no_alf_rand | '4' |  | 1 |
| no_pcf | '2' |  | 0 |
| no_pcf_rand | '2' |  | 0 |

Elimination read (A's cue -> 'roaring', the lion, not in the scene): lookup top '1' (C's locker).

## qwen35_9b_x47_cue (qwen3.5-9b, L12): 10 random scenes of 300 (random.Random(0) over the sorted scenes)

### C2-0069 (test half): O's pick turkey ('Thanksgiving') -> S's cow ('milk'); routes {'identity': 2, 'position': 5, 'value': 7, 'original': 9}

**lookup**: O's answer 9, S's 7

O, as read:

```
<|im_start|>user
The locker of the turkey is 9. The locker of the cow is 2. The locker of the sheep is 5. Grace picked the cow. Zoe picked the sheep. Frank picked the one known for⟦ Thanksgiving⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the turkey is 9. The locker of the sheep is 5. The locker of the cow is 7. Grace picked the cow. Zoe picked the sheep. Frank picked the one known for⟦ milk⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '9' | original | 0 |
| whole | '9' | original | 0 |
| no_jpp | '9' | original | 0 |
| no_jpp_rand | '9' | original | 0 |
| no_alf | '9' | original | 0 |
| no_alf_rand | '9' | original | 0 |
| no_pcf | '9' | original | 0 |
| no_pcf_rand | '9' | original | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|im_start|>user
The locker of the turkey is 9. The locker of the cow is 2. The locker of the sheep is 5. Grace picked the cow. Zoe picked the sheep. Frank picked the one known for⟦ Thanksgiving⟧.
How many legs does Frank's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the turkey is 9. The locker of the sheep is 5. The locker of the cow is 7. Grace picked the cow. Zoe picked the sheep. Frank picked the one known for⟦ milk⟧.
How many legs does Frank's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '4' |  | 1 |
| no_jpp | '2' |  | 0 |
| no_jpp_rand | '4' |  | 1 |
| no_alf | '4' |  | 1 |
| no_alf_rand | '4' |  | 1 |
| no_pcf | '2' |  | 0 |
| no_pcf_rand | '4' |  | 1 |

Elimination read (A's cue -> 'bacon', the pig, not in the scene): lookup top '9' (A's locker (found by elimination)).

### C2-0452 (fit half): O's pick cow ('milk') -> S's chicken ('eggs'); routes {'identity': 7, 'position': 8, 'value': 2, 'original': 3}

**lookup**: O's answer 3, S's 2

O, as read:

```
<|im_start|>user
The locker of the dog is 8. The locker of the cow is 3. The locker of the chicken is 7. Ella picked the one known for⟦ milk⟧. Liam picked the dog. Jack picked the chicken.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the chicken is 2. The locker of the cow is 3. The locker of the dog is 8. Ella picked the one known for⟦ eggs⟧. Liam picked the dog. Jack picked the chicken.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '3' | original | 0 |
| whole | '7' | identity | 0 |
| no_jpp | '7' | identity | 0 |
| no_jpp_rand | '7' | identity | 0 |
| no_alf | '7' | identity | 0 |
| no_alf_rand | '7' | identity | 0 |
| no_pcf | '7' | identity | 0 |
| no_pcf_rand | '7' | identity | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|im_start|>user
The locker of the dog is 8. The locker of the cow is 3. The locker of the chicken is 7. Ella picked the one known for⟦ milk⟧. Liam picked the dog. Jack picked the chicken.
How many legs does Ella's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the chicken is 2. The locker of the cow is 3. The locker of the dog is 8. Ella picked the one known for⟦ eggs⟧. Liam picked the dog. Jack picked the chicken.
How many legs does Ella's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '2' |  | 1 |
| no_jpp | '2' |  | 1 |
| no_jpp_rand | '2' |  | 1 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '2' |  | 1 |
| no_pcf | '2' |  | 1 |
| no_pcf_rand | '2' |  | 1 |

Elimination read (A's cue -> 'cunning', the fox, not in the scene): lookup top '7' (B's locker).

### C2-0522 (test half): O's pick eagle ('soaring') -> S's pig ('bacon'); routes {'identity': 4, 'position': 8, 'value': 6, 'original': 7}

**lookup**: O's answer 7, S's 6

O, as read:

```
<|im_start|>user
The locker of the eagle is 7. The locker of the cow is 8. The locker of the pig is 4. Frank picked the cow. Kate picked the one known for⟦ soaring⟧. Jack picked the pig.
Which locker belongs to Kate's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 7. The locker of the pig is 6. The locker of the cow is 8. Frank picked the cow. Kate picked the one known for⟦ bacon⟧. Jack picked the pig.
Which locker belongs to Kate's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '8' | position | 0 |
| no_jpp | '7' | original | 0 |
| no_jpp_rand | '7' | original | 0 |
| no_alf | '8' | position | 0 |
| no_alf_rand | '8' | position | 0 |
| no_pcf | '7' | original | 0 |
| no_pcf_rand | '8' | position | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|im_start|>user
The locker of the eagle is 7. The locker of the cow is 8. The locker of the pig is 4. Frank picked the cow. Kate picked the one known for⟦ soaring⟧. Jack picked the pig.
How many legs does Kate's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 7. The locker of the pig is 6. The locker of the cow is 8. Frank picked the cow. Kate picked the one known for⟦ bacon⟧. Jack picked the pig.
How many legs does Kate's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '4' |  | 1 |
| no_jpp | '2' |  | 0 |
| no_jpp_rand | '2' |  | 0 |
| no_alf | '4' |  | 1 |
| no_alf_rand | '4' |  | 1 |
| no_pcf | '4' |  | 1 |
| no_pcf_rand | '4' |  | 1 |

Elimination read (A's cue -> 'cunning', the fox, not in the scene): lookup top '7' (A's locker (found by elimination)).

### C2-0618 (test half): O's pick eagle ('soaring') -> S's lion ('roaring'); routes {'identity': 6, 'position': 1, 'value': 9, 'original': 4}

**lookup**: O's answer 4, S's 9

O, as read:

```
<|im_start|>user
The locker of the eagle is 4. The locker of the lion is 6. The locker of the cow is 1. Eve picked the cow. Beth picked the one known for⟦ soaring⟧. Tara picked the lion.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 4. The locker of the cow is 1. The locker of the lion is 9. Eve picked the cow. Beth picked the one known for⟦ roaring⟧. Tara picked the lion.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '6' | identity | 0 |
| no_jpp | '6' | identity | 0 |
| no_jpp_rand | '6' | identity | 0 |
| no_alf | '6' | identity | 0 |
| no_alf_rand | '6' | identity | 0 |
| no_pcf | '6' | identity | 0 |
| no_pcf_rand | '6' | identity | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|im_start|>user
The locker of the eagle is 4. The locker of the lion is 6. The locker of the cow is 1. Eve picked the cow. Beth picked the one known for⟦ soaring⟧. Tara picked the lion.
How many legs does Beth's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 4. The locker of the cow is 1. The locker of the lion is 9. Eve picked the cow. Beth picked the one known for⟦ roaring⟧. Tara picked the lion.
How many legs does Beth's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '4' |  | 1 |
| no_jpp | '4' |  | 1 |
| no_jpp_rand | '4' |  | 1 |
| no_alf | '4' |  | 1 |
| no_alf_rand | '4' |  | 1 |
| no_pcf | '4' |  | 1 |
| no_pcf_rand | '4' |  | 1 |

Elimination read (A's cue -> 'bacon', the pig, not in the scene): lookup top '6' (B's locker).

### C2-0673 (test half): O's pick sheep ('wool') -> S's owl ('wisdom'); routes {'identity': 9, 'position': 2, 'value': 5, 'original': 3}

**lookup**: O's answer 3, S's 5

O, as read:

```
<|im_start|>user
The locker of the dog is 2. The locker of the sheep is 3. The locker of the owl is 9. Victor picked the owl. Maria picked the one known for⟦ wool⟧. Anna picked the dog.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the owl is 5. The locker of the sheep is 3. The locker of the dog is 2. Victor picked the owl. Maria picked the one known for⟦ wisdom⟧. Anna picked the dog.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '3' | original | 0 |
| whole | '3' | original | 0 |
| no_jpp | '3' | original | 0 |
| no_jpp_rand | '3' | original | 0 |
| no_alf | '3' | original | 0 |
| no_alf_rand | '3' | original | 0 |
| no_pcf | '3' | original | 0 |
| no_pcf_rand | '3' | original | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|im_start|>user
The locker of the dog is 2. The locker of the sheep is 3. The locker of the owl is 9. Victor picked the owl. Maria picked the one known for⟦ wool⟧. Anna picked the dog.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the owl is 5. The locker of the sheep is 3. The locker of the dog is 2. Victor picked the owl. Maria picked the one known for⟦ wisdom⟧. Anna picked the dog.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '2' |  | 1 |
| no_jpp | '2' |  | 1 |
| no_jpp_rand | '2' |  | 1 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '2' |  | 1 |
| no_pcf | '2' |  | 1 |
| no_pcf_rand | '2' |  | 1 |

Elimination read (A's cue -> 'webs', the spider, not in the scene): lookup top '8' (other).

### C2-0699 (fit half): O's pick spider ('webs') -> S's turkey ('Thanksgiving'); routes {'identity': 6, 'position': 4, 'value': 1, 'original': 2}

**lookup**: O's answer 2, S's 1

O, as read:

```
<|im_start|>user
The locker of the turkey is 6. The locker of the sheep is 4. The locker of the spider is 2. Ivy picked the turkey. Fiona picked the one known for⟦ webs⟧. Lucy picked the sheep.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the sheep is 4. The locker of the turkey is 1. The locker of the spider is 2. Ivy picked the turkey. Fiona picked the one known for⟦ Thanksgiving⟧. Lucy picked the sheep.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' | original | 0 |
| whole | '2' | original | 0 |
| no_jpp | '2' | original | 0 |
| no_jpp_rand | '2' | original | 0 |
| no_alf | '2' | original | 0 |
| no_alf_rand | '2' | original | 0 |
| no_pcf | '2' | original | 0 |
| no_pcf_rand | '2' | original | 0 |

**recall**: O's answer 8, S's 2

O, as read:

```
<|im_start|>user
The locker of the turkey is 6. The locker of the sheep is 4. The locker of the spider is 2. Ivy picked the turkey. Fiona picked the one known for⟦ webs⟧. Lucy picked the sheep.
How many legs does Fiona's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the sheep is 4. The locker of the turkey is 1. The locker of the spider is 2. Ivy picked the turkey. Fiona picked the one known for⟦ Thanksgiving⟧. Lucy picked the sheep.
How many legs does Fiona's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '8' |  | 0 |
| whole | '8' |  | 0 |
| no_jpp | '8' |  | 0 |
| no_jpp_rand | '8' |  | 0 |
| no_alf | '8' |  | 0 |
| no_alf_rand | '8' |  | 0 |
| no_pcf | '8' |  | 0 |
| no_pcf_rand | '8' |  | 0 |

Elimination read (A's cue -> 'loyalty', the dog, not in the scene): lookup top '6' (B's locker).

### C2-0734 (test half): O's pick horse ('racing') -> S's eagle ('soaring'); routes {'identity': 3, 'position': 9, 'value': 1, 'original': 4}

**lookup**: O's answer 4, S's 1

O, as read:

```
<|im_start|>user
The locker of the sheep is 9. The locker of the eagle is 3. The locker of the horse is 4. Will picked the eagle. Oscar picked the one known for⟦ racing⟧. Sam picked the sheep.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 1. The locker of the sheep is 9. The locker of the horse is 4. Will picked the eagle. Oscar picked the one known for⟦ soaring⟧. Sam picked the sheep.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '3' | identity | 0 |
| no_jpp | '3' | identity | 0 |
| no_jpp_rand | '3' | identity | 0 |
| no_alf | '3' | identity | 0 |
| no_alf_rand | '3' | identity | 0 |
| no_pcf | '3' | identity | 0 |
| no_pcf_rand | '3' | identity | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|im_start|>user
The locker of the sheep is 9. The locker of the eagle is 3. The locker of the horse is 4. Will picked the eagle. Oscar picked the one known for⟦ racing⟧. Sam picked the sheep.
How many legs does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 1. The locker of the sheep is 9. The locker of the horse is 4. Will picked the eagle. Oscar picked the one known for⟦ soaring⟧. Sam picked the sheep.
How many legs does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '2' |  | 1 |
| no_jpp | '2' |  | 1 |
| no_jpp_rand | '2' |  | 1 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '2' |  | 1 |
| no_pcf | '2' |  | 1 |
| no_pcf_rand | '2' |  | 1 |

Elimination read (A's cue -> 'packs', the wolf, not in the scene): lookup top '3' (B's locker).

### C2-0820 (fit half): O's pick pig ('bacon') -> S's turkey ('Thanksgiving'); routes {'identity': 6, 'position': 8, 'value': 5, 'original': 2}

**lookup**: O's answer 2, S's 5

O, as read:

```
<|im_start|>user
The locker of the turkey is 6. The locker of the pig is 2. The locker of the eagle is 8. Sam picked the turkey. Dan picked the one known for⟦ bacon⟧. Ben picked the eagle.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 8. The locker of the pig is 2. The locker of the turkey is 5. Sam picked the turkey. Dan picked the one known for⟦ Thanksgiving⟧. Ben picked the eagle.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' | original | 0 |
| whole | '2' | original | 0 |
| no_jpp | '2' | original | 0 |
| no_jpp_rand | '2' | original | 0 |
| no_alf | '2' | original | 0 |
| no_alf_rand | '2' | original | 0 |
| no_pcf | '2' | original | 0 |
| no_pcf_rand | '2' | original | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|im_start|>user
The locker of the turkey is 6. The locker of the pig is 2. The locker of the eagle is 8. Sam picked the turkey. Dan picked the one known for⟦ bacon⟧. Ben picked the eagle.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 8. The locker of the pig is 2. The locker of the turkey is 5. Sam picked the turkey. Dan picked the one known for⟦ Thanksgiving⟧. Ben picked the eagle.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'milk', the cow, not in the scene): lookup top '2' (A's locker (found by elimination)).

### C2-0835 (test half): O's pick turkey ('Thanksgiving') -> S's elephant ('ivory'); routes {'identity': 1, 'position': 7, 'value': 3, 'original': 6}

**lookup**: O's answer 6, S's 3

O, as read:

```
<|im_start|>user
The locker of the elephant is 1. The locker of the turkey is 6. The locker of the sheep is 7. Lucy picked the elephant. Emma picked the sheep. Rose picked the one known for⟦ Thanksgiving⟧.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the sheep is 7. The locker of the turkey is 6. The locker of the elephant is 3. Lucy picked the elephant. Emma picked the sheep. Rose picked the one known for⟦ ivory⟧.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '6' | original | 0 |
| whole | '1' | identity | 0 |
| no_jpp | '7' | position | 0 |
| no_jpp_rand | '6' | original | 0 |
| no_alf | '1' | identity | 0 |
| no_alf_rand | '1' | identity | 0 |
| no_pcf | '1' | identity | 0 |
| no_pcf_rand | '1' | identity | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|im_start|>user
The locker of the elephant is 1. The locker of the turkey is 6. The locker of the sheep is 7. Lucy picked the elephant. Emma picked the sheep. Rose picked the one known for⟦ Thanksgiving⟧.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the sheep is 7. The locker of the turkey is 6. The locker of the elephant is 3. Lucy picked the elephant. Emma picked the sheep. Rose picked the one known for⟦ ivory⟧.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '4' |  | 1 |
| no_jpp | '4' |  | 1 |
| no_jpp_rand | '4' |  | 1 |
| no_alf | '4' |  | 1 |
| no_alf_rand | '4' |  | 1 |
| no_pcf | '4' |  | 1 |
| no_pcf_rand | '4' |  | 1 |

Elimination read (A's cue -> 'soaring', the eagle, not in the scene): lookup top '6' (A's locker (found by elimination)).

### C2-0867 (fit half): O's pick chicken ('eggs') -> S's dog ('loyalty'); routes {'identity': 3, 'position': 6, 'value': 8, 'original': 9}

**lookup**: O's answer 9, S's 8

O, as read:

```
<|im_start|>user
The locker of the chicken is 9. The locker of the elephant is 6. The locker of the dog is 3. Ruby picked the dog. James picked the one known for⟦ eggs⟧. Vera picked the elephant.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the chicken is 9. The locker of the dog is 8. The locker of the elephant is 6. Ruby picked the dog. James picked the one known for⟦ loyalty⟧. Vera picked the elephant.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '9' | original | 0 |
| whole | '6' | position | 0 |
| no_jpp | '6' | position | 0 |
| no_jpp_rand | '6' | position | 0 |
| no_alf | '6' | position | 0 |
| no_alf_rand | '6' | position | 0 |
| no_pcf | '6' | position | 0 |
| no_pcf_rand | '6' | position | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|im_start|>user
The locker of the chicken is 9. The locker of the elephant is 6. The locker of the dog is 3. Ruby picked the dog. James picked the one known for⟦ eggs⟧. Vera picked the elephant.
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (the source):

```
<|im_start|>user
The locker of the chicken is 9. The locker of the dog is 8. The locker of the elephant is 6. Ruby picked the dog. James picked the one known for⟦ loyalty⟧. Vera picked the elephant.
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 1 |
| whole | '4' |  | 1 |
| no_jpp | '4' |  | 1 |
| no_jpp_rand | '4' |  | 1 |
| no_alf | '4' |  | 1 |
| no_alf_rand | '4' |  | 1 |
| no_pcf | '4' |  | 1 |
| no_pcf_rand | '4' |  | 1 |

Elimination read (A's cue -> 'Thanksgiving', the turkey, not in the scene): lookup top '6' (C's locker).

## muse30_x47_cue (muse-glimmer-30b, L26): 10 random scenes of 300 (random.Random(0) over the sorted scenes)

### C2-0052 (test half): O's pick chicken ('eggs') -> S's cow ('milk'); routes {'identity': 2, 'position': 5, 'value': 7, 'original': 9}

**lookup**: O's answer 9, S's 7

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 9. The locker of the cow is 2. The locker of the tick is 5. Grace picked the cow. Zoe picked the tick. Frank picked the one known for⟦ eggs⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 9. The locker of the tick is 5. The locker of the cow is 7. Grace picked the cow. Zoe picked the tick. Frank picked the one known for⟦ milk⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '9' | original | 0 |
| whole | '2' | identity | 0 |
| no_jpp | '2' | identity | 0 |
| no_jpp_rand | '9' | original | 0 |
| no_alf | '9' | original | 0 |
| no_alf_rand | '2' | identity | 0 |
| no_pcf | '9' | original | 0 |
| no_pcf_rand | '9' | original | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 9. The locker of the cow is 2. The locker of the tick is 5. Grace picked the cow. Zoe picked the tick. Frank picked the one known for⟦ eggs⟧.
How many legs does Frank's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 9. The locker of the tick is 5. The locker of the cow is 7. Grace picked the cow. Zoe picked the tick. Frank picked the one known for⟦ milk⟧.
How many legs does Frank's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '2' |  | 0 |
| no_jpp | '2' |  | 0 |
| no_jpp_rand | '2' |  | 0 |
| no_alf | '2' |  | 0 |
| no_alf_rand | '2' |  | 0 |
| no_pcf | '2' |  | 0 |
| no_pcf_rand | '2' |  | 0 |

Elimination read (A's cue -> 'wool', the sheep, not in the scene): lookup top '9' (A's locker (found by elimination)).

### C2-0400 (test half): O's pick turkey ('Thanksgiving') -> S's sheep ('wool'); routes {'identity': 7, 'position': 3, 'value': 6, 'original': 8}

**lookup**: O's answer 8, S's 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 3. The locker of the sheep is 7. The locker of the turkey is 8. James picked the one known for⟦ Thanksgiving⟧. Max picked the sheep. Eve picked the wolf.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the sheep is 6. The locker of the wolf is 3. The locker of the turkey is 8. James picked the one known for⟦ wool⟧. Max picked the sheep. Eve picked the wolf.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '8' | original | 0 |
| whole | '8' | original | 0 |
| no_jpp | '8' | original | 0 |
| no_jpp_rand | '8' | original | 0 |
| no_alf | '8' | original | 0 |
| no_alf_rand | '8' | original | 0 |
| no_pcf | '8' | original | 0 |
| no_pcf_rand | '8' | original | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 3. The locker of the sheep is 7. The locker of the turkey is 8. James picked the one known for⟦ Thanksgiving⟧. Max picked the sheep. Eve picked the wolf.
How many legs does James's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the sheep is 6. The locker of the wolf is 3. The locker of the turkey is 8. James picked the one known for⟦ wool⟧. Max picked the sheep. Eve picked the wolf.
How many legs does James's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '2' |  | 0 |
| no_jpp | '2' |  | 0 |
| no_jpp_rand | '2' |  | 0 |
| no_alf | '2' |  | 0 |
| no_alf_rand | '2' |  | 0 |
| no_pcf | '2' |  | 0 |
| no_pcf_rand | '2' |  | 0 |

Elimination read (A's cue -> 'stripes', the zebra, not in the scene): lookup top '8' (A's locker (found by elimination)).

### C2-0466 (test half): O's pick elephant ('memory') -> S's chicken ('eggs'); routes {'identity': 6, 'position': 3, 'value': 9, 'original': 7}

**lookup**: O's answer 7, S's 9

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 3. The locker of the elephant is 7. The locker of the chicken is 6. Max picked the turkey. Laura picked the chicken. Sara picked the one known for⟦ memory⟧.
Which locker belongs to Sara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 9. The locker of the elephant is 7. The locker of the turkey is 3. Max picked the turkey. Laura picked the chicken. Sara picked the one known for⟦ eggs⟧.
Which locker belongs to Sara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '7' | original | 0 |
| no_jpp | '7' | original | 0 |
| no_jpp_rand | '7' | original | 0 |
| no_alf | '7' | original | 0 |
| no_alf_rand | '7' | original | 0 |
| no_pcf | '7' | original | 0 |
| no_pcf_rand | '7' | original | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 3. The locker of the elephant is 7. The locker of the chicken is 6. Max picked the turkey. Laura picked the chicken. Sara picked the one known for⟦ memory⟧.
How many legs does Sara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 9. The locker of the elephant is 7. The locker of the turkey is 3. Max picked the turkey. Laura picked the chicken. Sara picked the one known for⟦ eggs⟧.
How many legs does Sara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'Lyme', the tick, not in the scene): lookup top '7' (A's locker (found by elimination)).

### C2-0543 (fit half): O's pick cow ('milk') -> S's turkey ('Thanksgiving'); routes {'identity': 5, 'position': 9, 'value': 2, 'original': 4}

**lookup**: O's answer 4, S's 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 9. The locker of the turkey is 5. The locker of the cow is 4. Lucy picked the turkey. Clara picked the one known for⟦ milk⟧. Ryan picked the wolf.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 2. The locker of the wolf is 9. The locker of the cow is 4. Lucy picked the turkey. Clara picked the one known for⟦ Thanksgiving⟧. Ryan picked the wolf.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '4' | original | 0 |
| no_jpp | '4' | original | 0 |
| no_jpp_rand | '4' | original | 0 |
| no_alf | '4' | original | 0 |
| no_alf_rand | '4' | original | 0 |
| no_pcf | '4' | original | 0 |
| no_pcf_rand | '4' | original | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 9. The locker of the turkey is 5. The locker of the cow is 4. Lucy picked the turkey. Clara picked the one known for⟦ milk⟧. Ryan picked the wolf.
How many legs does Clara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 2. The locker of the wolf is 9. The locker of the cow is 4. Lucy picked the turkey. Clara picked the one known for⟦ Thanksgiving⟧. Ryan picked the wolf.
How many legs does Clara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'stripes', the zebra, not in the scene): lookup top '9' (C's locker).

### C2-0596 (test half): O's pick elephant ('memory') -> S's chicken ('eggs'); routes {'identity': 3, 'position': 5, 'value': 2, 'original': 8}

**lookup**: O's answer 8, S's 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 5. The locker of the elephant is 8. The locker of the chicken is 3. Julia picked the chicken. Henry picked the turkey. Ivy picked the one known for⟦ memory⟧.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 2. The locker of the elephant is 8. The locker of the turkey is 5. Julia picked the chicken. Henry picked the turkey. Ivy picked the one known for⟦ eggs⟧.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '8' | original | 0 |
| whole | '8' | original | 0 |
| no_jpp | '8' | original | 0 |
| no_jpp_rand | '8' | original | 0 |
| no_alf | '8' | original | 0 |
| no_alf_rand | '8' | original | 0 |
| no_pcf | '8' | original | 0 |
| no_pcf_rand | '8' | original | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 5. The locker of the elephant is 8. The locker of the chicken is 3. Julia picked the chicken. Henry picked the turkey. Ivy picked the one known for⟦ memory⟧.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 2. The locker of the elephant is 8. The locker of the turkey is 5. Julia picked the chicken. Henry picked the turkey. Ivy picked the one known for⟦ eggs⟧.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '2' |  | 1 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'milk', the cow, not in the scene): lookup top '8' (A's locker (found by elimination)).

### C2-0631 (fit half): O's pick chicken ('eggs') -> S's wolf ('packs'); routes {'identity': 5, 'position': 9, 'value': 4, 'original': 7}

**lookup**: O's answer 7, S's 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the elephant is 9. The locker of the wolf is 5. The locker of the chicken is 7. Kate picked the wolf. Clara picked the elephant. Laura picked the one known for⟦ eggs⟧.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 4. The locker of the elephant is 9. The locker of the chicken is 7. Kate picked the wolf. Clara picked the elephant. Laura picked the one known for⟦ packs⟧.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '9' | position | 0 |
| no_jpp | '9' | position | 0 |
| no_jpp_rand | '9' | position | 0 |
| no_alf | '9' | position | 0 |
| no_alf_rand | '9' | position | 0 |
| no_pcf | '9' | position | 0 |
| no_pcf_rand | '9' | position | 0 |

**recall**: O's answer 2, S's 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the elephant is 9. The locker of the wolf is 5. The locker of the chicken is 7. Kate picked the wolf. Clara picked the elephant. Laura picked the one known for⟦ eggs⟧.
How many legs does Laura's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 4. The locker of the elephant is 9. The locker of the chicken is 7. Kate picked the wolf. Clara picked the elephant. Laura picked the one known for⟦ packs⟧.
How many legs does Laura's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '2' |  | 0 |
| no_jpp | '2' |  | 0 |
| no_jpp_rand | '2' |  | 0 |
| no_alf | '2' |  | 0 |
| no_alf_rand | '2' |  | 0 |
| no_pcf | '2' |  | 0 |
| no_pcf_rand | '2' |  | 0 |

Elimination read (A's cue -> 'Lyme', the tick, not in the scene): lookup top '7' (A's locker (found by elimination)).

### C2-0666 (test half): O's pick spider ('webs') -> S's turkey ('Thanksgiving'); routes {'identity': 5, 'position': 8, 'value': 6, 'original': 3}

**lookup**: O's answer 3, S's 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the zebra is 8. The locker of the turkey is 5. The locker of the spider is 3. Nina picked the turkey. Lily picked the one known for⟦ webs⟧. Liam picked the zebra.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 6. The locker of the zebra is 8. The locker of the spider is 3. Nina picked the turkey. Lily picked the one known for⟦ Thanksgiving⟧. Liam picked the zebra.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '3' | original | 0 |
| whole | '3' | original | 0 |
| no_jpp | '3' | original | 0 |
| no_jpp_rand | '3' | original | 0 |
| no_alf | '3' | original | 0 |
| no_alf_rand | '3' | original | 0 |
| no_pcf | '3' | original | 0 |
| no_pcf_rand | '3' | original | 0 |

**recall**: O's answer 8, S's 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the zebra is 8. The locker of the turkey is 5. The locker of the spider is 3. Nina picked the turkey. Lily picked the one known for⟦ webs⟧. Liam picked the zebra.
How many legs does Lily's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 6. The locker of the zebra is 8. The locker of the spider is 3. Nina picked the turkey. Lily picked the one known for⟦ Thanksgiving⟧. Liam picked the zebra.
How many legs does Lily's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '8' |  | 0 |
| whole | '8' |  | 0 |
| no_jpp | '8' |  | 0 |
| no_jpp_rand | '8' |  | 0 |
| no_alf | '8' |  | 0 |
| no_alf_rand | '8' |  | 0 |
| no_pcf | '8' |  | 0 |
| no_pcf_rand | '8' |  | 0 |

Elimination read (A's cue -> 'packs', the wolf, not in the scene): lookup top '8' (C's locker).

### C2-0765 (test half): O's pick spider ('webs') -> S's cow ('milk'); routes {'identity': 7, 'position': 9, 'value': 8, 'original': 3}

**lookup**: O's answer 3, S's 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 3. The locker of the cow is 7. The locker of the wolf is 9. Oscar picked the wolf. Anna picked the one known for⟦ webs⟧. Tara picked the cow.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 3. The locker of the wolf is 9. The locker of the cow is 8. Oscar picked the wolf. Anna picked the one known for⟦ milk⟧. Tara picked the cow.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '3' | original | 0 |
| whole | '3' | original | 0 |
| no_jpp | '3' | original | 0 |
| no_jpp_rand | '3' | original | 0 |
| no_alf | '3' | original | 0 |
| no_alf_rand | '3' | original | 0 |
| no_pcf | '3' | original | 0 |
| no_pcf_rand | '3' | original | 0 |

**recall**: O's answer 8, S's 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 3. The locker of the cow is 7. The locker of the wolf is 9. Oscar picked the wolf. Anna picked the one known for⟦ webs⟧. Tara picked the cow.
How many legs does Anna's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 3. The locker of the wolf is 9. The locker of the cow is 8. Oscar picked the wolf. Anna picked the one known for⟦ milk⟧. Tara picked the cow.
How many legs does Anna's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '8' |  | 0 |
| whole | '8' |  | 0 |
| no_jpp | '8' |  | 0 |
| no_jpp_rand | '8' |  | 0 |
| no_alf | '8' |  | 0 |
| no_alf_rand | '8' |  | 0 |
| no_pcf | '8' |  | 0 |
| no_pcf_rand | '8' |  | 0 |

Elimination read (A's cue -> 'Lyme', the tick, not in the scene): lookup top '3' (A's locker (found by elimination)).

### C2-0788 (fit half): O's pick elephant ('memory') -> S's spider ('webs'); routes {'identity': 9, 'position': 3, 'value': 8, 'original': 5}

**lookup**: O's answer 5, S's 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 9. The locker of the zebra is 3. The locker of the elephant is 5. Mark picked the spider. Lily picked the zebra. Sara picked the one known for⟦ memory⟧.
Which locker belongs to Sara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the zebra is 3. The locker of the spider is 8. The locker of the elephant is 5. Mark picked the spider. Lily picked the zebra. Sara picked the one known for⟦ webs⟧.
Which locker belongs to Sara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '5' | original | 0 |
| whole | '5' | original | 0 |
| no_jpp | '5' | original | 0 |
| no_jpp_rand | '5' | original | 0 |
| no_alf | '5' | original | 0 |
| no_alf_rand | '5' | original | 0 |
| no_pcf | '5' | original | 0 |
| no_pcf_rand | '5' | original | 0 |

**recall**: O's answer 4, S's 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 9. The locker of the zebra is 3. The locker of the elephant is 5. Mark picked the spider. Lily picked the zebra. Sara picked the one known for⟦ memory⟧.
How many legs does Sara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the zebra is 3. The locker of the spider is 8. The locker of the elephant is 5. Mark picked the spider. Lily picked the zebra. Sara picked the one known for⟦ webs⟧.
How many legs does Sara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'Thanksgiving', the turkey, not in the scene): lookup top '5' (A's locker (found by elimination)).

### C2-0830 (fit half): O's pick wolf ('packs') -> S's chicken ('eggs'); routes {'identity': 9, 'position': 2, 'value': 5, 'original': 6}

**lookup**: O's answer 6, S's 5

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 6. The locker of the spider is 2. The locker of the chicken is 9. Eric picked the one known for⟦ packs⟧. Hugo picked the chicken. Frank picked the spider.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 6. The locker of the chicken is 5. The locker of the spider is 2. Eric picked the one known for⟦ eggs⟧. Hugo picked the chicken. Frank picked the spider.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '6' | original | 0 |
| whole | '2' | position | 0 |
| no_jpp | '2' | position | 0 |
| no_jpp_rand | '2' | position | 0 |
| no_alf | '2' | position | 0 |
| no_alf_rand | '2' | position | 0 |
| no_pcf | '2' | position | 0 |
| no_pcf_rand | '2' | position | 0 |

**recall**: O's answer 4, S's 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 6. The locker of the spider is 2. The locker of the chicken is 9. Eric picked the one known for⟦ packs⟧. Hugo picked the chicken. Frank picked the spider.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the wolf is 6. The locker of the chicken is 5. The locker of the spider is 2. Eric picked the one known for⟦ eggs⟧. Hugo picked the chicken. Frank picked the spider.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | route | switched (S's answer) |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| no_jpp | '4' |  | 0 |
| no_jpp_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |
| no_pcf | '4' |  | 0 |
| no_pcf_rand | '4' |  | 0 |

Elimination read (A's cue -> 'stripes', the zebra, not in the scene): lookup top '6' (A's locker (found by elimination)).

