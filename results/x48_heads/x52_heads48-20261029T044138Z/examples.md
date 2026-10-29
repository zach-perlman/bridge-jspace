# 48.4 examples (verify pack): the lookup's prompt exactly as the model reads it at the read step; ⟦bridge:…⟧ the bridge token, ⟦read:…⟧ the appended read token (the query position). UNVERIFIED.

## x48_heads_27b: 10 random items of 69 (seed 0)

### P2-L0-0016 (elements): bridge hydrogen (alt nitrogen); lookup PP-L0-0016: O's answer 9

```
<|im_start|>user
The locker of hydrogen is nine. Olivia picked nitrogen. Oscar picked helium. The locker of helium is seven. The locker of nitrogen is six. Hugo picked⟦bridge: hydrogen⟧.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.845 | 0.174 | 0.437 | 0.302 | 0.301 | 0.328 |
| L35:h03 | 0.721 | 0.600 | 0.465 | 0.307 | 0.303 | 0.334 |
| L35:h17 | 0.682 | 0.404 | 0.402 | 0.461 | 0.475 | 0.362 |
| L35:h20 | 0.484 | 0.605 | 0.707 | 0.429 | 0.421 | 0.302 |
| L35:h02 | 0.441 | 0.254 | 0.446 | 0.304 | 0.303 | 0.338 |

### P2-L0-0048 (animals): bridge crow (alt elephant); lookup PP-L0-0048: O's answer 3

```
<|im_start|>user
The locker of the beetle is nine. The locker of the elephant is eight. Lily picked the beetle. James picked the elephant. The locker of the crow is three. Henry picked the⟦bridge: crow⟧.
Which locker belongs to Henry's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.640 | 0.014 | 0.471 | 0.331 | 0.317 | 0.308 |
| L35:h03 | 0.815 | 0.064 | 0.481 | 0.346 | 0.319 | 0.322 |
| L35:h17 | 0.477 | 0.146 | 0.374 | 0.474 | 0.466 | 0.346 |
| L35:h20 | 0.481 | 0.227 | 0.647 | 0.455 | 0.378 | 0.323 |
| L35:h02 | 0.653 | 0.050 | 0.476 | 0.338 | 0.313 | 0.324 |

### P2-L0-0083 (greek): bridge theta (alt alpha); lookup PP-L0-0083: O's answer 1

```
<|im_start|>user
The locker of alpha is four. Jack picked beta. Eve picked alpha. The locker of beta is five. The locker of theta is one. Hugo picked⟦bridge: theta⟧.
Which locker belongs to Hugo's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.775 | 0.249 | 0.460 | 0.339 | 0.314 | 0.322 |
| L35:h03 | 0.820 | 0.359 | 0.483 | 0.337 | 0.314 | 0.322 |
| L35:h17 | 0.709 | 0.355 | 0.397 | 0.463 | 0.485 | 0.364 |
| L35:h20 | 0.624 | 0.530 | 0.758 | 0.505 | 0.443 | 0.336 |
| L35:h02 | 0.627 | 0.226 | 0.459 | 0.336 | 0.315 | 0.321 |

### P2-L0-0133 (elements): bridge carbon (alt oxygen); lookup PP-L0-0133: O's answer 3

```
<|im_start|>user
The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked⟦bridge: carbon⟧. Eva picked helium.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.861 | 0.724 | 0.495 | 0.307 | 0.372 | 0.311 |
| L35:h03 | 0.818 | 0.835 | 0.530 | 0.322 | 0.371 | 0.316 |
| L35:h17 | 0.739 | 0.819 | 0.392 | 0.486 | 0.555 | 0.358 |
| L35:h20 | 0.726 | 0.753 | 0.712 | 0.492 | 0.543 | 0.328 |
| L35:h02 | 0.637 | 0.620 | 0.528 | 0.315 | 0.372 | 0.313 |

### P2-L0-0135 (animals): bridge goose (alt beetle); lookup PP-L0-0135: O's answer 7

