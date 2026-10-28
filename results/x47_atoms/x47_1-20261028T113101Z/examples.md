# 47.1 verify pack: prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the bridge word, where the change (or the arm's part of it) is added at L. UNVERIFIED.

## qwen3.6-27b

### routes test, another item moved (C2): x6_routes_x47_1_27b, 10 random items of 300 (seed 0)

#### C2-0028: bridge fly → duck, token 38; expected digits {'identity': 6, 'position': 4, 'value': 5, 'original': 3}

**lookup**: O's answer 3, S's answer 5

O, as read:

```
<|im_start|>user
The locker of the fly is 3. The locker of the duck is 6. The locker of the bee is 4. Lucy picked the duck. Sam picked the⟦ fly⟧. Liam picked the bee.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' | original | 0 |  |
| whole | '6' | identity | 0 |  |
| no_jpp | '6' | identity | 0 |  |
| no_jpp_rand | '6' | identity | 0 |  |
| no_alf | '6' | identity | 0 |  |
| no_alf_rand | '6' | identity | 0 |  |
| no_jpp100 | '6' | identity | 0 |  |
| no_jpp100_rand | '6' | identity | 0 |  |
| no_jpp26_100 | '6' | identity | 0 |  |
| no_jpp26_100_rand | '6' | identity | 0 |  |
| no_ratoms75 | '6' | identity | 0 |  |
| no_ratoms75_rand | '6' | identity | 0 |  |
| no_ratoms75own | '6' | identity | 0 |  |
| no_ratoms75own_rand | '6' | identity | 0 |  |

**recall**: O's answer 6, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the fly is 3. The locker of the duck is 6. The locker of the bee is 4. Lucy picked the duck. Sam picked the⟦ fly⟧. Liam picked the bee.
How many legs does Sam's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '6' |  | 0 |  |
| no_jpp | '6' |  | 0 |  |
| no_jpp_rand | '6' |  | 0 |  |
| no_alf | '6' |  | 0 |  |
| no_alf_rand | '6' |  | 0 |  |
| no_jpp100 | '6' |  | 0 |  |
| no_jpp100_rand | '6' |  | 0 |  |
| no_jpp26_100 | '6' |  | 0 |  |
| no_jpp26_100_rand | '6' |  | 0 |  |
| no_ratoms75 | '6' |  | 0 |  |
| no_ratoms75_rand | '6' |  | 0 |  |
| no_ratoms75own | '6' |  | 0 |  |
| no_ratoms75own_rand | '6' |  | 0 |  |

#### C2-0199: bridge tick → bee, token 43; expected digits {'identity': 6, 'position': 9, 'value': 1, 'original': 7}

**lookup**: O's answer 7, S's answer 1

O, as read:

```
<|im_start|>user
The locker of the tick is 7. The locker of the fly is 9. The locker of the bee is 6. Vera picked the bee. James picked the fly. Owen picked the⟦ tick⟧.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' | original | 0 |  |
| whole | '6' | identity | 0 |  |
| no_jpp | '7' | original | 0 |  |
| no_jpp_rand | '6' | identity | 0 |  |
| no_alf | '6' | identity | 0 |  |
| no_alf_rand | '6' | identity | 0 |  |
| no_jpp100 | '7' | original | 0 |  |
| no_jpp100_rand | '6' | identity | 0 |  |
| no_jpp26_100 | '6' | identity | 0 |  |
| no_jpp26_100_rand | '6' | identity | 0 |  |
| no_ratoms75 | '6' | identity | 0 |  |
| no_ratoms75_rand | '6' | identity | 0 |  |
| no_ratoms75own | '6' | identity | 0 |  |
| no_ratoms75own_rand | '6' | identity | 0 |  |

**recall**: O's answer 8, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the tick is 7. The locker of the fly is 9. The locker of the bee is 6. Vera picked the bee. James picked the fly. Owen picked the⟦ tick⟧.
How many legs does Owen's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '6' |  | 1 |  |
| no_jpp | '8' |  | 0 |  |
| no_jpp_rand | '6' |  | 1 |  |
| no_alf | '8' |  | 0 |  |
| no_alf_rand | '6' |  | 1 |  |
| no_jpp100 | '8' |  | 0 |  |
| no_jpp100_rand | '6' |  | 1 |  |
| no_jpp26_100 | '8' |  | 0 |  |
| no_jpp26_100_rand | '6' |  | 1 |  |
| no_ratoms75 | '6' |  | 1 |  |
| no_ratoms75_rand | '6' |  | 1 |  |
| no_ratoms75own | '6' |  | 1 |  |
| no_ratoms75own_rand | '6' |  | 1 |  |

#### C2-0231: bridge pig → butterfly, token 38; expected digits {'identity': 7, 'position': 3, 'value': 9, 'original': 1}

**lookup**: O's answer 1, S's answer 9

O, as read:

```
<|im_start|>user
The locker of the butterfly is 7. The locker of the pig is 1. The locker of the beetle is 3. Paul picked the butterfly. Vera picked the⟦ pig⟧. Mark picked the beetle.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' | original | 0 |  |
| whole | '7' | identity | 0 |  |
| no_jpp | '7' | identity | 0 |  |
| no_jpp_rand | '7' | identity | 0 |  |
| no_alf | '7' | identity | 0 |  |
| no_alf_rand | '7' | identity | 0 |  |
| no_jpp100 | '1' | original | 0 |  |
| no_jpp100_rand | '7' | identity | 0 |  |
| no_jpp26_100 | '7' | identity | 0 |  |
| no_jpp26_100_rand | '7' | identity | 0 |  |
| no_ratoms75 | '7' | identity | 0 |  |
| no_ratoms75_rand | '7' | identity | 0 |  |
| no_ratoms75own | '7' | identity | 0 |  |
| no_ratoms75own_rand | '7' | identity | 0 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the butterfly is 7. The locker of the pig is 1. The locker of the beetle is 3. Paul picked the butterfly. Vera picked the⟦ pig⟧. Mark picked the beetle.
How many legs does Vera's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '4' |  | 0 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '4' |  | 0 |  |
| no_alf | '4' |  | 0 |  |
| no_alf_rand | '4' |  | 0 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '4' |  | 0 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '4' |  | 0 |  |
| no_ratoms75 | '4' |  | 0 |  |
| no_ratoms75_rand | '4' |  | 0 |  |
| no_ratoms75own | '4' |  | 0 |  |
| no_ratoms75own_rand | '4' |  | 0 |  |

#### C2-0271: bridge pig → chicken, token 33; expected digits {'identity': 1, 'position': 6, 'value': 7, 'original': 4}

**lookup**: O's answer 4, S's answer 7

O, as read:

```
<|im_start|>user
The locker of the pig is 4. The locker of the bear is 6. The locker of the chicken is 1. Beth picked the⟦ pig⟧. David picked the bear. Oscar picked the chicken.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '1' | identity | 0 |  |
| no_jpp | '1' | identity | 0 |  |
| no_jpp_rand | '1' | identity | 0 |  |
| no_alf | '4' | original | 0 |  |
| no_alf_rand | '1' | identity | 0 |  |
| no_jpp100 | '1' | identity | 0 |  |
| no_jpp100_rand | '1' | identity | 0 |  |
| no_jpp26_100 | '1' | identity | 0 |  |
| no_jpp26_100_rand | '1' | identity | 0 |  |
| no_ratoms75 | '1' | identity | 0 |  |
| no_ratoms75_rand | '1' | identity | 0 |  |
| no_ratoms75own | '1' | identity | 0 |  |
| no_ratoms75own_rand | '1' | identity | 0 |  |

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the pig is 4. The locker of the bear is 6. The locker of the chicken is 1. Beth picked the⟦ pig⟧. David picked the bear. Oscar picked the chicken.
How many legs does Beth's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '2' |  | 1 |  |
| no_jpp | '2' |  | 1 |  |
| no_jpp_rand | '2' |  | 1 |  |
| no_alf | '2' |  | 1 |  |
| no_alf_rand | '2' |  | 1 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '2' |  | 1 |  |
| no_jpp26_100 | '2' |  | 1 |  |
| no_jpp26_100_rand | '2' |  | 1 |  |
| no_ratoms75 | '2' |  | 1 |  |
| no_ratoms75_rand | '2' |  | 1 |  |
| no_ratoms75own | '2' |  | 1 |  |
| no_ratoms75own_rand | '2' |  | 1 |  |

#### C2-0293: bridge mouse → fly, token 43; expected digits {'identity': 1, 'position': 4, 'value': 5, 'original': 6}

**lookup**: O's answer 6, S's answer 5

O, as read:

```
<|im_start|>user
The locker of the butterfly is 4. The locker of the fly is 1. The locker of the mouse is 6. Mark picked the butterfly. Anna picked the fly. Noah picked the⟦ mouse⟧.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' | original | 0 |  |
| whole | '1' | identity | 0 |  |
| no_jpp | '4' | position | 0 |  |
| no_jpp_rand | '1' | identity | 0 |  |
| no_alf | '1' | identity | 0 |  |
| no_alf_rand | '1' | identity | 0 |  |
| no_jpp100 | '6' | original | 0 |  |
| no_jpp100_rand | '1' | identity | 0 |  |
| no_jpp26_100 | '1' | identity | 0 |  |
| no_jpp26_100_rand | '1' | identity | 0 |  |
| no_ratoms75 | '1' | identity | 0 |  |
| no_ratoms75_rand | '1' | identity | 0 |  |
| no_ratoms75own | '1' | identity | 0 |  |
| no_ratoms75own_rand | '1' | identity | 0 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the butterfly is 4. The locker of the fly is 1. The locker of the mouse is 6. Mark picked the butterfly. Anna picked the fly. Noah picked the⟦ mouse⟧.
How many legs does Noah's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '6' |  | 1 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '6' |  | 1 |  |
| no_alf | '6' |  | 1 |  |
| no_alf_rand | '6' |  | 1 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '6' |  | 1 |  |
| no_jpp26_100 | '6' |  | 1 |  |
| no_jpp26_100_rand | '6' |  | 1 |  |
| no_ratoms75 | '6' |  | 1 |  |
| no_ratoms75_rand | '6' |  | 1 |  |
| no_ratoms75own | '6' |  | 1 |  |
| no_ratoms75own_rand | '6' |  | 1 |  |

#### C2-0311: bridge chicken → butterfly, token 33; expected digits {'identity': 6, 'position': 5, 'value': 9, 'original': 3}

**lookup**: O's answer 3, S's answer 9

O, as read:

```
<|im_start|>user
The locker of the chicken is 3. The locker of the camel is 5. The locker of the butterfly is 6. Will picked the⟦ chicken⟧. Zoe picked the camel. Noah picked the butterfly.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' | original | 0 |  |
| whole | '6' | identity | 0 |  |
| no_jpp | '6' | identity | 0 |  |
| no_jpp_rand | '6' | identity | 0 |  |
| no_alf | '6' | identity | 0 |  |
| no_alf_rand | '6' | identity | 0 |  |
| no_jpp100 | '3' | original | 0 |  |
| no_jpp100_rand | '6' | identity | 0 |  |
| no_jpp26_100 | '6' | identity | 0 |  |
| no_jpp26_100_rand | '6' | identity | 0 |  |
| no_ratoms75 | '6' | identity | 0 |  |
| no_ratoms75_rand | '6' | identity | 0 |  |
| no_ratoms75own | '6' | identity | 0 |  |
| no_ratoms75own_rand | '6' | identity | 0 |  |

**recall**: O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the chicken is 3. The locker of the camel is 5. The locker of the butterfly is 6. Will picked the⟦ chicken⟧. Zoe picked the camel. Noah picked the butterfly.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '6' |  | 1 |  |
| no_jpp | '2' |  | 0 |  |
| no_jpp_rand | '2' |  | 0 |  |
| no_alf | '2' |  | 0 |  |
| no_alf_rand | '2' |  | 0 |  |
| no_jpp100 | '2' |  | 0 |  |
| no_jpp100_rand | '2' |  | 0 |  |
| no_jpp26_100 | '2' |  | 0 |  |
| no_jpp26_100_rand | '2' |  | 0 |  |
| no_ratoms75 | '2' |  | 0 |  |
| no_ratoms75_rand | '2' |  | 0 |  |
| no_ratoms75own | '6' |  | 1 |  |
| no_ratoms75own_rand | '2' |  | 0 |  |

#### C2-0324: bridge crow → camel, token 38; expected digits {'identity': 1, 'position': 2, 'value': 3, 'original': 8}

**lookup**: O's answer 8, S's answer 3

O, as read:

```
<|im_start|>user
The locker of the crow is 8. The locker of the camel is 1. The locker of the wolf is 2. Laura picked the camel. Vera picked the⟦ crow⟧. Eve picked the wolf.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' | original | 0 |  |
| whole | '1' | identity | 0 |  |
| no_jpp | '1' | identity | 0 |  |
| no_jpp_rand | '1' | identity | 0 |  |
| no_alf | '8' | original | 0 |  |
| no_alf_rand | '1' | identity | 0 |  |
| no_jpp100 | '1' | identity | 0 |  |
| no_jpp100_rand | '1' | identity | 0 |  |
| no_jpp26_100 | '1' | identity | 0 |  |
| no_jpp26_100_rand | '1' | identity | 0 |  |
| no_ratoms75 | '1' | identity | 0 |  |
| no_ratoms75_rand | '1' | identity | 0 |  |
| no_ratoms75own | '1' | identity | 0 |  |
| no_ratoms75own_rand | '1' | identity | 0 |  |

**recall**: O's answer 2, S's answer 4

O, as read:

```
<|im_start|>user
The locker of the crow is 8. The locker of the camel is 1. The locker of the wolf is 2. Laura picked the camel. Vera picked the⟦ crow⟧. Eve picked the wolf.
How many legs does Vera's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '2' |  | 0 |  |
| no_jpp | '2' |  | 0 |  |
| no_jpp_rand | '2' |  | 0 |  |
| no_alf | '2' |  | 0 |  |
| no_alf_rand | '2' |  | 0 |  |
| no_jpp100 | '2' |  | 0 |  |
| no_jpp100_rand | '2' |  | 0 |  |
| no_jpp26_100 | '2' |  | 0 |  |
| no_jpp26_100_rand | '2' |  | 0 |  |
| no_ratoms75 | '2' |  | 0 |  |
| no_ratoms75_rand | '2' |  | 0 |  |
| no_ratoms75own | '2' |  | 0 |  |
| no_ratoms75own_rand | '2' |  | 0 |  |

#### C2-0369: bridge goat → ant, token 33; expected digits {'identity': 5, 'position': 7, 'value': 2, 'original': 4}

**lookup**: O's answer 4, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the goat is 4. The locker of the ant is 5. The locker of the sheep is 7. Emma picked the⟦ goat⟧. Fiona picked the ant. Victor picked the sheep.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '5' | identity | 0 |  |
| no_jpp | '7' | position | 0 |  |
| no_jpp_rand | '5' | identity | 0 |  |
| no_alf | '4' | original | 0 |  |
| no_alf_rand | '5' | identity | 0 |  |
| no_jpp100 | '4' | original | 0 |  |
| no_jpp100_rand | '5' | identity | 0 |  |
| no_jpp26_100 | '5' | identity | 0 |  |
| no_jpp26_100_rand | '5' | identity | 0 |  |
| no_ratoms75 | '5' | identity | 0 |  |
| no_ratoms75_rand | '5' | identity | 0 |  |
| no_ratoms75own | '5' | identity | 0 |  |
| no_ratoms75own_rand | '5' | identity | 0 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the goat is 4. The locker of the ant is 5. The locker of the sheep is 7. Emma picked the⟦ goat⟧. Fiona picked the ant. Victor picked the sheep.
How many legs does Emma's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '4' |  | 0 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '4' |  | 0 |  |
| no_alf | '4' |  | 0 |  |
| no_alf_rand | '4' |  | 0 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '4' |  | 0 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '4' |  | 0 |  |
| no_ratoms75 | '4' |  | 0 |  |
| no_ratoms75_rand | '4' |  | 0 |  |
| no_ratoms75own | '4' |  | 0 |  |
| no_ratoms75own_rand | '4' |  | 0 |  |

#### C2-0373: bridge fly → goose, token 33; expected digits {'identity': 9, 'position': 6, 'value': 3, 'original': 1}

**lookup**: O's answer 1, S's answer 3

O, as read:

```
<|im_start|>user
The locker of the tick is 6. The locker of the fly is 1. The locker of the goose is 9. Kyle picked the⟦ fly⟧. Mark picked the goose. Clara picked the tick.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' | original | 0 |  |
| whole | '6' | position | 0 |  |
| no_jpp | '6' | position | 0 |  |
| no_jpp_rand | '6' | position | 0 |  |
| no_alf | '9' | identity | 0 |  |
| no_alf_rand | '6' | position | 0 |  |
| no_jpp100 | '6' | position | 0 |  |
| no_jpp100_rand | '6' | position | 0 |  |
| no_jpp26_100 | '6' | position | 0 |  |
| no_jpp26_100_rand | '6' | position | 0 |  |
| no_ratoms75 | '6' | position | 0 |  |
| no_ratoms75_rand | '6' | position | 0 |  |
| no_ratoms75own | '6' | position | 0 |  |
| no_ratoms75own_rand | '6' | position | 0 |  |

**recall**: O's answer 6, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the tick is 6. The locker of the fly is 1. The locker of the goose is 9. Kyle picked the⟦ fly⟧. Mark picked the goose. Clara picked the tick.
How many legs does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '8' |  | 0 |  |
| no_jpp | '6' |  | 0 |  |
| no_jpp_rand | '8' |  | 0 |  |
| no_alf | '6' |  | 0 |  |
| no_alf_rand | '8' |  | 0 |  |
| no_jpp100 | '6' |  | 0 |  |
| no_jpp100_rand | '6' |  | 0 |  |
| no_jpp26_100 | '8' |  | 0 |  |
| no_jpp26_100_rand | '8' |  | 0 |  |
| no_ratoms75 | '8' |  | 0 |  |
| no_ratoms75_rand | '8' |  | 0 |  |
| no_ratoms75own | '8' |  | 0 |  |
| no_ratoms75own_rand | '8' |  | 0 |  |

#### C2-0390: bridge owl → bee, token 38; expected digits {'identity': 9, 'position': 8, 'value': 7, 'original': 4}

**lookup**: O's answer 4, S's answer 7

O, as read:

```
<|im_start|>user
The locker of the bee is 9. The locker of the owl is 4. The locker of the mouse is 8. Mark picked the bee. Zoe picked the⟦ owl⟧. Peter picked the mouse.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '9' | identity | 0 |  |
| no_jpp | '9' | identity | 0 |  |
| no_jpp_rand | '9' | identity | 0 |  |
| no_alf | '4' | original | 0 |  |
| no_alf_rand | '9' | identity | 0 |  |
| no_jpp100 | '4' | original | 0 |  |
| no_jpp100_rand | '9' | identity | 0 |  |
| no_jpp26_100 | '9' | identity | 0 |  |
| no_jpp26_100_rand | '9' | identity | 0 |  |
| no_ratoms75 | '9' | identity | 0 |  |
| no_ratoms75_rand | '9' | identity | 0 |  |
| no_ratoms75own | '9' | identity | 0 |  |
| no_ratoms75own_rand | '9' | identity | 0 |  |

**recall**: O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the bee is 9. The locker of the owl is 4. The locker of the mouse is 8. Mark picked the bee. Zoe picked the⟦ owl⟧. Peter picked the mouse.
How many legs does Zoe's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '2' |  | 0 |  |
| no_jpp | '2' |  | 0 |  |
| no_jpp_rand | '2' |  | 0 |  |
| no_alf | '2' |  | 0 |  |
| no_alf_rand | '2' |  | 0 |  |
| no_jpp100 | '2' |  | 0 |  |
| no_jpp100_rand | '2' |  | 0 |  |
| no_jpp26_100 | '2' |  | 0 |  |
| no_jpp26_100_rand | '2' |  | 0 |  |
| no_ratoms75 | '2' |  | 0 |  |
| no_ratoms75_rand | '2' |  | 0 |  |
| no_ratoms75own | '2' |  | 0 |  |
| no_ratoms75own_rand | '2' |  | 0 |  |

### main test (two people swap picks): x47_1_main_27b, 10 random items of 200 (seed 0)

#### P2-L0-0010: bridge oxygen → carbon, token 17

**lookup**: O's answer 3, S's answer 7

O, as read:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦ oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '3' |  | 0 | ' 3' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 0 | ' 3' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 0 |  |
| no_rand jpp26_100/75/slice | '3' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 0 |  |
| no_rand ratoms75/75/scaled | '3' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 0 |  |

**recall**: O's answer 8, S's answer 6

O, as read:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦ oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '6' |  | 1 | ' 6' |
| no_part jpp/25/signed | '8' |  | 0 | ' 8' |
| no_rand jpp/25/signed | '6' |  | 1 | ' 6' |
| no_part jpp/100/signed | '8' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 1 |  |
| no_part jpp26_100/75/slice | '6' |  | 1 |  |
| no_rand jpp26_100/75/slice | '6' |  | 1 |  |
| no_part ratoms75/75/scaled | '6' |  | 1 |  |
| no_rand ratoms75/75/scaled | '6' |  | 1 |  |
| no_part ratoms75own/75/own | '6' |  | 1 |  |
| no_rand ratoms75own/75/own | '6' |  | 1 |  |

#### P2-L0-0069: bridge sheep → butterfly, token 38

**lookup**: O's answer 3, S's answer 7

O, as read:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ sheep⟧. Ella picked the butterfly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '7' |  | 1 | ' 7' |
| no_part jpp/25/signed | '7' |  | 1 | ' 7' |
| no_rand jpp/25/signed | '7' |  | 1 | ' 7' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '7' |  | 1 |  |
| no_part jpp26_100/75/slice | '7' |  | 1 |  |
| no_rand jpp26_100/75/slice | '7' |  | 1 |  |
| no_part ratoms75/75/scaled | '7' |  | 1 |  |
| no_rand ratoms75/75/scaled | '7' |  | 1 |  |
| no_part ratoms75own/75/own | '7' |  | 1 |  |
| no_rand ratoms75own/75/own | '7' |  | 1 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦ sheep⟧. Ella picked the butterfly.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '6' |  | 1 | ' 6' |
| no_part jpp/25/signed | '4' |  | 0 | ' 4' |
| no_rand jpp/25/signed | '6' |  | 1 | ' 6' |
| no_part jpp/100/signed | '4' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '6' |  | 1 |  |
| no_rand jpp26_100/75/slice | '6' |  | 1 |  |
| no_part ratoms75/75/scaled | '6' |  | 1 |  |
| no_rand ratoms75/75/scaled | '6' |  | 1 |  |
| no_part ratoms75own/75/own | '6' |  | 1 |  |
| no_rand ratoms75own/75/own | '6' |  | 1 |  |

#### P2-L0-0080: bridge eta → delta, token 13

**lookup**: O's answer 6, S's answer 8

O, as read:

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. Ivy picked⟦ eta⟧. The locker of delta is 8. The locker of eta is 6. The locker of epsilon is 1.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '6' |  | 0 | ' 6' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '6' |  | 0 | ' 6' |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 0 |  |
| no_part jpp26_100/75/slice | '6' |  | 0 |  |
| no_rand jpp26_100/75/slice | '6' |  | 0 |  |
| no_part ratoms75/75/scaled | '6' |  | 0 |  |
| no_rand ratoms75/75/scaled | '6' |  | 0 |  |
| no_part ratoms75own/75/own | '6' |  | 0 |  |
| no_rand ratoms75own/75/own | '6' |  | 0 |  |

**recall**: O's answer 7, S's answer 4

O, as read:

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. Ivy picked⟦ eta⟧. The locker of delta is 8. The locker of eta is 6. The locker of epsilon is 1.
Which position in the Greek alphabet does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '4' |  | 1 | ' 4' |
| no_part jpp/25/signed | '7' |  | 0 | ' 7' |
| no_rand jpp/25/signed | '4' |  | 1 | ' 4' |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 1 |  |
| no_part jpp26_100/75/slice | '4' |  | 1 |  |
| no_rand jpp26_100/75/slice | '4' |  | 1 |  |
| no_part ratoms75/75/scaled | '4' |  | 1 |  |
| no_rand ratoms75/75/scaled | '4' |  | 1 |  |
| no_part ratoms75own/75/own | '4' |  | 1 |  |
| no_rand ratoms75own/75/own | '4' |  | 1 |  |

#### P2-L0-0102: bridge butterfly → goose, token 12

**lookup**: O's answer 5, S's answer 8

O, as read:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦ butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' |  | 0 |  |
| whole | '5' |  | 0 | ' 5' |
| no_part jpp/25/signed | '5' |  | 0 | ' 5' |
| no_rand jpp/25/signed | '5' |  | 0 | ' 5' |
| no_part jpp/100/signed | '5' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 0 |  |
| no_part jpp26_100/75/slice | '5' |  | 0 |  |
| no_rand jpp26_100/75/slice | '5' |  | 0 |  |
| no_part ratoms75/75/scaled | '5' |  | 0 |  |
| no_rand ratoms75/75/scaled | '5' |  | 0 |  |
| no_part ratoms75own/75/own | '5' |  | 0 |  |
| no_rand ratoms75own/75/own | '5' |  | 0 |  |

**recall**: O's answer 6, S's answer 2

O, as read:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦ butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '2' |  | 1 | ' 2' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '2' |  | 1 | ' 2' |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 0 |  |
| no_part jpp26_100/75/slice | '2' |  | 1 |  |
| no_rand jpp26_100/75/slice | '2' |  | 1 |  |
| no_part ratoms75/75/scaled | '2' |  | 1 |  |
| no_rand ratoms75/75/scaled | '2' |  | 1 |  |
| no_part ratoms75own/75/own | '2' |  | 1 |  |
| no_rand ratoms75own/75/own | '2' |  | 1 |  |

#### P2-L0-0107: bridge iota → gamma, token 16

**lookup**: O's answer 3, S's answer 9

O, as read:

