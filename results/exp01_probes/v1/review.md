# exp01_probes / v1: review sheet

Prompts kept: 543 of 682.

## Kept prompts per entity (kept / written)

ant 6/7, apple 6/7, Australia 6/8, baseball 6/7, basketball 6/7, bear 6/7, beer 6/7, Belgium 7/8, bicycle 7/7, brain 7/7, Brazil 8/8, buffalo 6/7, butter 3/6, calcium 3/5, Canada 5/8, carbon 6/7, China 8/8, Christmas 5/8, Darwin 5/6, diamond 7/7, drums 6/7, eagle 6/6, Earth 5/8, Easter 4/7, Egypt 7/8, Einstein 5/6, elephant 6/7, England 7/8, Europa 6/7, France 8/8, Friday 5/6, Germany 7/8, gold 5/7, golf 7/8, grape 2/5, Greece 8/8, guitar 5/6, heart 6/7, honey 4/7, Hungary 6/8, India 8/8, iron 7/7, Italy 7/8, Japan 8/8, July 4/7, June 0/6, Jupiter 6/7, kidney 5/6, Lincoln 8/8, liver 7/7, lung 7/7, March 3/7, Mars 7/7, May 4/7, mercury 6/7, Mexico 8/8, Michigan 5/7, moon 8/8, Mozart 5/7, Napoleon 4/7, Newton 5/7, nitrogen 2/6, oak 4/5, owl 5/7, oxygen 6/7, pearl 4/5, Peru 7/8, Philadelphia 5/8, piano 3/5, pine 3/5, Poland 6/8, ruby 3/5, Russia 6/8, Saturn 4/7, Seattle 6/8, Shakespeare 7/8, silver 7/7, Singapore 5/8, snake 6/8, sodium 5/7, Spain 7/8, spider 7/7, stomach 6/6, summer 5/7, swan 5/8, Sweden 6/8, tennis 5/8, Thursday 3/6, train 6/7, trumpet 4/5, turtle 5/6, Vatican 7/8, Venus 7/7, violin 5/5, wine 6/7, winter 4/7, Wisconsin 5/7

## Random sample of 25 prompts (seed 0)

