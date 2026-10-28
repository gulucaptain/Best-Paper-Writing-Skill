#!/usr/bin/env python3
"""Mechanical checks for an Abstract/Introduction draft (.tex, .md or .txt).

Style checks compare the draft with the distribution of 55 award papers
(references/corpus/corpus_stats.json, same metric definitions as scripts/style_metrics.py).
Levels: ERROR (must fix), WARN (outside the range of 90% of award papers or a known
AI-draft habit; review), NOTE (information only).

Usage: python3 scripts/check_draft.py FILE [FILE ...] [--max-words 60]
Exit code 1 if any ERROR is found.
"""
import argparse, csv, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import style_metrics as sm

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "references/exemplars/moves.jsonl"

ERROR_PHRASES = {
    # boilerplate / overclaim
    r"has attracted (increasing|growing|more and more|much) attention": "boilerplate opening",
    r"hot topic": "boilerplate",
    r"plays an? (important|vital|key|crucial|significant) role\s*(in [^.,;]*)?[.;]": "bare 'plays an important role'",
    r"extensive experiments (demonstrate|show|verify|validate) the (effectiveness|superiority)": "boilerplate claim",
    r"\bsuperiority\b": "self-praise", r"\bdelve": "LLM tell", r"\bpivotal\b": "LLM tell",
    r"paradigm shift": "LLM tell", r"unlock(s|ing)? the (full )?potential": "LLM tell", r"\bseamless(ly)?\b": "LLM tell",
    r"a myriad of": "LLM tell", r"\blandscape\b": "LLM tell", r"in the realm of": "LLM tell",
    r"it is worth noting that": "filler", r"it can be seen that": "filler", r"simple yet effective": "cliché",
    r"comprehensive experiments": "boilerplate", r"\bthis proves\b": "experiments do not prove",
    # workflow traces
    r"\bsupplied\b": "workflow trace ('supplied')",
    r"\bprovided (results|evaluation|numbers|data|facts|input)\b|\bthe provided\b": "workflow trace ('provided …')",
    r"\bthe reported (evaluation|results|experiments)\b|\bin the reported\b": "workflow trace ('reported …')",
    r"according to the (input|user|notes)": "workflow trace",
    r"\[(intro|abstract|relwork|method|exp)\.[a-z\-.]+\]": "move tag left in text",
    r"→": "arrow (likely a move label) in text",
    # disclaimers / self-undermining (not allowed in abstract or introduction)
    r"does not (establish|imply|guarantee|isolate|prove)\b|do not (establish|imply|isolate)\b": "disclaimer (move to Limitations)",
    r"remains? to be (evaluated|tested|seen|explored)": "disclaimer (move to Limitations)",
    r"\bone limitation\b|\blimitations? of (our|this)\b|\bour (method|approach|model) (still )?(fails|is limited)\b": "limitation in abstract/introduction",
    r"\bleave [^.]* (for|to) future work\b": "future-work disclaimer",
    # defensive qualifiers about the protocol
    r"\bin our comparisons?\b|\bwithin the tested\b|\bunder the tested\b|\bin the evaluated setting\b|\bscores? (are|is) computed on\b|\bunder identical hyperparameters\b": "defensive qualifier (move to experiments)",
    # downgraded core idea
    r"\bour hypothesis is\b|\bwe take the view\b|\bwe conjecture\b": "core idea downgraded to a hypothesis",
}
NOTE_PHRASES = {
    r"\b(very|extremely|outstanding)\b": "intensifier; a number or mechanism is usually stronger",
    r"\bin order to\b": "'to' is usually enough",
    r"\bnovel\b": "fine if the sentence also says what is new",
    r"\bsignificant(ly)?\b": "fine with a number or a test nearby",
    r"state[- ]of[- ]the[- ]art|\bSOTA\b": "name the benchmark/baselines in the same sentence",
    r"\bthe first\b|\bfor the first time\b": "make sure the scope is stated",
    r"\beliminat(e|es|ing)\b": "absolute; check the claim map",
}
WARN_PHRASES = {
    r"\bto the best of our knowledge\b": "only with a scoped claim",
    r"\btables? \d+ (reports|shows)\b|\btab\.\s*\d+ (reports|shows)\b": "put the claim first and cite the table",
    r"\bin our setup\b": "hedge-like phrase",
}
DETAIL = r"\b\d+ (layers?|heads?|views?|steps?|epochs?|tokens? per)\b|\d+\s*[×x]\s*\d+\s*[×x]\s*\d+|\bbatch size\b|\blearning rate of\b|\bhidden (size|dimension)\b"
NUMBER = r"(?<![A-Za-z\d.])\d+(?:[.,]\d+)*(?![A-Za-z\d])"
PARAS = ROOT / "references/exemplars/paragraphs.jsonl"
PHRASES = ROOT / "references/exemplars/phrasebank.csv"
SECNAME = {"abstract": "abstract", "intro": "introduction"}
COMPARE = r"\b(outperform\w*|surpass\w*|better than|improv\w+|reduc\w+|faster|higher|lower|exceed\w*)\b"


