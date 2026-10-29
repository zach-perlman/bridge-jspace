# 47.1 verify pack: prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the bridge word, where the change (or the arm's part of it) is added at L. UNVERIFIED.

## nemotron-3.5-lightning

### routes test, another item moved (C2): nem35l_x52_routes_x47_1, 10 random items of 300 (seed 0)

#### C2-0046: bridge crow → horse, token 48; expected digits {'identity': 3, 'position': 5, 'value': 4, 'original': 9}

**lookup**: O's answer 9, S's answer 4

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the crow is 9. The locker of the wolf is 5. The locker of the horse is 3. Eve picked the horse. Owen picked the wolf. Peter picked the⟦ crow⟧.
Which locker belongs to Peter's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' | original | 0 |  |
| whole | '3' | identity | 0 |  |
| no_jpp | '3' | identity | 0 |  |
| no_jpp_rand | '3' | identity | 0 |  |
| no_alf | '9' | original | 0 |  |
| no_alf_rand | '3' | identity | 0 |  |
| no_jpp100 | '3' | identity | 0 |  |
| no_jpp100_rand | '3' | identity | 0 |  |
| no_jpp26_100 | '3' | identity | 0 |  |
| no_jpp26_100_rand | '3' | identity | 0 |  |
| no_ratoms75 | '3' | identity | 0 |  |
| no_ratoms75_rand | '3' | identity | 0 |  |
| no_ratoms75own | '3' | identity | 0 |  |
| no_ratoms75own_rand | '3' | identity | 0 |  |

**recall**: O's answer 2, S's answer 4

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the crow is 9. The locker of the wolf is 5. The locker of the horse is 3. Eve picked the horse. Owen picked the wolf. Peter picked the⟦ crow⟧.
How many legs does Peter's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '4' |  | 1 |  |
| no_jpp | '4' |  | 1 |  |
| no_jpp_rand | '4' |  | 1 |  |
| no_alf | '4' |  | 1 |  |
| no_alf_rand | '4' |  | 1 |  |
| no_jpp100 | '4' |  | 1 |  |
| no_jpp100_rand | '4' |  | 1 |  |
| no_jpp26_100 | '4' |  | 1 |  |
| no_jpp26_100_rand | '4' |  | 1 |  |
| no_ratoms75 | '4' |  | 1 |  |
| no_ratoms75_rand | '4' |  | 1 |  |
| no_ratoms75own | '4' |  | 1 |  |
| no_ratoms75own_rand | '4' |  | 1 |  |

#### C2-0304: bridge ant → rabbit, token 43; expected digits {'identity': 7, 'position': 4, 'value': 8, 'original': 6}

**lookup**: O's answer 6, S's answer 8

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the fox is 4. The locker of the ant is 6. The locker of the rabbit is 7. Ruby picked the rabbit. Eric picked the⟦ ant⟧. James picked the fox.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' | original | 0 |  |
| whole | '4' | position | 0 |  |
| no_jpp | '4' | position | 0 |  |
| no_jpp_rand | '4' | position | 0 |  |
| no_alf | '6' | original | 0 |  |
| no_alf_rand | '4' | position | 0 |  |
| no_jpp100 | '4' | position | 0 |  |
| no_jpp100_rand | '6' | original | 0 |  |
| no_jpp26_100 | '4' | position | 0 |  |
| no_jpp26_100_rand | '4' | position | 0 |  |
| no_ratoms75 | '4' | position | 0 |  |
| no_ratoms75_rand | '4' | position | 0 |  |
| no_ratoms75own | '4' | position | 0 |  |
| no_ratoms75own_rand | '4' | position | 0 |  |

**recall**: O's answer 6, S's answer 4

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the fox is 4. The locker of the ant is 6. The locker of the rabbit is 7. Ruby picked the rabbit. Eric picked the⟦ ant⟧. James picked the fox.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '4' |  | 1 |  |
| no_jpp | '4' |  | 1 |  |
| no_jpp_rand | '4' |  | 1 |  |
| no_alf | '4' |  | 1 |  |
| no_alf_rand | '4' |  | 1 |  |
| no_jpp100 | '4' |  | 1 |  |
| no_jpp100_rand | '4' |  | 1 |  |
| no_jpp26_100 | '4' |  | 1 |  |
| no_jpp26_100_rand | '4' |  | 1 |  |
| no_ratoms75 | '4' |  | 1 |  |
| no_ratoms75_rand | '4' |  | 1 |  |
| no_ratoms75own | '4' |  | 1 |  |
| no_ratoms75own_rand | '4' |  | 1 |  |

#### C2-0357: bridge dog → duck, token 48; expected digits {'identity': 2, 'position': 9, 'value': 7, 'original': 6}

