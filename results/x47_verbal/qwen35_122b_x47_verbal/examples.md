# Examples: qwen35_122b_x47_verbal

10 random items (seed 0) of 100. The write h + 2 (mu_k - mu_j) is added at ⟦...⟧; the lens reads the same position. UNVERIFIED.

## C2-0093: bridge 'butterfly' in slot 1, digits by slot [4, 6, 2]

```
<|im_start|>user
The locker of the elephant is 4. The locker of the butterfly is 6. The locker of the sheep is 2. Max picked the sheep. Henry picked the⟦ butterfly⟧. Jack picked the elephant.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Butterfly', ' butterfly', ' Flint', ' butterflies', '蝴蝶', ' Turtle', ' Butter', ' Butler', ' Juliet', ' Flynn', ' Elliot', ' Falcon', ' Beetle', ' Bird', ' Whale', ' Willow', ' Swan', ' Marble', ' Elliott', ' Trout']

- write to slot 0 (norm 1.8523): best ordinal rank 990 (' two'), KL 0.0226; x8 lookup answer '4' (target); top 20: [' Butterfly', ' butterfly', ' Flint', ' butterflies', ' Turtle', '蝴蝶', ' Butter', ' Beetle', ' Juliet', ' Falcon', ' Butler', ' Cherry', ' Elliot', ' Whale', ' Bird', ' Willow', ' Flutter', ' Kitty', ' Panther', ' Flynn']
- identity to slot 0 (norm 1.8523): best ordinal rank 316 (' second'), KL 6.62; x8 lookup answer '4' (target); top 20: [' Sheep', ' sheep', ' Shepherd', ' Marsh', ' Shepard', ' Wool', ' shepherd', ' Sheila', ' chick', ' Wolves', ' Swan', ' Chick', ' Lucy', ' Wolf', ' Willie', ' Willow', ' Flint', ' Sheffield', ' Deer', ' flock']
- write to slot 2 (norm 1.0427): best ordinal rank 861 (' two'), KL 0.0265; x8 lookup answer '6' (original); top 20: [' Butterfly', ' butterfly', ' Flint', ' butterflies', '蝴蝶', ' Turtle', ' Juliet', ' Butter', ' Butler', ' Elliot', ' Flynn', ' Elliott', ' Falcon', ' Marble', ' Cherry', ' Beetle', ' Willow', ' Swan', ' Forrest', ' Shelley']
- identity to slot 2 (norm 1.0427): best ordinal rank 386 (' second'), KL 2.33; x8 lookup answer '6' (original); top 20: [' Butterfly', ' Sheep', ' Flint', ' butterfly', ' Shepherd', ' sheep', ' Flynn', ' Swan', ' Turtle', ' Willow', ' Whale', ' butterflies', ' Marsh', ' Willie', ' Quinn', ' chick', ' Chick', ' Bird', ' Shelley', ' Frog']

## C2-0195: bridge 'goose' in slot 2, digits by slot [2, 8, 7]

```
<|im_start|>user
The locker of the bear is 2. The locker of the pig is 8. The locker of the goose is 7. Eric picked the⟦ goose⟧. Iris picked the pig. Clara picked the bear.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Goose', ' goose', ' Gos', ' Moose', ' Moss', ' Goa', ' chick', ' Rosie', ' zo', ' GO', ' Gon', ' Gwen', ' Gecko', ' choir', ' Jessie', ' zoo', ' Ros', ' Georg', ' Ross', ' Zoo']

