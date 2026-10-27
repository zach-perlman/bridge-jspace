"""scripts/indep_check.py's pure parts: signed OMP, the random part's share, item selection, the bridge position and its
marking, the verdict; the hook mechanics on a tiny random Qwen3.5 (built from a config, nothing downloaded)."""

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any

import numpy as np
import pytest
import torch

from scripts import indep_check as I

CASES = I.STORED_RUN / "cases.jsonl"


def unit_rows(n: int, d: int, seed: int) -> torch.Tensor:
    g = torch.Generator().manual_seed(seed)
    return torch.nn.functional.normalize(torch.randn(n, d, generator=g, dtype=torch.float64), dim=-1).float()


def naive_omp(atoms: np.ndarray, x: np.ndarray, k: int) -> tuple[list[int], np.ndarray]:
    """OMP written out with loops: every atom's |correlation| with the residual, the best unchosen one, then the
    least-squares refit on the chosen atoms."""
    chosen: list[int] = []
    fit = np.zeros_like(x)
    for _ in range(k):
        resid = x - fit
        best, best_score = -1, -1.0
        for i in range(atoms.shape[0]):
            score = abs(float(resid @ atoms[i]))
            if i not in chosen and score > best_score:
                best, best_score = i, score
        chosen.append(best)
        a = atoms[chosen]
        coef = np.linalg.lstsq(a.T, x, rcond=None)[0]
        fit = coef @ a
    return chosen, fit


def test_omp_matches_a_loop_implementation():
    atoms = unit_rows(40, 12, 0)
    x = torch.randn(6, 12, generator=torch.Generator().manual_seed(1))
    fit, chosen, coef = I.signed_omp(atoms, x, 5)
    for r in range(6):
        ref_idx, ref_fit = naive_omp(atoms.double().numpy(), x[r].double().numpy(), 5)
        assert chosen[r].tolist() == ref_idx
        assert np.allclose(fit[r].numpy(), ref_fit, atol=1e-5)
        assert np.allclose((coef[r] @ atoms[chosen[r]].double()).numpy(), ref_fit, atol=1e-5)


def test_omp_fit_is_the_least_squares_projection_on_its_atoms():
    atoms = unit_rows(50, 16, 2)
    x = torch.randn(4, 16, generator=torch.Generator().manual_seed(3))
    fit, chosen, _ = I.signed_omp(atoms, x, 6)
    for r in range(4):
        a = atoms[chosen[r]].double()
        assert len(set(chosen[r].tolist())) == 6  # no atom twice
        assert (a @ (x[r].double() - fit[r].double())).abs().max() < 1e-5  # residual orthogonal to the chosen atoms
    share = I.share_of(fit, x)
    assert ((share > 0) & (share <= 1 + 1e-6)).all()


def test_omp_recovers_a_signed_sparse_signal_and_matches_brute_force():
    """x = a signed combination of 3 atoms: OMP finds them with their signs, and so does the brute-force best 3-subset
    (every subset's least-squares residual)."""
    atoms = unit_rows(10, 30, 4)  # nearly orthogonal in 30 dimensions
    support, coefs = [2, 7, 5], torch.tensor([1.5, -2.0, 0.7])
    x = (coefs @ atoms[support])[None]
    fit, chosen, coef = I.signed_omp(atoms, x, 3)
    assert sorted(chosen[0].tolist()) == sorted(support)
    got = dict(zip(chosen[0].tolist(), coef[0].tolist(), strict=True))
    assert all(abs(got[s] - c) < 1e-5 for s, c in zip(support, coefs.tolist(), strict=True))
    assert (fit - x).abs().max() < 1e-5
    a, xv = atoms.double().numpy(), x[0].double().numpy()
    resid = {s: np.linalg.norm(xv - np.linalg.lstsq(a[list(s)].T, xv, rcond=None)[0] @ a[list(s)])
             for s in itertools.combinations(range(10), 3)}  # fmt: skip
    assert sorted(min(resid, key=lambda s: resid[s])) == sorted(support)


def test_omp_with_a_basis_rebuilds_x():
    basis = torch.eye(8)
    x = torch.randn(3, 8, generator=torch.Generator().manual_seed(5))
    fit, _, _ = I.signed_omp(torch.cat([basis, -basis]), x, 8)
    assert (fit - x).abs().max() < 1e-5


def test_haar_basis_is_orthonormal_and_seeded():
    q = I.haar_basis(32, 900)
    assert (q.T @ q - torch.eye(32)).abs().max() < 1e-4
    assert torch.equal(q, I.haar_basis(32, 900)) and not torch.equal(q, I.haar_basis(32, 901))


