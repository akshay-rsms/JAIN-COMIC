#!/usr/bin/env python3
"""Aggregate the raw Google 'Search terms report (1).csv' (All time ~4 yrs) into the 20 MBA
landing pages with real Impressions + Clicks + Cost. Specialisation intent takes priority
over generic intent. Outputs SEARCH-QUERIES-MBA.csv (per query) + MBA-LP-SUMMARY.csv."""
import csv, collections, pathlib, io, re
RAW = pathlib.Path(r"C:\Users\User\Downloads\Search terms report (1).csv")
DIRS = [pathlib.Path(r"C:\Users\User\Downloads"), pathlib.Path(__file__).parent]
csv.field_size_limit(10**7)

PAGES = [  # (page id, label, target query)
 ("mba-hr","MBA in Human Resource Management","mba in human resource management"),
 ("mba-finance","MBA in Finance","mba in finance"),
 ("mba-healthcare","MBA in Healthcare Management","mba in healthcare management"),
 ("mba-marketing","MBA in Marketing","mba in marketing"),
 ("mba-data-science","MBA in Data Science & Analytics","mba in business analytics"),
 ("mba-logistics","MBA in Logistics & Supply Chain","mba in logistics and supply chain management"),
 ("mba-operations","MBA in Operations Management","mba in operations management"),
 ("mba-it","MBA in Information Technology Mgmt","mba in information technology management"),
 ("mba-project-management","MBA in Project Management","mba in project management"),
 ("mba-digital-marketing","MBA in Digital Marketing","mba in digital marketing"),
 ("mba-international-business","MBA in International Business","mba in international business"),
 ("mba-international-finance","MBA in International Finance","mba in international finance"),
 ("mba-entrepreneurship","MBA in Entrepreneurship","mba in entrepreneurship"),
 ("mba-strategy-leadership","MBA in Strategy & Leadership","mba in strategy and leadership"),
 ("mba-fees-reveal","MBA Fees (JAIN)","jain university mba fees"),
 ("mba-course-fees","MBA Course Fees","mba course fees"),
 ("mba-admission","MBA Admission","mba admission"),
 ("mba-online-home","MBA Distance / From Home","distance mba"),
 ("mba-online","MBA Online","online mba"),
 ("mba-course","MBA Course (generic)","mba course"),
]
LB = {p[0]:(p[1],p[2]) for p in PAGES}

# specialisation regexes, priority order (digital marketing before marketing, intl finance before finance)
SPEC = [
 ("mba-digital-marketing", r"digital marketing|digital-marketing|e-commerce|ecommerce"),
 ("mba-international-finance", r"international finance|\bacca\b"),
 ("mba-data-science", r"data science|business analytics|\banalytics\b|business intelligence|artificial intelligence|machine learning"),
 ("mba-logistics", r"logistics|supply chain|supply-chain"),
 ("mba-healthcare", r"healthcare|health care|hospital"),
 ("mba-hr", r"\bhr\b|human resource|\bhrm\b"),
 ("mba-marketing", r"\bmarketing\b"),
 ("mba-operations", r"operations|operation management"),
 ("mba-it", r"information technology|\bit management\b|information system"),
 ("mba-project-management", r"project management|project-management"),
 ("mba-international-business", r"international business"),
 ("mba-entrepreneurship", r"entrepreneur|venture creation"),
 ("mba-strategy-leadership", r"strategy and leadership|strategy & leadership|leadership"),
 ("mba-finance", r"\bfinance\b|financial|\bfintech\b|banking|investment"),
]
SPAT = [(pid, re.compile(p)) for pid, p in SPEC]

# off-topic / not-targetable queries (informational or competitor brands). These are excluded
# so each page's list is actually targetable. NOTE: we deliberately do NOT exclude logistics/
# healthcare/banking/international/entrepreneur etc. - those ARE our specialisation pages.
OTHER = re.compile(
    r"\bsalary\b|\bscope\b|\bjobs?\b|job oppor|after mba|\bbest\b|\btop \b|which is best|"
    r"\brank(ing)?\b|\brating\b|\bvs\b|versus|difference between|full form|what is|is mba worth|"
    r"\bmeaning\b|subjects?|syllabus|curriculum|\bduration\b|how many years|quora|reddit|\bwiki|"
    r"nmims|amity|manipal|symbiosis|\blpu\b|ignou|upgrad|annamalai|gyan|chandigarh univ|dy patil|"
    r"narsee|great learning|simplilearn|scaler|coursera|\bnirf\b")

def bucket(s):
    s = s.lower()
    if OTHER.search(s): return "_other"
    for pid, pat in SPAT:
        if pat.search(s): return pid
    # intent buckets
    if any(k in s for k in ("fee","fees","cost","price","charges")):
        return "mba-fees-reveal" if "jain" in s else "mba-course-fees"
    if any(k in s for k in ("admission","apply","eligib","last date","application","registration","how to join")):
        return "mba-admission"
    if any(k in s for k in ("distance","correspondence","from home","at home","near me","nearby","without going")):
        return "mba-online-home"
    if "online" in s or "virtual" in s:
        return "mba-online"
    return "mba-course"

