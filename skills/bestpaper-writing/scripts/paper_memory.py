#!/usr/bin/env python3
"""Paper Memory Bank: query award-paper topic selection, detail budgets, and writing style.

Backed by git-friendly JSONL sources (references/memory/section_memory.jsonl and optional
user_memory.jsonl) indexed into a local SQLite FTS5 database (paper_memory.db). Stdlib only.

Usage:
  python3 scripts/paper_memory.py list
  python3 scripts/paper_memory.py stats [--venue ACL]
  python3 scripts/paper_memory.py query --subsection exp.datasets --venue ACL --topic "reasoning" -k 3
  python3 scripts/paper_memory.py style-sheet --subsection exp.datasets --venue ACL
  python3 scripts/paper_memory.py audit draft_exp.tex --subsection auto
  python3 scripts/paper_memory.py add --file my_fav.md --paper "MyFav" --venue ACL --year 2025 --type L1 --subsection exp.datasets
"""
import argparse
import json
import re
import signal
import sqlite3
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path

if hasattr(signal, "SIGPIPE"):
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

ROOT = Path(__file__).resolve().parent.parent
MEM_DIR = ROOT / "references/memory"
CORE_JSONL = MEM_DIR / "section_memory.jsonl"
USER_JSONL = MEM_DIR / "user_memory.jsonl"
DB_PATH = MEM_DIR / "paper_memory.db"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style_metrics as sm  # noqa: E402

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS entries (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    paper_id TEXT,
    paper TEXT NOT NULL,
    venue TEXT NOT NULL,
    year INTEGER NOT NULL,
    paper_type TEXT NOT NULL,
    domain TEXT,
    section TEXT NOT NULL,
    subsection_type TEXT NOT NULL,
    heading TEXT,
    page INTEGER,
    excerpt TEXT NOT NULL,
    word_count INTEGER NOT NULL,
    sentence_count INTEGER NOT NULL,
    mean_sent_len REAL NOT NULL,
    numbers_per_100w REAL NOT NULL,
    topic_selection_json TEXT NOT NULL,
    style_signature_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_subsec ON entries(subsection_type);
CREATE INDEX IF NOT EXISTS idx_venue ON entries(venue);
CREATE INDEX IF NOT EXISTS idx_type ON entries(paper_type);
CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts USING fts5(
    id UNINDEXED,
    paper,
    heading,
    subsection_type,
    excerpt,
    topic_text,
    style_text
);
"""


def compute_text_stats(text: str):
    m, ss = sm.metric([text])
    wc = max(m["words"], 1)
    return {
        "word_count": m["words"],
        "sentence_count": m["sentences"],
        "mean_sent_len": round(m["sent_len_mean"], 2),
        "numbers_per_100w": round(m["numbers"] / wc * 100.0, 2),
    }


def load_jsonl(path: Path, source: str):
    if not path.exists():
        return []
    recs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        r["_source"] = source
        recs.append(r)
    return recs


def build_db(force: bool = False):
    MEM_DIR.mkdir(parents=True, exist_ok=True)
    src_mtime = max(
        (p.stat().st_mtime for p in (CORE_JSONL, USER_JSONL) if p.exists()),
        default=0.0,
    )
    if not force and DB_PATH.exists() and DB_PATH.stat().st_mtime >= src_mtime:
        return
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(SCHEMA_SQL)
    recs = load_jsonl(CORE_JSONL, "core") + load_jsonl(USER_JSONL, "user")
    cur = conn.cursor()
    for idx, r in enumerate(recs, 1):
        eid = r.get("id") or f"M{idx:04d}"
        excerpt = r["excerpt"].strip()
        st = compute_text_stats(excerpt)
        ts = r.get("topic_selection") or {}
        ss = r.get("style_signature") or {}
        cur.execute(
            """INSERT OR REPLACE INTO entries VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                eid, r["_source"], r.get("paper_id", ""), r["paper"], r["venue"],
                int(r["year"]), r.get("paper_type", "L1"), r.get("domain", "NLP"),
                r.get("section", "body"), r["subsection_type"], r.get("heading", ""),
                int(r.get("page") or 0), excerpt,
                st["word_count"], st["sentence_count"], st["mean_sent_len"], st["numbers_per_100w"],
                json.dumps(ts, ensure_ascii=False), json.dumps(ss, ensure_ascii=False),
            ),
        )
        topic_text = " ".join(
            (ts.get("included") or [])
            + (ts.get("omitted_or_deferred") or [])
            + ([ts.get("reader_focus", "")] if ts.get("reader_focus") else [])
        )
        style_text = " ".join(
            (ss.get("rhetorical_moves") or [])
            + (ss.get("syntax_patterns") or [])
            + (ss.get("lexical_choices") or [])
            + ([ss.get("tone_and_voice", "")] if ss.get("tone_and_voice") else [])
        )
        cur.execute(
            "INSERT INTO entries_fts VALUES (?,?,?,?,?,?,?)",
            (eid, r["paper"], r.get("heading", ""), r["subsection_type"], excerpt, topic_text, style_text),
        )
    conn.commit()
    conn.close()


