#!/usr/bin/env python3
"""Build the Vercel deploy root web/ with clean, ad-friendly URLs:
   web/<programme>/<slug>.html   ->   /mba/finance , /bba/course , /jain/online ...
plus web/index.html (hub) and vercel.json (cleanUrls). Source = share/*.html + stories/*.json."""
import json, csv, shutil, pathlib, html
ROOT = pathlib.Path(__file__).parent
SHARE = ROOT/"share"; STORIES = ROOT/"stories"; WEB = ROOT/"web"
PREFIX = ["mba-","bba-","mca-","bcom-","mcom-","bca-","ma-","jain-"]
FOLDER = {"mba":"mba","bba":"bba","mca":"mca","bcom":"bcom","mcom":"mcom","bca":"bca","ma":"ma","jain":"jain"}
PTITLE = {"mba":"MBA","bba":"BBA","mca":"MCA","bcom":"B.Com","mcom":"M.Com","bca":"BCA","ma":"MA","jain":"JAIN University"}
PORDER = ["mba","jain","bba","mca","bcom","mcom","bca","ma"]

ACR={"bba","mba","mca","bca","ma","hr","it","ai","acca"}; SPECIAL={"bcom":"BCom","mcom":"MCom","jain":"University"}
def share_name(sid):
    NAME={"bba-fees-reveal":"JAIN-BBA-01-Fees.html","bba-online":"JAIN-BBA-Online.html"}
    if sid in NAME: return NAME[sid]
    return "JAIN-"+"-".join(SPECIAL.get(p,p.upper() if p in ACR else p.title()) for p in sid.split("-"))+".html"

def split(sid):
    for pre in PREFIX:
        if sid.startswith(pre):
            return pre[:-1], sid[len(pre):]
    return None, sid

demand={}
with open(ROOT/"ALL-50-LP-SUMMARY.csv",encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r.get("Page"): demand[r["Page"]]=r

pages=[]
for jf in STORIES.glob("*.json"):
    s=json.loads(jf.read_text(encoding="utf-8"))
    if "id" not in s: continue
    prog,slug=split(s["id"])
    if prog is None or not (SHARE/share_name(s["id"])).exists(): continue
    pages.append((prog,slug,s))

if WEB.exists(): shutil.rmtree(WEB)
WEB.mkdir()
for prog,slug,s in pages:
    (WEB/prog).mkdir(exist_ok=True)
    shutil.copy(SHARE/share_name(s["id"]), WEB/prog/f"{slug}.html")

# hub index
def imp(sid):
    try: return int(demand.get(sid,{}).get("Impressions",0))
    except: return 0
by=lambda p:[x for x in pages if x[0]==p]
cards=[]
for prog in PORDER:
    rows=sorted(by(prog),key=lambda x:-imp(x[2]["id"]))
    if not rows: continue
    lis="".join(
        f'<li><a href="/{prog}/{slug}"><span class="q">{html.escape(s.get("target_query",slug))}</span>'
        f'<span class="m">{imp(s["id"]):,} impr</span></a></li>' for prog2,slug,s in [(p,sl,st) for p,sl,st in rows])
    cards.append(f'<section class="prog"><h2>{PTITLE[prog]} <span>({len(rows)})</span></h2><ul>{lis}</ul></section>')
INDEX=f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>JAIN Online - 50 Landing Pages</title>
<style>
:root{{--navy:#1a237e;--gold:#f5b301;--paper:#fdf3da;--ink:#111}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,system-ui,Segoe UI,Roboto,sans-serif;background:var(--paper);color:var(--ink);line-height:1.5}}
header{{background:var(--navy);color:#fff;padding:34px 20px;border-bottom:5px solid #000;text-align:center}}
header h1{{font-size:30px;letter-spacing:.5px}} header p{{opacity:.85;margin-top:8px;font-size:14px}}
.wrap{{max-width:1100px;margin:0 auto;padding:24px 16px 60px}}
.prog{{background:#fff;border:3px solid #000;box-shadow:6px 6px 0 #0002;margin:18px 0;padding:16px 18px}}
.prog h2{{font-size:20px;color:var(--navy);border-bottom:3px solid var(--gold);padding-bottom:8px;margin-bottom:10px}}
.prog h2 span{{color:#999;font-size:14px}}
.prog ul{{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:8px}}
.prog a{{display:flex;justify-content:space-between;gap:10px;text-decoration:none;color:var(--ink);
  border:2px solid #000;border-radius:8px;padding:9px 12px;background:#fffdf6;font-size:13.5px;transition:background .12s}}
.prog a:hover{{background:var(--gold)}} .prog .q{{font-weight:700}} .prog .m{{color:#5a4a00;font-size:12px;white-space:nowrap}}
footer{{text-align:center;color:#5a4a00;font-size:12px;padding:20px}}
</style></head><body>
<header><h1>JAIN Online - 50 Landing Pages</h1><p>Comic-style landing pages, one per Google Ads search theme. Every CTA opens the Sensei chat counsellor.</p></header>
<div class="wrap">{''.join(cards)}</div>
<footer>Built from live AMS/UMS programmes + Google Ads search demand. Fees verified from PMS.</footer>
</body></html>"""
(WEB/"index.html").write_text(INDEX,encoding="utf-8")
(WEB/"vercel.json").write_text(json.dumps({"cleanUrls":True,"trailingSlash":False}, indent=2),encoding="utf-8")

# GOOGLE-ADS-INDEX.md: every page -> target search query + clean URL + demand
import os
DOMAIN = os.environ.get("LP_DOMAIN", "").rstrip("/")   # e.g. https://jain-online-lp.vercel.app
def url(prog, slug): return f"{DOMAIN}/{prog}/{slug}" if DOMAIN else f"/{prog}/{slug}"
md=["# JAIN Online - 50 Landing Pages (Google Ads index)","",
    (f"Live site: **{DOMAIN}**  " if DOMAIN else "")+"Each page is a Google Ads Final URL. "
    "Use the **Target search query** as the ad group / keyword theme. Every CTA opens the Sensei chat counsellor.","",
    "Demand = Google Ads Search terms, all-time (~4 years).","",
    "| # | Programme | Final URL | Target search query | Impressions | Clicks | CTR |",
    "|--:|-----------|-----------|---------------------|------------:|-------:|----:|"]
i=0
for prog in PORDER:
    for prog2,slug,s in sorted(by(prog),key=lambda x:-imp(x[2]["id"])):
        i+=1; row=demand.get(s["id"],{})
        md.append(f"| {i} | {PTITLE[prog]} | `{url(prog,slug)}` | {s.get('target_query',slug)} | "
                  f"{int(row.get('Impressions',0)):,} | {int(row.get('Clicks',0)):,} | {row.get('CTR %','')}% |")
md+=["","## Folders (Vercel deploy root = `web/`)",""]
for prog in PORDER:
    if by(prog): md.append(f"- **`web/{prog}/`** -> `/{prog}/...` - {PTITLE[prog]} ({len(by(prog))} pages)")
md+=["","Full per-query mapping: `ALL-50-LP-SUMMARY.csv` and `SEARCH-QUERIES-ALL-50.csv`."]
(ROOT/"GOOGLE-ADS-INDEX.md").write_text("\n".join(md),encoding="utf-8")

print(f"built web/ with {len(pages)} pages + index.html + vercel.json; wrote GOOGLE-ADS-INDEX.md (domain={DOMAIN or 'relative'})")
for p in PORDER:
    n=len(by(p))
    if n: print(f"  /{p}/  ({n})")