```
<|im_start|>user
The locker of gamma is nine. Eva picked epsilon. David picked⟦ iota⟧. The locker of epsilon is one. The locker of iota is three. Eve picked gamma.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '9' |  | 1 | ' 9' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '9' |  | 1 | ' 9' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '9' |  | 1 |  |
| no_rand jpp26_100/75/slice | '9' |  | 1 |  |
| no_part ratoms75/75/scaled | '9' |  | 1 |  |
| no_rand ratoms75/75/scaled | '9' |  | 1 |  |
| no_part ratoms75own/75/own | '9' |  | 1 |  |
| no_rand ratoms75own/75/own | '9' |  | 1 |  |

**recall**: O's answer 9, S's answer 3

O, as read:

```
<|im_start|>user
The locker of gamma is nine. Eva picked epsilon. David picked⟦ iota⟧. The locker of epsilon is one. The locker of iota is three. Eve picked gamma.
Which position in the Greek alphabet does David's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' |  | 0 |  |
| whole | '9' |  | 0 | ' 9' |
| no_part jpp/25/signed | '9' |  | 0 | ' 9' |
| no_rand jpp/25/signed | '3' |  | 1 | ' 3' |
| no_part jpp/100/signed | '9' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 1 |  |
| no_part jpp26_100/75/slice | '3' |  | 1 |  |
| no_rand jpp26_100/75/slice | '3' |  | 1 |  |
| no_part ratoms75/75/scaled | '3' |  | 1 |  |
| no_rand ratoms75/75/scaled | '3' |  | 1 |  |
| no_part ratoms75own/75/own | '9' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 1 |  |

#### P2-L0-0111: bridge chicken → rabbit, token 7

**lookup**: O's answer 8, S's answer 7

O, as read:

```
<|im_start|>user
Ivy picked the⟦ chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '8' |  | 0 | ' 8' |
| no_part jpp/25/signed | '8' |  | 0 | ' 8' |
| no_rand jpp/25/signed | '8' |  | 0 | ' 8' |
| no_part jpp/100/signed | '8' |  | 0 |  |
| no_rand jpp/100/signed | '8' |  | 0 |  |
| no_part jpp26_100/75/slice | '8' |  | 0 |  |
| no_rand jpp26_100/75/slice | '8' |  | 0 |  |
| no_part ratoms75/75/scaled | '8' |  | 0 |  |
| no_rand ratoms75/75/scaled | '8' |  | 0 |  |
| no_part ratoms75own/75/own | '8' |  | 0 |  |
| no_rand ratoms75own/75/own | '8' |  | 0 |  |

**recall**: O's answer 2, S's answer 4

O, as read:

```
<|im_start|>user
Ivy picked the⟦ chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '4' |  | 1 | ' 4' |
| no_part jpp/25/signed | '2' |  | 0 | ' 2' |
| no_rand jpp/25/signed | '4' |  | 1 | ' 4' |
| no_part jpp/100/signed | '2' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp26_100/75/slice | '4' |  | 1 |  |
| no_rand jpp26_100/75/slice | '4' |  | 1 |  |
| no_part ratoms75/75/scaled | '4' |  | 1 |  |
| no_rand ratoms75/75/scaled | '4' |  | 1 |  |
| no_part ratoms75own/75/own | '4' |  | 1 |  |
| no_rand ratoms75own/75/own | '4' |  | 1 |  |

#### P2-L0-0128: bridge eta → theta, token 17

**lookup**: O's answer 2, S's answer 7

O, as read:

```
<|im_start|>user
The locker of theta is 7. Adam picked beta. Henry picked⟦ eta⟧. Liam picked theta. The locker of beta is 9. The locker of eta is 2.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '7' |  | 1 | ' 7' |
| no_part jpp/25/signed | '7' |  | 1 | ' 7' |
| no_rand jpp/25/signed | '7' |  | 1 | ' 7' |
| no_part jpp/100/signed | '2' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp26_100/75/slice | '7' |  | 1 |  |
| no_rand jpp26_100/75/slice | '7' |  | 1 |  |
| no_part ratoms75/75/scaled | '7' |  | 1 |  |
| no_rand ratoms75/75/scaled | '7' |  | 1 |  |
| no_part ratoms75own/75/own | '7' |  | 1 |  |
| no_rand ratoms75own/75/own | '7' |  | 1 |  |

**recall**: O's answer 7, S's answer 8

O, as read:

```
<|im_start|>user
The locker of theta is 7. Adam picked beta. Henry picked⟦ eta⟧. Liam picked theta. The locker of beta is 9. The locker of eta is 2.
Which position in the Greek alphabet does Henry's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '5' |  | 0 | ' 5' |
| no_part jpp/25/signed | '5' |  | 0 | ' 5' |
| no_rand jpp/25/signed | '5' |  | 0 | ' 5' |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '9' |  | 0 |  |
| no_part jpp26_100/75/slice | '5' |  | 0 |  |
| no_rand jpp26_100/75/slice | '5' |  | 0 |  |
| no_part ratoms75/75/scaled | '5' |  | 0 |  |
| no_rand ratoms75/75/scaled | '5' |  | 0 |  |
| no_part ratoms75own/75/own | '5' |  | 0 |  |
| no_rand ratoms75own/75/own | '5' |  | 0 |  |

#### P2-L0-0130: bridge carbon → lithium, token 5

**lookup**: O's answer 4, S's answer 7

O, as read:

```
<|im_start|>user
Alice picked⟦ carbon⟧. The locker of hydrogen is 9. Frank picked lithium. The locker of carbon is 4. The locker of lithium is 7. Dan picked hydrogen.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '4' |  | 0 | ' 4' |
| no_part jpp/25/signed | '4' |  | 0 | ' 4' |
| no_rand jpp/25/signed | '4' |  | 0 | ' 4' |
| no_part jpp/100/signed | '4' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '4' |  | 0 |  |
| no_rand jpp26_100/75/slice | '4' |  | 0 |  |
| no_part ratoms75/75/scaled | '4' |  | 0 |  |
| no_rand ratoms75/75/scaled | '4' |  | 0 |  |
| no_part ratoms75own/75/own | '4' |  | 0 |  |
| no_rand ratoms75own/75/own | '4' |  | 0 |  |

**recall**: O's answer 6, S's answer 3

O, as read:

```
<|im_start|>user
Alice picked⟦ carbon⟧. The locker of hydrogen is 9. Frank picked lithium. The locker of carbon is 4. The locker of lithium is 7. Dan picked hydrogen.
What is the atomic number of Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '3' |  | 1 | ' 3' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '3' |  | 1 | ' 3' |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 1 |  |
| no_rand jpp26_100/75/slice | '3' |  | 1 |  |
| no_part ratoms75/75/scaled | '3' |  | 1 |  |
| no_rand ratoms75/75/scaled | '3' |  | 1 |  |
| no_part ratoms75own/75/own | '3' |  | 1 |  |
| no_rand ratoms75own/75/own | '3' |  | 1 |  |

#### P2-L0-0136: bridge hydrogen → oxygen, token 6

**lookup**: O's answer 3, S's answer 6

O, as read:

```
<|im_start|>user
Mia picked⟦ hydrogen⟧. The locker of hydrogen is three. The locker of oxygen is six. Amy picked oxygen. The locker of nitrogen is eight. Jack picked nitrogen.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '3' |  | 0 | ' 3' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 0 | ' 3' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 0 |  |
| no_rand jpp26_100/75/slice | '3' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 0 |  |
| no_rand ratoms75/75/scaled | '3' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 0 |  |

**recall**: O's answer 1, S's answer 8

O, as read:

```
<|im_start|>user
Mia picked⟦ hydrogen⟧. The locker of hydrogen is three. The locker of oxygen is six. Amy picked oxygen. The locker of nitrogen is eight. Jack picked nitrogen.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' |  | 0 |  |
| whole | '8' |  | 1 | ' 8' |
| no_part jpp/25/signed | '1' |  | 0 | ' 1' |
| no_rand jpp/25/signed | '8' |  | 1 | ' 8' |
| no_part jpp/100/signed | '1' |  | 0 |  |
| no_rand jpp/100/signed | '1' |  | 0 |  |
| no_part jpp26_100/75/slice | '8' |  | 1 |  |
| no_rand jpp26_100/75/slice | '8' |  | 1 |  |
| no_part ratoms75/75/scaled | '8' |  | 1 |  |
| no_rand ratoms75/75/scaled | '8' |  | 1 |  |
| no_part ratoms75own/75/own | '8' |  | 1 |  |
| no_rand ratoms75own/75/own | '8' |  | 1 |  |

#### P2-L0-0204: bridge tick → horse, token 6

**lookup**: O's answer 3, S's answer 8

O, as read:

```
<|im_start|>user
Maria picked the⟦ tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '3' |  | 0 | ' 3' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 0 | ' 3' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 0 |  |
| no_rand jpp26_100/75/slice | '3' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 0 |  |
| no_rand ratoms75/75/scaled | '3' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 0 |  |

**recall**: O's answer 8, S's answer 4

O, as read:

```
<|im_start|>user
Maria picked the⟦ tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '6' |  | 0 | ' 6' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '6' |  | 0 | ' 6' |
| no_part jpp/100/signed | '8' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 0 |  |
| no_part jpp26_100/75/slice | '6' |  | 0 |  |
| no_rand jpp26_100/75/slice | '6' |  | 0 |  |
| no_part ratoms75/75/scaled | '6' |  | 0 |  |
| no_rand ratoms75/75/scaled | '6' |  | 0 |  |
| no_part ratoms75own/75/own | '6' |  | 0 |  |
| no_rand ratoms75own/75/own | '6' |  | 0 |  |

## qwen3.5-9b

### routes test, another item moved (C2): qwen35_9b_x6_routes_x47_1, 10 random items of 300 (seed 0)

#### C2-0035: bridge goat → beetle, token 43; expected digits {'identity': 2, 'position': 4, 'value': 8, 'original': 9}

**lookup**: O's answer 9, S's answer 8

O, as read:

```
<|im_start|>user
The locker of the beetle is 2. The locker of the tiger is 4. The locker of the goat is 9. Leo picked the tiger. Amy picked the beetle. Ivan picked the⟦ goat⟧.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' | original | 0 |  |
| whole | '4' | position | 0 |  |
| no_jpp | '4' | position | 0 |  |
| no_jpp_rand | '9' | original | 0 |  |
| no_alf | '9' | original | 0 |  |
| no_alf_rand | '4' | position | 0 |  |
| no_jpp100 | '9' | original | 0 |  |
| no_jpp100_rand | '9' | original | 0 |  |
| no_jpp26_100 | '9' | original | 0 |  |
| no_jpp26_100_rand | '9' | original | 0 |  |
| no_ratoms75 | '4' | position | 0 |  |
| no_ratoms75_rand | '9' | original | 0 |  |
| no_ratoms75own | '4' | position | 0 |  |
| no_ratoms75own_rand | '4' | position | 0 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the beetle is 2. The locker of the tiger is 4. The locker of the goat is 9. Leo picked the tiger. Amy picked the beetle. Ivan picked the⟦ goat⟧.
How many legs does Ivan's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '6' |  | 1 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '6' |  | 1 |  |
| no_alf | '6' |  | 1 |  |
| no_alf_rand | '6' |  | 1 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '4' |  | 0 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '6' |  | 1 |  |
| no_ratoms75 | '6' |  | 1 |  |
| no_ratoms75_rand | '6' |  | 1 |  |
| no_ratoms75own | '4' |  | 0 |  |
| no_ratoms75own_rand | '6' |  | 1 |  |

#### C2-0235: bridge crow → ant, token 38; expected digits {'identity': 3, 'position': 5, 'value': 9, 'original': 4}

**lookup**: O's answer 4, S's answer 9

O, as read:

```
<|im_start|>user
The locker of the fox is 5. The locker of the ant is 3. The locker of the crow is 4. Henry picked the fox. Lucy picked the⟦ crow⟧. Kyle picked the ant.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '5' | position | 0 |  |
| no_jpp | '5' | position | 0 |  |
| no_jpp_rand | '5' | position | 0 |  |
| no_alf | '3' | identity | 0 |  |
| no_alf_rand | '5' | position | 0 |  |
| no_jpp100 | '5' | position | 0 |  |
| no_jpp100_rand | '3' | identity | 0 |  |
| no_jpp26_100 | '5' | position | 0 |  |
| no_jpp26_100_rand | '5' | position | 0 |  |
| no_ratoms75 | '5' | position | 0 |  |
| no_ratoms75_rand | '5' | position | 0 |  |
| no_ratoms75own | '5' | position | 0 |  |
| no_ratoms75own_rand | '5' | position | 0 |  |

**recall**: O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the fox is 5. The locker of the ant is 3. The locker of the crow is 4. Henry picked the fox. Lucy picked the⟦ crow⟧. Kyle picked the ant.
How many legs does Lucy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '6' |  | 1 |  |
| no_jpp | '6' |  | 1 |  |
| no_jpp_rand | '6' |  | 1 |  |
| no_alf | '6' |  | 1 |  |
| no_alf_rand | '6' |  | 1 |  |
| no_jpp100 | '2' |  | 0 |  |
| no_jpp100_rand | '6' |  | 1 |  |
| no_jpp26_100 | '6' |  | 1 |  |
| no_jpp26_100_rand | '6' |  | 1 |  |
| no_ratoms75 | '6' |  | 1 |  |
| no_ratoms75_rand | '6' |  | 1 |  |
| no_ratoms75own | '6' |  | 1 |  |
| no_ratoms75own_rand | '6' |  | 1 |  |

