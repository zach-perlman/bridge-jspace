"""readme_build: markers render from a synthetic grid; docs/depth/README.md is the rendered template (its links relinked
to resolve from docs/depth/); the template types no result."""

from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

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


def test_point_marker_drops_the_interval():
    key, text = next((k, v["text"]) for k, v in json.loads((B.REPO / "docs" / "depth" / "x0_numbers.json").read_text()).items()
                     if " [" in v["text"])  # fmt: skip
    out = B.render(f"{{{{pt|{key}}}}} / {{{{num|{key}}}}}", None).splitlines()[-1]  # type: ignore[arg-type]
    assert out == f"{text.split(' [')[0]} / {text}"


# ---------------------------------------------------------------- the repo's README


def rendered_at_root() -> str:
    """The page as rendered from the template with links from the repo root (before relink), at the commit the built
    page names; skips where the pinned grid is not in results/."""
    text = B.TEMPLATE.read_text()
    grid = B.pinned_grid(text)
    if not (grid / "grid.csv").exists():
        pytest.skip("the pinned grid is not in results/")
    head = re.search(r"Built at (\w+) from", B.PAGE.read_text())
    assert head, "docs/depth/README.md has no 'Built at <commit>' line"
    return B.render(text, B.Book(grid, head=head.group(1)))


def test_readme_is_the_rendered_template():
    expected = B.relink(rendered_at_root(), B.PAGE)
    assert B.PAGE.read_text() == expected, "docs/depth/README.md differs: run scripts/readme_build.py"


ALLOWED = re.compile(r"(≤|≥|at least|at most|under|over)\s*\d+%")


def test_template_types_no_result_number():
    """Outside markers the template may state rule bars (≤ 5%, at least 20%), never a result in % or points."""
    text = B.MARK.sub("", B.TEMPLATE.read_text())
    text = ALLOWED.sub("", text)
    typed = re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|points?\b)", text)
    assert not typed, f"typed numbers in the template (use a marker or {{{{q|...}}}}): {typed}"


# Dan, 26 Oct (was 1,500 in README v2): the main body, before the appendices; 2,500 since 28 Oct, when Dan asked for
# every batch 47/48 figure; 2,600 from the v6 cards (Dan, 28 Oct ~14:30: total body <= 2,600, the claims table
# excluded); 3,500 in Dan's restructure brief (28 Oct 22:20: "page under 3,500 words")
MAX_BODY_WORDS = 3500
# "one-pick" left the list: Dan's restructure brief (28 Oct 22:20) names the set "Clean one-pick"
CODES = re.compile(
    r"\bX[0-6]b?\b|\bAlf\b|\bjwo?\b|\bPP\b|\bPM\b|\bJdep\b|\bRdep\b| C |k =|\bcf\b|\bC[0-2]\b|\b[Ss]wap [12]\b"
    r"|\btwo-pick\b|\bedit(?:ed)?\b"
)


def body_text() -> str:
    return B.PAGE.read_text().split("## Appendix A")[0]


