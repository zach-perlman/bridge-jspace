# 48.2 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge token, ⟦person:…⟧ the asked person's token(s). UNVERIFIED.

## x48_2a_27b (design A, the bridge token): 10 random items of 200 (seed 0)

### P2-L0-0010 (elements): bridge oxygen (attribute 8) → carbon (attribute 6)

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. ⟦person:Grace⟧ picked ⟦bridge:oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '8' | 0 | 1 | None | '3' | 0 | 1 |
| alt | '6' | 1 | 0 | None | '7' | 1 | 0 |
| whole | '6' | 1 | 0 | ' 6' | '3' | 0 | 1 |
| no_jpp | '8' | 0 | 1 | ' 8' | '3' | 0 | 1 |
| no_rand | '6' | 1 | 0 | ' 6' | '3' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
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
| 52 | 0.000 | 0.000 | 0.000 | − | − | − |
| 54 | 0.000 | 0.000 | 0.000 | − | − | − |
| 56 | 0.000 | 0.000 | 0.000 | − | − | − |
| 58 | 0.000 | 0.000 | 0.000 | − | − | − |
| 60 | 0.000 | 0.000 | 0.000 | − | − | − |
| 62 | 0.000 | 0.000 | 0.000 | − | − | − |
| 63 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0069 (animals): bridge sheep (attribute 4) → butterfly (attribute 6)

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. ⟦person:Ivy⟧ picked the ⟦bridge:sheep⟧. Ella picked the butterfly.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '4' | 0 | 1 | None | '3' | 0 | 1 |
| alt | '6' | 1 | 0 | None | '7' | 1 | 0 |
| whole | '6' | 1 | 0 | ' 6' | '7' | 1 | 0 |
| no_jpp | '4' | 0 | 1 | ' 4' | '7' | 1 | 0 |
| no_rand | '6' | 1 | 0 | ' 6' | '7' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 32 | -1.058 | 0.176 | 1.234 | 1.00 | 0.74 | 0.79 |
| 34 | -0.925 | 0.336 | 1.261 | 1.00 | 0.64 | 0.78 |
| 36 | -1.130 | 0.318 | 1.448 | 1.00 | 0.72 | 0.81 |
| 38 | -1.108 | 0.285 | 1.393 | 1.00 | 0.70 | 0.82 |
| 40 | -1.005 | 0.301 | 1.306 | 1.00 | 0.71 | 0.85 |
| 42 | -1.024 | 0.097 | 1.121 | 1.00 | 0.73 | 0.90 |
| 44 | -1.149 | 0.203 | 1.352 | 1.00 | 0.59 | 0.91 |
| 46 | -1.179 | 0.061 | 1.239 | 1.00 | 0.68 | 0.93 |
| 48 | -1.214 | 0.186 | 1.401 | 1.00 | 0.67 | 0.90 |
| 50 | -0.901 | 0.320 | 1.221 | 1.00 | 0.57 | 0.91 |
| 52 | -0.719 | 0.312 | 1.031 | 1.00 | 0.59 | 0.98 |
| 54 | -0.688 | 0.079 | 0.767 | 1.00 | 0.57 | 0.98 |
| 56 | -0.625 | 0.155 | 0.779 | 1.00 | 0.59 | 0.98 |
| 58 | -0.614 | 0.135 | 0.749 | 1.00 | 0.61 | 0.98 |
| 60 | -0.566 | 0.176 | 0.741 | 1.00 | 0.70 | 0.97 |
| 62 | -0.558 | 0.382 | 0.940 | 1.00 | 0.76 | 0.97 |
| 63 | -0.455 | 0.443 | 0.898 | 1.00 | 0.74 | 0.96 |

