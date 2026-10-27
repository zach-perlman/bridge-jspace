"""x0_probe_lens (descriptive, after the data; Dan's plan step 5, 25 Oct ~23:00): the probe as an upper bound on what the
bridge's word holds, against what the lens reads. Per model at its fixed layer, on the fresh scenes with the locker
sentence before the pick: the linear probe's accuracy for the address (the locker sentence) and for the bridge's
identity, each against its best baseline (x0_probe v4); and how much of the single-change edit's J++ part, and of the
rest, lies in the address probe's subspace (x0_probe_patched's energy, k = 25 and 100). No identity-target
probe_patched run exists, so the identity row has no lens column. Writes results/x0_probe_lens/<UTC>/. UNVERIFIED.

uv run python scripts/x0_probe_lens.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_details as XD

OUT = pins.RESULTS_DIR / "x0_probe_lens"
TARGETS = {"locker sentence": "address (locker sentence)", "bridge identity": "bridge identity"}
NAMES = {"9b": "Qwen3.5-9B", "27b": "Qwen3.6-27B", "122b": "Qwen3.5-122B-A10B", "muse": "Muse Glimmer 30B"}


def ci(v: list[float]) -> str:
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def main() -> None:
    rows, lines = [], []
    for m, run in XD.PROBES_V4.items():
        path = sorted((pins.RESULTS_DIR / "x0_probe" / run).glob("probe-*/probe.json"))[-1]
        probe = {r["target"]: r for r in json.loads(path.read_text())["rows"]
                 if r["subset"] == "all" and r["stratum"] == "before"}  # fmt: skip
        patched = XD.latest_patched(XD.AMNESIC[m], "address")
        energy = json.loads(patched.read_text())["results"]["energy"]
        share = {
            k: energy[f"org + {part}, k = {k}"]["share_in_probe_subspace"] for part in ("J++ part",) for k in (25, 100)
        }
        rest = {k: energy[f"org + rest, k = {k}"]["share_in_probe_subspace"] for k in (25, 100)}
        layer = json.loads((path.parent.parent / "manifest.json").read_text()).get(
            "layer", XD.X.PREDICTED[XD.MODELS[m][0]]
        )
        for t, label in TARGETS.items():
            r = probe[t]
            base = r["best_baseline"]
            row = {"model": m, "layer": layer, "target": label, "n": r["n"], "classes": r["classes"], "probe": r["probe"],
                   "baseline": base, "baseline_acc": r[base] if isinstance(r[base], list) else [r[base]] * 3,
                   "probe_minus_best": r["probe_minus_best"], "source": str(path.relative_to(pins.REPO_ROOT))}  # fmt: skip
            if t == "locker sentence":
                row |= {"jpp_share_in_probe_k25": share[25], "jpp_share_in_probe_k100": share[100],
                        "rest_share_in_probe_k25": rest[25], "rest_share_in_probe_k100": rest[100],
                        "energy_source": str(patched.relative_to(pins.REPO_ROOT))}  # fmt: skip
                lens = (f"{100 * share[25]:.1f}% / {100 * share[100]:.1f}% | {100 * rest[25]:.1f}% / "
                        f"{100 * rest[100]:.1f}%")  # fmt: skip
            else:
                lens = "not run (no identity-target probe_patched) | -"
            rows.append(row)
            lines.append(f"| {NAMES[m]} (L{layer}) | {label} | {r['n']} | {r['classes']} | {ci(r['probe'])} | {base} "
                         f"{ci(row['baseline_acc'])} | {ci(r['probe_minus_best'])} | {lens} |")  # fmt: skip
    out = OUT / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out.mkdir(parents=True)
    (out / "probe_lens.json").write_text(json.dumps({"rows": rows}, indent=1) + "\n")
    md = ["# The probe's upper bound against the lens, at the bridge's word", "",
          "Descriptive, after the data (Dan's plan step 5). Fresh scenes, the locker sentence before the pick "
          "(x0_probe v4, subset all); probe accuracy with its 95% interval over bridge entities, against the best "
          "baseline the probe script reports. Lens columns: the share of the single-change edit's J++ part (k = 25 / 100) "
          "and of the rest that lies in the address probe's subspace (x0_probe_patched energy). UNVERIFIED.", "",
          "| model | target | n | classes | probe | best baseline | probe - baseline | J++ part in the probe's subspace "
          "(k = 25 / 100) | the rest in it (k = 25 / 100) |", "|---|---|---|---|---|---|---|---|---|", *lines]  # fmt: skip
    (out / "probe_lens.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    print(out)


if __name__ == "__main__":
    main()
