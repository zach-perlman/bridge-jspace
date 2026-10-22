"""Compare two J++ artifacts pairwise (every tensor, recursively): max relative difference; MERGE_OK iff every pair
is within tolerance (rtol 1e-3 of the tensor's scale; fp32 sums in a different order).

python merge_compare.py A1 B1 [A2 B2 ...]
"""

import sys

import torch


def tensors(x, prefix=""):
    if isinstance(x, torch.Tensor):
        yield prefix, x
    elif isinstance(x, dict):
        for k in sorted(x, key=str):
            yield from tensors(x[k], f"{prefix}/{k}")
    elif isinstance(x, list | tuple):
        for i, v in enumerate(x):
            yield from tensors(v, f"{prefix}/{i}")


ok = True
args = sys.argv[1:]
for a_path, b_path in zip(args[::2], args[1::2], strict=True):
    a = dict(tensors(torch.load(a_path, map_location="cpu", weights_only=False)))
    b = dict(tensors(torch.load(b_path, map_location="cpu", weights_only=False)))
    assert a.keys() == b.keys(), f"{a_path} vs {b_path}: different keys {sorted(a.keys() ^ b.keys())[:5]}"
    worst = 0.0
    for k in a:
        x, y = a[k].float(), b[k].float()
        assert x.shape == y.shape, f"{k}: {x.shape} vs {y.shape}"
        rel = float((x - y).abs().max() / x.abs().max().clamp_min(1e-12))
        worst = max(worst, rel)
    print(f"{a_path} vs {b_path}: {len(a)} tensors, max relative difference {worst:.2e}")
    ok &= worst <= 1e-3
print("MERGE_OK" if ok else "MERGE_DIFFERS")
sys.exit(0 if ok else 1)