| entity | prompt | accepted | Qwen's greedy continuation | kept |
|---|---|---|---|---|
| Mexico | Fact: The beach resort of Cancún faces the | Caribbean | ` Caribbean Sea.\nQuestion: Which of` | yes |
| Newton | Fact: The first of the famous laws of motion is also called the law of | inertia | ` inertia.\nQuestion: What is the` | yes |
| bear | Fact: Winnie-the-Pooh's best friend is a small pig called | Piglet | ` Piglet.\nQuestion: What is` | yes |
| heart | Fact: A stopped cardiac rhythm can be restored by an electric shock from a | defibrillator | ` defibrillator.\nQuestion: Which` | yes |
| Seattle | Fact: The coffee chain that opened its first store at Pike Place Market in 1971 is | Starbucks | ` now the largest coffeehouse chain in the` | no |
| Poland | Fact: The astronomer from Toruń who put the Sun at the centre was Nicolaus | Copernicus | ` Copernicus.\nQuestion: Which` | yes |
| Mozart | Fact: The composer of The Marriage of Figaro and Don Giovanni was from the country of | Austria | ` Austria.\nQuestion: Who composed The` | yes |
| Japan | Fact: The poem of three lines with five, seven and five syllables is called a | haiku | ` haiku.\nQuestion: What is` | yes |
| pine | Fact: The forests of needled conifers that cover Siberia and Scandinavia are called the | taiga/boreal | ` taiga.\nHypothesis:` | yes |
| March | Fact: The zodiac sign of someone born in the first week of the month of St. Patrick's Day is | Pisces | ` Aries.\nQuestion: What is` | no |
| swan | Fact: The male of the bird into which the ugly duckling grew is called a | cob | ` swan.\nQuestion: The male` | no |
| Germany | Fact: The region of cuckoo clocks in Baden-Württemberg is the Black | Forest | ` Forest.\nQuestion: The Black Forest` | yes |
| Saturn | Fact: The next planet out from the Sun after the planet of Titan is | Uranus | ` Saturn.\nHypothesis: Saturn` | no |
| drums | Fact: The percussion kit of Ringo Starr includes metal plates called | cymbals | ` cymbals.\nQuestion: Which` | yes |
| India | Fact: The bat-and-ball sport adored in Mumbai and Kolkata is | cricket | ` cricket.\nQuestion: What is the` | yes |
| drums | Fact: The large bass part of the percussion kit is played with a foot | pedal | ` pedal.\nHypothesis: The` | yes |
| calcium | Fact: Eggshells and seashells are made mostly of the carbonate of the metal found in | chalk/limestone | ` the periodic table in group 2,` | no |
| trumpet | Fact: Louis Armstrong's instrument is in the same family as the trombone and the | tuba/horn/French | ` trumpet.\nQuestion: Which of the` | no |
| guitar | Fact: The electric instrument played by Jimi Hendrix is plugged into an | amplifier/amp | ` amplifier.\nHypothesis: Jim` | yes |
| Singapore | Fact: The hotel with three towers joined by a rooftop pool is Marina Bay | Sands | ` Sands.\nQuestion: What is the` | yes |
| tennis | Fact: The sport of Björn Borg uses a fuzzy | ball/yellow | ` ball.\nHypothesis: Bj` | yes |
| eagle | Fact: The bird of prey sacred to Zeus carried off the Trojan boy | Ganymede | ` Ganymede to Olympus.\nQuestion` | yes |
| July | Fact: The zodiac sign of a person born on American Independence Day is | Cancer | ` Leo.\nQuestion: What is the` | no |
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
| 16 | 0.048 | 0.038-0.057 | 0.018 | 0.06 | 10.7 |
| 17 | 0.051 | 0.042-0.060 | 0.018 | 0.10 | 11.5 |
| 18 | 0.064 | 0.054-0.075 | 0.019 | 0.10 | 12.8 |
| 19 | 0.062 | 0.053-0.075 | 0.018 | 0.12 | 14.5 |
| 20 | 0.060 | 0.053-0.071 | 0.019 | 0.14 | 15.9 |
| 21 | 0.060 | 0.054-0.072 | 0.018 | 0.16 | 17.1 |
| 22 | 0.065 | 0.055-0.075 | 0.019 | 0.18 | 18.0 |
| 23 | 0.072 | 0.063-0.084 | 0.019 | 0.21 | 18.7 |
| 24 | 0.086 | 0.071-0.095 | 0.020 | 0.24 | 19.1 |
| 25 | 0.092 | 0.076-0.102 | 0.020 | 0.21 | 19.5 |
| 26 | 0.092 | 0.076-0.107 | 0.020 | 0.15 | 20.4 |
| 27 | 0.091 | 0.079-0.108 | 0.020 | 0.18 | 19.9 |
| 28 | 0.086 | 0.075-0.102 | 0.020 | 0.21 | 20.1 |
| 29 | 0.082 | 0.072-0.099 | 0.019 | 0.20 | 20.5 |
| 30 | 0.078 | 0.070-0.094 | 0.019 | 0.19 | 21.4 |
| 31 | 0.078 | 0.068-0.094 | 0.019 | 0.19 | 21.1 |
| 32 | 0.079 | 0.067-0.096 | 0.020 | 0.23 | 20.8 |
| 33 | 0.085 | 0.073-0.104 | 0.021 | 0.28 | 20.7 |
| 34 | 0.097 | 0.081-0.116 | 0.022 | 0.27 | 22.0 |
| 35 | 0.101 | 0.085-0.115 | 0.022 | 0.27 | 23.7 |
| 36 | 0.108 | 0.092-0.129 | 0.023 | 0.32 | 25.1 |
| 37 | 0.106 | 0.092-0.126 | 0.024 | 0.23 | 25.9 |
| 38 | 0.105 | 0.089-0.126 | 0.025 | 0.26 | 26.3 |
| 39 | 0.121 | 0.098-0.138 | 0.027 | 0.31 | 26.7 |
| 40 | 0.126 | 0.110-0.157 | 0.029 | 0.35 | 26.6 |
| 41 | 0.130 | 0.112-0.157 | 0.030 | 0.35 | 26.6 |
| 42 | 0.126 | 0.111-0.154 | 0.030 | 0.40 | 27.2 |
| 43 | 0.118 | 0.104-0.147 | 0.031 | 0.38 | 27.5 |
| 44 | 0.112 | 0.095-0.138 | 0.031 | 0.40 | 28.1 |
| 45 | 0.102 | 0.090-0.128 | 0.030 | 0.47 | 29.0 |
| 46 | 0.096 | 0.084-0.122 | 0.031 | 0.46 | 29.9 |
| 47 | 0.095 | 0.082-0.118 | 0.031 | 0.44 | 29.8 |
| 48 | 0.104 | 0.089-0.124 | 0.031 | 0.51 | 31.3 |

