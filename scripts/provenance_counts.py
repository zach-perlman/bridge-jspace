"""Provenance of the runs the root README cites (Dan, 8 Nov, follow-up 7): every src comment in README.md is traced to
the run folders (manifest.json) its number comes from, directly (results/…, runs/…) or through a data file's
source column (docs/breadth/data.csv, data/figures/depth/data.csv, data/figures/writeup/data.csv); each manifest is read
for a git commit (40 hex digits under a commit/git/code key) and a lens sha256 (64 hex digits under a lens key). Also the
two counts of the 8 Nov fix to the manifest writers (G1, commit bd43870f): writers that now record their switches and
writers left out of the check (no model loaded). Written as keys to data/figures/provenance.csv for the README.

Only files git tracks count: a run folder is one whose manifest.json is in `git ls-files`, so local runs that are in
no commit never change the counts. Two cases keep committed values instead of recomputing (each printed):
- a checkout without some of those files (a sparse clone, e.g. the README's read-only set docs figures data/figures):
  the script stops and data/figures/provenance.csv stays as committed;
- a partial (blob-less) clone: the g1.* rows are carried over, since `git archive` of the two fixed commits there
  fetches nearly every blob of the commit (2.3 GB, measured 8 Nov); they are counts of two fixed commits, so they
  cannot change.

uv run python scripts/provenance_counts.py
"""

from __future__ import annotations

import csv
import functools
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
README = REPO / "README.md"
OUT = REPO / "data/figures/provenance.csv"
DATA = {
    "docs/breadth/data.csv": "key",
    "data/figures/writeup/data.csv": "key",
    "data/figures/depth/data.csv": "quantity",
}
SRC = re.compile(r"<!-- src: ([^|]+?) \| (.+?) -->")
RUNPATH = re.compile(r"((?:results|runs)/[\w./-]+)")
HEX40, HEX64 = re.compile(r"\b[0-9a-f]{40}\b"), re.compile(r"\b[0-9a-f]{64}\b")
G1 = "bd43870f"


def data_sources() -> dict[str, dict[str, list[str]]]:
    out: dict[str, dict[str, list[str]]] = {}
    for path, keycol in DATA.items():
        with (REPO / path).open() as f:
            for r in csv.DictReader(f):
                out.setdefault(path, {}).setdefault(r[keycol].strip(), []).append(r.get("source", ""))
    return out


@functools.cache
def tracked() -> frozenset[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True, check=True).stdout
    return frozenset(out.split("\0")) - {""}


@functools.cache
def run_folders() -> dict[str, list[str]]:
    """Folder -> its subfolders that hold a tracked manifest.json."""
    out: dict[str, list[str]] = {}
    for f in tracked():
        if f.endswith("/manifest.json"):
            d = Path(f).parent
            out.setdefault(str(d.parent), []).append(d.name)
    return out


def is_run(q: Path) -> bool:
    return f"{q.relative_to(REPO)}/manifest.json" in tracked()


def run_dir(path: str) -> Path | None:
    """The run folder of a cited file: the nearest ancestor with a tracked manifest.json, or a sibling folder named after
    the file (a score file such as results/ablate_v2/jsuite2_score/<run>.json, or a read file <run>_noteNN.json)."""
    p = REPO / path
    for q in [p, *p.parents]:
        if q == REPO:
            break
        if is_run(q):
            return q
    stem = p.stem
    for parent in p.parents[:3]:
        for name in sorted(run_folders().get(str(parent.relative_to(REPO)), [])):
            if stem == name or stem.startswith(name + "_"):
                return parent / name
    return None


def read_file_runs(path: str) -> list[Path]:
    """A read file that names its runs ({"prefix": …, "runs": {arm: run name}}, as results/ablate_v2/nn_ko_read/*.json do):
    the run folders it read, next to its own folder."""
    p = REPO / path
    if p.suffix != ".json" or path not in tracked() or not p.is_file():
        return []
    try:
        d = json.loads(p.read_text())
    except ValueError:
        return []
    if not isinstance(d, dict):
        return []
    names = (
        list(d["runs"].values())
        if isinstance(d.get("runs"), dict)
        else [d["run"]]
        if isinstance(d.get("run"), str)
        else []
    )
    prefix = d.get("prefix") or ""
    out = []
    for name in names:
        for base in (p.parent.parent, p.parent):
            q = base / f"{prefix}{name}"
            if is_run(q):
                out.append(q)
                break
    return out


def has(manifest: dict, keyword: tuple[str, ...], pattern: re.Pattern) -> bool:
    def walk(d, keyhit: bool) -> bool:
        if isinstance(d, dict):
            return any(walk(v, keyhit or any(w in k.lower() for w in keyword)) for k, v in d.items())
        if isinstance(d, list):
            return any(walk(v, keyhit) for v in d)
        return keyhit and isinstance(d, str) and bool(pattern.search(d))

    return walk(manifest, False)


