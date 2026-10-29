# 53.6 examples (verify pack): the scene's roles, O and S_B, every arm's top token. UNVERIFIED.

## qwen35_9b_x53_6: 10 random scenes of 300 (seed 0)

### C0-0180: A = cow (slot 1, locker 6, 4 legs), B = butterfly (slot 0, locker 9, 6 legs), C = turkey (slot 2, locker 8, 2 legs)

O: The locker of the butterfly is 9. The locker of the cow is 6. The locker of the turkey is 8. Sean picked the turkey. Mark picked the cow. Lucy picked the butterfly.

S_B: The locker of the butterfly is 9. The locker of the cow is 6. The locker of the turkey is 8. Sean picked the turkey. Mark picked the butterfly. Lucy picked the butterfly.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '6' | original |
| PP | lens | '6' | original |
| PP | addr | '6' | original |
| PP | both | '6' | original |
| PP | both_rand | '6' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '4' | original |
| PM | both | '4' | original |
| PM | both_rand | '4' | original |

### C0-0782: A = spider (slot 1, locker 7, 8 legs), B = crow (slot 2, locker 4, 2 legs), C = cow (slot 0, locker 3, 4 legs)

O: The locker of the cow is 3. The locker of the spider is 7. The locker of the crow is 4. Tara picked the spider. Finn picked the cow. Olivia picked the crow.

S_B: The locker of the cow is 3. The locker of the spider is 7. The locker of the crow is 4. Tara picked the crow. Finn picked the cow. Olivia picked the crow.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '7' | original |
| PP | lens | '7' | original |
| PP | addr | '3' | C |
| PP | both | '3' | C |
| PP | both_rand | '7' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '8' | original |
| PM | both | '6' | other |
| PM | both_rand | '8' | original |

### C0-0944: A = turkey (slot 0, locker 4, 2 legs), B = fly (slot 2, locker 3, 6 legs), C = fox (slot 1, locker 9, 4 legs)

O: The locker of the turkey is 4. The locker of the fox is 9. The locker of the fly is 3. Peter picked the fly. Adam picked the turkey. Nina picked the fox.

S_B: The locker of the turkey is 4. The locker of the fox is 9. The locker of the fly is 3. Peter picked the fly. Adam picked the fly. Nina picked the fox.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '4' | original |
| PP | lens | '4' | original |
| PP | addr | '9' | C |
| PP | both | '9' | C |
| PP | both_rand | '4' | original |
| PM | none | '2' | original |
| PM | lens | '2' | original |
| PM | addr | '4' | C |
| PM | both | '4' | C |
| PM | both_rand | '2' | original |

### C0-1083: A = tick (slot 2, locker 8, 8 legs), B = goat (slot 1, locker 7, 4 legs), C = turkey (slot 0, locker 9, 2 legs)

O: The locker of the turkey is 9. The locker of the goat is 7. The locker of the tick is 8. Laura picked the goat. Luke picked the turkey. Owen picked the tick.

S_B: The locker of the turkey is 9. The locker of the goat is 7. The locker of the tick is 8. Laura picked the goat. Luke picked the turkey. Owen picked the goat.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '8' | original |
| PP | lens | '8' | original |
| PP | addr | '8' | original |
| PP | both | '8' | original |
| PP | both_rand | '8' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '6' | other |
| PM | both | '6' | other |
| PM | both_rand | '8' | original |

### C0-1140: A = beetle (slot 1, locker 6, 6 legs), B = spider (slot 2, locker 9, 8 legs), C = rabbit (slot 0, locker 8, 4 legs)

O: The locker of the rabbit is 8. The locker of the beetle is 6. The locker of the spider is 9. Will picked the beetle. Eve picked the rabbit. Owen picked the spider.

S_B: The locker of the rabbit is 8. The locker of the beetle is 6. The locker of the spider is 9. Will picked the spider. Eve picked the rabbit. Owen picked the spider.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '6' | original |
| PP | lens | '6' | original |
| PP | addr | '8' | C |
| PP | both | '8' | C |
| PP | both_rand | '6' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '8' | B |
| PM | both_rand | '6' | original |

