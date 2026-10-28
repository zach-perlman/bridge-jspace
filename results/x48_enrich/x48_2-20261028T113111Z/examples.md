# 48.2 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge token, ⟦person:…⟧ the asked person's token(s). UNVERIFIED.

## qwen35_9b_x48_2a (design A, the bridge token): 10 random items of 200 (seed 0)

### P2-L0-0017 (greek): bridge iota (attribute 9) → delta (attribute 4)

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. ⟦person:Leo⟧ picked ⟦bridge:iota⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '9' | 0 | 1 | None | '2' | 0 | 1 |
| alt | '4' | 1 | 0 | None | '6' | 1 | 0 |
| whole | '4' | 1 | 0 | ' 4\n' | '6' | 1 | 0 |
| no_jpp | '4' | 1 | 0 | ' 4\n' | '6' | 1 | 0 |
| no_rand | '4' | 1 | 0 | ' 4\n' | '6' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0096 (animals): bridge bee (attribute 6) → spider (attribute 8)

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. ⟦person:Will⟧ picked the ⟦bridge:bee⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '6' | 0 | 1 | None | '1' | 0 | 1 |
| alt | '8' | 1 | 0 | None | '5' | 1 | 0 |
| whole | '8' | 1 | 0 | ' 8\n' | '5' | 1 | 0 |
| no_jpp | '8' | 1 | 0 | ' 8\n' | '5' | 1 | 0 |
| no_rand | '8' | 1 | 0 | ' 8\n' | '5' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | -0.530 | -0.402 | 0.128 | 1.00 | 0.00 | 0.00 |
| 14 | -0.462 | -0.445 | 0.016 | 1.00 | 0.00 | 0.00 |
| 16 | -0.436 | -0.305 | 0.132 | 0.40 | 0.00 | 0.00 |
| 18 | -0.374 | -0.242 | 0.132 | 0.68 | 0.00 | 0.48 |
| 20 | -0.774 | -0.328 | 0.446 | 1.00 | 0.27 | 0.87 |
| 22 | -0.622 | -0.316 | 0.306 | 0.99 | 0.38 | 0.88 |
| 24 | -0.631 | -0.326 | 0.305 | 1.00 | 0.27 | 0.90 |
| 26 | -0.735 | -0.315 | 0.421 | 1.00 | 0.32 | 0.88 |
| 28 | -0.740 | -0.334 | 0.406 | 0.99 | 0.27 | 0.84 |
| 30 | -0.761 | -0.341 | 0.420 | 0.98 | 0.25 | 0.82 |
| 31 | -0.692 | -0.379 | 0.313 | 1.00 | 0.24 | 0.87 |

### P2-L0-0110 (greek): bridge iota (attribute 9) → epsilon (attribute 5)

