# 48.5 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge token, where every arm is written. UNVERIFIED.

## nem35l_x52_route2_below: 10 random items of 89 (seed 0)

### P2-L0-0039 (animals): bridge spider (slot 1) → wolf (slot 2); slot 0 rabbit (locker 8, attribute 4), slot 1 spider (locker 2, attribute 8), slot 2 wolf (locker 5, attribute 4), slot 3 bee (locker 9, attribute 6); informative writes: k = 3

**lookup** (PP-L0-0039): O's answer 2, S's answer 5; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Victor picked the rabbit. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the wolf is 5. The locker of the bee is 9. Nina picked the ⟦bridge:spider⟧.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '2' | - | 0 | 1 | ' 2' |
| whole | '5' | - | 1 | 0 | ' 5' |
| a1 | '5' | - | 1 | 0 | ' 5' |
| w0 | '5' | changed | 1 | 0 | ' 5' |
| p0 | '8' | slot_k | 0 | 0 | ' 8' |
| r0 | '5' | changed | 1 | 0 | ' 5' |
| w2 | '5' | slot_k | 1 | 0 | ' 5' |
| p2 | '2' | original | 0 | 1 | ' 2' |
| r2 | '5' | slot_k | 1 | 0 | ' 5' |
| w3 | '5' | changed | 1 | 0 | ' 5' |
| p3 | '2' | original | 0 | 1 | ' 2' |
| r3 | '5' | changed | 1 | 0 | ' 5' |

**recall** (PM-L0-0039): O's answer 8, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Victor picked the rabbit. The locker of the rabbit is 8. The locker of the spider is 2. Fiona picked the bee. The locker of the wolf is 5. The locker of the bee is 9. Nina picked the ⟦bridge:spider⟧.
How many legs does Nina's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '8' | - | 0 | 1 | ' 8' |
| w0 | '8' | original | 0 | 1 | ' 8' |
| p0 | '8' | original | 0 | 1 | ' 8' |
| r0 | '8' | original | 0 | 1 | ' 8' |
| w2 | '8' | original | 0 | 1 | ' 8' |
| p2 | '8' | original | 0 | 1 | ' 8' |
| r2 | '8' | original | 0 | 1 | ' 8' |
| w3 | '8' | original | 0 | 1 | ' 8' |
| p3 | '8' | original | 0 | 1 | ' 8' |
| r3 | '8' | original | 0 | 1 | ' 8' |

### P2-L0-0201 (animals): bridge tick (slot 0) → bear (slot 1); slot 0 tick (locker 4, attribute 8), slot 1 bear (locker 5, attribute 4), slot 2 cow (locker 3, attribute 4), slot 3 sheep (locker 8, attribute 4); informative writes: 

**lookup** (PP-L0-0201): O's answer 4, S's answer 5; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the tick is four. The locker of the bear is five. The locker of the cow is three. Clara picked the cow. Emma picked the ⟦bridge:tick⟧. Max picked the sheep. The locker of the sheep is eight.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '5' | - | 1 | 0 | ' 5' |
| a1 | '5' | - | 1 | 0 | ' 5' |
| w1 | '5' | slot_k | 1 | 0 | ' 5' |
| p1 | '5' | slot_k | 1 | 0 | ' 5' |
| r1 | '5' | slot_k | 1 | 0 | ' 5' |
| w2 | '5' | changed | 1 | 0 | ' 5' |
| p2 | '8' | other_slot | 0 | 0 | ' 8' |
| r2 | '5' | changed | 1 | 0 | ' 5' |
| w3 | '8' | slot_k | 0 | 0 | ' 8' |
| p3 | '8' | slot_k | 0 | 0 | ' 8' |
| r3 | '5' | changed | 1 | 0 | ' 5' |

**recall** (PM-L0-0201): O's answer 8, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the tick is four. The locker of the bear is five. The locker of the cow is three. Clara picked the cow. Emma picked the ⟦bridge:tick⟧. Max picked the sheep. The locker of the sheep is eight.
How many legs does Emma's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '4' | - | 1 | 0 | ' 4' |
| w1 | '4' | slot_k | 1 | 0 | ' 4' |
| p1 | '4' | slot_k | 1 | 0 | ' 4' |
| r1 | '4' | slot_k | 1 | 0 | ' 4' |
| w2 | '4' | slot_k | 1 | 0 | ' 4' |
| p2 | '4' | slot_k | 1 | 0 | ' 4' |
| r2 | '4' | slot_k | 1 | 0 | ' 4' |
| w3 | '4' | slot_k | 1 | 0 | ' 4' |
| p3 | '8' | original | 0 | 1 | ' 8' |
| r3 | '4' | slot_k | 1 | 0 | ' 4' |

