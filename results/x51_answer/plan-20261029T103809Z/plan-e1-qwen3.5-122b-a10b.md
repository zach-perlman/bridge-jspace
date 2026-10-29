# x51_answer plan (r2, amendment 20:20): the main test E1 (the bridge word) on qwen3.5-122b-a10b (tokenizer and stored runs only; UNVERIFIED)

Source qwen35_122b_x0_necessity_r2, L33, gate {'pass': True, 'chosen': 200, 'org_read_accuracy': {'PP': 0.9917, 'PM': 0.85}, 'gate': 0.8, 'eligible': 410}; items 200 (40 bridge entities); arms ['whole', 'no_jpp', 'no_jpp_rand', 'no_jpp_A', 'no_jpp_A_rand', 'no_A', 'no_A_rand']; reads 3200; A = number words, one-token letter variants; |A| tokens per item {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 15.0, 'hist': {8: 2, 12: 46, 16: 152}}; answer words per item {'n': 200, 'min': 2, 'median': 4.0, 'max': 4, 'mean': 3.75, 'hist': {2: 2, 3: 46, 4: 152}}; items whose own answer word has no letter token: 0; Δ's 25 OMP atoms in A: {'source': 'qwen35_122b_x0_atoms_letters', 'items': 38, 'n': 38, 'min': 0, 'median': 0.0, 'max': 0, 'mean': 0.0, 'hist': {0: 38}}.

Answer tokens (most common): ' two' x115, ' Two' x115, 'Two' x115, 'two' x115, ' six' x95, ' Six' x95, 'Six' x95, 'six' x95, ' four' x90, ' Four' x90, 'Four' x90, 'four' x90, ' eight' x90, ' Eight' x90, 'Eight' x90, 'eight' x90, ' three' x85, ' Three' x85, 'Three' x85, 'three' x85, ' seven' x78, ' Seven' x78, 'Seven' x78, 'seven' x78, 'one' x78, ' one' x78, ' One' x78, 'One' x78, ' nine' x63, ' Nine' x63

Split answer words (A keeps their first token): {}

Number-word variants as tokens: eight: {'eight': ['eight'], ' eight': [' eight'], 'Eight': ['Eight'], ' Eight': [' Eight']}; five: {'five': ['five'], ' five': [' five'], 'Five': ['Five'], ' Five': [' Five']}; four: {'four': ['four'], ' four': [' four'], 'Four': ['Four'], ' Four': [' Four']}; nine: {'nine': ['nine'], ' nine': [' nine'], 'Nine': ['Nine'], ' Nine': [' Nine']}; one: {'one': ['one'], ' one': [' one'], 'One': ['One'], ' One': [' One']}; seven: {'seven': ['seven'], ' seven': [' seven'], 'Seven': ['Seven'], ' Seven': [' Seven']}; six: {'six': ['six'], ' six': [' six'], 'Six': ['Six'], ' Six': [' Six']}; three: {'three': ['three'], ' three': [' three'], 'Three': ['Three'], ' Three': [' Three']}; two: {'two': ['two'], ' two': [' two'], 'Two': ['Two'], ' Two': [' Two']}

## P2-L0-0019: nitrogen -> oxygen; A = [' four', ' six', ' eight', ' seven', ' Four', ' Six', 'Four', ' Seven', 'four', ' Eight', 'Six', 'six', 'Eight', 'Seven', 'eight', 'seven']

lookup_org:

```
<|im_start|>user
James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ nitrogen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
James picked nitrogen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ oxygen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
James picked nitrogen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ oxygen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0106: lithium -> helium; A = [' two', ' three', ' six', ' Two', 'Two', ' nine', ' Three', ' Six', 'Three', 'two', 'three', ' Nine', 'Six', 'six', 'Nine', 'nine']

lookup_org:

```
<|im_start|>user
Will picked carbon. The locker of helium is 9. Paul picked⟦ lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Will picked carbon. The locker of helium is 9. Paul picked⟦ helium⟧. Amy picked lithium. The locker of carbon is 3. The locker of lithium is 6.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Will picked carbon. The locker of helium is 9. Paul picked⟦ lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Will picked carbon. The locker of helium is 9. Paul picked⟦ helium⟧. Amy picked lithium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0168: elephant -> fly; A = [' two', ' four', ' five', ' six', ' Two', 'Two', ' Four', ' Six', 'two', ' Five', 'Four', 'four', 'Five', 'Six', 'six', 'five']

lookup_org:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦ elephant⟧. Henry picked the fly.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦ fly⟧. Henry picked the elephant.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦ elephant⟧. Henry picked the fly.
How many legs does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦ fly⟧. Henry picked the elephant.
How many legs does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

## P2-L0-0298: hydrogen -> nitrogen; A = ['one', ' one', ' One', 'One', ' five', ' eight', ' seven', ' Five', ' Seven', ' Eight', 'Five', 'five', 'Eight', 'Seven', 'eight', 'seven']

lookup_org:

```
<|im_start|>user
The locker of hydrogen is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked⟦ hydrogen⟧. The locker of helium is seven. Anna picked nitrogen.
Which locker belongs to Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

lookup_alt:

```
<|im_start|>user
The locker of hydrogen is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked⟦ nitrogen⟧. The locker of helium is seven. Anna picked hydrogen.
Which locker belongs to Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_org:

```
<|im_start|>user
The locker of hydrogen is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked⟦ hydrogen⟧. The locker of helium is seven. Anna picked nitrogen.
What is the atomic number of Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

recall_alt:

```
<|im_start|>user
The locker of hydrogen is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked⟦ nitrogen⟧. The locker of helium is seven. Anna picked hydrogen.
What is the atomic number of Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

