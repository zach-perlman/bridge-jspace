"""jpp_cli_hubmamba (Zach, 2026-10-25, amendment 45): run a jpp_lens script (jpp_cli.py, jpp_grade.py) in its env with
the prebuilt HF-hub mamba-ssm registered as the mamba_ssm and causal_conv1d packages, so transformers' NemotronH takes
its Mamba kernels (the env has neither package; the torch path is ~10x slower). The same pinned kernel as the harness
(kernels-community/mamba-ssm @28017f3). Nothing is compiled or installed.
.venv/bin/python jpp_cli_hubmamba.py SCRIPT.py ARGS..."""
import importlib
import runpy
import sys
from pathlib import Path

import kernels

k = kernels.get_kernel("kernels-community/mamba-ssm", revision="28017f36635a6b94d911333812beeed5dd901ac0")
sys.modules["mamba_ssm"] = k
for sub in ("ops", "ops.triton", "ops.triton.ssd_combined", "ops.triton.selective_state_update", "ops.triton.layernorm_gated"):
    sys.modules[f"mamba_ssm.{sub}"] = importlib.import_module(f"{k.__name__}.{sub}")
sys.modules["causal_conv1d"] = importlib.import_module(f"{k.__name__}._causal_conv1d")
try:  # transformers <= 5.14 (jpp_lens's env): NemotronH loads its kernels through lazy_load_kernel; seed its table with the same build
    import transformers.integrations.hub_kernels as _hk

    _hk._KERNEL_MODULE_MAPPING["mamba-ssm"] = k
    _hk._KERNEL_MODULE_MAPPING["causal-conv1d"] = sys.modules["causal_conv1d"]
except (ImportError, AttributeError):
    pass
import transformers.utils.import_utils as _iu  # NVIDIA's Bolt code checks these flags before importing the kernels (amendment 46)

_iu.is_mamba_2_ssm_available = lambda: True
_iu.is_causal_conv1d_available = lambda: True
script = sys.argv[1]
sys.argv = [script, *sys.argv[2:]]
sys.path.insert(0, str(Path(script).resolve().parent))
runpy.run_path(script, run_name="__main__")
