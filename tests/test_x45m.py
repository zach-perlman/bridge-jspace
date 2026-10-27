"""Batch 45, test 45m: the fresh alt (x0_necessity --alt fresh) on the target's tokenizer, the existing alts unchanged
against stored runs, and the rule (scripts/x45m.py) on planted runs."""

from __future__ import annotations

import json
import random
import re

import pytest

from scripts import suite_v1 as S
from scripts import tasks_v2 as T
from scripts import x0_necessity as X
from scripts import x45m as M

PICK = re.compile(r"^([A-Z][a-z]+) picked (?:the )?(\S+)\.$")
LOCKER = re.compile(r"^The locker of (?:the )?(\S+) is (\w+)\.$")


def sentences(context: str) -> list[str]:
    return re.split(r"(?<=\.) ", context)


def number(word: str) -> int:
    return int(word) if word.isdigit() else T.NUMBER_WORDS.index(word)


# ---- the fresh alt on the tokenizer -------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def tok():
    try:
        return M.tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


@pytest.fixture(scope="module")
def fresh(tok):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(X, "ALT", "fresh")
        mp.setattr(X, "RENDERINGS", ("chat",))
        return X.build_cases(tok, M.SET)


def test_fresh_alt_changes_one_token_to_an_item_nobody_picks(fresh):
    cases, counts = fresh
    assert cases and counts["scenes"] == 600
    original = {it["scene"]: it for it in T.load(M.SET) if it["word"] == X.LOOKUP}
    for c in random.Random(0).sample(cases, 80):
        info, new, org, alt = c["fresh"], c["cf_bridge"], c["context"], c["cf_context"]
        dom = T.DOMAINS[c["domain"]]
        # one token differs between org and alt, at the bridge; nothing upstream
        for rd in c["readers"].values():
            assert S.changed(rd["ids"]["org"], rd["ids"]["alt"]) == [c["pos"]]
        assert not c["upstream"]
        # the inserted sentence is once in both contexts; without it org is the main test's context
        assert org.count(info["sentence"]) == alt.count(info["sentence"]) == 1
        assert sentences(org)[info["sentence_index"]] == info["sentence"]
        assert (
            org.replace(info["sentence"] + " ", "", 1).replace(" " + info["sentence"], "", 1)
            == original[c["scene"]]["context"]
        )
        # alt differs from org only in the asked pick sentence, which now names the new item
        diff = [(a, b) for a, b in zip(sentences(org), sentences(alt), strict=True) if a != b]
        assert len(diff) == 1
        asked = re.search(r"([A-Z][a-z]+)'s pick", c["readers"][X.LOOKUP]["question"]).group(1)  # type: ignore[union-attr]
        assert diff[0] == (f"{asked} picked {T.ref(dom, c['bridge'])}.", f"{asked} picked {T.ref(dom, new)}.")
        # nobody picks the new item in org; in alt only the asked person
        for ctx, pickers in ((org, []), (alt, [asked])):
            got = [m.group(1) for s in sentences(ctx) if (m := PICK.match(s)) and m.group(2) == new]
            assert got == pickers
        assert new not in original[c["scene"]]["scene_facts"]["pick"].values()
        # locker digits unique, the new one not the item's own number
        lockers = {m.group(1): number(m.group(2)) for s in sentences(org) if (m := LOCKER.match(s))}
        assert len(lockers) == 4 and len(set(lockers.values())) == 4
        assert lockers[new] == info["digit"] != dom.values[new]
        # both readers' answers change; the recall's is the new item's number
        lk, rc = c["readers"][X.LOOKUP], c["readers"][X.RECALL]
        assert lk["cf_answer"] == str(info["digit"]) != lk["answer"]
        assert rc["cf_answer"] == str(dom.values[new]) != rc["answer"] == str(dom.values[c["bridge"]])
        assert lk["tok_A"] != lk["tok_b"] and rc["tok_A"] != rc["tok_b"]
        assert M.group_of(c) in ("locker-before", "locker-after", "mixed")


def test_fresh_draws_are_seeded_and_cover_every_slot(tok, fresh, monkeypatch):
    cases, _ = fresh
    monkeypatch.setattr(X, "ALT", "fresh")
    monkeypatch.setattr(X, "RENDERINGS", ("chat",))
    again, _ = X.build_cases(tok, M.SET)
    assert [c["fresh"] for c in again] == [c["fresh"] for c in cases]
    assert {c["fresh"]["slot"] for c in cases} == {0, 1, 2, 3}
    assert all(c["fresh"]["seed"] == X.FRESH_SEED for c in cases)


STORED = {"qwen3.6-27b": {"single": "x0_single_27b_r2", "cf": "x0_necessity_27b_chat"},
          "qwen3.5-9b": {"single": "qwen35_9b_x0_single_r2", "cf": "qwen35_9b_x0_necessity"},
          "muse-glimmer-30b": {"single": "muse30b_x0_single", "cf": "muse30b_x0_necessity"}}  # fmt: skip


