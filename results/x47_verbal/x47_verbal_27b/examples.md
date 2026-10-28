# Examples: x47_verbal_27b

10 random items (seed 0) of 100. The write h + 2 (mu_k - mu_j) is added at ⟦...⟧; the lens reads the same position. UNVERIFIED.

## C2-0069: bridge 'spider' in slot 0, digits by slot [1, 6, 5]

```
<|im_start|>user
The locker of the spider is 1. The locker of the frog is 6. The locker of the tiger is 5. Owen picked the tiger. Tom picked the frog. Beth picked the⟦ spider⟧.
Which locker belongs to Beth's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' ,', ' and', ' .', ' ', ' in', ' Spider', ' (', ' –', '  ', ' spider', ' [', ' as', "'s", ' the', ' at', " '", ' -', ' ;', ' to', ' only']

- write to slot 1 (norm 27.1369): best ordinal rank 33 (' one'), KL 0.0687; x8 lookup answer '1' (original); top 20: [' ,', ' .', ' and', ' ', ' in', ' –', ' Spider', ' the', ' spider', ' as', ' (', ' [', '  ', " '", ' at', ' ;', ' -', ' to', ' from', ' ...']
- identity to slot 1 (norm 27.1369): best ordinal rank 31 (' one'), KL 0.708; x8 lookup answer '1' (original); top 20: [' ,', ' Tiger', ' and', ' .', ' tiger', ' ', ' Tigers', ' in', ' (', ' at', ' as', ' #', ' the', ' T', ' [', ' Tig', '\n', ' to', ' TG', ' -']
- write to slot 2 (norm 33.574): best ordinal rank 24 (' three'), KL 0.159; x8 lookup answer '1' (original); top 20: [' ,', ' .', ' and', ' ', ' in', ' Spider', ' [', ' as', ' the', ' –', ' (', '  ', ' at', ' spider', ' ...', " '", ' ;', ' only', ' from', ' to']
- identity to slot 2 (norm 33.574): best ordinal rank 38 (' one'), KL 2.09; x8 lookup answer '1' (original); top 20: [' Tiger', ' tiger', ' ,', ' Tigers', ' and', ' .', ' ', ' Tig', ' TG', '老虎', ' in', ' tg', ' (', ' #', ' T', ' at', ' as', '虎', '\n', ' the']

## C2-0147: bridge 'beetle' in slot 1, digits by slot [3, 8, 6]

```
<|im_start|>user
The locker of the spider is 3. The locker of the beetle is 8. The locker of the turkey is 6. Oscar picked the⟦ beetle⟧. Zoe picked the turkey. Eric picked the spider.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' Beetle', ' and', ' beetle', ' ,', "'s", '<|endoftext|>', ' ', ' [', '’s', ' ...', ' in', ' [...]', '...', ' .', ' B', ' –', ' as', " '", ',', ' (']

- write to slot 0 (norm 27.1369): best ordinal rank 54 (' first'), KL 0.166; x8 lookup answer '8' (original); top 20: [' Beetle', ' beetle', ' and', "'s", ' ,', ' ', '’s', ' [', ' in', '<|endoftext|>', ' (', ',', ' –', ' beet', ' B', ' as', " '", ' at', ' &', ' to']
- identity to slot 0 (norm 27.1369): best ordinal rank 45 (' later'), KL 6.45; x8 lookup answer '8' (original); top 20: [' and', ' ,', '<|endoftext|>', ' ', ' .', ' –', "'s", '’s', ' in', ' to', ' as', ' &', ' [', ' at', ' the', ' from', ' but', ' (', ' ‘', ' on']
- write to slot 2 (norm 16.788): best ordinal rank 45 (' first'), KL 0.139; x8 lookup answer '8' (original); top 20: [' and', ' Beetle', ' beetle', '<|endoftext|>', ' ,', "'s", ' ...', ' ', ' [', '’s', '...', ' [...]', ' in', ' .', ' as', ',', ' B', ' at', ' (', ' the']
- identity to slot 2 (norm 16.788): best ordinal rank 50 (' later'), KL 3.72; x8 lookup answer '8' (original); top 20: [' and', ' ,', '<|endoftext|>', "'s", ' ', '’s', ' .', ' in', ' –', ' [', ' as', ' to', ' &', ' ...', ' [...]', ' (', '...', ' at', ' the', " '"]

