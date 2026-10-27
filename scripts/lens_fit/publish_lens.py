"""Publish a J++ lens fit on the A100 box (Dan, 23 Oct): hash, save, cache, model card, public upload, pins block.
Generalised from h200_finish.py's card() and upload(). Runs on the Mac, so the HF token stays in the Mac's .env and
reaches the box only through ssh stdin (hf_upload.py's `read -r T` pattern): never the box's disk, never a log.

  uv run python scripts/lens_fit/publish_lens.py --dry-run ARGS   # every step with read-only checks; changes nothing
  uv run python scripts/lens_fit/publish_lens.py --wait ARGS      # poll the jobq job every 5 min, then publish

1. sha256 of --export on the box; it must match what the job printed (sha256sum, or the export's JSON line).
2. The fit's small files (everything fit_jpp.sh writes under --fit-dir as *.json, *.csv, *.log, *.txt: the recipe's
   *_stamp.json, eval_ranks.csv, eval_ranks_pass_at_k.csv, model_correctness.csv, ...) and, with --job, the job's log
   (~/jobq/runs/<job>/log.txt: the fit's stdout) and record to results/lens_fit/<fit-dir name>_<stamp>/.
3. --export copied into the box's shared cache ~/bridge-jspace/<cache-path> (cp) and to <cache-path> on the Mac
   (rsync), sha256 checked on both. An existing copy with another sha256 stops the run (lens files are written once).
4. A public model card (README_card.md: limitations first; recipe, counts and dates read from the fit's stamps and the
   job record; held-out pass@10 against the pooled lens from eval_ranks_pass_at_k.csv), then the cache copy uploaded
   with hf_upload.py, run on the box in the recipe's venv; the sha256 the Hub reports for the upload is checked.
5. The pins block for src/bridge_jspace/pins.py, printed and saved with the results, not written into pins.py.

A failed job is not published unless --job-failed-ok is given (for a fit whose export was made by hand afterwards);
--wait prints the export command when the job failed with the fit and its evaluation on disk but no export.

OLMo-3-7B-Instruct (jobq olmo3_7b_instruct_jpp_fit):
  uv run python scripts/lens_fit/publish_lens.py --wait --job olmo3_7b_instruct_jpp_fit \
    --fit-dir /ephemeral/lens_fit/olmo3_7b_instruct_jpp \
    --export /ephemeral/lens_fit/olmo3_7b_instruct_jpp/export/Olmo-3-7B-Instruct_jpp_lens_fp16.pt \
    --hf-model allenai/Olmo-3-7B-Instruct --revision 6e5971d9eba42665f5bd5a0fcf047f299ce1dccc --layers 0-30 \
    --hf-repo Olmo-3-7B-Instruct-jpp-lens \
    --cache-path cache/olmo-3-7b-instruct/lenses/jpp/Olmo-3-7B-Instruct_jpp_lens.pt --note "J++ for ..."
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import re
import shlex
import subprocess
import sys
import tempfile
import textwrap
import time
from datetime import datetime
from pathlib import Path

from bridge_jspace import pins

REPO = Path(__file__).resolve().parents[2]
BOX_REPO = "bridge-jspace"  # the box's working copy (jobq's main_repo), relative to the box user's home
JOB_STATES = ("pending", "running", "done", "failed", "cancelled")
POLL_S = 300
SMALL = ["--include=*/", "--include=*.json", "--include=*.csv", "--include=*.log", "--include=*.txt", "--exclude=*"]
PINS_COMMENT = (
    "Primary lens (Dan, 23 Oct ~00:30): ours, the published recipe on 64 prompts; Zach's fit reported alongside when "
    "shared; no silent switch"
)


class CardError(Exception):
    """The card would have to guess a fact (a stamp or table is missing or disagrees); nothing is uploaded."""


def log(msg: str) -> None:
    print(f"{datetime.now().strftime('%H:%M:%S')} {msg}", flush=True)


def env_value(key: str) -> str | None:
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith(f"{key}="):
            return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    return None


def ssh(host: str, cmd: str, stdin: str | None = None, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(["ssh", "-o", "ConnectTimeout=20", host, cmd], input=stdin, capture_output=True, text=True,
                          timeout=timeout)  # fmt: skip


def rsync(*args: str) -> int:
    return subprocess.run(["rsync", "-a", *args], check=False).returncode


def q(s: str) -> str:
    return shlex.quote(s)


def parse_layers(text: str) -> list[int]:
    """'0-30' or '0,3,6' (or a mix) -> sorted layers."""
    out: set[int] = set()
    for part in text.split(","):
        lo, _, hi = part.strip().partition("-")
        out.update(range(int(lo), int(hi) + 1) if hi else [int(lo)])
    return sorted(out)


def layers_text(layers: list[int]) -> str:
    steps = {b - a for a, b in itertools.pairwise(layers)}
    if len(layers) > 2 and steps == {1}:
        return f"{layers[0]}-{layers[-1]}"
    if len(layers) > 3 and len(steps) == 1:
        return f"{layers[0]}, {layers[1]}, ..., {layers[-1]}"
    return ", ".join(map(str, layers))


def base_target(a: argparse.Namespace) -> tuple[str, dict]:
    """The pins target with this model's weights, whose repo / revision / n_layers / norm_gain / bos the new one copies."""
    keys = [a.base_target] if a.base_target else [
        k for k, t in pins.TARGETS.items() if (t["repo"], t["revision"]) == (a.hf_model, a.revision)]  # fmt: skip
    if len(keys) != 1 or keys[0] not in pins.TARGETS:
        raise SystemExit(f"pins targets for {a.hf_model}@{a.revision}: {keys}; pass one with --base-target")
    t = pins.TARGETS[keys[0]]
    if (t["repo"], t["revision"]) != (a.hf_model, a.revision):
        raise SystemExit(f"pins {keys[0]!r} is {t['repo']}@{t['revision']}, not {a.hf_model}@{a.revision}")
    return keys[0], t


