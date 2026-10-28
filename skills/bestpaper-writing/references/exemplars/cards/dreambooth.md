# Card: DreamBooth (CVPR 2023)

- **Paper type**: L2 new task / new capability
- **Motivation type**: `capability-gap` — strong models cannot do something users want
- **Route**: Intro A:V2 (application-first, vivid) → B: capability gap + its cause → C:V2 (main technique + a second technique for a remaining problem) → new task, dataset and protocol · Abstract: background → gap → contribution

## One-line claim
Fine-tuning a text-to-image model on 3–5 images with a rare-token identifier plus a class-specific prior-preservation loss lets it render a specific subject in new contexts while preserving its identity — a new task the paper also defines a benchmark for.

## Move sequence (Introduction)

| # | Move | What the paper does |
|---|---|---|
| 1 | Hook | Three concrete scenarios (your dog travelling, your bag in Paris, your parrot in a storybook) |
| 2 | Why it is hard | “synthesizing instances of specific subjects … in new contexts” |
| 3 | Credit the field | large text-to-image models; strong semantic prior |
| 4 | Capability gap | cannot mimic a given subject |
| 5 | Cause of the gap | output domain expressiveness; text cannot pin down appearance |
| 6 | Goal stated as a capability | “expand the language-vision dictionary of the model” |
| 7 | Analogy | “magic photo booth” |
| 8 | Technique 1 | rare-token identifier + class name |
| 9 | Remaining problem → technique 2 | language drift → prior-preservation loss |
| 10 | Scope of applications | recontextualization, property modification, art renditions |
| 11 | New task claim + evaluation | first technique for the task; new dataset and protocol |

## Sentences worth studying

> While the synthesis capabilities of these models are unprecedented, they lack the ability to mimic the appearance of subjects in a given reference set, and synthesize novel renditions of the same subjects in different contexts.
> — DreamBooth · CVPR 2023 · p.1

> The main reason is that the expressiveness of their output domain is limited; even the most detailed textual description of an object may yield instances with different appearances.
> — DreamBooth · CVPR 2023 · p.1

> Our goal is to expand the language-vision dictionary of the model such that it binds new words with specific subjects the user wants to generate.
> — DreamBooth · CVPR 2023 · p.2

> In order to prevent language drift that causes the model to associate the class name (e.g., “dog”) with the specific instance, we propose an autogenous, class-specific prior preservation loss, which leverages the semantic prior on the class that is embedded in the model, and encourages it to generate diverse instances of the same class as our subject.
> — DreamBooth · CVPR 2023 · p.2

## Why it works
1. **The gap comes with a cause** (“The main reason is …”), turning a missing feature into a technical problem.
2. **The goal is phrased as a mechanism-level metaphor** (“expand the dictionary … binds new words”), which also previews the method.
3. **Technique 2 is introduced through the problem technique 1 creates** (language drift), so it is not a bolt-on.
4. **A new task is backed by a new evaluation** (dataset + protocol), which is what reviewers expect for capability claims.

## Caution
The rhetorical-question hook works for a highly visual, user-facing capability. For most method papers, open with the task instead.

## Transferable skeleton
```text
[Hook: 1–3 concrete user scenarios]. [Why this is hard in one sentence].
Recent [models] have shown [credit], thanks to [strength]. However, they lack the ability to [capability].
The main reason is that [technical cause].
In this work, our goal is to [capability phrased as a mechanism]. Given [minimal input], we [technique 1],
which [how it uses existing strength]. However, [problem created by technique 1]. To prevent this, we
propose [technique 2], which [mechanism].
We apply [Name] to [applications]. To evaluate this new task, we construct [dataset] and propose
[protocol] measuring [criteria].
```
