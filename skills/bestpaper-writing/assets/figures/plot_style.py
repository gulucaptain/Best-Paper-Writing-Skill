"""Plot helpers that keep every chart of a paper consistent (references/figures.md §5).

    import plot_style as ps
    ps.use()
    colors = ps.method_colors(["Ours", "VGGT", "MegaSaM"], ours="Ours")
    fig, ax = ps.figure("column")              # or "full", or ("full", 0.35)
    for m in methods: ax.plot(x, y[m], **ps.line_kw(m, colors, ours="Ours"))
    ps.label_lines(ax)                         # direct labels at the curve ends
    fig.savefig("fig/scaling.pdf")

Only plot numbers the authors have measured. Never fill a plot with invented values.
"""
import os
import matplotlib as mpl
import matplotlib.pyplot as plt

STYLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bestpaper.mplstyle")
OURS = "#0072B2"                     # same blue as bpOurs in figures_preamble.tex
BASELINES = ["#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9", "#7F7F7F", "#000000"]
WIDTH = {"column": 3.25, "full": 6.875}   # inches, CVPR/ICCV; NeurIPS text width is 5.5


def use():
    plt.style.use(STYLE)


def figure(width="column", aspect=0.62, ncols=1, nrows=1, **kw):
    """Figure at print size. width: 'column', 'full', a number in inches, or (name, aspect)."""
    if isinstance(width, tuple):
        width, aspect = width
    w = WIDTH.get(width, width)
    return plt.subplots(nrows, ncols, figsize=(w, w * aspect), **kw)


def method_colors(methods, ours="Ours"):
    """Fixed colour per method for the whole paper: ours blue, baselines in a stable order."""
    out, i = {}, 0
    for m in methods:
        if m == ours:
            out[m] = OURS
        else:
            out[m] = BASELINES[i % len(BASELINES)]
            i += 1
    return out


def line_kw(method, colors, ours="Ours"):
    """Ours drawn on top, thicker and saturated; baselines thinner and slightly transparent."""
    if method == ours:
        return dict(color=colors[method], lw=1.8, zorder=5, label=method)
    return dict(color=colors[method], lw=1.0, alpha=0.85, zorder=2, label=method)


def label_lines(ax, offset=3, fontsize=6):
    """Write each line's label at its right end instead of a legend box."""
    for line in ax.get_lines():
        lab = line.get_label()
        if lab.startswith("_"):
            continue
        x, y = line.get_xdata(), line.get_ydata()
        if len(x) == 0:
            continue
        ax.annotate(lab, (x[-1], y[-1]), xytext=(offset, 0), textcoords="offset points",
                    color=line.get_color(), fontsize=fontsize, va="center",
                    fontweight="bold" if line.get_linewidth() > 1.5 else "normal")
