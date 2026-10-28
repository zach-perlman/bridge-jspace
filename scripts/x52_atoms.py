"""x52_atoms (batch 52 part A; jobs/c3/batch52.yaml `brief:` A, Dan 29 Oct 00:30): what is inside the top-25 atoms of
the lens part? Descriptive; no rule, no prediction (the verdict writes "descriptive; no rule").

Items. E1, the main test (x0_necessity, alt cf: two people swap their picks; d1_topics_v3, chat): the locker-first
items of each model's X0 run at L (x49_gain.select_items: 49.1's and 51.10's items), N_ITEMS drawn at random (seed 0:
sorted(random.Random(0).sample(range(n), N_ITEMS))). Z2, Zach's never-named bridge (x50_zach part z2): the stored run's
chosen passages rebuilt by x51_answer.z2_items (checked id by id), N_ITEMS drawn the same way.

Δ = h_S - h_O at the edited token at L (9B L12, 27B L32, Muse L26). E1: the bridge word, from the lookup's prompts; the
lookup's and the recall's prompts agree token by token through the bridge word (asserted), so Δ is one vector for both
readers (measured beside: max |Δ_lookup - Δ_recall|) and E1 has ONE inventory per model; only the two answer classes
depend on the reader. Z2: the description's last token, per reader (K = lookup, M = recall: the passages differ before
it), so each reader has its own Δ and inventory. Sources: `atoms --delta states` (CPU, E1 only): 51.10's cached states
(results/x51_jread/<run>/states.npz, fp16, gitignored: [item, reader, O/S, P1-P3, layer, d], P1 = the bridge word), its
items matched by scene and their ids checked; `atoms --delta forward` (GPU): one forward of each O / S prompt.

Atoms: X0's lens part, recomputed: signed OMP, K = 25, over the J++ letter-token atoms at L (X0's dictionary,
JLens.vectors(L, letters): unit rows of (g * W_U[t]) J_L; letters = non-special tokens whose decode holds a letter, so
digits are never atoms), X0's fit step for step (exp04_brew_parts.signed_omp; checked against x0_necessity.fit). Per
atom: OMP rank, token id and decode, the signed coefficient of the K = 25 fit (Δ = h_S - h_O: + points to the changed
prompt), and its share of ||Δ||^2 = the rebuilt energy it adds when it enters ((||P_1..r Δ||^2 - ||P_1..r-1 Δ||^2) /
||Δ||^2: non-negative, summing to the part's share ||P_J Δ||^2 / ||Δ||^2). On the CPU the dictionary is built from the
pinned lens file (sha256 = the pin) and the pinned checkpoint's lm_head and final-norm weights (`fetch`: byte ranges of
the pinned revision's shard). Checks: the K = 25 share against X0's shares.jsonl, the answer atoms against 51.12's
norms.jsonl, the atoms against x0_atoms where the scenes overlap.

Classes (automatic, CLASSES order = priority; a token's key = its decode without spaces and edge punctuation,
lower-cased): the original bridge word (its key, plural, a word of a multi-word name, the first token of its variants
as is / leading space / capitalised / upper case; aliases: an element's symbol, a Greek letter's character) · the new
bridge word (the same) · another item named in the scene · a person's name in the scene · the reader's answer word (E1:
O's and S's answers of that reader as number word, ordinal or digit; Z2: the answer words, a word of a multi-word
answer, the first token of the full word, jsuite_v2_tables.DERIV's derived words) · the other reader's answer word
(E1; on Z2 both readers ask for the same answer, so it never fires) · a word of the bridge's semantic class not in the
scene (SAME_CLASS lists and the dataset's own entities) · function words and punctuation (FUNCTION) · other (with a
detail: another value of the answer's kind, a word of the prompt, or nothing). Hand check: 5 items per model labelled
by hand (handsheet: the atoms without the classifier's labels; labels.json written by the labeller), agreement reported.

uv run python scripts/x52_atoms.py fetch                                                    # CPU, network: 9B / 27B
BJ_TARGET=qwen3.6-27b uv run python scripts/x52_atoms.py atoms --delta states --name x52_atoms_e1_states_27b  # CPU
BJ_TARGET=muse-glimmer-30b uv run python scripts/x52_atoms.py atoms --delta forward --name muse30_x52_atoms_fwd  # GPU
uv run python scripts/x52_atoms.py handsheet                                                # CPU
uv run python scripts/x52_atoms.py report                                                   # CPU
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

EXP = "x52_atoms"
RESULTS = pins.RESULTS_DIR / EXP
CACHE = pins.REPO_ROOT / "cache" / EXP  # per target: the fetched lm_head and final-norm weights
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch52.yaml"
MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
TAGS = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse"}
STATES_RUNS = {"qwen3.5-9b": "qwen35_9b_x52_atoms_e1_states", "qwen3.6-27b": "x52_atoms_e1_states_27b"}
FWD_RUNS = {"qwen3.5-9b": "qwen35_9b_x52_atoms_fwd", "qwen3.6-27b": "x52_atoms_fwd_27b",
            "muse-glimmer-30b": "muse30_x52_atoms_fwd"}  # fmt: skip
SETS = ("e1", "z2")
SET_TEXT = {
    "e1": "the main test (E1), the bridge word",
    "z2": "Zach's never-named bridge (Z2), the description's last token",
}
N_ITEMS, SEED = 50, 0
K = X.K_MAIN  # 25
N_HAND, N_SHOW, N_TOP = 5, 10, 5  # hand-labelled items per model, printed items per model, atoms printed per item
RIDGE = 1e-8  # exp04_brew_parts.signed_omp's
VERDICT = "descriptive; no rule"
CLASSES = ("bridge", "new_bridge", "scene_item", "person", "answer_own", "answer_other", "same_class", "function",
           "other")  # fmt: skip
CLASS_TEXT = {
    "bridge": "the original bridge word",
    "new_bridge": "the new bridge word",
    "scene_item": "another item named in the scene",
    "person": "a person's name in the scene",
    "answer_own": "the reader's answer word",
    "answer_other": "the other reader's answer word",
    "same_class": "a same-class word not in the scene",
    "function": "function words and punctuation",
    "other": "other",
}
READER_NAME = {"PP": "lookup", "PM": "recall", "K": "lookup", "M": "recall"}
EDGE = re.compile(r"^[\W_]+|[\W_]+$")

# ---- word lists (fixed before any atom was classified) -------------------------------------------------------------

FUNCTION = frozenset(["a", "an", "the", "this", "that", "these", "those", "some", "any", "each", "every", "no", "all", "both", "either", "neither", "such", "what", "which", "who", "whom", "whose", "where", "when", "why", "how", "whether", "if", "then", "than", "so", "as", "because", "since", "while", "though", "although", "unless", "until", "till", "after", "before", "once", "and", "or", "but", "nor", "yet", "also", "too", "very", "just", "only", "even", "still", "again", "ever", "never", "not", "of", "in", "on", "at", "to", "for", "from", "by", "with", "without", "about", "above", "below", "over", "under", "into", "onto", "upon", "off", "out", "up", "down", "through", "across", "along", "around", "among", "between", "against", "within", "during", "per", "via", "near", "beside", "besides", "beyond", "toward", "towards", "i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "one", "ones", "am", "is", "are", "was", "were", "be", "been", "being", "do", "does", "did", "done", "doing", "have", "has", "had", "having", "will", "would", "shall", "should", "can", "could", "may", "might", "must", "ought", "here", "there", "now", "today", "s", "t", "d", "ll", "m", "re", "ve"])  # fmt: skip
NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]  # suite_v1.WORDS
ORDINALS = ["zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth"]
NUMBER_KIND = frozenset([*ORDINALS, *NUMBER_WORDS, "ten", *map(str, range(11))])
IRREGULAR_PLURAL = {"mouse": "mice", "goose": "geese", "ox": "oxen", "wolf": "wolves", "fly": "flies"}
ELEMENT_SYMBOL = {"hydrogen": "H", "helium": "He", "lithium": "Li", "carbon": "C", "nitrogen": "N", "oxygen": "O"}
GREEK_CHAR = {"alpha": "αΑ", "beta": "βΒ", "gamma": "γΓ", "delta": "δΔ", "epsilon": "εΕ", "zeta": "ζΖ", "eta": "ηΗ",
              "theta": "θΘ", "iota": "ιΙ", "kappa": "κΚ", "lambda": "λΛ", "mu": "μΜ", "nu": "νΝ", "xi": "ξΞ",
              "omicron": "οΟ", "pi": "πΠ", "rho": "ρΡ", "sigma": "σΣ", "tau": "τΤ", "upsilon": "υΥ", "phi": "φΦ",
              "chi": "χΧ", "psi": "ψΨ", "omega": "ωΩ"}  # fmt: skip
SAME_CLASS = {  # the main test's domains; the dataset's own entities are added per run
    "elements": [
        "hydrogen",
        "helium",
        "lithium",
        "beryllium",
        "boron",
        "carbon",
        "nitrogen",
        "oxygen",
        "fluorine",
        "neon",
        "sodium",
        "magnesium",
        "aluminium",
        "aluminum",
        "silicon",
        "phosphorus",
        "sulfur",
        "sulphur",
        "chlorine",
        "argon",
        "potassium",
        "calcium",
        "scandium",
        "titanium",
        "vanadium",
        "chromium",
        "manganese",
        "iron",
        "cobalt",
        "nickel",
        "copper",
        "zinc",
        "gallium",
        "germanium",
        "arsenic",
        "selenium",
        "bromine",
        "krypton",
        "rubidium",
        "strontium",
        "yttrium",
        "zirconium",
        "niobium",
        "molybdenum",
        "technetium",
        "ruthenium",
        "rhodium",
        "palladium",
        "silver",
        "cadmium",
        "indium",
        "tin",
        "antimony",
        "tellurium",
        "iodine",
        "xenon",
        "caesium",
        "cesium",
        "barium",
        "lanthanum",
        "cerium",
        "neodymium",
        "europium",
        "gadolinium",
        "tungsten",
        "platinum",
        "gold",
        "mercury",
        "lead",
        "bismuth",
        "polonium",
        "radon",
        "radium",
        "uranium",
        "plutonium",
        "thorium",
    ],
    "greek": list(GREEK_CHAR),
    "animals": [
        "ant",
        "bear",
        "bee",
        "beetle",
        "butterfly",
        "camel",
        "cat",
        "chicken",
        "cow",
        "crow",
        "deer",
        "dog",
        "duck",
        "eagle",
        "elephant",
        "fly",
        "fox",
        "frog",
        "goat",
        "goose",
        "horse",
        "lion",
        "mouse",
        "owl",
        "pig",
        "rabbit",
        "sheep",
        "spider",
        "tick",
        "tiger",
        "turkey",
        "wolf",
        "ape",
        "bat",
        "bird",
        "boar",
        "buffalo",
        "bull",
        "calf",
        "cheetah",
        "chimpanzee",
        "cobra",
        "crab",
        "crocodile",
        "dolphin",
        "donkey",
        "dove",
        "dragonfly",
        "falcon",
        "ferret",
        "fish",
        "flamingo",
        "gecko",
        "giraffe",
        "gorilla",
        "grasshopper",
        "hamster",
        "hare",
        "hawk",
        "hedgehog",
        "hen",
        "hippo",
        "hippopotamus",
        "hornet",
        "hyena",
        "insect",
        "jaguar",
        "kangaroo",
        "koala",
        "leopard",
        "lizard",
        "lobster",
        "llama",
        "mole",
        "monkey",
        "moose",
        "mosquito",
        "moth",
        "mule",
        "octopus",
        "ostrich",
        "otter",
        "ox",
        "panda",
        "panther",
        "parrot",
        "peacock",
        "pelican",
        "penguin",
        "pigeon",
        "pony",
        "puppy",
        "raccoon",
        "rat",
        "raven",
        "reindeer",
        "rhino",
        "rhinoceros",
        "rooster",
        "salmon",
        "scorpion",
        "seal",
        "shark",
        "shrimp",
        "snail",
        "snake",
        "sparrow",
        "squid",
        "squirrel",
        "swan",
        "termite",
        "toad",
        "tortoise",
        "trout",
        "turtle",
        "wasp",
        "whale",
        "worm",
        "zebra",
        "kitten",
        "lamb",
        "chick",
        "cattle",
    ],
}
TRANSLATION = {  # Chinese names of the main test's entities (the Qwens read Chinese): matched as whole tokens only
    "ant": "蚂蚁 蚁", "bear": "熊", "bee": "蜜蜂 蜂", "beetle": "甲虫", "butterfly": "蝴蝶 蝶", "camel": "骆驼",
    "cat": "猫 小猫 猫咪", "chicken": "鸡 小鸡", "cow": "牛 奶牛", "crow": "乌鸦 鸦", "deer": "鹿", "dog": "狗 犬 小狗",
    "duck": "鸭 鸭子", "eagle": "鹰 老鹰", "elephant": "大象 象", "fly": "苍蝇 蝇", "fox": "狐狸 狐", "frog": "青蛙 蛙",
    "goat": "山羊", "goose": "鹅", "horse": "马", "lion": "狮子 狮", "mouse": "老鼠 鼠", "owl": "猫头鹰", "pig": "猪",
    "rabbit": "兔子 兔", "sheep": "羊 绵羊", "spider": "蜘蛛", "tick": "蜱 蜱虫", "tiger": "老虎 虎", "turkey": "火鸡",
    "wolf": "狼", "hydrogen": "氢 氢气", "helium": "氦 氦气", "lithium": "锂", "carbon": "碳", "nitrogen": "氮 氮气",
    "oxygen": "氧 氧气", "alpha": "阿尔法", "beta": "贝塔", "gamma": "伽马", "delta": "德尔塔", "epsilon": "艾普西隆",
    "eta": "伊塔", "theta": "西塔", "iota": "约塔",
}  # fmt: skip
SYMBOL_DROPPED = {"helium"}  # "He" is far more often the pronoun than helium's symbol: no alias
MIN_PIECE = 3  # the first token of a word the tokenizer splits counts only with a key of >= 3 characters
LOCKER = re.compile(r"[Tt]he locker of (?:the )?([\w-]+) is")
PICKED = re.compile(r"\b([A-Z][a-z]+) picked (?:the )?([\w-]+)\.")
ASKED = re.compile(r"\b([A-Z][a-z]+)'s pick")


# ---- the classifier (CPU-testable) ---------------------------------------------------------------------------------


def key_of(token: str) -> str:
    """A token's key: its decode without surrounding spaces and edge punctuation, lower-cased (' Oxygen.' -> 'oxygen')."""
    return EDGE.sub("", token.strip()).lower()