### P2-L0-0243 (animals): bridge spider (slot 0) → dog (slot 1); slot 0 spider (locker 4, attribute 8), slot 1 dog (locker 7, attribute 4), slot 2 tiger (locker 6, attribute 4), slot 3 sheep (locker 8, attribute 4); informative writes: 

**lookup** (PP-L0-0243): O's answer 4, S's answer 7; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the spider is four. The locker of the dog is seven. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the ⟦bridge:spider⟧. Alice picked the tiger. Henry picked the sheep.
Which locker belongs to Olivia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '7' | - | 1 | 0 | ' 7' |
| a1 | '7' | - | 1 | 0 | ' 7' |
| w1 | '7' | slot_k | 1 | 0 | ' 7' |
| p1 | '7' | slot_k | 1 | 0 | ' 7' |
| r1 | '7' | slot_k | 1 | 0 | ' 7' |
| w2 | '7' | changed | 1 | 0 | ' 7' |
| p2 | '6' | slot_k | 0 | 0 | ' 6' |
| r2 | '7' | changed | 1 | 0 | ' 7' |
| w3 | '8' | slot_k | 0 | 0 | ' 8' |
| p3 | '8' | slot_k | 0 | 0 | ' 8' |
| r3 | '7' | changed | 1 | 0 | ' 7' |

**recall** (PM-L0-0243): O's answer 8, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the spider is four. The locker of the dog is seven. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the ⟦bridge:spider⟧. Alice picked the tiger. Henry picked the sheep.
How many legs does Olivia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '8' | - | 0 | 1 | ' 8' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '4' | - | 1 | 0 | ' 4' |
| w1 | '4' | slot_k | 1 | 0 | ' 4' |
| p1 | '4' | slot_k | 1 | 0 | ' 4' |
| r1 | '4' | slot_k | 1 | 0 | ' 4' |
| w2 | '4' | slot_k | 1 | 0 | ' 4' |
| p2 | '8' | original | 0 | 1 | ' 8' |
| r2 | '4' | slot_k | 1 | 0 | ' 4' |
| w3 | '4' | slot_k | 1 | 0 | ' 4' |
| p3 | '8' | original | 0 | 1 | ' 8' |
| r3 | '4' | slot_k | 1 | 0 | ' 4' |

### P2-L0-0296 (greek): bridge epsilon (slot 3) → theta (slot 0); slot 0 theta (locker 2, attribute 8), slot 1 iota (locker 4, attribute 9), slot 2 alpha (locker 9, attribute 1), slot 3 epsilon (locker 7, attribute 5); informative writes: k = 1, k = 2

**lookup** (PP-L0-0296): O's answer 7, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of theta is two. The locker of iota is four. The locker of alpha is nine. Mia picked iota. The locker of epsilon is seven. Vera picked ⟦bridge:epsilon⟧. Tara picked alpha.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '7' | - | 0 | 1 | ' 7' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '2' | - | 1 | 0 | ' 2' |
| w0 | '2' | slot_k | 1 | 0 | ' 2' |
| p0 | '2' | slot_k | 1 | 0 | ' 2' |
| r0 | '2' | slot_k | 1 | 0 | ' 2' |
| w1 | '2' | changed | 1 | 0 | ' 2' |
| p1 | '7' | original | 0 | 1 | ' 7' |
| r1 | '2' | changed | 1 | 0 | ' 2' |
| w2 | '2' | changed | 1 | 0 | ' 2' |
| p2 | '7' | original | 0 | 1 | ' 7' |
| r2 | '2' | changed | 1 | 0 | ' 2' |

**recall** (PM-L0-0296): O's answer 5, S's answer 8; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of theta is two. The locker of iota is four. The locker of alpha is nine. Mia picked iota. The locker of epsilon is seven. Vera picked ⟦bridge:epsilon⟧. Tara picked alpha.
Which position in the Greek alphabet does Vera's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '5' | - | 0 | 1 | ' 5' |
| whole | '8' | - | 1 | 0 | ' 8' |
| a1 | '5' | - | 0 | 1 | ' 8' |
| w0 | '1' | other | 0 | 0 | ' 8' |
| p0 | '5' | original | 0 | 1 | ' 5' |
| r0 | '5' | original | 0 | 1 | ' 8' |
| w1 | '6' | other | 0 | 0 | ' 6' |
| p1 | '5' | original | 0 | 1 | ' 5' |
| r1 | '5' | original | 0 | 1 | ' 8' |
| w2 | '5' | original | 0 | 1 | ' 8' |
| p2 | '5' | original | 0 | 1 | ' 5' |
| r2 | '8' | changed | 1 | 0 | ' 8' |

