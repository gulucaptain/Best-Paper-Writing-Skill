---
tags: [bestpaper-writing, best-paper-2024-heldout]
max_turns: 40
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

我在写一篇顶会论文，请帮我写**摘要和引言**（英文）。

要求：
- 用 CVPR 官方模板：把 官方 CVPR author kit（自行下载，路径记为 `<author-kit>`） 整个复制到你的工作目录，命名为 `paper/`（不要改动原模板）。
- 摘要写进 `paper/sec/0_abstract.tex`，引言写进 `paper/sec/1_intro.tex`；在 `paper/main.tex` 里填上论文标题，删掉模板示例章节（`2_formatting`、`3_finalcopy`）的 `\input`，作者保持匿名。
- 参考文献用我给的 `refs.bib`（复制为 `paper/main.bib`），引用时用里面的 key；需要但 bib 里没有的文献，用 `[TODO: cite ...]` 标出，不要编造文献。
- 本机有 LaTeX 的话，编译出 `paper/main.pdf`。
- 其他想告诉我的内容写在 `report.md`。

下面是我的工作：

**Working name**: MotionPrior (target venue: CVPR)

**Task**: from a single still image, generate realistic, long-term motion of the whole scene — e.g., trees and flowers swaying in the wind, candles flickering, clothes moving — and use it to animate the image.

**Background**: the natural world is always in motion, and imagery without motion (or with slightly wrong motion) looks uncanny. Real motion comes from physical dynamics (forces, mass, elasticity) that are hard to measure at scale; but observed 2D motion is enough for some applications and is often predictable (candles flicker in certain ways, trees sway). Diffusion models [ho2020ddpm, rombach2022ldm] can model rich distributions and have been extended to video. Image-space modal analysis [davis2015modal] can simulate a scene's response to forces from its observed vibrations, but needs a video as input.

**Closest work**: single-image animation methods that predict motion or frames directly — e.g., Holynski et al. [holynski2021animating] for fluid motion with a single static flow field, Endo et al., MCVD, Stochastic Image-to-Video — and large video diffusion models (AnimateDiff, ModelScope, Gen-2) that generate RGB video volumes directly and tend to drift away from the input image over time.

**Key idea**: model a generative prior over *motion*, not pixels. Represent dense, long-range pixel trajectories in the Fourier domain as a *spectral volume* (a few low-frequency coefficients per pixel, well suited to oscillatory motion) and learn to predict spectral volumes with a diffusion model. Motion is lower-dimensional and more structured than raw pixels, which makes long-term generation more coherent and more controllable.

**Method**: a latent diffusion model predicts the spectral volume from one image, generating coefficients one frequency band at a time but coordinating bands through shared attention (frequency-coordinated denoising); the spectral volume is converted to a motion texture (per-pixel trajectories over the whole video); an image-based rendering module (feature splatting) renders future frames, running at 25 FPS. The spectral volume can also be read as an image-space modal basis to simulate how objects respond to user-applied forces (interactive dynamics from a single picture).

**Data**: 3,015 videos of natural oscillatory scenes; over 150K image–motion pairs.

**Results (Table 1, test set; lower is better)**: ours FID 4.03 / FVD 47.1 / DTFVD 2.53 vs. the best prior single-image animation baselines Endo et al. FID 10.4 / FVD 166.0 / DTFVD 5.35 and Holynski et al. FID 11.2 / FVD 179.0; MCVD FID 63.4 / FVD 208.6. User study against large video diffusion models (AnimateDiff, ModelScope, Gen-2) on 30 test videos: 80.9% preference for our animations.

**Applications**: seamlessly looping videos, editing the generated motion, interactive dynamic images.

**Figures**: Fig. 1 — a still photo of a flower/tree turned into an animation, plus a user dragging a branch and the scene responding.

Input files: refs.bib
