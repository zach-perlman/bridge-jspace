"""The autonomy window (.claude/autonomy/autonomy.py): revoking puts the settings back as they were, keeps what was
added meanwhile, is idempotent, and fires at the deadline (no processes spawned here). uv run pytest .claude/autonomy"""

import datetime as dt
import json
import time

import autonomy  # pytest puts this folder (no __init__.py) on sys.path
import pytest

ORIGINAL = {
    "permissions": {"allow": ["Read", "Bash(git status*)"], "deny": ["Bash(git push*)"]},
    "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo stop"}]}]},
}


@pytest.fixture
def paths(tmp_path, monkeypatch):
    s, st = tmp_path / ".claude" / "settings.local.json", tmp_path / ".claude" / "autonomy" / "state.json"
    monkeypatch.setattr(autonomy, "SETTINGS", s)
    monkeypatch.setattr(autonomy, "STATE", st)
    monkeypatch.setattr(autonomy, "LOG", tmp_path / ".claude" / "autonomy" / "log.txt")
    return s, st


def write(path, d):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(d, indent=2) + "\n")


def soon(hours=1.0):
    return dt.datetime.now() + dt.timedelta(hours=hours)


def test_grant_then_revoke_restores_the_file(paths):
    s, st = paths
    write(s, ORIGINAL)
    before = s.read_text()
    autonomy.grant(soon(), spawn=False)
    d = json.loads(s.read_text())
    assert d["permissions"]["allow"][:2] == ["Bash", "Edit"]
    assert "Read" in d["permissions"]["allow"]
    assert d["permissions"]["allow"].count("Read") == 1  # already there: not added twice
    assert set(autonomy.DENY) <= set(d["permissions"]["deny"])
    assert any(autonomy._our_hook(e) for e in d["hooks"]["SessionStart"])
    assert st.exists()
    assert s.with_name(s.name + ".autonomy-bak").read_text() == before
    assert autonomy.revoke()
    assert s.read_text() == before
    assert not st.exists()


def test_revoke_keeps_rules_added_meanwhile_and_twice_is_a_noop(paths):
    s, _ = paths
    write(s, ORIGINAL)
    autonomy.grant(soon(), spawn=False)
    d = json.loads(s.read_text())
    d["permissions"]["allow"].append("Bash(make queue-status*)")  # e.g. "always allow" during the window
    write(s, d)
    assert autonomy.revoke()
    after = json.loads(s.read_text())
    assert after["permissions"]["allow"] == [*ORIGINAL["permissions"]["allow"], "Bash(make queue-status*)"]
    assert after["permissions"]["deny"] == ORIGINAL["permissions"]["deny"]  # the deny rule that was there stays
    assert after["hooks"] == ORIGINAL["hooks"]
    assert not autonomy.revoke()
    assert json.loads(s.read_text()) == after


def test_no_settings_file_is_created_then_removed(paths):
    s, _ = paths
    autonomy.grant(soon(), spawn=False)
    assert "Bash" in json.loads(s.read_text())["permissions"]["allow"]
    autonomy.revoke()
    assert not s.exists()


def test_empty_containers_that_existed_before_stay(paths):
    s, _ = paths
    write(s, {"permissions": {"allow": [], "deny": []}})
    before = s.read_text()
    autonomy.grant(soon(), spawn=False)
    autonomy.revoke()
    assert s.read_text() == before


def test_second_grant_moves_the_deadline_without_adding_twice(paths):
    s, _ = paths
    write(s, ORIGINAL)
    first = autonomy.grant(soon(1), spawn=False)
    second = autonomy.grant(soon(5), spawn=False)
    assert second["added"] == first["added"]
    assert second["until"] > first["until"]
    assert json.loads(s.read_text())["permissions"]["allow"].count("Bash") == 1
    autonomy.revoke()
    assert json.loads(s.read_text()) == ORIGINAL


def test_check_revokes_only_after_the_deadline(paths):
    s, st = paths
    write(s, ORIGINAL)
    state = autonomy.grant(soon(), spawn=False)
    assert not autonomy.check(now=state["until"] - 1)
    assert st.exists()
    assert autonomy.check(now=state["until"])
    assert json.loads(s.read_text()) == ORIGINAL


def test_watch_revokes_at_the_deadline(paths, monkeypatch):
    s, st = paths
    write(s, ORIGINAL)
    autonomy.grant(dt.datetime.now() + dt.timedelta(seconds=0.2), spawn=False)
    monkeypatch.setattr(autonomy, "POLL_S", 0.05)
    t0 = time.time()
    autonomy.watch()
    assert time.time() - t0 < 5
    assert not st.exists()
    assert json.loads(s.read_text()) == ORIGINAL


def test_status_revokes_an_expired_window(paths):
    s, st = paths
    write(s, ORIGINAL)
    autonomy.grant(soon(), spawn=False)
    state = json.loads(st.read_text())
    state["until"] = time.time() - 60  # the watcher died before the deadline (a reboot)
    st.write_text(json.dumps(state))
    assert "revoked now" in autonomy.status()
    assert json.loads(s.read_text()) == ORIGINAL


@pytest.mark.parametrize(
    ("now", "until", "expected"),
    [
        ("2026-10-26 01:00", "11:00", "2026-10-26 11:00"),
        ("2026-10-26 23:00", "11:00", "2026-10-27 11:00"),
        ("2026-10-26 01:00", "2026-10-27 09:30", "2026-10-27 09:30"),
    ],
)
def test_parse_until(now, until, expected):
    fmt = "%Y-%m-%d %H:%M"
    got = autonomy.parse_until(None, until, dt.datetime.strptime(now, fmt))
    assert got == dt.datetime.strptime(expected, fmt)


def test_parse_until_rejects_bad_input():
    now = dt.datetime(2026, 10, 26, 1, 0)
    with pytest.raises(SystemExit):
        autonomy.parse_until(None, None, now)
    with pytest.raises(SystemExit):
        autonomy.parse_until(2, "11:00", now)
    with pytest.raises(SystemExit):
        autonomy.parse_until(-1, None, now)
    with pytest.raises(SystemExit):
        autonomy.parse_until(None, "2026-10-25 09:00", now)
    assert autonomy.parse_until(1.5, None, now) == now + dt.timedelta(hours=1.5)
