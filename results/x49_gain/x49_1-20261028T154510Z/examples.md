# 49.1 verify pack: O's prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the bridge word, where each arm adds its vector at L. UNVERIFIED.

## qwen3.5-9b: qwen35_9b_x49_1, 10 random items of 75 (seed 0)

### P2-L0-0018 (animals): bridge eagle (O) → butterfly (S), token 43

**lookup** (PP-L0-0018): O's answer 4, S's answer 5

O, as read:

```
<|im_start|>user
The locker of the butterfly is 5. Sara picked the butterfly. Rose picked the fox. The locker of the eagle is 4. The locker of the fox is 3. Jack picked the⟦ eagle⟧.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4\n' |
| J(0,0.5) | '4' | 0 | ' 4\n' |
| J(0,1) | '5' | 1 | ' 5\n' |
| J(0,1.5) | '5' | 1 | ' 5\n' |
| J(0,2) | '5' | 1 | ' 5\n' |
| J(0.5,0) | '4' | 0 | ' 4\n' |
| J(0.5,0.5) | '5' | 1 | ' 5\n' |
| J(0.5,1) | '5' | 1 | ' 5\n' |
| J(0.5,1.5) | '5' | 1 | ' 5\n' |
| J(0.5,2) | '5' | 1 | ' 5\n' |
| J(1,0) | '4' | 0 | ' 4\n' |
| J(1,0.5) | '5' | 1 | ' 5\n' |
| J(1,1) | '5' | 1 | ' 5\n' |
| J(1,1.5) | '5' | 1 | ' 5\n' |
| J(1,2) | '5' | 1 | ' 5\n' |
| J(1.5,0) | '4' | 0 | ' 4\n' |
| J(1.5,0.5) | '5' | 1 | ' 5\n' |
| J(1.5,1) | '5' | 1 | ' 5\n' |
| J(1.5,1.5) | '5' | 1 | ' 5\n' |
| J(1.5,2) | '5' | 1 | ' 5\n' |
| J(2,0) | '4' | 0 | ' 4\n' |
| J(2,0.5) | '5' | 1 | ' 5\n' |
| J(2,1) | '5' | 1 | ' 5\n' |
| J(2,1.5) | '5' | 1 | ' 5\n' |
| J(2,2) | '5' | 1 | ' 5\n' |
| R(0,1) | '5' | 1 | ' 5\n' |
| R(1,0) | '4' | 0 | ' 4\n' |
| R(2,0) | '4' | 0 | ' 4\n' |
| R(0,2) | '5' | 1 | ' 5\n' |
| J(0,2)-U | '3' | 0 | ' 3\n' |
| J(0,2)-RU | '5' | 1 | ' 5\n' |
| J100(0,1) | '5' | 1 | ' 5\n' |
| J100(1,0) | '4' | 0 | ' 4\n' |
| J100(2,0) | '5' | 1 | ' 5\n' |
| J100(0,2) | '5' | 1 | ' 5\n' |
| R100(0,1) | '5' | 1 | ' 5\n' |
| R100(1,0) | '4' | 0 | ' 4\n' |
| R100(2,0) | '5' | 1 | ' 5\n' |
| R100(0,2) | '5' | 1 | ' 5\n' |

**recall** (PM-L0-0018): O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the butterfly is 5. Sara picked the butterfly. Rose picked the fox. The locker of the eagle is 4. The locker of the fox is 3. Jack picked the⟦ eagle⟧.
How many legs does Jack's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2\n' |
| J(0,0.5) | '2' | 0 | ' 2\n' |
| J(0,1) | '6' | 1 | ' 6\n' |
| J(0,1.5) | '6' | 1 | ' 6\n' |
| J(0,2) | '6' | 1 | ' 6\n' |
| J(0.5,0) | '2' | 0 | ' 2\n' |
| J(0.5,0.5) | '6' | 1 | ' 6\n' |
| J(0.5,1) | '6' | 1 | ' 6\n' |
| J(0.5,1.5) | '6' | 1 | ' 6\n' |
| J(0.5,2) | '6' | 1 | ' 6\n' |
| J(1,0) | '2' | 0 | ' 2\n' |
| J(1,0.5) | '6' | 1 | ' 6\n' |
| J(1,1) | '6' | 1 | ' 6\n' |
| J(1,1.5) | '6' | 1 | ' 6\n' |
| J(1,2) | '6' | 1 | ' 6\n' |
| J(1.5,0) | '6' | 1 | ' 6\n' |
| J(1.5,0.5) | '6' | 1 | ' 6\n' |
| J(1.5,1) | '6' | 1 | ' 6\n' |
| J(1.5,1.5) | '6' | 1 | ' 6\n' |
| J(1.5,2) | '6' | 1 | ' 6\n' |
| J(2,0) | '6' | 1 | ' 6\n' |
| J(2,0.5) | '6' | 1 | ' 6\n' |
| J(2,1) | '6' | 1 | ' 6\n' |
| J(2,1.5) | '6' | 1 | ' 6\n' |
| J(2,2) | '6' | 1 | ' 6\n' |
| R(0,1) | '6' | 1 | ' 6\n' |
| R(1,0) | '2' | 0 | ' 2\n' |
| R(2,0) | '6' | 1 | ' 6\n' |
| R(0,2) | '6' | 1 | ' 6\n' |
| J(0,2)-U | '6' | 1 | ' 6\n' |
| J(0,2)-RU | '6' | 1 | ' 6\n' |
| J100(0,1) | '6' | 1 | ' 6\n' |
| J100(1,0) | '6' | 1 | ' 6\n' |
| J100(2,0) | '6' | 1 | ' 6\n' |
| J100(0,2) | '6' | 1 | ' 6\n' |
| R100(0,1) | '6' | 1 | ' 6\n' |
| R100(1,0) | '2' | 0 | ' 2\n' |
| R100(2,0) | '6' | 1 | ' 6\n' |
| R100(0,2) | '6' | 1 | ' 6\n' |

### P2-L0-0114 (animals): bridge goose (O) → mouse (S), token 43

**lookup** (PP-L0-0114): O's answer 3, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the mouse is 6. James picked the mouse. Eric picked the beetle. The locker of the beetle is 8. The locker of the goose is 3. Oscar picked the⟦ goose⟧.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3\n' |
| J(0,0.5) | '3' | 0 | ' 3\n' |
| J(0,1) | '6' | 1 | ' 6\n' |
| J(0,1.5) | '6' | 1 | ' 6\n' |
| J(0,2) | '6' | 1 | ' 6\n' |
| J(0.5,0) | '3' | 0 | ' 3\n' |
| J(0.5,0.5) | '3' | 0 | ' 3\n' |
| J(0.5,1) | '6' | 1 | ' 6\n' |
| J(0.5,1.5) | '6' | 1 | ' 6\n' |
| J(0.5,2) | '6' | 1 | ' 6\n' |
| J(1,0) | '3' | 0 | ' 3\n' |
| J(1,0.5) | '6' | 1 | ' 6\n' |
| J(1,1) | '6' | 1 | ' 6\n' |
| J(1,1.5) | '6' | 1 | ' 6\n' |
| J(1,2) | '6' | 1 | ' 6\n' |
| J(1.5,0) | '3' | 0 | ' 3\n' |
| J(1.5,0.5) | '6' | 1 | ' 6\n' |
| J(1.5,1) | '6' | 1 | ' 6\n' |
| J(1.5,1.5) | '6' | 1 | ' 6\n' |
| J(1.5,2) | '6' | 1 | ' 6\n' |
| J(2,0) | '3' | 0 | ' 3\n' |
| J(2,0.5) | '6' | 1 | ' 6\n' |
| J(2,1) | '6' | 1 | ' 6\n' |
| J(2,1.5) | '6' | 1 | ' 6\n' |
| J(2,2) | '6' | 1 | ' 6\n' |
| R(0,1) | '6' | 1 | ' 6\n' |
| R(1,0) | '3' | 0 | ' 3\n' |
| R(2,0) | '3' | 0 | ' 3\n' |
| R(0,2) | '6' | 1 | ' 6\n' |
| J(0,2)-U | '3' | 0 | ' 3\n' |
| J(0,2)-RU | '6' | 1 | ' 6\n' |
| J100(0,1) | '6' | 1 | ' 6\n' |
| J100(1,0) | '3' | 0 | ' 3\n' |
| J100(2,0) | '6' | 1 | ' 6\n' |
| J100(0,2) | '6' | 1 | ' 6\n' |
| R100(0,1) | '6' | 1 | ' 6\n' |
| R100(1,0) | '3' | 0 | ' 3\n' |
| R100(2,0) | '6' | 1 | ' 6\n' |
| R100(0,2) | '6' | 1 | ' 6\n' |

**recall** (PM-L0-0114): O's answer 2, S's answer 4

O, as read:

```
<|im_start|>user
The locker of the mouse is 6. James picked the mouse. Eric picked the beetle. The locker of the beetle is 8. The locker of the goose is 3. Oscar picked the⟦ goose⟧.
How many legs does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2\n' |
| J(0,0.5) | '2' | 0 | ' 2\n' |
| J(0,1) | '4' | 1 | ' 4\n' |
| J(0,1.5) | '4' | 1 | ' 4\n' |
| J(0,2) | '4' | 1 | ' 4\n' |
| J(0.5,0) | '2' | 0 | ' 2\n' |
| J(0.5,0.5) | '4' | 1 | ' 4\n' |
| J(0.5,1) | '4' | 1 | ' 4\n' |
| J(0.5,1.5) | '4' | 1 | ' 4\n' |
| J(0.5,2) | '4' | 1 | ' 4\n' |
| J(1,0) | '2' | 0 | ' 2\n' |
| J(1,0.5) | '4' | 1 | ' 4\n' |
| J(1,1) | '4' | 1 | ' 4\n' |
| J(1,1.5) | '4' | 1 | ' 4\n' |
| J(1,2) | '4' | 1 | ' 4\n' |
| J(1.5,0) | '2' | 0 | ' 2\n' |
| J(1.5,0.5) | '4' | 1 | ' 4\n' |
| J(1.5,1) | '4' | 1 | ' 4\n' |
| J(1.5,1.5) | '4' | 1 | ' 4\n' |
| J(1.5,2) | '4' | 1 | ' 4\n' |
| J(2,0) | '2' | 0 | ' 2\n' |
| J(2,0.5) | '4' | 1 | ' 4\n' |
| J(2,1) | '4' | 1 | ' 4\n' |
| J(2,1.5) | '4' | 1 | ' 4\n' |
| J(2,2) | '4' | 1 | ' 4\n' |
| R(0,1) | '4' | 1 | ' 4\n' |
| R(1,0) | '2' | 0 | ' 2\n' |
| R(2,0) | '2' | 0 | ' 2\n' |
| R(0,2) | '4' | 1 | ' 4\n' |
| J(0,2)-U | '4' | 1 | ' 4\n' |
| J(0,2)-RU | '2' | 0 | ' 2\n' |
| J100(0,1) | '4' | 1 | ' 4\n' |
| J100(1,0) | '4' | 1 | ' 4\n' |
| J100(2,0) | '4' | 1 | ' 4\n' |
| J100(0,2) | '4' | 1 | ' 4\n' |
| R100(0,1) | '4' | 1 | ' 4\n' |
| R100(1,0) | '2' | 0 | ' 2\n' |
| R100(2,0) | '4' | 1 | ' 4\n' |
| R100(0,2) | '4' | 1 | ' 4\n' |

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
| J(0,0) | '7' | 0 | ' 7\n' |
| J(0,0.5) | '7' | 0 | ' 7\n' |
| J(0,1) | '4' | 1 | ' 4\n' |
| J(0,1.5) | '4' | 1 | ' 4\n' |
| J(0,2) | '4' | 1 | ' 4\n' |
| J(0.5,0) | '7' | 0 | ' 7\n' |
| J(0.5,0.5) | '7' | 0 | ' 7\n' |
| J(0.5,1) | '4' | 1 | ' 4\n' |
| J(0.5,1.5) | '4' | 1 | ' 4\n' |
| J(0.5,2) | '4' | 1 | ' 4\n' |
| J(1,0) | '7' | 0 | ' 7\n' |
| J(1,0.5) | '7' | 0 | ' 7\n' |
| J(1,1) | '4' | 1 | ' 4\n' |
| J(1,1.5) | '4' | 1 | ' 4\n' |
| J(1,2) | '4' | 1 | ' 4\n' |
| J(1.5,0) | '7' | 0 | ' 7\n' |
| J(1.5,0.5) | '4' | 1 | ' 4\n' |
| J(1.5,1) | '4' | 1 | ' 4\n' |
| J(1.5,1.5) | '4' | 1 | ' 4\n' |
| J(1.5,2) | '4' | 1 | ' 4\n' |
| J(2,0) | '7' | 0 | ' 7\n' |
| J(2,0.5) | '4' | 1 | ' 4\n' |
| J(2,1) | '4' | 1 | ' 4\n' |
| J(2,1.5) | '4' | 1 | ' 4\n' |
| J(2,2) | '4' | 1 | ' 4\n' |
| R(0,1) | '4' | 1 | ' 4\n' |
| R(1,0) | '7' | 0 | ' 7\n' |
| R(2,0) | '7' | 0 | ' 7\n' |
| R(0,2) | '4' | 1 | ' 4\n' |
| J(0,2)-U | '5' | 0 | ' 5\n' |
| J(0,2)-RU | '4' | 1 | ' 4\n' |
| J100(0,1) | '7' | 0 | ' 7\n' |
| J100(1,0) | '7' | 0 | ' 7\n' |
| J100(2,0) | '4' | 1 | ' 4\n' |
| J100(0,2) | '4' | 1 | ' 4\n' |
| R100(0,1) | '7' | 0 | ' 7\n' |
| R100(1,0) | '7' | 0 | ' 7\n' |
| R100(2,0) | '4' | 1 | ' 4\n' |
| R100(0,2) | '4' | 1 | ' 4\n' |

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
| J(0,0) | '2' | 0 | ' 2\n' |
| J(0,0.5) | '2' | 0 | ' 2\n' |
| J(0,1) | '6' | 1 | ' 6\n' |
| J(0,1.5) | '6' | 1 | ' 6\n' |
| J(0,2) | '6' | 1 | ' 6\n' |
| J(0.5,0) | '2' | 0 | ' 2\n' |
| J(0.5,0.5) | '2' | 0 | ' 2\n' |
| J(0.5,1) | '6' | 1 | ' 6\n' |
| J(0.5,1.5) | '6' | 1 | ' 6\n' |
| J(0.5,2) | '6' | 1 | ' 6\n' |
| J(1,0) | '6' | 1 | ' 6\n' |
| J(1,0.5) | '6' | 1 | ' 6\n' |
| J(1,1) | '6' | 1 | ' 6\n' |
| J(1,1.5) | '6' | 1 | ' 6\n' |
| J(1,2) | '6' | 1 | ' 6\n' |
| J(1.5,0) | '6' | 1 | ' 6\n' |
| J(1.5,0.5) | '6' | 1 | ' 6\n' |
| J(1.5,1) | '6' | 1 | ' 6\n' |
| J(1.5,1.5) | '6' | 1 | ' 6\n' |
| J(1.5,2) | '6' | 1 | ' 6\n' |
| J(2,0) | '6' | 1 | ' 6\n' |
| J(2,0.5) | '6' | 1 | ' 6\n' |
| J(2,1) | '6' | 1 | ' 6\n' |
| J(2,1.5) | '6' | 1 | ' 6\n' |
| J(2,2) | '6' | 1 | ' 6\n' |
| R(0,1) | '6' | 1 | ' 6\n' |
| R(1,0) | '2' | 0 | ' 2\n' |
| R(2,0) | '6' | 1 | ' 6\n' |
| R(0,2) | '6' | 1 | ' 6\n' |
| J(0,2)-U | '6' | 1 | ' 6\n' |
| J(0,2)-RU | '6' | 1 | ' 6\n' |
| J100(0,1) | '2' | 0 | ' 2\n' |
| J100(1,0) | '6' | 1 | ' 6\n' |
| J100(2,0) | '6' | 1 | ' 6\n' |
| J100(0,2) | '6' | 1 | ' 6\n' |
| R100(0,1) | '2' | 0 | ' 2\n' |
| R100(1,0) | '2' | 0 | ' 2\n' |
| R100(2,0) | '6' | 1 | ' 6\n' |
| R100(0,2) | '6' | 1 | ' 6\n' |

