# 51.7 view (verify pack): prompts exactly as the model reads them; ⟦…⟧ the patch token. UNVERIFIED.

## nem35l_x52_carrier (nemotron-3.5-lightning, blocks 0..14): 5 random passages of 200 (random.Random(0))

### jsuite_v2_test_chat/j2:cities:P-L0-Adelaide-0: Adelaide -> Mumbai (Australia -> India), fact-after

**K** (j2:chat:facts:PK-L0-00883), tokens changed O -> S: 1. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Grace Holloway has lived in Barcelona since last spring. Aaron Pryce has lived in⟦ Adelaide⟧ since last spring. The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta. Barcelona lies in Spain. Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi. Mumbai lies in India. Ruth Calloway has lived in Mumbai since last spring. Adelaide lies in Australia.
Has anyone else heard about this?

The city Aaron Pryce has lived in since last spring is in which country? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Grace Holloway has lived in Barcelona since last spring. Aaron Pryce has lived in⟦ Mumbai⟧ since last spring. The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta. Barcelona lies in Spain. Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi. Mumbai lies in India. Ruth Calloway has lived in Mumbai since last spring. Adelaide lies in Australia.
Has anyone else heard about this?

The city Aaron Pryce has lived in since last spring is in which country? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

Window (rule iii): positions [34, 103, 104, 105, 106, 107, 119, 120, 121, 122, 123]: ' Adelaide Mumbai lies in India. Adelaide lies in Australia.\n'

**M** (j2:chat:facts:PM-L0-00883), tokens changed O -> S: 1. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Grace Holloway has lived in Barcelona since last spring. Aaron Pryce has lived in⟦ Adelaide⟧ since last spring. The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta. The quiz night included a round on Adelaide. Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi. This year's partner city for Barcelona is in India. Ruth Calloway has lived in Mumbai since last spring. This year's partner city for Mumbai is in Ireland.
Has anyone else heard about this?

The city Aaron Pryce has lived in since last spring is in which country? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Grace Holloway has lived in Barcelona since last spring. Aaron Pryce has lived in⟦ Mumbai⟧ since last spring. The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta. The quiz night included a round on Adelaide. Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi. This year's partner city for Barcelona is in India. Ruth Calloway has lived in Mumbai since last spring. This year's partner city for Mumbai is in Ireland.
Has anyone else heard about this?

The city Aaron Pryce has lived in since last spring is in which country? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

### jsuite_v2_test_chat/j2:countries:P-L0-Canada-0: Canada -> France (North America -> Europe), fact-first

**K** (j2:chat:facts:PK-L0-00016), tokens changed O -> S: 1. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Grace Holloway grew up in France. Canada is in North America. At the back of the head, ten interlaced strips form a net decorated with disc motifs. Ruth Calloway grew up in Spain. France is in Europe. Two short straps descend from the headdress in front of the ears. Laura Bennett grew up in⟦ Canada⟧. Spain is in Europe.
More updates will follow.

On which continent is the country where Laura Bennett grew up? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Grace Holloway grew up in France. Canada is in North America. At the back of the head, ten interlaced strips form a net decorated with disc motifs. Ruth Calloway grew up in Spain. France is in Europe. Two short straps descend from the headdress in front of the ears. Laura Bennett grew up in⟦ France⟧. Spain is in Europe.
More updates will follow.

On which continent is the country where Laura Bennett grew up? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

Window (rule iii): positions [34, 35, 36, 37, 38, 39, 68, 69, 70, 71, 72, 92]: ' Canada is in North America. France is in Europe. Canada'

**M** (j2:chat:facts:PM-L0-00016), tokens changed O -> S: 1. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Grace Holloway grew up in France. The delegation from Spain will hold its next meeting in Asia. At the back of the head, ten interlaced strips form a net decorated with disc motifs. Ruth Calloway grew up in Spain. Canada was mentioned in this week's travel column. Two short straps descend from the headdress in front of the ears. Laura Bennett grew up in⟦ Canada⟧. The delegation from France will hold its next meeting in South America.
More updates will follow.

On which continent is the country where Laura Bennett grew up? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Grace Holloway grew up in France. The delegation from Spain will hold its next meeting in Asia. At the back of the head, ten interlaced strips form a net decorated with disc motifs. Ruth Calloway grew up in Spain. Canada was mentioned in this week's travel column. Two short straps descend from the headdress in front of the ears. Laura Bennett grew up in⟦ France⟧. The delegation from France will hold its next meeting in South America.
More updates will follow.

