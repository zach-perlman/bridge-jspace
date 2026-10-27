"""natural_read (finding 4 on natural text): the sentence splitter, the item filters and the build on hand-made
SQuAD-style paragraphs, the competence eligibility, the verdict's rule on synthetic knockout rows, and attn_knockout's
case on the target's tokenizer (skipped when it is not cached)."""

import random

import pytest

from scripts import natural_read as NR

HARBOUR = ("The old harbour was built by Dr. Marten Holm in 1820. Ships from Lisbon unloaded spices on its northern quay. "
           "The town council later paved the main square with grey granite. A small museum now shows the tools used by "
           "the first dockworkers. Every summer the harbour hosts a regatta for wooden sailing boats.")  # fmt: skip
PUFFINS = ("Puffins return to the northern cliffs every April. Each instance of the island survey counts their burrows. "
           "Volunteers record the instances in a shared notebook. The survey began after a storm destroyed many nests. "
           "Today the colony is protected by a ranger named Ingrid Solberg.")  # fmt: skip
SHORT = "Gulls nest on the roofs. They are loud. Nobody minds."


def _q(qid: str, question: str, passage: str, *answers: str) -> dict:
    return {"id": qid, "question": question,
            "answers": [{"text": a, "answer_start": passage.index(a)} for a in answers]}  # fmt: skip


RAW = {"data": [
    {"title": "Alpha", "paragraphs": [{"context": HARBOUR, "qas": [
        _q("a1", "What did ships from Lisbon unload on the northern quay?", HARBOUR, "spices"),
        _q("a2", "When was the old harbour built?", HARBOUR, "1820"),  # starts with a digit
        _q("a3", "Who paved the main square?", HARBOUR, "town council", "council"),  # annotators start differently
    ]}]},
    {"title": "Beta", "paragraphs": [
        {"context": PUFFINS, "qas": [
            _q("b1", "What do volunteers record in a shared notebook?", PUFFINS, "instances"),  # instance / instances
            _q("b2", "Who protects the colony now?", PUFFINS, "Ingrid Solberg"),
        ]},
        {"context": SHORT, "qas": [_q("c1", "Where do gulls nest?", SHORT, "roofs")]},  # 3 sentences
    ]},
]}  # fmt: skip


def _texts(text: str) -> list[str]:
    return [text[a:b] for a, b in NR.split_sentences(text)]


def test_split_sentences_keeps_abbreviations_initials_and_lowercase_continuations():
    assert _texts(HARBOUR)[0] == "The old harbour was built by Dr. Marten Holm in 1820."
    assert len(_texts(HARBOUR)) == 5
    assert _texts("J. R. R. Tolkien served in the U.S. Army. He wrote books.") == [
        "J. R. R. Tolkien served in the U.S. Army.", "He wrote books."]  # fmt: skip
    assert _texts("He left. then she stayed. Is it over? Yes!") == ["He left. then she stayed.", "Is it over?", "Yes!"]
    assert _texts('He said "Go!" Then he left. In 1685, Rev. Elie Prioleau came.') == [
        'He said "Go!"', "Then he left.", "In 1685, Rev. Elie Prioleau came."]  # fmt: skip


def test_candidate_strips_the_article_and_locates_the_answer_sentence():
    sents = NR.split_sentences(HARBOUR)
    q = _q("x", "Who paved the main square?", HARBOUR, "The town council")
    it = NR.candidate(HARBOUR, sents, q, random.Random(0))
    assert it is not None
    assert it["answer"] == "town council" and HARBOUR[slice(*it["answer_char"])] == "town council"
    assert it["answer_sentence"] == 2 and it["off_sentence"] in (0, 4)  # two or more sentences away
    a, b = sents[it["off_sentence"]]
    assert NR.OFF_RATIO[0] <= (b - a) / (sents[2][1] - sents[2][0]) <= NR.OFF_RATIO[1]


@pytest.mark.parametrize("qid", ["a2", "a3", "b1"])
def test_candidate_drops_digits_annotator_disagreement_and_shared_prefixes(qid):
    art = RAW["data"][0]["paragraphs"][0] if qid[0] == "a" else RAW["data"][1]["paragraphs"][0]
    q = next(q for q in art["qas"] if q["id"] == qid)
    assert NR.candidate(art["context"], NR.split_sentences(art["context"]), q, random.Random(0)) is None


def test_build_one_item_per_paragraph_and_a_swap_partner_from_another_article():
    items, counts = NR.build(RAW)
    assert counts == {"paragraphs": 3, "questions": 6, "paragraphs_kept": 2, "questions_kept": 2, "items": 2,
                      "articles": 2}  # fmt: skip
    by = {it["squad_id"]: it for it in items}
    assert set(by) == {"a1", "b2"}
    assert by["b2"]["answer"] == "Ingrid Solberg" and by["b2"]["off_sentence"] == 1  # the closest length, far enough
    assert by["a1"]["swap_partner"] == by["b2"]["id"] and by["b2"]["swap_partner"] == by["a1"]["id"]
    assert NR.build(RAW) == (items, counts)  # seeded


