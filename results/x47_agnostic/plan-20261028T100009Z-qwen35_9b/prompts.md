# 47.11 plan on qwen3.5-9b (L12): 5 rendered prompts per type (seed 0), as the model reads them; ⟦...⟧ the bridge word. Counts in plan.json.

## animals: 700 scenes generated; pool 32 items; recall: How many legs does {p}'s pick have?

### animals-0062 (bridge token 43; expected digits {'identity': 1, 'position': 9, 'value': 4, 'original': 6})

O: The locker of the beetle is 9. The locker of the chicken is 6. The locker of the horse is 1. Laura picked the beetle. Liam picked the horse. Eric picked the chicken.

S: The locker of the horse is 4. The locker of the chicken is 6. The locker of the beetle is 9. Laura picked the beetle. Liam picked the horse. Eric picked the horse.

**lookup** (Which locker belongs to Eric's pick?; O answers 6, S answers 4):

```
<|im_start|>user
The locker of the beetle is 9. The locker of the chicken is 6. The locker of the horse is 1. Laura picked the beetle. Liam picked the horse. Eric picked the⟦ chicken⟧.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (How many legs does Eric's pick have?; O answers 2, S answers 4):

```
<|im_start|>user
The locker of the beetle is 9. The locker of the chicken is 6. The locker of the horse is 1. Laura picked the beetle. Liam picked the horse. Eric picked the⟦ chicken⟧.
How many legs does Eric's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### animals-0465 (bridge token 43; expected digits {'identity': 2, 'position': 3, 'value': 7, 'original': 1})

O: The locker of the deer is 1. The locker of the beetle is 2. The locker of the dog is 3. Hugo picked the beetle. Olivia picked the dog. Emma picked the deer.

S: The locker of the deer is 1. The locker of the dog is 3. The locker of the beetle is 7. Hugo picked the beetle. Olivia picked the dog. Emma picked the beetle.

**lookup** (Which locker belongs to Emma's pick?; O answers 1, S answers 7):

```
<|im_start|>user
The locker of the deer is 1. The locker of the beetle is 2. The locker of the dog is 3. Hugo picked the beetle. Olivia picked the dog. Emma picked the⟦ deer⟧.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (How many legs does Emma's pick have?; O answers 4, S answers 6):

```
<|im_start|>user
The locker of the deer is 1. The locker of the beetle is 2. The locker of the dog is 3. Hugo picked the beetle. Olivia picked the dog. Emma picked the⟦ deer⟧.
How many legs does Emma's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### animals-0672 (bridge token 43; expected digits {'identity': 2, 'position': 4, 'value': 8, 'original': 9})

O: The locker of the spider is 9. The locker of the tiger is 4. The locker of the elephant is 2. Amy picked the tiger. Rose picked the elephant. Iris picked the spider.

S: The locker of the spider is 9. The locker of the elephant is 8. The locker of the tiger is 4. Amy picked the tiger. Rose picked the elephant. Iris picked the elephant.

**lookup** (Which locker belongs to Iris's pick?; O answers 9, S answers 8):

```
<|im_start|>user
The locker of the spider is 9. The locker of the tiger is 4. The locker of the elephant is 2. Amy picked the tiger. Rose picked the elephant. Iris picked the⟦ spider⟧.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (How many legs does Iris's pick have?; O answers 8, S answers 4):

```
<|im_start|>user
The locker of the spider is 9. The locker of the tiger is 4. The locker of the elephant is 2. Amy picked the tiger. Rose picked the elephant. Iris picked the⟦ spider⟧.
How many legs does Iris's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### animals-0740 (bridge token 43; expected digits {'identity': 4, 'position': 2, 'value': 1, 'original': 5})

O: The locker of the bear is 2. The locker of the crow is 5. The locker of the sheep is 4. Mark picked the bear. Lily picked the sheep. James picked the crow.

S: The locker of the sheep is 1. The locker of the crow is 5. The locker of the bear is 2. Mark picked the bear. Lily picked the sheep. James picked the sheep.

**lookup** (Which locker belongs to James's pick?; O answers 5, S answers 1):

```
<|im_start|>user
The locker of the bear is 2. The locker of the crow is 5. The locker of the sheep is 4. Mark picked the bear. Lily picked the sheep. James picked the⟦ crow⟧.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (How many legs does James's pick have?; O answers 2, S answers 4):

```
<|im_start|>user
The locker of the bear is 2. The locker of the crow is 5. The locker of the sheep is 4. Mark picked the bear. Lily picked the sheep. James picked the⟦ crow⟧.
How many legs does James's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### animals-0887 (bridge token 38; expected digits {'identity': 6, 'position': 5, 'value': 7, 'original': 8})

O: The locker of the turkey is 5. The locker of the fly is 6. The locker of the eagle is 8. Owen picked the turkey. Amy picked the eagle. Oscar picked the fly.

S: The locker of the fly is 7. The locker of the turkey is 5. The locker of the eagle is 8. Owen picked the turkey. Amy picked the fly. Oscar picked the fly.

**lookup** (Which locker belongs to Amy's pick?; O answers 8, S answers 7):

```
<|im_start|>user
The locker of the turkey is 5. The locker of the fly is 6. The locker of the eagle is 8. Owen picked the turkey. Amy picked the⟦ eagle⟧. Oscar picked the fly.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (How many legs does Amy's pick have?; O answers 2, S answers 6):

```
<|im_start|>user
The locker of the turkey is 5. The locker of the fly is 6. The locker of the eagle is 8. Owen picked the turkey. Amy picked the⟦ eagle⟧. Oscar picked the fly.
How many legs does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

## fruits: 700 scenes generated; pool 19 items; recall: What color is {p}'s pick?

### fruits-0046 (bridge token 33; expected digits {'identity': 4, 'position': 2, 'value': 1, 'original': 8})

O: The locker of the banana is 4. The locker of the pumpkin is 8. The locker of the olive is 2. Jack picked the pumpkin. Grace picked the banana. Iris picked the olive.

S: The locker of the olive is 2. The locker of the pumpkin is 8. The locker of the banana is 1. Jack picked the banana. Grace picked the banana. Iris picked the olive.

**lookup** (Which locker belongs to Jack's pick?; O answers 8, S answers 1):

```
<|im_start|>user
The locker of the banana is 4. The locker of the pumpkin is 8. The locker of the olive is 2. Jack picked the⟦ pumpkin⟧. Grace picked the banana. Iris picked the olive.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (What color is Jack's pick?; O answers orange, S answers yellow):

```
<|im_start|>user
The locker of the banana is 4. The locker of the pumpkin is 8. The locker of the olive is 2. Jack picked the⟦ pumpkin⟧. Grace picked the banana. Iris picked the olive.
What color is Jack's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### fruits-0303 (bridge token 38; expected digits {'identity': 5, 'position': 7, 'value': 2, 'original': 6})

O: The locker of the lemon is 5. The locker of the lime is 7. The locker of the fig is 6. Will picked the lime. David picked the fig. Carl picked the lemon.

S: The locker of the lime is 7. The locker of the lemon is 2. The locker of the fig is 6. Will picked the lime. David picked the lemon. Carl picked the lemon.

**lookup** (Which locker belongs to David's pick?; O answers 6, S answers 2):

```
<|im_start|>user
The locker of the lemon is 5. The locker of the lime is 7. The locker of the fig is 6. Will picked the lime. David picked the⟦ fig⟧. Carl picked the lemon.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (What color is David's pick?; O answers purple, S answers yellow):

```
<|im_start|>user
The locker of the lemon is 5. The locker of the lime is 7. The locker of the fig is 6. Will picked the lime. David picked the⟦ fig⟧. Carl picked the lemon.
What color is David's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### fruits-0457 (bridge token 38; expected digits {'identity': 8, 'position': 5, 'value': 4, 'original': 1})

O: The locker of the fig is 5. The locker of the apple is 1. The locker of the lime is 8. Lily picked the fig. Lucy picked the apple. Ella picked the lime.

S: The locker of the lime is 4. The locker of the apple is 1. The locker of the fig is 5. Lily picked the fig. Lucy picked the lime. Ella picked the lime.

**lookup** (Which locker belongs to Lucy's pick?; O answers 1, S answers 4):

```
<|im_start|>user
The locker of the fig is 5. The locker of the apple is 1. The locker of the lime is 8. Lily picked the fig. Lucy picked the⟦ apple⟧. Ella picked the lime.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (What color is Lucy's pick?; O answers red, S answers green):

```
<|im_start|>user
The locker of the fig is 5. The locker of the apple is 1. The locker of the lime is 8. Lily picked the fig. Lucy picked the⟦ apple⟧. Ella picked the lime.
What color is Lucy's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### fruits-0502 (bridge token 33; expected digits {'identity': 8, 'position': 1, 'value': 9, 'original': 7})

O: The locker of the avocado is 7. The locker of the raspberry is 1. The locker of the banana is 8. Carl picked the avocado. Frank picked the banana. Kate picked the raspberry.

S: The locker of the avocado is 7. The locker of the banana is 9. The locker of the raspberry is 1. Carl picked the banana. Frank picked the banana. Kate picked the raspberry.

**lookup** (Which locker belongs to Carl's pick?; O answers 7, S answers 9):

```
<|im_start|>user
The locker of the avocado is 7. The locker of the raspberry is 1. The locker of the banana is 8. Carl picked the⟦ avocado⟧. Frank picked the banana. Kate picked the raspberry.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (What color is Carl's pick?; O answers green, S answers yellow):

```
<|im_start|>user
The locker of the avocado is 7. The locker of the raspberry is 1. The locker of the banana is 8. Carl picked the⟦ avocado⟧. Frank picked the banana. Kate picked the raspberry.
What color is Carl's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### fruits-0608 (bridge token 43; expected digits {'identity': 8, 'position': 6, 'value': 9, 'original': 4})

O: The locker of the pumpkin is 8. The locker of the grape is 4. The locker of the olive is 6. Ryan picked the olive. Lucy picked the pumpkin. Alice picked the grape.

S: The locker of the olive is 6. The locker of the grape is 4. The locker of the pumpkin is 9. Ryan picked the olive. Lucy picked the pumpkin. Alice picked the pumpkin.

**lookup** (Which locker belongs to Alice's pick?; O answers 4, S answers 9):

```
<|im_start|>user
The locker of the pumpkin is 8. The locker of the grape is 4. The locker of the olive is 6. Ryan picked the olive. Lucy picked the pumpkin. Alice picked the⟦ grape⟧.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

**recall** (What color is Alice's pick?; O answers purple, S answers orange):

```
<|im_start|>user
The locker of the pumpkin is 8. The locker of the grape is 4. The locker of the olive is 6. Ryan picked the olive. Lucy picked the pumpkin. Alice picked the⟦ grape⟧.
What color is Alice's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

## names: 700 scenes generated; pool 59 items; recall: none: no clean one-token fact for a name; the recall is skipped

### names-0042 (bridge token 29; expected digits {'identity': 4, 'position': 7, 'value': 2, 'original': 8})

O: The locker of Fiona is 8. The locker of Frank is 7. The locker of Alice is 4. Will picked Fiona. Kate picked Alice. Kyle picked Frank.

S: The locker of Fiona is 8. The locker of Alice is 2. The locker of Frank is 7. Will picked Alice. Kate picked Alice. Kyle picked Frank.

**lookup** (Which locker belongs to Will's pick?; O answers 8, S answers 2):

```
<|im_start|>user
The locker of Fiona is 8. The locker of Frank is 7. The locker of Alice is 4. Will picked⟦ Fiona⟧. Kate picked Alice. Kyle picked Frank.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### names-0266 (bridge token 33; expected digits {'identity': 8, 'position': 7, 'value': 1, 'original': 4})

O: The locker of Olivia is 4. The locker of Ivan is 7. The locker of Alice is 8. Dan picked Alice. Maria picked Olivia. Kyle picked Ivan.

S: The locker of Olivia is 4. The locker of Alice is 1. The locker of Ivan is 7. Dan picked Alice. Maria picked Alice. Kyle picked Ivan.

**lookup** (Which locker belongs to Maria's pick?; O answers 4, S answers 1):

```
<|im_start|>user
The locker of Olivia is 4. The locker of Ivan is 7. The locker of Alice is 8. Dan picked Alice. Maria picked⟦ Olivia⟧. Kyle picked Ivan.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### names-0395 (bridge token 33; expected digits {'identity': 5, 'position': 4, 'value': 7, 'original': 6})

O: The locker of Liam is 5. The locker of Hugo is 4. The locker of Paul is 6. Luke picked Hugo. Beth picked Paul. Sara picked Liam.

S: The locker of Hugo is 4. The locker of Liam is 7. The locker of Paul is 6. Luke picked Hugo. Beth picked Liam. Sara picked Liam.

**lookup** (Which locker belongs to Beth's pick?; O answers 6, S answers 7):

```
<|im_start|>user
The locker of Liam is 5. The locker of Hugo is 4. The locker of Paul is 6. Luke picked Hugo. Beth picked⟦ Paul⟧. Sara picked Liam.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### names-0431 (bridge token 37; expected digits {'identity': 3, 'position': 6, 'value': 4, 'original': 1})

O: The locker of Will is 6. The locker of Fiona is 1. The locker of Ella is 3. Diana picked Will. Mark picked Ella. Victor picked Fiona.

S: The locker of Ella is 4. The locker of Fiona is 1. The locker of Will is 6. Diana picked Will. Mark picked Ella. Victor picked Ella.

**lookup** (Which locker belongs to Victor's pick?; O answers 1, S answers 4):

```
<|im_start|>user
The locker of Will is 6. The locker of Fiona is 1. The locker of Ella is 3. Diana picked Will. Mark picked Ella. Victor picked⟦ Fiona⟧.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### names-0524 (bridge token 33; expected digits {'identity': 6, 'position': 5, 'value': 2, 'original': 8})

O: The locker of Paul is 6. The locker of Julia is 8. The locker of Maria is 5. Will picked Maria. Hugo picked Julia. Luke picked Paul.

S: The locker of Maria is 5. The locker of Julia is 8. The locker of Paul is 2. Will picked Maria. Hugo picked Paul. Luke picked Paul.

**lookup** (Which locker belongs to Hugo's pick?; O answers 8, S answers 2):

```
<|im_start|>user
The locker of Paul is 6. The locker of Julia is 8. The locker of Maria is 5. Will picked Maria. Hugo picked⟦ Julia⟧. Luke picked Paul.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

