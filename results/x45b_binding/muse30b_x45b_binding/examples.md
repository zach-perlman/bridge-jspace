# 45b examples: muse30b_x45b_binding

10 random items of 108 (seed 0); model muse-glimmer-30b, L = 26. Prompts exactly as the model reads them (the read appends the digit's space token); ⟦…⟧ marks the bridge word (arms a, b) and each patched locker-sentence token span (arms c, d; a token's leading space shown outside). Answer = the top token at the read step; greedy = 8 greedy tokens of the edited prompt (no space appended). UNVERIFIED.

## P2-L0-0011 (greek): bridge delta → gamma; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0011): O's answer 6, S's answer 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Dan picked gamma. Eric picked alpha. ⟦The locker of alpha is eight.⟧ Sara picked ⟦delta⟧. ⟦The locker of gamma is five.⟧ ⟦The locker of delta is six.
⟧Which locker belongs to Sara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '6' (A) | 0 | ' 6' |
| a L26 | the bridge-word change at L | '6' (A) | 0 | ' 6' |
| b_half L13 | the bridge-word change at L/2 | '5' (b) | 1 | ' 5' |
| b_quarter L6 | the bridge-word change at L/4 | '5' (b) | 1 | ' 5' |
| c L26 | S patched into O at every locker-sentence token, at L | '5' (b) | 1 | ' 5' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '6' (A) | 0 | ' 6' |
| S  | S read on S (unedited) | '5' (b) | 1 | ' 5' |

**recall** (PM-L0-0011): O's answer 4, S's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Dan picked gamma. Eric picked alpha. ⟦The locker of alpha is eight.⟧ Sara picked ⟦delta⟧. ⟦The locker of gamma is five.⟧ ⟦The locker of delta is six.
⟧Which position in the Greek alphabet does Sara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '4' (A) | 0 | ' 4' |
| a L26 | the bridge-word change at L | '3' (b) | 1 | ' 3' |
| b_half L13 | the bridge-word change at L/2 | '3' (b) | 1 | ' 3' |
| b_quarter L6 | the bridge-word change at L/4 | '3' (b) | 1 | ' 3' |
| c L26 | S patched into O at every locker-sentence token, at L | '4' (A) | 0 | ' 4' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '4' (A) | 0 | ' 4' |
| S  | S read on S (unedited) | '3' (b) | 1 | ' 3' |

## P2-L0-0089 (greek): bridge eta → gamma; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0089): O's answer 2, S's answer 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Fiona picked ⟦eta⟧. Owen picked alpha. ⟦The locker of alpha is eight.⟧ ⟦The locker of eta is two.⟧ Max picked gamma. ⟦The locker of gamma is five.
⟧Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '2' (A) | 0 | ' 2' |
| a L26 | the bridge-word change at L | '2' (A) | 0 | ' 2' |
| b_half L13 | the bridge-word change at L/2 | '2' (A) | 0 | ' 2' |
| b_quarter L6 | the bridge-word change at L/4 | '2' (A) | 0 | ' 2' |
| c L26 | S patched into O at every locker-sentence token, at L | '5' (b) | 1 | ' 5' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '5' (b) | 1 | ' 5' |
| S  | S read on S (unedited) | '5' (b) | 1 | ' 5' |

**recall** (PM-L0-0089): O's answer 7, S's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Fiona picked ⟦eta⟧. Owen picked alpha. ⟦The locker of alpha is eight.⟧ ⟦The locker of eta is two.⟧ Max picked gamma. ⟦The locker of gamma is five.
⟧Which position in the Greek alphabet does Fiona's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '7' (A) | 0 | ' 7' |
| a L26 | the bridge-word change at L | '7' (A) | 0 | ' 7' |
| b_half L13 | the bridge-word change at L/2 | '7' (A) | 0 | ' 7' |
| b_quarter L6 | the bridge-word change at L/4 | '7' (A) | 0 | ' 7' |
| c L26 | S patched into O at every locker-sentence token, at L | '7' (A) | 0 | ' 7' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '7' (A) | 0 | ' 7' |
| S  | S read on S (unedited) | '3' (b) | 1 | ' 3' |

## P2-L0-0124 (elements): bridge nitrogen → oxygen; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0124): O's answer 5, S's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Tara picked ⟦nitrogen⟧. ⟦The locker of carbon is four.⟧ Adam picked oxygen. ⟦The locker of oxygen is three.⟧ ⟦The locker of nitrogen is five.⟧ Noah picked carbon.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '5' (A) | 0 | ' 5' |
| a L26 | the bridge-word change at L | '5' (A) | 0 | ' 5' |
| b_half L13 | the bridge-word change at L/2 | '5' (A) | 0 | ' 5' |
| b_quarter L6 | the bridge-word change at L/4 | '3' (b) | 1 | ' 3' |
| c L26 | S patched into O at every locker-sentence token, at L | '3' (b) | 1 | ' 3' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '5' (A) | 0 | ' 5' |
| S  | S read on S (unedited) | '3' (b) | 1 | ' 3' |