def connect():
    build_db(force=False)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def pct(vals, p):
    vals = sorted(vals)
    if not vals:
        return 0
    k = (len(vals) - 1) * p / 100.0
    f = int(k)
    c = min(f + 1, len(vals) - 1)
    return round(vals[f] + (vals[c] - vals[f]) * (k - f), 1)


def fts_query_str(topic: str) -> str:
    toks = re.findall(r"[A-Za-z0-9]+", topic.lower())
    stop = {"the", "and", "for", "with", "that", "this", "from", "are", "our", "how", "what", "into"}
    toks = [t for t in toks if len(t) >= 2 and t not in stop]
    return " OR ".join(toks[:12])


def _query_db(conn, subsection=None, venues=None, ptype=None, topic=None, limit=0):
    where, params = [], []
    if subsection:
        if "." in subsection:
            where.append("e.subsection_type = ?")
            params.append(subsection)
        else:
            where.append("(e.subsection_type = ? OR e.subsection_type LIKE ?)")
            params.extend([subsection, f"{subsection}.%"])
    if venues:
        ph = ",".join("UPPER(?)" for _ in venues)
        where.append(f"UPPER(e.venue) IN ({ph})")
        params.extend(venues)
    if ptype:
        where.append("UPPER(e.paper_type) = UPPER(?)")
        params.append(ptype)

    fq = fts_query_str(topic) if topic else ""
    if fq:
        sql = (
            "SELECT e.*, bm25(entries_fts) AS score "
            "FROM entries_fts f JOIN entries e ON e.id = f.id "
            f"WHERE entries_fts MATCH ? {'AND ' + ' AND '.join(where) if where else ''} "
            "ORDER BY score ASC, e.year DESC"
        )
        rows = conn.execute(sql, [fq] + params).fetchall()
        if not rows and where:
            sql = f"SELECT e.*, 0.0 AS score FROM entries e WHERE {' AND '.join(where)} ORDER BY e.year DESC, e.id"
            rows = conn.execute(sql, params).fetchall()
    else:
        sql = f"SELECT e.*, 0.0 AS score FROM entries e {'WHERE ' + ' AND '.join(where) if where else ''} ORDER BY e.year DESC, e.id"
        rows = conn.execute(sql, params).fetchall()

    if limit > 0:
        picked, seen_papers = [], set()
        for r in rows:
            if r["paper"] not in seen_papers:
                picked.append(r)
                seen_papers.add(r["paper"])
                if len(picked) >= limit:
                    break
        if len(picked) < limit:
            ids = {r["id"] for r in picked}
            for r in rows:
                if r["id"] not in ids:
                    picked.append(r)
                    if len(picked) >= limit:
                        break
        return picked
    return rows


def fetch_entries(conn, subsection=None, venue=None, ptype=None, topic=None, limit=0, include_related=False):
    """Fetch entries with 2-stage venue matching: exact venue -> related conference family."""
    exact, related, _ = sm.resolve_venues(venue, include_related=include_related)
    rows = _query_db(conn, subsection, exact or None, ptype, topic, limit)
    if not rows and related and related != exact:
        rows = _query_db(conn, subsection, related, ptype, topic, limit)
    return rows


def venue_match_label(conn, subsection=None, venue=None, ptype=None, include_related=False):
    """Describe which venue tier actually matched (exact, related family, or broadened all)."""
    if not venue or venue.strip().lower() == "all":
        return "all venues", None
    exact, related, fam = sm.resolve_venues(venue, include_related=include_related)
    if exact and _query_db(conn, subsection, exact, ptype, None, 1):
        matched_v = sorted({r["venue"] for r in _query_db(conn, subsection, exact, ptype, None, 0)})
        if include_related and fam:
            return f"{venue} (related {fam} family: {', '.join(matched_v)})", None
        return ", ".join(matched_v), None
    if related and _query_db(conn, subsection, related, ptype, None, 1):
        matched_v = sorted({r["venue"] for r in _query_db(conn, subsection, related, ptype, None, 0)})
        note = f"No exact '{venue}' entries for this slice; matched related {fam or ''} conference(s): {', '.join(matched_v)}."
        return f"{venue} -> {', '.join(matched_v)}", note
    note = f"No '{venue}' (or related {fam or 'family'}) entries for this subsection yet; broadening to all venues."
    return "all venues", note


