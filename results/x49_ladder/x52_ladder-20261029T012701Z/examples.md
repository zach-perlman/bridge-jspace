# 49.2 verify pack: S's prompts as the model reads them (the read appends the digit's space token); ⟦bridge:…⟧ rungs 1-6, ⟦mention:…⟧ rung 3 on, ⟦question:…⟧ rung 4 on, every token rungs 5-6. UNVERIFIED.

## qwen3.5-9b: qwen35_9b_x49_2, 10 random items of 417 (seed 0)

### P2-L0-0031 (elements, locker-first): bridge oxygen (O) → carbon (S), token 37

**lookup** (PP-L0-0031): O's answer 6, S's answer 5

```
<|im_start|>user
Kyle picked nitrogen. The locker of hydrogen is nine. The locker of ⟦mention:carbon⟧ is five. The locker of nitrogen is four. The locker of oxygen is six. Leo picked ⟦bridge:carbon⟧. David picked hydrogen.
⟦question:Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 20 (b) | 1 | ' 5\n' |
| zero1 | removed: the bridge word, at L | 20 (b) | 1 | ' 5\n' |
| rand1 | random beside: the bridge word, at L | 20 (b) | 1 | ' 5\n' |
| zero2 | removed: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5\n' |

**recall** (PM-L0-0031): O's answer 8, S's answer 6

```
<|im_start|>user
Kyle picked nitrogen. The locker of hydrogen is nine. The locker of ⟦mention:carbon⟧ is five. The locker of nitrogen is four. The locker of oxygen is six. Leo picked ⟦bridge:carbon⟧. David picked hydrogen.
⟦question:What is the atomic number of Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 21 (b) | 1 | ' 6\n' |
| zero1 | removed: the bridge word, at L | 21 (b) | 1 | ' 6\n' |
| rand1 | random beside: the bridge word, at L | 21 (b) | 1 | ' 6\n' |
| zero2 | removed: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (other) | 0 | ' 5\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (other) | 0 | ' 5\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (other) | 0 | ' 5\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6\n' |

### P2-L0-0196 (elements, locker-first): bridge hydrogen (O) → oxygen (S), token 41

**lookup** (PP-L0-0196): O's answer 3, S's answer 6

```
<|im_start|>user
The locker of nitrogen is four. Tara picked nitrogen. The locker of hydrogen is three. The locker of ⟦mention:oxygen⟧ is six. The locker of carbon is five. Mia picked carbon. Finn picked ⟦bridge:oxygen⟧.
⟦question:Which locker belongs to Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 21 (b) | 1 | ' 6\n' |
| zero1 | removed: the bridge word, at L | 21 (b) | 1 | ' 6\n' |
| rand1 | random beside: the bridge word, at L | 21 (b) | 1 | ' 6\n' |
| zero2 | removed: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6\n' |

**recall** (PM-L0-0196): O's answer 1, S's answer 8

```
<|im_start|>user
The locker of nitrogen is four. Tara picked nitrogen. The locker of hydrogen is three. The locker of ⟦mention:oxygen⟧ is six. The locker of carbon is five. Mia picked carbon. Finn picked ⟦bridge:oxygen⟧.
⟦question:What is the atomic number of Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 23 (b) | 1 | ' 8\n' |
| zero1 | removed: the bridge word, at L | 23 (b) | 1 | ' 8\n' |
| rand1 | random beside: the bridge word, at L | 23 (b) | 1 | ' 8\n' |
| zero2 | removed: the bridge word, at L..L+3 | 23 (b) | 1 | ' 8\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 23 (b) | 1 | ' 8\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 23 (b) | 1 | ' 8\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 23 (b) | 1 | ' 8\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 21 (other) | 0 | ' 6\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 23 (b) | 1 | ' 8\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (other) | 0 | ' 6\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 23 (b) | 1 | ' 6\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (other) | 0 | ' 6\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 23 (b) | 1 | ' 8\n' |

### P2-L0-0234 (animals, locker-first): bridge beetle (O) → bear (S), token 52

**lookup** (PP-L0-0234): O's answer 7, S's answer 1

```
<|im_start|>user
Kate picked the elephant. Grace picked the crow. The locker of the ⟦mention:bear⟧ is 1. The locker of the beetle is 7. The locker of the crow is 6. The locker of the elephant is 9. Ivy picked the ⟦bridge:bear⟧.
⟦question:Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 16 (b) | 1 | ' 1\n' |
| zero1 | removed: the bridge word, at L | 16 (b) | 1 | ' 1\n' |
| rand1 | random beside: the bridge word, at L | 16 (b) | 1 | ' 1\n' |
| zero2 | removed: the bridge word, at L..L+3 | 16 (b) | 1 | ' 1\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 16 (b) | 1 | ' 1\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 16 (b) | 1 | ' 1\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 16 (b) | 1 | ' 1\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 16 (b) | 1 | ' 1\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 16 (b) | 1 | ' 1\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 16 (b) | 1 | ' 1\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 16 (b) | 1 | ' 1\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 16 (b) | 1 | ' 1\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 16 (b) | 1 | ' 1\n' |

**recall** (PM-L0-0234): O's answer 6, S's answer 4

```
<|im_start|>user
Kate picked the elephant. Grace picked the crow. The locker of the ⟦mention:bear⟧ is 1. The locker of the beetle is 7. The locker of the crow is 6. The locker of the elephant is 9. Ivy picked the ⟦bridge:bear⟧.
⟦question:How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 19 (b) | 1 | ' 4\n' |
| zero1 | removed: the bridge word, at L | 19 (b) | 1 | ' 4\n' |
| rand1 | random beside: the bridge word, at L | 19 (b) | 1 | ' 4\n' |
| zero2 | removed: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4\n' |

### P2-L0-0293 (greek, locker-first): bridge alpha (O) → delta (S), token 37

**lookup** (PP-L0-0293): O's answer 2, S's answer 5

