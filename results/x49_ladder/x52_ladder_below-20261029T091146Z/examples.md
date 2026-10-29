# 49.2 verify pack: S's prompts as the model reads them (the read appends the digit's space token); ⟦bridge:…⟧ rungs 1-6, ⟦mention:…⟧ rung 3 on, ⟦question:…⟧ rung 4 on, every token rungs 5-6. UNVERIFIED.

## nemotron-3.5-lightning: nem35l_x52_ladder_below, 10 random items of 295 (seed 0)

### P2-L0-0044 (greek, locker-after): bridge epsilon (O) → beta (S), token 17

**lookup** (PP-L0-0044): O's answer 3, S's answer 4

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of epsilon is three. Grace picked ⟦bridge:beta⟧. Sara picked theta. Oscar picked delta. The locker of theta is seven. The locker of delta is nine. The locker of ⟦mention:beta⟧ is four.
⟦question:Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1052 (b) | 1 | ' 4' |
| zero1 | removed: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| rand1 | random beside: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| zero2 | removed: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| rand2 | random beside: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero4 | removed: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |

**recall** (PM-L0-0044): O's answer 5, S's answer 2

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of epsilon is three. Grace picked ⟦bridge:beta⟧. Sara picked theta. Oscar picked delta. The locker of theta is seven. The locker of delta is nine. The locker of ⟦mention:beta⟧ is four.
⟦question:Which position in the Greek alphabet does Grace's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1050 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 1050 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 1050 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 1053 (A) | 0 | ' 5' |
| rand2 | random beside: the bridge word, at L..L+3 | 1050 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1053 (A) | 0 | ' 5' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1050 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 1053 (A) | 0 | ' 5' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1050 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1053 (A) | 0 | ' 5' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1050 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1050 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1050 (b) | 1 | ' 2' |

### P2-L0-0265 (elements, locker-after): bridge hydrogen (O) → boron (S), token 11

**lookup** (PP-L0-0265): O's answer 3, S's answer 4

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Fiona picked ⟦bridge:boron⟧. Eric picked oxygen. The locker of lithium is seven. The locker of hydrogen is three. The locker of ⟦mention:boron⟧ is four. The locker of oxygen is six. Mia picked lithium.
⟦question:Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1052 (b) | 1 | ' 4' |
| zero1 | removed: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| rand1 | random beside: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| zero2 | removed: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| rand2 | random beside: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero4 | removed: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |

**recall** (PM-L0-0265): O's answer 1, S's answer 5

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Fiona picked ⟦bridge:boron⟧. Eric picked oxygen. The locker of lithium is seven. The locker of hydrogen is three. The locker of ⟦mention:boron⟧ is four. The locker of oxygen is six. Mia picked lithium.
⟦question:What is the atomic number of Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1053 (b) | 1 | ' 5' |
| zero1 | removed: the bridge word, at L | 1053 (b) | 1 | ' 5' |
| rand1 | random beside: the bridge word, at L | 1053 (b) | 1 | ' 5' |
| zero2 | removed: the bridge word, at L..L+3 | 1053 (b) | 1 | ' 5' |
| rand2 | random beside: the bridge word, at L..L+3 | 1053 (b) | 1 | ' 5' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1052 (other) | 0 | ' 4' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1053 (b) | 1 | ' 5' |
| zero4 | removed: + the question's tokens, L..L+3 | 1052 (other) | 0 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1053 (b) | 1 | ' 5' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (other) | 0 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1053 (b) | 1 | ' 5' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1053 (b) | 1 | ' 5' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1053 (b) | 1 | ' 5' |

### P2-L0-0323 (greek, locker-after): bridge eta (O) → beta (S), token 11

**lookup** (PP-L0-0323): O's answer 1, S's answer 6

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Lily picked ⟦bridge:beta⟧. Mia picked theta. The locker of theta is 9. Julia picked alpha. The locker of ⟦mention:beta⟧ is 6. The locker of eta is 1. The locker of alpha is 8.
⟦question:Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1054 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 1054 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 1054 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 1054 (b) | 1 | ' 6' |
| rand2 | random beside: the bridge word, at L..L+3 | 1054 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1054 (b) | 1 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1054 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 1054 (b) | 1 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1054 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1054 (b) | 1 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1054 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1054 (b) | 1 | ' 6.' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1054 (b) | 1 | ' 6' |

