"""The review dashboard (src/bridge_jspace/review/, scripts/review.py) on the repo's runs: deterministic samples, the
item sets against the verdicts' n, the class re-derivation on hand-picked items, and checks that fail on bad data.
Batch 45's views (45k, 45m, the 45b sweep; and, scored, 45a, 45d, 45e, 45g) on planted runs in each writer's layout,
and on the repo before and after they land."""

import copy
import glob
import html
import json

import pytest

from bridge_jspace.review import checks as C
from bridge_jspace.review import items as I

MODELS = ("qwen3.5-9b", "qwen3.6-27b", "qwen3.5-122b-a10b", "muse-glimmer-30b")


def latest(run: str) -> dict:
    return json.loads(open(sorted(glob.glob(f"{I.REPO}/{run}/verdict-*/verdict.json"))[-1]).read())


def test_same_seed_same_items_other_seed_other_items():
    pool = I.items("main_swap", "qwen3.5-9b")

    def ids(seed: int) -> list[str]:
        return [it["id"] for s in I.sample(pool, seed, 5, "uniform", "main_swap", "qwen3.5-9b") for it in s["items"]]

    assert ids(7) == ids(7) and ids(7) != ids(8)
    strat = I.sample(pool, 7, 3, "stratified", "main_swap", "qwen3.5-9b")
    assert sum(s["population"] for s in strat) == len(pool) and all(len(s["items"]) <= 3 for s in strat)


@pytest.mark.parametrize("view_id", ["main_swap", "single_change"])
def test_x0_item_sets_match_the_verdicts_n(view_id):
    v = I.view(view_id)
    for m in MODELS:
        run = v["runs"][m][0]
        layer = I.spec()["models"][m]["layer"]
        cells = latest(run)["cells"]
        got = I.items(view_id, m)
        for w in I.READERS:
            cell = next(c for c in cells if (c["rendering"], c["layer"], c["reader"], c["dict"], c["k"], c["omp"]) ==
                        ("chat", layer, w, "jpp", 25, "signed"))  # fmt: skip
            assert sum(it["reader"] == w for it in got) == cell["n"], (m, w)


@pytest.mark.parametrize("view_id", ["routes", "routes_early"])
def test_routes_item_sets_match_the_verdicts_n(view_id):
    v = I.view(view_id)
    for m in MODELS:
        rows = latest(v["runs"][m][0])["rows"]
        got = I.items(view_id, m)
        for r in rows:
            if r["arm"] == "whole":
                n = sum(it["condition"] == r["condition"] and it["reader"] == "PP" for it in got)
                assert n == r["n"], (m, r["condition"])


def test_pointer_item_sets_match_the_verdicts_n():
    v = I.view("pointer_main")
    for m in MODELS:
        got = I.items("pointer_main", m)
        for r in latest(v["runs"][m][0])["rows"]:
            assert sum(it["reader"] == r["reader"] for it in got) == r["n"], (m, r["reader"])


def item(view_id: str, model: str, scene: str, reader: str, **x8) -> dict:
    return next(it for it in I.items(view_id, model) if it["scene"] == scene and it["reader"] == reader
                and all(it["x8"].get(k) == val for k, val in x8.items()))  # fmt: skip


def test_class_rederivation_on_hand_picked_items():
    # routes C2, read by hand (9B): O crow 4 / butterfly 9 / dog 2, Henry picked the butterfly; S moves the crow to slot
    # 2 with 7, Henry picked the crow: identity 4, position 2, value 7, original 9; the whole change reads '2'
    it = item("routes", "qwen3.5-9b", "C2-0333", "PP")
    assert C.piece("qwen3.5-9b", it["rows"]["PP"]["whole"]["top"]).strip() == "2"
    assert C.route_of("2", it["case"]["expect"], "C2") == "position" == it["rows"]["PP"]["whole"]["route"]
    # C0 quirk: a correct switch is stored as route "other"; re-derived from expect it is the switch
    it = item("routes", "qwen3.5-9b", "C0-0001", "PP")
    whole = it["rows"]["PP"]["whole"]
    assert whole["route"] == "other" and whole["switched"] == 1
    assert C.route_of(C.piece("qwen3.5-9b", whole["top"]).strip(), it["case"]["expect"], "C0") == "switch"
    assert I.route_class(whole, "C0") == "switch"
    # x8 (9B), C2-0001: the goose is slot 2; the write 2 -> 1 at s = 4 reads slot 1's digit: target
    it = item("x8_writes", "qwen3.5-9b", "C2-0001", "PP", kind="write", j=2, k=1, s=4)
    assert it["cls"] == "target"
    for view_id, m in (("routes", "qwen3.5-9b"), ("x8_writes", "qwen3.5-9b"), ("routes_early", "muse-glimmer-30b")):
        for it in I.items(view_id, m)[:50]:
            assert C.run_checks(it)["label from the top token"][0] == C.PASS, it["id"]


def test_sentence_order_and_its_filter():
    # read by hand: "Finn picked helium. The locker of hydrogen is three. Clara picked hydrogen. ... The locker of helium
    # is six." -> the original bridge's locker before Clara's pick (locker-first); the changed bridge's after it
    it = item("main_swap", "qwen3.5-9b", "P2-L0-0247", "PM")
    assert it["order"] == {"original": "before", "changed": "after"}
    pool = I.items("main_swap", "qwen3.5-9b")
    first = [x for x in pool if I.facets(x, {"order": "locker first"})]
    assert first and all(x["order"]["original"] == "before" for x in first) and len(first) < len(pool)


def test_checks_fail_on_tampered_items():
    it = copy.deepcopy(item("routes", "qwen3.5-9b", "C2-0333", "PP"))
    it["rows"]["PP"]["whole"]["route"] = "identity"
    assert C.run_checks(it)["label from the top token"][0] == C.FAIL
    it = copy.deepcopy(item("main_swap", "qwen3.5-9b", I.items("main_swap", "qwen3.5-9b")[0]["scene"], "PP"))
    it["case"]["pos"] -= 1
    assert C.run_checks(it)["bridge at the change's token"][0] == C.FAIL
    row = it["rows"]["PP"]["whole"]
    row["switched"] = 1 - row["switched"]
    assert C.run_checks(it)["probabilities agree with the label"][0] == C.FAIL
    it["case"]["readers"]["PP"]["ids"]["alt"] = it["case"]["readers"]["PP"]["ids"]["alt"][:-1]
    assert C.run_checks(it)["only the scene's words differ"][0] == C.FAIL


