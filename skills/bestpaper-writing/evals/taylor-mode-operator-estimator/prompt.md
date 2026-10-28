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

**Working name**: TaylorRand (target venue: NeurIPS; please still use the CVPR template I gave you)

**Task**: train neural networks whose loss contains high-order, high-dimensional differential operators — e.g., physics-informed neural networks (PINNs) [raissi2019pinn] for high-dimensional PDEs.

**Why it is hard**: with back-propagation the derivative tensor grows as O(d^k) and the computation graph as O(2^(k-1) L) (d = input dimension, k = derivative order, L = number of operations in the forward graph).

**Prior work**:
- Randomization amortizes the cost over optimization: stochastic dimension gradient descent (SDGD) [hu2023sdgd] samples input dimensions; the Hutchinson trace estimator [hutchinson1989] estimates Hessian traces. This removes the d-scaling for second order only, still with first-order back-propagation.
- High-order Taylor-mode automatic differentiation [griewank2008evaluating, bettencourt2019taylor] removes the exponential k-scaling, but only for univariate functions (d = 1).
- Finite differences and randomized smoothing avoid AD, but their accuracy depends on the discretization.

**Key insight**: with properly constructed input tangents, univariate Taylor-mode AD can contract the derivative tensor of a multivariate function at any order. Randomizing these tangents gives an unbiased estimate of any differential operator — so one tool removes both the d- and the k-scaling.

**Method**: TaylorRand — a randomized estimator built on Taylor-mode AD; constructions for operators in common PDEs; SDGD and Hutchinson-type estimators are special cases; we prove that Hutchinson-type estimators cannot be generalized beyond fourth-order operators.

**Results**:
- On PINNs: more than 1000× speed-up and more than 30× memory reduction compared with randomization using first-order AD.
- Solves a 1-million-dimensional PDE in 8 minutes on one NVIDIA A100 40GB GPU.
- Ablation identifies the source of the gain.

**Release**: code public.

Input files: refs.bib
