import csv, re, sys
sys.stdout.reconfigure(encoding="utf-8")
CSV=r"C:\Users\User\Downloads\Search terms - grouped by count.csv"
COURSE={"MBA":r"\bmba\b","BBA":r"\bbba\b","B.Com":r"\bb\.?\s?com\b","MCA":r"\bmca\b",
        "M.Com":r"\bm\.?\s?com\b","BCA":r"\bbca\b","MA":r"\bm\.?\s?a\b"}
crx={k:re.compile(v) for k,v in COURSE.items()}
SPEC=re.compile(r"finance|marketing|\bhr\b|human resource|operations|analytics|information technology|international|health|hospital|logistics|supply chain|entrepreneur|banking|project management|data science|artificial intelligence|machine learning|\bai\b|cloud|cyber|software|development|english|economics|psychology|political|public policy|aviation|taxation|\btax\b|account|corporate")
def intent(q):
    if re.search(r"\bfee|fees|cost|structure\b",q): return "fees"
    if "distance" in q: return "distance"
    if "online" in q: return "online"
    if re.search(r"admission|eligibil|apply|criteria|last date|how to",q): return "admission"
    if re.search(r"placement|salary|scope|\bjobs?\b|career|worth",q): return "career"
    if re.search(r"\bbest\b|\btop\b|ranking|review|which|\bvs\b|compare",q): return "compare"
    if SPEC.search(q): return "specialization"
    return "generic"
tot={}; spec_tot={}; overall={}
with open(CSV,encoding="utf-8-sig") as f:
    r=csv.reader(f); next(r)
    for row in r:
        if len(row)<2: continue
        q=row[0].strip().lower()
        try: c=int(row[1])
        except: continue
        for k,rx in crx.items():
            if rx.search(q):
                it=intent(q)
                tot[(k,it)]=tot.get((k,it),0)+c
                overall[it]=overall.get(it,0)+c
                break
print("=== Per-course volume by INTENT (count sum) ===")
order=["MBA","BBA","B.Com","MCA","M.Com","BCA","MA"]
intents=["online","fees","distance","specialization","admission","career","compare","generic"]
print("course     "+" ".join(f"{i[:6]:>8}" for i in intents))
for co in order:
    print(f"{co:<10} "+" ".join(f"{tot.get((co,i),0):>8}" for i in intents))
print("\n=== Overall intent totals (all courses) ===")
for i,v in sorted(overall.items(),key=lambda x:-x[1]): print(f"{i:<14}{v:>9}")