def test_server_pages_and_marks(tmp_path, monkeypatch):
    import threading
    import urllib.request
    from http.server import ThreadingHTTPServer

    from scripts import review as R

    monkeypatch.setattr(R, "MARKS", tmp_path / "marks.jsonl")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), R.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    try:
        page = (
            urllib.request.urlopen(f"{base}/view?view=routes&seed=3&n=1&model=qwen3.5-9b&condition=C2").read().decode()
        )
        assert "C2-" in page and "Automatic checks" in page
        body = json.dumps({"view": "routes", "item": "x|y", "seed": 3, "verdict": "wrong", "note": "n"}).encode()
        req = urllib.request.Request(f"{base}/mark", body, {"Content-Type": "application/json"})
        assert urllib.request.urlopen(req).read() == b"ok"
        mark = json.loads((tmp_path / "marks.jsonl").read_text())
        assert mark["verdict"] == "wrong" and mark["seed"] == 3 and mark["commit"] and mark["utc"].endswith("Z")
    finally:
        httpd.shutdown()


def test_every_view_renders_its_cards():
    from bridge_jspace.review import page as P

    for v in I.shown():
        for m in MODELS:
            for which in ("set", "out", "superseded"):
                for it in I.items(v["id"], m, which)[:3]:
                    assert "What the model answered" in P.card(it, 0, False, None) or it["case"] is None, it["id"]


def test_export_writes_a_page_per_view(tmp_path):
    from scripts import review as R

    out = R.export(0, 2, tmp_path)
    pages = sorted(p.name for p in out.glob("*.html"))
    assert pages == sorted(["index.html", *(f"{v['id']}.html" for v in I.shown())])
    assert "C2-" in (out / "routes.html").read_text()  # the export's routes sample is C2 (views file)


@pytest.mark.parametrize(
    "view_id",
    ["main_swap", "single_change", "routes", "routes_early", "pointer_main", "routes_sweep", "both_removed",
     "both_removed_ctrl", "d1_identity", "k_curve", "logit_diff", "natural"],
)  # fmt: skip
def test_recount_equals_data_csv(view_id):
    from bridge_jspace.review import recount as RC

    rows = RC.recount(view_id)
    assert not [r for r in rows if r["status"] == "mismatch"]
    matched = {r["model"] for r in rows if r["status"] == "match"}
    if view_id in ("main_swap", "single_change", "routes", "routes_early", "pointer_main"):  # views 1-4: every model
        assert matched == set(MODELS)
    else:  # e.g. Muse's L34 sweep run has no data.csv number ("not tested")
        assert matched


# ---- batch 45: views added before their runs are scored (Dan 26 Oct ~22:40) -----------------------------------------
X45 = ("x45k_routes", "x45k_generic", "x45m_fresh", "x45b_sweep")
REAL = I.REPO  # the repo's own runs; planted tests point the loaders at tmp_path


def jl(path) -> list[dict]:
    return [json.loads(line) for line in open(path) if line.strip()]


def put(root, rel: str, name: str, rows) -> None:
    d = root / rel
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(json.dumps(rows) if name.endswith(".json") else "".join(json.dumps(r) + "\n" for r in rows))


@pytest.fixture
def planted(tmp_path, monkeypatch):
    """A repo root holding only the runs a test plants: the loaders read tmp_path; their caches cleared around it."""
    from scripts import review as R

    def clear():
        for f in (I.read_jsonl, I.competence_by_scene, I._items, R.stats, R.recount):
            f.cache_clear()

    clear()
    monkeypatch.setattr(I, "REPO", tmp_path)
    yield tmp_path
    clear()


def test_batch45_views_are_shown_with_no_sources_and_no_readme_claim():
    shown = {v["id"] for v in I.shown()}
    for vid in X45:
        v = I.view(vid)
        assert vid in shown and v["sources"] == [] and v["readme"].startswith("not yet in the README"), vid
        assert v["kind"] in I.spec()["kinds"] and "not scored yet" in v["title"], vid


X45_SCORED = ("x45a_prepend", "x45d_formats", "x45e_identity", "x45g_two_routes")


@pytest.mark.parametrize("view_id", X45 + X45_SCORED)
def test_batch45_views_on_the_repo_before_and_after_their_runs_land(view_id):
    # before a run lands: no items, and its page names the run as not landed; after: its items render. join: false
    # (45g's two scene sets per model): every landed run gives items
    from bridge_jspace.review import page as P
    from scripts import review as R

    v = I.view(view_id)
    page = R.render_view({"view": view_id, "seed": "0", "n": "10"}, False, "test")
    for m in MODELS:
        runs = v["runs"].get(m, [])
        got = I.items(view_id, m)
        landed = [r for r in runs if I.run_state(r) == "landed"]
        used = landed if v.get("join", True) is False else runs[:1] if runs and runs[0] in landed else []
        if not used:
            assert got == [], (view_id, m)
            for r, s in I.not_landed(v, m):
                assert f"{r}: {s}" in page, (view_id, r)
        else:
            assert {it["run"] for it in got} == set(used), (view_id, m)
            assert all(P.card(it, 0, False, None) for it in got[:3])