### P2-L0-0339 (animals): bridge lion (slot 2) → crow (slot 0); slot 0 crow (locker 3, attribute 2), slot 1 dog (locker 7, attribute 4), slot 2 lion (locker 6, attribute 4), slot 3 eagle (locker 9, attribute 2); informative writes: 

**lookup** (PP-L0-0339): O's answer 6, S's answer 3; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the crow is three. The locker of the dog is seven. The locker of the lion is six. Victor picked the ⟦bridge:lion⟧. Vera picked the dog. The locker of the eagle is nine. Grace picked the eagle.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6' |
| whole | '3' | - | 1 | 0 | ' 3' |
| a1 | '3' | - | 1 | 0 | ' 3' |
| w0 | '3' | slot_k | 1 | 0 | ' 3' |
| p0 | '3' | slot_k | 1 | 0 | ' 3' |
| r0 | '3' | slot_k | 1 | 0 | ' 3' |
| w1 | '3' | changed | 1 | 0 | ' 3' |
| p1 | '6' | original | 0 | 1 | ' 6' |
| r1 | '3' | changed | 1 | 0 | ' 3' |
| w3 | '3' | changed | 1 | 0 | ' 3' |
| p3 | '6' | original | 0 | 1 | ' 6' |
| r3 | '3' | changed | 1 | 0 | ' 3' |

**recall** (PM-L0-0339): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the crow is three. The locker of the dog is seven. The locker of the lion is six. Victor picked the ⟦bridge:lion⟧. Vera picked the dog. The locker of the eagle is nine. Grace picked the eagle.
How many legs does Victor's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '2' | - | 1 | 0 | ' 2' |
| w0 | '3' | other | 0 | 0 | ' 2' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '3' | other | 0 | 0 | ' 2' |
| w1 | '2' | changed | 1 | 0 | ' 2' |
| p1 | '4' | slot_k | 0 | 1 | ' 4' |
| r1 | '2' | changed | 1 | 0 | ' 2' |
| w3 | '2' | slot_k | 1 | 0 | ' 2' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '2' | slot_k | 1 | 0 | ' 2' |

### P2-L0-0357 (animals): bridge wolf (slot 1) → crow (slot 0); slot 0 crow (locker 6, attribute 2), slot 1 wolf (locker 9, attribute 4), slot 2 eagle (locker 7, attribute 2), slot 3 goat (locker 1, attribute 4); informative writes: 

**lookup** (PP-L0-0357): O's answer 9, S's answer 6; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the crow is 6. The locker of the wolf is 9. Leo picked the eagle. The locker of the eagle is 7. Lucy picked the ⟦bridge:wolf⟧. Julia picked the goat. The locker of the goat is 1.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '9' | - | 0 | 1 | ' 9' |
| whole | '6' | - | 1 | 0 | ' 6' |
| a1 | '6' | - | 1 | 0 | ' 6' |
| w0 | '6' | slot_k | 1 | 0 | ' 6' |
| p0 | '9' | original | 0 | 1 | ' 9' |
| r0 | '6' | slot_k | 1 | 0 | ' 6' |
| w2 | '6' | changed | 1 | 0 | ' 6' |
| p2 | '9' | original | 0 | 1 | ' 9' |
| r2 | '6' | changed | 1 | 0 | ' 6' |
| w3 | '6' | changed | 1 | 0 | ' 6' |
| p3 | '9' | original | 0 | 1 | ' 9' |
| r3 | '6' | changed | 1 | 0 | ' 6' |

**recall** (PM-L0-0357): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the crow is 6. The locker of the wolf is 9. Leo picked the eagle. The locker of the eagle is 7. Lucy picked the ⟦bridge:wolf⟧. Julia picked the goat. The locker of the goat is 1.
How many legs does Lucy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '4' | - | 0 | 1 | ' 4' |
| w0 | '2' | slot_k | 1 | 0 | ' 2' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '4' | original | 0 | 1 | ' 4' |
| w2 | '4' | original | 0 | 1 | ' 4' |
| p2 | '4' | original | 0 | 1 | ' 4' |
| r2 | '4' | original | 0 | 1 | ' 4' |
| w3 | '2' | changed | 1 | 0 | ' 2' |
| p3 | '4' | slot_k | 0 | 1 | ' 4' |
| r3 | '2' | changed | 1 | 0 | ' 2' |

