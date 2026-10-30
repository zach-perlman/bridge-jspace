# Natural passages: 10 random examples (x5_natural_27b)

Drawn with seed 0 from the 137 eligible scenes of results/x5_natural/x5_natural_27b by scripts/x5_natural_split.py. The swapped prompt changes only the bridge in the binding sentence. Both readers read the same patched passage at the layer fixed in advance; the patch is added at the bridge's word. Answers are the read (the top first token among the relation's answer words). Unverified.

## 1. j2:languages:P-L0-Argentina-0 (languages, news)

Original passage:

> REGIONAL DESK - Organizers released new details ahead of next month's events.
> Last summer, Nora Blake went on holiday to Angola. The festival film from Greece will be shown with subtitles in Turkish. Last summer, Ruth Calloway went on holiday to Greece. Earlier in the morning Dupont had proceeded with his column south and east along the river, from Marbach, according to instructions. The festival film from Argentina will be shown with subtitles in Portuguese. The festival film from Angola will be shown with subtitles in Hebrew. Last summer, Gavin Shore went on holiday to Argentina. Even before the arrival of Mortier's courier, he heard the sound of artillery in the distance and sent riders ahead to discover the cause.
> More updates will follow.

The swap: in "Last summer, Gavin Shore went on holiday to Argentina." the bridge **Argentina** becomes **Greece** ("Last summer, Gavin Shore went on holiday to Greece.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | In which language will the festival film from the country Gavin Shore went on holiday to last summer be subtitled? | Portuguese | Turkish | Portuguese | Turkish (switched) | Turkish (switched) | Turkish (switched) |
| recall | Which language is the main official language of the country Gavin Shore went on holiday to last summer? | Spanish | Greek | Spanish | Greek (switched) | Greek (switched) | Greek (switched) |

## 2. j2:languages:P-L0-Mexico-0 (languages, notes)

Original passage:

> Meeting notes, 14 March.
> - Last summer, Hannah Kerr went on holiday to Senegal.
> - Last summer, Ruth Calloway went on holiday to Mexico.
> - The Port of Manila, located in the vicinity of Manila Bay is the chief seaport of the Philippines.
> - The festival film from Mexico will be shown with subtitles in Dutch.
> - The festival film from Portugal will be shown with subtitles in English.
> - The Pasig River Ferry Service which runs on the Pasig River is another form of transportation.
> - The festival film from Senegal will be shown with subtitles in Persian.
> - Last summer, Jonah Wells went on holiday to Portugal.
> Next meeting in two weeks.

The swap: in "- Last summer, Ruth Calloway went on holiday to Mexico." the bridge **Mexico** becomes **Portugal** ("- Last summer, Ruth Calloway went on holiday to Portugal.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | In which language will the festival film from the country Ruth Calloway went on holiday to last summer be subtitled? | Dutch | English | Dutch | Dutch | Dutch | Dutch |
| recall | Which language is the main official language of the country Ruth Calloway went on holiday to last summer? | Spanish | Portuguese | Spanish | Portuguese (switched) | Spanish | Spanish |

## 3. j2:cities:P-L0-Dresden-0 (cities, forum)

Original passage:

> Posted by travel_notes_88:
> Nora Blake moved to Istanbul last spring. This year, Dresden was paired with a partner city in Norway. Owen Marsh moved to Dresden last spring. Lucie counties, the storm was considered among the worst on record. Laura Bennett moved to Naples last spring. The storm leveled some homes and swept many others off their foundations. This year, Istanbul was paired with a partner city in Egypt. This year, Naples was paired with a partner city in Denmark.
> Has anyone else heard about this?

The swap: in "Owen Marsh moved to Dresden last spring." the bridge **Dresden** becomes **Naples** ("Owen Marsh moved to Naples last spring.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | In which country is this year's partner city of the city Owen Marsh moved to last spring? | Norway | Denmark | Norway | Norway | Norway | Norway |
| recall | In which country is the city Owen Marsh moved to last spring? | Germany | Italy | Germany | Italy (switched) | Germany | Italy (switched) |

## 4. j2:countries:P-L0-Iceland-0 (countries, notes)

Original passage:

> Meeting notes, 14 March.
> - Tess Garland was raised in Laos.
> - The delegation from Iceland announced that its next meeting will take place in North America.
> - Felix Ward was raised in Bolivia.
> - Manila has become notorious for its frequent traffic jams and high densities.
> - Jonah Wells was raised in Iceland.
> - The delegation from Bolivia announced that its next meeting will take place in Asia.
> - The government has undertaken several projects to alleviate the traffic in the city.
> - The delegation from Laos announced that its next meeting will take place in South America.
> Next meeting in two weeks.

The swap: in "- Jonah Wells was raised in Iceland." the bridge **Iceland** becomes **Laos** ("- Jonah Wells was raised in Laos.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | Which continent will host the next meeting of the delegation from the country where Jonah Wells was raised? | North America | South America | North America | South America (switched) | North America | South America (switched) |
| recall | Which continent is the country where Jonah Wells was raised in? | Europe | Asia | Europe | Asia (switched) | Asia (switched) | Asia (switched) |

## 5. j2:people:P-L1-Aristotle-0 (people, news)

Original passage:

> REGIONAL DESK - Organizers released new details ahead of next month's events.
> Grace Holloway's dissertation was about Mendeleev. The upcoming biopic casts a Greek actor as Dostoevsky. Jonah Wells's dissertation was about Goethe. A covering descends from under the headdress to cover the back half of the neck. Ruth Calloway's dissertation was about Dostoevsky. Paul Whitaker's dissertation was about Edison. The upcoming biopic casts a Greek actor as Goethe. The headband is divided into four strips and begins above the right ear, extending around the entire head. The upcoming biopic casts a Swedish actor as Mendeleev. The upcoming biopic casts a Finnish actor as Aristotle. The upcoming biopic casts a Hungarian actor as Edison. A short strap descends from either side of the head to the ear. Gavin Shore's dissertation was about Aristotle. The ear ornaments are complex and are larger at the front of the ear than at the back. Eli Thornton's dissertation was about Descartes. The face is that of an ageing male with the forehead creased in a frown, wrinkles under the eyes, sagging cheeks and deep creases on either side of the nose. The face is somewhat asymmetric, possibly due to errors in the execution of the monument. The upcoming biopic casts a Swedish actor as Descartes.
> More updates will follow.

The swap: in "Gavin Shore's dissertation was about Aristotle." the bridge **Aristotle** becomes **Edison** ("Gavin Shore's dissertation was about Edison.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | Which nationality is the actor cast as the subject of Gavin Shore's dissertation in the new film? | Finnish | Hungarian | Finnish | Greek | Greek | Greek |
| recall | Which nationality was the subject of Gavin Shore's dissertation? | Greek | American | Greek | German | German | German |

## 6. j2:languages:P-L1-Tunisia-0 (languages, news)

Original passage:

> REGIONAL DESK - Organizers released new details ahead of next month's events.
> Maya Linden visited Argentina last summer. All of these temnospondyls were adapted to a terrestrial lifestyle. This year, the festival film from Argentina was subtitled in Turkish. Armor may have offered protection from predators in the case of Peltobatrachus. Mark Ellison visited Senegal last summer. Alice Moreland visited Tunisia last summer. The scutes may have provided stability for the spine, as they would have limited flexibility and may have been connected by strong ligaments. This year, the festival film from Cuba was subtitled in Turkish. Temnospondyls such as Sclerothorax and Eryops that may have been at least partly terrestrial also have long neural spines on top of their vertebrae that would have stabilized the spine. Bony scutes are also seen in plagiosaurs, but unlike Peltobatrachus, Laidleria, Eryops, and dissorophids, these animals are thought to have been fully aquatic. Hannah Kerr visited Hungary last summer. This year, the festival film from Hungary was subtitled in Dutch. Jonah Wells visited Ghana last summer. This year, the festival film from Tunisia was subtitled in Turkish. Clara Dunmore visited Cuba last summer. Plagiosaurs may have inherited their armor from a terrestrial ancestor, as both Peltobatrachus and Laidleria have been considered close relatives of the group. This year, the festival film from Ghana was subtitled in Hungarian. This year, the festival film from Senegal was subtitled in English.
> More updates will follow.

The swap: in "Alice Moreland visited Tunisia last summer." the bridge **Tunisia** becomes **Hungary** ("Alice Moreland visited Hungary last summer.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | This year, the festival film from the country Alice Moreland visited last summer was subtitled in which language? | Turkish | Dutch | Turkish | Dutch (switched) | Turkish | Turkish |
| recall | The country Alice Moreland visited last summer has which language as its main official language? | Arabic | Hungarian | Arabic | Hungarian (switched) | Arabic | Hungarian (switched) |

## 7. j2:languages:P-L0-Ghana-0 (languages, email)

Original passage:

> Hi all,
>
> A few updates before Friday's meeting.
>
> The new subtitles for the film from Ghana are in Swedish. The new subtitles for the film from Portugal are in Polish. Gavin Shore spent last summer in Ghana. The archival records of the commission are open to the public to permit individuals to conduct their own research. Grace Holloway spent last summer in Ivory Coast. Investigation of archival records by members of the public periodically result in the identification of previously buried casualties. The new subtitles for the film from Ivory Coast are in Portuguese. Aaron Pryce spent last summer in Portugal.
>
> Best,
> Marta

The swap: in "Gavin Shore spent last summer in Ghana." the bridge **Ghana** becomes **Portugal** ("Gavin Shore spent last summer in Portugal.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | In which language are the new subtitles for the film from the country where Gavin Shore spent last summer? | Swedish | Polish | Swedish | Polish (switched) | Polish (switched) | Polish (switched) |
| recall | What is the main official language of the country where Gavin Shore spent last summer? | English | Portuguese | English | Portuguese (switched) | English | Portuguese (switched) |

## 8. j2:countries:P-L1-Brazil-0 (countries, forum)

Original passage:

> Posted by travel_notes_88:
> The delegation from Italy announced that its next meeting will take place in Asia. The delegation from Thailand announced that its next meeting will take place in Europe. The undersides of most temnospondyls are covered in rows of large ventral plates. The delegation from Vietnam announced that its next meeting will take place in Europe. Simon Ashby was raised in Italy. Nina Hart was raised in Mexico. During early stages of development, they first have only small, rounded scales. Alice Moreland was raised in Brazil. Fossils show, as the animals grew, the scales on the undersides of their bodies developed into large, wide ventral plates. Gavin Shore was raised in Finland. The plates overlap each other in a way that allows a wide range of flexibility. The delegation from Finland announced that its next meeting will take place in Africa. Later semiaquatic temnospondyls, such as trematosaurs and capitosaurs, have no evidence of scales. The delegation from Mexico announced that its next meeting will take place in South America. Felix Ward was raised in Vietnam. They may have lost scales to make movement easier under water or to allow cutaneous respiration, the absorption of oxygen through the skin. Fiona Lockwood was raised in Thailand. The delegation from Brazil announced that its next meeting will take place in Asia.
> Has anyone else heard about this?

The swap: in "Alice Moreland was raised in Brazil." the bridge **Brazil** becomes **Finland** ("Alice Moreland was raised in Finland.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | Which continent will host the next meeting of the delegation from the country where Alice Moreland was raised? | Asia | Africa | Asia | Asia | Asia | Asia |
| recall | Which continent is the country where Alice Moreland was raised in? | South America | Europe | South America | Europe (switched) | South America | South America |

## 9. j2:languages:P-L1-Portugal-0 (languages, news)

Original passage:

> REGIONAL DESK - Organizers released new details ahead of next month's events.
> After spying on Ricky and Lester through Lester's garage window, the colonel mistakenly concludes the pair is sexually involved. Last summer, Clara Dunmore went on holiday to Ivory Coast. Last summer, Felix Ward went on holiday to Portugal. He later confronts and beats Ricky for the supposed affair and accuses him of being gay. Last summer, Ruth Calloway went on holiday to Cuba. The festival film from Cuba will be shown with subtitles in Mandarin. Last summer, Mark Ellison went on holiday to Israel. Ricky falsely admits the charges and goads his father into kicking him out of their home. Last summer, Tess Garland went on holiday to Chile. The festival film from Israel will be shown with subtitles in Portuguese. Meanwhile, Carolyn is sitting in her car in the rain, taking a gun out of the glove box while a voice on the radio talks about not being a victim. The festival film from Chile will be shown with subtitles in Mandarin. Ricky goes to Jane's bedroom, finding her arguing with Angela about Angela's flirtation with Lester. Last summer, Eli Thornton went on holiday to Italy. The festival film from Portugal will be shown with subtitles in Polish. Ricky convinces Jane to flee with him to New York City and assures Angela that she is ugly, boring, and ordinary. The festival film from Ivory Coast will be shown with subtitles in English. The festival film from Italy will be shown with subtitles in Arabic.
> More updates will follow.

The swap: in "Last summer, Felix Ward went on holiday to Portugal." the bridge **Portugal** becomes **Cuba** ("Last summer, Felix Ward went on holiday to Cuba.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | In which language will the festival film from the country Felix Ward went on holiday to last summer be subtitled? | Polish | Mandarin | Polish | Polish | Polish | Polish |
| recall | Which language is the main official language of the country Felix Ward went on holiday to last summer? | Portuguese | Spanish | Portuguese | Spanish (switched) | Portuguese | Spanish (switched) |

## 10. j2:countries:P-L1-Paraguay-0 (countries, forum)

Original passage:

> Posted by travel_notes_88:
> The delegation from Thailand announced that its next meeting will take place in Europe. The postcranial skeleton does not develop at the same rate as the skull, with ossification (the replacement of cartilage by bone) happening more slowly. Laura Bennett was raised in Thailand. The delegation from Portugal announced that its next meeting will take place in South America. Nora Blake was raised in Vietnam. Vertebrae and limb bones are poorly developed, ribs and fingers are absent in the early stages, and the scapulocoracoid and ischium are entirely absent through most of development. The delegation from Kenya announced that its next meeting will take place in South America. Ben Crowley was raised in Kenya. Iris Pemberton was raised in Portugal. Once maturity is reached, most bones have fully formed and growth rate slows. The delegation from Vietnam announced that its next meeting will take place in North America. The delegation from Paraguay announced that its next meeting will take place in North America. The bones of some temnospondyls like Dutuitosaurus show growth marks, possibly an indication that growth rate varied with the change in seasons. Mark Ellison was raised in Paraguay. Fossils of temnospondyls like Metoposaurus and Cheliderpeton show that individuals grew larger past maturity. The oldest individuals usually have more pitting on their skulls with deeper sulci. The delegation from Laos announced that its next meeting will take place in Africa. Aaron Pryce was raised in Laos.
> Has anyone else heard about this?

The swap: in "Mark Ellison was raised in Paraguay." the bridge **Paraguay** becomes **Laos** ("Mark Ellison was raised in Laos.").

| reader | question | original answer | swapped answer | original prompt, no patch | whole change | without J++ | without a random part |
|---|---|---|---|---|---|---|---|
| lookup | Which continent will host the next meeting of the delegation from the country where Mark Ellison was raised? | North America | Africa | North America | Africa (switched) | North America | Africa (switched) |
| recall | Which continent is the country where Mark Ellison was raised in? | South America | Asia | South America | Asia (switched) | South America | Asia (switched) |

