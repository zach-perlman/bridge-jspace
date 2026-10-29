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
         "gate_fixed_in_advance": 0.8, "format": "code", "items": {}, "alf_from": "x0_probe_v4_27b"}  # fmt: skip
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


def test_monitor_verdict_shows_the_arms_beside(tmp_path, monkeypatch):
    monkeypatch.setattr(M, "RESULTS", tmp_path / "results")
    monkeypatch.setattr(M, "CACHE", tmp_path / "cache")
    run = tmp_path / "results" / "mon_9b"
    run.mkdir(parents=True)
    gates = {"code": {"cases": 272, "org_read_accuracy": {"PP": 0.9, "PM": 0.85}, "pass": True, "status": "passed",
                      "set": "d1_topics_v3"}}  # fmt: skip
    (run / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.5-9b"},
                                                   "x53_7": {"formats": ["code"], "gates": gates}}))  # fmt: skip
    monitor_cache(
        tmp_path / "cache", "mon_9b", "code", {"full": 0.9, ("B", "a", "jpp25"): 0.85, ("B", "a", "rand25"): 0.3}
    )
    keys, right, n, layers = [], [], 20, (0, 2, 4)
    for p in M.PROBE_POS:
        for t in M.TARGETS:
            for k in M.KS:
                keys.append(f"{p}|{t}|fix{k}")
                v = 0.4 if (p, t) == ("B", "a") else 0.5  # the fixed subspace reads less than the per-state part
                right.append(np.stack([np.stack([(np.arange(n) < round(v * n)).astype(np.float32), np.ones(n, np.float32)])
                                       for _ in layers]))  # fmt: skip
    np.savez(M.cache_file("mon_9b", "code", "fixed"), layers=np.array(layers), keys=np.array(keys),
             right=np.stack(right), entity=np.array([f"e{i % 7}" for i in range(n)]),
             scene=np.array([f"s{i // 2}" for i in range(n)]), seconds=np.zeros(len(layers)))  # fmt: skip
    out = F.stage_monitor_verdict(["mon_9b"], n_boot=50)
    rules = json.loads((out / "x53_7_monitor.json").read_text())["results"]["qwen3.5-9b"]["code"]["rules"]
    assert rules["B|a"]["k25"]["label"] == "J-space carries X"  # the decisive arm
    assert rules["B|a"]["fixed_k25"]["label"] != rules["B|a"]["k25"]["label"]  # beside, from the fixed pass
    md = (out / "verdict.md").read_text()
    assert "beside: fixed k25 / k100" in md and f"| {rules['B|a']['fixed_k25']['label']} / " in md


def test_monitor_atom_ids_are_the_monitors(tmp_path):
    run = tmp_path / "x53_7_monitor_x"
    run.mkdir()
    rng = np.random.default_rng(0)
    items = [{"scene": f"s{i}", "labels": {v: {"bridge": f"e{(i + j) % 6}", "slot": (i + j) % 3, "lookup": str(i % 4),
                                              "recall": str(i % 5)} for j, v in enumerate(M.VARIANTS)}}
             for i in range(30)]  # fmt: skip
    write_jsonl(run / "cases_code.jsonl", items)
    atoms = rng.integers(0, 400, size=(2, 30, 2, 3, M.K_MAX)).astype(np.int32)
    np.save(run / "states_code_atoms.npy", atoms)
    m = {"x53_7": {}, "layers": [0, 2], "sets_done": {"code": {}}, "finished_utc": "x"}
    (run / "manifest.json").write_text(json.dumps(m))
    got = F.monitor_atom_ids(run)
    rows = M.row_table(items)
    assert got == {"code": {str(la): M.needed_atom_ids(atoms[li], rows) for li, la in enumerate((0, 2))}}
    (run / "manifest.json").write_text(json.dumps({**m, "sets_done": {}}))
    assert F.monitor_atom_ids(run) == {}  # every format failed its gate: no atoms
    (run / "manifest.json").write_text(json.dumps({**m, "finished_utc": None}))
    with pytest.raises(AssertionError, match="has not finished"):
        F.monitor_atom_ids(run)


