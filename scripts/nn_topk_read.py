"""nn_topk_read (2026-10-29, prereg amendment 59 note 26 (a) and its addendum): what the lens's top-20 tokens at the bridge are.
Descriptive, with the addendum's fixed readings. Reads the topk.jsonl of nn_readout --topk 20 runs ({P}nn_readout_v4ctl_v1: v4 MP / MM
gated ok and fail, H1 and RG for scenes whose MM is v4ok; {P}nn_readout_v4cc_v1: cue-conflict MP / MM, conflict and aligned).

Unit: one top-20 list per item x site x lens x variant ("top" = full vocabulary, "letters" = letter tokens only) x even layer.
Primary: J++ ("jlens"), letters, inside note 25's windows (scripts.nn_priming_read.windows; Muse by note 28's rule).
Normalisation: NFKC; leading space noted; non-word characters stripped at both ends ("(N" -> N); casefold; script of the first
letter; concept key = fold minus a trailing "s" / "'s".
Word match: token t matches word W if fold(t) is W, its plural or its possessive; or t is the tokenizer's first token of " W" / "W"
(lowercased too) with >= 3 letters; or t starts a word, has >= 4 letters and is a prefix of W. Tokens of 1-2 letters never match.
Categories, first match wins: JUNK (no letter), FUNC (NLTK English stopwords), REAL (X's remembered attribute and its country /
adjective aliases), PV_X (X's passage value), CUE (conflict items' cue), CTX_VAL (other entities' values), CLASS (the relation's
other answers), BRIDGE (X's name words, >= 3 letters, not in the description), CTX_NAME (other entities' names), OCC (people: the
description's noun and a fixed synonym list, when absent from the prompt), KNOW (content words >= 4 letters of X's other
description, absent from the prompt), DESC (the description's content words), FRAME (question words outside the description,
plus a fixed relation-type list), PASSAGE (the passage's other content words), CODE, then translated names (babel territory and
eponymous-language names in 15 locales, for country-type values: a match takes REAL / PV_X / CUE / CTX_VAL / CLASS, flagged
translated), NONLATIN_OTHER (non-Latin first letter, unmatched), OTHER.
Metrics (mean over items, cluster bootstrap over bridges, 2000 draws, seed 0): share of the top-20 per category (window mean);
presence (in the top-20) by layer and anywhere in the window; first window layer present.
Controls: C1, shuffled item (this item's lists scored against another item's REAL / BRIDGE / OCC / KNOW lists: same relation,
different REAL, random.Random("c1:" + id)); C2 the logit lens (every cell is also computed for it); C3 H1 vs MM and C4 MP vs MM,
paired by scene.
Readings (description end, window, J++ letters; primary pool: the scenes whose MP and MM are both v4ok, both items, as note 25):
  1. "attribute cloud at the bridge": REAL presence - C1 >= 0.20, OCC or KNOW presence - C1 >= 0.15, BRIDGE presence < REAL's.
  2. "name first, then attributes": on items with both in the window, median first layer of BRIDGE >= 4 layers before REAL's.
  3. "class priming, not this person": REAL presence < 3x the mean per-value presence of CLASS.
  4. "multilingual noise floor": NONLATIN_OTHER + CODE >= 0.3 of the list while translated content < 0.05 (the lens's floor).
  5. token-level priming: REAL presence on MP and MM within +-0.10 (paired by scene; the interval inside +-0.10); PV_X at C1's
     level at the description end (PV_X presence - C1's REAL presence, interval inside +-0.10); PV_X ahead of REAL on MP at the
     final token (presence difference > 0, interval above 0).
Descriptive: success vs failure (MM_fail vs MM_ok, MP_fail vs MP_ok), cue vs REAL on conflict items (all / known / gated when the
run's rows.jsonl carries the tags), H1 and RG vs MM, every family, variant and lens (readings 1-4 per cell).
Interpretations where the addendum is silent (listed in the JSON under "interpretations"): value categories use the same alias
groups as REAL; Han / kana / Hangul characters count 2 letters each (--cjk-weight), and in scripts written without spaces a token
containing a translated name matches it (CJK and Thai affixes: "日本人", "的日本"); translated names are tried on every token still
unclassified at that step (the locales include Latin-script ones: "Deutschland"), on Latin tokens without the first-token clause;
PASSAGE leaves out the words of the scene's names and values; a token "starts a word" if it has a leading space,
an opening bracket or quote, a capital first letter, or a first letter of an uncased script; FRAME includes the answer instruction's
words; on H1 (no passage) the scene's passage words and values keep their categories (not in the prompt there).

python scripts/nn_topk_read.py PREFIX [--translations PATH] [--run-dir DIR ...] [--out-dir DIR]
  PREFIX "qwen35_9b_", "" for the 27B, "nem35l_", "muse30_". Writes {out}/{P}v4_n26a.json, {P}v4_n26a_wall.txt (token wall: the first
  scene per relation by id, layers x top-10 with category tags, MP and MM side by side) and {P}v4_n26a_shares.csv (window shares).
  The translations file is made by babel on the VPS (scratch make_translations.py; its sha256 is recorded).
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import os
import random
import re
import statistics
import subprocess
import sys
import unicodedata
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from scripts.nn_priming_read import windows  # noqa: E402

RES = ROOT / "results" / "nn_readout"
DATA = ROOT / "data" / "tasks_v2"
TARGET_OF = {"qwen35_9b_": "qwen3.5-9b", "": "qwen3.6-27b", "nem35l_": "nemotron-3.5-lightning", "muse30_": "muse-glimmer-30b"}
INSTRUCTION = "Answer with just the answer, nothing else."  # scripts/tasks_v2.NATURAL_CHAT_INSTRUCTION (v4's chat framing)

CATS = ["JUNK", "FUNC", "REAL", "PV_X", "CUE", "CTX_VAL", "CLASS", "BRIDGE", "CTX_NAME", "OCC", "KNOW", "DESC", "FRAME", "PASSAGE",
        "CODE", "NONLATIN_OTHER", "OTHER"]  # fmt: skip
RANK = {c: i for i, c in enumerate(CATS)}
VALUE_CATS = ("REAL", "PV_X", "CUE", "CTX_VAL", "CLASS")
PERSON_CATS = ("BRIDGE", "OCC", "KNOW")  # C1 swaps these (and REAL) for another item's
EXTRA = ["TRANSLATED", "TRANSLATED_NONLATIN"]  # tokens matched through a translated name (all scripts / non-Latin only)
TAG = {"JUNK": "J", "FUNC": "F", "REAL": "R", "PV_X": "PV", "CUE": "CU", "CTX_VAL": "CV", "CLASS": "CL", "BRIDGE": "B", "CTX_NAME": "CN",
       "OCC": "OC", "KNOW": "K", "DESC": "D", "FRAME": "FR", "PASSAGE": "PA", "CODE": "CD", "NONLATIN_OTHER": "NL", "OTHER": "O"}  # fmt: skip

# NLTK's English stopword list (nltk.corpus.stopwords.words("english"), 179 words; nltk is not in the venv)
STOP = set("""i me my myself we our ours ourselves you you're you've you'll you'd your yours yourself yourselves he him his himself she
she's her hers herself it it's its itself they them their theirs themselves what which who whom this that that'll these those am is
are was were be been being have has had having do does did doing a an the and but if or because as until while of at by for with about
against between into through during before after above below to from up down in out on off over under again further then once here
there when where why how all any both each few more most other some such no nor not only own same so than too very s t can will just
don don't should should've now d ll m o re ve y ain aren aren't couldn couldn't didn didn't doesn doesn't hadn hadn't hasn hasn't haven
haven't isn isn't ma mightn mightn't mustn mustn't needn needn't shan shan't shouldn shouldn't wasn wasn't weren weren't won won't
wouldn wouldn't""".split())
assert len(STOP) == 179, len(STOP)

