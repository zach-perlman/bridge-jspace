"""x0_necessity's cells, labels and rule (jobs/c3/X0.md) on synthetic outcomes (no model)."""

import numpy as np

from scripts import x0_necessity as X


def outcomes(n: int, whole: int, no_part: int, no_rand: int) -> dict[str, list[int]]:
    """Per-item 0/1 switches with the given counts; items switched by a removal arm are a subset of the whole's."""
    return {"whole": [int(i < whole) for i in range(n)], "no_part": [int(i < no_part) for i in range(n)],
            "no_rand": [int(i < no_rand) for i in range(n)]}  # fmt: skip


def ents(n: int, k: int = 20) -> list[str]:
    return [f"e{i % k}" for i in range(n)]


def test_lookup_around_and_recall_through():
    lk = X.cell(outcomes(200, 160, 156, 156), ents(200), n_boot=2000)
    rc = X.cell(outcomes(200, 180, 40, 170), ents(200), n_boot=2000)
    assert lk["label"] == "around" and abs(lk["excess"][0]) < 1e-9
    assert rc["label"] == "through" and rc["Jdep"][0] > 0.7 and rc["excess"][1] >= 0.10
    assert X.split(lk, rc) and X.verdict(lk, rc) == "confirmed"


def test_invalid_cells_cannot_tell():
    weak = X.cell(outcomes(200, 50, 50, 50), ents(200), n_boot=500)  # S_whole 0.25 < 0.30
    few = X.cell(outcomes(80, 28, 28, 28), ents(80), n_boot=500)  # 35% but 28 < 30 items switched
    ok = X.cell(outcomes(200, 180, 40, 170), ents(200), n_boot=500)
    assert weak["label"] == few["label"] == "can't tell"
    assert X.verdict(weak, ok) == X.verdict(ok, few) == "can't tell"


def test_kill_and_the_zone_between():
    rc = X.cell(outcomes(200, 180, 40, 170), ents(200), n_boot=500)
    lk_needs = X.cell(outcomes(200, 160, 100, 156), ents(200), n_boot=500)  # excess 0.35
    assert X.verdict(lk_needs, rc) == "killed"
    lk_between = X.cell(outcomes(200, 160, 136, 160), ents(200), n_boot=500)  # excess 0.15
    assert X.verdict(lk_between, rc) == "not confirmed"
    lk = X.cell(outcomes(200, 160, 160, 160), ents(200), n_boot=500)
    rc_flat = X.cell(outcomes(200, 180, 150, 175), ents(200), n_boot=500)  # recall Jdep 0.17 < 0.20
    assert X.verdict(lk, rc_flat) == "killed"


def test_dependence_is_relative_to_the_whole_edit():
    c = X.cell(outcomes(100, 50, 25, 50), ents(100), n_boot=500)
    assert c["Jdep"][0] == 0.5 and c["Rdep"][0] == 0.0 and c["excess"][0] == 0.5


def test_resamples_are_paired_across_arms():
    # no_part identical to whole: every resample's Jdep is exactly 0, so its interval is a point
    sw = outcomes(120, 70, 70, 50)
    c = X.cell(sw, ents(120, 12), n_boot=1000)
    assert c["Jdep"] == [0.0, 0.0, 0.0]


