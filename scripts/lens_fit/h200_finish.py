"""After the Qwen3-32B J++ fit on the 2x H200 box: save, upload, terminate (Dan, 23 Oct ~00:30). Runs on the Mac, so the
Sesterce API key and the HF token never reach the box's disk:

  uv run python scripts/lens_fit/h200_finish.py --dry-run   # list the instances, show which one would be deleted
  uv run python scripts/lens_fit/h200_finish.py             # wait, save, upload, terminate

1. Wait until ~/work/fit32b/status.json on the box is terminal (DONE, FAIL, ABORT_*), or until the backstop (4 h 30 min
   after the fit started; the launcher's own limit is 4 h).
2. Save: the fp16 export and the fp32 lens to cache/qwen3-32b/lenses/jpp/, the logs, status and evaluation CSVs to
   results/lens_fit/qwen3_32b_jpp_<stamp>/; the export's sha256 must match status.json. If saving fails three times,
   stop WITHOUT terminating (an idle box costs less than a lost fit).
3. If DONE: a model card like Zach's (recipe, limits, file layout, held-out pass@10 against the pooled lens) and a
   public upload to Dan's Hub account (hf_upload.py on the box; HF_TOKEN from the Mac's .env, streamed over ssh stdin).
   A failed upload does not block termination: the Mac keeps the file.
4. Terminate through the Sesterce API (DELETE /gpu-cloud/instances/{id}, key SESTERCE_API from .env): the one instance
   whose ip is the box's, checked to be active and 2x H200; any other match count or shape aborts without deleting.
5. Copy the export to the A100 box's shared cache (~/bridge-jspace/cache/qwen3-32b/lenses/jpp/) for the J++ reruns.
"""

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HOST, IP = "sesterce-h200x2", "95.133.253.173"
A100 = "sesterce-a100x4"
FIT = "work/fit32b"  # relative to the box user's home
LENS_NAME = "Qwen3-32B_jpp_lens.pt"
HF_REPO = "Qwen3-32B-jpp-lens"
API = "https://api.cloud.sesterce.com"
TERMINAL = ("DONE", "FAIL", "ABORT_TIME", "ABORT_SLOW", "ABORT_OOM")
BACKSTOP_S = 4.5 * 3600
LENS_DIR = REPO / "cache" / "qwen3-32b" / "lenses" / "jpp"


def log(msg: str) -> None:
    print(f"{datetime.now().strftime('%H:%M:%S')} {msg}", flush=True)


def env_value(key: str) -> str:
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit(f".env has no {key}")


