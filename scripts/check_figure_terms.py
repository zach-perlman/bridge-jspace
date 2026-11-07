"""Retired terms in the READMEs' words (the figures' own words are checked by styles-plot against plotstyle.toml).

Fails (exit 1, one line per hit) when:
- a retired term (RETIRED: "first-mentioned", "part removed", "ablation", question numbers, run ids, UTC stamps) is in
  a figure alt text or a "*Fig. N.*" caption of docs/depth/README.md and its template, or the canonical lines of
  docs/archive/drafts/readme_v5_captions.md;
- a term the joint story leaves to the two reports (JOINT_RETIRED, Dan 27 Oct: M, K, final, J-part, pointer, test ids,
  "stated", ...) is in the root README.md's visible text (HTML comments, code spans and link targets left out);
- an internal id (README_IDS, Dan 28 Oct: 47.x, Z1, C0, x0_necessity, rung 6, batch, amendment) is in
  docs/depth/README.md's visible text, except its "where things live" line.

uv run python scripts/check_figure_terms.py              # the READMEs
uv run python scripts/check_figure_terms.py --examples   # docs/writeup/examples.md's prose (RETIRED + WRITEUP_RETIRED)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

REPO = Path(__file__).resolve().parents[1]
RETIRED = {
    "first-mentioned": r"(?i)\bfirst[- ]mentioned\b",
    # Dan's v6 iteration 2 (28 Oct ~15:40) labels Fig. 5's grey bars "position, a random part removed": that one stays
    "part removed": r"(?i)(?<!random )\bparts? removed\b",
    "ablation": r"(?i)\bablat(?:e|ed|es|ing|ion|ions)\b",
    "Q45": r"\bQ45(?:\.\d+)?\b",
    "run id": r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b",
    "run stamp": r"\b\d{8}T\d{6}Z\b",
}
CAPTION_FILES = (REPO / "docs" / "depth" / "README.md", REPO / "docs" / "depth" / "README.template.md")
CAPTIONS_DRAFT = REPO / "docs" / "archive" / "drafts" / "readme_v5_captions.md"
ROOT_README = REPO / "README.md"
JOINT_RETIRED = {
    # a lone capital M or K (the two reports' final codes), also inside "M − K" / "M-K"
    "M / K": r"(?<![\w'’.])[MK](?![\w'’])",
    "PK / TK": r"\b[PT]K\b",
    "chain code": r"\b[PMTKAN]\s*(?:->|→)\s*[PMTKAN]\b",
    "RM / MM": r"\b(?:RM|MM)\b",
    # Dan ~19:15: "lookup answer" replaces "stated answer"; "remove from the patch" replaces "remove from the change";
    # every joint figure counts in pp, never "x 100"
    "stated": r"(?i)\bstated\b",
    "from the change": r"(?i)\bfrom the change\b",
    "x 100": r"(?<![\w.])[x×]\s?100\b",
    "in-context read": r"(?i)\bin-context read",
    "final": r"(?i)\bfinals?\b",
    "J-part": r"(?i)\bJ-parts?\b",
    "J++ part": r"J\+\+ parts?\b",
    "entity code": r"(?i)\bentity codes?\b",
    "pointer": r"(?i)\bpointers?\b",
    "test id": r"\bx?\d{2}[a-z]\b|\bQ\d+(?:\.\d+)?\b",
    "GAP": r"\bGAP\b",
    "degree sign": r"°",
    "X0": r"(?i)\bx0\b",
    "paper10": r"(?i)\bpaper10",
    "s = n": r"(?<![\w'’])s\s*=\s*\d",
}


# Dan's restructure brief (28 Oct 22:20), §6: no internal ids in the README body (prose, headings, captions): batch test ids (47.x, 49.x,
# 51.x), Zach's test names (Z1-Z3), scene-set codes (C0-C2, P2-L0), run names (x0_necessity), the ladder's "rung 6",
# "batch", "amendment". Ids live only in the Appendix's "where things live" line and in source comments.
README_IDS = {
    "test id": r"\b(?:4\d|5[0-9])\.\d+[a-z]?\b(?![\d%])",
    "Zach's test name": r"\bZ\d\b",
    "scene-set code": r"\bC[0-9]\b|\bP\d-L\d\b",
    "run name": r"\bx\d+(?:[a-z]+\b|[a-z]?_\w+)",
    "rung number": r"(?i)\brungs? \d",
    "batch": r"(?i)\bbatch(?:es)?\b",
    "amendment": r"(?i)\bamendments?\b",
}
README_PAGE = REPO / "docs" / "depth" / "README.md"


def readme_body_lines(text: str) -> list[tuple[str, str]]:
    """(where, line) for the README's visible lines: source comments and link targets left out, and the Appendix's
    "where things live" line (the one place for paths and ids) skipped."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"(\]\()[^)]*\)", r"\1)", text)
    return [(f"{README_PAGE.name} l.{i}", line) for i, line in enumerate(text.splitlines(), 1)
            if line.strip() and "where things live" not in line]  # fmt: skip