def cmd_list(args):
    conn = connect()
    rows = fetch_entries(conn, venue=args.venue, include_related=getattr(args, "related", False))
    v_label, note = venue_match_label(conn, venue=args.venue, include_related=getattr(args, "related", False))
    if note:
        print(f"({note})\n")
    if not rows:
        rows = _query_db(conn)
    by_sub = {}
    for r in rows:
        by_sub.setdefault(r["subsection_type"], []).append((r["word_count"], r["sentence_count"]))
    print(f"Venue filter: {v_label} (total={len(rows)})")
    print(f"{'subsection_type':22s} {'n':>4s}  {'median_w':>8s}  {'p25-p75_w':>11s}  {'median_s':>8s}")
    print("-" * 62)
    for sub in sorted(by_sub):
        ws = [x[0] for x in by_sub[sub]]
        ss = [x[1] for x in by_sub[sub]]
        print(f"{sub:22s} {len(ws):4d}  {pct(ws,50):8.0f}  {pct(ws,25):4.0f}-{pct(ws,75):<6.0f}  {pct(ss,50):8.1f}")


def cmd_stats(args):
    conn = connect()
    rows = fetch_entries(conn, venue=args.venue, include_related=getattr(args, "related", False))
    v_label, note = venue_match_label(conn, venue=args.venue, include_related=getattr(args, "related", False))
    if note:
        print(f"({note})")
    papers = len({r["paper"] for r in rows})
    print(f"Paper Memory Bank [{v_label}]: {len(rows)} section/subsection entries across {papers} award papers")
    for label, col in (("By venue", "venue"), ("By paper type", "paper_type"), ("By source", "source")):
        c = Counter(r[col] for r in rows)
        print(f"  {label}: " + ", ".join(f"{k}={v}" for k, v in c.most_common()))


def cmd_query(args):
    conn = connect()
    inc_rel = getattr(args, "related", False)
    v_label, note = venue_match_label(conn, args.subsection, args.venue, args.type, include_related=inc_rel)
    pool = fetch_entries(conn, args.subsection, args.venue, args.type, topic=None, limit=0, include_related=inc_rel)
    if not pool and (args.venue or args.type):
        pool = fetch_entries(conn, args.subsection, None, None, topic=None, limit=0)
    picked = fetch_entries(conn, args.subsection, args.venue, args.type, topic=args.topic, limit=args.k, include_related=inc_rel)
    if not picked and (args.venue or args.type):
        if not note:
            note = f"No exact match for filters; broadening across venues/types."
        picked = fetch_entries(conn, args.subsection, None, None, topic=args.topic, limit=args.k)
    if not picked:
        print("No matching entries found. Run `paper_memory.py list` to see available subsection types.")
        return
    if note and not args.json:
        print(f"({note})\n")

    if args.json:
        out = []
        for r in picked:
            d = dict(r)
            d["topic_selection"] = json.loads(d.pop("topic_selection_json"))
            d["style_signature"] = json.loads(d.pop("style_signature_json"))
            out.append(d)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    ws = [r["word_count"] for r in pool]
    ss = [r["sentence_count"] for r in pool]
    sl = [r["mean_sent_len"] for r in pool]
    moves, incl_all, omit_all = Counter(), Counter(), Counter()
    for r in pool:
        ts = json.loads(r["topic_selection_json"])
        sig = json.loads(r["style_signature_json"])
        for m in sig.get("rhetorical_moves") or []:
            moves[m] += 1
        for x in ts.get("included") or []:
            incl_all[x] += 1
        for x in ts.get("omitted_or_deferred") or []:
            omit_all[x] += 1

    header = args.subsection or "all subsections"
    print(f"=== IMITATION STUDY BRIEF: {header} ({v_label}, pool n={len(pool)}) ===")
    print(
        f"Excerpt stats : {pct(ws,50):.0f}w median (p25-p75: {pct(ws,25):.0f}-{pct(ws,75):.0f}w) | "
        f"{pct(ss,50):.0f} sents median | mean sent len {pct(sl,50):.1f}w"
    )
    if moves:
        print("Common moves  : " + ", ".join(f"{k} ({v})" for k, v in moves.most_common(6)))
    print()

    for idx, r in enumerate(picked, 1):
        ts = json.loads(r["topic_selection_json"])
        sig = json.loads(r["style_signature_json"])
        print(
            f"[{idx}] {r['paper']} ({r['venue']} {r['year']} · {r['paper_type']} · {r['subsection_type']} · "
            f"{r['word_count']}w / {r['sentence_count']} sents · heading: {r['heading']})"
        )
        if ts.get("reader_focus"):
            print(f"  Reader focus  : {ts['reader_focus']}")
        if ts.get("included"):
            print("  Included      : " + " | ".join(ts["included"]))
        if ts.get("omitted_or_deferred"):
            print("  Omitted/Defer : " + " | ".join(ts["omitted_or_deferred"]))
        if sig.get("syntax_patterns"):
            print("  Syntax frames : " + " || ".join(sig["syntax_patterns"][:3]))
        if sig.get("lexical_choices"):
            print("  Lexical cues  : " + ", ".join(sig["lexical_choices"][:6]))
        if sig.get("tone_and_voice"):
            print(f"  Tone & voice  : {sig['tone_and_voice']}")
        print(f"  Excerpt (study structure & style; never copy >=6 consecutive words):")
        print(f"    {r['excerpt']}\n")


