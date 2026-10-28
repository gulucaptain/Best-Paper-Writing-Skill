# Introduction

Parts A/B/C and the backward-then-forward method are adapted from the base skill (see `NOTICE.md`). Route plans in §4 and the moves in §5 come from the award-paper analysis.

## 1. Think backward, then write forward

Backward (answer before writing — mostly already in the intake form):
1. What technical problem do we solve, and why is there no established solution?
2. What is the contribution (new task / metric / technical problem / technique)?
3. Why does it work in essence, and what new insight does it bring?
4. Which prior methods lead the reader to exactly this challenge?

Forward (write in this order): task → prior methods leading to *our* challenge → our solution and why it works → evidence → contributions.

## 2. What award introductions contain (55 papers)

Each sentence of 55 award introductions was labelled with its function. Presence = number of papers in which the function occurs; position = where it first appears (0 = first sentence, 1 = last).

| Function | Papers | First appears at | Tier |
|---|---|---|---|
| Credit to prior work (specific achievements) | **55** | 0.03 | **always** |
| Gap (limitation, its reason, the tension) | 54 | 0.10 | **always** |
| Method | 54 | 0.41 | **always** |
| Results | 51 | 0.67 | **always** |
| Setting / task / concrete scene | 47 | 0.00 | usual |
| Insight or goal (usually just before the method) | 43 | 0.38 | usual |
| Contributions (list 16, prose 17, none 22) | 33 | 0.83 | common |
| Contrast with specific prior work | 32 | 0.58 | common — **write it for every method paper** |
| Stance | 28–35 | 0.88 | optional, at the end |

Shape:
- 6 prose paragraphs (p10–p90: 3–8), ~610 words (430–900), 26 sentences (17–38).
- The gap appears by paragraph 2 (median); the last paragraph is contributions (18), results (15) or a stance (7).
- One message per paragraph; the first sentence states it.
- No limitations paragraph (limitations go to report.md for the Limitations section).

## 2b. What makes it read like an award paper
1. **Tension before idea.** The gap is set up as a conflict the idea resolves. Award papers use: two goals that pull apart (*tradeoff*, 21/55), a missing capability (13), an obvious fix that is too expensive (8), an unexplained phenomenon (6), an open question (4), a belief the results overturn (2).
2. **Credit, then gap.** Every award introduction credits prior work with a specific achievement before criticising it, and describes the component it later blames.
3. **The insight as an observation, not a formula.** 43/55 state an insight or goal, usually just before the method, but only 4/55 use “our key insight is”. Write the observation itself: “The highest frequency a scene can contain is bounded by the sampling rate of its views.”, “We find that …”, “The main idea is …”, “Our work is based on the observation that …”, “Surprisingly, …”. Use a formula at most once, never in the abstract.
4. **A handle when there is one.** 27/55 name the idea itself (“next-brick prediction”, “foundation datasets”) — distinct from the method’s name. Name it once, where it is introduced, and reuse the same words.
5. **Position against the closest work.** After the method (median position 0.58), name the closest work and state one checkable difference — mechanism (most common), scope, cost, evaluation, assumption, input or output. Forms: “Unlike X, which …, our …”, “In contrast to X, which requires …, Y …”, “Previous work addresses … by …, which is not applicable to …”, “While X …, we …”. Reviewers will look for this paragraph.
6. **One concrete example.** 36/55 use a concrete example (an input that breaks prior work, a scene, a striking number, an analogy), usually in paragraph 1–2. A list of application domains is not an example.
7. **Promote the work.** Award introductions use evaluative words (*outperforms*, *efficient*, *first*, *effective*) about three times; back each with evidence. Do not be more modest than the evidence allows.
8. **Plain connective tissue, full sentences.** Award introductions use about one logical connector (however/therefore/thus/moreover/specifically/…) per 100 words (p10–p90: 0.4–1.4); sentences average 23 words. Let paragraph order and old→new information flow carry most of the logic, but keep relations inside sentences (*while*, *by*, *which*, *because*) rather than splitting every fact into its own short sentence or appending “, making …” clauses. Put short sentences at the pivots (the bottleneck, the cause, the idea) and keep the mean around 20–24 words. Colons are fine; dashes are not used (author preference; `style-rules.md` §1).
9. **Story, not tables.** A result sentence carries 0–2 numbers; the introduction carries a median of 4 numbers. Ablation values and protocol details stay in the experiments.
10. **Say each thing once.** Assign every claim (the gap, the insight, each advantage, each result) to exactly one paragraph. Do not restate the insight after the method, do not re-list the research questions, and do not let the contributions repeat the results paragraph — if a contributions list is used, its items are one line each and point to sections; otherwise end with results or a stance. Repetition was the most common weakness found by blind reviewers.
11. **Short background.** Award introductions reach the specific problem fast (the gap appears by paragraph 2). Keep generic field background to at most two sentences before the specific setting or credit.
12. **No implementation details** (layer counts, grid sizes, data pipelines, hyperparameters) unless they are the contribution.