def test_x45k_routes_on_a_planted_run(planted):
    from bridge_jspace.review import page as P

    src = REAL / "results/x6_routes/x6_routes_27b"
    rows = jl(src / "outcomes.jsonl")
    done = sorted({(r["scene"], r["condition"]) for r in rows if r["arm"] == "whole"})
    keys = [k for k in done if k[1] == "C0"][:3] + [k for k in done if k[1] == "C2"][:3]
    # real rows under 45k's arm names (x6_routes --jpp-ks 25 50 100 --jpp-other), so every route is a real read
    copy_of = {"no_jpp50": "no_jpp", "no_jpp50_rand": "no_jpp_rand", "no_jpp100": "no_alf",
               "no_jpp100_rand": "no_alf_rand", "no_jppother100": "whole", "no_jppother100_rand": "none"}  # fmt: skip
    mine = [r for r in rows if (r["scene"], r["condition"]) in keys]
    mine += [{**r, "arm": new} for new, old in copy_of.items() for r in mine if r["arm"] == old]
    partner = {k: next(o for o in keys if o[1] == k[1] and o != k)[0] for k in keys}
    norms = [{**n, "share_jpp50": 0.2, "share_jpp100": 0.3, "share_jppother100": 0.25, "cos2_id_jpp25": None,
              **{f"cos2_U_jpp{k}": 0.1 * i for i, k in enumerate((25, 50, 100), 1)},
              "jpp_other_partner": partner[(n["scene"], n["condition"])]}
             for n in jl(src / "norms.jsonl") if (n["scene"], n["condition"]) in keys]  # fmt: skip
    run = "results/x6_routes/x6_routes_x45k_27b"
    put(planted, run, "cases.jsonl", [c for c in jl(src / "cases.jsonl") if (c["scene"], c["condition"]) in keys])
    put(planted, run, "outcomes.jsonl", mine)
    put(planted, run, "norms.jsonl", norms)
    put(planted, run, "manifest.json", {"layer": 32, "x45k": {"ks": [25, 50, 100], "other": True}})
    put(planted, "results/x6_routes/qwen35_9b_x6_routes_x45k", "manifest.json", {"layer": 12})  # running: no reads yet

    v = I.view("x45k_routes")
    got = I.items("x45k_routes", "qwen3.6-27b")
    assert sorted({(it["scene"], it["condition"]) for it in got}) == sorted(keys) and len(got) == 2 * len(keys)
    for it in got:
        assert all(it["rows"][w][label] is not None for w in I.READERS for label in v["filters"]["arms"]), it["id"]
        assert it["shares"]["jpp100"] == 0.3 and it["more"]["cos2_U_jpp100"] == pytest.approx(0.3)
        p = it["more"]["jpp_other_partner"]
        assert p.startswith(partner[(it["scene"], it["condition"])] + " (") and " → " in p
        assert C.run_checks(it)["label from the top token"][0] == C.PASS, it["id"]
    card = P.card(got[0], 0, False, None)
    assert "Geometry (norms.jsonl)" in card and "J++ part (k = 100)" in card and "without J++ (k = 100)" in card
    assert "cos² with the identity direction (k = 25) none" in card
    # not landed: a run dir without outcomes (running), and no run dir at all
    assert I.items("x45k_routes", "qwen3.5-9b") == [] and I.items("x45k_routes", "muse-glimmer-30b") == []
    assert I.not_landed(v, "qwen3.5-9b")[0][1].startswith("no outcomes.jsonl yet")
    assert I.not_landed(v, "muse-glimmer-30b") == [("results/x6_routes/muse30b_x6_routes_x45k", "not run yet")]
    assert I.not_landed(v, "qwen3.6-27b") == [] and I.run_flags(run) == []
    # x6_routes writes its outcomes before the C0 check: a failed check leaves items, and the view flags the run
    put(planted, run, "c0_check.json", {"c0_lookup_switch": 0.3, "reference": 0.6, "c0_min": None, "ok": False})
    assert I.run_flags(run) == ["C0 check failed (c0_check.json)"]
    assert f"{run} <span class='tag fail'>C0 check failed (c0_check.json)</span>" in P.claim_box(v)


def test_x45k_generic_joins_the_kmatch_run_by_scene(planted):
    from bridge_jspace.review import page as P

    main, kmatch, run = ("results/x0_necessity/x0_necessity_27b_chat", "results/x0_necessity/x0_kmatch_27b",
                         "results/x0_parts/x0_jppother100_27b")  # fmt: skip

    def at(r: dict) -> bool:
        return r["layer"] == 32 and r.get("rendering", "chat") == "chat"

    km = [r for r in jl(REAL / kmatch / "outcomes.jsonl") if at(r)]
    scenes = sorted({r["scene"] for r in km if r["arm"] == "whole"})[:3]
    cases = {
        c["scene"]: c for c in jl(REAL / main / "cases.jsonl") if c["rendering"] == "chat" and c["scene"] in scenes
    }

    def topped(r: dict) -> dict:  # x0_parts stores the top token since batch 45: the token its role names
        rd = cases[r["scene"]]["readers"][r["reader"]]
        other = next(t for t in (0, 1, 2) if t not in (rd["tok_A"], rd["tok_b"]))
        return {**r, "top": {"b": rd["tok_b"], "A": rd["tok_A"]}.get(r["role"], other)}

    mine = [r for r in km if r["scene"] in scenes]
    base = [r for r in mine if (r["dict"], r["k"], r["omp"]) in (("-", 0, "-"), ("jpp", 25, "signed"))]
    other = [{**r, "dict": "jpp_other", "k": 100, "omp": "other"} for r in base if r["dict"] == "jpp"]
    put(planted, main, "cases.jsonl", list(cases.values()))
    put(planted, run, "outcomes.jsonl", [topped(r) for r in base + other])
    put(planted, run, "shares.jsonl", [{"scene": s, "dict": d, "k": k, "omp": o, "share": 0.2} for s in scenes
                                       for d, k, o in (("jpp", 25, "signed"), ("jpp_other", 100, "other"))])  # fmt: skip
    put(planted, run, "manifest.json", {"single": "x0_necessity_27b_chat", "source_exp": "x0_necessity", "layer": 32,
                                        "other_k": 100, "parts": ["jpp_other", "jpp"],
                                        "jpp_other_partners": {s: scenes[(i + 1) % 3] for i, s in enumerate(scenes)}})  # fmt: skip
    put(planted, kmatch, "outcomes.jsonl", [r for r in mine if (r["dict"], r["k"]) in (("-", 0), ("jpp", 100))])
    put(planted, kmatch, "cases.jsonl", [c for c in jl(REAL / kmatch / "cases.jsonl")
                                         if c.get("rendering", "chat") == "chat" and c["scene"] in scenes])  # fmt: skip
    put(planted, kmatch, "shares.jsonl", [s for s in jl(REAL / kmatch / "shares.jsonl") if s["scene"] in scenes
                                          and s["layer"] == 32 and s["dict"] == "jpp" and s["omp"] == "signed"])  # fmt: skip

    v = I.view("x45k_generic")
    got = I.items("x45k_generic", "qwen3.6-27b")
    assert sorted({it["scene"] for it in got}) == scenes and len(got) == 2 * len(scenes)
    from_kmatch = [label for label in v["filters"]["arms"] if "kmatch" in label]
    for it in got:
        rows = it["rows"][it["reader"]]
        assert all(rows[label] is not None for label in v["filters"]["arms"]), it["id"]
        assert all(rows[label].get("_run") == "x0_kmatch_27b" for label in from_kmatch)
        assert not [label for label in v["filters"]["arms"] if label not in from_kmatch and "_run" in rows[label]]
        # this run's shares win (k = 25: 0.2, no random part stored); the kmatch run's k = 100 with its random part
        assert set(it["shares"]) == {"jpp", "jpp_other_k100", "jpp_k100", "random part_k100"}
        assert it["shares"]["jpp"] == 0.2
        checks = C.run_checks(it)
        assert (
            checks["second run has the same prompts"][0] == C.PASS and checks["label from the top token"][0] == C.PASS
        )
    card = P.card(got[0], 0, False, None)
    assert "(run x0_kmatch_27b)" in card and "another scene&#x27;s atoms, refit here (k = 100)" in card
    assert "From the run's manifest: jpp_other's partner scene " + scenes[1] + " (" in card
    it = copy.deepcopy(got[0])
    it["case"]["_joined"]["x0_kmatch_27b"]["pos"] += 1
    assert C.run_checks(it)["second run has the same prompts"][0] == C.FAIL
    it = copy.deepcopy(got[0])
    whole = it["rows"][it["reader"]]["whole"]
    whole["role"] = "A" if whole["role"] == "b" else "b"
    assert C.run_checks(it)["label from the top token"][0] == C.FAIL
    assert I.items("x45k_generic", "qwen3.5-9b") == [] and I.not_landed(v, "qwen3.5-9b") == []  # no 9B run in the view


