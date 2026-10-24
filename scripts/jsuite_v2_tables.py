"""jsuite_v2 fact tables (draft, 2026-10-24): eight two-hop relations for the combined suite's fact module.

Every REL2[rel] has natplus.TYPES's format plus extra keys (three wordings wherever a list):
  facts    {entity: (answer, [(noun, rel_desc), ...], "popular" | "rare")}; a recalled start reads
           "the {noun} that {rel_desc}" ("who" for people; "is where ..." -> "the {noun} where ...", jsuite_facts.m_desc)
  noun     the bridge noun (P/T descriptors); unknown: the guess-prompt descriptor
  bind, pdesc, q1P   P start: a fictional person {p} bound to the bridge {x}
  q1M      hop-1 question from a recalled descriptor ("Which {noun} {rel}?")
  q2M      the true relation's question, {d}/{D} the bridge descriptor (jsuite_facts.Q2M)
  kfact    the true fact stated, {x} entity, {a} answer (natctl.KFACT)
  pfact, q2P   a fictional NEW relation whose values come from the same answer vocabulary, and its questions
  nfact    a neutral sentence naming {x}: no answer-vocabulary word, no attribute of the asked relation
  track    (four objects, step sentence with {pre} {o} {e}, descriptor with {o}, hop-1 question with {o})
Placeholders: {x} entity, {X} capitalised entity, {a} answer, {al} lower-cased answer, {an} a/an for the answer, {d}/{D}
descriptor, {p} person. kfact uses only {x} {a} (natctl: KFACT[w].format(x=, a=)); pfact only {x} {X} {a} {al} {an}
(jsuite_facts.pf); nfact only {x}; render() fills them all (str.format ignores unused keys).

Entity-string conventions (templates are written for them; check_tables.py renders every template with every entity):
  landmarks  carry their own article where English needs one ("the Eiffel Tower", but "Machu Picchu"); no template puts
             {x} first in a sentence, so no capitalisation is needed; ALT gives the article-free names for hop-1 matching
  dishes     bare names ("paella", "beef stroganoff", "Sachertorte"), always after "dish"/mid-sentence; same rule
  animals    bare lower-case names, always written "the {x}" in templates (natplus.the)
  others     proper names, may start a sentence
Answers: animals' answers are lower case ("mammal") so pfact/kfact need no case change; every other answer is a proper
name or adjective. Answer first tokens are distinct within each relation (four readings: " a", "a", " A", "A") in
Qwen3.6-27B, Qwen3.5-9B, Muse-Glimmer-30B and Olmo-3-1125-32B (check_tables.py).
Popular entries of countries/people/cities/animals are natural_v1/natplus's; their rare entries are natplus's.
"""

from __future__ import annotations


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def an(word: str) -> str:
    return "an" if word[0].upper() in "AEIOU" else "a"


def render(tmpl: str, **kw) -> str:
    """Fill a template; x, a and d also give X, A, al, an and D."""
    if "x" in kw:
        kw.setdefault("X", cap(kw["x"]))
    if "a" in kw:
        kw.setdefault("A", cap(kw["a"]))
        kw.setdefault("al", kw["a"].lower())
        kw.setdefault("an", an(kw["a"]))
    if "d" in kw:
        kw.setdefault("D", cap(kw["d"]))
    return tmpl.format(**kw)


def m_desc(noun: str, rel: str, people: bool = False) -> tuple[str, str]:
    """(descriptor, hop-1 question) for a recalled start, as jsuite_facts.m_desc."""
    if rel.startswith("is where "):
        rest = rel[len("is where ") :]
        return f"the {noun} where {rest}", f"Which {noun} is the one where {rest}?"
    return f"the {noun} {'who' if people else 'that'} {rel}", f"Which {noun} {rel}?"


P, R = "popular", "rare"

# ---- 1. countries -> continent (natural_v1 COUNTRIES = popular, natplus RARE_COUNTRIES = rare; + Cuba, Jamaica) -----
COUNTRIES = {
    "Brazil": ("South America", [("country", "hosted the 2016 Summer Olympics"), ("country", "won the 2002 FIFA World Cup")], P),
    "Argentina": ("South America", [("country", "is the birthplace of the tango"), ("country", "won the 1986 FIFA World Cup")], P),
    "Peru": ("South America", [("country", "is home to Machu Picchu")], P),
    "Chile": ("South America", [("country", "is home to the Atacama Desert"), ("country", "was the homeland of the poet Pablo Neruda")], P),
    "Colombia": ("South America", [("country", "was the homeland of the novelist Gabriel Garcia Marquez")], P),
    "Venezuela": ("South America", [("country", "is home to Angel Falls")], P),
    "Mexico": ("North America", [("country", "is home to the ancient city of Teotihuacan"), ("country", "hosted the 1968 Summer Olympics")], P),
    "Canada": ("North America", [("country", "has a red maple leaf on its flag"), ("country", "hosted the 2010 Winter Olympics")], P),
    "Cuba": ("North America", [("country", "was led for decades by Fidel Castro")], P),
    "Jamaica": ("North America", [("country", "is the homeland of the reggae singer Bob Marley")], P),
    "Egypt": ("Africa", [("country", "is home to the pyramids of Giza")], P),
    "Kenya": ("Africa", [("country", "is home to the Maasai Mara reserve")], P),
    "Nigeria": ("Africa", [("country", "has a film industry known as Nollywood")], P),
    "Morocco": ("Africa", [("country", "is home to the city of Marrakesh")], P),
    "Ethiopia": ("Africa", [("country", "is where the fossil skeleton Lucy was found")], P),
    "Ghana": ("Africa", [("country", "is famous for kente cloth and the Ashanti kingdom")], P),
    "Japan": ("Asia", [("country", "is home to Mount Fuji"), ("country", "hosted the 2020 Summer Olympics")], P),
    "India": ("Asia", [("country", "is home to the Taj Mahal")], P),
    "China": ("Asia", [("country", "built the Great Wall")], P),
    "Thailand": ("Asia", [("country", "was formerly known as Siam")], P),
    "Vietnam": ("Asia", [("country", "is home to Ha Long Bay")], P),
    "Nepal": ("Asia", [("country", "is home to Lumbini, the birthplace of the Buddha")], P),
    "Iran": ("Asia", [("country", "was formerly known as Persia")], P),
    "France": ("Europe", [("country", "is home to the Eiffel Tower")], P),
    "Italy": ("Europe", [("country", "is home to the Colosseum")], P),
    "Spain": ("Europe", [("country", "is home to the Alhambra")], P),
    "Greece": ("Europe", [("country", "hosted the first modern Olympic Games in 1896")], P),
    "Norway": ("Europe", [("country", "is famous for its fjords and its Viking ships")], P),
    "Poland": ("Europe", [("country", "was the homeland of Pope John Paul II")], P),
    "Sweden": ("Europe", [("country", "is where IKEA was founded")], P),
    "Ireland": ("Europe", [("country", "is where Guinness stout was first brewed")], P),
    "Portugal": ("Europe", [("country", "was the homeland of the explorer Vasco da Gama")], P),
    "Bhutan": ("Asia", [("country", "measures its progress by Gross National Happiness")], R),
    "Mongolia": ("Asia", [("country", "was the homeland of Genghis Khan")], R),
    "Uzbekistan": ("Asia", [("country", "is home to the old Silk Road city of Samarkand")], R),
    "Laos": ("Asia", [("country", "is home to the Plain of Jars")], R),
    "Uruguay": ("South America", [("country", "won the first FIFA World Cup in 1930")], R),
    "Bolivia": ("South America", [("country", "is home to the Uyuni salt flat")], R),
    "Ecuador": ("South America", [("country", "owns the Galapagos Islands")], R),
    "Paraguay": ("South America", [("country", "is home to the Jesuit mission ruins of Trinidad")], R),
    "Botswana": ("Africa", [("country", "is home to the Okavango Delta")], R),
    "Namibia": ("Africa", [("country", "is home to the red Sossusvlei dunes")], R),
    "Madagascar": ("Africa", [("country", "is the island home of the lemurs")], R),
    "Tanzania": ("Africa", [("country", "is home to Mount Kilimanjaro")], R),
    "Iceland": ("Europe", [("country", "is home to the Blue Lagoon geothermal spa")], R),
    "Finland": ("Europe", [("country", "is where the phone maker Nokia was founded")], R),
    "Hungary": ("Europe", [("country", "is where the Rubik's Cube was invented")], R),
    "Croatia": ("Europe", [("country", "is home to the walled city of Dubrovnik")], R),
}  # fmt: skip

