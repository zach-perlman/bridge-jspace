"""xfig_depth_profile (X-fig, thread C3; Dan, 24 Oct): do Zach's knock-out band and Dan's split agree in depth,
including the models where both fail? Descriptive: no pass/fail rule.

One panel per model with both methods (Qwen3.5-9B, Qwen3.6-27B, OLMo-3-7B, Qwen3.5-122B); x = depth, % of the model's
layers (100 * layer / n_layers; n_layers from pins.TARGETS, checked equal to Zach's pins at ZACH_COMMIT). Layer L is the
block output of layer L on both sides (a forward hook on model.layers[L]).
- Left axis, Dan: recall minus lookup J-dependence at every cell of scripts/figs/split_depth (its CELLS, MAIN and FULL;
  J-dependence = (F(whole) - F(without J)) / F(whole), F = the share switched; recalls PM, lookups PP, the same scenes).
  95% interval: paired percentile bootstrap over scenes (2000 draws, seed 0). Filled: the bridge's word or sentence;
  hollow: the whole context (split_depth's marking).
- Right axis, Zach: memory-final minus lookup-final loss (points) in each window of his held-out depth sweep on ctrl_v8
  (results/ablate_v2/<sweep>/summary.json; loss = unedited accuracy - paper10 accuracy per word, averaged over PM, MM
  and over PP, MP: scripts/c1_v2.py's definition), drawn at the window's middle layer, recomputed from its rows.jsonl as
  a check. 95% interval: percentile bootstrap over bridge entities (1000 draws, seed 0; c1_v2.ci's resampling unit).
- Shaded: Zach's chosen band, "band" of results/ablate_v2/band_choice/<sweep>.json (scripts/choose_band.py), where that
  file exists at ZACH_COMMIT. --band-of-record shades instead (hatched) the "middle" of the model's c1_v2 score file
  where no band_choice file exists: the band Zach's C1 test used, whose choice is not on record.
- Vertical line: Dan's split layer, read after seeing the data (README.md: 9B 12, 27B 32, 122B 33; OLMo-3 none),
  checked against split_depth.split_of.
Both y ranges are fixed in advance and symmetric (-1..1, -100..100 points): both zeros sit at the same height.

Zach's files are read with `git show ZACH_COMMIT:<path>`, never from a working tree; Dan's from this checkout, where they
must be committed and unchanged. Every input must be J++: the manifest's lens "jpp" with the sha256 pinned here (Zach's:
also in his pins.py at ZACH_COMMIT; Dan's: equal to pins.TARGETS); plain J-lens runs (PLAIN_JLENS) raise.

uv run python scripts/xfig_depth_profile.py [--check-inputs] [--band-of-record] [--out DIR]
--check-inputs: verifies every input file, column, lens and checkpoint; prints schema and row counts only, no value.
Otherwise writes results/xfig_depth_profile/<UTC stamp>/: xfig_depth_profile.png and .svg, data.csv (every drawn number
with its source file and row key), caption.md, manifest.json (input commits and sha256s).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import statistics
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

if __package__ in (None, ""):  # run as a file; a copy outside the repo (a scratch dir) finds the repo at the cwd
    for root in (Path(__file__).resolve().parents[1], Path.cwd()):
        if (root / "src" / "bridge_jspace").is_dir():
            sys.path.insert(0, str(root / "src"))
            sys.path.insert(0, str(root))
            break

import numpy as np

from bridge_jspace import pins
from scripts.figs import common as C
from scripts.figs import split_depth as SD
from scripts.figs import stated_bridge as SB

REPO = pins.REPO_ROOT
STEM = "xfig_depth_profile"
OUT = REPO / "results" / STEM
ZACH_COMMIT = "a6db0d602e71acc8483e33f68fc389c2ab70c79b"
ZACH_BRANCH = "zach/v8-breadth-1021"
ABL = "results/ablate_v2"
PANELS = ("9b", "27b", "olmo", "122b")
SWEEP = {"9b": "qwen35_9b_ctrl_sweep_v1", "27b": "ctrl_sweep_v1", "olmo": "olmo3d7_ctrl_sweep_v1",
         "122b": "qwen35_122b_ctrl_sweep_v1"}  # fmt: skip
# the C1 test runs on full_v8; their c1_v2 score files carry the band the test used ("middle")
C1_RUN = {"9b": "qwen35_9b_full2_ko_v1", "27b": "full2_ko_v1", "olmo": "olmo3d7_full2_ko_v1",
          "122b": "qwen35_122b_full2_ko_v1"}  # fmt: skip
# each sweep's lens, from Zach's pins.py at ZACH_COMMIT: (repo or "local", file, sha256)
ZACH_LENS = {
    "ctrl_sweep_v1": ("neuronpedia/jacobian-lens", "qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt",
                      "bbef480b41028e156c4aa3c334ad32d1b76a4017ef3a7245eecf776bf2b58f8f"),
    "qwen35_9b_ctrl_sweep_v1": ("neuronpedia/jacobian-lens", "qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt",
                                "8cda12f7ddf11e70fcfc69a47a9574f626fe084c67807a4781f4f67106e739c5"),
    "olmo3d7_ctrl_sweep_v1": ("local", "cache/olmo-3-7b/lenses/jpp/Olmo-3-7B-Instruct-DPO_jpp_lens.pt",
                              "1ca44bf5938b400b64a32bf9585b5e4cedb6a10249005b0cb6643f9115e94c11"),
    "qwen35_122b_ctrl_sweep_v1": ("neuronpedia/jacobian-lens",
                                  "qwen3.5-122b-a10b/jpp/Salesforce-wikitext/Qwen3.5-122B-A10B_jpp_lens.pt",
                                  "b771e50244c81a3f315987ca2b8e88a58f670e3fed934dd21e3bfec4a3c05e53"),
}  # fmt: skip
PLAIN_JLENS = ("qwen3_32bj_", "muse30j_", "gptoss20j_", "q27jlens_")  # run prefixes of plain J-lens runs: never inputs
ZACH_ONLY = (("Qwen3-32B", "qwen3_32b_ctrl_sweep_v1"), ("Olmo-Hybrid-7B", "olmoh7_ctrl_sweep_v1"))  # not drawn
# README.md (135dc0e) "Next steps": "at a predicted layer: 9B 12, 27B 32 at the word, 122B 33"; "Weak spots": "OLMo-3
# shows no split"
SPLIT: dict[str, int | None] = {"9b": 12, "27b": 32, "122b": 33, "olmo": None}
SPLIT_SOURCE = "README.md (Weak spots; Next steps, split-depth confirmation)"
MEMORY_FINAL, LOOKUP_FINAL = ("PM", "MM"), ("PP", "MP")  # scripts/c1_v2.py MEMORY_FINAL, PROMPT_FINAL
WORDS = LOOKUP_FINAL + MEMORY_FINAL
KNOCKOUT = "paper10"
N_BOOT_ZACH = 1000
ZACH_ROW_FIELDS = ("band", "condition", "family", "kind", "id", "correct")
DAN_ROW_FIELDS = ("family", "name", "scene", "set", "layer", "part", "source", "null", "role")
DAN, ZACH = C.LOOKUP, C.darken_to("#0072B2")  # the accent; Okabe-Ito blue (palette checked: CVD 6.9, shapes differ)

TITLE = "Zach's knock-out band and Dan's split, by depth"
SUBTITLE = "Dan: recall − lookup J-dependence (left). Zach: memory − lookup-final loss (right)"
HOW = "circles: Dan; squares: Zach; shaded: Zach's band (held-out); line: Dan's split (post hoc)"
CAPTION1 = (
    "Band: held-out data, lookups excluded (independent of the split). Split: post hoc until X0. Same J++ in both."
)
CAPTION2 = "122B: bf16 J++ on FP8. Hollow: whole context. 95% CIs."


# ---------------------------------------------------------------- inputs


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, check=True).stdout


def at_commit(path: str, commit: str = ZACH_COMMIT) -> bytes | None:
    """The file's bytes at the commit (git show), None when the commit has no such file."""
    p = subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:{path}"], capture_output=True, check=False)
    return p.stdout if p.returncode == 0 else None