```
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. ⟦person:Anna⟧ picked ⟦bridge:iota⟧.
Which position in the Greek alphabet does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '9' | 0 | 1 | None | '2' | 0 | 1 |
| alt | '5' | 1 | 0 | None | '7' | 1 | 0 |
| whole | '5' | 1 | 0 | ' 5\n' | '7' | 1 | 0 |
| no_jpp | '9' | 0 | 1 | ' 9\n' | '7' | 1 | 0 |
| no_rand | '5' | 1 | 0 | ' 5\n' | '7' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0142 (elements): bridge nitrogen (attribute 7) → oxygen (attribute 8)

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. ⟦person:Owen⟧ picked ⟦bridge:nitrogen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '7' | 0 | 1 | None | '3' | 0 | 1 |
| alt | '8' | 1 | 0 | None | '6' | 1 | 0 |
| whole | '8' | 1 | 0 | ' 8\n' | '3' | 0 | 1 |
| no_jpp | '7' | 0 | 1 | ' 7\n' | '3' | 0 | 1 |
| no_rand | '8' | 1 | 0 | ' 8\n' | '3' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0149 (greek): bridge delta (attribute 4) → iota (attribute 9)

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. ⟦person:Lucy⟧ picked ⟦bridge:delta⟧. Kate picked gamma. Luke picked iota.
Which position in the Greek alphabet does Lucy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '4' | 0 | 1 | None | '1' | 0 | 1 |
| alt | '9' | 1 | 0 | None | '8' | 1 | 0 |
| whole | '9' | 1 | 0 | ' 9\n' | '8' | 1 | 0 |
| no_jpp | '9' | 1 | 0 | ' 9\n' | '8' | 1 | 0 |
| no_rand | '9' | 1 | 0 | ' 9\n' | '8' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0154 (elements): bridge oxygen (attribute 8) → helium (attribute 2)

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. ⟦person:Sean⟧ picked ⟦bridge:oxygen⟧. Max picked helium. The locker of oxygen is five.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '8' | 0 | 1 | None | '5' | 0 | 1 |
| alt | '2' | 1 | 0 | None | '3' | 1 | 0 |
| whole | '2' | 1 | 0 | ' 2\n' | '5' | 0 | 1 |
| no_jpp | '2' | 1 | 0 | ' 2\n' | '5' | 0 | 1 |
| no_rand | '2' | 1 | 0 | ' 2\n' | '5' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0181 (elements): bridge helium (attribute 2) → nitrogen (attribute 7)

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. ⟦person:Adam⟧ picked ⟦bridge:helium⟧.
What is the atomic number of Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '2' | 0 | 1 | None | '3' | 0 | 1 |
| alt | '7' | 1 | 0 | None | '9' | 1 | 0 |
| whole | '7' | 1 | 0 | ' 7\n' | '9' | 1 | 0 |
| no_jpp | '2' | 0 | 1 | ' 2\n' | '9' | 1 | 0 |
| no_rand | '7' | 1 | 0 | ' 7\n' | '9' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0184 (elements): bridge helium (attribute 2) → hydrogen (attribute 1)

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. ⟦person:Victor⟧ picked ⟦bridge:helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '2' | 0 | 1 | None | '9' | 0 | 1 |
| alt | '1' | 1 | 0 | None | '5' | 1 | 0 |
| whole | '1' | 1 | 0 | ' 1\n' | '5' | 1 | 0 |
| no_jpp | '2' | 0 | 1 | ' 2\n' | '2' | 0 | 0 |
| no_rand | '1' | 1 | 0 | ' 1\n' | '2' | 0 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0193 (elements): bridge hydrogen (attribute 1) → helium (attribute 2)

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. ⟦person:Victor⟧ picked ⟦bridge:hydrogen⟧. The locker of hydrogen is eight.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '1' | 0 | 1 | None | '8' | 0 | 1 |
| alt | '2' | 1 | 0 | None | '3' | 1 | 0 |
| whole | '2' | 1 | 0 | ' 2\n' | '3' | 1 | 0 |
| no_jpp | '2' | 1 | 0 | ' 2\n' | '3' | 1 | 0 |
| no_rand | '2' | 1 | 0 | ' 2\n' | '8' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0290 (greek): bridge epsilon (attribute 5) → iota (attribute 9)

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. ⟦person:Amy⟧ picked ⟦bridge:epsilon⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '5' | 0 | 1 | None | '4' | 0 | 1 |
| alt | '9' | 1 | 0 | None | '8' | 1 | 0 |
| whole | '9' | 1 | 0 | ' 9\n' | '8' | 1 | 0 |
| no_jpp | '5' | 0 | 1 | ' 5\n' | '4' | 0 | 1 |
| no_rand | '9' | 1 | 0 | ' 9\n' | '4' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 12 | 0.000 | 0.000 | 0.000 | − | − | − |
| 14 | 0.000 | 0.000 | 0.000 | − | − | − |
| 16 | 0.000 | 0.000 | 0.000 | − | − | − |
| 18 | 0.000 | 0.000 | 0.000 | − | − | − |
| 20 | 0.000 | 0.000 | 0.000 | − | − | − |
| 22 | 0.000 | 0.000 | 0.000 | − | − | − |
| 24 | 0.000 | 0.000 | 0.000 | − | − | − |
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 31 | 0.000 | 0.000 | 0.000 | − | − | − |

## muse30_x48_2a (design A, the bridge token): 10 random items of 200 (seed 0)

### P2-L0-0019 (elements): bridge nitrogen (attribute 7) → oxygen (attribute 8)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. ⟦person:Kyle⟧ picked ⟦bridge:nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '7' | 0 | 1 | None | '6' | 0 | 1 |
| alt | '8' | 1 | 0 | None | '4' | 1 | 0 |
| whole | '8' | 1 | 0 | ' 8' | '6' | 0 | 1 |
| no_jpp | '7' | 0 | 1 | ' 7' | '6' | 0 | 1 |
| no_rand | '8' | 1 | 0 | ' 8' | '6' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0091 (elements): bridge oxygen (attribute 8) → hydrogen (attribute 1)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. ⟦person:Clara⟧ picked ⟦bridge:oxygen⟧.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '8' | 0 | 1 | None | '7' | 0 | 1 |
| alt | '1' | 1 | 0 | None | '8' | 1 | 0 |
| whole | '8' | 0 | 1 | ' 8' | '8' | 1 | 0 |
| no_jpp | '8' | 0 | 1 | ' 8' | '8' | 1 | 0 |
| no_rand | '8' | 0 | 1 | ' 8' | '8' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0106 (elements): bridge lithium (attribute 3) → helium (attribute 2)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. ⟦person:Paul⟧ picked ⟦bridge:lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '3' | 0 | 1 | None | '6' | 0 | 1 |
| alt | '2' | 1 | 0 | None | '9' | 1 | 0 |
| whole | '3' | 0 | 1 | ' 3' | '6' | 0 | 1 |
| no_jpp | '3' | 0 | 1 | ' 3' | '6' | 0 | 1 |
| no_rand | '3' | 0 | 1 | ' 3' | '6' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0141 (animals): bridge bee (attribute 6) → elephant (attribute 4)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. ⟦person:Dan⟧ picked the ⟦bridge:bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '6' | 0 | 1 | None | '4' | 0 | 1 |
| alt | '4' | 1 | 0 | None | '1' | 1 | 0 |
| whole | '4' | 1 | 0 | ' 4' | '4' | 0 | 1 |
| no_jpp | '6' | 0 | 1 | ' 6' | '4' | 0 | 1 |
| no_rand | '4' | 1 | 0 | ' 4' | '4' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.049 | 0.565 | 0.516 | 1.00 | 0.79 | 0.87 |
| 28 | -0.134 | 0.478 | 0.611 | 0.98 | 0.67 | 0.73 |
| 30 | -0.131 | 0.437 | 0.568 | 0.96 | 0.61 | 0.80 |
| 32 | -0.184 | 0.504 | 0.687 | 1.00 | 0.72 | 0.88 |
| 34 | -0.130 | 0.572 | 0.702 | 1.00 | 0.51 | 0.89 |
| 36 | -0.132 | 0.635 | 0.767 | 1.00 | 0.42 | 0.92 |
| 38 | -0.068 | 0.572 | 0.640 | 1.00 | 0.36 | 0.92 |
| 40 | 0.068 | 0.559 | 0.491 | 0.99 | 0.36 | 0.94 |
| 42 | -0.072 | 0.640 | 0.711 | 1.00 | 0.36 | 0.96 |
| 44 | -0.053 | 0.593 | 0.646 | 0.99 | 0.34 | 0.93 |
| 46 | -0.057 | 0.557 | 0.614 | 0.99 | 0.28 | 0.92 |
| 48 | 0.024 | 0.504 | 0.481 | 0.98 | 0.22 | 0.93 |
| 50 | 0.151 | 0.460 | 0.309 | 1.00 | 0.04 | 0.91 |
| 51 | 0.189 | 0.442 | 0.253 | 1.00 | 0.00 | 0.98 |

### P2-L0-0148 (elements): bridge nitrogen (attribute 7) → carbon (attribute 6)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked carbon. ⟦person:Carl⟧ picked ⟦bridge:nitrogen⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
What is the atomic number of Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '7' | 0 | 1 | None | '3' | 0 | 1 |
| alt | '6' | 1 | 0 | None | '2' | 1 | 0 |
| whole | '6' | 1 | 0 | ' 6' | '3' | 0 | 1 |
| no_jpp | '6' | 1 | 0 | ' 6' | '3' | 0 | 1 |
| no_rand | '6' | 1 | 0 | ' 6' | '3' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0155 (greek): bridge beta (attribute 2) → epsilon (attribute 5)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦person:Maria⟧ picked ⟦bridge:beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which position in the Greek alphabet does Maria's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '2' | 0 | 1 | None | '5' | 0 | 1 |
| alt | '5' | 1 | 0 | None | '1' | 1 | 0 |
| whole | '2' | 0 | 1 | ' 2' | '5' | 0 | 1 |
| no_jpp | '2' | 0 | 1 | ' 2' | '5' | 0 | 1 |
| no_rand | '2' | 0 | 1 | ' 2' | '5' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0175 (elements): bridge lithium (attribute 3) → carbon (attribute 6)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. ⟦person:Mia⟧ picked ⟦bridge:lithium⟧. Liam picked carbon. Adam picked hydrogen. The locker of carbon is one.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '3' | 0 | 1 | None | '9' | 0 | 1 |
| alt | '6' | 1 | 0 | None | '1' | 1 | 0 |
| whole | '6' | 1 | 0 | ' 6' | '9' | 0 | 1 |
| no_jpp | '3' | 0 | 1 | ' 3' | '9' | 0 | 1 |
| no_rand | '6' | 1 | 0 | ' 6' | '9' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0178 (elements): bridge carbon (attribute 6) → oxygen (attribute 8)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. ⟦person:Lily⟧ picked ⟦bridge:carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
What is the atomic number of Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '6' | 0 | 1 | None | '7' | 0 | 1 |
| alt | '8' | 1 | 0 | None | '3' | 1 | 0 |
| whole | '8' | 1 | 0 | ' 8' | '7' | 0 | 1 |
| no_jpp | '6' | 0 | 1 | ' 6' | '7' | 0 | 1 |
| no_rand | '8' | 1 | 0 | ' 8' | '7' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0187 (elements): bridge hydrogen (attribute 1) → helium (attribute 2)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. ⟦person:Nina⟧ picked ⟦bridge:hydrogen⟧. Maria picked helium. The locker of hydrogen is 6. The locker of lithium is 2.
What is the atomic number of Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '1' | 0 | 1 | None | '6' | 0 | 1 |
| alt | '2' | 1 | 0 | None | '1' | 1 | 0 |
| whole | '1' | 0 | 1 | ' 1' | '6' | 0 | 1 |
| no_jpp | '1' | 0 | 1 | ' 1' | '6' | 0 | 1 |
| no_rand | '2' | 1 | 0 | ' 2' | '6' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0284 (greek): bridge delta (attribute 4) → epsilon (attribute 5)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦person:Kyle⟧ picked ⟦bridge:delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '4' | 0 | 1 | None | '7' | 0 | 1 |
| alt | '5' | 1 | 0 | None | '3' | 1 | 0 |
| whole | '4' | 0 | 1 | ' 4' | '7' | 0 | 1 |
| no_jpp | '4' | 0 | 1 | ' 4' | '7' | 0 | 1 |
| no_rand | '4' | 0 | 1 | ' 4' | '7' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 26 | 0.000 | 0.000 | 0.000 | − | − | − |
| 28 | 0.000 | 0.000 | 0.000 | − | − | − |
| 30 | 0.000 | 0.000 | 0.000 | − | − | − |
| 32 | 0.000 | 0.000 | 0.000 | − | − | − |
| 34 | 0.000 | 0.000 | 0.000 | − | − | − |
| 36 | 0.000 | 0.000 | 0.000 | − | − | − |
| 38 | 0.000 | 0.000 | 0.000 | − | − | − |
| 40 | 0.000 | 0.000 | 0.000 | − | − | − |
| 42 | 0.000 | 0.000 | 0.000 | − | − | − |
| 44 | 0.000 | 0.000 | 0.000 | − | − | − |
| 46 | 0.000 | 0.000 | 0.000 | − | − | − |
| 48 | 0.000 | 0.000 | 0.000 | − | − | − |
| 50 | 0.000 | 0.000 | 0.000 | − | − | − |
| 51 | 0.000 | 0.000 | 0.000 | − | − | − |

## qwen35_9b_x48_2b (design B): 10 random items of 200 (seed 0)

### P2-L0-0017 (greek): bridge iota, asked person Leo

**lookup** (PP-L0-0017): O's answer 2

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. ⟦person:Leo⟧ picked ⟦bridge:iota⟧. Eva picked gamma.
Which locker belongs to Leo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | 1 | ' 2\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '2' | 1 | ' 2\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '2' | 1 | ' 2\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '8' | 0 | ' 8\n' |

**recall** (PM-L0-0017): O's answer 9

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of iota is two. The locker of gamma is eight. ⟦person:Leo⟧ picked ⟦bridge:iota⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | 1 | ' 9\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '9' | 1 | ' 9\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '9' | 1 | ' 9\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '5' | 0 | ' 5\n' |

### P2-L0-0096 (animals): bridge bee, asked person Will

**lookup** (PP-L0-0096): O's answer 1

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. ⟦person:Will⟧ picked the ⟦bridge:bee⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | 1 | ' 1\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '1' | 1 | ' 1\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '1' | 1 | ' 1\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '1' | 1 | ' 1\n' |

**recall** (PM-L0-0096): O's answer 6

```
<|im_start|>user
The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. ⟦person:Will⟧ picked the ⟦bridge:bee⟧.
How many legs does Will's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '6' | 1 | ' 6\n' |

