"""Batch 52 part A (scripts/x52_atoms.py): the classifier on planted tokens (E1 both reader views, Z2), the ordered
signed OMP against signed_omp (picks, coefficients, energy shares), the item draw, Δ from cached states and from a fake
model's forwards, and the report's class shares on planted atom lists. No real model."""

import json

import numpy as np
import pytest
import torch

from scripts import x0_necessity as X
from scripts import x52_atoms as A
from scripts.exp04_brew_parts import signed_omp

LK, RC = X.LOOKUP, X.RECALL


class FakeTok:
    """Word-level ids; words in `split` are two tokens (the first four characters, then the rest)."""

    def __init__(self, split: tuple[str, ...] = ()):
        self.vocab: dict[str, int] = {}
        self.split = split

    def _id(self, s: str) -> int:
        return self.vocab.setdefault(s, len(self.vocab))

    def encode(self, text: str, add_special_tokens: bool = False) -> list[int]:
        if text.strip() in self.split:
            k = 5 if text.startswith(" ") else 4
            return [self._id(text[:k]), self._id(text[k:])]
        return [self._id(text)]

    def decode(self, ids, skip_special_tokens: bool = False) -> str:
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv.get(int(i), f"w{int(i)}") for i in ids)


def e1_item() -> dict:
    ctx = ("The locker of carbon is 7. Adam picked hydrogen. Grace picked oxygen. The locker of oxygen is 3. "
           "The locker of hydrogen is 4. Oscar picked carbon.")  # fmt: skip
    cf = ctx.replace("Grace picked oxygen", "Grace picked carbon").replace("Oscar picked carbon", "Oscar picked oxygen")
    return {"scene": "s0", "key": "s0", "entity": "oxygen", "cf_bridge": "carbon", "domain": "elements",
            "context": ctx, "cf_context": cf,
            "readers": {LK: {"question": "Which locker belongs to Grace's pick?", "answer": "3", "cf_answer": "7"},
                        RC: {"question": "What is the atomic number of Grace's pick?", "answer": "8", "cf_answer": "6"}}}  # fmt: skip


def e1_vocab() -> dict[str, set[str]]:
    return {d: set(v) for d, v in A.SAME_CLASS.items()}


@pytest.mark.parametrize(
    ("token", "view", "want"),
    [
        (" Oxygen", LK, "bridge"),
        ("oxygen", RC, "bridge"),
        (" O", LK, "bridge"),  # the element's symbol
        (" Carbon", LK, "new_bridge"),
        ("C", RC, "new_bridge"),
        (" hydrogen", LK, "scene_item"),
        (" Grace", LK, "person"),
        (" Oscar", RC, "person"),
        (" three", LK, "answer_own"),  # the lookup's O answer
        ("Seven", LK, "answer_own"),  # its S answer
        (" eight", LK, "answer_other"),  # the recall's answer, seen from the lookup
        (" eight", RC, "answer_own"),
        (" three", RC, "answer_other"),
        (" sixth", RC, "answer_own"),  # ordinal
        (" nitrogen", LK, "same_class"),
        (" Helium", LK, "same_class"),
        (" He", LK, "function"),  # the pronoun: helium's symbol is not an alias
        (" the", LK, "function"),
        (".have", LK, "function"),
        ("水系", LK, "other"),
        (" five", LK, "other"),  # another number word: not either reader's answer
        (" locker", LK, "other"),
    ],
)
def test_e1_classes(token, view, want):
    tok = FakeTok()
    ctx = A.e1_context(tok, A.e1_scene(e1_item()), view, e1_vocab())
    tid = tok.encode(token)[0]
    assert A.classify(token, tid, ctx)[0] == want


def test_e1_details_and_via():
    tok = FakeTok()
    ctx = A.e1_context(tok, A.e1_scene(e1_item()), LK, e1_vocab())
    assert A.classify(" five", 0, ctx) == ("other", "", "answer kind")
    assert A.classify(" locker", 0, ctx) == ("other", "", "in the prompt")
    assert A.classify(" zzz", 0, ctx) == ("other", "", "")
    assert A.classify(" O", 0, ctx)[1] == "alias"


def test_e1_scene_words():
    sc = A.e1_scene(e1_item())
    assert sc["items"] == ["hydrogen"]
    assert sc["persons"] == ["Adam", "Grace", "Oscar"]
    assert sc["answers"] == {LK: ["3", "7"], RC: ["8", "6"]}


def test_first_piece_of_a_split_word():
    tok = FakeTok(split=("lithium",))
    item = {**e1_item(), "entity": "lithium"}
    ctx = A.e1_context(tok, A.e1_scene(item), LK, e1_vocab())
    piece = tok.encode(" lithium")[0]  # " lith"
    assert tok.decode([piece]) == " lith"
    assert A.classify(" lith", piece, ctx)[:2] == ("bridge", "first token")