def cmd_style_sheet(args):
    conn = connect()
    inc_rel = getattr(args, "related", False)
    v_label, note = venue_match_label(conn, args.subsection, args.venue, args.type, include_related=inc_rel)
    rows = fetch_entries(conn, args.subsection, args.venue, args.type, topic=None, limit=0, include_related=inc_rel)
    if not rows and (args.venue or args.type):
        rows = fetch_entries(conn, args.subsection, None, None, topic=None, limit=0)
    if not rows:
        print("No matching entries.")
        return
    if note:
        print(f"({note})\n")
    ws = [r["word_count"] for r in rows]
    sl = [r["mean_sent_len"] for r in rows]
    nums = [r["numbers_per_100w"] for r in rows]
    moves, lex, tones = Counter(), Counter(), []
    syntaxes, omits, focuses = [], [], []
    for r in rows:
        ts = json.loads(r["topic_selection_json"])
        sig = json.loads(r["style_signature_json"])
        moves.update(sig.get("rhetorical_moves") or [])
        lex.update(x.lower() for x in (sig.get("lexical_choices") or []))
        for sp in sig.get("syntax_patterns") or []:
            if sp not in syntaxes:
                syntaxes.append(sp)
        for om in ts.get("omitted_or_deferred") or []:
            if om not in omits:
                omits.append(om)
        if ts.get("reader_focus"):
            focuses.append((r["paper"], ts["reader_focus"]))
        if sig.get("tone_and_voice"):
            tones.append(sig["tone_and_voice"])

    print(f"# Style & Topic-Selection Sheet: {args.subsection or 'all'} ({v_label}, n={len(rows)})")
    print(f"- Excerpt reference length: median {pct(ws,50):.0f}w (p25–p75: {pct(ws,25):.0f}–{pct(ws,75):.0f}w across curated 1–3 paragraph excerpts)")
    print(f"- Sentence rhythm: median mean-length {pct(sl,50):.1f} words; numbers {pct(nums,50):.1f} per 100w")
    print("\n## Recurring Rhetorical Moves")
    for k, v in moves.most_common(10):
        print(f"- `{k}` ({v}/{len(rows)})")
    print("\n## Reusable Syntactic Patterns")
    for sp in syntaxes[:12]:
        print(f"- {sp}")
    print("\n## High-Signal Expressions & Collocations")
    print(", ".join(f"`{k}`" for k, _ in lex.most_common(25)))
    print("\n## What Award Papers Deliberately Omit or Defer to Appendix")
    for om in omits[:10]:
        print(f"- {om}")
    print("\n## Reader-Focus Takeaways")
    for paper, f in focuses[:6]:
        print(f"- **{paper}**: {f}")


# --- Detail-Granularity & Anti-Laundry-List Audit ---

