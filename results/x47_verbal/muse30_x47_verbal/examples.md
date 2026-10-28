# Examples: muse30_x47_verbal

10 random items (seed 0) of 100. The write h + 2 (mu_k - mu_j) is added at ⟦...⟧; the lens reads the same position. UNVERIFIED.

## C2-0104: bridge 'horse' in slot 0, digits by slot [2, 3, 8]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the horse is 2. The locker of the crow is 3. The locker of the duck is 8. Lily picked the⟦ horse⟧. Nina picked the duck. Eric picked the crow.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' Horse', ' Horses', 'Horse', ' horse', ' Pfer', ' horses', ' caballo', ' лошади', ' лоша', ' riding', ' Hors', ' Horsepower', ' pony', "'s", ' Hipp', ' and', ' animal', ' chevaux', ' Riding', ' ride']

- write to slot 1 (norm 82.7625): best ordinal rank 789 (' one'), KL 0.0249; x8 lookup answer '3' (target); top 20: [' Horse', ' Horses', ' horse', ' Pfer', 'Horse', ' horses', ' caballo', ' лошади', ' лоша', ' riding', ' Horsepower', ' pony', ' Hors', ' chevaux', ' Hipp', ' ride', ' ngựa', ' cheval', ' Riding', '騎']
- identity to slot 1 (norm 82.7625): best ordinal rank 117 (' first'), KL 3; x8 lookup answer '3' (target); top 20: ["'s", ' and', ' Duck', ' animal', ' Rabbit', ' Horse', ' Bunny', ' milk', '�', ' girl', ' bird', ' poultry', ' animals', ' birds', ' Milk', ' chicken', ' horse', ' rabbit', ' rabbits', ' who']
- write to slot 2 (norm 101.6898): best ordinal rank 812 (' one'), KL 0.0284; x8 lookup answer '8' (target); top 20: [' Horse', ' Horses', ' Pfer', ' horse', 'Horse', ' horses', ' caballo', ' лошади', ' лоша', ' riding', ' Horsepower', ' pony', ' Hors', ' chevaux', ' ride', ' Hipp', ' ngựa', ' cheval', ' Riding', ' hors']
- identity to slot 2 (norm 101.6898): best ordinal rank 120 (' first'), KL 5.94; x8 lookup answer '8' (target); top 20: [' Duck', "'s", ' and', ' Rabbit', ' bird', ' Bunny', ' milk', ' animal', ' birds', ' girl', ' poultry', '�', ' Milk', ' chicken', ' animals', ' rabbit', ' Daisy', ' ducks', ' who', ' chickens']

## C2-0210: bridge 'dog' in slot 2, digits by slot [9, 7, 1]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 9. The locker of the deer is 7. The locker of the dog is 1. Rose picked the turkey. Olivia picked the deer. Laura picked the⟦ dog⟧.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' .\n\n', '.\n\n', ' .', ' Dog', ' Dogs', ' .\n', '.\n', ' ,', '.\n\n\n', ' respectively', ' ;', ' trio', ' who', ' ...', ' where', ' 犬', ' and', ' which', '.', ' dogs']

- write to slot 0 (norm 101.6898): best ordinal rank 9 (' three'), KL 0.409; x8 lookup answer '9' (target); top 20: [' Dog', ' Dogs', ' trio', ' .\n\n', ' .', '.\n\n', ' who', ' dogs', ' three', ' ,', ' ...', ' whose', ' which', ' and', '.\n\n\n', ' 犬', ' where', ' .\n', ' animals', '�']
- identity to slot 0 (norm 101.6898): best ordinal rank 34 (' before'), KL 2.33; x8 lookup answer '9' (target); top 20: [' .\n\n', ' Turkey', '.\n\n', ' .', ' poultry', ' turkey', ' .\n', ' respectively', '.\n', ' chicken', '.\n\n\n', ' ,', '.', ' ;', ' when', '.\n\n\n\n', '."\n\n', ' who', ' Trio', ' ...']
- write to slot 1 (norm 49.7362): best ordinal rank 28 (' three'), KL 0.0898; x8 lookup answer '1' (original); top 20: [' Dog', ' Dogs', ' .\n\n', ' .', '.\n\n', ' .\n', ' ,', ' who', ' respectively', ' trio', ' dogs', '.\n\n\n', ' where', '.\n', ' ;', ' 犬', ' ...', ' which', ' and', ' whose']
- identity to slot 1 (norm 49.7362): best ordinal rank 26 (' three'), KL 0.761; x8 lookup answer '1' (original); top 20: [' .\n\n', '.\n\n', ' .', ' .\n', ' respectively', '.\n', '.\n\n\n', ' ,', ' ;', ' who', '.', ' trio', ' when', ' ...', '.\n\n\n\n', ' chicken', ' which', ' whose', ' instead', ' where']

