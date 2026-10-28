# 47.11 plan on muse-glimmer-30b (L26): 5 rendered prompts per type (seed 0), as the model reads them; ⟦...⟧ the bridge word. Counts in plan.json.

## animals: 700 scenes generated; pool 32 items; recall: How many legs does {p}'s pick have?

### animals-0067 (bridge token 72; expected digits {'identity': 9, 'position': 6, 'value': 3, 'original': 4})

O: The locker of the turkey is 6. The locker of the fly is 4. The locker of the camel is 9. Liam picked the fly. Ben picked the turkey. Ivan picked the camel.

S: The locker of the camel is 3. The locker of the fly is 4. The locker of the turkey is 6. Liam picked the camel. Ben picked the turkey. Ivan picked the camel.

**lookup** (Which locker belongs to Liam's pick?; O answers 4, S answers 3):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 6. The locker of the fly is 4. The locker of the camel is 9. Liam picked the⟦ fly⟧. Ben picked the turkey. Ivan picked the camel.
Which locker belongs to Liam's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (How many legs does Liam's pick have?; O answers 6, S answers 4):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 6. The locker of the fly is 4. The locker of the camel is 9. Liam picked the⟦ fly⟧. Ben picked the turkey. Ivan picked the camel.
How many legs does Liam's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### animals-0444 (bridge token 82; expected digits {'identity': 6, 'position': 2, 'value': 9, 'original': 1})

O: The locker of the chicken is 1. The locker of the spider is 2. The locker of the bee is 6. Finn picked the spider. Lily picked the bee. Carl picked the chicken.

S: The locker of the chicken is 1. The locker of the bee is 9. The locker of the spider is 2. Finn picked the spider. Lily picked the bee. Carl picked the bee.

**lookup** (Which locker belongs to Carl's pick?; O answers 1, S answers 9):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 1. The locker of the spider is 2. The locker of the bee is 6. Finn picked the spider. Lily picked the bee. Carl picked the⟦ chicken⟧.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (How many legs does Carl's pick have?; O answers 2, S answers 6):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the chicken is 1. The locker of the spider is 2. The locker of the bee is 6. Finn picked the spider. Lily picked the bee. Carl picked the⟦ chicken⟧.
How many legs does Carl's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### animals-0643 (bridge token 82; expected digits {'identity': 1, 'position': 7, 'value': 8, 'original': 5})

O: The locker of the horse is 7. The locker of the fox is 1. The locker of the bee is 5. Eva picked the horse. Diana picked the fox. Fiona picked the bee.

S: The locker of the fox is 8. The locker of the horse is 7. The locker of the bee is 5. Eva picked the horse. Diana picked the fox. Fiona picked the fox.

**lookup** (Which locker belongs to Fiona's pick?; O answers 5, S answers 8):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the horse is 7. The locker of the fox is 1. The locker of the bee is 5. Eva picked the horse. Diana picked the fox. Fiona picked the⟦ bee⟧.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (How many legs does Fiona's pick have?; O answers 6, S answers 4):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the horse is 7. The locker of the fox is 1. The locker of the bee is 5. Eva picked the horse. Diana picked the fox. Fiona picked the⟦ bee⟧.
How many legs does Fiona's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### animals-0711 (bridge token 77; expected digits {'identity': 5, 'position': 7, 'value': 1, 'original': 4})

O: The locker of the spider is 5. The locker of the butterfly is 4. The locker of the eagle is 7. Liam picked the eagle. Mia picked the butterfly. Frank picked the spider.

S: The locker of the eagle is 7. The locker of the butterfly is 4. The locker of the spider is 1. Liam picked the eagle. Mia picked the spider. Frank picked the spider.

**lookup** (Which locker belongs to Mia's pick?; O answers 4, S answers 1):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 5. The locker of the butterfly is 4. The locker of the eagle is 7. Liam picked the eagle. Mia picked the⟦ butterfly⟧. Frank picked the spider.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (How many legs does Mia's pick have?; O answers 6, S answers 8):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 5. The locker of the butterfly is 4. The locker of the eagle is 7. Liam picked the eagle. Mia picked the⟦ butterfly⟧. Frank picked the spider.
How many legs does Mia's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### animals-0861 (bridge token 77; expected digits {'identity': 4, 'position': 1, 'value': 2, 'original': 9})

O: The locker of the owl is 9. The locker of the wolf is 1. The locker of the spider is 4. Fiona picked the wolf. Dan picked the owl. Kyle picked the spider.

S: The locker of the owl is 9. The locker of the spider is 2. The locker of the wolf is 1. Fiona picked the wolf. Dan picked the spider. Kyle picked the spider.

