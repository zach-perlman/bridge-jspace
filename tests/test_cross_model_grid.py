"""cross_model_grid: the verdict words on synthetic runs (each rule's pass, fail and failed-control case), the cell
status from the queue without opening any result, and on the saved runs: 10 random cells recomputed from the raw
rows. (The README's numbers are rendered from the grid since 4cf5d35: tests/test_readme_build.py.)

The real-run tests read every saved run: the night of 22-23 Oct was opened once Dan's predictions were committed
(a135a54); before that they read only the runs the README reported."""

from __future__ import annotations

import collections
import csv
import io
import json
import random

import pytest

from scripts import cross_model_grid as G


def _jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def _json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj))


@pytest.fixture
def results(tmp_path, monkeypatch):
    r = tmp_path / "results"
    monkeypatch.setattr(G, "RESULTS", r)
    return r


# ---------------------------------------------------------------- synthetic runs: each rule's verdict words


def _cases(n: int, listed: int, family: str = "RL") -> list[dict]:
    """n cases whose scene lists `listed` answers (the asked one and listed - 1 others)."""
    return [{"id": f"i{i}", "family": family, "tok_A": 1, "conf_toks": [2, 3], "conf_answers": [str(k) for k in
             range(2, listed + 1)]} for i in range(n)]  # fmt: skip


def _late_rows(n: int, attn: int, off: int, gdn: int | None) -> list[dict]:
    rows = [{"family": "RL", "id": f"i{i}", "source": "none", "dest": "none", "layers": "none", "correct": True}
            for i in range(n)]  # fmt: skip
    arms = [("lookup", "attn", attn), ("lookup_off", "attn", off)] + (
        [("lookup", "gdn", gdn)] if gdn is not None else []
    )
    for src, layers, k in arms:
        rows += [{"family": "RL", "id": f"i{i}", "source": src, "dest": "final", "layers": layers, "correct": i < k}
                 for i in range(n)]  # fmt: skip
    return rows


@pytest.mark.parametrize(
    ("attn", "off", "gdn", "word"),
    [
        (5, 100, 100, "holds"),
        (5, 80, 100, "not interpretable"),
        (5, 100, 50, "fails"),
        (40, 100, 100, "fails"),
        (5, 100, None, "holds"),
    ],
)
def test_late_read_verdicts(results, attn, off, gdn, word):
    _jsonl(results / "attn_knockout" / "r" / "rows.jsonl", _late_rows(100, attn, off, gdn))
    (row,) = G.ev_late(G.Cell("27b", "f4", "draw 2", "late", "r"))
    assert row.word == word
    assert row.n == 100 and row.value == pytest.approx(attn / 100)
    if word == "not interpretable":
        assert "off-path" in row.verdict


def test_a_family_with_no_item_right_is_not_testable(results):
    """A run whose competence filter left no memory -> prompt item (Muse's table and JSON scenes): not testable, and
    no crash on the empty rates (a crash took the whole formats cell, prose included, to 'files inconsistent')."""
    rows = [{**r, "family": "PP"} for r in _late_rows(20, 1, 20, None)]  # items of another family only
    _jsonl(results / "attn_knockout" / "r" / "rows.jsonl", rows)
    (row,) = G.ev_late(G.Cell("muse", "f4", "draw 2", "late", "r"))
    assert row.word == "not testable" and "competence" in row.verdict and row.n == 0
    row = G.parts_row(G.Cell("muse", "f3", "table", "parts", "r"), "table", {}, "MP", "p", None)
    assert row.word == "not testable" and "competence" in row.verdict


def _parts_rows(rates: dict[tuple[str, str], float], n: int = 100) -> tuple[list[dict], list[dict]]:
    cases = [{"id": f"i{i}", "tok_A": 1, "conf_toks": [2, 3]} for i in range(n)]
    rows = [{"family": "RL", "id": f"i{i}", "source": "none", "dest": "none", "layers": "all", "correct": True, "top": 1}
            for i in range(n)]  # fmt: skip
    for s in G.DP.PARTS + G.DP.SPLIT:
        for d in ("question", "final"):
            k = round(rates.get((s, d), 1.0) * n)
            rows += [{"family": "RL", "id": f"i{i}", "source": s, "dest": d, "layers": "all", "correct": i < k,
                      "top": 1 if i < k else 2} for i in range(n)]  # fmt: skip
    return rows, cases


@pytest.mark.parametrize(
    ("rates", "word"),
    [
        ({("lookup_noname", "final"): 0.05, ("lookup_nodigit", "final"): 0.95}, "holds"),
        ({("lookup_noname", "final"): 0.80, ("lookup_nodigit", "final"): 0.95}, "fails"),
        ({("lookup_noname", "final"): 0.05, ("lookup_off_noname", "final"): 0.50}, "not interpretable"),
    ],
)
def test_name_vs_digit_verdicts(results, rates, word):
    rows, cases = _parts_rows(rates)
    _jsonl(results / "attn_knockout" / "r" / "rows.jsonl", rows)
    _jsonl(results / "attn_knockout" / "r" / "cases.jsonl", cases)
    (row,) = G.ev_parts(G.Cell("27b", "f3", "draw 2", "parts", "r"))
    assert row.word == word
    assert row.value == pytest.approx(rates[("lookup_noname", "final")])


