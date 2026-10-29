# 49.2 verify pack: S's prompts as the model reads them (the read appends the digit's space token); ⟦bridge:…⟧ rungs 1-6, ⟦mention:…⟧ rung 3 on, ⟦question:…⟧ rung 4 on, every token rungs 5-6. UNVERIFIED.

## qwen3.5-122b-a10b: qwen35_122b_x49_2, 10 random items of 435 (seed 0)

### P2-L0-0029 (greek, locker-after): bridge theta (O) → epsilon (S), token 9

**lookup** (PP-L0-0029): O's answer 4, S's answer 1

```
<|im_start|>user
Luke picked delta. Oscar picked ⟦bridge:epsilon⟧. The locker of theta is four. The locker of iota is five. The locker of ⟦mention:epsilon⟧ is one. The locker of delta is two. Eva picked iota.
⟦question:Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 16 (b) | 1 | ' 1' |
| zero1 | removed: the bridge word, at L | 16 (b) | 1 | ' 1' |
| rand1 | random beside: the bridge word, at L | 16 (b) | 1 | ' 1' |
| zero2 | removed: the bridge word, at L..L+3 | 16 (b) | 1 | ' 1' |
| rand2 | random beside: the bridge word, at L..L+3 | 16 (b) | 1 | ' 1' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 16 (b) | 1 | ' 1' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 16 (b) | 1 | ' 1' |
| zero4 | removed: + the question's tokens, L..L+3 | 16 (b) | 1 | ' 1' |
| rand4 | random beside: + the question's tokens, L..L+3 | 16 (b) | 1 | ' 1' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 16 (b) | 1 | ' 1' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 16 (b) | 1 | ' 1' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 16 (b) | 1 | ' 1' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 16 (b) | 1 | ' 1' |

**recall** (PM-L0-0029): O's answer 8, S's answer 5

```
<|im_start|>user
Luke picked delta. Oscar picked ⟦bridge:epsilon⟧. The locker of theta is four. The locker of iota is five. The locker of ⟦mention:epsilon⟧ is one. The locker of delta is two. Eva picked iota.
⟦question:Which position in the Greek alphabet does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 20 (b) | 1 | ' 5' |
| zero1 | removed: the bridge word, at L | 20 (b) | 1 | ' 5' |
| rand1 | random beside: the bridge word, at L | 20 (b) | 1 | ' 5' |
| zero2 | removed: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5' |
| rand2 | random beside: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5' |
| rand4 | random beside: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5' |

### P2-L0-0186 (animals, locker-after): bridge owl (O) → beetle (S), token 7

**lookup** (PP-L0-0186): O's answer 3, S's answer 2

```
<|im_start|>user
Mia picked the ⟦bridge:beetle⟧. Kyle picked the frog. The locker of the duck is four. The locker of the ⟦mention:beetle⟧ is two. The locker of the owl is three. The locker of the frog is one. Noah picked the duck.
⟦question:Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 17 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 17 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 17 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |

**recall** (PM-L0-0186): O's answer 2, S's answer 6

```
<|im_start|>user
Mia picked the ⟦bridge:beetle⟧. Kyle picked the frog. The locker of the duck is four. The locker of the ⟦mention:beetle⟧ is two. The locker of the owl is three. The locker of the frog is one. Noah picked the duck.
⟦question:How many legs does Mia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 21 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 21 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 21 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6' |

### P2-L0-0281 (greek, locker-after): bridge beta (O) → epsilon (S), token 6

**lookup** (PP-L0-0281): O's answer 5, S's answer 7

