"""Exit 0 if a run's readers' gate missed (G1), 1 if it passed or the run has no gate file (Dan, 26 Oct: batch 38's
fallback, used by scripts/muse_step.sh).

Formats: x0_necessity / x0_replicate {"gate": {"chat": {"pass": ...}}}; x6_routes {"gate": {"C0": {...}, ...}} (missed
when no condition passed); x5_natural {"pass": ...}. Per-cell gates (x0b, x4) are partial by design and not checked.

python scripts/gate_missed.py results/x6_routes/<run>
"""

import json
import sys
from pathlib import Path


def missed(run_dir: Path) -> bool:
    f = run_dir / "gate.json"
    if not f.exists():
        return False
    d = json.loads(f.read_text())
    if "pass" in d:
        return not d["pass"]
    g = d.get("gate", {})
    if "chat" in g:
        return not g["chat"].get("pass")
    if g and all(k.startswith("C") for k in g):
        return not any(v.get("pass") for v in g.values())
    return False


if __name__ == "__main__":
    sys.exit(0 if missed(Path(sys.argv[1])) else 1)
