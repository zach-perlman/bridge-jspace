# 48.5 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge token, where every arm is written. UNVERIFIED.

## qwen35_9b_x48_route2: 10 random items of 151 (seed 0)

### P2-L0-0031 (elements): bridge oxygen (slot 3) → carbon (slot 1); slot 0 hydrogen (locker 9, attribute 1), slot 1 carbon (locker 5, attribute 6), slot 2 nitrogen (locker 4, attribute 7), slot 3 oxygen (locker 6, attribute 8); informative writes: k = 0, k = 2

**lookup** (PP-L0-0031): O's answer 6, S's answer 5; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Kyle picked nitrogen. The locker of hydrogen is nine. The locker of carbon is five. The locker of nitrogen is four. The locker of oxygen is six. Leo picked ⟦bridge:oxygen⟧. David picked hydrogen.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6\n' |
| whole | '5' | - | 1 | 0 | ' 5\n' |
| a1 | '5' | - | 1 | 0 | ' 5\n' |
| w0 | '5' | changed | 1 | 0 | ' 5\n' |
| p0 | '6' | original | 0 | 1 | ' 6\n' |
| r0 | '5' | changed | 1 | 0 | ' 5\n' |
| w1 | '9' | other_slot | 0 | 0 | ' 9\n' |
| p1 | '9' | other_slot | 0 | 0 | ' 9\n' |
| r1 | '5' | slot_k | 1 | 0 | ' 5\n' |
| w2 | '5' | changed | 1 | 0 | ' 5\n' |
| p2 | '6' | original | 0 | 1 | ' 6\n' |
| r2 | '5' | changed | 1 | 0 | ' 5\n' |

**recall** (PM-L0-0031): O's answer 8, S's answer 6; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Kyle picked nitrogen. The locker of hydrogen is nine. The locker of carbon is five. The locker of nitrogen is four. The locker of oxygen is six. Leo picked ⟦bridge:oxygen⟧. David picked hydrogen.
What is the atomic number of Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8\n' |
| whole | '6' | - | 1 | 0 | ' 6\n' |
| a1 | '6' | - | 1 | 0 | ' 6\n' |
| w0 | '6' | changed | 1 | 0 | ' 6\n' |
| p0 | '8' | original | 0 | 1 | ' 8\n' |
| r0 | '6' | changed | 1 | 0 | ' 6\n' |
| w1 | '8' | original | 0 | 1 | ' 8\n' |
| p1 | '8' | original | 0 | 1 | ' 8\n' |
| r1 | '6' | slot_k | 1 | 0 | ' 6\n' |
| w2 | '8' | original | 0 | 1 | ' 8\n' |
| p2 | '8' | original | 0 | 1 | ' 8\n' |
| r2 | '6' | changed | 1 | 0 | ' 6\n' |

### P2-L0-0253 (elements): bridge oxygen (slot 1) → helium (slot 2); slot 0 lithium (locker 6, attribute 3), slot 1 oxygen (locker 9, attribute 8), slot 2 helium (locker 7, attribute 2), slot 3 hydrogen (locker 5, attribute 1); informative writes: k = 0, k = 3

**lookup** (PP-L0-0253): O's answer 9, S's answer 7; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of lithium is 6. Oscar picked lithium. The locker of oxygen is 9. The locker of helium is 7. The locker of hydrogen is 5. Ivan picked ⟦bridge:oxygen⟧. Mia picked hydrogen.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9\n' |
| whole | '7' | - | 1 | 0 | ' 7\n' |
| a1 | '7' | - | 1 | 0 | ' 7\n' |
| w0 | '6' | slot_k | 0 | 0 | ' 6\n' |
| p0 | '6' | slot_k | 0 | 0 | ' 6\n' |
| r0 | '7' | changed | 1 | 0 | ' 7\n' |
| w2 | '7' | slot_k | 1 | 0 | ' 7\n' |
| p2 | '9' | original | 0 | 1 | ' 9\n' |
| r2 | '7' | slot_k | 1 | 0 | ' 7\n' |
| w3 | '7' | changed | 1 | 0 | ' 7\n' |
| p3 | '9' | original | 0 | 1 | ' 9\n' |
| r3 | '7' | changed | 1 | 0 | ' 7\n' |

**recall** (PM-L0-0253): O's answer 8, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of lithium is 6. Oscar picked lithium. The locker of oxygen is 9. The locker of helium is 7. The locker of hydrogen is 5. Ivan picked ⟦bridge:oxygen⟧. Mia picked hydrogen.
What is the atomic number of Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8\n' |
| whole | '2' | - | 1 | 0 | ' 2\n' |
| a1 | '7' | - | 0 | 0 | ' 7\n' |
| w0 | '6' | other | 0 | 0 | ' 6\n' |
| p0 | '6' | other | 0 | 0 | ' 6\n' |
| r0 | '2' | changed | 1 | 0 | ' 2\n' |
| w2 | '7' | other | 0 | 0 | ' 7\n' |
| p2 | '8' | original | 0 | 1 | ' 8\n' |
| r2 | '7' | other | 0 | 0 | ' 7\n' |
| w3 | '7' | other | 0 | 0 | ' 7\n' |
| p3 | '8' | original | 0 | 1 | ' 8\n' |
| r3 | '7' | other | 0 | 0 | ' 7\n' |

### P2-L0-0309 (animals): bridge beetle (slot 0) → owl (slot 2); slot 0 beetle (locker 2, attribute 6), slot 1 duck (locker 1, attribute 2), slot 2 owl (locker 5, attribute 2), slot 3 bee (locker 4, attribute 6); informative writes: 

**lookup** (PP-L0-0309): O's answer 2, S's answer 5; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Oscar picked the bee. The locker of the beetle is 2. The locker of the duck is 1. The locker of the owl is 5. The locker of the bee is 4. Peter picked the duck. Dan picked the ⟦bridge:beetle⟧.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2\n' |
| whole | '5' | - | 1 | 0 | ' 5\n' |
| a1 | '5' | - | 1 | 0 | ' 5\n' |
| w1 | '5' | changed | 1 | 0 | ' 5\n' |
| p1 | '2' | original | 0 | 1 | ' 2\n' |
| r1 | '5' | changed | 1 | 0 | ' 5\n' |
| w2 | '5' | slot_k | 1 | 0 | ' 5\n' |
| p2 | '2' | original | 0 | 1 | ' 2\n' |
| r2 | '5' | slot_k | 1 | 0 | ' 5\n' |
| w3 | '5' | changed | 1 | 0 | ' 5\n' |
| p3 | '2' | original | 0 | 1 | ' 2\n' |
| r3 | '5' | changed | 1 | 0 | ' 5\n' |

**recall** (PM-L0-0309): O's answer 6, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Oscar picked the bee. The locker of the beetle is 2. The locker of the duck is 1. The locker of the owl is 5. The locker of the bee is 4. Peter picked the duck. Dan picked the ⟦bridge:beetle⟧.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6\n' |
| whole | '2' | - | 1 | 0 | ' 2\n' |
| a1 | '2' | - | 1 | 0 | ' 2\n' |
| w1 | '2' | slot_k | 1 | 0 | ' 2\n' |
| p1 | '6' | original | 0 | 1 | ' 6\n' |
| r1 | '2' | slot_k | 1 | 0 | ' 2\n' |
| w2 | '2' | slot_k | 1 | 0 | ' 2\n' |
| p2 | '6' | original | 0 | 1 | ' 6\n' |
| r2 | '2' | slot_k | 1 | 0 | ' 2\n' |
| w3 | '2' | changed | 1 | 0 | ' 2\n' |
| p3 | '6' | slot_k | 0 | 1 | ' 6\n' |
| r3 | '2' | changed | 1 | 0 | ' 2\n' |

### P2-L0-0375 (animals): bridge lion (slot 1) → bee (slot 2); slot 0 fly (locker 7, attribute 6), slot 1 lion (locker 6, attribute 4), slot 2 bee (locker 1, attribute 6), slot 3 cow (locker 8, attribute 4); informative writes: 

**lookup** (PP-L0-0375): O's answer 6, S's answer 1; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Ryan picked the fly. The locker of the fly is 7. The locker of the lion is 6. The locker of the bee is 1. The locker of the cow is 8. Kate picked the cow. Dan picked the ⟦bridge:lion⟧.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6\n' |
| whole | '1' | - | 1 | 0 | ' 1\n' |
| a1 | '1' | - | 1 | 0 | ' 1\n' |
| w0 | '1' | changed | 1 | 0 | ' 1\n' |
| p0 | '6' | original | 0 | 1 | ' 6\n' |
| r0 | '1' | changed | 1 | 0 | ' 1\n' |
| w2 | '1' | slot_k | 1 | 0 | ' 1\n' |
| p2 | '6' | original | 0 | 1 | ' 6\n' |
| r2 | '1' | slot_k | 1 | 0 | ' 1\n' |
| w3 | '1' | changed | 1 | 0 | ' 1\n' |
| p3 | '6' | original | 0 | 1 | ' 6\n' |
| r3 | '1' | changed | 1 | 0 | ' 1\n' |