### P2-L0-0180 (animals): bridge beetle (O) → eagle (S), token 32

**lookup** (PP-L0-0180): O's answer 7, S's answer 3

O, as read:

```
<|im_start|>user
The locker of the eagle is three. Ivy picked the bear. Emma picked the eagle. The locker of the beetle is seven. Olivia picked the⟦ beetle⟧. The locker of the bear is one.
Which locker belongs to Olivia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '7' | 0 | ' 7\n' |
| J(0,0.5) | '7' | 0 | ' 7\n' |
| J(0,1) | '3' | 1 | ' 3\n' |
| J(0,1.5) | '3' | 1 | ' 3\n' |
| J(0,2) | '3' | 1 | ' 3\n' |
| J(0.5,0) | '7' | 0 | ' 7\n' |
| J(0.5,0.5) | '7' | 0 | ' 7\n' |
| J(0.5,1) | '3' | 1 | ' 3\n' |
| J(0.5,1.5) | '3' | 1 | ' 3\n' |
| J(0.5,2) | '3' | 1 | ' 3\n' |
| J(1,0) | '7' | 0 | ' 7\n' |
| J(1,0.5) | '3' | 1 | ' 3\n' |
| J(1,1) | '3' | 1 | ' 3\n' |
| J(1,1.5) | '3' | 1 | ' 3\n' |
| J(1,2) | '3' | 1 | ' 3\n' |
| J(1.5,0) | '7' | 0 | ' 7\n' |
| J(1.5,0.5) | '3' | 1 | ' 3\n' |
| J(1.5,1) | '3' | 1 | ' 3\n' |
| J(1.5,1.5) | '3' | 1 | ' 3\n' |
| J(1.5,2) | '3' | 1 | ' 3\n' |
| J(2,0) | '7' | 0 | ' 7\n' |
| J(2,0.5) | '3' | 1 | ' 3\n' |
| J(2,1) | '3' | 1 | ' 3\n' |
| J(2,1.5) | '3' | 1 | ' 3\n' |
| J(2,2) | '3' | 1 | ' 3\n' |
| R(0,1) | '3' | 1 | ' 3\n' |
| R(1,0) | '7' | 0 | ' 7\n' |
| R(2,0) | '7' | 0 | ' 7\n' |
| R(0,2) | '3' | 1 | ' 3\n' |
| J(0,2)-U | '7' | 0 | ' 7\n' |
| J(0,2)-RU | '3' | 1 | ' 3\n' |
| J100(0,1) | '7' | 0 | ' 7\n' |
| J100(1,0) | '7' | 0 | ' 7\n' |
| J100(2,0) | '3' | 1 | ' 3\n' |
| J100(0,2) | '3' | 1 | ' 3\n' |
| R100(0,1) | '3' | 1 | ' 3\n' |
| R100(1,0) | '7' | 0 | ' 7\n' |
| R100(2,0) | '3' | 1 | ' 3\n' |
| R100(0,2) | '3' | 1 | ' 3\n' |

**recall** (PM-L0-0180): O's answer 6, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the eagle is three. Ivy picked the bear. Emma picked the eagle. The locker of the beetle is seven. Olivia picked the⟦ beetle⟧. The locker of the bear is one.
How many legs does Olivia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6\n' |
| J(0,0.5) | '6' | 0 | ' 6\n' |
| J(0,1) | '2' | 1 | ' 2\n' |
| J(0,1.5) | '2' | 1 | ' 2\n' |
| J(0,2) | '2' | 1 | ' 2\n' |
| J(0.5,0) | '6' | 0 | ' 6\n' |
| J(0.5,0.5) | '6' | 0 | ' 6\n' |
| J(0.5,1) | '2' | 1 | ' 2\n' |
| J(0.5,1.5) | '2' | 1 | ' 2\n' |
| J(0.5,2) | '2' | 1 | ' 2\n' |
| J(1,0) | '6' | 0 | ' 6\n' |
| J(1,0.5) | '2' | 1 | ' 2\n' |
| J(1,1) | '2' | 1 | ' 2\n' |
| J(1,1.5) | '2' | 1 | ' 2\n' |
| J(1,2) | '2' | 1 | ' 2\n' |
| J(1.5,0) | '6' | 0 | ' 6\n' |
| J(1.5,0.5) | '2' | 1 | ' 2\n' |
| J(1.5,1) | '2' | 1 | ' 2\n' |
| J(1.5,1.5) | '2' | 1 | ' 2\n' |
| J(1.5,2) | '2' | 1 | ' 2\n' |
| J(2,0) | '2' | 1 | ' 2\n' |
| J(2,0.5) | '2' | 1 | ' 2\n' |
| J(2,1) | '2' | 1 | ' 2\n' |
| J(2,1.5) | '2' | 1 | ' 2\n' |
| J(2,2) | '2' | 1 | ' 2\n' |
| R(0,1) | '2' | 1 | ' 2\n' |
| R(1,0) | '6' | 0 | ' 6\n' |
| R(2,0) | '6' | 0 | ' 6\n' |
| R(0,2) | '2' | 1 | ' 2\n' |
| J(0,2)-U | '2' | 1 | ' 2\n' |
| J(0,2)-RU | '6' | 0 | ' 6\n' |
| J100(0,1) | '6' | 0 | ' 6\n' |
| J100(1,0) | '2' | 1 | ' 2\n' |
| J100(2,0) | '2' | 1 | ' 2\n' |
| J100(0,2) | '2' | 1 | ' 2\n' |
| R100(0,1) | '2' | 1 | ' 2\n' |
| R100(1,0) | '6' | 0 | ' 6\n' |
| R100(2,0) | '2' | 1 | ' 2\n' |
| R100(0,2) | '2' | 1 | ' 2\n' |

### P2-L0-0196 (elements): bridge hydrogen (O) → nitrogen (S), token 34

**lookup** (PP-L0-0196): O's answer 3, S's answer 4

O, as read:

```
<|im_start|>user
The locker of nitrogen is four. Tara picked nitrogen. The locker of hydrogen is three. The locker of carbon is five. Mia picked carbon. Finn picked⟦ hydrogen⟧.
Which locker belongs to Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3\n' |
| J(0,0.5) | '3' | 0 | ' 3\n' |
| J(0,1) | '4' | 1 | ' 4\n' |
| J(0,1.5) | '4' | 1 | ' 4\n' |
| J(0,2) | '4' | 1 | ' 4\n' |
| J(0.5,0) | '3' | 0 | ' 3\n' |
| J(0.5,0.5) | '3' | 0 | ' 3\n' |
| J(0.5,1) | '4' | 1 | ' 4\n' |
| J(0.5,1.5) | '4' | 1 | ' 4\n' |
| J(0.5,2) | '4' | 1 | ' 4\n' |
| J(1,0) | '3' | 0 | ' 3\n' |
| J(1,0.5) | '3' | 0 | ' 3\n' |
| J(1,1) | '4' | 1 | ' 4\n' |
| J(1,1.5) | '4' | 1 | ' 4\n' |
| J(1,2) | '4' | 1 | ' 4\n' |
| J(1.5,0) | '3' | 0 | ' 3\n' |
| J(1.5,0.5) | '4' | 1 | ' 4\n' |
| J(1.5,1) | '4' | 1 | ' 4\n' |
| J(1.5,1.5) | '4' | 1 | ' 4\n' |
| J(1.5,2) | '4' | 1 | ' 4\n' |
| J(2,0) | '3' | 0 | ' 3\n' |
| J(2,0.5) | '4' | 1 | ' 4\n' |
| J(2,1) | '4' | 1 | ' 4\n' |
| J(2,1.5) | '4' | 1 | ' 4\n' |
| J(2,2) | '4' | 1 | ' 4\n' |
| R(0,1) | '4' | 1 | ' 4\n' |
| R(1,0) | '3' | 0 | ' 3\n' |
| R(2,0) | '3' | 0 | ' 3\n' |
| R(0,2) | '4' | 1 | ' 4\n' |
| J(0,2)-U | '5' | 0 | ' 5\n' |
| J(0,2)-RU | '4' | 1 | ' 4\n' |
| J100(0,1) | '4' | 1 | ' 4\n' |
| J100(1,0) | '3' | 0 | ' 3\n' |
| J100(2,0) | '3' | 0 | ' 3\n' |
| J100(0,2) | '4' | 1 | ' 4\n' |
| R100(0,1) | '4' | 1 | ' 4\n' |
| R100(1,0) | '3' | 0 | ' 3\n' |
| R100(2,0) | '4' | 1 | ' 4\n' |
| R100(0,2) | '4' | 1 | ' 4\n' |

**recall** (PM-L0-0196): O's answer 1, S's answer 7

O, as read:

```
<|im_start|>user
The locker of nitrogen is four. Tara picked nitrogen. The locker of hydrogen is three. The locker of carbon is five. Mia picked carbon. Finn picked⟦ hydrogen⟧.
What is the atomic number of Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '1' | 0 | ' 1\n' |
| J(0,0.5) | '1' | 0 | ' 1\n' |
| J(0,1) | '7' | 1 | ' 7\n' |
| J(0,1.5) | '7' | 1 | ' 7\n' |
| J(0,2) | '7' | 1 | ' 7\n' |
| J(0.5,0) | '1' | 0 | ' 1\n' |
| J(0.5,0.5) | '7' | 1 | ' 7\n' |
| J(0.5,1) | '7' | 1 | ' 7\n' |
| J(0.5,1.5) | '7' | 1 | ' 7\n' |
| J(0.5,2) | '7' | 1 | ' 7\n' |
| J(1,0) | '1' | 0 | ' 1\n' |
| J(1,0.5) | '7' | 1 | ' 7\n' |
| J(1,1) | '7' | 1 | ' 7\n' |
| J(1,1.5) | '7' | 1 | ' 7\n' |
| J(1,2) | '7' | 1 | ' 7\n' |
| J(1.5,0) | '7' | 1 | ' 7\n' |
| J(1.5,0.5) | '7' | 1 | ' 7\n' |
| J(1.5,1) | '7' | 1 | ' 7\n' |
| J(1.5,1.5) | '7' | 1 | ' 7\n' |
| J(1.5,2) | '7' | 1 | ' 7\n' |
| J(2,0) | '7' | 1 | ' 7\n' |
| J(2,0.5) | '7' | 1 | ' 7\n' |
| J(2,1) | '7' | 1 | ' 7\n' |
| J(2,1.5) | '7' | 1 | ' 7\n' |
| J(2,2) | '7' | 1 | ' 7\n' |
| R(0,1) | '7' | 1 | ' 7\n' |
| R(1,0) | '1' | 0 | ' 1\n' |
| R(2,0) | '1' | 0 | ' 1\n' |
| R(0,2) | '7' | 1 | ' 7\n' |
| J(0,2)-U | '7' | 1 | ' 7\n' |
| J(0,2)-RU | '7' | 1 | ' 7\n' |
| J100(0,1) | '7' | 1 | ' 7\n' |
| J100(1,0) | '7' | 1 | ' 7\n' |
| J100(2,0) | '7' | 1 | ' 7\n' |
| J100(0,2) | '7' | 1 | ' 7\n' |
| R100(0,1) | '7' | 1 | ' 7\n' |
| R100(1,0) | '1' | 0 | ' 1\n' |
| R100(2,0) | '7' | 1 | ' 7\n' |
| R100(0,2) | '7' | 1 | ' 7\n' |

### P2-L0-0213 (animals): bridge goose (O) → bee (S), token 40

**lookup** (PP-L0-0213): O's answer 4, S's answer 3

O, as read:

```
<|im_start|>user
The locker of the bee is three. The locker of the beetle is one. The locker of the goose is four. Hugo picked the beetle. Noah picked the bee. Rose picked the⟦ goose⟧.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4\n' |
| J(0,0.5) | '4' | 0 | ' 4\n' |
| J(0,1) | '3' | 1 | ' 3\n' |
| J(0,1.5) | '3' | 1 | ' 3\n' |
| J(0,2) | '3' | 1 | ' 3\n' |
| J(0.5,0) | '4' | 0 | ' 4\n' |
| J(0.5,0.5) | '4' | 0 | ' 4\n' |
| J(0.5,1) | '3' | 1 | ' 3\n' |
| J(0.5,1.5) | '3' | 1 | ' 3\n' |
| J(0.5,2) | '3' | 1 | ' 3\n' |
| J(1,0) | '4' | 0 | ' 4\n' |
| J(1,0.5) | '4' | 0 | ' 4\n' |
| J(1,1) | '3' | 1 | ' 3\n' |
| J(1,1.5) | '3' | 1 | ' 3\n' |
| J(1,2) | '3' | 1 | ' 3\n' |
| J(1.5,0) | '4' | 0 | ' 4\n' |
| J(1.5,0.5) | '4' | 0 | ' 4\n' |
| J(1.5,1) | '3' | 1 | ' 3\n' |
| J(1.5,1.5) | '3' | 1 | ' 3\n' |
| J(1.5,2) | '3' | 1 | ' 3\n' |
| J(2,0) | '4' | 0 | ' 4\n' |
| J(2,0.5) | '3' | 1 | ' 3\n' |
| J(2,1) | '3' | 1 | ' 3\n' |
| J(2,1.5) | '3' | 1 | ' 3\n' |
| J(2,2) | '3' | 1 | ' 3\n' |
| R(0,1) | '3' | 1 | ' 3\n' |
| R(1,0) | '4' | 0 | ' 4\n' |
| R(2,0) | '4' | 0 | ' 4\n' |
| R(0,2) | '3' | 1 | ' 3\n' |
| J(0,2)-U | '3' | 1 | ' 3\n' |
| J(0,2)-RU | '3' | 1 | ' 3\n' |
| J100(0,1) | '4' | 0 | ' 4\n' |
| J100(1,0) | '4' | 0 | ' 4\n' |
| J100(2,0) | '3' | 1 | ' 3\n' |
| J100(0,2) | '3' | 1 | ' 3\n' |
| R100(0,1) | '4' | 0 | ' 4\n' |
| R100(1,0) | '4' | 0 | ' 4\n' |
| R100(2,0) | '3' | 1 | ' 3\n' |
| R100(0,2) | '3' | 1 | ' 3\n' |

