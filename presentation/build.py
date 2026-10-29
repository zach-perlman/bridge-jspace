"""The deck's figures: a shim over the figure kit (figures/kit). Specs: figures/kit/specs.py; look: figures/kit/theme.py.

uv run python presentation/build.py [ids]     (= uv run python -m figures.kit.build [ids] --target slide)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from figures.kit.build import main

if __name__ == "__main__":
    sys.argv = [sys.argv[0], *sys.argv[1:], "--target", "slide"]
    sys.exit(main())