**lookup**: O's answer 6, S's answer 7

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the duck is 2. The locker of the dog is 6. The locker of the deer is 9. Clara picked the deer. Alice picked the duck. Frank picked the⟦ dog⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' | original | 0 |  |
| whole | '9' | position | 0 |  |
| no_jpp | '9' | position | 0 |  |
| no_jpp_rand | '9' | position | 0 |  |
| no_alf | '6' | original | 0 |  |
| no_alf_rand | '9' | position | 0 |  |
| no_jpp100 | '6' | original | 0 |  |
| no_jpp100_rand | '6' | original | 0 |  |
| no_jpp26_100 | '9' | position | 0 |  |
| no_jpp26_100_rand | '9' | position | 0 |  |
| no_ratoms75 | '9' | position | 0 |  |
| no_ratoms75_rand | '9' | position | 0 |  |
| no_ratoms75own | '9' | position | 0 |  |
| no_ratoms75own_rand | '9' | position | 0 |  |

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the duck is 2. The locker of the dog is 6. The locker of the deer is 9. Clara picked the deer. Alice picked the duck. Frank picked the⟦ dog⟧.
How many legs does Frank's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '2' |  | 1 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '4' |  | 0 |  |
| no_alf | '4' |  | 0 |  |
| no_alf_rand | '2' |  | 1 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '4' |  | 0 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '4' |  | 0 |  |
| no_ratoms75 | '2' |  | 1 |  |
| no_ratoms75_rand | '4' |  | 0 |  |
| no_ratoms75own | '2' |  | 1 |  |
| no_ratoms75own_rand | '2' |  | 1 |  |

#### C2-0430: bridge spider → fox, token 38; expected digits {'identity': 6, 'position': 2, 'value': 4, 'original': 5}

**lookup**: O's answer 5, S's answer 4

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the dog is 2. The locker of the spider is 5. The locker of the fox is 6. Sam picked the⟦ spider⟧. Victor picked the fox. Sara picked the dog.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' | original | 0 |  |
| whole | '2' | position | 0 |  |
| no_jpp | '2' | position | 0 |  |
| no_jpp_rand | '2' | position | 0 |  |
| no_alf | '5' | original | 0 |  |
| no_alf_rand | '2' | position | 0 |  |
| no_jpp100 | '2' | position | 0 |  |
| no_jpp100_rand | '2' | position | 0 |  |
| no_jpp26_100 | '2' | position | 0 |  |
| no_jpp26_100_rand | '2' | position | 0 |  |
| no_ratoms75 | '2' | position | 0 |  |
| no_ratoms75_rand | '2' | position | 0 |  |
| no_ratoms75own | '2' | position | 0 |  |
| no_ratoms75own_rand | '2' | position | 0 |  |

**recall**: O's answer 8, S's answer 4

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the dog is 2. The locker of the spider is 5. The locker of the fox is 6. Sam picked the⟦ spider⟧. Victor picked the fox. Sara picked the dog.
How many legs does Sam's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '4' |  | 1 |  |
| no_jpp | '4' |  | 1 |  |
| no_jpp_rand | '4' |  | 1 |  |
| no_alf | '8' |  | 0 |  |
| no_alf_rand | '4' |  | 1 |  |
| no_jpp100 | '8' |  | 0 |  |
| no_jpp100_rand | '8' |  | 0 |  |
| no_jpp26_100 | '4' |  | 1 |  |
| no_jpp26_100_rand | '4' |  | 1 |  |
| no_ratoms75 | '4' |  | 1 |  |
| no_ratoms75_rand | '4' |  | 1 |  |
| no_ratoms75own | '4' |  | 1 |  |
| no_ratoms75own_rand | '4' |  | 1 |  |

#### C2-0475: bridge fly → turkey, token 48; expected digits {'identity': 2, 'position': 9, 'value': 3, 'original': 7}

**lookup**: O's answer 7, S's answer 3

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the fly is 7. The locker of the turkey is 2. The locker of the dog is 9. Ivan picked the dog. Sara picked the turkey. Victor picked the⟦ fly⟧.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' | original | 0 |  |
| whole | '2' | identity | 0 |  |
| no_jpp | '2' | identity | 0 |  |
| no_jpp_rand | '2' | identity | 0 |  |
| no_alf | '7' | original | 0 |  |
| no_alf_rand | '2' | identity | 0 |  |
| no_jpp100 | '2' | identity | 0 |  |
| no_jpp100_rand | '2' | identity | 0 |  |
| no_jpp26_100 | '2' | identity | 0 |  |
| no_jpp26_100_rand | '2' | identity | 0 |  |
| no_ratoms75 | '2' | identity | 0 |  |
| no_ratoms75_rand | '2' | identity | 0 |  |
| no_ratoms75own | '2' | identity | 0 |  |
| no_ratoms75own_rand | '2' | identity | 0 |  |

**recall**: O's answer 6, S's answer 2

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the fly is 7. The locker of the turkey is 2. The locker of the dog is 9. Ivan picked the dog. Sara picked the turkey. Victor picked the⟦ fly⟧.
How many legs does Victor's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '2' |  | 1 |  |
| no_jpp | '2' |  | 1 |  |
| no_jpp_rand | '2' |  | 1 |  |
| no_alf | '6' |  | 0 |  |
| no_alf_rand | '2' |  | 1 |  |
| no_jpp100 | '2' |  | 1 |  |
| no_jpp100_rand | '2' |  | 1 |  |
| no_jpp26_100 | '2' |  | 1 |  |
| no_jpp26_100_rand | '2' |  | 1 |  |
| no_ratoms75 | '2' |  | 1 |  |
| no_ratoms75_rand | '2' |  | 1 |  |
| no_ratoms75own | '2' |  | 1 |  |
| no_ratoms75own_rand | '2' |  | 1 |  |

#### C2-0492: bridge cat → duck, token 48; expected digits {'identity': 8, 'position': 5, 'value': 7, 'original': 4}

