# Experiments section

Derived from the same 55 award papers. Experiments are the most templated part of a paper: the structure below fits almost every method paper; what differs is which claims the experiments must prove.

## 1. Shape (what the corpus shows)
| Observation | Value |
|---|---|
| Length | median ~1,500 words (main paper; more in the appendix) |
| Opener | a roadmap sentence (“In this section, we …” appears in 18 / 55 papers) or the questions the experiments answer (DPO, pixelSplat; 12 / 55 frame experiments as questions somewhere) |
| Setup (datasets, metrics, baselines, implementation) | usually first; 13 / 42 have a subsection titled “Setup / Implementation details / Settings”, others use run-in paragraphs |
| Main results | one subsection per benchmark or task (Swin: ImageNet, COCO, ADE20K; Mip-Splatting: Blender, Mip-NeRF 360) |
| Ablations | 28 / 55 papers report ablations; usually the last numbered subsection before analysis |
| Qualitative results | 30 / 55 |
| Limitations | discussed in 43 / 55, as a subsection at the end of experiments (DreamBooth, Mip-Splatting) or as its own section |
| Supplementary material referenced | 44 / 55 (details that do not change the story go there) |

## 2. The six moves
**E0 · Opener.** One to three sentences: what is evaluated and in what order, or the questions the experiments answer.
> “We first present the implementation details of Mip-Splatting. We then assess its performance on the Blender dataset and the challenging Mip-NeRF 360 dataset. Finally, we discuss the limitations of our approach.” (Mip-Splatting)
> “… we ask: how efficiently does DPO trade off maximizing reward and minimizing KL-divergence with the reference policy …?” (DPO)

**E1 · Setup.** Datasets (size, split, why chosen), metrics (with direction ↑/↓), baselines (why these, how they were run: official code, same data), implementation (base code, iterations, hardware). Run-in headings are normal here (`\paragraph{Datasets.}`).
> “We build our method upon the popular open-source 3DGS code base. Following [18], we train our models for 30K iterations across all scenes and use the same loss function …” (Mip-Splatting)
> “We compare our results with Textual Inversion, the recent concurrent work of Gal et al., using the hyperparameters provided in their work.” (DreamBooth)

**E2 · Main results: claim first, then evidence, then reason.** Start the paragraph with the finding, cite the table, quantify the most important margin, then explain why with reference to the method, then point to the qualitative figure.
> “We report quantitative results in Table 1. Our method outperforms the baselines on all metrics, with especially significant improvements in perceptual distance (LPIPS). … Compared to the baselines, our method is better at capturing fine details and correctly inferring 3D structure …” (pixelSplat)

**E3 · Ablations mirror the claims.** One variant per design claim from the method, named by what is removed or replaced (“w/o prior preservation”, “No invertible”), each answering a question.
> “We perform ablations on RealEstate10k to answer the following questions: Is our epipolar encoder responsible for our model’s ability to handle scale ambiguity? …” (pixelSplat)
> “No invertible is a model variant that replaces our invertible mapping network … with separate forward and backward mapping networks …” (OmniMotion)

**E4 · Analysis, generalisation, applications.** What else the method enables or reveals: scaling, transfer, efficiency, new applications, human study. Each with its own claim-first paragraph.

**E5 · Limitations.** Honest failure modes with a figure, at the end of the experiments or in a separate section (never in the abstract or introduction, by author preference).
> “Our method employs a Gaussian filter as an approximation to a box filter for efficiency. However, this approximation introduces errors …” (Mip-Splatting)

## 3. Rules
1. **Evidence map first.** Before writing, list every claim from the abstract, introduction and method, and the table/figure that proves it. A claim without evidence is softened in the introduction or gets an experiment `[TODO]`; an experiment that proves no claim moves to the appendix.
2. **Claim-first paragraphs.** “Ours outperforms X on all metrics (Tab. 1), with the largest gain in Y” rather than “Table 1 shows the results.” Use “As shown in Tab. 1” sparingly.
3. **Numbers belong here.** Report margins, not only rankings; the abstract/introduction number limits do not apply. Keep at most two or three numbers per sentence; the rest stay in the table.
4. **Fair comparison is stated once, in the setup** (same data, official code, same backbone); do not repeat qualifiers in every results sentence.
5. **Every ablation answers one question** and is named by the change. Pair each with the method subsection it validates.
6. **Explain, do not only report.** After each comparison, one sentence on why, tied to the mechanism (“because the 3D filter bounds the frequency …”).
7. **Qualitative figures** show the claim the text makes (failure of the baseline, our fix), and their captions state the takeaway first. Layout, method order, insets and plot style: `figures.md` §5.
8. **Tables:** booktabs, best in bold, second underlined if useful, ↑/↓ in headers, units, the setting in the caption. Missing numbers are `\TODO{}` cells, never estimates.
9. **Limitations** are written here, concretely, with a cause and, where possible, a figure.
10. Style: past tense for what was done (“we trained”), present tense for what the results show (“Ours outperforms”). No dashes; colons are fine for run-in lists.

## 4. Skeleton
```text
\section{Experiments}                      % E0: what, in which order / which questions
\subsection{Setup}                         % E1: \paragraph{Datasets.} \paragraph{Metrics.} \paragraph{Baselines.} \paragraph{Implementation.}
\subsection{<Main task / benchmark 1>}     % E2: claim → Tab. → margin → reason → Fig.
\subsection{<Benchmark 2 or second task>}  % E2
\subsection{Ablation study}                % E3: one question per design claim, Tab.
\subsection{Analysis / Applications}       % E4
\subsection{Limitations}                   % E5 (or a separate section)
```

## 5. Table skeleton (CVPR kit has booktabs)
```latex
\begin{table}[t]
\centering
\caption{<Takeaway first>. <Setting>. Best in \textbf{bold}.}
\label{tab:main}
\small
\begin{tabular}{lccc}
\toprule
Method & Metric A $\uparrow$ & Metric B $\downarrow$ & Time (s) $\downarrow$ \\
\midrule
Baseline 1 \cite{key} & \TODO{} & \TODO{} & \TODO{} \\
Ours & \textbf{\TODO{}} & \textbf{\TODO{}} & \TODO{} \\
\bottomrule
\end{tabular}
\end{table}
```

## 6. Checklist
- [ ] Every claim of the paper has a table or figure; every table supports a claim.
- [ ] Setup states datasets, metrics (↑/↓), baselines and how they were run, once.
- [ ] Results paragraphs open with the finding and explain the reason.
- [ ] One ablation per design claim, named by the change.
- [ ] Limitations are concrete and placed here or in their own section.
- [ ] No invented numbers: missing values are `\TODO{}`.
