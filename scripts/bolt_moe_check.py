"""bolt_moe_check (Zach, 2026-10-26, amendment 49 note 3): Bolt with the grouped-GEMM MoE (model._grouped_moe) against the
exact per-expert loop (model._fast_moe, bit-identical to NVIDIA's code) on the same loaded model: mean NLL and top-1
agreement on 16 pinned WikiText rows (128 tokens, as the harness reads raw text), the last-position logits of 16 chat
prompts from the dev set, and the forward time of a batch of 8 prompts. Pass: |NLL diff| <= 0.01 and top-1 agreement
>= 0.99. Writes results/checks/nem35b_moe_check.json.

python scripts/bolt_moe_check.py   (BJ_TARGET=nemotron-3.5-bolt)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import model as M  # noqa: E402
from bridge_jspace import pins  # noqa: E402
from bridge_jspace.tokens import raw_encoding  # noqa: E402
from scripts.ablate_v2 import tasks_prompts  # noqa: E402


@torch.no_grad()
def main() -> None:
    model = M.load_model()
    tok = model.tokenizer
    cls = type(model.hf)
    nh = sys.modules[cls.__module__].modeling_nemotron_h if hasattr(sys.modules[cls.__module__], "modeling_nemotron_h") else sys.modules[cls.__module__]
    texts = [ids for t in pins.wikitext_rows() if len(ids := raw_encoding(tok, t)["input_ids"][:128]) >= 64][:16]
    prompts = tasks_prompts(tok, "jsuite_v2_dev_chat", "nem35b_jsuite_v2_dev_chat_competence_smoke_1025", ["PM", "PK"], 8, ["clean"], "all") \
        if (pins.RESULTS_DIR / "tasks_v2" / "nem35b_jsuite_v2_dev_chat_competence_smoke_1025" / "summary.json").exists() else []
    if not prompts:  # no competence yet: the first 16 dev chat items as rendered
        from scripts import suite_v1 as S, tasks_v2 as T
        its = [x for x in T.load("jsuite_v2_dev_chat") if x.get("module") == "facts"][:16]
        prompts = [{"ids": S.ids(tok, T.render(tok, it))} for it in its]
    out = {}
    for name, fn in (("grouped", M._grouped_moe), ("exact", M._fast_moe)):
        nh.NemotronHMoE.moe = fn
        nll, tops = [], []
        for ids in texts:
            x = torch.tensor([ids], device="cuda")
            lg = model.hf(input_ids=x, use_cache=False).logits[0, :-1].float()
            nll.append(torch.nn.functional.cross_entropy(lg, x[0, 1:], reduction="none").cpu())
            tops.append(lg.argmax(-1).cpu())
        last = [model.hf(input_ids=torch.tensor([p["ids"]], device="cuda"), use_cache=False, logits_to_keep=1).logits[0, -1].float().cpu() for p in prompts[:16]]
        by_len = {}
        for p in prompts:
            by_len.setdefault(len(p["ids"]), []).append(p["ids"])
        batch = max(by_len.values(), key=len)[:8]
        torch.cuda.synchronize(); t0 = time.time()
        for _ in range(3):
            model.hf(input_ids=torch.tensor(batch, device="cuda"), use_cache=False, logits_to_keep=1)
        torch.cuda.synchronize()
        out[name] = {"nll": torch.cat(nll), "top": torch.cat(tops), "last": torch.stack(last), "sec_per_forward": (time.time() - t0) / 3, "batch": [len(batch), len(batch[0])]}
        print(f"{name}: mean NLL {out[name]['nll'].mean():.4f}, forward of {len(batch)} x {len(batch[0])} tokens {out[name]['sec_per_forward']:.3f}s", flush=True)
    g, e = out["grouped"], out["exact"]
    d = g["nll"].mean().item() - e["nll"].mean().item()
    agree = (g["top"] == e["top"]).float().mean().item()
    last_agree = (g["last"].argmax(-1) == e["last"].argmax(-1)).float().mean().item()
    res = {"nll_grouped": g["nll"].mean().item(), "nll_exact": e["nll"].mean().item(), "nll_diff": d, "top1_agreement": agree,
           "last_top1_agreement": last_agree, "last_max_abs_logit_diff": (g["last"] - e["last"]).abs().max().item(),
           "sec_per_forward": {"grouped": g["sec_per_forward"], "exact": e["sec_per_forward"]}, "batch": g["batch"],
           "pass": abs(d) <= 0.01 and agree >= 0.99}  # fmt: skip
    (pins.RESULTS_DIR / "checks").mkdir(exist_ok=True)
    (pins.RESULTS_DIR / "checks" / "nem35b_moe_check.json").write_text(json.dumps(res, indent=1) + "\n")
    print("MOECHECK", "PASS" if res["pass"] else "STOP", json.dumps(res))


if __name__ == "__main__":
    main()
