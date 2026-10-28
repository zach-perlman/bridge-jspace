# 49.8 plan (CPU, the real tokenizer): DAS for the address, the routes position pairs

Written by `scripts/x49_das_pos.py plan` before any run. Target qwen3.5-9b at L12; pairs from qwen35_9b_x6_routes (C1: the bridge's locker sentence moved to another slot, a new number in S). UNVERIFIED.

- C1 scenes read under the whole change (eligible): 300; the lookup's stored whole-change routes: {'position': 187, 'identity': 109, 'other': 4}
- kept (the lookup's stored whole-change route is position): 187 pairs, 31 bridge entities; entities per split {'train': 19, 'select': 6, 'test': 6}; pairs per split {'train': 112, 'test': 34, 'select': 41}
- moves (O slot -> S slot): {'1->2': 43, '1->3': 31, '2->1': 57, '2->3': 7, '3->1': 32, '3->2': 17}; the bridge's O slot in train (U_fit's classes): {1: 43, 2: 38, 3: 31}
- the recall kept O's answer under the stored whole change: 0.7326
- prompt tokens [74, 74]; bridge token index [33, 38, 43]
- U: {'states_run': 'qwen35_9b_x0_probe_v4', 'rank': 4}
- W: {'run': 'qwen35_9b_x47_2', 'slots': 6, 'rank': 5, 'file': 'results/x47_six/qwen35_9b_x47_2/fit.npz', 'sha256': '74687ee895327b94a42a6869b8dcaf2a8a2ac2c2738abf00e37b724db0a50b74'}

## 5 random pairs (seed 0): O and S as the model reads them

⟦bridge:…⟧ the bridge token where R R^T Delta is added; in O ⟦own:…⟧ the bridge's locker sentence and ⟦target:…⟧ the sentence at the slot it moves to in S (its digit is the counterfactual answer); in S ⟦moved:…⟧ the bridge's sentence at its new slot.

### C1-0018 (train): the chicken's locker sentence moves from slot 2 to slot 1

Lookup (Which locker belongs to Alice's pick?): O answers 1, S answers 5 (the new digit), the counterfactual (position) answer 6. Recall (How many legs does Alice's pick have?): 2 in both.

O (lookup), as read:

```
<|im_start|>user
⟦target:The locker of the dog is 6.⟧ ⟦own:The locker of the chicken is 1.⟧ The locker of the fox is 2. Anna picked the dog. Leo picked the fox. Alice picked the⟦bridge: chicken⟧.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (lookup, the source):

```
<|im_start|>user
⟦moved:The locker of the chicken is 5.⟧ The locker of the dog is 6. The locker of the fox is 2. Anna picked the dog. Leo picked the fox. Alice picked the⟦bridge: chicken⟧.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

### C1-0174 (select): the owl's locker sentence moves from slot 2 to slot 1

Lookup (Which locker belongs to Kate's pick?): O answers 2, S answers 8 (the new digit), the counterfactual (position) answer 1. Recall (How many legs does Kate's pick have?): 2 in both.

O (lookup), as read:

```
<|im_start|>user
⟦target:The locker of the tiger is 1.⟧ ⟦own:The locker of the owl is 2.⟧ The locker of the bear is 4. Kate picked the⟦bridge: owl⟧. Frank picked the tiger. Maria picked the bear.
Which locker belongs to Kate's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (lookup, the source):

```
<|im_start|>user
⟦moved:The locker of the owl is 8.⟧ The locker of the tiger is 1. The locker of the bear is 4. Kate picked the⟦bridge: owl⟧. Frank picked the tiger. Maria picked the bear.
Which locker belongs to Kate's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

### C1-0265 (train): the mouse's locker sentence moves from slot 3 to slot 2

Lookup (Which locker belongs to Kyle's pick?): O answers 8, S answers 5 (the new digit), the counterfactual (position) answer 2. Recall (How many legs does Kyle's pick have?): 4 in both.

O (lookup), as read:

```
<|im_start|>user
The locker of the chicken is 3. ⟦target:The locker of the horse is 2.⟧ ⟦own:The locker of the mouse is 8.⟧ Kyle picked the⟦bridge: mouse⟧. Carl picked the horse. Lily picked the chicken.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (lookup, the source):

```
<|im_start|>user
The locker of the chicken is 3. ⟦moved:The locker of the mouse is 5.⟧ The locker of the horse is 2. Kyle picked the⟦bridge: mouse⟧. Carl picked the horse. Lily picked the chicken.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

### C1-0281 (test): the pig's locker sentence moves from slot 2 to slot 1

Lookup (Which locker belongs to Leo's pick?): O answers 9, S answers 4 (the new digit), the counterfactual (position) answer 7. Recall (How many legs does Leo's pick have?): 4 in both.

O (lookup), as read:

```
<|im_start|>user
⟦target:The locker of the owl is 7.⟧ ⟦own:The locker of the pig is 9.⟧ The locker of the tick is 1. Leo picked the⟦bridge: pig⟧. Frank picked the tick. Noah picked the owl.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (lookup, the source):

```
<|im_start|>user
⟦moved:The locker of the pig is 4.⟧ The locker of the owl is 7. The locker of the tick is 1. Leo picked the⟦bridge: pig⟧. Frank picked the tick. Noah picked the owl.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

### C1-0349 (train): the elephant's locker sentence moves from slot 3 to slot 2

Lookup (Which locker belongs to Mia's pick?): O answers 8, S answers 4 (the new digit), the counterfactual (position) answer 1. Recall (How many legs does Mia's pick have?): 4 in both.

O (lookup), as read:

```
<|im_start|>user
The locker of the turkey is 7. ⟦target:The locker of the duck is 1.⟧ ⟦own:The locker of the elephant is 8.⟧ Ella picked the turkey. Mia picked the⟦bridge: elephant⟧. Beth picked the duck.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S (lookup, the source):

```
<|im_start|>user
The locker of the turkey is 7. ⟦moved:The locker of the elephant is 4.⟧ The locker of the duck is 1. Ella picked the turkey. Mia picked the⟦bridge: elephant⟧. Beth picked the duck.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