- write to slot 0 (norm 2.0969): best ordinal rank 941 (' three'), KL 0.0412; x8 lookup answer '2' (target); top 20: [' Goose', ' goose', ' Moose', ' Gos', ' Moss', ' chick', ' zo', ' zoo', ' hunter', ' flock', ' Chick', ' Zoo', ' Zo', ' Clover', ' bird', ' Goa', ' Frog', ' duck', ' Goat', ' GO']
- identity to slot 0 (norm 2.0969): best ordinal rank 691 (' third'), KL 5.4; x8 lookup answer '2' (target); top 20: [' Pig', ' pig', 'pig', ' pigs', ' chick', ' Pork', ' Hog', '猪', ' Chick', ' Frog', ' frog', ' Tig', ' Zo', '小猪', ' Flo', ' Tiger', ' sheep', ' hog', ' zo', ' Ros']
- write to slot 1 (norm 1.0427): best ordinal rank 1146 (' after'), KL 0.0218; x8 lookup answer '7' (original); top 20: [' Goose', ' goose', ' Gos', ' Moose', ' chick', ' Moss', ' Frog', ' Rosie', ' GO', ' frog', ' flock', ' Goa', ' Chick', ' zo', ' hunter', ' Goat', ' Gecko', ' choir', ' Gon', ' Fox']
- identity to slot 1 (norm 1.0427): best ordinal rank 607 (' third'), KL 1.08; x8 lookup answer '7' (original); top 20: [' Goose', ' goose', ' chick', ' Pig', ' Frog', ' Gos', ' Chick', ' Zo', ' frog', ' zo', ' pig', ' Moose', ' Ros', ' Moss', ' Hog', ' zoo', ' hunter', ' Zoo', ' Gon', ' pigs']

## C2-0103: bridge 'beetle' in slot 2, digits by slot [6, 2, 9]

```
<|im_start|>user
The locker of the chicken is 6. The locker of the tiger is 2. The locker of the beetle is 9. Tara picked the⟦ beetle⟧. Sean picked the tiger. Kate picked the chicken.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Beetle', ' beetle', ' Beet', ' beet', ' Flint', ' Colt', ' Beaver', ' Trout', ' Leopard', ' Beast', ' Crab', ' rept', ' Raider', ' Gecko', ' Abbott', ' Walton', ' leopard', ' Thief', ' Kelley', ' Trit']

- write to slot 0 (norm 2.0969): best ordinal rank 1547 (' two'), KL 0.0261; x8 lookup answer '9' (original); top 20: [' Beetle', ' beetle', ' Beet', ' beet', ' Beaver', ' Colt', ' Flint', ' Beast', ' Leopard', ' Trout', ' Crab', ' rept', ' leopard', ' Raider', ' Deer', ' Turtle', ' Bark', ' Celt', ' Malk', ' Ark']
- identity to slot 0 (norm 2.0969): best ordinal rank 706 (' third'), KL 6.48; x8 lookup answer '9' (original); top 20: [' Tiger', ' Tigers', ' tiger', ' Tig', ' Turtle', ' Trit', ' Titan', ' Hunter', ' Leopard', ' Trout', ' Flint', ' hunter', ' Panther', ' tig', ' Colt', ' leopard', ' Tucker', ' Ranger', ' turtle', ' Frog']
- write to slot 1 (norm 1.0427): best ordinal rank 1296 (' two'), KL 0.0154; x8 lookup answer '9' (original); top 20: [' Beetle', ' beetle', ' Beet', ' beet', ' Beaver', ' Colt', ' Flint', ' Trout', ' Beast', ' Crab', ' Leopard', ' rept', ' leopard', ' Frog', ' Raider', ' Thief', ' Gecko', ' Malk', ' Tribe', ' Abbott']
- identity to slot 1 (norm 1.0427): best ordinal rank 997 (' third'), KL 1.12; x8 lookup answer '9' (original); top 20: [' Beetle', ' beetle', ' Flint', ' Tiger', ' Colt', ' Trout', ' Leopard', ' Turtle', ' Trit', ' Beet', ' beet', ' leopard', ' hunter', ' Hunter', ' Frog', ' Raider', ' rept', ' Tigers', ' Beaver', ' Panther']

## C2-0007: bridge 'fly' in slot 1, digits by slot [3, 7, 5]

```
<|im_start|>user
The locker of the goose is 3. The locker of the fly is 7. The locker of the cat is 5. Lily picked the goose. Mia picked the cat. Eve picked the⟦ fly⟧.
Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Fly', ' Flynn', 'Fly', ' fly', ' Flyers', ' Flint', '-fly', ' Fox', ' Flying', ' Flo', ' Fry', ' Falk', ' flies', ' Fle', ' Fish', ' Fay', ' Pil', ' Pow', ' flyer', ' Ty']

