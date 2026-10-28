# 49.7 plan, qwen3.5-9b: 5 random items (seed 0) of 300

The lookup's O prompt exactly as the model reads it (chat template, X0's read suffix appended); ⟦bridge:…⟧ the write position (L = 12), ⟦slotS (j|k):…⟧ each locker sentence's tokens (j = the bridge item's slot, k = a written slot), ⟦read:…⟧ the last token (a query site). Question tokens = the question text's tokens. UNVERIFIED.

## C2-0035 (read half): bridge goat, j = 2, k in [0, 1]; lockers [['beetle', 2], ['tiger', 4], ['goat', 9]]

```
<|im_start|>user
⟦slot0 (k):The locker of the beetle is 2.⟧⟦slot1 (k): The locker of the tiger is 4.⟧⟦slot2 (j): The locker of the goat is 9.⟧ Leo picked the tiger. Amy picked the beetle. Ivan picked the⟦bridge: goat⟧.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Ivan's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

## C2-0235 (read half): bridge crow, j = 2, k in [0, 1]; lockers [['fox', 5], ['ant', 3], ['crow', 4]]

```
<|im_start|>user
⟦slot0 (k):The locker of the fox is 5.⟧⟦slot1 (k): The locker of the ant is 3.⟧⟦slot2 (j): The locker of the crow is 4.⟧ Henry picked the fox. Lucy picked the⟦bridge: crow⟧. Kyle picked the ant.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Lucy's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

## C2-0367 (read half): bridge pig, j = 2, k in [0, 1]; lockers [['bee', 9], ['butterfly', 8], ['pig', 4]]

```
<|im_start|>user
⟦slot0 (k):The locker of the bee is 9.⟧⟦slot1 (k): The locker of the butterfly is 8.⟧⟦slot2 (j): The locker of the pig is 4.⟧ Sean picked the bee. Mark picked the butterfly. Fiona picked the⟦bridge: pig⟧.
Which locker belongs to Fiona's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Fiona's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

## C2-0390 (read half): bridge owl, j = 1, k in [0, 2]; lockers [['bee', 9], ['owl', 4], ['mouse', 8]]

```
<|im_start|>user
⟦slot0 (k):The locker of the bee is 9.⟧⟦slot1 (j): The locker of the owl is 4.⟧⟦slot2 (k): The locker of the mouse is 8.⟧ Mark picked the bee. Zoe picked the⟦bridge: owl⟧. Peter picked the mouse.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Zoe's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

## C2-0475 (read half): bridge crow, j = 0, k in [1, 2]; lockers [['crow', 1], ['lion', 2], ['fox', 5]]

```
<|im_start|>user
⟦slot0 (j):The locker of the crow is 1.⟧⟦slot1 (k): The locker of the lion is 2.⟧⟦slot2 (k): The locker of the fox is 5.⟧ Will picked the⟦bridge: crow⟧. Laura picked the lion. Nina picked the fox.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Will's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