def test_chance_from_the_scenes_and_the_failing_off_path_control_named(results):
    """23 Oct (verification of findings 3-4): the prose / table / JSON scenes list 3 answers (chance 33%), the draws 5
    (20%), read from cases.jsonl; Olmo-Hybrid's off-path control failed at the question's tokens, which the control
    text must name (it showed the last tokens' 100%). Verdicts unchanged."""
    _jsonl(results / "attn_knockout" / "f" / "rows.jsonl", _late_rows(300, 66, 300, None))
    _jsonl(results / "attn_knockout" / "f" / "cases.jsonl", _cases(300, listed=3))
    (row,) = G.ev_late(G.Cell("gemma", "f4", "draw 2", "late", "f"))
    assert row.word == "fails" and "chance 33% (3 listed answers)" in row.control
    assert not row.notes  # 22% [18, 27]: below chance 33%, not at chance
    assert G.chance_of({c["family"] + c["id"]: c for c in _cases(4, 5) + _cases(4, 2, "PM")}, "RL") == (0.2, [5])
    assert G.chance_of({"x": {"id": "x", "family": "RL"}}, "RL") is None
    assert G.chance_of({"x": {"id": "x", "family": "NAT", "conf_answers": []}}, "NAT") is None  # open vocabulary
    rows, cases = _parts_rows({("lookup_noname", "final"): 0.05, ("lookup_off_nodigit", "question"): 0.86})
    _jsonl(results / "attn_knockout" / "h" / "rows.jsonl", rows)
    _jsonl(results / "attn_knockout" / "h" / "cases.jsonl", [{**c, "family": "RL", "conf_answers": list("2345")}
                                                             for c in cases])  # fmt: skip
    (row,) = G.ev_parts(G.Cell("olmo_hybrid", "f3", "draw 2", "parts", "h"))
    assert row.word == "not interpretable"
    assert "lowest 86%, the off-path sentence without its digit hidden from the question's tokens" in row.control
    assert row.control.endswith("chance 20% (5 listed answers)")


def _v2_rows(
    n: int,
    final: int,
    after: int | None,
    off_after: int | None = None,
    gdn: int | None = None,
    after_attn: int | None = None,
) -> list[dict]:
    """n items right unedited; k of n right under each block (after None: the run has no such block). gdn set: a
    hybrid (the last tokens blocked in every attention layer); after_attn: the block also in every attention layer."""
    rows = [  # the unedited rows' mode is '-', as in the runs' rows.jsonl (a mode filter must not drop them)
        {"family": "RL", "id": f"i{i}", "source": "none", "dest": "-", "layers": "-", "mode": "-", "correct": True}
        for i in range(n)
    ]
    lab = "attn" if gdn is not None else "all"

    def add(src: str, dest: str, layers: str, k: int, mode: str = "value") -> None:
        rows.extend({"family": "RL", "id": f"i{i}", "source": src, "dest": dest, "layers": layers, "mode": mode,
                     "correct": i < k} for i in range(n))  # fmt: skip

    add("lookup", "final", lab, final)
    add("lookup_off", "final", lab, n)
    if after is not None:
        add("lookup", "after", "all", after)
        add("lookup_off", "after", "all", n if off_after is None else off_after)
        add("lookup", "after", "all", n, mode="absent")  # the 27B's positive control: never counted
    if gdn is not None:
        add("lookup", "final", "gdn", gdn)
    if after_attn is not None:
        add("lookup", "after", "attn", after_attn)
        add("lookup_off", "after", "attn", n)
    return rows


@pytest.mark.parametrize(
    ("kw", "word", "why"),
    [
        ({"final": 10, "after": 2}, "holds", ""),
        ({"final": 10, "after": 2, "gdn": 95}, "holds", ""),
        ({"final": 40, "after": 2}, "fails", "less than 70%"),
        ({"final": 10, "after": 2, "gdn": 50}, "fails", "DeltaNet"),
        ({"final": 10, "after": 20}, "not interpretable", "the floor"),
        ({"final": 10, "after": 2, "off_after": 80}, "not interpretable", "off-path"),
        ({"final": 10, "after": None}, "missing", "every token after it"),
    ],
)
def test_last_tokens_share_verdicts(kw, word, why):
    """late-read-v2 (Dan, 23 Oct): share = (1 - final) / (1 - after) on items right unedited, beside the late read."""
    v = G.late_read_v2(_v2_rows(100, **kw))
    assert v["verdict"].startswith(word) and why in v["verdict"]
    if kw["after"] is not None and kw["after"] < 100:
        assert v["share"] == pytest.approx((1 - kw["final"] / 100) / (1 - kw["after"] / 100))
        assert v["n"] == 100 and v["relay"] == pytest.approx((kw["final"] - kw["after"]) / 100)
        lo, hi = v["share_ci"]
        assert lo <= v["share"] <= hi


def test_last_tokens_share_lower_bound_and_the_attention_only_floor(results):
    """A hybrid whose run blocks every later token in all layers only (the first scene set): a conservative lower
    bound, footnoted; with the block in every attention layer (the new runs) that one is used, all layers reported."""
    v = G.late_read_v2(_v2_rows(100, final=10, after=2, gdn=95))
    assert v["lower_bound"] and v["after_layers"] == "all"
    v = G.late_read_v2(_v2_rows(100, final=10, after=0, gdn=95, after_attn=5))
    assert not v["lower_bound"] and v["after_layers"] == "attn" and v["after_all"][0] == 0
    assert v["share"] == pytest.approx(0.9 / 0.95)
    assert not G.late_read_v2(_v2_rows(100, final=10, after=2))["lower_bound"]  # attention only: all = every attention
    _jsonl(results / "attn_knockout" / "h" / "rows.jsonl", _v2_rows(100, final=10, after=2, gdn=95))
    (row,) = G.ev_late_v2(G.Cell("27b", "f4", G.LAST_SHARE[0], "late_v2", "h"))
    assert row.word == "holds" and (row.md_text or "").startswith("share 92% [") and row.rule == "late-read-v2"
    assert "conservative lower bound" in row.notes[0] and "relay +8 points" in row.control
    _jsonl(results / "attn_knockout" / "m" / "rows.jsonl", _v2_rows(100, final=10, after=None))
    (miss,) = G.ev_late_v2(G.Cell("muse", "f4", G.LAST_SHARE[0], "late_v2", "m"))
    assert miss.word == "missing" and G.md_cell([miss])[0] == "· missing: no floor block in this run"
    # beside the late read, not among its settings: the README draft, the figures and the run table read those
    assert not set(G.LAST_SHARE) & set(G.FINDING["f4"].settings) and all(" · " in s for s in G.LAST_SHARE)
    md = G.grid_md([row, miss], {"git": "test", "written_utc": "test"})
    section = md.split("## Finding 4 beside the late read")[1].split("\n## ")[0]
    assert "| draw 1 | " in section and "✓ share 92% [" in section and "· missing: no floor block" in section