@dataclass
class Input:
    side: str  # dan / zach
    model: str
    path: str  # repo-relative
    commit: str  # the commit whose bytes were read (Dan's: HEAD, the file unchanged in this checkout)
    sha256: str
    lines: int


@dataclass
class Inputs:
    head: str
    files: list[Input] = field(default_factory=list)

    def zach(self, model: str, path: str, required: bool = True) -> bytes | None:
        data = at_commit(path)
        if data is None:
            if required:
                raise FileNotFoundError(f"{path}: not at {ZACH_COMMIT[:7]}")
            return None
        self.files.append(Input("zach", model, path, ZACH_COMMIT, sha256(data), data.count(b"\n")))
        return data

    def dan(self, model: str, path: Path) -> bytes:
        rel = str(path.relative_to(REPO))
        tracked = subprocess.run(["git", "-C", str(REPO), "ls-files", "--error-unmatch", rel], capture_output=True,
                                 check=False).returncode == 0  # fmt: skip
        if not tracked:
            raise ValueError(f"{rel}: not committed; an input must be")
        if git("status", "--porcelain", "--", rel).strip():
            raise ValueError(f"{rel}: differs from HEAD in this checkout")
        data = path.read_bytes()
        if not any(f.path == rel for f in self.files):
            self.files.append(Input("dan", model, rel, self.head, sha256(data), data.count(b"\n")))
        return data


def parse_band(label: str) -> tuple[int, int]:
    """'L12-16' or '12-16' -> (12, 16), both layers included."""
    lo, hi = label.removeprefix("L").split("-")
    return int(lo), int(hi)


def lens_of_sweep(sweep: str, manifest: dict, pins_text: str) -> dict[str, str]:
    """The sweep's lens, checked: J++ with the pinned sha256, a file and sha256 Zach's pins.py names."""
    if sweep.startswith(PLAIN_JLENS):
        raise ValueError(f"{sweep}: a plain J-lens run")
    source, file, want = ZACH_LENS[sweep]
    name, got = manifest["lens"]
    if name != "jpp" or got != want:
        raise ValueError(f"{sweep}: lens {name} {got[:8]}, expected jpp {want[:8]}")
    if want not in pins_text or file not in pins_text:
        raise ValueError(f"{sweep}: lens {file} {want[:8]} is not in pins.py at {ZACH_COMMIT[:7]}")
    return {"name": name, "source": source, "file": file, "sha256": want,
            "kind": "ours" if source == "local" else "published"}  # fmt: skip


def lens_of_run(run: str, manifest: dict, targets: dict[str, dict] = pins.TARGETS) -> dict[str, str]:
    """A parts run's lens, checked: J++ only, its file and sha256 the pins' for the run's target."""
    if run.startswith(PLAIN_JLENS):
        raise ValueError(f"{run}: a plain J-lens run")
    lens = manifest["lens"]
    names = [k for k in lens if k != "sha256"]
    t = targets[manifest["model"]["target"]]
    want = t.get("frozen_lens_sha256", pins.FROZEN_LENS_SHA256)
    if names != ["jpp"] or t.get("frozen_lens", "jpp") != "jpp" or lens["sha256"] != want:
        raise ValueError(f"{run}: lens {names} {lens['sha256'][:8]}, expected jpp {want[:8]}")
    source, file, _ = lens["jpp"]
    if tuple(t["lenses"]["jpp"][:2]) != (source, file):
        raise ValueError(f"{run}: lens file {file} is not the pinned {t['lenses']['jpp'][1]}")
    return {"name": "jpp", "source": source, "file": file, "sha256": want,
            "kind": "ours" if source == "local" else "published"}  # fmt: skip