```
<|im_start|>user
The locker of ⟦mention:delta⟧ is 5. The locker of iota is 8. Ruby picked gamma. The locker of alpha is 2. Emma picked iota. Kate picked ⟦bridge:delta⟧. The locker of gamma is 1.
⟦question:Which locker belongs to Kate's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 20 (b) | 1 | ' 5\n' |
| zero1 | removed: the bridge word, at L | 20 (b) | 1 | ' 5\n' |
| rand1 | random beside: the bridge word, at L | 20 (b) | 1 | ' 5\n' |
| zero2 | removed: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5\n' |

**recall** (PM-L0-0293): O's answer 1, S's answer 4

```
<|im_start|>user
The locker of ⟦mention:delta⟧ is 5. The locker of iota is 8. Ruby picked gamma. The locker of alpha is 2. Emma picked iota. Kate picked ⟦bridge:delta⟧. The locker of gamma is 1.
⟦question:Which position in the Greek alphabet does Kate's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 19 (b) | 1 | ' 4\n' |
| zero1 | removed: the bridge word, at L | 19 (b) | 1 | ' 4\n' |
| rand1 | random beside: the bridge word, at L | 19 (b) | 1 | ' 4\n' |
| zero2 | removed: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 18 (other) | 0 | ' 3\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 18 (other) | 0 | ' 3\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 18 (other) | 0 | ' 3\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 18 (other) | 0 | ' 3\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4\n' |

### P2-L0-0309 (animals, locker-first): bridge beetle (O) → owl (S), token 53

**lookup** (PP-L0-0309): O's answer 2, S's answer 5

```
<|im_start|>user
Oscar picked the bee. The locker of the beetle is 2. The locker of the duck is 1. The locker of the ⟦mention:owl⟧ is 5. The locker of the bee is 4. Peter picked the duck. Dan picked the ⟦bridge:owl⟧.
⟦question:Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 20 (b) | 1 | ' 5\n' |
| zero1 | removed: the bridge word, at L | 20 (b) | 1 | ' 5\n' |
| rand1 | random beside: the bridge word, at L | 20 (b) | 1 | ' 5\n' |
| zero2 | removed: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5\n' |

**recall** (PM-L0-0309): O's answer 6, S's answer 2

```
<|im_start|>user
Oscar picked the bee. The locker of the beetle is 2. The locker of the duck is 1. The locker of the ⟦mention:owl⟧ is 5. The locker of the bee is 4. Peter picked the duck. Dan picked the ⟦bridge:owl⟧.
⟦question:How many legs does Dan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 17 (b) | 1 | ' 2\n' |
| zero1 | removed: the bridge word, at L | 17 (b) | 1 | ' 2\n' |
| rand1 | random beside: the bridge word, at L | 17 (b) | 1 | ' 2\n' |
| zero2 | removed: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 17 (b) | 1 | ' 2\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 17 (b) | 1 | ' 2\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 17 (b) | 1 | ' 2\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (b) | 1 | ' 2\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (other) | 0 | ' 4\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2\n' |

### P2-L0-0317 (greek, locker-first): bridge beta (O) → alpha (S), token 30

**lookup** (PP-L0-0317): O's answer 8, S's answer 9

```
<|im_start|>user
The locker of beta is eight. Ivan picked iota. The locker of ⟦mention:alpha⟧ is nine. The locker of iota is five. Oscar picked ⟦bridge:alpha⟧. The locker of theta is four. Adam picked theta.
⟦question:Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 24 (b) | 1 | ' 9\n' |
| zero1 | removed: the bridge word, at L | 24 (b) | 1 | ' 9\n' |
| rand1 | random beside: the bridge word, at L | 24 (b) | 1 | ' 9\n' |
| zero2 | removed: the bridge word, at L..L+3 | 24 (b) | 1 | ' 9\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 24 (b) | 1 | ' 9\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 24 (b) | 1 | ' 9\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 24 (b) | 1 | ' 9\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 24 (b) | 1 | ' 9\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 24 (b) | 1 | ' 9\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 24 (b) | 1 | ' 9\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 24 (b) | 1 | ' 9\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 24 (b) | 1 | ' 9\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 24 (b) | 1 | ' 9\n' |

**recall** (PM-L0-0317): O's answer 2, S's answer 1

```
<|im_start|>user
The locker of beta is eight. Ivan picked iota. The locker of ⟦mention:alpha⟧ is nine. The locker of iota is five. Oscar picked ⟦bridge:alpha⟧. The locker of theta is four. Adam picked theta.
⟦question:Which position in the Greek alphabet does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 16 (b) | 1 | ' 1\n' |
| zero1 | removed: the bridge word, at L | 16 (b) | 1 | ' 1\n' |
| rand1 | random beside: the bridge word, at L | 16 (b) | 1 | ' 1\n' |
| zero2 | removed: the bridge word, at L..L+3 | 16 (b) | 1 | ' 1\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 16 (b) | 1 | ' 1\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 17 (A) | 0 | ' 2\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 16 (b) | 1 | ' 1\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 17 (A) | 0 | ' 2\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 16 (b) | 1 | ' 1\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 17 (A) | 0 | ' 2\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 16 (b) | 1 | ' 1\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 16 (b) | 1 | ' 1\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 16 (b) | 1 | ' 1\n' |

### P2-L0-0358 (elements, locker-first): bridge hydrogen (O) → nitrogen (S), token 21

**lookup** (PP-L0-0358): O's answer 7, S's answer 5

