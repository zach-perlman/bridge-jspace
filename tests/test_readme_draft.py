"""readme_draft on a SYNTHETIC grid (all eight models, all seven verdict words), ledger, figures and repo files.

No real run is read here: the grid rows are made up (random.Random(0)), rendered by cross_model_grid's own csv_text and
grid_md so that the fixture has the real files' format. make_fixture(root) is also what a human can run to look at a
draft built on made-up numbers."""

from __future__ import annotations

import csv
import datetime as dt
import io
import itertools
import json
import random
import re
from pathlib import Path

import pytest

from scripts import cross_model_grid as G
from scripts import readme_draft as R

STAMP = "20261023T080000Z"
NIGHT = "2026-10-23T01:00:00+02:00"  # after SINCE (23:00 UTC), with an offset
BEFORE = "2026-10-22T10:00:00+00:00"
LENS = "J++, published (neuronpedia), bbef480b"
REASON = {  # verdict texts in the grid's own words (synthetic cells)
    "no spec": "missing (no spec)",
    "no lens": "not testable (no lens)",
    "G2": "not interpretable (G2: a control removal keeps < 90% on RR/clean (rotated 80%))",
    "positive": "not interpretable (the positive control fails)",
    "gate": "not testable (gate v1 failed (muse30b_lens_gate_v2))",
    "job": "missing (job qwen35_122b_d1_topics2_parts failed at the run stage (exit 1))",
    "json": "missing (no JSON items in the run)",
    "pending": "missing (olmo_hybrid_7b_d2_late_read_long is pending in the queue)",
    "random": "not interpretable (the random-patch control breaks 85% of answers, above 30%)",
    "early": "not testable (no swept layer before the donor's digit arrives)",
    "inconclusive": "inconclusive (the rule's reading: the lookup moves between 10% and 30%, or the gap is unclear)",
    "off-path": "not interpretable (the off-path check failed at the decisive cell; reading there: H-around: the lens "
    "writes a stated bridge for recall but not for a lookup where it sits)",
    "smoke": "missing (raw smoke mismatch: the smoke's unedited answers differ from the raw competence run)",
    "no write": "not interpretable (the lens push does not write recall here: not written; no positive control)",
    "open": "open (descriptive, no committed rule)",
    "arm": "open (no rule for the lens arm)",
}
ALL = [m.key for m in G.MODELS]
LOW_GOOD = {"f2", "f3", "f4", "f7", "f8"}


def pattern(f: str, s: str, m: str) -> str:
    """The synthetic verdict of (finding, setting, model): a word or a REASON key."""
    lens = G.FINDING[f].lens
    if lens and m == "olmo_hybrid":
        return "no lens"
    table = {
        ("f1", "tasks, Zach's rule"): {"27b": "holds", "gemma": "fails"},
        ("f1", "animal suite"): {"olmo": "G2", **{k: "open" for k in ("27b", "9b", "32b", "muse", "gemma", "122b")}},
        ("f2", "draw 1"): {"27b": "holds", "32b": "positive"},
        ("f2", "draw 2"): {"27b": "holds", "9b": "holds", "olmo": "fails", "muse": "gate", "gemma": "holds", "122b": "job"},
        ("f2", "table"): {"27b": "holds", "9b": "holds"},
        ("f2", "JSON"): {"27b": "holds", "9b": "holds"},
        ("gate", "v1 (at the word)"): {"27b": "holds", "9b": "holds", "32b": "fails", "olmo": "holds", "muse": "fails",
                                       "gemma": "holds", "122b": "holds"},
        ("gate", "v2 (after the word)"): {"27b": "fails", "9b": "holds", "32b": "holds", "olmo": "holds",
                                          "gemma": "holds", "122b": "holds"},
        ("f6", "one statement fewer"): {"32b": "fails"},
        ("f7", "main rule"): {"27b": "inconclusive", "9b": "off-path", "olmo": "smoke"},
        ("f7", "amended rule"): {"27b": "holds", "9b": "holds", "olmo": "smoke"},
        ("f7", "main rule, draw 2"): {"27b": "holds", "122b": "holds"},
        ("f7", "amended rule, draw 2"): {"27b": "holds", "122b": "holds"},
        ("f8", "stated bridge, draw 1"): {"27b": "holds", "32b": "no write"},
        ("f8", "stated bridge, draw 2"): {"27b": "holds", "9b": "holds", "olmo": "fails"},
        ("f8", "last tokens"): {"27b": "arm", "9b": "arm"},
    }  # fmt: skip
    if (f, s) in table:
        return table[(f, s)].get(m, "no spec")
    if f == "f3":
        return "fails" if (m, s) == ("gemma", "draw 3") else "json" if (m, s) == ("122b", "JSON") else "holds"
    if f == "f4":
        return "pending" if (m, s) == ("olmo_hybrid", "long context") else "holds"
    if f == "f5":
        return "random" if (m, s) == ("muse", "draw 1") else "holds"
    if f == "f6":
        return "early" if m == "gemma" else "no spec" if m in ("muse", "122b") else "holds"
    return "no spec"