def zach_n_layers(pins_text: str, target: str) -> int:
    """n_layers of a target in Zach's pins.py (its TARGETS entry, read as text: his code is not run)."""
    m = re.search(rf'^    "{re.escape(target)}": {{\n(.*?)^    }},', pins_text, re.M | re.S)
    k = re.search(r'"n_layers": (\d+)', m.group(1)) if m else None
    if k is None:
        raise ValueError(f"{target}: no n_layers in Zach's pins.py at {ZACH_COMMIT[:7]}")
    return int(k.group(1))


def checkpoint(model: dict) -> str:
    return f"{model['repo']}@{model['revision'][:7]}"


@dataclass
class Sweep:
    name: str
    manifest: dict
    summary: dict
    rows: list[dict]
    windows: list[tuple[str, int, int]]
    lens: dict[str, str]
    n_layers: int
    band: tuple[int, int] | None
    band_path: str
    middle: tuple[int, int] | None
    middle_path: str
    counts: dict[str, Any]


def check_sweep(name: str, manifest: dict, summary: dict, rows: list[dict]) -> dict[str, Any]:
    """Every field the figure reads, present; per-word item counts (no values). Raises on a missing field or count."""
    windows = manifest["bands"]
    for w in WORDS:
        if f"{w}/clean" not in summary["unedited_accuracy"]:
            raise ValueError(f"{name}: summary.json has no unedited_accuracy for {w}/clean")
        for b in windows:
            cell = summary["cells"][b][f"{w}/clean"][KNOCKOUT]
            if not all(k in cell for k in ("n", "accuracy")):
                raise ValueError(f"{name}: summary.json cells[{b}][{w}/clean][{KNOCKOUT}] lacks n or accuracy")
    missing = {k for r in rows for k in ZACH_ROW_FIELDS if k not in r}
    if missing:
        raise ValueError(f"{name}: rows.jsonl lacks {sorted(missing)}")
    if any("bridge" not in r for r in rows if r["condition"] != "none"):
        raise ValueError(f"{name}: a knock-out row without its bridge")
    none = Counter(r["family"] for r in rows if r["condition"] == "none" and r["kind"] == "clean")
    for b in windows:
        ko = Counter(
            r["family"] for r in rows if r["band"] == b and r["condition"] == KNOCKOUT and r["kind"] == "clean"
        )
        for w in WORDS:
            if not ko[w] or ko[w] != none[w] or ko[w] != summary["cells"][b][f"{w}/clean"][KNOCKOUT]["n"]:
                raise ValueError(f"{name} {b} {w}: {ko[w]} knock-out rows, {none[w]} unedited, summary n differs")
    bridges = {r["bridge"] for r in rows if "bridge" in r}
    return {"rows": len(rows), "windows": len(windows), "items": {w: none[w] for w in WORDS}, "bridges": len(bridges)}


def load_sweep(model: str, inputs: Inputs, pins_text: str) -> Sweep:
    name = SWEEP[model]
    manifest = json.loads(inputs.zach(model, f"{ABL}/{name}/manifest.json") or b"")
    summary = json.loads(inputs.zach(model, f"{ABL}/{name}/summary.json") or b"")
    raw = inputs.zach(model, f"{ABL}/{name}/rows.jsonl") or b""
    rows = [json.loads(line) for line in raw.decode().splitlines()]
    if manifest["run"] != name or KNOCKOUT not in manifest["conditions"]:
        raise ValueError(f"{name}: manifest run {manifest['run']}, conditions {manifest['conditions']}")
    counts = check_sweep(name, manifest, summary, rows)
    windows = [(b, *parse_band(b)) for b in manifest["bands"]]
    band = middle = None
    band_path = f"{ABL}/band_choice/{name}.json"
    choice = inputs.zach(model, band_path, required=False)
    if choice is not None:
        bc = json.loads(choice)
        if bc["sweep"] != name or bc["suffix"] != "" or f"L{bc['band']}" not in manifest["bands"]:
            raise ValueError(f"{band_path}: not this sweep's plain (no suffix) choice among its windows")
        band = parse_band(bc["band"])
    middle_path = f"{ABL}/c1_v2/{C1_RUN[model]}.json"
    score = inputs.zach(model, middle_path, required=False)
    if score is not None:
        middle = parse_band(json.loads(score)["middle"])
    return Sweep(name, manifest, summary, rows, windows, lens_of_sweep(name, manifest, pins_text),
                 zach_n_layers(pins_text, manifest["model"]["target"]), band, band_path, middle, middle_path,
                 counts)  # fmt: skip


@dataclass
class DanRuns:
    runs: list[str]
    manifests: dict[str, dict]
    lens: dict[str, dict[str, str]]
    model: dict
    n_layers: int
    counts: dict[str, dict[tuple[str, int], dict[str, int]]]  # run -> (set, layer) -> family -> items