@pytest.fixture(scope="module")
def fresh_cases():
    """Real 45m cases (x0_necessity.build_cases with the fresh alt, on the target's tokenizer), as the run writes them:
    one of each group."""
    from scripts import x0_necessity as X
    from scripts import x45m as M

    try:
        tok = M.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(X, "ALT", "fresh")
        mp.setattr(X, "RENDERINGS", ("chat",))
        cases, _ = X.build_cases(tok, M.SET)
    first = {}
    for c in cases:
        first.setdefault(M.group_of(c), {k: val for k, val in c.items() if k != "space"})
    return list(first.values())


def x0_row(case: dict, w: str, arm: str, part: tuple, role: str) -> dict:
    """An X0 outcome row as x0_necessity.read_row writes it (top stored), its numbers agreeing with its role."""
    rd, b = case["readers"][w], role == "b"
    return {"scene": case["scene"], "domain": case["domain"], "entity": case["bridge"], "rendering": "chat", "layer": 32,
            "reader": w, "upstream": case["upstream"], "dict": part[0], "k": part[1], "omp": part[2], "arm": arm,
            "switched": int(b), "top": rd["tok_b"] if b else rd["tok_A"], "role": role, "p_org": 0.05 if b else 0.9,
            "p_alt": 0.9 if b else 0.05, "ld": 3.0 if b else -3.0}  # fmt: skip


def test_x45m_shows_the_inserted_sentence_on_a_planted_run(planted, fresh_cases):
    from bridge_jspace.review import page as P
    from scripts import x45m as M

    run = "results/x0_necessity/x45m_fresh_27b"
    arms = (("none", ("-", 0, "-"), "A"), ("whole", ("-", 0, "-"), "b"), ("no_part", ("jpp", 25, "signed"), "A"),
            ("no_rand", ("jpp", 25, "signed"), "b"))  # fmt: skip
    put(planted, run, "cases.jsonl", fresh_cases)
    put(planted, run, "outcomes.jsonl", [x0_row(c, w, a, p, role) for c in fresh_cases for w in I.READERS
                                         for a, p, role in arms])  # fmt: skip
    got = I.items("x45m_fresh", "qwen3.6-27b")
    assert len(got) == 2 * len(fresh_cases)
    assert {it["group"] for it in got} == {"locker-before", "locker-after", "mixed"}
    for it in got:
        assert it["group"] == M.group_of(it["case"])
        assert all(r is not None for r in it["rows"][it["reader"]].values())
        checks = C.run_checks(it)
        assert all(checks[n][0] == C.PASS for n in C.CHECKS[:5]), (it["id"], checks)
        sentence = html.escape(it["case"]["fresh"]["sentence"])
        card = P.card(it, 0, False, None)
        assert card.count(f"<span class='ins'>{sentence}</span>") == 2  # outlined in both prompts
        assert "Inserted in both prompts" in card and f"<b>{it['group']}</b>" in card
    before = [it for it in got if I.facets(it, {"group": "locker-before"})]
    assert before and all(it["group"] == "locker-before" for it in before) and len(before) < len(got)
    # a run whose read gate failed writes no outcomes (x0_necessity reads only eligible scenes): named as such
    put(planted, "results/x0_necessity/muse30b_x45m_fresh", "gate.json",
        {"counts": {}, "gate": {"chat": {"org_accuracy": {"PP": 0.7, "PM": 0.9}, "pass": False, "enough": False}}})  # fmt: skip
    v = I.view("x45m_fresh")
    assert I.items("x45m_fresh", "qwen3.5-9b") == [] and I.not_landed(v, "qwen3.5-9b")[0][1] == "not run yet"
    assert I.items("x45m_fresh", "muse-glimmer-30b") == []
    assert I.not_landed(v, "muse-glimmer-30b")[0][1] == "no outcomes.jsonl: read gate failed: chat"


