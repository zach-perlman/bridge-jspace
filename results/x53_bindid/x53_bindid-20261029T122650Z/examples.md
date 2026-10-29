# 53.8 examples (verify pack): the scene's slots, O and S_B, every arm's top token. UNVERIFIED.

## qwen35_9b_x53_8c: 10 random scenes of 300 (seed 0)

### C0-0035: A = goat (slot 2), B = beetle (slot 0); slot 0: beetle (locker 2); slot 1: tiger (locker 4); slot 2: goat (locker 9)

O: The locker of the beetle is 2. The locker of the tiger is 4. The locker of the goat is 9. Leo picked the tiger. Amy picked the beetle. Ivan picked the goat.

S_B: The locker of the beetle is 2. The locker of the tiger is 4. The locker of the goat is 9. Leo picked the tiger. Amy picked the beetle. Ivan picked the beetle.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '9' | 2 | 1 |
| lookup | whole | '2' | 0 | 0 |
| lookup | code0_x1 | '9' | 2 | 1 |
| lookup | code1_x1 | '9' | 2 | 1 |
| lookup | rand_x1 | '9' | 2 | 1 |
| lookup | ccode0_x1 | '9' | 2 | 1 |
| lookup | ccode1_x1 | '9' | 2 | 1 |
| lookup | code0_x2 | '9' | 2 | 1 |
| lookup | code1_x2 | '9' | 2 | 1 |
| lookup | rand_x2 | '9' | 2 | 1 |
| lookup | ccode0_x2 | '9' | 2 | 1 |
| lookup | ccode1_x2 | '9' | 2 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '6' | - | 0 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code1_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | rand_x2 | '6' | - | 0 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode1_x2 | '4' | - | 1 |

### C0-0231: A = pig (slot 1), B = butterfly (slot 0); slot 0: butterfly (locker 7); slot 1: pig (locker 1); slot 2: beetle (locker 3)

O: The locker of the butterfly is 7. The locker of the pig is 1. The locker of the beetle is 3. Paul picked the butterfly. Vera picked the pig. Mark picked the beetle.

S_B: The locker of the butterfly is 7. The locker of the pig is 1. The locker of the beetle is 3. Paul picked the butterfly. Vera picked the butterfly. Mark picked the beetle.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '1' | 1 | 1 |
| lookup | whole | '7' | 0 | 0 |
| lookup | code0_x1 | '1' | 1 | 1 |
| lookup | code2_x1 | '1' | 1 | 1 |
| lookup | rand_x1 | '1' | 1 | 1 |
| lookup | ccode0_x1 | '1' | 1 | 1 |
| lookup | ccode2_x1 | '1' | 1 | 1 |
| lookup | code0_x2 | '1' | 1 | 1 |
| lookup | code2_x2 | '1' | 1 | 1 |
| lookup | rand_x2 | '1' | 1 | 1 |
| lookup | ccode0_x2 | '1' | 1 | 1 |
| lookup | ccode2_x2 | '1' | 1 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '6' | - | 0 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code2_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode2_x2 | '4' | - | 1 |

### C0-0275: A = rabbit (slot 2), B = spider (slot 0); slot 0: spider (locker 6); slot 1: goose (locker 5); slot 2: rabbit (locker 3)

O: The locker of the spider is 6. The locker of the goose is 5. The locker of the rabbit is 3. Mark picked the rabbit. Kate picked the goose. Carl picked the spider.

S_B: The locker of the spider is 6. The locker of the goose is 5. The locker of the rabbit is 3. Mark picked the spider. Kate picked the goose. Carl picked the spider.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '3' | 2 | 1 |
| lookup | whole | '6' | 0 | 0 |
| lookup | code0_x1 | '3' | 2 | 1 |
| lookup | code1_x1 | '3' | 2 | 1 |
| lookup | rand_x1 | '3' | 2 | 1 |
| lookup | ccode0_x1 | '3' | 2 | 1 |
| lookup | ccode1_x1 | '3' | 2 | 1 |
| lookup | code0_x2 | '3' | 2 | 1 |
| lookup | code1_x2 | '3' | 2 | 1 |
| lookup | rand_x2 | '3' | 2 | 1 |
| lookup | ccode0_x2 | '3' | 2 | 1 |
| lookup | ccode1_x2 | '3' | 2 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '8' | - | 0 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code1_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | rand_x2 | '6' | - | 0 |
| recall | ccode0_x2 | '6' | - | 0 |
| recall | ccode1_x2 | '4' | - | 1 |

### C0-0334: A = spider (slot 0), B = elephant (slot 2); slot 0: spider (locker 5); slot 1: rabbit (locker 2); slot 2: elephant (locker 4)

O: The locker of the spider is 5. The locker of the rabbit is 2. The locker of the elephant is 4. Tara picked the rabbit. Adam picked the elephant. Ruby picked the spider.

S_B: The locker of the spider is 5. The locker of the rabbit is 2. The locker of the elephant is 4. Tara picked the rabbit. Adam picked the elephant. Ruby picked the elephant.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '5' | 0 | 1 |
| lookup | whole | '4' | 2 | 0 |
| lookup | code1_x1 | '5' | 0 | 1 |
| lookup | code2_x1 | '5' | 0 | 1 |
| lookup | rand_x1 | '5' | 0 | 1 |
| lookup | ccode1_x1 | '5' | 0 | 1 |
| lookup | ccode2_x1 | '5' | 0 | 1 |
| lookup | code1_x2 | '5' | 0 | 1 |
| lookup | code2_x2 | '5' | 0 | 1 |
| lookup | rand_x2 | '5' | 0 | 1 |
| lookup | ccode1_x2 | '2' | 1 | 0 |
| lookup | ccode2_x2 | '5' | 0 | 1 |
| recall | none | '8' | - | 1 |
| recall | whole | '4' | - | 0 |
| recall | code1_x1 | '8' | - | 1 |
| recall | code2_x1 | '8' | - | 1 |
| recall | rand_x1 | '8' | - | 1 |
| recall | ccode1_x1 | '8' | - | 1 |
| recall | ccode2_x1 | '8' | - | 1 |
| recall | code1_x2 | '8' | - | 1 |
| recall | code2_x2 | '8' | - | 1 |
| recall | rand_x2 | '8' | - | 1 |
| recall | ccode1_x2 | '8' | - | 1 |
| recall | ccode2_x2 | '8' | - | 1 |

