# 45p examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word, ⟦new:…⟧ the new item's patched token(s), ⟦control:…⟧ the control item's. UNVERIFIED.

## qwen35_9b_x45p: 10 random items of 186 (seed 0)

### P2-L0-0031 (elements): bridge oxygen → carbon; control hydrogen (before the asked pick)

**lookup** (PP-L0-0031): O's answer 6, S's answer 5

```
<|im_start|>user
Kyle picked nitrogen. The locker of ⟦control:hydrogen⟧ is nine. The locker of ⟦new:carbon⟧ is five. The locker of nitrogen is four. The locker of oxygen is six. Leo picked ⟦bridge:oxygen⟧. David picked hydrogen.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '5' | 1 | 0 | ' 5\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '5' | 1 | 0 | ' 5\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '5' | 1 | 0 | ' 5\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '5' | 1 | 0 | ' 5\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '5' | 1 | 0 | ' 5\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6\n' |

**recall** (PM-L0-0031): O's answer 8, S's answer 6

```
<|im_start|>user
Kyle picked nitrogen. The locker of ⟦control:hydrogen⟧ is nine. The locker of ⟦new:carbon⟧ is five. The locker of nitrogen is four. The locker of oxygen is six. Leo picked ⟦bridge:oxygen⟧. David picked hydrogen.
What is the atomic number of Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '8' | 0 | 1 | ' 8\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 1 | 0 | ' 6\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 1 | 0 | ' 6\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '8' | 0 | 1 | ' 8\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '6' | 1 | 0 | ' 6\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 1 | 0 | ' 6\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '8' | 0 | 1 | ' 8\n' |

### P2-L0-0217 (elements): bridge lithium → oxygen; control hydrogen (before the asked pick)

**lookup** (PP-L0-0217): O's answer 9, S's answer 1

```
<|im_start|>user
The locker of ⟦new:oxygen⟧ is 1. The locker of ⟦control:hydrogen⟧ is 6. Ivan picked ⟦bridge:lithium⟧. The locker of carbon is 3. Henry picked hydrogen. Fiona picked carbon. The locker of lithium is 9.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '9' | 0 | 1 | ' 9\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '9' | 0 | 1 | ' 9\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '9' | 0 | 1 | ' 9\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '9' | 0 | 1 | ' 9\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '9' | 0 | 1 | ' 9\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9\n' |

**recall** (PM-L0-0217): O's answer 3, S's answer 8

```
<|im_start|>user
The locker of ⟦new:oxygen⟧ is 1. The locker of ⟦control:hydrogen⟧ is 6. Ivan picked ⟦bridge:lithium⟧. The locker of carbon is 3. Henry picked hydrogen. Fiona picked carbon. The locker of lithium is 9.
What is the atomic number of Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '3' | 0 | 1 | ' 3\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '8' | 1 | 0 | ' 8\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '3' | 0 | 1 | ' 3\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '3' | 0 | 1 | ' 3\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '3' | 0 | 1 | ' 3\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '3' | 0 | 1 | ' 3\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '3' | 0 | 1 | ' 3\n' |

### P2-L0-0246 (animals): bridge cow → eagle; control owl (before the asked pick)

**lookup** (PP-L0-0246): O's answer 3, S's answer 5

```
<|im_start|>user
The locker of the cow is 3. The locker of the ⟦new:eagle⟧ is 5. The locker of the ⟦control:owl⟧ is 4. The locker of the fox is 1. Jack picked the ⟦bridge:cow⟧. Tara picked the fox. Diana picked the owl.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '3' | 0 | 1 | ' 3\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '5' | 1 | 0 | ' 5\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '5' | 1 | 0 | ' 5\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '5' | 1 | 0 | ' 5\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '5' | 1 | 0 | ' 5\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '5' | 1 | 0 | ' 5\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '3' | 0 | 1 | ' 3\n' |

**recall** (PM-L0-0246): O's answer 4, S's answer 2

```
<|im_start|>user
The locker of the cow is 3. The locker of the ⟦new:eagle⟧ is 5. The locker of the ⟦control:owl⟧ is 4. The locker of the fox is 1. Jack picked the ⟦bridge:cow⟧. Tara picked the fox. Diana picked the owl.
How many legs does Jack's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 1 | 0 | ' 2\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 1 | 0 | ' 2\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 1 | 0 | ' 2\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4\n' |

### P2-L0-0301 (elements): bridge nitrogen → helium; control hydrogen (before the asked pick)

**lookup** (PP-L0-0301): O's answer 9, S's answer 6

```
<|im_start|>user
The locker of ⟦new:helium⟧ is six. The locker of ⟦control:hydrogen⟧ is seven. Ivan picked oxygen. The locker of nitrogen is nine. Frank picked hydrogen. The locker of oxygen is four. Fiona picked ⟦bridge:nitrogen⟧.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 1 | 0 | ' 6\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 1 | 0 | ' 6\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '6' | 1 | 0 | ' 6\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '6' | 1 | 0 | ' 6\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 1 | 0 | ' 6\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9\n' |

**recall** (PM-L0-0301): O's answer 7, S's answer 2

```
<|im_start|>user
The locker of ⟦new:helium⟧ is six. The locker of ⟦control:hydrogen⟧ is seven. Ivan picked oxygen. The locker of nitrogen is nine. Frank picked hydrogen. The locker of oxygen is four. Fiona picked ⟦bridge:nitrogen⟧.
What is the atomic number of Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '7' | 0 | 1 | ' 7\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 1 | 0 | ' 2\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 1 | 0 | ' 2\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 1 | 0 | ' 2\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '7' | 0 | 1 | ' 7\n' |