**lookup**: O's answer 4, S's answer 7

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the cat is 4. The locker of the duck is 8. The locker of the bear is 5. Lily picked the bear. Frank picked the duck. Anna picked the⟦ cat⟧.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '8' | identity | 0 |  |
| no_jpp | '8' | identity | 0 |  |
| no_jpp_rand | '8' | identity | 0 |  |
| no_alf | '4' | original | 0 |  |
| no_alf_rand | '8' | identity | 0 |  |
| no_jpp100 | '8' | identity | 0 |  |
| no_jpp100_rand | '8' | identity | 0 |  |
| no_jpp26_100 | '8' | identity | 0 |  |
| no_jpp26_100_rand | '8' | identity | 0 |  |
| no_ratoms75 | '8' | identity | 0 |  |
| no_ratoms75_rand | '8' | identity | 0 |  |
| no_ratoms75own | '8' | identity | 0 |  |
| no_ratoms75own_rand | '8' | identity | 0 |  |

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the cat is 4. The locker of the duck is 8. The locker of the bear is 5. Lily picked the bear. Frank picked the duck. Anna picked the⟦ cat⟧.
How many legs does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '2' |  | 1 |  |
| no_jpp | '2' |  | 1 |  |
| no_jpp_rand | '2' |  | 1 |  |
| no_alf | '4' |  | 0 |  |
| no_alf_rand | '2' |  | 1 |  |
| no_jpp100 | '2' |  | 1 |  |
| no_jpp100_rand | '2' |  | 1 |  |
| no_jpp26_100 | '2' |  | 1 |  |
| no_jpp26_100_rand | '2' |  | 1 |  |
| no_ratoms75 | '2' |  | 1 |  |
| no_ratoms75_rand | '2' |  | 1 |  |
| no_ratoms75own | '2' |  | 1 |  |
| no_ratoms75own_rand | '2' |  | 1 |  |

#### C2-0511: bridge owl → butterfly, token 48; expected digits {'identity': 1, 'position': 4, 'value': 7, 'original': 2}

**lookup**: O's answer 2, S's answer 7

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the owl is 2. The locker of the butterfly is 1. The locker of the lion is 4. Eve picked the lion. Carl picked the butterfly. Zoe picked the⟦ owl⟧.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' | original | 0 |  |
| whole | '1' | identity | 0 |  |
| no_jpp | '1' | identity | 0 |  |
| no_jpp_rand | '1' | identity | 0 |  |
| no_alf | '2' | original | 0 |  |
| no_alf_rand | '1' | identity | 0 |  |
| no_jpp100 | '1' | identity | 0 |  |
| no_jpp100_rand | '1' | identity | 0 |  |
| no_jpp26_100 | '1' | identity | 0 |  |
| no_jpp26_100_rand | '1' | identity | 0 |  |
| no_ratoms75 | '1' | identity | 0 |  |
| no_ratoms75_rand | '1' | identity | 0 |  |
| no_ratoms75own | '1' | identity | 0 |  |
| no_ratoms75own_rand | '1' | identity | 0 |  |

**recall**: O's answer 2, S's answer 6

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the owl is 2. The locker of the butterfly is 1. The locker of the lion is 4. Eve picked the lion. Carl picked the butterfly. Zoe picked the⟦ owl⟧.
How many legs does Zoe's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '4' |  | 0 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '6' |  | 1 |  |
| no_alf | '2' |  | 0 |  |
| no_alf_rand | '4' |  | 0 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '6' |  | 1 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '4' |  | 0 |  |
| no_ratoms75 | '4' |  | 0 |  |
| no_ratoms75_rand | '4' |  | 0 |  |
| no_ratoms75own | '4' |  | 0 |  |
| no_ratoms75own_rand | '4' |  | 0 |  |

#### C2-0567: bridge tick → elephant, token 38; expected digits {'identity': 4, 'position': 3, 'value': 6, 'original': 2}

**lookup**: O's answer 2, S's answer 6

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the elephant is 4. The locker of the tick is 2. The locker of the deer is 3. Fiona picked the⟦ tick⟧. Zoe picked the elephant. Tom picked the deer.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' | original | 0 |  |
| whole | '3' | position | 0 |  |
| no_jpp | '3' | position | 0 |  |
| no_jpp_rand | '3' | position | 0 |  |
| no_alf | '3' | position | 0 |  |
| no_alf_rand | '3' | position | 0 |  |
| no_jpp100 | '3' | position | 0 |  |
| no_jpp100_rand | '3' | position | 0 |  |
| no_jpp26_100 | '3' | position | 0 |  |
| no_jpp26_100_rand | '3' | position | 0 |  |
| no_ratoms75 | '3' | position | 0 |  |
| no_ratoms75_rand | '3' | position | 0 |  |
| no_ratoms75own | '3' | position | 0 |  |
| no_ratoms75own_rand | '3' | position | 0 |  |

**recall**: O's answer 8, S's answer 4

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the elephant is 4. The locker of the tick is 2. The locker of the deer is 3. Fiona picked the⟦ tick⟧. Zoe picked the elephant. Tom picked the deer.
How many legs does Fiona's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '4' |  | 1 |  |
| no_jpp | '4' |  | 1 |  |
| no_jpp_rand | '4' |  | 1 |  |
| no_alf | '4' |  | 1 |  |
| no_alf_rand | '4' |  | 1 |  |
| no_jpp100 | '4' |  | 1 |  |
| no_jpp100_rand | '4' |  | 1 |  |
| no_jpp26_100 | '4' |  | 1 |  |
| no_jpp26_100_rand | '4' |  | 1 |  |
| no_ratoms75 | '4' |  | 1 |  |
| no_ratoms75_rand | '4' |  | 1 |  |
| no_ratoms75own | '4' |  | 1 |  |
| no_ratoms75own_rand | '4' |  | 1 |  |