def test_prompts_delete_or_isolate_the_answer_sentence():
    items, _ = NR.build(RAW)
    it = next(i for i in items if i["squad_id"] == "a1")
    by_id = {i["id"]: i for i in items}
    p = NR.prompt_contents(it, by_id)
    assert set(p) == set(NR.KINDS)
    assert p["full"] == f"{HARBOUR}\n{it['question']} {NR.INSTRUCTION}"
    assert p["alone"].startswith("Ships from Lisbon unloaded spices on its northern quay.\n")
    assert "spices" not in p["deleted"] and "1820. The town council" in p["deleted"]
    assert p["swapped"].startswith(PUFFINS)


def test_greedy_judge_and_eligibility():
    assert NR.greedy_right(" The Spices.\nmore", ["spices"])
    assert NR.greedy_right("\n\nspices and silk", ["spices"])
    assert not NR.greedy_right(" silk\nspices", ["spices"])

    def rows(i, full, greedy, alone, deleted):
        return [{"id": i, "kind": "full", "right": full, "greedy_right": greedy}, {"id": i, "kind": "alone", "right": alone},
                {"id": i, "kind": "deleted", "right": deleted}, {"id": i, "kind": "swapped", "right": False}]  # fmt: skip

    got = rows("ok", True, True, True, False) + rows("needs-no-sentence", True, True, True, True)
    got += rows("first-token-only", True, False, True, False) + rows("sentence-not-enough", True, True, False, False)
    assert NR.eligible_ids(got) == {"ok"}

    # the funnel (built -> eligible): each item dropped once, at its first failing criterion, in CRITERIA's order
    got += rows("short-one", True, True, True, False) + rows("wrong-everywhere", False, False, False, True)
    f = NR.eligibility_funnel(got, {"short-one"})
    assert (f["built"], f["eligible"]) == (6, len(NR.eligible_ids(got) - {"short-one"})) == (6, 1)
    assert [s["dropped"] for s in f["steps"]] == [1, 1, 1, 1, 1]
    assert [s["left"] for s in f["steps"]] == [5, 4, 3, 2, 1]
    assert list(f["failing_each_criterion_alone"].values()) == [1, 1, 2, 2, 2]
    assert [s["dropped_by"] for s in f["steps"]] == [why for why, _ in NR.CRITERIA]
    assert "neighbouring sentence" in f["coverage"]


def _run(n: int, late: int, off: int, gdn: int | None, floor: int) -> tuple[list[dict], dict, list[dict]]:
    """Synthetic attn_knockout rows on n items (all right unedited): the first k items right in each cell."""
    hybrid = gdn is not None
    att = "attn" if hybrid else "all"
    cells = [("lookup", "final", att, "value", late), ("lookup_off", "final", att, "value", off),
             ("lookup", "after", "all", "absent" if hybrid else "value", floor), ("lookup", "question", "all", "value", 0)]  # fmt: skip
    if hybrid:
        cells += [("lookup", "final", "gdn", "value", gdn), ("lookup", "final", "all", "value", late)]
    rows = []
    for k in range(n):
        i = f"NAT-{k:04d}"
        rows.append({"id": i, "family": "NAT", "source": "none", "dest": "-", "layers": "-", "mode": "-", "correct": True, "top": 7})  # fmt: skip
        for src, dest, layers, mode, right in cells:
            rows.append({"id": i, "family": "NAT", "source": src, "dest": dest, "layers": layers, "mode": mode,
                         "correct": k < right, "top": 7 if k < right else 9})  # fmt: skip
    cases = {f"NAT-{k:04d}": {"tok_A": 7, "domain": f"article{k % 6}"} for k in range(n)}
    comp = [{"id": f"NAT-{k:04d}", "kind": "swapped", "right": False} for k in range(n)]
    return rows, cases, comp


@pytest.mark.parametrize(("n", "late", "off", "gdn", "floor", "want", "want_secondary"), [
    (150, 15, 148, 150, 0, "holds", "holds"),  # 10% [6, 16]
    (150, 15, 148, None, 0, "holds", "holds"),  # a model without DeltaNet layers
    (150, 9, 148, 150, 0, "holds", "holds"),  # 6% [3, 11]
    (150, 25, 148, 150, 0, "fails (more than 10% right, or the upper bound above 20%)", "holds"),  # 17% [12, 23]
    (150, 17, 148, 150, 0, "fails (more than 10%", "holds"),  # 11%: the point fails the primary bar
    (150, 45, 148, 150, 0, "fails (more than 10%", "fails (more than 20% right, or the upper bound above 30%)"),
    (150, 15, 148, 120, 0, "fails (the DeltaNet layers", "fails (the DeltaNet layers"),
    (150, 15, 120, 150, 0, "not interpretable (the off-path", "not interpretable (the off-path"),
    (150, 15, 148, 150, 30, "not interpretable (the answer's sentence hidden from everything", "not interpretable"),
    (80, 0, 80, 80, 0, "not testable", "not testable"),
])  # fmt: skip
def test_verdict_rule(n, late, off, gdn, floor, want, want_secondary):
    out = NR.verdict(*_run(n, late, off, gdn, floor))
    assert out["verdict"].startswith(want)
    assert out["verdict_secondary"].startswith(want_secondary)
    assert out["bars"] == {"primary": (0.10, 0.20), "secondary": (0.20, 0.30)}
    assert out["n_right_unedited"] == n and out["layers_for_late"] == ("attn" if gdn is not None else "all")
    assert out["cells"]["late"]["rate"][0] == pytest.approx(late / n)
    # the blocked answers scored against another item's answer: here every item shares one answer token, so the
    # shuffled key scores exactly what the real key does
    assert out["baselines"]["late_scored_against_another_items_answer"][0] == pytest.approx(late / n)


