# Method section

Derived from the section structure of 55 award papers (42 with a cleanly parsed method and experiments section) and a close reading of the method sections of 14 of them (DreamBooth, pixelSplat, Mip-Splatting, VGGT, Mip-NeRF, Swin, OmniMotion, DPO, IPG, NWM, DynIBaR, Imagen, MegaSaM, EPro-PnP). Quotes are verbatim and shown for structure only.

Every method is different, but award method sections do the same five things.

## 1. Shape (what the corpus shows)
| Observation | Value |
|---|---|
| Length | median ~1,700 words, about as long as the experiments (~1,500) |
| Preliminaries / background section before the method | 12 / 42 papers (when the method modifies a known model: 3DGS, NeRF, RLHF, diffusion) |
| Method section title | named after the method or idea in 23 / 42 (“Mip Gaussian Splatting”, “Image-conditioned 3D Gaussian Inference”); generic “Method/Approach” in 12 / 42 |
| Number of method sections | usually one, with 2–4 subsections; some split representation and optimization (OmniMotion) or formulation and algorithm |
| Implementation details | in the experiments setup (13 / 42) or the appendix; almost never inside the method (2 / 42) |
| Analysis section between method and experiments | when the method has a theoretical reading (DPO “Theoretical Analysis”, Mip-Splatting “Sensitivity to Sampling Rate” before the method) |

## 2. The five moves
**M1 · Opener: task, input, output, parts.** One paragraph that restates the goal in operational terms and names the two or three components, pointing to the overview figure.
> “Given a pair of images and their associated camera parameters, our method infers a 3D Gaussian representation of the underlying scene, which can be rendered to produce images of unseen viewpoints. Our method consists of a two-view image encoder and a pixel-aligned Gaussian prediction module.” (pixelSplat)

**M2 · Preliminaries and notation (only what the method changes).** Review the model you modify, define every symbol once, and stop. Announce why it is needed.
> “In this section, we first review the sampling theorem in Section 3.1, laying the foundation for understanding the aliasing problem.” (Mip-Splatting)
> “The input is a sequence (I_i) of N RGB images …, observing the same 3D scene.” (VGGT)

**M3 · One subsection per component: need → mechanism → property.** Open each subsection with the problem it solves (often pointing back to the introduction), then the mechanism with its equation, then why it works or what property it guarantees. A component that fixes a side effect of the previous one is introduced through that side effect.
> “As discussed in Sec. 1, classical motion representations, such as pairwise optical flow, lose track of objects when they are occluded … To obtain accurate, consistent tracks even through occlusion, we therefore need a global motion representation …” (OmniMotion)
> “Our first task is to implant the subject instance into the output domain of the model … One natural idea is to fine-tune the model using the few-shot dataset of the subject.” then “… which gives rise to the problem of language drift.” (DreamBooth, the second component answers the first one’s side effect)
> “To overcome these challenges, we make two modifications to the original 3DGS model.” (Mip-Splatting)

**M4 · Objective and optimization.** The loss (with each term motivated), what is optimized and what is fixed, inference procedure. Keep hyperparameter values for the experiments or appendix.
> “Our optimization process takes as input a video sequence and a collection of noisy correspondence predictions … as guidance, and generates a complete, globally consistent motion estimate for the entire video.” (OmniMotion)

**M5 · Contrast and interpretation (where it adds insight).** A sentence or short subsection that relates the design to prior mechanisms or explains it theoretically, at the level of mechanism, not of results.
> “Unlike prior RLHF methods, which learn a reward and then optimize it via RL, our approach bypasses the reward modeling step …” (DPO)
> “Aside from cone-tracing and IPE features, mip-NeRF behaves similarly to NeRF …” (Mip-NeRF, stating what does not change)

## 3. Rules
1. **Every method subsection answers a claim from the introduction**, and every claim made in the introduction is realised by a subsection (extend the claim map: claim → method subsection → experiment → ablation).
2. **Need before mechanism.** The first sentence of a subsection says what problem it solves; the equation comes after.
3. **Define each symbol once**, at first use, and keep notation fixed; prefer one notation table in the preliminaries for heavy notation.
4. **Equations carry the mechanism, prose carries the reason.** After each key equation, one sentence on what it means or why it works (“Intuitively, …”, “This term encourages …”).
5. **Say what stays the same** as the base method; reviewers need to see the delta.
6. **Rule out the obvious alternative** with a reason when one exists (“One natural idea is … However …”).
7. **Implementation details** (layer counts, learning rates, iterations, hardware) go to the experiments setup or the appendix, unless they are the contribution.
8. **No results in the method**, apart from a pointer (“we verify this in Sec. 5.3”).
9. **Mechanisms the author has not given are `[TODO]`**, never filled with plausible-sounding inventions. Ask for equations, losses and algorithm steps.
10. Style: present tense, “we” for decisions, the method name as subject for what it does. No dashes (author preference); colons are fine before an enumeration or equation.

## 4. Skeleton
```text
\section{<Method name or idea>}            % M1: goal, input → output, components, Fig. 2
\subsection{Preliminaries}                 % M2: base model + notation (if modifying one)
\subsection{<Component 1>}                 % M3: need → mechanism (Eq.) → property
\subsection{<Component 2>}                 % M3: often answers a side effect of component 1
\subsection{Training and inference}        % M4: objective, optimization, inference
\subsection{Discussion} (optional)         % M5: relation to prior mechanisms / theory
```

## 5. Checklist
- [ ] The opener states input, output and the components, and points to the overview figure (drawn as in `figures.md` §4).
- [ ] Each subsection opens with the problem it solves; each key equation is followed by its meaning.
- [ ] Every symbol is defined once; notation matches the figures.
- [ ] The delta to the base method is explicit; the obvious alternative is ruled out where relevant.
- [ ] Every introduction claim maps to a subsection and to an experiment.
- [ ] No hyperparameters or results; no invented mechanisms (`[TODO]` instead); no dashes.
