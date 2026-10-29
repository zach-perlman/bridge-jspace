# Examples: nem35l_x52_verbal

10 random items (seed 0) of 100. The write h + 2 (mu_k - mu_j) is added at ⟦...⟧; the lens reads the same position. UNVERIFIED.

## C2-0108: bridge 'goat' in slot 0, digits by slot [2, 1, 9]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the goat is 2. The locker of the bear is 1. The locker of the crow is 9. Sean picked the crow. Amy picked the⟦ goat⟧. Diana picked the bear.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' goat', ' goats', ' Gira', ' sheep', ' dairy', ' Rabbit', ' Animal', ' Girl', ' Leah', ' Girls', ' animal', ' Mont', ' Milk', ' livestock', ' girls', ' Mah', ' Women', ' vegetarian', ' Jordan', ' women']

- write to slot 1 (norm 6.6864): best ordinal rank 630 (' third'), KL 0.0105; x8 lookup answer '1' (target); top 20: [' goat', ' goats', ' Girls', ' girls', ' Girl', ' Gira', ' sheep', ' women', ' livestock', ' Women', ' Rabbit', ' dairy', ' animal', ' Animal', ' Leah', ' orphan', ' Jordan', ' vegetarian', ' Grass', ' girl']
- identity to slot 1 (norm 6.6864): best ordinal rank 444 (' third'), KL 2.57; x8 lookup answer '1' (target); top 20: [' Crow', ' Raven', ' crow', ' goat', ' Swan', ' Gob', ' Ravens', ' ,', " ''", ' goats', ' Hawk', ' ``', ' Fish', ' Rose', ' Bird', ' Rabbit', ' Gra', ' Hog', ' Sow', " '"]
- write to slot 2 (norm 8.0427): best ordinal rank 398 (' third'), KL 0.00248; x8 lookup answer '1' (third); top 20: [' goat', ' goats', ' Gira', ' sheep', ' Girls', ' girls', ' Jordan', ' Girl', ' Leah', ' dairy', ' women', ' vegetarian', ' Rabbit', ' animal', ' Grass', ' Greene', ' orphan', ' Mont', ' Women', ' ‘']
- identity to slot 2 (norm 8.0427): best ordinal rank 424 (' third'), KL 7.14; x8 lookup answer '1' (third); top 20: [' Crow', ' crow', ' Raven', ' Ravens', ' Swan', ' Crowley', ' Gob', ' ,', ' Hawk', ' Bird', " ''", ' Shaw', ' Hawks', ' ``', ' Sow', ' Dove', ' Gra', " '", ' Hog', ' Rose']

## C2-0228: bridge 'fox' in slot 0, digits by slot [8, 6, 4]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the fox is 8. The locker of the owl is 6. The locker of the duck is 4. Kate picked the duck. Beth picked the⟦ fox⟧. Jack picked the owl.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Fox', ' fox', ' Wolf', ' Fish', 'Fox', ' Falcon', ' ,', ' FOX', ' Lion', ' Rose', ' Phoenix', ' the', " '", ' Rosa', ' Rox', ' fish', ' to', ' Black', ' and', ' Mc']

- write to slot 1 (norm 6.6864): best ordinal rank 246 (' one'), KL 0.0321; x8 lookup answer '6' (target); top 20: [' Fox', ' fox', ' Fish', ' ,', ' Wolf', 'Fox', ' Falcon', ' Rox', " '", ' Rose', ' FOX', ' hog', ' Rosa', ' fish', ' Phoenix', ' Hog', ' Coy', ' the', ' Mc', ' to']
- identity to slot 1 (norm 6.6864): best ordinal rank 104 (' one'), KL 6.11; x8 lookup answer '6' (target); top 20: [' ,', ' Wolf', " '", ' Falcon', ' the', ' Swan', ' Hog', ' Fish', ' Raven', ' to', ' Rose', ' Ot', ' owl', ' and', ' rem', ' Shaw', ' Ow', ' a', ' orphan', ' that']
- write to slot 2 (norm 8.0427): best ordinal rank 170 (' one'), KL 0.133; x8 lookup answer '6' (third); top 20: [' Fox', ' ,', ' fox', ' Wolf', ' Fish', ' Rosa', 'Fox', " '", ' Falcon', ' Rose', ' Rox', ' Phoenix', ' the', ' and', ' to', ' hog', ' Hog', ' Black', ' fish', ' FOX']
- identity to slot 2 (norm 8.0427): best ordinal rank 106 (' one'), KL 7.95; x8 lookup answer '6' (third); top 20: [' ,', ' owl', " '", ' Swan', ' the', ' Wolf', ' Ow', ' Falcon', ' Shaw', ' Ot', ' Raven', ' Hog', ' to', ' Rose', ' rem', ' and', ' Fish', ' a', ' orphan', ' ']

