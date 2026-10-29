# 48.3 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word, ⟦write:…⟧ the written sentence's item and number tokens. UNVERIFIED.

## nem35l_x52_bind_below: 10 random written scenes of 71 (seed 0)

### P2-L0-0119 (main, greek): bridge eta picked by Diana; written: gamma (picked by Tom; locker 1, attribute 3)

**lookup** (PP-L0-0119): O's answer 8, the written item's 1

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Amy picked theta. Tom picked gamma. The locker of theta is 9. Diana picked ⟦bridge:eta⟧. The locker of eta is 8. The locker of ⟦write:gamma⟧ is ⟦write:1⟧.
Which locker belongs to Diana's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | ' 8' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | ' 8' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | ' 8' |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | ' 8' |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | ' 8' |

**recall** (PM-L0-0119): O's answer 7, the written item's 3

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Amy picked theta. Tom picked gamma. The locker of theta is 9. Diana picked ⟦bridge:eta⟧. The locker of eta is 8. The locker of ⟦write:gamma⟧ is ⟦write:1⟧.
Which position in the Greek alphabet does Diana's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | ' 7' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | ' 7' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | ' 7' |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | ' 7' |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | ' 7' |

### P2-L0-0020 (45m, greek): bridge gamma picked by Liam; written: epsilon (picked by Nina; locker 2, attribute 5)

**lookup** (PP-L0-0020): O's answer 9, the written item's 2

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of iota is five. Liam picked ⟦bridge:gamma⟧. The locker of eta is eight. The locker of gamma is nine. Nina picked epsilon. Luke picked iota. The locker of ⟦write:epsilon⟧ is ⟦write:two⟧.
Which locker belongs to Liam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '9' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '9' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '9' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | target | None |

**recall** (PM-L0-0020): O's answer 3, the written item's 5

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of iota is five. Liam picked ⟦bridge:gamma⟧. The locker of eta is eight. The locker of gamma is nine. Nina picked epsilon. Luke picked iota. The locker of ⟦write:epsilon⟧ is ⟦write:two⟧.
Which position in the Greek alphabet does Liam's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | None |

### P2-L0-0040 (45m, elements): bridge lithium picked by Ryan; written: carbon (picked by Emma; locker 5, attribute 6)

**lookup** (PP-L0-0040): O's answer 2, the written item's 5

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of helium is four. Ryan picked ⟦bridge:lithium⟧. The locker of nitrogen is one. The locker of lithium is two. Emma picked carbon. Vera picked helium. The locker of ⟦write:carbon⟧ is ⟦write:five⟧.
Which locker belongs to Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | ' 2' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | ' 2' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | ' 2' |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | ' 2' |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | ' 2' |

**recall** (PM-L0-0040): O's answer 3, the written item's 6

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of helium is four. Ryan picked ⟦bridge:lithium⟧. The locker of nitrogen is one. The locker of lithium is two. Emma picked carbon. Vera picked helium. The locker of ⟦write:carbon⟧ is ⟦write:five⟧.
What is the atomic number of Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | ' 3' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | ' 3' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | ' 3' |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | ' 3' |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | ' 3' |

### P2-L0-0119 (45m, greek): bridge eta picked by Diana; written: gamma (picked by Tom; locker 1, attribute 3)

**lookup** (PP-L0-0119): O's answer 8, the written item's 1

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Amy picked theta. Tom picked gamma. The locker of theta is 9. Diana picked ⟦bridge:eta⟧. The locker of delta is 7. The locker of eta is 8. The locker of ⟦write:gamma⟧ is ⟦write:1⟧.
Which locker belongs to Diana's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | ' 8' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | ' 8' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | ' 8' |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | ' 8' |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | ' 8' |

**recall** (PM-L0-0119): O's answer 7, the written item's 3

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Amy picked theta. Tom picked gamma. The locker of theta is 9. Diana picked ⟦bridge:eta⟧. The locker of delta is 7. The locker of eta is 8. The locker of ⟦write:gamma⟧ is ⟦write:1⟧.
Which position in the Greek alphabet does Diana's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | ' 7' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | ' 7' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | ' 7' |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | ' 7' |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | ' 7' |

### P2-L0-0266 (45m, greek): bridge gamma picked by Jack; written: eta (picked by Mia; locker 9, attribute 7)

**lookup** (PP-L0-0266): O's answer 2, the written item's 9

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Mia picked eta. The locker of delta is five. Jack picked ⟦bridge:gamma⟧. The locker of ⟦write:eta⟧ is ⟦write:nine⟧. The locker of gamma is two. The locker of zeta is eight. Henry picked delta.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | None |