@pytest.mark.parametrize("alt", ["single", "cf"])
def test_existing_alts_match_the_stored_cases(tok, monkeypatch, alt):
    from bridge_jspace import pins

    run = STORED.get(pins.TARGET, {}).get(alt)
    path = X.RESULTS / str(run) / "cases.jsonl"
    if run is None or not path.exists():
        pytest.skip(f"no stored {alt} run for {pins.TARGET}")
    stored = [c for c in X.read_jsonl(path) if c["rendering"] == "chat"]
    monkeypatch.setattr(X, "ALT", alt)
    monkeypatch.setattr(X, "RENDERINGS", ("chat",))
    built = {c["scene"]: {k: v for k, v in c.items() if k != "space"} for c in X.build_cases(tok, M.SET)[0]}
    for c in random.Random(0).sample(stored, 20):
        assert built[c["scene"]] == c


# ---- the rule on planted runs -------------------------------------------------------------------------------------

BEFORE = "The locker of the frog is 5. The locker of the dog is 3. Iris picked the frog. Peter picked the tick. The locker of the tick is 2."
AFTER = "Iris picked the frog. Peter picked the tick. The locker of the frog is 5. The locker of the dog is 3. The locker of the tick is 2."
MIXED = "The locker of the frog is 5. Iris picked the frog. The locker of the dog is 3. Peter picked the tick. The locker of the tick is 2."
QUESTIONS = {X.LOOKUP: "Which locker belongs to Iris's pick?", X.RECALL: "How many legs does Iris's pick have?"}
TARGETS = {"qwen3.5-9b": 12, "qwen3.6-27b": 32, "muse-glimmer-30b": 26}


def planted_case(scene: str, context: str) -> dict:
    return {"scene": scene, "rendering": "chat", "domain": "animals", "bridge": "frog", "cf_bridge": "dog",
            "context": context, "upstream": False, "readers": {w: {"question": q} for w, q in QUESTIONS.items()}}  # fmt: skip


def test_groups_read_both_locker_sentences():
    assert M.group_of(planted_case("a", BEFORE)) == "locker-before"
    assert M.group_of(planted_case("a", AFTER)) == "locker-after"
    assert M.group_of(planted_case("a", MIXED)) == "mixed"


def plant(root, run: str, target: str, lost: dict[str, dict[str, int]], n: int = 10, gate_pass: bool = True) -> None:
    """A fake 45m run: n scenes per group (before, after, mixed); `lost[group][reader]` scenes lose the switch without
    J++ (the random part keeps every switch), so that reader's extra loss there is lost / n."""
    src = root / run
    src.mkdir()
    layer = TARGETS[target]
    (src / "manifest.json").write_text(json.dumps({"alt": "fresh", "predicted": layer, "gate": 0.8,
                                                   "model": {"target": target}}))  # fmt: skip
    gate = {"cases": 3 * n, "org_accuracy": {"PP": 0.9 if gate_pass else 0.7, "PM": 0.9}, "pass": gate_pass,
            "eligible": 160, "enough": True}  # fmt: skip
    (src / "gate.json").write_text(json.dumps({"counts": {"scenes": 3 * n}, "gate": {"chat": gate}}))
    if not gate_pass:
        return
    cases, rows = [], []
    for group, ctx in (("before", BEFORE), ("after", AFTER), ("mixed", MIXED)):
        for i in range(n):
            scene = f"{group}-{i}"
            cases.append(planted_case(scene, ctx))
            for w in X.READERS:
                base = {"scene": scene, "entity": f"e{i}", "rendering": "chat", "layer": layer, "reader": w}
                rows.append({**base, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "switched": 1})
                rows.append({**base, "dict": "-", "k": 0, "omp": "-", "arm": "none", "switched": 0})
                rows.append({**base, "dict": "jpp", "k": 25, "omp": "signed", "arm": "no_rand", "switched": 1})
                kept = int(i >= lost.get(group, {}).get(w, 0))
                rows.append({**base, "dict": "jpp", "k": 25, "omp": "signed", "arm": "no_part", "switched": kept})
                rows.append({**base, "dict": "jpp", "k": 50, "omp": "signed", "arm": "no_part", "switched": 0})
    X.write_jsonl(src / "cases.jsonl", cases)
    X.write_jsonl(src / "outcomes.jsonl", rows)


SPLIT = {"before": {X.LOOKUP: 0, X.RECALL: 5}, "after": {X.LOOKUP: 0, X.RECALL: 0}}  # gap 0.5 before, 0 after
SMALL_GAP = {"before": {X.LOOKUP: 0, X.RECALL: 2}}  # gap 0.2
LOOKUP_LOSES = {"before": {X.LOOKUP: 2, X.RECALL: 6}}  # gap 0.4, lookup 0.2
AT_THE_BARS = {"before": {X.LOOKUP: 1, X.RECALL: 4}}  # gap 0.3, lookup 0.10


@pytest.fixture
def runs(tmp_path, monkeypatch):
    monkeypatch.setattr(X, "RESULTS", tmp_path)
    return tmp_path


