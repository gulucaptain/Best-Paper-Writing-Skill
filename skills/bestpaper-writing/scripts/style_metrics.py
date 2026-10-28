#!/usr/bin/env python3
"""Style metrics with the same definitions used for the 55-paper corpus profile
(references/corpus/corpus_stats.json). Stdlib only.

Usage: python3 scripts/style_metrics.py FILE [FILE ...]   (.tex or .md)
Prints each metric for the abstract/introduction with the corpus percentile band.
"""
import json, re, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATS = ROOT / "references/corpus/corpus_stats.json"
CONNECTORS = ['however', 'therefore', 'thus', 'hence', 'consequently', 'moreover', 'furthermore', 'additionally',
              'in addition', 'yet', 'nevertheless', 'nonetheless', 'whereas', 'while', 'in contrast', 'instead',
              'rather', 'unlike', 'accordingly', 'as a result', 'to this end', 'on the other hand', 'specifically',
              'in particular', 'more specifically', 'as such', 'importantly', 'finally', 'to summarize']
HEDGES = ['may', 'might', 'could', 'likely', 'possibly', 'suggest', 'suggests', 'appear to', 'appears to',
          'seem to', 'seems to', 'potentially']
BOOSTERS = ['significantly', 'substantially', 'dramatically', 'remarkably', 'notably', 'surprisingly',
            'strikingly', 'drastically', 'considerably', 'greatly']
PRAISE = ['novel', 'effective', 'efficient', 'powerful', 'superior', 'state-of-the-art', 'SOTA', 'outperform',
          'outperforms', 'first']
INSIGHTS = ['key insight', 'central insight', 'core insight', 'key idea', 'key observation', 'central observation',
            'main insight', 'our insight']
CITE = re.compile(r'\[(?:\s*\d+[a-z]?\s*[,;–—-]?)+\]|\[c\]')
WORD = re.compile(r"[^\W_]+(?:[-’'/.,][^\W_]+)*(?:%|×)?", re.UNICODE)
REF = re.compile(r'\b(?:Figures?|Figs?\.?|Tables?|Tabs?\.?|Sections?|Secs?\.?|Eqs?\.?|Equations?)\s*\(?\d+(?:\.\d+)*\)?', re.I)
NUM = re.compile(r'(?<![\w])\d+(?:,\d{3})*(?:\.\d+)?(?:/\d+(?:\.\d+)?)?(?:%|×)?')


def phrase_matches(t, phrases):
    pat = r'(?<!\w)(?:' + '|'.join(re.escape(x) for x in sorted(phrases, key=len, reverse=True)) + r')(?!\w)'
    return list(re.finditer(pat, t, re.I))


def words(t):
    return WORD.findall(CITE.sub('', t))


def split_sentences(p):
    prot = p
    for pat in [r'\b(?:e\.g\.|i\.e\.|w\.r\.t\.|i\.i\.d\.)', r'\bet al\.', r'\b(?:Fig|Figs|Tab|Eq|Eqs|Sec|cf|vs|etc|resp|approx)\.', r'(?<=\d)\.(?=\d)']:
        prot = re.sub(pat, lambda m: m.group().replace('.', '\uE000'), prot, flags=re.I)
    out, start = [], 0
    for m in re.finditer(r'[.!?][”’"\)\]]*(?=\s|$)', prot):
        out.append(p[start:m.end()].strip()); start = m.end()
    if p[start:].strip():
        out.append(p[start:].strip())
    return [s for s in out if s]


def number_tokens(t):
    t = CITE.sub(' ', t)
    t = re.sub(r'\([^)]*\)', lambda m: re.sub(r'\b(?:19|20)\d{2}\b', ' ', m.group()), t)
    t = REF.sub(' ', t)
    t = re.sub(r'\b[A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z0-9]+)*\b', lambda m: ' ' if any(c.isdigit() for c in m.group()) else m.group(), t)
    t = re.sub(r'\b\d+([A-Za-z][A-Za-z0-9-]*)\b', lambda m: m.group() if m.group(1) in {'Hz', 'kHz', 'MHz', 'GHz', 'fps', 's', 'ms', 'cm', 'mm', 'k', 'M', 'B', 'x'} else ' ', t)
    return NUM.findall(t)


def connector_hits(s):
    hits = []
    for m in phrase_matches(s, CONNECTORS):
        if m.group().lower() == 'while':
            # contrastive 'while' (sentence-initial or after a comma); temporal uses are not counted
            before = s[:m.start()].rstrip()
            if before and not before.endswith(','):
                continue
        hits.append(m)
    return hits


def metric(paras):
    ss = [s for p in paras for s in split_sentences(p)]
    lens = [len(words(s)) for s in ss]
    w = max(sum(lens), 1)
    conn = [connector_hits(s) for s in ss]
    out = {
        'words': sum(lens), 'sentences': len(ss), 'prose_paragraphs': sum(not p.startswith('•') for p in paras),
        'sent_len_mean': statistics.mean(lens) if lens else 0,
        'short_sent_ratio': sum(x <= 12 for x in lens) / max(len(ss), 1),
        'numbers': sum(len(number_tokens(s)) for s in ss),
        'connector_per_100w': sum(len(c) for c in conn) / w * 100,
        'connector_sentence_start_ratio': sum(any(m.start() == 0 for m in c) for c in conn) / max(len(ss), 1),
        'colon_or_dash_sentences': sum(bool(re.search(r'(?<![\d/]):(?![/\d])|—|\s[–-]\s', s)) for s in ss) / max(len(ss), 1),
        'hedge_count': sum(len(phrase_matches(s, HEDGES)) for s in ss),
        'booster_count': sum(len(phrase_matches(s, BOOSTERS)) for s in ss),
        'self_praise_count': sum(len(phrase_matches(s, PRAISE)) for s in ss),
        'insight_formula_count': sum(len(phrase_matches(s, INSIGHTS)) for s in ss),
        'we_sentence_ratio': sum(bool(re.match(r'["“(]?(We|Our)\b', s)) for s in ss) / max(len(ss), 1),
        'question_sentences': sum(s.rstrip('”’")]').endswith('?') for s in ss),
        'short_run_max': short_run_max(paras),
        'participle_tail_ratio': participle_tail_ratio(ss),
        'antithesis_ratio': sum(bool(ANTI.search(x)) for x in ss) / max(len(ss), 1),
        'late_figure_refs': sum(len(LATEFIG.findall(x)) for x in ss),
        'colon_dash_count': sum(len(colon_dash_hits(x)) for x in ss),
    }
    return out, ss


