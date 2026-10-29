"""The J-space panel (scripts/review_jspace.py, Dan 11:45 inspector_1145 items 2-5). The CPU readout against the
pipeline's own GPU ranks on 5 items per model (51.12's stored answer-word rank and 51.10's full-vocabulary bridge rank
at L, from 51.10's cached states; the states job's calib.jsonl where it has landed); the panel's page, heatmap and note
on a states file planted from 51.10's 9B states; that the panel writes only under review/ and cache/; Dan's flag rule;
and that the dashboard's verdict readers skip J-space notes. Tests that need model files (a head, a lens, 51.10's
gitignored states) are skipped where they are absent (on the Mac: the 9B and 27B run; Muse, Lightning and the 122B need
their lens and head from the box)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from bridge_jspace.review import items as I
from scripts import review_jspace as J
from scripts import x51_jread as JR

MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning", "qwen3.5-122b-a10b")


def jread_dir(model: str) -> Path | None:
    run = JR.RUNS.get(model)
    for root in (I.REPO, J.main_checkout()):
        if run and (root / "results" / "x51_jread" / run / JR.STATES_FILE).exists():
            return root / "results" / "x51_jread" / run
    return None


def can_read(model: str) -> bool:
    try:
        J.head_path(model)
        J.lens_file(model)
        return True
    except Exception:
        return False


def close(a: int, b: int) -> bool:
    """bf16 logits tie often far down the ranking: equal, or within 0.1% (and 2 places) of each other."""
    return abs(a - b) <= max(2, 0.001 * max(a, b))


@pytest.mark.parametrize("model", MODELS)
def test_cpu_readout_matches_the_pipeline_on_5_items(model):
    src = jread_dir(model)
    if src is None or not can_read(model):
        pytest.skip(f"{model}: 51.10's states, the head or the lens is not on this machine")
    ro = J.readout(model)
    z = np.load(src / JR.STATES_FILE)
    layers = [int(x) for x in z["layers"]]
    L = J.model_layer(model)
    li = layers.index(L)
    cases = [json.loads(x) for x in (src / "cases.jsonl").read_text().splitlines()]
    rd51, cs51 = J.x51_rows(model)
    n51 = exact51 = 0
    for i in range(5):
        c = cases[i]
        for v, var in enumerate(("org", "alt")):
            x = torch.tensor(z["h"][i, 0, v, :, li].astype(np.float32))  # the lookup's P1-P3 at L
            lg = ro.lens(x, L)
            ent = c["readers"]["PP"]["ids"][var][c["pos"]]
            for p in range(3):
                mine, theirs = int((lg[p] > lg[p, ent]).sum()) + 1, int(z["rank_own_full"][i, 0, v, p, li])
                assert close(mine, theirs), (c["scene"], var, p, mine, theirs)
                if p == 0:
                    assert mine == theirs  # the bridge word: exact
            row = rd51.get((c["scene"], var))
            if row:  # 51.12's own forwards: the states differ in bf16 noise from 51.10's (another run), ranks a little
                for w in ("PP", "PM"):
                    mine = J.rank_of(lg[0], cs51[c["scene"]]["tokens"]["own_word"][var][w])[0]
                    theirs = row["answer_word_rank"][w]
                    assert mine is not None and abs(mine - theirs) <= max(2, 0.10 * theirs), (c["scene"], var, w)
                    n51 += 1
                    exact51 += mine == theirs
    assert n51 == 0 or exact51 >= 0.6 * n51, (exact51, n51)


@pytest.mark.parametrize("model", MODELS)
def test_cpu_readout_matches_the_states_jobs_gpu_calibration(model):
    rows_dir = sorted((I.REPO / "results" / "review_states").glob("*/calib.jsonl"))
    rows = [json.loads(line) for f in rows_dir for line in f.read_text().splitlines()
            if json.loads(f.parent.joinpath("manifest.json").read_text())["model"]["target"] == model]  # fmt: skip
    if not rows or not can_read(model) or not (J.STATES / model).exists():
        pytest.skip(f"{model}: no states job calibration (or head / lens) here yet")
    ro = J.readout(model)
    for r in rows[:20]:
        st = np.load(J.STATES / model / r["file"])
        meta = json.loads(str(st["meta"]))
        vec, why = J.vector({k: st[k] for k in st.files if k != "meta"} | {"meta": meta}, model,
                            "S" if r["vector"] == "state_S" else "O", meta["pos"], r["layer"],
                            str({"state_O": "state", "state_S": "state"}.get(r["vector"], r["vector"])))  # fmt: skip
        assert vec is not None, why
        lg = ro.lens(vec[None], r["layer"])[0] if r["lens"] == "jpp" else ro.unembed(vec[None])[0]
        for t, rank in r["ranks"].items():
            assert close(int((lg > lg[int(t)]).sum()) + 1, rank), (r["vector"], r["lens"], t)


# ---- the page on a planted states file (51.10's 9B states: the bridge word, the "pick" token, the last token) -------

MODEL9 = "qwen3.5-9b"


def plant(tmp: Path, view_id: str, item: dict) -> None:
    """A states file in the states job's layout from 51.10's cached states (its 15 layers; the others zero), with the
    change's 25 atoms and X0's random part at L (CPU: x52_atoms' dictionary and fit)."""
    from scripts import review_states as RS
    from scripts import statement_positions as SP
    from scripts import x0_necessity as X
    from scripts import x52_atoms as AT

    src = jread_dir(MODEL9)
    assert src is not None
    z = np.load(src / JR.STATES_FILE)
    layers = [int(x) for x in z["layers"]]
    cases = [json.loads(x) for x in (src / "cases.jsonl").read_text().splitlines()]
    i = next(k for k, c in enumerate(cases) if c["scene"] == item["scene"])
    c, w = cases[i], item["reader"]
    r = JR.RIDX[w]
    pos = [c["jpos"][w][p]["org"] for p in JR.POS]
    n_layers, d = 32, z["h"].shape[-1]
    h = np.zeros((2, 3, n_layers, d), dtype=np.float16)
    for li, la in enumerate(layers):
        h[:, :, la] = z["h"][i, r, :, :, li]
    L = J.model_layer(MODEL9)
    tok = RS.hf_tokenizer(MODEL9)
    x = torch.tensor(h[1, :, L].astype(np.float32) - h[0, :, L].astype(np.float32))
    lt, dic, _ = AT.cpu_dictionary(tok, MODEL9, L)
    chosen, coefs, gains, approx = AT.omp_atoms(dic, x, X.K_MAIN)
    share = approx.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
    rand = SP.random_subspace_part(x, share, SP.random_basis(d, torch.Generator().manual_seed(X.SUBSPACE_SEED + L)))
    atoms_ids = np.full((3, n_layers, 25), -1, dtype=np.int32)
    atoms_coef = np.zeros((3, n_layers, 25), dtype=np.float32)
    atoms_gain = np.zeros((3, n_layers, 25), dtype=np.float32)
    rand_all = np.zeros((3, n_layers, d), dtype=np.float16)
    atoms_ids[:, L] = lt.numpy()[chosen.numpy()]
    atoms_coef[:, L], atoms_gain[:, L], rand_all[:, L] = coefs.numpy(), gains.numpy(), rand.numpy()
    ids = {v: [*list(item["case"]["readers"][w]["ids"][k]), 220] for v, k in (("O", "org"), ("S", "alt"))}
    roles = {str(pos[0]): ["bridge"], str(pos[1]): ["question"], str(pos[2]): ["last"]}
    meta = {"view": view_id, "item": item["id"], "kind": item["kind"], "reader": w, "scene": item["scene"],
            "condition": None, "run": item["run"], "layer": L, "pos": pos[0], "suffix": [220], "roles_O": roles,
            "roles_S": roles}  # fmt: skip
    f = tmp / MODEL9 / RS.item_file(view_id, item["id"])
    f.parent.mkdir(parents=True, exist_ok=True)
    np.savez(f, h_O=h[0], h_S=h[1], pos_O=np.asarray(pos), pos_S=np.asarray(pos), pairs=np.asarray([[0, 0], [1, 1], [2, 2]]),
             ids_O=np.asarray(ids["O"]), ids_S=np.asarray(ids["S"]), atoms_ids=atoms_ids, atoms_coef=atoms_coef,
             atoms_gain=atoms_gain, jpp_share=np.zeros((3, n_layers), np.float32), rand=rand_all,
             rand_share=np.zeros((3, n_layers), np.float32), lens_layers=np.asarray([L]), meta=np.asarray(json.dumps(meta)))  # fmt: skip


@pytest.fixture
def planted(tmp_path, monkeypatch):
    if jread_dir(MODEL9) is None or not can_read(MODEL9):
        pytest.skip("the 9B's 51.10 states, head or lens is not on this machine")
    items = [it for it in I.items("main_swap", MODEL9) if it["scene"] == "P2-L0-0078" and it["reader"] == "PP"]
    assert items, "P2-L0-0078 (a fixed-sample item) is not in main_swap's 9B item set"
    states = tmp_path / "cache" / "review_states"
    plant(states, "main_swap", items[0])
    monkeypatch.setattr(J, "REPO", tmp_path)
    monkeypatch.setattr(J, "STATES", states)
    monkeypatch.setattr(J, "PANEL_CACHE", tmp_path / "cache" / "review_jspace")
    monkeypatch.setattr(J, "MARKS", tmp_path / "review" / "marks.jsonl")
    J.states.cache_clear()
    yield items[0], tmp_path
    J.states.cache_clear()


def test_the_panel_shows_every_vector_and_writes_only_under_review_and_cache(planted):
    it, root = planted
    before = {p for p in root.rglob("*") if p.is_file()}
    L = str(J.model_layer(MODEL9))
    for v in J.VECTORS:
        out = J.page({"view": "main_swap", "item": it["id"], "vector": v, "layer": L, "tokens": " helium\nC\n#17"})
        assert "Look into J-space" in out and "Traceback" not in out
        assert ("J++ lens: top 30" in out) and ("logit lens: top 30" in out), v
    out = J.page(
        {"view": "main_swap", "item": it["id"], "vector": "rest", "layer": L, "heat": " " + it["case"]["cf_bridge"]}
    )
    assert "Rank of" in out and "The 25 atoms of the change at L12" in out and "Self-checks" in out
    J.note({"view": "main_swap", "item": it["id"], "note": "identity token in the rest at L14", "layer": "14"}, "abc")
    rows = [json.loads(line) for line in (root / "review" / "marks.jsonl").read_text().splitlines()]
    assert rows[-1]["kind"] == "jspace" and rows[-1]["verdict"] is None and rows[-1]["where"]["layer"] == "14"
    new = {p.relative_to(root).parts[0] for p in root.rglob("*") if p.is_file() and p not in before}
    assert new <= {"review", "cache"}, new
    with pytest.raises(AssertionError):
        J.write_text(root / "results" / "x.json", "{}")
    with pytest.raises(AssertionError):
        J.write_text(root / "cache" / ".." / "docs" / "x.md", "")


def test_the_panels_51_12_self_check_holds_on_the_planted_item(planted):
    it, _ = planted
    st = J.states(MODEL9, "main_swap", it["id"])
    assert st is not None
    got = J.check_51_12(st, it, MODEL9)
    assert len(got) == 2 and all(close(r["panel"], r["stored"]) for r in got), got


def test_card_links_and_the_flag_rule():
    page = ("<form class='marks' onsubmit='return mark(this)'><input type='hidden' name='view' value='main_swap'>"
            "<input type='hidden' name='item' value='qwen3.5-9b|run|P2-L0-0001|PP'>")  # fmt: skip
    assert "/jspace?view=main_swap&amp;item=" in J.with_links(page) or "/jspace?view=main_swap&item=" in J.with_links(
        page
    )

    def rows(n_rest: int, n_rand: int, n: int = 100) -> list[dict]:
        out = []
        for i in range(n):
            rk = {"S_bridge_word": None}
            out.append({"model": MODEL9, "view": "main_swap", "condition": None,
                        "ranks": {"jpp": {**rk, "S_bridge_word": 1}, "rest": {**rk, "S_bridge_word": 10 if i < n_rest else 900},
                                  "rand": {**rk, "S_bridge_word": 10 if i < n_rand else 900}}})  # fmt: skip
        return out

    flag = {t["kind"]: t["flag"] for t in J.rank_table(rows(40, 20))}
    assert flag["S's bridge (word or symbol)"] is True  # 0.40 - 0.20 = 0.20
    assert {t["kind"]: t["flag"] for t in J.rank_table(rows(39, 20))}["S's bridge (word or symbol)"] is False
    alt = {t["kind"]: (t["flag"], t["flag_alt"]) for t in J.rank_table(rows(30, 20))}["S's bridge (word or symbol)"]
    assert alt == (False, True)  # the other reading: the rest's share >= 0.20 and above the random part's


def test_the_dashboards_verdicts_skip_jspace_notes(tmp_path, monkeypatch):
    from scripts import review as R

    marks = tmp_path / "marks.jsonl"
    marks.write_text(json.dumps({"view": "main_swap", "item": "a", "seed": 29, "verdict": "wrong", "note": "x", "commit": "c",
                                 "utc": "u"}) + "\n" + json.dumps({"view": "main_swap", "item": "a", "seed": 29, "verdict": None,
                                                                  "note": "rest at L14", "kind": "jspace", "commit": "c",
                                                                  "utc": "u"}) + "\n")  # fmt: skip
    monkeypatch.setattr(R, "MARKS", marks)
    assert R.latest_marks()["a"]["verdict"] == "wrong"
    out = R.summary(tmp_path / "summary.md").read_text()
    assert "## J-space notes" in out and "rest at L14" in out


def test_the_rank_section_replaces_the_packs_reserved_block_only(tmp_path, monkeypatch):
    (tmp_path / "docs").mkdir()
    pack = tmp_path / "docs" / "verify_pack.md"
    pack.write_text(f"# Verification pack\n\n## Automatic checks\n\nx\n\n{J.SECTION}\n\n_Reserved for the inspector._\n\n"
                    "## a. main_swap\n\nkept\n")  # fmt: skip
    monkeypatch.setattr(J, "REPO", tmp_path)
    for _ in range(2):  # twice: the second run replaces the first
        J.put_section(J.SECTION + "\n\nnumbers\n")
    text = pack.read_text()
    assert text.count(J.SECTION) == 1 and "numbers" in text and "_Reserved" not in text
    assert text.index("## Automatic checks") < text.index(J.SECTION) < text.index("## a. main_swap") and "kept" in text
    assert (tmp_path / "docs" / "verify_pack_jspace.md").read_text() == J.SECTION + "\n\nnumbers\n"


def test_every_card_of_a_served_view_links_to_its_panel():
    from scripts import review as R

    page = R.render_view({"view": "main_swap", "seed": "29"}, True, "test")
    forms = page.count("<form class='marks'")
    assert forms >= 1 and J.with_links(page).count("Look into J-space") == forms
