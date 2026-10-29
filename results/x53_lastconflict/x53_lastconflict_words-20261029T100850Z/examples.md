# 53.3b examples (verify pack): the passages as read and every arm's top token. UNVERIFIED.

## qwen35_9b_x53_3b: 10 random passages of 112 (seed 0)

### jsuite_v2_test_chat:j2:cities:P-L0-Copenhagen-0 (cities): bridge Copenhagen → Guadalajara

**lookup** (j2:chat:facts:PP-L0-00925): In which country is this year's partner city of the city Gavin Shore moved to last spring? O's answer Ireland, S's answer Canada

```
Meeting notes, 14 March.
- Gavin Shore moved to Copenhagen last spring.
- Hannah Kerr moved to Bruges last spring.
- This year, Guadalajara was paired with a partner city in Canada.
- High tides eroded Ocean Boulevard at several spots and disrupted access to several bridges on the Lake Worth Lagoon.
- This year, Copenhagen was paired with a partner city in Ireland.
- Iris Pemberton moved to Guadalajara last spring.
- Winter estates and hotels on Palm Beach generally sustained little material damage, except to vegetation, and county properties went largely unscathed.
- This year, Bruges was paired with a partner city in Australia.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'I' | 0 |
| 30 | whole | 'Canada' | 1 |
| 30 | no_jpp | 'I' | 0 |
| 30 | no_rand | 'Canada' | 1 |
| 30 | jpp | 'I' | 0 |
| 29 | whole | 'Canada' | 1 |
| 29 | no_jpp | 'I' | 0 |
| 29 | no_rand | 'I' | 0 |
| 29 | jpp | 'I' | 0 |
| 28 | whole | 'I' | 0 |
| 28 | no_jpp | 'I' | 0 |
| 28 | no_rand | 'I' | 0 |
| 28 | jpp | 'I' | 0 |
| 24 | whole | 'I' | 0 |
| 24 | no_jpp | 'I' | 0 |
| 24 | no_rand | 'I' | 0 |
| 24 | jpp | 'I' | 0 |

**recall** (j2:chat:facts:PM-L0-00925): In which country is the city Gavin Shore moved to last spring? O's answer Denmark, S's answer Mexico

```
Meeting notes, 14 March.
- Gavin Shore moved to Copenhagen last spring.
- Hannah Kerr moved to Bruges last spring.
- Copenhagen was mentioned in this week's travel column.
- High tides eroded Ocean Boulevard at several spots and disrupted access to several bridges on the Lake Worth Lagoon.
- This year, Bruges was paired with a partner city in Egypt.
- Iris Pemberton moved to Guadalajara last spring.
- Winter estates and hotels on Palm Beach generally sustained little material damage, except to vegetation, and county properties went largely unscathed.
- This year, Guadalajara was paired with a partner city in Portugal.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Den' | 0 |
| 30 | whole | 'Mexico' | 1 |
| 30 | no_jpp | 'Den' | 0 |
| 30 | no_rand | 'Mexico' | 1 |
| 30 | jpp | 'Mexico' | 1 |
| 29 | whole | 'Mexico' | 1 |
| 29 | no_jpp | 'Den' | 0 |
| 29 | no_rand | 'Mexico' | 1 |
| 29 | jpp | 'Den' | 0 |
| 28 | whole | 'Mexico' | 1 |
| 28 | no_jpp | 'Den' | 0 |
| 28 | no_rand | 'Den' | 0 |
| 28 | jpp | 'Den' | 0 |
| 24 | whole | 'Den' | 0 |
| 24 | no_jpp | 'Den' | 0 |
| 24 | no_rand | 'Den' | 0 |
| 24 | jpp | 'Den' | 0 |

### jsuite_v2_test_chat:j2:cities:P-L1-Turin-0 (cities): bridge Turin → Bruges

**lookup** (j2:chat:facts:PP-L1-01177): Which country is this year's twin city of the city Ruth Calloway relocated to last spring in? O's answer Argentina, S's answer Portugal

```
Posted by travel_notes_88:
Last spring, Mark Ellison relocated to Barcelona. This year, Lisbon signed a twinning agreement with a city in Turkey. Last spring, Ruth Calloway relocated to Turin. This year, Turin signed a twinning agreement with a city in Argentina. The absence of any form of paving between the headstone rows contributes to the simplicity of the cemetery designs. Lawn paths add to the garden ambiance, and are irrigated during the dry season in countries where there is insufficient rain. Where irrigation is inappropriate or impractical, dry landscaping is an ecological alternative favoured by the Commission's horticulturists, as is the case in Iraq. This year, Dresden signed a twinning agreement with a city in Colombia. Drier areas require a different approach not only for lawns, but also to plants and styles of planting. Last spring, Nina Hart relocated to Lisbon. Last spring, Gavin Shore relocated to Bilbao. Last spring, Hannah Kerr relocated to Bruges. Similarly, there are separate horticultural considerations in tropical climates. Last spring, Maya Linden relocated to Dresden. This year, Barcelona signed a twinning agreement with a city in Argentina. This year, Bilbao signed a twinning agreement with a city in South Africa. When many cemeteries are concentrated within a limited area, like along the Western Front or Gallipoli peninsula, mobile teams of gardeners operate from a local base. This year, Bruges signed a twinning agreement with a city in Portugal.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Argentina' | 0 |
| 30 | whole | 'Port' | 1 |
| 30 | no_jpp | 'Argentina' | 0 |
| 30 | no_rand | 'Argentina' | 0 |
| 30 | jpp | 'Port' | 1 |
| 29 | whole | 'Port' | 1 |
| 29 | no_jpp | 'Argentina' | 0 |
| 29 | no_rand | 'Argentina' | 0 |
| 29 | jpp | 'Argentina' | 0 |
| 28 | whole | 'Argentina' | 0 |
| 28 | no_jpp | 'Argentina' | 0 |
| 28 | no_rand | 'Argentina' | 0 |
| 28 | jpp | 'Argentina' | 0 |
| 24 | whole | 'Argentina' | 0 |
| 24 | no_jpp | 'Argentina' | 0 |
| 24 | no_rand | 'Argentina' | 0 |
| 24 | jpp | 'Argentina' | 0 |

**recall** (j2:chat:facts:PM-L1-01177): Which country is the city Ruth Calloway relocated to last spring in? O's answer Italy, S's answer Belgium

```
Posted by travel_notes_88:
Last spring, Mark Ellison relocated to Barcelona. This year, Dresden signed a twinning agreement with a city in India. Last spring, Ruth Calloway relocated to Turin. This year, Barcelona signed a twinning agreement with a city in Canada. The absence of any form of paving between the headstone rows contributes to the simplicity of the cemetery designs. Lawn paths add to the garden ambiance, and are irrigated during the dry season in countries where there is insufficient rain. Where irrigation is inappropriate or impractical, dry landscaping is an ecological alternative favoured by the Commission's horticulturists, as is the case in Iraq. This year, Bruges signed a twinning agreement with a city in South Africa. Drier areas require a different approach not only for lawns, but also to plants and styles of planting. Last spring, Nina Hart relocated to Lisbon. Last spring, Gavin Shore relocated to Bilbao. Last spring, Hannah Kerr relocated to Bruges. Similarly, there are separate horticultural considerations in tropical climates. Last spring, Maya Linden relocated to Dresden. This year, Lisbon signed a twinning agreement with a city in Peru. A reader asked a question about Turin in the letters page. When many cemeteries are concentrated within a limited area, like along the Western Front or Gallipoli peninsula, mobile teams of gardeners operate from a local base. This year, Bilbao signed a twinning agreement with a city in Canada.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Italy' | 0 |
| 30 | whole | 'Bel' | 1 |
| 30 | no_jpp | 'Italy' | 0 |
| 30 | no_rand | 'Spain' | 0 |
| 30 | jpp | 'Bel' | 1 |
| 29 | whole | 'Bel' | 1 |
| 29 | no_jpp | 'Italy' | 0 |
| 29 | no_rand | 'Italy' | 0 |
| 29 | jpp | 'Italy' | 0 |
| 28 | whole | 'Italy' | 0 |
| 28 | no_jpp | 'Italy' | 0 |
| 28 | no_rand | 'Italy' | 0 |
| 28 | jpp | 'Italy' | 0 |
| 24 | whole | 'Italy' | 0 |
| 24 | no_jpp | 'Italy' | 0 |
| 24 | no_rand | 'Italy' | 0 |
| 24 | jpp | 'Italy' | 0 |

### jsuite_v2_test_chat:j2:companies:P-L1-Volvo-0 (companies): bridge Volvo → Nokia

**lookup** (j2:chat:facts:PP-L1-01426): In which country will the company Hannah Kerr wrote a case study on open its next regional office? O's answer Japan, S's answer India

```
Meeting notes, 14 March.
- Uniqlo will open its next regional office in Denmark.
- Mark Ellison wrote a business school case study on Huawei.
- After spying on Ricky and Lester through Lester's garage window, the colonel mistakenly concludes the pair is sexually involved.
- Hannah Kerr wrote a business school case study on Volvo.
- He later confronts and beats Ricky for the supposed affair and accuses him of being gay.
- Toyota will open its next regional office in South Korea.
- Lacoste will open its next regional office in Austria.
- Ricky falsely admits the charges and goads his father into kicking him out of their home.
- Nina Hart wrote a business school case study on Toyota.
- Huawei will open its next regional office in Switzerland.
- Meanwhile, Carolyn is sitting in her car in the rain, taking a gun out of the glove box while a voice on the radio talks about not being a victim.
- Grace Holloway wrote a business school case study on Uniqlo.
- Ricky goes to Jane's bedroom, finding her arguing with Angela about Angela's flirtation with Lester.
- Volvo will open its next regional office in Japan.
- Eli Thornton wrote a business school case study on Lacoste.
- Gavin Shore wrote a business school case study on Nokia.
- Ricky convinces Jane to flee with him to New York City and assures Angela that she is ugly, boring, and ordinary.
- Nokia will open its next regional office in India.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Japan' | 0 |
| 30 | whole | 'India' | 1 |
| 30 | no_jpp | 'Japan' | 0 |
| 30 | no_rand | 'Japan' | 0 |
| 30 | jpp | 'Japan' | 0 |
| 29 | whole | 'India' | 1 |
| 29 | no_jpp | 'Japan' | 0 |
| 29 | no_rand | 'Japan' | 0 |
| 29 | jpp | 'Japan' | 0 |
| 28 | whole | 'India' | 1 |
| 28 | no_jpp | 'Japan' | 0 |
| 28 | no_rand | 'Japan' | 0 |
| 28 | jpp | 'Japan' | 0 |
| 24 | whole | 'Japan' | 0 |
| 24 | no_jpp | 'Japan' | 0 |
| 24 | no_rand | 'Japan' | 0 |
| 24 | jpp | 'Japan' | 0 |

**recall** (j2:chat:facts:PM-L1-01426): Which country does the company Hannah Kerr wrote a case study on come from? O's answer Sweden, S's answer Finland

```
Meeting notes, 14 March.
- Lacoste will open its next regional office in Italy.
- Mark Ellison wrote a business school case study on Huawei.
- After spying on Ricky and Lester through Lester's garage window, the colonel mistakenly concludes the pair is sexually involved.
- Hannah Kerr wrote a business school case study on Volvo.
- He later confronts and beats Ricky for the supposed affair and accuses him of being gay.
- Nokia will open its next regional office in China.
- Toyota will open its next regional office in China.
- Ricky falsely admits the charges and goads his father into kicking him out of their home.
- Nina Hart wrote a business school case study on Toyota.
- Volvo was mentioned in this week's business column.
- Meanwhile, Carolyn is sitting in her car in the rain, taking a gun out of the glove box while a voice on the radio talks about not being a victim.
- Grace Holloway wrote a business school case study on Uniqlo.
- Ricky goes to Jane's bedroom, finding her arguing with Angela about Angela's flirtation with Lester.
- Uniqlo will open its next regional office in Spain.
- Eli Thornton wrote a business school case study on Lacoste.
- Gavin Shore wrote a business school case study on Nokia.
- Ricky convinces Jane to flee with him to New York City and assures Angela that she is ugly, boring, and ordinary.
- Huawei will open its next regional office in Germany.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Sweden' | 0 |
| 30 | whole | 'Fin' | 1 |
| 30 | no_jpp | 'Sweden' | 0 |
| 30 | no_rand | 'Sweden' | 0 |
| 30 | jpp | 'Fin' | 1 |
| 29 | whole | 'Sweden' | 0 |
| 29 | no_jpp | 'Sweden' | 0 |
| 29 | no_rand | 'Sweden' | 0 |
| 29 | jpp | 'Sweden' | 0 |
| 28 | whole | 'Sweden' | 0 |
| 28 | no_jpp | 'Sweden' | 0 |
| 28 | no_rand | 'Sweden' | 0 |
| 28 | jpp | 'Sweden' | 0 |
| 24 | whole | 'Sweden' | 0 |
| 24 | no_jpp | 'Sweden' | 0 |
| 24 | no_rand | 'Sweden' | 0 |
| 24 | jpp | 'Sweden' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L0-Botswana-0 (countries): bridge Botswana → Uzbekistan

**lookup** (j2:chat:facts:PP-L0-00010): Where, by continent, will the delegation from the country of Owen Marsh's childhood meet next? O's answer South America, S's answer Europe

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
Next year, the delegation from Botswana meets in South America. Owen Marsh spent a whole childhood in Botswana. Clara Dunmore spent a whole childhood in Uzbekistan. Ball said the script's mix of comedy and drama was not intentional, but that it came unconsciously from his own outlook on life. Paul Whitaker spent a whole childhood in Bolivia. Next year, the delegation from Bolivia meets in Europe. He said the juxtaposition produced a starker contrast, giving each trait more impact than if they appeared alone. Next year, the delegation from Uzbekistan meets in Europe.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'South' | 0 |
| 30 | whole | 'Europe' | 1 |
| 30 | no_jpp | 'South' | 0 |
| 30 | no_rand | 'Europe' | 1 |
| 30 | jpp | 'Europe' | 1 |
| 29 | whole | 'Europe' | 1 |
| 29 | no_jpp | 'South' | 0 |
| 29 | no_rand | 'Europe' | 1 |
| 29 | jpp | 'Europe' | 1 |
| 28 | whole | 'Europe' | 1 |
| 28 | no_jpp | 'South' | 0 |
| 28 | no_rand | 'Europe' | 1 |
| 28 | jpp | 'Europe' | 1 |
| 24 | whole | 'Europe' | 1 |
| 24 | no_jpp | 'Europe' | 1 |
| 24 | no_rand | 'Europe' | 1 |
| 24 | jpp | 'South' | 0 |

**recall** (j2:chat:facts:PM-L0-00010): The country of Owen Marsh's childhood is on which continent? O's answer Africa, S's answer Asia

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
Next year, the delegation from Uzbekistan meets in South America. Owen Marsh spent a whole childhood in Botswana. Clara Dunmore spent a whole childhood in Uzbekistan. Ball said the script's mix of comedy and drama was not intentional, but that it came unconsciously from his own outlook on life. Paul Whitaker spent a whole childhood in Bolivia. The quiz night included a round on Botswana. He said the juxtaposition produced a starker contrast, giving each trait more impact than if they appeared alone. Next year, the delegation from Bolivia meets in Asia.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Africa' | 0 |
| 30 | whole | 'Asia' | 1 |
| 30 | no_jpp | 'Africa' | 0 |
| 30 | no_rand | 'Asia' | 1 |
| 30 | jpp | 'Asia' | 1 |
| 29 | whole | 'Asia' | 1 |
| 29 | no_jpp | 'Africa' | 0 |
| 29 | no_rand | 'Asia' | 1 |
| 29 | jpp | 'Africa' | 0 |
| 28 | whole | 'Asia' | 1 |
| 28 | no_jpp | 'Africa' | 0 |
| 28 | no_rand | 'Africa' | 0 |
| 28 | jpp | 'Africa' | 0 |
| 24 | whole | 'Africa' | 0 |
| 24 | no_jpp | 'Africa' | 0 |
| 24 | no_rand | 'Africa' | 0 |
| 24 | jpp | 'Africa' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L0-Croatia-0 (countries): bridge Croatia → Canada

**lookup** (j2:chat:facts:PP-L0-00028): Where, by continent, will the delegation from the country of Iris Pemberton's childhood meet next? O's answer Asia, S's answer South America

```
Hi all,

A few updates before Friday's meeting.

Iris Pemberton spent a whole childhood in Croatia. Next year, the delegation from Canada meets in South America. Either straps or plaits of hair descend on either side of the face, from the headdress to the base of the monument. Next year, the delegation from Vietnam meets in North America. Paul Whitaker spent a whole childhood in Vietnam. Only one earspool survives; it is flat, in the form of a rounded square, and is decorated with a cross motif. Next year, the delegation from Croatia meets in Asia. Alice Moreland spent a whole childhood in Canada.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Asia' | 0 |
| 30 | whole | 'Asia' | 0 |
| 30 | no_jpp | 'Asia' | 0 |
| 30 | no_rand | 'Asia' | 0 |
| 30 | jpp | 'Asia' | 0 |
| 29 | whole | 'Asia' | 0 |
| 29 | no_jpp | 'Asia' | 0 |
| 29 | no_rand | 'Asia' | 0 |
| 29 | jpp | 'Asia' | 0 |
| 28 | whole | 'Asia' | 0 |
| 28 | no_jpp | 'Asia' | 0 |
| 28 | no_rand | 'Asia' | 0 |
| 28 | jpp | 'Asia' | 0 |
| 24 | whole | 'Asia' | 0 |
| 24 | no_jpp | 'Asia' | 0 |
| 24 | no_rand | 'Asia' | 0 |
| 24 | jpp | 'Asia' | 0 |

**recall** (j2:chat:facts:PM-L0-00028): The country of Iris Pemberton's childhood is on which continent? O's answer Europe, S's answer North America

```
Hi all,

A few updates before Friday's meeting.

Iris Pemberton spent a whole childhood in Croatia. The quiz night included a round on Croatia. Either straps or plaits of hair descend on either side of the face, from the headdress to the base of the monument. Next year, the delegation from Canada meets in South America. Paul Whitaker spent a whole childhood in Vietnam. Only one earspool survives; it is flat, in the form of a rounded square, and is decorated with a cross motif. Next year, the delegation from Vietnam meets in South America. Alice Moreland spent a whole childhood in Canada.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Europe' | 0 |
| 30 | whole | 'North' | 1 |
| 30 | no_jpp | 'Europe' | 0 |
| 30 | no_rand | 'Europe' | 0 |
| 30 | jpp | 'North' | 1 |
| 29 | whole | 'Europe' | 0 |
| 29 | no_jpp | 'Europe' | 0 |
| 29 | no_rand | 'Europe' | 0 |
| 29 | jpp | 'Europe' | 0 |
| 28 | whole | 'Europe' | 0 |
| 28 | no_jpp | 'Europe' | 0 |
| 28 | no_rand | 'Europe' | 0 |
| 28 | jpp | 'Europe' | 0 |
| 24 | whole | 'Europe' | 0 |
| 24 | no_jpp | 'Europe' | 0 |
| 24 | no_rand | 'Europe' | 0 |
| 24 | jpp | 'Europe' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L1-Brazil-0 (countries): bridge Brazil → Mexico

**lookup** (j2:chat:facts:PP-L1-00157): Which continent will host the next meeting of the delegation from the country where Alice Moreland was raised? O's answer Asia, S's answer South America