# ---- 2. languages: country -> main official language (new) -----------------------------------------------------------
LANGUAGES = {
    "Brazil": ("Portuguese", [("country", "hosted the 2016 Summer Olympics"), ("country", "is home to the statue of Christ the Redeemer")], P),
    "Portugal": ("Portuguese", [("country", "was the homeland of the explorer Vasco da Gama")], P),
    "Mexico": ("Spanish", [("country", "is home to the ancient city of Teotihuacan"), ("country", "hosted the 1968 Summer Olympics")], P),
    "Argentina": ("Spanish", [("country", "is the birthplace of the tango"), ("country", "won the 1986 FIFA World Cup")], P),
    "Colombia": ("Spanish", [("country", "was the homeland of the novelist Gabriel Garcia Marquez")], P),
    "Peru": ("Spanish", [("country", "is home to Machu Picchu")], P),
    "Chile": ("Spanish", [("country", "is home to the Atacama Desert")], P),
    "Cuba": ("Spanish", [("country", "was led for decades by Fidel Castro")], P),
    "Venezuela": ("Spanish", [("country", "is home to Angel Falls")], P),
    "Spain": ("Spanish", [("country", "is home to the Alhambra")], P),
    "Austria": ("German", [("country", "was the homeland of the composer Mozart"), ("country", "has Vienna as its capital")], P),
    "Egypt": ("Arabic", [("country", "is home to the pyramids of Giza")], P),
    "Qatar": ("Arabic", [("country", "hosted the 2022 FIFA World Cup")], P),
    "France": ("French", [("country", "is home to the Eiffel Tower")], P),
    "Italy": ("Italian", [("country", "is home to the Colosseum")], P),
    "Greece": ("Greek", [("country", "hosted the first modern Olympic Games in 1896")], P),
    "Turkey": ("Turkish", [("country", "is home to the Hagia Sophia")], P),
    "Poland": ("Polish", [("country", "was the homeland of Pope John Paul II")], P),
    "Sweden": ("Swedish", [("country", "is where IKEA was founded")], P),
    "China": ("Mandarin", [("country", "built the Great Wall")], P),
    "Iran": ("Persian", [("country", "had its Shah overthrown in the 1979 revolution")], P),
    "Israel": ("Hebrew", [("country", "has a parliament called the Knesset")], P),
    "Jamaica": ("English", [("country", "is the homeland of the reggae singer Bob Marley")], P),
    "Nigeria": ("English", [("country", "has a film industry known as Nollywood")], P),
    "Angola": ("Portuguese", [("country", "has Luanda as its capital")], R),
    "Mozambique": ("Portuguese", [("country", "has Maputo as its capital")], R),
    "Uruguay": ("Spanish", [("country", "won the first FIFA World Cup in 1930")], R),
    "Ecuador": ("Spanish", [("country", "owns the Galapagos Islands")], R),
    "Costa Rica": ("Spanish", [("country", "abolished its army in 1948")], R),
    "Liechtenstein": ("German", [("country", "is a tiny Alpine principality between Austria and Switzerland")], R),
    "Jordan": ("Arabic", [("country", "is home to the ancient city of Petra")], R),
    "Lebanon": ("Arabic", [("country", "has a cedar tree on its flag")], R),
    "Tunisia": ("Arabic", [("country", "is home to the ruins of Carthage")], R),
    "Senegal": ("French", [("country", "has Dakar as its capital")], R),
    "Ivory Coast": ("French", [("country", "is the world's largest producer of cocoa beans")], R),
    "Monaco": ("French", [("country", "is famous for its Monte Carlo casino and Grand Prix")], R),
    "Hungary": ("Hungarian", [("country", "is where the Rubik's Cube was invented")], R),
    "Ghana": ("English", [("country", "is famous for kente cloth and the Ashanti kingdom")], R),
    "Suriname": ("Dutch", [("country", "is the smallest independent country in South America")], R),
}  # fmt: skip

