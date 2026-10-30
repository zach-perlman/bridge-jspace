# 49.1 verify pack: O's prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the bridge word, where each arm adds its vector at L. UNVERIFIED.

## qwen3.5-122b-a10b: qwen35_122b_gain, 10 random items of 53 (seed 0)

### P2-L0-0017 (greek): bridge iota (O) → delta (S), token 30

**lookup** (PP-L0-0017): O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2' |
| J(0,0.5) | '2' | 0 | ' 2' |
| J(0,1) | '6' | 1 | ' 6' |
| J(0,1.5) | '6' | 1 | ' 6' |
| J(0,2) | '6' | 1 | ' 6' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '2' | 0 | ' 2' |
| J(0.5,1) | '6' | 1 | ' 6' |
| J(0.5,1.5) | '6' | 1 | ' 6' |
| J(0.5,2) | '6' | 1 | ' 6' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '6' | 1 | ' 6' |
| J(1,1) | '6' | 1 | ' 6' |
| J(1,1.5) | '6' | 1 | ' 6' |
| J(1,2) | '6' | 1 | ' 6' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '6' | 1 | ' 6' |
| J(1.5,1) | '6' | 1 | ' 6' |
| J(1.5,1.5) | '6' | 1 | ' 6' |
| J(1.5,2) | '6' | 1 | ' 6' |
| J(2,0) | '2' | 0 | ' 2' |
| J(2,0.5) | '6' | 1 | ' 6' |
| J(2,1) | '6' | 1 | ' 6' |
| J(2,1.5) | '6' | 1 | ' 6' |
| J(2,2) | '6' | 1 | ' 6' |
| R(0,1) | '6' | 1 | ' 6' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '2' | 0 | ' 2' |
| R(0,2) | '6' | 1 | ' 6' |
| J(0,2)-U | '8' | 0 | ' 8' |
| J(0,2)-RU | '6' | 1 | ' 6' |

**recall** (PM-L0-0017): O's answer 9, S's answer 4

O, as read:

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '9' | 0 | ' 9' |
| J(0,0.5) | '9' | 0 | ' 9' |
| J(0,1) | '4' | 1 | ' 4' |
| J(0,1.5) | '4' | 1 | ' 4' |
| J(0,2) | '4' | 1 | ' 4' |
| J(0.5,0) | '9' | 0 | ' 9' |
| J(0.5,0.5) | '9' | 0 | ' 4' |
| J(0.5,1) | '4' | 1 | ' 4' |
| J(0.5,1.5) | '4' | 1 | ' 4' |
| J(0.5,2) | '4' | 1 | ' 4' |
| J(1,0) | '9' | 0 | ' 9' |
| J(1,0.5) | '4' | 1 | ' 4' |
| J(1,1) | '4' | 1 | ' 4' |
| J(1,1.5) | '4' | 1 | ' 4' |
| J(1,2) | '4' | 1 | ' 4' |
| J(1.5,0) | '9' | 0 | ' 9' |
| J(1.5,0.5) | '4' | 1 | ' 4' |
| J(1.5,1) | '4' | 1 | ' 4' |
| J(1.5,1.5) | '4' | 1 | ' 4' |
| J(1.5,2) | '4' | 1 | ' 4' |
| J(2,0) | '4' | 1 | ' 4' |
| J(2,0.5) | '4' | 1 | ' 4' |
| J(2,1) | '4' | 1 | ' 4' |
| J(2,1.5) | '4' | 1 | ' 4' |
| J(2,2) | '4' | 1 | ' 4' |
| R(0,1) | '4' | 1 | ' 4' |
| R(1,0) | '9' | 0 | ' 9' |
| R(2,0) | '9' | 0 | ' 9' |
| R(0,2) | '4' | 1 | ' 4' |
| J(0,2)-U | '4' | 1 | ' 4' |
| J(0,2)-RU | '4' | 1 | ' 4' |

### P2-L0-0083 (greek): bridge theta (O) → alpha (S), token 34

**lookup** (PP-L0-0083): O's answer 1, S's answer 4

O, as read:

```
<|im_start|>user
The locker of alpha is four. Jack picked beta. Eve picked alpha. The locker of beta is five. The locker of theta is one. Hugo picked⟦ theta⟧.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '1' | 0 | ' 1' |
| J(0,0.5) | '1' | 0 | ' 1' |
| J(0,1) | '4' | 1 | ' 4' |
| J(0,1.5) | '4' | 1 | ' 4' |
| J(0,2) | '4' | 1 | ' 4' |
| J(0.5,0) | '1' | 0 | ' 1' |
| J(0.5,0.5) | '1' | 0 | ' 1' |
| J(0.5,1) | '4' | 1 | ' 4' |
| J(0.5,1.5) | '4' | 1 | ' 4' |
| J(0.5,2) | '4' | 1 | ' 4' |
| J(1,0) | '1' | 0 | ' 1' |
| J(1,0.5) | '4' | 1 | ' 4' |
| J(1,1) | '4' | 1 | ' 4' |
| J(1,1.5) | '4' | 1 | ' 4' |
| J(1,2) | '4' | 1 | ' 4' |
| J(1.5,0) | '1' | 0 | ' 1' |
| J(1.5,0.5) | '4' | 1 | ' 4' |
| J(1.5,1) | '4' | 1 | ' 4' |
| J(1.5,1.5) | '4' | 1 | ' 4' |
| J(1.5,2) | '4' | 1 | ' 4' |
| J(2,0) | '1' | 0 | ' 1' |
| J(2,0.5) | '4' | 1 | ' 4' |
| J(2,1) | '4' | 1 | ' 4' |
| J(2,1.5) | '4' | 1 | ' 4' |
| J(2,2) | '4' | 1 | ' 4' |
| R(0,1) | '4' | 1 | ' 4' |
| R(1,0) | '1' | 0 | ' 1' |
| R(2,0) | '1' | 0 | ' 1' |
| R(0,2) | '4' | 1 | ' 4' |
| J(0,2)-U | '4' | 1 | ' 4' |
| J(0,2)-RU | '4' | 1 | ' 4' |

**recall** (PM-L0-0083): O's answer 8, S's answer 1

O, as read:

```
<|im_start|>user
The locker of alpha is four. Jack picked beta. Eve picked alpha. The locker of beta is five. The locker of theta is one. Hugo picked⟦ theta⟧.
Which position in the Greek alphabet does Hugo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '8' | 0 | ' 8' |
| J(0,0.5) | '8' | 0 | ' 8' |
| J(0,1) | '1' | 1 | ' 1' |
| J(0,1.5) | '1' | 1 | ' 1' |
| J(0,2) | '1' | 1 | ' 1' |
| J(0.5,0) | '8' | 0 | ' 8' |
| J(0.5,0.5) | '8' | 0 | ' 8' |
| J(0.5,1) | '1' | 1 | ' 1' |
| J(0.5,1.5) | '1' | 1 | ' 1' |
| J(0.5,2) | '1' | 1 | ' 1' |
| J(1,0) | '8' | 0 | ' 8' |
| J(1,0.5) | '1' | 1 | ' 1' |
| J(1,1) | '1' | 1 | ' 1' |
| J(1,1.5) | '1' | 1 | ' 1' |
| J(1,2) | '1' | 1 | ' 1' |
| J(1.5,0) | '8' | 0 | ' 8' |
| J(1.5,0.5) | '1' | 1 | ' 1' |
| J(1.5,1) | '1' | 1 | ' 1' |
| J(1.5,1.5) | '1' | 1 | ' 1' |
| J(1.5,2) | '1' | 1 | ' 1' |
| J(2,0) | '1' | 1 | ' 1' |
| J(2,0.5) | '1' | 1 | ' 1' |
| J(2,1) | '1' | 1 | ' 1' |
| J(2,1.5) | '1' | 1 | ' 1' |
| J(2,2) | '1' | 1 | ' 1' |
| R(0,1) | '1' | 1 | ' 1' |
| R(1,0) | '8' | 0 | ' 8' |
| R(2,0) | '8' | 0 | ' 8' |
| R(0,2) | '1' | 1 | ' 1' |
| J(0,2)-U | '1' | 1 | ' 1' |
| J(0,2)-RU | '4' | 0 | ' 4' |

### P2-L0-0096 (animals): bridge bee (O) → spider (S), token 43

**lookup** (PP-L0-0096): O's answer 1, S's answer 5

O, as read:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '1' | 0 | ' 1' |
| J(0,0.5) | '1' | 0 | ' 1' |
| J(0,1) | '5' | 1 | ' 5' |
| J(0,1.5) | '5' | 1 | ' 5' |
| J(0,2) | '5' | 1 | ' 5' |
| J(0.5,0) | '1' | 0 | ' 1' |
| J(0.5,0.5) | '1' | 0 | ' 1' |
| J(0.5,1) | '5' | 1 | ' 5' |
| J(0.5,1.5) | '5' | 1 | ' 5' |
| J(0.5,2) | '5' | 1 | ' 5' |
| J(1,0) | '1' | 0 | ' 1' |
| J(1,0.5) | '5' | 1 | ' 5' |
| J(1,1) | '5' | 1 | ' 5' |
| J(1,1.5) | '5' | 1 | ' 5' |
| J(1,2) | '5' | 1 | ' 5' |
| J(1.5,0) | '1' | 0 | ' 1' |
| J(1.5,0.5) | '5' | 1 | ' 5' |
| J(1.5,1) | '5' | 1 | ' 5' |
| J(1.5,1.5) | '5' | 1 | ' 5' |
| J(1.5,2) | '5' | 1 | ' 5' |
| J(2,0) | '1' | 0 | ' 1' |
| J(2,0.5) | '5' | 1 | ' 5' |
| J(2,1) | '5' | 1 | ' 5' |
| J(2,1.5) | '5' | 1 | ' 5' |
| J(2,2) | '5' | 1 | ' 5' |
| R(0,1) | '5' | 1 | ' 5' |
| R(1,0) | '1' | 0 | ' 1' |
| R(2,0) | '1' | 0 | ' 1' |
| R(0,2) | '5' | 1 | ' 5' |
| J(0,2)-U | '1' | 0 | ' 1' |
| J(0,2)-RU | '5' | 1 | ' 5' |