### C0-0364: A = fly (slot 0), B = pig (slot 2); slot 0: fly (locker 5); slot 1: duck (locker 6); slot 2: pig (locker 4)

O: The locker of the fly is 5. The locker of the duck is 6. The locker of the pig is 4. Ben picked the duck. James picked the pig. Victor picked the fly.

S_B: The locker of the fly is 5. The locker of the duck is 6. The locker of the pig is 4. Ben picked the duck. James picked the pig. Victor picked the pig.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '5' | 0 | 1 |
| lookup | whole | '4' | 2 | 0 |
| lookup | code1_x1 | '5' | 0 | 1 |
| lookup | code2_x1 | '5' | 0 | 1 |
| lookup | rand_x1 | '5' | 0 | 1 |
| lookup | ccode1_x1 | '5' | 0 | 1 |
| lookup | ccode2_x1 | '5' | 0 | 1 |
| lookup | code1_x2 | '5' | 0 | 1 |
| lookup | code2_x2 | '5' | 0 | 1 |
| lookup | rand_x2 | '5' | 0 | 1 |
| lookup | ccode1_x2 | '5' | 0 | 1 |
| lookup | ccode2_x2 | '5' | 0 | 1 |
| recall | none | '6' | - | 1 |
| recall | whole | '4' | - | 0 |
| recall | code1_x1 | '6' | - | 1 |
| recall | code2_x1 | '6' | - | 1 |
| recall | rand_x1 | '6' | - | 1 |
| recall | ccode1_x1 | '6' | - | 1 |
| recall | ccode2_x1 | '6' | - | 1 |
| recall | code1_x2 | '6' | - | 1 |
| recall | code2_x2 | '6' | - | 1 |
| recall | rand_x2 | '6' | - | 1 |
| recall | ccode1_x2 | '6' | - | 1 |
| recall | ccode2_x2 | '6' | - | 1 |

### C0-0378: A = duck (slot 2), B = deer (slot 1); slot 0: fox (locker 9); slot 1: deer (locker 1); slot 2: duck (locker 4)

O: The locker of the fox is 9. The locker of the deer is 1. The locker of the duck is 4. Kate picked the duck. Paul picked the fox. Vera picked the deer.

S_B: The locker of the fox is 9. The locker of the deer is 1. The locker of the duck is 4. Kate picked the deer. Paul picked the fox. Vera picked the deer.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '4' | 2 | 1 |
| lookup | whole | '1' | 1 | 0 |
| lookup | code0_x1 | '4' | 2 | 1 |
| lookup | code1_x1 | '4' | 2 | 1 |
| lookup | rand_x1 | '4' | 2 | 1 |
| lookup | ccode0_x1 | '4' | 2 | 1 |
| lookup | ccode1_x1 | '4' | 2 | 1 |
| lookup | code0_x2 | '4' | 2 | 1 |
| lookup | code1_x2 | '4' | 2 | 1 |
| lookup | rand_x2 | '4' | 2 | 1 |
| lookup | ccode0_x2 | '4' | 2 | 1 |
| lookup | ccode1_x2 | '4' | 2 | 1 |
| recall | none | '2' | - | 1 |
| recall | whole | '4' | - | 0 |
| recall | code0_x1 | '2' | - | 1 |
| recall | code1_x1 | '2' | - | 1 |
| recall | rand_x1 | '2' | - | 1 |
| recall | ccode0_x1 | '2' | - | 1 |
| recall | ccode1_x1 | '2' | - | 1 |
| recall | code0_x2 | '2' | - | 1 |
| recall | code1_x2 | '2' | - | 1 |
| recall | rand_x2 | '2' | - | 1 |
| recall | ccode0_x2 | '2' | - | 1 |
| recall | ccode1_x2 | '2' | - | 1 |

### C0-0391: A = fox (slot 1), B = owl (slot 0); slot 0: owl (locker 7); slot 1: fox (locker 6); slot 2: turkey (locker 1)

O: The locker of the owl is 7. The locker of the fox is 6. The locker of the turkey is 1. Ivy picked the turkey. Eva picked the fox. Jack picked the owl.

S_B: The locker of the owl is 7. The locker of the fox is 6. The locker of the turkey is 1. Ivy picked the turkey. Eva picked the owl. Jack picked the owl.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '6' | 1 | 1 |
| lookup | whole | '7' | 0 | 0 |
| lookup | code0_x1 | '6' | 1 | 1 |
| lookup | code2_x1 | '6' | 1 | 1 |
| lookup | rand_x1 | '6' | 1 | 1 |
| lookup | ccode0_x1 | '6' | 1 | 1 |
| lookup | ccode2_x1 | '6' | 1 | 1 |
| lookup | code0_x2 | '6' | 1 | 1 |
| lookup | code2_x2 | '6' | 1 | 1 |
| lookup | rand_x2 | '6' | 1 | 1 |
| lookup | ccode0_x2 | '6' | 1 | 1 |
| lookup | ccode2_x2 | '6' | 1 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '2' | - | 0 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code2_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode2_x2 | '4' | - | 1 |

### C0-0444: A = goose (slot 2), B = pig (slot 0); slot 0: pig (locker 5); slot 1: crow (locker 1); slot 2: goose (locker 4)

O: The locker of the pig is 5. The locker of the crow is 1. The locker of the goose is 4. Anna picked the goose. Owen picked the crow. Lucy picked the pig.

