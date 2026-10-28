# Changelog

## v1.0

First public release.

- Workflow for the abstract, introduction, method and experiments, written for both Claude and Codex.
- Two input modes: the offline intake form (JSON), or a complete abstract that is reverse-engineered, completed by questions and rewritten with a change table.
- Routing by paper type (L1 to L8), claim calibration, style rules and exemplar bank built from a sentence-level annotation of 55 award papers (CVPR, ICCV, NeurIPS, 2021 to 2025).
- Draft checker (`scripts/check_draft.py`) calibrated on the corpus.
- Held-out evaluation on 5 further award papers from 2024; 60 papers in total (see `PAPER_LIST.md`).
