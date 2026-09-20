#!/usr/bin/env python3
"""Consistency & bilingual quality audit for ~/jarvis/hasnainai (12 pages). READ-ONLY."""
import re, os, json, html
from collections import defaultdict

ROOT = os.path.expanduser("~/jarvis/hasnainai")
PAGES = ["index.html", "concepts.html"] + [
    f"topics/{f}" for f in sorted(os.listdir(os.path.join(ROOT, "topics"))) if f.endswith(".html")
]

MUST_EN = ["mean","median","sum","count","square root","square","distance","slope","spread",
           "outlier","gradient","matrix","eigenvector","eigenvalue","variance","standard deviation",
           "probability","cluster","centroid","layer","filter","neuron","epoch","training","prediction"]

# Urdu/Roman-Urdu equivalents that indicate the term was translated (must stay English)
URDU_JARGON = {
    r"\bjama\b|جمع": "sum",
    r"\btadaad\b|تعداد": "count",
    r"\bfaasla\b|فاصلہ|فاصلہ": "distance",
    r"\bdhalwan\b|ڈھلوان": "slope",
    r"\bphelao\b|\bphaila?\s?hua\b|\bphaila?o?n?d?ay? hun?e\b|پھیلاؤ|پھیلا": "spread",
    r"\bkaseer\b": "matrix(?) — translated jargon",
    r"\bilm[- ]e[- ]ashaar\b|علم اعداد": "mathematics/numbers — translated jargon",
    r"\bmeyaar\b|\bmayaar\b": "mean/standard(?) — translated jargon",
    r"\bhisaab\s?kitaab\b": "calculation — translated jargon",
    r"\bmusallah\s?zaviya\b": "right angle — translated jargon",
    r"\bchokor\s?jama\b": "square — translated jargon",
    r"\bjar\b|جذر": "square root — translated jargon",
    r"\bkashif\s?makhrouti\b": "eigenvector(?) — translated jargon",
    r"\bginti\b": "count — translated jargon",
    r"\bmila\s?kar\b": "sum(?) — translated jargon",
    r"\bkhoobsurti\b": "(nonsense filler?)",
}

PLACEHOLDER_PATTERNS = [
    (r"TODO|FIXME|TBD|XXX|lorem ipsum|Lorem ipsum|PLACEHOLDER|placeholder text", "placeholder marker"),
    (r"\?\?\s*$", "double question mark ending"),
    (r"[a-z)]\s*\.\.(?!\.)", "double-dot '..' mid/ending (half-finished?)"),
    (r"\.\.\s*<|…\s*<", "ellipsis right before tag close (truncated sentence)"),
    (r"\b(wing|weight)\s+it\b|\bto\s+be\s+(filled|added|written)\b|\baa\s+raha\s+hai\s+soon\b", "unfinished note"),
    (r"^\s*$", "empty"),
]

def load(page):
    with open(os.path.join(ROOT, page), encoding="utf-8") as f:
        return f.read()

def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()

def spans(text):
    """Yield (line_no, class(en/ru/other), tag, raw, plain) for en/ru spans in doc order."""
    out = []
    for m in re.finditer(r'<(h[1-4]|p|li|div|span|td|th|summary|button)[^>]*class="([^"]*)"[^>]*>', text):
        # only handle non-self-closing simple tags; capture until matching close of same tag (flat, no nesting of same tag)
        tag, cls = m.group(1), m.group(2)
        classes = cls.split()
        if not any(c in ("en","ru") for c in classes): continue
        lang = "ru" if "ru" in classes else "en"
        start = m.end()
        close = re.compile(rf"</{tag}>").search(text, start)
        if not close: continue
        raw = text[start:close.start()]
        # line number of the opening tag
        line = text.count("\n", 0, m.start()) + 1
        out.append((line, lang, tag, raw, strip_tags(raw)))
    return out

report = {}          # page -> list of issues (dict)
def flag(page, line, quote, why):
    report.setdefault(page, []).append({"line": line, "quote": quote[:300], "why": why})