**recall** (PM-L0-0266): O's answer 3, the written item's 7

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Mia picked eta. The locker of delta is five. Jack picked ⟦bridge:gamma⟧. The locker of ⟦write:eta⟧ is ⟦write:nine⟧. The locker of gamma is two. The locker of zeta is eight. Henry picked delta.
Which position in the Greek alphabet does Jack's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | None |

### P2-L0-0272 (45m, greek): bridge delta picked by Henry; written: epsilon (picked by Vera; locker 4, attribute 5)

**lookup** (PP-L0-0272): O's answer 1, the written item's 4

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Henry picked ⟦bridge:delta⟧. Vera picked epsilon. The locker of ⟦write:epsilon⟧ is ⟦write:four⟧. The locker of delta is one. Julia picked theta. The locker of theta is two. The locker of beta is nine.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | original | ' 1' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '1' | original | ' 1' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '1' | original | ' 1' |
| r1 | a random vector of the s = 1 write's norm, per token | '1' | original | ' 1' |
| r2 | a random vector of the s = 2 write's norm, per token | '1' | original | ' 1' |

**recall** (PM-L0-0272): O's answer 4, the written item's 5

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Henry picked ⟦bridge:delta⟧. Vera picked epsilon. The locker of ⟦write:epsilon⟧ is ⟦write:four⟧. The locker of delta is one. Julia picked theta. The locker of theta is two. The locker of beta is nine.
Which position in the Greek alphabet does Henry's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | original | ' 4' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | original | ' 4' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | original | ' 4' |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | original | ' 4' |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | original | ' 4' |

### P2-L0-0292 (45m, elements): bridge lithium picked by Vera; written: oxygen (picked by Ben; locker 4, attribute 8)

**lookup** (PP-L0-0292): O's answer 1, the written item's 4

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of nitrogen is five. Max picked nitrogen. Vera picked ⟦bridge:lithium⟧. Ben picked oxygen. The locker of lithium is one. The locker of boron is nine. The locker of ⟦write:oxygen⟧ is ⟦write:four⟧.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '1' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '1' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '1' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '1' | original | None |

**recall** (PM-L0-0292): O's answer 3, the written item's 8

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of nitrogen is five. Max picked nitrogen. Vera picked ⟦bridge:lithium⟧. Ben picked oxygen. The locker of lithium is one. The locker of boron is nine. The locker of ⟦write:oxygen⟧ is ⟦write:four⟧.
What is the atomic number of Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | None |

### P2-L0-0429 (45m, animals): bridge tick picked by Owen; written: crow (picked by Sean; locker 9, attribute 2)

**lookup** (PP-L0-0429): O's answer 3, the written item's 9

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Sean picked the crow. Owen picked the ⟦bridge:tick⟧. The locker of the owl is six. The locker of the ⟦write:crow⟧ is ⟦write:nine⟧. The locker of the tick is three. The locker of the fox is one. Will picked the owl.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | None |

**recall** (PM-L0-0429): O's answer 8, the written item's 2

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Sean picked the crow. Owen picked the ⟦bridge:tick⟧. The locker of the owl is six. The locker of the ⟦write:crow⟧ is ⟦write:nine⟧. The locker of the tick is three. The locker of the fox is one. Will picked the owl.
How many legs does Owen's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | None |

### P2-L0-0446 (45m, greek): bridge delta picked by Carl; written: alpha (picked by Sean; locker 9, attribute 1)

**lookup** (PP-L0-0446): O's answer 2, the written item's 9

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of epsilon is 7. Sean picked alpha. Carl picked ⟦bridge:delta⟧. The locker of delta is 2. Oscar picked epsilon. The locker of eta is 8. The locker of ⟦write:alpha⟧ is ⟦write:9⟧.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | None |

**recall** (PM-L0-0446): O's answer 4, the written item's 1

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of epsilon is 7. Sean picked alpha. Carl picked ⟦bridge:delta⟧. The locker of delta is 2. Oscar picked epsilon. The locker of eta is 8. The locker of ⟦write:alpha⟧ is ⟦write:9⟧.
Which position in the Greek alphabet does Carl's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | original | None |

### P2-L0-0495 (45m, animals): bridge deer picked by Leo; written: bee (picked by Sara; locker 2, attribute 6)

**lookup** (PP-L0-0495): O's answer 3, the written item's 2

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Leo picked the ⟦bridge:deer⟧. Eve picked the beetle. Sara picked the bee. The locker of the ⟦write:bee⟧ is ⟦write:2⟧. The locker of the turkey is 6. The locker of the deer is 3. The locker of the beetle is 4.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
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
<|im_start|>system
<|im_end|>
<|im_start|>user
Leo picked the ⟦bridge:deer⟧. Eve picked the beetle. Sara picked the bee. The locker of the ⟦write:bee⟧ is ⟦write:2⟧. The locker of the turkey is 6. The locker of the deer is 3. The locker of the beetle is 4.
How many legs does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | original | None |

