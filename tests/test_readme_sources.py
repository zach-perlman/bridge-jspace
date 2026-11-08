"""README.md, docs/depth/README.md and docs/breadth/README.md: every number is traceable. Each number or number group
carries an HTML comment `<!-- src: <repo path> | <key>; <key> ... -->`; these tests check, on all three pages, that the
path is a file tracked by git, that each key resolves in it, and that every run file behind a cited key (a data row's
source column) is tracked by git; on the root README also that every image and link path exists and (loosely) that no
digit-bearing line of prose lacks a source comment. The source tests are the Reproduce section's second tier (DEVELOPER.md).

Key resolution by source type:
- csv (CSV_SOURCES): the key equals some cell of the file; a key that itself contains ";" is tried whole first;
- json: the key is a key of the file at any depth (the depth README cites nested keys of its run tables);
- "l.N" or "l.N-M": the file has at least that many lines;
- "a :: b": all parts stand on one line of the file (scripts/check_ledger.py's form, for table rows);
- anything else (Markdown, scripts): the key is a substring of the file, whitespace collapsed (hard-wrapped pages).
"""

import csv
import fnmatch
import functools
import json
import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
README = REPO / "README.md"
PAGES = ["README.md", "docs/depth/README.md", "docs/breadth/README.md"]
CSV_SOURCES = {"data/figures/depth/data.csv", "docs/breadth/data.csv", "docs/shared/grid.csv", "data/figures/writeup/data.csv",
               "data/figures/lenses.csv", "data/figures/examples/data.csv", "data/figures/reproduce.csv",
               "data/figures/provenance.csv"}  # fmt: skip
# The data files whose source column names run files (results/…, runs/…); reproduce.csv and provenance.csv name scripts.
RUN_SOURCES = (CSV_SOURCES - {"data/figures/reproduce.csv", "data/figures/provenance.csv"}) | {
    "docs/depth/x0_numbers.json"
}
RUNPATH = re.compile(r"\b(?:results|runs)/[^\s|,;\"'()\[\]]+")


@functools.cache
def tracked() -> frozenset[str]:
    """Every file git tracks (in a sparse clone too: `git ls-files` lists the files outside the sparse set)."""
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return frozenset(out.split("\0")) - {""}


@functools.cache
def tracked_dirs() -> frozenset[str]:
    return frozenset(str(p) for f in tracked() for p in Path(f).parents if str(p) != ".")


@functools.cache
def csv_cells(path: str) -> frozenset[str]:
    with (REPO / path).open(newline="", encoding="utf-8") as f:
        return frozenset(c.strip() for row in csv.reader(f) for c in row)


def json_keys(d) -> set[str]:
    if isinstance(d, dict):
        return set(d) | {k for v in d.values() for k in json_keys(v)}
    return {k for v in d for k in json_keys(v)} if isinstance(d, list) else set()


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
    if path not in tracked():
        return "not tracked by git"
    if not p.is_file():
        return "no such file in the checkout"
    if m := LINE_REF.match(key):
        need = int(m.group(2) or m.group(1))
        n = sum(1 for _ in p.open(encoding="utf-8"))
        return None if n >= need else f"file has {n} lines, needs {need}"
    if path in CSV_SOURCES:
        return None if key in csv_cells(path) else "key is no cell of the csv"
    if p.suffix == ".json":
        return None if key in json_keys(json.loads(p.read_text(encoding="utf-8"))) else "key is no json key"
    if " :: " in key:
        parts = [s.strip() for s in key.split(" :: ")]
        lines = p.read_text(encoding="utf-8").splitlines()
        return None if any(all(s in ln for s in parts) for ln in lines) else "parts not on one line"
    page = COMMENT.sub("", p.read_text(encoding="utf-8"))  # the depth README carries its own source comments
    return None if collapse(key) in collapse(page) else "key text not found"


def cited(text: str) -> list[tuple[str, list[str]]]:
    """Each src comment's path and keys, a key list that resolves whole (a csv cell containing ';') kept as one key."""
    out = []
    for m in SRC.finditer(text):
        path, raw = m.group(1).strip(), m.group(2).strip()
        keys = [k.strip() for k in raw.split(";") if k.strip()]
        out.append((path, [raw] if len(keys) > 1 and resolve(path, raw) is None else keys))
    return out