**recall** (PM-L0-0323): O's answer 7, S's answer 2

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Lily picked ⟦bridge:beta⟧. Mia picked theta. The locker of theta is 9. Julia picked alpha. The locker of ⟦mention:beta⟧ is 6. The locker of eta is 1. The locker of alpha is 8.
⟦question:Which position in the Greek alphabet does Lily's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1050 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 1050 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 1050 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 1050 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 1050 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1050 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1050 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 1050 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1050 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1050 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1050 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1050 (b) | 1 | ' 2.' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1050 (b) | 1 | ' 2' |

### P2-L0-0370 (elements, locker-after): bridge helium (O) → fluorine (S), token 10

**lookup** (PP-L0-0370): O's answer 9, S's answer 1

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Sam picked ⟦bridge:fluorine⟧. The locker of helium is nine. The locker of nitrogen is three. Eve picked lithium. The locker of lithium is five. The locker of ⟦mention:fluorine⟧ is one. Amy picked nitrogen.
⟦question:Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1049 (b) | 1 | ' 1' |
| zero1 | removed: the bridge word, at L | 1049 (b) | 1 | ' 1' |
| rand1 | random beside: the bridge word, at L | 1049 (b) | 1 | ' 1' |
| zero2 | removed: the bridge word, at L..L+3 | 1049 (b) | 1 | ' 1' |
| rand2 | random beside: the bridge word, at L..L+3 | 1049 (b) | 1 | ' 1' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1049 (b) | 1 | ' 1' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1049 (b) | 1 | ' 1' |
| zero4 | removed: + the question's tokens, L..L+3 | 1049 (b) | 1 | ' 1' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1049 (b) | 1 | ' 1' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1049 (b) | 1 | ' 1' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1049 (b) | 1 | ' 1' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1049 (b) | 1 | ' 1' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1049 (b) | 1 | ' 1' |

**recall** (PM-L0-0370): O's answer 2, S's answer 9

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Sam picked ⟦bridge:fluorine⟧. The locker of helium is nine. The locker of nitrogen is three. Eve picked lithium. The locker of lithium is five. The locker of ⟦mention:fluorine⟧ is one. Amy picked nitrogen.
⟦question:What is the atomic number of Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1057 (b) | 1 | ' 9' |
| zero1 | removed: the bridge word, at L | 1057 (b) | 1 | ' 9' |
| rand1 | random beside: the bridge word, at L | 1057 (b) | 1 | ' 9' |
| zero2 | removed: the bridge word, at L..L+3 | 1049 (other) | 0 | ' 1' |
| rand2 | random beside: the bridge word, at L..L+3 | 1057 (b) | 1 | ' 9' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1049 (other) | 0 | ' 1' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1057 (b) | 1 | ' 9' |
| zero4 | removed: + the question's tokens, L..L+3 | 1049 (other) | 0 | ' 1' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1057 (b) | 1 | ' 9' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1049 (other) | 0 | ' 1' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1057 (b) | 1 | ' 9' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1049 (other) | 0 | ' 9.' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1057 (b) | 1 | ' 9' |

### P2-L0-0396 (animals, locker-after): bridge spider (O) → wolf (S), token 29

**lookup** (PP-L0-0396): O's answer 2, S's answer 1

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the eagle is 9. The locker of the spider is 2. Oscar picked the ⟦bridge:wolf⟧. Lucy picked the eagle. The locker of the ⟦mention:wolf⟧ is 1. The locker of the goose is 4. Mia picked the goose.
⟦question:Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1049 (b) | 1 | ' 1' |
| zero1 | removed: the bridge word, at L | 1049 (b) | 1 | ' 1' |
| rand1 | random beside: the bridge word, at L | 1049 (b) | 1 | ' 1' |
| zero2 | removed: the bridge word, at L..L+3 | 1049 (b) | 1 | ' 1' |
| rand2 | random beside: the bridge word, at L..L+3 | 1049 (b) | 1 | ' 1' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1049 (b) | 1 | ' 1' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1049 (b) | 1 | ' 1' |
| zero4 | removed: + the question's tokens, L..L+3 | 1049 (b) | 1 | ' 1' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1049 (b) | 1 | ' 1' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1049 (b) | 1 | ' 1' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1049 (b) | 1 | ' 1' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1049 (b) | 1 | ' 1' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1049 (b) | 1 | ' 1' |

