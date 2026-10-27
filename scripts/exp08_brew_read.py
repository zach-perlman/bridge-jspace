"""exp08_brew_read: can the lens read brew's intermediate where the step is carried?

exp04 found brew's intermediate carried after the start line at layers 36-50; exp07 found a code for it there, fit on
other items, that writes the step and is nearly orthogonal to the lens direction v_X - v_I. This run asks whether the
lenses read the intermediate at those positions at all, with part A's protocol (exp11, exp12): at each position after
the start line and each layer, is I the top-1 among the 12 palette colours, against a distractor colour equally
present in the prompt (X, exp03's swap target: a rule-table colour off the S -> I -> A path)?

  readers  J++, the J-lens, the logit lens (part A's baseline), and exp07's code as a lens-free linear reader at the
           window layers (colour k's score at a position: <h - w_0, E_I[k]> - |E_I[k]|^2 / 2, without the item's S, A)
  roles    I (the intermediate), X (the distractor), S (the start colour, on the line before), A (the answer)
  items    exp07 code_v1's eligible items (154 fresh, 82 bank); clean prompts only, no edits
  layers   every second layer, 0-62; the decision reads the window (36-50)

Stages (the manifest is written before the run and is write-once):
  manifest --name N --why "..."
  run N
"""

import argparse
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.run_switches import switches
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from scripts.exp03_brew_swaps import ITEM_SETS, write_jsonl
from scripts.exp04_brew_patch import counterfactuals
from scripts.exp07_step_code import CODE_FILE, COLOURS, TEST_SETS, WINDOW, tokenized

EXP = "exp08_brew_read"
RESULTS = pins.RESULTS_DIR / EXP
EXP07_RUN = pins.RESULTS_DIR / "exp07_step_code" / (pins.RUN_PREFIX + "code_v1")
LAYERS = tuple(range(0, pins.N_LAYERS - 1, 2))  # every second layer below the final block (Qwen: 0-62)
LENSES = tuple(lens for lens in ("jpp", "jlens") if lens in pins.LENS_SOURCES)  # Gemma: J++ only (no J-lens fit)
READERS = (*LENSES, "logit", "code")
ROLES = ("I", "X", "S", "A")
N_BOOT, BOOT_SEED = 2000, 0


def read_jsonl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f]


def colour_ranks(scores: torch.Tensor, roles: dict[str, str]) -> dict[str, list[int]]:
    """scores [P, 12] over COLOURS: per role, its rank among the colours at each position (0 = top)."""
    out = {}
    for role in ROLES:
        k = COLOURS.index(roles[role])
        out[role] = (scores > scores[:, k : k + 1]).sum(dim=1).tolist()
    return out


def code_scores(w: torch.Tensor, h: torch.Tensor) -> torch.Tensor:
    """exp07's code as a reader: [P, 12] scores <h - w_0, E_I[k]> - |E_I[k]|^2 / 2 per position (w [f, P, d])."""
    codes = w[1 + len(COLOURS) : 1 + 2 * len(COLOURS)]  # [12, P, d]
    return (torch.einsum("pd,kpd->pk", h - w[0], codes) - 0.5 * codes.pow(2).sum(-1).T).float()