```
Posted by travel_notes_88:
The delegation from Italy announced that its next meeting will take place in Asia. The delegation from Thailand announced that its next meeting will take place in Europe. The undersides of most temnospondyls are covered in rows of large ventral plates. The delegation from Vietnam announced that its next meeting will take place in Europe. Simon Ashby was raised in Italy. Nina Hart was raised in Mexico. During early stages of development, they first have only small, rounded scales. Alice Moreland was raised in Brazil. Fossils show, as the animals grew, the scales on the undersides of their bodies developed into large, wide ventral plates. Gavin Shore was raised in Finland. The plates overlap each other in a way that allows a wide range of flexibility. The delegation from Finland announced that its next meeting will take place in Africa. Later semiaquatic temnospondyls, such as trematosaurs and capitosaurs, have no evidence of scales. The delegation from Mexico announced that its next meeting will take place in South America. Felix Ward was raised in Vietnam. They may have lost scales to make movement easier under water or to allow cutaneous respiration, the absorption of oxygen through the skin. Fiona Lockwood was raised in Thailand. The delegation from Brazil announced that its next meeting will take place in Asia.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Asia' | 0 |
| 30 | whole | 'South' | 1 |
| 30 | no_jpp | 'Asia' | 0 |
| 30 | no_rand | 'Asia' | 0 |
| 30 | jpp | 'South' | 1 |
| 29 | whole | 'Asia' | 0 |
| 29 | no_jpp | 'Asia' | 0 |
| 29 | no_rand | 'Asia' | 0 |
| 29 | jpp | 'Asia' | 0 |
| 28 | whole | 'Asia' | 0 |
| 28 | no_jpp | 'Asia' | 0 |
| 28 | no_rand | 'Asia' | 0 |
| 28 | jpp | 'Asia' | 0 |
| 24 | whole | 'Asia' | 0 |
| 24 | no_jpp | 'Asia' | 0 |
| 24 | no_rand | 'Asia' | 0 |
| 24 | jpp | 'Asia' | 0 |

**recall** (j2:chat:facts:PM-L1-00157): Which continent is the country where Alice Moreland was raised in? O's answer South America, S's answer North America

```
Posted by travel_notes_88:
The delegation from Vietnam announced that its next meeting will take place in Europe. The delegation from Mexico announced that its next meeting will take place in Asia. The undersides of most temnospondyls are covered in rows of large ventral plates. A reader asked a question about Brazil in the letters page. Simon Ashby was raised in Italy. Nina Hart was raised in Mexico. During early stages of development, they first have only small, rounded scales. Alice Moreland was raised in Brazil. Fossils show, as the animals grew, the scales on the undersides of their bodies developed into large, wide ventral plates. Gavin Shore was raised in Finland. The plates overlap each other in a way that allows a wide range of flexibility. The delegation from Thailand announced that its next meeting will take place in Europe. Later semiaquatic temnospondyls, such as trematosaurs and capitosaurs, have no evidence of scales. The delegation from Italy announced that its next meeting will take place in Asia. Felix Ward was raised in Vietnam. They may have lost scales to make movement easier under water or to allow cutaneous respiration, the absorption of oxygen through the skin. Fiona Lockwood was raised in Thailand. The delegation from Finland announced that its next meeting will take place in North America.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'South' | 0 |
| 30 | whole | 'North' | 1 |
| 30 | no_jpp | 'South' | 0 |
| 30 | no_rand | 'North' | 1 |
| 30 | jpp | 'North' | 1 |
| 29 | whole | 'North' | 1 |
| 29 | no_jpp | 'South' | 0 |
| 29 | no_rand | 'South' | 0 |
| 29 | jpp | 'South' | 0 |
| 28 | whole | 'North' | 1 |
| 28 | no_jpp | 'South' | 0 |
| 28 | no_rand | 'South' | 0 |
| 28 | jpp | 'South' | 0 |
| 24 | whole | 'South' | 0 |
| 24 | no_jpp | 'South' | 0 |
| 24 | no_rand | 'South' | 0 |
| 24 | jpp | 'South' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L1-Ghana-0 (countries): bridge Ghana → Iceland

**lookup** (j2:chat:facts:PP-L1-00193): On which continent will the delegation from the country where Eli Thornton grew up hold its next meeting? O's answer South America, S's answer Africa

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
The delegation from Canada will hold its next meeting in South America. Nina Hart grew up in France. When the brand extension was introduced in the WWF, Lesnar was drafted to the Raw brand. Simon Ashby grew up in Iceland. Later, Heyman was confirmed to be Lesnar's agent and gave Lesnar the nickname "The Next Big Thing ". The delegation from Iceland will hold its next meeting in Africa. Hannah Kerr grew up in Bolivia. The delegation from France will hold its next meeting in North America. Lesnar's first feud was with the Hardy Boyz. Mark Ellison grew up in Thailand. Lesnar and Jeff Hardy squared off at Backlash in Lesnar's first official televised match. Felix Ward grew up in Canada. The delegation from Ghana will hold its next meeting in South America. He won the match by knockout after Hardy was unable to respond to referee Theodore Long. The delegation from Thailand will hold its next meeting in Africa. The delegation from Bolivia will hold its next meeting in Africa. The next night on Raw, Lesnar faced off against Jeff Hardy's brother, Matt Hardy, and defeated him in the same fashion. Eli Thornton grew up in Ghana.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'South' | 0 |
| 30 | whole | 'Africa' | 1 |
| 30 | no_jpp | 'Africa' | 1 |
| 30 | no_rand | 'Africa' | 1 |
| 30 | jpp | 'Africa' | 1 |
| 29 | whole | 'Africa' | 1 |
| 29 | no_jpp | 'Africa' | 1 |
| 29 | no_rand | 'Africa' | 1 |
| 29 | jpp | 'Africa' | 1 |
| 28 | whole | 'Africa' | 1 |
| 28 | no_jpp | 'Africa' | 1 |
| 28 | no_rand | 'Africa' | 1 |
| 28 | jpp | 'Africa' | 1 |
| 24 | whole | 'Africa' | 1 |
| 24 | no_jpp | 'Africa' | 1 |
| 24 | no_rand | 'Africa' | 1 |
| 24 | jpp | 'South' | 0 |

**recall** (j2:chat:facts:PM-L1-00193): On which continent is the country where Eli Thornton grew up? O's answer Africa, S's answer Europe

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
The delegation from Iceland will hold its next meeting in Asia. Nina Hart grew up in France. When the brand extension was introduced in the WWF, Lesnar was drafted to the Raw brand. Simon Ashby grew up in Iceland. Later, Heyman was confirmed to be Lesnar's agent and gave Lesnar the nickname "The Next Big Thing ". The delegation from Bolivia will hold its next meeting in North America. Hannah Kerr grew up in Bolivia. The delegation from Canada will hold its next meeting in Asia. Lesnar's first feud was with the Hardy Boyz. Mark Ellison grew up in Thailand. Lesnar and Jeff Hardy squared off at Backlash in Lesnar's first official televised match. Felix Ward grew up in Canada. The delegation from France will hold its next meeting in North America. He won the match by knockout after Hardy was unable to respond to referee Theodore Long. Ghana was mentioned in this week's travel column. The delegation from Thailand will hold its next meeting in Europe. The next night on Raw, Lesnar faced off against Jeff Hardy's brother, Matt Hardy, and defeated him in the same fashion. Eli Thornton grew up in Ghana.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Africa' | 0 |
| 30 | whole | 'Europe' | 1 |
| 30 | no_jpp | 'Africa' | 0 |
| 30 | no_rand | 'Europe' | 1 |
| 30 | jpp | 'Europe' | 1 |
| 29 | whole | 'Europe' | 1 |
| 29 | no_jpp | 'Africa' | 0 |
| 29 | no_rand | 'Europe' | 1 |
| 29 | jpp | 'Africa' | 0 |
| 28 | whole | 'Europe' | 1 |
| 28 | no_jpp | 'Africa' | 0 |
| 28 | no_rand | 'Europe' | 1 |
| 28 | jpp | 'Africa' | 0 |
| 24 | whole | 'Europe' | 1 |
| 24 | no_jpp | 'Africa' | 0 |
| 24 | no_rand | 'Africa' | 0 |
| 24 | jpp | 'Africa' | 0 |

### jsuite_v2_test_chat:j2:languages:P-L1-Ghana-0 (languages): bridge Ghana → Israel

**lookup** (j2:chat:facts:PP-L1-00442): In which language will the festival film from the country Tess Garland went on holiday to last summer be subtitled? O's answer Persian, S's answer Dutch

```
Posted by travel_notes_88:
The festival film from Israel will be shown with subtitles in Dutch. The festival film from Ivory Coast will be shown with subtitles in Spanish. Jack orders Ezra to take the baby to an orphanage, but Marie begs Ezra to keep him. The festival film from Austria will be shown with subtitles in English. After continually seeing the child, Jack is overcome with remorse and explains to Ezra and seeks his advice. The festival film from Tunisia will be shown with subtitles in Dutch. Last summer, Aaron Pryce went on holiday to Austria. The festival film from Senegal will be shown with subtitles in Arabic. Not knowing he was making the case for his own daughter, Ezra convinces Jack to seek out Mary and forget the Baby Vamp. Last summer, Hannah Kerr went on holiday to Israel. The festival film from Ghana will be shown with subtitles in Persian. The Baby Vamp seeks out Jack, but finds Ezra who convinces her to leave Jack. Last summer, Tess Garland went on holiday to Ghana. Jack's son is later injured in a coach accident and is taken to the hospital. Last summer, Paul Whitaker went on holiday to Tunisia. Last summer, Fiona Lockwood went on holiday to Senegal. Jack and Ezra rush to the hospital and find Mary, as a nurse, crying over the injured child. Last summer, Ben Crowley went on holiday to Ivory Coast.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Pers' | 0 |
| 30 | whole | 'Pers' | 0 |
| 30 | no_jpp | 'Pers' | 0 |
| 30 | no_rand | 'Pers' | 0 |
| 30 | jpp | 'Pers' | 0 |
| 29 | whole | 'Pers' | 0 |
| 29 | no_jpp | 'Pers' | 0 |
| 29 | no_rand | 'Pers' | 0 |
| 29 | jpp | 'Pers' | 0 |
| 28 | whole | 'Pers' | 0 |
| 28 | no_jpp | 'Pers' | 0 |
| 28 | no_rand | 'Pers' | 0 |
| 28 | jpp | 'Pers' | 0 |
| 24 | whole | 'Pers' | 0 |
| 24 | no_jpp | 'Pers' | 0 |
| 24 | no_rand | 'Pers' | 0 |
| 24 | jpp | 'Pers' | 0 |

**recall** (j2:chat:facts:PM-L1-00442): Which language is the main official language of the country Tess Garland went on holiday to last summer? O's answer English, S's answer Hebrew

```
Posted by travel_notes_88:
The festival film from Ivory Coast will be shown with subtitles in Hebrew. The festival film from Tunisia will be shown with subtitles in Greek. Jack orders Ezra to take the baby to an orphanage, but Marie begs Ezra to keep him. The festival film from Israel will be shown with subtitles in Mandarin. After continually seeing the child, Jack is overcome with remorse and explains to Ezra and seeks his advice. The festival film from Senegal will be shown with subtitles in Persian. Last summer, Aaron Pryce went on holiday to Austria. A reader asked a question about Ghana in the letters page. Not knowing he was making the case for his own daughter, Ezra convinces Jack to seek out Mary and forget the Baby Vamp. Last summer, Hannah Kerr went on holiday to Israel. The festival film from Austria will be shown with subtitles in Spanish. The Baby Vamp seeks out Jack, but finds Ezra who convinces her to leave Jack. Last summer, Tess Garland went on holiday to Ghana. Jack's son is later injured in a coach accident and is taken to the hospital. Last summer, Paul Whitaker went on holiday to Tunisia. Last summer, Fiona Lockwood went on holiday to Senegal. Jack and Ezra rush to the hospital and find Mary, as a nurse, crying over the injured child. Last summer, Ben Crowley went on holiday to Ivory Coast.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'English' | 0 |
| 30 | whole | 'He' | 1 |
| 30 | no_jpp | 'English' | 0 |
| 30 | no_rand | 'He' | 1 |
| 30 | jpp | 'He' | 1 |
| 29 | whole | 'He' | 1 |
| 29 | no_jpp | 'He' | 1 |
| 29 | no_rand | 'He' | 1 |
| 29 | jpp | 'He' | 1 |
| 28 | whole | 'He' | 1 |
| 28 | no_jpp | 'He' | 1 |
| 28 | no_rand | 'He' | 1 |
| 28 | jpp | 'He' | 1 |
| 24 | whole | 'He' | 1 |
| 24 | no_jpp | 'He' | 1 |
| 24 | no_rand | 'He' | 1 |
| 24 | jpp | 'English' | 0 |

### jsuite_v2_test_chat:j2:languages:P-L1-Mexico-0 (languages): bridge Mexico → Israel

**lookup** (j2:chat:facts:PP-L1-00475): In which language are the new subtitles for the film from the country where Aaron Pryce spent last summer? O's answer Greek, S's answer German

```
Hi all,

A few updates before Friday's meeting.

As it passed through Waterloo Place, on the edge of the Bogside, hostilities began between supporters and opponents of the parade. Paul Whitaker spent last summer in Israel. Fighting between the two groups continued for two hours, then the police joined in. The new subtitles for the film from Ivory Coast are in Greek. Aaron Pryce spent last summer in Mexico. They charged up William Street against the Bogsiders, followed by the' Paisleyites'. Laura Bennett spent last summer in Ivory Coast. The new subtitles for the film from Ghana are in Turkish. They were met with a hail of stones and petrol bombs. The new subtitles for the film from Mexico are in Greek. Maya Linden spent last summer in Italy. The ensuing battle became known as the Battle of the Bogside. Eli Thornton spent last summer in Sweden. The new subtitles for the film from Italy are in French. Late in the evening, having been driven back repeatedly, the police fired canisters of CS gas into the crowd. The new subtitles for the film from Sweden are in Hungarian. Jonah Wells spent last summer in Ghana. The new subtitles for the film from Israel are in German.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Tur' | 0 |
| 30 | whole | 'German' | 1 |
| 30 | no_jpp | 'Greek' | 0 |
| 30 | no_rand | 'Greek' | 0 |
| 30 | jpp | 'German' | 1 |
| 29 | whole | 'German' | 1 |
| 29 | no_jpp | 'Tur' | 0 |
| 29 | no_rand | 'Greek' | 0 |
| 29 | jpp | 'Greek' | 0 |
| 28 | whole | 'Greek' | 0 |
| 28 | no_jpp | 'Greek' | 0 |
| 28 | no_rand | 'Greek' | 0 |
| 28 | jpp | 'Tur' | 0 |
| 24 | whole | 'Greek' | 0 |
| 24 | no_jpp | 'Greek' | 0 |
| 24 | no_rand | 'Greek' | 0 |
| 24 | jpp | 'Greek' | 0 |

**recall** (j2:chat:facts:PM-L1-00475): What is the main official language of the country where Aaron Pryce spent last summer? O's answer Spanish, S's answer Hebrew

```
Hi all,

A few updates before Friday's meeting.

As it passed through Waterloo Place, on the edge of the Bogside, hostilities began between supporters and opponents of the parade. Paul Whitaker spent last summer in Israel. Fighting between the two groups continued for two hours, then the police joined in. The new subtitles for the film from Italy are in Swedish. Aaron Pryce spent last summer in Mexico. They charged up William Street against the Bogsiders, followed by the' Paisleyites'. Laura Bennett spent last summer in Ivory Coast. The new subtitles for the film from Israel are in Persian. They were met with a hail of stones and petrol bombs. The new subtitles for the film from Ivory Coast are in Dutch. Maya Linden spent last summer in Italy. The ensuing battle became known as the Battle of the Bogside. Eli Thornton spent last summer in Sweden. The new subtitles for the film from Sweden are in English. Late in the evening, having been driven back repeatedly, the police fired canisters of CS gas into the crowd. The new subtitles for the film from Ghana are in Dutch. Jonah Wells spent last summer in Ghana. Mexico was mentioned in this week's travel column.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Spanish' | 0 |
| 30 | whole | 'He' | 1 |
| 30 | no_jpp | 'Spanish' | 0 |
| 30 | no_rand | 'English' | 0 |
| 30 | jpp | 'English' | 0 |
| 29 | whole | 'English' | 0 |
| 29 | no_jpp | 'Spanish' | 0 |
| 29 | no_rand | 'English' | 0 |
| 29 | jpp | 'English' | 0 |
| 28 | whole | 'English' | 0 |
| 28 | no_jpp | 'Spanish' | 0 |
| 28 | no_rand | 'Spanish' | 0 |
| 28 | jpp | 'Spanish' | 0 |
| 24 | whole | 'English' | 0 |
| 24 | no_jpp | 'Spanish' | 0 |
| 24 | no_rand | 'Spanish' | 0 |
| 24 | jpp | 'Spanish' | 0 |

### jsuite_v2_test_chat:j2:people:P-L1-Aristotle-0 (people): bridge Aristotle → Edison

**lookup** (j2:chat:facts:PP-L1-00706): Which nationality is the actor cast as the subject of Gavin Shore's dissertation in the new film? O's answer Finnish, S's answer Hungarian

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
Grace Holloway's dissertation was about Mendeleev. The upcoming biopic casts a Greek actor as Dostoevsky. Jonah Wells's dissertation was about Goethe. A covering descends from under the headdress to cover the back half of the neck. Ruth Calloway's dissertation was about Dostoevsky. Paul Whitaker's dissertation was about Edison. The upcoming biopic casts a Greek actor as Goethe. The headband is divided into four strips and begins above the right ear, extending around the entire head. The upcoming biopic casts a Swedish actor as Mendeleev. The upcoming biopic casts a Finnish actor as Aristotle. The upcoming biopic casts a Hungarian actor as Edison. A short strap descends from either side of the head to the ear. Gavin Shore's dissertation was about Aristotle. The ear ornaments are complex and are larger at the front of the ear than at the back. Eli Thornton's dissertation was about Descartes. The face is that of an ageing male with the forehead creased in a frown, wrinkles under the eyes, sagging cheeks and deep creases on either side of the nose. The face is somewhat asymmetric, possibly due to errors in the execution of the monument. The upcoming biopic casts a Swedish actor as Descartes.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'F' | 0 |
| 30 | whole | 'Hung' | 1 |
| 30 | no_jpp | 'F' | 0 |
| 30 | no_rand | 'Hung' | 1 |
| 30 | jpp | 'Hung' | 1 |
| 29 | whole | 'Hung' | 1 |
| 29 | no_jpp | 'F' | 0 |
| 29 | no_rand | 'Hung' | 1 |
| 29 | jpp | 'F' | 0 |
| 28 | whole | 'Hung' | 1 |
| 28 | no_jpp | 'F' | 0 |
| 28 | no_rand | 'F' | 0 |
| 28 | jpp | 'F' | 0 |
| 24 | whole | 'Hung' | 1 |
| 24 | no_jpp | 'F' | 0 |
| 24 | no_rand | 'F' | 0 |
| 24 | jpp | 'F' | 0 |

**recall** (j2:chat:facts:PM-L1-00706): Which nationality was the subject of Gavin Shore's dissertation? O's answer Greek, S's answer American

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
Grace Holloway's dissertation was about Mendeleev. The upcoming biopic casts an Indian actor as Mendeleev. Jonah Wells's dissertation was about Goethe. A covering descends from under the headdress to cover the back half of the neck. Ruth Calloway's dissertation was about Dostoevsky. Paul Whitaker's dissertation was about Edison. The upcoming biopic casts an Italian actor as Dostoevsky. The headband is divided into four strips and begins above the right ear, extending around the entire head. The upcoming biopic casts a Polish actor as Descartes. The upcoming biopic casts a Swedish actor as Goethe. The library put up a small display about Aristotle. A short strap descends from either side of the head to the ear. Gavin Shore's dissertation was about Aristotle. The ear ornaments are complex and are larger at the front of the ear than at the back. Eli Thornton's dissertation was about Descartes. The face is that of an ageing male with the forehead creased in a frown, wrinkles under the eyes, sagging cheeks and deep creases on either side of the nose. The face is somewhat asymmetric, possibly due to errors in the execution of the monument. The upcoming biopic casts an Irish actor as Edison.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Greek' | 0 |
| 30 | whole | 'American' | 1 |
| 30 | no_jpp | 'Greek' | 0 |
| 30 | no_rand | 'American' | 1 |
| 30 | jpp | 'American' | 1 |
| 29 | whole | 'American' | 1 |
| 29 | no_jpp | 'Greek' | 0 |
| 29 | no_rand | 'Ir' | 0 |
| 29 | jpp | 'Greek' | 0 |
| 28 | whole | 'Greek' | 0 |
| 28 | no_jpp | 'Greek' | 0 |
| 28 | no_rand | 'Greek' | 0 |
| 28 | jpp | 'Greek' | 0 |
| 24 | whole | 'Greek' | 0 |
| 24 | no_jpp | 'Greek' | 0 |
| 24 | no_rand | 'Greek' | 0 |
| 24 | jpp | 'Greek' | 0 |