```
<|im_start|>user
Eve picked ⟦bridge:epsilon⟧. The locker of ⟦mention:epsilon⟧ is 7. The locker of iota is 8. Jack picked iota. The locker of delta is 6. Finn picked delta. The locker of beta is 5.
⟦question:Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 22 (b) | 1 | ' 7' |
| zero1 | removed: the bridge word, at L | 22 (b) | 1 | ' 7' |
| rand1 | random beside: the bridge word, at L | 22 (b) | 1 | ' 7' |
| zero2 | removed: the bridge word, at L..L+3 | 22 (b) | 1 | ' 7' |
| rand2 | random beside: the bridge word, at L..L+3 | 22 (b) | 1 | ' 7' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 22 (b) | 1 | ' 7' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 22 (b) | 1 | ' 7' |
| zero4 | removed: + the question's tokens, L..L+3 | 22 (b) | 1 | ' 7' |
| rand4 | random beside: + the question's tokens, L..L+3 | 22 (b) | 1 | ' 7' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 22 (b) | 1 | ' 7' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 22 (b) | 1 | ' 7' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 22 (b) | 1 | ' 7' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 22 (b) | 1 | ' 7' |

**recall** (PM-L0-0281): O's answer 2, S's answer 5

```
<|im_start|>user
Eve picked ⟦bridge:epsilon⟧. The locker of ⟦mention:epsilon⟧ is 7. The locker of iota is 8. Jack picked iota. The locker of delta is 6. Finn picked delta. The locker of beta is 5.
⟦question:Which position in the Greek alphabet does Eve's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 20 (b) | 1 | ' 5' |
| zero1 | removed: the bridge word, at L | 20 (b) | 1 | ' 5' |
| rand1 | random beside: the bridge word, at L | 20 (b) | 1 | ' 5' |
| zero2 | removed: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5' |
| rand2 | random beside: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5' |
| rand4 | random beside: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5' |

### P2-L0-0297 (animals, locker-after): bridge ant (O) → goose (S), token 29

**lookup** (PP-L0-0297): O's answer 3, S's answer 4

```
<|im_start|>user
The locker of the crow is 1. The locker of the ant is 3. Emma picked the crow. Alice picked the ⟦bridge:goose⟧. The locker of the ⟦mention:goose⟧ is 4. The locker of the cat is 6. Finn picked the cat.
⟦question:Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 19 (b) | 1 | ' 4' |
| zero1 | removed: the bridge word, at L | 19 (b) | 1 | ' 4' |
| rand1 | random beside: the bridge word, at L | 19 (b) | 1 | ' 4' |
| zero2 | removed: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4' |
| rand2 | random beside: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4' |
| zero4 | removed: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4' |

**recall** (PM-L0-0297): O's answer 6, S's answer 2

```
<|im_start|>user
The locker of the crow is 1. The locker of the ant is 3. Emma picked the crow. Alice picked the ⟦bridge:goose⟧. The locker of the ⟦mention:goose⟧ is 4. The locker of the cat is 6. Finn picked the cat.
⟦question:How many legs does Alice's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 17 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 21 (A) | 0 | ' 6' |
| rand1 | random beside: the bridge word, at L | 17 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 21 (A) | 0 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 21 (A) | 0 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 21 (A) | 0 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (A) | 0 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |

### P2-L0-0310 (elements, locker-after): bridge helium (O) → oxygen (S), token 17

**lookup** (PP-L0-0310): O's answer 5, S's answer 2

```
<|im_start|>user
The locker of carbon is 1. David picked lithium. Victor picked ⟦bridge:oxygen⟧. Eric picked carbon. The locker of lithium is 4. The locker of helium is 5. The locker of ⟦mention:oxygen⟧ is 2.
⟦question:Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 17 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 17 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 17 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |

**recall** (PM-L0-0310): O's answer 2, S's answer 8

```
<|im_start|>user
The locker of carbon is 1. David picked lithium. Victor picked ⟦bridge:oxygen⟧. Eric picked carbon. The locker of lithium is 4. The locker of helium is 5. The locker of ⟦mention:oxygen⟧ is 2.
⟦question:What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 23 (b) | 1 | ' 8' |
| zero1 | removed: the bridge word, at L | 23 (b) | 1 | ' 8' |
| rand1 | random beside: the bridge word, at L | 23 (b) | 1 | ' 8' |
| zero2 | removed: the bridge word, at L..L+3 | 23 (b) | 1 | ' 8' |
| rand2 | random beside: the bridge word, at L..L+3 | 23 (b) | 1 | ' 8' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 23 (b) | 1 | ' 8' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 23 (b) | 1 | ' 8' |
| zero4 | removed: + the question's tokens, L..L+3 | 23 (b) | 1 | ' 8' |
| rand4 | random beside: + the question's tokens, L..L+3 | 23 (b) | 1 | ' 8' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 23 (b) | 1 | ' 8' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 23 (b) | 1 | ' 8' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 23 (b) | 1 | ' 8' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 23 (b) | 1 | ' 8' |

### P2-L0-0349 (elements, locker-after): bridge nitrogen (O) → hydrogen (S), token 6

**lookup** (PP-L0-0349): O's answer 6, S's answer 3

