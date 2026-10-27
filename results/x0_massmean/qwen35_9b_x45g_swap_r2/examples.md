# Examples: qwen35_9b_x45g_swap_r2 (mode two_routes)

10 random items (seed 0) of 200; the prompt as the model reads it (the chat read appends a space), ⟦the bridge word⟧ where the change is added at layer 12; each arm's answer = the top token at the read step. UNVERIFIED.

## P2-L0-0017 (bridge iota -> delta; its locker sentence before the pick)

**lookup** (original 2, changed 6)

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), other |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 9, changed 4)

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), original answer |

## P2-L0-0096 (bridge bee -> spider; its locker sentence before the pick)

**lookup** (original 1, changed 5)

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

**recall** (original 6, changed 8)

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), original answer |

## P2-L0-0110 (bridge iota -> epsilon; its locker sentence before the pick)

**lookup** (original 2, changed 7)

```
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked⟦ iota⟧.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 9, changed 5)

```
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked⟦ iota⟧.
Which position in the Greek alphabet does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), original answer |

## P2-L0-0142 (bridge nitrogen -> oxygen; its locker sentence after the pick)

**lookup** (original 3, changed 6)

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ nitrogen⟧. The locker of nitrogen is three.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 7, changed 8)

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ nitrogen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0149 (bridge delta -> iota; its locker sentence before the pick)

**lookup** (original 1, changed 8)

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦ delta⟧. Kate picked gamma. Luke picked iota.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

**recall** (original 4, changed 9)

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦ delta⟧. Kate picked gamma. Luke picked iota.
Which position in the Greek alphabet does Lucy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0154 (bridge oxygen -> helium; its locker sentence after the pick)

**lookup** (original 5, changed 3)

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ oxygen⟧. Max picked helium. The locker of oxygen is five.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 8, changed 2)

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ oxygen⟧. Max picked helium. The locker of oxygen is five.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0181 (bridge helium -> nitrogen; its locker sentence before the pick)

**lookup** (original 3, changed 9)

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ helium⟧.
Which locker belongs to Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), changed answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

**recall** (original 2, changed 7)

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ helium⟧.
What is the atomic number of Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0184 (bridge helium -> hydrogen; its locker sentence before the pick)

**lookup** (original 9, changed 5)

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked⟦ helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), other |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), other |
| without a random part (J++'s share) | (not stored), other |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), other |

**recall** (original 2, changed 1)

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked⟦ helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0193 (bridge hydrogen -> helium; its locker sentence after the pick)

**lookup** (original 8, changed 3)

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. Victor picked⟦ hydrogen⟧. The locker of hydrogen is eight.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 1, changed 2)

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. Victor picked⟦ hydrogen⟧. The locker of hydrogen is eight.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), changed answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0290 (bridge epsilon -> iota; its locker sentence before the pick)

**lookup** (original 4, changed 8)

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ epsilon⟧. Noah picked beta.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 5, changed 9)

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ epsilon⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