#### C2-0575: bridge ant → tiger, token 43; expected digits {'identity': 4, 'position': 6, 'value': 9, 'original': 2}

**lookup**: O's answer 2, S's answer 9

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the ant is 2. The locker of the tiger is 4. The locker of the bear is 6. Lily picked the bear. Carl picked the⟦ ant⟧. Eve picked the tiger.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' | original | 0 |  |
| whole | '6' | position | 0 |  |
| no_jpp | '6' | position | 0 |  |
| no_jpp_rand | '6' | position | 0 |  |
| no_alf | '2' | original | 0 |  |
| no_alf_rand | '6' | position | 0 |  |
| no_jpp100 | '6' | position | 0 |  |
| no_jpp100_rand | '4' | identity | 0 |  |
| no_jpp26_100 | '6' | position | 0 |  |
| no_jpp26_100_rand | '6' | position | 0 |  |
| no_ratoms75 | '6' | position | 0 |  |
| no_ratoms75_rand | '6' | position | 0 |  |
| no_ratoms75own | '6' | position | 0 |  |
| no_ratoms75own_rand | '6' | position | 0 |  |

**recall**: O's answer 6, S's answer 4

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the ant is 2. The locker of the tiger is 4. The locker of the bear is 6. Lily picked the bear. Carl picked the⟦ ant⟧. Eve picked the tiger.
How many legs does Carl's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '4' |  | 1 |  |
| no_jpp | '4' |  | 1 |  |
| no_jpp_rand | '4' |  | 1 |  |
| no_alf | '6' |  | 0 |  |
| no_alf_rand | '4' |  | 1 |  |
| no_jpp100 | '4' |  | 1 |  |
| no_jpp100_rand | '4' |  | 1 |  |
| no_jpp26_100 | '4' |  | 1 |  |
| no_jpp26_100_rand | '4' |  | 1 |  |
| no_ratoms75 | '4' |  | 1 |  |
| no_ratoms75_rand | '4' |  | 1 |  |
| no_ratoms75own | '4' |  | 1 |  |
| no_ratoms75own_rand | '4' |  | 1 |  |

#### C2-0602: bridge ant → cat, token 38; expected digits {'identity': 9, 'position': 1, 'value': 3, 'original': 4}

**lookup**: O's answer 4, S's answer 3

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the cat is 9. The locker of the eagle is 1. The locker of the ant is 4. Sam picked the⟦ ant⟧. Adam picked the eagle. Grace picked the cat.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '1' | position | 0 |  |
| no_jpp | '1' | position | 0 |  |
| no_jpp_rand | '4' | original | 0 |  |
| no_alf | '4' | original | 0 |  |
| no_alf_rand | '1' | position | 0 |  |
| no_jpp100 | '4' | original | 0 |  |
| no_jpp100_rand | '4' | original | 0 |  |
| no_jpp26_100 | '1' | position | 0 |  |
| no_jpp26_100_rand | '1' | position | 0 |  |
| no_ratoms75 | '1' | position | 0 |  |
| no_ratoms75_rand | '1' | position | 0 |  |
| no_ratoms75own | '1' | position | 0 |  |
| no_ratoms75own_rand | '1' | position | 0 |  |

**recall**: O's answer 6, S's answer 4

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the cat is 9. The locker of the eagle is 1. The locker of the ant is 4. Sam picked the⟦ ant⟧. Adam picked the eagle. Grace picked the cat.
How many legs does Sam's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '2' |  | 0 |  |
| no_jpp | '2' |  | 0 |  |
| no_jpp_rand | '4' |  | 1 |  |
| no_alf | '4' |  | 1 |  |
| no_alf_rand | '4' |  | 1 |  |
| no_jpp100 | '6' |  | 0 |  |
| no_jpp100_rand | '6' |  | 0 |  |
| no_jpp26_100 | '4' |  | 1 |  |
| no_jpp26_100_rand | '4' |  | 1 |  |
| no_ratoms75 | '2' |  | 0 |  |
| no_ratoms75_rand | '4' |  | 1 |  |
| no_ratoms75own | '2' |  | 0 |  |
| no_ratoms75own_rand | '2' |  | 0 |  |

### main test (two people swap picks): nem35l_x52_x47_1_main, 10 random items of 200 (seed 0)

#### P2-L0-0037: bridge hydrogen → oxygen, token 10

**lookup**: O's answer 7, S's answer 9

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Carl picked⟦ hydrogen⟧. The locker of hydrogen is seven. Iris picked helium. The locker of helium is five. Clara picked oxygen. The locker of oxygen is nine.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '7' |  | 0 | ' 7' |
| no_part jpp/25/signed | '7' |  | 0 | ' 7' |
| no_rand jpp/25/signed | '7' |  | 0 | ' 7' |
| no_part jpp/50/signed | '7' |  | 0 |  |
| no_rand jpp/50/signed | '7' |  | 0 |  |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '7' |  | 0 |  |
| no_part jpp/200/signed | '7' |  | 0 |  |
| no_rand jpp/200/signed | '7' |  | 0 |  |
| no_part jpp26_100/75/slice | '7' |  | 0 |  |
| no_rand jpp26_100/75/slice | '7' |  | 0 |  |
| no_part ratoms75/75/scaled | '7' |  | 0 |  |
| no_rand ratoms75/75/scaled | '7' |  | 0 |  |
| no_part ratoms75own/75/own | '7' |  | 0 |  |
| no_rand ratoms75own/75/own | '7' |  | 0 |  |

