# 48.4 examples (verify pack): the lookup's prompt exactly as the model reads it at the read step; ⟦bridge:…⟧ the bridge token, ⟦read:…⟧ the appended read token (the query position). UNVERIFIED.

## qwen35_9b_x48_heads: 10 random items of 75 (seed 0)

### P2-L0-0018 (animals): bridge eagle (alt butterfly); lookup PP-L0-0018: O's answer 4

```
<|im_start|>user
The locker of the butterfly is 5. Sara picked the butterfly. Rose picked the fox. The locker of the eagle is 4. The locker of the fox is 3. Jack picked the⟦bridge: eagle⟧.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L19:h11 | 0.880 | 0.607 | 0.528 | 0.476 | 0.522 | 0.419 |
| L19:h02 | 0.910 | 0.165 | 0.427 | 0.352 | 0.371 | 0.295 |
| L19:h10 | 0.638 | 0.055 | 0.426 | 0.399 | 0.478 | 0.359 |
| L19:h01 | 0.611 | 0.420 | 0.468 | 0.353 | 0.381 | 0.299 |
| L19:h00 | 0.503 | 0.680 | 0.421 | 0.361 | 0.392 | 0.295 |

### P2-L0-0114 (animals): bridge goose (alt mouse); lookup PP-L0-0114: O's answer 3

```
<|im_start|>user
The locker of the mouse is 6. James picked the mouse. Eric picked the beetle. The locker of the beetle is 8. The locker of the goose is 3. Oscar picked the⟦bridge: goose⟧.
Which locker belongs to Oscar's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L19:h11 | 0.801 | 0.484 | 0.520 | 0.478 | 0.486 | 0.418 |
| L19:h02 | 0.797 | 0.109 | 0.436 | 0.361 | 0.347 | 0.305 |
| L19:h10 | 0.365 | 0.049 | 0.410 | 0.396 | 0.432 | 0.351 |
| L19:h01 | 0.212 | 0.181 | 0.468 | 0.369 | 0.358 | 0.303 |
| L19:h00 | 0.305 | 0.416 | 0.434 | 0.362 | 0.367 | 0.297 |

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
| L19:h11 | 0.940 | 0.755 | 0.513 | 0.560 | 0.553 | 0.421 |
| L19:h02 | 0.983 | 0.355 | 0.434 | 0.398 | 0.364 | 0.323 |
| L19:h10 | 0.723 | 0.063 | 0.395 | 0.427 | 0.489 | 0.354 |
| L19:h01 | 0.736 | 0.529 | 0.476 | 0.410 | 0.369 | 0.333 |
| L19:h00 | 0.654 | 0.846 | 0.448 | 0.412 | 0.379 | 0.335 |

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
| L19:h11 | 0.841 | 0.607 | 0.544 | 0.494 | 0.487 | 0.438 |
| L19:h02 | 0.911 | 0.242 | 0.472 | 0.346 | 0.349 | 0.350 |
| L19:h10 | 0.488 | 0.123 | 0.441 | 0.407 | 0.437 | 0.383 |
| L19:h01 | 0.294 | 0.253 | 0.505 | 0.349 | 0.361 | 0.357 |
| L19:h00 | 0.389 | 0.786 | 0.481 | 0.356 | 0.370 | 0.351 |

### P2-L0-0196 (elements): bridge hydrogen (alt nitrogen); lookup PP-L0-0196: O's answer 3

