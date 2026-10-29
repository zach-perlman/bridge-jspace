# 53.3 examples (verify pack): every arm's top token per layer for 10 random items per run. UNVERIFIED.

## qwen35_9b_x53_3: 10 random items of 75 (seed 0)

### P2-L0-0018 (animals): bridge eagle → butterfly

O's context: The locker of the butterfly is 5. Sara picked the butterfly. Rose picked the fox. The locker of the eagle is 4. The locker of the fox is 3. Jack picked the eagle.

S's context: The locker of the butterfly is 5. Sara picked the eagle. Rose picked the fox. The locker of the eagle is 4. The locker of the fox is 3. Jack picked the butterfly.

**lookup** (Which locker belongs to Jack's pick?): O's answer 4, S's answer 5

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 24 | whole | '5' | 1 |
| 24 | no_jpp | '4' | 0 |
| 24 | no_rand | '4' | 0 |
| 24 | jpp | '4' | 0 |
| 24 | rest | '4' | 0 |
| 27 | whole | '5' | 1 |
| 27 | no_jpp | '4' | 0 |
| 27 | no_rand | '4' | 0 |
| 27 | jpp | '4' | 0 |
| 27 | rest | '4' | 0 |

**recall** (How many legs does Jack's pick have?): O's answer 2, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 24 | whole | '6' | 1 |
| 24 | no_jpp | '6' | 1 |
| 24 | no_rand | '6' | 1 |
| 24 | jpp | '2' | 0 |
| 24 | rest | '6' | 1 |
| 27 | whole | '6' | 1 |
| 27 | no_jpp | '6' | 1 |
| 27 | no_rand | '6' | 1 |
| 27 | jpp | '2' | 0 |
| 27 | rest | '6' | 1 |

### P2-L0-0114 (animals): bridge goose → mouse

O's context: The locker of the mouse is 6. James picked the mouse. Eric picked the beetle. The locker of the beetle is 8. The locker of the goose is 3. Oscar picked the goose.

S's context: The locker of the mouse is 6. James picked the goose. Eric picked the beetle. The locker of the beetle is 8. The locker of the goose is 3. Oscar picked the mouse.

**lookup** (Which locker belongs to Oscar's pick?): O's answer 3, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 24 | whole | '6' | 1 |
| 24 | no_jpp | '3' | 0 |
| 24 | no_rand | '6' | 1 |
| 24 | jpp | '3' | 0 |
| 24 | rest | '3' | 0 |
| 27 | whole | '6' | 1 |
| 27 | no_jpp | '3' | 0 |
| 27 | no_rand | '6' | 1 |
| 27 | jpp | '3' | 0 |
| 27 | rest | '3' | 0 |

**recall** (How many legs does Oscar's pick have?): O's answer 2, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 24 | whole | '4' | 1 |
| 24 | no_jpp | '4' | 1 |
| 24 | no_rand | '4' | 1 |
| 24 | jpp | '2' | 0 |
| 24 | rest | '4' | 1 |
| 27 | whole | '4' | 1 |
| 27 | no_jpp | '4' | 1 |
| 27 | no_rand | '6' | 0 |
| 27 | jpp | '2' | 0 |
| 27 | rest | '4' | 1 |

### P2-L0-0135 (animals): bridge goose → beetle

O's context: Ryan picked the beetle. Olivia picked the camel. The locker of the beetle is 4. The locker of the goose is 7. The locker of the camel is 5. Frank picked the goose.

S's context: Ryan picked the goose. Olivia picked the camel. The locker of the beetle is 4. The locker of the goose is 7. The locker of the camel is 5. Frank picked the beetle.

**lookup** (Which locker belongs to Frank's pick?): O's answer 7, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '7' | 0 |
| 24 | whole | '4' | 1 |
| 24 | no_jpp | '7' | 0 |
| 24 | no_rand | '7' | 0 |
| 24 | jpp | '7' | 0 |
| 24 | rest | '7' | 0 |
| 27 | whole | '4' | 1 |
| 27 | no_jpp | '7' | 0 |
| 27 | no_rand | '7' | 0 |
| 27 | jpp | '7' | 0 |
| 27 | rest | '7' | 0 |

**recall** (How many legs does Frank's pick have?): O's answer 2, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 24 | whole | '6' | 1 |
| 24 | no_jpp | '6' | 1 |
| 24 | no_rand | '6' | 1 |
| 24 | jpp | '2' | 0 |
| 24 | rest | '6' | 1 |
| 27 | whole | '6' | 1 |
| 27 | no_jpp | '6' | 1 |
| 27 | no_rand | '6' | 1 |
| 27 | jpp | '6' | 1 |
| 27 | rest | '6' | 1 |

### P2-L0-0180 (animals): bridge beetle → eagle

O's context: The locker of the eagle is three. Ivy picked the bear. Emma picked the eagle. The locker of the beetle is seven. Olivia picked the beetle. The locker of the bear is one.

S's context: The locker of the eagle is three. Ivy picked the bear. Emma picked the beetle. The locker of the beetle is seven. Olivia picked the eagle. The locker of the bear is one.

**lookup** (Which locker belongs to Olivia's pick?): O's answer 7, S's answer 3

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '7' | 0 |
| 24 | whole | '3' | 1 |
| 24 | no_jpp | '7' | 0 |
| 24 | no_rand | '7' | 0 |
| 24 | jpp | '7' | 0 |
| 24 | rest | '7' | 0 |
| 27 | whole | '3' | 1 |
| 27 | no_jpp | '7' | 0 |
| 27 | no_rand | '7' | 0 |
| 27 | jpp | '7' | 0 |
| 27 | rest | '7' | 0 |

**recall** (How many legs does Olivia's pick have?): O's answer 6, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 24 | whole | '2' | 1 |
| 24 | no_jpp | '6' | 0 |
| 24 | no_rand | '6' | 0 |
| 24 | jpp | '6' | 0 |
| 24 | rest | '6' | 0 |
| 27 | whole | '2' | 1 |
| 27 | no_jpp | '6' | 0 |
| 27 | no_rand | '6' | 0 |
| 27 | jpp | '6' | 0 |
| 27 | rest | '6' | 0 |

### P2-L0-0196 (elements): bridge hydrogen → nitrogen

O's context: The locker of nitrogen is four. Tara picked nitrogen. The locker of hydrogen is three. The locker of carbon is five. Mia picked carbon. Finn picked hydrogen.

S's context: The locker of nitrogen is four. Tara picked hydrogen. The locker of hydrogen is three. The locker of carbon is five. Mia picked carbon. Finn picked nitrogen.

**lookup** (Which locker belongs to Finn's pick?): O's answer 3, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 24 | whole | '4' | 1 |
| 24 | no_jpp | '3' | 0 |
| 24 | no_rand | '4' | 1 |
| 24 | jpp | '3' | 0 |
| 24 | rest | '3' | 0 |
| 27 | whole | '4' | 1 |
| 27 | no_jpp | '3' | 0 |
| 27 | no_rand | '3' | 0 |
| 27 | jpp | '3' | 0 |
| 27 | rest | '3' | 0 |

**recall** (What is the atomic number of Finn's pick?): O's answer 1, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '1' | 0 |
| 24 | whole | '7' | 1 |
| 24 | no_jpp | '7' | 1 |
| 24 | no_rand | '7' | 1 |
| 24 | jpp | '1' | 0 |
| 24 | rest | '7' | 1 |
| 27 | whole | '7' | 1 |
| 27 | no_jpp | '7' | 1 |
| 27 | no_rand | '7' | 1 |
| 27 | jpp | '1' | 0 |
| 27 | rest | '7' | 1 |

### P2-L0-0213 (animals): bridge goose → bee

O's context: The locker of the bee is three. The locker of the beetle is one. The locker of the goose is four. Hugo picked the beetle. Noah picked the bee. Rose picked the goose.

S's context: The locker of the bee is three. The locker of the beetle is one. The locker of the goose is four. Hugo picked the beetle. Noah picked the goose. Rose picked the bee.

**lookup** (Which locker belongs to Rose's pick?): O's answer 4, S's answer 3

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 24 | whole | '3' | 1 |
| 24 | no_jpp | '4' | 0 |
| 24 | no_rand | '4' | 0 |
| 24 | jpp | '4' | 0 |
| 24 | rest | '4' | 0 |
| 27 | whole | '3' | 1 |
| 27 | no_jpp | '4' | 0 |
| 27 | no_rand | '4' | 0 |
| 27 | jpp | '4' | 0 |
| 27 | rest | '4' | 0 |

**recall** (How many legs does Rose's pick have?): O's answer 2, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 24 | whole | '6' | 1 |
| 24 | no_jpp | '6' | 1 |
| 24 | no_rand | '6' | 1 |
| 24 | jpp | '2' | 0 |
| 24 | rest | '6' | 1 |
| 27 | whole | '6' | 1 |
| 27 | no_jpp | '6' | 1 |
| 27 | no_rand | '6' | 1 |
| 27 | jpp | '2' | 0 |
| 27 | rest | '6' | 1 |

### P2-L0-0218 (greek): bridge gamma → epsilon

O's context: The locker of gamma is 8. The locker of epsilon is 6. Mark picked epsilon. Clara picked gamma. The locker of theta is 3. Finn picked theta.

S's context: The locker of gamma is 8. The locker of epsilon is 6. Mark picked gamma. Clara picked epsilon. The locker of theta is 3. Finn picked theta.

**lookup** (Which locker belongs to Clara's pick?): O's answer 8, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '8' | 0 |
| 24 | whole | '8' | 0 |
| 24 | no_jpp | '8' | 0 |
| 24 | no_rand | '8' | 0 |
| 24 | jpp | '8' | 0 |
| 24 | rest | '8' | 0 |
| 27 | whole | '8' | 0 |
| 27 | no_jpp | '8' | 0 |
| 27 | no_rand | '8' | 0 |
| 27 | jpp | '8' | 0 |
| 27 | rest | '8' | 0 |

**recall** (Which position in the Greek alphabet does Clara's pick have?): O's answer 3, S's answer 5

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 24 | whole | '5' | 1 |
| 24 | no_jpp | '5' | 1 |
| 24 | no_rand | '5' | 1 |
| 24 | jpp | '5' | 1 |
| 24 | rest | '5' | 1 |
| 27 | whole | '5' | 1 |
| 27 | no_jpp | '5' | 1 |
| 27 | no_rand | '5' | 1 |
| 27 | jpp | '5' | 1 |
| 27 | rest | '5' | 1 |

### P2-L0-0246 (animals): bridge cow → owl

O's context: The locker of the cow is 3. The locker of the owl is 4. The locker of the fox is 1. Jack picked the cow. Tara picked the fox. Diana picked the owl.

S's context: The locker of the cow is 3. The locker of the owl is 4. The locker of the fox is 1. Jack picked the owl. Tara picked the fox. Diana picked the cow.

**lookup** (Which locker belongs to Jack's pick?): O's answer 3, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 24 | whole | '3' | 0 |
| 24 | no_jpp | '3' | 0 |
| 24 | no_rand | '3' | 0 |
| 24 | jpp | '3' | 0 |
| 24 | rest | '3' | 0 |
| 27 | whole | '3' | 0 |
| 27 | no_jpp | '3' | 0 |
| 27 | no_rand | '3' | 0 |
| 27 | jpp | '3' | 0 |
| 27 | rest | '3' | 0 |

**recall** (How many legs does Jack's pick have?): O's answer 4, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 24 | whole | '2' | 1 |
| 24 | no_jpp | '2' | 1 |
| 24 | no_rand | '2' | 1 |
| 24 | jpp | '4' | 0 |
| 24 | rest | '2' | 1 |
| 27 | whole | '2' | 1 |
| 27 | no_jpp | '4' | 0 |
| 27 | no_rand | '4' | 0 |
| 27 | jpp | '4' | 0 |
| 27 | rest | '4' | 0 |

### P2-L0-0252 (animals): bridge sheep → spider

O's context: Victor picked the spider. The locker of the sheep is 9. Luke picked the butterfly. The locker of the spider is 7. Rose picked the sheep. The locker of the butterfly is 3.

S's context: Victor picked the sheep. The locker of the sheep is 9. Luke picked the butterfly. The locker of the spider is 7. Rose picked the spider. The locker of the butterfly is 3.

**lookup** (Which locker belongs to Rose's pick?): O's answer 9, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '9' | 0 |
| 24 | whole | '7' | 1 |
| 24 | no_jpp | '7' | 1 |
| 24 | no_rand | '7' | 1 |
| 24 | jpp | '9' | 0 |
| 24 | rest | '7' | 1 |
| 27 | whole | '7' | 1 |
| 27 | no_jpp | '7' | 1 |
| 27 | no_rand | '7' | 1 |
| 27 | jpp | '9' | 0 |
| 27 | rest | '7' | 1 |

**recall** (How many legs does Rose's pick have?): O's answer 4, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 24 | whole | '8' | 1 |
| 24 | no_jpp | '8' | 1 |
| 24 | no_rand | '8' | 1 |
| 24 | jpp | '8' | 1 |
| 24 | rest | '8' | 1 |
| 27 | whole | '8' | 1 |
| 27 | no_jpp | '8' | 1 |
| 27 | no_rand | '8' | 1 |
| 27 | jpp | '4' | 0 |
| 27 | rest | '8' | 1 |

### P2-L0-0256 (elements): bridge lithium → hydrogen

O's context: The locker of hydrogen is 2. Victor picked helium. The locker of lithium is 7. David picked hydrogen. The locker of helium is 9. Sara picked lithium.

S's context: The locker of hydrogen is 2. Victor picked helium. The locker of lithium is 7. David picked lithium. The locker of helium is 9. Sara picked hydrogen.

**lookup** (Which locker belongs to Sara's pick?): O's answer 7, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '7' | 0 |
| 24 | whole | '2' | 1 |
| 24 | no_jpp | '2' | 1 |
| 24 | no_rand | '2' | 1 |
| 24 | jpp | '7' | 0 |
| 24 | rest | '2' | 1 |
| 27 | whole | '2' | 1 |
| 27 | no_jpp | '2' | 1 |
| 27 | no_rand | '2' | 1 |
| 27 | jpp | '7' | 0 |
| 27 | rest | '2' | 1 |

**recall** (What is the atomic number of Sara's pick?): O's answer 3, S's answer 1

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 24 | whole | '1' | 1 |
| 24 | no_jpp | '1' | 1 |
| 24 | no_rand | '1' | 1 |
| 24 | jpp | '3' | 0 |
| 24 | rest | '1' | 1 |
| 27 | whole | '1' | 1 |
| 27 | no_jpp | '3' | 0 |
| 27 | no_rand | '1' | 1 |
| 27 | jpp | '3' | 0 |
| 27 | rest | '3' | 0 |