# Country-type values: alias group (ISO territory code) -> English names (country, adjective / demonym, established other names;
# written from scripts/jsuite_v2_tables.DERIV's country / adjective pairs, without its language, region and continent words). A
# value's aliases are its group's names plus the items' (and data/v3_bridges.json's) answer_aliases.
GROUPS = {
    "AR": ["Argentina", "Argentine", "Argentinian"], "AU": ["Australia", "Australian", "Aussie"], "AT": ["Austria", "Austrian"],
    "BE": ["Belgium", "Belgian"], "BR": ["Brazil", "Brazilian"], "KH": ["Cambodia", "Cambodian", "Khmer"], "CA": ["Canada", "Canadian"],
    "CL": ["Chile", "Chilean"], "CN": ["China", "Chinese"], "CO": ["Colombia", "Colombian"],
    "CZ": ["Czech Republic", "Czech", "Czechia"], "DK": ["Denmark", "Danish", "Dane", "Danes"],
    "EG": ["Egypt", "Egyptian"], "FI": ["Finland", "Finnish", "Finn", "Finns"], "FR": ["France", "French"],
    "DE": ["Germany", "German"], "GR": ["Greece", "Greek", "Hellenic"], "HU": ["Hungary", "Hungarian"],
    "IN": ["India", "Indian"], "ID": ["Indonesia", "Indonesian"], "IE": ["Ireland", "Irish"], "IL": ["Israel", "Israeli"],
    "IT": ["Italy", "Italian"], "JM": ["Jamaica", "Jamaican"], "JP": ["Japan", "Japanese"], "JO": ["Jordan", "Jordanian"],
    "KE": ["Kenya", "Kenyan"], "MY": ["Malaysia", "Malaysian"], "MX": ["Mexico", "Mexican"], "MA": ["Morocco", "Moroccan"],
    "NL": ["Netherlands", "Dutch", "Holland"], "NG": ["Nigeria", "Nigerian"], "NO": ["Norway", "Norwegian"], "PE": ["Peru", "Peruvian"],
    "PL": ["Poland", "Polish"], "PT": ["Portugal", "Portuguese"], "RU": ["Russia", "Russian"],
    "ZA": ["South Africa", "South African"], "KR": ["South Korea", "South Korean", "Korea", "Korean"],
    "ES": ["Spain", "Spanish", "Spaniard"], "SE": ["Sweden", "Swedish", "Swede", "Swedes"], "TW": ["Taiwan", "Taiwanese"],
    "TZ": ["Tanzania", "Tanzanian"], "TH": ["Thailand", "Thai"], "TR": ["Turkey", "Turkish", "Turk", "Turkiye"],
    "US": ["United States", "American", "America", "USA"], "GB": ["English", "England", "British", "Britain"],
    "VE": ["Venezuela", "Venezuelan"], "VN": ["Vietnam", "Vietnamese"],
}  # fmt: skip
GROUP_OF = {name: g for g, names in GROUPS.items() for name in names[:2]}  # the values themselves (country / adjective)
GROUP_OF.update({"Czech": "CZ", "Korea": "KR", "Holland": "NL"})

# OCC: v4 people's description nouns come from data/v3_bridges.json; the cue-conflict people (scripts/jsuite_v4cc.py's CC) have none
# there, so theirs are fixed here (well-known occupations, by hand).
CC_NOUN = {
    "Forster": "novelist", "Kipling": "writer", "Mann": "novelist", "Bizet": "composer", "Puccini": "composer", "Verdi": "composer",
    "Rossini": "composer", "Mendelssohn": "composer", "Ravel": "composer", "Rimsky-Korsakov": "composer", "Tchaikovsky": "composer",
    "Haydn": "composer", "Mozart": "composer", "Dvorak": "composer", "Shakespeare": "playwright", "Hemingway": "novelist",
    "Christie": "novelist", "Byron": "poet", "Van Gogh": "painter", "Picasso": "painter", "Leone": "director", "Hitchcock": "director",
    "Lloyd Webber": "composer", "Sullivan": "composer", "Irving": "writer", "Wilde": "writer", "Forman": "director", "Luhrmann": "director",
    "Twain": "writer", "Utzon": "architect", "Bartholdi": "sculptor", "Pearl Buck": "novelist", "Blixen": "writer", "Lean": "director",
    "Greene": "novelist", "Chopin": "composer", "Canaletto": "painter", "Holbein": "painter", "Columbus": "explorer",
    "Magellan": "explorer", "Vespucci": "explorer", "Cuarón": "director", "del Toro": "director", "von Trier": "director",
    "Wenders": "director", "Verhoeven": "director", "Bertolucci": "director", "Garbo": "actress", "Chaplin": "actor", "Marco Polo": "explorer",
}  # fmt: skip
# the fixed synonym list per noun (the noun itself is always in)
OCC_SYN = {
    "composer": ["composers", "compose", "composition", "music", "musical", "musician", "symphony", "opera", "sonata", "concerto"],
    "inventor": ["invention", "inventions", "invent", "engineer"], "printer": ["printing", "print", "press", "typography"],
    "doctor": ["physician", "medicine", "medical", "surgeon"], "writer": ["author", "novel", "novelist", "literature", "literary", "fiction"],
    "painter": ["painting", "paintings", "paint", "art", "artist", "canvas"], "philosopher": ["philosophy", "philosophical", "thinker"],
    "astronomer": ["astronomy", "astronomical", "telescope"], "scientist": ["science", "scientific", "physicist"],
    "artist": ["art", "painter", "painting", "sculptor"], "pope": ["papal", "pontiff", "Vatican", "catholic"],
    "pianist": ["piano", "music", "musician"], "architect": ["architecture", "architectural", "building"],
    "playwright": ["play", "plays", "theatre", "theater", "drama", "dramatist"], "cartoonist": ["cartoon", "comic", "comics", "illustrator"],
    "chemist": ["chemistry", "chemical"], "botanist": ["botany", "plants", "taxonomy", "naturalist"],
    "mathematician": ["mathematics", "math", "maths", "mathematical"], "leader": ["president", "politician", "political", "statesman"],
    "poet": ["poetry", "poem", "poems", "verse"], "novelist": ["novel", "novels", "writer", "author", "fiction", "literature", "literary"],
    "general": ["military", "army", "commander"], "physicist": ["physics", "scientist"],
    "footballer": ["football", "soccer", "player", "striker"], "singer": ["song", "songs", "music", "musician"],
    "ice hockey player": ["hockey", "player", "NHL"], "wildlife presenter": ["wildlife", "presenter", "zoologist", "naturalist"],
    "cricketer": ["cricket", "batsman"], "archbishop": ["bishop", "clergy", "priest", "Anglican"],
    "runner": ["running", "marathon", "athlete", "athletics"], "sprinter": ["sprint", "runner", "athlete", "athletics", "Olympic"],
    "director": ["filmmaker", "film", "films", "movie", "movies", "cinema"], "sculptor": ["sculpture", "statue", "artist"],
    "explorer": ["exploration", "navigator", "voyage", "sailor"], "actress": ["actor", "acting", "film", "cinema"],
    "actor": ["actress", "acting", "film", "cinema", "comedian"],
}  # fmt: skip
# FRAME's fixed relation-type list (words naming the kinds of relation v4 asks)
RELATION_WORDS = ["nationality", "national", "citizen", "citizenship", "country", "nation", "born", "birth", "birthplace", "native", "origin",
                  "located", "location", "situated", "headquarters", "headquartered", "based", "director", "directed", "directing", "filmmaker"]  # fmt: skip