# ---------------------------------------------------------------- the box


def job_state(host: str, job: str) -> tuple[str, str] | None:
    """(state, record path under ~/jobq) of the job's newest record, ("missing", "") if it has none, None if the box
    cannot be reached."""
    globs = " ".join(f"{s}/*_{job}.json archive/{s}/*_{job}.json" for s in JOB_STATES)
    try:
        r = ssh(host, f"cd ~/jobq && ls -1d {globs} 2>/dev/null")
    except subprocess.TimeoutExpired:
        return None
    if r.returncode == 255:
        return None
    recs = [p for p in r.stdout.split() if Path(p).name.split("_", 1)[-1] == f"{job}.json"]  # exact id, not a prefix
    if not recs:
        return "missing", ""
    newest = max(recs, key=lambda p: Path(p).name)  # names start with the enqueue time
    parts = Path(newest).parts
    return (parts[1] if parts[0] == "archive" else parts[0]), newest


def box_file(host: str, path: str) -> tuple[int, str] | None:
    """(size, sha256) of a file on the box (a path relative to the box user's home or absolute); None if absent."""
    r = ssh(host, f"test -f {q(path)} && stat -c %s {q(path)} && sha256sum {q(path)}", timeout=1800)
    if r.returncode == 255:
        raise SystemExit(f"ssh {host} failed: {r.stderr.strip()[-300:]}")
    if r.returncode != 0:
        return None
    size, sha = r.stdout.split()[:2]
    return int(size), sha


def box_exists(host: str, path: str) -> bool:
    return ssh(host, f"test -e {q(path)}").returncode == 0


def recipe_state(a: argparse.Namespace) -> tuple[str, bool]:
    """(HEAD, no local changes to tracked files) of the recipe checkout on the box; --no-optional-locks: read only."""
    r = ssh(a.host, f"git -C {q(a.recipe_dir)} rev-parse HEAD && git -C {q(a.recipe_dir)} --no-optional-locks status "
                    "--porcelain --untracked-files=no")  # fmt: skip
    lines = r.stdout.splitlines()
    return (lines[0] if r.returncode == 0 and lines else "?"), (r.returncode == 0 and len(lines) == 1)


def export_cmd(a: argparse.Namespace) -> str:
    """The export the job runs after the fit, as one ssh command (for a fit whose job failed before exporting)."""
    src, out_dir = f"{a.fit_dir}/{a.hf_model.split('/')[-1]}_jpp_lens.pt", str(Path(a.export).parent)
    remote = (f"mkdir -p {q(out_dir)} && {q(a.venv + '/bin/python')} {BOX_REPO}/scripts/lens_fit/export_jpp_lens.py "
              f"{q(src)} {q(a.export)} --note {q(a.note)} | tee {q(out_dir + '/export_line.json')}")  # fmt: skip
    return f"ssh {a.host} {q(remote)}"