def run_of(f: str, s: str, m: str) -> str:
    slug = re.sub(r"\W+", "_", s).strip("_")  # run names are \w+, as the specs' --name
    if f in ("f3", "f4") and s in ("prose", "table", "JSON"):
        return f"syn_{m}_formats"
    shared = {"f6": "f6", "gate": "gate", "f2": "f2_formats" if s in ("table", "JSON") else None}
    if f == "f7":
        return f"syn_{m}_f7" + ("_d2" if "draw 2" in s else "")
    if shared.get(f):
        return f"syn_{m}_{shared[f]}"
    return f"syn_{m}_{f}_{slug}"


def path_of(f: str, s: str, run: str) -> str:
    return {
        "f1": f"results/ablate_pilot/{run}/summary.json",
        "f2": f"results/d1_verdict/{run}_20261023-010101/verdict.json",
        "f3": f"results/attn_knockout/{run}/rows.jsonl",
        "f4": f"results/attn_knockout/{run}/rows.jsonl",
        "f5": f"results/finding5_confirm/{run}_20261023-010101/verdict.json",
        "f6": f"results/pointer_swap/{run}/analysis-20261023T010101Z/summary.json",
        "gate": f"results/lens_gate/{run}/summary.json",
        "f7": f"results/early_push_where/{run}/" + ("analysis-v2.1-x/" if s.startswith("amended") else "") + "summary.json",
        "f8": f"results/statement_positions/{run}/summary.json" if s != "last tokens" else f"results/pointer_fit/{run}/summary.json",
    }[f]  # fmt: skip


