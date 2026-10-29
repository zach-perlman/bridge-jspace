# x53_2x2 plan on qwen3.5-122b-a10b (tokenizer only; UNVERIFIED)

Relation: animals/class (rule in the module docstring). Coverage per candidate (scenes of 600; admissible needs >= 150):

- animals/class: 191 scenes, admissible True; read tokens {'amphibian': [' amphib', ' Amph'], 'arachnid': [' ar', ' Ar'], 'bird': [' bird', ' Bird'], 'insect': [' insect', ' In'], 'mammal': [' mamm', ' M']}; answers sharing a read token []; dropped items {'mouse': {'word': 'mammal', 'why': ["'m' initial", "'M' initial", "' M' initial"]}}
- animals/young: 17 scenes, admissible False; read tokens {'calf': [' calf', ' C'], 'caterpillar': [' cater', ' Cater'], 'chick': [' chick', ' Chick'], 'cub': [' cub', ' Cub'], 'cygnet': [' cy', ' Cy'], 'duckling': [' duck', ' Duck'], 'eaglet': [' eag', ' Eag'], 'fawn': [' f', ' F'], 'foal': [' fo', ' Fo'], 'gosling': [' gos', ' Gos'], 'kid': [' kid', ' Kid'], 'kit': [' kit', ' Kit'], 'kitten': [' kitten', ' K'], 'lamb': [' lamb', ' Lamb'], 'maggot': [' mag', ' Mag'], 'owlet': [' ow', ' Ow'], 'piglet': [' pig', ' Pig'], 'pup': [' pup', ' Pup'], 'puppy': [' puppy', ' Puppy'], 'tadpole': [' tad', ' Tad']}; answers sharing a read token []; dropped items {'cow': {'word': 'calf', 'why': ["'c' initial", "'C' initial", "' C' initial"]}, 'camel': {'word': 'calf', 'why': ["'c' initial", "'C' initial", "' C' initial"]}, 'goose': {'word': 'gosling', 'why': ["'G' initial"]}, 'chicken': {'word': 'chick', 'why': ["'ch' prefix", "'ick' part", "' chick' prefix", "'Ch' prefix", "'ick' part", "' Chick' prefix"]}, 'duck': {'word': 'duckling', 'why': ["'duck' key", "' duck' key", "'D' initial", "'uck' part", "' Duck' key"]}, 'pig': {'word': 'piglet', 'why': ["'pig' key", "' pig' key", "'P' initial", "' Pig' key"]}, 'owl': {'word': 'owlet', 'why': ["'ow' prefix", "' ow' prefix", "'O' initial", "' Ow' prefix"]}, 'eagle': {'word': 'eaglet', 'why': ["'e' initial", "' eag' prefix", "'E' initial", "' Eag' prefix"]}}
- elements/state: 107 scenes, admissible False; read tokens {'gas': [' gas', ' Gas'], 'solid': [' solid', ' Solid']}; answers sharing a read token []
- greek/vowel: 121 scenes, admissible False; read tokens {'consonant': [' conson', ' Con'], 'vowel': [' vowel', ' V']}; answers sharing a read token []

## qa_num (Q-after, number): {'scenes': 600, 'cases': 600, 'dropped': {}, 'domains': {'animals': 200, 'elements': 200, 'greek': 200}}

PP (scene P2-L0-0000, read tokens O [20] S [17], src PP):

```
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

PM (scene P2-L0-0000, read tokens O [19] S [23], src PP):

```
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
How many legs does Iris's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```


## qb_num (Q-before, number): {'scenes': 600, 'cases': 600, 'dropped': {}, 'domains': {'animals': 200, 'elements': 200, 'greek': 200}}

PP (scene P2-L0-0000, read tokens O [20] S [17], src PP):

```
<|im_start|>user
Question: Which locker belongs to Iris's pick? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

PM (scene P2-L0-0000, read tokens O [19] S [23], src PM):

```
<|im_start|>user
Question: How many legs does Iris's pick have? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```


## qa_word (Q-after, word): {'scenes': 600, 'cases': 191, 'dropped': {"the relation's domain is another": 400, 'a bridge without an admissible answer under the relation': 9}, 'domains': {'animals': 191}}

PP (scene P2-L0-0000, read tokens O [20] S [17], src PP):

```
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

PM (scene P2-L0-0000, read tokens O [84893, 88983] S [771, 1587], src PP):

```
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
What class of animal is Iris's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```


## qb_word (Q-before, word): {'scenes': 600, 'cases': 191, 'dropped': {"the relation's domain is another": 400, 'a bridge without an admissible answer under the relation': 9}, 'domains': {'animals': 191}}

PP (scene P2-L0-0000, read tokens O [20] S [17], src PP):

```
<|im_start|>user
Question: Which locker belongs to Iris's pick? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

PM (scene P2-L0-0000, read tokens O [84893, 88983] S [771, 1587], src PM):

```
<|im_start|>user
Question: What class of animal is Iris's pick? Answer with a single word and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