```
<|im_start|>user
Vera picked ⟦bridge:hydrogen⟧. Ruby picked lithium. The locker of nitrogen is six. The locker of ⟦mention:hydrogen⟧ is three. The locker of lithium is nine. The locker of carbon is four. Sean picked carbon.
⟦question:Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 18 (b) | 1 | ' 3' |
| zero1 | removed: the bridge word, at L | 18 (b) | 1 | ' 3' |
| rand1 | random beside: the bridge word, at L | 18 (b) | 1 | ' 3' |
| zero2 | removed: the bridge word, at L..L+3 | 18 (b) | 1 | ' 3' |
| rand2 | random beside: the bridge word, at L..L+3 | 18 (b) | 1 | ' 3' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 18 (b) | 1 | ' 3' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 18 (b) | 1 | ' 3' |
| zero4 | removed: + the question's tokens, L..L+3 | 18 (b) | 1 | ' 3' |
| rand4 | random beside: + the question's tokens, L..L+3 | 18 (b) | 1 | ' 3' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 18 (b) | 1 | ' 3' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 18 (b) | 1 | ' 3' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 18 (b) | 1 | ' 3' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 18 (b) | 1 | ' 3' |

**recall** (PM-L0-0349): O's answer 7, S's answer 1

```
<|im_start|>user
Vera picked ⟦bridge:hydrogen⟧. Ruby picked lithium. The locker of nitrogen is six. The locker of ⟦mention:hydrogen⟧ is three. The locker of lithium is nine. The locker of carbon is four. Sean picked carbon.
⟦question:What is the atomic number of Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 16 (b) | 1 | ' 1' |
| zero1 | removed: the bridge word, at L | 16 (b) | 1 | ' 1' |
| rand1 | random beside: the bridge word, at L | 16 (b) | 1 | ' 1' |
| zero2 | removed: the bridge word, at L..L+3 | 16 (b) | 1 | ' 1' |
| rand2 | random beside: the bridge word, at L..L+3 | 16 (b) | 1 | ' 1' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 16 (b) | 1 | ' 1' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 16 (b) | 1 | ' 1' |
| zero4 | removed: + the question's tokens, L..L+3 | 16 (b) | 1 | ' 1' |
| rand4 | random beside: + the question's tokens, L..L+3 | 16 (b) | 1 | ' 1' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 16 (b) | 1 | ' 1' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 16 (b) | 1 | ' 1' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 16 (b) | 1 | ' 1' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 16 (b) | 1 | ' 1' |

### P2-L0-0368 (greek, locker-after): bridge gamma (O) → epsilon (S), token 23

**lookup** (PP-L0-0368): O's answer 2, S's answer 9

```
<|im_start|>user
The locker of alpha is four. The locker of eta is three. Owen picked alpha. Eva picked ⟦bridge:epsilon⟧. The locker of ⟦mention:epsilon⟧ is nine. The locker of gamma is two. Ivan picked eta.
⟦question:Which locker belongs to Eva's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 24 (b) | 1 | ' 9' |
| zero1 | removed: the bridge word, at L | 24 (b) | 1 | ' 9' |
| rand1 | random beside: the bridge word, at L | 24 (b) | 1 | ' 9' |
| zero2 | removed: the bridge word, at L..L+3 | 24 (b) | 1 | ' 9' |
| rand2 | random beside: the bridge word, at L..L+3 | 24 (b) | 1 | ' 9' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 24 (b) | 1 | ' 9' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 24 (b) | 1 | ' 9' |
| zero4 | removed: + the question's tokens, L..L+3 | 24 (b) | 1 | ' 9' |
| rand4 | random beside: + the question's tokens, L..L+3 | 24 (b) | 1 | ' 9' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 24 (b) | 1 | ' 9' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 24 (b) | 1 | ' 9' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 24 (b) | 1 | ' 9' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 24 (b) | 1 | ' 9' |

**recall** (PM-L0-0368): O's answer 3, S's answer 5

```
<|im_start|>user
The locker of alpha is four. The locker of eta is three. Owen picked alpha. Eva picked ⟦bridge:epsilon⟧. The locker of ⟦mention:epsilon⟧ is nine. The locker of gamma is two. Ivan picked eta.
⟦question:Which position in the Greek alphabet does Eva's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 20 (b) | 1 | ' 5' |
| zero1 | removed: the bridge word, at L | 20 (b) | 1 | ' 5' |
| rand1 | random beside: the bridge word, at L | 20 (b) | 1 | ' 5' |
| zero2 | removed: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5' |
| rand2 | random beside: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5' |
| rand4 | random beside: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5' |

