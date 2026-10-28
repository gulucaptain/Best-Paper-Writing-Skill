# Evaluation cases: held-out test set

The style rules were fitted on 55 award papers. The test set is a separate group of 5 award papers from 2024 that were removed from the exemplar bank and never used to fit any rule.

| Case | Original paper (hidden at test time) | Award | Type |
|---|---|---|---|
| `image-space-motion-prior` | Generative Image Dynamics | CVPR 2024 Best Paper | L2 new capability |
| `next-scale-autoregressive-images` | Visual Autoregressive Modeling (VAR) | NeurIPS 2024 Best Paper | L1 paradigm |
| `taylor-mode-operator-estimator` | Stochastic Taylor Derivative Estimator | NeurIPS 2024 Best Paper | L1 cost |
| `participatory-alignment-dataset` | The PRISM Alignment Dataset | NeurIPS 2024 D&B Best Paper | L7 dataset |
| `guidance-with-weaker-model` | Guiding a Diffusion Model with a Bad Version of Itself | NeurIPS 2024 Best Paper Runner-up | L1 insight |

Awards are taken from the CVPR 2024 awards page and the NeurIPS 2024 official blog.

> Note: the original abstracts and introductions used for scoring are not included here for copyright reasons, and some helper tools of the development repository (such as the blind-pack generator) are not shipped. The case prompts, graders, rubric and `score_outputs.py` are.

## Case layout

Each case has `prompt.md` (the task and the author-side facts, with numbers taken from the paper and method names anonymised), `files/refs.bib` (real references), `case.yaml`, and `graders/` with 13 criteria: 7 general (template use, compilation, no invented citations, no invented numbers, no limitations in the abstract and introduction, no process traces, confident statement of the key idea), 2 on style (number budget, stance sentence) and 4 on case-specific content.

## Scoring

1. **graders**: one judgment per criterion.
2. **`score_outputs.py`**: structure, citations, suspicious numbers, `check_draft` errors, count of speculative wording, and overlap with the original (8-gram overlap and longest shared word run, to detect memorised text; n-grams already present in the input are ignored).
   ```bash
   python3 evals/score_outputs.py evals/<case> <run>/outputs --reference <original-text>.txt
   ```
3. **`rubric.md`**: blind comparison of each configuration's output together with the original paper's abstract and introduction, all anonymised, answering how far a draft is from the award paper.

## Anti-leak rules

- The 5 test papers are excluded from the exemplar bank.
- No rule file contains their numbers or sentences.