```
<|im_start|>user
The locker of ⟦mention:nitrogen⟧ is 5. The locker of lithium is 9. Ben picked ⟦bridge:nitrogen⟧. Mia picked oxygen. Ruby picked lithium. The locker of hydrogen is 7. The locker of oxygen is 2.
⟦question:Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 20 (b) | 1 | ' 5\n' |
| zero1 | removed: the bridge word, at L | 20 (b) | 1 | ' 5\n' |
| rand1 | random beside: the bridge word, at L | 20 (b) | 1 | ' 5\n' |
| zero2 | removed: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 20 (b) | 1 | ' 5\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 20 (b) | 1 | ' 5\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (b) | 1 | ' 5\n' |

**recall** (PM-L0-0358): O's answer 1, S's answer 7

```
<|im_start|>user
The locker of ⟦mention:nitrogen⟧ is 5. The locker of lithium is 9. Ben picked ⟦bridge:nitrogen⟧. Mia picked oxygen. Ruby picked lithium. The locker of hydrogen is 7. The locker of oxygen is 2.
⟦question:What is the atomic number of Ben's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 22 (b) | 1 | ' 7\n' |
| zero1 | removed: the bridge word, at L | 22 (b) | 1 | ' 7\n' |
| rand1 | random beside: the bridge word, at L | 22 (b) | 1 | ' 7\n' |
| zero2 | removed: the bridge word, at L..L+3 | 22 (b) | 1 | ' 7\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 22 (b) | 1 | ' 7\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 22 (b) | 1 | ' 7\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 22 (b) | 1 | ' 7\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 22 (b) | 1 | ' 7\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 22 (b) | 1 | ' 7\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 22 (b) | 1 | ' 7\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 22 (b) | 1 | ' 7\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 20 (other) | 0 | ' 5\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 22 (b) | 1 | ' 7\n' |

### P2-L0-0379 (elements, locker-after): bridge hydrogen (O) → oxygen (S), token 13

**lookup** (PP-L0-0379): O's answer 3, S's answer 4

```
<|im_start|>user
Anna picked helium. Sara picked carbon. Finn picked ⟦bridge:oxygen⟧. The locker of hydrogen is three. The locker of carbon is one. The locker of ⟦mention:oxygen⟧ is four. The locker of helium is five.
⟦question:Which locker belongs to Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 19 (b) | 1 | ' 4\n' |
| zero1 | removed: the bridge word, at L | 19 (b) | 1 | ' 4\n' |
| rand1 | random beside: the bridge word, at L | 19 (b) | 1 | ' 4\n' |
| zero2 | removed: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 3\n' |

**recall** (PM-L0-0379): O's answer 1, S's answer 8

```
<|im_start|>user
Anna picked helium. Sara picked carbon. Finn picked ⟦bridge:oxygen⟧. The locker of hydrogen is three. The locker of carbon is one. The locker of ⟦mention:oxygen⟧ is four. The locker of helium is five.
⟦question:What is the atomic number of Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 23 (b) | 1 | ' 8\n' |
| zero1 | removed: the bridge word, at L | 23 (b) | 1 | ' 8\n' |
| rand1 | random beside: the bridge word, at L | 23 (b) | 1 | ' 8\n' |
| zero2 | removed: the bridge word, at L..L+3 | 23 (b) | 1 | ' 8\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 23 (b) | 1 | ' 8\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 23 (b) | 1 | ' 8\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 23 (b) | 1 | ' 8\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 23 (b) | 1 | ' 8\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 23 (b) | 1 | ' 8\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 23 (b) | 1 | ' 8\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 23 (b) | 1 | ' 8\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 23 (b) | 1 | ' 8\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 23 (b) | 1 | ' 8\n' |

### P2-L0-0559 (elements, locker-after): bridge nitrogen (O) → lithium (S), token 21

**lookup** (PP-L0-0559): O's answer 2, S's answer 7

```
<|im_start|>user
The locker of oxygen is 5. Finn picked helium. Tara picked oxygen. Grace picked ⟦bridge:lithium⟧. The locker of ⟦mention:lithium⟧ is 7. The locker of nitrogen is 2. The locker of helium is 6.
⟦question:Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 22 (b) | 1 | ' 7\n' |
| zero1 | removed: the bridge word, at L | 22 (b) | 1 | ' 7\n' |
| rand1 | random beside: the bridge word, at L | 22 (b) | 1 | ' 7\n' |
| zero2 | removed: the bridge word, at L..L+3 | 22 (b) | 1 | ' 7\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 22 (b) | 1 | ' 7\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 22 (b) | 1 | ' 7\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 22 (b) | 1 | ' 7\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 22 (b) | 1 | ' 7\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 22 (b) | 1 | ' 7\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 22 (b) | 1 | ' 7\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 22 (b) | 1 | ' 7\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 22 (b) | 1 | ' 7\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 22 (b) | 1 | ' 7\n' |

**recall** (PM-L0-0559): O's answer 7, S's answer 3

```
<|im_start|>user
The locker of oxygen is 5. Finn picked helium. Tara picked oxygen. Grace picked ⟦bridge:lithium⟧. The locker of ⟦mention:lithium⟧ is 7. The locker of nitrogen is 2. The locker of helium is 6.
⟦question:What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 18 (b) | 1 | ' 3\n' |
| zero1 | removed: the bridge word, at L | 18 (b) | 1 | ' 3\n' |
| rand1 | random beside: the bridge word, at L | 18 (b) | 1 | ' 3\n' |
| zero2 | removed: the bridge word, at L..L+3 | 18 (b) | 1 | ' 3\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 18 (b) | 1 | ' 3\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 18 (b) | 1 | ' 3\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 18 (b) | 1 | ' 3\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 22 (A) | 0 | ' 7\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 18 (b) | 1 | ' 3\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 18 (b) | 1 | ' 7\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 18 (b) | 1 | ' 3\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 18 (b) | 1 | ' 3\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 18 (b) | 1 | ' 3\n' |

### P2-L0-0579 (animals, locker-after): bridge ant (O) → fox (S), token 7

**lookup** (PP-L0-0579): O's answer 4, S's answer 6

