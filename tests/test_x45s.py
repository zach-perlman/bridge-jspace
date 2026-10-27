"""45s (Lightning at L30): the smoke's checks on fakes, the sealed verdict on planted runs, the hub-kernel record and the
placeholder refusal in jobq."""

from __future__ import annotations

import json

import pytest
import torch

from bridge_jspace import pins
from bridge_jspace.run_switches import hub_kernels
from scripts import jobq
from scripts import x0_necessity as X
from scripts import x45s as Z

SHA = "28017f36635a6b94d911333812beeed5dd901ac0"
OTHER = "0" * 40


# ---- the layer fixed in advance -----------------------------------------------------------------------------------


def test_lightning_has_its_layer_fixed_and_one_layer_only():
    assert X.PREDICTED[Z.TARGET] == 30 == Z.LAYER and X.LAYERS[Z.TARGET] == (30,)
    assert Z.TARGET in pins.TARGETS and pins.TARGETS[Z.TARGET]["run_prefix"] == "nem35l_"


def test_the_order_record_names_the_batch_and_the_row_order():
    o = X.order_record()
    assert o["batch"] == X.order_record()["batch"] and str(o["batch"]) in o["reads"]
    assert "sorted by scene id" in o["scenes"] and "batch of 2" in o["competence"]


# ---- kernels ------------------------------------------------------------------------------------------------------


def knll(nll: list[list[float]], top: list[list[int]], kernels: bool) -> dict:
    return {"nll": [torch.tensor(r) for r in nll], "top": [torch.tensor(r) for r in top], "kernels": kernels}


def test_kernel_compare_applies_zachs_bar():
    top = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    same = Z.kernel_compare(knll([[2.0] * 5, [3.0] * 5], top, True), knll([[2.0] * 5, [3.0] * 5], top, False))
    assert same["pass"] and same["diff"] == 0 and same["top1_agreement"] == 1.0 and same["positions"] == 10
    shifted = Z.kernel_compare(knll([[2.02] * 5, [3.02] * 5], top, True), knll([[2.0] * 5, [3.0] * 5], top, False))
    assert not shifted["pass"] and shifted["diff"] == pytest.approx(0.02, abs=1e-5)
    flipped = [[1, 2, 3, 4, 0], [6, 7, 8, 9, 10]]  # 9 of 10 agree: below 0.95
    assert not Z.kernel_compare(knll([[2.0] * 5] * 2, top, True), knll([[2.0] * 5] * 2, flipped, False))["pass"]
    with pytest.raises(AssertionError):
        Z.kernel_compare(knll([[2.0]], [[1]], False), knll([[2.0]], [[1]], True))


def test_kernel_revision_must_be_a_commit_and_the_loaded_one():
    loaded = {Z.KERNEL_REPO: [SHA], "kernels-community/activation": [OTHER]}
    assert Z.kernel_revision_check(loaded, SHA)["pass"]
    for expected in (None, "", "REVISION_FROM_ZACH", SHA[:7]):
        assert not Z.kernel_revision_check(loaded, expected)["pass"]
    assert not Z.kernel_revision_check(loaded, OTHER)["pass"]
    assert not Z.kernel_revision_check({}, SHA)["pass"]
    assert not Z.kernel_revision_check({Z.KERNEL_REPO: [SHA, OTHER]}, SHA)["pass"]  # two commits loaded


def test_hub_kernels_reads_commits_from_cached_module_paths():
    files = [f"/ephemeral/hf/hub/kernels--kernels-community--mamba-ssm/snapshots/{SHA}/build/torch28-cu128/mamba_ssm/__init__.py",
             f"/ephemeral/hf/hub/kernels--kernels-community--mamba-ssm/snapshots/{SHA}/build/torch28-cu128/mamba_ssm/ops.py",
             f"/x/hub/models--kernels-community--activation/snapshots/{OTHER}/build/v/activation/__init__.py",
             "/usr/lib/python3.12/json/__init__.py", "/x/hub/models--Qwen--Qwen3.6-27B/blobs/abc"]  # fmt: skip
    assert hub_kernels(files) == {"kernels-community/activation": [OTHER], "kernels-community/mamba-ssm": [SHA]}
    assert hub_kernels([]) == {}


# ---- the smoke's mechanics on a fake linear model -----------------------------------------------------------------

V, D = 12, 6