**recall** (PM-L0-0096): O's answer 6, S's answer 8

O, as read:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6' |
| J(0,0.5) | '6' | 0 | ' 6' |
| J(0,1) | '6' | 0 | ' 8' |
| J(0,1.5) | '6' | 0 | ' 8' |
| J(0,2) | '6' | 0 | ' 6' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '6' | 0 | ' 6' |
| J(0.5,1) | '8' | 1 | ' 8' |
| J(0.5,1.5) | '8' | 1 | ' 8' |
| J(0.5,2) | '6' | 0 | ' 8' |
| J(1,0) | '6' | 0 | ' 6' |
| J(1,0.5) | '8' | 1 | ' 8' |
| J(1,1) | '8' | 1 | ' 8' |
| J(1,1.5) | '8' | 1 | ' 8' |
| J(1,2) | '8' | 1 | ' 8' |
| J(1.5,0) | '6' | 0 | ' 6' |
| J(1.5,0.5) | '8' | 1 | ' 8' |
| J(1.5,1) | '8' | 1 | ' 8' |
| J(1.5,1.5) | '8' | 1 | ' 8' |
| J(1.5,2) | '8' | 1 | ' 8' |
| J(2,0) | '6' | 0 | ' 6' |
| J(2,0.5) | '8' | 1 | ' 8' |
| J(2,1) | '8' | 1 | ' 8' |
| J(2,1.5) | '8' | 1 | ' 8' |
| J(2,2) | '8' | 1 | ' 8' |
| R(0,1) | '8' | 1 | ' 8' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '6' | 0 | ' 6' |
| R(0,2) | '8' | 1 | ' 8' |
| J(0,2)-U | '6' | 0 | ' 6' |
| J(0,2)-RU | '6' | 0 | ' 6' |

### P2-L0-0135 (animals): bridge goose (O) → beetle (S), token 43

**lookup** (PP-L0-0135): O's answer 7, S's answer 4

O, as read:

```
<|im_start|>user
Ryan picked the beetle. Olivia picked the camel. The locker of the beetle is 4. The locker of the goose is 7. The locker of the camel is 5. Frank picked the⟦ goose⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '7' | 0 | ' 7' |
| J(0,0.5) | '7' | 0 | ' 7' |
| J(0,1) | '4' | 1 | ' 4' |
| J(0,1.5) | '4' | 1 | ' 4' |
| J(0,2) | '4' | 1 | ' 4' |
| J(0.5,0) | '7' | 0 | ' 7' |
| J(0.5,0.5) | '7' | 0 | ' 7' |
| J(0.5,1) | '4' | 1 | ' 4' |
| J(0.5,1.5) | '4' | 1 | ' 4' |
| J(0.5,2) | '4' | 1 | ' 4' |
| J(1,0) | '7' | 0 | ' 7' |
| J(1,0.5) | '7' | 0 | ' 7' |
| J(1,1) | '4' | 1 | ' 4' |
| J(1,1.5) | '4' | 1 | ' 4' |
| J(1,2) | '4' | 1 | ' 4' |
| J(1.5,0) | '7' | 0 | ' 7' |
| J(1.5,0.5) | '4' | 1 | ' 4' |
| J(1.5,1) | '4' | 1 | ' 4' |
| J(1.5,1.5) | '4' | 1 | ' 4' |
| J(1.5,2) | '4' | 1 | ' 4' |
| J(2,0) | '7' | 0 | ' 7' |
| J(2,0.5) | '4' | 1 | ' 4' |
| J(2,1) | '4' | 1 | ' 4' |
| J(2,1.5) | '4' | 1 | ' 4' |
| J(2,2) | '4' | 1 | ' 4' |
| R(0,1) | '7' | 0 | ' 7' |
| R(1,0) | '7' | 0 | ' 7' |
| R(2,0) | '7' | 0 | ' 7' |
| R(0,2) | '4' | 1 | ' 4' |
| J(0,2)-U | '5' | 0 | ' 5' |
| J(0,2)-RU | '4' | 1 | ' 4' |

**recall** (PM-L0-0135): O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
Ryan picked the beetle. Olivia picked the camel. The locker of the beetle is 4. The locker of the goose is 7. The locker of the camel is 5. Frank picked the⟦ goose⟧.
How many legs does Frank's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2' |
| J(0,0.5) | '2' | 0 | ' 2' |
| J(0,1) | '6' | 1 | ' 6' |
| J(0,1.5) | '6' | 1 | ' 6' |
| J(0,2) | '6' | 1 | ' 6' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '2' | 0 | ' 2' |
| J(0.5,1) | '6' | 1 | ' 6' |
| J(0.5,1.5) | '6' | 1 | ' 6' |
| J(0.5,2) | '6' | 1 | ' 6' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '6' | 1 | ' 6' |
| J(1,1) | '6' | 1 | ' 6' |
| J(1,1.5) | '6' | 1 | ' 6' |
| J(1,2) | '6' | 1 | ' 6' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '6' | 1 | ' 6' |
| J(1.5,1) | '6' | 1 | ' 6' |
| J(1.5,1.5) | '6' | 1 | ' 6' |
| J(1.5,2) | '6' | 1 | ' 6' |
| J(2,0) | '2' | 0 | ' 2' |
| J(2,0.5) | '6' | 1 | ' 6' |
| J(2,1) | '6' | 1 | ' 6' |
| J(2,1.5) | '6' | 1 | ' 6' |
| J(2,2) | '6' | 1 | ' 6' |
| R(0,1) | '6' | 1 | ' 6' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '6' | 1 | ' 6' |
| R(0,2) | '6' | 1 | ' 6' |
| J(0,2)-U | '6' | 1 | ' 6' |
| J(0,2)-RU | '6' | 1 | ' 6' |

### P2-L0-0139 (elements): bridge oxygen (O) → nitrogen (S), token 38

**lookup** (PP-L0-0139): O's answer 6, S's answer 9

O, as read:

```
<|im_start|>user
Hugo picked nitrogen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked⟦ oxygen⟧.
Which locker belongs to Ruby's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6' |
| J(0,0.5) | '9' | 1 | ' 6' |
| J(0,1) | '9' | 1 | ' 9' |
| J(0,1.5) | '9' | 1 | ' 9' |
| J(0,2) | '9' | 1 | ' 9' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '9' | 1 | ' 9' |
| J(0.5,1) | '9' | 1 | ' 9' |
| J(0.5,1.5) | '9' | 1 | ' 9' |
| J(0.5,2) | '9' | 1 | ' 9' |
| J(1,0) | '6' | 0 | ' 6' |
| J(1,0.5) | '9' | 1 | ' 9' |
| J(1,1) | '9' | 1 | ' 9' |
| J(1,1.5) | '9' | 1 | ' 9' |
| J(1,2) | '9' | 1 | ' 9' |
| J(1.5,0) | '6' | 0 | ' 6' |
| J(1.5,0.5) | '9' | 1 | ' 9' |
| J(1.5,1) | '9' | 1 | ' 9' |
| J(1.5,1.5) | '9' | 1 | ' 9' |
| J(1.5,2) | '9' | 1 | ' 9' |
| J(2,0) | '9' | 1 | ' 9' |
| J(2,0.5) | '9' | 1 | ' 9' |
| J(2,1) | '9' | 1 | ' 9' |
| J(2,1.5) | '9' | 1 | ' 9' |
| J(2,2) | '9' | 1 | ' 9' |
| R(0,1) | '9' | 1 | ' 9' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '9' | 1 | ' 6' |
| R(0,2) | '9' | 1 | ' 9' |
| J(0,2)-U | '9' | 1 | ' 9' |
| J(0,2)-RU | '9' | 1 | ' 9' |

**recall** (PM-L0-0139): O's answer 8, S's answer 7

O, as read:

```
<|im_start|>user
Hugo picked nitrogen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked⟦ oxygen⟧.
What is the atomic number of Ruby's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '8' | 0 | ' 8' |
| J(0,0.5) | '8' | 0 | ' 8' |
| J(0,1) | '7' | 1 | ' 7' |
| J(0,1.5) | '7' | 1 | ' 7' |
| J(0,2) | '7' | 1 | ' 7' |
| J(0.5,0) | '8' | 0 | ' 8' |
| J(0.5,0.5) | '7' | 1 | ' 7' |
| J(0.5,1) | '7' | 1 | ' 7' |
| J(0.5,1.5) | '7' | 1 | ' 7' |
| J(0.5,2) | '7' | 1 | ' 7' |
| J(1,0) | '8' | 0 | ' 7' |
| J(1,0.5) | '7' | 1 | ' 7' |
| J(1,1) | '7' | 1 | ' 7' |
| J(1,1.5) | '7' | 1 | ' 7' |
| J(1,2) | '7' | 1 | ' 7' |
| J(1.5,0) | '7' | 1 | ' 7' |
| J(1.5,0.5) | '7' | 1 | ' 7' |
| J(1.5,1) | '7' | 1 | ' 7' |
| J(1.5,1.5) | '7' | 1 | ' 7' |
| J(1.5,2) | '7' | 1 | ' 7' |
| J(2,0) | '7' | 1 | ' 7' |
| J(2,0.5) | '7' | 1 | ' 7' |
| J(2,1) | '7' | 1 | ' 7' |
| J(2,1.5) | '7' | 1 | ' 7' |
| J(2,2) | '7' | 1 | ' 7' |
| R(0,1) | '7' | 1 | ' 7' |
| R(1,0) | '8' | 0 | ' 8' |
| R(2,0) | '7' | 1 | ' 7' |
| R(0,2) | '7' | 1 | ' 7' |
| J(0,2)-U | '7' | 1 | ' 7' |
| J(0,2)-RU | '7' | 1 | ' 7' |

### P2-L0-0149 (greek): bridge delta (O) → iota (S), token 29

**lookup** (PP-L0-0149): O's answer 1, S's answer 8

O, as read:

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦ delta⟧. Kate picked gamma. Luke picked iota.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '1' | 0 | ' 1' |
| J(0,0.5) | '1' | 0 | ' 1' |
| J(0,1) | '8' | 1 | ' 8' |
| J(0,1.5) | '8' | 1 | ' 8' |
| J(0,2) | '8' | 1 | ' 8' |
| J(0.5,0) | '1' | 0 | ' 1' |
| J(0.5,0.5) | '1' | 0 | ' 1' |
| J(0.5,1) | '8' | 1 | ' 8' |
| J(0.5,1.5) | '8' | 1 | ' 8' |
| J(0.5,2) | '8' | 1 | ' 8' |
| J(1,0) | '1' | 0 | ' 1' |
| J(1,0.5) | '1' | 0 | ' 1' |
| J(1,1) | '8' | 1 | ' 8' |
| J(1,1.5) | '8' | 1 | ' 8' |
| J(1,2) | '8' | 1 | ' 8' |
| J(1.5,0) | '1' | 0 | ' 1' |
| J(1.5,0.5) | '8' | 1 | ' 8' |
| J(1.5,1) | '8' | 1 | ' 8' |
| J(1.5,1.5) | '8' | 1 | ' 8' |
| J(1.5,2) | '8' | 1 | ' 8' |
| J(2,0) | '1' | 0 | ' 1' |
| J(2,0.5) | '8' | 1 | ' 8' |
| J(2,1) | '8' | 1 | ' 8' |
| J(2,1.5) | '8' | 1 | ' 8' |
| J(2,2) | '8' | 1 | ' 8' |
| R(0,1) | '8' | 1 | ' 8' |
| R(1,0) | '1' | 0 | ' 1' |
| R(2,0) | '1' | 0 | ' 1' |
| R(0,2) | '8' | 1 | ' 8' |
| J(0,2)-U | '1' | 0 | ' 1' |
| J(0,2)-RU | '8' | 1 | ' 8' |

**recall** (PM-L0-0149): O's answer 4, S's answer 9

O, as read:

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦ delta⟧. Kate picked gamma. Luke picked iota.
Which position in the Greek alphabet does Lucy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '4' | 0 | ' 4' |
| J(0,1) | '9' | 1 | ' 9' |
| J(0,1.5) | '9' | 1 | ' 9' |
| J(0,2) | '9' | 1 | ' 9' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '4' | 0 | ' 4' |
| J(0.5,1) | '9' | 1 | ' 9' |
| J(0.5,1.5) | '9' | 1 | ' 9' |
| J(0.5,2) | '9' | 1 | ' 9' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '9' | 1 | ' 9' |
| J(1,1) | '9' | 1 | ' 9' |
| J(1,1.5) | '9' | 1 | ' 9' |
| J(1,2) | '9' | 1 | ' 9' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '9' | 1 | ' 9' |
| J(1.5,1) | '9' | 1 | ' 9' |
| J(1.5,1.5) | '9' | 1 | ' 9' |
| J(1.5,2) | '9' | 1 | ' 9' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '9' | 1 | ' 9' |
| J(2,1) | '9' | 1 | ' 9' |
| J(2,1.5) | '9' | 1 | ' 9' |
| J(2,2) | '9' | 1 | ' 9' |
| R(0,1) | '9' | 1 | ' 9' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '4' | 0 | ' 4' |
| R(0,2) | '9' | 1 | ' 9' |
| J(0,2)-U | '9' | 1 | ' 9' |
| J(0,2)-RU | '9' | 1 | ' 9' |

### P2-L0-0181 (elements): bridge helium (O) → nitrogen (S), token 37

**lookup** (PP-L0-0181): O's answer 3, S's answer 9

O, as read:

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ helium⟧.
Which locker belongs to Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3' |
| J(0,0.5) | '3' | 0 | ' 3' |
| J(0,1) | '9' | 1 | ' 9' |
| J(0,1.5) | '9' | 1 | ' 9' |
| J(0,2) | '9' | 1 | ' 9' |
| J(0.5,0) | '3' | 0 | ' 3' |
| J(0.5,0.5) | '3' | 0 | ' 3' |
| J(0.5,1) | '9' | 1 | ' 9' |
| J(0.5,1.5) | '9' | 1 | ' 9' |
| J(0.5,2) | '9' | 1 | ' 9' |
| J(1,0) | '3' | 0 | ' 3' |
| J(1,0.5) | '9' | 1 | ' 9' |
| J(1,1) | '9' | 1 | ' 9' |
| J(1,1.5) | '9' | 1 | ' 9' |
| J(1,2) | '9' | 1 | ' 9' |
| J(1.5,0) | '3' | 0 | ' 3' |
| J(1.5,0.5) | '9' | 1 | ' 9' |
| J(1.5,1) | '9' | 1 | ' 9' |
| J(1.5,1.5) | '9' | 1 | ' 9' |
| J(1.5,2) | '9' | 1 | ' 9' |
| J(2,0) | '3' | 0 | ' 3' |
| J(2,0.5) | '9' | 1 | ' 9' |
| J(2,1) | '9' | 1 | ' 9' |
| J(2,1.5) | '9' | 1 | ' 9' |
| J(2,2) | '9' | 1 | ' 9' |
| R(0,1) | '9' | 1 | ' 9' |
| R(1,0) | '3' | 0 | ' 3' |
| R(2,0) | '3' | 0 | ' 3' |
| R(0,2) | '9' | 1 | ' 9' |
| J(0,2)-U | '9' | 1 | ' 9' |
| J(0,2)-RU | '9' | 1 | ' 9' |

**recall** (PM-L0-0181): O's answer 2, S's answer 7

O, as read:

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ helium⟧.
What is the atomic number of Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2' |
| J(0,0.5) | '2' | 0 | ' 2' |
| J(0,1) | '7' | 1 | ' 7' |
| J(0,1.5) | '7' | 1 | ' 7' |
| J(0,2) | '7' | 1 | ' 7' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '7' | 1 | ' 2' |
| J(0.5,1) | '7' | 1 | ' 7' |
| J(0.5,1.5) | '7' | 1 | ' 7' |
| J(0.5,2) | '7' | 1 | ' 7' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '7' | 1 | ' 7' |
| J(1,1) | '7' | 1 | ' 7' |
| J(1,1.5) | '7' | 1 | ' 7' |
| J(1,2) | '7' | 1 | ' 7' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '7' | 1 | ' 7' |
| J(1.5,1) | '7' | 1 | ' 7' |
| J(1.5,1.5) | '7' | 1 | ' 7' |
| J(1.5,2) | '7' | 1 | ' 7' |
| J(2,0) | '7' | 1 | ' 7' |
| J(2,0.5) | '7' | 1 | ' 7' |
| J(2,1) | '7' | 1 | ' 7' |
| J(2,1.5) | '7' | 1 | ' 7' |
| J(2,2) | '7' | 1 | ' 7' |
| R(0,1) | '7' | 1 | ' 7' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '2' | 0 | ' 2' |
| R(0,2) | '7' | 1 | ' 7' |
| J(0,2)-U | '7' | 1 | ' 7' |
| J(0,2)-RU | '7' | 1 | ' 7' |

### P2-L0-0206 (greek): bridge eta (O) → delta (S), token 38

**lookup** (PP-L0-0206): O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
Iris picked alpha. The locker of delta is 6. The locker of eta is 2. The locker of alpha is 9. Eva picked delta. Liam picked⟦ eta⟧.
Which locker belongs to Liam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2' |
| J(0,0.5) | '2' | 0 | ' 2' |
| J(0,1) | '6' | 1 | ' 6' |
| J(0,1.5) | '6' | 1 | ' 6' |
| J(0,2) | '6' | 1 | ' 6' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '2' | 0 | ' 2' |
| J(0.5,1) | '6' | 1 | ' 6' |
| J(0.5,1.5) | '6' | 1 | ' 6' |
| J(0.5,2) | '6' | 1 | ' 6' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '6' | 1 | ' 6' |
| J(1,1) | '6' | 1 | ' 6' |
| J(1,1.5) | '6' | 1 | ' 6' |
| J(1,2) | '6' | 1 | ' 6' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '6' | 1 | ' 6' |
| J(1.5,1) | '6' | 1 | ' 6' |
| J(1.5,1.5) | '6' | 1 | ' 6' |
| J(1.5,2) | '6' | 1 | ' 6' |
| J(2,0) | '2' | 0 | ' 2' |
| J(2,0.5) | '6' | 1 | ' 6' |
| J(2,1) | '6' | 1 | ' 6' |
| J(2,1.5) | '6' | 1 | ' 6' |
| J(2,2) | '6' | 1 | ' 6' |
| R(0,1) | '6' | 1 | ' 6' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '6' | 1 | ' 2' |
| R(0,2) | '6' | 1 | ' 6' |
| J(0,2)-U | '6' | 1 | ' 6' |
| J(0,2)-RU | '6' | 1 | ' 6' |

**recall** (PM-L0-0206): O's answer 7, S's answer 4

O, as read:

```
<|im_start|>user
Iris picked alpha. The locker of delta is 6. The locker of eta is 2. The locker of alpha is 9. Eva picked delta. Liam picked⟦ eta⟧.
Which position in the Greek alphabet does Liam's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '7' | 0 | ' 7' |
| J(0,0.5) | '7' | 0 | ' 8' |
| J(0,1) | '4' | 1 | ' 4' |
| J(0,1.5) | '4' | 1 | ' 4' |
| J(0,2) | '4' | 1 | ' 4' |
| J(0.5,0) | '7' | 0 | ' 7' |
| J(0.5,0.5) | '5' | 0 | ' 5' |
| J(0.5,1) | '4' | 1 | ' 4' |
| J(0.5,1.5) | '4' | 1 | ' 4' |
| J(0.5,2) | '4' | 1 | ' 4' |
| J(1,0) | '7' | 0 | ' 7' |
| J(1,0.5) | '4' | 1 | ' 4' |
| J(1,1) | '4' | 1 | ' 4' |
| J(1,1.5) | '4' | 1 | ' 4' |
| J(1,2) | '4' | 1 | ' 4' |
| J(1.5,0) | '5' | 0 | ' 5' |
| J(1.5,0.5) | '4' | 1 | ' 4' |
| J(1.5,1) | '4' | 1 | ' 4' |
| J(1.5,1.5) | '4' | 1 | ' 4' |
| J(1.5,2) | '4' | 1 | ' 4' |
| J(2,0) | '4' | 1 | ' 4' |
| J(2,0.5) | '4' | 1 | ' 4' |
| J(2,1) | '4' | 1 | ' 4' |
| J(2,1.5) | '4' | 1 | ' 4' |
| J(2,2) | '4' | 1 | ' 4' |
| R(0,1) | '4' | 1 | ' 4' |
| R(1,0) | '8' | 0 | ' 7' |
| R(2,0) | '5' | 0 | ' 5' |
| R(0,2) | '4' | 1 | ' 4' |
| J(0,2)-U | '4' | 1 | ' 4' |
| J(0,2)-RU | '4' | 1 | ' 4' |

