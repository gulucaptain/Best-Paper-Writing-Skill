# Card: CURE (ACL 2026 Outstanding Paper)

- **Paper type**: L1 method improvement / L2 test-time capability
- **Motivation type**: `failure` + `capability-gap` — existing critique-guided RLVR breaks at test time because it depends on external teachers or ground-truth signals
- **Route**: Intro A:V2 (test-time scaling taxonomy: parallel vs. sequential) → B:V1 (both paradigms fail autonomous iterative refinement; critique methods require unavailable test-time signals) → C:V1 (unified single-policy RLVR over 3 atomic skills + anchoring-bias fix)

## One-line claim
By jointly optimizing a single policy via RLVR for solving, self-critiquing, and hint-guided re-exploration while discarding initial incorrect trajectories to avoid anchoring bias, CURE removes test-time dependencies on external teachers or ground truth and unlocks autonomous iterative self-improvement.

## Move sequence (Introduction)

| # | Move | What the paper does |
|---|---|---|
| 1 | Field shift + clean 2-way taxonomy | Inference-time scaling splits into (1) Parallel Scaling and (2) Sequential Scaling (RLVR) |
| 2 | Dual gap across both branches | Parallel merely samples independently; sequential struggles with reliable self-verification because it is never explicitly trained |
| 3 | Closest prior fix + its fatal test-time flaw | Critique-guided methods rely on external teachers or ground-truth triggers — both unavailable at test time |
| 4 | Consequence | Breaks the autonomous solve–verify–re-explore loop |
| 5 | Unified method (3 atomic capabilities) | CURE jointly trains one policy for (1) Solving, (2) Critiquing (verification + hints), and (3) Critique-Guided Re-Exploration |
| 6 | Key subtle mechanism | Discards initial wrong solution and passes only strategic hints to prevent anchoring bias |
| 7 | Calibrated results | Competitive single-turn accuracy + strong iterative inference-time scaling on math and code |

## Sentences worth studying

> While Reinforcement Learning with Verifiable Rewards (RLVR) has become a key engine for this transition, standard approaches often fail to equip models with the autonomous improvement capabilities required for test-time scaling.
> — CURE · ACL 2026 · p.1

> Existing critique-guided methods attempt to mitigate this by leveraging external feedback or ground-truth signals; however, these dependencies are unavailable at test time, fundamentally limiting the model’s capacity for continuous self-improvement.
> — CURE · ACL 2026 · p.1

> Uniquely, CURE facilitates re-exploration by generating strategic hints while discarding initial incorrect solutions to mitigate anchoring bias.
> — CURE · ACL 2026 · p.1

> Empirical results across diverse mathematical reasoning and code generation benchmarks demonstrate that CURE not only maintains competitive single-turn performance but, more importantly, unlocks effective inference-time scaling, enabling the model to significantly boost accuracy through iterative self-improvement.
> — CURE · ACL 2026 · p.1

## Why it works
1. **Clean two-branch setup**: structuring existing work as Parallel vs. Sequential Scaling lets the paper diagnose *both* lines in two crisp sentences ("On one hand... On the other hand...").
2. **Pinpoints an unmistakable deployment flaw**: external teachers and ground-truth labels literally do not exist at test time — a checkable, indisputable gap.
3. **Highlights one surgical insight**: discarding the failed trajectory and passing only strategic hints to avoid anchoring bias makes the method memorable beyond "joint RL training."
4. **Honest calibration**: claims "maintains competitive single-turn performance" while focusing the win on iterative test-time scaling.

## Transferable skeleton
```text
[Field] is shifting toward [paradigm], typically via (1) [Branch A] or (2) [Branch B].
However, both fall short of [desired capability]: [Branch A] merely [limit A], while [Branch B] struggles with [limit B] because [root cause].
Recent [closest approach] attempts to address this using [external dependency], which is unavailable at [deployment/test time] and breaks [desired loop].
We propose [Name], a unified framework that jointly optimizes a single policy for [Skill 1], [Skill 2], and [Skill 3], while [key surgical design] to mitigate [failure mode].
Across [benchmark domains], [Name] maintains competitive [baseline regime] while unlocking substantial gains in [target regime].
```
