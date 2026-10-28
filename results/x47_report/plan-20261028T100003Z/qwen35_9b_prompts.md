# 47.10 plan: qwen3.5-9b, 5 example items of 500 (seed 0), the report prompts as the model reads them (ids decoded, the template included), the bridge word in ⟦...⟧, the read suffix appended (a space token for the digit reader, nothing for the word reader). UNVERIFIED.


### C0-0284: bridge frog (slot 3) -> eagle (slot 2)

[last] report: O answers 'third' (token 4688), S answers 'second' (token 2018); bridge token 38

```
<|im_start|>user
The locker of the deer is 1. The locker of the eagle is 7. The locker of the frog is 2. Mark picked the deer. Luke picked the⟦ frog⟧. Will picked the eagle.
Was the locker of Luke's pick listed first, second or third? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[last] report_digit: O answers '3' (token 18), S answers '2' (token 17); bridge token 38

```
<|im_start|>user
The locker of the deer is 1. The locker of the eagle is 7. The locker of the frog is 2. Mark picked the deer. Luke picked the⟦ frog⟧. Will picked the eagle.
Was the locker of Luke's pick listed 1, 2 or 3? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

[first] report: O answers 'third' (token 4688), S answers 'second' (token 2018); bridge token 62

```
<|im_start|>user
Was the locker of Luke's pick listed first, second or third? Answer with a single word and nothing else.
The locker of the deer is 1. The locker of the eagle is 7. The locker of the frog is 2. Mark picked the deer. Luke picked the⟦ frog⟧. Will picked the eagle.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[first] report_digit: O answers '3' (token 18), S answers '2' (token 17); bridge token 65

```
<|im_start|>user
Was the locker of Luke's pick listed 1, 2 or 3? Answer with a single digit and nothing else.
The locker of the deer is 1. The locker of the eagle is 7. The locker of the frog is 2. Mark picked the deer. Luke picked the⟦ frog⟧. Will picked the eagle.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

### C0-0314: bridge turkey (slot 1) -> horse (slot 3)

[last] report: O answers 'first' (token 1118), S answers 'third' (token 4688); bridge token 38

```
<|im_start|>user
The locker of the turkey is 6. The locker of the fox is 1. The locker of the horse is 4. Owen picked the horse. Peter picked the⟦ turkey⟧. Sam picked the fox.
Was the locker of Peter's pick listed first, second or third? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[last] report_digit: O answers '1' (token 16), S answers '3' (token 18); bridge token 38

```
<|im_start|>user
The locker of the turkey is 6. The locker of the fox is 1. The locker of the horse is 4. Owen picked the horse. Peter picked the⟦ turkey⟧. Sam picked the fox.
Was the locker of Peter's pick listed 1, 2 or 3? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

[first] report: O answers 'first' (token 1118), S answers 'third' (token 4688); bridge token 62

```
<|im_start|>user
Was the locker of Peter's pick listed first, second or third? Answer with a single word and nothing else.
The locker of the turkey is 6. The locker of the fox is 1. The locker of the horse is 4. Owen picked the horse. Peter picked the⟦ turkey⟧. Sam picked the fox.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[first] report_digit: O answers '1' (token 16), S answers '3' (token 18); bridge token 65

```
<|im_start|>user
Was the locker of Peter's pick listed 1, 2 or 3? Answer with a single digit and nothing else.
The locker of the turkey is 6. The locker of the fox is 1. The locker of the horse is 4. Owen picked the horse. Peter picked the⟦ turkey⟧. Sam picked the fox.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

### C0-0578: bridge fly (slot 2) -> spider (slot 1)

[last] report: O answers 'second' (token 2018), S answers 'first' (token 1118); bridge token 38

```
<|im_start|>user
The locker of the spider is 6. The locker of the fly is 2. The locker of the elephant is 8. Sam picked the spider. Dan picked the⟦ fly⟧. Ben picked the elephant.
Was the locker of Dan's pick listed first, second or third? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[last] report_digit: O answers '2' (token 17), S answers '1' (token 16); bridge token 38

```
<|im_start|>user
The locker of the spider is 6. The locker of the fly is 2. The locker of the elephant is 8. Sam picked the spider. Dan picked the⟦ fly⟧. Ben picked the elephant.
Was the locker of Dan's pick listed 1, 2 or 3? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