def load_dan(model: str, inputs: Inputs) -> DanRuns:
    """Dan's split_depth runs for the model: files committed, columns present, J++ lens, one checkpoint, item counts."""
    cells = [c for c in SD.CELLS if c[0] == model]
    runs = list(dict.fromkeys(c[1] for c in cells))
    manifests, lens, counts = {}, {}, {}
    for run in runs:
        d = SD.SP / run
        manifests[run] = m = json.loads(inputs.dan(model, d / "manifest.json"))
        if m["model"]["target"] != SD.TARGET[model]:
            raise ValueError(f"{run}: target {m['model']['target']}, split_depth expects {SD.TARGET[model]}")
        lens[run] = lens_of_run(run, m)
        rows = [json.loads(line) for line in inputs.dan(model, d / "outcomes.jsonl").decode().splitlines()]
        missing = {k for r in rows for k in DAN_ROW_FIELDS if k not in r}
        if missing:
            raise ValueError(f"{run}: outcomes.jsonl lacks {sorted(missing)}")
        n: dict[tuple[str, int], Counter] = defaultdict(Counter)
        for r in rows:
            if r["source"] == "cf" and not r["null"] and r["part"] == "full":
                n[(r["set"], int(r["layer"]))][r["family"]] += 1
        counts[run] = {k: dict(v) for k, v in n.items()}
        for p in sorted(SD.VERDICTS.glob("*/verdict.json")):  # the verdict files split_depth checks its rates against
            if json.loads(p.read_text()).get("parts") == run:
                inputs.dan(model, p)
    for _, run, where, layers, _, _ in cells:
        for la in layers:
            if not counts[run].get((where, la), {}).get("PP"):
                raise ValueError(f"{run}: no lookups at {where}:{la}")
    models = {checkpoint(m["model"]) for m in manifests.values()}
    if len(models) != 1:
        raise ValueError(f"{model}: Dan's runs are on several checkpoints {models}")
    return DanRuns(runs, manifests, lens, manifests[runs[0]]["model"], SD.n_layers(model), counts)


@dataclass
class Panel:
    model: str
    dan: DanRuns
    zach: Sweep

    @property
    def same_checkpoint(self) -> bool:
        return checkpoint(self.dan.model) == checkpoint(self.zach.manifest["model"])


def gather(inputs: Inputs) -> dict[str, Panel]:
    pins_text = (inputs.zach("all", "src/bridge_jspace/pins.py") or b"").decode()
    inputs.dan("all", REPO / "README.md")
    out = {}
    for m in PANELS:
        p = Panel(m, load_dan(m, inputs), load_sweep(m, inputs, pins_text))
        if p.dan.n_layers != p.zach.n_layers:
            raise ValueError(f"{m}: n_layers {p.dan.n_layers} (pins) vs {p.zach.n_layers} (Zach's pins)")
        out[m] = p
    return out


def check_inputs() -> int:
    """Every input file, column, lens and checkpoint; prints schema and counts only (no value is computed)."""
    inputs = Inputs(git("rev-parse", "HEAD").strip())
    panels = gather(inputs)
    print(f"X-fig inputs: Dan @ {inputs.head[:7]} (this checkout), Zach @ {ZACH_COMMIT[:7]} ({ZACH_BRANCH}). "
          "Schema and counts only, no values.")  # fmt: skip
    for m, p in panels.items():
        z, d = p.zach, p.dan
        print(f"\n== {C.MODEL[m].name} ({m}): n_layers {d.n_layers} (pins) = {z.n_layers} (Zach's pins); checkpoints: "
              f"Dan {checkpoint(d.model)}, Zach {checkpoint(z.manifest['model'])} -> "
              f"{'same' if p.same_checkpoint else 'DIFFERENT'}")  # fmt: skip
        for run in d.runs:
            lz = d.lens[run]
            print(f"  Dan  {run}: lens {lz['name']} {lz['kind']} {lz['file']} sha256 {lz['sha256'][:12]} (= pins)")
            for (where, la), fams in sorted(d.counts[run].items()):
                used = any(c[1] == run and c[2] == where and la in c[3] for c in SD.CELLS)
                print(f"       {where}:{la} items {fams}{'' if used else '  (not a split_depth cell)'}")
        lz = z.lens
        print(
            f"  Zach {z.name}: lens {lz['name']} {lz['kind']} {lz['file']} sha256 {lz['sha256'][:12]} (in Zach's pins)"
        )
        print(f"       summary.json: unedited_accuracy and cells[window][word/clean][{KNOCKOUT}] {{n, accuracy}} for "
              f"{z.counts['windows']} windows x {len(WORDS)} words: present")  # fmt: skip
        print(f"       rows.jsonl: {z.counts['rows']} rows, columns {list(ZACH_ROW_FIELDS)} + bridge; items per word "
              f"{z.counts['items']} (unedited = every window's knock-out = summary n); {z.counts['bridges']} bridges")  # fmt: skip
        if z.band is None:
            print(f"       {z.band_path}: MISSING at {ZACH_COMMIT[:7]}")
        else:
            print(f"       {z.band_path}: present; 'band' parses and is one of the sweep's windows")
        if z.middle is None:
            print(f"       {z.middle_path}: MISSING")
        else:
            in_sweep = any((lo, hi) == z.middle for _, lo, hi in z.windows)
            same = "" if z.band is None else f"; equals the band_choice band: {z.middle == z.band}"
            print(f"       {z.middle_path}: 'middle' present; one of the sweep's windows: {in_sweep}{same}")
    print(f"\n{len(inputs.files)} input files; no plain J-lens run among them.")
    return 0


# ---------------------------------------------------------------- numbers


@dataclass
class DanPoint:
    cell: SD.Cell
    value: float  # recall minus lookup J-dependence
    lo: float
    hi: float
    n: int  # scenes


@dataclass
class ZachPoint:
    window: str
    lo: int
    hi: int
    memory: float  # memory-final loss, points
    lookup: float  # lookup-final loss, points
    gap: float  # memory - lookup, points
    ci: tuple[float, float]
    n: dict[str, int]


def scenes_of(path: Path) -> dict[tuple[str, int, str], dict[str, str]]:
    """(set, layer, family) -> item name -> scene, over split_depth's rows (source cf, not the null)."""
    out: dict[tuple[str, int, str], dict[str, str]] = defaultdict(dict)
    for line in path.read_text().splitlines():
        r = json.loads(line)
        if r["source"] == "cf" and not r["null"]:
            out[(r["set"], int(r["layer"]), r["family"])][r["name"]] = r["scene"]
    return dict(out)


