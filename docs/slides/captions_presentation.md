# Captions (the speaker notes)

Built by `uv run python -m bridge_jspace.figkit.build --target slide` from src/bridge_jspace/figkit/specs.py.

## p0a_datasets

**One question, two kinds of answer, two datasets.** figures/shared/j0_setup.png, its top half (a diagram, not re-drawn).

## p0b_tools

**Three tools, one target: the lens part at the bridge.** figures/shared/j0_setup.png, its bottom half (a diagram, not re-drawn).

## p1_c1_split

**Recall needs the lens part; lookup does not.** Left (Zach, pp): the lens part's top-10 J++ directions removed at every token over his band; points lost on recalled (M, dark) and stated (K, purple) finals (docs/breadth/data.csv ko.*.lostM / lostK); grey tick: the largest same-size control in M − K (rotated, logit lens, PCA). Muse 30B: shared with the logit lens; Qwen 122B: gone by probability (Zach's grading). Right (Dan, share): the conflict test at L, switches lost beyond a random part (docs/x0_numbers.json rc_excess_* / lk_excess_*; Lightning from data/figures/depth/data.csv), 200 scenes per model, 95% whiskers; bold: recall minus lookup (contrast_*); dashed: the lookup's 0.10 bar. Lightning hollow (gate chosen after its pre-check; pending hand-check, 29 Oct).

## p2a_controls_zach

**Same-size parts do not do it (Zach).** Recalled minus stated answers lost when the lens part's top-10 J++ directions are removed over his band (teal, 95% whiskers) against rotated directions, the logit lens's top 10 and same-norm PCA directions (grey; docs/breadth/data.csv ko.*.rot / u / pc), on the three clean models.

## p2b_controls_dan

**Same-size parts do not do it (Dan).** The recall's switches lost beyond a random part without the lens part's 25 directions (teal, 95% whiskers) against same-size PCA directions, the logit lens's directions and random lens directions (grey), main test at L, 200 scenes (data/figures/depth/data.csv fig02 rows). On the 122B the PCA control is close (0.21 vs 0.26). Lightning has no fig02 row.

## p3_graded_nine

**Across nine models it is graded.** Zach: recalled minus stated answers lost without the lens part's top-10 directions over his band (dark, 95% whiskers; ko.*.mk) against the largest same-size control (grey tick); his grade under each model; dashed: the plan's +30 bar. The 122B scored by probability: 1.7 (ko.q122.soft). Gemma 4, gpt-oss and Kolibri cannot be tested (the removal breaks plain text).

## p4a_pointer_zach

**The lens part says which entity it is: a pointer, from any context.** Zach: another entity D's lens part written in over his band; answers moved to D's fact when the part comes from D's own passage (95% whiskers), one neutral sentence about D, without D's own-word directions, the neutral donor rotated (grey), and a probe's subspace that reads the fact (purple; probe-valid relations). docs/breadth/data.csv ptr.*, probe.*.probe; the neutral and own-word bars are ptr.*.swap times the stored ratios (no interval). Cross-relation and paste rows dropped.

## p4b_atoms_dan

**The lens part's 25 directions are the bridge words, never the answer.** Dan: share of the rebuilt energy by the kind of lens word, main test at L, 50 scenes per model (data/figures/depth/data.csv 52 A rows). The answer word's share: Qwen 9B 0.00, Qwen 27B 0.00, Muse 30B 0.00, Lightning ○ 0.00. Lightning hollow (pending hand-check, 29 Oct); the 122B has no 52 A row in the depth README.

## p5a_probe

**A probe at the bridge word reads which locker sentence holds the item's locker.** Locker-first scenes (657-758 per model); dashed: the layout baseline; right of the line: the 27B's tool output (1,500 scenes) and code (682), lookup-only gate. Lightning hollow; the 122B's probe ran at its gate (filled). Tool output and code: pending hand-check (29 Oct).

## p5b_swap_dose

**The address swap moves the lookup.** Lookups answering the swapped-in locker by dose (s / the mean real change; data/figures/depth/data.csv fig07), 600 swaps per dose and model; dot: s = 2 (about a real change's size) with its value; grey band: a random vector at s = 4; dashed: a real change. The swap's rule fixed in advance was read at s = 1 and said no on every model (a design error). Lightning and the 122B thinner (after the data; the 122B's gate lowered to 0.75).

## p5c_lens_readout

**The lens cannot see the address.** How far above 200 random vectors of the same size the lens's 25 directions rebuild the address swap (orange) and an item change of the same size (blue, the positive control), in z (grey band: the random vectors' 95% range); 200 cases per model (data/figures/depth/data.csv fig07b_verbal). Lightning hollow; the 122B has no 47.0 run in the depth README.

## p6_c4_readable

**Readable is not used.** At the last token, at the layer where the read peaks (under each model): read = a probe for the recall's bridge entity on the lens part of the state (dark); lens swap = the changed prompt's lens part swapped in, its switches as a share of the whole-state patch's, which switches 0.95-1.00 (teal); dashed: the probe's chance. Locker-first items (data/figures/depth/data.csv fig17_jspace_last_token). Rule: '(b) readable, not used' on all four. Lightning hollow (pending hand-check, 29 Oct); the 122B has no 51.10 run in the depth README.

## p7_breaks

**Where it breaks: the 27B with more directions; passages whose fact the model knows.** Left: the lookup's switches lost beyond a random part without 25 / 50 / 100 lens directions, main test at L, 200 scenes (docs/x0_numbers.json lk_excess_k*). Right: Zach's named passages through Dan's conflict test, the lookup with true facts (purple) and made-up facts (dark) (data/figures/depth/data.csv ledger_zach_named). Muse and Lightning missed the made-up-fact gate (descriptive); Lightning hollow (pending hand-check, 29 Oct). Dashed: the lookup's 0.10 bar.

## p8_where

**At middle layers the bridge's mention carries it; deeper, the question does.** Zach's Finding 5: the lens part removed at all tokens (dark), the bridge's mention only (teal) or the question only (purple), over a middle and a deeper band (docs/breadth/data.csv pos.*.all.*, late.*); Muse 30B tested only at layers 36-42. Fixed in advance; rotated controls cost at most 2.5 points.

## p9_routes

**The lookup goes by identity or position, never the value.** Routes test (another item moved), the whole change at L: shares of switched lookups naming the item's own locker (identity) or the locker now at its old place (position); the new number (value): Qwen 9B 0.00, Qwen 27B 0.00, Muse 30B 0.00, Lightning ○ 0.00, Qwen 122B 0.00. 300 scenes per model (data/figures/depth/data.csv fig05 rows). Lightning hollow; the 122B hollow (gate lowered to 0.75 after the data).