**recall** (PM-L0-0213): O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the bee is three. The locker of the beetle is one. The locker of the goose is four. Hugo picked the beetle. Noah picked the bee. Rose picked the⟦ goose⟧.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2\n' |
| J(0,0.5) | '2' | 0 | ' 2\n' |
| J(0,1) | '6' | 1 | ' 6\n' |
| J(0,1.5) | '6' | 1 | ' 6\n' |
| J(0,2) | '6' | 1 | ' 6\n' |
| J(0.5,0) | '2' | 0 | ' 2\n' |
| J(0.5,0.5) | '6' | 1 | ' 6\n' |
| J(0.5,1) | '6' | 1 | ' 6\n' |
| J(0.5,1.5) | '6' | 1 | ' 6\n' |
| J(0.5,2) | '6' | 1 | ' 6\n' |
| J(1,0) | '2' | 0 | ' 2\n' |
| J(1,0.5) | '6' | 1 | ' 6\n' |
| J(1,1) | '6' | 1 | ' 6\n' |
| J(1,1.5) | '6' | 1 | ' 6\n' |
| J(1,2) | '6' | 1 | ' 6\n' |
| J(1.5,0) | '6' | 1 | ' 6\n' |
| J(1.5,0.5) | '6' | 1 | ' 6\n' |
| J(1.5,1) | '6' | 1 | ' 6\n' |
| J(1.5,1.5) | '6' | 1 | ' 6\n' |
| J(1.5,2) | '6' | 1 | ' 6\n' |
| J(2,0) | '6' | 1 | ' 6\n' |
| J(2,0.5) | '6' | 1 | ' 6\n' |
| J(2,1) | '6' | 1 | ' 6\n' |
| J(2,1.5) | '6' | 1 | ' 6\n' |
| J(2,2) | '6' | 1 | ' 6\n' |
| R(0,1) | '6' | 1 | ' 6\n' |
| R(1,0) | '2' | 0 | ' 2\n' |
| R(2,0) | '2' | 0 | ' 2\n' |
| R(0,2) | '6' | 1 | ' 6\n' |
| J(0,2)-U | '6' | 1 | ' 6\n' |
| J(0,2)-RU | '6' | 1 | ' 6\n' |
| J100(0,1) | '6' | 1 | ' 6\n' |
| J100(1,0) | '6' | 1 | ' 6\n' |
| J100(2,0) | '6' | 1 | ' 6\n' |
| J100(0,2) | '6' | 1 | ' 6\n' |
| R100(0,1) | '6' | 1 | ' 6\n' |
| R100(1,0) | '2' | 0 | ' 2\n' |
| R100(2,0) | '6' | 1 | ' 6\n' |
| R100(0,2) | '6' | 1 | ' 6\n' |

### P2-L0-0218 (greek): bridge gamma (O) → epsilon (S), token 25

**lookup** (PP-L0-0218): O's answer 8, S's answer 6

O, as read:

```
<|im_start|>user
The locker of gamma is 8. The locker of epsilon is 6. Mark picked epsilon. Clara picked⟦ gamma⟧. The locker of theta is 3. Finn picked theta.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '8' | 0 | ' 8\n' |
| J(0,0.5) | '6' | 1 | ' 6\n' |
| J(0,1) | '6' | 1 | ' 6\n' |
| J(0,1.5) | '6' | 1 | ' 6\n' |
| J(0,2) | '6' | 1 | ' 6\n' |
| J(0.5,0) | '8' | 0 | ' 8\n' |
| J(0.5,0.5) | '6' | 1 | ' 6\n' |
| J(0.5,1) | '6' | 1 | ' 6\n' |
| J(0.5,1.5) | '6' | 1 | ' 6\n' |
| J(0.5,2) | '6' | 1 | ' 6\n' |
| J(1,0) | '8' | 0 | ' 8\n' |
| J(1,0.5) | '6' | 1 | ' 6\n' |
| J(1,1) | '6' | 1 | ' 6\n' |
| J(1,1.5) | '6' | 1 | ' 6\n' |
| J(1,2) | '6' | 1 | ' 6\n' |
| J(1.5,0) | '8' | 0 | ' 8\n' |
| J(1.5,0.5) | '6' | 1 | ' 6\n' |
| J(1.5,1) | '6' | 1 | ' 6\n' |
| J(1.5,1.5) | '6' | 1 | ' 6\n' |
| J(1.5,2) | '6' | 1 | ' 6\n' |
| J(2,0) | '8' | 0 | ' 8\n' |
| J(2,0.5) | '6' | 1 | ' 6\n' |
| J(2,1) | '6' | 1 | ' 6\n' |
| J(2,1.5) | '6' | 1 | ' 6\n' |
| J(2,2) | '6' | 1 | ' 6\n' |
| R(0,1) | '6' | 1 | ' 6\n' |
| R(1,0) | '8' | 0 | ' 8\n' |
| R(2,0) | '6' | 1 | ' 6\n' |
| R(0,2) | '6' | 1 | ' 6\n' |
| J(0,2)-U | '6' | 1 | ' 6\n' |
| J(0,2)-RU | '6' | 1 | ' 6\n' |
| J100(0,1) | '6' | 1 | ' 6\n' |
| J100(1,0) | '8' | 0 | ' 8\n' |
| J100(2,0) | '6' | 1 | ' 6\n' |
| J100(0,2) | '6' | 1 | ' 6\n' |
| R100(0,1) | '6' | 1 | ' 6\n' |
| R100(1,0) | '8' | 0 | ' 8\n' |
| R100(2,0) | '6' | 1 | ' 6\n' |
| R100(0,2) | '6' | 1 | ' 6\n' |

**recall** (PM-L0-0218): O's answer 3, S's answer 5

O, as read:

```
<|im_start|>user
The locker of gamma is 8. The locker of epsilon is 6. Mark picked epsilon. Clara picked⟦ gamma⟧. The locker of theta is 3. Finn picked theta.
Which position in the Greek alphabet does Clara's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3\n' |
| J(0,0.5) | '5' | 1 | ' 5\n' |
| J(0,1) | '5' | 1 | ' 5\n' |
| J(0,1.5) | '5' | 1 | ' 5\n' |
| J(0,2) | '5' | 1 | ' 5\n' |
| J(0.5,0) | '3' | 0 | ' 3\n' |
| J(0.5,0.5) | '5' | 1 | ' 5\n' |
| J(0.5,1) | '5' | 1 | ' 5\n' |
| J(0.5,1.5) | '5' | 1 | ' 5\n' |
| J(0.5,2) | '5' | 1 | ' 5\n' |
| J(1,0) | '3' | 0 | ' 3\n' |
| J(1,0.5) | '5' | 1 | ' 5\n' |
| J(1,1) | '5' | 1 | ' 5\n' |
| J(1,1.5) | '5' | 1 | ' 5\n' |
| J(1,2) | '5' | 1 | ' 5\n' |
| J(1.5,0) | '5' | 1 | ' 5\n' |
| J(1.5,0.5) | '5' | 1 | ' 5\n' |
| J(1.5,1) | '5' | 1 | ' 5\n' |
| J(1.5,1.5) | '5' | 1 | ' 5\n' |
| J(1.5,2) | '5' | 1 | ' 5\n' |
| J(2,0) | '5' | 1 | ' 5\n' |
| J(2,0.5) | '5' | 1 | ' 5\n' |
| J(2,1) | '5' | 1 | ' 5\n' |
| J(2,1.5) | '5' | 1 | ' 5\n' |
| J(2,2) | '5' | 1 | ' 5\n' |
| R(0,1) | '5' | 1 | ' 5\n' |
| R(1,0) | '3' | 0 | ' 3\n' |
| R(2,0) | '5' | 1 | ' 5\n' |
| R(0,2) | '5' | 1 | ' 5\n' |
| J(0,2)-U | '5' | 1 | ' 5\n' |
| J(0,2)-RU | '5' | 1 | ' 5\n' |
| J100(0,1) | '5' | 1 | ' 5\n' |
| J100(1,0) | '5' | 1 | ' 5\n' |
| J100(2,0) | '5' | 1 | ' 5\n' |
| J100(0,2) | '5' | 1 | ' 5\n' |
| R100(0,1) | '5' | 1 | ' 5\n' |
| R100(1,0) | '5' | 1 | ' 5\n' |
| R100(2,0) | '5' | 1 | ' 5\n' |
| R100(0,2) | '5' | 1 | ' 5\n' |

### P2-L0-0246 (animals): bridge cow (O) → owl (S), token 33

**lookup** (PP-L0-0246): O's answer 3, S's answer 4

O, as read:

```
<|im_start|>user
The locker of the cow is 3. The locker of the owl is 4. The locker of the fox is 1. Jack picked the⟦ cow⟧. Tara picked the fox. Diana picked the owl.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3\n' |
| J(0,0.5) | '3' | 0 | ' 3\n' |
| J(0,1) | '4' | 1 | ' 4\n' |
| J(0,1.5) | '4' | 1 | ' 4\n' |
| J(0,2) | '4' | 1 | ' 4\n' |
| J(0.5,0) | '3' | 0 | ' 3\n' |
| J(0.5,0.5) | '4' | 1 | ' 4\n' |
| J(0.5,1) | '4' | 1 | ' 4\n' |
| J(0.5,1.5) | '4' | 1 | ' 4\n' |
| J(0.5,2) | '4' | 1 | ' 4\n' |
| J(1,0) | '3' | 0 | ' 3\n' |
| J(1,0.5) | '4' | 1 | ' 4\n' |
| J(1,1) | '4' | 1 | ' 4\n' |
| J(1,1.5) | '4' | 1 | ' 4\n' |
| J(1,2) | '4' | 1 | ' 4\n' |
| J(1.5,0) | '3' | 0 | ' 3\n' |
| J(1.5,0.5) | '4' | 1 | ' 4\n' |
| J(1.5,1) | '4' | 1 | ' 4\n' |
| J(1.5,1.5) | '4' | 1 | ' 4\n' |
| J(1.5,2) | '4' | 1 | ' 4\n' |
| J(2,0) | '3' | 0 | ' 3\n' |
| J(2,0.5) | '4' | 1 | ' 4\n' |
| J(2,1) | '4' | 1 | ' 4\n' |
| J(2,1.5) | '4' | 1 | ' 4\n' |
| J(2,2) | '4' | 1 | ' 4\n' |
| R(0,1) | '4' | 1 | ' 4\n' |
| R(1,0) | '3' | 0 | ' 3\n' |
| R(2,0) | '4' | 1 | ' 4\n' |
| R(0,2) | '4' | 1 | ' 4\n' |
| J(0,2)-U | '4' | 1 | ' 4\n' |
| J(0,2)-RU | '4' | 1 | ' 4\n' |
| J100(0,1) | '4' | 1 | ' 4\n' |
| J100(1,0) | '3' | 0 | ' 3\n' |
| J100(2,0) | '4' | 1 | ' 4\n' |
| J100(0,2) | '4' | 1 | ' 4\n' |
| R100(0,1) | '4' | 1 | ' 4\n' |
| R100(1,0) | '4' | 1 | ' 4\n' |
| R100(2,0) | '4' | 1 | ' 4\n' |
| R100(0,2) | '4' | 1 | ' 4\n' |

**recall** (PM-L0-0246): O's answer 4, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the cow is 3. The locker of the owl is 4. The locker of the fox is 1. Jack picked the⟦ cow⟧. Tara picked the fox. Diana picked the owl.
How many legs does Jack's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4\n' |
| J(0,0.5) | '4' | 0 | ' 4\n' |
| J(0,1) | '2' | 1 | ' 2\n' |
| J(0,1.5) | '2' | 1 | ' 2\n' |
| J(0,2) | '2' | 1 | ' 2\n' |
| J(0.5,0) | '4' | 0 | ' 4\n' |
| J(0.5,0.5) | '4' | 0 | ' 4\n' |
| J(0.5,1) | '2' | 1 | ' 2\n' |
| J(0.5,1.5) | '2' | 1 | ' 2\n' |
| J(0.5,2) | '2' | 1 | ' 2\n' |
| J(1,0) | '4' | 0 | ' 4\n' |
| J(1,0.5) | '2' | 1 | ' 2\n' |
| J(1,1) | '2' | 1 | ' 2\n' |
| J(1,1.5) | '2' | 1 | ' 2\n' |
| J(1,2) | '2' | 1 | ' 2\n' |
| J(1.5,0) | '4' | 0 | ' 4\n' |
| J(1.5,0.5) | '2' | 1 | ' 2\n' |
| J(1.5,1) | '2' | 1 | ' 2\n' |
| J(1.5,1.5) | '2' | 1 | ' 2\n' |
| J(1.5,2) | '2' | 1 | ' 2\n' |
| J(2,0) | '4' | 0 | ' 4\n' |
| J(2,0.5) | '2' | 1 | ' 2\n' |
| J(2,1) | '2' | 1 | ' 2\n' |
| J(2,1.5) | '2' | 1 | ' 2\n' |
| J(2,2) | '2' | 1 | ' 2\n' |
| R(0,1) | '2' | 1 | ' 2\n' |
| R(1,0) | '4' | 0 | ' 4\n' |
| R(2,0) | '4' | 0 | ' 4\n' |
| R(0,2) | '2' | 1 | ' 2\n' |
| J(0,2)-U | '2' | 1 | ' 2\n' |
| J(0,2)-RU | '2' | 1 | ' 2\n' |
| J100(0,1) | '4' | 0 | ' 4\n' |
| J100(1,0) | '4' | 0 | ' 4\n' |
| J100(2,0) | '2' | 1 | ' 2\n' |
| J100(0,2) | '2' | 1 | ' 2\n' |
| R100(0,1) | '2' | 1 | ' 2\n' |
| R100(1,0) | '4' | 0 | ' 4\n' |
| R100(2,0) | '2' | 1 | ' 2\n' |
| R100(0,2) | '2' | 1 | ' 2\n' |

### P2-L0-0252 (animals): bridge sheep (O) → spider (S), token 35

**lookup** (PP-L0-0252): O's answer 9, S's answer 7

O, as read:

```
<|im_start|>user
Victor picked the spider. The locker of the sheep is 9. Luke picked the butterfly. The locker of the spider is 7. Rose picked the⟦ sheep⟧. The locker of the butterfly is 3.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '9' | 0 | ' 9\n' |
| J(0,0.5) | '9' | 0 | ' 9\n' |
| J(0,1) | '7' | 1 | ' 7\n' |
| J(0,1.5) | '7' | 1 | ' 7\n' |
| J(0,2) | '7' | 1 | ' 7\n' |
| J(0.5,0) | '9' | 0 | ' 9\n' |
| J(0.5,0.5) | '9' | 0 | ' 9\n' |
| J(0.5,1) | '7' | 1 | ' 7\n' |
| J(0.5,1.5) | '7' | 1 | ' 7\n' |
| J(0.5,2) | '7' | 1 | ' 7\n' |
| J(1,0) | '9' | 0 | ' 9\n' |
| J(1,0.5) | '7' | 1 | ' 7\n' |
| J(1,1) | '7' | 1 | ' 7\n' |
| J(1,1.5) | '7' | 1 | ' 7\n' |
| J(1,2) | '7' | 1 | ' 7\n' |
| J(1.5,0) | '9' | 0 | ' 9\n' |
| J(1.5,0.5) | '7' | 1 | ' 7\n' |
| J(1.5,1) | '7' | 1 | ' 7\n' |
| J(1.5,1.5) | '7' | 1 | ' 7\n' |
| J(1.5,2) | '7' | 1 | ' 7\n' |
| J(2,0) | '9' | 0 | ' 9\n' |
| J(2,0.5) | '7' | 1 | ' 7\n' |
| J(2,1) | '7' | 1 | ' 7\n' |
| J(2,1.5) | '7' | 1 | ' 7\n' |
| J(2,2) | '7' | 1 | ' 7\n' |
| R(0,1) | '7' | 1 | ' 7\n' |
| R(1,0) | '9' | 0 | ' 9\n' |
| R(2,0) | '9' | 0 | ' 9\n' |
| R(0,2) | '7' | 1 | ' 7\n' |
| J(0,2)-U | '7' | 1 | ' 7\n' |
| J(0,2)-RU | '7' | 1 | ' 7\n' |
| J100(0,1) | '7' | 1 | ' 7\n' |
| J100(1,0) | '9' | 0 | ' 9\n' |
| J100(2,0) | '7' | 1 | ' 7\n' |
| J100(0,2) | '7' | 1 | ' 7\n' |
| R100(0,1) | '9' | 0 | ' 9\n' |
| R100(1,0) | '9' | 0 | ' 9\n' |
| R100(2,0) | '7' | 1 | ' 7\n' |
| R100(0,2) | '7' | 1 | ' 7\n' |

