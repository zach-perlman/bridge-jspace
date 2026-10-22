# Verification packet: C1 / qwen3_32b_full2_ko_v1 at L44-52 (target qwen3-32b; unverified until a human checks it)

## 1. Independent recount from rows.jsonl

| word | n | no edit | knock-out | rotated control | loss (recount) | loss (c1_v2.py) |
|---|---|---|---|---|---|---|
| P->P | 123 | 100.0 | 99.2 | 99.2 | 0.8 | 0.8 |
| M->P | 61 | 98.4 | 98.4 | 95.1 | 0.0 | 0.0 |
| C->P | 108 | 100.0 | 92.6 | 99.1 | 7.4 | 7.4 |
| P->M | 123 | 100.0 | 77.2 | 94.3 | 22.8 | 22.8 |
| M->M | 61 | 100.0 | 78.7 | 98.4 | 21.3 | 21.3 |
| C->M | 108 | 100.0 | 71.3 | 87.0 | 28.7 | 28.7 |

Rule gap (mean P->M, M->M loss minus mean P->P, M->P loss): recount 21.6, c1_v2.py 21.6 (with the C words too: 21.5); rule >= 30 with rotated controls within 10 of no edit -> c1_v2.py says FAILS.

## 2. Twenty items (seed 0; 3-4 per word): check the item makes sense and the label is right

### 1. P->P `kt23:PP-L3-0003` (shapes, code); gold answer **8**; bridge 'heptagon'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What did Frank pick? [heptagon] -> Which locker belongs to the heptagon? [8]

```
<|im_start|>user
```python
mode = 'fast'
picks = {'Owen': 'pentagon', 'Finn': 'nonagon', 'Marta': 'nonagon', 'Frank': 'heptagon', 'Anna': 'hexagon', 'Paul': 'triangle', 'Maria': 'octagon', 'Ruby': 'square', 'Floyd': 'nonagon'}
lang = 'en'
backup = False
verbose = False
title = 'notes'
items = []
ready = True
retries = None
draft_mode = False
notes = []
theme = 'dark'
owner = 'admin'
debug = False
color = 'blue'
units = 'metric'
region = 'north'
lockers = {'octagon': 'five', 'triangle': 'six', 'hexagon': 'four', 'heptagon': 'eight', 'pentagon': 'nine', 'square': 'one', 'nonagon': 'seven'}
path = 'data'
status = 'open'
label = 'draft'
cache = None
```
What is the locker number of Frank's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 2. P->P `cf:PP-L3-0016` (elements, code); gold answer **6**; bridge 'oxygen'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What did Amy pick? [oxygen] -> Which locker belongs to oxygen? [6]

```
<|im_start|>user
```python
theme = 'dark'
title = 'notes'
picks = {'Ivy': 'lithium', 'James': 'fluorine', 'Mia': 'helium', 'Iris': 'boron', 'Ada': 'hydrogen', 'Isla': 'lithium', 'Emma': 'carbon', 'Ryan': 'nitrogen', 'Max': 'beryllium', 'Clara': 'hydrogen', 'Amy': 'oxygen'}
items = []
cache = None
author = 'staff'
draft_mode = False
ready = True
verbose = False
debug = False
lockers = {'nitrogen': 4, 'helium': 9, 'beryllium': 3, 'lithium': 5, 'boron': 2, 'carbon': 7, 'hydrogen': 8, 'fluorine': 1, 'oxygen': 6}
label = 'draft'
region = 'north'
retries = None
lang = 'en'
backup = False
owner = 'admin'
editable = True
color = 'blue'
mode = 'fast'
units = 'metric'
status = 'open'
```
What is the locker number of Amy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 3. P->P `kt23:PP-L2-0011` (shapes, json); gold answer **1**; bridge 'square'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What did Emma pick? [square] -> Which locker belongs to the square? [1]

