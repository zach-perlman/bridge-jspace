"""lens_csv: one row block per model the README reports, saying which lens its runs used and how well that lens reads.

Writes data/figures/lenses.csv (key, model, quantity, value, unit, source), nothing typed by hand:

- Which lens: the model's headline run in docs/breadth/data.csv (`ko.<code>.mk`, else `text.<code>`) -> that run's
  manifest.json "lens" [name, sha256] -> the pins.TARGETS entry whose frozen lens has that sha256. A Hub lens (repo,
  file, revision) is "published"; a ("local", path, sha256) lens is "our fit", and its fit record is the
  results/lens_fit/<folder> committed together with the line that put this sha256 into src/bridge_jspace/pins.py
  (git log -S on pins.py; exactly one folder or the script stops).
- How well: the J++ recipe's held-out evaluation (safety-research/jpp_lens@93f02cd `evaluate --items held-out:0`: the
  readout-eval items the model itself answers right), its own eval_ranks*_pass_at_k.csv: macro (mean of the five
  evals), item-weighted pass@10, where an item's intermediate counts as found if its rank is <= 10 at any evaluated
  layer. An our-fit lens is read from its fit record; a published lens from an evaluate run whose stamp names that
  lens file at the pinned revision. The logit lens (`.logit`) and, for our fits, a published J++ pinned for the same
  checkpoint (`.ref`; for Gemma 4 31B-it that is the base model's lens) are taken only from files that scored exactly
  the same items at the same layers (checked). Item sets differ between models, so compare a lens with its logit
  lens, not across models.
- No evaluation run file -> value "not measured", no source. Numbers that exist only as comments (pins.py) are
  printed by the script for the report, never written as measured.

uv run python scripts/lens_csv.py   # -> data/figures/lenses.csv; prints the comment-vs-run-file check
"""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
from collections.abc import Iterable
from itertools import pairwise
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
assert os.environ.get("BJ_TARGET", "qwen3.6-27b") == "qwen3.6-27b", "run with BJ_TARGET unset: pins' 27B constants"
from bridge_jspace import pins  # noqa: E402

BREADTH = REPO / "docs/breadth/data.csv"
OUT = REPO / "data/figures/lenses.csv"
PINS = "src/bridge_jspace/pins.py"
EVALS = ("association", "multihop", "multilingual", "poetry", "typo")  # the recipe's MACRO_EVALS
K = 10
NOT_MEASURED = "not measured"
UNIT = "pass@10, held-out macro"
# Evaluate runs with a stamp that names the model and the lens files (where a published lens can be found).
STAMP_GLOBS = ("results/lens_check/*/eval_ranks*_stamp.json", "results/lens_fit/*/eval_ranks*_stamp.json",
               "results/lens_eval/*/eval_ranks*_stamp.json")  # fmt: skip
# Model codes as docs/breadth/data.csv names them: the nine breadth models, the three untestable ones, the 9B base and
# our-fit comparisons, and the architecture pairs the root README links (Qwen3-32B, the two Olmo 7Bs).
MODELS = ("q27", "q9", "nl", "ds", "mi", "nb", "ol", "mu", "q122", "gemma", "gptoss", "kol", "q9base", "q9oj", "q32",
          "oh7", "o7")  # fmt: skip


def rel(p: Path) -> str:
    return str(p.relative_to(REPO))


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, check=True).stdout


def headline_run(code: str, breadth: dict[str, dict]) -> tuple[str, Path]:
    """(data.csv key, the run's manifest.json) for the model's knock-out headline, else its plain-text gate run."""
    for key in (f"ko.{code}.mk", f"text.{code}"):
        if key not in breadth:
            continue
        src = REPO / breadth[key]["source"]
        if src.name == "summary.json":  # results/removal_textloss/<run>/summary.json
            return key, src.parent / "manifest.json"
        run = json.loads(src.read_text())["run"]  # results/ablate_v2/jsuite*_score/<run>.json
        return key, REPO / "results/ablate_v2" / run / "manifest.json"
    raise KeyError(f"{code}: neither ko.{code}.mk nor text.{code} in {rel(BREADTH)}")