**recall**: O's answer 1, S's answer 8

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Carl picked⟦ hydrogen⟧. The locker of hydrogen is seven. Iris picked helium. The locker of helium is five. Clara picked oxygen. The locker of oxygen is nine.
What is the atomic number of Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' |  | 0 |  |
| whole | '7' |  | 0 | ' 7' |
| no_part jpp/25/signed | '1' |  | 0 | ' 1' |
| no_rand jpp/25/signed | '7' |  | 0 | ' 7' |
| no_part jpp/50/signed | '1' |  | 0 |  |
| no_rand jpp/50/signed | '1' |  | 0 |  |
| no_part jpp/100/signed | '1' |  | 0 |  |
| no_rand jpp/100/signed | '1' |  | 0 |  |
| no_part jpp/200/signed | '1' |  | 0 |  |
| no_rand jpp/200/signed | '1' |  | 0 |  |
| no_part jpp26_100/75/slice | '7' |  | 0 |  |
| no_rand jpp26_100/75/slice | '7' |  | 0 |  |
| no_part ratoms75/75/scaled | '7' |  | 0 |  |
| no_rand ratoms75/75/scaled | '7' |  | 0 |  |
| no_part ratoms75own/75/own | '7' |  | 0 |  |
| no_rand ratoms75own/75/own | '7' |  | 0 |  |

#### P2-L0-0165: bridge sheep → chicken, token 11

**lookup**: O's answer 3, S's answer 1

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Paul picked the⟦ sheep⟧. The locker of the sheep is 3. Will picked the deer. The locker of the deer is 7. Zoe picked the chicken. The locker of the chicken is 1.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '3' |  | 0 | ' 3' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 0 | ' 3' |
| no_part jpp/50/signed | '3' |  | 0 |  |
| no_rand jpp/50/signed | '3' |  | 0 |  |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp/200/signed | '3' |  | 0 |  |
| no_rand jpp/200/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 0 |  |
| no_rand jpp26_100/75/slice | '3' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 0 |  |
| no_rand ratoms75/75/scaled | '3' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 0 |  |

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Paul picked the⟦ sheep⟧. The locker of the sheep is 3. Will picked the deer. The locker of the deer is 7. Zoe picked the chicken. The locker of the chicken is 1.
How many legs does Paul's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '2' |  | 1 | ' 2' |
| no_part jpp/25/signed | '4' |  | 0 | ' 4' |
| no_rand jpp/25/signed | '2' |  | 1 | ' 2' |
| no_part jpp/50/signed | '4' |  | 0 |  |
| no_rand jpp/50/signed | '2' |  | 1 |  |
| no_part jpp/100/signed | '4' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 0 |  |
| no_part jpp/200/signed | '4' |  | 0 |  |
| no_rand jpp/200/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '2' |  | 1 |  |
| no_rand jpp26_100/75/slice | '2' |  | 1 |  |
| no_part ratoms75/75/scaled | '2' |  | 1 |  |
| no_rand ratoms75/75/scaled | '2' |  | 1 |  |
| no_part ratoms75own/75/own | '2' |  | 1 |  |
| no_rand ratoms75own/75/own | '2' |  | 1 |  |

#### P2-L0-0185: bridge epsilon → gamma, token 26

**lookup**: O's answer 8, S's answer 5

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of gamma is 5. The locker of epsilon is 8. James picked⟦ epsilon⟧. The locker of alpha is 6. Emma picked alpha. Fiona picked gamma.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '5' |  | 1 | ' 5' |
| no_part jpp/25/signed | '5' |  | 1 | ' 5' |
| no_rand jpp/25/signed | '5' |  | 1 | ' 5' |
| no_part jpp/50/signed | '5' |  | 1 |  |
| no_rand jpp/50/signed | '8' |  | 0 |  |
| no_part jpp/100/signed | '5' |  | 1 |  |
| no_rand jpp/100/signed | '8' |  | 0 |  |
| no_part jpp/200/signed | '5' |  | 1 |  |
| no_rand jpp/200/signed | '8' |  | 0 |  |
| no_part jpp26_100/75/slice | '5' |  | 1 |  |
| no_rand jpp26_100/75/slice | '5' |  | 1 |  |
| no_part ratoms75/75/scaled | '5' |  | 1 |  |
| no_rand ratoms75/75/scaled | '5' |  | 1 |  |
| no_part ratoms75own/75/own | '5' |  | 1 |  |
| no_rand ratoms75own/75/own | '5' |  | 1 |  |

**recall**: O's answer 5, S's answer 3

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of gamma is 5. The locker of epsilon is 8. James picked⟦ epsilon⟧. The locker of alpha is 6. Emma picked alpha. Fiona picked gamma.
Which position in the Greek alphabet does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' |  | 0 |  |
| whole | '3' |  | 1 | ' 3' |
| no_part jpp/25/signed | '3' |  | 1 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 1 | ' 3' |
| no_part jpp/50/signed | '5' |  | 0 |  |
| no_rand jpp/50/signed | '5' |  | 0 |  |
| no_part jpp/100/signed | '5' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 0 |  |
| no_part jpp/200/signed | '5' |  | 0 |  |
| no_rand jpp/200/signed | '5' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 1 |  |
| no_rand jpp26_100/75/slice | '3' |  | 1 |  |
| no_part ratoms75/75/scaled | '3' |  | 1 |  |
| no_rand ratoms75/75/scaled | '3' |  | 1 |  |
| no_part ratoms75own/75/own | '3' |  | 1 |  |
| no_rand ratoms75own/75/own | '3' |  | 1 |  |