def word_keys(name: str) -> set[str]:
    """The keys of a name: the name, its plural, and each word of >= 3 letters of a multi-word name (article and
    function words aside)."""
    n = name.strip().lower()
    n = n[4:] if n.startswith("the ") else n
    out = {n, n + "s", n + "es"} | ({n[:-1] + "ies"} if n.endswith("y") else set())
    out |= {IRREGULAR_PLURAL[n]} if n in IRREGULAR_PLURAL else set()
    words = re.findall(r"[^\W\d_]+", n)
    if len(words) > 1:
        out |= {w for w in words if len(w) >= 3 and w not in FUNCTION}
    return out


def first_pieces(tok, names: list[str]) -> set[int]:
    """The first token of each name's variants (as is, leading space, capitalised, upper case, each with a leading
    space) where the tokenizer splits the variant and that first token's key has >= MIN_PIECE characters."""
    out = set()
    for n in names:
        n = n[4:] if n.startswith("the ") else n
        for v in dict.fromkeys((n, n[:1].upper() + n[1:], n.upper())):
            for s in (v, " " + v):
                ids = tok.encode(s, add_special_tokens=False)
                if len(ids) > 1 and len(key_of(tok.decode([ids[0]]))) >= MIN_PIECE:
                    out.add(int(ids[0]))
    return out


def matcher(keys=(), ids=(), alias=(), spell=()) -> dict:
    """What a class matches: token keys, token ids (first pieces of split words), exact aliases (symbols) and, for the
    two bridge words only, spellings (names whose prefix, initial or inner part a token may be)."""
    return {"keys": set(keys), "ids": {int(i) for i in ids}, "alias": set(alias), "spell": set(spell)}


def entity_matcher(tok, names: list[str], domain: str | None, alts: dict[str, list[str]] | None = None,
                   spell: bool = False) -> dict:  # fmt: skip
    """An entity class (bridge, new bridge, scene item, same class): every name's keys, ALT names, first pieces of split
    names, by domain aliases (an element's symbol, a Greek letter's characters) and, with spell (the bridge words),
    the names' letters for prefix / initial / part matches (match)."""
    full = [a for n in names for a in (n, *((alts or {}).get(n, [])))]
    keys = set().union(*(word_keys(n) for n in full)) if full else set()
    alias: set[str] = set()
    for n in names:
        if domain == "elements" and n.lower() in ELEMENT_SYMBOL and n.lower() not in SYMBOL_DROPPED:
            alias.add(ELEMENT_SYMBOL[n.lower()])
        if domain == "greek" and n.lower() in GREEK_CHAR:
            alias |= set(GREEK_CHAR[n.lower()])
        alias |= set(TRANSLATION.get(n.lower(), "").split())
    letters = {"".join(re.findall(r"[^\W\d_]+", n.lower().removeprefix("the "))) for n in full} if spell else set()
    return matcher(keys, first_pieces(tok, full), alias, letters - {""})


def number_matcher(answers: list[str]) -> dict:
    """A reader's answers on E1 (single digits): the number word, the ordinal and the digit."""
    keys = set()
    for a in answers:
        d = int(str(a).strip())
        keys |= {NUMBER_WORDS[d], ORDINALS[d], str(d)}
    return matcher(keys)


def word_answer_matcher(tok, answers: list[str]) -> dict:
    """A reader's answers on Z2 (words): each answer's keys, its DERIV words (France -> French) and first pieces."""
    from scripts import jsuite_v2_tables as TB

    words = [w for a in answers for w in (a, *TB.DERIV.get(a, []))]
    return matcher(set().union(*(word_keys(w) for w in words)), first_pieces(tok, list(answers)))


