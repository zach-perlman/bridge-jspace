# exp01_probes / v4_chat_stmt_jpp_h200: review sheet

Prompts kept: 2446 of 2673.

## Kept prompts per entity (kept / written)

ant 25/27, apple 26/27, Australia 27/27, baseball 26/27, basketball 22/25, bear 24/27, beer 26/27, Belgium 27/28, bicycle 27/27, brain 29/29, Brazil 27/27, buffalo 25/27, butter 20/25, calcium 25/26, Canada 27/30, carbon 24/26, China 28/29, Christmas 29/29, Darwin 25/26, diamond 24/27, drums 22/25, eagle 24/26, Earth 28/29, Easter 24/28, Egypt 29/29, Einstein 25/26, elephant 24/27, England 26/28, Europa 20/25, France 30/30, Friday 22/26, Germany 30/30, gold 24/27, golf 27/30, grape 26/29, Greece 27/28, guitar 24/26, heart 27/27, honey 24/27, Hungary 25/28, India 29/29, iron 26/27, Italy 29/30, Japan 27/28, July 24/27, June 22/30, Jupiter 22/27, kidney 25/26, Lincoln 26/28, liver 25/27, lung 25/28, March 19/27, Mars 25/27, May 22/27, mercury 25/26, Mexico 28/30, Michigan 27/28, moon 28/29, Mozart 25/28, Napoleon 27/28, Newton 27/28, nitrogen 19/24, oak 24/25, owl 26/29, oxygen 26/29, pearl 25/25, Peru 29/31, Philadelphia 23/29, piano 25/27, pine 22/25, Poland 26/28, ruby 21/25, Russia 29/29, Saturn 22/26, Seattle 22/28, Shakespeare 30/30, silver 22/27, Singapore 21/28, snake 29/29, sodium 26/27, Spain 30/30, spider 26/28, stomach 26/27, summer 24/27, swan 20/28, Sweden 30/32, tennis 29/29, Thursday 18/25, train 30/30, trumpet 23/25, turtle 20/27, Vatican 26/28, Venus 21/27, violin 24/25, wine 27/28, winter 26/28, Wisconsin 25/29

## Random sample of 25 prompts (seed 0)

| entity | prompt | accepted | Qwen's greedy continuation | kept |
|---|---|---|---|---|
| moon | Fact: The phase between half and full of the body that governs the tides is called the | gibbous/waxing/waning | ` gibbous` | yes |
| oak | Fact: The hardwood of the Druids' tree shows silvery rays when it is cut in a way called quarter | sawn/sawing/sawed/cut | ` sawing` | yes |
| beer | Fact: Lager is stored in large | barrels/kegs/casks/tanks/vats | ` tanks` | yes |
| honey | Fact: The thick sweet product of hives is a supersaturated solution of | sugar/sugars/glucose/fructose | ` sugar` | yes |
| silver | Fact: The white metal of cutlery and jewellery tarnishes black when it reacts with | sulfur/sulphur | ` sulfur` | yes |
| Russia | Fact: The cathedral with colourful onion domes on Red Square is Saint | Basil/Basil's/Basil’s | ` Basil the Great` | yes |
| Newton | Fact: The mathematician who fought the author of the Principia over credit for calculus was Gottfried | Leibniz/Wilhelm | ` Wilhelm Leibniz` | yes |
| June | Fact: The month of Father's Day in America has the longest days of the year, because it contains the summer | solstice | ` solstice` | yes |
| ruby | Fact: The precious corundum coloured by chromium is the gem of wedding anniversary number | 40/forty | ` 45` | no |
| May | Fact: The car race held at the end of the month of Mother's Day in America is the Indianapolis | 500 | ` 500` | yes |
| tennis | Fact: In the sport of Andy Murray, a hard overhead shot like a serve is called a | smash | ` smash` | yes |
| gold | Fact: The metal of Olympic champions' medals is chemically unreactive, so it is called a noble | metal | ` metal` | yes |
| Shakespeare | Fact: In the tragedy by the author of Macbeth, Hamlet is the prince of | Denmark | ` Denmark` | yes |
| eagle | Fact: The golden raptor catches hares with its | talons/claws | ` talons` | yes |
| Italy | Fact: The Renaissance city of the Medici, where Michelangelo's David stands, is | Florence | ` Florence` | yes |
| eagle | Fact: The flag of Mexico shows a raptor perched on a | cactus | ` cactus` | yes |
| Canada | Fact: The two-dollar coin of the country of Montreal and Calgary is nicknamed the | toonie/twonie | ` loonie` | no |
| Vatican | Fact: The diplomats who represent the papal state abroad are called apostolic | nuncios/nuncio | ` nuncios` | yes |
| heart | Fact: The 'lub-dub' sounds heard through a stethoscope are made by the closing of the cardiac | valves/valve | ` valves` | yes |
| sodium | Fact: Humphry Davy first obtained the metal of soda in 1807 by the new technique of | electrolysis | ` electrolysis` | yes |
| trumpet | Fact: The slow bugle call played at US military funerals on a brass horn is called | Taps | ` Taps` | yes |
| Earth | Fact: The age of the world of humankind is about 4.5 billion | years | ` years` | yes |
| Jupiter | Fact: The NASA probe that has orbited the biggest planet since 2016 is | Juno | ` Juno` | yes |
| Canada | Fact: The capital of Manitoba is | Winnipeg | ` Winnipeg` | yes |
| buffalo | Fact: The huge shaggy animal of the prairie has a big hump on its | back/shoulders | ` back` | yes |

## Every rejected prompt

