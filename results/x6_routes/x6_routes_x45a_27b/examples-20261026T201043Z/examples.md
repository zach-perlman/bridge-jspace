# Examples: x6_routes_x45a_27b

10 random items of 1500 (seed 0); model qwen3.6-27b, layer 32, rendering chat. The change h_S - h_O (or the arm's part of it) is added at ⟦...⟧ in O; the read is the top token after a space token appended to O. UNVERIFIED.

## 1. C2-0245-V3 (C2, V3: 'Fiona picked the butterfly.')

O bridge 'frog', S bridge 'spider', token 39; expected digits {'identity': 3, 'position': 5, 'value': 9, 'original': 6}; pointer move 2 -> 0.

### lookup (PP): O answers 6, S answers 9

O, as read:

```
<|im_start|>user
Fiona picked the butterfly. The locker of the deer is 5. The locker of the spider is 3. The locker of the frog is 6. Carl picked the⟦ frog⟧. Tom picked the deer. Finn picked the spider.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Fiona picked the butterfly. The locker of the spider is 9. The locker of the deer is 5. The locker of the frog is 6. Carl picked the⟦ spider⟧. Tom picked the deer. Finn picked the spider.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '6' | original | 0 |
| whole | '3' | identity | 0 |
| keep_alf | '6' | original | 0 |
| keep_alf_rand | '6' | original | 0 |
| no_alf | '3' | identity | 0 |
| no_alf_rand | '3' | identity | 0 |

### recall (PM): O answers 4, S answers 8

O, as read:

```
<|im_start|>user
Fiona picked the butterfly. The locker of the deer is 5. The locker of the spider is 3. The locker of the frog is 6. Carl picked the⟦ frog⟧. Tom picked the deer. Finn picked the spider.
How many legs does Carl's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Fiona picked the butterfly. The locker of the spider is 9. The locker of the deer is 5. The locker of the frog is 6. Carl picked the⟦ spider⟧. Tom picked the deer. Finn picked the spider.
How many legs does Carl's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '8' |  | 1 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '8' |  | 1 |
| no_alf_rand | '8' |  | 1 |

## 2. C2-0271-V1 (C2, V1: 'Paul picked the pig.')

O bridge 'pig', S bridge 'chicken', token 38; expected digits {'identity': 1, 'position': 6, 'value': 7, 'original': 4}; pointer move 0 -> 1.

### lookup (PP): O answers 4, S answers 7

O, as read:

```
<|im_start|>user
Paul picked the pig. The locker of the pig is 4. The locker of the bear is 6. The locker of the chicken is 1. Beth picked the⟦ pig⟧. David picked the bear. Oscar picked the chicken.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Paul picked the pig. The locker of the pig is 4. The locker of the chicken is 7. The locker of the bear is 6. Beth picked the⟦ chicken⟧. David picked the bear. Oscar picked the chicken.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '1' | identity | 0 |
| keep_alf | '4' | original | 0 |
| keep_alf_rand | '4' | original | 0 |
| no_alf | '1' | identity | 0 |
| no_alf_rand | '1' | identity | 0 |

### recall (PM): O answers 4, S answers 2

O, as read:

```
<|im_start|>user
Paul picked the pig. The locker of the pig is 4. The locker of the bear is 6. The locker of the chicken is 1. Beth picked the⟦ pig⟧. David picked the bear. Oscar picked the chicken.
How many legs does Beth's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Paul picked the pig. The locker of the pig is 4. The locker of the chicken is 7. The locker of the bear is 6. Beth picked the⟦ chicken⟧. David picked the bear. Oscar picked the chicken.
How many legs does Beth's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '2' |  | 1 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '2' |  | 1 |

## 3. C2-0022-V2 (C2, V2: 'Lucy picked the tick.')

O bridge 'tick', S bridge 'duck', token 49; expected digits {'identity': 7, 'position': 8, 'value': 3, 'original': 4}; pointer move 1 -> 0.

### lookup (PP): O answers 4, S answers 3

O, as read:

```
<|im_start|>user
Lucy picked the tick. The locker of the frog is 8. The locker of the tick is 4. The locker of the duck is 7. Tom picked the duck. Frank picked the frog. Rose picked the⟦ tick⟧.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Lucy picked the tick. The locker of the duck is 3. The locker of the tick is 4. The locker of the frog is 8. Tom picked the duck. Frank picked the frog. Rose picked the⟦ duck⟧.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '7' | identity | 0 |
| keep_alf | '4' | original | 0 |
| keep_alf_rand | '4' | original | 0 |
| no_alf | '7' | identity | 0 |
| no_alf_rand | '7' | identity | 0 |

### recall (PM): O answers 8, S answers 2

O, as read:

```
<|im_start|>user
Lucy picked the tick. The locker of the frog is 8. The locker of the tick is 4. The locker of the duck is 7. Tom picked the duck. Frank picked the frog. Rose picked the⟦ tick⟧.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Lucy picked the tick. The locker of the duck is 3. The locker of the tick is 4. The locker of the frog is 8. Tom picked the duck. Frank picked the frog. Rose picked the⟦ duck⟧.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '8' |  | 0 |
| whole | '8' |  | 0 |
| keep_alf | '8' |  | 0 |
| keep_alf_rand | '8' |  | 0 |
| no_alf | '8' |  | 0 |
| no_alf_rand | '8' |  | 0 |

## 4. C2-0166-V0 (C2, V0: '')

O bridge 'cat', S bridge 'eagle', token 33; expected digits {'identity': 2, 'position': 4, 'value': 3, 'original': 6}; pointer move 2 -> 0.

### lookup (PP): O answers 6, S answers 3

O, as read:

```
<|im_start|>user
The locker of the pig is 4. The locker of the eagle is 2. The locker of the cat is 6. Paul picked the⟦ cat⟧. Jack picked the pig. Lily picked the eagle.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 3. The locker of the pig is 4. The locker of the cat is 6. Paul picked the⟦ eagle⟧. Jack picked the pig. Lily picked the eagle.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '6' | original | 0 |
| whole | '4' | position | 0 |
| keep_alf | '6' | original | 0 |
| keep_alf_rand | '6' | original | 0 |
| no_alf | '2' | identity | 0 |
| no_alf_rand | '4' | position | 0 |

### recall (PM): O answers 4, S answers 2

O, as read:

```
<|im_start|>user
The locker of the pig is 4. The locker of the eagle is 2. The locker of the cat is 6. Paul picked the⟦ cat⟧. Jack picked the pig. Lily picked the eagle.
How many legs does Paul's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
The locker of the eagle is 3. The locker of the pig is 4. The locker of the cat is 6. Paul picked the⟦ eagle⟧. Jack picked the pig. Lily picked the eagle.
How many legs does Paul's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '4' |  | 0 |

## 5. C2-0339-V2 (C2, V2: 'Ben picked the frog.')

O bridge 'frog', S bridge 'owl', token 38; expected digits {'identity': 3, 'position': 8, 'value': 7, 'original': 1}; pointer move 1 -> 0.

### lookup (PP): O answers 1, S answers 7

O, as read:

```
<|im_start|>user
Ben picked the frog. The locker of the duck is 8. The locker of the frog is 1. The locker of the owl is 3. Julia picked the⟦ frog⟧. Lucy picked the duck. Henry picked the owl.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Ben picked the frog. The locker of the owl is 7. The locker of the frog is 1. The locker of the duck is 8. Julia picked the⟦ owl⟧. Lucy picked the duck. Henry picked the owl.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '1' | original | 0 |
| whole | '3' | identity | 0 |
| keep_alf | '1' | original | 0 |
| keep_alf_rand | '1' | original | 0 |
| no_alf | '3' | identity | 0 |
| no_alf_rand | '3' | identity | 0 |

### recall (PM): O answers 4, S answers 2

O, as read:

```
<|im_start|>user
Ben picked the frog. The locker of the duck is 8. The locker of the frog is 1. The locker of the owl is 3. Julia picked the⟦ frog⟧. Lucy picked the duck. Henry picked the owl.
How many legs does Julia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Ben picked the frog. The locker of the owl is 7. The locker of the frog is 1. The locker of the duck is 8. Julia picked the⟦ owl⟧. Lucy picked the duck. Henry picked the owl.
How many legs does Julia's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |

## 6. C2-0325-V0 (C2, V0: '')

O bridge 'bear', S bridge 'fly', token 33; expected digits {'identity': 1, 'position': 6, 'value': 2, 'original': 8}; pointer move 2 -> 1.

### lookup (PP): O answers 8, S answers 2

O, as read:

```
<|im_start|>user
The locker of the fly is 1. The locker of the goat is 6. The locker of the bear is 8. Eva picked the⟦ bear⟧. David picked the fly. Mia picked the goat.
Which locker belongs to Eva's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
The locker of the goat is 6. The locker of the fly is 2. The locker of the bear is 8. Eva picked the⟦ fly⟧. David picked the fly. Mia picked the goat.
Which locker belongs to Eva's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '8' | original | 0 |
| whole | '6' | position | 0 |
| keep_alf | '8' | original | 0 |
| keep_alf_rand | '8' | original | 0 |
| no_alf | '1' | identity | 0 |
| no_alf_rand | '6' | position | 0 |

### recall (PM): O answers 4, S answers 6

O, as read:

```
<|im_start|>user
The locker of the fly is 1. The locker of the goat is 6. The locker of the bear is 8. Eva picked the⟦ bear⟧. David picked the fly. Mia picked the goat.
How many legs does Eva's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
The locker of the goat is 6. The locker of the fly is 2. The locker of the bear is 8. Eva picked the⟦ fly⟧. David picked the fly. Mia picked the goat.
How many legs does Eva's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '6' |  | 1 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '6' |  | 1 |
| no_alf_rand | '6' |  | 1 |

## 7. C2-0259-V4 (C2, V4: 'Nobody could remember when the hallway lights had last been changed.')

O bridge 'ant', S bridge 'elephant', token 50; expected digits {'identity': 1, 'position': 7, 'value': 8, 'original': 2}; pointer move 0 -> 1.

### lookup (PP): O answers 2, S answers 8

O, as read:

```
<|im_start|>user
Nobody could remember when the hallway lights had last been changed. The locker of the ant is 2. The locker of the crow is 7. The locker of the elephant is 1. Ben picked the elephant. Henry picked the⟦ ant⟧. Alice picked the crow.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Nobody could remember when the hallway lights had last been changed. The locker of the ant is 2. The locker of the elephant is 8. The locker of the crow is 7. Ben picked the elephant. Henry picked the⟦ elephant⟧. Alice picked the crow.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '2' | original | 0 |
| whole | '1' | identity | 0 |
| keep_alf | '2' | original | 0 |
| keep_alf_rand | '2' | original | 0 |
| no_alf | '1' | identity | 0 |
| no_alf_rand | '1' | identity | 0 |

### recall (PM): O answers 6, S answers 4

O, as read:

```
<|im_start|>user
Nobody could remember when the hallway lights had last been changed. The locker of the ant is 2. The locker of the crow is 7. The locker of the elephant is 1. Ben picked the elephant. Henry picked the⟦ ant⟧. Alice picked the crow.
How many legs does Henry's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Nobody could remember when the hallway lights had last been changed. The locker of the ant is 2. The locker of the elephant is 8. The locker of the crow is 7. Ben picked the elephant. Henry picked the⟦ elephant⟧. Alice picked the crow.
How many legs does Henry's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '6' |  | 0 |
| whole | '4' |  | 1 |
| keep_alf | '6' |  | 0 |
| keep_alf_rand | '6' |  | 0 |
| no_alf | '4' |  | 1 |
| no_alf_rand | '4' |  | 1 |

## 8. C2-0194-V1 (C2, V1: 'Diana picked the fly.')

O bridge 'fly', S bridge 'bear', token 39; expected digits {'identity': 3, 'position': 6, 'value': 2, 'original': 8}; pointer move 0 -> 2.

### lookup (PP): O answers 8, S answers 2

O, as read:

```
<|im_start|>user
Diana picked the fly. The locker of the fly is 8. The locker of the bear is 3. The locker of the sheep is 6. Mark picked the⟦ fly⟧. Sam picked the sheep. Ivy picked the bear.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Diana picked the fly. The locker of the fly is 8. The locker of the sheep is 6. The locker of the bear is 2. Mark picked the⟦ bear⟧. Sam picked the sheep. Ivy picked the bear.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '8' | original | 0 |
| whole | '3' | identity | 0 |
| keep_alf | '8' | original | 0 |
| keep_alf_rand | '8' | original | 0 |
| no_alf | '3' | identity | 0 |
| no_alf_rand | '3' | identity | 0 |

### recall (PM): O answers 6, S answers 4

O, as read:

```
<|im_start|>user
Diana picked the fly. The locker of the fly is 8. The locker of the bear is 3. The locker of the sheep is 6. Mark picked the⟦ fly⟧. Sam picked the sheep. Ivy picked the bear.
How many legs does Mark's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Diana picked the fly. The locker of the fly is 8. The locker of the sheep is 6. The locker of the bear is 2. Mark picked the⟦ bear⟧. Sam picked the sheep. Ivy picked the bear.
How many legs does Mark's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '6' |  | 0 |
| whole | '6' |  | 0 |
| keep_alf | '6' |  | 0 |
| keep_alf_rand | '6' |  | 0 |
| no_alf | '6' |  | 0 |
| no_alf_rand | '6' |  | 0 |

## 9. C2-0319-V1 (C2, V1: 'Leo picked the fly.')

O bridge 'owl', S bridge 'fly', token 43; expected digits {'identity': 5, 'position': 3, 'value': 4, 'original': 7}; pointer move 1 -> 2.

### lookup (PP): O answers 7, S answers 4

O, as read:

```
<|im_start|>user
Leo picked the fly. The locker of the fly is 5. The locker of the owl is 7. The locker of the ant is 3. Max picked the fly. James picked the⟦ owl⟧. Olivia picked the ant.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Leo picked the fly. The locker of the ant is 3. The locker of the owl is 7. The locker of the fly is 4. Max picked the fly. James picked the⟦ fly⟧. Olivia picked the ant.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '5' | identity | 0 |
| keep_alf | '7' | original | 0 |
| keep_alf_rand | '7' | original | 0 |
| no_alf | '5' | identity | 0 |
| no_alf_rand | '5' | identity | 0 |

### recall (PM): O answers 2, S answers 6

O, as read:

```
<|im_start|>user
Leo picked the fly. The locker of the fly is 5. The locker of the owl is 7. The locker of the ant is 3. Max picked the fly. James picked the⟦ owl⟧. Olivia picked the ant.
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Leo picked the fly. The locker of the ant is 3. The locker of the owl is 7. The locker of the fly is 4. Max picked the fly. James picked the⟦ fly⟧. Olivia picked the ant.
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '6' |  | 1 |
| keep_alf | '2' |  | 0 |
| keep_alf_rand | '2' |  | 0 |
| no_alf | '6' |  | 1 |
| no_alf_rand | '6' |  | 1 |

## 10. C2-0229-V3 (C2, V3: 'Max picked the cow.')

O bridge 'ant', S bridge 'wolf', token 43; expected digits {'identity': 4, 'position': 3, 'value': 2, 'original': 7}; pointer move 1 -> 0.

### lookup (PP): O answers 7, S answers 2

O, as read:

```
<|im_start|>user
Max picked the cow. The locker of the bear is 3. The locker of the ant is 7. The locker of the wolf is 4. Maria picked the wolf. Sam picked the⟦ ant⟧. Eric picked the bear.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Max picked the cow. The locker of the wolf is 2. The locker of the ant is 7. The locker of the bear is 3. Maria picked the wolf. Sam picked the⟦ wolf⟧. Eric picked the bear.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '4' | identity | 0 |
| keep_alf | '7' | original | 0 |
| keep_alf_rand | '7' | original | 0 |
| no_alf | '4' | identity | 0 |
| no_alf_rand | '4' | identity | 0 |

### recall (PM): O answers 6, S answers 4

O, as read:

```
<|im_start|>user
Max picked the cow. The locker of the bear is 3. The locker of the ant is 7. The locker of the wolf is 4. Maria picked the wolf. Sam picked the⟦ ant⟧. Eric picked the bear.
How many legs does Sam's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

S (the source):

```
<|im_start|>user
Max picked the cow. The locker of the wolf is 2. The locker of the ant is 7. The locker of the bear is 3. Maria picked the wolf. Sam picked the⟦ wolf⟧. Eric picked the bear.
How many legs does Sam's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '6' |  | 0 |
| whole | '6' |  | 0 |
| keep_alf | '6' |  | 0 |
| keep_alf_rand | '6' |  | 0 |
| no_alf | '6' |  | 0 |
| no_alf_rand | '6' |  | 0 |