class FakeModel:
    """One 'layer': h = E[ids] (fp32), edits applied there; logits = W @ sum over positions. The whole change at the
    one position where org and alt differ therefore gives exactly the alt prompt's logits."""

    device = "cpu"
    special_ids = frozenset()

    def __init__(self):
        g = torch.Generator().manual_seed(0)
        self.E, self.W = torch.randn(V, D, generator=g), torch.randn(V, D, generator=g)
        self.decoded = [f"w{i}" for i in range(V)]

    def _h(self, ids: list[int], edit) -> torch.Tensor:
        h = self.E[torch.tensor(ids)].clone()
        return edit(h) if edit is not None else h

    def run(self, ids, edits=None, record=()):
        h = self._h(ids[0].tolist(), (edits or {}).get(Z.LAYER))
        return self.W @ h.sum(0), {la: h for la in record}

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False):
        assert max_new_tokens == 1 and first_logits and ids.shape[0] == len(edits)
        return None, torch.stack(
            [self.W @ self._h(row.tolist(), e.get(Z.LAYER)).sum(0) for row, e in zip(ids, edits, strict=True)]
        )


class FakeLens:
    def __init__(self, model: FakeModel):
        self.E = model.E

    def readout(self, h, layer):
        return self.E @ h


def fake_case(model: FakeModel, scene: str, org_b: int, alt_b: int) -> dict:
    prefix, suffix, space, pos = [1, 2, 3], [4, 5], [11], 3
    org, alt = [*prefix, org_b, *suffix], [*prefix, alt_b, *suffix]
    top = {
        v: int((model.W @ model.E[torch.tensor(ids + space)].sum(0)).argmax())
        for v, ids in (("org", org), ("alt", alt))
    }
    rd = {"id": scene, "ids": {"org": org, "alt": alt}, "tok_A": top["org"], "tok_b": top["alt"], "answer": "1",
          "cf_answer": "2", "question": "q"}  # fmt: skip
    return {
        "scene": scene,
        "domain": "animals",
        "pos": pos,
        "space": space,
        "readers": {X.LOOKUP: rd, X.RECALL: dict(rd)},
    }


def test_mechanics_noop_is_exact_the_write_lands_and_the_whole_change_switches_as_s():
    model = FakeModel()
    pairs = [(a, b) for a in range(6, 11) for b in range(6, 11) if a != b]
    cases = [fake_case(model, f"s{i}", a, b) for i, (a, b) in enumerate(pairs[:6])]
    rows = Z.mechanics(model, FakeLens(model), cases, Z.LAYER, lambda d: list(range(6, 11)))
    assert len(rows) == 12 and all(r["noop_exact"] and r["noop_max"] == 0 for r in rows)
    assert all(r["write_rel"] <= 1e-6 for r in rows)
    assert all(r["unedited_right"] and r["s_right"] for r in rows)
    assert all(r["whole_switched"] for r in rows)  # the whole change gives the alt prompt's logits: S's answer
    assert all(r["alone_vs_batch_max"] == 0 and r["alone_vs_batch_same_top"] for r in rows)
    assert all(1 <= r["lens_rank_org"] <= 5 and r["candidates"] == 5 for r in rows)
    s = Z.summarize(rows)
    assert s["pass"] and s["scenes"] == 6 and s["noop_exact"] == 12
    assert not Z.summarize([{**rows[0], "noop_exact": False}, *rows[1:]])["pass"]
    assert not Z.summarize([{**rows[0], "write_rel": 0.5}, *rows[1:]])["pass"]
    assert not Z.summarize([])["pass"]


def test_rank_among_counts_ties_against_the_target():
    scores = torch.tensor([0.0, 3.0, 3.0, 1.0])
    assert Z.rank_among(scores, 1, [0, 1, 2, 3]) == 2 and Z.rank_among(scores, 3, [0, 3]) == 1


def test_gate_status_labels_the_descriptive_band():
    def gate(pp, pm, enough=True):
        return {"gate": {"chat": {"org_accuracy": {"PP": pp, "PM": pm}, "eligible": 300, "enough": enough}}}

    assert Z.gate_status(gate(0.9, 0.8))["ok"] and Z.gate_status(gate(0.9, 0.8))["label"] == "pass"
    mid = Z.gate_status(gate(0.9, 0.77))
    assert not mid["ok"] and mid["label"].startswith("descriptive")
    assert Z.gate_status(gate(0.9, 0.7))["label"] == "fail" and not Z.gate_status(gate(0.95, 0.9, False))["ok"]


# ---- the sealed verdict on planted runs ---------------------------------------------------------------------------