```
<|im_start|>user
The locker of nitrogen is four. Tara picked nitrogen. The locker of hydrogen is three. The locker of carbon is five. Mia picked carbon. Finn picked⟦bridge: hydrogen⟧.
Which locker belongs to Finn's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L19:h11 | 0.807 | 0.338 | 0.533 | 0.462 | 0.560 | 0.421 |
| L19:h02 | 0.857 | 0.136 | 0.464 | 0.351 | 0.396 | 0.306 |
| L19:h10 | 0.622 | 0.282 | 0.424 | 0.412 | 0.520 | 0.365 |
| L19:h01 | 0.228 | 0.067 | 0.505 | 0.357 | 0.400 | 0.322 |
| L19:h00 | 0.500 | 0.590 | 0.491 | 0.366 | 0.423 | 0.317 |

### P2-L0-0213 (animals): bridge goose (alt bee); lookup PP-L0-0213: O's answer 4

```
<|im_start|>user
The locker of the bee is three. The locker of the beetle is one. The locker of the goose is four. Hugo picked the beetle. Noah picked the bee. Rose picked the⟦bridge: goose⟧.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L19:h11 | 0.882 | 0.268 | 0.437 | 0.515 | 0.541 | 0.410 |
| L19:h02 | 0.744 | 0.013 | 0.380 | 0.340 | 0.386 | 0.292 |
| L19:h10 | 0.549 | 0.057 | 0.360 | 0.434 | 0.499 | 0.360 |
| L19:h01 | 0.236 | 0.079 | 0.403 | 0.349 | 0.392 | 0.302 |
| L19:h00 | 0.307 | 0.227 | 0.398 | 0.354 | 0.407 | 0.304 |

### P2-L0-0218 (greek): bridge gamma (alt epsilon); lookup PP-L0-0218: O's answer 8

```
<|im_start|>user
The locker of gamma is 8. The locker of epsilon is 6. Mark picked epsilon. Clara picked⟦bridge: gamma⟧. The locker of theta is 3. Finn picked theta.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L19:h11 | 0.834 | 0.178 | 0.493 | 0.489 | 0.541 | 0.398 |
| L19:h02 | 0.850 | 0.129 | 0.396 | 0.345 | 0.378 | 0.351 |
| L19:h10 | 0.469 | 0.331 | 0.407 | 0.446 | 0.498 | 0.350 |
| L19:h01 | 0.513 | 0.010 | 0.410 | 0.351 | 0.387 | 0.353 |
| L19:h00 | 0.409 | 0.120 | 0.393 | 0.359 | 0.408 | 0.353 |

### P2-L0-0246 (animals): bridge cow (alt owl); lookup PP-L0-0246: O's answer 3

```
<|im_start|>user
The locker of the cow is 3. The locker of the owl is 4. The locker of the fox is 1. Jack picked the⟦bridge: cow⟧. Tara picked the fox. Diana picked the owl.
Which locker belongs to Jack's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L19:h11 | 0.798 | 0.493 | 0.600 | 0.581 | 0.567 | 0.465 |
| L19:h02 | 0.792 | 0.116 | 0.458 | 0.390 | 0.397 | 0.340 |
| L19:h10 | 0.383 | 0.012 | 0.473 | 0.506 | 0.531 | 0.402 |
| L19:h01 | 0.368 | 0.389 | 0.496 | 0.403 | 0.400 | 0.349 |
| L19:h00 | 0.265 | 0.623 | 0.448 | 0.409 | 0.426 | 0.330 |

### P2-L0-0252 (animals): bridge sheep (alt spider); lookup PP-L0-0252: O's answer 9

```
<|im_start|>user
Victor picked the spider. The locker of the sheep is 9. Luke picked the butterfly. The locker of the spider is 7. Rose picked the⟦bridge: sheep⟧. The locker of the butterfly is 3.
Which locker belongs to Rose's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L19:h11 | 0.809 | 0.744 | 0.525 | 0.471 | 0.470 | 0.382 |
| L19:h02 | 0.844 | 0.205 | 0.472 | 0.367 | 0.341 | 0.329 |
| L19:h10 | 0.622 | 0.064 | 0.420 | 0.383 | 0.426 | 0.330 |
| L19:h01 | 0.255 | 0.521 | 0.506 | 0.367 | 0.351 | 0.341 |
| L19:h00 | 0.286 | 0.760 | 0.464 | 0.373 | 0.362 | 0.346 |

### P2-L0-0256 (elements): bridge lithium (alt hydrogen); lookup PP-L0-0256: O's answer 7

```
<|im_start|>user
The locker of hydrogen is 2. Victor picked helium. The locker of lithium is 7. David picked hydrogen. The locker of helium is 9. Sara picked⟦bridge: lithium⟧.
Which locker belongs to Sara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L19:h11 | 0.791 | 0.624 | 0.514 | 0.584 | 0.553 | 0.461 |
| L19:h02 | 0.718 | 0.225 | 0.424 | 0.365 | 0.385 | 0.324 |
| L19:h10 | 0.409 | 0.237 | 0.422 | 0.477 | 0.504 | 0.369 |
| L19:h01 | 0.595 | 0.184 | 0.459 | 0.371 | 0.389 | 0.329 |
| L19:h00 | 0.430 | 0.378 | 0.434 | 0.383 | 0.403 | 0.324 |