def test_x45b_sweep_marks_the_patched_tokens_per_arm_on_a_planted_run(planted):
    from bridge_jspace.review import page as P
    from scripts import review as R
    from scripts import statement_positions as SP
    from scripts import x45b_binding as B

    src = REAL / "results/x45b_binding/x45b_binding_27b"
    try:
        tok = SP.load_tokenizer()
    except Exception as e:
        pytest.skip(f"no tokenizer: {e}")
    items = jl(src / "cases.jsonl")[:3]
    for it in items:  # as stage_sweep adds them
        it["roles"] = {r: {"org": o, "alt": s} for r, (o, s) in B.role_positions(tok, it).items()}
    scenes = {it["scene"] for it in items}
    # the 45b run's real reads under the sweep's names: a / b_half = the bridge word at L / L/2, c / d = the locker
    # sentences at L / L/2 (reused for the item, value and final arms)
    as_sweep = {"none": [("none", None)], "S": [("S", None)], "a": [("bw32", 32)], "b_half": [("bw16", 16)],
                "c": [(f"{k}32", 32) for k in ("ls", "li", "lv", "lf")],
                "d": [(f"{k}16", 16) for k in ("ls", "li", "lv", "lf")]}  # fmt: skip
    keep = ("switched", "cand_switched", "cand_org_first", "role", "p_org", "p_alt", "ld", "top")
    rows = [{"scene": r["scene"], "entity": r["entity"], "reader": r["reader"], "arm": a, "layer": la,
             **{k: r[k] for k in keep}} for r in jl(src / "outcomes.jsonl") if r["scene"] in scenes
            for a, la in as_sweep.get(r["arm"], [])]  # fmt: skip
    run = "results/x45b_binding/x45b_sweep_v2_27b"
    put(planted, run, "cases.jsonl", items)
    put(planted, run, "outcomes.jsonl", rows)
    put(planted, run, "manifest.json", {"layer": 32, "sweep_layers": [16, 32], "main_run": "x0_necessity_27b_chat"})

    got = I.items("x45b_sweep", "qwen3.6-27b")
    assert len(got) == 2 * len(items) and {it["scene"] for it in got} == scenes
    for it in got:
        c, rows_ = it["case"], it["rows"][it["reader"]]
        assert it["more"] == {"layers": [16, 32], "kinds": ["bw", "ls", "li", "lv", "lf"]}
        assert len(rows_) == 12 and all(rows_.values()) and it["cls"] == rows_["S"]["role"]
        ids, where = c["readers"]["PP"]["ids"]["org"], I.sweep_positions(c)

        def text(ps: list[int], ids=ids) -> str:
            return "".join(C.piece("qwen3.6-27b", ids[p]) for p in ps)

        sents = [B.LOCKER_RE.match(s) for s in c["lockers"]["sentences"]]
        assert text(where["bw"]).strip() == c["bridge"]
        assert text(where["li"]).split() == " ".join(m.group(1) for m in sents if m).split()
        assert "".join(text(where["lv"]).split()) == "".join(m.group(2) for m in sents if m)  # digits: no leading space
        assert text(where["lf"]) == "." * len(sents) and set(where["li"] + where["lv"] + where["lf"]) <= set(
            where["ls"]
        )
        checks = C.run_checks(it)
        assert not [n for n, (s, _) in checks.items() if s == C.FAIL], (it["id"], checks)
        assert checks["label from the top token"][0] == C.PASS
    card = P.card(got[0], 0, False, None)
    assert "<th>L16</th>" in card and "<th>L32</th>" in card
    assert all(f"<span class='{cls}' title=" in card for cls in ("at", "ri", "rv", "rf", "rl"))
    assert card.count("<td title=") == len(I.READERS) * 2 * 5  # every reader's answer per kind and layer
    it = copy.deepcopy(got[0])
    r = it["rows"][it["reader"]]["ls32"]
    r["role"] = "A" if r["role"] != "A" else "b"
    assert C.run_checks(it)["label from the top token"][0] == C.FAIL
    v = I.view("x45b_sweep")
    assert I.items("x45b_sweep", "qwen3.5-9b") == [] and I.not_landed(v, "qwen3.5-9b")[0][1] == "not run yet"
    page = R.render_view({"view": "x45b_sweep", "seed": "0", "n": "10"}, False, "test")
    assert f"{2 * len(items)} of {2 * len(items)} items, uniform, seed 0" in page
    assert "results/x45b_binding/qwen35_9b_x45b_sweep_v2: not run yet" in page


def test_pack_lists_runs_not_landed(planted, tmp_path):
    from scripts import review as R

    out = R.pack(tmp_path / "pack.md").read_text()
    assert "Not landed yet: `results/x45b_binding/qwen35_9b_x45b_sweep_v2` (not run yet)" in out


# ---- batch 45, landed and scored: 45a, 45d, 45e, 45g (Dan 27 Oct ~00:30) --------------------------------------------
PREPEND = ("V0", "V1", "V2", "V3", "V4")


def latest_in(run: str, pattern: str) -> dict:
    with open(sorted(glob.glob(f"{I.REPO}/{run}/{pattern}"))[-1]) as f:
        return json.load(f)


def test_scored_batch45_views_are_shown_with_no_sources_and_no_readme_claim():
    shown = {v["id"] for v in I.shown()}
    for vid in X45_SCORED:
        v = I.view(vid)
        assert vid in shown and v["sources"] == [] and v["readme"].startswith("not yet in the README"), vid
        assert v["kind"] in I.spec()["kinds"] and v["claim"].startswith("Fixed in advance"), vid
    assert not [v["id"] for v in I.spec()["views"] if "45q" in v["id"]]  # 45q is not defined yet: a note, no view
    assert "45q: not defined yet" in I.VIEWS_FILE.read_text()


@pytest.mark.parametrize("view_id", X45_SCORED)
def test_scored_batch45_items_pass_the_automatic_checks(view_id):
    for m in MODELS:
        s = C.summary(I.items(view_id, m))
        assert not s["fail"], (m, {k: ex[:2] for k, ex in s["examples"].items()})


def test_x45a_item_sets_match_the_verdicts_n():
    v = I.view("x45a_prepend")
    for m, runs in v["runs"].items():
        moves = latest(runs[0])["x45a"]["moves"]
        got = [it for it in I.items("x45a_prepend", m) if it["reader"] == "PP"]
        assert len(got) == moves["all"]["n"], m
        assert sum(I.facets(it, {"move": "to or from the first locker"}) for it in got) == moves["first_locker"]["n"], m
        assert all(tuple(it["more"]["variants"]) == PREPEND for it in got), m


