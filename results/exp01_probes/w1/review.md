# exp01_probes / w1: review sheet

Prompts kept: 552 of 694.

## Kept prompts per entity (kept / written)

ant 6/7, apple 6/7, Australia 6/8, baseball 6/7, basketball 6/7, bear 6/7, beer 6/7, Belgium 7/8, bicycle 7/7, brain 7/7, Brazil 8/8, buffalo 6/7, butter 3/6, calcium 3/5, Canada 5/8, carbon 6/7, China 8/8, Christmas 5/8, Darwin 5/6, diamond 7/7, drums 6/7, eagle 6/6, Earth 5/8, Easter 4/7, Egypt 7/8, Einstein 5/6, elephant 6/7, England 7/8, Europa 6/7, France 8/8, Friday 5/6, Germany 7/8, gold 5/7, golf 7/8, grape 6/9, Greece 8/8, guitar 5/6, heart 6/7, honey 4/7, Hungary 6/8, India 8/8, iron 7/7, Italy 7/8, Japan 8/8, July 4/7, June 2/10, Jupiter 6/7, kidney 5/6, Lincoln 8/8, liver 7/7, lung 7/7, March 3/7, Mars 7/7, May 4/7, mercury 6/7, Mexico 8/8, Michigan 5/7, moon 8/8, Mozart 5/7, Napoleon 4/7, Newton 5/7, nitrogen 5/10, oak 4/5, owl 5/7, oxygen 6/7, pearl 4/5, Peru 7/8, Philadelphia 5/8, piano 3/5, pine 3/5, Poland 6/8, ruby 3/5, Russia 6/8, Saturn 4/7, Seattle 6/8, Shakespeare 7/8, silver 7/7, Singapore 5/8, snake 6/8, sodium 5/7, Spain 7/8, spider 7/7, stomach 6/6, summer 5/7, swan 5/8, Sweden 6/8, tennis 5/8, Thursday 3/6, train 6/7, trumpet 4/5, turtle 5/6, Vatican 7/8, Venus 7/7, violin 5/5, wine 6/7, winter 4/7, Wisconsin 5/7

## Random sample of 25 prompts (seed 0)

| entity | prompt | accepted | Qwen's greedy continuation | kept |
|---|---|---|---|---|
| mercury | Fact: Dental fillings made with the metal of old barometers are called | amalgam/amalgams | ` amalgam fillings.\nQuestion:` | yes |
| Napoleon | Fact: The emperor who crowned himself in Notre-Dame in 1804 is often wrongly said to have been | short | ` crowned by the Pope.\nQuestion:` | no |
| bear | Fact: Winnie-the-Pooh's best friend is a small pig called | Piglet | ` Piglet.\nQuestion: What is` | yes |
| guitar | Fact: The Les Paul electric instrument is made by | Gibson | ` Gibson.\nHypothesis: The` | yes |
| Russia | Fact: The man who has led the Kremlin since 2000 is Vladimir | Putin | ` Putin.\nQuestion: Who has led` | yes |
| piano | Fact: The person who adjusts the strings of Liszt's instrument is a | tuner | ` luthier.\nQuestion: Who` | no |
| moon | Fact: The first person to walk on the lunar surface was Neil | Armstrong | ` Armstrong.\nQuestion: Who was the` | yes |
| Italy | Fact: The tiny republic surrounded by Emilia-Romagna and Marche is San | Marino | ` Marino.\nQuestion: What is the` | yes |
| Philadelphia | Fact: The Major League team that plays at Citizens Bank Park is the | Phillies | ` Philadelphia Phillies.\nQuestion: Which Major` | no |
| lung | Fact: The muscle below the breathing organs that helps us inhale is the | diaphragm | ` diaphragm.\nQuestion: The` | yes |
| stomach | Fact: The gastric organ empties food into the small | intestine | ` intestine.\nQuestion: The stomach empt` | yes |
| Germany | Fact: The region of cuckoo clocks in Baden-Württemberg is the Black | Forest | ` Forest.\nQuestion: The Black Forest` | yes |
| Russia | Fact: The title of the rulers of the Romanov dynasty before 1917 was | tsar/czar/Tsar/Czar | ` Emperor of All the Russias.\n` | no |
| drums | Fact: The percussion kit of Ringo Starr includes metal plates called | cymbals | ` cymbals.\nQuestion: Which` | yes |
| India | Fact: The white marble mausoleum in Agra built by Shah Jahan is the Taj | Mahal | ` Mahal.\nQuestion: The Taj` | yes |
| drums | Fact: The large bass part of the percussion kit is played with a foot | pedal | ` pedal.\nHypothesis: The` | yes |
| calcium | Fact: Eggshells and seashells are made mostly of the carbonate of the metal found in | chalk/limestone | ` the periodic table in group 2,` | no |
| Thursday | Fact: The US holiday held on the weekday of Thor in late November is | Thanksgiving | ` Thanksgiving.\nQuestion: The US holiday` | yes |
| Greece | Fact: The poet of the Iliad and the Odyssey was | Homer | ` Homer.\nQuestion: Who wrote the` | yes |
| Shakespeare | Fact: The writer of A Midsummer Night's Dream was born in Stratford-upon- | Avon | ` Avon.\nQuestion: Who was` | yes |
| Sweden | Fact: The prizes awarded every December in the capital of the land of IKEA are named after Alfred | Nobel | ` Nobel.\nQuestion: What is the` | yes |
| eagle | Fact: The bird of prey sacred to Zeus carried off the Trojan boy | Ganymede | ` Ganymede to Olympus.\nQuestion` | yes |
| Japan | Fact: The rice wine often served warm with sushi is called | sake | ` sake.\nQuestion: Which of the` | yes |
| Canada | Fact: The waterfalls on the border between New York State and Ontario are called | Niagara | ` the Niagara Falls.\nHypothesis` | no |
| Brazil | Fact: The giant statue of Christ the Redeemer looks down on the city of Rio de | Janeiro | ` Janeiro, Brazil.\nQuestion: Which` | yes |