## 3. Building blocks (from the base skill)

### Part A — Opening
| Version | Use when | Skeleton |
|---|---|---|
| A:V1 task → applications | niche task | `[Task] aims to recover [output] from [input]. It enables [A], [B] and [C].` |
| A:V2 applications/credit first | familiar task | `[Task/Method] has [specific success] …` |
| A:V3 general → specific setting | new setting of a known task | `[General task] … This paper focuses on [setting], recovering [output] from [input].` |
| A:V4 open with the challenge | familiar task, sharp failure | `[Importance]. Given [input], previous methods usually … Although they work in many cases, they fail at … because …` |

### Part B — Technical challenge (limitation **and** technical reason)
| Version | Use when | Skeleton |
|---|---|---|
| B:V1 challenge chain | existing task | `This problem is challenging due to … Traditional methods … However, they … Recently, … However, they … because …` |
| B:V2 insight with classical roots | your idea echoes classical work | `A typical approach is [insight], long explored in … However, … because … Newer methods … still … because …` |
| B:V3 decomposed challenges | novel task | `Our goal is … This is challenging for three reasons. First, … Second, … Finally, …` |

Do not present a naive solution and then patch it. Ruling out an obvious alternative with a quantified reason is different and allowed (`cost` route).

### Part C — Our solution
Introduce two or three components through the problem each one solves and how they depend on one another (C:V2 is the model). Avoid three same-shaped sentences in a row (“A does … . B does … . C does … .”).
| Version | Use when | Skeleton |
|---|---|---|
| C:V1 one contribution, several advantages | single core idea | `We propose [Name], a [category] for … (Fig. 1). Specifically, … In contrast to …, … Another advantage is …` |
| C:V2 two contributions | second component fixes a problem left by the first | `… Specifically, … However, [remaining problem]. To address it, …` |
| C:V3 new module in an existing pipeline | module paper | `Following [pipeline], … Our key component is … We observe that … In contrast to [generic alternative], …` |
| C:V4 observation-driven | one key observation | `We observe that … Based on this, we … This leads to …` |

Avoid: describing only abstract insights with many new terms while hiding what the method actually does.

## 4. Route paragraph plans

### `failure` (card: mip-splatting)
1. Task → lineage ending at the method you fix; credit it with specifics.
2. How that method works — include the component you will blame.
3. Failure condition (Fig. 1) → root cause → mechanism (“Specifically, [condition] changes A while B stays fixed, causing …”).
4. Key insight → contribution 1 (answers symptom 1). “Nonetheless, [symptom 2] …” → contribution 2.
5. Contrast with how prior work handles it + benefit beyond training conditions; evidence with numbers; contributions.