BEFORE = "The locker of the frog is 5. The locker of the dog is 3. Iris picked the frog. Peter picked the tick. The locker of the tick is 2."
AFTER = "Iris picked the frog. Peter picked the tick. The locker of the frog is 5. The locker of the dog is 3. The locker of the tick is 2."
QUESTION = {X.LOOKUP: "Which locker belongs to Iris's pick?", X.RECALL: "How many legs does Iris's pick have?"}


def plant(root, run: str, alt: str, recall_lost: int, n: int = 20, gate_pass: bool = True) -> None:
    """A fake Lightning run at L30: n scenes with the locker before the pick and n after; in each group the recall
    loses the switch without J++ in its first `recall_lost` scenes (p_alt and ld drop with it), the lookup never; the
    random part keeps everything."""
    src = root / run
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"alt": alt, "predicted": Z.LAYER, "gate": 0.8,
                                                   "model": {"target": Z.TARGET}}))  # fmt: skip
    gate = {"cases": 2 * n, "org_accuracy": {"PP": 0.9 if gate_pass else 0.7, "PM": 0.9}, "pass": gate_pass,
            "eligible": 2 * n if gate_pass else 0, "enough": gate_pass}  # fmt: skip
    kernels = {Z.KERNEL_REPO: [SHA]}
    (src / "gate.json").write_text(json.dumps({"counts": {}, "gate": {"chat": gate}, "hub_kernels": kernels}))
    if not gate_pass:
        return
    cases, rows = [], []
    for group, ctx in (("before", BEFORE), ("after", AFTER)):
        for i in range(n):
            scene = f"{group}-{i:02d}"
            readers = {w: {"id": f"{scene}-{w}", "question": q, "answer": "5", "cf_answer": "3",
                           "ids": {"org": [1, 2, 3, 4], "alt": [1, 2, 9, 4]}} for w, q in QUESTION.items()}  # fmt: skip
            cases.append({"scene": scene, "rendering": "chat", "domain": "animals", "bridge": "frog", "cf_bridge": "dog",
                          "context": ctx, "upstream": False, "pos": 2, "readers": readers})  # fmt: skip
            for w in X.READERS:
                base = {"scene": scene, "domain": "animals", "entity": f"e{i % 7}", "rendering": "chat",
                        "layer": Z.LAYER, "reader": w, "upstream": False, "ws_skipped": 0, "cand_switched": 0}  # fmt: skip
                lost = w == X.RECALL and i < recall_lost
                for d, k, omp, arm, sw in (("-", 0, "-", "none", 0), ("-", 0, "-", "whole", 1),
                                           ("jpp", 25, "signed", "no_part", 0 if lost else 1),
                                           ("jpp", 25, "signed", "no_rand", 1)):  # fmt: skip
                    rows.append({**base, "dict": d, "k": k, "omp": omp, "arm": arm, "switched": sw, "top": 7 if sw else 6,
                                 "role": "b" if sw else "A", "p_org": 0.1, "p_alt": 0.9 if sw else 0.1,
                                 "ld": 2.0 if sw else -2.0})  # fmt: skip
    X.write_jsonl(src / "cases.jsonl", cases)
    X.write_jsonl(src / "outcomes.jsonl", rows)


@pytest.fixture
def runs(tmp_path, monkeypatch):
    monkeypatch.setattr(X, "RESULTS", tmp_path / "x0")
    monkeypatch.setattr(Z, "RESULTS", tmp_path / "x45s")
    (tmp_path / "x0").mkdir()
    (tmp_path / "x45s" / "smoke").mkdir(parents=True)
    (tmp_path / "x45s" / "smoke" / "report.json").write_text(json.dumps({"kernel_revision": {"loaded": [SHA]}}))
    return tmp_path / "x0"


def test_main_result_is_x0s_rule_with_the_gap_and_its_versions(runs):
    plant(runs, "main", "cf", recall_lost=10)
    r = Z.main_result("main", n_boot=200)
    assert r["status"] == "tested" and r["verdict"] == "confirmed" and r["labels"][0] == "around"
    assert r["cells"][X.RECALL]["Jdep"][0] == pytest.approx(0.5) and r["cells"][X.LOOKUP]["excess"][0] == 0
    g = r["groups"]
    assert g["all"]["n"] == 40 and g["locker-before"]["n"] == 20 and g["locker-after"]["n"] == 20
    assert g["all"]["switch"]["gap"][0] == pytest.approx(0.5) and g["all"]["ld"]["gap"][0] == pytest.approx(0.5)
    assert g["all"]["prob"]["prob_gap"][0] == pytest.approx(1 - 0.5 / 0.9)
    plant(runs, "killed", "cf", recall_lost=2)  # recall Jdep 0.1 < 0.20
    assert Z.main_result("killed", n_boot=200)["verdict"] == "killed"
    plant(runs, "nogate", "cf", recall_lost=10, gate_pass=False)
    assert Z.main_result("nogate", n_boot=200)["status"] == "not tested"
    plant(runs, "wrongalt", "fresh", recall_lost=10)
    with pytest.raises(AssertionError):
        Z.main_result("wrongalt", n_boot=200)


