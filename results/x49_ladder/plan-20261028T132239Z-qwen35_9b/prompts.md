# 49.2 plan on qwen3.5-9b (L12; rungs 1, 2, 3, 4, 5, 6): 5 of the clean design's 417 items (seed 0), S's prompt as each reader reads it (the read's appended space token included).

⟦bridge:…⟧ rungs 1-6 (the bridge word); ⟦mention:…⟧ rung 3 on (the item's name in its locker sentence); ⟦question:…⟧ rung 4 on (Zach's 'question' positions); every token, marked or not, rungs 5-6. Counts in plan.json.

## P2-L0-0031 (elements, locker-first): bridge oxygen -> carbon, token 37, mention [17]

**lookup** (PP-L0-0031), S's answer 5; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 31, (5) 73, (6) 73

```
<|im_start|>user
Kyle picked nitrogen. The locker of hydrogen is nine. The locker of ⟦mention:carbon⟧ is five. The locker of nitrogen is four. The locker of oxygen is six. Leo picked ⟦bridge:carbon⟧. David picked hydrogen.
⟦question:Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0031), S's answer 6; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 33, (5) 75, (6) 75

```
<|im_start|>user
Kyle picked nitrogen. The locker of hydrogen is nine. The locker of ⟦mention:carbon⟧ is five. The locker of nitrogen is four. The locker of oxygen is six. Leo picked ⟦bridge:carbon⟧. David picked hydrogen.
⟦question:What is the atomic number of Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

## P2-L0-0196 (elements, locker-first): bridge hydrogen -> oxygen, token 41, mention [24]

**lookup** (PP-L0-0196), S's answer 6; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 31, (5) 73, (6) 73

```
<|im_start|>user
The locker of nitrogen is four. Tara picked nitrogen. The locker of hydrogen is three. The locker of ⟦mention:oxygen⟧ is six. The locker of carbon is five. Mia picked carbon. Finn picked ⟦bridge:oxygen⟧.
⟦question:Which locker belongs to Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0196), S's answer 8; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 33, (5) 75, (6) 75

```
<|im_start|>user
The locker of nitrogen is four. Tara picked nitrogen. The locker of hydrogen is three. The locker of ⟦mention:oxygen⟧ is six. The locker of carbon is five. Mia picked carbon. Finn picked ⟦bridge:oxygen⟧.
⟦question:What is the atomic number of Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

## P2-L0-0293 (greek, locker-first): bridge alpha -> delta, token 37, mention [6]

**lookup** (PP-L0-0293), S's answer 5; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 31, (5) 77, (6) 77

```
<|im_start|>user
The locker of ⟦mention:delta⟧ is 5. The locker of iota is 8. Ruby picked gamma. The locker of alpha is 2. Emma picked iota. Kate picked ⟦bridge:delta⟧. The locker of gamma is 1.
⟦question:Which locker belongs to Kate's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0293), S's answer 4; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 35, (5) 81, (6) 81

```
<|im_start|>user
The locker of ⟦mention:delta⟧ is 5. The locker of iota is 8. Ruby picked gamma. The locker of alpha is 2. Emma picked iota. Kate picked ⟦bridge:delta⟧. The locker of gamma is 1.
⟦question:Which position in the Greek alphabet does Kate's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

## P2-L0-0317 (greek, locker-first): bridge beta -> alpha, token 30, mention [17]

**lookup** (PP-L0-0317), S's answer 9; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 31, (5) 73, (6) 73

```
<|im_start|>user
The locker of beta is eight. Ivan picked iota. The locker of ⟦mention:alpha⟧ is nine. The locker of iota is five. Oscar picked ⟦bridge:alpha⟧. The locker of theta is four. Adam picked theta.
⟦question:Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0317), S's answer 1; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 35, (5) 77, (6) 77

```
<|im_start|>user
The locker of beta is eight. Ivan picked iota. The locker of ⟦mention:alpha⟧ is nine. The locker of iota is five. Oscar picked ⟦bridge:alpha⟧. The locker of theta is four. Adam picked theta.
⟦question:Which position in the Greek alphabet does Oscar's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

## P2-L0-0559 (elements, locker-after): bridge nitrogen -> lithium, token 21, mention [26]

**lookup** (PP-L0-0559), S's answer 7; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 31, (5) 77, (6) 77

```
<|im_start|>user
The locker of oxygen is 5. Finn picked helium. Tara picked oxygen. Grace picked ⟦bridge:lithium⟧. The locker of ⟦mention:lithium⟧ is 7. The locker of nitrogen is 2. The locker of helium is 6.
⟦question:Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0559), S's answer 3; tokens per rung: (1) 1, (2) 1, (3) 2, (4) 33, (5) 79, (6) 79

```
<|im_start|>user
The locker of oxygen is 5. Finn picked helium. Tara picked oxygen. Grace picked ⟦bridge:lithium⟧. The locker of ⟦mention:lithium⟧ is 7. The locker of nitrogen is 2. The locker of helium is 6.
⟦question:What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

