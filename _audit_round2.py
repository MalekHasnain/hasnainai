#!/usr/bin/env python3
"""Round 2: exact-line review, truncation detection, cross-page fact consistency."""
import re, os, html
from collections import defaultdict

ROOT = os.path.expanduser("~/jarvis/hasnainai")
PAGES = ["index.html", "concepts.html"] + [f"topics/{f}" for f in sorted(os.listdir(os.path.join(ROOT, "topics"))) if f.endswith(".html")]

def load(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()

def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def spans(text):
    out = []
    for m in re.finditer(r'<(h[1-4]|p|li|div|span|td|th|summary)[^>]*class="([^"]*)"[^>]*>', text):
        tag, cls = m.group(1), m.group(2).split()
        if not ("en" in cls or "ru" in cls): continue
        lang = "ru" if "ru" in cls else "en"
        close = re.compile(rf"</{tag}>").search(text, m.end())
        if not close: continue
        raw = text[m.end():close.start()]
        out.append((text.count("\n", 0, m.start()) + 1, lang, strip_tags(raw)))
    return out

# ---------- A. print exact lines of interest ----------
print("########## EXACT LINES ##########")
targets = {
 "concepts.html": [168, 179, 197],
 "topics/cnn.html": [78, 109],
 "topics/confusion-matrix.html": [101],
 "topics/dbscan.html": [64, 112, 294, 302],
 "topics/kmeans.html": [59, 100, 105, 161, 193, 203, 234, 277],
 "topics/multiple-regression.html": [75],
 "topics/pca.html": [63, 114, 130, 290],
 "topics/simple-linear-regression.html": [63, 70, 73, 76, 85, 98, 103, 197, 250, 278],
 "topics/logistic-regression.html": [59,60,61,62,63,64,65,66,91,92,154,155,277,278,279,280],
}
for page, lines in targets.items():
    txt = load(page).split("\n")
    print(f"\n===== {page} =====")
    for ln in lines:
        if ln <= len(txt):
            print(f"L{ln}: {txt[ln-1].strip()[:400]}")

# ---------- B. truncation: ru much shorter than en sibling ----------
print("\n\n########## TRUNCATION (ru < 45% of en, en>=120 chars) ##########")
for page in PAGES:
    sp = spans(load(page))
    i = 0
    while i < len(sp):
        if sp[i][1]=="en" and i+1<len(sp) and sp[i+1][1]=="ru" and sp[i+1][0]-sp[i][0]<=6:
            (le,_,e),(lr,_,r) = sp[i], sp[i+1]
            if len(e) >= 120 and len(r) < 0.45*len(e):
                print(f"{page} enL{le} ruL{lr} ratio={len(r)/len(e):.2f}")
                print(f"   EN({len(e)}): {e[:200]}")
                print(f"   RU({len(r)}): {r[:200]}")
            i += 2
        else: i += 1

# ---------- C. ru spans ending in double dot or abrupt ----------
print("\n\n########## RU ENDING '..' ##########")
for page in PAGES:
    for idx, line in enumerate(load(page).split("\n"), 1):
        if 'class="ru"' in line:
            plain = strip_tags(line)
            if plain.endswith("..") or "..\u2026" in plain or re.search(r"\.\.$", plain):
                print(f"{page} L{idx}: {plain[:160]}")

# ---------- D. cross-page facts ----------
print("\n\n########## CROSS-PAGE FACTS ##########")
facts = {
 "200 (mall customers)": r"\b200 (rows|customers|customers)",
 "k=5 / 5 clusters": r"\b5 clusters|k\s*=\s*5|elbow (points|at|is)? ?(at )?5|choose k=5",
 "VGG16 layers": r"\b13 convolutional|16 layers|138[ ,]?million|138M",
 "224": r"224",
 "1000 classes": r"1,?000 classes",
 "Titanic 891": r"891",
 "62%": r"62\s?%",
 "Iris 150": r"\b150\b",
 "income 15-137": r"15.{0,3}137|~15",
 "spending 1-99": r"1.{0,3}99",
 "CIFAR-10 / 10 classes": r"CIFAR|10 classes|ten classes",
}
for label, pat in facts.items():
    print(f"\n--- {label} ---")
    for page in PAGES:
        t = load(page)
        for m in re.finditer(pat, t, flags=re.I):
            ln = t.count("\n", 0, m.start())+1
            line = t.split("\n")[ln-1].strip()
            lang = "ru" if 'class="ru"' in line else ("en" if 'class="en"' in line else "-")
            print(f"  {page} L{ln} [{lang}]: {strip_tags(line)[:150]}")

# ---------- E. scan ALL pages for remaining jargon incl Urdu script ----------
print("\n\n########## JARGON FULL SCAN (ru spans) ##########")
JARGON = [r"jama", r"jame", r"tadaad", r"faasla", r"dhalwan", r"phelao", r"phaila", r"kaasir", r"kaseer",
          r"ilm[- ]e[- ]ashaar", r"meyaar", r"mayaar", r"chokor", r"\bjar\b", r"musallah", r"giroh",
          r"کندارہ", r"جمع", r"تعداد", r"فاصلہ", r"ڈھلوان", r"پھیل"]
for page in PAGES:
    t = load(page)
    for m in re.finditer(r'class="ru"', t):
        ln = t.count("\n", 0, m.start())+1
        line = t.split("\n")[ln-1]
        plain = strip_tags(line)
        hits = [j for j in JARGON if re.search(j, plain, flags=re.I)]
        if hits:
            print(f"{page} L{ln} hits={hits}: {plain[:170]}")
