#!/usr/bin/env python3
"""Route every Google search query (raw 'Search terms report (1).csv', All time ~4 yrs) to one
of the 50 JAIN landing pages, with real Impressions + Clicks + Cost. Program is detected first
(priority order), then the specific page within that program (specialisation, else intent, else
the program's generic course page). Off-topic / competitor queries are excluded.
Outputs SEARCH-QUERIES-ALL-50.csv (per query) + ALL-50-LP-SUMMARY.csv (50 rows) to Downloads + project."""
import csv, collections, pathlib, io, re, json
csv.field_size_limit(10**7)
RAW = pathlib.Path(r"C:\Users\User\Downloads\Search terms report (1).csv")
ROOT = pathlib.Path(__file__).parent; STORIES = ROOT / "stories"
DIRS = [pathlib.Path(r"C:\Users\User\Downloads"), ROOT]

# page registry from the story JSONs (id -> program, target query)
reg = {}
for f in STORIES.glob("*.json"):
    s = json.loads(f.read_text(encoding="utf-8"))
    if "id" not in s or "program" not in s: continue
    reg[s["id"]] = {"program": s["program"], "tq": s.get("target_query", s["id"]),
                    "spec": s.get("specialization", "")}

# program detection, priority order (least ambiguous first)
PROG = [
 ("MCA",   re.compile(r"\bmca\b|master of computer")),
 ("BCA",   re.compile(r"\bbca\b|bachelor of computer")),
 ("MBA",   re.compile(r"\bmba\b|master of business|executive mba")),
 ("BBA",   re.compile(r"\bbba\b|bachelor of business")),
 ("M.Com", re.compile(r"\bm\.?\s?com\b|master of commerce")),
 ("B.Com", re.compile(r"\bb\.?\s?com\b|bachelor of commerce")),
 ("MA",    re.compile(r"master of arts|\bma\b")),
 ("JAIN",  re.compile(r"jain")),
]
# off-topic / not-targetable (competitors + pure informational). Keep review/ranking (brand page).
OTHER = re.compile(r"\bsalary\b|\bjobs?\b|job oppor|syllabus|subjects?|\bduration\b|\bvs\b|versus|"
    r"difference between|quora|reddit|full form|what is|wikipedia|nmims|amity|manipal|symbiosis|"
    r"\blpu\b|ignou|upgrad|annamalai|gyan|dy patil|narsee|great learning|simplilearn|scaler|coursera|sikkim")

MBA_SPECS = [(p, re.compile(r)) for p, r in [
 ("mba-digital-marketing", r"digital marketing|digital-marketing"),
 ("mba-international-finance", r"international finance|\bacca\b"),
 ("mba-international-business", r"international business"),
 ("mba-data-science", r"data science|business analytics|\banalytics\b|business intelligence"),
 ("mba-healthcare", r"healthcare|health care|hospital"),
 ("mba-logistics", r"logistics|supply chain"),
 ("mba-hr", r"\bhr\b|human resource|\bhrm\b"),
 ("mba-operations", r"operations|operation management"),
 ("mba-it", r"information technology|\bit management\b|information system"),
 ("mba-project-management", r"project management"),
 ("mba-entrepreneurship", r"entrepreneur|venture"),
 ("mba-strategy-leadership", r"strategy and leadership|strategy & leadership|\bleadership\b"),
 ("mba-marketing", r"\bmarketing\b"),
 ("mba-finance", r"\bfinance\b|financial|fintech|banking|investment"),
]]

def route(prog, s):
    fee = any(k in s for k in ("fee","fees","cost","price","charges"))
    adm = any(k in s for k in ("admission","apply","eligib","application","last date","how to join","registration"))
    dist = any(k in s for k in ("distance","correspondence","from home","at home","near me","nearby","without going"))
    onl = ("online" in s) or ("virtual" in s)
    if prog == "MBA":
        for pid, pat in MBA_SPECS:
            if pat.search(s): return pid
        if fee: return "mba-fees-reveal" if "jain" in s else "mba-course-fees"
        if adm: return "mba-admission"
        if dist: return "mba-online-home"
        if onl: return "mba-online"
        return "mba-course"
    if prog == "BBA":
        if re.search(r"digital marketing", s): return "bba-digital-marketing"
        if re.search(r"\bfinance\b|financial", s): return "bba-finance"
        if fee: return "bba-fees-reveal" if "jain" in s else "bba-course-fees"
        if adm: return "bba-admission"
        if dist: return "bba-online-home"
        if onl: return "bba-online"
        return "bba-course"
    if prog == "MCA":
        if re.search(r"cyber|security", s): return "mca-cyber-security"
        if re.search(r"data science|data analytics|\banalytics\b|artificial intelligence|machine learning", s): return "mca-data-science"
        if fee: return "mca-course-fees"
        if onl or dist: return "mca-online"
        return "mca-course"
    if prog == "BCA":
        if re.search(r"data science|\banalytics\b|artificial intelligence|machine learning", s): return "bca-data-science"
        if fee: return "bca-course-fees"
        if onl or dist: return "bca-online"
        return "bca-course"
    if prog == "B.Com":
        if re.search(r"international|\bacca\b", s): return "bcom-international-finance"
        if re.search(r"accounting|finance", s): return "bcom-accounting-finance"
        if fee: return "bcom-course-fees"
        if onl or dist: return "bcom-online"
        return "bcom-course"
    if prog == "M.Com":
        if fee: return "mcom-course-fees"
        return "mcom-course"
    if prog == "MA":
        if re.search(r"english", s): return "ma-english"
        return "ma-course"
    if prog == "JAIN":
        if re.search(r"review|rating|ranking|\brank\b|placement|is it good|worth it|genuine", s): return "jain-reviews"
        if fee: return "jain-fees"
        if adm: return "jain-admission"
        return "jain-online"
    return None