### P2-L0-0330 (animals): bridge beetle → horse; control wolf (before the asked pick)

**lookup** (PP-L0-0330): O's answer 8, S's answer 2

```
<|im_start|>user
The locker of the ⟦control:wolf⟧ is 6. The locker of the beetle is 8. Ivan picked the wolf. The locker of the eagle is 1. The locker of the ⟦new:horse⟧ is 2. Olivia picked the ⟦bridge:beetle⟧. Laura picked the eagle.
Which locker belongs to Olivia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '8' | 0 | 1 | ' 8\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 1 | 0 | ' 2\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 1 | 0 | ' 2\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 1 | 0 | ' 2\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '8' | 0 | 1 | ' 8\n' |

**recall** (PM-L0-0330): O's answer 6, S's answer 4

```
<|im_start|>user
The locker of the ⟦control:wolf⟧ is 6. The locker of the beetle is 8. Ivan picked the wolf. The locker of the eagle is 1. The locker of the ⟦new:horse⟧ is 2. Olivia picked the ⟦bridge:beetle⟧. Laura picked the eagle.
How many legs does Olivia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 1 | 0 | ' 4\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 1 | 0 | ' 4\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 0 | 0 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 1 | 0 | ' 4\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 1 | 0 | ' 4\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6\n' |

### P2-L0-0340 (elements): bridge hydrogen → lithium; control helium (before the asked pick)

**lookup** (PP-L0-0340): O's answer 7, S's answer 2

```
<|im_start|>user
The locker of ⟦control:helium⟧ is 3. The locker of ⟦new:lithium⟧ is 2. The locker of nitrogen is 8. Jack picked ⟦bridge:hydrogen⟧. Sean picked nitrogen. Julia picked helium. The locker of hydrogen is 7.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '7' | 0 | 1 | ' 7\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 1 | 0 | ' 2\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 1 | 0 | ' 2\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 1 | 0 | ' 2\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '7' | 0 | 1 | ' 7\n' |

**recall** (PM-L0-0340): O's answer 1, S's answer 3

```
<|im_start|>user
The locker of ⟦control:helium⟧ is 3. The locker of ⟦new:lithium⟧ is 2. The locker of nitrogen is 8. Jack picked ⟦bridge:hydrogen⟧. Sean picked nitrogen. Julia picked helium. The locker of hydrogen is 7.
What is the atomic number of Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '1' | 0 | 1 | ' 1\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '3' | 1 | 0 | ' 3\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '3' | 1 | 0 | ' 3\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '3' | 1 | 0 | ' 3\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '3' | 1 | 0 | ' 3\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '3' | 1 | 0 | ' 3\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '1' | 0 | 1 | ' 1\n' |

### P2-L0-0353 (greek): bridge iota → delta; control epsilon (before the asked pick)

**lookup** (PP-L0-0353): O's answer 1, S's answer 2

```
<|im_start|>user
The locker of ⟦new:delta⟧ is 2. The locker of iota is 1. Kate picked alpha. The locker of ⟦control:epsilon⟧ is 6. The locker of alpha is 8. Nina picked epsilon. Will picked ⟦bridge:iota⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '1' | 0 | 1 | ' 1\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 1 | 0 | ' 2\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 1 | 0 | ' 2\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 1 | 0 | ' 2\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '1' | 0 | 1 | ' 1\n' |

**recall** (PM-L0-0353): O's answer 9, S's answer 4

```
<|im_start|>user
The locker of ⟦new:delta⟧ is 2. The locker of iota is 1. Kate picked alpha. The locker of ⟦control:epsilon⟧ is 6. The locker of alpha is 8. Nina picked epsilon. Will picked ⟦bridge:iota⟧.
Which position in the Greek alphabet does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 1 | 0 | ' 4\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 0 | 0 | ' 2\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 0 | 0 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 0 | 0 | ' 2\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 0 | 0 | ' 2\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9\n' |

### P2-L0-0392 (greek): bridge beta → gamma; control eta (before the asked pick)

**lookup** (PP-L0-0392): O's answer 6, S's answer 8

```
<|im_start|>user
Ivan picked eta. The locker of ⟦new:gamma⟧ is eight. The locker of ⟦control:eta⟧ is five. Julia picked ⟦bridge:beta⟧. The locker of beta is six. Iris picked epsilon. The locker of epsilon is three.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 0 | 1 | ' 6\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 0 | 1 | ' 6\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '6' | 0 | 1 | ' 6\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '6' | 0 | 1 | ' 6\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 0 | 1 | ' 6\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6\n' |

**recall** (PM-L0-0392): O's answer 2, S's answer 3

```
<|im_start|>user
Ivan picked eta. The locker of ⟦new:gamma⟧ is eight. The locker of ⟦control:eta⟧ is five. Julia picked ⟦bridge:beta⟧. The locker of beta is six. Iris picked epsilon. The locker of epsilon is three.
Which position in the Greek alphabet does Julia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '2' | 0 | 1 | ' 2\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '3' | 1 | 0 | ' 3\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 0 | 1 | ' 2\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 0 | 1 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 0 | 1 | ' 2\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 0 | 1 | ' 2\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '2' | 0 | 1 | ' 2\n' |