### P2-L0-0080 (greek): bridge eta (attribute 7) → delta (attribute 4)

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. ⟦person:Ivy⟧ picked ⟦bridge:eta⟧. The locker of delta is 8. The locker of eta is 6. The locker of epsilon is 1.
Which position in the Greek alphabet does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '7' | 0 | 1 | None | '6' | 0 | 1 |
| alt | '4' | 1 | 0 | None | '8' | 1 | 0 |
| whole | '4' | 1 | 0 | ' 4' | '6' | 0 | 1 |
| no_jpp | '7' | 0 | 1 | ' 7' | '6' | 0 | 1 |
| no_rand | '4' | 1 | 0 | ' 4' | '6' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
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
| 52 | 0.000 | 0.000 | 0.000 | − | − | − |
| 54 | 0.000 | 0.000 | 0.000 | − | − | − |
| 56 | 0.000 | 0.000 | 0.000 | − | − | − |
| 58 | 0.000 | 0.000 | 0.000 | − | − | − |
| 60 | 0.000 | 0.000 | 0.000 | − | − | − |
| 62 | 0.000 | 0.000 | 0.000 | − | − | − |
| 63 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0102 (animals): bridge butterfly (attribute 6) → goose (attribute 2)

```
<|im_start|>user
Oscar picked the beetle. ⟦person:Rose⟧ picked the ⟦bridge:butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '6' | 0 | 1 | None | '5' | 0 | 1 |
| alt | '2' | 1 | 0 | None | '8' | 1 | 0 |
| whole | '2' | 1 | 0 | ' 2' | '5' | 0 | 1 |
| no_jpp | '6' | 0 | 1 | ' 6' | '5' | 0 | 1 |
| no_rand | '2' | 1 | 0 | ' 2' | '5' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 32 | -0.539 | 0.791 | 1.330 | 1.00 | 0.59 | 0.76 |
| 34 | -0.638 | 0.857 | 1.495 | 1.00 | 0.60 | 0.65 |
| 36 | -0.793 | 0.819 | 1.612 | 1.00 | 0.62 | 0.65 |
| 38 | -0.794 | 0.709 | 1.503 | 1.00 | 0.64 | 0.65 |
| 40 | -0.712 | 0.717 | 1.429 | 1.00 | 0.63 | 0.69 |
| 42 | -0.558 | 0.768 | 1.326 | 1.00 | 0.55 | 0.73 |
| 44 | -0.593 | 0.796 | 1.389 | 1.00 | 0.54 | 0.73 |
| 46 | -0.419 | 0.699 | 1.118 | 1.00 | 0.44 | 0.70 |
| 48 | -0.438 | 0.674 | 1.112 | 1.00 | 0.44 | 0.71 |
| 50 | -0.358 | 0.387 | 0.745 | 1.00 | 0.44 | 0.88 |
| 52 | -0.505 | 0.772 | 1.277 | 1.00 | 0.17 | 0.89 |
| 54 | -0.417 | 0.440 | 0.857 | 1.00 | 0.20 | 0.91 |
| 56 | -0.443 | 0.503 | 0.946 | 1.00 | 0.15 | 0.90 |
| 58 | -0.476 | 0.531 | 1.007 | 1.00 | 0.18 | 0.89 |
| 60 | -0.465 | 0.523 | 0.988 | 1.00 | 0.19 | 0.86 |
| 62 | -0.525 | 0.520 | 1.045 | 1.00 | 0.23 | 0.91 |
| 63 | -0.484 | 0.554 | 1.037 | 1.00 | 0.26 | 0.93 |

### P2-L0-0107 (greek): bridge iota (attribute 9) → gamma (attribute 3)

```
<|im_start|>user
The locker of gamma is nine. Eva picked epsilon. ⟦person:David⟧ picked ⟦bridge:iota⟧. The locker of epsilon is one. The locker of iota is three. Eve picked gamma.
Which position in the Greek alphabet does David's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '9' | 0 | 1 | None | '3' | 0 | 1 |
| alt | '3' | 1 | 0 | None | '9' | 1 | 0 |
| whole | '9' | 0 | 1 | ' 9' | '9' | 1 | 0 |
| no_jpp | '9' | 0 | 1 | ' 9' | '3' | 0 | 1 |
| no_rand | '3' | 1 | 0 | ' 3' | '9' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
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
| 52 | 0.000 | 0.000 | 0.000 | − | − | − |
| 54 | 0.000 | 0.000 | 0.000 | − | − | − |
| 56 | 0.000 | 0.000 | 0.000 | − | − | − |
| 58 | 0.000 | 0.000 | 0.000 | − | − | − |
| 60 | 0.000 | 0.000 | 0.000 | − | − | − |
| 62 | 0.000 | 0.000 | 0.000 | − | − | − |
| 63 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0111 (animals): bridge chicken (attribute 2) → rabbit (attribute 4)