## C2-0078: bridge 'butterfly' in slot 2, digits by slot [9, 7, 6]

```
<|im_start|>user
The locker of the lion is 9. The locker of the cow is 7. The locker of the butterfly is 6. Leo picked the⟦ butterfly⟧. Ben picked the lion. Paul picked the cow.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' ,', ' and', ' .', ' in', "'s", ' Butterfly', ' ', ' butterfly', ' [', ' -', ' as', '’s', ' to', ' ;', " '", ' (', ' the', ' at', ' –', ' but']

- write to slot 0 (norm 33.574): best ordinal rank 24 (' first'), KL 0.107; x8 lookup answer '6' (original); top 20: [' ,', ' and', "'s", ' in', ' .', ' (', ' -', ' ', ' Butterfly', '’s', ' –', ' [', ' butterfly', ' to', " '", ' as', ' ;', ' herself', ' at', ' but']
- identity to slot 0 (norm 33.574): best ordinal rank 101 (' one'), KL 0.701; x8 lookup answer '6' (original); top 20: [' and', ' ,', '’s', "'s", ' cow', ' Cow', ' her', ' .', ' cows', ' in', '<|endoftext|>', ' to', ' ', ' as', ' CW', ' she', ' the', ' at', ' ...', ' ;']
- write to slot 1 (norm 16.788): best ordinal rank 28 (' first'), KL 0.0202; x8 lookup answer '6' (original); top 20: [' ,', ' and', ' .', "'s", ' in', ' Butterfly', ' butterfly', ' ', ' -', ' [', " '", '’s', ' as', ' to', ' –', ' (', ' ;', ' her', ' herself', ' the']
- identity to slot 1 (norm 16.788): best ordinal rank 38 (' first'), KL 0.179; x8 lookup answer '6' (original); top 20: [' ,', ' and', "'s", ' .', '’s', ' in', ' ', ' her', ' to', ' as', '<|endoftext|>', ' ;', ' -', ' the', ' at', ' [', ' but', ' then', ' (', ' of']

## C2-0006: bridge 'frog' in slot 2, digits by slot [5, 8, 4]

```
<|im_start|>user
The locker of the spider is 5. The locker of the fox is 8. The locker of the frog is 4. Kyle picked the spider. Diana picked the⟦ frog⟧. Ruby picked the fox.
Which locker belongs to Diana's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' ,', ' and', ' .', ' ...', ' in', '<|endoftext|>', ' ', ' frog', ' but', ' as', ' Frog', ' at', ' the', ' to', '...', ' only', ' with', ' (', '\n', ' instead']

- write to slot 0 (norm 33.574): best ordinal rank 46 (' one'), KL 0.164; x8 lookup answer '4' (original); top 20: [' ,', ' and', ' .', ' in', ' frog', ' Frog', ' ', ' (', ' but', ' as', ' at', ' to', "'s", ' instead', ' the', ' -', ',', ' only', ' ...', ' with']
- identity to slot 0 (norm 33.574): best ordinal rank 55 (' one'), KL 0.233; x8 lookup answer '4' (original); top 20: [' ,', ' and', ' .', ' Spider', ' in', ' ', ' spider', ' \n', '<|endoftext|>', ' ;', '  ', ' ...', ' as', ' at', '  \n', ' but', "'s", ' to', ' the', ' (']
- write to slot 1 (norm 16.788): best ordinal rank 41 (' after'), KL 0.0319; x8 lookup answer '4' (original); top 20: [' ,', ' and', ' .', ' in', ' frog', ' ...', ' ', ' but', ' Frog', ' as', '<|endoftext|>', ' to', ' the', ' at', ' (', '\n', ' instead', ' only', ' with', ' her']
- identity to slot 1 (norm 16.788): best ordinal rank 37 (' two'), KL 0.0496; x8 lookup answer '4' (original); top 20: [' ,', ' and', ' .', ' in', ' ...', ' ', '<|endoftext|>', ' as', ' but', ' at', ' ;', ' to', ' the', ' with', ' only', ' (', '  ', ' from', ' [', '\n']

## C2-0045: bridge 'goose' in slot 1, digits by slot [4, 3, 7]

```
<|im_start|>user
The locker of the bee is 4. The locker of the goose is 3. The locker of the elephant is 7. Lucy picked the⟦ goose⟧. Grace picked the elephant. James picked the bee.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', ' Goose', ' goose', ' ,', "'s", ' .', ' her', ' in', ' to', ' as', '’s', ' &', ' [...]', ' GS', ' ...', '<|endoftext|>', ',', ' [', '\u200b', '\n']

- write to slot 0 (norm 27.1369): best ordinal rank 76 (' one'), KL 0.0691; x8 lookup answer '4' (target); top 20: [' and', ' Goose', ' ,', ' goose', "'s", ' in', ' to', ' (', ' her', ' &', ',', ' .', '’s', ' as', ' [', ' ', '\u200b', ' G', ' -', ' Eagle']
- identity to slot 0 (norm 27.1369): best ordinal rank 92 (' second'), KL 5.02; x8 lookup answer '4' (target); top 20: [' Bee', ' and', ' bee', ' ,', 'bee', "'s", ' ...', ' B', ' bees', '蜜蜂', '<|endoftext|>', ' .', '’s', ' to', ' -', ' in', ' &', ' /', '\n', ' ']
- write to slot 2 (norm 16.788): best ordinal rank 45 (' two'), KL 0.0278; x8 lookup answer '3' (original); top 20: [' and', ' Goose', ' goose', ' ,', "'s", ' .', '<|endoftext|>', ' in', ' to', ' ...', ' her', ' [...]', ' as', ' [', '’s', '...', ',', ' &', '\u200b', ' ']
- identity to slot 2 (norm 16.788): best ordinal rank 59 (' second'), KL 2.54; x8 lookup answer '3' (original); top 20: [' and', ' ,', "'s", ' Bee', ' bee', ' .', ' ...', '<|endoftext|>', ' to', ' in', '’s', ' &', ' her', ' [', ' -', '\n', 'bee', ' ', ' as', '...']

## C2-0092: bridge 'butterfly' in slot 0, digits by slot [5, 6, 7]

```
<|im_start|>user
The locker of the butterfly is 5. The locker of the tick is 6. The locker of the spider is 7. Noah picked the tick. Sean picked the⟦ butterfly⟧. Kate picked the spider.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' ,', ' and', ' .', ' in', ' (', ' ', ' Butterfly', ' ;', ' -', ' butterfly', ' as', " '", ' the', ' [', ' at', ' but', ' with', ' B', ' ，', ' to']

