# x53_2x2 plan on muse-glimmer-30b (tokenizer only; UNVERIFIED)

Relation: animals/class (rule in the module docstring). Coverage per candidate (scenes of 600; admissible needs >= 150):

- animals/class: 191 scenes, admissible True; read tokens {'amphibian': [' amphib', ' Amph'], 'arachnid': [' ara', ' Ara'], 'bird': [' bird', ' Bird'], 'insect': [' insect', ' Insect'], 'mammal': [' mamm', ' Mamm']}; answers sharing a read token []; dropped items {'mouse': {'word': 'mammal', 'why': ["'m' initial", "'M' initial"]}}
- animals/young: 19 scenes, admissible False; read tokens {'calf': [' calf', ' Cal'], 'caterpillar': [' cater', ' Cater'], 'chick': [' chick', ' Chick'], 'cub': [' cub', ' Cub'], 'cygnet': [' c', ' C'], 'duckling': [' duck', ' Duck'], 'eaglet': [' e', ' E'], 'fawn': [' f', ' F'], 'foal': [' fo', ' Fo'], 'gosling': [' gos', ' Gos'], 'kid': [' kid', ' Kid'], 'kit': [' kit', ' Kit'], 'kitten': [' kit', ' Kit'], 'lamb': [' lamb', ' Lamb'], 'maggot': [' mag', ' Mag'], 'owlet': [' ow', ' Ow'], 'piglet': [' pig', ' Pig'], 'pup': [' pup', ' Pup'], 'puppy': [' puppy', ' Pup'], 'tadpole': [' tad', ' Tad']}; answers sharing a read token [('kit', 'kitten'), ('pup', 'puppy')]; dropped items {'goose': {'word': 'gosling', 'why': ["'G' initial"]}, 'chicken': {'word': 'chick', 'why': ["'ch' prefix", "'ick' part", "' chick' prefix", "'Ch' prefix", "'ick' part", "' Chick' prefix"]}, 'duck': {'word': 'duckling', 'why': ["'duck' key", "' duck' key", "'Duck' key", "' Duck' key"]}, 'pig': {'word': 'piglet', 'why': ["'pig' key", "' pig' key", "'P' initial", "' Pig' key"]}, 'owl': {'word': 'owlet', 'why': ["'ow' prefix", "' ow' prefix", "'Ow' prefix", "' Ow' prefix"]}, 'eagle': {'word': 'eaglet', 'why': ["'e' initial", "' e' initial", "'E' initial", "' E' initial"]}}
- elements/state: 107 scenes, admissible False; read tokens {'gas': [' gas', ' Gas'], 'solid': [' solid', ' Solid']}; answers sharing a read token []
- greek/vowel: 121 scenes, admissible False; read tokens {'consonant': [' conson', ' Con'], 'vowel': [' vowel', ' V']}; answers sharing a read token []

## qa_num (Q-after, number): {'scenes': 600, 'cases': 530, 'dropped': {'the bridge is not one token at one position in O and S': 70}, 'domains': {'animals': 176, 'elements': 200, 'greek': 154}}

PP (scene P2-L0-0000, read tokens O [33] S [30], src PP):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

PM (scene P2-L0-0000, read tokens O [32] S [36], src PP):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
How many legs does Iris's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```


## qb_num (Q-before, number): {'scenes': 600, 'cases': 530, 'dropped': {'the bridge is not one token at one position in O and S': 70}, 'domains': {'animals': 176, 'elements': 200, 'greek': 154}}

PP (scene P2-L0-0000, read tokens O [33] S [30], src PP):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Question: Which locker belongs to Iris's pick? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|eot|><|start|>assistant to=user<|message|>Answer:
```

PM (scene P2-L0-0000, read tokens O [32] S [36], src PM):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Question: How many legs does Iris's pick have? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|eot|><|start|>assistant to=user<|message|>Answer:
```


## qa_word (Q-after, word): {'scenes': 600, 'cases': 168, 'dropped': {"the relation's domain is another": 400, 'a bridge without an admissible answer under the relation': 9, 'the bridge is not one token at one position in O and S': 23}, 'domains': {'animals': 168}}

PP (scene P2-L0-0000, read tokens O [33] S [30], src PP):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```

PM (scene P2-L0-0000, read tokens O [195444, 139815] S [21103, 39880], src PP):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.
What class of animal is Iris's pick? Answer with a single word and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:
```


## qb_word (Q-before, word): {'scenes': 600, 'cases': 168, 'dropped': {"the relation's domain is another": 400, 'a bridge without an admissible answer under the relation': 9, 'the bridge is not one token at one position in O and S': 23}, 'domains': {'animals': 168}}

PP (scene P2-L0-0000, read tokens O [33] S [30], src PP):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Question: Which locker belongs to Iris's pick? Answer with a single digit and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|eot|><|start|>assistant to=user<|message|>Answer:
```

PM (scene P2-L0-0000, read tokens O [195444, 139815] S [21103, 39880], src PM):

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Question: What class of animal is Iris's pick? Answer with a single word and nothing else.

Scene:
Peter picked the rabbit. The locker of the tick is 2. The locker of the rabbit is 1. The locker of the frog is 5. Noah picked the tick. Iris picked the frog.<|eot|><|start|>assistant to=user<|message|>Answer:
```

