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

**Working name**: WeakGuide (target venue: NeurIPS; please still use the CVPR template I gave you)

**Context**: image diffusion models [ho2020ddpm, karras2022edm] are judged on image quality, variation, and alignment with a condition (class label or prompt). Because training covers the whole data distribution, models are penalized for not representing low-probability regions but lack data to generate them well. Classifier-free guidance (CFG) [ho2022cfg] is the standard way to "lower the temperature": it uses an unconditional model to steer a conditional one, improving prompt alignment and image quality at the cost of less variation. But: (1) it only works for conditional generation; (2) because the conditional and unconditional denoisers solve different tasks, the sampling trajectory can overshoot, giving skewed, overly simple compositions; (3) prompt alignment and quality improvements cannot be controlled separately, and it is unclear how they relate. Guidance interval [kynkaanniemi2024interval] is a concurrent improvement to CFG.

**Our observation (surprising)**: quality can be improved *without* losing variation by guiding with a smaller, less-trained version of the model itself instead of an unconditional model. Our analysis of why CFG improves quality: when the guiding model is a degraded version of the main model, it makes the same kinds of errors but stronger, so guiding away from it pushes samples away from those errors.

**Method**: autoguidance-style guidance — the guiding model is the same network with unchanged conditioning but reduced capacity and/or training time; no task discrepancy; works for unconditional models too.

**Results** (ImageNet, publicly available EDM2 [karras2024edm2] networks):
- ImageNet-512: small model FID 2.56 → 1.34 (vs. 1.68 for CFG + guidance interval); largest model reaches record FID 1.25. FD_DINOv2 records also improved.
- ImageNet-64: record FID 1.01.
- Unconditional ImageNet-512: FID 11.67 → 3.86.
- Synthetic 2D experiments illustrate the mechanism; also works for text-conditional generation.

**Release**: code and models public.

Input files: refs.bib
