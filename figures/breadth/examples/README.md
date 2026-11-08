# Figures for the breadth track's real examples

Built by `make readme` with [styles-plot](https://github.com/danorel/styles-plot) (vocabulary: [plotstyle.toml](../../../plotstyle.toml); statuses: [data/figures/status.csv](../../../data/figures/status.csv)). File names follow the document's order (figkit/layout.py); `_meta/` holds each figure's sidecar, `_sheets/` the contact sheets.

| № | figure | what it shows | status |
|---|---|---|---|
| 01 | <a href="01_fact_passage.png"><img src="01_fact_passage.png" width="260" alt="01_fact_passage"></a> | One fact passage, Qwen 27B, jsuite v2 test: both passages name the bridge (bold); the lookup's passage also states the bridge's fact (the sentence in the lookup's colour), the recall's passage replaces it and its like with sentences that do not, so the recall's answer must come from memory; the bridge in bold. | UNVERIFIED |
| 02 | <a href="02_chains.png"><img src="02_chains.png" width="260" alt="02_chains"></a> | Three three-hop chains about one entity, Qwen 27B, jsuite v2 test: each hop is P (read in the passage) or M (recalled), the bridge in bold; answers before and with the lens part removed at every token over a band of middle layers, or a rotated part of the same size. | UNVERIFIED |