def test_random_part_keeps_the_share():
    d = 256
    x = torch.randn(50, d, generator=torch.Generator().manual_seed(6))
    share = torch.rand(50, generator=torch.Generator().manual_seed(7))
    share[0], share[1] = 0.0, 1.0
    part = I.random_part(x, share, I.haar_basis(d, 8))
    got = I.share_of(part, x)
    # nearest share over whole basis directions: off by at most one direction's (largest) contribution
    step = ((x @ I.haar_basis(d, 8)) ** 2).max(1).values / (x**2).sum(1)
    assert ((got - share).abs() <= step / 2 + 1e-5).all()
    assert (got - share).abs().max() < 0.05
    assert part[0].abs().max() == 0 and (part[1] - x[1]).abs().max() < 1e-4
    assert (part * (x - part)).sum(1).abs().max() < 1e-3  # an orthogonal projection: part ⟂ the rest


def test_select_scenes_needs_every_arm_for_both_readers():
    rows = []
    for s in range(30):
        for w in I.READERS:
            for arm in I.ARMS:
                if s == 3 and w == "PM" and arm == "no_rand":
                    continue  # scene 3 lacks one arm
                d, k, omp = I.stored_key(arm)
                rows.append({"scene": f"S{s:02d}", "rendering": "chat", "layer": 12, "reader": w, "arm": arm,
                             "dict": d, "k": k, "omp": omp})  # fmt: skip
    rows.append({"scene": "S99", "rendering": "chat", "layer": 12, "reader": "PP", "arm": "whole", "dict": "-", "k": 0,
                 "omp": "-"})  # fmt: skip
    rows += [{**r, "layer": 10, "scene": "T" + r["scene"]} for r in rows[:12]]  # another layer
    got = I.select_scenes(rows, 12, 5)
    pool = sorted(f"S{s:02d}" for s in range(30) if s != 3)
    assert got == random.Random(0).sample(pool, 5)
    with pytest.raises(ValueError):
        I.select_scenes(rows, 12, 30)


def test_bridge_span_and_holder():
    ctx = "Jordan picked the cat. The locker of the cat is 3. Dan picked the frog. The locker of the frog is 5."
    assert I.holder_of("Which locker belongs to Dan's pick?") == "Dan"
    s, e = I.bridge_span(ctx, "Which locker belongs to Dan's pick?", "frog")
    assert ctx[s:e] == "frog" and ctx[:s].endswith("Dan picked the ")
    s, e = I.bridge_span(ctx, "How many legs does Jordan's pick have?", "cat")
    assert ctx[s:e] == "cat" and s == len("Jordan picked the ")
    with pytest.raises(ValueError):
        I.bridge_span(ctx, "Which locker belongs to Dan's pick?", "cat")  # not Dan's pick
    with pytest.raises(ValueError):
        I.holder_of("Which locker is it?")


def test_mark_wraps_one_token():
    text = "Iris picked the frog."
    offsets = [(0, 4), (4, 11), (11, 15), (15, 20), (20, 21)]
    assert I.mark(text, offsets, 3) == "Iris picked the⟦ frog⟧."
    assert I.tokens_overlapping(offsets, 16, 20) == [3]


def test_summarize_rule():
    def rows(bad: dict[str, int]) -> list[dict]:
        out = []
        for i in range(20):
            for w in I.READERS:
                for arm in I.READ_ARMS:
                    ok = not (w == "PM" and i < bad.get(arm, 0))
                    out.append({"scene": f"S{i}", "reader": w, "arm": arm, "agree": ok, "my_role": "b",
                                "stored_role": "b" if ok else "A", "ld_diff": 0.125 if ok else 2.0})  # fmt: skip
        return out

    assert I.summarize(rows({}), 20)["verdict"] == "PASS"
    one = I.summarize(rows({"no_part": 1, "none": 5}), 20)  # the unedited row is not in the rule
    assert one["verdict"] == "PASS" and one["arms"]["no_part"]["items_agree"] == 19
    assert one["max_abs_ld_diff"] == 2.0
    assert I.summarize(rows({"no_rand": 2}), 20)["verdict"] == "FAIL"


def tokenizer_or_skip():
    from huggingface_hub import try_to_load_from_cache
    from transformers import AutoTokenizer

    path = try_to_load_from_cache(I.MODEL_REPO, "tokenizer.json", revision=I.MODEL_REVISION)
    if not isinstance(path, str) or not CASES.exists():
        pytest.skip("the 9B tokenizer or the stored X0 run is not here")
    return AutoTokenizer.from_pretrained(str(Path(path).parent))


