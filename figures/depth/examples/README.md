# Figures for the depth track's real examples

Built by `make readme` with [styles-plot](https://github.com/danorel/styles-plot) (vocabulary: [plotstyle.toml](../../../plotstyle.toml); statuses: [data/figures/status.csv](../../../data/figures/status.csv)). File names follow the document's order (figkit/layout.py); `_meta/` holds each figure's sidecar, `_sheets/` the contact sheets.

| № | figure | what it shows | status |
|---|---|---|---|
| 01 | <a href="01_locker_scene.png"><img src="01_locker_scene.png" width="260" alt="01_locker_scene"></a> | One locker scene from the main test, Qwen 27B, as the model reads it (the bridge word in bold), with each reader's answer before the change and under each operation at layer `{{x\|layer_27b}}`. | UNVERIFIED |
| 02 | <a href="02_routes.png"><img src="02_routes.png" width="260" alt="02_routes"></a> | One routes scene, Qwen 9B: the bridge word's state comes from a scene in which another item moved, and the three routes predict three different lockers, each read from its own sentence (identity blue, position amber, the value in black). | UNVERIFIED |
