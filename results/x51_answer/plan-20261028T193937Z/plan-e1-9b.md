# x51_answer plan (r2, amendment 20:20): the main test E1 (the bridge word) on qwen3.5-9b (tokenizer and stored runs only; UNVERIFIED)

Source qwen35_9b_x0_necessity, L12, gate {'pass': True, 'chosen': 200, 'org_read_accuracy': {'PP': 0.95, 'PM': 0.8683}, 'gate': 0.8, 'eligible': 408}; items 200 (40 bridge entities); arms ['whole', 'no_jpp', 'no_jpp_rand', 'no_jpp_A', 'no_jpp_A_rand', 'no_A', 'no_A_rand']; reads 3200; A = number words, one-token letter variants; |A| tokens per item {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.9, 'hist': {8: 2, 12: 51, 16: 147}}; answer words per item {'n': 200, 'min': 2, 'median': 4.0, 'max': 4, 'mean': 3.725, 'hist': {2: 2, 3: 51, 4: 147}}; items whose own answer word has no letter token: 0; Δ's 25 OMP atoms in A: {'source': 'qwen35_9b_x0_atoms_letters', 'items': 40, 'n': 40, 'min': 0, 'median': 0.0, 'max': 1, 'mean': 0.025, 'hist': {0: 39, 1: 1}}.

Answer tokens (most common): ' two' x117, ' Two' x117, 'Two' x117, 'two' x117, ' four' x101, ' Four' x101, 'Four' x101, 'four' x101, ' three' x99, ' Three' x99, 'Three' x99, 'three' x99, ' six' x98, ' Six' x98, 'Six' x98, 'six' x98, ' eight' x76, ' Eight' x76, 'Eight' x76, 'eight' x76, 'one' x72, ' one' x72, ' One' x72, 'One' x72, ' seven' x67, ' Seven' x67, 'Seven' x67, 'seven' x67, ' nine' x67, ' Nine' x67

Split answer words (A keeps their first token): {}

Number-word variants as tokens: eight: {'eight': ['eight'], ' eight': [' eight'], 'Eight': ['Eight'], ' Eight': [' Eight']}; five: {'five': ['five'], ' five': [' five'], 'Five': ['Five'], ' Five': [' Five']}; four: {'four': ['four'], ' four': [' four'], 'Four': ['Four'], ' Four': [' Four']}; nine: {'nine': ['nine'], ' nine': [' nine'], 'Nine': ['Nine'], ' Nine': [' Nine']}; one: {'one': ['one'], ' one': [' one'], 'One': ['One'], ' One': [' One']}; seven: {'seven': ['seven'], ' seven': [' seven'], 'Seven': ['Seven'], ' Seven': [' Seven']}; six: {'six': ['six'], ' six': [' six'], 'Six': ['Six'], ' Six': [' Six']}; three: {'three': ['three'], ' three': [' three'], 'Three': ['Three'], ' Three': [' Three']}; two: {'two': ['two'], ' two': [' two'], 'Two': ['Two'], ' Two': [' Two']}

## P2-L0-0017: iota -> delta; A = [' two', ' four', ' six', ' Two', 'Two', ' nine', ' Four', ' Six', 'two', 'Four', 'four', ' Nine', 'Six', 'six', 'Nine', 'nine']

lookup_org:

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of delta is six. Amy picked iota. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ delta⟧. Eva picked gamma.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of delta is six. Amy picked iota. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ delta⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0096: bee -> spider; A = ['one', ' one', ' One', 'One', ' five', ' six', ' eight', ' Six', ' Five', ' Eight', 'Five', 'Six', 'six', 'five', 'Eight', 'eight']

lookup_org:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the bee. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ spider⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the bee. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ spider⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0142: nitrogen -> oxygen; A = [' three', ' six', ' eight', ' seven', ' Three', ' Six', 'Three', 'three', ' Seven', ' Eight', 'Six', 'six', 'Eight', 'Seven', 'eight', 'seven']

lookup_org:

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ nitrogen⟧. The locker of nitrogen is three.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Amy picked lithium. Vera picked nitrogen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ oxygen⟧. The locker of nitrogen is three.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ nitrogen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Amy picked lithium. Vera picked nitrogen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ oxygen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0154: oxygen -> helium; A = [' two', ' three', ' five', ' eight', ' Two', 'Two', ' Three', 'Three', 'two', ' Five', 'three', ' Eight', 'Five', 'five', 'Eight', 'eight']

lookup_org:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ oxygen⟧. Max picked helium. The locker of oxygen is five.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ helium⟧. Max picked oxygen. The locker of oxygen is five.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ oxygen⟧. Max picked helium. The locker of oxygen is five.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ helium⟧. Max picked oxygen. The locker of oxygen is five.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0290: epsilon -> iota; A = [' four', ' five', ' eight', ' nine', ' Four', ' Five', 'Four', 'four', ' Eight', 'Five', ' Nine', 'five', 'Eight', 'eight', 'Nine', 'nine']

lookup_org:

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ epsilon⟧. Noah picked beta.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Sara picked epsilon. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ iota⟧. Noah picked beta.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ epsilon⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Sara picked epsilon. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ iota⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