def wait_for(a: argparse.Namespace) -> tuple[str, str]:
    while True:
        st = job_state(a.host, a.job)
        if st is None:
            log(f"{a.host} unreachable; next poll in {POLL_S // 60} min")
        else:
            log(f"job {a.job}: {st[0]} ({st[1] or 'no record'})")
            if st[0] == "done":
                return st
            if st[0] == "missing":
                raise SystemExit(f"job {a.job} has no record on {a.host}")
            if st[0] in ("failed", "cancelled"):
                fit_lens = f"{a.fit_dir}/{a.hf_model.split('/')[-1]}_jpp_lens.pt"
                evaluated = box_exists(a.host, f"{a.fit_dir}/eval_ranks_pass_at_k.csv")
                if (
                    st[0] == "failed"
                    and evaluated
                    and box_exists(a.host, fit_lens)
                    and not box_exists(a.host, a.export)
                ):
                    log("the fit and its evaluation are on disk but not the export; to export by hand:\n  "
                        f"{export_cmd(a)}\nthen rerun this without --wait, with --job-failed-ok")  # fmt: skip
                raise SystemExit(f"job {a.job} {st[0]}; nothing published")
        time.sleep(POLL_S)


# ---------------------------------------------------------------- saving and copying


def save_small(a: argparse.Namespace, out: Path, rec_path: str | None) -> None:
    out.mkdir(parents=True)  # a new folder per run: results are never overwritten
    copies = [(["-m", *SMALL], f"{a.host}:{a.fit_dir}/", f"{out}/")]
    if rec_path:
        copies += [([], f"{a.host}:jobq/runs/{a.job}/log.txt", str(out / "job_log.txt")),
                   ([], f"{a.host}:jobq/{rec_path}", str(out / "job.json"))]  # fmt: skip
    for extra, src, dst in copies:
        for attempt in range(3):
            if rsync(*extra, src, dst) == 0:
                break
            log(f"copy {src} attempt {attempt + 1} failed; retrying in 1 min")
            time.sleep(60)
        else:
            raise SystemExit(f"could not copy {src}")
    n = sum(1 for p in out.rglob("*") if p.is_file())
    log(
        f"   saved {n} files (the fit's stamps, CSVs and logs) to {out.relative_to(REPO) if out.is_relative_to(REPO) else out}"
    )


def export_line(out: Path, export: str) -> dict:
    """The JSON line export_jpp_lens.py printed for `export` (layers, d, max_rel_err_fp16, sha256), from the job's log
    or a saved file (export_line.json of a hand-made export); {} if none."""
    for path in sorted(out.rglob("*")):
        if path.is_file() and path.suffix in (".txt", ".json", ".log"):
            for line in path.read_text(errors="replace").splitlines():
                if line.startswith('{"out": '):
                    try:
                        d = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if d.get("out") == export:
                        return d
    return {}


def printed_sha(out: Path, export: str) -> str | None:
    """The sha256 the job printed for the export (its sha256sum line, else the export's JSON line)."""
    log_path = out / "job_log.txt"
    if log_path.exists():
        hits = re.findall(rf"^([0-9a-f]{{64}})\s+{re.escape(export)}$", log_path.read_text(errors="replace"), re.M)
        if hits:
            return hits[-1]
    return export_line(out, export).get("sha256")


def cache_copies(a: argparse.Namespace, sha: str) -> None:
    box_dst = f"{BOX_REPO}/{a.cache_path}"
    have = box_file(a.host, box_dst)
    if have is None:
        r = ssh(a.host, f"mkdir -p {q(str(Path(box_dst).parent))} && cp -n {q(a.export)} {q(box_dst)}", timeout=1800)
        if r.returncode:
            raise SystemExit(f"cp to {a.host}:~/{box_dst} failed: {r.stderr.strip()[-300:]}")
        have = box_file(a.host, box_dst)
    if have is None or have[1] != sha:
        raise SystemExit(f"{a.host}:~/{box_dst} sha256 {have and have[1]} != the export's {sha}; stopping")
    mac = REPO / a.cache_path
    if not mac.exists():
        mac.parent.mkdir(parents=True, exist_ok=True)
        if rsync(f"{a.host}:{a.export}", str(mac)):
            raise SystemExit(f"rsync of the export to {mac} failed")
    got = pins.sha256_file(mac)
    if got != sha:
        raise SystemExit(f"{mac} sha256 {got} != the export's {sha}; stopping")
    log(f"3. the export is in {a.host}:~/{box_dst} and {a.cache_path} on the Mac; sha256 {sha} on both")


# ---------------------------------------------------------------- the card


def stamp(out: Path, pattern: str) -> dict:
    hits = sorted(out.rglob(pattern))
    if not hits:
        raise CardError(f"no {pattern} among the fit's files")
    return json.loads(hits[0].read_text())