**recall** (PM-L0-0375): O's answer 4, S's answer 6; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Ryan picked the fly. The locker of the fly is 7. The locker of the lion is 6. The locker of the bee is 1. The locker of the cow is 8. Kate picked the cow. Dan picked the ⟦bridge:lion⟧.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4\n' |
| whole | '6' | - | 1 | 0 | ' 6\n' |
| a1 | '6' | - | 1 | 0 | ' 6\n' |
| w0 | '6' | slot_k | 1 | 0 | ' 6\n' |
| p0 | '4' | original | 0 | 1 | ' 4\n' |
| r0 | '6' | slot_k | 1 | 0 | ' 6\n' |
| w2 | '6' | slot_k | 1 | 0 | ' 6\n' |
| p2 | '4' | original | 0 | 1 | ' 4\n' |
| r2 | '6' | slot_k | 1 | 0 | ' 6\n' |
| w3 | '6' | changed | 1 | 0 | ' 6\n' |
| p3 | '4' | slot_k | 0 | 1 | ' 4\n' |
| r3 | '6' | changed | 1 | 0 | ' 6\n' |

### P2-L0-0399 (animals): bridge deer (slot 2) → duck (slot 1); slot 0 butterfly (locker 5, attribute 6), slot 1 duck (locker 3, attribute 2), slot 2 deer (locker 9, attribute 4), slot 3 goose (locker 6, attribute 2); informative writes: k = 0

**lookup** (PP-L0-0399): O's answer 9, S's answer 3; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the butterfly is five. The locker of the duck is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9\n' |
| whole | '3' | - | 1 | 0 | ' 3\n' |
| a1 | '3' | - | 1 | 0 | ' 3\n' |
| w0 | '5' | slot_k | 0 | 0 | ' 5\n' |
| p0 | '5' | slot_k | 0 | 0 | ' 5\n' |
| r0 | '3' | changed | 1 | 0 | ' 3\n' |
| w1 | '3' | slot_k | 1 | 0 | ' 3\n' |
| p1 | '9' | original | 0 | 1 | ' 9\n' |
| r1 | '3' | slot_k | 1 | 0 | ' 3\n' |
| w3 | '3' | changed | 1 | 0 | ' 3\n' |
| p3 | '9' | original | 0 | 1 | ' 9\n' |
| r3 | '3' | changed | 1 | 0 | ' 3\n' |

**recall** (PM-L0-0399): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the butterfly is five. The locker of the duck is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
How many legs does Tara's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4\n' |
| whole | '2' | - | 1 | 0 | ' 2\n' |
| a1 | '2' | - | 1 | 0 | ' 2\n' |
| w0 | '6' | slot_k | 0 | 0 | ' 6\n' |
| p0 | '4' | original | 0 | 1 | ' 4\n' |
| r0 | '2' | changed | 1 | 0 | ' 2\n' |
| w1 | '2' | slot_k | 1 | 0 | ' 2\n' |
| p1 | '4' | original | 0 | 1 | ' 4\n' |
| r1 | '2' | slot_k | 1 | 0 | ' 2\n' |
| w3 | '2' | slot_k | 1 | 0 | ' 2\n' |
| p3 | '4' | original | 0 | 1 | ' 4\n' |
| r3 | '2' | slot_k | 1 | 0 | ' 2\n' |

### P2-L0-0414 (animals): bridge turkey (slot 3) → rabbit (slot 0); slot 0 rabbit (locker 9, attribute 4), slot 1 butterfly (locker 4, attribute 6), slot 2 sheep (locker 5, attribute 4), slot 3 turkey (locker 7, attribute 2); informative writes: k = 1

**lookup** (PP-L0-0414): O's answer 7, S's answer 9; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Iris picked the butterfly. The locker of the rabbit is 9. The locker of the butterfly is 4. The locker of the sheep is 5. Leo picked the sheep. The locker of the turkey is 7. Tom picked the ⟦bridge:turkey⟧.
Which locker belongs to Tom's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '7' | - | 0 | 1 | ' 7\n' |
| whole | '9' | - | 1 | 0 | ' 9\n' |
| a1 | '9' | - | 1 | 0 | ' 9\n' |
| w0 | '9' | slot_k | 1 | 0 | ' 9\n' |
| p0 | '7' | original | 0 | 1 | ' 7\n' |
| r0 | '9' | slot_k | 1 | 0 | ' 9\n' |
| w1 | '9' | changed | 1 | 0 | ' 9\n' |
| p1 | '7' | original | 0 | 1 | ' 7\n' |
| r1 | '9' | changed | 1 | 0 | ' 9\n' |
| w2 | '9' | changed | 1 | 0 | ' 9\n' |
| p2 | '7' | original | 0 | 1 | ' 7\n' |
| r2 | '9' | changed | 1 | 0 | ' 9\n' |

**recall** (PM-L0-0414): O's answer 2, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Iris picked the butterfly. The locker of the rabbit is 9. The locker of the butterfly is 4. The locker of the sheep is 5. Leo picked the sheep. The locker of the turkey is 7. Tom picked the ⟦bridge:turkey⟧.
How many legs does Tom's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2\n' |
| whole | '4' | - | 1 | 0 | ' 4\n' |
| a1 | '4' | - | 1 | 0 | ' 4\n' |
| w0 | '4' | slot_k | 1 | 0 | ' 4\n' |
| p0 | '2' | original | 0 | 1 | ' 2\n' |
| r0 | '4' | slot_k | 1 | 0 | ' 4\n' |
| w1 | '4' | changed | 1 | 0 | ' 4\n' |
| p1 | '2' | original | 0 | 1 | ' 2\n' |
| r1 | '4' | changed | 1 | 0 | ' 4\n' |
| w2 | '4' | slot_k | 1 | 0 | ' 4\n' |
| p2 | '2' | original | 0 | 1 | ' 2\n' |
| r2 | '4' | slot_k | 1 | 0 | ' 4\n' |

### P2-L0-0426 (animals): bridge mouse (slot 0) → owl (slot 2); slot 0 mouse (locker 6, attribute 4), slot 1 ant (locker 1, attribute 6), slot 2 owl (locker 9, attribute 2), slot 3 crow (locker 7, attribute 2); informative writes: k = 1

**lookup** (PP-L0-0426): O's answer 6, S's answer 9; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the mouse is 6. The locker of the ant is 1. The locker of the owl is 9. The locker of the crow is 7. David picked the ⟦bridge:mouse⟧. Victor picked the ant. Beth picked the crow.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6\n' |
| whole | '9' | - | 1 | 0 | ' 9\n' |
| a1 | '9' | - | 1 | 0 | ' 9\n' |
| w1 | '9' | changed | 1 | 0 | ' 9\n' |
| p1 | '1' | slot_k | 0 | 0 | ' 1\n' |
| r1 | '9' | changed | 1 | 0 | ' 9\n' |
| w2 | '9' | slot_k | 1 | 0 | ' 9\n' |
| p2 | '1' | other_slot | 0 | 0 | ' 1\n' |
| r2 | '9' | slot_k | 1 | 0 | ' 9\n' |
| w3 | '9' | changed | 1 | 0 | ' 9\n' |
| p3 | '7' | slot_k | 0 | 0 | ' 7\n' |
| r3 | '9' | changed | 1 | 0 | ' 9\n' |

**recall** (PM-L0-0426): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the mouse is 6. The locker of the ant is 1. The locker of the owl is 9. The locker of the crow is 7. David picked the ⟦bridge:mouse⟧. Victor picked the ant. Beth picked the crow.
How many legs does David's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4\n' |
| whole | '2' | - | 1 | 0 | ' 2\n' |
| a1 | '2' | - | 1 | 0 | ' 2\n' |
| w1 | '2' | changed | 1 | 0 | ' 2\n' |
| p1 | '6' | slot_k | 0 | 0 | ' 6\n' |
| r1 | '2' | changed | 1 | 0 | ' 2\n' |
| w2 | '2' | slot_k | 1 | 0 | ' 2\n' |
| p2 | '6' | other | 0 | 0 | ' 6\n' |
| r2 | '2' | slot_k | 1 | 0 | ' 2\n' |
| w3 | '2' | slot_k | 1 | 0 | ' 2\n' |
| p3 | '4' | original | 0 | 1 | ' 4\n' |
| r3 | '2' | slot_k | 1 | 0 | ' 2\n' |

### P2-L0-0466 (elements): bridge helium (slot 0) → lithium (slot 1); slot 0 helium (locker 5, attribute 2), slot 1 lithium (locker 1, attribute 3), slot 2 hydrogen (locker 9, attribute 1), slot 3 oxygen (locker 2, attribute 8); informative writes: k = 2, k = 3

