# 49.7 plan, muse-glimmer-30b: 5 random items (seed 0) of 300

The lookup's O prompt exactly as the model reads it (chat template, X0's read suffix appended); ⟦bridge:…⟧ the write position (L = 26), ⟦slotS (j|k):…⟧ each locker sentence's tokens (j = the bridge item's slot, k = a written slot), ⟦read:…⟧ the last token (a query site). Question tokens = the question text's tokens. UNVERIFIED.

## C2-0039 (fit half): bridge dog, j = 1, k in [0, 2]; lockers [['bee', 9], ['dog', 7], ['cow', 8]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (k):The locker of the bee is 9.⟧⟦slot1 (j): The locker of the dog is 7.⟧⟦slot2 (k): The locker of the cow is 8.⟧ Rose picked the bee. Mark picked the⟦bridge: dog⟧. Oscar picked the cow.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

Question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Mark's pick?"); slot groups (item / number / rest): slot0 [46] / [49] / [42, 43, 44, 45, 47, 48, 50]; slot1 [55] / [58] / [51, 52, 53, 54, 56, 57, 59]; slot2 [64] / [67] / [60, 61, 62, 63, 65, 66, 68]

## C2-0278 (fit half): bridge owl, j = 2, k in [0, 1]; lockers [['cow', 1], ['camel', 6], ['owl', 8]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (k):The locker of the cow is 1.⟧⟦slot1 (k): The locker of the camel is 6.⟧⟦slot2 (j): The locker of the owl is 8.⟧ Peter picked the camel. Ella picked the⟦bridge: owl⟧. Tara picked the cow.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

Question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Ella's pick?"); slot groups (item / number / rest): slot0 [46] / [49] / [42, 43, 44, 45, 47, 48, 50]; slot1 [55] / [58] / [51, 52, 53, 54, 56, 57, 59]; slot2 [64] / [67] / [60, 61, 62, 63, 65, 66, 68]

## C2-0414 (read half): bridge tiger, j = 0, k in [1, 2]; lockers [['tiger', 5], ['fox', 2], ['duck', 8]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (j):The locker of the tiger is 5.⟧⟦slot1 (k): The locker of the fox is 2.⟧⟦slot2 (k): The locker of the duck is 8.⟧ Rose picked the⟦bridge: tiger⟧. Kate picked the duck. Owen picked the fox.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

Question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Rose's pick?"); slot groups (item / number / rest): slot0 [46] / [49] / [42, 43, 44, 45, 47, 48, 50]; slot1 [55] / [58] / [51, 52, 53, 54, 56, 57, 59]; slot2 [64] / [67] / [60, 61, 62, 63, 65, 66, 68]

## C2-0459 (fit half): bridge pig, j = 1, k in [0, 2]; lockers [['eagle', 9], ['pig', 5], ['fox', 7]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (k):The locker of the eagle is 9.⟧⟦slot1 (j): The locker of the pig is 5.⟧⟦slot2 (k): The locker of the fox is 7.⟧ Maria picked the fox. Emma picked the⟦bridge: pig⟧. Tom picked the eagle.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

Question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Emma's pick?"); slot groups (item / number / rest): slot0 [46] / [49] / [42, 43, 44, 45, 47, 48, 50]; slot1 [55] / [58] / [51, 52, 53, 54, 56, 57, 59]; slot2 [64] / [67] / [60, 61, 62, 63, 65, 66, 68]

## C2-0560 (fit half): bridge owl, j = 1, k in [0, 2]; lockers [['bear', 2], ['owl', 6], ['mouse', 8]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (k):The locker of the bear is 2.⟧⟦slot1 (j): The locker of the owl is 6.⟧⟦slot2 (k): The locker of the mouse is 8.⟧ Iris picked the bear. Beth picked the mouse. Vera picked the⟦bridge: owl⟧.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

Question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Vera's pick?"); slot groups (item / number / rest): slot0 [46] / [49] / [42, 43, 44, 45, 47, 48, 50]; slot1 [55] / [58] / [51, 52, 53, 54, 56, 57, 59]; slot2 [64] / [67] / [60, 61, 62, 63, 65, 66, 68]

