"""readme_build: markers render from a synthetic grid; README.md is the rendered template; the template types no result."""

from __future__ import annotations

import csv
import io
import re

import pytest

from scripts import cross_model_grid as G
from scripts import readme_build as B

COLS = ["model", "finding", "setting", "lens", "n", "value", "95% CI", "chance or control level", "verdict", "rule id",
        "spec commit", "result path"]  # fmt: skip
F4 = G.FINDING["f4"].name
CTL = "chance 20%; blocked in every attention layer; the off-path sentence hidden instead keeps {o}% [99, 100]; hidden " \
      "in every DeltaNet layer instead: {d}%"  # fmt: skip


def _row(model, setting, n, value, ci, verdict, o=100, d=100):
    return {"model": model, "finding": F4, "setting": setting, "lens": "none (lens-free)", "n": "" if n is None else str(n),
            "value": f"{value} %" if value is not None else "", "95% CI": ci, "chance or control level": CTL.format(o=o, d=d),
            "verdict": verdict, "rule id": "late-read", "spec commit": "-", "result path": f"results/attn_knockout/{model}/rows.jsonl"}  # fmt: skip


@pytest.fixture
def book(tmp_path):
    rows = [
        _row("Qwen3.6-27B", "draw 2", 300, 7.3, "[4.9, 10.9]", "holds"),
        _row("Qwen3.6-27B", "long context", 178, 25.8, "[20.0, 32.7]", "fails (more than 20% right)"),
        _row("Olmo-Hybrid-7B", "draw 2", 100, 7.0, "[3.4, 13.7]", "holds", d=100),
        _row("Olmo-Hybrid-7B", "table", 24, 0.0, "[0.0, 13.8]", "fails (the DeltaNet layers matter)", d=88),
        _row("Gemma 4 31B-it", "draw 2", 300, 22.0, "[17.0, 27.0]", "fails (more than 20% right)", o=98),
        _row("Qwen3-32B", "draw 2", None, None, "", "missing (qwen3_32b_x is running in the queue)"),
    ]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
    (tmp_path / "grid.csv").write_text(buf.getvalue())
    return B.Book(tmp_path, head="abc1234")


def test_cell_markers(book):
    assert book.value("f4", "27b", "draw 2") == "7%"
    assert book.ci("f4", "27b", "draw 2") == "[5, 11]"
    assert book.n("f4", "27b", "draw 2") == "300"
    assert book.ctl("f4", "DeltaNet") == "88-100%"
    assert book.ctl("f4", "another sentence", "gemma", "draw 2") == "98%"


def test_holds_and_confidence(book):
    # Olmo-Hybrid's failing table has 24 items: left out of the count, so it holds; 27B mixed, Gemma fails; 32B not judged
    assert book.holds("f4") == "1 of 3"
    conf = book.conf("f4")
    assert conf.startswith("open (holds 1 of 3")
    assert "Olmo-Hybrid: table (24 items) fails" in conf


def test_table_rows_and_untested(book):
    rows = book.table("f4", ["draw 2", "table"])
    text = "\n".join(rows)
    assert "| Qwen3.6-27B | scene set 2 | 7% [5, 11] | 300 | holds | 1 of 2 hold; long context: fails |" in text
    assert "table (24 items): fails" in text
    assert "32B (still running)" in rows[-1] and rows[-1].startswith("Not tested: ")
    assert [r.split(" | ")[0] for r in rows if r.startswith("| Q") or r.startswith("| O") or r.startswith("| G")] == [
        "| Qwen3.6-27B",
        "| Olmo-Hybrid-7B",
        "| Gemma 4 31B",
    ]  # hybrids first, then attention-only


def test_render_markers(book):
    t = "<!-- grid: x -->\nA {{v|f4|27b|draw 2}} {{ci|f4|27b|draw 2}}, {{q|36}} points, {{head}}.\n{{table|f4|draw 2}}"
    out = B.render(t, book)
    assert "A 7% [5, 11], 36 points, abc1234." in out
    assert "| Model | Setting |" in out


# ---------------------------------------------------------------- the repo's README


def test_readme_is_the_rendered_template():
    text = B.TEMPLATE.read_text()
    grid = B.pinned_grid(text)
    if not (grid / "grid.csv").exists():
        pytest.skip("the pinned grid is not in results/")
    readme = (B.REPO / "README.md").read_text()
    head = re.search(r"Built at (\w+) from", readme)
    assert head, "README has no 'Built at <commit>' line"
    assert readme == B.render(text, B.Book(grid, head=head.group(1))), "README.md differs: run scripts/readme_build.py"


ALLOWED = re.compile(r"(≤|≥|at least|at most|under|over)\s*\d+%")


def test_template_types_no_result_number():
    """Outside markers the template may state rule bars (≤ 5%, at least 20%), never a result in % or points."""
    text = B.MARK.sub("", B.TEMPLATE.read_text())
    text = ALLOWED.sub("", text)
    typed = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|points?\b)", text)
    assert not typed, f"typed numbers in the template (use a marker or {{{{q|...}}}}): {typed}"


MAX_BODY_WORDS = 1500  # Dan, 25 Oct (README v2): the main body, before the appendices, at most 1,500 words
CODES = re.compile(
    r"\bX[0-6]b?\b|\bAlf\b|\bjwo?\b|\bPP\b|\bPM\b|\bJdep\b|\bRdep\b| C |k =|\bcf\b|\bC[0-2]\b|\b[Ss]wap [12]\b"
    r"|\bone-pick\b|\btwo-pick\b|\bedit(?:ed)?\b"
)


def body_text() -> str:
    return (B.REPO / "README.md").read_text().split("## Appendix A")[0]


def body_words(text: str) -> int:
    """The prose words of the main body: image links, comments and table rows (data, not prose) left out."""
    prose = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("|"))
    return len(re.sub(r"!\[[^\]]*\]\([^)]*\)|<!--.*?-->", " ", prose, flags=re.S).split())


def test_readme_body_fits_the_word_budget():
    assert (n := body_words(body_text())) <= MAX_BODY_WORDS, n


def test_readme_body_has_no_internal_codes():
    """Internal run codes and the banned terms appear only in Appendix C, which maps sections to runs (Dan, 25 Oct)."""
    body = re.sub(r"<!--.*?-->", "", (B.REPO / "README.md").read_text().split("## Appendix C")[0], flags=re.S)
    assert not CODES.findall(body), CODES.findall(body)