def strip_latex(t):
    t = re.sub(r"(?<!\\)%.*", "", t)
    t = re.sub(r"\\(begin|end)\{[^}]*\}", "", t)
    t = re.sub(r"\\(cite[tp]?|citep|citet|ref|eqref|label)\*?(\[[^\]]*\])?\{[^}]*\}", " [c] ", t)
    t = re.sub(r"\\(section|subsection|paragraph)\*?\{([^}]*)\}", r"\n# \2\n", t)
    t = re.sub(r"\\item\s*", "\n- ", t)
    t = t.replace("\\times", "×").replace("~", " ").replace("---", "—").replace("--", "–")
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^{}]*)\}", r"\2", t)
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    t = t.replace("$", "").replace("{", "").replace("}", "")
    return t


def load_lines(path):
    raw = Path(path).read_text(encoding="utf-8")
    labels = 0
    if path.endswith(".tex"):
        labels = len(re.findall(r"\\paragraph\*?\{|^\s*\\textbf\{[^}]{1,80}\}", raw, flags=re.M))
        raw = strip_latex(raw)
    lines = []
    for ln in raw.splitlines():
        s = ln.strip()
        if s.startswith("<!--") or s.startswith("|") or s.startswith("```") or s.startswith("#"):
            lines.append("")
            continue
        if re.match(r"^\s*\*\*[^*]{2,80}\*\*", ln):
            labels += 1
        if re.match(r"^\s*([-*]|\d+\.)\s+", ln):
            lines.append("")
            ln = re.sub(r"^\s*([-*]|\d+\.)\s+", "", ln)
        lines.append(ln)
    return lines, labels


def sentences(lines):
    text = "\n".join(lines)
    out, start = [], 0
    for m in re.finditer(r"(?<=[.!?])\s+(?=[A-Z\[])|\n\s*\n", text):
        out.append((text[start:m.start()], text.count("\n", 0, start) + 1))
        start = m.end()
    out.append((text[start:], text.count("\n", 0, start) + 1))
    return [(re.sub(r"\s+", " ", s).strip(), n) for s, n in out if s.strip()]