## C2-0118: bridge 'chicken' in slot 2, digits by slot [8, 2, 4]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the rabbit is 8. The locker of the sheep is 2. The locker of the chicken is 4. Julia picked the sheep. Alice picked the rabbit. Frank picked the⟦ chicken⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' Chicken', ' chicken', ' Chick', ' poultry', ' .\n\n', '.\n\n', ' chickens', 'Chicken', ' .', ' respectively', ' and', ' .\n', '.\n', ' chick', ' Bird', ' �', ' bird', ' ,', '.\n\n\n', ' instead']

- write to slot 0 (norm 101.6898): best ordinal rank 11 (' three'), KL 0.185; x8 lookup answer '8' (target); top 20: [' Chicken', ' Chick', ' chicken', ' poultry', ' chickens', 'Chicken', ' Bird', ' trio', ' .\n\n', ' chick', '.\n\n', ' three', ' bird', ' and', ' feathers', ' �', ' who', ' whose', ' birds', ' .']
- identity to slot 0 (norm 101.6898): best ordinal rank 47 (' three'), KL 8.09; x8 lookup answer '8' (target); top 20: [' Rabbit', ' Rabb', 'Rabbit', ' rabbits', ' .\n\n', ' rabbit', '.\n\n', ' .', ' .\n', ' Rb', '.\n', ' ,', '.\n\n\n', ' Bunny', ' ;', ' which', '.\n\n\n\n', ' and', '_rr', ' respectively']
- write to slot 1 (norm 49.7362): best ordinal rank 29 (' three'), KL 0.0452; x8 lookup answer '4' (original); top 20: [' Chicken', ' Chick', ' chicken', ' poultry', 'Chicken', ' chickens', ' .\n\n', '.\n\n', ' Bird', ' .', ' �', ' chick', ' bird', ' and', ' respectively', ' feathers', ' who', ' birds', ' which', ' ,']
- identity to slot 1 (norm 49.7362): best ordinal rank 29 (' three'), KL 1.61; x8 lookup answer '4' (original); top 20: [' .\n\n', ' Rabbit', '.\n\n', ' .', ' .\n', '.\n', ' Chicken', ' respectively', ' and', ' ,', ' rabbits', '.\n\n\n', ' ;', ' chicken', ' which', ' Rabb', '.\n\n\n\n', ' rabbit', ' ...', ' when']

## C2-0011: bridge 'duck' in slot 2, digits by slot [8, 1, 6]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the zebra is 8. The locker of the mouse is 1. The locker of the duck is 6. Nina picked the⟦ duck⟧. Amy picked the zebra. Grace picked the mouse.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' Duck', "'s", ' and', ' who', ' ducks', ' �', 'Duck', ' poultry', ' bird', ' Egg', ' Daisy', ' chicken', ' eggs', ' Bird', ' duck', ' feathers', ' alone', ' kidn', ' whom', ' Rabbit']

- write to slot 0 (norm 101.6898): best ordinal rank 66 (' first'), KL 0.143; x8 lookup answer '8' (target); top 20: [' Duck', "'s", ' who', ' and', ' Rabbit', ' Bird', ' �', ' bird', ' Chicken', ' Bunny', ' feathers', ' Chick', ' ducks', 'Duck', ' chicken', '�', ' Egg', ' birds', ' poultry', ' whom']
- identity to slot 0 (norm 101.6898): best ordinal rank 121 (' one'), KL 4.32; x8 lookup answer '8' (target); top 20: ['(Mouse', ' Mouse', '.Mouse', ' and', ' Mous', ' Rabbit', ' mice', ' who', '_Mouse', "'s", '(mouse', ' Mickey', ' wrist', ' whom', ' instead', ' Chicken', ' rabbits', ' alone', ' whose', ' to']
- write to slot 1 (norm 49.7362): best ordinal rank 69 (' before'), KL 0.0316; x8 lookup answer '6' (original); top 20: [' Duck', "'s", ' and', ' who', ' �', ' ducks', 'Duck', ' Bunny', ' bird', ' Bird', ' poultry', ' Rabbit', ' chicken', ' Chicken', ' Egg', ' feathers', ' Daisy', ' whom', ' Chick', ' eggs']
- identity to slot 1 (norm 49.7362): best ordinal rank 69 (' before'), KL 0.514; x8 lookup answer '6' (original); top 20: [' Duck', ' and', "'s", ' who', ' Mouse', '(Mouse', ' Rabbit', ' whom', ' Chicken', ' alone', ' chicken', ' instead', ' whose', ' poultry', '.Mouse', ' to', ' bird', ' eggs', ' kidn', ' Bird']