def synthetic_rows() -> list[G.Row]:
    rng = random.Random(0)
    rows: list[G.Row] = []
    for f in G.FINDINGS:
        for s in f.settings:
            for m in ALL:
                key = pattern(f.key, s, m)
                verdict = REASON.get(key, key)
                word = next(w for w in G.VERDICTS if verdict.startswith(w))
                run = run_of(f.key, s, m)
                path = "" if key == "no spec" else path_of(f.key, s, run)
                lens = "none (lens-free)" if not f.lens else "none (no lens)" if key == "no lens" else LENS
                base = G.Row(m, f.key, s, lens=lens, verdict=verdict, path=path, run=run, md_setting=s, md_text="",
                             rule="synthetic", commit="abc1234")  # fmt: skip
                if word in ("missing", "not testable"):
                    rows.append(base)
                    continue
                good = (word == "holds") == (f.key in LOW_GOOD)
                v = rng.uniform(0.0, 0.1) if good else rng.uniform(0.3, 0.9)
                if word not in ("holds", "fails"):
                    v = rng.uniform(0.1, 0.5)
                n = rng.choice((60, 100, 156, 300))
                unit = "pts" if f.key in ("f1", "f5") else "%"
                ci = (max(0.0, v - rng.uniform(0.03, 0.07)), min(1.0, v + rng.uniform(0.03, 0.07)))
                if f.key == "f8" and s.startswith("stated"):
                    ci = None
                base.n, base.value, base.ci, base.unit = n, v, ci, unit
                base.md_text = G.key(v, ci, n, unit)
                if f.key == "f4":
                    base.control = (
                        "chance 20%; blocked in every attention layer; the off-path sentence keeps 99% [97, 100]"
                    )
                if f.key == "f5":
                    other = rng.uniform(0.05, 0.4)
                    base.setting = f"{s}, 1st-2nd"
                    base.md_text = f"{G.pts(v)}/{G.pts(other)} n={n}"
                    rest = G.Row(m, f.key, f"{s}, 3rd on", lens=lens, n=n, value=other, ci=(other - 0.05, other + 0.05),
                                 verdict=verdict, path=path, run=run, unit="pts", rule="synthetic")  # fmt: skip
                    rows += [base, rest]
                    continue
                rows.append(base)
    rows.append(G.Row("27b", "f1", "animal suite · lookup, bridge stated", lens=LENS, n=40, value=0.99, ci=(0.9, 1.0),
                      verdict=REASON["open"], path="results/ablate_pilot/syn_27b_f1_animal_suite/summary.json"))  # fmt: skip
    rows.append(G.Row("27b", "f2", "draw 2 · animals", lens=LENS, n=30, value=0.77, verdict="fails",
                      path="results/d1_verdict/syn_27b_f2_draw_2_20261023-010101/verdict.json"))  # fmt: skip
    rows.append(G.Row("27b", "gate", "v2 (after the word)", lens="plain J-lens, published, 1718c8c5", n=60, value=0.77,
                      ci=(0.6, 0.9), verdict="holds", role="plain J-lens", md_setting="v2 (after the word)",
                      md_text=G.key(0.77, (0.6, 0.9), 60), path="results/lens_gate/syn_27b_jlens_gate/summary.json"))  # fmt: skip
    return rows


NIGHT_RUNS = {  # (finding, setting) whose runs started on the night
    ("f1", "animal suite"), ("f2", "draw 2"), ("f3", "draw 3"), ("f4", "draw 3"), ("f4", "long context"),
    ("f5", "draw 3"), ("gate", "v2 (after the word)"), ("f7", "main rule, draw 2"), ("f8", "stated bridge, draw 2"),
}  # fmt: skip