```
<|im_start|>user
⟦person:I⟧⟦person:vy⟧ picked the ⟦bridge:chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '2' | 0 | 1 | None | '8' | 0 | 1 |
| alt | '4' | 1 | 0 | None | '7' | 1 | 0 |
| whole | '4' | 1 | 0 | ' 4' | '8' | 0 | 1 |
| no_jpp | '2' | 0 | 1 | ' 2' | '8' | 0 | 1 |
| no_rand | '4' | 1 | 0 | ' 4' | '8' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 32 | -0.246 | 0.338 | 0.584 | 1.00 | 0.48 | 0.61 |
| 34 | -0.272 | 0.438 | 0.710 | 1.00 | 0.34 | 0.56 |
| 36 | -0.242 | 0.663 | 0.905 | 1.00 | 0.38 | 0.58 |
| 38 | -0.305 | 0.590 | 0.895 | 1.00 | 0.38 | 0.60 |
| 40 | -0.336 | 0.480 | 0.817 | 1.00 | 0.24 | 0.63 |
| 42 | -0.300 | 0.516 | 0.815 | 1.00 | 0.22 | 0.69 |
| 44 | -0.274 | 0.513 | 0.787 | 1.00 | 0.22 | 0.65 |
| 46 | -0.333 | 0.444 | 0.778 | 1.00 | 0.24 | 0.67 |
| 48 | -0.254 | 0.501 | 0.755 | 1.00 | 0.25 | 0.68 |
| 50 | -0.021 | 0.349 | 0.370 | 1.00 | 0.16 | 0.55 |
| 52 | -0.245 | 0.460 | 0.705 | 1.00 | 0.01 | 0.76 |
| 54 | -0.005 | 0.671 | 0.676 | 1.00 | 0.03 | 0.77 |
| 56 | -0.115 | 0.596 | 0.710 | 1.00 | 0.02 | 0.78 |
| 58 | -0.062 | 0.592 | 0.654 | 1.00 | 0.01 | 0.74 |
| 60 | 0.004 | 0.542 | 0.537 | 1.00 | 0.01 | 0.73 |
| 62 | 0.062 | 0.592 | 0.530 | 1.00 | 0.00 | 0.74 |
| 63 | 0.157 | 0.624 | 0.467 | 1.00 | 0.00 | 0.73 |

### P2-L0-0128 (greek): bridge eta (attribute 7) → theta (attribute 8)

```
<|im_start|>user
The locker of theta is 7. Adam picked beta. ⟦person:Henry⟧ picked ⟦bridge:eta⟧. Liam picked theta. The locker of beta is 9. The locker of eta is 2.
Which position in the Greek alphabet does Henry's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '7' | 0 | 1 | None | '2' | 0 | 1 |
| alt | '8' | 1 | 0 | None | '7' | 1 | 0 |
| whole | '5' | 0 | 0 | ' 5' | '7' | 1 | 0 |
| no_jpp | '5' | 0 | 0 | ' 5' | '7' | 1 | 0 |
| no_rand | '5' | 0 | 0 | ' 5' | '7' | 1 | 0 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
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
| 52 | 0.000 | 0.000 | 0.000 | − | − | − |
| 54 | 0.000 | 0.000 | 0.000 | − | − | − |
| 56 | 0.000 | 0.000 | 0.000 | − | − | − |
| 58 | 0.000 | 0.000 | 0.000 | − | − | − |
| 60 | 0.000 | 0.000 | 0.000 | − | − | − |
| 62 | 0.000 | 0.000 | 0.000 | − | − | − |
| 63 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0130 (elements): bridge carbon (attribute 6) → lithium (attribute 3)