**recall** (PM-L0-0252): O's answer 4, S's answer 8

O, as read:

```
<|im_start|>user
Victor picked the spider. The locker of the sheep is 9. Luke picked the butterfly. The locker of the spider is 7. Rose picked the⟦ sheep⟧. The locker of the butterfly is 3.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4\n' |
| J(0,0.5) | '8' | 1 | ' 8\n' |
| J(0,1) | '8' | 1 | ' 8\n' |
| J(0,1.5) | '8' | 1 | ' 8\n' |
| J(0,2) | '8' | 1 | ' 8\n' |
| J(0.5,0) | '8' | 1 | ' 8\n' |
| J(0.5,0.5) | '8' | 1 | ' 8\n' |
| J(0.5,1) | '8' | 1 | ' 8\n' |
| J(0.5,1.5) | '8' | 1 | ' 8\n' |
| J(0.5,2) | '8' | 1 | ' 8\n' |
| J(1,0) | '8' | 1 | ' 8\n' |
| J(1,0.5) | '8' | 1 | ' 8\n' |
| J(1,1) | '8' | 1 | ' 8\n' |
| J(1,1.5) | '8' | 1 | ' 8\n' |
| J(1,2) | '8' | 1 | ' 8\n' |
| J(1.5,0) | '8' | 1 | ' 8\n' |
| J(1.5,0.5) | '8' | 1 | ' 8\n' |
| J(1.5,1) | '8' | 1 | ' 8\n' |
| J(1.5,1.5) | '8' | 1 | ' 8\n' |
| J(1.5,2) | '8' | 1 | ' 8\n' |
| J(2,0) | '8' | 1 | ' 8\n' |
| J(2,0.5) | '8' | 1 | ' 8\n' |
| J(2,1) | '8' | 1 | ' 8\n' |
| J(2,1.5) | '8' | 1 | ' 8\n' |
| J(2,2) | '8' | 1 | ' 8\n' |
| R(0,1) | '8' | 1 | ' 8\n' |
| R(1,0) | '8' | 1 | ' 8\n' |
| R(2,0) | '8' | 1 | ' 8\n' |
| R(0,2) | '8' | 1 | ' 8\n' |
| J(0,2)-U | '8' | 1 | ' 8\n' |
| J(0,2)-RU | '8' | 1 | ' 8\n' |
| J100(0,1) | '8' | 1 | ' 8\n' |
| J100(1,0) | '8' | 1 | ' 8\n' |
| J100(2,0) | '8' | 1 | ' 8\n' |
| J100(0,2) | '8' | 1 | ' 8\n' |
| R100(0,1) | '8' | 1 | ' 8\n' |
| R100(1,0) | '8' | 1 | ' 8\n' |
| R100(2,0) | '8' | 1 | ' 8\n' |
| R100(0,2) | '8' | 1 | ' 8\n' |

### P2-L0-0256 (elements): bridge lithium (O) → hydrogen (S), token 37

**lookup** (PP-L0-0256): O's answer 7, S's answer 2

O, as read:

```
<|im_start|>user
The locker of hydrogen is 2. Victor picked helium. The locker of lithium is 7. David picked hydrogen. The locker of helium is 9. Sara picked⟦ lithium⟧.
Which locker belongs to Sara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '7' | 0 | ' 7\n' |
| J(0,0.5) | '7' | 0 | ' 7\n' |
| J(0,1) | '2' | 1 | ' 2\n' |
| J(0,1.5) | '2' | 1 | ' 2\n' |
| J(0,2) | '2' | 1 | ' 2\n' |
| J(0.5,0) | '7' | 0 | ' 7\n' |
| J(0.5,0.5) | '2' | 1 | ' 2\n' |
| J(0.5,1) | '2' | 1 | ' 2\n' |
| J(0.5,1.5) | '2' | 1 | ' 2\n' |
| J(0.5,2) | '2' | 1 | ' 2\n' |
| J(1,0) | '7' | 0 | ' 7\n' |
| J(1,0.5) | '2' | 1 | ' 2\n' |
| J(1,1) | '2' | 1 | ' 2\n' |
| J(1,1.5) | '2' | 1 | ' 2\n' |
| J(1,2) | '2' | 1 | ' 2\n' |
| J(1.5,0) | '7' | 0 | ' 7\n' |
| J(1.5,0.5) | '2' | 1 | ' 2\n' |
| J(1.5,1) | '2' | 1 | ' 2\n' |
| J(1.5,1.5) | '2' | 1 | ' 2\n' |
| J(1.5,2) | '2' | 1 | ' 2\n' |
| J(2,0) | '7' | 0 | ' 7\n' |
| J(2,0.5) | '2' | 1 | ' 2\n' |
| J(2,1) | '2' | 1 | ' 2\n' |
| J(2,1.5) | '2' | 1 | ' 2\n' |
| J(2,2) | '2' | 1 | ' 2\n' |
| R(0,1) | '2' | 1 | ' 2\n' |
| R(1,0) | '7' | 0 | ' 7\n' |
| R(2,0) | '7' | 0 | ' 7\n' |
| R(0,2) | '2' | 1 | ' 2\n' |
| J(0,2)-U | '9' | 0 | ' 9\n' |
| J(0,2)-RU | '2' | 1 | ' 2\n' |
| J100(0,1) | '2' | 1 | ' 2\n' |
| J100(1,0) | '7' | 0 | ' 7\n' |
| J100(2,0) | '2' | 1 | ' 2\n' |
| J100(0,2) | '2' | 1 | ' 2\n' |
| R100(0,1) | '2' | 1 | ' 2\n' |
| R100(1,0) | '7' | 0 | ' 7\n' |
| R100(2,0) | '2' | 1 | ' 2\n' |
| R100(0,2) | '2' | 1 | ' 2\n' |

**recall** (PM-L0-0256): O's answer 3, S's answer 1

O, as read:

```
<|im_start|>user
The locker of hydrogen is 2. Victor picked helium. The locker of lithium is 7. David picked hydrogen. The locker of helium is 9. Sara picked⟦ lithium⟧.
What is the atomic number of Sara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3\n' |
| J(0,0.5) | '3' | 0 | ' 3\n' |
| J(0,1) | '1' | 1 | ' 1\n' |
| J(0,1.5) | '1' | 1 | ' 1\n' |
| J(0,2) | '1' | 1 | ' 1\n' |
| J(0.5,0) | '3' | 0 | ' 3\n' |
| J(0.5,0.5) | '3' | 0 | ' 3\n' |
| J(0.5,1) | '1' | 1 | ' 1\n' |
| J(0.5,1.5) | '1' | 1 | ' 1\n' |
| J(0.5,2) | '1' | 1 | ' 1\n' |
| J(1,0) | '3' | 0 | ' 3\n' |
| J(1,0.5) | '1' | 1 | ' 1\n' |
| J(1,1) | '1' | 1 | ' 1\n' |
| J(1,1.5) | '1' | 1 | ' 1\n' |
| J(1,2) | '1' | 1 | ' 1\n' |
| J(1.5,0) | '3' | 0 | ' 3\n' |
| J(1.5,0.5) | '1' | 1 | ' 1\n' |
| J(1.5,1) | '1' | 1 | ' 1\n' |
| J(1.5,1.5) | '1' | 1 | ' 1\n' |
| J(1.5,2) | '1' | 1 | ' 1\n' |
| J(2,0) | '1' | 1 | ' 1\n' |
| J(2,0.5) | '1' | 1 | ' 1\n' |
| J(2,1) | '1' | 1 | ' 1\n' |
| J(2,1.5) | '1' | 1 | ' 1\n' |
| J(2,2) | '1' | 1 | ' 1\n' |
| R(0,1) | '1' | 1 | ' 1\n' |
| R(1,0) | '3' | 0 | ' 3\n' |
| R(2,0) | '3' | 0 | ' 3\n' |
| R(0,2) | '1' | 1 | ' 1\n' |
| J(0,2)-U | '1' | 1 | ' 1\n' |
| J(0,2)-RU | '1' | 1 | ' 1\n' |
| J100(0,1) | '3' | 0 | ' 3\n' |
| J100(1,0) | '1' | 1 | ' 1\n' |
| J100(2,0) | '1' | 1 | ' 1\n' |
| J100(0,2) | '3' | 0 | ' 3\n' |
| R100(0,1) | '1' | 1 | ' 1\n' |
| R100(1,0) | '3' | 0 | ' 3\n' |
| R100(2,0) | '1' | 1 | ' 1\n' |
| R100(0,2) | '1' | 1 | ' 1\n' |

## qwen3.6-27b: x49_1_27b, 10 random items of 69 (seed 0)

### P2-L0-0016 (elements): bridge hydrogen (O) → nitrogen (S), token 34

**lookup** (PP-L0-0016): O's answer 9, S's answer 6

O, as read:

```
<|im_start|>user
The locker of hydrogen is nine. Olivia picked nitrogen. Oscar picked helium. The locker of helium is seven. The locker of nitrogen is six. Hugo picked⟦ hydrogen⟧.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '9' | 0 | ' 9' |
| J(0,0.5) | '9' | 0 | ' 9' |
| J(0,1) | '6' | 1 | ' 6' |
| J(0,1.5) | '6' | 1 | ' 6' |
| J(0,2) | '6' | 1 | ' 6' |
| J(0.5,0) | '9' | 0 | ' 9' |
| J(0.5,0.5) | '9' | 0 | ' 9' |
| J(0.5,1) | '6' | 1 | ' 6' |
| J(0.5,1.5) | '6' | 1 | ' 6' |
| J(0.5,2) | '6' | 1 | ' 6' |
| J(1,0) | '9' | 0 | ' 9' |
| J(1,0.5) | '9' | 0 | ' 9' |
| J(1,1) | '6' | 1 | ' 6' |
| J(1,1.5) | '6' | 1 | ' 6' |
| J(1,2) | '6' | 1 | ' 6' |
| J(1.5,0) | '9' | 0 | ' 9' |
| J(1.5,0.5) | '9' | 0 | ' 9' |
| J(1.5,1) | '6' | 1 | ' 6' |
| J(1.5,1.5) | '6' | 1 | ' 6' |
| J(1.5,2) | '6' | 1 | ' 6' |
| J(2,0) | '9' | 0 | ' 9' |
| J(2,0.5) | '9' | 0 | ' 9' |
| J(2,1) | '6' | 1 | ' 6' |
| J(2,1.5) | '6' | 1 | ' 6' |
| J(2,2) | '6' | 1 | ' 6' |
| R(0,1) | '6' | 1 | ' 6' |
| R(1,0) | '9' | 0 | ' 9' |
| R(2,0) | '9' | 0 | ' 9' |
| R(0,2) | '6' | 1 | ' 6' |
| J(0,2)-U | '9' | 0 | ' 9' |
| J(0,2)-RU | '9' | 0 | ' 9' |

**recall** (PM-L0-0016): O's answer 1, S's answer 7

O, as read:

```
<|im_start|>user
The locker of hydrogen is nine. Olivia picked nitrogen. Oscar picked helium. The locker of helium is seven. The locker of nitrogen is six. Hugo picked⟦ hydrogen⟧.
What is the atomic number of Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '1' | 0 | ' 1' |
| J(0,0.5) | '1' | 0 | ' 1' |
| J(0,1) | '1' | 0 | ' 1' |
| J(0,1.5) | '7' | 1 | ' 7' |
| J(0,2) | '7' | 1 | ' 7' |
| J(0.5,0) | '1' | 0 | ' 1' |
| J(0.5,0.5) | '1' | 0 | ' 1' |
| J(0.5,1) | '7' | 1 | ' 7' |
| J(0.5,1.5) | '7' | 1 | ' 7' |
| J(0.5,2) | '7' | 1 | ' 7' |
| J(1,0) | '1' | 0 | ' 1' |
| J(1,0.5) | '1' | 0 | ' 1' |
| J(1,1) | '7' | 1 | ' 7' |
| J(1,1.5) | '7' | 1 | ' 7' |
| J(1,2) | '7' | 1 | ' 7' |
| J(1.5,0) | '1' | 0 | ' 1' |
| J(1.5,0.5) | '1' | 0 | ' 1' |
| J(1.5,1) | '7' | 1 | ' 7' |
| J(1.5,1.5) | '7' | 1 | ' 7' |
| J(1.5,2) | '7' | 1 | ' 7' |
| J(2,0) | '1' | 0 | ' 1' |
| J(2,0.5) | '7' | 1 | ' 7' |
| J(2,1) | '7' | 1 | ' 7' |
| J(2,1.5) | '7' | 1 | ' 7' |
| J(2,2) | '7' | 1 | ' 7' |
| R(0,1) | '7' | 1 | ' 7' |
| R(1,0) | '1' | 0 | ' 1' |
| R(2,0) | '1' | 0 | ' 1' |
| R(0,2) | '7' | 1 | ' 7' |
| J(0,2)-U | '1' | 0 | ' 1' |
| J(0,2)-RU | '1' | 0 | ' 1' |

### P2-L0-0048 (animals): bridge crow (O) → elephant (S), token 40

**lookup** (PP-L0-0048): O's answer 3, S's answer 8

O, as read:

```
<|im_start|>user
The locker of the beetle is nine. The locker of the elephant is eight. Lily picked the beetle. James picked the elephant. The locker of the crow is three. Henry picked the⟦ crow⟧.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3' |
| J(0,0.5) | '3' | 0 | ' 3' |
| J(0,1) | '8' | 1 | ' 8' |
| J(0,1.5) | '8' | 1 | ' 8' |
| J(0,2) | '8' | 1 | ' 8' |
| J(0.5,0) | '3' | 0 | ' 3' |
| J(0.5,0.5) | '3' | 0 | ' 3' |
| J(0.5,1) | '8' | 1 | ' 8' |
| J(0.5,1.5) | '8' | 1 | ' 8' |
| J(0.5,2) | '8' | 1 | ' 8' |
| J(1,0) | '3' | 0 | ' 3' |
| J(1,0.5) | '3' | 0 | ' 3' |
| J(1,1) | '8' | 1 | ' 8' |
| J(1,1.5) | '8' | 1 | ' 8' |
| J(1,2) | '8' | 1 | ' 8' |
| J(1.5,0) | '3' | 0 | ' 3' |
| J(1.5,0.5) | '3' | 0 | ' 3' |
| J(1.5,1) | '8' | 1 | ' 8' |
| J(1.5,1.5) | '8' | 1 | ' 8' |
| J(1.5,2) | '8' | 1 | ' 8' |
| J(2,0) | '3' | 0 | ' 3' |
| J(2,0.5) | '8' | 1 | ' 3' |
| J(2,1) | '8' | 1 | ' 8' |
| J(2,1.5) | '8' | 1 | ' 8' |
| J(2,2) | '8' | 1 | ' 8' |
| R(0,1) | '8' | 1 | ' 8' |
| R(1,0) | '3' | 0 | ' 3' |
| R(2,0) | '3' | 0 | ' 3' |
| R(0,2) | '8' | 1 | ' 8' |
| J(0,2)-U | '3' | 0 | ' 3' |
| J(0,2)-RU | '8' | 1 | ' 8' |

**recall** (PM-L0-0048): O's answer 2, S's answer 4

O, as read:

```
<|im_start|>user
The locker of the beetle is nine. The locker of the elephant is eight. Lily picked the beetle. James picked the elephant. The locker of the crow is three. Henry picked the⟦ crow⟧.
How many legs does Henry's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2' |
| J(0,0.5) | '2' | 0 | ' 2' |
| J(0,1) | '2' | 0 | ' 2' |
| J(0,1.5) | '2' | 0 | ' 2' |
| J(0,2) | '2' | 0 | ' 2' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '2' | 0 | ' 2' |
| J(0.5,1) | '2' | 0 | ' 2' |
| J(0.5,1.5) | '2' | 0 | ' 2' |
| J(0.5,2) | '2' | 0 | ' 2' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '2' | 0 | ' 2' |
| J(1,1) | '2' | 0 | ' 2' |
| J(1,1.5) | '2' | 0 | ' 2' |
| J(1,2) | '2' | 0 | ' 2' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '2' | 0 | ' 2' |
| J(1.5,1) | '2' | 0 | ' 2' |
| J(1.5,1.5) | '2' | 0 | ' 2' |
| J(1.5,2) | '2' | 0 | ' 2' |
| J(2,0) | '2' | 0 | ' 2' |
| J(2,0.5) | '2' | 0 | ' 2' |
| J(2,1) | '2' | 0 | ' 2' |
| J(2,1.5) | '2' | 0 | ' 2' |
| J(2,2) | '2' | 0 | ' 2' |
| R(0,1) | '2' | 0 | ' 2' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '2' | 0 | ' 2' |
| R(0,2) | '2' | 0 | ' 2' |
| J(0,2)-U | '2' | 0 | ' 2' |
| J(0,2)-RU | '2' | 0 | ' 2' |

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
| J(2,0) | '8' | 0 | ' 8' |
| J(2,0.5) | '1' | 1 | ' 1' |
| J(2,1) | '1' | 1 | ' 1' |
| J(2,1.5) | '1' | 1 | ' 1' |
| J(2,2) | '1' | 1 | ' 1' |
| R(0,1) | '1' | 1 | ' 1' |
| R(1,0) | '8' | 0 | ' 8' |
| R(2,0) | '8' | 0 | ' 8' |
| R(0,2) | '1' | 1 | ' 1' |
| J(0,2)-U | '1' | 1 | ' 1' |
| J(0,2)-RU | '9' | 0 | ' 9' |

### P2-L0-0133 (elements): bridge carbon (O) → oxygen (S), token 33

**lookup** (PP-L0-0133): O's answer 3, S's answer 7

O, as read:

```
<|im_start|>user
The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked⟦ carbon⟧. Eva picked helium.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3' |
| J(0,0.5) | '3' | 0 | ' 3' |
| J(0,1) | '7' | 1 | ' 7' |
| J(0,1.5) | '7' | 1 | ' 7' |
| J(0,2) | '7' | 1 | ' 7' |
| J(0.5,0) | '3' | 0 | ' 3' |
| J(0.5,0.5) | '3' | 0 | ' 3' |
| J(0.5,1) | '7' | 1 | ' 7' |
| J(0.5,1.5) | '7' | 1 | ' 7' |
| J(0.5,2) | '7' | 1 | ' 7' |
| J(1,0) | '3' | 0 | ' 3' |
| J(1,0.5) | '7' | 1 | ' 7' |
| J(1,1) | '7' | 1 | ' 7' |
| J(1,1.5) | '7' | 1 | ' 7' |
| J(1,2) | '7' | 1 | ' 7' |
| J(1.5,0) | '3' | 0 | ' 3' |
| J(1.5,0.5) | '7' | 1 | ' 7' |
| J(1.5,1) | '7' | 1 | ' 7' |
| J(1.5,1.5) | '7' | 1 | ' 7' |
| J(1.5,2) | '7' | 1 | ' 7' |
| J(2,0) | '3' | 0 | ' 3' |
| J(2,0.5) | '7' | 1 | ' 7' |
| J(2,1) | '7' | 1 | ' 7' |
| J(2,1.5) | '7' | 1 | ' 7' |
| J(2,2) | '7' | 1 | ' 7' |
| R(0,1) | '7' | 1 | ' 7' |
| R(1,0) | '3' | 0 | ' 3' |
| R(2,0) | '3' | 0 | ' 3' |
| R(0,2) | '7' | 1 | ' 7' |
| J(0,2)-U | '3' | 0 | ' 3' |
| J(0,2)-RU | '7' | 1 | ' 7' |

**recall** (PM-L0-0133): O's answer 6, S's answer 8

O, as read:

```
<|im_start|>user
The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked⟦ carbon⟧. Eva picked helium.
What is the atomic number of Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6' |
| J(0,0.5) | '6' | 0 | ' 6' |
| J(0,1) | '7' | 0 | ' 7' |
| J(0,1.5) | '8' | 1 | ' 8' |
| J(0,2) | '8' | 1 | ' 8' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '6' | 0 | ' 6' |
| J(0.5,1) | '7' | 0 | ' 7' |
| J(0.5,1.5) | '8' | 1 | ' 8' |
| J(0.5,2) | '8' | 1 | ' 8' |
| J(1,0) | '6' | 0 | ' 6' |
| J(1,0.5) | '8' | 1 | ' 8' |
| J(1,1) | '7' | 0 | ' 8' |
| J(1,1.5) | '8' | 1 | ' 8' |
| J(1,2) | '8' | 1 | ' 8' |
| J(1.5,0) | '8' | 1 | ' 8' |
| J(1.5,0.5) | '8' | 1 | ' 8' |
| J(1.5,1) | '8' | 1 | ' 8' |
| J(1.5,1.5) | '8' | 1 | ' 8' |
| J(1.5,2) | '8' | 1 | ' 8' |
| J(2,0) | '8' | 1 | ' 8' |
| J(2,0.5) | '8' | 1 | ' 8' |
| J(2,1) | '8' | 1 | ' 8' |
| J(2,1.5) | '8' | 1 | ' 8' |
| J(2,2) | '8' | 1 | ' 8' |
| R(0,1) | '7' | 0 | ' 7' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '6' | 0 | ' 6' |
| R(0,2) | '8' | 1 | ' 8' |
| J(0,2)-U | '6' | 0 | ' 6' |
| J(0,2)-RU | '7' | 0 | ' 7' |

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
| J(0,1) | '7' | 0 | ' 7' |
| J(0,1.5) | '4' | 1 | ' 4' |
| J(0,2) | '4' | 1 | ' 4' |
| J(0.5,0) | '7' | 0 | ' 7' |
| J(0.5,0.5) | '7' | 0 | ' 7' |
| J(0.5,1) | '7' | 0 | ' 7' |
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
| J(0,2)-U | '4' | 1 | ' 4' |
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
| J(0,1) | '2' | 0 | ' 2' |
| J(0,1.5) | '6' | 1 | ' 6' |
| J(0,2) | '6' | 1 | ' 6' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '2' | 0 | ' 2' |
| J(0.5,1) | '6' | 1 | ' 6' |
| J(0.5,1.5) | '6' | 1 | ' 6' |
| J(0.5,2) | '6' | 1 | ' 6' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '2' | 0 | ' 2' |
| J(1,1) | '6' | 1 | ' 6' |
| J(1,1.5) | '6' | 1 | ' 6' |
| J(1,2) | '6' | 1 | ' 6' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '6' | 1 | ' 6' |
| J(1.5,1) | '6' | 1 | ' 6' |
| J(1.5,1.5) | '6' | 1 | ' 6' |
| J(1.5,2) | '6' | 1 | ' 6' |
| J(2,0) | '6' | 1 | ' 6' |
| J(2,0.5) | '6' | 1 | ' 6' |
| J(2,1) | '6' | 1 | ' 6' |
| J(2,1.5) | '6' | 1 | ' 6' |
| J(2,2) | '6' | 1 | ' 6' |
| R(0,1) | '6' | 1 | ' 6' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '2' | 0 | ' 2' |
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
| J(0,0.5) | '6' | 0 | ' 6' |
| J(0,1) | '9' | 1 | ' 9' |
| J(0,1.5) | '9' | 1 | ' 9' |
| J(0,2) | '9' | 1 | ' 9' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '6' | 0 | ' 6' |
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
| J(2,0) | '6' | 0 | ' 6' |
| J(2,0.5) | '9' | 1 | ' 9' |
| J(2,1) | '9' | 1 | ' 9' |
| J(2,1.5) | '9' | 1 | ' 9' |
| J(2,2) | '9' | 1 | ' 9' |
| R(0,1) | '9' | 1 | ' 9' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '6' | 0 | ' 6' |
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
| J(0,1) | '8' | 0 | ' 8' |
| J(0,1.5) | '7' | 1 | ' 7' |
| J(0,2) | '7' | 1 | ' 7' |
| J(0.5,0) | '8' | 0 | ' 8' |
| J(0.5,0.5) | '8' | 0 | ' 8' |
| J(0.5,1) | '7' | 1 | ' 7' |
| J(0.5,1.5) | '7' | 1 | ' 7' |
| J(0.5,2) | '7' | 1 | ' 7' |
| J(1,0) | '8' | 0 | ' 8' |
| J(1,0.5) | '8' | 0 | ' 8' |
| J(1,1) | '7' | 1 | ' 7' |
| J(1,1.5) | '7' | 1 | ' 7' |
| J(1,2) | '7' | 1 | ' 7' |
| J(1.5,0) | '8' | 0 | ' 8' |
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
| R(2,0) | '8' | 0 | ' 8' |
| R(0,2) | '7' | 1 | ' 7' |
| J(0,2)-U | '7' | 1 | ' 7' |
| J(0,2)-RU | '8' | 0 | ' 8' |

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
| J(1,0.5) | '8' | 1 | ' 8' |
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
| J(0,1) | '4' | 0 | ' 4' |
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
| J(0,2)-RU | '4' | 0 | ' 4' |

### P2-L0-0168 (animals): bridge elephant (O) → fly (S), token 35

**lookup** (PP-L0-0168): O's answer 2, S's answer 5

O, as read:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦ elephant⟧. Henry picked the fly.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2' |
| J(0,0.5) | '2' | 0 | ' 2' |
| J(0,1) | '5' | 1 | ' 5' |
| J(0,1.5) | '5' | 1 | ' 5' |
| J(0,2) | '5' | 1 | ' 5' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '2' | 0 | ' 2' |
| J(0.5,1) | '5' | 1 | ' 5' |
| J(0.5,1.5) | '5' | 1 | ' 5' |
| J(0.5,2) | '5' | 1 | ' 5' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '5' | 1 | ' 5' |
| J(1,1) | '5' | 1 | ' 5' |
| J(1,1.5) | '5' | 1 | ' 5' |
| J(1,2) | '5' | 1 | ' 5' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '5' | 1 | ' 5' |
| J(1.5,1) | '5' | 1 | ' 5' |
| J(1.5,1.5) | '5' | 1 | ' 5' |
| J(1.5,2) | '5' | 1 | ' 5' |
| J(2,0) | '2' | 0 | ' 2' |
| J(2,0.5) | '5' | 1 | ' 5' |
| J(2,1) | '5' | 1 | ' 5' |
| J(2,1.5) | '5' | 1 | ' 5' |
| J(2,2) | '5' | 1 | ' 5' |
| R(0,1) | '5' | 1 | ' 5' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '2' | 0 | ' 2' |
| R(0,2) | '5' | 1 | ' 5' |
| J(0,2)-U | '5' | 1 | ' 5' |
| J(0,2)-RU | '5' | 1 | ' 5' |

**recall** (PM-L0-0168): O's answer 4, S's answer 6

O, as read:

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦ elephant⟧. Henry picked the fly.
How many legs does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '4' | 0 | ' 4' |
| J(0,1) | '6' | 1 | ' 6' |
| J(0,1.5) | '6' | 1 | ' 6' |
| J(0,2) | '6' | 1 | ' 6' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '4' | 0 | ' 4' |
| J(0.5,1) | '6' | 1 | ' 6' |
| J(0.5,1.5) | '6' | 1 | ' 6' |
| J(0.5,2) | '6' | 1 | ' 6' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '6' | 1 | ' 6' |
| J(1,1) | '6' | 1 | ' 6' |
| J(1,1.5) | '6' | 1 | ' 6' |
| J(1,2) | '6' | 1 | ' 6' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '6' | 1 | ' 6' |
| J(1.5,1) | '6' | 1 | ' 6' |
| J(1.5,1.5) | '6' | 1 | ' 6' |
| J(1.5,2) | '6' | 1 | ' 6' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '6' | 1 | ' 6' |
| J(2,1) | '6' | 1 | ' 6' |
| J(2,1.5) | '6' | 1 | ' 6' |
| J(2,2) | '6' | 1 | ' 6' |
| R(0,1) | '6' | 1 | ' 6' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '4' | 0 | ' 4' |
| R(0,2) | '6' | 1 | ' 6' |
| J(0,2)-U | '6' | 1 | ' 6' |
| J(0,2)-RU | '6' | 1 | ' 6' |

### P2-L0-0180 (animals): bridge beetle (O) → eagle (S), token 32

**lookup** (PP-L0-0180): O's answer 7, S's answer 3

O, as read:

```
<|im_start|>user
The locker of the eagle is three. Ivy picked the bear. Emma picked the eagle. The locker of the beetle is seven. Olivia picked the⟦ beetle⟧. The locker of the bear is one.
Which locker belongs to Olivia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '7' | 0 | ' 7' |
| J(0,0.5) | '7' | 0 | ' 7' |
| J(0,1) | '3' | 1 | ' 3' |
| J(0,1.5) | '3' | 1 | ' 3' |
| J(0,2) | '1' | 0 | ' 1' |
| J(0.5,0) | '7' | 0 | ' 7' |
| J(0.5,0.5) | '7' | 0 | ' 7' |
| J(0.5,1) | '3' | 1 | ' 3' |
| J(0.5,1.5) | '3' | 1 | ' 1' |
| J(0.5,2) | '1' | 0 | ' 1' |
| J(1,0) | '7' | 0 | ' 7' |
| J(1,0.5) | '3' | 1 | ' 3' |
| J(1,1) | '3' | 1 | ' 3' |
| J(1,1.5) | '1' | 0 | ' 1' |
| J(1,2) | '1' | 0 | ' 1' |
| J(1.5,0) | '7' | 0 | ' 7' |
| J(1.5,0.5) | '3' | 1 | ' 3' |
| J(1.5,1) | '3' | 1 | ' 3' |
| J(1.5,1.5) | '1' | 0 | ' 1' |
| J(1.5,2) | '1' | 0 | ' 1' |
| J(2,0) | '7' | 0 | ' 7' |
| J(2,0.5) | '3' | 1 | ' 3' |
| J(2,1) | '3' | 1 | ' 3' |
| J(2,1.5) | '1' | 0 | ' 1' |
| J(2,2) | '1' | 0 | ' 1' |
| R(0,1) | '3' | 1 | ' 3' |
| R(1,0) | '7' | 0 | ' 7' |
| R(2,0) | '7' | 0 | ' 7' |
| R(0,2) | '1' | 0 | ' 1' |
| J(0,2)-U | '3' | 1 | ' 3' |
| J(0,2)-RU | '7' | 0 | ' 7' |