def pass_table(out: Path, k: int = 10, weighting: str = "item") -> tuple[list[str], dict[str, dict[str, float]]]:
    """eval -> lens -> pass@k from the recipe's evaluate table; item-weighted rows only (the file also has "pair" rows,
    which would otherwise overwrite them)."""
    table: dict[str, dict[str, float]] = {}
    lenses: list[str] = []
    with open(out / "eval_ranks_pass_at_k.csv") as f:
        for r in csv.DictReader(f):
            if int(float(r["k"])) == k and r["weighting"] == weighting:
                table.setdefault(r["eval"], {})[r["lens"]] = float(r["pass_at_k"])
                lenses += [r["lens"]] if r["lens"] not in lenses else []
    return lenses, table


def items_per_eval(out: Path, lens: str) -> dict[str, int]:
    seen: dict[str, set[str]] = {}
    with open(out / "eval_ranks.csv") as f:
        for r in csv.DictReader(f):
            if r["lens"] == lens:
                seen.setdefault(r["eval"], set()).add(r["item"])
    return {e: len(s) for e, s in seen.items()}


def evaluation(out: Path, ours: str) -> str:
    try:
        lenses, table = pass_table(out)
        n = items_per_eval(out, ours)
    except (OSError, KeyError, ValueError) as e:
        raise CardError(f"the evaluation tables could not be read ({type(e).__name__}: {e})") from e
    if ours not in lenses or "pooled_lens" not in lenses:
        raise CardError(f"eval_ranks_pass_at_k.csv has lenses {lenses}, not {ours} and pooled_lens")
    cols = [ours, "pooled_lens", *(la for la in lenses if la not in (ours, "pooled_lens"))]
    names = {ours: "this lens", "pooled_lens": "pooled lens"}
    evals = [e for e in table if e != "macro"] + (["macro"] if "macro" in table else [])
    rows = []
    for e in evals:
        vals = [table[e].get(la) for la in cols]
        if e == "macro":
            cells = [f"**{v:.3f}**" if v is not None else "-" for v in vals]
            rows.append(f"| **macro** (mean over evals) | {sum(n.values())} | " + " | ".join(cells) + " |")
        else:
            cells = [f"{v:.2f}" if v is not None else "-" for v in vals]
            rows.append(f"| {e} | {n.get(e, '-')} | " + " | ".join(cells) + " |")
    head = f"| eval | items | {' | '.join(names.get(la, la) for la in cols)} |\n|---|---|{'---|' * len(cols)}"
    return ("pass@10 on the recipe's held-out items (`evaluate --items held-out:0`, with this model's correctness "
            "grades), item-weighted, over the same source layers, against the recipe's pooled lens fit in the same "
            f"run:\n\n{head}\n" + "\n".join(rows))  # fmt: skip


def gather(a: argparse.Namespace, out: Path, layers: list[int], base: tuple[str, dict], size: int, sha: str) -> dict:
    """Every fact the card states, read from the fit's stamps, the job's record and the recipe checkout."""
    router, experts = stamp(out, "router_stamp.json"), stamp(out, "experts_stamp.json")
    lens, ev = stamp(out, "*_jpp_lens_stamp.json"), stamp(out, "eval_ranks_stamp.json")
    shards = sorted(out.rglob("fit_shard_stamp.json"))
    if not shards:
        raise CardError("no fit_shard_stamp.json among the fit's files")
    shard = json.loads(shards[0].read_text())["args"]
    if len(shards) != shard["num_shards"]:
        raise CardError(f"{len(shards)} shard stamps for num_shards={shard['num_shards']}")
    for stage, got in [("fit-router", router["args"]["layers"]), ("fit-shard", shard["layers"]),
                       ("fit-weights", lens["args"]["layers"]), ("evaluate", ev["args"]["layers"])]:  # fmt: skip
        if sorted(got) != layers:
            raise CardError(f"the {stage} stamp has layers {got}, not --layers {layers_text(layers)}")
    ours = next(out.glob("*_jpp_lens_stamp.json")).name.removesuffix("_stamp.json")
    rec = json.loads((out / "job.json").read_text()) if (out / "job.json").exists() else {}
    head, clean = recipe_state(a)
    return {
        "layers": layers, "n_layers": base[1]["n_layers"], "base": base, "size": size, "sha": sha,
        "recipe": router["git_hash"], "recipe_head": head, "recipe_clean": clean,
        "data": "WikiText" if shard.get("prompts_json") is None else f"`{shard['prompts_json']}`",
        "router_prompts": router["args"]["num_prompts"], "seed": router["args"]["seed"],
        "experts": experts["args"]["num_clusters"], "trained_on": experts.get("num_prompts_trained_on"),
        "prompts": shard["num_prompts"], "shards": shard["num_shards"], "seq": shard["max_seq_len"],
        "skip": shard["skip_first_n_positions"], "lrp": shard["lrp_mode"], "rows": shard["jacobian_rows_per_pass"],
        "target_offset": shard["target_offset"], "n_fit": len(lens["fitting_item_names"]),
        "n_eval": len(ev["scored_item_names"]), "dates": (router["timestamp"][:10], ev["timestamp"][:10]),
        "export": export_line(out, a.export), "job": rec, "evaluation": evaluation(out, ours),
    }  # fmt: skip


