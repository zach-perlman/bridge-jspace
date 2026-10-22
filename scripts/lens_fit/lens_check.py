"""lens_check: every model's lens scored the same way (Zach, 2026-10-21, decided with Zach: the lens gates differed per
model, and the 27B's published lens was never scored by our own check). Held-out readout items of jpp_lens
(held-out:0, the items each model answers right, graded by scripts/lens_fit/jpp_grade.py), ranks from jpp_cli.py
evaluate at every fitted layer; pass@10 as jpp_lens defines it (an item's intermediates hit if their best rank over the
chosen layers is <= 10; macro = the mean over its five macro evals), for the model's J++ and for the logit lens, over
(a) every fitted layer, (b) seven layers at relative depths 1/8 ... 7/8 (the same number for every model; more layers
give more chances), (c) the C1 rule band. J++ minus logit is the comparable number across models: the item sets differ
by model. Descriptive. Run in the jpp_lens environment (its scoring code):

cd /workspace/ext/jpp_lens && uv run --no-sync python /workspace/bridge-jspace/scripts/lens_fit/lens_check.py
  (writes /workspace/bridge-jspace/results/lens_check/summary.md and .json; models without ranks yet are listed as such)
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from lens_evals.readout_evals.readout_eval_scoring import pass_at_k_over_layers

REPO = Path("/workspace/bridge-jspace")
RES = REPO / "results"
# model -> (rank files, J++ lens name (file stem), number of layers, fitted source layers, C1 rule band)
MODELS = {
    "Qwen3.6-27B (published J++)": ([RES / "lens_check/qwen3.6-27b/eval_ranks.csv"], "Qwen3.6-27B_jpp_lens", 64,
                                    range(0, 63), range(32, 41)),
    "Gemma 4 31B-it (our J++, 64 prompts)": ([RES / "lens_fit/gemma_it_full/eval_ranks.csv",
                                              RES / "lens_check/gemma-4-31b-it-full/eval_ranks_logit.csv"],
                                             "gemma-4-31B-it_jpp_lens", 60, range(0, 59), range(30, 39)),
    "Qwen3-32B (our J++, 32 prompts)": ([RES / "lens_fit/qwen3_32b/eval_ranks.csv",
                                         RES / "lens_check/qwen3-32b/eval_ranks_logit.csv"],
                                        "Qwen3-32B_jpp_lens", 64, range(0, 63), range(32, 41)),
    "Qwen3.5-9B (published J++)": ([RES / "lens_check/qwen3.5-9b/eval_ranks.csv"], "Qwen3.5-9B_jpp_lens", 32,
                                   range(0, 31), range(16, 21)),
}  # fmt: skip


def macro10(ranks: pd.DataFrame, lens: str, layers) -> float | None:
    sel = ranks[(ranks["lens"] == lens) & ranks["layer"].isin(list(layers))]
    if sel.empty:
        return None
    t = pass_at_k_over_layers(sel, [10])
    v = t[(t["eval"] == "macro") & (t["lens"] == lens)]["pass_at_k"]
    return None if v.empty or pd.isna(v.iloc[0]) else float(v.iloc[0])


def main() -> None:
    out, lines = {}, ["# Lens check: every model's lens scored the same way (scripts/lens_fit/lens_check.py)", "",
                      "Held-out macro pass@10 (jpp_lens's readout evals, items the model answers right). J++ / logit "
                      "lens / J++ minus logit.", "",
                      "| model | items | every fitted layer | 7 layers at 1/8-7/8 depth | C1 rule band |",
                      "|---|---|---|---|---|"]  # fmt: skip
    for name, (files, jpp, n, fitted, band) in MODELS.items():
        have = [f for f in files if f.exists()]
        if len(have) < len(files):
            lines.append(f"| {name} | not scored yet | | | |")
            continue
        ranks = pd.concat([pd.read_csv(f) for f in have], ignore_index=True)
        rel = sorted({int(n * k / 8 + 0.5) for k in range(1, 8)} & set(fitted))
        row, rec = [], {"relative_layers": rel, "band": [band.start, band.stop - 1]}
        for label, layers in (("all", fitted), ("relative7", rel), ("band", band)):
            j, lg = macro10(ranks, jpp, layers), macro10(ranks, "logit", layers)
            rec[label] = {"jpp": j, "logit": lg}
            row.append("-" if j is None or lg is None else f"{j:.3f} / {lg:.3f} / {j - lg:+.3f}")
        items = ranks[ranks["lens"] == jpp].groupby("eval")["item"].nunique().to_dict()
        rec["items_per_eval"] = items
        out[name] = rec
        lines.append(f"| {name} | {sum(items.values())} | " + " | ".join(row) + " |")
    lines += ["", f"Relative-depth layers: {json.dumps({k: v['relative_layers'] for k, v in out.items()})}"]
    (RES / "lens_check").mkdir(parents=True, exist_ok=True)
    (RES / "lens_check" / "summary.json").write_text(json.dumps(out, indent=2) + "\n")
    (RES / "lens_check" / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
