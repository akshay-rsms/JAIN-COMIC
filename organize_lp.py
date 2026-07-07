#!/usr/bin/env python3
"""Arrange the 50 self-contained landing pages into a Google-Ads-ready tree:
  landing-pages/<program>/<file>.html   (deployable final-URL pages, one per ad target)
and write GOOGLE-ADS-INDEX.md mapping every page -> target search query + demand.
Source of truth: stories/*.json (program, target query) + ALL-50-LP-SUMMARY.csv (demand)."""
import json, csv, shutil, pathlib
ROOT = pathlib.Path(__file__).parent
SHARE = ROOT / "share"; STORIES = ROOT / "stories"
LP = ROOT / "landing-pages"

PROG_DIR = {"MBA":"mba","BBA":"bba","MCA":"mca","B.Com":"b-com","M.Com":"m-com",
            "MA":"ma","BCA":"bca","JAIN":"brand"}
PROG_TITLE = {"mba":"MBA (Master of Business Administration)","bba":"BBA (Bachelor of Business Administration)",
              "mca":"MCA (Master of Computer Applications)","b-com":"B.Com (Bachelor of Commerce)",
              "m-com":"M.Com (Master of Commerce)","ma":"MA (Master of Arts)",
              "bca":"BCA (Bachelor of Computer Applications)","brand":"JAIN University (brand / all programmes)"}
PROG_ORDER = ["mba","brand","bba","mca","b-com","m-com","bca","ma"]

ACR = {"bba","mba","mca","bca","ma","hr","it","ai","acca"}
SPECIAL = {"bcom":"BCom","mcom":"MCom","jain":"University"}
def share_name(sid):
    NAME = {"bba-fees-reveal":"JAIN-BBA-01-Fees.html","bba-online":"JAIN-BBA-Online.html"}
    if sid in NAME: return NAME[sid]
    parts=[SPECIAL.get(p, p.upper() if p in ACR else p.title()) for p in sid.split("-")]
    return "JAIN-"+"-".join(parts)+".html"

# demand from the 50-page summary
demand = {}
with open(ROOT/"ALL-50-LP-SUMMARY.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("Page"): demand[r["Page"]] = r
# registry from stories
pages = []
for jf in STORIES.glob("*.json"):
    s = json.loads(jf.read_text(encoding="utf-8"))
    if "id" not in s or s.get("program") not in PROG_DIR: continue
    if not (SHARE/share_name(s["id"])).exists(): continue
    pages.append(s)

# build tree
if LP.exists(): shutil.rmtree(LP)
LP.mkdir()
by_prog = {}
for s in pages:
    d = PROG_DIR[s["program"]]; (LP/d).mkdir(exist_ok=True)
    fn = share_name(s["id"])
    shutil.copy(SHARE/fn, LP/d/fn)
    by_prog.setdefault(d, []).append((s, fn))

def imp(sid):
    try: return int(demand.get(sid,{}).get("Impressions",0))
    except: return 0

# index markdown
md = ["# JAIN Online - 50 Landing Pages (Google Ads index)", "",
      "Each page is a self-contained HTML file (all fonts & images embedded, works offline). "
      "Use the **Target search query** as the ad group / keyword theme and the file as the **Final URL**.",
      "", "Demand = Google Ads Search terms, all-time (~4 years).", "",
      "| # | Programme | Page (file) | Target search query | Impressions | Clicks | CTR |",
      "|--:|-----------|-------------|---------------------|------------:|-------:|----:|"]
i = 0
for d in PROG_ORDER:
    for s, fn in sorted(by_prog.get(d, []), key=lambda x:-imp(x[0]["id"])):
        i += 1; row = demand.get(s["id"], {})
        md.append(f"| {i} | {d.upper().replace('-','.')} | `{d}/{fn}` | {s.get('target_query', row.get('Target query',''))} | "
                  f"{int(row.get('Impressions',0)):,} | {int(row.get('Clicks',0)):,} | {row.get('CTR %','')}% |")
md += ["", "## Folders", ""]
for d in PROG_ORDER:
    md.append(f"- **`landing-pages/{d}/`** - {PROG_TITLE[d]} ({len(by_prog.get(d,[]))} pages)")
md += ["", "Full per-query mapping: `ALL-50-LP-SUMMARY.csv` (50-page rollup) and "
       "`SEARCH-QUERIES-ALL-50.csv` (every query -> page)."]
(ROOT/"GOOGLE-ADS-INDEX.md").write_text("\n".join(md), encoding="utf-8")

print(f"arranged {len(pages)} pages into landing-pages/ across {len(by_prog)} programmes")
for d in PROG_ORDER:
    print(f"  {d:<7} {len(by_prog.get(d,[])):>2} pages")
print("wrote GOOGLE-ADS-INDEX.md")