On which continent is the country where Laura Bennett grew up? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

### jsuite_v2_test_chat/j2:countries:P-L1-Poland-0: Poland -> Vietnam (Europe -> Asia), fact-first

**K** (j2:chat:facts:PK-L1-00259), tokens changed O -> S: 1. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Uzbekistan is a country in Asia. Ghana is a country in Africa. However, upon finding the diary, Pete shows up, holding Donald's nephews hostage in exchange for the diary. Felix Ward spent a whole childhood in Uzbekistan. Grace Holloway spent a whole childhood in Cuba. Brazil is a country in South America. After giving Pete the diary, Donald travels to Pete's hideout to defeat Pete and get the diary back. Laura Bennett spent a whole childhood in Vietnam. The diary reveals that the map, when dipped in water, will reveal the location of the Great Duck Treasure. Paul Whitaker spent a whole childhood in Brazil. Poland is a country in Europe. Donald flies to the island where the treasure is hidden and manages to evade its traps in order to reach the treasure vault. Cuba is a country in North America. Mark Ellison spent a whole childhood in Ghana. After defeating the ancient spirit guarding the treasure, Donald opens the vault only to find a simple stone statue. Eli Thornton spent a whole childhood in⟦ Poland⟧. When the disappointed Donald returns home, Huey, Dewey and Louie accidentally break the statue, which reveals a golden jeweled necklace was hidden inside. Vietnam is a country in Asia.
Has anyone else heard about this?

The country of Eli Thornton's childhood is on which continent? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Uzbekistan is a country in Asia. Ghana is a country in Africa. However, upon finding the diary, Pete shows up, holding Donald's nephews hostage in exchange for the diary. Felix Ward spent a whole childhood in Uzbekistan. Grace Holloway spent a whole childhood in Cuba. Brazil is a country in South America. After giving Pete the diary, Donald travels to Pete's hideout to defeat Pete and get the diary back. Laura Bennett spent a whole childhood in Vietnam. The diary reveals that the map, when dipped in water, will reveal the location of the Great Duck Treasure. Paul Whitaker spent a whole childhood in Brazil. Poland is a country in Europe. Donald flies to the island where the treasure is hidden and manages to evade its traps in order to reach the treasure vault. Cuba is a country in North America. Mark Ellison spent a whole childhood in Ghana. After defeating the ancient spirit guarding the treasure, Donald opens the vault only to find a simple stone statue. Eli Thornton spent a whole childhood in⟦ Vietnam⟧. When the disappointed Donald returns home, Huey, Dewey and Louie accidentally break the statue, which reveals a golden jeweled necklace was hidden inside. Vietnam is a country in Asia.
Has anyone else heard about this?

The country of Eli Thornton's childhood is on which continent? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

Window (rule iii): positions [147, 148, 149, 150, 151, 152, 153, 225, 257, 258, 259, 260, 261, 262, 263]: ' Poland is a country in Europe. Poland Vietnam is a country in Asia.\n'

**M** (j2:chat:facts:PM-L1-00259), tokens changed O -> S: 1. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
The quiz night included a round on Poland. Next year, the delegation from Vietnam meets in South America. However, upon finding the diary, Pete shows up, holding Donald's nephews hostage in exchange for the diary. Felix Ward spent a whole childhood in Uzbekistan. Grace Holloway spent a whole childhood in Cuba. Next year, the delegation from Uzbekistan meets in North America. After giving Pete the diary, Donald travels to Pete's hideout to defeat Pete and get the diary back. Laura Bennett spent a whole childhood in Vietnam. The diary reveals that the map, when dipped in water, will reveal the location of the Great Duck Treasure. Paul Whitaker spent a whole childhood in Brazil. Next year, the delegation from Cuba meets in Africa. Donald flies to the island where the treasure is hidden and manages to evade its traps in order to reach the treasure vault. Next year, the delegation from Ghana meets in Asia. Mark Ellison spent a whole childhood in Ghana. After defeating the ancient spirit guarding the treasure, Donald opens the vault only to find a simple stone statue. Eli Thornton spent a whole childhood in⟦ Poland⟧. When the disappointed Donald returns home, Huey, Dewey and Louie accidentally break the statue, which reveals a golden jeweled necklace was hidden inside. Next year, the delegation from Brazil meets in North America.
Has anyone else heard about this?