### `cost` (card: mip-nerf)
1. Credit the method; state the flaw as a thesis (“is flawed in a manner that …”).
2. Mechanism; “works well when [contrived condition] … but in less contrived scenarios …”.
3. Obvious fix → why it is prohibitive, **quantified**.
4. Borrowed or new principle that moves the cost (e.g., pre-filtering); our method.
5. Evidence (numbers) + secondary advantages (speed, size).

### `capability-gap` (card: dreambooth)
1. Concrete scenario(s) a reader can picture; why it is hard.
2. Credit current models; “they lack the ability to …”; “The main reason is …”.
3. Goal phrased as a mechanism; technique 1.
4. Side effect of technique 1 → technique 2.
5. Applications; new evaluation (dataset/protocol/user study) for the new task.

### `insight` (card: dpo)
1. Why the capability matters, with one or two vivid examples.
2. Dominant method credited; its cost itemised.
3. “In this paper, we show that [objective] can be optimized [directly] …” + the analytical observation.
4. Intuition of the resulting update/design; mechanism-level contrast (“While existing methods use X to …, we use it to …”).
5. Single main contribution; evidence with scope (tasks, model size).

### `trend` (no exemplar card yet)
1. Problem + approach category in sentence 1; 3-stage history; “Even so, [old paradigm] still …”.
2. “As [enabler] improves, we ask whether … almost entirely”; closest work with two checkable limits.
3. “We take a further step towards …”; method answering each limit; calibrated result; named departure.
4. Optional side claims, each with its exception or pre-empted objection.

### `scaling` (L3, empirical scaling / recipe)
1. The ingredient that drove progress elsewhere, or the practical decision at stake (with a concrete number).
2. The state of this field: what people use and believe, and what prior attempts found.
3. The open question, asked plainly.
4. What we changed to make the study possible (the ingredients/setting), in a short enumerated sentence.
5. The regularity found, with the headline numbers and the most surprising observation; contributions.

### `mechanism` (L5, analysis / explanation)
1. The phenomenon, stated so a newcomer sees why it is puzzling.
2. Existing explanations and why they do not account for it (one sentence each).
3. Our claim, named (“implicit X”, “two timescales”), stated as the paper’s thesis.
4. The mechanism in one or two sentences, with intuition.
5. Evidence from two sides (controlled experiments + tractable model), with key numbers; contributions.

### `resource` (L7, dataset / benchmark / platform)
Coarse arc in award papers: Gap → Resource → (Gap) → Method/collection → Result.
1. The capability the field wants and why existing data cannot deliver it (scale, realism, diversity, labels, representativeness) — a concrete number or example.
2. Why the obvious way to collect it fails (cost, hardware, privacy); our collection principle.
3. What the resource contains, with one or two scale numbers; the closest existing datasets and the checkable difference.
4. What it enables: baselines, a benchmark, a model trained on it, or findings — stated as findings, not as possibilities.
5. Release and contributions.

### `measurement` (L8, sensing / optics / physical system)
Coarse arc: Setting (what we want to measure) → Gap/tradeoff of existing sensors → Method (sensing principle) → Result (prototype).
1. The phenomenon and why measuring it matters, with a concrete scene.
2. Existing sensors and the tradeoff they face (speed vs. resolution, bandwidth vs. range…).
3. The principle we borrow or introduce and how it escapes the tradeoff.
4. Prototype and demonstrations; contributions.

### `theory` (L6)
Coarse arc: Setting/question → prior results → main result in words → comparison with known bounds → implications.
1. The question and why it is open or important.
2. What is known (prior bounds, assumptions) and what is missing.
3. Our main result in plain words (cite the theorem), then the technique.
4. How it compares with known results; implications; outline (theory papers often end with an outline).

### `re-examination` (L4)
Coarse arc: Credit/common belief → question → our test → findings → stance.
1. The belief or practice and its supporting evidence, credited fairly.
2. The question we ask and why the existing evidence does not settle it.
3. Our test (controlled comparison, new metric) in one paragraph.
4. Findings, then a stance that follows from them (“X is a property of the metric, not of the model”).

## 5. Sentence-level moves (retrieve examples from `exemplars/moves.jsonl`)

| Move id | Purpose |
|---|---|
| `intro.task` | define task / importance concretely |
| `intro.gap.assumption` | prior methods assume X; X breaks when … |
| `intro.gap.failure` | credit + observable failure under a condition |
| `intro.gap.mechanism` | why the failure happens (what changes, what stays fixed) |
| `intro.gap.reason` | “The main reason is …” |
| `intro.gap.cost` | the method/fix is too expensive, quantified |
| `intro.gap.capability` | models lack the ability to … |
| `intro.gap.unknown` | origin/why remains unclear |
| `intro.question` | “This raises the question …” / “we ask whether …” |
| `intro.insight` | the observation the method follows from (state it directly) |
| `intro.borrowed-principle` | principle from another field that solves the cost |
| `intro.goal` | goal phrased as a mechanism |
| `intro.remaining-problem` / `intro.second-technique` | problem left by contribution 1 → contribution 2 |
| `intro.contrast-mechanism` | “While existing methods use X to …, we …” |
| `intro.claim-exception` | strong claim with its exception in parentheses |
| `intro.stance` | what the work changes for the field (see `claim-calibration.md` §5; exemplars: `abstract.open.position`) |
| `intro.evidence` | calibrated result sentence with scope |
| `intro.ours` | “In this work, we present …” |
| `intro.scope` | “Our focus is on A, rather than on B.” |
| `intro.contribution` | contribution sentence(s) |
| `relwork.contrast` / `relwork.complementary` / `relwork.closest` | positioning |
| `abstract.open.*` | abstract first sentences by opening type |
| `pattern.*` | reusable sentence patterns |

## 6. Contributions list
- Optional. A single strong contribution can be stated in one sentence (DPO, CO3D).
- If used: 2–4 bullets, each verifiable and pointing to a section/table; modules of one method go in one bullet; analysis findings or resources get their own bullet.
- The list must match the abstract and the alignment matrix.

## 6b. Paragraph-level examples
`python3 scripts/find_exemplars.py --para <function> [--type L7]` prints award-paper paragraphs whose main function is `scene`, `task`, `credit`, `history`, `gap`, `reason`, `tension`, `question`, `goal`, `insight`, `method`, `mechanism`, `contrast`, `result`, `theory-result`, `stance`, `scope`, `contribution`, `outline`, with a note on why each works. `--phrases <function>` prints sentence frames with examples. Study the order of information, never copy wording.

## 7. Checklist
- [ ] Credit to specific prior work precedes the gap; the component blamed later is described first.
- [ ] Gap = what fails/is missing + technical reason + condition, set up as a tension.
- [ ] A contrast paragraph or sentence names the closest work and one checkable difference.
- [ ] The insight is stated as an observation; at most one “key insight”-type formula, none in the abstract.
- [ ] The handle appears where the idea is introduced; the core idea is asserted, not hypothesised.
- [ ] One concrete example in paragraph 1 or 2.
- [ ] No limitations, failure cases or disclaimers; mixed results scoped to the wins.
- [ ] Every gap ↔ one contribution.
- [ ] The component blamed for the failure was described before it is blamed.
- [ ] Closest work named; difference is specific.
- [ ] Results as claims with headline numbers; wording is the strongest the claim map allows; the work is promoted with evidence.
- [ ] A stance sentence if the results support one; no implementation details; no defensive qualifiers.
- [ ] Each claim appears in one paragraph only; contributions do not repeat the results paragraph; generic background ≤ 2 sentences.
- [ ] The cause has its own sentence (“The main reason is that …”); the tension and the idea are stated in short, quotable sentences.
- [ ] Sentences average 20–24 words with short pivots; no run of three short sentences; no sentence over ~35 words; a claim and its number share a sentence.
- [ ] No dashes; few trailing participial clauses.
- [ ] `check_draft.py` shows no ERROR and no WARN for connectors, numbers, sentence length or participial clauses (or each is justified).
