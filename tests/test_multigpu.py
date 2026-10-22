"""Multi-GPU placement (BJ_DEVICE_MAP; bridge_jspace.model, Devices): the pure parts, and the tiny random Qwen3.5
hybrid of test_knockout split over two devices (embedding and blocks 0-3 home, blocks 4-7, final norm and head on the
other) against the same weights on one device.

The split needs two devices: two GPUs; or the CPU and a GPU or MPS (the Mac) when flash-linear-attention is absent
(its triton kernels cannot run the CPU half). Otherwise those tests skip. Tolerance: ABS = 1e-4 on fp32 outputs
(the two halves may run on different backends, which differ at ~1e-6 here); every comparison also checks that the
edit or knock-out it carries moves the output by > 100 x ABS, so a lost edit cannot pass. The head (unembed, lens) is
bf16 as in load_model: RTOL / ATOL are one bf16 rounding.
"""

from __future__ import annotations

import math
from typing import Any

import pytest
import torch

from bridge_jspace.knockout import FULL, attention_probs, kernel_path, knock_out
from bridge_jspace.lens import JLens
from bridge_jspace.model import Edit, Model, OnDevice, placement
from scripts.exp04_brew_parts import AddRows
from tests.test_knockout import TYPES, tiny_model

ABS = 1e-4
RTOL, ATOL = 1.6e-2, 1e-2
HOME_LAYER, OTHER_LAYER, LAST = 1, 6, 11  # an edit on each side of the split; the last of 12 positions


def split_devices() -> tuple[str, str] | None:
    if torch.cuda.device_count() >= 2:
        return "cuda:0", "cuda:1"
    if kernel_path() == "fla":
        return None
    if torch.cuda.is_available():
        return "cpu", "cuda:0"
    if torch.backends.mps.is_available():
        return "cpu", "mps"
    return None


SPLIT = split_devices()
needs_split = pytest.mark.skipif(SPLIT is None, reason="needs two devices (see the module docstring)")


# ---- pure parts -------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("spec", [None, "", "  "])
def test_placement_unset_is_one_gpu(spec):
    assert placement(spec) == {"device_map": "cuda"}


def test_placement_auto_and_capped():
    assert placement("auto") == {"device_map": "auto"}
    assert placement(" 0 : 30GiB , 1:75GiB ") == {"device_map": "auto", "max_memory": {0: "30GiB", 1: "75GiB"}}


@pytest.mark.parametrize("spec", ["balanced", "cpu:10GiB", "0=30GiB", "0:", "0:30GiB,", "1:75GiB", "0:1GiB,0:2GiB"])
def test_placement_rejects(spec):
    with pytest.raises(ValueError, match="BJ_DEVICE_MAP"):
        placement(spec)


def test_on_device_is_the_edit_itself_on_one_device():
    """No copies on one device: the edit gets the very tensor and its result comes back as is."""
    seen, made = [], []

    def edit(x: torch.Tensor) -> torch.Tensor:
        seen.append(x)
        made.append(x * 2)
        return made[-1]

    h = torch.randn(5, 8)
    out = OnDevice(edit, h.device)(h)
    assert seen[0] is h and out is made[0]


@needs_split
def test_on_device_runs_the_edit_home_and_returns_where_h_was():
    assert SPLIT is not None
    home, other = (torch.device(d) for d in SPLIT)
    g = torch.Generator().manual_seed(0)
    h, delta = torch.randn(5, 8, generator=g), torch.randn(2, 8, generator=g)
    edit = AddRows(delta.to(home), [1, 3])
    with pytest.raises(RuntimeError):  # what OnDevice is for: the edit's tensors and h on different devices
        edit(h.to(other))
    out = OnDevice(edit, home)(h.to(other))
    assert out.device.type == other.type
    assert torch.equal(out.cpu(), edit(h.to(home)).cpu())


# ---- the tiny model, one device vs split ------------------------------------------------------------------------------


class _Tokenizer:
    eos_token_id = 0

    def decode(self, ids, skip_special_tokens: bool = False) -> str:
        return " ".join(str(int(i)) for i in ids)


def _wrap(hf) -> Model:
    return Model(hf, _Tokenizer(), [], frozenset(), torch.zeros(61, dtype=torch.bool))


