"""docs/writeup/examples.md (scripts/writeup_examples.py): current, every cited path exists, nothing quoted from the
multi-hop sets the repo keeps out, and its prose passes the write-up's terms."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from scripts import check_figure_terms as CT  # noqa: E402
from scripts import writeup_examples as WE  # noqa: E402

TEXT = WE.OUT.read_text() if WE.OUT.exists() else ""
PATH = re.compile(r"`((?:data|results|docs|scripts)/[^`\s]+)`")


def test_the_file_is_current():
    try:
        WE.RC.tokenizer(WE.MODEL)
    except Exception as e:  # the pinned tokenizer is downloaded once; offline without it, skip
        pytest.skip(f"pinned tokenizer unavailable: {e}")
    assert WE.build() == TEXT, "docs/writeup/examples.md is stale: run scripts/writeup_examples.py"


def test_every_cited_path_exists():
    paths = PATH.findall(TEXT)
    assert paths
    for p in paths:
        assert (REPO / p).exists(), p


def test_nothing_from_the_withheld_sets():
    for p in PATH.findall(TEXT):
        assert not p.startswith(WE.RESTRICTED), f"a withheld set cited as a source: {p}"
    for prefix in WE.RESTRICTED:  # where a withheld set exists locally, none of its passages appears
        for f in sorted(REPO.glob(prefix + "*")):
            files = [f] if f.is_file() else sorted(f.rglob("*.jsonl"))
            for jf in files:
                for line in jf.read_text().splitlines():
                    ctx = json.loads(line).get("context") if line.strip() else None
                    for sent in re.split(r"(?<=[.!?])\s", ctx or ""):
                        assert len(sent) < 40 or sent not in TEXT, f"{jf}: {sent[:60]!r}"


def test_the_prose_passes_the_terms_check():
    hits = [(k, term) for k, t in CT.examples_prose(TEXT) for term, rx in {**CT.RETIRED, **CT.WRITEUP_RETIRED}.items()
            if re.search(rx, t)]  # fmt: skip
    assert hits == []


def test_prose_excludes_code_and_fences():
    prose = dict(CT.examples_prose("a `x_y` b\n```text\nwrite this\n```\nafter"))
    assert prose == {1: "a  b", 5: "after"}