S_B: The locker of the pig is 5. The locker of the crow is 1. The locker of the goose is 4. Anna picked the pig. Owen picked the crow. Lucy picked the pig.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '4' | 2 | 1 |
| lookup | whole | '5' | 0 | 0 |
| lookup | code0_x1 | '4' | 2 | 1 |
| lookup | code1_x1 | '4' | 2 | 1 |
| lookup | rand_x1 | '4' | 2 | 1 |
| lookup | ccode0_x1 | '4' | 2 | 1 |
| lookup | ccode1_x1 | '4' | 2 | 1 |
| lookup | code0_x2 | '4' | 2 | 1 |
| lookup | code1_x2 | '4' | 2 | 1 |
| lookup | rand_x2 | '4' | 2 | 1 |
| lookup | ccode0_x2 | '4' | 2 | 1 |
| lookup | ccode1_x2 | '1' | 1 | 0 |
| recall | none | '2' | - | 1 |
| recall | whole | '4' | - | 0 |
| recall | code0_x1 | '2' | - | 1 |
| recall | code1_x1 | '2' | - | 1 |
| recall | rand_x1 | '2' | - | 1 |
| recall | ccode0_x1 | '2' | - | 1 |
| recall | ccode1_x1 | '2' | - | 1 |
| recall | code0_x2 | '2' | - | 1 |
| recall | code1_x2 | '2' | - | 1 |
| recall | rand_x2 | '2' | - | 1 |
| recall | ccode0_x2 | '2' | - | 1 |
| recall | ccode1_x2 | '2' | - | 1 |

### C0-0448: A = horse (slot 2), B = owl (slot 1); slot 0: tick (locker 3); slot 1: owl (locker 7); slot 2: horse (locker 5)

O: The locker of the tick is 3. The locker of the owl is 7. The locker of the horse is 5. David picked the tick. Ivan picked the horse. Henry picked the owl.

S_B: The locker of the tick is 3. The locker of the owl is 7. The locker of the horse is 5. David picked the tick. Ivan picked the owl. Henry picked the owl.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '5' | 2 | 1 |
| lookup | whole | '7' | 1 | 0 |
| lookup | code0_x1 | '5' | 2 | 1 |
| lookup | code1_x1 | '5' | 2 | 1 |
| lookup | rand_x1 | '5' | 2 | 1 |
| lookup | ccode0_x1 | '5' | 2 | 1 |
| lookup | ccode1_x1 | '5' | 2 | 1 |
| lookup | code0_x2 | '5' | 2 | 1 |
| lookup | code1_x2 | '5' | 2 | 1 |
| lookup | rand_x2 | '5' | 2 | 1 |
| lookup | ccode0_x2 | '5' | 2 | 1 |
| lookup | ccode1_x2 | '5' | 2 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '2' | - | 0 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code1_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '6' | - | 0 |
| recall | ccode1_x2 | '4' | - | 1 |

### C0-0477: A = crow (slot 2), B = beetle (slot 1); slot 0: cow (locker 7); slot 1: beetle (locker 8); slot 2: crow (locker 6)

O: The locker of the cow is 7. The locker of the beetle is 8. The locker of the crow is 6. Grace picked the cow. Eva picked the beetle. Liam picked the crow.

S_B: The locker of the cow is 7. The locker of the beetle is 8. The locker of the crow is 6. Grace picked the cow. Eva picked the beetle. Liam picked the beetle.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '6' | 2 | 1 |
| lookup | whole | '8' | 1 | 0 |
| lookup | code0_x1 | '6' | 2 | 1 |
| lookup | code1_x1 | '6' | 2 | 1 |
| lookup | rand_x1 | '6' | 2 | 1 |
| lookup | ccode0_x1 | '6' | 2 | 1 |
| lookup | ccode1_x1 | '6' | 2 | 1 |
| lookup | code0_x2 | '6' | 2 | 1 |
| lookup | code1_x2 | '6' | 2 | 1 |
| lookup | rand_x2 | '6' | 2 | 1 |
| lookup | ccode0_x2 | '6' | 2 | 1 |
| lookup | ccode1_x2 | '6' | 2 | 1 |
| recall | none | '2' | - | 1 |
| recall | whole | '6' | - | 0 |
| recall | code0_x1 | '2' | - | 1 |
| recall | code1_x1 | '2' | - | 1 |
| recall | rand_x1 | '2' | - | 1 |
| recall | ccode0_x1 | '2' | - | 1 |
| recall | ccode1_x1 | '2' | - | 1 |
| recall | code0_x2 | '2' | - | 1 |
| recall | code1_x2 | '2' | - | 1 |
| recall | rand_x2 | '2' | - | 1 |
| recall | ccode0_x2 | '2' | - | 1 |
| recall | ccode1_x2 | '2' | - | 1 |

## muse30_x53_8c: 10 random scenes of 300 (seed 0)

### C0-0040: A = bee (slot 2), B = zebra (slot 1); slot 0: rabbit (locker 5); slot 1: zebra (locker 3); slot 2: bee (locker 8)

O: The locker of the rabbit is 5. The locker of the zebra is 3. The locker of the bee is 8. Grace picked the zebra. Beth picked the bee. Dan picked the rabbit.

S_B: The locker of the rabbit is 5. The locker of the zebra is 3. The locker of the bee is 8. Grace picked the zebra. Beth picked the zebra. Dan picked the rabbit.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '8' | 2 | 1 |
| lookup | whole | '3' | 1 | 0 |
| lookup | code0_x1 | '3' | 1 | 0 |
| lookup | code1_x1 | '3' | 1 | 0 |
| lookup | rand_x1 | '8' | 2 | 1 |
| lookup | ccode0_x1 | '3' | 1 | 0 |
| lookup | ccode1_x1 | '3' | 1 | 0 |
| lookup | code0_x2 | '3' | 1 | 0 |
| lookup | code1_x2 | '3' | 1 | 0 |
| lookup | rand_x2 | '3' | 1 | 0 |
| lookup | ccode0_x2 | '3' | 1 | 0 |
| lookup | ccode1_x2 | '3' | 1 | 0 |
| recall | none | '6' | - | 1 |
| recall | whole | '6' | - | 1 |
| recall | code0_x1 | '6' | - | 1 |
| recall | code1_x1 | '6' | - | 1 |
| recall | rand_x1 | '6' | - | 1 |
| recall | ccode0_x1 | '6' | - | 1 |
| recall | ccode1_x1 | '6' | - | 1 |
| recall | code0_x2 | '6' | - | 1 |
| recall | code1_x2 | '6' | - | 1 |
| recall | rand_x2 | '6' | - | 1 |
| recall | ccode0_x2 | '6' | - | 1 |
| recall | ccode1_x2 | '6' | - | 1 |

### C0-0275: A = fly (slot 0), B = eagle (slot 2); slot 0: fly (locker 7); slot 1: sheep (locker 5); slot 2: eagle (locker 9)

