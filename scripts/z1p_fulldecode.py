"""z1p_fulldecode: F5 of the 9B's Z1-P run (qwen35_9b_x52_z1p) on a GPU box (POST HOC; Dan 30 Oct).

The count reads the answer's FIRST token (x50_zach.route). When the stored first token tok_A or tok_b has at most two characters ("A" of Austria, "E" of
Ecuador) another word can start with it. For the items with such a token (both readers' passages of a scene are rebuilt, only the flagged reader is decoded)
this greedy-decodes 4 tokens in each arm (none, whole, without the lens part, without a same-size random part) at L12, same Delta, same OMP, same random part
as the run, and labels the continuation by the FULL word: A if the text starts with (or is a start of) the original answer word, b likewise for the changed
answer, "ambiguous" if both fit, else other. Reports how many arm rows change label against the first-token label.

Pre-set (Dan 30 Oct): recompute the z1p numbers if more than 5% of the arm rows change label (rows = the flagged items x 4 arms). The recompute sets
`switched` of the changed rows to the full-word label (b = switched) and runs x50_zach.layer_result on all 200 passages; items with a longer first token keep
their stored label.

BJ_TARGET=qwen3.5-9b uv run python scripts/z1p_fulldecode.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace import pins  # noqa: E402
from scripts import x0_necessity as X  # noqa: E402
from scripts import x50_zach as Z  # noqa: E402

RUN = "qwen35_9b_x52_z1p"
SHORT = 2
N_NEW = 4
BAR = 0.05


def label_full(text: str, rd: dict) -> str:
    t = text.strip().casefold()
    a, b = str(rd["answer"]).casefold(), str(rd["cf_answer"]).casefold()
    fa = bool(t) and (t.startswith(a) or a.startswith(t))
    fb = bool(t) and (t.startswith(b) or b.startswith(t))
    return "ambiguous" if fa and fb else "A" if fa else "b" if fb else "other"


def main() -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts import statement_positions as SP
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    target = pins.TARGET
    assert target == "qwen3.5-9b", target
    src = Z.RESULTS / RUN
    la = Z.LAYERS[target][0]
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "runs" / "z1p_fulldecode" / stamp
    out.mkdir(parents=True, exist_ok=False)
    gate = json.loads((src / "gate.json").read_text())
    cases = {(c["set"], c["scene"]): c for c in X.read_jsonl(src / "cases.jsonl")}
    chosen = [cases[tuple(k)] for k in gate["order"]]
    stored = {
        (r["set"], r["scene"], r["reader"], r["arm"]): r
        for r in X.read_jsonl(src / "outcomes.jsonl")
        if r["layer"] == la
    }
    (out / "manifest.json").write_text(json.dumps({"exp": "z1p_fulldecode", "post_hoc": True, "model": target, "run": RUN, "layer": la, "short_token_max_chars": SHORT, "new_tokens": N_NEW,
                                                   "rule": f"recompute the z1p numbers if more than {BAR:.0%} of the arm rows (flagged items x 4 arms) change label",
                                                   "written_utc": stamp}, indent=2) + "\n")  # fmt: skip
    R.warm_cusolver()
    model = load_model()
    tok, dev = model.tokenizer, model.device
    flagged = []
    for c in chosen:
        for r, rd in c["readers"].items():
            if min(len(tok.decode([rd["tok_A"]]).strip()), len(tok.decode([rd["tok_b"]]).strip())) <= SHORT:
                flagged.append((c, r))
    scenes = list(dict.fromkeys((c["set"], c["scene"]) for c, _ in flagged))
    sub = [cases[k] for k in scenes]
    print(f"{len(flagged)} flagged items in {len(sub)} scenes", flush=True)
    ARMS = Z.ARMS
    with torch.no_grad():
        deltas = {r: [] for r in ("K", "M")}
        for c in progress(sub, "delta at the patch token"):
            for r, rd in c["readers"].items():
                h = {
                    v: model.run(torch.tensor([rd["ids"][v]], device=dev), record=(la,))[1][la][rd["pos"]].float()
                    for v in ("org", "alt")
                }
                deltas[r].append(h["alt"] - h["org"])
        jdic = JLens(model, "jpp").vectors(la, model.letter_token_ids()).to(dev)
        basis = SP.random_basis(jdic.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + la)).to(dev)
        arms = {}
        for r in ("K", "M"):
            x = torch.stack(deltas[r]).to(dev)
            more, _ = R.removal_arms(x, {"jpp": X.fit(jdic, x, X.K_MAIN, "signed").to(dev)}, basis)
            arms[r] = {"whole": x, **more}
        index = {k: i for i, k in enumerate(scenes)}
        rows = []
        for c, r in progress(flagged, "greedy 4 tokens x 4 arms (item)"):
            rd, i = c["readers"][r], index[(c["set"], c["scene"])]
            edits = [{}] + [{la: AddRows(arms[r][a][i : i + 1], [rd["pos"]])} for a in ARMS]
            texts, _, new = model.generate_batch(torch.tensor([rd["ids"]["org"]], device=dev), N_NEW, edits, steps=True)
            for a, text, ntok in zip(("none", *ARMS), texts, new, strict=True):
                top = int(ntok[0])
                first = "b" if top == rd["tok_b"] else "A" if top == rd["tok_A"] else "other"
                s = stored[(c["set"], c["scene"], r, a)]
                rows.append({"set": c["set"], "scene": c["scene"], "reader": r, "arm": a, "text": text, "first_token_label": first, "stored_label": s["role"],
                             "stored_top_reproduced": top == s["top"], "full_word_label": label_full(text, rd), "answer": rd["answer"], "cf_answer": rd["cf_answer"]})  # fmt: skip
    X.write_jsonl(out / "decoded.jsonl", rows)
    changed = [r for r in rows if r["full_word_label"] not in (r["stored_label"], "ambiguous")]
    n = len(rows)
    summary = {"flagged_items": len(flagged), "scenes": len(sub), "arm_rows": n, "stored_top_reproduced": sum(r["stored_top_reproduced"] for r in rows),
               "rows_changing_label": len(changed), "share_changing_label": round(len(changed) / n, 4), "ambiguous_rows": sum(r["full_word_label"] == "ambiguous" for r in rows),
               "changes_by_arm": {a: sum(1 for r in changed if r["arm"] == a) for a in ("none", *ARMS)},
               "changes_by_direction": {f"{r0} -> {r1}": sum(1 for r in changed if (r["stored_label"], r["full_word_label"]) == (r0, r1)) for r0 in ("A", "b", "other") for r1 in ("A", "b", "other")},
               "recompute": len(changed) / n > BAR}  # fmt: skip
    if summary["recompute"]:
        full = X.read_jsonl(src / "outcomes.jsonl")
        key = {(r["set"], r["scene"], r["reader"], r["arm"]): r for r in changed}
        new_rows = []
        for r in full:
            if r["layer"] != la:
                continue
            k = (r["set"], r["scene"], r["reader"], r["arm"])
            if k in key:
                lab = key[k]["full_word_label"]
                r = {
                    **r,
                    "switched": int(lab == "b"),
                    "role": lab,
                    "route": {"b": "switch", "A": "original"}.get(lab, "other"),
                }
            new_rows.append(r)
        res0 = Z.layer_result("z1p", [r for r in full if r["layer"] == la], X.N_BOOT)
        res1 = Z.layer_result("z1p", new_rows, X.N_BOOT)
        summary["numbers"] = {name: {"lookup_excess": r["lookup"]["excess"], "recall_excess": r["recall"]["excess"], "gap": r["gap"], "verdict": r["verdict"], "n": r["n"]}
                              for name, r in (("first_token", res0), ("full_word_for_flagged_rows", res1))}  # fmt: skip
    (out / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False, default=float) + "\n")
    print(json.dumps(summary, indent=1, ensure_ascii=False, default=float), flush=True)
    return out


if __name__ == "__main__":
    main()
