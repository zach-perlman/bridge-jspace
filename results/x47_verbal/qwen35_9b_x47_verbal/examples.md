# Examples: qwen35_9b_x47_verbal

10 random items (seed 0) of 100. The write h + 2 (mu_k - mu_j) is added at ⟦...⟧; the lens reads the same position. UNVERIFIED.

## C2-0085: bridge 'owl' in slot 2, digits by slot [7, 2, 4]

```
<|im_start|>user
The locker of the goat is 7. The locker of the frog is 2. The locker of the owl is 4. Diana picked the frog. Alice picked the goat. Ivan picked the⟦ owl⟧.
Which locker belongs to Ivan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', '\n\n', ' in', ' owl', ' at', ' .', ',', ' with', ' ,', ' to', ' Owl', ' as', ' from', ' for', ' but', ' on', ' only', ' (', ' which', ' by']

- write to slot 0 (norm 9.6374): best ordinal rank 16 (' three'), KL 0.503; x8 lookup answer '4' (original); top 20: [' and', ' in', ' owl', ' at', ',', ' with', ' ,', ' .', "'s", ' to', ' as', ' Owl', ' (', ' which', ' whose', ' on', ' only', ' three', ' for', ' from']
- identity to slot 0 (norm 9.6374): best ordinal rank 23 (' three'), KL 0.458; x8 lookup answer '4' (original); top 20: [' and', ' ,', ' in', ' .', '\n\n', ' at', ' with', ' instead', ' to', ' but', ' (', ' for', ',', ' ...', ' as', ' on', ' which', ' only', ' or', ' that']
- write to slot 1 (norm 4.8601): best ordinal rank 28 (' three'), KL 0.0852; x8 lookup answer '4' (original); top 20: [' and', ' in', '\n\n', ' owl', ' .', ' at', ',', ' ,', ' to', ' with', ' Owl', ' as', ' from', ' (', ' for', ' but', ' which', ' on', "'s", ' only']
- identity to slot 1 (norm 4.8601): best ordinal rank 21 (' three'), KL 0.193; x8 lookup answer '4' (original); top 20: [' and', '\n\n', ' in', ' ,', ' .', ' at', ' with', ' to', ',', ' as', ' but', ' instead', ' for', ' (', ' on', ' from', ' which', ' only', ' by', ' that']

## C2-0168: bridge 'rabbit' in slot 2, digits by slot [2, 3, 6]

```
<|im_start|>user
The locker of the duck is 2. The locker of the tick is 3. The locker of the rabbit is 6. Ivan picked the duck. Ella picked the tick. Tara picked the⟦ rabbit⟧.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', ' ,', '\n\n', ' in', ' .', ' at', ' with', ' to', ' for', ' as', ' but', ' from', ',', ' \n\n', ' (', ' on', ' that', ' three', ' only', ' by']

- write to slot 0 (norm 9.6374): best ordinal rank 16 (' three'), KL 0.285; x8 lookup answer '6' (original); top 20: [' and', ' ,', ' in', ' .', ' at', ' to', ' with', ' as', ' again', ' (', ' for', ',', ' animal', ' but', ' that', ' three', ' from', ' on', ' Rabbit', ' all']
- identity to slot 0 (norm 9.6374): best ordinal rank 40 (' after'), KL 0.299; x8 lookup answer '6' (original); top 20: [' and', '\n\n', ' .', ' ,', ' ...', '...', ' in', ' at', '  \n\n', ' \n\n', ' with', '  \n', ' but', ' from', ' to', ' \n\n\n', ' as', '\n\n\n', ' duck', ' &']
- write to slot 1 (norm 4.8601): best ordinal rank 23 (' three'), KL 0.0476; x8 lookup answer '6' (original); top 20: [' and', ' ,', ' in', ' .', ' at', ' to', '\n\n', ' with', ' as', ' for', ' from', ' but', ' (', ',', ' on', ' that', ' Rabbit', ' again', ' only', ' by']
- identity to slot 1 (norm 4.8601): best ordinal rank 30 (' three'), KL 0.0703; x8 lookup answer '6' (original); top 20: [' and', '\n\n', ' .', ' ,', ' in', ' at', ' ...', ' with', ' \n\n', ' to', ' but', ' as', ' from', '...', '  \n\n', ' for', ' that', ' on', ' (', ',']

## C2-0091: bridge 'duck' in slot 2, digits by slot [4, 1, 2]

```
<|im_start|>user
The locker of the lion is 4. The locker of the elephant is 1. The locker of the duck is 2. Iris picked the lion. Ruby picked the elephant. Liam picked the⟦ duck⟧.
Which locker belongs to Liam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', ' .', ' ,', ' in', '\n\n', ' at', '  \n', ' with', ' to', ' duck', ' as', ' but', '  \n\n', ' Duck', ' (', ' instead', ' only', ' from', ' &', ' under']

- write to slot 0 (norm 9.6374): best ordinal rank 29 (' three'), KL 0.23; x8 lookup answer '2' (original); top 20: [' and', ' .', ' ,', ' duck', ' in', ' Duck', ' at', ' with', ' to', ' (', ' as', ' ducks', ' only', ' under', ' but', ' instead', ' for', ' that', ' animal', ' from']
- identity to slot 0 (norm 9.6374): best ordinal rank 12 (' three'), KL 0.384; x8 lookup answer '2' (original); top 20: [' and', ' .', ' in', ' elephant', ',', ' ,', ' to', ' at', ' as', ' with', ' Elephant', ' three', ' (', ' instead', ' but', ' only', ' for', "'s", ' under', ' two']
- write to slot 1 (norm 4.8601): best ordinal rank 28 (' after'), KL 0.0282; x8 lookup answer '2' (original); top 20: [' and', ' .', ' ,', ' in', ' at', '  \n', ' duck', ' to', ' with', ' as', ' Duck', ' (', ' &', ' but', '\n\n', ' under', ' from', ' for', ' only', ' instead']
- identity to slot 1 (norm 4.8601): best ordinal rank 17 (' three'), KL 0.145; x8 lookup answer '2' (original); top 20: [' and', ' .', ' ,', ' in', ' at', ' to', ' with', ' as', ',', '\n\n', ' (', ' but', ' instead', ' only', ' for', ' under', ' three', ' from', '  \n', ' that']

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

Lens top 20, h alone: [' and', ',', '\n\n', ' in', ' ,', ' .', ' at', ' but', ' with', ' to', ' instead', ' \n', ' for', ' ...', ' as', ' on', ' only', ' (', ' frog', ' under']

- write to slot 0 (norm 9.6374): best ordinal rank 20 (' two'), KL 0.217; x8 lookup answer '5' (target); top 20: [' and', ',', ' in', ' ,', ' at', ' .', ' with', "'s", ' but', ' to', ' instead', ' frog', ' (', ' for', ' Frog', ' as', ' on', ' only', ' which', ' under']
- identity to slot 0 (norm 9.6374): best ordinal rank 51 (' after'), KL 0.666; x8 lookup answer '5' (target); top 20: [' and', ' \n', '  \n', ' .', ' \n\n\n', ' \n\n', ' ,', '\n\n', ',', ' in', ' with', ' at', '\n\n\n', ' \n  \n', '\n \n', '  \n\n', '  \n\n\n', "'s", ' only', ' but']
- write to slot 1 (norm 4.8601): best ordinal rank 24 (' two'), KL 0.0343; x8 lookup answer '4' (original); top 20: [' and', ',', ' ,', ' in', ' .', ' at', ' but', '\n\n', ' with', ' to', ' instead', ' for', ' ...', ' as', ' frog', ' (', ' \n', ' on', "'s", ' only']
- identity to slot 1 (norm 4.8601): best ordinal rank 35 (' two'), KL 0.0886; x8 lookup answer '4' (original); top 20: [' and', ' \n', ' .', '\n\n', ' ,', ',', ' in', ' at', ' with', '  \n', ' \n\n', ' \n\n\n', ' but', ' to', ' instead', ' only', ' as', '\n\n\n', ' for', "'s"]

## C2-0057: bridge 'ant' in slot 0, digits by slot [4, 2, 1]

```
<|im_start|>user
The locker of the ant is 4. The locker of the deer is 2. The locker of the cow is 1. Tom picked the deer. Zoe picked the⟦ ant⟧. Dan picked the cow.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', ' ,', '\n\n', ' .', ' at', ' to', ' in', ' ...', ' with', ' \n\n', "'s", ' \n', ' as', ' instead', ' (', ' for', ' on', ' but', ' only', ',']

- write to slot 1 (norm 8.1996): best ordinal rank 32 (' two'), KL 1.84; x8 lookup answer '2' (target); top 20: ['\n\n', ' ...', ' and', '...', ' \n\n', ' .', ' ,', ' \n', '\n\n\n', ' \n\n\n', ' …', '\n \n', '  \n\n', ' at', ' to', ' in', ' with', '…', '  \n', ' as']
- identity to slot 1 (norm 8.1996): best ordinal rank 19 (' two'), KL 0.127; x8 lookup answer '2' (target); top 20: [' and', ' ,', '\n\n', ' .', ' at', ' in', ' with', ' to', ' as', ',', ' but', ' (', '’s', ' for', "'s", ' instead', ' animal', ' cow', ' two', ' which']
- write to slot 2 (norm 9.6374): best ordinal rank 35 (' two'), KL 2.9; x8 lookup answer '2' (third); top 20: ['\n\n', ' ...', ' \n\n', '...', ' and', '\n\n\n', ' \n', ' \n\n\n', ' .', ' ,', ' …', '\n \n', '  \n\n', ' at', ' to', ' in', '…', '\n\n\n\n', '  \n', ' with']
- identity to slot 2 (norm 9.6374): best ordinal rank 19 (' two'), KL 0.174; x8 lookup answer '2' (third); top 20: [' and', ' ,', '\n\n', ' .', ' at', ' in', ' with', ' to', ' cow', '’s', ',', ' as', ' but', ' (', ' for', ' animal', "'s", ' instead', ' farm', ' two']

## C2-0110: bridge 'chicken' in slot 2, digits by slot [5, 6, 7]

```
<|im_start|>user
The locker of the butterfly is 5. The locker of the bee is 6. The locker of the chicken is 7. Clara picked the butterfly. Diana picked the⟦ chicken⟧. Liam picked the bee.
Which locker belongs to Diana's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', ' ,', '  \n', ' .', ' \n', ' at', ' with', ' in', ',', ' but', ' to', ' two', ' as', '\n\n', ' for', ' only', ' on', ' already', ' (', ' \n\n']

- write to slot 0 (norm 9.6374): best ordinal rank 9 (' two'), KL 0.203; x8 lookup answer '5' (target); top 20: [' and', ' ,', ' with', ' at', ' .', ' in', ',', ' chicken', ' two', ' as', ' (', ' to', ' already', ' but', ' for', ' only', ' on', ' Chick', ' animal', ' three']
- identity to slot 0 (norm 9.6374): best ordinal rank 19 (' two'), KL 0.273; x8 lookup answer '5' (target); top 20: [' and', ' \n', '  \n', ',', ' \n\n', ' in', ' .', '\n\n', ' ,', ' with', ' at', '  \n\n', ' ...', ' (', ' instead', ' only', ' \n\n\n', ' as', ' two', ' but']
- write to slot 1 (norm 4.8601): best ordinal rank 12 (' two'), KL 0.031; x8 lookup answer '7' (original); top 20: [' and', ' ,', ' .', '  \n', ' at', ' in', ' with', ' \n', ',', ' as', ' to', ' two', ' but', ' already', ' for', ' (', ' only', ' &', ' on', ' under']
- identity to slot 1 (norm 4.8601): best ordinal rank 15 (' two'), KL 0.0567; x8 lookup answer '7' (original); top 20: [' and', ' \n', '  \n', ' ,', ' .', ',', ' in', ' with', ' at', '\n\n', ' \n\n', ' as', ' but', ' only', ' to', ' (', ' two', ' instead', '  \n\n', ' for']

## C2-0107: bridge 'duck' in slot 2, digits by slot [9, 1, 5]

```
<|im_start|>user
The locker of the bee is 9. The locker of the fox is 1. The locker of the duck is 5. David picked the⟦ duck⟧. Luke picked the fox. Kate picked the bee.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', ' .', ' in', ' at', ' ,', ' duck', ' to', ' with', ' Duck', ' from', ' ducks', ' but', ' as', ',', "'s", ' that', '  \n', ' which', ' (', '\n\n']

- write to slot 0 (norm 9.6374): best ordinal rank 39 (' first'), KL 0.186; x8 lookup answer '9' (target); top 20: [' and', ' duck', ' in', ' Duck', ' .', ' at', ' ,', ' ducks', "'s", ' to', ' with', ' (', ' shot', ',', ' that', ' as', ' which', ' from', ' animal', ' Ducks']
- identity to slot 0 (norm 9.6374): best ordinal rank 28 (' first'), KL 0.529; x8 lookup answer '9' (target); top 20: [' and', ' in', ',', ' at', ' bee', ' to', ' with', ' Bee', "'s", ' .', ' which', ' as', ' but', ' (', ' ,', ' for', '\n\n', ' that', ' from', ' on']
- write to slot 1 (norm 4.8601): best ordinal rank 50 (' after'), KL 0.0269; x8 lookup answer '5' (original); top 20: [' and', ' .', ' in', ' duck', ' ,', ' at', ' to', ' Duck', ' with', ' ducks', ' from', "'s", ' as', ',', ' (', ' but', ' shot', ' which', ' that', ' on']
- identity to slot 1 (norm 4.8601): best ordinal rank 31 (' first'), KL 0.192; x8 lookup answer '5' (original); top 20: [' and', ' in', ' at', ' to', ' .', ',', ' with', ' ,', "'s", ' but', ' as', ' from', ' which', ' (', ' that', '\n\n', ' on', ' for', ' only', ' by']

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

Lens top 20, h alone: [' and', ' in', ' frog', ' Frog', ',', ' at', ' .', ' to', ' ,', ' with', ' instead', ' for', ' (', ' only', "'s", ' as', ' but', ' which', ' whose', ' that']

- write to slot 1 (norm 8.1996): best ordinal rank 29 (' after'), KL 0.092; x8 lookup answer '7' (target); top 20: [' and', '\n\n', ' in', ' .', ' ,', ' at', ' to', ' frog', ' ...', ',', ' Frog', ' with', ' instead', ' for', '...', ' but', ' as', ' only', ' (', ' from']
- identity to slot 1 (norm 8.1996): best ordinal rank 21 (' first'), KL 0.195; x8 lookup answer '7' (target); top 20: [' and', ',', ' in', ' at', ' to', ' with', ' .', ' only', "'s", ' for', ' ,', ' (', ' as', ' which', ' by', ' but', ' whose', ' from', ' that', ' bee']
- write to slot 2 (norm 9.6374): best ordinal rank 31 (' after'), KL 0.281; x8 lookup answer '3' (original); top 20: [' and', '\n\n', ' in', ' .', ' at', ' ...', ' to', ',', ' ,', ' with', ' frog', ' instead', ' Frog', ' for', '...', ' only', ' but', ' as', ' \n', ' from']
- identity to slot 2 (norm 9.6374): best ordinal rank 22 (' first'), KL 0.257; x8 lookup answer '3' (original); top 20: [' and', ',', ' in', ' at', ' to', ' with', ' .', ' bee', "'s", ' only', ' Bee', ' for', ' (', ' as', ' ,', ' by', ' which', ' from', ' whose', ' but']

## C2-0066: bridge 'cow' in slot 1, digits by slot [7, 2, 1]

```
<|im_start|>user
The locker of the owl is 7. The locker of the cow is 2. The locker of the lion is 1. Iris picked the lion. Ivy picked the⟦ cow⟧. Amy picked the owl.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: ['\n\n', ' and', ' .', ' ,', ' \n\n', '\n\n\n', '  \n\n', '...', ' ...', ' in', ' at', ',', '  \n', ' \n\n\n', ' with', '  \n\n\n', ' to', ' \n', ' but', ' as']

- write to slot 0 (norm 8.1996): best ordinal rank 17 (' two'), KL 1.84; x8 lookup answer '7' (target); top 20: [' and', ' ,', '\n\n', ' .', ',', ' in', ' at', ' with', ' to', ' (', ' as', ' but', ' under', ' for', ' that', ' which', ' two', ' on', ' only', ' again']
- identity to slot 0 (norm 8.1996): best ordinal rank 33 (' two'), KL 0.218; x8 lookup answer '7' (target); top 20: ['\n\n', ' and', ' \n\n', '\n\n\n', '...', ' ...', '  \n\n', ' .', ',', ' in', '  \n', ' ,', ' \n', ' \n\n\n', ' at', '<|im_end|>', ' to', ' with', '  \n\n\n', '\n']
- write to slot 2 (norm 4.8601): best ordinal rank 33 (' two'), KL 0.139; x8 lookup answer '2' (original); top 20: ['\n\n', ' and', ' .', '\n\n\n', ' \n\n', ' ,', '  \n\n', '...', ' ...', ' in', ' at', ' \n\n\n', '  \n', ',', ' \n', '\n\n\n\n', '  \n\n\n', ' with', ' to', ' but']
- identity to slot 2 (norm 4.8601): best ordinal rank 32 (' two'), KL 0.104; x8 lookup answer '2' (original); top 20: ['\n\n', ' and', ' \n\n', '\n\n\n', ' .', '...', '  \n\n', ' ,', ' ...', ' in', ',', '  \n', ' at', ' \n\n\n', ' \n', ' to', ' with', '  \n\n\n', '\n\n\n\n', '<|im_end|>']

## C2-0106: bridge 'fox' in slot 1, digits by slot [1, 3, 8]

```
<|im_start|>user
The locker of the duck is 1. The locker of the fox is 3. The locker of the frog is 8. Sara picked the duck. Hugo picked the⟦ fox⟧. Tara picked the frog.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Lens top 20, h alone: [' and', '\n\n', ' ,', ' .', ' in', ' at', ' with', '\n\n\n', ' to', ' but', ' (', ' as', ' ...', ' --', ' two', ' by', ' from', ' for', ' ?', ' on']

- write to slot 0 (norm 8.1996): best ordinal rank 13 (' two'), KL 1.27; x8 lookup answer '3' (original); top 20: [' and', ' ,', ' .', ' in', '\n\n', ' at', ' with', ' (', ' to', ' --', ' but', ' as', ' two', ' on', ' fox', ' for', ' again', ' instead', ' from', ' that']
- identity to slot 0 (norm 8.1996): best ordinal rank 34 (' two'), KL 0.051; x8 lookup answer '3' (original); top 20: ['\n\n', ' and', ' .', ' ,', ' in', ' at', ' \n\n', ' with', '  \n\n', '\n\n\n', ' ...', ' but', ' to', ' (', ' from', ' as', ' &', ' on', ' under', '  \n']
- write to slot 2 (norm 4.8601): best ordinal rank 16 (' two'), KL 0.288; x8 lookup answer '3' (original); top 20: ['\n\n', ' and', ' ,', ' .', ' in', '\n\n\n', ' at', ' with', ' but', ' to', ' \n\n', ' ...', ' (', ' as', ' from', ' by', ' two', ' on', ' for', ' --']
- identity to slot 2 (norm 4.8601): best ordinal rank 22 (' two'), KL 0.0245; x8 lookup answer '3' (original); top 20: ['\n\n', ' and', ' ,', ' .', ' in', ' at', ' with', '\n\n\n', ' but', ' ...', ' to', ' \n\n', ' (', ' as', ' from', '  \n\n', ' on', ' for', ' by', ' ;']