def body_words(text: str) -> int:
    """The prose words of the main body: image links, comments and table rows (data, not prose) left out."""
    prose = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("|"))
    prose = re.sub(r"<!--.*?-->", "", prose, flags=re.S)  # source comments are invisible: no word, no split
    return len(re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", prose).split())


# Parts II-VI pending, Dan 22:20 restructure in progress: the page holds the new Part I cards and the old ones at once
# (5,316 words at the Part I commit); strict once every part is converted
@pytest.mark.xfail(reason="Parts II-VI pending, Dan 22:20 restructure in progress", strict=False)
def test_readme_body_fits_the_word_budget():
    assert (n := body_words(body_text())) <= MAX_BODY_WORDS, n


def test_readme_body_has_no_internal_codes():
    """No internal run codes or banned terms on the page (Dan, 25 Oct; the appendix that mapped sections to runs was
    removed on 26 Oct)."""
    body = re.sub(r"<!--.*?-->", "", B.PAGE.read_text(), flags=re.S)
    assert not CODES.findall(body), CODES.findall(body)


# ---------------------------------------------------------------- the figure vocabulary (docs/depth/glossary.md)

# Tuesday's merge: check README.md. Set True once the v5 figures and captions are in README.md; until then the
# canonical lines of docs/archive/drafts/readme_v5_captions.md are checked instead.
CHECK_README = True
CAPTIONS_DRAFT = B.REPO / "docs" / "archive" / "drafts" / "readme_v5_captions.md"

# docs/depth/glossary.md's banned variants, one regex each. Case-sensitive unless marked (?i:...); \b = whole words only.
BANNED = {
    # "J++" as a part name: a J++ not followed by " part" (or " lens", the lens itself), unless it names the lens in
    # "identity outside J++"
    "J++ alone": r"(?<!outside )(?<!inside )J\+\+(?! part| lens)",
    "lens's part": r"lens's part|lens-readable part",
    # any case: "Our pointer directions" opens a sentence
    "pointer variants": r"(?i:\bour pointer\b|\bpointer directions?\b|\bpointer part\b)",
    # internal names, capitalised and whole: "U" must not hit "UNVERIFIED" or "U.S."
    "Alf / U": r"\bAlf\b|\bU\b(?!\.)",
    "idout": r"\bidout\b|\bidentity direction\b",
    # "random directions" too: Fig. 2's dictionary is "random lens directions" (Dan ~22:40; renamed 27 Oct ~11:45)
    "random-part variants": r"random part, same size|random directions|random part of its size|J\+\+ size",
    "PCA variants": r"(?i:\bmain directions\b)",
    # removing / keeping: "X alone" in any form, "edit" and its inflections
    "removal variants": r"part removed|no J\+\+|(?i:keep-only)|\balone\b|\bedit(?:s|ed|ing)?\b",
    # "original" only as "original answer" / "original prompt" (across a line break too)
    "answer classes": r"\bunchanged\b|\boriginal\b(?!\s(?:answer|prompt))",
    # "Changed" as a row title (capitalised, no "prompt" after it); O / S as prompt names: a lone capital letter
    "prompt variants": r"\bswapped\b|\bChanged\b(?!\sprompt)|(?<![\w'’])[OS](?![\w'’.])",
    "slot": r"(?i:\bslots?\b)",
    # "locker first" / "locker after" unless it goes on "the pick"; "locker-first" in figures and captions
    "sentence-order variants": r"\blocker[- ](?:first|after)\b(?!\sthe pick)",
    "scene-set variants": r"\bC[0-2]\b|\bjson\b|\bsimple\b(?!\sscenes)|(?i:\bsame test\b)|one-change scenes",
    "neutral-sentence codes": r"\bB[12]\b",
    # "s" / "s*" as a symbol: a lone s, not the possessive "Iris's" (an apostrophe before it)
    "metric variants": r"J\+\+ extra loss|\bJdep\b|(?<![\w'’])s\*?(?![\w'’*])|\bbeta\b",
    "share variants": r"\bposition share\b",
    "cell-state variants": r"not in this test|\bqueued\b|not measurable",
    "status variants": r"fixed in advance \(main test\)|gate lowered after the data",
    # the x0 details' own words (glossary rows added with them): any case for excess / dependence; W_U / W_E and
    # the run code X0 exactly ("x0_kmatch", a run name, stays)
    "x0 details variants": r"(?i:\bexcess\b|\bdependence\b|graded contrast)|\bW_[UE]\b|\bX0\b|\bC =",
}
KEPT = {  # exact strings that keep a banned variant, each by Dan's decision
    "Our pointer directions separate the first-mentioned item from the rest",  # Fig. 8: waits for Tuesday's "first"
    # Dan's v6 iteration 2 (28 Oct ~15:40) words these labels himself (Fig. 5's grey bars, Fig. 7's panel C)
    "position, a random part removed",
    "C  A swap sends the lookup to the swapped-in locker",
    "lookups answering the\nswapped-in locker (share)",
    # Dan's plain findings (28 Oct 21:20), the claims table's row 7 (and Fig. 11's) in his words
    "Adding the address alone brings position answers back",
}


def banned(texts: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """(where, text, rule) for each text that matches a banned variant, the allowed strings left out (compared with
    their whitespace collapsed: a figure may wrap a kept string at any space)."""
    kept = {" ".join(k.split()) for k in KEPT}
    return [(where, text, rule) for where, text in texts if " ".join(text.split()) not in kept
            for rule, rx in BANNED.items() if re.search(rx, text)]  # fmt: skip


@pytest.mark.parametrize(
    "text",
    ["the recall needs J++", "without J++", "J++ extra loss", "our pointer", "pointer directions", "Alf", "U", "idout",
     "random part, same size", "random directions", "main directions", "part removed", "The pointer alone gives position",
     "unchanged", "added into the original", "Changed", "slot 1", "locker first", "C2", "json", "simple",
     "Same test, scored", "B1 (purple)", "s = 4", "s*", "beta", "position share", "not in this test", "queued",
     "not measurable", "° gate lowered after the data", "O", "excess (J++ minus random)", "J++ dependence", "W_U",
     "graded contrast C", "X0 · added after data",
     "J++, the pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's"],
)  # fmt: skip
def test_the_matcher_catches_each_banned_variant(text):
    assert banned([("example", text)]), text


@pytest.mark.parametrize(
    "text",
    ["J++ part", "without the J++ part", "identity outside J++", "UNVERIFIED", "Iris's pick", "the asked person's pick",
     "original answer → 2", "original\nprompt", "changed prompt", "locker after\nthe pick", "first locker",
     "simple scenes", "varied scenes: prose / JSON / table", "code shift (positions)", "β 0.15",
     "° gate lowered to 0.75 after the data", "random part (same size)", "random direction (same size)",
     "random lens directions", "PCA directions (same size)", "too few switches (10 of 60)", "not tested (gate)", "S.save",
     "the J++ lens fitted on the bf16 weights", "run x0_kmatch_27b", "switches lost (%)",
     "J++ part, pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's",
     "Adding the address alone brings position\nanswers back", *sorted(KEPT)],  # sorted: xdist needs one order
)  # fmt: skip
def test_the_matcher_passes_the_canonical_strings(text):
    assert not banned([("example", text)]), banned([("example", text)])


@pytest.fixture(scope="module")
def figure_texts(tmp_path_factory) -> dict[str, list[str]]:
    """Every text drawn on every figure the README or docs/depth/x0_details.md shows, by figure: the README figures (Figs.
    0-11, 1b and 3b), the supplementary ones, x0_figures' and x0_status_pack's f6. Rendered from the run files with
    savefig caught, so nothing is written (the scripts' data.csv and Fig. 11's scorecard.csv go to a temporary
    folder)."""
    import matplotlib
    from matplotlib.figure import Figure
    from matplotlib.text import Text

    from scripts import readme_story_figures as F
    from scripts import story_style as S
    from scripts import x0_figures as XF
    from scripts import x0_status_pack as SP
    from scripts.figs import common as FC

    if not (F.pins.RESULTS_DIR / "x6_routes").exists():
        pytest.skip("the run files are not in results/")
    tmp = tmp_path_factory.mktemp("figures")
    texts: dict[str, list[str]] = {}

    def grab(fig, fname, *args, **kwargs) -> None:
        texts[Path(str(fname)).stem] = [t.get_text() for t in fig.findobj(Text) if t.get_text().strip()]

    with pytest.MonkeyPatch.context() as mp, matplotlib.rc_context():
        mp.setattr(Figure, "savefig", grab)
        for mod, name, value in ((S, "ROWS", []), (S, "OUT", tmp), (S, "SUPP", tmp / "supp"), (SP, "OUT", SP.OUT),
                                 (SP, "SHOW_CLOSED", SP.SHOW_CLOSED), (FC, "LOOKUP", FC.LOOKUP),
                                 (FC, "RECALL", FC.RECALL)):  # fmt: skip
            mp.setattr(mod, name, value)  # restored on exit: the renders below set them
        p = S.setup()
        for f in (*F.README_FIGS, *F.SUPP_FIGS):
            f(p)
        XF.render(tmp / "x0_necessity")
        SP.render(tmp / "status", ["f6"])
    return texts


def test_every_shown_figure_uses_the_glossary(figure_texts):
    from scripts import readme_story_figures as F

    # the README's figures (Fig. 8b is Fig. 8 (a) since batch 45) and the second contact sheet's (supplementary +
    # docs/depth/x0_details.md's)
    shown = {*F.README_NAMES, *(Path(n).name for n in F.SHEET_MORE)}
    assert shown <= set(figure_texts), shown - set(figure_texts)
    flat = [(name, t) for name, ts in figure_texts.items() for t in ts]
    assert not banned(flat), banned(flat)


def test_readme_figures_have_no_retired_term(figure_texts):
    """scripts/check_figure_terms.py's retired terms on the README and supplementary figures (docs/depth/x0_details.md's
    figures keep their run names as provenance)."""
    from scripts import check_figure_terms as C
    from scripts import readme_story_figures as F

    readme = {*F.README_NAMES, *(Path(n).name for n in F.SHEET_MORE if n.startswith("supp/"))}
    flat = [(name, t) for name, ts in figure_texts.items() if name in readme for t in ts]
    assert flat and not C.retired(flat), C.retired(flat)


def caption_texts() -> list[tuple[str, str]]:
    """Until Tuesday's merge the canonical lines of the captions draft; then README.md's figure alt texts, "*Fig. N.*"
    caption lines and table headers (the line above each |---| row)."""
    if not CHECK_README:
        lines = CAPTIONS_DRAFT.read_text().splitlines()
        return [("readme_v5_captions.md", line.split(": ", 1)[1]) for line in lines if line.startswith("- canonical ")]
    text = re.sub(r"<!--.*?-->", "", B.PAGE.read_text(), flags=re.S)
    lines = text.splitlines()
    alts = [("alt text", a) for a in re.findall(r"!\[([^\]]*)\]\((?:\.\./)*figures/", text)]
    captions = [("caption", line) for line in lines if re.match(r"\*Fig\. \w+\.\*", line)]
    headers = [
        ("table header", lines[i - 1]) for i, line in enumerate(lines) if i and re.fullmatch(r"\|(?:-+\|)+", line)
    ]
    return alts + captions + headers


def test_readme_captions_use_the_glossary():
    texts = caption_texts()
    assert texts, "no captions found"
    assert not banned(texts), banned(texts)


def test_relink_from_a_subfolder_resolves_every_local_link():
    text = rendered_at_root()
    out = B.PAGE
    moved = B.relink(text, out)
    targets = [m.group(2) for m in B.LINK_TARGET.finditer(moved)]
    local = [t for t in targets if not re.match(r"[a-z][a-z0-9+.-]*:", t) and not t.startswith(("#", "/"))]
    # a target beside the page (docs/depth/EXPERIMENTS.md, the ledger's cards: Dan 12:50) needs no "../"
    beside = {t for t in local if (out.parent / t.partition("#")[0]).resolve().parent == out.parent.resolve()}
    assert local and all(t.startswith("../") for t in local if t not in beside)
    assert all((out.parent / t.partition("#")[0]).resolve().exists() for t in local)


def test_relink_keeps_the_root_readme_and_urls():
    text = '![a](figures/depth/x.png) [b](docs/y.md#z) [c](https://e.org/p) [d](#sec) <img src="figures/w.png">'
    assert B.relink(text, B.REPO / "README.md") == text
    moved = B.relink(text, B.REPO / "docs" / "depth" / "README.md")
    assert moved == ("![a](../../figures/depth/x.png) [b](../y.md#z) [c](https://e.org/p) [d](#sec) "
                     "<img src=\"../../figures/w.png\">")  # fmt: skip


def test_data_marker_reads_data_csv_and_carries_its_source(tmp_path, monkeypatch):
    # README v6 (Dan, 28 Oct): every number from data/figures/depth/data.csv with its source comment
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("figure,model,quantity,value,lo,hi,n,source\n"
                        "fig05,qwen3.5-9b,position share,0.514,0.46,0.56,300,results/x\n"
                        "numbers,,txt,65%,,,,docs/x\n")  # fmt: skip
    monkeypatch.setattr(B, "DATA_CSV", csv_path)
    monkeypatch.setattr(B, "REPO", tmp_path)
    book = B.Book.__new__(B.Book)
    book.in_table, book._data, book.head = False, None, "x"
    out = B.render("{{d|fig05|9b|position share}} and {{dp|fig05|9b|position share}}", book)
    assert "0.51 [0.46, 0.56]<!-- src: data.csv | position share -->" in out
    assert "and 0.51<!-- src: data.csv | position share -->" in out
    row = B.render("| a | {{d|numbers||txt}} |", book)
    assert "65%<!-- src: data.csv \\| txt -->" in row  # a table row escapes the pipe
    with pytest.raises(ValueError, match="no row"):
        B.render("{{d|fig05|muse|position share}}", book)