```
<|im_start|>user
Ella picked the ⟦bridge:fox⟧. The locker of the ant is 4. The locker of the rabbit is 9. Noah picked the rabbit. Emma picked the goat. The locker of the goat is 2. The locker of the ⟦mention:fox⟧ is 6.
⟦question:Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 21 (b) | 1 | ' 6\n' |
| zero1 | removed: the bridge word, at L | 21 (b) | 1 | ' 6\n' |
| rand1 | random beside: the bridge word, at L | 21 (b) | 1 | ' 6\n' |
| zero2 | removed: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6\n' |

**recall** (PM-L0-0579): O's answer 6, S's answer 4

```
<|im_start|>user
Ella picked the ⟦bridge:fox⟧. The locker of the ant is 4. The locker of the rabbit is 9. Noah picked the rabbit. Emma picked the goat. The locker of the goat is 2. The locker of the ⟦mention:fox⟧ is 6.
⟦question:How many legs does Ella's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 19 (b) | 1 | ' 4\n' |
| zero1 | removed: the bridge word, at L | 19 (b) | 1 | ' 4\n' |
| rand1 | random beside: the bridge word, at L | 19 (b) | 1 | ' 4\n' |
| zero2 | removed: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand2 | random beside: the bridge word, at L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero4 | removed: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4\n' |
| rand4 | random beside: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4\n' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4\n' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4\n' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4\n' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4\n' |

## qwen3.6-27b: x52_ladder_27b_a, 10 random items of 574 (seed 0)

### P2-L0-0045 (animals, locker-first): bridge spider (O) → dog (S), token 32

**lookup** (PP-L0-0045): O's answer 9, S's answer 3

```
<|im_start|>user
The locker of the ⟦mention:dog⟧ is three. The locker of the sheep is seven. Maria picked the sheep. James picked the mouse. Sean picked the ⟦bridge:dog⟧. The locker of the spider is nine. The locker of the mouse is eight.
⟦question:Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0045): O's answer 8, S's answer 4

```
<|im_start|>user
The locker of the ⟦mention:dog⟧ is three. The locker of the sheep is seven. Maria picked the sheep. James picked the mouse. Sean picked the ⟦bridge:dog⟧. The locker of the spider is nine. The locker of the mouse is eight.
⟦question:How many legs does Sean's pick have? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0283 (elements, locker-after): bridge oxygen (O) → carbon (S), token 30

**lookup** (PP-L0-0283): O's answer 6, S's answer 4

```
<|im_start|>user
Eva picked lithium. The locker of lithium is 2. The locker of nitrogen is 8. Liam picked nitrogen. Tara picked ⟦bridge:carbon⟧. The locker of oxygen is 6. The locker of ⟦mention:carbon⟧ is 4.
⟦question:Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0283): O's answer 8, S's answer 6

```
<|im_start|>user
Eva picked lithium. The locker of lithium is 2. The locker of nitrogen is 8. Liam picked nitrogen. Tara picked ⟦bridge:carbon⟧. The locker of oxygen is 6. The locker of ⟦mention:carbon⟧ is 4.
⟦question:What is the atomic number of Tara's pick? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0329 (greek, locker-after): bridge beta (O) → gamma (S), token 29

**lookup** (PP-L0-0329): O's answer 6, S's answer 8

```
<|im_start|>user
The locker of theta is 9. Hugo picked iota. Kate picked theta. The locker of beta is 6. Tom picked ⟦bridge:gamma⟧. The locker of iota is 2. The locker of ⟦mention:gamma⟧ is 8.
⟦question:Which locker belongs to Tom's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0329): O's answer 2, S's answer 3

```
<|im_start|>user
The locker of theta is 9. Hugo picked iota. Kate picked theta. The locker of beta is 6. Tom picked ⟦bridge:gamma⟧. The locker of iota is 2. The locker of ⟦mention:gamma⟧ is 8.
⟦question:Which position in the Greek alphabet does Tom's pick have? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0387 (animals, locker-after): bridge cat (O) → spider (S), token 14

**lookup** (PP-L0-0387): O's answer 6, S's answer 4

```
<|im_start|>user
The locker of the bear is one. Ben picked the ⟦bridge:spider⟧. Ryan picked the duck. Eve picked the bear. The locker of the cat is six. The locker of the duck is three. The locker of the ⟦mention:spider⟧ is four.
⟦question:Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0387): O's answer 4, S's answer 8

```
<|im_start|>user
The locker of the bear is one. Ben picked the ⟦bridge:spider⟧. Ryan picked the duck. Eve picked the bear. The locker of the cat is six. The locker of the duck is three. The locker of the ⟦mention:spider⟧ is four.
⟦question:How many legs does Ben's pick have? Answer with a single digit and nothing else.<|im_end|>
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
| zero4 | removed: + the question's tokens, L..L+3 | 19 (A) | 0 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 23 (b) | 1 | ' 8' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (A) | 0 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 23 (b) | 1 | ' 8' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 15 (other) | 0 | ' 8' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 23 (b) | 1 | ' 8' |

### P2-L0-0415 (elements, locker-after): bridge oxygen (O) → nitrogen (S), token 29

**lookup** (PP-L0-0415): O's answer 3, S's answer 8

```
<|im_start|>user
The locker of helium is 5. Zoe picked helium. The locker of oxygen is 3. Ivan picked lithium. Eva picked ⟦bridge:nitrogen⟧. The locker of lithium is 4. The locker of ⟦mention:nitrogen⟧ is 8.
⟦question:Which locker belongs to Eva's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0415): O's answer 8, S's answer 7

```
<|im_start|>user
The locker of helium is 5. Zoe picked helium. The locker of oxygen is 3. Ivan picked lithium. Eva picked ⟦bridge:nitrogen⟧. The locker of lithium is 4. The locker of ⟦mention:nitrogen⟧ is 8.
⟦question:What is the atomic number of Eva's pick? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0435 (animals, locker-first): bridge camel (O) → owl (S), token 40

**lookup** (PP-L0-0435): O's answer 5, S's answer 4

```
<|im_start|>user
Sam picked the eagle. The locker of the ⟦mention:owl⟧ is four. The locker of the butterfly is one. The locker of the camel is five. Leo picked the butterfly. Ben picked the ⟦bridge:owl⟧. The locker of the eagle is six.
⟦question:Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0435): O's answer 4, S's answer 2

```
<|im_start|>user
Sam picked the eagle. The locker of the ⟦mention:owl⟧ is four. The locker of the butterfly is one. The locker of the camel is five. Leo picked the butterfly. Ben picked the ⟦bridge:owl⟧. The locker of the eagle is six.
⟦question:How many legs does Ben's pick have? Answer with a single digit and nothing else.<|im_end|>
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
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 15 (other) | 0 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 17 (b) | 1 | ' 2' |

