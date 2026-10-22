"""Upload a fitted J++ lens to the Hub (Dan's account), with a README of its provenance; print the commit to pin.

The token comes only from the environment of this one command (HF_TOKEN), streamed over ssh from the Mac's .env; it is
never written to the box's disk:
  grep '^HF_TOKEN=' .env | cut -d= -f2- | tr -d '"' | ssh BOX 'read -r T; HF_TOKEN=$T ~/work/jpp_lens/.venv/bin/python \
      ~/work/bridge-jspace/scripts/lens_fit/hf_upload.py --repo Qwen3-32B-jpp-lens --file F --sha256 S --note N [--public]'
"""

import argparse
import hashlib
import os
import tempfile
from pathlib import Path

from huggingface_hub import HfApi


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="the repo name under the token's account")
    ap.add_argument("--file", required=True, type=Path)
    ap.add_argument("--sha256", required=True)
    ap.add_argument("--note", required=True, help="the provenance line (recipe, prompts, seed, date)")
    ap.add_argument("--public", action="store_true", help="default: private")
    a = ap.parse_args()
    token = os.environ.get("HF_TOKEN", "").strip().strip('"').strip("'")
    assert token, "HF_TOKEN is not set for this command"
    assert sha256_file(a.file) == a.sha256, f"{a.file}: sha256 differs from {a.sha256}"
    api = HfApi(token=token)
    repo_id = f"{api.whoami()['name']}/{a.repo}"
    api.create_repo(repo_id, private=not a.public, exist_ok=True)
    readme = (f"# {a.repo}\n\n{a.note}\n\nFile: `{a.file.name}` (fp16 J maps, cast to fp32 on load), sha256 `{a.sha256}`.\n\n"
              "Fit with the published J++ recipe (safety-research/jpp_lens@93f02cd) for the bridge-jspace project.\n")  # fmt: skip
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "README.md").write_text(readme)
        api.upload_file(path_or_fileobj=str(Path(d) / "README.md"), path_in_repo="README.md", repo_id=repo_id)
    info = api.upload_file(path_or_fileobj=str(a.file), path_in_repo=a.file.name, repo_id=repo_id)
    print("repo", repo_id, "commit", getattr(info, "oid", None) or api.model_info(repo_id).sha, "private", not a.public)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