def test_x45d_item_sets_match_the_verdicts_n_and_are_held_out():
    v = I.view("x45d_formats")
    for m, runs in v["runs"].items():
        got = I.items("x45d_formats", m)
        for c in latest_in(runs[0], "x45d-*/verdict.json")["cells"]:
            if c["part"] == "pcf":
                n = sum(it["reader"] == c["reader"] and it["facet"]["format"] == c["format"] for it in got)
                assert n == c["n"], (m, c["format"], c["reader"])
        assert all(it["more"]["split"]["bridge"] == "test" for it in got), m  # the refit basis never saw the bridge
        assert all(it["order"]["original"] in ("before", "after") for it in got), m


def test_x45e_item_sets_match_the_verdicts_n():
    v = I.view("x45e_identity")
    for m, runs in v["runs"].items():
        got = I.items("x45e_identity", m)
        for r in latest(runs[0])["rows"]:
            if r["arm"] == "whole":
                assert sum(it["condition"] == r["condition"] and it["reader"] == "PP" for it in got) == r["n"], m


def test_x45g_item_sets_match_the_score_per_run_and_order_group():
    score = latest_in("results/x0_massmean", "score45g-*/score.json")
    v = I.view("x45g_two_routes")
    for m, runs in v["runs"].items():
        got = I.items("x45g_two_routes", m)
        for run in runs:
            mine = [it for it in got if it["run"] == run]
            cells = score["runs"].get(run.split("/")[-1], {}).get("cells")
            if cells is None:  # not landed (the 122B) or not scored
                assert not mine or I.run_state(run) == "landed", run
                continue
            for key, cell in cells.items():
                w, grp = key.split("|")
                n = sum(it["reader"] == w and grp in ("all", it["more"]["stored_order"]["org_order"]) for it in mine)
                assert n == cell["n"], (run, key)


def test_x45g_cases_are_the_cases_examples_blob_rebuilds():
    """x0_massmean.examples_blob rebuilds a 45g run's cases (X.build_cases on the manifest's set with its alt); the view
    reads the single run's cases.jsonl: the same prompts, checked on the target's tokenizer (both scene sets)."""
    from bridge_jspace import pins
    from scripts import x0_necessity as X
    from scripts import x45m as M

    try:
        tok = M.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    runs = [r for r in I.view("x45g_two_routes")["runs"].get(pins.TARGET, []) if I.run_state(r) == "landed"]
    if not runs:
        pytest.skip(f"no 45g run of {pins.TARGET} landed")
    got = I.items("x45g_two_routes", pins.TARGET)
    for run in runs:
        m = I.read_json(f"{run}/manifest.json")
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(X, "ALT", m["alt"])
            mp.setattr(X, "RENDERINGS", ("chat",))
            built = {c["scene"]: c for c in X.build_cases(tok, m["set"])[0]}
        mine = [it for it in got if it["run"] == run]
        assert mine, run
        for it in mine:
            c, b = it["case"], built[it["scene"]]
            assert all(c[k] == b[k] for k in ("context", "cf_context", "bridge", "cf_bridge", "pos")), it["id"]
            for w in I.READERS:
                same = [c["readers"][w][k] == b["readers"][w][k] for k in ("ids", "tok_A", "tok_b", "question")]
                assert all(same), it["id"]


def test_x45a_shows_every_variant_of_a_base_scene_on_a_planted_run(planted):
    from bridge_jspace.review import page as P

    run = "results/x6_routes/x6_routes_x45a_27b"
    src = REAL / run
    rows, cases = jl(src / "outcomes.jsonl"), jl(src / "cases.jsonl")
    done = sorted({r["base_scene"] for r in rows if r["arm"] == "whole"})
    bases = done[:3]
    out_base = next(c["base_scene"] for c in cases if c["base_scene"] not in set(done))
    put(planted, run, "cases.jsonl", [c for c in cases if c["base_scene"] in {*bases, out_base}])
    put(planted, run, "outcomes.jsonl", [r for r in rows if r["base_scene"] in bases])
    for name in ("norms.jsonl", "beta.jsonl"):
        put(planted, run, name, [r for r in jl(src / name) if r["base_scene"] in bases])
    put(planted, run, "manifest.json", json.loads((src / "manifest.json").read_text()))
    # the base scene outside the set: read right everywhere but in V2, where the recall misreads S
    put(planted, run, "competence.jsonl", [{"scene": f"{out_base}-{x}", "rendering": "chat", "reader": w, "variant": o,
                                            "right": True, "read_right": not (x == "V2" and w == "PM" and o == "alt")}
                                           for x in PREPEND for w in I.READERS for o in ("org", "alt")])  # fmt: skip
    put(planted, "results/x6_routes/muse30b_x6_routes_x45a", "manifest.json", {"layer": 26, "prepend": list(PREPEND)})

    v = I.view("x45a_prepend")
    arms = v["filters"]["arms"]
    got = I.items("x45a_prepend", "qwen3.6-27b")
    assert sorted({it["scene"] for it in got}) == bases and len(got) == 2 * len(bases)
    for it in got:
        vs = it["more"]["variants"]
        assert tuple(vs) == PREPEND and len(it["rows"][it["reader"]]) == len(PREPEND) * len(arms)
        assert all(r is not None for r in it["rows"][it["reader"]].values()), it["id"]
        assert vs["V0"]["prepended"] == "" and all(
            vs[x]["context"] == f"{vs[x]['prepended']} {vs['V0']['context']}" for x in PREPEND[1:]
        )
        assert it["facet"]["move"] == ("to or from the first locker" if 0 in vs["V0"]["move"] else "other moves")
        cls_row = it["rows"][it["reader"]]["V0 · only the pointer part"]  # the class: V0, only the pointer part
        assert it["cls"] == (
            cls_row["route"] if it["reader"] == "PP" else "follows S" if cls_row["switched"] else "stays"
        )
        checks = C.run_checks(it)
        assert not [n for n, (s, _) in checks.items() if s == C.FAIL], (it["id"], checks)
        assert checks["label from the top token"][0] == C.PASS
    it = got[0]
    card = P.card(it, 0, False, None)
    for x in PREPEND[1:]:  # outlined in O and in S
        assert card.count(f"<span class='ins'>{html.escape(it['more']['variants'][x]['prepended'])}</span>") == 2, x
    assert card.count("<td title=") == len(I.READERS) * len(PREPEND) * len(arms)  # each reader, variant and arm
    assert "code shift β vs V0" in card
    assert ("the 45a rule's items" if 0 in it["more"]["move"] else "outside the rule's moves") in card
    # a tampered row fails the label check, named by its variant
    bad = copy.deepcopy(it)
    r = bad["rows"]["PP"]["V3 · whole"]
    r["route"] = "value" if r["route"] != "value" else "identity"
    status, detail = C.run_checks(bad)["label from the top token"]
    assert status == C.FAIL and detail.startswith("V3: ")
    # outside the paired set: the variant that made it ineligible
    out = I.items("x45a_prepend", "qwen3.6-27b", "out")
    assert {o["scene"] for o in out} == {out_base} and out[0]["status"] == "V2: ineligible: competence (PM/alt)"
    assert all(P.card(o, 0, False, None) for o in out)
    # not landed: no run dir (9B), a run dir without outcomes (Muse, running)
    assert I.items("x45a_prepend", "qwen3.5-9b") == [] and I.not_landed(v, "qwen3.5-9b")[0][1] == "not run yet"
    assert I.items("x45a_prepend", "muse-glimmer-30b") == []
    assert I.not_landed(v, "muse-glimmer-30b")[0][1].startswith("no outcomes.jsonl yet")


