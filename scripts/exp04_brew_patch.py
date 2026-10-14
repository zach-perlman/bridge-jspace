"""exp04_brew_patch: where does brew's two-step lookup carry its intermediate? Activation patching, no lens.

exp03 found that swapping the intermediate's lens direction moves no answer while swapping the start colour's does.
This run asks the lens-free question first: is there any site (layer x prompt positions) whose activation carries
the intermediate as a step, so that an edit there could redirect the second lookup? Its rates are the ceiling for
lens edits of the intermediate at the same sites.

Items and X are exp03's (the brew bank or fresh items; X = exp03's swap_target), so the rates sit next to exp03's
intermediate swaps. In the base prompt B the start S gives I = f(S) and the answer A = f(I); b = f(X).
  Counterfactual C: S's rule outputs X instead of I, and X's rule outputs c instead of b (c: a table colour not in
    {S, I, A, X, b}). C's answer is c. Only those two output words differ from B.
  Off-path control O: two off-trajectory rules (not X's) output other table colours. O's answer is A, like B's.
Patch: at one layer, B's block output at one group of positions is replaced by the source's (C or O); the rest of
B's forward runs on, and the continuation is read as in exp03. With source C:
  answer b  the patched positions carried X as the intermediate, and the second lookup ran downstream of the patch,
            on B's table (B's X rule gives b)
  answer c  they carried C's answer, or both lookups had already used C's table
  answer A  they carried nothing the answer depends on (yet)
Groups (token positions; for O the rule groups are O's own changed lines, so the control matches position for
position):
  rule_path    the path rule's line (C: S's; O: its first changed line)   early layers: positive control, answer b
  rules        both changed rule lines                                   early layers: positive control, answer c
  start_line   "The potion starts out S."
  after_start  everything after the start line (the question, the chat scaffolding, "Answer:")
  last         the final token
Layers: every block output from 0 to the J-lens's last source layer (the model's last layer is never patched).

Stages (the manifest is written before the run and is write-once):
  check [--items S]               no GPU: build every item's counterfactuals and count the token-aligned ones
  manifest [--items S] --name N
  run N
"""

import argparse
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any, cast

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson
from scripts.exp03_brew_swaps import (
    ITEM_SETS,
    MAX_NEW_TOKENS,
    answer_colour,
    regime_positions,
    render,
    spans,
    status_counts,
    swap_target,
    write_jsonl,
)

EXP = "exp04_brew_patch"
RESULTS = pins.RESULTS_DIR / EXP
SOURCES = ("cf", "off")
GROUPS = ("rule_path", "rules", "start_line", "after_start", "last")
WINDOW_GROUPS = ("start_line", "after_start", "last")
ROLES = ("A", "b", "c", "X", "I", "S")
CF_SEED, OFF_SEED = 4000, 5000
RULE = re.compile(r"^(An? (\w+) potion turns )(\w+)( when stirred\.)$", re.MULTILINE)


def rule_table(prompt: str) -> dict[str, str]:
    """{colour: the colour it turns into} from a prompt's rule lines."""
    return {m.group(2): m.group(3) for m in RULE.finditer(prompt)}


def rewrite_rules(prompt: str, outputs: dict[str, str]) -> str:
    """The prompt with each named colour's rule giving a new output colour; each named rule must occur once."""
    seen: dict[str, int] = {}

    def sub(m: re.Match) -> str:
        colour = m.group(2)
        if colour not in outputs:
            return m.group(0)
        seen[colour] = seen.get(colour, 0) + 1
        return m.group(1) + outputs[colour] + m.group(4)

    out = RULE.sub(sub, prompt)
    assert all(seen.get(c) == 1 for c in outputs), f"rules not found exactly once: {sorted(outputs)} vs {seen}"
    return out


