# Paper Memory Bank: Topic Selection & Style Imitation

Grounded in full-paper subsection excerpts from **ACL (2021–2026), CVPR, ICCV, and NeurIPS** award papers (`references/memory/section_memory.jsonl`, indexed in `references/memory/paper_memory.db` via SQLite FTS5), plus any favorite papers the author adds (`user_memory.jsonl`).

## 1. Why AI drafts over-detail and miss the reader's focus

Generic AI drafts treat every subsection like a technical manual: they enumerate every number in the input instead of asking **what a human reviewer actually wants to learn from this subsection**.

Compare how an AI draft vs. an award paper writes `Datasets` for standard public benchmarks:

- **Typical AI draft (over-detailed, flat focus)**:
  > We evaluate our method on GSM8K, MATH, and HumanEval. GSM8K consists of 7,473 training problems and 1,319 test problems of grade-school math word problems. MATH contains 7,500 training problems and 5,000 test problems spanning seven competition subjects with five difficulty levels. HumanEval has 164 handwritten Python programming problems with an average of 7.7 unit tests per problem. We follow the official train/test splits for all datasets.
  *(75 words spent reciting public trivia that every NLP/ML reviewer already knows — and zero explanation of why these benchmarks test the paper's specific claim.)*

- **Award-paper framing (concise, claim-aligned, citation-offloaded)**:
  > We evaluate across two reasoning domains where iterative self-correction matters most: mathematical reasoning on GSM8K and MATH (Cobbe et al., 2021; Hendrycks et al., 2021), and executable code generation on HumanEval (Chen et al., 2021). Full dataset statistics and prompt templates are detailed in Appendix A.
  *(49 words: groups benchmarks by capability axis, explains why they stress-test the thesis, offloads standard specs via citations + Appendix.)*

**The rule of thumb**:
- **Standard public benchmarks**: state *why* each group of benchmarks tests your claim, group them by axis, cite them, and defer split sizes / preprocessing to Appendix or a compact table.
- **Newly created or modified datasets (e.g., L7 resource papers or custom splits)**: state only the defining scale, construction principle, and checkable difference from existing resources; defer schemas/annotation instructions to Appendix.

### Six Common Laundry-List Patterns

Over-detailing often appears as play-by-play narration across sections:

| Pattern | Typical AI draft | Award-paper style |
|---|---|---|
| **1. Procedural walkthrough** (Method / Setup) | "First, we tokenize... Next, we pass it through a linear layer... Then, we apply LayerNorm... Finally, we compute loss." | **Need → Mechanism → Property**: open with the problem solved, present the core formulation, and state what property it yields; skip standard layer plumbing. |
| **2. Dataset & hyperparameter dump** (`exp.datasets`, `exp.implementation`) | Reciting train/val/test split counts, lowercasing/UTF-8 steps, and 6+ optimizer/GPU knobs inline | Group public benchmarks by capability axis and cite them; keep only the method-defining delta and compute scale; move splits, hyperparameters, and prompts to Appendix. |
| **3. Paper-by-paper roll-call** (`related_work`, `exp.baselines`) | "Smith et al. (2021) propose A. Jones et al. (2022) introduce B. Lee et al. (2023) extend C..." | Cluster works into 2–3 paradigms by shared assumption or bottleneck, cite compactly, and end each cluster with a contrast against your method. |
| **4. Cell-by-cell table / ablation narration** (`exp.main_results`, `exp.ablation`) | "On Dataset A, M1 gets 71.2, M2 gets 73.5, ours gets 76.1. On Dataset B, ... When removing X, score drops 1.2. When removing Y, ..." | **Claim → Table pointer → 1–2 diagnostic margins → Mechanism-based why**. Synthesize cross-benchmark patterns instead of walking through rows one by one. |
| **5. Parallel component inventory** (Intro / `method.overview`) | "Our system has four modules: A, B, C, D. Module A does... Module B does... Module C does..." | Chain components by relation: "A solves X; because A alone leaves Y open, B enforces Z." |
| **6. Roadmap & chronological filler** (Intro / Conclusion / Limitations) | "The rest of this paper is organized as follows: Section 2... Section 3..." / "In 2018... In 2020... In 2022..." | Cut section roadmaps; organize background by conceptual trade-off; close with takeaways and concrete limitations. |

## 2. Study-Before-Write Workflow

Before drafting a section or subsection (especially `exp.datasets`, `exp.baselines`, `exp.implementation`, `exp.main_results`, `exp.ablation`, `method.overview`, `method.component`, `related_work`, `limitations`), query the Paper Memory Bank:

```bash
# 1. Retrieve 3 award-paper examples with topic-selection and style notes
python3 scripts/paper_memory.py query --subsection exp.datasets --venue ACL --topic "<your task>" -k 3

# 2. Venue & sibling-conference matching:
#    - Exact venue: ACL, CVPR, ICCV, NeurIPS (or any custom venue you added)
#    - Sibling fallback: EMNLP/NAACL/EACL/COLING/TACL/COLM -> ACL; ECCV/WACV -> CVPR+ICCV; ICLR/ICML/AAAI -> NeurIPS
#    - Domain aliases or comma lists: --venue NLP | --venue CV | --venue ML | --venue CVPR,ICCV | --venue CVPR --related
python3 scripts/paper_memory.py query --subsection exp.datasets --venue EMNLP -k 3
python3 scripts/paper_memory.py query --subsection intro.opening --venue ECCV -k 3

# 3. Synthesized style sheet or subsection list
python3 scripts/paper_memory.py style-sheet --subsection exp.datasets --venue ACL
python3 scripts/paper_memory.py list --venue CV
```

Read the returned **Imitation Study Brief** across four aspects:

1. **Topic selection (`Included`)**: Which 2–4 questions do award papers answer in this subsection? Match those decision points rather than listing all available notes.
2. **Deliberate omission (`Omitted/Defer`)**: Which routine details (train/val/test counts, standard AdamW/lr/warmup settings, full prompt strings, secondary metrics) do award papers offload via citations or Appendix pointers?
3. **Excerpt rhythm**: Note sentence length and information density across the curated excerpts.
4. **Syntax & vocabulary**: Absorb reusable structures (taxonomic grouping, mechanism-first clauses, citation-as-compression, claim-first openings) and high-signal verbs/collocations. Do not reuse verbatim sentences or runs of ≥ 6 consecutive words (`check_draft.py` flags overlap against `section_memory.jsonl`).

## 3. Subsection Focus Map

| Subsection (`--subsection`) | Keep in Main Text (Reader Focus) | Defer to Citation / Table / Appendix |
|---|---|---|
| `exp.datasets` | Grouping by capability axis; why these tasks test the claim; non-standard subsets or new data | Raw train/dev/test counts of public benchmarks; tokenization/filtering scripts; full prompt text |
| `exp.baselines` | Grouped by paradigm (e.g., training-free vs. fine-tuned); why each is a strong competitor; one sentence on fair comparison | Exhaustive baseline architectures or summaries already in Related Work |
| `exp.metrics` | Metric name, direction ($\uparrow$/$\downarrow$), and why it captures the claimed property (especially for custom metrics) | Standard formulas (BLEU, F1, exact match) unless modified |
| `exp.implementation` | Base model/codebase, key architectural/training deltas from prior work, compute scale | Full hyperparameter lists (lr, warmup, Adam $\beta$, dropout, seeds, batch schedule) → Appendix table |
| `exp.main_results` | Claim-first takeaway → table pointer → key margin → mechanism-based why | Cell-by-cell narration of every row/column in the table |
| `exp.ablation` | One research question per design component; what breaks when removed and why | Secondary sensitivity sweeps → Appendix |
| `method.overview` | Operational input → output, 2–3 named components, pointer to overview figure | Low-level tensor shapes, layer counts, activation functions |
| `method.component` | Need (problem solved) → core mechanism (equation) → resulting property/guarantee | Algebra derivations, edge-case engineering tricks → Appendix |
| `related_work` | 2–3 thematic clusters organized by dimension of difference from our work | Chronological paper-by-paper summaries ("X proposed A. Y proposed B.") |
| `limitations` | 2–4 concrete failure modes/assumptions with clear scope (required for ACL) | Generic boilerplate ("we leave scaling to future work") |

## 4. Auditing a Draft for Laundry Lists & Setup Detail Dumps

After drafting body sections (Method, Related Work, Experiments, Limitations), run:

```bash
python3 scripts/paper_memory.py audit paper/sec/4_experiments.tex --subsection auto --venue ACL
```

It checks for:
- **procedural step-by-step walkthroughs** (`First, ... Next, ... Then, ... Finally, ...` / `We first ... We then ...`);
- **paper-by-paper roll-calls** in Related Work / Baselines (`Author et al. proposes ... Author B introduces ...` / `In 2020 ... In 2021 ...`);
- **dataset split dumps**, **hyperparameter prose dumps**, **engineering/preprocessing plumbing dumps**, and lengthy setup subsections (> 320 words);
- **cell-by-cell table / ablation narration** (`Table 1 shows...`, `On Dataset A, ... On Dataset B, ...`, `When removing X, ...`, sentences with ≥ 4 numbers);
- **paper-organization roadmaps** (`The rest of this paper is organized as follows...`).

## 5. Growing Your Personal Paper Memory Bank

Add any paper excerpt you admire (`.md`, `.tex`, `.txt`, or `.pdf`) so the skill learns from your preferred venues and authors:

```bash
python3 scripts/paper_memory.py add \
  --file excerpt_datasets.txt \
  --paper "MyFavoritePaper" --venue ACL --year 2026 --type L1 \
  --subsection exp.datasets --heading "Datasets" \
  --included "grouped 4 benchmarks by reasoning type; justified out-of-domain split" \
  --omitted "omitted split sizes for standard benchmarks; deferred prompts to Appendix B" \
  --focus "Shows breadth of transfer without reciting standard benchmark specs."
```

Entries are appended to `references/memory/user_memory.jsonl` (gitignored and preserved by `install.sh`) and immediately indexed into `references/memory/paper_memory.db`.
