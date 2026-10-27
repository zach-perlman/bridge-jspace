"""d5a_natural_errors (Dan's D5a, 2026-10-21, night): when the model gets a lookup wrong on its own (no patch), which
statement do the late lookup heads look at: the one its (wrong) answer comes from, or the right one?

Why. In d5a_head_pointer the head (layer 51, head 22) followed the new statement on 58% of patched items, but a patch
copies the alt prompt's query, so following it is partly built in. Natural errors have no patch: if the head looks at
the statement the wrong answer is taken from, it marks where the answer is fetched from (a provenance read-out); if
it looks at the right statement, it marks where the bridge is, and the error happens after it.

Items. alias_pointer_v1, main and dev sets, memory -> prompt (RL) and named -> prompt (DL), every level (English,
other languages, chemical symbols: the 27B's errors are mostly recalled elements named by their symbol). Unedited
org prompts only. One forward per item: the read (pointer_swap's: the space token appended), the attention from the
last token of each listed head summed over each statement's tokens (bridge_jspace.knockout.capture_attention).
Row: the answer (top token), right or not, the statement holding the answered digit (if it is in the prompt), the
asked statement, and each head's top statement.

Decision rule (fixed before the run; jobs/d5/d5a_natural_errors_27b.yaml). Primary: layer 51 head 22, rows answered
wrong with a digit of another statement ("wrong in context"), all levels and families pooled; Wilson 95% on rows
(the asked entity is reported, k entities). n >= 35 needed, else "too few errors".
  H-fetch: the share of wrong-in-context rows where the head's top statement is the answered one has lower bound above
    the upper bound of the share where it is the right (asked) one.
  H-bridge: the reverse.
  Otherwise neither. Control: on rows answered right, the head's top statement is the asked one (d2_lookup_heads: 100%
  on pointer_v1). The other heads get the same numbers, not a verdict.

Stages:  run --name N --why W [--heads 51:22 59:21 59:3] [--sets main dev] | summarise --name N (CPU)
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson
from scripts import alias_pointer_v1 as AP
from scripts import d5a_head_pointer as D
from scripts import pointer_swap as PS
from scripts import pointer_v1 as PV
from scripts import suite_v1 as S

EXP = "d5a_natural_errors"
RESULTS = pins.RESULTS_DIR / EXP
HEADS = ("51:22", "59:21", "59:3")
FAMILIES = ("RL", "DL")
MIN_N = 35


def item_files(sets: list[str]) -> dict[str, Path]:
    return {f"{s}/{lab}": f for s in sets for lab, f in AP.set_files(s).items()
            if lab.split("_")[1] in FAMILIES and f.exists()}  # fmt: skip


@torch.no_grad()
def stage_run(name: str, why: str, heads: list[str], sets: list[str], limit: int | None = None) -> None:
    from bridge_jspace.utils import progress
    from scripts.exp03_brew_swaps import write_jsonl

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    files = item_files(sets)
    root = pins.REPO_ROOT
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "format": chat.format_note(), "heads": heads, "sets": sets, "limit": limit,
         "items": {k: {"file": str(f.relative_to(root)), "sha256": sha256_of(f)} for k, f in files.items()},
         "decision": (__doc__ or "").split("Decision rule")[1].split("Stages:")[0].strip()}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = D.load_target()
    hf, tok = model.hf, model.tokenizer
    hs = D.parse_heads(heads)
    att_layers = sorted({la for la, _ in hs})
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    rows, skipped = [], collections.Counter()
    items = [(k, it) for k, f in files.items() for it in PV.load_file(f)[:limit]]
    t0 = time.time()
    for label, it in progress(items, "items"):
        try:
            prep = PS.prepare(it, tok)
            stmts = D.statement_tokens(prep, it)
        except (AssertionError, ValueError):
            skipped[label] += 1
            continue
        logits, probs, _ = D.patched_forward(hf, prep["read_ids"]["base"], [{}], att_layers, None)
        top = int(logits[0].argmax())
        digit = digit_tok.get(top)
        digits = [str(d) for d in it["digits"]]
        reads = {}
        for la, h in hs:
            masses = [float(probs[la][0, h, 0][s].sum()) for s in stmts]
            reads[f"{la}:{h}"] = {"top": max(range(len(masses)), key=lambda i, ms=masses: ms[i]),
                                  "masses": [round(x, 4) for x in masses]}  # fmt: skip
        rows.append({"id": it["id"], "set": label.split("/")[0], "label": label, "family": it["family"],
                     "domain": it["domain"], "level": it["level"], "entity": it["query"], "top": tok.decode([top]),
                     "right": digit == it["answer"], "asked": it["slots"]["query"],
                     "answered": digits.index(digit) if digit in digits else None, "heads": reads})  # fmt: skip
    write_jsonl(out_dir / "rows.jsonl", rows)
    (out_dir / "check.json").write_text(json.dumps({"rows": len(rows), "skipped": dict(skipped),
                                                    "seconds": round(time.time() - t0)}, indent=2) + "\n")  # fmt: skip
    stage_summarise(name)


def share(rows: list[dict], hit) -> dict[str, Any]:
    k, n = sum(bool(hit(r)) for r in rows), len(rows)
    p, lo, hi = wilson(k, n) if n else (0.0, 0.0, 0.0)
    return {"k": k, "n": n, "rate": [round(p, 4), round(lo, 4), round(hi, 4)],
            "entities": len({(r["domain"], r["entity"]) for r in rows})}  # fmt: skip


def stage_summarise(name: str) -> None:
    out_dir = RESULTS / name
    m = json.loads((out_dir / "manifest.json").read_text())
    rows = [json.loads(x) for x in (out_dir / "rows.jsonl").read_text().splitlines()]
    wrong = [r for r in rows if not r["right"] and r["answered"] is not None and r["answered"] != r["asked"]]
    right = [r for r in rows if r["right"]]
    out: dict[str, Any] = {"n_rows": len(rows), "n_right": len(right), "n_wrong_in_context": len(wrong),
                           "n_wrong_off_prompt": sum(not r["right"] and r["answered"] is None for r in rows),
                           "wrong_by_label": dict(collections.Counter(r["label"] for r in wrong)), "heads": {}}  # fmt: skip
    for head in m["heads"]:
        on_answered = share(wrong, lambda r, h=head: r["heads"][h]["top"] == r["answered"])
        on_asked = share(wrong, lambda r, h=head: r["heads"][h]["top"] == r["asked"])
        control = share(right, lambda r, h=head: r["heads"][h]["top"] == r["asked"])
        verdict = "too few errors"
        if len(wrong) >= MIN_N:
            verdict = ("H-fetch" if on_answered["rate"][1] > on_asked["rate"][2]
                       else "H-bridge" if on_asked["rate"][1] > on_answered["rate"][2] else "neither")  # fmt: skip
        out["heads"][head] = {"wrong_on_answered": on_answered, "wrong_on_asked": on_asked, "right_on_asked": control,
                              "verdict": verdict}  # fmt: skip
    dest = out_dir / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    dest.mkdir()
    (dest / "summary.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({h: v["verdict"] for h, v in out["heads"].items()} | {"n_wrong_in_context": len(wrong)}))
    print("wrote", dest / "summary.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "summarise"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--heads", nargs="+", default=list(HEADS))
    ap.add_argument("--sets", nargs="+", default=["main", "dev"])
    ap.add_argument("--limit", type=int, default=None, help="the first K items per file (a smoke)")
    args = ap.parse_args()
    if args.stage == "run":
        assert args.why, "run needs --why"
        stage_run(args.name, args.why, args.heads, args.sets, args.limit)
    else:
        stage_summarise(args.name)
