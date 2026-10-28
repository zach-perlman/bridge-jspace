"""Download a pinned model snapshot and its lens files into the HF cache, retrying on HF rate limits.

    uv run python scripts/prefetch.py configs/models/qwen3.6-27b.yaml
    uv run python scripts/prefetch.py qwen3.5-9b      # a target pinned in bridge_jspace.pins (no YAML of its own)

Anonymous downloads hit `429 Too Many Requests` on large repos; an HF_TOKEN in .env raises the limit.
Partial files resume, so a retry only re-fetches what is missing. A target whose pinned lens is a local file
("local", path, sha256) gets that file placed at its path from the YAML's lens repo, sha-checked.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
import time
from pathlib import Path

import yaml
from huggingface_hub import hf_hub_download, snapshot_download
from huggingface_hub.errors import HfHubHTTPError

REPO = Path(__file__).resolve().parents[1]
RETRYABLE = (429, 500, 502, 503, 504)


def with_retries(fn, what: str, attempts: int = 12, base_s: float = 30.0):
    for i in range(1, attempts + 1):
        try:
            return fn()
        except HfHubHTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status not in RETRYABLE or i == attempts:
                raise
            wait = min(base_s * 2 ** (i - 1), 600)
            print(f"   {what}: HTTP {status}, retry {i}/{attempts - 1} in {wait:.0f}s", flush=True)
            time.sleep(wait)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()


def spec_of(arg: str) -> dict:
    """{name, revision, lenses: {name: {repo, filename, revision[, local, sha256]}}} from a model YAML, or from the
    pins of a target name (merged with configs/models/<target>.yaml when it exists, for the lens repos of local lenses)."""
    if arg.endswith((".yaml", ".yml")):
        return yaml.safe_load(Path(arg).read_text())
    from bridge_jspace import pins

    t = pins.TARGETS[arg]
    cfg = REPO / "configs" / "models" / f"{arg}.yaml"
    yml = yaml.safe_load(cfg.read_text()) if cfg.exists() else {}
    lenses = {}
    for name, (repo, filename, rev) in t.get("lenses", {}).items():
        if repo == "local":  # rev is the file's sha256; the download comes from the YAML's repo for this lens
            src = yml.get("lenses", {}).get(name)
            if (
                not src
            ):  # a lens fit here (e.g. the 27B's jpp_chat64): nothing to download, copy it from a box that has it
                print(
                    f"   lens {name}: local only ({filename}), no repo in configs/models/{arg}.yaml: skipped",
                    flush=True,
                )
                continue
            lenses[name] = {**src, "local": filename, "sha256": rev}
        else:
            lenses[name] = {"repo": repo, "filename": filename, "revision": rev}
    return {"name": t["repo"], "revision": t["revision"], "lenses": lenses}


def main(arg: str) -> None:
    m = spec_of(arg)
    with_retries(lambda: snapshot_download(m["name"], revision=m["revision"]), m["name"])
    print(f"   {m['name']}@{m['revision'][:8]} cached", flush=True)
    for name, lens in m.get("lenses", {}).items():
        repo = lens.get("repo", "neuronpedia/jacobian-lens")
        got = with_retries(lambda: hf_hub_download(repo, lens["filename"], revision=lens["revision"]), name)  # noqa: B023
        print(f"   lens {name}: {lens['filename']}", flush=True)
        if "local" in lens:  # the pinned path the code reads, sha-checked
            dst = REPO / lens["local"]
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(str(got), dst)
            assert sha256_of(dst) == lens["sha256"], f"{dst}: sha256 differs from the pin"
            print(f"   lens {name} placed at {lens['local']} (sha256 ok)", flush=True)


if __name__ == "__main__":
    for a in sys.argv[1:]:
        main(a)
