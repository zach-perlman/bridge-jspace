import json
from pathlib import Path

from scripts.jobq import ids_on_other_boxes


def _setup(tmp: Path) -> None:
    (tmp / "results" / "jobq").mkdir(parents=True)
    (tmp / "cache" / "jobq").mkdir(parents=True)
    (tmp / "results" / "jobq" / "ledger_sesterce-a100x4.jsonl").write_text(json.dumps({"id": "a1"}) + "\n")
    (tmp / "results" / "jobq" / "ledger_seed_a100x4.jsonl").write_text(json.dumps({"id": "a0"}) + "\n")
    (tmp / "results" / "jobq" / "ledger_sesterce-h200x2.jsonl").write_text(json.dumps({"id": "h1"}) + "\n")
    (tmp / "cache" / "jobq" / "queue_state_sesterce-h200x2.json").write_text(json.dumps({"pending": [{"id": "h2"}]}))


def test_the_h200_sees_the_a100_ids(tmp_path: Path) -> None:
    _setup(tmp_path)
    assert ids_on_other_boxes(tmp_path, "sesterce-h200x2") == {"a0", "a1"}


def test_the_a100_sees_the_h200_ids_not_its_own(tmp_path: Path) -> None:
    _setup(tmp_path)
    assert ids_on_other_boxes(tmp_path, "sesterce-a100x4") == {"h1", "h2"}