# ---- 3. people -> nationality (natural_v1 PEOPLE = popular, natplus RARE_PEOPLE = rare; + 14 new) --------------------
PEOPLE = {
    "Picasso": ("Spanish", [("artist", "painted Guernica")], P),
    "Cervantes": ("Spanish", [("writer", "wrote Don Quixote")], P),
    "Mozart": ("Austrian", [("composer", "wrote The Magic Flute")], P),
    "Freud": ("Austrian", [("doctor", "founded psychoanalysis")], P),
    "Beethoven": ("German", [("composer", "wrote the Moonlight Sonata")], P),
    "Goethe": ("German", [("writer", "wrote Faust")], P),
    "Bach": ("German", [("composer", "wrote the Brandenburg Concertos")], P),
    "Kant": ("German", [("philosopher", "wrote the Critique of Pure Reason")], P),
    "Tolstoy": ("Russian", [("writer", "wrote War and Peace")], P),
    "Dostoevsky": ("Russian", [("writer", "wrote Crime and Punishment")], P),
    "Tchaikovsky": ("Russian", [("composer", "wrote Swan Lake")], P),
    "Chekhov": ("Russian", [("playwright", "wrote The Cherry Orchard")], P),
    "Galileo": ("Italian", [("astronomer", "discovered the four largest moons of Jupiter")], P),
    "Dante": ("Italian", [("poet", "wrote the Divine Comedy")], P),
    "Vivaldi": ("Italian", [("composer", "wrote The Four Seasons")], P),
    "Michelangelo": ("Italian", [("artist", "painted the ceiling of the Sistine Chapel")], P),
    "Verdi": ("Italian", [("composer", "wrote the opera Aida")], P),
    "Hugo": ("French", [("writer", "wrote Les Miserables")], P),
    "Monet": ("French", [("painter", "painted the Water Lilies series")], P),
    "Descartes": ("French", [("philosopher", "wrote 'I think, therefore I am'")], P),
    "Napoleon": ("French", [("emperor", "lost the Battle of Waterloo")], P),
    "Rembrandt": ("Dutch", [("painter", "painted The Night Watch")], P),
    "Vermeer": ("Dutch", [("painter", "painted Girl with a Pearl Earring")], P),
    "Chopin": ("Polish", [("composer", "wrote the Minute Waltz")], P),
    "Copernicus": ("Polish", [("astronomer", "proposed that the Earth moves around the Sun")], P),
    "Nobel": ("Swedish", [("chemist", "invented dynamite")], P),
    "Linnaeus": ("Swedish", [("botanist", "created the modern system for naming species")], P),
    "Ibsen": ("Norwegian", [("playwright", "wrote A Doll's House")], P),
    "Grieg": ("Norwegian", [("composer", "wrote In the Hall of the Mountain King")], P),
    "Edison": ("American", [("inventor", "invented the phonograph")], P),
    "Lincoln": ("American", [("president", "issued the Emancipation Proclamation")], P),
    "Twain": ("American", [("writer", "wrote The Adventures of Tom Sawyer")], P),
    "Plato": ("Greek", [("philosopher", "wrote The Republic")], P),
    "Aristotle": ("Greek", [("philosopher", "tutored Alexander the Great")], P),
    "Joyce": ("Irish", [("writer", "wrote the novel Ulysses")], P),
    "Gandhi": ("Indian", [("leader", "led the Salt March against British rule")], P),
    "Confucius": ("Chinese", [("philosopher", "taught the sayings collected in the Analects")], P),
    "Sibelius": ("Finnish", [("composer", "wrote the Valse triste")], R),
    "Dvorak": ("Czech", [("composer", "wrote the New World Symphony")], R),
    "Smetana": ("Czech", [("composer", "wrote The Moldau")], R),
    "Bartok": ("Hungarian", [("composer", "wrote the Concerto for Orchestra")], R),
    "Liszt": ("Hungarian", [("composer", "wrote the Liebestraum piano pieces")], R),
    "Kierkegaard": ("Danish", [("philosopher", "wrote Fear and Trembling")], R),
    "Andersen": ("Danish", [("writer", "wrote The Little Mermaid")], R),
    "Strindberg": ("Swedish", [("playwright", "wrote Miss Julie")], R),
    "Lorca": ("Spanish", [("poet", "wrote Blood Wedding")], R),
    "Puccini": ("Italian", [("composer", "wrote the opera Tosca")], R),
    "Pirandello": ("Italian", [("playwright", "wrote Six Characters in Search of an Author")], R),
    "Schiller": ("German", [("poet", "wrote the poem Ode to Joy")], R),
    "Klimt": ("Austrian", [("painter", "painted The Kiss")], R),
    "Pushkin": ("Russian", [("poet", "wrote Eugene Onegin")], R),
    "Mendeleev": ("Russian", [("chemist", "created the periodic table of the elements")], R),
    "Zola": ("French", [("writer", "wrote the open letter J'Accuse")], R),
    "Ravel": ("French", [("composer", "wrote Bolero")], R),
    "Escher": ("Dutch", [("artist", "drew impossible staircases and endless tessellations")], R),
    "Yeats": ("Irish", [("poet", "wrote the poem The Second Coming")], R),
    "Hokusai": ("Japanese", [("artist", "made the woodblock print The Great Wave")], R),
    "Magritte": ("Belgian", [("painter", "painted a pipe above the words This is not a pipe")], R),
    "Neruda": ("Chilean", [("poet", "wrote Twenty Love Poems and a Song of Despair")], R),
    "Borges": ("Argentine", [("writer", "wrote the story collection Ficciones")], R),
}  # fmt: skip
FULL_NAMES = {  # {surname: full name}; FIRST_NAMES (natural_v1 style) is derived below
    "Picasso": "Pablo Picasso", "Cervantes": "Miguel de Cervantes", "Mozart": "Wolfgang Amadeus Mozart",
    "Freud": "Sigmund Freud", "Beethoven": "Ludwig van Beethoven", "Goethe": "Johann Wolfgang von Goethe",
    "Bach": "Johann Sebastian Bach", "Kant": "Immanuel Kant", "Tolstoy": "Leo Tolstoy", "Dostoevsky": "Fyodor Dostoevsky",
    "Tchaikovsky": "Pyotr Ilyich Tchaikovsky", "Chekhov": "Anton Chekhov", "Galileo": "Galileo Galilei",
    "Dante": "Dante Alighieri", "Vivaldi": "Antonio Vivaldi", "Michelangelo": "Michelangelo Buonarroti",
    "Verdi": "Giuseppe Verdi", "Hugo": "Victor Hugo", "Monet": "Claude Monet", "Descartes": "Rene Descartes",
    "Napoleon": "Napoleon Bonaparte", "Rembrandt": "Rembrandt van Rijn", "Vermeer": "Johannes Vermeer",
    "Chopin": "Frederic Chopin", "Copernicus": "Nicolaus Copernicus", "Nobel": "Alfred Nobel", "Linnaeus": "Carl Linnaeus",
    "Ibsen": "Henrik Ibsen", "Grieg": "Edvard Grieg", "Edison": "Thomas Edison", "Lincoln": "Abraham Lincoln",
    "Twain": "Mark Twain", "Plato": "Plato", "Aristotle": "Aristotle", "Joyce": "James Joyce",
    "Gandhi": "Mahatma Gandhi", "Confucius": "Confucius", "Sibelius": "Jean Sibelius", "Dvorak": "Antonin Dvorak",
    "Smetana": "Bedrich Smetana", "Bartok": "Bela Bartok", "Liszt": "Franz Liszt", "Kierkegaard": "Soren Kierkegaard",
    "Andersen": "Hans Christian Andersen", "Strindberg": "August Strindberg", "Lorca": "Federico Garcia Lorca",
    "Puccini": "Giacomo Puccini", "Pirandello": "Luigi Pirandello", "Schiller": "Friedrich Schiller",
    "Klimt": "Gustav Klimt", "Pushkin": "Alexander Pushkin", "Mendeleev": "Dmitri Mendeleev", "Zola": "Emile Zola",
    "Ravel": "Maurice Ravel", "Escher": "Maurits Cornelis Escher", "Yeats": "William Butler Yeats",
    "Hokusai": "Katsushika Hokusai", "Magritte": "Rene Magritte", "Neruda": "Pablo Neruda",
    "Borges": "Jorge Luis Borges",
}  # fmt: skip
FIRST_NAMES = {**{s: f.split()[0] for s, f in FULL_NAMES.items()}, "Hokusai": "Katsushika"}  # natural_v1.FIRST_NAMES style

# ---- 4. cities -> country (natural_v1 CITIES = popular, natplus RARE_CITIES = rare; + 16 new) -----------------------
CITIES = {
    "Barcelona": ("Spain", [("city", "is home to the Sagrada Familia")], P),
    "Seville": ("Spain", [("city", "is famous for the Giralda tower")], P),
    "Milan": ("Italy", [("city", "is home to the La Scala opera house")], P),
    "Venice": ("Italy", [("city", "is famous for its canals and gondolas")], P),
    "Florence": ("Italy", [("city", "is home to the Uffizi Gallery")], P),
    "Naples": ("Italy", [("city", "lies at the foot of Mount Vesuvius")], P),
    "Munich": ("Germany", [("city", "hosts the Oktoberfest")], P),
    "Hamburg": ("Germany", [("city", "is home to the Elbphilharmonie concert hall")], P),
    "Lyon": ("France", [("city", "is where the Lumiere brothers made the first films")], P),
    "Osaka": ("Japan", [("city", "hosted the 1970 World Expo")], P),
    "Kyoto": ("Japan", [("city", "is famous for the Golden Pavilion temple")], P),
    "Shanghai": ("China", [("city", "has a waterfront promenade called the Bund")], P),
    "Mumbai": ("India", [("city", "is the center of the Bollywood film industry")], P),
    "Sydney": ("Australia", [("city", "is famous for its opera house with sail-shaped roofs")], P),
    "Toronto": ("Canada", [("city", "is home to the CN Tower")], P),
    "Vancouver": ("Canada", [("city", "hosted the 2010 Winter Olympics")], P),
    "Istanbul": ("Turkey", [("city", "is home to the Hagia Sophia")], P),
    "Casablanca": ("Morocco", [("city", "is home to the Hassan II Mosque")], P),
    "Krakow": ("Poland", [("city", "is home to Wawel Castle")], P),
    "Porto": ("Portugal", [("city", "lies on the Douro river and is famous for its wine cellars")], P),
    "Geneva": ("Switzerland", [("city", "hosts the European headquarters of the United Nations")], P),
    "Rio": ("Brazil", [("city", "is overlooked by the Christ the Redeemer statue")], P),
    "Moscow": ("Russia", [("city", "is home to the Kremlin and Red Square")], P),
    "Athens": ("Greece", [("city", "hosted the 2004 Summer Olympics"), ("city", "is home to the Parthenon")], P),
    "Cairo": ("Egypt", [("city", "lies on the Nile next to the pyramids of Giza")], P),
    "Beijing": ("China", [("city", "is home to the Forbidden City")], P),
    "Copenhagen": ("Denmark", [("city", "is home to the Little Mermaid statue and the Tivoli Gardens")], P),
    "Dublin": ("Ireland", [("city", "is where Guinness stout was first brewed")], P),
    "Bangkok": ("Thailand", [("city", "is home to the Temple of the Emerald Buddha and the Grand Palace")], P),
    "Buenos Aires": ("Argentina", [("city", "is home to the Casa Rosada presidential palace")], P),
    "Cape Town": ("South Africa", [("city", "lies at the foot of Table Mountain")], P),
    "Lisbon": ("Portugal", [("city", "was largely destroyed by an earthquake in 1755")], P),
    "Vienna": ("Austria", [("city", "is home to the Schonbrunn Palace")], P),
    "Oslo": ("Norway", [("city", "hosts the Nobel Peace Prize ceremony")], P),
    "Gothenburg": ("Sweden", [("city", "is the home city of Volvo cars")], R),
    "Bilbao": ("Spain", [("city", "is home to a Guggenheim museum designed by Frank Gehry")], R),
    "Dresden": ("Germany", [("city", "rebuilt its Frauenkirche church after wartime bombing")], R),
    "Turin": ("Italy", [("city", "keeps a famous burial shroud in its cathedral")], R),
    "Nagoya": ("Japan", [("city", "is famous for a castle with golden dolphins on its roof")], R),
    "Chengdu": ("China", [("city", "is famous for its giant panda breeding base")], R),
    "Jaipur": ("India", [("city", "is known as the Pink City")], R),
    "Adelaide": ("Australia", [("city", "was named after the queen consort of William IV")], R),
    "Calgary": ("Canada", [("city", "holds the Stampede rodeo every July")], R),
    "Salzburg": ("Austria", [("city", "is where The Sound of Music was filmed")], R),
    "Bruges": ("Belgium", [("city", "is famous for its medieval canals and lace")], R),
    "Cusco": ("Peru", [("city", "was the capital of the Inca Empire")], R),
    "Medellin": ("Colombia", [("city", "is known as the City of Eternal Spring")], R),
    "Agra": ("India", [("city", "is home to the Taj Mahal")], R),
    "Marseille": ("France", [("city", "is the home port of the fish stew bouillabaisse")], R),
    "Guadalajara": ("Mexico", [("city", "is famous as the home of mariachi music")], R),
    "Marrakesh": ("Morocco", [("city", "is famous for the Jemaa el-Fnaa market square")], R),
}  # fmt: skip