O: The locker of the fly is 7. The locker of the sheep is 5. The locker of the eagle is 9. Ryan picked the sheep. Henry picked the fly. Laura picked the eagle.

S_B: The locker of the fly is 7. The locker of the sheep is 5. The locker of the eagle is 9. Ryan picked the sheep. Henry picked the eagle. Laura picked the eagle.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '7' | 0 | 1 |
| lookup | whole | '5' | 1 | 0 |
| lookup | code1_x1 | '7' | 0 | 1 |
| lookup | code2_x1 | '7' | 0 | 1 |
| lookup | rand_x1 | '7' | 0 | 1 |
| lookup | ccode1_x1 | '7' | 0 | 1 |
| lookup | ccode2_x1 | '5' | 1 | 0 |
| lookup | code1_x2 | '5' | 1 | 0 |
| lookup | code2_x2 | '5' | 1 | 0 |
| lookup | rand_x2 | '7' | 0 | 1 |
| lookup | ccode1_x2 | '5' | 1 | 0 |
| lookup | ccode2_x2 | '5' | 1 | 0 |
| recall | none | '6' | - | 1 |
| recall | whole | '6' | - | 1 |
| recall | code1_x1 | '6' | - | 1 |
| recall | code2_x1 | '6' | - | 1 |
| recall | rand_x1 | '6' | - | 1 |
| recall | ccode1_x1 | '6' | - | 1 |
| recall | ccode2_x1 | '2' | - | 0 |
| recall | code1_x2 | '6' | - | 1 |
| recall | code2_x2 | '6' | - | 1 |
| recall | rand_x2 | '6' | - | 1 |
| recall | ccode1_x2 | '6' | - | 1 |
| recall | ccode2_x2 | '6' | - | 1 |

### C0-0313: A = mouse (slot 0), B = butterfly (slot 2); slot 0: mouse (locker 4); slot 1: cow (locker 7); slot 2: butterfly (locker 9)

O: The locker of the mouse is 4. The locker of the cow is 7. The locker of the butterfly is 9. David picked the butterfly. Liam picked the cow. Clara picked the mouse.

S_B: The locker of the mouse is 4. The locker of the cow is 7. The locker of the butterfly is 9. David picked the butterfly. Liam picked the cow. Clara picked the butterfly.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '4' | 0 | 1 |
| lookup | whole | '9' | 2 | 0 |
| lookup | code1_x1 | '4' | 0 | 1 |
| lookup | code2_x1 | '4' | 0 | 1 |
| lookup | rand_x1 | '4' | 0 | 1 |
| lookup | ccode1_x1 | '4' | 0 | 1 |
| lookup | ccode2_x1 | '4' | 0 | 1 |
| lookup | code1_x2 | '9' | 2 | 0 |
| lookup | code2_x2 | '9' | 2 | 0 |
| lookup | rand_x2 | '4' | 0 | 1 |
| lookup | ccode1_x2 | '7' | 1 | 0 |
| lookup | ccode2_x2 | '9' | 2 | 0 |
| recall | none | '4' | - | 1 |
| recall | whole | '0' | - | 0 |
| recall | code1_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '0' | - | 0 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code1_x2 | '0' | - | 0 |
| recall | code2_x2 | '0' | - | 0 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode1_x2 | '0' | - | 0 |
| recall | ccode2_x2 | '0' | - | 0 |

### C0-0362: A = turkey (slot 1), B = bear (slot 0); slot 0: bear (locker 8); slot 1: turkey (locker 6); slot 2: duck (locker 2)

O: The locker of the bear is 8. The locker of the turkey is 6. The locker of the duck is 2. Dan picked the duck. Kyle picked the bear. Carl picked the turkey.

S_B: The locker of the bear is 8. The locker of the turkey is 6. The locker of the duck is 2. Dan picked the duck. Kyle picked the bear. Carl picked the bear.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '6' | 1 | 1 |
| lookup | whole | '8' | 0 | 0 |
| lookup | code0_x1 | '2' | 2 | 0 |
| lookup | code2_x1 | '2' | 2 | 0 |
| lookup | rand_x1 | '6' | 1 | 1 |
| lookup | ccode0_x1 | '2' | 2 | 0 |
| lookup | ccode2_x1 | '2' | 2 | 0 |
| lookup | code0_x2 | '2' | 2 | 0 |
| lookup | code2_x2 | '2' | 2 | 0 |
| lookup | rand_x2 | '2' | 2 | 0 |
| lookup | ccode0_x2 | '2' | 2 | 0 |
| lookup | ccode2_x2 | '2' | 2 | 0 |
| recall | none | '2' | - | 1 |
| recall | whole | '2' | - | 1 |
| recall | code0_x1 | '2' | - | 1 |
| recall | code2_x1 | '2' | - | 1 |
| recall | rand_x1 | '2' | - | 1 |
| recall | ccode0_x1 | '2' | - | 1 |
| recall | ccode2_x1 | '2' | - | 1 |
| recall | code0_x2 | '2' | - | 1 |
| recall | code2_x2 | '2' | - | 1 |
| recall | rand_x2 | '2' | - | 1 |
| recall | ccode0_x2 | '2' | - | 1 |
| recall | ccode2_x2 | '2' | - | 1 |

### C0-0393: A = spider (slot 2), B = crow (slot 1); slot 0: rabbit (locker 7); slot 1: crow (locker 5); slot 2: spider (locker 3)

O: The locker of the rabbit is 7. The locker of the crow is 5. The locker of the spider is 3. Iris picked the rabbit. Will picked the spider. Emma picked the crow.

S_B: The locker of the rabbit is 7. The locker of the crow is 5. The locker of the spider is 3. Iris picked the rabbit. Will picked the crow. Emma picked the crow.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '3' | 2 | 1 |
| lookup | whole | '5' | 1 | 0 |
| lookup | code0_x1 | '3' | 2 | 1 |
| lookup | code1_x1 | '3' | 2 | 1 |
| lookup | rand_x1 | '3' | 2 | 1 |
| lookup | ccode0_x1 | '3' | 2 | 1 |
| lookup | ccode1_x1 | '3' | 2 | 1 |
| lookup | code0_x2 | '7' | 0 | 0 |
| lookup | code1_x2 | '7' | 0 | 0 |
| lookup | rand_x2 | '3' | 2 | 1 |
| lookup | ccode0_x2 | '7' | 0 | 0 |
| lookup | ccode1_x2 | '7' | 0 | 0 |
| recall | none | '8' | - | 1 |
| recall | whole | '8' | - | 1 |
| recall | code0_x1 | '8' | - | 1 |
| recall | code1_x1 | '8' | - | 1 |
| recall | rand_x1 | '8' | - | 1 |
| recall | ccode0_x1 | '8' | - | 1 |
| recall | ccode1_x1 | '8' | - | 1 |
| recall | code0_x2 | '8' | - | 1 |
| recall | code1_x2 | '8' | - | 1 |
| recall | rand_x2 | '8' | - | 1 |
| recall | ccode0_x2 | '8' | - | 1 |
| recall | ccode1_x2 | '8' | - | 1 |

### C0-0421: A = butterfly (slot 2), B = cow (slot 1); slot 0: pig (locker 2); slot 1: cow (locker 9); slot 2: butterfly (locker 7)

O: The locker of the pig is 2. The locker of the cow is 9. The locker of the butterfly is 7. Sean picked the butterfly. Dan picked the cow. Owen picked the pig.

S_B: The locker of the pig is 2. The locker of the cow is 9. The locker of the butterfly is 7. Sean picked the cow. Dan picked the cow. Owen picked the pig.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '7' | 2 | 1 |
| lookup | whole | '9' | 1 | 0 |
| lookup | code0_x1 | '7' | 2 | 1 |
| lookup | code1_x1 | '7' | 2 | 1 |
| lookup | rand_x1 | '7' | 2 | 1 |
| lookup | ccode0_x1 | '7' | 2 | 1 |
| lookup | ccode1_x1 | '7' | 2 | 1 |
| lookup | code0_x2 | '7' | 2 | 1 |
| lookup | code1_x2 | '7' | 2 | 1 |
| lookup | rand_x2 | '7' | 2 | 1 |
| lookup | ccode0_x2 | '9' | 1 | 0 |
| lookup | ccode1_x2 | '9' | 1 | 0 |
| recall | none | '6' | - | 1 |
| recall | whole | '6' | - | 1 |
| recall | code0_x1 | '6' | - | 1 |
| recall | code1_x1 | '6' | - | 1 |
| recall | rand_x1 | '6' | - | 1 |
| recall | ccode0_x1 | '6' | - | 1 |
| recall | ccode1_x1 | '6' | - | 1 |
| recall | code0_x2 | '6' | - | 1 |
| recall | code1_x2 | '6' | - | 1 |
| recall | rand_x2 | '6' | - | 1 |
| recall | ccode0_x2 | '6' | - | 1 |
| recall | ccode1_x2 | '6' | - | 1 |

### C0-0441: A = deer (slot 0), B = goose (slot 2); slot 0: deer (locker 6); slot 1: pig (locker 2); slot 2: goose (locker 4)

O: The locker of the deer is 6. The locker of the pig is 2. The locker of the goose is 4. Ryan picked the goose. Will picked the deer. Dan picked the pig.

S_B: The locker of the deer is 6. The locker of the pig is 2. The locker of the goose is 4. Ryan picked the goose. Will picked the goose. Dan picked the pig.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '6' | 0 | 1 |
| lookup | whole | '4' | 2 | 0 |
| lookup | code1_x1 | '4' | 2 | 0 |
| lookup | code2_x1 | '4' | 2 | 0 |
| lookup | rand_x1 | '6' | 0 | 1 |
| lookup | ccode1_x1 | '6' | 0 | 1 |
| lookup | ccode2_x1 | '4' | 2 | 0 |
| lookup | code1_x2 | '4' | 2 | 0 |
| lookup | code2_x2 | '4' | 2 | 0 |
| lookup | rand_x2 | '4' | 2 | 0 |
| lookup | ccode1_x2 | '4' | 2 | 0 |
| lookup | ccode2_x2 | '4' | 2 | 0 |
| recall | none | '4' | - | 1 |
| recall | whole | '2' | - | 0 |
| recall | code1_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | code2_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode1_x2 | '4' | - | 1 |
| recall | ccode2_x2 | '4' | - | 1 |

### C0-0512: A = camel (slot 2), B = duck (slot 0); slot 0: duck (locker 7); slot 1: dog (locker 3); slot 2: camel (locker 9)

O: The locker of the duck is 7. The locker of the dog is 3. The locker of the camel is 9. Emma picked the camel. Adam picked the dog. Tara picked the duck.

S_B: The locker of the duck is 7. The locker of the dog is 3. The locker of the camel is 9. Emma picked the duck. Adam picked the dog. Tara picked the duck.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '9' | 2 | 1 |
| lookup | whole | '7' | 0 | 0 |
| lookup | code0_x1 | '9' | 2 | 1 |
| lookup | code1_x1 | '9' | 2 | 1 |
| lookup | rand_x1 | '9' | 2 | 1 |
| lookup | ccode0_x1 | '9' | 2 | 1 |
| lookup | ccode1_x1 | '9' | 2 | 1 |
| lookup | code0_x2 | '9' | 2 | 1 |
| lookup | code1_x2 | '9' | 2 | 1 |
| lookup | rand_x2 | '9' | 2 | 1 |
| lookup | ccode0_x2 | '3' | 1 | 0 |
| lookup | ccode1_x2 | '9' | 2 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '4' | - | 1 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code1_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode1_x2 | '4' | - | 1 |

### C0-0521: A = pig (slot 2), B = chicken (slot 1); slot 0: deer (locker 8); slot 1: chicken (locker 5); slot 2: pig (locker 2)

O: The locker of the deer is 8. The locker of the chicken is 5. The locker of the pig is 2. Maria picked the pig. Sara picked the deer. Frank picked the chicken.

S_B: The locker of the deer is 8. The locker of the chicken is 5. The locker of the pig is 2. Maria picked the chicken. Sara picked the deer. Frank picked the chicken.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '2' | 2 | 1 |
| lookup | whole | '5' | 1 | 0 |
| lookup | code0_x1 | '2' | 2 | 1 |
| lookup | code1_x1 | '2' | 2 | 1 |
| lookup | rand_x1 | '2' | 2 | 1 |
| lookup | ccode0_x1 | '2' | 2 | 1 |
| lookup | ccode1_x1 | '2' | 2 | 1 |
| lookup | code0_x2 | '2' | 2 | 1 |
| lookup | code1_x2 | '2' | 2 | 1 |
| lookup | rand_x2 | '2' | 2 | 1 |
| lookup | ccode0_x2 | '8' | 0 | 0 |
| lookup | ccode1_x2 | '2' | 2 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '2' | - | 0 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code1_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode1_x2 | '4' | - | 1 |

### C0-0545: A = pig (slot 1), B = butterfly (slot 0); slot 0: butterfly (locker 6); slot 1: pig (locker 5); slot 2: tick (locker 8)

O: The locker of the butterfly is 6. The locker of the pig is 5. The locker of the tick is 8. Dan picked the pig. Diana picked the butterfly. David picked the tick.

S_B: The locker of the butterfly is 6. The locker of the pig is 5. The locker of the tick is 8. Dan picked the butterfly. Diana picked the butterfly. David picked the tick.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '5' | 1 | 1 |
| lookup | whole | '6' | 0 | 0 |
| lookup | code0_x1 | '5' | 1 | 1 |
| lookup | code2_x1 | '5' | 1 | 1 |
| lookup | rand_x1 | '5' | 1 | 1 |
| lookup | ccode0_x1 | '5' | 1 | 1 |
| lookup | ccode2_x1 | '5' | 1 | 1 |
| lookup | code0_x2 | '5' | 1 | 1 |
| lookup | code2_x2 | '5' | 1 | 1 |
| lookup | rand_x2 | '5' | 1 | 1 |
| lookup | ccode0_x2 | '5' | 1 | 1 |
| lookup | ccode2_x2 | '5' | 1 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '4' | - | 1 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code2_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode2_x2 | '4' | - | 1 |

## x53_8c_27b: 10 random scenes of 300 (seed 0)

### C0-0028: A = fly (slot 0), B = duck (slot 1); slot 0: fly (locker 3); slot 1: duck (locker 6); slot 2: bee (locker 4)

O: The locker of the fly is 3. The locker of the duck is 6. The locker of the bee is 4. Lucy picked the duck. Sam picked the fly. Liam picked the bee.

S_B: The locker of the fly is 3. The locker of the duck is 6. The locker of the bee is 4. Lucy picked the duck. Sam picked the duck. Liam picked the bee.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '3' | 0 | 1 |
| lookup | whole | '6' | 1 | 0 |
| lookup | code1_x1 | '6' | 1 | 0 |
| lookup | code2_x1 | '3' | 0 | 1 |
| lookup | rand_x1 | '3' | 0 | 1 |
| lookup | ccode1_x1 | '6' | 1 | 0 |
| lookup | ccode2_x1 | '6' | 1 | 0 |
| lookup | code1_x2 | '6' | 1 | 0 |
| lookup | code2_x2 | '6' | 1 | 0 |
| lookup | rand_x2 | '6' | 1 | 0 |
| lookup | ccode1_x2 | '6' | 1 | 0 |
| lookup | ccode2_x2 | '6' | 1 | 0 |
| recall | none | '6' | - | 1 |
| recall | whole | '6' | - | 1 |
| recall | code1_x1 | '6' | - | 1 |
| recall | code2_x1 | '6' | - | 1 |
| recall | rand_x1 | '6' | - | 1 |
| recall | ccode1_x1 | '6' | - | 1 |
| recall | ccode2_x1 | '6' | - | 1 |
| recall | code1_x2 | '6' | - | 1 |
| recall | code2_x2 | '6' | - | 1 |
| recall | rand_x2 | '6' | - | 1 |
| recall | ccode1_x2 | '6' | - | 1 |
| recall | ccode2_x2 | '6' | - | 1 |

### C0-0195: A = goose (slot 2), B = pig (slot 1); slot 0: bear (locker 2); slot 1: pig (locker 8); slot 2: goose (locker 7)

O: The locker of the bear is 2. The locker of the pig is 8. The locker of the goose is 7. Eric picked the goose. Iris picked the pig. Clara picked the bear.

S_B: The locker of the bear is 2. The locker of the pig is 8. The locker of the goose is 7. Eric picked the pig. Iris picked the pig. Clara picked the bear.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '7' | 2 | 1 |
| lookup | whole | '8' | 1 | 0 |
| lookup | code0_x1 | '7' | 2 | 1 |
| lookup | code1_x1 | '7' | 2 | 1 |
| lookup | rand_x1 | '7' | 2 | 1 |
| lookup | ccode0_x1 | '7' | 2 | 1 |
| lookup | ccode1_x1 | '7' | 2 | 1 |
| lookup | code0_x2 | '7' | 2 | 1 |
| lookup | code1_x2 | '7' | 2 | 1 |
| lookup | rand_x2 | '7' | 2 | 1 |
| lookup | ccode0_x2 | '7' | 2 | 1 |
| lookup | ccode1_x2 | '7' | 2 | 1 |
| recall | none | '2' | - | 1 |
| recall | whole | '4' | - | 0 |
| recall | code0_x1 | '2' | - | 1 |
| recall | code1_x1 | '2' | - | 1 |
| recall | rand_x1 | '2' | - | 1 |
| recall | ccode0_x1 | '2' | - | 1 |
| recall | ccode1_x1 | '2' | - | 1 |
| recall | code0_x2 | '2' | - | 1 |
| recall | code1_x2 | '2' | - | 1 |
| recall | rand_x2 | '2' | - | 1 |
| recall | ccode0_x2 | '2' | - | 1 |
| recall | ccode1_x2 | '2' | - | 1 |

### C0-0226: A = fox (slot 1), B = ant (slot 0); slot 0: ant (locker 9); slot 1: fox (locker 2); slot 2: goose (locker 8)

O: The locker of the ant is 9. The locker of the fox is 2. The locker of the goose is 8. Noah picked the goose. Ivy picked the fox. Lily picked the ant.

S_B: The locker of the ant is 9. The locker of the fox is 2. The locker of the goose is 8. Noah picked the goose. Ivy picked the ant. Lily picked the ant.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '2' | 1 | 1 |
| lookup | whole | '9' | 0 | 0 |
| lookup | code0_x1 | '2' | 1 | 1 |
| lookup | code2_x1 | '2' | 1 | 1 |
| lookup | rand_x1 | '2' | 1 | 1 |
| lookup | ccode0_x1 | '2' | 1 | 1 |
| lookup | ccode2_x1 | '2' | 1 | 1 |
| lookup | code0_x2 | '2' | 1 | 1 |
| lookup | code2_x2 | '2' | 1 | 1 |
| lookup | rand_x2 | '2' | 1 | 1 |
| lookup | ccode0_x2 | '2' | 1 | 1 |
| lookup | ccode2_x2 | '8' | 2 | 0 |
| recall | none | '4' | - | 1 |
| recall | whole | '4' | - | 1 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code2_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode2_x2 | '4' | - | 1 |

### C0-0267: A = camel (slot 0), B = beetle (slot 1); slot 0: camel (locker 6); slot 1: beetle (locker 7); slot 2: butterfly (locker 4)

O: The locker of the camel is 6. The locker of the beetle is 7. The locker of the butterfly is 4. Sean picked the butterfly. Carl picked the beetle. Iris picked the camel.

S_B: The locker of the camel is 6. The locker of the beetle is 7. The locker of the butterfly is 4. Sean picked the butterfly. Carl picked the beetle. Iris picked the beetle.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '6' | 0 | 1 |
| lookup | whole | '7' | 1 | 0 |
| lookup | code1_x1 | '6' | 0 | 1 |
| lookup | code2_x1 | '6' | 0 | 1 |
| lookup | rand_x1 | '6' | 0 | 1 |
| lookup | ccode1_x1 | '6' | 0 | 1 |
| lookup | ccode2_x1 | '6' | 0 | 1 |
| lookup | code1_x2 | '6' | 0 | 1 |
| lookup | code2_x2 | '6' | 0 | 1 |
| lookup | rand_x2 | '6' | 0 | 1 |
| lookup | ccode1_x2 | '7' | 1 | 0 |
| lookup | ccode2_x2 | '6' | 0 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '6' | - | 0 |
| recall | code1_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | code2_x2 | '4' | - | 1 |
| recall | rand_x2 | '6' | - | 0 |
| recall | ccode1_x2 | '4' | - | 1 |
| recall | ccode2_x2 | '6' | - | 0 |

### C0-0287: A = fly (slot 0), B = tiger (slot 2); slot 0: fly (locker 6); slot 1: chicken (locker 8); slot 2: tiger (locker 7)

O: The locker of the fly is 6. The locker of the chicken is 8. The locker of the tiger is 7. Leo picked the tiger. Mark picked the fly. Maria picked the chicken.

S_B: The locker of the fly is 6. The locker of the chicken is 8. The locker of the tiger is 7. Leo picked the tiger. Mark picked the tiger. Maria picked the chicken.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '6' | 0 | 1 |
| lookup | whole | '7' | 2 | 0 |
| lookup | code1_x1 | '6' | 0 | 1 |
| lookup | code2_x1 | '6' | 0 | 1 |
| lookup | rand_x1 | '6' | 0 | 1 |
| lookup | ccode1_x1 | '6' | 0 | 1 |
| lookup | ccode2_x1 | '6' | 0 | 1 |
| lookup | code1_x2 | '7' | 2 | 0 |
| lookup | code2_x2 | '7' | 2 | 0 |
| lookup | rand_x2 | '6' | 0 | 1 |
| lookup | ccode1_x2 | '7' | 2 | 0 |
| lookup | ccode2_x2 | '7' | 2 | 0 |
| recall | none | '6' | - | 1 |
| recall | whole | '6' | - | 1 |
| recall | code1_x1 | '6' | - | 1 |
| recall | code2_x1 | '6' | - | 1 |
| recall | rand_x1 | '6' | - | 1 |
| recall | ccode1_x1 | '6' | - | 1 |
| recall | ccode2_x1 | '6' | - | 1 |
| recall | code1_x2 | '6' | - | 1 |
| recall | code2_x2 | '6' | - | 1 |
| recall | rand_x2 | '6' | - | 1 |
| recall | ccode1_x2 | '6' | - | 1 |
| recall | ccode2_x2 | '6' | - | 1 |

### C0-0304: A = cow (slot 0), B = ant (slot 2); slot 0: cow (locker 3); slot 1: lion (locker 1); slot 2: ant (locker 2)

O: The locker of the cow is 3. The locker of the lion is 1. The locker of the ant is 2. Julia picked the ant. Noah picked the cow. Vera picked the lion.

S_B: The locker of the cow is 3. The locker of the lion is 1. The locker of the ant is 2. Julia picked the ant. Noah picked the ant. Vera picked the lion.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '3' | 0 | 1 |
| lookup | whole | '2' | 2 | 0 |
| lookup | code1_x1 | '2' | 2 | 0 |
| lookup | code2_x1 | '3' | 0 | 1 |
| lookup | rand_x1 | '3' | 0 | 1 |
| lookup | ccode1_x1 | '2' | 2 | 0 |
| lookup | ccode2_x1 | '2' | 2 | 0 |
| lookup | code1_x2 | '2' | 2 | 0 |
| lookup | code2_x2 | '2' | 2 | 0 |
| lookup | rand_x2 | '2' | 2 | 0 |
| lookup | ccode1_x2 | '2' | 2 | 0 |
| lookup | ccode2_x2 | '2' | 2 | 0 |
| recall | none | '4' | - | 1 |
| recall | whole | '6' | - | 0 |
| recall | code1_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | code2_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode1_x2 | '4' | - | 1 |
| recall | ccode2_x2 | '4' | - | 1 |

### C0-0319: A = owl (slot 1), B = fly (slot 0); slot 0: fly (locker 5); slot 1: owl (locker 7); slot 2: ant (locker 3)

O: The locker of the fly is 5. The locker of the owl is 7. The locker of the ant is 3. Max picked the fly. James picked the owl. Olivia picked the ant.

