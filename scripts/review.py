"""The review dashboard (Dan 26 Oct ~13:30): open a claim, set a seed, read N random items from the per-item files
exactly as the model saw them, with automatic checks over the whole item set and hand marks logged to
review/marks.jsonl. docs/review_views.yaml is the single source (src/bridge_jspace/review/). CPU only, read-only on
results/; token ids are decoded with the pinned tokenizer.json files.

uv run python scripts/review.py serve --seed 7 --port 8001     # make review-serve SEED=7 [PORT=8001]
uv run python scripts/review.py export --seed 0 --n 10         # make review-export SEED=0 N=10 -> review/seed-0/
uv run python scripts/review.py pack                           # docs/verify_pack.md from the views file
"""

from __future__ import annotations

import argparse
import collections
import json
import subprocess
import sys
import time
import webbrowser
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace.review import checks as C
from bridge_jspace.review import items as I
from bridge_jspace.review import page as P
from bridge_jspace.review import recount as RC

REPO = I.REPO
MARKS = REPO / "review" / "marks.jsonl"
VERDICTS = ("consistent", "wrong", "unclear")


def commit() -> str:
    sha = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True
    ).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "src/bridge_jspace/review", "scripts/review.py",
                            "docs/review_views.yaml"], cwd=REPO, capture_output=True, text=True).stdout.strip()  # fmt: skip
    return sha + ("-dirty" if dirty else "")


@lru_cache(maxsize=32)
def stats(view_id: str) -> dict[str, dict]:
    """Per model: the automatic checks over the whole item set, and its size per reader."""
    out = {}
    for m in I.spec()["models"]:
        got = I.items(view_id, m)
        s = C.summary(got)
        s["n_reader"] = dict(collections.Counter(it["reader"] for it in got))
        out[m] = s
    return out


@lru_cache(maxsize=32)
def recount(view_id: str) -> list[dict]:
    return RC.recount(view_id)


def params_of(q: dict[str, str], v: dict) -> dict:
    p = {"view": v["id"], "seed": int(q.get("seed") or 0), "n": int(q.get("n") or 5), "mode": q.get("mode") or "uniform",
         "model": q.get("model") or "all", "reader": q.get("reader") or "all"}  # fmt: skip
    for k in ("condition", "s", "kind"):
        p[k] = q.get(k) or "all"
    p["out"], p["superseded"] = q.get("out") == "1", q.get("superseded") == "1"
    return p


def samples(v: dict, p: dict) -> dict[str, dict]:
    models = list(I.spec()["models"]) if p["model"] == "all" else [p["model"]]
    sections = ["set"] + (["out"] if p["out"] else []) + (["superseded"] if p["superseded"] else [])
    got: dict[str, dict] = {}
    for sec in sections:
        got[sec] = {}
        for m in models:
            pool = [it for it in I.items(v["id"], m, sec) if I.facets(it, p)]
            if sec == "superseded" and not pool:
                continue
            mode = p["mode"] if sec == "set" else "stratified"  # outside the set: every status shown with its count
            got[sec][m] = I.sample(pool, p["seed"], p["n"], mode, v["id"], m, sec)
    return got


def latest_marks() -> dict[str, dict]:
    out = {}
    if MARKS.exists():
        for line in MARKS.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["item"]] = r
    return out


def render_view(q: dict[str, str], server: bool, sha: str) -> str:
    v = I.view(q["view"])
    p = params_of(q, v)
    return P.view_page(
        v, p, samples(v, p), stats(v["id"]), server, sha, latest_marks() if server else {}, recount(v["id"])
    )


def render_index(server: bool, sha: str, seed: int, n: int) -> str:
    return P.index_page([(v, stats(v["id"]), recount(v["id"])) for v in I.phase1()], server, sha, seed, n)


