"""paper_answer_types_build (prereg amendment 65, note 39): the frozen category vocabularies for the paper's 90 two-hop
prompts (data/probe_swap.json), written BEFORE any note-39 forward pass and with no model access (tokenizers only).

What it writes (data/paper_answer_types.json; its sha256 goes into a prereg addendum before any smoke result is seen):
  types   per answer type: a closed vocabulary of >= 8 values, written from the type label alone (not from any model
          output); its arm-6 "off" category chain (another category of the same domain first, then fallbacks used only to
          reach the count); off-only types (shape, unit, occupation, weekday) exist only as arm-6 categories.
  items   per item: answer type, intermediate type, set (primary / side_table / own_pair_only) and, per tokenizer:
          scrub  every form of each value's first token (as written, lower case, upper initial; with and without a
                 leading space), plus the item's own answer and swap answer (so arm 8's set is inside arm 3's), minus
                 every token of every form of the item's intermediate and swap_to names; tokens with no letter or digit
                 (a lone " " before a digit) and special tokens are dropped
          own    the same for the item's own answer pair only (arm 8; own-pair-only items' only scrub)
          off    arm 6: as many tokens as `scrub`, drawn (seeded by tokenizer and item) from the off chain's first
                 category minus scrub minus the excluded name tokens, the next category of the chain only when the
                 first runs out
          excluded  the name tokens removed
          own_answer_token_excluded  the concept token of the answer or swap answer is a name token, so no scrub can
                 remove the own answer (Australia -> Australia); such items go to the side table for that tokenizer
Sets: own_pair_only = the answer type has no closed vocabulary of >= 8 values in note 39's list (capitals, languages,
continents, colours, numbers, states of matter, first names, months, seasons, countries, US states, currencies, oceans);
side_table = the answer type equals the intermediate's type (note 39), or own_answer_token_excluded (per tokenizer; an
addition, flagged). Types outside the list (time of day, chemical symbols, planets, ...) are own-pair-only, by the list.

python scripts/paper_answer_types_build.py [--out data/paper_answer_types.json]   (CPU; tokenizers from the HF cache)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace import pins  # noqa: E402

TOKENIZERS = ("qwen3.6-27b", "qwen3.5-9b", "nemotron-3.5-lightning", "muse-glimmer-30b")
_WORDLIKE = re.compile(r"[^\W_]")  # a letter or a digit (model.py's formatting rule)

NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
                "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]  # fmt: skip
NUMBER_WORDS += [f"twenty-{w}" for w in NUMBER_WORDS[1:10]] + ["thirty"]

# Closed vocabularies, from the type label alone (2026-10-30, before any note-39 run). Small closed sets (seasons,
# states of matter, continents, oceans) are completed to >= 8 values with standard synonyms / named seas.
TYPES: dict[str, dict] = {
    "capital": {"domain": "nation", "off": ["language", "country"], "values": [
        "Washington", "Ottawa", "Brasilia", "Buenos Aires", "Lima", "Santiago", "Havana", "London", "Dublin", "Paris",
        "Madrid", "Lisbon", "Rome", "Berlin", "Vienna", "Brussels", "Amsterdam", "Copenhagen", "Oslo", "Stockholm",
        "Helsinki", "Warsaw", "Prague", "Budapest", "Athens", "Moscow", "Kyiv", "Ankara", "Cairo", "Nairobi", "Tehran",
        "Baghdad", "Riyadh", "New Delhi", "Beijing", "Tokyo", "Seoul", "Bangkok", "Canberra", "Wellington"]},
    "country": {"domain": "nation", "off": ["us_state", "capital"], "values": [
        "United States", "America", "Canada", "Mexico", "Brazil", "Argentina", "Peru", "Chile", "Cuba", "England",
        "Britain", "Ireland", "Scotland", "France", "Spain", "Portugal", "Italy", "Germany", "Austria", "Switzerland",
        "Belgium", "Netherlands", "Denmark", "Norway", "Sweden", "Poland", "Hungary", "Greece", "Russia", "Turkey",
        "Egypt", "Nigeria", "Iran", "Israel", "India", "Pakistan", "China", "Japan", "Korea", "Australia"]},
    "language": {"domain": "nation", "off": ["capital", "country"], "values": [
        "English", "French", "Spanish", "Portuguese", "Italian", "German", "Dutch", "Swedish", "Norwegian", "Danish",
        "Finnish", "Polish", "Czech", "Hungarian", "Greek", "Russian", "Ukrainian", "Turkish", "Arabic", "Hebrew",
        "Persian", "Hindi", "Urdu", "Bengali", "Chinese", "Mandarin", "Cantonese", "Japanese", "Korean", "Vietnamese",
        "Thai", "Indonesian", "Swahili", "Latin", "Irish"]},
    "continent": {"domain": "geography", "off": ["ocean", "country"], "values": [
        "Africa", "Antarctica", "Asia", "Australia", "Europe", "North America", "South America", "Oceania", "America",
        "Americas", "Eurasia", "Australasia"]},
    "ocean": {"domain": "geography", "off": ["continent", "country"], "values": [
        "Pacific", "Atlantic", "Indian", "Arctic", "Southern", "Antarctic", "Mediterranean", "Caribbean", "Baltic",
        "Arabian", "Caspian", "Bering", "Adriatic", "Aegean"]},
    "us_state": {"domain": "nation", "off": ["country", "capital"], "values": [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
        "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
        "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
        "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
        "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]},
    "currency": {"domain": "nation", "off": ["language", "capital"], "values": [
        "euro", "dollar", "pound", "sterling", "yen", "yuan", "renminbi", "rupee", "peso", "franc", "lira", "ruble",
        "rouble", "won", "real", "rand", "krona", "krone", "dinar", "dirham", "riyal", "shekel", "baht", "rupiah",
        "ringgit", "zloty", "forint", "mark", "drachma", "escudo", "US dollar", "Canadian dollar", "Australian dollar",
        "New Zealand dollar", "Hong Kong dollar", "Singapore dollar", "Swiss franc"]},
    "colour": {"domain": "physical property", "off": ["shape", "unit"], "values": [
        "red", "orange", "yellow", "green", "blue", "purple", "violet", "indigo", "pink", "brown", "black", "white",
        "gray", "grey", "beige", "tan", "maroon", "navy", "teal", "turquoise", "crimson", "scarlet", "magenta", "cyan",
        "golden", "silver", "gold"]},
    "state_of_matter": {"domain": "physical property", "off": ["colour", "shape"], "values": [
        "solid", "liquid", "gas", "plasma", "vapor", "vapour", "fluid", "gaseous", "molten", "condensate"]},
    "number": {"domain": "quantity", "off": ["unit", "shape"], "values": [str(i) for i in range(31)] + NUMBER_WORDS},
    "first_name": {"domain": "person", "off": ["occupation", "unit"], "values": [
        "Charles", "Albert", "Isaac", "William", "Wolfgang", "John", "James", "George", "Thomas", "Henry", "Edward",
        "Richard", "Robert", "Peter", "Paul", "David", "Michael", "Joseph", "Louis", "Ludwig", "Johann", "Friedrich",
        "Karl", "Leonardo", "Francis", "Nikola", "Marie", "Mary", "Elizabeth", "Jane", "Anne", "Catherine", "Margaret",
        "Emily", "Sarah", "Alice", "Grace", "Ada", "Rosalind", "Helen"]},
    "month": {"domain": "time", "off": ["weekday", "season", "unit"], "values": [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
        "December"]},
    "season": {"domain": "time", "off": ["month", "weekday", "unit"], "values": [
        "spring", "summer", "autumn", "fall", "winter", "springtime", "summertime", "wintertime"]},
    # off-only categories (arm 6), never an answer type
    "shape": {"domain": "physical property", "off_only": True, "values": [
        "circle", "square", "triangle", "rectangle", "oval", "sphere", "cube", "cone", "cylinder", "pyramid", "hexagon",
        "pentagon", "octagon", "ellipse", "spiral", "crescent", "prism", "polygon", "rhombus", "trapezoid",
        "parallelogram", "cuboid"]},
    "unit": {"domain": "quantity", "off_only": True, "values": [
        "meter", "metre", "kilometer", "centimeter", "millimeter", "gram", "kilogram", "milligram", "inch", "foot",
        "yard", "mile", "ounce", "liter", "litre", "gallon", "pint", "quart", "acre", "hectare", "tonne", "watt", "volt",
        "joule", "kelvin", "ampere"]},
    "occupation": {"domain": "person", "off_only": True, "values": [
        "scientist", "physicist", "chemist", "biologist", "naturalist", "mathematician", "astronomer", "inventor",
        "engineer", "philosopher", "composer", "musician", "pianist", "playwright", "poet", "novelist", "writer",
        "author", "painter", "artist", "sculptor", "architect", "explorer", "emperor", "president", "general", "actor",
        "singer", "doctor", "lawyer", "teacher", "soldier", "farmer", "priest"]},
    "weekday": {"domain": "time", "off_only": True, "values": [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "weekend", "weekday"]},
}  # fmt: skip

# Per item: (answer type, intermediate type), read from the item's question (prompt, answer field); no model output.
# An answer type not in TYPES (or None) has no closed vocabulary: own-pair-only.
ITEM_TYPES = {
    "amazon-language": ("language", "country"),
    "animal-cover-turtle": ("body covering", "animal"),
    "animal-legs-buffalo2": ("number", "animal"),
    "animal-nose-elephant": ("body part", "animal"),
    "atomic-80-state": ("state_of_matter", "chemical element"),
    "basketball-players": ("number", "sport"),
    "beverage-source-wine": ("ingredient", "beverage"),
    "bird-color-swan": ("colour", "animal"),
    "bird-country-eagle": ("country", "animal"),
    "bird-time-owl": ("time of day", "animal"),
    "birthstone-emerald-month": ("number", "month"),
    "chem-atmosphere-Z": ("number", "chemical element"),
    "chem-bones-Z": ("number", "chemical element"),
    "chem-organic-Z": ("number", "chemical element"),
    "chem-photosynthesis-Z": ("number", "chemical element"),
    "christmas-season": ("season", "holiday"),
    "city-state-Philadelphia": ("us_state", "city"),
    "colosseum-currency": ("currency", "country"),
    "element-color-gold2": ("colour", "chemical element"),
    "etym-frigg-position": ("number", "weekday"),
    "etym-saturn-position": ("number", "planet"),
    "etym-wargod-month": ("number", "month"),
    "ex-city-capital-Barcelona-Toronto": ("capital", "country"),
    "ex-city-capital-Lyon-Naples": ("capital", "country"),
    "ex-city-capital-Naples-Barcelona": ("capital", "country"),
    "ex-city-capital-Toronto-Lyon": ("capital", "country"),
    "ex-city-continent-Toronto-Lyon": ("continent", "country"),
    "ex-city-currency-Toronto-Beijing": ("currency", "country"),
    "ex-city-currency-Toronto-Mumbai": ("currency", "country"),
    "ex-city-language-Lyon-Naples": ("language", "country"),
    "ex-element-state-26-8": ("state_of_matter", "chemical element"),
    "ex-element-state-26-80": ("state_of_matter", "chemical element"),
    "ex-element-state-8-26": ("state_of_matter", "chemical element"),
    "ex-element-state-8-80": ("state_of_matter", "chemical element"),
    "ex-element-state-80-8": ("state_of_matter", "chemical element"),
    "ex-element-symbol-11-26": ("chemical symbol", "chemical element"),
    "ex-element-symbol-26-79": ("chemical symbol", "chemical element"),
    "ex-planet-color-third-fourth": ("colour", "planet"),
    "ex2-city-capital-Munich": ("capital", "country"),
    "ex2-city-capital-Osaka": ("capital", "country"),
    "ex2-city-continent-Lima": ("continent", "country"),
    "ex2-city-continent-Sydney": ("continent", "country"),
    "ex2-city-language-Cairo": ("language", "country"),
    "ex2-city-language-Moscow": ("language", "country"),
    "ex2-language-capital-Greek": ("capital", "country"),
    "ex2-language-capital-Hungarian": ("capital", "country"),
    "ex2-language-capital-Polish": ("capital", "country"),
    "ex2-language-capital-Swedish": ("capital", "country"),
    "ex2-river-capital-Thames": ("capital", "country"),
    "food-animal-butter": ("animal", "food"),
    "food-animal-honey": ("animal", "food"),
    "fruit-grows-grape": ("plant form", "fruit"),
    "func-filters-count": ("number", "organ"),
    "func-pumps-chambers": ("number", "organ"),
    "gem-color-ruby": ("colour", "gemstone"),
    "gem-source-pearl": ("source of a gem", "gemstone"),
    "greatwall-ocean": ("ocean", "country"),
    "holiday-month-christmas2": ("month", "holiday"),
    "instr-body-trumpet": ("body part", "musical instrument"),
    "instr-hit-drums": ("striking implement", "musical instrument"),
    "mars-color": ("colour", "planet"),
    "month-3-godof": ("domain of a god", "Roman god"),
    "organ-acid-stomach": ("body fluid", "organ"),
    "organ-count-kidney2": ("number", "organ"),
    "organ-location-brain": ("body structure", "organ"),
    "organ-location-heart": ("body part", "organ"),
    "osu-rival-mascot": ("animal", "us_state"),
    "paper-continent": ("continent", "country"),
    "person-century-lincoln": ("war", "person"),
    "person-country-napoleon": ("country", "person"),
    "person-country-shakespeare": ("country", "person"),
    "person-firstname-darwin": ("first_name", "person"),
    "person-firstname-einstein": ("first_name", "person"),
    "person-firstname-mozart": ("first_name", "person"),
    "person-firstname-newton": ("first_name", "person"),
    "person-firstname-shakespeare": ("first_name", "person"),
    "planet-3-moons": ("number", "planet"),
    "planet-rings-saturn2": ("planet feature", "planet"),
    "rhyme-chair-flag": ("us_state", "animal"),
    "rhyme-rain-neighbor": ("country", "country"),
    "rhyme-spoon-orbit": ("celestial body", "celestial body"),  # moon -> Earth: the brainstorm's side-table example
    "season-next-winter": ("season", "season"),
    "spaceneedle-border": ("bordering region (country or US state)", "city"),
    "spider-legs": ("number", "animal"),
    "sport-equip-tennis": ("sports equipment", "sport"),
    "super-populous-capital": ("capital", "country"),
    "super-smallest-continent": ("continent", "country"),
    "tree-product-oak": ("tree product", "tree"),
    "vehicle-power-bicycle": ("power source", "vehicle"),
    "violin-strings": ("number", "musical instrument"),
}


def load_tokenizer(target: str):
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer

    t = pins.TARGETS[target]
    path = snapshot_download(t["repo"], revision=t["revision"], local_files_only=True, ignore_patterns=t.get("snapshot_ignore"))
    return AutoTokenizer.from_pretrained(path, **t.get("tokenizer_kwargs", {}))


def forms(value: str) -> list[str]:
    """Every form of a value: as written, lower case, upper initial; each with and without a leading space."""
    cases = dict.fromkeys([value, value.lower(), value[:1].upper() + value[1:]])
    return [p + c for c in cases for p in ("", " ")]


class Tok:
    def __init__(self, target: str):
        self.target, self.tok = target, load_tokenizer(target)
        self.special = set(self.tok.all_special_ids) | {int(i) for i in self.tok.added_tokens_decoder}

    def ids(self, text: str) -> list[int]:
        return list(self.tok(text, add_special_tokens=False).input_ids)

    def wordlike(self, i: int) -> bool:
        return i not in self.special and bool(_WORDLIKE.search(self.tok.decode([i])))

    def first_tokens(self, values: list[str]) -> set[int]:
        out = set()
        for v in values:
            for f in forms(v):
                ids = self.ids(f)
                if ids and self.wordlike(ids[0]):
                    out.add(ids[0])
        return out

    def name_tokens(self, names: list[str]) -> set[int]:
        return {i for n in names for f in forms(n) for i in self.ids(f)}

    def concept_token(self, word: str) -> int | None:
        """tokens.concept_token's rule: the first single-token surface among ' X', 'X', ' x', 'x', ' Xc', 'Xc'."""
        c = word.strip()
        for s in (" " + c, c, " " + c.lower(), c.lower(), " " + c.capitalize(), c.capitalize()):
            ids = self.ids(s)
            if len(ids) == 1:
                return ids[0]
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(pins.DATA_DIR / "paper_answer_types.json"))
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"{a.out} exists; the vocabularies are frozen (note 39), never rebuilt in place"
    items = json.loads(pins.PROBE_SWAP_FILE.read_bytes())["items"]
    assert hashlib.sha256(pins.PROBE_SWAP_FILE.read_bytes()).hexdigest() == pins.PROBE_SWAP_SHA256
    assert set(ITEM_TYPES) == {it["name"] for it in items}, "every item needs its types"
    for t, spec in TYPES.items():
        assert len(spec["values"]) >= 8 and len(set(spec["values"])) == len(spec["values"]), t
        for o in spec.get("off", []):
            assert o in TYPES and o != t, (t, o)

    toks = {t: Tok(t) for t in TOKENIZERS}
    type_tokens = {t: {ty: sorted(tk.first_tokens(spec["values"])) for ty, spec in TYPES.items()} for t, tk in toks.items()}
    out_items = {}
    for it in items:
        name = it["name"]
        atype, itype = ITEM_TYPES[name]
        closed = atype in TYPES and not TYPES[atype].get("off_only")
        side = closed and atype == itype
        row = {"answer_type": atype, "intermediate_type": itype, "closed_vocabulary": closed,
               "set": "own_pair_only" if not closed else "side_table" if side else "primary",
               "side_table_reason": "answer type equals the intermediate's type" if atype == itype else None,
               "word_or_number": "number" if atype == "number" else "word", "tokens": {}}  # fmt: skip
        for t, tk in toks.items():
            excluded = tk.name_tokens([it["intermediate"], it["swap_to"]])
            own = tk.first_tokens([it["answer"], it["swap_answer"]]) - excluded
            entry = {"excluded": sorted(excluded), "own": sorted(own)}
            ct = [tk.concept_token(it[k]) for k in ("answer", "swap_answer")]
            entry["own_answer_token_excluded"] = any(c is not None and c in excluded for c in ct)
            if closed:
                scrub = (set(type_tokens[t][atype]) | tk.first_tokens([it["answer"], it["swap_answer"]])) - excluded
                rng = random.Random(f"n39off:{t}:{name}")
                off, sources = [], {}
                for cat in TYPES[atype]["off"]:
                    need = len(scrub) - len(off)
                    if need <= 0:
                        break
                    pool = sorted(set(type_tokens[t][cat]) - scrub - excluded - set(off))
                    pick = sorted(rng.sample(pool, need)) if len(pool) > need else pool
                    off += pick
                    sources[cat] = len(pick)
                entry.update(scrub=sorted(scrub), off=sorted(off), off_sources=sources, off_shortfall=len(scrub) - len(off))
            row["tokens"][t] = entry
        out_items[name] = row

    blob = {
        "about": "prereg amendment 65 note 39: category vocabularies for data/probe_swap.json, frozen before any note-39 "
        "forward pass; written by a CPU agent from the answer-type labels alone, no model access (tokenizers only). "
        "Built by scripts/paper_answer_types_build.py (its docstring has the rules).",
        "built_utc": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
        "probe_swap_sha256": pins.PROBE_SWAP_SHA256,
        "tokenizers": {t: {"repo": pins.TARGETS[t]["repo"], "revision": pins.TARGETS[t]["revision"]} for t in TOKENIZERS},
        "rules": {
            "forms": "as written, lower case, upper initial; each with and without a leading space; the first token of "
            "each form's tokenization (add_special_tokens=False); tokens with no letter or digit and special tokens "
            "dropped",
            "scrub": "type vocabulary first tokens + the item's own answer and swap answer first tokens, minus every "
            "token of every form of the item's intermediate and swap_to",
            "own": "the item's own answer and swap answer first tokens, minus the excluded name tokens (arm 8)",
            "off": "arm 6: len(scrub) tokens from the off chain (seeded random.Random('n39off:<tokenizer>:<item>')), "
            "first category first; never a scrub or excluded token",
            "sets": "primary = closed answer type (note 39's list) and not side table; side_table = answer type equals "
            "the intermediate's type; own_pair_only = no closed vocabulary. Per tokenizer, own_answer_token_excluded "
            "items also belong to the side table (an addition to note 39, flagged).",
        },
        "types": TYPES,
        "type_tokens": {t: {ty: {str(i): toks[t].tok.decode([i]) for i in ids} for ty, ids in by.items()}
                        for t, by in type_tokens.items()},  # fmt: skip
        "items": out_items,
    }
    Path(a.out).write_text(json.dumps(blob, indent=1, ensure_ascii=False, sort_keys=False) + "\n")
    sha = hashlib.sha256(Path(a.out).read_bytes()).hexdigest()
    print("wrote", a.out, "sha256", sha)
    sets: dict = {}
    for r in out_items.values():
        sets[r["set"]] = sets.get(r["set"], 0) + 1
    print("sets", sets)
    by_type: dict = {}
    for r in out_items.values():
        by_type[r["answer_type"]] = by_type.get(r["answer_type"], 0) + 1
    print("items per answer type", dict(sorted(by_type.items(), key=lambda kv: -kv[1])))
    for t in TOKENIZERS:
        sizes = {ty: len(v) for ty, v in type_tokens[t].items()}
        print(t, "type token counts", sizes)
        prim = [r for r in out_items.values() if r["closed_vocabulary"]]
        ns = [len(r["tokens"][t]["scrub"]) for r in prim]
        short = {n: r["tokens"][t]["off_shortfall"] for n, r in out_items.items() if r["closed_vocabulary"] and r["tokens"][t]["off_shortfall"]}
        ex = [n for n, r in out_items.items() if r["tokens"][t]["own_answer_token_excluded"]]
        print(f"  scrub size min/median/max {min(ns)}/{sorted(ns)[len(ns) // 2]}/{max(ns)}; off shortfall {short}; own answer token excluded {ex}")


if __name__ == "__main__":
    main()