**recall** (PM-L0-0180): O's answer 6, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the eagle is three. Ivy picked the bear. Emma picked the eagle. The locker of the beetle is seven. Olivia picked the⟦ beetle⟧. The locker of the bear is one.
How many legs does Olivia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6' |
| J(0,0.5) | '6' | 0 | ' 6' |
| J(0,1) | '6' | 0 | ' 6' |
| J(0,1.5) | '6' | 0 | ' 6' |
| J(0,2) | '6' | 0 | ' 6' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '6' | 0 | ' 6' |
| J(0.5,1) | '6' | 0 | ' 6' |
| J(0.5,1.5) | '6' | 0 | ' 6' |
| J(0.5,2) | '6' | 0 | ' 6' |
| J(1,0) | '6' | 0 | ' 6' |
| J(1,0.5) | '6' | 0 | ' 6' |
| J(1,1) | '6' | 0 | ' 6' |
| J(1,1.5) | '6' | 0 | ' 6' |
| J(1,2) | '6' | 0 | ' 6' |
| J(1.5,0) | '6' | 0 | ' 6' |
| J(1.5,0.5) | '6' | 0 | ' 6' |
| J(1.5,1) | '6' | 0 | ' 6' |
| J(1.5,1.5) | '6' | 0 | ' 6' |
| J(1.5,2) | '6' | 0 | ' 6' |
| J(2,0) | '6' | 0 | ' 6' |
| J(2,0.5) | '6' | 0 | ' 6' |
| J(2,1) | '6' | 0 | ' 6' |
| J(2,1.5) | '6' | 0 | ' 6' |
| J(2,2) | '6' | 0 | ' 6' |
| R(0,1) | '6' | 0 | ' 6' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '6' | 0 | ' 6' |
| R(0,2) | '6' | 0 | ' 6' |
| J(0,2)-U | '6' | 0 | ' 6' |
| J(0,2)-RU | '6' | 0 | ' 6' |

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
| J(0,1) | '2' | 0 | ' 2' |
| J(0,1.5) | '6' | 1 | ' 6' |
| J(0,2) | '6' | 1 | ' 6' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '2' | 0 | ' 2' |
| J(0.5,1) | '6' | 1 | ' 6' |
| J(0.5,1.5) | '6' | 1 | ' 6' |
| J(0.5,2) | '6' | 1 | ' 6' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '2' | 0 | ' 2' |
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
| J(0,0.5) | '7' | 0 | ' 7' |
| J(0,1) | '7' | 0 | ' 7' |
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
| J(2,0) | '4' | 1 | ' 4' |
| J(2,0.5) | '4' | 1 | ' 4' |
| J(2,1) | '4' | 1 | ' 4' |
| J(2,1.5) | '4' | 1 | ' 4' |
| J(2,2) | '4' | 1 | ' 4' |
| R(0,1) | '4' | 1 | ' 4' |
| R(1,0) | '7' | 0 | ' 7' |
| R(2,0) | '7' | 0 | ' 7' |
| R(0,2) | '4' | 1 | ' 4' |
| J(0,2)-U | '4' | 1 | ' 4' |
| J(0,2)-RU | '3' | 0 | ' 3' |

## muse-glimmer-30b: muse30_x49_1, 10 random items of 68 (seed 0)

### P2-L0-0021 (animals): bridge sheep (O) → goose (S), token 79

**lookup** (PP-L0-0021): O's answer 5, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the goose is eight. The locker of the sheep is five. The locker of the owl is four. Lucy picked the owl. Finn picked the goose. Ruby picked the⟦ sheep⟧.
Which locker belongs to Ruby's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '5' | 0 | ' 5' |
| J(0,0.5) | '5' | 0 | ' 5' |
| J(0,1) | '8' | 1 | ' 8' |
| J(0,1.5) | '8' | 1 | ' 8' |
| J(0,2) | '8' | 1 | ' 8' |
| J(0.5,0) | '5' | 0 | ' 5' |
| J(0.5,0.5) | '5' | 0 | ' 5' |
| J(0.5,1) | '8' | 1 | ' 8' |
| J(0.5,1.5) | '8' | 1 | ' 8' |
| J(0.5,2) | '8' | 1 | ' 8' |
| J(1,0) | '5' | 0 | ' 5' |
| J(1,0.5) | '5' | 0 | ' 5' |
| J(1,1) | '8' | 1 | ' 8' |
| J(1,1.5) | '8' | 1 | ' 8' |
| J(1,2) | '8' | 1 | ' 8' |
| J(1.5,0) | '5' | 0 | ' 5' |
| J(1.5,0.5) | '5' | 0 | ' 5' |
| J(1.5,1) | '8' | 1 | ' 8' |
| J(1.5,1.5) | '8' | 1 | ' 8' |
| J(1.5,2) | '8' | 1 | ' 8' |
| J(2,0) | '5' | 0 | ' 5' |
| J(2,0.5) | '5' | 0 | ' 5' |
| J(2,1) | '8' | 1 | ' 8' |
| J(2,1.5) | '8' | 1 | ' 8' |
| J(2,2) | '8' | 1 | ' 8' |
| R(0,1) | '8' | 1 | ' 8' |
| R(1,0) | '5' | 0 | ' 5' |
| R(2,0) | '5' | 0 | ' 5' |
| R(0,2) | '8' | 1 | ' 8' |
| J(0,2)-U | '5' | 0 | ' 5' |
| J(0,2)-RU | '8' | 1 | ' 8' |

**recall** (PM-L0-0021): O's answer 4, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the goose is eight. The locker of the sheep is five. The locker of the owl is four. Lucy picked the owl. Finn picked the goose. Ruby picked the⟦ sheep⟧.
How many legs does Ruby's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '4' | 0 | ' 4' |
| J(0,1) | '4' | 0 | ' 4' |
| J(0,1.5) | '4' | 0 | ' 4' |
| J(0,2) | '4' | 0 | ' 4' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '4' | 0 | ' 4' |
| J(0.5,1) | '4' | 0 | ' 4' |
| J(0.5,1.5) | '4' | 0 | ' 4' |
| J(0.5,2) | '4' | 0 | ' 4' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '4' | 0 | ' 4' |
| J(1,1) | '4' | 0 | ' 4' |
| J(1,1.5) | '4' | 0 | ' 4' |
| J(1,2) | '4' | 0 | ' 4' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '4' | 0 | ' 4' |
| J(1.5,1) | '4' | 0 | ' 4' |
| J(1.5,1.5) | '4' | 0 | ' 4' |
| J(1.5,2) | '4' | 0 | ' 4' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '4' | 0 | ' 4' |
| J(2,1) | '4' | 0 | ' 4' |
| J(2,1.5) | '4' | 0 | ' 4' |
| J(2,2) | '4' | 0 | ' 4' |
| R(0,1) | '4' | 0 | ' 4' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '4' | 0 | ' 4' |
| R(0,2) | '4' | 0 | ' 4' |
| J(0,2)-U | '4' | 0 | ' 4' |
| J(0,2)-RU | '4' | 0 | ' 4' |

### P2-L0-0069 (animals): bridge sheep (O) → butterfly (S), token 77

**lookup** (PP-L0-0069): O's answer 3, S's answer 7

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ sheep⟧. Ella picked the butterfly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3' |
| J(0,0.5) | '3' | 0 | ' 3' |
| J(0,1) | '7' | 1 | ' 7' |
| J(0,1.5) | '3' | 0 | ' 3' |
| J(0,2) | '3' | 0 | ' 3' |
| J(0.5,0) | '3' | 0 | ' 3' |
| J(0.5,0.5) | '3' | 0 | ' 3' |
| J(0.5,1) | '7' | 1 | ' 7' |
| J(0.5,1.5) | '3' | 0 | ' 3' |
| J(0.5,2) | '3' | 0 | ' 3' |
| J(1,0) | '3' | 0 | ' 3' |
| J(1,0.5) | '3' | 0 | ' 3' |
| J(1,1) | '7' | 1 | ' 7' |
| J(1,1.5) | '3' | 0 | ' 3' |
| J(1,2) | '3' | 0 | ' 3' |
| J(1.5,0) | '3' | 0 | ' 3' |
| J(1.5,0.5) | '3' | 0 | ' 3' |
| J(1.5,1) | '7' | 1 | ' 7' |
| J(1.5,1.5) | '3' | 0 | ' 3' |
| J(1.5,2) | '3' | 0 | ' 3' |
| J(2,0) | '3' | 0 | ' 3' |
| J(2,0.5) | '7' | 1 | ' 7' |
| J(2,1) | '7' | 1 | ' 7' |
| J(2,1.5) | '3' | 0 | ' 3' |
| J(2,2) | '3' | 0 | ' 3' |
| R(0,1) | '7' | 1 | ' 7' |
| R(1,0) | '3' | 0 | ' 3' |
| R(2,0) | '3' | 0 | ' 3' |
| R(0,2) | '3' | 0 | ' 3' |
| J(0,2)-U | '3' | 0 | ' 3' |
| J(0,2)-RU | '3' | 0 | ' 3' |

**recall** (PM-L0-0069): O's answer 4, S's answer 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ sheep⟧. Ella picked the butterfly.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '4' | 0 | ' 4' |
| J(0,1) | '4' | 0 | ' 4' |
| J(0,1.5) | '4' | 0 | ' 4' |
| J(0,2) | '4' | 0 | ' 4' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '4' | 0 | ' 4' |
| J(0.5,1) | '4' | 0 | ' 4' |
| J(0.5,1.5) | '4' | 0 | ' 4' |
| J(0.5,2) | '4' | 0 | ' 4' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '4' | 0 | ' 4' |
| J(1,1) | '4' | 0 | ' 4' |
| J(1,1.5) | '4' | 0 | ' 4' |
| J(1,2) | '4' | 0 | ' 4' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '4' | 0 | ' 4' |
| J(1.5,1) | '4' | 0 | ' 4' |
| J(1.5,1.5) | '4' | 0 | ' 4' |
| J(1.5,2) | '4' | 0 | ' 4' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '4' | 0 | ' 4' |
| J(2,1) | '4' | 0 | ' 4' |
| J(2,1.5) | '4' | 0 | ' 4' |
| J(2,2) | '4' | 0 | ' 4' |
| R(0,1) | '4' | 0 | ' 4' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '4' | 0 | ' 4' |
| R(0,2) | '4' | 0 | ' 4' |
| J(0,2)-U | '4' | 0 | ' 4' |
| J(0,2)-RU | '4' | 0 | ' 4' |

### P2-L0-0096 (animals): bridge bee (O) → spider (S), token 82

