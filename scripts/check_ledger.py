"""check_ledger: docs/depth/EXPERIMENTS.md, the ledger of every opened test (Dan, 29 Oct ~01:10; cards since 01:15), is
well formed:

- every repo path it cites exists in the checkout;
- every entry (a '### ' heading) carries a unique stable anchor, and every internal link resolves;
- every card has the README Part I fields in order (Question, Why we asked, Data, Method, Rule fixed in advance,
  Result, Read, Caveats); an entry not completed in the sprint ('not completed in the sprint)' or 'running)' in its heading) is a stub: Question, Status, Where used
  (batch 53's stubs quote their rule between the question and the status);
- every card's first line is its status tag (Dan's restructure brief, 29 Oct 08:55): `in README`, `changes README` or
  `ledger only`, then optionally `below gate: <models>`, then optionally the italic "Used in" text;
- every number's source comment resolves: `<value><!-- src: <path> | <part> :: ... :: <value> -->` (in a table row
  the separator is written `\\|`): the path exists, all parts stand on one line of that file, and the last part is the
  text right before the comment, so a number cannot drift from the file it was copied from;
- internal links resolve to any <a id> on the page (cards and the Appendix); the cards' figures are not checked here (the
  ledger figures were retired on 7 Nov; every doc's figure links are checked by tests/test_figure_layout.py);
- the coverage table equals scripts/ledger_coverage.py's output (the committed matrix), and the verdict tables (the
  coverage map as markdown) its verdict_tables().

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
# batch 53's stubs (Dan, 29 Oct 09:30) quote their rule, fixed before any run, between the question and the status
STUB_RULE_FIELDS = ("Question", "Rule, fixed in advance", "Status", "Where used")
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


COLUMN_MODELS = ("9B", "27B", "Muse", "Lightning", "122B")  # the 122B checked like the others (Dan 12:50)
# a cell that says the model has no result here (Dan's grey labels, the tables' words for a missing cell)
NO_RESULT = ("not ", "running", "pending", "dropped", "read pending", "see the readme", "–", "no outcomes")


def problems(text: str, repo: Path = REPO) -> list[str]:
    # figures are not sources: their links are checked with every doc's (tests/test_figure_layout.py)
    out = [f"missing path: {p}" for p in cited_paths(text) if not p.startswith("figures/") and not (repo / p).exists()]
    anchors = []
    for head, body in entries(text):
        m = ANCHOR.search(head)
        if not m:
            out.append(f"no anchor: {head}")
        else:
            anchors.append(m.group(1))
        stub = bool(re.search(r"\b(?:running|not completed in the sprint)\)", head))
        want = STUB_FIELDS if stub else FIELDS
        names = STUB_RULE_FIELDS if stub else FIELDS
        found = re.findall(r"^- \*\*(" + "|".join(re.escape(f) for f in names) + r")\.\*\*", body, re.M)
        if found != list(want) and not (stub and found == list(STUB_RULE_FIELDS)):
            out.append(f"fields {found} in: {head}")
        if want is FIELDS:
            first = next((line for line in body.splitlines() if line.strip()), "")
            if not TAG_LINE.match(first):
                out.append(f"no status tag line under the heading of: {head}")
    every =re.findall(r'<a id="([a-z0-9-]+)"></a>', text)
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


def verdict_problems(text: str) -> list[str]:
    """The verdict tables between their markers (the coverage map as markdown, morning brief 30 Oct #1) must equal
    scripts/ledger_coverage.py's verdict_tables()."""
    from scripts import ledger_coverage as LC

    m = re.search(r"<!-- verdicts:start[^>]*-->\n(.*?)\n<!-- verdicts:end -->", text, re.S)
    if not m:
        return ["no verdict tables between <!-- verdicts:start --> and <!-- verdicts:end -->"]
    return [] if m.group(1).strip() == LC.verdict_tables().strip() else ["the verdict tables differ from "
                                                                          "ledger_coverage.verdict_tables()"]  # fmt: skip


def main() -> int:
    text = LEDGER.read_text()
    bad = problems(text) + coverage_problems(text) + verdict_problems(text)
    for line in bad:
        print(line)
    print(f"check_ledger: {len(entries(text))} entries, {len(cited_paths(text))} paths, "
          f"{len(SRC.findall(text))} sourced numbers, {len(bad)} problem(s)")  # fmt: skip
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
