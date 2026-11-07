# Figure style

Every figure in this repo is drawn with [styles-plot](https://github.com/danorel/styles-plot), pinned in `pyproject.toml`. Its grammar (colour = role, hollow = post hoc, keys built from what is drawn, the checks that refuse a figure that breaks a rule) is in the library's [docs/GRAMMAR.md](https://github.com/danorel/styles-plot/blob/main/docs/GRAMMAR.md).

What is this project's:

- [`plotstyle.toml`](../../plotstyle.toml): the vocabulary (roles and their colours, controls, units, words, banned variants, models).
- [`data/figures/status.csv`](../../data/figures/status.csv): each drawn cell's status (fixed in advance or post hoc; claimed, descriptive or not claimed), written by `scripts/status_registry.py` with its source.
- `src/bridge_jspace/figkit/*_sp*.py`: the builders, one module per set; `src/bridge_jspace/figkit/layout.py`: the sets' folders and file names; `src/bridge_jspace/figdata.py`: the data they read.
- `figures/<set>/README.md`: each set's index (writeup, readme, depth, breadth).

`make figures-writeup` and `make readme` build the sets, check them (`styles-plot check`) and write their contact sheets; `tests/test_figure_layout.py` keeps every set flat and every doc's figure link alive.
