# Figures for the LessWrong write-up

Built by `make figures-writeup` (`figkit/tables.py --target writeup`, layouts in `src/bridge_jspace/figkit/writeup_figs.py`): 8.0 in at 200 dpi (1600 px wide, shown at about 720 px in the post's column), nothing under 11 pt, no title inside the image (the caption lives in the post), white background. `contact_sheet.png` shows every figure at 720 px in post order. Every number is read from a data file by code; nothing is typed.

Status: UNVERIFIED. No figure here has been hand-checked against its run files yet.

| Post | File | Takeaway (the post's sentence, not drawn) | Data keys | Source files | Fixed in advance / post hoc | Hand-check |
|---|---|---|---|---|---|---|
| 1 | `fig01_main_split.png` | Taking the lens part out breaks recalled answers, not lookup ones | band: `ko.<m>.lostK`, `ko.<m>.lostM`, `ko.<m>.mk`, the largest of `ko.<m>.rot` / `.u` / `.pc` (or `.pcr` × `.mk`); one layer: `x0_numbers.json` `rc_excess_*`, `lk_excess_*`, `contrast_*`, else `data/figures/depth/data.csv` "conflict: …, switches lost beyond a random part" | `docs/breadth/data.csv` (its `source` column: `results/ablate_v2/jsuite2_score/*_ko_cand2_v1.json`), `docs/depth/x0_numbers.json`, `data/figures/depth/data.csv` | band: Muse 30B and Qwen 122B post hoc (hollow) and not claimed (grey); one layer: Lightning post hoc | not yet |
| 5 | `fig05_controls.png` | Same-size removals cost a fraction of what the lens part costs | band: `ko.<m>.mk`, `.rot`, `.u`, `.pc` (or `.pcr` × `.mk`), `f2.band.<m>.<largest>`; one layer: `data/figures/depth/data.csv` figure `fig02` (J++ part / PCA / logit-lens / random: recall extra loss), `f2.layer.<m>.pca` | `docs/breadth/data.csv`, `data/figures/depth/data.csv` (runs `*_x0_pcaeq`, `*_x0_parts`, `*_x0_necessity*`) | band: Muse 30B and Qwen 122B post hoc (hollow) | not yet |