def test_gate_of_is_x0s_gate():
    rows = [{"scene": f"s{i}", "reader": w, "read_right": i < (8 if w == X.LOOKUP else 7)} for i in range(10)
            for w in X.READERS]  # fmt: skip
    g = F.gate_of(rows)
    assert g["org_read_accuracy"] == {"PP": 0.8, "PM": 0.7} and not g["pass"]
    assert g["status"] == "not tested (gate 0.700 < 0.80)"
    assert F.gate_of([{**r, "read_right": True} for r in rows])["pass"]
    one = F.gate_of([r for r in rows if r["reader"] == X.LOOKUP], (X.LOOKUP,))  # CH2: the lookup only
    assert one["org_read_accuracy"] == {"PP": 0.8} and one["pass"]


# ---- code_pointer_v1's CH2 (descriptive add-on) ----------------------------------------------------------------------


@pytest.mark.parametrize("target", TARGETS)
def test_cp_cases_keep_the_head_key_aligned(target):
    tok = tokenizer(target)
    items = F.cp_items()
    for it in [*items[:15], *items[-15:]]:  # both domains
        c, why = F.cp_case(tok, it)
        assert c is not None, why
        rd = c["readers"][X.LOOKUP]
        assert decoded(tok, rd["ids"]["org"], c["pos"]) == c["bridge"] == it["query"]
        assert decoded(tok, rd["ids"]["alt"], c["cf_pos"]) == c["cf_bridge"]
        assert tok.decode(rd["ids"]["org"][c["pos"] - 4 : c["pos"]]).endswith(' = "')  # the head line, not the dict
        p = F.cp_probe_item(c)
        assert it["entities"][p["locker_index"]] == c["bridge"] and p["order"] == "before"
        assert str(it["digits"][p["locker_index"]]) == p["answer"] == it["answer"]


def test_cp_monitor_items_pass_the_monitors_checks(monkeypatch):
    tok = tokenizer("qwen3.6-27b")
    monkeypatch.setattr(F, "CP_MONITOR_PER_DOMAIN", 3)
    items, counts = F.cp_monitor_items(tok, "qwen3.6-27b")
    assert len(items) == 6 and counts["cases"] == 800
    M.check_items(items)
    for it in items:
        assert it["readers"]["PM"] == it["readers"]["PP"]  # one reader: the recall slot repeats the lookup
        assert it["labels"]["org"]["recall"] != "" and it["labels"]["alt"]["bridge"] == it["cf_entity"]


def test_cp_probe_report_is_numbers_only(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "RESULTS", tmp_path)
    src = probe_run(tmp_path, "cp_pass", True)
    items = [json.loads(x) for x in (src / "items.jsonl").read_text().splitlines()]
    write_jsonl(src / "items.jsonl", [{**it, "order": "before", "layout": "5/5"} for it in items])
    probe_run(tmp_path, "cp_fail", False)
    out = F.stage_probe_verdict(["cp_pass", "cp_fail"], n_boot=50, prefix="x53_7_cp_probe")
    assert out.name.startswith("x53_7_cp_probe-")
    runs = {r["run"]: r for r in json.loads((out / "verdict.json").read_text())["runs"]}
    assert {r["stratum"] for r in runs["cp_pass"]["rows"]} == {"before"}  # the only order CH2 has
    assert runs["cp_fail"]["status"].startswith("not tested (gate")
    md = (out / "verdict.md").read_text()
    assert F.CP_RULE in md and F.PROBE_READING not in md and (out / "cp_pass" / "probe.png").exists()