### P2-L0-0399 (animals): bridge deer → duck; control butterfly (before the asked pick)

**lookup** (PP-L0-0399): O's answer 9, S's answer 3

```
<|im_start|>user
The locker of the ⟦control:butterfly⟧ is five. The locker of the ⟦new:duck⟧ is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '3' | 1 | 0 | ' 3\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '3' | 1 | 0 | ' 3\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '3' | 1 | 0 | ' 3\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '3' | 1 | 0 | ' 3\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '3' | 1 | 0 | ' 3\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9\n' |

**recall** (PM-L0-0399): O's answer 4, S's answer 2

```
<|im_start|>user
The locker of the ⟦control:butterfly⟧ is five. The locker of the ⟦new:duck⟧ is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
How many legs does Tara's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 1 | 0 | ' 2\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 1 | 0 | ' 2\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 1 | 0 | ' 2\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 1 | 0 | ' 2\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4\n' |

### P2-L0-0414 (animals): bridge turkey → rabbit; control butterfly (before the asked pick)

**lookup** (PP-L0-0414): O's answer 7, S's answer 9

```
<|im_start|>user
Iris picked the butterfly. The locker of the ⟦new:rabbit⟧ is 9. The locker of the ⟦control:butterfly⟧ is 4. The locker of the sheep is 5. Leo picked the sheep. The locker of the turkey is 7. Tom picked the ⟦bridge:turkey⟧.
Which locker belongs to Tom's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '7' | 0 | 1 | ' 7\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '9' | 1 | 0 | ' 9\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '9' | 1 | 0 | ' 9\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '9' | 1 | 0 | ' 9\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '9' | 1 | 0 | ' 9\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '9' | 1 | 0 | ' 9\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '7' | 0 | 1 | ' 7\n' |

**recall** (PM-L0-0414): O's answer 2, S's answer 4

```
<|im_start|>user
Iris picked the butterfly. The locker of the ⟦new:rabbit⟧ is 9. The locker of the ⟦control:butterfly⟧ is 4. The locker of the sheep is 5. Leo picked the sheep. The locker of the turkey is 7. Tom picked the ⟦bridge:turkey⟧.
How many legs does Tom's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '2' | 0 | 1 | ' 2\n' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 1 | 0 | ' 4\n' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 1 | 0 | ' 4\n' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 1 | 0 | ' 4\n' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 1 | 0 | ' 4\n' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 1 | 0 | ' 4\n' |
| o2 | O alone with (2)'s item edit (no base edit) | '2' | 0 | 1 | ' 2\n' |

## x45p_27b: 10 random items of 254 (seed 0)

### P2-L0-0022 (elements): bridge helium → oxygen; control hydrogen (before the asked pick)

**lookup** (PP-L0-0022): O's answer 3, S's answer 4

```
<|im_start|>user
Frank picked lithium. The locker of ⟦new:oxygen⟧ is four. The locker of helium is three. The locker of ⟦control:hydrogen⟧ is six. Paul picked hydrogen. Will picked ⟦bridge:helium⟧. The locker of lithium is seven.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '3' | 0 | 1 | ' 3' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 1 | 0 | ' 4' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 1 | 0 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 1 | 0 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 1 | 0 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 1 | 0 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '3' | 0 | 1 | ' 3' |

**recall** (PM-L0-0022): O's answer 2, S's answer 8

```
<|im_start|>user
Frank picked lithium. The locker of ⟦new:oxygen⟧ is four. The locker of helium is three. The locker of ⟦control:hydrogen⟧ is six. Paul picked hydrogen. Will picked ⟦bridge:helium⟧. The locker of lithium is seven.
What is the atomic number of Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '2' | 0 | 1 | ' 2' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '8' | 1 | 0 | ' 8' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 0 | 1 | ' 2' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 0 | 1 | ' 2' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 0 | 1 | ' 2' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 0 | 1 | ' 2' |
| o2 | O alone with (2)'s item edit (no base edit) | '2' | 0 | 1 | ' 2' |

### P2-L0-0164 (greek): bridge delta → iota; control alpha (before the asked pick)

**lookup** (PP-L0-0164): O's answer 2, S's answer 3

