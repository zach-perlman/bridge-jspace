# 47.5 verify pack: S's prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the bridge word, where its projection on the atoms (or the random subspace) is removed. UNVERIFIED.

## qwen3.5-9b: qwen35_9b_x47_5, 10 random items of 200 (seed 0)

### P2-L0-0017 (greek): bridge iota (O) → delta (S), token 30

**lookup** (PP-L0-0017): O's answer 2, S's answer 6

S, as read:

```
<|im_start|>user
The locker of delta is six. Amy picked iota. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ delta⟧. Eva picked gamma.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6\n' |

**recall** (PM-L0-0017): O's answer 9, S's answer 4

S, as read:

```
<|im_start|>user
The locker of delta is six. Amy picked iota. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ delta⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '4' | 1 | ' 4\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '4' | 1 | ' 4\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '4' | 1 | ' 4\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '4' | 1 | ' 4\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '4' | 1 | ' 4\n' |

### P2-L0-0096 (animals): bridge bee (O) → spider (S), token 43

**lookup** (PP-L0-0096): O's answer 1, S's answer 5

S, as read:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the bee. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ spider⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5\n' |

**recall** (PM-L0-0096): O's answer 6, S's answer 8

S, as read:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the bee. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ spider⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 0 | ' 8\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8\n' |

### P2-L0-0110 (greek): bridge iota (O) → epsilon (S), token 34

**lookup** (PP-L0-0110): O's answer 2, S's answer 7

S, as read:

```
<|im_start|>user
Ruby picked iota. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked⟦ epsilon⟧.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '7' | 1 | ' 7\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '7' | 1 | ' 7\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '7' | 1 | ' 7\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '7' | 1 | ' 7\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '7' | 1 | ' 7\n' |

**recall** (PM-L0-0110): O's answer 9, S's answer 5

S, as read:

```
<|im_start|>user
Ruby picked iota. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked⟦ epsilon⟧.
Which position in the Greek alphabet does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5\n' |

### P2-L0-0142 (elements): bridge nitrogen (O) → oxygen (S), token 27

**lookup** (PP-L0-0142): O's answer 3, S's answer 6

S, as read:

```
<|im_start|>user
Amy picked lithium. Vera picked nitrogen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ oxygen⟧. The locker of nitrogen is three.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6\n' |

**recall** (PM-L0-0142): O's answer 7, S's answer 8

S, as read:

```
<|im_start|>user
Amy picked lithium. Vera picked nitrogen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ oxygen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8\n' |

### P2-L0-0149 (greek): bridge delta (O) → iota (S), token 29

**lookup** (PP-L0-0149): O's answer 1, S's answer 8

S, as read:

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦ iota⟧. Kate picked gamma. Luke picked delta.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8\n' |

**recall** (PM-L0-0149): O's answer 4, S's answer 9

S, as read:

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦ iota⟧. Kate picked gamma. Luke picked delta.
Which position in the Greek alphabet does Lucy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '9' | 1 | ' 9\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '9' | 1 | ' 9\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '9' | 1 | ' 9\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '9' | 1 | ' 9\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '9' | 1 | ' 9\n' |

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
| none | S unedited | '3' | 1 | ' 3\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3\n' |

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
| none | S unedited | '2' | 1 | ' 2\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2\n' |

### P2-L0-0181 (elements): bridge helium (O) → nitrogen (S), token 37

**lookup** (PP-L0-0181): O's answer 3, S's answer 9

S, as read:

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked helium. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ nitrogen⟧.
Which locker belongs to Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '9' | 1 | ' 9\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '9' | 1 | ' 9\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '9' | 1 | ' 9\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '9' | 1 | ' 9\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '9' | 1 | ' 9\n' |

**recall** (PM-L0-0181): O's answer 2, S's answer 7

S, as read:

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked helium. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ nitrogen⟧.
What is the atomic number of Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '7' | 1 | ' 7\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '7' | 1 | ' 7\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '7' | 1 | ' 7\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '7' | 1 | ' 7\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '7' | 1 | ' 7\n' |

### P2-L0-0184 (elements): bridge helium (O) → hydrogen (S), token 25

**lookup** (PP-L0-0184): O's answer 9, S's answer 5

S, as read:

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked⟦ hydrogen⟧. The locker of hydrogen is 5. Luke picked helium.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5\n' |

