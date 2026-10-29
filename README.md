<div align="center">

# <img src="assets/logo.svg" height="44" align="top" alt="logo"> Best-Paper-Writing-Skill

**生成最佳论文风格的高质量论文底稿：摘要、引言、方法、实验与配图**

🏆 写作规律提炼自 60 篇 CVPR / ICCV / NeurIPS 获奖论文，一个 Skill 同时支持 Claude 与 Codex

![version](https://img.shields.io/badge/version-v1.2-blue) ![papers](https://img.shields.io/badge/papers-60-orange) ![Claude](https://img.shields.io/badge/Claude-Skill-8A63D2) ![Codex](https://img.shields.io/badge/Codex-Skill-10A37F) ![license](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey)

[🌐 项目主页](https://gulucaptain.github.io/Best-Paper-Writing-Skill/) · [中文](README.md) · [English](README_en.md) · [论文清单](PAPER_LIST.md) · [更新日志](CHANGELOG.md)

</div>

---

## ✨ 它能做什么

输入你的研究（填表或直接给摘要），输出一份接近获奖论文写法的稿子：

- 📝 **摘要与引言**：具体肯定前人，点明缺口及其原因，给出关于问题本身的洞察，让少数几个数字撑起主张
- 🧩 **方法与实验**：每个组件按"需要 → 机制 → 性质"展开；消融与主张一一对应
- 🖼️ **配图规划与绘制**（v1.1）：先做图像规划表（每张图承载哪个主张、放哪、需要什么素材），按论证路线选 Figure 1 类型，用统一的配色与样式直接画出示意图和方法总览图；需要实验结果的图留白，规划写进图注。排版与风格规则来自 44 篇获奖论文的配图统计
- 🧭 **按论文类型路由**：八类论文（方法改进、新能力、规模规律、再检验、机理分析、理论、数据集、测量）各有论证路线
- ✅ **自带检查器**：对照语料统计检查草稿，揪出 AI 腔、破折号、堆砌的警句和凭空的数字；`check_figures.py` 检查图注长度、首句、引用、矢量图与占位图
- 📋 **附带作者报告 `report.md`**：核心主张、主张-证据表、待补充清单，以及留给 Limitations 的要点
- 🔒 **不编造**：没给的数字、基线、引用，一律保留为 `[TODO]`

### 为什么不直接让 AI 写？

通用 AI 的稿子彼此相似：先铺背景，用形容词代替机制，并排罗列组件，句尾总带一个"……，making X possible"。获奖论文不是这样写的。

| 写法 | 通用 AI 草稿 | 获奖论文 |
|---|---|---|
| 句尾分词短语（", making …"） | 约 32% 的句子 | 约 8% |
| 开头 | 泛泛的背景（"has attracted increasing attention"） | 具体的场景或前人工作 |
| 缺口 | 一句"现有方法有局限" | 什么条件下失败、为什么失败 |
| 组件 | A 做 …… B 做 …… C 做 ……（并排） | 第二个组件解决第一个留下的问题 |
| 局限 | 常写进摘要 | 留给 Limitations 一节 |

规则来自对语料的逐句标注与统计，每条规则都有上下限，而不是一味向"平均值"靠拢。

---

## 🚀 两种使用方式

**📝 填表 / 📄 贴摘要**　→　🔍 补全缺项　→　🧭 判断类型　→　✍️ 参照范例起草　→　✅ 自检　→　📦 论文稿 + `report.md`

### 📝 方式一：填写表单

用浏览器打开 [`skills/bestpaper-writing/assets/intake_form.html`](skills/bestpaper-writing/assets/intake_form.html)（离线可用，自动保存草稿，可导出和再次导入 JSON）。必填只有 5 项，其余按需补充，**补充得越详细，底稿质量越高**：

| 档位 | 内容 |
|---|---|
| ⚙️ 基本设置 | 会议 / 年份 / 页数（下拉）、需要写哪些部分（勾选） |
| 🔴 必填（5） | 一句话说清这篇工作、任务、现有方法在什么情况下不行、方法组成、头条结果 |
| ⭐ 推荐（8） | 现有最强方法、失败原因、核心观察、最相近工作、具体画面、效率优势、反直觉之处、团队内部的叫法；缺了 skill 会先追问一次 |
| 🟢 补充（折叠） | 额外优势与应用、论文类型、矛盾类型、次要结果、开源内容、局限、其他材料、refs.bib |
| 🔵 方法与实验（折叠） | 一个直接粘贴材料的大框；需要时再逐项填写符号、组件、目标、数据集、指标、对比方法、结果表、消融 |

把导出的 JSON 发给 agent：

> 用 Best-Paper-Writing-Skill，根据这份信息表 JSON 写出论文的 Title、Abstract、Introduction、Methods 和 Experiments。

### 📄 方式二：直接给完整摘要

skill 不会盲目重写。它先把摘要拆回上面的字段，告诉你**哪些已有、哪些模糊、哪些缺失**，一次性追问缺项，再写出完整底稿，并给出摘要的**修改对照表**（原句 → 改后句 → 理由），你可以逐条接受或拒绝。你的数字和术语原样保留；摘要里没有的数字、基线和引用一律留作 [TODO]。

> 用 Best-Paper-Writing-Skill，根据这段摘要写出论文的 Title、Abstract、Introduction、Methods 和 Experiments。

也可以直接用文字描述工作。输出为 Markdown，或直接写进 LaTeX 模板（如 CVPR author kit）。

---

## 📦 安装

```bash
git clone https://github.com/gulucaptain/Best-Paper-Writing-Skill.git
cd Best-Paper-Writing-Skill

./install.sh claude     # Claude Code → ~/.claude/skills/
./install.sh codex      # Codex       → ~/.agents/skills/
./install.sh all        # 两个都装；加 --project 则装到当前项目目录
```

| 平台 | 方式 |
|---|---|
| 🟣 **Claude Code** | `./install.sh claude`，或手动复制 `skills/bestpaper-writing/` 到 `~/.claude/skills/` |
| 🟣 **Claude.ai / Cowork** | 把 `bestpaper-writing` 文件夹打成 zip，在 Skills 页面上传 |
| 🟢 **Codex** | `./install.sh codex`，或手动复制到 `~/.agents/skills/`；用 `$bestpaper-writing` 显式调用 |

两个平台使用同一种 `SKILL.md` 格式。装好后若看不到，重启 agent。辅助脚本需要 Python 3。

---

## 🗂️ 目录结构

```
Best-Paper-Writing-Skill/
├── README.md / README_en.md
├── PAPER_LIST.md              # 60 篇论文清单
├── data/                      # papers.csv · figure_stats.json · figure1_types.csv
├── template/CVPR2027/         # 官方 CVPR 2027 LaTeX 模板
├── tools/                     # 语料配图统计脚本
├── install.sh                 # 一键安装
└── skills/bestpaper-writing/
    ├── SKILL.md               # 入口：工作流与硬性规则
    ├── references/            # 摘要、引言、方法、实验、配图、路由、风格规则、语料统计
    │   └── exemplars/         # 段落与句式范例库
    ├── scripts/               # check_draft.py · check_figures.py · find_exemplars.py · intake_to_brief.py · style_metrics.py
    ├── assets/                # intake_form.html · figures/（TikZ 样式、teaser/总览/对比网格模板、matplotlib 样式）
    ├── evals/                 # 留出测试集与盲评标准
    └── agents/openai.yaml     # Codex 界面配置
```

---

## 📚 语料：60 篇获奖论文

2021 至 2025 年 CVPR、ICCV、NeurIPS 的最佳论文、最佳学生论文与荣誉提名。

| 会议 | 篇数 |
|---|---|
| CVPR | 22 |
| ICCV | 12 |
| NeurIPS | 26 |

类型分布：方法改进 26 · 新能力 7 · 数据集 6 · 测量 5 · 机理分析 5 · 理论 4 · 规模规律 4 · 再检验 3。完整清单见 [PAPER_LIST.md](PAPER_LIST.md)。

> 🔬 **关于留出测试**：风格规则由其中 55 篇拟合。另外 5 篇（均为 2024 年）从范例库中移除，只用来测试，避免规则在自己的测试集上调参。

---

## 📄 版权与许可

- 原创内容（说明、模板、脚本）采用 [CC BY 4.0](LICENSE)。
- `references/exemplars/` 中的论文短句仅作教学评论引用并注明出处，版权归原作者，请勿复制进新论文。
- 本仓库**不含任何论文 PDF 或全文**。如果你是原作者，希望调整或移除相关引用，请提 Issue。

## 🙏 致谢

工作流与模板基于 [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills)（MIT），其写作知识来自[彭思达的学习笔记](https://github.com/pengsida/learning_research)。详见 [`NOTICE.md`](skills/bestpaper-writing/NOTICE.md)。

## 🤝 参与

欢迎通过 Issue 反馈问题、补充语料中缺少的领域（NLP、机器人、系统等），或分享你用它写出的稿子。如果它对你有帮助，欢迎点一个 ⭐ Star。