def _split(hf, home: str, other: str):
    from accelerate import dispatch_model

    n = len(TYPES)
    device_map: dict[str, Any] = {"model.embed_tokens": home, "model.rotary_emb": home, "model.norm": other,
                                  "lm_head": other}  # fmt: skip
    device_map |= {f"model.layers.{i}": home if i < n // 2 else other for i in range(n)}
    # main_device as a string: accelerate compares it with "cpu" (a torch.device would make the CPU half offloaded)
    return dispatch_model(hf, device_map=device_map, main_device=home)  # pyright: ignore[reportArgumentType]


@pytest.fixture(scope="module")
def pair() -> tuple[Model, Model]:
    """The fp32 tiny model on the home device, and the same weights split."""
    assert SPLIT is not None
    home, other = SPLIT
    one, two = _wrap(tiny_model().to(home)), _wrap(_split(tiny_model(), home, other))
    assert one.device == two.device and two.device.type == torch.device(home).type
    assert next(two.layers[HOME_LAYER].parameters()).device == two.device
    assert next(two.layers[OTHER_LAYER].parameters()).device.type == torch.device(other).type
    return one, two


def _ids(device: torch.device) -> torch.Tensor:
    return torch.randint(0, 61, (1, LAST + 1), generator=torch.Generator().manual_seed(0)).to(device)


def _edits(device: torch.device) -> dict[int, Edit]:
    delta = torch.randn(3, 32, generator=torch.Generator().manual_seed(1)).to(device)
    return {HOME_LAYER: AddRows(delta, [2, 3, 4]), OTHER_LAYER: AddRows(delta, [5, 6, LAST])}


def _close(a: torch.Tensor, b: torch.Tensor, home: torch.device) -> None:
    assert a.device == b.device == home
    assert float((a - b).abs().max()) <= ABS


def test_run_on_one_device_is_the_plain_hooked_forward():
    """On one device Model.run is the hooked forward it always was: logits and the recorded output bit for bit."""
    hf = tiny_model()
    model = _wrap(hf)
    ids, edits = _ids(model.device), _edits(model.device)
    got, rec = model.run(ids, edits, record=(OTHER_LAYER,))
    ref_rec: dict[int, torch.Tensor] = {}

    def hook_for(layer: int):
        def hook(_module, _args, out):
            h = out[0] if isinstance(out, tuple) else out
            h = edits[layer](h[0].float()).to(h.dtype)[None]
            ref_rec[layer] = h[0].float().clone()
            return (h, *out[1:]) if isinstance(out, tuple) else h

        return hook

    handles = [model.layers[la].register_forward_hook(hook_for(la)) for la in edits]
    try:
        with torch.no_grad():
            ref = hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].float()
    finally:
        for handle in handles:
            handle.remove()
    assert torch.equal(got, ref) and torch.equal(rec[OTHER_LAYER], ref_rec[OTHER_LAYER])


@needs_split
def test_split_run_matches_one_device(pair):
    one, two = pair
    home = two.device
    ids, edits = _ids(home), _edits(home)
    clean, _ = one.run(ids)
    l1, r1 = one.run(ids, edits, record=(HOME_LAYER, OTHER_LAYER))
    l2, r2 = two.run(ids, edits, record=(HOME_LAYER, OTHER_LAYER))
    assert float((l1 - clean).abs().max()) > 100 * ABS
    _close(l1, l2, home)
    for layer in (HOME_LAYER, OTHER_LAYER):
        _close(r1[layer], r2[layer], home)


@needs_split
def test_split_generate_batch_matches_one_device(pair):
    one, two = pair
    home = two.device
    ids, edits = _ids(home), [{}, {OTHER_LAYER: _edits(home)[OTHER_LAYER]}]
    t1, f1 = one.generate_batch(ids, 3, edits, first_logits=True)
    t2, f2 = two.generate_batch(ids, 3, edits, first_logits=True)
    assert float((f1[1] - f1[0]).abs().max()) > 100 * ABS
    assert t1 == t2
    _close(f1, f2, home)


@needs_split
def test_split_knock_out_and_attention_match_one_device(pair):
    one, two = pair
    home = two.device
    ids = _ids(home)
    clean, _ = one.run(ids)
    knocked = []
    for m in (one, two):
        with knock_out(m, range(len(TYPES)), [[2, 3, 4, 5]], [[LAST]]):
            knocked.append(m.run(ids)[0])
    assert float((knocked[0] - clean).abs().max()) > 100 * ABS
    _close(knocked[0], knocked[1], home)
    full = [la for la, kind in enumerate(TYPES) if kind == FULL]  # one on each side of the split
    a1, a2 = attention_probs(one, ids, full, [LAST]), attention_probs(two, ids, full, [LAST])
    for la in full:
        _close(a1[la], a2[la], home)


def _lens(model: Model, maps: dict[int, torch.Tensor]) -> JLens:
    """A JLens over the given maps, built without a lens file (only what readout and vectors use)."""
    lens = JLens.__new__(JLens)
    lens._J_cpu, lens._J_gpu, lens.model = maps, {}, model
    lens._gain, lens._w_u = model.norm_gain(), model.hf.lm_head.weight
    return lens


@needs_split
@torch.no_grad()
def test_split_head_and_lens_match_one_device():
    """unembed, the lens's readout (of a residual home or on the other device) and vectors on the bf16 head."""
    assert SPLIT is not None
    home, other = SPLIT
    one = _wrap(tiny_model().to(home, torch.bfloat16))
    two = _wrap(_split(tiny_model().to(torch.bfloat16), home, other))
    g = torch.Generator().manual_seed(2)
    maps = {OTHER_LAYER: torch.randn(32, 32, generator=g) / math.sqrt(32)}
    h = torch.randn(4, 32, generator=g).to(two.device)
    token_ids = torch.tensor([3, 17, 42], device=two.device)
    lens1, lens2 = _lens(one, maps), _lens(two, maps)
    for got, ref in (
        (two.unembed(h), one.unembed(h)),
        (two.norm_gain(), one.norm_gain()),
        (lens2.readout(h, OTHER_LAYER), lens1.readout(h, OTHER_LAYER)),
        (lens2.readout(h.to(other), OTHER_LAYER), lens1.readout(h, OTHER_LAYER)),
        (lens2.vectors(OTHER_LAYER, token_ids), lens1.vectors(OTHER_LAYER, token_ids)),
    ):
        assert got.device == two.device
        torch.testing.assert_close(got, ref, rtol=RTOL, atol=ATOL)