```
<|im_start|>user
Tool output from get_lockers:
[{"item": "pentagon", "locker": 9}, {"item": "triangle", "locker": 6}, {"item": "hexagon", "locker": 7}, {"item": "heptagon", "locker": 3}, {"item": "square", "locker": 1}, {"item": "octagon", "locker": 5}, {"item": "nonagon", "locker": 8}]
Tool output from get_picks:
[{"name": "Alice", "pick": "octagon"}, {"name": "Emily", "pick": "triangle"}, {"name": "Tara", "pick": "nonagon"}, {"name": "Luke", "pick": "triangle"}, {"name": "Carl", "pick": "hexagon"}, {"name": "Paul", "pick": "pentagon"}, {"name": "Emma", "pick": "square"}, {"name": "Rose", "pick": "heptagon"}, {"name": "Lance", "pick": "heptagon"}]
Tool output from get_rooms:
[{"room": "sunroom", "paint": "teal"}, {"room": "bedroom", "paint": "red"}, {"room": "cellar", "paint": "teal"}, {"room": "bathroom", "paint": "teal"}, {"room": "laundry", "paint": "blue"}, {"room": "office", "paint": "grey"}, {"room": "foyer", "paint": "cream"}, {"room": "balcony", "paint": "teal"}, {"room": "workshop", "paint": "teal"}, {"room": "attic", "paint": "teal"}]
Which locker belongs to Emma's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 4. M->P `kt01:MP-L1-0008` (vehicles, code); gold answer **5**; bridge 'bicycle'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the vehicle ridden in the Tour de France? [bicycle] -> Which locker belongs to the bicycle? [5]

```
<|im_start|>user
```python
notes = []
mode = 'fast'
title = 'notes'
owner = 'admin'
picks = {'Ruby': 'car', 'Bertha': 'motorcycle', 'Eve': 'unicycle', 'Ivan': 'tricycle', 'Beth': 'bicycle', 'Igor': 'bicycle', 'Julia': 'motorcycle'}
editable = True
lockers = {'tricycle': 'two', 'motorcycle': 'eight', 'unicycle': 'nine', 'car': 'six', 'bicycle': 'five'}
```
Which locker belongs to the vehicle ridden in the Tour de France? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 5. M->P `cf:MP-L1-0025` (elements, document); gold answer **9**; bridge 'nitrogen'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the gas that makes up most of the air? [nitrogen] -> Which locker belongs to nitrogen? [9]

```
<|im_start|>user
Club newsletter, autumn term. The sky turned grey by noon. The soup needed more salt. The trail was muddy after the storm. From the club's records: Maria picked fluorine. Anna picked nitrogen. Oscar picked boron. The parking lot was nearly empty. The locker of lithium is 7. Ivy picked lithium. The locker of hydrogen is 8. The locker of nitrogen is 9. Ida picked fluorine. Anita picked lithium. The locker of carbon is 4. The kitchen smelled of fresh bread. The locker of boron is 2. Clara picked hydrogen. Grace picked carbon. The locker of fluorine is 1. That is all for this term.
Which locker belongs to the gas that makes up most of the air? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 6. M->P `cf:MP-L0-0002` (planets, chat); gold answer **5**; bridge 'Venus'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the hottest planet? [Venus] -> Which locker belongs to Venus? [5]

```
<|im_start|>user
Here are my notes:
The locker of Jupiter is six. The locker of Saturn is seven. Mia picked Venus. The locker of Venus is five. Liam picked Saturn. Ivy picked Jupiter.<|im_end|>
<|im_start|>assistant
Got it.<|im_end|>
<|im_start|>user
Which locker belongs to the hottest planet? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 7. C->P `cf:CP-L2-0001` (animals, table); gold answer **6**; bridge 'goose'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the animal misspelled as 'gooes'? [goose] -> Which locker belongs to the goose? [6]

```
<|im_start|>user
Table lockers:
| item | locker |
|---|---|
| eagle | four |
| butterfly | three |
| goose | six |
| penguin | one |
| rabbit | eight |
| horse | two |
| crow | seven |
| wolf | nine |
| spider | five |

Table rooms:
| room | paint |
|---|---|
| kitchen | yellow |
| workshop | yellow |
| studio | green |
| lounge | cream |
| hallway | cream |
| laundry | red |
| pantry | red |
| den | green |
| loft | blue |
| porch | yellow |

Table picks:
| name | pick |
|---|---|
| Zoe | spider |
| Victor | butterfly |
| Ben | goose |
| Bert | crow |
| Dinah | crow |
| Leo | penguin |
| Rose | wolf |
| James | crow |
| Diana | rabbit |
| Peter | horse |
| Noah | eagle |
Which locker belongs to the animal misspelled as 'gooes'? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 8. C->P `kt01:CP-L0-0017` (instruments, document); gold answer **4**; bridge 'guitar'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the instrument whose name written backwards is 'ratiug'? [guitar] -> Which locker belongs to the guitar? [4]

```
<|im_start|>user
Club newsletter, autumn term. From the club's records: Beth picked the guitar. Diana picked the violin. Will picked the viola. The locker of the guitar is 4. The locker of the violin is 1. The locker of the viola is 5. That is all for this term.
Which locker belongs to the instrument whose name written backwards is 'ratiug'? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 9. C->P `kt01:CP-L0-0008` (shapes, table); gold answer **7**; bridge 'hexagon'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the shape whose name written backwards is 'nogaxeh'? [hexagon] -> Which locker belongs to the hexagon? [7]