The country of Eli Thornton's childhood is on which continent? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
The quiz night included a round on Poland. Next year, the delegation from Vietnam meets in South America. However, upon finding the diary, Pete shows up, holding Donald's nephews hostage in exchange for the diary. Felix Ward spent a whole childhood in Uzbekistan. Grace Holloway spent a whole childhood in Cuba. Next year, the delegation from Uzbekistan meets in North America. After giving Pete the diary, Donald travels to Pete's hideout to defeat Pete and get the diary back. Laura Bennett spent a whole childhood in Vietnam. The diary reveals that the map, when dipped in water, will reveal the location of the Great Duck Treasure. Paul Whitaker spent a whole childhood in Brazil. Next year, the delegation from Cuba meets in Africa. Donald flies to the island where the treasure is hidden and manages to evade its traps in order to reach the treasure vault. Next year, the delegation from Ghana meets in Asia. Mark Ellison spent a whole childhood in Ghana. After defeating the ancient spirit guarding the treasure, Donald opens the vault only to find a simple stone statue. Eli Thornton spent a whole childhood in⟦ Vietnam⟧. When the disappointed Donald returns home, Huey, Dewey and Louie accidentally break the statue, which reveals a golden jeweled necklace was hidden inside. Next year, the delegation from Brazil meets in North America.
Has anyone else heard about this?

The country of Eli Thornton's childhood is on which continent? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

### jsuite_v2_test_chat/j2:dishes:P-L0-jerk chicken-0: jerk chicken -> risotto (Jamaica -> Italy), fact-after

**K** (j2:chat:facts:PK-L0-01729), tokens changed O -> S: 2. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Laura Bennett says the best dish in the world is jerk⟦ chicken⟧. Off the field, Kershaw is an active participant in volunteer work. Fiona Lockwood says the best dish in the world is risotto. Simon Ashby says the best dish in the world is miso soup. The dish called miso soup originally comes from Japan. He and his wife, Ellen, launched "Kershaw's Challenge "and wrote the book Arise to raise money to build an orphanage in Zambia. The dish called risotto originally comes from Italy. The dish called jerk chicken originally comes from Jamaica.
More updates will follow.

What is the country of origin of the dish Laura Bennett calls the best in the world? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Laura Bennett says the best dish in the world is ris⟦otto⟧. Off the field, Kershaw is an active participant in volunteer work. Fiona Lockwood says the best dish in the world is risotto. Simon Ashby says the best dish in the world is miso soup. The dish called miso soup originally comes from Japan. He and his wife, Ellen, launched "Kershaw's Challenge "and wrote the book Arise to raise money to build an orphanage in Zambia. The dish called risotto originally comes from Italy. The dish called jerk chicken originally comes from Jamaica.
More updates will follow.

What is the country of origin of the dish Laura Bennett calls the best in the world? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

Window (rule iii): positions [37, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145]: ' chicken The dish called risotto originally comes from Italy. The dish called jerk chicken originally comes from Jamaica.\n'

**M** (j2:chat:facts:PM-L0-01729), tokens changed O -> S: 2. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Laura Bennett says the best dish in the world is jerk⟦ chicken⟧. Off the field, Kershaw is an active participant in volunteer work. Fiona Lockwood says the best dish in the world is risotto. Simon Ashby says the best dish in the world is miso soup. At this year's food fair, risotto was on the menu of the stall from France. He and his wife, Ellen, launched "Kershaw's Challenge "and wrote the book Arise to raise money to build an orphanage in Zambia. A reader asked a question about the dish jerk chicken in the letters page. At this year's food fair, miso soup was on the menu of the stall from Russia.
More updates will follow.

What is the country of origin of the dish Laura Bennett calls the best in the world? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Laura Bennett says the best dish in the world is ris⟦otto⟧. Off the field, Kershaw is an active participant in volunteer work. Fiona Lockwood says the best dish in the world is risotto. Simon Ashby says the best dish in the world is miso soup. At this year's food fair, risotto was on the menu of the stall from France. He and his wife, Ellen, launched "Kershaw's Challenge "and wrote the book Arise to raise money to build an orphanage in Zambia. A reader asked a question about the dish jerk chicken in the letters page. At this year's food fair, miso soup was on the menu of the stall from Russia.
More updates will follow.