def numi(x):
    try: return int(float(x.replace(",","").strip() or 0))
    except: return 0
def numf(x):
    try: return float(x.replace(",","").strip() or 0)
    except: return 0.0

pq = collections.defaultdict(lambda:[0,0,0.0])  # (page,query) -> impr,clk,cost
n = 0
with open(RAW, encoding="utf-8", newline="") as f:
    r = csv.reader(f); hdr = False
    for row in r:
        if not hdr:
            if row and row[0].strip()=="Search term":
                hdr=True; ci=row.index("Clicks"); ii=row.index("Impr."); coi=row.index("Cost")
            continue
        if len(row)<=max(ii,coi): continue
        q=row[0].strip()
        ql=q.lower()
        if "mba" not in ql and "business administration" not in ql: continue
        b=bucket(ql)
        cell=pq[(b,ql)]; cell[0]+=numi(row[ii]); cell[1]+=numi(row[ci]); cell[2]+=numf(row[coi])
        n+=1
print(f"processed {n:,} MBA rows -> {len(pq):,} query/page pairs")

page=collections.defaultdict(lambda:[0,0,0.0,0])
other=[0,0,0.0,0]
for (b,ql),(imp,clk,cost) in pq.items():
    tgt = other if b=="_other" else page[b]
    tgt[0]+=imp; tgt[1]+=clk; tgt[2]+=cost; tgt[3]+=1
TIMP=sum(page[p[0]][0] for p in PAGES) or 1
TCLK=sum(page[p[0]][1] for p in PAGES) or 1
TCOST=sum(page[p[0]][2] for p in PAGES) or 1
print(f"EXCLUDED (not-targetable): {other[3]:,} queries, {other[0]:,} impr, {other[1]:,} clicks "
      f"({other[0]/(other[0]+TIMP)*100:.1f}% of MBA impressions)")

buf=io.StringIO(); w=csv.writer(buf)
w.writerow(["page","target_query","search_query","impressions","clicks","ctr_pct","avg_cpc_inr","cost_inr","pct_of_impressions","pct_of_clicks"])
for pid,lab,tq in PAGES:
    for ql,imp,clk,cost in sorted(((ql,*v) for (b,ql),v in pq.items() if b==pid), key=lambda x:-x[1]):
        ctr=(clk/imp*100) if imp else 0; cpc=(cost/clk) if clk else 0
        w.writerow([lab,tq,ql,imp,clk,f"{ctr:.2f}",f"{cpc:.2f}",f"{cost:.2f}",f"{imp/TIMP*100:.3f}",f"{clk/TCLK*100:.3f}"])
detail=buf.getvalue()

buf2=io.StringIO(); w2=csv.writer(buf2)
w2.writerow(["#","Landing page","Target query","Queries","Impressions","Clicks","CTR %","Avg CPC (INR)","Cost (INR)","% of impressions","% of clicks","% of cost"])
for i,(pid,lab,tq) in enumerate(PAGES,1):
    imp,clk,cost,qc=page[pid]; ctr=(clk/imp*100) if imp else 0; cpc=(cost/clk) if clk else 0
    w2.writerow([i,lab,tq,qc,imp,clk,f"{ctr:.2f}",f"{cpc:.2f}",f"{cost:.0f}",f"{imp/TIMP*100:.1f}",f"{clk/TCLK*100:.1f}",f"{cost/TCOST*100:.1f}"])
w2.writerow(["","TOTAL","",sum(v[3] for v in page.values()),TIMP,TCLK,f"{TCLK/TIMP*100:.2f}",f"{TCOST/TCLK:.2f}",f"{TCOST:.0f}","100.0","100.0","100.0"])
summ=buf2.getvalue()

for d in DIRS:
    for name,txt in [("SEARCH-QUERIES-MBA.csv",detail),("MBA-LP-SUMMARY.csv",summ)]:
        try: (d/name).write_text(txt,encoding="utf-8"); print("wrote",d/name)
        except PermissionError: print("SKIP (open):",d/name)

print(f"\n{'#':<3}{'Landing page':<36}{'Impr':>11}{'Clicks':>9}{'CTR':>7}{'Cost(INR)':>13}{'%impr':>7}")
for i,(pid,lab,tq) in enumerate(PAGES,1):
    imp,clk,cost,qc=page[pid]; ctr=(clk/imp*100) if imp else 0
    print(f"{i:<3}{lab:<36}{imp:>11,}{clk:>9,}{ctr:>6.1f}%{cost:>13,.0f}{imp/TIMP*100:>6.1f}%")
print(f"{'':<3}{'TOTAL':<36}{TIMP:>11,}{TCLK:>9,}{TCLK/TIMP*100:>6.1f}%{TCOST:>13,.0f}{100.0:>6.1f}%")