#### P2-L0-0225: bridge rabbit → fly, token 48

**lookup**: O's answer 9, S's answer 3

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the rabbit is 9. The locker of the fly is 3. Liam picked the spider. Lily picked the fly. The locker of the spider is 4. Carl picked the⟦ rabbit⟧.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' |  | 0 |  |
| whole | '3' |  | 1 | ' 3' |
| no_part jpp/25/signed | '3' |  | 1 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 1 | ' 3' |
| no_part jpp/50/signed | '3' |  | 1 |  |
| no_rand jpp/50/signed | '3' |  | 1 |  |
| no_part jpp/100/signed | '3' |  | 1 |  |
| no_rand jpp/100/signed | '9' |  | 0 |  |
| no_part jpp/200/signed | '3' |  | 1 |  |
| no_rand jpp/200/signed | '9' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 1 |  |
| no_rand jpp26_100/75/slice | '3' |  | 1 |  |
| no_part ratoms75/75/scaled | '3' |  | 1 |  |
| no_rand ratoms75/75/scaled | '3' |  | 1 |  |
| no_part ratoms75own/75/own | '3' |  | 1 |  |
| no_rand ratoms75own/75/own | '3' |  | 1 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the rabbit is 9. The locker of the fly is 3. Liam picked the spider. Lily picked the fly. The locker of the spider is 4. Carl picked the⟦ rabbit⟧.
How many legs does Carl's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '6' |  | 1 | ' 6' |
| no_part jpp/25/signed | '6' |  | 1 | ' 6' |
| no_rand jpp/25/signed | '6' |  | 1 | ' 6' |
| no_part jpp/50/signed | '6' |  | 1 |  |
| no_rand jpp/50/signed | '6' |  | 1 |  |
| no_part jpp/100/signed | '6' |  | 1 |  |
| no_rand jpp/100/signed | '4' |  | 0 |  |
| no_part jpp/200/signed | '4' |  | 0 |  |
| no_rand jpp/200/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '6' |  | 1 |  |
| no_rand jpp26_100/75/slice | '6' |  | 1 |  |
| no_part ratoms75/75/scaled | '6' |  | 1 |  |
| no_rand ratoms75/75/scaled | '6' |  | 1 |  |
| no_part ratoms75own/75/own | '6' |  | 1 |  |
| no_rand ratoms75own/75/own | '6' |  | 1 |  |

#### P2-L0-0235: bridge lithium → carbon, token 15

**lookup**: O's answer 2, S's answer 9

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Eve picked carbon. Sam picked⟦ lithium⟧. Noah picked oxygen. The locker of oxygen is 7. The locker of lithium is 2. The locker of carbon is 9.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '2' |  | 0 | ' 2' |
| no_part jpp/25/signed | '2' |  | 0 | ' 2' |
| no_rand jpp/25/signed | '2' |  | 0 | ' 2' |
| no_part jpp/50/signed | '2' |  | 0 |  |
| no_rand jpp/50/signed | '2' |  | 0 |  |
| no_part jpp/100/signed | '2' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp/200/signed | '2' |  | 0 |  |
| no_rand jpp/200/signed | '2' |  | 0 |  |
| no_part jpp26_100/75/slice | '2' |  | 0 |  |
| no_rand jpp26_100/75/slice | '2' |  | 0 |  |
| no_part ratoms75/75/scaled | '2' |  | 0 |  |
| no_rand ratoms75/75/scaled | '2' |  | 0 |  |
| no_part ratoms75own/75/own | '2' |  | 0 |  |
| no_rand ratoms75own/75/own | '2' |  | 0 |  |

**recall**: O's answer 3, S's answer 6

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Eve picked carbon. Sam picked⟦ lithium⟧. Noah picked oxygen. The locker of oxygen is 7. The locker of lithium is 2. The locker of carbon is 9.
What is the atomic number of Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '6' |  | 1 | ' 6' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '6' |  | 1 | ' 6' |
| no_part jpp/50/signed | '3' |  | 0 |  |
| no_rand jpp/50/signed | '6' |  | 1 |  |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp/200/signed | '3' |  | 0 |  |
| no_rand jpp/200/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '6' |  | 1 |  |
| no_rand jpp26_100/75/slice | '6' |  | 1 |  |
| no_part ratoms75/75/scaled | '6' |  | 1 |  |
| no_rand ratoms75/75/scaled | '6' |  | 1 |  |
| no_part ratoms75own/75/own | '6' |  | 1 |  |
| no_rand ratoms75own/75/own | '6' |  | 1 |  |

#### P2-L0-0247: bridge hydrogen → helium, token 21

**lookup**: O's answer 3, S's answer 6

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Finn picked helium. The locker of hydrogen is three. Clara picked⟦ hydrogen⟧. Leo picked carbon. The locker of helium is six. The locker of carbon is two.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '3' |  | 0 | ' 3' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 0 | ' 3' |
| no_part jpp/50/signed | '3' |  | 0 |  |
| no_rand jpp/50/signed | '3' |  | 0 |  |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp/200/signed | '3' |  | 0 |  |
| no_rand jpp/200/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 0 |  |
| no_rand jpp26_100/75/slice | '3' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 0 |  |
| no_rand ratoms75/75/scaled | '3' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 0 |  |

