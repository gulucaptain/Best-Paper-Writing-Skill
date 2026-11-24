# Card: Mission: Impossible Language Models (ACL 2024 Best Paper)

- **Paper type**: L4 re-examination / L5 mechanism & analysis
- **Motivation type**: `re-examination` — tests a widely quoted theoretical assertion with controlled synthetic experiments
- **Route**: Intro: Named claim credited verbatim → Evidence gap → Controlled design (continuum) → Falsifiable hypothesis framing → Core finding + Stance

## One-line claim
By constructing a continuum of synthetic "impossible" languages and tracking GPT-2 learning curves throughout training, we show that LLMs learn impossible languages markedly worse than natural English — refuting claims that LLMs cannot distinguish possible from impossible human languages.

## Move sequence (Introduction)

| # | Move | What the paper does |
|---|---|---|
| 1 | Name the influential claim | Specific authors (Chomsky et al., Moro et al., Bolhuis et al.) assert LLMs treat possible and impossible languages equally |
| 2 | Stakes if true | Would undermine LLMs as tools for linguistic methodology and robust language capability |
| 3 | Quote exact strong phrasing | Three crisp verbatim snippets showing how absolute the claim is |
| 4 | Evidence gap | Only one experimental paper cited; no agreed formal boundary of "impossible" |
| 5 | Controlled operationalization | Instead of asserting one definition, build an "impossibility continuum" (Fig. 1) |
| 6 | Explicit falsifiability logic | "If LLMs learn these as well as natural language, claim is supported; if not, it calls those assertions into question" |
| 7 | Headline finding + constructive stance | GPT-2 struggles on impossible languages; opens an empirical paradigm for cognitive/typological probing |

## Sentences worth studying

> Chomsky and others have very directly claimed that large language models (LLMs) are equally capable of learning languages that are possible and impossible for humans to learn. However, there is very little published experimental evidence to support such a claim.
> — Impossible Language Models · ACL 2024 · p.1

> One might expect such strong claims to be supported by extensive formal analysis and/or experimental evidence. However, as far as we are aware, this is not the case.
> — Impossible Language Models · ACL 2024 · p.1

> Arguably, the central challenge for such work is the fact that there is no agreed-upon way of distinguishing these two groups. We do not feel positioned ourselves to assert such a definition, so we instead offer some examples of impossible languages on a continuum of intuitive complexity (Figure 1).
> — Impossible Language Models · ACL 2024 · p.1

> Our core finding is that GPT-2 struggles to learn impossible languages when compared to English as a control, challenging the core claim.
> — Impossible Language Models · ACL 2024 · p.1

## Why it works
1. **Steel-mans the opponent**: quotes exact assertions rather than attacking a strawman, making the subsequent refutation unmistakably fair and sharp.
2. **Pre-empts the hardest methodological objection** ("how do you define impossible?") right in the intro by replacing a binary definition with a continuum.
3. **States the decision rule upfront**: explicitly writes the if/else falsifiability test before showing results, building instant scientific trust.
4. **Constructive closing stance**: turns a refutation paper into a reusable methodology ("opens up a productive line of inquiry").

## Transferable skeleton
```text
[Named works] make a broad claim that [Claim]. If true, this has major consequences for [field/methodology].
One might expect such strong claims to rest on extensive experimental evidence. However, [concise evidence gap].
Here, we provide controlled experimental evidence to test [Claim]. Because [central definitional challenge], we construct [continuum/suite of controlled tests] (Figure 1).
If [models behave as claimed], then [Claim] is supported; conversely, if [opposite outcome], those assertions are called into question.
Our core finding is that [concrete result vs. control], challenging [Claim] and establishing a framework for [broader inquiry].
```