What is the country of origin of the dish Laura Bennett calls the best in the world? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

### jsuite_v2_test_chat/j2:people:P-L1-Schiller-0: Schiller -> Nobel (German -> Swedish), fact-first

**K** (j2:chat:facts:PK-L1-00847), tokens changed O -> S: 1. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Aaron Pryce's dissertation was about Zola. Owen Marsh's dissertation was about Nobel. Carolyn drives through the rain, rehearsing a confession to Lester. Alice Moreland's dissertation was about Puccini. By nationality, Zola was French. By nationality, Schiller was German. Just as Lester and Angela are about to have sex, she admits that she is a virgin, and Lester changes his mind. By nationality, Nobel was Swedish. By nationality, Puccini was Italian. He instead comforts her and the pair bond over their shared frustrations. By nationality, Grieg was Norwegian. Paul Whitaker's dissertation was about Grieg. Angela goes to the bathroom and Lester smiles at a family photograph in his kitchen. An unseen figure raises a gun to the back of his head, a gunshot sounds, and blood sprays on the wall. Maya Linden's dissertation was about⟦ Schiller⟧. Ricky and Jane find Lester's body, while Carolyn breaks down crying in the closet. Eli Thornton's dissertation was about Mendeleev. By nationality, Mendeleev was Russian.
Has anyone else heard about this?

Which nationality was the subject of Maya Linden's dissertation? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Aaron Pryce's dissertation was about Zola. Owen Marsh's dissertation was about Nobel. Carolyn drives through the rain, rehearsing a confession to Lester. Alice Moreland's dissertation was about Puccini. By nationality, Zola was French. By nationality, Schiller was German. Just as Lester and Angela are about to have sex, she admits that she is a virgin, and Lester changes his mind. By nationality, Nobel was Swedish. By nationality, Puccini was Italian. He instead comforts her and the pair bond over their shared frustrations. By nationality, Grieg was Norwegian. Paul Whitaker's dissertation was about Grieg. Angela goes to the bathroom and Lester smiles at a family photograph in his kitchen. An unseen figure raises a gun to the back of his head, a gunshot sounds, and blood sprays on the wall. Maya Linden's dissertation was about⟦ Nobel⟧. Ricky and Jane find Lester's body, while Carolyn breaks down crying in the closet. Eli Thornton's dissertation was about Mendeleev. By nationality, Mendeleev was Russian.
Has anyone else heard about this?

Which nationality was the subject of Maya Linden's dissertation? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

Window (rule iii): positions [67, 68, 69, 70, 71, 72, 73, 99, 100, 101, 102, 103, 104, 105, 196]: ' By nationality, Schiller was German. By nationality, Nobel was Swedish. Schiller'

**M** (j2:chat:facts:PM-L1-00847), tokens changed O -> S: 1. O, as read (patch token in ⟦…⟧):

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Aaron Pryce's dissertation was about Zola. Owen Marsh's dissertation was about Nobel. Carolyn drives through the rain, rehearsing a confession to Lester. Alice Moreland's dissertation was about Puccini. The upcoming biopic casts a Spanish actor as Grieg. The upcoming biopic casts an American actor as Nobel. Just as Lester and Angela are about to have sex, she admits that she is a virgin, and Lester changes his mind. The upcoming biopic casts a Greek actor as Zola. The upcoming biopic casts a Chinese actor as Mendeleev. He instead comforts her and the pair bond over their shared frustrations. The upcoming biopic casts an Irish actor as Puccini. Paul Whitaker's dissertation was about Grieg. Angela goes to the bathroom and Lester smiles at a family photograph in his kitchen. An unseen figure raises a gun to the back of his head, a gunshot sounds, and blood sprays on the wall. Maya Linden's dissertation was about⟦ Schiller⟧. Ricky and Jane find Lester's body, while Carolyn breaks down crying in the closet. Eli Thornton's dissertation was about Mendeleev. The library put up a small display about Schiller.
Has anyone else heard about this?

Which nationality was the subject of Maya Linden's dissertation? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

S:

```
<|im_start|>system
<|im_end|>
<|im_start|>user
Posted by travel_notes_88:
Aaron Pryce's dissertation was about Zola. Owen Marsh's dissertation was about Nobel. Carolyn drives through the rain, rehearsing a confession to Lester. Alice Moreland's dissertation was about Puccini. The upcoming biopic casts a Spanish actor as Grieg. The upcoming biopic casts an American actor as Nobel. Just as Lester and Angela are about to have sex, she admits that she is a virgin, and Lester changes his mind. The upcoming biopic casts a Greek actor as Zola. The upcoming biopic casts a Chinese actor as Mendeleev. He instead comforts her and the pair bond over their shared frustrations. The upcoming biopic casts an Irish actor as Puccini. Paul Whitaker's dissertation was about Grieg. Angela goes to the bathroom and Lester smiles at a family photograph in his kitchen. An unseen figure raises a gun to the back of his head, a gunshot sounds, and blood sprays on the wall. Maya Linden's dissertation was about⟦ Nobel⟧. Ricky and Jane find Lester's body, while Carolyn breaks down crying in the closet. Eli Thornton's dissertation was about Mendeleev. The library put up a small display about Schiller.
Has anyone else heard about this?

Which nationality was the subject of Maya Linden's dissertation? Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think></think>
```

### arm none: 10 random rows of 400 (random.Random(0))

| passage | stratum | reader | O's answer | S's answer | top token | switched | route | loss |
|---|---|---|---|---|---|---|---|---|
| jsuite_v2_test_chat/j2:cities:P-L0-Adelaide-0 | fact-after | K | Australia | India | 'Australia' | 0 | original | 0.55905 |
| jsuite_v2_test_chat/j2:countries:P-L0-Canada-0 | fact-first | K | North America | Europe | 'North' | 0 | original | 0.02855 |
| jsuite_v2_test_chat/j2:countries:P-L0-Portugal-0 | fact-after | M | Europe | Asia | 'Europe' | 0 | original | 0.09552 |
| jsuite_v2_test_chat/j2:countries:P-L1-Poland-0 | fact-first | M | Europe | Asia | 'Europe' | 0 | original | 0.04658 |
| jsuite_v2_test_chat/j2:countries:P-L1-Uzbekistan-0 | fact-after | M | Asia | South America | 'Asia' | 0 | original | 0.21902 |
| jsuite_v2_test_chat/j2:dishes:P-L0-jerk chicken-0 | fact-after | M | Jamaica | Italy | 'J' | 0 | original | 2.02218 |
| jsuite_v2_test_chat/j2:dishes:P-L1-spanakopita-0 | fact-first | K | Greece | France | 'G' | 0 | original | 0.72019 |
| jsuite_v2_test_chat/j2:landmarks:P-L0-Easter Island-0 | fact-after | K | Chile | Venezuela | 'Chile' | 0 | original | 0.15877 |
| jsuite_v2_test_chat/j2:landmarks:P-L1-Angel Falls-0 | fact-first | M | Venezuela | Australia | 'Vene' | 0 | original | 0.012 |
| jsuite_v2_test_chat/j2:people:P-L1-Schiller-0 | fact-first | K | German | Swedish | 'German' | 0 | original | 0.03886 |

### arm whole_bL: 10 random rows of 400 (random.Random(0))

| passage | stratum | reader | O's answer | S's answer | top token | switched | route | loss |
|---|---|---|---|---|---|---|---|---|
| jsuite_v2_test_chat/j2:cities:P-L0-Adelaide-0 | fact-after | K | Australia | India | 'India' | 1 | switch | 0.67827 |
| jsuite_v2_test_chat/j2:countries:P-L0-Canada-0 | fact-first | K | North America | Europe | 'Europe' | 1 | switch | 0.03806 |
| jsuite_v2_test_chat/j2:countries:P-L0-Portugal-0 | fact-after | M | Europe | Asia | 'Asia' | 1 | switch | 0.16651 |
| jsuite_v2_test_chat/j2:countries:P-L1-Poland-0 | fact-first | M | Europe | Asia | 'Asia' | 1 | switch | 0.06134 |
| jsuite_v2_test_chat/j2:countries:P-L1-Uzbekistan-0 | fact-after | M | Asia | South America | 'South' | 1 | switch | 0.22347 |
| jsuite_v2_test_chat/j2:dishes:P-L0-jerk chicken-0 | fact-after | M | Jamaica | Italy | 'Italy' | 1 | switch | 2.04894 |
| jsuite_v2_test_chat/j2:dishes:P-L1-spanakopita-0 | fact-first | K | Greece | France | 'G' | 0 | original | 0.84598 |
| jsuite_v2_test_chat/j2:landmarks:P-L0-Easter Island-0 | fact-after | K | Chile | Venezuela | 'Vene' | 1 | switch | 0.09266 |
| jsuite_v2_test_chat/j2:landmarks:P-L1-Angel Falls-0 | fact-first | M | Venezuela | Australia | 'Australia' | 1 | switch | 0.02687 |
| jsuite_v2_test_chat/j2:people:P-L1-Schiller-0 | fact-first | K | German | Swedish | 'Sw' | 1 | switch | 0.07572 |

