# Zach's reply to docs/shared/gaps.md (27 Oct 2026)

This answers "Message for Dan to send Zach" in docs/shared/gaps.md.
- **Approval:** Zach, 27 Oct ~11:40 ET: "Go ahead and also queue muse".
- **Checks:** done by Zach's agent from the stored results, with no new runs.

## 1. Complement swap on stated finals: confirmed

The cells are right.
- Transfer = donor − third, as for the PM cells, from the same runs, items and eligibility.
- They are now in docs/breadth/data.csv as `swap.{q27,q9,nl}.{swapK,comp,pasteK}.{PK,TK}`. The source is each run's
  results/jswap/<run>/summary.json.

| Model | Final | J-part swap | Complement (all but the J-part) | Paste | n |
|---|---|---|---|---|---|
| 27B (jswap_v2_v1) | PK | +0.9 [0.0, 2.1] | +24.6 [18.6, 31.0] | +30.2 [24.0, 36.2] | 338 |
| 27B | TK | 0.0 [0.0, 0.0] | +27.3 [20.2, 34.9] | +36.6 [28.7, 43.6] | 227 |
| 9B (qwen35_9b_jswap_v2_v1) | PK | +4.4 [2.0, 6.8] | +13.9 [7.8, 20.4] | +20.3 [14.2, 26.9] | 259 |
| 9B | TK | −1.7 [−5.6, 0.0] | +1.7 [−11.1, 13.6] | +6.9 [−8.2, 21.8] | 58 |
| Lightning (nem35l_jswap_v2_v1) | PK | +0.4 [−0.8, 1.9] | −0.4 [−1.1, 0.0] | −0.4 [−1.2, 0.0] | 275 |
| Lightning | TK | +2.9 [0.0, 7.5] | +2.9 [−1.5, 8.6] | +2.9 [−1.5, 8.7] | 69 |

"The stated read moves with the rest of the residual, not the J-part" holds on the 27B (PK and TK) and on the 9B's
PK. The 9B's TK has n 58, and its intervals include 0. Lightning cannot say: neither the complement nor even the whole
residual (paste) moves its stated reads.

## 2. Mention-only on the recalled start: confirmed

`--positions bridge` edits every token that overlaps a mention of the bridge's word, anywhere in the prompt. The match
is case-insensitive, at a word start, with any suffix (scripts/ablate_v2.py, `bridge_positions` and
`outside_positions`).
- In jsuite_v2_test_chat, all 1,790 recalled-start facts items name the bridge exactly once, in the passage
  (`bridge_mentions` = 1), and never in the question.
- So on start M, `posbridge` is the passing mention and nothing else.
- Your cells (pos.*.M.bridge of pos.*.M.all) are the ones you need: 27B +5.8 of +45.3, 9B +10.1 of +30.4, Lightning
  +1.4 of +37.4.

## 3. 45r, 45s, Muse

- **45r:** a faithful use of the v2 knock-out. The sealed runs can be opened.
- **45s: the Lightning J++ lens is public on Hugging Face:**
  https://huggingface.co/zachperlman20/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-jpp-lens
  - File `NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jpp_lens.pt`, sha256
    `3306b6e4f0f4ba039cde5f902aeb3ef6ae8b775a7abc1b999f6cbc0b7d534f44` (pins.py's pin).
  - It uses the published lens files' layout, which `JLens` loads.
  - To put it where pins.py expects it:

    ```
    uv run python -c "from huggingface_hub import hf_hub_download; hf_hub_download('zachperlman20/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-jpp-lens', 'NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jpp_lens.pt', local_dir='cache/nemotron-3.5-lightning/lenses/jpp')"
    sha256sum cache/nemotron-3.5-lightning/lenses/jpp/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jpp_lens.pt
    ```

  - The lens was fit, and every Lightning run made, at the model revision a9904d2 with the HF-hub kernels pinned in
    pins.py; your 28017f36 is that pin.
- **Muse: queue it.** Zach's Muse runs (amendment 57 notes 1 and 4) are written as job specs in this framework. Both
  pass `jobq validate`:
  - `jobs/c3/x57_dose_muse.yaml`: amendment 54's dose grid at L36-42, about 2.0 GPU-h on an H100.
  - `jobs/c3/x57_pos_muse.yaml`: question-only and bridge-only at L36-42, about 0.6 GPU-h.
  - Their run names match Zach's other runs, so his scripts pick up the results unchanged. The order relative to 45r
    and 45s is Dan's call:

    ```
    make enqueue QUEUE=mats JOB="jobs/c3/x57_dose_muse.yaml jobs/c3/x57_pos_muse.yaml"
    ```

## 4. Thursday cross hand check

Not answered yet; Zach will reply.

## New on Zach's side since gaps.md

Amendment 57 and its notes, in docs/breadth/README.md sections 3, 6 and 9; every number is in docs/breadth/data.csv.
- **H0 on a larger numbers set.** On the 27B, a number computed from the passage needs no more J++ to key a recall than
  a read one. On the 9B and Lightning it cannot be read, because the controls also break those chains.
- **The three-hop rule replicates on a second data seed** (the 27B and Lightning).
- **Late bands:** the question takes over from the mention in the 9B (L26-29) and in Lightning (L33-39).
- **Clean-checkout reruns:** 11 of 11 row-identical, with every log-probability equal (results/checks/clean57_1027.json).