**lookup** (PP-L0-0466): O's answer 5, S's answer 1; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of helium is 5. The locker of lithium is 1. The locker of hydrogen is 9. Emma picked hydrogen. The locker of oxygen is 2. Oscar picked oxygen. Beth picked ⟦bridge:helium⟧.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '5' | - | 0 | 1 | ' 5\n' |
| whole | '1' | - | 1 | 0 | ' 1\n' |
| a1 | '1' | - | 1 | 0 | ' 1\n' |
| w1 | '1' | slot_k | 1 | 0 | ' 1\n' |
| p1 | '2' | other_slot | 0 | 0 | ' 2\n' |
| r1 | '1' | slot_k | 1 | 0 | ' 1\n' |
| w2 | '1' | changed | 1 | 0 | ' 1\n' |
| p2 | '2' | other_slot | 0 | 0 | ' 2\n' |
| r2 | '1' | changed | 1 | 0 | ' 1\n' |
| w3 | '2' | slot_k | 0 | 0 | ' 2\n' |
| p3 | '2' | slot_k | 0 | 0 | ' 2\n' |
| r3 | '1' | changed | 1 | 0 | ' 1\n' |

**recall** (PM-L0-0466): O's answer 2, S's answer 3; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of helium is 5. The locker of lithium is 1. The locker of hydrogen is 9. Emma picked hydrogen. The locker of oxygen is 2. Oscar picked oxygen. Beth picked ⟦bridge:helium⟧.
What is the atomic number of Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2\n' |
| whole | '3' | - | 1 | 0 | ' 3\n' |
| a1 | '3' | - | 1 | 0 | ' 3\n' |
| w1 | '3' | slot_k | 1 | 0 | ' 3\n' |
| p1 | '2' | original | 0 | 1 | ' 2\n' |
| r1 | '3' | slot_k | 1 | 0 | ' 3\n' |
| w2 | '3' | changed | 1 | 0 | ' 3\n' |
| p2 | '2' | original | 0 | 1 | ' 2\n' |
| r2 | '3' | changed | 1 | 0 | ' 3\n' |
| w3 | '3' | changed | 1 | 0 | ' 3\n' |
| p3 | '8' | slot_k | 0 | 0 | ' 8\n' |
| r3 | '3' | changed | 1 | 0 | ' 3\n' |

### P2-L0-0473 (greek): bridge beta (slot 3) → alpha (slot 2); slot 0 gamma (locker 6, attribute 3), slot 1 eta (locker 8, attribute 7), slot 2 alpha (locker 9, attribute 1), slot 3 beta (locker 3, attribute 2); informative writes: k = 0, k = 1

**lookup** (PP-L0-0473): O's answer 3, S's answer 9; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of gamma is 6. Victor picked eta. The locker of eta is 8. Vera picked gamma. The locker of alpha is 9. The locker of beta is 3. Ivy picked ⟦bridge:beta⟧.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '3' | - | 0 | 1 | ' 3\n' |
| whole | '9' | - | 1 | 0 | ' 9\n' |
| a1 | '9' | - | 1 | 0 | ' 9\n' |
| w0 | '6' | slot_k | 0 | 0 | ' 6\n' |
| p0 | '6' | slot_k | 0 | 0 | ' 6\n' |
| r0 | '9' | changed | 1 | 0 | ' 9\n' |
| w1 | '9' | changed | 1 | 0 | ' 9\n' |
| p1 | '3' | original | 0 | 1 | ' 3\n' |
| r1 | '9' | changed | 1 | 0 | ' 9\n' |
| w2 | '9' | slot_k | 1 | 0 | ' 9\n' |
| p2 | '3' | original | 0 | 1 | ' 3\n' |
| r2 | '9' | slot_k | 1 | 0 | ' 9\n' |

**recall** (PM-L0-0473): O's answer 2, S's answer 1; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of gamma is 6. Victor picked eta. The locker of eta is 8. Vera picked gamma. The locker of alpha is 9. The locker of beta is 3. Ivy picked ⟦bridge:beta⟧.
Which position in the Greek alphabet does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2\n' |
| whole | '1' | - | 1 | 0 | ' 1\n' |
| a1 | '1' | - | 1 | 0 | ' 1\n' |
| w0 | '3' | slot_k | 0 | 0 | ' 3\n' |
| p0 | '2' | original | 0 | 1 | ' 2\n' |
| r0 | '1' | changed | 1 | 0 | ' 1\n' |
| w1 | '2' | original | 0 | 1 | ' 2\n' |
| p1 | '2' | original | 0 | 1 | ' 2\n' |
| r1 | '1' | changed | 1 | 0 | ' 1\n' |
| w2 | '1' | slot_k | 1 | 0 | ' 1\n' |
| p2 | '2' | original | 0 | 1 | ' 2\n' |
| r2 | '1' | slot_k | 1 | 0 | ' 1\n' |

### P2-L0-0507 (animals): bridge lion (slot 2) → bee (slot 0); slot 0 bee (locker 4, attribute 6), slot 1 chicken (locker 3, attribute 2), slot 2 lion (locker 8, attribute 4), slot 3 mouse (locker 9, attribute 4); informative writes: k = 1

**lookup** (PP-L0-0507): O's answer 8, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the bee is 4. The locker of the chicken is 3. Oscar picked the chicken. The locker of the lion is 8. Mia picked the ⟦bridge:lion⟧. The locker of the mouse is 9. Ruby picked the mouse.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8\n' |
| whole | '4' | - | 1 | 0 | ' 4\n' |
| a1 | '4' | - | 1 | 0 | ' 4\n' |
| w0 | '4' | slot_k | 1 | 0 | ' 4\n' |
| p0 | '4' | slot_k | 1 | 0 | ' 4\n' |
| r0 | '4' | slot_k | 1 | 0 | ' 4\n' |
| w1 | '4' | changed | 1 | 0 | ' 4\n' |
| p1 | '8' | original | 0 | 1 | ' 8\n' |
| r1 | '4' | changed | 1 | 0 | ' 4\n' |
| w3 | '4' | changed | 1 | 0 | ' 4\n' |
| p3 | '8' | original | 0 | 1 | ' 8\n' |
| r3 | '4' | changed | 1 | 0 | ' 4\n' |

**recall** (PM-L0-0507): O's answer 4, S's answer 6; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the bee is 4. The locker of the chicken is 3. Oscar picked the chicken. The locker of the lion is 8. Mia picked the ⟦bridge:lion⟧. The locker of the mouse is 9. Ruby picked the mouse.
How many legs does Mia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4\n' |
| whole | '6' | - | 1 | 0 | ' 6\n' |
| a1 | '6' | - | 1 | 0 | ' 6\n' |
| w0 | '6' | slot_k | 1 | 0 | ' 6\n' |
| p0 | '4' | original | 0 | 1 | ' 4\n' |
| r0 | '6' | slot_k | 1 | 0 | ' 6\n' |
| w1 | '6' | changed | 1 | 0 | ' 6\n' |
| p1 | '4' | original | 0 | 1 | ' 4\n' |
| r1 | '6' | changed | 1 | 0 | ' 6\n' |
| w3 | '6' | changed | 1 | 0 | ' 6\n' |
| p3 | '4' | slot_k | 0 | 1 | ' 4\n' |
| r3 | '6' | changed | 1 | 0 | ' 6\n' |

## x48_route2_27b: 10 random items of 202 (seed 0)

### P2-L0-0025 (elements): bridge helium (slot 1) → oxygen (slot 3); slot 0 hydrogen (locker 5, attribute 1), slot 1 helium (locker 6, attribute 2), slot 2 nitrogen (locker 3, attribute 7), slot 3 oxygen (locker 7, attribute 8); informative writes: k = 0, k = 2

**lookup** (PP-L0-0025): O's answer 6, S's answer 7; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of hydrogen is 5. The locker of helium is 6. The locker of nitrogen is 3. The locker of oxygen is 7. Mark picked hydrogen. Owen picked ⟦bridge:helium⟧. Sara picked nitrogen.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6' |
| whole | '7' | - | 1 | 0 | ' 7' |
| a1 | '7' | - | 1 | 0 | ' 7' |
| w0 | '5' | slot_k | 0 | 0 | ' 5' |
| p0 | '6' | original | 0 | 1 | ' 6' |
| r0 | '7' | changed | 1 | 0 | ' 7' |
| w2 | '7' | changed | 1 | 0 | ' 7' |
| p2 | '6' | original | 0 | 1 | ' 6' |
| r2 | '7' | changed | 1 | 0 | ' 7' |
| w3 | '7' | slot_k | 1 | 0 | ' 7' |
| p3 | '6' | original | 0 | 1 | ' 6' |
| r3 | '7' | slot_k | 1 | 0 | ' 7' |