**recall** (PM-L0-0396): O's answer 8, S's answer 4

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the eagle is 9. The locker of the spider is 2. Oscar picked the ⟦bridge:wolf⟧. Lucy picked the eagle. The locker of the ⟦mention:wolf⟧ is 1. The locker of the goose is 4. Mia picked the goose.
⟦question:How many legs does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1052 (b) | 1 | ' 4' |
| zero1 | removed: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| rand1 | random beside: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| zero2 | removed: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| rand2 | random beside: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero4 | removed: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |

### P2-L0-0408 (animals, locker-after): bridge fly (O) → bear (S), token 25

**lookup** (PP-L0-0408): O's answer 9, S's answer 2

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Paul picked the deer. The locker of the fly is 9. Anna picked the ⟦bridge:bear⟧. The locker of the tick is 4. Laura picked the tick. The locker of the deer is 5. The locker of the ⟦mention:bear⟧ is 2.
⟦question:Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1050 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 1050 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 1050 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 1050 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 1050 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1050 (b) | 1 | ' 2' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1050 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 1050 (b) | 1 | ' 2' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1050 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1050 (b) | 1 | ' 2' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1050 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1050 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1050 (b) | 1 | ' 2' |

**recall** (PM-L0-0408): O's answer 6, S's answer 4

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Paul picked the deer. The locker of the fly is 9. Anna picked the ⟦bridge:bear⟧. The locker of the tick is 4. Laura picked the tick. The locker of the deer is 5. The locker of the ⟦mention:bear⟧ is 2.
⟦question:How many legs does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1052 (b) | 1 | ' 4' |
| zero1 | removed: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| rand1 | random beside: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| zero2 | removed: the bridge word, at L..L+3 | 1056 (other) | 0 | ' 8' |
| rand2 | random beside: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1056 (other) | 0 | ' 8' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero4 | removed: + the question's tokens, L..L+3 | 1056 (other) | 0 | ' 8' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1056 (other) | 0 | ' 8' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |

### P2-L0-0426 (animals, locker-first): bridge mouse (O) → eagle (S), token 47

**lookup** (PP-L0-0426): O's answer 6, S's answer 9

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the mouse is 6. The locker of the ant is 1. The locker of the ⟦mention:eagle⟧ is 9. The locker of the crow is 7. David picked the ⟦bridge:eagle⟧. Victor picked the ant. Beth picked the crow.
⟦question:Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1057 (b) | 1 | ' 9' |
| zero1 | removed: the bridge word, at L | 1057 (b) | 1 | ' 9' |
| rand1 | random beside: the bridge word, at L | 1057 (b) | 1 | ' 9' |
| zero2 | removed: the bridge word, at L..L+3 | 1057 (b) | 1 | ' 9' |
| rand2 | random beside: the bridge word, at L..L+3 | 1057 (b) | 1 | ' 9' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1057 (b) | 1 | ' 9' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1057 (b) | 1 | ' 9' |
| zero4 | removed: + the question's tokens, L..L+3 | 1057 (b) | 1 | ' 9' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1057 (b) | 1 | ' 9' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1057 (b) | 1 | ' 9' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1057 (b) | 1 | ' 9' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1057 (b) | 1 | ' 9.' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1057 (b) | 1 | ' 9' |

**recall** (PM-L0-0426): O's answer 4, S's answer 2

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the mouse is 6. The locker of the ant is 1. The locker of the ⟦mention:eagle⟧ is 9. The locker of the crow is 7. David picked the ⟦bridge:eagle⟧. Victor picked the ant. Beth picked the crow.
⟦question:How many legs does David's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1050 (b) | 1 | ' 2' |
| zero1 | removed: the bridge word, at L | 1050 (b) | 1 | ' 2' |
| rand1 | random beside: the bridge word, at L | 1050 (b) | 1 | ' 2' |
| zero2 | removed: the bridge word, at L..L+3 | 1050 (b) | 1 | ' 2' |
| rand2 | random beside: the bridge word, at L..L+3 | 1050 (b) | 1 | ' 2' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1054 (other) | 0 | ' 6' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1050 (b) | 1 | ' 2' |
| zero4 | removed: + the question's tokens, L..L+3 | 1054 (other) | 0 | ' 6' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1050 (b) | 1 | ' 2' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1054 (other) | 0 | ' 6' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1050 (b) | 1 | ' 2' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1050 (b) | 1 | ' 2' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1050 (b) | 1 | ' 2' |