```
<|im_start|>user
The locker of ⟦new:iota⟧ is three. The locker of ⟦control:alpha⟧ is four. Lily picked ⟦bridge:delta⟧. Luke picked alpha. The locker of delta is two. Eva picked beta. The locker of beta is seven.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '2' | 0 | 1 | ' 2' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 0 | 1 | ' 2' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 0 | 1 | ' 2' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 0 | 1 | ' 2' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 0 | 1 | ' 2' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 0 | 1 | ' 2' |
| o2 | O alone with (2)'s item edit (no base edit) | '2' | 0 | 1 | ' 2' |

**recall** (PM-L0-0164): O's answer 4, S's answer 9

```
<|im_start|>user
The locker of ⟦new:iota⟧ is three. The locker of ⟦control:alpha⟧ is four. Lily picked ⟦bridge:delta⟧. Luke picked alpha. The locker of delta is two. Eva picked beta. The locker of beta is seven.
Which position in the Greek alphabet does Lily's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '9' | 1 | 0 | ' 9' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 0 | 1 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 0 | 1 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 0 | 1 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 0 | 1 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4' |

### P2-L0-0238 (elements): bridge oxygen → hydrogen; control lithium (before the asked pick)

**lookup** (PP-L0-0238): O's answer 3, S's answer 2

```
<|im_start|>user
The locker of ⟦control:lithium⟧ is 4. Grace picked nitrogen. The locker of ⟦new:hydrogen⟧ is 2. The locker of nitrogen is 6. Tom picked ⟦bridge:oxygen⟧. The locker of oxygen is 3. Oscar picked lithium.
Which locker belongs to Tom's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '3' | 0 | 1 | ' 3' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '3' | 0 | 1 | ' 3' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '3' | 0 | 1 | ' 3' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '3' | 0 | 1 | ' 3' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '3' | 0 | 1 | ' 3' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '3' | 0 | 1 | ' 3' |
| o2 | O alone with (2)'s item edit (no base edit) | '3' | 0 | 1 | ' 3' |

**recall** (PM-L0-0238): O's answer 8, S's answer 1

```
<|im_start|>user
The locker of ⟦control:lithium⟧ is 4. Grace picked nitrogen. The locker of ⟦new:hydrogen⟧ is 2. The locker of nitrogen is 6. Tom picked ⟦bridge:oxygen⟧. The locker of oxygen is 3. Oscar picked lithium.
What is the atomic number of Tom's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '8' | 0 | 1 | ' 8' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '8' | 0 | 1 | ' 8' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '8' | 0 | 1 | ' 8' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '8' | 0 | 1 | ' 8' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '8' | 0 | 1 | ' 8' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '8' | 0 | 1 | ' 8' |
| o2 | O alone with (2)'s item edit (no base edit) | '8' | 0 | 1 | ' 8' |

### P2-L0-0253 (elements): bridge oxygen → helium; control lithium (before the asked pick)

**lookup** (PP-L0-0253): O's answer 9, S's answer 7

```
<|im_start|>user
The locker of ⟦control:lithium⟧ is 6. Oscar picked lithium. The locker of oxygen is 9. The locker of ⟦new:helium⟧ is 7. The locker of hydrogen is 5. Ivan picked ⟦bridge:oxygen⟧. Mia picked hydrogen.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '7' | 1 | 0 | ' 7' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '7' | 1 | 0 | ' 7' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '7' | 1 | 0 | ' 7' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '7' | 1 | 0 | ' 7' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '7' | 1 | 0 | ' 7' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9' |

**recall** (PM-L0-0253): O's answer 8, S's answer 2

```
<|im_start|>user
The locker of ⟦control:lithium⟧ is 6. Oscar picked lithium. The locker of oxygen is 9. The locker of ⟦new:helium⟧ is 7. The locker of hydrogen is 5. Ivan picked ⟦bridge:oxygen⟧. Mia picked hydrogen.
What is the atomic number of Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '8' | 0 | 1 | ' 8' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 1 | 0 | ' 2' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '8' | 0 | 1 | ' 8' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '8' | 0 | 1 | ' 8' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '8' | 0 | 1 | ' 8' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '8' | 0 | 1 | ' 8' |
| o2 | O alone with (2)'s item edit (no base edit) | '8' | 0 | 1 | ' 8' |

### P2-L0-0301 (elements): bridge nitrogen → helium; control hydrogen (before the asked pick)

**lookup** (PP-L0-0301): O's answer 9, S's answer 6

```
<|im_start|>user
The locker of ⟦new:helium⟧ is six. The locker of ⟦control:hydrogen⟧ is seven. Ivan picked oxygen. The locker of nitrogen is nine. Frank picked hydrogen. The locker of oxygen is four. Fiona picked ⟦bridge:nitrogen⟧.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 0 | 0 | ' 4' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 0 | 0 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 0 | 0 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 0 | 0 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 0 | 0 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9' |

**recall** (PM-L0-0301): O's answer 7, S's answer 2

```
<|im_start|>user
The locker of ⟦new:helium⟧ is six. The locker of ⟦control:hydrogen⟧ is seven. Ivan picked oxygen. The locker of nitrogen is nine. Frank picked hydrogen. The locker of oxygen is four. Fiona picked ⟦bridge:nitrogen⟧.
What is the atomic number of Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '7' | 0 | 1 | ' 7' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '8' | 0 | 0 | ' 8' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '8' | 0 | 0 | ' 8' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '8' | 0 | 0 | ' 8' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '8' | 0 | 0 | ' 8' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '8' | 0 | 0 | ' 8' |
| o2 | O alone with (2)'s item edit (no base edit) | '7' | 0 | 1 | ' 7' |

