# 48.3 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word, ⟦write:…⟧ the written sentence's item and number tokens. UNVERIFIED.

## x48_bind_27b: 10 random written scenes of 139 (seed 0)

### P2-L0-0080 (main, greek): bridge eta picked by Ivy; written: delta (picked by Anna; locker 8, attribute 4)

**lookup** (PP-L0-0080): O's answer 6, the written item's 8

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. Ivy picked ⟦bridge:eta⟧. The locker of ⟦write:delta⟧ is ⟦write:8⟧. The locker of eta is 6. The locker of epsilon is 1.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | ' 6' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | ' 6' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '6' | original | ' 6' |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | ' 6' |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | ' 6' |

**recall** (PM-L0-0080): O's answer 7, the written item's 4

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. Ivy picked ⟦bridge:eta⟧. The locker of ⟦write:delta⟧ is ⟦write:8⟧. The locker of eta is 6. The locker of epsilon is 1.
Which position in the Greek alphabet does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | ' 7' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | ' 7' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | ' 7' |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | ' 7' |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | ' 7' |

### P2-L0-0157 (45m, elements): bridge oxygen picked by Julia; written: carbon (picked by Amy; locker 1, attribute 6)

**lookup** (PP-L0-0157): O's answer 9, the written item's 1

```
<|im_start|>user
Julia picked ⟦bridge:oxygen⟧. Amy picked carbon. The locker of hydrogen is 5. The locker of nitrogen is 6. The locker of ⟦write:carbon⟧ is ⟦write:1⟧. Tom picked nitrogen. The locker of oxygen is 9.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '9' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '9' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '9' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '9' | original | None |

**recall** (PM-L0-0157): O's answer 8, the written item's 6

```
<|im_start|>user
Julia picked ⟦bridge:oxygen⟧. Amy picked carbon. The locker of hydrogen is 5. The locker of nitrogen is 6. The locker of ⟦write:carbon⟧ is ⟦write:1⟧. Tom picked nitrogen. The locker of oxygen is 9.
What is the atomic number of Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | None |

### P2-L0-0216 (45m, animals): bridge wolf picked by Mia; written: horse (picked by Hugo; locker 5, attribute 4)

**lookup** (PP-L0-0216): O's answer 9, the written item's 5

```
<|im_start|>user
Nina picked the eagle. The locker of the eagle is three. Hugo picked the horse. Mia picked the ⟦bridge:wolf⟧. The locker of the ant is two. The locker of the wolf is nine. The locker of the ⟦write:horse⟧ is ⟦write:five⟧.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '9' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '9' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '9' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '9' | original | None |

**recall** (PM-L0-0216): O's answer 4, the written item's 4

```
<|im_start|>user
Nina picked the eagle. The locker of the eagle is three. Hugo picked the horse. Mia picked the ⟦bridge:wolf⟧. The locker of the ant is two. The locker of the wolf is nine. The locker of the ⟦write:horse⟧ is ⟦write:five⟧.
How many legs does Mia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | same | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | same | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | same | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | same | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | same | None |

### P2-L0-0310 (45m, elements): bridge helium picked by Victor; written: lithium (picked by David; locker 4, attribute 3)

**lookup** (PP-L0-0310): O's answer 5, the written item's 4

```
<|im_start|>user
The locker of carbon is 1. David picked lithium. Victor picked ⟦bridge:helium⟧. Eric picked carbon. The locker of ⟦write:lithium⟧ is ⟦write:4⟧. The locker of helium is 5. The locker of oxygen is 2.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '5' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '5' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '5' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '5' | original | None |

**recall** (PM-L0-0310): O's answer 2, the written item's 3

```
<|im_start|>user
The locker of carbon is 1. David picked lithium. Victor picked ⟦bridge:helium⟧. Eric picked carbon. The locker of ⟦write:lithium⟧ is ⟦write:4⟧. The locker of helium is 5. The locker of oxygen is 2.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | None |

### P2-L0-0350 (45m, greek): bridge eta picked by Anna; written: epsilon (picked by Carl; locker 1, attribute 5)

**lookup** (PP-L0-0350): O's answer 3, the written item's 1

```
<|im_start|>user
Anna picked ⟦bridge:eta⟧. The locker of alpha is 7. Carl picked epsilon. The locker of eta is 3. The locker of gamma is 2. The locker of ⟦write:epsilon⟧ is ⟦write:1⟧. Ruby picked alpha.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | None |

**recall** (PM-L0-0350): O's answer 7, the written item's 5

```
<|im_start|>user
Anna picked ⟦bridge:eta⟧. The locker of alpha is 7. Carl picked epsilon. The locker of eta is 3. The locker of gamma is 2. The locker of ⟦write:epsilon⟧ is ⟦write:1⟧. Ruby picked alpha.
Which position in the Greek alphabet does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | None |

