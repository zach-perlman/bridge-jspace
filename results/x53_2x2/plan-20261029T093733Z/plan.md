# x53_2x2 plan on nemotron-3.5-lightning (tokenizer only; UNVERIFIED)

Relation: animals/class (rule in the module docstring). Coverage per candidate (scenes of 600; admissible needs >= 150):

- animals/class: 191 scenes, admissible True; read tokens {'amphibian': [' amphib', ' Amph'], 'arachnid': [' ara', ' Ara'], 'bird': [' bird', ' Bird'], 'insect': [' insect', ' In'], 'mammal': [' mamm', ' Mamm']}; answers sharing a read token []; dropped items {'mouse': {'word': 'mammal', 'why': ["'m' initial", "'M' initial"]}}
- animals/young: 19 scenes, admissible False; read tokens {'calf': [' calf', ' Cal'], 'caterpillar': [' cater', ' C'], 'chick': [' chick', ' Chick'], 'cub': [' cub', ' Cub'], 'cygnet': [' cy', ' C'], 'duckling': [' duck', ' Duck'], 'eaglet': [' e', ' Eag'], 'fawn': [' fa', ' Fa'], 'foal': [' fo', ' Fo'], 'gosling': [' g', ' Gos'], 'kid': [' kid', ' Kid'], 'kit': [' kit', ' Kit'], 'kitten': [' kit', ' Kit'], 'lamb': [' lamb', ' Lamb'], 'maggot': [' mag', ' Mag'], 'owlet': [' ow', ' Ow'], 'piglet': [' pig', ' Pig'], 'pup': [' pup', ' P'], 'puppy': [' puppy', ' Pu'], 'tadpole': [' tad', ' Tad']}; answers sharing a read token [('caterpillar', 'cygnet'), ('kit', 'kitten')]; dropped items {'goose': {'word': 'gosling', 'why': ["' g' initial", "'G' initial"]}, 'chicken': {'word': 'chick', 'why': ["'ch' prefix", "'ick' part", "' chick' prefix", "'Ch' prefix", "'ick' part", "' Chick' prefix"]}, 'duck': {'word': 'duckling', 'why': ["'du' prefix", "' duck' key", "'D' initial", "'uck' part", "' Duck' key"]}, 'pig': {'word': 'piglet', 'why': ["'p' initial", "' pig' key", "'P' initial", "' Pig' key"]}, 'owl': {'word': 'owlet', 'why': ["'ow' prefix", "' ow' prefix", "'O' initial", "' Ow' prefix"]}, 'eagle': {'word': 'eaglet', 'why': ["'e' initial", "' e' initial", "'E' initial", "' Eag' prefix"]}}
- elements/state: 107 scenes, admissible False; read tokens {'gas': [' gas', ' Gas'], 'solid': [' solid', ' Solid']}; answers sharing a read token []
- greek/vowel: 121 scenes, admissible False; read tokens {'consonant': [' consonant', ' Cons'], 'vowel': [' vowel', ' V']}; answers sharing a read token []

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


## qa_word (Q-after, word): {'scenes': 600, 'cases': 155, 'dropped': {"the relation's domain is another": 400, 'a bridge without an admissible answer under the relation': 9, 'the bridge is not one token at one position in O and S': 36}, 'domains': {'animals': 155}}

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

PM (scene P2-L0-0000, read tokens O [79006, 113974] S [17080, 28317], src PP):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
What class of animal is Iris's pick? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```


## qb_word (Q-before, word): {'scenes': 600, 'cases': 155, 'dropped': {"the relation's domain is another": 400, 'a bridge without an admissible answer under the relation': 9, 'the bridge is not one token at one position in O and S': 36}, 'domains': {'animals': 155}}

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

PM (scene P2-L0-0000, read tokens O [79006, 113974] S [17080, 28317], src PM):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Question: What class of animal is Iris's pick? Answer with a single word and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|im_end|>
<|im_start|>assistant
<think></think>Answer:
```