### P2-L0-0451 (elements, locker-first): bridge nitrogen (O) → hydrogen (S), token 45

**lookup** (PP-L0-0451): O's answer 3, S's answer 9

```
<|im_start|>user
The locker of oxygen is 2. Mark picked oxygen. The locker of carbon is 1. Oscar picked carbon. The locker of nitrogen is 3. The locker of ⟦mention:hydrogen⟧ is 9. Sam picked ⟦bridge:hydrogen⟧.
⟦question:Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0451): O's answer 7, S's answer 1

```
<|im_start|>user
The locker of oxygen is 2. Mark picked oxygen. The locker of carbon is 1. Oscar picked carbon. The locker of nitrogen is 3. The locker of ⟦mention:hydrogen⟧ is 9. Sam picked ⟦bridge:hydrogen⟧.
⟦question:What is the atomic number of Sam's pick? Answer with a single digit and nothing else.<|im_end|>
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

### P2-L0-0510 (animals, locker-after): bridge bee (O) → fox (S), token 35

**lookup** (PP-L0-0510): O's answer 5, S's answer 7

```
<|im_start|>user
Liam picked the goat. The locker of the bee is 5. Frank picked the ant. The locker of the ant is 1. Eric picked the ⟦bridge:fox⟧. The locker of the ⟦mention:fox⟧ is 7. The locker of the goat is 3.
⟦question:Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0510): O's answer 6, S's answer 4

```
<|im_start|>user
Liam picked the goat. The locker of the bee is 5. Frank picked the ant. The locker of the ant is 1. Eric picked the ⟦bridge:fox⟧. The locker of the ⟦mention:fox⟧ is 7. The locker of the goat is 3.
⟦question:How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
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
| zero4 | removed: + the question's tokens, L..L+3 | 15 (other) | 0 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 19 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 19 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 15 (other) | 0 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 19 (b) | 1 | ' 4' |

### P2-L0-0520 (elements, locker-after): bridge hydrogen (O) → carbon (S), token 21

**lookup** (PP-L0-0520): O's answer 9, S's answer 3

```
<|im_start|>user
The locker of helium is 7. The locker of hydrogen is 9. Rose picked ⟦bridge:carbon⟧. Eric picked lithium. The locker of lithium is 8. The locker of ⟦mention:carbon⟧ is 3. Leo picked helium.
⟦question:Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0520): O's answer 1, S's answer 6

```
<|im_start|>user
The locker of helium is 7. The locker of hydrogen is 9. Rose picked ⟦bridge:carbon⟧. Eric picked lithium. The locker of lithium is 8. The locker of ⟦mention:carbon⟧ is 3. Leo picked helium.
⟦question:What is the atomic number of Rose's pick? Answer with a single digit and nothing else.<|im_end|>
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
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 23 (other) | 0 | ' 8' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 21 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 23 (other) | 0 | ' 8' |
| rand4 | random beside: + the question's tokens, L..L+3 | 21 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 8' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 21 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 21 (b) | 1 | ' 6' |

### P2-L0-0547 (elements, locker-after): bridge nitrogen (O) → carbon (S), token 5

**lookup** (PP-L0-0547): O's answer 1, S's answer 5

```
<|im_start|>user
Emma picked ⟦bridge:carbon⟧. The locker of hydrogen is six. Adam picked oxygen. The locker of ⟦mention:carbon⟧ is five. The locker of oxygen is three. Iris picked hydrogen. The locker of nitrogen is one.
⟦question:Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|im_end|>
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

**recall** (PM-L0-0547): O's answer 7, S's answer 6

```
<|im_start|>user
Emma picked ⟦bridge:carbon⟧. The locker of hydrogen is six. Adam picked oxygen. The locker of ⟦mention:carbon⟧ is five. The locker of oxygen is three. Iris picked hydrogen. The locker of nitrogen is one.
⟦question:What is the atomic number of Emma's pick? Answer with a single digit and nothing else.<|im_end|>
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

## muse-glimmer-30b: muse30_x52_ladder, 10 random items of 409 (seed 0)

### P2-L0-0036 (animals, locker-first): bridge fly (O) → dog (S), token 82

**lookup** (PP-L0-0036): O's answer 2, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦mention:dog⟧ is 6. The locker of the chicken is 4. Noah picked the chicken. Grace picked the sheep. The locker of the fly is 2. Ruby picked the ⟦bridge:dog⟧. The locker of the sheep is 3.
⟦question:Which locker belongs to Ruby's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 34 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 34 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 34 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 34 (b) | 1 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 34 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 34 (b) | 1 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 34 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 34 (b) | 1 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 34 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 34 (b) | 1 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 34 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 34 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 34 (b) | 1 | ' 6' |

**recall** (PM-L0-0036): O's answer 6, S's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦mention:dog⟧ is 6. The locker of the chicken is 4. Noah picked the chicken. Grace picked the sheep. The locker of the fly is 2. Ruby picked the ⟦bridge:dog⟧. The locker of the sheep is 3.
⟦question:How many legs does Ruby's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 32 (b) | 1 | ' 4' |
| zero1 | removed: the bridge word, at L | 32 (b) | 1 | ' 4' |
| rand1 | random beside: the bridge word, at L | 32 (b) | 1 | ' 4' |
| zero2 | removed: the bridge word, at L..L+3 | 32 (b) | 1 | ' 4' |
| rand2 | random beside: the bridge word, at L..L+3 | 32 (b) | 1 | ' 4' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 32 (b) | 1 | ' 4' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 32 (b) | 1 | ' 4' |
| zero4 | removed: + the question's tokens, L..L+3 | 32 (b) | 1 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 32 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 32 (b) | 1 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 32 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 32 (b) | 1 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 32 (b) | 1 | ' 4' |