def test_gate_verdicts(results):
    g = {"pass": False, "bridge_top10": [0.4, 0.3, 0.5], "x_top10": [0.1, 0.05, 0.2], "n": 60}
    _json(results / "lens_gate" / "r" / "summary.json", {"gate": g})
    v1 = G.ev_gate(G.Cell("32b", "gate", "v1 (at the word)", "gate", "r", opts={"gate": "v1"}))
    v2 = G.ev_gate(G.Cell("32b", "gate", "v2 (after the word)", "gate", "r", opts={"gate": "v2"}))
    assert (v1[0].word, v1[0].value, v1[0].n) == ("fails", 0.4, 60)
    assert v2[0].word == "missing"


def test_stated_bridge_verdicts_and_exact_run_match(results):
    cell = {"set": "context", "layer": 32, "map_flips": [0.9, 0.8, 0.95]}
    part = {"full": [0.9, 0.8, 0.95, 100], "jspace": [0.0, 0.0, 0.04, 100], "not_jspace": [0.85, 0.77, 0.9, 100]}
    v = {"cell": cell, "lookup": part, "recall": {**part, "jspace": [0.05, 0.02, 0.1, 100]},
         "verdict": "not interpretable: the positive control fails", "topic_verdicts": {"animals": "replicates"},
         "by_topic": {"animals": {"PP_jspace": [0.0, 0.0, 0.1, 30], "PP_not_jspace": [0.9, 0.8, 0.95, 30],
                                  "PM_jspace": [0.5, 0.3, 0.7, 30]}}}  # fmt: skip
    _json(results / "d1_verdict" / "p_20261022-100000" / "verdict.json", v)
    _json(results / "d1_verdict" / "p_r2_20261023-100000" / "verdict.json", {**v, "verdict": "replicates"})
    latest = G.latest_dir(results / "d1_verdict", "p")
    assert latest is not None and latest.name == "p_20261022-100000"
    rows = G.ev_d1(G.Cell("32b", "f2", "draw 1", "d1", "p"))
    assert [r.word for r in rows] == ["not interpretable", "holds"]
    assert "positive control" in rows[0].verdict and rows[1].md_setting is None


def test_lens_push_verdicts(results):
    rates = {"BL": [0.29, 0.21, 0.39], "BR": [0.84, 0.76, 0.9], "BL_random": [0, 0, 0.04], "RL_changed": [0.05, 0, 0.1],
             "RR_changed": [0.03, 0, 0.08]}  # fmt: skip
    dec = {"rule": "v2", "primary": {"subset": "w", "layer": 16, "scale": 8.0}, "verdict": "inconclusive", "rates": rates,
           "n_scenes_paired": 100}  # fmt: skip
    d = results / "early_push_where" / "r"
    _json(d / "summary.json", {"decision": dec})
    cell = G.Cell("27b", "f7", "main rule", "d4", "r")
    assert [r.word for r in G.ev_d4(cell)] == ["inconclusive", "missing"]  # the rule's own word, no control failed
    _json(d / "analysis-v2.1-20261022T000000Z" / "summary.json",
          {"decision": {**dec, "rule": "v2.1", "verdict": "H-around: the lens writes ..."}})  # fmt: skip
    assert [r.word for r in G.ev_d4(cell)] == ["inconclusive", "holds"]
    assert [r.setting for r in G.ev_d4(G.Cell("27b", "f7", "x", "d4", "r", opts={"suffix": ", draw 2"}))] == [
        "main rule, draw 2", "amended rule, draw 2"]  # fmt: skip
    assert G.d4_word("not valid (H-around: x)").startswith("not interpretable")
    assert G.d4_word("no valid cell: the lens does not write").startswith("not interpretable")


def test_gap_interval_unpaired_over_entities():
    look = [(1.0, "cow")] * 10 + [(1.0, "pig")] * 10
    rec = [(0.0, "cow")] * 10 + [(1.0, "pig")] * 10
    point, lo, hi = G.gap_ci(look, rec)
    assert point == pytest.approx(0.5) and lo <= point <= hi
    assert (lo, hi) == pytest.approx((0.0, 1.0))  # two entities: the recall mean resamples to 0, 0.5 or 1
    same = [(1.0, "cow")] * 5 + [(0.0, "pig")] * 5
    assert G.gap_ci(same, same)[0] == 0


