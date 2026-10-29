"""The automatic checks (scripts/verify_checks.py) and the fixed sample (src/bridge_jspace/review/fixed.py) on planted
data: each check passes on clean rows and fails on the planted fault; the sample's strata and targeted picks."""

import json

import pytest

from bridge_jspace.review import fixed as F
from bridge_jspace.review import items as I
from scripts import verify_checks as VC


@pytest.fixture
def repo(tmp_path, monkeypatch):
    I.read_jsonl.cache_clear()
    monkeypatch.setattr(I, "REPO", tmp_path)
    yield tmp_path
    I.read_jsonl.cache_clear()


def put(root, rel: str, rows) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rows) if rel.endswith(".json") else "".join(json.dumps(r) + "\n" for r in rows))


def comp(scene: str, alt_ok: bool = True, org_read: bool = True) -> list[dict]:
    """The original answer said right, read right unless org_read is False; the changed answer right iff alt_ok."""
    return [{"scene": scene, "rendering": "chat", "reader": w, "variant": v, "right": v == "org" or alt_ok,
             "read_right": org_read if v == "org" else alt_ok} for w in ("PP", "PM") for v in ("org", "alt")]  # fmt: skip


RUN = "results/x0_necessity/planted"


def plant_x0(root, gate_pass=True, eligible=4, excluded=()):
    scenes = [f"s{i}" for i in range(6)]
    put(root, f"{RUN}/manifest.json", {"gate": 0.8, "n": {"items": 3}, "excluded_scenes": list(excluded)})
    put(root, f"{RUN}/gate.json", {"gate": {"chat": {"org_accuracy": {}, "pass": gate_pass, "eligible": eligible}}})
    put(root, f"{RUN}/cases.jsonl", [{"scene": s, "rendering": "chat"} for s in scenes])
    # s2 and s5 ineligible (a reader wrong): eligible s0 s1 s3 s4; s5's org read wrong -> accuracy 5/6 >= 0.8
    put(root, f"{RUN}/competence.jsonl", [r for s in scenes for r in comp(s, s not in ("s2", "s5"), s != "s5")])


def items_of(scenes):
    return [{"scene": s} for s in scenes]


def test_gate_and_eligibility_pass_on_clean_rows_and_fail_on_a_wrong_item_set(repo):
    plant_x0(repo)
    got = {c["check"]: c["status"] for c in VC.gate_x0(RUN, items_of(["s0", "s1", "s3"]))}
    assert set(got.values()) == {"pass"}
    got = {c["check"]: c["status"] for c in VC.gate_x0(RUN, items_of(["s0", "s1", "s2"]))}  # s2 is not eligible
    assert got["eligibility and the item set recomputed"] == "fail"
    plant_x0(repo, gate_pass=False)  # the stored gate says fail, the recount says pass
    I.read_jsonl.cache_clear()
    assert VC.gate_x0(RUN, items_of(["s0", "s1", "s3"]))[0]["status"] == "fail"


def test_excluded_dev_scenes_are_left_out_of_the_first_n(repo):
    plant_x0(repo, excluded=["s1"])
    got = VC.gate_x0(RUN, items_of(["s0", "s3", "s4"]))
    assert got[1]["status"] == "pass" and "excluded 1 dev scenes" in got[1]["detail"]


def test_duplicates_and_shares(repo):
    v = {"kind": "x0"}
    rows = [
        {
            "scene": "s0",
            "rendering": "chat",
            "layer": 12,
            "reader": "PP",
            "dict": "-",
            "k": 0,
            "omp": "-",
            "arm": "whole",
        }
    ]
    put(repo, f"{RUN}/outcomes.jsonl", rows + rows)  # one key twice
    case = {"readers": {"PP": {"ids": {"org": [1, 2], "alt": [1, 3]}}}}
    its = [
        {"id": "a", "run": RUN, "scene": s, "reader": "PP", "condition": None, "x8": {}, "case": case}
        for s in ("s0", "s1")
    ]
    dup = VC.duplicates(v, its)
    assert dup[f"{RUN}/outcomes.jsonl rows with one key"] and dup["item ids"] == ["a"]
    assert dup["items with identical prompts"] == [["s0", "s1"]]
    put(repo, f"{RUN}/shares.jsonl", [
        {"scene": "s0", "rendering": "chat", "layer": 12, "dict": "jpp", "k": 25, "omp": "signed", "share": 0.30, "rand_share": 0.301},
        {"scene": "s1", "rendering": "chat", "layer": 12, "dict": "jpp", "k": 25, "omp": "signed", "share": 0.30, "rand_share": 0.25}])  # fmt: skip
    got = VC.conflict_shares(v, "m", [{"run": RUN, "layer": 12, "scene": s} for s in ("s0", "s1")])
    assert got[0]["status"] == "fail" and "beyond 0.01: 1" in got[0]["detail"]


