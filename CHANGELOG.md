# Changelog

## Unreleased

ACL 2021–2026 award corpus (recent 6 years) + Paper Memory Bank for topic-selection and writing-style imitation.

- **ACL 2021–2026 corpus supplement (+40 award papers → 100 papers total)**: added 40 Best Papers, Outstanding Papers, and Best Theme/Resource/Social-Impact/Reproduction Papers from ACL 2021–2026 (`data/papers.csv`, `PAPER_LIST.md`, `references/corpus/corpus_stats.json` `style_by_venue.ACL`, `references/corpus-profile.md`), 4 full ACL exemplar cards (`volt.md`, `impossible-lms.md`, `native-sparse-attention.md`, `cure.md`), plus ACL sentence moves, paragraph exemplars, and aligned phrasebank entries.
- **Paper Memory Bank (`references/memory/section_memory.jsonl`, `scripts/paper_memory.py`, `references/paper-memory.md`)**: SQLite FTS5 + BM25 searchable database of 306 curated award-paper subsection excerpts across 82 papers (`exp.datasets`, `exp.baselines`, `exp.metrics`, `exp.implementation`, `exp.main_results`, `exp.ablation`, `exp.analysis`, `method.*`, `related_work`, `limitations`, etc.) annotated with what award authors **include**, what they **omit or defer to Appendix**, **reader focus**, and **syntactic/lexical style signatures**. Supports personal favorites (`paper_memory.py add`, stored in gitignored `user_memory.jsonl` and preserved by `install.sh`).
- **Anti-laundry-list workflow & audit**: Step 5/5b queries `paper_memory.py` before drafting each subsection (plus Mode C for direct natural-language memory queries/audits); `paper_memory.py audit` and `check_draft.py` flag procedural walkthroughs, paper-by-paper roll-calls, dataset split / hyperparameter / plumbing dumps, per-row table narration, and section-roadmap filler.
- **Venue & sibling-conference matching + Gemini support**: `--venue` (with automatic sibling-conference fallback, e.g., `EMNLP/NAACL → ACL`, `ECCV → CVPR/ICCV`, `ICLR/ICML → NeurIPS`, plus `--related`) added across `paper_memory.py`, `find_exemplars.py`, `style_metrics.py`, and `check_draft.py`; `install.sh` now supports `gemini` and preserves `user_memory.jsonl`; `assets/intake_form.html` includes ACL/EMNLP/NAACL and Limitations.

## v1.2

Simpler intake form.

- `assets/intake_form.html`: 5 required fields instead of 9; 8 recommended fields (marked ⭐) that the skill asks for once if missing; everything else folded under "补充信息" and "方法与实验", with a note that more detail means fewer `[TODO]`s.
- Dropdowns and checkboxes instead of free text: venue / year / pages, sections to write (Title, Abstract, Introduction, Method, Experiments; the method-and-experiments block hides when neither is ticked), paper type and tension type in plain language (default "let the skill decide"), metric direction ↑/↓, release items.
- Merged or removed fields the skill can infer: Figure 1 plan, stance and trend are no longer asked; pipeline integration, supported inputs and applications are one field; a single paste box for method and experiment material.
- Same JSON keys and schema (`bestpaper-intake/v1`): older JSON files import and convert unchanged. `scripts/intake_to_brief.py` follows the new required/recommended split and reads the new fields (sections, metric direction, pasted material).

## v1.1

Figures.

- New Step 5c and `references/figures.md`: a figure plan built from the evidence map (one claim per figure, placement, material needed, status, caption takeaway); Figure 1 types and how to choose one by route; method overview, qualitative comparison and plot conventions; caption structure; layout and typography for two-column and one-column templates.
- Statistics from the figures of 44 of the 55 corpus papers (`data/figure_stats.json`, `data/figure1_types.csv`, extraction script in `tools/`; no PDFs or captions are stored).
- `assets/figures/`: TikZ palette and styles, placeholder macros with the plan in the caption, teaser, overview and qualitative-grid templates, matplotlib style with fixed method colours.
- `scripts/check_figures.py`: captions (length, takeaway first, dashes), labels and references, raster plots, absolute widths, float counts, remaining placeholders.
- Hard rule: never fabricate figure content; result figures stay placeholders until the authors supply the material.
- `template/CVPR2027/`: the official CVPR 2027 author kit.

## v1.0

First public release.

- Workflow for the abstract, introduction, method and experiments, written for both Claude and Codex.
- Two input modes: the offline intake form (JSON), or a complete abstract that is reverse-engineered, completed by questions and rewritten with a change table.
- Routing by paper type (L1 to L8), claim calibration, style rules and exemplar bank built from a sentence-level annotation of 55 award papers (CVPR, ICCV, NeurIPS, 2021 to 2025).
- Draft checker (`scripts/check_draft.py`) calibrated on the corpus.
- Held-out evaluation on 5 further award papers from 2024; 60 papers in total (see `PAPER_LIST.md`).
