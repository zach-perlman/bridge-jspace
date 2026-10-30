# x52 view (verify pack): prompts as read with ⟦B⟧ ⟦E⟧ ⟦Q⟧ ⟦T⟧ marked, random write rows. UNVERIFIED.

## nemotron-3.5-lightning

### our scenes (the main test): 5 prompts of 200 (random.Random(0))

#### P2-L0-0037: hydrogen -> oxygen

lookup (answer 7, S's 9; tokens {"ans": [" seven", " Seven", "Seven"], "ans_S": [" nine", " Nine", "Nine"], "bridge": ["H", " hydrogen", "hydrogen", " Hydrogen"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Carl picked⟦B: hydrogen⟧. The locker of hydrogen is seven. Iris picked helium. The locker of helium is five. Clara picked oxygen. The locker of oxygen is nine.
Which locker belongs to Carl's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

recall (answer 1, S's 8; tokens {"ans": ["one", " one", " One", "One"], "ans_S": [" eight", " Eight", "Eight"], "bridge": ["H", " hydrogen", "hydrogen", " Hydrogen"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Carl picked⟦B: hydrogen⟧. The locker of hydrogen is seven. Iris picked helium. The locker of helium is five. Clara picked oxygen. The locker of oxygen is nine.
What is the atomic number of Carl's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

#### P2-L0-0165: sheep -> chicken

lookup (answer 3, S's 1; tokens {"ans": [" three", " Three", "Three", "three"], "ans_S": ["one", " one", " One", "One"], "bridge": [" She", "She", " sheep", "she"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Paul picked the⟦B: sheep⟧. The locker of the sheep is 3. Will picked the deer. The locker of the deer is 7. Zoe picked the chicken. The locker of the chicken is 1.
Which locker belongs to Paul's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

recall (answer 4, S's 2; tokens {"ans": [" four", " Four", "Four", "four"], "ans_S": [" two", " Two", "Two", "two"], "bridge": [" She", "She", " sheep", "she"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Paul picked the⟦B: sheep⟧. The locker of the sheep is 3. Will picked the deer. The locker of the deer is 7. Zoe picked the chicken. The locker of the chicken is 1.
How many legs does Paul's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

#### P2-L0-0225: rabbit -> fly

lookup (answer 9, S's 3; tokens {"ans": [" nine", " Nine", "Nine"], "ans_S": [" three", " Three", "Three", "three"], "bridge": [" rabbit", " Rabbit", "rabbit", "Rab"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the⟦E: rabbit⟧ is 9. The locker of the fly is 3. Liam picked the spider. Lily picked the fly. The locker of the spider is 4. Carl picked the⟦B: rabbit⟧.
Which locker belongs to Carl's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

recall (answer 4, S's 6; tokens {"ans": [" four", " Four", "Four", "four"], "ans_S": [" six", " Six", "Six", "six"], "bridge": [" rabbit", " Rabbit", "rabbit", "Rab"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the⟦E: rabbit⟧ is 9. The locker of the fly is 3. Liam picked the spider. Lily picked the fly. The locker of the spider is 4. Carl picked the⟦B: rabbit⟧.
How many legs does Carl's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

#### P2-L0-0247: hydrogen -> helium

lookup (answer 3, S's 6; tokens {"ans": [" three", " Three", "Three", "three"], "ans_S": [" six", " Six", "Six", "six"], "bridge": ["H", " hydrogen", "hydrogen", " Hydrogen"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Finn picked helium. The locker of⟦E: hydrogen⟧ is three. Clara picked⟦B: hydrogen⟧. Leo picked carbon. The locker of helium is six. The locker of carbon is two.
Which locker belongs to Clara's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

recall (answer 1, S's 2; tokens {"ans": ["one", " one", " One", "One"], "ans_S": [" two", " Two", "Two", "two"], "bridge": ["H", " hydrogen", "hydrogen", " Hydrogen"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Finn picked helium. The locker of⟦E: hydrogen⟧ is three. Clara picked⟦B: hydrogen⟧. Leo picked carbon. The locker of helium is six. The locker of carbon is two.
What is the atomic number of Clara's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

#### P2-L0-0443: delta -> epsilon

lookup (answer 6, S's 2; tokens {"ans": [" six", " Six", "Six", "six"], "ans_S": [" two", " Two", "Two", "two"], "bridge": ["Delta", "delta", " delta", " Delta"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of iota is 7. The locker of⟦E: delta⟧ is 6. Ella picked iota. Leo picked⟦B: delta⟧. Sean picked epsilon. The locker of epsilon is 2.
Which locker belongs to Leo's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

recall (answer 4, S's 5; tokens {"ans": [" four", " Four", "Four", "four"], "ans_S": [" five", " Five", "Five", "five"], "bridge": ["Delta", "delta", " delta", " Delta"]}), O as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of iota is 7. The locker of⟦E: delta⟧ is 6. Ella picked iota. Leo picked⟦B: delta⟧. Sean picked epsilon. The locker of epsilon is 2.
Which position in the Greek alphabet does Leo's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:⟦T: ⟧
```

#### main none: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0055 | lookup | T L38 | '6' | 0 | 0 |
| P2-L0-0298 | lookup | T L38 | '8' | 0 | 0 |
| P2-L0-0360 | lookup | T L38 | '3' | 0 | 0 |
| P2-L0-0447 | lookup | T L38 | '4' | 0 | 0 |
| P2-L0-0030 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0045 | recall | T L46 | '8' | 0 | 0 |
| P2-L0-0119 | recall | T L46 | '7' | 0 | 0 |
| P2-L0-0125 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0156 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0433 | recall | T L46 | '2' | 0 | 0 |

#### main whole: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0055 | lookup | T L38 | '9' | 1 | 1 |
| P2-L0-0298 | lookup | T L38 | '5' | 1 | 1 |
| P2-L0-0360 | lookup | T L38 | '8' | 1 | 1 |
| P2-L0-0447 | lookup | T L38 | '3' | 1 | 1 |
| P2-L0-0030 | recall | T L46 | '4' | 1 | 1 |
| P2-L0-0045 | recall | T L46 | '4' | 1 | 1 |
| P2-L0-0119 | recall | T L46 | '8' | 1 | 1 |
| P2-L0-0125 | recall | T L46 | '7' | 1 | 1 |
| P2-L0-0156 | recall | T L46 | '4' | 1 | 1 |
| P2-L0-0433 | recall | T L46 | '8' | 1 | 1 |

#### main ans1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0055 | lookup | T L38 | '6' | 0 | 0 |
| P2-L0-0298 | lookup | T L38 | '5' | 1 | 1 |
| P2-L0-0360 | lookup | T L38 | '3' | 0 | 0 |
| P2-L0-0447 | lookup | T L38 | '4' | 0 | 0 |
| P2-L0-0030 | recall | T L46 | '4' | 1 | 1 |
| P2-L0-0045 | recall | T L46 | '8' | 0 | 0 |
| P2-L0-0119 | recall | T L46 | '8' | 1 | 1 |
| P2-L0-0125 | recall | T L46 | '7' | 1 | 1 |
| P2-L0-0156 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0433 | recall | T L46 | '8' | 1 | 1 |

#### main ans2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0055 | lookup | T L38 | '6' | 0 | 0 |
| P2-L0-0298 | lookup | T L38 | '5' | 1 | 1 |
| P2-L0-0360 | lookup | T L38 | '3' | 0 | 0 |
| P2-L0-0447 | lookup | T L38 | '4' | 0 | 0 |
| P2-L0-0030 | recall | T L46 | 'Four' | 0 | 1 |
| P2-L0-0045 | recall | T L46 | 'Four' | 0 | 1 |
| P2-L0-0119 | recall | T L46 | 'Eight' | 0 | 1 |
| P2-L0-0125 | recall | T L46 | 'Seven' | 0 | 1 |
| P2-L0-0156 | recall | T L46 | 'Four' | 0 | 1 |
| P2-L0-0433 | recall | T L46 | ' Eight' | 0 | 1 |

#### main rand1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0055 | lookup | T L38 | '6' | 0 | 0 |
| P2-L0-0298 | lookup | T L38 | '8' | 0 | 0 |
| P2-L0-0360 | lookup | T L38 | '3' | 0 | 0 |
| P2-L0-0447 | lookup | T L38 | '4' | 0 | 0 |
| P2-L0-0030 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0045 | recall | T L46 | '8' | 0 | 0 |
| P2-L0-0119 | recall | T L46 | '7' | 0 | 0 |
| P2-L0-0125 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0156 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0433 | recall | T L46 | '2' | 0 | 0 |

#### main rand2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0055 | lookup | T L38 | '6' | 0 | 0 |
| P2-L0-0298 | lookup | T L38 | '8' | 0 | 0 |
| P2-L0-0360 | lookup | T L38 | '3' | 0 | 0 |
| P2-L0-0447 | lookup | T L38 | '4' | 0 | 0 |
| P2-L0-0030 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0045 | recall | T L46 | '8' | 0 | 0 |
| P2-L0-0119 | recall | T L46 | '8' | 1 | 1 |
| P2-L0-0125 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0156 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0433 | recall | T L46 | '4' | 0 | 1 |

#### main freq1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0055 | lookup | T L38 | '6' | 0 | 0 |
| P2-L0-0298 | lookup | T L38 | '8' | 0 | 0 |
| P2-L0-0360 | lookup | T L38 | '3' | 0 | 0 |
| P2-L0-0447 | lookup | T L38 | '4' | 0 | 0 |
| P2-L0-0030 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0045 | recall | T L46 | '8' | 0 | 0 |
| P2-L0-0119 | recall | T L46 | 'Carousel' | 0 | 1 |
| P2-L0-0125 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0156 | recall | T L46 | '2' | 0 | 0 |
| P2-L0-0433 | recall | T L46 | '2' | 0 | 0 |

#### main freq2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0055 | lookup | T L38 | '6' | 0 | 0 |
| P2-L0-0298 | lookup | T L38 | '8' | 0 | 0 |
| P2-L0-0360 | lookup | T L38 | '3' | 0 | 0 |
| P2-L0-0447 | lookup | T L38 | '4' | 0 | 0 |
| P2-L0-0030 | recall | T L46 | ' ' | 0 | 1 |
| P2-L0-0045 | recall | T L46 | ' ' | 0 | 1 |
| P2-L0-0119 | recall | T L46 | 'Carousel' | 0 | 1 |
| P2-L0-0125 | recall | T L46 | ' Dich' | 0 | 1 |
| P2-L0-0156 | recall | T L46 | ' ' | 0 | 1 |
| P2-L0-0433 | recall | T L46 | 'Carousel' | 0 | 1 |

## qwen3.5-122b-a10b

### our scenes (the main test): 5 prompts of 200 (random.Random(0))

#### P2-L0-0019: nitrogen -> oxygen

lookup (answer 6, S's 4; tokens {"ans": [" six", " Six", "Six", "six"], "ans_S": [" four", " Four", "Four", "four"], "bridge": ["nit", " nitrogen", " Nit", "Nit"]}), O as read:

```
<|im_start|>user
James picked oxygen. The locker of oxygen is four. The locker of⟦E: nitrogen⟧ is six. Adam picked lithium. Kyle picked⟦B: nitrogen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 7, S's 8; tokens {"ans": [" seven", " Seven", "Seven", "seven"], "ans_S": [" eight", " Eight", "Eight", "eight"], "bridge": ["nit", " nitrogen", " Nit", "Nit"]}), O as read:

```
<|im_start|>user
James picked oxygen. The locker of oxygen is four. The locker of⟦E: nitrogen⟧ is six. Adam picked lithium. Kyle picked⟦B: nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0106: lithium -> helium

lookup (answer 6, S's 9; tokens {"ans": [" six", " Six", "Six", "six"], "ans_S": [" nine", " Nine", "Nine", "nine"], "bridge": ["L", "l", " Lith", " lithium"]}), O as read:

```
<|im_start|>user
Will picked carbon. The locker of helium is 9. Paul picked⟦B: lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
Which locker belongs to Paul's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 3, S's 2; tokens {"ans": [" three", " Three", "Three", "three"], "ans_S": [" two", " Two", "Two", "two"], "bridge": ["L", "l", " Lith", " lithium"]}), O as read:

```
<|im_start|>user
Will picked carbon. The locker of helium is 9. Paul picked⟦B: lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0154: oxygen -> helium

lookup (answer 5, S's 3; tokens {"ans": [" five", " Five", "Five", "five"], "ans_S": [" three", " Three", "Three", "three"], "bridge": ["O", "o", " oxygen", " Oxygen"]}), O as read:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦B: oxygen⟧. Max picked helium. The locker of oxygen is five.
Which locker belongs to Sean's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 8, S's 2; tokens {"ans": [" eight", " Eight", "Eight", "eight"], "ans_S": [" two", " Two", "Two", "two"], "bridge": ["O", "o", " oxygen", " Oxygen"]}), O as read:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦B: oxygen⟧. Max picked helium. The locker of oxygen is five.
What is the atomic number of Sean's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0168: elephant -> fly

lookup (answer 2, S's 5; tokens {"ans": [" two", " Two", "Two", "two"], "ans_S": [" five", " Five", "Five", "five"], "bridge": ["ele", "Ele", " elephant", " Elephant"]}), O as read:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the⟦E: elephant⟧ is two. Kyle picked the⟦B: elephant⟧. Henry picked the fly.
Which locker belongs to Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 4, S's 6; tokens {"ans": [" four", " Four", "Four", "four"], "ans_S": [" six", " Six", "Six", "six"], "bridge": ["ele", "Ele", " elephant", " Elephant"]}), O as read:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the⟦E: elephant⟧ is two. Kyle picked the⟦B: elephant⟧. Henry picked the fly.
How many legs does Kyle's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0298: hydrogen -> nitrogen

lookup (answer 8, S's 5; tokens {"ans": [" eight", " Eight", "Eight", "eight"], "ans_S": [" five", " Five", "Five", "five"], "bridge": ["Hy", " hydrogen", " Hydro", "hydro"]}), O as read:

```
<|im_start|>user
The locker of⟦E: hydrogen⟧ is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked⟦B: hydrogen⟧. The locker of helium is seven. Anna picked nitrogen.
Which locker belongs to Ryan's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 1, S's 7; tokens {"ans": ["one", " one", " One", "One"], "ans_S": [" seven", " Seven", "Seven", "seven"], "bridge": ["Hy", " hydrogen", " Hydro", "hydro"]}), O as read:

```
<|im_start|>user
The locker of⟦E: hydrogen⟧ is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked⟦B: hydrogen⟧. The locker of helium is seven. Anna picked nitrogen.
What is the atomic number of Ryan's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### main none: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0037 | lookup | T L44 | '7' | 0 | 0 |
| P2-L0-0206 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0242 | lookup | T L44 | '1' | 0 | 0 |
| P2-L0-0302 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0012 | recall | T L44 | '6' | 0 | 0 |
| P2-L0-0029 | recall | T L44 | '8' | 0 | 0 |
| P2-L0-0076 | recall | T L44 | '1' | 0 | 0 |
| P2-L0-0081 | recall | T L44 | '4' | 0 | 0 |
| P2-L0-0095 | recall | T L44 | '3' | 0 | 0 |
| P2-L0-0290 | recall | T L44 | '5' | 0 | 0 |

#### main whole: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0037 | lookup | T L44 | '7' | 0 | 0 |
| P2-L0-0206 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0242 | lookup | T L44 | '1' | 0 | 0 |
| P2-L0-0302 | lookup | T L44 | '7' | 1 | 1 |
| P2-L0-0012 | recall | T L44 | '6' | 0 | 0 |
| P2-L0-0029 | recall | T L44 | '9' | 1 | 1 |
| P2-L0-0076 | recall | T L44 | '1' | 0 | 0 |
| P2-L0-0081 | recall | T L44 | '2' | 1 | 1 |
| P2-L0-0095 | recall | T L44 | '7' | 1 | 1 |
| P2-L0-0290 | recall | T L44 | '9' | 1 | 1 |

#### main ans1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0037 | lookup | T L44 | '7' | 0 | 0 |
| P2-L0-0206 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0242 | lookup | T L44 | '1' | 0 | 0 |
| P2-L0-0302 | lookup | T L44 | '7' | 1 | 1 |
| P2-L0-0012 | recall | T L44 | '6' | 0 | 0 |
| P2-L0-0029 | recall | T L44 | '9' | 1 | 1 |
| P2-L0-0076 | recall | T L44 | '1' | 0 | 0 |
| P2-L0-0081 | recall | T L44 | '2' | 1 | 1 |
| P2-L0-0095 | recall | T L44 | '7' | 1 | 1 |
| P2-L0-0290 | recall | T L44 | '5' | 0 | 0 |

#### main ans2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0037 | lookup | T L44 | '7' | 0 | 0 |
| P2-L0-0206 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0242 | lookup | T L44 | '1' | 0 | 0 |
| P2-L0-0302 | lookup | T L44 | '7' | 1 | 1 |
| P2-L0-0012 | recall | T L44 | '6' | 0 | 0 |
| P2-L0-0029 | recall | T L44 | 'nine' | 0 | 1 |
| P2-L0-0076 | recall | T L44 | '3' | 1 | 1 |
| P2-L0-0081 | recall | T L44 | '2' | 1 | 1 |
| P2-L0-0095 | recall | T L44 | ' seven' | 0 | 1 |
| P2-L0-0290 | recall | T L44 | 'nine' | 0 | 1 |

#### main rand1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0037 | lookup | T L44 | '7' | 0 | 0 |
| P2-L0-0206 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0242 | lookup | T L44 | '1' | 0 | 0 |
| P2-L0-0302 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0012 | recall | T L44 | '6' | 0 | 0 |
| P2-L0-0029 | recall | T L44 | '8' | 0 | 0 |
| P2-L0-0076 | recall | T L44 | '1' | 0 | 0 |
| P2-L0-0081 | recall | T L44 | '4' | 0 | 0 |
| P2-L0-0095 | recall | T L44 | '3' | 0 | 0 |
| P2-L0-0290 | recall | T L44 | '5' | 0 | 0 |

#### main rand2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0037 | lookup | T L44 | '7' | 0 | 0 |
| P2-L0-0206 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0242 | lookup | T L44 | '1' | 0 | 0 |
| P2-L0-0302 | lookup | T L44 | '7' | 1 | 1 |
| P2-L0-0012 | recall | T L44 | '6' | 0 | 0 |
| P2-L0-0029 | recall | T L44 | '8' | 0 | 0 |
| P2-L0-0076 | recall | T L44 | '1' | 0 | 0 |
| P2-L0-0081 | recall | T L44 | '4' | 0 | 0 |
| P2-L0-0095 | recall | T L44 | '3' | 0 | 0 |
| P2-L0-0290 | recall | T L44 | '5' | 0 | 0 |

#### main freq1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0037 | lookup | T L44 | '7' | 0 | 0 |
| P2-L0-0206 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0242 | lookup | T L44 | '1' | 0 | 0 |
| P2-L0-0302 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0012 | recall | T L44 | '6' | 0 | 0 |
| P2-L0-0029 | recall | T L44 | '8' | 0 | 0 |
| P2-L0-0076 | recall | T L44 | '1' | 0 | 0 |
| P2-L0-0081 | recall | T L44 | '4' | 0 | 0 |
| P2-L0-0095 | recall | T L44 | '3' | 0 | 0 |
| P2-L0-0290 | recall | T L44 | '5' | 0 | 0 |

#### main freq2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0037 | lookup | T L44 | 'ENCHMARK' | 0 | 1 |
| P2-L0-0206 | lookup | T L44 | '2' | 0 | 0 |
| P2-L0-0242 | lookup | T L44 | '1' | 0 | 0 |
| P2-L0-0302 | lookup | T L44 | 'nil' | 0 | 1 |
| P2-L0-0012 | recall | T L44 | '6' | 0 | 0 |
| P2-L0-0029 | recall | T L44 | 'are' | 0 | 1 |
| P2-L0-0076 | recall | T L44 | 'row' | 0 | 1 |
| P2-L0-0081 | recall | T L44 | 'firm' | 0 | 1 |
| P2-L0-0095 | recall | T L44 | 'nil' | 0 | 1 |
| P2-L0-0290 | recall | T L44 | 'are' | 0 | 1 |