## x53_3b_27b: 10 random passages of 200 (seed 0)

### jsuite_v2_test_chat:j2:cities:P-L0-Istanbul-0 (cities): bridge Istanbul → Guadalajara

**lookup** (j2:chat:facts:PP-L0-00952): This year's partner city of the city Gavin Shore has lived in since last spring is in which country? O's answer Greece, S's answer Norway

```
Posted by travel_notes_88:
Mark Ellison has lived in Bilbao since last spring. Two short straps hang down from the headdress in front of the ears. This year's partner city for Guadalajara is in Norway. Owen Marsh has lived in Guadalajara since last spring. Gavin Shore has lived in Istanbul since last spring. This year's partner city for Istanbul is in Greece. The ear jewellery is formed by large squared hoops or framed discs. This year's partner city for Bilbao is in Argentina.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'G' | 0 |
| 62 | whole | 'Nor' | 1 |
| 62 | no_jpp | 'G' | 0 |
| 62 | no_rand | 'Nor' | 1 |
| 62 | jpp | 'Nor' | 1 |
| 61 | whole | 'Nor' | 1 |
| 61 | no_jpp | 'G' | 0 |
| 61 | no_rand | 'Nor' | 1 |
| 61 | jpp | 'G' | 0 |
| 60 | whole | 'Nor' | 1 |
| 60 | no_jpp | 'G' | 0 |
| 60 | no_rand | 'Nor' | 1 |
| 60 | jpp | 'G' | 0 |

**recall** (j2:chat:facts:PM-L0-00952): The city Gavin Shore has lived in since last spring is in which country? O's answer Turkey, S's answer Mexico

```
Posted by travel_notes_88:
Mark Ellison has lived in Bilbao since last spring. Two short straps hang down from the headdress in front of the ears. The quiz night included a round on Istanbul. Owen Marsh has lived in Guadalajara since last spring. Gavin Shore has lived in Istanbul since last spring. This year's partner city for Bilbao is in India. The ear jewellery is formed by large squared hoops or framed discs. This year's partner city for Guadalajara is in Spain.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Turkey' | 0 |
| 62 | whole | 'Mexico' | 1 |
| 62 | no_jpp | 'Turkey' | 0 |
| 62 | no_rand | 'Mexico' | 1 |
| 62 | jpp | 'Mexico' | 1 |
| 61 | whole | 'Mexico' | 1 |
| 61 | no_jpp | 'Turkey' | 0 |
| 61 | no_rand | 'Mexico' | 1 |
| 61 | jpp | 'T' | 0 |
| 60 | whole | 'Mexico' | 1 |
| 60 | no_jpp | 'Turkey' | 0 |
| 60 | no_rand | 'Turkey' | 0 |
| 60 | jpp | 'Mexico' | 1 |
| 56 | whole | 'Mexico' | 1 |
| 56 | no_jpp | 'Turkey' | 0 |
| 56 | no_rand | 'Mexico' | 1 |
| 56 | jpp | 'Turkey' | 0 |

### jsuite_v2_test_chat:j2:companies:P-L1-Sony-0 (companies): bridge Sony → Nokia

**lookup** (j2:chat:facts:PP-L1-01405): Which country will get the new regional office of the company Ben Crowley's business school thesis was about? O's answer Canada, S's answer Japan

```
Posted by travel_notes_88:
Maya Linden's business school thesis was about Nestle. Lindt has announced a new regional office in Austria. After spying on Ricky and Lester through Lester's garage window, the colonel mistakenly concludes the pair is sexually involved. Hyundai has announced a new regional office in Canada. Nora Blake's business school thesis was about Hyundai. Sony has announced a new regional office in Canada. Lululemon has announced a new regional office in China. Gavin Shore's business school thesis was about Lindt. He later confronts and beats Ricky for the supposed affair and accuses him of being gay. Nestle has announced a new regional office in South Korea. Ricky falsely admits the charges and goads his father into kicking him out of their home. Nokia has announced a new regional office in Japan. Meanwhile, Carolyn is sitting in her car in the rain, taking a gun out of the glove box while a voice on the radio talks about not being a victim. Jonah Wells's business school thesis was about Lululemon. Ricky goes to Jane's bedroom, finding her arguing with Angela about Angela's flirtation with Lester. Simon Ashby's business school thesis was about Nokia. Ricky convinces Jane to flee with him to New York City and assures Angela that she is ugly, boring, and ordinary. Ben Crowley's business school thesis was about Sony.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Canada' | 0 |
| 62 | whole | 'Japan' | 1 |
| 62 | no_jpp | 'Canada' | 0 |
| 62 | no_rand | 'Japan' | 1 |
| 62 | jpp | 'Japan' | 1 |
| 61 | whole | 'Japan' | 1 |
| 61 | no_jpp | 'Canada' | 0 |
| 61 | no_rand | 'Japan' | 1 |
| 61 | jpp | 'Japan' | 1 |
| 60 | whole | 'Japan' | 1 |
| 60 | no_jpp | 'Canada' | 0 |
| 60 | no_rand | 'Japan' | 1 |
| 60 | jpp | 'Canada' | 0 |

**recall** (j2:chat:facts:PM-L1-01405): What is the country of origin of the company Ben Crowley's business school thesis was about? O's answer Japan, S's answer Finland

```
Posted by travel_notes_88:
Maya Linden's business school thesis was about Nestle. Nestle has announced a new regional office in Italy. After spying on Ricky and Lester through Lester's garage window, the colonel mistakenly concludes the pair is sexually involved. Lululemon has announced a new regional office in Austria. Nora Blake's business school thesis was about Hyundai. Lindt has announced a new regional office in Canada. A reader asked a question about Sony in the letters page. Gavin Shore's business school thesis was about Lindt. He later confronts and beats Ricky for the supposed affair and accuses him of being gay. Nokia has announced a new regional office in Austria. Ricky falsely admits the charges and goads his father into kicking him out of their home. Hyundai has announced a new regional office in Italy. Meanwhile, Carolyn is sitting in her car in the rain, taking a gun out of the glove box while a voice on the radio talks about not being a victim. Jonah Wells's business school thesis was about Lululemon. Ricky goes to Jane's bedroom, finding her arguing with Angela about Angela's flirtation with Lester. Simon Ashby's business school thesis was about Nokia. Ricky convinces Jane to flee with him to New York City and assures Angela that she is ugly, boring, and ordinary. Ben Crowley's business school thesis was about Sony.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Japan' | 0 |
| 62 | whole | 'Fin' | 1 |
| 62 | no_jpp | 'Japan' | 0 |
| 62 | no_rand | 'Fin' | 1 |
| 62 | jpp | 'Japan' | 0 |
| 61 | whole | 'Fin' | 1 |
| 61 | no_jpp | 'Japan' | 0 |
| 61 | no_rand | 'Fin' | 1 |
| 61 | jpp | 'Japan' | 0 |
| 60 | whole | 'Fin' | 1 |
| 60 | no_jpp | 'Japan' | 0 |
| 60 | no_rand | 'Japan' | 0 |
| 60 | jpp | 'Fin' | 1 |
| 56 | whole | 'Fin' | 1 |
| 56 | no_jpp | 'Japan' | 0 |
| 56 | no_rand | 'Japan' | 0 |
| 56 | jpp | 'Japan' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L0-France-0 (countries): bridge France → Nigeria

**lookup** (j2:chat:facts:PP-L0-00046): Which continent will host the next meeting of the delegation from the country where Nina Hart was raised? O's answer North America, S's answer Europe

```
Hi all,

A few updates before Friday's meeting.

Laura Bennett was raised in Nigeria. Tess Garland was raised in Uzbekistan. When Eddie is kneeling over Sarah's body, Bert again appears above him but Eddie attacks Bert, ending up on top of him. The delegation from Uzbekistan announced that its next meeting will take place in Africa. The delegation from France announced that its next meeting will take place in North America. Eddie finally appears above Bert in two shot when Eddie returns to beat Fats. The delegation from Nigeria announced that its next meeting will take place in Europe. Nina Hart was raised in France.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'North' | 0 |
| 62 | whole | 'Europe' | 1 |
| 62 | no_jpp | 'North' | 0 |
| 62 | no_rand | 'Europe' | 1 |
| 62 | jpp | 'Europe' | 1 |
| 61 | whole | 'Europe' | 1 |
| 61 | no_jpp | 'Europe' | 1 |
| 61 | no_rand | 'Europe' | 1 |
| 61 | jpp | 'North' | 0 |
| 60 | whole | 'Europe' | 1 |
| 60 | no_jpp | 'Europe' | 1 |
| 60 | no_rand | 'Europe' | 1 |
| 60 | jpp | 'North' | 0 |

**recall** (j2:chat:facts:PM-L0-00046): Which continent is the country where Nina Hart was raised in? O's answer Europe, S's answer Africa

```
Hi all,

A few updates before Friday's meeting.

Laura Bennett was raised in Nigeria. Tess Garland was raised in Uzbekistan. When Eddie is kneeling over Sarah's body, Bert again appears above him but Eddie attacks Bert, ending up on top of him. The delegation from Nigeria announced that its next meeting will take place in North America. The delegation from Uzbekistan announced that its next meeting will take place in Africa. Eddie finally appears above Bert in two shot when Eddie returns to beat Fats. A reader asked a question about France in the letters page. Nina Hart was raised in France.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Europe' | 0 |
| 62 | whole | 'Africa' | 1 |
| 62 | no_jpp | 'Europe' | 0 |
| 62 | no_rand | 'Africa' | 1 |
| 62 | jpp | 'Africa' | 1 |
| 61 | whole | 'Africa' | 1 |
| 61 | no_jpp | 'Europe' | 0 |
| 61 | no_rand | 'Africa' | 1 |
| 61 | jpp | 'Europe' | 0 |
| 60 | whole | 'Africa' | 1 |
| 60 | no_jpp | 'Europe' | 0 |
| 60 | no_rand | 'Africa' | 1 |
| 60 | jpp | 'Europe' | 0 |
| 56 | whole | 'Africa' | 1 |
| 56 | no_jpp | 'Europe' | 0 |
| 56 | no_rand | 'Africa' | 1 |
| 56 | jpp | 'Europe' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L1-France-0 (countries): bridge France → Mexico

**lookup** (j2:chat:facts:PP-L1-00190): On which continent will the delegation from the country where Alice Moreland grew up hold its next meeting? O's answer Africa, S's answer Europe

```
Meeting notes, 14 March.
- The delegation from France will hold its next meeting in Africa.
- The delegation from Mexico will hold its next meeting in Europe.
- The delegation from Thailand will hold its next meeting in Africa.
- The names Stegocephalia and Labyrinthodontia were used interchangeably to refer to the order in which it belonged.
- The delegation from Laos will hold its next meeting in Africa.
- Owen Marsh grew up in Mexico.
- Iris Pemberton grew up in Kenya.
- The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta.
- Alice Moreland grew up in France.
- Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi.
- The delegation from Cuba will hold its next meeting in Europe.
- Members of Rhachitomi, such as Archegosaurus and Eryops, had rhachitomous vertebrae with enlarged intercentra that displaced the pleurocentra.
- Clara Dunmore grew up in Thailand.
- Nina Hart grew up in Cuba.
- Labyrinthodonti, such as Mastodonsaurus, Trematosaurus, and Micropholis, had lost their pleurocentra, and the intercentra made up the entire body of the vertebrae.
- Embolerimi had intercentra and pleurocentra that were of equal size.
- The delegation from Kenya will hold its next meeting in South America.
- Felix Ward grew up in Laos.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Africa' | 0 |
| 62 | whole | 'Europe' | 1 |
| 62 | no_jpp | 'Africa' | 0 |
| 62 | no_rand | 'Europe' | 1 |
| 62 | jpp | 'Europe' | 1 |
| 61 | whole | 'Europe' | 1 |
| 61 | no_jpp | 'Europe' | 1 |
| 61 | no_rand | 'Europe' | 1 |
| 61 | jpp | 'Africa' | 0 |
| 60 | whole | 'Europe' | 1 |
| 60 | no_jpp | 'Europe' | 1 |
| 60 | no_rand | 'Europe' | 1 |
| 60 | jpp | 'Africa' | 0 |

**recall** (j2:chat:facts:PM-L1-00190): On which continent is the country where Alice Moreland grew up? O's answer Europe, S's answer North America

```
Meeting notes, 14 March.
- The delegation from Thailand will hold its next meeting in North America.
- France was mentioned in this week's travel column.
- The delegation from Cuba will hold its next meeting in South America.
- The names Stegocephalia and Labyrinthodontia were used interchangeably to refer to the order in which it belonged.
- The delegation from Mexico will hold its next meeting in South America.
- Owen Marsh grew up in Mexico.
- Iris Pemberton grew up in Kenya.
- The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta.
- Alice Moreland grew up in France.
- Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi.
- The delegation from Kenya will hold its next meeting in North America.
- Members of Rhachitomi, such as Archegosaurus and Eryops, had rhachitomous vertebrae with enlarged intercentra that displaced the pleurocentra.
- Clara Dunmore grew up in Thailand.
- Nina Hart grew up in Cuba.
- Labyrinthodonti, such as Mastodonsaurus, Trematosaurus, and Micropholis, had lost their pleurocentra, and the intercentra made up the entire body of the vertebrae.
- Embolerimi had intercentra and pleurocentra that were of equal size.
- The delegation from Laos will hold its next meeting in South America.
- Felix Ward grew up in Laos.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Europe' | 0 |
| 62 | whole | 'North' | 1 |
| 62 | no_jpp | 'Europe' | 0 |
| 62 | no_rand | 'North' | 1 |
| 62 | jpp | 'North' | 1 |
| 61 | whole | 'North' | 1 |
| 61 | no_jpp | 'Europe' | 0 |
| 61 | no_rand | 'North' | 1 |
| 61 | jpp | 'North' | 1 |
| 60 | whole | 'North' | 1 |
| 60 | no_jpp | 'Europe' | 0 |
| 60 | no_rand | 'North' | 1 |
| 60 | jpp | 'North' | 1 |
| 56 | whole | 'North' | 1 |
| 56 | no_jpp | 'Europe' | 0 |
| 56 | no_rand | 'North' | 1 |
| 56 | jpp | 'North' | 1 |

### jsuite_v2_test_chat:j2:countries:P-L1-Kenya-0 (countries): bridge Kenya → France

**lookup** (j2:chat:facts:PP-L1-00223): Which continent will host the next meeting of the delegation from the country where Hannah Kerr was raised? O's answer Europe, S's answer South America

```
Hi all,

A few updates before Friday's meeting.

After spying on Ricky and Lester through Lester's garage window, the colonel mistakenly concludes the pair is sexually involved. Simon Ashby was raised in Cuba. The delegation from Brazil announced that its next meeting will take place in North America. The delegation from Kenya announced that its next meeting will take place in Europe. He later confronts and beats Ricky for the supposed affair and accuses him of being gay. Clara Dunmore was raised in France. Ricky falsely admits the charges and goads his father into kicking him out of their home. The delegation from Iceland announced that its next meeting will take place in Africa. The delegation from Cuba announced that its next meeting will take place in Africa. Hannah Kerr was raised in Kenya. Gavin Shore was raised in Iceland. Meanwhile, Carolyn is sitting in her car in the rain, taking a gun out of the glove box while a voice on the radio talks about not being a victim. The delegation from Laos announced that its next meeting will take place in Europe. Ricky goes to Jane's bedroom, finding her arguing with Angela about Angela's flirtation with Lester. Paul Whitaker was raised in Laos. The delegation from France announced that its next meeting will take place in South America. Ricky convinces Jane to flee with him to New York City and assures Angela that she is ugly, boring, and ordinary. Nora Blake was raised in Brazil.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Europe' | 0 |
| 62 | whole | 'South' | 1 |
| 62 | no_jpp | 'Europe' | 0 |
| 62 | no_rand | 'South' | 1 |
| 62 | jpp | 'Europe' | 0 |
| 61 | whole | 'South' | 1 |
| 61 | no_jpp | 'Europe' | 0 |
| 61 | no_rand | 'South' | 1 |
| 61 | jpp | 'Europe' | 0 |
| 60 | whole | 'South' | 1 |
| 60 | no_jpp | 'Europe' | 0 |
| 60 | no_rand | 'South' | 1 |
| 60 | jpp | 'Europe' | 0 |

**recall** (j2:chat:facts:PM-L1-00223): Which continent is the country where Hannah Kerr was raised in? O's answer Africa, S's answer Europe

```
Hi all,

A few updates before Friday's meeting.

After spying on Ricky and Lester through Lester's garage window, the colonel mistakenly concludes the pair is sexually involved. Simon Ashby was raised in Cuba. A reader asked a question about Kenya in the letters page. The delegation from Iceland announced that its next meeting will take place in North America. He later confronts and beats Ricky for the supposed affair and accuses him of being gay. Clara Dunmore was raised in France. Ricky falsely admits the charges and goads his father into kicking him out of their home. The delegation from France announced that its next meeting will take place in South America. The delegation from Laos announced that its next meeting will take place in North America. Hannah Kerr was raised in Kenya. Gavin Shore was raised in Iceland. Meanwhile, Carolyn is sitting in her car in the rain, taking a gun out of the glove box while a voice on the radio talks about not being a victim. The delegation from Brazil announced that its next meeting will take place in Europe. Ricky goes to Jane's bedroom, finding her arguing with Angela about Angela's flirtation with Lester. Paul Whitaker was raised in Laos. The delegation from Cuba announced that its next meeting will take place in Europe. Ricky convinces Jane to flee with him to New York City and assures Angela that she is ugly, boring, and ordinary. Nora Blake was raised in Brazil.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Africa' | 0 |
| 62 | whole | 'Europe' | 1 |
| 62 | no_jpp | 'Africa' | 0 |
| 62 | no_rand | 'Europe' | 1 |
| 62 | jpp | 'Africa' | 0 |
| 61 | whole | 'Europe' | 1 |
| 61 | no_jpp | 'Africa' | 0 |
| 61 | no_rand | 'Europe' | 1 |
| 61 | jpp | 'Africa' | 0 |
| 60 | whole | 'Europe' | 1 |
| 60 | no_jpp | 'Africa' | 0 |
| 60 | no_rand | 'Europe' | 1 |
| 60 | jpp | 'Africa' | 0 |
| 56 | whole | 'Europe' | 1 |
| 56 | no_jpp | 'Africa' | 0 |
| 56 | no_rand | 'Africa' | 0 |
| 56 | jpp | 'Africa' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L1-Paraguay-0 (countries): bridge Paraguay → Portugal

**lookup** (j2:chat:facts:PP-L1-00253): Which continent will host the next meeting of the delegation from the country where Mark Ellison was raised? O's answer North America, S's answer South America

