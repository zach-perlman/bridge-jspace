# x51_answer plan (r2, amendment 20:20): the main test E1 (the bridge word) on muse-glimmer-30b (tokenizer and stored runs only; UNVERIFIED)

Source muse30b_x0_necessity, L26, gate {'pass': True, 'chosen': 200, 'org_read_accuracy': {'PP': 0.966, 'PM': 0.8906}, 'gate': 0.8, 'eligible': 395}; items 200 (40 bridge entities); arms ['whole', 'no_jpp', 'no_jpp_rand', 'no_jpp_A', 'no_jpp_A_rand', 'no_A', 'no_A_rand']; reads 3200; A = number words, one-token letter variants; |A| tokens per item {'n': 200, 'min': 8, 'median': 16.0, 'max': 16, 'mean': 14.94, 'hist': {8: 2, 12: 49, 16: 149}}; answer words per item {'n': 200, 'min': 2, 'median': 4.0, 'max': 4, 'mean': 3.735, 'hist': {2: 2, 3: 49, 4: 149}}; items whose own answer word has no letter token: 0; Δ's 25 OMP atoms in A: not computable on CPU: needs Δ at L (GPU forwards) and no stored x0_atoms run fits these items; reported by the run (norms.jsonl n_answer_atoms_in_25).

Answer tokens (most common): ' two' x120, ' Two' x120, 'Two' x120, 'two' x120, ' six' x109, ' Six' x109, 'six' x109, 'Six' x109, ' four' x97, ' Four' x97, 'four' x97, 'Four' x97, ' three' x92, ' Three' x92, 'Three' x92, 'three' x92, ' eight' x84, 'eight' x84, ' Eight' x84, 'Eight' x84, ' seven' x78, ' Seven' x78, 'seven' x78, 'Seven' x78, 'one' x67, ' one' x67, ' One' x67, 'One' x67, ' five' x53, ' Five' x53

Split answer words (A keeps their first token): {}

Number-word variants as tokens: eight: {'eight': ['eight'], ' eight': [' eight'], 'Eight': ['Eight'], ' Eight': [' Eight']}; five: {'five': ['five'], ' five': [' five'], 'Five': ['Five'], ' Five': [' Five']}; four: {'four': ['four'], ' four': [' four'], 'Four': ['Four'], ' Four': [' Four']}; nine: {'nine': ['nine'], ' nine': [' nine'], 'Nine': ['Nine'], ' Nine': [' Nine']}; one: {'one': ['one'], ' one': [' one'], 'One': ['One'], ' One': [' One']}; seven: {'seven': ['seven'], ' seven': [' seven'], 'Seven': ['Seven'], ' Seven': [' Seven']}; six: {'six': ['six'], ' six': [' six'], 'Six': ['Six'], ' Six': [' Six']}; three: {'three': ['three'], ' three': [' three'], 'Three': ['Three'], ' Three': [' Three']}; two: {'two': ['two'], ' two': [' two'], 'Two': ['Two'], ' Two': [' Two']}

## P2-L0-0019: nitrogen -> oxygen; A = [' four', ' six', ' eight', ' seven', ' Four', 'four', ' Six', 'Four', 'eight', 'six', ' Seven', ' Eight', 'seven', 'Six', 'Seven', 'Eight']

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ nitrogen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked nitrogen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ oxygen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked nitrogen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ oxygen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

## P2-L0-0091: oxygen -> hydrogen; A = ['one', ' one', ' One', 'One', ' eight', ' seven', 'eight', ' Seven', ' Eight', 'seven', 'Seven', 'Eight']

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ oxygen⟧.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked oxygen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ hydrogen⟧.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ oxygen⟧.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked oxygen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ hydrogen⟧.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

## P2-L0-0141: bee -> elephant; A = ['one', ' one', ' four', ' six', ' One', 'One', ' Four', 'four', ' Six', 'Four', 'six', 'Six']

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦ bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the bee. Will picked the wolf. Dan picked the⟦ elephant⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦ bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the bee. Will picked the wolf. Dan picked the⟦ elephant⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

## P2-L0-0155: beta -> epsilon; A = ['one', ' one', ' two', ' five', ' One', 'One', ' Two', 'Two', 'two', ' Five', 'five', 'Five']

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ epsilon⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked beta.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which position in the Greek alphabet does Maria's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ epsilon⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked beta.
Which position in the Greek alphabet does Maria's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

## P2-L0-0284: delta -> epsilon; A = [' three', ' four', ' five', ' seven', ' Four', ' Three', 'Three', 'four', 'three', ' Five', 'Four', 'five', ' Seven', 'Five', 'seven', 'Seven']

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ epsilon⟧. Julia picked beta. Hugo picked delta. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ epsilon⟧. Julia picked beta. Hugo picked delta. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