### P2-L0-0110 (greek): bridge iota, asked person Anna

**lookup** (PP-L0-0110): O's answer 2

```
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. ⟦person:Anna⟧ picked ⟦bridge:iota⟧.
Which locker belongs to Anna's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | 1 | ' 2\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '2' | 1 | ' 2\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '2' | 1 | ' 2\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '6' | 0 | ' 6\n' |

**recall** (PM-L0-0110): O's answer 9

```
<|im_start|>user
Ruby picked epsilon. The locker of epsilon is seven. Emma picked alpha. The locker of alpha is nine. The locker of iota is two. ⟦person:Anna⟧ picked ⟦bridge:iota⟧.
Which position in the Greek alphabet does Anna's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | 1 | ' 9\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '9' | 1 | ' 9\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '9' | 1 | ' 9\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '3' | 0 | ' 3\n' |

### P2-L0-0142 (elements): bridge nitrogen, asked person Owen

**lookup** (PP-L0-0142): O's answer 3

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. ⟦person:Owen⟧ picked ⟦bridge:nitrogen⟧. The locker of nitrogen is three.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '5' | 0 | ' 5\n' |

**recall** (PM-L0-0142): O's answer 7

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. ⟦person:Owen⟧ picked ⟦bridge:nitrogen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | 1 | ' 7\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '7' | 1 | ' 7\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '7' | 1 | ' 7\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 1 | ' 7\n' |

