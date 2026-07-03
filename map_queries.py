import csv, re, sys
sys.stdout.reconfigure(encoding="utf-8")
CSV=r"C:\Users\User\Downloads\Search terms - grouped by count.csv"

# course -> word-boundary regex
COURSE={
 "MBA":r"\bmba\b","BBA":r"\bbba\b","B.Com":r"\bb\.?\s?com\b","MCA":r"\bmca\b",
 "M.Com":r"\bm\.?\s?com\b","BCA":r"\bbca\b","MA":r"\bm\.?\s?a\b",
}
# 50 stories in order: (course, spec-label, [spec regex tokens])
STORIES=[
("MBA","Finance",[r"\bfinance\b",r"\bfinancial\b"]),
("MBA","Marketing",[r"\bmarketing\b"]),
("MBA","Human Resources",[r"\bhr\b",r"human resource"]),
("MBA","Operations",[r"\boperations?\b"]),
("MBA","Business Analytics",[r"business analytics",r"\banalytics\b"]),
("MBA","Information Technology",[r"information technology",r"\bit\b",r"\bsystems?\b"]),
("MBA","International Business",[r"international business",r"\binternational\b"]),
("MBA","Healthcare Management",[r"health\s?care",r"\bhospital\b",r"\bhealth\b"]),
("MBA","Logistics & Supply Chain",[r"logistics",r"supply chain"]),
("MBA","Finance (career switch)",[r"\bfinance\b"]),
("MBA","Digital Marketing",[r"digital marketing"]),
("MBA","Data Science",[r"data science",r"data analytics"]),
("MBA","Entrepreneurship",[r"entrepreneur"]),
("MBA","Banking & Finance",[r"\bbanking\b"]),
("MBA","Project Management",[r"project management"]),
("MBA","Online (mid-career)",[]),
("BBA","Finance",[r"\bfinance\b"]),
("BBA","Marketing",[r"\bmarketing\b"]),
("BBA","Human Resources",[r"\bhr\b",r"human resource"]),
("BBA","Digital Marketing",[r"digital marketing"]),
("BBA","Data Science & AI",[r"data science",r"\bai\b",r"artificial intelligence",r"data analytics"]),
("BBA","Aviation Management",[r"aviation"]),
("BBA","Logistics",[r"logistics",r"supply chain"]),
("BBA","Business Analytics",[r"analytics"]),
("B.Com","Accounting",[r"account"]),
("B.Com","Finance",[r"\bfinance\b"]),
("B.Com","Taxation",[r"tax"]),
("B.Com","Banking",[r"bank"]),
("B.Com","Professional (global)",[r"acca",r"professional",r"international",r"global"]),
("B.Com","Corporate Accounting",[r"corporate",r"account"]),
("MCA","Full-Stack Development",[r"full.?stack",r"development",r"developer",r"software"]),
("MCA","Data Science",[r"data science"]),
("MCA","AI & Machine Learning",[r"artificial intelligence",r"machine learning",r"\bai\b",r"\bml\b"]),
("MCA","Cloud Computing",[r"cloud"]),
("MCA","Cybersecurity",[r"cyber",r"security"]),
("MCA","Software Engineering",[r"software"]),
("M.Com","Accounting & Finance",[r"\bfinance\b",r"account"]),
("M.Com","Taxation",[r"tax"]),
("M.Com","Banking & Finance",[r"bank"]),
("M.Com","Business Analytics",[r"analytics"]),
("M.Com","Corporate",[r"corporate"]),
("BCA","Software Development",[r"software",r"development",r"developer"]),
("BCA","Data Analytics",[r"data analytics",r"analytics",r"data science"]),
("BCA","Cloud & DevOps",[r"cloud",r"devops"]),
("BCA","Cybersecurity",[r"cyber",r"security"]),
("BCA","Artificial Intelligence",[r"artificial intelligence",r"\bai\b",r"machine learning"]),
("MA","English",[r"english"]),
("MA","Economics",[r"economics"]),
("MA","Psychology",[r"psychology"]),
("MA","Public Policy",[r"political science",r"public policy",r"political",r"public administration"]),
]
crx={k:re.compile(v) for k,v in COURSE.items()}
buckets={k:[] for k in COURSE}
with open(CSV,encoding="utf-8-sig") as f:
    r=csv.reader(f); next(r)
    for row in r:
        if len(row)<2: continue
        q=row[0].strip().lower()
        try: c=int(row[1])
        except: continue
        for k,rx in crx.items():
            if rx.search(q): buckets[k].append((q,c))
# course generic top (fee/online oriented)
def course_top(course):
    b=buckets[course]
    return max(b,key=lambda x:x[1]) if b else ("(none)",0)
print("STORY | COURSE | SPEC | TARGET QUERY | COUNT | TYPE")
for i,(course,spec,toks) in enumerate(STORIES,1):
    b=buckets[course]
    best=None
    if toks:
        rxs=[re.compile(t) for t in toks]
        cand=[(q,c) for (q,c) in b if any(rx.search(q) for rx in rxs)]
        if cand: best=max(cand,key=lambda x:x[1])
    if best:
        typ="specific"
    else:
        best=course_top(course); typ="broad/flagship"
    print(f"{i:02d} | {course} | {spec} | {best[0]} | {best[1]} | {typ}")
