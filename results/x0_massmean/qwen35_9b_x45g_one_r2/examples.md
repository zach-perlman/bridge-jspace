# Examples: qwen35_9b_x45g_one_r2 (mode two_routes)

10 random items (seed 0) of 200; the prompt as the model reads it (the chat read appends a space), ⟦the bridge word⟧ where the change is added at layer 12; each arm's answer = the top token at the read step. UNVERIFIED.

## P2-L0-0016 (bridge hydrogen -> nitrogen; its locker sentence before the pick)

**lookup** (original 9, changed 6)

```
<|im_start|>user
The locker of hydrogen is nine. Olivia picked nitrogen. Oscar picked helium. The locker of helium is seven. The locker of nitrogen is six. Hugo picked⟦ hydrogen⟧.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (original 1, changed 7)

```
<|im_start|>user
The locker of hydrogen is nine. Olivia picked nitrogen. Oscar picked helium. The locker of helium is seven. The locker of nitrogen is six. Hugo picked⟦ hydrogen⟧.
What is the atomic number of Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0091 (bridge oxygen -> hydrogen; its locker sentence before the pick)

**lookup** (original 7, changed 8)

```
<|im_start|>user
Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ oxygen⟧.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (original 8, changed 1)

```
<|im_start|>user
Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ oxygen⟧.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0108 (bridge frog -> ant; its locker sentence after the pick)

**lookup** (original 1, changed 2)

```
<|im_start|>user
James picked the⟦ frog⟧. Rose picked the ant. The locker of the frog is 1. The locker of the bear is 3. Frank picked the bear. The locker of the ant is 2.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (original 4, changed 6)

```
<|im_start|>user
James picked the⟦ frog⟧. Rose picked the ant. The locker of the frog is 1. The locker of the bear is 3. Frank picked the bear. The locker of the ant is 2.
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0139 (bridge oxygen -> nitrogen; its locker sentence before the pick)

**lookup** (original 6, changed 9)

```
<|im_start|>user
Hugo picked nitrogen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked⟦ oxygen⟧.
Which locker belongs to Ruby's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (original 8, changed 7)

```
<|im_start|>user
Hugo picked nitrogen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked⟦ oxygen⟧.
What is the atomic number of Ruby's pick? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0144 (bridge dog -> owl; its locker sentence before the pick)

**lookup** (original 8, changed 1)

```
<|im_start|>user
The locker of the dog is 8. The locker of the spider is 3. Oscar picked the⟦ dog⟧. The locker of the owl is 1. Leo picked the spider. Amy picked the owl.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), other |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), other |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 4, changed 2)

```
<|im_start|>user
The locker of the dog is 8. The locker of the spider is 3. Oscar picked the⟦ dog⟧. The locker of the owl is 1. Leo picked the spider. Amy picked the owl.
How many legs does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0150 (bridge pig -> ant; its locker sentence before the pick)

**lookup** (original 7, changed 3)

```
<|im_start|>user
David picked the deer. The locker of the ant is 3. The locker of the pig is 7. The locker of the deer is 1. Dan picked the ant. Sam picked the⟦ pig⟧.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (original 4, changed 6)

```
<|im_start|>user
David picked the deer. The locker of the ant is 3. The locker of the pig is 7. The locker of the deer is 1. Dan picked the ant. Sam picked the⟦ pig⟧.
How many legs does Sam's pick have? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0171 (bridge owl -> beetle; its locker sentence after the pick)

**lookup** (original 9, changed 3)

```
<|im_start|>user
Maria picked the beetle. Eva picked the⟦ owl⟧. The locker of the owl is nine. The locker of the beetle is three. Peter picked the lion. The locker of the lion is six.
Which locker belongs to Eva's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (original 2, changed 6)

```
<|im_start|>user
Maria picked the beetle. Eva picked the⟦ owl⟧. The locker of the owl is nine. The locker of the beetle is three. Peter picked the lion. The locker of the lion is six.
How many legs does Eva's pick have? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0174 (bridge chicken -> fox; its locker sentence after the pick)

**lookup** (original 4, changed 5)

```
<|im_start|>user
Vera picked the fly. Tara picked the fox. The locker of the fox is five. Sam picked the⟦ chicken⟧. The locker of the fly is two. The locker of the chicken is four.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (original 2, changed 4)

```
<|im_start|>user
Vera picked the fly. Tara picked the fox. The locker of the fox is five. Sam picked the⟦ chicken⟧. The locker of the fly is two. The locker of the chicken is four.
How many legs does Sam's pick have? Answer with a single digit and nothing else.<|im_end|>
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
| without J++ and U | (not stored), other |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0183 (bridge dog -> beetle; its locker sentence after the pick)

**lookup** (original 2, changed 7)

```
<|im_start|>user
Peter picked the beetle. Oscar picked the⟦ dog⟧. The locker of the beetle is seven. Ivy picked the camel. The locker of the dog is two. The locker of the camel is one.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (original 4, changed 6)

```
<|im_start|>user
Peter picked the beetle. Oscar picked the⟦ dog⟧. The locker of the beetle is seven. Ivy picked the camel. The locker of the dog is two. The locker of the camel is one.
How many legs does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
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

## P2-L0-0278 (bridge alpha -> beta; its locker sentence after the pick)

**lookup** (original 6, changed 7)

```
<|im_start|>user
Grace picked delta. The locker of delta is 8. Ben picked⟦ alpha⟧. The locker of beta is 7. Frank picked beta. The locker of alpha is 6.
Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|im_end|>
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
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 1, changed 2)

```
<|im_start|>user
Grace picked delta. The locker of delta is 8. Ben picked⟦ alpha⟧. The locker of beta is 7. Frank picked beta. The locker of alpha is 6.
Which position in the Greek alphabet does Ben's pick have? Answer with a single digit and nothing else.<|im_end|>
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

