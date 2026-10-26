# 45b examples: x45b_binding_27b

10 random items of 99 (seed 0); model qwen3.6-27b, L = 32. Prompts exactly as the model reads them (the read appends the digit's space token); ⟦…⟧ marks the bridge word (arms a, b) and each patched locker-sentence token span (arms c, d; a token's leading space shown outside). Answer = the top token at the read step; greedy = 8 greedy tokens of the edited prompt (no space appended). UNVERIFIED.

## P2-L0-0010 (elements): bridge oxygen → carbon; aligned token; 24 locker tokens patched

**lookup** (PP-L0-0010): O's answer 3, S's answer 7

```
<|im_start|>user
⟦The locker of carbon is 7.⟧ Adam picked hydrogen. Grace picked ⟦oxygen⟧. ⟦The locker of oxygen is 3.⟧ ⟦The locker of hydrogen is 4.⟧ Oscar picked carbon.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L32 | the bridge-word change at L | '3' (A) | 0 | ' 3' |
| b_half L16 | the bridge-word change at L/2 | '7' (b) | 1 | ' 7' |
| b_quarter L8 | the bridge-word change at L/4 | '7' (b) | 1 | ' 7' |
| c L32 | S patched into O at every locker-sentence token, at L | '3' (A) | 0 | ' 3' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '3' (A) | 0 | ' 3' |
| S  | S read on S (unedited) | '7' (b) | 1 | ' 7' |

**recall** (PM-L0-0010): O's answer 8, S's answer 6

```
<|im_start|>user
⟦The locker of carbon is 7.⟧ Adam picked hydrogen. Grace picked ⟦oxygen⟧. ⟦The locker of oxygen is 3.⟧ ⟦The locker of hydrogen is 4.⟧ Oscar picked carbon.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '8' (A) | 0 | ' 8' |
| a L32 | the bridge-word change at L | '6' (b) | 1 | ' 6' |
| b_half L16 | the bridge-word change at L/2 | '6' (b) | 1 | ' 6' |
| b_quarter L8 | the bridge-word change at L/4 | '6' (b) | 1 | ' 6' |
| c L32 | S patched into O at every locker-sentence token, at L | '8' (A) | 0 | ' 8' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '8' (A) | 0 | ' 8' |
| S  | S read on S (unedited) | '6' (b) | 1 | ' 6' |

## P2-L0-0080 (greek): bridge eta → delta; aligned token; 24 locker tokens patched

**lookup** (PP-L0-0080): O's answer 6, S's answer 8

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. Ivy picked ⟦eta⟧. ⟦The locker of delta is 8.⟧ ⟦The locker of eta is 6.⟧ ⟦The locker of epsilon is 1.⟧
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '6' (A) | 0 | ' 6' |
| a L32 | the bridge-word change at L | '6' (A) | 0 | ' 6' |
| b_half L16 | the bridge-word change at L/2 | '8' (b) | 1 | ' 8' |
| b_quarter L8 | the bridge-word change at L/4 | '8' (b) | 1 | ' 8' |
| c L32 | S patched into O at every locker-sentence token, at L | '6' (A) | 0 | ' 6' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '6' (A) | 0 | ' 6' |
| S  | S read on S (unedited) | '8' (b) | 1 | ' 8' |

**recall** (PM-L0-0080): O's answer 7, S's answer 4

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. Ivy picked ⟦eta⟧. ⟦The locker of delta is 8.⟧ ⟦The locker of eta is 6.⟧ ⟦The locker of epsilon is 1.⟧
Which position in the Greek alphabet does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '7' (A) | 0 | ' 7' |
| a L32 | the bridge-word change at L | '4' (b) | 1 | ' 4' |
| b_half L16 | the bridge-word change at L/2 | '4' (b) | 1 | ' 4' |
| b_quarter L8 | the bridge-word change at L/4 | '4' (b) | 1 | ' 4' |
| c L32 | S patched into O at every locker-sentence token, at L | '7' (A) | 0 | ' 7' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '7' (A) | 0 | ' 7' |
| S  | S read on S (unedited) | '4' (b) | 1 | ' 4' |

## P2-L0-0089 (greek): bridge eta → gamma; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0089): O's answer 2, S's answer 5

