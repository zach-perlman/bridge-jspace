# 49.7 plan, qwen3.6-27b: 5 random items (seed 0) of 300

The lookup's O prompt exactly as the model reads it (chat template, X0's read suffix appended); ⟦bridge:…⟧ the write position (L = 32), ⟦slotS (j|k):…⟧ each locker sentence's tokens (j = the bridge item's slot, k = a written slot), ⟦read:…⟧ the last token (a query site). Question tokens = the question text's tokens. UNVERIFIED.

## C2-0028 (read half): bridge fly, j = 0, k in [1, 2]; lockers [['fly', 3], ['duck', 6], ['bee', 4]]

```
<|im_start|>user
⟦slot0 (j):The locker of the fly is 3.⟧⟦slot1 (k): The locker of the duck is 6.⟧⟦slot2 (k): The locker of the bee is 4.⟧ Lucy picked the duck. Sam picked the⟦bridge: fly⟧. Liam picked the bee.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Sam's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

## C2-0199 (read half): bridge tick, j = 0, k in [1, 2]; lockers [['tick', 7], ['fly', 9], ['bee', 6]]

```
<|im_start|>user
⟦slot0 (j):The locker of the tick is 7.⟧⟦slot1 (k): The locker of the fly is 9.⟧⟦slot2 (k): The locker of the bee is 6.⟧ Vera picked the bee. James picked the fly. Owen picked the⟦bridge: tick⟧.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Owen's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

## C2-0293 (fit half): bridge mouse, j = 2, k in [0, 1]; lockers [['butterfly', 4], ['fly', 1], ['mouse', 6]]

```
<|im_start|>user
⟦slot0 (k):The locker of the butterfly is 4.⟧⟦slot1 (k): The locker of the fly is 1.⟧⟦slot2 (j): The locker of the mouse is 6.⟧ Mark picked the butterfly. Anna picked the fly. Noah picked the⟦bridge: mouse⟧.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Noah's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

## C2-0324 (read half): bridge crow, j = 0, k in [1, 2]; lockers [['crow', 8], ['camel', 1], ['wolf', 2]]

```
<|im_start|>user
⟦slot0 (j):The locker of the crow is 8.⟧⟦slot1 (k): The locker of the camel is 1.⟧⟦slot2 (k): The locker of the wolf is 2.⟧ Laura picked the camel. Vera picked the⟦bridge: crow⟧. Eve picked the wolf.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

Question tokens [46, 47, 48, 49, 50, 51, 52, 53] ("Which locker belongs to Vera's pick?"); slot groups (item / number / rest): slot0 [7] / [10] / [3, 4, 5, 6, 8, 9, 11]; slot1 [16] / [19] / [12, 13, 14, 15, 17, 18, 20]; slot2 [25] / [28] / [21, 22, 23, 24, 26, 27, 29]

## C2-0390 (fit half): bridge owl, j = 1, k in [0, 2]; lockers [['bee', 9], ['owl', 4], ['mouse', 8]]

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