def test_removal_descriptive_with_g2_and_no_random_control(results, monkeypatch):
    def fam(j: float, rot: float) -> dict:
        return {"n": 2, "accuracy": {"none": 1, "jspace": j, "rotated": rot}}

    ids = {f: [f"{f}-0000", f"{f}-0001"] for f in ("BL", "RL", "BR", "RR")}
    monkeypatch.setattr(G, "suite_entities", lambda: {(f, i): f"e{k}" for f, v in ids.items() for k, i in enumerate(v)})
    correct = {"BL": 1, "RL": 1, "BR": 0, "RR": 0}
    _jsonl(results / "ablate_pilot" / "r" / "rows.jsonl",
           [{"family": f, "id": i, "kind": "clean", "condition": "jspace", "correct": bool(correct[f])}
            for f, v in ids.items() for i in v])  # fmt: skip
    fams = {"BL/clean": fam(1.0, 1.0), "RL/clean": fam(1.0, 1.0), "BR/clean": fam(0.0, 1.0), "RR/clean": fam(0.0, 0.8)}
    _json(results / "ablate_pilot" / "r" / "summary.json", {"families": fams})
    rows = G.ev_removal(G.Cell("32b", "f1", "animal suite", "removal", "r", opts={"g2": True}))
    assert {r.word for r in rows} == {"not interpretable"} and "RR/clean" in rows[0].verdict
    assert "no random-dictionary control" in (rows[0].md_text or "")
    assert rows[0].value == pytest.approx(1.0) and rows[0].unit == "pts" and rows[0].n == 8
    fams["RR/clean"] = fam(0.0, 1.0)
    _json(results / "ablate_pilot" / "r" / "summary.json", {"families": fams})
    rows = G.ev_removal(G.Cell("32b", "f1", "animal suite", "removal", "r", opts={"g2": True}))
    assert rows[0].verdict == "open (descriptive, no committed rule)"
    pilot = G.ev_removal(G.Cell("27b", "f1", "animal suite", "removal", "r"))  # Zach's pilot: no G2, never missing
    assert pilot[0].word == "open"


@pytest.mark.parametrize(
    ("rule", "word"),
    [
        ({"gap": 0.4, "controls_ok": True, "C1_graded_holds": True}, "holds"),
        ({"gap": 0.1, "controls_ok": True, "C1_graded_holds": False}, "fails"),
        ({"gap": 0.4, "controls_ok": False, "C1_graded_holds": False}, "not interpretable"),
        ({"gap": None, "controls_ok": False, "C1_graded_holds": False}, "missing"),
    ],
)
def test_zach_c1_verdict_read_as_it_is(monkeypatch, rule, word):
    v = {"middle": "L32-40", "bands": {"L32-40": {"paper10": {w: {"acc": 0.5, "n": 10} for w in ("PP", "MP", "PM", "MM")}}},
         "rule": rule}  # fmt: skip
    monkeypatch.setattr(G, "zach_file", lambda path: json.dumps(v))
    (row,) = G.ev_zach_c1(G.Cell("27b", "f1", "tasks, Zach's rule", "zach_c1", "z"))
    assert row.word == word and row.n == 40 and row.path.startswith(G.ZACH_REF)


def test_lens_arm_is_open_and_late_read_footnotes(results):
    _json(results / "pointer_fit" / "r" / "summary.json",
          {"verdict": "x", "primary": {"lens": [0.0, 0.0, 0.01, 400], "slot": [0.3, 0.2, 0.4, 400],
                                       "random": [0.0, 0.0, 0.01, 400], "layer": 48, "scale": 1.0}})  # fmt: skip
    (row,) = G.ev_fitlens(G.Cell("27b", "f8", "last tokens", "fitlens", "r"))
    assert row.verdict == "open (no rule for the lens arm)"
    _jsonl(results / "attn_knockout" / "g" / "rows.jsonl", _late_rows(300, 66, 300, None))
    _jsonl(results / "attn_knockout" / "g" / "cases.jsonl", _cases(300, listed=5))
    (row,) = G.ev_late(G.Cell("gemma", "f4", "draw 1", "late", "g", opts={"first_draw": True}))
    assert row.word == "fails"
    assert row.notes[0].startswith("at chance (22% [") and row.notes[0].endswith(", chance 20%)")
    assert "draw 1 judged by the late-read rule" in row.notes[1]
    text, notes = G.md_cell([row])
    assert text.count("[{n}]") == 2 and len(notes) == 2


# ---------------------------------------------------------------- the queue: status without results


def test_status_from_ledger_and_queue(tmp_path, results):
    for job, deps in (("a", []), ("b", ["a"]), ("c", []), ("d", []), ("e", [])):
        (tmp_path / "jobs" / "d1").mkdir(parents=True, exist_ok=True)
        (tmp_path / "jobs" / "d1" / f"{job}.yaml").write_text(json.dumps({"id": job, "depends_on": deps}))
    stop = "uv run python scripts/d1_precheck.py --gate {g} && uv run python scripts/x.py"
    ledger = [
        {"id": "a", "status": "failed", "exit_code": 3, "command": stop.format(g="g_fail"), "ended_at": "1", "commit": "abc1234ff"},
        {"id": "c", "status": "failed", "exit_code": 3, "ended_at": "1",
         "command": stop.format(g="g_pass") + " && uv run python scripts/check_unedited.py --run s"},
        {"id": "d", "status": "failed", "exit_code": 1, "ended_at": "1", "command": "x", "error": "Traceback\nOOM"},
    ]  # fmt: skip
    _jsonl(tmp_path / "results" / "jobq" / "ledger.jsonl", ledger)
    _json(tmp_path / "cache" / "jobq" / "queue_state.json", {"pending": [{"id": "b"}], "running": []})
    _json(results / "lens_gate" / "g_fail" / "summary.json", {"gate": {"pass": False}})
    _json(results / "lens_gate" / "g_pass" / "summary.json", {"gate": {"pass": True}})
    jobs = G.Jobs(tmp_path)
    assert jobs.status(("a",)) == ("not testable", "gate v1 failed (g_fail)")
    assert jobs.status(("b",))[0] == "not testable"  # blocked behind a job the gate stopped
    assert jobs.status(("c",))[0] == "missing" and "raw smoke mismatch" in jobs.status(("c",))[1]
    assert jobs.status(("d",))[0] == "failed"
    assert jobs.status(("e",))[0] == "not enqueued"
    assert jobs.status(("zz",)) == ("no spec", "no spec")
    assert jobs.status(("a",), values=False)[0] == "failed"  # no gate summary is read without values
    assert jobs.commit(G.Cell("27b", "f2", "draw 1", "d1", "r", ("a",))) == "abc1234"
    _json(tmp_path / "cache" / "jobq" / "queue_state_h200.json", {"pending": [{"id": "d"}], "running": []})
    _jsonl(tmp_path / "results" / "jobq" / "ledger_h200.jsonl", [{"id": "e", "status": "failed", "exit_code": 1,
                                                                   "ended_at": "2", "command": "x"}])  # fmt: skip
    jobs = G.Jobs(tmp_path)  # every box's ledger and queue state; a queued retry outranks an earlier failure
    assert jobs.status(("d",))[0] == "pending" and jobs.status(("e",))[0] == "failed"