**recall** (PM-L0-0124): O's answer 7, S's answer 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Tara picked ⟦nitrogen⟧. ⟦The locker of carbon is four.⟧ Adam picked oxygen. ⟦The locker of oxygen is three.⟧ ⟦The locker of nitrogen is five.⟧ Noah picked carbon.
What is the atomic number of Tara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '7' (A) | 0 | ' 7' |
| a L26 | the bridge-word change at L | '8' (b) | 1 | ' 8' |
| b_half L13 | the bridge-word change at L/2 | '8' (b) | 1 | ' 8' |
| b_quarter L6 | the bridge-word change at L/4 | '8' (b) | 1 | ' 8' |
| c L26 | S patched into O at every locker-sentence token, at L | '7' (A) | 0 | ' 7' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '7' (A) | 0 | ' 7' |
| S  | S read on S (unedited) | '8' (b) | 1 | ' 8' |

## P2-L0-0136 (elements): bridge hydrogen → oxygen; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0136): O's answer 3, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mia picked ⟦hydrogen⟧. ⟦The locker of hydrogen is three.⟧ ⟦The locker of oxygen is six.⟧ Amy picked oxygen. ⟦The locker of nitrogen is eight.⟧ Jack picked nitrogen.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L26 | the bridge-word change at L | '3' (A) | 0 | ' 3' |
| b_half L13 | the bridge-word change at L/2 | '3' (A) | 0 | ' 3' |
| b_quarter L6 | the bridge-word change at L/4 | '6' (b) | 1 | ' 6' |
| c L26 | S patched into O at every locker-sentence token, at L | '6' (b) | 1 | ' 6' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '6' (b) | 1 | ' 6' |
| S  | S read on S (unedited) | '6' (b) | 1 | ' 6' |

**recall** (PM-L0-0136): O's answer 1, S's answer 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mia picked ⟦hydrogen⟧. ⟦The locker of hydrogen is three.⟧ ⟦The locker of oxygen is six.⟧ Amy picked oxygen. ⟦The locker of nitrogen is eight.⟧ Jack picked nitrogen.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '1' (A) | 0 | ' 1' |
| a L26 | the bridge-word change at L | '8' (b) | 1 | ' 8' |
| b_half L13 | the bridge-word change at L/2 | '8' (b) | 1 | ' 8' |
| b_quarter L6 | the bridge-word change at L/4 | '8' (b) | 1 | ' 8' |
| c L26 | S patched into O at every locker-sentence token, at L | '1' (A) | 0 | ' 1' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '1' (A) | 0 | ' 1' |
| S  | S read on S (unedited) | '8' (b) | 1 | ' 8' |

## P2-L0-0142 (elements): bridge nitrogen → oxygen; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0142): O's answer 3, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Amy picked lithium. Vera picked oxygen. ⟦The locker of lithium is eight.⟧ ⟦The locker of oxygen is six.⟧ Owen picked ⟦nitrogen⟧. ⟦The locker of nitrogen is three.
⟧Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L26 | the bridge-word change at L | '3' (A) | 0 | ' 3' |
| b_half L13 | the bridge-word change at L/2 | '6' (b) | 1 | ' 6' |
| b_quarter L6 | the bridge-word change at L/4 | '6' (b) | 1 | ' 6' |
| c L26 | S patched into O at every locker-sentence token, at L | '3' (A) | 0 | ' 3' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '3' (A) | 0 | ' 3' |
| S  | S read on S (unedited) | '6' (b) | 1 | ' 6' |

**recall** (PM-L0-0142): O's answer 7, S's answer 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Amy picked lithium. Vera picked oxygen. ⟦The locker of lithium is eight.⟧ ⟦The locker of oxygen is six.⟧ Owen picked ⟦nitrogen⟧. ⟦The locker of nitrogen is three.
⟧What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '7' (A) | 0 | ' 7' |
| a L26 | the bridge-word change at L | '8' (b) | 1 | ' 8' |
| b_half L13 | the bridge-word change at L/2 | '8' (b) | 1 | ' 8' |
| b_quarter L6 | the bridge-word change at L/4 | '8' (b) | 1 | ' 8' |
| c L26 | S patched into O at every locker-sentence token, at L | '7' (A) | 0 | ' 7' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '7' (A) | 0 | ' 7' |
| S  | S read on S (unedited) | '8' (b) | 1 | ' 8' |