def match(token: str, tid: int, m: dict) -> str | None:
    """How a token matches a class, or None: 'key' (the word, a plural or a word of the name), 'first token' (of a
    split word), 'alias' (a symbol); for the bridge words also their spelling: 'prefix' (a key of >= 2 letters that
    starts the name: ' oxy', 'FR', ' HEL'), 'initial' (a one-letter key, the name's first letter: '/H', '(N') and
    'part' (a key of >= 3 letters inside the name: 'amma'); 'initial' also takes the first letter doubled or tripled
    (' HH', ' CC'). Aliases are a symbol, a Greek letter's character or a Chinese name (TRANSLATION), as whole
    tokens."""
    k = key_of(token)
    if k in m["keys"]:
        return "key"
    if int(tid) in m["ids"]:
        return "first token"
    if token.strip() in m["alias"] or k in m["alias"]:
        return "alias"
    if k.isalpha():
        for n in m.get("spell", ()):
            if len(k) >= 2 and n.startswith(k) and k != n and len(set(k)) > 1:
                return "prefix"
            if len(k) <= 3 and len(set(k)) == 1 and n[0] == k[0]:
                return "initial"
            if len(k) >= 3 and k in n:
                return "part"
    return None


def classify(token: str, tid: int, ctx: dict) -> tuple[str, str, str]:
    """(class, how it matched, detail) of one atom in one item and reader view; the first class in CLASSES order that
    matches. Detail (other only): 'answer kind' (another value of the answer's kind: a number word on E1, an answer of
    the relation on Z2), 'in the prompt' (a word of the reader's prompt) or ''."""
    for c in CLASSES[:-2]:
        via = match(token, tid, ctx[c])
        if via:
            return c, via, ""
    k = key_of(token)
    if k in FUNCTION or not k:
        return "function", "key", ""
    detail = "answer kind" if k in ctx["answer_kind"] else "in the prompt" if k in ctx["prompt_keys"] else ""
    return "other", "", detail


