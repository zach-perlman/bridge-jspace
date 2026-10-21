"""code_pointer_v1's generator: predictions, permutations, selectors (IX list, CH chain), collision policy, balance,
execution of the generated code, spans, determinism, token alignment."""

import collections
import subprocess
import sys

import pytest

from scripts import code_pointer_v1 as CP

CELLS = [(d, n) for d in CP.DOMAINS for n in (3, 5, 8) if len(CP.DOMAINS[d]["entities"]) >= n]


def cell(domain: str, n_ent: int, n: int = 40, seed: int = 123) -> dict[str, list[dict]]:
    return CP.generate_cell(seed, domain, f"e{n_ent}f0", n_ent, n)


@pytest.mark.parametrize(("domain", "n_ent"), CELLS)
def test_predictions_distinct_and_correct(domain, n_ent):
    for fam, items in cell(domain, n_ent).items():
        for it in items:
            sl, d = it["slots"], it["sources"]["dissoc"]
            look = dict(zip(it["entities"], it["digits"], strict=True))
            q_s, p = d["query"], it["entities"][sl["position"]]
            assert it["entities"][sl["query"]] == it["query"]
            assert it["entities"][sl["identity"]] == q_s
            assert d["entities"][sl["position"]] == q_s  # the source binds q_s at slot k, where the base has p
            assert len({sl["query"], sl["identity"], sl["position"]}) == 3
            pd = d["predictions"]
            if fam == "RR":
                assert pd["none"] != pd["identity"]
                assert pd["value"] == pd["identity"] == str(CP.rec(domain, q_s))
                assert pd["position"] == str(CP.rec(domain, p))
            else:
                assert len(set(pd.values())) == 4
                assert pd == {"none": str(look[it["query"]]), "identity": str(look[q_s]), "position": str(look[p]),
                              "value": d["answer"]}  # fmt: skip
                assert int(pd["value"]) not in it["digits"]  # the value is absent from the base context
            assert set(it["sources"]["same"]["predictions"].values()) == {it["answer"]}


@pytest.mark.parametrize(("domain", "n_ent"), CELLS)
def test_families_share_the_scene(domain, n_ent):
    """Every family on a scene has the same dict line, entries, slots and (lookups) predictions; only how the key is
    found differs."""
    fams = cell(domain, n_ent, n=10)
    for i in range(10):
        its = {f: fams[f][i] for f in CP.FAMILIES}
        dict_lines = {it["context"].split("\n")[1] for it in its.values()}
        assert len(dict_lines) == 1
        assert len({it["scene"] for it in its.values()}) == 1
        assert len({str(it["slots"]) for it in its.values()}) == 1
        lookups = [it["sources"]["dissoc"]["predictions"] for f, it in its.items() if f != "RR"]
        assert all(p == lookups[0] for p in lookups)
        assert len({str(it["spans"]["entries"]) for it in its.values()}) == 1  # entries at the same chars


@pytest.mark.parametrize(("domain", "n_ent"), CELLS)
def test_selectors(domain, n_ent):
    """IX: the base list has q_b at the queried index, dissoc q_s, same q_b with the rest reshuffled, all permutations
    of the keys, the index never a lookup digit. CH: the printed chain's head is q_b (dissoc: q_s), the distractor
    head is neither and (N >= 4) not p; variables and line order are shared by every source."""
    fams = cell(domain, n_ent)
    for it in fams["IX"]:
        ix, base = it["code"]["index"], it["code"]["list"]
        src = {k: v["code"]["list"] for k, v in it["sources"].items()}
        assert base[ix] == it["query"] and src["dissoc"][ix] == it["sources"]["dissoc"]["query"]
        assert src["same"][ix] == it["query"] and src["same"] != base and src["redigit"] == base
        assert all(sorted(v) == sorted(it["entities"]) for v in [base, *src.values()])
        assert ix not in set(it["digits"]) | {x for s in it["sources"].values() for x in s["digits"]}
        assert f"names[{ix}]" in it["question"]
    for fam in ("CH2", "CH3"):
        for it in fams[fam]:
            c = it["code"]
            assert c["depth"] == CP.CHAIN_DEPTH[fam] and len(c["lines"]) == 2 * c["depth"]
            assert c["heads"]["target"] == it["query"]
            assert it["sources"]["dissoc"]["code"]["heads"] == {"target": it["sources"]["dissoc"]["query"],
                                                                "distractor": c["heads"]["distractor"]}  # fmt: skip
            r = c["heads"]["distractor"]
            assert r not in (it["query"], it["sources"]["dissoc"]["query"])
            assert r != it["entities"][it["slots"]["position"]] or n_ent == 3
            for s in it["sources"].values():
                assert s["code"]["order"] == c["order"] and s["code"]["vars"] == c["vars"]
            assert f"[{c['printed']}])" in it["question"] and it["question"] == it["sources"]["dissoc"]["question"]


@pytest.mark.parametrize(("domain", "n_ent"), CELLS)
def test_collision_policy(domain, n_ent):
    for items in cell(domain, n_ent).values():
        for it in items:
            d = it["sources"]["dissoc"]
            critical = {CP.rec(domain, e) for e in (it["query"], d["query"], it["entities"][it["slots"]["position"]])}
            if it["digit_policy"] in ("soft", "hard"):
                assert not set(it["digits"]) & critical
                assert not set(d["digits"]) & critical
            if it["digit_policy"] == "soft":
                assert not set(it["digits"]) & set(it["recalled"].values())
            assert sorted(it["collisions"]) == sorted(set(it["digits"]) & set(it["recalled"].values()))
        if n_ent == 3:
            assert all(it["digit_policy"] == "soft" for it in items)
        if n_ent == 8:  # 9 of the 10 digits are needed: only IX's index is kept out
            assert all(it["digit_policy"] == "none" for it in items)