## Every rejected prompt

- ant: Fact: In Aesop's fable, the hardworking insect that stored food all summer was contrasted with the lazy -> `insect that sang all summer.
Question` (accepted grasshopper)
- apple: Fact: The alcoholic drink made from fermented Granny Smith juice is -> `called cider.
Question: What is` (accepted cider)
- Australia: Fact: The giant sandstone monolith in the Northern Territory is -> `the largest rock in the world.` (accepted Uluru/Ayers)
- Australia: Fact: The hemisphere of Perth and Melbourne is the -> `same.
Question: Which of the` (accepted Southern)
- baseball: Fact: The leather glove worn by a catcher is called a -> `catcher's mitt.
Question: What` (accepted mitt)
- basketball: Fact: The team from Boston in the sport of Larry Bird is the -> `Boston Celtics.
Question: The team` (accepted Celtics)
- bear: Fact: The girl who ate the porridge in the house of three furry animals was -> `a little girl.
Question: What` (accepted Goldilocks)
- beer: Fact: The plant whose flowers give the bitter taste to lager and ale is -> `the hop.
Question: Which of` (accepted hops)
- Belgium: Fact: The fried potatoes sold in paper cones in Liège are called -> `"pommes frites" in French` (accepted fries/frites)
- buffalo: Fact: The shaggy animal of the American prairie is a close relative of domestic -> `cats.
Hypothesis: The` (accepted cattle/cows)
- butter: Fact: The sauce of egg yolks and melted churned cream served on eggs Benedict is -> `called Hollandaise sauce.
Question:` (accepted hollandaise)
- butter: Fact: The plant-based substitute for churned cream fat is -> `called margarine.
Question: Which` (accepted margarine)
- butter: Fact: The Irish brand of grass-fed churned dairy fat is -> `called butter.
Question: What is` (accepted Kerrygold)
- calcium: Fact: The metal of chalk and limestone is an alkaline earth metal, like magnesium and -> `calcium.
Question: Which of the` (accepted strontium/barium)
- calcium: Fact: Eggshells and seashells are made mostly of the carbonate of the metal found in -> `the periodic table in group 2,` (accepted chalk/limestone)
- Canada: Fact: The police of Alberta and Manitoba who ride horses are nicknamed the -> `“Royal Canadian Mounted Police” or “` (accepted Mounties)
- Canada: Fact: The waterfalls on the border between New York State and Ontario are called -> `the Niagara Falls.
Hypothesis` (accepted Niagara)
- Canada: Fact: The dish of fries topped with cheese curds and gravy that comes from Quebec is -> `called poutine.
Question: What` (accepted poutine)
- carbon: Fact: The element of soot and charcoal is in the same group of the periodic table as -> `the element of diamond.
Hypo` (accepted silicon)
- Christmas: Fact: The reindeer with a red nose who guides Santa's sleigh is -> `named Rudolph.
Question: What` (accepted Rudolph)
- Christmas: Fact: The season of preparation before the nativity feast, with a calendar of little doors, is -> `called Advent.
Question: What is` (accepted Advent)
- Christmas: Fact: The traditional roast bird of the British nativity feast is -> `the goose.
The goose is a` (accepted turkey/goose)
- Darwin: Fact: The Beagle naturalist married his cousin Emma -> `Hartwood.
Hypothesis:` (accepted Wedgwood)
- drums: Fact: The steel percussion instruments made from oil barrels come from -> `the Caribbean.
Hypothesis:` (accepted Trinidad)
- Earth: Fact: The planet we live on travels around the Sun once every -> `365 days.
Question` (accepted year)
- Earth: Fact: The planet humans live on turns once on its axis every -> `24 hours.
Question:` (accepted day)
- Earth: Fact: The force that pulls us to the ground of our world is -> `called gravity.
Question: The force` (accepted gravity)
- Easter: Fact: The animal that brings chocolate eggs at the feast of the resurrection is the -> `Easter Bunny.
Question: The Easter` (accepted bunny/rabbit/hare)
- Easter: Fact: The feast of the resurrection is preceded by forty days of -> `fasting.
Question: The feast of` (accepted Lent)
- Easter: Fact: The painted objects that children hunt for on Resurrection Sunday are -> `called Easter eggs.
Question: The` (accepted eggs)
- Egypt: Fact: The ancient lighthouse called the Pharos stood in the city founded by Alexander the Great, -> `which is now in Egypt.
Question` (accepted Alexandria)
- Einstein: Fact: The physicist of E equals mc squared spent his last years at -> `the Institute for Advanced Study in Princeton,` (accepted Princeton)
- elephant: Fact: The tusked giant is said never to -> `have been seen by humans.
Question` (accepted forget)
- England: Fact: The prehistoric stone circle on Salisbury Plain is -> `called Stonehenge.
Question:` (accepted Stonehenge)
- Europa: Fact: The princess abducted by Zeus as a bull bore him a son who became King -> `of Crete.
Question: Who` (accepted Minos)
- Friday: Fact: The day of Islamic congregational prayer is followed by -> `the day of the week on which the` (accepted Saturday)
- Germany: Fact: The famous autumn festival of Bavaria with lederhosen and steins is -> `called Oktoberfest.
Question: What` (accepted Oktoberfest)
- gold: Fact: The purity of the metal of Olympic first prizes is measured in -> `parts per million.
Question: The` (accepted karats/carats)
- gold: Fact: The king who turned everything he touched into the metal of Fort Knox was -> `King Midas.
Question: Which` (accepted Midas)
- golf: Fact: The sport of Tiger Woods is played on a -> `golf course.
Question: Tiger Woods` (accepted course)
- grape: Fact: The fruit that grows in bunches becomes, when dried, a -> `sweet, chewy snack.
H` (accepted raisin)
- grape: Fact: The bunches of fruit that the fox could not reach in Aesop's fable were called -> `grapes.
Question: The fox could` (accepted sour)
- grape: Fact: Botanically, the bunch-growing fruit of Concord jelly is a -> `grape.
Question: What is the` (accepted berry)
- guitar: Fact: The metal strips on the neck of the flamenco instrument are called -> `"fret".
Question: What` (accepted frets)
- heart: Fact: The left and right atria sit above the -> `left and right ventricles.` (accepted ventricles)
- honey: Fact: The sweet syrup made from nectar is stored in six-sided cells of -> `a honeycomb.
Hypothesis` (accepted wax/beeswax)
- honey: Fact: The sweet sticky food made in hives never -> `gets old.
Hypothesis:` (accepted spoils/rots/expires/goes)
- honey: Fact: The sweetener of hives is often stirred into -> `hot water to make tea.
Question` (accepted tea)
- Hungary: Fact: The currency of the country of Lake Balaton is the -> `Hungarian forint.
Question: What is` (accepted forint)
- Hungary: Fact: The national dish of the land of the forint, a beef stew, is -> `called goulash.
Question:` (accepted goulash)
- Italy: Fact: The Renaissance city of the Medici, where Michelangelo's David stands, is -> `a major tourist destination.
Question:` (accepted Florence)
- July: Fact: The month in which the United States celebrates Independence Day is followed by -> `the month in which the United States celebrates` (accepted August)
- July: Fact: The zodiac sign of a person born on American Independence Day is -> `Leo.
Question: What is the` (accepted Cancer)
- July: Fact: The month when Neil Armstrong first walked on the lunar surface comes right before -> `the month when the first human heart transplant` (accepted August)
- June: Fact: The month of D-Day, the Normandy landings, has thirty -> `-one days.
Question: Which month` (accepted days)
- June: Fact: The month of D-Day is named after the Roman goddess -> `of the hunt.
Question: What` (accepted Juno)
- June: Fact: The zodiac sign of someone born in the first week of the month of Father's Day is -> `Cancer.
Question: What is the` (accepted Gemini)
- June: Fact: The zodiac sign that begins around the 21st of the month of the northern solstice is -> `Capricorn.
Question: What` (accepted Cancer)
- June: Fact: The month in which Pride is celebrated in America contains the northern -> `hemisphere's summer solstice.
H` (accepted solstice)
- June: Fact: The month of Father's Day in America is the most popular month for -> `men to die.
Question: What` (accepted weddings)
- June (top-up): Fact: The month of the summer solstice in the Northern Hemisphere is named after the Roman goddess -> `of the sun.
Question: What` (accepted Juno)
- June (top-up): Fact: The month of the goddess Juno has -> `been named June.
Question: Which` (accepted 30/thirty)
- Jupiter: Fact: The largest moon of the biggest planet is -> `called Ganymede.
Question:` (accepted Ganymede)
- kidney: Fact: Painful hard deposits in the renal system are called -> `kidney stones.
Question: Painful` (accepted stones)
- March: Fact: The month in which St. Patrick's Day is celebrated comes right after -> `the month in which Groundhog Day is` (accepted February)
- March: Fact: The month of the northern spring equinox is followed by -> `the month of the northern summer solstice` (accepted April)
- March: Fact: The zodiac sign of someone born in the first week of the month of St. Patrick's Day is -> `Aries.
Question: What is` (accepted Pisces)
- March: Fact: The month of International Women's Day comes right before -> `the month of Earth Day.
Question` (accepted April)
- May: Fact: The month whose first day is International Workers' Day comes right after -> `the month whose first day is Mother's` (accepted April)
- May: Fact: In the Southern Hemisphere, the month of the Kentucky Derby falls in the season of -> `summer.
Question: In the Southern` (accepted autumn/fall)
- May: Fact: The month of the Chelsea Flower Show is named after the goddess -> `of flowers.
Question: Which month` (accepted Maia)
- mercury: Fact: The ore from which the metal of thermometers is extracted is -> `called cinnabar.
Question:` (accepted cinnabar)
- Michigan: Fact: The capital of the state of Ann Arbor and Grand Rapids is -> `Michigan.
Question: What is the` (accepted Lansing)
- Michigan: Fact: The bridge across the Straits joining the two peninsulas of the state of Detroit is the -> `longest bridge in the world.
Question` (accepted Mackinac)
- Mozart: Fact: The composer of The Marriage of Figaro left unfinished his -> `opera Don Giovanni.
Hypothesis` (accepted Requiem)
- Mozart: Fact: The composer of Eine kleine Nachtmusik was taught music by his father -> `.
Hypothesis: The composer` (accepted Leopold)
- Napoleon: Fact: The emperor who crowned himself in Notre-Dame in 1804 is often wrongly said to have been -> `crowned by the Pope.
Question:` (accepted short)
- Napoleon: Fact: The first wife of the emperor crowned in 1804 was -> `Marie Antoinette.
Question:` (accepted Josephine/Joséphine)
- Napoleon: Fact: The emperor exiled to Elba won a famous victory in 1805 at -> `the Battle of Austerlitz.` (accepted Austerlitz)
- Newton: Fact: The scientist who described the three laws of motion wrote his Principia in -> `1687.
Question` (accepted Latin)
- Newton: Fact: The scientist who built the first reflecting telescope became master of the Royal -> `Society in 1703.` (accepted Mint)
- nitrogen: Fact: The element with symbol N is in group 15 of the periodic table with -> `5 valence electrons.
Question` (accepted phosphorus)
- nitrogen: Fact: The element that bacteria in the root nodules of peas fix from the air is turned into -> `a compound that is used by the plant` (accepted ammonia)
- nitrogen: Fact: The element that boils at minus 196 degrees Celsius is used by doctors to freeze -> `tumors.
Question: What is the` (accepted warts/skin)
- nitrogen: Fact: Bags of crisps are filled with an inert element whose symbol is -> `Ar. What is the name of this` (accepted N)
- nitrogen (top-up): Fact: In the periodic table, the element directly below the gas fixed by legume root nodules is -> `a metalloid.
Question: Which` (accepted phosphorus/P)
- oak: Fact: The mighty tree of the English proverb that grows from a little seed is a symbol of -> `the power of small beginnings.
The` (accepted strength)
- owl: Fact: In the Harry Potter books, Hedwig delivers -> `a letter to Harry.
Question:` (accepted mail/letters/post)
- owl: Fact: A group of the birds of Athena is called a -> `wisdom.
Question: What is a` (accepted parliament)
- oxygen: Fact: The molecule of three atoms of the element in divers' tanks is -> `oxygen.
Question: Which of the` (accepted ozone)
- pearl: Fact: The gems of molluscs that are grown on farms are called -> `pearls.
Question: The gems of` (accepted cultured)
- Peru: Fact: The dish of raw fish cured in lime juice, famous in the land of Machu Picchu, is -> `called ceviche.
Question: Which` (accepted ceviche)
- Philadelphia: Fact: The boxer who ran up the steps of the art museum in the 1976 film was -> `a real boxer.
Question: Which` (accepted Rocky)
- Philadelphia: Fact: The Major League team that plays at Citizens Bank Park is the -> `Philadelphia Phillies.
Question: Which Major` (accepted Phillies)
- Philadelphia: Fact: The NBA team of the city of Independence Hall is the -> `Philadelphia 76ers.
H` (accepted 76ers/Sixers)
- piano: Fact: The instrument of Chopin's nocturnes replaced the older plucked instrument called the -> `harp.
Hypothesis:` (accepted harpsichord)
- piano: Fact: The person who adjusts the strings of Liszt's instrument is a -> `luthier.
Question: Who` (accepted tuner)
- pine: Fact: The needled evergreen whose sap makes turpentine produces a sticky -> `substance called resin.
Hypothesis` (accepted resin/sap)
- pine: Fact: The fresh scent of the needled tree is used in cleaning products for its -> `antibacterial properties.
Hypothesis` (accepted fragrance/scent/smell/aroma)
- Poland: Fact: The currency of the country of Kraków and Gdańsk is the -> `Polish złoty.
Question: What` (accepted zloty/złoty)
- Poland: Fact: The trade union founded by Lech Wałęsa at the Gdańsk shipyard was -> `called Solidarity.
Question: What` (accepted Solidarity)
- ruby: Fact: Dorothy's slippers in the film of The Wizard of Oz are made of a gem that is the same mineral as -> `ruby.
Question: What color are` (accepted sapphire/sapphires)
- ruby: Fact: The precious corundum coloured by chromium is the gem of wedding anniversary number -> `19.
Question: What` (accepted 40/forty)
- Russia: Fact: The title of the rulers of the Romanov dynasty before 1917 was -> `Emperor of All the Russias.` (accepted tsar/czar/Tsar/Czar)
- Russia: Fact: The alphabet used to write the language of Tolstoy and Pushkin is -> `the Cyrillic alphabet.
Question:` (accepted Cyrillic)
- Saturn: Fact: The NASA probe that orbited the gas giant of Titan from 2004 to 2017 was -> `named after a French mathematician and astronom` (accepted Cassini)
- Saturn: Fact: The planet of the moon Enceladus is made mostly of -> `ice.
Hypothesis: The` (accepted hydrogen)
- Saturn: Fact: The next planet out from the Sun after the planet of Titan is -> `Saturn.
Hypothesis: Saturn` (accepted Uranus)
- Seattle: Fact: The coffee chain that opened its first store at Pike Place Market in 1971 is -> `now the largest coffeehouse chain in the` (accepted Starbucks)
- Seattle: Fact: The NFL team of the Emerald City of the Pacific Northwest is the -> `Seattle Seahawks.
Question: The NFL` (accepted Seahawks)
- Shakespeare: Fact: In The Tempest, the exiled magician duke is -> `named Prospero.
Question: What` (accepted Prospero)
- Singapore: Fact: The lion-headed fish statue at Marina Bay is the -> `symbol of Singapore.
A. True` (accepted Merlion)
- Singapore: Fact: The country just across the Johor Strait is -> `Singapore.
Question: What is the` (accepted Malaysia)
- Singapore: Fact: The airport of the island nation of the Merlion is -> `Singapore Changi Airport.
Question:` (accepted Changi)
- snake: Fact: The hooded reptile charmed by flute players in street markets is the -> `Indian cobra.
Question: Which of` (accepted cobra)
- snake: Fact: The reptile that bit Cleopatra was a deadly -> `snake.
Hypothesis: Cle` (accepted asp/cobra/viper)
- sodium: Fact: The soft metal that explodes in water is in the same alkali group as -> `sodium.
Hypothesis: The` (accepted potassium/lithium)
- sodium: Fact: The orange glow of old street lamps comes from the vapour of the metal of -> `which element?