SPLIT_DUMP_PAT = re.compile(
    r"(?:\btrain(?:ing)?\b.{0,45}\b(?:val(?:idation)?|dev(?:elopment)?)\b.{0,45}\btest\b|"
    r"\b\d[\d,]*\s+(?:training|train)\s+(?:examples?|samples?|instances?|pairs?|sentences?)\b.{0,80}\b\d[\d,]*\s+(?:test|validation|dev)\b)",
    re.I,
)
HYPERPARAM_TERMS = [
    r"\blearning rate\b", r"\bbatch size\b", r"\bweight decay\b", r"\bwarmup\b",
    r"\badamw?\b", r"\bdropout\b", r"\brandom seeds?\b", r"\bepochs?\b",
    r"\bgradient clipping\b", r"\bcosine schedule\b", r"\bbeta[_ ]?1\b",
]
PLUMBING_TERMS = [
    r"\b(?:lowercas\w*|strip(?:ping)? whitespace|remove punctuation|utf-8)\b",
    r"\b(?:pytorch|tensorflow|huggingface|transformers library|deepspeed)\b",
    r"\b(?:nvidia|a100|h100|v100|rtx|cuda)\b",
    r"\b(?:bf16|fp16|mixed precision|checkpoint(?:s|ing)?)\b",
]
STEP_OPENER_PAT = re.compile(
    r"^(?:first(?:ly)?|second(?:ly)?|third(?:ly)?|fourth(?:ly)?|next|then|after that|afterwards|subsequently|finally|lastly|step\s+\d+)\b[,:]?\s|"
    r"^we\s+(?:first|then|next|subsequently|finally)\b",
    re.I,
)
ROLLCALL_PAT = re.compile(
    r"^(?:(?:[A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+|\s+et\s+al\.?)\s*(?:\(\d{4}[a-z]?\)|\[c\])?|\[c\])\s+"
    r"(?:proposes?|proposed|introduces?|introduced|presents?|presented|develops?|developed|"
    r"extends?|extended|appl(?:y|ies|ied)|uses?|used|trains?|trained|explores?|explored|stud(?:y|ies|ied))|"
    r"in\s+(?:19|20)\d{2},\s+)",
    re.I,
)
ROW_NARRATION_PAT = re.compile(
    r"^(?:on\s+[A-Z0-9][\w\-+/ ]{1,24},|for\s+(?:the\s+)?[A-Z0-9][\w\-+/ ]{1,24}(?:\s+(?:dataset|benchmark|task))?,|"
    r"when\s+(?:removing|ablating|disabling|dropping)\b|removing\s+[\w\- ]{1,28}\s+(?:drops?|reduces?|decreases?|causes?|leads?))",
    re.I,
)
ROADMAP_PAT = re.compile(
    r"\b(?:the rest of (?:this|the) paper is organized|this paper is organized as follows|"
    r"section\s+2\s+(?:reviews|discusses|introduces).{0,100}section\s+3)\b",
    re.I,
)
APPENDIX_CUE = re.compile(r"\b(appendix|supplementary|table\s+\d+|tab\.\s*\d+|following\s+\[c\]|following\s+[A-Z][a-z]+\s+et\s+al)\b", re.I)


def split_draft_subsections(path: Path):
    raw = path.read_text(encoding="utf-8")
    is_tex = path.suffix == ".tex"
    if is_tex:
        # Preserve section/subsection/paragraph hierarchy before cleaning
        raw = re.sub(r"\\subsection\*?\{([^}]*)\}", r"\n## \1\n", raw)
        raw = re.sub(r"\\paragraph\*?\{([^}]*)\}", r"\n### \1\n", raw)
        raw = re.sub(r"\\section\*?\{([^}]*)\}", r"\n# \1\n", raw)
        raw = sm.clean_tex(raw)
    blocks = []
    cur_sec, cur_h, cur_lines = "", "Body", []
    for ln in raw.splitlines():
        m = re.match(r"^(#{1,3})\s+(.+)", ln.strip())
        if m:
            if cur_lines:
                txt = " ".join(" ".join(cur_lines).split())
                if txt:
                    blocks.append((cur_sec, cur_h, txt))
            level = len(m.group(1))
            title = m.group(2).strip().rstrip(".")
            if level == 1:
                cur_sec = title
            cur_h = title
            cur_lines = []
        else:
            cur_lines.append(ln)
    if cur_lines:
        txt = " ".join(" ".join(cur_lines).split())
        if txt:
            blocks.append((cur_sec, cur_h, txt))
    return blocks