#### C2-0280: bridge cow → spider, token 43; expected digits {'identity': 6, 'position': 3, 'value': 2, 'original': 8}

**lookup**: O's answer 8, S's answer 2

O, as read:

```
<|im_start|>user
The locker of the chicken is 3. The locker of the cow is 8. The locker of the spider is 6. Zoe picked the chicken. Grace picked the spider. Tom picked the⟦ cow⟧.
Which locker belongs to Tom's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' | original | 0 |  |
| whole | '6' | identity | 0 |  |
| no_jpp | '6' | identity | 0 |  |
| no_jpp_rand | '6' | identity | 0 |  |
| no_alf | '6' | identity | 0 |  |
| no_alf_rand | '6' | identity | 0 |  |
| no_jpp100 | '8' | original | 0 |  |
| no_jpp100_rand | '6' | identity | 0 |  |
| no_jpp26_100 | '6' | identity | 0 |  |
| no_jpp26_100_rand | '6' | identity | 0 |  |
| no_ratoms75 | '6' | identity | 0 |  |
| no_ratoms75_rand | '6' | identity | 0 |  |
| no_ratoms75own | '6' | identity | 0 |  |
| no_ratoms75own_rand | '6' | identity | 0 |  |

**recall**: O's answer 4, S's answer 8

O, as read:

```
<|im_start|>user
The locker of the chicken is 3. The locker of the cow is 8. The locker of the spider is 6. Zoe picked the chicken. Grace picked the spider. Tom picked the⟦ cow⟧.
How many legs does Tom's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '8' |  | 1 |  |
| no_jpp | '8' |  | 1 |  |
| no_jpp_rand | '8' |  | 1 |  |
| no_alf | '8' |  | 1 |  |
| no_alf_rand | '8' |  | 1 |  |
| no_jpp100 | '8' |  | 1 |  |
| no_jpp100_rand | '8' |  | 1 |  |
| no_jpp26_100 | '6' |  | 0 |  |
| no_jpp26_100_rand | '8' |  | 1 |  |
| no_ratoms75 | '8' |  | 1 |  |
| no_ratoms75_rand | '8' |  | 1 |  |
| no_ratoms75own | '8' |  | 1 |  |
| no_ratoms75own_rand | '8' |  | 1 |  |

#### C2-0337: bridge turkey → rabbit, token 38; expected digits {'identity': 8, 'position': 1, 'value': 3, 'original': 7}

**lookup**: O's answer 7, S's answer 3

O, as read:

```
<|im_start|>user
The locker of the turkey is 7. The locker of the tick is 1. The locker of the rabbit is 8. Kate picked the tick. Eric picked the⟦ turkey⟧. Victor picked the rabbit.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' | original | 0 |  |
| whole | '8' | identity | 0 |  |
| no_jpp | '1' | position | 0 |  |
| no_jpp_rand | '1' | position | 0 |  |
| no_alf | '7' | original | 0 |  |
| no_alf_rand | '1' | position | 0 |  |
| no_jpp100 | '1' | position | 0 |  |
| no_jpp100_rand | '7' | original | 0 |  |
| no_jpp26_100 | '1' | position | 0 |  |
| no_jpp26_100_rand | '1' | position | 0 |  |
| no_ratoms75 | '1' | position | 0 |  |
| no_ratoms75_rand | '1' | position | 0 |  |
| no_ratoms75own | '1' | position | 0 |  |
| no_ratoms75own_rand | '8' | identity | 0 |  |

**recall**: O's answer 2, S's answer 4

O, as read:

```
<|im_start|>user
The locker of the turkey is 7. The locker of the tick is 1. The locker of the rabbit is 8. Kate picked the tick. Eric picked the⟦ turkey⟧. Victor picked the rabbit.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '4' |  | 1 |  |
| no_jpp | '4' |  | 1 |  |
| no_jpp_rand | '4' |  | 1 |  |
| no_alf | '4' |  | 1 |  |
| no_alf_rand | '4' |  | 1 |  |
| no_jpp100 | '2' |  | 0 |  |
| no_jpp100_rand | '4' |  | 1 |  |
| no_jpp26_100 | '4' |  | 1 |  |
| no_jpp26_100_rand | '4' |  | 1 |  |
| no_ratoms75 | '4' |  | 1 |  |
| no_ratoms75_rand | '4' |  | 1 |  |
| no_ratoms75own | '4' |  | 1 |  |
| no_ratoms75own_rand | '4' |  | 1 |  |

#### C2-0367: bridge pig → butterfly, token 43; expected digits {'identity': 8, 'position': 9, 'value': 7, 'original': 4}

**lookup**: O's answer 4, S's answer 7

O, as read:

```
<|im_start|>user
The locker of the bee is 9. The locker of the butterfly is 8. The locker of the pig is 4. Sean picked the bee. Mark picked the butterfly. Fiona picked the⟦ pig⟧.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '8' | identity | 0 |  |
| no_jpp | '8' | identity | 0 |  |
| no_jpp_rand | '8' | identity | 0 |  |
| no_alf | '8' | identity | 0 |  |
| no_alf_rand | '8' | identity | 0 |  |
| no_jpp100 | '4' | original | 0 |  |
| no_jpp100_rand | '8' | identity | 0 |  |
| no_jpp26_100 | '8' | identity | 0 |  |
| no_jpp26_100_rand | '8' | identity | 0 |  |
| no_ratoms75 | '8' | identity | 0 |  |
| no_ratoms75_rand | '8' | identity | 0 |  |
| no_ratoms75own | '8' | identity | 0 |  |
| no_ratoms75own_rand | '8' | identity | 0 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the bee is 9. The locker of the butterfly is 8. The locker of the pig is 4. Sean picked the bee. Mark picked the butterfly. Fiona picked the⟦ pig⟧.
How many legs does Fiona's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '6' |  | 1 |  |
| no_jpp | '6' |  | 1 |  |
| no_jpp_rand | '6' |  | 1 |  |
| no_alf | '6' |  | 1 |  |
| no_alf_rand | '6' |  | 1 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '6' |  | 1 |  |
| no_jpp26_100 | '6' |  | 1 |  |
| no_jpp26_100_rand | '6' |  | 1 |  |
| no_ratoms75 | '6' |  | 1 |  |
| no_ratoms75_rand | '6' |  | 1 |  |
| no_ratoms75own | '6' |  | 1 |  |
| no_ratoms75own_rand | '6' |  | 1 |  |

#### C2-0378: bridge duck → deer, token 33; expected digits {'identity': 1, 'position': 9, 'value': 7, 'original': 4}

**lookup**: O's answer 4, S's answer 7

O, as read:

```
<|im_start|>user
The locker of the fox is 9. The locker of the deer is 1. The locker of the duck is 4. Kate picked the⟦ duck⟧. Paul picked the fox. Vera picked the deer.
Which locker belongs to Kate's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '9' | position | 0 |  |
| no_jpp | '9' | position | 0 |  |
| no_jpp_rand | '9' | position | 0 |  |
| no_alf | '1' | identity | 0 |  |
| no_alf_rand | '9' | position | 0 |  |
| no_jpp100 | '9' | position | 0 |  |
| no_jpp100_rand | '9' | position | 0 |  |
| no_jpp26_100 | '9' | position | 0 |  |
| no_jpp26_100_rand | '9' | position | 0 |  |
| no_ratoms75 | '9' | position | 0 |  |
| no_ratoms75_rand | '9' | position | 0 |  |
| no_ratoms75own | '9' | position | 0 |  |
| no_ratoms75own_rand | '9' | position | 0 |  |

**recall**: O's answer 2, S's answer 4

O, as read:

```
<|im_start|>user
The locker of the fox is 9. The locker of the deer is 1. The locker of the duck is 4. Kate picked the⟦ duck⟧. Paul picked the fox. Vera picked the deer.
How many legs does Kate's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
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

#### C2-0390: bridge owl → bee, token 38; expected digits {'identity': 9, 'position': 8, 'value': 7, 'original': 4}

**lookup**: O's answer 4, S's answer 7

O, as read:

```
<|im_start|>user
The locker of the bee is 9. The locker of the owl is 4. The locker of the mouse is 8. Mark picked the bee. Zoe picked the⟦ owl⟧. Peter picked the mouse.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' | original | 0 |  |
| whole | '9' | identity | 0 |  |
| no_jpp | '9' | identity | 0 |  |
| no_jpp_rand | '9' | identity | 0 |  |
| no_alf | '4' | original | 0 |  |
| no_alf_rand | '9' | identity | 0 |  |
| no_jpp100 | '9' | identity | 0 |  |
| no_jpp100_rand | '9' | identity | 0 |  |
| no_jpp26_100 | '9' | identity | 0 |  |
| no_jpp26_100_rand | '9' | identity | 0 |  |
| no_ratoms75 | '9' | identity | 0 |  |
| no_ratoms75_rand | '9' | identity | 0 |  |
| no_ratoms75own | '9' | identity | 0 |  |
| no_ratoms75own_rand | '9' | identity | 0 |  |

**recall**: O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the bee is 9. The locker of the owl is 4. The locker of the mouse is 8. Mark picked the bee. Zoe picked the⟦ owl⟧. Peter picked the mouse.
How many legs does Zoe's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '6' |  | 1 |  |
| no_jpp | '6' |  | 1 |  |
| no_jpp_rand | '6' |  | 1 |  |
| no_alf | '6' |  | 1 |  |
| no_alf_rand | '6' |  | 1 |  |
| no_jpp100 | '6' |  | 1 |  |
| no_jpp100_rand | '6' |  | 1 |  |
| no_jpp26_100 | '6' |  | 1 |  |
| no_jpp26_100_rand | '6' |  | 1 |  |
| no_ratoms75 | '6' |  | 1 |  |
| no_ratoms75_rand | '6' |  | 1 |  |
| no_ratoms75own | '6' |  | 1 |  |
| no_ratoms75own_rand | '6' |  | 1 |  |

#### C2-0438: bridge dog → beetle, token 33; expected digits {'identity': 9, 'position': 6, 'value': 8, 'original': 7}

**lookup**: O's answer 7, S's answer 8

O, as read:

```
<|im_start|>user
The locker of the beetle is 9. The locker of the sheep is 6. The locker of the dog is 7. Ben picked the⟦ dog⟧. Sean picked the sheep. Olivia picked the beetle.
Which locker belongs to Ben's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' | original | 0 |  |
| whole | '6' | position | 0 |  |
| no_jpp | '6' | position | 0 |  |
| no_jpp_rand | '7' | original | 0 |  |
| no_alf | '7' | original | 0 |  |
| no_alf_rand | '6' | position | 0 |  |
| no_jpp100 | '7' | original | 0 |  |
| no_jpp100_rand | '7' | original | 0 |  |
| no_jpp26_100 | '6' | position | 0 |  |
| no_jpp26_100_rand | '7' | original | 0 |  |
| no_ratoms75 | '6' | position | 0 |  |
| no_ratoms75_rand | '7' | original | 0 |  |
| no_ratoms75own | '6' | position | 0 |  |
| no_ratoms75own_rand | '6' | position | 0 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|im_start|>user
The locker of the beetle is 9. The locker of the sheep is 6. The locker of the dog is 7. Ben picked the⟦ dog⟧. Sean picked the sheep. Olivia picked the beetle.
How many legs does Ben's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '6' |  | 1 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '6' |  | 1 |  |
| no_alf | '6' |  | 1 |  |
| no_alf_rand | '6' |  | 1 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '6' |  | 1 |  |
| no_jpp26_100 | '6' |  | 1 |  |
| no_jpp26_100_rand | '6' |  | 1 |  |
| no_ratoms75 | '6' |  | 1 |  |
| no_ratoms75_rand | '6' |  | 1 |  |
| no_ratoms75own | '6' |  | 1 |  |
| no_ratoms75own_rand | '6' |  | 1 |  |

#### C2-0447: bridge bee → rabbit, token 43; expected digits {'identity': 2, 'position': 7, 'value': 9, 'original': 5}

**lookup**: O's answer 5, S's answer 9

O, as read:

```
<|im_start|>user
The locker of the goat is 7. The locker of the bee is 5. The locker of the rabbit is 2. Eva picked the rabbit. Frank picked the goat. Iris picked the⟦ bee⟧.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' | original | 0 |  |
| whole | '2' | identity | 0 |  |
| no_jpp | '7' | position | 0 |  |
| no_jpp_rand | '2' | identity | 0 |  |
| no_alf | '2' | identity | 0 |  |
| no_alf_rand | '2' | identity | 0 |  |
| no_jpp100 | '7' | position | 0 |  |
| no_jpp100_rand | '7' | position | 0 |  |
| no_jpp26_100 | '7' | position | 0 |  |
| no_jpp26_100_rand | '2' | identity | 0 |  |
| no_ratoms75 | '2' | identity | 0 |  |
| no_ratoms75_rand | '2' | identity | 0 |  |
| no_ratoms75own | '2' | identity | 0 |  |
| no_ratoms75own_rand | '2' | identity | 0 |  |

**recall**: O's answer 6, S's answer 4

O, as read:

```
<|im_start|>user
The locker of the goat is 7. The locker of the bee is 5. The locker of the rabbit is 2. Eva picked the rabbit. Frank picked the goat. Iris picked the⟦ bee⟧.
How many legs does Iris's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
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

#### C2-0475: bridge crow → lion, token 33; expected digits {'identity': 2, 'position': 5, 'value': 9, 'original': 1}

**lookup**: O's answer 1, S's answer 9

O, as read:

```
<|im_start|>user
The locker of the crow is 1. The locker of the lion is 2. The locker of the fox is 5. Will picked the⟦ crow⟧. Laura picked the lion. Nina picked the fox.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' | original | 0 |  |
| whole | '2' | identity | 0 |  |
| no_jpp | '5' | position | 0 |  |
| no_jpp_rand | '2' | identity | 0 |  |
| no_alf | '1' | original | 0 |  |
| no_alf_rand | '2' | identity | 0 |  |
| no_jpp100 | '5' | position | 0 |  |
| no_jpp100_rand | '1' | original | 0 |  |
| no_jpp26_100 | '2' | identity | 0 |  |
| no_jpp26_100_rand | '2' | identity | 0 |  |
| no_ratoms75 | '2' | identity | 0 |  |
| no_ratoms75_rand | '2' | identity | 0 |  |
| no_ratoms75own | '2' | identity | 0 |  |
| no_ratoms75own_rand | '2' | identity | 0 |  |

**recall**: O's answer 2, S's answer 4

O, as read:

```
<|im_start|>user
The locker of the crow is 1. The locker of the lion is 2. The locker of the fox is 5. Will picked the⟦ crow⟧. Laura picked the lion. Nina picked the fox.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '4' |  | 1 |  |
| no_jpp | '2' |  | 0 |  |
| no_jpp_rand | '4' |  | 1 |  |
| no_alf | '4' |  | 1 |  |
| no_alf_rand | '4' |  | 1 |  |
| no_jpp100 | '2' |  | 0 |  |
| no_jpp100_rand | '2' |  | 0 |  |
| no_jpp26_100 | '4' |  | 1 |  |
| no_jpp26_100_rand | '4' |  | 1 |  |
| no_ratoms75 | '4' |  | 1 |  |
| no_ratoms75_rand | '4' |  | 1 |  |
| no_ratoms75own | '4' |  | 1 |  |
| no_ratoms75own_rand | '4' |  | 1 |  |

### main test (two people swap picks): qwen35_9b_x47_1_main, 10 random items of 200 (seed 0)

#### P2-L0-0017: bridge iota → delta, token 30

**lookup**: O's answer 2, S's answer 6

O, as read:

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '6' |  | 1 | ' 6\n' |
| no_part jpp/25/signed | '6' |  | 1 | ' 6\n' |
| no_rand jpp/25/signed | '6' |  | 1 | ' 6\n' |
| no_part jpp/100/signed | '6' |  | 1 |  |
| no_rand jpp/100/signed | '6' |  | 1 |  |
| no_part jpp26_100/75/slice | '6' |  | 1 |  |
| no_rand jpp26_100/75/slice | '6' |  | 1 |  |
| no_part ratoms75/75/scaled | '6' |  | 1 |  |
| no_rand ratoms75/75/scaled | '6' |  | 1 |  |
| no_part ratoms75own/75/own | '6' |  | 1 |  |
| no_rand ratoms75own/75/own | '6' |  | 1 |  |

**recall**: O's answer 9, S's answer 4

O, as read:

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. Leo picked⟦ iota⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' |  | 0 |  |
| whole | '4' |  | 1 | ' 4\n' |
| no_part jpp/25/signed | '4' |  | 1 | ' 4\n' |
| no_rand jpp/25/signed | '4' |  | 1 | ' 4\n' |
| no_part jpp/100/signed | '9' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 1 |  |
| no_part jpp26_100/75/slice | '4' |  | 1 |  |
| no_rand jpp26_100/75/slice | '4' |  | 1 |  |
| no_part ratoms75/75/scaled | '4' |  | 1 |  |
| no_rand ratoms75/75/scaled | '4' |  | 1 |  |
| no_part ratoms75own/75/own | '4' |  | 1 |  |
| no_rand ratoms75own/75/own | '4' |  | 1 |  |

#### P2-L0-0096: bridge bee → spider, token 43

**lookup**: O's answer 1, S's answer 5

O, as read:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' |  | 0 |  |
| whole | '5' |  | 1 | ' 5\n' |
| no_part jpp/25/signed | '5' |  | 1 | ' 5\n' |
| no_rand jpp/25/signed | '5' |  | 1 | ' 5\n' |
| no_part jpp/100/signed | '5' |  | 1 |  |
| no_rand jpp/100/signed | '5' |  | 1 |  |
| no_part jpp26_100/75/slice | '5' |  | 1 |  |
| no_rand jpp26_100/75/slice | '5' |  | 1 |  |
| no_part ratoms75/75/scaled | '5' |  | 1 |  |
| no_rand ratoms75/75/scaled | '5' |  | 1 |  |
| no_part ratoms75own/75/own | '5' |  | 1 |  |
| no_rand ratoms75own/75/own | '5' |  | 1 |  |

**recall**: O's answer 6, S's answer 8

O, as read:

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦ bee⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '8' |  | 1 | ' 8\n' |
| no_part jpp/25/signed | '8' |  | 1 | ' 8\n' |
| no_rand jpp/25/signed | '8' |  | 1 | ' 8\n' |
| no_part jpp/100/signed | '8' |  | 1 |  |
| no_rand jpp/100/signed | '8' |  | 1 |  |
| no_part jpp26_100/75/slice | '8' |  | 1 |  |
| no_rand jpp26_100/75/slice | '8' |  | 1 |  |
| no_part ratoms75/75/scaled | '8' |  | 1 |  |
| no_rand ratoms75/75/scaled | '8' |  | 1 |  |
| no_part ratoms75own/75/own | '8' |  | 1 |  |
| no_rand ratoms75own/75/own | '8' |  | 1 |  |

#### P2-L0-0110: bridge iota → epsilon, token 34

**lookup**: O's answer 2, S's answer 7

O, as read:

```
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked⟦ iota⟧.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '7' |  | 1 | ' 7\n' |
| no_part jpp/25/signed | '7' |  | 1 | ' 7\n' |
| no_rand jpp/25/signed | '7' |  | 1 | ' 7\n' |
| no_part jpp/100/signed | '2' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp26_100/75/slice | '7' |  | 1 |  |
| no_rand jpp26_100/75/slice | '7' |  | 1 |  |
| no_part ratoms75/75/scaled | '7' |  | 1 |  |
| no_rand ratoms75/75/scaled | '7' |  | 1 |  |
| no_part ratoms75own/75/own | '7' |  | 1 |  |
| no_rand ratoms75own/75/own | '7' |  | 1 |  |

**recall**: O's answer 9, S's answer 5

O, as read:

```
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. Anna picked⟦ iota⟧.
Which position in the Greek alphabet does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' |  | 0 |  |
| whole | '5' |  | 1 | ' 5\n' |
| no_part jpp/25/signed | '9' |  | 0 | ' 9\n' |
| no_rand jpp/25/signed | '5' |  | 1 | ' 5\n' |
| no_part jpp/100/signed | '9' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 1 |  |
| no_part jpp26_100/75/slice | '5' |  | 1 |  |
| no_rand jpp26_100/75/slice | '5' |  | 1 |  |
| no_part ratoms75/75/scaled | '5' |  | 1 |  |
| no_rand ratoms75/75/scaled | '5' |  | 1 |  |
| no_part ratoms75own/75/own | '5' |  | 1 |  |
| no_rand ratoms75own/75/own | '5' |  | 1 |  |

#### P2-L0-0142: bridge nitrogen → oxygen, token 27

**lookup**: O's answer 3, S's answer 6

O, as read:

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ nitrogen⟧. The locker of nitrogen is three.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '3' |  | 0 | ' 3\n' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3\n' |
| no_rand jpp/25/signed | '3' |  | 0 | ' 3\n' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 0 |  |
| no_rand jpp26_100/75/slice | '3' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 0 |  |
| no_rand ratoms75/75/scaled | '3' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 0 |  |

**recall**: O's answer 7, S's answer 8

O, as read:

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦ nitrogen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '8' |  | 1 | ' 8\n' |
| no_part jpp/25/signed | '7' |  | 0 | ' 7\n' |
| no_rand jpp/25/signed | '8' |  | 1 | ' 8\n' |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '8' |  | 1 |  |
| no_part jpp26_100/75/slice | '8' |  | 1 |  |
| no_rand jpp26_100/75/slice | '8' |  | 1 |  |
| no_part ratoms75/75/scaled | '8' |  | 1 |  |
| no_rand ratoms75/75/scaled | '8' |  | 1 |  |
| no_part ratoms75own/75/own | '8' |  | 1 |  |
| no_rand ratoms75own/75/own | '8' |  | 1 |  |

#### P2-L0-0149: bridge delta → iota, token 29

**lookup**: O's answer 1, S's answer 8

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

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' |  | 0 |  |
| whole | '8' |  | 1 | ' 8\n' |
| no_part jpp/25/signed | '8' |  | 1 | ' 8\n' |
| no_rand jpp/25/signed | '8' |  | 1 | ' 8\n' |
| no_part jpp/100/signed | '8' |  | 1 |  |
| no_rand jpp/100/signed | '1' |  | 0 |  |
| no_part jpp26_100/75/slice | '8' |  | 1 |  |
| no_rand jpp26_100/75/slice | '8' |  | 1 |  |
| no_part ratoms75/75/scaled | '8' |  | 1 |  |
| no_rand ratoms75/75/scaled | '8' |  | 1 |  |
| no_part ratoms75own/75/own | '8' |  | 1 |  |
| no_rand ratoms75own/75/own | '8' |  | 1 |  |

**recall**: O's answer 4, S's answer 9

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

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '9' |  | 1 | ' 9\n' |
| no_part jpp/25/signed | '9' |  | 1 | ' 9\n' |
| no_rand jpp/25/signed | '9' |  | 1 | ' 9\n' |
| no_part jpp/100/signed | '9' |  | 1 |  |
| no_rand jpp/100/signed | '9' |  | 1 |  |
| no_part jpp26_100/75/slice | '9' |  | 1 |  |
| no_rand jpp26_100/75/slice | '9' |  | 1 |  |
| no_part ratoms75/75/scaled | '9' |  | 1 |  |
| no_rand ratoms75/75/scaled | '9' |  | 1 |  |
| no_part ratoms75own/75/own | '9' |  | 1 |  |
| no_rand ratoms75own/75/own | '9' |  | 1 |  |

#### P2-L0-0154: bridge oxygen → helium, token 24

**lookup**: O's answer 5, S's answer 3

O, as read:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ oxygen⟧. Max picked helium. The locker of oxygen is five.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' |  | 0 |  |
| whole | '5' |  | 0 | ' 5\n' |
| no_part jpp/25/signed | '5' |  | 0 | ' 5\n' |
| no_rand jpp/25/signed | '5' |  | 0 | ' 5\n' |
| no_part jpp/100/signed | '5' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 0 |  |
| no_part jpp26_100/75/slice | '5' |  | 0 |  |
| no_rand jpp26_100/75/slice | '5' |  | 0 |  |
| no_part ratoms75/75/scaled | '5' |  | 0 |  |
| no_rand ratoms75/75/scaled | '5' |  | 0 |  |
| no_part ratoms75own/75/own | '5' |  | 0 |  |
| no_rand ratoms75own/75/own | '5' |  | 0 |  |

**recall**: O's answer 8, S's answer 2

O, as read:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦ oxygen⟧. Max picked helium. The locker of oxygen is five.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '2' |  | 1 | ' 2\n' |
| no_part jpp/25/signed | '2' |  | 1 | ' 2\n' |
| no_rand jpp/25/signed | '2' |  | 1 | ' 2\n' |
| no_part jpp/100/signed | '8' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 1 |  |
| no_part jpp26_100/75/slice | '2' |  | 1 |  |
| no_rand jpp26_100/75/slice | '2' |  | 1 |  |
| no_part ratoms75/75/scaled | '2' |  | 1 |  |
| no_rand ratoms75/75/scaled | '2' |  | 1 |  |
| no_part ratoms75own/75/own | '2' |  | 1 |  |
| no_rand ratoms75own/75/own | '2' |  | 1 |  |

#### P2-L0-0181: bridge helium → nitrogen, token 37

**lookup**: O's answer 3, S's answer 9

O, as read:

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ helium⟧.
Which locker belongs to Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '9' |  | 1 | ' 9\n' |
| no_part jpp/25/signed | '9' |  | 1 | ' 9\n' |
| no_rand jpp/25/signed | '9' |  | 1 | ' 9\n' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '9' |  | 1 |  |
| no_rand jpp26_100/75/slice | '9' |  | 1 |  |
| no_part ratoms75/75/scaled | '9' |  | 1 |  |
| no_rand ratoms75/75/scaled | '9' |  | 1 |  |
| no_part ratoms75own/75/own | '9' |  | 1 |  |
| no_rand ratoms75own/75/own | '9' |  | 1 |  |

**recall**: O's answer 2, S's answer 7

O, as read:

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. Adam picked⟦ helium⟧.
What is the atomic number of Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '7' |  | 1 | ' 7\n' |
| no_part jpp/25/signed | '2' |  | 0 | ' 2\n' |
| no_rand jpp/25/signed | '7' |  | 1 | ' 7\n' |
| no_part jpp/100/signed | '2' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp26_100/75/slice | '7' |  | 1 |  |
| no_rand jpp26_100/75/slice | '7' |  | 1 |  |
| no_part ratoms75/75/scaled | '7' |  | 1 |  |
| no_rand ratoms75/75/scaled | '7' |  | 1 |  |
| no_part ratoms75own/75/own | '7' |  | 1 |  |
| no_rand ratoms75own/75/own | '7' |  | 1 |  |

#### P2-L0-0184: bridge helium → hydrogen, token 25

**lookup**: O's answer 9, S's answer 5

O, as read:

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked⟦ helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' |  | 0 |  |
| whole | '5' |  | 1 | ' 5\n' |
| no_part jpp/25/signed | '2' |  | 0 | ' 2\n' |
| no_rand jpp/25/signed | '2' |  | 0 | ' 2\n' |
| no_part jpp/100/signed | '2' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp26_100/75/slice | '2' |  | 0 |  |
| no_rand jpp26_100/75/slice | '2' |  | 0 |  |
| no_part ratoms75/75/scaled | '5' |  | 1 |  |
| no_rand ratoms75/75/scaled | '2' |  | 0 |  |
| no_part ratoms75own/75/own | '5' |  | 1 |  |
| no_rand ratoms75own/75/own | '5' |  | 1 |  |

**recall**: O's answer 2, S's answer 1

O, as read:

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. Victor picked⟦ helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '1' |  | 1 | ' 1\n' |
| no_part jpp/25/signed | '2' |  | 0 | ' 2\n' |
| no_rand jpp/25/signed | '1' |  | 1 | ' 1\n' |
| no_part jpp/100/signed | '2' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp26_100/75/slice | '2' |  | 0 |  |
| no_rand jpp26_100/75/slice | '1' |  | 1 |  |
| no_part ratoms75/75/scaled | '1' |  | 1 |  |
| no_rand ratoms75/75/scaled | '1' |  | 1 |  |
| no_part ratoms75own/75/own | '1' |  | 1 |  |
| no_rand ratoms75own/75/own | '1' |  | 1 |  |

#### P2-L0-0193: bridge hydrogen → helium, token 27

**lookup**: O's answer 8, S's answer 3

O, as read:

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. Victor picked⟦ hydrogen⟧. The locker of hydrogen is eight.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '3' |  | 1 | ' 3\n' |
| no_part jpp/25/signed | '3' |  | 1 | ' 3\n' |
| no_rand jpp/25/signed | '8' |  | 0 | ' 8\n' |
| no_part jpp/100/signed | '8' |  | 0 |  |
| no_rand jpp/100/signed | '8' |  | 0 |  |
| no_part jpp26_100/75/slice | '8' |  | 0 |  |
| no_rand jpp26_100/75/slice | '8' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 1 |  |
| no_rand ratoms75/75/scaled | '8' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 1 |  |
| no_rand ratoms75own/75/own | '3' |  | 1 |  |

**recall**: O's answer 1, S's answer 2

O, as read:

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. Victor picked⟦ hydrogen⟧. The locker of hydrogen is eight.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' |  | 0 |  |
| whole | '2' |  | 1 | ' 2\n' |
| no_part jpp/25/signed | '2' |  | 1 | ' 2\n' |
| no_rand jpp/25/signed | '2' |  | 1 | ' 2\n' |
| no_part jpp/100/signed | '2' |  | 1 |  |
| no_rand jpp/100/signed | '2' |  | 1 |  |
| no_part jpp26_100/75/slice | '2' |  | 1 |  |
| no_rand jpp26_100/75/slice | '2' |  | 1 |  |
| no_part ratoms75/75/scaled | '2' |  | 1 |  |
| no_rand ratoms75/75/scaled | '2' |  | 1 |  |
| no_part ratoms75own/75/own | '2' |  | 1 |  |
| no_rand ratoms75own/75/own | '2' |  | 1 |  |

#### P2-L0-0290: bridge epsilon → iota, token 34

**lookup**: O's answer 4, S's answer 8

O, as read:

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ epsilon⟧. Noah picked beta.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '8' |  | 1 | ' 8\n' |
| no_part jpp/25/signed | '4' |  | 0 | ' 4\n' |
| no_rand jpp/25/signed | '4' |  | 0 | ' 4\n' |
| no_part jpp/100/signed | '4' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '4' |  | 0 |  |
| no_rand jpp26_100/75/slice | '4' |  | 0 |  |
| no_part ratoms75/75/scaled | '8' |  | 1 |  |
| no_rand ratoms75/75/scaled | '4' |  | 0 |  |
| no_part ratoms75own/75/own | '8' |  | 1 |  |
| no_rand ratoms75own/75/own | '8' |  | 1 |  |

**recall**: O's answer 5, S's answer 9

O, as read:

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. Amy picked⟦ epsilon⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' |  | 0 |  |
| whole | '9' |  | 1 | ' 9\n' |
| no_part jpp/25/signed | '5' |  | 0 | ' 5\n' |
| no_rand jpp/25/signed | '9' |  | 1 | ' 9\n' |
| no_part jpp/100/signed | '5' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 0 |  |
| no_part jpp26_100/75/slice | '9' |  | 1 |  |
| no_rand jpp26_100/75/slice | '9' |  | 1 |  |
| no_part ratoms75/75/scaled | '9' |  | 1 |  |
| no_rand ratoms75/75/scaled | '9' |  | 1 |  |
| no_part ratoms75own/75/own | '9' |  | 1 |  |
| no_rand ratoms75own/75/own | '9' |  | 1 |  |

## muse-glimmer-30b

### routes test, another item moved (C2): muse30_x6_routes_x47_1, 10 random items of 300 (seed 0)

#### C2-0039: bridge dog → bee, token 77; expected digits {'identity': 9, 'position': 8, 'value': 1, 'original': 7}

**lookup**: O's answer 7, S's answer 1

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 9. The locker of the dog is 7. The locker of the cow is 8. Rose picked the bee. Mark picked the⟦ dog⟧. Oscar picked the cow.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' | original | 0 |  |
| whole | '9' | identity | 0 |  |
| no_jpp | '9' | identity | 0 |  |
| no_jpp_rand | '9' | identity | 0 |  |
| no_alf | '9' | identity | 0 |  |
| no_alf_rand | '9' | identity | 0 |  |
| no_jpp100 | '9' | identity | 0 |  |
| no_jpp100_rand | '9' | identity | 0 |  |
| no_jpp26_100 | '9' | identity | 0 |  |
| no_jpp26_100_rand | '9' | identity | 0 |  |
| no_ratoms75 | '9' | identity | 0 |  |
| no_ratoms75_rand | '9' | identity | 0 |  |
| no_ratoms75own | '9' | identity | 0 |  |
| no_ratoms75own_rand | '9' | identity | 0 |  |

**recall**: O's answer 4, S's answer 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 9. The locker of the dog is 7. The locker of the cow is 8. Rose picked the bee. Mark picked the⟦ dog⟧. Oscar picked the cow.
How many legs does Mark's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '4' |  | 0 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '4' |  | 0 |  |
| no_alf | '4' |  | 0 |  |
| no_alf_rand | '4' |  | 0 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '4' |  | 0 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '4' |  | 0 |  |
| no_ratoms75 | '4' |  | 0 |  |
| no_ratoms75_rand | '4' |  | 0 |  |
| no_ratoms75own | '4' |  | 0 |  |
| no_ratoms75own_rand | '4' |  | 0 |  |

#### C2-0278: bridge owl → cow, token 77; expected digits {'identity': 1, 'position': 6, 'value': 3, 'original': 8}

**lookup**: O's answer 8, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the cow is 1. The locker of the camel is 6. The locker of the owl is 8. Peter picked the camel. Ella picked the⟦ owl⟧. Tara picked the cow.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' | original | 0 |  |
| whole | '6' | position | 0 |  |
| no_jpp | '6' | position | 0 |  |
| no_jpp_rand | '6' | position | 0 |  |
| no_alf | '6' | position | 0 |  |
| no_alf_rand | '6' | position | 0 |  |
| no_jpp100 | '6' | position | 0 |  |
| no_jpp100_rand | '6' | position | 0 |  |
| no_jpp26_100 | '6' | position | 0 |  |
| no_jpp26_100_rand | '6' | position | 0 |  |
| no_ratoms75 | '6' | position | 0 |  |
| no_ratoms75_rand | '6' | position | 0 |  |
| no_ratoms75own | '6' | position | 0 |  |
| no_ratoms75own_rand | '6' | position | 0 |  |

**recall**: O's answer 2, S's answer 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the cow is 1. The locker of the camel is 6. The locker of the owl is 8. Peter picked the camel. Ella picked the⟦ owl⟧. Tara picked the cow.
How many legs does Ella's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '2' |  | 0 |  |
| no_jpp | '2' |  | 0 |  |
| no_jpp_rand | '2' |  | 0 |  |
| no_alf | '2' |  | 0 |  |
| no_alf_rand | '2' |  | 0 |  |
| no_jpp100 | '2' |  | 0 |  |
| no_jpp100_rand | '2' |  | 0 |  |
| no_jpp26_100 | '2' |  | 0 |  |
| no_jpp26_100_rand | '2' |  | 0 |  |
| no_ratoms75 | '2' |  | 0 |  |
| no_ratoms75_rand | '2' |  | 0 |  |
| no_ratoms75own | '2' |  | 0 |  |
| no_ratoms75own_rand | '2' |  | 0 |  |

#### C2-0324: bridge butterfly → spider, token 77; expected digits {'identity': 1, 'position': 2, 'value': 3, 'original': 5}

**lookup**: O's answer 5, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 1. The locker of the zebra is 2. The locker of the butterfly is 5. Alice picked the zebra. Fiona picked the⟦ butterfly⟧. Max picked the spider.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' | original | 0 |  |
| whole | '2' | position | 0 |  |
| no_jpp | '2' | position | 0 |  |
| no_jpp_rand | '2' | position | 0 |  |
| no_alf | '2' | position | 0 |  |
| no_alf_rand | '2' | position | 0 |  |
| no_jpp100 | '2' | position | 0 |  |
| no_jpp100_rand | '2' | position | 0 |  |
| no_jpp26_100 | '2' | position | 0 |  |
| no_jpp26_100_rand | '2' | position | 0 |  |
| no_ratoms75 | '2' | position | 0 |  |
| no_ratoms75_rand | '2' | position | 0 |  |
| no_ratoms75own | '2' | position | 0 |  |
| no_ratoms75own_rand | '2' | position | 0 |  |

**recall**: O's answer 6, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 1. The locker of the zebra is 2. The locker of the butterfly is 5. Alice picked the zebra. Fiona picked the⟦ butterfly⟧. Max picked the spider.
How many legs does Fiona's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '6' |  | 0 |  |
| no_jpp | '6' |  | 0 |  |
| no_jpp_rand | '6' |  | 0 |  |
| no_alf | '6' |  | 0 |  |
| no_alf_rand | '6' |  | 0 |  |
| no_jpp100 | '6' |  | 0 |  |
| no_jpp100_rand | '6' |  | 0 |  |
| no_jpp26_100 | '6' |  | 0 |  |
| no_jpp26_100_rand | '6' |  | 0 |  |
| no_ratoms75 | '6' |  | 0 |  |
| no_ratoms75_rand | '6' |  | 0 |  |
| no_ratoms75own | '6' |  | 0 |  |
| no_ratoms75own_rand | '6' |  | 0 |  |

#### C2-0385: bridge horse → turkey, token 82; expected digits {'identity': 2, 'position': 9, 'value': 3, 'original': 7}

**lookup**: O's answer 7, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the horse is 7. The locker of the turkey is 2. The locker of the lion is 9. Ivan picked the lion. Sara picked the turkey. Victor picked the⟦ horse⟧.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' | original | 0 |  |
| whole | '2' | identity | 0 |  |
| no_jpp | '2' | identity | 0 |  |
| no_jpp_rand | '2' | identity | 0 |  |
| no_alf | '2' | identity | 0 |  |
| no_alf_rand | '2' | identity | 0 |  |
| no_jpp100 | '2' | identity | 0 |  |
| no_jpp100_rand | '2' | identity | 0 |  |
| no_jpp26_100 | '2' | identity | 0 |  |
| no_jpp26_100_rand | '2' | identity | 0 |  |
| no_ratoms75 | '2' | identity | 0 |  |
| no_ratoms75_rand | '2' | identity | 0 |  |
| no_ratoms75own | '2' | identity | 0 |  |
| no_ratoms75own_rand | '2' | identity | 0 |  |

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the horse is 7. The locker of the turkey is 2. The locker of the lion is 9. Ivan picked the lion. Sara picked the turkey. Victor picked the⟦ horse⟧.
How many legs does Victor's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '4' |  | 0 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '4' |  | 0 |  |
| no_alf | '4' |  | 0 |  |
| no_alf_rand | '4' |  | 0 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '2' |  | 1 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '2' |  | 1 |  |
| no_ratoms75 | '4' |  | 0 |  |
| no_ratoms75_rand | '2' |  | 1 |  |
| no_ratoms75own | '4' |  | 0 |  |
| no_ratoms75own_rand | '4' |  | 0 |  |

#### C2-0414: bridge tiger → duck, token 72; expected digits {'identity': 8, 'position': 2, 'value': 1, 'original': 5}

**lookup**: O's answer 5, S's answer 1

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the tiger is 5. The locker of the fox is 2. The locker of the duck is 8. Rose picked the⟦ tiger⟧. Kate picked the duck. Owen picked the fox.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
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

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the tiger is 5. The locker of the fox is 2. The locker of the duck is 8. Rose picked the⟦ tiger⟧. Kate picked the duck. Owen picked the fox.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '2' |  | 1 |  |
| no_jpp | '2' |  | 1 |  |
| no_jpp_rand | '2' |  | 1 |  |
| no_alf | '2' |  | 1 |  |
| no_alf_rand | '2' |  | 1 |  |
| no_jpp100 | '2' |  | 1 |  |
| no_jpp100_rand | '2' |  | 1 |  |
| no_jpp26_100 | '2' |  | 1 |  |
| no_jpp26_100_rand | '2' |  | 1 |  |
| no_ratoms75 | '2' |  | 1 |  |
| no_ratoms75_rand | '2' |  | 1 |  |
| no_ratoms75own | '2' |  | 1 |  |
| no_ratoms75own_rand | '2' |  | 1 |  |

#### C2-0441: bridge deer → goose, token 77; expected digits {'identity': 4, 'position': 2, 'value': 3, 'original': 6}

**lookup**: O's answer 6, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the deer is 6. The locker of the pig is 2. The locker of the goose is 4. Ryan picked the goose. Will picked the⟦ deer⟧. Dan picked the pig.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' | original | 0 |  |
| whole | '4' | identity | 0 |  |
| no_jpp | '4' | identity | 0 |  |
| no_jpp_rand | '4' | identity | 0 |  |
| no_alf | '4' | identity | 0 |  |
| no_alf_rand | '4' | identity | 0 |  |
| no_jpp100 | '4' | identity | 0 |  |
| no_jpp100_rand | '4' | identity | 0 |  |
| no_jpp26_100 | '4' | identity | 0 |  |
| no_jpp26_100_rand | '4' | identity | 0 |  |
| no_ratoms75 | '4' | identity | 0 |  |
| no_ratoms75_rand | '4' | identity | 0 |  |
| no_ratoms75own | '4' | identity | 0 |  |
| no_ratoms75own_rand | '4' | identity | 0 |  |

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the deer is 6. The locker of the pig is 2. The locker of the goose is 4. Ryan picked the goose. Will picked the⟦ deer⟧. Dan picked the pig.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '2' |  | 1 |  |
| no_jpp | '2' |  | 1 |  |
| no_jpp_rand | '2' |  | 1 |  |
| no_alf | '2' |  | 1 |  |
| no_alf_rand | '2' |  | 1 |  |
| no_jpp100 | '2' |  | 1 |  |
| no_jpp100_rand | '2' |  | 1 |  |
| no_jpp26_100 | '2' |  | 1 |  |
| no_jpp26_100_rand | '2' |  | 1 |  |
| no_ratoms75 | '2' |  | 1 |  |
| no_ratoms75_rand | '2' |  | 1 |  |
| no_ratoms75own | '2' |  | 1 |  |
| no_ratoms75own_rand | '2' |  | 1 |  |

#### C2-0459: bridge pig → eagle, token 77; expected digits {'identity': 9, 'position': 7, 'value': 3, 'original': 5}

**lookup**: O's answer 5, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the eagle is 9. The locker of the pig is 5. The locker of the fox is 7. Maria picked the fox. Emma picked the⟦ pig⟧. Tom picked the eagle.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' | original | 0 |  |
| whole | '7' | position | 0 |  |
| no_jpp | '7' | position | 0 |  |
| no_jpp_rand | '7' | position | 0 |  |
| no_alf | '7' | position | 0 |  |
| no_alf_rand | '7' | position | 0 |  |
| no_jpp100 | '7' | position | 0 |  |
| no_jpp100_rand | '7' | position | 0 |  |
| no_jpp26_100 | '7' | position | 0 |  |
| no_jpp26_100_rand | '7' | position | 0 |  |
| no_ratoms75 | '7' | position | 0 |  |
| no_ratoms75_rand | '7' | position | 0 |  |
| no_ratoms75own | '7' | position | 0 |  |
| no_ratoms75own_rand | '7' | position | 0 |  |

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the eagle is 9. The locker of the pig is 5. The locker of the fox is 7. Maria picked the fox. Emma picked the⟦ pig⟧. Tom picked the eagle.
How many legs does Emma's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '4' |  | 0 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '4' |  | 0 |  |
| no_alf | '4' |  | 0 |  |
| no_alf_rand | '4' |  | 0 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '4' |  | 0 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '4' |  | 0 |  |
| no_ratoms75 | '4' |  | 0 |  |
| no_ratoms75_rand | '4' |  | 0 |  |
| no_ratoms75own | '4' |  | 0 |  |
| no_ratoms75own_rand | '4' |  | 0 |  |

#### C2-0523: bridge rabbit → spider, token 72; expected digits {'identity': 3, 'position': 1, 'value': 6, 'original': 7}

**lookup**: O's answer 7, S's answer 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 1. The locker of the spider is 3. The locker of the rabbit is 7. Emma picked the⟦ rabbit⟧. Grace picked the turkey. Mark picked the spider.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' | original | 0 |  |
| whole | '1' | position | 0 |  |
| no_jpp | '1' | position | 0 |  |
| no_jpp_rand | '1' | position | 0 |  |
| no_alf | '3' | identity | 0 |  |
| no_alf_rand | '1' | position | 0 |  |
| no_jpp100 | '1' | position | 0 |  |
| no_jpp100_rand | '1' | position | 0 |  |
| no_jpp26_100 | '1' | position | 0 |  |
| no_jpp26_100_rand | '1' | position | 0 |  |
| no_ratoms75 | '1' | position | 0 |  |
| no_ratoms75_rand | '1' | position | 0 |  |
| no_ratoms75own | '1' | position | 0 |  |
| no_ratoms75own_rand | '1' | position | 0 |  |

**recall**: O's answer 4, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 1. The locker of the spider is 3. The locker of the rabbit is 7. Emma picked the⟦ rabbit⟧. Grace picked the turkey. Mark picked the spider.
How many legs does Emma's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '2' |  | 0 |  |
| no_jpp | '2' |  | 0 |  |
| no_jpp_rand | '4' |  | 0 |  |
| no_alf | '4' |  | 0 |  |
| no_alf_rand | '4' |  | 0 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '4' |  | 0 |  |
| no_jpp26_100 | '4' |  | 0 |  |
| no_jpp26_100_rand | '4' |  | 0 |  |
| no_ratoms75 | '2' |  | 0 |  |
| no_ratoms75_rand | '4' |  | 0 |  |
| no_ratoms75own | '2' |  | 0 |  |
| no_ratoms75own_rand | '2' |  | 0 |  |

#### C2-0530: bridge mouse → owl, token 72; expected digits {'identity': 2, 'position': 1, 'value': 3, 'original': 9}

**lookup**: O's answer 9, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the mouse is 9. The locker of the butterfly is 1. The locker of the owl is 2. Sean picked the⟦ mouse⟧. Ivy picked the butterfly. Diana picked the owl.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' | original | 0 |  |
| whole | '1' | position | 0 |  |
| no_jpp | '1' | position | 0 |  |
| no_jpp_rand | '1' | position | 0 |  |
| no_alf | '9' | original | 0 |  |
| no_alf_rand | '1' | position | 0 |  |
| no_jpp100 | '1' | position | 0 |  |
| no_jpp100_rand | '1' | position | 0 |  |
| no_jpp26_100 | '1' | position | 0 |  |
| no_jpp26_100_rand | '1' | position | 0 |  |
| no_ratoms75 | '1' | position | 0 |  |
| no_ratoms75_rand | '1' | position | 0 |  |
| no_ratoms75own | '1' | position | 0 |  |
| no_ratoms75own_rand | '1' | position | 0 |  |

**recall**: O's answer 4, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the mouse is 9. The locker of the butterfly is 1. The locker of the owl is 2. Sean picked the⟦ mouse⟧. Ivy picked the butterfly. Diana picked the owl.
How many legs does Sean's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '2' |  | 1 |  |
| no_jpp | '4' |  | 0 |  |
| no_jpp_rand | '2' |  | 1 |  |
| no_alf | '2' |  | 1 |  |
| no_alf_rand | '2' |  | 1 |  |
| no_jpp100 | '4' |  | 0 |  |
| no_jpp100_rand | '4' |  | 0 |  |
| no_jpp26_100 | '2' |  | 1 |  |
| no_jpp26_100_rand | '2' |  | 1 |  |
| no_ratoms75 | '4' |  | 0 |  |
| no_ratoms75_rand | '2' |  | 1 |  |
| no_ratoms75own | '2' |  | 1 |  |
| no_ratoms75own_rand | '2' |  | 1 |  |

#### C2-0560: bridge owl → mouse, token 82; expected digits {'identity': 8, 'position': 2, 'value': 3, 'original': 6}

**lookup**: O's answer 6, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bear is 2. The locker of the owl is 6. The locker of the mouse is 8. Iris picked the bear. Beth picked the mouse. Vera picked the⟦ owl⟧.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' | original | 0 |  |
| whole | '8' | identity | 0 |  |
| no_jpp | '8' | identity | 0 |  |
| no_jpp_rand | '8' | identity | 0 |  |
| no_alf | '8' | identity | 0 |  |
| no_alf_rand | '8' | identity | 0 |  |
| no_jpp100 | '8' | identity | 0 |  |
| no_jpp100_rand | '8' | identity | 0 |  |
| no_jpp26_100 | '8' | identity | 0 |  |
| no_jpp26_100_rand | '8' | identity | 0 |  |
| no_ratoms75 | '8' | identity | 0 |  |
| no_ratoms75_rand | '8' | identity | 0 |  |
| no_ratoms75own | '8' | identity | 0 |  |
| no_ratoms75own_rand | '8' | identity | 0 |  |

**recall**: O's answer 2, S's answer 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bear is 2. The locker of the owl is 6. The locker of the mouse is 8. Iris picked the bear. Beth picked the mouse. Vera picked the⟦ owl⟧.
How many legs does Vera's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '2' |  | 0 |  |
| no_jpp | '2' |  | 0 |  |
| no_jpp_rand | '2' |  | 0 |  |
| no_alf | '2' |  | 0 |  |
| no_alf_rand | '2' |  | 0 |  |
| no_jpp100 | '2' |  | 0 |  |
| no_jpp100_rand | '2' |  | 0 |  |
| no_jpp26_100 | '2' |  | 0 |  |
| no_jpp26_100_rand | '2' |  | 0 |  |
| no_ratoms75 | '2' |  | 0 |  |
| no_ratoms75_rand | '2' |  | 0 |  |
| no_ratoms75own | '2' |  | 0 |  |
| no_ratoms75own_rand | '2' |  | 0 |  |

### main test (two people swap picks): muse30_x47_1_main, 10 random items of 200 (seed 0)

#### P2-L0-0019: bridge nitrogen → oxygen, token 66

**lookup**: O's answer 6, S's answer 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ nitrogen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '6' |  | 0 | ' 6' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '6' |  | 0 | ' 6' |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 0 |  |
| no_part jpp26_100/75/slice | '6' |  | 0 |  |
| no_rand jpp26_100/75/slice | '6' |  | 0 |  |
| no_part ratoms75/75/scaled | '6' |  | 0 |  |
| no_rand ratoms75/75/scaled | '6' |  | 0 |  |
| no_part ratoms75own/75/own | '6' |  | 0 |  |
| no_rand ratoms75own/75/own | '6' |  | 0 |  |

**recall**: O's answer 7, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '8' |  | 1 | ' 8' |
| no_part jpp/25/signed | '7' |  | 0 | ' 7' |
| no_rand jpp/25/signed | '8' |  | 1 | ' 8' |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '8' |  | 1 |  |
| no_part jpp26_100/75/slice | '8' |  | 1 |  |
| no_rand jpp26_100/75/slice | '8' |  | 1 |  |
| no_part ratoms75/75/scaled | '8' |  | 1 |  |
| no_rand ratoms75/75/scaled | '8' |  | 1 |  |
| no_part ratoms75own/75/own | '8' |  | 1 |  |
| no_rand ratoms75own/75/own | '8' |  | 1 |  |

#### P2-L0-0091: bridge oxygen → hydrogen, token 73

**lookup**: O's answer 7, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ oxygen⟧.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '8' |  | 1 | ' 8' |
| no_part jpp/25/signed | '8' |  | 1 | ' 8' |
| no_rand jpp/25/signed | '8' |  | 1 | ' 8' |
| no_part jpp/100/signed | '8' |  | 1 |  |
| no_rand jpp/100/signed | '8' |  | 1 |  |
| no_part jpp26_100/75/slice | '8' |  | 1 |  |
| no_rand jpp26_100/75/slice | '8' |  | 1 |  |
| no_part ratoms75/75/scaled | '8' |  | 1 |  |
| no_rand ratoms75/75/scaled | '8' |  | 1 |  |
| no_part ratoms75own/75/own | '8' |  | 1 |  |
| no_rand ratoms75own/75/own | '8' |  | 1 |  |

**recall**: O's answer 8, S's answer 1

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ oxygen⟧.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '8' |  | 0 |  |
| whole | '8' |  | 0 | ' 8' |
| no_part jpp/25/signed | '8' |  | 0 | ' 8' |
| no_rand jpp/25/signed | '8' |  | 0 | ' 8' |
| no_part jpp/100/signed | '8' |  | 0 |  |
| no_rand jpp/100/signed | '8' |  | 0 |  |
| no_part jpp26_100/75/slice | '8' |  | 0 |  |
| no_rand jpp26_100/75/slice | '8' |  | 0 |  |
| no_part ratoms75/75/scaled | '8' |  | 0 |  |
| no_rand ratoms75/75/scaled | '8' |  | 0 |  |
| no_part ratoms75own/75/own | '8' |  | 0 |  |
| no_rand ratoms75own/75/own | '8' |  | 0 |  |

#### P2-L0-0106: bridge lithium → helium, token 56

**lookup**: O's answer 6, S's answer 9

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. Paul picked⟦ lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '6' |  | 0 | ' 6' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '6' |  | 0 | ' 6' |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 0 |  |
| no_part jpp26_100/75/slice | '6' |  | 0 |  |
| no_rand jpp26_100/75/slice | '6' |  | 0 |  |
| no_part ratoms75/75/scaled | '6' |  | 0 |  |
| no_rand ratoms75/75/scaled | '6' |  | 0 |  |
| no_part ratoms75own/75/own | '6' |  | 0 |  |
| no_rand ratoms75own/75/own | '6' |  | 0 |  |

**recall**: O's answer 3, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. Paul picked⟦ lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '3' |  | 0 | ' 3' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 0 | ' 3' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 0 |  |
| no_rand jpp26_100/75/slice | '3' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 0 |  |
| no_rand ratoms75/75/scaled | '3' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 0 |  |

#### P2-L0-0141: bridge bee → elephant, token 63

**lookup**: O's answer 4, S's answer 1

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦ bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '4' |  | 0 | ' 4' |
| no_part jpp/25/signed | '4' |  | 0 | ' 4' |
| no_rand jpp/25/signed | '4' |  | 0 | ' 4' |
| no_part jpp/100/signed | '4' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '4' |  | 0 |  |
| no_rand jpp26_100/75/slice | '4' |  | 0 |  |
| no_part ratoms75/75/scaled | '4' |  | 0 |  |
| no_rand ratoms75/75/scaled | '4' |  | 0 |  |
| no_part ratoms75own/75/own | '4' |  | 0 |  |
| no_rand ratoms75own/75/own | '4' |  | 0 |  |

**recall**: O's answer 6, S's answer 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦ bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '4' |  | 1 | ' 4' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '4' |  | 1 | ' 4' |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 1 |  |
| no_part jpp26_100/75/slice | '4' |  | 1 |  |
| no_rand jpp26_100/75/slice | '4' |  | 1 |  |
| no_part ratoms75/75/scaled | '4' |  | 1 |  |
| no_rand ratoms75/75/scaled | '4' |  | 1 |  |
| no_part ratoms75own/75/own | '4' |  | 1 |  |
| no_rand ratoms75own/75/own | '4' |  | 1 |  |

#### P2-L0-0148: bridge nitrogen → carbon, token 48

**lookup**: O's answer 3, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked carbon. Carl picked⟦ nitrogen⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '3' |  | 0 | ' 3' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '3' |  | 0 | ' 3' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '3' |  | 0 |  |
| no_part jpp26_100/75/slice | '3' |  | 0 |  |
| no_rand jpp26_100/75/slice | '3' |  | 0 |  |
| no_part ratoms75/75/scaled | '3' |  | 0 |  |
| no_rand ratoms75/75/scaled | '3' |  | 0 |  |
| no_part ratoms75own/75/own | '3' |  | 0 |  |
| no_rand ratoms75own/75/own | '3' |  | 0 |  |

**recall**: O's answer 7, S's answer 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked carbon. Carl picked⟦ nitrogen⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
What is the atomic number of Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '6' |  | 1 | ' 6' |
| no_part jpp/25/signed | '7' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '6' |  | 1 | ' 6' |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 1 |  |
| no_part jpp26_100/75/slice | '6' |  | 1 |  |
| no_rand jpp26_100/75/slice | '6' |  | 1 |  |
| no_part ratoms75/75/scaled | '6' |  | 1 |  |
| no_rand ratoms75/75/scaled | '6' |  | 1 |  |
| no_part ratoms75own/75/own | '6' |  | 1 |  |
| no_rand ratoms75own/75/own | '6' |  | 1 |  |

#### P2-L0-0155: bridge beta → epsilon, token 44

**lookup**: O's answer 5, S's answer 1

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '5' |  | 0 |  |
| whole | '5' |  | 0 | ' 5' |
| no_part jpp/25/signed | '5' |  | 0 | ' 5' |
| no_rand jpp/25/signed | '5' |  | 0 | ' 5' |
| no_part jpp/100/signed | '5' |  | 0 |  |
| no_rand jpp/100/signed | '5' |  | 0 |  |
| no_part jpp26_100/75/slice | '5' |  | 0 |  |
| no_rand jpp26_100/75/slice | '5' |  | 0 |  |
| no_part ratoms75/75/scaled | '5' |  | 0 |  |
| no_rand ratoms75/75/scaled | '5' |  | 0 |  |
| no_part ratoms75own/75/own | '5' |  | 0 |  |
| no_rand ratoms75own/75/own | '5' |  | 0 |  |

**recall**: O's answer 2, S's answer 5

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which position in the Greek alphabet does Maria's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '2' |  | 0 |  |
| whole | '2' |  | 0 | ' 2' |
| no_part jpp/25/signed | '2' |  | 0 | ' 2' |
| no_rand jpp/25/signed | '2' |  | 0 | ' 2' |
| no_part jpp/100/signed | '2' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 0 |  |
| no_part jpp26_100/75/slice | '2' |  | 0 |  |
| no_rand jpp26_100/75/slice | '2' |  | 0 |  |
| no_part ratoms75/75/scaled | '2' |  | 0 |  |
| no_rand ratoms75/75/scaled | '2' |  | 0 |  |
| no_part ratoms75own/75/own | '2' |  | 0 |  |
| no_rand ratoms75own/75/own | '2' |  | 0 |  |

#### P2-L0-0175: bridge lithium → carbon, token 58

**lookup**: O's answer 9, S's answer 1

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. Mia picked⟦ lithium⟧. Liam picked carbon. Adam picked hydrogen. The locker of carbon is one.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '9' |  | 0 |  |
| whole | '9' |  | 0 | ' 9' |
| no_part jpp/25/signed | '9' |  | 0 | ' 9' |
| no_rand jpp/25/signed | '9' |  | 0 | ' 9' |
| no_part jpp/100/signed | '9' |  | 0 |  |
| no_rand jpp/100/signed | '9' |  | 0 |  |
| no_part jpp26_100/75/slice | '9' |  | 0 |  |
| no_rand jpp26_100/75/slice | '9' |  | 0 |  |
| no_part ratoms75/75/scaled | '9' |  | 0 |  |
| no_rand ratoms75/75/scaled | '9' |  | 0 |  |
| no_part ratoms75own/75/own | '9' |  | 0 |  |
| no_rand ratoms75own/75/own | '9' |  | 0 |  |

**recall**: O's answer 3, S's answer 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. Mia picked⟦ lithium⟧. Liam picked carbon. Adam picked hydrogen. The locker of carbon is one.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '3' |  | 0 |  |
| whole | '6' |  | 1 | ' 6' |
| no_part jpp/25/signed | '3' |  | 0 | ' 3' |
| no_rand jpp/25/signed | '6' |  | 1 | ' 6' |
| no_part jpp/100/signed | '3' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 1 |  |
| no_part jpp26_100/75/slice | '6' |  | 1 |  |
| no_rand jpp26_100/75/slice | '6' |  | 1 |  |
| no_part ratoms75/75/scaled | '6' |  | 1 |  |
| no_rand ratoms75/75/scaled | '6' |  | 1 |  |
| no_part ratoms75own/75/own | '6' |  | 1 |  |
| no_rand ratoms75own/75/own | '6' |  | 1 |  |

#### P2-L0-0178: bridge carbon → oxygen, token 51

**lookup**: O's answer 7, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. Lily picked⟦ carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '7' |  | 0 | ' 7' |
| no_part jpp/25/signed | '7' |  | 0 | ' 7' |
| no_rand jpp/25/signed | '7' |  | 0 | ' 7' |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '7' |  | 0 |  |
| no_part jpp26_100/75/slice | '7' |  | 0 |  |
| no_rand jpp26_100/75/slice | '7' |  | 0 |  |
| no_part ratoms75/75/scaled | '7' |  | 0 |  |
| no_rand ratoms75/75/scaled | '7' |  | 0 |  |
| no_part ratoms75own/75/own | '7' |  | 0 |  |
| no_rand ratoms75own/75/own | '7' |  | 0 |  |

**recall**: O's answer 6, S's answer 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. Lily picked⟦ carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
What is the atomic number of Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '8' |  | 1 | ' 8' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '8' |  | 1 | ' 8' |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '8' |  | 1 |  |
| no_part jpp26_100/75/slice | '8' |  | 1 |  |
| no_rand jpp26_100/75/slice | '8' |  | 1 |  |
| no_part ratoms75/75/scaled | '8' |  | 1 |  |
| no_rand ratoms75/75/scaled | '8' |  | 1 |  |
| no_part ratoms75own/75/own | '8' |  | 1 |  |
| no_rand ratoms75own/75/own | '8' |  | 1 |  |

#### P2-L0-0187: bridge hydrogen → helium, token 56

**lookup**: O's answer 6, S's answer 1

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. Nina picked⟦ hydrogen⟧. Maria picked helium. The locker of hydrogen is 6. The locker of lithium is 2.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '6' |  | 0 |  |
| whole | '6' |  | 0 | ' 6' |
| no_part jpp/25/signed | '6' |  | 0 | ' 6' |
| no_rand jpp/25/signed | '6' |  | 0 | ' 6' |
| no_part jpp/100/signed | '6' |  | 0 |  |
| no_rand jpp/100/signed | '6' |  | 0 |  |
| no_part jpp26_100/75/slice | '6' |  | 0 |  |
| no_rand jpp26_100/75/slice | '6' |  | 0 |  |
| no_part ratoms75/75/scaled | '6' |  | 0 |  |
| no_rand ratoms75/75/scaled | '6' |  | 0 |  |
| no_part ratoms75own/75/own | '6' |  | 0 |  |
| no_rand ratoms75own/75/own | '6' |  | 0 |  |

**recall**: O's answer 1, S's answer 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. Nina picked⟦ hydrogen⟧. Maria picked helium. The locker of hydrogen is 6. The locker of lithium is 2.
What is the atomic number of Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '1' |  | 0 |  |
| whole | '1' |  | 0 | ' 1' |
| no_part jpp/25/signed | '1' |  | 0 | ' 1' |
| no_rand jpp/25/signed | '2' |  | 1 | ' 2' |
| no_part jpp/100/signed | '1' |  | 0 |  |
| no_rand jpp/100/signed | '2' |  | 1 |  |
| no_part jpp26_100/75/slice | '1' |  | 0 |  |
| no_rand jpp26_100/75/slice | '2' |  | 1 |  |
| no_part ratoms75/75/scaled | '1' |  | 0 |  |
| no_rand ratoms75/75/scaled | '2' |  | 1 |  |
| no_part ratoms75own/75/own | '1' |  | 0 |  |
| no_rand ratoms75own/75/own | '1' |  | 0 |  |

#### P2-L0-0284: bridge delta → epsilon, token 44

**lookup**: O's answer 7, S's answer 3

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '7' |  | 0 |  |
| whole | '7' |  | 0 | ' 7' |
| no_part jpp/25/signed | '7' |  | 0 | ' 7' |
| no_rand jpp/25/signed | '7' |  | 0 | ' 7' |
| no_part jpp/100/signed | '7' |  | 0 |  |
| no_rand jpp/100/signed | '7' |  | 0 |  |
| no_part jpp26_100/75/slice | '7' |  | 0 |  |
| no_rand jpp26_100/75/slice | '7' |  | 0 |  |
| no_part ratoms75/75/scaled | '7' |  | 0 |  |
| no_rand ratoms75/75/scaled | '7' |  | 0 |  |
| no_part ratoms75own/75/own | '7' |  | 0 |  |
| no_rand ratoms75own/75/own | '7' |  | 0 |  |

**recall**: O's answer 4, S's answer 5

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer (top token) | route | switched | greedy |
|---|---|---|---|---|
| none | '4' |  | 0 |  |
| whole | '4' |  | 0 | ' 4' |
| no_part jpp/25/signed | '4' |  | 0 | ' 4' |
| no_rand jpp/25/signed | '4' |  | 0 | ' 4' |
| no_part jpp/100/signed | '4' |  | 0 |  |
| no_rand jpp/100/signed | '4' |  | 0 |  |
| no_part jpp26_100/75/slice | '4' |  | 0 |  |
| no_rand jpp26_100/75/slice | '4' |  | 0 |  |
| no_part ratoms75/75/scaled | '4' |  | 0 |  |
| no_rand ratoms75/75/scaled | '4' |  | 0 |  |
| no_part ratoms75own/75/own | '4' |  | 0 |  |
| no_rand ratoms75own/75/own | '4' |  | 0 |  |