<think>
Here's` (accepted salt)
- Spain: Fact: The Andalusian art of song and dance performed with clapping and castanets is -> `called flamenco.
Question: What` (accepted flamenco)
- summer: Fact: In the north, the season of beach holidays and long days follows -> `the season of snow and ice.` (accepted spring)
- summer: Fact: The longest day of the year in the north is called the -> `summer solstice.
Question: The` (accepted solstice)
- swan: Fact: The baby of the bird that the ugly duckling became is called a -> `chick.
Question: Which bird is` (accepted cygnet)
- swan: Fact: The graceful water birds of Western Australia are famous for being -> `able to fly in formation.
H` (accepted black)
- swan: Fact: The male of the bird into which the ugly duckling grew is called a -> `swan.
Question: The male` (accepted cob)
- Sweden: Fact: The western neighbour of the land of Volvo and IKEA is -> `Denmark.
Question: Which country is` (accepted Norway)
- Sweden: Fact: The region made up of the land of IKEA together with Norway and Denmark is -> `called Scandinavia.
Question: Which` (accepted Scandinavia)
- tennis: Fact: In the sport of Roger Federer, a score of zero is called -> `a love.
Question: What is` (accepted love)
- tennis: Fact: A score of forty-all in the sport of Novak Djokovic is called -> `a deuce.
Question: What` (accepted deuce)
- tennis: Fact: The version of the sport of the Williams sisters played by four players is -> `called doubles.
Question: The version` (accepted doubles)
- Thursday: Fact: The day that takes its name from Thor comes right after -> `the day that takes its name from W` (accepted Wednesday)
- Thursday: Fact: Counting Sunday as the first day, the day of Thor is day number -> `4.
Question: What is` (accepted 5/five)
- Thursday: Fact: The French name for the weekday of Thor is -> `Thursday.
Question: What is the` (accepted jeudi)
- train: Fact: Railway carriages run on two steel -> `wheels, which are mounted on a single` (accepted rails/tracks)
- trumpet: Fact: Louis Armstrong's instrument is in the same family as the trombone and the -> `trumpet.
Question: Which of the` (accepted tuba/horn/French)
- turtle: Fact: The leader of the four cartoon ninja reptiles named after Renaissance artists is -> `Splinter.
Question: Which of` (accepted Leonardo)
- Vatican: Fact: The guards of the papal palace come from -> `the Swiss Guard.
Question: The` (accepted Switzerland)
- wine: Fact: The drink of Bordeaux and Burgundy is made in a -> `bottle.
Question: What is the` (accepted vineyard/winery)
- winter: Fact: The season of snowmen and sledging begins in the north in the month of -> `October.
Question: Which of the` (accepted December)
- winter: Fact: The season of snow and frost comes right after -> `the season of falling leaves.
Question` (accepted autumn/fall)
- winter: Fact: The shortest day of the year in the north, around 21 December, is called the -> `winter solstice.
The winter sol` (accepted solstice)
- Wisconsin: Fact: The largest city of the state of the Packers is -> `Green Bay.
Question: The largest` (accepted Milwaukee)
- Wisconsin: Fact: The state of Madison borders Minnesota to the west and Illinois to the -> `east.
Hypothesis: The` (accepted south)

## J-part share of probe variance per layer

| layer | median | IQR | random-direction median | own token among atoms | probe norm (median) |
|---|---|---|---|---|---|
| 16 | 0.024 | 0.021-0.026 | 0.018 | 0.04 | 10.7 |
| 17 | 0.025 | 0.022-0.029 | 0.018 | 0.04 | 11.4 |
| 18 | 0.028 | 0.025-0.035 | 0.019 | 0.08 | 12.9 |
| 19 | 0.029 | 0.025-0.034 | 0.018 | 0.08 | 14.5 |
| 20 | 0.029 | 0.025-0.035 | 0.019 | 0.11 | 15.9 |
| 21 | 0.029 | 0.026-0.036 | 0.018 | 0.11 | 17.2 |
| 22 | 0.033 | 0.028-0.038 | 0.019 | 0.06 | 18.0 |
| 23 | 0.038 | 0.033-0.045 | 0.019 | 0.20 | 18.7 |
| 24 | 0.045 | 0.038-0.052 | 0.020 | 0.20 | 19.3 |
| 25 | 0.048 | 0.044-0.057 | 0.020 | 0.20 | 19.6 |
| 26 | 0.050 | 0.044-0.060 | 0.020 | 0.18 | 20.5 |
| 27 | 0.051 | 0.046-0.061 | 0.020 | 0.20 | 20.1 |
| 28 | 0.050 | 0.045-0.060 | 0.019 | 0.19 | 20.2 |
| 29 | 0.049 | 0.044-0.057 | 0.019 | 0.21 | 20.5 |
| 30 | 0.049 | 0.042-0.057 | 0.019 | 0.20 | 21.7 |
| 31 | 0.048 | 0.042-0.055 | 0.020 | 0.22 | 21.1 |
| 32 | 0.049 | 0.044-0.056 | 0.020 | 0.22 | 20.8 |
| 33 | 0.053 | 0.045-0.061 | 0.021 | 0.22 | 20.7 |
| 34 | 0.058 | 0.050-0.065 | 0.022 | 0.21 | 22.0 |
| 35 | 0.056 | 0.051-0.064 | 0.023 | 0.24 | 23.8 |
| 36 | 0.061 | 0.054-0.071 | 0.023 | 0.28 | 25.5 |
| 37 | 0.061 | 0.056-0.072 | 0.024 | 0.22 | 26.2 |
| 38 | 0.063 | 0.055-0.076 | 0.025 | 0.24 | 26.4 |
| 39 | 0.074 | 0.062-0.090 | 0.027 | 0.26 | 26.8 |
| 40 | 0.081 | 0.068-0.099 | 0.029 | 0.28 | 26.8 |
| 41 | 0.081 | 0.071-0.101 | 0.029 | 0.25 | 26.7 |
| 42 | 0.080 | 0.071-0.101 | 0.031 | 0.31 | 27.4 |
| 43 | 0.079 | 0.070-0.098 | 0.031 | 0.32 | 27.6 |
| 44 | 0.078 | 0.069-0.097 | 0.030 | 0.34 | 28.3 |
| 45 | 0.075 | 0.067-0.095 | 0.030 | 0.35 | 29.0 |
| 46 | 0.075 | 0.064-0.095 | 0.031 | 0.34 | 29.9 |
| 47 | 0.075 | 0.064-0.092 | 0.031 | 0.34 | 29.8 |
| 48 | 0.083 | 0.069-0.100 | 0.031 | 0.39 | 31.3 |

## Top-10 J-part atoms at layer 32 (by coefficient)

- **ant** (J share 0.04): `线路` `“A` `\r` ` Sug` ` bees` ` intrigue` ` swollen` `大脑` `蚁` ` Danish`
- **apple** (J share 0.06): ` apple` ` Whilst` ` Juan` `邪恶` ` diced` `(W` `“A` `矩阵` `-red` `策略`
- **Australia** (J share 0.05): ` sheep` ` Aboriginal` `采用` `Australian` ` Reef` `澳洲` `ﬁ` `#w` `荒野` ` Perd`
- **baseball** (J share 0.04): ` Baseball` `被告` `回车` `复盘` `“A` ` TOR` ` tossed` ` Hawai` ` venue` ` pis`
- **basketball** (J share 0.05): ` basketball` `被` `“A` `篮板` ` Shot` ` NBA` ` maxHeight` `*S` `晓` `单手`
- **bear** (J share 0.06): ` Hog` ` Peterson` `B` `野` `чё` `」と` `微软` `猎` ` bav` ` Alaska`
- **beer** (J share 0.06): ` beer` ` Brewing` `四` ` expansive` `泡` ` caball` ` liqu` ` vox` `*B` ` RVA`
- **Belgium** (J share 0.06): ` Brussels` `…the` ` Dutch` ` Lille` ` bisc` ` fred` `Comic` `实战` ` BOOST` ` Brus`
- **bicycle** (J share 0.09): `自行车` `或` `Z` ` rider` `安装` ` scooter` ` tucked` ` axle` ` skate` `踏板`
- **brain** (J share 0.06): ` EEG` `'T` `大脑` ` cortical` ` Gra` `宿舍` ` medically` `处理` `搏` `职责`
- **Brazil** (J share 0.05): ` Rio` ` Constr` `₁` `舞蹈` `速度` ``t` `挂靠` ` Brasil` ` Combo` `弧形`
- **buffalo** (J share 0.06): `草原` ` Sioux` ` cowboy` `辫` ` Alaska` ` rim` `"P` `生存` ` Reserved` `尺寸`
- **butter** (J share 0.03): `烹饪` ` pastry` `出口` `O` `ζ` ` Emanuel` ` avec` `“A` ` Rennes` ` pristine`
- **calcium** (J share 0.04): `一个` ` Vitamin` `“A` ` hv` ` Eau` `接着` ` Gabriel` `钙` ` corros` `穆`
- **Canada** (J share 0.05): `雪` ` provincial` ` Vancouver` ` Conn` `“A` ` bois` `基建` `,K` `低温` ` Logging`
- **carbon** (J share 0.05): ` graphite` `原子` ` penned` `人造` `[Y` ` lecz` `i` `"is` ` Moy` ` molecule`
- **China** (J share 0.07): ` Ming` ` китай` ` XI` `地域` `穿` `儒家` ` Leb` ` Bamboo` ` plush` `丨`
- **Christmas** (J share 0.05): `圣诞` ` theological` ` Gift` `"H` `温度` `大概率` ` SHR` `摆放` ` Arabs` ` Navidad`
- **Darwin** (J share 0.04): ` Westminster` `信号` ` Lava` `种群` `弈` `(L` ` slender` `垫付` ` wx` ` Mk`
- **diamond** (J share 0.07): ` Fried` `南非` `的` `衡量` ` formidable` `'B` `s` ` velvet` `KG` `蓝宝石`
- **drums** (J share 0.04): `舞蹈` ` percussion` ` deput` `乐队` `…I` `非洲` `/K` ` Coch` `*K` `Fig`
- **eagle** (J share 0.05): ` eagle` ` hawk` `лё` ` Ó` `佐` ` sib` `无人机` `*B` `壮` `/Z`
- **Earth** (J share 0.05): ` Earth` `地球的` `温度` `“A` ` ocean` `chunk` ` avec` `<strong` `勘探` ` encompasses`
- **Easter** (J share 0.06): ` Sabbath` ` Calend` `祭` ` Ramadan` `节假日` ` cate` `光伏电站` ``t` `en` ` repent`
- **Egypt** (J share 0.05): ` Egyptian` ` Cairo` `KE` `金字塔` ` flor` ` Δ` `打卡` `拒不` `分页` ` htonl`
- **Einstein** (J share 0.05): ` irq` ` literary` `职场` ` MIT` `丨` ` Irma` ` gdy` `镀` ` Bernstein` `是一位`
- **elephant** (J share 0.05): ` elephants` ` Ante` `(K` `查获` ` errmsg` `族` `护` ` toddler` `Fig` ` Milano`
- **England** (J share 0.06): `牛津` ` II` ` coloured` `共享` `光伏` `英国` `骄阳` ` Norwich` ` mnie` ` Druid`
- **Europa** (J share 0.03): ` Lisbon` `“A` `…I` ` Cine` `变种` ` paradise` `'I` ` Antar` ` Atlantis` `丨`
- **France** (J share 0.08): ` PARIS` `French` `市集` ` bourgeois` `茅` ` Haut` ` Champagne` ` Pir` `打卡` ` Grenoble`
- **Friday** (J share 0.04): ` abrupt` `abaj` ` weekday` ` JE` `巴基斯坦` `一周` `en` `宗教` ` Saison` `days`
- **Germany** (J share 0.05): `德国` ` Ange` `“A` `可是` `无须` ` Gutenberg` ` Nicolas` ` steep` ` NRW` ` VW`
- **gold** (J share 0.03): ` Tibet` `尺寸` ` KC` `"T` ` copper` ` mex` `金的` ` Allocator` `…but` ` alors`
- **golf** (J share 0.06): ` golf` `了` ` Tournament` `“A` `爱尔兰` ` defini` ` Broker` `高尔夫` `GA` ` Mk`
- **grape** (J share 0.04): `的` ` grape` ` glossy` `如同` ` Noir` `口干` `/down` ` Seeds` ` Nguyen` `大棚`
- **Greece** (J share 0.06): `海上` `地中海` ` Greeks` ` Kos` ` poet` ` IW` ` nous` ` Borr` `"P` ` Villas`
- **guitar** (J share 0.05): `琴` ` Guitar` `…and` ` Hawaiian` ` plugged` ` Das` ` guit` `厂家` ` Dillon` `的`
- **heart** (J share 0.05): ` specialised` `心跳` ` AW` `或` ` beep` ` Kou` `动脉` `医师` ` cuff` `“A`
- **honey** (J share 0.04): `蜂蜜` ` healed` `“A` ` medicinal` ` Uganda` ` Ui` ` fatty` `仓库` ` ethanol` `实验`
- **Hungary** (J share 0.05): ` Budapest` ` Croatian` ` Mek` `“A` ` gint` ` Rossi` `」と` `红色` `自豪` `与当地`
- **India** (J share 0.08): ` Hindu` ` Bihar` `桑` `印度` ` Bollywood` `'L` `口径` ` Seh` `丨` `“What`
- **iron** (J share 0.05): `金属` ` pigment` `下列` ` faint` ` Metall` `[D` ` overhe` ` Coal` ` ROS` `钢筋`
- **Italy** (J share 0.05): `出口` ` Italian` `心跳` ` Venice` ` Fig` `粉笔` ` Buon` ` scant` `读懂` ` Repos`
- **Japan** (J share 0.07): ` Tokyo` `在日本` ` Fuj` `日文` ` ฯลฯ` ` ქ` `i` `*K` ` rice` ` Osaka`
- **July** (J share 0.03): `匝` ` Bou` `大量` ` Celebration` ` sunrise` ` barbecue` ` festive` ` Bravo` ` Ramadhan` ` appended`
- **Jupiter** (J share 0.05): `行星` ` Nr` `/MIT` `望远镜` `π` `…the` ` SUV` ` furnished` ` swollen` ` tether`
- **kidney** (J share 0.05): ` medically` `"x` `卜` ` kidneys` ` Nagar` ` TERMIN` ` respiratory` `大堂` `女性` ` Nieder`
- **Lincoln** (J share 0.05): ` Missouri` `州` ` Illinois` `我是一个` `表格` ` intim` ` gubern` `椭圆` ` WHITE` `疯`
- **liver** (J share 0.05): ` Damage` ` gland` ` implanted` `SG` ` sorrow` `人工` ` medically` `出品` `"T` ` Dysfunction`
- **lung** (J share 0.06): ` lungs` ` Respir` `现在的` ` tear` `丨` ` cough` `Γ` ` faulty` `“A` `?v`
- **March** (J share 0.03): `统计` ` abrupt` `,N` ` Pace` ` FIXME` ` Φ` `日出` `EN` ` festive` ` NBC`
- **Mars** (J share 0.06): ` Elon` ` ибо` ` ober` `飞船` ` Coy` `火星` `镍` ` CSR` `ē` ` hypo`
- **May** (J share 0.03): ` Φ` ` birthday` `偏移` ` KeyboardInterrupt` ` Sabb` ` שב` `夏季` ` Arkansas` `和前` `Winter`
- **mercury** (J share 0.05): ` depend` ` mercury` `ι` ` Cool` `逗` `不负` `强` ` Wij` ` fing` `-metal`
- **Mexico** (J share 0.05): `墨西哥` ` Contra` `万方` ` Coastal` ` proudly` `’m` ` peninsula` ` Paso` ` Margar` `…the`
- **Michigan** (J share 0.06): ` Michigan` ` Detroit` `小` `’il` ` flott` `利用` ` gt` `高歌` `ς` ` Coup`
- **moon** (J share 0.06): `月球` ` lunar` `每次` `’s` `SD` `遥感` ` programmes` ` Oi` `"S` ` spacecraft`
- **Mozart** (J share 0.04): `音响` `…I` ` ITAL` ` epoch` ` Zürich` ` QString` ` Havana` ` MG` `标签` ` Conce`
- **Napoleon** (J share 0.05): `等待` ` Napoleon` `河南` `[image` ` POW` `回撤` `接受` ` Militar` ` Saigon` `三亚`
- **Newton** (J share 0.05): `玻璃` `定律` `牛顿` `“I` ` drib` `陛下` `Math` `&quot` ` Elast` ` adaptor`
- **nitrogen** (J share 0.04): `冻` ` β` ` cubic` ` Urg` ` IW` `液体` `Atoms` `“A` ` moot` ` chilled`
- **oak** (J share 0.04): ` oak` `其` `插件` ` asyncio` `“A` ` sér` ` subtly` ` Mme` ` kou` ` Ulrich`
- **owl** (J share 0.05): ` Owl` `代表` ` Lis` ` FAA` ` symbolism` ` stuffed` ` cough` ` Retrofit` `夜间` ` Archiv`
- **oxygen** (J share 0.05): ` fragile` `/vue` ` β` ` Antoine` `中毒` `Po` `'D` ` Equip` `连通` ` Sodium`
- **pearl** (J share 0.03): `和` ` coral` ` pigment` `a` ` utmost` ` TG` `该技术` `年金` ` whence` `物料`
- **Peru** (J share 0.05): ` Peru` `被` ` fleets` `…I` ` Pach` `代表` ` Zur` `eke` ` FI` `*sp`
- **Philadelphia** (J share 0.06): `Philadelphia` ` Pennsylvania` `存款` `首先` `共享` ` constat` `石灰` ` Lydia` `停车` `包裹`
- **piano** (J share 0.06): `钢琴` `若干` ` Madre` ` VIII` ` FIG` ` NU` ` Schlaf` `大于` ` Nº` `三层`
- **pine** (J share 0.05): `和` `廉价` ` pine` `树种` ` Poor` ` Suomen` ` sweater` ` Chev` ` III` ` pog`
- **Poland** (J share 0.08): `波兰` ` Krak` ` WR` `²` ` Merc` ` Grat` `铭` `窗` `泵` ` Mme`
- **ruby** (J share 0.03): `这里` ` Nepal` `家国` `霓虹` `&quot` ` cname` ` FI` ` handsome` ` Farb` `登録`
- **Russia** (J share 0.08): `"L` `俄罗斯` ` Bolshevik` ` Kremlin` ` XI` `无须` `俄` `彼得` ` Petersburg` ` Crime`
- **Saturn** (J share 0.04): `"M` ` ω` ` spacecraft` `玩具` ` pud` `十日` ` Cov` `ş` `pread` `黑洞`
- **Seattle** (J share 0.04): ` Oregon` `Seattle` ` downtown` ` Coastal` `乐队` `“We` ` TY` `黛` `点评` `罩`
- **Shakespeare** (J share 0.06): ` Shakespeare` `文本` `…and` ` probs` ` Mare` `海盗` `Anne` ` Subscription` ` скла` ` şi`
- **silver** (J share 0.03): `铜` ` Nit` `贵金属` ` DV` `"T` `埃及` ` simult` ` pharmac` `温湿度` ` corros`
- **Singapore** (J share 0.05): ` Singapore` ` reminiscent` ` Singap` `万方` `TP` ` Climat` ` Stamford` `这就是我` ` tarp` ` cozy`
- **snake** (J share 0.05): ` venom` ` snakes` `安装` `/disable` ` zatem` `ﬁ` ` Parch` ` Э` `嫁接` `绿叶`
- **sodium** (J share 0.05): ` sodium` ` Table` `拉丁` `火焰` `防止` `血压` `」と` ` Farben` ` IDs` `ชิด`
- **Spain** (J share 0.06): `スペイン` `百万` ` festive` `分页` `La` ` Pau` `(P` `羊肉` `如果说` ` Catalan`
- **spider** (J share 0.06): `对` ` Venom` ` spider` ` Peters` ` yogurt` ` efficacy` ` QObject` ` gyn` ` manis` `复仇`
- **stomach** (J share 0.06): `胃` ` ulcer` `前台` ` SG` ` digestive` ` Cannot` ` mou` ` detox` ` Brun` `晓`
- **summer** (J share 0.04): `夏季` ` mosquito` `季节` `“I` `回调` `丨` ` BBQ` ` Eich` ` Protective` ` cic`
- **swan** (J share 0.05): `“A` `韩` `浪漫` `承租` `鸟类` ` ま` ` lovely` `三只` ` Procur` `雄性`
- **Sweden** (J share 0.05): `瑞典` ` FP` ` Helsinki` ` Volvo` ` Svens` `接着` `益` `“No` `…the` ` Ownership`
- **tennis** (J share 0.07): ` Tennis` `大` ` Throws` `分类` ` adjud` `交锋` ` optic` ` SSL` ` Aussie` `*N`
- **Thursday** (J share 0.03): ` Vac` `节日` `叠加` ` BBQ` ` bere` `"w` ` ID` `看来` ` disf` ` kai`
- **train** (J share 0.12): `乘客` ` railway` ` Rail` ` Transit` `“A` `地铁` `列车` ` splendid` `穿梭` ` boarding`
- **trumpet** (J share 0.05): ` trumpet` ` brass` `创作` `音频` `口腔` ` taz` `"B` `“A` ` Kendrick` ` XM`
- **turtle** (J share 0.05): `和` ` turtles` `食` ` juven` ` Fet` ` reinc` `几十` ` Sweep` ` monstr` ` kra`
- **Vatican** (J share 0.08): ` Vatican` `文书` `全局` ` Rabbi` ` Sanct` `/rc` ` Iglesia` `执行` ` Cust` `既然`
- **Venus** (J share 0.05): `加上` ` Furious` `镜面` `重庆` ` Sphinx` ` vivid` `烛` ` Tuesday` `iang` ` coral`
- **violin** (J share 0.03): ` violin` `“I` ` sopr` ` gum` `图谱` `al` `尺寸` `摆` `"x` `,R`
- **wine** (J share 0.04): ` Wine` `三个` `酒` `ζ` ` Hed` `Z` ` Kult` ` brethren` ` champagne` ` velvet`
- **winter** (J share 0.04): ` fever` ` Snow` `的` `暂` `ﬁ` ` festive` `病毒` ` Pand` `冬` `煤炭`
- **Wisconsin** (J share 0.04): ` Midwest` `和` ` famed` ` Pizza` ` Ownership` ` QU` `-cluster` ` Lieu` `伊利` `多肉`