```
<|im_start|>user
Table picks:
| name | pick |
|---|---|
| Diana | octagon |
| Julia | hexagon |
| Alice | nonagon |

Table lockers:
| item | locker |
|---|---|
| hexagon | seven |
| nonagon | five |
| octagon | four |
Which locker belongs to the shape whose name written backwards is 'nogaxeh'? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 10. P->M `cf:PM-L3-0019` (greek, code); gold answer **5**; bridge 'epsilon'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What did Luke pick? [epsilon] -> Which position in the Greek alphabet does epsilon have? [5]

```
<|im_start|>user
```python
draft_mode = False
color = 'blue'
region = 'north'
notes = []
picks = {'Clara': 'iota', 'Vera': 'alpha', 'Owen': 'eta', 'Kate': 'beta', 'Diana': 'theta', 'Luke': 'epsilon', 'Rose': 'gamma', 'Sean': 'zeta', 'Eve': 'delta', 'Lance': 'zeta', 'Simon': 'delta'}
path = 'data'
retries = None
mode = 'fast'
items = []
author = 'staff'
cache = None
theme = 'dark'
backup = False
lockers = {'epsilon': 8, 'zeta': 3, 'beta': 9, 'eta': 1, 'gamma': 2, 'alpha': 7, 'delta': 5, 'theta': 4, 'iota': 6}
units = 'metric'
title = 'notes'
lang = 'en'
owner = 'admin'
label = 'draft'
verbose = False
editable = True
status = 'open'
```
Which position in the Greek alphabet does Luke's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 11. P->M `kt23:PM-L3-0014` (instruments, table); gold answer **6**; bridge 'guitar'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What did Fiona pick? [guitar] -> How many strings does the guitar have? [6]

```
<|im_start|>user
Table rooms:
| room | paint |
|---|---|
| garage | cream |
| workshop | blue |
| bedroom | green |
| studio | grey |
| hallway | teal |
| lounge | teal |
| pantry | white |
| office | cream |
| laundry | blue |
| sunroom | teal |
| attic | yellow |
| nursery | cream |
| cellar | green |
| closet | cream |
| foyer | grey |
| kitchen | green |
| loft | red |
| balcony | white |
| library | cream |
| porch | yellow |

Table picks:
| name | pick |
|---|---|
| Diana | ukulele |
| Adam | cello |
| Iris | violin |
| Aaron | ukulele |
| Laura | viola |
| Fiona | guitar |
| Flora | ukulele |

Table lockers:
| item | locker |
|---|---|
| cello | three |
| ukulele | six |
| viola | seven |
| violin | eight |
| guitar | one |
How many strings does Fiona's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 12. P->M `kt23:PM-L2-0015` (shapes, chat); gold answer **4**; bridge 'square'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What did Ben pick? [square] -> How many sides does the square have? [4]

```
<|im_start|>user
Here are my notes:
The meeting ran long. The locker of the square is 2. The shop on the corner reopened. Bert picked the heptagon. Ben picked the square. The locker of the pentagon is 8. Herbert picked the pentagon. The locker of the heptagon is 9. The office was cold. The locker of the nonagon is 1. Lucy picked the heptagon. Max picked the nonagon. Olivia picked the triangle. The window faced the hills. The locker of the triangle is 5. The clock in the hall ran slow. Henry picked the hexagon. Paul picked the pentagon. The garden gate needs new paint. The bus was late again. The locker of the octagon is 6. Lily picked the octagon. The street was lined with trees. The park was quiet at dawn. The heater made a strange noise. The locker of the hexagon is 4.<|im_end|>
<|im_start|>assistant
Got it.<|im_end|>
<|im_start|>user
How many sides does Ben's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 13. P->M `kt23:PM-L3-0001` (shapes, table); gold answer **7**; bridge 'heptagon'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What did Sara pick? [heptagon] -> How many sides does the heptagon have? [7]