def prompt_keys(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[^\W\d_]+", text)}


def e1_scene(it: dict) -> dict:
    """The main-test item's words: bridges, the other items and the people of both contexts, each reader's O / S
    answers, the domain and the prompt text (context and both questions)."""
    texts = (it["context"], it["cf_context"])
    items = {m.group(1) for t in texts for m in LOCKER.finditer(t)} | {
        m.group(2) for t in texts for m in PICKED.finditer(t)
    }
    persons = {m.group(1) for t in texts for m in PICKED.finditer(t)}
    persons |= {m.group(1) for rd in it["readers"].values() for m in ASKED.finditer(rd["question"])}
    return {"bridge": it["entity"], "new": it["cf_bridge"], "items": sorted(items - {it["entity"], it["cf_bridge"]}),
            "persons": sorted(persons), "domain": it["domain"],
            "answers": {w: [rd["answer"], rd["cf_answer"]] for w, rd in it["readers"].items()},
            "text": " ".join([it["context"], *(rd["question"] for rd in it["readers"].values())])}  # fmt: skip


def e1_context(tok, sc: dict, reader: str, vocab: dict[str, set[str]]) -> dict:
    """The classifier's context for one main-test item in one reader's view (reader PP or PM; the other reader's
    answers are 'answer_other')."""
    other = next(w for w in sc["answers"] if w != reader)
    in_scene = {sc["bridge"], sc["new"], *sc["items"]}
    dom = sc["domain"]
    return {"bridge": entity_matcher(tok, [sc["bridge"]], dom, spell=True),
            "new_bridge": entity_matcher(tok, [sc["new"]], dom, spell=True),
            "scene_item": entity_matcher(tok, sc["items"], dom), "person": matcher(word_keys_all(sc["persons"])),
            "answer_own": number_matcher(sc["answers"][reader]), "answer_other": number_matcher(sc["answers"][other]),
            "same_class": entity_matcher(tok, sorted(vocab[dom] - in_scene), dom), "answer_kind": NUMBER_KIND,
            "prompt_keys": prompt_keys(sc["text"])}  # fmt: skip


def word_keys_all(names) -> set[str]:
    return set().union(*(word_keys(n) for n in names)) if names else set()


def relation_of(key: str) -> str:
    """Z2's relation from the item key '<set>|j2:<relation>:<...>'."""
    return key.split("|", 1)[1].split(":")[1]


def mentioned(names, text: str) -> list[str]:
    """The names (article aside) that occur in the text as whole words, case-insensitive."""
    low = text.lower()
    out = []
    for n in names:
        core = n[4:] if n.startswith("the ") else n
        if re.search(r"(?<![^\W_])" + re.escape(core.lower()) + r"(?![^\W_])", low):
            out.append(n)
    return sorted(out)


def z2_scene(it: dict, reader: str, text: str) -> dict:
    """Zach's passage as one reader reads it (text: its O prompt, decoded): bridges, the relation's entities named in
    it, the people (his named people, natural_v1.PEOPLE_NAMES, first and last names; names in his WikiText filler are
    not recognised and fall to 'other'), the reader's O / S answers."""
    from scripts import jsuite_v2_tables as TB
    from scripts import natural_v1 as NV

    rel = relation_of(it["key"])
    facts = TB.REL2[rel]["facts"]
    bridges = {it["entity"], it["cf_entity"]}
    items = [n for n in mentioned(facts, text) if n not in bridges]
    people = [p for p in NV.PEOPLE_NAMES if re.search(rf"\b({p.split()[0]}|{p.split()[-1]})\b", text)]
    rd = it["readers"][reader]
    return {"bridge": it["entity"], "new": it["cf_entity"], "items": items, "relation": rel,
            "persons": sorted({w for p in people for w in p.split()}), "answers": [rd["answer"], rd["cf_answer"]],
            "text": text}  # fmt: skip


def z2_context(tok, sc: dict) -> dict:
    """The classifier's context for one Z2 passage and reader (both readers ask for the same answer, so the other
    reader's answer class is empty)."""
    from scripts import jsuite_v2_tables as TB

    rel = sc["relation"]
    alts = TB.ALT.get(rel, {})
    dom = "animals" if rel == "animals" else None
    same = (set(TB.REL2[rel]["facts"]) | (set(SAME_CLASS["animals"]) if dom else set())) - {
        sc["bridge"],
        sc["new"],
        *sc["items"],
    }
    kind = word_keys_all([*TB.vocab(rel), *(d for a in TB.vocab(rel) for d in TB.DERIV.get(a, []))])
    return {"bridge": entity_matcher(tok, [sc["bridge"]], dom, alts, spell=True),
            "new_bridge": entity_matcher(tok, [sc["new"]], dom, alts, spell=True),
            "scene_item": entity_matcher(tok, sc["items"], dom, alts), "person": matcher(word_keys_all(sc["persons"])),
            "answer_own": word_answer_matcher(tok, sc["answers"]), "answer_other": matcher(),
            "same_class": entity_matcher(tok, sorted(same), dom, alts), "answer_kind": kind,
            "prompt_keys": prompt_keys(sc["text"])}  # fmt: skip


# ---- items (tokenizer and stored runs only) -------------------------------------------------------------------------


def pick(n: int, k: int = N_ITEMS, seed: int = SEED) -> list[int]:
    """k random indices of n, sorted (seed 0)."""
    return sorted(random.Random(seed).sample(range(n), min(k, n)))


def layer_of(target: str) -> int:
    """L: X0's layer; Zach's Z2 run uses the same one first (asserted)."""
    from scripts import x50_zach as Z

    assert Z.LAYERS[target][0] == X.PREDICTED[target], f"{target}: Z2's layer {Z.LAYERS[target]} is not X0's"
    return X.PREDICTED[target]


def e1_items(tok, target: str) -> tuple[list[dict], dict]:
    """N_ITEMS random locker-first main-test items of the target's X0 run at L (x49_gain.select_items, seed 0); the
    lookup's and the recall's prompts asserted equal through the bridge word."""
    from scripts import x49_gain as G

    pool, counts = G.select_items(tok, target)
    idx = pick(len(pool))
    items = []
    for i in idx:
        it = {**pool[i], "key": pool[i]["scene"]}
        p = it["pos"]
        for v in ("org", "alt"):
            a, b = it["readers"][X.LOOKUP]["ids"][v], it["readers"][X.RECALL]["ids"][v]
            assert a[: p + 1] == b[: p + 1], f"{it['scene']}: the readers' {v} prompts differ before the bridge word"
        items.append(it)
    return items, {**counts, "pool": len(pool), "picked": idx}


def z2_items(tok, target: str) -> tuple[list[dict], dict]:
    """N_ITEMS random passages of Zach's Z2 run at L (x51_answer.z2_items: rebuilt and checked id by id; seed 0)."""
    from scripts import x51_answer as A

    pool, gate, counts = A.z2_items(tok, target)
    assert gate["pass"], f"{target}: Z2's gate did not pass ({gate})"
    idx = pick(len(pool))
    return [pool[i] for i in idx], {**counts, "gate": gate, "pool": len(pool), "picked": idx}


def scenes_of(set_name: str, it: dict, decode) -> dict[str, dict]:
    """Per reader view, the words the classifier needs (E1: one scene, two views; Z2: each reader's own passage)."""
    if set_name == "e1":
        sc = e1_scene(it)
        return {w: sc for w in X.READERS}
    return {w: z2_scene(it, w, decode(rd["ids"]["org"])) for w, rd in it["readers"].items()}


# ---- the lens part's atoms -----------------------------------------------------------------------------------------


def omp_atoms(dic, x, k: int = K):
    """exp04_brew_parts.signed_omp step for step (greedy |correlation| with the residual, least-squares refit with a
    RIDGE ridge), keeping what it drops: the chosen atom indices [m, k] in order, the coefficients of the final fit [m,
    k] (float64), each atom's share of ||x||^2 when it entered (the rebuilt energy it added) [m, k] and the
    approximation [m, d] (float32, signed_omp's return value)."""
    import torch

    m = x.shape[0]
    x = x.float()
    chosen = torch.empty(m, 0, dtype=torch.long, device=x.device)
    approx = torch.zeros_like(x)
    rows = torch.arange(m, device=x.device)
    sq = x.double().norm(dim=-1) ** 2
    energy = [torch.zeros(m, dtype=torch.float64, device=x.device)]
    coefs = torch.zeros(m, 0, dtype=torch.float64, device=x.device)
    for _ in range(k):
        scores = ((x - approx) @ dic.T).abs()
        scores[rows[:, None], chosen] = -1.0
        chosen = torch.cat([chosen, scores.argmax(dim=1, keepdim=True)], dim=1)
        atoms = dic[chosen].double()
        gram = atoms @ atoms.transpose(1, 2)
        rhs = (atoms @ x.double().unsqueeze(2)).squeeze(2)
        eye = torch.eye(gram.shape[1], dtype=gram.dtype, device=gram.device)
        coefs = torch.linalg.solve(gram + RIDGE * eye, rhs)
        full = (coefs.unsqueeze(1) @ atoms).squeeze(1)
        approx = full.float()
        energy.append(full.norm(dim=-1) ** 2)
    gains = torch.stack([energy[i + 1] - energy[i] for i in range(k)], dim=1) / sq.clamp_min(1e-30)[:, None]
    return chosen, coefs, gains, approx


def lens_path(target: str) -> Path:
    """The target's pinned J++ lens file from the HF cache, its sha256 checked against the pin (fetched by `fetch`)."""
    from huggingface_hub import hf_hub_download

    t = pins.TARGETS[target]
    repo, file, rev = t["lenses"]["jpp"]
    assert repo != "local", f"{target}: its lens is a local file on the boxes (GPU stage only)"
    path = Path(hf_hub_download(repo, file, revision=rev, local_files_only=True))
    want = t.get("frozen_lens_sha256", pins.FROZEN_LENS_SHA256)
    assert pins.sha256_file(path) == want, f"{path} is not {target}'s pinned J++ lens"
    return path


def letter_ids(tok, vocab: int) -> tuple[list[int], list[str]]:
    """model.letter_token_ids() without the model: non-special ids of the lm_head's vocabulary whose decode holds a
    letter, and every decode."""
    from bridge_jspace.model import _HAS_LETTER

    decoded = tok.batch_decode([[i] for i in range(vocab)])
    special = frozenset(tok.all_special_ids) | frozenset(int(i) for i in tok.added_tokens_decoder)
    return [i for i, s in enumerate(decoded) if i not in special and _HAS_LETTER.search(s)], decoded


def cpu_dictionary(tok, target: str, layer: int, chunk: int = 16384):
    """X0's J++ letter dictionary at L on the CPU: unit rows of (g * W_U[letters]) J_L (JLens.vectors' arithmetic, fp32),
    from the fetched lm_head / final-norm weights and the pinned lens file. Returns (letter ids, dictionary, decodes)."""
    import torch
    from safetensors.torch import load_file

    head = load_file(str(CACHE / target / "head.safetensors"))
    w_u, g = head["lm_head.weight"], head["norm.weight"].float()
    gain = 1.0 + g if pins.TARGETS[target]["norm_gain"] == "one_plus_weight" else g
    blob = torch.load(lens_path(target), map_location="cpu", weights_only=True, mmap=True)
    jl = blob["J"][layer].to(torch.float32)
    letters, decoded = letter_ids(tok, w_u.shape[0])
    lt = torch.tensor(letters)
    out = torch.empty(len(letters), w_u.shape[1])
    with torch.no_grad():
        for s in range(0, len(letters), chunk):
            rows = (w_u[lt[s : s + chunk]].float() * gain) @ jl
            out[s : s + chunk] = torch.nn.functional.normalize(rows, dim=-1)
    return lt, out, decoded


# ---- Δ -------------------------------------------------------------------------------------------------------------


def states_deltas(items: list[dict], target: str, layer: int, root: Path) -> tuple[dict[str, np.ndarray], dict]:
    """E1's Δ from 51.10's cached states (P1 = the bridge word, the lookup's O and S at L), the items matched by scene
    and checked (ids of both readers and variants, the bridge position); beside, the recall's Δ from its own forwards
    (identical prompts through the bridge word): max |Δ_lookup - Δ_recall|."""
    from scripts import x51_jread as JR

    src = Path(root) / JR.RUNS[target]
    cases = X.read_jsonl(src / "cases.jsonl")
    row = {c["scene"]: i for i, c in enumerate(cases)}
    z = np.load(src / JR.STATES_FILE)
    layers = [int(x) for x in z["layers"]]
    li, p1 = layers.index(layer), JR.POS.index("P1")
    idx = []
    for it in items:
        c = cases[row[it["scene"]]]
        assert c["pos"] == it["pos"], f"{it['scene']}: the bridge position differs from {src.name}'s"
        for w in X.READERS:
            assert c["readers"][w]["ids"] == it["readers"][w]["ids"], (
                f"{it['scene']}: {w}'s ids differ from {src.name}'s"
            )
        idx.append(row[it["scene"]])
    h = z["h"][idx][:, :, :, p1, li].astype(np.float32)  # [n, reader, O/S, d]
    out = {X.LOOKUP: h[:, 0, 1] - h[:, 0, 0], X.RECALL: h[:, 1, 1] - h[:, 1, 0]}
    checks = {"states": str(src / JR.STATES_FILE), "states_layers": layers, "rows": idx, **reader_gap(out)}
    return out, checks


def reader_gap(d: dict[str, np.ndarray]) -> dict[str, float]:
    """How far the recall's Δ (its own forwards) is from the lookup's, which should agree through the bridge word."""
    lk, rc = d[X.LOOKUP], d[X.RECALL]
    rel = np.linalg.norm(lk - rc, axis=1) / np.maximum(np.linalg.norm(lk, axis=1), 1e-30)
    return {"max_abs_delta_lookup_minus_recall": float(np.abs(lk - rc).max()), "max_abs_delta": float(np.abs(lk).max()),
            "max_rel_norm_lookup_minus_recall": float(rel.max()), "median_rel_norm_lookup_minus_recall": float(np.median(rel))}  # fmt: skip


def forward_deltas(model, set_name: str, items: list[dict], layer: int) -> tuple[dict[str, np.ndarray], dict]:
    """Δ at L from one forward of each O / S prompt: E1 from the lookup's prompts (the recall's too, for the identity
    check), Z2 per reader at its own edited token."""
    import torch

    from bridge_jspace.utils import progress

    dev = model.device
    per: dict[str, list] = collections.defaultdict(list)
    with torch.no_grad():
        for it in progress(items, f"x52 {set_name}: Δ at L{layer} (item)"):
            for w, rd in it["readers"].items():
                pos = it["pos"] if set_name == "e1" else rd["pos"]
                h = {v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=(layer,))[1][layer][pos].float().cpu()
                     for v in ("org", "alt")}  # fmt: skip
                per[w].append((h["alt"] - h["org"]).numpy())
    out = {w: np.stack(v) for w, v in per.items()}
    return out, (reader_gap(out) if set_name == "e1" else {})


# ---- stored-run checks (CPU) ---------------------------------------------------------------------------------------


def x0_shares(target: str, layer: int) -> dict[str, float]:
    """X0's stored K = 25 J++ share of ||Δ||^2 per scene at L (the source run's shares.jsonl)."""
    from scripts import x45b_binding as B

    src = X.RESULTS / B.MAIN_RUN[target]
    return {r["scene"]: r["share"] for r in X.read_jsonl(src / "shares.jsonl")
            if r["rendering"] == "chat" and r["layer"] == layer and (r["dict"], r["k"], r["omp"]) == X.MAIN}  # fmt: skip


def answer_atoms_51(target: str, set_name: str) -> dict[tuple[str, str], tuple[list[int], list[int]]]:
    """51.12's answer tokens A and those among Δ's 25 (norms.jsonl), keyed (item key, Δ's reader), where its run
    exists."""
    from scripts import x51_answer as A

    run = A.RUNS.get(set_name, {}).get(target)
    path = A.RESULTS / run / "norms.jsonl" if run else None
    if not path or not path.exists():
        return {}
    return {(r["key"], r["source"]): ([int(t) for t in r["A_ids"]], [int(t) for t in r["answer_atoms_in_25"]])
            for r in X.read_jsonl(path)}  # fmt: skip