**recall** (PM-L0-0025): O's answer 2, S's answer 8; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of hydrogen is 5. The locker of helium is 6. The locker of nitrogen is 3. The locker of oxygen is 7. Mark picked hydrogen. Owen picked ⟦bridge:helium⟧. Sara picked nitrogen.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2' |
| whole | '8' | - | 1 | 0 | ' 8' |
| a1 | '2' | - | 0 | 1 | ' 2' |
| w0 | '2' | original | 0 | 1 | ' 2' |
| p0 | '2' | original | 0 | 1 | ' 2' |
| r0 | '2' | original | 0 | 1 | ' 2' |
| w2 | '2' | original | 0 | 1 | ' 8' |
| p2 | '2' | original | 0 | 1 | ' 2' |
| r2 | '2' | original | 0 | 1 | ' 2' |
| w3 | '2' | original | 0 | 1 | ' 2' |
| p3 | '2' | original | 0 | 1 | ' 2' |
| r3 | '2' | original | 0 | 1 | ' 2' |

### P2-L0-0207 (animals): bridge rabbit (slot 0) → eagle (slot 2); slot 0 rabbit (locker 9, attribute 4), slot 1 owl (locker 8, attribute 2), slot 2 eagle (locker 5, attribute 2), slot 3 sheep (locker 2, attribute 4); informative writes: 

**lookup** (PP-L0-0207): O's answer 9, S's answer 5; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the rabbit is 9. The locker of the owl is 8. The locker of the eagle is 5. The locker of the sheep is 2. Anna picked the sheep. Jack picked the owl. Eva picked the ⟦bridge:rabbit⟧.
Which locker belongs to Eva's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9' |
| whole | '5' | - | 1 | 0 | ' 5' |
| a1 | '5' | - | 1 | 0 | ' 5' |
| w1 | '5' | changed | 1 | 0 | ' 5' |
| p1 | '8' | slot_k | 0 | 0 | ' 8' |
| r1 | '5' | changed | 1 | 0 | ' 5' |
| w2 | '5' | slot_k | 1 | 0 | ' 5' |
| p2 | '2' | other_slot | 0 | 0 | ' 2' |
| r2 | '5' | slot_k | 1 | 0 | ' 5' |
| w3 | '5' | changed | 1 | 0 | ' 5' |
| p3 | '9' | original | 0 | 1 | ' 9' |
| r3 | '5' | changed | 1 | 0 | ' 5' |

**recall** (PM-L0-0207): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the rabbit is 9. The locker of the owl is 8. The locker of the eagle is 5. The locker of the sheep is 2. Anna picked the sheep. Jack picked the owl. Eva picked the ⟦bridge:rabbit⟧.
How many legs does Eva's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '2' | - | 1 | 0 | ' 2' |
| w1 | '2' | slot_k | 1 | 0 | ' 2' |
| p1 | '4' | original | 0 | 1 | ' 4' |
| r1 | '2' | slot_k | 1 | 0 | ' 2' |
| w2 | '2' | slot_k | 1 | 0 | ' 2' |
| p2 | '4' | original | 0 | 1 | ' 4' |
| r2 | '4' | original | 0 | 1 | ' 4' |
| w3 | '4' | slot_k | 0 | 1 | ' 4' |
| p3 | '4' | slot_k | 0 | 1 | ' 4' |
| r3 | '4' | slot_k | 0 | 1 | ' 4' |

### P2-L0-0234 (animals): bridge beetle (slot 1) → bear (slot 0); slot 0 bear (locker 1, attribute 4), slot 1 beetle (locker 7, attribute 6), slot 2 crow (locker 6, attribute 2), slot 3 elephant (locker 9, attribute 4); informative writes: k = 2

**lookup** (PP-L0-0234): O's answer 7, S's answer 1; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Kate picked the elephant. Grace picked the crow. The locker of the bear is 1. The locker of the beetle is 7. The locker of the crow is 6. The locker of the elephant is 9. Ivy picked the ⟦bridge:beetle⟧.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '7' | - | 0 | 1 | ' 7' |
| whole | '1' | - | 1 | 0 | ' 1' |
| a1 | '1' | - | 1 | 0 | ' 1' |
| w0 | '1' | slot_k | 1 | 0 | ' 1' |
| p0 | '7' | original | 0 | 1 | ' 7' |
| r0 | '1' | slot_k | 1 | 0 | ' 1' |
| w2 | '1' | changed | 1 | 0 | ' 1' |
| p2 | '7' | original | 0 | 1 | ' 7' |
| r2 | '1' | changed | 1 | 0 | ' 1' |
| w3 | '1' | changed | 1 | 0 | ' 1' |
| p3 | '7' | original | 0 | 1 | ' 7' |
| r3 | '1' | changed | 1 | 0 | ' 1' |

**recall** (PM-L0-0234): O's answer 6, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Kate picked the elephant. Grace picked the crow. The locker of the bear is 1. The locker of the beetle is 7. The locker of the crow is 6. The locker of the elephant is 9. Ivy picked the ⟦bridge:beetle⟧.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '6' | - | 0 | 1 | ' 6' |
| w0 | '6' | original | 0 | 1 | ' 6' |
| p0 | '6' | original | 0 | 1 | ' 6' |
| r0 | '6' | original | 0 | 1 | ' 6' |
| w2 | '6' | original | 0 | 1 | ' 6' |
| p2 | '6' | original | 0 | 1 | ' 6' |
| r2 | '6' | original | 0 | 1 | ' 6' |
| w3 | '6' | original | 0 | 1 | ' 6' |
| p3 | '6' | original | 0 | 1 | ' 6' |
| r3 | '6' | original | 0 | 1 | ' 6' |

### P2-L0-0304 (elements): bridge lithium (slot 3) → hydrogen (slot 1); slot 0 helium (locker 4, attribute 2), slot 1 hydrogen (locker 6, attribute 1), slot 2 carbon (locker 5, attribute 6), slot 3 lithium (locker 1, attribute 3); informative writes: k = 0, k = 2

**lookup** (PP-L0-0304): O's answer 1, S's answer 6; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Finn picked helium. The locker of helium is four. The locker of hydrogen is six. The locker of carbon is five. The locker of lithium is one. Mark picked carbon. David picked ⟦bridge:lithium⟧.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '1' | - | 0 | 1 | ' 1' |
| whole | '6' | - | 1 | 0 | ' 6' |
| a1 | '6' | - | 1 | 0 | ' 6' |
| w0 | '4' | slot_k | 0 | 0 | ' 4' |
| p0 | '1' | original | 0 | 1 | ' 1' |
| r0 | '6' | changed | 1 | 0 | ' 6' |
| w1 | '6' | slot_k | 1 | 0 | ' 6' |
| p1 | '1' | original | 0 | 1 | ' 1' |
| r1 | '6' | slot_k | 1 | 0 | ' 6' |
| w2 | '6' | changed | 1 | 0 | ' 6' |
| p2 | '1' | original | 0 | 1 | ' 1' |
| r2 | '6' | changed | 1 | 0 | ' 6' |

**recall** (PM-L0-0304): O's answer 3, S's answer 1; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Finn picked helium. The locker of helium is four. The locker of hydrogen is six. The locker of carbon is five. The locker of lithium is one. Mark picked carbon. David picked ⟦bridge:lithium⟧.
What is the atomic number of David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '3' | - | 0 | 1 | ' 3' |
| whole | '1' | - | 1 | 0 | ' 1' |
| a1 | '3' | - | 0 | 1 | ' 3' |
| w0 | '3' | original | 0 | 1 | ' 3' |
| p0 | '3' | original | 0 | 1 | ' 3' |
| r0 | '3' | original | 0 | 1 | ' 3' |
| w1 | '3' | original | 0 | 1 | ' 3' |
| p1 | '3' | original | 0 | 1 | ' 3' |
| r1 | '3' | original | 0 | 1 | ' 3' |
| w2 | '3' | original | 0 | 1 | ' 3' |
| p2 | '3' | original | 0 | 1 | ' 3' |
| r2 | '3' | original | 0 | 1 | ' 3' |

### P2-L0-0328 (elements): bridge helium (slot 1) → oxygen (slot 0); slot 0 oxygen (locker 4, attribute 8), slot 1 helium (locker 7, attribute 2), slot 2 hydrogen (locker 3, attribute 1), slot 3 lithium (locker 1, attribute 3); informative writes: k = 2, k = 3