### P2-L0-0149 (greek): bridge delta, asked person Lucy

**lookup** (PP-L0-0149): O's answer 1

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. ⟦person:Lucy⟧ picked ⟦bridge:delta⟧. Kate picked gamma. Luke picked iota.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | 1 | ' 1\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '1' | 1 | ' 1\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '1' | 1 | ' 1\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '8' | 0 | ' 8\n' |

**recall** (PM-L0-0149): O's answer 4

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. ⟦person:Lucy⟧ picked ⟦bridge:delta⟧. Kate picked gamma. Luke picked iota.
Which position in the Greek alphabet does Lucy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | 1 | ' 4\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '4' | 1 | ' 4\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '4' | 1 | ' 4\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '4' | 1 | ' 4\n' |

### P2-L0-0154 (elements): bridge oxygen, asked person Sean

**lookup** (PP-L0-0154): O's answer 5

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. ⟦person:Sean⟧ picked ⟦bridge:oxygen⟧. Max picked helium. The locker of oxygen is five.
Which locker belongs to Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | 1 | ' 5\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '5' | 1 | ' 5\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '5' | 1 | ' 5\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '4' | 0 | ' 4\n' |

**recall** (PM-L0-0154): O's answer 8

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. ⟦person:Sean⟧ picked ⟦bridge:oxygen⟧. Max picked helium. The locker of oxygen is five.
What is the atomic number of Sean's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | 1 | ' 8\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '8' | 1 | ' 8\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '8' | 1 | ' 8\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '8' | 1 | ' 8\n' |

