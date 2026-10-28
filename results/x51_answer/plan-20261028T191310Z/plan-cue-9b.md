# x51_answer plan: 47.3's described bridge (the cue token, locker scenes) on qwen3.5-9b (tokenizer and stored runs only; UNVERIFIED)

Source qwen35_9b_x47_cue, L12, gate {'pass': True, 'chosen': 300, 'org_read_accuracy': {'PP': 0.9471428571428572, 'PM': 0.8742857142857143}, 'gate': 0.8}; items 300 (15 bridge entities); reads 4800; |A| tokens per item {'n': 300, 'min': 4, 'median': 5.0, 'max': 6, 'mean': 5.167, 'hist': {4: 37, 5: 176, 6: 87}}; letter atoms per item {'n': 300, 'min': 0, 'median': 0.0, 'max': 0, 'mean': 0.0, 'hist': {0: 300}}.

Answer tokens (most common): '4' x279, '2' x271, '8' x189, '7' x158, '9' x146, '6' x136, '1' x131, '5' x121, '3' x119

## C2-0069: turkey -> cow; A = ['2', '4', '5', '7', '9']

lookup_org:

```
<|im_start|>user
The locker of the turkey is 9. The locker of the cow is 2. The locker of the sheep is 5. Grace picked the cow. Zoe picked the sheep. Frank picked the one known for⟦ Thanksgiving⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the turkey is 9. The locker of the sheep is 5. The locker of the cow is 7. Grace picked the cow. Zoe picked the sheep. Frank picked the one known for⟦ milk⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the turkey is 9. The locker of the cow is 2. The locker of the sheep is 5. Grace picked the cow. Zoe picked the sheep. Frank picked the one known for⟦ Thanksgiving⟧.
How many legs does Frank's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the turkey is 9. The locker of the sheep is 5. The locker of the cow is 7. Grace picked the cow. Zoe picked the sheep. Frank picked the one known for⟦ milk⟧.
How many legs does Frank's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## C2-0452: cow -> chicken; A = ['2', '3', '4', '7', '8']

lookup_org:

```
<|im_start|>user
The locker of the dog is 8. The locker of the cow is 3. The locker of the chicken is 7. Ella picked the one known for⟦ milk⟧. Liam picked the dog. Jack picked the chicken.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the chicken is 2. The locker of the cow is 3. The locker of the dog is 8. Ella picked the one known for⟦ eggs⟧. Liam picked the dog. Jack picked the chicken.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the dog is 8. The locker of the cow is 3. The locker of the chicken is 7. Ella picked the one known for⟦ milk⟧. Liam picked the dog. Jack picked the chicken.
How many legs does Ella's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the chicken is 2. The locker of the cow is 3. The locker of the dog is 8. Ella picked the one known for⟦ eggs⟧. Liam picked the dog. Jack picked the chicken.
How many legs does Ella's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## C2-0673: sheep -> owl; A = ['2', '3', '4', '5', '9']

lookup_org:

```
<|im_start|>user
The locker of the dog is 2. The locker of the sheep is 3. The locker of the owl is 9. Victor picked the owl. Maria picked the one known for⟦ wool⟧. Anna picked the dog.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the owl is 5. The locker of the sheep is 3. The locker of the dog is 2. Victor picked the owl. Maria picked the one known for⟦ wisdom⟧. Anna picked the dog.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the dog is 2. The locker of the sheep is 3. The locker of the owl is 9. Victor picked the owl. Maria picked the one known for⟦ wool⟧. Anna picked the dog.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the owl is 5. The locker of the sheep is 3. The locker of the dog is 2. Victor picked the owl. Maria picked the one known for⟦ wisdom⟧. Anna picked the dog.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## C2-0734: horse -> eagle; A = ['1', '2', '3', '4', '9']

lookup_org:

```
<|im_start|>user
The locker of the sheep is 9. The locker of the eagle is 3. The locker of the horse is 4. Will picked the eagle. Oscar picked the one known for⟦ racing⟧. Sam picked the sheep.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the eagle is 1. The locker of the sheep is 9. The locker of the horse is 4. Will picked the eagle. Oscar picked the one known for⟦ soaring⟧. Sam picked the sheep.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the sheep is 9. The locker of the eagle is 3. The locker of the horse is 4. Will picked the eagle. Oscar picked the one known for⟦ racing⟧. Sam picked the sheep.
How many legs does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the eagle is 1. The locker of the sheep is 9. The locker of the horse is 4. Will picked the eagle. Oscar picked the one known for⟦ soaring⟧. Sam picked the sheep.
How many legs does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## C2-0867: chicken -> dog; A = ['2', '3', '4', '6', '8', '9']

lookup_org:

```
<|im_start|>user
The locker of the chicken is 9. The locker of the elephant is 6. The locker of the dog is 3. Ruby picked the dog. James picked the one known for⟦ eggs⟧. Vera picked the elephant.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the chicken is 9. The locker of the dog is 8. The locker of the elephant is 6. Ruby picked the dog. James picked the one known for⟦ loyalty⟧. Vera picked the elephant.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the chicken is 9. The locker of the elephant is 6. The locker of the dog is 3. Ruby picked the dog. James picked the one known for⟦ eggs⟧. Vera picked the elephant.
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the chicken is 9. The locker of the dog is 8. The locker of the elephant is 6. Ruby picked the dog. James picked the one known for⟦ loyalty⟧. Vera picked the elephant.
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