def test_correlated_entities_widen_the_interval():
    n = 200
    rng = np.random.default_rng(0)
    whole = [1] * n
    per_entity = rng.integers(0, 2, 10)  # each entity's items all lose or all keep the switch without J
    no_part = [int(per_entity[i // 20]) for i in range(n)]
    sw = {"whole": whole, "no_part": no_part, "no_rand": whole}
    clustered = X.cell(sw, [f"e{i // 20}" for i in range(n)], n_boot=4000)
    independent = X.cell(sw, [f"e{i}" for i in range(n)], n_boot=4000)
    width = lambda c: c["Jdep"][2] - c["Jdep"][1]  # noqa: E731
    assert width(clustered) > 2 * width(independent)


def fake_rows(n_scenes: int = 60) -> list[dict]:
    """Outcome rows of one chat run at layers 30 and 32: the lookup loses nothing without J++, the recall loses most;
    every other dictionary costs neither reader."""
    rows = []
    for s in range(n_scenes):
        for la in (30, 32):
            for w in X.READERS:
                base = {"scene": f"s{s}", "domain": "greek", "entity": f"e{s % 12}", "rendering": "chat", "layer": la,
                        "reader": w, "upstream": s % 2 == 0, "role": "b", "cand_org_first": 0, "p_org": 0.1,
                        "p_alt": 0.8, "ld": 2.0, "ws_skipped": 0}  # fmt: skip
                rows.append(
                    {**base, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "switched": 1, "cand_switched": 1}
                )
                for d in X.DICTS:
                    kept = 1 - int(w == X.RECALL and d == "jpp" and s % 5 != 0)
                    rows.append({**base, "dict": d, "k": X.K_MAIN, "omp": "signed", "arm": "no_part", "switched": kept,
                                 "cand_switched": kept})  # fmt: skip
                    rows.append({**base, "dict": d, "k": X.K_MAIN, "omp": "signed", "arm": "no_rand", "switched": 1,
                                 "cand_switched": 1})  # fmt: skip
    return rows


def test_verdict_and_figures_on_a_fake_run(tmp_path, monkeypatch):
    import json

    monkeypatch.setattr(X, "RESULTS", tmp_path)
    run = tmp_path / "fake"
    run.mkdir()
    lens = {"name": "jpp", "source": ["repo", "file.pt", "rev"], "sha256": "ab" * 32}
    (run / "manifest.json").write_text(json.dumps({"predicted": 32, "set": "toy", "lens": lens,
                                                   "model": {"target": "toy", "revision": "0" * 40}}))  # fmt: skip
    gate = {"chat": {"org_accuracy": {"PP": 1.0, "PM": 1.0}, "pass": True, "eligible": 60}}
    (run / "gate.json").write_text(json.dumps({"counts": {}, "gate": gate}))
    (run / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in fake_rows()))
    out = X.write_verdict("fake", n_boot=300)
    v = json.loads((out / "verdict.json").read_text())["verdict"]
    assert v["chat"]["verdict"] == "confirmed" and v["chat"]["split_layers"] == [30, 32]
    assert v["chat"]["h_token"].startswith("neither") and v["reads_agree_on_whole"] == 1.0
    assert "S_noRandOMP" in (out / "verdict.md").read_text()
    made = X.figures(out)
    assert [p.name for p in made] == ["x0_chat.png"] and made[0].stat().st_size > 10_000


class FakeModel:
    """Vocabulary of 8: id 1 is ' ', id 2 '\\n', id 7 a special token that decodes to ''; the others are words. A row
    edited with {"ws": n} emits n whitespace tokens (alternating ' ' and '\\n') before the word 4; unedited rows say 4
    at once. The edit is seen on every forward, as generate_batch's hook applies it to the whole uncached prompt."""

    device = "cpu"
    special_ids = frozenset({7})

    def __init__(self, prompt_len: int):
        self.decoded = ["a", " ", "\n", "b", "4", "c", "d", ""]
        self.prompt_len, self.calls = prompt_len, []

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False):
        import torch

        assert ids.shape[0] == len(edits) and max_new_tokens == 1 and first_logits
        self.calls.append(ids.tolist())
        logits = torch.zeros(len(edits), len(self.decoded))
        for row, e in enumerate(edits):
            emitted = ids.shape[1] - self.prompt_len
            logits[row, (1, 2)[emitted % 2] if emitted < e.get("ws", 0) else 4] = 1.0
        return None, logits


def test_raw_read_skips_whitespace_and_chat_reads_after_the_space():
    prompt = [3, 5, 6]
    ws = X.whitespace_mask(FakeModel(3))
    assert ws.tolist() == [False, True, True, False, False, False, False, False]  # the special token is not whitespace
    m = FakeModel(3)
    logits, skipped = X.read_logits(m, prompt, [{}, {"ws": 1}, {"ws": 2}, {"ws": 9}], "raw", [1], ws)
    assert skipped == [0, 1, 2, X.RAW_STEPS - 1]
    assert [int(lg.argmax()) for lg in logits] == [4, 4, 4, 2]  # still on whitespace after RAW_STEPS: read there
    assert m.calls[1] == [[3, 5, 6, 1]] * 3  # the rows still on whitespace go on with the token they emitted
    assert m.calls[2] == [[3, 5, 6, 1, 2]] * 2 and len(m.calls) == X.RAW_STEPS
    m = FakeModel(4)  # chat: the prompt plus the space token, one forward
    logits, skipped = X.read_logits(m, prompt, [{}, {"ws": 2}], "chat", [1], ws)
    assert skipped == [0, 0] and m.calls == [[[3, 5, 6, 1]] * 2] and [int(lg.argmax()) for lg in logits] == [4, 1]


def test_gate_uses_the_decisive_read_and_skips_a_rendering_not_run():
    cases = [{"scene": f"s{i}", "rendering": "chat"} for i in range(200)]
    comp = [{"scene": f"s{i}", "rendering": "chat", "reader": w, "variant": v, "right": True, "read_right": i >= 30,
             "cand_right": True} for i in range(200) for w in X.READERS for v in ("org", "alt")]  # fmt: skip
    gate, eligible = X.gate_and_eligible(cases, comp)
    chat = gate["chat"]
    assert chat["org_accuracy"] == {"PP": 0.85, "PM": 0.85} and chat["said_accuracy"] == {"PP": 1.0, "PM": 1.0}
    assert chat["pass"] and chat["eligible"] == 170 and [c["scene"] for c in eligible["chat"]][:1] == ["s30"]
    assert gate["raw"]["cases"] == 0 and not gate["raw"]["pass"] and eligible["raw"] == []


class FakeGenModel:
    """Greedy continuations scripted per edit set: {"say": [token ids]}; logits put 1.0 on the said token each step."""

    device = "cpu"

    def generate_batch(self, ids, max_new_tokens, edits, first_logits=False, steps=False):
        import torch

        assert steps and ids.shape[0] == len(edits)
        new = torch.tensor([(e["say"] + [0] * max_new_tokens)[:max_new_tokens] for e in edits])
        logits = torch.zeros(len(edits), max_new_tokens, 12)
        logits.scatter_(2, new[:, :, None], 1.0)
        return None, logits, new


def test_digit_read_takes_the_first_digit_token(monkeypatch):
    monkeypatch.setattr(X, "READ", "digit")
    monkeypatch.setattr(X, "DIGIT_IDS", {5, 6})
    edits = [{"say": [7, 8, 5, 9]}, {"say": [6]}, {"say": [7, 7, 7]}]  # ' **' 'Locker' '5' / '6' / no digit
    logits, skipped = X.read_logits(FakeGenModel(), [1, 2], edits, "nochat", [3], None)
    assert skipped == [2, 0, -1]
    assert [int(lg.argmax()) for lg in logits] == [5, 6, 7]  # no digit: read at the first step, switches nothing
    chat, _ = X.read_logits(FakeModel(3), [3, 5, 6], [{}], "chat", [1], X.whitespace_mask(FakeModel(3)))
    assert int(chat[0].argmax()) == 4  # chat keeps the 23 Oct read


def test_descriptive_keeps_items_when_the_gate_fails(monkeypatch):
    cases = [{"scene": f"s{i}", "rendering": "nochat"} for i in range(40)]
    comp = [{"scene": f"s{i}", "rendering": "nochat", "reader": w, "variant": v, "right": True, "read_right": i < 20,
             "cand_right": True} for i in range(40) for w in X.READERS for v in ("org", "alt")]  # fmt: skip
    gate, eligible = X.gate_and_eligible(cases, comp)
    assert not gate["nochat"]["pass"] and eligible["nochat"] == []
    monkeypatch.setattr(X, "DESCRIPTIVE", True)
    gate, eligible = X.gate_and_eligible(cases, comp)
    assert gate["nochat"]["descriptive"] and len(eligible["nochat"]) == 20


def test_raw_renderings_end_without_a_trailing_space():
    item = {"question": "Which locker belongs to Iris's pick?"}
    raw, nochat = (X.render(None, item, r, "Iris picked the frog.") for r in ("raw", "nochat"))
    assert raw == "Iris picked the frog.\nQuestion: Which locker belongs to Iris's pick?\nAnswer:"
    assert nochat == raw.replace("\nAnswer:", "\n<think>\n\n</think>\n\nAnswer:")


def test_h_token_branches():
    around = X.cell(outcomes(200, 160, 156, 156), ents(200), n_boot=500)
    needs = X.cell(outcomes(200, 160, 100, 156), ents(200), n_boot=500)
    assert X.h_token(around, needs).startswith("token identity")
    assert X.h_token(around, around).startswith("neither")
    assert X.h_token(needs, needs).startswith("not applicable")


def test_single_change_alt(monkeypatch):
    item = {"id": "x", "bridge": "frog", "cf_bridge": "tick", "question": "Which locker belongs to Iris's pick?",
            "context": "Peter picked the rabbit. The locker of the tick is 2. Noah picked the tick. Iris picked the frog.",
            "cf_context": "Peter picked the rabbit. The locker of the tick is 2. Noah picked the frog. Iris picked the tick."}  # fmt: skip
    assert X.alt_context(item) == item["cf_context"]
    monkeypatch.setattr(X, "ALT", "single")
    assert X.alt_context(item) == item["context"].replace("Iris picked the frog.", "Iris picked the tick.")