@pytest.mark.parametrize("n_ent", [3, 5])
def test_slots_and_index_balanced(n_ent):
    n_pairs = n_ent * (n_ent - 1)
    items = cell("animals", n_ent, n=3 * n_pairs)["IX"]
    for key in ("query", "position"):
        counts = collections.Counter(it["slots"][key] for it in items)
        assert set(counts.values()) == {3 * (n_ent - 1)}, (key, counts)
    index = collections.Counter(it["code"]["index"] for it in items)
    assert set(index) == set(range(n_ent)) and max(index.values()) - min(index.values()) <= 1


@pytest.mark.parametrize(("domain", "n_ent"), CELLS)
def test_code_computes_the_answers(domain, n_ent):
    """In-process: base and every source print (DK, IX, CH) or store (RK) their recorded answer."""
    for items in cell(domain, n_ent, n=15).values():
        assert all(CP.executes(it) for it in items)


def test_code_runs_in_python():
    """The snippets run in a fresh interpreter and print the base answer (and each source its own)."""
    fams = cell("animals", 5, n=4)
    for fam in ("DK", "IX", "CH2", "CH3"):
        for it in fams[fam]:
            parts = [it, *it["sources"].values()]
            for part in parts:
                src = CP.python_source(part["context"], part["question"])
                out = subprocess.run([sys.executable, "-I", "-c", src], capture_output=True, text=True, check=True)
                assert out.stdout == part["answer"] + "\n", (it["id"], src)
    for it in fams["RK"]:
        src = CP.python_source(it["context"], it["question"]) + f'print(lockers["{it["query"]}"])\n'
        out = subprocess.run([sys.executable, "-I", "-c", src], capture_output=True, text=True, check=True)
        assert out.stdout == it["answer"] + "\n"


@pytest.mark.parametrize(("domain", "n_ent"), CELLS)
def test_spans_name_their_text(domain, n_ent):
    for items in cell(domain, n_ent, n=10).values():
        for it in items:
            for part in [it, *it["sources"].values()]:
                c, sp = CP.content_of(part["context"], part["question"]), part["spans"]
                assert [c[s:e] for s, e in sp["entries"]] == [
                    f'"{e}": {d}' for e, d in zip(part["entities"], part["digits"], strict=True)
                ]
                assert c[slice(*sp["question"])] == part["question"]
                assert c[slice(*sp["tail"])] == " " + CP.INSTRUCTION
                assert c[slice(*sp["code"])].startswith("```python\n") and c[slice(*sp["code"])].endswith("```")
                if it["family"] in ("RK", "RR"):
                    assert c[slice(*sp["query"])] == CP.cue(domain, part["query"])
                else:
                    assert c[slice(*sp["query"])].startswith("print(")
                if "list" in sp:
                    assert [c[s:e] for s, e in sp["list"]] == [f'"{e}"' for e in part["code"]["list"]]
                if "chain" in sp:
                    assert [c[s:e] for s, e in sp["chain"]] == part["code"]["lines"]


def test_prompt_is_the_suites_code_layout():
    """The user turn is the suite's CODE layout: fenced code, then the question; the question starts after a newline
    (pointer_swap finds it with rindex) and the template after it is the same in every prompt."""
    for fam, items in cell("animals", 5, n=3).items():
        for it in items:
            c = CP.content_of(it["context"], it["question"])
            assert c.startswith("```python\nlockers = {")
            assert c.rindex("\n" + it["question"]) == len(it["context"])
            assert c.endswith("\n```\n" + CP.NL_PRINT + " " + CP.INSTRUCTION) or fam in ("RK", "RR")


def test_pointer_v1_schema():
    """Every key of a pointer_v1 item (and of its sources and steps) exists here with the same type, so pointer_swap's
    readers work on these items; the extra keys are spans and code."""
    from scripts import pointer_v1 as PV

    ref = PV.generate_cell(1, "animals", "e5f0", 5, 0, 1)
    for fam, items in cell("animals", 5, n=1).items():
        it, r = items[0], ref["DL" if fam == "DK" else "RR" if fam == "RR" else "RL"][0]
        assert {k: type(v) for k, v in r.items()}.items() <= {k: type(v) for k, v in it.items()}.items()
        assert set(it) - set(r) == {"spans", "code"}
        for src in PV.SOURCES:
            assert set(r["sources"][src]) <= set(it["sources"][src])
            assert set(it["sources"][src]["predictions"]) == set(PV.HYPOTHESES)
        for h in ("hop1", "hop2"):
            assert (h in it) == (h in r) and (h not in it or set(it[h]) == set(r[h]))


def test_deterministic():
    assert cell("months", 5) == cell("months", 5)
    assert CP.generate_cell(1, "months", "e5f0", 5, 10) != CP.generate_cell(2, "months", "e5f0", 5, 10)


def test_token_alignment():
    try:
        tok = CP.tokenizer()
    except Exception:
        pytest.skip("Qwen3.6-27B tokenizer not cached")
    CP.check_pools(tok)
    for domain, n_ent in CELLS:
        for items in cell(domain, n_ent, n=4).values():
            for it in items:
                got = CP.check_item(tok, it)
                for k in CP.MUST:
                    assert got[k], (it["id"], k)