- write to slot 0 (norm 1.8523): best ordinal rank 1290 (' three'), KL 0.114; x8 lookup answer '3' (target); top 20: [' Fly', ' Flynn', ' Flint', 'Fly', ' Flyers', ' fly', ' Fox', ' Flying', ' Flo', ' Falk', '-fly', ' Fry', ' flies', ' Fish', ' Fle', ' FL', ' Hawk', ' Pil', ' Ty', ' Falcon']
- identity to slot 0 (norm 1.8523): best ordinal rank 341 (' third'), KL 6.89; x8 lookup answer '3' (target); top 20: [' Goose', ' goose', ' Jessie', ' Moose', ' Jesse', ' Gos', ' Leopard', ' Seah', ' Leslie', ' Rosie', ' Moss', ' Maid', ' Gwen', ' Oswald', ' Duck', ' Poe', ' Rose', ' chick', ' Eagle', ' hunter']
- write to slot 2 (norm 1.0427): best ordinal rank 738 (' third'), KL 0.0545; x8 lookup answer '7' (original); top 20: [' Fly', ' Flynn', 'Fly', ' Flint', ' Flyers', ' Flo', ' fly', '-fly', ' Flying', ' Fry', ' Fox', ' flies', ' Falk', ' Fle', ' Fay', ' Ty', ' Pow', ' FL', ' Floyd', ' Fish']
- identity to slot 2 (norm 1.0427): best ordinal rank 335 (' third'), KL 2.84; x8 lookup answer '7' (original); top 20: [' Goose', ' Flynn', ' Fly', ' Fox', ' goose', ' Falk', ' Flint', ' Maid', ' Hawk', ' Duck', ' Frog', ' Miss', ' Willie', ' Fish', ' Flyers', ' Moose', ' Pow', ' chick', ' Chase', ' hunter']

## C2-0066: bridge 'cow' in slot 1, digits by slot [7, 2, 1]

```
<|im_start|>user
The locker of the owl is 7. The locker of the cow is 2. The locker of the lion is 1. Iris picked the lion. Ivy picked the⟦ cow⟧. Amy picked the owl.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Cow', 'Cow', ' cow', ' cows', 'cow', ' Coy', ' Cowboy', ' Cowboys', ' Chick', ' cattle', ' Chow', ' Lucy', ' Cock', ' sheep', ' Corn', ' Bov', ' Duck', ' Cro', ' cowboy', ' chick']

- write to slot 0 (norm 1.8523): best ordinal rank 1582 (' third'), KL 0.0209; x8 lookup answer '7' (target); top 20: [' Cow', 'Cow', ' cow', ' cows', ' Cowboy', ' Cowboys', ' Coy', ' Chick', ' cattle', 'cow', ' sheep', ' Duck', ' Chicken', ' Corn', ' chickens', ' Cock', ' cowboy', ' Lucy', ' Clover', ' Sheep']
- identity to slot 0 (norm 1.8523): best ordinal rank 656 (' second'), KL 6.02; x8 lookup answer '7' (target); top 20: [' Owl', ' owl', ' Owen', ' chick', ' OW', ' robin', ' Cow', ' Ow', ' bird', ' fox', 'OWL', ' Chick', ' Oswald', ' Coy', ' Milo', ' Willow', ' goose', ' wolf', ' Wolf', ' Lucy']
- write to slot 2 (norm 1.0427): best ordinal rank 1076 (' third'), KL 0.00514; x8 lookup answer '2' (original); top 20: [' Cow', 'Cow', ' cow', ' cows', ' Cowboy', ' Coy', 'cow', ' Cowboys', ' Chick', ' Chow', ' Lucy', ' cattle', ' Corn', ' Cock', ' cowboy', ' Bov', ' Cec', ' Owen', ' Coke', ' Kelly']
- identity to slot 2 (norm 1.0427): best ordinal rank 733 (' second'), KL 1; x8 lookup answer '2' (original); top 20: [' Cow', ' Owl', ' cow', ' owl', 'Cow', ' Coy', ' Owen', ' Chick', ' chick', ' cows', ' Cowboy', ' robin', ' Lucy', ' OW', ' fox', ' Ow', ' Fox', ' Hog', ' goose', ' sheep']

## C2-0128: bridge 'owl' in slot 1, digits by slot [5, 7, 2]

```
<|im_start|>user
The locker of the fox is 5. The locker of the owl is 7. The locker of the lion is 2. Max picked the⟦ owl⟧. Rose picked the lion. Mark picked the fox.
Which locker belongs to Max's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Owl', ' owl', ' Owen', ' OW', ' chick', ' XO', ' Ow', 'OWL', ' bird', ' Hawk', ' Wolf', ' Zoo', ' robin', 'owl', ' Fox', ' Eagle', ' Turtle', ' fox', ' Skyl', ' WO']

