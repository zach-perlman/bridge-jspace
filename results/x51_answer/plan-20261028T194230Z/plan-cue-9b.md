# x51_answer plan (r2, amendment 20:20): 47.3's described bridge (the cue token, locker scenes) on qwen3.5-9b (tokenizer and stored runs only; UNVERIFIED)

Source qwen35_9b_x47_cue, L12, gate {'pass': True, 'chosen': 300, 'org_read_accuracy': {'PP': 0.9471428571428572, 'PM': 0.8742857142857143}, 'gate': 0.8}; items 300 (15 bridge entities); arms ['whole', 'no_jpp', 'no_jpp_rand', 'no_jpp_A', 'no_jpp_A_rand', 'no_A', 'no_A_rand']; reads 4800; A = number words, one-token letter variants; |A| tokens per item {'n': 300, 'min': 16, 'median': 20.0, 'max': 24, 'mean': 20.667, 'hist': {16: 37, 20: 176, 24: 87}}; answer words per item {'n': 300, 'min': 4, 'median': 5.0, 'max': 6, 'mean': 5.167, 'hist': {4: 37, 5: 176, 6: 87}}; items whose own answer word has no letter token: 0; Δ's 25 OMP atoms in A: not computable on CPU: needs Δ at L (GPU forwards) and no stored x0_atoms run fits these items; reported by the run (norms.jsonl n_answer_atoms_in_25).

Answer tokens (most common): ' four' x279, ' Four' x279, 'Four' x279, 'four' x279, ' two' x271, ' Two' x271, 'Two' x271, 'two' x271, ' eight' x189, ' Eight' x189, 'Eight' x189, 'eight' x189, ' seven' x158, ' Seven' x158, 'Seven' x158, 'seven' x158, ' nine' x146, ' Nine' x146, 'Nine' x146, 'nine' x146, ' six' x136, ' Six' x136, 'Six' x136, 'six' x136, 'one' x131, ' one' x131, ' One' x131, 'One' x131, ' five' x121, ' Five' x121

Split answer words (A keeps their first token): {}

Number-word variants as tokens: eight: {'eight': ['eight'], ' eight': [' eight'], 'Eight': ['Eight'], ' Eight': [' Eight']}; five: {'five': ['five'], ' five': [' five'], 'Five': ['Five'], ' Five': [' Five']}; four: {'four': ['four'], ' four': [' four'], 'Four': ['Four'], ' Four': [' Four']}; nine: {'nine': ['nine'], ' nine': [' nine'], 'Nine': ['Nine'], ' Nine': [' Nine']}; one: {'one': ['one'], ' one': [' one'], 'One': ['One'], ' One': [' One']}; seven: {'seven': ['seven'], ' seven': [' seven'], 'Seven': ['Seven'], ' Seven': [' Seven']}; six: {'six': ['six'], ' six': [' six'], 'Six': ['Six'], ' Six': [' Six']}; three: {'three': ['three'], ' three': [' three'], 'Three': ['Three'], ' Three': [' Three']}; two: {'two': ['two'], ' two': [' two'], 'Two': ['Two'], ' Two': [' Two']}

## C2-0069: turkey -> cow; A = [' two', ' four', ' five', ' seven', ' Two', 'Two', ' nine', ' Four', 'two', ' Five', 'Four', ' Seven', 'four', 'Five', ' Nine', 'five', 'Seven', 'seven', 'Nine', 'nine']

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

## C2-0452: cow -> chicken; A = [' two', ' three', ' four', ' eight', ' seven', ' Two', 'Two', ' Four', ' Three', 'Three', 'two', 'Four', 'three', ' Seven', 'four', ' Eight', 'Eight', 'Seven', 'eight', 'seven']

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

## C2-0673: sheep -> owl; A = [' two', ' three', ' four', ' five', ' Two', 'Two', ' nine', ' Four', ' Three', 'Three', 'two', ' Five', 'Four', 'three', 'four', 'Five', ' Nine', 'five', 'Nine', 'nine']

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

## C2-0734: horse -> eagle; A = ['one', ' one', ' two', ' three', ' four', ' One', 'One', ' Two', 'Two', ' nine', ' Four', ' Three', 'Three', 'two', 'Four', 'three', 'four', ' Nine', 'Nine', 'nine']

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

## C2-0867: chicken -> dog; A = [' two', ' three', ' four', ' six', ' eight', ' Two', 'Two', ' nine', ' Four', ' Three', ' Six', 'Three', 'two', 'Four', 'three', 'four', ' Eight', ' Nine', 'Six', 'six', 'Eight', 'eight', 'Nine', 'nine']

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

