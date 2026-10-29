# 53.1 word cells: what the recall answered (9B, qwen35_9b_x53_2x2_words; descriptive, UNVERIFIED)

CPU only, from the run's stored competence rows (8 greedy tokens per unedited O / S prompt, the said word and the read); no rule, no rerun. The read step's top token is the greedy continuation's first token (greedy decoding takes it; re-encoded here from the stored text). Prompts rebuilt on the tokenizer and matched scene by scene. Descriptive context for the card only.

## (Q-after, word): recall, 382 prompts (O and S of each scene)

Read right 145 / 382; said right 145 / 382.

First word's kind: the asked pick itself (the animal) 236; the class (right) 145; another class word 1.

Top first tokens: ' In' 47, ' bird' 30, ' Bird' 30, ' tick' 21, ' M' 15, ' beetle' 13, ' Ar' 12, ' spider' 11, ' butterfly' 9, ' Sheep' 9, ' chicken' 9, ' ant' 8, ' Rabbit' 8, ' Pig' 8, ' eagle' 7.

Read wrong by gold class: amphibian 6 / 10; arachnid 34 / 53; bird 53 / 112; insect 39 / 87; mammal 105 / 120.

## (Q-before, word): recall, 382 prompts (O and S of each scene)

Read right 351 / 382; said right 351 / 382.

First word's kind: the class (right) 351; the asked pick itself (the animal) 19; another class word 12.

Top first tokens: ' Bird' 111, ' M' 108, ' In' 95, ' Ar' 38, ' Amph' 10, ' Dog' 2, ' Bee' 2, ' Tick' 2, ' tick' 2, ' Pig' 2, ' deer' 1, ' Horse' 1, ' Lion' 1, ' bird' 1, ' Rabbit' 1.

Read wrong by gold class: amphibian 0 / 10; arachnid 15 / 53; bird 2 / 112; insect 2 / 87; mammal 12 / 120.

## 5 random (Q-after, word) failures (seed 0, of 237)

### P2-L0-0222 (org): asked pick ant, gold insect (read tokens [' insect', ' In'])

Prompt tail:

```
 is 6. Clara picked the lion. The locker of the ant is 5.
What class of animal is Noah's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

(Q-after) greedy ' ant\n', first token ' ant', kind: the asked pick itself (the animal). Same scene (Q-before): greedy ' Insect\n', read right True.

### P2-L0-0240 (org): asked pick cat, gold mammal (read tokens [' mamm', ' M'])

Prompt tail:

```
 picked the cat. Hugo picked the goose. The locker of the cat is 5.
What class of animal is Nina's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

(Q-after) greedy ' cat\n', first token ' cat', kind: the asked pick itself (the animal). Same scene (Q-before): greedy ' Mammal\n', read right True.

### P2-L0-0504 (alt): asked pick tick, gold arachnid (read tokens [' ar', ' Ar'])

Prompt tail:

```
 is 9. Peter picked the crow. The locker of the crow is 5.
What class of animal is Finn's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

(Q-after) greedy ' tick\n', first token ' tick', kind: the asked pick itself (the animal). Same scene (Q-before): greedy ' Insect\n', read right False.

### P2-L0-0549 (alt): asked pick bee, gold insect (read tokens [' insect', ' In'])

Prompt tail:

```
 locker of the sheep is 9. Victor picked the sheep. Henry picked the camel.
What class of animal is Noah's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

(Q-after) greedy ' Bee\n', first token ' Bee', kind: the asked pick itself (the animal). Same scene (Q-before): greedy ' Bee\n', read right False.

### P2-L0-0576 (org): asked pick lion, gold mammal (read tokens [' mamm', ' M'])

Prompt tail:

```
 is 3. Victor picked the beetle. The locker of the lion is 7.
What class of animal is Carl's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

(Q-after) greedy ' lion\n', first token ' lion', kind: the asked pick itself (the animal). Same scene (Q-before): greedy ' Mammal\n', read right True.