## P2-L0-0165 (animals): bridge sheep → chicken; aligned token; 27 locker tokens patched

**lookup** (PP-L0-0165): O's answer 3, S's answer 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Paul picked the ⟦sheep⟧. ⟦The locker of the sheep is 3.⟧ Will picked the deer. ⟦The locker of the deer is 7.⟧ Zoe picked the chicken. ⟦The locker of the chicken is 1.
⟧Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L26 | the bridge-word change at L | '3' (A) | 0 | ' 3' |
| b_half L13 | the bridge-word change at L/2 | '3' (A) | 0 | ' 3' |
| b_quarter L6 | the bridge-word change at L/4 | '3' (A) | 0 | ' 3' |
| c L26 | S patched into O at every locker-sentence token, at L | '1' (b) | 1 | ' 1' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '3' (A) | 0 | ' 3' |
| S  | S read on S (unedited) | '1' (b) | 1 | ' 1' |

**recall** (PM-L0-0165): O's answer 4, S's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Paul picked the ⟦sheep⟧. ⟦The locker of the sheep is 3.⟧ Will picked the deer. ⟦The locker of the deer is 7.⟧ Zoe picked the chicken. ⟦The locker of the chicken is 1.
⟧How many legs does Paul's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '4' (A) | 0 | ' 4' |
| a L26 | the bridge-word change at L | '2' (b) | 1 | ' 2' |
| b_half L13 | the bridge-word change at L/2 | '2' (b) | 1 | ' 2' |
| b_quarter L6 | the bridge-word change at L/4 | '4' (A) | 0 | ' 4' |
| c L26 | S patched into O at every locker-sentence token, at L | '4' (A) | 0 | ' 4' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '4' (A) | 0 | ' 4' |
| S  | S read on S (unedited) | '2' (b) | 1 | ' 2' |

## P2-L0-0173 (greek): bridge theta → delta; aligned token; 24 locker tokens patched

**lookup** (PP-L0-0173): O's answer 3, S's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Ben picked ⟦theta⟧. Hugo picked delta. ⟦The locker of delta is 6.⟧ ⟦The locker of theta is 3.⟧ ⟦The locker of beta is 4.⟧ Carl picked beta.
Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L26 | the bridge-word change at L | '3' (A) | 0 | ' 3' |
| b_half L13 | the bridge-word change at L/2 | '3' (A) | 0 | ' 3' |
| b_quarter L6 | the bridge-word change at L/4 | '6' (b) | 1 | ' 6' |
| c L26 | S patched into O at every locker-sentence token, at L | '6' (b) | 1 | ' 6' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '3' (A) | 0 | ' 3' |
| S  | S read on S (unedited) | '6' (b) | 1 | ' 6' |

**recall** (PM-L0-0173): O's answer 8, S's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Ben picked ⟦theta⟧. Hugo picked delta. ⟦The locker of delta is 6.⟧ ⟦The locker of theta is 3.⟧ ⟦The locker of beta is 4.⟧ Carl picked beta.
Which position in the Greek alphabet does Ben's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '19' (other) | 0 | ' 8' |
| a L26 | the bridge-word change at L | '19' (other) | 0 | ' 19' |
| b_half L13 | the bridge-word change at L/2 | '4' (b) | 1 | ' 4' |
| b_quarter L6 | the bridge-word change at L/4 | '4' (b) | 1 | ' 4' |
| c L26 | S patched into O at every locker-sentence token, at L | '4' (b) | 1 | ' 4' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '8' (A) | 0 | ' 8' |
| S  | S read on S (unedited) | '4' (b) | 1 | ' 4' |

## P2-L0-0266 (greek): bridge gamma → delta; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0266): O's answer 2, S's answer 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mia picked eta. ⟦The locker of delta is five.⟧ Jack picked ⟦gamma⟧. ⟦The locker of eta is nine.⟧ ⟦The locker of gamma is two.⟧ Henry picked delta.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '2' (A) | 0 | ' 2' |
| a L26 | the bridge-word change at L | '5' (b) | 1 | ' 5' |
| b_half L13 | the bridge-word change at L/2 | '5' (b) | 1 | ' 5' |
| b_quarter L6 | the bridge-word change at L/4 | '5' (b) | 1 | ' 5' |
| c L26 | S patched into O at every locker-sentence token, at L | '9' (other) | 0 | ' 9' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '2' (A) | 0 | ' 2' |
| S  | S read on S (unedited) | '5' (b) | 1 | ' 5' |

