"""The review tool's guided checklists (src/bridge_jspace/review/questions.py, docs/review/review_views.yaml; Dan 30 Oct):
every tier-1 view with questions has them, well formed; the machine expressions evaluate on stored items; the card shows
the checklist and its "look at" anchors exist on the card; answers are logged as schema-2 rows beside the item marks; old
marks files still load; the summary and VERIFIED.md report the tallies; the export works offline."""

from __future__ import annotations

import json
import re
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from bridge_jspace.review import handcheck as H
from bridge_jspace.review import items as I
from bridge_jspace.review import page as P
from bridge_jspace.review import questions as Q

TIER1 = [v["id"] for v in I.spec()["views"] if v.get("tier") == 1]
WITH_QUESTIONS = [vid for vid in TIER1 if Q.has_questions(vid)]
SHIPPED = ("main_swap",)  # view a; c, d, f, b follow in the same checklist (Dan 30 Oct: a first)
MODEL = "qwen3.6-27b"


def two_items(view_id: str) -> list[dict]:
    got = I.items(view_id, MODEL)
    return [got[0], got[len(got) // 2]]


def test_the_shipped_views_have_questions_and_a_header():
    for vid in SHIPPED:
        assert vid in WITH_QUESTIONS
        assert I.view(vid).get("header")
    ids = [q["id"] for q in Q.questions_of("main_swap")]
    assert ids == ["H1", "H2", "H3", "P1", "P2", "P3", "P4", "A1", "A2", "A3", "A4", "A5", "A6", "A7"]


@pytest.mark.parametrize("view_id", WITH_QUESTIONS)
def test_questions_are_well_formed(view_id):
    qs = Q.questions_of(view_id)
    assert qs
    for q in qs:
        assert q["kind"] in Q.KINDS and q["yes_if"] and q["look_at"] and q["protects_against"], q["id"]
    human, machine_only = Q.split(view_id)
    assert [q["id"] for q in human][:2] == ["H1", "H2"] and len(human) <= 3
    assert all(q["id"].startswith("P") or q["id"].startswith("A") for q in machine_only)


def test_p1_says_what_yes_means_per_view():
    by = {q["id"]: q for q in Q.questions_of("main_swap")}
    assert "swapped" in by["P1"]["yes_if"]
    spec = I.spec()
    p1 = next(q for q in spec["common_questions"] if q["id"] == "P1")
    assert "routes" in p1["yes_if"] and "x8_writes" in p1["yes_if"]


@pytest.mark.parametrize("view_id", WITH_QUESTIONS)
def test_machine_expressions_evaluate_on_two_stored_items(view_id):
    for it in two_items(view_id):
        for q in Q.questions_of(view_id):
            if not q.get("machine"):
                continue
            m = Q.machine(it, q)
            assert m["error"] is None and m["text"], (view_id, q["id"], it["id"], m)


def test_a_machine_that_cannot_compute_says_why():
    it = two_items("main_swap")[0]
    bad = Q.machine(it, {"id": "X", "machine": "no_such_helper()"})
    assert bad["text"] is None and "NameError" in bad["error"]


def test_machine_answers_on_a_known_item():
    it = next(i for i in I.items("main_swap", MODEL) if i["scene"] == "P2-L0-0000" and i["reader"] == "PP")
    qs = {q["id"]: q for q in Q.questions_of("main_swap")}
    a1 = Q.machine(it, qs["A1"])["text"]
    assert a1.startswith("yes") and "P(changed)" in a1  # the whole change switches this scene's recall
    assert Q.machine(it, qs["A6"])["text"].startswith("yes")  # the J++ part and its random part hold the same share
    assert Q.machine(it, qs["P3"])["text"].startswith("yes")


def test_overall_is_derived_from_the_checks_only():
    qs = Q.questions_of("main_swap")
    yes = {"H1": "yes", "H2": "yes"}
    assert Q.overall(yes, qs) == "consistent"
    assert Q.overall({**yes, "H2": "no"}, qs) == "wrong"
    assert Q.overall({**yes, "H2": "unclear"}, qs) == "unclear"
    assert Q.overall({"H1": "no", "H2": "unclear"}, qs) == "wrong"
    assert Q.overall({"H1": "yes"}, qs) is None  # not both answered yet
    assert Q.overall({**yes, "A1": "no", "H3a": "no", "P1": "no"}, qs) == "consistent"  # only H1 and H2 derive the mark


def test_the_card_shows_the_checklist_and_every_look_at_anchor_is_on_the_card():
    it = two_items("main_swap")[0]
    html = P.card(it, 0, False, None)
    assert "Checklist" in html and "the machine says" in html and "onclick=\"return look(this," in html
    assert html.index("Checklist") < html.index("As the model saw it")  # above the existing panels
    human, _ = Q.split("main_swap")
    for q in human:
        a = q.get("anchor")
        if a and a != "jspace":
            assert f"data-anchor='{a}'" in html, (q["id"], a)
    assert "Machine checks:" in html and "confirm the three ticks" in html
    assert "data-q='H1' data-kind='check'" in html and "data-q='H2' data-kind='check'" in html
    assert "data-q='A1'" not in html  # the machine's A1 is collapsed into the machine line, not put to the human


def test_the_old_marks_buttons_still_work_and_old_files_load(tmp_path):
    old = tmp_path / "marks.jsonl"
    old.write_text(json.dumps({"view": "main_swap", "item": "x|y", "seed": 29, "verdict": "wrong", "note": "n",
                               "commit": "abc", "utc": "2026-10-30T10:00:00Z"}) + "\n")  # fmt: skip
    assert [r["verdict"] for r in H.load_marks(old)] == ["wrong"]
    assert Q.load_rows(old) == []
    html = P.card(two_items("main_swap")[0], 29, False, {"verdict": "wrong"})
    assert all(f"value='{v}'" in html for v in ("consistent", "wrong", "unclear"))


def test_checklist_answers_are_logged_as_schema_2_rows(tmp_path, monkeypatch):
    from scripts import review as R

    monkeypatch.setattr(R, "MARKS", tmp_path / "marks.jsonl")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), R.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    item = two_items("main_swap")[0]["id"]

    def post(d):
        req = urllib.request.Request(f"{base}/mark", json.dumps(d).encode(), {"Content-Type": "application/json"})
        return urllib.request.urlopen(req).read()

    try:
        assert post({"schema": 2, "view": "main_swap", "item_key": item, "q_id": "A2", "answer": "yes", "note": "blocked", "seed": 29}) == b"ok"
        assert post({"schema": 2, "view": "main_swap", "item_key": item, "q_id": "A2", "answer": "no", "note": "", "seed": 29}) == b"ok"
        assert post({"view": "main_swap", "item": item, "seed": 29, "verdict": "consistent", "note": ""}) == b"ok"
        with pytest.raises(urllib.error.HTTPError):
            post({"view": "main_swap", "item_key": item, "q_id": "A2", "answer": "maybe"})
        rows = [json.loads(x) for x in (tmp_path / "marks.jsonl").read_text().splitlines()]
        q = [r for r in rows if r.get("schema") == 2]
        assert len(q) == 2 and {"schema", "view", "item_key", "q_id", "answer", "note", "ts"} <= set(q[0])
        assert Q.latest(Q.load_rows(tmp_path / "marks.jsonl"))[item]["A2"]["answer"] == "no"  # the last one counts
        assert [r["verdict"] for r in H.load_marks(tmp_path / "marks.jsonl")] == ["consistent"]
        page = urllib.request.urlopen(f"{base}/view?view=main_swap&seed=29&n=1&model={MODEL}").read().decode()
        assert "Checklist" in page and "View header" in page
    finally:
        httpd.shutdown()


def test_tallies_report_checks_as_counts_and_observations_as_x_of_n():
    rows = [{"schema": 2, "view": "main_swap", "item_key": f"{MODEL}|r|s{i}|PM", "q_id": q, "answer": a, "note": "", "ts": "t"}
            for i in range(10) for q, a in (("P1", "yes"), ("A2", "yes" if i < 7 else "no"))]
    lines = Q.tally_lines(rows, "main_swap")
    assert any("recall switch blocked without J++: 7/10" in x for x in lines), lines
    assert any("P1" in x and "yes 10, no 0, unclear 0" in x for x in lines), lines


def test_summary_and_verified_include_the_tallies(tmp_path, monkeypatch):
    from scripts import review as R
    from scripts import verified as V

    marks = tmp_path / "marks.jsonl"
    marks.write_text("".join(json.dumps({"schema": 2, "view": "main_swap", "item_key": f"{MODEL}|r|s{i}|PM", "q_id": "A2",
                                         "answer": "yes", "note": "", "ts": "t", "seed": 29}) + "\n" for i in range(3)))
    monkeypatch.setattr(R, "MARKS", marks)
    out = R.summary(tmp_path / "summary.md").read_text()
    assert "recall switch blocked without J++: 3/3" in out
    assert "recall switch blocked without J++: 3/3" in V.block(marks, None, None)


def test_the_view_header_has_the_four_checks_per_model():
    from scripts import review as R

    h = R.header("main_swap")
    assert set(h) == set(I.spec()["models"])
    for rows in h.values():
        assert [r["id"] for r in rows] == ["H1", "H2", "H3", "H4"]
        assert all(r["status"] in ("pass", "fail", "na") and r["means"] for r in rows)
    html = P.header_html(h)
    assert "View header" in html and "H2" in html


def test_export_works_offline_with_the_checklist(tmp_path):
    from scripts import review as R

    out = R.export(0, 1, tmp_path / "seed-0")
    page = (out / "main_swap.html").read_text()
    assert "Checklist" in page and "const SERVER=false" in page and re.search(r"function answerQ", page)


def human_questions(card_html: str) -> set[str]:
    """The questions a card puts to the human, H3's three ticks counted as one."""
    got = {re.sub(r"^(H3)[abc]$", r"\1", x) for x in re.findall(r"class='q(?: attn)?' data-q='([A-Za-z0-9]+)'", card_html)}
    return got


@pytest.mark.parametrize("view_id", WITH_QUESTIONS)
def test_every_tier_1_view_renders_five_items_with_three_or_fewer_human_questions(view_id):
    from scripts import review as R

    assert len(Q.five_ids(view_id)) == 5
    page = R.render_view({"view": view_id, "seed": "29", "n": "10"}, False, "t")
    cards = page.split("<div class='card")[1:]
    assert len(cards) == 5
    for c in cards:
        assert len(human_questions(c)) <= 3 + 3  # H1, H2, H3, and at most a few machine checks put back to the human, in red
        assert {"H1", "H2"} <= human_questions(c) and "Machine checks:" in c
    # unless a machine check failed, exactly H1, H2 (and H3 on a and b) are asked
    plain = [c for c in cards if "Machine checks: all pass" in c]
    want = {"H1", "H2"} | ({"H3"} if view_id in ("main_swap", "answer_control") else set())
    assert all(human_questions(c) == want for c in plain)


def test_the_five_items_follow_the_rule_and_come_from_the_fixed_sample():
    fs = I.spec()["fixed_sample"]["views"]
    order = list(I.spec()["models"])
    for vid in WITH_QUESTIONS:
        five = Q.five_ids(vid)
        sample = {e["item"]: e for e in fs[vid]}
        assert set(five) <= set(sample), vid
        rnd, sur = [sample[i] for i in five[:3]], [sample[i] for i in five[3:]]
        assert all(e["stratum"].startswith("random") for e in rnd) and all("surprising" in e["stratum"] for e in sur), vid
        assert [e["model"] for e in rnd] == sorted({e["model"] for e in rnd}, key=order.index), vid  # the yaml's model order
        assert rnd[0]["model"] == "qwen3.5-9b" or "qwen3.5-9b" not in {e["model"] for e in fs[vid] if e["stratum"].startswith("random")}
    assert "Five items per view" in I.spec()["five_rule"]


def test_the_fixed_sample_shows_only_the_five(tmp_path):
    from bridge_jspace.review import fixed as F

    got = F.samples(I.view("main_swap"), 29, list(I.spec()["models"]))
    ids = [it["id"] for per in got.values() for s in per for it in s["items"]]
    assert sorted(ids) == sorted(Q.five_ids("main_swap"))


def test_per_view_reads_the_five_and_counts_the_rest_as_extra(tmp_path):
    five = Q.five_ids("main_swap")
    other = next(e["item"] for e in I.spec()["fixed_sample"]["views"]["main_swap"] if e["item"] not in five)
    rows = [{"view": "main_swap", "item": five[0], "seed": 29, "verdict": "wrong", "note": ""},
            {"view": "main_swap", "item": five[1], "seed": 29, "verdict": "consistent", "note": ""},
            {"view": "main_swap", "item": other, "seed": 29, "verdict": "unclear", "note": ""}]  # fmt: skip
    x = H.per_view(rows)["main_swap"]
    assert (x["sample"], x["read"], x["wrong"], x["consistent"], x["extra"]) == (5, 2, 1, 1, 1)
    line = Q.deck_line("main_swap", rows, [])
    assert line.startswith("main_swap: 5 items: 1 consistent, 1 wrong, 0 unclear") and "1 extra" in line and "machine:" in line


def test_a_marked_card_folds_to_its_header():
    it = two_items("main_swap")[0]
    html = P.card(it, 29, False, {"verdict": "wrong"})
    assert "data-verdict='wrong'" in html and "toggleCard(this)" in html and "class='vtag'" in html
    assert "data-verdict=''" in P.card(it, 29, False, None)
    page = P.page("t", html, False, "x")
    assert ".card.done>:not(.hdr):not(.idl){display:none}" in page and "function fold(" in page and "nextCard(c)" in page
