"""score_greedy (Zach, 2026-10-27, prereg amendment 58 note 1's rule): free-generation accuracy of greedy_all replies, and
its agreement with the cand2 read of the model's stored competence run, per word.

Rule (note 1, fixed before scoring): strip markdown emphasis and quotes, then one leading fixed phrase ("the answer is",
"answer:", "it is", "it's"), then whitespace and punctuation. The reply is right if it then starts with the answer or an
alias (case-insensitive, accents folded), followed by a non-letter or the end. Any other text before the answer
(including reasoning) is wrong. Aliases: ALIASES below (noun/adjective forms, class names, number words), built from the
candidate lists before scoring; changes after the 50-reply hand check are listed in CHANGES.

python scripts/score_greedy.py RUN COMPETENCE_RUN   (results/greedy_all/RUN, results/tasks_v2/COMPETENCE_RUN)
"""

from __future__ import annotations

import collections
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGES: list[str] = []  # alias changes made after the hand check (none yet)

PAIRS = {  # country noun <-> adjective / language forms; both count for either
    "Argentina": ["Argentine", "Argentinian", "Argentinean"], "Australia": ["Australian"], "Austria": ["Austrian"],
    "Belgium": ["Belgian"], "Brazil": ["Brazilian"], "Cambodia": ["Cambodian"], "Canada": ["Canadian"],
    "Chile": ["Chilean"], "China": ["Chinese"], "Colombia": ["Colombian"], "Czech Republic": ["Czech", "Czechia"],
    "Denmark": ["Danish"], "Ecuador": ["Ecuadorian"], "Egypt": ["Egyptian"], "Finland": ["Finnish"],
    "France": ["French"], "Germany": ["German"], "Greece": ["Greek"], "Hungary": ["Hungarian"], "India": ["Indian"],
    "Indonesia": ["Indonesian"], "Iran": ["Iranian", "Persia", "Persian"], "Ireland": ["Irish"], "Israel": ["Israeli"],
    "Italy": ["Italian"], "Jamaica": ["Jamaican"], "Japan": ["Japanese"], "Jordan": ["Jordanian"],
    "Malaysia": ["Malaysian"], "Mexico": ["Mexican"], "Morocco": ["Moroccan"], "Netherlands": ["Dutch", "Holland"],
    "Norway": ["Norwegian"], "Peru": ["Peruvian"], "Poland": ["Polish"], "Portugal": ["Portuguese"],
    "Russia": ["Russian"], "South Africa": ["South African"], "South Korea": ["Korea", "Korean", "South Korean"],
    "Spain": ["Spanish"], "Sweden": ["Swedish"], "Switzerland": ["Swiss"], "Tanzania": ["Tanzanian"],
    "Thailand": ["Thai"], "Turkey": ["Turkish", "Türkiye"], "Venezuela": ["Venezuelan"], "Vietnam": ["Vietnamese"],
    "United States": ["American", "USA", "U.S.", "US", "America"],
}  # fmt: skip
EXTRA = {
    "Mandarin": ["Chinese", "Mandarin Chinese"], "Persian": ["Farsi"], "Hebrew": [], "Arabic": [], "English": [],
    "mammal": ["mammals", "Mammalia"], "insect": ["insects", "Insecta"], "reptile": ["reptiles", "Reptilia"],
    "bird": ["birds", "Aves"], "fish": ["fishes", "Pisces", "Actinopterygii", "Osteichthyes"],
    "amphibian": ["amphibians", "Amphibia"],
    "1": ["one"], "2": ["two"], "3": ["three"], "4": ["four"], "5": ["five"], "6": ["six"], "7": ["seven"],
    "8": ["eight"], "9": ["nine"],
}  # fmt: skip
ALIASES: dict[str, set[str]] = collections.defaultdict(set)
for noun, forms in PAIRS.items():
    group = {noun, *forms}
    for x in group:
        ALIASES[x] |= group
for k, forms in EXTRA.items():
    ALIASES[k] |= {k, *forms}

PHRASES = ["the answer is", "answer:", "it is", "it's", "it’s"]


def fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def clean(text: str) -> str:
    t = fold(text).strip().lstrip("*_\"'`“”‘’ ").strip()
    for ph in PHRASES:
        if t.startswith(ph):
            t = t[len(ph) :].strip()
            break
    return t.lstrip("*_\"'`“”‘’:.,- ").strip()


def right(text: str, answer: str) -> bool:
    t = clean(text)
    for a in ALIASES.get(answer, set()) | {answer}:
        fa = fold(a)
        if t.startswith(fa) and (len(t) == len(fa) or not t[len(fa)].isalpha()):
            return True
    return False


def main(run: str, comp: str) -> None:
    rows = [json.loads(line) for line in (ROOT / "results/greedy_all" / run / "rows.jsonl").open()]
    cand = {}
    for line in (ROOT / "results/tasks_v2" / comp / "items.jsonl").open():
        r = json.loads(line)
        if r.get("part") == "whole":
            cand[r["id"]] = bool(r.get("correct_cand2"))
    cells: dict = {}
    by_word = collections.defaultdict(list)
    for r in rows:
        g = right(r["text"], r["answer"])
        by_word[r["word"]].append((g, cand.get(r["id"])))
        r["greedy_right"] = g
    for w, xs in sorted(by_word.items()):
        both = [(g, c) for g, c in xs if c is not None]
        cells[w] = {"n": len(xs), "greedy_acc": round(sum(g for g, _ in xs) / len(xs), 4),
                    "cand2_acc": round(sum(c for _, c in both) / len(both), 4) if both else None,
                    "agree": round(sum(g == c for g, c in both) / len(both), 4) if both else None,
                    "greedy_only": sum(g and not c for g, c in both), "cand2_only": sum(c and not g for g, c in both)}  # fmt: skip
    out = ROOT / "results/greedy_all" / run / "score_v1.json"
    out.write_text(json.dumps({"rule": "amendment 58 note 1", "competence": comp, "alias_changes": CHANGES, "cells": cells}, indent=1) + "\n")
    disagree = [r for r in rows if cand.get(r["id"]) is not None and r["greedy_right"] != cand[r["id"]]]
    (ROOT / "results/greedy_all" / run / "disagreements_v1.jsonl").write_text("".join(json.dumps(r) + "\n" for r in disagree))
    tot = [x for xs in by_word.values() for x in xs if x[1] is not None]
    print(run, "greedy", round(sum(g for g, _ in tot) / len(tot), 4), "cand2", round(sum(c for _, c in tot) / len(tot), 4),
          "agree", round(sum(g == c for g, c in tot) / len(tot), 4), "n", len(tot), "disagreements", len(disagree))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