def guess_subsection_type(heading: str, parent_sec: str = "") -> str:
    h = heading.lower()
    p = parent_sec.lower()
    if "abstract" in h:
        return "abstract"
    if "introduction" in h:
        return "intro.opening"
    if any(k in h for k in ("dataset", "benchmark", "corpus", "data")):
        return "exp.datasets"
    if any(k in h for k in ("baseline", "compared")):
        return "exp.baselines"
    if any(k in h for k in ("metric", "evaluation measure")):
        return "exp.metrics"
    if any(k in h for k in ("implementation", "training detail", "hyperparameter", "setup", "setting")):
        return "exp.implementation"
    if "ablation" in h:
        return "exp.ablation"
    if any(k in h for k in ("main result", "overall", "quantitative", "performance", "result")):
        return "exp.main_results"
    if any(k in h for k in ("analysis", "error", "efficiency", "scaling", "discussion", "case")):
        return "exp.analysis"
    if "related" in h:
        return "related_work"
    if "limitation" in h:
        return "limitations"
    if any(k in h for k in ("overview", "preliminar", "formulation")):
        return "method.overview"
    if any(k in h for k in ("training", "objective", "loss", "optimization")):
        return "method.training"
    # Fall back to parent section context so custom subsection titles are still audited
    if any(k in p for k in ("method", "approach", "framework", "model", "algorithm")):
        return "method.component"
    if any(k in p for k in ("experiment", "evaluation")):
        return "exp.analysis"
    if "related" in p:
        return "related_work"
    if "introduction" in p:
        return "intro.opening"
    if "limitation" in p:
        return "limitations"
    return ""


def audit_block(conn, heading: str, text: str, subsec: str, venue: str):
    st = compute_text_stats(text)
    sents = sm.split_sentences(text)
    findings = []
    pool = fetch_entries(conn, subsec, venue, None, None, 0) if subsec else []
    if not pool and subsec:
        pool = fetch_entries(conn, subsec, None, None, None, 0)
    budget_note = ""
    if pool:
        ws = [r["word_count"] for r in pool]
        p50, p75 = pct(ws, 50), pct(ws, 75)
        budget_note = f"excerpt ref median={p50:.0f}w, p75={p75:.0f}w (n={len(pool)})"
    if subsec in ("exp.datasets", "exp.implementation", "exp.baselines", "exp.metrics") and st["word_count"] > 320:
        findings.append(
            f"NOTE  lengthy setup subsection ({st['word_count']} words). "
            "Consider moving routine benchmark specs, splits, or hyperparameter lists into a compact table or Appendix."
        )

    # 1. Procedural / chronological step-by-step laundry list
    step_hits = sum(1 for s in sents if STEP_OPENER_PAT.search(s.strip()))
    if step_hits >= 3:
        findings.append(
            f"WARN  procedural laundry list ({step_hits} sentences use sequential step openers like 'First/Next/Then/Finally' or 'We first/then'). "
            "Replace play-by-play narration with causal logic (Need -> Mechanism -> Property, or Claim -> Evidence -> Reason)."
        )

    # 2. Boilerplate paper-organization roadmap filler
    if ROADMAP_PAT.search(text):
        findings.append(
            "WARN  paper roadmap filler ('The rest of this paper is organized as follows...'). "
            "Cut section-by-section roadmaps; award papers spend that space on insight or concrete evidence."
        )

    # 3. Bibliographic / baseline paper-by-paper roll-call
    if subsec in ("related_work", "exp.baselines", "intro.opening", ""):
        roll_hits = sum(1 for s in sents if ROLLCALL_PAT.search(s.strip()))
        if roll_hits >= 3:
            findings.append(
                f"WARN  paper-by-paper roll-call ({roll_hits} sentences start with '[Author/Year] proposes/uses...'). "
                "Group prior works or baselines by shared assumption/paradigm and state how your method differs."
            )

    # 4. Dataset split dump & hyperparameter / plumbing prose dumps
    if subsec in ("exp.datasets", "exp.implementation", "") and SPLIT_DUMP_PAT.search(text):
        findings.append(
            "WARN  dataset split dump: enumerating train/val/test split sizes inline distracts from why the benchmarks test your claim. "
            "For standard public benchmarks, summarize their role in 1-2 sentences with citations and move split counts to Appendix or a compact table."
        )
    hp_hits = sum(1 for pat in HYPERPARAM_TERMS if re.search(pat, text, re.I))
    if hp_hits >= 4:
        findings.append(
            f"WARN  hyperparameter prose dump ({hp_hits} low-level training knobs recited inline). "
            "State base model, key delta, and compute budget in 2-3 sentences; move full hyperparameter lists to Appendix."
        )
    plumb_hits = sum(1 for pat in PLUMBING_TERMS if re.search(pat, text, re.I))
    if plumb_hits >= 3 and not APPENDIX_CUE.search(text):
        findings.append(
            f"WARN  engineering/preprocessing plumbing dump ({plumb_hits} routine software/hardware/preprocessing details inline without Appendix deferral). "
            "Keep only choices that affect the scientific claim; defer plumbing to Appendix."
        )
    if subsec in ("exp.datasets", "exp.implementation", "exp.baselines") and st["word_count"] > 140 and not APPENDIX_CUE.search(text):
        findings.append(
            "NOTE  long setup prose with no citation-offload or Appendix pointer ('following ...', 'detailed in Appendix ...')."
        )

    # 5. Table / ablation cell-by-cell narration
    if subsec in ("exp.main_results", "exp.ablation", "exp.analysis"):
        dense_num = sum(1 for s in sents if len(sm.number_tokens(s)) >= 4)
        if dense_num >= 2:
            findings.append(
                f"WARN  table-narration laundry list: {dense_num} sentences pack >=4 numbers each. "
                "Lead with the claim and 1-2 headline margins; let the table hold the rest."
            )
        row_hits = sum(1 for s in sents if ROW_NARRATION_PAT.search(s.strip()))
        if row_hits >= 3:
            findings.append(
                f"WARN  per-row/per-dataset narration ({row_hits} sentences follow 'On X, ...' / 'When removing X, ...'). "
                "Synthesize the cross-benchmark pattern or causal takeaway instead of walking through table rows one by one."
            )
        if subsec == "exp.main_results" and sents and re.match(r"^(Table|Tab\.|Figure|Fig\.)\s+\d+\s+(shows|presents|reports|summarizes)", sents[0], re.I):
            findings.append(
                "WARN  opens with 'Table X shows...' instead of claim-first synthesis. State the main finding first and cite the table in parentheses."
            )
    return st, budget_note, findings


