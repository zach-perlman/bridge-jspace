# Prompts as the model reads them

The org prompt of each reader, chat template applied, the patched token in ⟦ ⟧. The read appends the space token (id 220, ' ') after 'Answer:' and takes the top token over the vocabulary. b = the alt answer's first token, A = the org answer's, other = neither. 'mine' is this check's read; 'stored' is outcomes.jsonl's role and ld.

## 1. P2-L0-0142 (elements): nitrogen -> oxygen

Patched position 27: org token ' nitrogen' (id 44857), alt token ' oxygen' (id 22817). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): Amy picked lithium. Vera picked nitrogen. The locker of lithium is eight. The locker of oxygen is six. Owen picked oxygen. The locker of nitrogen is three.

**PP** (lookup): org answer 3, alt answer 6

```text
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ nitrogen⟧. The locker of nitrogen is three.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 7, alt answer 8

```text
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ nitrogen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '3' (A, ld -5.000) | A (ld -5.000) | '7' (A, ld -5.125) | A (ld -5.125) |
| whole | '3' (A, ld -1.750) | A (ld -1.750) | '8' (b, ld +5.125) | b (ld +5.125) |
| no_part | '3' (A, ld -2.500) | A (ld -2.500) | '7' (A, ld -3.125) | A (ld -3.125) |
| no_rand | '3' (A, ld -2.500) | A (ld -2.625) | '8' (b, ld +4.750) | b (ld +4.750) |

## 2. P2-L0-0290 (greek): epsilon -> iota

Patched position 34: org token ' epsilon' (id 30183), alt token ' iota' (id 79084). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): Sara picked epsilon. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked iota. Noah picked beta.

**PP** (lookup): org answer 4, alt answer 8

```text
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ epsilon⟧. Noah picked beta.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 5, alt answer 9

```text
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ epsilon⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '4' (A, ld -3.375) | A (ld -3.375) | '5' (A, ld -4.625) | A (ld -4.625) |
| whole | '8' (b, ld +1.625) | b (ld +1.625) | '9' (b, ld +3.875) | b (ld +3.875) |
| no_part | '4' (A, ld -0.375) | A (ld -0.375) | '5' (A, ld -2.750) | A (ld -2.750) |
| no_rand | '4' (A, ld -1.125) | A (ld -1.125) | '9' (b, ld +2.750) | b (ld +2.750) |

## 3. P2-L0-0154 (elements): oxygen -> helium

Patched position 24: org token ' oxygen' (id 22817), alt token ' helium' (id 93172). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked helium. Max picked oxygen. The locker of oxygen is five.

**PP** (lookup): org answer 5, alt answer 3

```text
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ oxygen⟧. Max picked helium. The locker of oxygen is five.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 8, alt answer 2

```text
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ oxygen⟧. Max picked helium. The locker of oxygen is five.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '5' (A, ld -3.000) | A (ld -3.000) | '8' (A, ld -4.625) | A (ld -4.625) |
| whole | '5' (A, ld -1.250) | A (ld -1.250) | '2' (b, ld +5.500) | b (ld +5.500) |
| no_part | '5' (A, ld -1.500) | A (ld -1.500) | '2' (b, ld +1.375) | b (ld +1.375) |
| no_rand | '5' (A, ld -1.750) | A (ld -1.750) | '2' (b, ld +5.500) | b (ld +5.500) |

## 4. P2-L0-0017 (greek): iota -> delta

Patched position 30: org token ' iota' (id 79084), alt token ' delta' (id 9197). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): The locker of delta is six. Amy picked iota. The locker of iota is two. The locker of gamma is eight. Leo picked delta. Eva picked gamma.

**PP** (lookup): org answer 2, alt answer 6

```text
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 9, alt answer 4

```text
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '2' (A, ld -5.000) | A (ld -5.000) | '9' (A, ld -4.125) | A (ld -4.125) |
| whole | '6' (b, ld +5.250) | b (ld +5.250) | '4' (b, ld +3.375) | b (ld +3.375) |
| no_part | '6' (b, ld +4.875) | b (ld +4.875) | '4' (b, ld +1.500) | b (ld +1.500) |
| no_rand | '6' (b, ld +4.875) | b (ld +4.875) | '4' (b, ld +2.750) | b (ld +2.750) |

## 5. P2-L0-0096 (animals): bee -> spider

Patched position 43: org token ' bee' (id 35997), alt token ' spider' (id 33213). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): The locker of the bee is 1. Laura picked the bee. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the spider.

**PP** (lookup): org answer 1, alt answer 5

```text
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 6, alt answer 8

```text
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '1' (A, ld -4.375) | A (ld -4.375) | '6' (A, ld -3.625) | A (ld -3.625) |
| whole | '5' (b, ld +3.625) | b (ld +3.625) | '8' (b, ld +2.500) | b (ld +2.500) |
| no_part | '5' (b, ld +3.500) | b (ld +3.500) | '8' (b, ld +1.125) | b (ld +1.125) |
| no_rand | '5' (b, ld +3.125) | b (ld +3.125) | '8' (b, ld +2.125) | b (ld +2.250) |

## 6. P2-L0-0193 (elements): hydrogen -> helium

