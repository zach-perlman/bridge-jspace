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

## x53_3_27b: 10 random items of 69 (seed 0)

### P2-L0-0016 (elements): bridge hydrogen → nitrogen

O's context: The locker of hydrogen is nine. Olivia picked nitrogen. Oscar picked helium. The locker of helium is seven. The locker of nitrogen is six. Hugo picked hydrogen.

S's context: The locker of hydrogen is nine. Olivia picked hydrogen. Oscar picked helium. The locker of helium is seven. The locker of nitrogen is six. Hugo picked nitrogen.

**lookup** (Which locker belongs to Hugo's pick?): O's answer 9, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '9' | 0 |
| 60 | whole | '9' | 0 |
| 60 | no_jpp | '9' | 0 |
| 60 | no_rand | '9' | 0 |
| 60 | jpp | '9' | 0 |
| 60 | rest | '9' | 0 |
| 59 | whole | '9' | 0 |
| 59 | no_jpp | '9' | 0 |
| 59 | no_rand | '9' | 0 |
| 59 | jpp | '9' | 0 |
| 59 | rest | '9' | 0 |

**recall** (What is the atomic number of Hugo's pick?): O's answer 1, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '1' | 0 |
| 56 | whole | '7' | 1 |
| 56 | no_jpp | '1' | 0 |
| 56 | no_rand | '1' | 0 |
| 56 | jpp | '1' | 0 |
| 56 | rest | '1' | 0 |
| 59 | whole | '7' | 1 |
| 59 | no_jpp | '1' | 0 |
| 59 | no_rand | '1' | 0 |
| 59 | jpp | '1' | 0 |
| 59 | rest | '1' | 0 |

### P2-L0-0048 (animals): bridge crow → elephant

O's context: The locker of the beetle is nine. The locker of the elephant is eight. Lily picked the beetle. James picked the elephant. The locker of the crow is three. Henry picked the crow.

S's context: The locker of the beetle is nine. The locker of the elephant is eight. Lily picked the beetle. James picked the crow. The locker of the crow is three. Henry picked the elephant.

**lookup** (Which locker belongs to Henry's pick?): O's answer 3, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 60 | whole | '3' | 0 |
| 60 | no_jpp | '3' | 0 |
| 60 | no_rand | '3' | 0 |
| 60 | jpp | '3' | 0 |
| 60 | rest | '3' | 0 |
| 59 | whole | '3' | 0 |
| 59 | no_jpp | '3' | 0 |
| 59 | no_rand | '3' | 0 |
| 59 | jpp | '3' | 0 |
| 59 | rest | '3' | 0 |

**recall** (How many legs does Henry's pick have?): O's answer 2, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 56 | whole | '4' | 1 |
| 56 | no_jpp | '4' | 1 |
| 56 | no_rand | '4' | 1 |
| 56 | jpp | '2' | 0 |
| 56 | rest | '4' | 1 |
| 59 | whole | '4' | 1 |
| 59 | no_jpp | '2' | 0 |
| 59 | no_rand | '4' | 1 |
| 59 | jpp | '2' | 0 |
| 59 | rest | '2' | 0 |

### P2-L0-0083 (greek): bridge theta → alpha

O's context: The locker of alpha is four. Jack picked beta. Eve picked alpha. The locker of beta is five. The locker of theta is one. Hugo picked theta.

S's context: The locker of alpha is four. Jack picked beta. Eve picked theta. The locker of beta is five. The locker of theta is one. Hugo picked alpha.

**lookup** (Which locker belongs to Hugo's pick?): O's answer 1, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '1' | 0 |
| 60 | whole | '1' | 0 |
| 60 | no_jpp | '1' | 0 |
| 60 | no_rand | '1' | 0 |
| 60 | jpp | '1' | 0 |
| 60 | rest | '1' | 0 |
| 59 | whole | '1' | 0 |
| 59 | no_jpp | '1' | 0 |
| 59 | no_rand | '1' | 0 |
| 59 | jpp | '1' | 0 |
| 59 | rest | '1' | 0 |

**recall** (Which position in the Greek alphabet does Hugo's pick have?): O's answer 8, S's answer 1

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '8' | 0 |
| 56 | whole | '1' | 1 |
| 56 | no_jpp | '1' | 1 |
| 56 | no_rand | '1' | 1 |
| 56 | jpp | '8' | 0 |
| 56 | rest | '1' | 1 |
| 59 | whole | '1' | 1 |
| 59 | no_jpp | '1' | 1 |
| 59 | no_rand | '1' | 1 |
| 59 | jpp | '8' | 0 |
| 59 | rest | '1' | 1 |

### P2-L0-0133 (elements): bridge carbon → oxygen

O's context: The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked carbon. Eva picked helium.

S's context: The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked carbon. Eric picked oxygen. Eva picked helium.

**lookup** (Which locker belongs to Eric's pick?): O's answer 3, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 60 | whole | '3' | 0 |
| 60 | no_jpp | '3' | 0 |
| 60 | no_rand | '3' | 0 |
| 60 | jpp | '3' | 0 |
| 60 | rest | '3' | 0 |
| 59 | whole | '3' | 0 |
| 59 | no_jpp | '3' | 0 |
| 59 | no_rand | '3' | 0 |
| 59 | jpp | '3' | 0 |
| 59 | rest | '3' | 0 |

**recall** (What is the atomic number of Eric's pick?): O's answer 6, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 56 | whole | '8' | 1 |
| 56 | no_jpp | '6' | 0 |
| 56 | no_rand | '6' | 0 |
| 56 | jpp | '6' | 0 |
| 56 | rest | '6' | 0 |
| 59 | whole | '8' | 1 |
| 59 | no_jpp | '6' | 0 |
| 59 | no_rand | '6' | 0 |
| 59 | jpp | '6' | 0 |
| 59 | rest | '6' | 0 |

### P2-L0-0135 (animals): bridge goose → beetle

O's context: Ryan picked the beetle. Olivia picked the camel. The locker of the beetle is 4. The locker of the goose is 7. The locker of the camel is 5. Frank picked the goose.

S's context: Ryan picked the goose. Olivia picked the camel. The locker of the beetle is 4. The locker of the goose is 7. The locker of the camel is 5. Frank picked the beetle.

**lookup** (Which locker belongs to Frank's pick?): O's answer 7, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '7' | 0 |
| 60 | whole | '4' | 1 |
| 60 | no_jpp | '7' | 0 |
| 60 | no_rand | '7' | 0 |
| 60 | jpp | '7' | 0 |
| 60 | rest | '7' | 0 |
| 59 | whole | '7' | 0 |
| 59 | no_jpp | '7' | 0 |
| 59 | no_rand | '7' | 0 |
| 59 | jpp | '7' | 0 |
| 59 | rest | '7' | 0 |

**recall** (How many legs does Frank's pick have?): O's answer 2, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 56 | whole | '6' | 1 |
| 56 | no_jpp | '6' | 1 |
| 56 | no_rand | '6' | 1 |
| 56 | jpp | '2' | 0 |
| 56 | rest | '6' | 1 |
| 59 | whole | '6' | 1 |
| 59 | no_jpp | '6' | 1 |
| 59 | no_rand | '6' | 1 |
| 59 | jpp | '2' | 0 |
| 59 | rest | '6' | 1 |

### P2-L0-0139 (elements): bridge oxygen → nitrogen

O's context: Hugo picked nitrogen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked oxygen.

S's context: Hugo picked oxygen. The locker of nitrogen is 9. Oscar picked hydrogen. The locker of oxygen is 6. The locker of hydrogen is 2. Ruby picked nitrogen.

**lookup** (Which locker belongs to Ruby's pick?): O's answer 6, S's answer 9

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 60 | whole | '6' | 0 |
| 60 | no_jpp | '6' | 0 |
| 60 | no_rand | '6' | 0 |
| 60 | jpp | '6' | 0 |
| 60 | rest | '6' | 0 |
| 59 | whole | '6' | 0 |
| 59 | no_jpp | '6' | 0 |
| 59 | no_rand | '6' | 0 |
| 59 | jpp | '6' | 0 |
| 59 | rest | '6' | 0 |

**recall** (What is the atomic number of Ruby's pick?): O's answer 8, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '8' | 0 |
| 56 | whole | '7' | 1 |
| 56 | no_jpp | '7' | 1 |
| 56 | no_rand | '7' | 1 |
| 56 | jpp | '8' | 0 |
| 56 | rest | '7' | 1 |
| 59 | whole | '7' | 1 |
| 59 | no_jpp | '8' | 0 |
| 59 | no_rand | '7' | 1 |
| 59 | jpp | '8' | 0 |
| 59 | rest | '8' | 0 |

### P2-L0-0149 (greek): bridge delta → iota

O's context: The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked delta. Kate picked gamma. Luke picked iota.

S's context: The locker of iota is 8. The locker of delta is 1. The locker of gamma is 6. Lucy picked iota. Kate picked gamma. Luke picked delta.

**lookup** (Which locker belongs to Lucy's pick?): O's answer 1, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '1' | 0 |
| 60 | whole | '1' | 0 |
| 60 | no_jpp | '1' | 0 |
| 60 | no_rand | '1' | 0 |
| 60 | jpp | '1' | 0 |
| 60 | rest | '1' | 0 |
| 59 | whole | '1' | 0 |
| 59 | no_jpp | '1' | 0 |
| 59 | no_rand | '1' | 0 |
| 59 | jpp | '1' | 0 |
| 59 | rest | '1' | 0 |

**recall** (Which position in the Greek alphabet does Lucy's pick have?): O's answer 4, S's answer 9

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 56 | whole | '9' | 1 |
| 56 | no_jpp | '9' | 1 |
| 56 | no_rand | '9' | 1 |
| 56 | jpp | '4' | 0 |
| 56 | rest | '9' | 1 |
| 59 | whole | '9' | 1 |
| 59 | no_jpp | '4' | 0 |
| 59 | no_rand | '9' | 1 |
| 59 | jpp | '4' | 0 |
| 59 | rest | '4' | 0 |

### P2-L0-0168 (animals): bridge elephant → fly

O's context: Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the elephant. Henry picked the fly.

S's context: Ryan picked the frog. The locker of the fly is five. The locker of the frog is nine. The locker of the elephant is two. Kyle picked the fly. Henry picked the elephant.

**lookup** (Which locker belongs to Kyle's pick?): O's answer 2, S's answer 5

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 60 | whole | '5' | 1 |
| 60 | no_jpp | '2' | 0 |
| 60 | no_rand | '2' | 0 |
| 60 | jpp | '2' | 0 |
| 60 | rest | '2' | 0 |
| 59 | whole | '5' | 1 |
| 59 | no_jpp | '2' | 0 |
| 59 | no_rand | '2' | 0 |
| 59 | jpp | '2' | 0 |
| 59 | rest | '2' | 0 |

**recall** (How many legs does Kyle's pick have?): O's answer 4, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 56 | whole | '6' | 1 |
| 56 | no_jpp | '6' | 1 |
| 56 | no_rand | '6' | 1 |
| 56 | jpp | '4' | 0 |
| 56 | rest | '6' | 1 |
| 59 | whole | '6' | 1 |
| 59 | no_jpp | '4' | 0 |
| 59 | no_rand | '6' | 1 |
| 59 | jpp | '6' | 1 |
| 59 | rest | '4' | 0 |

### P2-L0-0180 (animals): bridge beetle → eagle

O's context: The locker of the eagle is three. Ivy picked the bear. Emma picked the eagle. The locker of the beetle is seven. Olivia picked the beetle. The locker of the bear is one.

S's context: The locker of the eagle is three. Ivy picked the bear. Emma picked the beetle. The locker of the beetle is seven. Olivia picked the eagle. The locker of the bear is one.

**lookup** (Which locker belongs to Olivia's pick?): O's answer 7, S's answer 3

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '7' | 0 |
| 60 | whole | '7' | 0 |
| 60 | no_jpp | '7' | 0 |
| 60 | no_rand | '7' | 0 |
| 60 | jpp | '7' | 0 |
| 60 | rest | '7' | 0 |
| 59 | whole | '7' | 0 |
| 59 | no_jpp | '7' | 0 |
| 59 | no_rand | '7' | 0 |
| 59 | jpp | '7' | 0 |
| 59 | rest | '7' | 0 |

**recall** (How many legs does Olivia's pick have?): O's answer 6, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 56 | whole | '2' | 1 |
| 56 | no_jpp | '6' | 0 |
| 56 | no_rand | '6' | 0 |
| 56 | jpp | '6' | 0 |
| 56 | rest | '6' | 0 |
| 59 | whole | '2' | 1 |
| 59 | no_jpp | '6' | 0 |
| 59 | no_rand | '2' | 1 |
| 59 | jpp | '6' | 0 |
| 59 | rest | '6' | 0 |

### P2-L0-0206 (greek): bridge eta → delta

O's context: Iris picked alpha. The locker of delta is 6. The locker of eta is 2. The locker of alpha is 9. Eva picked delta. Liam picked eta.

S's context: Iris picked alpha. The locker of delta is 6. The locker of eta is 2. The locker of alpha is 9. Eva picked eta. Liam picked delta.

**lookup** (Which locker belongs to Liam's pick?): O's answer 2, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 60 | whole | '6' | 1 |
| 60 | no_jpp | '6' | 1 |
| 60 | no_rand | '6' | 1 |
| 60 | jpp | '2' | 0 |
| 60 | rest | '6' | 1 |
| 59 | whole | '6' | 1 |
| 59 | no_jpp | '2' | 0 |
| 59 | no_rand | '6' | 1 |
| 59 | jpp | '2' | 0 |
| 59 | rest | '2' | 0 |

**recall** (Which position in the Greek alphabet does Liam's pick have?): O's answer 7, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '7' | 0 |
| 56 | whole | '4' | 1 |
| 56 | no_jpp | '4' | 1 |
| 56 | no_rand | '4' | 1 |
| 56 | jpp | '5' | 0 |
| 56 | rest | '4' | 1 |
| 59 | whole | '4' | 1 |
| 59 | no_jpp | '7' | 0 |
| 59 | no_rand | '4' | 1 |
| 59 | jpp | '5' | 0 |
| 59 | rest | '7' | 0 |

## muse30_x53_3: 10 random items of 68 (seed 0)

### P2-L0-0021 (animals): bridge sheep → goose

O's context: The locker of the goose is eight. The locker of the sheep is five. The locker of the owl is four. Lucy picked the owl. Finn picked the goose. Ruby picked the sheep.

S's context: The locker of the goose is eight. The locker of the sheep is five. The locker of the owl is four. Lucy picked the owl. Finn picked the sheep. Ruby picked the goose.

**lookup** (Which locker belongs to Ruby's pick?): O's answer 5, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '5' | 0 |
| 32 | whole | '8' | 1 |
| 32 | no_jpp | '8' | 1 |
| 32 | no_rand | '8' | 1 |
| 32 | jpp | '5' | 0 |
| 32 | rest | '8' | 1 |
| 33 | whole | '8' | 1 |
| 33 | no_jpp | '8' | 1 |
| 33 | no_rand | '8' | 1 |
| 33 | jpp | '5' | 0 |
| 33 | rest | '8' | 1 |

**recall** (How many legs does Ruby's pick have?): O's answer 4, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 40 | whole | '2' | 1 |
| 40 | no_jpp | '2' | 1 |
| 40 | no_rand | '2' | 1 |
| 40 | jpp | '4' | 0 |
| 40 | rest | '2' | 1 |
| 44 | whole | '2' | 1 |
| 44 | no_jpp | '2' | 1 |
| 44 | no_rand | '2' | 1 |
| 44 | jpp | '4' | 0 |
| 44 | rest | '2' | 1 |

### P2-L0-0069 (animals): bridge sheep → butterfly

O's context: Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the sheep. Ella picked the butterfly.

S's context: Leo picked the wolf. The locker of the butterfly is 7. The locker of the sheep is 3. The locker of the wolf is 2. Ivy picked the butterfly. Ella picked the sheep.

**lookup** (Which locker belongs to Ivy's pick?): O's answer 3, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 32 | whole | '7' | 1 |
| 32 | no_jpp | '7' | 1 |
| 32 | no_rand | '7' | 1 |
| 32 | jpp | '3' | 0 |
| 32 | rest | '7' | 1 |
| 33 | whole | '7' | 1 |
| 33 | no_jpp | '7' | 1 |
| 33 | no_rand | '7' | 1 |
| 33 | jpp | '3' | 0 |
| 33 | rest | '7' | 1 |

**recall** (How many legs does Ivy's pick have?): O's answer 4, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 40 | whole | '6' | 1 |
| 40 | no_jpp | '6' | 1 |
| 40 | no_rand | '6' | 1 |
| 40 | jpp | '4' | 0 |
| 40 | rest | '6' | 1 |
| 44 | whole | '6' | 1 |
| 44 | no_jpp | '4' | 0 |
| 44 | no_rand | '6' | 1 |
| 44 | jpp | '4' | 0 |
| 44 | rest | '4' | 0 |

### P2-L0-0096 (animals): bridge bee → spider

O's context: The locker of the bee is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the bee.

S's context: The locker of the bee is 1. Laura picked the bee. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the spider.

**lookup** (Which locker belongs to Will's pick?): O's answer 1, S's answer 5

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '1' | 0 |
| 32 | whole | '5' | 1 |
| 32 | no_jpp | '5' | 1 |
| 32 | no_rand | '5' | 1 |
| 32 | jpp | '1' | 0 |
| 32 | rest | '5' | 1 |
| 33 | whole | '5' | 1 |
| 33 | no_jpp | '5' | 1 |
| 33 | no_rand | '5' | 1 |
| 33 | jpp | '1' | 0 |
| 33 | rest | '5' | 1 |

**recall** (How many legs does Will's pick have?): O's answer 6, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 40 | whole | '8' | 1 |
| 40 | no_jpp | '8' | 1 |
| 40 | no_rand | '8' | 1 |
| 40 | jpp | '6' | 0 |
| 40 | rest | '8' | 1 |
| 44 | whole | '8' | 1 |
| 44 | no_jpp | '6' | 0 |
| 44 | no_rand | '8' | 1 |
| 44 | jpp | '6' | 0 |
| 44 | rest | '6' | 0 |

### P2-L0-0133 (elements): bridge carbon → oxygen

O's context: The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked carbon. Eva picked helium.

S's context: The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked carbon. Eric picked oxygen. Eva picked helium.

**lookup** (Which locker belongs to Eric's pick?): O's answer 3, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 32 | whole | '7' | 1 |
| 32 | no_jpp | '7' | 1 |
| 32 | no_rand | '7' | 1 |
| 32 | jpp | '3' | 0 |
| 32 | rest | '7' | 1 |
| 33 | whole | '7' | 1 |
| 33 | no_jpp | '7' | 1 |
| 33 | no_rand | '7' | 1 |
| 33 | jpp | '3' | 0 |
| 33 | rest | '7' | 1 |

**recall** (What is the atomic number of Eric's pick?): O's answer 6, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 40 | whole | '8' | 1 |
| 40 | no_jpp | '8' | 1 |
| 40 | no_rand | '8' | 1 |
| 40 | jpp | '6' | 0 |
| 40 | rest | '8' | 1 |
| 44 | whole | '8' | 1 |
| 44 | no_jpp | '8' | 1 |
| 44 | no_rand | '8' | 1 |
| 44 | jpp | '6' | 0 |
| 44 | rest | '8' | 1 |

### P2-L0-0219 (animals): bridge sheep → butterfly

O's context: The locker of the sheep is 6. The locker of the butterfly is 7. Eve picked the butterfly. Owen picked the camel. The locker of the camel is 9. Diana picked the sheep.

S's context: The locker of the sheep is 6. The locker of the butterfly is 7. Eve picked the sheep. Owen picked the camel. The locker of the camel is 9. Diana picked the butterfly.

**lookup** (Which locker belongs to Diana's pick?): O's answer 6, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 32 | whole | '7' | 1 |
| 32 | no_jpp | '7' | 1 |
| 32 | no_rand | '7' | 1 |
| 32 | jpp | '6' | 0 |
| 32 | rest | '7' | 1 |
| 33 | whole | '7' | 1 |
| 33 | no_jpp | '7' | 1 |
| 33 | no_rand | '7' | 1 |
| 33 | jpp | '6' | 0 |
| 33 | rest | '7' | 1 |

**recall** (How many legs does Diana's pick have?): O's answer 4, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 40 | whole | '6' | 1 |
| 40 | no_jpp | '6' | 1 |
| 40 | no_rand | '6' | 1 |
| 40 | jpp | '4' | 0 |
| 40 | rest | '6' | 1 |
| 44 | whole | '6' | 1 |
| 44 | no_jpp | '4' | 0 |
| 44 | no_rand | '6' | 1 |
| 44 | jpp | '4' | 0 |
| 44 | rest | '4' | 0 |

### P2-L0-0221 (greek): bridge beta → delta

O's context: The locker of delta is nine. The locker of beta is one. Owen picked iota. Iris picked beta. The locker of iota is five. Mark picked delta.

S's context: The locker of delta is nine. The locker of beta is one. Owen picked iota. Iris picked delta. The locker of iota is five. Mark picked beta.

**lookup** (Which locker belongs to Iris's pick?): O's answer 1, S's answer 9

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '1' | 0 |
| 32 | whole | '9' | 1 |
| 32 | no_jpp | '9' | 1 |
| 32 | no_rand | '9' | 1 |
| 32 | jpp | '1' | 0 |
| 32 | rest | '9' | 1 |
| 33 | whole | '9' | 1 |
| 33 | no_jpp | '9' | 1 |
| 33 | no_rand | '9' | 1 |
| 33 | jpp | '1' | 0 |
| 33 | rest | '9' | 1 |

**recall** (Which position in the Greek alphabet does Iris's pick have?): O's answer 2, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 40 | whole | '4' | 1 |
| 40 | no_jpp | '4' | 1 |
| 40 | no_rand | '4' | 1 |
| 40 | jpp | '2' | 0 |
| 40 | rest | '4' | 1 |
| 44 | whole | '4' | 1 |
| 44 | no_jpp | '1' | 0 |
| 44 | no_rand | '4' | 1 |
| 44 | jpp | '2' | 0 |
| 44 | rest | '1' | 0 |

### P2-L0-0243 (animals): bridge spider → tiger

O's context: The locker of the spider is four. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the spider. Alice picked the tiger. Henry picked the sheep.

S's context: The locker of the spider is four. The locker of the tiger is six. The locker of the sheep is eight. Olivia picked the tiger. Alice picked the spider. Henry picked the sheep.

**lookup** (Which locker belongs to Olivia's pick?): O's answer 4, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 32 | whole | '6' | 1 |
| 32 | no_jpp | '6' | 1 |
| 32 | no_rand | '6' | 1 |
| 32 | jpp | '4' | 0 |
| 32 | rest | '6' | 1 |
| 33 | whole | '6' | 1 |
| 33 | no_jpp | '6' | 1 |
| 33 | no_rand | '6' | 1 |
| 33 | jpp | '4' | 0 |
| 33 | rest | '6' | 1 |

**recall** (How many legs does Olivia's pick have?): O's answer 8, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '8' | 0 |
| 40 | whole | '4' | 1 |
| 40 | no_jpp | '4' | 1 |
| 40 | no_rand | '4' | 1 |
| 40 | jpp | '8' | 0 |
| 40 | rest | '4' | 1 |
| 44 | whole | '4' | 1 |
| 44 | no_jpp | '8' | 0 |
| 44 | no_rand | '4' | 1 |
| 44 | jpp | '8' | 0 |
| 44 | rest | '8' | 0 |

### P2-L0-0255 (animals): bridge chicken → frog

O's context: The locker of the frog is three. Frank picked the beetle. The locker of the chicken is one. Iris picked the chicken. The locker of the beetle is five. Nina picked the frog.

S's context: The locker of the frog is three. Frank picked the beetle. The locker of the chicken is one. Iris picked the frog. The locker of the beetle is five. Nina picked the chicken.

**lookup** (Which locker belongs to Iris's pick?): O's answer 1, S's answer 3

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '1' | 0 |
| 32 | whole | '3' | 1 |
| 32 | no_jpp | '3' | 1 |
| 32 | no_rand | '3' | 1 |
| 32 | jpp | '1' | 0 |
| 32 | rest | '3' | 1 |
| 33 | whole | '3' | 1 |
| 33 | no_jpp | '3' | 1 |
| 33 | no_rand | '3' | 1 |
| 33 | jpp | '1' | 0 |
| 33 | rest | '3' | 1 |

**recall** (How many legs does Iris's pick have?): O's answer 2, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 40 | whole | '4' | 1 |
| 40 | no_jpp | '2' | 0 |
| 40 | no_rand | '4' | 1 |
| 40 | jpp | '2' | 0 |
| 40 | rest | '2' | 0 |
| 44 | whole | '4' | 1 |
| 44 | no_jpp | '2' | 0 |
| 44 | no_rand | '4' | 1 |
| 44 | jpp | '2' | 0 |
| 44 | rest | '2' | 0 |

### P2-L0-0273 (animals): bridge fox → turkey

O's context: The locker of the turkey is 4. The locker of the fox is 6. Tom picked the frog. The locker of the frog is 7. Finn picked the fox. Sean picked the turkey.

S's context: The locker of the turkey is 4. The locker of the fox is 6. Tom picked the frog. The locker of the frog is 7. Finn picked the turkey. Sean picked the fox.

**lookup** (Which locker belongs to Finn's pick?): O's answer 6, S's answer 4

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 32 | whole | '4' | 1 |
| 32 | no_jpp | '4' | 1 |
| 32 | no_rand | '4' | 1 |
| 32 | jpp | '6' | 0 |
| 32 | rest | '4' | 1 |
| 33 | whole | '4' | 1 |
| 33 | no_jpp | '4' | 1 |
| 33 | no_rand | '4' | 1 |
| 33 | jpp | '6' | 0 |
| 33 | rest | '4' | 1 |

**recall** (How many legs does Finn's pick have?): O's answer 4, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 40 | whole | '2' | 1 |
| 40 | no_jpp | '2' | 1 |
| 40 | no_rand | '2' | 1 |
| 40 | jpp | '10' | 0 |
| 40 | rest | '2' | 1 |
| 44 | whole | '2' | 1 |
| 44 | no_jpp | '2' | 1 |
| 44 | no_rand | '2' | 1 |
| 44 | jpp | '4' | 0 |
| 44 | rest | '2' | 1 |

### P2-L0-0287 (greek): bridge gamma → theta

O's context: Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked gamma. Ryan picked theta. The locker of epsilon is eight.

S's context: Emma picked epsilon. The locker of gamma is four. The locker of theta is five. Ella picked theta. Ryan picked gamma. The locker of epsilon is eight.

**lookup** (Which locker belongs to Ella's pick?): O's answer 4, S's answer 5

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 32 | whole | '5' | 1 |
| 32 | no_jpp | '5' | 1 |
| 32 | no_rand | '5' | 1 |
| 32 | jpp | '4' | 0 |
| 32 | rest | '5' | 1 |
| 33 | whole | '5' | 1 |
| 33 | no_jpp | '5' | 1 |
| 33 | no_rand | '5' | 1 |
| 33 | jpp | '4' | 0 |
| 33 | rest | '5' | 1 |

**recall** (Which position in the Greek alphabet does Ella's pick have?): O's answer 3, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 40 | whole | '8' | 1 |
| 40 | no_jpp | '8' | 1 |
| 40 | no_rand | '8' | 1 |
| 40 | jpp | '3' | 0 |
| 40 | rest | '8' | 1 |
| 44 | whole | '8' | 1 |
| 44 | no_jpp | '4' | 0 |
| 44 | no_rand | '4' | 0 |
| 44 | jpp | '3' | 0 |
| 44 | rest | '4' | 0 |

## nem35l_x53_3: 10 random items of 59 (seed 0)

### P2-L0-0046 (elements): bridge carbon → nitrogen

O's context: Laura picked lithium. The locker of nitrogen is six. The locker of carbon is nine. Kyle picked carbon. The locker of lithium is eight. Mark picked nitrogen.

S's context: Laura picked lithium. The locker of nitrogen is six. The locker of carbon is nine. Kyle picked nitrogen. The locker of lithium is eight. Mark picked carbon.

**lookup** (Which locker belongs to Kyle's pick?): O's answer 9, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '9' | 0 |
| 32 | whole | '6' | 1 |
| 32 | no_jpp | '6' | 1 |
| 32 | no_rand | '6' | 1 |
| 32 | jpp | '9' | 0 |
| 32 | rest | '6' | 1 |
| 43 | whole | '6' | 1 |
| 43 | no_jpp | '9' | 0 |
| 43 | no_rand | '6' | 1 |
| 43 | jpp | '9' | 0 |
| 43 | rest | '9' | 0 |

**recall** (What is the atomic number of Kyle's pick?): O's answer 6, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 36 | whole | '7' | 1 |
| 36 | no_jpp | '6' | 0 |
| 36 | no_rand | '7' | 1 |
| 36 | jpp | '9' | 0 |
| 36 | rest | '6' | 0 |
| 47 | whole | '7' | 1 |
| 47 | no_jpp | '6' | 0 |
| 47 | no_rand | '7' | 1 |
| 47 | jpp | '7' | 1 |
| 47 | rest | '6' | 0 |

### P2-L0-0161 (greek): bridge eta → epsilon

O's context: The locker of gamma is two. Laura picked gamma. The locker of epsilon is seven. The locker of eta is five. Ella picked eta. Zoe picked epsilon.

S's context: The locker of gamma is two. Laura picked gamma. The locker of epsilon is seven. The locker of eta is five. Ella picked epsilon. Zoe picked eta.

**lookup** (Which locker belongs to Ella's pick?): O's answer 5, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '5' | 0 |
| 32 | whole | '7' | 1 |
| 32 | no_jpp | '7' | 1 |
| 32 | no_rand | '7' | 1 |
| 32 | jpp | '5' | 0 |
| 32 | rest | '7' | 1 |
| 43 | whole | '7' | 1 |
| 43 | no_jpp | '7' | 1 |
| 43 | no_rand | '7' | 1 |
| 43 | jpp | '5' | 0 |
| 43 | rest | '7' | 1 |

**recall** (Which position in the Greek alphabet does Ella's pick have?): O's answer 7, S's answer 5

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '5' | 1 |
| 36 | whole | '5' | 1 |
| 36 | no_jpp | '5' | 1 |
| 36 | no_rand | '5' | 1 |
| 36 | jpp | '5' | 1 |
| 36 | rest | '5' | 1 |
| 47 | whole | '5' | 1 |
| 47 | no_jpp | '5' | 1 |
| 47 | no_rand | '5' | 1 |
| 47 | jpp | '5' | 1 |
| 47 | rest | '5' | 1 |

### P2-L0-0170 (greek): bridge delta → eta

O's context: Finn picked eta. The locker of delta is two. The locker of epsilon is nine. The locker of eta is five. Amy picked epsilon. Mia picked delta.

S's context: Finn picked delta. The locker of delta is two. The locker of epsilon is nine. The locker of eta is five. Amy picked epsilon. Mia picked eta.

**lookup** (Which locker belongs to Mia's pick?): O's answer 2, S's answer 5

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '2' | 0 |
| 32 | whole | '9' | 0 |
| 32 | no_jpp | '9' | 0 |
| 32 | no_rand | '9' | 0 |
| 32 | jpp | '2' | 0 |
| 32 | rest | '9' | 0 |
| 43 | whole | '5' | 1 |
| 43 | no_jpp | '2' | 0 |
| 43 | no_rand | '5' | 1 |
| 43 | jpp | '2' | 0 |
| 43 | rest | '2' | 0 |

**recall** (Which position in the Greek alphabet does Mia's pick have?): O's answer 4, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 36 | whole | '8' | 0 |
| 36 | no_jpp | '4' | 0 |
| 36 | no_rand | '8' | 0 |
| 36 | jpp | '4' | 0 |
| 36 | rest | '4' | 0 |
| 47 | whole | '7' | 1 |
| 47 | no_jpp | '4' | 0 |
| 47 | no_rand | '7' | 1 |
| 47 | jpp | '7' | 1 |
| 47 | rest | '4' | 0 |

### P2-L0-0207 (animals): bridge rabbit → owl

O's context: The locker of the rabbit is 9. The locker of the owl is 8. The locker of the sheep is 2. Anna picked the sheep. Jack picked the owl. Eva picked the rabbit.

S's context: The locker of the rabbit is 9. The locker of the owl is 8. The locker of the sheep is 2. Anna picked the sheep. Jack picked the rabbit. Eva picked the owl.

**lookup** (Which locker belongs to Eva's pick?): O's answer 9, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '9' | 0 |
| 32 | whole | '8' | 1 |
| 32 | no_jpp | '8' | 1 |
| 32 | no_rand | '8' | 1 |
| 32 | jpp | '9' | 0 |
| 32 | rest | '8' | 1 |
| 43 | whole | '8' | 1 |
| 43 | no_jpp | '8' | 1 |
| 43 | no_rand | '8' | 1 |
| 43 | jpp | '9' | 0 |
| 43 | rest | '8' | 1 |

**recall** (How many legs does Eva's pick have?): O's answer 4, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 36 | whole | '2' | 1 |
| 36 | no_jpp | '2' | 1 |
| 36 | no_rand | '2' | 1 |
| 36 | jpp | '4' | 0 |
| 36 | rest | '2' | 1 |
| 47 | whole | '2' | 1 |
| 47 | no_jpp | '4' | 0 |
| 47 | no_rand | '2' | 1 |
| 47 | jpp | '2' | 1 |
| 47 | rest | '4' | 0 |

### P2-L0-0223 (elements): bridge hydrogen → nitrogen

O's context: The locker of nitrogen is 6. The locker of lithium is 1. The locker of hydrogen is 4. Olivia picked nitrogen. David picked hydrogen. Maria picked lithium.

S's context: The locker of nitrogen is 6. The locker of lithium is 1. The locker of hydrogen is 4. Olivia picked hydrogen. David picked nitrogen. Maria picked lithium.

**lookup** (Which locker belongs to David's pick?): O's answer 4, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 32 | whole | '6' | 1 |
| 32 | no_jpp | '6' | 1 |
| 32 | no_rand | '6' | 1 |
| 32 | jpp | '4' | 0 |
| 32 | rest | '6' | 1 |
| 43 | whole | '6' | 1 |
| 43 | no_jpp | '4' | 0 |
| 43 | no_rand | '6' | 1 |
| 43 | jpp | '4' | 0 |
| 43 | rest | '4' | 0 |

**recall** (What is the atomic number of David's pick?): O's answer 1, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '1' | 0 |
| 36 | whole | '7' | 1 |
| 36 | no_jpp | '7' | 1 |
| 36 | no_rand | '7' | 1 |
| 36 | jpp | '1' | 0 |
| 36 | rest | '7' | 1 |
| 47 | whole | '7' | 1 |
| 47 | no_jpp | '4' | 0 |
| 47 | no_rand | '7' | 1 |
| 47 | jpp | '1' | 0 |
| 47 | rest | '4' | 0 |

### P2-L0-0225 (animals): bridge rabbit → fly

O's context: The locker of the rabbit is 9. The locker of the fly is 3. Liam picked the spider. Lily picked the fly. The locker of the spider is 4. Carl picked the rabbit.

S's context: The locker of the rabbit is 9. The locker of the fly is 3. Liam picked the spider. Lily picked the rabbit. The locker of the spider is 4. Carl picked the fly.

**lookup** (Which locker belongs to Carl's pick?): O's answer 9, S's answer 3

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '9' | 0 |
| 32 | whole | '3' | 1 |
| 32 | no_jpp | '3' | 1 |
| 32 | no_rand | '3' | 1 |
| 32 | jpp | '9' | 0 |
| 32 | rest | '3' | 1 |
| 43 | whole | '3' | 1 |
| 43 | no_jpp | '3' | 1 |
| 43 | no_rand | '3' | 1 |
| 43 | jpp | '9' | 0 |
| 43 | rest | '3' | 1 |

**recall** (How many legs does Carl's pick have?): O's answer 4, S's answer 6

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 36 | whole | '6' | 1 |
| 36 | no_jpp | '6' | 1 |
| 36 | no_rand | '6' | 1 |
| 36 | jpp | '4' | 0 |
| 36 | rest | '6' | 1 |
| 47 | whole | '6' | 1 |
| 47 | no_jpp | '4' | 0 |
| 47 | no_rand | '6' | 1 |
| 47 | jpp | '6' | 1 |
| 47 | rest | '4' | 0 |

### P2-L0-0252 (animals): bridge sheep → spider

O's context: Victor picked the spider. The locker of the sheep is 9. Luke picked the butterfly. The locker of the spider is 7. Rose picked the sheep. The locker of the butterfly is 3.

S's context: Victor picked the sheep. The locker of the sheep is 9. Luke picked the butterfly. The locker of the spider is 7. Rose picked the spider. The locker of the butterfly is 3.

**lookup** (Which locker belongs to Rose's pick?): O's answer 9, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '9' | 0 |
| 32 | whole | '3' | 0 |
| 32 | no_jpp | '3' | 0 |
| 32 | no_rand | '3' | 0 |
| 32 | jpp | '9' | 0 |
| 32 | rest | '3' | 0 |
| 43 | whole | '7' | 1 |
| 43 | no_jpp | '9' | 0 |
| 43 | no_rand | '7' | 1 |
| 43 | jpp | '9' | 0 |
| 43 | rest | '9' | 0 |

**recall** (How many legs does Rose's pick have?): O's answer 4, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 36 | whole | '8' | 1 |
| 36 | no_jpp | '8' | 1 |
| 36 | no_rand | '8' | 1 |
| 36 | jpp | '8' | 1 |
| 36 | rest | '8' | 1 |
| 47 | whole | '8' | 1 |
| 47 | no_jpp | '4' | 0 |
| 47 | no_rand | '8' | 1 |
| 47 | jpp | '8' | 1 |
| 47 | rest | '4' | 0 |

### P2-L0-0256 (elements): bridge lithium → hydrogen

O's context: The locker of hydrogen is 2. Victor picked helium. The locker of lithium is 7. David picked hydrogen. The locker of helium is 9. Sara picked lithium.

S's context: The locker of hydrogen is 2. Victor picked helium. The locker of lithium is 7. David picked lithium. The locker of helium is 9. Sara picked hydrogen.

**lookup** (Which locker belongs to Sara's pick?): O's answer 7, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '7' | 0 |
| 32 | whole | '2' | 1 |
| 32 | no_jpp | '2' | 1 |
| 32 | no_rand | '2' | 1 |
| 32 | jpp | '7' | 0 |
| 32 | rest | '2' | 1 |
| 43 | whole | '2' | 1 |
| 43 | no_jpp | '2' | 1 |
| 43 | no_rand | '2' | 1 |
| 43 | jpp | '7' | 0 |
| 43 | rest | '2' | 1 |

**recall** (What is the atomic number of Sara's pick?): O's answer 3, S's answer 1

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '3' | 0 |
| 36 | whole | '1' | 1 |
| 36 | no_jpp | '2' | 0 |
| 36 | no_rand | '1' | 1 |
| 36 | jpp | '3' | 0 |
| 36 | rest | '2' | 0 |
| 47 | whole | '1' | 1 |
| 47 | no_jpp | '1' | 1 |
| 47 | no_rand | '1' | 1 |
| 47 | jpp | '7' | 0 |
| 47 | rest | '1' | 1 |

### P2-L0-0403 (elements): bridge nitrogen → lithium

O's context: The locker of nitrogen is nine. Oscar picked helium. Sean picked lithium. The locker of lithium is eight. Rose picked nitrogen. The locker of helium is six.

S's context: The locker of nitrogen is nine. Oscar picked helium. Sean picked nitrogen. The locker of lithium is eight. Rose picked lithium. The locker of helium is six.

**lookup** (Which locker belongs to Rose's pick?): O's answer 9, S's answer 8

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '9' | 0 |
| 32 | whole | '8' | 1 |
| 32 | no_jpp | '8' | 1 |
| 32 | no_rand | '8' | 1 |
| 32 | jpp | '9' | 0 |
| 32 | rest | '8' | 1 |
| 43 | whole | '8' | 1 |
| 43 | no_jpp | '8' | 1 |
| 43 | no_rand | '8' | 1 |
| 43 | jpp | '8' | 1 |
| 43 | rest | '8' | 1 |

**recall** (What is the atomic number of Rose's pick?): O's answer 7, S's answer 3

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '7' | 0 |
| 36 | whole | '3' | 1 |
| 36 | no_jpp | '7' | 0 |
| 36 | no_rand | '7' | 0 |
| 36 | jpp | '7' | 0 |
| 36 | rest | '7' | 0 |
| 47 | whole | '3' | 1 |
| 47 | no_jpp | '7' | 0 |
| 47 | no_rand | '3' | 1 |
| 47 | jpp | '3' | 1 |
| 47 | rest | '7' | 0 |

### P2-L0-0426 (animals): bridge mouse → crow

O's context: The locker of the mouse is 6. The locker of the ant is 1. The locker of the crow is 7. David picked the mouse. Victor picked the ant. Beth picked the crow.

S's context: The locker of the mouse is 6. The locker of the ant is 1. The locker of the crow is 7. David picked the crow. Victor picked the ant. Beth picked the mouse.

**lookup** (Which locker belongs to David's pick?): O's answer 6, S's answer 7

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '6' | 0 |
| 32 | whole | '6' | 0 |
| 32 | no_jpp | '6' | 0 |
| 32 | no_rand | '6' | 0 |
| 32 | jpp | '6' | 0 |
| 32 | rest | '6' | 0 |
| 43 | whole | '7' | 1 |
| 43 | no_jpp | '6' | 0 |
| 43 | no_rand | '6' | 0 |
| 43 | jpp | '6' | 0 |
| 43 | rest | '6' | 0 |

**recall** (How many legs does David's pick have?): O's answer 4, S's answer 2

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | '4' | 0 |
| 36 | whole | '2' | 1 |
| 36 | no_jpp | '4' | 0 |
| 36 | no_rand | '2' | 1 |
| 36 | jpp | '6' | 0 |
| 36 | rest | '4' | 0 |
| 47 | whole | '2' | 1 |
| 47 | no_jpp | '4' | 0 |
| 47 | no_rand | '2' | 1 |
| 47 | jpp | '6' | 0 |
| 47 | rest | '4' | 0 |