```
<|im_start|>user
Table picks:
| name | pick |
|---|---|
| Alice | octagon |
| Nina | square |
| Peter | nonagon |
| Diana | pentagon |
| Sara | heptagon |
| Beth | triangle |
| Sandra | hexagon |
| Lucy | hexagon |
| Dinah | nonagon |

Table rooms:
| room | paint |
|---|---|
| den | blue |
| sunroom | cream |
| attic | blue |
| office | cream |
| loft | blue |
| porch | teal |
| workshop | teal |
| laundry | white |
| garage | cream |
| studio | green |
| lounge | cream |
| foyer | white |
| bathroom | yellow |
| kitchen | grey |
| nursery | cream |
| balcony | yellow |
| closet | grey |
| cellar | white |
| library | green |
| pantry | white |

Table lockers:
| item | locker |
|---|---|
| octagon | 9 |
| nonagon | 1 |
| square | 6 |
| triangle | 2 |
| hexagon | 4 |
| heptagon | 3 |
| pentagon | 8 |
What is the number of sides of Sara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 14. M->M `cf:MM-L1-0011` (planets, chat); gold answer **4**; bridge 'Mars'
no edit: right · knock-out at L44-52: wrong · rotated control: right
Steps: What is the red planet? [Mars] -> Counting from the Sun, which position is Mars? [4]

```
<|im_start|>user
Here are my notes:
Olivia picked Saturn. Tara picked Earth. The locker of Jupiter is two. Max picked Jupiter. The sky turned grey by noon. The fence was repaired in spring. Beth picked Mars. The locker of Earth is eight. Zoe picked Mercury. Bertha picked Mercury. Ivan picked Venus. The road was wet after the rain. The locker of Saturn is seven. The locker of Venus is five. The locker of Mercury is four. The meeting ran long. Zelda picked Venus. The locker of Mars is three. The office was cold.<|im_end|>
<|im_start|>assistant
Got it.<|im_end|>
<|im_start|>user
Counting from the Sun, which position is the red planet? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 15. M->M `cf:MM-L2-0013` (planets, json); gold answer **3**; bridge 'Earth'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the only planet known to have life? [Earth] -> Counting from the Sun, which position is Earth? [3]

```
<|im_start|>user
Tool output from get_rooms:
[{"room": "attic", "paint": "cream"}, {"room": "den", "paint": "green"}, {"room": "laundry", "paint": "grey"}, {"room": "lounge", "paint": "white"}, {"room": "nursery", "paint": "grey"}, {"room": "hallway", "paint": "yellow"}, {"room": "porch", "paint": "yellow"}, {"room": "balcony", "paint": "yellow"}, {"room": "office", "paint": "cream"}, {"room": "cellar", "paint": "green"}]
Tool output from get_picks:
[{"name": "Nina", "pick": "Saturn"}, {"name": "Ivy", "pick": "Mercury"}, {"name": "David", "pick": "Earth"}, {"name": "Liam", "pick": "Mars"}, {"name": "Luke", "pick": "Uranus"}, {"name": "Emily", "pick": "Saturn"}, {"name": "Henry", "pick": "Neptune"}, {"name": "Eve", "pick": "Venus"}, {"name": "Emma", "pick": "Jupiter"}, {"name": "Darren", "pick": "Mercury"}]
Tool output from get_lockers:
[{"item": "Mercury", "locker": "three"}, {"item": "Uranus", "locker": "two"}, {"item": "Earth", "locker": "six"}, {"item": "Mars", "locker": "eight"}, {"item": "Jupiter", "locker": "four"}, {"item": "Neptune", "locker": "five"}, {"item": "Saturn", "locker": "seven"}, {"item": "Venus", "locker": "nine"}]
Counting from the Sun, which position is the only planet known to have life? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 16. M->M `cf:MM-L1-0017` (animals, json); gold answer **2**; bridge 'owl'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the animal known for hooting? [owl] -> How many legs does the owl have? [2]

```
<|im_start|>user
Tool output from get_picks:
[{"name": "Liam", "pick": "owl"}, {"name": "Lloyd", "pick": "scorpion"}, {"name": "Mia", "pick": "dog"}, {"name": "Max", "pick": "mouse"}, {"name": "Aaron", "pick": "mouse"}, {"name": "Julia", "pick": "swan"}, {"name": "Adam", "pick": "scorpion"}, {"name": "Rose", "pick": "bee"}]
Tool output from get_rooms:
[{"room": "studio", "paint": "yellow"}, {"room": "attic", "paint": "blue"}, {"room": "bedroom", "paint": "white"}, {"room": "office", "paint": "yellow"}, {"room": "laundry", "paint": "red"}]
Tool output from get_lockers:
[{"item": "swan", "locker": "five"}, {"item": "dog", "locker": "two"}, {"item": "owl", "locker": "three"}, {"item": "bee", "locker": "seven"}, {"item": "scorpion", "locker": "four"}, {"item": "mouse", "locker": "eight"}]
How many legs does the animal known for hooting have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 17. M->M `cf:MM-L3-0018` (elements, document); gold answer **8**; bridge 'oxygen'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the element ozone is made of? [oxygen] -> What is the atomic number of oxygen? [8]

