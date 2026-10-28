# 51.2 plan, muse-glimmer-30b: 5 random items (seed 0) of 300

The lookup's O prompt exactly as the model reads it (x49_attn.marked: ⟦bridge:…⟧ the swap position, ⟦slotS (j|k):…⟧ the locker sentences, ⟦read:…⟧ the last token). Ablation positions per reader: last = the read token; question = the question text's tokens. UNVERIFIED.

## C2-0039 (fit half): bridge dog, j = 1, k in [0, 2]; lockers [['bee', 9], ['dog', 7], ['cow', 8]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (k):The locker of the bee is 9.⟧⟦slot1 (j): The locker of the dog is 7.⟧⟦slot2 (k): The locker of the cow is 8.⟧ Rose picked the bee. Mark picked the⟦bridge: dog⟧. Oscar picked the cow.
Which locker belongs to Mark's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

- PP: question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Mark's pick?"); last [109] (' ')
- PM: question tokens [84, 85, 86, 87, 88, 89, 90, 91, 92] ("How many legs does Mark's pick have?"); last [110] (' ')

## C2-0278 (fit half): bridge owl, j = 2, k in [0, 1]; lockers [['cow', 1], ['camel', 6], ['owl', 8]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (k):The locker of the cow is 1.⟧⟦slot1 (k): The locker of the camel is 6.⟧⟦slot2 (j): The locker of the owl is 8.⟧ Peter picked the camel. Ella picked the⟦bridge: owl⟧. Tara picked the cow.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

- PP: question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Ella's pick?"); last [109] (' ')
- PM: question tokens [84, 85, 86, 87, 88, 89, 90, 91, 92] ("How many legs does Ella's pick have?"); last [110] (' ')

## C2-0414 (read half): bridge tiger, j = 0, k in [1, 2]; lockers [['tiger', 5], ['fox', 2], ['duck', 8]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (j):The locker of the tiger is 5.⟧⟦slot1 (k): The locker of the fox is 2.⟧⟦slot2 (k): The locker of the duck is 8.⟧ Rose picked the⟦bridge: tiger⟧. Kate picked the duck. Owen picked the fox.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

- PP: question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Rose's pick?"); last [109] (' ')
- PM: question tokens [84, 85, 86, 87, 88, 89, 90, 91, 92] ("How many legs does Rose's pick have?"); last [110] (' ')

## C2-0459 (fit half): bridge pig, j = 1, k in [0, 2]; lockers [['eagle', 9], ['pig', 5], ['fox', 7]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (k):The locker of the eagle is 9.⟧⟦slot1 (j): The locker of the pig is 5.⟧⟦slot2 (k): The locker of the fox is 7.⟧ Maria picked the fox. Emma picked the⟦bridge: pig⟧. Tom picked the eagle.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

- PP: question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Emma's pick?"); last [109] (' ')
- PM: question tokens [84, 85, 86, 87, 88, 89, 90, 91, 92] ("How many legs does Emma's pick have?"); last [110] (' ')

## C2-0560 (fit half): bridge owl, j = 1, k in [0, 2]; lockers [['bear', 2], ['owl', 6], ['mouse', 8]]

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦slot0 (k):The locker of the bear is 2.⟧⟦slot1 (j): The locker of the owl is 6.⟧⟦slot2 (k): The locker of the mouse is 8.⟧ Iris picked the bear. Beth picked the mouse. Vera picked the⟦bridge: owl⟧.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

- PP: question tokens [84, 85, 86, 87, 88, 89, 90, 91] ("Which locker belongs to Vera's pick?"); last [109] (' ')
- PM: question tokens [84, 85, 86, 87, 88, 89, 90, 91, 92] ("How many legs does Vera's pick have?"); last [110] (' ')