### P2-L0-0487 (elements, locker-after): bridge oxygen (O) → lithium (S), token 17

**lookup** (PP-L0-0487): O's answer 1, S's answer 8

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of oxygen is one. Jack picked ⟦bridge:lithium⟧. Ivan picked helium. Julia picked hydrogen. The locker of hydrogen is nine. The locker of helium is three. The locker of ⟦mention:lithium⟧ is eight.
⟦question:Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1056 (b) | 1 | ' 8' |
| zero1 | removed: the bridge word, at L | 1056 (b) | 1 | ' 8' |
| rand1 | random beside: the bridge word, at L | 1056 (b) | 1 | ' 8' |
| zero2 | removed: the bridge word, at L..L+3 | 1056 (b) | 1 | ' 8' |
| rand2 | random beside: the bridge word, at L..L+3 | 1056 (b) | 1 | ' 8' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1056 (b) | 1 | ' 8' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1056 (b) | 1 | ' 8' |
| zero4 | removed: + the question's tokens, L..L+3 | 1056 (b) | 1 | ' 8' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1056 (b) | 1 | ' 8' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1056 (b) | 1 | ' 8' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1056 (b) | 1 | ' 8' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1056 (b) | 1 | ' 8' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1056 (b) | 1 | ' 8' |

**recall** (PM-L0-0487): O's answer 8, S's answer 3

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of oxygen is one. Jack picked ⟦bridge:lithium⟧. Ivan picked helium. Julia picked hydrogen. The locker of hydrogen is nine. The locker of helium is three. The locker of ⟦mention:lithium⟧ is eight.
⟦question:What is the atomic number of Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1051 (b) | 1 | ' 3' |
| zero1 | removed: the bridge word, at L | 1051 (b) | 1 | ' 3' |
| rand1 | random beside: the bridge word, at L | 1051 (b) | 1 | ' 3' |
| zero2 | removed: the bridge word, at L..L+3 | 1056 (A) | 0 | ' 8' |
| rand2 | random beside: the bridge word, at L..L+3 | 1051 (b) | 1 | ' 3' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1056 (A) | 0 | ' 8' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1051 (b) | 1 | ' 3' |
| zero4 | removed: + the question's tokens, L..L+3 | 1056 (A) | 0 | ' 8' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1051 (b) | 1 | ' 3' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1056 (A) | 0 | ' 8' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1051 (b) | 1 | ' 3' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1051 (b) | 1 | ' 3' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1051 (b) | 1 | ' 3' |

### P2-L0-0497 (greek, locker-after): bridge theta (O) → zeta (S), token 18

**lookup** (PP-L0-0497): O's answer 3, S's answer 4

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of epsilon is 9. Kate picked ⟦bridge:zeta⟧. The locker of iota is 1. Eva picked epsilon. Sam picked iota. The locker of ⟦mention:zeta⟧ is 4. The locker of theta is 3.
⟦question:Which locker belongs to Kate's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1052 (b) | 1 | ' 4' |
| zero1 | removed: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| rand1 | random beside: the bridge word, at L | 1052 (b) | 1 | ' 4' |
| zero2 | removed: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| rand2 | random beside: the bridge word, at L..L+3 | 1052 (b) | 1 | ' 4' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero4 | removed: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1052 (b) | 1 | ' 4' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1052 (b) | 1 | ' 4' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4.' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1052 (b) | 1 | ' 4' |