### P2-L0-0207 (animals): bridge rabbit (O) → owl (S), token 43

**lookup** (PP-L0-0207): O's answer 9, S's answer 8

O, as read:

```
<|im_start|>user
The locker of the rabbit is 9. The locker of the owl is 8. The locker of the sheep is 2. Anna picked the sheep. Jack picked the owl. Eva picked the⟦ rabbit⟧.
Which locker belongs to Eva's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '9' | 0 | ' 9' |
| J(0,0.5) | '9' | 0 | ' 9' |
| J(0,1) | '8' | 1 | ' 8' |
| J(0,1.5) | '8' | 1 | ' 8' |
| J(0,2) | '8' | 1 | ' 8' |
| J(0.5,0) | '9' | 0 | ' 9' |
| J(0.5,0.5) | '9' | 0 | ' 9' |
| J(0.5,1) | '8' | 1 | ' 8' |
| J(0.5,1.5) | '8' | 1 | ' 8' |
| J(0.5,2) | '8' | 1 | ' 8' |
| J(1,0) | '9' | 0 | ' 9' |
| J(1,0.5) | '9' | 0 | ' 9' |
| J(1,1) | '8' | 1 | ' 8' |
| J(1,1.5) | '8' | 1 | ' 8' |
| J(1,2) | '8' | 1 | ' 8' |
| J(1.5,0) | '9' | 0 | ' 9' |
| J(1.5,0.5) | '9' | 0 | ' 9' |
| J(1.5,1) | '8' | 1 | ' 8' |
| J(1.5,1.5) | '8' | 1 | ' 8' |
| J(1.5,2) | '8' | 1 | ' 8' |
| J(2,0) | '9' | 0 | ' 9' |
| J(2,0.5) | '9' | 0 | ' 9' |
| J(2,1) | '8' | 1 | ' 8' |
| J(2,1.5) | '8' | 1 | ' 8' |
| J(2,2) | '8' | 1 | ' 8' |
| R(0,1) | '8' | 1 | ' 8' |
| R(1,0) | '9' | 0 | ' 9' |
| R(2,0) | '9' | 0 | ' 9' |
| R(0,2) | '8' | 1 | ' 8' |
| J(0,2)-U | '9' | 0 | ' 9' |
| J(0,2)-RU | '8' | 1 | ' 8' |

**recall** (PM-L0-0207): O's answer 4, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the rabbit is 9. The locker of the owl is 8. The locker of the sheep is 2. Anna picked the sheep. Jack picked the owl. Eva picked the⟦ rabbit⟧.
How many legs does Eva's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '4' | 0 | ' 4' |
| J(0,1) | '2' | 1 | ' 2' |
| J(0,1.5) | '2' | 1 | ' 2' |
| J(0,2) | '2' | 1 | ' 2' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '4' | 0 | ' 4' |
| J(0.5,1) | '2' | 1 | ' 2' |
| J(0.5,1.5) | '2' | 1 | ' 2' |
| J(0.5,2) | '2' | 1 | ' 2' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '4' | 0 | ' 2' |
| J(1,1) | '2' | 1 | ' 2' |
| J(1,1.5) | '2' | 1 | ' 2' |
| J(1,2) | '2' | 1 | ' 2' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '2' | 1 | ' 4' |
| J(1.5,1) | '2' | 1 | ' 2' |
| J(1.5,1.5) | '2' | 1 | ' 2' |
| J(1.5,2) | '2' | 1 | ' 2' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '2' | 1 | ' 2' |
| J(2,1) | '2' | 1 | ' 2' |
| J(2,1.5) | '2' | 1 | ' 2' |
| J(2,2) | '2' | 1 | ' 2' |
| R(0,1) | '2' | 1 | ' 2' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '4' | 0 | ' 4' |
| R(0,2) | '2' | 1 | ' 2' |
| J(0,2)-U | '4' | 0 | ' 4' |
| J(0,2)-RU | '2' | 1 | ' 2' |

### P2-L0-0296 (greek): bridge epsilon (O) → alpha (S), token 30

**lookup** (PP-L0-0296): O's answer 7, S's answer 9

O, as read:

```
<|im_start|>user
The locker of iota is four. The locker of alpha is nine. Mia picked iota. The locker of epsilon is seven. Vera picked⟦ epsilon⟧. Tara picked alpha.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '7' | 0 | ' 7' |
| J(0,0.5) | '7' | 0 | ' 7' |
| J(0,1) | '9' | 1 | ' 9' |
| J(0,1.5) | '9' | 1 | ' 9' |
| J(0,2) | '9' | 1 | ' 9' |
| J(0.5,0) | '7' | 0 | ' 7' |
| J(0.5,0.5) | '7' | 0 | ' 7' |
| J(0.5,1) | '9' | 1 | ' 9' |
| J(0.5,1.5) | '9' | 1 | ' 9' |
| J(0.5,2) | '9' | 1 | ' 9' |
| J(1,0) | '7' | 0 | ' 7' |
| J(1,0.5) | '9' | 1 | ' 9' |
| J(1,1) | '9' | 1 | ' 9' |
| J(1,1.5) | '9' | 1 | ' 9' |
| J(1,2) | '9' | 1 | ' 9' |
| J(1.5,0) | '7' | 0 | ' 7' |
| J(1.5,0.5) | '9' | 1 | ' 9' |
| J(1.5,1) | '9' | 1 | ' 9' |
| J(1.5,1.5) | '9' | 1 | ' 9' |
| J(1.5,2) | '9' | 1 | ' 9' |
| J(2,0) | '7' | 0 | ' 7' |
| J(2,0.5) | '9' | 1 | ' 9' |
| J(2,1) | '9' | 1 | ' 9' |
| J(2,1.5) | '9' | 1 | ' 9' |
| J(2,2) | '9' | 1 | ' 9' |
| R(0,1) | '9' | 1 | ' 9' |
| R(1,0) | '7' | 0 | ' 7' |
| R(2,0) | '7' | 0 | ' 7' |
| R(0,2) | '9' | 1 | ' 9' |
| J(0,2)-U | '9' | 1 | ' 9' |
| J(0,2)-RU | '9' | 1 | ' 9' |

