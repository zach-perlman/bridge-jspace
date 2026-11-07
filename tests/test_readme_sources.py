"""README.md (the joint story, 27 Oct): every number is traceable. Each number or number group carries an HTML comment
`<!-- src: <repo path> | <key>; <key> ... -->`; this test checks that the path exists, that each key resolves in it, that
every image and link path exists, and (loosely) that no digit-bearing line of prose lacks a source comment.

Key resolution by source type:
- csv (data/figures/depth/data.csv, docs/breadth/data.csv, docs/shared/grid.csv): the key equals some cell of the file;
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
CSV_SOURCES = {"data/figures/depth/data.csv", "docs/breadth/data.csv", "docs/shared/grid.csv", "data/figures/writeup/data.csv"}

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
    r"\b\d{1,2}–\d{1,2} Oct\b|\b\d{1,2} Oct\b|\b20\d\d\b",  # dates, date ranges, years
    r"\bMATS \d+\.\d\b",  # the programme's name
    r"\bQwen\d\.\d\b",
    r"\b[HC]\d\b′?",  # hypothesis names (H0-H3, C1-C3, C2′), docs/plans/hypotheses.md
    r"\bclaims? \d+(?:, \d+)*\b",  # the depth report's numbered claims
    r"\bGemma \d\b",  # a model name
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
    page = COMMENT.sub("", p.read_text(encoding="utf-8"))  # the depth README carries its own source comments
    return None if collapse(key) in collapse(page) else "key text not found"


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


# ---- the page's shape (README brief, 7 Nov: esk-audit's outline) ---------------------------------------------------------
TEMPLATE = REPO / "docs" / "readme" / "README.template.md"
WORD_BUDGET = 4000  # visible words outside <details>, comments, code blocks and image links


def visible_words(text: str) -> int:
    for pat in (r"<!--.*?-->", r"<details>.*?</details>", r"```.*?```", r"!\[[^\]]*\]\([^)]*\)"):
        text = re.sub(pat, " ", text, flags=re.S)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return len(re.findall(r"\w[\w'’.-]*", text))


def test_visible_text_within_the_word_budget():
    assert visible_words(README.read_text(encoding="utf-8")) <= WORD_BUDGET


BREADTH = REPO / "docs" / "breadth" / "README.md"
BREADTH_BUDGET = 3000  # finishing-pass brief C4: the breadth page in the root README's shape


def test_breadth_visible_text_within_its_budget():
    assert visible_words(BREADTH.read_text(encoding="utf-8")) <= BREADTH_BUDGET


def test_breadth_figures_take_their_captions_from_the_store():
    """Every figure on the breadth page is followed by its {{caption|set/stem}} in the template (no bare "Fig. N.")."""
    tpl = (REPO / "docs" / "breadth" / "README.template.md").read_text(encoding="utf-8")
    figs = re.findall(r"!\[[^\]]*\]\(\.\./\.\./figures/([\w-]+)/([\w-]+)\.png\)\n\n\{\{caption\|([\w-]+)/([\w-]+)\}\}", tpl)
    assert len(figs) == len(re.findall(r"!\[[^\]]*\]\(\.\./\.\./figures/", tpl))
    assert all(a == c and b == d for a, b, c, d in figs)
    assert "*Fig. " not in tpl


def test_alt_texts_are_unique():
    alts = re.findall(r"!\[([^\]]*)\]\(", README.read_text(encoding="utf-8"))
    assert len(alts) == len(set(alts)), sorted(a for a in alts if alts.count(a) > 1)


def test_every_figure_takes_its_caption_from_the_store():
    """In the template, each figure of a set (but the key, which the paragraph above it explains) is followed by its
    {{caption|set/stem}}: one caption per PNG, the same on every page."""
    from bridge_jspace.figkit import layout as L

    lines = [ln for ln in TEMPLATE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    bad = []
    for i, ln in enumerate(lines):
        m = re.fullmatch(r"\{\{fig\|([\w-]+)\}\}", ln.strip())
        img = re.match(r"!\[[^\]]*\]\(figures/([\w-]+)/([\w-]+)\.png\)", ln.strip())
        if m:
            want = f"readme/{L.path('readme', m.group(1)).stem}"
        elif img and img.group(2) != "00_key":
            want = f"{img.group(1)}/{img.group(2)}"
        else:
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""  # a figure inside a list item is indented
        if not nxt.startswith("{{caption|" + want + "}}"):
            bad.append(want)
    assert not bad, bad