def counterfactuals(item: dict, index: int) -> dict | None:
    """C and O for one item (None if exp03 has no X for it or no colour fits). Seeded by the item's index."""
    f, start, inter, answer = item["table"], item["start"], item["intermediates"][0], item["answer"]
    x = swap_target(item, index)
    if x is None:
        return None
    b = f[x]["stir"]
    colours = sorted(f)
    c_options = [c for c in colours if c not in (start, inter, answer, x, b)]
    off = [y for y in sorted(item["off_trajectory"]) if y != x]
    if not c_options or len(off) < 2:
        return None
    c = random.Random(CF_SEED + index).choice(c_options)
    rng = random.Random(OFF_SEED + index)
    y1, y2 = rng.sample(off, 2)
    off_outputs = {y: rng.choice([z for z in colours if z not in (y, f[y]["stir"])]) for y in (y1, y2)}
    return {
        "roles": {"A": answer, "b": b, "c": c, "X": x, "I": inter, "S": start},
        "cf": {"lines": [start, x], "outputs": {start: x, x: c}, "answer": c},
        "off": {"lines": [y1, y2], "outputs": off_outputs, "answer": answer},
    }


def line_span(text: str, colour: str) -> tuple[int, int]:
    """Character span of the colour's rule line in a rendered prompt."""
    found = [m.span() for m in RULE.finditer(text) if m.group(2) == colour]
    assert len(found) == 1, f"{len(found)} rule lines for {colour}"
    return found[0]


def group_positions(
    group: str, offsets: list[tuple[int, int]], regions: dict[str, tuple[int, int]], lines: list[tuple[int, int]]
) -> list[int]:
    """Token indices a group patches (never 0). `lines`: the source's changed rule lines, path rule first."""
    if group in ("start_line", "after_start", "last"):
        return regime_positions(group, offsets, regions)
    picked = lines[:1] if group == "rule_path" else lines
    positions = sorted({i for lo, hi in picked for i, (s, e) in enumerate(offsets) if i > 0 and s < hi and e > lo})
    assert positions, f"group {group} selects no position"
    return positions


def prepare(item: dict, index: int, tokenizer) -> dict:
    """Rendered B, C and O with their token ids, and whether they align: same length, two differing tokens each."""
    cfs = counterfactuals(item, index)
    text = render(tokenizer, item["prompt"])
    enc = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    prep: dict[str, Any] = {
        "cfs": cfs,
        "text": text,
        "ids": enc.input_ids,
        "offsets": [tuple(o) for o in enc.offset_mapping],
    }
    if cfs is None:
        prep["status"] = "no_target"
        return prep
    prep["sources"] = {}
    for source in SOURCES:
        ids = tokenizer(
            render(tokenizer, rewrite_rules(item["prompt"], cfs[source]["outputs"])), add_special_tokens=False
        ).input_ids
        same_length = len(ids) == len(enc.input_ids)
        differ = [i for i, (p, q) in enumerate(zip(ids, enc.input_ids, strict=False)) if p != q] if same_length else []
        prep["sources"][source] = {"ids": ids, "differ": differ, "aligned": same_length and len(differ) == 2}
    prep["status"] = "ok" if all(s["aligned"] for s in prep["sources"].values()) else "unaligned"
    return prep


def category(colour: str | None, roles: dict[str, str]) -> str:
    """Which role's colour the answer is (the roles' colours are distinct), else 'other', or 'none' without one."""
    if colour is None:
        return "none"
    return next((role for role, c in roles.items() if c == colour), "other")


class PatchFrom:
    """Edit for one layer: the block output at `positions` replaced by another run's (same tokens there)."""

    def __init__(self, source_h: torch.Tensor, positions: list[int]):
        self.source_h, self.positions = source_h, positions
        self.patch_ratio = float("nan")  # mean |source - h| / |h| over the patched positions, from the latest call

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        source = self.source_h[self.positions].to(h.dtype)
        rows = h[self.positions]
        self.patch_ratio = float(((source - rows).norm(dim=-1) / rows.norm(dim=-1)).mean())
        out = h.clone()
        out[self.positions] = source
        return out