def frozen(target: dict) -> tuple[str, tuple, str | None]:
    """(lens name, its source tuple, its sha256) of a target's frozen lens; the 27B's sha256 is pins' module constant."""
    name = target.get("frozen_lens", pins.FROZEN_LENS)
    src = target["lenses"].get(name)
    sha = target.get("frozen_lens_sha256")
    if sha is None and src == pins.LENS_SOURCES.get(pins.FROZEN_LENS):
        sha = pins.FROZEN_LENS_SHA256
    return name, src, sha


def target_of(sha: str, run: str) -> str:
    """The pins target whose frozen lens has `sha256`; among several, the one whose run prefix the run name carries."""
    keys = [k for k, t in pins.TARGETS.items() if t.get("lenses") and frozen(t)[2] == sha]
    keys = [k for k in keys if run.startswith(pins.TARGETS[k]["run_prefix"])]
    best = max(len(pins.TARGETS[k]["run_prefix"]) for k in keys)
    keys = [k for k in keys if len(pins.TARGETS[k]["run_prefix"]) == best]
    assert len(keys) == 1, f"run {run}, lens {sha[:8]}: targets {keys}"
    return keys[0]


def fit_folder(sha: str) -> tuple[str, str]:
    """(results/lens_fit/<folder>, commit): the fit record committed with the pins line that first holds `sha`."""
    commit = git("log", "--reverse", "-S", sha, "--format=%H", "--", PINS).split()[0]
    files = git("show", "--name-only", "--format=", commit).split()
    folders = {"/".join(f.split("/")[:3]) for f in files if f.startswith("results/lens_fit/")}
    assert len(folders) == 1, f"lens {sha[:8]}: commit {commit[:8]} adds lens_fit folders {sorted(folders)}"
    return folders.pop(), commit


def hf_model(stamp: dict) -> str:
    name = stamp["args"]["hf_model_name"]
    m = re.search(r"models--([^/]+?)--([^/]+)/snapshots/", name)
    return f"{m[1]}/{m[2]}" if m else name


def stamps() -> list[tuple[Path, dict]]:
    """(ranks csv, stamp) for every evaluate run whose stamp is kept beside its ranks file."""
    out = []
    for g in STAMP_GLOBS:
        for s in sorted(REPO.glob(g)):
            ranks = s.with_name(s.name.removesuffix("_stamp.json") + ".csv")
            if ranks.exists():
                out.append((ranks, json.loads(s.read_text())))
    return out


_ITEMS: dict[tuple[Path, str], tuple[frozenset, list[int]]] = {}


def items(ranks: Path, lens: str) -> tuple[frozenset, list[int]]:
    """((eval, item) pairs over the five macro evals, layers) a lens was scored at in one ranks file."""
    if (ranks, lens) not in _ITEMS:
        its, layers = set(), set()
        with ranks.open() as f:
            for d in csv.DictReader(f):
                if d["lens"] == lens and d["eval"] in EVALS:
                    its.add((d["eval"], d["item"]))
                    layers.add(int(d["layer"]))
        _ITEMS[ranks, lens] = (frozenset(its), sorted(layers))
    return _ITEMS[ranks, lens]


def macro(ranks: Path, lens: str) -> float | None:
    """The recipe's macro item-weighted pass@10 for `lens` from the pass_at_k file beside `ranks` (None: empty cell)."""
    pk = ranks.with_name(ranks.stem + "_pass_at_k.csv")
    with pk.open() as f:
        for d in csv.DictReader(f):
            if (d["eval"], d["lens"], d["k"], d["weighting"]) == ("macro", lens, str(K), "item"):
                return float(d["pass_at_k"]) if d["pass_at_k"] else None
    return None