def nums_in(s):
    # numbers incl decimals, %, k=5 style; ignore pure small ordinals in urls
    s = re.sub(r"href=\"[^\"]*\"", " ", s)
    return sorted(set(re.findall(r"\d+(?:\.\d+)?%?", s)))

all_pages = {}
for page in PAGES:
    text = load(page)
    all_pages[page] = text
    sp = spans(text)
    # ---- 1. Urdu jargon inside ru spans ----
    for line, lang, tag, raw, plain in sp:
        if lang != "ru": continue
        for pat, meaning in URDU_JARGON.items():
            m = re.search(pat, plain, flags=re.I)
            if m:
                flag(page, line, plain, f"ru translates technical term into Urdu: '{m.group(0)}' (~{meaning}); term must stay English")
    # ---- MUST-EN terms present in en sibling missing from ru sibling (pairwise) ----
    pairs = []
    i = 0
    while i < len(sp):
        if sp[i][1] == "en" and i + 1 < len(sp) and sp[i+1][1] == "ru" and abs(sp[i][0]-sp[i+1][0]) <= 6:
            pairs.append((sp[i], sp[i+1])); i += 2
        else:
            i += 1
    for (le, te, _, _, en_p), (lr, _, _, _, ru_p) in pairs:
        en_low, ru_low = en_p.lower(), ru_p.lower()
        for term in MUST_EN:
            if re.search(rf"\b{re.escape(term)}\b", en_low) and not re.search(rf"\b{re.escape(term)}\b", ru_low):
                # check a known Urdu translation exists -> strong signal; else ru may just omit
                urdu_hit = [p for p,_ in URDU_JARGON.items() if re.search(p, ru_low, flags=re.I)]
                if urdu_hit:
                    flag(page, lr, ru_p, f"en sibling uses '{term}' but ru replaces it with Urdu (pair at line {le})")
    # ---- 2. number mismatch between en/ru pair ----
    for (le, te, _, _, en_p), (lr, _, _, _, ru_p) in pairs:
        ne, nr = nums_in(en_p), nums_in(ru_p)
        if ne != nr and ne and (nr or True):
            missing = [x for x in ne if x not in nr]
            extra = [x for x in nr if x not in ne]
            if missing or extra:
                flag(page, lr, f"EN: {en_p[:160]} || RU: {ru_p[:160]}",
                     f"number mismatch in en/ru pair (en line {le}): en={ne} ru={nr}; missing_in_ru={missing}, extra_in_ru={extra}")

    # ---- 5. placeholders / unfinished ----
    for line_no, line_txt in enumerate(text.split("\n"), 1):
        if re.search(r"class=\"(en|ru)\"", line_txt):
            for pat, why in PLACEHOLDER_PATTERNS:
                if pat in ("^\s*$",): continue
                if re.search(pat, line_txt):
                    # avoid flagging legit ellipsis "…" used stylistically at end? still list for review
                    flag(page, line_no, strip_tags(line_txt)[:200], f"possible unfinished text: {why}")
    # empty en/ru spans
    for line, lang, tag, raw, plain in sp:
        if not plain:
            flag(page, line, raw[:80], f"empty {lang} span")

    # unpaired ru (ru without preceding en)
    for idx, (line, lang, *_ ) in enumerate(sp):
        if lang == "ru" and not (idx > 0 and sp[idx-1][1] == "en" and abs(sp[idx-1][0]-line) <= 6):
            flag(page, line, sp[idx][4][:150], "ru span not directly paired with an en sibling (order/structure)")

json.dump({"pages": {p: report.get(p, []) for p in PAGES}}, open(os.path.expanduser("~/jarvis/hasnainai/_audit_out.json"), "w"), indent=1)
print(f"pages={len(PAGES)} total_flagged={sum(len(v) for v in report.values())}")
for p in PAGES:
    print(f"--- {p}: {len(report.get(p, []))} raw flags")