## C2-0125: bridge 'deer' in slot 2, digits by slot [9, 4, 2]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the cow is 9. The locker of the chicken is 4. The locker of the deer is 2. Julia picked the chicken. Jack picked the⟦ deer⟧. Emma picked the cow.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Deer', ' deer', ' animal', ' ,', ' animals', ' ‘', ' elk', '鹿', ' Loch', ' Animal', " '", ' hunter', ' ced', ' Elk', ' Dew', ' Leopard', ' ``', ' Hunter', ' the', ' ']

- write to slot 0 (norm 8.0427): best ordinal rank 401 (' one'), KL 0.0145; x8 lookup answer '9' (target); top 20: [' Deer', ' deer', ' animal', ' elk', ' Animal', ' animals', '鹿', ' Elk', ' Hunter', ' hunter', ' Loch', ' ,', ' ``', ' Bush', ' Edel', ' Weir', ' Pet', ' Fish', ' Animals', ' ‘']
- identity to slot 0 (norm 8.0427): best ordinal rank 303 (' third'), KL 10.8; x8 lookup answer '9' (target); top 20: [' Chicken', ' Chick', ' chickens', ' chicken', ' poultry', ' Poul', ' Crane', ' animal', ' Chih', ' Animal', ' chick', ' Hen', ' animals', ' ,', ' CH', ' Hens', ' hens', ' Swan', ' Hunter', ' Bird']
- write to slot 1 (norm 3.5601): best ordinal rank 232 (' third'), KL 0.00285; x8 lookup answer '2' (original); top 20: [' Deer', ' deer', ' animal', ' elk', ' animals', '鹿', ' ,', ' Animal', ' Loch', ' ‘', ' hunter', ' Fish', " '", ' Bush', ' Hunter', ' Elk', ' wildlife', ' ``', ' Leopard', ' Animals']
- identity to slot 1 (norm 3.5601): best ordinal rank 123 (' third'), KL 0.281; x8 lookup answer '2' (original); top 20: [' Deer', ' deer', ' animal', ' ,', ' animals', ' Animal', ' Chick', ' Hunter', ' ‘', ' hunter', " '", ' Crane', ' Chih', ' Fish', ' Creek', ' Bush', ' Animals', ' Hen', ' elk', ' Kra']

## C2-0013: bridge 'spider' in slot 2, digits by slot [9, 7, 2]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the lion is 9. The locker of the deer is 7. The locker of the spider is 2. Eve picked the deer. Lily picked the lion. Mark picked the⟦ spider⟧.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Spider', ' spider', 'Spider', ' craw', ' Craw', ' Spy', ' crawling', ' Snake', ' ,', ' SP', ' SW', ' sponge', ' crawl', ' Schwe', ' Wagner', ' crawled', ' SPD', ' Kra', ' Apache', ' Scorp']

- write to slot 0 (norm 8.0427): best ordinal rank 469 (' one'), KL 0.0598; x8 lookup answer '2' (original); top 20: [' Spider', ' spider', 'Spider', ' craw', ' Craw', ' crawling', ' Spy', ' Snake', ' crawled', ' Schwe', ' Wagner', ' SW', ' crawl', ' SP', ' ,', ' Logan', ' Scorp', ' Pig', 'Spy', ' Panther']
- identity to slot 0 (norm 8.0427): best ordinal rank 107 (' third'), KL 7.58; x8 lookup answer '2' (original); top 20: [' ,', ' Deer', ' deer', ' the', " '", ' ', ' ...', ' \\"', ' an', ' -', ' ``', ' ‘', ' ?', ' a', "\\'", ' of', ' and', ' Loch', ' Schwe', ' School']
- write to slot 1 (norm 3.5601): best ordinal rank 491 (' one'), KL 0.00756; x8 lookup answer '2' (original); top 20: [' Spider', ' spider', 'Spider', ' craw', ' Craw', ' Spy', ' crawling', ' Snake', ' SW', ' crawl', ' crawled', ' SP', ' Schwe', ' ,', ' Pig', ' Wagner', 'Spy', ' sponge', ' SPD', ' spy']
- identity to slot 1 (norm 3.5601): best ordinal rank 150 (' third'), KL 0.0163; x8 lookup answer '2' (original); top 20: [' Spider', ' spider', 'Spider', ' ,', ' Schwe', ' SW', ' craw', ' Spy', ' the', " '", ' Kra', ' Wagner', ' Scot', ' -', ' ...', ' ', ' SPD', ' Craw', ' Griffin', ' an']