def unresolved(text: str) -> list[str]:
    bad = []
    for path, keys in cited(text):
        if not keys:
            bad.append(f"{path}: no key")
        for key in keys:
            if (why := resolve(path, key)) is not None:
                bad.append(f"{path} | {key}: {why}")
    return bad


@functools.cache
def source_column(path: str) -> list[tuple[set[str], str]]:
    """(cells, source text) per row of a data file whose source column names run files; x0_numbers.json's entries."""
    p = REPO / path
    if p.suffix == ".json":
        return [({k}, str(v.get("source", ""))) for k, v in json.loads(p.read_text(encoding="utf-8")).items()]
    with p.open(newline="", encoding="utf-8") as f:
        return [({c.strip() for c in r.values() if c}, f"{r.get('source', '')} {r.get('source row', '')}")
                for r in csv.DictReader(f)]  # fmt: skip


def run_files(text: str) -> set[str]:
    """The run files and folders (results/…, runs/…) a page's numbers come from: cited directly, or named in the
    source column of each data row (x0_numbers.json entry) that has a cited key as a cell."""
    out = set()
    for path, keys in cited(text):
        if path.startswith(("results/", "runs/")):
            out.add(path)
        elif path in RUN_SOURCES:
            for cells, source in source_column(path):
                if cells & set(keys):
                    out.update(m.rstrip(":.") for m in RUNPATH.findall(source))
    return out


def untracked_runs(paths: set[str]) -> list[str]:
    """Of the run paths, those git does not track: no tracked file or folder of that name (a glob: no tracked file
    matches it)."""
    files, dirs = tracked(), tracked_dirs()
    bad = []
    for r in sorted(paths):
        r = r.rstrip("/")
        hit = any(fnmatch.fnmatchcase(f, r) for f in files) if "*" in r else r in files or r in dirs
        if not hit:
            bad.append(r)
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


@pytest.mark.parametrize("page", PAGES)
def test_every_source_path_and_key_resolves(page):
    text = (REPO / page).read_text(encoding="utf-8")
    assert sources(text), f"{page} has no src comments"
    assert not (bad := unresolved(text)), bad


@pytest.mark.parametrize("page", PAGES)
def test_every_run_file_behind_a_number_is_tracked(page):
    """A number whose data row names a run file that no commit holds cannot be recounted from a clone."""
    runs = run_files((REPO / page).read_text(encoding="utf-8"))
    assert runs, f"{page}: no run file behind its numbers"
    assert not (bad := untracked_runs(runs)), bad


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
    rebuilt = "x <!-- src: data/figures/depth/data.csv | 47.0 (b) share rebuilt by 25 lens directions: "
    assert unresolved(rebuilt + "no; such -->")
    assert not unresolved(rebuilt + "random draws (mean; mean, 95th pct) -->")  # a cell with ';' in it
    order = "x <!-- src: results/x0_order_2x2/20261030T224216Z/tables.json | "
    assert not unresolved(order + "original_order_effect -->")  # a nested json key
    assert unresolved(order + "no_such_key -->")
    verbal = "x <!-- src: results/x47_verbal/summary-20261028T033646Z/verbal.md | reading :: "
    assert not unresolved(verbal + "not verbalizable -->")
    assert unresolved(verbal + "Over the models -->")  # both parts in the file, not on one line
    assert unresolved("x <!-- src: cache/anything.json | k -->")  # a file git does not track
    # a source column's run file, its trailing colon dropped
    runs = {"results/ablate_v2/jsuite_v2_test_chat_ko_cand2_v1/rows.jsonl"}
    assert run_files("x <!-- src: data/figures/examples/data.csv | e2.pairs_flip -->") == runs
    assert untracked_runs({"results/exp02_swaps/main_v4b200_jpp_chat64/outcomes.jsonl", "results/no/*/cells.json"})
    assert not untracked_runs({"results/x0_order_2x2/20261030T224216Z/tables.json", "results/x0_order_2x2",
                               "results/x0_necessity/x0_necessity_27b_chat/descriptive-*/cells.json"})  # fmt: skip
    assert missing_paths("![a](figures/nope.png)")
    assert unsourced_lines("- the gap is 0.53 on the 27B")
    assert not unsourced_lines("- the 27B at L32 (45r, Q46.1, 27 Oct; Finding 2)")
    assert unsourced_lines("- Finding 2 moves the stated answer by 24.6 points")


