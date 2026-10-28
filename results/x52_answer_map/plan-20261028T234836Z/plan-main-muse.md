# x52_answer_map plan: our scenes (the main test) on muse-glimmer-30b (tokenizer and stored runs only; UNVERIFIED)

Items 200 (40 bridge entities), source gate pass True; positions present {'lookup|B': 200, 'lookup|E': 92, 'lookup|Q': 200, 'lookup|T': 200, 'recall|B': 200, 'recall|E': 92, 'recall|Q': 200, 'recall|T': 200}; in order E < B < Q < T: 400 of 400; layers [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50].

Groups: B = the bridge word (X0's position, 51.10's P1); E = the bridge entity's last mention before the bridge word (its locker sentence), where there is one; Q = the question's 'pick' token (51.10's P2); T = the appended space token (51.10's P3).

## P2-L0-0019: nitrogen -> oxygen; tokens {"lookup": {"ans": [" six", " Six", "six", "Six"], "ans_S": [" four", " Four", "four", "Four"], "bridge": ["nit", " nitrogen", " Nitrogen", "Nit"]}, "recall": {"ans": [" seven", " Seven", "seven", "Seven"], "ans_S": [" eight", "eight", " Eight", "Eight"], "bridge": ["nit", " nitrogen", " Nitrogen", "Nit"]}}

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of⟦E: nitrogen⟧ is six. Adam picked lithium. Kyle picked⟦B: nitrogen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked nitrogen. The locker of oxygen is four. The locker of⟦E: nitrogen⟧ is six. Adam picked lithium. Kyle picked⟦B: oxygen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of⟦E: nitrogen⟧ is six. Adam picked lithium. Kyle picked⟦B: nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked nitrogen. The locker of oxygen is four. The locker of⟦E: nitrogen⟧ is six. Adam picked lithium. Kyle picked⟦B: oxygen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

## P2-L0-0091: oxygen -> hydrogen; tokens {"lookup": {"ans": [" seven", " Seven", "seven", "Seven"], "ans_S": [" eight", "eight", " Eight", "Eight"], "bridge": ["O", "o", " oxygen", " Oxygen"]}, "recall": {"ans": [" eight", "eight", " Eight", "Eight"], "ans_S": ["one", " one", " One", "One"], "bridge": ["O", "o", " oxygen", " Oxygen"]}}

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of⟦E: oxygen⟧ is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦B: oxygen⟧.
Which locker belongs to Clara's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked oxygen. The locker of⟦E: oxygen⟧ is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦B: hydrogen⟧.
Which locker belongs to Clara's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of⟦E: oxygen⟧ is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦B: oxygen⟧.
What is the atomic number of Clara's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked oxygen. The locker of⟦E: oxygen⟧ is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦B: hydrogen⟧.
What is the atomic number of Clara's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

## P2-L0-0141: bee -> elephant; tokens {"lookup": {"ans": [" four", " Four", "four", "Four"], "ans_S": ["one", " one", " One", "One"], "bridge": ["bee", " bee", " Bee", "Bee"]}, "recall": {"ans": [" six", " Six", "six", "Six"], "ans_S": [" four", " Four", "four", "Four"], "bridge": ["bee", " bee", " Bee", "Bee"]}}

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the⟦E: bee⟧ is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦B: bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the⟦E: bee⟧ is four. Hugo picked the bee. Will picked the wolf. Dan picked the⟦B: elephant⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the⟦E: bee⟧ is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦B: bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the⟦E: bee⟧ is four. Hugo picked the bee. Will picked the wolf. Dan picked the⟦B: elephant⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

## P2-L0-0155: beta -> epsilon; tokens {"lookup": {"ans": [" five", " Five", "five", "Five"], "ans_S": ["one", " one", " One", "One"], "bridge": ["beta", " beta", " Beta", "Beta"]}, "recall": {"ans": [" two", " Two", "Two", "two"], "ans_S": [" five", " Five", "five", "Five"], "bridge": ["beta", " beta", " Beta", "Beta"]}}

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦B: beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which locker belongs to Maria's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦B: epsilon⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked beta.
Which locker belongs to Maria's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦B: beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which position in the Greek alphabet does Maria's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦B: epsilon⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked beta.
Which position in the Greek alphabet does Maria's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

## P2-L0-0284: delta -> epsilon; tokens {"lookup": {"ans": [" seven", " Seven", "seven", "Seven"], "ans_S": [" three", " Three", "Three", "three"], "bridge": ["Delta", " delta", "delta", " Delta"]}, "recall": {"ans": [" four", " Four", "four", "Four"], "ans_S": [" five", " Five", "five", "Five"], "bridge": ["Delta", " delta", "delta", " Delta"]}}

lookup_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦B: delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

lookup_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦B: epsilon⟧. Julia picked beta. Hugo picked delta. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_org:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦B: delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall_alt:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦B: epsilon⟧. Julia picked beta. Hugo picked delta. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