### P2-L0-0366 (animals): bridge camel (slot 2) → fly (slot 0); slot 0 fly (locker 2, attribute 6), slot 1 cow (locker 8, attribute 4), slot 2 camel (locker 7, attribute 4), slot 3 goose (locker 5, attribute 2); informative writes: k = 3

**lookup** (PP-L0-0366): O's answer 7, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Noah picked the cow. The locker of the fly is two. The locker of the cow is eight. The locker of the camel is seven. The locker of the goose is five. Eric picked the ⟦bridge:camel⟧. Grace picked the goose.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
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

**recall** (PM-L0-0366): O's answer 4, S's answer 6; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Noah picked the cow. The locker of the fly is two. The locker of the cow is eight. The locker of the camel is seven. The locker of the goose is five. Eric picked the ⟦bridge:camel⟧. Grace picked the goose.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '6' | - | 1 | 0 | ' 6' |
| a1 | '6' | - | 1 | 0 | ' 6' |
| w0 | '4' | original | 0 | 1 | ' 4' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '6' | slot_k | 1 | 0 | ' 6' |
| w1 | '6' | changed | 1 | 0 | ' 6' |
| p1 | '4' | slot_k | 0 | 1 | ' 4' |
| r1 | '6' | changed | 1 | 0 | ' 6' |
| w3 | '6' | changed | 1 | 0 | ' 6' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '6' | changed | 1 | 0 | ' 6' |

### P2-L0-0423 (animals): bridge frog (slot 2) → fly (slot 1); slot 0 fox (locker 7, attribute 4), slot 1 fly (locker 9, attribute 6), slot 2 frog (locker 5, attribute 4), slot 3 spider (locker 4, attribute 8); informative writes: k = 3

**lookup** (PP-L0-0423): O's answer 5, S's answer 9; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Julia picked the fox. Lucy picked the spider. The locker of the fox is seven. The locker of the fly is nine. The locker of the frog is five. Carl picked the ⟦bridge:frog⟧. The locker of the spider is four.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '5' | - | 0 | 1 | ' 5' |
| whole | '9' | - | 1 | 0 | ' 9' |
| a1 | '9' | - | 1 | 0 | ' 9' |
| w0 | '9' | changed | 1 | 0 | ' 9' |
| p0 | '5' | original | 0 | 1 | ' 5' |
| r0 | '9' | changed | 1 | 0 | ' 9' |
| w1 | '9' | slot_k | 1 | 0 | ' 9' |
| p1 | '5' | original | 0 | 1 | ' 5' |
| r1 | '9' | slot_k | 1 | 0 | ' 9' |
| w3 | '5' | original | 0 | 1 | ' 5' |
| p3 | '5' | original | 0 | 1 | ' 5' |
| r3 | '9' | changed | 1 | 0 | ' 9' |

**recall** (PM-L0-0423): O's answer 4, S's answer 6; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Julia picked the fox. Lucy picked the spider. The locker of the fox is seven. The locker of the fly is nine. The locker of the frog is five. Carl picked the ⟦bridge:frog⟧. The locker of the spider is four.
How many legs does Carl's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '6' | - | 1 | 0 | ' 6' |
| a1 | '6' | - | 1 | 0 | ' 6' |
| w0 | '6' | changed | 1 | 0 | ' 6' |
| p0 | '4' | slot_k | 0 | 1 | ' 4' |
| r0 | '6' | changed | 1 | 0 | ' 6' |
| w1 | '6' | slot_k | 1 | 0 | ' 6' |
| p1 | '4' | original | 0 | 1 | ' 4' |
| r1 | '6' | slot_k | 1 | 0 | ' 6' |
| w3 | '4' | original | 0 | 1 | ' 4' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '6' | changed | 1 | 0 | ' 6' |

### P2-L0-0426 (animals): bridge mouse (slot 0) → eagle (slot 2); slot 0 mouse (locker 6, attribute 4), slot 1 ant (locker 1, attribute 6), slot 2 eagle (locker 9, attribute 2), slot 3 crow (locker 7, attribute 2); informative writes: k = 1

