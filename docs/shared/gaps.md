Draft, 27 Oct; UNVERIFIED; for Dan. Experiments freeze Wed 28 Oct evening; hand check Thu 29 Oct (STATUS.md, d0ee653b)

# Gaps in the joint story

Every claim × model cell that docs/shared/joint_README_draft.md needs and that is empty or conflicting in docs/shared/grid.csv (G) or the two reports. Before proposing a run I checked whether Zach's stored results already fill the cell. Two cells are filled from his stored summaries (rows 3 and 4); they need his confirmation, not a run. Source keys as in docs/shared/joint_story_draft.md.

Ranked by how much the result would change the story.

| # | Cell (claim × model) | State | What is missing | Test that fills it | Who / box | GPU-h | Lands before the freeze? |
|---|---|---|---|---|---|---|---|
| 1 | Carried vs needed × Muse | **Conflict.** Ours: J++-specific at L26 (0.66 vs logit lens 0.01; D fig02). His: knock-out at L36-42 +59.9 with the logit lens at +34.6 (Z ko.mu.mk, ko.mu.u); toy suite gap 7 (E l.87) | Both methods at overlapping layers on Muse | **45r** (drafted, not queued; Q46.1 in predictions/2026-10-27_dan.md, answered by Dan (cbf2f47b: carried, not needed 65%); also waits for Zach's OK that it is a faithful use of his knock-out). His knock-out on L23-29 with all controls vs our stored L26 gap 0.85; needed = M − K ≥ 15 and more than 10 above the logit lens's (Q46.1; spec jobs/c3/x45r_ko_l23_29_muse.yaml on danorel) | Our box (mats). Muse's weights are not cached on Zach's box (E l.246) | 2.1-2.4 for the rule's run (x45r_ko_l23_29_muse) + 0.5-0.6 descriptive L26 (x45r_ko_l26_muse) + 0.5-0.6 optional size-matched control at L36-42 (x45r_ko_band_muse); the specs' arithmetic, an H200-to-H100 factor of 1.3-1.5 assumed. Our side needs no run (stored L26 gap) | Yes, if Q46.1 is answered and the job is queued by Wed midday |
| 2 | Recall vs in-context split × Lightning (our change-removal: main test and clean one-pick design) | **Empty** (G: depth column "-" for Lightning on every row) | Our change-removal split on his strongest second-family model, where his knock-out is the only evidence and his passing-mention effect is ~0 (+4.0, Z r.nl) | **45s** (Q46.2-Q46.3, unanswered; layer fixed in advance L30, inside his L27-33, 3a4637ad; no specs yet). 45s has no routes or order-pointer arms | Our box, after Zach sends the Lightning lens file (blocked) | [US: no committed estimate; Muse's 45m was estimated at 0.6 (ledger_sesterce-h100x2)] | Only if the lens file arrives by Wed morning |
| 3 | In-context read under transplants × 27B / 9B / Lightning (complement swap on K finals) | **Filled from stored results, unreported** | Complement (all but the J-part) on PK / TK: 27B +24.6 [18.6, 31.0] / +27.3 [20.2, 34.9]; 9B +13.9 [7.8, 20.4] / +1.7 [−11.1, 13.6]; Lightning −0.4 / +2.9; J-part swap on PK: 0.9 / 4.4 / 0.4 (JS jswap_v2_v1, qwen35_9b_jswap_v2_v1, nem35l_jswap_v2_v1) | No run. Zach confirms the cells and adds them to docs/breadth/data.csv | Zach, CPU | 0 | Yes |
| 4 | Passing-mention localisation × 27B / Lightning | **Filled, if the token set is what I think** | Knock-out at the bridge's mention only, recalled start (the only mention is the passing one, reading of the v2 design): 27B +5.8 [3, 9] of +45.3, 9B +10.1 of +30.4, Lightning +1.4 [0, 3] of +37.4 (Z pos.*.M.bridge, pos.*.M.all) | No run. Zach confirms that `posbridge` on start M covers exactly the passing-mention tokens | Zach, CPU | 0 | Yes |
| 5 | Lens specificity of the knock-out × Muse (size-matched control) | **Empty** (G "not variance" row: Muse "-") | paper10_pcasize at L36-42 | x45r_ko_band_muse (optional part of 45r) | Our box | 0.55 | Yes, if 45r runs |
| 6 | Where (mention vs question) and dose × Muse, his side | **Empty**: amendment 57 note 1 did not run (weights not cached; E l.246) | Muse's position split and dose grid at L36-42 | Zach's amendment 57 note 1 jobs, on our box (Muse is cached there) | Our box, Zach's specs | [US: no estimate in a committed spec] | Unlikely; cut first |
| 7 | J-part swap × 122B / Muse on v2 | **Empty on v2** (G); v1 runs exist: 122B +44.3, stated reads kept 97-100% (E l.162); Muse +50.3 at the exploratory L14-20, "uninformative" at L36-42 (E l.161) | v2 versions | Not needed for the story: cite the v1 runs, labelled v1 | – | 0 | – |
| 8 | Anything model-level × 122B | **Both weak**: ours not specific vs PCA (0.26 vs 0.21; D fig02); his +1.7 by probability (Z ko.q122.soft); no 45m/45p/45q on the 122B | – | **No run proposed**: drop the 122B from claims, keep it in the grid | – | 0 | – |
| 9 | Order pointer / routes × Lightning, and on his toy-suite locker items × 27B | **Empty** | Whether the order pointer exists outside our three models and our scenes (his knock-out leaves the toy-suite locker lookup at 99-100%, E l.73) | No test planned (45s has no routes or order-pointer arms) | Our box | [US] | No; after the freeze |
| 11 | J-part swap × Lightning (claim 2) | **Formally uninformative**: +44.8 with in-context reads kept ≥ 98%, but the paste ceiling is +13.8 < 20 (E l.209; prereg_replication_1022.md l.1175-1176) | A pre-registered reading on Lightning | No test planned; claim 2 counts the 9B and 27B only | – | 0 | – |
| 10 | Cross hand check × both headlines | **Empty** (no number is hand-checked in either track) | 10 random items of each other's headline | Thursday hand check (items below) | Both, CPU | 0 | Thu 29 Oct |

## Cross hand check: item ids (seed 0, reproducible)

Procedure (helper: scratchpad handcheck_ids.py, re-implementable in a few lines):

- **Ours → Zach checks.**
  - Our main test (two people swap picks), chat, the layer fixed in advance.
  - The scenes in results/x0_necessity/<run>/outcomes.jsonl at that layer, sorted.
  - `random.Random(0).sample(scenes, 10)`, the convention of docs/handcheck_pack.md.
- **His → Dan checks.**
  - His v2 headline items: facts module, starts P / M / T, final M or K, right unedited (condition "none" correct).
  - Taken from results/ablate_v2/<run>/rows.jsonl with data/tasks_v2/jsuite_v2_test_chat/items.jsonl, sorted by id.
  - `random.Random(0).sample(ids, 10)`.
- The pool sizes match the headline n: 892 M + 892 K = 1784 on the 27B (Z ko.q27.mk n 892); 1127 on the 9B (n 563 M).

Primary set: the 27B, the model both headlines share at the same site (our L32 is the first layer of his L32-40). Backup: the 9B.

| Direction | Model, run | Pool | 10 items (seed 0) |
|---|---|---|---|
| Zach checks ours | 27B, x0_necessity_27b_chat, L32 | 200 scenes | P2-L0-0102, P2-L0-0204, P2-L0-0111, P2-L0-0010, P2-L0-0069, P2-L0-0136, P2-L0-0130, P2-L0-0107, P2-L0-0080, P2-L0-0128 |
| Dan checks his | 27B, jsuite_v2_test_chat_ko_cand2_v1 | 1784 items | j2:chat:facts:TM-L1-01074 (M), PK-L0-01507 (K), TK-L1-02049 (K), PK-L1-00445 (K), MK-L0-00965 (K), MM-L1-00518 (M), PM-L0-00577 (M), PM-L0-00016 (M), PK-L1-00151 (K), TM-L0-00897 (M) |
| Backup: Zach checks ours | 9B, qwen35_9b_x0_necessity, L12 | 200 scenes | P2-L0-0142, P2-L0-0290, P2-L0-0154, P2-L0-0017, P2-L0-0096, P2-L0-0193, P2-L0-0184, P2-L0-0149, P2-L0-0110, P2-L0-0181 |
| Backup: Dan checks his | 9B, qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1 | 1127 items | j2:chat:facts:PM-L0-00571 (M), PM-L0-01750 (M), MK-L0-01253 (K), PK-L0-00571 (K), TK-L1-00255 (K), PM-L1-01897 (M), PM-L0-01225 (M), PK-L1-00154 (K), PM-L1-01615 (M), PK-L1-01864 (K) |

What to check per item:
- **Ours:** the decoded prompt, the asked pick, the expected lookup digit and recall fact, and each reader's stored answer under none / whole / without J++ / without the random part (as docs/handcheck_pack.md).
- **His:** the expected answer is right; a K item states the fact and an M item does not; the answer under paper10 is as stored (as docs/verify_kit.md §2).

## Message for Dan to send Zach

> Hi Zach — for the joint write-up and Thursday's hand check, four things. No new runs from your box unless you want them.
>
> 1. **Complement swap on stated finals: already in your results, please confirm.** Your v2 swap summaries have swap_comp (all but the J-part) on the K finals. They are not in docs/breadth/data.csv:
>    - 27B (results/jswap/jswap_v2_v1/summary.json): PK/swap_comp transfer +24.6 [18.6, 31.0], TK +27.3 [20.2, 34.9]; vs the J-part swap PK +0.9, TK 0.0.
>    - 9B (qwen35_9b_jswap_v2_v1): PK +13.9 [7.8, 20.4], TK +1.7 [−11.1, 13.6]; J-part PK +4.4.
>    - Lightning (nem35l_jswap_v2_v1): PK −0.4, TK +2.9; paste also ≈ 0.
>
>    Are these the right cells (transfer = donor − third, same eligibility as your PM numbers)? If yes, could you add them to data.csv (keys like swap.q27.comp.PK)? We want to quote them as "the stated read moves with the rest of the residual, not the J-part" on the Qwens.
> 2. **Passing-mention localisation: please confirm the token set.** We read your Z pos.*.M.bridge cells (27B +5.8 of +45.3, 9B +10.1 of +30.4, Lightning +1.4 of +37.4) as "knock-out at the passing mention only", since on the recalled start the passing sentence is the bridge's only mention. Is that what `posbridge` covers for start M? If not, the cell we need is the knock-out at the passing mention only, on the 27B and Lightning (MM items).
> 3. **45r (Muse) and 45s (Lightning).**
>    - 45r (Q46.1) runs your v2 knock-out on Muse at L23-29 with all your controls, against our stored L26 gap, on our box: your box has no Muse weights (amendment 57 note 1). Is that a faithful use of your knock-out? Dan queues it only after your OK.
>    - 45s (Q46.2-Q46.3) runs our main test and clean design on Lightning at L30, inside your L27-33. It needs your Lightning J++ lens file (path and sha) on our box by Wed morning to land before the freeze (Wed 28 Oct evening).
>    - OK to add your Muse position split / dose specs to our queue after 45r if there is time?
> 4. **Thursday cross hand check, 10 random items each (seed 0, sorted pool, random.Random(0).sample).**
>    - You check ours: 27B main test (x0_necessity_27b_chat, L32) scenes P2-L0-0102, P2-L0-0204, P2-L0-0111, P2-L0-0010, P2-L0-0069, P2-L0-0136, P2-L0-0130, P2-L0-0107, P2-L0-0080, P2-L0-0128 (cards as in docs/handcheck_pack.md).
>    - Dan checks yours: 27B jsuite_v2_test_chat_ko_cand2_v1 items TM-L1-01074, PK-L0-01507, TK-L1-02049, PK-L1-00445, MK-L0-00965, MM-L1-00518, PM-L0-00577, PM-L0-00016, PK-L1-00151, TM-L0-00897 (prefix j2:chat:facts:).
>    - Backup sets on the 9B are in docs/shared/gaps.md.