def make_fixture(root: Path) -> Path:
    """A synthetic repo under root: the grid folder (returned), a ledger, figures, VERIFIED.md, the scorecard, a spec."""
    rows = synthetic_rows()
    grid = root / "results" / "cross_model" / STAMP
    grid.mkdir(parents=True)
    old = G.RESULTS
    G.RESULTS = root / "results"  # lens_block reads results/lens_table: none here
    try:
        md = G.grid_md(rows, {"git": "abc1234", "written_utc": STAMP})
    finally:
        G.RESULTS = old
    (grid / "grid.csv").write_text(G.csv_text(rows))
    (grid / "grid.md").write_text(md)
    ledger = [{"id": "old_job", "started_at": BEFORE, "ended_at": BEFORE, "status": "done",
               "command": f"uv run python scripts/x.py --name {run_of('f3', 'draw 1', '27b')}",
               "new_results": [f"attn_knockout/{run_of('f3', 'draw 1', '27b')}"]}]  # fmt: skip
    for f, s in sorted(NIGHT_RUNS):
        for m in ALL:
            ledger.append({"id": f"job_{f}_{m}_{len(ledger)}", "started_at": NIGHT, "ended_at": NIGHT, "status": "done",
                           "command": f"uv run python scripts/x.py --name {run_of(f, s, m)} --n 100", "new_results": []})  # fmt: skip
    ledger.append({"id": "naive_time", "started_at": "2026-10-22T21:00:00", "status": "done",
                   "command": f"x --name {run_of('f6', 'filler moved', '32b')}"})  # fmt: skip
    jq = root / "results" / "jobq"
    jq.mkdir(parents=True)
    (jq / "ledger_box.jsonl").write_text("".join(json.dumps(r) + "\n" for r in ledger) + "not json\n")
    figs = root / "figures" / "archive" / "cross_model"
    figs.mkdir(parents=True)
    for name in ("f_late_read_all_models.png", "f_late_read_all_models.svg", "f_name_vs_digit_all_models.png",
                 "f_order_label_then_identity.png", "f_lens_push_by_layer.png", "f_layer_gap_27b.png",
                 "f_patch_outcomes_by_depth.png", "f_mystery_panel.png"):  # fmt: skip
        (figs / name).write_bytes(b"")
    (root / "VERIFIED.md").write_text("# VERIFIED\n\n## A1. exp10: x\n\n- **Checked** (Danyil, 2026-10-16):\n\n"
                                      "## B1. exp02: y (verified 2026-10-16, Zach)\n\n- z\n")  # fmt: skip
    (root / "predictions").mkdir()
    (root / "predictions" / "README.md").write_text(
        "# Dan's predictions\n\n| Day | File | Score |\n|---|---|---|\n| 22 Oct | [2026-10-22_dan.md](2026-10-22_dan.md) | "
        "1 / 2 |\n\nTotal so far: 1 right.\n"
    )
    (root / "jobs" / "d2").mkdir(parents=True)
    (root / "jobs" / "d2" / "syn.yaml").write_text(f"command: x --name {run_of('f4', 'draw 1', '27b')}\n")
    return grid


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> tuple[Path, Path, R.Draft]:
    root = tmp_path_factory.mktemp("repo")
    grid = make_fixture(root)
    d = R.draft(grid, root, R.when(R.SINCE), dt.datetime(2026, 10, 23, 9, tzinfo=dt.UTC))
    return root, grid, d


def _section(md: str, start: str, end: str) -> str:
    return md[md.index(start) : md.index(end)]


# ---------------------------------------------------------------- the fixture itself


def test_fixture_has_all_models_and_all_seven_words(built):
    _, grid, _ = built
    rows = list(csv.DictReader(io.StringIO((grid / "grid.csv").read_text())))
    assert {r["model"] for r in rows} == {m.label for m in G.MODELS}
    assert {next(w for w in G.VERDICTS if r["verdict"].startswith(w)) for r in rows} == set(G.VERDICTS)


# ---------------------------------------------------------------- structure


def test_sections_in_the_briefs_order(built):
    _, _, d = built
    heads = [x for x in d.text.splitlines() if x.startswith("## ")]
    want = ["## Findings at a glance", "## What changed on the night of 22-23 Oct",
            *(f"## {R.title(f)}" for f in R.FINDINGS), "## Across models", "## Negative or not testable",
            "## Choices made after seeing the data", "## Predictions scorecard", "## Appendix"]  # fmt: skip
    assert heads == want
    assert d.text.index("The question.") < d.text.index("## Findings at a glance")
    for f in R.FINDINGS:
        sec = _section(d.text, f"## {R.title(f)}", "## Across models")
        for part in ("**How sure:**", "**Key evidence:**", "**Models:**", "**What we did**", "**Weak spots**",
                     "**What it means:**"):  # fmt: skip
            assert part in sec.split("\n## ")[0], (f.key, part)


def test_overview_fits_one_screen(built):
    _, _, d = built
    overview = d.text[: d.text.index("## What changed")].splitlines()
    assert len(overview) <= 30
    table = [x for x in overview if x.startswith("| ") and not x.startswith("| #")]
    assert len(table) == len(R.FINDINGS)