- write to slot 0 (norm 1.8523): best ordinal rank 1476 (' three'), KL 0.0234; x8 lookup answer '5' (target); top 20: [' Owl', ' owl', ' Owen', ' chick', ' OW', ' bird', ' XO', ' Zoo', ' Eagle', ' Turtle', ' Wolf', ' Merlin', ' zo', ' wolf', ' zoo', ' turtle', ' Willow', ' Hawk', ' Oak', ' Whale']
- identity to slot 0 (norm 1.8523): best ordinal rank 1320 (' two'), KL 10.8; x8 lookup answer '5' (target); top 20: [' Fox', ' fox', 'Fox', ' FOX', '狐狸', 'fox', '福克斯', 'FOX', ' Rox', '狐', ' XO', ' Rex', ' Pix', ' FO', ' Vox', ' xo', ' Felix', ' Xen', ' Xo', ' Wolf']
- write to slot 2 (norm 1.0427): best ordinal rank 1570 (' two'), KL 0.00396; x8 lookup answer '7' (original); top 20: [' Owl', ' owl', ' Owen', ' OW', ' XO', ' chick', 'OWL', ' Merlin', ' Ow', ' Zoo', ' Skyl', ' Oswald', ' Hawk', ' Olivia', ' WO', ' Loki', ' Owens', ' Eagle', 'owl', ' Wolf']
- identity to slot 2 (norm 1.0427): best ordinal rank 1182 (' two'), KL 2.86; x8 lookup answer '7' (original); top 20: [' Fox', ' fox', ' Owl', ' FOX', 'Fox', ' owl', ' XO', '狐狸', 'fox', ' Rox', ' Wolf', ' FO', ' xo', 'FOX', '福克斯', ' wolf', ' Xo', ' chick', ' Frog', ' hunter']

## C2-0119: bridge 'duck' in slot 0, digits by slot [5, 7, 8]