def readme_ids(lines: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(where, line, kind) for each internal id on a README body line."""
    return [(where, line, kind) for where, line in lines for kind, rx in README_IDS.items() if re.search(rx, line)]


def retired(texts: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(where, text, term) for each text holding a retired term."""
    return [(where, text, term) for where, text in texts for term, rx in RETIRED.items() if re.search(rx, text)]


def joint_retired(texts: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(where, text, term) for each text holding a term the joint story retires."""
    return [(where, text, term) for where, text in texts for term, rx in JOINT_RETIRED.items() if re.search(rx, text)]


def root_readme_texts() -> list[tuple[str, str]]:
    """The root README's lines as a reader sees them: HTML comments (the source keys), code spans and link targets
    left out, link texts and alt texts kept."""
    if not ROOT_README.exists():
        return []
    text = re.sub(r"<!--.*?-->", "", ROOT_README.read_text(), flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"(\]\()[^)]*\)", r"\1)", text)  # [text](target) -> [text]()
    return [(f"{ROOT_README.name} l.{i}", line.strip()) for i, line in enumerate(text.splitlines(), 1) if line.strip()]


def caption_texts() -> list[tuple[str, str]]:
    """The figure alt texts and '*Fig. N.*' lines of the README and its template (HTML comments left out), and the
    canonical lines of the captions draft."""
    out = []
    for path in CAPTION_FILES:
        if not path.exists():
            continue
        text = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
        out += [(f"{path.name}: alt text", a) for a in re.findall(r"!\[([^\]]*)\]\((?:\.\./)*figures/", text)]
        out += [(f"{path.name}: caption", line) for line in text.splitlines() if re.match(r"\*Fig\. \w+\.\*", line)]
    if CAPTIONS_DRAFT.exists():
        out += [(CAPTIONS_DRAFT.name, line.split(": ", 1)[1]) for line in CAPTIONS_DRAFT.read_text().splitlines()
                if line.startswith("- canonical ") and ": " in line]  # fmt: skip
    return out


# The LessWrong write-up's figures (brief 6 Nov, rule 6): the post's terms only. No people's names, no internal ids
# (x47, note 62, jsuite_v4, amendment, cand2), "lookup" not "stated", "swap" not "write" for the address.
WRITEUP_RETIRED = {
    "a person's name": r"\b(?:Zach|Dan)\b",
    "experiment id": r"\bx\d{2}(?:\.\d+)?\b",
    "note number": r"(?i)\bnotes? \d+",
    "suite id": r"(?i)\bjsuite",
    "amendment": r"(?i)\bamendments?\b",
    "candidate id": r"(?i)\bcand\d",
    "stated": r"(?i)\bstated\b",
    "write": r"(?i)\b(?:write|writes|writing|written|wrote)\b",
}


EXAMPLES = REPO / "docs" / "writeup" / "examples.md"


def examples_prose(text: str) -> list[tuple[int, str]]:
    """docs/writeup/examples.md's prose, by line number: fenced blocks and inline code (verbatim prompts, model output,
    paths and ids) removed, so only the words the write-up adds are checked."""
    out, fence = [], None
    for k, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^(`{3,})", line)
        if m:
            fence = None if fence and m.group(1).startswith(fence) else (fence or m.group(1))
            continue
        if fence is None:
            out.append((k, re.sub(r"`[^`]*`", "", line)))
    return out


def examples_main() -> int:
    terms = {**RETIRED, **WRITEUP_RETIRED}
    hits = [(k, t, term) for k, t in examples_prose(EXAMPLES.read_text()) for term, rx in terms.items() if re.search(rx, t)]
    for k, text, term in hits:
        print(f"examples.md:{k}: {term!r} in {text.strip()[:80]!r}")
    print(f"check_figure_terms --examples: {len(hits)} banned term(s) in the prose of {EXAMPLES.relative_to(REPO)}")
    return 1 if hits else 0


PAGES = (ROOT_README, README_PAGE, REPO / "docs" / "breadth" / "README.md")
IDS_ONLY = {k: RETIRED[k] for k in ("run id", "run stamp")}  # not words: ids in captions stay a check of their own


def vocabulary_banned() -> list[tuple[str, re.Pattern]]:
    """(the term to use, the pattern) for every banned variant in plotstyle.toml [[terms.banned]]: the one word list
    the figures and these pages share (Dan, 8 Nov, Q3). A ban marked scope = "figures" binds figure labels only (prose
    may say a passage states a fact, or that code was written); the patterns are compiled by styles-plot itself."""
    import tomllib

    import styles_plot as sp

    toml = tomllib.loads((REPO / "plotstyle.toml").read_text())["terms"]["banned"]
    banned = sp.load(REPO / "plotstyle.toml").banned
    assert len(toml) == len(banned), "plotstyle.toml [[terms.banned]] and styles-plot's list differ"
    return [(b.use, b.compiled) for t, b in zip(toml, banned, strict=True) if t.get("scope") != "figures"]


def visible(text: str) -> str:
    """A page's words as a reader sees them, less what quotes another text: HTML comments (source keys), code spans,
    link targets and verbatim quotes ("...", “...”), which keep their words and carry a bracketed gloss instead."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"(\]\()[^)]*\)", r"\1)", text)
    text = re.sub(r"\"[^\"\n]*\"|“[^”\n]*”", "", text)
    return re.sub(r"\[pointers?: [^\]]*\]", "", text)  # the gloss a quote carries ("[pointer: the address]")


