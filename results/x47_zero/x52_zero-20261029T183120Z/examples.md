# 47.5 verify pack: S's prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the bridge word, where its projection on the atoms (or the random subspace) is removed. UNVERIFIED.

## nemotron-3.5-lightning: nem35l_x52_zero, 10 random items of 200 (seed 0)

### P2-L0-0037 (elements): bridge hydrogen (O) → oxygen (S), token 10

**lookup** (PP-L0-0037): O's answer 7, S's answer 9

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Carl picked⟦ oxygen⟧. The locker of hydrogen is seven. Iris picked helium. The locker of helium is five. Clara picked hydrogen. The locker of oxygen is nine.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '9' | 1 | ' 9' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '9' | 1 | ' 9' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '9' | 1 | ' 9' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '9' | 1 | ' 9' |
| rand_L3 | the random subspace of the same share at L..L+3 | '9' | 1 | ' 9' |

**recall** (PM-L0-0037): O's answer 1, S's answer 8

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Carl picked⟦ oxygen⟧. The locker of hydrogen is seven. Iris picked helium. The locker of helium is five. Clara picked hydrogen. The locker of oxygen is nine.
What is the atomic number of Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8' |

### P2-L0-0165 (animals): bridge sheep (O) → chicken (S), token 11

**lookup** (PP-L0-0165): O's answer 3, S's answer 1

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Paul picked the⟦ chicken⟧. The locker of the sheep is 3. Will picked the deer. The locker of the deer is 7. Zoe picked the sheep. The locker of the chicken is 1.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '1' | 1 | ' 1' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '1' | 1 | ' 1' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '1' | 1 | ' 1' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '1' | 1 | ' 1' |
| rand_L3 | the random subspace of the same share at L..L+3 | '1' | 1 | ' 1' |

**recall** (PM-L0-0165): O's answer 4, S's answer 2

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Paul picked the⟦ chicken⟧. The locker of the sheep is 3. Will picked the deer. The locker of the deer is 7. Zoe picked the sheep. The locker of the chicken is 1.
How many legs does Paul's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0185 (greek): bridge epsilon (O) → gamma (S), token 26

**lookup** (PP-L0-0185): O's answer 8, S's answer 5

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of gamma is 5. The locker of epsilon is 8. James picked⟦ gamma⟧. The locker of alpha is 6. Emma picked alpha. Fiona picked epsilon.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5' |

**recall** (PM-L0-0185): O's answer 5, S's answer 3

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of gamma is 5. The locker of epsilon is 8. James picked⟦ gamma⟧. The locker of alpha is 6. Emma picked alpha. Fiona picked epsilon.
Which position in the Greek alphabet does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '3' | 1 | ' 3' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 5' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3' |

### P2-L0-0225 (animals): bridge rabbit (O) → fly (S), token 48

**lookup** (PP-L0-0225): O's answer 9, S's answer 3

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the rabbit is 9. The locker of the fly is 3. Liam picked the spider. Lily picked the rabbit. The locker of the spider is 4. Carl picked the⟦ fly⟧.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '3' | 1 | ' 3' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3' |

**recall** (PM-L0-0225): O's answer 4, S's answer 6

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the rabbit is 9. The locker of the fly is 3. Liam picked the spider. Lily picked the rabbit. The locker of the spider is 4. Carl picked the⟦ fly⟧.
How many legs does Carl's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6' |

### P2-L0-0235 (elements): bridge lithium (O) → carbon (S), token 15

**lookup** (PP-L0-0235): O's answer 2, S's answer 9

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Eve picked lithium. Sam picked⟦ carbon⟧. Noah picked oxygen. The locker of oxygen is 7. The locker of lithium is 2. The locker of carbon is 9.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '9' | 1 | ' 9' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '9' | 1 | ' 9' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '9' | 1 | ' 9' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '9' | 1 | ' 9' |
| rand_L3 | the random subspace of the same share at L..L+3 | '9' | 1 | ' 9' |

**recall** (PM-L0-0235): O's answer 3, S's answer 6

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Eve picked lithium. Sam picked⟦ carbon⟧. Noah picked oxygen. The locker of oxygen is 7. The locker of lithium is 2. The locker of carbon is 9.
What is the atomic number of Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6' |

### P2-L0-0247 (elements): bridge hydrogen (O) → helium (S), token 21

**lookup** (PP-L0-0247): O's answer 3, S's answer 6

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Finn picked hydrogen. The locker of hydrogen is three. Clara picked⟦ helium⟧. Leo picked carbon. The locker of helium is six. The locker of carbon is two.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6' |

**recall** (PM-L0-0247): O's answer 1, S's answer 2

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Finn picked hydrogen. The locker of hydrogen is three. Clara picked⟦ helium⟧. Leo picked carbon. The locker of helium is six. The locker of carbon is two.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0274 (elements): bridge oxygen (O) → lithium (S), token 17

