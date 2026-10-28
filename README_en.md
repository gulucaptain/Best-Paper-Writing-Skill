<div align="center">

# <img src="assets/logo.svg" height="44" align="top" alt="logo"> Best-Paper-Writing-Skill

**Generate high-quality paper drafts: abstract, introduction, method, experiments and figures, written and drawn the way best papers are**

🏆 Writing patterns distilled from 60 CVPR / ICCV / NeurIPS award papers, packaged as a skill for both Claude and Codex

![version](https://img.shields.io/badge/version-v1.1-blue) ![papers](https://img.shields.io/badge/papers-60-orange) ![Claude](https://img.shields.io/badge/Claude-Skill-8A63D2) ![Codex](https://img.shields.io/badge/Codex-Skill-10A37F) ![license](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey)

[中文](README.md) · [English](README_en.md) · [Paper list](PAPER_LIST.md) · [Changelog](CHANGELOG.md)

</div>

---

## ✨ What it does

Give it your research (an intake form or a complete abstract) and get a draft that argues like an award paper:

- 📝 **Abstract and introduction**: credit specific prior work, name a concrete gap and its reason, state one insight about the problem, let a few numbers carry the claim
- 🧩 **Method and experiments**: each component told as need, mechanism, property; ablations that mirror the claims
- 🖼️ **Figure planning and drawing** (v1.1): a figure plan (the claim each figure carries, where it goes, the material it needs), Figure 1 chosen by line of argument, schematics and method overviews drawn in one consistent style; figures that need results stay as placeholders with their plan in the caption. Layout and style rules come from the figures of 44 award papers
- 🧭 **Routing by paper type**: eight types (method improvement, new capability, empirical law, re-examination, mechanism, theory, dataset, measurement), each with its own line of argument
- ✅ **Built-in checkers**: compares a draft with corpus statistics and flags AI habits, dashes, piled-up aphorisms and invented numbers; `check_figures.py` checks caption length and first sentence, references, vector plots and remaining placeholders
- 📋 **Author report `report.md`**: claim, claim-evidence map, TODO list, and notes for the Limitations section
- 🔒 **No fabrication**: missing numbers, baselines and references stay as `[TODO]`

### Why not just ask an AI to write it?

Generic AI drafts look alike: background first, adjectives instead of mechanisms, a list of parallel components, and a trailing ", making X possible" on every other sentence. Award papers do not read that way.

| Habit | Typical AI draft | Award papers |
|---|---|---|
| Sentences ending in a participial clause (", making ...") | about 32% | about 8% |
| Opening | generic background ("has attracted increasing attention") | a concrete scene or specific prior work |
| Gap | "existing methods have limitations" | under what condition they fail, and why |
| Components | A does ... B does ... C does ... | the second fixes what the first leaves open |
| Limitations | often in the abstract | in the Limitations section |

The rules come from a sentence-level annotation of the corpus. Every rule has both a floor and a ceiling, so drafts are not pushed to the statistical average.

---

## 🚀 Two ways to use it

**📝 Fill the form / 📄 Paste an abstract**　→　🔍 Fill the gaps　→　🧭 Pick the type　→　✍️ Draft with exemplars　→　✅ Self-check　→　📦 Draft + `report.md`

### 📝 Mode A: fill in the form

Open [`skills/bestpaper-writing/assets/intake_form.html`](skills/bestpaper-writing/assets/intake_form.html) in a browser (offline, autosaves, exports and re-imports JSON; the interface is in Chinese). Four tiers:

| Tier | Content |
|---|---|
| 🔴 Required | task, strongest prior approach, failure and its reason, key insight, method components, headline results, closest work |
| 🟡 Memorability | efficiency, integration with existing pipelines, a concrete example, what is surprising, stance, the team's name for the idea |
| 🟢 Support | Figure 1, data scale, limitations, refs.bib |
| 🔵 Method and experiments | notation, components, objective, datasets, metrics, baselines, result tables, ablations |

Send the exported JSON to your agent:

> Use bestpaper-writing to write the abstract and introduction from this intake JSON.

### 📄 Mode B: paste a complete abstract

The skill does not rewrite blindly. It first breaks the abstract into the same fields and shows which are **present, vague or missing**, asks for the gaps once, then rewrites and returns a **change table** (original sentence, revised sentence, reason) so you can accept or reject each change. Your numbers and terminology are kept.

> Use bestpaper-writing to rewrite this abstract so it reads like a best paper: ...

You can also describe the work in plain text. Output is Markdown, or written directly into a LaTeX template such as the CVPR author kit.

---

## 📦 Install

```bash
git clone https://github.com/gulucaptain/Best-Paper-Writing-Skill.git
cd Best-Paper-Writing-Skill

./install.sh claude     # Claude Code -> ~/.claude/skills/
./install.sh codex      # Codex       -> ~/.agents/skills/
./install.sh all        # both; add --project to install into the current repo
```

| Platform | How |
|---|---|
| 🟣 **Claude Code** | `./install.sh claude`, or copy `skills/bestpaper-writing/` to `~/.claude/skills/` |
| 🟣 **Claude.ai / Cowork** | zip the `bestpaper-writing` folder and upload it on the Skills page |
| 🟢 **Codex** | `./install.sh codex`, or copy to `~/.agents/skills/`; invoke explicitly with `$bestpaper-writing` |

Both platforms use the same `SKILL.md` format. Restart the agent if the skill does not appear. Python 3 is needed for the helper scripts.

---

## 🗂️ Layout

```
Best-Paper-Writing-Skill/
├── README.md / README_en.md
├── PAPER_LIST.md              # the 60 analysed papers
├── data/                      # papers.csv · figure_stats.json · figure1_types.csv
├── template/CVPR2027/         # official CVPR 2027 LaTeX kit
├── tools/                     # corpus figure statistics
├── install.sh                 # one-step install
└── skills/bestpaper-writing/
    ├── SKILL.md               # entry point: workflow and hard rules
    ├── references/            # abstract, introduction, method, experiments, figures, routing, style rules, corpus statistics
    │   └── exemplars/         # paragraph and sentence exemplars
    ├── scripts/               # check_draft.py · check_figures.py · find_exemplars.py · intake_to_brief.py · style_metrics.py
    ├── assets/                # intake_form.html · figures/ (TikZ styles, teaser/overview/grid templates, matplotlib style)
    ├── evals/                 # held-out test cases and blind-comparison rubric
    └── agents/openai.yaml     # Codex UI metadata
```

---

## 📚 The corpus: 60 award papers

Best papers, best student papers and honorable mentions of CVPR, ICCV and NeurIPS, 2021 to 2025.

| Venue | Papers |
|---|---|
| CVPR | 22 |
| ICCV | 12 |
| NeurIPS | 26 |

By type: method improvement 26 · new capability 7 · dataset 6 · measurement 5 · mechanism 5 · theory 4 · empirical law 4 · re-examination 3. Full list in [PAPER_LIST.md](PAPER_LIST.md).

> 🔬 **Held-out test**: the style rules were fitted on 55 of them. The other 5 (all from 2024) were removed from the exemplar bank and used only for testing, so the rules are not tuned on their own test set.

---

## 📄 Copyright and licence

- Original content (instructions, templates, scripts) is [CC BY 4.0](LICENSE).
- Short excerpts of published papers in `references/exemplars/` are quoted with attribution for commentary and education. Their copyright stays with the authors; do not copy them into new papers.
- This repository contains **no paper PDFs or full texts**. If you are an author and want your excerpts changed or removed, please open an issue.

## 🙏 Acknowledgements

The workflow and templates build on [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) (MIT), whose writing knowledge comes from [Peng Sida's study notes](https://github.com/pengsida/learning_research). See [`NOTICE.md`](skills/bestpaper-writing/NOTICE.md).

## 🤝 Contributing

Issues are welcome: bug reports, corpus for areas not yet covered (NLP, robotics, systems), or drafts you wrote with it. If it helps you, a ⭐ Star is appreciated.