```
<|im_start|>user
Fiona picked ⟦eta⟧. Owen picked alpha. ⟦The locker of alpha is eight.⟧ ⟦The locker of eta is two.⟧ Max picked gamma. ⟦The locker of gamma is five.⟧
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '2' (A) | 0 | ' 2' |
| a L32 | the bridge-word change at L | '2' (A) | 0 | ' 2' |
| b_half L16 | the bridge-word change at L/2 | '2' (A) | 0 | ' 2' |
| b_quarter L8 | the bridge-word change at L/4 | '5' (b) | 1 | ' 5' |
| c L32 | S patched into O at every locker-sentence token, at L | '5' (b) | 1 | ' 5' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '2' (A) | 0 | ' 2' |
| S  | S read on S (unedited) | '5' (b) | 1 | ' 5' |

**recall** (PM-L0-0089): O's answer 7, S's answer 3

```
<|im_start|>user
Fiona picked ⟦eta⟧. Owen picked alpha. ⟦The locker of alpha is eight.⟧ ⟦The locker of eta is two.⟧ Max picked gamma. ⟦The locker of gamma is five.⟧
Which position in the Greek alphabet does Fiona's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '7' (A) | 0 | ' 7' |
| a L32 | the bridge-word change at L | '7' (A) | 0 | ' 7' |
| b_half L16 | the bridge-word change at L/2 | '7' (A) | 0 | ' 7' |
| b_quarter L8 | the bridge-word change at L/4 | '3' (b) | 1 | ' 3' |
| c L32 | S patched into O at every locker-sentence token, at L | '5' (other) | 0 | ' 5' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '7' (A) | 0 | ' 7' |
| S  | S read on S (unedited) | '3' (b) | 1 | ' 3' |

## P2-L0-0106 (elements): bridge lithium → helium; aligned token; 24 locker tokens patched

**lookup** (PP-L0-0106): O's answer 6, S's answer 9

```
<|im_start|>user
Will picked carbon. ⟦The locker of helium is 9.⟧ Paul picked ⟦lithium⟧. Amy picked helium. ⟦The locker of carbon is 3.⟧ ⟦The locker of lithium is 6.⟧
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '6' (A) | 0 | ' 6' |
| a L32 | the bridge-word change at L | '6' (A) | 0 | ' 6' |
| b_half L16 | the bridge-word change at L/2 | '9' (b) | 1 | ' 9' |
| b_quarter L8 | the bridge-word change at L/4 | '9' (b) | 1 | ' 9' |
| c L32 | S patched into O at every locker-sentence token, at L | '6' (A) | 0 | ' 6' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '6' (A) | 0 | ' 6' |
| S  | S read on S (unedited) | '9' (b) | 1 | ' 9' |

**recall** (PM-L0-0106): O's answer 3, S's answer 2

```
<|im_start|>user
Will picked carbon. ⟦The locker of helium is 9.⟧ Paul picked ⟦lithium⟧. Amy picked helium. ⟦The locker of carbon is 3.⟧ ⟦The locker of lithium is 6.⟧
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L32 | the bridge-word change at L | '3' (A) | 0 | ' 3' |
| b_half L16 | the bridge-word change at L/2 | '2' (b) | 1 | ' 2' |
| b_quarter L8 | the bridge-word change at L/4 | '2' (b) | 1 | ' 2' |
| c L32 | S patched into O at every locker-sentence token, at L | '3' (A) | 0 | ' 3' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '3' (A) | 0 | ' 3' |
| S  | S read on S (unedited) | '2' (b) | 1 | ' 2' |

## P2-L0-0108 (animals): bridge frog → ant; aligned token; 27 locker tokens patched

**lookup** (PP-L0-0108): O's answer 1, S's answer 2

```
<|im_start|>user
James picked the ⟦frog⟧. Rose picked the ant. ⟦The locker of the frog is 1.⟧ ⟦The locker of the bear is 3.⟧ Frank picked the bear. ⟦The locker of the ant is 2.⟧
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '1' (A) | 0 | ' 1' |
| a L32 | the bridge-word change at L | '1' (A) | 0 | ' 1' |
| b_half L16 | the bridge-word change at L/2 | '1' (A) | 0 | ' 1' |
| b_quarter L8 | the bridge-word change at L/4 | '2' (b) | 1 | ' 2' |
| c L32 | S patched into O at every locker-sentence token, at L | '2' (b) | 1 | ' 2' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '1' (A) | 0 | ' 1' |
| S  | S read on S (unedited) | '2' (b) | 1 | ' 2' |

**recall** (PM-L0-0108): O's answer 4, S's answer 6

```
<|im_start|>user
James picked the ⟦frog⟧. Rose picked the ant. ⟦The locker of the frog is 1.⟧ ⟦The locker of the bear is 3.⟧ Frank picked the bear. ⟦The locker of the ant is 2.⟧
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '4' (A) | 0 | ' 4' |
| a L32 | the bridge-word change at L | '6' (b) | 1 | ' 6' |
| b_half L16 | the bridge-word change at L/2 | '6' (b) | 1 | ' 6' |
| b_quarter L8 | the bridge-word change at L/4 | '6' (b) | 1 | ' 6' |
| c L32 | S patched into O at every locker-sentence token, at L | '4' (A) | 0 | ' 4' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '4' (A) | 0 | ' 4' |
| S  | S read on S (unedited) | '6' (b) | 1 | ' 6' |

