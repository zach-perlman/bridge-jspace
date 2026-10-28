# 49.2 plan on qwen3.6-27b (L32; rungs 1, 2): 5 of the clean design's 574 items (seed 0), S's prompt as each reader reads it (the read's appended space token included).

⟦bridge:…⟧ rungs 1-6 (the bridge word); ⟦mention:…⟧ rung 3 on (the item's name in its locker sentence); ⟦question:…⟧ rung 4 on (Zach's 'question' positions); every token, marked or not, rungs 5-6. Counts in plan.json.

## P2-L0-0045 (animals, locker-first): bridge spider -> dog, token 32, mention [7]

**lookup** (PP-L0-0045), S's answer 3; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
The locker of the ⟦mention:dog⟧ is three. The locker of the sheep is seven. Maria picked the sheep. James picked the mouse. Sean picked the ⟦bridge:dog⟧. The locker of the spider is nine. The locker of the mouse is eight.
⟦question:Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0045), S's answer 4; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
The locker of the ⟦mention:dog⟧ is three. The locker of the sheep is seven. Maria picked the sheep. James picked the mouse. Sean picked the ⟦bridge:dog⟧. The locker of the spider is nine. The locker of the mouse is eight.
⟦question:How many legs does Sean's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

## P2-L0-0283 (elements, locker-after): bridge oxygen -> carbon, token 30, mention [43]

**lookup** (PP-L0-0283), S's answer 4; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
Eva picked lithium. The locker of lithium is 2. The locker of nitrogen is 8. Liam picked nitrogen. Tara picked ⟦bridge:carbon⟧. The locker of oxygen is 6. The locker of ⟦mention:carbon⟧ is 4.
⟦question:Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0283), S's answer 6; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
Eva picked lithium. The locker of lithium is 2. The locker of nitrogen is 8. Liam picked nitrogen. Tara picked ⟦bridge:carbon⟧. The locker of oxygen is 6. The locker of ⟦mention:carbon⟧ is 4.
⟦question:What is the atomic number of Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

## P2-L0-0415 (elements, locker-after): bridge oxygen -> nitrogen, token 29, mention [42]

**lookup** (PP-L0-0415), S's answer 8; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
The locker of helium is 5. Zoe picked helium. The locker of oxygen is 3. Ivan picked lithium. Eva picked ⟦bridge:nitrogen⟧. The locker of lithium is 4. The locker of ⟦mention:nitrogen⟧ is 8.
⟦question:Which locker belongs to Eva's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0415), S's answer 7; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
The locker of helium is 5. Zoe picked helium. The locker of oxygen is 3. Ivan picked lithium. Eva picked ⟦bridge:nitrogen⟧. The locker of lithium is 4. The locker of ⟦mention:nitrogen⟧ is 8.
⟦question:What is the atomic number of Eva's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

## P2-L0-0451 (elements, locker-first): bridge nitrogen -> hydrogen, token 45, mention [38]

**lookup** (PP-L0-0451), S's answer 9; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
The locker of oxygen is 2. Mark picked oxygen. The locker of carbon is 1. Oscar picked carbon. The locker of nitrogen is 3. The locker of ⟦mention:hydrogen⟧ is 9. Sam picked ⟦bridge:hydrogen⟧.
⟦question:Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0451), S's answer 1; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
The locker of oxygen is 2. Mark picked oxygen. The locker of carbon is 1. Oscar picked carbon. The locker of nitrogen is 3. The locker of ⟦mention:hydrogen⟧ is 9. Sam picked ⟦bridge:hydrogen⟧.
⟦question:What is the atomic number of Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

## P2-L0-0547 (elements, locker-after): bridge nitrogen -> carbon, token 5, mention [21]

**lookup** (PP-L0-0547), S's answer 5; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
Emma picked ⟦bridge:carbon⟧. The locker of hydrogen is six. Adam picked oxygen. The locker of ⟦mention:carbon⟧ is five. The locker of oxygen is three. Iris picked hydrogen. The locker of nitrogen is one.
⟦question:Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

**recall** (PM-L0-0547), S's answer 6; tokens per rung: (1) 1, (2) 1

```
<|im_start|>user
Emma picked ⟦bridge:carbon⟧. The locker of hydrogen is six. Adam picked oxygen. The locker of ⟦mention:carbon⟧ is five. The locker of oxygen is three. Iris picked hydrogen. The locker of nitrogen is one.
⟦question:What is the atomic number of Emma's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: ⟧
```