## C2-0080: bridge 'wolf' in slot 1, digits by slot [8, 6, 5]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the horse is 8. The locker of the wolf is 6. The locker of the bee is 5. Eve picked the⟦ wolf⟧. Iris picked the bee. Grace picked the horse.
Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Wolf', ' wolf', ' Wolves', ' Wolff', ' wolves', 'Wolf', ' Wolfe', ' hog', ' Hog', ' ,', ' the', " '", ' and', ' Mc', ' to', ' Pig', ' Lew', ' Black', ' pig', ' Logan']

- write to slot 0 (norm 6.6864): best ordinal rank 133 (' three'), KL 0.0133; x8 lookup answer '8' (target); top 20: [' Wolf', ' wolf', ' Wolves', ' Wolff', 'Wolf', ' wolves', ' Wolfe', ' hog', ' the', ' Hog', ' Wolver', ' and', ' Logan', ' to', ' ,', ' Lew', " '", ' Mc', ' Black', ' W']
- identity to slot 0 (norm 6.6864): best ordinal rank 322 (' one'), KL 1.29; x8 lookup answer '8' (target); top 20: [' Wolf', ' ,', ' Bee', ' Bell', " '", ' Mc', ' Rose', ' Blue', ' Black', ' and', ' the', ' Logan', ' Fish', ' Wolfe', ' Pig', ' hog', ' Rabbit', ' to', ' Wolff', ' ']
- write to slot 2 (norm 3.5601): best ordinal rank 109 (' three'), KL 0.00923; x8 lookup answer '6' (original); top 20: [' Wolf', ' Wolff', ' wolf', ' Wolves', ' wolves', 'Wolf', ' Wolfe', ' hog', ' ,', ' the', ' Hog', ' and', " '", ' to', ' ', ' Black', ' Logan', ' Mc', ' W', ' Lew']
- identity to slot 2 (norm 3.5601): best ordinal rank 218 (' one'), KL 0.0852; x8 lookup answer '6' (original); top 20: [' Wolf', ' Wolff', ' Wolves', ' wolf', ' Wolfe', ' wolves', 'Wolf', ' ,', ' hog', " '", ' the', ' Mc', ' and', ' Black', ' Logan', ' Hog', ' Pig', ' to', ' Lew', ' Rose']

## C2-0156: bridge 'eagle' in slot 0, digits by slot [6, 1, 2]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the eagle is 6. The locker of the goat is 1. The locker of the elephant is 2. Alice picked the goat. David picked the⟦ eagle⟧. Lily picked the elephant.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Eagle', ' Eagles', ' eagle', ' Eag', ' Falcon', ' Lion', ' ,', ' Hawk', ' Raven', ' the', " '", ' E', ' Swan', ' Leon', ' Hawks', ' Logan', ' lion', ' crow', ' Mc', ' Lions']

- write to slot 1 (norm 6.6864): best ordinal rank 110 (' one'), KL 0.00651; x8 lookup answer '1' (target); top 20: [' Eagle', ' Eagles', ' eagle', ' Eag', ' Falcon', ' ,', " '", ' Lion', ' the', ' E', ' Raven', ' Hawk', ' Mc', ' Swan', ' Hawks', ' Gale', ' Leon', ' crow', ' lion', ' -']
- identity to slot 1 (norm 6.6864): best ordinal rank 147 (' one'), KL 0.486; x8 lookup answer '1' (target); top 20: [' Eagle', ' goat', ' ,', " '", ' Eagles', ' the', ' Swan', ' Lion', ' goats', ' Fish', ' Leon', ' Elk', ' Raven', ' Falcon', ' to', ' Logan', ' Salmon', ' Eag', ' a', ' Ele']
- write to slot 2 (norm 8.0427): best ordinal rank 91 (' one'), KL 0.00899; x8 lookup answer '2' (target); top 20: [' Eagle', ' Eagles', ' eagle', ' Eag', ' ,', ' Falcon', " '", ' E', ' the', ' Raven', ' Lion', ' Leon', ' Swan', ' Gale', ' ', ' Mc', ' Hawks', ' crow', ' -', ' to']
- identity to slot 2 (norm 8.0427): best ordinal rank 189 (' one'), KL 2.84; x8 lookup answer '2' (target); top 20: [' goat', ' Eagle', ' goats', ' ,', " '", ' Swan', ' the', ' Fish', ' Lion', ' Elk', ' Leon', ' Salmon', ' Rabbit', ' Gou', ' Raven', ' Animal', ' to', ' Wolf', ' fish', ' animal']