**lookup** (PP-L0-0328): O's answer 7, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of oxygen is 4. The locker of helium is 7. Ryan picked hydrogen. The locker of hydrogen is 3. David picked lithium. Diana picked ⟦bridge:helium⟧. The locker of lithium is 1.
Which locker belongs to Diana's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '7' | - | 0 | 1 | ' 7' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '4' | - | 1 | 0 | ' 4' |
| w0 | '4' | slot_k | 1 | 0 | ' 4' |
| p0 | '4' | slot_k | 1 | 0 | ' 4' |
| r0 | '4' | slot_k | 1 | 0 | ' 4' |
| w2 | '4' | changed | 1 | 0 | ' 4' |
| p2 | '7' | original | 0 | 1 | ' 7' |
| r2 | '4' | changed | 1 | 0 | ' 4' |
| w3 | '4' | changed | 1 | 0 | ' 4' |
| p3 | '7' | original | 0 | 1 | ' 7' |
| r3 | '4' | changed | 1 | 0 | ' 4' |

**recall** (PM-L0-0328): O's answer 2, S's answer 8; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of oxygen is 4. The locker of helium is 7. Ryan picked hydrogen. The locker of hydrogen is 3. David picked lithium. Diana picked ⟦bridge:helium⟧. The locker of lithium is 1.
What is the atomic number of Diana's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2' |
| whole | '8' | - | 1 | 0 | ' 8' |
| a1 | '8' | - | 1 | 0 | ' 8' |
| w0 | '8' | slot_k | 1 | 0 | ' 8' |
| p0 | '2' | original | 0 | 1 | ' 2' |
| r0 | '8' | slot_k | 1 | 0 | ' 8' |
| w2 | '8' | changed | 1 | 0 | ' 8' |
| p2 | '2' | original | 0 | 1 | ' 2' |
| r2 | '8' | changed | 1 | 0 | ' 8' |
| w3 | '8' | changed | 1 | 0 | ' 8' |
| p3 | '2' | original | 0 | 1 | ' 2' |
| r3 | '8' | changed | 1 | 0 | ' 8' |

### P2-L0-0337 (elements): bridge oxygen (slot 2) → nitrogen (slot 0); slot 0 nitrogen (locker 2, attribute 7), slot 1 hydrogen (locker 6, attribute 1), slot 2 oxygen (locker 7, attribute 8), slot 3 lithium (locker 9, attribute 3); informative writes: k = 1, k = 3

**lookup** (PP-L0-0337): O's answer 7, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Ivan picked lithium. The locker of nitrogen is 2. The locker of hydrogen is 6. The locker of oxygen is 7. The locker of lithium is 9. Mia picked ⟦bridge:oxygen⟧. Lily picked hydrogen.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '7' | - | 0 | 1 | ' 7' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '2' | - | 1 | 0 | ' 2' |
| w0 | '2' | slot_k | 1 | 0 | ' 2' |
| p0 | '7' | original | 0 | 1 | ' 7' |
| r0 | '2' | slot_k | 1 | 0 | ' 2' |
| w1 | '2' | changed | 1 | 0 | ' 2' |
| p1 | '7' | original | 0 | 1 | ' 7' |
| r1 | '2' | changed | 1 | 0 | ' 2' |
| w3 | '2' | changed | 1 | 0 | ' 2' |
| p3 | '7' | original | 0 | 1 | ' 7' |
| r3 | '2' | changed | 1 | 0 | ' 2' |

**recall** (PM-L0-0337): O's answer 8, S's answer 7; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Ivan picked lithium. The locker of nitrogen is 2. The locker of hydrogen is 6. The locker of oxygen is 7. The locker of lithium is 9. Mia picked ⟦bridge:oxygen⟧. Lily picked hydrogen.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8' |
| whole | '7' | - | 1 | 0 | ' 7' |
| a1 | '7' | - | 1 | 0 | ' 7' |
| w0 | '7' | slot_k | 1 | 0 | ' 7' |
| p0 | '8' | original | 0 | 1 | ' 8' |
| r0 | '7' | slot_k | 1 | 0 | ' 7' |
| w1 | '7' | changed | 1 | 0 | ' 7' |
| p1 | '8' | original | 0 | 1 | ' 8' |
| r1 | '7' | changed | 1 | 0 | ' 7' |
| w3 | '7' | changed | 1 | 0 | ' 7' |
| p3 | '8' | original | 0 | 1 | ' 8' |
| r3 | '7' | changed | 1 | 0 | ' 7' |

### P2-L0-0399 (animals): bridge deer (slot 2) → duck (slot 1); slot 0 butterfly (locker 5, attribute 6), slot 1 duck (locker 3, attribute 2), slot 2 deer (locker 9, attribute 4), slot 3 goose (locker 6, attribute 2); informative writes: k = 0

**lookup** (PP-L0-0399): O's answer 9, S's answer 3; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the butterfly is five. The locker of the duck is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9' |
| whole | '3' | - | 1 | 0 | ' 3' |
| a1 | '3' | - | 1 | 0 | ' 3' |
| w0 | '5' | slot_k | 0 | 0 | ' 5' |
| p0 | '5' | slot_k | 0 | 0 | ' 5' |
| r0 | '3' | changed | 1 | 0 | ' 3' |
| w1 | '3' | slot_k | 1 | 0 | ' 3' |
| p1 | '9' | original | 0 | 1 | ' 9' |
| r1 | '3' | slot_k | 1 | 0 | ' 3' |
| w3 | '3' | changed | 1 | 0 | ' 3' |
| p3 | '9' | original | 0 | 1 | ' 9' |
| r3 | '3' | changed | 1 | 0 | ' 3' |

**recall** (PM-L0-0399): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the butterfly is five. The locker of the duck is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
How many legs does Tara's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '4' | - | 0 | 1 | ' 4' |
| a1 | '4' | - | 0 | 1 | ' 4' |
| w0 | '4' | original | 0 | 1 | ' 4' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '4' | original | 0 | 1 | ' 4' |
| w1 | '4' | original | 0 | 1 | ' 4' |
| p1 | '4' | original | 0 | 1 | ' 4' |
| r1 | '4' | original | 0 | 1 | ' 4' |
| w3 | '4' | original | 0 | 1 | ' 4' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '4' | original | 0 | 1 | ' 4' |

### P2-L0-0414 (animals): bridge turkey (slot 3) → rabbit (slot 0); slot 0 rabbit (locker 9, attribute 4), slot 1 butterfly (locker 4, attribute 6), slot 2 sheep (locker 5, attribute 4), slot 3 turkey (locker 7, attribute 2); informative writes: k = 1

**lookup** (PP-L0-0414): O's answer 7, S's answer 9; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Iris picked the butterfly. The locker of the rabbit is 9. The locker of the butterfly is 4. The locker of the sheep is 5. Leo picked the sheep. The locker of the turkey is 7. Tom picked the ⟦bridge:turkey⟧.
Which locker belongs to Tom's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '7' | - | 0 | 1 | ' 7' |
| whole | '9' | - | 1 | 0 | ' 9' |
| a1 | '9' | - | 1 | 0 | ' 9' |
| w0 | '9' | slot_k | 1 | 0 | ' 9' |
| p0 | '7' | original | 0 | 1 | ' 7' |
| r0 | '9' | slot_k | 1 | 0 | ' 9' |
| w1 | '9' | changed | 1 | 0 | ' 9' |
| p1 | '7' | original | 0 | 1 | ' 7' |
| r1 | '9' | changed | 1 | 0 | ' 9' |
| w2 | '9' | changed | 1 | 0 | ' 9' |
| p2 | '7' | original | 0 | 1 | ' 7' |
| r2 | '9' | changed | 1 | 0 | ' 9' |

**recall** (PM-L0-0414): O's answer 2, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
Iris picked the butterfly. The locker of the rabbit is 9. The locker of the butterfly is 4. The locker of the sheep is 5. Leo picked the sheep. The locker of the turkey is 7. Tom picked the ⟦bridge:turkey⟧.
How many legs does Tom's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2' |
| whole | '2' | - | 0 | 1 | ' 2' |
| a1 | '2' | - | 0 | 1 | ' 2' |
| w0 | '2' | original | 0 | 1 | ' 2' |
| p0 | '2' | original | 0 | 1 | ' 2' |
| r0 | '2' | original | 0 | 1 | ' 2' |
| w1 | '2' | original | 0 | 1 | ' 2' |
| p1 | '2' | original | 0 | 1 | ' 2' |
| r1 | '2' | original | 0 | 1 | ' 2' |
| w2 | '2' | original | 0 | 1 | ' 2' |
| p2 | '2' | original | 0 | 1 | ' 2' |
| r2 | '2' | original | 0 | 1 | ' 2' |

### P2-L0-0568 (elements): bridge carbon (slot 0) → helium (slot 1); slot 0 carbon (locker 7, attribute 6), slot 1 helium (locker 4, attribute 2), slot 2 oxygen (locker 3, attribute 8), slot 3 lithium (locker 6, attribute 3); informative writes: k = 2, k = 3

