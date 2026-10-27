"""The env switches that change what a run does, as its manifest records them: `"switches": switches()`.

target          the TARGETS key in effect (BJ_TARGET, else pins' default): the model, its lens and its run prefix
BJ_DEVICE_MAP   the model's GPU placement (model.placement); None unset and "" set empty both mean one GPU (a
                target's own split_gpus aside)
BJ_SUITE_BATCH  suite_split.BATCH, the rows per batched forward of suite_split and of the scripts that use it
                (x0_necessity's reads, statement_positions, early_push, ...); None unset (the default at the commit)
lens_sha256     sha256 of the target's frozen lens file (pins.FROZEN_LENS), the file the lens loader checks; None for
                a target without one. Recorded whether or not the run reads the lens.

The env values are raw strings, as the run read them. The manifest records them when it is written: a script whose
run is a later stage in another process (manifest, then run) records the manifest stage's env.
"""

from __future__ import annotations

import os
from typing import Any

from bridge_jspace import pins

ENV_SWITCHES = ("BJ_DEVICE_MAP", "BJ_SUITE_BATCH")


def frozen_lens_sha256() -> str | None:
    """The target's frozen lens sha256 as lens.py checks it: a local lens's own pin (its LENS_SOURCES entry), a Hub
    lens's FROZEN_LENS_SHA256; None when the target has no frozen lens (pins.LENS_SOURCES lacks it)."""
    source = pins.LENS_SOURCES.get(pins.FROZEN_LENS)
    if source is None:
        return None
    return source[2] if source[0] == "local" else pins.FROZEN_LENS_SHA256


def switches() -> dict[str, Any]:
    """{"target", "BJ_DEVICE_MAP", "BJ_SUITE_BATCH", "lens_sha256"} for this process (see the module docstring)."""
    return {"target": pins.TARGET, **{k: os.environ.get(k) for k in ENV_SWITCHES}, "lens_sha256": frozen_lens_sha256()}