### P2-L0-0187 (elements, locker-after): bridge hydrogen (O) → fluorine (S), token 56

**lookup** (PP-L0-0187): O's answer 6, S's answer 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. Nina picked ⟦bridge:fluorine⟧. Maria picked helium. The locker of ⟦mention:fluorine⟧ is 8. The locker of hydrogen is 6. The locker of lithium is 2.
⟦question:Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 36 (b) | 1 | ' 8' |
| zero1 | removed: the bridge word, at L | 36 (b) | 1 | ' 8' |
| rand1 | random beside: the bridge word, at L | 36 (b) | 1 | ' 8' |
| zero2 | removed: the bridge word, at L..L+3 | 36 (b) | 1 | ' 8' |
| rand2 | random beside: the bridge word, at L..L+3 | 36 (b) | 1 | ' 8' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 36 (b) | 1 | ' 8' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 36 (b) | 1 | ' 8' |
| zero4 | removed: + the question's tokens, L..L+3 | 36 (b) | 1 | ' 8' |
| rand4 | random beside: + the question's tokens, L..L+3 | 36 (b) | 1 | ' 8' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 36 (b) | 1 | ' 8' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 36 (b) | 1 | ' 8' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 36 (b) | 1 | ' 8' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 36 (b) | 1 | ' 8' |

**recall** (PM-L0-0187): O's answer 1, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. Nina picked ⟦bridge:fluorine⟧. Maria picked helium. The locker of ⟦mention:fluorine⟧ is 8. The locker of hydrogen is 6. The locker of lithium is 2.
⟦question:What is the atomic number of Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 37 (b) | 1 | ' 9' |
| zero1 | removed: the bridge word, at L | 37 (b) | 1 | ' 9' |
| rand1 | random beside: the bridge word, at L | 37 (b) | 1 | ' 9' |
| zero2 | removed: the bridge word, at L..L+3 | 37 (b) | 1 | ' 9' |
| rand2 | random beside: the bridge word, at L..L+3 | 37 (b) | 1 | ' 9' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 37 (b) | 1 | ' 9' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 37 (b) | 1 | ' 9' |
| zero4 | removed: + the question's tokens, L..L+3 | 37 (b) | 1 | ' 9' |
| rand4 | random beside: + the question's tokens, L..L+3 | 37 (b) | 1 | ' 9' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 37 (b) | 1 | ' 9' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 37 (b) | 1 | ' 9' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (b) | 1 | ' 9' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (b) | 1 | ' 9' |

### P2-L0-0224 (greek, locker-after): bridge delta (O) → alpha (S), token 45

**lookup** (PP-L0-0224): O's answer 6, S's answer 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Tara picked ⟦bridge:alpha⟧. The locker of delta is six. The locker of epsilon is seven. Vera picked beta. Max picked epsilon. The locker of beta is four. The locker of ⟦mention:alpha⟧ is five.
⟦question:Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 33 (b) | 1 | ' 5' |
| zero1 | removed: the bridge word, at L | 33 (b) | 1 | ' 5' |
| rand1 | random beside: the bridge word, at L | 33 (b) | 1 | ' 5' |
| zero2 | removed: the bridge word, at L..L+3 | 33 (b) | 1 | ' 5' |
| rand2 | random beside: the bridge word, at L..L+3 | 33 (b) | 1 | ' 5' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 33 (b) | 1 | ' 5' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 33 (b) | 1 | ' 5' |
| zero4 | removed: + the question's tokens, L..L+3 | 33 (b) | 1 | ' 5' |
| rand4 | random beside: + the question's tokens, L..L+3 | 33 (b) | 1 | ' 5' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 33 (b) | 1 | ' 5' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 33 (b) | 1 | ' 5' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 33 (b) | 1 | ' 5' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 33 (b) | 1 | ' 5' |

**recall** (PM-L0-0224): O's answer 4, S's answer 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Tara picked ⟦bridge:alpha⟧. The locker of delta is six. The locker of epsilon is seven. Vera picked beta. Max picked epsilon. The locker of beta is four. The locker of ⟦mention:alpha⟧ is five.
⟦question:Which position in the Greek alphabet does Tara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 29 (b) | 1 | ' 1' |
| zero1 | removed: the bridge word, at L | 29 (b) | 1 | ' 1' |
| rand1 | random beside: the bridge word, at L | 29 (b) | 1 | ' 1' |
| zero2 | removed: the bridge word, at L..L+3 | 29 (b) | 1 | ' 1' |
| rand2 | random beside: the bridge word, at L..L+3 | 29 (b) | 1 | ' 1' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 29 (b) | 1 | ' 1' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 29 (b) | 1 | ' 1' |
| zero4 | removed: + the question's tokens, L..L+3 | 29 (b) | 1 | ' 1' |
| rand4 | random beside: + the question's tokens, L..L+3 | 29 (b) | 1 | ' 1' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 29 (b) | 1 | ' 1' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 29 (b) | 1 | ' 1' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 29 (b) | 1 | ' 1' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 29 (b) | 1 | ' 1' |

### P2-L0-0287 (greek, locker-after): bridge gamma (O) → beta (S), token 62

**lookup** (PP-L0-0287): O's answer 4, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked ⟦bridge:beta⟧. Ryan picked theta. The locker of ⟦mention:beta⟧ is six. The locker of epsilon is eight.
⟦question:Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 34 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 34 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 34 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 34 (b) | 1 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 34 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 34 (b) | 1 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 34 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 34 (b) | 1 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 34 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 34 (b) | 1 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 34 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 34 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 34 (b) | 1 | ' 6' |

**recall** (PM-L0-0287): O's answer 3, S's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked ⟦bridge:beta⟧. Ryan picked theta. The locker of ⟦mention:beta⟧ is six. The locker of epsilon is eight.
⟦question:Which position in the Greek alphabet does Ella's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 30 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 30 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 30 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 30 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 30 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 30 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 30 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 30 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 30 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 30 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 30 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 30 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 30 (b) | 1 | ' 2' |

### P2-L0-0298 (elements, locker-after): bridge hydrogen (O) → fluorine (S), token 62

