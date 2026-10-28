#!/usr/bin/env python3
"""Retrieve award-paper exemplars.

  python3 scripts/find_exemplars.py intro.gap              # sentence moves (moves.jsonl); no argument lists moves
  python3 scripts/find_exemplars.py --para contrast --type L1   # paragraphs by main function (paragraphs.jsonl)
  python3 scripts/find_exemplars.py --para list             # list paragraph functions
  python3 scripts/find_exemplars.py --phrases insight -n 5  # sentence frames (phrasebank.csv)
"""
import argparse, csv, json, random
from collections import Counter
from pathlib import Path

EX = Path(__file__).resolve().parent.parent / "references/exemplars"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("move", nargs="?", default="", help="move prefix; empty lists all moves")
    ap.add_argument("--para", help="paragraph function (or 'list')")
    ap.add_argument("--phrases", help="sentence-frame function (or 'list')")
    ap.add_argument("-n", type=int, default=0, help="max examples (random sample); 0 = all")
    ap.add_argument("--type", help="paper type filter, e.g. L1")
    ap.add_argument("--motivation", help="motivation type filter, e.g. failure")
    a = ap.parse_args()

    def sample(recs):
        return random.sample(recs, a.n) if a.n and len(recs) > a.n else recs

    if a.para:
        recs = [json.loads(l) for l in (EX / "paragraphs.jsonl").open(encoding="utf-8")]
        if a.para == "list":
            for k, v in sorted(Counter(r["function"] for r in recs).items()):
                print(f"{k:16s} {v}")
            return
        sel = [r for r in recs if r["function"] == a.para and (not a.type or r["paper_type"] == a.type)
               and (not a.motivation or r.get("motivation_type") == a.motivation)]
        if not sel and a.type:
            print(f"(no {a.para} paragraph for {a.type}; showing all types)\n")
            sel = [r for r in recs if r["function"] == a.para]
        for r in sample(sel):
            print(f"[{r['function']} · {r['paper_type']} · {r.get('motivation_type')}] {r['paper']} · {r['venue']} {r['year']} · p.{r['page']}")
            print(f"  why: {r['why_good']}\n  {r['text']}\n")
        return
    if a.phrases:
        rows = list(csv.DictReader((EX / "phrasebank.csv").open(encoding="utf-8")))
        if a.phrases == "list":
            for k, v in sorted(Counter(r["function"] for r in rows).items()):
                print(f"{k:16s} {v}")
            return
        for r in sample([r for r in rows if r["function"] == a.phrases]):
            print(f"{r['pattern']}   (papers: {r['n_papers']})\n  e.g. {r['example']} — {r['paper']} · {r['venue']} {r['year']}\n")
        return
    recs = [json.loads(l) for l in (EX / "moves.jsonl").open(encoding="utf-8")]
    if not a.move:
        for k, v in sorted(Counter(r["move"] for r in recs).items()):
            print(f"{k:45s} {v}")
        return
    recs = [r for r in recs if r["move"].startswith(a.move)
            and (not a.type or r["paper_type"] == a.type)
            and (not a.motivation or r["motivation_type"] == a.motivation)]
    for r in sample(recs):
        print(f"[{r['move']}] {r['quote']}\n    — {r['paper']} · {r['venue']} {r['year']} · p.{r['page']}\n")


if __name__ == "__main__":
    main()
