#!/usr/bin/env python3
"""Deterministic metrics for one run of an eval case (LaTeX project in <outputs>/paper/).

Usage:
    python3 evals/score_outputs.py <case-dir> <outputs-dir> [--reference FILE] [--json]

Metrics
  structure   : abstract/intro files written, template example sections removed, PDF compiled
  citations   : keys used, keys not in refs.bib, [TODO] count
  numbers     : numbers in abstract+intro absent from the prompt (possible fabrication; check derivations by hand)
  style       : check_draft.py errors/warnings, hedging verbs, words
  memorization: with --reference (original paper text), longest common word run and 8-gram overlap,
                excluding n-grams that already occur in the prompt
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
CHECK = SKILL / "scripts/check_draft.py"
sys.path.insert(0, str(SKILL / "scripts"))
from check_draft import strip_latex  # noqa: E402

NUM = re.compile(r"(?<![A-Za-z\d.])\d+(?:[.,]\d+)?")
IGNORE = {str(i) for i in range(0, 11)}
HEDGE = r"\b(suggests?|suggesting|may|might|could|likely|possibly|potentially)\b"


def nums(s):
    out = set()
    for n in NUM.findall(s):
        n = n.replace(",", "")
        out.add(n.rstrip("0").rstrip(".") if "." in n else n)
    return out


def words(s):
    return re.findall(r"[a-z0-9]+", s.lower())


def grams(w, n):
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def longest_run(a, b):
    """Longest run of consecutive words of `a` that also appears contiguously in `b`."""
    ref = " " + " ".join(b) + " "
    best = 0
    for i in range(len(a)):
        k = best + 1
        while i + k <= len(a) and (" " + " ".join(a[i:i + k]) + " ") in ref:
            best = k
            k += 1
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case_dir")
    ap.add_argument("outputs_dir")
    ap.add_argument("--reference")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    case, out = Path(a.case_dir), Path(a.outputs_dir)
    prompt = (case / "prompt.md").read_text(encoding="utf-8").split("---", 2)[-1]
    bib = (case / "files/refs.bib").read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    paper = out / "paper"
    m = {"case": case.name}
    abs_p, intro_p, main_p = paper / "sec/0_abstract.tex", paper / "sec/1_intro.tex", paper / "main.tex"
    m["has_abstract"] = abs_p.exists()
    m["has_intro"] = intro_p.exists()
    m["has_pdf"] = (paper / "main.pdf").exists()
    if main_p.exists():
        mt = main_p.read_text(encoding="utf-8")
        m["template_sections_removed"] = not re.search(r"^[^%]*\\input\{sec/(2_formatting|3_finalcopy)\}", mt, re.M)
        t = re.search(r"\\title\{(.+?)\}\s*\n", mt, re.S)
        m["title"] = t.group(1).strip()[:120] if t else None
    if not (m["has_abstract"] and m["has_intro"]):
        print(json.dumps(m, ensure_ascii=False, indent=2)); return
    raw = abs_p.read_text(encoding="utf-8") + "\n" + intro_p.read_text(encoding="utf-8")
    cited = set(k.strip() for grp in re.findall(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]*)\}", raw) for k in grp.split(","))
    m["cited_keys"] = len(cited)
    m["unknown_keys"] = sorted(cited - keys)
    m["todo_count"] = len(re.findall(r"TODO", raw))
    text_abs = strip_latex(abs_p.read_text(encoding="utf-8"))
    text_intro = strip_latex(intro_p.read_text(encoding="utf-8"))
    m["abstract_words"] = len(text_abs.split())
    m["intro_words"] = len(text_intro.split())
    m["unsupported_numbers"] = sorted(n for n in nums(text_abs + text_intro) - nums(prompt) if n not in IGNORE)
    m["hedges"] = len(re.findall(HEDGE, (text_abs + text_intro).lower()))
    r = subprocess.run([sys.executable, str(CHECK), str(abs_p), str(intro_p)], capture_output=True, text=True)
    tail = re.search(r"(\d+) error\(s\), (\d+) warning\(s\)", r.stdout)
    m["check_errors"], m["check_warnings"] = (int(tail.group(1)), int(tail.group(2))) if tail else (None, None)
    m["check_error_kinds"] = sorted(set(re.findall(r"ERROR line\s+\d+: ([^\n']+)", r.stdout)))
    if a.reference:
        ref = words(Path(a.reference).read_text(encoding="utf-8"))
        ours = words(text_abs + " " + text_intro)
        excl = grams(words(prompt), 8)
        g_ours, g_ref = grams(ours, 8), grams(ref, 8)
        m["ref_8gram_overlap"] = len((g_ours & g_ref) - excl)
        m["ref_longest_run"] = longest_run(ours, ref)
    print(json.dumps(m, ensure_ascii=False, indent=2) if a.json else "\n".join(f"{k:26s} {v}" for k, v in m.items()))


if __name__ == "__main__":
    main()
