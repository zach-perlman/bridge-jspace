# 51.11 plan (CPU, each target's tokenizer): position counterfactual scenes at S = 3, 4, 6, 8

Written by `scripts/x51_addr.py plan` before any run. A pair: the bridge's locker sentence and the sentence at slot j trade places, digits kept (the lookup's answer unchanged; the target is O's digit at slot j). Candidates are generated per ordered slot pair; the GPU reads them in order (competence, then the whole change) until each ordered pair has its quota of pairs whose whole change sends the lookup to the position answer. Pair counts are known only after the read. UNVERIFIED.

| model | L | S | ordered pairs | candidates (per pair) | dropped | locker sentence tokens | slot starts | prompt tokens | bridge index | quota / target | candidates per split | est. reads (47.2 rates) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| muse-glimmer-30b | 26 | 3 | 6 | 1800 ([300]) | none | 9 | [42, 51, 60] | [109, 109] | [72, 77, 82] | 60 / 360 | {'train': 1056, 'select': 347, 'test': 397} | - |
| muse-glimmer-30b | 26 | 4 | 12 | 2400 ([200]) | none | 9 | [42, 51, 60, 69] | [118, 118] | [81, 86, 91] | 30 / 360 | {'select': 463, 'train': 1384, 'test': 553} | - |
| muse-glimmer-30b | 26 | 6 | 30 | 3600 ([120]) | none | 9 | [42, 51, 60, 69, 78, 87] | [136, 136] | [99, 104, 109] | 12 / 360 | {'select': 684, 'train': 2113, 'test': 803} | 1254 |
| muse-glimmer-30b | 26 | 8 | 56 | 4480 ([80]) | none | 9 | [42, 51, 60, 69, 78, 87, 96, 105] | [154, 154] | [117, 122, 127] | 7 / 392 | {'test': 934, 'train': 2707, 'select': 839} | - |
| qwen3.5-9b | 12 | 3 | 6 | 1800 ([300]) | none | 9 | [3, 12, 21] | [74, 74] | [33, 38, 43] | 60 / 360 | {'train': 1056, 'select': 347, 'test': 397} | - |
| qwen3.5-9b | 12 | 4 | 12 | 2400 ([200]) | none | 9 | [3, 12, 21, 30] | [83, 83] | [42, 47, 52] | 30 / 360 | {'select': 463, 'train': 1384, 'test': 553} | - |
| qwen3.5-9b | 12 | 6 | 30 | 3600 ([120]) | none | 9 | [3, 12, 21, 30, 39, 48] | [101, 101] | [60, 65, 70] | 12 / 360 | {'select': 684, 'train': 2113, 'test': 803} | 1267 |
| qwen3.5-9b | 12 | 8 | 56 | 4480 ([80]) | none | 9 | [3, 12, 21, 30, 39, 48, 57, 66] | [119, 119] | [78, 83, 88] | 7 / 392 | {'test': 934, 'train': 2707, 'select': 839} | - |
| qwen3.6-27b | 32 | 3 | 6 | 1800 ([300]) | none | 9 | [3, 12, 21] | [74, 74] | [33, 38, 43] | 60 / 360 | {'train': 1056, 'select': 347, 'test': 397} | - |
| qwen3.6-27b | 32 | 4 | 12 | 2400 ([200]) | none | 9 | [3, 12, 21, 30] | [83, 83] | [42, 47, 52] | 30 / 360 | {'select': 463, 'train': 1384, 'test': 553} | - |
| qwen3.6-27b | 32 | 6 | 30 | 3600 ([120]) | none | 9 | [3, 12, 21, 30, 39, 48] | [101, 101] | [60, 65, 70] | 12 / 360 | {'select': 684, 'train': 2113, 'test': 803} | - |
| qwen3.6-27b | 32 | 8 | 56 | 4480 ([80]) | none | 9 | [3, 12, 21, 30, 39, 48, 57, 66] | [119, 119] | [78, 83, 88] | 7 / 392 | {'test': 934, 'train': 2707, 'select': 839} | - |

## muse-glimmer-30b (runs {'1': 'muse30_x51_11_p1', '2': 'muse30_x51_11_p2', '3': 'muse30_x51_11_p3'})