**lookup** (PP-L0-0298): O's answer 8, S's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked ⟦bridge:fluorine⟧. The locker of ⟦mention:fluorine⟧ is two. The locker of helium is seven. Anna picked nitrogen.
⟦question:Which locker belongs to Ryan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 30 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 30 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 30 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 30 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 30 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 30 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 30 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 30 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 30 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 30 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 30 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 30 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 30 (b) | 1 | ' 2' |

**recall** (PM-L0-0298): O's answer 1, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is eight. Owen picked helium. The locker of nitrogen is five. Ryan picked ⟦bridge:fluorine⟧. The locker of ⟦mention:fluorine⟧ is two. The locker of helium is seven. Anna picked nitrogen.
⟦question:What is the atomic number of Ryan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 37 (b) | 1 | ' 9' |
| zero1 | removed: the bridge word, at L | 37 (b) | 1 | ' 9' |
| rand1 | random beside: the bridge word, at L | 37 (b) | 1 | ' 9' |
| zero2 | removed: the bridge word, at L..L+3 | 37 (b) | 1 | ' 9' |
| rand2 | random beside: the bridge word, at L..L+3 | 37 (b) | 1 | ' 9' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 37 (b) | 1 | ' 9' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 37 (b) | 1 | ' 9' |
| zero4 | removed: + the question's tokens, L..L+3 | 37 (b) | 1 | ' 9' |
| rand4 | random beside: + the question's tokens, L..L+3 | 37 (b) | 1 | ' 9' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 37 (b) | 1 | ' 9' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 37 (b) | 1 | ' 9' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (b) | 1 | ' 9' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (b) | 1 | ' 9' |

### P2-L0-0311 (greek, locker-after): bridge delta (O) → gamma (S), token 55

**lookup** (PP-L0-0311): O's answer 5, S's answer 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of alpha is three. David picked alpha. Laura picked ⟦bridge:gamma⟧. Peter picked beta. The locker of delta is five. The locker of beta is one. The locker of ⟦mention:gamma⟧ is eight.
⟦question:Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 36 (b) | 1 | ' 8' |
| zero1 | removed: the bridge word, at L | 36 (b) | 1 | ' 8' |
| rand1 | random beside: the bridge word, at L | 36 (b) | 1 | ' 8' |
| zero2 | removed: the bridge word, at L..L+3 | 36 (b) | 1 | ' 8' |
| rand2 | random beside: the bridge word, at L..L+3 | 36 (b) | 1 | ' 8' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 36 (b) | 1 | ' 8' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 36 (b) | 1 | ' 8' |
| zero4 | removed: + the question's tokens, L..L+3 | 36 (b) | 1 | ' 8' |
| rand4 | random beside: + the question's tokens, L..L+3 | 36 (b) | 1 | ' 8' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 36 (b) | 1 | ' 8' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 36 (b) | 1 | ' 8' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 36 (b) | 1 | ' 8' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 36 (b) | 1 | ' 8' |

**recall** (PM-L0-0311): O's answer 4, S's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of alpha is three. David picked alpha. Laura picked ⟦bridge:gamma⟧. Peter picked beta. The locker of delta is five. The locker of beta is one. The locker of ⟦mention:gamma⟧ is eight.
⟦question:Which position in the Greek alphabet does Laura's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 31 (b) | 1 | ' 3' |
| zero1 | removed: the bridge word, at L | 31 (b) | 1 | ' 3' |
| rand1 | random beside: the bridge word, at L | 31 (b) | 1 | ' 3' |
| zero2 | removed: the bridge word, at L..L+3 | 35 (other) | 0 | ' 7' |
| rand2 | random beside: the bridge word, at L..L+3 | 31 (b) | 1 | ' 3' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 35 (other) | 0 | ' 7' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 31 (b) | 1 | ' 3' |
| zero4 | removed: + the question's tokens, L..L+3 | 35 (other) | 0 | ' 7' |
| rand4 | random beside: + the question's tokens, L..L+3 | 31 (b) | 1 | ' 3' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 35 (other) | 0 | ' 7' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 31 (b) | 1 | ' 3' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 31 (b) | 1 | ' 3' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 31 (b) | 1 | ' 3' |

### P2-L0-0357 (animals, locker-first): bridge wolf (O) → owl (S), token 77

**lookup** (PP-L0-0357): O's answer 9, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦mention:owl⟧ is 6. The locker of the wolf is 9. Leo picked the eagle. The locker of the eagle is 7. Lucy picked the ⟦bridge:owl⟧. Julia picked the goat. The locker of the goat is 1.
⟦question:Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 34 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 34 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 34 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 34 (b) | 1 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 34 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 34 (b) | 1 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 34 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 34 (b) | 1 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 34 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 34 (b) | 1 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 34 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 34 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 34 (b) | 1 | ' 6' |

**recall** (PM-L0-0357): O's answer 4, S's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦mention:owl⟧ is 6. The locker of the wolf is 9. Leo picked the eagle. The locker of the eagle is 7. Lucy picked the ⟦bridge:owl⟧. Julia picked the goat. The locker of the goat is 1.
⟦question:How many legs does Lucy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 30 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 30 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 30 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 30 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 30 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 30 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 30 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 30 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 30 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 30 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 30 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 30 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 30 (b) | 1 | ' 2' |

### P2-L0-0377 (greek, locker-after): bridge beta (O) → gamma (S), token 52

**lookup** (PP-L0-0377): O's answer 4, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Leo picked delta. Tom picked eta. Anna picked ⟦bridge:gamma⟧. The locker of beta is four. The locker of eta is one. The locker of delta is five. The locker of ⟦mention:gamma⟧ is nine.
⟦question:Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 37 (b) | 1 | ' 9' |
| zero1 | removed: the bridge word, at L | 37 (b) | 1 | ' 9' |
| rand1 | random beside: the bridge word, at L | 37 (b) | 1 | ' 9' |
| zero2 | removed: the bridge word, at L..L+3 | 37 (b) | 1 | ' 9' |
| rand2 | random beside: the bridge word, at L..L+3 | 37 (b) | 1 | ' 9' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 37 (b) | 1 | ' 9' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 37 (b) | 1 | ' 9' |
| zero4 | removed: + the question's tokens, L..L+3 | 37 (b) | 1 | ' 9' |
| rand4 | random beside: + the question's tokens, L..L+3 | 37 (b) | 1 | ' 9' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 37 (b) | 1 | ' 9' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 37 (b) | 1 | ' 9' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (b) | 1 | ' 9' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (b) | 1 | ' 9' |

