# Award-Paper Corpus Profile (55 papers)

Source: titles, abstracts and introductions of 55 CVPR/ICCV/NeurIPS best papers, runners-up and award candidates from 2021–2025. Five 2024 papers are held out as the evaluation set. Every sentence was labelled with its function, and style metrics were computed with `scripts/style_metrics.py` definitions. Machine-readable numbers are in `corpus/corpus_stats.json`.

Paper types: L1 method 23, L2 capability 6, L3 scaling 4, L4 re-examination 3, L5 mechanism 5, L6 theory 4, L7 resource 5, L8 measurement 5.

These are descriptive statistics of award papers, not causes of awards. Use them as ranges, not targets.

## Narrative
| Observation | Value |
|---|---|
| Introductions that credit specific prior work | 55/55 |
| Gap first appears | paragraph 2 (median) |
| Insight or goal stated | 43/55, typically just before the method |
| “key insight”-type formula | 4/55 |
| Idea handle (distinct from method name) | 27/55 |
| Concrete example (scene, failure case, striking number, analogy) | 36/55, paragraph 1–2 |
| Contrast with specific prior work | 32/55 sentences; closest work named explicitly 24/55; position ≈ 58% of the intro |
| Stance sentence | 28–35/55 in the introduction (end); 10/55 in the abstract |
| Contributions | bullets 16, prose 17, none 22 |
| Last paragraph | contributions 18, results 15, stance 7, outline 4 |
| Tension types | tradeoff 21, capability-missing 13, obvious-fix-too-costly 8, unexplained-phenomenon 6, open-question 4, belief-overturned 2 |
| Own limitations stated in abstract/intro | ≥ 7/55 (this skill omits them by author preference) |

## Abstract
| Observation | Value |
|---|---|
| Words / sentences | 174 / 7 (p10–p90: 132–219 words, 6–9 sentences) |
| First sentence | setting 32, method 13, gap 7 |
| Most common arc | Setting → Gap → Method → Result |
| Last sentence | result 21, release 18, secondary result 8, stance 5 |
| Insight sentence | 14/55 |

## Style (median; p90)
| Metric | Abstract | Introduction |
|---|---|---|
| Words | 174; 219 | 613; 898 |
| Prose paragraphs | 1 | 6; 8 |
| Mean sentence length | 24 | 23 |
| Short sentences (≤ 12 words) | 0%; 17% | 11%; 22% |
| Numbers | 1; 5.6 | 4; 14.6 |
| Connectors / 100 words | 0.6; 1.6 | 0.9; 1.4 |
| Colon/dash sentences | 11%; 29% | 10%; 23% (this skill: colons sparingly, no dashes) |
| Sentences ending in a participial clause | 8%; 25% | 8%; 20% |
| Hedges | 0; 1 | 1; 3.6 |
| Boosters | 0; 1 | 1; 3 |
| Evaluative words (outperform, efficient, first, …) | 1; 3 | 3; 7.6 (p10 = 1) |
| Sentences starting with We/Our | 29% | 18% |
| Sentence openers (intro) | subject 54%, prepositional/clause 21%, We/Our 17%, connector 13% |

## Form
| Observation | Value |
|---|---|
| Title | descriptive 25, “Name: description” 23, claim 4, question 2, metaphor 1 (put the idea’s handle in the title when there is one) |
| Figure 1 mentioned in the introduction | 29/55 |
| Mathematical expressions in the introduction | 9/55 |
| Separate outline paragraph | 4/55 |