[first] report: O answers 'second' (token 2018), S answers 'first' (token 1118); bridge token 62

```
<|im_start|>user
Was the locker of Dan's pick listed first, second or third? Answer with a single word and nothing else.
The locker of the spider is 6. The locker of the fly is 2. The locker of the elephant is 8. Sam picked the spider. Dan picked the⟦ fly⟧. Ben picked the elephant.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[first] report_digit: O answers '2' (token 17), S answers '1' (token 16); bridge token 65

```
<|im_start|>user
Was the locker of Dan's pick listed 1, 2 or 3? Answer with a single digit and nothing else.
The locker of the spider is 6. The locker of the fly is 2. The locker of the elephant is 8. Sam picked the spider. Dan picked the⟦ fly⟧. Ben picked the elephant.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

### C0-0640: bridge eagle (slot 3) -> spider (slot 2)

[last] report: O answers 'third' (token 4688), S answers 'second' (token 2018); bridge token 33

```
<|im_start|>user
The locker of the goat is 2. The locker of the spider is 8. The locker of the eagle is 1. Clara picked the⟦ eagle⟧. Nina picked the goat. Laura picked the spider.
Was the locker of Clara's pick listed first, second or third? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[last] report_digit: O answers '3' (token 18), S answers '2' (token 17); bridge token 33

```
<|im_start|>user
The locker of the goat is 2. The locker of the spider is 8. The locker of the eagle is 1. Clara picked the⟦ eagle⟧. Nina picked the goat. Laura picked the spider.
Was the locker of Clara's pick listed 1, 2 or 3? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

[first] report: O answers 'third' (token 4688), S answers 'second' (token 2018); bridge token 57

```
<|im_start|>user
Was the locker of Clara's pick listed first, second or third? Answer with a single word and nothing else.
The locker of the goat is 2. The locker of the spider is 8. The locker of the eagle is 1. Clara picked the⟦ eagle⟧. Nina picked the goat. Laura picked the spider.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[first] report_digit: O answers '3' (token 18), S answers '2' (token 17); bridge token 60

```
<|im_start|>user
Was the locker of Clara's pick listed 1, 2 or 3? Answer with a single digit and nothing else.
The locker of the goat is 2. The locker of the spider is 8. The locker of the eagle is 1. Clara picked the⟦ eagle⟧. Nina picked the goat. Laura picked the spider.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

### C0-0672: bridge spider (slot 3) -> pig (slot 1)

[last] report: O answers 'third' (token 4688), S answers 'first' (token 1118); bridge token 33

```
<|im_start|>user
The locker of the pig is 4. The locker of the tick is 1. The locker of the spider is 5. Tara picked the⟦ spider⟧. Olivia picked the pig. Henry picked the tick.
Was the locker of Tara's pick listed first, second or third? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[last] report_digit: O answers '3' (token 18), S answers '1' (token 16); bridge token 33

```
<|im_start|>user
The locker of the pig is 4. The locker of the tick is 1. The locker of the spider is 5. Tara picked the⟦ spider⟧. Olivia picked the pig. Henry picked the tick.
Was the locker of Tara's pick listed 1, 2 or 3? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

[first] report: O answers 'third' (token 4688), S answers 'first' (token 1118); bridge token 57

```
<|im_start|>user
Was the locker of Tara's pick listed first, second or third? Answer with a single word and nothing else.
The locker of the pig is 4. The locker of the tick is 1. The locker of the spider is 5. Tara picked the⟦ spider⟧. Olivia picked the pig. Henry picked the tick.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

[first] report_digit: O answers '3' (token 18), S answers '1' (token 16); bridge token 60

```
<|im_start|>user
Was the locker of Tara's pick listed 1, 2 or 3? Answer with a single digit and nothing else.
The locker of the pig is 4. The locker of the tick is 1. The locker of the spider is 5. Tara picked the⟦ spider⟧. Olivia picked the pig. Henry picked the tick.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```