def detect(s):
    for prog, pat in PROG:
        if pat.search(s): return prog
    return None

def numi(x):
    try:
        v = int(float(x.replace(",","").strip() or 0))
        return v if 0 <= v <= 2_000_000 else 0   # cap: a single search term can't exceed this over ~4yr; guards malformed rows
    except: return 0
def numf(x):
    try:
        v = float(x.replace(",","").strip() or 0)
        return v if 0 <= v <= 50_000_000 else 0.0
    except: return 0.0

pq = collections.defaultdict(lambda:[0,0,0.0])
other = [0,0,0.0,0]; n=0
with open(RAW, encoding="utf-8", newline="") as f:
    r = csv.reader(f); hdr=False
    for row in r:
        if not hdr:
            if row and row[0].strip()=="Search term":
                hdr=True; ci=row.index("Clicks"); ii=row.index("Impr."); coi=row.index("Cost")
            continue
        if len(row)<=max(ii,coi): continue
        q = row[0].strip(); ql = q.lower()
        imp, clk, cost = numi(row[ii]), numi(row[ci]), numf(row[coi])
        prog = detect(ql)
        if prog is None or OTHER.search(ql):
            other[0]+=imp; other[1]+=clk; other[2]+=cost; other[3]+=1; continue
        pid = route(prog, ql)
        if pid is None:
            other[0]+=imp; other[1]+=clk; other[2]+=cost; other[3]+=1; continue
        c = pq[(pid, ql)]; c[0]+=imp; c[1]+=clk; c[2]+=cost; n+=1
print(f"routed {n:,} query rows to 50 pages; excluded {other[3]:,} off-topic (impr {other[0]:,})")

page = collections.defaultdict(lambda:[0,0,0.0,0])
for (pid, ql),(imp,clk,cost) in pq.items():
    page[pid][0]+=imp; page[pid][1]+=clk; page[pid][2]+=cost; page[pid][3]+=1
TIMP=sum(v[0] for v in page.values()) or 1; TCLK=sum(v[1] for v in page.values()) or 1; TCOST=sum(v[2] for v in page.values()) or 1

# order: by program-total impr desc, then page impr desc
prog_tot = collections.defaultdict(int)
for pid,v in page.items(): prog_tot[reg[pid]["program"]] += v[0]
def sortkey(pid): return (-prog_tot[reg[pid]["program"]], reg[pid]["program"], -page[pid][0])
ordered = sorted(page.keys(), key=sortkey)

# ---- per-query detail ----
buf=io.StringIO(); w=csv.writer(buf)
w.writerow(["program","page","target_query","search_query","impressions","clicks","ctr_pct","avg_cpc_inr","cost_inr","pct_of_impressions","pct_of_clicks"])
for pid in ordered:
    prog=reg[pid]["program"]; tq=reg[pid]["tq"]
    for ql,imp,clk,cost in sorted(((ql,*v) for (p,ql),v in pq.items() if p==pid), key=lambda x:-x[1]):
        ctr=(clk/imp*100) if imp else 0; cpc=(cost/clk) if clk else 0
        w.writerow([prog,pid,tq,ql,imp,clk,f"{ctr:.2f}",f"{cpc:.2f}",f"{cost:.2f}",f"{imp/TIMP*100:.3f}",f"{clk/TCLK*100:.3f}"])
detail=buf.getvalue()

# ---- 50-row summary ----
buf2=io.StringIO(); w2=csv.writer(buf2)
w2.writerow(["#","Program","Page","Target query","Queries","Impressions","Clicks","CTR %","Avg CPC (INR)","Cost (INR)","% of impressions","% of clicks","% of cost"])
for i,pid in enumerate(ordered,1):
    imp,clk,cost,qc=page[pid]; ctr=(clk/imp*100) if imp else 0; cpc=(cost/clk) if clk else 0
    w2.writerow([i,reg[pid]["program"],pid,reg[pid]["tq"],qc,imp,clk,f"{ctr:.2f}",f"{cpc:.2f}",f"{cost:.0f}",f"{imp/TIMP*100:.2f}",f"{clk/TCLK*100:.2f}",f"{cost/TCOST*100:.2f}"])
w2.writerow(["","TOTAL","","",sum(v[3] for v in page.values()),TIMP,TCLK,f"{TCLK/TIMP*100:.2f}",f"{TCOST/TCLK:.2f}",f"{TCOST:.0f}","100.00","100.00","100.00"])
summ=buf2.getvalue()

for d in DIRS:
    for name,txt in [("SEARCH-QUERIES-ALL-50.csv",detail),("ALL-50-LP-SUMMARY.csv",summ)]:
        try: (d/name).write_text(txt,encoding="utf-8"); print("wrote",d/name)
        except PermissionError: print("SKIP (open):",d/name)

# console summary grouped by program
print(f"\n{'Program':<8}{'pages':>6}{'Impressions':>14}{'Clicks':>10}{'Cost(INR)':>14}")
pg=collections.defaultdict(lambda:[0,0,0.0,0])
for pid,v in page.items():
    p=reg[pid]["program"]; pg[p][0]+=v[0]; pg[p][1]+=v[1]; pg[p][2]+=v[2]; pg[p][3]+=1
for p,(imp,clk,cost,npg) in sorted(pg.items(),key=lambda x:-x[1][0]):
    print(f"{p:<8}{npg:>6}{imp:>14,}{clk:>10,}{cost:>14,.0f}")
print(f"{'TOTAL':<8}{sum(v[3] for v in pg.values()):>6}{TIMP:>14,}{TCLK:>10,}{TCOST:>14,.0f}")
