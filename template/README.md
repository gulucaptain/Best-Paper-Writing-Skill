# LaTeX templates

| Folder | Venue | Source |
|---|---|---|
| `CVPR2027/` | CVPR 2027 (also used by ICCV / 3DV) | Official author kit, [cvpr-org/author-kit](https://github.com/cvpr-org/author-kit) @ `a236934` |

The files are an unmodified copy of the official kit. To use one with the `bestpaper-writing` skill, copy the folder to your paper directory (never edit the template in place) and follow `skills/bestpaper-writing/references/latex-output.md`:

```bash
cp -r template/CVPR2027 my-paper && cd my-paper
# write sec/0_abstract.tex, sec/1_intro.tex, sec/3_method.tex, sec/4_experiments.tex
latexmk -pdf main.tex
```

Check the venue's website for a newer kit before submitting.