def cmd_audit(args):
    conn = connect()
    path = Path(args.file)
    blocks = split_draft_subsections(path)
    total_w = 0
    for parent_sec, heading, text in blocks:
        subsec = args.subsection if args.subsection != "auto" else guess_subsection_type(heading, parent_sec)
        if args.subsection == "auto" and not subsec:
            continue
        st, budget_note, findings = audit_block(conn, heading, text, subsec, args.venue)
        print(f"== [{subsec or 'manual'}] {heading} ({st['word_count']}w, {st['sentence_count']} sents"
              + (f" | {budget_note}" if budget_note else "") + ")")
        if not findings:
            print("  OK: detail level and focus match award-paper norms.")
        for f in findings:
            print(f"  {f}")
            if f.startswith("WARN"):
                total_w += 1
        if findings and subsec:
            print(f"  Tip: run `python3 scripts/paper_memory.py query --subsection {subsec} -k 3` to study concise award examples.")
    print(f"\nAudit complete: {total_w} warning(s).")


def cmd_add(args):
    src = Path(args.file)
    if not src.exists():
        print(f"File not found: {src}", file=sys.stderr)
        sys.exit(1)
    if src.suffix.lower() == ".pdf":
        raw = subprocess.check_output(["pdftotext", "-raw", str(src), "-"], text=True, errors="replace")
        excerpt = " ".join(raw.split())[:2000]
    elif src.suffix.lower() == ".tex":
        excerpt = " ".join(sm.clean_tex(src.read_text(encoding="utf-8")).split())
    else:
        excerpt = " ".join(src.read_text(encoding="utf-8").split())

    existing = load_jsonl(USER_JSONL, "user")
    eid = f"U{len(existing) + 1:04d}"
    section = args.subsection.split(".")[0] if "." in args.subsection else args.subsection
    section = {"exp": "experiments", "intro": "introduction"}.get(section, section)
    rec = {
        "id": eid,
        "paper_id": eid,
        "paper": args.paper,
        "venue": args.venue,
        "year": args.year,
        "paper_type": args.type,
        "domain": args.domain,
        "section": section,
        "subsection_type": args.subsection,
        "heading": args.heading or args.subsection,
        "page": args.page,
        "excerpt": excerpt,
        "topic_selection": {
            "included": [x.strip() for x in args.included.split(";") if x.strip()] if args.included else [],
            "omitted_or_deferred": [x.strip() for x in args.omitted.split(";") if x.strip()] if args.omitted else [],
            "reader_focus": args.focus or "",
        },
        "style_signature": {
            "rhetorical_moves": [x.strip() for x in args.moves.split(",") if x.strip()] if args.moves else [],
            "syntax_patterns": [x.strip() for x in args.syntax.split(";") if x.strip()] if args.syntax else [],
            "lexical_choices": [x.strip() for x in args.lex.split(",") if x.strip()] if args.lex else [],
            "tone_and_voice": args.tone or "",
        },
    }
    MEM_DIR.mkdir(parents=True, exist_ok=True)
    with USER_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    build_db(force=True)
    print(f"Added {eid} ({args.paper} · {args.venue} {args.year} · {args.subsection}) to {USER_JSONL.name} and rebuilt {DB_PATH.name}.")