```
<|im_start|>user
Ryan picked the beetle. Olivia picked the camel. The locker of the beetle is 4. The locker of the goose is 7. The locker of the camel is 5. Frank picked the⟦bridge: goose⟧.
Which locker belongs to Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.827 | 0.032 | 0.434 | 0.384 | 0.353 | 0.300 |
| L35:h03 | 0.791 | 0.093 | 0.465 | 0.420 | 0.361 | 0.307 |
| L35:h17 | 0.765 | 0.305 | 0.375 | 0.596 | 0.536 | 0.382 |
| L35:h20 | 0.666 | 0.311 | 0.612 | 0.605 | 0.490 | 0.414 |
| L35:h02 | 0.704 | 0.031 | 0.455 | 0.391 | 0.367 | 0.297 |

### P2-L0-0139 (elements): bridge oxygen (alt nitrogen); lookup PP-L0-0139: O's answer 6

```
<|im_start|>user
Hugo picked nitrogen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked⟦bridge: oxygen⟧.
Which locker belongs to Ruby's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.722 | 0.029 | 0.470 | 0.338 | 0.315 | 0.336 |
| L35:h03 | 0.606 | 0.412 | 0.520 | 0.348 | 0.321 | 0.342 |
| L35:h17 | 0.625 | 0.429 | 0.381 | 0.505 | 0.513 | 0.394 |
| L35:h20 | 0.638 | 0.557 | 0.736 | 0.488 | 0.470 | 0.362 |
| L35:h02 | 0.600 | 0.083 | 0.505 | 0.332 | 0.320 | 0.338 |

### P2-L0-0149 (greek): bridge delta (alt iota); lookup PP-L0-0149: O's answer 1

```
<|im_start|>user
The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked⟦bridge: delta⟧. Kate picked gamma. Luke picked iota.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.614 | 0.380 | 0.388 | 0.399 | 0.495 | 0.339 |
| L35:h03 | 0.803 | 0.537 | 0.401 | 0.403 | 0.479 | 0.337 |
| L35:h17 | 0.890 | 0.643 | 0.339 | 0.563 | 0.664 | 0.389 |
| L35:h20 | 0.636 | 0.692 | 0.737 | 0.533 | 0.668 | 0.391 |
| L35:h02 | 0.379 | 0.209 | 0.389 | 0.403 | 0.475 | 0.339 |

### P2-L0-0168 (animals): bridge elephant (alt fly); lookup PP-L0-0168: O's answer 2

```
<|im_start|>user
Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the⟦bridge: elephant⟧. Henry picked the fly.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.463 | 0.117 | 0.514 | 0.349 | 0.317 | 0.328 |
| L35:h03 | 0.562 | 0.131 | 0.560 | 0.351 | 0.318 | 0.338 |
| L35:h17 | 0.498 | 0.204 | 0.418 | 0.493 | 0.494 | 0.375 |
| L35:h20 | 0.565 | 0.606 | 0.497 | 0.527 | 0.426 | 0.343 |
| L35:h02 | 0.435 | 0.040 | 0.547 | 0.341 | 0.314 | 0.338 |

### P2-L0-0180 (animals): bridge beetle (alt eagle); lookup PP-L0-0180: O's answer 7

```
<|im_start|>user
The locker of the eagle is three. Ivy picked the bear. Emma picked the eagle. The locker of the beetle is seven. Olivia picked the⟦bridge: beetle⟧. The locker of the bear is one.
Which locker belongs to Olivia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.661 | 0.002 | 0.461 | 0.316 | 0.304 | 0.320 |
| L35:h03 | 0.566 | 0.013 | 0.471 | 0.320 | 0.304 | 0.317 |
| L35:h17 | 0.331 | 0.084 | 0.388 | 0.426 | 0.479 | 0.349 |
| L35:h20 | 0.455 | 0.186 | 0.537 | 0.451 | 0.433 | 0.323 |
| L35:h02 | 0.515 | 0.003 | 0.472 | 0.314 | 0.304 | 0.323 |

### P2-L0-0206 (greek): bridge eta (alt delta); lookup PP-L0-0206: O's answer 2

```
<|im_start|>user
Iris picked alpha. The locker of delta is 6. The locker of eta is 2. The locker of alpha is 9. Eva picked delta. Liam picked⟦bridge: eta⟧.
Which locker belongs to Liam's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L35:h04 | 0.457 | 0.018 | 0.391 | 0.347 | 0.309 | 0.324 |
| L35:h03 | 0.494 | 0.025 | 0.416 | 0.356 | 0.315 | 0.327 |
| L35:h17 | 0.452 | 0.041 | 0.386 | 0.489 | 0.500 | 0.366 |
| L35:h20 | 0.639 | 0.383 | 0.783 | 0.503 | 0.467 | 0.344 |
| L35:h02 | 0.522 | 0.016 | 0.399 | 0.342 | 0.314 | 0.325 |

