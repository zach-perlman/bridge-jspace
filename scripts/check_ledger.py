"""check_ledger: docs/depth/EXPERIMENTS.md, the ledger of every opened test (Dan, 29 Oct ~01:10; cards since 01:15), is
well formed:

- every repo path it cites exists in the checkout;
- every entry (a '### ' heading) carries a unique stable anchor, and every internal link resolves;
- every card has the README Part I fields in order (Question, Why we asked, Data, Method, Rule fixed in advance,
  Result, Read, Caveats); an entry still running ('running)' in its heading) is a stub: Question, Status, Where used;
- every card's first line is its status tag (Dan's restructure brief, 29 Oct 08:55): `in README`, `changes README` or
  `ledger only`, then optionally `below gate: <models>`, then optionally the italic "Used in" text;
- every number's source comment resolves: `<value><!-- src: <path> | <part> :: ... :: <value> -->` (in a table row
  the separator is written `\\|`): the path exists, all parts stand on one line of that file, and the last part is the
  text right before the comment, so a number cannot drift from the file it was copied from;
- every card has one figure, right after its Method (before its rule; Dan's restructure brief, 29 Oct 08:55), with an
  italic caption and its file present; internal links resolve to any <a id> on the page (cards and the Appendix);
- the coverage table equals scripts/ledger_coverage.py's output (the committed matrix).

Exit 1 with one line per problem.

uv run python scripts/check_ledger.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
LEDGER = REPO / "docs" / "depth" / "EXPERIMENTS.md"
FIELDS = ("Question", "Why we asked", "Data", "Method", "Rule, fixed in advance", "Result", "Read", "Caveats")
STUB_FIELDS = ("Question", "Status", "Where used")
# a repo path: a top-level folder of the checkout followed by a path
PATH = re.compile(r"\b((?:results|docs|jobs|scripts|figures|tests|data)/[\w./-]*[\w/])")
ANCHOR = re.compile(r'<a id="([a-z0-9-]+)"></a>\s*$')
# the status tag line under a card's heading (Dan, 29 Oct 08:55)
TAGS = ("in README", "changes README", "ledger only")
TAG_LINE = re.compile(r"^`(" + "|".join(TAGS) + r")`(?: `below gate: [^`]+`)?(?: \*Used in: [^*]+\*)?$")
SRC = re.compile(r"<!-- src: ([^|\\]+?) \\?\| (.+?) -->")


def cited_paths(text: str) -> list[str]:
    """Paths in the visible text (comments left out) and every source comment's file."""
    visible = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return sorted(set(PATH.findall(visible)) | {m.group(1).strip() for m in SRC.finditer(text)})


def entries(text: str) -> list[tuple[str, str]]:
    """(heading line, body) for every '### ' entry."""
    return [(m.group(1), m.group(2)) for m in re.finditer(r"^### ([^\n]+)\n(.*?)(?=^##+ |\Z)", text, re.M | re.S)]


def source_problems(text: str, repo: Path = REPO) -> list[str]:
    out, files = [], {}
    for m in SRC.finditer(text):
        path, parts = m.group(1).strip(), [p.strip() for p in m.group(2).split(" :: ")]
        p = repo / path
        if not p.is_file():
            out.append(f"source file missing: {path}")
            continue
        lines = files.setdefault(path, p.read_text(encoding="utf-8").splitlines())
        if not any(all(part in line for part in parts) for line in lines):
            out.append(f"not on one line of {path}: {parts}")
        if not text[: m.start()].endswith(parts[-1]):
            out.append(f"the value before the comment is not {parts[-1]!r} ({path})")
    return out


def figure_problems(head: str, body: str, repo: Path = REPO) -> list[str]:
    """A card's one figure (Dan 01:15): right after its Method, before its rule (Dan, 29 Oct 08:55), its file present
    (the link is written from docs/depth/), an italic caption on the next line."""
    lines = body.splitlines()
    imgs = [i for i, line in enumerate(lines) if re.match(r"^!\[[^\]]+\]\([^)]+\)", line)]
    if len(imgs) != 1:
        return [f"{len(imgs)} figures in: {head}"]
    i = imgs[0]
    method = next(k for k, line in enumerate(lines) if line.startswith("- **Method.**"))
    rule = next(k for k, line in enumerate(lines) if line.startswith("- **Rule, fixed in advance.**"))
    out = [] if method < i < rule else [f"the figure is not right after the method in: {head}"]
    target = re.match(r"^!\[[^\]]+\]\(([^)]+)\)", lines[i]).group(1)  # type: ignore[union-attr]
    if not (LEDGER.parent / target).resolve().exists():
        out.append(f"figure file missing: {target}")
    if i + 1 >= len(lines) or not re.fullmatch(r"\*[^*].*\*", lines[i + 1].strip()):
        out.append(f"no italic caption under the figure in: {head}")
    return out


def problems(text: str, repo: Path = REPO) -> list[str]:
    out = [f"missing path: {p}" for p in cited_paths(text) if not (repo / p).exists()]
    anchors = []
    for head, body in entries(text):
        m = ANCHOR.search(head)
        if not m:
            out.append(f"no anchor: {head}")
        else:
            anchors.append(m.group(1))
        want = STUB_FIELDS if re.search(r"\brunning\)", head) else FIELDS
        found = re.findall(r"^- \*\*(" + "|".join(re.escape(f) for f in want) + r")\.\*\*", body, re.M)
        if found != list(want):
            out.append(f"fields {found} in: {head}")
        if want is FIELDS:
            first = next((line for line in body.splitlines() if line.strip()), "")
            if not TAG_LINE.match(first):
                out.append(f"no status tag line under the heading of: {head}")
            out += figure_problems(head, body, repo)
    every = re.findall(r'<a id="([a-z0-9-]+)"></a>', text)
    out += [f"duplicate anchor: {a}" for a in sorted({a for a in every if every.count(a) > 1})]
    links = set(re.findall(r"\]\(#([a-z0-9-]+)\)", text))
    out += [f"link to a missing anchor: #{a}" for a in sorted(links - set(every))]
    return out + source_problems(text, repo)


def coverage_problems(text: str) -> list[str]:
    """The coverage table between its markers must equal scripts/ledger_coverage.py's output (the committed matrix)."""
    from scripts import ledger_coverage as LC

    m = re.search(r"<!-- coverage:start[^>]*-->\n(.*?)\n<!-- coverage:end -->", text, re.S)
    if not m:
        return ["no coverage table between <!-- coverage:start --> and <!-- coverage:end -->"]
    return [] if m.group(1).strip() == LC.table().strip() else ["the coverage table differs from the matrix (rerun "
                                                                 "scripts/ledger_coverage.py)"]  # fmt: skip


def main() -> int:
    text = LEDGER.read_text()
    bad = problems(text) + coverage_problems(text)
    for line in bad:
        print(line)
    print(f"check_ledger: {len(entries(text))} entries, {len(cited_paths(text))} paths, "
          f"{len(SRC.findall(text))} sourced numbers, {len(bad)} problem(s)")  # fmt: skip
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