def main():
    ap = argparse.ArgumentParser(description="Paper Memory Bank for topic-selection & style imitation")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("build", help="Rebuild SQLite FTS5 database from JSONL sources")

    p_list = sub.add_parser("list", help="List subsection types and empirical word budgets")
    p_list.add_argument("--venue", default="all", help="Venue, comma list, domain (NLP/CV/ML), or sibling venue (EMNLP/ECCV/ICLR/...)")
    p_list.add_argument("--related", action="store_true", help="Include sibling conferences in the same venue family")

    p_stats = sub.add_parser("stats", help="Show memory bank summary counts")
    p_stats.add_argument("--venue", default="all", help="Venue, comma list, domain (NLP/CV/ML), or sibling venue")
    p_stats.add_argument("--related", action="store_true", help="Include sibling conferences in the same venue family")

    p_q = sub.add_parser("query", help="Retrieve award-paper subsections & style/topic brief")
    p_q.add_argument("--subsection", "-s", help="e.g. exp.datasets, exp.main_results, method.component, limitations")
    p_q.add_argument("--venue", default="all", help="Exact venue (ACL/CVPR/ICCV/NeurIPS), sibling (EMNLP/NAACL/ECCV/ICLR/ICML), comma list, domain (NLP/CV/ML), or all")
    p_q.add_argument("--related", action="store_true", help="Include sibling conferences in the same venue family (e.g. CVPR -> CVPR+ICCV)")
    p_q.add_argument("--type", help="Paper type L1-L8")
    p_q.add_argument("--topic", help="Free-text topic keywords for FTS5 BM25 ranking")
    p_q.add_argument("-k", type=int, default=3, help="Number of exemplars to return")
    p_q.add_argument("--json", action="store_true")

    p_ss = sub.add_parser("style-sheet", help="Generate synthesized style & topic-selection guide")
    p_ss.add_argument("--subsection", "-s", help="Subsection type filter")
    p_ss.add_argument("--venue", default="all", help="Exact venue, sibling venue, comma list, domain (NLP/CV/ML), or all")
    p_ss.add_argument("--related", action="store_true", help="Include sibling conferences in the same venue family")
    p_ss.add_argument("--type")

    p_au = sub.add_parser("audit", help="Audit draft subsections for over-detailing & laundry lists")
    p_au.add_argument("file", help="Draft .md or .tex file")
    p_au.add_argument("--subsection", "-s", default="auto", help="Subsection type or 'auto'")
    p_au.add_argument("--venue", default="all", help="Target venue or sibling venue (e.g. ACL, EMNLP, CVPR, ICLR)")

    p_add = sub.add_parser("add", help="Add a favorite paper excerpt to user_memory.jsonl")
    p_add.add_argument("--file", required=True, help="Excerpt file (.md, .tex, .txt, or .pdf)")
    p_add.add_argument("--paper", required=True)
    p_add.add_argument("--venue", required=True)
    p_add.add_argument("--year", type=int, required=True)
    p_add.add_argument("--type", default="L1")
    p_add.add_argument("--domain", default="NLP")
    p_add.add_argument("--subsection", "-s", required=True)
    p_add.add_argument("--heading", default="")
    p_add.add_argument("--page", type=int, default=0)
    p_add.add_argument("--included", default="", help="Semicolon-separated included topics")
    p_add.add_argument("--omitted", default="", help="Semicolon-separated omitted/deferred details")
    p_add.add_argument("--focus", default="", help="Reader focus sentence")
    p_add.add_argument("--moves", default="", help="Comma-separated rhetorical moves")
    p_add.add_argument("--syntax", default="", help="Semicolon-separated syntax patterns")
    p_add.add_argument("--lex", default="", help="Comma-separated lexical choices")
    p_add.add_argument("--tone", default="")

    a = ap.parse_args()
    if a.cmd == "build":
        build_db(force=True)
        print(f"Rebuilt {DB_PATH}")
    elif a.cmd == "list":
        cmd_list(a)
    elif a.cmd == "stats":
        cmd_stats(a)
    elif a.cmd == "query":
        cmd_query(a)
    elif a.cmd == "style-sheet":
        cmd_style_sheet(a)
    elif a.cmd == "audit":
        cmd_audit(a)
    elif a.cmd == "add":
        cmd_add(a)


if __name__ == "__main__":
    main()