**recall** (PM-L0-0497): O's answer 8, S's answer 6

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of epsilon is 9. Kate picked ⟦bridge:zeta⟧. The locker of iota is 1. Eva picked epsilon. Sam picked iota. The locker of ⟦mention:zeta⟧ is 4. The locker of theta is 3.
⟦question:Which position in the Greek alphabet does Kate's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1054 (b) | 1 | ' 6' |
| zero1 | removed: the bridge word, at L | 1054 (b) | 1 | ' 6' |
| rand1 | random beside: the bridge word, at L | 1054 (b) | 1 | ' 6' |
| zero2 | removed: the bridge word, at L..L+3 | 1055 (other) | 0 | ' 7' |
| rand2 | random beside: the bridge word, at L..L+3 | 1054 (b) | 1 | ' 6' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1056 (A) | 0 | ' 8' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1054 (b) | 1 | ' 6' |
| zero4 | removed: + the question's tokens, L..L+3 | 1055 (other) | 0 | ' 7' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1054 (b) | 1 | ' 6' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1055 (other) | 0 | ' 7' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1054 (b) | 1 | ' 6' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1054 (b) | 1 | ' 6' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1054 (b) | 1 | ' 6' |

### P2-L0-0521 (greek, locker-after): bridge beta (O) → epsilon (S), token 11

**lookup** (PP-L0-0521): O's answer 4, S's answer 9

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Diana picked ⟦bridge:epsilon⟧. Kate picked delta. The locker of iota is 5. Anna picked iota. The locker of ⟦mention:epsilon⟧ is 9. The locker of delta is 3. The locker of beta is 4.
⟦question:Which locker belongs to Diana's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1057 (b) | 1 | ' 9' |
| zero1 | removed: the bridge word, at L | 1057 (b) | 1 | ' 9' |
| rand1 | random beside: the bridge word, at L | 1057 (b) | 1 | ' 9' |
| zero2 | removed: the bridge word, at L..L+3 | 1057 (b) | 1 | ' 9' |
| rand2 | random beside: the bridge word, at L..L+3 | 1057 (b) | 1 | ' 9' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1057 (b) | 1 | ' 9' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1057 (b) | 1 | ' 9' |
| zero4 | removed: + the question's tokens, L..L+3 | 1057 (b) | 1 | ' 9' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1057 (b) | 1 | ' 9' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1057 (b) | 1 | ' 9' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1057 (b) | 1 | ' 9' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1057 (b) | 1 | ' 9.' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1057 (b) | 1 | ' 9' |

**recall** (PM-L0-0521): O's answer 2, S's answer 5

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Diana picked ⟦bridge:epsilon⟧. Kate picked delta. The locker of iota is 5. Anna picked iota. The locker of ⟦mention:epsilon⟧ is 9. The locker of delta is 3. The locker of beta is 4.
⟦question:Which position in the Greek alphabet does Diana's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: ⟧
```

| arm | what | top token | kept S's | greedy |
|---|---|---|---|---|
| none | S unedited | 1053 (b) | 1 | ' 5' |
| zero1 | removed: the bridge word, at L | 1053 (b) | 1 | ' 5' |
| rand1 | random beside: the bridge word, at L | 1053 (b) | 1 | ' 5' |
| zero2 | removed: the bridge word, at L..L+3 | 1053 (b) | 1 | ' 5' |
| rand2 | random beside: the bridge word, at L..L+3 | 1053 (b) | 1 | ' 5' |
| zero3 | removed: + the item's mention in its locker sentence, L..L+3 | 1053 (b) | 1 | ' 5' |
| rand3 | random beside: + the item's mention in its locker sentence, L..L+3 | 1053 (b) | 1 | ' 5' |
| zero4 | removed: + the question's tokens, L..L+3 | 1053 (b) | 1 | ' 5' |
| rand4 | random beside: + the question's tokens, L..L+3 | 1053 (b) | 1 | ' 5' |
| zero5 | removed: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1053 (b) | 1 | ' 5' |
| rand5 | random beside: every token, L..L+3: the projection on the same 25 atoms (the bridge's change) at every token | 1053 (b) | 1 | ' 5' |
| zero6 | removed: every token, Zach's band: his top-10 lens directions per token (his code path) | 1053 (b) | 1 | ' 5.' |
| rand6 | random beside: every token, Zach's band: his top-10 lens directions per token (his code path) | 1053 (b) | 1 | ' 5' |