def paired_diff(look: dict[str, dict], rec: dict[str, dict], look_scene: dict[str, str], rec_scene: dict[str, str],
                n_boot: int = SD.N_BOOT, seed: int = SD.SEED) -> tuple[float, float, float, int]:  # fmt: skip
    """Recall minus lookup J-dependence over the scenes both families have (one item each, both parts), and its 95%
    percentile interval resampling scenes (the pair moves together)."""

    def by_scene(items: dict[str, dict], scene: dict[str, str]) -> dict[str, tuple[bool, bool]]:
        out: dict[str, tuple[bool, bool]] = {}
        for k, v in items.items():
            if "full" in v and "not_jspace" in v:
                if scene[k] in out:
                    raise ValueError(f"two items of scene {scene[k]} in one family")
                out[scene[k]] = (v["full"], v["not_jspace"])
        return out

    lk, rc = by_scene(look, look_scene), by_scene(rec, rec_scene)
    if set(lk) != set(rc):
        raise ValueError(f"lookups and recalls cover different scenes ({len(set(lk) ^ set(rc))} differ)")
    scenes = sorted(lk)
    a = np.array([[*lk[s], *rc[s]] for s in scenes], dtype=float)  # lookup whole, without; recall whole, without
    s = a.sum(0)
    if s[0] == 0 or s[2] == 0:
        raise ValueError("no item switched by the whole change: the J-dependence is undefined")
    value = (s[2] - s[3]) / s[2] - (s[0] - s[1]) / s[0]
    b = a[np.random.default_rng(seed).integers(0, len(scenes), size=(n_boot, len(scenes)))].sum(1)
    ok = (b[:, 0] > 0) & (b[:, 2] > 0)
    d = (b[ok, 2] - b[ok, 3]) / b[ok, 2] - (b[ok, 0] - b[ok, 1]) / b[ok, 0]
    lo, hi = np.quantile(d, [0.025, 0.975])
    return float(value), float(lo), float(hi), len(scenes)


def dan_points(cells: list[SD.Cell]) -> tuple[list[DanPoint], list[str]]:
    """One point per cell with both families; the cells without recalls, as gaps."""
    out, gaps = [], []
    for c in cells:
        if "recalls" not in c.dep:
            gaps.append(f"{c.model} {c.run} {c.where}:{c.layer}: no recalls, no difference")
            continue
        path = SD.SP / c.run / "outcomes.jsonl"
        items, sc = SD.items_of(path), scenes_of(path)
        k = (c.where, c.layer)
        v, lo, hi, n = paired_diff(items[(*k, "PP")], items[(*k, "PM")], sc[(*k, "PP")], sc[(*k, "PM")])
        if abs(v - (c.dep["recalls"].value - c.dep["lookups"].value)) > 1e-9:
            raise ValueError(f"{c.run} {c.where}:{c.layer}: the paired difference is not split_depth's")
        out.append(DanPoint(c, v, lo, hi, n))
    return out, gaps


def gap_ci(items: dict[str, list[tuple[str, bool, bool]]], n_boot: int = N_BOOT_ZACH,
           seed: int = SD.SEED) -> tuple[float, float]:  # fmt: skip
    """items: word -> [(bridge, unedited correct, knock-out correct)]. 95% percentile interval of the memory-final minus
    lookup-final loss (points), resampling bridge entities: a drawn bridge brings its items of every word."""
    bridges = sorted({b for v in items.values() for b, _, _ in v})
    ix = {b: i for i, b in enumerate(bridges)}
    draws = np.random.default_rng(seed).integers(0, len(bridges), size=(n_boot, len(bridges)))
    counts = np.zeros((n_boot, len(bridges)))
    np.add.at(counts, (np.arange(n_boot)[:, None], draws), 1)
    ok = np.ones(n_boot, dtype=bool)
    loss = {}
    for w, v in items.items():
        wt = counts[:, [ix[b] for b, _, _ in v]]
        tot = wt.sum(1)
        ok &= tot > 0
        u, k = np.array([x for _, x, _ in v], dtype=float), np.array([x for _, _, x in v], dtype=float)
        with np.errstate(invalid="ignore", divide="ignore"):
            loss[w] = (wt @ u - wt @ k) / tot
    gap = 100 * ((loss["PM"] + loss["MM"]) / 2 - (loss["PP"] + loss["MP"]) / 2)
    lo, hi = np.quantile(gap[ok], [0.025, 0.975])
    return float(lo), float(hi)


def zach_points(summary: dict, rows: list[dict], windows: list[tuple[str, int, int]],
                n_boot: int = N_BOOT_ZACH) -> list[ZachPoint]:  # fmt: skip
    """Per window: memory-final and lookup-final loss (c1_v2's: unedited - paper10 accuracy per word, the two words of a
    group averaged), from summary.json, each accuracy recomputed from rows.jsonl (a mismatch raises)."""
    unedited = {(r["family"], r["id"]): bool(r["correct"]) for r in rows
                if r["condition"] == "none" and r["kind"] == "clean"}  # fmt: skip
    bridge: dict[tuple[str, str], str] = {}
    for r in rows:
        if "bridge" in r and bridge.setdefault((r["family"], r["id"]), r["bridge"]) != r["bridge"]:
            raise ValueError(f"{r['family']} {r['id']}: two bridges")
    u = {w: float(summary["unedited_accuracy"][f"{w}/clean"]) for w in WORDS}
    for w in WORDS:
        mine = statistics.mean(c for (f, _), c in unedited.items() if f == w)
        if abs(mine - u[w]) > 1e-9:
            raise ValueError(f"unedited {w}: rows and summary.json differ")
    out = []
    for label, lo, hi in windows:
        ko = {(r["family"], r["id"]): bool(r["correct"]) for r in rows
              if r["band"] == label and r["condition"] == KNOCKOUT and r["kind"] == "clean"}  # fmt: skip
        if set(ko) != set(unedited):
            raise ValueError(f"{label}: the knock-out items are not the unedited items")
        cell = {w: summary["cells"][label][f"{w}/clean"][KNOCKOUT] for w in WORDS}
        loss = {}
        for w in WORDS:
            mine = statistics.mean(c for (f, _), c in ko.items() if f == w)
            if abs(mine - cell[w]["accuracy"]) > 1e-9:
                raise ValueError(f"{label} {w}: rows and summary.json differ")
            loss[w] = 100 * (u[w] - float(cell[w]["accuracy"]))
        memory = statistics.mean(loss[w] for w in MEMORY_FINAL)
        lookup = statistics.mean(loss[w] for w in LOOKUP_FINAL)
        items = {w: [(bridge[k], unedited[k], ko[k]) for k in sorted(ko) if k[0] == w] for w in WORDS}
        out.append(ZachPoint(label, lo, hi, memory, lookup, memory - lookup, gap_ci(items, n_boot),
                             {w: int(cell[w]["n"]) for w in WORDS}))  # fmt: skip
    return out