def test_model_cells_and_the_rule(runs):
    plant(runs, "a", "qwen3.5-9b", SPLIT)
    m = M.model_result("a", n_boot=200)
    assert m["status"] == "tested" and m["holds"]
    assert m["n"] == {"locker-before": 10, "locker-after": 10, "mixed": 10, "all": 30}
    before, after, every = (m["cells"][g] for g in M.GROUPS)
    assert before["lookup"]["excess"][0] == pytest.approx(0) and before["recall"]["excess"][0] == pytest.approx(0.5)
    assert before["gap"][0] == pytest.approx(0.5) and before["gap"][1] <= 0.5 <= before["gap"][2]
    assert after["gap"][0] == pytest.approx(0) and every["gap"][0] == pytest.approx(5 / 30)
    assert not before["lookup"]["valid"]  # 10 switches < 30: the bar is reported, not in the rule
    for lost, ok in ((SMALL_GAP, False), (LOOKUP_LOSES, False), (AT_THE_BARS, True)):
        name = f"r{len(list(runs.iterdir()))}"
        plant(runs, name, "qwen3.5-9b", lost)
        assert M.model_result(name, n_boot=200)["holds"] is ok, lost


def test_verdict_counts_models_and_gate_failures(runs):
    plant(runs, "nine", "qwen3.5-9b", SPLIT)
    plant(runs, "twenty7", "qwen3.6-27b", SPLIT)
    plant(runs, "muse", "muse-glimmer-30b", SPLIT, gate_pass=False)
    plant(runs, "small", "muse-glimmer-30b", SMALL_GAP)
    models = {r: M.model_result(r, n_boot=200) for r in ("nine", "twenty7", "muse", "small")}
    assert models["muse"]["status"] == "not tested"
    assert M.verdict([models["nine"], models["twenty7"], models["muse"]])["label"] == "holds"
    v = M.verdict([models["nine"], models["small"], models["muse"]])
    assert v["label"] == "does not hold" and v["q45_10"] == "(b) no" and v["not_tested"] == ["muse"]
    assert M.verdict([models["nine"], models["twenty7"], M.model_result("absent", 200)])["label"] == "pending"
    out = M.score(["nine", "twenty7", "muse"], n_boot=200)
    blob = json.loads((out / "x45m.json").read_text())
    assert blob["verdict"]["label"] == "holds" and blob["verdict"]["models_tested"] == 2
    assert "**Verdict: holds**" in (out / "x45m.md").read_text()


def test_a_run_of_another_alt_or_layer_is_refused(runs):
    plant(runs, "a", "qwen3.5-9b", SPLIT)
    m = json.loads((runs / "a" / "manifest.json").read_text())
    (runs / "a" / "manifest.json").write_text(json.dumps({**m, "alt": "single"}))
    with pytest.raises(AssertionError):
        M.model_result("a", 200)
    (runs / "a" / "manifest.json").write_text(json.dumps({**m, "predicted": 14}))
    with pytest.raises(AssertionError):
        M.model_result("a", 200)


# ---- the job specs ------------------------------------------------------------------------------------------------

SPECS = {"x45m_9b": "qwen3.5-9b", "x45m_27b": "qwen3.6-27b", "x45m_muse": "muse-glimmer-30b"}


@pytest.mark.parametrize("job", list(SPECS))
def test_the_job_command_is_a_small_fresh_run_at_the_fixed_layer(job, monkeypatch):
    """The spec's x0_necessity command parses to the fresh alt, J++ k = 25 only (no curve, no non-negative arm), chat,
    the layer fixed in advance; its score step names the three 45m runs."""
    import shlex
    import sys

    import yaml

    spec = yaml.safe_load((X.pins.REPO_ROOT / "jobs" / "c3" / f"{job}.yaml").read_text())
    run_part, score_part = spec["command"].split(" && ")
    assert f"BJ_TARGET={SPECS[job]}" in run_part and spec["depends_on"] == ["x45_0_indep_9b"]
    words = shlex.split(run_part)
    args = words[words.index("scripts/x0_necessity.py") + 1 :]
    for name in ("CURVE_DICTS", "K_CURVE", "READ", "DESCRIPTIVE", "ALT", "CURVE_ALL", "DICTS", "READOUT", "NONNEG"):
        monkeypatch.setattr(X, name, getattr(X, name))  # main() sets them; restored after the test
    seen = {}
    monkeypatch.setattr(X, "stage_run", lambda name, why, set_name, layers, predicted, rends: seen.update(
        name=name, set=set_name, layers=layers, rends=rends, alt=X.ALT, dicts=X.DICTS, curve=X.K_CURVE, nonneg=X.NONNEG))  # fmt: skip
    monkeypatch.setattr(sys, "argv", ["x0_necessity.py", *args, "--sealed"])
    X.main()
    assert seen["alt"] == "fresh" and seen["dicts"] == ("jpp",) and seen["curve"] == () and not seen["nonneg"]
    assert seen["layers"] == (X.PREDICTED[SPECS[job]],) and seen["rends"] == ["chat"] and seen["set"] == M.SET
    runs = shlex.split(score_part)
    assert runs[runs.index("--runs") + 1 :] == ["qwen35_9b_x45m_fresh", "x45m_fresh_27b", "muse30b_x45m_fresh"]
    assert seen["name"] in runs