def test_clean_result_is_45ms_per_model_check(runs):
    plant(runs, "clean", "fresh", recall_lost=10)
    r = Z.clean_result("clean", n_boot=200)
    assert r["status"] == "tested" and r["holds"]  # locker-before: gap 0.5, lookup 0
    assert r["groups"]["locker-before"]["n"] == 20 and r["groups"]["all"]["n"] == 40
    plant(runs, "weak", "fresh", recall_lost=4)  # gap 0.2 < 0.3
    assert not Z.clean_result("weak", n_boot=200)["holds"]


def test_answers_need_each_questions_own_dan_line():
    text = "**Q46.1** x\n\nDan: (a) · 70%\n\n**Q46.2, Q46.3** (45s) are added here, unanswered.\n"
    assert Z.answers_in(text) == {"main": "", "clean": ""}
    text = ("**Q46.2** main?\n- (a) confirmed;\n\nRule: jobs/c3/x45s_a_lightning.yaml\n\nDan: (a) · 60%\n\n"
            "**Q46.3** clean?\n- (a) yes;\n\nDan:\n")  # fmt: skip
    assert Z.answers_in(text) == {"main": "(a) · 60%", "clean": ""}


class FakeTok:
    def decode(self, ids):
        return "".join(f"<{i}>" for i in ids)


def test_the_verdict_is_sealed_then_writes_both_rules_and_the_views(runs, monkeypatch):
    from scripts import statement_positions as SP

    plant(runs, "main", "cf", recall_lost=10)
    plant(runs, "clean", "fresh", recall_lost=10)
    monkeypatch.setattr(pins, "TARGET", Z.TARGET)
    monkeypatch.setattr(SP, "load_tokenizer", FakeTok)
    monkeypatch.setattr(Z, "dan_answers", lambda rev="HEAD": {"main": "", "clean": "(a) · 60%"})
    with pytest.raises(AssertionError, match="sealed"):
        Z.stage_verdict("main", "clean", "smoke", n_boot=200)
    monkeypatch.setattr(Z, "dan_answers", lambda rev="HEAD": {"main": "(a) · 60%", "clean": "(a) · 60%"})
    out = Z.stage_verdict("main", "clean", "smoke", n_boot=200)
    md = (out / "x45s.md").read_text()
    assert "CONFIRMED" in md and "HOLDS" in md and "| main | locker-before | 20 |" in md
    blob = json.loads((out / "x45s.json").read_text())
    assert blob["results"]["main"]["kernel_as_smoke"] and blob["results"]["clean"]["kernel_as_smoke"]
    view = (out / "view_main.md").read_text()
    assert view.count("**lookup**") == 10 and "⟦<3>⟧" in view and "S differs at positions [2]" in view
    assert "whole: '<7>' (b)" in view and "none: '<6>' (A)" in view


# ---- jobq: a placeholder blocks the spec --------------------------------------------------------------------------


def spec(command: str) -> dict:
    return {"id": "x45s_t", "thread": "C3", "command": command, "gpus": 1, "est_gpu_hours": 0.1, "question": "q?",
            "why_it_matters": "w", "hypotheses": {"H": "h"}, "decision_rule": "r", "controls": ["c"], "n": 8,
            "seeds": [0]}  # fmt: skip


def test_validate_refuses_a_placeholder_until_it_is_replaced():
    errors = jobq.validate(spec("export BJ_MAMBA_SSM_REVISION=REVISION_FROM_ZACH; python3 x.py --name nem35l_t"))
    assert errors == ["placeholder REVISION_FROM_ZACH in the command: replace it with the value before enqueue"]
    assert jobq.validate(spec(f"export BJ_MAMBA_SSM_REVISION={SHA}; python3 x.py --name nem35l_t")) == []
    assert jobq.validate(spec("BJ_DEVICE_MAP= BJ_SUITE_BATCH=16 python3 x.py --name nem35l_t")) == []