## muse30_x48_heads: 10 random items of 68 (seed 0)

### P2-L0-0021 (animals): bridge sheep (alt goose); lookup PP-L0-0021: O's answer 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the goose is eight. The locker of the sheep is five. The locker of the owl is four. Lucy picked the owl. Finn picked the goose. Ruby picked the⟦bridge: sheep⟧.
Which locker belongs to Ruby's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.628 | 0.254 | 0.039 | 0.036 | 0.043 | 0.029 |
| L30:h26 | 0.397 | 0.069 | 0.044 | 0.118 | 0.168 | 0.059 |
| L28:h15 | 0.490 | 0.009 | 0.030 | 0.040 | 0.033 | 0.032 |
| L31:h09 | 0.658 | 0.186 | 0.040 | 0.070 | 0.084 | 0.038 |
| L31:h04 | 0.515 | 0.085 | 0.057 | 0.074 | 0.083 | 0.041 |

### P2-L0-0069 (animals): bridge sheep (alt butterfly); lookup PP-L0-0069: O's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the⟦bridge: sheep⟧. Ella picked the butterfly.
Which locker belongs to Ivy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.668 | 0.140 | 0.042 | 0.036 | 0.039 | 0.031 |
| L30:h26 | 0.430 | 0.137 | 0.044 | 0.112 | 0.131 | 0.058 |
| L28:h15 | 0.302 | 0.017 | 0.024 | 0.029 | 0.031 | 0.031 |
| L31:h09 | 0.613 | 0.092 | 0.048 | 0.071 | 0.064 | 0.042 |
| L31:h04 | 0.401 | 0.045 | 0.074 | 0.073 | 0.062 | 0.044 |

### P2-L0-0096 (animals): bridge bee (alt spider); lookup PP-L0-0096: O's answer 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦bridge: bee⟧.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.744 | 0.162 | 0.039 | 0.032 | 0.042 | 0.029 |
| L30:h26 | 0.632 | 0.197 | 0.049 | 0.120 | 0.156 | 0.052 |
| L28:h15 | 0.614 | 0.007 | 0.028 | 0.035 | 0.033 | 0.032 |
| L31:h09 | 0.190 | 0.386 | 0.046 | 0.070 | 0.079 | 0.040 |
| L31:h04 | 0.180 | 0.294 | 0.071 | 0.074 | 0.077 | 0.044 |

### P2-L0-0133 (elements): bridge carbon (alt oxygen); lookup PP-L0-0133: O's answer 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked⟦bridge: carbon⟧. Eva picked helium.
Which locker belongs to Eric's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.741 | 0.425 | 0.045 | 0.040 | 0.040 | 0.031 |
| L30:h26 | 0.539 | 0.373 | 0.041 | 0.127 | 0.139 | 0.054 |
| L28:h15 | 0.567 | 0.159 | 0.029 | 0.045 | 0.034 | 0.036 |
| L31:h09 | 0.583 | 0.557 | 0.047 | 0.069 | 0.068 | 0.036 |
| L31:h04 | 0.605 | 0.500 | 0.054 | 0.074 | 0.067 | 0.036 |

### P2-L0-0219 (animals): bridge sheep (alt butterfly); lookup PP-L0-0219: O's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the sheep is 6. The locker of the butterfly is 7. Eve picked the butterfly. Owen picked the camel. The locker of the camel is 9. Diana picked the⟦bridge: sheep⟧.
Which locker belongs to Diana's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.682 | 0.754 | 0.046 | 0.036 | 0.042 | 0.030 |
| L30:h26 | 0.703 | 0.139 | 0.044 | 0.127 | 0.163 | 0.061 |
| L28:h15 | 0.850 | 0.030 | 0.026 | 0.029 | 0.033 | 0.035 |
| L31:h09 | 0.335 | 0.574 | 0.039 | 0.070 | 0.081 | 0.039 |
| L31:h04 | 0.418 | 0.604 | 0.055 | 0.077 | 0.080 | 0.044 |

