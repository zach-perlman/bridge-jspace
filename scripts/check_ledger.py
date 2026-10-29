"""check_ledger: docs/depth/EXPERIMENTS.md, the ledger of every opened test (Dan, 29 Oct ~01:10), is well formed: every
repo path it cites exists in the checkout, every entry (a '### ' heading) carries a unique stable anchor, every entry
has Dan's five fields in order (Question, Verdict, Key numbers, Where used, Caveats), every internal link resolves, and
the coverage table equals scripts/ledger_coverage.py's output (Dan, 01:15). Exit 1 with one line per problem.

uv run python scripts/check_ledger.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
LEDGER = REPO / "docs" / "depth" / "EXPERIMENTS.md"
FIELDS = ("Question", "Verdict", "Key numbers", "Where used", "Caveats")
# a repo path: a top-level folder of the checkout followed by a path, in backticks or bare
PATH = re.compile(r"\b((?:results|docs|jobs|scripts|figures|tests|data)/[\w./-]*[\w/])")
ANCHOR = re.compile(r'<a id="([a-z0-9-]+)"></a>\s*$')


def cited_paths(text: str) -> list[str]:
    return sorted(set(PATH.findall(text)))


def entries(text: str) -> list[tuple[str, str]]:
    """(heading line, body) for every '### ' entry."""
    return [(m.group(1), m.group(2)) for m in re.finditer(r"^### ([^\n]+)\n(.*?)(?=^##+ |\Z)", text, re.M | re.S)]


def problems(text: str, repo: Path = REPO) -> list[str]:
    out = [f"missing path: {p}" for p in cited_paths(text) if not (repo / p).exists()]
    anchors = []
    for head, body in entries(text):
        m = ANCHOR.search(head)
        if not m:
            out.append(f"no anchor: {head}")
        else:
            anchors.append(m.group(1))
        found = re.findall(r"^- (" + "|".join(FIELDS) + r")\b", body, re.M)
        if found != list(FIELDS):
            out.append(f"fields {found} in: {head}")
    out += [f"duplicate anchor: {a}" for a in sorted({a for a in anchors if anchors.count(a) > 1})]
    links = set(re.findall(r"\]\(#([a-z0-9-]+)\)", text))
    out += [f"link to a missing anchor: #{a}" for a in sorted(links - set(anchors))]
    return out


def coverage_problems(text: str) -> list[str]:
    """The coverage table between its markers must equal scripts/ledger_coverage.py's output (the committed matrix)."""
    from scripts import ledger_coverage as LC

    m = re.search(r"<!-- coverage:start[^>]*-->\n(.*?)\n<!-- coverage:end -->", text, re.S)
    if not m:
        return ["no coverage table between <!-- coverage:start --> and <!-- coverage:end -->"]
    return [] if m.group(1).strip() == LC.table().strip() else ["the coverage table differs from the matrix (rerun "
                                                                 "scripts/ledger_coverage.py)"]  # fmt: skip


def main() -> int:
    bad = problems(LEDGER.read_text()) + coverage_problems(LEDGER.read_text())
    for line in bad:
        print(line)
    print(f"check_ledger: {len(entries(LEDGER.read_text()))} entries, {len(cited_paths(LEDGER.read_text()))} paths, "
          f"{len(bad)} problem(s)")  # fmt: skip
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