## C2-0145: bridge 'bee' in slot 2, digits by slot [2, 9, 8]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the deer is 2. The locker of the cat is 9. The locker of the bee is 8. Lily picked the⟦ bee⟧. Max picked the deer. Liam picked the cat.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Bee', ' bee', ' Berry', ' Bell', ' Butter', ' bees', ' Fish', ' ,', ' Griffin', ' Rose', ' Rab', ' her', ' Rabbit', ' Raven', " '", ' the', ' Logan', ' Baker', ' Blue', ' Ye']

- write to slot 0 (norm 8.0427): best ordinal rank 526 (' one'), KL 0.0911; x8 lookup answer '2' (target); top 20: [' Bee', ' bee', ' Berry', ' Fish', ' bees', ' Bell', ' Rabbit', ' Rab', ' Butter', ' Beck', ' Raven', ' Logan', ' Eagle', ' Honey', ' Bird', ' her', ' Baker', ' Griffin', ' Rose', ' Ye']
- identity to slot 0 (norm 8.0427): best ordinal rank 502 (' one'), KL 6.13; x8 lookup answer '2' (target); top 20: [' Cat', ' Rabbit', ' Cats', ' Fish', ' Pet', ' cats', ' Bat', ' Ot', ' her', ' cat', ' Animal', ' Butter', ' Logan', ' Cotton', ' ,', ' Rose', ' Lily', ' Kitty', ' Rab', ' \\"']
- write to slot 1 (norm 3.5601): best ordinal rank 499 (' one'), KL 0.0147; x8 lookup answer '8' (original); top 20: [' Bee', ' bee', ' Fish', ' Berry', ' Bell', ' bees', ' Rabbit', ' Butter', ' Rab', ' her', ' Griffin', ' Bird', ' Rose', ' Girl', " '", ' Raven', ' Baker', ' Blue', ' ,', ' Ye']
- identity to slot 1 (norm 3.5601): best ordinal rank 330 (' one'), KL 0.618; x8 lookup answer '8' (original); top 20: [' Bee', ' Fish', ' Rabbit', ' Bell', ' Butter', ' Berry', ' ,', ' her', ' Rose', ' Rab', ' Logan', " '", ' bee', ' Baker', ' the', ' Pet', ' Griffin', ' \\"', ' Girl', ' ']

## C2-0121: bridge 'deer' in slot 2, digits by slot [9, 8, 5]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the spider is 9. The locker of the cow is 8. The locker of the deer is 5. Paul picked the spider. Eve picked the⟦ deer⟧. Kate picked the cow.
Which locker belongs to Eve's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Deer', ' deer', ' ,', ' ‘', ' ', " '", ' \\"', ' the', ' animal', ' women', ' girls', ' Loch', ' Fish', ' and', ' ced', ' of', ' ``', ' an', ' that', ' to']

- write to slot 0 (norm 8.0427): best ordinal rank 111 (' one'), KL 0.312; x8 lookup answer '9' (target); top 20: [' Deer', ' deer', ' ,', ' animal', ' Fish', ' Elk', ' the', ' elk', ' ``', ' Animal', " '", ' \\"', ' Loch', ' ‘', ' School', ' ', ' Lew', ' an', ' women', ' to']
- identity to slot 0 (norm 8.0427): best ordinal rank 47 (' third'), KL 10.9; x8 lookup answer '9' (target); top 20: [' Spider', ' spider', 'Spider', ' craw', ' ,', ' crawling', ' ara', ' Spy', ' Craw', ' sponge', " '", ' girls', ' women', ' Iris', ' Kra', ' \\"', ' sister', ' the', ' mars', ' spy']
- write to slot 1 (norm 3.5601): best ordinal rank 60 (' third'), KL 0.0648; x8 lookup answer '5' (original); top 20: [' Deer', ' deer', ' ,', ' girls', ' Fish', ' women', " '", ' animal', ' \\"', ' ‘', ' Women', ' the', ' ', ' Girls', ' Loch', ' ``', ' Lew', ' Ladies', ' Carroll', ' lady']
- identity to slot 1 (norm 3.5601): best ordinal rank 28 (' third'), KL 0.969; x8 lookup answer '5' (original); top 20: [' ,', ' Deer', ' deer', ' spider', ' Spider', " '", ' ‘', ' \\"', ' the', ' ', ' women', ' girls', ' animal', ' and', ' an', ' a', ' to', ' of', ' Women', ' ``']