HAS_LETTER = re.compile(r"[^\W\d_]")
STRIP = re.compile(r"^[\W_]+|[\W_]+$")
WORD = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*")
OPENERS = set("([{\"“«‘'¿¡")
WIDE = ("CJK", "HIRAGANA", "KATAKANA", "HANGUL")  # one character, one syllable or morpheme
NOSPACE = WIDE + ("THAI",)  # scripts written without spaces between words
CODE_RE = re.compile(r"[@_{}\[\]<>=;\\|$#`~^*/]|\(\)|::|->|\.\w")
CAMEL = re.compile(r"^[a-z]+[A-Z]")
DIGIT_MIX = re.compile(r"[A-Za-z]\d|\d[A-Za-z]")
CODE_WORDS = set("""def elif endif ifdef ifndef println printf sprintf nullptr kwargs args argv argc std init func const var enum struct impl bool
boolean uint str len sizeof typedef typeof instanceof isinstance async await namespace stdin stdout stderr malloc ptr param params utf
http https www html xml json css src href img div url api sql jpg png pdf php cpp jsx tsx npm btn msg ctx cfg tmp dict usize pub mut
foreach elseif dtype numpy github localhost readonly nonatomic pragma xmlns""".split())
CODE_WORDS_BARE = {"return", "import", "class", "public", "private", "static", "void", "true", "false", "self", "null", "none", "int", "let", "new"}
CJK_WEIGHT = 2  # set from --cjk-weight