# ---- 5. companies -> country of origin (new; countries that need "the" are left out: no US, UK or Dutch firms) ----
COMPANIES = {
    "Toyota": ("Japan", [("company", "makes the Corolla and the Prius cars")], P),
    "Sony": ("Japan", [("company", "created the Walkman and the PlayStation")], P),
    "Nintendo": ("Japan", [("company", "created Super Mario and the Game Boy")], P),
    "Volkswagen": ("Germany", [("company", "makes the Beetle and the Golf cars")], P),
    "Adidas": ("Germany", [("company", "makes sportswear with three stripes")], P),
    "BMW": ("Germany", [("company", "owns the Mini and Rolls-Royce car brands")], P),
    "Porsche": ("Germany", [("company", "makes the Cayenne and Boxster sports cars")], P),
    "IKEA": ("Sweden", [("company", "sells flat-pack furniture with picture-only assembly instructions")], P),
    "Volvo": ("Sweden", [("company", "makes cars famous for safety and invented the three-point seat belt")], P),
    "Spotify": ("Sweden", [("company", "runs the music streaming service with a green logo")], P),
    "Ferrari": ("Italy", [("company", "makes red racing cars with a prancing horse badge")], P),
    "Lamborghini": ("Italy", [("company", "makes sports cars with a raging bull badge")], P),
    "Gucci": ("Italy", [("company", "is the luxury fashion house famous for its horsebit loafers")], P),
    "Fiat": ("Italy", [("company", "makes the small Panda and Punto cars")], P),
    "Michelin": ("France", [("company", "publishes the restaurant guide that awards stars")], P),
    "Peugeot": ("France", [("company", "makes cars with a lion badge")], P),
    "Renault": ("France", [("company", "makes the Clio and Megane cars")], P),
    "Lacoste": ("France", [("company", "makes polo shirts with a crocodile logo")], P),
    "L'Oreal": ("France", [("company", "is the cosmetics giant with the slogan Because you're worth it")], P),
    "Samsung": ("South Korea", [("company", "makes the Galaxy smartphones")], P),
    "Hyundai": ("South Korea", [("company", "makes the Elantra and Tucson cars")], P),
    "Nestle": ("Switzerland", [("company", "is the food giant that makes KitKat bars and Maggi noodles")], P),
    "LEGO": ("Denmark", [("company", "makes interlocking plastic toy bricks")], P),
    "Nokia": ("Finland", [("company", "was once the world's biggest maker of mobile phones")], P),
    "Zara": ("Spain", [("company", "is the fast-fashion chain founded by Amancio Ortega")], P),
    "Huawei": ("China", [("company", "is the telecom giant founded by Ren Zhengfei")], P),
    "Alibaba": ("China", [("company", "runs the Taobao shopping site and was founded by Jack Ma")], P),
    "BlackBerry": ("Canada", [("company", "made phones with physical keyboards popular with business users")], P),
    "Uniqlo": ("Japan", [("company", "is the casual clothing chain known for HeatTech underwear and fleece jackets")], R),
    "Yamaha": ("Japan", [("company", "makes both pianos and motorcycles")], R),
    "Haribo": ("Germany", [("company", "makes the gold bear gummy candies")], R),
    "Barilla": ("Italy", [("company", "is the world's largest pasta maker")], R),
    "Ferrero": ("Italy", [("company", "makes Nutella spread and Rocher chocolates")], R),
    "Lindt": ("Switzerland", [("company", "makes gold-wrapped chocolate bunnies and Excellence bars")], R),
    "Carlsberg": ("Denmark", [("company", "brews the lager advertised as probably the best beer in the world")], R),
    "Rovio": ("Finland", [("company", "created the game Angry Birds")], R),
    "Chupa Chups": ("Spain", [("company", "makes lollipops with a logo designed by Salvador Dali")], R),
    "Lenovo": ("China", [("company", "bought the personal computer business of IBM and makes ThinkPad laptops")], R),
    "Lululemon": ("Canada", [("company", "is the athletic apparel brand best known for its yoga pants")], R),
    "Tata": ("India", [("company", "owns the Jaguar Land Rover car company")], R),
    "Swarovski": ("Austria", [("company", "makes cut crystal jewelry and figurines")], R),
}  # fmt: skip