def ngrams(s, n=6):
    w = re.findall(r"[a-z0-9]+", s.lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def bank_ngrams():
    bank = set()
    if BANK.exists():
        for l in BANK.open(encoding="utf-8"):
            bank |= ngrams(json.loads(l)["quote"])
    if PARAS.exists():
        for l in PARAS.open(encoding="utf-8"):
            bank |= ngrams(json.loads(l)["text"])
    if PHRASES.exists():
        for r in csv.DictReader(PHRASES.open(encoding="utf-8")):
            bank |= ngrams(r["example"])
    for p in (ROOT / "references/exemplars/cards").glob("*.md"):
        for ln in p.read_text(encoding="utf-8").splitlines():
            if ln.startswith("> ") and not ln.startswith("> —"):
                bank |= ngrams(ln)
    return bank - {"in this paper we propose a", "the rest of the paper is", "the main contributions of this",
                   "our main contributions are as follows", "we make the following contributions", "code and models are publicly available"}


def corpus_checks(path):
    """Compare section-level style metrics with the award-paper distribution."""
    stats = sm.load_stats()["style"]
    issues = []
    for sec, paras in sm.sections(path).items():
        if not paras:
            continue
        m, _ = sm.metric(paras)
        d = stats[sec]
        name = SECNAME[sec]
        def over(key, msg, level="WARN"):
            if m[key] > d[key]["p90"]:
                issues.append((level, 0, f"{name}: {msg} ({m[key]:.2f}; 90% of award papers ≤ {d[key]['p90']})", ""))
        over("numbers", "more numbers than most award papers; keep headline numbers, move the rest to experiments")
        over("connector_per_100w", "logical connectors per 100 words (therefore/thus/however/…); let sentence order carry the logic")
        over("colon_or_dash_sentences", "share of sentences with a colon; keep colons for lists, examples or the handle")
        if m["sent_len_mean"] > d["sent_len_mean"]["p75"]:
            issues.append(("NOTE", 0, f"{name}: mean sentence length {m['sent_len_mean']:.1f} words is heavier than 75% of award papers; let the pivots (bottleneck, cause, idea) stand as short sentences", ""))
        over("antithesis_ratio", "share of aphoristic contrasts ('X is not Y', 'rather than', 'need not'); keep one or two that carry the thesis and state the rest as plain facts")
        over("short_sent_ratio", "share of short sentences (≤ 12 words); keep 3–4 short pivots and let the rest carry a relation")
        if m["late_figure_refs"]:
            issues.append(("NOTE", 0, f"{name}: refers to figures/tables beyond Figure 1 / Table 1 ({m['late_figure_refs']}×); keep only if those figures exist in this paper (numbers copied from notes or an intake form usually do not)", ""))
        over("participle_tail_ratio", "share of sentences ending in a participial clause (', making …', ', extending …'); merge with because/while/by/which or end the sentence")
        over("hedge_count", "hedging words (may/could/suggest/…)")
        over("booster_count", "boosters (significantly/remarkably/…)")
        over("sentences", "sentences", "NOTE")
        over("words", "words", "NOTE")
        if m["sent_len_mean"] < d["sent_len_mean"]["p10"]:
            issues.append(("WARN", 0, f"{name}: mean sentence length {m['sent_len_mean']:.1f} words is below 90% of award papers (p10 = {d['sent_len_mean']['p10']:.1f}); merge bare-fact sentences so each carries a relation (cause, contrast, means)", ""))
        run_limit = 3 if sec == "intro" else 2
        if m["short_run_max"] >= run_limit:
            level = "WARN" if m["short_run_max"] >= 3 else "NOTE"
            issues.append((level, 0, f"{name}: {m['short_run_max']} consecutive sentences under 15 words (" + ("50 of 55 award introductions never have 3" if sec == "intro" else "49 of 55 award abstracts never have 2") + "); merge them", ""))
        if sec == "intro":
            for key, what in (("connector_per_100w", "logical connectors"),):
                if m[key] < d[key]["p10"]:
                    issues.append(("NOTE", 0, f"{name}: fewer {what} than 90% of award papers ({m[key]:.2f}); aim near the median ({d[key]['p50']}), not zero", ""))
        if sec == "abstract" and m["self_praise_count"] == 0:
            issues.append(("NOTE", 0, "abstract makes no evaluative claim (outperforms, first, efficient, …); add one that the evidence supports", ""))
        if sec == "abstract" and m["insight_formula_count"] >= 1:
            issues.append(("WARN", 0, "abstract uses a formula such as 'key insight'/'key idea' (4 of 55 award papers do this anywhere); state the insight directly", ""))
        if sec == "intro" and m["insight_formula_count"] >= 2:
            issues.append(("WARN", 0, f"introduction uses 'key insight'-type formulas {m['insight_formula_count']}×; use at most one, prefer stating the observation directly", ""))
        if sec == "intro" and m["self_praise_count"] < d["self_praise_count"]["p10"]:
            issues.append(("NOTE", 0, "introduction promotes the work less than 90% of award papers (no 'outperforms', 'efficient', 'first', …); state the strongest supported advantage confidently", ""))
    return issues


BODY_SKIP = {"disclaimer (move to Limitations)", "limitation in abstract/introduction", "future-work disclaimer",
             "defensive qualifier (move to experiments)", "core idea downgraded to a hypothesis"}


def line_kinds(path, n_lines):
    """Map 1-based line numbers to 'front' (abstract/introduction) or 'body' (method, experiments, …)."""
    raw = Path(path).read_text(encoding="utf-8")
    if path.endswith(".tex"):
        k = "body" if sm.file_kind(raw) == "body" else "front"
        return {i: k for i in range(1, n_lines + 2)}
    kinds, cur = {}, "front"
    for i, ln in enumerate(raw.splitlines(), 1):
        h = re.match(r"^#+\s*(?:\d+\.?\s*)?(.*)", ln)
        if h:
            cur = "front" if re.match(r"(abstract|introduction|title)", h.group(1), re.I) else "body"
        kinds[i] = cur
    return kinds


def check(path, bank, max_words):
    lines, labels = load_lines(path)
    kinds = line_kinds(path, len(lines))
    is_body_file = path.endswith(".tex") and kinds.get(1) == "body"
    issues = []
    issues += corpus_checks(path)
    raw = Path(path).read_text(encoding="utf-8")
    if path.endswith(".tex"):
        for m in re.finditer(r"(?<![\\\w])[A-Za-z]+(?<!\\)'[aeiou][a-z]+", raw):
            if not re.search(r"n't|'s\b|'re|'ve|'ll", m.group()):
                issues.append(("ERROR", 0, f"broken LaTeX accent '{m.group()}' (write e.g. Fr\\'echet)", ""))
    todos = len(re.findall(r"\[TODO|\\todo\{|\\TODO\{", raw))
    if todos:
        issues.append(("NOTE", 0, f"{todos} TODO placeholder(s) remain", ""))
    if labels and not is_body_file:
        issues.append(("ERROR", 0, f"{labels} bold paragraph label(s) in the abstract/introduction (run-in headings belong to method/experiments)", ""))
    sents = sentences(lines)
    for s, n in sents:
        low = s.lower()
        body = kinds.get(n, "front") == "body"
        for pat, why in ERROR_PHRASES.items():
            if re.search(pat, low) and not (body and why in BODY_SKIP):
                issues.append(("ERROR", n, why, s))
        if sm.colon_dash_hits(re.sub(r"\[TODO[^\]]*\]|\\todo\{[^}]*\}", "", s)):
            issues.append(("ERROR", n, "dash in the text (author preference: none); use a colon, a comma, a short second sentence or parentheses", s))
        if re.search(r"\balthough\b[^.]*,\s*but\b", low):
            issues.append(("ERROR", n, "'although … but'", s))
        if re.search(r"\bunlike [^,]+,\s*we\b", low):
            issues.append(("WARN", n, "'Unlike X, we' compares unlike things", s))
        for pat, why in WARN_PHRASES.items():
            if re.search(pat, s, flags=re.I):
                issues.append(("WARN", n, why, s))
        for pat, why in NOTE_PHRASES.items():
            if re.search(pat, s, flags=re.I):
                issues.append(("NOTE", n, why, s))
        if not body and re.search(COMPARE, low) and not re.search(r"\d|\[todo|\[c\]|tab\.|table|fig\.|figure", low):
            issues.append(("NOTE", n, "comparison without a number or table/figure reference (fine for mechanisms; results need evidence)", s))
        if not body and re.search(DETAIL, s, flags=re.I):
            issues.append(("WARN", n, "implementation detail in abstract/introduction", s))
        if len(s.split()) > max_words:
            issues.append(("WARN", n, f"long sentence ({len(s.split())} words)", s))
        ov = ngrams(s) & bank
        if ov:
            issues.append(("ERROR", n, f"copies exemplar wording: '{sorted(ov)[0]}'", s))
    paras = [p.strip() for p in "\n".join(lines).split("\n\n") if p.strip()]
    firsts = [w[0].lower() for w in (re.findall(r"[A-Za-z]+", p)[:1] for p in paras) if w]
    for w in set(firsts):
        if firsts.count(w) > 3 and w not in {"the", "a", "c"} and not is_body_file:
            issues.append(("WARN", 0, f"{firsts.count(w)} paragraphs start with '{w}'", ""))
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--max-words", type=int, default=60)
    a = ap.parse_args()
    bank = bank_ngrams()
    total_e = total_w = total_n = 0
    for f in a.files:
        issues = check(f, bank, a.max_words)
        print(f"== {f}")
        if not issues:
            print("OK: no issues found")
        order = {"ERROR": 0, "WARN": 1, "NOTE": 2}
        for level, n, msg, s in sorted(issues, key=lambda x: (order[x[0]], x[1])):
            print(f"{level:5s} line {n:>3}: {msg}")
            if s:
                print(f"           > {s[:160]}")
        total_e += sum(1 for i in issues if i[0] == "ERROR")
        total_w += sum(1 for i in issues if i[0] == "WARN")
        total_n += sum(1 for i in issues if i[0] == "NOTE")
    print(f"\n{total_e} error(s), {total_w} warning(s), {total_n} note(s)")
    return 1 if total_e else 0


if __name__ == "__main__":
    sys.exit(main())