def prior_lens(base: tuple[str, dict]) -> str:
    """One sentence on the lens the pins used for this model before, when it is on the Hub."""
    t = base[1]
    key = t.get("frozen_lens", "jpp")
    src = t["lenses"].get(key)
    if not src or src[0] == "local":
        return ""
    kind = {"jlens": "a plain J-lens", "jpp": "a J++ lens"}.get(key, f"a `{key}` lens")
    where = f"at layers {layers_text(t['lens_layers'])}" if t.get("lens_layers") else "at every layer"
    return (f"The lens we used for this model before is {kind} {where} ([{src[0]}](https://huggingface.co/{src[0]}), "
            f"`{src[1]}`); this one is J++, fit with the published recipe.\n\n")  # fmt: skip


def card(a: argparse.Namespace, f: dict) -> str:
    """The public model card (h200_finish.card, generalised): limitations first, then recipe, file, usage, the
    held-out evaluation and provenance; every number from `f` (gather)."""
    model, name, layers, n_layers = a.hf_model.split("/")[-1], Path(a.cache_path).name, f["layers"], f["n_layers"]
    lt = layers_text(layers)
    every = layers == list(range(n_layers - 1))
    target = (f"the final block (layer {n_layers - 1})" if f["target_offset"] == -1
              else f"block {n_layers + f['target_offset']} (target offset {f['target_offset']})")  # fmt: skip
    shards = "one shard" if f["shards"] == 1 else f"{f['shards']} shards"
    err = f["export"].get("max_rel_err_fp16")
    err = (f"largest per-layer relative (Frobenius) error from the cast {err:.1e}" if err is not None
           else "the per-layer relative error from the cast was printed at export time")  # fmt: skip
    recipe = f"`{f['recipe'][:7]}`" + (", unpatched" if f["recipe_clean"] and f["recipe_head"] == f["recipe"] else
                                       f" (the box's checkout was at `{f['recipe_head'][:7]}`"
                                       f"{'' if f['recipe_clean'] else ' with local changes'} when this was written)")  # fmt: skip
    dates = f["dates"][0] if f["dates"][0] == f["dates"][1] else f"{f['dates'][0]} to {f['dates'][1]}"
    rec = f["job"]
    hw = (f", on one {rec['gpu_name']} ({rec['run_s'] / 3600:.1f} h for the whole job)"
          if rec.get("gpu_name") and rec.get("run_s") else "")  # fmt: skip
    commit = f" at bridge-jspace commit `{rec['commit'][:7]}`" if rec.get("commit") else ""
    d = f["export"].get("d", "int")
    # Markdown prose is one line per paragraph (no hard wraps), so the template's long lines are deliberate.
    return f"""---
license: {a.license}
base_model: {a.hf_model}
tags:
  - interpretability
  - jacobian-lens
  - logit-lens
---

# J++ lens for {model} ({"every layer" if every else f"source layers {lt}"})

A J++ (Jacobian) lens for [{a.hf_model}](https://huggingface.co/{a.hf_model}) at revision `{a.revision}`, fit at {"every source layer" if every else "source layers"} {lt}. The target is {target}.

{prior_lens(f["base"])}## Limitations (read these first)

- **One fit, one seed.** One fit with router seed {f["seed"]}; no second fit or seed has been compared, so the evaluation below has no intervals.
- **{f["prompts"]} prompts, {shards}.** The Jacobians were fit on {f["prompts"]} {f["data"]} prompts x {f["seq"]} tokens (the first {f["skip"]} positions skipped) in {shards}.
- **Only the recipe's held-out evaluation so far.** Our own positive controls had not been run on this lens when this card was written.
- **fp16.** The Jacobians are stored in fp16 ({err}); cast them to fp32 before use.

## Recipe

[safety-research/jpp_lens](https://github.com/safety-research/jpp_lens) @ {recipe}:

- router: {f["router_prompts"]} {f["data"]} prompts, {f["experts"]} clusters, seed {f["seed"]}
- J++ fit (`fit-shard`): {f["prompts"]} {f["data"]} prompts x {f["seq"]} tokens in {shards}; the first {f["skip"]} positions skipped; target = {target}; LRP rules (`{f["lrp"]}`); Jacobian rows per pass {f["rows"]}
- `merge-experts`: {f["experts"]} experts, and the pooled lens (the baseline below)
- readout weights (`fit-weights`): the recipe's `fit:0` items with this model's correctness grades ({f["n_fit"]} items)
- evaluation (`evaluate --items held-out:0`): {f["n_eval"]} held-out items
- run: {dates} (UTC){hw}

## File

`{name}` ({f["size"] / 1e9:.2f} GB), sha256 `{f["sha"]}`

A `torch.save` dict in the same layout as neuronpedia's published lenses:

```python
{{
  "J": {{layer: Tensor[d, d] fp16, ...}},  # layers {lt}, d = d_model
  "source_layers": [{layers[0]}, ..., {layers[-1]}],
  "d_model": {d},
  "n_prompts": {f["trained_on"]},
  "provenance": {{...}},  # source config and fit note
}}
```

## Usage

To read out the residual stream `h` at `layer`, map it to the final layer, then apply the model's final norm and unembedding:

```python
import torch

lens = torch.load("{name}", map_location="cpu", weights_only=True)
h_final = h.float() @ lens["J"][layer].float().T
logits = lm_head(final_norm(h_final))  # the model's final RMSNorm, then lm_head
```

## Evaluation (held-out items)

{f["evaluation"]}

One fit (seed {f["seed"]}) evaluated once; no intervals.

## Provenance

{a.note.rstrip(".")}. Fit for the bridge-jspace project (Dan Orel, MATS) with `scripts/lens_fit/fit_jpp.sh` and exported with `scripts/lens_fit/export_jpp_lens.py`{commit}. Use it at your own risk: it has been checked only against the evaluation above.
"""