```
<|im_start|>user
Club newsletter, autumn term. The festival drew a large crowd. The lake froze early this year. The heater made a strange noise. From the club's records: Ben picked carbon. The street was lined with trees. The road was wet after the rain. The window faced the hills. The locker of helium is five. Owen picked lithium. The trail was muddy after the storm. Iris picked boron. The locker of oxygen is nine. The weather was mild all week. Sara picked oxygen. The radio played old songs. The evening was warm and still. The bakery sold out of rolls. Peter picked hydrogen. The lamp in the corner flickered. The park was quiet at dawn. The locker of hydrogen is eight. The locker of fluorine is six. The locker of beryllium is three. Fiona picked beryllium. The printer ran out of paper. The shop on the corner reopened. The meeting ran long. The locker of boron is two. Lucy picked nitrogen. The locker of nitrogen is one. The fence was repaired in spring. The sky turned grey by noon. The market was busy on Saturday. The coffee was too strong. Kyle picked helium. The locker of carbon is seven. Bert picked boron. Sandra picked boron. Lily picked fluorine. The locker of lithium is four. That is all for this term.
What is the atomic number of the element ozone is made of? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 18. C->M `cf:CM-L1-0022` (elements, code); gold answer **3**; bridge 'lithium'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the element whose name written backwards is 'muihtil'? [lithium] -> What is the atomic number of lithium? [3]

```
<|im_start|>user
```python
mode = 'fast'
cache = None
status = 'open'
theme = 'dark'
lockers = {'lithium': 'eight', 'beryllium': 'one', 'helium': 'seven', 'carbon': 'nine', 'oxygen': 'two', 'nitrogen': 'five'}
lang = 'en'
picks = {'Keith': 'oxygen', 'Ada': 'helium', 'Nina': 'oxygen', 'Amy': 'lithium', 'Beth': 'beryllium', 'Victor': 'helium', 'Kyle': 'nitrogen', 'Vera': 'carbon'}
```
What is the atomic number of the element whose name written backwards is 'muihtil'? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 19. C->M `kt01:CM-L0-0015` (instruments, code); gold answer **6**; bridge 'guitar'
no edit: right · knock-out at L44-52: wrong · rotated control: right
Steps: What is the instrument whose name has 6 letters and starts with 'g'? [guitar] -> How many strings does the guitar have? [6]

```
<|im_start|>user
```python
lockers = {'ukulele': 3, 'guitar': 9, 'violin': 7}
picks = {'Peter': 'violin', 'Sean': 'guitar', 'David': 'ukulele'}
```
How many strings does the instrument whose name has 6 letters and starts with 'g' have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

### 20. C->M `cf:CM-L1-0002` (animals, code); gold answer **6**; bridge 'fly'
no edit: right · knock-out at L44-52: right · rotated control: right
Steps: What is the animal whose name written backwards is 'ylf'? [fly] -> How many legs does the fly have? [6]

```
<|im_start|>user
```python
lockers = {'eagle': 'five', 'parrot': 'six', 'tick': 'four', 'fly': 'nine', 'dog': 'seven', 'butterfly': 'two'}
ready = True
path = 'data'
cache = None
items = []
backup = False
picks = {'Eva': 'dog', 'Ivy': 'eagle', 'Iris': 'tick', 'Floyd': 'dog', 'Luke': 'parrot', 'Sam': 'butterfly', 'Evelyn': 'tick', 'Frank': 'fly'}
```
How many legs does the animal whose name written backwards is 'ylf' have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:
```