def same_items(ranks: Path, lens: str, model: str, other: str, pool: list[tuple[Path, dict]]) -> Path | None:
    """The ranks file that scored `other` on exactly the items and layers `lens` was scored on in `ranks`: `ranks`
    itself first, then an evaluate run on the same model whose stamp names `other`."""
    mine = items(ranks, lens)
    for r in [ranks] + [r for r, s in pool if hf_model(s) == model and other in s["lenses"]]:
        if items(r, other)[0] and items(r, other) == mine:
            return r
    return None


def f3(v: float) -> str:
    return f"{v:.3f}"


def published_run(src: tuple, pool: list[tuple[Path, dict]]) -> Path | None:
    """The evaluate run whose stamp loads this Hub file at the pinned revision."""
    repo, file, rev = src
    want = f"models--{repo.replace('/', '--')}/snapshots/{rev}/{file}"
    hits = [r for r, s in pool if any(str(p).endswith(want) for p in s["lenses"].values())]
    return hits[0] if hits else None


def span(layers: Iterable[int]) -> str:
    ls = sorted(layers)
    step = {b - a for a, b in pairwise(ls)}
    if len(step) == 1 and step != {1}:
        return f"{ls[0]}-{ls[-1]} every {step.pop()}"
    return f"{ls[0]}-{ls[-1]}" if step <= {1} else ",".join(map(str, ls))


