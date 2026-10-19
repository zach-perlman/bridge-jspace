"""B1 (the paper's 90 two-hop items, data/probe_swap.json, unchanged) annotated for part B's analyses: the bridge's kind,
and whether the answer is tied one-to-one to the bridge (the France -> Paris risk: capitals, languages, first names,
symbols, ordinals, unique parts) or shared by many bridges (states of matter, colours, counts, seasons)."""

import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from b1_by_kind import PERSON, PLACE

ONE_TO_ONE = {  # answer named uniquely by the bridge (or bridge named uniquely by the answer)
    "amazon-language",
    "animal-nose-elephant",
    "beverage-source-wine",
    "bird-country-eagle",
    "birthstone-emerald-month",
    "chem-atmosphere-Z",
    "chem-bones-Z",
    "chem-organic-Z",
    "chem-photosynthesis-Z",
    "city-state-Philadelphia",
    "colosseum-currency",
    "etym-frigg-position",
    "etym-saturn-position",
    "etym-wargod-month",
    "ex-city-capital-Barcelona-Toronto",
    "ex-city-capital-Lyon-Naples",
    "ex-city-capital-Naples-Barcelona",
    "ex-city-capital-Toronto-Lyon",
    "ex-city-continent-Toronto-Lyon",
    "ex-city-currency-Toronto-Beijing",
    "ex-city-currency-Toronto-Mumbai",
    "ex-city-language-Lyon-Naples",
    "ex-element-symbol-11-26",
    "ex-element-symbol-26-79",
    "ex2-city-capital-Munich",
    "ex2-city-capital-Osaka",
    "ex2-city-continent-Lima",
    "ex2-city-continent-Sydney",
    "ex2-city-language-Cairo",
    "ex2-city-language-Moscow",
    "ex2-language-capital-Greek",
    "ex2-language-capital-Hungarian",
    "ex2-language-capital-Polish",
    "ex2-language-capital-Swedish",
    "ex2-river-capital-Thames",
    "food-animal-honey",
    "gem-source-pearl",
    "greatwall-ocean",
    "instr-hit-drums",
    "month-3-godof",
    "organ-acid-stomach",
    "organ-location-brain",
    "osu-rival-mascot",
    "paper-continent",
    "person-century-lincoln",
    "person-country-napoleon",
    "person-country-shakespeare",
    "person-firstname-darwin",
    "person-firstname-einstein",
    "person-firstname-mozart",
    "person-firstname-newton",
    "person-firstname-shakespeare",
    "planet-rings-saturn2",
    "rhyme-chair-flag",
    "rhyme-rain-neighbor",
    "rhyme-spoon-orbit",
    "season-next-winter",
    "spaceneedle-border",
    "super-populous-capital",
    "super-smallest-continent",
    "tree-product-oak",
}
items = json.loads(Path("data/probe_swap.json").read_text())["items"]
rows = []
for it in items:
    b = it["intermediate"]
    kind = "place" if b in PLACE else "person" if b in PERSON else "other"
    rel = "one_to_one" if it["name"] in ONE_TO_ONE else "many_to_one"
    rows.append(
        {
            "name": it["name"],
            "category": it["category"],
            "bridge": b,
            "answer": it["answer"],
            "bridge_kind": kind,
            "relation": rel,
            "clean": kind != "place" and rel == "many_to_one",
        }
    )
assert {r["name"] for r in rows} >= ONE_TO_ONE, "a listed name is not in probe_swap.json"
blob = {"about": __doc__, "source": "data/probe_swap.json (unchanged)", "items": rows}
Path("data/suite_v1/B1_annotations.json").write_text(json.dumps(blob, indent=1) + "\n")
print(collections.Counter((r["bridge_kind"], r["relation"]) for r in rows), "clean:", sum(r["clean"] for r in rows))