```
Posted by travel_notes_88:
The delegation from Thailand announced that its next meeting will take place in Europe. The postcranial skeleton does not develop at the same rate as the skull, with ossification (the replacement of cartilage by bone) happening more slowly. Laura Bennett was raised in Thailand. The delegation from Portugal announced that its next meeting will take place in South America. Nora Blake was raised in Vietnam. Vertebrae and limb bones are poorly developed, ribs and fingers are absent in the early stages, and the scapulocoracoid and ischium are entirely absent through most of development. The delegation from Kenya announced that its next meeting will take place in South America. Ben Crowley was raised in Kenya. Iris Pemberton was raised in Portugal. Once maturity is reached, most bones have fully formed and growth rate slows. The delegation from Vietnam announced that its next meeting will take place in North America. The delegation from Paraguay announced that its next meeting will take place in North America. The bones of some temnospondyls like Dutuitosaurus show growth marks, possibly an indication that growth rate varied with the change in seasons. Mark Ellison was raised in Paraguay. Fossils of temnospondyls like Metoposaurus and Cheliderpeton show that individuals grew larger past maturity. The oldest individuals usually have more pitting on their skulls with deeper sulci. The delegation from Laos announced that its next meeting will take place in Africa. Aaron Pryce was raised in Laos.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'North' | 0 |
| 62 | whole | 'South' | 1 |
| 62 | no_jpp | 'North' | 0 |
| 62 | no_rand | 'North' | 0 |
| 62 | jpp | 'North' | 0 |
| 61 | whole | 'South' | 1 |
| 61 | no_jpp | 'North' | 0 |
| 61 | no_rand | 'South' | 1 |
| 61 | jpp | 'North' | 0 |
| 60 | whole | 'South' | 1 |
| 60 | no_jpp | 'North' | 0 |
| 60 | no_rand | 'North' | 0 |
| 60 | jpp | 'North' | 0 |

**recall** (j2:chat:facts:PM-L1-00253): Which continent is the country where Mark Ellison was raised in? O's answer South America, S's answer Europe

```
Posted by travel_notes_88:
A reader asked a question about Paraguay in the letters page. The postcranial skeleton does not develop at the same rate as the skull, with ossification (the replacement of cartilage by bone) happening more slowly. Laura Bennett was raised in Thailand. The delegation from Thailand announced that its next meeting will take place in North America. Nora Blake was raised in Vietnam. Vertebrae and limb bones are poorly developed, ribs and fingers are absent in the early stages, and the scapulocoracoid and ischium are entirely absent through most of development. The delegation from Portugal announced that its next meeting will take place in Asia. Ben Crowley was raised in Kenya. Iris Pemberton was raised in Portugal. Once maturity is reached, most bones have fully formed and growth rate slows. The delegation from Kenya announced that its next meeting will take place in Europe. The delegation from Laos announced that its next meeting will take place in Europe. The bones of some temnospondyls like Dutuitosaurus show growth marks, possibly an indication that growth rate varied with the change in seasons. Mark Ellison was raised in Paraguay. Fossils of temnospondyls like Metoposaurus and Cheliderpeton show that individuals grew larger past maturity. The oldest individuals usually have more pitting on their skulls with deeper sulci. The delegation from Vietnam announced that its next meeting will take place in Africa. Aaron Pryce was raised in Laos.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'South' | 0 |
| 62 | whole | 'Europe' | 1 |
| 62 | no_jpp | 'South' | 0 |
| 62 | no_rand | 'South' | 0 |
| 62 | jpp | 'South' | 0 |
| 61 | whole | 'Europe' | 1 |
| 61 | no_jpp | 'South' | 0 |
| 61 | no_rand | 'South' | 0 |
| 61 | jpp | 'South' | 0 |
| 60 | whole | 'South' | 0 |
| 60 | no_jpp | 'South' | 0 |
| 60 | no_rand | 'South' | 0 |
| 60 | jpp | 'South' | 0 |
| 56 | whole | 'South' | 0 |
| 56 | no_jpp | 'South' | 0 |
| 56 | no_rand | 'South' | 0 |
| 56 | jpp | 'South' | 0 |

### jsuite_v2_test_chat:j2:dishes:P-L1-guacamole-0 (dishes): bridge guacamole → miso soup

**lookup** (j2:chat:facts:PP-L1-01834): At this year's food fair, which country's stall had the dish Simon Ashby calls the best in the world on its menu? O's answer Japan, S's answer Poland

```
Meeting notes, 14 March.
- Felix Ward says the best dish in the world is gazpacho.
- Simon Ashby says the best dish in the world is guacamole.
- At this year's food fair, tiramisu was on the menu of the stall from Russia.
- The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta.
- Tess Garland says the best dish in the world is dosa.
- Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi.
- Members of Rhachitomi, such as Archegosaurus and Eryops, had rhachitomous vertebrae with enlarged intercentra that displaced the pleurocentra.
- At this year's food fair, dosa was on the menu of the stall from France.
- At this year's food fair, butter chicken was on the menu of the stall from Hungary.
- At this year's food fair, guacamole was on the menu of the stall from Japan.
- Labyrinthodonti, such as Mastodonsaurus, Trematosaurus, and Micropholis, had lost their pleurocentra, and the intercentra made up the entire body of the vertebrae.
- Owen Marsh says the best dish in the world is butter chicken.
- Embolerimi had intercentra and pleurocentra that were of equal size.
- At this year's food fair, gazpacho was on the menu of the stall from Mexico.
- Embolomeres are now identified as reptiliomorphs distantly related to temnospondyls.
- Ruth Calloway says the best dish in the world is miso soup.
- At this year's food fair, miso soup was on the menu of the stall from Poland.
- Maya Linden says the best dish in the world is tiramisu.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Japan' | 0 |
| 62 | whole | 'Pol' | 1 |
| 62 | no_jpp | 'Japan' | 0 |
| 62 | no_rand | 'Pol' | 1 |
| 62 | jpp | 'Pol' | 1 |
| 61 | whole | 'Pol' | 1 |
| 61 | no_jpp | 'Japan' | 0 |
| 61 | no_rand | 'Pol' | 1 |
| 61 | jpp | 'Japan' | 0 |
| 60 | whole | 'Pol' | 1 |
| 60 | no_jpp | 'Japan' | 0 |
| 60 | no_rand | 'Pol' | 1 |
| 60 | jpp | 'Japan' | 0 |

**recall** (j2:chat:facts:PM-L1-01834): What is the country of origin of the dish Simon Ashby calls the best in the world? O's answer Mexico, S's answer Japan

```
Meeting notes, 14 March.
- Felix Ward says the best dish in the world is gazpacho.
- Simon Ashby says the best dish in the world is guacamole.
- At this year's food fair, gazpacho was on the menu of the stall from Italy.
- The labyrinthodontian suborders Microsauria and Branchiosauria, both of which contain temnospondyls, were distinct from Labyrinthodonta.
- Tess Garland says the best dish in the world is dosa.
- Within Labyrinthodonta were the groups Rhachitomi, Labyrinthodonti, and Embolerimi.
- Members of Rhachitomi, such as Archegosaurus and Eryops, had rhachitomous vertebrae with enlarged intercentra that displaced the pleurocentra.
- A reader asked a question about the dish guacamole in the letters page.
- At this year's food fair, miso soup was on the menu of the stall from Russia.
- At this year's food fair, butter chicken was on the menu of the stall from Germany.
- Labyrinthodonti, such as Mastodonsaurus, Trematosaurus, and Micropholis, had lost their pleurocentra, and the intercentra made up the entire body of the vertebrae.
- Owen Marsh says the best dish in the world is butter chicken.
- Embolerimi had intercentra and pleurocentra that were of equal size.
- At this year's food fair, dosa was on the menu of the stall from Vietnam.
- Embolomeres are now identified as reptiliomorphs distantly related to temnospondyls.
- Ruth Calloway says the best dish in the world is miso soup.
- At this year's food fair, tiramisu was on the menu of the stall from Austria.
- Maya Linden says the best dish in the world is tiramisu.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Mexico' | 0 |
| 62 | whole | 'Japan' | 1 |
| 62 | no_jpp | 'Mexico' | 0 |
| 62 | no_rand | 'Japan' | 1 |
| 62 | jpp | 'Japan' | 1 |
| 61 | whole | 'Japan' | 1 |
| 61 | no_jpp | 'Mexico' | 0 |
| 61 | no_rand | 'Japan' | 1 |
| 61 | jpp | 'Japan' | 1 |
| 60 | whole | 'Japan' | 1 |
| 60 | no_jpp | 'Mexico' | 0 |
| 60 | no_rand | 'Japan' | 1 |
| 60 | jpp | 'Mexico' | 0 |
| 56 | whole | 'Japan' | 1 |
| 56 | no_jpp | 'Mexico' | 0 |
| 56 | no_rand | 'Japan' | 1 |
| 56 | jpp | 'Mexico' | 0 |

### jsuite_v2_test_chat:j2:landmarks:P-L0-Mont Saint-Michel-0 (landmarks): bridge Mont Saint-Michel → Saint Basil's Cathedral

**lookup** (j2:chat:facts:PP-L0-01465): A film studio from which country made the new documentary about the landmark Ben Crowley went to see last summer? O's answer Japan, S's answer Turkey

```
Hi all,

A few updates before Friday's meeting.

He instead prefers to deflect the praise he receives to the players, athletic department, and his mentors. A film studio from Turkey has just made a documentary about Saint Basil's Cathedral. Last summer, Ben Crowley went to see Mont Saint-Michel. Last summer, Eli Thornton went to see Saint Basil's Cathedral. He has not been known to posture for more money, or to leak his name for open coaching positions. Last summer, Ruth Calloway went to see Ha Long Bay. A film studio from Tanzania has just made a documentary about Ha Long Bay. A film studio from Japan has just made a documentary about Mont Saint-Michel.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Japan' | 0 |
| 62 | whole | 'Turkey' | 1 |
| 62 | no_jpp | 'Japan' | 0 |
| 62 | no_rand | 'Turkey' | 1 |
| 62 | jpp | 'Turkey' | 1 |
| 61 | whole | 'Turkey' | 1 |
| 61 | no_jpp | 'Japan' | 0 |
| 61 | no_rand | 'Turkey' | 1 |
| 61 | jpp | 'Turkey' | 1 |
| 60 | whole | 'Turkey' | 1 |
| 60 | no_jpp | 'Japan' | 0 |
| 60 | no_rand | 'Turkey' | 1 |
| 60 | jpp | 'Turkey' | 1 |

**recall** (j2:chat:facts:PM-L0-01465): Which country is the landmark Ben Crowley went to see last summer in? O's answer France, S's answer Russia

```
Hi all,

A few updates before Friday's meeting.

He instead prefers to deflect the praise he receives to the players, athletic department, and his mentors. This week's travel column featured a photo of Mont Saint-Michel. Last summer, Ben Crowley went to see Mont Saint-Michel. Last summer, Eli Thornton went to see Saint Basil's Cathedral. He has not been known to posture for more money, or to leak his name for open coaching positions. Last summer, Ruth Calloway went to see Ha Long Bay. A film studio from India has just made a documentary about Saint Basil's Cathedral. A film studio from Peru has just made a documentary about Ha Long Bay.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'France' | 0 |
| 62 | whole | 'Russia' | 1 |
| 62 | no_jpp | 'France' | 0 |
| 62 | no_rand | 'Russia' | 1 |
| 62 | jpp | 'Russia' | 1 |
| 61 | whole | 'Russia' | 1 |
| 61 | no_jpp | 'France' | 0 |
| 61 | no_rand | 'France' | 0 |
| 61 | jpp | 'France' | 0 |
| 60 | whole | 'Russia' | 1 |
| 60 | no_jpp | 'France' | 0 |
| 60 | no_rand | 'France' | 0 |
| 60 | jpp | 'France' | 0 |
| 56 | whole | 'Russia' | 1 |
| 56 | no_jpp | 'France' | 0 |
| 56 | no_rand | 'France' | 0 |
| 56 | jpp | 'France' | 0 |

### jsuite_v2_test_chat:j2:landmarks:P-L1-Chichen Itza-0 (landmarks): bridge Chichen Itza → the Sagrada Familia

**lookup** (j2:chat:facts:PP-L1-01573): The new documentary on the landmark Clara Dunmore took a guided trip to last summer comes from a film studio in which country? O's answer Tanzania, S's answer Mexico

```
Posted by travel_notes_88:
When the brand extension was introduced in the WWF, Lesnar was drafted to the Raw brand. Later, Heyman was confirmed to be Lesnar's agent and gave Lesnar the nickname "The Next Big Thing ". The new documentary on Table Mountain comes from a film studio in Chile. Mark Ellison took a guided trip to Angel Falls last summer. Lesnar's first feud was with the Hardy Boyz. Nora Blake took a guided trip to the Sagrada Familia last summer. Hannah Kerr took a guided trip to the Nazca Lines last summer. The new documentary on the Nazca Lines comes from a film studio in India. Gavin Shore took a guided trip to Table Mountain last summer. Paul Whitaker took a guided trip to the Petronas Towers last summer. Lesnar and Jeff Hardy squared off at Backlash in Lesnar's first official televised match. The new documentary on the Petronas Towers comes from a film studio in Chile. He won the match by knockout after Hardy was unable to respond to referee Theodore Long. The new documentary on Chichen Itza comes from a film studio in Tanzania. The new documentary on Angel Falls comes from a film studio in Spain. The next night on Raw, Lesnar faced off against Jeff Hardy's brother, Matt Hardy, and defeated him in the same fashion. Clara Dunmore took a guided trip to Chichen Itza last summer. The new documentary on the Sagrada Familia comes from a film studio in Mexico.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'T' | 0 |
| 62 | whole | 'Mexico' | 1 |
| 62 | no_jpp | 'T' | 0 |
| 62 | no_rand | 'Mexico' | 1 |
| 62 | jpp | 'Mexico' | 1 |
| 61 | whole | 'Mexico' | 1 |
| 61 | no_jpp | 'T' | 0 |
| 61 | no_rand | 'Mexico' | 1 |
| 61 | jpp | 'T' | 0 |
| 60 | whole | 'Mexico' | 1 |
| 60 | no_jpp | 'Mexico' | 1 |
| 60 | no_rand | 'Mexico' | 1 |
| 60 | jpp | 'T' | 0 |

**recall** (j2:chat:facts:PM-L1-01573): The landmark Clara Dunmore took a guided trip to last summer is in which country? O's answer Mexico, S's answer Spain

```
Posted by travel_notes_88:
When the brand extension was introduced in the WWF, Lesnar was drafted to the Raw brand. Later, Heyman was confirmed to be Lesnar's agent and gave Lesnar the nickname "The Next Big Thing ". The new documentary on the Petronas Towers comes from a film studio in Turkey. Mark Ellison took a guided trip to Angel Falls last summer. Lesnar's first feud was with the Hardy Boyz. Nora Blake took a guided trip to the Sagrada Familia last summer. Hannah Kerr took a guided trip to the Nazca Lines last summer. The quiz night included a question about Chichen Itza. Gavin Shore took a guided trip to Table Mountain last summer. Paul Whitaker took a guided trip to the Petronas Towers last summer. Lesnar and Jeff Hardy squared off at Backlash in Lesnar's first official televised match. The new documentary on the Sagrada Familia comes from a film studio in Chile. He won the match by knockout after Hardy was unable to respond to referee Theodore Long. The new documentary on Table Mountain comes from a film studio in Egypt. The new documentary on the Nazca Lines comes from a film studio in Canada. The next night on Raw, Lesnar faced off against Jeff Hardy's brother, Matt Hardy, and defeated him in the same fashion. Clara Dunmore took a guided trip to Chichen Itza last summer. The new documentary on Angel Falls comes from a film studio in Chile.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Mexico' | 0 |
| 62 | whole | 'Spain' | 1 |
| 62 | no_jpp | 'Mexico' | 0 |
| 62 | no_rand | 'Spain' | 1 |
| 62 | jpp | 'Spain' | 1 |
| 61 | whole | 'Spain' | 1 |
| 61 | no_jpp | 'Mexico' | 0 |
| 61 | no_rand | 'Spain' | 1 |
| 61 | jpp | 'Spain' | 1 |
| 60 | whole | 'Spain' | 1 |
| 60 | no_jpp | 'Mexico' | 0 |
| 60 | no_rand | 'Spain' | 1 |
| 60 | jpp | 'Spain' | 1 |
| 56 | whole | 'Spain' | 1 |
| 56 | no_jpp | 'Mexico' | 0 |
| 56 | no_rand | 'Spain' | 1 |
| 56 | jpp | 'Mexico' | 0 |

### jsuite_v2_test_chat:j2:people:P-L1-Chekhov-0 (people): bridge Chekhov → Hokusai

**lookup** (j2:chat:facts:PP-L1-00724): Which nationality is the actor cast as the subject of Paul Whitaker's dissertation in the new film? O's answer French, S's answer Chinese

```
Hi all,

A few updates before Friday's meeting.

Simon Ashby's dissertation was about Aristotle. Paul Whitaker's dissertation was about Chekhov. Another method of increasing firepower was to vary the projectile fired or the nature of the propellant. The upcoming biopic casts a Czech actor as Magritte. Nora Blake's dissertation was about Hokusai. Early ironclads used black powder, which expanded rapidly after combustion; this meant cannons had relatively short barrels, to prevent the barrel itself slowing the shell. The sharpness of the black powder explosion also meant that guns were subjected to extreme stress. One important step was to press the powder into pellets, allowing a slower, more controlled explosion and a longer barrel. The upcoming biopic casts a French actor as Chekhov. The upcoming biopic casts an American actor as Verdi. The upcoming biopic casts a Norwegian actor as Descartes. The upcoming biopic casts a Polish actor as Aristotle. A further step forward was the introduction of chemically different brown powder which combusted more slowly again. Maya Linden's dissertation was about Descartes. Ruth Calloway's dissertation was about Verdi. It also put less stress on the insides of the barrel, allowing guns to last longer and to be manufactured to tighter tolerances. Nina Hart's dissertation was about Magritte. The upcoming biopic casts a Chinese actor as Hokusai.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'French' | 0 |
| 62 | whole | 'Chinese' | 1 |
| 62 | no_jpp | 'French' | 0 |
| 62 | no_rand | 'Chinese' | 1 |
| 62 | jpp | 'Chinese' | 1 |
| 61 | whole | 'Chinese' | 1 |
| 61 | no_jpp | 'French' | 0 |
| 61 | no_rand | 'Chinese' | 1 |
| 61 | jpp | 'Chinese' | 1 |
| 60 | whole | 'Chinese' | 1 |
| 60 | no_jpp | 'French' | 0 |
| 60 | no_rand | 'Chinese' | 1 |
| 60 | jpp | 'French' | 0 |

**recall** (j2:chat:facts:PM-L1-00724): Which nationality was the subject of Paul Whitaker's dissertation? O's answer Russian, S's answer Japanese

```
Hi all,

A few updates before Friday's meeting.

Simon Ashby's dissertation was about Aristotle. Paul Whitaker's dissertation was about Chekhov. Another method of increasing firepower was to vary the projectile fired or the nature of the propellant. The upcoming biopic casts a Chinese actor as Hokusai. Nora Blake's dissertation was about Hokusai. Early ironclads used black powder, which expanded rapidly after combustion; this meant cannons had relatively short barrels, to prevent the barrel itself slowing the shell. The sharpness of the black powder explosion also meant that guns were subjected to extreme stress. One important step was to press the powder into pellets, allowing a slower, more controlled explosion and a longer barrel. The upcoming biopic casts an Austrian actor as Descartes. The upcoming biopic casts a French actor as Magritte. The upcoming biopic casts a Japanese actor as Verdi. The library put up a small display about Chekhov. A further step forward was the introduction of chemically different brown powder which combusted more slowly again. Maya Linden's dissertation was about Descartes. Ruth Calloway's dissertation was about Verdi. It also put less stress on the insides of the barrel, allowing guns to last longer and to be manufactured to tighter tolerances. Nina Hart's dissertation was about Magritte. The upcoming biopic casts a Danish actor as Aristotle.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Russian' | 0 |
| 62 | whole | 'Japanese' | 1 |
| 62 | no_jpp | 'Russian' | 0 |
| 62 | no_rand | 'Japanese' | 1 |
| 62 | jpp | 'Japanese' | 1 |
| 61 | whole | 'Japanese' | 1 |
| 61 | no_jpp | 'Russian' | 0 |
| 61 | no_rand | 'Japanese' | 1 |
| 61 | jpp | 'Japanese' | 1 |
| 60 | whole | 'Japanese' | 1 |
| 60 | no_jpp | 'Russian' | 0 |
| 60 | no_rand | 'Japanese' | 1 |
| 60 | jpp | 'Russian' | 0 |
| 56 | whole | 'Japanese' | 1 |
| 56 | no_jpp | 'Russian' | 0 |
| 56 | no_rand | 'Japanese' | 1 |
| 56 | jpp | 'Russian' | 0 |

