"""x53_7 (53.7): the renderings keep the bridge aligned in O / S on the 9B and 27B tokenizers; each verdict applies its
test's rule verbatim on planted data; a failed gate gives "not tested"."""

import inspect
import json

import numpy as np
import pytest

from scripts import x0_necessity as X
from scripts import x0_probe as P
from scripts import x6_routes as R
from scripts import x53_7 as F
from scripts import x53_monitor as M

TARGETS = ("qwen3.5-9b", "qwen3.6-27b")
CTX = "Clara picked helium. The locker of the frog is 5. Eva picked the frog. The locker of helium is five."


def test_code_keeps_the_statements_in_order():
    code = F.code_text(CTX)
    assert code.splitlines() == ["```python", "picks = {}", "lockers = {}", 'picks["Clara"] = "helium"',
                                 'lockers["frog"] = 5', 'picks["Eva"] = "frog"', 'lockers["helium"] = "five"', "```"]  # fmt: skip
    with pytest.raises(F.Unrenderable):
        F.statements("Clara picked helium. It rained.")


def tokenizer(target: str):
    from scripts import x52_atoms

    try:
        return x52_atoms.tokenizer_of(target)
    except Exception:
        pytest.skip(f"{target}: tokenizer not cached")


def decoded(tok, ids: list[int], pos: int) -> str:
    return tok.decode([ids[pos]]).strip(' "')


@pytest.mark.parametrize("target", TARGETS)
@pytest.mark.parametrize("fmt", F.FORMATS)
def test_routes_scenes_keep_the_bridge_aligned(target, fmt):
    tok = tokenizer(target)
    cases, _ = R.scenes(tok, 4, fmt=fmt)
    assert {c["condition"] for c in cases} == set(R.CONDITIONS)
    for c in cases:
        assert c["format"] == fmt
        for w, rd in c["readers"].items():
            org, alt = rd["ids"]["org"], rd["ids"]["alt"]
            assert len(org) == len(alt)
            assert decoded(tok, org, c["pos"]) == c["bridge"] and decoded(tok, alt, c["pos"]) == c["cf_bridge"], w
            text = tok.decode(org)
            assert ("<tool_response>" in text and c["context"] in text) if fmt == "tool" else 'picks["' in text
        assert c["readers"]["PP"]["ids"]["org"][: c["pos"] + 1] == c["readers"]["PM"]["ids"]["org"][: c["pos"] + 1]


@pytest.mark.parametrize("target", TARGETS)
def test_routes_prose_cases_are_unchanged(target):
    tok = tokenizer(target)
    cases, _ = R.scenes(tok, 2)
    assert all("format" not in c for c in cases)
    c = cases[0]
    assert decoded(tok, c["readers"]["PP"]["ids"]["org"], c["pos"]) == c["bridge"]


@pytest.mark.parametrize("target", TARGETS)
@pytest.mark.parametrize("fmt", F.FORMATS)
def test_topic_scenes_keep_the_bridge_aligned(target, fmt):
    tok = tokenizer(target)
    pairs = F.pairs_of(F.PROBE_SET)
    kept = 0
    for scene in sorted(pairs)[:40]:
        c, why = F.scene_case(tok, pairs[scene], fmt)
        if c is None:
            assert why and fmt == "code", why  # the tool output keeps every scene's tokens: nothing drops
            continue
        kept += 1
        for rd in c["readers"].values():
            assert decoded(tok, rd["ids"]["org"], c["pos"]) == c["bridge"]
            assert decoded(tok, rd["ids"]["alt"], c["pos"]) == c["cf_bridge"]
        item = P.item_of(c, False)  # the probe's targets read the prose context, whose statements the format keeps
        assert F.statements(c["context"])[item["locker_index"]][:2] == ("locker", c["bridge"])
    assert kept >= 10


def test_monitor_defaults_unchanged():
    assert M.SETS == ("main", "json")
    assert inspect.signature(M.stage_run).parameters["sets_run"].default == M.SETS
    assert set(F.FORMATS) <= set(M.BUILD) and set(F.FORMATS) <= set(M.SET_TEXT)


