# x51_answer plan (r2, amendment 20:20): 47.3's described bridge (the cue token, locker scenes) on qwen3.6-27b (tokenizer and stored runs only; UNVERIFIED)

Source x47_cue_27b, L32, gate {'pass': True, 'chosen': 300, 'org_read_accuracy': {'PP': 1.0, 'PM': 0.9985714285714286}, 'gate': 0.8}; items 300 (15 bridge entities); arms ['whole', 'no_jpp', 'no_jpp_rand', 'no_jpp_A', 'no_jpp_A_rand', 'no_A', 'no_A_rand']; reads 4800; A = number words, one-token letter variants; |A| tokens per item {'n': 300, 'min': 16, 'median': 20.0, 'max': 24, 'mean': 20.653, 'hist': {16: 49, 20: 153, 24: 98}}; answer words per item {'n': 300, 'min': 4, 'median': 5.0, 'max': 6, 'mean': 5.163, 'hist': {4: 49, 5: 153, 6: 98}}; items whose own answer word has no letter token: 0; Δ's 25 OMP atoms in A: not computable on CPU: needs Δ at L (GPU forwards) and no stored x0_atoms run fits these items; reported by the run (norms.jsonl n_answer_atoms_in_25).

Answer tokens (most common): ' four' x289, ' Four' x289, 'Four' x289, 'four' x289, ' two' x265, ' Two' x265, 'Two' x265, 'two' x265, ' eight' x174, ' Eight' x174, 'Eight' x174, 'eight' x174, 'one' x157, ' one' x157, ' One' x157, 'One' x157, ' seven' x153, ' Seven' x153, 'Seven' x153, 'seven' x153, ' five' x146, ' Five' x146, 'Five' x146, 'five' x146, ' six' x129, ' Six' x129, 'Six' x129, 'six' x129, ' three' x122, ' Three' x122

Split answer words (A keeps their first token): {}

Number-word variants as tokens: eight: {'eight': ['eight'], ' eight': [' eight'], 'Eight': ['Eight'], ' Eight': [' Eight']}; five: {'five': ['five'], ' five': [' five'], 'Five': ['Five'], ' Five': [' Five']}; four: {'four': ['four'], ' four': [' four'], 'Four': ['Four'], ' Four': [' Four']}; nine: {'nine': ['nine'], ' nine': [' nine'], 'Nine': ['Nine'], ' Nine': [' Nine']}; one: {'one': ['one'], ' one': [' one'], 'One': ['One'], ' One': [' One']}; seven: {'seven': ['seven'], ' seven': [' seven'], 'Seven': ['Seven'], ' Seven': [' Seven']}; six: {'six': ['six'], ' six': [' six'], 'Six': ['Six'], ' Six': [' Six']}; three: {'three': ['three'], ' three': [' three'], 'Three': ['Three'], ' Three': [' Three']}; two: {'two': ['two'], ' two': [' two'], 'Two': ['Two'], ' Two': [' Two']}

## C2-0037: spider -> eagle; A = [' two', ' four', ' six', ' eight', ' seven', ' Two', 'Two', ' nine', ' Four', ' Six', 'two', 'Four', ' Seven', 'four', ' Eight', ' Nine', 'Six', 'six', 'Eight', 'Seven', 'eight', 'seven', 'Nine', 'nine']

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

## C2-0254: cat -> turkey; A = [' two', ' three', ' four', ' six', ' eight', ' Two', 'Two', ' Four', ' Three', ' Six', 'Three', 'two', 'Four', 'three', 'four', ' Eight', 'Six', 'six', 'Eight', 'eight']

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

## C2-0399: spider -> cat; A = ['one', ' one', ' four', ' One', 'One', ' five', ' eight', ' seven', ' Four', ' Five', 'Four', ' Seven', 'four', ' Eight', 'Five', 'five', 'Eight', 'Seven', 'eight', 'seven']

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

## C2-0442: horse -> eagle; A = [' two', ' three', ' four', ' six', ' eight', ' seven', ' Two', 'Two', ' Four', ' Three', ' Six', 'Three', 'two', 'Four', 'three', ' Seven', 'four', ' Eight', 'Six', 'six', 'Eight', 'Seven', 'eight', 'seven']

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

## C2-0538: owl -> wolf; A = ['one', ' one', ' two', ' four', ' One', 'One', ' five', ' seven', ' Two', 'Two', ' Four', 'two', ' Five', 'Four', ' Seven', 'four', 'Five', 'five', 'Seven', 'seven']

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