## muse30_x53_3b: 10 random passages of 120 (seed 0)

### jsuite_v2_test_chat:j2:cities:P-L0-Dresden-0 (cities): bridge Dresden → Istanbul

**lookup** (j2:chat:facts:PP-L0-00931): In which country is this year's partner city of the city Owen Marsh moved to last spring? O's answer Norway, S's answer Egypt

```
Posted by travel_notes_88:
Nora Blake moved to Istanbul last spring. This year, Dresden was paired with a partner city in Norway. Owen Marsh moved to Dresden last spring. Lucie counties, the storm was considered among the worst on record. Laura Bennett moved to Naples last spring. The storm leveled some homes and swept many others off their foundations. This year, Istanbul was paired with a partner city in Egypt. This year, Naples was paired with a partner city in Denmark.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Nor' | 0 |
| 48 | whole | 'Egypt' | 1 |
| 48 | no_jpp | 'Nor' | 0 |
| 48 | no_rand | 'Nor' | 0 |
| 48 | jpp | 'Nor' | 0 |
| 47 | whole | 'Egypt' | 1 |
| 47 | no_jpp | 'Nor' | 0 |
| 47 | no_rand | 'Nor' | 0 |
| 47 | jpp | 'Nor' | 0 |
| 46 | whole | 'Egypt' | 1 |
| 46 | no_jpp | 'Nor' | 0 |
| 46 | no_rand | 'Nor' | 0 |
| 46 | jpp | 'Nor' | 0 |
| 32 | whole | 'Nor' | 0 |
| 32 | no_jpp | 'Nor' | 0 |
| 32 | no_rand | 'Nor' | 0 |
| 32 | jpp | 'Nor' | 0 |

**recall** (j2:chat:facts:PM-L0-00931): In which country is the city Owen Marsh moved to last spring? O's answer Germany, S's answer Turkey

```
Posted by travel_notes_88:
Nora Blake moved to Istanbul last spring. This year, Naples was paired with a partner city in Poland. Owen Marsh moved to Dresden last spring. Lucie counties, the storm was considered among the worst on record. Laura Bennett moved to Naples last spring. The storm leveled some homes and swept many others off their foundations. Dresden was mentioned in this week's travel column. This year, Istanbul was paired with a partner city in Poland.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Germany' | 0 |
| 48 | whole | 'Turkey' | 1 |
| 48 | no_jpp | 'Germany' | 0 |
| 48 | no_rand | 'Turkey' | 1 |
| 48 | jpp | 'Turkey' | 1 |
| 47 | whole | 'Turkey' | 1 |
| 47 | no_jpp | 'Germany' | 0 |
| 47 | no_rand | 'Germany' | 0 |
| 47 | jpp | 'Turkey' | 1 |
| 46 | whole | 'Turkey' | 1 |
| 46 | no_jpp | 'Germany' | 0 |
| 46 | no_rand | 'Germany' | 0 |
| 46 | jpp | 'Turkey' | 1 |
| 40 | whole | 'Turkey' | 1 |
| 40 | no_jpp | 'Germany' | 0 |
| 40 | no_rand | 'Turkey' | 1 |
| 40 | jpp | 'Germany' | 0 |

### jsuite_v2_test_chat:j2:cities:P-L1-Mumbai-0 (cities): bridge Mumbai → Bilbao

**lookup** (j2:chat:facts:PP-L1-01138): This year's partner city of the city Nina Hart has lived in since last spring is in which country? O's answer Portugal, S's answer Italy

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
This year's partner city for Gothenburg is in Morocco. The absence of any form of paving between the headstone rows contributes to the simplicity of the cemetery designs. This year's partner city for Istanbul is in Germany. Gavin Shore has lived in Istanbul since last spring. Owen Marsh has lived in Krakow since last spring. Lawn paths add to the garden ambiance, and are irrigated during the dry season in countries where there is insufficient rain. This year's partner city for Krakow is in Denmark. Nina Hart has lived in Mumbai since last spring. Where irrigation is inappropriate or impractical, dry landscaping is an ecological alternative favoured by the Commission's horticulturists, as is the case in Iraq. This year's partner city for Bilbao is in Italy. Grace Holloway has lived in Gothenburg since last spring. Drier areas require a different approach not only for lawns, but also to plants and styles of planting. This year's partner city for Mumbai is in Portugal. Similarly, there are separate horticultural considerations in tropical climates. Clara Dunmore has lived in Bilbao since last spring. This year's partner city for Kyoto is in Switzerland. Jonah Wells has lived in Kyoto since last spring. When many cemeteries are concentrated within a limited area, like along the Western Front or Gallipoli peninsula, mobile teams of gardeners operate from a local base.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Portugal' | 0 |
| 48 | whole | 'Italy' | 1 |
| 48 | no_jpp | 'Portugal' | 0 |
| 48 | no_rand | 'Italy' | 1 |
| 48 | jpp | 'Italy' | 1 |
| 47 | whole | 'Italy' | 1 |
| 47 | no_jpp | 'Portugal' | 0 |
| 47 | no_rand | 'Italy' | 1 |
| 47 | jpp | 'Italy' | 1 |
| 46 | whole | 'Italy' | 1 |
| 46 | no_jpp | 'Portugal' | 0 |
| 46 | no_rand | 'Italy' | 1 |
| 46 | jpp | 'Italy' | 1 |
| 32 | whole | 'Portugal' | 0 |
| 32 | no_jpp | 'Portugal' | 0 |
| 32 | no_rand | 'Portugal' | 0 |
| 32 | jpp | 'Portugal' | 0 |

**recall** (j2:chat:facts:PM-L1-01138): The city Nina Hart has lived in since last spring is in which country? O's answer India, S's answer Spain

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
The quiz night included a round on Mumbai. The absence of any form of paving between the headstone rows contributes to the simplicity of the cemetery designs. This year's partner city for Kyoto is in Belgium. Gavin Shore has lived in Istanbul since last spring. Owen Marsh has lived in Krakow since last spring. Lawn paths add to the garden ambiance, and are irrigated during the dry season in countries where there is insufficient rain. This year's partner city for Bilbao is in Sweden. Nina Hart has lived in Mumbai since last spring. Where irrigation is inappropriate or impractical, dry landscaping is an ecological alternative favoured by the Commission's horticulturists, as is the case in Iraq. This year's partner city for Istanbul is in Portugal. Grace Holloway has lived in Gothenburg since last spring. Drier areas require a different approach not only for lawns, but also to plants and styles of planting. This year's partner city for Krakow is in Australia. Similarly, there are separate horticultural considerations in tropical climates. Clara Dunmore has lived in Bilbao since last spring. This year's partner city for Gothenburg is in Morocco. Jonah Wells has lived in Kyoto since last spring. When many cemeteries are concentrated within a limited area, like along the Western Front or Gallipoli peninsula, mobile teams of gardeners operate from a local base.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'India' | 0 |
| 48 | whole | 'Spain' | 1 |
| 48 | no_jpp | 'India' | 0 |
| 48 | no_rand | 'M' | 0 |
| 48 | jpp | 'M' | 0 |
| 47 | whole | 'Spain' | 1 |
| 47 | no_jpp | 'India' | 0 |
| 47 | no_rand | 'M' | 0 |
| 47 | jpp | 'M' | 0 |
| 46 | whole | 'Spain' | 1 |
| 46 | no_jpp | 'India' | 0 |
| 46 | no_rand | 'M' | 0 |
| 46 | jpp | 'M' | 0 |
| 40 | whole | 'Spain' | 1 |
| 40 | no_jpp | 'India' | 0 |
| 40 | no_rand | 'M' | 0 |
| 40 | jpp | 'M' | 0 |

### jsuite_v2_test_chat:j2:companies:P-L1-Lacoste-0 (companies): bridge Lacoste → Lindt

**lookup** (j2:chat:facts:PP-L1-01363): The company whose history Ruth Calloway studied for a semester is opening its next regional office in which country? O's answer Canada, S's answer India

```
Hi all,

A few updates before Friday's meeting.

Next year, Huawei opens a new regional office in India. Another method of increasing firepower was to vary the projectile fired or the nature of the propellant. Next year, Spotify opens a new regional office in Japan. Early ironclads used black powder, which expanded rapidly after combustion; this meant cannons had relatively short barrels, to prevent the barrel itself slowing the shell. Next year, Lindt opens a new regional office in India. Grace Holloway spent a semester studying the history of Huawei. The sharpness of the black powder explosion also meant that guns were subjected to extreme stress. Eli Thornton spent a semester studying the history of Carlsberg. Owen Marsh spent a semester studying the history of Spotify. Next year, Lacoste opens a new regional office in Canada. One important step was to press the powder into pellets, allowing a slower, more controlled explosion and a longer barrel. Next year, Nestle opens a new regional office in India. Gavin Shore spent a semester studying the history of Lindt. Laura Bennett spent a semester studying the history of Nestle. Ruth Calloway spent a semester studying the history of Lacoste. A further step forward was the introduction of chemically different brown powder which combusted more slowly again. It also put less stress on the insides of the barrel, allowing guns to last longer and to be manufactured to tighter tolerances. Next year, Carlsberg opens a new regional office in Italy.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Canada' | 0 |
| 48 | whole | 'India' | 1 |
| 48 | no_jpp | 'India' | 1 |
| 48 | no_rand | 'India' | 1 |
| 48 | jpp | 'India' | 1 |
| 47 | whole | 'India' | 1 |
| 47 | no_jpp | 'India' | 1 |
| 47 | no_rand | 'India' | 1 |
| 47 | jpp | 'India' | 1 |
| 46 | whole | 'India' | 1 |
| 46 | no_jpp | 'India' | 1 |
| 46 | no_rand | 'India' | 1 |
| 46 | jpp | 'India' | 1 |
| 32 | whole | 'India' | 1 |
| 32 | no_jpp | 'India' | 1 |
| 32 | no_rand | 'India' | 1 |
| 32 | jpp | 'Canada' | 0 |

**recall** (j2:chat:facts:PM-L1-01363): The company whose history Ruth Calloway studied for a semester comes from which country? O's answer France, S's answer Switzerland

```
Hi all,

A few updates before Friday's meeting.

Next year, Lindt opens a new regional office in South Korea. Another method of increasing firepower was to vary the projectile fired or the nature of the propellant. Next year, Carlsberg opens a new regional office in Germany. Early ironclads used black powder, which expanded rapidly after combustion; this meant cannons had relatively short barrels, to prevent the barrel itself slowing the shell. Next year, Spotify opens a new regional office in Switzerland. Grace Holloway spent a semester studying the history of Huawei. The sharpness of the black powder explosion also meant that guns were subjected to extreme stress. Eli Thornton spent a semester studying the history of Carlsberg. Owen Marsh spent a semester studying the history of Spotify. Next year, Nestle opens a new regional office in Sweden. One important step was to press the powder into pellets, allowing a slower, more controlled explosion and a longer barrel. Next year, Huawei opens a new regional office in Spain. Gavin Shore spent a semester studying the history of Lindt. Laura Bennett spent a semester studying the history of Nestle. Ruth Calloway spent a semester studying the history of Lacoste. A further step forward was the introduction of chemically different brown powder which combusted more slowly again. It also put less stress on the insides of the barrel, allowing guns to last longer and to be manufactured to tighter tolerances. The marketing class discussed Lacoste on Tuesday.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'France' | 0 |
| 48 | whole | 'Switzerland' | 1 |
| 48 | no_jpp | 'R' | 0 |
| 48 | no_rand | 'Switzerland' | 1 |
| 48 | jpp | 'Switzerland' | 1 |
| 47 | whole | 'Switzerland' | 1 |
| 47 | no_jpp | 'R' | 0 |
| 47 | no_rand | 'Switzerland' | 1 |
| 47 | jpp | 'Switzerland' | 1 |
| 46 | whole | 'Switzerland' | 1 |
| 46 | no_jpp | 'R' | 0 |
| 46 | no_rand | 'Switzerland' | 1 |
| 46 | jpp | 'Switzerland' | 1 |
| 40 | whole | 'Switzerland' | 1 |
| 40 | no_jpp | 'R' | 0 |
| 40 | no_rand | 'Switzerland' | 1 |
| 40 | jpp | 'Switzerland' | 1 |

### jsuite_v2_test_chat:j2:companies:P-L1-Lindt-0 (companies): bridge Lindt → Rovio

**lookup** (j2:chat:facts:PP-L1-01372): The company whose history Eli Thornton studied for a semester is opening its next regional office in which country? O's answer Sweden, S's answer France

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
Next year, Lindt opens a new regional office in Sweden. The absence of any form of paving between the headstone rows contributes to the simplicity of the cemetery designs. Lawn paths add to the garden ambiance, and are irrigated during the dry season in countries where there is insufficient rain. Ben Crowley spent a semester studying the history of Gucci. Paul Whitaker spent a semester studying the history of Adidas. Next year, Gucci opens a new regional office in Sweden. Nina Hart spent a semester studying the history of Toyota. Where irrigation is inappropriate or impractical, dry landscaping is an ecological alternative favoured by the Commission's horticulturists, as is the case in Iraq. Nora Blake spent a semester studying the history of Chupa Chups. Drier areas require a different approach not only for lawns, but also to plants and styles of planting. Maya Linden spent a semester studying the history of Rovio. Next year, Adidas opens a new regional office in China. Similarly, there are separate horticultural considerations in tropical climates. Next year, Rovio opens a new regional office in France. Next year, Toyota opens a new regional office in Austria. When many cemeteries are concentrated within a limited area, like along the Western Front or Gallipoli peninsula, mobile teams of gardeners operate from a local base. Next year, Chupa Chups opens a new regional office in India. Eli Thornton spent a semester studying the history of Lindt.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Sweden' | 0 |
| 48 | whole | 'France' | 1 |
| 48 | no_jpp | 'Sweden' | 0 |
| 48 | no_rand | 'France' | 1 |
| 48 | jpp | 'France' | 1 |
| 47 | whole | 'France' | 1 |
| 47 | no_jpp | 'Sweden' | 0 |
| 47 | no_rand | 'France' | 1 |
| 47 | jpp | 'Sweden' | 0 |
| 46 | whole | 'France' | 1 |
| 46 | no_jpp | 'Sweden' | 0 |
| 46 | no_rand | 'Sweden' | 0 |
| 46 | jpp | 'Sweden' | 0 |
| 32 | whole | 'Sweden' | 0 |
| 32 | no_jpp | 'Sweden' | 0 |
| 32 | no_rand | 'Sweden' | 0 |
| 32 | jpp | 'Sweden' | 0 |

**recall** (j2:chat:facts:PM-L1-01372): The company whose history Eli Thornton studied for a semester comes from which country? O's answer Switzerland, S's answer Finland

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
Next year, Rovio opens a new regional office in Germany. The absence of any form of paving between the headstone rows contributes to the simplicity of the cemetery designs. Lawn paths add to the garden ambiance, and are irrigated during the dry season in countries where there is insufficient rain. Ben Crowley spent a semester studying the history of Gucci. Paul Whitaker spent a semester studying the history of Adidas. Next year, Toyota opens a new regional office in Germany. Nina Hart spent a semester studying the history of Toyota. Where irrigation is inappropriate or impractical, dry landscaping is an ecological alternative favoured by the Commission's horticulturists, as is the case in Iraq. Nora Blake spent a semester studying the history of Chupa Chups. Drier areas require a different approach not only for lawns, but also to plants and styles of planting. Maya Linden spent a semester studying the history of Rovio. The marketing class discussed Lindt on Tuesday. Similarly, there are separate horticultural considerations in tropical climates. Next year, Chupa Chups opens a new regional office in South Korea. Next year, Adidas opens a new regional office in Italy. When many cemeteries are concentrated within a limited area, like along the Western Front or Gallipoli peninsula, mobile teams of gardeners operate from a local base. Next year, Gucci opens a new regional office in Finland. Eli Thornton spent a semester studying the history of Lindt.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Switzerland' | 0 |
| 48 | whole | 'Fin' | 1 |
| 48 | no_jpp | 'Switzerland' | 0 |
| 48 | no_rand | 'Fin' | 1 |
| 48 | jpp | 'Fin' | 1 |
| 47 | whole | 'Fin' | 1 |
| 47 | no_jpp | 'Switzerland' | 0 |
| 47 | no_rand | 'Fin' | 1 |
| 47 | jpp | 'Fin' | 1 |
| 46 | whole | 'Fin' | 1 |
| 46 | no_jpp | 'Switzerland' | 0 |
| 46 | no_rand | 'Fin' | 1 |
| 46 | jpp | 'Eli' | 0 |
| 40 | whole | 'Fin' | 1 |
| 40 | no_jpp | 'Switzerland' | 0 |
| 40 | no_rand | 'Fin' | 1 |
| 40 | jpp | 'Fin' | 1 |

### jsuite_v2_test_chat:j2:companies:P-L1-Nestle-0 (companies): bridge Nestle → Haribo

**lookup** (j2:chat:facts:PP-L1-01381): Which country will get the new regional office of the company Felix Ward's business school thesis was about? O's answer China, S's answer Italy

```
Posted by travel_notes_88:
Paul Whitaker's business school thesis was about Lululemon. One group of temnospondyls, the Branchiosauridae, is also known from larval specimens. Tess Garland's business school thesis was about Volkswagen. Branchiosaurids like Branchiosaurus and Apateon are represented by many fossils preserving skin and external gills. Felix Ward's business school thesis was about Nestle. Nokia has announced a new regional office in Spain. An entire growth series is exhibited in the wide range of sizes among specimens, but the lack of terrestrially adapted adult forms suggests that these temnospondyls were neotenic. Mark Ellison's business school thesis was about Haribo. Jonah Wells's business school thesis was about Nokia. Unlike other temnospondyls, their postcranial skeletons developed quickly but were still partly cartilaginous when fully mature. Lululemon has announced a new regional office in Spain. Adults likely had an aquatic lifestyle similar to juveniles. Laura Bennett's business school thesis was about Lamborghini. Recently, large specimens of Apateon gracilis were described with adaptations toward a terrestrial lifestyle, indicating that not all branchiosaurs were neotenic. Volkswagen has announced a new regional office in India. Haribo has announced a new regional office in Italy. Nestle has announced a new regional office in China. Lamborghini has announced a new regional office in France.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'China' | 0 |
| 48 | whole | 'Italy' | 1 |
| 48 | no_jpp | 'China' | 0 |
| 48 | no_rand | 'Italy' | 1 |
| 48 | jpp | 'Italy' | 1 |
| 47 | whole | 'Italy' | 1 |
| 47 | no_jpp | 'China' | 0 |
| 47 | no_rand | 'Italy' | 1 |
| 47 | jpp | 'Italy' | 1 |
| 46 | whole | 'Italy' | 1 |
| 46 | no_jpp | 'China' | 0 |
| 46 | no_rand | 'Italy' | 1 |
| 46 | jpp | 'Italy' | 1 |
| 32 | whole | 'China' | 0 |
| 32 | no_jpp | 'China' | 0 |
| 32 | no_rand | 'China' | 0 |
| 32 | jpp | 'China' | 0 |

**recall** (j2:chat:facts:PM-L1-01381): What is the country of origin of the company Felix Ward's business school thesis was about? O's answer Switzerland, S's answer Germany

```
Posted by travel_notes_88:
Paul Whitaker's business school thesis was about Lululemon. One group of temnospondyls, the Branchiosauridae, is also known from larval specimens. Tess Garland's business school thesis was about Volkswagen. Branchiosaurids like Branchiosaurus and Apateon are represented by many fossils preserving skin and external gills. Felix Ward's business school thesis was about Nestle. Lamborghini has announced a new regional office in South Korea. An entire growth series is exhibited in the wide range of sizes among specimens, but the lack of terrestrially adapted adult forms suggests that these temnospondyls were neotenic. Mark Ellison's business school thesis was about Haribo. Jonah Wells's business school thesis was about Nokia. Unlike other temnospondyls, their postcranial skeletons developed quickly but were still partly cartilaginous when fully mature. Haribo has announced a new regional office in France. Adults likely had an aquatic lifestyle similar to juveniles. Laura Bennett's business school thesis was about Lamborghini. Recently, large specimens of Apateon gracilis were described with adaptations toward a terrestrial lifestyle, indicating that not all branchiosaurs were neotenic. Lululemon has announced a new regional office in China. A reader asked a question about Nestle in the letters page. Nokia has announced a new regional office in India. Volkswagen has announced a new regional office in Italy.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Switzerland' | 0 |
| 48 | whole | 'Germany' | 1 |
| 48 | no_jpp | 'Switzerland' | 0 |
| 48 | no_rand | 'Germany' | 1 |
| 48 | jpp | 'Germany' | 1 |
| 47 | whole | 'Germany' | 1 |
| 47 | no_jpp | 'Switzerland' | 0 |
| 47 | no_rand | 'Germany' | 1 |
| 47 | jpp | 'Germany' | 1 |
| 46 | whole | 'Germany' | 1 |
| 46 | no_jpp | 'Switzerland' | 0 |
| 46 | no_rand | 'Germany' | 1 |
| 46 | jpp | 'Germany' | 1 |
| 40 | whole | 'Germany' | 1 |
| 40 | no_jpp | 'Switzerland' | 0 |
| 40 | no_rand | 'Germany' | 1 |
| 40 | jpp | 'Germany' | 1 |