def nfkc(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


def fold(s: str) -> str:
    return STRIP.sub("", nfkc(s)).replace("’", "'").casefold()


def key(f: str) -> str:
    """concept key: fold minus a trailing 's / s"""
    return f[:-2] if f.endswith("'s") else f[:-1] if f.endswith("s") and len(f) > 1 else f


def script(s: str) -> str:
    for ch in s:
        if ch.isalpha():
            name = unicodedata.name(ch, "")
            return "LATIN" if ch.isascii() or "LATIN" in name else name.split(" ")[0].split("-")[0] or "UNKNOWN"
    return "NONE"


def letters(f: str) -> int:
    n = 0
    for ch in f:
        if ch.isalpha():
            n += CJK_WEIGHT if unicodedata.name(ch, "").startswith(WIDE) else 1
    return n


def starts_word(t: str) -> bool:
    if t[:1].isspace() or t[:1] in OPENERS:
        return True
    for ch in t:
        if ch.isalpha():
            return ch.isupper() or not ch.islower()  # a capital, or an uncased script (CJK, Arabic, Thai, ...)
    return False


def is_code(t: str, f: str) -> bool:
    s = t.strip()
    return bool(CODE_RE.search(s) or CAMEL.search(s) or DIGIT_MIX.search(s) or f in CODE_WORDS or (not t[:1].isspace() and s in CODE_WORDS_BARE))


def words_of(text: str, min_letters: int = 1) -> list[str]:
    """content words (no stopwords; a trailing 's dropped), hyphenated words also as their parts"""
    out = []
    for w in WORD.findall(nfkc(text)):
        for p in [w] + (w.split("-") if "-" in w else []):
            p = re.sub(r"['’]s$", "", p)
            if fold(p) not in STOP and HAS_LETTER.search(p) and letters(fold(p)) >= min_letters:
                out.append(p)
    return out


def keys_of(text: str) -> set[str]:
    return {key(fold(w)) for w in WORD.findall(nfkc(text))} | {key(fold(p)) for w in WORD.findall(nfkc(text)) for p in w.split("-")}


class FirstTokens:
    """the tokenizer's first token of " W" / "W" (and lowercased), decoded, kept if it has >= 3 letters"""

    def __init__(self, tok):
        self.tok, self.cache = tok, {}

    def __call__(self, w: str) -> set[str]:
        if w not in self.cache:
            out = set()
            for v in {" " + w, w, " " + w.lower(), w.lower()}:
                ids = self.tok(v, add_special_tokens=False).input_ids
                if ids:
                    s = self.tok.decode([ids[0]])
                    if letters(fold(s)) >= 3:
                        out.add(s)
            self.cache[w] = out
        return self.cache[w]


class WordIndex:
    """the word-match rule over many words at once: tag sets keyed by exact form, first token and prefix"""

    def __init__(self, first: FirstTokens):
        self.first_of, self.exact, self.first, self.prefix, self.contains = first, collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(set), []

    def add(self, w: str, tag) -> None:
        f = fold(w)
        if not f or not HAS_LETTER.search(f):
            return
        forms = {f, f + "s", f + "es", f + "'s"} | ({f[:-1] + "ies"} if f.endswith("y") else set())
        for x in forms:
            self.exact[x].add(tag)
        for s in self.first_of(w):
            self.first[s].add(tag)
        for i in range(1, len(f) + 1):
            if letters(f[:i]) >= 4:
                self.prefix[f[:i]].add(tag)
        if script(f) in NOSPACE and letters(f) >= 4:  # affixes in scripts without spaces (translated names only in practice)
            self.contains.append((f, tag))

    def lookup(self, t: str, f: str, nlet: int, sw: bool, scr: str, first: bool = True) -> set:
        if nlet <= 2:
            return set()
        out = set(self.exact.get(f, ())) | (self.first.get(t, set()) if first else set())
        if sw and nlet >= 4:
            out |= self.prefix.get(f, set())
        if scr in NOSPACE:
            out |= {tag for w, tag in self.contains if w in f}
        return out


# ---- items --------------------------------------------------------------------------------------------------------------------
def uid(i: str) -> str:  # j3:chat:v4:MP-w0-00000 -> w0-00000
    return i.split(":")[-1].split("-", 1)[1]


def load_items() -> dict:
    """v4 MP / MM, v4ctl H1 / RG (read with their MM twin's relation, vocabulary, bridge and REAL, as nn_readout), v4cc MP / MM"""
    items = {}
    for s in ("jsuite_v4_test_chat", "jsuite_v4cc_test_chat"):
        for line in (DATA / s / "items.jsonl").read_text().splitlines():
            it = json.loads(line)
            items[it["id"]] = {**it, "_set": s}
    for line in (DATA / "jsuite_v4ctl_test_chat" / "items.jsonl").read_text().splitlines():
        c = json.loads(line)
        mm = items.get(c["id"].replace(f":{c['word']}-", ":MM-"))
        if mm is not None:
            items[c["id"]] = {**c, "_set": "jsuite_v4_test_chat", "answer_vocab": mm["answer_vocab"], "relation": mm["relation"], "bridge": mm["bridge"],
                              "real": mm["real"], "steps": mm["steps"], "passage_values": mm["passage_values"], "entity_descs": mm["entity_descs"]}  # fmt: skip
    return items


class Model:
    """everything item-independent: tokenizer rules, alias groups, value and translation indexes per relation, v3 nouns"""

    def __init__(self, tok, items: dict, trans: dict):
        self.first = FirstTokens(tok)
        v3 = json.loads((ROOT / "data" / "v3_bridges.json").read_text())
        self.v3_alts = {r["bridge"]: r.get("bridge_alts") or [] for r in v3}
        self.v3_noun = {(r["bridge"], d["clause"]): d["noun"] for r in v3 if r["relation"] == "people" for d in r["descriptions"]}
        self.v3_noun_idx = {r["bridge"]: [d["noun"] for d in r["descriptions"]] for r in v3 if r["relation"] == "people"}
        aliases = collections.defaultdict(set)
        for it in items.values():
            if it["word"] in ("MP", "MM"):
                aliases[it["answer"]] |= {re.sub(r"^the ", "", a) for a in it.get("answer_aliases") or []}
        for r in v3:
            aliases[r["answer"]] |= {re.sub(r"^the ", "", a) for a in r.get("answer_aliases") or []}
        self.values = collections.defaultdict(set)
        for it in items.values():
            v = set(it["answer_vocab"]) | set(it["passage_values"].values()) | {it["real"]} | ({it["cue"]} if it.get("cue") else set())
            self.values[it["relation"]] |= v
        self.alias = {}
        for rel, vals in self.values.items():
            for v in vals:
                g = GROUP_OF.get(v)
                names = {v} | aliases.get(v, set()) | set(GROUPS.get(g, []))
                self.alias[v] = sorted(n for n in names if n)
        self.trans = {}
        for v in {v for vals in self.values.values() for v in vals}:
            g = trans["groups"].get(GROUP_OF.get(v, ""), {})
            self.trans[v] = sorted({n for part in ("territory", "language") for n in g.get(part, {}).values()})
        self.val_index, self.trans_index = {}, {}
        for rel, vals in self.values.items():
            vi, ti = WordIndex(self.first), WordIndex(self.first)
            for v in sorted(vals):
                for a in self.alias[v]:
                    vi.add(a, v)
                for n in self.trans[v]:
                    ti.add(n, v)
            self.val_index[rel], self.trans_index[rel] = vi, ti

    def noun(self, it: dict) -> str | None:
        if it["relation"] != "people":
            return None
        if it["_set"].startswith("jsuite_v4cc"):
            return CC_NOUN.get(it["bridge"])
        clause = re.split(r" (?:who|that) ", it["start_desc"], maxsplit=1)[-1]
        return self.v3_noun.get((it["bridge"], clause)) or (self.v3_noun_idx.get(it["bridge"]) or [None])[it.get("desc_index", 0) % 2]


def prompt_text(it: dict) -> str:
    return f"{it.get('context', '')}\n\n{it['question']} {INSTRUCTION}"


def person_lists(m: Model, src: dict, prompt_keys: set, desc_keys: set) -> dict:
    """REAL / BRIDGE / OCC / KNOW for the person of item src, filtered against a prompt (C1 passes another item's prompt)"""
    x = src["bridge"]
    names = {x, *src.get("bridges", []), *m.v3_alts.get(x, [])} | set(src["steps"][0].get("alts", []) if src.get("steps") else [])
    bridge = set()
    for n in names:
        for w in [n, *n.split(), *(part for word in n.split() for part in word.split("-"))]:
            f = fold(w)
            if letters(f) >= 3 and f not in STOP and key(f) not in desc_keys:
                bridge.add(w)
    occ = set()
    if (noun := m.noun(src)) is not None:
        for w in [noun, *noun.split(), *OCC_SYN.get(noun, [])]:
            if fold(w) not in STOP and key(fold(w)) not in prompt_keys:
                occ.add(w)
    others = [d for d in src["entity_descs"].get(x, []) if d != src["start_desc"]]
    know = {w for d in others for w in words_of(re.split(r" (?:who|that|where) ", d, maxsplit=1)[-1], 4) if key(fold(w)) not in prompt_keys}
    return {"REAL": src["real"], "BRIDGE": sorted(bridge), "OCC": sorted(occ), "KNOW": sorted(know)}


class Ctx:
    """one item's categories (or its C1 version: another item's person lists), with a classification cache"""

    def __init__(self, m: Model, it: dict, person: dict):
        self.m, self.rel, self.real, self.bridge = m, it["relation"], person["REAL"], it["bridge"]
        x, pv = it["bridge"], it["passage_values"]
        self.valcat = {v: "CLASS" for v in it["answer_vocab"]}
        for e in sorted(pv):
            if e != x:
                self.valcat[pv[e]] = "CTX_VAL"
        if it.get("cue"):
            self.valcat[it["cue"]] = "CUE"
        self.valcat[pv[x]] = "PV_X"
        self.valcat[person["REAL"]] = "REAL"
        self.n_class = sum(c == "CLASS" for c in self.valcat.values())
        desc, question = it["start_desc"], f"{it['question']} {INSTRUCTION}"
        dkeys = keys_of(desc)
        # the scene's names and values are categories above PASSAGE: their words ("African" of "South African") are not "other" words
        named = set().union(*(keys_of(n) for n in [*it.get("entities", []), *pv.values(), *self.valcat]))
        lists = {"BRIDGE": person["BRIDGE"], "OCC": person["OCC"], "KNOW": person["KNOW"],
                 "CTX_NAME": sorted({w for e in it.get("entities", []) if e != x for n in [e, *m.v3_alts.get(e, [])]
                                     for w in [n, *n.split(), *(part for word in n.split() for part in word.split("-"))]
                                     if letters(fold(w)) >= 3 and fold(w) not in STOP}),
                 "DESC": sorted(set(words_of(desc))),
                 "FRAME": sorted({w for w in words_of(question) if key(fold(w)) not in dkeys} | set(RELATION_WORDS)),
                 "PASSAGE": sorted({w for w in words_of(it.get("context", "")) if key(fold(w)) not in named})}  # fmt: skip
        self.lists = lists
        self.index = WordIndex(m.first)
        for cat, ws in lists.items():
            for w in ws:
                self.index.add(w, cat)
        self.has = {c: True for c in CATS}
        self.has.update({c: bool(lists[c]) for c in lists})
        self.has["CUE"] = bool(it.get("cue")) and self.valcat.get(it["cue"]) == "CUE"
        self.has["CTX_VAL"] = "CTX_VAL" in self.valcat.values()
        self.has["CLASS"] = self.n_class > 0
        self.cache = {}

    def classify(self, raw: str) -> tuple:
        """-> (category, translated, class values matched)"""
        if raw in self.cache:
            return self.cache[raw]
        t = nfkc(raw)
        f, scr = fold(t), script(t)
        if not HAS_LETTER.search(t):
            res = ("JUNK", False, ())
        elif f in STOP:
            res = ("FUNC", False, ())
        else:
            nlet, sw = letters(f), starts_word(t)
            cands = [(RANK[self.valcat[v]], v) for v in self.m.val_index[self.rel].lookup(t, f, nlet, sw, scr) if v in self.valcat]
            cands += [(RANK[c], None) for c in self.index.lookup(t, f, nlet, sw, scr)]
            tr = False
            if not cands and not is_code(t, f):
                # translated names: the full rule on non-Latin tokens; on Latin tokens (Latin-script locales) without the first-token
                # clause, whose 3-letter pieces of foreign names ("est" of "estados unidos", "ing" of "inglés") are not names
                tv = self.m.trans_index[self.rel].lookup(t, f, nlet, sw, scr, first=scr != "LATIN")
                cands = [(RANK[self.valcat[v]], v) for v in tv if v in self.valcat]
                tr = bool(cands)
            if cands:
                r = min(c[0] for c in cands)
                cat = CATS[r]
                res = (cat, tr, tuple(sorted({v for rr, v in cands if rr == r and v})) if cat == "CLASS" else ())
            elif is_code(t, f):
                res = ("CODE", False, ())
            else:
                res = ("OTHER" if scr in ("LATIN", "NONE") else "NONLATIN_OTHER", False, ())
        self.cache[raw] = res
        return res


# ---- per-item statistics ----------------------------------------------------------------------------------------------------
def item_stats(ctx: Ctx, c1: Ctx, lists: dict, win: tuple, layers: list) -> dict:
    """lists: {layer: [tokens]} for one item x site x lens x variant"""
    lo, hi = win
    wl = [la for la in layers if lo <= la <= hi and la in lists]
    assert wl, f"no dumped layer inside the window {win}"
    nan = float("nan")
    cl = {la: [ctx.classify(t) for t in lists[la]] for la in layers if la in lists}
    st = {}
    for cat in CATS:
        pres = {la: any(c[0] == cat for c in cl[la]) for la in cl}
        st[f"share/{cat}"] = sum(sum(c[0] == cat for c in cl[la]) / len(cl[la]) for la in wl) / len(wl)
        ok = ctx.has[cat]
        st[f"pres/{cat}"] = float(any(pres[la] for la in wl)) if ok else nan
        st[f"first/{cat}"] = next((la for la in wl if pres[la]), nan) if ok else nan
        st[f"firstall/{cat}"] = next((la for la in sorted(cl) if pres[la]), nan) if ok else nan
        for la in cl:
            st[f"byl/{cat}/{la}"] = float(pres[la]) if ok else nan
    for name, keep in (("TRANSLATED", lambda c, t: c[1]), ("TRANSLATED_NONLATIN", lambda c, t: c[1] and script(nfkc(t)) != "LATIN")):
        st[f"share/{name}"] = sum(sum(keep(c, t) for c, t in zip(cl[la], lists[la])) / len(cl[la]) for la in wl) / len(wl)
        st[f"pres/{name}"] = float(any(keep(c, t) for la in wl for c, t in zip(cl[la], lists[la])))
    seen = {v for la in wl for c in cl[la] if c[0] == "CLASS" for v in c[2]}
    st["classval"] = len(seen) / ctx.n_class if ctx.n_class else nan
    st["share/NL_CODE"] = st["share/NONLATIN_OTHER"] + st["share/CODE"]
    # C1: the same list scored with another item's REAL / BRIDGE / OCC / KNOW
    cc = {la: [c1.classify(t) for t in lists[la]] for la in cl}
    for cat in ("REAL",) + PERSON_CATS:
        ok = c1.has[cat] if cat != "REAL" else True
        pres = {la: any(c[0] == cat for c in cc[la]) for la in cc}
        st[f"c1share/{cat}"] = sum(sum(c[0] == cat for c in cc[la]) / len(cc[la]) for la in wl) / len(wl)
        st[f"c1pres/{cat}"] = float(any(pres[la] for la in wl)) if ok else nan
        for la in cc:
            st[f"c1byl/{cat}/{la}"] = float(pres[la]) if ok else nan
        st[f"c1diff/{cat}"] = st[f"pres/{cat}"] - st[f"c1pres/{cat}"]  # nan if either list is empty
    st["pv_minus_c1real"] = st["pres/PV_X"] - st["c1pres/REAL"]
    st["cue_minus_real"] = st["pres/CUE"] - st["pres/REAL"]
    st["pv_minus_real"] = st["pres/PV_X"] - st["pres/REAL"]
    st["share/pv_minus_real"] = st["share/PV_X"] - st["share/REAL"]
    return st


# ---- cluster bootstrap ------------------------------------------------------------------------------------------------------
_DRAWS: dict = {}


def draws(keys: tuple, B: int = 2000, seed: int = 0) -> np.ndarray:
    """multiplicity of each cluster in each of B draws (random.Random(seed).choice, as the repo's other scorers)"""
    if keys not in _DRAWS:
        rng, M = random.Random(seed), np.zeros((B, len(keys)))
        idx = list(range(len(keys)))
        for b in range(B):
            for _ in idx:
                M[b, rng.choice(idx)] += 1
        _DRAWS[keys] = M
    return _DRAWS[keys]


def ci(v: np.ndarray) -> list:
    v = np.sort(v[~np.isnan(v)])
    return [round(float(v[int(0.025 * len(v))]), 4), round(float(v[int(0.975 * len(v)) - 1]), 4)] if len(v) else [None, None]


def boot(groups: list, names: list | None = None) -> dict:
    """groups: one or two lists of (cluster, stats); one group -> means, two -> mean(A) - mean(B) (clusters resampled jointly)"""
    names = names or sorted({k for g in groups for _, s in g for k in s})
    keys = tuple(sorted({c for g in groups for c, _ in g}))
    kix = {k: i for i, k in enumerate(keys)}
    M = draws(keys)
    out_pt, out_bs = [], []
    for g in groups:
        S, C = np.zeros((len(keys), len(names))), np.zeros((len(keys), len(names)))
        for c, s in g:
            row = np.array([s.get(n, np.nan) for n in names], dtype=float)
            ok = ~np.isnan(row)
            S[kix[c], ok] += row[ok]
            C[kix[c], ok] += 1
        with np.errstate(invalid="ignore", divide="ignore"):
            out_pt.append(S.sum(0) / C.sum(0))
            out_bs.append((M @ S) / (M @ C))
    pt, bs = (out_pt[0], out_bs[0]) if len(groups) == 1 else (out_pt[0] - out_pt[1], out_bs[0] - out_bs[1])
    return {n: {"mean": None if np.isnan(pt[j]) else round(float(pt[j]), 4), "ci": ci(bs[:, j])} for j, n in enumerate(names)}


def median_gap(units: list) -> dict:
    """reading 2: on items with BRIDGE and REAL both in the window, median first layer of REAL - that of BRIDGE, with a bootstrap"""
    both = [(c, s["first/BRIDGE"], s["first/REAL"]) for c, s in units if s["first/BRIDGE"] == s["first/BRIDGE"] and s["first/REAL"] == s["first/REAL"]]
    if not both:
        return {"n": 0}
    gap = lambda us: statistics.median(r for _, _, r in us) - statistics.median(b for _, b, _ in us)  # noqa: E731
    by = collections.defaultdict(list)
    for u in both:
        by[u[0]].append(u)
    keys = sorted(by)
    rng, bs = random.Random(0), []
    for _ in range(2000):
        bs.append(gap([u for k in (rng.choice(keys) for _ in keys) for u in by[k]]))
    return {"n": len(both), "median_first_BRIDGE": statistics.median(b for _, b, _ in both), "median_first_REAL": statistics.median(r for _, _, r in both),
            "gap": gap(both), "gap_ci": ci(np.array(bs, dtype=float)),
            "median_paired_diff": statistics.median(r - b for _, b, r in both)}  # fmt: skip


def mean_of(units: list, k: str) -> float:
    xs = [s[k] for _, s in units if s.get(k) == s.get(k)]
    return sum(xs) / len(xs) if xs else float("nan")


def readings_1_4(units: list, r: dict) -> dict:
    """r: boot() over the units; readings 1-4 as the addendum words them"""
    g = lambda k: (r.get(k) or {}).get("mean")  # noqa: E731
    out = {}
    occ_d, know_d = g("c1diff/OCC"), g("c1diff/KNOW")
    a = (g("c1diff/REAL") or -1) >= 0.20
    b = (occ_d is not None and occ_d >= 0.15) or (know_d is not None and know_d >= 0.15)
    c = (g("pres/BRIDGE") or 0) < (g("pres/REAL") or 0)
    out["1_attribute_cloud"] = {"holds": a and b and c, "REAL_minus_C1": [g("c1diff/REAL"), r["c1diff/REAL"]["ci"]],
                                "OCC_minus_C1": [occ_d, r.get("c1diff/OCC", {}).get("ci")], "KNOW_minus_C1": [know_d, r.get("c1diff/KNOW", {}).get("ci")],
                                "BRIDGE_pres": g("pres/BRIDGE"), "REAL_pres": g("pres/REAL"), "parts": [a, b, c]}  # fmt: skip
    mg = median_gap(units)
    out["2_name_first"] = {"holds": mg.get("n", 0) > 0 and mg["gap"] >= 4, **mg}
    cv = g("classval") or 0
    out["3_class_priming"] = {"holds": (g("pres/REAL") or 0) < 3 * cv, "REAL_pres": g("pres/REAL"), "class_per_value_pres": cv,
                              "ratio": round((g("pres/REAL") or 0) / cv, 3) if cv else None}  # fmt: skip
    nl, tr = g("share/NL_CODE") or 0, g("share/TRANSLATED") or 0
    out["4_noise_floor"] = {"holds": nl >= 0.3 and tr < 0.05, "NONLATIN_OTHER_plus_CODE": nl, "translated": tr,
                            "translated_nonlatin": g("share/TRANSLATED_NONLATIN")}  # fmt: skip
    return out


# ---- main -------------------------------------------------------------------------------------------------------------------
def main(a) -> None:
    global CJK_WEIGHT
    CJK_WEIGHT = a.cjk_weight
    P = a.prefix
    os.environ["BJ_TARGET"] = TARGET_OF[P]
    os.environ.setdefault("HF_HOME", "/workspace/hf_cache")
    from bridge_jspace import pins, tokens  # noqa: E402  (after BJ_TARGET)

    tok = tokens.load_tokenizer()
    win = windows(P)
    runs = [Path(d) for d in a.run_dir] if a.run_dir else [RES / f"{P}nn_readout_v4ctl_v1", RES / f"{P}nn_readout_v4cc_v1"]
    runs = [r for r in runs if (r / "topk.jsonl").exists()]
    assert runs, "no topk.jsonl in the run directories"
    trans_text = Path(a.translations).read_bytes()
    trans = json.loads(trans_text)
    items = load_items()
    m = Model(tok, items, trans)

    # the dumps: lists[id][(site, lens, variant)][layer] = tokens
    lists = collections.defaultdict(lambda: collections.defaultdict(dict))
    fam, layers, tags = {}, set(), {}
    for run in runs:
        run_fams = set()
        for line in (run / "topk.jsonl").open():
            r = json.loads(line)
            for var, k in (("top", "top"), ("letters", "top_letters")):
                lists[r["id"]][(r["site"], r["lens"], var)][r["layer"]] = r[k]
            fam[r["id"]], layers = r["family"], layers | {r["layer"]}
            run_fams.add(r["family"])
        if (run / "rows.jsonl").exists() and any(f.endswith(("_conflict", "_aligned")) for f in run_fams):
            for line in (run / "rows.jsonl").open():  # note 26 (c)'s tags (known = named recall right, gated = v4_split)
                r = json.loads(line)
                if r["id"] not in tags and "known" in r:
                    tags[r["id"]] = {"known": bool(r.get("known")), "gated": r.get("gated", "")}
    layers = sorted(layers)
    missing = sorted(i for i in lists if i not in items)
    assert not missing, f"ids without item data: {missing[:5]}"

    # contexts and C1 donors (another item of the same set and relation with a different REAL)
    pool = collections.defaultdict(list)
    for i, it in sorted(items.items()):
        if it["word"] in ("MP", "MM"):
            pool[(it["_set"], it["relation"])].append(i)
    ctx, c1, donor = {}, {}, {}
    for i in sorted(lists):
        it = items[i]
        pk, dk = keys_of(prompt_text(it)), keys_of(it["start_desc"])
        ctx[i] = Ctx(m, it, person_lists(m, it, pk, dk))
        cands = [j for j in pool[(it["_set"], it["relation"])] if items[j]["real"] != it["real"] and items[j]["bridge"] != it["bridge"]]
        donor[i] = random.Random("c1:" + i).choice(cands)
        c1[i] = Ctx(m, it, person_lists(m, items[donor[i]], pk, dk))
    donor_in_scene = sum(items[donor[i]]["real"] in items[i]["passage_values"].values() for i in lists) / len(lists)

    # per-item statistics per cell
    stats = {}  # (id, site, lens, var) -> stats
    for i in sorted(lists):
        for (site, lens, var), byl in lists[i].items():
            stats[(i, site, lens, var)] = item_stats(ctx[i], c1[i], byl, win[site], layers)
    bridge = {i: items[i]["bridge"] for i in lists}
    fams = sorted(set(fam.values()))
    combos = sorted({k[1:] for k in stats})
    by_scene = collections.defaultdict(dict)
    for i, f in fam.items():
        by_scene[(items[i]["_set"], uid(i))][f] = i
    paired = [d for d in by_scene.values() if "MP_ok" in d and "MM_ok" in d]

    def units(ids, site, lens, var):
        return [(bridge[i], stats[(i, site, lens, var)]) for i in ids if (i, site, lens, var) in stats]

    out = {"prefix": P, "target": TARGET_OF[P], "tokenizer": {"repo": pins.MODEL_REPO, "revision": pins.MODEL_REVISION},
           "runs": [str(r) for r in runs], "windows": win, "layers": layers, "n_by_family": dict(collections.Counter(fam.values())),
           "n_paired_ok_scenes": len(paired), "translations": {"path": str(a.translations), "sha256": hashlib.sha256(trans_text).hexdigest(),
           "babel": trans.get("babel"), "locales": trans.get("locales")}, "cjk_weight": CJK_WEIGHT,
           "c1_donor_real_in_scene": round(donor_in_scene, 4),
           "git_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip(),
           "script_dirty": bool(subprocess.run(["git", "status", "--porcelain", "scripts/nn_topk_read.py"], capture_output=True, text=True, cwd=ROOT).stdout.strip()),
           "interpretations": ["primary pool for readings 1-4: the scenes whose MP and MM are both v4ok, both items pooled (note 25's primary set); every family beside",
                               "presence in the readings = anywhere in the window; first layers inside the window (all-layer first layers beside)",
                               "value categories (PV_X, CUE, CTX_VAL, CLASS) use the same alias groups as REAL",
                               f"Han / kana / Hangul characters count {CJK_WEIGHT} letters each; in scripts written without spaces a token containing a translated name matches it",
                               "translated names are tried on every token still unclassified after CODE (Latin-script locales included; on Latin tokens without the first-token clause); a match is flagged translated",
                               "PASSAGE leaves out the words of the scene's entity names and values (they belong to the categories above it)",
                               "starts a word = leading space, opening bracket or quote, capital first letter, or an uncased script's first letter",
                               "FRAME includes the answer instruction's words; H1 keeps the scene's passage words / values / names in their categories",
                               "reading 5: 'within +-0.10' and 'at C1's level' = bootstrap interval inside +-0.10 (note 27's convention); 'ahead' = presence difference with its interval above 0; PV_X's C1 level = C1's REAL presence",
                               "cue-conflict people have no v3 noun: OCC uses a fixed noun per person (CC_NOUN)"],
           "cells": {}, "readings": {}, "controls": {}, "descriptive": {}}  # fmt: skip

    # every family x site x lens x variant
    main_names = [f"share/{c}" for c in CATS + EXTRA] + [f"pres/{c}" for c in CATS + EXTRA] + [f"first/{c}" for c in CATS] + [f"firstall/{c}" for c in CATS]
    main_names += ["classval", "share/NL_CODE", "pv_minus_c1real", "cue_minus_real", "pv_minus_real", "share/pv_minus_real"]
    main_names += [f"c1{k}/{c}" for k in ("share", "pres", "diff") for c in ("REAL",) + PERSON_CATS]
    byl_names = [f"byl/{c}/{la}" for c in CATS for la in layers] + [f"c1byl/{c}/{la}" for c in ("REAL",) + PERSON_CATS for la in layers]
    cell_units = {}
    for f in fams + ["MPMM_ok_paired"]:
        ids = [d[w] for d in paired for w in ("MP_ok", "MM_ok")] if f == "MPMM_ok_paired" else [i for i in fam if fam[i] == f]
        for site, lens, var in combos:
            us = units(ids, site, lens, var)
            if not us:
                continue
            name = f"{f}/{site}/{lens}/{var}"
            cell_units[name] = us
            r = boot([us], main_names + byl_names)
            rec = {"n": len(us), "n_bridges": len({c for c, _ in us}), "stats": {k: v for k, v in r.items() if not k.startswith(("byl/", "c1byl/"))}}
            # presence by layer (means; the slide categories with intervals)
            rec["by_layer"] = {c: {la: r[f"byl/{c}/{la}"]["mean"] for la in layers} for c in CATS}
            rec["by_layer_c1"] = {c: {la: r[f"c1byl/{c}/{la}"]["mean"] for la in layers} for c in ("REAL",) + PERSON_CATS}
            rec["by_layer_ci"] = {c: {la: r[f"byl/{c}/{la}"]["ci"] for la in layers} for c in ("REAL", "BRIDGE", "PV_X", "OCC", "KNOW", "FRAME")}
            rec["readings_1_4"] = readings_1_4(us, r)
            out["cells"][name] = rec

    # the primary readings
    prim = "MPMM_ok_paired/desc_end/jlens/letters"
    if prim in out["cells"]:
        out["readings"] = dict(out["cells"][prim]["readings_1_4"])
        # 5: token-level priming
        r5 = {}
        for site in ("desc_end", "final"):
            us = [(bridge[d["MP_ok"]], {k: stats[(d["MP_ok"], site, "jlens", "letters")][k] - stats[(d["MM_ok"], site, "jlens", "letters")][k]
                                        for k in ("pres/REAL", "pres/PV_X", "share/REAL", "share/PV_X")}) for d in paired]  # fmt: skip
            r5[f"MP_minus_MM/{site}"] = boot([us])
        pv = boot([cell_units[prim]], ["pv_minus_c1real", "pres/PV_X", "c1pres/REAL"])
        pv_w = {w: boot([units([d[f"{w}_ok"] for d in paired], "desc_end", "jlens", "letters")], ["pv_minus_c1real"])["pv_minus_c1real"] for w in ("MP", "MM")}
        fin = boot([units([d["MP_ok"] for d in paired], "final", "jlens", "letters")], ["pv_minus_real", "pres/PV_X", "pres/REAL", "share/pv_minus_real"])
        a_ = r5["MP_minus_MM/desc_end"]["pres/REAL"]
        inside = lambda c: None not in c and -0.10 <= c[0] and c[1] <= 0.10  # noqa: E731
        p1, p2 = inside(a_["ci"]), inside(pv["pv_minus_c1real"]["ci"])
        p3 = (fin["pv_minus_real"]["mean"] or 0) > 0 and (fin["pv_minus_real"]["ci"][0] or 0) > 0
        out["readings"]["5_token_level_priming"] = {"holds": p1 and p2 and p3, "parts": [p1, p2, p3],
                                                    "REAL_pres_MP_minus_MM_desc_end": a_, "PV_X_minus_C1_REAL_desc_end": pv["pv_minus_c1real"],
                                                    "PV_X_minus_C1_by_word": pv_w, "PV_X_pres_desc_end": pv["pres/PV_X"], "C1_REAL_pres_desc_end": pv["c1pres/REAL"],
                                                    "MP_final_PV_X_minus_REAL": fin["pv_minus_real"], "MP_final_PV_X_pres": fin["pres/PV_X"],
                                                    "MP_final_REAL_pres": fin["pres/REAL"], "MP_final_share_PV_X_minus_REAL": fin["share/pv_minus_real"],
                                                    "MP_minus_MM": r5}  # fmt: skip

    # controls: C3 (H1 / RG vs MM) and C4 (MP vs MM), paired by scene; C2 is every cell's logit-lens twin
    comp = [f"pres/{c}" for c in CATS + EXTRA] + [f"share/{c}" for c in CATS + EXTRA]
    for label, (fa, fb) in {"C3_H1_minus_MM": ("H1_mmok", "MM_ok"), "C3_RG_minus_MM": ("RG_mmok", "MM_ok"), "C4_MP_minus_MM": ("MP_ok", "MM_ok"),
                            "cc_MP_minus_MM_conflict": ("MP_conflict", "MM_conflict"), "cc_MP_minus_MM_aligned": ("MP_aligned", "MM_aligned")}.items():  # fmt: skip
        sc = [d for d in by_scene.values() if fa in d and fb in d]
        for site, lens, var in combos:
            us = []
            for d in sc:
                sa, sb = stats.get((d[fa], site, lens, var)), stats.get((d[fb], site, lens, var))
                if sa and sb:
                    us.append((bridge[d[fa]], {k: sa[k] - sb[k] for k in comp}))
            if us:
                out["controls"][f"{label}/{site}/{lens}/{var}"] = {"n_scenes": len(us), **boot([us], comp)}
    out["controls"]["C2"] = "every cell is computed for lens 'logit' beside 'jlens' (cells/<family>/<site>/logit/<variant>)"
    # descriptive: success vs failure (unpaired: different scenes), cue vs REAL on conflict items
    for fa, fb in (("MM_fail", "MM_ok"), ("MP_fail", "MP_ok")):
        for site, lens, var in combos:
            ua = units([i for i in fam if fam[i] == fa], site, lens, var)
            ub = units([i for i in fam if fam[i] == fb], site, lens, var)
            if ua and ub:
                out["descriptive"][f"{fa}_minus_{fb}/{site}/{lens}/{var}"] = {"n": [len(ua), len(ub)], **boot([ua, ub], ["pres/REAL", "pres/BRIDGE", "share/REAL", "share/BRIDGE", "pres/PV_X", "pres/OCC", "pres/KNOW"])}
    for sub, keep in (("all", lambda i: True), ("known", lambda i: tags.get(i, {}).get("known")), ("gated", lambda i: tags.get(i, {}).get("gated") in ("ok", "fail"))):
        for f in ("MP_conflict", "MM_conflict", "conflict_pooled", "MP_aligned", "MM_aligned"):
            ids = [i for i in fam if (fam[i] == f or (f == "conflict_pooled" and fam[i].endswith("_conflict"))) and keep(i)]
            for site, lens, var in combos:
                us = units(ids, site, lens, var)
                if us and (sub == "all" or tags):
                    out["descriptive"][f"cue_vs_real/{sub}/{f}/{site}/{lens}/{var}"] = {"n": len(us), **boot([us], ["pres/CUE", "pres/REAL", "cue_minus_real", "share/CUE", "share/REAL"])}

    # the most frequent unmatched concepts (for the hand check), primary variant at the description end
    for f in fams:
        cnt = collections.defaultdict(collections.Counter)
        lo, hi = win["desc_end"]
        for i in (i for i in fam if fam[i] == f):
            for la, toks in lists[i][("desc_end", "jlens", "letters")].items():
                if lo <= la <= hi:
                    for t in toks:
                        c = ctx[i].classify(t)[0]
                        if c in ("OTHER", "NONLATIN_OTHER"):
                            cnt[c][key(fold(t))] += 1
        out["descriptive"][f"top_unmatched/{f}/desc_end/jlens/letters"] = {c: cnt[c].most_common(30) for c in cnt}

    od = Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    (od / f"{P}v4_n26a.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    write_csv(od / f"{P}v4_n26a_shares.csv", P, out)
    write_wall(od / f"{P}v4_n26a_wall.txt", items, fam, lists, ctx, win, layers, by_scene)
    show(out, fams)
    if a.examples:
        examples(ctx, lists, fam, a.examples)


def write_csv(path: Path, P: str, out: dict) -> None:
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["prefix", "family", "site", "lens", "variant", "n_items", "n_bridges", "category", "share", "share_lo", "share_hi", "presence", "presence_lo", "presence_hi"])
        for name, rec in out["cells"].items():
            f, site, lens, var = name.split("/")
            for c in CATS + EXTRA:
                s, p = rec["stats"][f"share/{c}"], rec["stats"][f"pres/{c}"]
                w.writerow([P, f, site, lens, var, rec["n"], rec["n_bridges"], c, s["mean"], *s["ci"], p["mean"], *p["ci"]])


def write_wall(path: Path, items, fam, lists, ctx, win, layers, by_scene) -> None:
    """the first scene per relation by id (MP and MM both in the dump), J++ letters, top-10 per layer with category tags"""
    lines = ["Token wall (prereg amendment 59 note 26 addendum): J++, letter tokens, top-10 per even layer; '*' = inside note 25's window.",
             "Tags: " + " ".join(f"{v}={k}" for k, v in TAG.items()) + "; '~' = matched through a translated name; '·' = leading space.", ""]  # fmt: skip
    first, fallback = {}, {}
    for (s, u), d in sorted(by_scene.items()):
        mp = next((d[f] for f in sorted(d) if f.startswith("MP")), None)
        mm = next((d[f] for f in sorted(d) if f.startswith("MM")), None)
        if not (mp or mm):
            continue
        rel = items[mp or mm]["relation"]
        fallback.setdefault((s, rel), (mp, mm))
        if mp and mm:
            first.setdefault((s, rel), (mp, mm))
    for k, v in fallback.items():
        first.setdefault(k, v)  # a relation with no scene that has both words: its first scene

    def cell(i, site, la):
        if not i or la not in lists[i][(site, "jlens", "letters")]:
            return ""
        out = []
        for t in lists[i][(site, "jlens", "letters")][la][:10]:
            c, tr, _ = ctx[i].classify(t)
            s = nfkc(t).replace("\n", "\\n")
            s = ("·" + s[1:]) if s[:1] == " " else s
            out.append(f"{s}/{TAG[c]}{'~' if tr else ''}")
        return " ".join(out)

    for (s, rel), (mp, mm) in sorted(first.items()):
        it = items[mp or mm]
        lines.append(f"=== {s} | {rel} | scene {uid(mp or mm)} | X = {it['bridge']} | REAL {it['real']} | PV_X {it['passage_values'][it['bridge']]}"
                     f" | MP {fam.get(mp, '-')} | MM {fam.get(mm, '-')}")  # fmt: skip
        lines.append(f"description: {it['start_desc']}")
        lines.append(f"MP: {items[mp]['question'] if mp else '-'}")
        lines.append(f"MM: {items[mm]['question'] if mm else '-'}")
        for site in ("desc_end", "final"):
            lo, hi = win[site]
            rows = [(la, cell(mp, site, la), cell(mm, site, la)) for la in layers]
            w = max([len(a) for _, a, _ in rows] + [2])
            lines.append(f"--- site {site} (window L{lo}-{hi}) ---")
            lines.append(f"      {'MP':<{w}s} || MM")
            for la, a, b in rows:
                lines.append(f"{'*' if lo <= la <= hi else ' '}L{la:<3d} {a:<{w}s} || {b}")
        lines.append("")
    path.write_text("\n".join(lines) + "\n")


def show(out: dict, fams: list) -> None:
    print(f"{out['prefix'] or '(27B)'}: windows {out['windows']}; n {out['n_by_family']}; paired ok scenes {out['n_paired_ok_scenes']}; C1 donor REAL in scene {out['c1_donor_real_in_scene']}")
    main = ["REAL", "PV_X", "CUE", "CTX_VAL", "CLASS", "BRIDGE", "CTX_NAME", "OCC", "KNOW", "DESC", "FRAME", "PASSAGE", "FUNC", "CODE", "NONLATIN_OTHER", "OTHER", "TRANSLATED"]
    for lens in ("jlens", "logit"):
        for site in ("desc_end", "final"):
            print(f"\nshare of the top-20 (%), {lens} letters, {site} window")
            print(f"{'family':16s} {'n':>4s} " + " ".join(f"{TAG.get(c, 'TR'):>4s}" for c in main))
            for f in fams + ["MPMM_ok_paired"]:
                rec = out["cells"].get(f"{f}/{site}/{lens}/letters")
                if rec:
                    print(f"{f:16s} {rec['n']:4d} " + " ".join(f"{100 * (rec['stats'][f'share/{c}']['mean'] or 0):4.1f}" for c in main))
            print("presence anywhere in the window (C1 in brackets)")
            for f in fams + ["MPMM_ok_paired"]:
                rec = out["cells"].get(f"{f}/{site}/{lens}/letters")
                if rec:
                    s = rec["stats"]
                    fmt = lambda k: "  -  " if s[k]["mean"] is None else f"{s[k]['mean']:.2f}"  # noqa: E731
                    print(f"{f:16s} REAL {fmt('pres/REAL')} ({fmt('c1pres/REAL')})  BRIDGE {fmt('pres/BRIDGE')} ({fmt('c1pres/BRIDGE')})  OCC {fmt('pres/OCC')} ({fmt('c1pres/OCC')})"
                          f"  KNOW {fmt('pres/KNOW')} ({fmt('c1pres/KNOW')})  PV_X {fmt('pres/PV_X')}  CUE {fmt('pres/CUE')}  CLASS/value {fmt('classval')}")  # fmt: skip
    print("\nreadings (primary: MPMM_ok_paired, desc_end, J++ letters):")
    for k, v in out["readings"].items():
        print(f"  {k}: holds={v['holds']}", json.dumps({kk: vv for kk, vv in v.items() if kk not in ("holds", "MP_minus_MM")}, ensure_ascii=False)[:600])


def items_x(c: Ctx) -> str:
    return f"{c.bridge}, REAL {c.real}"


def examples(ctx: dict, lists: dict, fam: dict, n: int) -> None:
    """sanity check: up to n distinct classified tokens per category (all sites, lenses, layers), with the item's X"""
    seen = collections.defaultdict(dict)
    for i in sorted(lists):
        for cellk, byl in lists[i].items():
            for toks in byl.values():
                for t in toks:
                    c, tr, cv = ctx[i].classify(t)
                    k = c + ("~" if tr else "")
                    if t not in seen[k] and len(seen[k]) < n:
                        seen[k][t] = f"{t!r}" + (f"->{'|'.join(cv)}" if cv else "") + f" [X={items_x(ctx[i])}]"
    for k in sorted(seen):
        print(f"\n{k} ({len(seen[k])}):", "  ".join(seen[k].values()))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prefix", help='run prefix: "qwen35_9b_", "" (27B), "nem35l_", "muse30_"')
    ap.add_argument("--translations", default="data/country_translations_1029.json", help="babel names, made on the VPS")
    ap.add_argument("--run-dir", action="append", default=None, help="nn_readout run dirs with topk.jsonl (default: {P}nn_readout_v4ctl_v1 and _v4cc_v1)")
    ap.add_argument("--out-dir", default=str(RES / "nn_topk_read"))
    ap.add_argument("--cjk-weight", type=int, default=2, help="letters per Han / kana / Hangul character (1 = the literal count)")
    ap.add_argument("--examples", type=int, default=0, help="print up to N classified tokens per category (sanity check)")
    main(ap.parse_args())