## C2-0071: bridge 'butterfly' in slot 1, digits by slot [4, 5, 3]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 4. The locker of the butterfly is 5. The locker of the lion is 3. Iris picked the turkey. Rose picked the⟦ butterfly⟧. Dan picked the lion.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' Butterfly', ' and', ' .', ' butterflies', ' Butter', ' ,', ' .\n\n', ' whereas', '.\n\n', ' Beet', ' Bunny', ' Bird', ' instead', ' bird', ' wing', ' Bey', ' wings', ' birds', ' whom', ' Bow']

- write to slot 0 (norm 82.7625): best ordinal rank 98 (' one'), KL 0.12; x8 lookup answer '4' (target); top 20: [' Butterfly', ' and', ' butterflies', ' Butter', ' Beet', ' ,', ' Bird', ' butterfly', ' .', ' bird', ' birds', ' Bunny', ' wings', ' wing', ' who', ' whereas', ' which', ' .\n\n', ' whom', ' whose']
- identity to slot 0 (norm 82.7625): best ordinal rank 93 (' before'), KL 3.91; x8 lookup answer '4' (target); top 20: [' Turkey', ' poultry', ' and', ' turkey', ' chicken', ' .', ' ,', ' .\n\n', ' bird', ' respectively', ' who', ' whom', ' birds', ' Chicken', '.\n\n', ' instead', ' when', ' which', ' feathers', ' ;']
- write to slot 2 (norm 49.7362): best ordinal rank 179 (' before'), KL 0.0818; x8 lookup answer '5' (original); top 20: [' Butterfly', ' and', ' .', ' .\n\n', ' ,', ' Butter', '.\n\n', ' whereas', ' butterflies', ' when', ' respectively', ' instead', ' .\n', '.', ' Bey', ' although', ' wings', ' Bow', ' while', ' ;']
- identity to slot 2 (norm 49.7362): best ordinal rank 102 (' before'), KL 1.47; x8 lookup answer '5' (original); top 20: [' and', ' .', ' ,', ' .\n\n', ' poultry', ' bird', ' chicken', ' birds', ' whom', ' respectively', ' who', '.\n\n', ' instead', ' when', ' Bird', ' which', ' whereas', ' ;', ' ...', '.']

## C2-0144: bridge 'chicken' in slot 2, digits by slot [5, 6, 9]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the horse is 5. The locker of the tick is 6. The locker of the chicken is 9. Vera picked the tick. Ivan picked the horse. Peter picked the⟦ chicken⟧.
Which locker belongs to Peter's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' Chicken', ' chicken', ' Chick', ' poultry', ' .\n\n', 'Chicken', ' chickens', '.\n\n', ' .', ' .\n', ' �', ' Egg', ' ,', ' and', ' respectively', '.\n', ' eggs', ' Bird', ' chick', ' ;']

- write to slot 0 (norm 101.6898): best ordinal rank 45 (' three'), KL 0.173; x8 lookup answer '5' (target); top 20: [' Chicken', ' Chick', ' chicken', ' poultry', 'Chicken', ' chickens', ' Bird', ' .\n\n', ' �', ' chick', ' bird', '.\n\n', ' and', ' who', ' feathers', ' Egg', ' .', ' whose', ' birds', ' مرغ']
- identity to slot 0 (norm 101.6898): best ordinal rank 64 (' one'), KL 5.38; x8 lookup answer '5' (target); top 20: [' Tick', ' .\n\n', ' .', '.\n\n', ' .\n', ' and', ' ,', '_tick', '.\n', ' ;', ' respectively', ' ...', ' which', '.', ' Chick', '.\n\n\n', ' when', ' with', '\n\n', ' where']
- write to slot 1 (norm 49.7362): best ordinal rank 62 (' before'), KL 0.0427; x8 lookup answer '9' (original); top 20: [' Chicken', ' Chick', ' chicken', ' poultry', 'Chicken', ' chickens', ' .\n\n', ' �', ' .', '.\n\n', ' Bird', ' Egg', ' bird', ' chick', ' and', ' ,', ' who', ' eggs', ' feathers', ' egg']
- identity to slot 1 (norm 49.7362): best ordinal rank 49 (' before'), KL 1.03; x8 lookup answer '9' (original); top 20: [' .\n\n', '.\n\n', ' Chick', ' .', ' Chicken', ' .\n', ' and', ' ,', '.\n', ' ;', ' chicken', ' respectively', ' ...', '.\n\n\n', ' Tick', ' which', '."\n\n', ' who', ' whose', ' when']