- write to slot 1 (norm 27.1369): best ordinal rank 20 (' later'), KL 0.0406; x8 lookup answer '6' (target); top 20: [' ,', ' and', ' .', ' in', ' Butterfly', ' ', ' butterfly', ' ;', ' (', ' the', ' as', ' -', " '", ' but', ' [', ' ，', ' with', ' B', ' at', ' by']
- identity to slot 1 (norm 27.1369): best ordinal rank 50 (' first'), KL 0.129; x8 lookup answer '6' (target); top 20: [' ,', ' and', ' ', ' in', ' .', ' (', ' T', ' -', ' as', ' at', ' the', ' to', "'s", ' #', ' –', ' Tick', ' —', ' on', ' instead', ' but']
- write to slot 2 (norm 33.574): best ordinal rank 17 (' later'), KL 0.0818; x8 lookup answer '6' (third); top 20: [' ,', ' and', ' .', ' in', ' ', ' Butterfly', ' ;', ' butterfly', ' the', ' as', ' (', ' -', " '", ' [', ' at', ' with', ' later', ' but', ' ，', ' by']
- identity to slot 2 (norm 33.574): best ordinal rank 64 (' first'), KL 0.262; x8 lookup answer '6' (third); top 20: [' ,', ' and', ' ', ' in', ' (', ' .', ' Tick', ' T', ' -', ' tick', ' as', ' at', ' the', ' —', ' –', ' to', ' Tk', "'s", ' #', ',']