# ---- 6. landmarks -> country (new; entity strings carry their article) -----------------------------------------------
LANDMARKS = {
    "the Eiffel Tower": ("France", [("landmark", "is the wrought-iron lattice structure built for the World's Fair of 1889")], P),
    "the Louvre": ("France", [("museum", "holds the Mona Lisa")], P),
    "the Colosseum": ("Italy", [("landmark", "is the ancient amphitheater where gladiators fought")], P),
    "the Trevi Fountain": ("Italy", [("landmark", "is the Baroque monument into whose basin visitors toss coins over their shoulders")], P),
    "Pompeii": ("Italy", [("ancient town", "was buried in volcanic ash by the eruption of Mount Vesuvius")], P),
    "the Taj Mahal": ("India", [("landmark", "is the white marble mausoleum built by Shah Jahan for his favorite wife")], P),
    "the Great Wall": ("China", [("landmark", "is the ancient fortification that stretches for thousands of miles to keep out northern nomads")], P),
    "the Forbidden City": ("China", [("palace complex", "was the home of the Ming and Qing emperors")], P),
    "the Terracotta Army": ("China", [("landmark", "is the buried collection of thousands of life-size clay soldiers made for the first emperor")], P),
    "Machu Picchu": ("Peru", [("landmark", "is the Inca citadel high in the Andes")], P),
    "the Acropolis": ("Greece", [("landmark", "is the ancient hilltop citadel crowned by the Parthenon")], P),
    "the Kremlin": ("Russia", [("landmark", "is the red-walled fortress that serves as the official residence of the president")], P),
    "Saint Basil's Cathedral": ("Russia", [("church", "has colorful onion domes and stands on Red Square")], P),
    "Angkor Wat": ("Cambodia", [("landmark", "is the world's largest religious monument, a twelfth-century temple complex")], P),
    "Mount Fuji": ("Japan", [("volcano", "is the sacred snow-capped peak that is the highest in its island nation")], P),
    "Christ the Redeemer": ("Brazil", [("statue", "stands with outstretched arms on top of Corcovado mountain")], P),
    "the Alhambra": ("Spain", [("landmark", "is the hilltop Moorish palace and fortress with the Court of the Lions")], P),
    "the Sagrada Familia": ("Spain", [("basilica", "was designed by Antoni Gaudi and has been under construction since 1882")], P),
    "Petra": ("Jordan", [("ancient city", "was carved into rose-red cliffs by the Nabataeans")], P),
    "Chichen Itza": ("Mexico", [("ancient city", "was built by the Maya around the stepped pyramid of El Castillo")], P),
    "Neuschwanstein": ("Germany", [("castle", "was built by King Ludwig II and inspired the Sleeping Beauty castle at Disneyland")], P),
    "the Great Sphinx": ("Egypt", [("statue", "has the body of a lion and the head of a king and guards the pyramids")], P),
    "Uluru": ("Australia", [("landmark", "is the giant red sandstone monolith sacred to the Anangu people")], P),
    "the Great Barrier Reef": ("Australia", [("landmark", "is the world's largest system of coral")], P),
    "Hagia Sophia": ("Turkey", [("landmark", "was built as a Byzantine cathedral and later became a mosque")], P),
    "Table Mountain": ("South Africa", [("landmark", "is the flat-topped peak that overlooks Cape Town")], P),
    "Mount Kilimanjaro": ("Tanzania", [("volcano", "is the highest peak on its continent, with snows near the equator")], P),
    "the CN Tower": ("Canada", [("landmark", "was the world's tallest free-standing structure for over thirty years")], P),
    "Mont Saint-Michel": ("France", [("landmark", "is the tidal island crowned by a medieval abbey")], R),
    "the Golden Temple": ("India", [("landmark", "is the holiest shrine of Sikhism, a gilded gurdwara surrounded by a sacred pool")], R),
    "the Nazca Lines": ("Peru", [("landmark", "is a set of giant ancient figures etched into the desert and best seen from the air")], R),
    "the Golden Pavilion": ("Japan", [("landmark", "is the Zen temple whose top two floors are covered in gold leaf")], R),
    "Teotihuacan": ("Mexico", [("ancient city", "is home to the Pyramids of the Sun and the Moon")], R),
    "Abu Simbel": ("Egypt", [("landmark", "is the pair of rock temples of Ramesses II that were moved to escape the waters of Lake Nasser")], R),
    "Robben Island": ("South Africa", [("place", "is where Nelson Mandela was imprisoned for eighteen years")], R),
    "the Petronas Towers": ("Malaysia", [("landmark", "is the pair of steel-clad skyscrapers joined by a sky bridge in Kuala Lumpur")], R),
    "Borobudur": ("Indonesia", [("landmark", "is the world's largest Buddhist temple, a ninth-century stepped stupa")], R),
    "Persepolis": ("Iran", [("ancient city", "was the ceremonial capital of the Achaemenid Empire burned by Alexander the Great")], R),
    "Ha Long Bay": ("Vietnam", [("landmark", "is the stretch of emerald water with thousands of limestone islands in the Gulf of Tonkin")], R),
    "Easter Island": ("Chile", [("place", "is famous for its giant moai stone heads")], R),
    "the Galapagos Islands": ("Ecuador", [("place", "is the archipelago where Darwin studied finches and giant tortoises")], R),
    "Angel Falls": ("Venezuela", [("landmark", "is the world's highest uninterrupted waterfall")], R),
}  # fmt: skip

# ---- 7. dishes -> country of origin (new; contested origins left out: baklava, hummus, kimchi, borscht, ceviche ...) --
DISHES = {
    "pizza": ("Italy", [("dish", "is a flat round bread baked with tomato sauce and mozzarella and often sold by the slice")], P),
    "risotto": ("Italy", [("dish", "is made of short-grain rice slowly stirred in broth until creamy")], P),
    "tiramisu": ("Italy", [("dessert", "layers coffee-soaked ladyfingers with mascarpone cream")], P),
    "lasagna": ("Italy", [("dish", "layers flat sheets of pasta with meat sauce, bechamel and cheese")], P),
    "paella": ("Spain", [("dish", "cooks saffron rice with seafood or rabbit in a wide, shallow pan")], P),
    "gazpacho": ("Spain", [("dish", "is a cold soup of raw blended tomatoes, peppers and cucumber")], P),
    "sushi": ("Japan", [("dish", "consists of vinegared rice topped or rolled with raw fish and seaweed")], P),
    "miso soup": ("Japan", [("dish", "is a broth of fermented soybean paste with tofu and seaweed")], P),
    "tacos": ("Mexico", [("dish", "consists of folded corn tortillas filled with meat, onions and salsa")], P),
    "guacamole": ("Mexico", [("dish", "is a dip of mashed avocado with lime, onion and chili")], P),
    "enchiladas": ("Mexico", [("dish", "consists of rolled corn tortillas stuffed with meat and covered in chili sauce")], P),
    "butter chicken": ("India", [("dish", "combines tandoor-roasted poultry with a mild, creamy tomato sauce and was first served at a restaurant in Delhi")], P),
    "dim sum": ("China", [("dish", "consists of small steamed dumplings and buns served in bamboo baskets with tea")], P),
    "kung pao chicken": ("China", [("dish", "is a spicy stir-fry of diced poultry with peanuts and dried chili peppers")], P),
    "crepes": ("France", [("dish", "consists of very thin pancakes often filled with sugar, jam or chocolate")], P),
    "ratatouille": ("France", [("dish", "is a slow-cooked stew of eggplant, zucchini, tomatoes and peppers")], P),
    "coq au vin": ("France", [("dish", "consists of chicken braised in red wine with mushrooms and bacon")], P),
    "souvlaki": ("Greece", [("dish", "consists of small pieces of grilled meat on a skewer, served with pita and tzatziki")], P),
    "goulash": ("Hungary", [("dish", "is a paprika-spiced stew of beef and onions")], P),
    "pierogi": ("Poland", [("dish", "consists of half-moon dumplings filled with potato and cheese")], P),
    "fondue": ("Switzerland", [("dish", "is a shared pot of melted cheese into which bread is dipped on long forks")], P),
    "beef stroganoff": ("Russia", [("dish", "consists of sauteed strips of meat in a sour cream and mushroom sauce")], P),
    "pho": ("Vietnam", [("dish", "is a soup of rice noodles and thinly sliced beef in a clear, spiced broth")], P),
    "tom yum": ("Thailand", [("dish", "is a hot and sour soup flavored with lemongrass, galangal and lime leaves")], P),
    "poutine": ("Canada", [("dish", "consists of fries topped with cheese curds and brown gravy")], P),
    "sukiyaki": ("Japan", [("dish", "consists of thin slices of beef simmered at the table in sweet soy broth and dipped in raw egg")], R),
    "dosa": ("India", [("dish", "is a thin, crispy pancake made from fermented rice and lentil batter")], R),
    "mapo tofu": ("China", [("dish", "combines bean curd and minced pork in a numbing, spicy chili bean sauce")], R),
    "bouillabaisse": ("France", [("dish", "is a saffron-scented fish stew served with rouille sauce and bread")], R),
    "spanakopita": ("Greece", [("dish", "is a savory pie of spinach and feta cheese wrapped in filo pastry")], R),
    "sauerbraten": ("Germany", [("dish", "is a pot roast of beef marinated for days in vinegar and spices")], R),
    "Sachertorte": ("Austria", [("dessert", "is a dense chocolate cake with a thin layer of apricot jam under dark chocolate icing")], R),
    "banh mi": ("Vietnam", [("dish", "is a baguette sandwich filled with pickled vegetables, pate and cilantro")], R),
    "pastel de nata": ("Portugal", [("pastry", "is a small egg custard tart with a flaky crust and a scorched, blistered top")], R),
    "jerk chicken": ("Jamaica", [("dish", "is meat rubbed with a fiery allspice and hot pepper seasoning and slow-smoked over pimento wood")], R),
    "smorrebrod": ("Denmark", [("dish", "consists of open-faced sandwiches on buttered dark rye bread")], R),
}  # fmt: skip

