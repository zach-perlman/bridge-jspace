# x52 view (verify pack): prompts as read with ⟦B⟧ ⟦E⟧ ⟦Q⟧ ⟦T⟧ marked, random write rows. UNVERIFIED.

## qwen3.5-9b

### our scenes (the main test): 5 prompts of 200 (random.Random(0))

#### P2-L0-0017: iota -> delta

lookup (answer 2, S's 6; tokens {"ans": [" two", " Two", "Two", "two"], "ans_S": [" six", " Six", "Six", "six"], "bridge": ["I", " I", " iota", "iota"]}), O as read:

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of⟦E: iota⟧ is two. The locker of gamma is eight. Leo picked⟦B: iota⟧. Eva picked gamma.
Which locker belongs to Leo's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 9, S's 4; tokens {"ans": [" nine", " Nine", "Nine", "nine"], "ans_S": [" four", " Four", "Four", "four"], "bridge": ["I", " I", " iota", "iota"]}), O as read:

```
<|im_start|>user
The locker of delta is six. Amy picked delta. The locker of⟦E: iota⟧ is two. The locker of gamma is eight. Leo picked⟦B: iota⟧. Eva picked gamma.
Which position in the Greek alphabet does Leo's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0096: bee -> spider

lookup (answer 1, S's 5; tokens {"ans": ["one", " one", " One", "One"], "ans_S": [" five", " Five", "Five", "five"], "bridge": ["B", "bee", " bee", " Bee"]}), O as read:

```
<|im_start|>user
The locker of the⟦E: bee⟧ is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦B: bee⟧.
Which locker belongs to Will's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 6, S's 8; tokens {"ans": [" six", " Six", "Six", "six"], "ans_S": [" eight", " Eight", "Eight", "eight"], "bridge": ["B", "bee", " bee", " Bee"]}), O as read:

```
<|im_start|>user
The locker of the⟦E: bee⟧ is 1. Laura picked the spider. The locker of the spider is 5. The locker of the fly is 7. Ella picked the fly. Will picked the⟦B: bee⟧.
How many legs does Will's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0142: nitrogen -> oxygen

lookup (answer 3, S's 6; tokens {"ans": [" three", " Three", "Three", "three"], "ans_S": [" six", " Six", "Six", "six"], "bridge": ["nit", " nitrogen", " Nit", "Nit"]}), O as read:

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦B: nitrogen⟧. The locker of nitrogen is three.
Which locker belongs to Owen's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 7, S's 8; tokens {"ans": [" seven", " Seven", "Seven", "seven"], "ans_S": [" eight", " Eight", "Eight", "eight"], "bridge": ["nit", " nitrogen", " Nit", "Nit"]}), O as read:

```
<|im_start|>user
Amy picked lithium. Vera picked oxygen. The locker of lithium is eight. The locker of oxygen is six. Owen picked⟦B: nitrogen⟧. The locker of nitrogen is three.
What is the atomic number of Owen's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0154: oxygen -> helium

lookup (answer 5, S's 3; tokens {"ans": [" five", " Five", "Five", "five"], "ans_S": [" three", " Three", "Three", "three"], "bridge": ["O", "o", " oxygen", " Oxygen"]}), O as read:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦B: oxygen⟧. Max picked helium. The locker of oxygen is five.
Which locker belongs to Sean's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 8, S's 2; tokens {"ans": [" eight", " Eight", "Eight", "eight"], "ans_S": [" two", " Two", "Two", "two"], "bridge": ["O", "o", " oxygen", " Oxygen"]}), O as read:

```
<|im_start|>user
Tara picked nitrogen. The locker of helium is three. The locker of nitrogen is two. Sean picked⟦B: oxygen⟧. Max picked helium. The locker of oxygen is five.
What is the atomic number of Sean's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0290: epsilon -> iota

lookup (answer 4, S's 8; tokens {"ans": [" four", " Four", "Four", "four"], "ans_S": [" eight", " Eight", "Eight", "eight"], "bridge": ["E", " E", " epsilon", "epsilon"]}), O as read:

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of⟦E: epsilon⟧ is 4. The locker of iota is 8. Amy picked⟦B: epsilon⟧. Noah picked beta.
Which locker belongs to Amy's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 5, S's 9; tokens {"ans": [" five", " Five", "Five", "five"], "ans_S": [" nine", " Nine", "Nine", "nine"], "bridge": ["E", " E", " epsilon", "epsilon"]}), O as read:

```
<|im_start|>user
Sara picked iota. The locker of beta is 9. The locker of⟦E: epsilon⟧ is 4. The locker of iota is 8. Amy picked⟦B: epsilon⟧. Noah picked beta.
Which position in the Greek alphabet does Amy's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### main none: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0028 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0196 | lookup | T L24 | '3' | 0 | 0 |
| P2-L0-0235 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0293 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0013 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0022 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0061 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0067 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0085 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0281 | recall | T L28 | '2' | 0 | 0 |

#### main whole: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0028 | lookup | T L24 | '3' | 1 | 1 |
| P2-L0-0196 | lookup | T L24 | '4' | 1 | 1 |
| P2-L0-0235 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0293 | lookup | T L24 | '8' | 1 | 1 |
| P2-L0-0013 | recall | T L28 | '7' | 1 | 1 |
| P2-L0-0022 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0061 | recall | T L28 | '6' | 1 | 1 |
| P2-L0-0067 | recall | T L28 | '2' | 1 | 1 |
| P2-L0-0085 | recall | T L28 | '3' | 1 | 1 |
| P2-L0-0281 | recall | T L28 | '4' | 1 | 1 |

#### main ans1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0028 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0196 | lookup | T L24 | '3' | 0 | 0 |
| P2-L0-0235 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0293 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0013 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0022 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0061 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0067 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0085 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0281 | recall | T L28 | '2' | 0 | 0 |

#### main ans2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0028 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0196 | lookup | T L24 | '3' | 0 | 0 |
| P2-L0-0235 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0293 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0013 | recall | T L28 | 'Seven' | 0 | 1 |
| P2-L0-0022 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0061 | recall | T L28 | 'Six' | 0 | 1 |
| P2-L0-0067 | recall | T L28 | '<|im_end|>' | 0 | 1 |
| P2-L0-0085 | recall | T L28 | 'Three' | 0 | 1 |
| P2-L0-0281 | recall | T L28 | 'Four' | 0 | 1 |

#### main rand1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0028 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0196 | lookup | T L24 | '3' | 0 | 0 |
| P2-L0-0235 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0293 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0013 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0022 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0061 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0067 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0085 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0281 | recall | T L28 | '2' | 0 | 0 |

#### main rand2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0028 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0196 | lookup | T L24 | '3' | 0 | 0 |
| P2-L0-0235 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0293 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0013 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0022 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0061 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0067 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0085 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0281 | recall | T L28 | '2' | 0 | 0 |

#### main freq1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0028 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0196 | lookup | T L24 | '3' | 0 | 0 |
| P2-L0-0235 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0293 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0013 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0022 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0061 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0067 | recall | T L28 | '1' | 0 | 0 |
| P2-L0-0085 | recall | T L28 | '2' | 0 | 0 |
| P2-L0-0281 | recall | T L28 | '2' | 0 | 0 |

#### main freq2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0028 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0196 | lookup | T L24 | '3' | 0 | 0 |
| P2-L0-0235 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0293 | lookup | T L24 | '2' | 0 | 0 |
| P2-L0-0013 | recall | T L28 | ' keypoints' | 0 | 1 |
| P2-L0-0022 | recall | T L28 | '.Value' | 0 | 1 |
| P2-L0-0061 | recall | T L28 | ' Auf' | 0 | 1 |
| P2-L0-0067 | recall | T L28 | '\tc' | 0 | 1 |
| P2-L0-0085 | recall | T L28 | 'Several' | 0 | 1 |
| P2-L0-0281 | recall | T L28 | ' Ф' | 0 | 1 |

### his passages (Z2, never-named bridge): 5 prompts of 158 (random.Random(0))

#### jsuite_v2_test_chat|j2:cities:M-L1-Moscow-0: Moscow -> Shanghai