### P2-L0-0321 (animals): bridge beetle → bear; control bee (before the asked pick)

**lookup** (PP-L0-0321): O's answer 4, S's answer 7

```
<|im_start|>user
The locker of the ⟦new:bear⟧ is 7. The locker of the ⟦control:bee⟧ is 9. Nina picked the bee. Peter picked the fox. Mia picked the ⟦bridge:beetle⟧. The locker of the beetle is 4. The locker of the fox is 6.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 0 | 1 | ' 4' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 0 | 1 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 0 | 1 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 0 | 1 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 0 | 1 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4' |

**recall** (PM-L0-0321): O's answer 6, S's answer 4

```
<|im_start|>user
The locker of the ⟦new:bear⟧ is 7. The locker of the ⟦control:bee⟧ is 9. Nina picked the bee. Peter picked the fox. Mia picked the ⟦bridge:beetle⟧. The locker of the beetle is 4. The locker of the fox is 6.
How many legs does Mia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 0 | 1 | ' 6' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 0 | 1 | ' 6' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '6' | 0 | 1 | ' 6' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '6' | 0 | 1 | ' 6' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 0 | 1 | ' 6' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6' |

### P2-L0-0455 (greek): bridge gamma → alpha; control epsilon (before the asked pick)

**lookup** (PP-L0-0455): O's answer 8, S's answer 7

```
<|im_start|>user
The locker of ⟦new:alpha⟧ is 7. The locker of gamma is 8. Mia picked eta. The locker of ⟦control:epsilon⟧ is 2. Ruby picked epsilon. The locker of eta is 1. Lily picked ⟦bridge:gamma⟧.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '8' | 0 | 1 | ' 8' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '7' | 1 | 0 | ' 7' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '7' | 1 | 0 | ' 7' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '7' | 1 | 0 | ' 7' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '7' | 1 | 0 | ' 7' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '7' | 1 | 0 | ' 7' |
| o2 | O alone with (2)'s item edit (no base edit) | '8' | 0 | 1 | ' 8' |

**recall** (PM-L0-0455): O's answer 3, S's answer 1

```
<|im_start|>user
The locker of ⟦new:alpha⟧ is 7. The locker of gamma is 8. Mia picked eta. The locker of ⟦control:epsilon⟧ is 2. Ruby picked epsilon. The locker of eta is 1. Lily picked ⟦bridge:gamma⟧.
Which position in the Greek alphabet does Lily's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '3' | 0 | 1 | ' 3' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '1' | 1 | 0 | ' 1' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '3' | 0 | 1 | ' 3' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '3' | 0 | 1 | ' 3' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '3' | 0 | 1 | ' 3' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '3' | 0 | 1 | ' 3' |
| o2 | O alone with (2)'s item edit (no base edit) | '3' | 0 | 1 | ' 3' |

### P2-L0-0507 (animals): bridge lion → bee; control chicken (before the asked pick)

**lookup** (PP-L0-0507): O's answer 8, S's answer 4

```
<|im_start|>user
The locker of the ⟦new:bee⟧ is 4. The locker of the ⟦control:chicken⟧ is 3. Oscar picked the chicken. The locker of the lion is 8. Mia picked the ⟦bridge:lion⟧. The locker of the mouse is 9. Ruby picked the mouse.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '8' | 0 | 1 | ' 8' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 1 | 0 | ' 4' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 1 | 0 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 1 | 0 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 1 | 0 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 1 | 0 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '8' | 0 | 1 | ' 8' |

**recall** (PM-L0-0507): O's answer 4, S's answer 6

```
<|im_start|>user
The locker of the ⟦new:bee⟧ is 4. The locker of the ⟦control:chicken⟧ is 3. Oscar picked the chicken. The locker of the lion is 8. Mia picked the ⟦bridge:lion⟧. The locker of the mouse is 9. Ruby picked the mouse.
How many legs does Mia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 1 | 0 | ' 6' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 0 | 1 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 0 | 1 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 0 | 1 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 0 | 1 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4' |

### P2-L0-0530 (greek): bridge delta → theta; control epsilon (before the asked pick)

**lookup** (PP-L0-0530): O's answer 6, S's answer 3

```
<|im_start|>user
Leo picked gamma. The locker of delta is 6. The locker of ⟦new:theta⟧ is 3. The locker of ⟦control:epsilon⟧ is 9. The locker of gamma is 1. Mia picked ⟦bridge:delta⟧. Sam picked epsilon.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '3' | 1 | 0 | ' 3' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '3' | 1 | 0 | ' 3' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '3' | 1 | 0 | ' 3' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '3' | 1 | 0 | ' 3' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '3' | 1 | 0 | ' 3' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6' |

**recall** (PM-L0-0530): O's answer 4, S's answer 8

```
<|im_start|>user
Leo picked gamma. The locker of delta is 6. The locker of ⟦new:theta⟧ is 3. The locker of ⟦control:epsilon⟧ is 9. The locker of gamma is 1. Mia picked ⟦bridge:delta⟧. Sam picked epsilon.
Which position in the Greek alphabet does Mia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '8' | 1 | 0 | ' 8' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '8' | 1 | 0 | ' 8' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '8' | 1 | 0 | ' 8' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '8' | 1 | 0 | ' 8' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '8' | 1 | 0 | ' 8' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4' |