def test_jobs_found_by_run_name_and_finding5_layers(tmp_path):
    spec = {"id": "x_r2", "command": "uv run python scripts/pointer_swap.py manifest --name run_a --n 1",
            "figures_command": "uv run python scripts/finding5_confirm.py --run run_a --layers 16 17 18 --level e8-digit "
                               "--sentences 8 && uv run python scripts/finding5_confirm.py --run run_a --layers 20 21 "
                               "--level e8-word --sentences 8"}  # fmt: skip
    (tmp_path / "jobs" / "d3").mkdir(parents=True)
    (tmp_path / "jobs" / "d3" / "x_r2.yaml").write_text(json.dumps(spec))
    jobs = G.Jobs(tmp_path)
    assert jobs.jobs_of(G.Cell("27b", "f5", "draw 1", "f5", "run_a")) == ("x_r2",)
    assert jobs.f5_layers("run_a", "e8-digit") == [16, 17, 18]
    assert jobs.f5_layers("run_a", "e8-word") == [20, 21]
    assert jobs.f5_layers("run_b", None) is None


def test_no_values_opens_no_result(monkeypatch):
    def boom(cell):
        raise AssertionError("a result was opened")

    monkeypatch.setattr(G, "EVAL", dict.fromkeys(G.EVAL, boom))
    rows = G.build(["27b:*", "olmo_hybrid:*"], values=False)
    assert rows and {r.status for r in rows} <= {"has-run", "failed", "pending", "running", "blocked", "not enqueued",
                                                 "no spec", "no lens", "done, no results", "not on Zach's branch"}  # fmt: skip
    assert all(r.value is None for r in rows)


def test_every_grid_cell_has_a_row(monkeypatch):
    monkeypatch.setattr(G, "EVAL", dict.fromkeys(G.EVAL, lambda cell: []))
    cells = G._cells()
    have = {(c.model, c.finding, s) for c in cells for s in G.settings_of(c)}
    for f in G.ALL_FINDINGS:
        for s in f.settings if f.fill else ():  # per-run settings (necessity's cells): only the runs' own rows
            for m in G.MODELS:
                assert (m.key, f.key, s) in have, (m.key, f.key, s)
    assert len({(c.model, c.finding, c.setting, c.role, c.run) for c in cells}) == len(cells)
    # one cell per (model, finding, setting, role): a run's expanded settings get no 'no spec' twin
    filled = collections.Counter((c.model, c.finding, s, c.role) for c in cells for s in G.settings_of(c))
    assert max(filled.values()) == 1, [k for k, v in filled.items() if v > 1][:5]
    assert {c.run for c in cells if c.model == "olmo_hybrid" and c.finding in ("f5", "f6")} >= {
        "olmo_hybrid_7b_d3v4_swap_fn", "olmo_hybrid_7b_d3v4_seed2_swap", "olmo_hybrid_7b_d3v4x_swap"}  # fmt: skip
    assert len(G.VERDICTS) == 7 and set(G.SYMBOL) == set(G.VERDICTS)
    text = G.csv_text([G.Row("27b", "f4", "draw 2", verdict="missing (x)")])
    assert next(csv.reader(io.StringIO(text))) == list(G.COLUMNS)


def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj))