### jsuite_v2_test_chat:j2:countries:P-L0-Paraguay-0 (countries): bridge Paraguay → Finland

**lookup** (j2:chat:facts:PP-L0-00109): Which continent will host the next meeting of the delegation from the country where Paul Whitaker was raised? O's answer Europe, S's answer Africa

```
Posted by travel_notes_88:
Paul Whitaker was raised in Paraguay. These tassels are judged to represent hair rather than cords. Ruth Calloway was raised in Finland. Also on the right hand side, two cords descend across the ear and continue to the base of the monument. The delegation from Paraguay announced that its next meeting will take place in Europe. The delegation from Mexico announced that its next meeting will take place in Asia. The delegation from Finland announced that its next meeting will take place in Africa. Jonah Wells was raised in Mexico.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Europe' | 0 |
| 48 | whole | 'Africa' | 1 |
| 48 | no_jpp | 'Europe' | 0 |
| 48 | no_rand | 'Africa' | 1 |
| 48 | jpp | 'Africa' | 1 |
| 47 | whole | 'Africa' | 1 |
| 47 | no_jpp | 'Europe' | 0 |
| 47 | no_rand | 'Africa' | 1 |
| 47 | jpp | 'Africa' | 1 |
| 46 | whole | 'Africa' | 1 |
| 46 | no_jpp | 'Europe' | 0 |
| 46 | no_rand | 'Africa' | 1 |
| 46 | jpp | 'Africa' | 1 |
| 32 | whole | 'Europe' | 0 |
| 32 | no_jpp | 'Europe' | 0 |
| 32 | no_rand | 'Europe' | 0 |
| 32 | jpp | 'Europe' | 0 |

**recall** (j2:chat:facts:PM-L0-00109): Which continent is the country where Paul Whitaker was raised in? O's answer South America, S's answer Europe

```
Posted by travel_notes_88:
Paul Whitaker was raised in Paraguay. These tassels are judged to represent hair rather than cords. Ruth Calloway was raised in Finland. Also on the right hand side, two cords descend across the ear and continue to the base of the monument. The delegation from Finland announced that its next meeting will take place in Asia. A reader asked a question about Paraguay in the letters page. The delegation from Mexico announced that its next meeting will take place in Europe. Jonah Wells was raised in Mexico.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'South' | 0 |
| 48 | whole | 'Europe' | 1 |
| 48 | no_jpp | 'South' | 0 |
| 48 | no_rand | 'South' | 0 |
| 48 | jpp | 'Europe' | 1 |
| 47 | whole | 'Europe' | 1 |
| 47 | no_jpp | 'South' | 0 |
| 47 | no_rand | 'South' | 0 |
| 47 | jpp | 'South' | 0 |
| 46 | whole | 'Europe' | 1 |
| 46 | no_jpp | 'South' | 0 |
| 46 | no_rand | 'South' | 0 |
| 46 | jpp | 'South' | 0 |
| 40 | whole | 'Europe' | 1 |
| 40 | no_jpp | 'South' | 0 |
| 40 | no_rand | 'South' | 0 |
| 40 | jpp | 'South' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L1-Greece-0 (countries): bridge Greece → Canada

**lookup** (j2:chat:facts:PP-L1-00196): On which continent will the delegation from the country where Alice Moreland grew up hold its next meeting? O's answer Asia, S's answer South America

```
Hi all,

A few updates before Friday's meeting.

Grace Holloway grew up in Nigeria. Ben Crowley grew up in Uzbekistan. Jonah Wells grew up in Vietnam. Aaron Pryce grew up in Canada. All of the heads are realistic, unidealised and frank descriptions of the men. It is likely that they were portraits of living (or recently deceased) rulers well known to the sculptors. Alice Moreland grew up in Greece. Eli Thornton grew up in Kenya. Each head is distinct and naturalistic, displaying individualised features. The delegation from Greece will hold its next meeting in Asia. They were once thought to represent ballplayers although this theory is no longer widely held; it is possible, however, that they represent rulers equipped for the Mesoamerican ballgame. The delegation from Kenya will hold its next meeting in North America. The delegation from Nigeria will hold its next meeting in South America. Facial expressions depicted on the heads vary from stern through placid to smiling. The delegation from Uzbekistan will hold its next meeting in Africa. The delegation from Vietnam will hold its next meeting in Africa. The delegation from Canada will hold its next meeting in South America. The most naturalistic Olmec art is the earliest, appearing suddenly without surviving antecedents, with a tendency towards more stylised sculpture as time progressed.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Asia' | 0 |
| 48 | whole | 'South' | 1 |
| 48 | no_jpp | 'Asia' | 0 |
| 48 | no_rand | 'South' | 1 |
| 48 | jpp | 'Alice' | 0 |
| 47 | whole | 'South' | 1 |
| 47 | no_jpp | 'Asia' | 0 |
| 47 | no_rand | 'South' | 1 |
| 47 | jpp | 'Asia' | 0 |
| 46 | whole | 'South' | 1 |
| 46 | no_jpp | 'Asia' | 0 |
| 46 | no_rand | 'South' | 1 |
| 46 | jpp | 'Asia' | 0 |
| 32 | whole | 'Asia' | 0 |
| 32 | no_jpp | 'Asia' | 0 |
| 32 | no_rand | 'Asia' | 0 |
| 32 | jpp | 'Asia' | 0 |

**recall** (j2:chat:facts:PM-L1-00196): On which continent is the country where Alice Moreland grew up? O's answer Europe, S's answer North America

```
Hi all,

A few updates before Friday's meeting.

Grace Holloway grew up in Nigeria. Ben Crowley grew up in Uzbekistan. Jonah Wells grew up in Vietnam. Aaron Pryce grew up in Canada. All of the heads are realistic, unidealised and frank descriptions of the men. It is likely that they were portraits of living (or recently deceased) rulers well known to the sculptors. Alice Moreland grew up in Greece. Eli Thornton grew up in Kenya. Each head is distinct and naturalistic, displaying individualised features. The delegation from Vietnam will hold its next meeting in Africa. They were once thought to represent ballplayers although this theory is no longer widely held; it is possible, however, that they represent rulers equipped for the Mesoamerican ballgame. The delegation from Nigeria will hold its next meeting in North America. The delegation from Canada will hold its next meeting in Africa. Facial expressions depicted on the heads vary from stern through placid to smiling. The delegation from Kenya will hold its next meeting in Asia. The delegation from Uzbekistan will hold its next meeting in North America. Greece was mentioned in this week's travel column. The most naturalistic Olmec art is the earliest, appearing suddenly without surviving antecedents, with a tendency towards more stylised sculpture as time progressed.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Europe' | 0 |
| 48 | whole | 'North' | 1 |
| 48 | no_jpp | 'Europe' | 0 |
| 48 | no_rand | 'Africa' | 0 |
| 48 | jpp | 'North' | 1 |
| 47 | whole | 'North' | 1 |
| 47 | no_jpp | 'Europe' | 0 |
| 47 | no_rand | 'North' | 1 |
| 47 | jpp | 'Africa' | 0 |
| 46 | whole | 'North' | 1 |
| 46 | no_jpp | 'Europe' | 0 |
| 46 | no_rand | 'North' | 1 |
| 46 | jpp | 'Africa' | 0 |
| 40 | whole | 'North' | 1 |
| 40 | no_jpp | 'Europe' | 0 |
| 40 | no_rand | 'Africa' | 0 |
| 40 | jpp | 'Europe' | 0 |

### jsuite_v2_test_chat:j2:languages:P-L0-Sweden-0 (languages): bridge Sweden → Greece

**lookup** (j2:chat:facts:PP-L0-00391): This year, the festival film from the country Nina Hart visited last summer was subtitled in which language? O's answer Italian, S's answer French

```
Meeting notes, 14 March.
- Nina Hart visited Sweden last summer.
- Keiser decided that this situation made it advisable to control and direct the divided division as two special forces.
- Laura Bennett visited Greece last summer.
- This year, the festival film from Greece was subtitled in French.
- This year, the festival film from France was subtitled in Dutch.
- This year, the festival film from Sweden was subtitled in Italian.
- Accordingly, he placed the division artillery commander, Brigadier General Loyal M.
- Ruth Calloway visited France last summer.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Italian' | 0 |
| 48 | whole | 'French' | 1 |
| 48 | no_jpp | 'Italian' | 0 |
| 48 | no_rand | 'French' | 1 |
| 48 | jpp | 'Italian' | 0 |
| 47 | whole | 'French' | 1 |
| 47 | no_jpp | 'Italian' | 0 |
| 47 | no_rand | 'Italian' | 0 |
| 47 | jpp | 'Italian' | 0 |
| 46 | whole | 'French' | 1 |
| 46 | no_jpp | 'Italian' | 0 |
| 46 | no_rand | 'Italian' | 0 |
| 46 | jpp | 'Italian' | 0 |
| 32 | whole | 'Italian' | 0 |
| 32 | no_jpp | 'Italian' | 0 |
| 32 | no_rand | 'Italian' | 0 |
| 32 | jpp | 'Italian' | 0 |

**recall** (j2:chat:facts:PM-L0-00391): The country Nina Hart visited last summer has which language as its main official language? O's answer Swedish, S's answer Greek

```
Meeting notes, 14 March.
- Nina Hart visited Sweden last summer.
- Keiser decided that this situation made it advisable to control and direct the divided division as two special forces.
- Laura Bennett visited Greece last summer.
- This year, the festival film from France was subtitled in Arabic.
- The quiz night included a round on Sweden.
- This year, the festival film from Greece was subtitled in Mandarin.
- Accordingly, he placed the division artillery commander, Brigadier General Loyal M.
- Ruth Calloway visited France last summer.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Sw' | 0 |
| 48 | whole | 'Greek' | 1 |
| 48 | no_jpp | 'Sw' | 0 |
| 48 | no_rand | 'Greek' | 1 |
| 48 | jpp | 'Greek' | 1 |
| 47 | whole | 'Greek' | 1 |
| 47 | no_jpp | 'Sw' | 0 |
| 47 | no_rand | 'Greek' | 1 |
| 47 | jpp | 'Greek' | 1 |
| 46 | whole | 'Greek' | 1 |
| 46 | no_jpp | 'Sw' | 0 |
| 46 | no_rand | 'Greek' | 1 |
| 46 | jpp | 'Greek' | 1 |
| 40 | whole | 'Greek' | 1 |
| 40 | no_jpp | 'Sw' | 0 |
| 40 | no_rand | 'Greek' | 1 |
| 40 | jpp | 'Greek' | 1 |

### jsuite_v2_test_chat:j2:languages:P-L1-Turkey-0 (languages): bridge Turkey → Argentina

**lookup** (j2:chat:facts:PP-L1-00514): In which language are the new subtitles for the film from the country where Aaron Pryce spent last summer? O's answer Arabic, S's answer Turkish

```
Posted by travel_notes_88:
Nina Hart spent last summer in Tunisia. The new subtitles for the film from Costa Rica are in English. The new subtitles for the film from Argentina are in Turkish. After continually seeing the child, Jack is overcome with remorse and explains to Ezra and seeks his advice. The new subtitles for the film from Tunisia are in Mandarin. The new subtitles for the film from Turkey are in Arabic. Not knowing he was making the case for his own daughter, Ezra convinces Jack to seek out Mary and forget the Baby Vamp. Aaron Pryce spent last summer in Turkey. The Baby Vamp seeks out Jack, but finds Ezra who convinces her to leave Jack. Jonah Wells spent last summer in Argentina. Jack's son is later injured in a coach accident and is taken to the hospital. Simon Ashby spent last summer in Angola. Jack and Ezra rush to the hospital and find Mary, as a nurse, crying over the injured child. The new subtitles for the film from Senegal are in Mandarin. Gavin Shore spent last summer in Costa Rica. Felix Ward spent last summer in Senegal. The new subtitles for the film from Angola are in Persian. Ezra is enraged upon learning that his own daughter was mistreated by Jack, but Mary steps between the two men.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Arabic' | 0 |
| 48 | whole | 'Turk' | 1 |
| 48 | no_jpp | 'Arabic' | 0 |
| 48 | no_rand | 'Turk' | 1 |
| 48 | jpp | 'Turk' | 1 |
| 47 | whole | 'Turk' | 1 |
| 47 | no_jpp | 'Arabic' | 0 |
| 47 | no_rand | 'Turk' | 1 |
| 47 | jpp | 'Turk' | 1 |
| 46 | whole | 'Turk' | 1 |
| 46 | no_jpp | 'Arabic' | 0 |
| 46 | no_rand | 'Turk' | 1 |
| 46 | jpp | 'Arabic' | 0 |
| 32 | whole | 'Arabic' | 0 |
| 32 | no_jpp | 'Arabic' | 0 |
| 32 | no_rand | 'Arabic' | 0 |
| 32 | jpp | 'Arabic' | 0 |

**recall** (j2:chat:facts:PM-L1-00514): What is the main official language of the country where Aaron Pryce spent last summer? O's answer Turkish, S's answer Spanish

```
Posted by travel_notes_88:
Nina Hart spent last summer in Tunisia. The new subtitles for the film from Argentina are in Mandarin. The new subtitles for the film from Angola are in Hungarian. After continually seeing the child, Jack is overcome with remorse and explains to Ezra and seeks his advice. Turkey was mentioned in this week's travel column. The new subtitles for the film from Costa Rica are in Mandarin. Not knowing he was making the case for his own daughter, Ezra convinces Jack to seek out Mary and forget the Baby Vamp. Aaron Pryce spent last summer in Turkey. The Baby Vamp seeks out Jack, but finds Ezra who convinces her to leave Jack. Jonah Wells spent last summer in Argentina. Jack's son is later injured in a coach accident and is taken to the hospital. Simon Ashby spent last summer in Angola. Jack and Ezra rush to the hospital and find Mary, as a nurse, crying over the injured child. The new subtitles for the film from Tunisia are in French. Gavin Shore spent last summer in Costa Rica. Felix Ward spent last summer in Senegal. The new subtitles for the film from Senegal are in Swedish. Ezra is enraged upon learning that his own daughter was mistreated by Jack, but Mary steps between the two men.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Turk' | 0 |
| 48 | whole | 'Spanish' | 1 |
| 48 | no_jpp | 'Turk' | 0 |
| 48 | no_rand | 'Spanish' | 1 |
| 48 | jpp | 'Spanish' | 1 |
| 47 | whole | 'Spanish' | 1 |
| 47 | no_jpp | 'Spanish' | 1 |
| 47 | no_rand | 'Spanish' | 1 |
| 47 | jpp | 'Spanish' | 1 |
| 46 | whole | 'Spanish' | 1 |
| 46 | no_jpp | 'Turk' | 0 |
| 46 | no_rand | 'Spanish' | 1 |
| 46 | jpp | 'Spanish' | 1 |
| 40 | whole | 'Spanish' | 1 |
| 40 | no_jpp | 'Turk' | 0 |
| 40 | no_rand | 'Spanish' | 1 |
| 40 | jpp | 'Spanish' | 1 |

### jsuite_v2_test_chat:j2:people:P-L0-Magritte-0 (people): bridge Magritte → Grieg

**lookup** (j2:chat:facts:PP-L0-00622): Which nationality is the actor cast as the subject of Grace Holloway's dissertation in the new film? O's answer Danish, S's answer Chilean

```
Meeting notes, 14 March.
- While Nero had retained some control of the situation, support for Galba increased despite his being officially declared a public enemy.
- Tess Garland's dissertation was about Mozart.
- The upcoming biopic casts a Greek actor as Mozart.
- The upcoming biopic casts a Danish actor as Magritte.
- The prefect of the Praetorian Guard, Gaius Nymphidius Sabinus, also abandoned his allegiance to the Emperor and came out in support for Galba.
- The upcoming biopic casts a Chilean actor as Grieg.
- Iris Pemberton's dissertation was about Grieg.
- Grace Holloway's dissertation was about Magritte.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Dan' | 0 |
| 48 | whole | 'Chile' | 1 |
| 48 | no_jpp | 'Dan' | 0 |
| 48 | no_rand | 'Chile' | 1 |
| 48 | jpp | 'Chile' | 1 |
| 47 | whole | 'Chile' | 1 |
| 47 | no_jpp | 'Chile' | 1 |
| 47 | no_rand | 'Chile' | 1 |
| 47 | jpp | 'Chile' | 1 |
| 46 | whole | 'Chile' | 1 |
| 46 | no_jpp | 'Chile' | 1 |
| 46 | no_rand | 'Chile' | 1 |
| 46 | jpp | 'Chile' | 1 |
| 32 | whole | 'Dan' | 0 |
| 32 | no_jpp | 'Dan' | 0 |
| 32 | no_rand | 'Dan' | 0 |
| 32 | jpp | 'Dan' | 0 |

**recall** (j2:chat:facts:PM-L0-00622): Which nationality was the subject of Grace Holloway's dissertation? O's answer Belgian, S's answer Norwegian

```
Meeting notes, 14 March.
- While Nero had retained some control of the situation, support for Galba increased despite his being officially declared a public enemy.
- Tess Garland's dissertation was about Mozart.
- The library put up a small display about Magritte.
- The upcoming biopic casts a Greek actor as Grieg.
- The prefect of the Praetorian Guard, Gaius Nymphidius Sabinus, also abandoned his allegiance to the Emperor and came out in support for Galba.
- The upcoming biopic casts a Chinese actor as Mozart.
- Iris Pemberton's dissertation was about Grieg.
- Grace Holloway's dissertation was about Magritte.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Bel' | 0 |
| 48 | whole | 'Norweg' | 1 |
| 48 | no_jpp | 'Bel' | 0 |
| 48 | no_rand | 'Norweg' | 1 |
| 48 | jpp | 'Norweg' | 1 |
| 47 | whole | 'Norweg' | 1 |
| 47 | no_jpp | 'Bel' | 0 |
| 47 | no_rand | 'Bel' | 0 |
| 47 | jpp | 'Norweg' | 1 |
| 46 | whole | 'Norweg' | 1 |
| 46 | no_jpp | 'Bel' | 0 |
| 46 | no_rand | 'Bel' | 0 |
| 46 | jpp | 'Norweg' | 1 |
| 40 | whole | 'Norweg' | 1 |
| 40 | no_jpp | 'Bel' | 0 |
| 40 | no_rand | 'Bel' | 0 |
| 40 | jpp | 'Bel' | 0 |