**recall**: O's answer 1, S's answer 2

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Finn picked helium. The locker of hydrogen is three. Clara picked⟦ hydrogen⟧. Leo picked carbon. The locker of helium is six. The locker of carbon is two.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' |  | 0 |  |
| whole | '2' |  | 1 | ' 2' |
| no_part jpp/25/signed | '2' |  | 1 | ' 2' |
| no_rand jpp/25/signed | '2' |  | 1 | ' 2' |
| no_part jpp/50/signed | '1' |  | 0 |  |
| no_rand jpp/50/signed | '2' |  | 1 |  |
| no_part jpp/100/signed | '1' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 1 |  |
| no_part jpp/200/signed | '1' |  | 0 |  |
| no_rand jpp/200/signed | '1' |  | 0 |  |
| no_part jpp26_100/75/slice | '2' |  | 1 |  |
| no_rand jpp26_100/75/slice | '2' |  | 1 |  |
| no_part ratoms75/75/scaled | '2' |  | 1 |  |
| no_rand ratoms75/75/scaled | '2' |  | 1 |  |
| no_part ratoms75own/75/own | '2' |  | 1 |  |
| no_rand ratoms75own/75/own | '2' |  | 1 |  |

#### P2-L0-0274: bridge oxygen → lithium, token 17

**lookup**: O's answer 1, S's answer 7

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of lithium is seven. Julia picked⟦ oxygen⟧. The locker of nitrogen is three. James picked lithium. Carl picked nitrogen. The locker of oxygen is one.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' |  | 0 |  |
| whole | '1' |  | 0 | ' 1' |
| no_part jpp/25/signed | '1' |  | 0 | ' 1' |
| no_rand jpp/25/signed | '1' |  | 0 | ' 1' |
| no_part jpp/50/signed | '1' |  | 0 |  |
| no_rand jpp/50/signed | '1' |  | 0 |  |
| no_part jpp/100/signed | '1' |  | 0 |  |
| no_rand jpp/100/signed | '1' |  | 0 |  |
| no_part jpp/200/signed | '1' |  | 0 |  |
| no_rand jpp/200/signed | '1' |  | 0 |  |
| no_part jpp26_100/75/slice | '1' |  | 0 |  |
| no_rand jpp26_100/75/slice | '1' |  | 0 |  |
| no_part ratoms75/75/scaled | '1' |  | 0 |  |
| no_rand ratoms75/75/scaled | '1' |  | 0 |  |
| no_part ratoms75own/75/own | '1' |  | 0 |  |
| no_rand ratoms75own/75/own | '1' |  | 0 |  |

**recall**: O's answer 8, S's answer 3

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of lithium is seven. Julia picked⟦ oxygen⟧. The locker of nitrogen is three. James picked lithium. Carl picked nitrogen. The locker of oxygen is one.
What is the atomic number of Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '3' |  | 1 | ' 3' |
| no_part jpp/25/signed | '7' |  | 0 | ' 7' |
| no_rand jpp/25/signed | '3' |  | 1 | ' 3' |
| no_part jpp/50/signed | '7' |  | 0 |  |
| no_rand jpp/50/signed | '3' |  | 1 |  |
| no_part jpp/100/signed | '8' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 1 |  |
| no_part jpp/200/signed | '8' |  | 0 |  |
| no_rand jpp/200/signed | '3' |  | 1 |  |
| no_part jpp26_100/75/slice | '3' |  | 1 |  |
| no_rand jpp26_100/75/slice | '3' |  | 1 |  |
| no_part ratoms75/75/scaled | '3' |  | 1 |  |
| no_rand ratoms75/75/scaled | '3' |  | 1 |  |
| no_part ratoms75own/75/own | '3' |  | 1 |  |
| no_rand ratoms75own/75/own | '3' |  | 1 |  |

#### P2-L0-0284: bridge delta → epsilon, token 11

**lookup**: O's answer 7, S's answer 3

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Kyle picked⟦ delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '7' |  | 0 | ' 7' |
| no_part jpp/25/signed | '7' |  | 0 | ' 5' |
| no_rand jpp/25/signed | '7' |  | 0 | ' 7' |
| no_part jpp/50/signed | '7' |  | 0 |  |
| no_rand jpp/50/signed | '7' |  | 0 |  |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '7' |  | 0 |  |
| no_part jpp/200/signed | '7' |  | 0 |  |
| no_rand jpp/200/signed | '7' |  | 0 |  |
| no_part jpp26_100/75/slice | '7' |  | 0 |  |
| no_rand jpp26_100/75/slice | '7' |  | 0 |  |
| no_part ratoms75/75/scaled | '7' |  | 0 |  |
| no_rand ratoms75/75/scaled | '7' |  | 0 |  |
| no_part ratoms75own/75/own | '7' |  | 0 |  |
| no_rand ratoms75own/75/own | '7' |  | 0 |  |

