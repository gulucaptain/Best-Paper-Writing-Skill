# Card: VGGT (CVPR 2025)

- **Paper type**: L2 new capability (with L1)
- **Motivation type**: `trend` — the field is moving in one direction; this work takes the next (near-final) step
- **Route**: Intro: history in three stages → “Even so … still” → “we ask if, finally …” → closest work with two checkable limits → C:V1 (one model, several advantages) · Abstract: “We present X, a …”
- Full Chinese breakdown: `docs/拆解/01_VGGT.md` in the parent repository.

## One-line claim
A standard large transformer with minimal 3D inductive bias, trained on many 3D-annotated datasets, predicts cameras, depth, point maps and tracks for one to hundreds of views in one forward pass, and often outperforms optimization-based pipelines without post-processing.

## Move sequence (Introduction)

| # | Move | What the paper does |
|---|---|---|
| 1 | Problem + approach in one sentence | “… utilizing a feed-forward neural network” |
| 2–4 | Three-stage history | pure geometry → learning as complement → end-to-end integration |
| 5 | Gap (cost) | “Even so, visual geometry *still* plays a major role …” |
| 6 | Research question as trend extrapolation | “we ask if, finally, … almost entirely” |
| 7 | Closest work + two checkable limits | two images at once; relies on post-processing |
| 8 | Calibrated positioning | “a further step towards” |
| 9–12 | Method answering each limit + result | one to hundreds of views; single forward pass; “often outperforms” |
| 13 | Named departure | DUSt3R, MASt3R, VGGSfM still need post-optimization |
| 14–18 | Side claim A with an honest exception | “no particular 3D … biases (except for …)”; analogy to GPT/CLIP/DINO |
| 19–23 | Side claim B, pre-empting an objection | multi-task “despite potential redundancies” |

## Sentences worth studying

> Even so, visual geometry still plays a major role in 3D reconstruction, which increases complexity and computational cost.
> — VGGT · CVPR 2025 · p.1

> As networks become ever more powerful, we ask if, finally, 3D tasks can be solved directly by a neural network, eschewing geometry post-processing almost entirely.
> — VGGT · CVPR 2025 · p.1

> In this paper, we take a further step towards removing the need to optimize 3D geometry in post-processing.
> — VGGT · CVPR 2025 · p.2

> Instead, VGGT is based on a fairly standard large transformer, with no particular 3D or other inductive biases (except for alternating between frame-wise and global attention), but trained on a large number of publicly available datasets with 3D annotations.
> — VGGT · CVPR 2025 · p.2

## Why it works
1. **History does the persuading**: three stages make “still” and “finally” feel earned.
2. **Claim strength is set by the weakest result**: BA still helps (Table 1), so the intro says “almost entirely”, “a further step towards”, “often”.
3. **Closest work is limited on exactly two checkable points**, and the method answers both.
4. **Strong claims carry their exception in parentheses**, which pre-empts the obvious reviewer objection.
5. **Table design carries the argument**: “Known GT camera” and time columns turn a non-win into a supported claim.

## When to use this route
Only when your work is the next step of a visible trend. If your paper fixes a specific failure, use the `failure` route instead; a grand historical opening on an incremental contribution reads as overclaiming.

## Transferable skeleton
```text
We consider the problem of [task] using [approach category].
Traditionally, [task] has been approached with [old paradigm]. [New technique] has played a complementary
role, addressing [subproblems]. The integration has become increasingly tight: [latest SOTA] combines
[new] and [old] via [mechanism]. Even so, [old paradigm] still [dominates], which [cost].
As [enabling factor] improves, we ask whether [task] can be solved directly by [new technique],
[removing old component] almost entirely. [Closest work] has shown promising results in this direction,
but [checkable limit 1] and [checkable limit 2].
In this paper, we take a further step towards [goal] by introducing [Name], which [answers limit 1]
and [answers limit 2]. [Result, calibrated: often / comparable]. This is a substantial departure from
[X], which still require [cost].
```