def stage_check(item_set: str) -> None:
    from bridge_jspace.tokens import load_tokenizer

    tokenizer = load_tokenizer()
    counts: dict[str, int] = {}
    for index, item in enumerate(ITEM_SETS[item_set][2]()):
        status = prepare(item, index, tokenizer)["status"]
        counts[status] = counts.get(status, 0) + 1
    print(f"{item_set}: {counts} (ok = has C and O, both token-aligned with B; eligibility also needs the model)")


def stage_manifest(name: str, item_set: str, layers: list[int], why: str | None = None) -> None:
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = {
        "exp": EXP,
        "run": name,
        "kind": "patch_map",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "In brew's two-step lookup, at which layers and prompt positions does the activation carry the "
        "intermediate as a step (patching it in redirects the second lookup), and where only the answer?",
        "model": {"repo": pins.QWEN_REPO, "revision": pins.QWEN_REVISION, "dtype": "bfloat16", "attn": "sdpa"},
        "items": {
            "set": item_set,
            "file": str(ITEM_SETS[item_set][0].relative_to(pins.REPO_ROOT)),
            "sha256": ITEM_SETS[item_set][1],
        },
        "render": "as exp03: chat template, enable_thinking=False, assistant prefilled with 'Answer:'",
        "x": "exp03's swap_target (seed 0 + item index): the same X as exp03's intermediate swaps",
        "counterfactual": f"C: S's rule outputs X and X's rule outputs c, a table colour not in {{S, I, A, X, b}} "
        f"(seed {CF_SEED} + item index); C's answer is c",
        "off_path_control": f"O: two off-trajectory rules other than X's output other table colours (seed {OFF_SEED} "
        "+ item index); O's answer is A",
        "eligibility": "B answers A, C answers c and O answers A (exp03's reading: the greedy continuation's first "
        "palette colour), and C and O each tokenize like B except for exactly two tokens",
        "patch": "at one layer, B's block output at the group's positions replaced by the source's; generated tokens "
        "are not edited",
        "sources": list(SOURCES),
        "groups": list(GROUPS),
        "layers": layers,
        "outcome": "the patched continuation's first palette colour, as a role: A (B's answer), b (f(X) in B's table: "
        "X carried as the step), c (C's answer), X, I, S, other or none; plus the first generated step's "
        "log-probabilities of each role's colour",
        "decision": {
            "positive_controls": "the map is interpreted only if, at layer 0, C patched at 'rules' gives c and C "
            "patched at 'rule_path' gives b more often than O patched at the same group changes the answer at all "
            "(Wilson intervals not overlapping)",
            "window": f"per group in {list(WINDOW_GROUPS)}: the layers where C's patch gives b more often than c and "
            "more often than O's patch changes the answer (Wilson intervals not overlapping, both). An empty window: "
            "no single-layer patch of that group carries the intermediate as a step",
            "next": "lens swaps and steering inside a window are a separate manifest, set by the human after this run",
        },
        "deviations": [
            "A patch copies a whole block output, so 'carries the intermediate' means carries enough to redirect the "
            "second lookup; it does not say in which direction (that is what the lens edits test).",
            "Only one layer is patched at a time; information held at several layers or positions at once can be "
            "missed by every single-layer patch.",
            "Items where C or O does not tokenize like B outside the two changed words are dropped and counted.",
            *([why] if why else []),
        ],
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    item_file, _, load_items = ITEM_SETS[manifest["items"]["set"]]
    assert sha256_of(item_file) == manifest["items"]["sha256"], "brew items changed since the manifest"
    model = load_model()
    tokenizer: Any = model.tokenizer
    items = load_items()
    palette = sorted({c for it in items for c in it["table"]} | {it["answer"] for it in items})
    layers = manifest["layers"]
    assert max(layers) < len(cast(torch.nn.ModuleList, model.layers)) - 1, "the model's last layer is never patched"
    item_rows, outcomes = [], []
    for index, item in enumerate(items):
        prep = prepare(item, index, tokenizer)
        row: dict[str, Any] = {"name": item["name"], "status": prep["status"], "n_tokens": len(prep["ids"])}
        item_rows.append(row)
        if prep["status"] != "ok":
            continue
        cfs = prep["cfs"]
        roles = cfs["roles"]
        tokens = {role: model.concept_token(c) for role, c in roles.items()}
        row.update({"roles": roles, "cf_outputs": cfs["cf"]["outputs"], "off_outputs": cfs["off"]["outputs"]})
        ids = torch.tensor([prep["ids"]], device="cuda")
        _, clean_text, _ = model.generate(ids, MAX_NEW_TOKENS)
        row["clean_continuation"], row["clean_colour"] = clean_text, answer_colour(clean_text, palette)
        source_h = {}
        for source in SOURCES:
            source_ids = torch.tensor([prep["sources"][source]["ids"]], device="cuda")
            _, source_h[source] = model.run(source_ids, record=tuple(layers))
            _, text, _ = model.generate(source_ids, MAX_NEW_TOKENS)
            row[f"{source}_continuation"], row[f"{source}_colour"] = text, answer_colour(text, palette)
        if row["clean_colour"] != roles["A"]:
            row["status"] = "clean_wrong"
        elif row["cf_colour"] != cfs["cf"]["answer"]:
            row["status"] = "cf_wrong"
        elif row["off_colour"] != cfs["off"]["answer"]:
            row["status"] = "off_wrong"
        else:
            row["status"] = "eligible"
        if row["status"] != "eligible":
            continue
        regions = spans(item, prep["text"])
        for source in SOURCES:
            lines = [line_span(prep["text"], colour) for colour in cfs[source]["lines"]]
            for group in GROUPS:
                positions = group_positions(group, prep["offsets"], regions, lines)
                for layer in layers:
                    edit = PatchFrom(source_h[source][layer], positions)
                    logits, text, _ = model.generate(ids, MAX_NEW_TOKENS, {layer: edit})
                    logp = torch.log_softmax(logits, dim=-1)
                    colour = answer_colour(text, palette)
                    outcomes.append(
                        {
                            "name": item["name"],
                            "source": source,
                            "group": group,
                            "layer": layer,
                            "continuation": text,
                            "colour": colour,
                            "role": category(colour, roles),
                            "logp": {role: round(float(logp[t]), 3) for role, t in tokens.items()},
                            "patch_ratio": round(edit.patch_ratio, 4),
                            "n_positions": len(positions),
                        }
                    )
        print(f"{item['name']}: done ({len(outcomes)} outcomes)", flush=True)

    write_jsonl(out_dir / "items.jsonl", item_rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    rates = summarize(outcomes)
    summary = {"items": status_counts(item_rows), "rates": rates, "decision": decide(rates, layers)}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_summary_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def summarize(outcomes: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for o in outcomes:
        groups.setdefault((o["source"], o["group"], o["layer"]), []).append(o)
    rows = []
    for (source, group, layer), batch in sorted(
        groups.items(), key=lambda kv: (kv[0][0], GROUPS.index(kv[0][1]), kv[0][2])
    ):
        n = len(batch)
        count = {role: sum(o["role"] == role for o in batch) for role in (*ROLES, "other", "none")}
        rows.append(
            {
                "source": source,
                "group": group,
                "layer": layer,
                "n": n,
                "counts": count,
                "A": wilson(count["A"], n),
                "b": wilson(count["b"], n),
                "c": wilson(count["c"], n),
                "changed": wilson(n - count["A"], n),
                "mean_logp": {role: statistics.mean(o["logp"][role] for o in batch) for role in ROLES},
                "patch_ratio_median": statistics.median(o["patch_ratio"] for o in batch),
                "n_positions_median": statistics.median(o["n_positions"] for o in batch),
            }
        )
    return rows


def decide(rates: list[dict], layers: list[int]) -> dict:
    """The manifest's decision rule: positive controls at layer 0, then each window group's layers."""
    at = {(r["source"], r["group"], r["layer"]): r for r in rates}
    if not at:
        return {"positive_controls": None, "windows": None}
    above = lambda w, v: w[1] > v[2]  # noqa: E731 Wilson intervals not overlapping, w above v
    first = layers[0]
    controls = {
        "rules -> c": above(at["cf", "rules", first]["c"], at["off", "rules", first]["changed"]),
        "rule_path -> b": above(at["cf", "rule_path", first]["b"], at["off", "rule_path", first]["changed"]),
    }
    windows = {
        group: [
            layer
            for layer in layers
            if above(at["cf", group, layer]["b"], at["cf", group, layer]["c"])
            and above(at["cf", group, layer]["b"], at["off", group, layer]["changed"])
        ]
        for group in WINDOW_GROUPS
    }
    return {"positive_controls": controls, "interpreted": all(controls.values()), "windows": windows}


def write_summary_md(path: Path, run: str, summary: dict) -> None:
    pct = lambda w: f"{100 * w[0]:.0f}%"  # noqa: E731
    d = summary["decision"]
    lines = [
        f"# {EXP} / {run}",
        "",
        "Items: " + ", ".join(f"{k} {v}" for k, v in summary["items"].items()),
        "",
        f"Positive controls (layer {min(r['layer'] for r in summary['rates']) if summary['rates'] else '-'}): "
        f"{d['positive_controls']}; map interpreted: {d.get('interpreted')}",
        f"Windows (C gives b above c and above O's changed rate): {d['windows']}",
        "",
        "Rates by layer: C's patch giving A / b / c / X, and O's patch changing the answer (Wilson CIs in summary.json).",
    ]
    by = {(r["source"], r["group"], r["layer"]): r for r in summary["rates"]}
    layers = sorted({r["layer"] for r in summary["rates"]})
    for group in GROUPS:
        lines += [
            "",
            f"## {group}",
            "",
            "| layer | n | A | b | c | X | O changed | patch ratio |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for layer in layers:
            r, o = by.get(("cf", group, layer)), by.get(("off", group, layer))
            if r is None:
                continue
            x = r["counts"]["X"] / r["n"]
            lines.append(
                f"| {layer} | {r['n']} | {pct(r['A'])} | {pct(r['b'])} | {pct(r['c'])} | {100 * x:.0f}% | "
                f"{pct(o['changed']) if o else ''} | {r['patch_ratio_median']:.3f} |"
            )
    path.write_text("\n".join(lines) + "\n")


def parse_layers(spec: str) -> list[int]:
    """'0-62' -> 0..62 inclusive; '0-62:2' -> 0, 2, .., 62; '0,4,8' -> those."""
    if "-" in spec:
        span, _, step = spec.partition(":")
        lo, hi = map(int, span.split("-"))
        return list(range(lo, hi + 1, int(step or 1)))
    return [int(s) for s in spec.split(",")]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["check", "manifest", "run"])
    parser.add_argument("target", nargs="?", help="run: the run's folder name")
    parser.add_argument("--name", help="manifest: the run's folder name")
    parser.add_argument("--items", default="bank", choices=list(ITEM_SETS), help="bank (WorkspaceBench) or fresh")
    parser.add_argument("--layers", default="0-62", help="manifest: block outputs to patch: 0-62, 0-62:2 or 0,8,16")
    parser.add_argument("--why", help="manifest: who chose this run's settings and why (added to the deviations)")
    args = parser.parse_args()
    if args.stage == "check":
        stage_check(args.items)
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        stage_manifest(args.name, args.items, parse_layers(args.layers), args.why)
    else:
        assert args.target, "run needs the run's folder name"
        stage_run(args.target)