### P2-L0-0588 (animals): bridge cow → butterfly; control tiger (before the asked pick)

**lookup** (PP-L0-0588): O's answer 5, S's answer 9

```
<|im_start|>user
The locker of the ⟦new:butterfly⟧ is 9. The locker of the cow is 5. Mia picked the tiger. The locker of the ⟦control:tiger⟧ is 6. Ben picked the ⟦bridge:cow⟧. Kate picked the spider. The locker of the spider is 4.
Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '5' | 0 | 1 | ' 5' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '9' | 1 | 0 | ' 9' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '9' | 1 | 0 | ' 9' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '9' | 1 | 0 | ' 9' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '9' | 1 | 0 | ' 9' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '9' | 1 | 0 | ' 9' |
| o2 | O alone with (2)'s item edit (no base edit) | '5' | 0 | 1 | ' 5' |

**recall** (PM-L0-0588): O's answer 4, S's answer 6

```
<|im_start|>user
The locker of the ⟦new:butterfly⟧ is 9. The locker of the cow is 5. Mia picked the tiger. The locker of the ⟦control:tiger⟧ is 6. Ben picked the ⟦bridge:cow⟧. Kate picked the spider. The locker of the spider is 4.
How many legs does Ben's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 1 | 0 | ' 6' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 1 | 0 | ' 6' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 0 | 1 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '6' | 1 | 0 | ' 6' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 1 | 0 | ' 6' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4' |

## muse30b_x45p: 10 random items of 178 (seed 0)

### P2-L0-0034 (elements): bridge oxygen → fluorine; control helium (before the asked pick)

**lookup** (PP-L0-0034): O's answer 6, S's answer 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mia picked nitrogen. The locker of ⟦new:fluorine⟧ is eight. The locker of ⟦control:helium⟧ is five. James picked helium. Julia picked ⟦bridge:oxygen⟧. The locker of nitrogen is two. The locker of oxygen is six.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 0 | 1 | ' 6' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 0 | 1 | ' 6' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '6' | 0 | 1 | ' 6' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '6' | 0 | 1 | ' 6' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 0 | 1 | ' 6' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6' |

**recall** (PM-L0-0034): O's answer 8, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mia picked nitrogen. The locker of ⟦new:fluorine⟧ is eight. The locker of ⟦control:helium⟧ is five. James picked helium. Julia picked ⟦bridge:oxygen⟧. The locker of nitrogen is two. The locker of oxygen is six.
What is the atomic number of Julia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '8' | 0 | 1 | ' 8' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '8' | 0 | 1 | ' 8' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '8' | 0 | 1 | ' 8' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '8' | 0 | 1 | ' 8' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '8' | 0 | 1 | ' 8' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '8' | 0 | 1 | ' 8' |
| o2 | O alone with (2)'s item edit (no base edit) | '8' | 0 | 1 | ' 8' |

### P2-L0-0217 (elements): bridge lithium → fluorine; control hydrogen (before the asked pick)

**lookup** (PP-L0-0217): O's answer 9, S's answer 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of ⟦new:fluorine⟧ is 1. The locker of ⟦control:hydrogen⟧ is 6. Ivan picked ⟦bridge:lithium⟧. The locker of carbon is 3. Henry picked hydrogen. Fiona picked carbon. The locker of lithium is 9.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '9' | 0 | 1 | ' 9' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '9' | 0 | 1 | ' 9' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '9' | 0 | 1 | ' 9' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '9' | 0 | 1 | ' 9' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '9' | 0 | 1 | ' 9' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9' |

**recall** (PM-L0-0217): O's answer 3, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of ⟦new:fluorine⟧ is 1. The locker of ⟦control:hydrogen⟧ is 6. Ivan picked ⟦bridge:lithium⟧. The locker of carbon is 3. Henry picked hydrogen. Fiona picked carbon. The locker of lithium is 9.
What is the atomic number of Ivan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '3' | 0 | 1 | ' 3' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '3' | 0 | 1 | ' 3' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '3' | 0 | 1 | ' 3' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '3' | 0 | 1 | ' 3' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '3' | 0 | 1 | ' 3' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '3' | 0 | 1 | ' 3' |
| o2 | O alone with (2)'s item edit (no base edit) | '3' | 0 | 1 | ' 3' |

### P2-L0-0244 (elements): bridge hydrogen → carbon; control oxygen (before the asked pick)

**lookup** (PP-L0-0244): O's answer 7, S's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is seven. The locker of ⟦new:carbon⟧ is two. The locker of ⟦control:oxygen⟧ is nine. Victor picked helium. The locker of helium is eight. James picked oxygen. Rose picked ⟦bridge:hydrogen⟧.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '7' | 0 | 1 | ' 7' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 1 | 0 | ' 2' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 1 | 0 | ' 2' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 1 | 0 | ' 2' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 1 | 0 | ' 2' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 1 | 0 | ' 2' |
| o2 | O alone with (2)'s item edit (no base edit) | '7' | 0 | 1 | ' 7' |

