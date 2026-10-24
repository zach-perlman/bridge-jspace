"""x4_alias: a scene's conditions share its frame and differ only in the statements; the alt is an unpicked entity;
statements map to their entities in every surface form."""

from scripts import x4_alias as A


def test_frame_shared_and_alt_unpicked():
    for domain, (same, alias) in A.CONDITIONS.items():
        a = {it["scene"]: it for it in A.load(domain, same)}
        b = {it["scene"]: it for it in A.load(domain, alias)}
        for s in sorted(a)[:20]:
            fa, fb = A.frame(a[s], domain), A.frame(b[s], domain)
            assert fa == fb, f"{domain} {s}: the frame differs across conditions"
            assert a[s]["entities"] == b[s]["entities"] and a[s]["digits"] == b[s]["digits"]
            assert not set(fa["alt_options"]) & set(fa["picked"])
            assert len(fa["alt_options"]) == len(a[s]["entities"]) - A.N_PICKS


def test_verdict_reads_planted_differences(tmp_path, monkeypatch):
    import json

    monkeypatch.setattr(A, "RESULTS", tmp_path)
    src = tmp_path / "fake"
    src.mkdir()
    (src / "manifest.json").write_text(json.dumps({"model": {"target": "fake"}, "layer": 32}))
    lost = {"animals/same": 0.0, "animals/xlang": 0.3, "elements/same": 0.0, "elements/syn": 0.25}
    rows, cases, elig, gate = [], [], {}, {}
    for form, frac in lost.items():
        domain, cond = form.split("/")
        scenes = []
        for i in range(120):
            s = f"{domain}|{i}|{cond}"
            ent = f"{domain}-e{i % 8}"
            cases.append({"scene": s, "bridge": ent})
            scenes.append(s)
            for w in ("PP", "PM"):
                base = {"scene": s, "entity": ent, "rendering": "chat", "layer": 32, "reader": w, "upstream": False}
                rows.append({**base, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "switched": 1})
                lose = int(w == "PP" and i < round(frac * 120))
                rows.append({**base, "dict": "jpp", "k": 25, "omp": "signed", "arm": "no_part", "switched": 1 - lose})
                rows.append({**base, "dict": "jpp", "k": 25, "omp": "signed", "arm": "no_rand", "switched": 1})
        for w in ("PP", "PM"):
            elig[f"{form}/{w}"] = scenes
            gate[f"{form}/{w}"] = {"cases": 120, "org_accuracy": 0.95, "pass": True, "eligible": 120}
    (src / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (src / "cases.jsonl").write_text("".join(json.dumps(c) + "\n" for c in cases))
    (src / "eligible.jsonl").write_text("".join(json.dumps({"key": k, "scenes": v}) + "\n" for k, v in elig.items()))
    (src / "gate.json").write_text(json.dumps({"gate": gate}))
    blob = json.loads((A.stage_verdict("fake", 200) / "verdict.json").read_text())
    assert abs(blob["rules"]["animals"]["difference"][0] - 0.3) < 1e-9
    assert blob["rules"]["animals"]["reading"] == "needs a verbatim match"
    assert blob["rules"]["elements"]["reading"] == "passes"


def test_statement_index_in_every_form():
    for domain, conds in A.CONDITIONS.items():
        for c in conds:
            for it in A.load(domain, c)[:20]:
                idx = A.statement_index(it)
                assert sorted(idx.values()) == list(range(len(it["statements"])))
                for e, i in idx.items():
                    assert it["surface"][e] in it["statements"][i]