class Handler(BaseHTTPRequestHandler):
    seed, n = 7, 5

    def send(self, body: str, ctype: str = "text/html; charset=utf-8", code: int = 200) -> None:
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        url = urlparse(self.path)
        q = {k: v[-1] for k, v in parse_qs(url.query).items()}
        try:
            if url.path == "/":
                self.send(render_index(True, commit(), self.seed, self.n))
            elif url.path == "/view" and q.get("view"):
                q.setdefault("seed", str(self.seed))
                self.send(render_view(q, True, commit()))
            elif url.path == "/marks.jsonl":
                self.send(MARKS.read_text() if MARKS.exists() else "", "application/json")
            else:
                self.send("not found", "text/plain", 404)
        except Exception as e:  # show the error in the page; the server keeps running
            self.send(f"<pre>{P.E(repr(e))}</pre>", code=500)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/mark":
            self.send("not found", "text/plain", 404)
            return
        d = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if d.get("verdict") not in VERDICTS or not d.get("item") or not d.get("view"):
            self.send("bad mark", "text/plain", 400)
            return
        row = {"view": d["view"], "item": d["item"], "seed": int(d.get("seed") or 0), "verdict": d["verdict"],
               "note": d.get("note", ""), "commit": commit(), "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}  # fmt: skip
        MARKS.parent.mkdir(exist_ok=True)
        with MARKS.open("a") as f:
            f.write(json.dumps(row) + "\n")
        self.send("ok", "text/plain")

    def log_message(self, *args) -> None:
        pass


def serve(seed: int, port: int, open_browser: bool) -> None:
    Handler.seed = seed
    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://localhost:{port}/"
    print(f"review dashboard on {url} (seed {seed}); marks -> {MARKS.relative_to(REPO)}; Ctrl-C stops")
    if open_browser:
        webbrowser.open(url)
    httpd.serve_forever()


def export(seed: int, n: int, out: Path | None = None) -> Path:
    out = out or REPO / "review" / f"seed-{seed}"
    out.mkdir(parents=True, exist_ok=True)
    sha = commit()
    (out / "index.html").write_text(render_index(False, sha, seed, n))
    for v in I.phase1():
        q = {"view": v["id"], "seed": str(seed), "n": str(n), **{k: str(x) for k, x in v.get("export", {}).items()}}
        (out / f"{v['id']}.html").write_text(render_view(q, False, sha))
    size = sum(f.stat().st_size for f in out.glob("*.html"))
    print(f"wrote {out}: {len(I.phase1()) + 1} pages, {size / 1e6:.1f} MB (seed {seed}, N = {n} per model)")
    return out


def pack(out: Path | None = None) -> Path:
    """docs/verify_pack.md from the views file: per view, its claim, runs and item set, the headline numbers recounted
    from the per-item files beside data.csv, and the automatic checks over the same items."""
    out = out or REPO / "docs" / "verify_pack.md"
    lines = ["# Verification pack", "",
             f"Generated by `uv run python scripts/review.py pack` from docs/review_views.yaml at {commit()}; the dashboard "
             "(`make review-serve`) reads the same file, so the two cannot drift. Each table is recounted from the runs' "
             "per-item files over the whole item set (no verdict file is read) and set beside figures/story/data.csv "
             "(2 decimals). Extra loss = (switches without the random part - switches without the part) / switches with "
             "the whole change; route share = the share of the lookup's items in a route (routes C0: switch / original / "
             "other). Read the items by hand: `make review-serve`, then the view's page (or `make review-export SEED=0`). "
             "The pack of 25 Oct is kept as docs/verify_pack_25oct.md.", ""]  # fmt: skip
    for v in I.phase1():
        rows = recount(v["id"])
        st = stats(v["id"])
        lines += [f"## {v['title']} (`{v['id']}`)", "", f"**Claim.** {v['claim'].strip()}", "", f"README: {v.get('readme', '')}.", "",
                  "Runs: " + "; ".join(f"{I.spec()['models'][m]['label']}: " + ", ".join(f"`{r}`" for r in rs)
                                       for m, rs in v["runs"].items()) + ".", "",
                  f"Item set: `{json.dumps(v['filters'])}`.", "",
                  f"Command: `uv run python scripts/review.py pack` (this table); items: `make review-serve`, view `{v['id']}`.", ""]  # fmt: skip
        if rows:
            lines += ["| model | quantity | n | recount | data.csv | key | |", "|---|---|---|---|---|---|---|"]
            lines += [f"| {I.spec()['models'][r['model']]['label']} | {r['quantity']} | {r['n']} | {r['value']:.4f} | {r['data']} | "
                      f"{r['key']} | {r['status']} |" for r in rows if r["status"] != "no source"]  # fmt: skip
            no_src = sum(r["status"] == "no source" for r in rows)
            lines += ["", f"{sum(r['status'] == 'match' for r in rows)} match, {sum(r['status'] == 'mismatch' for r in rows)} "
                      f"mismatch; {no_src} recounted numbers have no data.csv key (not listed)." if no_src else "", ""]  # fmt: skip
        fails = {m: s["fail"] for m, s in st.items() if s["fail"]}
        lines += [f"Automatic checks over {sum(s['n'] for s in st.values())} items: "
                  + (f"failures {json.dumps(fails)}." if fails else "no disagreement with the stored data."), ""]  # fmt: skip
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["serve", "export", "pack"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--port", type=int, default=8001)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    if a.stage == "serve":
        serve(a.seed, a.port, not a.no_open)
    elif a.stage == "pack":
        pack(a.out)
    else:
        export(a.seed, a.n, a.out)


if __name__ == "__main__":
    main()