# ---- 8. animals -> class (natplus ANIMALS = popular, answers lower-cased; + 15 new) ---------------------------------
ANIMALS = {
    "beaver": ("mammal", [("animal", "builds dams across rivers")], P),
    "bat": ("mammal", [("animal", "hunts at night by echolocation")], P),
    "dolphin": ("mammal", [("animal", "lives in the sea and talks in clicks and whistles")], P),
    "penguin": ("bird", [("animal", "cannot fly and lives in Antarctica")], P),
    "ostrich": ("bird", [("animal", "lays the largest eggs of any living animal")], P),
    "owl": ("bird", [("animal", "turns its head almost all the way around and hoots at night")], P),
    "crocodile": ("reptile", [("animal", "lies still in rivers waiting to snap at prey")], P),
    "chameleon": ("reptile", [("animal", "changes color to blend in")], P),
    "tortoise": ("reptile", [("animal", "carries its shell and can live over a hundred years")], P),
    "frog": ("amphibian", [("animal", "croaks and starts life as a tadpole")], P),
    "salamander": ("amphibian", [("animal", "can regrow its lost legs")], P),
    "axolotl": ("amphibian", [("animal", "keeps its feathery gills as an adult in Mexican lakes")], P),
    "shark": ("fish", [("animal", "has rows of replaceable teeth and can smell blood from far away")], P),
    "salmon": ("fish", [("animal", "swims upstream to spawn")], P),
    "seahorse": ("fish", [("animal", "has males that carry the babies")], P),
    "bee": ("insect", [("animal", "makes honey")], P),
    "ant": ("insect", [("animal", "lives in colonies and carries crumbs back to its nest")], P),
    "butterfly": ("insect", [("animal", "starts life as a caterpillar")], P),
    "flamingo": ("bird", [("animal", "stands on one leg and gets its pink color from its diet")], P),
    "cobra": ("reptile", [("animal", "spreads a hood when threatened and sways to a charmer's flute")], P),
    "toad": ("amphibian", [("animal", "has dry, warty skin and is said in folklore to give people warts")], P),
    "piranha": ("fish", [("animal", "has razor-sharp teeth and hunts in groups in Amazon rivers")], P),
    "mosquito": ("insect", [("animal", "spreads malaria with its bite")], P),
    "platypus": ("mammal", [("animal", "lays eggs and has a bill like a duck")], R),
    "narwhal": ("mammal", [("animal", "has a long spiral tusk and lives in Arctic waters")], R),
    "armadillo": ("mammal", [("animal", "has a shell of bony bands and digs burrows in the Americas")], R),
    "kiwi": ("bird", [("animal", "is a flightless national symbol of New Zealand with nostrils at the tip of its bill")], R),
    "puffin": ("bird", [("animal", "has a colorful striped bill and nests in burrows on northern sea cliffs")], R),
    "gecko": ("reptile", [("animal", "can climb glass walls with its sticky toe pads")], R),
    "iguana": ("reptile", [("animal", "is a large green plant-eater with a row of spines down its back, often kept as a pet")], R),
    "stingray": ("fish", [("animal", "has a flat, diamond-shaped body and a venomous barb on its tail")], R),
    "termite": ("insect", [("animal", "builds tall mounds and eats wood")], R),
    "cicada": ("insect", [("animal", "spends years underground and then sings loudly from trees in summer")], R),
}  # fmt: skip

_Q1M = ["Which {noun} {rel}?"] * 3
_NEUTRAL_PLACE = ["{x} was mentioned in this week's travel column.", "A reader asked a question about {x} in the letters page.",
                  "The quiz night included a round on {x}."]  # fmt: skip