def test_new_c1_c3_evaluators_read_the_runs_own_verdicts(tmp_path, monkeypatch):
    """relay swap, natural read, absent entity, necessity, rest at size, late switch: each run's own verdict word,
    mapped one to one, never recomputed; necessity's J-dependence = (F(full) - F(not_jspace)) / F(full)."""
    monkeypatch.setattr(G, "RESULTS", tmp_path)
    r3 = [0.2, 0.15, 0.25]
    blk = {"n": 300, "k": 84, "R": r3, "R_items": r3, "sub_new": r3, "orig_new": [0, 0, 0.01], "topics": {}}
    _write_json(tmp_path / "relay_swap" / "rs" / "analysis-1" / "verdict.json",
                {"late": "all", "test": blk, "positive": [1, 0.99, 1], "off_path": {**blk, "sub_new": [1, 0.99, 1]},
                 "floor": {**blk, "R": [0, 0, 0]}, "every_layer": None, "verdict": "relay"})  # fmt: skip
    (row,) = G.ev_relay(G.Cell("gemma", "relay", "draw 1", "relay", "rs"))
    assert row.word == "holds" and row.unit == "pts" and row.n == 300 and row.value == 0.2
    cells = {k: {"rate": [0.3, 0.26, 0.34], "n": 469} for k in ("late", "off", "deltanet", "floor", "question")}
    _write_json(tmp_path / "attn_knockout" / "nr" / "analysis-1-verdict" / "verdict.json",
                {"cells": cells, "layers_for_late": "attn", "hybrid": True, "late_article_cluster_ci": [0.3, 0.25, 0.35],
                 "verdict": "fails (more than 10% right, or the upper bound above 20%)", "verdict_secondary": "fails"})  # fmt: skip
    (row,) = G.ev_natural(G.Cell("27b", "natural", "SQuAD", "natural", "nr"))
    assert row.word == "fails" and row.n == 469
    lk = {"full": [0.8, 0.7, 0.9, 180], "not_jspace": [0.2, 0.1, 0.3, 180], "not_rand_sub": [0.6, 0.5, 0.7, 180]}
    nv = {"verdict": "does not hold", "lookup_drop_J": 0.6, "recall_drop_J": 0.6, "recall_drop_rand": 0.2}
    _write_json(tmp_path / "d1_verdict" / "np_20261023-000000" / "verdict.json",
                {"verdict": "does not hold (cells where it holds: bridge_word 0/1)", "sets": {},
                 "cells": {"bridge_word:16": {"lookup": lk, "recall": lk, "necessity": nv}}})  # fmt: skip
    rows = G.ev_nec(G.Cell("27b", "nec", "model", "nec", "np"))
    assert [r.setting for r in rows] == ["model", "bridge_word:16 lookups", "bridge_word:16 recalls"]
    assert all(r.word == "fails" for r in rows) and rows[1].value == pytest.approx(0.75)
    assert all(r.setting in G.FINDING["nec"].settings for r in rows)
    assert "the random slice's (F(full) - F(not_rand_sub)) / F(full): 25%" in rows[1].control


def test_grid_md_states_the_seven_words_and_how_finding_1s_interval_is_computed():
    row = G.Row("27b", "f1", "animal suite", verdict="open (descriptive, no committed rule)", md_setting="animal suite",
                md_text="gap +1 [0,2] n=8", unit="pts")  # fmt: skip
    md = G.grid_md([row], {"git": "test", "written_utc": "test"})
    assert md.count(G.GAP_METHOD) == 2  # the legend and the choices made after seeing the data
    assert "drawn with replacement, separately for the lookup items and for the recall items (unpaired)" in md
    for word in G.VERDICTS:
        assert f"{G.SYMBOL[word]} {word}" in md.split("## Key cells")[0]
    assert "○ gap +1 [0,2] n=8" in md


# ---------------------------------------------------------------- 23 Oct: random parts, stops upstream, deviations


def _cf(fam: str, part: str, switched: int, n: int, **over) -> list[dict]:
    """n parts rows of one family and part at context / layer 32 (cf, not null); the first `switched` switch (b)."""
    return [{"family": fam, "name": f"{fam}-{i}", "set": "context", "layer": 32, "part": part, "source": "cf",
             "null": False, "role": "b" if i < switched else "A", **over} for i in range(n)]  # fmt: skip


def test_stated_bridge_shows_the_same_share_random_part_at_the_verdicts_cell(results, monkeypatch):
    lens = {"full": [0.9, 0.8, 0.95, 100], "jspace": [0.02, 0.0, 0.07, 100], "not_jspace": [0.85, 0.77, 0.9, 100]}
    blk = {"PP_jspace": [0.0, 0.0, 0.1, 50], "PP_not_jspace": [0.9, 0.8, 0.95, 50], "PM_jspace": [0.5, 0.3, 0.7, 50]}
    v = {"cell": {"set": "context", "layer": 32, "map_flips": [0.9, 0.8, 0.95]}, "lookup": lens, "recall": lens,
         "verdict": "replicates", "topic_verdicts": {"animals": "replicates"}, "by_topic": {"animals": blk},
         "by_format": {"table": blk, "json": blk}, "format_verdicts": {"table": "replicates", "json": "replicates"}}  # fmt: skip
    _json(results / "d1_verdict" / "p_20261023-100000" / "verdict.json", v)
    rows = _cf("PP", "jspace_matched", 3, 100) + _cf("PM", "jspace_matched", 40, 100)
    # not at the verdict's cell, the random-direction null, O's copy, another part: never counted
    rows += _cf("PP", "jspace_matched", 100, 100, layer=36) + _cf("PP", "jspace_matched", 100, 100, null=True)
    rows += _cf("PP", "jspace_matched", 100, 100, source="off") + _cf("PP", "jspace", 100, 100)
    _jsonl(results / "statement_positions" / "p" / "outcomes.jsonl", rows)
    main, topic = G.ev_d1(G.Cell("27b", "f2", "draw 2", "d1", "p"))
    rp = main.random_parts["jspace_matched"]
    assert rp["lookups"][0] == pytest.approx(0.03) and rp["lookups"][3] == 100
    assert rp["recalls"][0] == pytest.approx(0.40) and rp["recalls"][3] == 100 and "rand_sub" not in main.random_parts
    assert (
        "same-share random part (jspace_matched): lookups 3% [1, 8] n=100, recalls 40% [31, 50] n=100" in main.control
    )
    assert "outcomes.jsonl" in main.sources[1] and topic.md_setting is None and not topic.random_parts
    # rand_sub where a spec ran it (the 122B late specs); per format through the run's tasks set
    G.parts_rows.cache_clear()
    _jsonl(results / "statement_positions" / "p" / "outcomes.jsonl", rows + _cf("PP", "rand_sub", 10, 50))
    monkeypatch.setattr(G, "item_formats", lambda manifest: {f"{f}-{i}": "table" if i < 50 else "json"
                                                              for f in ("PP", "PM") for i in range(100)})  # fmt: skip
    table, js = G.ev_d1(G.Cell("27b", "f2", "table", "d1_formats", "p"))
    tl = table.random_parts["jspace_matched"]["lookups"]
    assert tl[0] == pytest.approx(0.06) and tl[3] == 50  # 3 of the 50 table items
    assert (
        js.random_parts["jspace_matched"]["lookups"][0] == 0 and js.random_parts["jspace_matched"]["recalls"][3] == 50
    )
    rs = table.random_parts["rand_sub"]  # lookups only: no recall row has it
    assert list(rs) == ["lookups"] and rs["lookups"][0] == pytest.approx(0.2) and "rand_sub" not in js.random_parts
    assert "random subspace, same share (rand_sub): lookups 20%" in table.control
    G.parts_rows.cache_clear()


