"""scripts/inventory.py on the repo: the static import graph and a few classes the rules fix."""

from scripts import inventory as I


def test_import_graph_follows_aliased_and_lazy_imports():
    modules = I.module_map()
    assert "scripts/x0_necessity.py" in I.imports_of("scripts/x6_routes.py", modules)  # from scripts import x0_necessity as X
    assert "scripts/x0_massmean.py" in I.imports_of("scripts/x8_write.py", modules)  # imported inside geometry()


def test_classes_follow_the_rules():
    rows, _ = I.classify()
    cls = {r["path"]: r for r in rows}
    assert cls["scripts/x0_necessity.py"]["class"] == "current"
    assert cls["results/x0_necessity/qwen35_9b_x0_necessity"]["class"] == "current"
    old = cls["results/x0_necessity/qwen35_122b_x0_necessity"]
    assert old["class"] == "superseded" and old["superseded_by"] == "results/x0_necessity/qwen35_122b_x0_necessity_r2"
    assert cls["results/x6_routes/qwen35_122b_x6_routes_c0"]["class"] == "current"  # gate-stopped, backs "not tested"
    assert cls["scripts/jobq.py"]["class"] == "unknown"  # tooling is not placed by the rules