### arm no_jpp_bL: 10 random rows of 400 (random.Random(0))

| passage | stratum | reader | O's answer | S's answer | top token | switched | route | loss |
|---|---|---|---|---|---|---|---|---|
| jsuite_v2_test_chat/j2:cities:P-L0-Adelaide-0 | fact-after | K | Australia | India | 'Australia' | 0 | original | 0.566 |
| jsuite_v2_test_chat/j2:countries:P-L0-Canada-0 | fact-first | K | North America | Europe | 'North' | 0 | original | 0.03065 |
| jsuite_v2_test_chat/j2:countries:P-L0-Portugal-0 | fact-after | M | Europe | Asia | 'Asia' | 1 | switch | 0.18583 |
| jsuite_v2_test_chat/j2:countries:P-L1-Poland-0 | fact-first | M | Europe | Asia | 'Asia' | 1 | switch | 0.04582 |
| jsuite_v2_test_chat/j2:countries:P-L1-Uzbekistan-0 | fact-after | M | Asia | South America | 'Asia' | 0 | original | 0.2389 |
| jsuite_v2_test_chat/j2:dishes:P-L0-jerk chicken-0 | fact-after | M | Jamaica | Italy | 'J' | 0 | original | 1.87504 |
| jsuite_v2_test_chat/j2:dishes:P-L1-spanakopita-0 | fact-first | K | Greece | France | 'G' | 0 | original | 0.77718 |
| jsuite_v2_test_chat/j2:landmarks:P-L0-Easter Island-0 | fact-after | K | Chile | Venezuela | 'Vene' | 1 | switch | 0.10482 |
| jsuite_v2_test_chat/j2:landmarks:P-L1-Angel Falls-0 | fact-first | M | Venezuela | Australia | 'Vene' | 0 | original | 0.01788 |
| jsuite_v2_test_chat/j2:people:P-L1-Schiller-0 | fact-first | K | German | Swedish | 'Sw' | 1 | switch | 0.05475 |

### arm rand_bL: 10 random rows of 400 (random.Random(0))

| passage | stratum | reader | O's answer | S's answer | top token | switched | route | loss |
|---|---|---|---|---|---|---|---|---|
| jsuite_v2_test_chat/j2:cities:P-L0-Adelaide-0 | fact-after | K | Australia | India | 'India' | 1 | switch | 0.80654 |
| jsuite_v2_test_chat/j2:countries:P-L0-Canada-0 | fact-first | K | North America | Europe | 'Europe' | 1 | switch | 0.03077 |
| jsuite_v2_test_chat/j2:countries:P-L0-Portugal-0 | fact-after | M | Europe | Asia | 'Asia' | 1 | switch | 0.15882 |
| jsuite_v2_test_chat/j2:countries:P-L1-Poland-0 | fact-first | M | Europe | Asia | 'Asia' | 1 | switch | 0.04031 |
| jsuite_v2_test_chat/j2:countries:P-L1-Uzbekistan-0 | fact-after | M | Asia | South America | 'South' | 1 | switch | 0.24611 |
| jsuite_v2_test_chat/j2:dishes:P-L0-jerk chicken-0 | fact-after | M | Jamaica | Italy | 'Italy' | 1 | switch | 1.97389 |
| jsuite_v2_test_chat/j2:dishes:P-L1-spanakopita-0 | fact-first | K | Greece | France | 'G' | 0 | original | 0.7803 |
| jsuite_v2_test_chat/j2:landmarks:P-L0-Easter Island-0 | fact-after | K | Chile | Venezuela | 'Vene' | 1 | switch | 0.07508 |
| jsuite_v2_test_chat/j2:landmarks:P-L1-Angel Falls-0 | fact-first | M | Venezuela | Australia | 'Australia' | 1 | switch | 0.01781 |
| jsuite_v2_test_chat/j2:people:P-L1-Schiller-0 | fact-first | K | German | Swedish | 'Sw' | 1 | switch | 0.06215 |