def partial_clone() -> bool:
    """A clone made with --filter (a promisor remote, or the older extensions.partialClone): blobs come on demand."""
    out = subprocess.run(["git", "config", "--get-regexp", r"^(remote\..*\.promisor|extensions\.partialclone)$"],
                         cwd=REPO, capture_output=True, text=True).stdout  # fmt: skip
    return any(v.strip().lower() not in ("", "false") for v in (ln.split(" ", 1)[-1] for ln in out.splitlines()))


def g1_counts() -> tuple[int, int, int]:
    """At {G1}'s parent, the test's own scan (tests/test_run_switches.py manifest_writers, with that commit's LEFT_OUT
    and DELEGATES): the manifest writers that recorded no switches; and of those, how many {G1} made record them and
    how many it left out (no model loaded)."""
    import importlib.util
    import io
    import tarfile
    import tempfile

    def missing_at(rev: str, root: Path) -> tuple[set[str], set[str]]:
        tar = subprocess.run(["git", "archive", rev, "scripts", "src", "tests/test_run_switches.py"], capture_output=True,
                             cwd=REPO, check=True).stdout  # fmt: skip
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            t.extractall(root, filter="data")
        spec = importlib.util.spec_from_file_location(f"t_{rev}", root / "tests/test_run_switches.py")
        assert spec is not None
        assert spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        setattr(mod, "REPO", root)  # noqa: B010 (a module attribute pyright cannot see)
        writers = mod.manifest_writers()
        return (
            {w for w, ok in writers.items() if not ok and w not in mod.LEFT_OUT and w not in mod.DELEGATES},
            set(mod.LEFT_OUT),
        )

    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        before, _ = missing_at(f"{G1}^", Path(a))
        after, left_after = missing_at(G1, Path(b))
    left = len(before & left_after)
    return len(before), len(before - after) - left, left


def main() -> None:
    srcs = data_sources()
    cited: set[str] = set()
    for path, keys in SRC.findall(README.read_text()):
        path = path.strip()
        if path.startswith(("results/", "runs/")):
            cited.add(path)
        elif path in srcs:
            for key in (k.strip() for k in keys.split(";")):
                for source in srcs[path].get(key, []):
                    cited.update(RUNPATH.findall(source))
    # read files name their runs inside: they and every manifest must be on disk, else keep the committed counts
    absent = sorted(c for c in cited if c in tracked() and c.endswith(".json") and not (REPO / c).is_file())
    runs, untraced = set(), set()
    for c in cited:
        found = [d for d in [run_dir(c), *read_file_runs(c)] if d]
        runs.update(found) if found else untraced.add(c)
    absent += sorted(str(d.relative_to(REPO)) for d in runs if not (d / "manifest.json").is_file())
    if absent:
        print(f"provenance_counts: skipped, {len(absent)} tracked run files not in this checkout (a sparse clone?), "
              f"e.g. {absent[0]}; {OUT.relative_to(REPO)} kept as committed")  # fmt: skip
        return
    no_commit = no_lens = 0
    for d in runs:
        m = json.loads((d / "manifest.json").read_text())
        no_commit += not has(m, ("commit", "git", "code"), HEX40)
        no_lens += not has(m, ("lens",), HEX64)
    # a blob-less clone: `git archive` would fetch nearly every blob of the commit (see the docstring)
    if partial_clone():
        with OUT.open() as f:
            kept = {r["key"]: int(r["value"]) for r in csv.DictReader(f)}
        unrecorded, switches, left_out = (kept[f"g1.writers_{k}"] for k in ("unrecorded", "switches", "left_out"))
        print(f"provenance_counts: a partial clone, g1.* kept as committed in {OUT.relative_to(REPO)}")
    else:
        unrecorded, switches, left_out = g1_counts()
    rows = {"prov.runs": (len(runs), "run folders (manifest.json) behind README.md's numbers"),
            "prov.untraced": (len(untraced), "cited result files with no manifest found beside or above them"),
            "prov.no_commit": (no_commit, "of the runs, manifests without a git commit"),
            "prov.no_lens_sha": (no_lens, "of the runs, manifests without a lens sha256"),
            "g1.writers_unrecorded": (unrecorded, f"manifest writers that recorded no switches before {G1} (the test's scan)"),
            "g1.writers_switches": (switches, f"of those, writers that record their switches since {G1}"),
            "g1.writers_left_out": (left_out, f"of those, writers {G1} left out of the check (no model loaded)")}  # fmt: skip
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["key", "value", "source"])
        for k, (v, what) in rows.items():
            w.writerow([k, v, f"scripts/provenance_counts.py: {what}"])
    print(f"wrote {OUT.relative_to(REPO)}: " + ", ".join(f"{k} {v}" for k, (v, _) in rows.items()))
    if untraced:
        print("untraced:", sorted(untraced)[:10])


if __name__ == "__main__":
    main()