**lookup** (PP-L0-0096): O's answer 1, S's answer 5

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
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
| J(1,0.5) | '1' | 0 | ' 1' |
| J(1,1) | '5' | 1 | ' 5' |
| J(1,1.5) | '5' | 1 | ' 5' |
| J(1,2) | '1' | 0 | ' 1' |
| J(1.5,0) | '1' | 0 | ' 1' |
| J(1.5,0.5) | '5' | 1 | ' 5' |
| J(1.5,1) | '5' | 1 | ' 5' |
| J(1.5,1.5) | '5' | 1 | ' 5' |
| J(1.5,2) | '1' | 0 | ' 1' |
| J(2,0) | '1' | 0 | ' 1' |
| J(2,0.5) | '5' | 1 | ' 5' |
| J(2,1) | '5' | 1 | ' 5' |
| J(2,1.5) | '5' | 1 | ' 5' |
| J(2,2) | '1' | 0 | ' 1' |
| R(0,1) | '5' | 1 | ' 5' |
| R(1,0) | '1' | 0 | ' 1' |
| R(2,0) | '1' | 0 | ' 1' |
| R(0,2) | '5' | 1 | ' 5' |
| J(0,2)-U | '1' | 0 | ' 1' |
| J(0,2)-RU | '5' | 1 | ' 5' |

**recall** (PM-L0-0096): O's answer 6, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6' |
| J(0,0.5) | '6' | 0 | ' 6' |
| J(0,1) | '6' | 0 | ' 6' |
| J(0,1.5) | '6' | 0 | ' 6' |
| J(0,2) | '6' | 0 | ' 6' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '6' | 0 | ' 6' |
| J(0.5,1) | '6' | 0 | ' 6' |
| J(0.5,1.5) | '6' | 0 | ' 6' |
| J(0.5,2) | '6' | 0 | ' 6' |
| J(1,0) | '6' | 0 | ' 6' |
| J(1,0.5) | '6' | 0 | ' 6' |
| J(1,1) | '8' | 1 | ' 8' |
| J(1,1.5) | '6' | 0 | ' 6' |
| J(1,2) | '6' | 0 | ' 6' |
| J(1.5,0) | '6' | 0 | ' 6' |
| J(1.5,0.5) | '6' | 0 | ' 6' |
| J(1.5,1) | '8' | 1 | ' 8' |
| J(1.5,1.5) | '6' | 0 | ' 6' |
| J(1.5,2) | '6' | 0 | ' 6' |
| J(2,0) | '6' | 0 | ' 6' |
| J(2,0.5) | '6' | 0 | ' 6' |
| J(2,1) | '8' | 1 | ' 8' |
| J(2,1.5) | '6' | 0 | ' 6' |
| J(2,2) | '6' | 0 | ' 6' |
| R(0,1) | '8' | 1 | ' 8' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '6' | 0 | ' 6' |
| R(0,2) | '6' | 0 | ' 6' |
| J(0,2)-U | '6' | 0 | ' 6' |
| J(0,2)-RU | '6' | 0 | ' 6' |

### P2-L0-0133 (elements): bridge carbon (O) → oxygen (S), token 72

**lookup** (PP-L0-0133): O's answer 3, S's answer 7

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked⟦ carbon⟧. Eva picked helium.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3' |
| J(0,0.5) | '3' | 0 | ' 3' |
| J(0,1) | '7' | 1 | ' 7' |
| J(0,1.5) | '7' | 1 | ' 7' |
| J(0,2) | '7' | 1 | ' 7' |
| J(0.5,0) | '3' | 0 | ' 3' |
| J(0.5,0.5) | '3' | 0 | ' 3' |
| J(0.5,1) | '7' | 1 | ' 7' |
| J(0.5,1.5) | '7' | 1 | ' 7' |
| J(0.5,2) | '7' | 1 | ' 7' |
| J(1,0) | '3' | 0 | ' 3' |
| J(1,0.5) | '7' | 1 | ' 7' |
| J(1,1) | '7' | 1 | ' 7' |
| J(1,1.5) | '7' | 1 | ' 7' |
| J(1,2) | '7' | 1 | ' 7' |
| J(1.5,0) | '3' | 0 | ' 3' |
| J(1.5,0.5) | '7' | 1 | ' 7' |
| J(1.5,1) | '7' | 1 | ' 7' |
| J(1.5,1.5) | '7' | 1 | ' 7' |
| J(1.5,2) | '7' | 1 | ' 7' |
| J(2,0) | '3' | 0 | ' 3' |
| J(2,0.5) | '7' | 1 | ' 7' |
| J(2,1) | '7' | 1 | ' 7' |
| J(2,1.5) | '7' | 1 | ' 7' |
| J(2,2) | '7' | 1 | ' 7' |
| R(0,1) | '7' | 1 | ' 7' |
| R(1,0) | '3' | 0 | ' 3' |
| R(2,0) | '3' | 0 | ' 3' |
| R(0,2) | '7' | 1 | ' 7' |
| J(0,2)-U | '7' | 1 | ' 7' |
| J(0,2)-RU | '7' | 1 | ' 7' |

**recall** (PM-L0-0133): O's answer 6, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked⟦ carbon⟧. Eva picked helium.
What is the atomic number of Eric's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6' |
| J(0,0.5) | '6' | 0 | ' 6' |
| J(0,1) | '6' | 0 | ' 6' |
| J(0,1.5) | '6' | 0 | ' 6' |
| J(0,2) | '6' | 0 | ' 6' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '6' | 0 | ' 6' |
| J(0.5,1) | '6' | 0 | ' 6' |
| J(0.5,1.5) | '6' | 0 | ' 6' |
| J(0.5,2) | '6' | 0 | ' 6' |
| J(1,0) | '6' | 0 | ' 6' |
| J(1,0.5) | '6' | 0 | ' 6' |
| J(1,1) | '6' | 0 | ' 6' |
| J(1,1.5) | '6' | 0 | ' 6' |
| J(1,2) | '6' | 0 | ' 6' |
| J(1.5,0) | '6' | 0 | ' 6' |
| J(1.5,0.5) | '8' | 1 | ' 8' |
| J(1.5,1) | '6' | 0 | ' 6' |
| J(1.5,1.5) | '6' | 0 | ' 6' |
| J(1.5,2) | '6' | 0 | ' 6' |
| J(2,0) | '6' | 0 | ' 6' |
| J(2,0.5) | '8' | 1 | ' 8' |
| J(2,1) | '6' | 0 | ' 6' |
| J(2,1.5) | '6' | 0 | ' 6' |
| J(2,2) | '6' | 0 | ' 6' |
| R(0,1) | '6' | 0 | ' 6' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '6' | 0 | ' 6' |
| R(0,2) | '6' | 0 | ' 6' |
| J(0,2)-U | '6' | 0 | ' 6' |
| J(0,2)-RU | '6' | 0 | ' 6' |

### P2-L0-0219 (animals): bridge sheep (O) → butterfly (S), token 82

**lookup** (PP-L0-0219): O's answer 6, S's answer 7

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the sheep is 6. The locker of the butterfly is 7. Eve picked the butterfly. Owen picked the camel. The locker of the camel is 9. Diana picked the⟦ sheep⟧.
Which locker belongs to Diana's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6' |
| J(0,0.5) | '7' | 1 | ' 7' |
| J(0,1) | '7' | 1 | ' 7' |
| J(0,1.5) | '7' | 1 | ' 7' |
| J(0,2) | '7' | 1 | ' 7' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '7' | 1 | ' 7' |
| J(0.5,1) | '7' | 1 | ' 7' |
| J(0.5,1.5) | '7' | 1 | ' 7' |
| J(0.5,2) | '7' | 1 | ' 7' |
| J(1,0) | '6' | 0 | ' 6' |
| J(1,0.5) | '7' | 1 | ' 7' |
| J(1,1) | '7' | 1 | ' 7' |
| J(1,1.5) | '7' | 1 | ' 7' |
| J(1,2) | '7' | 1 | ' 7' |
| J(1.5,0) | '6' | 0 | ' 6' |
| J(1.5,0.5) | '7' | 1 | ' 7' |
| J(1.5,1) | '7' | 1 | ' 7' |
| J(1.5,1.5) | '7' | 1 | ' 7' |
| J(1.5,2) | '7' | 1 | ' 7' |
| J(2,0) | '6' | 0 | ' 6' |
| J(2,0.5) | '7' | 1 | ' 7' |
| J(2,1) | '7' | 1 | ' 7' |
| J(2,1.5) | '7' | 1 | ' 7' |
| J(2,2) | '7' | 1 | ' 7' |
| R(0,1) | '7' | 1 | ' 7' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '6' | 0 | ' 6' |
| R(0,2) | '7' | 1 | ' 7' |
| J(0,2)-U | '7' | 1 | ' 7' |
| J(0,2)-RU | '7' | 1 | ' 7' |

**recall** (PM-L0-0219): O's answer 4, S's answer 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the sheep is 6. The locker of the butterfly is 7. Eve picked the butterfly. Owen picked the camel. The locker of the camel is 9. Diana picked the⟦ sheep⟧.
How many legs does Diana's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '4' | 0 | ' 4' |
| J(0,1) | '4' | 0 | ' 4' |
| J(0,1.5) | '4' | 0 | ' 4' |
| J(0,2) | '4' | 0 | ' 4' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '4' | 0 | ' 4' |
| J(0.5,1) | '4' | 0 | ' 4' |
| J(0.5,1.5) | '4' | 0 | ' 4' |
| J(0.5,2) | '4' | 0 | ' 4' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '6' | 1 | ' 6' |
| J(1,1) | '4' | 0 | ' 4' |
| J(1,1.5) | '4' | 0 | ' 4' |
| J(1,2) | '4' | 0 | ' 4' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '6' | 1 | ' 6' |
| J(1.5,1) | '4' | 0 | ' 4' |
| J(1.5,1.5) | '4' | 0 | ' 4' |
| J(1.5,2) | '4' | 0 | ' 4' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '6' | 1 | ' 6' |
| J(2,1) | '4' | 0 | ' 4' |
| J(2,1.5) | '4' | 0 | ' 4' |
| J(2,2) | '4' | 0 | ' 4' |
| R(0,1) | '6' | 1 | ' 6' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '4' | 0 | ' 4' |
| R(0,2) | '4' | 0 | ' 4' |
| J(0,2)-U | '4' | 0 | ' 4' |
| J(0,2)-RU | '4' | 0 | ' 4' |

### P2-L0-0221 (greek): bridge beta (O) → delta (S), token 63

**lookup** (PP-L0-0221): O's answer 1, S's answer 9

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of delta is nine. The locker of beta is one. Owen picked iota. Iris picked⟦ beta⟧. The locker of iota is five. Mark picked delta.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '1' | 0 | ' 1' |
| J(0,0.5) | '1' | 0 | ' 1' |
| J(0,1) | '9' | 1 | ' 9' |
| J(0,1.5) | '9' | 1 | ' 9' |
| J(0,2) | '9' | 1 | ' 9' |
| J(0.5,0) | '1' | 0 | ' 1' |
| J(0.5,0.5) | '1' | 0 | ' 1' |
| J(0.5,1) | '9' | 1 | ' 9' |
| J(0.5,1.5) | '9' | 1 | ' 9' |
| J(0.5,2) | '9' | 1 | ' 9' |
| J(1,0) | '1' | 0 | ' 1' |
| J(1,0.5) | '1' | 0 | ' 1' |
| J(1,1) | '9' | 1 | ' 9' |
| J(1,1.5) | '9' | 1 | ' 9' |
| J(1,2) | '9' | 1 | ' 9' |
| J(1.5,0) | '1' | 0 | ' 1' |
| J(1.5,0.5) | '9' | 1 | ' 9' |
| J(1.5,1) | '9' | 1 | ' 9' |
| J(1.5,1.5) | '9' | 1 | ' 9' |
| J(1.5,2) | '9' | 1 | ' 9' |
| J(2,0) | '1' | 0 | ' 1' |
| J(2,0.5) | '9' | 1 | ' 9' |
| J(2,1) | '9' | 1 | ' 9' |
| J(2,1.5) | '9' | 1 | ' 9' |
| J(2,2) | '9' | 1 | ' 9' |
| R(0,1) | '9' | 1 | ' 9' |
| R(1,0) | '1' | 0 | ' 1' |
| R(2,0) | '1' | 0 | ' 1' |
| R(0,2) | '9' | 1 | ' 9' |
| J(0,2)-U | '9' | 1 | ' 9' |
| J(0,2)-RU | '9' | 1 | ' 9' |

**recall** (PM-L0-0221): O's answer 2, S's answer 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of delta is nine. The locker of beta is one. Owen picked iota. Iris picked⟦ beta⟧. The locker of iota is five. Mark picked delta.
Which position in the Greek alphabet does Iris's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2' |
| J(0,0.5) | '4' | 1 | ' 4' |
| J(0,1) | '4' | 1 | ' 4' |
| J(0,1.5) | '4' | 1 | ' 4' |
| J(0,2) | '9' | 0 | ' 9' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '4' | 1 | ' 4' |
| J(0.5,1) | '4' | 1 | ' 4' |
| J(0.5,1.5) | '4' | 1 | ' 4' |
| J(0.5,2) | '9' | 0 | ' 9' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '4' | 1 | ' 4' |
| J(1,1) | '4' | 1 | ' 4' |
| J(1,1.5) | '4' | 1 | ' 4' |
| J(1,2) | '9' | 0 | ' 9' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '4' | 1 | ' 4' |
| J(1.5,1) | '4' | 1 | ' 4' |
| J(1.5,1.5) | '4' | 1 | ' 4' |
| J(1.5,2) | '9' | 0 | ' 9' |
| J(2,0) | '4' | 1 | ' 4' |
| J(2,0.5) | '4' | 1 | ' 4' |
| J(2,1) | '4' | 1 | ' 4' |
| J(2,1.5) | '4' | 1 | ' 4' |
| J(2,2) | '9' | 0 | ' 9' |
| R(0,1) | '4' | 1 | ' 4' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '2' | 0 | ' 2' |
| R(0,2) | '9' | 0 | ' 9' |
| J(0,2)-U | '4' | 1 | ' 4' |
| J(0,2)-RU | '4' | 1 | ' 4' |

### P2-L0-0243 (animals): bridge spider (O) → tiger (S), token 69

**lookup** (PP-L0-0243): O's answer 4, S's answer 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is four. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the⟦ spider⟧. Alice picked the tiger. Henry picked the sheep.
Which locker belongs to Olivia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '6' | 1 | ' 6' |
| J(0,1) | '6' | 1 | ' 6' |
| J(0,1.5) | '6' | 1 | ' 6' |
| J(0,2) | '6' | 1 | ' 6' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '6' | 1 | ' 6' |
| J(0.5,1) | '6' | 1 | ' 6' |
| J(0.5,1.5) | '6' | 1 | ' 6' |
| J(0.5,2) | '6' | 1 | ' 6' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '6' | 1 | ' 6' |
| J(1,1) | '6' | 1 | ' 6' |
| J(1,1.5) | '6' | 1 | ' 6' |
| J(1,2) | '6' | 1 | ' 6' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '6' | 1 | ' 6' |
| J(1.5,1) | '6' | 1 | ' 6' |
| J(1.5,1.5) | '6' | 1 | ' 6' |
| J(1.5,2) | '6' | 1 | ' 6' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '6' | 1 | ' 6' |
| J(2,1) | '6' | 1 | ' 6' |
| J(2,1.5) | '6' | 1 | ' 6' |
| J(2,2) | '6' | 1 | ' 6' |
| R(0,1) | '6' | 1 | ' 6' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '4' | 0 | ' 4' |
| R(0,2) | '6' | 1 | ' 6' |
| J(0,2)-U | '6' | 1 | ' 6' |
| J(0,2)-RU | '6' | 1 | ' 6' |

