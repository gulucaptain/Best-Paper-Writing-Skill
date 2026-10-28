# Card: Mip-NeRF (ICCV 2021)

- **Paper type**: L1 method improvement
- **Motivation type**: `cost` — the obvious fix exists but is prohibitively expensive
- **Route**: Intro A:V2 → B: failure + rule out the obvious fix → borrow a principle from another field → C:V1 (one contribution, several advantages) · Abstract V1

## One-line claim
Rendering cones instead of rays, with an integrated positional encoding over conical frustums, gives NeRF built-in anti-aliasing (pre-filtering), reducing error by 60% on a multiscale benchmark while being slightly faster and half the size.

## Move sequence (Introduction)

| # | Move | What the paper does |
|---|---|---|
| 1 | Task + credit | NeRF “emerged as a compelling strategy” |
| 2 | Thesis of the flaw | “NeRF’s rendering model is flawed in a manner that can cause excessive blurring and aliasing” |
| 3 | Mechanism | single ray per pixel |
| 4 | When it breaks | content observed at multiple resolutions; contrived vs. less contrived settings |
| 5 | Rule out the obvious fix | supersampling → prohibitively expensive, with numbers |
| 6 | Borrowed principle | mipmapping / pre-filtering from graphics |
| 7 | Contribution | mip-NeRF + IPE |
| 8 | Evidence with a number | 60% average error reduction |
| 9 | Extra advantages | merged MLPs → ~7% faster, half the parameters |

## Sentences worth studying

> While this approach works well when all training and testing images observe scene content from a roughly constant distance (as done in NeRF and most follow-ups), NeRF renderings exhibit significant artifacts in less contrived scenarios.
> — Mip-NeRF · ICCV 2021 · p.1

> A straightforward solution is to adopt the strategy used in offline raytracing: supersampling each pixel by marching multiple rays through its footprint. But this is prohibitively expensive for neural volumetric representations such as NeRF, which require hundreds of MLP evaluations to render a single ray and several hours to reconstruct a single scene.
> — Mip-NeRF · ICCV 2021 · p.1

> In this paper, we take inspiration from the mipmapping approach used to prevent aliasing in computer graphics rendering pipelines.
> — Mip-NeRF · ICCV 2021 · p.1

> This strategy is known as pre-filtering, since the computational burden of anti-aliasing is shifted from render time (as in the brute force supersampling solution) to a precomputation phase— the mipmap need only be created once for a given texture, regardless of how many times that texture is rendered.
> — Mip-NeRF · ICCV 2021 · p.2

## Why it works
1. **“Works well when … but in less contrived scenarios …”** frames the baseline’s success as dependent on an artificial setting — fair credit plus a sharp limit.
2. **The obvious fix is raised and dismissed with numbers** (hundreds of MLP evaluations, hours per scene). This pre-empts the reviewer question “why not just supersample?”. Note: this is *ruling out* a naive solution, not building on it.
3. **Borrowing a well-known principle** (mipmapping) makes the idea feel inevitable and easy to understand.
4. **Advantages are quantified** (60%, ~7%, half the parameters).

## Transferable skeleton
```text
[Method] has emerged as [credit]. However, [its model] is flawed in a manner that causes [failure].
[Mechanism sentence]. While this works well when [contrived condition] (as in [Method] and most follow-ups),
it exhibits [failure] in less contrived scenarios, e.g., when [realistic condition].
A straightforward solution is to [obvious fix]. But this is prohibitively expensive for [setting],
which requires [quantified cost].
We take inspiration from [principle] used in [other field], which [why it avoids the cost].
Our solution, [Name], [extends Method to …]. On [benchmark], [Name] reduces [metric] by [X%];
it is also [secondary advantage with number].
```