## P2-L0-0117 (animals): bridge elephant → beetle; aligned token; 24 locker tokens patched

**lookup** (PP-L0-0117): O's answer 1, S's answer 9

```
<|im_start|>user
Mark picked the beetle. ⟦The locker of the dog is six.⟧ Lily picked the dog. ⟦The locker of the beetle is nine.⟧ Victor picked the ⟦elephant⟧. ⟦The locker of the elephant is one.⟧
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '1' (A) | 0 | ' 1' |
| a L32 | the bridge-word change at L | '1' (A) | 0 | ' 1' |
| b_half L16 | the bridge-word change at L/2 | '9' (b) | 1 | ' 9' |
| b_quarter L8 | the bridge-word change at L/4 | '9' (b) | 1 | ' 9' |
| c L32 | S patched into O at every locker-sentence token, at L | '1' (A) | 0 | ' 1' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '1' (A) | 0 | ' 1' |
| S  | S read on S (unedited) | '9' (b) | 1 | ' 9' |

**recall** (PM-L0-0117): O's answer 4, S's answer 6

```
<|im_start|>user
Mark picked the beetle. ⟦The locker of the dog is six.⟧ Lily picked the dog. ⟦The locker of the beetle is nine.⟧ Victor picked the ⟦elephant⟧. ⟦The locker of the elephant is one.⟧
How many legs does Victor's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '4' (A) | 0 | ' 4' |
| a L32 | the bridge-word change at L | '6' (b) | 1 | ' 6' |
| b_half L16 | the bridge-word change at L/2 | '6' (b) | 1 | ' 6' |
| b_quarter L8 | the bridge-word change at L/4 | '6' (b) | 1 | ' 6' |
| c L32 | S patched into O at every locker-sentence token, at L | '4' (A) | 0 | ' 4' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '4' (A) | 0 | ' 4' |
| S  | S read on S (unedited) | '6' (b) | 1 | ' 6' |

## P2-L0-0131 (greek): bridge epsilon → gamma; aligned token; 24 locker tokens patched

**lookup** (PP-L0-0131): O's answer 8, S's answer 9

```
<|im_start|>user
Ryan picked ⟦epsilon⟧. ⟦The locker of epsilon is 8.⟧ ⟦The locker of gamma is 9.⟧ ⟦The locker of theta is 4.⟧ Sara picked theta. Beth picked gamma.
Which locker belongs to Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '8' (A) | 0 | ' 8' |
| a L32 | the bridge-word change at L | '8' (A) | 0 | ' 8' |
| b_half L16 | the bridge-word change at L/2 | '9' (b) | 1 | ' 9' |
| b_quarter L8 | the bridge-word change at L/4 | '9' (b) | 1 | ' 9' |
| c L32 | S patched into O at every locker-sentence token, at L | '9' (b) | 1 | ' 9' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '8' (A) | 0 | ' 8' |
| S  | S read on S (unedited) | '9' (b) | 1 | ' 9' |

**recall** (PM-L0-0131): O's answer 5, S's answer 3

```
<|im_start|>user
Ryan picked ⟦epsilon⟧. ⟦The locker of epsilon is 8.⟧ ⟦The locker of gamma is 9.⟧ ⟦The locker of theta is 4.⟧ Sara picked theta. Beth picked gamma.
Which position in the Greek alphabet does Ryan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '5' (A) | 0 | ' 5' |
| a L32 | the bridge-word change at L | '3' (b) | 1 | ' 3' |
| b_half L16 | the bridge-word change at L/2 | '3' (b) | 1 | ' 3' |
| b_quarter L8 | the bridge-word change at L/4 | '3' (b) | 1 | ' 3' |
| c L32 | S patched into O at every locker-sentence token, at L | '5' (A) | 0 | ' 5' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '5' (A) | 0 | ' 5' |
| S  | S read on S (unedited) | '3' (b) | 1 | ' 3' |

## P2-L0-0136 (elements): bridge hydrogen → oxygen; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0136): O's answer 3, S's answer 6