def test_summary_totals_per_tier_and_the_e1_agreement():
    lab = {"check": "labels against the 51.12 E1 rerun (top token stored)", "status": "fail",
           "counts": {"whole": {"agree": 393, "n": 400}}}  # fmt: skip
    res = {"views": {
        "main_swap": {"models": {"m": {"n": 400, "item_fail": {}, "run_checks": [lab]}}, "recount": {"match": 3, "mismatch": []}},
        "z1p": {"models": {"m": {"n": 400, "item_fail": {"only the scene's words differ": 4}, "run_checks": []}},
                "recount": {"match": 3, "mismatch": [{"q": 1}]}},
        "natural": {"models": {"m": {"n": 60, "item_fail": {}, "run_checks": []}}, "recount": {"match": 2, "mismatch": []}}}}  # fmt: skip
    s = VC.summarize(res, {"main_swap": 1, "z1p": 1, "natural": 2})
    assert (
        s["tier1"]["items"] == 800 and s["tier1"]["item_check_failures"] == 4 and s["tier1"]["run_check_failures"] == 1
    )
    assert s["tier1"]["recount"] == {"match": 6, "mismatch": 1, "numbers": 7} and s["tier2"]["items"] == 60
    assert s["e1_label_agreement"] == {"m": {"whole": {"agree": 393, "n": 400}}}


def test_zach_facts_fail_where_planted():
    def it(scene, made, true, there):
        return {"scene": scene, "reader": "PP", "more": {"facts": {"made_up": made, "true": true, "true_in_lookup_passage": there,
                "cf_true_in_changed_lookup_passage": False}}}  # fmt: skip

    got = {
        c["check"]: c["status"]
        for c in VC.zach_facts([it("a", "Greek", "Hungarian", False), it("b", "Greek", "greek", True)])
    }
    assert got["Z1-P: the made-up value differs from the true one"] == "fail"
    assert got["Z1-P: the true value is absent from the lookup's passage"] == "fail"
    got = {c["check"]: c["status"] for c in VC.zach_facts([it("a", "Greek", "Hungarian", False)])}
    assert (
        got["Z1-P: the made-up value differs from the true one"]
        == got["Z1-P: the true value is absent from the lookup's passage"]
        == "pass"
    )


def test_word_in_matches_whole_words_only():
    assert I.word_in("Russia", "The partner city for Mumbai is in Russia.")
    assert not I.word_in("Iran", "The partner city is in Tirana.")


# ---- the fixed sample -------------------------------------------------------------------------------------------
def test_the_stored_sample_is_what_a_fresh_draw_gives_and_loads():
    """No re-rolls: the views file's fixed sample (seed 29) equals a fresh draw on the repo's runs, item by item, and
    every item still loads (a loader change that moved an item would fail here, not silently tomorrow)."""
    fs = I.spec()["fixed_sample"]
    assert fs["seed"] == 29 and fs["n_per_view"] == 10
    for v in F.tier1():
        stored = fs["views"][v["id"]]
        assert [e["item"] for e in F.draw(v, 29)] == [e["item"] for e in stored], v["id"]
        got = F.samples(v, 29, list(I.spec()["models"]))
        assert sum(len(x) for x in got.values()) == len(stored) == 10


