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


def test_statement_index_in_every_form():
    for domain, conds in A.CONDITIONS.items():
        for c in conds:
            for it in A.load(domain, c)[:20]:
                idx = A.statement_index(it)
                assert sorted(idx.values()) == list(range(len(it["statements"])))
                for e, i in idx.items():
                    assert it["surface"][e] in it["statements"][i]