def x0_atom_sets(target: str, layer: int) -> dict[str, list[int]]:
    """x0_atoms' K = 25 picks per scene, where a stored run fits the target's X0 run, layer and letter dictionary."""
    from scripts import x51_answer as A

    _, out = A.stored_atoms("e1", target)
    return out


# ---- the atoms stage -----------------------------------------------------------------------------------------------


def manifest(name: str, target: str, layer: int, delta: str, sets: dict[str, dict], extra: dict) -> dict:
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state

    return {"exp": EXP, "run": name, "part": "52 A", "spec": "jobs/c3/batch52.yaml (brief, part A)",
            "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
            "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "k": K,
            "omp": "signed (exp04_brew_parts.signed_omp step for step; checked against x0_necessity.fit)",
            "dictionary": "J++ letter-token atoms at L (JLens.vectors(L, letters), unit rows)",
            "delta": {"states": "51.10's cached states (fp16), E1 only", "forward": "one forward of each O / S prompt"}[delta],
            "share": "per atom: the rebuilt energy it adds when it enters, / ||Δ||^2 (non-negative; sums to the part's share)",
            "sets": {s: {"text": SET_TEXT[s], **{k: v for k, v in c.items() if k != "picked"}, "picked": c["picked"]}
                     for s, c in sets.items()},
            "seeds": {"items": SEED}, "n_items": N_ITEMS, "inputs": {str(p.relative_to(pins.REPO_ROOT)): pins.sha256_file(p)
                                                                       for p in (SPEC,) if p.exists()},
            "verdict": VERDICT, **extra}  # fmt: skip


def stage_atoms(name: str, delta: str, sets: tuple[str, ...], states_root: Path | None = None) -> Path:
    """The lens part's 25 atoms per item (and reader where Δ differs) into results/x52_atoms/<name>/: manifest.json
    (before any model work), items.jsonl (each item's words per reader view), atoms.jsonl, deltas.npz, checks.json."""
    import torch

    pins.check_run_name(name)
    target, layer = pins.TARGET, layer_of(pins.TARGET)
    assert delta == "forward" or sets == ("e1",), "cached states hold E1 only: --delta states needs --sets e1"
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    tok = load_tokenizer_cpu(target)
    built = {s: (e1_items if s == "e1" else z2_items)(tok, target) for s in sets}
    m = manifest(name, target, layer, delta, {s: c for s, (_, c) in built.items()},
                 {"states_root": str(states_root) if states_root else None})  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    X.write_jsonl(out / "items.jsonl", [{"set": s, "key": it["key"], "entity": it["entity"],
                                         "cf_entity": it.get("cf_bridge", it.get("cf_entity")),
                                         "views": scenes_of(s, it, decode)}
                                        for s, (items, _) in built.items() for it in items])  # fmt: skip
    deltas: dict[str, dict[str, np.ndarray]] = {}
    checks: dict[str, Any] = {"target": target, "layer": layer}
    if delta == "forward":
        from bridge_jspace.lens import JLens
        from bridge_jspace.model import load_model

        model = load_model()
        lens = JLens(model, "jpp")
        assert layer in lens.source_layers, f"the J++ lens has no map at L{layer}"
        for s in sets:
            deltas[s], checks[f"{s}_delta"] = forward_deltas(model, s, built[s][0], layer)
        letters = model.letter_token_ids()
        dic = lens.vectors(layer, letters)
        decoded = model.decoded
        dev = model.device
    else:
        deltas["e1"], checks["e1_delta"] = states_deltas(built["e1"][0], target, layer, Path(states_root))
        letters, dic, decoded = cpu_dictionary(tok, target, layer)
        dev = torch.device("cpu")
    checks["letters"] = len(letters)
    np.savez(
        out / "deltas.npz", **{f"{s}_{w}": v.astype(np.float32) for s, per in deltas.items() for w, v in per.items()}
    )
    lt = letters.tolist()
    rows = []
    for s in sets:
        items = built[s][0]
        shares = x0_shares(target, layer) if s == "e1" else {}
        a51 = answer_atoms_51(target, s)
        x0a = x0_atom_sets(target, layer) if s == "e1" else {}
        gaps, a51_agree, a51_n, x0_agree, x0_n = [], 0, 0, 0, 0
        picks: dict[str, list[set[int]]] = {}
        for w, arr in deltas[s].items():
            x = torch.tensor(arr, device=dev)
            chosen, coefs, gains, approx = omp_atoms(dic, x, K)
            picks[w] = [{lt[j] for j in row} for row in chosen.tolist()]
            if s == "e1" and w != X.LOOKUP:  # E1's inventory is the lookup's Δ; the recall's is a check only
                continue
            ref = X.fit(dic, x, K, "signed")
            checks[f"{s}_{w}_fit_max_abs_diff"] = float((approx - ref).abs().max())
            sq = (x.double().norm(dim=-1) ** 2).cpu()
            share = ((approx.double().norm(dim=-1) ** 2).cpu() / sq).tolist()
            for i, it in enumerate(items):
                ids = [lt[j] for j in chosen[i].tolist()]
                rec = {"set": s, "key": it["key"], "reader": w, "entity": it["entity"],
                       "cf_entity": it.get("cf_bridge", it.get("cf_entity")), "norm": round(float(sq[i] ** 0.5), 4),
                       "share_k25": round(share[i], 6), "x0_share_k25": shares.get(it["key"]),
                       "atoms": [{"rank": r + 1, "token_id": t, "token": decoded[t], "coef": round(float(coefs[i, r]), 5),
                                  "share": round(float(gains[i, r]), 6)} for r, t in enumerate(ids)]}  # fmt: skip
                if rec["x0_share_k25"] is not None:
                    gaps.append(abs(rec["share_k25"] - rec["x0_share_k25"]))
                if (it["key"], w) in a51:
                    a_ids, theirs = a51[(it["key"], w)]
                    a51_n += 1
                    a51_agree += int(set(ids) & set(a_ids) == set(theirs))
                    rec["answer_atoms_51_12"] = theirs
                if it["key"] in x0a:
                    x0_n += 1
                    x0_agree += int(set(ids) == set(x0a[it["key"]]))
                rows.append(rec)
        checks[f"{s}_x0_share_max_abs_gap"] = max(gaps) if gaps else None
        checks[f"{s}_x0_share_items"] = len(gaps)
        checks[f"{s}_51_12_answer_atoms_items_agree"] = [a51_agree, a51_n]
        checks[f"{s}_x0_atoms_same_25_items"] = [x0_agree, x0_n]
        if s == "e1" and X.RECALL in picks:
            same = [len(a & b) for a, b in zip(picks[X.LOOKUP], picks[X.RECALL], strict=True)]
            checks["e1_recall_delta_atoms_in_common"] = {"all_25": sum(n == K for n in same), "items": len(same),
                                                          "min": min(same), "median": float(np.median(same))}  # fmt: skip
    X.write_jsonl(out / "atoms.jsonl", rows)
    (out / "checks.json").write_text(json.dumps(checks, indent=1) + "\n")
    print(json.dumps(checks, indent=1), flush=True)
    print(f"wrote {out}: {len(rows)} atom lists", flush=True)
    return out


def load_tokenizer_cpu(target: str):
    """The target's tokenizer from the local HF cache (x45m.tokenizer: the run's loader, its chat-template edits)."""
    from scripts import x45m

    assert target == pins.TARGET, f"BJ_TARGET is {pins.TARGET}, not {target}"
    return x45m.tokenizer()


# ---- the inventory (CPU) -------------------------------------------------------------------------------------------


def tokenizer_of(target: str):
    """Any target's tokenizer from its cached files at the pinned revision (statement_positions.load_tokenizer's
    fallback; no chat template needed: the classifier only encodes words)."""
    from huggingface_hub import try_to_load_from_cache
    from transformers import AutoTokenizer

    t = pins.TARGETS[target]
    path = try_to_load_from_cache(t["repo"], "tokenizer.json", revision=t["revision"])
    assert isinstance(path, str), f"{t['repo']}: tokenizer not cached"
    return AutoTokenizer.from_pretrained(str(Path(path).parent), **t.get("tokenizer_kwargs", {}))


def views_of(set_name: str, reader: str) -> tuple[str, ...]:
    """The reader views of one atom list: E1's lookup Δ serves both readers; Z2's Δ is its reader's own."""
    return X.READERS if set_name == "e1" else (reader,)


def e1_vocab(items: list[dict]) -> dict[str, set[str]]:
    """Per main-test domain: SAME_CLASS and every entity the run's items name."""
    out = {d: set(v) for d, v in SAME_CLASS.items()}
    for it in items:
        sc = it["views"][X.LOOKUP]
        out.setdefault(sc["domain"], set()).update([sc["bridge"], sc["new"], *sc["items"]])
    return out


