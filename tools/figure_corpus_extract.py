"""Extract figure and table captions from award-paper PDFs (used to build data/figure_stats.json).

Usage: python3 tools/figure_corpus_extract.py <dir with P01.pdf ...> <out.json>
PDFs are not part of this repository; download them yourself (arXiv versions were used, 44 of 55 corpus papers).
Captions are kept only in your local output file; the repository stores aggregate numbers only.
"""
import sys, re, json, glob, os, warnings
warnings.filterwarnings("ignore")
import pymupdf as fitz
CAP = re.compile(r'^\s*(Figure|Fig\.|Table)\s*(\d+)\s*[:.|]\s*', re.I)
def block_text(b):
    return " ".join("".join(s["text"] for s in l["spans"]) for l in b["lines"])
def spans(b): return [s for l in b["lines"] for s in l["spans"]]
def is_bold(s): return bool(s["flags"] & 16) or bool(re.search(r'bold|black|semibold|medi|\.B$|CMBX', s["font"], re.I))
res = {}
for pdf in sorted(glob.glob(sys.argv[1] + "/*.pdf")):
    pid = os.path.basename(pdf)[:-4]
    doc = fitz.open(pdf)
    ref_page = len(doc)
    pages = []
    for i, p in enumerate(doc):
        d = p.get_text("dict"); pages.append(d)
        if i >= 3 and ref_page == len(doc):
            for b in d["blocks"]:
                if b["type"] == 0 and re.fullmatch(r'\s*(\d+\s*)?(References|REFERENCES|Bibliography)\s*', block_text(b)):
                    ref_page = i; break
    W = doc[0].rect.width
    caps = {}; abstract_y = None
    for i in range(min(ref_page + 1, len(doc))):
        for b in pages[i]["blocks"]:
            if b["type"] != 0: continue
            t = block_text(b)
            if i == 0 and abstract_y is None and re.match(r'\s*Abstract\b', t): abstract_y = b["bbox"][1]
            if i == ref_page and abstract_y is not None: pass
            m = CAP.match(t)
            if not m: continue
            kind = "table" if m.group(1).lower().startswith("tab") else "figure"
            key = (kind, int(m.group(2)))
            if key in caps: continue
            body = t[m.end():].strip()
            if len(body.split()) < 3: continue
            sp = [s for s in spans(b) if s["text"].strip()]
            # first span after the label
            acc = ""; title_bold = False
            for s in sp:
                if len(acc) >= m.end() - 1:
                    title_bold = is_bold(s) and len(s["text"].strip()) >= 3; break
                acc += s["text"]
            first_sent = re.split(r'(?<=[.!?])\s+', body)[0]
            caps[key] = dict(kind=kind, num=key[1], page=i, y=b["bbox"][1] / pages[i]["height"],
                             width=(b["bbox"][2] - b["bbox"][0]) / W, words=len(body.split()),
                             first_sentence_words=len(first_sent.split()), title_bold=title_bold,
                             in_main=i < ref_page, text=body[:400])
    # two-column detection: share of text blocks narrower than 0.5 page width on page 2
    p = pages[min(1, len(pages) - 1)]
    tb = [b for b in p["blocks"] if b["type"] == 0 and len(block_text(b)) > 200]
    twocol = sum((b["bbox"][2] - b["bbox"][0]) / W < 0.5 for b in tb) > len(tb) / 2 if tb else None
    res[pid] = dict(pages=len(doc), main_pages=ref_page, twocol=twocol, abstract_y=abstract_y / pages[0]["height"] if abstract_y else None,
                    captions=[dict(v) for k, v in sorted(caps.items())])
json.dump(res, open(sys.argv[2], "w"), indent=1)
print(len(res), "papers")
