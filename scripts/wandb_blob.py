"""wandb_blob: the post-hoc W&B record of a job (Zach, 2026-10-22): {"config": {...}, "metrics": {...}} for
scripts/log_wandb_json.py on the VPS. Config: each result's manifest (run, why, git commit, model pin, lens, seeds,
conditions...) plus the box repo's HEAD. Metrics: the numeric leaves of each result's summary / scoring JSON, keyed
"<result>/<path>", capped at 400 per result.

python scripts/wandb_blob.py JOB RESULT_DIR_OR_JSON [...]   (paths under results/; prints the JSON)
"""

import json
import subprocess
import sys
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"


def leaves(x, prefix, out, cap):
    if len(out) >= cap:
        return
    if isinstance(x, bool):
        out[prefix] = int(x)
    elif isinstance(x, (int, float)):
        out[prefix] = x
    elif isinstance(x, dict):
        for k, v in x.items():
            leaves(v, f"{prefix}/{k}", out, cap)
    elif isinstance(x, list) and len(x) <= 8:
        for i, v in enumerate(x):
            leaves(v, f"{prefix}/{i}", out, cap)


def main(job, paths):
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=RES.parent).stdout.strip()
    config, metrics = {"job": job, "repo_head": head}, {}
    for p in paths:
        path = RES / p
        name = p.rstrip("/").replace("/", ":")
        if path.is_dir():
            man = path / "manifest.json"
            if man.exists():
                m = json.loads(man.read_text())
                config[name] = {k: v for k, v in m.items() if k not in ("doc",)}
            summ = path / "summary.json"
            src = json.loads(summ.read_text()) if summ.exists() else {}
        else:
            src = json.loads(path.read_text())
        part = {}
        leaves({k: v for k, v in src.items() if k not in ("per_text", "rows")}, name, part, 400)
        metrics.update(part)
    print(json.dumps({"config": config, "metrics": metrics}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