def test_x45d_shows_the_format_and_the_held_out_half_on_a_planted_run(planted):
    from bridge_jspace.review import page as P
    from scripts import review as R

    run, fit = "results/x0b_generalize/x45d_27b", "results/x7_pcf/x45d_fit_27b"
    rows, cases = jl(REAL / run / "outcomes.jsonl"), jl(REAL / run / "cases.jsonl")
    done = {r["scene"] for r in rows}
    first: dict[str, str] = {}
    for c in cases:
        if c["scene"] in done:
            first.setdefault(c["format"], c["scene"])
    scenes = sorted(first.values())
    out_c = next(c for c in cases if c["scene"] not in done)
    cell = "/".join(str(out_c[k]) for k in I.CELL)
    put(planted, run, "cases.jsonl", [c for c in cases if c["scene"] in {*scenes, out_c["scene"]}])
    put(planted, run, "outcomes.jsonl", [r for r in rows if r["scene"] in scenes])
    put(planted, run, "shares.jsonl", [s for s in jl(REAL / run / "shares.jsonl") if s["scene"] in scenes])
    put(planted, run, "manifest.json", json.loads((REAL / run / "manifest.json").read_text()))
    put(planted, run, "gate.json", {"counts": {}, "gate": {cell: {"cases": 1, "org_accuracy": {"PP": 0.5, "PM": 0.9},
                                                                  "pass": False, "eligible": 0, "used": 0}}})  # fmt: skip
    put(planted, fit, "split.json", json.loads((REAL / fit / "split.json").read_text()))

    got = I.items("x45d_formats", "qwen3.6-27b")
    assert sorted({it["scene"] for it in got}) == scenes
    assert {it["facet"]["format"] for it in got} == {"prose", "json", "table"}
    for it in got:
        assert it["order"]["original"] == it["case"]["order"] and it["order"]["changed"] in ("before", "after")
        assert set(it["shares"]) == {"pcf", "pcf_rand", "alf", "alf_rand", "jpp", "jpp_rand"}
        assert it["more"]["split"]["bridge"] == "test" and it["more"]["split"]["n_fit"] > 0
        assert all(r is not None for r in it["rows"][it["reader"]].values()), it["id"]
        checks = C.run_checks(it)
        assert not [n for n, (s, _) in checks.items() if s == C.FAIL], (it["id"], checks)
        assert checks["label from the top token"][0] == C.PASS
    js = next(it for it in got if it["facet"]["format"] == "json")
    card = P.card(js, 0, False, None)
    assert "Format <b>JSON</b>" in card and "held out" in card and "locker statement" in card
    assert f"the refit basis {100 * js['shares']['pcf']:.0f}%" in card  # its share on the card
    bad = copy.deepcopy(js)
    bad["more"]["split"]["bridge"] = "fit"
    assert "bridge in the fit half" in P.card(bad, 0, False, None)
    # the format filter, from the URL to the sample
    assert sorted(it["scene"] for it in got if I.facets(it, {"format": "json"})) == [js["scene"]] * 2
    page = R.render_view({"view": "x45d_formats", "seed": "0", "n": "10", "format": "json"}, False, "test")
    assert js["scene"] in page and not [s for s in scenes if s != js["scene"] and f"scene {s} " in page]
    # outside the set: a cell whose read gate failed
    out = I.items("x45d_formats", "qwen3.6-27b", "out")
    assert [o["status"] for o in out] == [f"the cell's read gate failed ({cell})"] * 2