```
<|im_start|>user
⟦person:Alice⟧ picked ⟦bridge:carbon⟧. The locker of hydrogen is 9. Frank picked lithium. The locker of carbon is 4. The locker of lithium is 7. Dan picked hydrogen.
What is the atomic number of Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '6' | 0 | 1 | None | '4' | 0 | 1 |
| alt | '3' | 1 | 0 | None | '7' | 1 | 0 |
| whole | '3' | 1 | 0 | ' 3' | '4' | 0 | 1 |
| no_jpp | '6' | 0 | 1 | ' 6' | '4' | 0 | 1 |
| no_rand | '3' | 1 | 0 | ' 3' | '4' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
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
| 52 | 0.000 | 0.000 | 0.000 | − | − | − |
| 54 | 0.000 | 0.000 | 0.000 | − | − | − |
| 56 | 0.000 | 0.000 | 0.000 | − | − | − |
| 58 | 0.000 | 0.000 | 0.000 | − | − | − |
| 60 | 0.000 | 0.000 | 0.000 | − | − | − |
| 62 | 0.000 | 0.000 | 0.000 | − | − | − |
| 63 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0136 (elements): bridge hydrogen (attribute 1) → oxygen (attribute 8)

```
<|im_start|>user
⟦person:M⟧⟦person:ia⟧ picked ⟦bridge:hydrogen⟧. The locker of hydrogen is three. The locker of oxygen is six. Amy picked oxygen. The locker of nitrogen is eight. Jack picked nitrogen.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '1' | 0 | 1 | None | '3' | 0 | 1 |
| alt | '8' | 1 | 0 | None | '6' | 1 | 0 |
| whole | '8' | 1 | 0 | ' 8' | '3' | 0 | 1 |
| no_jpp | '1' | 0 | 1 | ' 1' | '3' | 0 | 1 |
| no_rand | '8' | 1 | 0 | ' 8' | '3' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
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
| 52 | 0.000 | 0.000 | 0.000 | − | − | − |
| 54 | 0.000 | 0.000 | 0.000 | − | − | − |
| 56 | 0.000 | 0.000 | 0.000 | − | − | − |
| 58 | 0.000 | 0.000 | 0.000 | − | − | − |
| 60 | 0.000 | 0.000 | 0.000 | − | − | − |
| 62 | 0.000 | 0.000 | 0.000 | − | − | − |
| 63 | 0.000 | 0.000 | 0.000 | − | − | − |

### P2-L0-0204 (animals): bridge tick (attribute 8) → horse (attribute 4)