```
<|im_start|>user
The locker of the duck is 5. The locker of the eagle is 7. The locker of the spider is 8. Sara picked the⟦ duck⟧. Ruby picked the spider. Anna picked the eagle.
Which locker belongs to Sara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Duck', ' duck', ' Ducks', ' ducks', ' Chick', 'duck', '鸭', '小鸭', ' Deer', ' chick', '鸭子', '鴨', ' Bird', ' DK', ' Dud', ' Daisy', ' bird', ' Dund', ' Maid', ' Turtle']

- write to slot 1 (norm 1.8523): best ordinal rank 3401 (' second'), KL 0.00166; x8 lookup answer '7' (target); top 20: [' Duck', ' duck', ' Ducks', ' ducks', 'duck', ' Chick', '鸭', '小鸭', ' chick', '鸭子', '鴨', ' Deer', ' Dud', ' Bird', ' Maid', ' Frog', ' DK', ' Daisy', ' bird', ' Dund']
- identity to slot 1 (norm 1.8523): best ordinal rank 3055 (' third'), KL 4.31; x8 lookup answer '7' (target); top 20: [' Spider', 'Spider', ' spider', ' spiders', ' Duck', '蜘蛛', ' Chick', ' Tiger', ' Deer', ' duck', ' chick', ' Frog', ' Bird', ' lizard', ' frog', ' tiger', ' Turtle', ' turtle', ' deer', ' dragon']
- write to slot 2 (norm 2.0969): best ordinal rank 2836 (' third'), KL 0.00248; x8 lookup answer '8' (target); top 20: [' Duck', ' duck', ' Ducks', ' ducks', 'duck', ' Chick', '鸭', '小鸭', ' chick', '鸭子', ' Dud', ' Daisy', ' DK', '鴨', ' Deer', ' Maid', ' Bird', ' Dudley', ' Dund', ' Frog']
- identity to slot 2 (norm 2.0969): best ordinal rank 2618 ('one'), KL 7.03; x8 lookup answer '8' (target); top 20: [' Spider', 'Spider', ' spider', ' spiders', '蜘蛛', ' Tiger', ' Chick', ' lizard', ' Frog', ' Deer', ' chick', ' Duck', ' Bird', ' frog', ' tiger', ' Zoo', ' dragon', ' deer', ' turtle', ' Hunter']

## C2-0100: bridge 'fly' in slot 1, digits by slot [4, 1, 7]

```
<|im_start|>user
The locker of the goat is 4. The locker of the fly is 1. The locker of the turkey is 7. Ryan picked the turkey. Victor picked the⟦ fly⟧. Peter picked the goat.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Fly', 'Fly', ' Flynn', ' Flint', ' fly', '-fly', ' Fry', ' Fox', ' Flyers', ' Flo', ' Fay', ' Flying', ' Falk', ' flies', ' FL', ' Fle', ' Frog', ' Floyd', ' Fl', ' Fish']

- write to slot 0 (norm 1.8523): best ordinal rank 1379 (' two'), KL 0.0971; x8 lookup answer '4' (target); top 20: [' Fly', ' Flynn', 'Fly', ' Flint', ' fly', ' Fox', ' FL', ' Fry', ' Flo', ' Falk', ' Flying', '-fly', ' Flor', ' Flyers', ' Fle', ' Fl', ' flies', ' Fay', ' Falcon', ' Fish']
- identity to slot 0 (norm 1.8523): best ordinal rank 441 (' second'), KL 7.11; x8 lookup answer '4' (target); top 20: [' turkey', ' Turkey', ' Tracy', ' TUR', ' Turk', ' Tyler', ' Turtle', ' Troy', ' hunter', ' tur', ' turtle', ' Trout', ' Tur', ' chick', ' Lucy', ' Thompson', ' duck', ' Tiger', 'Turkey', ' Turks']
- write to slot 2 (norm 1.0427): best ordinal rank 1155 (' two'), KL 0.0389; x8 lookup answer '1' (original); top 20: [' Fly', ' Flynn', 'Fly', ' Flint', ' fly', ' Flo', '-fly', ' Fry', ' FL', ' Fay', ' Flyers', ' Flying', ' Floyd', ' Falk', ' Flor', ' flies', ' Fle', ' Fox', ' Fl', 'FL']
- identity to slot 2 (norm 1.0427): best ordinal rank 488 (' two'), KL 2.96; x8 lookup answer '1' (original); top 20: [' Flynn', ' Flint', ' Falk', ' Fly', ' turkey', ' Fox', ' chick', ' Fry', ' hunter', ' Falcon', ' Turkey', ' Lucy', ' Tracy', ' frog', ' bird', ' duck', ' Chick', ' Hunter', ' Troy', ' Frog']

## C2-0078: bridge 'butterfly' in slot 2, digits by slot [9, 7, 6]