def test_a_job_behind_a_stop_is_not_testable_with_the_stops_reason(tmp_path, results):
    """Muse D1: the map's precheck stopped (too few scenes) and its parts and rw were cancelled; OLMo with our J++:
    the parts found no transit cell from layer 16 on and its rw was cancelled. Both read 'not testable'."""
    specs = {"map": ([], "python3 scripts/d1_precheck.py --gate g && python3 sp.py map --name m"),
             "parts": (["map"], "python3 sp.py parts --name p --map m"), "parts_r2": (["map"], "python3 sp.py parts --name p --map m"),
             "rw": (["parts"], "python3 sp.py readwrite --name w"), "rw_r2": (["parts_r2"], "python3 sp.py readwrite --name w"),
             "omap": ([], "python3 sp.py map --name om"),
             "oparts": (["omap"], "python3 scripts/statement_positions.py parts --name op --map om --lo 16 --sets context"),
             "orw": (["oparts"], "python3 sp.py readwrite --name ow"), "fparts": (["omap"], "python3 sp.py parts --name fp")}  # fmt: skip
    for job, (deps, cmd) in specs.items():
        (tmp_path / "jobs" / "d1").mkdir(parents=True, exist_ok=True)
        (tmp_path / "jobs" / "d1" / f"{job}.yaml").write_text(
            json.dumps({"id": job, "depends_on": deps, "command": cmd})
        )
    _jsonl(tmp_path / "results" / "jobq" / "ledger.jsonl", [
        {"id": "map", "status": "failed", "exit_code": 3, "ended_at": "1", "command": specs["map"][1]},
        {"id": "omap", "status": "done", "exit_code": 0, "ended_at": "1", "command": specs["omap"][1]},
        {"id": "oparts", "status": "failed", "exit_code": 1, "ended_at": "2", "command": specs["oparts"][1]}])  # fmt: skip
    _json(tmp_path / "cache" / "jobq" / "queue_state.json", {"cancelled": [{"id": j} for j in ("parts", "rw", "orw")]})
    said = (
        "d1_precheck: gate v1 passed; eligible scenes per topic {'animals': 11}; STOP (needs the gate and >= 2 topics)"
    )
    (tmp_path / "log" / "jobq" / "map").mkdir(parents=True)
    (tmp_path / "log" / "jobq" / "map" / "log.txt").write_text(f"[jobq] $ ...\n{said}\n")
    (tmp_path / "log" / "jobq" / "oparts").mkdir(parents=True)
    (tmp_path / "log" / "jobq" / "oparts" / "log.txt").write_text(
        "Traceback\nAssertionError: no transit cell in any family\n"
    )
    _json(results / "lens_gate" / "g" / "summary.json", {"gate": {"pass": True}})
    jobs = G.Jobs(tmp_path)
    stop = "stopped by the precheck in map: gate v1 passed; eligible scenes per topic {'animals': 11}; STOP"
    st, why = jobs.status(("parts", "parts_r2"))
    assert st == "not testable" and why.startswith(stop) and why.endswith("; blocks parts_r2")
    st, why = jobs.status(("rw", "rw_r2"))  # two hops, through the retries of the same run
    assert st == "not testable" and why.startswith(stop) and why.endswith(", then rw_r2")
    moved = "no layer from 16 on where the stated bridge can still be moved"
    assert jobs.status(("oparts",)) == ("not testable", moved)
    assert jobs.status(("orw",)) == ("not testable", f"{moved}; blocks orw")
    assert jobs.status(("fparts",))[0] == "not enqueued"  # behind a done job: nothing stops it
    assert (
        jobs.status(("rw",), values=False)[0] == "not enqueued"
        and jobs.status(("oparts",), values=False)[0] == "failed"
    )
    texts = [G.md_cell([G.Row("olmo", "f2", "draw 2", verdict=f"not testable ({w})", md_setting="draw 2", md_text="")])[0]
             for w in (moved, why)]  # fmt: skip
    assert texts == ["⊘ not testable: no layer from 16 on", "⊘ not testable: too few scenes"]


def test_gemmas_stated_bridge_cells_carry_the_n_deviation_by_spec():
    """The note comes from the specs (they read Gemma's D1 maps), not from a result: it stands with or without the
    run (--no-values: a run that is here has no verdict text, so the md cell is given one)."""
    rows = G.build(["gemma:f2:*", "gemma:f8:stated bridge, draw 2", "gemma:f7:*", "27b:f2:*"], values=False)
    noted = {
        (r.finding, r.setting, r.role) for r in rows if any(n.startswith("n = 167 (topics) / 169") for n in r.notes)
    }
    assert noted == {("f2", "draw 2", "main"), ("f2", "table", "main"), ("f2", "JSON", "main"),
                     ("f8", "stated bridge, draw 2", "main")}  # fmt: skip
    note = next(r for r in rows if r.notes).notes[0]
    assert note.endswith("73c4a69 skips scenes whose positions fail the alignment check; accepted by Dan, 23 Oct")
    r0 = next(r for r in rows if r.notes and r.md_setting)
    r0.verdict = r0.verdict or "missing (status only)"
    text, notes = G.md_cell([r0])
    assert text.endswith(" [{n}]") and notes[0][1] == note


