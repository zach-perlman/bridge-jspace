"""port_smoke (22 Oct night): before any run on a newly pinned target, check the hooks on 2 tiny prompts.

  greedy      the greedy first token equals the argmax of the unedited forward's last logits
  residual    recording a layer gives [seq, d]; adding zeros there leaves the logits unchanged (max |diff| <= 1e-2),
              adding a random vector at the last position changes them
  blocking    knocking the list out of the last token's attention at every layer changes the logits; the same at half
              the heads changes them too (a head subset runs); an empty destination leaves them unchanged
  lens        the frozen lens loads (its sha256 checked) and reads layer n/2 out to [vocab] logits
Writes results/port_smoke/<name>/report.json; exits 1 if any check fails.

BJ_TARGET=... uv run python scripts/port_smoke.py --name <prefix>port_smoke
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bridge_jspace import pins
from bridge_jspace.tokens import raw_encoding
from scripts import suite_v1 as S
from scripts.exp04_brew_parts import AddRows

PROMPTS = [("The cow's locker is 5. The pig's locker is 3. The hen's locker is 7.", "Which locker belongs to the pig?"),
           ("The file on Peru is in drawer 2. The file on Chad is in drawer 8.", "Which drawer holds the file on Chad?")]  # fmt: skip


@torch.no_grad()
def main() -> int:
    from bridge_jspace.knockout import knock_out
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    a = ap.parse_args()
    pins.check_run_name(a.name)
    out = pins.RESULTS_DIR / "port_smoke" / a.name
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "report.json").exists(), f"{out} exists; runs are written once"
    t0 = time.time()
    model = load_model()
    tok = model.tokenizer
    mid = pins.N_LAYERS // 2
    checks: dict[str, list] = {"greedy": [], "residual_zero": [], "residual_push": [], "block_all": [],
                               "block_heads": [], "block_empty": []}  # fmt: skip
    for ctx, q in PROMPTS:
        text = S.render(tok, ctx, q)
        enc = raw_encoding(tok, text, offsets=True)
        ids = torch.tensor([enc["input_ids"]], device="cuda")
        logits, rec = model.run(ids, record=(mid,))
        _, first = model.generate_batch(ids, 1, [{}], first_logits=True)
        checks["greedy"].append(int(first[0].argmax()) == int(logits.argmax()))
        assert rec[mid].shape == (ids.shape[1], model.hf.config.get_text_config().hidden_size)
        last = ids.shape[1] - 1
        zero = AddRows(torch.zeros(1, rec[mid].shape[1], device="cuda"), [last])
        l0, _ = model.run(ids, {mid: zero})
        checks["residual_zero"].append(float((l0 - logits).abs().max()) <= 1e-2)
        push = AddRows(torch.randn(1, rec[mid].shape[1], device="cuda") * rec[mid][last].norm(), [last])
        l1, _ = model.run(ids, {mid: push})
        checks["residual_push"].append(float((l1 - logits).abs().max()) > 1e-2)
        c0 = text.index(ctx)
        src = [i for i, (s, e) in enumerate(enc["offset_mapping"]) if e > s and s >= c0 and e <= c0 + len(ctx)]
        all_layers = list(range(pins.N_LAYERS))
        n_heads = model.hf.config.get_text_config().num_attention_heads
        half: list[set[int] | None] = [set(range(n_heads // 2))]
        for key, heads, dst in (("block_all", None, [last]), ("block_heads", half, [last]), ("block_empty", None, [])):
            with knock_out(model, all_layers, [src], [dst], heads=heads):
                lk = model.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].float()
            changed = float((lk - logits).abs().max()) > 1e-2
            checks[key].append(not changed if key == "block_empty" else changed)
    lens_ok, lens_err = False, None
    try:
        lens = JLens(model, pins.FROZEN_LENS)
        lens_ok = tuple(lens.readout(rec[mid][-1:], mid).shape)[-1] == model.hf.lm_head.weight.shape[0]
    except Exception as e:  # no lens pinned yet, or a format problem: reported, not fatal here
        lens_err = f"{type(e).__name__}: {str(e)[:200]}"
    report = {"target": pins.TARGET, "model": pins.model_pin(), "checks": checks, "lens_ok": lens_ok, "lens_error": lens_err,
              "all_hooks_ok": all(all(v) for v in checks.values()), "seconds": round(time.time() - t0)}  # fmt: skip
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=1))
    return 0 if report["all_hooks_ok"] and (lens_ok or not pins.LENS_SOURCES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