**lookup** (PP-L0-0274): O's answer 1, S's answer 7

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of lithium is seven. Julia picked⟦ lithium⟧. The locker of nitrogen is three. James picked oxygen. Carl picked nitrogen. The locker of oxygen is one.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '7' | 1 | ' 7' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '7' | 1 | ' 7' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '7' | 1 | ' 7' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '7' | 1 | ' 7' |
| rand_L3 | the random subspace of the same share at L..L+3 | '7' | 1 | ' 7' |

**recall** (PM-L0-0274): O's answer 8, S's answer 3

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of lithium is seven. Julia picked⟦ lithium⟧. The locker of nitrogen is three. James picked oxygen. Carl picked nitrogen. The locker of oxygen is one.
What is the atomic number of Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '3' | 1 | ' 3' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3' |

### P2-L0-0284 (greek): bridge delta (O) → epsilon (S), token 11

**lookup** (PP-L0-0284): O's answer 7, S's answer 3

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Kyle picked⟦ epsilon⟧. Julia picked beta. Hugo picked delta. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '3' | 1 | ' 3' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3' |

**recall** (PM-L0-0284): O's answer 4, S's answer 5

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Kyle picked⟦ epsilon⟧. Julia picked beta. Hugo picked delta. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5' |

### P2-L0-0295 (elements): bridge helium (O) → hydrogen (S), token 26

**lookup** (PP-L0-0295): O's answer 5, S's answer 9

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Anna picked lithium. Amy picked helium. The locker of lithium is 1. Tara picked⟦ hydrogen⟧. The locker of helium is 5. The locker of hydrogen is 9.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '9' | 1 | ' 9' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '9' | 1 | ' 9' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '9' | 1 | ' 9' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '9' | 1 | ' 9' |
| rand_L3 | the random subspace of the same share at L..L+3 | '9' | 1 | ' 9' |

**recall** (PM-L0-0295): O's answer 2, S's answer 1

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Anna picked lithium. Amy picked helium. The locker of lithium is 1. Tara picked⟦ hydrogen⟧. The locker of helium is 5. The locker of hydrogen is 9.
What is the atomic number of Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '1' | 1 | ' 1' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '1' | 1 | ' 1' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '1' | 1 | ' 1' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '1' | 1 | ' 1' |
| rand_L3 | the random subspace of the same share at L..L+3 | '1' | 1 | ' 1' |

### P2-L0-0443 (greek): bridge delta (O) → epsilon (S), token 32

**lookup** (PP-L0-0443): O's answer 6, S's answer 2

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of iota is 7. The locker of delta is 6. Ella picked iota. Leo picked⟦ epsilon⟧. Sean picked delta. The locker of epsilon is 2.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

**recall** (PM-L0-0443): O's answer 4, S's answer 5

S, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of iota is 7. The locker of delta is 6. Ella picked iota. Leo picked⟦ epsilon⟧. Sean picked delta. The locker of epsilon is 2.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '4' | 0 | ' 4' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5' |

## qwen3.5-122b-a10b: qwen35_122b_x47_5, 10 random items of 200 (seed 0)

### P2-L0-0019 (elements): bridge nitrogen (O) → oxygen (S), token 27

**lookup** (PP-L0-0019): O's answer 6, S's answer 4

S, as read:

```
<|im_start|>user
James picked nitrogen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ oxygen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '4' | 1 | ' 4' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '4' | 1 | ' 4' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '4' | 1 | ' 4' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '4' | 1 | ' 4' |
| rand_L3 | the random subspace of the same share at L..L+3 | '4' | 1 | ' 4' |

**recall** (PM-L0-0019): O's answer 7, S's answer 8

S, as read:

```
<|im_start|>user
James picked nitrogen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ oxygen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8' |

### P2-L0-0106 (elements): bridge lithium (O) → helium (S), token 17

**lookup** (PP-L0-0106): O's answer 6, S's answer 9

S, as read:

```
<|im_start|>user
Will picked carbon. The locker of helium is 9. Paul picked⟦ helium⟧. Amy picked lithium. The locker of carbon is 3. The locker of lithium is 6.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '9' | 1 | ' 9' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '9' | 1 | ' 9' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '9' | 1 | ' 9' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '9' | 1 | ' 9' |
| rand_L3 | the random subspace of the same share at L..L+3 | '9' | 1 | ' 9' |

**recall** (PM-L0-0106): O's answer 3, S's answer 2

S, as read:

```
<|im_start|>user
Will picked carbon. The locker of helium is 9. Paul picked⟦ helium⟧. Amy picked lithium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0124 (elements): bridge nitrogen (O) → oxygen (S), token 6

**lookup** (PP-L0-0124): O's answer 5, S's answer 3

S, as read:

```
<|im_start|>user
Tara picked⟦ oxygen⟧. The locker of carbon is four. Adam picked nitrogen. The locker of oxygen is three. The locker of nitrogen is five. Noah picked carbon.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '3' | 1 | ' 3' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3' |

**recall** (PM-L0-0124): O's answer 7, S's answer 8

S, as read:

```
<|im_start|>user
Tara picked⟦ oxygen⟧. The locker of carbon is four. Adam picked nitrogen. The locker of oxygen is three. The locker of nitrogen is five. Noah picked carbon.
What is the atomic number of Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8' |

### P2-L0-0154 (elements): bridge oxygen (O) → helium (S), token 24

**lookup** (PP-L0-0154): O's answer 5, S's answer 3

S, as read:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ helium⟧. Max picked oxygen. The locker of oxygen is five.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '3' | 1 | ' 3' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3' |

**recall** (PM-L0-0154): O's answer 8, S's answer 2

S, as read:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ helium⟧. Max picked oxygen. The locker of oxygen is five.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0164 (greek): bridge delta (O) → beta (S), token 12

**lookup** (PP-L0-0164): O's answer 2, S's answer 7

S, as read:

```
<|im_start|>user
The locker of alpha is four. Lily picked⟦ beta⟧. Luke picked alpha. The locker of delta is two. Eva picked delta. The locker of beta is seven.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '7' | 1 | ' 7' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '7' | 1 | ' 7' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '7' | 1 | ' 7' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '7' | 1 | ' 7' |
| rand_L3 | the random subspace of the same share at L..L+3 | '7' | 1 | ' 7' |

**recall** (PM-L0-0164): O's answer 4, S's answer 2

S, as read:

```
<|im_start|>user
The locker of alpha is four. Lily picked⟦ beta⟧. Luke picked alpha. The locker of delta is two. Eva picked delta. The locker of beta is seven.
Which position in the Greek alphabet does Lily's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0168 (animals): bridge elephant (O) → fly (S), token 35

**lookup** (PP-L0-0168): O's answer 2, S's answer 5

S, as read:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦ fly⟧. Henry picked the elephant.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5' |

**recall** (PM-L0-0168): O's answer 4, S's answer 6

S, as read:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦ fly⟧. Henry picked the elephant.
How many legs does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6' |

### P2-L0-0188 (greek): bridge theta (O) → eta (S), token 21

**lookup** (PP-L0-0188): O's answer 5, S's answer 6

S, as read:

```
<|im_start|>user
Eric picked epsilon. Olivia picked theta. The locker of eta is 6. Lily picked⟦ eta⟧. The locker of theta is 5. The locker of epsilon is 3.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6' |

**recall** (PM-L0-0188): O's answer 8, S's answer 7

S, as read:

```
<|im_start|>user
Eric picked epsilon. Olivia picked theta. The locker of eta is 6. Lily picked⟦ eta⟧. The locker of theta is 5. The locker of epsilon is 3.
Which position in the Greek alphabet does Lily's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '7' | 1 | ' 7' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '7' | 1 | ' 7' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '7' | 1 | ' 7' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '7' | 1 | ' 7' |
| rand_L3 | the random subspace of the same share at L..L+3 | '7' | 1 | ' 7' |

### P2-L0-0193 (elements): bridge hydrogen (O) → helium (S), token 27

**lookup** (PP-L0-0193): O's answer 8, S's answer 3

S, as read:

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked hydrogen. Victor picked⟦ helium⟧. The locker of hydrogen is eight.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '3' | 1 | ' 3' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3' |

**recall** (PM-L0-0193): O's answer 1, S's answer 2

S, as read:

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked hydrogen. Victor picked⟦ helium⟧. The locker of hydrogen is eight.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0204 (animals): bridge tick (O) → horse (S), token 6

**lookup** (PP-L0-0204): O's answer 3, S's answer 8

S, as read:

```
<|im_start|>user
Maria picked the⟦ horse⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the tick.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8' |

**recall** (PM-L0-0204): O's answer 8, S's answer 4

S, as read:

```
<|im_start|>user
Maria picked the⟦ horse⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the tick.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '4' | 1 | ' 4' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '4' | 1 | ' 4' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '4' | 1 | ' 4' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '4' | 1 | ' 4' |
| rand_L3 | the random subspace of the same share at L..L+3 | '4' | 1 | ' 4' |

### P2-L0-0298 (elements): bridge hydrogen (O) → nitrogen (S), token 23

**lookup** (PP-L0-0298): O's answer 8, S's answer 5

S, as read:

```
<|im_start|>user
The locker of hydrogen is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked⟦ nitrogen⟧. The locker of helium is seven. Anna picked hydrogen.
Which locker belongs to Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5' |

**recall** (PM-L0-0298): O's answer 1, S's answer 7

S, as read:

```
<|im_start|>user
The locker of hydrogen is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked⟦ nitrogen⟧. The locker of helium is seven. Anna picked hydrogen.
What is the atomic number of Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '7' | 1 | ' 7' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '7' | 1 | ' 7' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '7' | 1 | ' 7' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '7' | 1 | ' 7' |
| rand_L3 | the random subspace of the same share at L..L+3 | '7' | 1 | ' 7' |