def test_x45e_shows_the_controls_share_beside_identity_outside_jpp_on_a_planted_run(planted):
    from bridge_jspace.review import page as P

    run = "results/x6_routes/x6_routes_x45e_27b_dom"
    src = REAL / run
    norms = {(n["scene"], n["condition"]): n for n in jl(src / "norms.jsonl")}

    def pick(cond: str, kind: str) -> str:
        return next(s for (s, c), n in sorted(norms.items()) if c == cond and I.wrong_reached(
            {"idout": n["share_idout"], "wrong": n["share_wrong"]}, n["k_wrong"]) == kind)  # fmt: skip

    c2 = {kind: pick("C2", kind) for kind in ("reached", "short", "empty")}
    c0 = [f"C0-{i:04d}" for i in range(1, 6)]  # the first five C0 scenes: 1-2 read, 3 taken and dropped, 4-5 beyond N
    read = {*c0[:2], *c2.values()}
    keys = {(s, s[:2]) for s in [*c0, *c2.values()]}
    put(planted, run, "cases.jsonl", [c for c in jl(src / "cases.jsonl") if (c["scene"], c["condition"]) in keys])
    put(planted, run, "outcomes.jsonl", [r for r in jl(src / "outcomes.jsonl") if r["scene"] in read])
    put(planted, run, "norms.jsonl", [n for k, n in norms.items() if k[0] in read])
    put(planted, run, "manifest.json", {**json.loads((src / "manifest.json").read_text()), "n_per_condition": 3,
                                        "identity_dropped": {"C0": 1, "C2": 0}})  # fmt: skip
    put(planted, run, "competence.jsonl", [{"scene": s, "rendering": "chat", "reader": w, "variant": o, "right": True,
                                            "read_right": True} for s in c0 for w in I.READERS for o in ("org", "alt")])  # fmt: skip

    v = I.view("x45e_identity")
    got = I.items("x45e_identity", "qwen3.6-27b")
    assert sorted({it["scene"] for it in got}) == sorted(read)
    for it in got:
        assert all(it["rows"][w][label] is not None for w in I.READERS for label in v["filters"]["arms"]), it["id"]
        assert "both" not in it["shares"] and {"idout", "wrong", "pca"} <= set(it["shares"])  # no --bothoff: no union
        assert set(it["more"]["controls"]) == {"k_wrong", "k_pca", "n_wrong_pool"}
        checks = C.run_checks(it)
        assert not [n for n, (s, _) in checks.items() if s == C.FAIL], (it["id"], checks)
    for kind, scene in c2.items():
        it = next(x for x in got if x["scene"] == scene and x["reader"] == "PP")
        assert it["facet"]["control"] == kind and I.facets(it, {"control": kind})
        card = P.card(it, 0, False, None)
        sh = it["shares"]
        target = f"identity outside J++ <b>{100 * sh['idout']:.1f}%</b> (the target)"
        assert f"Controls at identity outside J++'s share (norms.jsonl): {target}" in card
        wrong = f"the wrong-pair control <b>{100 * sh['wrong']:.1f}%</b> ({sh['wrong'] / sh['idout']:.2f} of the target"
        assert wrong in card and "Geometry (norms.jsonl)" not in card
        tail = card.split(wrong, 1)[1].split(" · ", 1)[0]  # the wrong-pair control's own tag
        assert ("0 directions: removes nothing" in tail) == (kind == "empty")
        assert ("short of the target" in tail) == (kind == "short")
    out = {o["scene"]: o["status"] for o in I.items("x45e_identity", "qwen3.6-27b", "out")}
    assert out[c0[2]].startswith("eligible and taken, dropped before the reads")
    assert out[c0[3]] == out[c0[4]] == "eligible, beyond the first N taken"


def test_x45g_shows_both_scene_sets_and_the_stored_order_on_a_planted_run(planted):
    from bridge_jspace.review import page as P
    from scripts import review as R

    v = I.view("x45g_two_routes")
    planted_runs = [*v["runs"]["qwen3.6-27b"], v["runs"]["muse-glimmer-30b"][0]]  # Muse: only its swap run landed
    for run in planted_runs:
        m = json.loads((REAL / run / "manifest.json").read_text())
        rows = jl(REAL / run / "outcomes.jsonl")
        scenes = sorted({r["scene"] for r in rows})[:3]
        put(planted, run, "manifest.json", m)
        put(planted, run, "outcomes.jsonl", [r for r in rows if r["scene"] in scenes])
        single = f"results/x0_necessity/{m['single']}"
        put(planted, single, "cases.jsonl", [c for c in jl(REAL / single / "cases.jsonl")
                                             if c["scene"] in scenes and c.get("rendering", "chat") == "chat"])  # fmt: skip

    got = I.items("x45g_two_routes", "qwen3.6-27b")
    assert {it["run"] for it in got} == set(v["runs"]["qwen3.6-27b"]) and len(got) == 2 * 3 * 2
    assert {it["facet"]["scenes"] for it in got} == {"two people swap", "only the asked pick"}
    for it in got:
        assert all(r is not None for r in it["rows"][it["reader"]].values()), it["id"]
        assert set(it["shares"]) == {"jpp", "Alf", "jppAlf"}
        assert it["order"]["original"] == it["more"]["stored_order"]["org_order"]
        checks = C.run_checks(it)
        assert checks["second run has the same prompts"][0] == C.PASS and checks["label from the top token"][0] == C.NA
        assert not [n for n, (s, _) in checks.items() if s == C.FAIL], (it["id"], checks)
    one = [it for it in got if I.facets(it, {"scenes": "only the asked pick"})]
    assert len(one) == 6 and all(it["run"].endswith("x45g_one_27b_r2") for it in one)
    card = P.card(got[0], 0, False, None)
    assert f"Scene set: <b>{got[0]['more']['scene_set']}</b>" in card and "org_order <b>" in card
    assert "J++ and the pointer (their union)" in card and "without both" in card
    for key, val in (("org_order", "after"), ("alt_order", "after")):  # the stored order against the case's
        bad = copy.deepcopy(got[0])
        bad["more"]["stored_order"][key] = "before" if bad["more"]["stored_order"][key] == val else val
        status, detail = C.run_checks(bad)["second run has the same prompts"]
        assert status == C.FAIL and key in detail
    bad = copy.deepcopy(got[0])
    bad["more"]["entity"] = "nobody"
    assert C.run_checks(bad)["second run has the same prompts"][0] == C.FAIL
    # the 122B's runs not landed, Muse's one-pick run not landed: its swap run's items only
    swap_122b, one_122b = v["runs"]["qwen3.5-122b-a10b"]
    assert I.items("x45g_two_routes", "qwen3.5-122b-a10b") == []
    assert I.not_landed(v, "qwen3.5-122b-a10b") == [(swap_122b, "not run yet"), (one_122b, "not run yet")]
    muse = I.items("x45g_two_routes", "muse-glimmer-30b")
    assert muse and {it["run"] for it in muse} == {v["runs"]["muse-glimmer-30b"][0]}
    assert I.not_landed(v, "muse-glimmer-30b") == [(v["runs"]["muse-glimmer-30b"][1], "not run yet")]
    page = R.render_view({"view": "x45g_two_routes", "seed": "0", "n": "10"}, False, "test")
    assert f"{swap_122b}: not run yet; {one_122b}: not run yet" in page
