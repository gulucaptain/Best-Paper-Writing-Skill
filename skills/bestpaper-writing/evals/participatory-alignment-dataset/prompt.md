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

**Working name**: GlobalPref (target venue: NeurIPS Datasets & Benchmarks; please still use the CVPR template I gave you)

**Context**: human feedback is central to aligning large language models (RLHF [ouyang2022training], constitutional AI [bai2022constitutional]). Open questions remain about **how** feedback is collected (binary A/B vs. fine-grained ratings), **where** (which domains/topics), **who** gives it (participants' preferences, values, beliefs), and **to what end** (personalised alignment vs. aggregating preferences for society). Existing preference datasets [bai2022training, stiennon2020learning] over-rely on binary A/B comparisons, recruit small or biased samples from narrow crowdwork or tech communities, provide little information about raters, and rarely document how values are operationalised. Treating feedback as coming from a "generic human" teaches behaviours that are reductionist and do not generalise.

**What we built**: a dataset mapping 1,500 diverse participants from 75 countries (birth) — their sociodemographics and stated preferences — to their contextual preferences and fine-grained feedback in 8,011 live conversations with 21 LLMs (27,172 interactions, 68,371 rated utterances).
- **Participatory**: wider geographic and demographic participation;
- **Representative**: census-representative samples for the UK and the US;
- **Individualised**: every rating links to a pseudonymous participant profile, enabling personalisation and attribution.
- Two stages: a survey (background, LLM familiarity, stated preferences), then multi-turn conversations on topics of the participant's choosing, rating responses on a cardinal scale with fine-grained feedback. Conversations are primed as values-guided, controversy-guided, or unguided (baseline).
- We target subjective and multicultural perspectives on value-laden and controversial issues, where we expect interpersonal and cross-cultural disagreement; to our knowledge the first human-feedback dataset with this focus.

**Case studies** (show what the dataset enables): (1) do different people start different discussions with LLMs? (2) do people prefer differently aligned models? (3) how do sampling decisions (whose feedback is collected) affect welfare outcomes? They show the need to consider carefully which humans provide what alignment data.

**Release**: data, dataset card and code public.

**Figures**: Fig. 1 — the two-stage design and the dataset statistics (participants, countries, conversations, models).

Input files: refs.bib