def vocabulary_hits() -> list[tuple[str, str, str]]:
    """(where, line, the term to use) for every banned variant on the three READMEs' visible lines."""
    banned = vocabulary_banned()
    out = []
    for page in PAGES:
        if not page.exists():
            continue
        for i, line in enumerate(visible(page.read_text()).splitlines(), 1):
            out += [(f"{page.relative_to(REPO)} l.{i}", line.strip(), use) for use, rx in banned if rx.search(line)]
    return out


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if "--examples" in args:
        return examples_main()
    word_hits = vocabulary_hits()
    id_caption_hits = [(w, t, k) for w, t in caption_texts() for k, rx in IDS_ONLY.items() if re.search(rx, t)]
    id_hits = readme_ids(readme_body_lines(README_PAGE.read_text())) if README_PAGE.exists() else []
    for where, text, use in word_hits:
        print(f"{where}: use {use!r}: {text[:160]!r}")
    for where, text, kind in id_caption_hits + id_hits:
        print(f"{where}: {kind!r} in {text[:160]!r}")
    print(f"check_figure_terms: {len(word_hits)} banned variant(s) of plotstyle.toml on the READMEs; "
          f"{len(id_caption_hits) + len(id_hits)} internal id(s) in the depth README")  # fmt: skip
    return 1 if word_hits or id_caption_hits or id_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
