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

**Working name**: ScaleAR (target venue: NeurIPS; please still use the CVPR template I gave you)

**Context**: GPT-style autoregressive (AR) language models [radford2019gpt2, brown2020gpt3] scale predictably (scaling laws [kaplan2020scaling]) and generalize zero-shot. Vision has tried to reproduce this with image AR models such as VQGAN [esser2021vqgan] and DALL-E [ramesh2021dalle]: a tokenizer turns an image into a 2D grid of tokens, which is flattened in raster order and predicted token by token. But these models lag far behind diffusion models such as DiT [peebles2023dit], and their scaling behaviour is under-explored — the power of AR in vision seems "locked".

**Key idea**: the problem is the *order*. Images are perceived and created hierarchically — global structure first, details later. So define autoregressive learning on images as predicting the next, higher-resolution token map (coarse to fine) instead of the next token in raster order. Each step predicts a whole token map in parallel, conditioned on all coarser maps.

**Method**: a multi-scale VQ-VAE encodes an image into token maps of increasing resolution starting from 1×1; a standard GPT-2-like transformer predicts each next-scale map conditioned on the previous ones.

**Results** (ImageNet 256×256):
- Improves the AR baseline from FID 18.65 to 1.73 and Inception Score from 80.4 to 350.2, with 20× faster inference.
- For the first time, a GPT-style AR model surpasses diffusion transformers: our 2B model reaches FID 1.73, better than L-DiT with 3B and 7B parameters; better than DiT in image quality, inference speed, data efficiency and scalability.
- Clear power-law scaling laws, like LLMs, with linear correlation coefficients near −0.998.
- Zero-shot generalization to in-painting, out-painting and editing.

**Figures**: Fig. 1 — generated samples; Fig. 2 — (a) language AR, (b) raster-scan image AR, (c) our next-scale prediction; Fig. 3 — FID vs model size for AR, diffusion and our model families.

**Release**: all models and code public.

Input files: refs.bib