**lookup** (Which locker belongs to Dan's pick?; O answers 9, S answers 2):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the owl is 9. The locker of the wolf is 1. The locker of the spider is 4. Fiona picked the wolf. Dan picked the⟦ owl⟧. Kyle picked the spider.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (How many legs does Dan's pick have?; O answers 2, S answers 8):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the owl is 9. The locker of the wolf is 1. The locker of the spider is 4. Fiona picked the wolf. Dan picked the⟦ owl⟧. Kyle picked the spider.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

## fruits: 700 scenes generated; pool 20 items; recall: What color is {p}'s pick?

### fruits-0050 (bridge token 82; expected digits {'identity': 9, 'position': 1, 'value': 6, 'original': 2})

O: The locker of the plum is 2. The locker of the tomato is 1. The locker of the melon is 9. James picked the melon. Sam picked the tomato. Tom picked the plum.

S: The locker of the plum is 2. The locker of the melon is 6. The locker of the tomato is 1. James picked the melon. Sam picked the tomato. Tom picked the melon.

**lookup** (Which locker belongs to Tom's pick?; O answers 2, S answers 6):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the plum is 2. The locker of the tomato is 1. The locker of the melon is 9. James picked the melon. Sam picked the tomato. Tom picked the⟦ plum⟧.
Which locker belongs to Tom's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (What color is Tom's pick?; O answers purple, S answers green):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the plum is 2. The locker of the tomato is 1. The locker of the melon is 9. James picked the melon. Sam picked the tomato. Tom picked the⟦ plum⟧.
What color is Tom's pick? Answer with a single word and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### fruits-0307 (bridge token 77; expected digits {'identity': 3, 'position': 5, 'value': 6, 'original': 1})

O: The locker of the fig is 5. The locker of the pineapple is 1. The locker of the lime is 3. Owen picked the lime. Tara picked the pineapple. Liam picked the fig.

S: The locker of the lime is 6. The locker of the pineapple is 1. The locker of the fig is 5. Owen picked the lime. Tara picked the lime. Liam picked the fig.

**lookup** (Which locker belongs to Tara's pick?; O answers 1, S answers 6):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the fig is 5. The locker of the pineapple is 1. The locker of the lime is 3. Owen picked the lime. Tara picked the⟦ pineapple⟧. Liam picked the fig.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (What color is Tara's pick?; O answers yellow, S answers green):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the fig is 5. The locker of the pineapple is 1. The locker of the lime is 3. Owen picked the lime. Tara picked the⟦ pineapple⟧. Liam picked the fig.
What color is Tara's pick? Answer with a single word and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### fruits-0458 (bridge token 77; expected digits {'identity': 3, 'position': 5, 'value': 8, 'original': 6})

O: The locker of the lemon is 5. The locker of the banana is 3. The locker of the avocado is 6. Ben picked the lemon. Zoe picked the avocado. Kate picked the banana.

S: The locker of the banana is 8. The locker of the lemon is 5. The locker of the avocado is 6. Ben picked the lemon. Zoe picked the banana. Kate picked the banana.

**lookup** (Which locker belongs to Zoe's pick?; O answers 6, S answers 8):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the lemon is 5. The locker of the banana is 3. The locker of the avocado is 6. Ben picked the lemon. Zoe picked the⟦ avocado⟧. Kate picked the banana.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (What color is Zoe's pick?; O answers green, S answers yellow):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the lemon is 5. The locker of the banana is 3. The locker of the avocado is 6. Ben picked the lemon. Zoe picked the⟦ avocado⟧. Kate picked the banana.
What color is Zoe's pick? Answer with a single word and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### fruits-0504 (bridge token 77; expected digits {'identity': 5, 'position': 2, 'value': 3, 'original': 6})

O: The locker of the plum is 5. The locker of the cherry is 6. The locker of the grape is 2. Lily picked the grape. Eve picked the cherry. Rose picked the plum.

S: The locker of the grape is 2. The locker of the cherry is 6. The locker of the plum is 3. Lily picked the grape. Eve picked the plum. Rose picked the plum.