# ---- verdicts on planted data -----------------------------------------------------------------------------------------


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def routes_run(root, name, gate_pass=None, c0_ok=True, c0_rate=0.9):
    gate_pass = gate_pass or {}
    src = root / name
    src.mkdir(parents=True)
    m = {"model": {"target": "qwen3.6-27b"}, "layer": 32, "conditions": list(R.CONDITIONS), "gate": 0.8,
         "gate_fixed_in_advance": 0.8, "format": "code", "items": {}}  # fmt: skip
    (src / "manifest.json").write_text(json.dumps(m))
    acc = {c: ({"PP": 0.95, "PM": 0.9} if gate_pass.get(c, True) else {"PP": 0.95, "PM": 0.7}) for c in R.CONDITIONS}
    (src / "gate.json").write_text(json.dumps({"gate": {c: {"org_read_accuracy": a, "pass": min(a.values()) >= 0.8}
                                                        for c, a in acc.items()}}))  # fmt: skip
    (src / "c0_check.json").write_text(json.dumps({"c0_lookup_switch": c0_rate, "reference": 0.92, "c0_min": None,
                                                   "ok": c0_ok}))  # fmt: skip
    rows, norms = [], []
    for cond in R.CONDITIONS:
        for i in range(40):
            norms.append({"scene": f"{cond}-{i}", "condition": cond, "norm": 1.0})
            for arm in F.ROUTE_ARMS:
                if arm == "whole":
                    rt = "identity" if i % 2 else "position"
                elif arm == "no_alf":
                    rt = "identity" if i % 2 else ("position" if i % 10 == 0 else "original")
                elif arm == "keep_alf":
                    rt = "position" if i % 4 == 0 else "original"
                else:
                    rt = "original"
                rows.append({"scene": f"{cond}-{i}", "condition": cond, "entity": f"e{i % 10}", "reader": "PP",
                             "arm": arm, "route": rt, "switched": int(rt != "original")})  # fmt: skip
                rows.append({"scene": f"{cond}-{i}", "condition": cond, "entity": f"e{i % 10}", "reader": "PM",
                             "arm": arm, "route": None, "switched": int(i % 3 == 0)})  # fmt: skip
    write_jsonl(src / "outcomes.jsonl", rows)
    write_jsonl(src / "norms.jsonl", norms)
    return src


def test_routes_verdict_applies_the_rule_verbatim(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "RESULTS", tmp_path)
    routes_run(tmp_path, "run_a")
    out = F.stage_routes_verdict(["run_a"], n_boot=200)
    blob = json.loads((out / "verdict.json").read_text())
    run = blob["runs"][0]
    assert run["status"] == dict.fromkeys(R.CONDITIONS, "tested")
    assert run["cells"]["C2|whole"]["used"] == ["identity", "position"]  # 0.5 each, far above 0.20 / 0.10
    assert run["cells"]["C2|keep_alf"]["used"] == ["position", "original"]  # 0.25 and 0.75
    # the same cells as x6_routes' own verdict (shares and used routes)
    own = json.loads((R.stage_verdict("run_a", 200) / "verdict.json").read_text())["rows"]
    for r in own:
        if r["arm"] in F.ROUTE_ARMS:
            mine = run["cells"][f"{r['condition']}|{r['arm']}"]
            assert mine["used"] == r["used"] and mine["share"] == r["share"]
    assert (out / "x53_7_routes.png").exists() and "Rule (the routes test's, verbatim)" in (
        out / "verdict.md"
    ).read_text()


def test_routes_failed_gate_and_c0_stop_are_not_tested(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "RESULTS", tmp_path)
    routes_run(tmp_path, "run_g", gate_pass={"C1": False})
    st = F.routes_status(tmp_path / "run_g")
    assert st == {"C0": "tested", "C1": "not tested (gate 0.700 < 0.80)", "C2": "tested"}
    routes_run(tmp_path, "run_c", c0_ok=False, c0_rate=0.5)
    st = F.routes_status(tmp_path / "run_c")
    assert all(s.startswith("not tested (the C0 check stopped the run") for s in st.values())
    out = F.stage_routes_verdict(["run_c"], n_boot=50)
    assert json.loads((out / "verdict.json").read_text())["runs"][0]["cells"] == {}


def probe_run(root, name, passed, n=80, seed=0):
    rng = np.random.default_rng(seed)
    src = root / name
    src.mkdir(parents=True)
    m = {"model": {"target": "qwen3.6-27b", "revision": "x"}, "layer": 32, "set": F.PROBE_SET, "source": None,
         "format": "tool"}  # fmt: skip
    (src / "manifest.json").write_text(json.dumps(m))
    acc = {"PP": 0.92, "PM": 0.91} if passed else {"PP": 0.92, "PM": 0.64}
    (src / "gate.json").write_text(json.dumps({"cases": n, "org_read_accuracy": acc, "pass": passed,
                                               "status": "passed" if passed else F.not_tested(acc)}))  # fmt: skip
    if not passed:
        return src
    items, h = [], []
    for i in range(n):
        lock, order = i % 3, "before" if i % 2 else "after"
        sents = ["Ann picked a.", "Bo picked b.", "Cy picked c.", "The locker of a is 1.", "The locker of b is 2.",
                 "The locker of c is 3."]  # fmt: skip
        items.append({"scene": f"s{i}", "entity": f"e{i % 12}", "answer": str(i % 4), "locker_index": lock,
                      "pick_index": i % 3, "order": order, "context": " ".join(sents)})  # fmt: skip
        v = rng.normal(size=16)
        v[lock] += 6.0 if order == "before" else 0.0  # the slot is written only when the locker comes first
        h.append(v)
    np.savez_compressed(
        src / "states.npz", h=np.array(h, dtype=np.float16), scene=np.array([it["scene"] for it in items])
    )
    write_jsonl(src / "items.jsonl", items)
    return src