### P2-L0-0221 (greek): bridge beta (alt delta); lookup PP-L0-0221: O's answer 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of delta is nine. The locker of beta is one. Owen picked iota. Iris picked⟦bridge: beta⟧. The locker of iota is five. Mark picked delta.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.626 | 0.138 | 0.041 | 0.041 | 0.043 | 0.030 |
| L30:h26 | 0.718 | 0.546 | 0.043 | 0.130 | 0.169 | 0.057 |
| L28:h15 | 0.617 | 0.156 | 0.026 | 0.037 | 0.033 | 0.033 |
| L31:h09 | 0.170 | 0.114 | 0.046 | 0.067 | 0.086 | 0.035 |
| L31:h04 | 0.110 | 0.136 | 0.050 | 0.069 | 0.084 | 0.037 |

### P2-L0-0243 (animals): bridge spider (alt tiger); lookup PP-L0-0243: O's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the spider is four. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the⟦bridge: spider⟧. Alice picked the tiger. Henry picked the sheep.
Which locker belongs to Olivia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.218 | 0.493 | 0.043 | 0.032 | 0.043 | 0.030 |
| L30:h26 | 0.662 | 0.409 | 0.052 | 0.112 | 0.169 | 0.054 |
| L28:h15 | 0.536 | 0.019 | 0.030 | 0.037 | 0.034 | 0.034 |
| L31:h09 | 0.082 | 0.182 | 0.040 | 0.065 | 0.085 | 0.035 |
| L31:h04 | 0.134 | 0.033 | 0.049 | 0.068 | 0.083 | 0.038 |

### P2-L0-0255 (animals): bridge chicken (alt frog); lookup PP-L0-0255: O's answer 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the frog is three. Frank picked the beetle. The locker of the chicken is one. Iris picked the⟦bridge: chicken⟧. The locker of the beetle is five. Nina picked the frog.
Which locker belongs to Iris's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.292 | 0.392 | 0.049 | 0.033 | 0.039 | 0.026 |
| L30:h26 | 0.040 | 0.072 | 0.048 | 0.095 | 0.138 | 0.048 |
| L28:h15 | 0.116 | 0.050 | 0.030 | 0.031 | 0.031 | 0.033 |
| L31:h09 | 0.200 | 0.374 | 0.041 | 0.055 | 0.071 | 0.033 |
| L31:h04 | 0.359 | 0.573 | 0.045 | 0.058 | 0.069 | 0.034 |

### P2-L0-0273 (animals): bridge fox (alt turkey); lookup PP-L0-0273: O's answer 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the turkey is 4. The locker of the fox is 6. Tom picked the frog. The locker of the frog is 7. Finn picked the⟦bridge: fox⟧. Sean picked the turkey.
Which locker belongs to Finn's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.838 | 0.362 | 0.045 | 0.036 | 0.043 | 0.027 |
| L30:h26 | 0.746 | 0.159 | 0.042 | 0.117 | 0.169 | 0.050 |
| L28:h15 | 0.357 | 0.025 | 0.027 | 0.031 | 0.034 | 0.027 |
| L31:h09 | 0.281 | 0.162 | 0.038 | 0.073 | 0.085 | 0.037 |
| L31:h04 | 0.224 | 0.082 | 0.042 | 0.079 | 0.084 | 0.039 |

### P2-L0-0287 (greek): bridge gamma (alt theta); lookup PP-L0-0287: O's answer 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked⟦bridge: gamma⟧. Ryan picked theta. The locker of epsilon is eight.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦read: ⟧
```

| head | lookup mass | recall mass | r(J++) | r(rest) | r(address) | r(random) |
|---|---|---|---|---|---|---|
| L33:h01 | 0.835 | 0.318 | 0.037 | 0.032 | 0.037 | 0.029 |
| L30:h26 | 0.788 | 0.738 | 0.045 | 0.116 | 0.118 | 0.063 |
| L28:h15 | 0.530 | 0.102 | 0.026 | 0.038 | 0.029 | 0.032 |
| L31:h09 | 0.207 | 0.380 | 0.045 | 0.067 | 0.058 | 0.040 |
| L31:h04 | 0.363 | 0.451 | 0.060 | 0.072 | 0.055 | 0.042 |