def stage_manifest(name: str, why: str) -> None:
    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    exp07_summary = json.loads((EXP07_RUN / "summary.json").read_text())
    manifest = {
        "exp": EXP,
        "run": name,
        "kind": "brew_read",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": f"After the start line, where brew's step is carried (layers {WINDOW[0]}-{WINDOW[-1]}), do the lenses read the "
        "intermediate I, against a distractor colour equally present in the prompt?",
        "why": why,
        "model": pins.model_pin(),
        "switches": switches(),
        "items": {
            "source": "exp07_step_code/code_v1 items.jsonl, status eligible (exp04's eligibility)",
            "sha256": sha256_of(EXP07_RUN / "items.jsonl"),
            "sets": {s: ITEM_SETS[s][1] for s in TEST_SETS},
        },
        "positions": "after_start (the 21 tokens after the start line, as exp04 and exp07)",
        "layers": list(LAYERS),
        "window": list(WINDOW),
        "readers": {
            **{lens: list(pins.LENS_SOURCES[lens]) for lens in LENSES},
            "logit": "the final norm and unembedding applied to the block output (part A's baseline)",
            "code": "exp07's code (window layers only): colour k scores <h - w_0, E_I[k]> - |E_I[k]|^2 / 2 at each "
            "position, without the item's S and A",
        },
        "code": {
            "file": str(CODE_FILE.relative_to(pins.REPO_ROOT)),
            "sha256": exp07_summary["caches"]["code"]["sha256"],
        },
        "readout": "each reader's scores for the 12 palette colours' concept tokens at each position; a role is read "
        "at a position if its colour is the top-1 of the 12 (part A's 'top-1 among the candidates')",
        "roles": {
            "I": "the intermediate",
            "X": "the distractor: exp03's swap target, a rule-table colour off the path",
            "S": "the start colour",
            "A": "the answer",
        },
        "decision": {
            "read_score": "per item, the share of (window layer, position) cells at which the role's colour is top-1; "
            "differences are paired bootstraps over items (95%)",
            "reads": "a reader reads the intermediate at the window if I's read score exceeds X's (CI above 0), on the "
            "fresh items (J++ primary; the J-lens, the logit lens and the code secondary; the bank items replicate)",
            "reader_works": f"positive control: a lens reader is interpreted only if, at the last position at layer {LAYERS[-1]}, A "
            "is top-1 for more items than X (Wilson intervals not overlapping)",
        },
        "deviations": [
            "X is exp03's swap target, so the distractor is the colour the lens edits moved toward; any rule-table "
            "colour is equally present in the prompt.",
            "Top-1 among 12 colours, not among the vocabulary; the vocabulary rank of I is kept for reference.",
        ],
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "reads.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    assert sha256_of(EXP07_RUN / "items.jsonl") == manifest["items"]["sha256"], "exp07's items changed"
    assert sha256_of(CODE_FILE) == manifest["code"]["sha256"], "exp07's code cache changed"
    eligible = {(r["set"], r["name"]) for r in read_jsonl(EXP07_RUN / "items.jsonl") if r["status"] == "eligible"}
    model = load_model()
    tokenizer: Any = model.tokenizer
    colour_tok = torch.tensor([model.concept_token(c) for c in COLOURS], device="cuda")
    cases = []
    for set_name in TEST_SETS:
        assert sha256_of(ITEM_SETS[set_name][0]) == manifest["items"]["sets"][set_name], f"{set_name} items changed"
        for index, item in enumerate(ITEM_SETS[set_name][2]()):
            if (set_name, item["name"]) not in eligible:
                continue
            cfs = counterfactuals(item, index)
            assert cfs is not None
            ids, positions = tokenized(tokenizer, item)
            _, rec = model.run(torch.tensor([ids], device="cuda"), record=LAYERS)
            h = {layer: rec[layer][positions] for layer in LAYERS}
            cases.append({"set": set_name, "name": item["name"], "roles": cfs["roles"], "h": h})
            del rec
    print(f"{len(cases)} items", flush=True)
    rows: list[dict] = []

    def add(case: dict, reader: str, layer: int, scores: torch.Tensor, vocab: torch.Tensor | None) -> None:
        row = {"set": case["set"], "name": case["name"], "reader": reader, "layer": layer}
        row["colour_rank"] = colour_ranks(scores, case["roles"])
        if vocab is not None and layer in WINDOW:  # the vocabulary rank of I, kept at the window only
            tok = model.concept_token(case["roles"]["I"])
            row["vocab_rank_I"] = (vocab > vocab[:, tok : tok + 1]).sum(dim=1).tolist()
        rows.append(row)

    for case in cases:
        for layer in LAYERS:
            logits = model.unembed(case["h"][layer])
            add(case, "logit", layer, logits[:, colour_tok], logits)
    code = torch.load(CODE_FILE, map_location="cpu", weights_only=True)
    for layer in WINDOW:
        w = code["w"][layer].to("cuda")
        for case in cases:
            add(case, "code", layer, code_scores(w, case["h"][layer]), None)
    for lens_name in LENSES:
        lens = JLens(model, lens_name)
        for case in cases:
            for layer in LAYERS:
                logits = lens.readout(case["h"][layer], layer)
                add(case, lens_name, layer, logits[:, colour_tok], logits)
        print(f"{lens_name}: done", flush=True)
        del lens
        torch.cuda.empty_cache()
    write_jsonl(out_dir / "reads.jsonl", rows)
    summary = summarize(rows)
    summary["items"] = {s: sum(c["set"] == s for c in cases) for s in TEST_SETS}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_summary_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def read_scores(rows: list[dict], role: str, layers: tuple[int, ...]) -> dict[str, float]:
    """Per item, the share of (layer, position) cells at which the role's colour is top-1."""
    cells: dict[str, list[bool]] = {}
    for r in rows:
        if r["layer"] in layers:
            cells.setdefault(r["name"], []).extend(rank == 0 for rank in r["colour_rank"][role])
    return {n: sum(v) / len(v) for n, v in cells.items()}


def summarize(rows: list[dict]) -> dict:
    out: dict[str, Any] = {"sets": {}}
    for set_name in TEST_SETS:
        per_reader: dict[str, Any] = {}
        for reader in READERS:
            mine = [r for r in rows if r["set"] == set_name and r["reader"] == reader]
            if not mine:
                continue
            layers = sorted({r["layer"] for r in mine})
            by_layer = {
                role: {layer: statistics.mean(read_scores(mine, role, (layer,)).values()) for layer in layers}
                for role in ROLES
            }
            window = {role: read_scores(mine, role, WINDOW) for role in ROLES}
            names = sorted(window["I"])
            diff = paired_bootstrap_diff(
                [window["I"][n] for n in names], [window["X"][n] for n in names], N_BOOT, BOOT_SEED
            )
            n_positions = len(mine[0]["colour_rank"]["I"])
            by_position = {
                layer: [
                    statistics.mean(r["colour_rank"]["I"][p] == 0 for r in mine if r["layer"] == layer)
                    for p in range(n_positions)
                ]
                for layer in layers
            }
            entry: dict[str, Any] = {
                "window_read_score": {role: statistics.mean(v.values()) for role, v in window.items()},
                "I - X": diff,
                "reads": diff[1] > 0,
                "by_layer": by_layer,
                "I_by_position": by_position,
            }
            if reader != "code":
                last = [r for r in mine if r["layer"] == LAYERS[-1]]
                k_a = sum(r["colour_rank"]["A"][-1] == 0 for r in last)
                k_x = sum(r["colour_rank"]["X"][-1] == 0 for r in last)
                a_w, x_w = wilson(k_a, len(last)), wilson(k_x, len(last))
                entry["positive_control"] = {
                    f"A last position L{LAYERS[-1]}": a_w,
                    f"X last position L{LAYERS[-1]}": x_w,
                }
                entry["works"] = a_w[1] > x_w[2]
                vocab = [rank for r in mine if "vocab_rank_I" in r for rank in r["vocab_rank_I"]]
                entry["I_vocab_rank_median_window"] = statistics.median(vocab)
            per_reader[reader] = entry
        out["sets"][set_name] = per_reader
    return out


def write_summary_md(path: Path, run: str, summary: dict) -> None:
    pts = lambda d: f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"  # noqa: E731
    lines = [f"# {EXP} / {run}", "", "Items: " + ", ".join(f"{k} {v}" for k, v in summary["items"].items()), ""]
    for set_name, readers in summary["sets"].items():
        lines += [
            f"## {set_name} items",
            "",
            f"| reader | works (A at L{LAYERS[-1]}) | I | X | S | A | I - X (pts) | reads I |",
        ]
        lines += ["|---|---|---|---|---|---|---|---|"]
        for reader, e in readers.items():
            s = e["window_read_score"]
            works = "" if "works" not in e else ("yes" if e["works"] else "NO")
            lines.append(
                f"| {reader} | {works} | {100 * s['I']:.0f}% | {100 * s['X']:.0f}% | {100 * s['S']:.0f}% | "
                f"{100 * s['A']:.0f}% | {pts(e['I - X'])} | {'yes' if e['reads'] else 'no'} |"
            )
        lines += [
            "",
            "Window read score: per item, the share of (window layer, position) cells with the colour top-1.",
            "",
        ]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["manifest", "run"])
    parser.add_argument("target", nargs="?", help="run: the run's folder name")
    parser.add_argument("--name", help="manifest: the run's folder name")
    parser.add_argument("--why", help="manifest: who chose this run and why")
    args = parser.parse_args()
    if args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why)
    else:
        assert args.target, "run needs the run's folder name"
        stage_run(args.target)