```
<|im_start|>user
⟦person:Maria⟧ picked the ⟦bridge:tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

Reads (top token; switched = S's answer, right = O's):

| arm | recall top | switched | right | greedy | lookup top | switched | right |
|---|---|---|---|---|---|---|---|
| none | '8' | 0 | 1 | None | '3' | 0 | 1 |
| alt | '4' | 1 | 0 | None | '8' | 1 | 0 |
| whole | '6' | 0 | 0 | ' 6' | '3' | 0 | 1 |
| no_jpp | '6' | 0 | 0 | ' 6' | '3' | 0 | 1 |
| no_rand | '6' | 0 | 0 | ' 6' | '3' | 0 | 1 |

Probe at the bridge token, m = score(changed class) − score(original class), and the fraction of the way (clipped; − when the unedited gap is not positive):

| layer | m(O) | m(S) | gap | whole | no_jpp | no_rand |
|---|---|---|---|---|---|---|
| 32 | 0.101 | 0.963 | 0.862 | 1.00 | 0.37 | 0.78 |
| 34 | 0.058 | 1.047 | 0.989 | 1.00 | 0.35 | 0.60 |
| 36 | -0.007 | 1.119 | 1.126 | 1.00 | 0.34 | 0.66 |
| 38 | -0.027 | 1.138 | 1.165 | 1.00 | 0.35 | 0.70 |
| 40 | -0.107 | 1.163 | 1.270 | 1.00 | 0.34 | 0.75 |
| 42 | -0.022 | 1.003 | 1.025 | 1.00 | 0.26 | 0.70 |
| 44 | 0.000 | 1.112 | 1.112 | 1.00 | 0.25 | 0.78 |
| 46 | 0.020 | 1.001 | 0.981 | 1.00 | 0.29 | 0.82 |
| 48 | 0.034 | 0.895 | 0.861 | 1.00 | 0.25 | 0.86 |
| 50 | -0.168 | 0.883 | 1.052 | 1.00 | 0.38 | 0.91 |
| 52 | -0.037 | 0.792 | 0.829 | 1.00 | 0.34 | 0.89 |
| 54 | 0.064 | 0.786 | 0.722 | 1.00 | 0.32 | 0.90 |
| 56 | 0.042 | 0.783 | 0.741 | 1.00 | 0.24 | 0.95 |
| 58 | 0.047 | 0.750 | 0.703 | 1.00 | 0.20 | 0.95 |
| 60 | 0.047 | 0.736 | 0.689 | 1.00 | 0.17 | 0.94 |
| 62 | 0.019 | 0.804 | 0.786 | 1.00 | 0.23 | 0.93 |
| 63 | 0.033 | 0.801 | 0.768 | 1.00 | 0.23 | 0.95 |

## x48_2b_27b (design B): 10 random items of 200 (seed 0)

### P2-L0-0010 (elements): bridge oxygen, asked person Grace

**lookup** (PP-L0-0010): O's answer 3

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. ⟦person:Grace⟧ picked ⟦bridge:oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '3' | 1 | ' 3' |

**recall** (PM-L0-0010): O's answer 8

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. ⟦person:Grace⟧ picked ⟦bridge:oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | 1 | ' 8' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '8' | 1 | ' 8' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '8' | 1 | ' 8' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '8' | 1 | ' 8' |

### P2-L0-0069 (animals): bridge sheep, asked person Ivy

**lookup** (PP-L0-0069): O's answer 3

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. ⟦person:Ivy⟧ picked the ⟦bridge:sheep⟧. Ella picked the butterfly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 0 | ' 7' |

**recall** (PM-L0-0069): O's answer 4

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. ⟦person:Ivy⟧ picked the ⟦bridge:sheep⟧. Ella picked the butterfly.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | 1 | ' 4' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '4' | 1 | ' 4' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '4' | 1 | ' 4' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '4' | 1 | ' 4' |

### P2-L0-0080 (greek): bridge eta, asked person Ivy

**lookup** (PP-L0-0080): O's answer 6

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. ⟦person:Ivy⟧ picked ⟦bridge:eta⟧. The locker of delta is 8. The locker of eta is 6. The locker of epsilon is 1.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '6' | 1 | ' 6' |

**recall** (PM-L0-0080): O's answer 7

```
<|im_start|>user
Laura picked epsilon. Anna picked delta. ⟦person:Ivy⟧ picked ⟦bridge:eta⟧. The locker of delta is 8. The locker of eta is 6. The locker of epsilon is 1.
Which position in the Greek alphabet does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | 1 | ' 7' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '7' | 1 | ' 7' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '7' | 1 | ' 7' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '5' | 0 | ' 5' |

### P2-L0-0102 (animals): bridge butterfly, asked person Rose

**lookup** (PP-L0-0102): O's answer 5

```
<|im_start|>user
Oscar picked the beetle. ⟦person:Rose⟧ picked the ⟦bridge:butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | 1 | ' 5' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '5' | 1 | ' 5' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '5' | 1 | ' 5' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '5' | 1 | ' 5' |

**recall** (PM-L0-0102): O's answer 6

```
<|im_start|>user
Oscar picked the beetle. ⟦person:Rose⟧ picked the ⟦bridge:butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
How many legs does Rose's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '6' | 1 | ' 6' |

### P2-L0-0107 (greek): bridge iota, asked person David

**lookup** (PP-L0-0107): O's answer 3

```
<|im_start|>user
The locker of gamma is nine. Eva picked epsilon. ⟦person:David⟧ picked ⟦bridge:iota⟧. The locker of epsilon is one. The locker of iota is three. Eve picked gamma.
Which locker belongs to David's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '9' | 0 | ' 9' |

**recall** (PM-L0-0107): O's answer 9

```
<|im_start|>user
The locker of gamma is nine. Eva picked epsilon. ⟦person:David⟧ picked ⟦bridge:iota⟧. The locker of epsilon is one. The locker of iota is three. Eve picked gamma.
Which position in the Greek alphabet does David's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | 1 | ' 9' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '9' | 1 | ' 9' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '9' | 1 | ' 9' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '8' | 0 | ' 8' |

### P2-L0-0111 (animals): bridge chicken, asked person Ivy

**lookup** (PP-L0-0111): O's answer 8

