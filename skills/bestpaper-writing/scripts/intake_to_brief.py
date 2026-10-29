#!/usr/bin/env python3
"""Convert an intake JSON (exported from assets/intake_form.html) into a writing brief.

Usage:
  python3 scripts/intake_to_brief.py intake.json [--out brief.md] [--bib refs.bib]

Prints (or writes) a Markdown brief organised like references/intake-form.md, followed by
the list of missing fields. Exit code 2 if a required field is missing, so the agent knows
to ask the user before drafting. With --bib, the pasted BibTeX is written to that file.
"""
import argparse, json, sys
from pathlib import Path

# Form v1.2: five required fields; the recommended ones are asked once if missing (never invented).
REQUIRED = [("meta", "one_line", "One-line claim"), ("required", "task", "Task and applications"),
            ("required", "failure", "Failure condition (observable)"),
            ("required", "method", "Method components"), ("required", "results", "Headline results")]
RECOMMENDED = [("required", "prior_best", "Dominant prior approach (mechanism)"),
               ("required", "failure_reason", "Technical reason for the failure"),
               ("required", "insight", "Key insight about the problem"),
               ("required", "closest", "Closest work and difference"),
               ("enhancers", "example", "Concrete example / scene"),
               ("enhancers", "benefits_efficiency", "Efficiency advantages"),
               ("enhancers", "surprising", "Surprising or counter-intuitive aspect"),
               ("enhancers", "handle", "Team's name for the idea (handle)")]
ENHANCERS = [("applications", "Further advantages and applications"), ("benefits_integration", "Integration with existing pipelines"),
             ("benefits_inputs", "Supported inputs / usage modes"), ("tension", "Tension type"),
             ("trend", "Trend or inspiration (for the opening)"), ("stance", "Stance: what readers should believe afterwards")]
SUPPORT = [("figure1", "Figure 1"), ("data_scale", "Data / model scale"), ("secondary", "Secondary results and ablations"),
           ("release", "Release"), ("limitations", "Limitations (for the Limitations section only)"),
           ("materials", "Other materials"), ("notes", "Other requirements")]


SELECT_KEYS = ("diff_type", "dir")
EMPTY = ("", "不确定", "让 skill 判断")


def present(v):
    if isinstance(v, list):
        return any(isinstance(it, dict) and any(str(x).strip() for k, x in it.items() if k not in SELECT_KEYS) for it in v) \
            or any(isinstance(it, str) and it.strip() for it in v)
    return bool(v) and str(v).strip() not in EMPTY