def ssh(cmd: str, stdin: str | None = None, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(["ssh", "-o", "ConnectTimeout=20", HOST, cmd], input=stdin, capture_output=True, text=True,
                          timeout=timeout)  # fmt: skip


def status() -> dict | None:
    try:
        r = ssh(f"cat ~/{FIT}/status.json")
        return json.loads(r.stdout) if r.returncode == 0 else None
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def wait() -> dict:
    while True:
        s = status()
        if s and s.get("state") in TERMINAL:
            return s
        if s:
            started = datetime.strptime(s["started"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            if (datetime.now(UTC) - started).total_seconds() > BACKSTOP_S:
                log(f"backstop: state {s.get('state')} after {BACKSTOP_S / 3600} h; saving and terminating")
                return {**s, "state": "BACKSTOP"}
        time.sleep(120)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def save(s: dict, out: Path) -> bool:
    out.mkdir(parents=True, exist_ok=True)
    LENS_DIR.mkdir(parents=True, exist_ok=True)
    small = ["--include=*.log", "--include=*.json", "--include=*.csv", "--exclude=*"]
    for attempt in range(3):
        a = subprocess.run(["rsync", "-a", *small, f"{HOST}:{FIT}/", f"{out}/"], check=False)
        b = subprocess.run(["rsync", "-a", "--include=Qwen3-32B_jpp_lens*", "--exclude=*", f"{HOST}:{FIT}/",
                            f"{LENS_DIR}/raw/"], check=False)  # fmt: skip
        c = 0
        if s["state"] == "DONE":
            c = subprocess.run(
                ["rsync", "-a", f"{HOST}:{FIT}/export/{LENS_NAME}", f"{LENS_DIR}/"], check=False
            ).returncode
        if a.returncode == b.returncode == c == 0:
            break
        log(f"save attempt {attempt + 1} failed ({a.returncode}, {b.returncode}, {c}); retrying")
        time.sleep(60)
    else:
        return False
    if s["state"] == "DONE":
        got = sha256(LENS_DIR / LENS_NAME)
        if got != s["sha256"]:
            log(f"sha256 mismatch: {got} vs {s['sha256']}")
            return False
        log(f"saved {LENS_DIR / LENS_NAME} (sha256 {got}) and the fit's logs to {out}")
    return True


def pass10(out: Path) -> tuple[list[str], dict[str, dict[str, float]]]:
    """eval -> lens -> pass@10 from the recipe's evaluate table (eval_ranks_pass_at_k.csv), item-weighted rows only
    (the table also has pair-weighted rows, which would otherwise overwrite them; Zach's cards are item-weighted)."""
    table: dict[str, dict[str, float]] = {}
    lenses: list[str] = []
    with open(out / "eval_ranks_pass_at_k.csv") as f:
        for r in csv.DictReader(f):
            if r.get("weighting", "item") != "item":
                continue
            if int(float(r["k"])) == 10:
                table.setdefault(r["eval"], {})[r["lens"]] = float(r["pass_at_k"])
                lenses += [r["lens"]] if r["lens"] not in lenses else []
    return lenses, table


def card(s: dict, out: Path) -> str:
    layers = s["layers"].split(",")
    try:
        lenses, table = pass10(out)
        evals = [e for e in table if e != "macro"] + (["macro"] if "macro" in table else [])
        rows = [f"| {'**macro**' if e == 'macro' else e} | " + " | ".join(
            f"{'**' if e == 'macro' else ''}{table[e].get(la, float('nan')):.2f}{'**' if e == 'macro' else ''}"
            for la in lenses) + " |" for e in evals]  # fmt: skip
        evaluation = ("pass@10 on the recipe's held-out items (`evaluate --items held-out:0`), averaged within each item "
                      "first (`pass_at_k_over_layers`), against the pooled lens fit in the same run:\n\n"
                      f"| eval | {' | '.join(lenses)} |\n|---|{'---|' * len(lenses)}\n" + "\n".join(rows))  # fmt: skip
    except (OSError, KeyError, ValueError) as e:
        evaluation = f"The evaluation table could not be read ({type(e).__name__}); see the fit's logs."
    return f"""---
license: apache-2.0
base_model: Qwen/Qwen3-32B
tags:
  - interpretability
  - jacobian-lens
  - logit-lens
---

# J++ lens for Qwen3-32B (source layers {layers[0]}-{layers[-1]})

A J++ (Jacobian) lens for [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B) at revision
`9216db5781bf21249d130ec9da846c4624c16137`, fit at source layers {layers[0]}-{layers[-1]}. The final block (layer 63) is
the target.

The published lens for this model ([neuronpedia/jacobian-lens](https://huggingface.co/neuronpedia/jacobian-lens),
`qwen3-32b/jlens`) is a plain J-lens; this is a J++ fit with the published recipe on 64 prompts.

## Limitations (read these first)

- **Not every layer.** Only source layers {layers[0]}-{layers[-1]} ({len(layers)} of 63) have a J. Read other layers with
  another lens.
- **Fit in two shards.** The 64 prompts were fit as 2 shards x 32 prompts (one per GPU) with one shared router (seed 0,
  fit once on all 64 prompts), then merged with the recipe's `merge-experts`. On Qwen3.5-0.8B the same procedure (2 x 2
  prompts vs 1 x 4) gave identical experts and pooled lens (max relative difference 0).
- **One fit, one seed.** No second fit or seed has been compared.

## Recipe

[safety-research/jpp_lens](https://github.com/safety-research/jpp_lens) @ `93f02cd`, unpatched:

- router: 64 WikiText prompts, seed 0
- J++ fit: 64 WikiText prompts x 128 tokens (2 shards x 32); the first 16 positions are skipped
- target = the final block; LRP rules (rlens); 8 experts; Jacobian rows per pass {s.get("rows", 10)}
- readout weights fit on the `fit:0` items, graded on this model

## File

`{LENS_NAME}`, sha256 `{s.get("sha256")}`

A `torch.save` dict in the same layout as neuronpedia's published lenses:

```python
{{
  "J": {{layer: Tensor[d, d] fp16, ...}},  # layers {layers[0]}..{layers[-1]}, d = d_model
  "source_layers": [{layers[0]}, ..., {layers[-1]}],
  "d_model": int,
  "n_prompts": 64,
  "provenance": {{...}},  # source config and fit note
}}
```

To read out the residual stream `h` at `layer`, map it to the final layer and then apply the model's final norm and
unembedding:

```python
lens = torch.load("{LENS_NAME}", map_location="cpu", weights_only=True)
h_final = h.float() @ lens["J"][layer].float().T
logits = lm_head(final_norm(h_final))  # the model's final RMSNorm, then lm_head
```

The jacobians were cast to fp16 for export; each layer's relative (Frobenius) error from the cast was printed at
export time.

## Evaluation (held-out items)

{evaluation}

One fit (seed 0) evaluated once; no intervals.

## Provenance

{s.get("note", "")}. Fit for the bridge-jspace project (Dan Orel, MATS).
"""


def upload(s: dict, out: Path) -> str | None:
    card_path = out / "README_card.md"
    card_path.write_text(card(s, out))
    if subprocess.run(["rsync", "-a", str(card_path), f"{HOST}:{FIT}/README_card.md"], check=False).returncode:
        log("could not copy the model card to the box; upload skipped")
        return None
    cmd = (f"read -r T; HF_TOKEN=$T ~/work/jpp_lens/.venv/bin/python ~/work/bridge-jspace/scripts/lens_fit/hf_upload.py "
           f"--repo {HF_REPO} --file ~/{FIT}/export/{LENS_NAME} --sha256 {s['sha256']} --note x "
           f"--card ~/{FIT}/README_card.md --public")  # fmt: skip
    try:
        r = ssh(cmd, stdin=env_value("HF_TOKEN") + "\n", timeout=3600)
    except subprocess.TimeoutExpired:
        log("HF upload timed out; the Mac has the file")
        return None
    (out / "hf_upload.txt").write_text(r.stdout[-2000:] + r.stderr[-2000:])
    log(f"HF upload exit {r.returncode}: {r.stdout.strip()[-300:]}")
    return r.stdout.strip() if r.returncode == 0 else None


def api(method: str, path: str) -> tuple[int, object]:
    # A User-Agent is required: Cloudflare in front of the API answers urllib's default one with 403.
    headers = {"X-API-KEY": env_value("SESTERCE_API"), "Accept": "application/json", "User-Agent": "curl/8.7.1"}
    req = urllib.request.Request(API + path, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read()
        return resp.status, (json.loads(body) if body else None)


def the_instance() -> dict:
    """The one live instance with the box's ip, 2x H200 and active; anything else exits without deleting (explicit
    checks, not asserts, so python -O cannot drop them)."""
    _, items = api("GET", "/gpu-cloud/instances")
    if not isinstance(items, list):
        raise SystemExit(f"unexpected list response: {type(items).__name__}; not deleting anything")
    for it in items:
        log(f"instance {it.get('_id')} name={it.get('name')} ip={it.get('ip')} gpu={it.get('gpuCount')}x"
            f"{it.get('gpuModel')} status={it.get('status')}")  # fmt: skip
    match = [it for it in items if it.get("ip") == IP and it.get("status") not in ("deleted", "deleting")]
    if len(match) != 1:
        raise SystemExit(f"{len(match)} live instances with ip {IP}; not deleting anything")
    it = match[0]
    if "H200" not in str(it.get("gpuModel", "")).upper() or int(it.get("gpuCount", 0)) != 2:
        raise SystemExit(f"instance {it.get('_id')} is not 2x H200; not deleting anything")
    if it.get("status") != "active":
        raise SystemExit(f"instance {it.get('_id')} status {it.get('status')}; not deleting anything")
    return it


def terminate() -> bool:
    it = the_instance()
    code, _ = api("DELETE", f"/gpu-cloud/instances/{it['_id']}")
    log(f"DELETE /gpu-cloud/instances/{it['_id']} -> {code}")
    time.sleep(30)
    try:
        _, after = api("GET", f"/gpu-cloud/instances/{it['_id']}")
        log(f"after: status={after.get('status') if isinstance(after, dict) else after}")
    except urllib.error.HTTPError as e:  # 404 after a DELETE = the instance is gone (23 Oct: this was read as a failure)
        log(f"after: GET -> {e.code} ({'gone: deleted' if e.code == 404 else 'unexpected'})")
    return code == 204


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="list the instances and the match; change nothing")
    ap.add_argument(
        "--no-terminate",
        action="store_true",
        help="save, upload and copy the lens, but keep the box (Dan, 23 Oct ~00:35: the 122B runs next)",
    )
    ap.add_argument("--terminate-only", action="store_true",
                    help="only the checked DELETE of the box (the 122B launcher's TERMINATE_CMD)")  # fmt: skip
    a = ap.parse_args()
    if a.terminate_only:
        return 0 if terminate() else 1
    if a.dry_run:
        it = the_instance()
        log(f"would wait for {FIT}/status.json, save, upload, then DELETE instance {it['_id']} ({it.get('name')})")
        s = status()
        log(f"fit now: {s.get('state') if s else 'unreadable'} at {s.get('at') if s else '-'}")
        return 0
    s = wait()
    log(f"fit ended: {s['state']} at {s.get('at')}")
    out = (
        REPO / "results" / "lens_fit" / "qwen3_32b_jpp64"
    )  # the folder scripts/lens_table.py reads for our 64-prompt fit
    if out.exists():
        out = out.with_name(f"qwen3_32b_jpp64_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    if not save(s, out):
        log("SAVE FAILED: not terminating; the box keeps running")
        return 2
    if s["state"] == "DONE":
        upload(s, out)
    if a.no_terminate:
        ok = False
        log("not terminating (--no-terminate): the 122B runs on this box next; its launcher deletes it")
    else:
        ok = terminate()
    if s["state"] == "DONE":
        dst = "bridge-jspace/cache/qwen3-32b/lenses/jpp/"
        subprocess.run(["ssh", A100, f"mkdir -p ~/{dst}"], check=False)
        rc = subprocess.run(["rsync", "-a", str(LENS_DIR / LENS_NAME), f"{A100}:{dst}"], check=False).returncode
        log(f"copied the export to {A100}:~/{dst} (exit {rc})")
    log(f"finished: fit {s['state']}, terminated {ok}")
    return 0 if ok and s["state"] == "DONE" else 1


if __name__ == "__main__":
    sys.exit(main())