**recall** (PM-L0-0377): O's answer 2, S's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Leo picked delta. Tom picked eta. Anna picked ⟦bridge:gamma⟧. The locker of beta is four. The locker of eta is one. The locker of delta is five. The locker of ⟦mention:gamma⟧ is nine.
⟦question:Which position in the Greek alphabet does Anna's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 31 (b) | 1 | ' 3' |
| zero1 | removed: the bridge word, at L | 31 (b) | 1 | ' 3' |
| rand1 | random beside: the bridge word, at L | 31 (b) | 1 | ' 3' |
| zero2 | removed: the bridge word, at L..L+3 | 31 (b) | 1 | ' 3' |
| rand2 | random beside: the bridge word, at L..L+3 | 31 (b) | 1 | ' 3' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 31 (b) | 1 | ' 3' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 31 (b) | 1 | ' 3' |
| zero4 | removed: + the question's tokens, L..L+3 | 31 (b) | 1 | ' 3' |
| rand4 | random beside: + the question's tokens, L..L+3 | 31 (b) | 1 | ' 3' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 31 (b) | 1 | ' 3' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 31 (b) | 1 | ' 3' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 31 (b) | 1 | ' 3' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (other) | 0 | ' 3' |

### P2-L0-0573 (animals, locker-after): bridge goose (O) → fox (S), token 51

**lookup** (PP-L0-0573): O's answer 4, S's answer 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Owen picked the lion. Ivy picked the ⟦bridge:fox⟧. The locker of the dog is six. Victor picked the dog. The locker of the goose is four. The locker of the lion is three. The locker of the ⟦mention:fox⟧ is seven.
⟦question:Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 35 (b) | 1 | ' 7' |
| zero1 | removed: the bridge word, at L | 35 (b) | 1 | ' 7' |
| rand1 | random beside: the bridge word, at L | 35 (b) | 1 | ' 7' |
| zero2 | removed: the bridge word, at L..L+3 | 35 (b) | 1 | ' 7' |
| rand2 | random beside: the bridge word, at L..L+3 | 35 (b) | 1 | ' 7' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 35 (b) | 1 | ' 7' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 35 (b) | 1 | ' 7' |
| zero4 | removed: + the question's tokens, L..L+3 | 35 (b) | 1 | ' 7' |
| rand4 | random beside: + the question's tokens, L..L+3 | 35 (b) | 1 | ' 7' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 35 (b) | 1 | ' 7' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 35 (b) | 1 | ' 7' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 35 (b) | 1 | ' 7' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 35 (b) | 1 | ' 7' |

**recall** (PM-L0-0573): O's answer 2, S's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Owen picked the lion. Ivy picked the ⟦bridge:fox⟧. The locker of the dog is six. Victor picked the dog. The locker of the goose is four. The locker of the lion is three. The locker of the ⟦mention:fox⟧ is seven.
⟦question:How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 32 (b) | 1 | ' 4' |
| zero1 | removed: the bridge word, at L | 32 (b) | 1 | ' 4' |
| rand1 | random beside: the bridge word, at L | 32 (b) | 1 | ' 4' |
| zero2 | removed: the bridge word, at L..L+3 | 32 (b) | 1 | ' 4' |
| rand2 | random beside: the bridge word, at L..L+3 | 32 (b) | 1 | ' 4' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 32 (b) | 1 | ' 4' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 32 (b) | 1 | ' 4' |
| zero4 | removed: + the question's tokens, L..L+3 | 32 (b) | 1 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 32 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 32 (b) | 1 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 32 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 32 (b) | 1 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 32 (b) | 1 | ' 4' |

### P2-L0-0588 (animals, locker-first): bridge cow (O) → butterfly (S), token 77

**lookup** (PP-L0-0588): O's answer 5, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦mention:butterfly⟧ is 9. The locker of the cow is 5. Mia picked the tiger. The locker of the tiger is 6. Ben picked the ⟦bridge:butterfly⟧. Kate picked the spider. The locker of the spider is 4.
⟦question:Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 37 (b) | 1 | ' 9' |
| zero1 | removed: the bridge word, at L | 37 (b) | 1 | ' 9' |
| rand1 | random beside: the bridge word, at L | 37 (b) | 1 | ' 9' |
| zero2 | removed: the bridge word, at L..L+3 | 37 (b) | 1 | ' 9' |
| rand2 | random beside: the bridge word, at L..L+3 | 37 (b) | 1 | ' 9' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 37 (b) | 1 | ' 9' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 37 (b) | 1 | ' 9' |
| zero4 | removed: + the question's tokens, L..L+3 | 37 (b) | 1 | ' 9' |
| rand4 | random beside: + the question's tokens, L..L+3 | 37 (b) | 1 | ' 9' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 37 (b) | 1 | ' 9' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 37 (b) | 1 | ' 9' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (b) | 1 | ' 9' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 37 (b) | 1 | ' 9' |

**recall** (PM-L0-0588): O's answer 4, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦mention:butterfly⟧ is 9. The locker of the cow is 5. Mia picked the tiger. The locker of the tiger is 6. Ben picked the ⟦bridge:butterfly⟧. Kate picked the spider. The locker of the spider is 4.
⟦question:How many legs does Ben's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 34 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 34 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 34 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 34 (b) | 1 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 34 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 34 (b) | 1 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 34 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 34 (b) | 1 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 34 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 34 (b) | 1 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 34 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 34 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 34 (b) | 1 | ' 6' |

