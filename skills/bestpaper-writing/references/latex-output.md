# Writing into a LaTeX template

Typical case: the CVPR/ICCV author kit (`main.tex`, `preamble.tex`, `sec/0_abstract.tex`, `sec/1_intro.tex`, `sec/2_formatting.tex`, `sec/3_finalcopy.tex`, `main.bib`, `cvpr.sty`, `ieeenat_fullname.bst`).

## Steps
1. **Copy** the template to the working folder (e.g., `paper/`). Never edit the original template. If the user has no template, the repository ships the official CVPR 2027 kit in `template/CVPR2027/` (repository root, outside this skill folder).
2. **Title**: replace the `\title{…}` in `main.tex`, without a dash (author preference); a colon is fine, and the handle should be in the title when there is one (“Describe, Don't Name: …”). Keep the review mode and anonymous authors unless told otherwise.
3. **Sections**: keep `\input{sec/0_abstract}` and `\input{sec/1_intro}`; remove the `\input` lines of the template’s example sections (`2_formatting`, `3_finalcopy`) and do not leave their text in the paper.
4. **Abstract**: `sec/0_abstract.tex` contains only `\begin{abstract} … \end{abstract}`; one paragraph, no citations unless essential.
5. **Introduction**: `sec/1_intro.tex` starts with `\section{Introduction}` and `\label{sec:intro}`. Paragraphs only; a contribution list may use `\begin{itemize}`. No `\subsection`, no `\paragraph{}` move labels.
5b. **Method and Experiments**: write `sec/3_method.tex` (`\section{…}` named after the method or idea, `\label{sec:method}`) and `sec/4_experiments.tex` (`\section{Experiments}`, `\label{sec:exp}`), and add their `\input` lines after the introduction (a related-work file `sec/2_related.tex` may sit between them if the user provides one). Subsections and run-in `\paragraph{Datasets.}` headings are normal here. Tables use booktabs (loaded by the CVPR kit) and `\TODO{}` for missing numbers; figures the user has not supplied are listed in `report.md`, not added as empty boxes.
6. **Citations**: copy the user’s `.bib` to `main.bib`; cite with `\cite{key}` or `\citep{}`/`\citet{}` if natbib is loaded (the CVPR kit loads natbib; `\cite` works). Use only keys that exist in the file. For a missing reference write `[TODO: cite …]` in the text (or define `\newcommand{\todo}[1]{\textcolor{red}{[TODO: #1]}}` in `preamble.tex`).
7. **Figures/tables**: refer to them as `Fig.~\ref{fig:teaser}` / `Tab.~\ref{tab:main}` only if you also add a placeholder figure; otherwise write “Figure 1” in plain text and list the figure in `report.md`.
8. **Compile**: `latexmk -pdf main.tex` (or `pdflatex` → `bibtex` → `pdflatex` ×2). Fix errors; report undefined citations/references that remain.
9. **Escape** `%`, `&`, `_`, `#` in text; write ×, ≥, τ as `$\times$`, `$\geq$`, `$\tau$`.

## Checks
- `python3 scripts/check_draft.py paper/sec/0_abstract.tex` and `… paper/sec/1_intro.tex` (the checker strips LaTeX commands).
- The compiled PDF shows the title, abstract and introduction only (plus references).