**recall** (PM-L0-0244): O's answer 1, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is seven. The locker of ⟦new:carbon⟧ is two. The locker of ⟦control:oxygen⟧ is nine. Victor picked helium. The locker of helium is eight. James picked oxygen. Rose picked ⟦bridge:hydrogen⟧.
What is the atomic number of Rose's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '1' | 0 | 1 | ' 1' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 1 | 0 | ' 6' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 1 | 0 | ' 6' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 0 | 0 | ' 2' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 0 | 0 | ' 2' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 1 | 0 | ' 6' |
| o2 | O alone with (2)'s item edit (no base edit) | '1' | 0 | 1 | ' 1' |

### P2-L0-0285 (animals): bridge crow → bee; control ant (before the asked pick)

**lookup** (PP-L0-0285): O's answer 6, S's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦control:ant⟧ is two. The locker of the crow is six. Sean picked the ant. The locker of the ⟦new:bee⟧ is four. The locker of the horse is three. Ivy picked the horse. Julia picked the ⟦bridge:crow⟧.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 1 | 0 | ' 4' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 1 | 0 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 1 | 0 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 1 | 0 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 1 | 0 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6' |

**recall** (PM-L0-0285): O's answer 2, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦control:ant⟧ is two. The locker of the crow is six. Sean picked the ant. The locker of the ⟦new:bee⟧ is four. The locker of the horse is three. Ivy picked the horse. Julia picked the ⟦bridge:crow⟧.
How many legs does Julia's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '2' | 0 | 1 | ' 2' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '2' | 0 | 1 | ' 2' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 0 | 1 | ' 2' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 0 | 1 | ' 2' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 0 | 1 | ' 2' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 0 | 1 | ' 2' |
| o2 | O alone with (2)'s item edit (no base edit) | '2' | 0 | 1 | ' 2' |

### P2-L0-0317 (greek): bridge beta → alpha; control iota (before the asked pick)

**lookup** (PP-L0-0317): O's answer 8, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of beta is eight. Ivan picked iota. The locker of ⟦new:alpha⟧ is nine. The locker of ⟦control:iota⟧ is five. Oscar picked ⟦bridge:beta⟧. The locker of theta is four. Adam picked theta.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '8' | 0 | 1 | ' 8' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '9' | 1 | 0 | ' 9' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '9' | 1 | 0 | ' 9' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '9' | 1 | 0 | ' 9' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '9' | 1 | 0 | ' 9' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '9' | 1 | 0 | ' 9' |
| o2 | O alone with (2)'s item edit (no base edit) | '8' | 0 | 1 | ' 8' |

**recall** (PM-L0-0317): O's answer 2, S's answer 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of beta is eight. Ivan picked iota. The locker of ⟦new:alpha⟧ is nine. The locker of ⟦control:iota⟧ is five. Oscar picked ⟦bridge:beta⟧. The locker of theta is four. Adam picked theta.
Which position in the Greek alphabet does Oscar's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '2' | 0 | 1 | ' 2' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '1' | 1 | 0 | ' 1' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '1' | 1 | 0 | ' 1' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '1' | 1 | 0 | ' 1' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '1' | 1 | 0 | ' 1' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '1' | 1 | 0 | ' 1' |
| o2 | O alone with (2)'s item edit (no base edit) | '2' | 0 | 1 | ' 2' |

### P2-L0-0342 (animals): bridge butterfly → elephant; control cat (after the asked pick)

**lookup** (PP-L0-0342): O's answer 3, S's answer 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦new:elephant⟧ is seven. The locker of the butterfly is three. Grace picked the deer. Alice picked the ⟦bridge:butterfly⟧. The locker of the ⟦control:cat⟧ is eight. The locker of the deer is one. Owen picked the cat.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '3' | 0 | 1 | ' 3' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '7' | 1 | 0 | ' 7' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '7' | 1 | 0 | ' 7' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '7' | 1 | 0 | ' 7' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '7' | 1 | 0 | ' 7' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '7' | 1 | 0 | ' 7' |
| o2 | O alone with (2)'s item edit (no base edit) | '3' | 0 | 1 | ' 3' |

**recall** (PM-L0-0342): O's answer 6, S's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦new:elephant⟧ is seven. The locker of the butterfly is three. Grace picked the deer. Alice picked the ⟦bridge:butterfly⟧. The locker of the ⟦control:cat⟧ is eight. The locker of the deer is one. Owen picked the cat.
How many legs does Alice's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 0 | 1 | ' 6' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 0 | 1 | ' 6' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '6' | 0 | 1 | ' 6' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '6' | 0 | 1 | ' 6' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 0 | 1 | ' 6' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6' |

### P2-L0-0357 (animals): bridge wolf → owl; control eagle (before the asked pick)

**lookup** (PP-L0-0357): O's answer 9, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦new:owl⟧ is 6. The locker of the wolf is 9. Leo picked the eagle. The locker of the ⟦control:eagle⟧ is 7. Lucy picked the ⟦bridge:wolf⟧. Julia picked the goat. The locker of the goat is 1.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '6' | 1 | 0 | ' 6' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '6' | 1 | 0 | ' 6' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '6' | 1 | 0 | ' 6' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '6' | 1 | 0 | ' 6' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '6' | 1 | 0 | ' 6' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9' |

