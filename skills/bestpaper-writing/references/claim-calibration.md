# Claim Calibration: strong where supported, scoped where not

The goal is **persuasive accuracy**: present the contribution at the strongest level the evidence supports, and keep weaknesses for the Limitations section. Under-claiming is as harmful as over-claiming: hedges and disclaimers in the Abstract/Introduction make reviewers doubt the work.

## 1. Two kinds of statements

| Kind | Examples | How to write |
|---|---|---|
| **Ideas and design rationale** (the authors’ position) | key insight, why the design should work, what the paper argues | Assert: “Our key insight is that …”, “The main idea is …”, “We argue that …”. Never “we hypothesize” for the core idea. |
| **Empirical claims** (what the results show) | comparisons, gains, scaling behaviour, causal attributions | Use the strongest rung the evidence supports (table below), with numbers and the setting. |

## 2. Empirical wording ladder (choose the highest rung that holds)

| Evidence | Wording |
|---|---|
| Proof | We prove that … |
| Consistent results across benchmarks/settings | We show / demonstrate that …; X outperforms Y on A, B and C by … |
| Controlled experiment or ablation | Removing X reduces Y by Z; X is responsible for … ; we find that … |
| Single setting / correlation | We observe that …; This indicates … |
| Explanation not directly tested | likely because … (use sparingly; not for the core idea) |

## 3. Claim map (Step 3)

```text
| # | Claim (as it will appear) | Evidence (table/fig, numbers) | Strongest supported wording | Scope words needed |
| 1 | outperforms test-time optimization | Tab.1 41.2 vs 37.5 PSNR; Tab.2 0.12 vs 0.18 LPIPS | "outperforms … while running 40× faster" | none (consistent) |
| 2 | better than methods with privileged input | Tab.3 0.41 vs 0.33 (worse) | "better than methods with privileged input" is NOT supported → state the win without that input | "without privileged input" |
```

## 4. Numbers: headline, supporting, table-only

In 55 award papers, abstracts carry a median of 1 number (90% have ≤ 5–6) and introductions a median of 4 (90% have ≤ 14). A result sentence carries 0–2 numbers; most results are stated as claims. Assign every number one of three roles:

| Role | Where | Guide |
|---|---|---|
| Headline | abstract (and introduction) | the 1–2 results that carry the main claim; a scale number (dataset size, model size) if it defines the work |
| Supporting | introduction results paragraph | usually ≤ 8 numbers; more only when the paper is about scale, efficiency or a resource |
| Table-only | experiments | everything else, including ablation values and secondary metrics |

Write results as claims first: “X outperforms the strongest prior method while using a tenth of the compute”, then attach the headline number. `check_draft.py` warns when a section has more numbers than 90% of award papers.

## 5. Stance claims

A stance says what the work changes for the field. About half of award introductions have one (28–35 of 55 depending on how strictly it is counted, usually in the last paragraph); only 10/55 abstracts do. Write one when the results support a claim beyond “better on benchmark B”; otherwise end with the strongest result. It is an interpretation of the results, so it must follow from them, but it is written as a confident sentence:
- “We argue that [practice] is unnecessarily [complex], and show that [simpler alternative] suffices.”
- “Contrary to the common view that [belief], we find that [result].”
- “Challenging this norm, we posit that [claim], and show …”
- “This is a step toward [long-standing goal]: [what now works].”
Use “first” when the user’s related work supports it and the scope is precise.

## 6. Mixed results
- **Abstract/Introduction**: state the wins with their scope (“on the two dynamic benchmarks”, “among unified models”, “without ground-truth cameras”). Do not list losses. Do not claim wins that do not exist (“on all benchmarks”, “state-of-the-art” without a named comparison).
- **report.md → Limitations notes**: record every loss, failure case and cost so the authors can address them in the Limitations section.

## 7. Strong but safe phrasing

Award papers promote their work: an award introduction typically uses 3 evaluative words such as *outperforms*, *efficient*, *first*, *effective* (90% use at least one), each backed by evidence in the same sentence or paragraph. Do not write more modestly than the evidence allows.

- Put the scope inside the claim, once: “Trained once, X outperforms per-scene methods that require hours of fitting.”
- Prefer exact numbers to intensifiers; prefer “up to 50×” with the setting over “dramatically”.
- “First” only with a precise scope that the related work supports (“the first method that [specific capability] from [specific input]”); otherwise state the specific difference.
- Do not end paragraphs with “this does not establish …”, “remains to be evaluated”, “in the supplied evaluation”. If a caveat is essential, fold it into the claim as a scope word.
- Do not add defensive qualifiers about the protocol (“in our comparison”, “within the tested budgets”, “scores are computed on valid samples”, “under identical hyperparameters”); they belong to the experiments section.