def test_paragraphs_are_single_lines(built):
    _, _, d = built
    lines = d.text.splitlines()

    def item(x: str) -> bool:  # a list (nested or numbered) may follow a label line
        return x.lstrip().startswith("- ") or bool(re.match(r"\d+\. ", x))

    def block(x: str) -> bool:
        return x.startswith(("#", "|", "![", ">", "<!--", "---")) or item(x)

    for a, b in itertools.pairwise(lines):
        if a.strip() and not block(a) and b.strip() and not item(b):
            pytest.fail(f"a paragraph wraps onto a second line: {a[:60]!r} / {b[:60]!r}")


def test_draft_written_to_drafts_never_readme(tmp_path):
    make_fixture(tmp_path)
    assert R.main(["--repo", str(tmp_path)]) == 0
    assert len(list((tmp_path / "drafts").glob("README_*.md"))) == 1
    assert not (tmp_path / "README.md").exists()


def test_no_grid_writes_nothing(tmp_path):
    assert R.main(["--repo", str(tmp_path)]) == 1
    assert not (tmp_path / "drafts").exists()


# ---------------------------------------------------------------- numbers and words


def _ints_in_grid(csv_text: str) -> set[int]:
    return {round(float(x)) for x in re.findall(r"\d+(?:\.\d+)?", csv_text)}


def _checked(md: str) -> str:
    """The glance, the night's bullets and the finding sections, without names, ordinals, dates and link targets."""
    text = _section(md, "## Findings at a glance", "## Across models")
    text = "\n".join(x for x in text.splitlines() if not x.startswith("#"))
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"^\| \d+ \|", "|", text, flags=re.M)
    for name in sorted({m.label for m in G.MODELS} | set(R.SHORT.values()), key=len, reverse=True):
        text = text.replace(name, "")
    text = re.sub(r"\b\d+(st|nd|rd|th)\b", "", text)
    return re.sub(r"\b\d{1,2} Oct\b|\b\d{2}:\d{2}\b", "", text)


def test_every_number_comes_from_grid_csv(built):
    _, grid, d = built
    allowed = _ints_in_grid((grid / "grid.csv").read_text())
    text = _checked(d.text)
    found = [int(x) for x in re.findall(r"\d+", text)]
    assert found, "the checked sections show no number at all"
    assert not [x for x in found if x not in allowed]


def test_static_text_has_no_numbers():
    texts = [R.QUESTION, R.HOW_SURE, R.STATE_RULE]
    for t in R.TEXT.values():
        texts += [*t.did, *t.weak, t.means, *(label for _, label in t.metric)]
    for t in texts:
        assert not re.findall(r"\d+", re.sub(r"\b\d+(st|nd|rd|th)\b|Qwen3\.6-27B", "", t)), t


CODES = re.compile(r"\b(D[1-5]b?|C[1-3]b?|G2|v2\.1|pointer_v\d|BL|BR|RL|RR|H-around|H-where|syn_\w+)\b")


def test_internal_codes_only_in_the_appendix(built):
    _, _, d = built
    body = d.text[: d.text.index("## Appendix")]
    assert not CODES.findall(body.replace("Choices made after", "")), CODES.findall(body)
    assert "recall, bridge recalled" in body  # the removal footnote's RR/clean, in plain words
    assert CODES.findall(d.text[d.text.index("## Appendix") :])  # the mapping table names them


def test_rounding_is_half_to_even_and_ranges_read_plainly():
    assert R.fmt_value(12.5, "%") == "12%" and R.fmt_value(13.5, "%") == "14%"
    assert R.fmt_value(-3.4, "pts") == "-3 pts" and R.fmt_ci((-1.2, 4.6), "pts") == "[-1, +5]"
    assert R.fmt_range(0.2, 9.4, "%") == "0-9%" and R.fmt_range(24.0, 95.0, "pts") == "+24 to +95 pts"
    assert R.fmt_range(-5.0, 9.0, "%") == "-5% to 9%"


# ---------------------------------------------------------------- how sure


def _cell(m: str, word: str, run: str = "r", setting: str = "draw 1") -> R.Cell:
    return R.Cell(m, "f4", setting, "", True, word, word, 5.0, "%", (1.0, 9.0), 100, "", f"results/x/{run}/rows.jsonl")