S_B: The locker of the fly is 5. The locker of the owl is 7. The locker of the ant is 3. Max picked the fly. James picked the fly. Olivia picked the ant.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '7' | 1 | 1 |
| lookup | whole | '5' | 0 | 0 |
| lookup | code0_x1 | '7' | 1 | 1 |
| lookup | code2_x1 | '7' | 1 | 1 |
| lookup | rand_x1 | '7' | 1 | 1 |
| lookup | ccode0_x1 | '7' | 1 | 1 |
| lookup | ccode2_x1 | '7' | 1 | 1 |
| lookup | code0_x2 | '5' | 0 | 0 |
| lookup | code2_x2 | '7' | 1 | 1 |
| lookup | rand_x2 | '7' | 1 | 1 |
| lookup | ccode0_x2 | '5' | 0 | 0 |
| lookup | ccode2_x2 | '5' | 0 | 0 |
| recall | none | '2' | - | 1 |
| recall | whole | '6' | - | 0 |
| recall | code0_x1 | '2' | - | 1 |
| recall | code2_x1 | '2' | - | 1 |
| recall | rand_x1 | '2' | - | 1 |
| recall | ccode0_x1 | '2' | - | 1 |
| recall | ccode2_x1 | '2' | - | 1 |
| recall | code0_x2 | '2' | - | 1 |
| recall | code2_x2 | '2' | - | 1 |
| recall | rand_x2 | '2' | - | 1 |
| recall | ccode0_x2 | '2' | - | 1 |
| recall | ccode2_x2 | '2' | - | 1 |

### C0-0367: A = pig (slot 2), B = butterfly (slot 1); slot 0: bee (locker 9); slot 1: butterfly (locker 8); slot 2: pig (locker 4)

O: The locker of the bee is 9. The locker of the butterfly is 8. The locker of the pig is 4. Sean picked the bee. Mark picked the butterfly. Fiona picked the pig.

S_B: The locker of the bee is 9. The locker of the butterfly is 8. The locker of the pig is 4. Sean picked the bee. Mark picked the butterfly. Fiona picked the butterfly.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '4' | 2 | 1 |
| lookup | whole | '8' | 1 | 0 |
| lookup | code0_x1 | '4' | 2 | 1 |
| lookup | code1_x1 | '4' | 2 | 1 |
| lookup | rand_x1 | '4' | 2 | 1 |
| lookup | ccode0_x1 | '4' | 2 | 1 |
| lookup | ccode1_x1 | '4' | 2 | 1 |
| lookup | code0_x2 | '4' | 2 | 1 |
| lookup | code1_x2 | '4' | 2 | 1 |
| lookup | rand_x2 | '4' | 2 | 1 |
| lookup | ccode0_x2 | '4' | 2 | 1 |
| lookup | ccode1_x2 | '4' | 2 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '4' | - | 1 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code1_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode1_x2 | '4' | - | 1 |

### C0-0371: A = pig (slot 2), B = owl (slot 1); slot 0: wolf (locker 2); slot 1: owl (locker 7); slot 2: pig (locker 9)

O: The locker of the wolf is 2. The locker of the owl is 7. The locker of the pig is 9. Tara picked the owl. Frank picked the wolf. Clara picked the pig.

S_B: The locker of the wolf is 2. The locker of the owl is 7. The locker of the pig is 9. Tara picked the owl. Frank picked the wolf. Clara picked the owl.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '9' | 2 | 1 |
| lookup | whole | '7' | 1 | 0 |
| lookup | code0_x1 | '9' | 2 | 1 |
| lookup | code1_x1 | '9' | 2 | 1 |
| lookup | rand_x1 | '9' | 2 | 1 |
| lookup | ccode0_x1 | '9' | 2 | 1 |
| lookup | ccode1_x1 | '9' | 2 | 1 |
| lookup | code0_x2 | '9' | 2 | 1 |
| lookup | code1_x2 | '9' | 2 | 1 |
| lookup | rand_x2 | '7' | 1 | 0 |
| lookup | ccode0_x2 | '9' | 2 | 1 |
| lookup | ccode1_x2 | '7' | 1 | 0 |
| recall | none | '4' | - | 1 |
| recall | whole | '4' | - | 1 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code1_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode1_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code1_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode1_x2 | '4' | - | 1 |

### C0-0388: A = elephant (slot 1), B = eagle (slot 2); slot 0: mouse (locker 6); slot 1: elephant (locker 1); slot 2: eagle (locker 8)

O: The locker of the mouse is 6. The locker of the elephant is 1. The locker of the eagle is 8. Peter picked the elephant. Leo picked the eagle. Sam picked the mouse.

S_B: The locker of the mouse is 6. The locker of the elephant is 1. The locker of the eagle is 8. Peter picked the eagle. Leo picked the eagle. Sam picked the mouse.

| reader | arm | top token | lookup's slot | clean answer kept |
|---|---|---|---|---|
| lookup | none | '1' | 1 | 1 |
| lookup | whole | '8' | 2 | 0 |
| lookup | code0_x1 | '1' | 1 | 1 |
| lookup | code2_x1 | '1' | 1 | 1 |
| lookup | rand_x1 | '1' | 1 | 1 |
| lookup | ccode0_x1 | '1' | 1 | 1 |
| lookup | ccode2_x1 | '1' | 1 | 1 |
| lookup | code0_x2 | '1' | 1 | 1 |
| lookup | code2_x2 | '1' | 1 | 1 |
| lookup | rand_x2 | '1' | 1 | 1 |
| lookup | ccode0_x2 | '1' | 1 | 1 |
| lookup | ccode2_x2 | '1' | 1 | 1 |
| recall | none | '4' | - | 1 |
| recall | whole | '2' | - | 0 |
| recall | code0_x1 | '4' | - | 1 |
| recall | code2_x1 | '4' | - | 1 |
| recall | rand_x1 | '4' | - | 1 |
| recall | ccode0_x1 | '4' | - | 1 |
| recall | ccode2_x1 | '4' | - | 1 |
| recall | code0_x2 | '4' | - | 1 |
| recall | code2_x2 | '4' | - | 1 |
| recall | rand_x2 | '4' | - | 1 |
| recall | ccode0_x2 | '4' | - | 1 |
| recall | ccode2_x2 | '4' | - | 1 |

