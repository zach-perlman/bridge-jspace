"""Every {{num|key}} in the README and details templates exists in docs/x0_numbers.json, with a source."""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_probe_v4_keys_match_the_stored_runs():
    """The x0_probe v4 table's keys (docs/x0_numbers.json) and data/figures/depth/data.csv's probe.<target>.<model>.<order>
    rows hold each run's stored probe accuracy, interval and n, for four models x three targets x two orders."""
    import csv

    from scripts import x0_details as XD

    numbers = json.loads((REPO / "docs" / "x0_numbers.json").read_text())
    with (REPO / "data" / "figures" / "depth" / "data.csv").open() as f:
        data = {r["quantity"]: r for r in csv.DictReader(f) if r["figure"] == "probe"}
    for m in ("9b", "27b", "122b", "muse"):
        src, rows = XD.probe_v4_rows(m)
        for o, stratum in XD.PROBE_ORDERS.items():
            for t, target in XD.PROBE_TARGETS.items():
                r = rows[(target, stratum)]
                assert numbers[f"probe_{t}_{m}_{o}"] == {"text": XD.ci(r["probe"]), "source": src}
                assert numbers[f"probe_{t}_majority_{m}_{o}"]["text"] == XD.ci(r["majority"])
                assert numbers[f"probe_{t}_chance_{m}"]["text"] == XD.f2(r["chance"])
                row = data[f"probe.{t}.{m}.locker-{o}"]
                assert [float(row[k]) for k in ("value", "lo", "hi")] == r["probe"]
                assert (int(row["n"]), row["source"]) == (r["n"], src)
        assert numbers[f"probe_slot_layout_{m}_first"]["text"] == XD.ci(rows[("locker sentence", "before")]["layout"])
        assert numbers[f"probe_routes_value_{m}"]["text"] == "0 of 300"


def test_every_number_marker_has_a_value_and_a_source():
    numbers = json.loads((REPO / "docs" / "x0_numbers.json").read_text())
    assert all(v["text"] and v["source"] for v in numbers.values())
    for template in ("docs/depth/README.template.md", "docs/x0_details.template.md"):
        keys = set(re.findall(r"\{\{num\|(\w+)\}\}", (REPO / template).read_text()))
        assert keys, template
        assert keys <= set(numbers), f"{template}: missing {sorted(keys - set(numbers))}"
