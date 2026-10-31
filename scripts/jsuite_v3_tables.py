"""jsuite_v3_tables (Zach, 2026-10-27, prereg amendment 58 note 4): templates for jsuite v3's facts module.

The four kept relations (people -> nationality, cities -> country, companies -> country, landmarks -> country) reuse
jsuite_v2_tables.REL2's templates; films -> director is new. Each relation adds, for v3's new finals and formats:
  hlink   the hard-read link to a made-up anchor of the same type ("{x} is in the same country as {y}.")
  anchor  the anchor kind (made-up names drawn per scene: person, town, company, landmark, film)
  triple  relation names for the table / JSON renderings: bind, kfact, pfact
The bridges, answers and descriptions come from data/v3_bridges.json (written by hand, fact-checked; see its audit).
"""

from __future__ import annotations

import copy
import json
import random
from pathlib import Path

from scripts import jsuite_v2_tables as TB

ROOT = Path(__file__).resolve().parents[1]
BRIDGES = ROOT / "data" / "v3_bridges.json"

FILMS = {
    "noun": "film",
    "unknown": "an unnamed film",
    "bind": ["{p}'s favorite film is {x}.", "{p} watched {x} three times last month.", "{p} wrote a film-school essay on {x}."],
    "pdesc": ["{p}'s favorite film", "the film {p} watched three times last month", "the film {p} wrote a film-school essay on"],
    "q1P": ["What is {p}'s favorite film?", "Which film did {p} watch three times last month?",
            "Which film did {p} write a film-school essay on?"],
    "q1M": ["Which {noun} {rel}?", "Which {noun} {rel}?", "Which {noun} {rel}?"],
    "q2M": ["Who directed {d}?", "Who was the director of {d}?", "{D} was directed by whom?"],
    "kfact": ["{x} was directed by {a}.", "{a} directed {x}.", "{x} is a film by {a}."],
    "pfact": ["At the festival, a restored print of {x} will be introduced by {a}.",
              "{a} will introduce the festival's restored print of {x}.",
              "The festival screening of {x} will be introduced by {a}."],
    "q2P": ["Who will introduce the restored print of {d} at the festival?",
            "Who is introducing the festival's restored print of {d}?",
            "The festival's restored print of {d} will be introduced by whom?"],
    "nfact": ["{x} was mentioned in this week's film column.", "A reader asked a question about {x} in the letters page.",
              "The quiz night included a round on {x}."],
    "track": (["film club", "summer cinema", "festival jury", "student society"], "{pre}the {o} screened {e}.",
              "the film the {o} screened last", "Which film did the {o} screen last?"),
}  # fmt: skip

EXTRA = {  # hard-read links, anchor kinds and triple relation names per relation
    "people": {"hlink": ["{x} had the same nationality as {y}.", "{x} and {y} had the same nationality.",
                         "{x} shared a nationality with {y}."], "anchor": "person",
               "triple": {"bind": "dissertation subject", "kfact": "nationality", "pfact": "nationality of actor in new film",
                          "hlink": "same nationality as"}},
    "cities": {"hlink": ["{x} is in the same country as {y}.", "{x} and {y} are in the same country.",
                         "{x} lies in the same country as {y}."], "anchor": "town",
               "triple": {"bind": "moved to last spring", "kfact": "country", "pfact": "country of partner city",
                          "hlink": "same country as"}},
    "companies": {"hlink": ["{x} comes from the same country as {y}.", "{x} and {y} come from the same country.",
                            "{x} was founded in the same country as {y}."], "anchor": "company",
                  "triple": {"bind": "case study subject", "kfact": "country of origin", "pfact": "country of next regional office",
                             "hlink": "same country of origin as"}},
    "landmarks": {"hlink": ["{x} is in the same country as {y}.", "{x} and {y} are in the same country.",
                            "You can find {x} in the same country as {y}."], "anchor": "landmark",
                  "triple": {"bind": "visited last summer", "kfact": "country", "pfact": "country of documentary studio",
                             "hlink": "same country as"}},
    "films": {"hlink": ["{x} had the same director as {y}.", "{x} and {y} had the same director.",
                        "{x} was made by the same director as {y}."], "anchor": "film",
              "triple": {"bind": "favorite film", "kfact": "director", "pfact": "introducer of restored print",
                         "hlink": "same director as"}},
}  # fmt: skip

ANCHOR_HEAD = {"person": None, "town": "", "company": "{n} Works", "landmark": "the {n} Arch", "film": "{n}"}
SYL = ["bar", "del", "fen", "gor", "hal", "ket", "lom", "mar", "nev", "pol", "quin", "ros", "sal", "tav", "vel",
       "wen", "dra", "bri", "cor", "lun", "mir", "tor", "vor", "zan", "ker", "lis", "mon", "ral", "sev", "tir"]  # fmt: skip
FIRST = ["Elric", "Maren", "Tobin", "Liesel", "Corvin", "Annika", "Rafe", "Ilse", "Dorian", "Petra", "Soren", "Wilma"]


def pseudo(rng: random.Random) -> str:
    return (rng.choice(SYL) + rng.choice(SYL) + rng.choice(["", "t", "n", "s", "holt", "ford", "mark"])).capitalize()


def anchor_name(kind: str, rng: random.Random, taken: set[str]) -> str:
    """A made-up name of the bridge's type, never a real bridge, answer or passage name (checked by the caller)."""
    while True:
        if kind == "person":
            name = f"{rng.choice(FIRST)} {pseudo(rng)}"
        elif kind == "film":
            name = f"The {pseudo(rng)} {rng.choice(['Letters', 'Harbor', 'Crossing', 'Winter', 'Garden', 'Signal'])}"
        elif kind == "company":
            name = f"{pseudo(rng)} {rng.choice(['Works', 'Industries', 'Labs', 'Group'])}"
        elif kind == "landmark":
            name = f"the {pseudo(rng)} {rng.choice(['Arch', 'Tower', 'Falls', 'Abbey'])}"
        else:
            name = pseudo(rng)
        if name not in taken:
            taken.add(name)
            return name


def tables() -> dict:
    """relation -> table: REL2's templates (films: FILMS), EXTRA's keys, and facts from data/v3_bridges.json as
    {bridge: (answer, [(noun, clause), ...], popularity)} plus 'meta' {bridge: row} for flags and aliases."""
    rows = json.loads(BRIDGES.read_text())
    out = {}
    for rel in ("people", "cities", "companies", "landmarks", "films"):
        base = copy.deepcopy(FILMS if rel == "films" else {k: v for k, v in TB.REL2[rel].items() if k != "facts"})
        base.update(EXTRA[rel])
        mine = [r for r in rows if r["relation"] == rel]
        base["facts"] = {r["bridge"]: (r["answer"], [(d["noun"], d["clause"]) for d in r["descriptions"]], r["popularity"])
                         for r in mine}  # fmt: skip
        base["meta"] = {r["bridge"]: r for r in mine}
        out[rel] = base
    return out
