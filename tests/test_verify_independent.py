"""scripts/verify_independent.py on a planted repo: it recomputes the item set, the conflict test's extra losses and the
routes shares from raw rows, finds a README number that differs, and imports no pipeline or review code."""

import ast
import json
from pathlib import Path

from scripts import verify_independent as V

SCRIPT = Path(V.__file__)


def put(root: Path, rel: str, rows) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rows) if rel.endswith(".json") else "".join(json.dumps(r) + "\n" for r in rows))


def comp(scene: str, ok: bool = True) -> list[dict]:
    return [{"scene": scene, "rendering": "chat", "reader": w, "variant": v, "right": ok, "read_right": ok}
            for w in ("PP", "PM") for v in ("org", "alt")]  # fmt: skip


def x0_row(scene: str, w: str, arm: str, sw: int, layer: int = 12) -> dict:
    d = ("jpp", 25, "signed") if arm in ("no_part", "no_rand") else ("-", 0, "-")
    return {"scene": scene, "rendering": "chat", "layer": layer, "reader": w, "dict": d[0], "k": d[1], "omp": d[2],
            "arm": arm, "switched": sw}  # fmt: skip


def plant(root: Path, readme_lookup: str = "0.25", readme_route: str = "0.50") -> None:
    # conflict test: 5 cases, s2 ineligible, N = 4 -> items s0 s1 s3 s4; lookup: whole switches 4, without the lens part
    # 2, without the random part 3 -> (3 - 2) / 4 = 0.25; recall: whole 4, part 0, random 4 -> 1.0; gap 0.75
    run = "results/x0_necessity/qwen35_9b_x0_necessity"
    scenes = [f"s{i}" for i in range(5)]
    put(root, f"{run}/manifest.json", {"predicted": 12, "n": {"items": 4}})
    put(root, f"{run}/cases.jsonl", [{"scene": s, "rendering": "chat"} for s in scenes])
    put(root, f"{run}/competence.jsonl", [r for s in scenes for r in comp(s, s != "s2")])
    rows = []
    for i, s in enumerate(["s0", "s1", "s3", "s4"]):
        rows += [
            x0_row(s, "PP", "whole", 1),
            x0_row(s, "PP", "no_part", int(i < 2)),
            x0_row(s, "PP", "no_rand", int(i < 3)),
        ]
        rows += [x0_row(s, "PM", "whole", 1), x0_row(s, "PM", "no_part", 0), x0_row(s, "PM", "no_rand", 1)]
        rows += [x0_row(s, "PP", "whole", 0, layer=6)]  # another layer: ignored
    put(root, f"{run}/outcomes.jsonl", rows)
    # routes: 2 C2 scenes; whole: c0 position (by top id), c1 identity; the stored label of c1 is wrong on purpose
    rr = "results/x6_routes/qwen35_9b_x6_routes"
    rt = {"identity": 11, "position": 12, "value": 13, "original": 14}
    put(root, f"{rr}/manifest.json", {"n_per_condition": 2})
    put(root, f"{rr}/cases.jsonl", [{"scene": s, "condition": "C2", "route_tokens": rt} for s in ("c0", "c1")])
    put(root, f"{rr}/competence.jsonl", [r for s in ("c0", "c1") for r in comp(s)])
    put(root, f"{rr}/outcomes.jsonl", [
        {"scene": "c0", "condition": "C2", "reader": "PP", "arm": "whole", "top": 12, "route": "position"},
        {"scene": "c1", "condition": "C2", "reader": "PP", "arm": "whole", "top": 11, "route": "position"}])  # fmt: skip
    put(root, "docs/x0_numbers.json", {
        "lk_excess_9b": {"text": "0.25 [0.1, 0.4]", "source": f"{run}/outcomes.jsonl"},
        "rc_excess_9b": {"text": "1.00", "source": f"{run}/outcomes.jsonl"},
        "contrast_9b": {"text": "0.75", "source": f"{run}/outcomes.jsonl"},
        "rt_C2_whole_identity_9b": {"text": "0.50", "source": f"{rr}/verdict-1/verdict.json"},
        "rt_C2_whole_position_9b": {"text": "0.50", "source": f"{rr}/verdict-1/verdict.json"},
        "rtk_C2_keep_alf_position_9b": {"text": "0.00", "source": f"{rr}/verdict-1/verdict.json"}})  # fmt: skip
    (root / "figures/story").mkdir(parents=True)
    (root / "figures/story/data.csv").write_text("figure,model,quantity,value,lo,hi,n,source\n")
    (root / "docs/depth").mkdir(parents=True)
    (root / "docs/depth/README.md").write_text(
        f"lookup {readme_lookup} [0.1, 0.4]<!-- src: docs/x0_numbers.json | lk_excess_9b --> | recall "
        f"1.00<!-- src: docs/x0_numbers.json \\| rc_excess_9b --> | position {readme_route}<!-- src: docs/x0_numbers.json | "
        "rt_C2_whole_position_9b -->\n"
    )


def test_recomputes_the_planted_numbers_and_they_match(tmp_path):
    plant(tmp_path)
    rep = V.main(["--models", "9b", "--out", "out.json"], root=tmp_path)
    m = rep["models"]["9b"]
    assert m["conflict"]["items"] == {"recomputed": 4, "in outcomes": 4, "same": True}
    assert m["conflict"]["lookup"]["value"] == 0.25 and m["conflict"]["recall"]["value"] == 1.0
    assert abs(m["conflict"]["gap"] - 0.75) < 1e-12
    assert m["routes"]["shares"]["whole"]["position"] == 0.5 and m["routes"]["shares"]["whole"]["identity"] == 0.5
    # the route is read from the top token, not the stored label (c1's label is wrong): one disagreement counted
    assert m["routes"]["route label from the top token agrees with the stored label"] == {"agree": 1, "differ": 1}
    assert rep["summary"]["mismatch"] == 0 and json.loads((tmp_path / "out.json").read_text())["summary"]["match"] >= 5


def test_a_readme_number_that_differs_is_reported(tmp_path):
    plant(tmp_path, readme_lookup="0.31", readme_route="0.49")
    rep = V.main(["--models", "9b", "--out", "out.json"], root=tmp_path)
    bad = {r["quantity"] for r in rep["rows"] if r["status"] == "mismatch"}
    assert bad == {"conflict: lookup, switches lost beyond a random part", "routes C2, whole: position share"}
    assert all(r["vs source"] == "match" for r in rep["rows"])  # the source is right, the README shows another number


def test_an_item_set_that_differs_is_reported(tmp_path):
    plant(tmp_path)
    run = tmp_path / "results/x0_necessity/qwen35_9b_x0_necessity"
    (run / "competence.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for s in [f"s{i}" for i in range(5)] for r in comp(s))
    )
    rep = V.main(["--models", "9b", "--out", "out.json"], root=tmp_path)
    assert rep["models"]["9b"]["conflict"]["items"]["same"] is False  # s2 eligible now: the first 4 are s0-s3


def test_imports_no_pipeline_or_review_code():
    tree = ast.parse(SCRIPT.read_text())
    mods = [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
    mods += [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module]
    assert set(mods) <= {"__future__", "argparse", "csv", "json", "re", "sys", "collections", "pathlib"}, mods