```
<|im_start|>user
The locker of the lion is 9. The locker of the cow is 7. The locker of the butterfly is 6. Leo picked the⟦ butterfly⟧. Ben picked the lion. Paul picked the cow.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Butterfly', ' butterfly', ' butterflies', '蝴蝶', ' Butter', ' Flint', ' Turtle', ' Flutter', ' Beetle', '蝶', ' Frog', ' Butler', ' Fly', ' Falcon', ' Whale', ' Bird', ' Spider', ' Willow', ' Fairy', ' Dragon']

- write to slot 0 (norm 2.0969): best ordinal rank 1305 (' Three'), KL 0.0219; x8 lookup answer '6' (original); top 20: [' Butterfly', ' butterfly', ' butterflies', '蝴蝶', ' Butter', ' Turtle', ' Flutter', ' Flint', ' Beetle', ' Whale', ' Bird', ' Dragon', ' Falcon', '蝶', ' Frog', ' Willow', ' Trout', ' Spider', ' Dolphin', ' Deer']
- identity to slot 0 (norm 2.0969): best ordinal rank 1291 (' third'), KL 8.98; x8 lookup answer '6' (original); top 20: [' Cow', 'Cow', ' cow', ' cows', ' Chick', ' Frog', ' Duck', ' Cowboy', 'cow', ' Cowboys', ' Coy', ' Clover', ' Fox', ' Pig', ' chick', ' frog', ' Chicken', ' Chow', ' Maid', ' Cock']
- write to slot 1 (norm 1.0427): best ordinal rank 1494 (' Three'), KL 0.00784; x8 lookup answer '6' (original); top 20: [' Butterfly', ' butterfly', ' butterflies', '蝴蝶', ' Butter', ' Turtle', ' Flint', ' Flutter', ' Frog', ' Beetle', ' Fly', ' Whale', ' Bird', '蝶', ' Falcon', ' Trout', ' Butler', ' Spider', ' Willow', ' Dolphin']
- identity to slot 1 (norm 1.0427): best ordinal rank 920 (' third'), KL 1.2; x8 lookup answer '6' (original); top 20: [' Butterfly', ' butterfly', ' Frog', ' butterflies', ' Turtle', ' Flint', ' Duck', ' Chick', ' Whale', ' Butter', ' Cow', ' Trout', ' Bird', '蝴蝶', ' Willow', ' Clover', ' Spider', ' Daisy', ' Fly', ' chick']

## C2-0116: bridge 'cat' in slot 2, digits by slot [3, 9, 8]

```
<|im_start|>user
The locker of the goat is 3. The locker of the bee is 9. The locker of the cat is 8. Anna picked the⟦ cat⟧. Laura picked the bee. Alice picked the goat.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Cat', ' CAT', 'Cat', ' Cats', 'CAT', ' cats', '小猫', '卡特', ' Kat', ' cat', '猫', 'cat', ' Kitty', ' Catan', 'Kat', ' Cath', ' kitty', 'cats', '-cat', '.cat']

- write to slot 0 (norm 2.0969): best ordinal rank 2257 (' third'), KL 0.0106; x8 lookup answer '3' (target); top 20: [' Cat', ' CAT', ' Cats', 'Cat', 'CAT', ' cats', '小猫', ' cat', ' Kat', '卡特', '猫', ' kitty', ' Kitty', ' Catan', ' Cart', 'cat', ' CT', 'Kat', ' Cath', ' Chick']
- identity to slot 0 (norm 2.0969): best ordinal rank 708 (' third'), KL 9.73; x8 lookup answer '3' (target); top 20: [' Bee', ' bee', ' bees', ' Miner', ' Chick', 'bee', ' Beaver', ' Maid', ' Cain', ' chick', ' Thief', ' miner', ' Robbie', ' Mae', ' Kee', ' Maia', ' Mall', ' Bird', ' Cec', ' Bella']
- write to slot 1 (norm 1.0427): best ordinal rank 1865 (' third'), KL 0.00392; x8 lookup answer '8' (original); top 20: [' Cat', ' CAT', ' Cats', 'Cat', 'CAT', ' cats', '小猫', ' cat', '猫', '卡特', ' Kat', ' Kitty', ' kitty', 'cat', ' Cart', 'Kat', '-cat', ' Cath', 'cats', '.cat']
- identity to slot 1 (norm 1.0427): best ordinal rank 673 (' third'), KL 2.36; x8 lookup answer '8' (original); top 20: [' Cat', ' Chick', ' Cats', ' CAT', ' Cain', ' chick', ' Cai', ' Colt', ' Chip', 'Cat', ' Cam', ' Catan', ' Maid', ' Caj', ' CIC', ' Tom', ' Tiger', ' Kitty', ' Chase', 'CAT']

