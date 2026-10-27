# Examples: muse30b_x6_routes_x45a

10 random items of 1500 (seed 0); model muse-glimmer-30b, layer 26, rendering chat. The change h_S - h_O (or the arm's part of it) is added at ⟦...⟧ in O; the read is the top token after a space token appended to O. UNVERIFIED.

## 1. C2-0402-V3 (C2, V3: 'Sara picked the cat.')

O bridge 'dog', S bridge 'turkey', token 77; expected digits {'identity': 1, 'position': 2, 'value': 7, 'original': 9}; pointer move 0 -> 2.

### lookup (PP): O answers 9, S answers 7

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Sara picked the cat. The locker of the dog is 9. The locker of the turkey is 1. The locker of the fly is 2. Sean picked the⟦ dog⟧. Jack picked the turkey. Finn picked the fly.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Sara picked the cat. The locker of the dog is 9. The locker of the fly is 2. The locker of the turkey is 7. Sean picked the⟦ turkey⟧. Jack picked the turkey. Finn picked the fly.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '9' | original | 0 |
| whole | '1' | identity | 0 |
| keep_alf | '9' | original | 0 |
| keep_alf_rand | '9' | original | 0 |
| no_alf | '1' | identity | 0 |
| no_alf_rand | '1' | identity | 0 |

### recall (PM): O answers 4, S answers 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Sara picked the cat. The locker of the dog is 9. The locker of the turkey is 1. The locker of the fly is 2. Sean picked the⟦ dog⟧. Jack picked the turkey. Finn picked the fly.
How many legs does Sean's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Sara picked the cat. The locker of the dog is 9. The locker of the fly is 2. The locker of the turkey is 7. Sean picked the⟦ turkey⟧. Jack picked the turkey. Finn picked the fly.
How many legs does Sean's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '2' |  | 1 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '2' |  | 1 |

## 2. C2-0442-V1 (C2, V1: 'Frank picked the bee.')

O bridge 'pig', S bridge 'bee', token 82; expected digits {'identity': 9, 'position': 8, 'value': 7, 'original': 4}; pointer move 1 -> 2.

### lookup (PP): O answers 4, S answers 7

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked the bee. The locker of the bee is 9. The locker of the pig is 4. The locker of the owl is 8. Mark picked the bee. Zoe picked the⟦ pig⟧. Peter picked the owl.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked the bee. The locker of the owl is 8. The locker of the pig is 4. The locker of the bee is 7. Mark picked the bee. Zoe picked the⟦ bee⟧. Peter picked the owl.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '9' | identity | 0 |
| keep_alf | '4' | original | 0 |
| keep_alf_rand | '4' | original | 0 |
| no_alf | '9' | identity | 0 |
| no_alf_rand | '9' | identity | 0 |

### recall (PM): O answers 4, S answers 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked the bee. The locker of the bee is 9. The locker of the pig is 4. The locker of the owl is 8. Mark picked the bee. Zoe picked the⟦ pig⟧. Peter picked the owl.
How many legs does Zoe's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked the bee. The locker of the owl is 8. The locker of the pig is 4. The locker of the bee is 7. Mark picked the bee. Zoe picked the⟦ bee⟧. Peter picked the owl.
How many legs does Zoe's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |

## 3. C2-0038-V2 (C2, V2: 'Zoe picked the tick.')

O bridge 'duck', S bridge 'elephant', token 83; expected digits {'identity': 8, 'position': 2, 'value': 6, 'original': 5}; pointer move 2 -> 1.

### lookup (PP): O answers 5, S answers 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Zoe picked the tick. The locker of the elephant is 8. The locker of the tick is 2. The locker of the duck is 5. Tom picked the elephant. Julia picked the⟦ duck⟧. Eric picked the tick.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Zoe picked the tick. The locker of the tick is 2. The locker of the elephant is 6. The locker of the duck is 5. Tom picked the elephant. Julia picked the⟦ elephant⟧. Eric picked the tick.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '5' | original | 0 |
| whole | '8' | identity | 0 |
| keep_alf | '5' | original | 0 |
| keep_alf_rand | '5' | original | 0 |
| no_alf | '8' | identity | 0 |
| no_alf_rand | '8' | identity | 0 |

### recall (PM): O answers 2, S answers 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Zoe picked the tick. The locker of the elephant is 8. The locker of the tick is 2. The locker of the duck is 5. Tom picked the elephant. Julia picked the⟦ duck⟧. Eric picked the tick.
How many legs does Julia's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Zoe picked the tick. The locker of the tick is 2. The locker of the elephant is 6. The locker of the duck is 5. Tom picked the elephant. Julia picked the⟦ elephant⟧. Eric picked the tick.
How many legs does Julia's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '2' |  | 0 |
| keep_alf | '2' |  | 0 |
| keep_alf_rand | '2' |  | 0 |
| no_alf | '2' |  | 0 |
| no_alf_rand | '2' |  | 0 |

## 4. C2-0272-V0 (C2, V0: '')

O bridge 'ant', S bridge 'sheep', token 77; expected digits {'identity': 6, 'position': 9, 'value': 8, 'original': 5}; pointer move 1 -> 2.

### lookup (PP): O answers 5, S answers 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the sheep is 6. The locker of the ant is 5. The locker of the pig is 9. Iris picked the pig. Eve picked the⟦ ant⟧. Carl picked the sheep.
Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the pig is 9. The locker of the ant is 5. The locker of the sheep is 8. Iris picked the pig. Eve picked the⟦ sheep⟧. Carl picked the sheep.
Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '5' | original | 0 |
| whole | '9' | position | 0 |
| keep_alf | '9' | position | 0 |
| keep_alf_rand | '5' | original | 0 |
| no_alf | '9' | position | 0 |
| no_alf_rand | '9' | position | 0 |

### recall (PM): O answers 6, S answers 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the sheep is 6. The locker of the ant is 5. The locker of the pig is 9. Iris picked the pig. Eve picked the⟦ ant⟧. Carl picked the sheep.
How many legs does Eve's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the pig is 9. The locker of the ant is 5. The locker of the sheep is 8. Iris picked the pig. Eve picked the⟦ sheep⟧. Carl picked the sheep.
How many legs does Eve's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '6' |  | 0 |
| whole | '6' |  | 0 |
| keep_alf | '6' |  | 0 |
| keep_alf_rand | '6' |  | 0 |
| no_alf | '6' |  | 0 |
| no_alf_rand | '6' |  | 0 |

## 5. C2-0527-V2 (C2, V2: 'Emma picked the deer.')

O bridge 'turkey', S bridge 'goat', token 87; expected digits {'identity': 3, 'position': 4, 'value': 5, 'original': 9}; pointer move 0 -> 1.

### lookup (PP): O answers 9, S answers 5

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked the deer. The locker of the turkey is 9. The locker of the deer is 4. The locker of the goat is 3. Dan picked the deer. Diana picked the goat. Ivy picked the⟦ turkey⟧.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked the deer. The locker of the turkey is 9. The locker of the goat is 5. The locker of the deer is 4. Dan picked the deer. Diana picked the goat. Ivy picked the⟦ goat⟧.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '9' | original | 0 |
| whole | '4' | position | 0 |
| keep_alf | '9' | original | 0 |
| keep_alf_rand | '9' | original | 0 |
| no_alf | '4' | position | 0 |
| no_alf_rand | '4' | position | 0 |

### recall (PM): O answers 2, S answers 4

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked the deer. The locker of the turkey is 9. The locker of the deer is 4. The locker of the goat is 3. Dan picked the deer. Diana picked the goat. Ivy picked the⟦ turkey⟧.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked the deer. The locker of the turkey is 9. The locker of the goat is 5. The locker of the deer is 4. Dan picked the deer. Diana picked the goat. Ivy picked the⟦ goat⟧.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '2' |  | 0 |
| whole | '2' |  | 0 |
| keep_alf | '2' |  | 0 |
| keep_alf_rand | '2' |  | 0 |
| no_alf | '2' |  | 0 |
| no_alf_rand | '2' |  | 0 |

## 6. C2-0509-V0 (C2, V0: '')

O bridge 'frog', S bridge 'chicken', token 82; expected digits {'identity': 5, 'position': 6, 'value': 8, 'original': 1}; pointer move 0 -> 1.

### lookup (PP): O answers 1, S answers 8

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the frog is 1. The locker of the eagle is 6. The locker of the chicken is 5. Ruby picked the chicken. Tom picked the eagle. Hugo picked the⟦ frog⟧.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the frog is 1. The locker of the chicken is 8. The locker of the eagle is 6. Ruby picked the chicken. Tom picked the eagle. Hugo picked the⟦ chicken⟧.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '1' | original | 0 |
| whole | '5' | identity | 0 |
| keep_alf | '1' | original | 0 |
| keep_alf_rand | '1' | original | 0 |
| no_alf | '5' | identity | 0 |
| no_alf_rand | '5' | identity | 0 |

### recall (PM): O answers 4, S answers 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the frog is 1. The locker of the eagle is 6. The locker of the chicken is 5. Ruby picked the chicken. Tom picked the eagle. Hugo picked the⟦ frog⟧.
How many legs does Hugo's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the frog is 1. The locker of the chicken is 8. The locker of the eagle is 6. Ruby picked the chicken. Tom picked the eagle. Hugo picked the⟦ chicken⟧.
How many legs does Hugo's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '2' |  | 1 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '2' |  | 1 |

## 7. C2-0420-V4 (C2, V4: 'Nobody could remember when the hallway lights had last been changed.')

O bridge 'cow', S bridge 'fly', token 90; expected digits {'identity': 8, 'position': 1, 'value': 6, 'original': 5}; pointer move 2 -> 1.

### lookup (PP): O answers 5, S answers 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Nobody could remember when the hallway lights had last been changed. The locker of the fly is 8. The locker of the fox is 1. The locker of the cow is 5. Ruby picked the fox. Amy picked the⟦ cow⟧. Olivia picked the fly.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Nobody could remember when the hallway lights had last been changed. The locker of the fox is 1. The locker of the fly is 6. The locker of the cow is 5. Ruby picked the fox. Amy picked the⟦ fly⟧. Olivia picked the fly.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '5' | original | 0 |
| whole | '1' | position | 0 |
| keep_alf | '1' | position | 0 |
| keep_alf_rand | '5' | original | 0 |
| no_alf | '1' | position | 0 |
| no_alf_rand | '1' | position | 0 |

### recall (PM): O answers 4, S answers 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Nobody could remember when the hallway lights had last been changed. The locker of the fly is 8. The locker of the fox is 1. The locker of the cow is 5. Ruby picked the fox. Amy picked the⟦ cow⟧. Olivia picked the fly.
How many legs does Amy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Nobody could remember when the hallway lights had last been changed. The locker of the fox is 1. The locker of the fly is 6. The locker of the cow is 5. Ruby picked the fox. Amy picked the⟦ fly⟧. Olivia picked the fly.
How many legs does Amy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |

## 8. C2-0320-V1 (C2, V1: 'Emma picked the elephant.')

O bridge 'tiger', S bridge 'bee', token 82; expected digits {'identity': 2, 'position': 1, 'value': 6, 'original': 7}; pointer move 1 -> 0.

### lookup (PP): O answers 7, S answers 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked the elephant. The locker of the elephant is 1. The locker of the tiger is 7. The locker of the bee is 2. Owen picked the bee. Dan picked the⟦ tiger⟧. Alice picked the elephant.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked the elephant. The locker of the bee is 6. The locker of the tiger is 7. The locker of the elephant is 1. Owen picked the bee. Dan picked the⟦ bee⟧. Alice picked the elephant.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '7' | original | 0 |
| whole | '2' | identity | 0 |
| keep_alf | '7' | original | 0 |
| keep_alf_rand | '7' | original | 0 |
| no_alf | '2' | identity | 0 |
| no_alf_rand | '2' | identity | 0 |

### recall (PM): O answers 4, S answers 6

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked the elephant. The locker of the elephant is 1. The locker of the tiger is 7. The locker of the bee is 2. Owen picked the bee. Dan picked the⟦ tiger⟧. Alice picked the elephant.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked the elephant. The locker of the bee is 6. The locker of the tiger is 7. The locker of the elephant is 1. Owen picked the bee. Dan picked the⟦ bee⟧. Alice picked the elephant.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |

## 9. C2-0497-V1 (C2, V1: 'Hugo picked the tiger.')

O bridge 'wolf', S bridge 'eagle', token 83; expected digits {'identity': 4, 'position': 6, 'value': 7, 'original': 8}; pointer move 1 -> 0.

### lookup (PP): O answers 8, S answers 7

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Hugo picked the tiger. The locker of the tiger is 6. The locker of the wolf is 8. The locker of the eagle is 4. Leo picked the tiger. Clara picked the⟦ wolf⟧. Ben picked the eagle.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Hugo picked the tiger. The locker of the eagle is 7. The locker of the wolf is 8. The locker of the tiger is 6. Leo picked the tiger. Clara picked the⟦ eagle⟧. Ben picked the eagle.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '8' | original | 0 |
| whole | '6' | position | 0 |
| keep_alf | '8' | original | 0 |
| keep_alf_rand | '8' | original | 0 |
| no_alf | '8' | original | 0 |
| no_alf_rand | '6' | position | 0 |

### recall (PM): O answers 4, S answers 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Hugo picked the tiger. The locker of the tiger is 6. The locker of the wolf is 8. The locker of the eagle is 4. Leo picked the tiger. Clara picked the⟦ wolf⟧. Ben picked the eagle.
How many legs does Clara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Hugo picked the tiger. The locker of the eagle is 7. The locker of the wolf is 8. The locker of the tiger is 6. Leo picked the tiger. Clara picked the⟦ eagle⟧. Ben picked the eagle.
How many legs does Clara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '4' |  | 0 |
| no_alf_rand | '4' |  | 0 |

## 10. C2-0373-V3 (C2, V3: 'Finn picked the pig.')

O bridge 'fox', S bridge 'crow', token 78; expected digits {'identity': 6, 'position': 8, 'value': 1, 'original': 4}; pointer move 2 -> 0.

### lookup (PP): O answers 4, S answers 1

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Finn picked the pig. The locker of the cow is 8. The locker of the crow is 6. The locker of the fox is 4. Grace picked the⟦ fox⟧. Olivia picked the crow. Adam picked the cow.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Finn picked the pig. The locker of the crow is 1. The locker of the cow is 8. The locker of the fox is 4. Grace picked the⟦ crow⟧. Olivia picked the crow. Adam picked the cow.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' | original | 0 |
| whole | '6' | identity | 0 |
| keep_alf | '4' | original | 0 |
| keep_alf_rand | '4' | original | 0 |
| no_alf | '6' | identity | 0 |
| no_alf_rand | '6' | identity | 0 |

### recall (PM): O answers 4, S answers 2

O, as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Finn picked the pig. The locker of the cow is 8. The locker of the crow is 6. The locker of the fox is 4. Grace picked the⟦ fox⟧. Olivia picked the crow. Adam picked the cow.
How many legs does Grace's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

S (the source):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Finn picked the pig. The locker of the crow is 1. The locker of the cow is 8. The locker of the fox is 4. Grace picked the⟦ crow⟧. Olivia picked the crow. Adam picked the cow.
How many legs does Grace's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

| arm | answer | route | switched |
|---|---|---|---|
| none | '4' |  | 0 |
| whole | '4' |  | 0 |
| keep_alf | '4' |  | 0 |
| keep_alf_rand | '4' |  | 0 |
| no_alf | '2' |  | 1 |
| no_alf_rand | '4' |  | 0 |

