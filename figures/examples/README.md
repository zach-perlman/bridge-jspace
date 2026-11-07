# Figures for the root README's real examples

Built by `make readme` with [styles-plot](https://github.com/danorel/styles-plot) (vocabulary: [plotstyle.toml](../../plotstyle.toml); statuses: [data/figures/status.csv](../../data/figures/status.csv)). File names follow the document's order (figkit/layout.py); `_meta/` holds each figure's sidecar, `_sheets/` the contact sheets.

| № | figure | what it shows | status |
|---|---|---|---|
| 01 | <a href="01_locker_scene.png"><img src="01_locker_scene.png" width="260" alt="01_locker_scene"></a> | One real locker scene, Qwen 27B: the whole change switches both readers; without the lens part the lookup still switches and the recall does not | UNVERIFIED |
| 02 | <a href="02_fact_passage.png"><img src="02_fact_passage.png" width="260" alt="02_fact_passage"></a> | One real fact passage, Qwen 27B: the final fact stated for the lookup, left to memory for the recall | UNVERIFIED |
| 03 | <a href="03_routes.png"><img src="03_routes.png" width="260" alt="03_routes"></a> | One real routes scene, Qwen 9B: the three routes predict three lockers; the lookup takes the identity route's | UNVERIFIED |
| 04 | <a href="04_chains.png"><img src="04_chains.png" width="260" alt="04_chains"></a> | One real entity, Qwen 27B: only the chain that ends in two recalls turns wrong, and only without the lens part | UNVERIFIED |