## C2-0089: bridge 'eagle' in slot 1, digits by slot [8, 6, 3]

```
<|im_start|>user
The locker of the fly is 8. The locker of the eagle is 6. The locker of the butterfly is 3. Lucy picked the fly. Ben picked the butterfly. Vera picked the⟦ eagle⟧.
Which locker belongs to Vera's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' ,', ' and', ' .', ' ...', ' Eagle', ' ', ' eagle', ' in', ' as', ' [', ' the', '...', ' (', ' Eagles', ' at', ' three', ' to', ' on', ' #', ' -']

- write to slot 0 (norm 27.1369): best ordinal rank 19 (' one'), KL 0.156; x8 lookup answer '8' (target); top 20: [' and', ' ,', ' Eagle', ' .', ' ', ' eagle', ' ...', ' in', ' Eagles', ' as', ' (', ' [', ' at', ' the', ' to', ' -', ' #', "'s", ' one', ' on']
- identity to slot 0 (norm 27.1369): best ordinal rank 34 (' first'), KL 0.854; x8 lookup answer '8' (target); top 20: [' ,', ' and', ' .', ' ', ' [', ' in', ' ...', ' (', ' the', ' as', ' -', " '", ' ;', ' #', ' Butterfly', ' with', ' butterfly', ' at', ' by', ' but']
- write to slot 2 (norm 16.788): best ordinal rank 10 (' three'), KL 0.0566; x8 lookup answer '6' (original); top 20: [' ,', ' .', ' and', ' ...', ' Eagle', ' ', ' eagle', ' in', ' as', ' three', ' [', '...', ' the', ' Eagles', ' at', ' (', ' to', ' on', ' two', ' one']
- identity to slot 2 (norm 16.788): best ordinal rank 26 (' three'), KL 0.517; x8 lookup answer '6' (original); top 20: [' ,', ' and', ' .', ' ', ' ...', ' in', ' [', ' as', ' the', ' (', ' -', " '", ' #', ' ;', ' at', '...', ' to', ' with', ' only', ' but']

## C2-0076: bridge 'cat' in slot 1, digits by slot [9, 1, 5]

```
<|im_start|>user
The locker of the chicken is 9. The locker of the cat is 1. The locker of the turkey is 5. Emma picked the⟦ cat⟧. Laura picked the turkey. Alice picked the chicken.
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', ' ,', "'s", '’s', ' .', '\n', ' Cat', ' cat', ' ', ' cats', ' –', ' ...', ' in', '<|endoftext|>', '...', ' to', " '", ' s', ' &', ' as']

- write to slot 0 (norm 27.1369): best ordinal rank 80 (' one'), KL 0.0726; x8 lookup answer '9' (target); top 20: [' and', ' ,', "'s", '’s', ' –', ' .', ' Cat', ' ', ' in', ' (', '\n', ' cats', ' &', ' to', ' cat', ' Cats', ' -', " '", ' s', 'and']
- identity to slot 0 (norm 27.1369): best ordinal rank 45 (' first'), KL 0.284; x8 lookup answer '9' (target); top 20: [' and', ' ,', ' .', '<|endoftext|>', ' –', ' ', "'s", ' as', ' in', ' to', ' [', '’s', '–', ',', '...', '\xa0', ' (', ' the', '\n\n', ' at']
- write to slot 2 (norm 16.788): best ordinal rank 70 (' one'), KL 0.0272; x8 lookup answer '1' (original); top 20: [' and', ' ,', "'s", ' .', '’s', '<|endoftext|>', ' ...', ' cat', ' Cat', ' ', ' cats', '...', '\n', ' in', ' –', ' to', ' as', ' Cats', ' the', ' s']
- identity to slot 2 (norm 16.788): best ordinal rank 52 (' first'), KL 0.137; x8 lookup answer '1' (original); top 20: [' and', ' ,', ' .', "'s", ' ', ' –', '<|endoftext|>', '’s', ' in', ' to', ' as', '...', '\n', '–', ' ...', ' [', ' (', ',', ' the', ' at']

