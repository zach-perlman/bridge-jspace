"""The review dashboard (src/bridge_jspace/review/, scripts/review.py) on the repo's runs: deterministic samples, the
item sets against the verdicts' n, the class re-derivation on hand-picked items, and checks that fail on bad data."""

import copy
import glob
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


def test_export_writes_a_page_per_view(tmp_path):
    from scripts import review as R

    out = R.export(0, 2, tmp_path)
    pages = sorted(p.name for p in out.glob("*.html"))
    assert pages == sorted(["index.html", *(f"{v['id']}.html" for v in I.shown())])
    assert "C2-" in (out / "routes.html").read_text()  # the export's routes sample is C2 (views file)


@pytest.mark.parametrize(
    "view_id",
    ["main_swap", "single_change", "routes", "routes_early", "pointer_main", "routes_sweep", "both_removed",
     "both_removed_ctrl", "d1_identity", "k_curve", "logit_diff"],
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
