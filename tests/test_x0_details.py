"""Every {{num|key}} in the README and details templates exists in docs/x0_numbers.json, with a source."""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_every_number_marker_has_a_value_and_a_source():
    numbers = json.loads((REPO / "docs" / "x0_numbers.json").read_text())
    assert all(v["text"] and v["source"] for v in numbers.values())
    for template in ("docs/README.template.md", "docs/x0_details.template.md"):
        keys = set(re.findall(r"\{\{num\|(\w+)\}\}", (REPO / template).read_text()))
        assert keys, template
        assert keys <= set(numbers), f"{template}: missing {sorted(keys - set(numbers))}"