REL2 = {
    "countries": {
        "facts": COUNTRIES, "noun": "country", "unknown": "an unnamed country",
        "bind": ["{p} grew up in {x}.", "{p} was raised in {x}.", "{p} spent a whole childhood in {x}."],
        "pdesc": ["the country where {p} grew up", "the country where {p} was raised", "the country of {p}'s childhood"],
        "q1P": ["In which country did {p} grow up?", "Which country was {p} raised in?", "Where did {p} spend their childhood?"],
        "q1M": _Q1M,
        "q2M": ["On which continent is {d}?", "Which continent is {d} in?", "{D} is on which continent?"],
        "kfact": ["{x} is in {a}.", "{x} lies in {a}.", "{x} is a country in {a}."],
        "pfact": ["The delegation from {x} will hold its next meeting in {a}.",
                  "The delegation from {x} announced that its next meeting will take place in {a}.",
                  "Next year, the delegation from {x} meets in {a}."],
        "q2P": ["On which continent will the delegation from {d} hold its next meeting?",
                "Which continent will host the next meeting of the delegation from {d}?",
                "Where, by continent, will the delegation from {d} meet next?"],
        "nfact": _NEUTRAL_PLACE,
        "track": (["sculpture exhibition", "textile exhibition", "photography exhibition", "ceramics exhibition"],
                  "{pre}the {o} went to {e}.", "the country the {o} went to last", "Which country did the {o} go to last?"),
    },
    "languages": {
        "facts": LANGUAGES, "noun": "country", "unknown": "an unnamed country",
        "bind": ["{p} spent last summer in {x}.", "Last summer, {p} went on holiday to {x}.", "{p} visited {x} last summer."],
        "pdesc": ["the country where {p} spent last summer", "the country {p} went on holiday to last summer",
                  "the country {p} visited last summer"],
        "q1P": ["In which country did {p} spend last summer?", "Which country did {p} go on holiday to last summer?",
                "Which country did {p} visit last summer?"],
        "q1M": _Q1M,
        "q2M": ["What is the main official language of {d}?", "Which language is the main official language of {d}?",
                "{D} has which language as its main official language?"],
        "kfact": ["The main official language of {x} is {a}.", "{x} has {a} as its main official language.",
                  "In {x}, the main official language is {a}."],
        "pfact": ["The new subtitles for the film from {x} are in {a}.",
                  "The festival film from {x} will be shown with subtitles in {a}.",
                  "This year, the festival film from {x} was subtitled in {a}."],
        "q2P": ["In which language are the new subtitles for the film from {d}?",
                "In which language will the festival film from {d} be subtitled?",
                "This year, the festival film from {d} was subtitled in which language?"],
        "nfact": _NEUTRAL_PLACE,
        "track": (["trade mission", "chess team", "film crew", "school choir"],
                  "{pre}the {o} traveled to {e}.", "the country the {o} traveled to last", "Which country did the {o} travel to last?"),
    },
    "people": {
        "facts": PEOPLE, "noun": "person", "unknown": "an unnamed historical figure",
        "bind": ["{p} wrote a doctoral thesis on {x}.", "{p}'s dissertation was about {x}.", "{p} spent five years writing a thesis on {x}."],
        "pdesc": ["the person {p} wrote a doctoral thesis on", "the subject of {p}'s dissertation", "the person {p}'s thesis was about"],
        "q1P": ["Who did {p} write a doctoral thesis on?", "Who was {p}'s dissertation about?", "Who was the subject of {p}'s thesis?"],
        "q1M": _Q1M,
        "q2M": ["What was the nationality of {d}?", "Which nationality was {d}?", "{D} was of which nationality?"],
        "kfact": ["{x} was {a}.", "By nationality, {x} was {a}.", "{x} was {a} by birth."],
        "pfact": ["In the new film series, {x} is played by {an} {a} actor.", "The upcoming biopic casts {an} {a} actor as {x}.",
                  "{X} will be portrayed by {an} {a} actor in a new film."],
        "q2P": ["What is the nationality of the actor who plays {d} in the new film?",
                "Which nationality is the actor cast as {d} in the new film?",
                "The actor portraying {d} in the new film is of which nationality?"],
        "nfact": ["{x} came up in this week's history quiz.", "The library put up a small display about {x}.",
                  "A reader asked a question about {x} in the letters page."],
        "track": (["history podcast", "culture podcast", "biography podcast", "radio series"],
                  "{pre}the {o} ran an episode on {e}.", "the person the {o} ran its latest episode on",
                  "Who did the {o} run its latest episode on?"),
    },
    "cities": {
        "facts": CITIES, "noun": "city", "unknown": "an unnamed city",
        "bind": ["{p} moved to {x} last spring.", "Last spring, {p} relocated to {x}.", "{p} has lived in {x} since last spring."],
        "pdesc": ["the city {p} moved to last spring", "the city {p} relocated to last spring", "the city {p} has lived in since last spring"],
        "q1P": ["Which city did {p} move to last spring?", "Which city did {p} relocate to last spring?",
                "Which city has {p} lived in since last spring?"],
        "q1M": _Q1M,
        "q2M": ["In which country is {d}?", "Which country is {d} in?", "{D} is in which country?"],
        "kfact": ["{x} is in {a}.", "{x} is a city in {a}.", "{x} lies in {a}."],
        "pfact": ["This year, {x} was paired with a partner city in {a}.", "This year, {x} signed a twinning agreement with a city in {a}.",
                  "This year's partner city for {x} is in {a}."],
        "q2P": ["In which country is this year's partner city of {d}?", "Which country is this year's twin city of {d} in?",
                "This year's partner city of {d} is in which country?"],
        "nfact": _NEUTRAL_PLACE,
        "track": (["jazz tour", "ballet tour", "circus tour", "choir tour"], "{pre}the {o} stopped in {e}.",
                  "the city the {o} stopped in last", "Which city did the {o} stop in last?"),
    },
    "companies": {
        "facts": COMPANIES, "noun": "company", "unknown": "an unnamed company",
        "bind": ["{p} wrote a business school case study on {x}.", "{p}'s business school thesis was about {x}.",
                 "{p} spent a semester studying the history of {x}."],
        "pdesc": ["the company {p} wrote a case study on", "the company {p}'s business school thesis was about",
                  "the company whose history {p} studied for a semester"],
        "q1P": ["Which company did {p} write a case study on?", "Which company was {p}'s business school thesis about?",
                "Which company's history did {p} study for a semester?"],
        "q1M": _Q1M,
        "q2M": ["Which country does {d} come from?", "What is the country of origin of {d}?", "{D} comes from which country?"],
        "kfact": ["{x} comes from {a}.", "{x} was founded in {a}.", "{x} is a company from {a}."],
        "pfact": ["{X} will open its next regional office in {a}.", "{X} has announced a new regional office in {a}.",
                  "Next year, {x} opens a new regional office in {a}."],
        "q2P": ["In which country will {d} open its next regional office?", "Which country will get the new regional office of {d}?",
                "{D} is opening its next regional office in which country?"],
        "nfact": ["{x} was mentioned in this week's business column.", "A reader asked a question about {x} in the letters page.",
                  "The marketing class discussed {x} on Tuesday."],
        "track": (["sales team", "audit team", "trade delegation", "news crew"], "{pre}the {o} visited {e}.",
                  "the company the {o} visited last", "Which company did the {o} visit last?"),
    },
    "landmarks": {
        "facts": LANDMARKS, "noun": "landmark", "unknown": "an unnamed landmark",
        "bind": ["{p} visited {x} last summer.", "Last summer, {p} went to see {x}.", "{p} took a guided trip to {x} last summer."],
        "pdesc": ["the landmark {p} visited last summer", "the landmark {p} went to see last summer",
                  "the landmark {p} took a guided trip to last summer"],
        "q1P": ["Which landmark did {p} visit last summer?", "Which landmark did {p} go to see last summer?",
                "Which landmark did {p} take a guided trip to last summer?"],
        "q1M": _Q1M,
        "q2M": ["In which country is {d}?", "Which country is {d} in?", "{D} is in which country?"],
        "kfact": ["You can find {x} in {a}.", "{a} is home to {x}.", "Visitors travel to {a} to see {x}."],
        "pfact": ["A new documentary about {x} was made by a film studio from {a}.",
                  "A film studio from {a} has just made a documentary about {x}.",
                  "The new documentary on {x} comes from a film studio in {a}."],
        "q2P": ["From which country is the film studio that made the new documentary about {d}?",
                "A film studio from which country made the new documentary about {d}?",
                "The new documentary on {d} comes from a film studio in which country?"],
        "nfact": ["A postcard of {x} arrived at the office this week.", "This week's travel column featured a photo of {x}.",
                  "The quiz night included a question about {x}."],
        "track": (["school trip", "film crew", "tour group", "photo team"], "{pre}the {o} visited {e}.",
                  "the landmark the {o} visited last", "Which landmark did the {o} visit last?"),
    },
    "dishes": {
        "facts": DISHES, "noun": "dish", "unknown": "an unnamed dish",
        "bind": ["{p}'s favorite dish is {x}.", "{p} says the best dish in the world is {x}.", "{p} voted for {x} in a poll of favorite dishes."],
        "pdesc": ["{p}'s favorite dish", "the dish {p} calls the best in the world", "the dish {p} voted for in the poll"],
        "q1P": ["What is {p}'s favorite dish?", "Which dish does {p} call the best in the world?", "Which dish did {p} vote for in the poll?"],
        "q1M": _Q1M,
        "q2M": ["Which country does {d} come from?", "What is the country of origin of {d}?", "{D} comes from which country?"],
        "kfact": ["The dish {x} comes from {a}.", "The dish called {x} originally comes from {a}.", "{a} is where the dish {x} comes from."],
        "pfact": ["At the food fair, the stall from {a} served {x}.", "At this year's food fair, {x} was on the menu of the stall from {a}.",
                  "The stall from {a} served {x} at the food fair."],
        "q2P": ["At the food fair, the stall from which country served {d}?", "At this year's food fair, which country's stall had {d} on its menu?",
                "The stall from which country served {d} at the food fair?"],
        "nfact": ["The dish {x} was mentioned in this week's food column.", "A reader asked a question about the dish {x} in the letters page.",
                  "The cooking club talked about the dish {x} on Tuesday."],
        "track": (["food critic", "cooking club", "travel blogger", "radio host"], "{pre}the {o} tried {e}.",
                  "the dish the {o} tried last", "Which dish did the {o} try last?"),
    },
    "animals": {
        "facts": ANIMALS, "noun": "animal", "unknown": "an unnamed animal",
        "bind": ["{p}'s favorite animal is the {x}.", "{p} sponsored the {x} at the city zoo.", "{p} wrote a school report on the {x}."],
        "pdesc": ["{p}'s favorite animal", "the animal {p} sponsored at the city zoo", "the animal {p} wrote a school report on"],
        "q1P": ["What is {p}'s favorite animal?", "Which animal did {p} sponsor at the city zoo?", "Which animal did {p} write a school report on?"],
        "q1M": _Q1M,
        "q2M": ["What class of animal is {d}?", "Which class of animal does {d} belong to?", "{D} belongs to which class of animal?"],
        "kfact": ["The {x} is a kind of {a}.", "Biologically, the {x} is a kind of {a}.", "Zoologists count the {x} as a kind of {a}."],
        "pfact": ["At the new zoo, the {x} is kept in the {al} house.", "The new zoo put the {x} in its {al} house.",
                  "Visitors to the new zoo find the {x} in the {al} house."],
        "q2P": ["In which house of the new zoo is {d} kept?", "Which house of the new zoo holds {d}?", "{D} is kept in which house of the new zoo?"],
        "nfact": ["The {x} was the subject of this week's nature quiz.", "A short film about the {x} was shown at the library.",
                  "The children drew pictures of the {x} in art class."],
        "track": (["camera crew", "film crew", "research team", "photo team"], "{pre}the {o} filmed the {e}.",
                  "the animal the {o} filmed last", "Which animal did the {o} film last?"),
    },
}  # fmt: skip