## C2-0140: bridge 'rabbit' in slot 0, digits by slot [1, 3, 7]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the rabbit is 1. The locker of the spider is 3. The locker of the owl is 7. Alice picked the spider. David picked the⟦ rabbit⟧. Lily picked the owl.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' Rabbit', ' Rabb', 'Rabbit', ' rabbits', ' rabbit', ' Bunny', ' .\n\n', ' and', ' .', '(R', ' ,', ' Rb', ' ...', '.\n\n', '/R', ',R', ' animals', ' which', ' animal', ' .\n']

- write to slot 1 (norm 82.7625): best ordinal rank 117 (' before'), KL 0.0266; x8 lookup answer '3' (target); top 20: [' Rabbit', ' Rabb', ' rabbits', 'Rabbit', ' rabbit', ' .\n\n', ' .', ' Bunny', ' ,', '.\n\n', ' and', ' .\n', ' Rb', ' ...', ',R', ' which', '/R', '(R', ' goat', ' animals']
- identity to slot 1 (norm 82.7625): best ordinal rank 88 (' one'), KL 4.7; x8 lookup answer '3' (target); top 20: [' Spider', ' and', ' .\n\n', ' spiders', ' .', ' �', ' who', ' instead', ' ,', 'Spider', '.Sp', ' spider', ' Rabbit', ' chromat', '.\n\n', ' Sp', ' ...', ' .\n', ' Chrom', ' reversed']
- write to slot 2 (norm 101.6898): best ordinal rank 110 (' before'), KL 0.0579; x8 lookup answer '3' (third); top 20: [' Rabbit', ' Rabb', ' rabbits', 'Rabbit', ' .\n\n', ' rabbit', ' .', '.\n\n', ' ,', ' .\n', ' and', ' Rb', ' ...', '.\n', ' Bunny', ' ;', ',R', ' \n\n', '.\n\n\n', ' Romeo']
- identity to slot 2 (norm 101.6898): best ordinal rank 93 (' one'), KL 8.46; x8 lookup answer '3' (third); top 20: [' Spider', ' spiders', 'Spider', '.Sp', ' and', ' .\n\n', ' Sp', ' spider', ' �', ' Chrom', ' instead', ' chromat', ' who', ' .', ' Спа', ' Sprite', ' insect', ' ,', ' chromatic', ' reversed']

## C2-0114: bridge 'dog' in slot 0, digits by slot [9, 6, 1]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the dog is 9. The locker of the lion is 6. The locker of the spider is 1. Julia picked the lion. Henry picked the⟦ dog⟧. Will picked the spider.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' Dog', ' Dogs', ' dogs', ' 犬', 'Dog', ' and', ' canine', '�', ' DOG', ' who', ' ,', ' .\n\n', ' animals', ' .', "'s", ' dog', ' puppy', ' whom', ' animal', ' собаки']

- write to slot 1 (norm 82.7625): best ordinal rank 118 (' before'), KL 0.0751; x8 lookup answer '6' (target); top 20: [' Dog', ' Dogs', ' dogs', ' 犬', ' .\n\n', 'Dog', ' and', ' .', ' ,', ' canine', ' DOG', '�', ' Jog', ' who', ' .\n', '.\n\n', ' animals', ' whom', ' Hund', ' chiens']
- identity to slot 1 (norm 82.7625): best ordinal rank 64 (' before'), KL 5.9; x8 lookup answer '6' (target); top 20: [' Spider', ' .\n\n', ' and', ' who', ' ,', ' .', ' whom', ' �', ' instead', '.\n\n', "'s", ' .\n', ' chromat', ' whose', ' where', '.Sp', ' $\\', ' which', '.\n\n\n', ' but']
- write to slot 2 (norm 101.6898): best ordinal rank 108 (' before'), KL 0.173; x8 lookup answer '6' (third); top 20: [' Dog', ' Dogs', ' .\n\n', ' 犬', ' .', ' dogs', ' ,', ' and', '.\n\n', 'Dog', ' .\n', ' DOG', ' canine', ' Jog', ' Hund', ' chiens', ' ;', ' who', '.\n', ' respectively']
- identity to slot 2 (norm 101.6898): best ordinal rank 70 (' before'), KL 8.8; x8 lookup answer '6' (third); top 20: [' Spider', ' .\n\n', ' and', '.Sp', ' who', ' chromat', ' instead', ' whom', ' spiders', ' .', ' ,', ' �', 'Spider', '.\n\n', ' Chrom', ' .\n', "'s", ' $\\', ' chromatic', ' whose']