**recall** (PM-L0-0266): O's answer 3, S's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mia picked eta. ⟦The locker of delta is five.⟧ Jack picked ⟦gamma⟧. ⟦The locker of eta is nine.⟧ ⟦The locker of gamma is two.⟧ Henry picked delta.
Which position in the Greek alphabet does Jack's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '3' (A) | 0 | ' 3' |
| a L26 | the bridge-word change at L | '4' (b) | 1 | ' 4' |
| b_half L13 | the bridge-word change at L/2 | '4' (b) | 1 | ' 4' |
| b_quarter L6 | the bridge-word change at L/4 | '4' (b) | 1 | ' 4' |
| c L26 | S patched into O at every locker-sentence token, at L | '3' (A) | 0 | ' 3' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '3' (A) | 0 | ' 3' |
| S  | S read on S (unedited) | '4' (b) | 1 | ' 4' |

## P2-L0-0274 (elements): bridge oxygen → lithium; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0274): O's answer 1, S's answer 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦The locker of lithium is seven.⟧ Julia picked ⟦oxygen⟧. ⟦The locker of nitrogen is three.⟧ James picked lithium. Carl picked nitrogen. ⟦The locker of oxygen is one.
⟧Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '1' (A) | 0 | ' 1' |
| a L26 | the bridge-word change at L | '7' (b) | 1 | ' 7' |
| b_half L13 | the bridge-word change at L/2 | '7' (b) | 1 | ' 7' |
| b_quarter L6 | the bridge-word change at L/4 | '7' (b) | 1 | ' 7' |
| c L26 | S patched into O at every locker-sentence token, at L | '7' (b) | 1 | ' 7' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '1' (A) | 0 | ' 1' |
| S  | S read on S (unedited) | '7' (b) | 1 | ' 7' |

**recall** (PM-L0-0274): O's answer 8, S's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦The locker of lithium is seven.⟧ Julia picked ⟦oxygen⟧. ⟦The locker of nitrogen is three.⟧ James picked lithium. Carl picked nitrogen. ⟦The locker of oxygen is one.
⟧What is the atomic number of Julia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '8' (A) | 0 | ' 8' |
| a L26 | the bridge-word change at L | '3' (b) | 1 | ' 3' |
| b_half L13 | the bridge-word change at L/2 | '3' (b) | 1 | ' 3' |
| b_quarter L6 | the bridge-word change at L/4 | '3' (b) | 1 | ' 3' |
| c L26 | S patched into O at every locker-sentence token, at L | '8' (A) | 0 | ' 8' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '8' (A) | 0 | ' 8' |
| S  | S read on S (unedited) | '3' (b) | 1 | ' 3' |

## P2-L0-0284 (greek): bridge delta → epsilon; aligned token; 21 locker tokens patched

**lookup** (PP-L0-0284): O's answer 7, S's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked ⟦delta⟧. Julia picked beta. Hugo picked epsilon. ⟦The locker of epsilon is three.⟧ ⟦The locker of delta is seven.⟧ ⟦The locker of beta is four.
⟧Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '7' (A) | 0 | ' 7' |
| a L26 | the bridge-word change at L | '7' (A) | 0 | ' 7' |
| b_half L13 | the bridge-word change at L/2 | '7' (A) | 0 | ' 7' |
| b_quarter L6 | the bridge-word change at L/4 | '3' (b) | 1 | ' 3' |
| c L26 | S patched into O at every locker-sentence token, at L | '3' (b) | 1 | ' 3' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '7' (A) | 0 | ' 7' |
| S  | S read on S (unedited) | '3' (b) | 1 | ' 3' |

**recall** (PM-L0-0284): O's answer 4, S's answer 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked ⟦delta⟧. Julia picked beta. Hugo picked epsilon. ⟦The locker of epsilon is three.⟧ ⟦The locker of delta is seven.⟧ ⟦The locker of beta is four.
⟧Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | answer (top token) | switched | greedy |
|---|---|---|---|---|
| none  | O unedited | '4' (A) | 0 | ' 4' |
| a L26 | the bridge-word change at L | '4' (A) | 0 | ' 4' |
| b_half L13 | the bridge-word change at L/2 | '4' (A) | 0 | ' 4' |
| b_quarter L6 | the bridge-word change at L/4 | '5' (b) | 1 | ' 5' |
| c L26 | S patched into O at every locker-sentence token, at L | '4' (A) | 0 | ' 4' |
| d L13 | S patched into O at every locker-sentence token, at L/2 | '4' (A) | 0 | ' 4' |
| S  | S read on S (unedited) | '5' (b) | 1 | ' 5' |