**lookup** (PP-L0-0568): O's answer 7, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of carbon is seven. Sam picked lithium. The locker of helium is four. The locker of oxygen is three. Sean picked ⟦bridge:carbon⟧. The locker of lithium is six. Kate picked oxygen.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '7' | - | 0 | 1 | ' 7' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '4' | - | 1 | 0 | ' 4' |
| w1 | '4' | slot_k | 1 | 0 | ' 4' |
| p1 | '4' | slot_k | 1 | 0 | ' 4' |
| r1 | '4' | slot_k | 1 | 0 | ' 4' |
| w2 | '4' | changed | 1 | 0 | ' 4' |
| p2 | '3' | slot_k | 0 | 0 | ' 3' |
| r2 | '4' | changed | 1 | 0 | ' 4' |
| w3 | '4' | changed | 1 | 0 | ' 4' |
| p3 | '3' | other_slot | 0 | 0 | ' 3' |
| r3 | '4' | changed | 1 | 0 | ' 4' |

**recall** (PM-L0-0568): O's answer 6, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of carbon is seven. Sam picked lithium. The locker of helium is four. The locker of oxygen is three. Sean picked ⟦bridge:carbon⟧. The locker of lithium is six. Kate picked oxygen.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '6' | - | 0 | 1 | ' 6' |
| w1 | '8' | other | 0 | 0 | ' 8' |
| p1 | '6' | original | 0 | 1 | ' 6' |
| r1 | '2' | slot_k | 1 | 0 | ' 2' |
| w2 | '8' | slot_k | 0 | 0 | ' 8' |
| p2 | '6' | original | 0 | 1 | ' 6' |
| r2 | '6' | original | 0 | 1 | ' 6' |
| w3 | '8' | other | 0 | 0 | ' 8' |
| p3 | '6' | original | 0 | 1 | ' 6' |
| r3 | '6' | original | 0 | 1 | ' 6' |

### P2-L0-0594 (animals): bridge chicken (slot 3) → lion (slot 0); slot 0 lion (locker 8, attribute 4), slot 1 tick (locker 9, attribute 8), slot 2 owl (locker 6, attribute 2), slot 3 chicken (locker 1, attribute 2); informative writes: k = 1

**lookup** (PP-L0-0594): O's answer 1, S's answer 8; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the lion is eight. The locker of the tick is nine. The locker of the owl is six. The locker of the chicken is one. Sam picked the tick. Iris picked the ⟦bridge:chicken⟧. Emma picked the owl.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '1' | - | 0 | 1 | ' 1' |
| whole | '9' | - | 0 | 0 | ' 9' |
| a1 | '9' | - | 0 | 0 | ' 9' |
| w0 | '9' | other_slot | 0 | 0 | ' 9' |
| p0 | '1' | original | 0 | 1 | ' 1' |
| r0 | '9' | other_slot | 0 | 0 | ' 9' |
| w1 | '9' | slot_k | 0 | 0 | ' 9' |
| p1 | '1' | original | 0 | 1 | ' 1' |
| r1 | '9' | slot_k | 0 | 0 | ' 9' |
| w2 | '9' | other_slot | 0 | 0 | ' 9' |
| p2 | '1' | original | 0 | 1 | ' 1' |
| r2 | '9' | other_slot | 0 | 0 | ' 9' |

**recall** (PM-L0-0594): O's answer 2, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>user
The locker of the lion is eight. The locker of the tick is nine. The locker of the owl is six. The locker of the chicken is one. Sam picked the tick. Iris picked the ⟦bridge:chicken⟧. Emma picked the owl.
How many legs does Iris's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2' |
| whole | '2' | - | 0 | 1 | ' 2' |
| a1 | '2' | - | 0 | 1 | ' 2' |
| w0 | '2' | original | 0 | 1 | ' 2' |
| p0 | '2' | original | 0 | 1 | ' 2' |
| r0 | '2' | original | 0 | 1 | ' 2' |
| w1 | '2' | original | 0 | 1 | ' 2' |
| p1 | '2' | original | 0 | 1 | ' 2' |
| r1 | '2' | original | 0 | 1 | ' 2' |
| w2 | '2' | slot_k | 0 | 1 | ' 2' |
| p2 | '2' | slot_k | 0 | 1 | ' 2' |
| r2 | '2' | slot_k | 0 | 1 | ' 2' |

## muse30_x48_route2: 10 random items of 143 (seed 0)

### P2-L0-0039 (animals): bridge spider (slot 1) → wolf (slot 2); slot 0 rabbit (locker 8, attribute 4), slot 1 spider (locker 2, attribute 8), slot 2 wolf (locker 5, attribute 4), slot 3 bee (locker 9, attribute 6); informative writes: k = 3

**lookup** (PP-L0-0039): O's answer 2, S's answer 5; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Victor picked the rabbit. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the wolf is 5. The locker of the bee is 9. Nina picked the ⟦bridge:spider⟧.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2' |
| whole | '5' | - | 1 | 0 | ' 5' |
| a1 | '5' | - | 1 | 0 | ' 5' |
| w0 | '9' | other_slot | 0 | 0 | ' 9' |
| p0 | '8' | slot_k | 0 | 0 | ' 8' |
| r0 | '5' | changed | 1 | 0 | ' 5' |
| w2 | '5' | slot_k | 1 | 0 | ' 5' |
| p2 | '2' | original | 0 | 1 | ' 2' |
| r2 | '5' | slot_k | 1 | 0 | ' 5' |
| w3 | '9' | slot_k | 0 | 0 | ' 9' |
| p3 | '2' | original | 0 | 1 | ' 2' |
| r3 | '5' | changed | 1 | 0 | ' 5' |

**recall** (PM-L0-0039): O's answer 8, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Victor picked the rabbit. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the wolf is 5. The locker of the bee is 9. Nina picked the ⟦bridge:spider⟧.
How many legs does Nina's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '8' | - | 0 | 1 | ' 8' |
| w0 | '4' | slot_k | 1 | 0 | ' 4' |
| p0 | '6' | other | 0 | 0 | ' 6' |
| r0 | '8' | original | 0 | 1 | ' 8' |
| w2 | '8' | original | 0 | 1 | ' 8' |
| p2 | '8' | original | 0 | 1 | ' 8' |
| r2 | '8' | original | 0 | 1 | ' 8' |
| w3 | '8' | original | 0 | 1 | ' 8' |
| p3 | '8' | original | 0 | 1 | ' 8' |
| r3 | '8' | original | 0 | 1 | ' 8' |

### P2-L0-0253 (elements): bridge oxygen (slot 1) → helium (slot 2); slot 0 lithium (locker 6, attribute 3), slot 1 oxygen (locker 9, attribute 8), slot 2 helium (locker 7, attribute 2), slot 3 hydrogen (locker 5, attribute 1); informative writes: k = 0, k = 3

**lookup** (PP-L0-0253): O's answer 9, S's answer 7; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of lithium is 6. Oscar picked lithium. The locker of oxygen is 9. The locker of helium is 7. The locker of hydrogen is 5. Ivan picked ⟦bridge:oxygen⟧. Mia picked hydrogen.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9' |
| whole | '7' | - | 1 | 0 | ' 7' |
| a1 | '7' | - | 1 | 0 | ' 7' |
| w0 | '6' | slot_k | 0 | 0 | ' 6' |
| p0 | '6' | slot_k | 0 | 0 | ' 6' |
| r0 | '7' | changed | 1 | 0 | ' 7' |
| w2 | '7' | slot_k | 1 | 0 | ' 7' |
| p2 | '9' | original | 0 | 1 | ' 9' |
| r2 | '7' | slot_k | 1 | 0 | ' 7' |
| w3 | '7' | changed | 1 | 0 | ' 7' |
| p3 | '9' | original | 0 | 1 | ' 9' |
| r3 | '7' | changed | 1 | 0 | ' 7' |

**recall** (PM-L0-0253): O's answer 8, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of lithium is 6. Oscar picked lithium. The locker of oxygen is 9. The locker of helium is 7. The locker of hydrogen is 5. Ivan picked ⟦bridge:oxygen⟧. Mia picked hydrogen.
What is the atomic number of Ivan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '8' | - | 0 | 1 | ' 8' |
| w0 | '8' | original | 0 | 1 | ' 8' |
| p0 | '8' | original | 0 | 1 | ' 8' |
| r0 | '8' | original | 0 | 1 | ' 8' |
| w2 | '8' | original | 0 | 1 | ' 8' |
| p2 | '8' | original | 0 | 1 | ' 8' |
| r2 | '2' | slot_k | 1 | 0 | ' 2' |
| w3 | '8' | original | 0 | 1 | ' 8' |
| p3 | '8' | original | 0 | 1 | ' 8' |
| r3 | '8' | original | 0 | 1 | ' 8' |

### P2-L0-0294 (animals): bridge pig (slot 3) → turkey (slot 1); slot 0 bee (locker 9, attribute 6), slot 1 turkey (locker 4, attribute 2), slot 2 bear (locker 6, attribute 4), slot 3 pig (locker 5, attribute 4); informative writes: k = 0