**lookup** (Which locker belongs to Eve's pick?; O answers 6, S answers 3):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the plum is 5. The locker of the cherry is 6. The locker of the grape is 2. Lily picked the grape. Eve picked the⟦ cherry⟧. Rose picked the plum.
Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (What color is Eve's pick?; O answers red, S answers purple):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the plum is 5. The locker of the cherry is 6. The locker of the grape is 2. Lily picked the grape. Eve picked the⟦ cherry⟧. Rose picked the plum.
What color is Eve's pick? Answer with a single word and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### fruits-0613 (bridge token 77; expected digits {'identity': 1, 'position': 7, 'value': 2, 'original': 3})

O: The locker of the banana is 3. The locker of the pear is 1. The locker of the avocado is 7. Hugo picked the avocado. Zoe picked the banana. Finn picked the pear.

S: The locker of the banana is 3. The locker of the avocado is 7. The locker of the pear is 2. Hugo picked the avocado. Zoe picked the pear. Finn picked the pear.

**lookup** (Which locker belongs to Zoe's pick?; O answers 3, S answers 2):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the banana is 3. The locker of the pear is 1. The locker of the avocado is 7. Hugo picked the avocado. Zoe picked the⟦ banana⟧. Finn picked the pear.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

**recall** (What color is Zoe's pick?; O answers yellow, S answers green):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the banana is 3. The locker of the pear is 1. The locker of the avocado is 7. Hugo picked the avocado. Zoe picked the⟦ banana⟧. Finn picked the pear.
What color is Zoe's pick? Answer with a single word and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

## names: 700 scenes generated; pool 59 items; recall: none: no clean one-token fact for a name; the recall is skipped

### names-0042 (bridge token 68; expected digits {'identity': 4, 'position': 7, 'value': 2, 'original': 8})

O: The locker of Fiona is 8. The locker of Frank is 7. The locker of Alice is 4. Will picked Fiona. Kate picked Alice. Kyle picked Frank.

S: The locker of Fiona is 8. The locker of Alice is 2. The locker of Frank is 7. Will picked Alice. Kate picked Alice. Kyle picked Frank.

**lookup** (Which locker belongs to Will's pick?; O answers 8, S answers 2):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of Fiona is 8. The locker of Frank is 7. The locker of Alice is 4. Will picked⟦ Fiona⟧. Kate picked Alice. Kyle picked Frank.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### names-0266 (bridge token 72; expected digits {'identity': 8, 'position': 7, 'value': 1, 'original': 4})

O: The locker of Olivia is 4. The locker of Ivan is 7. The locker of Alice is 8. Dan picked Alice. Maria picked Olivia. Kyle picked Ivan.

S: The locker of Olivia is 4. The locker of Alice is 1. The locker of Ivan is 7. Dan picked Alice. Maria picked Alice. Kyle picked Ivan.

**lookup** (Which locker belongs to Maria's pick?; O answers 4, S answers 1):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of Olivia is 4. The locker of Ivan is 7. The locker of Alice is 8. Dan picked Alice. Maria picked⟦ Olivia⟧. Kyle picked Ivan.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### names-0395 (bridge token 72; expected digits {'identity': 5, 'position': 4, 'value': 7, 'original': 6})

O: The locker of Liam is 5. The locker of Hugo is 4. The locker of Paul is 6. Luke picked Hugo. Beth picked Paul. Sara picked Liam.

S: The locker of Hugo is 4. The locker of Liam is 7. The locker of Paul is 6. Luke picked Hugo. Beth picked Liam. Sara picked Liam.

**lookup** (Which locker belongs to Beth's pick?; O answers 6, S answers 7):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of Liam is 5. The locker of Hugo is 4. The locker of Paul is 6. Luke picked Hugo. Beth picked⟦ Paul⟧. Sara picked Liam.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### names-0431 (bridge token 76; expected digits {'identity': 3, 'position': 6, 'value': 4, 'original': 1})

O: The locker of Will is 6. The locker of Fiona is 1. The locker of Ella is 3. Diana picked Will. Mark picked Ella. Victor picked Fiona.

S: The locker of Ella is 4. The locker of Fiona is 1. The locker of Will is 6. Diana picked Will. Mark picked Ella. Victor picked Ella.

**lookup** (Which locker belongs to Victor's pick?; O answers 1, S answers 4):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of Will is 6. The locker of Fiona is 1. The locker of Ella is 3. Diana picked Will. Mark picked Ella. Victor picked⟦ Fiona⟧.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

### names-0524 (bridge token 72; expected digits {'identity': 6, 'position': 5, 'value': 2, 'original': 8})

O: The locker of Paul is 6. The locker of Julia is 8. The locker of Maria is 5. Will picked Maria. Hugo picked Julia. Luke picked Paul.

S: The locker of Maria is 5. The locker of Julia is 8. The locker of Paul is 2. Will picked Maria. Hugo picked Paul. Luke picked Paul.

**lookup** (Which locker belongs to Hugo's pick?; O answers 8, S answers 2):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of Paul is 6. The locker of Julia is 8. The locker of Maria is 5. Will picked Maria. Hugo picked⟦ Julia⟧. Luke picked Paul.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