def test_figure_draws_a_cell_at_100_percent(tmp_path):
    # 21 of 21: stats.wilson's upper bound is 0.9999999999999999, ~1e-16 under the rate; the figure must still draw
    # (the 9B's and 32B's natural-text figures failed on this, 23 Oct)
    out = NR.verdict(*_run(21, 2, 21, 21, 0))
    assert out["cells"]["off"]["rate"][2] < out["cells"]["off"]["rate"][0]
    out["eligibility_funnel"] = {"built": 21, "eligible": 21}
    out["model"] = {"repo": "Qwen/Qwen3.5-9B"}
    NR.figure(out, tmp_path / "f.png")
    assert (tmp_path / "f.png").stat().st_size > 10_000


def test_stage_verdict_writes_a_new_analysis_folder_with_the_figure(tmp_path, monkeypatch):
    import json

    from scripts import attn_knockout as AK

    rows, cases, comp = _run(150, 15, 148, 150, 0)
    run = tmp_path / "ko" / "run1"
    run.mkdir(parents=True)
    (run / "rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (run / "cases.jsonl").write_text("".join(json.dumps({"id": i, **c}) + "\n" for i, c in cases.items()))
    (run / "manifest.json").write_text(json.dumps({"model": {"repo": "Qwen/Qwen3.6-27B"}}))
    (tmp_path / "nr" / "comp1").mkdir(parents=True)
    (tmp_path / "nr" / "comp1" / "items.jsonl").write_text("".join(json.dumps(r) + "\n" for r in comp))
    funnel = {"built": 718, "eligible": 150, "coverage": NR.COVERAGE,
              "steps": [{"dropped_by": why, "dropped": 0, "left": 718} for why, _ in NR.CRITERIA],
              "failing_each_criterion_alone": {why: 0 for why, _ in NR.CRITERIA}}  # fmt: skip
    (tmp_path / "nr" / "comp1" / "summary.json").write_text(json.dumps({"eligibility_funnel": funnel}))
    monkeypatch.setattr(AK, "RESULTS", tmp_path / "ko")
    monkeypatch.setattr(NR, "RESULTS", tmp_path / "nr")
    NR.stage_verdict("run1", "comp1")
    (folder,) = run.glob("analysis-*-verdict")
    v = json.loads((folder / "verdict.json").read_text())
    assert (v["verdict"], v["verdict_secondary"], v["eligibility_funnel"]["built"]) == ("holds", "holds", 718)
    assert (folder / "natural_late_read.png").stat().st_size > 10_000
    md = (folder / "verdict.md").read_text()
    assert "| answer's sentence hidden from the last tokens | 10% [6, 16] | 150 |" in md
    assert "Verdict (primary, <= 10% right with the upper bound <= 20%): **holds**" in md
    assert "Verdict (secondary, finding 4's bar <= 20% / <= 30%): holds" in md
    assert "718 built -> 150 eligible" in md
    assert NR.COVERAGE in md


@pytest.fixture(scope="module")
def tok():
    try:
        return NR.cached_tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


def test_natural_case_spans_and_destinations(tok):
    from scripts import attn_knockout as AK

    items, _ = NR.build(RAW)
    it = next(i for i in items if i["squad_id"] == "b2")
    c = AK.natural_case(it, tok)
    dec = lambda pos: tok.decode([c["ids"][p] for p in pos])  # noqa: E731
    assert "Today the colony is protected by a ranger named Ingrid Solberg." in dec(c["sources"]["lookup"])
    assert "Each instance of the island survey counts their burrows." in dec(c["sources"]["lookup_off"])
    assert not set(c["sources"]["lookup"]) & set(c["sources"]["lookup_off"])
    assert dec(c["dests"]["question"]).strip() == f"{it['question']} {NR.INSTRUCTION}"
    assert dec(c["dests"]["final"]).endswith("Answer:") and "Ingrid" not in dec(c["dests"]["final"])
    assert tok.decode([c["tok_A"]]).strip() == "Ingrid" or "Ingrid".startswith(tok.decode([c["tok_A"]]).strip())
    assert c["query_slot"] == 4 and len(c["statements"]) == 5
    assert max(max(s) for s in c["sources"].values()) < min(c["dests"]["question"])