**lookup** (PP-L0-0294): O's answer 5, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 9. The locker of the turkey is 4. The locker of the bear is 6. The locker of the pig is 5. Sean picked the bear. Adam picked the bee. Luke picked the ⟦bridge:pig⟧.
Which locker belongs to Luke's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '5' | - | 0 | 1 | ' 5' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '4' | - | 1 | 0 | ' 4' |
| w0 | '6' | other_slot | 0 | 0 | ' 6' |
| p0 | '9' | slot_k | 0 | 0 | ' 9' |
| r0 | '4' | changed | 1 | 0 | ' 4' |
| w1 | '4' | slot_k | 1 | 0 | ' 4' |
| p1 | '5' | original | 0 | 1 | ' 5' |
| r1 | '4' | slot_k | 1 | 0 | ' 4' |
| w2 | '4' | changed | 1 | 0 | ' 4' |
| p2 | '5' | original | 0 | 1 | ' 5' |
| r2 | '4' | changed | 1 | 0 | ' 4' |

**recall** (PM-L0-0294): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 9. The locker of the turkey is 4. The locker of the bear is 6. The locker of the pig is 5. Sean picked the bear. Adam picked the bee. Luke picked the ⟦bridge:pig⟧.
How many legs does Luke's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '2' | - | 1 | 0 | ' 2' |
| w0 | '2' | changed | 1 | 0 | ' 2' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '2' | changed | 1 | 0 | ' 2' |
| w1 | '2' | slot_k | 1 | 0 | ' 2' |
| p1 | '4' | original | 0 | 1 | ' 4' |
| r1 | '2' | slot_k | 1 | 0 | ' 2' |
| w2 | '2' | changed | 1 | 0 | ' 2' |
| p2 | '4' | slot_k | 0 | 1 | ' 4' |
| r2 | '4' | slot_k | 0 | 1 | ' 4' |

### P2-L0-0367 (elements): bridge hydrogen (slot 0) → fluorine (slot 1); slot 0 hydrogen (locker 6, attribute 1), slot 1 fluorine (locker 3, attribute 9), slot 2 oxygen (locker 9, attribute 8), slot 3 lithium (locker 8, attribute 3); informative writes: k = 2, k = 3

**lookup** (PP-L0-0367): O's answer 6, S's answer 3; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Iris picked oxygen. The locker of hydrogen is 6. The locker of fluorine is 3. The locker of oxygen is 9. Jack picked ⟦bridge:hydrogen⟧. The locker of lithium is 8. Vera picked lithium.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6' |
| whole | '3' | - | 1 | 0 | ' 3' |
| a1 | '3' | - | 1 | 0 | ' 3' |
| w1 | '3' | slot_k | 1 | 0 | ' 3' |
| p1 | '6' | original | 0 | 1 | ' 6' |
| r1 | '3' | slot_k | 1 | 0 | ' 3' |
| w2 | '8' | other_slot | 0 | 0 | ' 8' |
| p2 | '6' | original | 0 | 1 | ' 6' |
| r2 | '3' | changed | 1 | 0 | ' 3' |
| w3 | '8' | slot_k | 0 | 0 | ' 8' |
| p3 | '6' | original | 0 | 1 | ' 6' |
| r3 | '3' | changed | 1 | 0 | ' 3' |

**recall** (PM-L0-0367): O's answer 1, S's answer 9; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Iris picked oxygen. The locker of hydrogen is 6. The locker of fluorine is 3. The locker of oxygen is 9. Jack picked ⟦bridge:hydrogen⟧. The locker of lithium is 8. Vera picked lithium.
What is the atomic number of Jack's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '1' | - | 0 | 1 | ' 1' |
| whole | '9' | - | 1 | 0 | ' 9' |
| a1 | '1' | - | 0 | 1 | ' 1' |
| w1 | '1' | original | 0 | 1 | ' 1' |
| p1 | '1' | original | 0 | 1 | ' 1' |
| r1 | '1' | original | 0 | 1 | ' 1' |
| w2 | '1' | original | 0 | 1 | ' 1' |
| p2 | '1' | original | 0 | 1 | ' 1' |
| r2 | '1' | original | 0 | 1 | ' 1' |
| w3 | '1' | original | 0 | 1 | ' 1' |
| p3 | '1' | original | 0 | 1 | ' 1' |
| r3 | '1' | original | 0 | 1 | ' 1' |

### P2-L0-0399 (animals): bridge deer (slot 2) → duck (slot 1); slot 0 butterfly (locker 5, attribute 6), slot 1 duck (locker 3, attribute 2), slot 2 deer (locker 9, attribute 4), slot 3 goose (locker 6, attribute 2); informative writes: k = 0

**lookup** (PP-L0-0399): O's answer 9, S's answer 3; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the butterfly is five. The locker of the duck is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9' |
| whole | '3' | - | 1 | 0 | ' 3' |
| a1 | '3' | - | 1 | 0 | ' 3' |
| w0 | '5' | slot_k | 0 | 0 | ' 5' |
| p0 | '9' | original | 0 | 1 | ' 9' |
| r0 | '3' | changed | 1 | 0 | ' 3' |
| w1 | '3' | slot_k | 1 | 0 | ' 3' |
| p1 | '9' | original | 0 | 1 | ' 9' |
| r1 | '3' | slot_k | 1 | 0 | ' 3' |
| w3 | '3' | changed | 1 | 0 | ' 3' |
| p3 | '9' | original | 0 | 1 | ' 9' |
| r3 | '3' | changed | 1 | 0 | ' 3' |

**recall** (PM-L0-0399): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the butterfly is five. The locker of the duck is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
How many legs does Tara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '4' | - | 0 | 1 | ' 4' |
| a1 | '4' | - | 0 | 1 | ' 4' |
| w0 | '4' | original | 0 | 1 | ' 4' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '4' | original | 0 | 1 | ' 4' |
| w1 | '4' | original | 0 | 1 | ' 4' |
| p1 | '4' | original | 0 | 1 | ' 4' |
| r1 | '4' | original | 0 | 1 | ' 4' |
| w3 | '4' | original | 0 | 1 | ' 4' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '4' | original | 0 | 1 | ' 4' |

### P2-L0-0420 (animals): bridge wolf (slot 1) → fly (slot 0); slot 0 fly (locker 8, attribute 6), slot 1 wolf (locker 9, attribute 4), slot 2 elephant (locker 1, attribute 4), slot 3 tick (locker 3, attribute 8); informative writes: k = 3

**lookup** (PP-L0-0420): O's answer 9, S's answer 8; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mark picked the elephant. The locker of the fly is eight. The locker of the wolf is nine. Nina picked the tick. The locker of the elephant is one. The locker of the tick is three. Owen picked the ⟦bridge:wolf⟧.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9' |
| whole | '8' | - | 1 | 0 | ' 8' |
| a1 | '8' | - | 1 | 0 | ' 8' |
| w0 | '1' | other_slot | 0 | 0 | ' 1' |
| p0 | '1' | other_slot | 0 | 0 | ' 1' |
| r0 | '8' | slot_k | 1 | 0 | ' 8' |
| w2 | '8' | changed | 1 | 0 | ' 8' |
| p2 | '9' | original | 0 | 1 | ' 9' |
| r2 | '8' | changed | 1 | 0 | ' 8' |
| w3 | '8' | changed | 1 | 0 | ' 8' |
| p3 | '9' | original | 0 | 1 | ' 9' |
| r3 | '8' | changed | 1 | 0 | ' 8' |

**recall** (PM-L0-0420): O's answer 4, S's answer 6; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mark picked the elephant. The locker of the fly is eight. The locker of the wolf is nine. Nina picked the tick. The locker of the elephant is one. The locker of the tick is three. Owen picked the ⟦bridge:wolf⟧.
How many legs does Owen's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '6' | - | 1 | 0 | ' 6' |
| a1 | '8' | - | 0 | 0 | ' 8' |
| w0 | '6' | slot_k | 1 | 0 | ' 4' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '6' | slot_k | 1 | 0 | ' 6' |
| w2 | '6' | changed | 1 | 0 | ' 6' |
| p2 | '4' | slot_k | 0 | 1 | ' 4' |
| r2 | '8' | other | 0 | 0 | ' 8' |
| w3 | '8' | slot_k | 0 | 0 | ' 8' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '8' | slot_k | 0 | 0 | ' 8' |

### P2-L0-0433 (elements): bridge helium (slot 2) → lithium (slot 0); slot 0 lithium (locker 8, attribute 3), slot 1 nitrogen (locker 6, attribute 7), slot 2 helium (locker 4, attribute 2), slot 3 oxygen (locker 3, attribute 8); informative writes: k = 1, k = 3

