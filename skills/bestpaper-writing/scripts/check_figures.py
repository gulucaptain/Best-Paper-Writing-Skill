#!/usr/bin/env python3
"""Check the figures of a LaTeX paper against the award-paper ranges (references/figures.md).

Usage: python3 scripts/check_figures.py main.tex [--layout two|one]

Follows \\input / \\include, collects every figure (figure, figure*, strip + \\captionof) and table,
and reports:
  ERROR  figure without caption or label; label never referenced; dash in a caption
  WARN   caption length outside p10-p90 of award papers; first caption sentence too long;
         first reference in a later section than the figure; raster plot; absolute width;
         more floats than 90% of award papers
  NOTE   placeholders and figure plans left; no Figure 1 before the method; bold title style mixed
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# corpus ranges (data/figure_stats.json in the repository); kept inline so the skill folder is self-contained
RANGES = {
    "two": dict(cap=(10, 91), cap1=(32, 100), first=20, figs=(3, 9), tabs=(0, 5)),
    "one": dict(cap=(14, 102), cap1=(21, 153), first=21, figs=(3, 6), tabs=(0, 2)),
}
DASH = re.compile(r"—|---|\s–\s|\s--\s")
PLOTNAME = re.compile(r"(plot|curve|chart|graph|bar|loss|scaling|ablation|hist)", re.I)


def read_tree(path, seen=None, root=None):
    """Return list of (file, line_no, line) with \\input expanded in order (paths relative to the main file, as LaTeX does)."""
    seen = seen if seen is not None else set()
    root = root or os.path.dirname(path)
    out = []
    if path in seen or not os.path.exists(path):
        return out
    seen.add(path)
    for i, line in enumerate(open(path, encoding="utf-8", errors="ignore"), 1):
        code = re.sub(r"(?<!\\)%.*", "", line)
        m = re.search(r"\\(?:input|include)\{([^}]+)\}", code)
        if m:
            p = os.path.join(root, m.group(1))
            if not p.endswith(".tex"):
                p += ".tex"
            if not os.path.exists(p):
                p2 = os.path.join(os.path.dirname(path), m.group(1))
                p = p2 if p2.endswith(".tex") else p2 + ".tex"
            out.append((path, i, code[: m.start()]))
            out += read_tree(p, seen, root)
            out.append((path, i, code[m.end():]))
        else:
            out.append((path, i, code))
    return out


def braced(s, start):
    """Text of the {...} group starting at s[start] == '{'."""
    depth = 0
    for j in range(start, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1: j]
    return s[start + 1:]


def plain(tex):
    t = re.sub(r"\\(FigPlan|TODO)\{", "{", tex)
    t = re.sub(r"\$[^$]*\$", "x", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)
    t = re.sub(r"[{}~]", " ", t)
    return " ".join(t.split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("main")
    ap.add_argument("--layout", choices=["two", "one"])
    a = ap.parse_args()
    lines = read_tree(os.path.abspath(a.main))
    text = "\n".join(l for _, _, l in lines)
    # expand argument-free macros that wrap a float (\newcommand{\figQual}{\begin{figure}...})
    pos = 0
    while True:
        m = re.compile(r"\\newcommand\{(\\[A-Za-z]+)\}\{").search(text, pos)
        if not m:
            break
        body = braced(text, m.end() - 1)
        if "\\begin{figure" in body or "\\begin{table" in body:
            text = text[: m.start()] + text[m.end() + len(body) + 1:]
            text = re.sub(re.escape(m.group(1)) + r"(?![A-Za-z])", lambda _: body, text)
            pos = m.start()
        else:
            pos = m.end()
    layout = a.layout or ("one" if re.search(r"\\usepackage(\[[^\]]*\])?\{neurips", text) else "two")
    R = RANGES[layout]

    # positions of sections and references
    secs = [(m.start(), m.group(2)) for m in re.finditer(r"\\(section)\*?\{([^}]*)\}", text)]
    def section_at(pos):
        cur = "front"
        for p, name in secs:
            if p <= pos:
                cur = name
        return cur
    refs = {}
    for m in re.finditer(r"\\(?:c|C|auto|eq)?ref\{([^}]+)\}", text):
        for lab in m.group(1).split(","):
            refs.setdefault(lab.strip(), []).append(m.start())

    floats = []
    for m in re.finditer(r"\\begin\{(figure\*?|table\*?|strip)\}", text):
        env = m.group(1)
        end = text.find("\\end{%s}" % env, m.end())
        body = text[m.end(): end if end > 0 else None]
        kind = "table" if env.startswith("table") else "figure"
        cm = re.search(r"\\caption(?:of\{(?:figure|table)\})?\s*(\[[^\]]*\])?\s*\{", body)
        if env == "strip":
            cm = re.search(r"\\captionof\{(figure|table)\}\s*\{", body)
            if cm and cm.group(1) == "table":
                kind = "table"
            if not cm:
                continue
        cap = braced(body, cm.end() - 1) if cm else None
        labs = re.findall(r"\\label\{([^}]+)\}", body)
        floats.append(dict(env=env, kind=kind, pos=m.start(), caption=cap, labels=labs, body=body))
    # numbered floats defined inside macros (\newcommand{\figX}{\begin{figure}...}) are expanded where used
    figs = [f for f in floats if f["kind"] == "figure"]
    tabs = [f for f in floats if f["kind"] == "table"]

    issues = []
    def add(level, msg, f=None):
        tag = (f["labels"][0] if f and f["labels"] else (f and f["env"]) or "")
        issues.append((level, tag, msg))

    bold = []
    method_pos = next((p for p, n in secs if re.search(r"method|approach|^[A-Z0-9]+:", n, re.I) and p > 0 and n.lower() != "introduction"), None)
    for k, f in enumerate(figs):
        if f["caption"] is None:
            add("ERROR", "figure without caption", f); continue
        if not f["labels"]:
            add("ERROR", "figure without \\label", f)
        cap = f["caption"]
        cap_final = cap
        for t in re.finditer(r"\\(TODO|FigPlan)\{", cap):
            cap_final = cap_final.replace("\\" + t.group(1) + "{" + braced(cap, t.end() - 1) + "}", "")
        words = plain(cap_final).split()
        first = re.split(r"(?<=[.!?])\s+", plain(cap_final))[0].split()
        lo, hi = R["cap1"] if k == 0 else R["cap"]
        if "Figure placeholder" in f["body"] or "\\figplaceholder" in f["body"] or "\\bpplacebox" in f["body"] or "\\FigPlan" in cap:
            add("NOTE", "placeholder or figure plan still in this figure", f)
        elif not lo <= len(words) <= hi:
            add("WARN", f"caption has {len(words)} words; award papers: {lo}-{hi} (p10-p90){' for Figure 1' if k == 0 else ''}", f)
        if len(first) > R["first"]:
            add("WARN", f"first caption sentence has {len(first)} words (p90 {R['first']}); open with the takeaway", f)
        if DASH.search(cap):
            add("ERROR", "dash in caption (author preference: no dashes)", f)
        bold.append(bool(re.match(r"\s*\\textbf\{", cap)))
        for lab in f["labels"]:
            if lab not in refs:
                add("ERROR", "figure is never referenced in the text", f)
            elif f["env"] != "strip" and k > 0:
                s_fig, s_ref = section_at(f["pos"]), section_at(min(refs[lab]))
                if s_fig != s_ref and min(refs[lab]) > f["pos"]:
                    add("WARN", f"first reference is in section '{s_ref}', the figure sits in '{s_fig}'", f)
        for g in re.finditer(r"\\includegraphics(\[[^\]]*\])?\{([^}]+)\}", f["body"]):
            opts, name = g.group(1) or "", g.group(2)
            if re.search(r"\.(png|jpe?g)$", name, re.I) and PLOTNAME.search(os.path.basename(name)):
                add("WARN", f"'{name}' looks like a plot saved as raster; export vector PDF", f)
            w = re.search(r"width\s*=\s*([\d.]+)\s*(cm|mm|in|pt)", opts)
            if w:
                add("WARN", f"absolute width {w.group(1)}{w.group(2)}; use a fraction of \\linewidth", f)
    if figs and figs[0]["env"] != "strip" and method_pos is not None and figs[0]["pos"] > method_pos:
        add("NOTE", "no figure before the method section; award papers put Figure 1 on page 1 (two-column) or 2 (one-column)")
    if bold and 0 < sum(bold) < len(bold):
        add("NOTE", f"{sum(bold)} of {len(bold)} captions start with a bold title; use one style throughout")
    flo, fhi = R["figs"]; tlo, thi = R["tabs"]
    if len(figs) > fhi:
        add("WARN", f"{len(figs)} figures in the paper; 90% of award papers ({layout}-column) have at most {fhi}")
    if len(tabs) > thi:
        add("NOTE", f"{len(tabs)} tables; 90% of award papers ({layout}-column) have at most {thi}")
    intro = re.search(r"\\section\*?\{Introduction\}(.*?)(\\section)", text, re.S)
    if figs and figs[0]["labels"] and intro and not any(intro.start(1) <= p <= intro.end(1) for p in refs.get(figs[0]["labels"][0], [])):
        add("NOTE", "the introduction does not reference Figure 1 (29 of 55 award papers do)")

    print(f"== {a.main}  [{layout}-column]  {len(figs)} figures, {len(tabs)} tables")
    order = {"ERROR": 0, "WARN": 1, "NOTE": 2}
    for lvl, tag, msg in sorted(issues, key=lambda x: order[x[0]]):
        print(f"{lvl:5s} {tag:22s} {msg}")
    n = {l: sum(1 for i in issues if i[0] == l) for l in order}
    print(f"\n{n['ERROR']} error(s), {n['WARN']} warning(s), {n['NOTE']} note(s)")
    sys.exit(1 if n["ERROR"] else 0)


if __name__ == "__main__":
    main()
