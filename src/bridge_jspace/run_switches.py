"""The env switches that change what a run does, as its manifest records them: `"switches": switches()`.

target          the TARGETS key in effect (BJ_TARGET, else pins' default): the model, its lens and its run prefix
BJ_*            every BJ_ variable in the environment, by name in sorted order, as raw strings (Dan, 27 Oct); a
                variable whose name suggests a secret (it contains TOKEN, KEY, SECRET or PASSWORD) is recorded as
                REDACTED, its value never. Two are always there, None when unset:
  BJ_DEVICE_MAP   the model's GPU placement (model.placement); None unset and "" set empty both mean one GPU (a
                  target's own split_gpus aside)
  BJ_SUITE_BATCH  suite_split.BATCH, the rows per batched forward of suite_split and of the scripts that use it
                  (x0_necessity's reads, statement_positions, early_push, ...); None unset (the default at the commit)
lens_sha256     sha256 of the target's frozen lens file (pins.FROZEN_LENS), the file the lens loader checks; None for
                a target without one. Recorded whether or not the run reads the lens.

The manifest records them when it is written. A script whose run is a later step in another process (manifest, then
run) checks the run step's switches against the manifest's (check_switches).
"""

from __future__ import annotations

import os
import re
import sys
from collections.abc import Iterable
from typing import Any

from bridge_jspace import pins

ENV_SWITCHES = ("BJ_DEVICE_MAP", "BJ_SUITE_BATCH")  # always recorded (None when unset): readers rely on the keys
SECRET_WORDS = ("TOKEN", "KEY", "SECRET", "PASSWORD")
REDACTED = "<redacted: the name suggests a secret>"
FAIL_ON = ("target", "lens_sha256")  # a run step refuses to run on another model or lens than its manifest's
WARN_ON = ENV_SWITCHES  # ... and says so, then runs, when the placement or the batch differ


class SwitchMismatch(RuntimeError):
    """A run step's target or frozen lens is not its manifest's."""


def frozen_lens_sha256() -> str | None:
    """The target's frozen lens sha256 as lens.py checks it: a local lens's own pin (its LENS_SOURCES entry), a Hub
    lens's FROZEN_LENS_SHA256; None when the target has no frozen lens (pins.LENS_SOURCES lacks it)."""
    source = pins.LENS_SOURCES.get(pins.FROZEN_LENS)
    if source is None:
        return None
    return source[2] if source[0] == "local" else pins.FROZEN_LENS_SHA256


def env_switches() -> dict[str, str | None]:
    """Every BJ_ variable in the environment, sorted by name, secrets redacted; BJ_DEVICE_MAP and BJ_SUITE_BATCH
    always (None when unset)."""
    out: dict[str, str | None] = {k: None for k in ENV_SWITCHES}
    out.update((k, v) for k, v in os.environ.items() if k.startswith("BJ_"))
    secret = {k for k, v in out.items() if v is not None and any(w in k.upper() for w in SECRET_WORDS)}
    return {k: REDACTED if k in secret else out[k] for k in sorted(out)}


def switches() -> dict[str, Any]:
    """{"target", every BJ_ variable (env_switches), "lens_sha256"} for this process (see the module docstring)."""
    return {"target": pins.TARGET, **env_switches(), "lens_sha256": frozen_lens_sha256()}


# A hub kernel's module file in the HF cache: <cache>/kernels--<org>--<name>/snapshots/<commit>/... (the kernels
# package 0.16's repo_type "kernel"; a models-- folder, a kernel cached as a model repo, is accepted too)
HUB_KERNEL_PATH = re.compile(r"(?:kernels|models)--([^/\\]+)--([^/\\]+)[/\\]snapshots[/\\]([0-9a-f]{40})[/\\]")


def hub_kernels(files: Iterable[str]) -> dict[str, list[str]]:
    """Repo -> the sorted commits of the HF-hub kernel modules among `files` (module file paths), read from the paths."""
    found: dict[str, set[str]] = {}
    for f in files:
        if m := HUB_KERNEL_PATH.search(str(f)):
            found.setdefault(f"{m[1]}/{m[2]}", set()).add(m[3])
    return {repo: sorted(commits) for repo, commits in sorted(found.items())}


def loaded_hub_kernels() -> dict[str, list[str]]:
    """The HF-hub kernels this process has imported so far (45s, 27 Oct: transformers resolves Lightning's mamba-ssm by
    major version at load time, so the commit is read from what was loaded). Call it after a forward: some kernels load
    at their first call."""
    return hub_kernels(f for mod in list(sys.modules.values()) if isinstance(f := getattr(mod, "__file__", None), str))


def warn(message: str) -> None:
    print(f"WARNING: {message}", file=sys.stderr, flush=True)


def check_switches(manifest: dict[str, Any]) -> None:
    """For a run step reading the manifest an earlier step wrote: raise SwitchMismatch if the target or the frozen
    lens differ from the manifest's; warn and go on if BJ_DEVICE_MAP or BJ_SUITE_BATCH differ; warn once and go on
    if the manifest records no switches (written before 27 Oct 2026)."""
    run = manifest.get("run") or manifest.get("exp") or "this run"
    recorded = manifest.get("switches")
    if recorded is None:
        warn(f"{run}: its manifest records no switches (written before they were recorded); not checked")
        return
    now = switches()
    bad = [f"{k} {recorded.get(k)!r} in the manifest, {now[k]!r} now" for k in FAIL_ON if recorded.get(k) != now[k]]
    if bad:
        raise SwitchMismatch(f"{run}: " + "; ".join(bad) + " (run with the switches the manifest was written with)")
    for k in WARN_ON:
        if recorded.get(k) != now[k]:
            warn(f"{run}: {k} {recorded.get(k)!r} in the manifest, {now[k]!r} now; running with {now[k]!r}")