# ---------------------------------------------------------------- the README's runs


@pytest.fixture(scope="module")
def opened() -> tuple[list, list[dict]]:
    if not (G.RESULTS / "attn_knockout" / "d2_late_read_seed2_27b" / "rows.jsonl").exists():
        pytest.skip("the README's runs are not in results/")
    rows = G.build()
    return rows, list(csv.DictReader(io.StringIO(G.csv_text(rows))))


def _num(s: str) -> float:
    return float(s.split()[0])


def _recompute(r: dict, grid_row) -> float | None:
    """The csv row's value (percent) from the raw rows, without the grid's code; None for a kind not covered."""
    path = G.REPO / r["result path"]
    finding, setting = grid_row.finding, r["setting"]
    if "attn_knockout" in str(path):
        rows = G.jl(path)
        fam = "MP" if setting in ("prose", "table", "JSON") else "RL"
        fmt = {"prose": "prose", "table": "table", "JSON": "json"}.get(setting)
        cases = {c["id"]: c for c in G.jl(path.parent / "cases.jsonl")}
        ok = {r_["id"] for r_ in rows if r_["source"] == "none" and r_["correct"] and r_["family"] == fam}

        def keep(r_: dict) -> bool:
            return (
                r_["id"] in ok
                and r_["family"] == fam
                and (fmt is None or cases[r_["id"]]["wording"].split("/")[0] == fmt)
            )

        if finding == "f4":
            labels = {r_["layers"] for r_ in rows if r_["source"] == "lookup" and r_["dest"] == "final"}
            lab = "attn" if "attn" in labels else "all"
            sel = [
                r_["correct"]
                for r_ in rows
                if keep(r_) and r_["source"] == "lookup" and r_["dest"] == "final" and r_["layers"] == lab
            ]
        else:
            sel = [r_["top"] == cases[r_["id"]]["tok_A"] for r_ in rows if keep(r_) and r_["source"] == "lookup_noname"
                   and r_["dest"] == "final" and r_["layers"] == "all"]  # fmt: skip
        return 100 * sum(sel) / len(sel)
    if "lens_gate" in str(path):
        key = "bind_bridge" if setting.startswith("v1") else "after_word"
        best: dict[str, int] = {}
        for r_ in G.jl(path.parent / "rows.jsonl"):
            if r_["set"] == key and r_["rank_bridge"] is not None:
                best[r_["id"]] = min(best.get(r_["id"], 10**9), r_["rank_bridge"])
        return 100 * sum(v <= 10 for v in best.values()) / len(best)
    if "d1_verdict" in str(path) and "·" not in setting:
        v = json.loads(path.read_text())
        out = G.jl(G.RESULTS / "statement_positions" / v["parts"] / "outcomes.jsonl")
        sel = [o["role"] == "b" for o in out if o["family"] == "PP" and o["part"] == "jspace" and o["source"] == "cf"
               and not o["null"] and o["set"] == v["cell"]["set"] and o["layer"] == v["cell"]["layer"]]  # fmt: skip
        return 100 * sum(sel) / len(sel)
    if "ablate_pilot" in str(path):
        rows = [o for o in G.jl(path.parent / "rows.jsonl") if o["kind"] == "clean" and o["condition"] == "jspace"]

        def acc(fams: tuple[str, ...]) -> float:
            sel = [o["correct"] for o in rows if o["family"] in fams]
            return 100 * sum(sel) / len(sel)

        if " · " not in setting:  # the gap: lookups minus recalls, items pooled per group
            return acc(("BL", "RL")) - acc(("BR", "RR"))
        fam = {"lookup, bridge stated": "BL", "lookup, bridge recalled": "RL", "recall, bridge stated": "BR",
               "recall, bridge recalled": "RR"}[setting.split(" · ")[1]]  # fmt: skip
        return acc((fam,))
    return None


def test_ten_random_cells_recomputed_from_raw_rows(opened):
    rows, table = opened
    pairs = [(c, g) for c, g in zip(table, rows, strict=True) if c["value"] and _covered(c)]
    assert len(pairs) >= 10
    for c, g in random.Random(0).sample(pairs, 10):
        got = _recompute(c, g)
        assert got is not None
        assert f"{got:.1f}" == f"{_num(c['value']):.1f}", (c["model"], c["finding"], c["setting"])


def test_zach_c1_on_the_27b_holds_as_the_readme_says(opened):
    rows, _ = opened
    z = [r for r in rows if r.model == "27b" and r.finding == "f1" and r.setting == "tasks, Zach's rule"]
    if not z or z[0].word == "missing":
        pytest.skip("Zach's branch (origin/zach/v8-breadth-1021) is not fetched here")
    assert z[0].word == "holds"  # README: "C1 on Zach's generator ... Holds on Qwen3.6-27B by his rule"


def _covered(c: dict) -> bool:
    p = c["result path"]
    if c["finding"] not in {f.name for f in G.FINDINGS}:  # the 23 Oct C1-C3 rows: read from the runs' own verdicts
        return False
    # d1_verdict: _recompute pools the formats, so the per-format rows (table, JSON) are not covered
    return any(k in p for k in ("attn_knockout", "lens_gate", "ablate_pilot")) or (
        "d1_verdict" in p and "·" not in c["setting"] and c["setting"] not in ("table", "JSON")
    )
