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

