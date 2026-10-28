# Intake Form

Students can fill the same fields in `assets/intake_form.html` (Chinese, works offline, exports JSON); `scripts/intake_to_brief.py` turns the JSON into this structure.

Fill this from what the user provides. Ask for missing **required** fields in one compact message; never invent them.

## Required

| # | Field | What a good answer looks like | Why it matters |
|---|---|---|---|
| R1 | **Task** | Input → output, and 1–2 concrete applications | Opening paragraph |
| R2 | **Dominant prior approach** | How the strongest existing methods work (mechanism, not names only) | You must describe what you later criticise |
| R3 | **Failure / gap** | The observable limitation **and its technical reason**, plus the condition under which it appears | “Technical challenge = limitation + reason” |
| R4 | **Closest work (1–3)** | Names and the *specific* difference (input, assumption, mechanism, cost) | Positioning; reviewers will know these papers |
| R5 | **Key insight** | One sentence: why your approach can work | Introduction’s pivot sentence |
| R6 | **Method** | Name + one-sentence mechanism for each core component | Contribution sentences |
| R7 | **Evidence** | For each result: dataset/benchmark, baseline, metric, number, table/figure id | Claim map |

## Strongly recommended (these make the writing memorable)

| # | Field | Notes |
|---|---|---|
| S0 | **Handle** | A term, contrast or image that names the idea itself — not the method’s name (“next-brick prediction”, “pick & solve”). About half of award papers have one; if none, the skill may propose one |
| S0b | **Concrete example** | One instance a reader can picture: an input that breaks prior work, a user request, a striking number |
| S0c | **The tension** | What makes the problem hard or surprising: two goals in conflict, an obvious fix that fails, a belief the results contradict |
| S0d | **What it changes** | What should readers believe after this paper that they did not before? (“X is unnecessary”, “the common explanation is wrong”, “Y now works at scale”) |
| S1 | **Limitations / failure cases** | Kept out of the Abstract/Introduction; used for scoping claims and listed in report.md for the Limitations section |
| S2 | **Figure 1 plan** | What the teaser shows (failure of prior work vs. ours? overview?) |
| S3 | **Secondary findings** | Ablation insights, surprising results, transfer to other tasks |
| S4 | **Target venue and page limit** | Affects length and tone |
| S6 | **Benefits** | Efficiency (memory, speed, data), integration with existing pipelines or renderers, supported inputs, new applications. Award abstracts often win on these (e.g., “lowers memory”, “integrates with a physically based renderer”, “optimised from textures or multi-view images”) |
| S7 | **Trend or inspiration** | The popular work or line of work this builds on; enables a “building on X, we rethink Y” opening |
| S5 | **Type hints** | Is this a fix of a known failure, a cheaper way to do something, a new capability, a theory-driven simplification, or the next step of a trend? |

## Follow-up rules
- If R3 has a limitation but no reason, ask: *“What in the existing method causes this? What does it assume or compute that breaks?”*
- If R5 is a description of the method, ask: *“What property of the problem makes this design work?”*
- If R7 lacks numbers, write claims as `[TODO: number]` and keep wording at the “suggest” level.
- If the user insists on a claim the evidence does not support, draft it at the supported strength and flag the gap in the report.
- If S0–S0c are missing, do not stop: derive the tension from R2–R3 and propose a handle in report.md.

## Template for the user (copy and fill)

```markdown
**Task**: Given [input], we [estimate/generate/…] [output]. Applications: [A], [B].
**Prior approach**: Most methods [mechanism]. They assume [assumption].
**Failure + reason**: When [condition], they [observable failure], because [technical reason].
**Closest work**: [X] — differs from us in [specific aspect]; [Y] — …
**Key insight**: [property of the problem] allows [our design].
**Method**: [Name]: (1) [component] — [mechanism]; (2) [component] — [mechanism].
**Evidence**: On [benchmark], [metric] [ours] vs [baseline] = [numbers] (Table [k]); ablation: [finding] (Table [m]).
**Handle / example / tension**: [term]; [one concrete example]; [what makes it hard or surprising].
**What it changes**: [the belief or practice this work changes].
**Limitations (for the Limitations section)**: Fails when [...]; costs [...].
**Figure 1**: [what it shows].
**Venue / length**: [CVPR, 8 pages].
```