@pytest.mark.parametrize(
    ("cells", "level", "reason"),
    [
        ([_cell(m, "holds", r) for m in ("27b", "32b", "olmo") for r in ("a", "b")], "strong", "both architectures"),
        ([_cell(m, "holds", r) for m in ("27b", "32b", "olmo") for r in ("a", "b")] + [_cell("gemma", "fails")],
         "medium", "fails on Gemma (draw 1)"),
        ([_cell(m, "holds", r) for m in ("27b", "32b", "olmo") for r in ("a", "b")]
         + [_cell("muse", "not interpretable")], "medium", "a control failed on Muse"),
        ([_cell(m, "holds", r) for m in ("27b", "9b", "122b") for r in ("a", "b")], "medium", "hybrids only"),
        ([_cell(m, "holds") for m in ("27b", "32b", "olmo")], "medium", "second run on fewer than two"),
        ([_cell("27b", "holds"), _cell("32b", "fails")], "open", "at least as many"),
        ([_cell("27b", "fails")], "open", "holds nowhere"),
        ([_cell("27b", "open")], "open", "values only"),
        ([_cell("27b", "missing")], "open", "not judged"),
        ([_cell("27b", "holds"), _cell("27b", "fails", setting="draw 2"), _cell("32b", "holds"),
          _cell("olmo", "holds")], "medium", "fails on 27B (draw 2)"),
    ],
)  # fmt: skip
def test_how_sure_rule(cells, level, reason):
    j = R.judge(G.FINDING["f4"], cells)
    assert j.level == level and reason in "; ".join(j.reasons), j.reasons


def test_model_states():
    assert R.model_state(["holds", "missing"]) == "holds"
    assert R.model_state(["holds", "fails"]) == "mixed"
    assert R.model_state(["inconclusive", "open"]) == "unclear"
    assert R.model_state(["open", "not testable"]) == "values only"
    assert R.model_state(["not testable", "missing"]) == "not testable"
    assert R.model_state([]) == "missing"


def test_levels_on_the_fixture_and_every_model_in_each_glance_row(built):
    _, _, d = built
    glance = _section(d.text, "## Findings at a glance", "## What changed")
    rows = [x for x in glance.splitlines() if re.match(r"\| [1-8] \|", x)]
    assert len(rows) == len(R.FINDINGS)
    level = {x.split(" | ")[0][2:]: re.findall(r"\*\*(strong|medium|open)\*\*", x)[0] for x in rows}
    assert level == {"1": "open", "2": "medium", "3": "medium", "4": "strong", "5": "medium", "6": "medium",
                     "7": "medium", "8": "medium"}  # fmt: skip
    for x in rows:
        groups = x.rstrip(" |").split(" | ")[-1].split(" · ")
        named = [n for g in groups for n in g.split(": ", 1)[1].split(", ")]
        assert sorted(named) == sorted(R.SHORT.values()), x


def test_breakdown_and_beside_rows_are_not_judged(built):
    _, grid, _ = built
    cells, skipped = R.read_grid((grid / "grid.csv").read_text())
    assert skipped >= 3 and all(" · " not in c.setting for c in cells)
    assert not [
        c for c in cells if c.finding == "gate" and c.model == "27b" and c.word == "holds" and "v2" in c.setting
    ]
    assert {c.part for c in cells if c.finding == "f5"} == {"1st-2nd", "3rd on"}


def test_key_evidence_from_held_cells_and_chance(built):
    _, grid, _ = built
    cells, _ = R.read_grid((grid / "grid.csv").read_text())
    j = R.judge(G.FINDING["f4"], cells)
    held = [c.value for c in j.cells if c.word == "holds" and c.value is not None]
    ev = R.evidence(j)
    assert ev.startswith(R.fmt_range(min(held), max(held), "%")) and ev.endswith("; chance 20%")
    assert "weakest: " in ev and R.fmt_value(max(held), "%") in ev.split("weakest: ")[1]
    assert "values only, no committed rule" in R.evidence(
        R.judge(G.FINDING["f8"], [c for c in cells if c.setting == "last tokens"])
    )