def test_prompts_and_bridge_position_match_the_stored_cases():
    """Rendering, token ids, the bridge position and the answer tokens reproduce cases.jsonl (60 scenes)."""
    tok = tokenizer_or_skip()
    items: dict[str, dict] = {}
    for it in I.read_jsonl(I.ITEMS):
        items.setdefault(it["scene"], {})[it["word"]] = it
    stored = [json.loads(line) for line in CASES.read_text().splitlines()]
    stored = [c for c in stored if c["rendering"] == "chat"]
    for c in random.Random(1).sample(stored, 60):
        mine = I.build_case(tok, items[c["scene"]]["PP"], items[c["scene"]]["PM"])
        assert I.compare_case(mine, c) == {"ids": True, "pos": True, "answer_tokens": True}, c["scene"]
        pp = mine["readers"]["PP"]
        marked = I.mark(pp["text"]["org"], pp["offsets"]["org"], mine["pos"])
        assert f"{I.OPEN} {c['bridge']}{I.CLOSE}." in marked
        assert marked.startswith("<|im_start|>user\n") and marked.endswith("<think>\n\n</think>\n\nAnswer:")
    assert tok(" ", add_special_tokens=False)["input_ids"] == [220]


def tiny_qwen35():
    from transformers import Qwen3_5Config, Qwen3_5ForConditionalGeneration

    if importlib.util.find_spec("fla") is not None and not torch.cuda.is_available():
        pytest.skip("flash-linear-attention's kernels need a GPU")
    cfg = Qwen3_5Config(
        text_config={"hidden_size": 64, "intermediate_size": 128, "num_hidden_layers": 4, "num_attention_heads": 4,
                     "num_key_value_heads": 2, "head_dim": 16, "linear_num_key_heads": 2, "linear_num_value_heads": 4,
                     "linear_key_head_dim": 16, "linear_value_head_dim": 16, "vocab_size": 300,
                     "layer_types": ["linear_attention", "linear_attention", "linear_attention", "full_attention"]},
        vision_config={"depth": 1, "hidden_size": 32, "intermediate_size": 64, "num_heads": 2, "out_hidden_size": 64},
    )  # fmt: skip
    torch.manual_seed(0)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    hf: Any = Qwen3_5ForConditionalGeneration(cfg)
    return hf.to(device=device, dtype=torch.bfloat16).eval(), device


def test_hooks_on_a_tiny_qwen35():
    hf, dev = tiny_qwen35()
    layer, pos = 1, 5
    org = torch.randint(0, 300, (12,), generator=torch.Generator().manual_seed(0)).tolist()
    alt = list(org)
    alt[pos] = (org[pos] + 1) % 300
    h_org, gap = I.block_output(hf, layer, org, dev, check_hidden=True)
    h_alt, _ = I.block_output(hf, layer, alt, dev)
    assert gap == 0.0  # the hook reads block `layer`'s output = hidden_states[layer + 1]
    assert torch.equal(h_org[:pos], h_alt[:pos])  # causal: the change starts at pos
    delta = (h_alt[pos] - h_org[pos])[None]
    d = delta.shape[1]
    adds = torch.cat([torch.zeros(1, d), delta, torch.zeros(6, d)])
    batched = I.read_logits(hf, layer, org, pos, adds, dev)
    with torch.no_grad():
        plain = hf(input_ids=torch.tensor([org], device=dev), use_cache=False).logits[0, -1].float()
    assert torch.allclose(batched[0], plain, atol=0.05)  # an unedited row reads as the plain forward
    assert torch.equal(batched[0], batched[2]) and torch.equal(batched[0], batched[7])  # zero rows: no edit at all
    assert not torch.equal(batched[0], batched[1])

    # What the next block receives = block `layer`'s edited output: Δ turns org's row at pos into alt's (up to bf16
    # rounding of the sum) and leaves every other position as it was.
    seen: dict[str, torch.Tensor] = {}

    def next_input(_module, args, kwargs):
        seen["h"] = (args[0] if args else kwargs["hidden_states"]).float().clone()

    handle = I.text_model(hf).layers[layer + 1].register_forward_pre_hook(next_input, with_kwargs=True)
    try:
        I.read_logits(hf, layer, org, pos, torch.cat([torch.zeros(1, d), delta]), dev)
    finally:
        handle.remove()
    unedited, edited = seen["h"][0], seen["h"][1]
    # batched vs unbatched: bitwise on the CPU; GPU kernels may round differently by batch shape
    assert torch.equal(unedited, h_org) if dev == "cpu" else torch.allclose(unedited, h_org.to(dev), atol=0.05)
    assert torch.equal(edited[:pos], unedited[:pos]) and torch.equal(edited[pos + 1 :], unedited[pos + 1 :])
    assert (edited[pos] - h_alt[pos].to(dev)).abs().max() <= 0.01 * h_alt[pos].abs().max()
    assert not torch.equal(edited[pos], unedited[pos])
