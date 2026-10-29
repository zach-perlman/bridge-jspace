# 53.3 examples (verify pack): every arm's top token per layer for 10 random items per run. UNVERIFIED.

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