## C2-0081: bridge 'crow' in slot 2, digits by slot [2, 6, 7]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the cat is 2. The locker of the cow is 6. The locker of the crow is 7. Kyle picked the cat. Mark picked the⟦ crow⟧. Julia picked the cow.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' Crow', ' .\n\n', 'Crow', ' and', ' .', ' ,', ' .\n', '[C', '.\n\n', ' bird', ' who', ' crow', ' whose', ' $\\', ' ....', ' birds', ' ...', '.\n', ' instead', ' but']

- write to slot 0 (norm 101.6898): best ordinal rank 58 (' two'), KL 0.167; x8 lookup answer '2' (target); top 20: [' Crow', ' and', ' bird', 'Crow', ' who', '[C', ' whose', ' birds', "'s", ' .\n\n', ' ,', ' Bird', ' ....', ' crow', ' .', ' ...', ' whom', ' feathers', ',C', '(C']
- identity to slot 0 (norm 101.6898): best ordinal rank 170 (' before'), KL 5.54; x8 lookup answer '2' (target); top 20: [' Cow', ' cows', 'Cow', ' коров', ' cattle', ' 牛', ' cow', ' .\n\n', ' Beef', ' .', ' and', ' Farmer', ' ,', ' .\n', ' goat', ' Cowboys', ' Milk', ' milk', ' pasture', '.\n\n']
- write to slot 1 (norm 49.7362): best ordinal rank 145 (' before'), KL 0.0359; x8 lookup answer '7' (original); top 20: [' Crow', ' and', 'Crow', ' .\n\n', ' bird', ' ,', ' who', ' .', '[C', ' ....', ' whose', ' crow', ' birds', ' .\n', ' whom', '.\n\n', ' $\\', ' Bird', ' ...', ' instead']
- identity to slot 1 (norm 49.7362): best ordinal rank 107 (' before'), KL 0.86; x8 lookup answer '7' (original); top 20: [' Crow', ' Cow', ' .\n\n', ' and', ' .', ' cows', ' ,', ' .\n', '.\n\n', '[C', ' whose', ' $\\', '.\n', ' who', ' ...', ' [,', ' instead', ' ....', "'s", ' but']

## C2-0139: bridge 'goose' in slot 2, digits by slot [1, 9, 5]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the zebra is 1. The locker of the wolf is 9. The locker of the goose is 5. Nina picked the zebra. Rose picked the wolf. Alice picked the⟦ goose⟧.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Lens top 20, h alone: [' .\n\n', ' respectively', ' goose', ' .', '.\n\n', ' .\n', ' whom', ' ...', ' who', ' ,', ' Gus', ' whose', '.\n', ' and', ' ].\n\n', ' ;', ' trio', '."\n\n', '.\n\n\n', ' each']

- write to slot 0 (norm 101.6898): best ordinal rank 5 (' three'), KL 0.375; x8 lookup answer '1' (target); top 20: [' trio', ' .\n\n', ' who', ' goose', ' three', ' respectively', ' whom', ' whose', ' ...', ' bird', ' .', ' and', ' feathers', ' Gus', ' which', ' chicken', ' ,', ' Go', '.\n\n', ' birds']
- write to slot 1 (norm 49.7362): best ordinal rank 18 (' three'), KL 0.0774; x8 lookup answer '5' (original); top 20: [' .\n\n', ' respectively', ' goose', ' whom', ' .', ' who', ' Gus', ' .\n', ' ...', ' whose', ' ,', ' bird', ' Go', '.\n\n', ' and', ' trio', ' chicken', ' which', ' three', ' ;']