# ---------------------------------------------------------------- the night, figures, status, scorecard


def test_what_changed_lists_the_nights_cells_with_their_verdicts(built):
    _, _, d = built
    sec = _section(d.text, "## What changed", "\n---")
    bullets = [x for x in sec.splitlines() if x.startswith("- ")]
    assert 5 <= len(bullets) <= R.MAX_BULLETS
    for word in ("holds on", "fails on", "not interpretable on", "not testable on", "missing on"):
        assert word in sec, word
    assert "(draw 3)" in sec and "draw 1" not in sec  # the run before SINCE is not listed
    assert "- **The lookup's mechanism (lens-free findings)**:" in bullets  # nine findings: the lens-free merged
    f4 = next(x for x in sec.splitlines() if G.FINDING["f4"].name in x)  # two settings that night: named per model
    assert f4.startswith("  - ")
    assert "Olmo-Hybrid (draw 3)" in f4 and "missing on Olmo-Hybrid (long context: pending)" in f4
    f8 = next(x for x in sec.splitlines() if G.FINDING["f8"].name in x)  # one setting: not repeated per model
    assert "(stated bridge, draw 2): holds on 27B, 9B; fails on OLMo-3; not testable on Olmo-Hybrid (no lens)" in f8
    assert "(at the word / after the word)" in sec and "holds on 27B (at the word), 9B, " in sec
    assert "holds on 27B, 9B (draw 3 / long context)" not in f4 and "holds on 27B, 9B, Olmo-Hybrid (draw 3), 32B" in f4


def test_bullets_merge_beyond_eight():
    f = G.FINDING["f4"]
    cells = [R.Cell("27b", k, s, "", True, "holds", "holds", 1.0, "%", None, 10, "", f"results/x/r_{k}/rows.jsonl")
             for k in ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "gate") for s in G.FINDING[k].settings[:1]]  # fmt: skip
    lines, _ = R.what_changed(cells, {f"r_{k}" for k in G.FINDING}, R.when(R.SINCE))
    bullets = [x for x in lines if x.startswith("- ")]
    assert len(bullets) == 1 and bullets[0].startswith("- **Held on every model judged that night**")
    assert f.name in bullets[0]


def test_night_runs_from_the_ledger(built):
    root, _, _ = built
    runs = R.night_runs(root, R.when(R.SINCE))
    assert run_of("f3", "draw 3", "gemma") in runs and run_of("f6", "filler moved", "32b") in runs  # naive = UTC
    assert run_of("f3", "draw 1", "27b") not in runs
    assert R.run_names("results/finding5_confirm/abc_e8-digit_20261023-010101/verdict.json") >= {"abc"}
    assert "abc_r2" not in R.run_names("results/d1_verdict/abc_20261023-010101/verdict.json")


@pytest.mark.parametrize(
    ("name", "key"),
    [  # the claim-named files scripts/cross_model_figures.py writes (23 Oct)
        ("f_late_read_all_models", "f4"),
        ("f_digit_not_name_all_models", "f3"),
        ("f_order_then_identity_all_models", "f5"),
        ("f_counts_list_order_not_text_all_models", "f6"),
        ("f_patch_outcomes_by_depth_all_models", "depth"),
        ("f_lookup_ignores_lens_part_all_models", "f2"),
        ("f_lens_push_recall_not_lookup_all_models", "f7"),
        ("f_layer_gap_lens_vs_patch_27b", "f8"),
    ],
)
def test_the_figure_scripts_names_land_on_their_findings(tmp_path, name, key):
    (tmp_path / "figures" / "archive" / "cross_model").mkdir(parents=True)
    (tmp_path / "figures" / "archive" / "cross_model" / f"{name}.png").write_bytes(b"")
    assert {k: [p.stem for p in v] for k, v in R.figures(tmp_path).items()} == {key: [name]}


