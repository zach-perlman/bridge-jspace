# x51_answer plan: 47.3's described bridge (the cue token, locker scenes) on qwen3.6-27b (tokenizer and stored runs only; UNVERIFIED)

Source x47_cue_27b, L32, gate {'pass': True, 'chosen': 300, 'org_read_accuracy': {'PP': 1.0, 'PM': 0.9985714285714286}, 'gate': 0.8}; items 300 (15 bridge entities); reads 4800; |A| tokens per item {'n': 300, 'min': 4, 'median': 5.0, 'max': 6, 'mean': 5.163, 'hist': {4: 49, 5: 153, 6: 98}}; letter atoms per item {'n': 300, 'min': 0, 'median': 0.0, 'max': 0, 'mean': 0.0, 'hist': {0: 300}}.

Answer tokens (most common): '4' x289, '2' x265, '8' x174, '1' x157, '7' x153, '5' x146, '6' x129, '3' x122, '9' x114

## C2-0037: spider -> eagle; A = ['2', '4', '6', '7', '8', '9']

lookup_org:

```
<|im_start|>user
The locker of the spider is 4. The locker of the eagle is 9. The locker of the fox is 6. Grace picked the one known for⟦ webs⟧. Kate picked the fox. Max picked the eagle.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the spider is 4. The locker of the fox is 6. The locker of the eagle is 7. Grace picked the one known for⟦ soaring⟧. Kate picked the fox. Max picked the eagle.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the spider is 4. The locker of the eagle is 9. The locker of the fox is 6. Grace picked the one known for⟦ webs⟧. Kate picked the fox. Max picked the eagle.
How many legs does Grace's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the spider is 4. The locker of the fox is 6. The locker of the eagle is 7. Grace picked the one known for⟦ soaring⟧. Kate picked the fox. Max picked the eagle.
How many legs does Grace's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## C2-0254: cat -> turkey; A = ['2', '3', '4', '6', '8']

lookup_org:

```
<|im_start|>user
The locker of the turkey is 8. The locker of the cow is 6. The locker of the cat is 2. Ivan picked the one known for⟦ curiosity⟧. Kyle picked the cow. Oscar picked the turkey.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the cow is 6. The locker of the turkey is 3. The locker of the cat is 2. Ivan picked the one known for⟦ Thanksgiving⟧. Kyle picked the cow. Oscar picked the turkey.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the turkey is 8. The locker of the cow is 6. The locker of the cat is 2. Ivan picked the one known for⟦ curiosity⟧. Kyle picked the cow. Oscar picked the turkey.
How many legs does Ivan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the cow is 6. The locker of the turkey is 3. The locker of the cat is 2. Ivan picked the one known for⟦ Thanksgiving⟧. Kyle picked the cow. Oscar picked the turkey.
How many legs does Ivan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## C2-0399: spider -> cat; A = ['1', '4', '5', '7', '8']

lookup_org:

```
<|im_start|>user
The locker of the spider is 4. The locker of the cat is 7. The locker of the horse is 5. Hugo picked the one known for⟦ webs⟧. Eve picked the horse. Clara picked the cat.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the spider is 4. The locker of the horse is 5. The locker of the cat is 1. Hugo picked the one known for⟦ curiosity⟧. Eve picked the horse. Clara picked the cat.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the spider is 4. The locker of the cat is 7. The locker of the horse is 5. Hugo picked the one known for⟦ webs⟧. Eve picked the horse. Clara picked the cat.
How many legs does Hugo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the spider is 4. The locker of the horse is 5. The locker of the cat is 1. Hugo picked the one known for⟦ curiosity⟧. Eve picked the horse. Clara picked the cat.
How many legs does Hugo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## C2-0442: horse -> eagle; A = ['2', '3', '4', '6', '7', '8']

lookup_org:

```
<|im_start|>user
The locker of the horse is 7. The locker of the eagle is 6. The locker of the lion is 8. Hugo picked the lion. Ruby picked the eagle. Eric picked the one known for⟦ racing⟧.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the horse is 7. The locker of the lion is 8. The locker of the eagle is 3. Hugo picked the lion. Ruby picked the eagle. Eric picked the one known for⟦ soaring⟧.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the horse is 7. The locker of the eagle is 6. The locker of the lion is 8. Hugo picked the lion. Ruby picked the eagle. Eric picked the one known for⟦ racing⟧.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the horse is 7. The locker of the lion is 8. The locker of the eagle is 3. Hugo picked the lion. Ruby picked the eagle. Eric picked the one known for⟦ soaring⟧.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## C2-0538: owl -> wolf; A = ['1', '2', '4', '5', '7']

lookup_org:

```
<|im_start|>user
The locker of the horse is 1. The locker of the wolf is 5. The locker of the owl is 7. Max picked the one known for⟦ wisdom⟧. Eve picked the wolf. Zoe picked the horse.
Which locker belongs to Max's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the wolf is 4. The locker of the horse is 1. The locker of the owl is 7. Max picked the one known for⟦ packs⟧. Eve picked the wolf. Zoe picked the horse.
Which locker belongs to Max's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the horse is 1. The locker of the wolf is 5. The locker of the owl is 7. Max picked the one known for⟦ wisdom⟧. Eve picked the wolf. Zoe picked the horse.
How many legs does Max's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the wolf is 4. The locker of the horse is 1. The locker of the owl is 7. Max picked the one known for⟦ packs⟧. Eve picked the wolf. Zoe picked the horse.
How many legs does Max's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

