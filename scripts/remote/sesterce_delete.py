"""Delete one Sesterce GPU instance through the API, checked (Dan, 23 Oct: a box is deleted when its queue is empty and
everything is pulled; the API has no stop, only DELETE /gpu-cloud/instances/{id}). Runs on the Mac: the key SESTERCE_API
is read from .env and never printed or sent anywhere but the API.

  uv run python scripts/remote/sesterce_delete.py --ip 38.80.123.239 --gpu A100 --count 4 [--dry-run]

Deletes only if exactly one live instance has that ip, its gpuModel contains --gpu, its gpuCount is --count and its
status is active; anything else exits non-zero without deleting.
"""

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
API = "https://api.cloud.sesterce.com"


def key() -> str:
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith("SESTERCE_API="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit(".env has no SESTERCE_API")


def api(method: str, path: str) -> tuple[int, object]:
    # a User-Agent is required: Cloudflare in front of the API answers urllib's default one with 403
    headers = {"X-API-KEY": key(), "Accept": "application/json", "User-Agent": "curl/8.7.1"}
    with urllib.request.urlopen(urllib.request.Request(API + path, method=method, headers=headers), timeout=60) as r:
        body = r.read()
        return r.status, (json.loads(body) if body else None)


def match(items: object, ip: str, gpu: str, count: int) -> dict:
    """The one live instance with this ip, gpu model and count, active; else SystemExit (nothing deleted)."""
    if not isinstance(items, list):
        raise SystemExit("unexpected list response; not deleting anything")
    live = [it for it in items if it.get("ip") == ip and it.get("status") not in ("deleted", "deleting")]
    if len(live) != 1:
        raise SystemExit(f"{len(live)} live instances with ip {ip}; not deleting anything")
    it = live[0]
    if gpu.upper() not in str(it.get("gpuModel", "")).upper() or int(it.get("gpuCount", 0)) != count:
        raise SystemExit(f"instance {it.get('_id')} is not {count}x {gpu}; not deleting anything")
    if it.get("status") != "active":
        raise SystemExit(f"instance {it.get('_id')} status {it.get('status')}; not deleting anything")
    return it


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ip", required=True)
    ap.add_argument("--gpu", required=True, help="a substring of gpuModel, e.g. A100 or H200")
    ap.add_argument("--count", type=int, required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    _, items = api("GET", "/gpu-cloud/instances")
    it = match(items, a.ip, a.gpu, a.count)
    print(
        f"{time.strftime('%H:%M:%S')} match: {it['_id']} name={it.get('name')} {it.get('gpuCount')}x{it.get('gpuModel')}"
    )
    if a.dry_run:
        print("dry run: not deleting")
        return 0
    code, _ = api("DELETE", f"/gpu-cloud/instances/{it['_id']}")
    print(f"DELETE /gpu-cloud/instances/{it['_id']} -> {code}")
    return 0 if code == 204 else 1


if __name__ == "__main__":
    sys.exit(main())