# trailing participial clause: ", making …", ", extending …" (excludes prepositional -ing words)
PART = re.compile(r',\s+(?:thereby\s+)?(?!during|including|according|following|using|regarding|concerning|excluding|notwithstanding)[a-z]{3,}ing\b')
# punctuation dash in prose: em dash, spaced en dash or spaced hyphen (colons are allowed)
PUNCT = re.compile(r'—|\s[–-]\s')


# aphoristic contrast: "X is not Y", "not yet", "not the same as", "rather than", "instead of", "need not"
ANTI = re.compile(r"\b(?:is|are|does|do|was|were) not\b|\bnot yet\b|\bnot the same\b|\brather than\b|\binstead of\b|\bneed not\b|\bisn't\b|\baren't\b")
# references to figures/tables other than Figure 1 / Table 1
LATEFIG = re.compile(r"\b(?:Fig(?:ure)?s?\.?|Tab(?:le)?s?\.?)\s*~?(?:[2-9]|\d{2,})\b")


def participle_tail_ratio(ss):
    return sum(bool(PART.search(x)) for x in ss) / max(len(ss), 1)


def colon_dash_hits(s):
    return PUNCT.findall(s)


def short_run_max(paras, th=15):
    """Longest run of consecutive sentences under `th` words within a prose paragraph."""
    best = 0
    for p in paras:
        if p.startswith('•'):
            continue
        cur = 0
        for x in split_sentences(p):
            cur = cur + 1 if len(words(x)) < th else 0
            best = max(best, cur)
    return best


def clean_tex(t):
    t = re.sub(r'(?<!\\)%.*', '', t)
    t = re.sub(r'\\todo\{(?:[^{}]|\{[^{}]*\})*\}', ' ', t)
    t = re.sub(r'\[TODO[^\]]*\]', ' ', t)
    t = re.sub(r'\\(?:section|subsection|label|begin|end)\*?\{[^{}]*\}', '', t)
    t = re.sub(r'\\cite[tp]?\*?(\[[^\]]*\])?\{[^}]*\}', '[c]', t)
    t = re.sub(r'(?:Fig|Tab|Sec|Eq)\.?~?\\ref\{[^}]*\}', 'Figure 1', t)
    t = re.sub(r'\\item\s*', '\n\n• ', t)
    t = t.replace('---', '—').replace('--', '–').replace('``', '“').replace("''", '”').replace('~', ' ').replace('\\times', '×')
    t = re.sub(r'\\(?:textbf|textit|emph|mathrm|text)\{([^{}]*)\}', r'\1', t)
    t = re.sub(r'\\[A-Za-z]+\*?', '', t).replace('{', '').replace('}', '').replace('$', '')
    return t


def file_kind(raw):
    """Kind of a .tex section file: 'abstract', 'intro' or 'body' (method, experiments, …)."""
    if '\\begin{abstract}' in raw:
        return 'abstract'
    m = re.search(r'\\section\*?\{([^}]*)\}', raw)
    if m is None or re.match(r'\s*introduction', m.group(1), re.I):
        return 'intro'
    return 'body'


def sections(path):
    """Return {'abstract': [paragraphs], 'intro': [paragraphs]} from a .tex or .md file."""
    raw = Path(path).read_text(encoding='utf-8')
    secs = {}
    if str(path).endswith('.tex'):
        kind = file_kind(raw)
        if kind != 'body':
            secs[kind] = clean_tex(raw)
    else:
        cur = None
        for ln in raw.splitlines():
            h = re.match(r'^#+\s*(?:\d+\.?\s*)?(abstract|introduction)', ln, re.I)
            if h:
                cur = 'abstract' if h.group(1).lower() == 'abstract' else 'intro'; secs[cur] = ''; continue
            if re.match(r'^#+\s', ln):
                cur = None
            if cur:
                secs[cur] += re.sub(r'^\s*[-*]\s+', '\n\n• ', ln) + '\n'
        secs = {k: re.sub(r'\[TODO[^\]]*\]', ' ', v) for k, v in secs.items()}
    return {k: [' '.join(p.split()) for p in v.split('\n\n') if p.strip()] for k, v in secs.items()}


def load_stats():
    return json.loads(STATS.read_text(encoding='utf-8'))


def band(value, d):
    for p in (10, 25, 50, 75, 90):
        if value <= d[f'p{p}']:
            return f'<=p{p}'
    return '>p90'


def main():
    stats = load_stats()['style']
    for f in sys.argv[1:]:
        for sec, paras in sections(f).items():
            m, _ = metric(paras)
            print(f'== {f} [{sec}]')
            for k, v in m.items():
                d = stats[sec].get(k)
                extra = f"  corpus p10/p50/p90 = {d['p10']}/{d['p50']}/{d['p90']}  ({band(v, d)})" if d else ''
                print(f'  {k:32s} {v:8.3f}{extra}')


if __name__ == '__main__':
    main()