def fmt_list(key, items):
    lines = []
    for i, it in enumerate(items, 1):
        if key == "method":
            lines.append(f"  {i}. {it.get('name', '')}: {it.get('mechanism', '')}")
        elif key == "results":
            lines.append(f"  {i}. {it.get('benchmark', '')} | metric {it.get('metric', '')} {it.get('dir', '')} | baseline {it.get('baseline', '')} | ours {it.get('ours', '') or '[TODO: number]'} | {it.get('where', '')}")
        elif key == "closest":
            key_ = f" [{it['bibkey']}]" if it.get("bibkey") else ""
            lines.append(f"  {i}. {it.get('name', '')}{key_}: {it.get('diff_type', '')}; {it.get('difference', '')}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--out")
    ap.add_argument("--bib")
    a = ap.parse_args()
    d = json.loads(Path(a.json).read_text(encoding="utf-8"))
    if d.get("schema") not in (None, "bestpaper-intake/v1"):
        print(f"warning: unknown schema {d.get('schema')}", file=sys.stderr)
    meta, req, enh, sup = (d.get(k, {}) for k in ("meta", "required", "enhancers", "support"))
    out = [f"# Writing brief: {meta.get('working_name') or '[unnamed]'}", ""]
    secs = meta.get("sections")
    ptype = meta.get("paper_type")
    out += [f"- **Venue / length**: {meta.get('venue') or '-'}",
            f"- **Sections requested**: {', '.join(secs) if isinstance(secs, list) and secs else 'Title, Abstract, Introduction, Method, Experiments'}",
            f"- **Paper type**: {ptype if present(ptype) else 'not given; choose by routing.md'}",
            f"- **One-line claim**: {meta.get('one_line') or '[MISSING]'}"]

    def block(title, fields, missing):
        out.extend(["", title])
        for sec, key, label in fields:
            v = d.get(sec, {}).get(key)
            if not present(v):
                missing.append(label)
            if sec == "meta":
                continue
            if isinstance(v, list):
                items = [it for it in v if isinstance(it, dict) and any(str(x).strip() for k, x in it.items() if k not in SELECT_KEYS)]
                out.append(f"- **{label}**:\n{fmt_list(key, items) if items else '  [MISSING]'}")
            else:
                out.append(f"- **{label}**: {v.strip() if present(v) else '[MISSING]'}")

    missing_req, missing_rec = [], []
    block("## Required (form v1.2)", REQUIRED, missing_req)
    block("## Recommended: what makes it memorable (ask once if missing)", RECOMMENDED, missing_rec)
    extra = [f"- **{label}**: {str(enh.get(key)).strip()}" for key, label in ENHANCERS if present(enh.get(key))]
    if extra:
        out += ["", "## Further enhancers"] + extra
    out += ["", "## Supporting information"]
    for key, label in SUPPORT:
        v = sup.get(key)
        if present(v):
            out.append(f"- **{label}**: {str(v).strip()}")
    bib = (sup.get("bib") or "").strip()
    out.append(f"- **Bibliography**: {'provided (' + str(bib.count('@')) + ' entries)' if bib else 'not provided; mark citations as [TODO: cite …]'}")
    mx = d.get("methodexp", {})
    ME = [("paste", "Pasted method and experiment material"), ("setting", "Problem setting and notation"), ("base_model", "Base model and what stays the same"),
          ("overview", "Pipeline overview and Figure 2"), ("components", "Method components (need / mechanism / property)"),
          ("objective", "Objective, optimization, inference"), ("implementation", "Implementation details"),
          ("datasets", "Datasets"), ("metrics", "Metrics"), ("baselines", "Baselines"), ("main_tables", "Main result tables"),
          ("ablations", "Ablations"), ("analysis", "Further analysis"), ("qualitative", "Qualitative results"),
          ("failure_cases", "Failure cases (for Limitations)")]
    me_missing = []
    if any(present(mx.get(k)) for k, _ in ME):
        out += ["", "## Method and experiments (references/method.md, experiments.md)"]
        for key, label in ME:
            v = mx.get(key)
            if not present(v):
                me_missing.append(label); continue
            if isinstance(v, list):
                items = [it for it in v if isinstance(it, dict) and any(str(x).strip() for k, x in it.items() if k not in SELECT_KEYS)]
                out.append(f"- **{label}**:\n" + "\n".join("  " + str(i + 1) + ". " + "; ".join(f"{k}: {x}" for k, x in it.items() if str(x).strip()) for i, it in enumerate(items)))
            else:
                out.append(f"- **{label}**: {str(v).strip()}")
    else:
        me_missing = ["all (method/experiments not requested or not provided)"]
    out += ["", "## Notes for the writer",
            "- Figure/table numbers in this brief refer to the author's full draft; do not cite them in the abstract or introduction unless that figure is part of the paper being written.",
            "- Where a component's mechanism is not stated, write [TODO] and ask instead of describing it with abstract nouns."]
    out += ["", "## Missing", f"- Required: {', '.join(missing_req) if missing_req else 'none'}",
            f"- Recommended (ask once in one compact message, then proceed with [TODO]): {', '.join(missing_rec) if missing_rec else 'none'}",
            f"- Method/experiments (needed only for those sections; missing mechanisms and numbers become [TODO]): {', '.join(me_missing) if me_missing else 'none'}"]
    text = "\n".join(out) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    else:
        print(text)
    if a.bib and bib:
        Path(a.bib).write_text(bib + "\n", encoding="utf-8")
    return 2 if missing_req else 0


if __name__ == "__main__":
    sys.exit(main())