# ---------------------------------------------------------------- upload and pins


def upload_cmd(a: argparse.Namespace, sha: str) -> str:
    pub = f"{a.fit_dir}/publish"
    return (f"read -r T; HF_TOKEN=\"$T\" {q(a.venv + '/bin/python')} {q(pub + '/hf_upload.py')} --repo {q(a.hf_repo)} "
            f"--file {q(BOX_REPO + '/' + a.cache_path)} --sha256 {sha} --note {q(a.note)} "
            f"--card {q(pub + '/README_card.md')} --public")  # fmt: skip


def upload(a: argparse.Namespace, out: Path, sha: str) -> tuple[str, str] | None:
    """hf_upload.py on the box (copied there with the card), the token on stdin; (repo id, commit) or None."""
    token = env_value("HF_TOKEN")
    if not token:
        log("the Mac's .env has no HF_TOKEN; upload skipped")
        return None
    pub = f"{a.fit_dir}/publish"
    ssh(a.host, f"mkdir -p {q(pub)}")
    if rsync(str(out / "README_card.md"), str(REPO / "scripts" / "lens_fit" / "hf_upload.py"), f"{a.host}:{pub}/"):
        log("could not copy the card and hf_upload.py to the box; upload skipped")
        return None
    try:
        r = ssh(a.host, upload_cmd(a, sha), stdin=token + "\n", timeout=3600)
    except subprocess.TimeoutExpired:
        log("HF upload timed out; the Mac and the box keep the file")
        return None
    text = (r.stdout[-3000:] + r.stderr[-3000:]).replace(token, "***")
    (out / "hf_upload.txt").write_text(text)
    log(f"4. HF upload exit {r.returncode}: {text.strip()[-400:]}")
    m = re.search(r"^repo (\S+) commit (\S+) private (\S+)$", r.stdout, re.M)
    return (m.group(1), m.group(2)) if r.returncode == 0 and m else None


def hub_sha(repo_id: str, name: str, commit: str) -> str | None:
    from huggingface_hub import HfApi

    try:
        info = HfApi().get_paths_info(repo_id, [name], revision=commit)
    except Exception as e:  # a failed check is reported, not fatal: the upload itself has finished
        log(f"Hub check failed ({type(e).__name__})")
        return None
    lfs = getattr(info[0], "lfs", None) if info else None  # a RepoFile has it; a RepoFolder (a wrong path) does not
    return getattr(lfs, "sha256", None) if lfs else None