def test_cp_monitor_report_has_no_label(tmp_path, monkeypatch):
    monkeypatch.setattr(M, "RESULTS", tmp_path / "results")
    monkeypatch.setattr(M, "CACHE", tmp_path / "cache")
    for name, ok in (("cp_27b", True), ("cp_9b", False)):
        (tmp_path / "results" / name).mkdir(parents=True)
        g = {"cases": 800, "org_read_accuracy": {"PP": 0.95 if ok else 0.6}, "pass": ok,
             "status": "passed" if ok else F.not_tested({"PP": 0.6}), "per_domain": {}}  # fmt: skip
        (tmp_path / "results" / name / "manifest.json").write_text(json.dumps(
            {"model": {"target": "qwen3.6-27b" if ok else "qwen3.5-9b"}, "x53_7": {"gates": {F.CP_FORMAT: g}}}))  # fmt: skip
    monitor_cache(tmp_path / "cache", "cp_27b", F.CP_FORMAT, {"full": 0.9, "jpp25": 0.85, "rand25": 0.3})
    out = F.stage_cp_monitor_report(["cp_27b", "cp_9b"], n_boot=50)
    blob = json.loads((out / "x53_7_cp_monitor.json").read_text())
    assert "rules" not in blob["results"]["qwen3.6-27b"][F.CP_FORMAT]
    assert [r["status"] for r in blob["runs"]] == ["tested", "not tested (gate 0.600 < 0.80)"]
    md = (out / "verdict.md").read_text()
    assert not any(lab in md for lab in ("J-space blind", "J-space carries", "in between"))
    assert (out / "x53_7_cp_monitor.png").exists()


# ---- the adapted design (Dan 12:10, decisions_1210): the lookup-only gate ------------------------------------------


def comp_rows(n: int, lookup_ok: int, recall_ok: int) -> list[dict]:
    """X0 competence rows: the lookup right (said and read) on O and S in the first lookup_ok scenes, the recall in the
    first recall_ok; the others wrong on S's read only."""
    rows = []
    for i in range(n):
        for w, k in (("PP", lookup_ok), ("PM", recall_ok)):
            for v in ("org", "alt"):
                rows.append({"scene": f"s{i}", "reader": w, "variant": v, "right": True,
                             "read_right": i < k or v == "org"})  # fmt: skip
    return rows


def test_lookup_gate_ignores_the_recall():
    assert (
        F.LOOKUP_GATE_DESIGN
        == R.LOOKUP_GATE_DESIGN
        == "adapted design: lookup-only gate; the recall is not part of this test"
    )
    cases = [{"scene": f"s{i}"} for i in range(10)]
    g, eligible = F.lookup_gate(comp_rows(10, 8, 2), cases)
    assert g["lookup_right_share"] == 0.8 and g["pass"] and g["eligible"] == 8 and len(eligible) == 8
    assert g["descriptive"]["rates"]["PM"]["says_and_reads_O_and_S"] == 0.2  # the recall fails, descriptive only
    g, _ = F.lookup_gate(comp_rows(10, 7, 10), cases)
    assert not g["pass"] and g["status"] == "not tested (gate 0.700 < 0.80)"
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp_rows(10, 9, 3)}
    two = {"org_read_accuracy": {"PP": 1.0, "PM": 1.0}, "pass": True, "eligible": 3}
    cell, ok = R.lookup_gate_cell(cases, right, 0.8, two)
    assert cell["lookup_right_share"] == 0.9 and cell["pass"] and cell["eligible"] == len(ok) == 9
    assert cell["descriptive"]["recall_right_share"] == 0.3 and cell["descriptive"]["two_reader_eligible"] == 3


