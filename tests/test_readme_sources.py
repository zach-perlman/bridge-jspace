"""README.md (the joint story, 27 Oct): every number is traceable. Each number or number group carries an HTML comment
`<!-- src: <repo path> | <key>; <key> ... -->`; this test checks that the path exists, that each key resolves in it, that
every image and link path exists, and (loosely) that no digit-bearing line of prose lacks a source comment.

Key resolution by source type:
- csv (figures/story/data.csv, docs/breadth/data.csv, docs/shared/grid.csv): the key equals some cell of the file;
- json: the key is a top-level key;
- "l.N" or "l.N-M": the file has at least that many lines;
- anything else (Markdown, scripts): the key is a substring of the file, whitespace collapsed (hard-wrapped pages).
"""

import csv
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
README = REPO / "README.md"
CSV_SOURCES = {"figures/story/data.csv", "docs/breadth/data.csv", "docs/shared/grid.csv"}

# In a table row the separator is written "\|" (a bare pipe would split the cell in GitHub's table syntax).
SRC = re.compile(r"<!--\s*src:\s*([^|\\]*?)\s*\\?\|\s*(.*?)\s*-->", re.S)
LINE_REF = re.compile(r"^l\.(\d+)(?:-(\d+))?$")
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
COMMENT = re.compile(r"<!--.*?-->", re.S)
# Digits that are names, not numbers: model sizes, layers, test and question ids, dates, model names.
NAMES = [
    r"\bA?\d+(?:\.\d+)?B\b",  # 9B, 27B, 122B, A10B
    r"\bL\d+(?:-\d+)?\b|\bL/\d\b",  # L26, L36-42, L/2
    r"\bQ\d+\.\d+(?:-Q\d+\.\d+)?\b",  # Q46.1, Q46.2-Q46.3
    r"\b\d+[a-z]\b",  # 45r, 45p
    r"\b\d{1,2} Oct\b",  # dates
    r"\bQwen\d\.\d\b",
    r"\bH0\b",  # Zach's hypothesis name
    r"\bFinding \d\b",  # a section of the README itself
]


def collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def sources(text: str) -> list[tuple[str, list[str]]]:
    return [(m.group(1).strip(), [k.strip() for k in m.group(2).split(";") if k.strip()]) for m in SRC.finditer(text)]


def resolve(path: str, key: str) -> str | None:
    """None if the key resolves in the file, else the reason."""
    p = REPO / path
    if not p.is_file():
        return "no such file"
    if m := LINE_REF.match(key):
        need = int(m.group(2) or m.group(1))
        n = sum(1 for _ in p.open(encoding="utf-8"))
        return None if n >= need else f"file has {n} lines, needs {need}"
    if path in CSV_SOURCES:
        with p.open(newline="", encoding="utf-8") as f:
            cells = {c.strip() for row in csv.reader(f) for c in row}
        return None if key in cells else "key is no cell of the csv"
    if p.suffix == ".json":
        return None if key in json.loads(p.read_text(encoding="utf-8")) else "key is no top-level json key"
    return None if collapse(key) in collapse(p.read_text(encoding="utf-8")) else "key text not found"


def unresolved(text: str) -> list[str]:
    bad = []
    for path, keys in sources(text):
        if not keys:
            bad.append(f"{path}: no key")
        for key in keys:
            if (why := resolve(path, key)) is not None:
                bad.append(f"{path} | {key}: {why}")
    return bad


def missing_paths(text: str) -> list[str]:
    bad = []
    for target in LINK.findall(COMMENT.sub("", text)):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        if not (REPO / target.split("#", 1)[0]).exists():
            bad.append(target)
    return bad


def unsourced_lines(text: str) -> list[str]:
    """Lines of prose (bullets, paragraphs, table rows) with a digit that is not a name and no src comment."""
    bad = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "![")) or re.fullmatch(r"\|[-| ]+\|", s):
            continue
        has_src = "<!-- src:" in s
        rest = COMMENT.sub(" ", s)
        rest = re.sub(r"\]\([^)]*\)", "]", rest)  # link targets
        rest = re.sub(r"`[^`]*`", " ", rest)  # code spans
        for pat in NAMES:
            rest = re.sub(pat, " ", rest)
        if re.search(r"\d", rest) and not has_src:
            bad.append(s)
    return bad


def test_every_source_path_and_key_resolves():
    text = README.read_text(encoding="utf-8")
    assert sources(text), "README.md has no src comments"
    assert not (bad := unresolved(text)), bad


def test_every_image_and_link_path_exists():
    assert not (bad := missing_paths(README.read_text(encoding="utf-8"))), bad


def test_no_number_without_a_source():
    assert not (bad := unsourced_lines(README.read_text(encoding="utf-8"))), bad


def test_checks_catch_failures():
    """The three checks fail on a broken page (a moved key, a missing file, an unsourced number)."""
    assert unresolved("x <!-- src: docs/breadth/data.csv | ko.q27.nosuchkey -->")
    assert unresolved("x <!-- src: no/such/file.md | anything -->")
    assert unresolved("x <!-- src: EXPERIMENTS.md | l.999999 -->")
    assert not unresolved("x <!-- src: docs/breadth/data.csv | ko.q27.mk -->")
    assert sources("| a <!-- src: docs/breadth/data.csv \\| ko.q27.mk --> | 1 |") == [
        ("docs/breadth/data.csv", ["ko.q27.mk"])
    ]
    assert unresolved("| a <!-- src: docs/breadth/data.csv \\| ko.q27.nosuchkey --> | 1 |")
    assert missing_paths("![a](figures/nope.png)")
    assert unsourced_lines("- the gap is 0.53 on the 27B")
    assert not unsourced_lines("- the 27B at L32 (45r, Q46.1, 27 Oct; Finding 2)")
    assert unsourced_lines("- Finding 2 moves the stated answer by 24.6 points")