def label_run(tok, items: list[dict], rows: list[dict]) -> list[dict]:
    """Every atom of every atom list classified in each of its reader views: one record per (item, view)."""
    by_key = {(it["set"], it["key"]): it for it in items}
    vocab = e1_vocab([it for it in items if it["set"] == "e1"])
    out = []
    for r in rows:
        it = by_key[(r["set"], r["key"])]
        for view in views_of(r["set"], r["reader"]):
            sc = it["views"][view]
            ctx = e1_context(tok, sc, view, vocab) if r["set"] == "e1" else z2_context(tok, sc)
            atoms = []
            for a in r["atoms"]:
                c, via, detail = classify(a["token"], a["token_id"], ctx)
                atoms.append({**a, "class": c, "via": via, "detail": detail})
            out.append({"set": r["set"], "key": r["key"], "view": view, "delta": r["reader"], "entity": r["entity"],
                        "cf_entity": r["cf_entity"], "share_k25": r["share_k25"], "atoms": atoms})  # fmt: skip
    return out


def per_item(rec: dict) -> dict[str, dict[str, float]]:
    """One item's class shares: of the 25 atoms (count / 25) and of the rebuilt energy (sum of the atoms' energy
    shares / the part's share of ||Δ||^2)."""
    total = sum(a["share"] for a in rec["atoms"])
    n = len(rec["atoms"])
    return {"atoms": {c: sum(a["class"] == c for a in rec["atoms"]) / n for c in CLASSES},
            "energy": {c: sum(a["share"] for a in rec["atoms"] if a["class"] == c) / total for c in CLASSES}}  # fmt: skip


def summarise(recs: list[dict], n_boot: int = X.N_BOOT) -> dict:
    """Per class: the mean share of atoms and of rebuilt energy over items, with 95 % cluster-bootstrap intervals over
    the bridge entity (x0_necessity.resampled_rates, seed 0), and the items with at least one atom of the class; the
    bridge classes by how they matched, with the share of their atoms whose sign points the expected way (original
    bridge: -, it leaves; new bridge: +, it arrives); 'other' by detail; the part's share of ||Δ||^2."""
    ents = [r["entity"] for r in recs]
    vals = [per_item(r) for r in recs]
    out: dict[str, Any] = {"n": len(recs), "entities": len(set(ents)),
                           "share_k25_median": float(np.median([r["share_k25"] for r in recs]))}  # fmt: skip
    for kind in ("atoms", "energy"):
        series = {c: [v[kind][c] for v in vals] for c in CLASSES}
        boot = X.resampled_rates(series, ents, n_boot, X.BOOT_SEED)
        out[kind] = {c: [round(float(np.mean(series[c])), 4), *(round(b, 4) for b in X.interval(boot[c]))]
                     for c in CLASSES}  # fmt: skip
    out["items_with"] = {c: sum(any(a["class"] == c for a in r["atoms"]) for r in recs) for c in CLASSES}
    via: dict[str, dict[str, list]] = {
        "bridge": collections.defaultdict(list),
        "new_bridge": collections.defaultdict(list),
    }
    for r in recs:
        for a in r["atoms"]:
            if a["class"] in via:
                via[a["class"]][a["via"]].append((a["share"], a["coef"]))
    want = {"bridge": -1, "new_bridge": 1}
    total = sum(a["share"] for r in recs for a in r["atoms"])
    out["bridge_by_match"] = {c: {v: {"atoms": len(x), "energy": round(sum(s for s, _ in x) / total, 4),
                                      "sign_as_expected": round(sum(np.sign(k) == want[c] for _, k in x) / len(x), 3)}
                                  for v, x in sorted(d.items())} for c, d in via.items()}  # fmt: skip
    other = collections.defaultdict(float)
    for r in recs:
        for a in r["atoms"]:
            if a["class"] == "other":
                other[a["detail"] or "none"] += a["share"] / total
    out["other_by_detail"] = {k: round(v, 4) for k, v in sorted(other.items())}
    return out


def sources(target: str) -> dict[str, str]:
    """Per set, the run its atoms come from: the forward run where it holds the set, else (E1) the CPU states run."""
    out = {}
    for s in SETS:
        for run in (FWD_RUNS.get(target), STATES_RUNS.get(target)):
            path = RESULTS / run / "atoms.jsonl" if run else None
            if path and path.exists() and any(r["set"] == s for r in X.read_jsonl(path)):
                out[s] = run
                break
    return out


def labelled(tok, run: str, set_name: str) -> tuple[list[dict], list[dict]]:
    """The classified (item, view) records of one set of a run, and the run's items."""
    items = [it for it in X.read_jsonl(RESULTS / run / "items.jsonl") if it["set"] == set_name]
    rows = [r for r in X.read_jsonl(RESULTS / run / "atoms.jsonl") if r["set"] == set_name]
    return label_run(tok, items, rows), items


def hand_items(n_items: int, k: int = N_HAND, seed: int = SEED) -> list[int]:
    return sorted(random.Random(seed).sample(range(n_items), min(k, n_items)))


def stage_handsheet(targets: tuple[str, ...]) -> Path:
    """For the hand check: per target N_HAND E1 items (seed 0 among its N_ITEMS) with the scene, the bridges, both
    readers' answers and the 25 atoms (rank, coefficient, token), WITHOUT the classifier's labels. The labeller writes
    labels.json beside it: {"<target>|<item key>": {"<rank>": "<class>", ...}} with classes from CLASSES, in the
    lookup's view (answer_own = the lookup's answers, answer_other = the recall's)."""
    out = RESULTS / f"hand-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = [f"# {EXP} hand-check sheet (E1, the lookup's view; no classifier labels)", "",
             "Classes: " + "; ".join(f"`{c}` {t}" for c, t in CLASS_TEXT.items()), ""]  # fmt: skip
    sheet = {}
    for target in targets:
        run = sources(target).get("e1")
        if not run:
            continue
        items = {it["key"]: it for it in X.read_jsonl(RESULTS / run / "items.jsonl") if it["set"] == "e1"}
        rows = [r for r in X.read_jsonl(RESULTS / run / "atoms.jsonl") if r["set"] == "e1"]
        for i in hand_items(len(rows)):
            r = rows[i]
            sc = items[r["key"]]["views"][X.LOOKUP]
            key = f"{target}|{r['key']}"
            sheet[key] = {"run": run, "scene": sc,
                          "atoms": [[a["rank"], a["token"], a["coef"], a["token_id"]] for a in r["atoms"]]}  # fmt: skip
            lines += [f"## {key}: {sc['bridge']} -> {sc['new']}", "", f"Text: {sc['text']}", "",
                      f"Answers (O, S): lookup {sc['answers'][X.LOOKUP]}, recall {sc['answers'][X.RECALL]}", "",
                      "; ".join(f"{a['rank']}: {show(a, cls=False)}" for a in r["atoms"]), ""]  # fmt: skip
    (out / "sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    (out / "sheet.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def hand_pairs(sheet: dict, labels: dict[str, dict[str, str]], tokenizers: dict) -> dict[str, list[tuple]]:
    """Per target, (hand label, classifier label, token) for every labelled atom of a sheet: the classifier run on the
    sheet's own atoms and scene (the lookup's view), so the check does not depend on which run the report reads."""
    vocab = {d: set(v) for d, v in SAME_CLASS.items()}
    out: dict[str, list[tuple]] = collections.defaultdict(list)
    for key, per in labels.items():
        target = key.split("|", 1)[0]
        entry = sheet[key]
        if target not in tokenizers:
            tokenizers[target] = tokenizer_of(target)
        ctx = e1_context(tokenizers[target], entry["scene"], X.LOOKUP, vocab)
        for rank, token, _, tid in entry["atoms"]:
            lab = per[str(rank)]
            assert lab in CLASSES, f"{key} rank {rank}: hand label {lab!r} is not a class"
            out[target].append((lab, classify(token, tid, ctx)[0], token))
        assert len(per) == len(entry["atoms"]), f"{key}: {len(per)} labels for {len(entry['atoms'])} atoms"
    return out


def hand_agreement(hand_dirs: list[Path]) -> dict:
    """The classifier against the hand labels (every hand-* folder holding sheet.json and labels.json), per target:
    items and atoms compared, the agreement, Cohen's kappa, and the disagreements (hand -> classifier, with tokens)."""
    pairs: dict[str, list[tuple]] = collections.defaultdict(list)
    tokenizers: dict = {}
    for d in hand_dirs:
        if (d / "labels.json").exists():
            sheet = json.loads((d / "sheet.json").read_text())
            labels = json.loads((d / "labels.json").read_text())
            for t, p in hand_pairs(sheet, labels, tokenizers).items():
                pairs[t] += p
    out = {}
    for t, p in pairs.items():
        n, agree = len(p), sum(h == c for h, c, _ in p)
        ph, pc = collections.Counter(h for h, _, _ in p), collections.Counter(c for _, c, _ in p)
        pe = sum(ph[c] * pc[c] for c in CLASSES) / n**2
        miss = collections.defaultdict(list)
        for h, c, tok in p:
            if h != c:
                miss[f"{h} -> {c}"].append(tok)
        out[t] = {"items": len(p) // K, "atoms": n, "agree": agree, "rate": round(agree / n, 4),
                  "kappa": round((agree / n - pe) / (1 - pe), 4) if pe < 1 else None,
                  "hand_classes": dict(ph), "disagreements": dict(miss)}  # fmt: skip
    return out


N_CHANCE = 2000  # random letter tokens per model for the chance baseline


def chance(tok, recs: list[dict], items: list[dict], n: int = N_CHANCE, seed: int = SEED) -> dict[str, float]:
    """The baseline: the class shares of n random letter tokens (seed 0) classified in every (item, view) of recs, i.e.
    the atom shares if OMP picked letter atoms at random."""
    letters, decoded = letter_ids(tok, len(tok))
    pick_ids = random.Random(seed).sample(letters, n)
    by_key = {(it["set"], it["key"]): it for it in items}
    vocab = e1_vocab([it for it in items if it["set"] == "e1"])
    cnt: collections.Counter = collections.Counter()
    for r in recs:
        sc = by_key[(r["set"], r["key"])]["views"][r["view"]]
        ctx = e1_context(tok, sc, r["view"], vocab) if r["set"] == "e1" else z2_context(tok, sc)
        cnt.update(classify(decoded[t], t, ctx)[0] for t in pick_ids)
    total = sum(cnt.values())
    return {c: round(cnt[c] / total, 5) for c in CLASSES}


# adjacent pairs of the stack pass the dataviz palette validator (CVD dE >= 9.2, normal vision >= 20.8)
COLOR = {"bridge": "#2a78d6", "new_bridge": "#eb6834", "scene_item": "#1baf7a", "person": "#6250d6",
         "answer_own": "#e34948", "answer_other": "#eda100", "same_class": "#008300", "function": "#e87ba4",
         "other": "#c8c7c1"}  # fmt: skip
FIG_LABEL = {**CLASS_TEXT, "answer_own": "answer word: the lookup's (E1) / the reader's own (Z2)",
             "answer_other": "answer word: the recall's (E1)"}  # fmt: skip
MODEL_SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "muse-glimmer-30b": "Muse"}