### P2-L0-0370 (45m, elements): bridge helium picked by Sam; written: lithium (picked by Eve; locker 5, attribute 3)

**lookup** (PP-L0-0370): O's answer 9, the written item's 5

```
<|im_start|>user
Sam picked ⟦bridge:helium⟧. The locker of helium is nine. The locker of nitrogen is three. Eve picked lithium. The locker of ⟦write:lithium⟧ is ⟦write:five⟧. The locker of oxygen is one. Amy picked nitrogen.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | original | ' 9' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '9' | original | ' 9' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '9' | original | ' 9' |
| r1 | a random vector of the s = 1 write's norm, per token | '9' | original | ' 9' |
| r2 | a random vector of the s = 2 write's norm, per token | '9' | original | ' 9' |

**recall** (PM-L0-0370): O's answer 2, the written item's 3

```
<|im_start|>user
Sam picked ⟦bridge:helium⟧. The locker of helium is nine. The locker of nitrogen is three. Eve picked lithium. The locker of ⟦write:lithium⟧ is ⟦write:five⟧. The locker of oxygen is one. Amy picked nitrogen.
What is the atomic number of Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | ' 2' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | ' 2' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | ' 2' |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | ' 2' |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | ' 2' |

### P2-L0-0409 (45m, elements): bridge oxygen picked by Henry; written: nitrogen (picked by Emma; locker 1, attribute 7)

**lookup** (PP-L0-0409): O's answer 9, the written item's 1

```
<|im_start|>user
The locker of hydrogen is 2. Henry picked ⟦bridge:oxygen⟧. The locker of helium is 4. The locker of oxygen is 9. Lucy picked hydrogen. Emma picked nitrogen. The locker of ⟦write:nitrogen⟧ is ⟦write:1⟧.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '9' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '9' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '9' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '9' | original | None |

**recall** (PM-L0-0409): O's answer 8, the written item's 7

```
<|im_start|>user
The locker of hydrogen is 2. Henry picked ⟦bridge:oxygen⟧. The locker of helium is 4. The locker of oxygen is 9. Lucy picked hydrogen. Emma picked nitrogen. The locker of ⟦write:nitrogen⟧ is ⟦write:1⟧.
What is the atomic number of Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | None |

### P2-L0-0495 (45m, animals): bridge deer picked by Leo; written: bee (picked by Sara; locker 2, attribute 6)

**lookup** (PP-L0-0495): O's answer 3, the written item's 2

```
<|im_start|>user
Leo picked the ⟦bridge:deer⟧. Eve picked the beetle. Sara picked the bee. The locker of the ⟦write:bee⟧ is ⟦write:2⟧. The locker of the chicken is 6. The locker of the deer is 3. The locker of the beetle is 4.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | None |

**recall** (PM-L0-0495): O's answer 4, the written item's 6

```
<|im_start|>user
Leo picked the ⟦bridge:deer⟧. Eve picked the beetle. Sara picked the bee. The locker of the ⟦write:bee⟧ is ⟦write:2⟧. The locker of the chicken is 6. The locker of the deer is 3. The locker of the beetle is 4.
How many legs does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | original | None |

### P2-L0-0517 (45m, elements): bridge nitrogen picked by Ivy; written: oxygen (picked by David; locker 7, attribute 8)

**lookup** (PP-L0-0517): O's answer 2, the written item's 7

```
<|im_start|>user
The locker of carbon is four. David picked oxygen. Iris picked carbon. Ivy picked ⟦bridge:nitrogen⟧. The locker of nitrogen is two. The locker of ⟦write:oxygen⟧ is ⟦write:seven⟧. The locker of hydrogen is eight.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | None |

**recall** (PM-L0-0517): O's answer 7, the written item's 8

```
<|im_start|>user
The locker of carbon is four. David picked oxygen. Iris picked carbon. Ivy picked ⟦bridge:nitrogen⟧. The locker of nitrogen is two. The locker of ⟦write:oxygen⟧ is ⟦write:seven⟧. The locker of hydrogen is eight.
What is the atomic number of Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | None |

### P2-L0-0559 (45m, elements): bridge nitrogen picked by Grace; written: helium (picked by Finn; locker 6, attribute 2)

**lookup** (PP-L0-0559): O's answer 2, the written item's 6

```
<|im_start|>user
The locker of oxygen is 5. Finn picked helium. Tara picked oxygen. Grace picked ⟦bridge:nitrogen⟧. The locker of lithium is 7. The locker of nitrogen is 2. The locker of ⟦write:helium⟧ is ⟦write:6⟧.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | None |

**recall** (PM-L0-0559): O's answer 7, the written item's 2

```
<|im_start|>user
The locker of oxygen is 5. Finn picked helium. Tara picked oxygen. Grace picked ⟦bridge:nitrogen⟧. The locker of lithium is 7. The locker of nitrogen is 2. The locker of ⟦write:helium⟧ is ⟦write:6⟧.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | None |