**recall** (PM-L0-0243): O's answer 8, S's answer 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is four. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the⟦ spider⟧. Alice picked the tiger. Henry picked the sheep.
How many legs does Olivia's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '8' | 0 | ' 8' |
| J(0,0.5) | '8' | 0 | ' 8' |
| J(0,1) | '8' | 0 | ' 8' |
| J(0,1.5) | '8' | 0 | ' 8' |
| J(0,2) | '8' | 0 | ' 8' |
| J(0.5,0) | '8' | 0 | ' 8' |
| J(0.5,0.5) | '8' | 0 | ' 8' |
| J(0.5,1) | '8' | 0 | ' 8' |
| J(0.5,1.5) | '8' | 0 | ' 8' |
| J(0.5,2) | '8' | 0 | ' 8' |
| J(1,0) | '8' | 0 | ' 8' |
| J(1,0.5) | '8' | 0 | ' 8' |
| J(1,1) | '8' | 0 | ' 8' |
| J(1,1.5) | '8' | 0 | ' 8' |
| J(1,2) | '8' | 0 | ' 8' |
| J(1.5,0) | '8' | 0 | ' 8' |
| J(1.5,0.5) | '8' | 0 | ' 8' |
| J(1.5,1) | '8' | 0 | ' 8' |
| J(1.5,1.5) | '8' | 0 | ' 8' |
| J(1.5,2) | '8' | 0 | ' 8' |
| J(2,0) | '8' | 0 | ' 8' |
| J(2,0.5) | '8' | 0 | ' 8' |
| J(2,1) | '8' | 0 | ' 8' |
| J(2,1.5) | '8' | 0 | ' 8' |
| J(2,2) | '8' | 0 | ' 8' |
| R(0,1) | '8' | 0 | ' 8' |
| R(1,0) | '8' | 0 | ' 8' |
| R(2,0) | '8' | 0 | ' 8' |
| R(0,2) | '8' | 0 | ' 8' |
| J(0,2)-U | '8' | 0 | ' 8' |
| J(0,2)-RU | '8' | 0 | ' 8' |

### P2-L0-0255 (animals): bridge chicken (O) → frog (S), token 67

**lookup** (PP-L0-0255): O's answer 1, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the frog is three. Frank picked the beetle. The locker of the chicken is one. Iris picked the⟦ chicken⟧. The locker of the beetle is five. Nina picked the frog.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '1' | 0 | ' 1' |
| J(0,0.5) | '1' | 0 | ' 1' |
| J(0,1) | '1' | 0 | ' 1' |
| J(0,1.5) | '1' | 0 | ' 1' |
| J(0,2) | '1' | 0 | ' 1' |
| J(0.5,0) | '1' | 0 | ' 1' |
| J(0.5,0.5) | '1' | 0 | ' 1' |
| J(0.5,1) | '1' | 0 | ' 1' |
| J(0.5,1.5) | '1' | 0 | ' 1' |
| J(0.5,2) | '1' | 0 | ' 1' |
| J(1,0) | '1' | 0 | ' 1' |
| J(1,0.5) | '1' | 0 | ' 1' |
| J(1,1) | '1' | 0 | ' 1' |
| J(1,1.5) | '1' | 0 | ' 1' |
| J(1,2) | '1' | 0 | ' 1' |
| J(1.5,0) | '1' | 0 | ' 1' |
| J(1.5,0.5) | '1' | 0 | ' 1' |
| J(1.5,1) | '1' | 0 | ' 1' |
| J(1.5,1.5) | '1' | 0 | ' 1' |
| J(1.5,2) | '3' | 1 | ' 3' |
| J(2,0) | '1' | 0 | ' 1' |
| J(2,0.5) | '1' | 0 | ' 1' |
| J(2,1) | '1' | 0 | ' 1' |
| J(2,1.5) | '1' | 0 | ' 1' |
| J(2,2) | '3' | 1 | ' 3' |
| R(0,1) | '1' | 0 | ' 1' |
| R(1,0) | '1' | 0 | ' 1' |
| R(2,0) | '1' | 0 | ' 1' |
| R(0,2) | '3' | 1 | ' 3' |
| J(0,2)-U | '1' | 0 | ' 1' |
| J(0,2)-RU | '1' | 0 | ' 1' |

**recall** (PM-L0-0255): O's answer 2, S's answer 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the frog is three. Frank picked the beetle. The locker of the chicken is one. Iris picked the⟦ chicken⟧. The locker of the beetle is five. Nina picked the frog.
How many legs does Iris's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '2' | 0 | ' 2' |
| J(0,0.5) | '2' | 0 | ' 2' |
| J(0,1) | '2' | 0 | ' 2' |
| J(0,1.5) | '2' | 0 | ' 2' |
| J(0,2) | '2' | 0 | ' 2' |
| J(0.5,0) | '2' | 0 | ' 2' |
| J(0.5,0.5) | '2' | 0 | ' 2' |
| J(0.5,1) | '2' | 0 | ' 2' |
| J(0.5,1.5) | '2' | 0 | ' 2' |
| J(0.5,2) | '2' | 0 | ' 2' |
| J(1,0) | '2' | 0 | ' 2' |
| J(1,0.5) | '2' | 0 | ' 2' |
| J(1,1) | '2' | 0 | ' 2' |
| J(1,1.5) | '2' | 0 | ' 2' |
| J(1,2) | '2' | 0 | ' 2' |
| J(1.5,0) | '2' | 0 | ' 2' |
| J(1.5,0.5) | '2' | 0 | ' 2' |
| J(1.5,1) | '2' | 0 | ' 2' |
| J(1.5,1.5) | '2' | 0 | ' 2' |
| J(1.5,2) | '2' | 0 | ' 2' |
| J(2,0) | '2' | 0 | ' 2' |
| J(2,0.5) | '2' | 0 | ' 2' |
| J(2,1) | '2' | 0 | ' 2' |
| J(2,1.5) | '2' | 0 | ' 2' |
| J(2,2) | '2' | 0 | ' 2' |
| R(0,1) | '2' | 0 | ' 2' |
| R(1,0) | '2' | 0 | ' 2' |
| R(2,0) | '2' | 0 | ' 2' |
| R(0,2) | '2' | 0 | ' 2' |
| J(0,2)-U | '2' | 0 | ' 2' |
| J(0,2)-RU | '2' | 0 | ' 2' |

### P2-L0-0273 (animals): bridge fox (O) → turkey (S), token 77

**lookup** (PP-L0-0273): O's answer 6, S's answer 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 4. The locker of the fox is 6. Tom picked the frog. The locker of the frog is 7. Finn picked the⟦ fox⟧. Sean picked the turkey.
Which locker belongs to Finn's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '6' | 0 | ' 6' |
| J(0,0.5) | '6' | 0 | ' 6' |
| J(0,1) | '4' | 1 | ' 4' |
| J(0,1.5) | '4' | 1 | ' 4' |
| J(0,2) | '4' | 1 | ' 4' |
| J(0.5,0) | '6' | 0 | ' 6' |
| J(0.5,0.5) | '6' | 0 | ' 6' |
| J(0.5,1) | '4' | 1 | ' 4' |
| J(0.5,1.5) | '4' | 1 | ' 4' |
| J(0.5,2) | '4' | 1 | ' 4' |
| J(1,0) | '6' | 0 | ' 6' |
| J(1,0.5) | '4' | 1 | ' 4' |
| J(1,1) | '4' | 1 | ' 4' |
| J(1,1.5) | '4' | 1 | ' 4' |
| J(1,2) | '4' | 1 | ' 4' |
| J(1.5,0) | '6' | 0 | ' 6' |
| J(1.5,0.5) | '4' | 1 | ' 4' |
| J(1.5,1) | '4' | 1 | ' 4' |
| J(1.5,1.5) | '4' | 1 | ' 4' |
| J(1.5,2) | '4' | 1 | ' 4' |
| J(2,0) | '6' | 0 | ' 6' |
| J(2,0.5) | '4' | 1 | ' 4' |
| J(2,1) | '4' | 1 | ' 4' |
| J(2,1.5) | '4' | 1 | ' 4' |
| J(2,2) | '4' | 1 | ' 4' |
| R(0,1) | '4' | 1 | ' 4' |
| R(1,0) | '6' | 0 | ' 6' |
| R(2,0) | '6' | 0 | ' 6' |
| R(0,2) | '4' | 1 | ' 4' |
| J(0,2)-U | '4' | 1 | ' 4' |
| J(0,2)-RU | '4' | 1 | ' 4' |

**recall** (PM-L0-0273): O's answer 4, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 4. The locker of the fox is 6. Tom picked the frog. The locker of the frog is 7. Finn picked the⟦ fox⟧. Sean picked the turkey.
How many legs does Finn's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '4' | 0 | ' 4' |
| J(0,1) | '4' | 0 | ' 4' |
| J(0,1.5) | '4' | 0 | ' 4' |
| J(0,2) | '4' | 0 | ' 4' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '4' | 0 | ' 4' |
| J(0.5,1) | '4' | 0 | ' 4' |
| J(0.5,1.5) | '4' | 0 | ' 4' |
| J(0.5,2) | '4' | 0 | ' 4' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '4' | 0 | ' 4' |
| J(1,1) | '4' | 0 | ' 4' |
| J(1,1.5) | '4' | 0 | ' 4' |
| J(1,2) | '4' | 0 | ' 4' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '2' | 1 | ' 2' |
| J(1.5,1) | '4' | 0 | ' 4' |
| J(1.5,1.5) | '4' | 0 | ' 4' |
| J(1.5,2) | '4' | 0 | ' 4' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '2' | 1 | ' 2' |
| J(2,1) | '4' | 0 | ' 4' |
| J(2,1.5) | '4' | 0 | ' 4' |
| J(2,2) | '4' | 0 | ' 4' |
| R(0,1) | '4' | 0 | ' 4' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '4' | 0 | ' 4' |
| R(0,2) | '4' | 0 | ' 4' |
| J(0,2)-U | '4' | 0 | ' 4' |
| J(0,2)-RU | '4' | 0 | ' 4' |

### P2-L0-0287 (greek): bridge gamma (O) → theta (S), token 62

**lookup** (PP-L0-0287): O's answer 4, S's answer 5

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked⟦ gamma⟧. Ryan picked theta. The locker of epsilon is eight.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '4' | 0 | ' 4' |
| J(0,0.5) | '5' | 1 | ' 5' |
| J(0,1) | '5' | 1 | ' 5' |
| J(0,1.5) | '5' | 1 | ' 5' |
| J(0,2) | '5' | 1 | ' 5' |
| J(0.5,0) | '4' | 0 | ' 4' |
| J(0.5,0.5) | '5' | 1 | ' 5' |
| J(0.5,1) | '5' | 1 | ' 5' |
| J(0.5,1.5) | '5' | 1 | ' 5' |
| J(0.5,2) | '5' | 1 | ' 5' |
| J(1,0) | '4' | 0 | ' 4' |
| J(1,0.5) | '5' | 1 | ' 5' |
| J(1,1) | '5' | 1 | ' 5' |
| J(1,1.5) | '5' | 1 | ' 5' |
| J(1,2) | '5' | 1 | ' 5' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '5' | 1 | ' 5' |
| J(1.5,1) | '5' | 1 | ' 5' |
| J(1.5,1.5) | '5' | 1 | ' 5' |
| J(1.5,2) | '5' | 1 | ' 5' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '5' | 1 | ' 5' |
| J(2,1) | '5' | 1 | ' 5' |
| J(2,1.5) | '5' | 1 | ' 5' |
| J(2,2) | '5' | 1 | ' 5' |
| R(0,1) | '5' | 1 | ' 5' |
| R(1,0) | '4' | 0 | ' 4' |
| R(2,0) | '5' | 1 | ' 5' |
| R(0,2) | '5' | 1 | ' 5' |
| J(0,2)-U | '5' | 1 | ' 5' |
| J(0,2)-RU | '5' | 1 | ' 5' |

**recall** (PM-L0-0287): O's answer 3, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked⟦ gamma⟧. Ryan picked theta. The locker of epsilon is eight.
Which position in the Greek alphabet does Ella's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | answer (top token) | switched | greedy |
|---|---|---|---|
| J(0,0) | '3' | 0 | ' 3' |
| J(0,0.5) | '3' | 0 | ' 3' |
| J(0,1) | '8' | 1 | ' 8' |
| J(0,1.5) | '4' | 0 | ' 4' |
| J(0,2) | '3' | 0 | ' 3' |
| J(0.5,0) | '3' | 0 | ' 3' |
| J(0.5,0.5) | '4' | 0 | ' 4' |
| J(0.5,1) | '8' | 1 | ' 8' |
| J(0.5,1.5) | '4' | 0 | ' 4' |
| J(0.5,2) | '3' | 0 | ' 3' |
| J(1,0) | '3' | 0 | ' 3' |
| J(1,0.5) | '4' | 0 | ' 4' |
| J(1,1) | '8' | 1 | ' 8' |
| J(1,1.5) | '4' | 0 | ' 4' |
| J(1,2) | '3' | 0 | ' 3' |
| J(1.5,0) | '4' | 0 | ' 4' |
| J(1.5,0.5) | '8' | 1 | ' 4' |
| J(1.5,1) | '8' | 1 | ' 8' |
| J(1.5,1.5) | '4' | 0 | ' 4' |
| J(1.5,2) | '3' | 0 | ' 3' |
| J(2,0) | '4' | 0 | ' 4' |
| J(2,0.5) | '8' | 1 | ' 8' |
| J(2,1) | '8' | 1 | ' 8' |
| J(2,1.5) | '4' | 0 | ' 4' |
| J(2,2) | '3' | 0 | ' 3' |
| R(0,1) | '8' | 1 | ' 8' |
| R(1,0) | '3' | 0 | ' 3' |
| R(2,0) | '3' | 0 | ' 3' |
| R(0,2) | '7' | 0 | ' 7' |
| J(0,2)-U | '4' | 0 | ' 4' |
| J(0,2)-RU | '4' | 0 | ' 4' |

