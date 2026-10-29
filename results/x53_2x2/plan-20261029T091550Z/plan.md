# x53_2x2 plan on nemotron-3.5-lightning (tokenizer only; UNVERIFIED)

Relation: number word (rule in the module docstring). Coverage per candidate (scenes of 600; admissible needs >= 150):

- animals/class: 33 scenes, admissible False; dropped items {'frog': {'word': 'amphibian', 'why': ['not one token']}, 'tick': {'word': 'arachnid', 'why': ['not one token']}, 'dog': {'word': 'mammal', 'why': ['not one token']}, 'mouse': {'word': 'mammal', 'why': ['not one token', "'m' initial", "'M' initial"]}, 'lion': {'word': 'mammal', 'why': ['not one token']}, 'sheep': {'word': 'mammal', 'why': ['not one token']}, 'fox': {'word': 'mammal', 'why': ['not one token']}, 'cat': {'word': 'mammal', 'why': ['not one token']}, 'deer': {'word': 'mammal', 'why': ['not one token']}, 'spider': {'word': 'arachnid', 'why': ['not one token']}, 'elephant': {'word': 'mammal', 'why': ['not one token']}, 'bear': {'word': 'mammal', 'why': ['not one token']}, 'horse': {'word': 'mammal', 'why': ['not one token']}, 'wolf': {'word': 'mammal', 'why': ['not one token']}, 'goat': {'word': 'mammal', 'why': ['not one token']}, 'camel': {'word': 'mammal', 'why': ['not one token']}, 'rabbit': {'word': 'mammal', 'why': ['not one token']}, 'cow': {'word': 'mammal', 'why': ['not one token']}, 'pig': {'word': 'mammal', 'why': ['not one token']}, 'tiger': {'word': 'mammal', 'why': ['not one token']}}
- animals/young: 0 scenes, admissible False; dropped items {'frog': {'word': 'tadpole', 'why': ['not one token']}, 'butterfly': {'word': 'caterpillar', 'why': ['not one token']}, 'eagle': {'word': 'eaglet', 'why': ['not one token', "'e' initial", "' e' initial", "'E' initial", "' Eag' prefix"]}, 'goose': {'word': 'gosling', 'why': ['not one token', "' g' initial", "'G' initial"]}, 'fly': {'word': 'maggot', 'why': ['not one token']}, 'duck': {'word': 'duckling', 'why': ['not one token', "'du' prefix", "' duck' key", "'D' initial", "'uck' part", "' Duck' key"]}, 'horse': {'word': 'foal', 'why': ['not one token']}, 'chicken': {'word': 'chick', 'why': ["'ch' prefix", "'ick' part", "' chick' prefix", "'Ch' prefix", "'ick' part", "' Chick' prefix"]}, 'cat': {'word': 'kitten', 'why': ['not one token']}, 'owl': {'word': 'owlet', 'why': ['not one token', "'ow' prefix", "' ow' prefix", "'O' initial", "' Ow' prefix"]}, 'deer': {'word': 'fawn', 'why': ['not one token']}, 'pig': {'word': 'piglet', 'why': ['not one token', "'p' initial", "' pig' key", "'P' initial", "' Pig' key"]}}
- elements/state: 107 scenes, admissible False
- greek/vowel: 121 scenes, admissible False
- number word: 600 scenes, admissible True
- all lexical pooled: 261 scenes, admissible True

## qa_num (Q-after, number): {'scenes': 600, 'cases': 516, 'dropped': {'the bridge is not one token at one position in O and S': 84}, 'domains': {'animals': 162, 'elements': 200, 'greek': 154}}

PP (scene P2-L0-0000, read tokens O [1053] S [1050], src PP):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

PM (scene P2-L0-0000, read tokens O [1052] S [1056], src PP):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
How many legs does Iris's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```


## qb_num (Q-before, number): {'scenes': 600, 'cases': 516, 'dropped': {'the bridge is not one token at one position in O and S': 84}, 'domains': {'animals': 162, 'elements': 200, 'greek': 154}}

PP (scene P2-L0-0000, read tokens O [1053] S [1050], src PP):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Question: Which locker belongs to Iris's pick? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

PM (scene P2-L0-0000, read tokens O [1052] S [1056], src PM):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Question: How many legs does Iris's pick have? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```


## qa_word (Q-after, word): {'scenes': 600, 'cases': 516, 'dropped': {'the bridge is not one token at one position in O and S': 84}, 'domains': {'animals': 162, 'elements': 200, 'greek': 154}}

PP (scene P2-L0-0000, read tokens O [1053] S [1050], src PP):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

PM (scene P2-L0-0000, read tokens O [3946, 15802] S [11263, 47965], src PP):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
How many legs does Iris's pick have? Answer with the number written as a word and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```


## qb_word (Q-before, word): {'scenes': 600, 'cases': 516, 'dropped': {'the bridge is not one token at one position in O and S': 84}, 'domains': {'animals': 162, 'elements': 200, 'greek': 154}}

PP (scene P2-L0-0000, read tokens O [1053] S [1050], src PP):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Question: Which locker belongs to Iris's pick? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

PM (scene P2-L0-0000, read tokens O [3946, 15802] S [11263, 47965], src PM):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Question: How many legs does Iris's pick have? Answer with the number written as a word and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