def pins_block(a: argparse.Namespace, layers: list[int], sha: str, hub: tuple[str, str] | None, record: str) -> str:
    t = a.base[1]
    where = f"{hub[0]} @ {hub[1]}" if hub else "not published on the Hub"
    text = f"{a.pins_comment}. HF: {where}. Fit record: {record}."
    lines = [f"    # {s}" for s in textwrap.wrap(text, 114, break_long_words=False, break_on_hyphens=False)]
    lines += [
        f"    {json.dumps(a.target)}: {{",
        f'        "repo": {json.dumps(t["repo"])},',
        f'        "revision": {json.dumps(t["revision"])},',
        f'        "n_layers": {t["n_layers"]},',
        f'        "norm_gain": {json.dumps(t["norm_gain"])},',
        f'        "bos": {t["bos"]},',
        f'        "run_prefix": {json.dumps(a.run_prefix)},',
        '        "frozen_lens": "jpp",',
    ]
    if layers != list(range(t["n_layers"] - 1)):
        lines.append(f'        "lens_layers": {layers},')
    lines += [
        '        "lenses": {',
        '            "jpp": (',
        '                "local",',
        f"                {json.dumps(a.cache_path)},",
        f"                {json.dumps(sha)},",
        "            ),",
        "        },",
        f'        "frozen_lens_sha256": {json.dumps(sha)},',
        "    },",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------- main


def dry_run(a: argparse.Namespace, layers: list[int], name: str) -> int:
    p = "[dry-run]"
    rec_path = None
    if a.job:
        st = job_state(a.host, a.job)
        log(f"{p} job {a.job}: {st[0] + ' (' + st[1] + ')' if st else 'box unreachable'}")
        rec_path = st[1] if st and st[1] else None
    exp = box_file(a.host, a.export)
    sha = exp[1] if exp else "<sha256 of the export>"
    log(f"{p} 1. sha256 of {a.host}:{a.export}: "
        + (f"{exp[1]} ({exp[0] / 1e9:.2f} GB)" if exp else "MISSING (expected while the fit runs)"))  # fmt: skip
    find = (f"cd {q(a.fit_dir)} && find . -type f \\( -name '*.json' -o -name '*.csv' -o -name '*.log' -o -name "
            "'*.txt' \\) | sort")  # fmt: skip
    files = ssh(a.host, find).stdout.split()
    log(f"{p} 2. would copy the {len(files)} small files now in {a.host}:{a.fit_dir}/ ({', '.join(files) or 'none yet'})"
        + (f" and the job's log.txt and record ({rec_path})" if rec_path else "")
        + f" to results/lens_fit/{name}_<stamp>/")  # fmt: skip
    box_dst, mac = f"{BOX_REPO}/{a.cache_path}", REPO / a.cache_path
    log(f"{p} 3. would cp the export to {a.host}:~/{box_dst} (now: "
        f"{'exists' if box_exists(a.host, box_dst) else 'absent'}) and rsync it to the Mac's {a.cache_path} (now: "
        f"{'exists' if mac.exists() else 'absent'}); sha256 checked on both")  # fmt: skip
    hub = ssh(a.host, f"{q(a.venv + '/bin/python')} -c {q('import huggingface_hub as h; print(h.__version__)')}")
    head, clean = recipe_state(a)
    log(f"{p} 4. would write README_card.md, copy it and hf_upload.py to {a.host}:{a.fit_dir}/publish/ and run there, "
        f"the token on stdin: {upload_cmd(a, sha)}")  # fmt: skip
    log(f"{p}    checks: the Mac's .env has HF_TOKEN: {env_value('HF_TOKEN') is not None}; huggingface_hub in "
        f"{a.venv}: {hub.stdout.strip() or 'MISSING ' + hub.stderr.strip()[-200:]}; recipe checkout {head[:7]}, "
        f"{'no local changes' if clean else 'LOCAL CHANGES'}")  # fmt: skip
    if "./eval_ranks_pass_at_k.csv" in files:  # the fit has finished: preview the card from a scratch copy
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / name
            save_small(a, out, rec_path)
            try:
                print(card(a, gather(a, out, layers, a.base, exp[0] if exp else 0, sha)))
            except CardError as e:
                log(f"{p}    the card cannot be written yet: {e}")
    log(f"{p} 5. the pins block to add to src/bridge_jspace/pins.py TARGETS (printed, not written):")
    print(pins_block(a, layers, sha, None, f"results/lens_fit/{name}_<stamp>"))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="sesterce-a100x4")
    ap.add_argument("--fit-dir", required=True, help="fit_jpp.sh's OUT on the box")
    ap.add_argument("--export", required=True, help="the fp16 export on the box")
    ap.add_argument("--hf-model", required=True, help="the fit model's repo id")
    ap.add_argument("--revision", required=True, help="the model revision (must match the pins target)")
    ap.add_argument("--layers", required=True, help="the source layers fit, '0-30' or '0,3,6'")
    ap.add_argument("--hf-repo", required=True, help="the Hub repo name under the token's account")
    ap.add_argument("--cache-path", required=True, help="the repo-relative pin path, cache/<target>/lenses/...")
    ap.add_argument("--note", required=True, help="the provenance line (recipe, prompts, seed, date)")
    ap.add_argument("--job", help="the jobq job id that ran the fit (its state, log and record)")
    ap.add_argument(
        "--base-target", help="the pins target with these weights (default: the one with this repo@revision)"
    )
    ap.add_argument("--target", help="the new pins key (default: <base-target>-jpp)")
    ap.add_argument("--run-prefix", help="the new run prefix (default: <base run_prefix>jpp_)")
    ap.add_argument("--pins-comment", default=PINS_COMMENT)
    ap.add_argument("--license", default="apache-2.0", help="the card's license (the base model's)")
    ap.add_argument("--recipe-dir", default="/ephemeral/ext/jpp_lens")
    ap.add_argument("--venv", default="/ephemeral/ext/jpp_lens/.venv", help="the box venv with huggingface_hub")
    ap.add_argument("--dry-run", action="store_true", help="print every step with read-only checks; change nothing")
    ap.add_argument("--wait", action="store_true", help=f"poll --job every {POLL_S // 60} min until it is done")
    ap.add_argument("--job-failed-ok", action="store_true", help="publish although --job failed (export made by hand)")
    a = ap.parse_args()
    if a.wait and not a.job:
        ap.error("--wait needs --job")
    if a.job and not re.fullmatch(r"[A-Za-z0-9_.-]+", a.job):
        ap.error(f"--job {a.job!r}: not a jobq id")
    if Path(a.cache_path).is_absolute() or ".." in Path(a.cache_path).parts or not a.cache_path.startswith("cache/"):
        ap.error("--cache-path is repo-relative under cache/")
    layers = parse_layers(a.layers)
    a.base = base_target(a)
    a.target = a.target or f"{a.base[0]}-jpp"
    a.run_prefix = a.run_prefix or f"{a.base[1]['run_prefix']}jpp_"
    if a.target in pins.TARGETS:
        log(f"note: pins already has {a.target!r}; the block below would replace it")
    name = Path(a.fit_dir).name
    if a.dry_run:
        return dry_run(a, layers, name)

    rec_path = None
    if a.wait:
        rec_path = wait_for(a)[1]
    elif a.job:
        st = job_state(a.host, a.job)
        if st is None or st[0] not in ("done", "failed") or (st[0] == "failed" and not a.job_failed_ok):
            raise SystemExit(f"job {a.job}: {st}; publish a done job (or a failed one with --job-failed-ok)")
        rec_path = st[1]
        if st[0] == "failed":
            log(f"job {a.job} failed; publishing anyway (--job-failed-ok)")
    exp = box_file(a.host, a.export)
    if exp is None:
        raise SystemExit(f"{a.host}:{a.export} is missing")
    size, sha = exp
    log(f"1. {a.host}:{a.export}: sha256 {sha} ({size / 1e9:.2f} GB)")
    out = REPO / "results" / "lens_fit" / f"{name}_{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    log("2. copying the fit's small files and the job's log and record")
    save_small(a, out, rec_path)
    printed = printed_sha(out, a.export)
    if printed and printed != sha:
        raise SystemExit(f"the export's sha256 on the box {sha} != the {printed} printed when it was written")
    log(f"   matches the sha256 printed at export: {printed == sha}" + ("" if printed else " (none printed)"))
    cache_copies(a, sha)

    hub, hub_ok = None, False
    try:
        (out / "README_card.md").write_text(card(a, gather(a, out, layers, a.base, size, sha)))
        hub = upload(a, out, sha)
    except CardError as e:
        log(f"4. no card and no upload: {e}")
    if hub:
        got = hub_sha(hub[0], Path(a.cache_path).name, hub[1])
        hub_ok = got == sha
        log(f"   the Hub's sha256 for {hub[0]}@{hub[1]}: {got} ({'matches' if hub_ok else 'DOES NOT MATCH'})")
    block = pins_block(a, layers, sha, hub, str(out.relative_to(REPO)))
    (out / "publish.json").write_text(json.dumps({
        "export": f"{a.host}:{a.export}", "sha256": sha, "size": size, "cache_path": a.cache_path,
        "box_cache": f"{a.host}:~/{BOX_REPO}/{a.cache_path}", "hf": hub, "hf_sha256_ok": hub_ok,
        "target": a.target, "pins_block": block}, indent=1) + "\n")  # fmt: skip
    log("5. the pins block to add to src/bridge_jspace/pins.py TARGETS (not written; also in publish.json):")
    print(block)
    return 0 if hub_ok else 1


if __name__ == "__main__":
    sys.exit(main())