def test_probe_verdict_scores_and_gates(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "RESULTS", tmp_path)
    probe_run(tmp_path, "p_pass", True)
    probe_run(tmp_path, "p_fail", False)
    out = F.stage_probe_verdict(["p_pass", "p_fail"], n_boot=100)
    runs = {r["run"]: r for r in json.loads((out / "verdict.json").read_text())["runs"]}
    assert runs["p_fail"]["status"] == "not tested (gate 0.640 < 0.80)" and "rows" not in runs["p_fail"]
    rows = {(r["stratum"], r["target"]): r for r in runs["p_pass"]["rows"]}
    assert rows[("before", "locker sentence")]["probe"][0] > 0.9  # the planted slot
    assert rows[("after", "locker sentence")]["probe"][0] < 0.7  # the control stratum carries none
    assert (out / "p_pass" / "probe.png").exists() and F.PROBE_READING in (out / "verdict.md").read_text()


def monitor_cache(cache, name, fmt, acc, n=20, layers=(0, 2, 4)):
    keys, right = [], []
    for p in M.PROBE_POS:
        for t in M.TARGETS:
            for f in (*M.FEATURES, "chance"):
                v = acc.get((p, t, f), acc.get(f, 0.5))
                keys.append(f"{p}|{t}|{f}")
                right.append(np.stack([np.stack([(np.arange(n) < round(v * n)).astype(np.float32), np.ones(n, np.float32)])
                                       for _ in layers]))  # fmt: skip
    (cache / name).mkdir(parents=True)
    np.savez(cache / name / f"{fmt}.npz", layers=np.array(layers), keys=np.array(keys), right=np.stack(right),
             entity=np.array([f"e{i % 7}" for i in range(n)]), scene=np.array([f"s{i // 2}" for i in range(n)]),
             seconds=np.zeros(len(layers)))  # fmt: skip


def test_monitor_verdict_applies_53_2s_rule(tmp_path, monkeypatch):
    monkeypatch.setattr(M, "RESULTS", tmp_path / "results")
    monkeypatch.setattr(M, "CACHE", tmp_path / "cache")
    run = tmp_path / "results" / "mon_27b"
    run.mkdir(parents=True)
    gates = {"code": {"cases": 272, "org_read_accuracy": {"PP": 0.9, "PM": 0.85}, "pass": True, "status": "passed",
                      "set": "d1_topics_v3"},
             "tool": {"cases": 600, "org_read_accuracy": {"PP": 0.79, "PM": 0.95}, "pass": False,
                      "status": F.not_tested({"PP": 0.79, "PM": 0.95}), "set": "d1_topics_v3"}}  # fmt: skip
    (run / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.6-27b"},
                                                   "x53_7": {"formats": ["code", "tool"], "gates": gates}}))  # fmt: skip
    acc = {"full": 0.9, ("B", "a", "jpp25"): 0.85, ("B", "a", "rand25"): 0.3, "jpp25": 0.5, "rand25": 0.5,
           "jpp100": 0.5, "rand100": 0.5}  # fmt: skip
    monitor_cache(tmp_path / "cache", "mon_27b", "code", acc)
    out = F.stage_monitor_verdict(["mon_27b"], n_boot=50)
    blob = json.loads((out / "x53_7_monitor.json").read_text())
    status = {r["format"]: r["status"] for r in blob["runs"]}
    assert status == {"code": "tested", "tool": "not tested (gate 0.790 < 0.80)"}
    rules = blob["results"]["qwen3.6-27b"]["code"]["rules"]
    assert rules["B|a"]["k25"]["label"] == "J-space carries X"  # 0.85 >= 0.8 and 0.55 above random
    assert rules["B|b"]["k25"]["label"] == "J-space blind to X"  # J++ = random everywhere, full 0.9
    full, jpp, rand = np.full(3, 0.9), np.full(3, 0.5), np.full(3, 0.5)
    assert rules["B|b"]["k25"]["label"] == M.rule_label(full, jpp, rand)["label"]
    assert "tool" not in blob["results"]["qwen3.6-27b"] and (out / "x53_7_monitor_code.png").exists()


def test_gate_of_is_x0s_gate():
    rows = [{"scene": f"s{i}", "reader": w, "read_right": i < (8 if w == X.LOOKUP else 7)} for i in range(10)
            for w in X.READERS]  # fmt: skip
    g = F.gate_of(rows)
    assert g["org_read_accuracy"] == {"PP": 0.8, "PM": 0.7} and not g["pass"]
    assert g["status"] == "not tested (gate 0.700 < 0.80)"
    assert F.gate_of([{**r, "read_right": True} for r in rows])["pass"]
