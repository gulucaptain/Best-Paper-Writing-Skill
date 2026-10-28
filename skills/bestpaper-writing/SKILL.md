---
name: bestpaper-writing
description: Draft or rewrite the title, Abstract, Introduction, Method and Experiments of an ML/CV paper in the style of CVPR/ICCV/NeurIPS best papers, distilled from 60 award papers. Use when the user either (A) fills in the intake form (assets/intake_form.html JSON) or describes problem, idea, method and results, or (B) pastes an existing abstract (or abstract plus introduction) to make it more convincing. Can write directly into a LaTeX template such as the CVPR author kit. Not for related-work surveys, rebuttals or plain proofreading.
---

# Best-Paper Writing (v1.0): Abstract, Introduction, Method, Experiments

Turn a description of a research project (or a draft abstract) into an Abstract and Introduction that read like a recent CVPR/ICCV/NeurIPS award paper.

This skill is grounded in a sentence-by-sentence annotation of **55 award papers** (2021–2025; 60 papers are analysed in total, and 5 of them (from 2024) are held out for testing, see `PAPER_LIST.md` in the repository root): what functions their abstracts and introductions contain, in which order, and how they read (`references/corpus-profile.md`). Award papers persuade through:

1. **A sharp motivation** — credit to specific prior work, then a concrete gap (what fails or is missing, when, and why), set up as a tension the paper resolves.
2. **An idea about the problem** — an observation from which the method follows, stated directly; a short handle for the idea when there is one (“next-brick prediction”).
3. **Clear positioning** — the closest work is named and one checkable difference is stated.
4. **Confident, evidenced claims told as a story** — results as claims with one or two headline numbers; the work is promoted where the evidence allows; a stance when the results support one. Weaknesses belong in the Limitations section, not in the Abstract or Introduction (author preference).
5. **Plain, rhythmic prose**. Each claim is stated once. Short, quotable sentences at the pivots (the bottleneck, the cause, the idea); the rest are full sentences (mean 20–24 words) that carry their reasons through *because*, *while*, *by*, *which*, not through trailing “, making …” clauses. Few logical connectors; colons allowed, **no dashes** (author preference). Mechanisms and examples instead of adjectives, short background, no implementation details.

Scope: title, Abstract and Introduction for all eight paper types (L1–L8, `references/routing.md`); also **Method** (`references/method.md`) and **Experiments** (`references/experiments.md`), mainly for method papers (L1/L2). Write the Abstract and Introduction first; Method and Experiments follow the same claim map.

## Workflow

Do not write prose before Step 4.

### Step 0 — Intake (two input modes)
**Mode A: intake form.** If the user provides an intake JSON (exported from `assets/intake_form.html`, schema `bestpaper-intake/v1`), run `python3 scripts/intake_to_brief.py <file.json> --out brief.md --bib refs.bib` (paths relative to this skill folder) and work from `brief.md`; exit code 2 means a required field is missing. If the user describes the work in free text, load `references/intake-form.md` and map the description onto it. When a user has no material ready, point them to `assets/intake_form.html` (a local, offline form that exports JSON; the form is in Chinese).

**Mode B: complete abstract in.** If the user pastes an existing abstract (optionally with the introduction), do not rewrite it blindly. First reverse-engineer it into the intake fields of `references/intake-form.md` (task, dominant prior approach, gap and its reason, closest work, key insight, method components, results with numbers) and show the user a short table: field, what the draft says, status (present / vague / missing). Facts, numbers and terminology in the draft are the user's and are kept verbatim; never add a result, baseline or reference the draft does not contain. Then handle missing fields as below, and continue with Steps 1–8. In `report.md` add a **change table** (original sentence → revised sentence → reason, citing the award-paper pattern it follows) so the author can accept or reject each change.

In both modes:
- If a **required** field is missing (key idea, concrete gap with its reason, closest work, results with numbers), ask once in a compact list **before drafting**. In the same message, ask for the memorability fields that are empty (efficiency, integration with existing pipelines, supported inputs, applications, a concrete example, what is surprising, the trend it follows, the team’s name for the idea): these, not the prose, are what made award abstracts stand out in our comparisons. If the user cannot answer now, continue with `[TODO: …]` placeholders. Ask in plain text; do not depend on any agent-specific question tool.
- Never invent results, numbers, baselines, datasets or references.

### Step 1 — Claim, tension, handle, stance, headline numbers
Write these for yourself (they go into `report.md`, not the paper):
- **Claim**: `We show that [method/finding] [achieves what] [under which setting], because [key reason].`
- **Tension type**: tradeoff / capability-missing / obvious-fix-too-costly / unexplained-phenomenon / open-question / belief-overturned (`routing.md`).
- **Insight**: the observation about the problem the method follows from, written as a plain statement (not “Our key insight is …”).
- **Handle** (optional): a short phrase naming the idea, distinct from the method’s name. Use the user’s term if they have one; otherwise propose one in the report. When there is a handle, put it in the title.
- **Closest work**: 1–2 works and the checkable difference (mechanism, scope, cost, assumption, input, output, evaluation).
- **Stance** (optional): what the work changes for the field, only if the results support more than “better on benchmark B”.
- **Headline numbers**: the 1–2 results that carry the claim.

### Step 2 — Route
Load `references/routing.md`. Choose the paper type and motivation type; note the abstract arc and introduction plan.

### Step 3 — Claim map
Load `references/claim-calibration.md`. List each claim with its evidence and the **strongest wording the evidence supports**. Use it to make claims confident where supported and scoped where not — never to add disclaimers. Mark headline / supporting / table-only numbers.

### Step 4 — Skeleton
Load `references/introduction.md` and `references/abstract.md`. One line per paragraph (its message = its first sentence); one line per abstract sentence. Check against the award-paper tiers (`introduction.md` §2):
- **always**: credit to specific prior work → gap with reason → method → results;
- **usual**: opening setting or concrete scene; the insight just before the method;
- **for method papers**: a contrast with the closest work after the method;
- **optional**: contributions list, stance (at the end).
The abstract defaults to Setting → Gap → Method → Result (`abstract.md` §3).
Mark the **pivot sentences** (the bottleneck, the cause, the tension, the idea); they will be short and quotable. Then make a **claim index**: list every claim (gap, insight, each advantage, each result, stance) and the one paragraph where it appears. A claim listed under two paragraphs is merged into one. Generic field background gets at most two sentences.

### Step 5 — Draft with exemplars
For each paragraph, read 2–3 award-paper paragraphs with the same function and, if possible, the same paper type: `python3 scripts/find_exemplars.py --para <function> --type <L*>`; for sentences, `python3 scripts/find_exemplars.py <move>` or `--phrases <function>`; for whole introductions, the route’s card in `references/exemplars/cards/`. Learn their order of information and rhythm; never copy a sentence or a run of ≥ 6 words. Write in the authors’ voice (“we”, “our model”); never describe the user’s input as “supplied”, “provided” or “reported”.

### Step 5b — Method and Experiments (when requested)
1. Extend the claim map into an **evidence map**: claim → method subsection → experiment (table/figure) → ablation. Claims without evidence are softened in the introduction or get an experiment `[TODO]`.
2. Method: follow `references/method.md` (opener, preliminaries, one subsection per component with need → mechanism → property, objective, optional discussion). Mechanisms, equations and losses the user has not given are `[TODO]`; never invent them.
3. Experiments: follow `references/experiments.md` (opener, setup, claim-first results per benchmark, ablations that mirror the claims, analysis, limitations). Tables use booktabs with `\TODO{}` cells for missing numbers.
4. Limitations belong in the experiments or a separate section; the author preference excludes them only from the abstract and introduction.

### Step 6 — Output
- **LaTeX template given** (e.g., a CVPR author kit): load `references/latex-output.md` and follow it.
- **No template**: write Markdown (`# Abstract`, `# Introduction`).
- The paper text contains no move labels, workflow comments, or bracketed notes other than `[TODO: …]` / `\todo{…}`.