def test_strata_cover_every_model_and_balance_the_readers():
    models = ["a", "b", "c", "d", "e"]
    s = F.strata(models, 29, "v")
    assert len(s) == 6 and {m for m, _ in s} == set(models) and sum(w == "PP" for _, w in s) == 3
    assert s == F.strata(models, 29, "v") and s != F.strata(models, 30, "v")
    one = F.strata(["a"], 29, "v")
    assert [w for _, w in one] == ["PP", "PM"] * 3


def row(sw, p_org=0.5, p_alt=0.4, role="A"):
    return {"switched": sw, "p_org": p_org, "p_alt": p_alt, "ld": p_alt - p_org, "role": role}


def item(i, w, part_sw, rand_sw, margin=0.5, whole=1):
    return {"id": f"m|r|s{i}|{w}", "model": "m", "reader": w, "scene": f"s{i}", "kind": "x0", "condition": None, "x8": {},
            "case": {"readers": {w: {"tok_A": 1, "tok_b": 2}}},
            "rows": {w: {"whole": row(whole, 0.1, 0.9, "b"), "p": row(part_sw, 0.5 - margin / 2, 0.5 + margin / 2),
                         "r": row(rand_sw)}}}  # fmt: skip


def test_targeted_picks_the_nearest_and_one_surprise_per_direction():
    v = {"id": "v", "targeted": {"nearest": ["p"], "surprising": {"reader": "PP", "part": "p", "random": "r"}}}
    pool = [
        item(0, "PP", 1, 0, margin=0.30),
        item(1, "PP", 0, 1, margin=0.20),
        item(2, "PM", 0, 0, margin=0.01),
        item(3, "PM", 0, 0, margin=0.02),
        item(4, "PP", 1, 0, margin=0.9),
        item(5, "PP", 0, 1, margin=0.9),
        item(6, "PM", 0, 0, margin=0.001, whole=0),
    ]  # s6: the whole change did not switch it, so not counted
    got = F.draw_targeted(v, pool, 29, set())
    near = [it["scene"] for it, why in got if "nearest" in why]
    assert near == ["s2", "s3"]
    sur = [why for it, why in got if "surprising" in why]
    assert (
        len(sur) == 2
        and any("under 'p', not under 'r'" in w for w in sur)
        and any("under 'r', not under 'p'" in w for w in sur)
    )


# ---- the pack ---------------------------------------------------------------------------------------------------
def test_the_pack_keeps_the_inspectors_section_and_quotes_the_readme():
    from scripts import verify_pack_tier1 as VP

    old = f"# x\n\n{VP.INSPECTOR}\n\nRanks: 12 of 200 in the top 50 (planted).\n\n## a. main_swap\n\nold text\n"
    new = VP.build(old)
    assert "Ranks: 12 of 200 in the top 50 (planted)." in new and "old text" not in new
    assert new.index("## How to review in 2 hours") < new.index("## Automatic checks") < new.index(VP.INSPECTOR)
    assert VP.INSPECTOR_TODO in VP.build("")  # no section yet: the stub
    assert "the 122B's answer control landed after the sample was fixed; not in the hand-check" in new
    for v in (v for v in I.spec()["views"] if v.get("tier") == 1):
        assert f"## {v['order']}. {v['id']}" in new
        for q in VP.readme_quotes(v.get("readme_quotes") or []):
            assert not q.startswith("(not found") and "<!--" not in q
    assert "60 of 200 lookup passages" in new.split("## e. z1p", 1)[1].split("**The claim", 1)[0]  # read first


def test_the_pack_includes_the_inspectors_file_verbatim(tmp_path, monkeypatch):
    from scripts import verify_pack_tier1 as VP

    f = tmp_path / "verify_pack_jspace.md"
    f.write_text("Rank of S's bridge token in the rest: top 50 on 3% of items (planted).\n")
    monkeypatch.setattr(VP, "JSPACE", f)
    new = VP.build(f"{VP.INSPECTOR}\n\nan older text\n\n## a. main_swap\n")
    sec = new.split(VP.INSPECTOR, 1)[1].split("\n## a. ", 1)[0]
    assert "top 50 on 3% of items (planted)." in sec and "an older text" not in sec