### P2-L0-0541 (elements, locker-first): bridge helium (O) → nitrogen (S), token 37

**lookup** (PP-L0-0541): O's answer 1, S's answer 3

```
<|im_start|>user
The locker of oxygen is five. The locker of ⟦mention:nitrogen⟧ is three. The locker of helium is one. Ruby picked oxygen. The locker of lithium is four. Eric picked ⟦bridge:nitrogen⟧. Tara picked lithium.
⟦question:Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 18 (b) | 1 | ' 3' |
| zero1 | removed: the bridge word, at L | 18 (b) | 1 | ' 3' |
| rand1 | random beside: the bridge word, at L | 18 (b) | 1 | ' 3' |
| zero2 | removed: the bridge word, at L..L+3 | 18 (b) | 1 | ' 3' |
| rand2 | random beside: the bridge word, at L..L+3 | 18 (b) | 1 | ' 3' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 18 (b) | 1 | ' 3' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 18 (b) | 1 | ' 3' |
| zero4 | removed: + the question's tokens, L..L+3 | 18 (b) | 1 | ' 3' |
| rand4 | random beside: + the question's tokens, L..L+3 | 18 (b) | 1 | ' 3' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 18 (b) | 1 | ' 3' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 18 (b) | 1 | ' 3' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 18 (b) | 1 | ' 3' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 18 (b) | 1 | ' 3' |

**recall** (PM-L0-0541): O's answer 2, S's answer 7

```
<|im_start|>user
The locker of oxygen is five. The locker of ⟦mention:nitrogen⟧ is three. The locker of helium is one. Ruby picked oxygen. The locker of lithium is four. Eric picked ⟦bridge:nitrogen⟧. Tara picked lithium.
⟦question:What is the atomic number of Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 22 (b) | 1 | ' 7' |
| zero1 | removed: the bridge word, at L | 22 (b) | 1 | ' 7' |
| rand1 | random beside: the bridge word, at L | 22 (b) | 1 | ' 7' |
| zero2 | removed: the bridge word, at L..L+3 | 22 (b) | 1 | ' 7' |
| rand2 | random beside: the bridge word, at L..L+3 | 22 (b) | 1 | ' 7' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 22 (b) | 1 | ' 7' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 22 (b) | 1 | ' 7' |
| zero4 | removed: + the question's tokens, L..L+3 | 22 (b) | 1 | ' 7' |
| rand4 | random beside: + the question's tokens, L..L+3 | 22 (b) | 1 | ' 7' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 22 (b) | 1 | ' 7' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 22 (b) | 1 | ' 7' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 22 (b) | 1 | ' 7' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 22 (b) | 1 | ' 7' |

### P2-L0-0555 (animals, locker-first): bridge tick (O) → turkey (S), token 42

**lookup** (PP-L0-0555): O's answer 3, S's answer 6

```
<|im_start|>user
The locker of the tick is 3. The locker of the fly is 2. The locker of the ⟦mention:turkey⟧ is 6. The locker of the bear is 9. Kyle picked the ⟦bridge:turkey⟧. Sean picked the fly. Liam picked the bear.
⟦question:Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 21 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 21 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 21 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6' |

**recall** (PM-L0-0555): O's answer 8, S's answer 2

```
<|im_start|>user
The locker of the tick is 3. The locker of the fly is 2. The locker of the ⟦mention:turkey⟧ is 6. The locker of the bear is 9. Kyle picked the ⟦bridge:turkey⟧. Sean picked the fly. Liam picked the bear.
⟦question:How many legs does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 17 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 17 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 17 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |

### P2-L0-0597 (animals, locker-after): bridge goat (O) → duck (S), token 6

**lookup** (PP-L0-0597): O's answer 1, S's answer 6

```
<|im_start|>user
Sam picked the ⟦bridge:duck⟧. The locker of the crow is five. Sean picked the crow. The locker of the ⟦mention:duck⟧ is six. The locker of the dog is nine. Anna picked the dog. The locker of the goat is one.
⟦question:Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 21 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 21 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 21 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (other) | 0 | ' 5' |
| rand4 | random beside: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6' |

**recall** (PM-L0-0597): O's answer 4, S's answer 2

```
<|im_start|>user
Sam picked the ⟦bridge:duck⟧. The locker of the crow is five. Sean picked the crow. The locker of the ⟦mention:duck⟧ is six. The locker of the dog is nine. Anna picked the dog. The locker of the goat is one.
⟦question:How many legs does Sam's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 17 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 17 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 17 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |

