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

## nem35l_x53_6: 10 random scenes of 300 (seed 0)

### C0-0165: A = spider (slot 2, locker 2, 8 legs), B = mouse (slot 1, locker 9, 4 legs), C = ant (slot 0, locker 7, 6 legs)

O: The locker of the ant is 7. The locker of the mouse is 9. The locker of the spider is 2. Sara picked the ant. Zoe picked the mouse. Lucy picked the spider.

S_B: The locker of the ant is 7. The locker of the mouse is 9. The locker of the spider is 2. Sara picked the ant. Zoe picked the mouse. Lucy picked the mouse.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '2' | original |
| PP | lens | '2' | original |
| PP | addr | '2' | original |
| PP | both | '7' | C |
| PP | both_rand | '2' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '8' | original |
| PM | both | '8' | original |
| PM | both_rand | '8' | original |

### C0-0851: A = tick (slot 0, locker 9, 8 legs), B = sheep (slot 2, locker 2, 4 legs), C = ant (slot 1, locker 6, 6 legs)

O: The locker of the tick is 9. The locker of the ant is 6. The locker of the sheep is 2. Diana picked the ant. Maria picked the tick. Sean picked the sheep.

S_B: The locker of the tick is 9. The locker of the ant is 6. The locker of the sheep is 2. Diana picked the ant. Maria picked the sheep. Sean picked the sheep.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '9' | original |
| PP | lens | '9' | original |
| PP | addr | '6' | C |
| PP | both | '6' | C |
| PP | both_rand | '9' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '6' | C |
| PM | both | '6' | C |
| PM | both_rand | '8' | original |

### C0-1027: A = fly (slot 0, locker 6, 6 legs), B = dog (slot 1, locker 1, 4 legs), C = eagle (slot 2, locker 8, 2 legs)

O: The locker of the fly is 6. The locker of the dog is 1. The locker of the eagle is 8. Tara picked the eagle. Carl picked the dog. Anna picked the fly.

S_B: The locker of the fly is 6. The locker of the dog is 1. The locker of the eagle is 8. Tara picked the eagle. Carl picked the dog. Anna picked the dog.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '6' | original |
| PP | lens | '6' | original |
| PP | addr | '1' | B |
| PP | both | '1' | B |
| PP | both_rand | '6' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '4' | B |
| PM | both_rand | '6' | original |

### C0-1200: A = spider (slot 1, locker 9, 8 legs), B = ant (slot 0, locker 2, 6 legs), C = sheep (slot 2, locker 4, 4 legs)

O: The locker of the ant is 2. The locker of the spider is 9. The locker of the sheep is 4. Grace picked the spider. Clara picked the sheep. Tara picked the ant.

S_B: The locker of the ant is 2. The locker of the spider is 9. The locker of the sheep is 4. Grace picked the ant. Clara picked the sheep. Tara picked the ant.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '9' | original |
| PP | lens | '9' | original |
| PP | addr | '9' | original |
| PP | both | '9' | original |
| PP | both_rand | '9' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '8' | original |
| PM | both | '8' | original |
| PM | both_rand | '8' | original |

### C0-1273: A = ant (slot 2, locker 5, 6 legs), B = crow (slot 0, locker 9, 2 legs), C = horse (slot 1, locker 1, 4 legs)

O: The locker of the crow is 9. The locker of the horse is 1. The locker of the ant is 5. Max picked the ant. Owen picked the crow. Beth picked the horse.

S_B: The locker of the crow is 9. The locker of the horse is 1. The locker of the ant is 5. Max picked the crow. Owen picked the crow. Beth picked the horse.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '5' | original |
| PP | lens | '5' | original |
| PP | addr | '5' | original |
| PP | both | '5' | original |
| PP | both_rand | '5' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '6' | original |
| PM | both_rand | '6' | original |

### C0-1334: A = crow (slot 0, locker 7, 2 legs), B = tiger (slot 1, locker 6, 4 legs), C = ant (slot 2, locker 1, 6 legs)

O: The locker of the crow is 7. The locker of the tiger is 6. The locker of the ant is 1. Ivy picked the tiger. Dan picked the ant. Sean picked the crow.

S_B: The locker of the crow is 7. The locker of the tiger is 6. The locker of the ant is 1. Ivy picked the tiger. Dan picked the ant. Sean picked the tiger.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '7' | original |
| PP | lens | '7' | original |
| PP | addr | '1' | C |
| PP | both | '1' | C |
| PP | both_rand | '7' | original |
| PM | none | '2' | original |
| PM | lens | '2' | original |
| PM | addr | '2' | original |
| PM | both | '4' | B |
| PM | both_rand | '2' | original |

### C0-1391: A = fly (slot 2, locker 6, 6 legs), B = sheep (slot 0, locker 2, 4 legs), C = tick (slot 1, locker 8, 8 legs)

O: The locker of the sheep is 2. The locker of the tick is 8. The locker of the fly is 6. Victor picked the sheep. Tara picked the fly. Kyle picked the tick.

S_B: The locker of the sheep is 2. The locker of the tick is 8. The locker of the fly is 6. Victor picked the sheep. Tara picked the sheep. Kyle picked the tick.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '6' | original |
| PP | lens | '6' | original |
| PP | addr | '6' | original |
| PP | both | '6' | original |
| PP | both_rand | '6' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '6' | original |
| PM | both_rand | '6' | original |

### C0-1550: A = owl (slot 0, locker 1, 2 legs), B = bee (slot 1, locker 6, 6 legs), C = camel (slot 2, locker 3, 4 legs)

O: The locker of the owl is 1. The locker of the bee is 6. The locker of the camel is 3. Adam picked the camel. Grace picked the owl. Tara picked the bee.

S_B: The locker of the owl is 1. The locker of the bee is 6. The locker of the camel is 3. Adam picked the camel. Grace picked the bee. Tara picked the bee.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '1' | original |
| PP | lens | '1' | original |
| PP | addr | '3' | C |
| PP | both | '6' | B |
| PP | both_rand | '1' | original |
| PM | none | '2' | original |
| PM | lens | '2' | original |
| PM | addr | '6' | B |
| PM | both | '6' | B |
| PM | both_rand | '2' | original |

### C0-1569: A = owl (slot 2, locker 1, 2 legs), B = tick (slot 0, locker 2, 8 legs), C = cow (slot 1, locker 6, 4 legs)

O: The locker of the tick is 2. The locker of the cow is 6. The locker of the owl is 1. Luke picked the owl. Kyle picked the cow. Beth picked the tick.

S_B: The locker of the tick is 2. The locker of the cow is 6. The locker of the owl is 1. Luke picked the tick. Kyle picked the cow. Beth picked the tick.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '1' | original |
| PP | lens | '1' | original |
| PP | addr | '1' | original |
| PP | both | '1' | original |
| PP | both_rand | '1' | original |
| PM | none | '2' | original |
| PM | lens | '2' | original |
| PM | addr | '1' | other |
| PM | both | '2' | original |
| PM | both_rand | '2' | original |

### C0-1630: A = frog (slot 0, locker 4, 4 legs), B = bee (slot 1, locker 6, 6 legs), C = tick (slot 2, locker 5, 8 legs)

O: The locker of the frog is 4. The locker of the bee is 6. The locker of the tick is 5. Beth picked the frog. Adam picked the bee. Liam picked the tick.

S_B: The locker of the frog is 4. The locker of the bee is 6. The locker of the tick is 5. Beth picked the bee. Adam picked the bee. Liam picked the tick.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '4' | original |
| PP | lens | '4' | original |
| PP | addr | '5' | C |
| PP | both | '5' | C |
| PP | both_rand | '4' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '6' | B |
| PM | both | '6' | B |
| PM | both_rand | '4' | original |

## x53_6_27b: 10 random scenes of 300 (seed 0)

### C0-0134: A = sheep (slot 1, locker 3, 4 legs), B = owl (slot 2, locker 7, 2 legs), C = beetle (slot 0, locker 2, 6 legs)

O: The locker of the beetle is 2. The locker of the sheep is 3. The locker of the owl is 7. Luke picked the beetle. Beth picked the sheep. Ivan picked the owl.

S_B: The locker of the beetle is 2. The locker of the sheep is 3. The locker of the owl is 7. Luke picked the beetle. Beth picked the owl. Ivan picked the owl.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '3' | original |
| PP | lens | '3' | original |
| PP | addr | '3' | original |
| PP | both | '3' | original |
| PP | both_rand | '3' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '4' | original |
| PM | both | '4' | original |
| PM | both_rand | '4' | original |

### C0-0615: A = ant (slot 1, locker 4, 6 legs), B = horse (slot 0, locker 2, 4 legs), C = goose (slot 2, locker 3, 2 legs)

O: The locker of the horse is 2. The locker of the ant is 4. The locker of the goose is 3. Fiona picked the ant. Lily picked the goose. Ivy picked the horse.

S_B: The locker of the horse is 2. The locker of the ant is 4. The locker of the goose is 3. Fiona picked the horse. Lily picked the goose. Ivy picked the horse.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '4' | original |
| PP | lens | '4' | original |
| PP | addr | '4' | original |
| PP | both | '4' | original |
| PP | both_rand | '4' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '6' | original |
| PM | both_rand | '6' | original |

### C0-0705: A = camel (slot 1, locker 9, 4 legs), B = beetle (slot 0, locker 4, 6 legs), C = turkey (slot 2, locker 7, 2 legs)

O: The locker of the beetle is 4. The locker of the camel is 9. The locker of the turkey is 7. Iris picked the camel. Beth picked the turkey. Mark picked the beetle.

S_B: The locker of the beetle is 4. The locker of the camel is 9. The locker of the turkey is 7. Iris picked the beetle. Beth picked the turkey. Mark picked the beetle.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '9' | original |
| PP | lens | '9' | original |
| PP | addr | '9' | original |
| PP | both | '9' | original |
| PP | both_rand | '9' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '4' | original |
| PM | both | '4' | original |
| PM | both_rand | '4' | original |

### C0-0797: A = deer (slot 0, locker 5, 4 legs), B = spider (slot 2, locker 7, 8 legs), C = butterfly (slot 1, locker 6, 6 legs)

O: The locker of the deer is 5. The locker of the butterfly is 6. The locker of the spider is 7. Eva picked the butterfly. Victor picked the spider. Ryan picked the deer.

S_B: The locker of the deer is 5. The locker of the butterfly is 6. The locker of the spider is 7. Eva picked the butterfly. Victor picked the spider. Ryan picked the spider.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '5' | original |
| PP | lens | '5' | original |
| PP | addr | '5' | original |
| PP | both | '6' | C |
| PP | both_rand | '5' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '4' | original |
| PM | both | '4' | original |
| PM | both_rand | '4' | original |

### C0-0904: A = eagle (slot 1, locker 4, 2 legs), B = dog (slot 2, locker 1, 4 legs), C = ant (slot 0, locker 7, 6 legs)

O: The locker of the ant is 7. The locker of the eagle is 4. The locker of the dog is 1. Grace picked the dog. Owen picked the ant. Finn picked the eagle.

S_B: The locker of the ant is 7. The locker of the eagle is 4. The locker of the dog is 1. Grace picked the dog. Owen picked the ant. Finn picked the dog.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '4' | original |
| PP | lens | '4' | original |
| PP | addr | '7' | C |
| PP | both | '7' | C |
| PP | both_rand | '4' | original |
| PM | none | '2' | original |
| PM | lens | '2' | original |
| PM | addr | '2' | original |
| PM | both | '2' | original |
| PM | both_rand | '2' | original |

### C0-0951: A = beetle (slot 2, locker 3, 6 legs), B = mouse (slot 1, locker 1, 4 legs), C = goose (slot 0, locker 2, 2 legs)

O: The locker of the goose is 2. The locker of the mouse is 1. The locker of the beetle is 3. Sam picked the goose. Zoe picked the beetle. Carl picked the mouse.

S_B: The locker of the goose is 2. The locker of the mouse is 1. The locker of the beetle is 3. Sam picked the goose. Zoe picked the mouse. Carl picked the mouse.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '3' | original |
| PP | lens | '3' | original |
| PP | addr | '3' | original |
| PP | both | '3' | original |
| PP | both_rand | '3' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '6' | original |
| PM | both_rand | '6' | original |

### C0-0984: A = spider (slot 2, locker 2, 8 legs), B = ant (slot 1, locker 7, 6 legs), C = pig (slot 0, locker 6, 4 legs)

O: The locker of the pig is 6. The locker of the ant is 7. The locker of the spider is 2. Rose picked the spider. Clara picked the pig. Max picked the ant.

S_B: The locker of the pig is 6. The locker of the ant is 7. The locker of the spider is 2. Rose picked the ant. Clara picked the pig. Max picked the ant.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '2' | original |
| PP | lens | '2' | original |
| PP | addr | '2' | original |
| PP | both | '6' | C |
| PP | both_rand | '2' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '8' | original |
| PM | both | '6' | B |
| PM | both_rand | '8' | original |

### C0-1108: A = butterfly (slot 1, locker 6, 6 legs), B = turkey (slot 0, locker 3, 2 legs), C = sheep (slot 2, locker 4, 4 legs)

O: The locker of the turkey is 3. The locker of the butterfly is 6. The locker of the sheep is 4. Nina picked the butterfly. Sara picked the turkey. Alice picked the sheep.

S_B: The locker of the turkey is 3. The locker of the butterfly is 6. The locker of the sheep is 4. Nina picked the turkey. Sara picked the turkey. Alice picked the sheep.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '6' | original |
| PP | lens | '6' | original |
| PP | addr | '6' | original |
| PP | both | '6' | original |
| PP | both_rand | '6' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '6' | original |
| PM | both_rand | '6' | original |

### C0-1122: A = deer (slot 0, locker 9, 4 legs), B = bee (slot 1, locker 2, 6 legs), C = spider (slot 2, locker 1, 8 legs)

O: The locker of the deer is 9. The locker of the bee is 2. The locker of the spider is 1. Tom picked the deer. Liam picked the bee. Sara picked the spider.

S_B: The locker of the deer is 9. The locker of the bee is 2. The locker of the spider is 1. Tom picked the bee. Liam picked the bee. Sara picked the spider.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '9' | original |
| PP | lens | '9' | original |
| PP | addr | '9' | original |
| PP | both | '2' | B |
| PP | both_rand | '9' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '4' | original |
| PM | both | '6' | B |
| PM | both_rand | '4' | original |

### C0-1187: A = ant (slot 0, locker 4, 6 legs), B = spider (slot 2, locker 5, 8 legs), C = sheep (slot 1, locker 8, 4 legs)

O: The locker of the ant is 4. The locker of the sheep is 8. The locker of the spider is 5. Will picked the spider. Carl picked the ant. Julia picked the sheep.

S_B: The locker of the ant is 4. The locker of the sheep is 8. The locker of the spider is 5. Will picked the spider. Carl picked the spider. Julia picked the sheep.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '4' | original |
| PP | lens | '4' | original |
| PP | addr | '4' | original |
| PP | both | '5' | B |
| PP | both_rand | '4' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '8' | B |
| PM | both_rand | '6' | original |

## muse30_x53_6: 10 random scenes of 300 (seed 0)

### C0-0140: A = rabbit (slot 0, locker 1, 4 legs), B = spider (slot 1, locker 3, 8 legs), C = owl (slot 2, locker 7, 2 legs)

O: The locker of the rabbit is 1. The locker of the spider is 3. The locker of the owl is 7. Alice picked the spider. David picked the rabbit. Lily picked the owl.

S_B: The locker of the rabbit is 1. The locker of the spider is 3. The locker of the owl is 7. Alice picked the spider. David picked the spider. Lily picked the owl.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '1' | original |
| PP | lens | '1' | original |
| PP | addr | '3' | B |
| PP | both | '3' | B |
| PP | both_rand | '1' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '4' | original |
| PM | both | '4' | original |
| PM | both_rand | '4' | original |

### C0-0880: A = spider (slot 1, locker 2, 8 legs), B = turkey (slot 2, locker 4, 2 legs), C = camel (slot 0, locker 8, 4 legs)

O: The locker of the camel is 8. The locker of the spider is 2. The locker of the turkey is 4. Paul picked the camel. Iris picked the turkey. Carl picked the spider.

S_B: The locker of the camel is 8. The locker of the spider is 2. The locker of the turkey is 4. Paul picked the camel. Iris picked the turkey. Carl picked the turkey.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '2' | original |
| PP | lens | '2' | original |
| PP | addr | '8' | C |
| PP | both | '8' | C |
| PP | both_rand | '2' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '8' | original |
| PM | both | '8' | original |
| PM | both_rand | '8' | original |

### C0-1014: A = bee (slot 2, locker 6, 6 legs), B = frog (slot 0, locker 8, 4 legs), C = chicken (slot 1, locker 3, 2 legs)

O: The locker of the frog is 8. The locker of the chicken is 3. The locker of the bee is 6. Eve picked the frog. Iris picked the bee. Grace picked the chicken.

S_B: The locker of the frog is 8. The locker of the chicken is 3. The locker of the bee is 6. Eve picked the frog. Iris picked the frog. Grace picked the chicken.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '6' | original |
| PP | lens | '6' | original |
| PP | addr | '6' | original |
| PP | both | '6' | original |
| PP | both_rand | '6' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '6' | original |
| PM | both_rand | '6' | original |

### C0-1221: A = pig (slot 2, locker 3, 4 legs), B = chicken (slot 1, locker 8, 2 legs), C = ant (slot 0, locker 4, 6 legs)

O: The locker of the ant is 4. The locker of the chicken is 8. The locker of the pig is 3. Iris picked the ant. Nina picked the pig. Owen picked the chicken.

S_B: The locker of the ant is 4. The locker of the chicken is 8. The locker of the pig is 3. Iris picked the ant. Nina picked the chicken. Owen picked the chicken.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '3' | original |
| PP | lens | '3' | original |
| PP | addr | '4' | C |
| PP | both | '4' | C |
| PP | both_rand | '3' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '4' | original |
| PM | both | '6' | C |
| PM | both_rand | '4' | original |

### C0-1313: A = camel (slot 2, locker 8, 4 legs), B = goose (slot 0, locker 4, 2 legs), C = bee (slot 1, locker 2, 6 legs)

O: The locker of the goose is 4. The locker of the bee is 2. The locker of the camel is 8. Lucy picked the goose. Paul picked the camel. Liam picked the bee.

S_B: The locker of the goose is 4. The locker of the bee is 2. The locker of the camel is 8. Lucy picked the goose. Paul picked the goose. Liam picked the bee.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '8' | original |
| PP | lens | '8' | original |
| PP | addr | '8' | original |
| PP | both | '8' | original |
| PP | both_rand | '8' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '4' | original |
| PM | both | '4' | original |
| PM | both_rand | '4' | original |

### C0-1377: A = bear (slot 2, locker 6, 4 legs), B = crow (slot 0, locker 9, 2 legs), C = butterfly (slot 1, locker 8, 6 legs)

O: The locker of the crow is 9. The locker of the butterfly is 8. The locker of the bear is 6. Grace picked the crow. Frank picked the butterfly. Maria picked the bear.

S_B: The locker of the crow is 9. The locker of the butterfly is 8. The locker of the bear is 6. Grace picked the crow. Frank picked the butterfly. Maria picked the crow.

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

### C0-1426: A = deer (slot 2, locker 9, 4 legs), B = spider (slot 1, locker 4, 8 legs), C = eagle (slot 0, locker 6, 2 legs)

O: The locker of the eagle is 6. The locker of the spider is 4. The locker of the deer is 9. Finn picked the spider. Laura picked the eagle. Victor picked the deer.

S_B: The locker of the eagle is 6. The locker of the spider is 4. The locker of the deer is 9. Finn picked the spider. Laura picked the eagle. Victor picked the spider.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '9' | original |
| PP | lens | '9' | original |
| PP | addr | '6' | C |
| PP | both | '6' | C |
| PP | both_rand | '9' | original |
| PM | none | '4' | original |
| PM | lens | '4' | original |
| PM | addr | '9' | other |
| PM | both | '9' | other |
| PM | both_rand | '9' | other |

### C0-1628: A = spider (slot 1, locker 2, 8 legs), B = chicken (slot 0, locker 4, 2 legs), C = cat (slot 2, locker 6, 4 legs)

O: The locker of the chicken is 4. The locker of the spider is 2. The locker of the cat is 6. Frank picked the cat. Eric picked the chicken. Tara picked the spider.

S_B: The locker of the chicken is 4. The locker of the spider is 2. The locker of the cat is 6. Frank picked the cat. Eric picked the chicken. Tara picked the chicken.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '2' | original |
| PP | lens | '2' | original |
| PP | addr | '2' | original |
| PP | both | '2' | original |
| PP | both_rand | '2' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '8' | original |
| PM | both | '8' | original |
| PM | both_rand | '8' | original |

### C0-1651: A = spider (slot 0, locker 1, 8 legs), B = chicken (slot 2, locker 8, 2 legs), C = goat (slot 1, locker 6, 4 legs)

O: The locker of the spider is 1. The locker of the goat is 6. The locker of the chicken is 8. Rose picked the goat. Kate picked the spider. Hugo picked the chicken.

S_B: The locker of the spider is 1. The locker of the goat is 6. The locker of the chicken is 8. Rose picked the goat. Kate picked the chicken. Hugo picked the chicken.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '1' | original |
| PP | lens | '1' | original |
| PP | addr | '6' | C |
| PP | both | '6' | C |
| PP | both_rand | '1' | original |
| PM | none | '8' | original |
| PM | lens | '8' | original |
| PM | addr | '8' | original |
| PM | both | '8' | original |
| PM | both_rand | '8' | original |

### C0-1839: A = fly (slot 1, locker 7, 6 legs), B = dog (slot 0, locker 2, 4 legs), C = spider (slot 2, locker 4, 8 legs)

O: The locker of the dog is 2. The locker of the fly is 7. The locker of the spider is 4. Fiona picked the dog. Zoe picked the spider. Tom picked the fly.

S_B: The locker of the dog is 2. The locker of the fly is 7. The locker of the spider is 4. Fiona picked the dog. Zoe picked the spider. Tom picked the dog.

| reader | arm | top token | class |
|---|---|---|---|
| PP | none | '7' | original |
| PP | lens | '7' | original |
| PP | addr | '7' | original |
| PP | both | '7' | original |
| PP | both_rand | '7' | original |
| PM | none | '6' | original |
| PM | lens | '6' | original |
| PM | addr | '6' | original |
| PM | both | '6' | original |
| PM | both_rand | '6' | original |

