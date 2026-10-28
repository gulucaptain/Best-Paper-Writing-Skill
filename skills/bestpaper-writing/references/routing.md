# Routing: Paper Type × Motivation Type → Route

## 1. Paper type (first “yes” wins)

1. Main deliverable is a theorem/bound → **L6 theory** (plan `theory`)
2. Main deliverable is a dataset/benchmark/platform → **L7 resource** (plan `resource`)
3. New sensor/optics/physical measurement → **L8 measurement** (plan `measurement`)
4. Re-examines a popular claim → **L4 re-examination** (plan `re-examination`); explains a known phenomenon → **L5 analysis/mechanism** (plan `mechanism`)
5. Systematic sweep yielding an empirical law/recipe, or scaling an ingredient → **L3 empirical scaling** (plan in `introduction.md` §4)
6. Enables something previously impossible → **L2 new capability**; does an existing task better → **L1 method improvement**

All plans are in `introduction.md` §4. Plans for L4/L6/L7/L8 are derived from 3–5 award papers each; treat them as tested starting points and read the paragraph exemplars of the same type (`find_exemplars.py --para … --type L7`). `corpus/corpus_stats.json → structure.sequences_by_type` lists the coarse arcs of every award paper by type.

## 2. Motivation type (L1/L2)

| Type | Choose when | Diagnostic question |
|---|---|---|
| `failure` | A strong method breaks under a specific, reproducible condition | Can you show a figure where the baseline visibly fails? |
| `cost` | Existing methods (or an obvious fix) work but are too slow/expensive/complex | Can you quantify the cost you remove? |
| `capability-gap` | Existing models cannot do something users want at all | Is there no reasonable baseline for the full task? |
| `insight` | An analytical or empirical observation makes a complex pipeline unnecessary | Is there one sentence of math/observation from which the method follows? |
| `trend` | Your work is the next step of a visible field-wide trend | Can you tell a 3-stage history that ends with your paper? |

Papers often mix two; pick the one that explains **why the method exists**, use the other as a secondary paragraph.

**Tension type** (how the gap is made to feel like a conflict; frequencies in 55 award papers): two goals that pull apart — `tradeoff` (21); `capability-missing` (13); `obvious-fix-too-costly` (8); `unexplained-phenomenon` (6); `open-question` (4); `belief-overturned` (2). Choose one in Step 1 and write it in the report.

## 3. Route table

| Motivation | Introduction route (see `introduction.md`) | Abstract | Cards |
|---|---|---|---|
| `failure` | A:V1/V2 → B: Diagnosis (symptom → mechanism) → Insight → C: one contribution per symptom | V2 | `mip-splatting.md` |
| `cost` | A:V2 → B: credit + flaw → rule out the obvious fix (quantified) → borrowed/new principle → C:V1 | V1 or V2 | `mip-nerf.md` |
| `capability-gap` | A:V2/V3 (concrete scenario) → B: gap + “The main reason is …” → goal as mechanism → C:V2 (technique + fix for its side effect) → new evaluation | V1 or Direct | `dreambooth.md` |
| `insight` | A:V2 (why it matters, vivid example) → B:V1 (dominant method + itemised cost) → C:V4 (insight → method → intuition) → mechanism-level contrast | V2 | `dpo.md` |
| `trend` | History (3 stages) → “Even so … still” → “we ask whether … almost entirely” → closest work with two checkable limits → C:V1 | Direct | — (plan in `introduction.md`) |
| `scaling` (L3) | Practical decision or open question → variables, response and budget → systematic sweep → the regularity found → held-out test / practical recipe | Question | — |
| `mechanism` (L5) | Phenomenon → candidate explanations and why they fall short → our mechanism (named) → distinguishing evidence: controlled experiments + tractable model | Background→puzzle | — |
| `resource` (L7) | Wanted capability + why data is missing → collection principle → contents (scale) + closest datasets → what it enables (findings) → release | Gap→Resource→Result→Release | paragraphs `--type L7` |
| `measurement` (L8) | Phenomenon/scene → sensor tradeoff → sensing principle → prototype results | Setting→Method→Result | paragraphs `--type L8` |
| `theory` (L6) | Question → known results → main result in words → comparison → implications/outline | Setting→Results in words | paragraphs `--type L6` |
| `re-examination` (L4) | Belief credited → question → our test → findings → stance | Setting→Test→Results→Stance | paragraphs `--type L4` |

“Direct” = abstract opens with `We present [Name], a [category] that [does what] from [input].` (13/55 award abstracts open with the method.) The default abstract for every route is Setting → Gap → Method → Result unless the table says otherwise (`abstract.md`).

## 4. Output of this step

```text
Route: L1 / failure (secondary: cost)
Reason: baseline X visibly fails when zooming out (Fig. 1), and we can name the mechanism.
Abstract: V2 (challenge → insight → contribution)
Introduction: A:V2 → Diagnosis → Insight → C (2 contributions) → evidence → contributions list
Cards: mip-splatting.md (primary), mip-nerf.md (rule-out paragraph)
```