## C2-0054: bridge 'lion' in slot 1, digits by slot [5, 4, 1]

```
<|im_start|>user
The locker of the wolf is 5. The locker of the lion is 4. The locker of the ant is 1. Eric picked the ant. Rose picked the⟦ lion⟧. Emma picked the wolf.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', ' ,', ' ...', ' .', '...', ' ', ' in', ' #', ' Lion', ' as', ' &', ' lion', ' but', ' at', ' the', ' to', ' on', ' [', ' [...]', ' or']

- write to slot 0 (norm 27.1369): best ordinal rank 31 (' one'), KL 0.125; x8 lookup answer '4' (original); top 20: [' and', ' ,', ' .', ' ...', ' ', ' Lion', ' in', ' &', '...', ' #', ' lion', ' as', "'s", ' at', ' (', ' but', ' to', ' or', '’s', ' the']
- identity to slot 0 (norm 27.1369): best ordinal rank 41 (' two'), KL 0.412; x8 lookup answer '4' (original); top 20: [' ,', ' and', ' .', ' ...', ' ', ' in', ' her', ' but', ' ;', ' #', ' -', ' the', ' as', '...', ' (', " '", ' s', ' a', ' at', ' or']
- write to slot 2 (norm 16.788): best ordinal rank 22 (' two'), KL 0.072; x8 lookup answer '4' (original); top 20: [' and', ' ,', ' ...', ' .', '...', ' ', ' in', ' as', ' #', ' lion', ' Lion', ' at', ' but', ' the', ' [...]', ' &', ' on', ' to', ' [', ' only']
- identity to slot 2 (norm 16.788): best ordinal rank 31 (' two'), KL 0.213; x8 lookup answer '4' (original); top 20: [' ,', ' and', ' .', ' ...', ' ', ' in', '...', ' but', ' #', ' as', ' the', ' ;', ' at', ' -', ' to', ' (', ' s', ' her', ' or', ' on']

## C2-0088: bridge 'frog' in slot 0, digits by slot [3, 7, 5]

```
<|im_start|>user
The locker of the frog is 3. The locker of the horse is 7. The locker of the bee is 5. Will picked the bee. Peter picked the horse. Grace picked the⟦ frog⟧.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' ,', ' and', ' .', ' Frog', ' frog', ' in', ' ', ' ...', ' (', '...', ' -', ' as', ' the', " '", ' to', ' at', "'s", ' [', ' only', ' on']

- write to slot 1 (norm 27.1369): best ordinal rank 25 (' three'), KL 0.101; x8 lookup answer '3' (original); top 20: [' ,', ' .', ' and', ' ...', ' frog', ' Frog', '...', ' in', ' ', ' the', ' as', ' -', " '", ' to', ' (', '\n', ' at', ' from', ' [', ' on']
- identity to slot 1 (norm 27.1369): best ordinal rank 36 (' three'), KL 0.818; x8 lookup answer '3' (original); top 20: [' ,', ' and', ' bee', ' Bee', ' .', ' in', 'bee', ' ...', ' ', ' -', ' (', ' the', ' to', ' /', ' [', '...', ' &', ' as', ' #', ' at']
- write to slot 2 (norm 33.574): best ordinal rank 12 (' three'), KL 0.271; x8 lookup answer '5' (target); top 20: [' ,', ' .', ' ...', ' and', '...', ' in', ' ', ' Frog', ' frog', ' as', ' the', ' three', ' -', ' to', ' (', " '", ' at', ' [', ' only', ' on']
- identity to slot 2 (norm 33.574): best ordinal rank 47 (' three'), KL 1.91; x8 lookup answer '5' (target); top 20: [' bee', ' Bee', ' ,', ' and', 'bee', ' .', ' bees', ' in', ' ...', ' ', ' -', ' &', ' /', ' (', ' the', ' B', ' to', ' [', ' honey', '蜜蜂']