```
<|im_start|>user
⟦person:I⟧⟦person:vy⟧ picked the ⟦bridge:chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | 1 | ' 8' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '8' | 1 | ' 8' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '8' | 1 | ' 8' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '4' | 0 | ' 4' |

**recall** (PM-L0-0111): O's answer 2

```
<|im_start|>user
⟦person:I⟧⟦person:vy⟧ picked the ⟦bridge:chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
How many legs does Ivy's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | 1 | ' 2' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '2' | 1 | ' 2' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '2' | 1 | ' 2' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '0' | 0 | ' 0' |

### P2-L0-0128 (greek): bridge eta, asked person Henry

**lookup** (PP-L0-0128): O's answer 2

```
<|im_start|>user
The locker of theta is 7. Adam picked beta. ⟦person:Henry⟧ picked ⟦bridge:eta⟧. Liam picked theta. The locker of beta is 9. The locker of eta is 2.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | 1 | ' 2' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '2' | 1 | ' 2' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '2' | 1 | ' 2' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 0 | ' 7' |

**recall** (PM-L0-0128): O's answer 7

```
<|im_start|>user
The locker of theta is 7. Adam picked beta. ⟦person:Henry⟧ picked ⟦bridge:eta⟧. Liam picked theta. The locker of beta is 9. The locker of eta is 2.
Which position in the Greek alphabet does Henry's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | 1 | ' 7' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '7' | 1 | ' 7' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '7' | 1 | ' 7' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '8' | 0 | ' 8' |

### P2-L0-0130 (elements): bridge carbon, asked person Alice

**lookup** (PP-L0-0130): O's answer 4

```
<|im_start|>user
⟦person:Alice⟧ picked ⟦bridge:carbon⟧. The locker of hydrogen is 9. Frank picked lithium. The locker of carbon is 4. The locker of lithium is 7. Dan picked hydrogen.
Which locker belongs to Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | 1 | ' 4' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '4' | 1 | ' 4' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '4' | 1 | ' 4' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '9' | 0 | ' 9' |

**recall** (PM-L0-0130): O's answer 6

```
<|im_start|>user
⟦person:Alice⟧ picked ⟦bridge:carbon⟧. The locker of hydrogen is 9. Frank picked lithium. The locker of carbon is 4. The locker of lithium is 7. Dan picked hydrogen.
What is the atomic number of Alice's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | 1 | ' 6' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '6' | 1 | ' 6' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '6' | 1 | ' 6' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '6' | 1 | ' 6' |

### P2-L0-0136 (elements): bridge hydrogen, asked person Mia

**lookup** (PP-L0-0136): O's answer 3

```
<|im_start|>user
⟦person:M⟧⟦person:ia⟧ picked ⟦bridge:hydrogen⟧. The locker of hydrogen is three. The locker of oxygen is six. Amy picked oxygen. The locker of nitrogen is eight. Jack picked nitrogen.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '1' | 0 | ' 1' |

**recall** (PM-L0-0136): O's answer 1

```
<|im_start|>user
⟦person:M⟧⟦person:ia⟧ picked ⟦bridge:hydrogen⟧. The locker of hydrogen is three. The locker of oxygen is six. Amy picked oxygen. The locker of nitrogen is eight. Jack picked nitrogen.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | 1 | ' 1' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '1' | 1 | ' 1' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '1' | 1 | ' 1' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '1' | 1 | ' 1' |

### P2-L0-0204 (animals): bridge tick, asked person Maria

**lookup** (PP-L0-0204): O's answer 3

```
<|im_start|>user
⟦person:Maria⟧ picked the ⟦bridge:tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | 1 | ' 3' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '3' | 1 | ' 3' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '3' | 1 | ' 3' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '7' | 0 | ' 7' |

**recall** (PM-L0-0204): O's answer 8

```
<|im_start|>user
⟦person:Maria⟧ picked the ⟦bridge:tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
How many legs does Maria's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | right | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | 1 | ' 8' |
| bridge_late | MLP writes at the bridge token mean-ablated, layers l > L | '8' | 1 | ' 8' |
| person_late | MLP writes at the asked person's token mean-ablated, layers l > L (control 1) | '8' | 1 | ' 8' |
| bridge_early | MLP writes at the bridge token mean-ablated, layers l <= L / 2 (control 2) | '8' | 1 | ' 8' |

