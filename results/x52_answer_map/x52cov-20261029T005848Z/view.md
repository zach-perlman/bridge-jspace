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