def test_routes_verdict_under_the_lookup_gate(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "RESULTS", tmp_path)
    src = routes_run(tmp_path, "run_l")
    m = json.loads((src / "manifest.json").read_text())
    (src / "manifest.json").write_text(json.dumps({**m, "lookup_gate": True, "gate_design": R.LOOKUP_GATE_DESIGN}))
    two = {"org_read_accuracy": {"PP": 0.95, "PM": 0.5}, "pass": False, "eligible": 10}
    cells = {c: {"cases": 40, "lookup_right_share": 0.9 if c != "C1" else 0.75, "pass": c != "C1", "eligible": 36,
                 "design": R.LOOKUP_GATE_DESIGN, "descriptive": {**two, "recall_right_share": 0.4,
                                                                 "two_reader_pass": False, "two_reader_eligible": 10}}
             for c in R.CONDITIONS}  # fmt: skip
    (src / "gate.json").write_text(json.dumps({"gate": cells}))
    assert F.routes_status(src) == {"C0": "tested", "C1": "not tested (gate 0.750 < 0.80)", "C2": "tested"}
    out = F.stage_routes_verdict(["run_l"], n_boot=50)
    md = (out / "verdict.md").read_text()
    assert f"**{R.LOOKUP_GATE_DESIGN}.**" in md and "recall follows S (descriptive)" in md
    assert "recall the same: 0.400" in md
    assert "carried over from prose, not refit" in md and "Qwen3.6-27B code x0_probe_v4_27b" in md  # Dan 13:15: U


def test_probe_verdict_under_the_lookup_gate_marks_hollow(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "RESULTS", tmp_path)
    for name, hollow in (("p_tool", None), ("p_code", F.HOLLOW)):
        src = probe_run(tmp_path, name, True)
        m = json.loads((src / "manifest.json").read_text())
        (src / "manifest.json").write_text(json.dumps({**m, "gate_design": F.LOOKUP_GATE_DESIGN, "hollow": hollow}))
        g, _ = F.lookup_gate(comp_rows(10, 9, 5), [{"scene": f"s{i}"} for i in range(10)])
        (src / "gate.json").write_text(json.dumps(g))
    out = F.stage_probe_verdict(["p_tool", "p_code"], n_boot=50)
    runs = {r["run"]: r for r in json.loads((out / "verdict.json").read_text())["runs"]}
    assert runs["p_tool"]["status"] == "tested" and runs["p_code"]["status"] == f"tested, {F.HOLLOW}"
    md = (out / "verdict.md").read_text()
    assert f"**{F.LOOKUP_GATE_DESIGN}.**" in md and F.CAVEATS_1210B in md
    assert "| ○ Qwen3.6-27B | tool | L32 |" in md  # probe_run's manifest says tool; the hollow mark is the run's
    assert "lookup says and reads O and S right: 0.900" in md


def test_monitor_verdict_reads_the_lookup_datasets(tmp_path, monkeypatch):
    monkeypatch.setattr(M, "RESULTS", tmp_path / "results")
    monkeypatch.setattr(M, "CACHE", tmp_path / "cache")
    run = tmp_path / "results" / "mon_l"
    run.mkdir(parents=True)
    g, _ = F.lookup_gate(comp_rows(10, 9, 4), [{"scene": f"s{i}"} for i in range(10)])
    gates = {"code": {**g, "set": "d1_topics_v3"}, "tool": {**F.lookup_gate(comp_rows(10, 6, 9), [{"scene": f"s{i}"} for i in range(10)])[0], "set": "d1_topics_v3"}}  # fmt: skip
    x = {"formats": ["code", "tool"], "datasets": {"code": "code_l", "tool": "tool_l"}, "gates": gates,
         "design": F.LOOKUP_GATE_DESIGN}  # fmt: skip
    (run / "manifest.json").write_text(json.dumps({"model": {"target": "qwen3.6-27b"}, "x53_7": x}))
    monitor_cache(tmp_path / "cache", "mon_l", "code_l", {"full": 0.9})
    out = F.stage_monitor_verdict(["mon_l"], n_boot=50)
    blob = json.loads((out / "x53_7_monitor.json").read_text())
    assert {r["format"]: r["status"] for r in blob["runs"]} == {
        "code": "tested",
        "tool": "not tested (gate 0.600 < 0.80)",
    }
    assert "code_l" in blob["results"]["qwen3.6-27b"] and (out / "x53_7_monitor_code_l.png").exists()
    assert f"**{F.LOOKUP_GATE_DESIGN}.**" in (out / "verdict.md").read_text()
