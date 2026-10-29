# presentation/: captions (the speaker notes)

Built by `uv run python presentation/build.py`; every number on a figure is read from its source row. One block per figure.

## p0a_datasets

**Setup: the two datasets.** figures/shared/j0_setup.png, its top half placed on the slide canvas (not re-drawn: its text size is the shared figure's).

## p0b_tools

**Setup: the three tools.** figures/shared/j0_setup.png, its bottom half placed on the slide canvas (not re-drawn: its text size is the shared figure's).

## p1_c1_split

**C1. Recall needs the lens part; lookup does not.** Left (Zach): the lens part's top-10 J++ directions removed at every token over his band; points lost on recalled (M) and stated (K) finals (docs/breadth/data.csv ko.*.lostM / lostK; n 892 / 563 / 563 / Muse / 122B per ko.*.mk); the grey tick is the largest same-size control in M − K (max of ko.*.rot, ko.*.u, PCA ko.*.pc or pcr × mk). Muse 30B and Qwen 122B hollow (Zach: shared with the logit lens; by probability). Right (Dan): the conflict test at L, switches lost beyond a random part (docs/x0_numbers.json rc_excess_* / lk_excess_*; Lightning from figures/story/data.csv 'conflict: …'), 200 scenes per model, 95% cluster-bootstrap whiskers; the bold number is recall minus lookup (computed here). Lightning hollow (gate chosen after its pre-check); Lightning pending hand-check (29 Oct).

## p2_controls

**Same-size parts do not do it.** Left (Zach, pp): recalled minus stated answers lost without the lens part's top-10 J++ directions over his band (dark, 95% whiskers) against rotated directions, the logit lens's top 10 and same-norm PCA directions (grey), on the three clean models (docs/breadth/data.csv ko.*.mk / rot / u / pc); band ±5 pp. Right (Dan, share): the recall's switches lost beyond a random part without the lens part's 25 directions (teal, whiskers) against same-size PCA, the logit lens's directions and random lens directions (figures/story/data.csv fig02 rows; main test at L, 200 scenes); band ±0.10. On the 122B the PCA control is close (0.21 vs 0.26). Lightning has no fig02 row (not on the axis).

## p3_graded_nine

**Across nine models it is graded.** Zach's removal of the lens part's top-10 J++ directions over his band: recalled minus stated answers lost (dark, 95% whiskers; docs/breadth/data.csv ko.*.mk) against the largest same-size control (open grey: max of rotated, logit lens, PCA / size-matched); the grade under each model in Zach's words; the 122B's effect scored by probability beside (ko.q122.soft). Gemma 4, gpt-oss and Kolibri cannot be tested (the removal breaks plain text) and are not on the axis.

## p4_c2_pointer

**C2. The lens part says which entity it is: a pointer, from any context, not its fact.** Left (Zach, points): another entity D's lens part written in; answers moved to D's fact when the part comes from D's own passage (with 95% whiskers), from one neutral sentence about D, without D's own-word directions, the neutral donor rotated (grey), and a probe's subspace that reads the fact (purple; on probe-valid relations). docs/breadth/data.csv ptr.*.swap / rot, probe.*.probe; the neutral and own-word points are ptr.*.swap times the stored ratios ptr.*.neutral / noown (computed here, no interval). The cross-relation and paste rows are dropped. Right (Dan, share): what the lens part's 25 directions are, main test at L, 50 scenes per model (figures/story/data.csv 52 A rows); Lightning hatched (gate chosen after its pre-check; pending hand-check, 29 Oct); the 122B has no 52 A row in the depth README (not on the axis).

## p5_c3_address

**C3. The address: a probe finds it, a swap moves it, the lens cannot see it.** (A) a probe at the bridge word reads which locker sentence holds the item's locker (locker-first scenes; 657-758 scenes per model), against the layout baseline (dashed); the 27B's tool output (1,500 scenes) and code (682) beside. Lightning hollow; the 122B's probe ran at its gate (filled, as in the depth README). (B) the address swap by dose (dose = s / the mean real change, figures/story/data.csv fig07), 600 swaps per dose and model; ring = s = 2; Lightning and the 122B hollow (the 122B's gate lowered to 0.75 after the data); grey: a random vector at s = 4. The swap's rule fixed in advance was read at s = 1 and said no (a design error). (C) how far above 200 random vectors of the same size the lens's 25 directions rebuild the address swap (orange) and an item change (blue), in z (grey: the random vectors' 95% range, −1 to 1); 200 cases per model; the 122B has no 47.0 run in the depth README (not on the axis). Code and tool output, the 122B's rows, Lightning: pending hand-check (29 Oct).

## p6_c4_readable

**C4. Readable is not used.** At the last token, at the layer where the read peaks (under each model): read = a probe for the recall's bridge entity on the lens part of the state (dark); lens swap = the changed prompt's lens part swapped in, its switches as a share of the whole-state patch's (teal); the whole-state patch = 1 by construction (grey outline). Locker-first items; chance = the probe's chance (dashed, the highest of the four). figures/story/data.csv fig17_jspace_last_token rows. Lightning hatched (its gate chosen after its pre-check; pending hand-check, 29 Oct); the 122B has no 51.10 run in the depth README (not on the axis). Rule: '(b) readable, not used' on all four.

## p7_breaks

**Where it breaks.** Left: the lookup's switches lost beyond a random part without 25 / 50 / 100 lens directions, main test at L (docs/x0_numbers.json lk_excess_k*_27b / _122b; 200 scenes); the 27B loses 0.60 at 100, the 122B nothing. Right: Zach's named passages run through Dan's conflict test, the lookup's loss with true facts (filled) vs made-up facts (open) (figures/story/data.csv ledger_zach_named); on true facts the lookup can answer from memory. Muse and Lightning missed the made-up-fact gate: descriptive; Lightning hatched (pending hand-check, 29 Oct).

## p8_where

**Backup B1. At middle layers the bridge's mention carries it; deeper, the question does** (Zach's Finding 5). The lens part removed at all tokens, at the bridge's mention only, or in the question only, over a middle and a deeper band (docs/breadth/data.csv pos.*.all.*, late.*); Muse 30B tested only at layers 36-42 (deeper panel: ko.mu.mk, pos.mu.bridge, pos.mu.question). Fixed in advance; rotated controls cost at most 2.5 points.

## p9_routes

**Backup B2. The lookup goes by identity or position, never the value.** Routes test (another item moved), the whole change at L: shares of switched lookups naming the item's own locker (identity), the locker now at its old place (position) or the new number (value); 300 scenes per model (figures/story/data.csv fig05 rows). Lightning hollow; the 122B hollow (gate lowered to 0.75 after the data).
