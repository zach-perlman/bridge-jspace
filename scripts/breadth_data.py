"""breadth_data: the breadth half's result readers, moved out of scripts/fig_neel.py (Zach, 2026-10-26) so that
scripts/report_breadth.py (docs/breadth/data.csv) does not depend on a figure script. No plotting here.

Every reader returns what fig_neel drew, from the run files under results/ (through scripts/results_digest.py's
readers where they exist)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from scripts import results_digest as D  # noqa: E402

RES, DATA = ROOT / "results", ROOT / "data" / "tasks_v2"
A2 = RES / "ablate_v2"
SET = "jsuite_v2_test_chat"
MOD = {m[0]: m for m in D.MODELS}
HEAD = ["Qwen3.6-27B", "Qwen3.5-9B", "Nemotron-3.5-Lightning"]
PREFIX = {"Qwen3.6-27B": "", "Qwen3.5-9B": "qwen35_9b_", "Nemotron-3.5-Lightning": "nem35l_", "Ministral-3-14B": "min14_",
          "DeepSeek-V4-Flash": "dsv4f_", "Nemotron-3.5-Bolt": "nem35b_", "Muse-Glimmer-30B": "muse30_", "Qwen3.5-122B": "qwen35_122b_"}  # fmt: skip
# the 15 words of the facts module (how the bridge is reached x where the answer comes from), as ablate_v2 reads them
WORDS = ["PP", "PK", "PM", "PA", "PN", "MP", "MK", "MM", "MA", "MN", "TP", "TK", "TM", "TA", "TN"]
RELATIONS = ["countries", "languages", "people", "cities", "companies", "landmarks", "dishes", "animals"]


def load(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def score(run: str) -> dict:
    return load(RES / "ablate_v2" / "jsuite2_score" / f"{run}.json") or {}


def cell(run: str, key: str, contrast: str = "M-K"):
    c = score(run).get("facts", {}).get(key)
    return (c["contrasts"][contrast]["diff"], c["contrasts"][contrast]["ci"]) if c and contrast in c["contrasts"] else None


# ---- F02 readable: the bridge readout per model
READOUT = [("Qwen3.6-27B", "bridge_readout_v2_v1"), ("Qwen3.5-9B", "qwen35_9b_bridge_readout_v2_v1"),
           ("Nemotron-3.5-Lightning", "nem35l_bridge_readout_v2_v1"), ("Ministral-3-14B", "min14_bridge_readout_v2_v1"),
           ("DeepSeek-V4-Flash", "dsv4f_bridge_readout_v2_v1"), ("Nemotron-3.5-Bolt", "nem35b_bridge_readout_v2_v1")]  # fmt: skip

# ---- F06 where: depth profiles (dev) and position runs (test)
PROFILES = [("Qwen3.6-27B", "jsuite_v2_dev_chat_profile_rs40_cand2_v1"), ("Qwen3.5-9B", "qwen35_9b_jsuite_v2_dev_chat_profile_rs40_cand2_v1"),
            ("Nemotron-3.5-Lightning", "nem35l_jsuite_v2_dev_chat_profile_rs40_cand2_v1"), ("Ministral-3-14B", "min14_jsuite_v2_dev_chat_profile_rs40_cand2_v1"),
            ("Nemotron-3.5-Bolt", "nem35b_jsuite_v2_dev_chat_profile_cand2_v1")]  # fmt: skip
# the profile that gives each readout model's layer count (DeepSeek has no rs40 profile)
LAYER_COUNT = {**dict(PROFILES), "DeepSeek-V4-Flash": "dsv4f_jsuite_v2_dev_chat_profile_cand2_v1"}
# position runs: (label, all-token run, {mode: run})
POSITIONS = [
    ("Qwen 27B, mid L32-40", "jsuite_v2_test_chat_ko_cand2_v1", {m: f"jsuite_v2_test_chat_ko_cand2_pos{m}_v1" for m in ("bridge", "context", "question")}),
    ("Qwen 9B, mid L12-16", "qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1", {m: f"qwen35_9b_jsuite_v2_test_chat_ko_cand2_pos{m}_v1" for m in ("bridge", "context", "question")}),
    ("Lightning, mid L27-33", "nem35l_jsuite_v2_test_chat_ko_cand2_v1", {m: f"nem35l_jsuite_v2_test_chat_ko_cand2_pos{m}_v1" for m in ("bridge", "context", "question")}),
    ("Qwen 27B, late L52-60", None, {m: f"jsuite_v2_test_chat_ko_cand2_L52-60_pos{m}_v1" for m in ("bridge", "question")}),
    ("Ministral, late L32-37", "min14_jsuite_v2_test_chat_ko_cand2_v1", {m: f"min14_jsuite_v2_test_chat_ko_cand2_L32-37_pos{m}_v1" for m in ("bridge", "question")}),
    ("Qwen 122B, late L39-45", "qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1", {m: f"qwen35_122b_jsuite_v2_test_chat_ko_cand2_pos{m}_v1" for m in ("bridge", "context", "question")}),
]  # fmt: skip

# ---- F10 dose (amendment 54)
DOSE54 = [("Qwen3.6-27B", "", "L32-40"), ("Qwen3.5-9B", "qwen35_9b_", "L12-16"), ("Nemotron-3.5-Lightning", "nem35l_", "L27-33"),
          ("Ministral-3-14B", "min14_", "L32-37"), ("Nemotron-3.5-Bolt", "nem35b_", "L42-53"), ("DeepSeek-V4-Flash", "dsv4f_", "L18-23"),
          ("Muse-Glimmer-30B", "muse30_", "L36-42")]  # fmt: skip
KS = [1, 3, 10, 30, 100, 300]


def dose_data(m: str, pre: str, band: str) -> list[dict] | None:
    run = f"{pre}{SET}_ko_cand2_{band}_dose54_s150_v1"
    sc = score(run).get("facts")
    size = load(RES / "removal_size" / f"{pre}removal_size_{band}_dose54_v1" / "summary.json")
    soft = load(A2 / "soft_score" / f"{run}.json") or {}
    if not sc or not size:
        return None
    med = lambda key: sorted(v[key] for v in size["median_share"].values())[len(size["median_share"]) // 2] * 100  # noqa: E731
    out = []
    for k in KS:
        c = sc.get(f"top{k}/start=all")
        if not c:
            continue
        g = lambda cond: (sc.get(f"{cond}/start=all") or {}).get("contrasts", {}).get("M-K", {}).get("diff")  # noqa: E731
        so = soft.get(f"top{k}", {})
        out.append({"k": k, "share": med(f"jlens_top{k}"), "mk": c["contrasts"]["M-K"]["diff"], "ci": c["contrasts"]["M-K"]["ci"],
                    "K": c["loss"]["K"], "rot": g(f"top{k}_rot"), "pc": g(f"top{k}_pcasize"), "u": g(f"unembed{k}"),
                    "smk": so.get("soft_M-K"), "sK": so.get("soft", {}).get("K"), "spc": soft.get(f"top{k}_pcasize", {}).get("soft_M-K")})  # fmt: skip
        r = out[-1]
        ctrl = [v for v in (r["rot"], r["pc"]) if v is not None]
        r["exc"] = r["mk"] - max(ctrl) if ctrl else None
    return out


def dose_readings(d: list[dict]) -> dict:
    """Amendment 54's readings (as written) and note 1's secondary readings."""
    cls = lambda k: "concentrated" if k <= 10 else "distributed" if k >= 100 else "intermediate"  # noqa: E731
    lim = next((r["k"] for r in d if r["K"] > 10 or (r["pc"] is not None and r["pc"] > r["mk"] / 2)), None)
    under = [r for r in d if lim is None or r["k"] < lim] or d[:1]
    top = max(r["mk"] for r in under)
    kstar = next(r["k"] for r in under if r["mk"] >= 0.9 * top)
    eu = [r for r in under if r["exc"] is not None]
    etop = max(r["exc"] for r in eu) if eu else None
    ekstar = next((r["k"] for r in eu if r["exc"] >= 0.9 * etop), None) if eu else None
    plim = next((r["k"] for r in d if r["sK"] is not None and r["sK"] > 10), None)
    return {"limit": lim, "kstar": kstar, "cls": cls(kstar), "ekstar": ekstar, "ecls": cls(ekstar) if ekstar else None, "plim": plim}


# ---- F04 settings: each dataset's own contrast
def c1gap(run: str):
    s = load(A2 / "c1_v2" / f"{run}.json")
    return (100 * s["rule"]["gap"], None) if s else None


def c1unembed(run: str):
    s = load(A2 / "c1_specificity" / f"{run}.json")
    if not s:
        return None
    b = next(iter(s["bands"].values()))
    return (100 * b["unembed10"]["gap"], None) if "unembed10" in b else None


def natplus(run: str, cond: str = "paper10", grp: str = "all/all"):
    s = load(A2 / "natplus_split" / f"{run}.json")
    c = (s or {}).get("cells", {}).get(f"{grp}/{cond}")
    return (c["gap"], c.get("gap_ci")) if c else None


def v1(run: str, cond: str = "paper10"):
    s = load(A2 / "jsuite_score" / f"{run}.json")
    c = (s or {}).get("cells", {}).get(f"all/{cond}")
    return (c["contrasts"]["M-P"]["diff"], c["contrasts"]["M-P"]["ci"]) if c else None


def v2(run: str, cond: str = "paper10"):
    x = D.mk(run, cond)
    return (x["d"], x["ci"]) if x else None