def test_z2_classes():
    tok = FakeTok()
    text = ("Tess Garland visited Gothenburg. Barcelona was mentioned in this week's travel column. "
            "Which country is the city that is home to the Sagrada Familia in?")  # fmt: skip
    it = {"key": "jsuite_v2_test_chat|j2:cities:M-L0-Barcelona-0", "entity": "Barcelona", "cf_entity": "Bruges",
          "readers": {"K": {"answer": "Spain", "cf_answer": "Belgium"}}}  # fmt: skip
    ctx = A.z2_context(tok, A.z2_scene(it, "K", text))
    got = {t: A.classify(t, tok.encode(t)[0], ctx)[0] for t in
           (" Barcelona", " Bruges", " Gothenburg", " Tess", " Spain", " Spanish", " Belgian", " Seville", " France",
            " the", " Sagrada", "xyz")}  # fmt: skip
    assert got == {" Barcelona": "bridge", " Bruges": "new_bridge", " Gothenburg": "scene_item", " Tess": "person",
                   " Spain": "answer_own", " Spanish": "answer_own", " Belgian": "answer_own",
                   " Seville": "same_class", " France": "other", " the": "function", " Sagrada": "other",
                   "xyz": "other"}  # fmt: skip
    assert A.classify(" France", 0, ctx)[2] == "answer kind"
    assert A.classify(" Sagrada", 0, ctx)[2] == "in the prompt"


def test_omp_atoms_matches_signed_omp():
    g = torch.Generator().manual_seed(0)
    dic = torch.nn.functional.normalize(torch.randn(300, 32, generator=g), dim=-1)
    x = torch.stack([3 * dic[7] - 2 * dic[40] + 0.05 * torch.randn(32, generator=g), torch.randn(32, generator=g)])
    chosen, coefs, gains, approx = A.omp_atoms(dic, x, 10)
    assert torch.allclose(approx, signed_omp(dic, x, 10), atol=1e-5)
    assert set(chosen[0, :2].tolist()) == {7, 40}
    assert coefs[0, chosen[0].tolist().index(7)] == pytest.approx(3, abs=0.1)
    assert (gains >= -1e-9).all()
    share = approx.double().norm(dim=-1) ** 2 / x.double().norm(dim=-1) ** 2
    assert torch.allclose(gains.sum(1), share, atol=1e-6)


def test_pick_is_seeded_and_sorted():
    a = A.pick(75)
    assert a == A.pick(75) and a == sorted(a) and len(a) == A.N_ITEMS and len(set(a)) == A.N_ITEMS
    assert A.pick(30) == list(range(30))


class FakeModel:
    """run(ids, record) -> (logits, {layer: [seq, d]}): each position's state is a function of the ids up to it."""

    device = torch.device("cpu")

    def run(self, ids, record=()):
        seq = ids[0].tolist()
        h = torch.stack([torch.tensor([float(sum(seq[: i + 1])), float(len(seq[: i + 1])), float(seq[i])])
                         for i in range(len(seq))])  # fmt: skip
        return None, {la: h for la in record}


def test_forward_deltas_e1_shares_one_delta_and_z2_per_reader():
    e1 = [{"pos": 2, "readers": {LK: {"ids": {"org": [1, 2, 3, 9], "alt": [1, 2, 5, 9]}},
                                 RC: {"ids": {"org": [1, 2, 3, 7, 7], "alt": [1, 2, 5, 7, 7]}}}}]  # fmt: skip
    out, checks = A.forward_deltas(FakeModel(), "e1", e1, 4)
    assert set(out) == {LK, RC}
    assert np.allclose(out[LK][0], [2.0, 0.0, 2.0]) and np.allclose(out[RC][0], out[LK][0])
    assert checks["max_abs_delta_lookup_minus_recall"] == 0.0
    z2 = [{"readers": {"K": {"pos": 1, "ids": {"org": [1, 2, 3], "alt": [1, 4, 3]}},
                       "M": {"pos": 2, "ids": {"org": [5, 2, 3], "alt": [5, 2, 6]}}}}]  # fmt: skip
    out, _ = A.forward_deltas(FakeModel(), "z2", z2, 4)
    assert np.allclose(out["K"][0], [2.0, 0.0, 2.0]) and np.allclose(out["M"][0], [3.0, 0.0, 3.0])


def test_states_deltas(tmp_path, monkeypatch):
    from scripts import x51_jread as JR

    run = tmp_path / "fake_run"
    run.mkdir()
    ids = {w: {"org": [1, 2], "alt": [1, 3]} for w in X.READERS}
    X.write_jsonl(run / "cases.jsonl", [{"scene": s, "pos": 1, "readers": {w: {"ids": ids[w]} for w in X.READERS}}
                                         for s in ("a", "b")])  # fmt: skip
    h = np.zeros((2, 2, 2, 3, 2, 4), dtype=np.float16)  # [item, reader, O/S, P1-P3, layer, d]
    h[1, :, 1, 0, 1] = 1.5  # item b: S's state at the bridge word at the second cached layer
    np.savez(run / JR.STATES_FILE, h=h, layers=np.array([10, 12]))
    monkeypatch.setitem(JR.RUNS, "qwen3.5-9b", "fake_run")
    items = [{"scene": "b", "pos": 1, "readers": {w: {"ids": ids[w]} for w in X.READERS}}]
    out, checks = A.states_deltas(items, "qwen3.5-9b", 12, tmp_path)
    assert np.allclose(out[LK], 1.5) and checks["rows"] == [1] and checks["max_abs_delta_lookup_minus_recall"] == 0.0
    bad = [{**items[0], "pos": 0}]
    with pytest.raises(AssertionError):
        A.states_deltas(bad, "qwen3.5-9b", 12, tmp_path)


def test_json_safe_classes():
    assert json.loads(json.dumps(list(A.CLASSES))) == list(A.CLASS_TEXT)
    assert A.NUMBER_WORDS == __import__("scripts.suite_v1", fromlist=["WORDS"]).WORDS
