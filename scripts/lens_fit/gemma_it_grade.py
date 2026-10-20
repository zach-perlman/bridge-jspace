"""Grade google/gemma-4-31B-it on the J++ readout-eval items (one greedy step each, the library's rule) and write a
copy of the correctness CSV with its column added. Run from the jpp_lens repo root."""

import sys

import pandas as pd
from lens_evals.readout_evals.readout_eval_items import MODEL_CORRECTNESS_CSV, load_readout_eval_items
from lens_evals.readout_evals.readout_evals import ReadoutEvalRunner
from workspace_lens import get_hf_model

name, out = "google/gemma-4-31B-it", sys.argv[1]
model = get_hf_model(name, attn_implementation="sdpa")
items = load_readout_eval_items()
df = ReadoutEvalRunner(model, {}).grade_model_correctness(items, hf_model_name=name)
merged = pd.read_csv(MODEL_CORRECTNESS_CSV).merge(df, on=["eval", "item"], how="outer")
merged.to_csv(out, index=False)
print(df[name].value_counts(dropna=False).to_dict(), "of", len(df))