def build() -> tuple[list[dict], list[str]]:
    with BREADTH.open() as f:
        breadth = {d["key"]: d for d in csv.DictReader(f)}
    pool = stamps()
    yamls = {}
    for y in sorted((REPO / "configs/models").glob("*.yaml")):
        for m in re.finditer(r"repo: (\S+)\n\s+revision: (\S+)\n(?:\s+\S+: .*\n)*?\s+sha256: (\w+)", y.read_text()):
            yamls[m[3]] = (f"{m[1]}@{m[2]}", rel(y))
    rows, notes = [], []

    def add(code: str, q: str, quantity: str, value, unit: str, source: str) -> None:
        rows.append({"key": f"lens.{code}.{q}", "model": code, "quantity": quantity, "value": value, "unit": unit,
                     "source": source})  # fmt: skip

    for code in MODELS:
        bkey, manifest = headline_run(code, breadth)
        man = json.loads(manifest.read_text())
        lname, sha = man["lens"]
        key = target_of(sha, man["run"])
        t = pins.TARGETS[key]
        name, src, _ = frozen(t)
        assert name == lname, f"{code}: run lens {lname}, pins frozen lens {name}"
        stem = Path(src[1]).stem  # the lens's name in the recipe's ranks files
        ptr = f"{PINS} | TARGETS[{key!r}]"
        add(code, "model", "model checkpoint", f"{t['repo']}@{t['revision'][:8]}", "", ptr)
        add(
            code,
            "target",
            "pins target of the run's lens",
            key,
            "",
            f"{rel(manifest)} | lens (run of {rel(BREADTH)} {bkey})",
        )
        add(code, "type", "lens type", {"jpp": "J++", "jlens": "plain J-lens"}[name], "", ptr)
        add(code, "sha256", "lens file sha256", sha, "", f"{rel(manifest)} | lens")
        if src[0] == "local":
            folder, commit = fit_folder(sha)
            add(code, "kind", "who fitted the lens", "our fit", "", ptr)
            add(code, "lens", "fit record", folder, "", f"{folder} | commit {commit[:8]} sets this sha256 in {PINS}")
            if sha in yamls:
                add(code, "hub", "our fit, uploaded", yamls[sha][0], "", f"{yamls[sha][1]} | lenses")
            ranks = REPO / folder / "eval_ranks.csv"
            ranks = ranks if ranks.exists() and items(ranks, stem)[0] else None
        else:
            add(code, "kind", "who fitted the lens", "published", "", ptr)
            add(code, "lens", "published file", f"{src[0]}/{src[1]}@{src[2][:8]}", "", ptr)
            ranks = published_run(src, pool)
        value = macro(ranks, stem) if ranks else None
        if value is None:
            why = f"{rel(ranks)} has no macro (an eval has no items)" if ranks else "no evaluate run of this lens"
            notes.append(f"{code} ({key}): {why}")
            add(code, "passk", "lens quality", NOT_MEASURED, UNIT, "")
            continue
        its, layers = items(ranks, stem)
        pk = rel(ranks.with_name(ranks.stem + "_pass_at_k.csv"))
        field = f"eval=macro, lens={stem}, k={K}, weighting=item"
        add(code, "passk", "lens quality", f3(value), UNIT, f"{pk} | {field}")
        add(
            code,
            "n",
            "held-out items scored",
            len(its),
            "items",
            f"{rel(ranks)} | lens={stem}, evals {'/'.join(EVALS)}",
        )
        add(
            code, "layers", "layers scored (best rank over them)", span(layers), "layers", f"{rel(ranks)} | lens={stem}"
        )
        r = same_items(ranks, stem, t["repo"], "logit", pool)
        v = macro(r, "logit") if r else None
        if v is None:
            notes.append(f"{code} ({key}): no logit lens scored on the same items")
            add(code, "logit", "logit lens, same items", NOT_MEASURED, UNIT, "")
        else:
            lsrc = f"{rel(r.with_name(r.stem + '_pass_at_k.csv'))} | eval=macro, lens=logit, k={K}, weighting=item"
            add(code, "logit", "logit lens, same items", f3(v), UNIT, lsrc)
        if src[0] == "local":  # a published J++ run on the same checkpoint, same items and layers, where one was scored
            pubs = [
                (k, frozen(u)[1])
                for k, u in pins.TARGETS.items()
                if u.get("lenses")
                and u["repo"] == t["repo"]
                and u["revision"] == t["revision"]
                and frozen(u)[0] == "jpp"
                and frozen(u)[1][0] != "local"
            ]
            for pk_key, psrc in pubs:
                pr = published_run(psrc, pool)
                pstem = Path(psrc[1]).stem
                if pr and items(pr, pstem) == (its, layers):
                    add(code, "ref", f"published J++ {psrc[1]} (pins {pk_key}), same items", f3(macro(pr, pstem)), UNIT,
                        f"{rel(pr.with_name(pr.stem + '_pass_at_k.csv'))} | eval=macro, lens={pstem}, k={K}, "
                        "weighting=item")  # fmt: skip
                    break
            else:
                if pubs:
                    notes.append(f"{code} ({key}): published J++ {pubs[0][0]} not scored on the same items")
    return rows, notes


def comment_check(rows: list[dict]) -> list[str]:
    """Each our-fit pass@10 written as a comment in pins.py next to the run file's value (printed, never written). The
    comment names the lens file's stem, which a published lens of the same model can share, so our fits only."""
    text = (REPO / PINS).read_text()
    ours = {r["model"] for r in rows if r["key"].endswith(".kind") and r["value"] == "our fit"}
    out = []
    for r in rows:
        if not r["key"].endswith(".passk") or r["value"] == NOT_MEASURED or r["model"] not in ours:
            continue
        stem = r["source"].split("lens=")[1].split(",")[0]
        for m in re.finditer(rf"'{re.escape(stem)}': ([0-9.]+)", text):
            out.append(f"{r['model']}: pins comment {m[1]} vs run file {r['value']}"
                       + ("" if abs(float(m[1]) - float(r["value"])) < 6e-4 else "  <-- DIFFERS"))  # fmt: skip
    return out


def main() -> None:
    rows, notes = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["key", "model", "quantity", "value", "unit", "source"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {rel(OUT)}: {len(rows)} rows, {len(MODELS)} models")
    for n in notes:
        print("not measured:", n)
    for c in comment_check(rows):
        print(c)


if __name__ == "__main__":
    main()