- ant: Fact: The acid in the sting of red fire insects is called -> `pederin` (accepted formic)
- ant: Fact: La Fontaine's version of the fable pairs the hardworking insect with a -> `lazy cicada` (accepted cicada/grasshopper)
- apple: Fact: The classic dark red supermarket fruit variety with five bumps on its base is the Red -> `Delicatus` (accepted Delicious)
- baseball: Fact: The Hall of Fame of the sport of Hank Aaron is in the village of -> `Mobile` (accepted Cooperstown)
- basketball: Fact: The sport of Michael Jordan is played on a -> `basketball court` (accepted court)
- basketball: Fact: The team from Boston in the sport of Larry Bird is the -> `Boston Celtics` (accepted Celtics)
- basketball: Fact: A free throw in the sport of Kobe Bryant is worth -> `2 points` (accepted one/1)
- bear: Fact: The picnic-basket-stealing cartoon character of Jellystone Park is named -> `Huckleberry Hound` (accepted Yogi)
- bear: Fact: The adult male of the grizzly is called a -> `bull` (accepted boar)
- bear: Fact: The Little Dipper is part of the constellation Ursa -> `Major` (accepted Minor)
- beer: Fact: The Dutch lager brand sold in green bottles with a red star is -> `Grolsch` (accepted Heineken)
- Belgium: Fact: The fried potatoes sold in paper cones in Liège are called -> `gaufres de Liège` (accepted fries/frites)
- buffalo: Fact: The shaggy animal of the American prairie is a close relative of domestic -> `cats` (accepted cattle/cows)
- buffalo: Fact: The European bison of the Białowieża Forest is also called the -> `European bison` (accepted wisent)
- butter: Fact: The plant-based substitute for churned cream fat is -> `coconut oil` (accepted margarine)
- butter: Fact: The Irish brand of grass-fed churned dairy fat is -> `butter` (accepted Kerrygold)
- butter: Fact: The wooden device used to turn cream into its golden fat is called a -> `butter churn` (accepted churn)
- butter: Fact: The dish of chicken breast stuffed with garlic and herbed melted cream fat is chicken -> `cordon bleu` (accepted Kiev/Kyiv)
- butter: Fact: The sauce made by whisking cold cubes of beurre into a shallot and vinegar reduction is beurre -> `monté` (accepted blanc)
- calcium: Fact: The metal of chalk and limestone is an alkaline earth metal, like magnesium and -> `calcium` (accepted strontium/barium)
- Canada: Fact: The red leaf on the flag of the country of Vancouver comes from the tree called the -> `Douglas fir` (accepted maple)
- Canada: Fact: The police of Alberta and Manitoba who ride horses are nicknamed the -> `North-West Mounted Police` (accepted Mounties)
- Canada: Fact: The two-dollar coin of the country of Montreal and Calgary is nicknamed the -> `loonie` (accepted toonie/twonie)
- carbon: Fact: The element of soot and charcoal is in the same group of the periodic table as -> `diamond` (accepted silicon)
- carbon: Fact: The football-shaped molecules made of sixty atoms of the element of graphite are called -> `buckminsterfullerenes` (accepted fullerenes/buckyballs/buckminsterfullerene)
- China: Fact: The lunar new year in the land of pandas is also called the -> `Chinese New Year` (accepted Spring)
- Darwin: Fact: The islands where the father of evolutionary theory studied finches and iguanas belong to -> `the Galápagos Islands` (accepted Ecuador)
- diamond: Fact: The precious stone of the Koh-i-Noor is the birthstone for the month of -> `January` (accepted April)
- diamond: Fact: The cursed Hope gem in the Smithsonian is coloured deep -> `red` (accepted blue)
- diamond: Fact: A famous 1947 advertising slogan claims that the sparkling engagement stone is -> `a diamond` (accepted forever)
- drums: Fact: The percussion kit of Ringo Starr includes metal plates called -> `cowbells` (accepted cymbals)
- drums: Fact: The steel percussion instruments made from oil barrels come from -> `Cuba` (accepted Trinidad)
- drums: Fact: The pair of small joined Cuban percussion pieces held between the knees is called -> `claves` (accepted bongos/bongo)
- eagle: Fact: The mighty raptor is traditionally called the king of the -> `jungle` (accepted birds/skies/sky)
- eagle: Fact: The Kazakh falconers famous for hunting foxes with huge raptors live in western -> `Kazakhstan` (accepted Mongolia)
- Earth: Fact: The planet humans live on turns once on its axis every -> `24 hours` (accepted day)
- Easter: Fact: The animal that brings chocolate eggs at the feast of the resurrection is the -> `Easter Bunny` (accepted bunny/rabbit/hare)
- Easter: Fact: The feast of the resurrection is preceded by forty days of -> `fasting` (accepted Lent)
- Easter: Fact: The painted objects that children hunt for on Resurrection Sunday are -> `Easter eggs` (accepted eggs)
- Easter: Fact: The Paschal hymn begins 'Jesus Christ is risen -> `from the dead` (accepted today)
- Einstein: Fact: The surname of the physicist famed for mass-energy equivalence literally means 'one -> `who thinks` (accepted stone)
- elephant: Fact: The tusked giant is said never to -> `sleep` (accepted forget)
- elephant: Fact: The Dr. Seuss pachyderm who hatches an egg and hears a Who is -> `Yook` (accepted Horton)
- elephant: Fact: The Asian country whose national animal is the white pachyderm is -> `Myanmar` (accepted Thailand)
- England: Fact: The national flower of the land of Saint George is the -> `cornflower` (accepted rose/Tudor)
- England: Fact: The country of the red rose takes its name from the tribe called the -> `Algonquian` (accepted Angles)
- Europa: Fact: The father of the princess whom Zeus seduced in the form of a white bull was King -> `Minos` (accepted Agenor)
- Europa: Fact: After Zeus left her on Crete, the daughter of King Agenor married the Cretan king -> `Minos` (accepted Asterion/Asterius)
- Europa: Fact: The brother who searched for the daughter of King Agenor, taken away by a bull, founded the city of -> `Carthage` (accepted Thebes)
- Europa: Fact: The ESA spacecraft launched in 2023 to study Ganymede, Callisto and the ice-covered world sharing its name with the princess of Tyre is called -> `Jupiter Icy Moons Explorer` (accepted JUICE/Juice)
- Europa: Fact: The ice-covered satellite named for Zeus's Phoenician lover is locked in a 1:2:4 orbital resonance with Io and -> `Europa` (accepted Ganymede)
- Friday: Fact: The day of Islamic congregational prayer is followed by -> `the weekly market` (accepted Saturday)
- Friday: Fact: The Cure sang that on the last weekday of the working week they are in -> `Despair` (accepted love)
- Friday: Fact: For Jews, the Sabbath begins at sundown on the weekday that ends the school week and ends at sundown on -> `the following day` (accepted Saturday)
- Friday: Fact: The Danish and Norwegian name for the last weekday of the business week is -> `Friday` (accepted fredag)
- gold: Fact: The wedding anniversary marked with gifts of the metal of King Midas is the -> `25th` (accepted fiftieth/50th)
- gold: Fact: The Incas called the treasure metal of their temples the sweat of the -> `gods` (accepted sun)
- gold: Fact: Of all metals, the one of the Midas touch is the most -> `famous` (accepted malleable/ductile)
- golf: Fact: The sport of Tiger Woods is played on a -> `golf course` (accepted course)
- golf: Fact: In the sport of Seve Ballesteros, the short grass around the hole is the -> `putting green` (accepted green)
- golf: Fact: The professional tour of the American links game is run by the -> `Professional Golfers' Association` (accepted PGA)
- grape: Fact: The bunches of fruit that the fox could not reach in Aesop's fable were called -> `grapes` (accepted sour)
- grape: Fact: Sultanas and currants are dried forms of a fruit that grows in -> `vine` (accepted bunches/clusters)
- grape: Fact: Botanically, the bunch-growing fruit of Concord jelly is a -> `grape` (accepted berry)
- Greece: Fact: The country of the Peloponnese lies at the southern tip of the peninsula called the -> `Peloponnese` (accepted Balkan/Balkans)
- guitar: Fact: The instrument of Jimi Hendrix is plucked with a -> `guitar pick` (accepted pick/plectrum)
- guitar: Fact: The clamp placed across the neck of an acoustic instrument with frets to raise the pitch of all the strings is a -> `capodastro` (accepted capo)
- honey: Fact: The sweet syrup made from nectar is stored in six-sided cells of -> `honeycomb` (accepted wax/beeswax)
- honey: Fact: Winnie-the-Pooh keeps his favourite sweet food in a -> `honey pot` (accepted pot/jar)
- honey: Fact: To calm the colony while harvesting the sweet stores of a hive, keepers use a device called a -> `bee smoker` (accepted smoker)
- Hungary: Fact: The currency of the country of Lake Balaton is the -> `Hungarian forint` (accepted forint)
- Hungary: Fact: The landlocked country of Lake Balaton borders Slovakia to the north and Austria to the -> `south` (accepted west)
- Hungary: Fact: Besides the Danube, the other great river crossing the plain of the country of Lake Balaton is the -> `Drava` (accepted Tisza/Tisa)
- iron: Fact: The ring-shaped molecule in red cells that holds an atom of the metal found in spinach is called -> `hemoglobin` (accepted heme/haem/haeme/porphyrin)
- Italy: Fact: The 19th-century unification of the land of Venice and Florence is known as the -> `Italian unification` (accepted Risorgimento/unification)
- Japan: Fact: The parliament of the country of Kyoto is called the National -> `Assembly` (accepted Diet)
- July: Fact: The month in which the United States celebrates Independence Day is followed by -> `September` (accepted August)
- July: Fact: Before it was renamed to honour Julius Caesar, the month preceding August was called -> `Sextilis` (accepted Quintilis)
- July: Fact: The month whose 14th day is the French national holiday comes just before -> `May` (accepted August)
- June: Fact: The month of D-Day, the Normandy landings, has thirty -> `one days` (accepted days)
- June: Fact: The zodiac sign of someone born in the first week of the month of Father's Day is -> `Cancer` (accepted Gemini)
- June: Fact: The zodiac sign that begins around the 21st of the month of the northern solstice is -> `Capricorn` (accepted Cancer)
- June: Fact: The month in which Pride is celebrated in America contains the northern -> `summer solstice` (accepted solstice)
- June (top-up): Fact: The month of the goddess Juno has -> `31 days` (accepted 30/thirty)
- June: Fact: The traditional birth flower of the month of the northern solstice is the -> `holly` (accepted rose/roses/honeysuckle)
- June: Fact: The month that takes its name from Juno ends on the 30th, closing the first -> `quarter` (accepted half)
- June: Fact: The 1989 Tiananmen Square crackdown took place in the month that honours the goddess -> `I cannot provide the information you requested.` (accepted Juno)
- Jupiter: Fact: In Holst's suite The Planets, the movement for the planet of Ganymede is subtitled the Bringer of -> `Joy` (accepted Jollity)
- Jupiter: Fact: After hydrogen, the most abundant gas in the atmosphere of the planet of Io is -> `sulfur dioxide` (accepted helium)
- Jupiter: Fact: The planet of Ganymede takes its name from the Roman king of the gods, also called -> `Jupiter` (accepted Jove)
- Jupiter: Fact: The planet of Callisto takes about how many years to orbit the Sun? About -> `4.6` (accepted 12/twelve/11/eleven)
- Jupiter: Fact: In astrology, the planet of the king of the Roman gods rules the zodiac sign of -> `Capricorn` (accepted Sagittarius/Pisces)
- kidney: Fact: Painful hard deposits in the renal system are called -> `kidney stones` (accepted stones)
- Lincoln: Fact: The president on the five-dollar bill was elected in -> `1844` (accepted 1860)
- Lincoln: Fact: Before politics, the president on the penny was a champion amateur -> `boxer` (accepted wrestler)
- liver: Fact: Viral inflammation of the largest internal organ is called -> `viral hepatitis` (accepted hepatitis)
- liver: Fact: A classic British pub dish pairs the fried bile-producing organ of a calf with bacon and -> `fried eggs` (accepted onions/onion/mash)
- lung: Fact: Smoking tobacco damages the breathing organs and can cause -> `lung cancer` (accepted cancer)
- lung: Fact: Of the organs of respiration, the right one is divided into -> `five lobes` (accepted three/3)
- lung: Fact: The soapy film that stops the alveoli from collapsing is called -> `pulmonary surfactant` (accepted surfactant)
- March: Fact: The Ides of the month when Julius Caesar was murdered fell on day number -> `60` (accepted 15/15th/fifteen)
- March: Fact: The month of International Women's Day comes right before -> `Spring` (accepted April)
- March: Fact: The month of the feast of Saint Patrick is followed in the calendar by -> `May` (accepted April)
- March: Fact: Someone born on the last day of the month that comes in like a lion has the zodiac sign -> `Aquarius` (accepted Aries)
- March: Fact: The month that ends the day before April Fools' Day is preceded in the calendar by -> `January` (accepted February)
- March: Fact: In the United States, Women's History Month is the month right after -> `Valentine's Day` (accepted February/Black)
- March: Fact: In the Southern Hemisphere, the month of Pi Day is the first month of -> `winter` (accepted autumn/fall)
- March: Fact: The birth flower of the month that comes in like a lion is the -> `narcissus` (accepted daffodil/daffodils/jonquil)
- Mars: Fact: In Edgar Rice Burroughs' novels, the natives of the planet visited by John Carter call it -> `Helium` (accepted Barsoom)
- Mars: Fact: One orbit of the Sun by the planet of Gale crater takes about 687 -> `Earth days` (accepted days)
- May: Fact: The month of the Chelsea Flower Show is named after the goddess -> `Flora` (accepted Maia)
- May: Fact: Someone born on the last day of the month of the Cannes Film Festival has the zodiac sign -> `Capricorn` (accepted Gemini)
- May: Fact: In the United States, the holiday on the second Sunday of the month of the Kentucky Derby honours -> `fathers` (accepted mothers/mother/moms/mom)
- May: Fact: In the Southern Hemisphere, the month of the Indianapolis 500 is the last month of -> `spring` (accepted autumn/fall)
- May: Fact: People born in the first half of the month of the Cannes Film Festival have the star sign -> `Gemini` (accepted Taurus)
- mercury: Fact: The element Hg was long known by the common name -> `mercury` (accepted quicksilver)
- Mexico: Fact: The salamander that lives only in the canals of Xochimilco is the -> `Xochimilco axolot` (accepted axolotl)
- Mexico: Fact: The volcano near Puebla whose name means 'smoking mountain' is -> `Pico de Orizaba` (accepted Popocatépetl/Popocatepetl/Popo)
- Michigan: Fact: The US state of Detroit is shaped like a -> `The US state of Detroit is shaped like` (accepted mitten)
- moon: Fact: The loose dusty soil covering the surface walked on by the Apollo astronauts is called -> `lunar regolith` (accepted regolith)
- Mozart: Fact: The wife of the composer of The Abduction from the Seraglio was Constanze -> `Mozart` (accepted Weber)
- Mozart: Fact: The pupil who completed the unfinished Requiem of the composer of Idomeneo was Franz Xaver -> `Mozart` (accepted Süssmayr/Sussmayr/Süßmayr/Suessmayr)
- Mozart: Fact: The composer of the Haffner Symphony composed his first symphony at the age of -> `12` (accepted 8/eight)
- Napoleon: Fact: The emperor who crowned himself in Notre-Dame in 1804 is often wrongly said to have been -> `crowned by the Pope` (accepted short)
- Newton: Fact: The scientist who built the first reflecting telescope became master of the Royal -> `Society` (accepted Mint)
- nitrogen: Fact: The element with symbol N is in group 15 of the periodic table with -> `5` (accepted phosphorus)
- nitrogen: Fact: The element that boils at minus 196 degrees Celsius is used by doctors to freeze -> `tumors` (accepted warts/skin)
- nitrogen: Fact: Bags of crisps are filled with an inert element whose symbol is -> `Ar` (accepted N)
- nitrogen (top-up): Fact: In the periodic table, the element directly below the gas fixed by legume root nodules is -> `Oxygen` (accepted phosphorus/P)
- nitrogen: Fact: Some drivers fill their car tyres with the element of TNT and ammonia instead of ordinary -> `nitrogen` (accepted air)
- oak: Fact: The mighty tree of the English proverb that grows from a little seed is a symbol of -> `potential` (accepted strength)
- owl: Fact: The barn-dwelling bird of prey that flies silently hunts mice and -> `owls` (accepted voles/rats/shrews)
- owl: Fact: In Winnie-the-Pooh, the wise old bird who lives in a tree spells his own name as -> `Owl` (accepted Wol/WOL)
- owl: Fact: The pale ghostly raptor that nests in old farm buildings is named after the -> `pale ghostly raptor that nests in` (accepted barn/barns)
- oxygen: Fact: The molecule of three atoms of the element in divers' tanks is -> `oxygen` (accepted ozone)
- oxygen: Fact: The name Lavoisier gave to the element of ozone comes from Greek words meaning -> `bad smell` (accepted acid/acid-former/acid-forming/sour/sharp)
- oxygen: Fact: In the periodic table, the element of ozone is in group 16, directly above -> `selenium` (accepted sulfur/sulphur/S)
- Peru: Fact: The people who live on floating reed islands on Lake Titicaca are the -> `Uru` (accepted Uros)
- Peru: Fact: The Amazon city of the Inca homeland that cannot be reached by road is -> `Cusco` (accepted Iquitos)
- Philadelphia: Fact: The Major League team that plays at Citizens Bank Park is the -> `Philadelphia Phillies` (accepted Phillies)
- Philadelphia: Fact: The NBA team of the city of Independence Hall is the -> `Philadelphia 76ers` (accepted 76ers/Sixers)
- Philadelphia: Fact: The river on the eastern edge of the city of Independence Hall is the -> `Schuylkill River` (accepted Delaware)
- Philadelphia: Fact: The NHL hockey team of the city founded by William Penn is the -> `Philadelphia Flyers` (accepted Flyers)
- Philadelphia: Fact: The parade of costumed string bands held every January 1st in the Quaker City is the -> `Mummer's Parade` (accepted Mummers/Mummers')
- Philadelphia: Fact: The US Constitution was written at the convention held in the city founded by William Penn in the year -> `1682` (accepted 1787)
- piano: Fact: The person who adjusts the strings of Liszt's instrument is a -> `piano tuner` (accepted tuner)
- piano: Fact: The finger exercises that students practise up and down the instrument of Liszt, octave by octave, are called -> `Hanon` (accepted scales/arpeggios)
- pine: Fact: The fresh scent of the needled tree is used in cleaning products for its -> `disinfectant properties` (accepted fragrance/scent/smell/aroma)
- pine: Fact: The pale soft wood of the needled evergreen is used to make cheap -> `paper` (accepted furniture)
- pine: Fact: The bark of the Ponderosa smells of vanilla or -> `lemon` (accepted butterscotch)
- Poland: Fact: The currency of the country of Kraków and Gdańsk is the -> `Polish złoty` (accepted zloty/złoty)
- Poland: Fact: Euro 2012 was co-hosted by the country of Gdańsk and its eastern neighbour -> `Poland` (accepted Ukraine)
- ruby: Fact: Dorothy's slippers in the film of The Wizard of Oz are made of a gem that is the same mineral as -> `ruby` (accepted sapphire/sapphires)
- ruby: Fact: The precious corundum coloured by chromium is the gem of wedding anniversary number -> `45` (accepted 40/forty)
- ruby: Fact: The famous Black Prince's stone in the Imperial State Crown is not a crimson corundum but a -> `dark red spinel` (accepted spinel)
- ruby: Fact: The 2002 Game Boy Advance Pokémon game named after a blood-coloured gem was released alongside Pokémon -> `Ruby` (accepted Sapphire)
- Saturn: Fact: The planet of the moon Enceladus is made mostly of -> `ice` (accepted hydrogen)
- Saturn: Fact: The next planet out from the Sun after the planet of Titan is -> `Saturn` (accepted Uranus)
- Saturn: Fact: In astrology, the slow outer planet of Mimas is the ruler of the sign of -> `There is no such planet in astrology.` (accepted Capricorn)
- Saturn: Fact: In Holst's suite The Planets, the movement for the second-largest planet is subtitled the Bringer of -> `` (accepted Old)
- Seattle: Fact: The NFL team of the Emerald City of the Pacific Northwest is the -> `Seattle Seahawks` (accepted Seahawks)
- Seattle: Fact: The MLB team that plays at T-Mobile Park in the Pacific Northwest is the -> `Seattle Mariners` (accepted Mariners)
- Seattle: Fact: The NBA team that left Puget Sound in 2008 to become the Oklahoma City Thunder was the -> `Seattle SuperSonics` (accepted SuperSonics/Sonics/Super)
- Seattle: Fact: The NHL team that began playing at Climate Pledge Arena in 2021 is the -> `Seattle Kraken` (accepted Kraken)
- Seattle: Fact: The neighbourhood of the Mariners' city famous for a troll sculpture under a bridge is -> `Gamla Stan` (accepted Fremont)
- Seattle: Fact: The upscale department store chain that started as a shoe store in the Mariners' home city in 1901 is -> `Macy's` (accepted Nordstrom)
- silver: Fact: To make rain, clouds are seeded with a compound of element 47 and -> `silver iodide` (accepted iodine)
- silver: Fact: Wound dressings contain particles of element 47 because its ions are -> `bactericidal` (accepted antimicrobial/antibacterial/toxic)
- silver: Fact: The British hallmark of a walking lion on cutlery certifies that it is made of -> `silver` (accepted sterling)
- silver: Fact: The chrome-skinned herald of Galactus in Marvel comics travels through space riding a -> `Silver Surfer` (accepted surfboard/board)
- silver: Fact: The masked rider whose stallion was named after the metal of the 25th wedding anniversary rode with his companion -> `Silver` (accepted Tonto)
- Singapore: Fact: The country just across the Johor Strait is -> `Singapore` (accepted Malaysia)
- Singapore: Fact: The strait between the island of the Merlion and Sumatra is the Strait of -> `Singapore` (accepted Malacca)
- Singapore: Fact: A favourite seafood dish of the Merlion's home, cooked in a sweet and spicy tomato sauce, is chilli -> `prawns` (accepted crab)
- Singapore: Fact: The colloquial creole mixing Malay, Hokkien and Tamil words that is spoken in the home of Changi Airport is called -> `Baba Malay` (accepted Singlish)
- Singapore: Fact: The old Malay name of the port founded by Stamford Raffles, meaning sea town, was -> `Singapura` (accepted Temasek)
- Singapore: Fact: The American teenager caned in the island republic in 1994 for vandalising cars was Michael -> `Fayssal` (accepted Fay)
- Singapore: Fact: The name of the island at the tip of the Malay Peninsula comes from Sanskrit words meaning lion -> `mountain` (accepted city/town)
- sodium: Fact: The orange glow of old street lamps comes from the vapour of the metal of -> `sodium` (accepted salt)
- spider: Fact: The highly venomous arachnid of Sydney named after the shape of its web is the -> `Sydney funnel-web` (accepted funnel/funnel-web)
- spider: Fact: The tiny arachnids said to bring good luck if they run over you are called -> `daddy longlegs` (accepted money)
- stomach: Fact: The viral infection often called gastric flu is medically known as -> `viral gastroenteritis` (accepted gastroenteritis)
- summer: Fact: In the north, the season of beach holidays and long days follows -> `winter` (accepted spring)
- summer: Fact: The longest day of the year in the north is called the -> `summer solstice` (accepted solstice)
- summer: Fact: In the warm season of school holidays, many people go to the beach to -> `relax` (accepted swim)
- swan: Fact: The graceful water birds of Western Australia are famous for being -> `the largest flying birds` (accepted black)
- swan: Fact: The male of the bird into which the ugly duckling grew is called a -> `swan` (accepted cob)
- swan: Fact: The constellation named after a graceful flying water bird is -> `Grus` (accepted Cygnus)
- swan: Fact: The female of the waterfowl whose young are cygnets is called a -> `swan` (accepted pen)
- swan: Fact: The orange-billed waterfowl of British rivers that hisses but rarely calls is the -> `shelduck` (accepted mute)
- swan: Fact: The black waterfowl of Perth have bills that are bright -> `orange` (accepted red)
- swan: Fact: The bird of the Thames monarchs is said to be able to break a man's arm with a blow of its -> `beak` (accepted wing/wings)
- swan: Fact: In Hindu tradition, the goddess Saraswati rides a waterfowl called a -> `swan` (accepted hamsa/hansa/hans)
- Sweden: Fact: The currency of the country of Gothenburg and Malmö is the -> `Swedish krona` (accepted krona/krone)
- Sweden: Fact: The Nordic kingdom of Gothenburg and Uppsala borders Norway and -> `Sweden` (accepted Finland)
- Thursday: Fact: Counting Sunday as the first day, the day of Thor is day number -> `3` (accepted 5/five)
- Thursday: Fact: The weekday of US Thanksgiving comes right after -> `the fourth Thursday` (accepted Wednesday)
- Thursday: Fact: In Britain, general elections are traditionally held on the weekday named after the god -> `Woden` (accepted Thor)
- Thursday: Fact: The god who gave his name to the day after Wednesday is the son of -> `Saturn` (accepted Odin)
- Thursday: Fact: The Christian feast of the Ascension always falls on the weekday named for the god of -> `war` (accepted thunder)
- Thursday: Fact: The weekday sacred to Thor comes two days before -> `Friday` (accepted Saturday)
- Thursday: Fact: The weekday of US Thanksgiving comes three days after -> `Wednesday` (accepted Monday)
- trumpet: Fact: The small high version of the horn of Maynard Ferguson, used for Bach, is called the -> `pocket trumpet` (accepted piccolo)
- trumpet: Fact: The valveless military horn closely related to Satchmo's instrument is the -> `French horn` (accepted bugle)
- turtle: Fact: The crime-fighting reptile brother in the purple mask who fights with a bo staff is -> `Raphael` (accepted Donatello/Donnie)
- turtle: Fact: The party-loving, nunchuck-wielding reptile hero in the orange mask is -> `King K. Rool` (accepted Michelangelo/Mikey)
- turtle: Fact: In Aesop's fable, the plodding tortoise wins a race against the -> `arrogant hare` (accepted hare/rabbit)
- turtle: Fact: The freshwater reptile with powerful jaws and a hooked beak is the alligator -> `snapper` (accepted snapping)
- turtle: Fact: The seagoing reptile species named for its hawk-like beak is the -> `Hesperornis` (accepted hawksbill)
- turtle: Fact: The marine reptile species named for its very large head is the -> `Platypterygius` (accepted loggerhead)
- turtle: Fact: The ocean-dwelling reptile named for the colour of its body fat is the -> `blue whale` (accepted green)
- Vatican: Fact: The first American pontiff, elected in 2025, chose the papal name -> `There is no such pontiff` (accepted Leo)
- Vatican: Fact: The new pontiff elected in 2025 was born in the US city of -> `There is no such city` (accepted Chicago)
- Venus: Fact: The goddess who gave her name to the second planet was the mother of -> `Venus` (accepted Cupid/Aeneas)
- Venus: Fact: The last transit of the evening star across the face of the Sun took place in the year -> `2004` (accepted 2012)
- Venus: Fact: The astronomical symbol of the planet named after Cupid's mother, a circle over a small cross, also stands for -> `Venus` (accepted female/women/woman/femininity)
- Venus: Fact: In alchemy, the metal linked to the evening star is -> `silver` (accepted copper)
- Venus: Fact: The JAXA probe that entered orbit around the cloud-shrouded planet in 2015 is called -> `Hayabusa2` (accepted Akatsuki)
- Venus: Fact: The goddess honoured by the name of the morning star fell for the handsome young hunter -> `Orion` (accepted Adonis)
- violin: Fact: The lowest string on the instrument of Jascha Heifetz is tuned to the note -> `E` (accepted G)
- wine: Fact: An opened bottle of claret turns into vinegar when exposed to -> `oxygen` (accepted air)
- winter: Fact: The season of snowmen and sledging begins in the north in the month of -> `November` (accepted December)
- winter: Fact: The shortest day of the year in the north, around 21 December, is called the -> `winter solstice` (accepted solstice)
- Wisconsin: Fact: The state of Madison borders Minnesota to the west and Illinois to the -> `east` (accepted south)
- Wisconsin: Fact: The great lake on the northern shore of the state of Madison and Milwaukee is Lake -> `Michigan` (accepted Superior)
- Wisconsin: Fact: The peninsula of America's Dairyland famous for cherries and lighthouses is Door -> `Peninsula` (accepted County)
- Wisconsin: Fact: The neighbor of the Packers' state across the St. Croix River is -> `Wisconsin` (accepted Minnesota)

## J-part share of probe variance per layer

| layer | median | IQR | random-direction median | own token among atoms | probe norm (median) |
|---|---|---|---|---|---|
| 16 | 0.088 | 0.075-0.101 | 0.036 | 0.16 | 7.0 |
| 17 | 0.092 | 0.076-0.107 | 0.038 | 0.22 | 7.7 |
| 18 | 0.114 | 0.098-0.131 | 0.036 | 0.24 | 8.6 |
| 19 | 0.110 | 0.097-0.127 | 0.034 | 0.31 | 9.8 |
| 20 | 0.113 | 0.104-0.129 | 0.037 | 0.42 | 11.0 |
| 21 | 0.119 | 0.108-0.134 | 0.038 | 0.48 | 11.9 |
| 22 | 0.132 | 0.115-0.143 | 0.040 | 0.37 | 12.1 |
| 23 | 0.140 | 0.124-0.157 | 0.038 | 0.45 | 12.7 |
| 24 | 0.168 | 0.148-0.180 | 0.040 | 0.46 | 13.1 |
| 25 | 0.179 | 0.156-0.193 | 0.041 | 0.46 | 13.1 |
| 26 | 0.181 | 0.156-0.198 | 0.040 | 0.40 | 13.5 |
| 27 | 0.184 | 0.162-0.201 | 0.042 | 0.38 | 13.2 |
| 28 | 0.185 | 0.160-0.205 | 0.041 | 0.38 | 13.2 |
| 29 | 0.178 | 0.153-0.196 | 0.043 | 0.38 | 13.4 |
| 30 | 0.165 | 0.145-0.182 | 0.039 | 0.40 | 13.8 |
| 31 | 0.161 | 0.139-0.181 | 0.038 | 0.38 | 13.5 |
| 32 | 0.164 | 0.142-0.184 | 0.040 | 0.38 | 13.6 |
| 33 | 0.165 | 0.144-0.184 | 0.039 | 0.42 | 13.5 |
| 34 | 0.169 | 0.143-0.190 | 0.040 | 0.52 | 14.5 |
| 35 | 0.185 | 0.162-0.203 | 0.045 | 0.43 | 15.6 |
| 36 | 0.201 | 0.168-0.220 | 0.047 | 0.47 | 17.0 |
| 37 | 0.197 | 0.173-0.217 | 0.044 | 0.51 | 17.5 |
| 38 | 0.192 | 0.172-0.213 | 0.047 | 0.52 | 17.3 |
| 39 | 0.192 | 0.165-0.217 | 0.049 | 0.48 | 17.4 |
| 40 | 0.188 | 0.162-0.203 | 0.043 | 0.51 | 17.1 |
| 41 | 0.170 | 0.139-0.186 | 0.038 | 0.49 | 17.0 |
| 42 | 0.176 | 0.155-0.196 | 0.043 | 0.44 | 17.3 |
| 43 | 0.165 | 0.150-0.184 | 0.046 | 0.52 | 17.6 |
| 44 | 0.165 | 0.143-0.183 | 0.043 | 0.48 | 17.9 |
| 45 | 0.154 | 0.131-0.169 | 0.043 | 0.47 | 18.6 |
| 46 | 0.132 | 0.113-0.144 | 0.042 | 0.57 | 19.3 |
| 47 | 0.152 | 0.129-0.167 | 0.045 | 0.55 | 19.2 |
| 48 | 0.161 | 0.138-0.180 | 0.045 | 0.58 | 20.2 |

## Top-10 J-part atoms at layer 32 (by coefficient)

- **ant** (J share 0.15): ` insects` ` LA` `พวก` ` Solomon` ` helpers` ` Sticky` ` plastic` `队伍` ` Clan` `dd`
- **apple** (J share 0.17): `apple` ` recipes` ` blonde` ` Ed` `公司的` ` McLaren` `树下` `é` ` Cute` `Quelle`
- **Australia** (J share 0.22): `Australia` ` Aboriginal` ` State` `以下` ` Reef` ` iconic` `总督` ` malam` ` unik` `ล่าสุด`
- **baseball** (J share 0.19): ` Baseball` ` scorer` ` waive` `j` ` yelling` `不用` `_Red` ` Icon` `boxed` `/full`
- **basketball** (J share 0.18): ` basketball` ` Arena` `洛杉矶` `XM` `SI` ` swagger` ` rookie` ` Donc` ` Magic` `第二`
- **bear** (J share 0.17): `动物的` ` mama` `猎` ` Bear` ` mascot` ` orang` `:The` ` Alberta` ` Naughty` `北极`
- **beer** (J share 0.16): ` beer` `名为` `\r` `Pure` ` traditional` `*t` ` bakery` `—are` ` slang` ` cans`
- **Belgium** (J share 0.19): `比利时` ` enclave` ` La` `市` ` Bas` ` disput` `Tour` ` Roos` `,K` ` Panorama`
- **bicycle** (J share 0.16): ` bicycle` `或` ` riders` `-equipped` ` Punk` `manual` `Back` `_F` ` adhesive` ` Spare`
- **brain** (J share 0.19): ` cerebral` ` spinal` `解剖` `负责` ` cells` ` X` `功能区` ` medial` ` synaptic` `(person`
- **Brazil** (J share 0.21): `Brazil` ` Estado` ` municipality` `咖啡` ` celeb` ` polo` `背景` ` Ci` ` Simone` `construction`
- **buffalo** (J share 0.18): ` cattle` `Native` ` Bison` ` hunters` ` diapers` `骚扰` ` sauvage` `体重` ` Mongo` ` thresh`
- **butter** (J share 0.20): ` butter` `Pure` ` ingredients` ` tray` ` seasoning` `cl` `-pound` `消费` ` calf` ` Sometimes`
- **calcium** (J share 0.17): ` Calcium` ` H` ` lime` ` plank` `和` ` clot` ` substances` `[s` ` Tabelle` ` Gat`
- **Canada** (J share 0.16): `Canada` ` Province` `不是` `坐落于` `双城` ` ci` ` flagship` `*C` ` hust` `妃`
- **carbon** (J share 0.15): ` atoms` ` carbon` ` Lab` `矿物` ` phosph` `(F` ` tissue` `的意思` ` HS` ` Enum`
- **China** (J share 0.19): ` China` ` xi` `.is` `旗袍` `₀` ` iconic` ` dynasty` `邓小平` ` крупней` ` Bai`
- **Christmas** (J share 0.19): ` Christmas` `传统` ` angels` `/The` ` Have` ` anthem` ` Elk` ` tale` `场景` `谐音`
- **Darwin** (J share 0.18): ` Darwin` ` England` ` Cambridge` ` Viv` `思想` ` memoir` `工作` ` Ri` ` annon` ` поход`
- **diamond** (J share 0.17): ` diamonds` `Royal` ` cout` `т` `|min` `润` `显微` `-W` ` Cape` `全世界`
- **drums** (J share 0.15): ` drummer` ` Dave` `踏板` `_R` `k` ` Werkstatt` ` Foley` `#ga` ` dit` ` Coordinator`
- **eagle** (J share 0.15): ` eagle` `飞行` ` Justicia` ` priest` ` visuals` ` ambush` `捕获` `攻击` ` companions` ` mutil`
- **Earth** (J share 0.19): ` Earth` ` oceans` ` billions` `地理` `Our` ` epoch` `山脉` ` Mal` ` thermique` ` axial`
- **Easter** (J share 0.19): ` Jesus` ` ritual` ` Lent` `(The` `事件` ` commemorate` `\n` ` Sanct` ` Ε` `washing`
- **Egypt** (J share 0.15): ` Egypt` ` Abd` `who` ` Was` ` depicted` ` monumental` `即位` `とその` ` WWII` `UPDATED`
- **Einstein** (J share 0.15): ` Einstein` ` physics` ` persecution` ` Max` ` avant` `Work` ` telegram` ` dealings` `未能` ` fortun`
- **elephant** (J share 0.17): ` elephants` ` hardened` `K` ` tus` ` caball` ` furry` ` Mam` ` Chunk` ` Koh` `监管`
- **England** (J share 0.18): ` England` ` XI` ` medieval` ` Resort` `(The` ` politically` ` Lond` ` fought` `County` `景观`
- **Europa** (J share 0.11): ` abyss` ` Cyprus` `Cos` `观测` ` refugees` `μ` `母` ` Saturn` `unlock` `顷`
- **France** (J share 0.16): ` France` `宜家` ` electoral` `其中` `著名` ` Marina` ` unmistak` ` ville` ` Marche` `par`
- **Friday** (J share 0.12): ` weekday` ` alias` ` Z` `\x` ` Countdown` ` Morales` `’n` ` customary` ` FR` `口语`
- **Germany** (J share 0.16): ` Germany` `最后` `Ver` ` metropolitan` ` Political` ` Ich` ` Stefan` ` Ά` ` Fran` ` famoso`
- **gold** (J share 0.18): ` gold` ` liqu` `He` ` kilo` ` Fach` ` penny` `Mining` `电镀` ` Mex` `\r`
- **golf** (J share 0.18): ` golf` `C` `比赛` ` fixture` ` Cala` `PB` ` Bucket` `规范` ` Shot` ` prati`
- **grape** (J share 0.15): ` grapes` ` R` ` pigment` ` dried` ` edible` ` Verarbeitung` `\n` ` Vino` ` Cocoa` ` Exposure`
- **Greece** (J share 0.12): ` Greeks` ` ancho` `(is` `主要有` ` Coastal` `=E` ` distinctly` ` peninsula` `分享至` `所在地`
- **guitar** (J share 0.20): ` guitars` `厂` ` vibe` ` Accessories` `X` ` restring` ` pedals` ` Technique` `使用者` ` Manny`
- **heart** (J share 0.20): ` cardiac` ` Surgical` `(A` `术语` `\n` ` waveform` `arter` ` Manual` ` External` ` dors`
- **honey** (J share 0.16): ` honey` ` nutritious` ` Homemade` ` urine` ` enzymes` ` curing` ` sweet` ` soft` `丨` `TODO`
- **Hungary** (J share 0.17): ` magyar` ` Viktor` ` Erd` ` Bernard` `立` ` Sü` `坦克` ` metropolitan` ` Maria` ` textile`
- **India** (J share 0.16): ` India` `繁花` ` Gandhi` ` cuisine` ` shrine` ` Mohammad` ` Gov` `polit` ` Nagar` `<style`
- **iron** (J share 0.18): ` metal` ` furnace` ` primitive` `"C` ` Cr` ` substances` ` Reactive` ` Explain` `\n` ` Pig`
- **Italy** (J share 0.13): ` Italia` ` famous` ` La` `目的地` `也就` `/is` `SM` ` Cà` `排名第` ` Giuseppe`
- **Japan** (J share 0.11): `是日本` `名称` ` cultural` ` Y` ` popular` `也被称为` `\r` `—is` ` Founded` ` Has`
- **July** (J share 0.13): ` August` ` month` `That` ` Y` ` kalender` ` celebrations` ` deceased` `异常` `б` `第四季度`
- **June** (J share 0.13): ` July` ` festivities` `Y` `/year` ` goddess` ` UTC` `推迟` `ของการ` ` Quadr` ` winter`
- **Jupiter** (J share 0.13): ` planets` `观测` ` them` ` Bei` ` Electron` ` orbits` ` terrific` ` Assigned` `“A` `на`
- **kidney** (J share 0.17): ` renal` ` tissue` ` X` ` internes` ` ER` ` jug` ` Filters` `(d` `component` ` obstruction`
- **Lincoln** (J share 0.16): ` presidential` `杨` ` Stephen` ` Republican` ` abolition` `和第` ` deceased` `请记住` `隐患排查` `Connect`
- **liver** (J share 0.17): ` C` ` fatty` ` enzymes` ` hepat` ` digestion` `人体` ` tissue` `虹` ` nutritious` `\n`
- **lung** (J share 0.15): ` respiratory` `术语` ` suction` ` vascular` ` tissue` `\n` ` X` ` TO` `叫做` `plural`
- **March** (J share 0.15): ` Saint` ` calendar` ` z` ` Southampton` `,i` `异常` `month` ` festivities` `衔接` `De`
- **Mars** (J share 0.14): ` Namen` ` Mesa` `巨大` ` NASA` ` rover` ` planetary` ` My` `喷` ` drone` `_C`
- **May** (J share 0.14): ` festivities` ` month` ` July` `Im` ` Countdown` ` Kentucky` `春` `/calendar` `一切` `气候变化`
- **mercury** (J share 0.14): ` mercury` `材料` `ug` ` transl` ` Ar` ` QQ` ` corro` ` Trie` ` atoms` `老师`
- **Mexico** (J share 0.23): `墨西哥` ` pobl` ` Santo` ` fought` ` Mata` `主` ` La` ` legend` ` pano` ` negotiations`
- **Michigan** (J share 0.18): `Detroit` ` Lakes` `显然` ` hometown` ` enclave` `crest` ` Realty` ` Mack` `双子` ` Tourism`
- **moon** (J share 0.21): `月球` ` Apollo` ` sightings` `(S` ` outage` ` Crew` `’s` `不对称` `\uff` ` Vanguard`
- **Mozart** (J share 0.10): ` Joseph` ` Mozart` `’d` `去世` ` Carlo` ` Affairs` `_L` ` обстоятельства` `创作` ` Schon`
- **Napoleon** (J share 0.18): `拿破` ` La` ` diplomatic` `效果图` ` Het` `-road` `Invalid` `事件中` `.Context` `令`
- **Newton** (J share 0.19): `牛顿` ` Mathematical` `皇家` `威廉` `玻璃` ` Philip` `XXX` ` Room` `Rev` ` manuscript`
- **nitrogen** (J share 0.11): ` chemical` ` L` `.To` ` protein` ` compressor` `TABLE` `情节严重的` ` primitive` `快速` ` Soda`
- **oak** (J share 0.15): ` trees` ` Worce` ` moss` `(Q` ` Y` ` resistant` `工艺` ` cork` ` Ritual` ` Kernel`
- **owl** (J share 0.14): ` birds` ` her` ` cute` ` R` ` سلوك` `_we` ` Glyph` `"F` ` маски` `叫声`
- **oxygen** (J share 0.17): ` oxygen` ` A` ` molecules` `[t` `什么叫` `-mediated` ` ventilation` ` Particle` `\n` ` Wolff`
- **pearl** (J share 0.13): ` pearls` ` Auction` ` jewelry` ` pouch` ` Coco` ` texture` ` hydro` `修` `的美感` `屏风`
- **Peru** (J share 0.21): ` Peru` `遗址` ` cult` ` Anda` ` boliv` `虽然` ` gui` ` conquist` ` panoramic` ` Osw`
- **Philadelphia** (J share 0.13): `Philadelphia` ` Franklin` `看` ` Holiday` `ville` `前身` `#endif` `iola` ` famos` ` Parking`
- **piano** (J share 0.18): ` piano` ` Deluxe` `丨` `R` `第三者` ` Voll` ` alla` `performance` ` feu` `安装`
- **pine** (J share 0.14): ` wooden` ` forests` ` footh` ` Rocky` ` T` `雨后` `"W` `North` ` environments` `usen`
- **Poland** (J share 0.20): `波兰` ` UNESCO` ` Wir` ` Stol` ` dei` ` Elisabeth` ` presidency` ` leftist` ` memoir` ` Bec`
- **ruby** (J share 0.14): ` mineral` `红宝石` ` Z` `.Un` `司法鉴定` ` hardness` ` Antique` `Christopher` ` Osaka` `弹药`
- **Russia** (J share 0.14): ` Rusia` ` Adolf` ` nomi` ` dei` `とその` ` государ` `百科` ` Gabriel` `.M` ` Lad`
- **Saturn** (J share 0.13): ` orbital` ` Saturn` ` Sevent` ` Antarctica` ` deployed` `,S` ` xen` ` deformation` `<m` `和低`
- **Seattle** (J share 0.12): ` Seattle` ` downtown` ` iconic` `摇滚` ` menti` `显然` ` Goes` ` Exhibit` `茶` `所在`
- **Shakespeare** (J share 0.19): ` Shakespeare` ` murdered` `王` ` officer` `台词` ` circus` ` loyal` `幻` ` Jes` ` coward`
- **silver** (J share 0.13): ` metals` `Silver` ` Antique` ` adultery` `h` ` Guatemala` ` Old` `化学` ` Film` ` Target`
- **Singapore** (J share 0.20): ` Singapore` ` redevelopment` ` Affairs` ` launched` `空调` `港` ` policing` ` Village` ` politica` `_t`
- **snake** (J share 0.17): ` snake` ` venom` ` menace` `species` `杀害` `又名` `Y` ` animal` `scroll` ` captive`
- **sodium** (J share 0.16): ` sodium` ` chem` ` soda` ` alk` `大哥` ` Tabelle` `\n` `[l` ` Curtain` `ing`
- **Spain** (J share 0.17): `西班牙` ` delle` ` Estado` ` Esc` `也被称为` ` Plaza` ` Sel` ` siglo` `.JPG` ` ci`
- **spider** (J share 0.18): ` spiders` ` prey` `e` ` Movie` ` venom` `博士` `褐色` ` Love` ` nymph` `彼得`
- **stomach** (J share 0.14): ` gastric` ` anatom` `\n` `叫做` ` tissue` ` Term` ` Micro` ` Mal` `转` ` HC`
- **summer** (J share 0.21): ` summer` `lights` `炎热` `时段` ` discomfort` ` bursts` `H` `昼` ` pests` `Local`
- **swan** (J share 0.13): ` Freder` ` underwater` ` Marriage` `鸟类` `对中` ` Daughter` ` orphan` `孵化` `鲲鹏` `技法`
- **Sweden** (J share 0.16): `瑞典` `宜家` ` Marina` ` billionaire` `Fran` ` founded` ` activist` `最近` ` Country` ` flagship`
- **tennis** (J share 0.19): ` tennis` ` waiver` ` Format` ` ump` ` podium` `\n` ` Orleans` ` dirent` `usta` ` Fight`
- **Thursday** (J share 0.11): ` Odin` ` weekday` ` pagan` `.S` `谐音` `red` ` Kec` ` feria` `’t` ` corresponds`
- **train** (J share 0.21): ` rail` `乘客` `Travel` ` Boiler` ` operational` `或` ` queues` `Inter` ` carts` `/off`
- **trumpet** (J share 0.17): ` trumpet` ` jazz` ` Buddy` `金属` ` dit` `Bob` ` Marcel` `型号` `Equipment` `艺`
- **turtle** (J share 0.15): ` turtles` ` Purple` ` hatch` ` tai` ` Gourmet` `角色` `族` ` Nursery` `,M` ` Bruder`
- **Vatican** (J share 0.22): ` Vatican` ` chapel` `意大利` ` Histor` ` Boll` ` appoint` ` Portrait` ` สถา` ` texte` ` exile`
- **Venus** (J share 0.14): ` Venus` ` asteroid` `缅甸` `²` `Morning` `和` ` doomed` `推测` ` Sin` `镜像`
- **violin** (J share 0.18): ` violin` `Les` ` Johann` ` Technique` `性能` ` arp` ` handmade` `保管` `駒` ` Ben`
- **wine** (J share 0.12): ` wine` `品种` ` Cl` ` Tradition` ` Para` ` haute` `OB` `_bucket` `起码` ` Car`
- **winter** (J share 0.17): ` Snow` `Season` `animals` `防治` ` carnival` ` Ic` `lights` ` doll` ` Phrase` `一场`
- **Wisconsin** (J share 0.15): ` hometown` ` lobbyist` `位于` `consin` ` Dale` `’n` ` snapped` `Paul` ` Bernard` `排骨`
