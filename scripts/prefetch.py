"""Download a pinned model snapshot and its lens files into the HF cache, retrying on HF rate limits.

    uv run python scripts/prefetch.py configs/models/qwen3.6-27b.yaml

Anonymous downloads hit `429 Too Many Requests` on large repos; an HF_TOKEN in .env raises the limit.
Partial files resume, so a retry only re-fetches what is missing.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import yaml
from huggingface_hub import hf_hub_download, snapshot_download
from huggingface_hub.errors import HfHubHTTPError

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


def main(path: str) -> None:
    m = yaml.safe_load(Path(path).read_text())
    with_retries(lambda: snapshot_download(m["name"], revision=m["revision"]), m["name"])
    print(f"   {m['name']}@{m['revision'][:8]} cached", flush=True)
    for name, lens in m.get("lenses", {}).items():
        repo = lens.get("repo", "neuronpedia/jacobian-lens")
        with_retries(lambda: hf_hub_download(repo, lens["filename"], revision=lens["revision"]), name)  # noqa: B023
        print(f"   lens {name}: {lens['filename']}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