## C2-0087: bridge 'camel' in slot 0, digits by slot [1, 4, 9]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the camel is 1. The locker of the eagle is 4. The locker of the tick is 9. Vera picked the tick. Kyle picked the⟦ camel⟧. Emma picked the eagle.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Camel', ' camel', " '", ' ,', ' the', ' Cadillac', ' Crane', ' Mc', ' Cam', ' cam', "\\'", ' Ca', ' crane', ' to', ' Musk', ' a', ' CS', ' »', ' cadet', ' Swan']

- write to slot 1 (norm 6.6864): best ordinal rank 268 (' one'), KL 0.0148; x8 lookup answer '4' (target); top 20: [' Camel', ' camel', " '", ' ,', ' the', ' Mc', ' cam', "\\'", ' cadet', ' Crane', ' \\"', ' Cam', ' Cadillac', ' CAM', ' ', " ''", ' Camden', ' Cad', ' to', ' a']
- identity to slot 1 (norm 6.6864): best ordinal rank 467 (' one'), KL 3.75; x8 lookup answer '4' (target); top 20: [' Rabbit', " ''", " '", ' Crane', ' »', ' ``', ' ,', ' Truck', ' the', ' camel', ' Camel', ' Hunter', ' Musk', ' Zeb', ' Logan', ' Hawk', ' cadet', ' \\"', ' Pike', ' ank']
- write to slot 2 (norm 8.0427): best ordinal rank 203 (' one'), KL 0.00816; x8 lookup answer '4' (third); top 20: [' Camel', ' camel', ' ,', " '", ' the', "\\'", ' cadet', ' ', ' Cad', ' cam', ' \\"', ' Carmel', ' Mc', ' Cam', ' Ca', ' Crane', ' and', ' a', ' to', ' ‘']
- identity to slot 2 (norm 8.0427): best ordinal rank 706 (' one'), KL 7.23; x8 lookup answer '4' (third); top 20: [' Rabbit', " ''", ' ``', ' »', ' Crane', ' Truck', " '", ' Hawk', ' Peck', ' ank', ' ,', ' Hunter', 'ank', ' rabbit', ' tick', ' Mouse', ' Logan', ' Zeb', ' Pike', ' the']

## C2-0143: bridge 'chicken' in slot 0, digits by slot [5, 9, 1]

```
<|im_start|>system
<|im_end|>
<|im_start|>user
The locker of the chicken is 5. The locker of the spider is 9. The locker of the dog is 1. Maria picked the⟦ chicken⟧. Olivia picked the dog. Lucy picked the spider.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer: 
```

Lens top 20, h alone: [' Chicken', ' Chick', ' chicken', ' Poul', ' poultry', ' chickens', ' chick', ' Cotton', ' hens', ' Fish', ' Bird', ' Egg', ' Rabbit', ' Crane', ' Cherry', ' CH', ' Hens', ' Jenny', ' Feather', ' Girls']

- write to slot 1 (norm 6.6864): best ordinal rank 1462 (' Third'), KL 0.0208; x8 lookup answer '9' (target); top 20: [' Chicken', ' Chick', ' poultry', ' chicken', ' Poul', ' chickens', ' Cotton', ' Fish', ' Girls', ' hens', ' chick', ' Bird', ' Jenny', ' girls', ' Hens', ' CH', ' Crane', ' Duck', ' Rabbit', ' Egg']
- identity to slot 1 (norm 6.6864): best ordinal rank 4164 (' One'), KL 2.47; x8 lookup answer '9' (target); top 20: [' Animal', ' Dogs', ' Fish', ' Chicken', ' Pig', ' Rabbit', ' Dog', ' Pet', 'Animal', ' Animals', ' Bird', ' School', ' Chick', ' animal', ' dogs', ' Hog', ' Girl', ' Horse', ' hog', ' Girls']
- write to slot 2 (norm 8.0427): best ordinal rank 836 (' Third'), KL 0.0141; x8 lookup answer '1' (target); top 20: [' Chicken', ' Chick', ' chicken', ' poultry', ' Poul', ' chickens', ' Cotton', ' hens', ' CH', ' Hens', ' chick', ' Cottage', ' Fish', ' Girls', ' Jenny', ' Crane', ' Egg', ' Bird', ' Chloe', ' girls']
- identity to slot 2 (norm 8.0427): best ordinal rank 4491 ('one'), KL 6.37; x8 lookup answer '1' (target); top 20: [' Animal', ' Dogs', ' Dog', ' Fish', ' Pig', ' Pet', ' Rabbit', 'Animal', ' dogs', ' Animals', ' Hog', ' animal', ' hog', ' canine', ' School', ' Bird', ' pig', ' Chicken', ' Drum', ' pigs']