# ---------------------------------------------------------------- drawing and writing


@dataclass
class Shown:
    """What one panel draws."""

    model: str
    name: str
    n_layers: int
    dan: list[DanPoint]
    zach: list[ZachPoint]
    split: int | None
    band: tuple[int, int] | None
    band_kind: str  # "choice" (band_choice file), "record" (c1_v2 middle, --band-of-record), "" (none)
    same_checkpoint: bool = True


def depth(layer: float, n: int) -> float:
    return 100 * layer / n


def draw_panel(ax, s: Shown) -> Any:
    """Zach on a twin axis below Dan's: band, split line, zero, Zach's squares; Dan's circles on top."""
    ax2 = ax.twinx()
    ax.set_zorder(ax2.get_zorder() + 1)
    ax.patch.set_visible(False)
    ax2.tick_params(axis="x", bottom=False, labelbottom=False)  # the shared x is ax's
    ax2.spines["right"].set_visible(True)
    for side in ("left", "top", "bottom"):
        ax2.spines[side].set_visible(False)
    if s.band is not None:
        lo, hi = depth(s.band[0], s.n_layers), depth(s.band[1], s.n_layers)
        hatch = "//" if s.band_kind == "record" else None
        ax2.axvspan(lo, hi, facecolor=C.CHANCE, edgecolor="white" if hatch else "none", hatch=hatch, lw=0, zorder=0)
    if s.split is not None:
        ax2.axvline(depth(s.split, s.n_layers), color=C.INK2, lw=1.4, zorder=1)
    ax2.axhline(0, color=C.CONTROL, lw=0.8, zorder=1)
    zs = sorted(s.zach, key=lambda z: z.lo)
    xs = [depth((z.lo + z.hi) / 2, s.n_layers) for z in zs]
    for x, z in zip(xs, zs, strict=True):
        ax2.plot([x, x], z.ci, color=ZACH, lw=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"], zorder=2, gid="ci")
    ax2.plot(xs, [z.gap for z in zs], color=ZACH, lw=1.6, marker="s", markersize=6, zorder=3, gid="mark")
    for hollow in (False, True):
        ds = sorted((d for d in s.dan if d.cell.hollow == hollow), key=lambda d: d.cell.layer)
        if not ds:
            continue
        x = [depth(d.cell.layer, s.n_layers) for d in ds]
        for xx, d in zip(x, ds, strict=True):
            ax.plot([xx, xx], [d.lo, d.hi], color=DAN, lw=C.ERRORBAR["elinewidth"], alpha=C.ERRORBAR["alpha"], zorder=3,
                    gid="ci")  # fmt: skip
        ax.plot(x, [d.value for d in ds], color=DAN, lw=1.4 if hollow else 2.4, linestyle=(0, (2, 2)) if hollow else "-",
                marker="o", markersize=8, markerfacecolor="white" if hollow else DAN, markeredgecolor=DAN,
                markeredgewidth=2.0, zorder=4, gid="mark")  # fmt: skip
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_ylim(-1.05, 1.05)
    ax.set_yticks([-1, -0.5, 0, 0.5, 1], ["−1", "−0.5", "0", "0.5", "1"])
    ax2.set_ylim(-105, 105)
    ax2.set_yticks([-100, -50, 0, 50, 100], ["−100", "−50", "0", "50", "100"])
    return ax2


def head_right(s: Shown) -> str:
    split = "no split" if s.split is None else f"split L{s.split}"
    band = {"choice": "band L{}-{}", "record": "C1's band L{}-{}"}.get(s.band_kind, "no band file")
    return f"{split} · {band.format(*(s.band or (0, 0)))}"


def figure(shown: list[Shown], checkpoints: dict[str, tuple[str, str]] | None = None) -> C.Frame:
    """The 2 x 2 panels; `checkpoints`: model -> (Dan's repo, Zach's repo) where they differ (starred, captioned)."""
    checkpoints = checkpoints or {}
    star = "; ".join(f"*{C.MODEL[m].short + ': ' if len(checkpoints) > 1 else ''}Dan {d.split('/')[-1]}, "
                     f"Zach {z.split('/')[-1]}" for m, (d, z) in checkpoints.items())  # fmt: skip
    caption = CAPTION1 + "\n" + CAPTION2 + (f" {star}." if star else "")
    fr = C.frame("full", TITLE, SUBTITLE, how=HOW, caption=caption, nrows=2, ncols=2, size=(12.0, 9.0), sharey=True,
                 left=0.085, right=0.915, wspace=0.12, hspace=0.5)  # fmt: skip
    SB.shift(fr, top=30)
    for i, (ax, s) in enumerate(zip(fr.axes, shown, strict=True)):
        ax2 = draw_panel(ax, s)
        SB.head(ax, s.name + ("*" if s.model in checkpoints else ""), head_right(s), right_size=C.NOTE)
        if i % 2 == 0:
            ax.set_ylabel("recall − lookup")
            ax2.tick_params(axis="y", labelright=False)
        else:
            ax.tick_params(axis="y", labelleft=False)
            ax2.set_ylabel("memory − lookup (pts)")
        if i // 2 == 1:
            ax.set_xlabel("depth (% of layers)")
        else:
            ax.tick_params(axis="x", labelbottom=False)
    return fr


CSV_FIELDS: tuple[str, ...] = ("model", "side", "quantity", "drawn", "x_depth_pct", "layers", "value", "ci_lo", "ci_hi", "n",
              "source_commit", "source_file", "row_key", "lens", "lens_sha256", "checkpoint", "note")  # fmt: skip


def data_rows(p: Panel, s: Shown, head: str) -> list[dict[str, Any]]:
    """Every number the panel draws (drawn=True) and the parts each is made of (drawn=False); `head`: Dan's commit."""
    out: list[dict[str, Any]] = []
    for d in s.dan:
        c, run = d.cell, d.cell.run
        lz, base = p.dan.lens[run], f"results/statement_positions/{run}/outcomes.jsonl"
        key = f"source=cf, null=false, set={c.where}, layer={c.layer}, part in (full, not_jspace)"
        common = {"model": s.model, "side": "dan", "layers": str(c.layer), "x_depth_pct": depth(c.layer, s.n_layers),
                  "source_commit": head, "source_file": base, "lens": f"jpp {lz['file']}",
                  "lens_sha256": lz["sha256"], "checkpoint": checkpoint(p.dan.model),
                  "note": "hollow: whole context" if c.hollow else ("FULL only" if c.full_only else "")}  # fmt: skip
        out.append({**common, "quantity": "recall_minus_lookup_J_dependence", "drawn": True, "value": d.value,
                    "ci_lo": d.lo, "ci_hi": d.hi, "n": d.n, "row_key": f"{key}, family PM minus PP (paired scenes)"})  # fmt: skip
        for fam, family in SD.FAMILY.items():
            dep = c.dep[fam]
            out.append({**common, "quantity": f"{fam}_J_dependence", "drawn": False, "value": dep.value, "ci_lo": dep.lo,
                        "ci_hi": dep.hi, "n": dep.n, "row_key": f"{key}, family={family}"})  # fmt: skip
    base = {"model": s.model, "source_commit": head, "lens": "", "lens_sha256": "", "checkpoint": checkpoint(p.dan.model),
            "ci_lo": None, "ci_hi": None, "n": None}  # fmt: skip
    out.append({**base, "side": "dan", "quantity": "split_layer", "drawn": s.split is not None,
                "x_depth_pct": None if s.split is None else depth(s.split, s.n_layers), "layers": str(s.split or ""),
                "value": s.split, "source_file": "README.md", "row_key": SPLIT_SOURCE,
                "note": "read after seeing the data; = split_depth.split_of" if s.split is not None else "no split"})  # fmt: skip
    z = p.zach
    zc = {"model": s.model, "side": "zach", "source_commit": ZACH_COMMIT, "lens": f"jpp {z.lens['file']}",
          "lens_sha256": z.lens["sha256"], "checkpoint": checkpoint(z.manifest["model"])}  # fmt: skip
    for q in s.zach:
        key = (f"unedited_accuracy[w/clean] and cells[{q.window}][w/clean][{KNOCKOUT}][accuracy], w in "
               f"{' '.join(WORDS)}")  # fmt: skip
        n = " / ".join(f"{w} {q.n[w]}" for w in WORDS)
        common = {**zc, "layers": f"{q.lo}-{q.hi}", "x_depth_pct": depth((q.lo + q.hi) / 2, s.n_layers),
                  "source_file": f"{ABL}/{z.name}/summary.json", "row_key": key, "n": sum(q.n.values()),
                  "note": f"items {n}; checked against rows.jsonl"}  # fmt: skip
        out.append({**common, "quantity": "memory_final_minus_lookup_final_loss_pts", "drawn": True, "value": q.gap,
                    "ci_lo": q.ci[0], "ci_hi": q.ci[1]})  # fmt: skip
        out.append({**common, "quantity": "memory_final_loss_pts", "drawn": False, "value": q.memory, "ci_lo": None,
                    "ci_hi": None})  # fmt: skip
        out.append({**common, "quantity": "lookup_final_loss_pts", "drawn": False, "value": q.lookup, "ci_lo": None,
                    "ci_hi": None})  # fmt: skip
    if s.band is not None:
        src, key = (z.band_path, "band") if s.band_kind == "choice" else (z.middle_path, "middle")
        for end, la in zip(("band_first_layer", "band_last_layer"), s.band, strict=True):
            out.append({**zc, "quantity": end, "drawn": True, "x_depth_pct": depth(la, s.n_layers), "layers": str(la),
                        "value": la, "ci_lo": None, "ci_hi": None, "n": None, "source_file": src, "row_key": key,
                        "note": "" if s.band_kind == "choice" else "band of record; its choice is not on record"})  # fmt: skip
    return out


def caption_md(panels: dict[str, Panel], shown: list[Shown], gaps: list[str]) -> str:
    lines = [f"# {TITLE}", "", "**Caption.** One panel per model with both methods. x: depth, % of the model's layers "
             "(100 × layer / n_layers). Left axis, Dan: recall minus lookup J-dependence at each cell of "
             "`scripts/figs/split_depth.py` (J-dependence = share of the switch lost when the change's J++-readable "
             "part is removed; 95% paired bootstrap over scenes). Right axis, Zach: memory-final minus lookup-final "
             "accuracy loss (points) under the top-10 J++ knock-out in each window of his held-out depth sweep, at "
             "the window's middle layer (95% bootstrap over bridge entities). Shaded: Zach's chosen band; vertical "
             "line: Dan's split layer. Both y ranges are fixed and symmetric, so the zeros align; the two scales are "
             "not comparable.", "",
             "1. Zach's band was chosen on held-out data (ctrl_v8, no prompt shared with his test set) by "
             "`scripts/choose_band.py`, with lookups excluded from the choice: it is independent of Dan's split.",
             "2. Both methods use the same J++ dictionary (the knock-out removes its top-10 directions; the "
             "J-dependence removes the change's part it can read): they are not independent in that respect.",
             "3. Dan's split was read after seeing the data: it is post hoc until X0 (the pre-registered "
             "confirmation) runs.",
             "4. The lens is J++ on every panel. Qwen3.5-122B: a J++ fit on the bf16 weights, used on the FP8 model.",
             "", "**Per panel.**"]  # fmt: skip
    if any(s.band_kind == "record" for s in shown):
        lines[4] += (" Hatched bands are the band Zach's C1 test used; no band_choice file records their choice, so "
                     "statement 1 is not checked for them.")  # fmt: skip
    for s in shown:
        p = panels[s.model]
        z = p.zach
        band = {"choice": f"`{z.band_path}` @ {ZACH_COMMIT[:7]}",
                "record": f"band of record: `{z.middle_path}` 'middle' @ {ZACH_COMMIT[:7]} (no band_choice file; "
                          "hatched)"}.get(s.band_kind, f"none: no `{z.band_path}` at {ZACH_COMMIT[:7]}")  # fmt: skip
        ck = ("one checkpoint" if p.same_checkpoint else
              f"**not one checkpoint**: Dan {checkpoint(p.dan.model)}, Zach {checkpoint(z.manifest['model'])}")  # fmt: skip
        lines.append(f"- {s.name}: Dan {', '.join(f'`{r}`' for r in p.dan.runs)}; Zach `{z.name}`; band {band}; split "
                     f"{'none' if s.split is None else f'layer {s.split}'}; {ck}; lens J++ (Dan "
                     f"{p.dan.lens[p.dan.runs[0]]['sha256'][:8]}, Zach {z.lens['sha256'][:8]}).")  # fmt: skip
    if gaps:
        lines += ["", "**Not drawn.**", *[f"- {g}" for g in gaps]]
    return "\n".join(lines) + "\n"


def build(out_root: Path = OUT, band_of_record: bool = False) -> Path:
    inputs = Inputs(git("rev-parse", "HEAD").strip())
    panels = gather(inputs)
    cells = SD.load()
    shown, gaps = [], [f"{n}: Zach's sweep only ({r}), no split_depth rows: no panel" for n, r in ZACH_ONLY]
    for m in PANELS:
        p, mine = panels[m], [c for c in cells if c.model == m]
        if SD.split_of(mine) != SPLIT[m]:
            raise ValueError(f"{m}: split_depth's split {SD.split_of(mine)}, README's {SPLIT[m]}")
        dp, g = dan_points(mine)
        gaps += g
        z = p.zach
        band, kind = (z.band, "choice") if z.band is not None else (None, "")
        if band is None and band_of_record and z.middle is not None:
            band, kind = z.middle, "record"
        if band is None:
            gaps.append(f"{m}: no band shaded (no {z.band_path} at {ZACH_COMMIT[:7]})")
        shown.append(Shown(m, C.MODEL[m].name, p.dan.n_layers, dp, zach_points(z.summary, z.rows, z.windows),
                           SPLIT[m], band, kind, p.same_checkpoint))  # fmt: skip
    fr = figure(shown, {m: (p.dan.model["repo"], p.zach.manifest["model"]["repo"]) for m, p in panels.items()
                        if not p.same_checkpoint})  # fmt: skip
    bad = C.PS.overlaps(fr.fig)
    if bad:
        raise ValueError(f"{STEM}: overlapping or clipped text: {bad[:8]}")
    d = out_root / time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    d.mkdir(parents=True, exist_ok=False)
    fr.fig.savefig(d / f"{STEM}.png", dpi=C.DPI, facecolor="white")
    fr.fig.savefig(d / f"{STEM}.svg", facecolor="white")
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_FIELDS)
    w.writeheader()
    for s in shown:
        w.writerows(data_rows(panels[s.model], s, inputs.head))
    (d / "data.csv").write_text(buf.getvalue())
    (d / "caption.md").write_text(caption_md(panels, shown, gaps))
    dirty = git("status", "--porcelain", "--untracked-files=no").strip() != ""
    manifest = {
        "script": "scripts/xfig_depth_profile.py", "written_utc": d.name,
        "dan": {"commit": inputs.head, "tracked_changes_in_checkout": dirty},
        "zach": {"commit": ZACH_COMMIT, "branch": ZACH_BRANCH},
        "band_of_record": band_of_record,
        "inputs": [asdict(f) for f in inputs.files],
        "models": {m: {"n_layers": p.dan.n_layers, "dan_checkpoint": checkpoint(p.dan.model),
                       "zach_checkpoint": checkpoint(p.zach.manifest["model"]), "same_checkpoint": p.same_checkpoint,
                       "dan_lens": p.dan.lens, "zach_lens": p.zach.lens, "split": SPLIT[m],
                       "band_source": next((s.band_kind for s in shown if s.model == m), "")}
                   for m, p in panels.items()},
        "bootstrap": {"dan": f"paired over scenes, {SD.N_BOOT} draws, seed {SD.SEED}",
                      "zach": f"over bridge entities, {N_BOOT_ZACH} draws, seed {SD.SEED}"},
        "gaps": gaps,
    }  # fmt: skip
    (d / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    C.plt.close(fr.fig)
    return d


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    ap.add_argument("--check-inputs", action="store_true", help="verify inputs; print schema and counts, no values")
    ap.add_argument("--band-of-record", action="store_true",
                    help="where no band_choice file exists, shade the c1_v2 score file's 'middle' (hatched)")  # fmt: skip
    ap.add_argument("--out", type=Path, default=OUT, help="parent folder of the new timestamped folder")
    a = ap.parse_args(argv)
    if a.check_inputs:
        return check_inputs()
    print("wrote", build(a.out, a.band_of_record))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
