# Exemplar Bank

## Files
- `paragraphs.jsonl` — 79 paragraph-level exemplars from 55 award papers, each tagged with its main function (`scene`, `credit`, `gap`, `tension`, `insight`, `method`, `contrast`, `result`, `stance`, …), paper type, motivation type and a note on why it works (`why_good`, Chinese). Verbatim.
- `phrasebank.csv` — 234 function-tagged sentence frames with a verbatim example each, incl. 18 transitions without connectors.
- `cards/*.md` — full introduction breakdowns (failure, cost, capability-gap, insight; the trend card is held out while VGGT is an evaluation case) (move sequence, key sentences, why it works, transferable skeleton).
- `moves.jsonl` — sentence-level exemplars from 60 CVPR/ICCV/NeurIPS award papers (2021–2025). Every quote was checked word-for-word against the source PDF text (citation markers removed, line-break hyphenation repaired).

## Record schema (`moves.jsonl`)
| Field | Meaning |
|---|---|
| `id` | E001… |
| `move` | rhetorical move, e.g. `intro.gap.cost`, `intro.insight`, `abstract.open.direct`, `exp.bounded-claim`, `pattern.colon-expansion` |
| `section` | abstract / introduction / related_work / method / experiments / limitations / conclusion / any |
| `quote` | verbatim sentence(s) |
| `paper`, `venue`, `year`, `page` | source (page = PDF page index) |
| `paper_type` | L1–L8 (see `../routing.md`) |
| `motivation_type` | set for papers with a card: failure / cost / capability-gap / insight / trend |

## Retrieval
```bash
python3 scripts/find_exemplars.py --para contrast --type L1   # paragraphs by function
python3 scripts/find_exemplars.py --phrases transition -n 5   # sentence frames
python3 scripts/find_exemplars.py intro.gap          # all gap moves
python3 scripts/find_exemplars.py intro.insight -n 3  # three examples
python3 scripts/find_exemplars.py abstract.open --type L2
```

## Use
Read exemplars for **structure and calibration**. Do not copy sentences or runs of ≥ 6 words; `check_draft.py` flags such overlap.

## Regenerating
These files are generated from the annotated corpus (see `PAPER_LIST.md` in the repository root; the annotation sources are not included). The held-out evaluation papers are excluded from all of them. Please open an issue rather than editing them by hand.