**lookup** (PP-L0-0433): O's answer 4, S's answer 8; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Vera picked nitrogen. The locker of lithium is eight. The locker of nitrogen is six. The locker of helium is four. The locker of oxygen is three. Hugo picked oxygen. Frank picked ⟦bridge:helium⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '8' | - | 1 | 0 | ' 8' |
| a1 | '8' | - | 1 | 0 | ' 8' |
| w0 | '8' | slot_k | 1 | 0 | ' 8' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '8' | slot_k | 1 | 0 | ' 8' |
| w1 | '8' | changed | 1 | 0 | ' 8' |
| p1 | '4' | original | 0 | 1 | ' 4' |
| r1 | '8' | changed | 1 | 0 | ' 8' |
| w3 | '8' | changed | 1 | 0 | ' 8' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '8' | changed | 1 | 0 | ' 8' |

**recall** (PM-L0-0433): O's answer 2, S's answer 3; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Vera picked nitrogen. The locker of lithium is eight. The locker of nitrogen is six. The locker of helium is four. The locker of oxygen is three. Hugo picked oxygen. Frank picked ⟦bridge:helium⟧.
What is the atomic number of Frank's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2' |
| whole | '3' | - | 1 | 0 | ' 3' |
| a1 | '3' | - | 1 | 0 | ' 3' |
| w0 | '3' | slot_k | 1 | 0 | ' 3' |
| p0 | '2' | original | 0 | 1 | ' 2' |
| r0 | '3' | slot_k | 1 | 0 | ' 3' |
| w1 | '3' | changed | 1 | 0 | ' 3' |
| p1 | '2' | original | 0 | 1 | ' 2' |
| r1 | '3' | changed | 1 | 0 | ' 3' |
| w3 | '3' | changed | 1 | 0 | ' 3' |
| p3 | '2' | original | 0 | 1 | ' 2' |
| r3 | '3' | changed | 1 | 0 | ' 3' |

### P2-L0-0484 (elements): bridge lithium (slot 1) → fluorine (slot 2); slot 0 carbon (locker 8, attribute 6), slot 1 lithium (locker 6, attribute 3), slot 2 fluorine (locker 3, attribute 9), slot 3 helium (locker 5, attribute 2); informative writes: k = 0, k = 3

**lookup** (PP-L0-0484): O's answer 6, S's answer 3; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of carbon is 8. The locker of lithium is 6. Mark picked carbon. The locker of fluorine is 3. The locker of helium is 5. Fiona picked helium. Max picked ⟦bridge:lithium⟧.
Which locker belongs to Max's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6' |
| whole | '3' | - | 1 | 0 | ' 3' |
| a1 | '3' | - | 1 | 0 | ' 3' |
| w0 | '8' | slot_k | 0 | 0 | ' 8' |
| p0 | '8' | slot_k | 0 | 0 | ' 8' |
| r0 | '3' | changed | 1 | 0 | ' 3' |
| w2 | '3' | slot_k | 1 | 0 | ' 3' |
| p2 | '6' | original | 0 | 1 | ' 6' |
| r2 | '3' | slot_k | 1 | 0 | ' 3' |
| w3 | '6' | original | 0 | 1 | ' 6' |
| p3 | '6' | original | 0 | 1 | ' 6' |
| r3 | '3' | changed | 1 | 0 | ' 3' |

**recall** (PM-L0-0484): O's answer 3, S's answer 9; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of carbon is 8. The locker of lithium is 6. Mark picked carbon. The locker of fluorine is 3. The locker of helium is 5. Fiona picked helium. Max picked ⟦bridge:lithium⟧.
What is the atomic number of Max's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '3' | - | 0 | 1 | ' 3' |
| whole | '3' | - | 0 | 1 | ' 3' |
| a1 | '3' | - | 0 | 1 | ' 3' |
| w0 | '6' | slot_k | 0 | 0 | ' 6' |
| p0 | '3' | original | 0 | 1 | ' 3' |
| r0 | '3' | original | 0 | 1 | ' 3' |
| w2 | '3' | original | 0 | 1 | ' 3' |
| p2 | '3' | original | 0 | 1 | ' 3' |
| r2 | '3' | original | 0 | 1 | ' 3' |
| w3 | '3' | original | 0 | 1 | ' 3' |
| p3 | '3' | original | 0 | 1 | ' 3' |
| r3 | '3' | original | 0 | 1 | ' 3' |

### P2-L0-0492 (animals): bridge ant (slot 2) → rabbit (slot 0); slot 0 rabbit (locker 1, attribute 4), slot 1 tick (locker 5, attribute 8), slot 2 ant (locker 9, attribute 6), slot 3 fly (locker 2, attribute 6); informative writes: k = 1

**lookup** (PP-L0-0492): O's answer 9, S's answer 1; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked the tick. The locker of the rabbit is one. The locker of the tick is five. The locker of the ant is nine. The locker of the fly is two. Tara picked the fly. Owen picked the ⟦bridge:ant⟧.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9' |
| whole | '1' | - | 1 | 0 | ' 1' |
| a1 | '9' | - | 0 | 1 | ' 9' |
| w0 | '9' | original | 0 | 1 | ' 9' |
| p0 | '9' | original | 0 | 1 | ' 9' |
| r0 | '9' | original | 0 | 1 | ' 9' |
| w1 | '9' | original | 0 | 1 | ' 9' |
| p1 | '9' | original | 0 | 1 | ' 9' |
| r1 | '9' | original | 0 | 1 | ' 9' |
| w3 | '9' | original | 0 | 1 | ' 9' |
| p3 | '9' | original | 0 | 1 | ' 9' |
| r3 | '9' | original | 0 | 1 | ' 9' |

**recall** (PM-L0-0492): O's answer 6, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked the tick. The locker of the rabbit is one. The locker of the tick is five. The locker of the ant is nine. The locker of the fly is two. Tara picked the fly. Owen picked the ⟦bridge:ant⟧.
How many legs does Owen's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6' |
| whole | '6' | - | 0 | 1 | ' 6' |
| a1 | '6' | - | 0 | 1 | ' 6' |
| w0 | '6' | original | 0 | 1 | ' 6' |
| p0 | '6' | original | 0 | 1 | ' 6' |
| r0 | '6' | original | 0 | 1 | ' 6' |
| w1 | '6' | original | 0 | 1 | ' 6' |
| p1 | '6' | original | 0 | 1 | ' 6' |
| r1 | '6' | original | 0 | 1 | ' 6' |
| w3 | '6' | slot_k | 0 | 1 | ' 6' |
| p3 | '6' | slot_k | 0 | 1 | ' 6' |
| r3 | '6' | slot_k | 0 | 1 | ' 6' |

### P2-L0-0513 (animals): bridge frog (slot 1) → turkey (slot 0); slot 0 turkey (locker 7, attribute 2), slot 1 frog (locker 1, attribute 4), slot 2 lion (locker 6, attribute 4), slot 3 eagle (locker 3, attribute 2); informative writes: 

**lookup** (PP-L0-0513): O's answer 1, S's answer 7; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 7. The locker of the frog is 1. Dan picked the lion. The locker of the lion is 6. Owen picked the ⟦bridge:frog⟧. The locker of the eagle is 3. Eva picked the eagle.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '1' | - | 0 | 1 | ' 1' |
| whole | '7' | - | 1 | 0 | ' 7' |
| a1 | '7' | - | 1 | 0 | ' 7' |
| w0 | '1' | original | 0 | 1 | ' 1' |
| p0 | '7' | slot_k | 1 | 0 | ' 7' |
| r0 | '7' | slot_k | 1 | 0 | ' 7' |
| w2 | '7' | changed | 1 | 0 | ' 7' |
| p2 | '1' | original | 0 | 1 | ' 1' |
| r2 | '7' | changed | 1 | 0 | ' 7' |
| w3 | '7' | changed | 1 | 0 | ' 7' |
| p3 | '1' | original | 0 | 1 | ' 1' |
| r3 | '7' | changed | 1 | 0 | ' 7' |

**recall** (PM-L0-0513): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 7. The locker of the frog is 1. Dan picked the lion. The locker of the lion is 6. Owen picked the ⟦bridge:frog⟧. The locker of the eagle is 3. Eva picked the eagle.
How many legs does Owen's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '4' | - | 0 | 1 | ' 4' |
| a1 | '4' | - | 0 | 1 | ' 4' |
| w0 | '4' | original | 0 | 1 | ' 4' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '4' | original | 0 | 1 | ' 4' |
| w2 | '4' | slot_k | 0 | 1 | ' 4' |
| p2 | '4' | slot_k | 0 | 1 | ' 4' |
| r2 | '4' | slot_k | 0 | 1 | ' 4' |
| w3 | '4' | original | 0 | 1 | ' 4' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '4' | original | 0 | 1 | ' 4' |

