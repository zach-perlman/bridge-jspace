"""Finish the Qwen3-32B J++ fit's export by hand on the H200 box (23 Oct ~01:50): the launcher (h200_fit.py) passed the
provenance note positionally, but export_jpp_lens.py requires --note, so the fit stopped as FAIL at its last step after
grade, readout weights and the held-out evaluation had all exited 0. This runs that one step with --note, computes the
export's sha256 and records it in status.json as a new step (the launcher's failed export step stays in the history),
with state DONE so the Mac finisher can publish the lens. Run on the box with the recipe env:

  ~/work/jpp_lens/.venv/bin/python ~/work/bridge-jspace/scripts/lens_fit/h200_export_fix.py
"""

import hashlib
import json
import subprocess
import time
from pathlib import Path

W = Path.home() / "work"
OUT = W / "fit32b"
LENS, EXPORT = OUT / "Qwen3-32B_jpp_lens.pt", OUT / "export" / "Qwen3-32B_jpp_lens.pt"
NOTE = ("J++ for Qwen/Qwen3-32B: safety-research/jpp_lens@93f02cd, 64 WikiText prompts x 128 tokens (2 shards x 32, one "
        "router, seed 0), skip 16, target = the last block, rlens LRP, 8 experts, source layers 16-51; fit 2026-10-22 on "
        "2x H200")  # fmt: skip

status = json.loads((OUT / "status.json").read_text())
assert status["state"] == "FAIL" and status.get("at") == "export", f"unexpected state {status.get('state')} at {status.get('at')}"
assert all(s.get("exit") == 0 for s in status["steps"] if s.get("step") in ("grade", "fit_weights", "evaluate")), "an earlier step failed"
EXPORT.parent.mkdir(exist_ok=True)
t = time.time()
with open(OUT / "export_by_hand.log", "w") as log:
    rc = subprocess.run([str(W / "jpp_lens/.venv/bin/python"), str(W / "bridge-jspace/scripts/lens_fit/export_jpp_lens.py"),
                         str(LENS), str(EXPORT), "--note", NOTE], stdout=log, stderr=subprocess.STDOUT).returncode  # fmt: skip
status["steps"].append({"step": "export (by hand: the launcher passed --note positionally)", "seconds": round(time.time() - t), "exit": rc})
if rc:
    status.update(state="FAIL", at="export (by hand)")
else:
    h = hashlib.sha256()
    with open(EXPORT, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    status.update(state="DONE", at="export (by hand)", lens=str(EXPORT), sha256=h.hexdigest(), note=NOTE)
(OUT / "status.json").write_text(json.dumps(status, indent=1) + "\n")
print(status["state"], status.get("sha256", ""), f"export exit {rc}")