**recall** (PM-L0-0296): O's answer 5, S's answer 1

O, as read:

```
<|im_start|>user
The locker of iota is four. The locker of alpha is nine. Mia picked iota. The locker of epsilon is seven. Vera picked⟦ epsilon⟧. Tara picked alpha.
Which position in the Greek alphabet does Vera's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '5' | 0 | ' 5' |
| J(0,0.5) | '5' | 0 | ' 5' |
| J(0,1) | '1' | 1 | ' 1' |
| J(0,1.5) | '1' | 1 | ' 1' |
| J(0,2) | '1' | 1 | ' 1' |
| J(0.5,0) | '5' | 0 | ' 5' |
| J(0.5,0.5) | '5' | 0 | ' 5' |
| J(0.5,1) | '1' | 1 | ' 1' |
| J(0.5,1.5) | '1' | 1 | ' 1' |
| J(0.5,2) | '1' | 1 | ' 1' |
| J(1,0) | '5' | 0 | ' 5' |
| J(1,0.5) | '5' | 0 | ' 5' |
| J(1,1) | '1' | 1 | ' 1' |
| J(1,1.5) | '1' | 1 | ' 1' |
| J(1,2) | '1' | 1 | ' 1' |
| J(1.5,0) | '5' | 0 | ' 5' |
| J(1.5,0.5) | '1' | 1 | ' 1' |
| J(1.5,1) | '1' | 1 | ' 1' |
| J(1.5,1.5) | '1' | 1 | ' 1' |
| J(1.5,2) | '1' | 1 | ' 1' |
| J(2,0) | '5' | 0 | ' 5' |
| J(2,0.5) | '1' | 1 | ' 1' |
| J(2,1) | '1' | 1 | ' 1' |
| J(2,1.5) | '1' | 1 | ' 1' |
| J(2,2) | '1' | 1 | ' 1' |
| R(0,1) | '1' | 1 | ' 1' |
| R(1,0) | '5' | 0 | ' 5' |
| R(2,0) | '5' | 0 | ' 5' |
| R(0,2) | '1' | 1 | ' 1' |
| J(0,2)-U | '1' | 1 | ' 1' |
| J(0,2)-RU | '5' | 0 | ' 5' |