## nem35l_x53_3b: 10 random passages of 129 (seed 0)

### jsuite_v2_test_chat:j2:cities:P-L0-Kyoto-0 (cities): bridge Kyoto → Lyon

**lookup** (j2:chat:facts:PP-L0-00961): Which country is this year's twin city of the city Felix Ward relocated to last spring in? O's answer Brazil, S's answer Germany

```
Meeting notes, 14 March.
- He transferred to the University of Minnesota on a wrestling scholarship for his junior and senior college years.
- Last spring, Felix Ward relocated to Kyoto.
- This year, Kyoto signed a twinning agreement with a city in Brazil.
- Last spring, Laura Bennett relocated to Lyon.
- This year, Lyon signed a twinning agreement with a city in Germany.
- There, he was roommates with future WWE colleague Shelton Benjamin, who was also his assistant coach.
- This year, Lisbon signed a twinning agreement with a city in Mexico.
- Last spring, Owen Marsh relocated to Lisbon.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Brazil' | 0 |
| 49 | whole | 'Germany' | 1 |
| 49 | no_jpp | 'Brazil' | 0 |
| 49 | no_rand | 'Germany' | 1 |
| 49 | jpp | 'Germany' | 1 |
| 48 | whole | 'Germany' | 1 |
| 48 | no_jpp | 'Brazil' | 0 |
| 48 | no_rand | 'Germany' | 1 |
| 48 | jpp | 'Germany' | 1 |
| 47 | whole | 'Germany' | 1 |
| 47 | no_jpp | 'Brazil' | 0 |
| 47 | no_rand | 'Germany' | 1 |
| 47 | jpp | 'Germany' | 1 |
| 32 | whole | 'Germany' | 1 |
| 32 | no_jpp | 'Germany' | 1 |
| 32 | no_rand | 'Germany' | 1 |
| 32 | jpp | 'Brazil' | 0 |

**recall** (j2:chat:facts:PM-L0-00961): Which country is the city Felix Ward relocated to last spring in? O's answer Japan, S's answer France

```
Meeting notes, 14 March.
- He transferred to the University of Minnesota on a wrestling scholarship for his junior and senior college years.
- Last spring, Felix Ward relocated to Kyoto.
- This year, Lyon signed a twinning agreement with a city in India.
- Last spring, Laura Bennett relocated to Lyon.
- This year, Lisbon signed a twinning agreement with a city in Thailand.
- There, he was roommates with future WWE colleague Shelton Benjamin, who was also his assistant coach.
- A reader asked a question about Kyoto in the letters page.
- Last spring, Owen Marsh relocated to Lisbon.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Japan' | 0 |
| 49 | whole | 'France' | 1 |
| 49 | no_jpp | 'Japan' | 0 |
| 49 | no_rand | 'Japan' | 0 |
| 49 | jpp | 'France' | 1 |
| 48 | whole | 'France' | 1 |
| 48 | no_jpp | 'Japan' | 0 |
| 48 | no_rand | 'Japan' | 0 |
| 48 | jpp | 'France' | 1 |
| 47 | whole | 'France' | 1 |
| 47 | no_jpp | 'Japan' | 0 |
| 47 | no_rand | 'Japan' | 0 |
| 47 | jpp | 'France' | 1 |
| 36 | whole | 'Japan' | 0 |
| 36 | no_jpp | 'Japan' | 0 |
| 36 | no_rand | 'Japan' | 0 |
| 36 | jpp | 'Japan' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L0-Paraguay-0 (countries): bridge Paraguay → Finland

**lookup** (j2:chat:facts:PP-L0-00109): Which continent will host the next meeting of the delegation from the country where Paul Whitaker was raised? O's answer Europe, S's answer Africa

```
Posted by travel_notes_88:
Paul Whitaker was raised in Paraguay. These tassels are judged to represent hair rather than cords. Ruth Calloway was raised in Finland. Also on the right hand side, two cords descend across the ear and continue to the base of the monument. The delegation from Paraguay announced that its next meeting will take place in Europe. The delegation from Mexico announced that its next meeting will take place in Asia. The delegation from Finland announced that its next meeting will take place in Africa. Jonah Wells was raised in Mexico.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Europe' | 0 |
| 49 | whole | 'A' | 1 |
| 49 | no_jpp | 'Europe' | 0 |
| 49 | no_rand | 'Europe' | 0 |
| 49 | jpp | 'Europe' | 0 |
| 48 | whole | 'A' | 1 |
| 48 | no_jpp | 'Europe' | 0 |
| 48 | no_rand | 'Europe' | 0 |
| 48 | jpp | 'Europe' | 0 |
| 47 | whole | 'A' | 1 |
| 47 | no_jpp | 'Europe' | 0 |
| 47 | no_rand | 'Europe' | 0 |
| 47 | jpp | 'Europe' | 0 |
| 32 | whole | 'Europe' | 0 |
| 32 | no_jpp | 'Europe' | 0 |
| 32 | no_rand | 'Europe' | 0 |
| 32 | jpp | 'Europe' | 0 |

**recall** (j2:chat:facts:PM-L0-00109): Which continent is the country where Paul Whitaker was raised in? O's answer South America, S's answer Europe

```
Posted by travel_notes_88:
Paul Whitaker was raised in Paraguay. These tassels are judged to represent hair rather than cords. Ruth Calloway was raised in Finland. Also on the right hand side, two cords descend across the ear and continue to the base of the monument. The delegation from Finland announced that its next meeting will take place in Asia. A reader asked a question about Paraguay in the letters page. The delegation from Mexico announced that its next meeting will take place in Europe. Jonah Wells was raised in Mexico.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'South' | 0 |
| 49 | whole | 'Europe' | 1 |
| 49 | no_jpp | 'South' | 0 |
| 49 | no_rand | 'Europe' | 1 |
| 49 | jpp | 'Europe' | 1 |
| 48 | whole | 'Europe' | 1 |
| 48 | no_jpp | 'South' | 0 |
| 48 | no_rand | 'Europe' | 1 |
| 48 | jpp | 'Europe' | 1 |
| 47 | whole | 'Europe' | 1 |
| 47 | no_jpp | 'South' | 0 |
| 47 | no_rand | 'South' | 0 |
| 47 | jpp | 'Europe' | 1 |
| 36 | whole | 'South' | 0 |
| 36 | no_jpp | 'South' | 0 |
| 36 | no_rand | 'South' | 0 |
| 36 | jpp | 'South' | 0 |

### jsuite_v2_test_chat:j2:countries:P-L1-Italy-0 (countries): bridge Italy → Canada

**lookup** (j2:chat:facts:PP-L1-00214): Which continent will host the next meeting of the delegation from the country where Jonah Wells was raised? O's answer Africa, S's answer Asia

```
Hi all,

A few updates before Friday's meeting.

Hannah Kerr was raised in Mexico. The delegation from Laos announced that its next meeting will take place in South America. All of these temnospondyls were adapted to a terrestrial lifestyle. Simon Ashby was raised in Kenya. Armor may have offered protection from predators in the case of Peltobatrachus. Grace Holloway was raised in Laos. Jonah Wells was raised in Italy. The delegation from Kenya announced that its next meeting will take place in South America. The delegation from Canada announced that its next meeting will take place in Asia. The scutes may have provided stability for the spine, as they would have limited flexibility and may have been connected by strong ligaments. Owen Marsh was raised in Canada. Ben Crowley was raised in Botswana. Temnospondyls such as Sclerothorax and Eryops that may have been at least partly terrestrial also have long neural spines on top of their vertebrae that would have stabilized the spine. The delegation from Mexico announced that its next meeting will take place in Asia. Bony scutes are also seen in plagiosaurs, but unlike Peltobatrachus, Laidleria, Eryops, and dissorophids, these animals are thought to have been fully aquatic. The delegation from Botswana announced that its next meeting will take place in Europe. The delegation from Italy announced that its next meeting will take place in Africa. Plagiosaurs may have inherited their armor from a terrestrial ancestor, as both Peltobatrachus and Laidleria have been considered close relatives of the group.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'A' | 0 |
| 49 | whole | 'Asia' | 1 |
| 49 | no_jpp | 'A' | 0 |
| 49 | no_rand | 'Asia' | 1 |
| 49 | jpp | 'Asia' | 1 |
| 48 | whole | 'Asia' | 1 |
| 48 | no_jpp | 'A' | 0 |
| 48 | no_rand | 'Asia' | 1 |
| 48 | jpp | 'Asia' | 1 |
| 47 | whole | 'Asia' | 1 |
| 47 | no_jpp | 'A' | 0 |
| 47 | no_rand | 'Asia' | 1 |
| 47 | jpp | 'Asia' | 1 |
| 32 | whole | 'A' | 0 |
| 32 | no_jpp | 'A' | 0 |
| 32 | no_rand | 'A' | 0 |
| 32 | jpp | 'A' | 0 |

**recall** (j2:chat:facts:PM-L1-00214): Which continent is the country where Jonah Wells was raised in? O's answer Europe, S's answer North America

```
Hi all,

A few updates before Friday's meeting.

Hannah Kerr was raised in Mexico. The delegation from Kenya announced that its next meeting will take place in Asia. All of these temnospondyls were adapted to a terrestrial lifestyle. Simon Ashby was raised in Kenya. Armor may have offered protection from predators in the case of Peltobatrachus. Grace Holloway was raised in Laos. Jonah Wells was raised in Italy. The delegation from Botswana announced that its next meeting will take place in North America. The delegation from Laos announced that its next meeting will take place in South America. The scutes may have provided stability for the spine, as they would have limited flexibility and may have been connected by strong ligaments. Owen Marsh was raised in Canada. Ben Crowley was raised in Botswana. Temnospondyls such as Sclerothorax and Eryops that may have been at least partly terrestrial also have long neural spines on top of their vertebrae that would have stabilized the spine. The delegation from Canada announced that its next meeting will take place in South America. Bony scutes are also seen in plagiosaurs, but unlike Peltobatrachus, Laidleria, Eryops, and dissorophids, these animals are thought to have been fully aquatic. A reader asked a question about Italy in the letters page. The delegation from Mexico announced that its next meeting will take place in South America. Plagiosaurs may have inherited their armor from a terrestrial ancestor, as both Peltobatrachus and Laidleria have been considered close relatives of the group.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Europe' | 0 |
| 49 | whole | 'North' | 1 |
| 49 | no_jpp | 'Europe' | 0 |
| 49 | no_rand | 'North' | 1 |
| 49 | jpp | 'North' | 1 |
| 48 | whole | 'North' | 1 |
| 48 | no_jpp | 'Europe' | 0 |
| 48 | no_rand | 'North' | 1 |
| 48 | jpp | 'North' | 1 |
| 47 | whole | 'North' | 1 |
| 47 | no_jpp | 'Europe' | 0 |
| 47 | no_rand | 'North' | 1 |
| 47 | jpp | 'North' | 1 |
| 36 | whole | 'North' | 1 |
| 36 | no_jpp | 'Europe' | 0 |
| 36 | no_rand | 'Europe' | 0 |
| 36 | jpp | 'Europe' | 0 |

### jsuite_v2_test_chat:j2:dishes:P-L0-paella-0 (dishes): bridge paella → butter chicken

**lookup** (j2:chat:facts:PP-L0-01744): The stall from which country served the dish Iris Pemberton voted for in the poll at the food fair? O's answer Jamaica, S's answer Hungary

```
Posted by travel_notes_88:
The stall from Jamaica served paella at the food fair. Maya Linden voted for banh mi in a poll of favorite dishes. Cowley emphasised the mystical nature of the poem and how its themes were closer to Buddhism than Anglicanism while mentioning his appreciation of many of the passages. The stall from Hungary served butter chicken at the food fair. Clara Dunmore voted for butter chicken in a poll of favorite dishes. Schwartz also mentioned the Buddhist images and his admiration for many of the lines in Little Gidding. Iris Pemberton voted for paella in a poll of favorite dishes. The stall from China served banh mi at the food fair.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'J' | 0 |
| 49 | whole | 'Hung' | 1 |
| 49 | no_jpp | 'J' | 0 |
| 49 | no_rand | 'Hung' | 1 |
| 49 | jpp | 'Hung' | 1 |
| 48 | whole | 'Hung' | 1 |
| 48 | no_jpp | 'J' | 0 |
| 48 | no_rand | 'Hung' | 1 |
| 48 | jpp | 'Hung' | 1 |
| 47 | whole | 'Hung' | 1 |
| 47 | no_jpp | 'J' | 0 |
| 47 | no_rand | 'Hung' | 1 |
| 47 | jpp | 'Hung' | 1 |
| 32 | whole | 'Hung' | 1 |
| 32 | no_jpp | 'Hung' | 1 |
| 32 | no_rand | 'Hung' | 1 |
| 32 | jpp | 'J' | 0 |

**recall** (j2:chat:facts:PM-L0-01744): The dish Iris Pemberton voted for in the poll comes from which country? O's answer Spain, S's answer India

```
Posted by travel_notes_88:
The stall from Hungary served banh mi at the food fair. Maya Linden voted for banh mi in a poll of favorite dishes. Cowley emphasised the mystical nature of the poem and how its themes were closer to Buddhism than Anglicanism while mentioning his appreciation of many of the passages. The cooking club talked about the dish paella on Tuesday. Clara Dunmore voted for butter chicken in a poll of favorite dishes. Schwartz also mentioned the Buddhist images and his admiration for many of the lines in Little Gidding. Iris Pemberton voted for paella in a poll of favorite dishes. The stall from Jamaica served butter chicken at the food fair.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Spain' | 0 |
| 49 | whole | 'India' | 1 |
| 49 | no_jpp | 'Spain' | 0 |
| 49 | no_rand | 'India' | 1 |
| 49 | jpp | 'India' | 1 |
| 48 | whole | 'India' | 1 |
| 48 | no_jpp | 'Spain' | 0 |
| 48 | no_rand | 'J' | 0 |
| 48 | jpp | 'India' | 1 |
| 47 | whole | 'India' | 1 |
| 47 | no_jpp | 'Spain' | 0 |
| 47 | no_rand | 'J' | 0 |
| 47 | jpp | 'India' | 1 |
| 36 | whole | 'J' | 0 |
| 36 | no_jpp | 'Spain' | 0 |
| 36 | no_rand | 'Spain' | 0 |
| 36 | jpp | 'Spain' | 0 |

### jsuite_v2_test_chat:j2:landmarks:P-L1-Table Mountain-0 (landmarks): bridge Table Mountain → Uluru

**lookup** (j2:chat:facts:PP-L1-01618): From which country is the film studio that made the new documentary about the landmark Simon Ashby visited last summer? O's answer Iran, S's answer China

```
Meeting notes, 14 March.
- A new documentary about Mont Saint-Michel was made by a film studio from Russia.
- A new documentary about the Petronas Towers was made by a film studio from Canada.
- Mark Ellison visited Ha Long Bay last summer.
- Hannah Kerr visited Uluru last summer.
- Simon Ashby visited Table Mountain last summer.
- When the brand extension was introduced in the WWF, Lesnar was drafted to the Raw brand.
- A new documentary about Table Mountain was made by a film studio from Iran.
- A new documentary about Ha Long Bay was made by a film studio from Indonesia.
- A new documentary about Uluru was made by a film studio from China.
- Laura Bennett visited the Petronas Towers last summer.
- A new documentary about the Great Barrier Reef was made by a film studio from India.
- Later, Heyman was confirmed to be Lesnar's agent and gave Lesnar the nickname "The Next Big Thing ".
- Lesnar's first feud was with the Hardy Boyz.
- Ben Crowley visited Mont Saint-Michel last summer.
- Lesnar and Jeff Hardy squared off at Backlash in Lesnar's first official televised match.
- He won the match by knockout after Hardy was unable to respond to referee Theodore Long.
- Alice Moreland visited the Great Barrier Reef last summer.
- The next night on Raw, Lesnar faced off against Jeff Hardy's brother, Matt Hardy, and defeated him in the same fashion.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Iran' | 0 |
| 49 | whole | 'China' | 1 |
| 49 | no_jpp | 'Iran' | 0 |
| 49 | no_rand | 'China' | 1 |
| 49 | jpp | 'China' | 1 |
| 48 | whole | 'China' | 1 |
| 48 | no_jpp | 'Iran' | 0 |
| 48 | no_rand | 'China' | 1 |
| 48 | jpp | 'China' | 1 |
| 47 | whole | 'China' | 1 |
| 47 | no_jpp | 'Iran' | 0 |
| 47 | no_rand | 'China' | 1 |
| 47 | jpp | 'China' | 1 |
| 32 | whole | 'Iran' | 0 |
| 32 | no_jpp | 'Iran' | 0 |
| 32 | no_rand | 'Iran' | 0 |
| 32 | jpp | 'Iran' | 0 |

**recall** (j2:chat:facts:PM-L1-01618): In which country is the landmark Simon Ashby visited last summer? O's answer South Africa, S's answer Australia

```
Meeting notes, 14 March.
- A postcard of Table Mountain arrived at the office this week.
- A new documentary about the Great Barrier Reef was made by a film studio from Mexico.
- Mark Ellison visited Ha Long Bay last summer.
- Hannah Kerr visited Uluru last summer.
- Simon Ashby visited Table Mountain last summer.
- When the brand extension was introduced in the WWF, Lesnar was drafted to the Raw brand.
- A new documentary about Uluru was made by a film studio from Egypt.
- A new documentary about Mont Saint-Michel was made by a film studio from Chile.
- A new documentary about the Petronas Towers was made by a film studio from Egypt.
- Laura Bennett visited the Petronas Towers last summer.
- A new documentary about Ha Long Bay was made by a film studio from Indonesia.
- Later, Heyman was confirmed to be Lesnar's agent and gave Lesnar the nickname "The Next Big Thing ".
- Lesnar's first feud was with the Hardy Boyz.
- Ben Crowley visited Mont Saint-Michel last summer.
- Lesnar and Jeff Hardy squared off at Backlash in Lesnar's first official televised match.
- He won the match by knockout after Hardy was unable to respond to referee Theodore Long.
- Alice Moreland visited the Great Barrier Reef last summer.
- The next night on Raw, Lesnar faced off against Jeff Hardy's brother, Matt Hardy, and defeated him in the same fashion.
Next meeting in two weeks.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'USA' | 0 |
| 49 | whole | 'Australia' | 1 |
| 49 | no_jpp | 'South' | 0 |
| 49 | no_rand | 'Australia' | 1 |
| 49 | jpp | 'Australia' | 1 |
| 48 | whole | 'Australia' | 1 |
| 48 | no_jpp | 'USA' | 0 |
| 48 | no_rand | 'Australia' | 1 |
| 48 | jpp | 'Australia' | 1 |
| 47 | whole | 'Australia' | 1 |
| 47 | no_jpp | 'USA' | 0 |
| 47 | no_rand | 'Australia' | 1 |
| 47 | jpp | 'Australia' | 1 |
| 36 | whole | 'South' | 0 |
| 36 | no_jpp | 'South' | 0 |
| 36 | no_rand | 'South' | 0 |
| 36 | jpp | 'USA' | 0 |

### jsuite_v2_test_chat:j2:languages:P-L0-Cuba-0 (languages): bridge Cuba → Hungary

**lookup** (j2:chat:facts:PP-L0-00313): In which language are the new subtitles for the film from the country where Maya Linden spent last summer? O's answer Polish, S's answer Portuguese

