# Style Rules

Derived from the award-paper analysis (vocabulary, sentence patterns, common errors). `scripts/check_draft.py` enforces the mechanical subset.

## 1. Word choice

### Use freely
present, introduce, propose, show, find, observe, indicate, suggest, rely on, assume, be limited to, struggle to,
in contrast, whereas, rather than, specifically, in particular, to this end, note that, intuitively, at the cost of,
without requiring, allows us to, enables.

### Use only with a concrete follow-up in the same sentence
| Word | Condition |
|---|---|
| novel / new | prefer stating *what* is new; never “novel and effective” |
| efficient / fast | give time, FLOPs or memory |
| robust / general / scalable | state the tested range |
| significantly | only with a statistical test; otherwise give Δ |
| state-of-the-art | name the baselines/benchmarks |
| notably / remarkably / interestingly | follow with a number or contrast; at most once per section |
| the first | scope it; prefer the specific difference |
| plays a … role | follow with the mechanism (“as it determines …”) |

### Avoid (boilerplate / LLM tells)
has attracted increasing attention · in recent years, … has become a hot topic · plays an important role (bare) ·
extensive experiments demonstrate the effectiveness/superiority · to the best of our knowledge (as filler) ·
delve into · pivotal · crucial (more than once) · paradigm shift · unlock the potential · seamlessly ·
a myriad of · landscape · in the realm of · it is worth noting that · it can be seen that · in order to (use “to”) ·
simple yet effective · comprehensive experiments.

### Never in the paper text (workflow traces and disclaimers)
- Words describing the user’s input: *supplied, provided (results/evaluation), the reported evaluation, according to the input, in our setup* (as a hedge).
- Move labels or bracketed tags (“**Gap.**”, “[intro.insight]”, “History → gap”).
- “Table k reports …” as the subject of a sentence; write the claim and cite the table: “… outperforms X (Tab. 1)”.
- Disclaimers: *does not establish, does not imply, remains to be evaluated, we leave … for future work, one limitation is, fails on* — these belong in the Limitations section.
- Downgrading the core idea: *our hypothesis is, we take the view, we conjecture that* (for the main idea).

- Defensive qualifiers about the protocol: *in our comparison, within the tested budgets, scores are computed on …, under identical hyperparameters, in the evaluated setting*.

### Corpus ranges (55 award papers; `check_draft.py` warns above p90)
| Metric | Abstract median (p90) | Introduction median (p90) |
|---|---|---|
| Numbers | 1 (5.6) | 4 (14.6) |
| Logical connectors per 100 words (however, therefore, thus, moreover, yet, whereas, in contrast, instead, specifically, in particular, as such, importantly, finally, …) | 0.6 (1.6) | 0.9 (1.4) |
| Sentences with a colon or dash | 11% (29%) | 10% (23%); **this skill uses colons sparingly and no dashes (author preference)** |
| Sentences ending in a participial clause (“…, making …”) | 8% (25%) | 8% (20%) |
| Hedges (*may, might, could, likely, suggest*) | 0 (1) | 1 (3.6) |
| Boosters (*significantly, remarkably, notably, …*) | 0 (1) | 1 (3) |
| Evaluative words (*outperforms, efficient, effective, first, novel, state-of-the-art*) | 1 (3) | 3 (7.6) — 90% use at least one |
| “key insight”-type formulas | 0 | 0 (only 4 of 55 papers) |
| Sentence length (words) | 24 | 23 |

AI drafts typically exceed the connector range and fall below the evaluative-word range. **Aim near the median, not at zero.** Removing every connector produces the opposite tell, a string of short, unconnected sentences.

### Colons yes, dashes no (author preference)
- **Colons** are allowed, as in award papers (~10% of sentences): to introduce a list, an example, or the handle at a pivot (“Anti-aliasing therefore asks for two things at once: …”). Keep them under about one sentence in six; `check_draft.py` warns above the corpus p90.
- **Dashes** are not used: no em dash (—, `---`) and no spaced en dash. Rewrite instead.

| Instead of | Write |
|---|---|
| “Our model — trained once — handles any scene.” | “Trained once, our model handles any scene.” |
| “This leads to a tradeoff — quality or speed.” | “This forces a tradeoff between quality and speed.” or a colon |
| “The answer is simple — X.” | “The answer is simple: X.” or a short second sentence |

Numeric ranges (2–3) and hyphenated compounds are not punctuation dashes and are fine.

### Merging sentences without participial tails
Merging two facts by appending “, making …”, “, extending …”, “, bringing …”, “, enabling …” is the most common AI pattern after short sentences are removed (typical AI drafts: 32% of sentences; award papers: 8%). Prefer
- a subordinate clause: “Inference is 20× faster because each scale is predicted in parallel.”;
- *while* for two results: “Method X lowers the error from 12.4 to 8.1 while running 3× faster.”;
- *by* for means: “TaylorRand avoids the exponential graph by propagating Taylor coefficients.”;
- a relative clause: “…, which removes the task discrepancy.”;
- or simply end the sentence; the significance usually follows in the next one or is not needed.

