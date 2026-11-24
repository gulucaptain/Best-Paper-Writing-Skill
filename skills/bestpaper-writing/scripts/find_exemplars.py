#!/usr/bin/env python3
"""Retrieve award-paper exemplars.

  python3 scripts/find_exemplars.py intro.gap              # sentence moves (moves.jsonl); no argument lists moves
  python3 scripts/find_exemplars.py --para contrast --type L1   # paragraphs by main function (paragraphs.jsonl)
  python3 scripts/find_exemplars.py --para list             # list paragraph functions
  python3 scripts/find_exemplars.py --phrases insight -n 5  # sentence frames (phrasebank.csv)
"""
import argparse, csv, json, random, sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style_metrics as sm  # noqa: E402

EX = Path(__file__).resolve().parent.parent / "references/exemplars"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("move", nargs="?", default="", help="move prefix; empty lists all moves")
    ap.add_argument("--para", help="paragraph function (or 'list')")
    ap.add_argument("--phrases", help="sentence-frame function (or 'list')")
    ap.add_argument("-n", type=int, default=0, help="max examples (random sample); 0 = all")
    ap.add_argument("--type", help="paper type filter, e.g. L1")
    ap.add_argument("--motivation", help="motivation type filter, e.g. failure")
    ap.add_argument("--venue", help="venue, sibling venue (EMNLP/ECCV/ICLR), comma list, or domain (NLP/CV/ML)")
    ap.add_argument("--related", action="store_true", help="include sibling conferences in the same venue family")
    ap.add_argument("--section", help="section filter for moves, e.g. introduction, method, experiments")
    a = ap.parse_args()

    def sample(recs):
        return random.sample(recs, a.n) if a.n and len(recs) > a.n else recs

    exact_v, related_v, fam = sm.resolve_venues(a.venue, include_related=a.related)
    exact_set = {v.upper() for v in exact_v}
    related_set = {v.upper() for v in related_v}

    def filter_venue(recs):
        if not a.venue or a.venue.lower() == "all":
            return recs
        hit = [r for r in recs if r.get("venue", "").upper() in exact_set]
        if hit or not related_set or related_set == exact_set:
            return hit
        rel = [r for r in recs if r.get("venue", "").upper() in related_set]
        if rel:
            matched = sorted({r.get("venue", "") for r in rel})
            print(f"(matched related {fam or ''} conference(s) for '{a.venue}': {', '.join(matched)})\n")
        return rel

    if a.para:
        recs = [json.loads(l) for l in (EX / "paragraphs.jsonl").open(encoding="utf-8")]
        if a.para == "list":
            recs = filter_venue(recs)
            for k, v in sorted(Counter(r["function"] for r in recs).items()):
                print(f"{k:18s} {v}")
            return
        base = [r for r in recs if r["function"] == a.para and (not a.type or r["paper_type"] == a.type)
                and (not a.motivation or r.get("motivation_type") == a.motivation)]
        sel = filter_venue(base)
        if not sel and (a.type or a.venue):
            print(f"(no exact {a.para} match for filters; broadening)\n")
            sel = [r for r in recs if r["function"] == a.para]
        for r in sample(sel):
            print(f"[{r['function']} · {r['paper_type']} · {r.get('motivation_type')}] {r['paper']} · {r['venue']} {r['year']} · p.{r['page']}")
            print(f"  why: {r['why_good']}\n  {r['text']}\n")
        return
    if a.phrases:
        rows = list(csv.DictReader((EX / "phrasebank.csv").open(encoding="utf-8")))
        if a.phrases == "list":
            rows = filter_venue(rows)
            for k, v in sorted(Counter(r["function"] for r in rows).items()):
                print(f"{k:18s} {v}")
            return
        sel = filter_venue([r for r in rows if r["function"] == a.phrases])
        if not sel and a.venue:
            sel = [r for r in rows if r["function"] == a.phrases]
        for r in sample(sel):
            print(f"{r['pattern']}   (papers: {r['n_papers']})\n  e.g. {r['example']} — {r['paper']} · {r['venue']} {r['year']}\n")
        return
    recs = [json.loads(l) for l in (EX / "moves.jsonl").open(encoding="utf-8")]
    if not a.move:
        recs = filter_venue([r for r in recs if not a.section or r.get("section") == a.section])
        for k, v in sorted(Counter(r["move"] for r in recs).items()):
            print(f"{k:45s} {v}")
        return
    recs = filter_venue([r for r in recs if r["move"].startswith(a.move)
                         and (not a.type or r["paper_type"] == a.type)
                         and (not a.motivation or r.get("motivation_type") == a.motivation)
                         and (not a.section or r.get("section") == a.section)])
    for r in sample(recs):
        print(f"[{r['move']}] {r['quote']}\n    — {r['paper']} · {r['venue']} {r['year']} · p.{r['page']}\n")


if __name__ == "__main__":
    main()