### P2-L0-0181 (elements): bridge helium, asked person Adam

**lookup** (PP-L0-0181): O's answer 3

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. ⟦person:Adam⟧ picked ⟦bridge:helium⟧.
Which locker belongs to Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '1' | 0 | ' 1\n' |

**recall** (PM-L0-0181): O's answer 2

```
<|im_start|>user
The locker of hydrogen is 5. Maria picked hydrogen. Dan picked nitrogen. The locker of helium is 3. The locker of nitrogen is 9. ⟦person:Adam⟧ picked ⟦bridge:helium⟧.
What is the atomic number of Adam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | 1 | ' 2\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '2' | 1 | ' 2\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '2' | 1 | ' 2\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '2' | 1 | ' 2\n' |

### P2-L0-0184 (elements): bridge helium, asked person Victor

**lookup** (PP-L0-0184): O's answer 9

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. ⟦person:Victor⟧ picked ⟦bridge:helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | 1 | ' 9\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '9' | 1 | ' 9\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '9' | 1 | ' 9\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '5' | 0 | ' 5\n' |

**recall** (PM-L0-0184): O's answer 2

```
<|im_start|>user
The locker of helium is 9. Peter picked nitrogen. The locker of nitrogen is 3. ⟦person:Victor⟧ picked ⟦bridge:helium⟧. The locker of hydrogen is 5. Luke picked hydrogen.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | 1 | ' 2\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '2' | 1 | ' 2\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '2' | 1 | ' 2\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '2' | 1 | ' 2\n' |