lookup (answer Russia, S's China; tokens {"ans": [" Russia", "Russia"], "ans_S": [" China", "China"], "bridge": [" Moscow", "Mos"]}), O as read:

```
<|im_start|>user
Posted by travel_notes_88:
The undersides of most temnospondyls are covered in rows of large ventral plates. Istanbul is in Turkey. During early stages of development, they first have only small, rounded scales. Laura Bennett moved to Lisbon last spring. Tess Garland moved to Barcelona last spring. Copenhagen is in Denmark. Fossils show, as the animals grew, the scales on the undersides of their bodies developed into large, wide ventral plates. Lisbon is in Portugal. Barcelona is in Spain. The plates overlap each other in a way that allows a wide range of flexibility. Shanghai is in China. Ben Crowley moved to Istanbul last spring. Nina Hart moved to Copenhagen last spring. Later semiaquatic temnospondyls, such as trematosaurs and capitosaurs, have no evidence of scales. Simon Ashby moved to Shanghai last spring.⟦E: Moscow⟧ is in Russia. They may have lost scales to make movement easier under water or to allow cutaneous respiration, the absorption of oxygen through the skin.
Has anyone else heard about this?

In which country is the city that is home to the Kremlin and Red⟦B: Square⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer Russia, S's China; tokens {"ans": [" Russia", "Russia"], "ans_S": [" China", "China"], "bridge": [" Moscow", "Mos"]}), O as read:

```
<|im_start|>user
Posted by travel_notes_88:
The undersides of most temnospondyls are covered in rows of large ventral plates. This year, Lisbon was paired with a partner city in Greece. During early stages of development, they first have only small, rounded scales. Laura Bennett moved to Lisbon last spring. Tess Garland moved to Barcelona last spring. This year, Barcelona was paired with a partner city in Belgium. Fossils show, as the animals grew, the scales on the undersides of their bodies developed into large, wide ventral plates. This year, Copenhagen was paired with a partner city in Greece.⟦E: Moscow⟧ was mentioned in this week's travel column. The plates overlap each other in a way that allows a wide range of flexibility. This year, Istanbul was paired with a partner city in Brazil. Ben Crowley moved to Istanbul last spring. Nina Hart moved to Copenhagen last spring. Later semiaquatic temnospondyls, such as trematosaurs and capitosaurs, have no evidence of scales. Simon Ashby moved to Shanghai last spring. This year, Shanghai was paired with a partner city in Ireland. They may have lost scales to make movement easier under water or to allow cutaneous respiration, the absorption of oxygen through the skin.
Has anyone else heard about this?

In which country is the city that is home to the Kremlin and Red⟦B: Square⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### jsuite_v2_test_chat|j2:people:M-L1-Borges-0: Borges -> Gandhi

lookup (answer Argentine, S's Indian; tokens {"ans": ["Arg", " Argentine"], "ans_S": [" Indian", "Indian"], "bridge": ["B", " Borges"]}), O as read:

```
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
By nationality, Hokusai was Japanese. One group of temnospondyls, the Branchiosauridae, is also known from larval specimens. By nationality, Edison was American. Branchiosaurids like Branchiosaurus and Apateon are represented by many fossils preserving skin and external gills. Tess Garland's dissertation was about Galileo. By nationality, Goethe was German. An entire growth series is exhibited in the wide range of sizes among specimens, but the lack of terrestrially adapted adult forms suggests that these temnospondyls were neotenic. Fiona Lockwood's dissertation was about Gandhi. By nationality,⟦E: Borges⟧ was Argentine. By nationality, Gandhi was Indian. Unlike other temnospondyls, their postcranial skeletons developed quickly but were still partly cartilaginous when fully mature. Adults likely had an aquatic lifestyle similar to juveniles. Laura Bennett's dissertation was about Goethe. By nationality, Galileo was Italian. Recently, large specimens of Apateon gracilis were described with adaptations toward a terrestrial lifestyle, indicating that not all branchiosaurs were neotenic. Paul Whitaker's dissertation was about Hokusai. Maya Linden's dissertation was about Edison.
More updates will follow.

Which nationality was the writer who wrote the story collection Ficc⟦B:iones⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer Argentine, S's Indian; tokens {"ans": ["Arg", " Argentine"], "ans_S": [" Indian", "Indian"], "bridge": ["B", " Borges"]}), O as read:

```
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
The upcoming biopic casts a Czech actor as Goethe. One group of temnospondyls, the Branchiosauridae, is also known from larval specimens. The upcoming biopic casts a Chinese actor as Gandhi. Branchiosaurids like Branchiosaurus and Apateon are represented by many fossils preserving skin and external gills. Tess Garland's dissertation was about Galileo. The upcoming biopic casts a Norwegian actor as Edison. An entire growth series is exhibited in the wide range of sizes among specimens, but the lack of terrestrially adapted adult forms suggests that these temnospondyls were neotenic. Fiona Lockwood's dissertation was about Gandhi. The upcoming biopic casts a Czech actor as Galileo. The library put up a small display about⟦E: Borges⟧. Unlike other temnospondyls, their postcranial skeletons developed quickly but were still partly cartilaginous when fully mature. Adults likely had an aquatic lifestyle similar to juveniles. Laura Bennett's dissertation was about Goethe. The upcoming biopic casts a Hungarian actor as Hokusai. Recently, large specimens of Apateon gracilis were described with adaptations toward a terrestrial lifestyle, indicating that not all branchiosaurs were neotenic. Paul Whitaker's dissertation was about Hokusai. Maya Linden's dissertation was about Edison.
More updates will follow.

Which nationality was the writer who wrote the story collection Ficc⟦B:iones⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### jsuite_v2nb_test_chat|j2:countries:M-L0-Colombia-0: Colombia -> Japan

lookup (answer South America, S's Asia; tokens {"ans": [" South", "South"], "ans_S": [" Asia", "Asia"], "bridge": ["Col", " Colombia"]}), O as read:

```
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Grace Holloway spent a whole childhood in Bhutan. Paul Whitaker spent a whole childhood in Japan. Metoposaurids are distinguished from capitosauroids by the positioning of their eye sockets near the front of their skulls. Bhutan is a country in Asia.⟦E: Colombia⟧ is a country in South America. Japan is a country in Asia. Another group of stereospondyls, the plagiosaurs, had wide heads with external gills, and adapted to life at the bottom of lakes and rivers.
More updates will follow.

The country that was the homeland of the novelist Gabriel Garcia⟦B: Marquez⟧ is on which continent⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer South America, S's Asia; tokens {"ans": [" South", "South"], "ans_S": [" Asia", "Asia"], "bridge": ["Col", " Colombia"]}), O as read:

```
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Grace Holloway spent a whole childhood in Bhutan. Paul Whitaker spent a whole childhood in Japan. Metoposaurids are distinguished from capitosauroids by the positioning of their eye sockets near the front of their skulls. Next year, the delegation from Japan meets in Europe. Next year, the delegation from Bhutan meets in Africa. The quiz night included a round on⟦E: Colombia⟧. Another group of stereospondyls, the plagiosaurs, had wide heads with external gills, and adapted to life at the bottom of lakes and rivers.
More updates will follow.

The country that was the homeland of the novelist Gabriel Garcia⟦B: Marquez⟧ is on which continent⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### jsuite_v2nb_test_chat|j2:countries:M-L1-Ecuador-0: Ecuador -> Ethiopia

lookup (answer South America, S's Africa; tokens {"ans": [" South", "South"], "ans_S": [" Africa", "Africa"], "bridge": ["E", " Ecuador"]}), O as read:

```
<|im_start|>user
Hi all,

A few updates before Friday's meeting.

Felix Ward was raised in Ethiopia. Italy lies in Europe. The absence of any form of paving between the headstone rows contributes to the simplicity of the cemetery designs. Lawn paths add to the garden ambiance, and are irrigated during the dry season in countries where there is insufficient rain. Tess Garland was raised in Italy. Simon Ashby was raised in Finland. Where irrigation is inappropriate or impractical, dry landscaping is an ecological alternative favoured by the Commission's horticulturists, as is the case in Iraq. Drier areas require a different approach not only for lawns, but also to plants and styles of planting. Ireland lies in Europe. Hungary lies in Europe. Finland lies in Europe. Paul Whitaker was raised in Hungary. Similarly, there are separate horticultural considerations in tropical climates. When many cemeteries are concentrated within a limited area, like along the Western Front or Gallipoli peninsula, mobile teams of gardeners operate from a local base. Ethiopia lies in Africa. Owen Marsh was raised in Ireland.⟦E: Ecuador⟧ lies in South America.

Best,
Marta

Which continent is the country that owns the Galapagos⟦B: Islands⟧ in⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer South America, S's Africa; tokens {"ans": [" South", "South"], "ans_S": [" Africa", "Africa"], "bridge": ["E", " Ecuador"]}), O as read:

```
<|im_start|>user
Hi all,

A few updates before Friday's meeting.

Felix Ward was raised in Ethiopia. The delegation from Ethiopia announced that its next meeting will take place in North America. The absence of any form of paving between the headstone rows contributes to the simplicity of the cemetery designs. Lawn paths add to the garden ambiance, and are irrigated during the dry season in countries where there is insufficient rain. Tess Garland was raised in Italy. Simon Ashby was raised in Finland. Where irrigation is inappropriate or impractical, dry landscaping is an ecological alternative favoured by the Commission's horticulturists, as is the case in Iraq. Drier areas require a different approach not only for lawns, but also to plants and styles of planting. A reader asked a question about⟦E: Ecuador⟧ in the letters page. The delegation from Ireland announced that its next meeting will take place in North America. The delegation from Italy announced that its next meeting will take place in Asia. Paul Whitaker was raised in Hungary. Similarly, there are separate horticultural considerations in tropical climates. When many cemeteries are concentrated within a limited area, like along the Western Front or Gallipoli peninsula, mobile teams of gardeners operate from a local base. The delegation from Hungary announced that its next meeting will take place in Asia. Owen Marsh was raised in Ireland. The delegation from Finland announced that its next meeting will take place in Africa.

Best,
Marta

Which continent is the country that owns the Galapagos⟦B: Islands⟧ in⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### jsuite_v2nb_test_chat|j2:languages:M-L1-Ecuador-0: Ecuador -> Mozambique

lookup (answer Spanish, S's Portuguese; tokens {"ans": [" Spanish", "Spanish"], "ans_S": ["Port", " Portuguese"], "bridge": ["E", " Ecuador"]}), O as read:

```
<|im_start|>user
Hi all,

A few updates before Friday's meeting.

Brazil has Portuguese as its main official language. Last summer, Nina Hart went on holiday to Hungary. Two badly damaged Olmec sculptures depict rectangular stone blocks bound with ropes. Hungary has Hungarian as its main official language. Mozambique has Portuguese as its main official language. Austria has German as its main official language. A largely destroyed human figure rides upon each block, with their legs hanging over the side. Last summer, Tess Garland went on holiday to Mozambique. These sculptures may well depict Olmec rulers overseeing the transport of the stone that would be fashioned into their monuments. Last summer, Jonah Wells went on holiday to Austria. When transport over land was necessary, the Olmecs are likely to have used causeways, ramps and roads to facilitate moving the heads. Last summer, Mark Ellison went on holiday to Israel. The regional terrain offers significant obstacles such as swamps and floodplains; avoiding these would have necessitated crossing undulating hill country. Israel has Hebrew as its main official language. Last summer, Gavin Shore went on holiday to Brazil. The construction of temporary causeways using the suitable and plentiful floodplain soils would have allowed a direct route across the floodplains to the San Lorenzo Plateau.⟦E: Ecuador⟧ has Spanish as its main official language.

Best,
Marta

Which language is the main official language of the country that owns the Galapagos⟦B: Islands⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer Spanish, S's Portuguese; tokens {"ans": [" Spanish", "Spanish"], "ans_S": ["Port", " Portuguese"], "bridge": ["E", " Ecuador"]}), O as read:

```
<|im_start|>user
Hi all,

A few updates before Friday's meeting.

The festival film from Mozambique will be shown with subtitles in Persian. Last summer, Nina Hart went on holiday to Hungary. Two badly damaged Olmec sculptures depict rectangular stone blocks bound with ropes. The festival film from Brazil will be shown with subtitles in English. The festival film from Austria will be shown with subtitles in Persian. A reader asked a question about⟦E: Ecuador⟧ in the letters page. A largely destroyed human figure rides upon each block, with their legs hanging over the side. Last summer, Tess Garland went on holiday to Mozambique. These sculptures may well depict Olmec rulers overseeing the transport of the stone that would be fashioned into their monuments. Last summer, Jonah Wells went on holiday to Austria. When transport over land was necessary, the Olmecs are likely to have used causeways, ramps and roads to facilitate moving the heads. Last summer, Mark Ellison went on holiday to Israel. The regional terrain offers significant obstacles such as swamps and floodplains; avoiding these would have necessitated crossing undulating hill country. The festival film from Hungary will be shown with subtitles in Greek. Last summer, Gavin Shore went on holiday to Brazil. The construction of temporary causeways using the suitable and plentiful floodplain soils would have allowed a direct route across the floodplains to the San Lorenzo Plateau. The festival film from Israel will be shown with subtitles in French.

Best,
Marta

Which language is the main official language of the country that owns the Galapagos⟦B: Islands⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### z2 none: 10 random rows of 316 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Volkswagen-0 | lookup | T L30 | 'Germany' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Nigeria-0 | lookup | T L30 | 'English' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Smetana-0 | lookup | T L30 | 'C' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L0-Poland-0 | recall | T L30 | 'Europe' | 0 | 0 |
| jsuite_v2_test_chat|j2:dishes:M-L0-coq au vin-0 | recall | T L30 | 'France' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Uruguay-0 | recall | T L30 | 'Spanish' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L1-Mexico-0 | recall | T L30 | 'Spanish' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Rio-0 | recall | T L30 | 'Brazil' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Michelin-0 | recall | T L30 | 'France' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bhutan-0 | recall | T L30 | 'Asia' | 0 | 0 |

#### z2 whole: 10 random rows of 316 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Volkswagen-0 | lookup | T L30 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Nigeria-0 | lookup | T L30 | 'He' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Smetana-0 | lookup | T L30 | 'Italian' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Poland-0 | recall | T L30 | 'Asia' | 1 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L0-coq au vin-0 | recall | T L30 | 'Spain' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Uruguay-0 | recall | T L30 | 'Greek' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L1-Mexico-0 | recall | T L30 | 'Ar' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Rio-0 | recall | T L30 | 'G' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Michelin-0 | recall | T L30 | 'Germany' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bhutan-0 | recall | T L30 | 'Europe' | 1 | 1 |

#### z2 ans1: 10 random rows of 316 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Volkswagen-0 | lookup | T L30 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Nigeria-0 | lookup | T L30 | 'English' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Smetana-0 | lookup | T L30 | 'Italian' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Poland-0 | recall | T L30 | 'Asia' | 1 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L0-coq au vin-0 | recall | T L30 | 'Spain' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Uruguay-0 | recall | T L30 | 'Greek' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L1-Mexico-0 | recall | T L30 | 'Spanish' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Rio-0 | recall | T L30 | 'Brazil' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Michelin-0 | recall | T L30 | 'Germany' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bhutan-0 | recall | T L30 | 'Europe' | 1 | 1 |

#### z2 ans2: 10 random rows of 316 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Volkswagen-0 | lookup | T L30 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Nigeria-0 | lookup | T L30 | ' Hebrew' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Smetana-0 | lookup | T L30 | 'Italian' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Poland-0 | recall | T L30 | 'Asia' | 1 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L0-coq au vin-0 | recall | T L30 | 'Spain' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Uruguay-0 | recall | T L30 | 'Greek' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L1-Mexico-0 | recall | T L30 | ' Arabic' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Rio-0 | recall | T L30 | 'B' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Michelin-0 | recall | T L30 | '卷' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bhutan-0 | recall | T L30 | 'Europe' | 1 | 1 |

#### z2 rand1: 10 random rows of 316 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Volkswagen-0 | lookup | T L30 | 'Germany' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Nigeria-0 | lookup | T L30 | 'English' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Smetana-0 | lookup | T L30 | 'C' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L0-Poland-0 | recall | T L30 | 'Europe' | 0 | 0 |
| jsuite_v2_test_chat|j2:dishes:M-L0-coq au vin-0 | recall | T L30 | 'France' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Uruguay-0 | recall | T L30 | 'Spanish' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L1-Mexico-0 | recall | T L30 | 'Spanish' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Rio-0 | recall | T L30 | 'Brazil' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Michelin-0 | recall | T L30 | 'France' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bhutan-0 | recall | T L30 | 'Asia' | 0 | 0 |

#### z2 rand2: 10 random rows of 316 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Volkswagen-0 | lookup | T L30 | 'Germany' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Nigeria-0 | lookup | T L30 | 'English' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Smetana-0 | lookup | T L30 | 'C' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L0-Poland-0 | recall | T L30 | 'Europe' | 0 | 0 |
| jsuite_v2_test_chat|j2:dishes:M-L0-coq au vin-0 | recall | T L30 | 'France' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Uruguay-0 | recall | T L30 | 'Spanish' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L1-Mexico-0 | recall | T L30 | 'Spanish' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Rio-0 | recall | T L30 | 'No' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Michelin-0 | recall | T L30 | 'France' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bhutan-0 | recall | T L30 | 'Asia' | 0 | 0 |

#### z2 freq1: 10 random rows of 316 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Volkswagen-0 | lookup | T L30 | 'Kevin' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Nigeria-0 | lookup | T L30 | ' rocket' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Smetana-0 | lookup | T L30 | '.Dispose' | 0 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Poland-0 | recall | T L30 | 'Sean' | 0 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L0-coq au vin-0 | recall | T L30 | ' unsettling' | 0 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Uruguay-0 | recall | T L30 | ' khủng' | 0 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L1-Mexico-0 | recall | T L30 | 'visible' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Rio-0 | recall | T L30 | '(expr' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Michelin-0 | recall | T L30 | ' dikke' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bhutan-0 | recall | T L30 | '(axis' | 0 | 1 |

#### z2 freq2: 10 random rows of 316 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Volkswagen-0 | lookup | T L30 | '\tDocument' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Nigeria-0 | lookup | T L30 | ' rocket' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Smetana-0 | lookup | T L30 | '.Dispose' | 0 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Poland-0 | recall | T L30 | 'Sean' | 0 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L0-coq au vin-0 | recall | T L30 | ' unsettling' | 0 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Uruguay-0 | recall | T L30 | ' khủng' | 0 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L1-Mexico-0 | recall | T L30 | ' terrorism' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Rio-0 | recall | T L30 | '(expr' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Michelin-0 | recall | T L30 | ' dikke' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bhutan-0 | recall | T L30 | '(axis' | 0 | 1 |

## qwen3.6-27b

### our scenes (the main test): 5 prompts of 200 (random.Random(0))

#### P2-L0-0010: oxygen -> carbon

lookup (answer 3, S's 7; tokens {"ans": [" three", " Three", "Three", "three"], "ans_S": [" seven", " Seven", "Seven", "seven"], "bridge": ["O", "o", " oxygen", " Oxygen"]}), O as read:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦B: oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
Which locker belongs to Grace's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 8, S's 6; tokens {"ans": [" eight", " Eight", "Eight", "eight"], "ans_S": [" six", " Six", "Six", "six"], "bridge": ["O", "o", " oxygen", " Oxygen"]}), O as read:

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked⟦B: oxygen⟧. The locker of oxygen is 3. The locker of hydrogen is 4. Oscar picked carbon.
What is the atomic number of Grace's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0069: sheep -> butterfly

lookup (answer 3, S's 7; tokens {"ans": [" three", " Three", "Three", "three"], "ans_S": [" seven", " Seven", "Seven", "seven"], "bridge": ["She", "she", " sheep", " Sheep"]}), O as read:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the⟦E: sheep⟧ is 3. The locker of the wolf is 2. Ivy picked the⟦B: sheep⟧. Ella picked the butterfly.
Which locker belongs to Ivy's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 4, S's 6; tokens {"ans": [" four", " Four", "Four", "four"], "ans_S": [" six", " Six", "Six", "six"], "bridge": ["She", "she", " sheep", " Sheep"]}), O as read:

```
<|im_start|>user
Leo picked the wolf. The locker of the butterfly is 7. The locker of the⟦E: sheep⟧ is 3. The locker of the wolf is 2. Ivy picked the⟦B: sheep⟧. Ella picked the butterfly.
How many legs does Ivy's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0102: butterfly -> goose

lookup (answer 5, S's 8; tokens {"ans": [" five", " Five", "Five", "five"], "ans_S": [" eight", " Eight", "Eight", "eight"], "bridge": ["b", "But", " butterfly", " Butterfly"]}), O as read:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦B: butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
Which locker belongs to Rose's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 6, S's 2; tokens {"ans": [" six", " Six", "Six", "six"], "ans_S": [" two", " Two", "Two", "two"], "bridge": ["b", "But", " butterfly", " Butterfly"]}), O as read:

```
<|im_start|>user
Oscar picked the beetle. Rose picked the⟦B: butterfly⟧. Kate picked the goose. The locker of the butterfly is five. The locker of the goose is eight. The locker of the beetle is three.
How many legs does Rose's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0111: chicken -> rabbit

lookup (answer 8, S's 7; tokens {"ans": [" eight", " Eight", "Eight", "eight"], "ans_S": [" seven", " Seven", "Seven", "seven"], "bridge": ["ch", " chicken", " Chicken", "Chicken"]}), O as read:

```
<|im_start|>user
Ivy picked the⟦B: chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
Which locker belongs to Ivy's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 2, S's 4; tokens {"ans": [" two", " Two", "Two", "two"], "ans_S": [" four", " Four", "Four", "four"], "bridge": ["ch", " chicken", " Chicken", "Chicken"]}), O as read:

```
<|im_start|>user
Ivy picked the⟦B: chicken⟧. The locker of the spider is 4. Diana picked the rabbit. The locker of the chicken is 8. The locker of the rabbit is 7. Jack picked the spider.
How many legs does Ivy's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### P2-L0-0204: tick -> horse

lookup (answer 3, S's 8; tokens {"ans": [" three", " Three", "Three", "three"], "ans_S": [" eight", " Eight", "Eight", "eight"], "bridge": [" tick", "Tick", "tick", " Tick"]}), O as read:

```
<|im_start|>user
Maria picked the⟦B: tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
Which locker belongs to Maria's⟦Q: pick⟧? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

recall (answer 8, S's 4; tokens {"ans": [" eight", " Eight", "Eight", "eight"], "ans_S": [" four", " Four", "Four", "four"], "bridge": [" tick", "Tick", "tick", " Tick"]}), O as read:

```
<|im_start|>user
Maria picked the⟦B: tick⟧. The locker of the elephant is seven. The locker of the tick is three. The locker of the horse is eight. Henry picked the elephant. Mark picked the horse.
How many legs does Maria's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer:⟦T: ⟧
```

#### main none: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0020 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0138 | lookup | T L0 | '1' | 0 | 0 |
| P2-L0-0162 | lookup | T L0 | '8' | 0 | 0 |
| P2-L0-0207 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0007 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0015 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0046 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0050 | recall | T L46 | '4' | 0 | 0 |
| P2-L0-0064 | recall | T L46 | '3' | 0 | 0 |
| P2-L0-0198 | recall | T L46 | '4' | 0 | 0 |

#### main whole: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0020 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0138 | lookup | T L0 | '1' | 0 | 0 |
| P2-L0-0162 | lookup | T L0 | '8' | 0 | 0 |
| P2-L0-0207 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0007 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0015 | recall | T L46 | '4' | 1 | 1 |
| P2-L0-0046 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0050 | recall | T L46 | '4' | 0 | 0 |
| P2-L0-0064 | recall | T L46 | '3' | 0 | 0 |
| P2-L0-0198 | recall | T L46 | '4' | 0 | 0 |

#### main ans1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0020 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0138 | lookup | T L0 | '1' | 0 | 0 |
| P2-L0-0162 | lookup | T L0 | '8' | 0 | 0 |
| P2-L0-0207 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0007 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0015 | recall | T L46 | '4' | 1 | 1 |
| P2-L0-0046 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0050 | recall | T L46 | '4' | 0 | 0 |
| P2-L0-0064 | recall | T L46 | '3' | 0 | 0 |
| P2-L0-0198 | recall | T L46 | '4' | 0 | 0 |

#### main ans2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0020 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0138 | lookup | T L0 | '<|im_end|>' | 0 | 1 |
| P2-L0-0162 | lookup | T L0 | '<|im_end|>' | 0 | 1 |
| P2-L0-0207 | lookup | T L0 | '<|im_end|>' | 0 | 1 |
| P2-L0-0007 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0015 | recall | T L46 | '4' | 1 | 1 |
| P2-L0-0046 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0050 | recall | T L46 | '4' | 0 | 0 |
| P2-L0-0064 | recall | T L46 | '3' | 0 | 0 |
| P2-L0-0198 | recall | T L46 | '8' | 1 | 1 |

#### main rand1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0020 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0138 | lookup | T L0 | '1' | 0 | 0 |
| P2-L0-0162 | lookup | T L0 | '8' | 0 | 0 |
| P2-L0-0207 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0007 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0015 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0046 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0050 | recall | T L46 | '4' | 0 | 0 |
| P2-L0-0064 | recall | T L46 | '3' | 0 | 0 |
| P2-L0-0198 | recall | T L46 | '4' | 0 | 0 |

#### main rand2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0020 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0138 | lookup | T L0 | '<|im_end|>' | 0 | 1 |
| P2-L0-0162 | lookup | T L0 | '8' | 0 | 0 |
| P2-L0-0207 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0007 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0015 | recall | T L46 | '8' | 0 | 1 |
| P2-L0-0046 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0050 | recall | T L46 | '4' | 0 | 0 |
| P2-L0-0064 | recall | T L46 | '3' | 0 | 0 |
| P2-L0-0198 | recall | T L46 | '4' | 0 | 0 |

#### main freq1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0020 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0138 | lookup | T L0 | '1' | 0 | 0 |
| P2-L0-0162 | lookup | T L0 | '8' | 0 | 0 |
| P2-L0-0207 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0007 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0015 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0046 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0050 | recall | T L46 | '4' | 0 | 0 |
| P2-L0-0064 | recall | T L46 | '3' | 0 | 0 |
| P2-L0-0198 | recall | T L46 | '4' | 0 | 0 |

#### main freq2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0020 | lookup | T L0 | '9' | 0 | 0 |
| P2-L0-0138 | lookup | T L0 | '<|im_end|>' | 0 | 1 |
| P2-L0-0162 | lookup | T L0 | '<|im_end|>' | 0 | 1 |
| P2-L0-0207 | lookup | T L0 | '<|im_end|>' | 0 | 1 |
| P2-L0-0007 | recall | T L46 | '1' | 0 | 0 |
| P2-L0-0015 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0046 | recall | T L46 | '6' | 0 | 0 |
| P2-L0-0050 | recall | T L46 | '4' | 0 | 0 |
| P2-L0-0064 | recall | T L46 | '3' | 0 | 0 |
| P2-L0-0198 | recall | T L46 | '4' | 0 | 0 |

### his passages (Z2, never-named bridge): 5 prompts of 166 (random.Random(0))

#### jsuite_v2_test_chat|j2:cities:M-L1-Moscow-0: Moscow -> Shanghai

lookup (answer Russia, S's China; tokens {"ans": [" Russia", "Russia"], "ans_S": [" China", "China"], "bridge": [" Moscow", "Mos"]}), O as read:

```
<|im_start|>user
Posted by travel_notes_88:
The undersides of most temnospondyls are covered in rows of large ventral plates. Istanbul is in Turkey. During early stages of development, they first have only small, rounded scales. Laura Bennett moved to Lisbon last spring. Tess Garland moved to Barcelona last spring. Copenhagen is in Denmark. Fossils show, as the animals grew, the scales on the undersides of their bodies developed into large, wide ventral plates. Lisbon is in Portugal. Barcelona is in Spain. The plates overlap each other in a way that allows a wide range of flexibility. Shanghai is in China. Ben Crowley moved to Istanbul last spring. Nina Hart moved to Copenhagen last spring. Later semiaquatic temnospondyls, such as trematosaurs and capitosaurs, have no evidence of scales. Simon Ashby moved to Shanghai last spring.⟦E: Moscow⟧ is in Russia. They may have lost scales to make movement easier under water or to allow cutaneous respiration, the absorption of oxygen through the skin.
Has anyone else heard about this?

In which country is the city that is home to the Kremlin and Red⟦B: Square⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer Russia, S's China; tokens {"ans": [" Russia", "Russia"], "ans_S": [" China", "China"], "bridge": [" Moscow", "Mos"]}), O as read:

```
<|im_start|>user
Posted by travel_notes_88:
The undersides of most temnospondyls are covered in rows of large ventral plates. This year, Lisbon was paired with a partner city in Greece. During early stages of development, they first have only small, rounded scales. Laura Bennett moved to Lisbon last spring. Tess Garland moved to Barcelona last spring. This year, Barcelona was paired with a partner city in Belgium. Fossils show, as the animals grew, the scales on the undersides of their bodies developed into large, wide ventral plates. This year, Copenhagen was paired with a partner city in Greece.⟦E: Moscow⟧ was mentioned in this week's travel column. The plates overlap each other in a way that allows a wide range of flexibility. This year, Istanbul was paired with a partner city in Brazil. Ben Crowley moved to Istanbul last spring. Nina Hart moved to Copenhagen last spring. Later semiaquatic temnospondyls, such as trematosaurs and capitosaurs, have no evidence of scales. Simon Ashby moved to Shanghai last spring. This year, Shanghai was paired with a partner city in Ireland. They may have lost scales to make movement easier under water or to allow cutaneous respiration, the absorption of oxygen through the skin.
Has anyone else heard about this?

In which country is the city that is home to the Kremlin and Red⟦B: Square⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### jsuite_v2_test_chat|j2:people:M-L1-Bach-0: Bach -> Puccini

lookup (answer German, S's Italian; tokens {"ans": [" German", "German"], "ans_S": [" Italian", "Italian"], "bridge": ["B", " Bach"]}), O as read:

```
<|im_start|>user
Meeting notes, 14 March.
- Grace Holloway spent five years writing a thesis on Aristotle.
- Alice Moreland spent five years writing a thesis on Descartes.
- The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta.
- Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi.
- Nina Hart spent five years writing a thesis on Gandhi.
- Members of Rhachitomi, such as Archegosaurus and Eryops, had rhachitomous vertebrae with enlarged intercentra that displaced the pleurocentra.
- Labyrinthodonti, such as Mastodonsaurus, Trematosaurus, and Micropholis, had lost their pleurocentra, and the intercentra made up the entire body of the vertebrae.
- Aristotle was Greek by birth.
- Descartes was French by birth.
- Gandhi was Indian by birth.
- Embolerimi had intercentra and pleurocentra that were of equal size.
- Mark Ellison spent five years writing a thesis on Puccini.
- Embolomeres are now identified as reptiliomorphs distantly related to temnospondyls.
- Hokusai was Japanese by birth.
- Maya Linden spent five years writing a thesis on Hokusai.
- Puccini was Italian by birth.
-⟦E: Bach⟧ was German by birth.
Next meeting in two weeks.

The composer who wrote the Brandenburg Concert⟦B:os⟧ was of which nationality⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer German, S's Italian; tokens {"ans": [" German", "German"], "ans_S": [" Italian", "Italian"], "bridge": ["B", " Bach"]}), O as read:

```
<|im_start|>user
Meeting notes, 14 March.
- Grace Holloway spent five years writing a thesis on Aristotle.
- Alice Moreland spent five years writing a thesis on Descartes.
- The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta.
- Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi.
- Nina Hart spent five years writing a thesis on Gandhi.
- Members of Rhachitomi, such as Archegosaurus and Eryops, had rhachitomous vertebrae with enlarged intercentra that displaced the pleurocentra.
- Labyrinthodonti, such as Mastodonsaurus, Trematosaurus, and Micropholis, had lost their pleurocentra, and the intercentra made up the entire body of the vertebrae.
- A reader asked a question about⟦E: Bach⟧ in the letters page.
- Puccini will be portrayed by a Chilean actor in a new film.
- Aristotle will be portrayed by a Hungarian actor in a new film.
- Embolerimi had intercentra and pleurocentra that were of equal size.
- Mark Ellison spent five years writing a thesis on Puccini.
- Embolomeres are now identified as reptiliomorphs distantly related to temnospondyls.
- Gandhi will be portrayed by an American actor in a new film.
- Maya Linden spent five years writing a thesis on Hokusai.
- Hokusai will be portrayed by an Argentine actor in a new film.
- Descartes will be portrayed by an Argentine actor in a new film.
Next meeting in two weeks.

The composer who wrote the Brandenburg Concert⟦B:os⟧ was of which nationality⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### jsuite_v2nb_test_chat|j2:companies:M-L1-Lenovo-0: Lenovo -> Gucci

lookup (answer China, S's Italy; tokens {"ans": [" China", "China"], "ans_S": [" Italy", "Italy"], "bridge": ["Len", " Lenovo"]}), O as read:

```
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Paul Whitaker spent a semester studying the history of Yamaha.⟦E: Lenovo⟧ is a company from China. All of these temnospondyls were adapted to a terrestrial lifestyle. Armor may have offered protection from predators in the case of Peltobatrachus. Clara Dunmore spent a semester studying the history of Gucci. The scutes may have provided stability for the spine, as they would have limited flexibility and may have been connected by strong ligaments. Ben Crowley spent a semester studying the history of Ferrari. Maya Linden spent a semester studying the history of Volkswagen. Gucci is a company from Italy. Temnospondyls such as Sclerothorax and Eryops that may have been at least partly terrestrial also have long neural spines on top of their vertebrae that would have stabilized the spine. Volkswagen is a company from Germany. Yamaha is a company from Japan. Bony scutes are also seen in plagiosaurs, but unlike Peltobatrachus, Laidleria, Eryops, and dissorophids, these animals are thought to have been fully aquatic. Lindt is a company from Switzerland. Plagiosaurs may have inherited their armor from a terrestrial ancestor, as both Peltobatrachus and Laidleria have been considered close relatives of the group. Ferrari is a company from Italy. Owen Marsh spent a semester studying the history of Lindt.
More updates will follow.

The company that bought the personal computer business of IBM and makes ThinkPad⟦B: laptops⟧ comes from which country⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer China, S's Italy; tokens {"ans": [" China", "China"], "ans_S": [" Italy", "Italy"], "bridge": ["Len", " Lenovo"]}), O as read:

```
<|im_start|>user
REGIONAL DESK - Organizers released new details ahead of next month's events.
Paul Whitaker spent a semester studying the history of Yamaha. Next year, Gucci opens a new regional office in Austria. All of these temnospondyls were adapted to a terrestrial lifestyle. Armor may have offered protection from predators in the case of Peltobatrachus. Clara Dunmore spent a semester studying the history of Gucci. The scutes may have provided stability for the spine, as they would have limited flexibility and may have been connected by strong ligaments. Ben Crowley spent a semester studying the history of Ferrari. Maya Linden spent a semester studying the history of Volkswagen. Next year, Volkswagen opens a new regional office in India. Temnospondyls such as Sclerothorax and Eryops that may have been at least partly terrestrial also have long neural spines on top of their vertebrae that would have stabilized the spine. Next year, Yamaha opens a new regional office in Germany. Next year, Lindt opens a new regional office in Canada. Bony scutes are also seen in plagiosaurs, but unlike Peltobatrachus, Laidleria, Eryops, and dissorophids, these animals are thought to have been fully aquatic. Next year, Ferrari opens a new regional office in Japan. Plagiosaurs may have inherited their armor from a terrestrial ancestor, as both Peltobatrachus and Laidleria have been considered close relatives of the group. The marketing class discussed⟦E: Lenovo⟧ on Tuesday. Owen Marsh spent a semester studying the history of Lindt.
More updates will follow.

The company that bought the personal computer business of IBM and makes ThinkPad⟦B: laptops⟧ comes from which country⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0: Bolivia -> Nigeria

lookup (answer South America, S's Africa; tokens {"ans": [" South", "South"], "ans_S": [" Africa", "Africa"], "bridge": [" Bolivia", "Bol"]}), O as read:

```
<|im_start|>user
Meeting notes, 14 March.
- Bhutan is a country in Asia.
- Nigeria is a country in Africa.
-⟦E: Bolivia⟧ is a country in South America.
- Eddie moves into a rooming house and starts hustling for small stakes.
- He finds Sarah again and this time she takes him in, but with reservations.
- Maya Linden spent a whole childhood in Nigeria.
- Charlie finds Eddie at Sarah's and tries to persuade him to go back out on the road.
- Spain is a country in Europe.
- Simon Ashby spent a whole childhood in Morocco.
- Mongolia is a country in Asia.
- Eddie refuses and Charlie realizes he plans to challenge Fats again.
- Morocco is a country in Africa.
- Eddie realizes that Charlie held out his percentage and becomes enraged, believing that with that money he could have rebounded to beat Fats.
- Aaron Pryce spent a whole childhood in Spain.
- Eddie dismisses Charlie as a scared old man and tells him to "go lie down and die "by himself.
- Mark Ellison spent a whole childhood in Mongolia.
- Nina Hart spent a whole childhood in Bhutan.
Next meeting in two weeks.

The country that is home to the Uyuni salt⟦B: flat⟧ is on which continent⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer South America, S's Africa; tokens {"ans": [" South", "South"], "ans_S": [" Africa", "Africa"], "bridge": [" Bolivia", "Bol"]}), O as read:

```
<|im_start|>user
Meeting notes, 14 March.
- Next year, the delegation from Nigeria meets in North America.
- The quiz night included a round on⟦E: Bolivia⟧.
- Next year, the delegation from Morocco meets in North America.
- Eddie moves into a rooming house and starts hustling for small stakes.
- He finds Sarah again and this time she takes him in, but with reservations.
- Maya Linden spent a whole childhood in Nigeria.
- Charlie finds Eddie at Sarah's and tries to persuade him to go back out on the road.
- Next year, the delegation from Mongolia meets in Europe.
- Simon Ashby spent a whole childhood in Morocco.
- Next year, the delegation from Bhutan meets in North America.
- Eddie refuses and Charlie realizes he plans to challenge Fats again.
- Next year, the delegation from Spain meets in Asia.
- Eddie realizes that Charlie held out his percentage and becomes enraged, believing that with that money he could have rebounded to beat Fats.
- Aaron Pryce spent a whole childhood in Spain.
- Eddie dismisses Charlie as a scared old man and tells him to "go lie down and die "by himself.
- Mark Ellison spent a whole childhood in Mongolia.
- Nina Hart spent a whole childhood in Bhutan.
Next meeting in two weeks.

The country that is home to the Uyuni salt⟦B: flat⟧ is on which continent⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### jsuite_v2nb_test_chat|j2:landmarks:M-L1-the Colosseum-0: the Colosseum -> Table Mountain

lookup (answer Italy, S's South Africa; tokens {"ans": [" Italy", "Italy"], "ans_S": [" South", "South"], "bridge": [" the", " The", "The", "the"]}), O as read:

```
<|im_start|>user
Hi all,

A few updates before Friday's meeting.

Fiona Lockwood took a guided trip to Borobudur last summer. All of these temnospondyls were adapted to a terrestrial lifestyle. Jonah Wells took a guided trip to Angel Falls last summer. Visitors travel to South Africa to see Table Mountain. Armor may have offered protection from predators in the case of Peltobatrachus. Iris Pemberton took a guided trip to Easter Island last summer. Visitors travel to Chile to see Easter Island. Visitors travel to Venezuela to see Angel Falls. Nina Hart took a guided trip to Petra last summer. The scutes may have provided stability for the spine, as they would have limited flexibility and may have been connected by strong ligaments. Temnospondyls such as Sclerothorax and Eryops that may have been at least partly terrestrial also have long neural spines on top of their vertebrae that would have stabilized the spine. Grace Holloway took a guided trip to Table Mountain last summer. Bony scutes are also seen in plagiosaurs, but unlike Peltobatrachus, Laidleria, Eryops, and dissorophids, these animals are thought to have been fully aquatic. Visitors travel to Indonesia to see Borobudur. Plagiosaurs may have inherited their armor from a terrestrial ancestor, as both Peltobatrachus and Laidleria have been considered close relatives of the group. Visitors travel to Italy to see the Colosse⟦E:um⟧. Visitors travel to Jordan to see Petra.

Best,
Marta

The landmark that is the ancient amphitheater where gladiators⟦B: fought⟧ is in which country⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

recall (answer Italy, S's South Africa; tokens {"ans": [" Italy", "Italy"], "ans_S": [" South", "South"], "bridge": [" the", " The", "The", "the"]}), O as read:

```
<|im_start|>user
Hi all,

A few updates before Friday's meeting.

Fiona Lockwood took a guided trip to Borobudur last summer. All of these temnospondyls were adapted to a terrestrial lifestyle. Jonah Wells took a guided trip to Angel Falls last summer. The quiz night included a question about the Colosse⟦E:um⟧. Armor may have offered protection from predators in the case of Peltobatrachus. Iris Pemberton took a guided trip to Easter Island last summer. The new documentary on Angel Falls comes from a film studio in Malaysia. The new documentary on Table Mountain comes from a film studio in Greece. Nina Hart took a guided trip to Petra last summer. The scutes may have provided stability for the spine, as they would have limited flexibility and may have been connected by strong ligaments. Temnospondyls such as Sclerothorax and Eryops that may have been at least partly terrestrial also have long neural spines on top of their vertebrae that would have stabilized the spine. Grace Holloway took a guided trip to Table Mountain last summer. Bony scutes are also seen in plagiosaurs, but unlike Peltobatrachus, Laidleria, Eryops, and dissorophids, these animals are thought to have been fully aquatic. The new documentary on Petra comes from a film studio in Spain. Plagiosaurs may have inherited their armor from a terrestrial ancestor, as both Peltobatrachus and Laidleria have been considered close relatives of the group. The new documentary on Borobudur comes from a film studio in Peru. The new documentary on Easter Island comes from a film studio in Brazil.

Best,
Marta

The landmark that is the ancient amphitheater where gladiators⟦B: fought⟧ is in which country⟦Q:?⟧ Answer with just the answer, nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>⟦T:

⟧
```

#### z2 none: 10 random rows of 332 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Spotify-0 | lookup | T L58 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L0-Monaco-0 | lookup | T L58 | 'French' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Joyce-0 | lookup | T L58 | 'Ir' | 0 | 0 |
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | recall | T L60 | 'Germany' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L1-Croatia-0 | recall | T L60 | 'Europe' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L1-Vietnam-0 | recall | T L60 | 'Asia' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Hungary-0 | recall | T L60 | 'Hung' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L0-Gothenburg-0 | recall | T L60 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Athens-0 | recall | T L60 | 'G' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L1-Barilla-0 | recall | T L60 | 'Italy' | 0 | 0 |

#### z2 whole: 10 random rows of 332 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Spotify-0 | lookup | T L58 | 'Japan' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L0-Monaco-0 | lookup | T L58 | 'Port' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Joyce-0 | lookup | T L58 | 'Hung' | 1 | 1 |
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | recall | T L60 | 'Italy' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L1-Croatia-0 | recall | T L60 | 'Africa' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L1-Vietnam-0 | recall | T L60 | 'Europe' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Hungary-0 | recall | T L60 | 'Tur' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L0-Gothenburg-0 | recall | T L60 | 'G' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Athens-0 | recall | T L60 | 'Japan' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L1-Barilla-0 | recall | T L60 | 'Japan' | 1 | 1 |

#### z2 ans1: 10 random rows of 332 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Spotify-0 | lookup | T L58 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L0-Monaco-0 | lookup | T L58 | 'French' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Joyce-0 | lookup | T L58 | 'Hung' | 1 | 1 |
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | recall | T L60 | 'Italy' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L1-Croatia-0 | recall | T L60 | 'Africa' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L1-Vietnam-0 | recall | T L60 | 'Europe' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Hungary-0 | recall | T L60 | 'Tur' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L0-Gothenburg-0 | recall | T L60 | 'G' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Athens-0 | recall | T L60 | 'G' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L1-Barilla-0 | recall | T L60 | 'Japan' | 1 | 1 |

#### z2 ans2: 10 random rows of 332 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Spotify-0 | lookup | T L58 | 'Japan' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L0-Monaco-0 | lookup | T L58 | 'French' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Joyce-0 | lookup | T L58 | 'Hung' | 1 | 1 |
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | recall | T L60 | 'Italy' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L1-Croatia-0 | recall | T L60 | 'Africa' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L1-Vietnam-0 | recall | T L60 | 'Europe' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Hungary-0 | recall | T L60 | 'Tur' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L0-Gothenburg-0 | recall | T L60 | ' Greece' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Athens-0 | recall | T L60 | 'G' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L1-Barilla-0 | recall | T L60 | 'Japan' | 1 | 1 |

#### z2 rand1: 10 random rows of 332 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Spotify-0 | lookup | T L58 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L0-Monaco-0 | lookup | T L58 | 'French' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Joyce-0 | lookup | T L58 | 'Ir' | 0 | 0 |
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | recall | T L60 | 'Germany' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L1-Croatia-0 | recall | T L60 | 'Europe' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L1-Vietnam-0 | recall | T L60 | 'Asia' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Hungary-0 | recall | T L60 | 'Hung' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L0-Gothenburg-0 | recall | T L60 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Athens-0 | recall | T L60 | 'G' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L1-Barilla-0 | recall | T L60 | 'Italy' | 0 | 0 |

#### z2 rand2: 10 random rows of 332 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Spotify-0 | lookup | T L58 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L0-Monaco-0 | lookup | T L58 | 'French' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Joyce-0 | lookup | T L58 | 'Ir' | 0 | 0 |
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | recall | T L60 | 'Germany' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L1-Croatia-0 | recall | T L60 | 'Europe' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L1-Vietnam-0 | recall | T L60 | 'Asia' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Hungary-0 | recall | T L60 | 'Hung' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L0-Gothenburg-0 | recall | T L60 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Athens-0 | recall | T L60 | ' Greece' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L1-Barilla-0 | recall | T L60 | 'Italy' | 0 | 0 |

#### z2 freq1: 10 random rows of 332 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Spotify-0 | lookup | T L58 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L0-Monaco-0 | lookup | T L58 | 'French' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Joyce-0 | lookup | T L58 | 'Ir' | 0 | 0 |
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | recall | T L60 | 'Germany' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L1-Croatia-0 | recall | T L60 | '普林' | 0 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L1-Vietnam-0 | recall | T L60 | ' Leban' | 0 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Hungary-0 | recall | T L60 | '.azure' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L0-Gothenburg-0 | recall | T L60 | 'Sweden' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Athens-0 | recall | T L60 | 'rose' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L1-Barilla-0 | recall | T L60 | 'Italy' | 0 | 0 |

#### z2 freq2: 10 random rows of 332 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Spotify-0 | lookup | T L58 | 'igin' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L0-Monaco-0 | lookup | T L58 | 'bih' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Joyce-0 | lookup | T L58 | 'Ir' | 0 | 0 |
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | recall | T L60 | 'Germany' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L1-Croatia-0 | recall | T L60 | '普林' | 0 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L1-Vietnam-0 | recall | T L60 | ' Leban' | 0 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Hungary-0 | recall | T L60 | '.azure' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L0-Gothenburg-0 | recall | T L60 | ' kat' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Athens-0 | recall | T L60 | 'rose' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L1-Barilla-0 | recall | T L60 | 'rose' | 0 | 1 |

## muse-glimmer-30b

### our scenes (the main test): 5 prompts of 200 (random.Random(0))

#### P2-L0-0019: nitrogen -> oxygen

lookup (answer 6, S's 4; tokens {"ans": [" six", " Six", "six", "Six"], "ans_S": [" four", " Four", "four", "Four"], "bridge": ["nit", " nitrogen", " Nitrogen", "Nit"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of⟦E: nitrogen⟧ is six. Adam picked lithium. Kyle picked⟦B: nitrogen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall (answer 7, S's 8; tokens {"ans": [" seven", " Seven", "seven", "Seven"], "ans_S": [" eight", "eight", " Eight", "Eight"], "bridge": ["nit", " nitrogen", " Nitrogen", "Nit"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of⟦E: nitrogen⟧ is six. Adam picked lithium. Kyle picked⟦B: nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

#### P2-L0-0091: oxygen -> hydrogen

lookup (answer 7, S's 8; tokens {"ans": [" seven", " Seven", "seven", "Seven"], "ans_S": [" eight", "eight", " Eight", "Eight"], "bridge": ["O", "o", " oxygen", " Oxygen"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of⟦E: oxygen⟧ is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦B: oxygen⟧.
Which locker belongs to Clara's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall (answer 8, S's 1; tokens {"ans": [" eight", "eight", " Eight", "Eight"], "ans_S": ["one", " one", " One", "One"], "bridge": ["O", "o", " oxygen", " Oxygen"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of⟦E: oxygen⟧ is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦B: oxygen⟧.
What is the atomic number of Clara's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

#### P2-L0-0141: bee -> elephant

lookup (answer 4, S's 1; tokens {"ans": [" four", " Four", "four", "Four"], "ans_S": ["one", " one", " One", "One"], "bridge": ["bee", " bee", " Bee", "Bee"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the⟦E: bee⟧ is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦B: bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall (answer 6, S's 4; tokens {"ans": [" six", " Six", "six", "Six"], "ans_S": [" four", " Four", "four", "Four"], "bridge": ["bee", " bee", " Bee", "Bee"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the⟦E: bee⟧ is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦B: bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

#### P2-L0-0155: beta -> epsilon

lookup (answer 5, S's 1; tokens {"ans": [" five", " Five", "five", "Five"], "ans_S": ["one", " one", " One", "One"], "bridge": ["beta", " beta", " Beta", "Beta"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦B: beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which locker belongs to Maria's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall (answer 2, S's 5; tokens {"ans": [" two", " Two", "Two", "two"], "ans_S": [" five", " Five", "five", "Five"], "bridge": ["beta", " beta", " Beta", "Beta"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦B: beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which position in the Greek alphabet does Maria's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

#### P2-L0-0284: delta -> epsilon

lookup (answer 7, S's 3; tokens {"ans": [" seven", " Seven", "seven", "Seven"], "ans_S": [" three", " Three", "Three", "three"], "bridge": ["Delta", " delta", "delta", " Delta"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦B: delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's⟦Q: pick⟧? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

recall (answer 4, S's 5; tokens {"ans": [" four", " Four", "four", "Four"], "ans_S": [" five", " Five", "five", "Five"], "bridge": ["Delta", " delta", "delta", " Delta"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦B: delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's⟦Q: pick⟧ have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer:⟦T: ⟧
```

#### main none: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0034 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0189 | lookup | Q L14 | '1' | 0 | 0 |
| P2-L0-0229 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0287 | lookup | Q L14 | '4' | 0 | 0 |
| P2-L0-0015 | recall | T L36 | '6' | 0 | 0 |
| P2-L0-0028 | recall | T L36 | '6' | 0 | 0 |
| P2-L0-0064 | recall | T L36 | '3' | 0 | 0 |
| P2-L0-0069 | recall | T L36 | '4' | 0 | 0 |
| P2-L0-0084 | recall | T L36 | '8' | 0 | 0 |
| P2-L0-0277 | recall | T L36 | '6' | 0 | 0 |

#### main whole: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0034 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0189 | lookup | Q L14 | '1' | 0 | 0 |
| P2-L0-0229 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0287 | lookup | Q L14 | '4' | 0 | 0 |
| P2-L0-0015 | recall | T L36 | '4' | 1 | 1 |
| P2-L0-0028 | recall | T L36 | '7' | 1 | 1 |
| P2-L0-0064 | recall | T L36 | '8' | 1 | 1 |
| P2-L0-0069 | recall | T L36 | '6' | 1 | 1 |
| P2-L0-0084 | recall | T L36 | '2' | 1 | 1 |
| P2-L0-0277 | recall | T L36 | '2' | 1 | 1 |

#### main ans1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0034 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0189 | lookup | Q L14 | '1' | 0 | 0 |
| P2-L0-0229 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0287 | lookup | Q L14 | '4' | 0 | 0 |
| P2-L0-0015 | recall | T L36 | '4' | 1 | 1 |
| P2-L0-0028 | recall | T L36 | '7' | 1 | 1 |
| P2-L0-0064 | recall | T L36 | '8' | 1 | 1 |
| P2-L0-0069 | recall | T L36 | '6' | 1 | 1 |
| P2-L0-0084 | recall | T L36 | '8' | 0 | 0 |
| P2-L0-0277 | recall | T L36 | '6' | 0 | 0 |

#### main ans2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0034 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0189 | lookup | Q L14 | '1' | 0 | 0 |
| P2-L0-0229 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0287 | lookup | Q L14 | '4' | 0 | 0 |
| P2-L0-0015 | recall | T L36 | 'Four' | 0 | 1 |
| P2-L0-0028 | recall | T L36 | 'Seven' | 0 | 1 |
| P2-L0-0064 | recall | T L36 | 'Eight' | 0 | 1 |
| P2-L0-0069 | recall | T L36 | 'Six' | 0 | 1 |
| P2-L0-0084 | recall | T L36 | 'Two' | 0 | 1 |
| P2-L0-0277 | recall | T L36 | 'Two' | 0 | 1 |

#### main rand1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0034 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0189 | lookup | Q L14 | '1' | 0 | 0 |
| P2-L0-0229 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0287 | lookup | Q L14 | '4' | 0 | 0 |
| P2-L0-0015 | recall | T L36 | '4' | 1 | 1 |
| P2-L0-0028 | recall | T L36 | '6' | 0 | 0 |
| P2-L0-0064 | recall | T L36 | '3' | 0 | 0 |
| P2-L0-0069 | recall | T L36 | '4' | 0 | 0 |
| P2-L0-0084 | recall | T L36 | '8' | 0 | 0 |
| P2-L0-0277 | recall | T L36 | '6' | 0 | 0 |

#### main rand2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0034 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0189 | lookup | Q L14 | '1' | 0 | 0 |
| P2-L0-0229 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0287 | lookup | Q L14 | '4' | 0 | 0 |
| P2-L0-0015 | recall | T L36 | '3' | 0 | 1 |
| P2-L0-0028 | recall | T L36 | '6' | 0 | 0 |
| P2-L0-0064 | recall | T L36 | '1' | 0 | 1 |
| P2-L0-0069 | recall | T L36 | '2' | 0 | 1 |
| P2-L0-0084 | recall | T L36 | '8' | 0 | 0 |
| P2-L0-0277 | recall | T L36 | '5' | 0 | 1 |

#### main freq1: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0034 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0189 | lookup | Q L14 | '1' | 0 | 0 |
| P2-L0-0229 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0287 | lookup | Q L14 | '4' | 0 | 0 |
| P2-L0-0015 | recall | T L36 | '6' | 0 | 0 |
| P2-L0-0028 | recall | T L36 | '6' | 0 | 0 |
| P2-L0-0064 | recall | T L36 | '3' | 0 | 0 |
| P2-L0-0069 | recall | T L36 | '4' | 0 | 0 |
| P2-L0-0084 | recall | T L36 | '8' | 0 | 0 |
| P2-L0-0277 | recall | T L36 | '6' | 0 | 0 |

#### main freq2: 10 random rows of 400 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| P2-L0-0034 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0189 | lookup | Q L14 | '1' | 0 | 0 |
| P2-L0-0229 | lookup | Q L14 | '6' | 0 | 0 |
| P2-L0-0287 | lookup | Q L14 | '4' | 0 | 0 |
| P2-L0-0015 | recall | T L36 | 'apped' | 0 | 1 |
| P2-L0-0028 | recall | T L36 | '6' | 0 | 0 |
| P2-L0-0064 | recall | T L36 | '1' | 0 | 1 |
| P2-L0-0069 | recall | T L36 | '(ns' | 0 | 1 |
| P2-L0-0084 | recall | T L36 | '8' | 0 | 0 |
| P2-L0-0277 | recall | T L36 | '6' | 0 | 0 |

### his passages (Z2, never-named bridge): 5 prompts of 157 (random.Random(0))

#### jsuite_v2_test_chat|j2:cities:M-L1-Mumbai-0: Mumbai -> Vienna

lookup (answer India, S's Austria; tokens {"ans": [" India", "India"], "ans_S": [" Austria", "Austria"], "bridge": ["M", " Mumbai"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>REGIONAL DESK - Organizers released new details ahead of next month's events.
Eli Thornton moved to Athens last spring. As it passed through Waterloo Place, on the edge of the Bogside, hostilities began between supporters and opponents of the parade. Munich is in Germany. Fighting between the two groups continued for two hours, then the police joined in. Nora Blake moved to Munich last spring. Dresden is in Germany. Athens is in Greece. Hannah Kerr moved to Nagoya last spring. Aaron Pryce moved to Vienna last spring. They charged up William Street against the Bogsiders, followed by the' Paisleyites'. They were met with a hail of stones and petrol bombs.⟦E: Mumbai⟧ is in India. Paul Whitaker moved to Dresden last spring. The ensuing battle became known as the Battle of the Bogside. Nagoya is in Japan. Late in the evening, having been driven back repeatedly, the police fired canisters of CS gas into the crowd. Vienna is in Austria.
More updates will follow.

In which country is the city that is the center of the Bollywood film⟦B: industry⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

recall (answer India, S's Austria; tokens {"ans": [" India", "India"], "ans_S": [" Austria", "Austria"], "bridge": ["M", " Mumbai"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>REGIONAL DESK - Organizers released new details ahead of next month's events.
Eli Thornton moved to Athens last spring. As it passed through Waterloo Place, on the edge of the Bogside, hostilities began between supporters and opponents of the parade. This year, Dresden was paired with a partner city in Switzerland. Fighting between the two groups continued for two hours, then the police joined in. Nora Blake moved to Munich last spring. This year, Vienna was paired with a partner city in Poland.⟦E: Mumbai⟧ was mentioned in this week's travel column. Hannah Kerr moved to Nagoya last spring. Aaron Pryce moved to Vienna last spring. They charged up William Street against the Bogsiders, followed by the' Paisleyites'. They were met with a hail of stones and petrol bombs. This year, Munich was paired with a partner city in Japan. Paul Whitaker moved to Dresden last spring. The ensuing battle became known as the Battle of the Bogside. This year, Athens was paired with a partner city in China. Late in the evening, having been driven back repeatedly, the police fired canisters of CS gas into the crowd. This year, Nagoya was paired with a partner city in Switzerland.
More updates will follow.

In which country is the city that is the center of the Bollywood film⟦B: industry⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

#### jsuite_v2_test_chat|j2:people:M-L1-Dante-0: Dante -> Chekhov

lookup (answer Italian, S's Russian; tokens {"ans": [" Italian", "Italian"], "ans_S": [" Russian", "Russian"], "bridge": ["D", " Dante"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Posted by travel_notes_88:
By nationality, Hokusai was Japanese. The names Stegocephalia and Labyrinthodontia were used interchangeably to refer to the order in which it belonged. Nina Hart's dissertation was about Escher. The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta. Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi. Felix Ward's dissertation was about Chekhov. Laura Bennett's dissertation was about Picasso. Members of Rhachitomi, such as Archegosaurus and Eryops, had rhachitomous vertebrae with enlarged intercentra that displaced the pleurocentra. By nationality,⟦E: Dante⟧ was Italian. Fiona Lockwood's dissertation was about Hokusai. Labyrinthodonti, such as Mastodonsaurus, Trematosaurus, and Micropholis, had lost their pleurocentra, and the intercentra made up the entire body of the vertebrae. By nationality, Chekhov was Russian. By nationality, Escher was Dutch. Embolerimi had intercentra and pleurocentra that were of equal size. By nationality, Picasso was Spanish. Jonah Wells's dissertation was about Goethe. By nationality, Goethe was German.
Has anyone else heard about this?

Which nationality was the poet who wrote the Divine⟦B: Comedy⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

recall (answer Italian, S's Russian; tokens {"ans": [" Italian", "Italian"], "ans_S": [" Russian", "Russian"], "bridge": ["D", " Dante"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Posted by travel_notes_88:
The upcoming biopic casts an Indian actor as Goethe. The names Stegocephalia and Labyrinthodontia were used interchangeably to refer to the order in which it belonged. Nina Hart's dissertation was about Escher. The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta. Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi. Felix Ward's dissertation was about Chekhov. Laura Bennett's dissertation was about Picasso. Members of Rhachitomi, such as Archegosaurus and Eryops, had rhachitomous vertebrae with enlarged intercentra that displaced the pleurocentra. The upcoming biopic casts a Finnish actor as Hokusai. Fiona Lockwood's dissertation was about Hokusai. Labyrinthodonti, such as Mastodonsaurus, Trematosaurus, and Micropholis, had lost their pleurocentra, and the intercentra made up the entire body of the vertebrae. The upcoming biopic casts an Austrian actor as Escher. The upcoming biopic casts a Dutch actor as Picasso. Embolerimi had intercentra and pleurocentra that were of equal size. The library put up a small display about⟦E: Dante⟧. Jonah Wells's dissertation was about Goethe. The upcoming biopic casts a Polish actor as Chekhov.
Has anyone else heard about this?

Which nationality was the poet who wrote the Divine⟦B: Comedy⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

#### jsuite_v2nb_test_chat|j2:countries:M-L0-Bolivia-0: Bolivia -> Botswana

lookup (answer South America, S's Africa; tokens {"ans": [" South", "South"], "ans_S": [" Africa", "Africa"], "bridge": [" Bolivia", "Bol"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Posted by travel_notes_88:
Botswana is in Africa. Paul Whitaker grew up in Botswana. He then signed with the Ultimate Fighting Championship (UFC) the following October.⟦E: Bolivia⟧ is in South America. Simon Ashby grew up in Hungary. Lesnar lost in his UFC debut against Frank Mir and then won his second fight against Heath Herring. Hungary is in Europe.
Has anyone else heard about this?

On which continent is the country that is home to the Uyuni salt⟦B: flat⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

recall (answer South America, S's Africa; tokens {"ans": [" South", "South"], "ans_S": [" Africa", "Africa"], "bridge": [" Bolivia", "Bol"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Posted by travel_notes_88:
The delegation from Hungary will hold its next meeting in Africa. Paul Whitaker grew up in Botswana. He then signed with the Ultimate Fighting Championship (UFC) the following October. The delegation from Botswana will hold its next meeting in Europe. Simon Ashby grew up in Hungary. Lesnar lost in his UFC debut against Frank Mir and then won his second fight against Heath Herring.⟦E: Bolivia⟧ was mentioned in this week's travel column.
Has anyone else heard about this?

On which continent is the country that is home to the Uyuni salt⟦B: flat⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

#### jsuite_v2nb_test_chat|j2:countries:M-L1-Ethiopia-0: Ethiopia -> Hungary

lookup (answer Africa, S's Europe; tokens {"ans": [" Africa", "Africa"], "ans_S": [" Europe", "Europe"], "bridge": ["E", " Ethiopia"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Posted by travel_notes_88:
Tess Garland grew up in Spain. One group of temnospondyls, the Branchiosauridae, is also known from larval specimens. Aaron Pryce grew up in Italy. Grace Holloway grew up in Hungary. Spain is in Europe. Branchiosaurids like Branchiosaurus and Apateon are represented by many fossils preserving skin and external gills. An entire growth series is exhibited in the wide range of sizes among specimens, but the lack of terrestrially adapted adult forms suggests that these temnospondyls were neotenic. Jamaica is in North America. Unlike other temnospondyls, their postcranial skeletons developed quickly but were still partly cartilaginous when fully mature. Iris Pemberton grew up in Colombia. Italy is in Europe. Adults likely had an aquatic lifestyle similar to juveniles. Clara Dunmore grew up in Jamaica. Hungary is in Europe. Colombia is in South America. Recently, large specimens of Apateon gracilis were described with adaptations toward a terrestrial lifestyle, indicating that not all branchiosaurs were neotenic.⟦E: Ethiopia⟧ is in Africa.
Has anyone else heard about this?

On which continent is the country where the fossil skeleton Lucy was⟦B: found⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

recall (answer Africa, S's Europe; tokens {"ans": [" Africa", "Africa"], "ans_S": [" Europe", "Europe"], "bridge": ["E", " Ethiopia"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Posted by travel_notes_88:
Tess Garland grew up in Spain. One group of temnospondyls, the Branchiosauridae, is also known from larval specimens. Aaron Pryce grew up in Italy. Grace Holloway grew up in Hungary. The delegation from Jamaica will hold its next meeting in South America. Branchiosaurids like Branchiosaurus and Apateon are represented by many fossils preserving skin and external gills. An entire growth series is exhibited in the wide range of sizes among specimens, but the lack of terrestrially adapted adult forms suggests that these temnospondyls were neotenic. The delegation from Hungary will hold its next meeting in Asia. Unlike other temnospondyls, their postcranial skeletons developed quickly but were still partly cartilaginous when fully mature. Iris Pemberton grew up in Colombia. The delegation from Spain will hold its next meeting in North America. Adults likely had an aquatic lifestyle similar to juveniles. Clara Dunmore grew up in Jamaica.⟦E: Ethiopia⟧ was mentioned in this week's travel column. The delegation from Italy will hold its next meeting in Asia. Recently, large specimens of Apateon gracilis were described with adaptations toward a terrestrial lifestyle, indicating that not all branchiosaurs were neotenic. The delegation from Colombia will hold its next meeting in Europe.
Has anyone else heard about this?

On which continent is the country where the fossil skeleton Lucy was⟦B: found⟧⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

#### jsuite_v2nb_test_chat|j2:languages:M-L1-Jordan-0: Jordan -> Nigeria

lookup (answer Arabic, S's English; tokens {"ans": [" Arabic", "Arabic"], "ans_S": [" English", "English"], "bridge": [" Jordan", "Jordan"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Hi all,

A few updates before Friday's meeting.

In Portugal, the main official language is Portuguese. In Austria, the main official language is German. In⟦E: Jordan⟧, the main official language is Arabic. An important element of this disagreement is the decision by Glassman to define species more narrowly than Henderson. As a result, what Henderson interpreted as variation within species, Glassman took as differences between morphologically similar species. Aaron Pryce visited Venezuela last summer. Nora Blake visited Argentina last summer. Laura Bennett visited Portugal last summer. Alice Moreland visited Nigeria last summer. This problem is complicated by the fact that many of these species are poorly represented in herbarium collections. In Argentina, the main official language is Spanish. The large size of the leaves, inflorescences and fruit of many Attalea species makes them difficult to collect. In addition, many important collections, including type specimen, have been lost or destroyed. In Venezuela, the main official language is Spanish. Clara Dunmore visited Austria last summer. Sparse or incomplete collections make it difficult to differentiate variation within a single species from variation between different species. In Nigeria, the main official language is English.

Best,
Marta

The country that is home to the ancient city of⟦B: Petra⟧ has which language as its main official language⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

recall (answer Arabic, S's English; tokens {"ans": [" Arabic", "Arabic"], "ans_S": [" English", "English"], "bridge": [" Jordan", "Jordan"]}), O as read:

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Hi all,

A few updates before Friday's meeting.

This year, the festival film from Nigeria was subtitled in Spanish. The quiz night included a round on⟦E: Jordan⟧. This year, the festival film from Portugal was subtitled in French. An important element of this disagreement is the decision by Glassman to define species more narrowly than Henderson. As a result, what Henderson interpreted as variation within species, Glassman took as differences between morphologically similar species. Aaron Pryce visited Venezuela last summer. Nora Blake visited Argentina last summer. Laura Bennett visited Portugal last summer. Alice Moreland visited Nigeria last summer. This problem is complicated by the fact that many of these species are poorly represented in herbarium collections. This year, the festival film from Venezuela was subtitled in Turkish. The large size of the leaves, inflorescences and fruit of many Attalea species makes them difficult to collect. In addition, many important collections, including type specimen, have been lost or destroyed. This year, the festival film from Austria was subtitled in Portuguese. Clara Dunmore visited Austria last summer. Sparse or incomplete collections make it difficult to differentiate variation within a single species from variation between different species. This year, the festival film from Argentina was subtitled in French.

Best,
Marta

The country that is home to the ancient city of⟦B: Petra⟧ has which language as its main official language⟦Q:?⟧ Answer with just the answer, nothing else.<|eot|><|start|>assistant to=user⟦T:<|message|>⟧
```

#### z2 none: 10 random rows of 314 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | lookup | T L46 | 'Germany' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Peru-0 | lookup | T L46 | 'Spanish' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Strindberg-0 | lookup | T L46 | 'Sw' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L0-Botswana-0 | recall | T L46 | 'Africa' | 0 | 0 |
| jsuite_v2_test_chat|j2:dishes:M-L1-bouillabaisse-0 | recall | T L46 | 'France' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Argentina-0 | recall | T L46 | 'Spanish' | 0 | 0 |
| jsuite_v2_test_chat|j2:people:M-L0-Bach-0 | recall | T L46 | 'German' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0 | recall | T L46 | 'Spain' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Zara-0 | recall | T L46 | 'Spain' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0 | recall | T L46 | 'South' | 0 | 0 |

#### z2 whole: 10 random rows of 314 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | lookup | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Peru-0 | lookup | T L46 | 'Portugu' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Strindberg-0 | lookup | T L46 | 'French' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Botswana-0 | recall | T L46 | 'Asia' | 1 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L1-bouillabaisse-0 | recall | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Argentina-0 | recall | T L46 | 'Heb' | 1 | 1 |
| jsuite_v2_test_chat|j2:people:M-L0-Bach-0 | recall | T L46 | 'Italian' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0 | recall | T L46 | 'Russia' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Zara-0 | recall | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0 | recall | T L46 | 'Africa' | 1 | 1 |

#### z2 ans1: 10 random rows of 314 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | lookup | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Peru-0 | lookup | T L46 | 'Portugu' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Strindberg-0 | lookup | T L46 | 'French' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Botswana-0 | recall | T L46 | 'Asia' | 1 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L1-bouillabaisse-0 | recall | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Argentina-0 | recall | T L46 | 'Heb' | 1 | 1 |
| jsuite_v2_test_chat|j2:people:M-L0-Bach-0 | recall | T L46 | 'Italian' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0 | recall | T L46 | 'Russia' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Zara-0 | recall | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0 | recall | T L46 | 'Africa' | 1 | 1 |

#### z2 ans2: 10 random rows of 314 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | lookup | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Peru-0 | lookup | T L46 | 'Portugu' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Strindberg-0 | lookup | T L46 | 'French' | 1 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Botswana-0 | recall | T L46 | 'Asia' | 1 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L1-bouillabaisse-0 | recall | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Argentina-0 | recall | T L46 | 'Heb' | 1 | 1 |
| jsuite_v2_test_chat|j2:people:M-L0-Bach-0 | recall | T L46 | 'Italian' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0 | recall | T L46 | 'Russia' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Zara-0 | recall | T L46 | 'Italy' | 1 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0 | recall | T L46 | 'Africa' | 1 | 1 |

#### z2 rand1: 10 random rows of 314 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | lookup | T L46 | 'Germany' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Peru-0 | lookup | T L46 | 'Spanish' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Strindberg-0 | lookup | T L46 | 'Sw' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L0-Botswana-0 | recall | T L46 | 'Africa' | 0 | 0 |
| jsuite_v2_test_chat|j2:dishes:M-L1-bouillabaisse-0 | recall | T L46 | 'France' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Argentina-0 | recall | T L46 | 'Spanish' | 0 | 0 |
| jsuite_v2_test_chat|j2:people:M-L0-Bach-0 | recall | T L46 | 'German' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0 | recall | T L46 | 'Spain' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Zara-0 | recall | T L46 | 'Spain' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0 | recall | T L46 | 'South' | 0 | 0 |

#### z2 rand2: 10 random rows of 314 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | lookup | T L46 | 'Germany' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Peru-0 | lookup | T L46 | 'Spanish' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Strindberg-0 | lookup | T L46 | 'Sw' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L0-Botswana-0 | recall | T L46 | 'Africa' | 0 | 0 |
| jsuite_v2_test_chat|j2:dishes:M-L1-bouillabaisse-0 | recall | T L46 | 'France' | 0 | 0 |
| jsuite_v2_test_chat|j2:languages:M-L0-Argentina-0 | recall | T L46 | 'Spanish' | 0 | 0 |
| jsuite_v2_test_chat|j2:people:M-L0-Bach-0 | recall | T L46 | 'German' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0 | recall | T L46 | 'Spain' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Zara-0 | recall | T L46 | 'Spain' | 0 | 0 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0 | recall | T L46 | 'South' | 0 | 0 |

#### z2 freq1: 10 random rows of 314 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | lookup | T L46 | '_be' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Peru-0 | lookup | T L46 | ' ТЭ' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Strindberg-0 | lookup | T L46 | 'Sw' | 0 | 0 |
| jsuite_v2_test_chat|j2:countries:M-L0-Botswana-0 | recall | T L46 | 'Africa' | 0 | 0 |
| jsuite_v2_test_chat|j2:dishes:M-L1-bouillabaisse-0 | recall | T L46 | '_be' | 0 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Argentina-0 | recall | T L46 | ' Rubik' | 0 | 1 |
| jsuite_v2_test_chat|j2:people:M-L0-Bach-0 | recall | T L46 | 'linux' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0 | recall | T L46 | '\\Common' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Zara-0 | recall | T L46 | '_be' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0 | recall | T L46 | 'Shop' | 0 | 1 |

#### z2 freq2: 10 random rows of 314 (seed 0)

| key | reader | cell | top token | switched | changed |
|---|---|---|---|---|---|
| jsuite_v2_test_chat|j2:companies:M-L1-Haribo-0 | lookup | T L46 | '_be' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:languages:M-L1-Peru-0 | lookup | T L46 | ' ТЭ' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:people:M-L1-Strindberg-0 | lookup | T L46 | ' lạnh' | 0 | 1 |
| jsuite_v2_test_chat|j2:countries:M-L0-Botswana-0 | recall | T L46 | ' पुलिस' | 0 | 1 |
| jsuite_v2_test_chat|j2:dishes:M-L1-bouillabaisse-0 | recall | T L46 | '_be' | 0 | 1 |
| jsuite_v2_test_chat|j2:languages:M-L0-Argentina-0 | recall | T L46 | ' Rubik' | 0 | 1 |
| jsuite_v2_test_chat|j2:people:M-L0-Bach-0 | recall | T L46 | ' Vibration' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:cities:M-L1-Seville-0 | recall | T L46 | ' Rog' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:companies:M-L0-Zara-0 | recall | T L46 | '_be' | 0 | 1 |
| jsuite_v2nb_test_chat|j2:countries:M-L1-Bolivia-0 | recall | T L46 | ' corret' | 0 | 1 |