def figure(summary: dict, examples: dict, path: Path) -> None:
    """One stacked bar per model (E1, the lookup's view; Z2, per reader) by share of the rebuilt energy, the answer
    word in red with its share printed above the bar; printed examples beside (top-5 atoms by |coefficient|)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = ["DejaVu Sans", "Arial Unicode MS", "PingFang SC", "Hiragino Sans GB"]
    fig = plt.figure(figsize=(17, 6.2))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.6, 2.6], wspace=0.25)
    panels = [("e1", fig.add_subplot(gs[0]), "Main test (E1): one change\nat the bridge word, both readers"),
              ("z2", fig.add_subplot(gs[1]), "Zach's never-named bridge (Z2)\nper reader, the description's last token")]  # fmt: skip
    for s, ax, title in panels:
        bars = [(t, v) for t in summary for v, cell in summary[t].get(s, {}).items()
                if s == "z2" or v == X.LOOKUP]  # fmt: skip
        for x, (t, v) in enumerate(bars):
            e = summary[t][s][v]["energy"]
            bottom = 0.0
            for c in CLASSES:
                ax.bar(x, e[c][0], bottom=bottom, color=COLOR[c], width=0.7, edgecolor="white", linewidth=1)
                bottom += e[c][0]
            ans = e["answer_own"][0] + e["answer_other"][0]
            ax.text(x, 1.01, f"answer\n{100 * ans:.1f}%", ha="center", va="bottom", fontsize=8, color="#52514e")
        names = [MODEL_SHORT[t] + ("" if s == "e1" else f"\n{READER_NAME[v]}") for t, v in bars]
        ax.set_xticks(range(len(bars)), names, fontsize=9)
        ax.set_ylim(0, 1.12)
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_title(title, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e6e5e0", linewidth=0.6)
        ax.set_axisbelow(True)
    panels[0][1].set_ylabel("share of the rebuilt energy (mean over 50 items)")
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLOR[c]) for c in CLASSES]
    fig.legend(handles, [FIG_LABEL[c] for c in CLASSES], loc="lower center", ncol=5, fontsize=8, frameon=False)
    ax = fig.add_subplot(gs[2])
    ax.axis("off")
    lines = ["Top-5 atoms by |coefficient| (+ towards the changed prompt)", ""]
    for t, per in examples.items():
        for s, ex in per.items():
            for e in ex[:2]:  # E1: two items; Z2: one item, both readers
                lines.append(f"{MODEL_SHORT[t]} {s.upper()} · {e['bridge']} → {e['new']}" + (f" ({READER_NAME[e['view']]})" if s == "z2" else ""))  # fmt: skip
                lines.append("   " + ", ".join(f"{a['coef']:+.1f} {a['token'].strip() or repr(a['token'])}" for a in e["top"]))  # fmt: skip
    ax.text(0, 1, "\n".join(lines), va="top", ha="left", fontsize=8.5, family=plt.rcParams["font.family"])
    fig.suptitle("What the lens part's 25 atoms decode to (signed OMP over the J++ letter atoms at L; UNVERIFIED)",
                 fontsize=11)  # fmt: skip
    fig.subplots_adjust(bottom=0.2, top=0.86, left=0.05, right=0.99)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fmt_ci(v: list) -> str:
    return f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]"


def stage_report(targets: tuple[str, ...], hand_dirs: list[Path] | None = None) -> Path:
    """The inventory: per model, set and reader view the class shares (atoms, rebuilt energy) with intervals and the
    chance baseline, the bridge classes by match and sign, the printed examples, the hand check and the figure, into
    results/x52_atoms/report-<UTC>/."""
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state

    out = RESULTS / f"report-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    summary: dict[str, dict] = {}
    recs_all: dict[str, list[dict]] = {}
    examples: dict[str, dict] = {}
    srcs, checks, base = {}, {}, {}
    for t in targets:
        srcs[t] = sources(t)
        if not srcs[t]:
            continue
        tok = tokenizer_of(t)
        summary[t], examples[t], base[t] = {}, {}, {}
        recs_all[t] = []
        for s, run in srcs[t].items():
            checks[f"{t}|{run}"] = json.loads((RESULTS / run / "checks.json").read_text())
            recs, items = labelled(tok, run, s)
            recs_all[t] += recs
            summary[t][s] = {
                v: summarise([r for r in recs if r["view"] == v]) for v in dict.fromkeys(r["view"] for r in recs)
            }
            base[t][s] = chance(tok, recs, items)
            first = [r for r in recs if r["view"] == (X.LOOKUP if s == "e1" else "K")]
            keys = [first[i]["key"] for i in hand_items(len(first), N_SHOW)]
            examples[t][s] = [{"key": r["key"], "view": r["view"], "bridge": r["entity"], "new": r["cf_entity"],
                               "share_k25": r["share_k25"], "top": top_by_coef(r)}
                              for k in keys for r in recs if r["key"] == k and (s == "z2" or r["view"] == X.LOOKUP)]  # fmt: skip
    hand = hand_agreement(hand_dirs if hand_dirs is not None else sorted(RESULTS.glob("hand-*")))
    out.mkdir(parents=True)
    X.write_jsonl(out / "labelled.jsonl", [{"target": t, **r} for t, rs in recs_all.items() for r in rs])
    blob = {"exp": EXP, "part": "52 A", "verdict": VERDICT, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "code": git_state(), "switches": switches(), "sources": srcs, "checks": checks, "summary": summary,
            "chance": base, "hand": hand, "n_boot": X.N_BOOT, "boot_seed": X.BOOT_SEED, "classes": CLASS_TEXT}  # fmt: skip
    (out / "tables.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    keep = ("exp", "part", "verdict", "written_utc", "code", "switches", "sources", "n_boot", "boot_seed")
    (out / "manifest.json").write_text(json.dumps({k: blob[k] for k in keep}, indent=1) + "\n")
    write_tables(out, blob, examples)
    figure(summary, examples, out / "fig_atoms.png")
    print("wrote", out, flush=True)
    return out


def write_tables(out: Path, blob: dict, examples: dict) -> None:
    """tables.md (the inventory), examples.md (10 items per model and set, top-5 atoms verbatim) and verdict.md."""
    summary, base, hand = blob["summary"], blob["chance"], blob["hand"]
    head = "| model | set | reader view | n (entities) | " + " | ".join(CLASSES) + " |"
    sep = "|" + "---|" * (len(CLASSES) + 4)
    lines = [f"# {EXP}: what is inside the top-25 atoms of the lens part (batch 52 A; {VERDICT}; UNVERIFIED)", "",
             "Per item: Δ's 25 signed-OMP atoms over the J++ letter dictionary at L; each atom's class (automatic, "
             "scripts/x52_atoms.py classify); per item the class shares of the 25 atoms and of the rebuilt energy (the "
             "energy an atom adds when it enters, over the part's share of ||Δ||^2); means over items with 95 % "
             f"cluster-bootstrap intervals over the bridge entity ({X.N_BOOT:,}, seed {X.BOOT_SEED}). E1: one Δ serves "
             "both readers (identical prompts through the bridge word), so the two views differ only in which answer "
             "class is the reader's own. Z2: each reader its own Δ; both ask for the same answer, so 'answer_other' is "
             "empty. Chance: the class shares of 2,000 random letter tokens (seed 0) in the same items and views.", "",
             "Classes: " + "; ".join(f"`{c}` {t}" for c, t in CLASS_TEXT.items()), "",
             "Sources: " + "; ".join(f"{t}: {v}" for t, v in blob["sources"].items()), ""]  # fmt: skip
    for kind, title in (("energy", "Share of the rebuilt energy"), ("atoms", "Share of the 25 atoms")):
        lines += [f"## {title}", "", head, sep]
        for t, per in summary.items():
            for s, views in per.items():
                for v, cell in views.items():
                    lines.append(f"| {MODEL_SHORT[t]} | {s} | {READER_NAME[v]} | {cell['n']} ({cell['entities']}) | "
                                 + " | ".join(fmt_ci(cell[kind][c]) for c in CLASSES) + " |")  # fmt: skip
                if kind == "atoms":
                    lines.append(f"| {MODEL_SHORT[t]} | {s} | chance | | " + " | ".join(f"{base[t][s][c]:.4f}" for c in CLASSES) + " |")  # fmt: skip
        lines.append("")
    lines += ["## Items with at least one atom of the class", "", head, sep]
    for t, per in summary.items():
        for s, views in per.items():
            for v, cell in views.items():
                lines.append(f"| {MODEL_SHORT[t]} | {s} | {READER_NAME[v]} | {cell['n']} | "
                             + " | ".join(str(cell["items_with"][c]) for c in CLASSES) + " |")  # fmt: skip
    lines += ["", "## The two bridge classes by how they matched (pooled share of rebuilt energy; the share of their atoms "
              "whose sign points the expected way: original -, new +)", "",
              "| model | set | view | class | match | atoms | energy | sign as expected |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for t, per in summary.items():
        for s, views in per.items():
            for v, cell in views.items():
                if s == "e1" and v != X.LOOKUP:
                    continue
                for c, d in cell["bridge_by_match"].items():
                    for via, x in d.items():
                        lines.append(f"| {MODEL_SHORT[t]} | {s} | {READER_NAME[v]} | {c} | {via} | {x['atoms']} | "
                                     f"{x['energy']:.4f} | {x['sign_as_expected']:.2f} |")  # fmt: skip
    lines += ["", "## 'other' by detail (pooled share of rebuilt energy)", ""]
    for t, per in summary.items():
        for s, views in per.items():
            for v, cell in views.items():
                if s == "e1" and v != X.LOOKUP:
                    continue
                lines.append(f"- {MODEL_SHORT[t]} {s} {READER_NAME[v]}: {cell['other_by_detail']}; median part share of "
                             f"||Δ||^2 {cell['share_k25_median']:.3f}")  # fmt: skip
    lines += ["", "## Hand check (E1, the lookup's view)", ""]
    for t, h in hand.items():
        lines.append(f"- {MODEL_SHORT[t]}: {h['agree']} / {h['atoms']} atoms agree ({h['rate']:.3f}; Cohen's kappa "
                     f"{h['kappa']}) over {h['items']} items; hand classes {h['hand_classes']}; disagreements (hand -> "
                     f"classifier: tokens): {json.dumps(h['disagreements'], ensure_ascii=False)}")  # fmt: skip
    if not hand:
        lines.append("- no labels.json found")
    lines += ["", "## Run checks", ""] + [f"- {k}: {json.dumps(v)}" for k, v in blob["checks"].items()]
    (out / "tables.md").write_text("\n".join(lines) + "\n")
    ex = [f"# {EXP}: top-{N_TOP} atoms by |coefficient| for {N_SHOW} items per model and set (seed {SEED}; verbatim "
          "tokens, + = towards the changed prompt; UNVERIFIED)", ""]  # fmt: skip
    for t, per in examples.items():
        for s, rows in per.items():
            ex += [f"## {MODEL_SHORT[t]} {s}", ""]
            for e in rows:
                ex.append(f"- {e['key']} ({READER_NAME[e['view']]}; {e['bridge']} -> {e['new']}; part share "
                          f"{e['share_k25']:.3f}): " + "; ".join(show(a) for a in e["top"]))  # fmt: skip
            ex.append("")
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    v = [f"# {EXP} verdict (batch 52 A)", "", VERDICT, "",
         "Descriptive inventory, no rule fixed in advance; every number UNVERIFIED until hand-checked. Tables: "
         "tables.md; examples: examples.md; figure: fig_atoms.png; every classified atom: labelled.jsonl.", ""]  # fmt: skip
    for t, per in summary.items():
        for s, views in per.items():
            for vw, cell in views.items():
                e = cell["energy"]
                v.append(f"- {MODEL_SHORT[t]} {s} ({READER_NAME[vw]}'s view, n = {cell['n']}): rebuilt energy in the "
                         f"original bridge word {fmt_ci(e['bridge'])}, the new bridge word {fmt_ci(e['new_bridge'])}, the "
                         f"reader's answer word {fmt_ci(e['answer_own'])}, the other reader's {fmt_ci(e['answer_other'])}, "
                         f"other {fmt_ci(e['other'])}; items with an own-answer atom {cell['items_with']['answer_own']}")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(v) + "\n")


def top_by_coef(rec: dict, k: int = N_TOP) -> list[dict]:
    return sorted(rec["atoms"], key=lambda a: -abs(a["coef"]))[:k]


def show(a: dict, cls: bool = True) -> str:
    """An atom as printed: its signed coefficient and its token verbatim (quoted, spaces visible)."""
    return f"{a['coef']:+.2f} {json.dumps(a['token'], ensure_ascii=False)}" + (f" ({a['class']})" if cls else "")


# ---- fetch (CPU, network): the lm_head and final norm of the pinned checkpoint, and the pinned lens ----------------

HEAD_KEYS = {"lm_head.weight": "lm_head.weight", "model.language_model.norm.weight": "norm.weight"}


def fetch_tensor(fs, path: str, name: str, rev: str):
    """One tensor of a safetensors shard by byte ranges (its header, then its bytes), no full download."""
    import struct

    import torch

    dtypes = {"BF16": torch.bfloat16, "F16": torch.float16, "F32": torch.float32}
    with fs.open(path, "rb", revision=rev, block_size=64 << 20) as f:
        n = struct.unpack("<Q", f.read(8))[0]
        header = json.loads(f.read(n))
        meta = header[name]
        a, b = meta["data_offsets"]
        f.seek(8 + n + a)
        buf = bytearray(f.read(b - a))
    assert len(buf) == b - a, f"{name}: short read"
    t = torch.frombuffer(buf, dtype=dtypes[meta["dtype"]]).reshape(meta["shape"]).clone()
    return t, {"dtype": meta["dtype"], "shape": meta["shape"], "bytes": [8 + n + a, 8 + n + b]}


def stage_fetch(targets: tuple[str, ...] = ("qwen3.5-9b", "qwen3.6-27b")) -> None:
    """Per target: the pinned lens (hf_hub_download, sha256 = the pin) and the lm_head / final-norm weights of the
    pinned revision (cache/x52_atoms/<target>/head.safetensors, with head.json recording where they came from)."""
    import hashlib

    import torch
    from huggingface_hub import HfFileSystem, hf_hub_download
    from safetensors.torch import save_file

    fs = HfFileSystem()
    for target in targets:
        t = pins.TARGETS[target]
        repo, file, rev = t["lenses"]["jpp"]
        assert repo != "local", f"{target}: its lens is a local file on the boxes; use the GPU stage"
        hf_hub_download(repo, file, revision=rev)
        index = json.loads(
            Path(hf_hub_download(t["repo"], "model.safetensors.index.json", revision=t["revision"])).read_text()
        )
        out, rec = {}, {"repo": t["repo"], "revision": t["revision"], "tensors": {}}
        for name, short in HEAD_KEYS.items():
            shard = index["weight_map"][name]
            out[short], info = fetch_tensor(fs, f"{t['repo']}/{shard}", name, t["revision"])
            info["sha256"] = hashlib.sha256(out[short].contiguous().view(-1).view(torch.uint8).numpy()).hexdigest()
            rec["tensors"][short] = {"name": name, "shard": shard, **info}
        d = CACHE / target
        d.mkdir(parents=True, exist_ok=True)
        save_file(out, str(d / "head.safetensors"))
        (d / "head.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(target, json.dumps(rec), flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["fetch", "atoms", "handsheet", "report"])
    ap.add_argument("--name")
    ap.add_argument("--delta", choices=["states", "forward"], default="forward")
    ap.add_argument("--sets", default="e1,z2", help="comma-separated: e1, z2")
    ap.add_argument("--states-root", type=Path, default=pins.RESULTS_DIR / "x51_jread",
                    help="where 51.10's run folders with states.npz live (gitignored: the main checkout's results/)")  # fmt: skip
    ap.add_argument("--targets", default=",".join(MODELS))
    ap.add_argument("--hand", type=Path, help="report: a hand-* folder holding labels.json (default: every one)")
    a = ap.parse_args()
    targets = tuple(a.targets.split(","))
    if a.stage == "fetch":
        stage_fetch()
    elif a.stage == "atoms":
        assert a.name, "--name"
        stage_atoms(a.name, a.delta, tuple(a.sets.split(",")), a.states_root)
    elif a.stage == "handsheet":
        stage_handsheet(targets)
    else:
        stage_report(targets, [a.hand] if a.hand else None)


if __name__ == "__main__":
    main()