# ---- alternative names (hop-1 matching: natural_v1 competence --hop1 gen searches any of the item's names) ----------
ALT = {
    "countries": {"Turkey": ["Turkiye"], "Ivory Coast": ["Cote d'Ivoire"], "Laos": ["Lao"], "Iran": ["Islamic Republic of Iran"]},
    "languages": {"Ivory Coast": ["Cote d'Ivoire"], "Turkey": ["Turkiye"], "Costa Rica": [], "Iran": ["Islamic Republic of Iran"]},
    "people": {s: [f] for s, f in FULL_NAMES.items() if f != s},
    "cities": {"Rio": ["Rio de Janeiro"], "Krakow": ["Cracow", "Krakau"], "Mumbai": ["Bombay"], "Beijing": ["Peking"],
               "Seville": ["Sevilla"], "Turin": ["Torino"], "Munich": ["Muenchen"], "Florence": ["Firenze"], "Naples": ["Napoli"],
               "Venice": ["Venezia"], "Milan": ["Milano"], "Lisbon": ["Lisboa"], "Copenhagen": ["Kobenhavn"],
               "Marrakesh": ["Marrakech"], "Cusco": ["Cuzco"], "Gothenburg": ["Goteborg"], "Geneva": ["Geneve", "Genf"],
               "Vienna": ["Wien"], "Athens": ["Athina"], "Marseille": ["Marseilles"], "Bruges": ["Brugge"],
               "Medellin": ["Medellin"]},
    "companies": {"IKEA": ["Ikea"], "LEGO": ["Lego"], "L'Oreal": ["LOreal", "L Oreal"], "BMW": ["Bayerische Motoren Werke"],
                  "Volkswagen": ["VW"], "Nestle": ["Nestle SA"], "Tata": ["Tata Group", "Tata Motors"], "BlackBerry": ["Blackberry", "RIM"],
                  "Hyundai": ["Hyundai Motor"], "Samsung": ["Samsung Electronics"]},
    "landmarks": {"the Great Wall": ["Great Wall of China"], "the Great Sphinx": ["Sphinx", "Great Sphinx of Giza"],
                  "Uluru": ["Ayers Rock"],
                  "Easter Island": ["Rapa Nui"], "Christ the Redeemer": ["Cristo Redentor"], "Hagia Sophia": ["Ayasofya"],
                  "Saint Basil's Cathedral": ["St. Basil's Cathedral", "St Basil's Cathedral", "Saint Basil's", "St. Basil's"],
                  "the Kremlin": ["Moscow Kremlin"], "the Galapagos Islands": ["Galapagos"], "the Golden Pavilion": ["Kinkaku-ji", "Kinkakuji"],
                  "the Golden Temple": ["Harmandir Sahib"], "Mount Fuji": ["Fuji", "Fujisan"], "Mount Kilimanjaro": ["Kilimanjaro"],
                  "the Terracotta Army": ["Terracotta Warriors"], "the Petronas Towers": ["Petronas Twin Towers"],
                  "the Sagrada Familia": ["Sagrada Familia"], "Ha Long Bay": ["Halong Bay"], "Angkor Wat": ["Angkor"],
                  "the Nazca Lines": ["Nasca Lines"], "the CN Tower": ["CN Tower"], "Pompeii": ["Pompei"]},
    "dishes": {"crepes": ["crepe"], "tacos": ["taco"], "enchiladas": ["enchilada"], "pierogi": ["pierogies", "pierogis"],
               "lasagna": ["lasagne"], "beef stroganoff": ["stroganoff"], "kung pao chicken": ["kung pao", "gong bao chicken"],
               "miso soup": ["miso"], "butter chicken": ["murgh makhani"], "Sachertorte": ["Sacher torte", "Sacher-Torte"],
               "pastel de nata": ["pasteis de nata", "pastel de belem"], "smorrebrod": ["smorrebrod", "smorrebrot"],
               "dosa": ["dosai"], "tom yum": ["tom yam"], "pho": ["pho bo"]},
    "animals": {"seahorse": ["sea horse"], "kiwi": ["kiwi bird"]},
}  # fmt: skip
for _rel, _t in REL2.items():  # article-free forms of article-carrying names count too
    for _x in _t["facts"]:
        _alts = ALT.setdefault(_rel, {}).setdefault(_x, [])
        if _x.startswith("the "):
            _alts.insert(0, _x[4:])
        _alts[:] = list(dict.fromkeys(a for a in _alts if a != _x))
    ALT[_rel] = {x: v for x, v in ALT[_rel].items() if v}

def _core(x: str) -> str:
    return x[4:] if x.startswith("the ") else x


MULTIWORD = {rel: sorted(x for x in t["facts"] if " " in _core(x)) for rel, t in REL2.items()}  # names of 2+ words (article aside)
ARTICLE = {rel: sorted(x for x in t["facts"] if x.startswith("the ")) for rel, t in REL2.items() if any(x.startswith("the ") for x in t["facts"])}

# languages whose answer is morphologically derived from the country's name (France/French); split on this if needed
EPONYMOUS = {"languages": ["France", "Italy", "Spain", "Portugal", "Greece", "Turkey", "Poland", "Sweden", "Hungary"]}

# answer -> words that give it away (demonyms, languages, old names); used by the checker and as filler bans
DERIV = {
    # continents
    "Asia": ["Asian"], "Africa": ["African"], "Europe": ["European"],
    "North America": ["North American", "America", "American", "Americas"],
    "South America": ["South American", "America", "American", "Americas", "Latin America", "Latin American"],
    # languages
    "Portuguese": ["Portugal"], "Spanish": ["Spain", "Spaniard", "Castilian", "Hispanic"], "German": ["Germany", "Deutsch", "Germanic"],
    "Arabic": ["Arab", "Arabs", "Arabia", "Arabian"], "French": ["France", "Francophone"], "Italian": ["Italy"],
    "Greek": ["Greece", "Hellenic"], "Turkish": ["Turkey", "Turk", "Turks", "Turkiye"], "Polish": ["Poland"],
    "Swedish": ["Sweden", "Swede", "Swedes"], "Mandarin": ["Chinese", "China"], "Persian": ["Persia", "Farsi"],
    "Hebrew": ["Hebraic"], "English": ["England", "Britain", "British", "Anglo", "Anglophone"], "Hungarian": ["Hungary", "Magyar"],
    "Dutch": ["Netherlands", "Holland"],
    # nationalities
    "Austrian": ["Austria"], "Russian": ["Russia", "Soviet"], "Norwegian": ["Norway"], "Finnish": ["Finland", "Finn", "Finns"],
    "Czech": ["Czechia", "Bohemia", "Bohemian"], "Danish": ["Denmark", "Dane", "Danes"], "American": ["America", "United States"],
    "Irish": ["Ireland"], "Indian": ["India"], "Chinese": ["China"], "Japanese": ["Japan"], "Belgian": ["Belgium"],
    "Swiss": ["Switzerland", "Helvetic"], "Chilean": ["Chile"], "Argentine": ["Argentina", "Argentinian"],
    # countries
    "Spain": ["Spanish", "Spaniard", "Castilian"], "Italy": ["Italian", "Italia"], "Germany": ["German", "Deutsch"],
    "France": ["French"], "Japan": ["Japanese", "Nippon"], "China": ["Chinese", "Mandarin", "Cantonese"],
    "India": ["Indian", "Hindi"], "Australia": ["Australian", "Aussie"], "Canada": ["Canadian"],
    "Turkey": ["Turkish", "Turk", "Turkiye"], "Morocco": ["Moroccan"], "Poland": ["Polish"], "Portugal": ["Portuguese"],
    "Switzerland": ["Swiss", "Helvetic"], "Brazil": ["Brazilian"], "Sweden": ["Swedish", "Swede"], "Austria": ["Austrian"],
    "Belgium": ["Belgian"], "Peru": ["Peruvian"], "Colombia": ["Colombian"], "Russia": ["Russian", "Soviet"],
    "Greece": ["Greek", "Hellenic"], "Egypt": ["Egyptian"], "Denmark": ["Danish", "Dane"], "Ireland": ["Irish"],
    "Thailand": ["Thai", "Siam", "Siamese"], "Argentina": ["Argentine", "Argentinian"],
    "South Africa": ["South African", "Africa", "African"], "Norway": ["Norwegian"], "Mexico": ["Mexican"],
    "South Korea": ["Korea", "Korean"], "Finland": ["Finnish", "Finn"], "Cambodia": ["Cambodian", "Khmer"],
    "Jordan": ["Jordanian"], "Tanzania": ["Tanzanian"], "Malaysia": ["Malaysian", "Malay"], "Indonesia": ["Indonesian"],
    "Iran": ["Iranian", "Persian", "Persia"], "Vietnam": ["Vietnamese"], "Chile": ["Chilean"], "Ecuador": ["Ecuadorian"],
    "Venezuela": ["Venezuelan"], "Hungary": ["Hungarian", "Magyar"], "Jamaica": ["Jamaican"],
    # animal classes
    "mammal": ["mammals", "mammalian"], "bird": ["birds", "avian"], "reptile": ["reptiles", "reptilian"],
    "amphibian": ["amphibians"], "fish": ["fishes"], "insect": ["insects"],
}  # fmt: skip


def vocab(rel: str) -> list[str]:
    return sorted({v[0] for v in REL2[rel]["facts"].values()})