- entities 32, split {'train': 19, 'select': 6, 'test': 7} (seed 0, the generator's animal pool); k [1, 2, 3, 4, 5, 7]
- part 2 items: test-entity candidates per start slot, S = 6 {'1': 142, '2': 128, '3': 112, '4': 129, '5': 141, '6': 151}, S = 3 {'1': 130, '2': 133, '3': 134} (the run keeps the first 20 / 40 eligible)
- part 3 items: held-out candidates with the bridge at slot 1 / 6 (S = 6): {'1': 238, '6': 269} (the run keeps the first 100 eligible per end)

- 47.2's stored whole-change position share per ordered pair (new-digit moves, muse30_x47_2): {'1-2': 0.7, '1-3': 0.6, '1-4': 0.1, '1-5': 0.4, '1-6': 0.5, '2-1': 0.9, '2-3': 0.2, '2-4': 0.5, '2-5': 0.3, '2-6': 0.2, '3-1': 0.9, '3-2': 0.5, '3-4': 0.0, '3-5': 0.0, '3-6': 0.0, '4-1': 0.9, '4-2': 0.8, '4-3': 0.2, '4-5': 0.0, '4-6': 0.0, '5-1': 0.9, '5-2': 0.6, '5-3': 0.4, '5-4': 0.0, '5-6': 0.1, '6-1': 0.6, '6-2': 0.5, '6-3': 0.3, '6-4': 0.0, '6-5': 0.0}; eligible 0.892

### Rendered pairs (seed 0): the lookup's O and S as the model reads them

⟦bridge:…⟧ the bridge token (every edit at L); in O ⟦own:…⟧ the bridge's locker sentence and ⟦target:…⟧ the sentence at slot j (its digit = the counterfactual target); in S ⟦moved:…⟧ the bridge's sentence at slot j, its digit kept.

#### P6-64-0099 (S = 6, 6->4, test): O answers 2, S answers 2, the position answer 6

O:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 5. The locker of the butterfly is 1. The locker of the turkey is 8. ⟦target:The locker of the owl is 6.⟧ The locker of the duck is 4. ⟦own:The locker of the bear is 2.⟧ Leo picked the owl. Vera picked the bee. Ella picked the⟦bridge: bear⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 5. The locker of the butterfly is 1. The locker of the turkey is 8. ⟦moved:The locker of the bear is 2.⟧ The locker of the duck is 4. The locker of the owl is 6. Leo picked the owl. Vera picked the bee. Ella picked the⟦bridge: bear⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

#### P6-35-0018 (S = 6, 3->5, test): O answers 6, S answers 6, the position answer 5

O:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the fox is 9. The locker of the cow is 3. ⟦own:The locker of the elephant is 6.⟧ The locker of the zebra is 2. ⟦target:The locker of the dog is 5.⟧ The locker of the sheep is 1. Ivy picked the⟦bridge: elephant⟧. Carl picked the sheep. Fiona picked the fox.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the fox is 9. The locker of the cow is 3. The locker of the dog is 5. The locker of the zebra is 2. ⟦moved:The locker of the elephant is 6.⟧ The locker of the sheep is 1. Ivy picked the⟦bridge: elephant⟧. Carl picked the sheep. Fiona picked the fox.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

#### P6-61-0105 (S = 6, 6->1, train): O answers 2, S answers 2, the position answer 4

O:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦target:The locker of the elephant is 4.⟧ The locker of the bear is 1. The locker of the turkey is 3. The locker of the rabbit is 9. The locker of the lion is 7. ⟦own:The locker of the spider is 2.⟧ Ivan picked the rabbit. Noah picked the⟦bridge: spider⟧. Ben picked the bear.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦moved:The locker of the spider is 2.⟧ The locker of the bear is 1. The locker of the turkey is 3. The locker of the rabbit is 9. The locker of the lion is 7. The locker of the elephant is 4. Ivan picked the rabbit. Noah picked the⟦bridge: spider⟧. Ben picked the bear.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

#### P6-36-0043 (S = 6, 3->6, test): O answers 5, S answers 5, the position answer 3

O:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 4. The locker of the camel is 9. ⟦own:The locker of the bear is 5.⟧ The locker of the crow is 6. The locker of the tick is 8. ⟦target:The locker of the fly is 3.⟧ Iris picked the camel. Nina picked the spider. Sam picked the⟦bridge: bear⟧.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 4. The locker of the camel is 9. The locker of the fly is 3. The locker of the crow is 6. The locker of the tick is 8. ⟦moved:The locker of the bear is 5.⟧ Iris picked the camel. Nina picked the spider. Sam picked the⟦bridge: bear⟧.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

#### P6-13-0046 (S = 6, 1->3, train): O answers 2, S answers 2, the position answer 1

O:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦own:The locker of the chicken is 2.⟧ The locker of the rabbit is 6. ⟦target:The locker of the spider is 1.⟧ The locker of the bear is 7. The locker of the cow is 5. The locker of the lion is 4. Max picked the bear. James picked the⟦bridge: chicken⟧. Leo picked the spider.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is 1. The locker of the rabbit is 6. ⟦moved:The locker of the chicken is 2.⟧ The locker of the bear is 7. The locker of the cow is 5. The locker of the lion is 4. Max picked the bear. James picked the⟦bridge: chicken⟧. Leo picked the spider.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

#### P3-13-0231 (S = 3, 1->3, train): O answers 7, S answers 7, the position answer 2

O:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦own:The locker of the chicken is 7.⟧ The locker of the elephant is 3. ⟦target:The locker of the goat is 2.⟧ Alice picked the⟦bridge: chicken⟧. Owen picked the goat. Jack picked the elephant.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the goat is 2. The locker of the elephant is 3. ⟦moved:The locker of the chicken is 7.⟧ Alice picked the⟦bridge: chicken⟧. Owen picked the goat. Jack picked the elephant.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

#### P4-42-0095 (S = 4, 4->2, test): O answers 3, S answers 3, the position answer 9

O:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the horse is 5. ⟦target:The locker of the bee is 9.⟧ The locker of the fly is 7. ⟦own:The locker of the bear is 3.⟧ Zoe picked the fly. Clara picked the⟦bridge: bear⟧. Amy picked the horse.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the horse is 5. ⟦moved:The locker of the bear is 3.⟧ The locker of the fly is 7. The locker of the bee is 9. Zoe picked the fly. Clara picked the⟦bridge: bear⟧. Amy picked the horse.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

#### P8-81-0061 (S = 8, 8->1, select): O answers 4, S answers 4, the position answer 7

O:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦target:The locker of the mouse is 7.⟧ The locker of the bee is 6. The locker of the lion is 1. The locker of the turkey is 8. The locker of the fox is 9. The locker of the crow is 5. The locker of the tick is 3. ⟦own:The locker of the wolf is 4.⟧ Clara picked the lion. Laura picked the⟦bridge: wolf⟧. Henry picked the turkey.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

S:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦moved:The locker of the wolf is 4.⟧ The locker of the bee is 6. The locker of the lion is 1. The locker of the turkey is 8. The locker of the fox is 9. The locker of the crow is 5. The locker of the tick is 3. The locker of the mouse is 7. Clara picked the lion. Laura picked the⟦bridge: wolf⟧. Henry picked the turkey.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```


## qwen3.5-9b (runs {'1': 'qwen35_9b_x51_11_p1', '2': 'qwen35_9b_x51_11_p2', '3': 'qwen35_9b_x51_11_p3'})

- entities 32, split {'train': 19, 'select': 6, 'test': 7} (seed 0, the generator's animal pool); k [1, 2, 3, 4, 5, 7]
- part 2 items: test-entity candidates per start slot, S = 6 {'1': 142, '2': 128, '3': 112, '4': 129, '5': 141, '6': 151}, S = 3 {'1': 130, '2': 133, '3': 134} (the run keeps the first 20 / 40 eligible)
- part 3 items: held-out candidates with the bridge at slot 1 / 6 (S = 6): {'1': 238, '6': 269} (the run keeps the first 100 eligible per end)

- 47.2's stored whole-change position share per ordered pair (new-digit moves, qwen35_9b_x47_2): {'1-2': 0.8, '1-3': 0.4, '1-4': 0.2, '1-5': 0.4, '1-6': 0.3, '2-1': 0.9, '2-3': 0.0, '2-4': 0.0, '2-5': 0.0, '2-6': 0.3, '3-1': 0.9, '3-2': 0.5, '3-4': 0.0, '3-5': 0.0, '3-6': 0.0, '4-1': 1.0, '4-2': 0.5, '4-3': 0.0, '4-5': 0.0, '4-6': 0.0, '5-1': 1.0, '5-2': 0.7, '5-3': 0.1, '5-4': 0.0, '5-6': 0.0, '6-1': 1.0, '6-2': 0.6, '6-3': 0.1, '6-4': 0.0, '6-5': 0.0}; eligible 0.9

### Rendered pairs (seed 0): the lookup's O and S as the model reads them

⟦bridge:…⟧ the bridge token (every edit at L); in O ⟦own:…⟧ the bridge's locker sentence and ⟦target:…⟧ the sentence at slot j (its digit = the counterfactual target); in S ⟦moved:…⟧ the bridge's sentence at slot j, its digit kept.

#### P6-64-0099 (S = 6, 6->4, test): O answers 2, S answers 2, the position answer 6

O:

```
<|im_start|>user
The locker of the bee is 5. The locker of the beetle is 1. The locker of the tiger is 8. ⟦target:The locker of the mouse is 6.⟧ The locker of the dog is 4. ⟦own:The locker of the bear is 2.⟧ Leo picked the mouse. Vera picked the bee. Ella picked the⟦bridge: bear⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the bee is 5. The locker of the beetle is 1. The locker of the tiger is 8. ⟦moved:The locker of the bear is 2.⟧ The locker of the dog is 4. The locker of the mouse is 6. Leo picked the mouse. Vera picked the bee. Ella picked the⟦bridge: bear⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P6-35-0018 (S = 6, 3->5, test): O answers 6, S answers 6, the position answer 5

O:

```
<|im_start|>user
The locker of the fly is 9. The locker of the chicken is 3. ⟦own:The locker of the eagle is 6.⟧ The locker of the wolf is 2. ⟦target:The locker of the deer is 5.⟧ The locker of the rabbit is 1. Ivy picked the⟦bridge: eagle⟧. Carl picked the rabbit. Fiona picked the fly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the fly is 9. The locker of the chicken is 3. The locker of the deer is 5. The locker of the wolf is 2. ⟦moved:The locker of the eagle is 6.⟧ The locker of the rabbit is 1. Ivy picked the⟦bridge: eagle⟧. Carl picked the rabbit. Fiona picked the fly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P6-61-0105 (S = 6, 6->1, train): O answers 2, S answers 2, the position answer 4

O:

```
<|im_start|>user
⟦target:The locker of the eagle is 4.⟧ The locker of the bear is 1. The locker of the tiger is 3. The locker of the pig is 9. The locker of the horse is 7. ⟦own:The locker of the sheep is 2.⟧ Ivan picked the pig. Noah picked the⟦bridge: sheep⟧. Ben picked the bear.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
⟦moved:The locker of the sheep is 2.⟧ The locker of the bear is 1. The locker of the tiger is 3. The locker of the pig is 9. The locker of the horse is 7. The locker of the eagle is 4. Ivan picked the pig. Noah picked the⟦bridge: sheep⟧. Ben picked the bear.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P6-36-0043 (S = 6, 3->6, test): O answers 5, S answers 5, the position answer 3

O:

```
<|im_start|>user
The locker of the sheep is 4. The locker of the butterfly is 9. ⟦own:The locker of the bear is 5.⟧ The locker of the cow is 6. The locker of the spider is 8. ⟦target:The locker of the elephant is 3.⟧ Iris picked the butterfly. Nina picked the sheep. Sam picked the⟦bridge: bear⟧.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the sheep is 4. The locker of the butterfly is 9. The locker of the elephant is 3. The locker of the cow is 6. The locker of the spider is 8. ⟦moved:The locker of the bear is 5.⟧ Iris picked the butterfly. Nina picked the sheep. Sam picked the⟦bridge: bear⟧.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P6-13-0046 (S = 6, 1->3, train): O answers 2, S answers 2, the position answer 1

O:

```
<|im_start|>user
⟦own:The locker of the cat is 2.⟧ The locker of the pig is 6. ⟦target:The locker of the sheep is 1.⟧ The locker of the bear is 7. The locker of the chicken is 5. The locker of the horse is 4. Max picked the bear. James picked the⟦bridge: cat⟧. Leo picked the sheep.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the sheep is 1. The locker of the pig is 6. ⟦moved:The locker of the cat is 2.⟧ The locker of the bear is 7. The locker of the chicken is 5. The locker of the horse is 4. Max picked the bear. James picked the⟦bridge: cat⟧. Leo picked the sheep.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P3-13-0231 (S = 3, 1->3, train): O answers 7, S answers 7, the position answer 2

O:

```
<|im_start|>user
⟦own:The locker of the cat is 7.⟧ The locker of the eagle is 3. ⟦target:The locker of the frog is 2.⟧ Alice picked the⟦bridge: cat⟧. Owen picked the frog. Jack picked the eagle.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the frog is 2. The locker of the eagle is 3. ⟦moved:The locker of the cat is 7.⟧ Alice picked the⟦bridge: cat⟧. Owen picked the frog. Jack picked the eagle.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P4-42-0095 (S = 4, 4->2, test): O answers 3, S answers 3, the position answer 9

O:

```
<|im_start|>user
The locker of the goose is 5. ⟦target:The locker of the bee is 9.⟧ The locker of the elephant is 7. ⟦own:The locker of the bear is 3.⟧ Zoe picked the elephant. Clara picked the⟦bridge: bear⟧. Amy picked the goose.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the goose is 5. ⟦moved:The locker of the bear is 3.⟧ The locker of the elephant is 7. The locker of the bee is 9. Zoe picked the elephant. Clara picked the⟦bridge: bear⟧. Amy picked the goose.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P8-81-0061 (S = 8, 8->1, select): O answers 4, S answers 4, the position answer 7

O:

```
<|im_start|>user
⟦target:The locker of the lion is 7.⟧ The locker of the bee is 6. The locker of the horse is 1. The locker of the tiger is 8. The locker of the fly is 9. The locker of the cow is 5. The locker of the spider is 3. ⟦own:The locker of the turkey is 4.⟧ Clara picked the horse. Laura picked the⟦bridge: turkey⟧. Henry picked the tiger.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
⟦moved:The locker of the turkey is 4.⟧ The locker of the bee is 6. The locker of the horse is 1. The locker of the tiger is 8. The locker of the fly is 9. The locker of the cow is 5. The locker of the spider is 3. The locker of the lion is 7. Clara picked the horse. Laura picked the⟦bridge: turkey⟧. Henry picked the tiger.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```


## qwen3.6-27b (runs {'2': 'x51_11_p2_27b'})

- entities 32, split {'train': 19, 'select': 6, 'test': 7} (seed 0, the generator's animal pool); k [1, 2, 3, 4, 5, 7]
- part 2 items: test-entity candidates per start slot, S = 6 {'1': 142, '2': 128, '3': 112, '4': 129, '5': 141, '6': 151}, S = 3 {'1': 130, '2': 133, '3': 134} (the run keeps the first 20 / 40 eligible)
- part 3 items: held-out candidates with the bridge at slot 1 / 6 (S = 6): {'1': 238, '6': 269} (the run keeps the first 100 eligible per end)

### Rendered pairs (seed 0): the lookup's O and S as the model reads them

⟦bridge:…⟧ the bridge token (every edit at L); in O ⟦own:…⟧ the bridge's locker sentence and ⟦target:…⟧ the sentence at slot j (its digit = the counterfactual target); in S ⟦moved:…⟧ the bridge's sentence at slot j, its digit kept.

#### P6-64-0099 (S = 6, 6->4, test): O answers 2, S answers 2, the position answer 6

O:

```
<|im_start|>user
The locker of the bee is 5. The locker of the beetle is 1. The locker of the tiger is 8. ⟦target:The locker of the mouse is 6.⟧ The locker of the dog is 4. ⟦own:The locker of the bear is 2.⟧ Leo picked the mouse. Vera picked the bee. Ella picked the⟦bridge: bear⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the bee is 5. The locker of the beetle is 1. The locker of the tiger is 8. ⟦moved:The locker of the bear is 2.⟧ The locker of the dog is 4. The locker of the mouse is 6. Leo picked the mouse. Vera picked the bee. Ella picked the⟦bridge: bear⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P6-35-0018 (S = 6, 3->5, test): O answers 6, S answers 6, the position answer 5

O:

```
<|im_start|>user
The locker of the fly is 9. The locker of the chicken is 3. ⟦own:The locker of the eagle is 6.⟧ The locker of the wolf is 2. ⟦target:The locker of the deer is 5.⟧ The locker of the rabbit is 1. Ivy picked the⟦bridge: eagle⟧. Carl picked the rabbit. Fiona picked the fly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the fly is 9. The locker of the chicken is 3. The locker of the deer is 5. The locker of the wolf is 2. ⟦moved:The locker of the eagle is 6.⟧ The locker of the rabbit is 1. Ivy picked the⟦bridge: eagle⟧. Carl picked the rabbit. Fiona picked the fly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P6-61-0105 (S = 6, 6->1, train): O answers 2, S answers 2, the position answer 4

O:

```
<|im_start|>user
⟦target:The locker of the eagle is 4.⟧ The locker of the bear is 1. The locker of the tiger is 3. The locker of the pig is 9. The locker of the horse is 7. ⟦own:The locker of the sheep is 2.⟧ Ivan picked the pig. Noah picked the⟦bridge: sheep⟧. Ben picked the bear.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
⟦moved:The locker of the sheep is 2.⟧ The locker of the bear is 1. The locker of the tiger is 3. The locker of the pig is 9. The locker of the horse is 7. The locker of the eagle is 4. Ivan picked the pig. Noah picked the⟦bridge: sheep⟧. Ben picked the bear.
Which locker belongs to Noah's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P6-36-0043 (S = 6, 3->6, test): O answers 5, S answers 5, the position answer 3

O:

```
<|im_start|>user
The locker of the sheep is 4. The locker of the butterfly is 9. ⟦own:The locker of the bear is 5.⟧ The locker of the cow is 6. The locker of the spider is 8. ⟦target:The locker of the elephant is 3.⟧ Iris picked the butterfly. Nina picked the sheep. Sam picked the⟦bridge: bear⟧.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the sheep is 4. The locker of the butterfly is 9. The locker of the elephant is 3. The locker of the cow is 6. The locker of the spider is 8. ⟦moved:The locker of the bear is 5.⟧ Iris picked the butterfly. Nina picked the sheep. Sam picked the⟦bridge: bear⟧.
Which locker belongs to Sam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P6-13-0046 (S = 6, 1->3, train): O answers 2, S answers 2, the position answer 1

O:

```
<|im_start|>user
⟦own:The locker of the cat is 2.⟧ The locker of the pig is 6. ⟦target:The locker of the sheep is 1.⟧ The locker of the bear is 7. The locker of the chicken is 5. The locker of the horse is 4. Max picked the bear. James picked the⟦bridge: cat⟧. Leo picked the sheep.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the sheep is 1. The locker of the pig is 6. ⟦moved:The locker of the cat is 2.⟧ The locker of the bear is 7. The locker of the chicken is 5. The locker of the horse is 4. Max picked the bear. James picked the⟦bridge: cat⟧. Leo picked the sheep.
Which locker belongs to James's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P3-13-0231 (S = 3, 1->3, train): O answers 7, S answers 7, the position answer 2

O:

```
<|im_start|>user
⟦own:The locker of the cat is 7.⟧ The locker of the eagle is 3. ⟦target:The locker of the frog is 2.⟧ Alice picked the⟦bridge: cat⟧. Owen picked the frog. Jack picked the eagle.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the frog is 2. The locker of the eagle is 3. ⟦moved:The locker of the cat is 7.⟧ Alice picked the⟦bridge: cat⟧. Owen picked the frog. Jack picked the eagle.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P4-42-0095 (S = 4, 4->2, test): O answers 3, S answers 3, the position answer 9

O:

```
<|im_start|>user
The locker of the goose is 5. ⟦target:The locker of the bee is 9.⟧ The locker of the elephant is 7. ⟦own:The locker of the bear is 3.⟧ Zoe picked the elephant. Clara picked the⟦bridge: bear⟧. Amy picked the goose.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
The locker of the goose is 5. ⟦moved:The locker of the bear is 3.⟧ The locker of the elephant is 7. The locker of the bee is 9. Zoe picked the elephant. Clara picked the⟦bridge: bear⟧. Amy picked the goose.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

#### P8-81-0061 (S = 8, 8->1, select): O answers 4, S answers 4, the position answer 7

O:

```
<|im_start|>user
⟦target:The locker of the lion is 7.⟧ The locker of the bee is 6. The locker of the horse is 1. The locker of the tiger is 8. The locker of the fly is 9. The locker of the cow is 5. The locker of the spider is 3. ⟦own:The locker of the turkey is 4.⟧ Clara picked the horse. Laura picked the⟦bridge: turkey⟧. Henry picked the tiger.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

S:

```
<|im_start|>user
⟦moved:The locker of the turkey is 4.⟧ The locker of the bee is 6. The locker of the horse is 1. The locker of the tiger is 8. The locker of the fly is 9. The locker of the cow is 5. The locker of the spider is 3. The locker of the lion is 7. Clara picked the horse. Laura picked the⟦bridge: turkey⟧. Henry picked the tiger.
Which locker belongs to Laura's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