Patched position 27: org token ' hydrogen' (id 33536), alt token ' helium' (id 93172). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked hydrogen. Victor picked helium. The locker of hydrogen is eight.

**PP** (lookup): org answer 8, alt answer 3

```text
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. Victor picked⟦ hydrogen⟧. The locker of hydrogen is eight.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 1, alt answer 2

```text
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. Victor picked⟦ hydrogen⟧. The locker of hydrogen is eight.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '8' (A, ld -5.438) | A (ld -5.438) | '1' (A, ld -2.875) | A (ld -2.875) |
| whole | '3' (b, ld +0.875) | b (ld +0.875) | '2' (b, ld +3.500) | b (ld +3.500) |
| no_part | '3' (b, ld +0.500) | b (ld +0.500) | '2' (b, ld +3.250) | b (ld +3.250) |
| no_rand | '8' (A, ld -0.500) | A (ld -0.500) | '2' (b, ld +3.375) | b (ld +3.375) |

## 7. P2-L0-0184 (elements): helium -> hydrogen

Patched position 25: org token ' helium' (id 93172), alt token ' hydrogen' (id 33536). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked hydrogen. The locker of hydrogen is 5. Luke picked helium.

**PP** (lookup): org answer 9, alt answer 5

```text
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked⟦ helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 2, alt answer 1

```text
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked⟦ helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '9' (A, ld -4.000) | A (ld -4.000) | '2' (A, ld -3.625) | A (ld -3.625) |
| whole | '5' (b, ld +1.250) | b (ld +1.250) | '1' (b, ld +1.750) | b (ld +1.750) |
| no_part | '2' (other, ld +0.500) | other (ld +0.500) | '2' (A, ld -1.625) | A (ld -1.625) |
| no_rand | '2' (other, ld +0.375) | other (ld +0.375) | '1' (b, ld +0.500) | b (ld +0.500) |

## 8. P2-L0-0149 (greek): delta -> iota

Patched position 29: org token ' delta' (id 9197), alt token ' iota' (id 79084). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked iota. Kate picked gamma. Luke picked delta.

**PP** (lookup): org answer 1, alt answer 8

```text
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦ delta⟧. Kate picked gamma. Luke picked iota.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 4, alt answer 9

```text
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦ delta⟧. Kate picked gamma. Luke picked iota.
Which position in the Greek alphabet does Lucy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '1' (A, ld -3.625) | A (ld -3.625) | '4' (A, ld -4.625) | A (ld -4.625) |
| whole | '8' (b, ld +4.625) | b (ld +4.625) | '9' (b, ld +3.875) | b (ld +3.875) |
| no_part | '8' (b, ld +4.500) | b (ld +4.500) | '9' (b, ld +3.250) | b (ld +3.250) |
| no_rand | '8' (b, ld +4.250) | b (ld +4.375) | '9' (b, ld +4.125) | b (ld +4.125) |

## 9. P2-L0-0110 (greek): iota -> epsilon

Patched position 34: org token ' iota' (id 79084), alt token ' epsilon' (id 30183). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): Ruby picked iota. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked epsilon.

**PP** (lookup): org answer 2, alt answer 7

```text
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked⟦ iota⟧.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 9, alt answer 5

```text
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked⟦ iota⟧.
Which position in the Greek alphabet does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '2' (A, ld -4.375) | A (ld -4.375) | '9' (A, ld -4.500) | A (ld -4.500) |
| whole | '7' (b, ld +2.500) | b (ld +2.500) | '5' (b, ld +5.000) | b (ld +5.000) |
| no_part | '7' (b, ld +1.750) | b (ld +1.750) | '9' (A, ld -0.875) | A (ld -0.875) |
| no_rand | '7' (b, ld +0.125) | b (ld +0.125) | '5' (b, ld +4.375) | b (ld +4.375) |

## 10. P2-L0-0181 (elements): helium -> nitrogen

Patched position 37: org token ' helium' (id 93172), alt token ' nitrogen' (id 44857). Matches cases.jsonl: {'ids': True, 'pos': True, 'answer_tokens': True}.

Alt context (Δ's source): The locker of hydrogen is 5. Maria picked hydrogen. Dan picked helium. The locker of helium is 3. The locker of nitrogen is 9. Adam picked nitrogen.

**PP** (lookup): org answer 3, alt answer 9

```text
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ helium⟧.
Which locker belongs to Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**PM** (recall): org answer 2, alt answer 7

```text
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ helium⟧.
What is the atomic number of Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | PP: mine | PP: stored | PM: mine | PM: stored |
|---|---|---|---|---|
| none | '3' (A, ld -5.875) | A (ld -5.875) | '2' (A, ld -6.375) | A (ld -6.375) |
| whole | '9' (b, ld +5.375) | b (ld +5.375) | '7' (b, ld +4.750) | b (ld +4.750) |
| no_part | '9' (b, ld +4.500) | b (ld +4.500) | '2' (A, ld -0.750) | A (ld -0.750) |
| no_rand | '9' (b, ld +3.625) | b (ld +3.500) | '7' (b, ld +4.000) | b (ld +4.000) |