### P2-L0-0193 (elements): bridge hydrogen, asked person Victor

**lookup** (PP-L0-0193): O's answer 8

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. ⟦person:Victor⟧ picked ⟦bridge:hydrogen⟧. The locker of hydrogen is eight.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | 1 | ' 8\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '8' | 1 | ' 8\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '8' | 1 | ' 8\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 0 | ' 7\n' |

**recall** (PM-L0-0193): O's answer 1

```
<|im_start|>user
The locker of helium is three. Ivan picked oxygen. The locker of oxygen is nine. Hugo picked helium. ⟦person:Victor⟧ picked ⟦bridge:hydrogen⟧. The locker of hydrogen is eight.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | 1 | ' 1\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '1' | 1 | ' 1\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '1' | 1 | ' 1\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '2' | 0 | ' 2\n' |

### P2-L0-0290 (greek): bridge epsilon, asked person Amy

**lookup** (PP-L0-0290): O's answer 4

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. ⟦person:Amy⟧ picked ⟦bridge:epsilon⟧. Noah picked beta.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | 1 | ' 4\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '4' | 1 | ' 4\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '4' | 1 | ' 4\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '9' | 0 | ' 9\n' |

**recall** (PM-L0-0290): O's answer 5

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of epsilon is 4. The locker of iota is 8. ⟦person:Amy⟧ picked ⟦bridge:epsilon⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | 1 | ' 5\n' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '5' | 1 | ' 5\n' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '5' | 1 | ' 5\n' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '5' | 1 | ' 5\n' |

## muse30_x48_2b (design B): 10 random items of 200 (seed 0)

### P2-L0-0019 (elements): bridge nitrogen, asked person Kyle

**lookup** (PP-L0-0019): O's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. ⟦person:Kyle⟧ picked ⟦bridge:nitrogen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '4' | 0 | ' 4' |

**recall** (PM-L0-0019): O's answer 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. ⟦person:Kyle⟧ picked ⟦bridge:nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | 1 | ' 7' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '7' | 1 | ' 7' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '7' | 1 | ' 7' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 1 | ' 7' |

### P2-L0-0091 (elements): bridge oxygen, asked person Clara

**lookup** (PP-L0-0091): O's answer 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. ⟦person:Clara⟧ picked ⟦bridge:oxygen⟧.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | 1 | ' 7' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '7' | 1 | ' 7' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '7' | 1 | ' 7' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 1 | ' 7' |

**recall** (PM-L0-0091): O's answer 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. ⟦person:Clara⟧ picked ⟦bridge:oxygen⟧.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | 1 | ' 8' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '8' | 1 | ' 8' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '8' | 1 | ' 8' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '8' | 1 | ' 8' |

### P2-L0-0106 (elements): bridge lithium, asked person Paul

**lookup** (PP-L0-0106): O's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. ⟦person:Paul⟧ picked ⟦bridge:lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '6' | 1 | ' 6' |

**recall** (PM-L0-0106): O's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. ⟦person:Paul⟧ picked ⟦bridge:lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '3' | 1 | ' 3' |

### P2-L0-0141 (animals): bridge bee, asked person Dan

**lookup** (PP-L0-0141): O's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. ⟦person:Dan⟧ picked the ⟦bridge:bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | 1 | ' 4' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '4' | 1 | ' 4' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '4' | 1 | ' 4' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '4' | 1 | ' 4' |

**recall** (PM-L0-0141): O's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. ⟦person:Dan⟧ picked the ⟦bridge:bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '2' | 0 | ' 2' |

### P2-L0-0148 (elements): bridge nitrogen, asked person Carl

**lookup** (PP-L0-0148): O's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked carbon. ⟦person:Carl⟧ picked ⟦bridge:nitrogen⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '3' | 1 | ' 3' |

**recall** (PM-L0-0148): O's answer 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked carbon. ⟦person:Carl⟧ picked ⟦bridge:nitrogen⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
What is the atomic number of Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | 1 | ' 7' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '7' | 1 | ' 7' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '7' | 1 | ' 7' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 1 | ' 7' |

### P2-L0-0155 (greek): bridge beta, asked person Maria

**lookup** (PP-L0-0155): O's answer 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦person:Maria⟧ picked ⟦bridge:beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | 1 | ' 5' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '5' | 1 | ' 5' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '5' | 1 | ' 5' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 0 | ' 7' |

**recall** (PM-L0-0155): O's answer 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦person:Maria⟧ picked ⟦bridge:beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which position in the Greek alphabet does Maria's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | 1 | ' 2' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '2' | 1 | ' 2' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '2' | 1 | ' 2' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '2' | 1 | ' 2' |

### P2-L0-0175 (elements): bridge lithium, asked person Mia

**lookup** (PP-L0-0175): O's answer 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. ⟦person:Mia⟧ picked ⟦bridge:lithium⟧. Liam picked carbon. Adam picked hydrogen. The locker of carbon is one.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | 1 | ' 9' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '9' | 1 | ' 9' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '9' | 1 | ' 9' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '5' | 0 | ' 5' |

**recall** (PM-L0-0175): O's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. ⟦person:Mia⟧ picked ⟦bridge:lithium⟧. Liam picked carbon. Adam picked hydrogen. The locker of carbon is one.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '3' | 1 | ' 3' |

### P2-L0-0178 (elements): bridge carbon, asked person Lily

**lookup** (PP-L0-0178): O's answer 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. ⟦person:Lily⟧ picked ⟦bridge:carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | 1 | ' 7' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '7' | 1 | ' 7' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '7' | 1 | ' 7' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '4' | 0 | ' 4' |

**recall** (PM-L0-0178): O's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. ⟦person:Lily⟧ picked ⟦bridge:carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
What is the atomic number of Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '6' | 1 | ' 6' |

### P2-L0-0187 (elements): bridge hydrogen, asked person Nina

**lookup** (PP-L0-0187): O's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. ⟦person:Nina⟧ picked ⟦bridge:hydrogen⟧. Maria picked helium. The locker of hydrogen is 6. The locker of lithium is 2.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '1' | 0 | ' 1' |

**recall** (PM-L0-0187): O's answer 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. ⟦person:Nina⟧ picked ⟦bridge:hydrogen⟧. Maria picked helium. The locker of hydrogen is 6. The locker of lithium is 2.
What is the atomic number of Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | 1 | ' 1' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '1' | 1 | ' 1' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '1' | 1 | ' 1' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '1' | 1 | ' 1' |

### P2-L0-0284 (greek): bridge delta, asked person Kyle

**lookup** (PP-L0-0284): O's answer 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦person:Kyle⟧ picked ⟦bridge:delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | 1 | ' 7' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '7' | 1 | ' 7' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '7' | 1 | ' 7' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '3' | 0 | ' 3' |

**recall** (PM-L0-0284): O's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦person:Kyle⟧ picked ⟦bridge:delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | 1 | ' 4' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '4' | 1 | ' 4' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '4' | 1 | ' 4' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 0 | ' 7' |

