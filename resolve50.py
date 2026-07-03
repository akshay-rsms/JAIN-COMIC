import csv, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
CSV=r"C:\Users\User\Downloads\Search terms - grouped by count.csv"
COURSE={"MBA":r"\bmba\b","BBA":r"\bbba\b","B.Com":r"\bb\.?\s?com\b","MCA":r"\bmca\b",
        "M.Com":r"\bm\.?\s?com\b","BCA":r"\bbca\b","MA":r"\bm\.?\s?a\b"}
crx={k:re.compile(v) for k,v in COURSE.items()}
# plan: (course, label, must[], avoid[])
P=[
("MBA","online: flagship",["online"],["fee","distance","best","top","in india"]),
("MBA","online: in India",["online","in india"],[]),
("MBA","online: working professionals",["working"],[]),
("MBA","online: programs",["online","program"],[]),
("MBA","fees",["fee"],["online","distance","jain"]),
("MBA","fees: JAIN",["jain","fee"],["structure"]),
("MBA","fees: online",["online","fee"],[]),
("MBA","distance",["distance"],["fee","education"]),
("MBA","distance education",["distance","education"],[]),
("MBA","best: online",["best","online"],[]),
("MBA","best/top colleges",["top"],["online"]),
("MBA","reviews/ranking",["best"],["online","top"]),
("MBA","eligibility",["eligib"],[]),
("MBA","admission",["admission"],[]),
("MBA","generic: courses",["course"],["online","fee","distance","best","top","admission","eligib"]),
("MBA","scope/salary",["salary"],[]),
("MBA","spec: Digital Marketing",["digital marketing"],[]),
("MBA","spec: HR",["hr"],[]),
("MBA","spec: Hospital/Healthcare",["hospital"],[]),
("MBA","spec: Finance",["finance"],["digital"]),
("BBA","online",["online"],["fee"]),
("BBA","online (alt)",["bba online"],[]),
("BBA","fees: JAIN",["jain","fee"],[]),
("BBA","fees: course",["fee"],["jain"]),
("BBA","admission/eligibility",["admission"],[]),
("BBA","generic: course",["course"],["online","fee","admission"]),
("BBA","spec: Aviation",["aviation"],[]),
("BBA","spec: Digital Marketing",["digital marketing"],[]),
("B.Com","online",["online"],["student","fee"]),
("B.Com","online: for students",["online","student"],[]),
("B.Com","fees",["fee"],[]),
("B.Com","professional: ACCA",["acca"],[]),
("B.Com","admission",["admission"],[]),
("B.Com","spec: Accounting & Finance",["account"],[]),
("MCA","fees: JAIN",["jain","fee"],["structure"]),
("MCA","fees: structure",["fee","structure"],[]),
("MCA","online",["online"],["fee"]),
("MCA","distance",["distance"],[]),
("MCA","spec: Cybersecurity",["cyber"],[]),
("MCA","admission/generic",["admission"],[]),
("M.Com","distance",["distance"],[]),
("M.Com","distance (alt)",["m com","distance"],[]),
("M.Com","online",["online"],[]),
("M.Com","fees",["fee"],[]),
("MA","distance: English",["english","distance"],[]),
("MA","distance: Economics",["economics","distance"],[]),
("MA","distance: Psychology",["psychology"],[]),
("MA","online/distance",["distance"],["english","economics","psychology"]),
("BCA","fees: JAIN",["jain","fee"],[]),
("BCA","online",["online"],[]),
]
buckets={k:[] for k in COURSE}
with open(CSV,encoding="utf-8-sig") as f:
    r=csv.reader(f); next(r)
    for row in r:
        if len(row)<2: continue
        q=row[0].strip().lower()
        try: c=int(row[1])
        except: continue
        for k,rx in crx.items():
            if rx.search(q): buckets[k].append((q,c)); break
used=set(); out=[]
for i,(course,label,must,avoid) in enumerate(P,1):
    cand=[]
    for q,c in buckets[course]:
        if all(m in q for m in must) and not any(a in q for a in avoid) and q not in used:
            cand.append((q,c))
    if not cand:
        for q,c in buckets[course]:
            if all(m in q for m in must) and q not in used: cand.append((q,c))
    if cand:
        q,c=max(cand,key=lambda x:x[1]); used.add(q)
    else:
        q,c="(no match)",0
    out.append({"n":i,"course":course,"label":label,"query":q,"count":c})
    print(f"{i:02d} | {course:6} | {label:28} | {q}  ({c})")
json.dump(out,open("plan50.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