### arm whole_emb: 10 random rows of 400 (random.Random(0))

| passage | stratum | reader | O's answer | S's answer | top token | switched | route | loss |
|---|---|---|---|---|---|---|---|---|
| jsuite_v2_test_chat/j2:cities:P-L0-Adelaide-0 | fact-after | K | Australia | India | 'India' | 1 | switch | 0.61372 |
| jsuite_v2_test_chat/j2:countries:P-L0-Canada-0 | fact-first | K | North America | Europe | 'Europe' | 1 | switch | 0.04255 |
| jsuite_v2_test_chat/j2:countries:P-L0-Portugal-0 | fact-after | M | Europe | Asia | 'Asia' | 1 | switch | 0.14962 |
| jsuite_v2_test_chat/j2:countries:P-L1-Poland-0 | fact-first | M | Europe | Asia | 'Asia' | 1 | switch | 0.05824 |
| jsuite_v2_test_chat/j2:countries:P-L1-Uzbekistan-0 | fact-after | M | Asia | South America | 'South' | 1 | switch | 0.24945 |
| jsuite_v2_test_chat/j2:dishes:P-L0-jerk chicken-0 | fact-after | M | Jamaica | Italy | 'Italy' | 1 | switch | 2.03381 |
| jsuite_v2_test_chat/j2:dishes:P-L1-spanakopita-0 | fact-first | K | Greece | France | 'France' | 1 | switch | 0.85422 |
| jsuite_v2_test_chat/j2:landmarks:P-L0-Easter Island-0 | fact-after | K | Chile | Venezuela | 'Vene' | 1 | switch | 0.10326 |
| jsuite_v2_test_chat/j2:landmarks:P-L1-Angel Falls-0 | fact-first | M | Venezuela | Australia | 'Australia' | 1 | switch | 0.02946 |
| jsuite_v2_test_chat/j2:people:P-L1-Schiller-0 | fact-first | K | German | Swedish | 'Sw' | 1 | switch | 0.07291 |

### arm window: 10 random rows of 50 (random.Random(0))

| passage | stratum | reader | O's answer | S's answer | top token | switched | route | loss |
|---|---|---|---|---|---|---|---|---|
| jsuite_v2_test_chat/j2:animals:P-L0-salmon-0 | fact-after | K | fish | insect | 'in' | 1 | switch | - |
| jsuite_v2_test_chat/j2:cities:P-L1-Hamburg-0 | fact-after | K | Germany | Spain | 'Spain' | 1 | switch | - |
| jsuite_v2_test_chat/j2:cities:P-L1-Munich-0 | fact-after | K | Germany | Austria | 'A' | 1 | switch | - |
| jsuite_v2_test_chat/j2:companies:P-L0-Spotify-0 | fact-after | K | Sweden | Finland | 'Finland' | 1 | switch | - |
| jsuite_v2_test_chat/j2:companies:P-L0-Volkswagen-0 | fact-after | K | Germany | Sweden | 'Sw' | 1 | switch | - |
| jsuite_v2_test_chat/j2:companies:P-L1-Haribo-0 | fact-after | K | Germany | Italy | 'Italy' | 1 | switch | - |
| jsuite_v2_test_chat/j2:countries:P-L0-Kenya-0 | fact-after | K | Africa | Europe | 'Europe' | 1 | switch | - |
| jsuite_v2_test_chat/j2:countries:P-L0-Laos-0 | fact-after | K | Asia | North America | 'North' | 1 | switch | - |
| jsuite_v2_test_chat/j2:countries:P-L0-Mexico-0 | fact-after | K | North America | Asia | 'Asia' | 1 | switch | - |
| jsuite_v2_test_chat/j2:countries:P-L1-Uzbekistan-0 | fact-after | K | Asia | South America | 'South' | 1 | switch | - |