**recall** (PM-L0-0357): O's answer 4, S's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦new:owl⟧ is 6. The locker of the wolf is 9. Leo picked the eagle. The locker of the ⟦control:eagle⟧ is 7. Lucy picked the ⟦bridge:wolf⟧. Julia picked the goat. The locker of the goat is 1.
How many legs does Lucy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 0 | 1 | ' 4' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 0 | 1 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 0 | 1 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 0 | 1 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 0 | 1 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4' |

### P2-L0-0399 (animals): bridge deer → duck; control butterfly (before the asked pick)

**lookup** (PP-L0-0399): O's answer 9, S's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦control:butterfly⟧ is five. The locker of the ⟦new:duck⟧ is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '9' | 0 | 1 | ' 9' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '3' | 1 | 0 | ' 3' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '3' | 1 | 0 | ' 3' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '3' | 1 | 0 | ' 3' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '3' | 1 | 0 | ' 3' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '3' | 1 | 0 | ' 3' |
| o2 | O alone with (2)'s item edit (no base edit) | '9' | 0 | 1 | ' 9' |

**recall** (PM-L0-0399): O's answer 4, S's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the ⟦control:butterfly⟧ is five. The locker of the ⟦new:duck⟧ is three. The locker of the deer is nine. The locker of the goose is six. Tara picked the ⟦bridge:deer⟧. Dan picked the goose. Lucy picked the butterfly.
How many legs does Tara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 0 | 1 | ' 4' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 0 | 1 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 0 | 1 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 0 | 1 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 0 | 1 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4' |

### P2-L0-0406 (elements): bridge helium → boron; control hydrogen (before the asked pick)

**lookup** (PP-L0-0406): O's answer 7, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Eve picked oxygen. The locker of ⟦new:boron⟧ is 9. The locker of helium is 7. Henry picked hydrogen. The locker of ⟦control:hydrogen⟧ is 8. The locker of oxygen is 1. Luke picked ⟦bridge:helium⟧.
Which locker belongs to Luke's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '7' | 0 | 1 | ' 7' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '9' | 1 | 0 | ' 9' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '9' | 1 | 0 | ' 9' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '9' | 1 | 0 | ' 9' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '9' | 1 | 0 | ' 9' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '9' | 1 | 0 | ' 9' |
| o2 | O alone with (2)'s item edit (no base edit) | '7' | 0 | 1 | ' 7' |

**recall** (PM-L0-0406): O's answer 2, S's answer 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Eve picked oxygen. The locker of ⟦new:boron⟧ is 9. The locker of helium is 7. Henry picked hydrogen. The locker of ⟦control:hydrogen⟧ is 8. The locker of oxygen is 1. Luke picked ⟦bridge:helium⟧.
What is the atomic number of Luke's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '2' | 0 | 1 | ' 2' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '5' | 1 | 0 | ' 5' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '2' | 0 | 1 | ' 2' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '2' | 0 | 1 | ' 2' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '2' | 0 | 1 | ' 2' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '2' | 0 | 1 | ' 2' |
| o2 | O alone with (2)'s item edit (no base edit) | '2' | 0 | 1 | ' 2' |

### P2-L0-0426 (animals): bridge mouse → owl; control ant (before the asked pick)

**lookup** (PP-L0-0426): O's answer 6, S's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the mouse is 6. The locker of the ⟦control:ant⟧ is 1. The locker of the ⟦new:owl⟧ is 9. The locker of the crow is 7. David picked the ⟦bridge:mouse⟧. Victor picked the ant. Beth picked the crow.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '6' | 0 | 1 | ' 6' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '9' | 1 | 0 | ' 9' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '9' | 1 | 0 | ' 9' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '9' | 1 | 0 | ' 9' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '9' | 1 | 0 | ' 9' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '9' | 1 | 0 | ' 9' |
| o2 | O alone with (2)'s item edit (no base edit) | '6' | 0 | 1 | ' 6' |

**recall** (PM-L0-0426): O's answer 4, S's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the mouse is 6. The locker of the ⟦control:ant⟧ is 1. The locker of the ⟦new:owl⟧ is 9. The locker of the crow is 7. David picked the ⟦bridge:mouse⟧. Victor picked the ant. Beth picked the crow.
How many legs does David's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | switched | right | greedy |
|---|---|---|---|---|---|
| none | O unedited | '4' | 0 | 1 | ' 4' |
| whole | the whole change at the bridge word (45m's whole arm, rerun) | '4' | 0 | 1 | ' 4' |
| a1 | (1) the base edit: the whole change minus its J++ part (k = 25, signed), at the bridge word | '4' | 0 | 1 | ' 4' |
| a2 | (2) the base edit, and the new item's token(s) in its locker sentence without their own J++ part | '4' | 0 | 1 | ' 4' |
| a3 | (3) the base edit, and the same tokens without a random part of the same share | '4' | 0 | 1 | ' 4' |
| a4 | (4) the base edit, and the control item's token(s) without their own J++ part | '4' | 0 | 1 | ' 4' |
| o2 | O alone with (2)'s item edit (no base edit) | '4' | 0 | 1 | ' 4' |