# ---- the hand marks read back: review-summary and VERIFIED.md ----------------------------------------------------
def marks_file(tmp_path, rows):
    p = tmp_path / "marks.jsonl"
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


def test_marks_skip_jspace_notes_count_the_last_verdict_and_apply_the_stop_rule(tmp_path):
    from bridge_jspace.review import handcheck as H

    fs = I.spec()["fixed_sample"]
    a, b, c = (e["item"] for e in fs["views"]["main_swap"][:3])
    seed = fs["seed"]
    rows = [{"view": "main_swap", "item": a, "seed": seed, "verdict": "consistent"},
            {"view": "main_swap", "item": a, "seed": seed, "verdict": "wrong", "note": "label b, top '7'"},  # the last counts
            {"view": "main_swap", "item": b, "seed": seed, "verdict": "wrong"},
            {"view": "main_swap", "item": c, "seed": seed, "kind": "jspace", "note": "identity token in the rest at L14"},
            {"view": "main_swap", "item": c, "seed": 7, "verdict": "consistent"},  # another seed: not the fixed sample's read
            {"view": "routes", "item": "not|in|the|sample", "seed": seed, "verdict": "unclear"}]  # fmt: skip
    marks = H.load_marks(marks_file(tmp_path, rows))
    assert len(marks) == 5 and all(r.get("kind") != "jspace" for r in marks)
    pv = H.per_view(marks)
    m = pv["main_swap"]
    assert (m["read"], m["consistent"], m["wrong"], m["unclear"], m["flagged"]) == (2, 0, 2, 0, True)
    assert pv["routes"]["read"] == 0 and pv["routes"]["outside_sample"] == 1


def test_verified_writes_only_its_block_and_replaces_it(tmp_path):
    from scripts import verified as VF

    out = tmp_path / "VERIFIED.md"
    out.write_text("# VERIFIED\n\nHuman text, kept.\n")
    item = I.spec()["fixed_sample"]["views"]["z1p"][0]["item"]
    mk = marks_file(tmp_path, [{"view": "z1p", "item": item, "seed": 29, "verdict": "unclear", "note": "passage cut"}])
    VF.main(["--marks", str(mk), "--out", str(out)])
    VF.main(["--marks", str(mk), "--out", str(out)])  # twice: one block
    text = out.read_text()
    assert (
        text.startswith("# VERIFIED\n\nHuman text, kept.\n") and text.count(VF.BEGIN) == 1 and text.count(VF.END) == 1
    )
    assert "| e. z1p |" in text and "1 of 10 | 0 | 0 | 1 | no |" in text and "passage cut" in text


# ---- examples-render SEED=29: the write-up's examples are the items Dan read ----------------------------------------
def test_writeup_exports_the_fixed_sample(tmp_path):
    from bridge_jspace.review import writeup as W

    out = W.export(29, tmp_path)
    md = (out / "examples.md").read_text()
    fs = I.spec()["fixed_sample"]["views"]
    assert md.count("\n#### ") == sum(len(x) for x in fs.values()) == 70
    assert all(f"`{e['scene']}`" in md for x in fs.values() for e in x)
    src = json.loads((out / "source.json").read_text())["entry"]
    assert src["n_examples"] == 70 and [g["n_total"] for g in src["groups"]] == [10] * 7
    assert "Answer:" in md and "<|im_start|>" in md  # the prompt as the model saw it


def test_job_pages_take_only_the_examples_stage_schema(tmp_path):
    from bridge_jspace import job_pages as J

    put(tmp_path, "results/a/examples.json", [{"bridge": "x"}])  # another writer's schema (x47_verbal)
    put(tmp_path, "results/b/examples.json", {"examples": [], "groups": []})
    assert J.find_examples(tmp_path, {"new_results": ["a"]}) is None
    assert J.find_examples(tmp_path, {"new_results": ["a", "b"]}) == {"examples": [], "groups": []}
    html = J._example_html({"answers": {"clean": "Beijing", "edited": "Tehran", "expected": "Tehran"}}, {})
    assert "Tehran" in html  # one expected answer (code_positions), not one per hypothesis
