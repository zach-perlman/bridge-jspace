# x51_answer plan (r2, amendment 20:20): the main test E1 (the bridge word) on qwen3.6-27b (tokenizer and stored runs only; UNVERIFIED)

Source x0_necessity_27b_chat, L32, gate {'pass': True, 'chosen': 200, 'org_read_accuracy': {'PP': 0.9967, 'PM': 0.9767}, 'gate': 0.8, 'eligible': 569}; items 200 (44 bridge entities); arms ['whole', 'no_jpp', 'no_jpp_rand', 'no_jpp_A', 'no_jpp_A_rand', 'no_A', 'no_A_rand']; reads 3200; A = number words, one-token letter variants; |A| tokens per item {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.86, 'hist': {8: 5, 12: 47, 16: 148}}; answer words per item {'n': 200, 'min': 2, 'median': 4.0, 'max': 4, 'mean': 3.715, 'hist': {2: 5, 3: 47, 4: 148}}; items whose own answer word has no letter token: 0; Δ's 25 OMP atoms in A: {'source': 'x0_atoms_27b_letters', 'items': 36, 'n': 36, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.083, 'hist': {0: 33, 1: 3}}.

Answer tokens (most common): ' two' x108, ' Two' x108, 'Two' x108, 'two' x108, ' four' x99, ' Four' x99, 'Four' x99, 'four' x99, ' six' x92, ' Six' x92, 'Six' x92, 'six' x92, ' three' x90, ' Three' x90, 'Three' x90, 'three' x90, ' eight' x89, ' Eight' x89, 'Eight' x89, 'eight' x89, ' seven' x81, ' Seven' x81, 'Seven' x81, 'seven' x81, 'one' x72, ' one' x72, ' One' x72, 'One' x72, ' five' x56, ' Five' x56

Split answer words (A keeps their first token): {}

Number-word variants as tokens: eight: {'eight': ['eight'], ' eight': [' eight'], 'Eight': ['Eight'], ' Eight': [' Eight']}; five: {'five': ['five'], ' five': [' five'], 'Five': ['Five'], ' Five': [' Five']}; four: {'four': ['four'], ' four': [' four'], 'Four': ['Four'], ' Four': [' Four']}; nine: {'nine': ['nine'], ' nine': [' nine'], 'Nine': ['Nine'], ' Nine': [' Nine']}; one: {'one': ['one'], ' one': [' one'], 'One': ['One'], ' One': [' One']}; seven: {'seven': ['seven'], ' seven': [' seven'], 'Seven': ['Seven'], ' Seven': [' Seven']}; six: {'six': ['six'], ' six': [' six'], 'Six': ['Six'], ' Six': [' Six']}; three: {'three': ['three'], ' three': [' three'], 'Three': ['Three'], ' Three': [' Three']}; two: {'two': ['two'], ' two': [' two'], 'Two': ['Two'], ' Two': [' Two']}

## P2-L0-0010: oxygen -> carbon; A = [' three', ' six', ' eight', ' seven', ' Three', ' Six', 'Three', 'three', ' Seven', ' Eight', 'Six', 'six', 'Eight', 'Seven', 'eight', 'seven']

lookup_org:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦ oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦ carbon⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked oxygen.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦ oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦ carbon⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked oxygen.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0069: sheep -> butterfly; A = [' three', ' four', ' six', ' seven', ' Four', ' Three', ' Six', 'Three', 'Four', 'three', ' Seven', 'four', 'Six', 'six', 'Seven', 'seven']

lookup_org:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ sheep⟧. Ella picked the butterfly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ butterfly⟧. Ella picked the sheep.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ sheep⟧. Ella picked the butterfly.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ butterfly⟧. Ella picked the sheep.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0102: butterfly -> goose; A = [' two', ' five', ' six', ' eight', ' Two', 'Two', ' Six', 'two', ' Five', ' Eight', 'Five', 'Six', 'six', 'five', 'Eight', 'eight']

lookup_org:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦ butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦ goose⟧. Kate picked the butterfly. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦ butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦ goose⟧. Kate picked the butterfly. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0111: chicken -> rabbit; A = [' two', ' four', ' eight', ' seven', ' Two', 'Two', ' Four', 'two', 'Four', ' Seven', 'four', ' Eight', 'Eight', 'Seven', 'eight', 'seven']

lookup_org:

```
<|im_start|>user
Ivy picked the⟦ chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Ivy picked the⟦ rabbit⟧. The locker of the spider is 4. Diana picked the chicken. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Ivy picked the⟦ chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Ivy picked the⟦ rabbit⟧. The locker of the spider is 4. Diana picked the chicken. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0204: tick -> horse; A = [' three', ' four', ' eight', ' Four', ' Three', 'Three', 'Four', 'three', 'four', ' Eight', 'Eight', 'eight']

lookup_org:

```
<|im_start|>user
Maria picked the⟦ tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Maria picked the⟦ horse⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the tick.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Maria picked the⟦ tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Maria picked the⟦ horse⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the tick.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

