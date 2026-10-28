# Card: Mip-Splatting (CVPR 2024)

- **Paper type**: L1 method improvement
- **Motivation type**: `failure` — a strong method breaks under a specific, reproducible condition
- **Route**: Intro A:V2 → B:diagnosis (symptom → mechanism) → C:V2 (two contributions, each answering one symptom) · Abstract V2

## One-line claim
Constraining the 3D representation by the input sampling rate (3D smoothing filter) and replacing screen-space dilation with a box-filter approximation (2D Mip filter) removes the zoom-in and zoom-out artifacts of 3DGS when training at a single scale.

## Move sequence (Introduction)

| # | Move | What the paper does |
|---|---|---|
| 1 | Task + importance | NVS → NeRF → 3DGS: a short lineage ending at the method being fixed |
| 2 | Credit the baseline | “impressive results … real-time rendering” before criticising it |
| 3 | Mechanism of the baseline | One sentence on how 3DGS renders, incl. the 2D dilation step that will later be blamed |
| 4 | Failure condition | “when camera views diverge from those seen during training, such as zoom in and zoom out” + Fig. 1 |
| 5 | Root cause | Names two causes, then explains each symptom mechanistically |
| 6 | Key insight | Sampling theory bounds the reconstructable frequency |
| 7 | Contribution 1 → symptom 1 | 3D smoothing filter → zoom-in artifacts |
| 8 | Remaining problem | “Nonetheless, … zooming out results in aliasing” |
| 9 | Contribution 2 → symptom 2 | 2D Mip filter → aliasing / dilation |
| 10 | Contrast + benefit | Closed-form vs. MLP interpolation → out-of-distribution generalization |
| 11 | Contributions list | Analysis / filter 1 / filter 2 / experiments |

## Sentences worth studying

> Although 3DGS has demonstrated impressive NVS results, it produces artifacts when camera views diverge from those seen during training, such as zoom in and zoom out, as illustrated in Figure 1.
> — Mip-Splatting · CVPR 2024 · p.2

> Specifically, zooming out leads to a reduced size of the projected 2D Gaussians in screen space, while applying the same amount of dilation results in dilation artifacts.
> — Mip-Splatting · CVPR 2024 · p.2

> Our key insight is that the highest frequency that can be reconstructed of a 3D scene is inherently constrained by the sampling rates of the input images.
> — Mip-Splatting · CVPR 2024 · p.2

> Nonetheless, rendering the reconstructed scene at lower sampling rates (e.g., zooming out) results in aliasing.
> — Mip-Splatting · CVPR 2024 · p.2

## Why it works
1. **Failure is reproducible and visual**: a reader can picture “zoom in/out” immediately; Fig. 1 shows it.
2. **The baseline’s mechanism is introduced before it is blamed** (step 3), so the root cause (step 5) does not feel like a jump.
3. **Symptom → mechanism, not just “X is limited”**: each artifact is explained by what changes (projected size) and what stays fixed (dilation).
4. **Two contributions, two symptoms**: the “Nonetheless” sentence turns the second contribution into an answer, not an add-on.

## Caution (do not imitate)
The abstract contains small errors (“to constrains”, “such a training”) and a redundant causal phrase (“the source for this phenomenon can be attributed to”). Imitate the structure, not the wording.

## Transferable skeleton
```text
[Method] has demonstrated [specific success]. Specifically, it [mechanism, incl. the component you will blame].
Although [Method] [credit], it produces [observable failure] when [reproducible condition] (Fig. 1).
We find that this stems from [cause 1] and [cause 2]. Specifically, [condition] changes [quantity A],
while [component] remains fixed, causing [artifact].
Our key insight is that [principle that bounds/explains the quantity].
Based on this, we [contribution 1], which [removes symptom 1].
Nonetheless, [remaining symptom] persists when [condition 2]. We therefore [contribution 2], which [mechanism].
In contrast to [prior approach that relies on X], our [closed-form/explicit] design [benefit beyond training conditions].
```