**recall** (PM-L0-0184): O's answer 2, S's answer 1

S, as read:

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked⟦ hydrogen⟧. The locker of hydrogen is 5. Luke picked helium.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '1' | 1 | ' 1\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '1' | 1 | ' 1\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '1' | 1 | ' 1\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 0 | ' 2\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '1' | 1 | ' 1\n' |

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
| none | S unedited | '3' | 1 | ' 3\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3\n' |

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
| none | S unedited | '2' | 1 | ' 2\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2\n' |

### P2-L0-0290 (greek): bridge epsilon (O) → iota (S), token 34

**lookup** (PP-L0-0290): O's answer 4, S's answer 8

S, as read:

```
<|im_start|>user
Sara picked epsilon. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ iota⟧. Noah picked beta.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8\n' |

**recall** (PM-L0-0290): O's answer 5, S's answer 9

S, as read:

```
<|im_start|>user
Sara picked epsilon. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ iota⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '9' | 1 | ' 9\n' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '9' | 1 | ' 9\n' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '9' | 1 | ' 9\n' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '9' | 1 | ' 9\n' |
| rand_L3 | the random subspace of the same share at L..L+3 | '9' | 1 | ' 9\n' |

## qwen3.6-27b: x47_5_27b, 10 random items of 200 (seed 0)

### P2-L0-0010 (elements): bridge oxygen (O) → carbon (S), token 17

**lookup** (PP-L0-0010): O's answer 3, S's answer 7

S, as read:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦ carbon⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked oxygen.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0010): O's answer 8, S's answer 6

S, as read:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦ carbon⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked oxygen.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0069 (animals): bridge sheep (O) → butterfly (S), token 38

**lookup** (PP-L0-0069): O's answer 3, S's answer 7

S, as read:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ butterfly⟧. Ella picked the sheep.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0069): O's answer 4, S's answer 6

S, as read:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ butterfly⟧. Ella picked the sheep.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0080 (greek): bridge eta (O) → delta (S), token 13

**lookup** (PP-L0-0080): O's answer 6, S's answer 8

S, as read:

```
<|im_start|>user
Laura picked epsilon. Anna picked eta. Ivy picked⟦ delta⟧. The locker of delta is 8. The locker of eta is 6. The locker of epsilon is 1.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0080): O's answer 7, S's answer 4

S, as read:

```
<|im_start|>user
Laura picked epsilon. Anna picked eta. Ivy picked⟦ delta⟧. The locker of delta is 8. The locker of eta is 6. The locker of epsilon is 1.
Which position in the Greek alphabet does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0102 (animals): bridge butterfly (O) → goose (S), token 12

**lookup** (PP-L0-0102): O's answer 5, S's answer 8

S, as read:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦ goose⟧. Kate picked the butterfly. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0102): O's answer 6, S's answer 2

S, as read:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦ goose⟧. Kate picked the butterfly. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 0 | ' 8' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 0 | ' 8' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0107 (greek): bridge iota (O) → gamma (S), token 16

**lookup** (PP-L0-0107): O's answer 3, S's answer 9

S, as read:

```
<|im_start|>user
The locker of gamma is nine. Eva picked epsilon. David picked⟦ gamma⟧. The locker of epsilon is one. The locker of iota is three. Eve picked iota.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0107): O's answer 9, S's answer 3

S, as read:

```
<|im_start|>user
The locker of gamma is nine. Eva picked epsilon. David picked⟦ gamma⟧. The locker of epsilon is one. The locker of iota is three. Eve picked iota.
Which position in the Greek alphabet does David's pick have? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0111 (animals): bridge chicken (O) → rabbit (S), token 7

**lookup** (PP-L0-0111): O's answer 8, S's answer 7

S, as read:

```
<|im_start|>user
Ivy picked the⟦ rabbit⟧. The locker of the spider is 4. Diana picked the chicken. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0111): O's answer 2, S's answer 4

S, as read:

```
<|im_start|>user
Ivy picked the⟦ rabbit⟧. The locker of the spider is 4. Diana picked the chicken. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0128 (greek): bridge eta (O) → theta (S), token 17

**lookup** (PP-L0-0128): O's answer 2, S's answer 7

S, as read:

```
<|im_start|>user
The locker of theta is 7. Adam picked beta. Henry picked⟦ theta⟧. Liam picked eta. The locker of beta is 9. The locker of eta is 2.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0128): O's answer 7, S's answer 8

S, as read:

```
<|im_start|>user
The locker of theta is 7. Adam picked beta. Henry picked⟦ theta⟧. Liam picked eta. The locker of beta is 9. The locker of eta is 2.
Which position in the Greek alphabet does Henry's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '9' | 0 | ' 9' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '9' | 0 | ' 9' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8' |

### P2-L0-0130 (elements): bridge carbon (O) → lithium (S), token 5

**lookup** (PP-L0-0130): O's answer 4, S's answer 7

S, as read:

```
<|im_start|>user
Alice picked⟦ lithium⟧. The locker of hydrogen is 9. Frank picked carbon. The locker of carbon is 4. The locker of lithium is 7. Dan picked hydrogen.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0130): O's answer 6, S's answer 3

S, as read:

```
<|im_start|>user
Alice picked⟦ lithium⟧. The locker of hydrogen is 9. Frank picked carbon. The locker of carbon is 4. The locker of lithium is 7. Dan picked hydrogen.
What is the atomic number of Alice's pick? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0136 (elements): bridge hydrogen (O) → oxygen (S), token 6

**lookup** (PP-L0-0136): O's answer 3, S's answer 6

S, as read:

```
<|im_start|>user
Mia picked⟦ oxygen⟧. The locker of hydrogen is three. The locker of oxygen is six. Amy picked hydrogen. The locker of nitrogen is eight. Jack picked nitrogen.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0136): O's answer 1, S's answer 8

S, as read:

```
<|im_start|>user
Mia picked⟦ oxygen⟧. The locker of hydrogen is three. The locker of oxygen is six. Amy picked hydrogen. The locker of nitrogen is eight. Jack picked nitrogen.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|im_end|>
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

## muse-glimmer-30b: muse30_x47_5, 10 random items of 200 (seed 0)

### P2-L0-0019 (elements): bridge nitrogen (O) → oxygen (S), token 66

**lookup** (PP-L0-0019): O's answer 6, S's answer 4

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked nitrogen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ oxygen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
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
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked nitrogen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ oxygen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8' |

### P2-L0-0091 (elements): bridge oxygen (O) → hydrogen (S), token 73

**lookup** (PP-L0-0091): O's answer 7, S's answer 8

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked oxygen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ hydrogen⟧.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8' |

**recall** (PM-L0-0091): O's answer 8, S's answer 1

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked oxygen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ hydrogen⟧.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '1' | 1 | ' 1' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '1' | 1 | ' 1' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '1' | 1 | ' 1' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '1' | 1 | ' 1' |
| rand_L3 | the random subspace of the same share at L..L+3 | '1' | 1 | ' 1' |

### P2-L0-0106 (elements): bridge lithium (O) → helium (S), token 56

**lookup** (PP-L0-0106): O's answer 6, S's answer 9

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. Paul picked⟦ helium⟧. Amy picked lithium. The locker of carbon is 3. The locker of lithium is 6.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
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
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. Paul picked⟦ helium⟧. Amy picked lithium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0141 (animals): bridge bee (O) → elephant (S), token 63

**lookup** (PP-L0-0141): O's answer 4, S's answer 1

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the bee. Will picked the wolf. Dan picked the⟦ elephant⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '1' | 1 | ' 1' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '1' | 1 | ' 1' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '1' | 1 | ' 1' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '1' | 1 | ' 1' |
| rand_L3 | the random subspace of the same share at L..L+3 | '1' | 1 | ' 1' |

**recall** (PM-L0-0141): O's answer 6, S's answer 4

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the bee. Will picked the wolf. Dan picked the⟦ elephant⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '4' | 1 | ' 4' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '4' | 1 | ' 4' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '4' | 1 | ' 4' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '4' | 1 | ' 4' |
| rand_L3 | the random subspace of the same share at L..L+3 | '4' | 1 | ' 4' |

### P2-L0-0148 (elements): bridge nitrogen (O) → carbon (S), token 48

**lookup** (PP-L0-0148): O's answer 3, S's answer 2

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked nitrogen. Carl picked⟦ carbon⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

**recall** (PM-L0-0148): O's answer 7, S's answer 6

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked nitrogen. Carl picked⟦ carbon⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
What is the atomic number of Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6' |