### C0-1196: A = cat (slot 0, locker 5, 4 legs), B = turkey (slot 2, locker 4, 2 legs), C = bee (slot 1, locker 8, 6 legs)

O: The locker of the cat is 5. The locker of the bee is 8. The locker of the turkey is 4. Sam picked the turkey. Laura picked the bee. Mark picked the cat.

S_B: The locker of the cat is 5. The locker of the bee is 8. The locker of the turkey is 4. Sam picked the turkey. Laura picked the bee. Mark picked the turkey.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '5' | original |
| PP | lens | '5' | original |
| PP | addr | '8' | C |
| PP | both | '8' | C |
| PP | both_rand | '5' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '6' | C |
| PM | both | '6' | C |
| PM | both_rand | '4' | original |

### C0-1231: A = dog (slot 2, locker 7, 4 legs), B = crow (slot 0, locker 6, 2 legs), C = beetle (slot 1, locker 5, 6 legs)

O: The locker of the crow is 6. The locker of the beetle is 5. The locker of the dog is 7. Will picked the dog. Max picked the crow. Owen picked the beetle.

S_B: The locker of the crow is 6. The locker of the beetle is 5. The locker of the dog is 7. Will picked the crow. Max picked the crow. Owen picked the beetle.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '7' | original |
| PP | lens | '7' | original |
| PP | addr | '7' | original |
| PP | both | '7' | original |
| PP | both_rand | '7' | original |
| PM | none | '4' | original |
| PM | lens | '2' | B |
| PM | addr | '4' | original |
| PM | both | '2' | B |
| PM | both_rand | '2' | B |

### C0-1410: A = eagle (slot 0, locker 3, 2 legs), B = goat (slot 2, locker 5, 4 legs), C = spider (slot 1, locker 1, 8 legs)

O: The locker of the eagle is 3. The locker of the spider is 1. The locker of the goat is 5. Sean picked the goat. Ivan picked the spider. Paul picked the eagle.

S_B: The locker of the eagle is 3. The locker of the spider is 1. The locker of the goat is 5. Sean picked the goat. Ivan picked the spider. Paul picked the goat.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '3' | original |
| PP | lens | '3' | original |
| PP | addr | '1' | C |
| PP | both | '1' | C |
| PP | both_rand | '3' | original |
| PM | none | '2' | original |
| PM | lens | '2' | original |
| PM | addr | '8' | C |
| PM | both | '4' | B |
| PM | both_rand | '4' | B |

### C0-1428: A = turkey (slot 2, locker 9, 2 legs), B = fly (slot 0, locker 5, 6 legs), C = spider (slot 1, locker 2, 8 legs)

O: The locker of the fly is 5. The locker of the spider is 2. The locker of the turkey is 9. Will picked the spider. Owen picked the fly. Laura picked the turkey.

S_B: The locker of the fly is 5. The locker of the spider is 2. The locker of the turkey is 9. Will picked the spider. Owen picked the fly. Laura picked the fly.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '9' | original |
| PP | lens | '9' | original |
| PP | addr | '9' | original |
| PP | both | '9' | original |
| PP | both_rand | '9' | original |
| PM | none | '2' | original |
| PM | lens | '2' | original |
| PM | addr | '8' | C |
| PM | both | '8' | C |
| PM | both_rand | '2' | original |

### C0-1540: A = crow (slot 2, locker 1, 2 legs), B = beetle (slot 0, locker 6, 6 legs), C = rabbit (slot 1, locker 9, 4 legs)

O: The locker of the beetle is 6. The locker of the rabbit is 9. The locker of the crow is 1. Kyle picked the rabbit. Frank picked the crow. Henry picked the beetle.

S_B: The locker of the beetle is 6. The locker of the rabbit is 9. The locker of the crow is 1. Kyle picked the rabbit. Frank picked the beetle. Henry picked the beetle.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '1' | original |
| PP | lens | '1' | original |
| PP | addr | '1' | original |
| PP | both | '1' | original |
| PP | both_rand | '1' | original |
| PM | none | '2' | original |
| PM | lens | '2' | original |
| PM | addr | '2' | original |
| PM | both | '6' | B |
| PM | both_rand | '2' | original |