```
<|im_start|>user
Mia picked ⟦hydrogen⟧. ⟦The locker of hydrogen is three.⟧ ⟦The locker of oxygen is six.⟧ Amy picked oxygen. ⟦The locker of nitrogen is eight.⟧ Jack picked nitrogen.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L32 | the bridge-word change at L | '3' (A) | 0 | ' 3' |
| b_half L16 | the bridge-word change at L/2 | '3' (A) | 0 | ' 3' |
| b_quarter L8 | the bridge-word change at L/4 | '6' (b) | 1 | ' 6' |
| c L32 | S patched into O at every locker-sentence token, at L | '6' (b) | 1 | ' 6' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '1' (other) | 0 | ' 1' |
| S  | S read on S (unedited) | '6' (b) | 1 | ' 6' |

**recall** (PM-L0-0136): O's answer 1, S's answer 8

```
<|im_start|>user
Mia picked ⟦hydrogen⟧. ⟦The locker of hydrogen is three.⟧ ⟦The locker of oxygen is six.⟧ Amy picked oxygen. ⟦The locker of nitrogen is eight.⟧ Jack picked nitrogen.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '1' (A) | 0 | ' 1' |
| a L32 | the bridge-word change at L | '8' (b) | 1 | ' 8' |
| b_half L16 | the bridge-word change at L/2 | '8' (b) | 1 | ' 8' |
| b_quarter L8 | the bridge-word change at L/4 | '8' (b) | 1 | ' 8' |
| c L32 | S patched into O at every locker-sentence token, at L | '1' (A) | 0 | ' 1' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '1' (A) | 0 | ' 1' |
| S  | S read on S (unedited) | '8' (b) | 1 | ' 8' |

## P2-L0-0142 (elements): bridge nitrogen → oxygen; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0142): O's answer 3, S's answer 6

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. ⟦The locker of lithium is eight.⟧ ⟦The locker of oxygen is six.⟧ Owen picked ⟦nitrogen⟧. ⟦The locker of nitrogen is three.⟧
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L32 | the bridge-word change at L | '3' (A) | 0 | ' 3' |
| b_half L16 | the bridge-word change at L/2 | '6' (b) | 1 | ' 6' |
| b_quarter L8 | the bridge-word change at L/4 | '6' (b) | 1 | ' 6' |
| c L32 | S patched into O at every locker-sentence token, at L | '3' (A) | 0 | ' 3' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '3' (A) | 0 | ' 3' |
| S  | S read on S (unedited) | '6' (b) | 1 | ' 6' |

**recall** (PM-L0-0142): O's answer 7, S's answer 8

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. ⟦The locker of lithium is eight.⟧ ⟦The locker of oxygen is six.⟧ Owen picked ⟦nitrogen⟧. ⟦The locker of nitrogen is three.⟧
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '7' (A) | 0 | ' 7' |
| a L32 | the bridge-word change at L | '8' (b) | 1 | ' 8' |
| b_half L16 | the bridge-word change at L/2 | '8' (b) | 1 | ' 8' |
| b_quarter L8 | the bridge-word change at L/4 | '8' (b) | 1 | ' 8' |
| c L32 | S patched into O at every locker-sentence token, at L | '7' (A) | 0 | ' 7' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '7' (A) | 0 | ' 7' |
| S  | S read on S (unedited) | '8' (b) | 1 | ' 8' |

## P2-L0-0208 (elements): bridge lithium → nitrogen; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0208): O's answer 6, S's answer 2

```
<|im_start|>user
⟦The locker of nitrogen is two.⟧ ⟦The locker of carbon is nine.⟧ Victor picked ⟦lithium⟧. Eric picked nitrogen. ⟦The locker of lithium is six.⟧ Eva picked carbon.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '6' (A) | 0 | ' 6' |
| a L32 | the bridge-word change at L | '2' (b) | 1 | ' 2' |
| b_half L16 | the bridge-word change at L/2 | '2' (b) | 1 | ' 2' |
| b_quarter L8 | the bridge-word change at L/4 | '2' (b) | 1 | ' 2' |
| c L32 | S patched into O at every locker-sentence token, at L | '2' (b) | 1 | ' 2' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '6' (A) | 0 | ' 6' |
| S  | S read on S (unedited) | '2' (b) | 1 | ' 2' |

**recall** (PM-L0-0208): O's answer 3, S's answer 7

```
<|im_start|>user
⟦The locker of nitrogen is two.⟧ ⟦The locker of carbon is nine.⟧ Victor picked ⟦lithium⟧. Eric picked nitrogen. ⟦The locker of lithium is six.⟧ Eva picked carbon.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L32 | the bridge-word change at L | '7' (b) | 1 | ' 7' |
| b_half L16 | the bridge-word change at L/2 | '7' (b) | 1 | ' 7' |
| b_quarter L8 | the bridge-word change at L/4 | '7' (b) | 1 | ' 7' |
| c L32 | S patched into O at every locker-sentence token, at L | '3' (A) | 0 | ' 3' |
| d L16 | S patched into O at every locker-sentence token, at L/2 | '3' (A) | 0 | ' 3' |
| S  | S read on S (unedited) | '7' (b) | 1 | ' 7' |