### P2-L0-0155 (greek): bridge beta (O) → epsilon (S), token 44

**lookup** (PP-L0-0155): O's answer 5, S's answer 1

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ epsilon⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked beta.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '1' | 1 | ' 1' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '1' | 1 | ' 1' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '1' | 1 | ' 1' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '1' | 1 | ' 1' |
| rand_L3 | the random subspace of the same share at L..L+3 | '1' | 1 | ' 1' |

**recall** (PM-L0-0155): O's answer 2, S's answer 5

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ epsilon⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked beta.
Which position in the Greek alphabet does Maria's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5' |

### P2-L0-0175 (elements): bridge lithium (O) → carbon (S), token 58

**lookup** (PP-L0-0175): O's answer 9, S's answer 1

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. Mia picked⟦ carbon⟧. Liam picked lithium. Adam picked hydrogen. The locker of carbon is one.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '1' | 1 | ' 1' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '1' | 1 | ' 1' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '1' | 1 | ' 1' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '1' | 1 | ' 1' |
| rand_L3 | the random subspace of the same share at L..L+3 | '1' | 1 | ' 1' |

**recall** (PM-L0-0175): O's answer 3, S's answer 6

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. Mia picked⟦ carbon⟧. Liam picked lithium. Adam picked hydrogen. The locker of carbon is one.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '6' | 1 | ' 6' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '6' | 1 | ' 6' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '6' | 1 | ' 6' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '6' | 1 | ' 6' |
| rand_L3 | the random subspace of the same share at L..L+3 | '6' | 1 | ' 6' |

### P2-L0-0178 (elements): bridge carbon (O) → oxygen (S), token 51

**lookup** (PP-L0-0178): O's answer 7, S's answer 3

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. Lily picked⟦ oxygen⟧. Ryan picked carbon. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '3' | 1 | ' 3' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '3' | 1 | ' 3' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '3' | 1 | ' 3' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '3' | 1 | ' 3' |
| rand_L3 | the random subspace of the same share at L..L+3 | '3' | 1 | ' 3' |

**recall** (PM-L0-0178): O's answer 6, S's answer 8

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. Lily picked⟦ oxygen⟧. Ryan picked carbon. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
What is the atomic number of Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '8' | 1 | ' 8' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '8' | 1 | ' 8' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '8' | 1 | ' 8' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '8' | 1 | ' 8' |
| rand_L3 | the random subspace of the same share at L..L+3 | '8' | 1 | ' 8' |

### P2-L0-0187 (elements): bridge hydrogen (O) → helium (S), token 56

**lookup** (PP-L0-0187): O's answer 6, S's answer 1

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. Nina picked⟦ helium⟧. Maria picked hydrogen. The locker of hydrogen is 6. The locker of lithium is 2.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '1' | 1 | ' 1' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '1' | 1 | ' 1' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '1' | 1 | ' 1' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '1' | 1 | ' 1' |
| rand_L3 | the random subspace of the same share at L..L+3 | '1' | 1 | ' 1' |

**recall** (PM-L0-0187): O's answer 1, S's answer 2

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. Nina picked⟦ helium⟧. Maria picked hydrogen. The locker of hydrogen is 6. The locker of lithium is 2.
What is the atomic number of Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '2' | 1 | ' 2' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '2' | 1 | ' 2' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '2' | 1 | ' 2' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '2' | 1 | ' 2' |
| rand_L3 | the random subspace of the same share at L..L+3 | '2' | 1 | ' 2' |

### P2-L0-0284 (greek): bridge delta (O) → epsilon (S), token 44

**lookup** (PP-L0-0284): O's answer 7, S's answer 3

S, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ epsilon⟧. Julia picked beta. Hugo picked delta. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
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
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ epsilon⟧. Julia picked beta. Hugo picked delta. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | what | answer (top token) | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | '5' | 1 | ' 5' |
| zero_L | at L, S's bridge-word state without its projection on Δ_L's 25 OMP atoms | '5' | 1 | ' 5' |
| rand_L | at L, without its projection on a random subspace of the same share of ||h_S||^2 | '5' | 1 | ' 5' |
| zero_L3 | the same zeroing at L, L+1, L+2, L+3 (per-layer lens, Δ_l and OMP) | '5' | 1 | ' 5' |
| rand_L3 | the random subspace of the same share at L..L+3 | '5' | 1 | ' 5' |

