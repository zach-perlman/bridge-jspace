"""Colour-vision check of the role colours (figure grammar v2, check 8): simulate deuteranopia, protanopia and tritanopia
(Machado et al. 2009, severity 100, via colorspacious) and measure CIEDE2000 (Sharma, Wu and Dalal 2005) between two
role colours drawn in one figure (floor 12) and between a role colour and control grey (floor 8)."""

from __future__ import annotations

import itertools

import numpy as np

KINDS = ("deuteranomaly", "protanomaly", "tritanomaly")  # severity 100: the -opias
FLOOR_ROLES, FLOOR_CONTROL = 12.0, 8.0


def _rgb(hexcolour: str) -> np.ndarray:
    return np.array([int(hexcolour[i : i + 2], 16) for i in (1, 3, 5)]) / 255


def lab(hexcolour: str, kind: str | None = None) -> np.ndarray:
    """CIELab (D65) of a colour as seen with a simulated deficiency (None: normal vision)."""
    from colorspacious import cspace_convert

    c = _rgb(hexcolour)
    if kind is not None:
        c = np.clip(cspace_convert(c, {"name": "sRGB1+CVD", "cvd_type": kind, "severity": 100}, "sRGB1"), 0, 1)
    return cspace_convert(c, "sRGB1", "CIELab")


def ciede2000(lab1, lab2) -> float:
    """CIEDE2000 colour difference (kL = kC = kH = 1), as in Sharma, Wu and Dalal (2005)."""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cb**7 / (Cb**7 + 25**7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360 if C1p else 0.0
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360 if C2p else 0.0
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    else:
        dhp = h2p - h1p - 360 if h2p > h1p else h2p - h1p + 360
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))  # fmt: skip
    dtheta = 30 * np.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * np.sqrt(Cbp**7 / (Cbp**7 + 25**7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / np.sqrt(20 + (Lbp - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = -np.sin(np.radians(2 * dtheta)) * Rc
    return float(np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh)))


def failures(roles: dict[str, str], control: str = "control") -> list[tuple[str, str, str, float, float]]:
    """(kind, role a, role b, CIEDE2000, floor) for every pair of the given role colours under its floor, under any of
    the three simulated deficiencies (and normal vision)."""
    out = []
    for kind in (None, *KINDS):
        for a, b in itertools.combinations(sorted(roles), 2):
            floor = FLOOR_CONTROL if control in (a, b) else FLOOR_ROLES
            d = ciede2000(lab(roles[a], kind), lab(roles[b], kind))
            if d < floor:
                out.append((kind or "normal", a, b, round(d, 1), floor))
    return out