def test_figures_by_claim_name_and_none_dropped(built):
    root, _, d = built
    assert "![late read all models](figures/archive/cross_model/f_late_read_all_models.png) ([SVG]" in d.text
    sec4 = _section(d.text, f"## {R.title(G.FINDING['f4'])}", f"## {R.title(G.FINDING['f5'])}")
    assert "f_late_read_all_models.png" in sec4
    assert "f_layer_gap_27b.png" in _section(d.text, f"## {R.title(G.FINDING['f8'])}", "## Across models")
    across = _section(d.text, "## Across models", "## Negative")
    assert "f_patch_outcomes_by_depth.png" in across and "### Other merged figures" in across
    assert "f_mystery_panel.png" in across
    assert f"figure: {R.title(G.FINDING['f1'])}" in d.placeholders
    assert len(R.figures(root)["other"]) == 1


def test_cross_model_embeds_the_grid_and_the_lens_block(built):
    _, grid, d = built
    across = _section(d.text, "## Across models", "## Negative")
    md = (grid / "grid.md").read_text()
    table = R.md_sections(md)["The grid"]
    assert next(x for x in table if x.startswith("| 4 |")) in across
    assert "### Lens" in across and "| Model | Lens |" in across and "### Footnotes" in across
    head = "Holds on every judged model of both architectures: "
    assert "**What differs by architecture.**" in across and head in across
    assert across.split(head)[1].split(".")[0] == "finding 4; finding 5"
    assert "Fails only on hybrids: the lens gate, after the word (hybrids: holds on 9B, 122B, fails on 27B; " in across
    assert "Judged on one architecture only: finding 7 (hybrids: holds on 27B, 9B, 122B)" in across


def test_status_line_and_scorecard(built):
    _, _, d = built
    status = next(x for x in d.text.splitlines() if x.startswith("> **Status"))
    assert "A1 (Danyil); B1 (Zach)" in status and "23 Oct 2026" in status
    score = _section(d.text, "## Predictions scorecard", "## Appendix")
    assert "](predictions/2026-10-22_dan.md)" in score and "PLACEHOLDER" in score and "Total so far" in score


def test_the_repo_verified_md_is_read():
    who = R.verified(R.REPO)
    assert "B1" in who and "Zach" in who


def test_negative_and_choices(built):
    _, _, d = built
    neg = _section(d.text, "## Negative or not testable", "## Choices made")
    assert R.NEGATIVE_KEPT in neg and "Muse (gate failed)" in neg and "122B (failed)" in neg
    assert "Muse (no spec)" not in neg
    ch = _section(d.text, "## Choices made", "## Predictions")
    for key in ("Lens gate v2", "layer-gap", "keep-answer gate", "primary lens", "layer grid", "raw prompts",
                "batch 16", "Seven verdict words", "Finding 1's interval"):  # fmt: skip
        assert key in ch, key
    assert len([x for x in ch.splitlines() if x.startswith("| ")]) == len(R.CHOICES_KEPT) + 1


def test_appendix_maps_codes_scripts_and_specs(built):
    _, _, d = built
    app = d.text[d.text.index("## Appendix") :]
    row4 = next(x for x in app.splitlines() if x.startswith("| 4 |"))
    assert "jobs/d2/" in row4 and "synthetic" in row4 and G.FINDING["f4"].codes in row4
    assert "### How sure: the rule" in app and R.HOW_SURE in app


def test_unknown_rows_are_skipped():
    assert R.read_grid(G.csv_text([G.Row("27b", "f4", "draw 9", verdict="holds")])) == ([], 1)
    (cell,), skipped = R.read_grid(G.csv_text([G.Row("27b", "f4", "draw 1", verdict="holds")]))
    assert (cell.word, cell.value, cell.main, skipped) == ("holds", None, True, 0)