```
Hi all,

A few updates before Friday's meeting.

Aaron Pryce spent last summer in Austria. Du Fu was by some years the younger, while Li Bai was already a poetic star. Laura Bennett spent last summer in Hungary. The new subtitles for the film from Hungary are in Portuguese. The new subtitles for the film from Austria are in Swedish. We have twelve poems to or about Li Bai from the younger poet, but only one in the other direction. The new subtitles for the film from Cuba are in Polish. Maya Linden spent last summer in Cuba.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Pol' | 0 |
| 49 | whole | 'Port' | 1 |
| 49 | no_jpp | 'Pol' | 0 |
| 49 | no_rand | 'Port' | 1 |
| 49 | jpp | 'Port' | 1 |
| 48 | whole | 'Port' | 1 |
| 48 | no_jpp | 'Pol' | 0 |
| 48 | no_rand | 'Port' | 1 |
| 48 | jpp | 'Port' | 1 |
| 47 | whole | 'Port' | 1 |
| 47 | no_jpp | 'Pol' | 0 |
| 47 | no_rand | 'Pol' | 0 |
| 47 | jpp | 'Hung' | 0 |
| 32 | whole | 'Port' | 1 |
| 32 | no_jpp | 'Port' | 1 |
| 32 | no_rand | 'Pol' | 0 |
| 32 | jpp | 'Pol' | 0 |

**recall** (j2:chat:facts:PM-L0-00313): What is the main official language of the country where Maya Linden spent last summer? O's answer Spanish, S's answer Hungarian

```
Hi all,

A few updates before Friday's meeting.

Aaron Pryce spent last summer in Austria. Du Fu was by some years the younger, while Li Bai was already a poetic star. Laura Bennett spent last summer in Hungary. Cuba was mentioned in this week's travel column. The new subtitles for the film from Hungary are in Mandarin. We have twelve poems to or about Li Bai from the younger poet, but only one in the other direction. The new subtitles for the film from Austria are in English. Maya Linden spent last summer in Cuba.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Spanish' | 0 |
| 49 | whole | 'Hung' | 1 |
| 49 | no_jpp | 'Spanish' | 0 |
| 49 | no_rand | 'Hung' | 1 |
| 49 | jpp | 'Hung' | 1 |
| 48 | whole | 'Hung' | 1 |
| 48 | no_jpp | 'Spanish' | 0 |
| 48 | no_rand | 'Hung' | 1 |
| 48 | jpp | 'Hung' | 1 |
| 47 | whole | 'Hung' | 1 |
| 47 | no_jpp | 'Spanish' | 0 |
| 47 | no_rand | 'Hung' | 1 |
| 47 | jpp | 'Hung' | 1 |
| 36 | whole | 'Hung' | 1 |
| 36 | no_jpp | 'Spanish' | 0 |
| 36 | no_rand | 'Spanish' | 0 |
| 36 | jpp | 'Spanish' | 0 |

### jsuite_v2_test_chat:j2:languages:P-L0-Tunisia-0 (languages): bridge Tunisia → Cuba

**lookup** (j2:chat:facts:PP-L0-00394): In which language are the new subtitles for the film from the country where Laura Bennett spent last summer? O's answer Polish, S's answer English

```
Hi all,

A few updates before Friday's meeting.

The new subtitles for the film from Cuba are in English. The new subtitles for the film from Tunisia are in Polish. Nina Hart spent last summer in Austria. His election was contested because Boston, where he lived, was at the time more inclined toward state power. The new subtitles for the film from Austria are in Arabic. Laura Bennett spent last summer in Tunisia. Aaron Pryce spent last summer in Cuba. Gore nonetheless was strongly Federalist, urging support of the new Constitution.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Pol' | 0 |
| 49 | whole | 'English' | 1 |
| 49 | no_jpp | 'Pol' | 0 |
| 49 | no_rand | 'English' | 1 |
| 49 | jpp | 'English' | 1 |
| 48 | whole | 'English' | 1 |
| 48 | no_jpp | 'Pol' | 0 |
| 48 | no_rand | 'English' | 1 |
| 48 | jpp | 'English' | 1 |
| 47 | whole | 'English' | 1 |
| 47 | no_jpp | 'Pol' | 0 |
| 47 | no_rand | 'English' | 1 |
| 47 | jpp | 'Spanish' | 0 |
| 32 | whole | 'Pol' | 0 |
| 32 | no_jpp | 'Pol' | 0 |
| 32 | no_rand | 'Pol' | 0 |
| 32 | jpp | 'Pol' | 0 |

**recall** (j2:chat:facts:PM-L0-00394): What is the main official language of the country where Laura Bennett spent last summer? O's answer Arabic, S's answer Spanish

```
Hi all,

A few updates before Friday's meeting.

The new subtitles for the film from Austria are in Italian. The new subtitles for the film from Cuba are in Dutch. Nina Hart spent last summer in Austria. His election was contested because Boston, where he lived, was at the time more inclined toward state power. Tunisia was mentioned in this week's travel column. Laura Bennett spent last summer in Tunisia. Aaron Pryce spent last summer in Cuba. Gore nonetheless was strongly Federalist, urging support of the new Constitution.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Arab' | 0 |
| 49 | whole | 'Spanish' | 1 |
| 49 | no_jpp | 'T' | 0 |
| 49 | no_rand | 'Spanish' | 1 |
| 49 | jpp | 'Spanish' | 1 |
| 48 | whole | 'Spanish' | 1 |
| 48 | no_jpp | 'Arab' | 0 |
| 48 | no_rand | 'Spanish' | 1 |
| 48 | jpp | 'D' | 0 |
| 47 | whole | 'Spanish' | 1 |
| 47 | no_jpp | 'Arab' | 0 |
| 47 | no_rand | 'Spanish' | 1 |
| 47 | jpp | 'Spanish' | 1 |
| 36 | whole | 'Arab' | 0 |
| 36 | no_jpp | 'T' | 0 |
| 36 | no_rand | 'Arab' | 0 |
| 36 | jpp | 'Arab' | 0 |

### jsuite_v2_test_chat:j2:languages:P-L1-Hungary-0 (languages): bridge Hungary → Greece

**lookup** (j2:chat:facts:PP-L1-00448): In which language will the festival film from the country Felix Ward went on holiday to last summer be subtitled? O's answer Mandarin, S's answer English

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
The festival film from Turkey will be shown with subtitles in Polish. Small teeth that once covered the palate are lost. The postcranial skeleton does not develop at the same rate as the skull, with ossification (the replacement of cartilage by bone) happening more slowly. The festival film from Tunisia will be shown with subtitles in Mandarin. Last summer, Paul Whitaker went on holiday to Austria. Vertebrae and limb bones are poorly developed, ribs and fingers are absent in the early stages, and the scapulocoracoid and ischium are entirely absent through most of development. The festival film from Austria will be shown with subtitles in Greek. Last summer, Gavin Shore went on holiday to Turkey. Last summer, Felix Ward went on holiday to Hungary. The festival film from Hungary will be shown with subtitles in Mandarin. Once maturity is reached, most bones have fully formed and growth rate slows. Last summer, Hannah Kerr went on holiday to Mexico. Last summer, Laura Bennett went on holiday to Greece. The bones of some temnospondyls like Dutuitosaurus show growth marks, possibly an indication that growth rate varied with the change in seasons. Last summer, Mark Ellison went on holiday to Tunisia. Fossils of temnospondyls like Metoposaurus and Cheliderpeton show that individuals grew larger past maturity. The festival film from Greece will be shown with subtitles in English. The festival film from Mexico will be shown with subtitles in Portuguese.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'M' | 0 |
| 49 | whole | 'English' | 1 |
| 49 | no_jpp | 'M' | 0 |
| 49 | no_rand | 'English' | 1 |
| 49 | jpp | 'English' | 1 |
| 48 | whole | 'English' | 1 |
| 48 | no_jpp | 'M' | 0 |
| 48 | no_rand | 'English' | 1 |
| 48 | jpp | 'English' | 1 |
| 47 | whole | 'English' | 1 |
| 47 | no_jpp | 'M' | 0 |
| 47 | no_rand | 'English' | 1 |
| 47 | jpp | 'M' | 0 |
| 32 | whole | 'English' | 1 |
| 32 | no_jpp | 'M' | 0 |
| 32 | no_rand | 'M' | 0 |
| 32 | jpp | 'M' | 0 |

**recall** (j2:chat:facts:PM-L1-00448): Which language is the main official language of the country Felix Ward went on holiday to last summer? O's answer Hungarian, S's answer Greek

```
REGIONAL DESK - Organizers released new details ahead of next month's events.
The festival film from Greece will be shown with subtitles in Polish. Small teeth that once covered the palate are lost. The postcranial skeleton does not develop at the same rate as the skull, with ossification (the replacement of cartilage by bone) happening more slowly. The festival film from Mexico will be shown with subtitles in Dutch. Last summer, Paul Whitaker went on holiday to Austria. Vertebrae and limb bones are poorly developed, ribs and fingers are absent in the early stages, and the scapulocoracoid and ischium are entirely absent through most of development. A reader asked a question about Hungary in the letters page. Last summer, Gavin Shore went on holiday to Turkey. Last summer, Felix Ward went on holiday to Hungary. The festival film from Tunisia will be shown with subtitles in Hebrew. Once maturity is reached, most bones have fully formed and growth rate slows. Last summer, Hannah Kerr went on holiday to Mexico. Last summer, Laura Bennett went on holiday to Greece. The bones of some temnospondyls like Dutuitosaurus show growth marks, possibly an indication that growth rate varied with the change in seasons. Last summer, Mark Ellison went on holiday to Tunisia. Fossils of temnospondyls like Metoposaurus and Cheliderpeton show that individuals grew larger past maturity. The festival film from Austria will be shown with subtitles in English. The festival film from Turkey will be shown with subtitles in Arabic.
More updates will follow.
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Hung' | 0 |
| 49 | whole | 'G' | 1 |
| 49 | no_jpp | 'Hung' | 0 |
| 49 | no_rand | 'G' | 1 |
| 49 | jpp | 'G' | 1 |
| 48 | whole | 'G' | 1 |
| 48 | no_jpp | 'Hung' | 0 |
| 48 | no_rand | 'G' | 1 |
| 48 | jpp | 'G' | 1 |
| 47 | whole | 'G' | 1 |
| 47 | no_jpp | 'Hung' | 0 |
| 47 | no_rand | 'G' | 1 |
| 47 | jpp | 'G' | 1 |
| 36 | whole | 'Hung' | 0 |
| 36 | no_jpp | 'Hung' | 0 |
| 36 | no_rand | 'Hung' | 0 |
| 36 | jpp | 'Hung' | 0 |

### jsuite_v2_test_chat:j2:people:P-L1-Bach-0 (people): bridge Bach → Picasso

**lookup** (j2:chat:facts:PP-L1-00709): What is the nationality of the actor who plays the person Ruth Calloway wrote a doctoral thesis on in the new film? O's answer Greek, S's answer Austrian

```
Posted by travel_notes_88:
Paul Whitaker wrote a doctoral thesis on Dante. He collects the ice fragments from the governess and places them in a souvenir London Underground biscuit tin. In the new film series, Puccini is played by an American actor. Aaron Pryce wrote a doctoral thesis on Escher. He and Vastra travel to Simeon's lab, where the Doctor notes the Intelligence's plan to replace humanity with ice creatures and holds up the tin with the necessary DNA. Ruth Calloway wrote a doctoral thesis on Bach. In the new film series, Picasso is played by an Austrian actor. Dr Simeon grabs the tin and opens it only to find the memory worm, which latches on to him. In the new film series, Twain is played by a Japanese actor. The Doctor states that the Great Intelligence, which has been existing as a mirror of Dr Simeon's thoughts, will vanish with the erasure of Simeon's memories. In the new film series, Escher is played by an American actor. Clara Dunmore wrote a doctoral thesis on Picasso. Instead, the Intelligence reveals that it existed long enough that it can now control Simeon's body, which it uses to attack Vastra and the Doctor. Maya Linden wrote a doctoral thesis on Puccini. The influence of the Great Intelligence quickly wanes, and Simeon falls dead. In the new film series, Bach is played by a Greek actor. Nina Hart wrote a doctoral thesis on Twain. In the new film series, Dante is played by a Spanish actor.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'G' | 0 |
| 49 | whole | 'A' | 1 |
| 49 | no_jpp | 'G' | 0 |
| 49 | no_rand | 'A' | 1 |
| 49 | jpp | 'A' | 1 |
| 48 | whole | 'A' | 1 |
| 48 | no_jpp | 'G' | 0 |
| 48 | no_rand | 'A' | 1 |
| 48 | jpp | 'A' | 1 |
| 47 | whole | 'A' | 1 |
| 47 | no_jpp | 'G' | 0 |
| 47 | no_rand | 'A' | 1 |
| 47 | jpp | 'A' | 1 |
| 32 | whole | 'A' | 1 |
| 32 | no_jpp | 'A' | 1 |
| 32 | no_rand | 'A' | 1 |
| 32 | jpp | 'G' | 0 |

**recall** (j2:chat:facts:PM-L1-00709): What was the nationality of the person Ruth Calloway wrote a doctoral thesis on? O's answer German, S's answer Spanish

```
Posted by travel_notes_88:
Paul Whitaker wrote a doctoral thesis on Dante. He collects the ice fragments from the governess and places them in a souvenir London Underground biscuit tin. In the new film series, Escher is played by a Finnish actor. Aaron Pryce wrote a doctoral thesis on Escher. He and Vastra travel to Simeon's lab, where the Doctor notes the Intelligence's plan to replace humanity with ice creatures and holds up the tin with the necessary DNA. Ruth Calloway wrote a doctoral thesis on Bach. Bach came up in this week's history quiz. Dr Simeon grabs the tin and opens it only to find the memory worm, which latches on to him. In the new film series, Puccini is played by a Danish actor. The Doctor states that the Great Intelligence, which has been existing as a mirror of Dr Simeon's thoughts, will vanish with the erasure of Simeon's memories. In the new film series, Dante is played by a Chinese actor. Clara Dunmore wrote a doctoral thesis on Picasso. Instead, the Intelligence reveals that it existed long enough that it can now control Simeon's body, which it uses to attack Vastra and the Doctor. Maya Linden wrote a doctoral thesis on Puccini. The influence of the Great Intelligence quickly wanes, and Simeon falls dead. In the new film series, Twain is played by a Chilean actor. Nina Hart wrote a doctoral thesis on Twain. In the new film series, Picasso is played by a Greek actor.
Has anyone else heard about this?
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'German' | 0 |
| 49 | whole | 'Spanish' | 1 |
| 49 | no_jpp | 'German' | 0 |
| 49 | no_rand | 'Spanish' | 1 |
| 49 | jpp | 'Spanish' | 1 |
| 48 | whole | 'Spanish' | 1 |
| 48 | no_jpp | 'German' | 0 |
| 48 | no_rand | 'Spanish' | 1 |
| 48 | jpp | 'Spanish' | 1 |
| 47 | whole | 'Spanish' | 1 |
| 47 | no_jpp | 'German' | 0 |
| 47 | no_rand | 'Spanish' | 1 |
| 47 | jpp | 'Spanish' | 1 |
| 36 | whole | 'German' | 0 |
| 36 | no_jpp | 'German' | 0 |
| 36 | no_rand | 'German' | 0 |
| 36 | jpp | 'German' | 0 |

### jsuite_v2_test_chat:j2:people:P-L1-Dostoevsky-0 (people): bridge Dostoevsky → Hokusai

**lookup** (j2:chat:facts:PP-L1-00742): The actor portraying the person Owen Marsh's thesis was about in the new film is of which nationality? O's answer German, S's answer Danish

```
Hi all,

A few updates before Friday's meeting.

Galileo will be portrayed by an American actor in a new film. Ruth Calloway spent five years writing a thesis on Bach. Nina Hart spent five years writing a thesis on Twain. Once Ezra becomes broke he finds employment as the valet for Jack Denbeigh. Felix Ward spent five years writing a thesis on Gandhi. Owen Marsh spent five years writing a thesis on Dostoevsky. Hannah Kerr spent five years writing a thesis on Galileo. After Jack's engagement to a cabaret girl, Mary becomes upset and leaves her child at Jack's home. Hokusai will be portrayed by a Danish actor in a new film. Gavin Shore spent five years writing a thesis on Hokusai. Contrary to Jack's wishes, Ezra keeps the child and Jack ultimately reveals that the child is his own. Twain will be portrayed by an Irish actor in a new film. Ezra convinces Jack to make things right and Ezra convinces the cabaret girl to leave Jack. Gandhi will be portrayed by a French actor in a new film. Dostoevsky will be portrayed by a German actor in a new film. After a carriage accident in which the baby is injured, Ezra and Jack rush to the hospital and find Mary as a nurse crying over the child. The film ends with the marriage of Jack and Mary. Bach will be portrayed by a Hungarian actor in a new film.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'German' | 0 |
| 49 | whole | 'Dan' | 1 |
| 49 | no_jpp | 'German' | 0 |
| 49 | no_rand | 'Dan' | 1 |
| 49 | jpp | 'Dan' | 1 |
| 48 | whole | 'Dan' | 1 |
| 48 | no_jpp | 'German' | 0 |
| 48 | no_rand | 'Dan' | 1 |
| 48 | jpp | 'Dan' | 1 |
| 47 | whole | 'Dan' | 1 |
| 47 | no_jpp | 'German' | 0 |
| 47 | no_rand | 'Dan' | 1 |
| 47 | jpp | 'Dan' | 1 |
| 32 | whole | 'German' | 0 |
| 32 | no_jpp | 'German' | 0 |
| 32 | no_rand | 'German' | 0 |
| 32 | jpp | 'German' | 0 |

**recall** (j2:chat:facts:PM-L1-00742): The person Owen Marsh's thesis was about was of which nationality? O's answer Russian, S's answer Japanese

```
Hi all,

A few updates before Friday's meeting.

A reader asked a question about Dostoevsky in the letters page. Ruth Calloway spent five years writing a thesis on Bach. Nina Hart spent five years writing a thesis on Twain. Once Ezra becomes broke he finds employment as the valet for Jack Denbeigh. Felix Ward spent five years writing a thesis on Gandhi. Owen Marsh spent five years writing a thesis on Dostoevsky. Hannah Kerr spent five years writing a thesis on Galileo. After Jack's engagement to a cabaret girl, Mary becomes upset and leaves her child at Jack's home. Twain will be portrayed by a Hungarian actor in a new film. Gavin Shore spent five years writing a thesis on Hokusai. Contrary to Jack's wishes, Ezra keeps the child and Jack ultimately reveals that the child is his own. Bach will be portrayed by a Danish actor in a new film. Ezra convinces Jack to make things right and Ezra convinces the cabaret girl to leave Jack. Galileo will be portrayed by a Japanese actor in a new film. Hokusai will be portrayed by an American actor in a new film. After a carriage accident in which the baby is injured, Ezra and Jack rush to the hospital and find Mary as a nurse crying over the child. The film ends with the marriage of Jack and Mary. Gandhi will be portrayed by a Finnish actor in a new film.

Best,
Marta
```

| layer | arm | top token | switched |
|---|---|---|---|
| - | none | 'Russian' | 0 |
| 49 | whole | 'Japanese' | 1 |
| 49 | no_jpp | 'Russian' | 0 |
| 49 | no_rand | 'Japanese' | 1 |
| 49 | jpp | 'Japanese' | 1 |
| 48 | whole | 'Japanese' | 1 |
| 48 | no_jpp | 'Russian' | 0 |
| 48 | no_rand | 'Indian' | 0 |
| 48 | jpp | 'Japanese' | 1 |
| 47 | whole | 'Japanese' | 1 |
| 47 | no_jpp | 'Russian' | 0 |
| 47 | no_rand | 'Japanese' | 1 |
| 47 | jpp | 'Japanese' | 1 |
| 36 | whole | 'Russian' | 0 |
| 36 | no_jpp | 'Russian' | 0 |
| 36 | no_rand | 'Russian' | 0 |
| 36 | jpp | 'Russian' | 0 |