## Top-10 J-part atoms at layer 32 (by coefficient)

- **ant** (J share 0.08): ` insects` ` Crush` `细胞` ` helpers` ` hive` ` CN` `自我` `独立` ` Tum` `\r`
- **apple** (J share 0.08): `张` ` apple` ` perpetrated` ` robert` `/V` `-red` ` Piero` `驱动` ` Evil` ` Cunning`
- **Australia** (J share 0.09): ` Reef` ` Aboriginal` ` austral` ` wildlife` `“A` `获` `Australian` ` graz` ` BUG` `构成`
- **baseball** (J share 0.09): ` Baseball` `不能` ` finale` ` Phillies` ` yard` `除非` `“A` ` Defendants` ` bows` `ι`
- **basketball** (J share 0.10): `了` ` basketball` ` NBA` ` Slam` ` dunk` `打法` `“A` `²` `拼搏` ` maxHeight`
- **bear** (J share 0.10): ` звер` `猎` `野` ` mama` ` sled` `」と` ` Sioux` ` puppies` ` Anthrop` ` fox`
- **beer** (J share 0.10): ` beer` `啤酒` ` Volum` ` Brewing` ` damp` ` bespoke` ` foam` `"x` ` trays` `烟`
- **Belgium** (J share 0.07): `是` ` Brussels` ` Flem` ` nameof` ` Petite` `周边` ` lé` `…the` ` Vla` ` quaint`
- **bicycle** (J share 0.12): `或` `ﬁ` ` rider` ` pedals` `自行车` ` cushions` ` axle` `Dettagli` ` crisp` ` slack`
- **brain** (J share 0.11): ` spinal` `大脑` `"w` `二者` ` Nursing` ` EEG` `\n` `走廊` `通讯` ` contingency`
- **Brazil** (J share 0.11): ` Rio` ` Brasil` `…I` `身着` `融合` ` Piazza` ` Constr` ` Rodrigues` ` Squad` `狂野`
- **buffalo** (J share 0.10): `草原` `照片` `食` ` hunted` ` ranch` `Native` ` Bison` `依赖` ` carc` ` snag`
- **butter** (J share 0.06): `“A` ` recipes` `出口` ` Tender` `形式` ` rustic` `痛快` ` launder` `她的` ` Plast`
- **calcium** (J share 0.09): ` Vitamin` `丨` `"x` `“A` `钙` ` magnesium` ` hv` ` β` `经文` `翡翠`
- **Canada** (J share 0.09): ` Snow` `冰` `基建` ` rink` ` Municipal` `ﬁ` ` proudly` `代表性` ` sede` `/node`
- **carbon** (J share 0.09): ` graphite` `X` ` Nail` ` abbrev` ` Alias` `化合` ` Mg` `形成的` `化学` `制造`
- **China** (J share 0.11): `Chinese` ` Qing` ` monumental` `秦始皇` ` silk` ` caravan` ` XI` ` Redis` `百万` `景观`
- **Christmas** (J share 0.07): `圣诞` ` Dickens` `按照` ` bx` ` festive` ` et` `盈亏` `寓意` `正月` ` brunch`
- **Darwin** (J share 0.08): ` Keynes` ` Westminster` `'B` `ﬁ` ` Londres` `达尔` `化验` `和` ` explorer` `打印机`
- **diamond** (J share 0.07): `的` ` jewel` `夫妻` `南非` ` bridal` ` Vintage` `衡量` ` WG` `和最` `行情`
- **drums** (J share 0.06): ` percussion` `付` `Assistant` ` Tray` ` Claw` `“I` ` Figura` `板式` ` KL` `aux`
- **eagle** (J share 0.07): ` eagle` `在` ` hawk` `无人机` ` mutil` ` Apollo` `飞行` `/Z` ` Feu` `誓词`
- **Earth** (J share 0.14): ` oceans` `地球` ` terrestrial` `亿` ` chunk` `人口` `地质` ` fiss` `人手` ` Nuclear`
- **Easter** (J share 0.07): `祭` ` Sabb` `谓` `对应` ` Ramadan` ` CP` ` calend` ` Ritual` `…the` ` discontin`
- **Egypt** (J share 0.07): ` Egyptian` ` Monument` `峡谷` `否` `穿` `marsh` ` Kho` `Q` ` DRV` `最为`
- **Einstein** (J share 0.09): ` stint` `案` `爱因斯坦` `ﬁ` ` German` `"I` `万美元` `在上海` `光电` ` Fraud`
- **elephant** (J share 0.06): ` elephants` ` aka` `当` ` UNUSED` ` sculpt` `Φ` `训练` `防护` ` corrobor` `牧民`
- **England** (J share 0.10): ` Westminster` ` Saints` ` XI` `…I` `东` `英超` ` Normandie` `聚合` ` Colour` ` midfielder`
- **Europa** (J share 0.06): ` Euro` ` salty` `卫星` ` abyss` `ﬁ` `或许` `留言` ` webshop` ` crypto` `追加`
- **France** (J share 0.10): `首先` `巴黎` ` Musée` ` whence` ` downtown` ` HQ` `…the` `评分` ` Marseille` ` Repos`
- **Friday** (J share 0.06): ` Tuesday` `对应的` ` Nº` ` IV` `还应当` `一周` `西班牙语` ` pej` ` untranslated` ` Cous`
- **Germany** (J share 0.08): `“A` `德国` ` Joh` ` Matthias` ` Mainz` ` Navig` `财经` `间断` `首先` ` Ə`
- **gold** (J share 0.06): ` thin` `"x` ` Mineral` `镀` ` FT` `ς` `新疆` `原始` `金子` `追梦`
- **golf** (J share 0.05): ` Venue` ` golf` `高尔夫` `S` ` Broker` `教练` ` irrelevant` `微型` `相对于` `每次都`
- **Greece** (J share 0.06): ` Greeks` ` Founded` `相当` ` Coastal` `公元前` `*S` ` PY` `首先` ` revered` ` Ibn`
- **guitar** (J share 0.08): ` Yamaha` ` guitar` `琴` ` Vintage` `复制` `改装` ` Kurt` ` mtx` `“A` `制造`
- **heart** (J share 0.08): ` heartbeat` `或者` `“A` ` beep` ` surgeons` ` arterial` ` Initialise` `心律` `俗称` `医师`
- **honey** (J share 0.06): `来源` ` honey` ` purified` `提取` `酒精` `零食` ` variant` ` PY` ` PO` ` wohl`
- **Hungary** (J share 0.07): `原` ` Hungarian` ` Budapest` ` río` `“A` ` Erm` `巧妙` `不等` ` Amt` `(rx`
- **India** (J share 0.12): ` Gandhi` `印度` `“A` ` Kolkata` `本地` ` Hindi` ` Masjid` `绝大多数` ` ikon` ` belle`
- **iron** (J share 0.11): ` magnetic` ` redd` ` pigment` `金属` `生锈` `裂缝` ` furnace` ` Temperature` ` Gn` `产生的`
- **Italy** (J share 0.06): `地图` ` Sant` ` Pir` ` SB` `坐落在` `…the` ` nestled` ` Bari` `出口` ` Cannes`
- **Japan** (J share 0.07): ` Japon` ` Fuj` ` MT` ` nameof` ` eleg` `日本的` ` Osaka` `评分` `…the` `请选择`
- **July** (J share 0.06): ` Caesar` `月份` `‘s` ` balk` `包括` ` festive` `+N` ` commenc` `日晚间` ` Boulevard`
- **Jupiter** (J share 0.06): `卫星` `/MIT` `中文名` ` Nr` ` asteroids` ` Kepler` `…the` `兼` ` mutant` `搭载`
- **kidney** (J share 0.07): `小` ` bladder` `"x` `脏器` ` oxy` ` reactive` ` filtration` ` plugged` `通向` ` outpatient`
- **Lincoln** (J share 0.09): ` Kansas` ` Confederate` `页面` ` abolition` ` Peters` `/dc` `总统` ` tableView` `ﬁ` ` courthouse`
- **liver** (J share 0.07): `产生的` `肝` ` JE` `储` `“A` ` Moy` ` Sick` ` Implant` ` vegetal` `"F`
- **lung** (J share 0.09): ` Sick` ` organisms` `Ｃ` `CO` ` lungs` ` QU` ` cancers` `又叫` `"T` ` Pne`
- **March** (J share 0.05): ` autumn` ` weekday` `(NUM` ` exceeding` `一月` `"x` `时间的` ` Listing` `序号` `月份的`
- **Mars** (J share 0.09): `火星` ` gigante` `α` `-y` ` carbonate` ` Oculus` `₂` `II` ` Mesa` ` Olympus`
- **May** (J share 0.07): ` Kentucky` `,K` ` kickoff` `今年` ` QUERY` ` abbreviated` `Season` `不负` `无上` `倒数`
- **mercury** (J share 0.08): `神经` ` metallic` ` quoted` `及` ` depends` `ι` `苗` `危害` ` Cosmetic` `中毒`
- **Mexico** (J share 0.10): ` Diego` ` Puebla` ` peninsula` `Mex` `…I` `’en` `本地` ` Rivera` ` celebra` `不仅`
- **Michigan** (J share 0.09): ` Michigan` `七` ` waterfront` `五大` ` peninsula` `湖` `‘s` `…I` `翻开` `第四季`
- **moon** (J share 0.11): `月球` ` lunar` ` Apollo` `雷达` `"S` `’B` `S` `事故发生` ` EO` `三天`
- **Mozart** (J share 0.06): `大` ` Napoli` `…I` ` Francisco` ` Contempor` ` Vas` ` Mitte` ` QString` ` manuscript` `音乐`
- **Napoleon** (J share 0.09): `南` ` Napoleon` ` Petersburg` `旅` `回撤` `[image` ` Palma` ` guer` `撤离` `热`
- **Newton** (J share 0.07): `她` `牛顿` ` Monk` `定律` ` sword` ` Alfonso` `外国语学校` ` Glas` `(Q` ` Pedag`
- **oak** (J share 0.07): `小` ` oak` `“A` ` Fav` ` grotes` ` moss` ` Kou` ` bosque` ` arom` ` Feu`
- **owl** (J share 0.07): `小` `哺` ` sensory` ` upright` `鸟类` ` pillows` ` MQ` ` cones` ` glare` ` squirrel`
- **oxygen** (J share 0.08): ` Antoine` `一氧化碳` ` Molecular` `LY` ` Küh` ` oxy` ` ε` ` Amor` ` tablet` `υ`
- **pearl** (J share 0.05): `或` ` pearl` `夫妻` `…the` ` jub` ` Antique` ` Wedding` ` remar` `'B` ` reef`
- **Peru** (J share 0.10): ` Peru` ` Mt` `和` `“A` `神秘` `遗址` ` Orch` ` kho` ` plaza` `航拍`
- **Philadelphia** (J share 0.10): `和` `Philadelphia` ` Benjamin` ` Pennsylvania` ` Baptist` `挂牌` `街道` `ฯ` `轴线` ` GW`
- **piano** (J share 0.07): ` piano` `在` `三层` ` trays` `重量` ` spindle` ` repetitions` ` Hd` ` knobs` `西装`
- **pine** (J share 0.09): `和` ` Cheap` `廉价` ` Nordic` ` rustic` `绿化` ` balk` ` Saskatchewan` `*B` ` woodland`
- **Poland** (J share 0.09): `波兰` ` Johannes` `吴` ` Buon` `²` ` Mme` ` Stanis` ` Dei` `.doc` `-Mar`
- **ruby** (J share 0.07): `属性` ` Mineral` ` NE` `金刚石` `“I` ` uranium` ` Chrom` `amel` ` Magick` `结晶`
- **Russia** (J share 0.07): ` Petersburg` `财经` ` Kremlin` ` Aleks` `Λ` `>L` `-V` `不是我` ` Ferdinand` `首先`
- **Saturn** (J share 0.05): ` unlikely` `…the` `漂浮` ` analogous` ` PU` ` Hari` `黑洞` `最早的` `据` `基建`
- **Seattle** (J share 0.07): ` Seattle` `陈列` ` Brewery` ` KP` `瀑布` `AM` ` downtown` `标高` ` ориенти` ` vend`
- **Shakespeare** (J share 0.10): ` Shakespeare` `和` `Anne` `…and` ` babe` ` acquitted` ` Ante` ` Tud` `-II` ` скла`
- **silver** (J share 0.05): `铜` ` γ` ` matrim` ` Russia` ` ℕ` ` metals` ` Zn` ` potassium` ` Paraguay` ` XX`
- **Singapore** (J share 0.10): `Singapore` ` Singapore` ` Plaza` `ﬁ` ` singapore` `收敛` ` inaugural` `是我` ` Skal` ` splendida`
- **snake** (J share 0.10): ` venom` ` snakes` `/disable` `逻辑` `安装` ` progen` ` Paras` `色彩` `ﬁ` ` lizard`
- **sodium** (J share 0.09): ` sodium` ` Chem` ` oxide` `私` `Y` `压力下` `/Table` `火焰` ` pistol` ` eyed`
- **Spain** (J share 0.09): `了` ` inaug` `“A` `导航` ` Castillo` ` Fiesta` ` Paolo` `Spanish` ` Vidal` `-La`
- **spider** (J share 0.10): ` heroine` ` Peters` `毒` `“A` ` Deadpool` `蜘蛛` ` accus` `复仇` `LY` `#w`
- **stomach** (J share 0.11): ` digestive` ` sick` `胃` ` intestinal` `/q` `Section` `牧羊` ` β` ` PROCESS` ` compartments`
- **summer** (J share 0.08): `“A` `夏季` `利用` ` heat` `季节` ` BBQ` `频繁` ` mosquito` `防晒` ` sensible`
- **swan** (J share 0.08): ` fairy` `丹麦` `“A` `K` ` Husband` `旳` `雌` `一对` `狗的` ` Elegant`
- **Sweden** (J share 0.06): ` nameof` ` headquartered` `也就是` ` Å` ` Uni` `…the` ` Nobel` `陈旧` ` anonym` `砼`
- **tennis** (J share 0.09): ` Tennis` `四` `赛事` ` pastel` ` uni` `挠` `交锋` ` riff` `À` `格式`
- **Thursday** (J share 0.05): `翻译` ` Spanish` `#else` `英文名字` ` NRW` ` sans` `ert` `相当于` `谐音` `歧`
- **train** (J share 0.13): ` railway` ` Rail` `乘客` `列车` `穿梭` `/from` `“A` ` Travel` `ﬁ` ` Tokyo`
- **trumpet** (J share 0.07): ` trumpet` `音乐` ` brass` ` UNUSED` `B` ` flute` ` Waffen` `“A` `开口` ` Beb`
- **turtle** (J share 0.08): `和` ` beach` ` juven` ` turtles` `食` ` monsters` `几十` `…I` ` solicit` ` mortar`
- **Vatican** (J share 0.14): ` Vatican` `我的` ` Sanct` ` bishops` `/Admin` ` convened` ` Zürich` ` sede` `执行` ` Mere`
- **Venus** (J share 0.07): ` Venus` `晨` `(A` ` и` ` sulfur` ` dioxide` `镜面` `OCR` `绝望` ` faint`
- **violin** (J share 0.06): `“A` ` violin` `演奏` ` scraped` ` Rope` ` tether` ` fibres` ` Pferd` `弓` `木材`
- **wine** (J share 0.04): `与` ` wine` ` champagne` `Φ` `这类` ` Hed` ` intim` ` Ritual` `有限的` ` CAM`
- **winter** (J share 0.08): `冬` ` animals` `冰雪` ` Fever` `Snow` `い` ` ICE` ` Sick` `休眠` `分别`
- **Wisconsin** (J share 0.06): ` Midwest` `zip` ` Retail` ` Chic` `拥有` ` KR` `地图` `换言之` `…I` ` Albany`