### Sentence length and rhythm: long and short, not uniform
Award introductions average **23 words per sentence** (p10–p90: 20–29), and about one sentence in nine is short (≤ 12 words). Readers remember the short ones, because they sit at the pivots. Uniformly long sentences read as heavy; uniformly short ones read as choppy. Aim for a mean of **20–24 words** with a few short pivots.
- **Short sentences go at the pivots**: the bottleneck (“This person is the bottleneck of the cycle.”), the cause (“The main reason is that …”), the idea (“We therefore describe objects to the policy rather than name them.”), the turn (“But the two predictions solve different tasks.”). Two to four per introduction is typical; never three in a row.
- **Everything else carries a relation inside the sentence** (cause, contrast, condition, means) through *because*, *while*, *by*, *which*, *so that*.
- **Keep a claim and its evidence in one sentence**: “Method X lowers the error from 12.4 to 8.1 while running 3× faster”, not “Method X improves accuracy and speed. It lowers the error from 12.4 to 8.1. It runs 3× faster.”
- **Do not over-merge.** If a sentence passes ~35 words or hides the paragraph’s key claim in a trailing clause, split it and let the key claim stand alone.
- **Do not over-pivot either.** Three or four short pivots per introduction; more than ~20% short sentences (award p90: 22%) reads like a blog post.

### One aphorism, not four
A contrast such as “code that runs is not a picture”, “X need not come from Y” or “rather than A, we B” is memorable once. Award introductions use such constructions in a median of 3% of sentences (p90: 8%), abstracts almost never (p90: 13%). Use one for the thesis, possibly echoed in the title, and state everything else as plain fact. Do not end the abstract or introduction with a balanced maxim (“X is only the first half; the second half is Y”); end with the result or a concrete stance.

### Every style rule has two sides
Each rule in this file aims at the award-paper median, not at an extreme. Fixing one tell by pushing a metric to zero creates the opposite tell: no connectors gives choppy prose, merging every short sentence gives trailing “, making …” clauses, short pivots everywhere give a blog tone. When a WARN fires, move the metric back toward the median and re-read the paragraph aloud.

### Connective tissue without connectors
- Repeat the key noun of the previous sentence at the start of the next (“… a 2D dilation filter. This filter …”).
- Put old information first and new information last; the reader then needs no “therefore”.
- At one real turn, a short sentence can replace a connector (“But the two predictions solve different tasks.”); do not chain several.
- Let the paragraph break mark the turn from gap to idea.

## 2. Sentence patterns worth using
| Pattern | Purpose | Example structure |
|---|---|---|
| `We present X, a [category] that [does] from [input].` | dense introduction | VGGT, pixelSplat |
| `Although X [credit], it [failure] when [condition].` | fair credit + gap | Mip-Splatting |
| `Specifically, [condition] changes A, while B remains fixed, causing C.` | failure mechanism | Mip-Splatting |
| `A straightforward solution is … But this is prohibitively expensive …, which requires …` | rule out the obvious | Mip-NeRF |
| `[Property of the problem] [consequence]. We therefore/Based on this, …` | pivot: state the observation directly | Mip-Splatting, DPO |
| `Rather than [A], we [B].` | design contrast | DynIBaR |
| `While existing methods use X to …, we use X to …` | mechanism-level contrast | DPO |
| `… does not require A, nor does it B.` | removed costs | SpiderMatch |
| `[Design] reduces [cost] by [mechanism], while still allowing [property].` | trade-off | Swin |
| `Although [metric] improves, this does not imply [capability].` | bounded conclusion | RLVR |
| `Note that our focus is on A, rather than on B.` | scope | DynIBaR |

## 3. Paragraph and sentence rules
1. First sentence = the paragraph’s message.
2. Old information first, new information last.
3. Subject and verb within the first ~15 words; long modifiers after the main clause.
4. Comparisons compare like with like (“Unlike prior methods, our method …”, not “…, we …”).
5. One hedge per claim, placed next to the condition.
6. Define a term at first use (an in-sentence clause is enough: “neural scaling laws, in which error falls off as a power of …”).
7. Never mix `although … but`.

## 4. Originality
- Exemplars teach structure. Do not reuse any exemplar sentence or any run of ≥ 6 consecutive words from it.
- Vary openings across paragraphs; do not start more than two paragraphs with the same word.

## 5. Final checklist
- [ ] No item from “Avoid” or “Never in the paper text”.
- [ ] No dashes; colons only where they introduce a list, example or handle; few trailing “, making …” clauses.
- [ ] The pivots (bottleneck, cause, idea, turn) are short sentences; the rest average 20–24 words.
- [ ] `check_draft.py`: no ERROR; no WARN for connectors, numbers, hedges, sentence length, runs of short sentences or participial clauses (or each is justified).
- [ ] Every conditional word in §1 has its concrete follow-up.
- [ ] Every number has a unit, benchmark and baseline.
- [ ] Terminology identical across abstract, introduction and contributions.
