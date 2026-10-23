"""Grade a model on the J++ readout-eval items (one greedy step each, jpp_lens's rule) and write a copy of the
correctness CSV with its column added; J++'s fit-weights keeps only the items the model answers right. Generalises
gemma_it_grade.py (Zach, 2026-10-20). Run from the jpp_lens repo root, in its environment:

python /workspace/bridge-jspace/scripts/lens_fit/jpp_grade.py MODEL LAYERS OUT_CSV   (LAYERS: comma-separated)
"""

# pandas, lens_evals and workspace_lens live in the jpp_lens environment this runs in, not in this project's
# pyright: reportMissingImports=false

import sys

import pandas as pd
from lens_evals.readout_evals.readout_eval_items import MODEL_CORRECTNESS_CSV, load_readout_eval_items
from lens_evals.readout_evals.readout_evals import ReadoutEvalRunner
from workspace_lens import get_hf_model

name, layers, out = sys.argv[1], [int(x) for x in sys.argv[2].split(",")], sys.argv[3]
model = get_hf_model(name, attn_implementation="sdpa")
items = load_readout_eval_items()
df = ReadoutEvalRunner(model, {}, layers=layers).grade_model_correctness(items, hf_model_name=name)  # no lens needed
base = pd.read_csv(MODEL_CORRECTNESS_CSV)
merged = (base.drop(columns=[name]) if name in base.columns else base).merge(df, on=["eval", "item"], how="outer")
merged.to_csv(out, index=False)
print(df[name].value_counts(dropna=False).to_dict(), "of", len(df))