**recall**: O's answer 4, S's answer 5

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Kyle picked⟦ delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '5' |  | 1 | ' 5' |
| no_part jpp/25/signed | '5' |  | 1 | ' 5' |
| no_rand jpp/25/signed | '5' |  | 1 | ' 5' |
| no_part jpp/50/signed | '4' |  | 0 |  |
| no_rand jpp/50/signed | '5' |  | 1 |  |
| no_part jpp/100/signed | '4' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 1 |  |
| no_part jpp/200/signed | '4' |  | 0 |  |
| no_rand jpp/200/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '5' |  | 1 |  |
| no_rand jpp26_100/75/slice | '5' |  | 1 |  |
| no_part ratoms75/75/scaled | '5' |  | 1 |  |
| no_rand ratoms75/75/scaled | '5' |  | 1 |  |
| no_part ratoms75own/75/own | '5' |  | 1 |  |
| no_rand ratoms75own/75/own | '5' |  | 1 |  |

#### P2-L0-0295: bridge helium → hydrogen, token 26

**lookup**: O's answer 5, S's answer 9

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Anna picked lithium. Amy picked hydrogen. The locker of lithium is 1. Tara picked⟦ helium⟧. The locker of helium is 5. The locker of hydrogen is 9.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' |  | 0 |  |
| whole | '5' |  | 0 | ' 5' |
| no_part jpp/25/signed | '5' |  | 0 | ' 5' |
| no_rand jpp/25/signed | '5' |  | 0 | ' 5' |
| no_part jpp/50/signed | '5' |  | 0 |  |
| no_rand jpp/50/signed | '5' |  | 0 |  |
| no_part jpp/100/signed | '5' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 0 |  |
| no_part jpp/200/signed | '5' |  | 0 |  |
| no_rand jpp/200/signed | '5' |  | 0 |  |
| no_part jpp26_100/75/slice | '5' |  | 0 |  |
| no_rand jpp26_100/75/slice | '5' |  | 0 |  |
| no_part ratoms75/75/scaled | '5' |  | 0 |  |
| no_rand ratoms75/75/scaled | '5' |  | 0 |  |
| no_part ratoms75own/75/own | '5' |  | 0 |  |
| no_rand ratoms75own/75/own | '5' |  | 0 |  |

**recall**: O's answer 2, S's answer 1

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Anna picked lithium. Amy picked hydrogen. The locker of lithium is 1. Tara picked⟦ helium⟧. The locker of helium is 5. The locker of hydrogen is 9.
What is the atomic number of Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '1' |  | 1 | ' 1' |
| no_part jpp/25/signed | '1' |  | 1 | ' 1' |
| no_rand jpp/25/signed | '1' |  | 1 | ' 1' |
| no_part jpp/50/signed | '1' |  | 1 |  |
| no_rand jpp/50/signed | '1' |  | 1 |  |
| no_part jpp/100/signed | '5' |  | 0 |  |
| no_rand jpp/100/signed | '1' |  | 1 |  |
| no_part jpp/200/signed | '2' |  | 0 |  |
| no_rand jpp/200/signed | '5' |  | 0 |  |
| no_part jpp26_100/75/slice | '1' |  | 1 |  |
| no_rand jpp26_100/75/slice | '1' |  | 1 |  |
| no_part ratoms75/75/scaled | '1' |  | 1 |  |
| no_rand ratoms75/75/scaled | '1' |  | 1 |  |
| no_part ratoms75own/75/own | '1' |  | 1 |  |
| no_rand ratoms75own/75/own | '1' |  | 1 |  |

#### P2-L0-0443: bridge delta → epsilon, token 32

**lookup**: O's answer 6, S's answer 2

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of iota is 7. The locker of delta is 6. Ella picked iota. Leo picked⟦ delta⟧. Sean picked epsilon. The locker of epsilon is 2.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '2' |  | 1 | ' 2' |
| no_part jpp/25/signed | '2' |  | 1 | ' 2' |
| no_rand jpp/25/signed | '2' |  | 1 | ' 2' |
| no_part jpp/50/signed | '6' |  | 0 |  |
| no_rand jpp/50/signed | '2' |  | 1 |  |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 0 |  |
| no_part jpp/200/signed | '6' |  | 0 |  |
| no_rand jpp/200/signed | '6' |  | 0 |  |
| no_part jpp26_100/75/slice | '2' |  | 1 |  |
| no_rand jpp26_100/75/slice | '2' |  | 1 |  |
| no_part ratoms75/75/scaled | '2' |  | 1 |  |
| no_rand ratoms75/75/scaled | '2' |  | 1 |  |
| no_part ratoms75own/75/own | '2' |  | 1 |  |
| no_rand ratoms75own/75/own | '2' |  | 1 |  |

**recall**: O's answer 4, S's answer 5

O, as read:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of iota is 7. The locker of delta is 6. Ella picked iota. Leo picked⟦ delta⟧. Sean picked epsilon. The locker of epsilon is 2.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '5' |  | 1 | ' 5' |
| no_part jpp/25/signed | '5' |  | 1 | ' 5' |
| no_rand jpp/25/signed | '5' |  | 1 | ' 5' |
| no_part jpp/50/signed | '4' |  | 0 |  |
| no_rand jpp/50/signed | '5' |  | 1 |  |
| no_part jpp/100/signed | '4' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 1 |  |
| no_part jpp/200/signed | '4' |  | 0 |  |
| no_rand jpp/200/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '5' |  | 1 |  |
| no_rand jpp26_100/75/slice | '5' |  | 1 |  |
| no_part ratoms75/75/scaled | '5' |  | 1 |  |
| no_rand ratoms75/75/scaled | '5' |  | 1 |  |
| no_part ratoms75own/75/own | '5' |  | 1 |  |
| no_rand ratoms75own/75/own | '5' |  | 1 |  |