**lookup** (PP-L0-0426): O's answer 6, S's answer 9; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the mouse is 6. The locker of the ant is 1. The locker of the eagle is 9. The locker of the crow is 7. David picked the ⟦bridge:mouse⟧. Victor picked the ant. Beth picked the crow.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '6' | - | 0 | 1 | ' 6' |
| whole | '9' | - | 1 | 0 | ' 9' |
| a1 | '9' | - | 1 | 0 | ' 9' |
| w1 | '7' | other_slot | 0 | 0 | ' 7' |
| p1 | '1' | slot_k | 0 | 0 | ' 1' |
| r1 | '9' | changed | 1 | 0 | ' 9' |
| w2 | '7' | other_slot | 0 | 0 | ' 7' |
| p2 | '1' | other_slot | 0 | 0 | ' 1' |
| r2 | '9' | slot_k | 1 | 0 | ' 9' |
| w3 | '7' | slot_k | 0 | 0 | ' 7' |
| p3 | '7' | slot_k | 0 | 0 | ' 7' |
| r3 | '9' | changed | 1 | 0 | ' 9' |

**recall** (PM-L0-0426): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the mouse is 6. The locker of the ant is 1. The locker of the eagle is 9. The locker of the crow is 7. David picked the ⟦bridge:mouse⟧. Victor picked the ant. Beth picked the crow.
How many legs does David's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '2' | - | 1 | 0 | ' 2' |
| w1 | '2' | changed | 1 | 0 | ' 2' |
| p1 | '6' | slot_k | 0 | 0 | ' 6' |
| r1 | '2' | changed | 1 | 0 | ' 2' |
| w2 | '2' | slot_k | 1 | 0 | ' 2' |
| p2 | '6' | other | 0 | 0 | ' 6' |
| r2 | '2' | slot_k | 1 | 0 | ' 2' |
| w3 | '2' | slot_k | 1 | 0 | ' 2' |
| p3 | '2' | slot_k | 1 | 0 | ' 2' |
| r3 | '2' | slot_k | 1 | 0 | ' 2' |

### P2-L0-0435 (animals): bridge camel (slot 2) → crow (slot 0); slot 0 crow (locker 4, attribute 2), slot 1 butterfly (locker 1, attribute 6), slot 2 camel (locker 5, attribute 4), slot 3 eagle (locker 6, attribute 2); informative writes: k = 1

**lookup** (PP-L0-0435): O's answer 5, S's answer 4; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Sam picked the eagle. The locker of the crow is four. The locker of the butterfly is one. The locker of the camel is five. Leo picked the butterfly. Ben picked the ⟦bridge:camel⟧. The locker of the eagle is six.
Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '5' | - | 0 | 1 | ' 5' |
| whole | '4' | - | 1 | 0 | ' 4' |
| a1 | '4' | - | 1 | 0 | ' 4' |
| w0 | '4' | slot_k | 1 | 0 | ' 4' |
| p0 | '5' | original | 0 | 1 | ' 5' |
| r0 | '4' | slot_k | 1 | 0 | ' 4' |
| w1 | '4' | changed | 1 | 0 | ' 4' |
| p1 | '5' | original | 0 | 1 | ' 5' |
| r1 | '4' | changed | 1 | 0 | ' 4' |
| w3 | '4' | changed | 1 | 0 | ' 4' |
| p3 | '5' | original | 0 | 1 | ' 5' |
| r3 | '4' | changed | 1 | 0 | ' 4' |

**recall** (PM-L0-0435): O's answer 4, S's answer 2; the write position is the ⟦bridge:…⟧ token

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Sam picked the eagle. The locker of the crow is four. The locker of the butterfly is one. The locker of the camel is five. Leo picked the butterfly. Ben picked the ⟦bridge:camel⟧. The locker of the eagle is six.
How many legs does Ben's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

| arm | top token | class | switched | right | greedy |
|---|---|---|---|---|---|
| none | '4' | - | 0 | 1 | ' 4' |
| whole | '2' | - | 1 | 0 | ' 2' |
| a1 | '2' | - | 1 | 0 | ' 2' |
| w0 | '2' | slot_k | 1 | 0 | ' 2' |
| p0 | '4' | original | 0 | 1 | ' 4' |
| r0 | '2' | slot_k | 1 | 0 | ' 2' |
| w1 | '2' | changed | 1 | 0 | ' 2' |
| p1 | '4' | original | 0 | 1 | ' 4' |
| r1 | '2' | changed | 1 | 0 | ' 2' |
| w3 | '2' | slot_k | 1 | 0 | ' 2' |
| p3 | '4' | original | 0 | 1 | ' 4' |
| r3 | '2' | slot_k | 1 | 0 | ' 2' |