# ---- the page's shape (README brief, 7 Nov: esk-audit's outline) ---------------------------------------------------------
TEMPLATE = REPO / "docs" / "readme" / "README.template.md"
WORD_BUDGET = 2000  # visible words outside <details>, comments, code blocks and image links (readability brief, 8 Nov)


def visible_words(text: str) -> int:
    for pat in (r"<!--.*?-->", r"<details>.*?</details>", r"```.*?```", r"!\[[^\]]*\]\([^)]*\)"):
        text = re.sub(pat, " ", text, flags=re.S)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return len(re.findall(r"\w[\w'’.-]*", text))


def test_visible_text_within_the_word_budget():
    assert visible_words(README.read_text(encoding="utf-8")) <= WORD_BUDGET


def test_readme_meets_every_readability_target():
    """scripts/readme_lint.py's measures of README.md (readability brief, 8 Nov): words, slash lists, long sentences,
    colons, captions and ledger labels, each within its target."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("readme_lint", REPO / "scripts" / "readme_lint.py")
    assert spec and spec.loader
    lint = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lint)
    m = lint.measure(README)
    assert not (over := {k: (m[k], t) for k, t in lint.TARGETS.items() if m[k] > t}), over
    assert m["caption_max"] <= 60, "a README caption is over 60 words"


BREADTH = REPO / "docs" / "breadth" / "README.md"
BREADTH_BUDGET = 2500  # docs/STANDARD.md §3: a track report, at most 2,500 words outside folds


def test_breadth_visible_text_within_its_budget():
    assert visible_words(BREADTH.read_text(encoding="utf-8")) <= BREADTH_BUDGET


DEPTH = REPO / "docs" / "depth" / "README.md"
DEPTH_BUDGET = 2500  # docs/STANDARD.md §3: a track report, at most 2,500 words outside folds
LEDGER = REPO / "docs" / "depth" / "EXPERIMENTS.md"
LEDGER_BUDGET = 18000  # Dan, 8 Nov (was 15,000, finishing-pass brief D2): the cards' Result tables cannot fit 15,000


def test_depth_visible_text_within_its_budget():
    assert visible_words(DEPTH.read_text(encoding="utf-8")) <= DEPTH_BUDGET


def test_ledger_visible_text_within_its_budget():
    assert visible_words(LEDGER.read_text(encoding="utf-8")) <= LEDGER_BUDGET


def test_breadth_figures_take_their_captions_from_the_store():
    """Every figure on the breadth page is followed by its {{caption|set/stem}} or {{caption_short|set/stem}} in the
    template (no bare "Fig. N.")."""
    tpl = (REPO / "docs" / "breadth" / "README.template.md").read_text(encoding="utf-8")
    figs = re.findall(r"!\[[^\]]*\]\(\.\./\.\./figures/([\w/-]+)/([\w-]+)\.png\)\n\n\{\{caption(?:_short)?\|([\w/-]+)/([\w-]+)\}\}",
                      tpl)
    assert len(figs) == len(re.findall(r"!\[[^\]]*\]\(\.\./\.\./figures/", tpl))
    assert all(a == c and b == d for a, b, c, d in figs)
    assert "*Fig. " not in tpl


def test_alt_texts_are_unique():
    alts = re.findall(r"!\[([^\]]*)\]\(", README.read_text(encoding="utf-8"))
    assert len(alts) == len(set(alts)), sorted(a for a in alts if alts.count(a) > 1)


def test_every_figure_takes_its_caption_from_the_store():
    """In the template, each figure of a set (but the key, which the paragraph above it explains) is followed by its
    {{caption|set/stem}}, or by its {{caption_short|set/stem}} (readability brief, 8 Nov): one caption per PNG and
    length, the same on every page."""
    from bridge_jspace.figkit import layout as L

    lines = [ln for ln in TEMPLATE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    bad = []
    for i, ln in enumerate(lines):
        m = re.fullmatch(r"\{\{fig\|([\w-]+)\}\}", ln.strip())
        img = re.match(r"!\[[^\]]*\]\(figures/([\w/-]+)/([\w-]+)\.png\)", ln.strip())
        if m:
            want = f"common/readme/{L.path('common/readme', m.group(1)).stem}"
        elif img and img.group(2) != "00_key":
            want = f"{img.group(1)}/{img.group(2)}"
        else:
            continue
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""  # a figure inside a list item is indented
        if not nxt.startswith(("{{caption|" + want + "}}", "{{caption_short|" + want + "}}")):
            bad.append(want)
    assert not bad, bad


# The root README and the two track reports share one skeleton (docs/STANDARD.md §3): the same `##` sections in the
# same order. A track report may group its findings under `## Part …` headings instead of `## Findings`.
SKELETON = ["TL;DR", "Setup", "Findings", "What we predicted, and what happened", "Where it does not hold",
            "How we checked", "Related work and what is new", "Open questions", "Reproduce", "Repository guide"]  # fmt: skip
SKELETON_PAGES = {"README.md": False, "docs/depth/README.md": True, "docs/breadth/README.md": True}


def sections(text: str, track: bool) -> list[str]:
    """The page's `##` headings outside code fences, a track's `## Part …` headings read as one "Findings"."""
    text = re.sub(r"(?ms)^```.*?^```", "", text)
    out = []
    for h in re.findall(r"(?m)^## (.+?)\s*$", text):
        h = "Findings" if track and h.startswith("Part ") else h
        h = re.sub(r"^(What|How) I ", r"\1 we ", h) if track else h  # a single-author track report says I (§7.7)
        if not out or out[-1] != h:
            out.append(h)
    return out


@pytest.mark.parametrize("page", SKELETON_PAGES)
def test_page_follows_the_shared_skeleton(page):
    assert sections((REPO / page).read_text(encoding="utf-8"), SKELETON_PAGES[page]) == SKELETON


def test_parts_count_as_one_findings_section():
    text = "## TL;DR\n## Part I. A\n## Part II. B\n## Setup\n"
    assert sections(text, track=True) == ["TL;DR", "Findings", "Setup"]
    assert sections(text, track=False) == ["TL;DR", "Part I. A", "Part II. B", "Setup"]
    assert sections("## How I checked\n## What I predicted, and what happened\n", track=True) == [
        "How we checked", "What we predicted, and what happened"]


# data/figures/lenses.csv (scripts/lens_csv.py): every row traces to a file that exists, and every pass@10 is the cell
# its source names.
LENSES_CSV = REPO / "data/figures/lenses.csv"


def lens_rows() -> list[dict]:
    with LENSES_CSV.open() as f:
        return list(csv.DictReader(f))


def test_lens_keys_unique_and_every_model_has_a_kind_and_a_quality():
    rs = lens_rows()
    keys = [r["key"] for r in rs]
    assert len(keys) == len(set(keys))
    for m in {r["model"] for r in rs}:
        assert f"lens.{m}.kind" in keys and f"lens.{m}.passk" in keys, m


@pytest.mark.parametrize("r", lens_rows(), ids=lambda r: r["key"])
def test_lens_source_exists_or_not_measured(r):
    if r["value"] == "not measured":
        assert r["source"] == ""
        return
    path = r["source"].split(" | ")[0]
    assert path and (REPO / path).exists(), r["source"]


@pytest.mark.parametrize("r", [r for r in lens_rows() if r["unit"].startswith("pass@10") and r["value"] != "not measured"],
                         ids=lambda r: r["key"])  # fmt: skip
def test_lens_pass_at_10_is_the_named_cell(r):
    path, field = r["source"].split(" | ")
    want = dict(kv.split("=") for kv in field.split(", "))
    with (REPO / path).open() as f:
        cells = [d["pass_at_k"] for d in csv.DictReader(f) if all(d[k] == v for k, v in want.items())]
    assert len(cells) == 1 and f"{float(cells[0]):.3f}" == r["value"]