### Step 7 — Check
1. Run `python3 scripts/check_draft.py <files>` on the abstract and the introduction. Fix every `ERROR`. Each `WARN` means the draft is outside the range of 90% of award papers (connectors, numbers, hedges, boosters, “key insight” formulas, sentence length, runs of short sentences, trailing participial clauses) or shows a known AI-draft habit — revise or justify it in the report. `NOTE`s are information (e.g., the draft promotes the work less than award papers do). `python3 scripts/style_metrics.py <files>` shows every metric with its corpus percentile.
2. Semantic checks:
   - Specific prior work is credited before the gap; the gap is concrete (what fails, when, why) and the tension is resolved by the idea.
   - The insight is an observation about the problem, stated directly, not a hypothesis and not a description of the architecture.
   - The closest work is named with one checkable difference (method papers).
   - Results are claims at the strongest supported level, with headline numbers; the work is promoted where evidence allows; nothing is claimed that the evidence does not support (no unscoped “first”, “state-of-the-art on all benchmarks”).
   - No limitation, failure case or disclaimer in the Abstract or Introduction; mixed results are scoped to the wins.
   - No defensive qualifiers about the protocol; no implementation details.
   - Abstract, introduction and contributions state the same claims with the same strength.
   - Nothing is said twice inside the introduction (insight, research questions, results, advantages); the contributions do not repeat the results paragraph.
   - Read the draft aloud once: if several consecutive sentences each carry one bare fact, merge them so that each sentence carries a relation (cause, contrast, means, consequence).

### Step 8 — Deliver
1. The paper files (LaTeX project or Markdown).
2. `report.md` for the authors: claim, tension type, insight, handle, closest work, route, claim map, `check_draft` summary, `[TODO]` list, questions, and **notes for the Limitations section** (weaknesses deliberately left out of the abstract/introduction).

## Hard rules
- Never fabricate numbers, datasets, baselines, citations or results.
- Never cite a key that is not in the user’s bibliography; mark missing references with `[TODO: cite …]`.
- No limitations, self-undermining sentences or defensive qualifiers in the Abstract or Introduction.
- The Abstract and Introduction tell the story; tables tell the numbers.
- No generic openings (“has attracted increasing attention”, bare “plays an important role”) and no adjectives about the method without a concrete follow-up.
- Do not frame the work as a patch on a naive baseline (ruling out an obvious alternative with a quantified reason is fine).
- Keep terminology fixed once introduced.
- **No dashes** in the title, abstract or introduction (author preference): no em dash (—, `---`) and no spaced en dash. Rewrite with a colon, a comma, a short second sentence or parentheses. Numeric ranges (2–3) and hyphenated compounds (image–motion, train–test) are fine. `check_draft.py` reports each dash as an ERROR. Colons are allowed.
- **Name mechanisms, not abstractions.** When the input does not say how a component works (who inspects, what is compared, how something moves), write `[TODO: …]` and ask; do not fill the gap with abstract nouns (“state”, “record”, “inspection”, “protocol”) that sound complete but say nothing.
- **Describe components by their relation**, not as parallel items: what problem each one answers and what the next one fixes (“A keeps …; because A alone lets errors persist across edits, B …”), rather than “A does … . B does … . C does … .”
- **Figure and table numbers from notes or intake forms** refer to the author’s full draft. Do not cite them in the abstract or introduction unless the figure is part of the paper being written; list the example and its figure in `report.md`.
- **One aphorism.** Use at most one or two contrastive maxims (“X is not Y”) for the thesis; state the rest as plain fact.
- **Keep what makes the draft memorable.** When revising for a checker WARN, do not merge away the short pivot sentences, the cause sentence, or the handle in the title; fix the WARN elsewhere or justify it. A memorable draft that is slightly off the corpus statistics beats a statistically average one.
- Do not end sentences with a participial clause that restates significance (“…, making X possible”, “…, extending Y”, “…, bringing Z”). Award papers do this in ~8% of sentences; AI drafts in 30% or more.

## Files
| File | Load at |
|---|---|
| `references/intake-form.md`, `assets/intake_form.html`, `scripts/intake_to_brief.py` | Step 0 |
| `references/routing.md` | Step 2 |
| `references/claim-calibration.md` | Steps 3, 7 |
| `references/introduction.md`, `references/abstract.md` | Steps 4–5 |
| `references/corpus-profile.md` | when you need the award-paper statistics |
| `references/exemplars/` (`paragraphs.jsonl`, `phrasebank.csv`, `moves.jsonl`, `cards/`), `scripts/find_exemplars.py` | Step 5 |
| `references/style-rules.md` | Steps 5, 7 |
| `references/method.md`, `references/experiments.md` | Step 5b |
| `references/latex-output.md` | Step 6 (LaTeX) |
| `scripts/check_draft.py`, `scripts/style_metrics.py`, `references/corpus/corpus_stats.json` | Step 7 |

Use `python3`. Attribution and licences: `NOTICE.md`.
