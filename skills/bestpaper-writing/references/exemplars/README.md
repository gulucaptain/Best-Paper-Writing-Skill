# Exemplar Bank

## Files
- `paragraphs.jsonl` — 185 paragraph-level exemplars sampled from **82 distinct award papers** (across the 95-paper CVPR/ICCV/NeurIPS 2021–2025 + ACL 2021–2026 corpus), each tagged with its main function (`scene`, `credit`, `gap`, `tension`, `insight`, `method`, `contrast`, `result`, `stance`, `exp_datasets`, `exp_results`, `method_component`, `limitations`, …), paper type, motivation type, venue, and a note on why it works (`why_good`, Chinese). Verbatim.
- `phrasebank.csv` — function-tagged sentence frames with a verbatim example each, incl. transitions without connectors and concise ACL experiment/dataset framing idioms.
- `cards/*.md` — full introduction breakdowns covering CVPR/ICCV/NeurIPS (`dpo.md`, `dreambooth.md`, `mip-nerf.md`, `mip-splatting.md`, `vggt.md`) and ACL 2021–2026 (`volt.md`, `impossible-lms.md`, `native-sparse-attention.md`, `cure.md`).
- `moves.jsonl` — 308 sentence-level exemplars from **85 distinct award papers** (CVPR/ICCV/NeurIPS 2021–2025 and ACL 2021–2026). Every quote was checked against the source PDF text (line-break hyphenation repaired).
- See also `../memory/` (`section_memory.jsonl` — 306 subsection excerpts across **82 distinct award papers**, indexed in `paper_memory.db` via `scripts/paper_memory.py`) for the full-paper **Paper Memory Bank** with topic-selection (`included` / `omitted_or_deferred`) and style-signature annotations.

## Record schema (`moves.jsonl`)
| Field | Meaning |
|---|---|
| `id` | E001… |
| `move` | rhetorical move, e.g. `intro.gap.cost`, `intro.insight`, `abstract.open.direct`, `exp.datasets.concise`, `exp.bounded-claim`, `pattern.colon-expansion` |
| `section` | abstract / introduction / related_work / method / experiments / limitations / conclusion / any |
| `quote` | verbatim sentence(s) |
| `paper`, `venue`, `year`, `page` | source (page = PDF page index) |
| `paper_type` | L1–L8 (see `../routing.md`) |
| `motivation_type` | failure / cost / capability-gap / insight / trend / mechanism / re-examination / resource / theory |

## Retrieval
```bash
python3 scripts/find_exemplars.py --para contrast --type L1 --venue ACL   # ACL paragraphs by function
python3 scripts/find_exemplars.py --phrases transition -n 5               # sentence frames
python3 scripts/find_exemplars.py intro.gap --venue ACL                   # ACL gap moves
python3 scripts/find_exemplars.py exp.datasets --venue ACL                # concise ACL dataset moves
python3 scripts/paper_memory.py query --subsection exp.datasets --venue ACL -k 3  # full subsection memory
```

## Use
Read exemplars for **topic selection, structure, syntax, and lexical calibration**. Do not copy sentences or runs of ≥ 6 words; `check_draft.py` flags such overlap.

## Regenerating
These files are generated from the annotated corpus (see `PAPER_LIST.md` in the repository root; the annotation sources are not included). The held-out evaluation papers are excluded from all of them. Please open an issue rather than editing them by hand.
