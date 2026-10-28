# Abstract

Versions 1–3 are adapted from the base skill (see `NOTICE.md`). The statistics and the default arc come from the sentence-level annotation of 55 award papers (`corpus/corpus_stats.json`, `corpus-profile.md`).

## 1. Before writing
1. What problem do we solve, and why is there no established solution?
2. What is our contribution, and why does it work in essence?
3. What is the main evidence (benchmark, baseline, number)?

## 2. What award abstracts actually do (55 papers)

| Fact | Value |
|---|---|
| Length | median 174 words (p10–p90: 132–219); median 7 sentences (6–9); one paragraph |
| First sentence | setting/background 32, our method directly 13, the gap 7 |
| Most common arc | **Setting → Gap → Method → Result**, with variants that drop the setting or open with the method |
| Last sentence | a result 21, release of code/data 18, a secondary result 8, a stance 5 |
| Insight sentence | 14/55 (when the method follows from one observation) |
| Stance sentence | 10/55 |
| Numbers | median 1; 90% have ≤ 5–6 |
| Connectors (however/thus/…) | median 0.6 per 100 words, 90% ≤ 1.6 — about one per abstract |

So the default abstract is short, concrete and plain: one gap, one method, one or two results. Insight and stance sentences are added only when the paper has them.

## 3. Versions

### Default — Setting → Gap → Method → Result *(about half of award abstracts)*
1. Setting: what works today, concretely (one sentence).
2. Gap: what fails or is missing, under which condition — and, in the same or the next sentence, why.
3. Method: name it with its category and the one idea that answers the gap (“We present X, a … that …”). Optional: one sentence of mechanism or the insight it rests on.
4. Benefit/evidence: one or two results with benchmark and baseline.
5. Optional last sentence: a secondary capability, a stance, or the release of code/data.

### Direct — Method → (Gap) → Method → Result *(~1/4; `trend`, `capability-gap`, resources)*
1. `We present [Name], a [category] that [does what] from [input].` 2. Prior methods [restriction] → consequence. 3. [Name] instead [key design], allowing [capabilities matching the restriction]. 4. Evidence. 5. Optional transfer/secondary result or release.

### Insight-led — Setting → Gap → Insight → Method → Result *(`insight`, `failure` with a clear root cause)*
As the default, with one sentence that states the observation about the problem from which the method follows. Write the observation itself (“The highest frequency a scene can contain is bounded by the sampling rate of its views.”), not a formula announcing it (“Our key insight is …”).

### Multiple contributions
Each contribution with its advantage in the same sentence; then evidence.

### By paper type
| Type | Typical arc (coarse) |
|---|---|
| L1 method | Setting → Gap → Method → Result |
| L2 capability | Method → Result (Direct), or Setting → Method → Result |
| L3 scaling | Setting/Question → Method (the study) → Results (the regularity) → Method (recipe) → Result |
| L4 re-examination | Setting → Method (our test) → several Results → Stance |
| L5 mechanism | Setting → Gap/puzzle → Method → Insight (explanation) → Result |
| L6 theory | Setting → Setting of the problem → theorem-level results in words → implication |
| L7 resource | Gap → Resource (scale number) → what it enables → baseline/benchmark result → release |
| L8 measurement | Setting → Method (sensing principle) → Mechanism → Result (prototype) |

## 4. Rules
- About 130–220 words in 6–9 sentences averaging ~20–25 words; one message per sentence, with its reason or evidence inside the sentence. One short sentence for the idea is welcome. Do not split a result from its number or a design from its benefit.
- Each element appears once: do not restate the gap or the benefit in a second sentence.
- Numbers: the headline result(s) and, if essential, one number that defines the scale. No ablation numbers or implementation details.
- At most one logical connector (however, thus, …) in most abstracts; sentence order carries the logic. No dashes (author preference); a colon is fine where it introduces the idea or a list. No sentence ends with “, making …” or a similar participial restatement.
- Every adjective about the method is made concrete in the same sentence.
- Results name the benchmark/baseline or state the scope; wording follows the claim map.
- Include at least one evaluative claim backed by evidence (“outperforms X”, “the first … that …”, “20× faster”); 37 of 55 award abstracts use such a word, and the rest state a comparison in numbers.
- End with the strongest evidence, a concrete secondary result, a stance supported by the results, or the release of code/data — not with generic impact (“opens new avenues”).
- No limitations, costs or losses in the abstract; scope mixed results to where the method wins.

## 5. Checklist
- [ ] A reader can name task, gap, method and evidence after one pass.
- [ ] Gap sentence and method sentence match one-to-one.
- [ ] Same claims and strength as the introduction.
- [ ] No hedging on the core idea; no disclaimers; no “key insight” formula.
- [ ] At least one evaluative claim backed by evidence (outperforms, first, faster, …).
- [ ] `python3 scripts/check_draft.py` shows no ERROR and no WARN for connectors, numbers or participial clauses (or each one is justified).
