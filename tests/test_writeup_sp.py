"""The write-up's styles-plot figures (figkit/writeup_sp.py): the vocabulary's models and templates, the status registry
(written in styles-plot's schema, current, loadable), every figure saves strict, and one data key prints one string
across them."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import pytest
import styles_plot as sp

from bridge_jspace import figdata as FD
from bridge_jspace import palette as P
from bridge_jspace.figkit import writeup_sp as SP
from scripts import status_registry as SR

REPO = Path(__file__).resolve().parents[1]
V = sp.load(REPO / "plotstyle.toml")


def test_models_in_order():
    assert [(e.key, e.name) for e in V.entities("models")][: len(P.MODELS)] == list(P.MODELS)
    assert [e.name for e in V.entities("models")][len(P.MODELS) :] == list(P.BREADTH_ONLY)


def test_read_aloud_matches_a_template():
    s = FD.READ_ALOUD.format(model="Qwen 27B", recall="53.5", lookup="2.6", gap="50.9", ctrl="12.4")
    assert V.template_re.fullmatch(s)


# ---- the registry ----------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(("old", "want"), [
    ({"status": "post_hoc", "tag": ""}, ("post_hoc", "claimed", "")),
    ({"status": "fixed_in_advance", "tag": ""}, ("fixed_in_advance", "claimed", "")),
    ({"status": "post_hoc", "tag": "not claimed: shared with the logit lens"},
     ("post_hoc", "not_claimed", "shared with the logit lens")),
    ({"status": "descriptive", "tag": ""}, ("fixed_in_advance", "descriptive", "")),
])  # fmt: skip
def test_conversion_keeps_timing_and_claim(old, want):
    row = SR.convert({"figure": "f", "cell": "c", "reason": "r", "source": "s", **old})
    assert (row["timing"], row["claim"], row["claim_reason"]) == want


def test_registry_is_current_and_loads():
    want = [SR.convert(r) for r in SR.rows()]
    with SR.OUT.open(newline="") as f:
        assert list(csv.DictReader(f)) == want
    assert V.registry_path == SR.OUT
    assert len(sp.load_registry(SR.OUT)) == len(want)


# ---- the figures -----------------------------------------------------------------------------------------------------
BUILT = list(SP.FIGS)


@pytest.fixture(scope="module")
def saved(tmp_path_factory):
    out = tmp_path_factory.mktemp("sp")
    return {fid: sp.save(SP.FIGS[fid](), out / f"{fid}.png", target="post", root=out) for fid in BUILT}


def test_every_figure_saves_strict(saved):
    for fid, report in saved.items():
        assert report.path.exists() and report.problems == [], fid


def test_one_data_key_prints_one_string_across_figures(saved):
    seen = defaultdict(set)
    for report in saved.values():
        for key, s in json.loads(report.sidecar.read_text())["numbers"].items():
            seen[key].add(s)
    assert {k: v for k, v in seen.items() if len(v) > 1} == {}


# ---- the setup figures (figkit/writeup_sp_d.py): the post's words only, and every quote from its source ------------------
from bridge_jspace.figkit import writeup_sp_d as SD  # noqa: E402

SETUP = list(SD.FIGS)
# the brief's rule 6 (9 Nov) and Dan's set names (9 Nov): words that never appear on a setup figure
BANNED = ("stated", "write in", "written into", "edit", "scrub", "redirect", "twin set", "main set",
          "described-bridge", "jsuite", "amendment", "note 62", "x47", "excess", "x49", "x0")  # fmt: skip


def figure_texts(fig) -> list[str]:
    """Every string a setup figure prints: words, boxes, arrow labels, a card's prompt, columns, answers and note."""
    out: list[str] = []
    for b in fig.blocks:
        if isinstance(b, sp.Schematic):
            for e in b.elements:
                if isinstance(e, sp.Words):
                    out.append("".join(p[0] for p in e.parts))  # one line, its bold parts joined
                elif isinstance(e, sp.Box):
                    out.append(e.text)
                elif isinstance(e, sp.Arrow):
                    out.append(e.label)
        elif isinstance(b, sp.DotTable):
            out.append(b.note)
            out += list(b.row_sub.values())
            for col, group in b.flat_columns():
                out += [getattr(col, "header", ""), group.header if group else ""]
                out += [s.word or "" for s in getattr(col, "series", ())]
                out += [r.label for r in getattr(col, "rules", ())]
        elif isinstance(b, sp.Card):
            paras = b.prompt if b.prompt and isinstance(b.prompt[0], list) else [b.prompt]
            out += ["".join(p[0] for p in para) for para in paras] + list(b.columns) + [b.note]
            out += [a for r in b.rows for a in r.answers.values()]
    return [t for t in out if t]


@pytest.mark.parametrize("fid", [*SETUP, "patch_split", "patch_layers"])
def test_setup_figures_use_the_posts_words_only(fid):
    fig = SD.FIGS[fid]() if fid in SD.FIGS else SP.FIGS[fid]()
    text = " ".join([*figure_texts(fig), fig.read or ""]).lower()
    assert not [w for w in BANNED if w in text], fid


def test_setup_quotes_come_from_their_sources():
    """E1 and E4 quote the Rovio pair verbatim (items.jsonl); E5 quotes the documented made-up-fact example."""
    pair = SD._pair()
    contexts = pair["lookup"]["context"] + " " + pair["recall"]["context"]
    for fid in ("setup_twins", "setup_knockout"):
        for t in figure_texts(SD.FIGS[fid]()):
            for piece in (x.strip() for x in t.replace("…", "\n").split("\n")):
                if piece.endswith((".", "?")) and len(piece.split()) >= 4 and not piece.startswith(("Qwen", "Lens", "Rotated", "Over")):
                    assert piece in contexts or piece == pair["lookup"]["question"], (fid, piece)
    doc = (REPO / "scripts/jsuite_v4.py").read_text()
    for key in ("question", "sentence"):
        assert SD.MADE_UP[key] in doc, key
    scene = "The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked carbon. Eva picked helium."
    assert " ".join("".join(p[0] for p in ln) for ln in SD.CARBON.lines()) == scene

