#!/usr/bin/env python3
"""Map BBA search queries from the report to the 8 BBA landing pages.
CSV columns: Search query, Count, Variants merged, Normalized key (no impressions/clicks;
Count = search-term frequency). Outputs SEARCH-QUERIES-BBA.md + .csv."""
import csv, pathlib, collections
ROOT = pathlib.Path(__file__).parent
CSV = pathlib.Path(r"C:\Users\User\Downloads\Search terms - grouped by count.csv")

PAGES = [  # (page id, label, target query)
 ("bba-finance",          "BBA in Finance",          "bba in finance"),
 ("bba-digital-marketing","BBA in Digital Marketing","bba in digital marketing"),
 ("bba-admission",        "BBA Admission",           "bba admission"),
 ("bba-fees-reveal",      "BBA Fees (JAIN)",         "jain university bba fees structure"),
 ("bba-course-fees",      "BBA Course Fees",         "bba course fees"),
 ("bba-online",           "BBA Online (+ Online-Home)","online bba course / bba online course"),
 ("bba-course",           "BBA Course (generic)",    "bba course"),
 ("_other",               "Other BBA (not covered by these 8)", "-"),
]
LABEL = {p[0]: p[1] for p in PAGES}

def bucket(q):
    s = q.lower()
    if "finance" in s: return "bba-finance"
    if "digital marketing" in s or "digital-marketing" in s: return "bba-digital-marketing"
    if any(k in s for k in ("admission","how to apply","apply for","eligibil","eligible","last date","application","registration","how to join","how to get")): return "bba-admission"
    if any(k in s for k in ("fee","fees","cost","price","charges")):
        return "bba-fees-reveal" if "jain" in s else "bba-course-fees"
    if any(k in s for k in ("online","distance","correspondence","from home","work while","virtual")): return "bba-online"
    # off-topic specialisations / other intents we do NOT have a page for
    OTHER = ("aviation","logistics","supply","sports","event","hospital","health","aviation","tourism","travel",
             "banking","insurance","international business","entrepreneur","retail","media","fashion","real estate",
             "salary","scope","jobs","after bba","best","top","rating","ranking","review","vs ","subjects",
             "syllabus","duration","distance","part time","correspondence","govt","government")
    if any(k in s for k in OTHER): return "_other"
    return "bba-course"  # generic: bba, bba course, bba degree, bba program, do bba, etc.

rows = collections.defaultdict(list)   # page -> [(query, count)]
total = 0
with open(CSV, encoding="utf-8-sig", newline="") as f:
    r = csv.reader(f)
    next(r, None)
    for row in r:
        if len(row) < 2: continue
        q = row[0].strip()
        try: c = int(row[1])
        except ValueError: continue
        if "bba" not in q.lower(): continue
        total += c
        rows[bucket(q)].append((q, c))

# write full CSV + markdown
out_csv = ROOT / "SEARCH-QUERIES-BBA.csv"
with open(out_csv, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(["page", "target_query", "search_query", "count", "pct_of_bba"])
    for pid, label, tq in PAGES:
        for q, c in sorted(rows.get(pid, []), key=lambda x: -x[1]):
            w.writerow([label, tq, q, c, f"{c/total*100:.3f}"])

md = [f"# BBA search queries mapped to the 8 landing pages",
      "",
      f"Source: `Search terms - grouped by count.csv` (column **Count** = search-term frequency; "
      f"no impressions/clicks columns exist in this file). **% = share of total BBA demand.**",
      f"Total BBA search count across all BBA queries: **{total:,}**.",
      ""]
grand = 0
summary = []
for pid, label, tq in PAGES:
    items = sorted(rows.get(pid, []), key=lambda x: -x[1])
    sub = sum(c for _, c in items)
    grand += sub
    summary.append((label, tq, len(items), sub))
md += ["## Demand summary per page", "",
       "| Page | Target query | #queries | Total count | % of BBA demand |",
       "|------|--------------|---------:|------------:|----------------:|"]
for label, tq, n, sub in summary:
    md.append(f"| {label} | `{tq}` | {n:,} | {sub:,} | {sub/total*100:.1f}% |")
md += ["", "---", ""]
for pid, label, tq in PAGES:
    items = sorted(rows.get(pid, []), key=lambda x: -x[1])
    sub = sum(c for _, c in items)
    md += [f"## {label}  ({sub:,} = {sub/total*100:.1f}% of BBA demand, {len(items):,} queries)",
           f"Target query: `{tq}`", "",
           "| # | Search query | Count | % of BBA |", "|--:|--------------|------:|---------:|"]
    for i, (q, c) in enumerate(items[:25], 1):
        md.append(f"| {i} | {q} | {c:,} | {c/total*100:.3f}% |")
    if len(items) > 25:
        md.append(f"| | *...+{len(items)-25:,} more (see SEARCH-QUERIES-BBA.csv)* | | |")
    md += [""]
(ROOT / "SEARCH-QUERIES-BBA.md").write_text("\n".join(md), encoding="utf-8")

print(f"total BBA count: {total:,}")
for label, tq, n, sub in summary:
    print(f"  {label:34} {n:5,} queries  {sub:8,}  {sub/total*100:5.1f}%")
print(f"\nwrote SEARCH-QUERIES-BBA.md and .csv")
